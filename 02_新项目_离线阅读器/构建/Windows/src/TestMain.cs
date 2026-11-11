using System;
using System.IO;
using System.Windows.Forms;
using Microsoft.Web.WebView2.Core;

internal static class TestMain
{
    [STAThread]
    private static void Main()
    {
        Console.WriteLine("stage1: CLR ok, framework=" + Environment.Version);
        try
        {
            Application.EnableVisualStyles();
            using (var f = new Form())
            {
                Console.WriteLine("stage2: WinForms ok, handle=" + f.Handle);
            }
        }
        catch (Exception e)
        {
            Console.WriteLine("stage2 FAIL: " + e);
            return;
        }
        try
        {
            string dataDir = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "userdata_test");
            Directory.CreateDirectory(dataDir);
            var env = CoreWebView2Environment.CreateAsync(null, dataDir).GetAwaiter().GetResult();
            Console.WriteLine("stage3: WebView2 env ok: " + (env != null) + " browser=" + env.BrowserVersionString);
        }
        catch (Exception e)
        {
            Console.WriteLine("stage3 FAIL: " + e.GetType().Name + " " + e.Message);
        }
        Console.WriteLine("done");
    }
}
