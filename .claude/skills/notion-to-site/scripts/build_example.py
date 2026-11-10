import sys, os, json, re
# 사용: python build_example.py <작업폴더>   (작업폴더 = <tag>_raw.txt, *_meta.json이 있는 곳)
SP = sys.argv[1].rstrip("/\\") + "/"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion2site as N

def clean_c(s): return re.sub(r"(<br\s*/?>)+\s*$", "", s)

# =====================================================================
# 4일차
# =====================================================================
cm4 = {
 "001c7d48923d": ["전기가 흐른다는 말은 애매한 말입니다. 전류가 흐르는 것입니다.",
                  "<b>전기</b>: 전하, 전기장, 전압, 전류, 전기에너지 등을 포괄하는 넓은 개념입니다. 따라서 무엇이 흐른다는 것인지 명확하지 않습니다.",
                  "<b>전류</b>: 단위시간 동안 도체의 단면을 통과하는 전하량을 뜻합니다. 즉, 전하의 이동을 수치로 나타낸 것입니다."],
 "001cd39c4c70": ["강사님은 이걸 혼합물 반도체라고 했다. 화학쪽이 아니신가본데? 화합물은 화학적인 결합을 이루고 있는 것이다. 혼합물은 물리적으로 섞여 있는 것이다."],
 "001c14841f1b": ["이해가 안돼 이해가 안돼 이해가 안돼 261105"],
 "001c643b9f12": ["그러면 8대 공정에 들어가는데 8대 공정이라고 말하지 않는다는거야? 뭔 말인지는 알겠는데 우리가 이걸 어떻게 아냐고 그렇게 가르치잖아? \\^\\^"],
 "001cbf4d34e9": ["261105(목) 여기서부터 복습 이어서 진행해야됨"],
 "001cd0a6ded2": ["과거를 얘기하는 것이었다면 뭐 ok 아니라면 개소리"],
}
cap4 = {
 1: "판서 — Energy band gap: 에너지 준위(n=1, 2, 3)와 Conduction Band · Valence Band",
 2: "판서 — 반도체의 종류: 용도(Memory / non-Memory)와 구성 성분(Elementals · Compounds · Alloy)",
 3: "판서 — High-K / Low-K와 정전용량 · 저항",
 4: "판서 — 증착 후 생기는 단차 (Step difference, μm 단위)",
 5: "판서 — 반도체 8대 공정 Cycle (Photo · Dry Etch · Ion Implantation · Thin Film Deposition · Diffusion · CMP · Wet Clean)",
 6: "판서 — 패턴 단면과 PR 높이",
 7: "판서 — Aspect Ratio = h / w (PR 구조)",
 8: "판서 — 가시광선 파장 범위 (780 ~ 380)",
 9: "Snell’s Law — 입사광 · 반사광 · 굴절광과 굴절률(n₁, n₂)",
 10: "판서 — ArFi: Air · Water · PR · Wafer의 굴절률",
 11: "판서 — Interference(간섭): 보강간섭과 상쇄간섭",
 12: "판서 — 간섭과 3-Beam Imaging (Condensor 렌즈 · Mask · Projection 렌즈)",
 13: "판서 — Diffraction(회절): Light Source → Mask",
 14: "판서 — Mask 통과 후 회절과 PR Slope",
 15: "판서 — Positive PR 노광 (Mask · PR · A-Film · Wafer)",
}
H2_4 = {
 "실제 훈련)", "실제 훈련) 우문 현답형 질문 (질문 자체는 어리석으나 답은 똑똑하게)",
 "건물 1~30층 짓기", "반도체 공정의 변천사", "Dielectric (유전체)", "[오후 시간]", "Photo 공정", "질문",
}
H3_4 = {
 "1. Conductivity (전기전도도)", "2. Resistivity (비저항)", "3. Energy Band gap",
 "1. Metal", "2. Dielectric", "3. Impurity", "<Nitride의 사용 용도>",
 "1. Conventional (1970~1990 중반) - “과거에는”", "2. Modification (1990년 중반~) - “현재에는”",
 "1. 유전체의 성립조건", "2. 유전체의 역할", "Dielectric Constant (k)",
 "1. Snell’s Law", "회절각", "ArFi", "2. Interference (간섭)", "3. Diffraction(회절)",
 "PR (Photoresist)", "(1) Positive PR", "(2) Negative PR",
}
RENAME_4 = {}
INSERT_4 = [
 ("Q. 반도체 8대 공정이 무엇인가요?", "h2", "반도체 8대 공정"),
 ("중간정리:", "h2", "중간 정리: 단차와 CMP, 공정 Cycle"),
]
items4 = N.parse(N.load_content(SP + "d4_raw.txt"), {"img": 0})
meta4 = json.load(open(SP + "thein_d4_meta.json"))
secs4 = N.Builder(items4, meta4, cap4, {k: [clean_c(c) for c in v] for k, v in cm4.items()},
                  h2=H2_4, h3=H3_4, rename=RENAME_4, insert=INSERT_4, first_title="들어가며", drop_first="들어가며").build()
N.render_page("thein-day4", "더인 교육 4일차", "더인 교육 4일차",
              "더인 교육 4일차: 반도체 정의, 유전체와 Dielectric constant, 8대 공정, Photo 공정(Snell·간섭·회절), PR 정리 노트",
              "날짜: 2026-11-05 · 종류: 교육", "원본: 사용자 노션 필기 (더인 교육 4일차)", secs4)
print("day4 sections:", [(i, t) for i, t, _ in secs4])

# =====================================================================
# 5일차
# =====================================================================
cm5 = {
 "001c23a0ddb7": ["이것도 NUV 처럼 스토리를 만들고 싶으면 정리해라. 그리고 비교해서 설명할 수 있으면 좋다."],
 "001c7105bcb6": ["내 말로 다시 정리하기"],
 "001c93a118ea": ["메모리 반도체를 지원하면 여기 얘기를 해야지, 비메모리 반도체 FinFET 인데 엉뚱하게 설명하면 안된다."],
 "001c0e1ef667": ["이것 그 이후 HDMS 처리와 더불어서 조금 더 생각해서 정리하기"],
 "001cb6aef8dc": ["이거 내 단점이다. 내가 이렇게 하려고 했는데.."],
}
cap5 = {
 1: "판서 — PR과 그 아래 A-Film 구조 (빛이 위에서 입사)",
 2: "판서 — 광원 파장 표시 (436 · 365nm / 248 · 193nm)",
 3: "Photon Energy 식 — E(eV) = 1.24 / λ(μm)",
 4: "EUV(13.5nm)의 Photon Energy 계산 — 약 91.85 eV",
 5: "Photon Energy에 대응하는 온도 — 약 1.066×10<sup>6</sup> K",
 6: "Decomposition by Light — DNQ가 빛을 받아 Carboxylic acid(현상액에 용해)로 변하는 과정 (강의 슬라이드)",
 7: "Dissolution Mechanism — Novolac과 DNQ의 용해 속도 변화, Stone-wall model (KOCW 슬라이드)",
 8: "판서 — 12인치 Wafer 두께 775 μm와 사용 두께 약 100 μm",
 9: "판서 — Amorphous Si · Poly Si · Single Crystal",
 10: "판서 — 노광 장치 개략도(조명·마스크·렌즈·웨이퍼)와 R = k<sub>1</sub>λ / NA",
 11: "판서 — NA = n sinθ 유도 (sinθ ≈ tanθ = r/d)",
 12: "판서 — k<sub>1</sub>을 낮추는 방법: L [OAI] · M [OPC, PSM]",
 13: "판서 — 회로 선폭(Gate to Gate, Metal to Metal)과 Memory / 비Memory 반도체",
 14: "판서 — 반사광에 의한 Standing Wave",
 15: "판서 — 파동으로 본 입사광과 반사광 (Resin · PAC)",
 16: "판서 — 접촉각: 친수성(90° 이하)과 소수성(90° 이상)",
 17: "판서 — Carrier Mobility (NMOS 채널, 전자와 정공)",
 18: "판서 — Dangling bond와 Passivation layer",
 19: "판서 — A 레시피 1000±10Å의 관리도 (USL · UCL · LCL · LSL)",
 20: "조별과제 — SCE, 오옴의 법칙, BJT와 MOSFET, DRAM Read/Write, FLASH MEMORY (강의 슬라이드)",
 21: "Flash 메모리 셀 개략도 (Control gate · Tunnel oxide · N⁺형 소스/드레인 · P형 반도체)",
 22: "Flash 메모리 셀 구조 (Gate · Control gate · Floating gate · Blocking/Tunneling oxide · Source · Drain · P-Substrate, V<sub>th</sub> = 3 V)",
 23: "비휘발성 메모리의 전하 저장 원리 (1) — Erased State와 Read (Erased – ‘ON’)",
 24: "비휘발성 메모리의 전하 저장 원리 (2) — Programming Operation과 Read (Programmed – ‘OFF’)",
 25: "Flash 메모리 셀 Erase (V<sub>G</sub> = V<sub>DD</sub> = −12 V)",
}
H2_5 = {
 "HRR(High Resolution Resist): 흡광계수 (Absorption Coefficient)", "[eV] 단위의 의미부터 짚고 가자",
 "교재 2slide", "Amorphous Si - Poly Si - Single crystal", "회로 선폭의 의미하는 것은?",
 "PEB", "HMDS 처리", "Carrier Mobility", "15Slide", "16 Slide", "대본 (Flash 메모리의 Erase, program에 대해서 설명드리겠습니다.)", "발표 피드백",
}
H3_5 = {
 "1. NUV(Near UV) PR - 436nm G-Line, 365nm I-Line", "2. DUV PR(Deep) - 248, 193nm", "3. EUV PR - 13.5nm",
 "Photon Energy(eV)", "<추가공부 KOCW 261107(토)>",
 "<Memory 반도체>", "<비Memory 반도체>",
 "5Slide", "8Slide", "9Slide", "10Slide", "11Slide", "12Slide", "13Slide",
 "더 구체적인 설명", "기존의 잘못된 관점",
 "주제: FLASH MEMORY의 동작원리(Program/Erase)를 설명하시오.",
 "1. 개요", "2. 구조", "3. 동작원리",
}
RENAME_5 = {}
INSERT_5 = [
 ("1. NUV(Near UV) PR", "h2", "PR의 종류와 구성"),
 ("<Coating>", "h2", "NUV PR의 현상 메커니즘 (Coating → Exposure)"),
 ("NA 에서 Numerical Aperture", "h2", "NA(Numerical Aperture)와 해상도"),
 ("<Memory 반도체>", "h2", "Memory 반도체와 비Memory 반도체"),
 ("5Slide", "h2", "슬라이드별 메모 (5 · 8 · 9 · 10 Slide)"),
 ("NUV 기준으로 설명", "h2", "Soft Bake & Hard Bake"),
 ("11Slide", "h2", "슬라이드별 메모 (11 · 12 · 13 Slide)"),
 ("주제: FLASH MEMORY", "h2", "Presentation (13:20-15:50)"),
]
raw5 = N.load_content(SP + "d5_raw.txt")
# "#### Presentation (13:20-15:50)" 헤더가 원문에 있으므로 삽입 규칙의 Presentation 항목은 제거
INSERT_5 = [e for e in INSERT_5 if not e[0].startswith("주제: FLASH")]
items5 = N.parse(raw5, {"img": 0})
meta5 = json.load(open(SP + "thein_d5_meta.json"))
secs5 = N.Builder(items5, meta5, cap5, {k: [clean_c(c) for c in v] for k, v in cm5.items()},
                  h2=H2_5, h3=H3_5, rename=RENAME_5, insert=INSERT_5, first_title="HRR").build()
N.render_page("thein-day5", "더인 교육 5일차", "더인 교육 5일차",
              "더인 교육 5일차: PR(NUV·DUV·EUV)과 현상 메커니즘, NA와 해상도, Bake·PEB·HMDS, Presentation(FLASH MEMORY)과 피드백 정리 노트",
              "날짜: 2026-11-06 · 종류: 교육", "원본: 사용자 노션 필기 (더인 교육 5일차)", secs5)
print("day5 sections:", [(i, t) for i, t, _ in secs5])
