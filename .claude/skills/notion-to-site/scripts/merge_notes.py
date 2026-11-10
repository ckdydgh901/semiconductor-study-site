# -*- coding: utf-8 -*-
"""이미지·제목 없이 바로 이어지는 [사용자 노트 필기] 박스를 하나로 합친다 (사용자 지시, 2026-11-10).
- 라벨은 첫 박스에만 남기고, <p> 줄의 순서·문구는 그대로 둔다.
- 이미지·제목·질문 노트 등으로 나뉜 박스와 .cols2 안의 나란한 박스(줄바꿈 없이 붙음)는 건드리지 않는다.
사용법: python merge_notes.py topics/*/index.html   (파일을 제자리에서 고친다)
"""
import re, sys

PAT = re.compile(
    r'(<div class="note">\s*<b>\[사용자 노트 필기\]</b>(?:(?!</div>).)*?)'
    r'\r?\n[ \t]*</div>[ \t]*\r?\n[ \t]*<div class="note">\s*<b>\[사용자 노트 필기\]</b>',
    re.S)

def merge_adjacent_notes(html):
    prev = None
    while prev != html:
        prev = html
        html = PAT.sub(r'\1', html)
    return html

if __name__ == "__main__":
    for p in sys.argv[1:]:
        s = open(p, encoding="utf-8", newline="").read()
        t = merge_adjacent_notes(s)
        if t != s:
            open(p, "w", encoding="utf-8", newline="").write(t)
            print("merged:", p, s.count("[사용자 노트 필기]") - t.count("[사용자 노트 필기]"))
