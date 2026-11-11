const z = require("zlib"), fs = require("fs");
const D = __dirname + "/data/";
const t2s = JSON.parse(z.gunzipSync(fs.readFileSync(D + "t2s.json.gz")));
const toc = JSON.parse(z.gunzipSync(fs.readFileSync(D + "toc.json.gz")));
const PROT = "\uE000";
const phrases = t2s.p || [];
const chars = Object.assign({}, t2s.c || {});
delete chars["祇"];
function toSimp(s) {
  let out = String(s).split("明覆").join(PROT);
  for (let i = 0; i < phrases.length; i++) {
    const k = phrases[i][0];
    if (out.indexOf(k) >= 0) out = out.split(k).join(phrases[i][1]);
  }
  const arr = new Array(out.length);
  for (let j = 0; j < out.length; j++) arr[j] = chars[out[j]] || out[j];
  return arr.join("").split(PROT).join("明覆").replace(/庄春江/g, "莊春江");
}
for (const id of ["SA", "SN", "AA"]) {
  const p = toc.cats.find(c => c.id === id).page;
  const t0 = Date.now();
  const out = toSimp(p);
  console.log(id, "len", p.length, "->", out.length, "ms", Date.now() - t0);
}
const t0 = Date.now();
const h = toSimp(toc.home);
console.log("home", toc.home.length, "ms", Date.now() - t0);
console.log("sample:", h.slice(0, 80).replace(/\s+/g, " "));
