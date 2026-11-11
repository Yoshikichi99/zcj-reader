# -*- coding: utf-8 -*-
"""
P1 打包：_pages.jsonl -> 前端/data/*.json.gz + 前端/assets/**

产出:
  data/toc.json.gz         目录树（栏目/分组/书/参考页）
  data/pages/<CAT>.json.gz 各栏目正文（id -> 记录）
  data/pages/book.json.gz  著作正文
  data/pages/doc.json.gz   参考页（读书站说明、主题索引、栏目凡例）
  data/notes.json.gz       999 条全局注释（繁体）
  data/map.json.gz         SN/AN 经号比对映射
  assets/<站点相对路径>      正文引用的图片
"""
import os, re, io, sys, json, gzip, shutil, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract as E

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(BASE, "源数据", "agama.buddhason.org_simp")
OUT = os.path.join(BASE, "前端")
DATA = os.path.join(OUT, "data")
ASSETS = os.path.join(OUT, "assets")

CAT_NAMES = {
    "SA": "雜阿含經", "SN": "相應部", "MA": "中阿含經", "MN": "中部",
    "DA": "長阿含經", "DN": "長部", "AA": "增壹阿含經", "AN": "增支部",
    "Kh": "小誦", "Dh": "法句", "Ud": "優陀那", "It": "如是語",
    "Su": "經集", "Vi": "天宮事", "Pv": "餓鬼事", "Th": "長老偈",
    "Ti": "長老尼偈", "Ja": "本生", "Ap": "譬喻", "Bv": "佛種姓",
    "Cp": "所行藏", "Ni": "大義釋", "Mi": "彌蘭王問", "Ps": "無解道",
}
CAT_ORDER = ["SA", "SN", "MA", "MN", "DA", "DN", "AA", "AN",
             "Kh", "Dh", "Ud", "It", "Su", "Vi", "Pv", "Th",
             "Ti", "Ja", "Ap", "Bv", "Cp", "Ni", "Mi", "Ps"]
CAT_SHORT = {"SA": "雜", "SN": "相應", "MA": "中", "MN": "中部", "DA": "長", "DN": "長部",
             "AA": "增壹", "AN": "增支"}

BOOKS = [
    ("book/ann", "阿含經南北對讀摘記", "anni.htm"),
    ("book/as", "阿含經故事選", "asi.htm"),
    ("book/bb", "學佛的基本認識", "bbi.htm"),
    ("book/buhis", "印度佛教思想史要略", "buhisi.htm"),
    ("book/mn12", "中阿含經十二選", "mn12i.htm"),
    ("book/nn20", "雜阿含經二十選", "nn20i.htm"),
    ("book/tb", "阿含經隨身剪輯", "tbi.htm"),
]

ANN_ORDER = ["san1", "san2", "san3", "san4", "san5", "san6",
             "man1", "man2", "man3", "dan1",
             "aan1", "aan2", "aan3", "sn", "mn"]

def strip_tags(h):
    return re.sub(r"<[^>]+>", "", h)

def gz_write(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    raw = json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", compresslevel=9, mtime=0) as f:
        f.write(raw)
    data = buf.getvalue()
    io.open(path, "wb").write(data)
    return len(raw), len(data)

def first_lines(html_text, n=12):
    lines = [x.strip() for x in strip_tags(html_text).split("\n")]
    return [x for x in lines if x]

# ---------------- 加载 ----------------

def load_pages():
    p = os.path.join(BASE, "数据", "_pages.jsonl")
    out = []
    for line in io.open(p, encoding="utf-8"):
        out.append(json.loads(line))
    return out

# ---------------- 分组 ----------------

def first_paren(s):
    m = re.match(r"\s*\(([^)]*)\)", s or "")
    return m.group(1) if m else ""

def group_of(rec, sn_map):
    cat = rec["cat"]
    nm, sub = rec["nm"], rec["sub"]
    if cat == "SN":
        m = re.search(r"相應部(\d+)相應", nm)
        if m:
            k = int(m.group(1))
            name = first_paren(sub).split("/")[0].strip()
            if name:
                sn_map[k] = name
            return k
        return 0
    if cat == "AN":
        m = re.search(r"增支部(\d+)集", nm)
        return int(m.group(1)) if m else 0
    if cat in ("SA", "MA", "DA", "AA", "It", "Ud", "MN", "DN"):
        name = first_paren(sub).split("/")[0].strip()
        return name
    return ""

def chapter_title(rec, book_name):
    lines = first_lines(rec["blk"][0][2], 12)
    lines = [l for l in lines if l != "简体" and "莊春江" not in l and "初稿" not in l
             and "更新" not in l and l != book_name and not l.startswith("(")]
    if not lines:
        return rec["nm"][:40]
    pat = re.compile(r"^(第[\s一二三四五六七八九十百]+[章節選篇]|§|\d{1,3}[.．])")
    idx = None
    for i, l in enumerate(lines[:6]):
        if pat.match(l):
            idx = i
            break
    if idx is None:
        return lines[0][:50]
    t = lines[idx]
    if idx + 1 < len(lines):
        nxt = lines[idx + 1]
        if len(nxt) < 32 and not nxt.endswith(("。", "，", "；", "：", "！", "？")):
            t += " " + nxt
    return re.sub(r"\s+", " ", t.replace("\u3000", " ")).strip()[:60]

# ---------------- 注释与比对表 ----------------

def build_notes():
    notes = {}
    nd = os.path.join(SRC, "note")
    for i in range(10):
        p = os.path.join(nd, "note%d.js" % i)
        if not os.path.exists(p):
            continue
        raw = io.open(p, encoding="utf-8", errors="replace").read()
        m = re.search(r"=\s*(\{.*\})\s*;?\s*$", raw, re.S)
        if not m:
            print("WARN note parse", p)
            continue
        try:
            d = json.loads(m.group(1))
        except Exception as e:
            print("WARN note json", p, e)
            continue
        for k, v in d.items():
            notes[k] = v
    return notes

def build_map():
    p = os.path.join(SRC, "map.js")
    raw = io.open(p, encoding="utf-8", errors="replace").read()
    out = {}
    for name in ("SN_MAP", "AN_MAP"):
        m = re.search(name + r"\s*=\s*(\{.*?\})\s*;", raw, re.S)
        if m:
            try:
                out[name] = json.loads(m.group(1))
            except Exception as e:
                print("WARN map", name, e)
    return out

def load_ts(path):
    d = collections.OrderedDict()
    for line in io.open(path, encoding="utf-8"):
        if line.startswith("#") or not line.strip():
            continue
        parts = line.rstrip("\n").split("\t")
        if len(parts) >= 2:
            d[parts[0]] = parts[1].split(" ")[0]
    return d

def build_t2s():
    tool = os.path.join(BASE, "工具")
    ph = load_ts(os.path.join(tool, "TSPhrases.txt"))
    ch = load_ts(os.path.join(tool, "TSCharacters.txt"))
    plist = sorted(ph.items(), key=lambda kv: -len(kv[0]))
    return {"p": [[k, v] for k, v in plist], "c": dict(ch)}

# ---------------- 主流程 ----------------

def main():
    recs = load_pages()
    by_rel = {r["p"]: r for r in recs}

    # 分类收集
    sutra = collections.defaultdict(list)
    books = collections.defaultdict(list)
    docs = []
    for r in recs:
        rel = r["p"]
        k = E.classify(rel)
        if not any(b[2].strip() for b in r["blk"]):
            continue
        if k == "sutra" and r["num"] == 0:
            docs.append(r)
            continue
        if k == "sutra":
            sutra[r["cat"]].append(r)
        elif k == "book":
            books["/".join(rel.split("/")[:2])].append(r)
        elif k in ("study", "doc"):
            docs.append(r)
        elif k == "index":
            docs.append(r)

    # 去掉不需要的辅助页（留言板、下载页、词典说明）
    docs = [d for d in docs if not d["p"].startswith(("le/", "ad/"))]

    os.makedirs(DATA, exist_ok=True)
    os.makedirs(ASSETS, exist_ok=True)

    total_raw = total_gz = 0
    report = []

    # 页面数据
    sn_map = {}
    page_files = {}
    for cat in CAT_ORDER:
        rs = sutra.get(cat, [])
        if not rs:
            continue
        obj = {}
        for r in rs:
            pid = r["p"][:-4]
            obj[pid] = [r["nm"], r["sub"], r["n"], r["s"], r["tp"], r["blk"]]
        raw_len, gz_len = gz_write(os.path.join(DATA, "pages", cat + ".json.gz"), obj)
        total_raw += raw_len; total_gz += gz_len
        report.append(("pages/" + cat, len(obj), raw_len, gz_len))
        page_files[cat] = rs

    # 著作
    book_obj = {}
    for b, name, idx in BOOKS:
        for r in books.get(b, []):
            pid = r["p"][:-4]
            book_obj[pid] = [r["nm"], r["sub"], r["n"], r["s"], r["tp"], r["blk"]]
    if book_obj:
        raw_len, gz_len = gz_write(os.path.join(DATA, "pages", "book.json.gz"), book_obj)
        total_raw += raw_len; total_gz += gz_len
        report.append(("pages/book", len(book_obj), raw_len, gz_len))

    # 参考页
    doc_obj = {}
    for r in docs:
        pid = r["p"][:-4]
        if not any(x[2].strip() for x in r["blk"]):
            continue
        doc_obj[pid] = [r["nm"] or r["t"], r["sub"], r["n"], r["s"], r["tp"], r["blk"]]
    if doc_obj:
        raw_len, gz_len = gz_write(os.path.join(DATA, "pages", "doc.json.gz"), doc_obj)
        total_raw += raw_len; total_gz += gz_len
        report.append(("pages/doc", len(doc_obj), raw_len, gz_len))

    # 目录
    toc_cats = []
    for cat in CAT_ORDER:
        rs = page_files.get(cat, [])
        if not rs:
            continue
        rs = sorted(rs, key=lambda r: r["num"])
        groups = collections.OrderedDict()
        for r in rs:
            key = group_of(r, sn_map)
            if isinstance(key, int):
                key = ("%d" % key) if cat == "AN" else ("__%d" % key)
            groups.setdefault(key, []).append(r)
        glist = []
        for key, rlist in groups.items():
            if cat == "SN":
                num = int(key[2:]) if key.startswith("__") else 0
                gname = sn_map.get(num) or ("%d相應" % num)
                if not num:
                    gname = "其他"
            elif cat == "AN":
                gname = key + "集"
            else:
                gname = key or "全部"
            glist.append({"n": gname, "p": [[r["p"][:-4], r["num"], r["nm"]] for r in rlist]})
        toc_cats.append({"id": cat, "n": CAT_NAMES.get(cat, cat), "g": glist})

    toc_books = []
    for b, name, idx in BOOKS:
        rs = books.get(b, [])
        if not rs:
            continue
        if b == "book/ann":
            order = {n: i for i, n in enumerate(ANN_ORDER)}
            rs = sorted(rs, key=lambda r: (order.get(r["p"].split("/")[-1][:-4], 99), r["num"]))
        else:
            # 从目录页链接顺序取章节序
            ip = os.path.join(SRC, "book", b.split("/")[1], idx)
            order = []
            if os.path.exists(ip):
                raw = io.open(ip, encoding="utf-8", errors="replace").read()
                for h in re.findall(r'href="([^"#]+\.htm)"', raw, re.I):
                    h = os.path.basename(h)
                    if h.endswith("_s.htm") or h.startswith("."):
                        continue
                    order.append(h[:-4])
            oidx = {n: i for i, n in enumerate(order)}
            rs = sorted(rs, key=lambda r: (oidx.get(r["p"].split("/")[-1][:-4], 999), r["num"]))
        chapters = []
        for r in rs:
            pid = r["p"][:-4]
            chapters.append([pid, r["num"], chapter_title(r, name)])
        toc_books.append({"id": b, "n": name, "p": chapters})

    toc_docs = []
    STUDY_NAMES = {
        "study/index": "巴利經文自學",
        "study/text": "經文解讀範例",
        "study/ending": "巴利語語尾變化表",
        "study/dic": "查字典要領",
        "study/note": "簡要巴漢辭典",
    }
    for r in docs:
        pid = r["p"][:-4]
        if pid not in doc_obj:
            continue
        if pid in STUDY_NAMES:
            nm = STUDY_NAMES[pid]
        elif r["cat"] in CAT_NAMES and r["p"].endswith("index.htm"):
            nm = CAT_NAMES[r["cat"]] + "凡例"
        else:
            nm = r["nm"] or r["t"] or pid
        toc_docs.append([pid, nm])

    toc = {"v": 1, "cats": toc_cats, "books": toc_books, "docs": toc_docs}
    raw_len, gz_len = gz_write(os.path.join(DATA, "toc.json.gz"), toc)
    total_raw += raw_len; total_gz += gz_len
    report.append(("toc", 1, raw_len, gz_len))
    print("toc size raw=%d gz=%d" % (raw_len, gz_len))

    notes = build_notes()
    raw_len, gz_len = gz_write(os.path.join(DATA, "notes.json.gz"), notes)
    total_raw += raw_len; total_gz += gz_len
    report.append(("notes", len(notes), raw_len, gz_len))

    cmap = build_map()
    raw_len, gz_len = gz_write(os.path.join(DATA, "map.json.gz"), cmap)
    total_raw += raw_len; total_gz += gz_len
    report.append(("map", 1, raw_len, gz_len))

    t2s = build_t2s()
    raw_len, gz_len = gz_write(os.path.join(DATA, "t2s.json.gz"), t2s)
    total_raw += raw_len; total_gz += gz_len
    report.append(("t2s", len(t2s["c"]), raw_len, gz_len))

    # 图片
    imgs = set()
    for obj in list(page_files.values()) + [list(book_obj.items()), docs]:
        pass
    all_objs = []
    for cat, rs in page_files.items():
        all_objs.extend(rs)
    all_objs.extend(books_all := [r for b in books.values() for r in b])
    all_objs.extend(docs)
    for r in all_objs:
        for k, src, h in r["blk"]:
            for m in re.finditer(r'<img[^>]+src="([^"]+)"', h):
                imgs.add(m.group(1))
    copied = 0
    copied_bytes = 0
    for s in imgs:
        if s.startswith(("http://", "https://", "data:")):
            continue
        sp = os.path.join(SRC, s.replace("/", os.sep))
        if not os.path.exists(sp):
            print("MISS img", s)
            continue
        dp = os.path.join(ASSETS, s.replace("/", os.sep))
        os.makedirs(os.path.dirname(dp), exist_ok=True)
        shutil.copy2(sp, dp)
        copied += 1
        copied_bytes += os.path.getsize(sp)

    # 报告
    print("\n%-16s %6s %10s %10s" % ("file", "count", "raw", "gz"))
    for name, cnt, raw_len, gz_len in report:
        print("%-16s %6d %9.2fMB %9.2fMB" % (name, cnt, raw_len / 1048576, gz_len / 1048576))
    print("-" * 50)
    print("%-16s %6s %9.2fMB %9.2fMB" % ("TOTAL", "", total_raw / 1048576, total_gz / 1048576))
    print("images: %d files, %.2f MB" % (copied, copied_bytes / 1048576))
    print("notes:", len(notes))

if __name__ == "__main__":
    main()

