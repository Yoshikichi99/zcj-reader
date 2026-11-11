# -*- coding: utf-8 -*-
"""
SA / SN 语料库原型
1) 抽出 SA 栏全部北传正文、SN 栏全部南传正文（各只存一份，不含巴利）
2) 生成可阅读的 SA.html / SN.html
3) 逐页校验：北传页嵌入的南传段，能否由 SN 语料重组
4) 输出报告 report.md
"""
import os, io, sys, json, re, gzip, html, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract as E

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(BASE, "验证", "SA_SN原型")
os.makedirs(OUT, exist_ok=True)

recs = [json.loads(l) for l in io.open(os.path.join(BASE, "数据", "_pages.jsonl"), encoding="utf-8")]
by = {r["p"]: r for r in recs}

def nz(s):
    return re.sub(r"\s+", "", s)

def block_of(r, kind, src=None):
    out = []
    for k, s, h in r["blk"]:
        if k == kind and (src is None or s == src):
            out.append(h)
    return out

def text_of(r, kind, src=None):
    return "".join(E.strip_tags(h) for h in block_of(r, kind, src))

# ---------- 索引 ----------
IDX = {}
for r in recs:
    nm, pid = r["nm"], r["p"][:-4]
    m = re.match(r"相應部(\d+)相應(\d+)經", nm)
    if m: IDX[("SN", int(m.group(1)), int(m.group(2)))] = pid; continue
    m = re.match(r"增支部(\d+)集(\d+)經", nm)
    if m: IDX[("AN", int(m.group(1)), int(m.group(2)))] = pid; continue
    m = re.match(r"中部(\d+)經", nm)
    if m: IDX[("MN", 0, int(m.group(1)))] = pid; continue
    m = re.match(r"長部(\d+)經", nm)
    if m: IDX[("DN", 0, int(m.group(1)))] = pid; continue
    m = re.match(r"雜阿含(\d+)經", nm)
    if m: IDX[("SA", 0, int(m.group(1)))] = pid; continue
    m = re.match(r"中阿含(\d+)經", nm)
    if m: IDX[("MA", 0, int(m.group(1)))] = pid; continue
    m = re.match(r"長阿含(\d+)經", nm)
    if m: IDX[("DA", 0, int(m.group(1)))] = pid; continue
    m = re.match(r"增壹阿含(\d+)品(\d+)經", nm)
    if m: IDX[("AA", int(m.group(1)), int(m.group(2)))] = pid; continue

def expand_refs(s):
    """把「南傳:相應部30相應1,2經」这类描述展开成 (kind, group, num) 列表。"""
    refs = []
    for m in re.finditer(r"(相應部|增支部)(\d+)(相應|集)((?:\d+(?:-\d+)?)(?:[,\u3001]\s*\d+(?:-\d+)?)*)經", s):
        kind = "SN" if m.group(1) == "相應部" else "AN"
        for part in re.split(r"[,\u3001]", m.group(4)):
            part = part.strip()
            if not part:
                continue
            if "-" in part:
                a, b = part.split("-")
                for k in range(int(a), int(b) + 1):
                    refs.append((kind, int(m.group(2)), k))
            else:
                refs.append((kind, int(m.group(2)), int(part)))
    for m in re.finditer(r"(中部|長部)((?:\d+(?:-\d+)?)(?:[,\u3001]\s*\d+(?:-\d+)?)*)經", s):
        kind = "MN" if m.group(1) == "中部" else "DN"
        for part in re.split(r"[,\u3001]", m.group(2)):
            part = part.strip()
            if not part:
                continue
            if "-" in part:
                a, b = part.split("-")
                for k in range(int(a), int(b) + 1):
                    refs.append((kind, 0, k))
            else:
                refs.append((kind, 0, int(part)))
    for m in re.finditer(r"中阿含(\d+)經", s):
        refs.append(("MA", 0, int(m.group(1))))
    for m in re.finditer(r"長阿含(\d+)經", s):
        refs.append(("DA", 0, int(m.group(1))))
    return refs

def title_of(h):
    """取正文块第一行作为经名（去标注）。"""
    t = E.strip_tags(h)
    for ln in t.split("\n"):
        s = re.sub(r"\[[A-Z]{1,4}\.\d+(?:\.\d+)*\]", "", ln).strip()
        if s:
            return s
    return ""

def split_title_body(h):
    """拆成（经名, 空, 其余HTML）。只把经名那一行拿出来，其余原样保留（含品名行）。"""
    segs = re.split(r"<br\s*/?>", h, flags=re.I)
    ti = None
    for i, seg in enumerate(segs[:5]):
        t = re.sub(r"<[^>]+>", "", seg).strip()
        if not t:
            continue
        if "莊春江" in t or ("/" in t and "經" in t):
            ti = i
            break
    if ti is None:
        for i, seg in enumerate(segs):
            if re.sub(r"<[^>]+>", "", seg).strip():
                ti = i
                break
    if ti is None:
        return title_of(h), "", ""
    title = re.sub(r"\[[A-Z]{1,4}\.\d+(?:\.\d+)*\]", "", re.sub(r"<[^>]+>", "", segs[ti])).strip()
    heads = []
    j = ti - 1
    while j >= 0:
        prev = re.sub(r"<[^>]+>", "", segs[j]).strip()
        if not prev:
            j -= 1
            continue
        if re.match(r"^\d+[.\/]", prev) and re.search(r"(品|相應|篇|分)\]?$", prev):
            heads.insert(0, prev)
            j -= 1
            continue
        break
    pin = " ".join(heads)
    body = "<br>".join(segs[:j + 1] + segs[ti + 1:])
    return title, pin, body

# ---------- 语料 ----------
SA = []   # (id, title, body_html)
SN = []
for r in recs:
    if r["cat"] == "SA" and r["num"] > 0:
        hs = block_of(r, "zh", "agama") or block_of(r, "zh", "")
        if not hs:
            continue
        h = "".join(hs)
        t, pin, b = split_title_body(h)
        SA.append((r["p"][:-4], t, pin, b))
    elif r["cat"] == "SN" and r["num"] > 0:
        hs = block_of(r, "zh", "nikaya") or block_of(r, "zh", "")
        if not hs:
            continue
        h = "".join(hs)
        t, pin, b = split_title_body(h)
        SN.append((r["p"][:-4], t, pin, b))

SA.sort(key=lambda x: int(re.search(r"(\d+)", x[0].split("/")[1]).group(1)))
SN.sort(key=lambda x: int(re.search(r"(\d+)", x[0].split("/")[1]).group(1)))
print("SA 语料:", len(SA), "页   SN 语料:", len(SN), "页")

# ---------- HTML ----------
CSS = """
body{font-family:"Noto Serif CJK SC","Source Han Serif SC","Songti SC",SimSun,serif;
  max-width:820px;margin:0 auto;padding:24px 18px 80px;line-height:1.95;color:#26231f;background:#fbfaf7}
h1{font-size:24px;margin:0 0 4px} .meta{color:#7d756a;font-size:13px;margin-bottom:18px}
.toc{columns:3;column-gap:18px;font-size:13px;line-height:1.7;margin:16px 0 28px;padding:14px;border:1px solid #e7e2d9;border-radius:10px;background:#fff}
.toc a{color:#2f6b4f;text-decoration:none;display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
article{border-top:1px solid #e7e2d9;padding:18px 0 6px}
article:target{background:#fff8dd}
h2{font-size:17px;margin:0 0 10px;line-height:1.6;color:#8a5a2b}
.body{font-size:17px}
.body .sn{font-weight:700;color:#8a5a2b}
.body a.n,.body a.l{border-bottom:1px dotted #c9a06a;text-decoration:none;color:inherit}
.body .pnote{font-size:.86em;color:#7d756a;border-top:1px dashed #e7e2d9;padding-top:.5em}
.idtag{font-family:system-ui,sans-serif;font-size:11px;color:#a09a90;letter-spacing:.05em}
"""

def write_html(path, title, items, note):
    parts = []
    parts.append("<!doctype html><html lang='zh-Hant'><head><meta charset='utf-8'>")
    parts.append("<title>%s</title><style>%s</style></head><body>" % (html.escape(title), CSS))
    parts.append("<h1>%s</h1>" % html.escape(title))
    parts.append("<div class='meta'>%s</div>" % note)
    parts.append("<div class='toc'>")
    for pid, t, pin, b in items:
        label = (pin + " · " if pin else "") + t
        parts.append("<a href='#%s'>%s</a>" % (pid.replace("/", "_"), html.escape(label[:30])))
    parts.append("</div>")
    for pid, t, pin, b in items:
        parts.append("<article id='%s'>" % pid.replace("/", "_"))
        parts.append("<div class='idtag'>%s</div>" % html.escape(pid))
        head = ("<span class='pin'>%s</span> · " % html.escape(pin)) if pin else ""
        parts.append("<h2>%s%s</h2>" % (head, html.escape(t)))
        parts.append("<div class='body'>%s</div>" % b)
        parts.append("</article>")
    parts.append("</body></html>")
    io.open(path, "w", encoding="utf-8").write("\n".join(parts))

write_html(os.path.join(OUT, "SA_杂阿含全经.html"), "雜阿含經 · 全經（每經一份，不含巴利）", SA,
           "共 %d 經。取自 SA 页面北传正文，标题用独立页完整品名。" % len(SA))
write_html(os.path.join(OUT, "SN_相应部全经.html"), "相應部 · 全經（每經一份，不含巴利）", SN,
           "共 %d 經。取自 SN 页面南传正文，不含巴利原文。" % len(SN))

# ---------- 校验：北传页嵌入的南传段能否重组 ----------
def clean_compare(s):
    s = re.sub(r"\[[A-Z]{1,4}\.\d+(?:\.\d+)*\]", "", s)
    out = []
    for ln in s.split("\n"):
        t = ln.strip()
        if not t:
            continue
        if re.match(r"^\d+\.\S+品$", t):
            continue
        out.append(re.sub(r"\s+", "", t))
    return "".join(out)

# 供比对用的正文（不含标题行）
SN_BODY = {}
for pid, t, pin, b in SN:
    SN_BODY[pid] = E.strip_tags(b)
SA_REF = {}
for pid, t, pin, b in SA:
    SA_REF[pid] = E.strip_tags(b)

tested = 0
allhit = 0
partial = 0
missing = []
for pid, t, pin, b in SA:
    r = by[pid + ".htm"]
    sfield = r["s"]
    if not sfield or "無" == sfield.strip("南傳:："):
        continue
    refs = expand_refs(sfield)
    ids = [IDX.get(x) for x in refs]
    ids = [i for i in ids if i]
    if not refs:
        continue
    emb = clean_compare(E.strip_tags("".join(block_of(r, "zh", "nikaya"))))
    if not emb:
        continue
    tested += 1
    tot = hit = 0
    for i in ids:
        body = clean_compare(SN_BODY.get(i, ""))
        if not body:
            continue
        # 按行比对
        for ln in E.strip_tags(SN_BODY.get(i, "")).split("\n"):
            ln = re.sub(r"\[[A-Z]{1,4}\.\d+(?:\.\d+)*\]", "", ln).strip()
            if len(ln) < 10 or re.match(r"^\d+\.\S+品$", ln):
                continue
            k = re.sub(r"\s+", "", ln)
            tot += len(k)
            if k in emb:
                hit += len(k)
    if tot == 0:
        continue
    cov = hit / tot
    if cov >= 0.995:
        allhit += 1
    elif cov >= 0.9:
        partial += 1
    else:
        missing.append((pid, round(cov, 2), tot))

print("SA 页含南传引用并可比对:", tested)
print("  完全可重组:", allhit)
print("  90%% 以上:", partial)
print("  低于 90%%:", len(missing))

# ---------- 体积 ----------
def gzs(s):
    return len(gzip.compress(s.encode("utf-8"), 9, mtime=0))

sa_text = "".join(E.strip_tags(b) for _, t, pin, b in SA)
sn_text = "".join(E.strip_tags(b) for _, t, pin, b in SN)
print("SA 正文 %.2f MB   SN 正文 %.2f MB" % (len(sa_text.encode())/1048576, len(sn_text.encode())/1048576))

rep = []
rep.append("# SA / SN 语料库原型报告\n")
rep.append("- **SA 语料**：%d 经，正文 %.2f MB（UTF-8），gzip %.2f MB" %
           (len(SA), len(sa_text.encode())/1048576, gzs(sa_text)/1048576))
rep.append("- **SN 语料**：%d 经，正文 %.2f MB（UTF-8），gzip %.2f MB" % (len(SN), len(sn_text.encode())/1048576, gzs(sn_text)/1048576))
rep.append("- **两栏合计 gzip**：%.2f MB" % ((gzs(sa_text)+gzs(sn_text))/1048576))
rep.append("")
rep.append("## 重组校验（SA 页里的南传段）")
rep.append("- 可解析引用的 SA 页：%d" % tested)
rep.append("- 南传段 100%% 可由 SN 语料重组：%d" % allhit)
rep.append("- 覆盖 90%% 以上：%d" % partial)
rep.append("- 覆盖低于 90%%：%d（多半是节略引用）" % len(missing))
if missing:
    rep.append("\n低于 90% 的页面：\n")
    for m in missing[:40]:
        rep.append("- %s 覆盖率 %.0f%%（SN 原文 %d 字）" % (m[0], m[1]*100, m[2]))
rep.append("")
rep.append("## 说明")
rep.append("- 语料库每经只存一份；SA 页的南传段、SN 页的北传段都由引用重组。")
rep.append("- 巴利原文不在本原型内（按要求 SN 不含巴利）。")
rep.append("- 律藏引用（5 页）与无法解析的引用保留原块。")
io.open(os.path.join(OUT, "报告.md"), "w", encoding="utf-8").write("\n".join(rep))
print("报告写入", os.path.join(OUT, "报告.md"))
