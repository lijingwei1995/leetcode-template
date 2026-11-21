#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把题库、模板与题解数据生成为一个静态站点（输出到 ../html）。"""

import os
import re
import sys
import html
import shutil
import importlib
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
OUT = os.path.join(PROJECT, "html")
sys.path.insert(0, HERE)

from manifest import MANIFEST, CATEGORIES          # noqa: E402
from templates_data import TEMPLATES, TEMPLATE_BY_ID, GROUPS  # noqa: E402

ORIGIN_NAME = "面试经典 150 题 - 学习计划 - 力扣（LeetCode）全球极客挚爱的技术成长平台.html"
ORIGIN_QUOTED = quote(ORIGIN_NAME)

# --------------------------------------------------------------------------
# 数据装载
# --------------------------------------------------------------------------
DATA = {}
MISSING_MODULES = []
for modname in ["problems_a", "problems_b", "problems_c", "problems_d", "problems_e", "problems_f"]:
    try:
        mod = importlib.import_module(modname)
        DATA.update(mod.DATA)
    except ModuleNotFoundError:
        MISSING_MODULES.append(modname)

PROBLEMS = []
missing = []
for pid, cat, title, diff, slug, tpls in MANIFEST:
    entry = DATA.get(pid)
    if not entry:
        missing.append(pid)
        continue
    p = dict(entry)
    p.update({"id": pid, "category": cat, "title": title, "difficulty": diff,
              "slug": slug, "templates": tpls,
              "url": "https://leetcode.cn/problems/%s/" % slug})
    PROBLEMS.append(p)

if missing:
    print("提示：%d 道题暂无数据，先生成部分站点：%s" % (len(missing), missing))

PROBLEM_BY_ID = {p["id"]: p for p in PROBLEMS}
PROBLEM_INDEX = {p["id"]: i for i, p in enumerate(PROBLEMS)}
DIFF_ORDER = {"简单": 0, "中等": 1, "困难": 2}

TPL_PROBLEMS = {t["id"]: [] for t in TEMPLATES}
for p in PROBLEMS:
    for tid in p["templates"]:
        if tid in TPL_PROBLEMS:
            TPL_PROBLEMS[tid].append(p)


# --------------------------------------------------------------------------
# 工具
# --------------------------------------------------------------------------
def esc(s):
    return html.escape(str(s), quote=False)


def diff_class(d):
    return {"简单": "easy", "中等": "medium", "困难": "hard"}.get(d, "medium")


def tpl_name(tid):
    return TEMPLATE_BY_ID[tid]["name"] if tid in TEMPLATE_BY_ID else tid


def origin_href(root):
    depth = root.count("../") + 1
    return ("../" * depth) + ORIGIN_QUOTED


KEYWORDS = {
    "def", "class", "return", "if", "else", "elif", "for", "while", "in", "not",
    "and", "or", "is", "None", "True", "False", "import", "from", "as", "with",
    "try", "except", "finally", "raise", "pass", "break", "continue", "lambda",
    "yield", "global", "nonlocal", "assert", "del", "async", "await",
}
BUILTINS = {
    "len", "range", "enumerate", "zip", "min", "max", "sum", "abs", "sorted",
    "list", "dict", "set", "tuple", "int", "str", "bool", "float", "print",
    "deque", "defaultdict", "Counter", "heappush", "heappop", "heapify",
    "heapreplace", "inf", "reversed", "any", "all", "map", "filter",
}

TOKEN_RE = re.compile(
    r'(?P<str>"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')'
    r'|(?P<cmt>#[^\n]*)'
    r'|(?P<num>\b\d+(?:\.\d+)?\b)'
    r'|(?P<kw>\b(?:' + "|".join(sorted(KEYWORDS, key=len, reverse=True)) + r')\b)'
    r'|(?P<bi>\b(?:' + "|".join(sorted(BUILTINS, key=len, reverse=True)) + r')\b)'
    r'|(?P<fn>\b[A-Za-z_]\w*(?=\())'
)


def highlight(line):
    out, pos = [], 0
    for m in TOKEN_RE.finditer(line):
        if m.start() > pos:
            out.append(esc(line[pos:m.start()]))
        out.append('<span class="tok-%s">%s</span>' % (m.lastgroup, esc(m.group())))
        pos = m.end()
    out.append(esc(line[pos:]))
    return "".join(out)


def render_code(code):
    lines = code.strip("\n").split("\n")
    rows = []
    for i, line in enumerate(lines, 1):
        hl = " hl" if "# 变化点" in line else ""
        body = highlight(line) if line.strip() else "&nbsp;"
        rows.append('<span class="cl%s"><span class="ln">%d</span><span class="lt">%s</span></span>'
                    % (hl, i, body))
    return '<pre class="code-body">%s</pre>' % "".join(rows)


def variations_of(code):
    notes = []
    for i, line in enumerate(code.strip("\n").split("\n"), 1):
        if "# 变化点" in line:
            note = line.split("# 变化点", 1)[1].lstrip("：: ").strip()
            notes.append((i, note or "本题相对模板的调整"))
    return notes


def tpl_chip(tid, root):
    if tid not in TEMPLATE_BY_ID:
        return ""
    return '<a class="chip chip-tpl" href="%stemplates/%s.html">%s</a>' % (root, tid, esc(tpl_name(tid)))


def diff_pill(d):
    return '<span class="pill pill-%s">%s</span>' % (diff_class(d), esc(d))


def pager(p):
    idx = PROBLEM_INDEX[p["id"]]
    prev_p = PROBLEMS[idx - 1] if idx > 0 else None
    next_p = PROBLEMS[idx + 1] if idx + 1 < len(PROBLEMS) else None
    out = ['<div class="pager">']
    if prev_p:
        out.append('<a class="pager-link prev" href="%s.html"><span>上一题</span><strong>%s</strong></a>'
                   % (prev_p["slug"], esc(prev_p["title"])))
    else:
        out.append('<span class="pager-link disabled"></span>')
    if next_p:
        out.append('<a class="pager-link next" href="%s.html"><span>下一题</span><strong>%s</strong></a>'
                   % (next_p["slug"], esc(next_p["title"])))
    else:
        out.append('<span class="pager-link disabled"></span>')
    out.append("</div>")
    return "".join(out)


# --------------------------------------------------------------------------
# 页面骨架
# --------------------------------------------------------------------------
def layout(title, root, body, active="", desc="用模板解一类题，而不是一题一解。"):
    nav = []
    for key, label, href in [("index", "题库导航", "index.html"),
                             ("templates", "模板手册", "templates.html")]:
        cls = "nav-link active" if key == active else "nav-link"
        nav.append('<a class="%s" href="%s%s">%s</a>' % (cls, root, href, label))
    nav_html = "".join(nav)
    return """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="icon" href="data:image/svg+xml,%%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%%3E%%3Crect width='32' height='32' rx='7' fill='%%231b1f1d'/%%3E%%3Cpath d='M9 9h14M16 9v14' stroke='%%23f0ead9' stroke-width='3' stroke-linecap='round'/%%3E%%3C/svg%%3E">
<link rel="stylesheet" href="%sassets/style.css">
</head>
<body>
<header class="topbar">
  <div class="topbar-inner">
    <a class="brand" href="%sindex.html" aria-label="LeetCode 模板手册">
      <span class="brand-mark"><i></i><i></i><i></i><i></i></span>
      <span class="brand-text">模板<span class="dot">·</span>LEETCODE</span>
    </a>
    <nav class="nav">%s
      <a class="nav-link nav-ext" href="%s" target="_blank" rel="noopener">原题计划 <span class="up">↗</span></a>
    </nav>
  </div>
</header>
%s
<footer class="footer">
  <div class="footer-inner">
    <p class="footer-brand">模板 · LEETCODE</p>
    <p>基于《面试经典 150 题》整理 · 代码以 Python 3 书写 · 静态站点，可离线阅读</p>
  </div>
</footer>
<script src="%sassets/app.js"></script>
</body>
</html>
""" % (esc(title), esc(desc), root, root, nav_html, origin_href(root), body, root)


# --------------------------------------------------------------------------
# 导航页
# --------------------------------------------------------------------------
def page_index():
    by_cat = {c: [p for p in PROBLEMS if p["category"] == c] for c in CATEGORIES}
    total_vars = sum(len(variations_of(p["code"])) for p in PROBLEMS)
    root = ""

    cells = []
    for p in PROBLEMS:
        cells.append('<a class="cell %s" href="problems/%s.html" title="%02d %s · %s"></a>'
                     % (diff_class(p["difficulty"]), p["slug"], p["id"], esc(p["title"]), esc(p["difficulty"])))

    jump = []
    for i, c in enumerate(CATEGORIES, 1):
        jump.append('<a class="jump" href="#cat-%02d">%s<span>%d</span></a>' % (i, esc(c), len(by_cat[c])))

    tpl_options = "".join('<option value="%s">%s</option>' % (t["id"], esc(t["name"])) for t in TEMPLATES)

    sections = []
    for ci, c in enumerate(CATEGORIES, 1):
        rows = []
        for p in by_cat[c]:
            tpl_tags = ('<span class="chip chip-cat">%s</span>' % esc(p["category"])) + \
                       "".join(tpl_chip(t, root) for t in p["templates"][:2])
            if len(p["templates"]) > 2:
                tpl_tags += '<span class="chip chip-more">+%d</span>' % (len(p["templates"]) - 2)
            rows.append(
                '<div class="problem-row" data-diff="%s" data-tpl="%s" data-search="%02d %s %s %s %s">'
                '<a class="row-main" href="problems/%s.html">'
                '<span class="p-num">%02d</span>'
                '<span class="p-body"><span class="p-title">%s</span><span class="p-tags">%s</span></span>'
                '<span class="p-meta">%s</span>'
                '<span class="p-arrow">→</span>'
                '</a>'
                '<a class="row-ext" href="%s" target="_blank" rel="noopener" title="在 LeetCode 打开原题">↗</a>'
                '</div>' % (
                    diff_class(p["difficulty"]), " ".join(p["templates"]),
                    p["id"], esc(p["title"]), esc(p["category"]), " ".join(tpl_name(t) for t in p["templates"]),
                    p["slug"], p["slug"], p["id"], esc(p["title"]), tpl_tags,
                    diff_pill(p["difficulty"]), p["url"])
            )
        sections.append(
            '<section class="category" id="cat-%02d">'
            '<div class="cat-head"><div class="cat-title"><span class="cat-index">%02d</span><h2>%s</h2></div>'
            '<span class="cat-count">%d 题</span></div>'
            '<div class="problem-list">%s</div>'
            '</section>' % (ci, ci, esc(c), len(by_cat[c]), "".join(rows)))

    body = """
<main>
  <section class="hero">
    <div class="container hero-inner">
      <div class="hero-copy">
        <p class="eyebrow">LEETCODE · 面试经典 150 题</p>
        <h1>用模板，<br>解一类题。</h1>
        <p class="lede">把《面试经典 150 题》压缩成 35 个可复用的套路。每道题标注所用模板、变化点与可直接运行的 Python 代码。</p>
        <div class="hero-stats">
          <div><strong>%d</strong><span>道题</span></div>
          <div><strong>%d</strong><span>个分类</span></div>
          <div><strong>%d</strong><span>个模板</span></div>
          <div><strong>%d</strong><span>处变化点</span></div>
        </div>
        <div class="hero-actions">
          <a class="btn btn-primary" href="#catalog">开始浏览 <span>↓</span></a>
          <a class="btn btn-ghost" href="templates.html">模板手册</a>
          <button class="btn btn-ghost" id="randomBtn" type="button">随机一题</button>
        </div>
      </div>
      <div class="hero-map">
        <div class="map-head"><span>题号一览</span><span>点击任意格 →</span></div>
        <div class="cell-grid">%s</div>
        <div class="map-legend">
          <span><i class="lg easy"></i>简单</span>
          <span><i class="lg medium"></i>中等</span>
          <span><i class="lg hard"></i>困难</span>
        </div>
      </div>
    </div>
  </section>

  <section class="container toolbar-wrap" id="catalog-top">
    <div class="toolbar">
      <label class="search">
        <span class="search-icon"></span>
        <input id="search" type="search" placeholder="搜索题目、分类或模板… 按 / 聚焦" autocomplete="off">
      </label>
      <div class="diff-filter" role="group" aria-label="按难度筛选">
        <button class="fchip active" data-diff-filter="all" type="button">全部</button>
        <button class="fchip" data-diff-filter="easy" type="button">简单</button>
        <button class="fchip" data-diff-filter="medium" type="button">中等</button>
        <button class="fchip" data-diff-filter="hard" type="button">困难</button>
      </div>
      <label class="select-wrap">
        <select id="tplFilter">
          <option value="all">全部模板</option>
          %s
        </select>
      </label>
      <span class="result-count" id="resultCount">%d / %d 题</span>
    </div>
    <div class="cat-jump">%s</div>
  </section>

  <div class="container catalog" id="catalog">
    %s
  </div>
  <div class="container empty-state" id="emptyState" hidden>
    <p class="empty-title">没有匹配的题目</p>
    <p>换个关键词，或把筛选条件改回“全部”。</p>
  </div>
</main>
<script>
  window.PROBLEM_LINKS = %s;
  document.getElementById('randomBtn').addEventListener('click', function () {
    var links = window.PROBLEM_LINKS;
    location.href = links[Math.floor(Math.random() * links.length)];
  });
</script>
""" % (len(PROBLEMS), len(CATEGORIES), len(TEMPLATES), total_vars,
       "".join(cells), tpl_options, len(PROBLEMS), len(PROBLEMS),
       "".join(jump), "".join(sections),
       "[" + ",".join('"problems/%s.html"' % p["slug"] for p in PROBLEMS) + "]")
    return layout("LeetCode 模板手册 · 题库导航", "", body, "index")


# --------------------------------------------------------------------------
# 模板索引页
# --------------------------------------------------------------------------
def page_templates_index():
    root = ""
    total_links = sum(len(TPL_PROBLEMS[t["id"]]) for t in TEMPLATES)
    sections = []
    for gi, group in enumerate(GROUPS, 1):
        tpls = [t for t in TEMPLATES if t["group"] == group]
        cards = []
        for t in tpls:
            ps = TPL_PROBLEMS[t["id"]]
            primary = [p for p in ps if p["templates"][0] == t["id"]]
            mini = "、".join(p["title"] for p in (primary or ps)[:3])
            cards.append(
                '<a class="tpl-card" href="templates/%s.html">'
                '<div class="tpl-card-top"><span class="tpl-no">%02d</span><span class="tpl-count">%d 题</span></div>'
                '<h3>%s</h3><p>%s</p>'
                '<div class="tpl-mini">%s</div>'
                '<div class="tpl-card-foot"><span>%s</span><span class="arrow">→</span></div>'
                '</a>' % (t["id"], TEMPLATES.index(t) + 1, len(ps), esc(t["name"]),
                          esc(t["tagline"]), esc(mini), esc(t["complexity"])))
        sections.append(
            '<section class="tpl-group">'
            '<div class="tpl-group-head"><span class="cat-index">%02d</span><h2>%s</h2><span class="cat-count">%d 个模板</span></div>'
            '<div class="tpl-grid">%s</div></section>' % (gi, esc(group), len(tpls), "".join(cards)))

    body = """
<main>
  <section class="page-hero container">
    <p class="eyebrow">TEMPLATE LIBRARY</p>
    <h1 class="hero-title-lg">35 个模板，<br>覆盖 %d 道题。</h1>
    <p class="lede">模板不是答案，而是识别题型的框架。先看“什么时候用”，再看骨架代码和变化点，最后到具体题目里对照。</p>
    <div class="hero-stats">
      <div><strong>%d</strong><span>个模板</span></div>
      <div><strong>%d</strong><span>次题目关联</span></div>
      <div><strong>%d</strong><span>个分类</span></div>
    </div>
  </section>
  <div class="container tpl-groups">%s</div>
</main>
""" % (len(TEMPLATES), len(PROBLEMS), total_links, len(CATEGORIES), "".join(sections))
    return layout("模板手册 · LeetCode 模板手册", root, body, "templates")


# --------------------------------------------------------------------------
# 模板详情页
# --------------------------------------------------------------------------
def page_template(t):
    root = "../"
    tid = t["id"]
    ps = TPL_PROBLEMS[tid]
    primary = [p for p in ps if p["templates"][0] == tid]
    secondary = [p for p in ps if p["templates"][0] != tid]

    signals = "".join('<li><span>%02d</span>%s</li>' % (i, esc(s)) for i, s in enumerate(t["signals"], 1))
    variations = "".join('<li><span class="v-dot"></span><p>%s</p></li>' % esc(v) for v in t["variations"])
    var_notes = variations_of(t["skeleton"])

    same_group = [x for x in TEMPLATES if x["group"] == t["group"] and x["id"] != tid]
    same_links = "".join('<a class="rail-link" href="%s.html"><span>%s</span><i>→</i></a>'
                         % (x["id"], esc(x["name"])) for x in same_group)

    def prob_rows(items):
        out = []
        for p in items:
            role = "主模板" if p["templates"][0] == tid else "相关"
            out.append('<a class="mini-row" href="../problems/%s.html">'
                       '<span class="mini-no">%02d</span><span class="mini-title">%s</span>'
                       '%s<span class="mini-role">%s</span></a>'
                       % (p["slug"], p["id"], esc(p["title"]), diff_pill(p["difficulty"]), role))
        return "".join(out)

    body = """
<main>
  <div class="container crumbs"><a href="../templates.html">模板手册</a><span>/</span>%s<span>/</span><span>%s</span></div>
  <header class="container page-head tpl-head">
    <p class="page-kicker">%s · TEMPLATE</p>
    <h1>%s</h1>
    <p class="lede">%s</p>
    <div class="meta-row">
      <span class="pill pill-plain">%d 道题</span>
      <span class="pill pill-plain">%s</span>
    </div>
  </header>

  <div class="container tpl-layout">
    <article class="prose">
      <section>
        <h2>核心思路</h2>
        <p class="lead-p">%s</p>
        <div class="callout"><span class="callout-mark">!</span><p>%s</p></div>
      </section>

      <section>
        <h2>识别信号</h2>
        <p>看到下面这些特征，优先想到这个模板；如果同时符合多个模板，再看哪一条约束最紧。</p>
        <ol class="signal-list">%s</ol>
      </section>

      <section>
        <h2>模板骨架</h2>
        <div class="code-card">
          <div class="code-head"><span class="code-dots"><i></i><i></i><i></i></span><span class="code-lang">Python 3</span><button class="copy-btn" data-copy type="button">复制代码</button></div>
          %s
        </div>
        <p class="code-note">高亮行是应用时需要替换或调整的地方，下面逐条说明。</p>
      </section>

      <section>
        <h2>变化点</h2>
        <ul class="var-list">%s</ul>
      </section>

      <section>
        <h2>适用题目</h2>
        <div class="role-block"><span class="role-label">主模板 · %d 题</span><div class="mini-list">%s</div></div>
        %s
      </section>

      <section>
        <h2>参考</h2>
        <p class="ref-line">%s</p>
      </section>
    </article>

    <aside class="rail">
      <div class="rail-card">
        <h3>模板信息</h3>
        <dl class="rail-dl">
          <div><dt>分组</dt><dd>%s</dd></div>
          <div><dt>复杂度</dt><dd>%s</dd></div>
          <div><dt>主模板</dt><dd>%d 题</dd></div>
          <div><dt>相关引用</dt><dd>%d 题</dd></div>
        </dl>
      </div>
      <div class="rail-card">
        <h3>同组模板</h3>
        %s
      </div>
      <div class="rail-card">
        <h3>快速跳转</h3>
        <a class="rail-link" href="../templates.html"><span>全部模板</span><i>→</i></a>
        <a class="rail-link" href="../index.html"><span>题库导航</span><i>→</i></a>
      </div>
    </aside>
  </div>
</main>
""" % (esc(t["group"]), esc(t["name"]), esc(t["group"]), esc(t["name"]), esc(t["tagline"]),
       len(ps), esc(t["complexity"]), esc(t["idea"]),
       "本模板在题库中关联 %d 道题，其中 %d 道以它为主模板。先判断题型，再动手写代码。" % (len(ps), len(primary)),
       signals, render_code(t["skeleton"]), variations, len(primary), prob_rows(primary),
       ('<div class="role-block"><span class="role-label">作为相关模板 · %d 题</span><div class="mini-list">%s</div></div>'
        % (len(secondary), prob_rows(secondary))) if secondary else "",
       esc(t["ref"]), esc(t["group"]), esc(t["complexity"]), len(primary), len(secondary), same_links)
    return layout("%s · 模板 · LeetCode 模板手册" % t["name"], root, body, "templates",
                  t["tagline"])


# --------------------------------------------------------------------------
# 题目详情页
# --------------------------------------------------------------------------
def page_problem(p):
    root = "../"
    notes = variations_of(p["code"])
    examples = []
    for i, ex in enumerate(p.get("examples", []), 1):
        examples.append(
            '<div class="example"><div class="ex-head">示例 %d</div>'
            '<div class="ex-row"><span>输入</span><code>%s</code></div>'
            '<div class="ex-row"><span>输出</span><code>%s</code></div></div>'
            % (i, esc(ex.get("input", "")), esc(ex.get("output", ""))))
    pitfalls = "".join('<li><span>%02d</span><p>%s</p></li>' % (i, esc(x))
                       for i, x in enumerate(p.get("pitfalls", []), 1))

    related_tpls = "".join(
        '<a class="tpl-block" href="../templates/%s.html">'
        '<span class="tpl-block-role">%s</span><strong>%s</strong><span class="arrow">→</span></a>'
        % (tid, "主模板" if i == 0 else "相关模板", esc(tpl_name(tid)))
        for i, tid in enumerate(p["templates"]) if tid in TEMPLATE_BY_ID)

    primary_tid = p["templates"][0]
    siblings = [x for x in PROBLEMS if x["id"] != p["id"] and primary_tid in x["templates"]][:5]
    sibling_html = "".join('<a class="rail-link" href="%s.html"><span>%02d %s</span><i>→</i></a>'
                           % (x["slug"], x["id"], esc(x["title"])) for x in siblings)

    note_html = "".join('<li><span class="v-line">L%d</span><p>%s</p></li>' % (n, esc(txt))
                        for n, txt in notes)
    if not note_html:
        note_html = '<li><span class="v-line">—</span><p>本题基本是模板的直接应用，没有额外的结构性变化。</p></li>'

    toc = [("statement", "题目"), ("idea", "思路"), ("code", "模板解法"),
           ("pitfalls", "易错点"), ("complexity", "复杂度")]
    toc_html = "".join('<a href="#%s">%s</a>' % (k, v) for k, v in toc)

    body = """
<main>
  <div class="container crumbs"><a href="../index.html">题库导航</a><span>/</span>%s<span>/</span><span>%s</span></div>

  <header class="container page-head">
    <p class="page-kicker">No.%02d · %s</p>
    <h1>%s</h1>
    <div class="meta-row">
      %s
      <a class="meta-link" href="%s" target="_blank" rel="noopener">LeetCode 原题 <span class="up">↗</span></a>
    </div>
    <div class="tpl-row">%s</div>
  </header>

  <div class="container problem-layout">
    <article class="prose">
      <section id="statement">
        <h2>题目</h2>
        <p class="statement-p">%s</p>
        <div class="examples">%s</div>
      </section>

      <section id="idea">
        <h2>思路</h2>
        <p class="lead-p">%s</p>
        <div class="path-line">
          <span class="path-step">识别信号</span><i>→</i>
          <span class="path-step">套用模板</span><i>→</i>
          <span class="path-step">调整变化点</span>
        </div>
      </section>

      <section id="code">
        <h2>模板解法</h2>
        <div class="code-card">
          <div class="code-head"><span class="code-dots"><i></i><i></i><i></i></span><span class="code-lang">Python 3</span><button class="copy-btn" data-copy type="button">复制代码</button></div>
          %s
        </div>
        <h3 class="sub-h">变化点代码</h3>
        <ul class="var-list">%s</ul>
      </section>

      <section id="pitfalls">
        <h2>易错点</h2>
        <ul class="pitfall-list">%s</ul>
      </section>

      <section id="complexity">
        <h2>复杂度</h2>
        <div class="complexity-grid">
          <div><span>时间复杂度</span><strong>%s</strong></div>
          <div><span>空间复杂度</span><strong>%s</strong></div>
        </div>
      </section>

      %s
    </article>

    <aside class="rail">
      <div class="rail-card">
        <h3>本页目录</h3>
        <div class="toc">%s</div>
      </div>
      <div class="rail-card">
        <h3>本题模板</h3>
        %s
      </div>
      <div class="rail-card">
        <h3>同模板题目</h3>
        %s
      </div>
    </aside>
  </div>
</main>
""" % (esc(p["category"]), esc(p["title"]), p["id"], esc(p["category"]), esc(p["title"]),
       diff_pill(p["difficulty"]), p["url"], related_tpls, esc(p.get("statement", "")),
       "".join(examples), esc(p.get("approach", "")), render_code(p["code"]), note_html,
       pitfalls, esc(p.get("time", "—")), esc(p.get("space", "—")), pager(p), toc_html,
       related_tpls, sibling_html)
    return layout("%s · LeetCode 模板手册" % p["title"], root, body, "index",
                  p.get("statement", ""))


# --------------------------------------------------------------------------
# 资源
# --------------------------------------------------------------------------
CSS = r"""
:root{
  --paper:#f6f3ec;
  --paper-2:#fffdf8;
  --ink:#191d1b;
  --ink-soft:#3c433f;
  --muted:#767c74;
  --line:#ded8c9;
  --line-soft:#ece7da;
  --accent:#b84a24;
  --accent-2:#d9774f;
  --green:#1f5c45;
  --green-soft:#e3efe9;
  --amber:#956716;
  --amber-soft:#f6ecd6;
  --red:#a63a34;
  --red-soft:#f7e3df;
  --code-bg:#151a18;
  --code-line:#202723;
  --code-text:#e9e5d9;
  --serif:"Iowan Old Style","Palatino Linotype","Book Antiqua","Songti SC","Noto Serif CJK SC",serif;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
  --mono:"JetBrains Mono","SFMono-Regular",Consolas,"Liberation Mono",monospace;
  --shadow:0 1px 2px rgba(25,29,27,.04),0 12px 32px rgba(25,29,27,.05);
  --radius:14px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:92px}
body{
  margin:0;background:var(--paper);color:var(--ink);
  font-family:var(--sans);font-size:15.5px;line-height:1.75;
  -webkit-font-smoothing:antialiased;
  background-image:radial-gradient(rgba(25,29,27,.045) .7px,transparent .7px);
  background-size:22px 22px;
}
a{color:inherit;text-decoration:none}
p{margin:0 0 1em}
h1,h2,h3{font-family:var(--serif);font-weight:600;letter-spacing:-.01em;margin:0}
.container{width:min(1180px,calc(100% - 64px));margin:0 auto}
::selection{background:rgba(184,74,36,.18)}

/* ---------- topbar ---------- */
.topbar{
  position:sticky;top:0;z-index:50;
  background:rgba(246,243,236,.9);backdrop-filter:blur(14px);
  border-bottom:1px solid var(--line);
}
.topbar-inner{
  width:min(1180px,calc(100% - 64px));margin:0 auto;height:66px;
  display:flex;align-items:center;justify-content:space-between;gap:24px;
}
.brand{display:flex;align-items:center;gap:11px}
.brand-mark{
  width:22px;height:22px;display:grid;grid-template-columns:1fr 1fr;gap:3px;
  transform:rotate(-8deg);transition:transform .4s ease;
}
.brand:hover .brand-mark{transform:rotate(0)}
.brand-mark i{display:block;background:var(--ink);border-radius:2px}
.brand-mark i:nth-child(2){background:var(--accent)}
.brand-mark i:nth-child(3){background:var(--accent)}
.brand-mark i:nth-child(4){background:var(--ink);opacity:.35}
.brand-text{font-size:12.5px;font-weight:700;letter-spacing:.16em}
.brand-text .dot{color:var(--accent);margin:0 2px}
.nav{display:flex;align-items:center;gap:6px}
.nav-link{
  font-size:13.5px;color:var(--ink-soft);padding:7px 13px;border-radius:999px;
  transition:background .2s,color .2s;
}
.nav-link:hover{background:rgba(25,29,27,.06)}
.nav-link.active{background:var(--ink);color:var(--paper-2)}
.nav-ext{margin-left:8px;color:var(--muted);font-size:12.5px}
.up{font-size:11px}

/* ---------- hero ---------- */
.hero{padding:78px 0 54px;border-bottom:1px solid var(--line)}
.hero-inner{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(340px,.85fr);gap:64px;align-items:center}
.eyebrow{
  font-size:11.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--accent);
  font-weight:700;margin-bottom:18px;
}
.hero h1{
  font-size:clamp(46px,6vw,76px);line-height:1.08;letter-spacing:-.035em;margin-bottom:24px;
}
.hero h1::after{content:"";display:block;width:74px;height:4px;background:var(--accent);margin-top:22px;border-radius:2px}
.lede{font-size:16px;color:var(--ink-soft);max-width:560px;line-height:1.8}
.hero-stats{display:flex;gap:0;margin:32px 0 30px;flex-wrap:wrap}
.hero-stats>div{padding:0 24px;border-left:1px solid var(--line)}
.hero-stats>div:first-child{padding-left:0;border-left:0}
.hero-stats strong{display:block;font-family:var(--serif);font-size:30px;line-height:1.1;letter-spacing:-.02em}
.hero-stats span{font-size:11.5px;color:var(--muted);letter-spacing:.05em}
.hero-actions{display:flex;gap:10px;flex-wrap:wrap}
.btn{
  display:inline-flex;align-items:center;gap:9px;border:1px solid transparent;
  padding:11px 20px;border-radius:999px;font-size:13.5px;font-weight:600;
  cursor:pointer;font-family:var(--sans);transition:transform .18s ease,background .2s,box-shadow .2s;
}
.btn:hover{transform:translateY(-1px)}
.btn-primary{background:var(--ink);color:var(--paper-2);box-shadow:0 8px 20px rgba(25,29,27,.16)}
.btn-primary:hover{background:#000}
.btn-ghost{background:transparent;border-color:var(--line);color:var(--ink-soft)}
.btn-ghost:hover{background:var(--paper-2);border-color:#c9c2b2}

.hero-map{
  background:var(--paper-2);border:1px solid var(--line);border-radius:18px;
  padding:20px 22px 18px;box-shadow:var(--shadow);
}
.map-head{display:flex;justify-content:space-between;font-size:10.5px;letter-spacing:.14em;color:var(--muted);margin-bottom:14px}
.cell-grid{display:grid;grid-template-columns:repeat(15,1fr);gap:4px}
.cell{
  aspect-ratio:1;border-radius:2px;display:block;
  transition:transform .15s ease,box-shadow .15s ease;position:relative;
}
.cell.easy{background:#bcd2c5}
.cell.medium{background:#e3c58c}
.cell.hard{background:#d79a8d}
.cell:hover{transform:scale(1.45);box-shadow:0 0 0 2px var(--paper-2),0 4px 10px rgba(0,0,0,.18);z-index:2}
.map-legend{display:flex;gap:18px;margin-top:16px;font-size:11px;color:var(--muted)}
.map-legend span{display:flex;align-items:center;gap:6px}
.lg{width:8px;height:8px;border-radius:2px;display:inline-block}
.lg.easy{background:#bcd2c5}.lg.medium{background:#e3c58c}.lg.hard{background:#d79a8d}

/* ---------- toolbar ---------- */
.toolbar-wrap{padding-top:26px}
.toolbar{
  display:flex;align-items:center;gap:14px;flex-wrap:wrap;
  background:var(--paper-2);border:1px solid var(--line);border-radius:var(--radius);
  padding:12px 14px;box-shadow:var(--shadow);
}
.search{flex:1 1 320px;display:flex;align-items:center;gap:10px;padding:0 8px;min-width:220px}
.search-icon{
  width:15px;height:15px;border:2px solid var(--muted);border-radius:50%;
  position:relative;flex:0 0 auto;
}
.search-icon::after{content:"";position:absolute;width:7px;height:2px;background:var(--muted);transform:rotate(45deg);right:-5px;bottom:-1px;border-radius:2px}
.search input{
  flex:1;border:0;background:transparent;outline:none;font-size:14px;color:var(--ink);
  font-family:var(--sans);min-width:0;
}
.search input::placeholder{color:#9a9e96}
.diff-filter{display:flex;gap:4px;padding:3px;background:rgba(25,29,27,.045);border-radius:999px}
.fchip{
  border:0;background:transparent;padding:6px 13px;border-radius:999px;font-size:12.5px;
  color:var(--muted);cursor:pointer;font-family:var(--sans);transition:background .18s,color .18s;
}
.fchip:hover{color:var(--ink)}
.fchip.active{background:var(--paper-2);color:var(--ink);box-shadow:0 1px 3px rgba(0,0,0,.08);font-weight:600}
.select-wrap{position:relative}
.select-wrap select{
  appearance:none;border:1px solid var(--line);background:var(--paper);color:var(--ink-soft);
  font-family:var(--sans);font-size:12.5px;padding:8px 32px 8px 12px;border-radius:8px;cursor:pointer;outline:none;
}
.select-wrap::after{content:"▾";position:absolute;right:11px;top:50%;transform:translateY(-50%);pointer-events:none;font-size:10px;color:var(--muted)}
.result-count{font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums;margin-left:auto;padding-right:6px}
.cat-jump{display:flex;flex-wrap:wrap;gap:7px;margin:16px 0 8px}
.jump{
  font-size:11.5px;color:var(--ink-soft);border:1px solid var(--line);background:rgba(255,253,248,.5);
  padding:5px 10px;border-radius:999px;transition:all .18s;
}
.jump span{color:var(--muted);margin-left:5px;font-variant-numeric:tabular-nums}
.jump:hover{border-color:var(--accent);color:var(--accent)}

/* ---------- catalog ---------- */
.catalog{padding:22px 0 80px}
.category{display:grid;grid-template-columns:230px minmax(0,1fr);gap:40px;padding:34px 0;border-top:1px solid var(--line)}
.category:first-child{border-top:0}
.cat-head{position:sticky;top:88px;align-self:start;padding-top:6px}
.cat-title{display:flex;align-items:baseline;gap:12px}
.cat-index{font-family:var(--mono);font-size:11px;color:var(--accent);letter-spacing:.08em}
.cat-head h2{font-size:23px;letter-spacing:-.01em}
.cat-count{font-size:11.5px;color:var(--muted);display:block;margin-top:8px;padding-left:0}
.problem-list{min-width:0}
.problem-row{position:relative;border-bottom:1px solid var(--line-soft);transition:background .18s}
.problem-row:first-child{border-top:1px solid var(--line-soft)}
.problem-row:hover{background:rgba(255,253,248,.72)}
.problem-row[hidden],.category[hidden],.empty-state[hidden]{display:none}
.row-main{display:grid;grid-template-columns:44px minmax(0,1fr) auto 22px;align-items:center;gap:14px;padding:14px 42px 14px 10px}
.p-num{font-family:var(--mono);font-size:11.5px;color:#a2a69d;font-variant-numeric:tabular-nums}
.p-body{min-width:0;display:flex;flex-direction:column;gap:5px}
.p-title{font-size:15.5px;font-weight:600;letter-spacing:.005em;transition:color .18s}
.problem-row:hover .p-title{color:var(--accent)}
.p-tags{display:flex;flex-wrap:wrap;gap:5px}
.chip{
  font-size:10.5px;line-height:1.6;padding:1px 8px;border-radius:999px;
  border:1px solid var(--line);color:var(--muted);white-space:nowrap;background:rgba(255,253,248,.6);
  transition:all .18s;
}
.chip-tpl:hover{border-color:var(--accent);color:var(--accent);background:#fff}
.chip-cat{border-color:transparent;background:rgba(25,29,27,.045);color:#8b9088}
.chip-more{color:#a2a69d}
.p-meta{display:flex;align-items:center}
.pill{display:inline-block;font-size:10.5px;line-height:1.7;padding:1px 9px;border-radius:999px;font-weight:600;white-space:nowrap}
.pill-easy{color:var(--green);background:var(--green-soft)}
.pill-medium{color:var(--amber);background:var(--amber-soft)}
.pill-hard{color:var(--red);background:var(--red-soft)}
.pill-plain{color:var(--ink-soft);background:rgba(25,29,27,.05);font-weight:500}
.p-arrow{color:#b5b8b0;font-size:14px;transition:transform .18s,color .18s;justify-self:end}
.problem-row:hover .p-arrow{transform:translateX(4px);color:var(--accent)}
.row-ext{
  position:absolute;right:8px;top:50%;transform:translateY(-50%);
  font-size:12px;color:#b5b8b0;padding:6px;border-radius:6px;
}
.row-ext:hover{color:var(--accent);background:rgba(184,74,36,.08)}
.empty-state{text-align:center;padding:60px 0 100px;color:var(--muted)}
.empty-title{font-family:var(--serif);font-size:24px;color:var(--ink);margin-bottom:8px}

/* ---------- page head ---------- */
.crumbs{display:flex;gap:8px;align-items:center;font-size:11.5px;color:var(--muted);padding:26px 0 0;flex-wrap:wrap}
.crumbs a:hover{color:var(--accent)}
.crumbs span{color:#b5b8b0}
.page-head{padding:30px 0 34px;border-bottom:1px solid var(--line)}
.page-kicker{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);font-weight:700;margin-bottom:14px}
.page-head h1{font-size:clamp(34px,4.4vw,54px);line-height:1.14;letter-spacing:-.03em;max-width:900px}
.meta-row{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-top:18px}
.meta-link{font-size:12.5px;color:var(--ink-soft);border-bottom:1px solid var(--line);padding-bottom:2px}
.meta-link:hover{color:var(--accent);border-color:var(--accent)}
.tpl-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}
.tpl-row .chip{padding:4px 11px;font-size:11.5px;background:var(--paper-2)}
.hero-title-lg{font-size:clamp(40px,5vw,64px);line-height:1.1;letter-spacing:-.035em;margin-bottom:20px}
.page-hero{padding:64px 0 48px;border-bottom:1px solid var(--line)}

/* ---------- problem layout ---------- */
.problem-layout{display:grid;grid-template-columns:minmax(0,1fr) 290px;gap:68px;padding:48px 0 90px;align-items:start}
.prose{min-width:0;max-width:860px}
.prose section{padding:0 0 40px;margin-bottom:40px;border-bottom:1px solid var(--line-soft)}
.prose section:last-child{border-bottom:0;margin-bottom:0;padding-bottom:0}
.prose h2{
  font-size:13px;font-family:var(--sans);letter-spacing:.12em;text-transform:uppercase;
  color:var(--muted);font-weight:700;margin-bottom:18px;display:flex;align-items:center;gap:10px;
}
.prose h2::before{content:"";width:7px;height:7px;background:var(--accent);border-radius:1px;transform:rotate(45deg);flex:0 0 auto}
.statement-p{font-size:16.5px;line-height:1.95;color:var(--ink-soft);white-space:pre-line}
.lead-p{font-size:16px;line-height:1.9;color:var(--ink-soft);white-space:pre-line}
.sub-h{font-family:var(--sans);font-size:13px;letter-spacing:.08em;color:var(--ink);margin:26px 0 14px;text-transform:uppercase}
.examples{display:grid;gap:10px;margin-top:24px}
.example{background:var(--paper-2);border:1px solid var(--line);border-radius:10px;padding:14px 18px}
.ex-head{font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);font-weight:700;margin-bottom:8px}
.ex-row{display:flex;gap:14px;font-size:13px;padding:4px 0;align-items:baseline}
.ex-row>span{color:var(--muted);flex:0 0 34px;font-size:11.5px}
.ex-row code{font-family:var(--mono);font-size:12.5px;background:rgba(25,29,27,.05);padding:2px 7px;border-radius:5px;word-break:break-word}
.path-line{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin-top:26px;font-size:11.5px}
.path-step{border:1px solid var(--line);padding:5px 12px;border-radius:999px;background:var(--paper-2);color:var(--ink-soft)}
.path-line i{color:#b5b8b0;font-style:normal}
.callout{display:flex;gap:14px;background:var(--green-soft);border-left:3px solid var(--green);padding:16px 18px;border-radius:0 10px 10px 0;margin-top:20px}
.callout-mark{font-family:var(--serif);font-size:20px;color:var(--green);line-height:1.2;font-weight:700}
.callout p{margin:0;font-size:13.5px;color:#244a3b;line-height:1.8}
.signal-list,.var-list,.pitfall-list{list-style:none;padding:0;margin:20px 0 0;display:grid;gap:10px}
.signal-list li,.pitfall-list li,.var-list li{display:flex;gap:14px;align-items:flex-start;background:var(--paper-2);border:1px solid var(--line-soft);border-radius:9px;padding:12px 16px;font-size:13.5px;color:var(--ink-soft)}
.signal-list span,.pitfall-list span{font-family:var(--mono);font-size:10.5px;color:var(--accent);padding-top:3px}
.signal-list p,.pitfall-list p,.var-list p{margin:0;font-size:13.5px;color:var(--ink-soft);line-height:1.75}
.var-list .v-line{font-family:var(--mono);font-size:10.5px;color:var(--accent);background:rgba(184,74,36,.08);padding:2px 7px;border-radius:5px;white-space:nowrap;margin-top:2px}
.var-list .v-dot{width:6px;height:6px;background:var(--accent);border-radius:50%;margin-top:9px;flex:0 0 auto}
.ref-line{font-size:13px;color:var(--muted)}
.complexity-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.complexity-grid>div{background:var(--paper-2);border:1px solid var(--line);border-radius:10px;padding:16px 18px}
.complexity-grid span{display:block;font-size:11px;color:var(--muted);letter-spacing:.06em;margin-bottom:4px}
.complexity-grid strong{font-family:var(--mono);font-size:15px;font-weight:600}

/* ---------- code ---------- */
.code-card{background:var(--code-bg);border-radius:var(--radius);overflow:hidden;box-shadow:0 14px 34px rgba(21,26,24,.16)}
.code-head{display:flex;align-items:center;gap:14px;padding:12px 18px;border-bottom:1px solid var(--code-line)}
.code-dots{display:flex;gap:5px}
.code-dots i{width:8px;height:8px;border-radius:50%;background:#3a443e;display:block}
.code-dots i:first-child{background:#b84a24}
.code-lang{font-size:10.5px;letter-spacing:.1em;color:#8b968e;text-transform:uppercase}
.copy-btn{
  margin-left:auto;border:1px solid #333d37;background:transparent;color:#aab5ac;
  font-size:11px;padding:5px 11px;border-radius:6px;cursor:pointer;font-family:var(--sans);transition:all .18s;
}
.copy-btn:hover{border-color:#6f7d73;color:#e9e5d9}
.code-body{margin:0;padding:18px 0 22px;overflow-x:auto;font-family:var(--mono);font-size:12.8px;line-height:1.78;color:var(--code-text)}
.cl{display:flex;min-width:max-content;padding-right:24px;border-left:2px solid transparent}
.cl .ln{flex:0 0 46px;text-align:right;padding-right:16px;color:#58625b;user-select:none;font-size:11.5px}
.cl .lt{white-space:pre}
.cl.hl{background:linear-gradient(90deg,rgba(184,74,36,.24),rgba(184,74,36,.02));border-left-color:#d9774f}
.cl.hl .lt{color:#ffd9bd}
.tok-kw{color:#e2906f}
.tok-str{color:#a9c98e}
.tok-num{color:#d9b56b}
.tok-cmt{color:#7d8a80;font-style:italic}
.tok-fn{color:#8fb9d9}
.tok-bi{color:#b8a7da}
.code-note{font-size:12px;color:var(--muted);margin-top:12px}
.mini-row .pill,.role-label .pill{transform:none}

/* ---------- rail ---------- */
.rail{position:sticky;top:88px;display:grid;gap:14px}
.rail-card{background:var(--paper-2);border:1px solid var(--line);border-radius:12px;padding:18px}
.rail-card h3{font-family:var(--sans);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:12px;font-weight:700}
.toc{display:grid;gap:2px}
.toc a{font-size:13px;color:var(--ink-soft);padding:5px 8px;border-radius:6px;border-left:2px solid transparent;transition:all .18s}
.toc a:hover{background:rgba(25,29,27,.04)}
.toc a.active{color:var(--accent);border-left-color:var(--accent);background:rgba(184,74,36,.06)}
.tpl-block{display:flex;align-items:center;gap:8px;padding:9px 10px;border-radius:8px;border:1px solid var(--line-soft);margin-bottom:7px;transition:all .18s;flex-wrap:wrap}
.tpl-block:hover{border-color:var(--accent);background:#fff}
.tpl-block-role{font-size:9.5px;letter-spacing:.06em;color:var(--accent);border:1px solid rgba(184,74,36,.3);padding:0 5px;border-radius:4px;white-space:nowrap}
.tpl-block strong{font-size:12.5px;font-weight:600;line-height:1.5}
.tpl-block .arrow{margin-left:auto;color:#b5b8b0;font-size:12px}
.rail-link{display:flex;justify-content:space-between;align-items:center;gap:10px;font-size:12.5px;color:var(--ink-soft);padding:7px 2px;border-bottom:1px solid var(--line-soft)}
.rail-link:last-child{border-bottom:0}
.rail-link i{font-style:normal;color:#b5b8b0;font-size:11px;transition:transform .18s}
.rail-link:hover{color:var(--accent)}
.rail-link:hover i{transform:translateX(3px);color:var(--accent)}
.rail-dl{margin:0;display:grid;gap:8px}
.rail-dl>div{display:flex;justify-content:space-between;gap:12px;font-size:12px}
.rail-dl dt{color:var(--muted)}
.rail-dl dd{margin:0;color:var(--ink-soft);text-align:right}

/* ---------- pager ---------- */
.pager{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:8px}
.pager-link{display:flex;flex-direction:column;gap:3px;border:1px solid var(--line);background:var(--paper-2);border-radius:10px;padding:14px 16px;transition:all .18s}
.pager-link span{font-size:10px;letter-spacing:.08em;color:var(--muted);text-transform:uppercase}
.pager-link strong{font-size:13.5px;font-weight:600;line-height:1.5}
.pager-link.next{text-align:right;align-items:flex-end}
.pager-link:not(.disabled):hover{border-color:var(--accent);transform:translateY(-1px)}
.pager-link.disabled{border-color:transparent;background:transparent}

/* ---------- templates index ---------- */
.tpl-groups{padding:12px 0 90px}
.tpl-group{padding:40px 0;border-top:1px solid var(--line)}
.tpl-group:first-child{border-top:0}
.tpl-group-head{display:flex;align-items:baseline;gap:14px;margin-bottom:22px;flex-wrap:wrap}
.tpl-group-head h2{font-size:26px}
.tpl-group-head .cat-count{margin:0 0 0 auto}
.tpl-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.tpl-card{
  background:var(--paper-2);border:1px solid var(--line);border-radius:12px;padding:20px;
  display:flex;flex-direction:column;gap:10px;transition:transform .2s ease,box-shadow .2s,border-color .2s;
}
.tpl-card:hover{transform:translateY(-3px);border-color:#c9c2b2;box-shadow:var(--shadow)}
.tpl-card-top{display:flex;justify-content:space-between;align-items:center}
.tpl-no{font-family:var(--mono);font-size:11px;color:var(--accent)}
.tpl-count{font-size:10.5px;color:var(--muted);background:rgba(25,29,27,.045);padding:1px 8px;border-radius:999px}
.tpl-card h3{font-size:20px;line-height:1.3}
.tpl-card p{font-size:12.5px;color:var(--muted);line-height:1.7;margin:0;min-height:42px}
.tpl-mini{font-size:11px;color:#9a9e96;border-top:1px dashed var(--line);padding-top:10px;line-height:1.6}
.tpl-card-foot{display:flex;justify-content:space-between;align-items:center;font-size:10.5px;color:var(--muted);margin-top:auto}
.tpl-card-foot .arrow{font-size:14px;color:#b5b8b0;transition:transform .18s,color .18s}
.tpl-card:hover .tpl-card-foot .arrow{transform:translateX(4px);color:var(--accent)}

/* ---------- template detail ---------- */
.tpl-head{padding-bottom:30px}
.tpl-layout{display:grid;grid-template-columns:minmax(0,1fr) 290px;gap:68px;padding:48px 0 90px;align-items:start}
.role-block{margin-top:16px}
.role-label{font-size:10.5px;letter-spacing:.08em;color:var(--muted);text-transform:uppercase;display:block;margin-bottom:8px}
.mini-list{display:grid;gap:0}
.mini-row{display:flex;align-items:center;gap:12px;padding:10px 6px;border-bottom:1px solid var(--line-soft);font-size:13px}
.mini-row:last-child{border-bottom:0}
.mini-no{font-family:var(--mono);font-size:10.5px;color:#a2a69d;flex:0 0 22px}
.mini-title{flex:1;min-width:0}
.mini-role{font-size:10px;color:var(--muted);white-space:nowrap}
.mini-row:hover .mini-title{color:var(--accent)}

/* ---------- footer ---------- */
.footer{border-top:1px solid var(--line);padding:32px 0 40px;margin-top:20px}
.footer-inner{width:min(1180px,calc(100% - 64px));margin:0 auto;display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap}
.footer p{margin:0;font-size:11.5px;color:var(--muted)}
.footer-brand{font-size:11px;letter-spacing:.16em;font-weight:700;color:var(--ink-soft)}

/* ---------- responsive ---------- */
@media (max-width:1024px){
  .hero-inner{grid-template-columns:1fr;gap:40px}
  .hero-map{max-width:560px}
  .problem-layout,.tpl-layout{grid-template-columns:1fr;gap:40px}
  .rail{position:static;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}
  .tpl-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
  .category{grid-template-columns:190px minmax(0,1fr);gap:28px}
}
@media (max-width:760px){
  .container,.topbar-inner,.footer-inner{width:calc(100% - 36px)}
  .topbar-inner{height:58px}
  .brand-text{font-size:11px;letter-spacing:.12em}
  .nav-link{padding:6px 9px;font-size:12px}
  .nav-ext{display:none}
  .hero{padding:50px 0 40px}
  .hero h1{font-size:clamp(38px,11vw,56px)}
  .hero-stats>div{padding:0 14px}
  .hero-stats strong{font-size:24px}
  .cell-grid{grid-template-columns:repeat(15,1fr);gap:3px}
  .category{grid-template-columns:1fr;gap:12px;padding:26px 0}
  .cat-head{position:static;padding-top:0}
  .cat-count{display:inline;margin-left:10px}
  .row-main{grid-template-columns:34px minmax(0,1fr) auto;gap:10px;padding-right:34px}
  .p-arrow{display:none}
  .p-meta{grid-column:3}
  .prose section{padding-bottom:30px;margin-bottom:30px}
  .complexity-grid{grid-template-columns:1fr}
  .tpl-grid{grid-template-columns:1fr}
  .tpl-layout,.problem-layout{padding-top:32px}
  .rail{grid-template-columns:1fr}
  .pager{grid-template-columns:1fr}
  .pager-link.next{text-align:left;align-items:flex-start}
  .footer-inner{flex-direction:column;gap:6px}
  .toolbar{padding:10px}
  .result-count{width:100%;text-align:right;margin-left:0}
}
@media (max-width:480px){
  .hero-map{padding:14px}
  .map-head span:last-child{display:none}
  .diff-filter{width:100%;justify-content:space-between}
  .fchip{flex:1}
  .select-wrap{width:100%}
  .select-wrap select{width:100%}
}
"""
JS = r"""
(function () {
  'use strict';

  // 复制代码
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var card = btn.closest('.code-card');
      if (!card) return;
      var body = card.querySelector('.code-body');
      var text = Array.prototype.map.call(body.querySelectorAll('.lt'), function (el) {
        return el.textContent.replace(/\u00a0/g, '');
      }).join('\n');
      var done = function () {
        var old = btn.textContent;
        btn.textContent = '已复制';
        setTimeout(function () { btn.textContent = old; }, 1500);
      };
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(done, function () { fallback(text, done); });
      } else {
        fallback(text, done);
      }
    });
  });

  function fallback(text, done) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); done(); } catch (e) {}
    document.body.removeChild(ta);
  }

  // 导航页筛选
  var search = document.getElementById('search');
  if (search) {
    var rows = Array.prototype.slice.call(document.querySelectorAll('.problem-row'));
    var sections = Array.prototype.slice.call(document.querySelectorAll('.category'));
    var chips = Array.prototype.slice.call(document.querySelectorAll('[data-diff-filter]'));
    var tplFilter = document.getElementById('tplFilter');
    var countEl = document.getElementById('resultCount');
    var emptyEl = document.getElementById('emptyState');
    var state = { diff: 'all', tpl: 'all', q: '' };

    function apply() {
      var visible = 0;
      rows.forEach(function (row) {
        var okDiff = state.diff === 'all' || row.dataset.diff === state.diff;
        var okTpl = state.tpl === 'all' || row.dataset.tpl.split(' ').indexOf(state.tpl) !== -1;
        var okQ = !state.q || row.dataset.search.toLowerCase().indexOf(state.q) !== -1;
        var ok = okDiff && okTpl && okQ;
        row.hidden = !ok;
        if (ok) visible++;
      });
      sections.forEach(function (sec) {
        var any = Array.prototype.some.call(sec.querySelectorAll('.problem-row'), function (r) { return !r.hidden; });
        sec.hidden = !any;
      });
      if (countEl) countEl.textContent = visible + ' / ' + rows.length + ' 题';
      if (emptyEl) emptyEl.hidden = visible !== 0;
    }

    search.addEventListener('input', function () {
      state.q = search.value.trim().toLowerCase();
      apply();
    });
    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        state.diff = chip.dataset.diffFilter;
        chips.forEach(function (c) { c.classList.toggle('active', c === chip); });
        apply();
      });
    });
    if (tplFilter) {
      tplFilter.addEventListener('change', function () {
        state.tpl = tplFilter.value;
        apply();
      });
    }
    document.addEventListener('keydown', function (e) {
      if (e.key === '/' && document.activeElement !== search) {
        e.preventDefault();
        search.focus();
      }
    });
    apply();
  }

  // 目录高亮
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll('.toc a'));
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var map = {};
    tocLinks.forEach(function (a) {
      var id = a.getAttribute('href').slice(1);
      var sec = document.getElementById(id);
      if (sec) map[id] = a;
    });
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          tocLinks.forEach(function (a) { a.classList.remove('active'); });
          var a = map[entry.target.id];
          if (a) a.classList.add('active');
        }
      });
    }, { rootMargin: '-15% 0px -70% 0px', threshold: 0 });
    Object.keys(map).forEach(function (id) { obs.observe(document.getElementById(id)); });
  }
})();
"""


# --------------------------------------------------------------------------
# 构建
# --------------------------------------------------------------------------
def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "problems"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "templates"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)

    with open(os.path.join(OUT, "assets", "style.css"), "w", encoding="utf-8") as f:
        f.write(CSS)
    with open(os.path.join(OUT, "assets", "app.js"), "w", encoding="utf-8") as f:
        f.write(JS)

    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(page_index())
    with open(os.path.join(OUT, "templates.html"), "w", encoding="utf-8") as f:
        f.write(page_templates_index())

    for p in PROBLEMS:
        with open(os.path.join(OUT, "problems", p["slug"] + ".html"), "w", encoding="utf-8") as f:
            f.write(page_problem(p))
    for t in TEMPLATES:
        with open(os.path.join(OUT, "templates", t["id"] + ".html"), "w", encoding="utf-8") as f:
            f.write(page_template(t))

    print("生成完成：%s" % OUT)
    print("题目 %d 页，模板 %d 页，分类 %d 个" % (len(PROBLEMS), len(TEMPLATES), len(CATEGORIES)))


if __name__ == "__main__":
    main()
