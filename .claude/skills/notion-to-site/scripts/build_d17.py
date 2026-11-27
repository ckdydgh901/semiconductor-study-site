"""더인 교육 17일차 빌드 (2026-11-24 추가)."""
import sys
sys.path.insert(0, '.')
import build_d101112 as B
import build_generic as G
S = B.S
cap = {
 1: "Colab 노트북 — print('Hello Jupyter notebook!!') 실행 화면 (261124 더 인 에듀 파이썬 실습.ipynb)",
 2: "판서 — 입력 x가 함수 f(x)를 거쳐 출력 y로 나오는 모습 (Print · 함수 개념)",
 3: "진수 표현 — 10진법 · 60진법 · 12진법, 컴퓨터의 2진법(on/off), 8진수·16진수와 파이썬의 입력 표기 (Ob · Oo · Ox) (강의 슬라이드)",
}
H2 = S(["강의자료", "코랩으로 진행", "Print가 갖는 의미", "정올"])
DESC = '더인 교육 17일차: 파이썬(Colab) 실습 안내, Print의 의미, 정올(jungol) 문제, 진수 표현'
if __name__ == '__main__':
    G.build_page('d17', 'thein-day17', '더인 교육 17일차', '17일차', '2026-11-24', '교육', {}, cap, H2, set(), [], '수업 일정', ('<b>수업 일정</b>',), DESC)
