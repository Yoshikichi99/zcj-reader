// 通过 WebView DevTools 协议读页面实际布局宽度，定位横向溢出的元素。
// 用法：node layout_probe.js [hash]
// 前提：adb forward tcp:9222 localabstract:webview_devtools_remote_<pid>
const http = require("http");

function getTargets() {
  return new Promise((res, rej) => {
    http.get("http://127.0.0.1:9222/json", r => {
      let b = "";
      r.on("data", c => (b += c));
      r.on("end", () => res(JSON.parse(b)));
    }).on("error", rej);
  });
}

function evalIn(url, expression) {
  return new Promise((res, rej) => {
    const ws = new WebSocket(url);
    const timer = setTimeout(() => { try { ws.close(); } catch (e) {} rej(new Error("timeout")); }, 15000);
    ws.onopen = () => ws.send(JSON.stringify({
      id: 1, method: "Runtime.evaluate",
      params: { expression, returnByValue: true, awaitPromise: true },
    }));
    ws.onmessage = e => {
      const m = JSON.parse(e.data);
      if (m.id === 1) {
        clearTimeout(timer);
        ws.close();
        if (m.result && m.result.exceptionDetails) return rej(new Error(JSON.stringify(m.result.exceptionDetails)));
        res(m.result && m.result.result ? m.result.result.value : null);
      }
    };
    ws.onerror = e => { clearTimeout(timer); rej(new Error("ws error")); };
  });
}

(async () => {
  const hash = process.argv[2];
  const t = (await getTargets()).find(x => x.type === "page");
  if (!t) throw new Error("no page target");
  if (hash) {
    await evalIn(t.webSocketDebuggerUrl, `location.hash=${JSON.stringify(hash)}`);
    await new Promise(r => setTimeout(r, 1500));
  }
  const expr = `(() => {
    const vw = Math.round(window.innerWidth);
    const de = document.documentElement;
    const wide = [...document.querySelectorAll('body *')]
      .map(el => ({el, r: el.getBoundingClientRect(), s: getComputedStyle(el)}))
      .filter(x => x.r.width > vw + 1 || x.r.right > vw + 1)
      .slice(0, 12)
      .map(x => x.el.tagName.toLowerCase() + (x.el.id ? '#'+x.el.id : '') +
        (x.el.className && typeof x.el.className === 'string' ? '.'+x.el.className.trim().split(/\\s+/).join('.') : '') +
        ' w=' + Math.round(x.r.width) + ' right=' + Math.round(x.r.right));
    return JSON.stringify({
      vw, scrollW: de.scrollWidth, bodyW: document.body.scrollWidth,
      scrollLeft: de.scrollLeft || window.scrollX,
      wide
    }, null, 1);
  })()`;
  console.log(await evalIn(t.webSocketDebuggerUrl, expr));
})().catch(e => { console.error("ERR", e.message); process.exit(1); });
