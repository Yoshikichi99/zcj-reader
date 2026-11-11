# -*- coding: utf-8 -*-
"""从源数据抽取「经号 → 页面」映射，供栏目页的「經號 / 大正本 / 正聞本 / 佛光本」框直接跳转。

输出：前端/proto/data/num.json.gz 与 数据/package/num.json.gz
结构：{"v":1, "SA": {"tz": {"10": "SA/SA0010"}, "zw": {...}, "fg": {...}}, ...}
  tz = 大正本（北传）/ 本部经号（南传）
  zw = 正聞本
  fg = 佛光本
"""
import gzip
import json
import os
import re

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(BASE, "源数据", "agama.buddhason.org_simp")
OUTS = [
    os.path.join(BASE, "前端", "proto", "data", "num.json.gz"),
    os.path.join(BASE, "数据", "package", "num.json.gz"),
]

# 每类的取号规则：正则作用于拼接后的 title+sutra 文本
SIMPLE = {
    "SA": "雜阿含",
    "MA": "中阿含",
    "DA": "長阿含",
    "MN": "中部",
    "DN": "長部",
    "Ud": "優陀那",
    "It": "如是語",
}


def expand(part):
    """'1-4' -> ['1','2','3','4']；'12' -> ['12']"""
    m = re.match(r"^(\d+)\s*-\s*(\d+)$", part)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        if a <= b and b - a <= 200:
            return [str(i) for i in range(a, b + 1)]
    return [part.strip()] if part.strip() else []


def norm_num(s):
    return re.sub(r"\s+", "", s or "")


def read_text(path):
    for enc in ("utf-8", "big5", "cp950"):
        try:
            return open(path, "r", encoding=enc).read()
        except UnicodeDecodeError:
            continue
    return open(path, "r", encoding="utf-8", errors="replace").read()


def extract(cat, names):
    """返回 {scheme: {key: pageid}} 与统计"""
    out = {"tz": {}}
    if cat == "SA":
        out["zw"] = {}
        out["fg"] = {}
    if cat == "AA":
        out["fg"] = {}
    dup = 0
    used = 0
    for name in names:
        path = os.path.join(SRC, cat, name)
        t = read_text(path)
        title = (re.search(r"<title>(.*?)</title>", t, re.S) or [None, ""])[1]
        sutra = (re.search(r'class="sutra_name">(.*?)</span>', t, re.S) or [None, ""])[1]
        text = title + " " + sutra
        pid = cat + "/" + os.path.splitext(name)[0]
        keys = []

        if cat == "SA":
            m = re.search(SIMPLE["SA"] + r"\s*(\d+(?:-\d+)?)經", text)
            if m:
                keys = [( "tz", k) for k in expand(m.group(1))]
            m = re.search(r"正聞本\s*(\d+(?:-\d+)?)經", sutra)
            if m:
                keys += [("zw", k) for k in expand(m.group(1))]
            m = re.search(r"佛光本\s*(\d+(?:-\d+)?)經", sutra)
            if m:
                keys += [("fg", k) for k in expand(m.group(1))]
        elif cat == "AA":
            m = re.search(r"增壹阿含\s*(\d+)品\s*(\d+)經", text)
            if m:
                keys.append(("tz", "%s.%s" % (m.group(1), m.group(2))))
            m = re.search(r"佛光本\s*(\d+)經", sutra)
            if m:
                keys.append(("fg", m.group(1)))
        elif cat == "SN":
            m = re.search(r"相應部?\s*(\d+)相應\s*(\d+(?:-\d+)?)經", sutra)
            if m:
                keys = [("tz", "%s.%s" % (m.group(1), n)) for n in expand(m.group(2))]
        elif cat == "AN":
            m = re.search(r"增支部\s*(\d+)集\s*(\d+(?:-\d+)?)經", sutra)
            if m:
                keys = [("tz", "%s.%s" % (m.group(1), n)) for n in expand(m.group(2))]
        elif cat in SIMPLE:
            m = re.search(SIMPLE[cat] + r"\s*(\d+)經", text)
            if m:
                keys = [("tz", m.group(1))]

        for scheme, key in keys:
            key = norm_num(key)
            if not key:
                continue
            bucket = out.setdefault(scheme, {})
            if key in bucket and bucket[key] != pid:
                dup += 1
                continue
            bucket[key] = pid
            used += 1
    return out, used, dup


def main():
    data = {"v": 1}
    total = 0
    valid = None
    pp = os.path.join(BASE, "前端", "proto", "data", "pages.json.gz")
    if os.path.exists(pp):
        with gzip.open(pp, "rt", encoding="utf-8") as f:
            valid = {k[:-4] if k.endswith(".htm") else k for k in json.load(f)}
        print("参照 pages.json：%d 页" % len(valid))

    for cat in ["SA", "MA", "DA", "AA", "MN", "DN", "SN", "AN", "Ud", "It"]:
        d = os.path.join(SRC, cat)
        if not os.path.isdir(d):
            print("跳过（无目录）:", cat)
            continue
        names = sorted(
            n for n in os.listdir(d)
            if n.lower().endswith(".htm") and not n.endswith("_s.htm") and n.lower() != "index.htm"
        )
        mapping, used, dup = extract(cat, names)
        if valid is not None:
            dropped = 0
            for scheme, bucket in mapping.items():
                for key in [k for k, v in bucket.items() if v not in valid]:
                    del bucket[key]
                    dropped += 1
            if dropped:
                print("%-3s 丢弃 %d 条（页面未成功抽取）" % (cat, dropped))
        mapping = {k: v for k, v in mapping.items() if v}
        if not mapping:
            continue
        data[cat] = mapping
        total += sum(len(v) for v in mapping.values())
        print("%-3s 文件 %-5d 条目 %-5d 冲突 %-3d 方案 %s" % (
            cat, len(names), sum(len(v) for v in mapping.values()), dup,
            ",".join("%s:%d" % (k, len(v)) for k, v in mapping.items())))

    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    for out in OUTS:
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with gzip.open(out, "wb", compresslevel=9) as f:
            f.write(payload)
        print("写出", out, "%d 字节 → gz %d 字节" % (len(payload), os.path.getsize(out)))
    print("合计条目", total)


if __name__ == "__main__":
    main()
