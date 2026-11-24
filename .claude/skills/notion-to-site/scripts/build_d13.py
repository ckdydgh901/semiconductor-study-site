"""더인 교육 13일차 빌드 (2026-11-24 재동기화).
- 노션 전체를 그대로 옮긴다(맨 위·중간 "B.D" 블록 포함). 사용자가 "개인적인 메모 (여기 내용은 웹사이트에 옮기지 X)"라고 표시한 블록만 뺀다 — 13일차에는 그런 표시가 없다.
- 사용: 작업폴더(scratchpad)에 d13c_raw.txt, d13c_meta.json, d13c/ 가 있는 상태에서 이 폴더에서 실행
"""
import sys
sys.path.insert(0, '.')
import build_d101112 as B
S = B.S

cm13 = dict(B.cm12)
cm13["001c6f6e361f"] = ["이건 이렇게 일반론적으로 말할 수 있는건가 싶음"]
cm13["001cb92225f5"] = ["더 디테일하게 어떤 Gas 를 사용했을 때 어떤 부산물이 생기는 데 그 부산물의 m.p이 어떻게 되어서 다마신 공정을 도입하게 되었다. 라고 말할 수 있도록 정리하기"]

cap13 = {
 1: '판서 — 기체 A · B가 표면에 닿은 뒤 표면을 따라 확산',
 2: '판서 — 400°C 기준 고온·저온 공정 비교: Wafer(Thermal stress)와 Film(Density)의 장단점',
 3: '판서 — FEOL · BEOL 구조 (Contact · Via · ILD · IMD, HARC) (화이트보드 사진)',
 4: '판서 — BEOL / FEOL별 PR strip · 층간절연막(IMD / ILD) · 배선 금속 · FOUP clean 정리표 (화이트보드 사진)',
 5: '판서 — 온도(T)에 따른 저항(R): Metal은 증가, Semi는 감소',
 6: '판서 — Conduction Band(C.B)와 Valence Band(V.B)',
 7: '판서 — p-type과 n-type의 C.B · V.B와 Fermi level(E<sub>F</sub>)',
 8: 'Claude가 그려준 N-type · P-type 에너지 밴드: E<sub>c</sub> · E<sub>d</sub> · E<sub>F</sub> · E<sub>i</sub> · E<sub>a</sub> · E<sub>v</sub> (Claude 그림 캡처)',
 9: '판서 — n-type의 에너지 밴드: C.B 아래의 E<sub>F</sub>와 V.B',
 10: '교재 메모 — 0 K에서 300 K로 올라갈 때 공유결합이 끊어지는 모습과 n<sub>i</sub> = 1.45 × 10<sup>10</sup> (cm³)',
 11: '판서 — Al 배선의 결정립과 결정립계, 결정립이 빠져나가는 모습 (Electromigration)',
 12: 'RC Delay — 배선 저항 R = ρL/(w·h), 커패시턴스 C = ε₀ε<sub>ox</sub>·wL/t<sub>ox</sub>, RC = (ρ/h)·ε₀ε<sub>ox</sub>·L²/t<sub>ox</sub> → 낮은 저항 금속과 낮은 커패시턴스 절연체 필요 (세종대 이원준 교수님 강의 슬라이드 캡처)',
 13: '판서 — Al 배선 공정: Al 패턴 위의 Dielectric과 PR',
 14: '판서 — Cu 다마신 공정: PR 패턴, Dielectric에 식각한 홈과 아래 Metal',
 15: '판서 — 식각한 홈 안쪽에 Barrier Metal과 Cu를 채우는 모습',
 16: '판서 — 식각 부산물의 녹는점: CuCl<sub>2</sub> 1490°C · CuF<sub>2</sub> 1100°C, AlCl<sub>3</sub> 177 · AlF<sub>3</sub> 1291',
 17: '판서 — A-Film 위의 Capping layer와 Compressive stress (Metal 열처리, 14pg)',
 18: '판서 — B/L · W/L과 트랜지스터(G · S · D): 신호는 Metal 배선으로 전달',
 19: '판서 — 깊은 Via 구멍: Not open과 식각 문제',
 20: '판서 — 칩 가장자리의 패드',
 21: '이건희 회장의 프랑크푸르트 선언 — 배경과 핵심 내용 정리 (Claude 답변 캡처)',
 22: '교재 17pg — Metallization: 금속 박막의 요구 조건 (전기적 특성 · 박막 형성 · 신뢰성)',
 23: '판서 — Contact과 Silicide: Ohmic contact',
 24: '판서 — 홈 안에 생긴 Void(단면과 입체)와 저항 R의 식',
 25: '판서 — Dielectric 내부의 Void (절연파괴 관점)',
 26: '교재 18pg — Metallization [Metal Process]: PVD(Evaporation · Sputtering) · CVD · ALD의 종류',
 27: '교재 19pg — PVD · CVD · ALD의 장점과 단점',
 28: '판서 — Step 구조와 Trench (단차 100 Å)',
 29: '판서 — SiO<sub>2</sub> 100 Å 박막 (Bulk 영역)',
 30: '판서 — Heterogeneous / Homogeneous Reaction(Cluster)과 SOD · SOH, ALD (화이트보드 사진)',
 31: '판서 — CF<sub>4</sub> 가스로 SiO<sub>2</sub> 식각: Mask(M) 아래의 SiO<sub>2</sub>와 B-Film',
 32: '판서 — Metal–Semi, Metal–Metal 오믹 컨택: Si + Metal → Silicide(Anneal), Ti / Ni / Co (화이트보드 사진)',
 33: '판서 — Mask와 이온 주입, 0.5 μm 깊이(Junction depth)의 농도 분포와 R<sub>p</sub>',
 34: '판서 — Cell(NMOS)과 Core / Peri의 층별 이온 주입: LDD · S/D · V<sub>th</sub> adjust · Pinch-off · Halo · p-well · Deep well',
 35: '판서 — Cell(NMOS)과 Core / Peri의 층별 이온 주입 (화이트보드 사진)',
 36: '판서 — 트랜지스터의 S / D는 네모가 아니라 점처럼 찍힌 영역',
 37: '판서 — 같은 불순물의 R<sub>p</sub>를 여러 번 중첩해 원하는 깊이(0.1 ~ 0.9 μm)에 주입',
 38: '판서 — 이온 주입 장비: PH<sub>3</sub> → P⁺ 이온 종류, Suppression · Extraction plate, 자기장 질량 분석, Blow-up, Junction depth와 Dose (화이트보드 사진)',
 39: '판서 — 이온 빔의 추출과 자기장 질량 분석(M), 이온 에너지(100 keV)와 Junction depth',
 40: '판서 — Mask에도 이온이 주입되고 아래로 확산되는 모습 (Hard Mask)',
 41: '판서 — Plasma: Ionization Energy · Collision · Ion(+) · Radical · Sheath · Self-bias (화이트보드 사진)',
}

H2_13 = B.H2_12 | S([
    "RC dealy가 무엇인가? (세종대 이원준 교수님)",
    "SOD, SOH → SOG 라는 용어로 많이 사용하는 듯하다.",
])
H3_13 = B.H3_12 | S([
    "ex) 3가 B을 주입한다고 해보자. (P도 마찬가지겠지?)",
    "PH₃(g) → $\mathrm{P}^{+}$",
    "122pg - 사진 추가하기",
])
DESC13 = B.DESC12.replace('더인 교육 12일차', '더인 교육 13일차')

if __name__ == '__main__':
    B.build('d13c', 'thein-day13', '더인 교육 13일차', '2026-11-19', cm13, cap13, H2_13, H3_13, [], 'B.D', (), DESC13)
