"""더인 교육 14일차 빌드 (2026-11-23 추가).
사용: 작업폴더(scratchpad)에 d14_raw.txt, d14_meta.json, d14/ 가 있는 상태에서 이 폴더에서 실행
  python build_d14.py
"""
import sys
sys.path.insert(0, '.')
import build_d101112 as B
S = B.S

cm14 = {
 "001c0df674cf": ["흠", "이렇게 섞어서 쓰거나 제어하는 이유가 뭐지?"],
 "001cd697a243": ["근데 이게 왜 몇 배를 해주고 있는건데? 20/20 이라고 쓰는 이유가 뭔데?"],
 "001ce44a91a9": ["여기 내용은 내가 더 정리해서 내걸로 만드는거야"],
 "001c7ff74e4e": ["이런 분야는 반도체 뿐만 아니라 여러가지 분야에서 필수 아닌가? 재밌어보이는데"],
 "001c42359e48": ["기본 마인드로 탑재"],
 "001c0db0d77e": ["찾아보기 - 렛유인 교재랑 연관"],
 "001c6c907e1d": ["나 이 얘기 들은 기억이 없는데요?"],
 "001c2270ad9b": ["이게 Borch 인가 borsch 인가 그건가?"],
 "001ca60d51ff": ["숙제"],
}

cap14 = {
 1: "판서 — Metal 층별 Pitch Size: 1X 20/20 · 2X 40/40 · 3X 60/60 · 4X 80/80 · 5X 100/100 (면적과 저항 R)",
 2: "판서 — Contact · Via 구조: W 플러그, Al, IMD · ILD(PMD), 제거 대상(Native Oxide SiO<sub>2</sub>, Al<sub>2</sub>O<sub>3</sub>), Cu: Ta/TaN · W: Ti/TiN",
 3: "판서 — Surface Roughness: 울퉁불퉁한 Si 표면과 그 위에 올라간 막(M)",
 4: "판서 — LER · LWR: 게이트 라인의 가장자리 거칠기와 선폭 변동 (S · D 사이)",
 5: "판서(화이트보드 사진) — 반도체 8대 공정: Photo(PR Mask 형성) → Dry Etch · Ion Implantation → PR 제거(Ashing + PR Strip) → Thin Film Deposition(PVD · CVD · Diffusion) → CMP, ⑧ WET Clean, DOF margin (화이트보드 사진)",
 6: "교재 — Cleaning Steps: 반도체 소자 공정 Step에 따른 Cleaning 공정 기술 분류 (Pre Treatment · Post Treatment · Wet Etch)",
 7: "교재 — Typical Contaminants: Particle · Metal · Organics · Native Oxide · Micro roughness의 오염원(Sources)과 영향(Effects)",
 8: "판서 — 웨이퍼 가장자리: 위 · 아래와 Etch 측",
 9: "교재 — Wet Chemical 재료: Particles · Metallic Impurities · Organic · Micro Roughness · Native Oxide의 오염 경로 · 파급 효과 · 세정 방법",
 10: "Claude 답변 — 세정 약액 표: APM(SC-1) · HPM(SC-2) · SPM · DHF · BHF · IPA의 풀네임과 구성 (Claude 답변 캡처)",
 11: "판서 — ArFi(193 nm) Half pitch = R = k<sub>1</sub>·λ/NA(NA 1.44, 37.5 ≈ 38), RET(off-axis · PSM · OPC), EUV 13.5 nm(NA 0.33 · 0.55)",
 12: "판서(화이트보드 사진) — EUV와 ArF 193i의 해상도 R = k<sub>1</sub>·λ/NA, RET(off-axis · PSM · OPC), LELELE → LE (화이트보드 사진)",
 13: "판서 — R! Loading Effect in Etch: PR 패턴 사이의 식각 깊이 차이",
 14: "판서 — 칩 안의 패턴 밀도(Pattern Density) 차이",
 15: "판서 — Q. ADI CD: 패턴 A · B · C · D · E의 폭(30)과 간격(30 · 30 · 360)",
 16: "판서 — 위 그림에서 패턴 A · B · C · D · E의 영역을 표시한 모습",
 17: "판서 — Drying: 표면 장력 (물방울 곡면)",
 18: "판서 — ALE: (1)층 Si에 붙은 Cl과 아래 (2)층의 Si–Si 결합",
 19: "CCl<sub>4</sub> 폴리머 형성 메커니즘 — 플라즈마에서 분해, 조각이 이어 붙어 고분자가 됨, 전체 반응식 (Claude 답변 캡처)",
 20: "교재 슬라이드 — Future Cleaning: GAA · CFET · 3D NAND로 가면서 Device Damage Free · Material Selectivity · Atomic Level Surface Control, Focusing Technology 5가지 (슬라이드 사진)",
 21: "교재 슬라이드 — Future Cleaning (위 슬라이드 사진과 같은 이미지)",
}

H2_14 = S([
 "잠깐 딴소리", "Clean 공정", "예상되는 문제", "오염 물질", "Cleaning 방법", "Wet Clean 과정", "Dry Clean 과정",
 "Wafer를 처음 투입 할 때 RCA Cleaning을 진행", "그림을 통해 process 이해해보기", "변천사", "Cleaning Parameter", "딴소리",
 "Wet Chemical의 재료", "R! Loading Effect in Etch", "Organic Contaminant, Metallic Contaminant", "Cleaning Method",
 "Attenuated phase shift mask", "Silicon Surface", "Drying", "Resist Strip", "Cleaning Perfectly", "ALE",
 "Etch에 대해서 정리해보자 (잠깐 딴 얘기)",
])
H3_14 = S([
 "12pg", "13pg", "14pg", "16pg", "17pg", "18pg", "19pg", "20pg(과거) → 21pg(현재)", "33, 34pg", "63pg 사진추가하기", "66pg", "67pg",
 "Surface Roughness를 설명하시며", "EUV와 Gate를 언급하며",
 "(1) SiO₂ 제거", "(2) Al₂O₃ 제거", "(1) 화학적인 방법", "(2) 물리적인 방법", "(1) 유기 용제", "(2) 산, 알칼리 계열",
 "(1) micro effect", "(2) macro effect",
])
DESC14 = ('더인 교육 14일차: Metal 배선과 Pitch Size, Clean 공정(오염 물질 · Wet/Dry Clean · RCA Cleaning), Surface Roughness와 EUV · LER/LWR, '
          'RET와 멀티 패터닝(LELELE → LE), Loading Effect · Pattern Density, Drying · Resist Strip · ALE, Etch 정리 노트')

if __name__ == '__main__':
    B.build('d14', 'thein-day14', '더인 교육 14일차', '2026-11-20', cm14, cap14, H2_14, H3_14, [], '들어가며', ('<b>들어가며</b>',), DESC14)
