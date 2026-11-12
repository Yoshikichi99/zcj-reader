// 定位「凡例」文本所在元素的祖先链宽度，查清横向裁切来自哪一层。
const http = require("http");

function getTarget() {
  return new Promise((res, rej) => {
    http.get("http://127.0.0.1:9222/json", r => {
      let b = ""; r.on("data", c => (b += c));
      r.on("end", () => res(JSON.parse(b).find(x => x.type === "page")));
    }).on("error", rej);
  });
}
function ev(url, expression) {
  return new Promise((res, rej) => {
    const ws = new WebSocket(url);
    ws.onopen = () => ws.send(JSON.stringify({ id: 1, method: "Runtime.evaluate",
      params: { expression, returnByValue: true } }));
    ws.onmessage = e => {
      const m = JSON.parse(e.data);
      if (m.id === 1) { ws.close(); res(m.result.result.value); }
    };
    ws.onerror = () => rej(new Error("ws error"));
  });
}
(async () => {
  const t = await getTarget();
  const expr = `(() => {
    const el = [...document.querySelectorAll('body *')].find(e =>
      e.textContent && e.textContent.indexOf('凡\\u3000例') >= 0 && e.children.length < 4);
    if (!el) return 'not found';
    const out = [];
    let n = el;
    while (n && n !== document.documentElement) {
      const r = n.getBoundingClientRect(), cs = getComputedStyle(n);
      out.push(n.tagName.toLowerCase() + (n.className ? '.' + String(n.className).trim() : '')
        + ' w=' + Math.round(r.width) + ' x=' + Math.round(r.x)
        + ' ws=' + cs.whiteSpace + ' ov=' + cs.overflowX + ' fz=' + cs.fontSize
        + ' tbl=' + cs.tableLayout);
      n = n.parentElement;
    }
    return out.join('\\n');
  })()`;
  console.log(await ev(t.webSocketDebuggerUrl, expr));
})().catch(e => { console.error("ERR", e.message); process.exit(1); });
