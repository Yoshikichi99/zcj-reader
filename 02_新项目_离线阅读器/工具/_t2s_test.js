const fs = require("fs");
const path = require("path");
const T2S = require("./t2s.js");

const dir = __dirname;
const data = JSON.parse(fs.readFileSync(path.join(dir, "_t2s.json"), "utf8"));
T2S.init(data);

const lines = fs.readFileSync(path.join(dir, "_pairs.jsonl"), "utf8").split("\n").filter(Boolean);
let same = 0;
const bad = [];
const t0 = Date.now();
let chars = 0;

for (const line of lines) {
  const p = JSON.parse(line);
  chars += p.t.length;
  const got = T2S.toSimp(p.t);
  if (got === p.s) {
    same++;
  } else {
    let i = 0;
    while (i < got.length && i < p.s.length && got[i] === p.s[i]) i++;
    bad.push({
      p: p.p, k: p.k, len: p.t.length,
      exp: p.s.slice(Math.max(0, i - 12), i + 18),
      got: got.slice(Math.max(0, i - 12), i + 18),
      pos: i
    });
  }
}
const ms = Date.now() - t0;

console.log("配对块:", lines.length, " 完全一致:", same, " 不一致:", bad.length);
console.log("总字数:", chars, " 耗时:", ms, "ms", " 平均:", (ms / lines.length).toFixed(2), "ms/块");
console.log("每秒处理字数:", Math.round(chars / (ms / 1000)));
console.log("\n不一致样例（前 15）:");
for (const b of bad.slice(0, 15)) {
  console.log(`  ${b.p} [${b.k}] 位置 ${b.pos}`);
  console.log(`     原简体: ...${b.exp}...`);
  console.log(`     实时转: ...${b.got}...`);
}

// 性能：最大块
let maxP = null;
for (const line of lines) {
  const p = JSON.parse(line);
  if (!maxP || p.t.length > maxP.t.length) maxP = p;
}
const t1 = Date.now();
for (let i = 0; i < 5; i++) T2S.toSimp(maxP.t);
console.log(`\n最大块 ${maxP.p} ${maxP.t.length} 字，单次约 ${((Date.now() - t1) / 5).toFixed(1)} ms`);
