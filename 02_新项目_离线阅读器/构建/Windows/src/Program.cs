using System;
using System.Diagnostics;
using System.IO;
using System.Runtime.InteropServices;
using System.Threading;
using System.Windows.Forms;
using Microsoft.Web.WebView2.Core;
using Microsoft.Web.WebView2.WinForms;

namespace ZCJReader
{
    internal static class Program
    {
        internal static void Log(string m)
        {
            try
            {
                File.AppendAllText(
                    Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "startup.log"),
                    DateTime.Now.ToString("HH:mm:ss") + " " + m + "\r\n");
            }
            catch { }
        }

        [DllImport("user32.dll", CharSet = CharSet.Unicode)]
        private static extern IntPtr FindWindow(string cls, string title);

        [DllImport("user32.dll")]
        private static extern bool SetForegroundWindow(IntPtr h);

        [DllImport("user32.dll")]
        private static extern bool ShowWindow(IntPtr h, int cmd);

        [DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
        internal static extern bool SetDllDirectory(string path);

        internal const string WindowTitle = "莊春江讀經站 · 離線版";

        [STAThread]
        private static void Main()
        {
            bool created;
            using (var mutex = new Mutex(true, "Global\\ZCJReader_SingleInstance", out created))
            {
                if (!created)
                {
                    IntPtr h = FindWindow(null, WindowTitle);
                    if (h != IntPtr.Zero)
                    {
                        ShowWindow(h, 9);        // SW_RESTORE
                        SetForegroundWindow(h);
                    }
                    else
                    {
                        MessageBox.Show("程式已在執行中。", "莊春江讀經站",
                            MessageBoxButtons.OK, MessageBoxIcon.Information);
                    }
                    return;
                }

                Log("main start .NET " + Environment.Version);
                Application.EnableVisualStyles();
                Application.SetCompatibleTextRenderingDefault(false);
                try
                {
                    Application.Run(new MainForm());
                    Log("run returned");
                }
                catch (Exception ex)
                {
                    Log("exception: " + ex);
                    MessageBox.Show(
                        "啟動失敗：\n" + ex.Message,
                        "莊春江讀經站",
                        MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
        }
    }

    internal sealed class MainForm : Form
    {
        private readonly WebView2 _web;

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
            string portable = Path.Combine(BaseDir, "userdata");
            try
            {
                Directory.CreateDirectory(portable);
                string probe = Path.Combine(portable, ".writable");
                File.WriteAllText(probe, "1");
                File.Delete(probe);
                return portable;
            }
            catch
            {
                string local = Path.Combine(
                    Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
                    "ZCJReader", "WebView2");
                Directory.CreateDirectory(local);
                return local;
            }
        }

        /// <summary>按进程位数选择 WebView2Loader.dll 所在目录。</summary>
        internal static void PrepareLoader()
        {
            string arch = IntPtr.Size == 8 ? "x64" : "x86";
            string dir = Path.Combine(BaseDir, "loader", arch);
            if (Directory.Exists(dir)) Program.Log("loader dir " + dir);
            Program.SetDllDirectory(dir);
        }

        private static bool CheckFiles()
        {
            string[] need = {
                Path.Combine(BaseDir, "ui", "index.html"),
                Path.Combine(BaseDir, "ui", "app.js"),
                Path.Combine(BaseDir, "ui", "data", "toc.json.gz"),
                Path.Combine(BaseDir, "ui", "data", "pages.json.gz"),
                Path.Combine(BaseDir, "ui", "data", "pali.json.gz"),
            };
            foreach (string f in need)
            {
                if (!File.Exists(f))
                {
                    Program.Log("missing file " + f);
                    MessageBox.Show(
                        "安裝不完整，缺少檔案：\n" + f +
                        "\n\n請重新解壓縮整個資料夾，不要把 exe 單獨拿出。",
                        "莊春江讀經站", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return false;
                }
            }
            return true;
        }

        private async System.Threading.Tasks.Task InitAsync()
        {
            Program.Log("load event");
            if (!CheckFiles()) { Close(); return; }

            PrepareLoader();
            string ui = Path.Combine(BaseDir, "ui");
            string dataDir = PickDataDir();
            Program.Log("dataDir=" + dataDir);

            try
            {
                CoreWebView2Environment env =
                    await CoreWebView2Environment.CreateAsync(null, dataDir);
                Program.Log("env ok " + env.BrowserVersionString);
                await _web.EnsureCoreWebView2Async(env);
                Program.Log("webview ok");

                CoreWebView2 core = _web.CoreWebView2;
                core.SetVirtualHostNameToFolderMapping(
                    "app.local", ui, CoreWebView2HostResourceAccessKind.Allow);
                core.Settings.AreDevToolsEnabled = false;
                core.Settings.IsStatusBarEnabled = false;
                // 允许 Ctrl+C / Ctrl+V 与右键菜单，保证复制粘贴可用
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
