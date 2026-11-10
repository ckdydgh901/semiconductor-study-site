"""Word(.docx) 'Q1. … / A1. …' 정리노트 -> 사이트 연습용 Q&A 페이지(topics/<id>/index.html).
질문만 보이고 클릭하면 답이 펼쳐지는 <details> 카드로 만든다. file://에서 동작(서버·fetch 불필요).

사용: python docx_to_qa.py <docx경로> <topic-id> [<작업폴더>]
  - Word가 열려 있어도 읽을 수 있지만, 저장하지 않은 수정은 파일에 없다(Ctrl+S 후 실행).
  - 열린 Word 파일은 작업폴더로 복사해서 읽는다(원본은 건드리지 않음).
규칙(원문 그대로): 질문/답 텍스트·번호·오타·메모(*…, (수정이 필요한 답변) 등)를 바꾸지 않는다.
  "[답변]" 줄(구분 표시)만 뺀다. 첨자·단위 표기는 여기서 바꾸지 않는다(사용자 승인 후 notation-fix로).
섹션 묶음(GROUPS)은 질문 번호 기준으로 이 파일에서 정한다. 새 질문이 늘면 GROUPS를 손본다.
"""
import sys, os, re, html, shutil, tempfile
import docx

PROJ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..")).replace("\\", "/")

TITLE = "반도체 정리노트 Q&A 연습"
SHORT = "Q&A 연습"
# (섹션을 시작하는 질문 id, 섹션 제목)
GROUPS = [
    ("1", "Q1~Q2. 반도체의 정의와 종류"),
    ("3", "Q3~Q5. Nitride, 건물 비유, 공정 변천사"),
    ("6", "Q6~Q8. 유전체와 High-k / Low-k"),
    ("9", "Q9~Q15. 8대 공정과 Photo 공정 기초"),
    ("16", "Q16~Q20. 해상도, Yellow Room, 스넬의 법칙·간섭·회절"),
    ("21", "Q21~Q23-3. PR (Negative PR, 흡광계수, NUV 구성·용해)"),
    ("24", "Q24~Q25-1. Wafer"),
    ("26", "Q26~Q28. NA, k1, 회로 선폭"),
    ("29", "Q29~Q31-4. Bake, PEB, HMDS, Adhesion"),
    ("32", "Q32~Q33-1. PMOS, Passivation"),
]

Q_RE = re.compile(r"^(?:\[[^\]]*\]\s*)?Q(\d+(?:-\d+)?)[.)]")


# 사용자가 승인한 첨자·단위 표기 수정(2026-11-08 "전부 적용"). 재변환해도 유지되도록 출력 단계에서 적용한다.
# 새 표기 후보가 생기면 사용자에게 먼저 묻고 승인된 것만 여기에 추가한다. Vt, Vth 같은 관용 표기는 넣지 않는다.
NOTATION = [
    (r"SiO2", "SiO₂"),
    (r"Si3N4", "Si₃N₄"),
    (r"(?<=\d)um(?![A-Za-z])", "μm"),
    (r"10\^-3", "10⁻³"),
    (r"10\^3", "10³"),
]


def fix_notation(s):
    for pat, rep in NOTATION:
        s = re.sub(pat, rep, s)
    return s


def esc(s):
    return html.escape(fix_notation(s), quote=False)


def parse(path):
    d = docx.Document(path)
    paras = [p.text.replace("\r", "").strip() for p in d.paragraphs]
    head, items, cur = [], [], None
    for t in paras:
        m = Q_RE.match(t)
        if m:
            cur = {"id": m.group(1), "q": t, "qsub": [], "ans": [], "marker": False}
            items.append(cur)
            continue
        if not t:
            continue
        if cur is None:
            head.append(t)
        elif t == "[답변]":
            cur["marker"] = True
        elif not cur["marker"] and not re.match(r"^A[\d-]*[.)]", t) and not cur["ans"]:
            cur["qsub"].append(t)          # 질문 아래 보기/키워드(예: Q1의 1.~3.)
        else:
            cur["ans"].append(t)
    return head, items


def card(it):
    qsub = "".join('<span class="qsub">%s</span>' % esc(x) for x in it["qsub"])
    ans = "".join("<p>%s</p>" % esc(x) for x in it["ans"]) or "<p>(답변 없음)</p>"
    return ('      <details class="note qa qa-card" id="q%s"><summary><b>[질문 노트]</b><span class="q">%s</span>%s</summary>\n'
            '        <div class="ans">%s</div>\n      </details>\n') % (it["id"], esc(it["q"]), qsub, ans)


def build(head, items, pid):
    first_ids = {g[0]: g[1] for g in GROUPS}
    body, n, open_sec = [], 0, False
    for it in items:
        if it["id"] in first_ids:
            if open_sec:
                body.append("    </section>\n\n")
            n += 1
            body.append('    <section>\n      <h2 id="s%d">%d. %s</h2>\n' % (n, n, esc(first_ids[it["id"]])))
            open_sec = True
        body.append(card(it))
    if open_sec:
        body.append("    </section>\n")
    tips = [x for x in head[1:]]  # head[0]은 문서 제목
    tip_html = ""
    if tips:
        tip_html = ('    <div class="note"><b>[사용자 노트 필기]</b>\n' +
                    "".join("      <p>%s</p>\n" % esc(x) for x in tips) + "    </div>\n")
    return '''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="Word로 정리한 반도체 질문과 답변. 질문만 보고 답해 본 뒤 눌러서 답을 확인하는 연습용 페이지">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../assets/style.css">
</head>
<body data-root="../../" data-topic="%(pid)s">

<div id="progress" aria-hidden="true"></div>

<header class="site-header">
  <button id="menuBtn" class="icon-btn menu-btn" aria-label="목차 열기" aria-expanded="false">☰</button>
  <a id="brand" class="brand" href="../../index.html">나의 공부 공간</a>
  <nav id="tabs" class="tabs" aria-label="주제"></nav>
  <button id="themeBtn" class="icon-btn" aria-label="다크 모드 전환">◐</button>
</header>

<div class="layout">
  <aside id="sidebar" class="sidebar" aria-label="목차">
    <div class="sidebar-head">
      <a href="#top" class="sidebar-title">%(short)s</a>
    </div>
    <nav id="toc"></nav>
  </aside>
  <div id="scrim" class="scrim"></div>

  <main id="top" class="content">

    <header class="cover">
      <h1>%(title)s</h1>
      <p class="meta">질문만 보고 먼저 말해 본 뒤, 질문을 눌러서 답변을 확인합니다. (총 %(count)d문항)</p>
      <p class="meta">출처: Word 파일 「반도체 정리노트」 (사용자 정리)</p>
      <div class="qa-tools">
        <button type="button" class="qa-btn" id="openAll">모두 펼치기</button>
        <button type="button" class="qa-btn" id="closeAll">모두 접기</button>
      </div>
    </header>

%(tips)s
%(body)s
    <footer class="site-footer">
      <p>질문과 답변은 사용자가 Word에 정리한 원문 그대로입니다.</p>
      <p><span id="updatedAt"></span> · <a href="../../index.html">홈으로</a></p>
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
<script>
(function () {
  var all = function () { return document.querySelectorAll('details.qa-card'); };
  var set = function (v) { Array.prototype.forEach.call(all(), function (d) { d.open = v; }); };
  document.getElementById('openAll').addEventListener('click', function () { set(true); });
  document.getElementById('closeAll').addEventListener('click', function () { set(false); });
  /* 주소의 #q31 처럼 질문으로 바로 이동하면 그 질문은 펼쳐 둔다 */
  function openHash() { var h = location.hash; if (h.indexOf('#q') === 0) { var e = document.getElementById(h.slice(1)); if (e && e.tagName === 'DETAILS') e.open = true; } }
  openHash(); window.addEventListener('hashchange', openHash);
})();
</script>
</body>
</html>
''' % dict(title=TITLE, pid=pid, short=SHORT, count=len(items), tips=tip_html, body="".join(body))


if __name__ == "__main__":
    src, pid = sys.argv[1], sys.argv[2]
    work = sys.argv[3] if len(sys.argv) > 3 else tempfile.gettempdir()
    tmp = os.path.join(work, "_qa_copy.docx")
    shutil.copy(src, tmp)                      # Word가 열어 둔 파일이어도 복사본으로 읽는다
    head, items = parse(tmp)
    out_dir = os.path.join(PROJ, "topics", pid)
    os.makedirs(out_dir, exist_ok=True)
    page = build(head, items, pid)
    open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(page)
    ids = [it["id"] for it in items]
    print("questions:", len(items), "| groups:", len(GROUPS))
    print("unlabeled starts:", [g[0] for g in GROUPS if g[0] not in ids])
    print("empty answers:", [it["id"] for it in items if not it["ans"]])
    print("with qsub:", [it["id"] for it in items if it["qsub"]])
