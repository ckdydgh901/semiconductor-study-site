import sys, os, re, json, html as H
SC = 'C:/Users/user/OneDrive/바탕 화면/4-2학기/반도체 공부 자료 정리_노션 연동/.claude/skills/notion-to-site/scripts'
sys.path.insert(0, SC)
import notion2site as N
W = 'C:/Users/user/AppData/Local/Temp/claude/a5c06dd2006c0365/dd153eae-432a-40b1-9b24-1fff828e8940/scratchpad/'

def clean_c(s): return re.sub(r"(<br\s*/?>)+\s*$", "", s)

def S(xs):
    return {N.plain(N.inline(N.tex_inline(x).replace('</b><b>', ''))) for x in xs}

def _multi(m):
    urls = m.group(1).split(',')
    out = f'<span discussion-urls="{urls[0]}">{m.group(2)}</span>'
    for u in urls[1:]:
        out += f'<span discussion-urls="{u}"></span>'
    return out

def load(tag, drop_exact=()):
    out = []
    for l in N.load_content(W + f'{tag}_raw.txt'):
        if l.strip() in drop_exact: continue
        l = N.tex_inline(l).replace('</b><b>', '')
        l = re.sub(r'<span color="[a-z_]+" (discussion-urls="[^"]+")>', r'<span \1>', l)
        l = re.sub(r'<span discussion-urls="([^",]+(?:,[^"]+)+)">(.*?)</span>', _multi, l)
        out.append(l)
    return out

def ctxfix(b):
    b = b.replace('대상: “”', '대상: “Q. 플라즈마가 무엇인가요?”')
    return re.sub(r'<p class="cmt-ctx">.*?</p>', lambda m: m.group(0).replace('\\~', '~'), b)

def add_q_breaks(items):
    out = []; first = True
    for it in items:
        if it[0] == 'line' and re.match(r'^Q\d{0,2}\.', N.plain(N.inline(it[1]))) and not first:
            out += [('sp',), ('sp',)]
        out.append(it); first = False
    return out

def build(tag, pid, title, date, cm, cap, h2, h3, ins, first_title, drop_exact, desc):
    items = add_q_breaks(N.parse(load(tag, drop_exact), {"img": 0}))
    meta = json.load(open(W + f'{tag}_meta.json'))
    n_img = sum(1 for it in items if it[0] == 'img') + sum(len(ids) for it in items if it[0] == 'imgcols' for ids in it[1])
    assert len(meta) == n_img, (len(meta), n_img)
    assert sorted(cap) == list(range(1, len(meta) + 1)), (sorted(cap)[:3], len(cap))
    b = N.Builder(items, meta, cap, {k: [clean_c(c) for c in v] for k, v in cm.items()},
                  h2=h2, h3=h3, rename={}, insert=ins, first_title=first_title, drop_first=None)
    secs = [(i, t, ctxfix(x)) for i, t, x in b.build()]
    unused = set(cm) - b.used_cmt
    if unused: print('!! unused comments:', sorted(unused))
    N.render_page(pid, title, title, desc, f"날짜: {date} · 종류: 교육", f"원본: 사용자 노션 필기 ({title})", secs)
    print(pid, 'sections:', len(secs), [(i, t) for i, t, _ in secs])

# ============================================================ 10일차
cm10 = {
 "001ce40a4850": ["강사님이 면접관이라면 이렇게 답하길 원한다라는 말"],
 "001c0f26369a": ["여기 내용 조금 찾아보기 "],
 "001c4916a028": ["이런 지식이 툭툭 머릿속에서 튀어 나와야 함"],
 "001c992b80ca": ["반도체하는데 이걸 모르면 안되지"],
 "001c369b26eb": ["이런거 별거 아니니까 외워두자"],
 "001c9a46cd8b": ["다시 확인해보기"],
 "001c335c7ad1": ["천천히 그리면서 이해하기"],
 "001c5309452b": ["다시 책 보고 확인하기"],
 "001c002afe61": ["예?"],
 "001c5bb77a7c": ["여기 내용 놓쳤음"],
}
cap10 = {
 1: "HKMG — 문턱전압과 게이트 일함수, Fermi level pinning과 NMOS·PMOS용 금속 (설명 캡처)",
 2: "왕복 다차선 고속도로 사진 — Q8 비유",
 3: "판서 — 적층한 칩을 수직으로 관통하는 TSV",
 4: "부르즈 칼리파 사진 — Q9 수직 적층 비유",
 5: "판서 — Cell Array 주변의 Peri 영역과 Input / Output",
 6: "판서 — Cell Array · Peri(1.5 V)와 Input/Output Circuit(2.5 / 3.3 V)",
 7: "판서 — Cell Array 아래에 I/O를 배치한 적층 구조",
 8: "판서 — 칩 가장자리의 패드: V<sub>DD</sub> · V<sub>SS</sub> · Input · Output",
 9: "판서 — 노이즈로 흔들리는 V<sub>DD</sub>(1.5 V)와 V<sub>SS</sub>(0 V)",
 10: "판서 — DRAM 셀 회로 (W.L, 트랜지스터, Storage와 Cap)",
 11: "DRAM 단면 SEM — Capacitor stack · Bitline · Wordline transistors",
 12: "판서 — NAND Flash 셀의 직렬 연결 회로 (정보를 저장하는 트랜지스터 표시)",
 13: "판서 — 원형 Wafer 위의 Die와 Scribe line, 위치별 측정 지점",
 14: "교재 29pg — Doping 농도와 온도에 따른 Fermi level 변화",
 15: "교재 — 반도체 내부 소재 (트랜지스터 단면 ①~⑧: Doped Silicon · Doped Poly Silicon · Gate Oxide · Side Wall Spacer · 보호막 SiN · Silicide · Contact · ILD)",
 16: "판서 — MOSFET의 회로 기호 · 레이아웃 · 단면 (G, S, D, B)",
 17: "판서 — 10 V 전원과 5 Ω · 10 Ω 직렬 저항, V<sub>x</sub> 구하기 (I<sub>1</sub> = I<sub>2</sub> = I<sub>3</sub>)",
 18: "판서 — NMOS: 드레인 5 V, 게이트 5 V, V<sub>th</sub> = 1 V, 소스 쪽 V<sub>x</sub>와 커패시터",
 19: "판서 — 게이트 전압을 바꿔 가며 구한 V<sub>x</sub>",
 20: "PN 접합 — Zero bias · Reverse bias · Forward bias의 공핍 영역과 에너지 밴드 (교재)",
 21: "판서 — PN Diode 기호",
 22: "판서 — PN 접합 단면 (p형 / n형)",
 23: "판서 — PN 접합의 레이아웃 (p-well 안의 N⁺ 영역과 Contact)",
 24: "교재 — Inverter 동작원리: NMOS · PMOS 단면과 레이아웃 (V<sub>DD</sub> · GND · Input · Output)",
 25: "판서 — CMOS Inverter: PMOS는 charging, NMOS는 discharging",
 26: "판서 — 출력 파형의 Rising / Pulling",
}
H2_10 = S([
 "Quiz (이 정도는 면접에서 물어볼 수 있다 - 반도체 상식)", "보충 설명", "교재", "강사님 딴소리",
 "반도체 소재", "페르미 준위", "절연체와 유전체의 늬양스 차이", "Transistor Length", "Capacitor", "기생 커패시터",
 "PN 접합의 원리", "MOS", "C-V 커브", "문턱전압", "CMOS Inverter 에 Photo mask가 몇 장이 필요할지 맞추기",
])
H3_10 = S([
 "HBM", "왜 수율 차이가 많이 나오는가?", "반도체란?", "반도체의 역할", "Wafer 구조", "Scribe line 구성요소 ",
 "반도체 칩/제품", "시스템 반도체", "DRAM", "Flash 메모리", "\\<훈련> 선배님이 시키셨던 것들",
 "Wafer에서 전기적인 특성을 측정해보면?", "문제를 찾아가는 과정", "(1) $V=IR$", "(2) MOSFET의 원리",
 "Zener Diode", "PN Diode",
])
DESC10 = ('더인 교육 10일차: 반도체 상식 Quiz(HKMG·SoC/SiP/Chiplet·HBM·수직 적층 NAND·Planar/Fin/GAA), 교재 정리(Wafer 구조·Scribe line·DRAM·Flash), '
          '페르미 준위, 옴의 법칙·MOSFET 원리·PN 접합·MOS·CMOS Inverter 정리 노트')

# ============================================================ 11일차
cm11 = {
 "001c8b215678": ["왓??"],
 "001c60eb829a": ["채널에 대한 얘기인데 불순물과 관련? 아 P type 기판에? "],
 "001ca14a916f": ["여기는 따로 천천히 이해하면서 정리해보자"],
 "001cc670c387": ["Diffusion node라는게 뭔지 모르겠어"],
 "001cff5518bc": ["이걸 그래서 어디에 Source랑인지 뭔지 P-type 기판이랑 어디를?"],
 "001c212dbda4": ["조금 더 말을 깔끔하게 정리했으면 좋겠다"],
 "001cf9dac9cf": ["이거 솔직히 모르잖아. 다시 공부하면서 정리하자"],
}
cap11 = {
 1: "판서 — 온도 상승(T↑)에 따른 V<sub>th</sub>(↓) · I<sub>dsat</sub>(↓) · I<sub>off</sub>(↑)",
 2: "판서 — 온도 변화에 따른 준위 그래프 (진성 준위를 가운데 두고 위·아래 준위가 모이는 방향, 파란 화살표)",
 3: "판서 — I<sub>Dsat</sub> 포화 전류 곡선 (온도가 올라가면 점선 쪽으로 감소)",
 4: "CIS(CMOS Image Sensor) 칩 사진",
 5: "판서 — 아날로그 신호를 샘플링·양자화해 코딩하는 과정 (V–t)",
 6: "FSI · BSI CIS 구조 — Lenses · Color filters · Multi-layer wiring · Photodiodes",
 7: "SRAM 작동 원리와 단위 셀 구조 — 인버터 2개와 M<sub>1</sub>~M<sub>6</sub> (SK hynix 뉴스룸)",
 8: "판서 — ROM 셀 배열 (B/L 1·2, W/L 1·2와 트랜지스터)",
 9: "판서 — NAND: B.L 하나에 직렬로 연결된 셀과 Diffusion 영역",
 10: "판서 — NOR: 비트라인과 워드라인의 교차점에 만든 셀",
 11: "판서 — Flash Write: F/G에 전자가 들어가면 문턱전압이 우측으로, 빠지면 좌측으로 이동",
 12: "교재 130pg — Flash의 Write 동작 (Program / Erase, Hot Carrier Injection과 FN Tunneling)",
 13: "판서 — NAND 셀의 직렬 연결 (맨 처음 트랜지스터만 기호가 다름)",
 14: "판서 — Short Channel Effect: channel 길이 L과 Hot carrier의 Trap (n⁺ 영역)",
}
H2_11 = S([
 "각각이 온도에 영향을 왜 받는지, 영향을 받는다면 왜 영향을 받는지 공부하기", "메모리와 비메모리 반도체", "사업특성 구분",
 "스마트폰 반도체 부품", "메모리의 층위", "SRAM (Static RAM)", "DRAM (Dynamic RAM) - 117pg", "DRAM Capacitor 구조 발전",
 "HBM", "비메모리 반도체의 변천사", "NAND vs NOR", "Flash Write 동작", "Speed와 Density, 비휘발성", "Transistor",
 "Short Channel Effect", "기술의 동향", "EDS 공정", "반도체 스터디",
])
H3_11 = S([
 "(1) 문턱 전압", "(2) $I_{Dsat}$", "(3) $I_{off}$", "Low $V_{CC}$ margin", "AP", "CIS", "PMIC (Power Management Intergrated Circuit)",
 "DDI (Display Driver IC)", "ADC와 DAC", "(1) Refresh", "(2) Write 동작", "(3) Read 동작", "각각의 과정에 대한 설명",
 "Pre-charge → Charge Sharing → Sensing Amp → Restore 동작", "(1) Pre-charge", "123pg 예제", "125pg ",
 "(1) ROM", "(2) EPROM", "(3) EEPROM", "(4) Flash Memory", "\\[스터디 방식\\]",
])
DESC11 = ('더인 교육 11일차: 온도에 따른 문턱전압·I_Dsat·I_off, 메모리·비메모리 반도체(SRAM·DRAM Read 동작·ROM·EPROM·EEPROM·Flash), '
          '스마트폰 반도체 부품(AP·CIS·PMIC·DDI), Short Channel Effect, 반도체 스터디 질문 정리 노트')

# ============================================================ 12일차
cm12 = {
 "001cbfce5d55": ["혼자 공부하면서 정리하기"],
 "001c64667b9d": ["이해가 안되네 진성일 때는 확률이고 나머지는 실제 준위라는 거면 Ea랑 Ed는?"],
 "001cbec1c347": ["책 다시 펴고 녹는점, 사용 gas 차분하게 정리하고 천천히 찾아보기"],
 "001c57310a39": ["걍 반응성이 높다고 퉁치면 안되나?"],
 "001cfdf8f591": ["녹는점이 높으면 못날려서 그런거지? 부산물도 없애야하는데 못없애서 문제가 생기는거야?"],
 "001c678bb334": ["여기를 쫙 말할 수 있어야겠지?"],
 "001cfd9b6bff": ["이 생각 꼭 내걸로 만들기"],
 "001c6a3ce32c": ["그림을 보면서 다시 확인해보자"],
 "001c01fab301": ["설명이 조금 이상한데? 비정질이라고 공간이 비어 있는건 아니잖아.."],
 "001c58f38441": ["와 이런거였네 ;;"],
 "001ce252c386": ["I-V Curve에 대한 얘기, Saturation이 생기고 그렇게 되는게 해당 영역에 의해 결정되고 동작할 수 있다."],
 "001c2b5a65ad": ["소자 수업에서 제대로 못 듣고 넘어갔던 동작 특성에 대해서 세종대 교수님 수업을 들으면서 복습할 때 오늘 배웠던 내용들을 생각하면서 공부하자. 연결지으면서"],
 "001c4ccede9e": ["아마 예비군 수업 때일 듯 사진 확인하기"],
 "001c10062dea": ["공부하고 정리 노트 만들 때 이런 느낌으로 정리하기"],
 "001caffd3cff": ["답변을 할 때 글을 그대로 읽지 말고 말하듯이 설명해라. 지금 적힌 것은 문어체이고, 구어체로 반드시 다시 정리하기"],
 "001c704f52e6": ["솔직히 몰랐음 알았으면 말로 나왔겠지"],
 "001cdab7553e": ["이런걸 생각할 수 있어야 한다고"],
 "001cce7c5ddc": ["아 과학 인물 100인 책 다시 빌려야하는데.."],
}
cap12 = {
 1: "판서 — 기체 A · B가 표면에 닿은 뒤 표면을 따라 확산",
 2: "판서 — 400°C 기준 고온·저온 공정 비교: Wafer(Thermal stress)와 Film(Density)의 장단점",
 3: "판서 — FEOL · BEOL 구조 (Contact · Via · ILD · IMD, HARC) (화이트보드 사진)",
 4: "판서 — BEOL / FEOL별 PR strip · 층간절연막(IMD / ILD) · 배선 금속 · FOUP clean 정리표 (화이트보드 사진)",
 5: "판서 — 온도(T)에 따른 저항(R): Metal은 증가, Semi는 감소",
 6: "판서 — Conduction Band(C.B)와 Valence Band(V.B)",
 7: "판서 — p-type과 n-type의 C.B · V.B와 Fermi level(E<sub>F</sub>)",
 8: "판서 — n-type의 에너지 밴드: C.B 아래의 E<sub>F</sub>와 V.B",
 9: "교재 메모 — 0 K에서 300 K로 올라갈 때 공유결합이 끊어지는 모습과 n<sub>i</sub> = 1.45 × 10<sup>10</sup> (cm³)",
 10: "판서 — Al 배선의 결정립과 결정립계, 결정립이 빠져나가는 모습 (Electromigration)",
 11: "판서 — Al 배선 공정: Al 패턴 위의 Dielectric과 PR",
 12: "판서 — Cu 다마신 공정: PR 패턴, Dielectric에 식각한 홈과 아래 Metal",
 13: "판서 — 식각한 홈 안쪽에 Barrier Metal과 Cu를 채우는 모습",
 14: "판서 — 식각 부산물의 녹는점: CuCl<sub>2</sub> 1490°C · CuF<sub>2</sub> 1100°C, AlCl<sub>3</sub> 177 · AlF<sub>3</sub> 1291",
 15: "판서 — A-Film 위의 Capping layer와 Compressive stress (Metal 열처리, 14pg)",
 16: "판서 — B/L · W/L과 트랜지스터(G · S · D): 신호는 Metal 배선으로 전달",
 17: "판서 — 깊은 Via 구멍: Not open과 식각 문제",
 18: "판서 — 칩 가장자리의 패드",
 19: "이건희 회장의 프랑크푸르트 선언 — 배경과 핵심 내용 정리 (Claude 답변 캡처)",
 20: "교재 17pg — Metallization: 금속 박막의 요구 조건 (전기적 특성 · 박막 형성 · 신뢰성)",
 21: "판서 — Contact과 Silicide: Ohmic contact",
 22: "판서 — 홈 안에 생긴 Void(단면과 입체)와 저항 R의 식",
 23: "판서 — Dielectric 내부의 Void (절연파괴 관점)",
 24: "교재 18pg — Metallization [Metal Process]: PVD(Evaporation · Sputtering) · CVD · ALD의 종류",
 25: "교재 19pg — PVD · CVD · ALD의 장점과 단점",
 26: "판서 — Step 구조와 Trench (단차 100 Å)",
 27: "판서 — SiO<sub>2</sub> 100 Å 박막 (Bulk 영역)",
 28: "판서 — Heterogeneous / Homogeneous Reaction(Cluster)과 SOD · SOH, ALD (화이트보드 사진)",
 29: "판서 — CF<sub>4</sub> 가스로 SiO<sub>2</sub> 식각: Mask(M) 아래의 SiO<sub>2</sub>와 B-Film",
 30: "판서 — Metal–Semi, Metal–Metal 오믹 컨택: Si + Metal → Silicide(Anneal), Ti / Ni / Co (화이트보드 사진)",
 31: "판서 — Mask와 이온 주입, 0.5 μm 깊이(Junction depth)의 농도 분포와 R<sub>p</sub>",
 32: "판서 — Cell(NMOS)과 Core / Peri의 층별 이온 주입: LDD · S/D · V<sub>th</sub> adjust · Pinch-off · Halo · p-well · Deep well",
 33: "판서 — Cell(NMOS)과 Core / Peri의 층별 이온 주입 (화이트보드 사진)",
 34: "판서 — 트랜지스터의 S / D는 네모가 아니라 점처럼 찍힌 영역",
 35: "판서 — 같은 불순물의 R<sub>p</sub>를 여러 번 중첩해 원하는 깊이(0.1 ~ 0.9 μm)에 주입",
 36: "판서 — 이온 주입 장비: PH<sub>3</sub> → P⁺ 이온 종류, Suppression · Extraction plate, 자기장 질량 분석, Blow-up, Junction depth와 Dose (화이트보드 사진)",
 37: "판서 — 이온 빔의 추출과 자기장 질량 분석(M), 이온 에너지(100 keV)와 Junction depth",
 38: "판서 — Mask에도 이온이 주입되고 아래로 확산되는 모습 (Hard Mask)",
 39: "판서 — Plasma: Ionization Energy · Collision · Ion(+) · Radical · Sheath · Self-bias (화이트보드 사진)",
}
H2_12 = S([
 "B.D", "들어가며", "Metal 공정", "정리하자", "Metal의 Work function을 공부해보자",
 "Al 을 사용하다가 Cu를 사용하게 된 이유 (다마신 공정을 설명하기 위해)", "Al 배선 공정 (한 번 짚고 넘어가자)", "Cu 다마신 공정",
 "Cu etch에 대한 얘기", "Metal 을 열처리 했을 때 (14pg)", "금속 배선의 역할", "패드란?", "과거의 수율과 지금의 수율",
 "R! PR의 사용조건", "금속의 박막 조건", "PVD 공정", "CVD 공정", "ALD 공정", "PVD vs CVD vs ALD", "SOD, SOH",
 "다시 내 말로 정리해보기", "$\\mathrm{SiO_2}$를 CF4 gas로 etch 하는 메커니즘", "SiO₂를 CF₄ gas로 etch 하는 메커니즘",
 "결국에 다양한 Metal과 Semi, Metal과 Metal 사이에 오믹 컨택을 어떻게 시키는지에 대한 얘기이다.",
 "Ion Implantatiion", "메모리 반도체", "R! PR Mask의 용도", "Mask는 이온주입시에 Mask 자체도 이온주입이 된다!",
 "Vacuum (진공): 기체 분자수의 감소", "플라즈마를 사용하는 공정은 다시 생각해봐야한다?", "스터디",
])
H3_12 = S([
 "(1) Conventional (과거에는)", "(2) Modification (현재에는)", "Diffusion", "CVD", "BEOL", "반도체에서 400°C 기준이 저온 고온 공정의 개념",
 "122pg", "123pg", "124pg", "125pg", "126pg", "132pg", "133pg", "136pg", "137pg", "140pg", "144pg",
 "(1) Deep Junction - 확산", "(2) Shallow Junction - 이온 주입", "Ion Implantation에서 사용하는 용어 정리",
 "Si 격자 크기 - 암기하기!", "Si-Si 활성화 에너지 (Bonding이 끊어지는 에너지) - 암기하기!", "계산 (100 기준)", "정리",
 "ex) 3가 B⁺을 주입한다고 해보자. (P도 마찬가지겠지?)", "PH₃(g) → P⁺", "P나 H 중에 +를 갖고 있는 모든 애들의 거동",
 "(1) SiO₂ - Ga/Al Impurity", "(2) Si₃N₄", "내 말로 정리", "RF Bias를 걸었을 때 Self bias가 걸리는 메커니즘",
 "플라즈마 내에서의 Mobility",
])
DESC12 = ('더인 교육 12일차: Diffusion과 CVD의 변천, Metal 배선(Contact·Via, Al→Cu 다마신 공정), PVD·CVD·ALD 비교, 오믹 컨택(Silicide), '
          '이온 주입(Rp·Dose·하드마스크), 플라즈마·Sheath·Self bias, 진공도 분류 정리 노트')

if __name__ == '__main__':
    which = sys.argv[1]
    if which == '10':
        build('d10', 'thein-day10', '더인 교육 10일차', '2026-11-16', cm10, cap10, H2_10, H3_10, [], '들어가며', ('<b>들어가며</b>',), DESC10)
    elif which == '11':
        build('d11', 'thein-day11', '더인 교육 11일차', '2026-11-17', cm11, cap11, H2_11, H3_11, [], '온도에 따른 소자 특성', (), DESC11)
    else:
        build('d12', 'thein-day12', '더인 교육 12일차', '2026-11-19', cm12, cap12, H2_12, H3_12, [], 'B.D', (), DESC12)
