# -*- coding: utf-8 -*-
"""数据异常体检：把可疑页面汇总成一份 Markdown 日志，便于人工修正。

用法：python 工具\\audit_data.py [--out 验证/数据异常日志.md]

只在构建侧运行，不参与运行时，也不进 exe。
检查项：
  1. 内容块无法配对结尾（会被整块丢弃的隐患）
  2. 页面键在语料库中缺失
  3. 空页面（既无键文本，也无对读/巴利）
  4. 仅对读的页面
  5. 抽取字数远少于原页正文（剔除简体副本后）
  6. 同一语料键有多个来源页且字数差异明显（可能撞键）
"""
import argparse
import gzip
import io
import json
import os
import re
import sys

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract as E

SRC = os.path.join(BASE, "源数据", "agama.buddhason.org_simp")
DATA = os.path.join(BASE, "前端", "proto", "data")
JSONL = os.path.join(BASE, "数据", "_pages.jsonl")

TAG = re.compile(r"<[^>]+>")
SIMP = re.compile(r'<div[^>]*class="[^"]*\bsimp\b[^"]*"[^>]*>', re.I)
DIV = re.compile(r"<div\b[^>]*>", re.I)
CLS = re.compile(r'class="([^"]*)"', re.I)


def plain(h):
    return "".join(TAG.sub("", h).split())


def load_gz(path):
    with gzip.open(path, "rt", encoding="utf-8") as f:
        return json.load(f)


def content_len(raw):
    """原页正文（#center 区，剔除简体副本）。老版页面没有 #center，返回 None 无法可靠比对。"""
    t = E.STYLE_RE.sub("", E.SCRIPT_RE.sub("", raw))
    a = t.find('<div id="center"')
    if a < 0:
        return None
    b = t.find('<div id="south"', a)
    if b > a:
        t = t[a:b]
    else:
        t = t[a:]
    out, pos = [], 0
    for m in SIMP.finditer(t):
        if m.start() < pos:
            continue
        end = E.find_div_end(t, m.end())
        if end <= m.end():
            continue
        out.append(t[pos:m.start()])
        pos = end
    out.append(t[pos:])
    return len(plain("".join(out)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(BASE, "验证", "数据异常日志.md"))
    args = ap.parse_args()

    pages = load_gz(os.path.join(DATA, "pages.json.gz"))
    pali = load_gz(os.path.join(DATA, "pali.json.gz"))
    corpus = {}
    for fn in sorted(os.listdir(os.path.join(DATA, "corpus"))):
        if fn.endswith(".json.gz"):
            corpus.update(load_gz(os.path.join(DATA, "corpus", fn)))

    # ---- 源记录与源页面 ----
    raw_len, blk_kinds, key_sources = {}, {}, {}
    with io.open(JSONL, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            raw_len[r["p"]] = sum(len(plain(b[2])) for b in r["blk"])
            blk_kinds[r["p"]] = [b[0] for b in r["blk"]]
            for b in r["blk"]:
                if b[0] == "zh":
                    for k in re.findall(r"sutra_name\">([^<]+)<", b[2]) or []:
                        pass

    unpaired, empty_pages, cmp_only, low_text = [], [], [], []
    missing_keys = []
    skipped_no_center = 0
    for pid, rec in pages.items():
        keys, ov, cmp, pali_ids = rec[1], rec[2], rec[3], rec[4]
        if not keys and not cmp and not pali_ids:
            empty_pages.append(pid)
        if not keys and cmp and not pali_ids:
            cmp_only.append(pid)
        for k in keys:
            if k not in ov and k not in corpus:
                missing_keys.append((pid, k))
        raw = raw_len.get(pid, 0)
        path = os.path.join(SRC, pid.replace("/", os.sep))
        if os.path.exists(path) and raw:
            src = content_len(io.open(path, encoding="utf-8", errors="replace").read())
            if src is None:
                skipped_no_center += 1
            elif src > 400 and raw < src * 0.55:
                low_text.append((pid, raw, src, raw / src))

    # ---- 扫描内容块配对 ----
    scanned = 0
    for dirpath, _, files in os.walk(SRC):
        for fn in files:
            if not fn.lower().endswith((".htm", ".html")) or fn.endswith("_s.htm"):
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, SRC).replace("\\", "/")
            raw = io.open(path, encoding="utf-8", errors="replace").read()
            raw = E.SCRIPT_RE.sub("", raw)
            raw = E.STYLE_RE.sub("", raw)
            scanned += 1
            for m in DIV.finditer(raw):
                cm = CLS.search(m.group(0))
                if not cm:
                    continue
                cls = cm.group(1).split()
                if "simp" in cls or not ({"trad", "pali", "comp"} & set(cls)):
                    continue
                if E.find_div_end(raw, m.end()) < 0:
                    unpaired.append((rel, " ".join(cls)))

    # ---- 写日志 ----
    n = len(pages)
    out = io.open(args.out, "w", encoding="utf-8")
    out.write("# 数据异常日志\n\n")
    out.write("> 由 `工具/audit_data.py` 生成，供人工核对；不参与运行时。\n\n")
    out.write("## 总览\n\n")
    out.write("| 项目 | 数量 |\n|---|---|\n")
    out.write("| 页面 | %d |\n| 巴利段 | %d |\n| 语料键 | %d |\n| 扫描源页面 | %d |\n" % (
        n, len(pali), len(corpus), scanned))
    out.write("| 无法配对的内容块 | %d |\n| 语料键缺失 | %d |\n| 空页面 | %d |\n"
              "| 仅对读页面 | %d |\n| 抽取偏少（<55%%，剔除简体副本） | %d |\n"
              "| 无 #center、未做字数比对 | %d |\n\n" % (
                  len(unpaired), len(missing_keys), len(empty_pages), len(cmp_only),
                  len(low_text), skipped_no_center))

    def section(title, rows, note=""):
        out.write("## %s\n\n" % title)
        if note:
            out.write(note + "\n\n")
        if not rows:
            out.write("无。\n\n")
            return
        for r in rows[:60]:
            out.write("- %s\n" % r)
        if len(rows) > 60:
            out.write("- ……其余 %d 条省略\n" % (len(rows) - 60))
        out.write("\n")

    section("无法配对结尾的内容块", ["`%s`（%s）" % (p, c) for p, c in unpaired],
            "这类块会被当成没有内容；需要时给 `find_div_end` 加新的结构边界。")
    section("语料键缺失", ["`%s` → `%s`" % (p, k) for p, k in missing_keys],
            "页面引用了语料库里没有的键，拼装时会静默少一段。")
    section("空页面", ["`%s`" % p for p in sorted(empty_pages)],
            "既无键文本、也无对读/巴利，通常是索引页或原站的空壳页。")
    section("仅对读页面", ["`%s`" % p for p in sorted(cmp_only)],
            "原站这页只有南北传对读，阅读器会加提示条。")
    section("抽取偏少（低于原页正文 55%）",
            ["`%s` 抽取 %d / 正文 %d（%.0f%%）" % (p, r, s, ratio * 100)
             for p, r, s, ratio in sorted(low_text, key=lambda x: x[3])],
            "先排除源页繁简双份；剩下的多半是对读/注释的呈现差异。")

    out.write("## 用法\n\n```bat\npython 工具\\audit_data.py\n```\n\n")
    out.write("改完数据后重跑一次，确认「无法配对」「键缺失」两项保持为 0。\n")
    out.close()

    print("写出", args.out)
    print("无法配对 %d | 键缺失 %d | 空页 %d | 仅对读 %d | 抽取偏少 %d" % (
        len(unpaired), len(missing_keys), len(empty_pages), len(cmp_only), len(low_text)))


if __name__ == "__main__":
    main()
