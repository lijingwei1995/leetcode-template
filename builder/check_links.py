# -*- coding: utf-8 -*-
"""检查生成站点中的内部链接是否都能落到真实文件。"""

import os
import re
import sys
from urllib.parse import unquote

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "html")
HREF = re.compile(r'href="([^"]+)"')

bad = []
checked = 0
for base, _, files in os.walk(ROOT):
    for name in files:
        if not name.endswith(".html"):
            continue
        path = os.path.join(base, name)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        for href in HREF.findall(text):
            if href.startswith(("http://", "https://", "#", "mailto:", "data:")):
                continue
            checked += 1
            target = os.path.normpath(os.path.join(base, unquote(href.split("#")[0])))
            if not os.path.exists(target):
                bad.append((os.path.relpath(path, ROOT), href))

print("检查内部链接 %d 个，失效 %d 个" % (checked, len(bad)))
for page, href in bad[:30]:
    print("  %s -> %s" % (page, href))
sys.exit(0 if not bad else 1)
