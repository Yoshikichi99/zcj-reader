# -*- coding: utf-8 -*-
"""
页面视图模型：页面只存「按顺序引用的文本 key」，正文从语料库取。
并逐页验证：用引用拼出来的正文，与原页面的正文是否一致。

产出：
  数据/model_sample.jsonl   页面模型（id -> 引用列表 + 比对 + 巴利）
  验证/页面视图报告.md
"""
import os, io, sys, json, re, gzip, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract as E

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(BASE, "验证", "页面视图")
os.makedirs(OUT, exist_ok=True)

recs = [json.loads(l) for l in io.open(os.path.join(BASE, "数据", "_pages.jsonl"), encoding="utf-8")]
SN_RE = re.compile(r"<span class=\"sn\">(.*?)</span>", re.S)
U_RE = re.compile(r"<u>(.*?)</u>", re.S)
SUTRA_CATS = {"SA", "SN", "AN", "MA", "MN", "DA", "DN", "AA", "Ud", "It", "Ap", "Ja",
              "Su", "Th", "Vi", "Ti", "Cp", "Mi", "Ps", "Bv", "Dh", "Pv", "Kh", "Ni"}

def key_of(title):
    t = re.sub(r"<[^>]+>", "", title or "")
    t = re.sub(r"\[[^\]]*\]", "", t).strip()
    m = re.match(r"^雜阿含\s*(\d+)[、,]\s*(\d+)", t)
    if m:
        return ("SA", int(m.group(1)), int(m.group(2)))
    m = re.match(r"^相應(\d+)相應\s*(\d+)", t)
    if m:
        return ("SN", int(m.group(1)), int(m.group(2)))
    pats = [
        (r"^雜阿含\s*(\d+)(?:-(\d+))?經", ("SA",)),
        (r"^別譯雜阿含\s*(\d+)(?:-(\d+))?經", ("ZA",)),
        (r"^增壹阿含(\d+)品(\d+)(?:-(\d+))?經", ("AA",)),
        (r"^中阿含\s*(\d+)(?:-(\d+))?經", ("MA",)),
        (r"^長阿含\s*(\d+)(?:-(\d+))?經", ("DA",)),
        (r"^相應部(\d+)相應\s*(\d+)(?:-(\d+))?經", ("SN",)),
        (r"^增支部(\d+)集\s*(\d+)(?:-(\d+))?經", ("AN",)),
        (r"^中部\s*(\d+)(?:-(\d+))?經", ("MN",)),
        (r"^長部\s*(\d+)(?:-(\d+))?經", ("DN",)),
    ]
    for pat, prefix in pats:
        m = re.match(pat, t)
        if m:
            return prefix + tuple(int(x) for x in m.groups() if x is not None)
    return None

def segments(h):
    ms = list(SN_RE.finditer(h))
    if not ms:
        return [(None, h)]
    out = []
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(h)
        out.append((m.group(1), h[m.start():end]))
    return out

def seg_key(title, whole):
    if title is not None:
        k = key_of(title)
        return k
    mu = U_RE.search(whole[:300])
    if mu:
        return key_of(mu.group(1))
    return None

# ---------- 语料 + 权威副本 ----------
texts = collections.defaultdict(list)   # key -> [(page, html)]
page_model = {}

for r in recs:
    cat = r["cat"]
    if cat not in SUTRA_CATS or r["num"] == 0:
        continue
    own = key_of(r["nm"])
    keys = []
    pres = {}
    cmp_html = ""
    pali_html = ""
    for kind, src, h in r["blk"]:
        if kind == "pali":
            pali_html = h
            continue
        if kind == "cmp":
            cmp_html += h
            continue
        if kind != "zh":
            continue
        segs = segments(h)
        # 旧版单块
        if len(segs) == 1 and segs[0][0] is None:
            k = seg_key(None, h)
            if k:
                texts[k].append((r["p"], h))
                keys.append(k)
            continue
        block_keys = []
        for title, seg in segs:
            if title is None:
                continue
            k = key_of(title)
            if k is None:
                k = ("OTHER", re.sub(r"<[^>]+>", "", title)[:40])
            texts[k].append((r["p"], seg))
            keys.append(k)
            block_keys.append(k)
        # 记录块开头（标题之前）的品名/礼敬文字
        if block_keys:
            m0 = SN_RE.search(h)
            if m0:
                pre = h[:m0.start()]
                if E.strip_tags(pre).strip():
                    pres[block_keys[0]] = pre
    if not keys:
        zh = "".join(h for k, s, h in r["blk"] if k == "zh")
        if zh.strip():
            k = ("PAGE", r["p"])
            texts[k].append((r["p"], zh))
            keys = [k]
    if keys:
        page_model[r["p"]] = {
            "cat": cat, "num": r["num"], "nm": r["nm"],
            "keys": keys, "cmp": cmp_html, "pali": pali_html,
            "n": r["n"], "s": r["s"], "tp": r["tp"], "sub": r["sub"], "pres": pres,
        }

# 权威副本：优先取「本页就是这部经」的那一份，否则取最长
owner = {}
for r in recs:
    if r["cat"] in SUTRA_CATS and r["num"] > 0:
        k = key_of(r["nm"])
        if k:
            owner[k] = r["p"]
canon = {}
for k, copies in texts.items():
    op = owner.get(k)
    chosen = None
    if op:
        for pid, h in copies:
            if pid == op:
                chosen = h
                break
    if chosen is None:
        chosen = max(copies, key=lambda x: len(E.strip_tags(x[1])))[1]
    canon[k] = chosen

# ---------- 验证 ----------
def clean(s):
    s = re.sub(r"\[[A-Z]{1,4}\.\d+(?:\.\d+)*\]", "", s)
    out = []
    for ln in s.split("\n"):
        t = ln.strip()
        if not t:
            continue
        if re.match(r"^\d+[.\/].*(品|相應|篇|分)\]?$", t):
            continue
        out.append(re.sub(r"\s+", "", t))
    return "".join(out)

stats = collections.Counter()
diffs = []
for pid, m in page_model.items():
    r = next((x for x in recs if x["p"] == pid), None)
    if r is None:
        continue
    orig = clean("".join(E.strip_tags(h) for k, s, h in r["blk"] if k == "zh"))
    comp = clean("".join(E.strip_tags(canon[k]) for k in m["keys"] if k in canon))
    if orig == comp:
        stats["exact"] += 1
    elif orig and len(comp) >= len(orig) * 0.95:
        stats["close"] += 1
        diffs.append((pid, "close", len(orig), len(comp)))
    else:
        stats["diff"] += 1
        diffs.append((pid, "diff", len(orig), len(comp)))

print("页面模型:", len(page_model))
print("拼装结果:", dict(stats))
for d in diffs[:15]:
    print("   ", d)

# ---------- 写模型样例（只写 SA/SN 两栏，便于检查） ----------
sample_path = os.path.join(BASE, "数据", "model_sample.jsonl")
with io.open(sample_path, "w", encoding="utf-8") as f:
    for pid, m in page_model.items():
        if m["cat"] not in ("SA", "SN"):
            continue
        f.write(json.dumps({
            "id": pid, "nm": m["nm"], "keys": [".".join(str(x) for x in k) for k in m["keys"]],
            "cmp": m["cmp"], "pali_len": len(m["pali"]),
        }, ensure_ascii=False) + "\n")
print("样例写入", sample_path)

# ---------- 报告 ----------
rep = ["# 页面视图模型报告\n"]
rep.append("页面只存「按顺序引用的文本」，正文从语料库取。\n")
rep.append("- 页面总数：%d" % len(page_model))
rep.append("- 拼装后与原页面逐字一致：%d" % stats["exact"])
rep.append("- 覆盖率 ≥95%%（差异多为品名/标注）：%d" % stats["close"])
rep.append("- 明显不一致（原页节略或引用不全）：%d" % stats["diff"])
rep.append("\n## 不一致样例\n")
for d in diffs[:30]:
    rep.append("- `%s` 原 %d 字 / 拼装 %d 字（%s）" % (d[0], d[2], d[3], d[1]))
io.open(os.path.join(OUT, "页面视图报告.md"), "w", encoding="utf-8").write("\n".join(rep))
print("报告写入", os.path.join(OUT, "页面视图报告.md"))
