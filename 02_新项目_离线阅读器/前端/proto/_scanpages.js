const z = require("zlib"), fs = require("fs");
const t = JSON.parse(z.gunzipSync(fs.readFileSync(__dirname + "/data/toc.json.gz")));
for (const c of t.cats) {
  const p = c.page || "";
  const open = (p.match(/<table/gi) || []).length;
  const close = (p.match(/<\/table/gi) || []).length;
  const tr = (p.match(/<tr/gi) || []).length;
  const trc = (p.match(/<\/tr/gi) || []).length;
  const td = (p.match(/<td/gi) || []).length;
  const tdc = (p.match(/<\/td/gi) || []).length;
  const forms = (p.match(/<form/g) || []).length;
  const style = (p.match(/<style[\s>=]/gi) || []).length;
  const bad = (open !== close) || (tr !== trc) || (style > 0);
  if (bad) console.log(c.id, "len", p.length, "table", open, close, "tr", tr, trc, "td", td, tdc, "forms", forms, "style", style);
}
