"""Notion(enhanced markdown) -> 사이트 주제 페이지 변환기.
본문 텍스트는 노션 원문 그대로 쓰고, 구조(제목 승격·삽입)만 규칙으로 지정한다.
"""
import json, re, os, html as H

PROJ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "topics")).replace("\\", "/") + "/"

# ---------------------------------------------------------------- 인라인
def inline(s, anchors=None):
    def disc(m):
        if anchors is not None:
            anchors.append((m.group(1)[-12:], re.sub(r"<[^>]+>", "", m.group(2)).strip()))
        return m.group(2)
    s = re.sub(r'<span discussion-urls="discussion://[^/"]+/[^/"]+/([0-9a-f-]+)">(.*?)</span>', disc, s, flags=re.S)
    s = s.replace('<span color="red_bg">', '<span class="mark-red">').replace('<span color="yellow_bg">', '<span class="mark-yel">')
    s = re.sub(r'<span color="[a-z_]+">', '<span>', s)
    s = s.replace("<br />", "<br>")
    s = s.replace("\\<", "&lt;").replace("\\>", "&gt;")
    s = re.sub(r'\\([\\`*_{}\[\]()#+\-.!~^|:"\'$%&])', r"\1", s)
    s = re.sub(r"&(?!(?:amp|lt|gt|quot|#\d+);)", "&amp;", s)
    return s.strip()

def plain(html_s):
    return H.unescape(re.sub(r"<[^>]+>", "", html_s)).strip()

def is_bold_only(s):
    return re.fullmatch(r"\s*<b>(?:(?!</b>).)*</b>\s*", s, flags=re.S) is not None

# ---------------------------------------------------------------- 파서
def parse(lines, ctx):
    items = []; i = 0; n = len(lines)
    while i < n:
        raw = lines[i]; s = raw.strip(); i += 1
        if not s: continue
        if s == "<p />": items.append(("sp",)); continue
        if s.startswith("<image "):
            ctx["img"] += 1; items.append(("img", ctx["img"])); continue
        if s == "---": items.append(("hr",)); continue
        if s.startswith("#### "): items.append(("h4", s[5:])); continue
        if s == "<p>":
            buf = []
            while i < n and lines[i].strip() != "</p>":
                if lines[i].strip(): buf.append(lines[i].strip())
                i += 1
            i += 1
            if buf: items.append(("line", "<br>".join(buf)))
            continue
        if s.startswith("<p>") and s.endswith("</p>"):
            items.append(("line", s[3:-4])); continue
        if s == "<ul>":
            while i < n and lines[i].strip() != "</ul>":
                if lines[i].strip() == "<li>":
                    inner = []; i += 1
                    while i < n and lines[i].strip() != "</li>":
                        inner.append(lines[i]); i += 1
                    i += 1
                    sub_items = parse(inner, ctx)
                    if sub_items and sub_items[0][0] == "line":
                        sub_items[0] = ("bullet", sub_items[0][1], 0)
                    items.extend(sub_items)
                else:
                    i += 1
            i += 1
            continue
        if s.startswith("<columns>"):
            cols = []; cur = None
            while i < n and lines[i].strip() != "</columns>":
                t = lines[i].strip()
                if t.startswith("<column"): cur = []
                elif t == "</column>": cols.append("<br>".join(cur)); cur = None
                elif cur is not None and t: cur.append(t)
                i += 1
            i += 1
            items.append(("cols", cols)); continue
        if s.startswith("<callout"):
            inner = []
            while i < n and lines[i].strip() != "</callout>":
                inner.append(lines[i]); i += 1
            i += 1
            items.append(("callout", parse(inner, ctx))); continue
        if s == "<quote>":
            buf = []
            while i < n and lines[i].strip() != "</quote>":
                if lines[i].strip(): buf.append(lines[i].strip())
                i += 1
            i += 1
            items.append(("quote", "<br>".join(buf))); continue
        if s.startswith("> "):
            buf = [s[2:]]
            while i < n and lines[i].strip().startswith("> "):
                buf.append(lines[i].strip()[2:]); i += 1
            items.append(("quote", "<br>".join(buf))); continue
        m = re.match(r"^(\s*)- (.*)$", raw)
        if m:
            items.append(("bullet", m.group(2).strip(), len(m.group(1)) // 2)); continue
        items.append(("line", s))
    return items

# ---------------------------------------------------------------- 빌더
class Builder:
    def __init__(self, items, meta, caps, comments, h2=(), h3=(), rename=None, insert=None, first_title="", drop_first=None):
        self.items, self.meta, self.caps, self.comments = items, meta, caps, comments
        self.h2, self.h3, self.rename = set(h2), set(h3), rename or {}
        self.insert = list(insert or [])          # [(prefix, kind, title)]
        self.first_title, self.drop_first = first_title, drop_first
        self.secs = []; self.cur = None; self.h3n = 0
        self.run = []; self.qa = None; self.used_cmt = set()

    # ---- 출력 조각
    def figure(self, n):
        fn, w, h, _ = self.meta[n - 1]; cap = self.caps[n]
        alt = H.escape(H.unescape(re.sub(r"<[^>]+>", "", cap)))
        return (f'      <figure><img src="images/{fn}" width="{w}" height="{h}" alt="{alt}" loading="lazy">'
                f'<figcaption>{cap} (출처: 사용자 노션 캡처)</figcaption></figure>\n')

    def cmt_boxes(self, anchors):
        out = ""
        for tail, ctxt in anchors:
            if tail in self.used_cmt or tail not in self.comments: continue
            self.used_cmt.add(tail)
            ps = "".join(f"        <p>{inline(c)}</p>\n" for c in self.comments[tail])
            short = H.escape(ctxt if len(ctxt) <= 60 else ctxt[:58] + "…", quote=False)
            out += ('      <div class="note cmt"><b>[댓글]</b>\n'
                    f'        <p class="cmt-ctx">대상: “{short}”</p>\n{ps}      </div>\n')
        return out

    def emit(self, html_s):
        if self.cur is None:
            self.new_section(self.first_title or "본문")
        self.cur["body"].append(html_s)

    def new_section(self, title):
        k = len(self.secs) + 1
        if not re.match(r"^\d+\. ", title): title = f"{k}. {title}"
        self.cur = {"id": f"s{k}", "title": title, "body": []}
        self.secs.append(self.cur); self.h3n = 0

    def flush_run(self):
        if not self.run: return
        ps = []; anchors = []
        for it in self.run:
            html_s = inline(it[1], anchors)
            if it[0] == "bullet":
                lvl = it[2]
                ps.append(f'        <p class="sub">– {html_s}</p>' if lvl else f"        <p>- {html_s}</p>")
            else:
                ps.append(f"        <p>{html_s}</p>")
        self.emit('      <div class="note"><b>[사용자 노트 필기]</b>\n' + "\n".join(ps) + "\n      </div>\n" + self.cmt_boxes(anchors))
        self.run = []

    def flush_qa(self):
        if not self.qa: return
        ps = []; anchors = []
        for k, it in enumerate(self.qa):
            html_s = inline(it[1], anchors)
            if k == 0:
                html_s = re.sub(r"^\s*<b>(.*)</b>\s*$", r"\1", html_s, flags=re.S)
                ps.append(f'        <p class="q">{html_s}</p>')
            elif it[0] == "bullet":
                ps.append(f"        <p>- {html_s}</p>")
            else:
                ps.append(f"        <p>{html_s}</p>")
        self.emit('      <div class="note qa"><b>[질문 노트]</b>\n' + "\n".join(ps) + "\n      </div>\n" + self.cmt_boxes(anchors))
        self.qa = None

    def flush(self):
        self.flush_run(); self.flush_qa()

    # ---- 항목 키(삽입 규칙용)
    def key_of(self, it):
        if it[0] in ("line", "bullet", "quote"): return plain(inline(it[1]))
        if it[0] == "cols": return plain(inline(it[1][0]))
        if it[0] == "h4": return plain(inline(it[1]))
        return None

    def render_callout(self, inner):
        anchors = []; ps = []
        for it in inner:
            if it[0] in ("line", "bullet"):
                t = inline(it[1], anchors)
                ps.append(f"      <p>- {t}</p>" if it[0] == "bullet" else f"      <p>{t}</p>")
        return '      <div class="callout">\n' + "\n".join(ps) + "\n      </div>\n" + self.cmt_boxes(anchors)

    def heading(self, kind, text_html):
        self.flush()
        anchors = []
        t = inline(text_html, anchors)
        t = re.sub(r"</?b>", "", t).strip()
        t = self.rename.get(plain(t), t)
        if kind == "h2":
            self.new_section(t)
        else:
            if self.cur is None: self.new_section(self.first_title or "본문")
            self.h3n += 1
            self.cur["body"].append(f'\n      <h3 id="{self.cur["id"]}-{self.h3n}">{t}</h3>\n')
        self.cur["body"].append(self.cmt_boxes(anchors))

    def build(self):
        items = self.items; sp_run = 0; first = True
        for it in items:
            kind = it[0]
            # 삽입 규칙
            key = self.key_of(it)
            if key is not None:
                for ent in list(self.insert):
                    if key.startswith(ent[0]):
                        self.insert.remove(ent)
                        self.heading(ent[1], ent[2])
                        break
            if kind == "sp":
                sp_run += 1
                if sp_run >= 2: self.flush_qa()
                continue
            sp_run = 0
            if first and self.drop_first and kind == "line" and plain(inline(it[1])) == self.drop_first:
                first = False; continue
            first = False
            if kind == "h4":
                self.heading("h2", it[1]); continue
            if kind == "hr":
                self.flush(); continue
            if kind == "img":
                self.flush(); self.emit(self.figure(it[1])); continue
            if kind == "callout":
                self.flush(); self.emit(self.render_callout(it[1])); continue
            if kind == "quote":
                self.flush(); anchors = []
                self.emit(f"      <blockquote>{inline(it[1], anchors)}</blockquote>\n" + self.cmt_boxes(anchors)); continue
            if kind == "cols":
                self.flush(); anchors = []
                boxes = "".join(f'<div class="note"><b>[사용자 노트 필기]</b><p>{inline(c, anchors)}</p></div>' for c in it[1])
                self.emit(f'      <div class="cols2">{boxes}</div>\n' + self.cmt_boxes(anchors)); continue
            # line / bullet
            txt = plain(inline(it[1]))
            if kind == "line" and is_bold_only(it[1]) or kind == "line":
                if txt in self.h2: self.heading("h2", it[1]); continue
                if txt in self.h3: self.heading("h3", it[1]); continue
            if kind == "bullet" and txt in self.h3:
                self.heading("h3", it[1]); continue
            if self.qa is not None:
                self.qa.append(it); continue
            if kind == "line" and re.match(r"^Q\d?\.", txt):
                self.flush_run(); self.qa = [it]; continue
            self.run.append(it)
        self.flush()
        return [(s["id"], s["title"], "".join(s["body"])) for s in self.secs]

# ---------------------------------------------------------------- 페이지
def render_page(pid, title, side, desc, sub_line, source, secs):
    body = "".join(f'\n    <section>\n      <h2 id="{i}">{t}</h2>\n{b}    </section>\n' for i, t, b in secs)
    toc = " · ".join(f'<a href="#{i}">{re.sub(r"^\d+\. ", "", t)}</a>' for i, t, _ in secs)
    page = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../assets/style.css">
</head>
<body data-root="../../" data-topic="{pid}">

<div id="progress" aria-hidden="true"></div>

<header class="site-header">
  <button id="menuBtn" class="icon-btn menu-btn" aria-label="목차 열기" aria-expanded="false">☰</button>
  <a id="brand" class="brand" href="../../index.html">나의 공부 공간</a>
  <nav id="tabs" class="tabs" aria-label="영역"></nav>
  <button id="themeBtn" class="icon-btn" aria-label="다크 모드 전환">◐</button>
</header>

<div class="layout">
  <aside id="sidebar" class="sidebar" aria-label="목차">
    <div class="sidebar-head">
      <a href="#top" class="sidebar-title">{side}</a>
    </div>
    <nav id="toc"></nav>
  </aside>
  <div id="scrim" class="scrim"></div>

  <main id="top" class="content">

    <header class="cover">
      <h1>{title}</h1>
      <p class="meta">{sub_line}</p>
      <p class="meta">{source}</p>

      <div class="toc-box">
        <b>목차</b>
        <p>{toc}</p>
        <p class="meta small">[사용자 노트 필기] 표시 = 사용자가 노션에 직접 정리한 원본 노트(내용·말투·감상은 원문 그대로). [질문 노트] = 사용자의 질문과 답. [댓글] = 사용자가 노션에 남긴 댓글. 회색 캡션은 이미지 설명.</p>
      </div>
    </header>
{body}
    <footer class="site-footer">
      <p>필기는 사용자가 노션에 정리한 원문 그대로이며, 이미지는 교재·강의 슬라이드·판서 촬영본입니다.</p>
      <p><span id="updatedAt"></span> · <a id="notionLink" href="#" target="_blank" rel="noopener" hidden>Notion 원본 보기</a> · <a href="../../index.html">홈으로</a></p>
    </footer>
  </main>
</div>

<button id="toTop" class="to-top" aria-label="맨 위로" hidden>↑</button>

<div id="lightbox" class="lightbox" hidden role="dialog" aria-modal="true" aria-label="이미지 확대">
  <button class="lb-close" aria-label="닫기">✕</button>
  <img alt="">
  <p class="lb-cap"></p>
</div>

<script src="../../topics.js"></script>
<script src="../../assets/common.js"></script>
<script src="../../assets/topic.js"></script>
</body>
</html>
'''
    open(PROJ + pid + "/index.html", "w", encoding="utf-8").write(page)
    return page

def load_content(raw_path):
    t = open(raw_path, encoding="utf-8").read()
    c = t.split("<content>", 1)[1].split("</content>", 1)[0]
    return c.split("\n")
