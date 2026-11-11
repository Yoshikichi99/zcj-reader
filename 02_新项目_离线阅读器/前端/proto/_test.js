// Node 侧验证：模拟前端的加载与拼装流程（直接读文件，不经过 HTTP）
const fs = require("fs");
const path = require("path");
const zlib = require("zlib");

const DIR = path.join(__dirname, "data");
function loadGz(rel) {
  return JSON.parse(zlib.gunzipSync(fs.readFileSync(path.join(DIR, rel))).toString("utf8"));
}

const t0 = Date.now();
const pages = loadGz("pages.json.gz");
const pali = loadGz("pali.json.gz");
const toc = loadGz("toc.json.gz");
const corpus = {};
for (const c of ["SA", "SN", "MA", "MN", "DA", "DN", "AA", "AN", "ZA", "OTHER"]) {
  Object.assign(corpus, loadGz("corpus/" + c + ".json.gz"));
}
const t1 = Date.now();
console.log("load ms:", t1 - t0, "pages:", Object.keys(pages).length,
  "pali:", Object.keys(pali).length, "corpus:", Object.keys(corpus).length,
  "toc cats:", toc.cats.length, "books(items):", toc.books.length, "docs:", toc.docs.length);

function build(pid) {
  const rec = pages[pid];
  if (!rec) return null;
  const [nm, keys, ov, cmp, pids, cat, num, pres] = rec;
  let content = "";
  for (const k of keys) content += (pres && pres[k] ? pres[k] : "") + (ov[k] || corpus[k] || "");
  const paliHtml = (pids || []).map(id => pali[id] || "").join("<br>");
  return { nm, keys, contentLen: content.length, paliLen: paliHtml.length, cmpLen: (cmp || "").length };
}

for (const pid of ["SA/SA0073.htm", "SA/SA0001.htm", "SN/SN0544.htm", "AA/AA011.htm",
  "Ap/Ap1.htm", "book/bb/bb01.htm", "study/note.htm"]) {
  const b = build(pid);
  console.log(pid, b ? b : "(不在 pages，走 books/docs)");
}

const d = build("SA/SA0073.htm");
if (d) {
  const text = Object.entries(corpus).length;
  console.log("SA0073 keys:", d.keys.join(" | "));
  console.log("SA0073 文字前缀:", d.nm);
}
