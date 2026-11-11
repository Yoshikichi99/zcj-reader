# -*- coding: utf-8 -*-
"""抽取原站每个「小部」集的下拉菜单（Ext.menu 里的 go2("X.htm") 条目）。

输出：前端/proto/data/menu.json.gz 与 数据/package/menu.json.gz
结构：{"Kh": [["1.三歸依", "Kh/Kh1"], ...], ...}
"""
import gzip
import json
import os
import re

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(BASE, "源数据", "agama.buddhason.org_simp")
OUTS = [
    os.path.join(BASE, "前端", "proto", "data", "menu.json.gz"),
    os.path.join(BASE, "数据", "package", "menu.json.gz"),
]
PAT = re.compile(
    r"\{\s*text\s*:\s*['\"]([^'\"]{1,60})['\"]\s*,\s*handler\s*:\s*function\s*\(\s*\)\s*"
    r"\{\s*go2\s*\(\s*['\"]([^'\"]+\.htm)['\"]"
)


def read_text(path):
    for enc in ("utf-8", "big5", "cp950"):
        try:
            return open(path, "r", encoding=enc).read()
        except UnicodeDecodeError:
            continue
    return open(path, "r", encoding="utf-8", errors="replace").read()


def main():
    data = {}
    for cat in sorted(os.listdir(SRC)):
        d = os.path.join(SRC, cat)
        if not os.path.isdir(d):
            continue
        pages = {os.path.splitext(n)[0].lower()
                 for n in os.listdir(d) if n.lower().endswith(".htm") and not n.endswith("_s.htm")}
        items, seen = [], set()
        for n in sorted(os.listdir(d)):
            if not n.lower().endswith(".js"):
                continue
            t = read_text(os.path.join(d, n))
            for label, target in PAT.findall(t):
                base = os.path.splitext(os.path.basename(target))[0]
                if base.lower() == "index":        # 「首 頁」项，由页面导航承担
                    continue
                if base.lower() not in pages:      # 跨目录或不存在
                    continue
                pid = cat + "/" + base
                if pid in seen:
                    continue
                seen.add(pid)
                items.append([" ".join(label.split()), pid])
        if items:
            data[cat] = items
            print("%-3s 菜单 %-4d 条（页面 %d）" % (cat, len(items), len(pages)))

    if not data:
        print("未发现菜单")
        return
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    for out in OUTS:
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with gzip.open(out, "wb", compresslevel=9) as f:
            f.write(payload)
        print("写出", out, "%d → gz %d 字节" % (len(payload), os.path.getsize(out)))
    print("栏目数", len(data), "条目合计", sum(len(v) for v in data.values()))


if __name__ == "__main__":
    main()
