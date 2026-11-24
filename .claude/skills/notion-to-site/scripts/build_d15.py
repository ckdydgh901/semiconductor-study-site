"""더인 교육 15일차 빌드 (2026-11-24 추가). 노션의 `생각정리` 아래 "B.D" 줄부터 끝까지(개인적인 생각 14개 항목)는 사용자 지시로 옮기지 않는다 —
d15_raw.txt는 이미 그 앞에서 잘라 만든 것이다(원문 15일차 노션에서 "B.D" 이후를 제거)."""
import sys
sys.path.insert(0, '.')
import build_d101112 as B
import build_generic as G
S = B.S
cm = {"001cedb31d30": ["무슨 소릴까?"]}
cap = {
 1: "판서 — Turn on Voltage: 다이오드와 저항의 I–V 특성 그래프",
 2: "EDS 기본 테스트 표 — Power Short · Pin Open/Short(Continuity) · Pin Leakage (Claude 답변 캡처)",
 3: "열가소성과 열경화성 비교표, Tg와 반도체(EMC · 포토레지스트)와의 연결 (Claude 답변 캡처)",
 4: "판서 — 입력 전압 0 V · 3.3 V에 따른 I–V 곡선과 I<sub>IL</sub> · I<sub>IH</sub>",
}
H2 = S(["신소재공학과에서 외우면 좋을 만한 것들", "신소재가 전문으로 할 수 있어야 함 (전 유기쪽인데요;)", "금속 전기전도도 순서", "PN 접합", "전압", "DRAM", "EDS",
        "Parameter Analyzer (파라미터 분석기)", "Transistor", "정전기 (Electrostatic)", "Open과 Short가 일어나는 이유?", "반도체 패키징",
        "Capacitance 감소가 되면 다른 값들은 어떻게 되는가?", "<반도체 카페에서 다시 확인>", "생각정리"])
H3 = S(["(1) 문턱전압이 높다.", "(2) Isat 감소한다 → 성능이 떨어진다.", "(3) Ioff 증가한다."])
DESC = ('더인 교육 15일차: 금속 전기전도도 순서, PN 접합·전압, DRAM(LPDDR/DDR)과 EDS 테스트(Power short · Pin open/short · Pin Leakage), '
        'Parameter Analyzer(V_th · I_sat · I_off), 정전기, 반도체 패키징(Tg · 열가소성/열경화성), Capacitance 감소의 영향, 포트폴리오 정리 방법')
if __name__ == '__main__':
    G.build_page('d15', 'thein-day15', '더인 교육 15일차', '15일차', '2026-11-21', '교육', cm, cap, H2, H3, [], '신소재공학과에서 외우면 좋을 만한 것들',
                 ('<b>신소재공학과에서 외우면 좋을 만한 것들</b>',), DESC)
