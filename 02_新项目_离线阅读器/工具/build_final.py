# -*- coding: utf-8 -*-
"""
生成最终数据包（v2 模型）：
  corpus/<系列>.json.gz   中文语料（每部一份）
  pali.json.gz            巴利段（内容相同才合并）
  pages.json.gz           页面索引：引用列表 + override + 比对 + 巴利引用
  books.json.gz           7 本著作
  docs.json.gz            读书站说明 / 凡例 / 主题索引
  toc.json.gz             目录树
  notes/map/t2s
"""
import os, io, sys, json, re, gzip, hashlib, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_model as M
import extract as E

BASE = M.BASE
OUT = os.path.join(BASE, "数据", "package")
os.makedirs(OUT, exist_ok=True)

def gz_write(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    raw = json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", compresslevel=9, mtime=0) as f:
        f.write(raw)
    data = buf.getvalue()
    io.open(path, "wb").write(data)
    return len(raw), len(data)

# ---------- 中文语料 ----------
series = collections.defaultdict(dict)
for k, h in M.canon.items():
    if k[0] == "PAGE":
        continue
    sid = ".".join(str(x) for x in k)
    series[k[0]][sid] = h

SERIES = "SN|AN|MN|DN|SA|MA|DA|AA|Ud|It|Ap|Ja|Su|Th|Vi|Ti|Cp|Mi|Ps|Bv|Dh|Pv|Kh|Ni"
REF = re.compile(r"(%s)\.(\d+(?:\.\d+)?(?:-\d+)?)" % SERIES)

def ref_of(line):
    s = line.strip().lstrip("\u3000 ").strip()
    if not s or len(s) > 200:
        return None
    m = REF.search(s[:80])
    if not m or m.start() > 30:
        return None
    return m.group(1) + "." + m.group(2)

def M_split_pali(t):
    lines = t.split("\n")
    idx = []
    for i, ln in enumerate(lines):
        r = ref_of(ln)
        if r:
            idx.append((i, r))
    if not idx:
        return [("_", t)]
    out = []
    if idx[0][0] > 0:
        pre = "\n".join(lines[:idx[0][0]]).strip()
        if pre:
            out.append(("_pre", pre))
    for j, (i, key) in enumerate(idx):
        end = idx[j + 1][0] if j + 1 < len(idx) else len(lines)
        out.append((key, "\n".join(lines[i:end])))
    return out
# ---------- 页面 ----------
def clean2(s):
    s = re.sub(r"\[(?:\u21dd)?[A-Za-z]{1,4}\.[\d.]+\]", "", s)
    out = []
    for ln in s.split("\n"):
        t = ln.strip()
        if not t:
            continue
        if re.match(r"^\d+[.\/].*(品|相應|篇|分)\]?$", t):
            continue
        out.append(re.sub(r"\s+", "", t))
    return "".join(out)

def body_only(h):
    parts = re.split(r"<br\s*/?>", h, flags=re.I)
    return "<br>".join(parts[1:]) if len(parts) > 1 else ""

# 巴利：内容完全相同的段合并
pali_table = {}
pali_id_by_hash = {}
pages = {}
pali_chars = 0
pali_seg_count = 0

def pali_id(txt):
    global pali_chars, pali_seg_count
    n = re.sub(r"\s+", "", txt)
    h = hashlib.sha1(n.encode()).hexdigest()[:12]
    if h not in pali_table:
        pali_table[h] = txt
        pali_chars += len(txt)
    pali_seg_count += 1
    return h

for pid, m in M.page_model.items():
    keys = [".".join(str(x) for x in k) for k in m["keys"]]
    ov = {}
    for k, sid in zip(m["keys"], keys):
        if k[0] == "PAGE":
            ov[sid] = M.canon.get(k, "")
            continue
        own = [h for p, h in M.texts.get(k, []) if p == pid]
        if own and clean2(body_only(own[0])) != clean2(body_only(M.canon[k])):
            ov[sid] = own[0]
    pali_ids = []
    # 巴利按段切
    if m["pali"]:
        t = E.strip_tags(m["pali"])
        for key, seg in M_split_pali(t):
            pali_ids.append(pali_id(seg))
    pres = {".".join(str(x) for x in k): v for k, v in m.get("pres", {}).items()}
    pages[pid] = [m["nm"], keys, ov, m["cmp"], pali_ids, m["cat"], m["num"], pres, m.get("sub", "")]


# ---------- 著作与参考页 ----------
books = {}
docs = {}
for r in M.recs:
    if r["cat"] == "book":
        books[r["p"][:-4]] = [r["nm"], r["blk"]]
    elif r["cat"] in ("study",) or r["p"].endswith("index.htm") or (r["cat"] not in M.SUTRA_CATS and r["num"] == 0):
        if any(b[2].strip() for b in r["blk"]):
            docs[r["p"][:-4]] = [r["nm"] or r["t"], r["blk"]]

# ---------- 写盘 ----------
report = []
tot_raw = tot_gz = 0
for code, obj in series.items():
    raw, gz = gz_write(os.path.join(OUT, "corpus", code + ".json.gz"), obj)
    tot_raw += raw; tot_gz += gz
    report.append(("corpus/" + code, len(obj), raw, gz))

for name, obj in (
    ("pali", pali_table),
    ("pages", pages),
    ("books", books),
    ("docs", docs),
):
    raw, gz = gz_write(os.path.join(OUT, name + ".json.gz"), obj)
    tot_raw += raw; tot_gz += gz
    report.append((name, len(obj), raw, gz))

print("%-18s %8s %10s %10s" % ("file", "count", "raw", "gz"))
for n, c, r, g in report:
    print("%-18s %8d %9.2fMB %9.2fMB" % (n, c, r / 1048576, g / 1048576))
print("-" * 52)
print("%-18s %8s %9.2fMB %9.2fMB" % ("TOTAL", "", tot_raw / 1048576, tot_gz / 1048576))
print("pali 段引用 %d 次，唯一段 %d 个，唯一巴利 %d 字" % (pali_seg_count, len(pali_table), pali_chars))
