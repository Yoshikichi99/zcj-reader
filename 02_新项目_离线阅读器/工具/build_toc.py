# -*- coding: utf-8 -*-
"""生成原型数据（v4）：首页/栏目页直接搬原站 HTML，只改链接。"""
import os, io, sys, json, gzip, re, shutil, posixpath
from lxml import html as LH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PKG = os.path.join(BASE, "数据", "package")
SRC = os.path.join(BASE, "源数据", "agama.buddhason.org_simp")
OUT = os.path.join(BASE, "前端", "proto")
ASSETS = os.path.join(OUT, "assets")
os.makedirs(ASSETS, exist_ok=True)

def load(name):
    return json.loads(gzip.open(os.path.join(PKG, name), "rt", encoding="utf-8").read())

corpus = {}
for fn in os.listdir(os.path.join(PKG, "corpus")):
    corpus.update(load(os.path.join("corpus", fn)))
pages = load("pages.json.gz")
books = load("books.json.gz")
docs = load("docs.json.gz")

CAT_CODES = {"SA", "SN", "MA", "MN", "DA", "DN", "AA", "AN", "ZA",
             "Kh", "Dh", "Ud", "It", "Su", "Vi", "Pv", "Th", "Ti",
             "Ja", "Ap", "Bv", "Cp", "Ni", "Mi", "Ps"}
PAGE_IDS = set(pages)
BOOK_IDS = set(books)
DOC_IDS = set(docs)
# 原站提取时漏掉的下載页（含 7 本 PDF 链接）
for _extra in ("le/le1",):
    _p = os.path.join(SRC, _extra + ".htm")
    if os.path.exists(_p) and _extra not in docs:
        docs[_extra] = ["下載", []]
        DOC_IDS.add(_extra)

SCRIPT = re.compile(r"<script\b.*?</script\s*>", re.S | re.I)
STYLE = re.compile(r"<style\b.*?</style\s*>", re.S | re.I)
COMMENT = re.compile(r"<!--.*?-->", re.S)
CHROME = re.compile(r'<div[^>]*id="(?:lang-bar|notediv)"[^>]*>.*?</div\s*>', re.S | re.I)

def trad_body(raw):
    raw = raw.lstrip("\ufeff \r\n\t")
    m = re.search(r'<div class="trad">', raw, re.I)
    if m:
        s = m.end()
        # 优先切在简体块之前（原站有些页 trad 块没闭合）
        e = raw.find('<div class="simp">', s)
        if e > 0:
            body = raw[s:e]
            return re.sub(r"</div>\s*$", "", body)
        depth = 1
        pos = s
        pat = re.compile(r"<(/?)div\b", re.I)
        while True:
            mm = pat.search(raw, pos)
            if not mm:
                break
            depth += -1 if mm.group(1) else 1
            pos = mm.end()
            if depth == 0:
                close = raw.rfind("</div", 0, mm.end())
                return raw[s:close] if close > 0 else raw[s:]
    b = re.search(r"<body\b[^>]*>", raw, re.I)
    e = re.search(r"</body\s*>", raw, re.I)
    if b and e:
        return raw[b.end():e.start()]
    return raw

def resolve(href, base):
    if not href:
        return None
    h = href.split("#")[0]
    if h.startswith(("http:", "https:", "mailto:")):
        return href
    if h.startswith(("javascript:", "#")):
        return None
    target = posixpath.normpath(posixpath.join(base, h))
    if target in (".", "index.htm"):
        return "#/"
    if target.endswith("/index.htm"):
        d = target.split("/")[0]
        if d in CAT_CODES:
            return "#/c/" + d
        return "#/d/" + target[:-4]
    low = target
    if low in PAGE_IDS:
        return "#/p/" + low[:-4]
    base_no = low[:-4] if low.endswith(".htm") else low
    if base_no in BOOK_IDS:
        return "#/p/" + base_no
    if base_no in DOC_IDS:
        return "#/d/" + base_no
    return None

def extract_html(raw):
    """用 lxml 解析原文，取 trad 块（或 body），输出标签平衡的 HTML。"""
    try:
        doc = LH.document_fromstring(raw)
    except Exception:
        return raw
    ds = doc.xpath('//div[contains(@class,"trad")]')
    node = ds[0] if ds else doc.find("body")
    if node is None:
        return raw
    # 去掉简体副本与语言条（有些页面 trad 未闭合，会把 simp 包进来）
    for bad in node.xpath('.//div[contains(@class,"simp")] | .//*[@id="lang-bar"] | .//*[@id="notediv"]'):
        p = bad.getparent()
        if p is not None:
            p.remove(bad)
    html = LH.tostring(node, encoding="unicode", method="html")
    if ds:
        m = re.match(r"<div[^>]*>", html)
        if m:
            html = html[m.end():]
        html = re.sub(r"</div>\s*$", "", html)
    else:
        m = re.search(r"<body[^>]*>", html)
        if m:
            html = html[m.end():]
        html = re.sub(r"</body>\s*$", "", html)
    return html

def clean_page(raw, base):
    # 原站笔误：<style="..."> 应为 <span style="...">，否则会吞掉整页
    raw = re.sub(r'<style\s*="', '<span style="', raw, flags=re.I)
    raw = SCRIPT.sub("", raw)
    raw = STYLE.sub("", raw)
    raw = COMMENT.sub("", raw)
    raw = CHROME.sub("", raw)
    html = extract_html(raw)

    def fix_img(m):
        src = m.group(1)
        if src.startswith(("http:", "https:", "data:")):
            return m.group(0)
        rel = posixpath.normpath(posixpath.join(base, src))
        for root in (SRC, os.path.join(os.path.dirname(SRC))):
            p = os.path.join(root, rel.replace("/", os.sep))
            if os.path.exists(p):
                dst = os.path.join(ASSETS, rel.replace("/", os.sep))
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(p, dst)
                return 'src="assets/%s"' % rel
        return m.group(0)

    html = re.sub(r'src="([^"]+)"', fix_img, html, flags=re.I)

    def fix_a(m):
        href = m.group(1)
        if href.startswith("#") and not href.startswith("#/"):
            return 'data-anchor="%s" class="anch"' % href[1:]
        low = href.lower()
        if low.endswith(".pdf"):
            # PDF 不内置，统一导向「未实装」说明页
            return 'href="#/notice"'
        if low.rstrip("/").endswith("d.htm"):
            # 影音下載：音频为独立扩展包，应用内不打开
            return 'href="#/notice"'
        new = resolve(href, base)
        if new is None:
            return ""
        return 'href="%s"' % new

    html = re.sub(r'href="([^"]+)"', fix_a, html, flags=re.I)
    html = re.sub(r"<form\b", '<form onsubmit="return false"', html, flags=re.I)
    html = re.sub(r"#EDFFE1|#edffe1", "#EFFFDE", html)
    html = re.sub(r"\son\w+\s*=\s*\"[^\"]*\"", "", html, flags=re.I)
    return html.strip()

# ---------- 首页 ----------
home_raw = io.open(os.path.join(SRC, "index.htm"), encoding="utf-8", errors="replace").read()
home_page = clean_page(home_raw, "")

# ---------- 栏目 ----------
CAT_NAMES = {
    "SA": "雜阿含", "SN": "相應部", "MA": "中阿含", "MN": "中部",
    "DA": "長阿含", "DN": "長部", "AA": "增壹阿含", "AN": "增支部",
    "Kh": "小誦", "Dh": "法句", "Ud": "優陀那", "It": "如是語",
    "Su": "經集", "Vi": "天宮事", "Pv": "餓鬼事", "Th": "長老偈",
    "Ti": "長老尼偈", "Ja": "本生", "Ap": "譬喻", "Bv": "佛種姓",
    "Cp": "所行藏", "Ni": "大義釋", "Mi": "彌蘭王問", "Ps": "無解道",
    "ZA": "別譯雜阿含", "OTHER": "其他",
}
ORDER = ["SA", "SN", "MA", "MN", "DA", "DN", "AA", "AN", "ZA",
         "Kh", "Dh", "Ud", "It", "Su", "Vi", "Pv", "Th",
         "Ti", "Ja", "Ap", "Bv", "Cp", "Ni", "Mi", "Ps", "OTHER"]

def key_of_title(t):
    t = re.sub(r"\[[^\]]*\]", "", t or "").strip()
    pats = [
        (r"^雜阿含\s*(\d+)", ("SA",)), (r"^別譯雜阿含\s*(\d+)", ("ZA",)),
        (r"^增壹阿含(\d+)品(\d+)", ("AA",)), (r"^中阿含\s*(\d+)", ("MA",)),
        (r"^長阿含\s*(\d+)", ("DA",)), (r"^相應部(\d+)相應\s*(\d+)", ("SN",)),
        (r"^增支部(\d+)集\s*(\d+)", ("AN",)), (r"^中部\s*(\d+)", ("MN",)),
        (r"^長部\s*(\d+)", ("DN",)),
    ]
    for pat, pre in pats:
        m = re.match(pat, t)
        if m:
            return pre + tuple(m.groups())
    return None

owner = {}
ref_map = {}
for pid, rec in pages.items():
    k = key_of_title(rec[0])
    if k:
        owner[".".join(str(x) for x in k)] = pid
    for kk in rec[1]:
        ref_map.setdefault(kk, pid)
for k, pid in ref_map.items():
    owner.setdefault(k, pid)

def key_sort(k):
    parts = k.split(".")
    try:
        return (len(parts), [int(x) for x in parts[1:]])
    except ValueError:
        return (9, [])

cats = []
for code in ORDER:
    items = []
    if code == "OTHER" or any(k.split(".")[0] == code for k in corpus):
        for k, v in corpus.items():
            if k.split(".")[0] != code:
                continue
            pid = owner.get(k)
            if pid:
                items.append({"p": pid[:-4], "k": k})
        items.sort(key=lambda x: key_sort(x["k"]))
    if not items:
        for pid, rec in pages.items():
            if rec[5] != code or rec[6] == 0:
                continue
            items.append({"p": pid[:-4], "k": ""})
        items.sort(key=lambda x: x["p"])
    if not items:
        continue
    p = os.path.join(SRC, code, "index.htm")
    page_html = ""
    if os.path.exists(p):
        page_html = clean_page(io.open(p, encoding="utf-8", errors="replace").read(), code)
    cats.append({"id": code, "n": CAT_NAMES.get(code, code), "items": items,
                 "page": page_html})

# ---------- 著作 ----------
ANN_ORDER = ["san1", "san2", "san3", "san4", "san5", "san6",
             "man1", "man2", "man3", "dan1", "aan1", "aan2", "aan3", "sn", "mn"]
BOOK_NAMES = {
    "book/ann": "阿含經南北傳對讀摘記", "book/as": "阿含經故事選",
    "book/bb": "學佛的基本認識", "book/buhis": "印度佛教思想史要略",
    "book/mn12": "中阿含經十二選", "book/nn20": "雜阿含經二十選",
    "book/tb": "阿含經隨身剪輯",
}
BOOK_INDEX = {
    "book/ann": "anni", "book/as": "asi", "book/bb": "bbi",
    "book/buhis": "buhisi", "book/mn12": "mn12i", "book/nn20": "nn20i", "book/tb": "tbi",
}

def chapter_title(html, book_name):
    t = re.sub(r"<[^>]+>", "\n", html)
    lines = [x.strip() for x in t.split("\n") if x.strip()]
    lines = [l for l in lines if l != "简体" and "莊春江" not in l and "初稿" not in l
             and "更新" not in l and l != book_name and not l.startswith("(")]
    if not lines:
        return ""
    pat = re.compile(r"^(第[\s一二三四五六七八九十百]+[章節選篇]|§|\d{1,3}[.．]|自\s*序|序|前\s*言|凡\s*例)")
    for l in lines[:6]:
        if pat.match(l):
            return l[:50]
    return lines[0][:50]

book_groups = {}
for pid, v in books.items():
    parts = pid.split("/")
    if len(parts) < 3:
        continue
    gid = "/".join(parts[:2])
    # 目录页本身不算章节（否则会出现「上一节/下一节」跨级）
    if pid.split("/")[-1] == BOOK_INDEX.get(gid, ""):
        continue
    book_groups.setdefault(gid, []).append((pid, v))

book_list = []
for gid, chs in book_groups.items():
    name = BOOK_NAMES.get(gid, gid)
    if gid == "book/ann":
        order = {n: i for i, n in enumerate(ANN_ORDER)}
        chs.sort(key=lambda x: (order.get(x[0].split("/")[-1], 99), x[0]))
    else:
        def sk(x):
            m = re.search(r"(\d+)$", x[0].split("/")[-1])
            return int(m.group(1)) if m else 9999
        chs.sort(key=sk)
    chapters = []
    for pid, v in chs:
        html = "".join(b[2] for b in v[1] if len(b) > 2)
        chapters.append({"id": pid, "t": chapter_title(html, name)[:50]})
    book_list.append({"id": gid, "n": name, "chapters": chapters, "idx": (gid + "/" + BOOK_INDEX[gid]) if gid in BOOK_INDEX else ""})

doc_list = [{"id": pid, "t": v[0] or pid} for pid, v in docs.items()]
doc_list.sort(key=lambda x: x["id"])

# ---------- 参考页 / 著作目录页：直接搬原站 ----------
static = {}
for did in sorted(DOC_IDS):
    d0 = did.split("/")[0]
    if d0 in CAT_CODES and did.endswith("/index"):
        continue          # 栏目首页已作为 cat.page
    if did in ("index", "index."):
        continue
    p = os.path.join(SRC, did + ".htm")
    if os.path.exists(p):
        static[did] = clean_page(io.open(p, encoding="utf-8", errors="replace").read(), posixpath.dirname(did))
for bid in sorted(BOOK_IDS):
    p = os.path.join(SRC, bid + ".htm")
    if not os.path.exists(p):
        continue
    base = posixpath.dirname(bid)
    static[bid] = clean_page(io.open(p, encoding="utf-8", errors="replace").read(), base)

toc = {"v": 1, "home": home_page, "cats": cats, "books": book_list, "docs": doc_list, "static": static}
buf = io.BytesIO()
with gzip.GzipFile(fileobj=buf, mode="wb", compresslevel=9, mtime=0) as f:
    f.write(json.dumps(toc, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
io.open(os.path.join(PKG, "toc.json.gz"), "wb").write(buf.getvalue())
print("toc：栏目", len(cats), "著作", len(book_list), "参考", len(doc_list),
      "home", len(home_page), "大小 %.2f MB" % (len(buf.getvalue()) / 1048576))
for c in cats[:4]:
    print("  ", c["id"], len(c["items"]), "page", len(c["page"]))
