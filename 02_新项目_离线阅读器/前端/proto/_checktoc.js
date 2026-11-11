const z = require("zlib"), fs = require("fs");
const t = JSON.parse(z.gunzipSync(fs.readFileSync(__dirname + "/data/toc.json.gz")));
const home = t.home || "";
console.log("home len", home.length, "imgs", (home.match(/<img/g) || []).length,
  "links", (home.match(/<a /g) || []).length);
console.log("home head:", home.slice(0, 160).replace(/\s+/g, " "));
for (const c of t.cats) {
  if (!["SA", "SN", "AA"].includes(c.id)) continue;
  const p = c.page || "";
  console.log(c.id, "page", p.length,
    "sutraLinks", (p.match(/#\/p\//g) || []).length,
    "catLinks", (p.match(/#\/c\//g) || []).length,
    "dead", (p.match(/href="[^"]*\.htm/g) || []).length,
    "tail:", p.slice(-80).replace(/\s+/g, " "));
}
