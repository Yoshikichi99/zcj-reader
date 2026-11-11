const z = require("zlib"), fs = require("fs");
const D = __dirname + "/data/";
const load = f => JSON.parse(z.gunzipSync(fs.readFileSync(D + f)));
const toc = load("toc.json.gz");
const pages = load("pages.json.gz");
const corpus = {};
for (const c of ["SA", "SN", "MA", "MN", "DA", "DN", "AA", "AN", "ZA", "OTHER"])
  Object.assign(corpus, load("corpus/" + c + ".json.gz"));

const strip = h => String(h || "").replace(/<script[\s\S]*?<\/script>/gi, "")
  .replace(/<[^>]+>/g, "").replace(/&nbsp;/g, " ").replace(/&amp;/g, "&")
  .replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"');

function pageText(pid) {
  const rec = pages[pid];
  let s = "";
  if (rec) {
    for (const k of rec[1]) s += (rec[2][k] || corpus[k] || "");
    s += rec[3] || "";
  } else {
    const st = toc.static && toc.static[pid.replace(/\.htm$/i, "")];
    if (st) s = st;
  }
  return strip(s);
}

function search(cat, q) {
  const t0 = Date.now();
  const c = toc.cats.find(x => x.id === cat);
  let n = 0, hits = [];
  for (const it of c.items) {
    const t = pageText(it.p + ".htm");
    n += t.length;
    if (t.indexOf(q) >= 0) hits.push(it.p);
    if (hits.length > 500) break;
  }
  console.log(cat, "text chars", n, "hits", hits.length, "ms", Date.now() - t0);
  return hits;
}

for (const cat of ["SA", "SN", "MA"]) {
  search(cat, "無常");
  search(cat, "涅槃");
}
