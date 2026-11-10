"""사이트 주제 페이지에서 첨자·단위 표기 후보를 찾아 문맥과 함께 출력한다.
사용: python scan_notation.py <topic-id> [<topic-id> ...]      (예: thein-day6 plasma)
출력만 한다(파일을 고치지 않는다). 새 주제면 이 목록을 사용자에게 보여 주고 승인을 받는다.
"""
import os, re, sys, collections

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "topics"))

# (이름, 정규식, 제안) — 제안은 사람이 읽는 힌트일 뿐 자동 치환에는 쓰지 않는다.
PATTERNS = [
    ("화학식 첨자", r"(?<![A-Za-z0-9₀-₉])(?:H2O2?|O2|N2|H2|CO2|CF4|SiF4|SiH4|WF6|SF6|C4F8|NH3|H3PO4|TiO2|Ta2O5|CeO2|Al2O3|ZrO2|HfO2|SiO2|Si3N4|NO2|N2O|BCl3|Cl2|HF2|NF3|CH2F2|CHF3|C2F6)(?![A-Za-z0-9₀-₉])", "아래첨자 (SiO₂ …)"),
    ("이온 위첨자", r"(?<![A-Za-z])(?:Ar|He|N|P|B|As|Si|Ga|F|Cl|O|H)[+-](?![A-Za-z0-9])|\b[NP][+-](?=[로의은는이가를에])", "위첨자 (Ar⁺, N⁺, P⁻ …) — 조사가 바로 붙은 N-로/P-로도 포함"),
    ("마이크로 단위", r"\d[\d.]*\s?um\b|[~-]\d+um\b", "um → μm"),
    ("옹스트롬", r"\b\d{3,5}\s?A\b|\d+\s?\+-\s?\d+A\b", "A → Å"),
    ("mm/nm 의심", r"\d{2,4}\s?mm\b", "파장·선폭이면 nm일 수 있음 — 원문 오류면 고치지 말고 알림"),
    ("eV 등", r"\d[\d.]*\s?(?:ev|EV)\b", "ev → eV"),
    ("지수 ^", r"10\^[-+]?\d+|cm\^2|cm\^-?\d|\bx10\^|\d\^\d", "10⁻³, cm² …"),
    ("F2 면적", r"\b\d+F2\b", "8F² …"),
    ("± 대용", r"\+-|\+/-", "±"),
    ("곱셈/온도", r"\d\s?[xX]\s?10|\d\s?(?:도씨|℃C)|\d\sdegC", "× , ℃ 확인"),
    ("서브스크립트 변수(참고)", r"\bk1\b|\bk2\b|\bV[sd]s\b|\bTox\b|\bCox\b", "k₁ 등 — 관용 표기(Vt, Vth 등)는 건드리지 않는다"),
]
HABIT = "Vt, Vth 같은 관용 표기는 후보에서 제외한다."

for pid in sys.argv[1:]:
    path = os.path.join(ROOT, pid, "index.html")
    s = open(path, encoding="utf-8").read()
    body = re.sub(r"<[^>]+>", " ", s.split('<main id="top"', 1)[1])
    print("==", pid)
    for name, pat, hint in PATTERNS:
        c = collections.Counter(m.group(0) for m in re.finditer(pat, body))
        if not c:
            continue
        print(f"  [{name}] {dict(c)}  → {hint}")
        seen = []
        for m in re.finditer(pat, body):
            ctx = re.sub(r"\s+", " ", body[max(0, m.start() - 16):m.end() + 16]).strip()
            if ctx not in seen:
                seen.append(ctx)
        for ctx in seen[:6]:
            print("      ·", ctx)
print(HABIT)
