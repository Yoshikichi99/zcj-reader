using System;
using System.Diagnostics;
using System.IO;
using System.IO.Compression;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;
using System.Threading;
using System.Windows.Forms;
using Microsoft.Web.WebView2.Core;
using Microsoft.Web.WebView2.WinForms;

namespace ZCJReader
{
    internal static class Program
    {
        internal const string WindowTitle = "莊春江讀經站 · 離線版";
        private static readonly Assembly Self = Assembly.GetExecutingAssembly();

        [DllImport("user32.dll", CharSet = CharSet.Unicode)]
        private static extern IntPtr FindWindow(string cls, string title);

        [DllImport("user32.dll")]
        private static extern bool SetForegroundWindow(IntPtr h);

        [DllImport("user32.dll")]
        private static extern bool ShowWindow(IntPtr h, int cmd);

        [DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
        internal static extern bool SetDllDirectory(string path);

        internal static void Log(string m)
        {
            try
            {
                string dir = Path.Combine(
                    Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
                    "ZCJReader");
                string path = Path.Combine(dir, "startup.log");
                try
                {
                    Directory.CreateDirectory(dir);
                    File.AppendAllText(path, DateTime.Now.ToString("HH:mm:ss") + " " + m + "\r\n");
                }
                catch
                {
                    string alt = Path.Combine(Path.GetTempPath(), "ZCJReader_startup.log");
                    File.AppendAllText(alt, DateTime.Now.ToString("HH:mm:ss") + " " + m + "\r\n");
                }
            }
            catch { }
        }

        [STAThread]
        private static void Main()
        {
            RegisterResolver();

            bool created;
            using (var mutex = new Mutex(true, "Global\\ZCJReader_SingleInstance", out created))
            {
                if (!created)
                {
                    IntPtr h = FindWindow(null, WindowTitle);
                    if (h != IntPtr.Zero)
                    {
                        ShowWindow(h, 9);
                        SetForegroundWindow(h);
                    }
                    else
                    {
                        MessageBox.Show("程式已在執行中。", "莊春江讀經站",
                            MessageBoxButtons.OK, MessageBoxIcon.Information);
                    }
                    return;
                }

                Log("single-file start .NET " + Environment.Version);
                Application.EnableVisualStyles();
                Application.SetCompatibleTextRenderingDefault(false);
                try
                {
                    RunApp();
                    Log("run returned");
                }
                catch (Exception ex)
                {
                    Log("exception: " + ex);
                    MessageBox.Show("啟動失敗：\n" + ex.Message, "莊春江讀經站",
                        MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
        }

        [MethodImpl(MethodImplOptions.NoInlining)]
        private static void RunApp()
        {
            Application.Run(new MainForm());
        }

        /// <summary>从内嵌资源加载 WebView2 托管程序集，不落地。</summary>
        private static void RegisterResolver()
        {
            AppDomain.CurrentDomain.AssemblyResolve += delegate (object sender, ResolveEventArgs e)
            {
                string name = new AssemblyName(e.Name).Name + ".dll";
                try
                {
                    using (Stream st = Self.GetManifestResourceStream(name))
                    {
                        if (st == null) return null;
                        byte[] buf = new byte[st.Length];
                        int read = 0;
                        while (read < buf.Length)
                        {
                            int n = st.Read(buf, read, buf.Length - read);
                            if (n <= 0) break;
                            read += n;
                        }
                        return Assembly.Load(buf);
                    }
                }
                catch (Exception ex)
                {
                    Log("resolve fail " + name + ": " + ex.Message);
                    return null;
                }
            };
        }

        /// <summary>把内嵌的 WebView2Loader.dll 释放到临时目录（仅约 195 KB）。</summary>
        internal static string PrepareLoader()
        {
            string arch = IntPtr.Size == 8 ? "x64" : "x86";

            string[] candidates = new string[] {
                Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
                    "ZCJReader", "loader", arch),
                Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData),
                    "ZCJReader", "loader", arch),
                Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.CommonApplicationData),
                    "ZCJReader", "loader", arch),
                Path.Combine(Path.GetTempPath(), "ZCJReader", "loader", arch),
                Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "loader", arch)
            };

            Exception last = null;
            foreach (string dir in candidates)
            {
                try
                {
                    Directory.CreateDirectory(dir);
                    string dll = Path.Combine(dir, "WebView2Loader.dll");
                    using (Stream st = Self.GetManifestResourceStream("loader_" + arch + ".dll"))
                    {
                        if (st == null) throw new InvalidOperationException("內嵌 loader 遺失");
                        byte[] buf = new byte[st.Length];
                        st.Read(buf, 0, buf.Length);
                        File.WriteAllBytes(dll, buf);
                    }
                    SetDllDirectory(dir);
                    Log("loader ok " + dir);
                    return dir;
                }
                catch (Exception ex)
                {
                    last = ex;
                    Log("loader path failed " + dir + ": " + ex.Message);
                }
            }

            throw new IOException(
                "無法寫入 WebView2 載入器檔案。\n已嘗試：\n  " + string.Join("\n  ", candidates) +
                "\n\n最後錯誤：" + (last == null ? "未知" : last.Message),
                last);
        }
    }

    internal sealed class MainForm : Form
    {
        private readonly WebView2 _web;
        private static ZipArchive _zip;
        private static CoreWebView2Environment _env;

        public MainForm()
        {
            Text = Program.WindowTitle;
            Width = 1280;
            Height = 880;
            MinimumSize = new System.Drawing.Size(760, 520);
            StartPosition = FormStartPosition.CenterScreen;
            BackColor = System.Drawing.Color.FromArgb(239, 255, 222);

            _web = new WebView2();
            _web.Dock = DockStyle.Fill;
            Controls.Add(_web);
            Program.Log("form ctor");
            Load += async delegate { await InitAsync(); };
        }

        private static string BaseDir
        {
            get { return AppDomain.CurrentDomain.BaseDirectory; }
        }

        private static string PickDataDir()
        {
            // 默认放在用户目录，程序文件夹保持「只有一个 exe」；
            // 若 exe 旁存在 portable.txt，则改为便携模式（数据放在 exe 旁）。
            bool portableMode = File.Exists(Path.Combine(BaseDir, "portable.txt"));

            string portable = Path.Combine(BaseDir, "userdata");
            string local = Path.Combine(
                Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
                "ZCJReader", "WebView2");
            string roaming = Path.Combine(
                Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData),
                "ZCJReader", "WebView2");
            string common = Path.Combine(
                Environment.GetFolderPath(Environment.SpecialFolder.CommonApplicationData),
                "ZCJReader", "WebView2");

            string[] order = portableMode
                ? new string[] { portable, local, roaming }
                : new string[] { local, roaming, common, portable };

            Exception last = null;
            foreach (string dir in order)
            {
                try
                {
                    Directory.CreateDirectory(dir);
                    string probe = Path.Combine(dir, ".writable");
                    File.WriteAllText(probe, "1");
                    File.Delete(probe);
                    Program.Log("data dir " + dir);
                    return dir;
                }
                catch (Exception ex)
                {
                    last = ex;
                    Program.Log("data dir failed " + dir + ": " + ex.Message);
                }
            }
            throw new IOException("無法建立資料目錄：" + (last == null ? "未知" : last.Message), last);
        }

        private static void OpenZip()
        {
            if (_zip != null) return;
            Stream st = Assembly.GetExecutingAssembly().GetManifestResourceStream("ui.zip");
            if (st == null) throw new InvalidOperationException("內嵌資料遺失（ui.zip）");
            var ms = new MemoryStream();
            st.CopyTo(ms);
            ms.Position = 0;
            _zip = new ZipArchive(ms, ZipArchiveMode.Read);
            Program.Log("zip entries " + _zip.Entries.Count);
        }

        private static string Mime(string path)
        {
            string ext = Path.GetExtension(path).ToLowerInvariant();
            switch (ext)
            {
                case ".html": case ".htm": return "text/html; charset=utf-8";
                case ".js": return "application/javascript; charset=utf-8";
                case ".css": return "text/css; charset=utf-8";
                case ".json": return "application/json; charset=utf-8";
                case ".gz": return "application/gzip";
                case ".png": return "image/png";
                case ".jpg": case ".jpeg": return "image/jpeg";
                case ".gif": return "image/gif";
                case ".svg": return "image/svg+xml";
                case ".ico": return "image/x-icon";
                default: return "application/octet-stream";
            }
        }

        private static void OnResource(object sender, CoreWebView2WebResourceRequestedEventArgs e)
        {
            try
            {
                var uri = new Uri(e.Request.Uri);
                string path = Uri.UnescapeDataString(uri.AbsolutePath);
                if (string.IsNullOrEmpty(path) || path == "/") path = "/index.html";
                string rel = path.TrimStart('/');

                ZipArchiveEntry entry = _zip.GetEntry(rel);
                if (entry == null && !rel.EndsWith(".html", StringComparison.OrdinalIgnoreCase))
                    entry = _zip.GetEntry(rel + ".html");

                if (entry == null)
                {
                    e.Response = _env.CreateWebResourceResponse(null, 404, "Not Found",
                        "Content-Type: text/plain; charset=utf-8");
                    Program.Log("404 " + rel);
                    return;
                }

                var ms = new MemoryStream();
                using (Stream es = entry.Open()) es.CopyTo(ms);
                ms.Position = 0;
                e.Response = _env.CreateWebResourceResponse(ms, 200, "OK",
                    "Content-Type: " + Mime(rel) + "\r\nCache-Control: no-store");
            }
            catch (Exception ex)
            {
                Program.Log("resource fail: " + ex.Message);
                try
                {
                    e.Response = _env.CreateWebResourceResponse(null, 500, "Error",
                        "Content-Type: text/plain");
                }
                catch { }
            }
        }

        private async System.Threading.Tasks.Task InitAsync()
        {
            Program.Log("load event");
            try
            {
                OpenZip();
            }
            catch (Exception ex)
            {
                Program.Log("zip fail: " + ex);
                MessageBox.Show("程式檔案損壞（內嵌資料無法讀取），請重新下載。",
                    "莊春江讀經站", MessageBoxButtons.OK, MessageBoxIcon.Error);
                Close();
                return;
            }

            string loaderDir;
            try
            {
                loaderDir = Program.PrepareLoader();
            }
            catch (Exception ex)
            {
                Program.Log("loader fatal: " + ex);
                MessageBox.Show(ex.Message, "無法初始化（WebView2 載入器）",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
                Close();
                return;
            }

            Program.Log("loader " + loaderDir);
            string dataDir = PickDataDir();
            Program.Log("dataDir=" + dataDir);

            try
            {
                var envOptions = new CoreWebView2EnvironmentOptions("--disk-cache-size=52428800");
                _env = await CoreWebView2Environment.CreateAsync(null, dataDir, envOptions);
                Program.Log("env ok " + _env.BrowserVersionString);
                await _web.EnsureCoreWebView2Async(_env);
                Program.Log("webview ok");

                CoreWebView2 core = _web.CoreWebView2;
                core.AddWebResourceRequestedFilter("https://app.local/*",
                    CoreWebView2WebResourceContext.All);
                core.WebResourceRequested += OnResource;
                core.Settings.AreDevToolsEnabled = false;
                core.Settings.IsStatusBarEnabled = false;
                core.Settings.AreBrowserAcceleratorKeysEnabled = true;
                core.Settings.AreDefaultContextMenusEnabled = true;
                core.Settings.IsZoomControlEnabled = false;

                core.Navigate("https://app.local/index.html");
                Program.Log("navigate");
            }
            catch (Exception ex)
            {
                Program.Log("init fail: " + ex);
                DialogResult r = MessageBox.Show(
                    "無法啟動內嵌瀏覽器（WebView2）。\n\n" +
                    "本程式需要系統安裝「Microsoft Edge WebView2 Runtime」。\n" +
                    "Windows 10（1803 以後）與 Windows 11 通常已內建；\n" +
                    "若缺少，可到微軟官方頁面下載安裝：\n\n" +
                    "https://developer.microsoft.com/microsoft-edge/webview2/\n\n" +
                    "是否打開下載頁面？",
                    "缺少 WebView2 Runtime",
                    MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                if (r == DialogResult.Yes)
                {
                    try { Process.Start("https://developer.microsoft.com/microsoft-edge/webview2/"); }
                    catch { }
                }
                Close();
            }
        }
    }
}
