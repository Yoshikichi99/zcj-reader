using System;
using System.IO;
class P {
  [STAThread] static void Main() {
    File.WriteAllText(Path.Combine(AppContext.BaseDirectory, "mini.log"), "ran " + DateTime.Now);
  }
}
