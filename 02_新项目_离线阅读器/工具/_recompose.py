# -*- coding: utf-8 -*-
"""验证：北传页里嵌的南传文本，能否由「南传独立页」重组出来。"""
import os, io, sys, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract as E

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
recs = [json.loads(l) for l in io.open(os.path.join(BASE, "数据", "_pages.jsonl"), encoding="utf-8")]
by = {r["p"]: r for r in recs}

def nz(s):
    return re.sub(r"\s+", "", E.strip_tags(s))

def first_zh(r):
    for k, src, h in r["blk"]:
        if k == "zh":
            return h
    return ""

# 建立 SN / AN / MN / DN / MA / DA / AA 的 (编号) -> 页面id
index = {}
for r in recs:
    nm = r["nm"]
    cat = r["cat"]
    pid = r["p"][:-4]
    m = re.match(r"相應部(\d+)相應(\d+)經", nm)
    if m:
        index[("SN", int(m.group(1)), int(m.group(2)))] = pid
        continue
    m = re.match(r"增支部(\d+)集(\d+)經", nm)
    if m:
        index[("AN", int(m.group(1)), int(m.group(2)))] = pid
        continue
    m = re.match(r"中部(\d+)經", nm)
    if m:
        index[("MN", 0, int(m.group(1)))] = pid
        continue
    m = re.match(r"長部(\d+)經", nm)
    if m:
        index[("DN", 0, int(m.group(1)))] = pid
        continue
    m = re.match(r"中阿含(\d+)經", nm)
    if m:
        index[("MA", 0, int(m.group(1)))] = pid
        continue
    m = re.match(r"長阿含(\d+)經", nm)
    if m:
        index[("DA", 0, int(m.group(1)))] = pid
        continue
    m = re.match(r"增壹阿含(\d+)品(\d+)經", nm)
    if m:
        index[("AA", int(m.group(1)), int(m.group(2)))] = pid
        continue

print("索引条目", len(index))

def strip_ann(t):
    # 去掉 [SA.1] 这类标注、空行、品名行
    lines = [x for x in t.split("\n")]
    out = []
    for ln in lines:
        s = re.sub(r"\[[A-Z]{1,3}\.\d+(?:\.\d+)*\]", "", ln)
        if not s.strip():
            continue
        if re.match(r"^\s*\d+\.\S+品\s*$", s):
            continue
        out.append(s)
    return re.sub(r"\s+", "", "".join(out))

def parse_refs(s):
    refs = []
    for m in re.finditer(r"相應部(\d+)相應(\d+)(?:-(\d+))?經", s):
        a, b = int(m.group(1)), int(m.group(2))
        e = int(m.group(3)) if m.group(3) else b
        for k in range(b, e + 1):
            refs.append(("SN", a, k))
    for m in re.finditer(r"增支部(\d+)集(\d+)(?:-(\d+))?經", s):
        a, b = int(m.group(1)), int(m.group(2))
        e = int(m.group(3)) if m.group(3) else b
        for k in range(b, e + 1):
            refs.append(("AN", a, k))
    for m in re.finditer(r"中部(\d+)(?:-(\d+))?經", s):
        a = int(m.group(1))
        e = int(m.group(2)) if m.group(2) else a
        for k in range(a, e + 1):
            refs.append(("MN", 0, k))
    for m in re.finditer(r"長部(\d+)(?:-(\d+))?經", s):
        a = int(m.group(1))
        e = int(m.group(2)) if m.group(2) else a
        for k in range(a, e + 1):
            refs.append(("DN", 0, k))
    return refs

tested = 0
full = 0
partial = 0
missing_ref = 0
north = {"SA", "MA", "DA", "AA"}
for r in recs:
    if r["cat"] not in north or not r["s"]:
        continue
    nk = [b for b in r["blk"] if b[0] == "zh" and b[1] == "nikaya"]
    if not nk:
        continue
    emb = nz(nk[0][2])
    refs = parse_refs(r["s"])
    if not refs:
        continue
    tested += 1
    hit = 0
    for ref in refs:
        pid = index.get(ref)
        if not pid:
            missing_ref += 1
            continue
        rt = strip_ann(E.strip_tags(first_zh(by[pid + ".htm"])))
        rt = re.sub(r"^.*?\((?:莊春江譯|莊春江標點)\)", "", rt, count=1)
        # 去掉标题行：取正文第一个「　　」之后
        body = rt
        if body and body in emb:
            hit += 1
    if refs and hit == len(refs):
        full += 1
    elif hit:
        partial += 1

print("北传页(含南传块+南传引用) 测试数:", tested)
print("  引用的南传页面全部能在嵌入文本中找到:", full)
print("  部分找到:", partial)
print("  找不到的引用条数:", missing_ref)
