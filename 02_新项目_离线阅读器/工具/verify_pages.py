# -*- coding: utf-8 -*-
"""校验：抽取出来的每个正文块，必须能在源页面的可见文本里原样找到（去空白、反转义后）。"""
import os, re, io, sys, json, random, collections, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract as E

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
recs = [json.loads(l) for l in io.open(os.path.join(BASE, "数据", "_pages.jsonl"), encoding="utf-8")]

def norm(s):
    return E.norm_ws(H.unescape(s))

random.seed(11)
sample = random.sample(recs, min(500, len(recs)))
bad = []
stats = collections.Counter()
for r in sample:
    rel = r["p"]
    raw = io.open(os.path.join(E.ROOT, rel), encoding="utf-8", errors="replace").read()
    src = E.STYLE_RE.sub("", E.SCRIPT_RE.sub("", raw))
    src_norm = norm(re.sub(r"<[^>]+>", " ", src))
    stats[E.classify(rel)] += 1
    for kind, s, h in r["blk"]:
        t = norm(E.strip_tags(h))
        if not t:
            continue
        if t not in src_norm:
            bad.append((rel, kind, len(t), t[:60]))

print("sampled:", len(sample), dict(stats))
print("missing blocks:", len(bad), "in", len(set(b[0] for b in bad)), "pages")
for b in bad[:20]:
    print("  ", b[0], b[1], b[2], b[3])
