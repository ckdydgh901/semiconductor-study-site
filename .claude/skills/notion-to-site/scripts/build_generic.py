"""노션 페이지 → 주제 페이지 범용 빌드 (2026-11-24). build_d101112.build()와 같지만 종류(교육/강의 등)와 사이드바 제목을 지정할 수 있다.
사용 예(작업폴더 W에 <tag>_raw.txt, <tag>_meta.json 이 있는 상태):
  import build_generic as G
  G.build_page('ic','kocw-interconnect','KOCW 세종대 이원준 교수님 (Interconnect 1&2)','KOCW 배선','2026-11-24','강의',cm,cap,h2,h3,[],first_title,(),desc)
"""
import sys, json
sys.path.insert(0, '.')
import build_d101112 as B
import notion2site as N

def build_page(tag, pid, title, side, date, kind, cm, cap, h2, h3, ins, first_title, drop_exact, desc, source=None):
    items = B.add_q_breaks(N.parse(B.load(tag, drop_exact), {"img": 0}))
    meta = json.load(open(B.W + f'{tag}_meta.json'))
    n_img = sum(1 for it in items if it[0] == 'img') + sum(len(ids) for it in items if it[0] == 'imgcols' for ids in it[1])
    assert len(meta) == n_img, (len(meta), n_img)
    assert sorted(cap) == list(range(1, len(meta) + 1)), (sorted(cap)[:3], len(cap))
    b = N.Builder(items, meta, cap, {k: [B.clean_c(c) for c in v] for k, v in cm.items()},
                  h2=h2, h3=h3, rename={}, insert=ins, first_title=first_title, drop_first=None)
    secs = [(i, t, B.ctxfix(x)) for i, t, x in b.build()]
    unused = set(cm) - b.used_cmt
    if unused: print('!! unused comments:', sorted(unused))
    N.render_page(pid, title, side, desc, f"날짜: {date} · 종류: {kind}", source or f"원본: 사용자 노션 필기 ({title})", secs)
    print(pid, 'sections:', len(secs), [(i, t) for i, t, _ in secs])
