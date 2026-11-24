import sys
sys.path.insert(0, '.')
import build_d101112 as B
import build_generic as G
S = B.S
cm = {"001cfe9b3cc1": ["그러면 TiN은?"]}
cap = {
 1: "배선공정이란? — Metallization · Interconnect · BEOL 용어와 배선 구조의 변화 (강의 슬라이드)",
 2: "MPU Interconnects — 단면도(Global · Intermediate · Metal 1)와 Top view (Source: ITRS 2007)",
 3: "반도체 배선구조의 발전 — 256k DRAM(Al/Si contact) · W via 2층 배선 · Cu 10층 배선 (Source: ADMETA 2008)",
 4: "반도체 배선기술의 흐름 — Spiking, 단차 문제, Stress voiding, CMP, Low-k까지 배선층수별 기술 변천 (Source: ADMETA 2008)",
 5: "AL 배선기술 — 섹션 표지 슬라이드",
 6: "Junction Spiking — Al(Si) Alloy와 Barrier Metal(TiSi<sub>2</sub> · TiN)",
 7: "Reliability Issue → Al(Cu) alloy — Hillock · Void와 Electromigration",
 8: "Al Alloy → Sputtering — Evaporation과 Sputtering 비교",
 9: "Poly gate, junction → silicides — Salicide(self-aligned silicide) 공정 (Figure 11-14)",
 10: "C54-TiSi<sub>2</sub>, CoSi<sub>2</sub>, NiSi — 실리사이드 특성 비교표",
 11: "C54-TiSi<sub>2</sub> Limitation — C49 → C54 상전이와 좁은 선폭 문제",
 12: "CoSi<sub>2</sub> Limitation — poly-Si 선폭에 따른 저항 상승과 NiSi 비교",
 13: "Multilevel Metallization → W Plug — 초기 2층 배선의 단차 문제(Failure)와 W plug",
 14: "W Plug Process — TiN · Blanket W · Etchback W (Figure 11-19)",
 15: "텅스텐(W)의 비저항 — Cu · Al · W 비교 (GPT 정보 캡처)",
 16: "Multilevel Metallization → Planarization — 평탄화 종류 (Figure 11-24)",
 17: "Chemical Mechanical Polishing — CMP 시스템 (Figure 11-27)",
 18: "RC Delay — R = ρL/(w·h), C = ε<sub>0</sub>ε<sub>ox</sub>·wL/t<sub>ox</sub>, RC = (ρ/h)·ε<sub>0</sub>ε<sub>ox</sub>·L²/t<sub>ox</sub>",
 19: "Candidates for Interconnect — Al · Au · Ag · Cu 특성 비교표 (Ryu, Ph.D. Thesis, Stanford, 1998)",
}
H2 = S(["Pure한 Al의 다양한 문제들"])
H3 = S(["해결 방법 1 (Al에 미리 Si를 녹여두자)", "해결 방법 2 (Barrier Metal을 사용하자)", "(1) Heating 할 때", "(2) Cooling 할 때",
        "해결책: Cu 넣어주기 (Hillock & Electromigration 해결)", "(이건 강의 내용은 아님)", "(강의 내용)", "Ref) GPT 정보이긴 하지만 실제로 이렇게 비저항 값이 높음"])
DESC = ('KOCW 세종대 이원준 교수님 Interconnect 1&2: 배선 구조와 소재의 변천(Al → W → Cu → Co), Al 배선의 Junction Spiking·Hillock·Void와 Al(Si)·Al(Cu) 합금, '
        'Silicide(TiSi₂ → CoSi₂ → NiSi), W Plug, CMP 평탄화, RC Delay')
if __name__ == '__main__':
    G.build_page('ic', 'kocw-interconnect', 'KOCW 세종대 이원준 교수님 (Interconnect 1&2)', 'KOCW 배선', '2026-11-24', '강의', cm, cap, H2, H3, [], 'Interconnect 1', (), DESC)
