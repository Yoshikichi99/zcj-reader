# -*- coding: utf-8 -*-
"""测量正文重复率：同一段文字是否同时出现在「北传页」和「南传页」里。"""
import os, io, sys, json, re, hashlib, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract as E

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
recs = [json.loads(l) for l in io.open(os.path.join(BASE, "数据", "_pages.jsonl"), encoding="utf-8")]
recs = [r for r in recs if any(b[2].strip() for b in r["blk"])]

def norm(s):
    return re.sub(r"\s+", "", E.strip_tags(s))

items = []   # (page, kind, src, chars, hash)
for r in recs:
    for kind, src, h in r["blk"]:
        t = norm(h)
        if len(t) < 40:
            continue
        items.append((r["p"], r["cat"], kind, src, len(t), hashlib.sha1(t.encode()).hexdigest()))

total = sum(i[4] for i in items)
by_hash = collections.defaultdict(list)
for i in items:
    by_hash[i[5]].append(i)

dup_extra = 0
dup_groups = 0
examples = []
for h, lst in by_hash.items():
    if len(lst) > 1:
        dup_groups += 1
        dup_extra += sum(x[4] for x in lst) - max(x[4] for x in lst)
        if len(examples) < 12:
            examples.append(lst)

print("参与统计的块: %d, 总字数: %d (%.2f MB utf8)" % (len(items), total, total * 3 / 1048576))
print("重复组: %d, 可省字数: %d (%.1f%% 的总文本)" % (dup_groups, dup_extra, dup_extra / total * 100))
print("去重后字数: %d (%.2f MB utf8)" % (total - dup_extra, (total - dup_extra) * 3 / 1048576))
print()
print("重复样例：")
for lst in examples[:6]:
    print("  [%d 份] %s" % (len(lst), "  |  ".join("%s(%s/%s,%d字)" % (x[0], x[2] or "-", x[3] or "-", x[4]) for x in lst)))
print()

# 按「重复发生在哪些块类型之间」分类
pairs = collections.Counter()
for h, lst in by_hash.items():
    if len(lst) > 1:
        kinds = tuple(sorted(set((x[2] or "-") + ":" + (x[3] or "-") for x in lst)))
        pairs[kinds] += sum(x[4] for x in lst) - max(x[4] for x in lst)
for k, v in pairs.most_common(10):
    print("%-40s 可省 %d 字" % (str(k), v))
