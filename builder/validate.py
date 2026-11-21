# -*- coding: utf-8 -*-
"""校验 150 道题的数据完整性、模板映射与代码语法。"""

import os
import sys
import importlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from manifest import MANIFEST  # noqa: E402
from templates_data import TEMPLATE_BY_ID  # noqa: E402

DATA = {}
for name in ["problems_a", "problems_b", "problems_c", "problems_d", "problems_e", "problems_f"]:
    try:
        mod = importlib.import_module(name)
        DATA.update(mod.DATA)
    except ModuleNotFoundError:
        print("[缺少模块] %s" % name)

errors = []
warnings = []

manifest_ids = [row[0] for row in MANIFEST]
if sorted(DATA) != sorted(manifest_ids):
    missing = sorted(set(manifest_ids) - set(DATA))
    extra = sorted(set(DATA) - set(manifest_ids))
    errors.append("id 不匹配：缺少 %s，多出 %s" % (missing, extra))

required = {"statement", "examples", "approach", "code", "time", "space", "pitfalls"}
tpl_refs = 0
var_lines = 0

for pid, cat, title, diff, slug, tpls in MANIFEST:
    d = DATA.get(pid)
    if not d:
        continue
    label = "%02d %s" % (pid, title)
    miss = required - set(d)
    if miss:
        errors.append("%s 缺字段 %s" % (label, sorted(miss)))
        continue
    for key in ("statement", "approach", "code", "time", "space"):
        if not isinstance(d[key], str) or not d[key].strip():
            errors.append("%s 字段 %s 为空" % (label, key))
    if not isinstance(d["pitfalls"], list) or len(d["pitfalls"]) < 2:
        warnings.append("%s pitfalls 少于 2 条" % label)
    if not isinstance(d["examples"], list) or not d["examples"]:
        errors.append("%s 缺少 examples" % label)
    if len(d["statement"]) < 20:
        warnings.append("%s statement 过短" % label)
    if len(d["approach"]) < 25:
        warnings.append("%s approach 过短" % label)
    if "```" in d["code"]:
        errors.append("%s code 含 markdown 围栏" % label)
    try:
        compile(d["code"], "<%s>" % slug, "exec")
    except SyntaxError as exc:
        errors.append("%s 代码语法错误：%s" % (label, exc))
    if d["code"].count("# 变化点") == 0:
        warnings.append("%s 没有标记变化点" % label)
    var_lines += d["code"].count("# 变化点")
    for tid in tpls:
        tpl_refs += 1
        if tid not in TEMPLATE_BY_ID:
            errors.append("%s 引用未知模板 %s" % (label, tid))
    if "List[" in d["code"] and "from typing import" not in d["code"]:
        warnings.append("%s 使用 List 但未导入 typing" % label)

print("题目 %d / 150，模板引用 %d 次，变化点 %d 处" % (len(DATA), tpl_refs, var_lines))
for w in warnings:
    print("[警告] " + w)
for e in errors:
    print("[错误] " + e)
print("校验通过" if not errors else "校验失败：%d 个错误" % len(errors))
sys.exit(0 if not errors else 1)
