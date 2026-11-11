# -*- coding: utf-8 -*-
"""分析巴利块：按经号引用切分，看去重空间（修正 KN/It 这类前缀）。"""
import os, io, sys, json, re, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract as E

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
recs = [json.loads(l) for l in io.open(os.path.join(BASE, "数据", "_pages.jsonl"), encoding="utf-8")]

SERIES = "SN|AN|MN|DN|SA|MA|DA|AA|Ud|It|Ap|Ja|Su|Th|Vi|Ti|Cp|Mi|Ps|Bv|Dh|Pv|Kh|Ni"
REF = re.compile(r"(%s)\.(\d+(?:\.\d+)?(?:-\d+)?)" % SERIES)

def ref_of(line):
    s = line.strip().lstrip("\u3000 ").strip()
    if not s or len(s) > 200:
        return None
    m = REF.search(s[:80])
    if not m:
        return None
    # 必须靠近行首（允许 KN/ 、括号说明等前缀）
    if m.start() > 30:
        return None
    return m.group(1) + "." + m.group(2)

def split_pali(h, pid=""):
    t = E.strip_tags(h)
    lines = t.split("\n")
    idx = []
    for i, ln in enumerate(lines):
        r = ref_of(ln)
        if r:
            idx.append((i, r))
    if not idx:
        return [("PAGE:" + pid, t)] if pid else [("_", t)]
    out = []
    if idx[0][0] > 0:
        pre = "\n".join(lines[:idx[0][0]]).strip()
        if pre:
            out.append(("PRE:" + pid, pre))
    for j, (i, key) in enumerate(idx):
        end = idx[j + 1][0] if j + 1 < len(idx) else len(lines)
        out.append((key, "\n".join(lines[i:end])))
    return out

segs = []
for r in recs:
    for k, s, h in r["blk"]:
        if k != "pali":
            continue
        for key, txt in split_pali(h, r["p"]):
            segs.append((r["p"], key, txt))

total = sum(len(x[2]) for x in segs)
bykey = collections.defaultdict(list)
for pid, key, txt in segs:
    bykey[key].append((pid, txt))

uniq = sum(max(len(t) for _, t in v) for v in bykey.values())
print("巴利块段:", len(segs), " 不同 key:", len(bykey))
print("总字数:", total, " 去重后:", uniq, " 可省 %.1f%%" % ((1 - uniq / total) * 100))
dups = [(k, len(v)) for k, v in bykey.items() if len(v) > 1 and not k.startswith(("PAGE:", "PRE:"))]
print("重复经号:", len(dups), " 样例:", dups[:8])
print("无经号(按页)段:", len([1 for x in segs if x[1].startswith("PAGE:")]))
print("前言段:", len([1 for x in segs if x[1].startswith("PRE:")]))
