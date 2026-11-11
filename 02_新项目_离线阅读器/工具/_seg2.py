# -*- coding: utf-8 -*-
"""细化统计：按经文身份切分，估算「每部只存一份」的真实收益。"""
import os, io, sys, json, re, collections, gzip
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract as E

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
recs = [json.loads(l) for l in io.open(os.path.join(BASE, "数据", "_pages.jsonl"), encoding="utf-8")]
SN_RE = re.compile(r"<span class=\"sn\">(.*?)</span>", re.S)
U_RE = re.compile(r"<u>(.*?)</u>", re.S)

def key_of(title):
    t = re.sub(r"<[^>]+>", "", title)
    t = re.sub(r"\[[^\]]*\]", "", t).strip()
    pats = [
        (r"^雜阿含(\d+)經", ("SA",)),
        (r"^別譯雜阿含(\d+)經", ("ZA",)),
        (r"^增壹阿含(\d+)品(\d+)經", ("AA",)),
        (r"^中阿含(\d+)經", ("MA",)),
        (r"^長阿含(\d+)經", ("DA",)),
        (r"^相應部(\d+)相應(\d+)經", ("SN",)),
        (r"^增支部(\d+)集(\d+)經", ("AN",)),
        (r"^中部(\d+)經", ("MN",)),
        (r"^長部(\d+)經", ("DN",)),
    ]
    for pat, prefix in pats:
        m = re.match(pat, t)
        if m:
            return prefix + tuple(int(x) for x in m.groups()), t
    return ("OTHER", t[:30]), t

def segments(h):
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

texts = {}   # key -> list of (page, html)
series = collections.Counter()
multi = 0
for r in recs:
    for kind, src, h in r["blk"]:
        if kind not in ("zh", "doc"):
            continue
        segs = segments(h)
        if len(segs) > 1:
            multi += 1
        for title, seg in segs:
            if title is None:
                mu = U_RE.search(seg[:300])
                if mu:
                    key, name = key_of(mu.group(1))
                else:
                    key, name = ("PAGE", r["p"][:-4]), (r["nm"] or r["t"])
            else:
                key, name = key_of(title)
            texts.setdefault(key, []).append((r["p"], seg))
            series[key[0]] += 1

total_chars = sum(len(re.sub(r"<[^>]+>", "", h)) for v in texts.values() for _, h in v)
uniq_chars = sum(max(len(re.sub(r"<[^>]+>", "", h)) for _, h in v) for v in texts.values())
dup_keys = [k for k, v in texts.items() if len(v) > 1]
print("段总数 %d，不同文本 %d，多经块 %d" % (sum(len(v) for v in texts.values()), len(texts), multi))
print("按系统:", dict(series.most_common(15)))
print("总字数 %d，去重后 %d，可省 %.1f%%" % (total_chars, uniq_chars, (1 - uniq_chars / total_chars) * 100))
print("重复文本 %d 个" % len(dup_keys))
top = sorted(texts.items(), key=lambda kv: -len(kv[1]))[:10]
for k, v in top:
    print("   %s 出现 %d 次" % (k, len(v)))
# 估算 gzip
uniq_html = "".join(max(v, key=lambda x: len(x[1]))[1] for v in texts.values())
print("去重后 HTML %.2f MB，gzip %.2f MB" % (len(uniq_html.encode())/1048576, len(gzip.compress(uniq_html.encode(), 9, mtime=0))/1048576))
# OTHER 样例
others = [k for k in texts if k[0] == "OTHER"][:15]
print("OTHER 样例:", [k[1] for k in others])
