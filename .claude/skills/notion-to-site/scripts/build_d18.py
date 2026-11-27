"""더인 교육 18일차 빌드 (2026-11-27 추가).
- 맨 위 "여기에 적인 내용은 웹사이트로 옮기지 말 것" 블록(번호 1~5)은 사용자 표시대로 옮기지 않는다.
- "오후 수업" 안에 그 블록 1·2번과 똑같이 다시 적힌 두 줄도 함께 뺐다.
- d18_raw.txt는 위 줄들을 뺀 채로 만든 것이다."""
import sys, re
sys.path.insert(0, '.')
import build_d101112 as B
import build_generic as G
S = B.S
raw = open(B.W + 'd18_raw.txt', encoding='utf-8').read()
bold = [m.group(1) for m in re.finditer(r'^<b>(.*?)</b>\s*$', raw, re.M)]
major = ["Cleaning Review", "듀얼 다마신 설명 (Etch stopper에 대한 설명)", "What is CMP", "CMP Utilization", "CMP에서 중요한 것들 - 14pg",
         "25pg - Preston’s Law", "26pg - CMP Pad", "<span color=\"yellow_bg\">32,33pg - CMP Slurry - Contents</span>", "34pg - CMP Slurry 종류",
         "Zeta potential -44, 45, 46pg", "다양한 Slurry들", "<b>Ceria (CeO₂)</b>", "Ceria (CeO₂)", "STI CMP - 71pg", "W CMP - 73pg", "Cu CMP - 80pg, 81pg",
         "Future Tech - 99pg", "지난 주 숙제에 대한 설명", "오후 수업", "Review Metal 17, 18개 "]
H2 = S(major)
H3 = S(bold + ["7pg", "8pg", "15pg", "16pg, 17pg - Platen", "18pg - Wafer Carrier", "21pg - Removal Rate", "22pg - Conditional", "39pg", "75pg, 76pg"]) - H2
cm = {
 "001c61cb5a86": ["이거 이해하고 넘어가기"],
 "001cc3fc0487": ["Etch 할 때 무슨 gas 사용하는지 다시 복습하기!"],
 "001cab96c879": ["이게 뭔데??"],
 "001c11f33067": ["silicate가 SiO2야?"],
 "001cc7c29176": ["왜 반데르발스 힘은 달라붙으려고 하는데?"],
 "001c086753ec": ["이건 어떻게 아는거지? 그냥 받아들이는 영역인가?"],
}
caps = [
 "판서 — CMP 전 단차 위의 PR 노광: Mask · PR · ILD/PMD",
 "판서 — 단차에 따른 DOF 차이 (x만큼의 높이 차)",
 "판서 — R = k<sub>1</sub>·λ/NA, DOF = k<sub>2</sub>·λ/NA²",
 "판서 — CMP ① 면과 DOF, R · DOF 식",
 "판서 — 듀얼 다마신 구조: Si<sub>3</sub>N<sub>4</sub> · IMD · Si<sub>3</sub>N<sub>4</sub> · IMD",
 "판서 — PR 패턴과 3000 Å 식각, Etch stopper(Si<sub>3</sub>N<sub>4</sub>)",
 "교재 — CMP: BPSG Depo, Re-flow 후, CMP 후 단면 SEM (교재 사진)",
 "교재 — CMP Infrastructure: 측정·검사 항목 (Removal Rate, Uniformity, Dishing, Erosion, Plug recess, Planarity 등) (교재 사진)",
 "판서 — 패턴 밀도 차이에 따른 CMP 후 표면 (Dishing)",
 "판서 — 빈 곳에 Dummy pattern을 넣은 모습",
 "정상과 Plug recess 비교 그림 (Claude 답변 캡처)",
 "판서 — Planarity: CMP 전후 평탄화 정도",
 "교재 — CMP System: Pad에 따른 산화막 Removal rate 분포 (교재 사진)",
 "CMP 공정 모식도 — 압력 · Slurry · Chuck · Wafer · Pad · Platen (SK hynix Newsroom)",
 "CMP 장비 구성 — Load, Head, Membrane/Retainer ring, Conditioner, Platen, Pad",
 "판서 — STI 산화(Bird’s beak)와 Contact 면적 · W 감소: I<sub>DS</sub> ∝ μC<sub>ox</sub>W/L",
 "판서 — Si<sub>3</sub>N<sub>4</sub> · SiO<sub>2</sub>와 Bird’s beak",
 "판서 — Bird’s beak으로 인해 생기는 문제 영역",
 "판서 — W plug와 Ti/TiN Barrier의 CMP · Blanket etch",
 "판서 — Poly-Si 위 PR 패터닝과 SiO<sub>2</sub>",
 "판서 — RMG: W 게이트와 Ti/TiN",
 "판서 — RMG 흐름: Poly-Si를 Wet etch로 제거",
 "교재 — CMP Slurry 입자: Fumed Silica와 Colloidal Silica (교재 사진)",
 "판서(종이) — Al + 0.5% Cu 흐름성 금속과 Contact · 평탄화 (필기 사진)",
 "판서 — Al 증착과 평탄화 전 단면 흐름 ①②③",
 "화이트보드 — B/L · W/L · Capacitor contact, Metal-Semi / Metal-Metal, Silicide (화이트보드 사진)",
 "교재 — CMP Slurry: FEOL은 Ceria, BEOL은 Silica (교재 사진)",
 "판서 — Edge Engineering: Bevel (W CVD · PR coating)",
 "교재 — STI CMP 공정 순서 (교재 사진)",
 "판서 — W 채움에서의 Grain과 Seam",
 "판서 — 웨이퍼에 남은 W",
 "판서 — R = ρ·L/A, Al → Cu, Ta/TaN과 Ru · Mo · Co",
 "판서 — 전자 충돌로 여기된 Ar이 빛을 내는 모습: E = hν",
 "판서 — 전자 에너지 분포(EEDF) 곡선",
]
cap = {i + 1: c for i, c in enumerate(caps)}
DESC = ('더인 교육 18일차: Cleaning 복습, CMP(Litho DOF, 듀얼 다마신 Etch stopper, Pattern density · Dishing · Plug recess, Preston 법칙, Pad · Slurry · Ceria, STI · W · Cu CMP), '
        'RMG, 플라즈마가 보라색인 이유와 EEDF 정리 노트')
if __name__ == '__main__':
    G.build_page('d18', 'thein-day18', '더인 교육 18일차', '18일차', '2026-11-26', '교육', cm, cap, H2, H3, [], '들어가며', ('<b>들어가며</b>',), DESC)
