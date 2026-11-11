# -*- coding: utf-8 -*-
"""
按「经文身份」切分语料：
一个内容块里可能并排多部经（SA.73 里就有 增壹阿含25品4），必须按 <span class="sn"> 切开，
各自归入自己的系统（SA / SN / ZA / AA / MA / DA / MN / DN / AN / 其他）。

产出：
  SA_杂阿含全经.html   只含 SA.* （1359 部）
  SN_相应部全经.html   只含 SN.*，无巴利
  其他文本.html        ZA / AA / MA / DA / MN / DN / AN / 其他
  报告.md
"""
import os, io, sys, json, re, gzip, html, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract as E

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(BASE, "验证", "语料库v2")
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
        return ("SA", int(m.group(1)), int(m.group(2))), t
    m = re.match(r"^相應(\d+)相應\s*(\d+)", t)
    if m:
        return ("SN", int(m.group(1)), int(m.group(2))), t
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
            nums = tuple(int(x) for x in m.groups() if x is not None)
            return prefix + nums, t
    return None, t

def segments(h):
    """返回 [(title_or_None, html)]，按 <span class="sn"> 切。"""
    ms = list(SN_RE.finditer(h))
    if not ms:
        return [(None, h)]
    out = []
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(h)
        out.append((m.group(1), h[m.start():end]))
    return out

SERIES_NAME = {
    "SA": "雜阿含", "ZA": "別譯雜阿含", "SN": "相應部", "AN": "增支部",
    "MA": "中阿含", "DA": "長阿含", "MN": "中部", "DN": "長部",
    "AA": "增壹阿含", "OTHER": "其他（律藏/單經/小部）",
}

texts = collections.defaultdict(list)   # key -> [(page, title, html)]
page_refs = collections.defaultdict(list)

for r in recs:
    cat = r["cat"]
    if cat not in SUTRA_CATS:
        continue
    for kind, src, h in r["blk"]:
        if kind != "zh":
            continue
        segs = segments(h)
        got = []
        if len(segs) == 1 and segs[0][0] is None:
            # 旧版：从 <u> 取经名
            mu = U_RE.search(h[:300])
            if mu:
                key, name = key_of(mu.group(1))
                if key:
                    texts[key].append((r["p"], name, h))
                    got.append(key)
            continue
        for title, seg in segs:
            if title is None:
                continue
            key, name = key_of(title)
            if key is None:
                key = ("OTHER", name[:40])
            texts[key].append((r["p"], name, seg))
            got.append(key)
        if got:
            page_refs[r["p"]] = got

print("不同文本:", len(texts))
per = collections.Counter(k[0] for k in texts)
print("按系统:", dict(per))

# 选权威副本：优先取「页面自身经名就是该文本」的那份，否则取最长
def pick(key, copies):
    for pid, name, h in copies:
        if pid.endswith(name[:2]):
            pass
    best = max(copies, key=lambda x: len(re.sub(r"<[^>]+>", "", x[2])))
    for pid, name, h in copies:
        base = os.path.basename(pid).replace(".htm", "")
        if base.upper().startswith("".join(str(x) for x in key[1:])):
            return h
    return best[2]

canon = {}
for k, v in texts.items():
    canon[k] = pick(k, v)

def sort_key(k):
    if k[0] == "SA":
        return (0, k[1])
    if k[0] == "SN":
        return (0, k[1], k[2] if len(k) > 2 else 0)
    return (1, str(k))

def title_from(key, h):
    m = SN_RE.search(h)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    mu = U_RE.search(h[:300])
    return re.sub(r"<[^>]+>", "", mu.group(1)).strip() if mu else ""

def strip_title(h):
    """把开头的标题 span 去掉，返回正文。"""
    m = SN_RE.search(h)
    if m:
        rest = h[m.end():]
        # 去掉标题后的 (品/篇)(译者)[标注]
        rest = re.sub(r"^(?:\s*\([^)]*\))*\s*(?:\[[^\]]*\])?\s*(?:<br\s*/?>)?", "", rest, count=1)
        return rest
    mu = U_RE.search(h[:300])
    if mu:
        rest = h[mu.end():]
        rest = re.sub(r"^(?:\s*\([^)]*\))*\s*(?:<br\s*/?>)?", "", rest, count=1)
        return rest
    return h

CSS = """
body{font-family:"Noto Serif CJK SC","Songti SC",SimSun,serif;max-width:820px;margin:0 auto;
 padding:24px 18px 80px;line-height:1.95;color:#26231f;background:#fbfaf7}
h1{font-size:24px;margin:0 0 4px}.meta{color:#7d756a;font-size:13px;margin-bottom:18px;line-height:1.7}
.toc{columns:3;column-gap:18px;font-size:13px;line-height:1.7;margin:16px 0 28px;padding:14px;
 border:1px solid #e7e2d9;border-radius:10px;background:#fff}
.toc a{color:#2f6b4f;text-decoration:none;display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
article{border-top:1px solid #e7e2d9;padding:18px 0 6px}article:target{background:#fff8dd}
h2{font-size:17px;margin:0 0 6px;line-height:1.6;color:#8a5a2b}
.tag{font-family:system-ui,sans-serif;font-size:11px;color:#a09a90;letter-spacing:.05em;margin-bottom:4px}
.body{font-size:17px}
.body a.n,.body a.l{border-bottom:1px dotted #c9a06a;text-decoration:none;color:inherit}
.body sup{font-size:.7em}
"""

def write(path, title, keys, note):
    parts = ["<!doctype html><html lang='zh-Hant'><head><meta charset='utf-8'>",
             "<title>%s</title><style>%s</style></head><body>" % (html.escape(title), CSS),
             "<h1>%s</h1>" % html.escape(title), "<div class='meta'>%s</div>" % note]
    parts.append("<div class='toc'>")
    for k in keys:
        t = title_from(k, canon[k])
        parts.append("<a href='#%s'>%s</a>" % (str(k).replace(" ", "_").replace("'", "").replace("(", "").replace(")", "").replace(",", "_"),
                                               html.escape(t[:30])))
    parts.append("</div>")
    for k in keys:
        h = canon[k]
        t = title_from(k, h)
        body = strip_title(h)
        aid = str(k).replace(" ", "_").replace("'", "").replace("(", "").replace(")", "").replace(",", "_")
        parts.append("<article id='%s'>" % aid)
        tag = ".".join(str(x) for x in k)
        parts.append("<div class='tag'>%s</div>" % html.escape(tag))
        parts.append("<h2>%s</h2>" % html.escape(t))
        parts.append("<div class='body'>%s</div>" % body)
        parts.append("</article>")
    parts.append("</body></html>")
    io.open(path, "w", encoding="utf-8").write("\n".join(parts))

sa_keys = sorted([k for k in canon if k[0] == "SA"], key=lambda k: k[1])
sn_keys = sorted([k for k in canon if k[0] == "SN"], key=lambda k: (k[1], k[2]))
other_keys = sorted([k for k in canon if k[0] not in ("SA", "SN")], key=sort_key)

write(os.path.join(OUT, "SA_杂阿含全经.html"), "雜阿含經 · 全經（只含 SA 文本）", sa_keys,
      "共 %d 部。每部一份；页面里并排的別譯雜阿含、增壹阿含等已归入其它文件。" % len(sa_keys))
write(os.path.join(OUT, "SN_相应部全经.html"), "相應部 · 全經（只含 SN 文本，不含巴利）", sn_keys,
      "共 %d 部。每部一份，不含巴利原文。" % len(sn_keys))
series_files = [
    ("ZA", "別譯雜阿含全经.html", "別譯雜阿含 · 全經"),
    ("AN", "增支部全经.html", "增支部 · 全經"),
    ("AA", "增壹阿含全经.html", "增壹阿含 · 全經"),
    ("MA", "中阿含全经.html", "中阿含 · 全經"),
    ("DA", "长阿含全经.html", "長阿含 · 全經"),
    ("MN", "中部全经.html", "中部 · 全經"),
    ("DN", "长部全经.html", "長部 · 全經"),
    ("OTHER", "其他文本.html", "其他文本（律藏 / 單經 / 小部等）"),
]
written = []
for code, fn, label in series_files:
    ks = sorted([k for k in canon if k[0] == code], key=sort_key)
    if not ks:
        continue
    write(os.path.join(OUT, fn), label, ks, "共 %d 部，每部一份。" % len(ks))
    written.append((code, label, ks))

# ---- 体积 ----
def gzs(keys):
    s = "".join(E.strip_tags(canon[k]) for k in keys)
    return len(s.encode()), len(gzip.compress(s.encode(), 9, mtime=0))

all_rows = [("SA 雜阿含", sa_keys), ("SN 相應部", sn_keys)]
for code, label, ks in written:
    all_rows.append((label, ks))
for name, keys in all_rows:
    a, b = gzs(keys)
    print("%s: %d 部, 正文 %.2f MB, gzip %.2f MB" % (name, len(keys), a / 1048576, b / 1048576))

tot_a = sum(gzs(k)[0] for _, k in all_rows)
tot_b = sum(gzs(k)[1] for _, k in all_rows)
rep = ["# 语料库 v2 报告\n"]
rep.append("按经文身份切分，每部只存一份。一个页面里的「并排文本」已拆开，各归各的系统。\n")
rep.append("| 系统 | 部数 | 正文 | gzip |")
rep.append("|---|---|---|---|")
for name, keys in all_rows:
    a, b = gzs(keys)
    rep.append("| %s | %d | %.2f MB | %.2f MB |" % (name, len(keys), a / 1048576, b / 1048576))
rep.append("| **合计** | **%d** | **%.2f MB** | **%.2f MB** |" % (sum(len(k) for _, k in all_rows), tot_a / 1048576, tot_b / 1048576))
dups = [(k, len(v)) for k, v in texts.items() if len(v) > 1]
rep.append("\n- 文本总数（含重复副本）：%d" % sum(len(v) for v in texts.values()))
rep.append("- 不同文本：%d" % len(texts))
rep.append("- 出现多次的文本：%d" % len(dups))
rep.append("- 多经并排的内容块：%d" % sum(1 for r in recs for k, s, h in r["blk"] if k == "zh" and len(segments(h)) > 1))
rep.append("\n## 说明")
rep.append("- 之前把整块当一部，导致 SA 文件里混进增壹阿含、別譯雜阿含等内容；v2 已按标题切开。")
rep.append("- 巴利原文、南北传比对（cmp）尚未纳入。")
io.open(os.path.join(OUT, "报告.md"), "w", encoding="utf-8").write("\n".join(rep))
print("done")
