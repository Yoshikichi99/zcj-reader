# -*- coding: utf-8 -*-
"""统计：一个内容块里到底装了几部经、分别属于哪个系统、重复多少。"""
import os, io, sys, json, re, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract as E

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
recs = [json.loads(l) for l in io.open(os.path.join(BASE, "数据", "_pages.jsonl"), encoding="utf-8")]

SN_RE = re.compile(r"<span class=\"sn\">(.*?)</span>", re.S)

def key_of(title):
    t = re.sub(r"<[^>]+>", "", title)
    t = re.sub(r"\[[^\]]*\]", "", t).strip()
    for pat, fmt in (
        (r"^雜阿含(\d+)經", lambda m: ("SA", int(m.group(1)))),
        (r"^別譯雜阿含(\d+)經", lambda m: ("ZA", int(m.group(1)))),
        (r"^增壹阿含(\d+)品(\d+)經", lambda m: ("AA", int(m.group(1)), int(m.group(2)))),
        (r"^中阿含(\d+)經", lambda m: ("MA", int(m.group(1)))),
        (r"^長阿含(\d+)經", lambda m: ("DA", int(m.group(1)))),
        (r"^相應部(\d+)相應(\d+)經", lambda m: ("SN", int(m.group(1)), int(m.group(2)))),
        (r"^增支部(\d+)集(\d+)經", lambda m: ("AN", int(m.group(1)), int(m.group(2)))),
        (r"^中部(\d+)經", lambda m: ("MN", int(m.group(1)))),
        (r"^長部(\d+)經", lambda m: ("DN", int(m.group(1)))),
        (r"^增支部(\d+)集", lambda m: ("AN", int(m.group(1)), 0)),
    ):
        m = re.match(pat, t)
        if m:
            return fmt(m), t
    return ("OTHER", t[:40]), t

def segments(h):
    """按 <span class="sn"> 把块切成若干部经。"""
    ms = list(SN_RE.finditer(h))
    if not ms:
        return [(None, h)]
    out = []
    if ms[0].start() > 0:
        pre = h[:ms[0].start()]
        if re.sub(r"<[^>]+>", "", pre).strip():
            out.append((None, pre))
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(h)
        out.append((m.group(1), h[m.start():end]))
    return out

keys = {}
series = collections.Counter()
blocks_multi = 0
texts_total = 0
for r in recs:
    for kind, src, h in r["blk"]:
        if kind not in ("zh", "doc"):
            continue
        segs = segments(h)
        if len(segs) > 1:
            blocks_multi += 1
        for title, seg in segs:
            if title is None:
                t = r["nm"] or r["t"]
            else:
                t = title
            (k, name) = key_of(t) if title is not None else (("PAGE", r["p"][:-4]), t)
            series[k[0]] += 1
            keys.setdefault(k, []).append((r["p"], len(re.sub(r"<[^>]+>", "", seg))))
            texts_total += 1

print("内容块总数:", sum(len(v) for v in keys.values()))
print("多经块:", blocks_multi)
print("不同 key 数:", len(keys))
print("按系统:", dict(series.most_common(20)))
dups = [(k, len(v)) for k, v in keys.items() if len(v) > 1]
print("重复 key 数:", len(dups))
print("重复样例:", dups[:10])
