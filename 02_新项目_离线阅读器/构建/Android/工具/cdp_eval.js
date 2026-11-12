// 通用 CDP 求值：node cdp_eval.js <表达式文本文件>
// 前提：adb forward tcp:9222 localabstract:webview_devtools_remote_<pid>
const fs = require("fs");
const http = require("http");

function target() {
  return new Promise((res, rej) => {
    http.get("http://127.0.0.1:9222/json", r => {
      let b = ""; r.on("data", c => (b += c));
      r.on("end", () => {
        const t = JSON.parse(b).find(x => x.type === "page");
        t ? res(t) : rej(new Error("no page"));
      });
    }).on("error", rej);
  });
}

(async () => {
  const expr = fs.readFileSync(process.argv[2], "utf8");
  const t = await target();
  const ws = new WebSocket(t.webSocketDebuggerUrl);
  const timer = setTimeout(() => { console.error("timeout"); process.exit(2); }, 20000);
  ws.onopen = () => ws.send(JSON.stringify({
    id: 1, method: "Runtime.evaluate",
    params: { expression: expr, returnByValue: true, awaitPromise: true },
  }));
  ws.onmessage = e => {
    const m = JSON.parse(e.data);
    if (m.id !== 1) return;
    clearTimeout(timer);
    if (m.result && m.result.exceptionDetails) {
      console.error("EXCEPTION", JSON.stringify(m.result.exceptionDetails).slice(0, 400));
    } else {
      const v = m.result.result.value;
      console.log(typeof v === "string" ? v : JSON.stringify(v, null, 1));
    }
    ws.close();
    process.exit(0);
  };
  ws.onerror = () => { console.error("ws error"); process.exit(1); };
})();
