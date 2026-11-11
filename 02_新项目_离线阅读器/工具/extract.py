# -*- coding: utf-8 -*-
"""
P1 数据抽取 v3
不依赖 lxml 的整页树（libxml2 会按 HTML4 规则丢弃畸形页面里的内容），
改为：在原始字符串里按 <div> 深度配对定位内容块，再对每个块做容忍式清洗。

用法:
    python extract.py --out ..\\数据\\_pages.jsonl [--limit N]
"""
import os, re, io, sys, json, html, argparse, posixpath
from lxml import html as LH

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "源数据", "agama.buddhason.org_simp"))

INLINE = {"a", "b", "i", "u", "s", "sup", "sub", "span", "font", "br", "img"}
BLOCK = {"p", "div", "table", "tr", "td", "th", "tbody", "thead", "ol", "ul", "li",
         "hr", "blockquote", "h1", "h2", "h3", "h4", "h5", "h6", "center"}
KEEP = INLINE | BLOCK
DROP = {"script", "style", "link", "meta", "iframe", "object", "embed", "form",
        "input", "noscript", "title", "head"}

SCRIPT_RE = re.compile(r"<script\b.*?</script\s*>", re.S | re.I)
STYLE_RE = re.compile(r"<style\b.*?</style\s*>", re.S | re.I)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
DIV_TAG_RE = re.compile(r"<div\b[^>]*>", re.I)
CLASS_ATTR_RE = re.compile(r"\bclass\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s>]+))", re.I)
ID_ATTR_RE = re.compile(r"\bid\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s>]+))", re.I)

NOTE_RE = re.compile(r"note\s*\(\s*this\s*,\s*(\d+)\s*\)", re.I)
LOCAL_RE = re.compile(r"local\s*\(\s*this\s*,\s*(\d+)\s*\)", re.I)
OVER_RE = re.compile(r"note_over\s*\(\s*(\d+)\s*\)", re.I)
FS_RE = re.compile(r"font-size\s*:\s*([\d.]+)\s*(px|pt|em|%)", re.I)

CHROME_IDS = {"lang-bar", "notediv"}

def norm_ws(s):
    return re.sub(r"\s+", "", s or "")

def strip_tags(h):
    return re.sub(r"<[^>]+>", "", h)

def esc_text(s):
    return html.escape(s, quote=False)

def esc_attr(s):
    return html.escape(s, quote=True)

def px_of(val, unit):
    v = float(val)
    if unit == "pt":
        return v * 4 / 3
    if unit == "em":
        return v * 16
    if unit == "%":
        return v * 16 / 100
    return v

def fs_bucket(px):
    if px >= 30:
        return "xxl"
    if px >= 22:
        return "xl"
    if px >= 18.5:
        return "l"
    if px >= 16.5:
        return "m"
    return None

def attr_val(m):
    return m.group(1) or m.group(2) or m.group(3) or ""

def resolve_href(href, page_rel):
    if not href:
        return ""
    if href.startswith(("http://", "https://", "mailto:")):
        return href
    if href.startswith("#"):
        return href
    if href.startswith("javascript:"):
        return ""
    href = href.split("#")[0]
    if not href:
        return ""
    base = posixpath.dirname(page_rel)
    return posixpath.normpath(posixpath.join(base, href))

# ---------------- 清洗 ----------------

class Cleaner:
    def __init__(self, page_rel):
        self.page_rel = page_rel

    def attrs_for(self, el):
        tag = el.tag
        a = {}
        if tag == "a":
            onmouse = el.get("onmouseover") or ""
            m = NOTE_RE.search(onmouse)
            if m:
                a["class"] = "n"
                a["data-n"] = m.group(1)
            else:
                m = LOCAL_RE.search(onmouse) or OVER_RE.search(onmouse)
                if m:
                    a["class"] = "l"
                    a["data-n"] = m.group(1)
                else:
                    href = resolve_href(el.get("href") or "", self.page_rel)
                    if href:
                        a["href"] = href
            eid = el.get("id") or ""
            if eid.startswith("link"):
                a["id"] = eid
        elif tag == "img":
            src = resolve_href(el.get("src") or "", self.page_rel)
            if src:
                a["src"] = src
            if el.get("alt"):
                a["alt"] = el.get("alt")
            for k in ("width", "height"):
                v = (el.get(k) or "").strip()
                if v.isdigit() and int(v) <= 1200:
                    a[k] = v
        elif tag in ("td", "th"):
            for k in ("colspan", "rowspan"):
                if el.get(k):
                    a[k] = el.get(k)
        eid = el.get("id") or ""
        if eid.startswith(("note", "div")):
            a["id"] = eid
        # 只有短元素才保留字号/颜色（长块是正文包裹层，不是标题）
        try:
            blen = len(el.text_content() or "")
        except Exception:
            blen = 999
        if blen <= 40:
            fs = FS_RE.search(el.get("style") or "")
            if fs:
                b = fs_bucket(px_of(fs.group(1), fs.group(2)))
                if b:
                    a["data-fs"] = b
            if tag in ("font", "span"):
                color = el.get("color") or ""
                if re.match(r"^#[0-9a-fA-F]{6}$", color):
                    a["data-c"] = color.upper()
        cls = el.get("class") or ""
        if "sutra_name" in cls.split():
            a["class"] = (a.get("class", "") + " sn").strip()
        elif "note" in cls.split() and tag == "div":
            a["class"] = (a.get("class", "") + " pnote").strip()
        return a

    def ser(self, el):
        tag = el.tag
        if not isinstance(tag, str):
            return ""
        if tag in DROP:
            return ""
        if "simp" in (el.get("class") or "").split():
            return ""
        inner = esc_text(el.text) if el.text else ""
        for ch in el:
            inner += self.ser(ch)
            if ch.tail:
                inner += esc_text(ch.tail)
        if tag == "br":
            return "<br>" + inner
        if tag not in KEEP:
            return inner
        out_tag = "span" if tag == "font" else tag
        attrs = self.attrs_for(el)
        astr = "".join(' %s="%s"' % (k, esc_attr(v)) for k, v in attrs.items())
        if out_tag in ("br", "img", "hr"):
            return "<%s%s>" % (out_tag, astr)
        return "<%s%s>%s</%s>" % (out_tag, astr, inner, out_tag)

def inner_html(el, page_rel):
    c = Cleaner(page_rel)
    out = esc_text(el.text) if el.text else ""
    for ch in el:
        out += c.ser(ch)
        if ch.tail:
            out += esc_text(ch.tail)
    return out

def clean_fragment(inner, page_rel):
    """把一段 HTML 片段清洗成受控标记；失败时退回正则清洗。"""
    try:
        frag = LH.fragment_fromstring(inner, create_parent="div")
        out = inner_html(frag, page_rel)
        if out.strip():
            return out
    except Exception:
        pass
    s = re.sub(r"<(?!br|/br|a\s|/a>|b>|/b>|i>|/i>|u>|/u>|span|/span>|img\s|sup>|/sup>|sub>|/sub>)[^>]*>", "", inner, flags=re.I)
    return s.strip()

# ---------------- 原始字符串定位 ----------------

def find_div_end(s, tag_start):
    """从 <div ...> 的起始位置，按深度配对找到结束位置（返回结束偏移）。"""
    depth = 1
    pos = tag_start
    pat = re.compile(r"<(/?)div\b", re.I)
    while True:
        m = pat.search(s, pos)
        if not m:
            return -1
        depth += -1 if m.group(1) else 1
        pos = m.end()
        if depth == 0:
            j = s.find(">", m.end())
            return j + 1 if j >= 0 else -1

def find_blocks(raw, page_rel):
    """按文档顺序返回 [(kind, src, clean_html)]。"""
    pre = SCRIPT_RE.sub("", raw)
    pre = STYLE_RE.sub("", pre)
    pre = COMMENT_RE.sub("", pre)

    spans = []
    for m in DIV_TAG_RE.finditer(pre):
        tag = m.group(0)
        cm = CLASS_ATTR_RE.search(tag)
        if not cm:
            continue
        cls = attr_val(cm).split()
        if not cls or "simp" in cls:
            continue
        if not ("trad" in cls or "pali" in cls or "comp" in cls):
            continue
        start = m.start()
        if any(a <= start < b for a, b in spans):
            continue
        end = find_div_end(pre, m.end())
        if end < 0:
            continue
        spans.append((start, end))

    out = []
    for a, b in spans:
        tag_end = pre.find(">", a) + 1
        tag = pre[a:tag_end]
        cm = CLASS_ATTR_RE.search(tag)
        cls = attr_val(cm).split() if cm else []
        close = pre.rfind("</div", tag_end, b)
        if close < 0:
            close = b
        inner = pre[tag_end:close]
        if "pali" in cls:
            out.append(["pali", "", clean_fragment(inner, page_rel)])
        elif "comp" in cls:
            out.append(["cmp", "", clean_fragment(inner, page_rel)])
        else:
            src = "agama" if "agama" in cls else ("nikaya" if "nikaya" in cls else "")
            out.append(["zh", src, clean_fragment(inner, page_rel)])
    return out

CHROME_RE = re.compile(r'<div[^>]*id="(?:lang-bar|notediv)"[^>]*>.*?</div\s*>', re.S | re.I)

def strip_chrome(s):
    return CHROME_RE.sub("", s)

def body_inner(raw):
    m = re.search(r"<body\b[^>]*>", raw, re.I)
    if not m:
        return raw
    rest = raw[m.end():]
    e = re.search(r"</body\s*>", rest, re.I)
    if e:
        rest = rest[:e.start()]
    return strip_chrome(rest)

def find_maindiv(raw):
    for m in DIV_TAG_RE.finditer(raw):
        tag = m.group(0)
        im = ID_ATTR_RE.search(tag)
        if im and attr_val(im) == "maindiv":
            end = find_div_end(raw, m.end())
            if end > 0:
                return raw[m.end():end - len("</div>")]
    return None

# ---------------- 页面分类 ----------------

CATS = {"SA", "SN", "AN", "MA", "MN", "DA", "DN", "AA", "Ud", "It", "Ap", "Ja",
        "Su", "Th", "Vi", "Ti", "Cp", "Mi", "Ps", "Bv", "Dh", "Pv", "Kh", "Ni"}

def classify(rel):
    parts = rel.split("/")
    if rel.startswith("book/"):
        return "book"
    if rel.startswith("note/"):
        return "note"
    if rel.startswith("study/"):
        return "study"
    if "/" in rel and parts[0] in CATS:
        if parts[-1].lower().startswith("index"):
            return "index"
        return "sutra"
    if rel.startswith(("le/", "ad/")):
        return "doc"
    return "root"

def num_of(rel):
    m = re.search(r"(\d+)", posixpath.basename(rel))
    return int(m.group(1)) if m else 0

def page_title(raw):
    m = re.search(r"<title>(.*?)</title>", raw, re.S | re.I)
    return re.sub(r"\s+", " ", html.unescape(strip_tags(m.group(1)))).strip() if m else ""

def first_line_text(h):
    t = strip_tags(h)
    t = re.sub(r"[ \t\r\f\v\u00a0]+", " ", t)
    t = re.sub(r"\n+", "\n", t).strip()
    return t.split("\n")[0].strip() if t else ""

def grab(raw, label):
    m = re.search(label + r"[:：]\s*([^<\r\n]{1,90})", raw)
    return re.sub(r"\s+", " ", html.unescape(m.group(1))).strip() if m else ""

def analyse_text(rec):
    for kind, src, h in rec["blk"]:
        if kind not in ("zh", "doc"):
            continue
        line = first_line_text(h)
        m = re.search(r'<span class="sn">(.*?)</span>', h, re.S)
        if m:
            nm = strip_tags(m.group(1)).strip()
        else:
            mu = re.search(r"<u>(.*?)</u>", h, re.S)
            nm = strip_tags(mu.group(1)).strip() if mu else ""
        if nm:
            idx = line.find(nm)
            rest = line[idx + len(nm):].strip() if idx >= 0 else ""
            rec["nm"] = nm
            rec["sub"] = rest
        if rec["nm"]:
            break
        # 小部：页面是"小部 / 本生經典 / (第N部分)"这类合集页
        lines = [x.strip() for x in strip_tags(h).split("\n") if x.strip()]
        for i, ln in enumerate(lines[:8]):
            if "經典" in ln or "經集" in ln:
                rec["nm"] = ln
                if i + 1 < len(lines):
                    rec["sub"] = lines[i + 1].strip()
                break
        break
    if not rec["nm"]:
        rec["nm"] = rec["t"]

def add_note_spans(rec, raw):
    """把页面内的注释文字（note 链接）收集成字典，供前端弹窗。
    这里只做统计，真正的注释数据在 build_notes 里合并。"""

# ---------------- 各类页面 ----------------

def extract_sutra(path, rel, raw):
    rec = {"p": rel, "cat": rel.split("/")[0] if "/" in rel else "", "num": num_of(rel),
           "t": page_title(raw), "nm": "", "sub": "", "n": "", "s": "", "tp": "", "blk": []}
    north = re.search(r'<div id="north".*?</div>', raw, re.S | re.I)
    if north:
        frag = north.group(0)
        for cls, key in (("agama", "n"), ("nikaya", "s"), ("subject", "tp")):
            m = re.search(r'<span[^>]*class="[^"]*%s[^"]*"[^>]*>(.*?)</span>' % cls, frag, re.S | re.I)
            if m:
                rec[key] = re.sub(r"\s+", " ", strip_tags(m.group(1))).strip()
    rec["blk"] = find_blocks(raw, rel)
    analyse_text(rec)
    if not rec["n"]:
        rec["n"] = grab(raw, "北傳")
    if not rec["s"]:
        rec["s"] = grab(raw, "南傳")
    if not rec["tp"]:
        rec["tp"] = grab(raw, "關涉主題")
    if not rec["blk"]:
        body = body_inner(raw)
        h = clean_fragment(body, rel)
        if h.strip():
            rec["blk"] = [["doc", "", h]]
    return rec

def extract_book(path, rel, raw):
    rec = {"p": rel, "cat": "book", "num": num_of(rel), "t": page_title(raw),
           "nm": "", "sub": "", "n": "", "s": "", "tp": "", "blk": []}
    main = find_maindiv(raw)
    if main is not None:
        src = main
    else:
        src = body_inner(raw)
    h = clean_fragment(src, rel)
    if h.strip():
        rec["blk"] = [["doc", "", h]]
    rec["nm"] = rec["t"]
    return rec

def extract_doc(path, rel, raw):
    rec = {"p": rel, "cat": rel.split("/")[0] if "/" in rel else "", "num": num_of(rel),
           "t": page_title(raw), "nm": "", "sub": "", "n": "", "s": "", "tp": "", "blk": []}
    h = clean_fragment(body_inner(raw), rel)
    if h.strip():
        rec["blk"] = [["doc", "", h]]
    return rec

def parse_page(path, rel):
    raw = io.open(path, encoding="utf-8", errors="replace").read()
    raw = raw.lstrip("\ufeff \r\n\t")
    i = raw.lower().find("<html")
    if i > 0:
        raw = raw[i:]
    k = classify(rel)
    if k == "sutra":
        return extract_sutra(path, rel, raw)
    if k == "book":
        return extract_book(path, rel, raw)
    return extract_doc(path, rel, raw)

# ---------------- 主流程 ----------------

def list_files():
    files = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        for fn in filenames:
            if not fn.lower().endswith((".htm", ".html")):
                continue
            if fn.lower().endswith("_s.htm") or fn.startswith("."):
                continue
            if "search" in fn.lower() or "_demo" in fn.lower():
                continue
            rel = os.path.relpath(os.path.join(dirpath, fn), ROOT).replace("\\", "/")
            files.append(rel)
    files.sort()
    return files

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    files = list_files()
    if args.limit:
        files = files[:args.limit]

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    stats = {"n": 0, "empty": 0, "kinds": {}, "chars": 0}
    empties = []
    with io.open(args.out, "w", encoding="utf-8") as f:
        for rel in files:
            try:
                rec = parse_page(os.path.join(ROOT, rel), rel)
            except Exception as e:
                print("ERR", rel, e, file=sys.stderr)
                continue
            k = classify(rel)
            stats["kinds"][k] = stats["kinds"].get(k, 0) + 1
            stats["n"] += 1
            alltext = "".join(strip_tags(b[2]) for b in rec["blk"])
            stats["chars"] += len(alltext)
            if not alltext.strip():
                stats["empty"] += 1
                empties.append(rel)
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    print("empties:", empties[:30])

if __name__ == "__main__":
    main()
