"""더인 교육 16일차 빌드 (2026-11-24 추가). 노션 맨 위의 "개인적인 메모 (여기 내용은 웹사이트에 옮기지 X)" 블록(번호 목록 11개)은 사용자 표시대로 옮기지 않는다 —
d16_raw.txt는 그 블록을 뺀 채로 만든 것이다."""
import sys, re
sys.path.insert(0, '.')
import build_d101112 as B
import build_generic as G
S = B.S
raw = open(B.W + 'd16_raw.txt', encoding='utf-8').read()
bold = [m.group(1) for m in re.finditer(r'^<b>(.*?)</b>\s*$', raw, re.M)]
H2 = S(bold)
H3 = S(["(1) planar 2D", "(2) 3D 소자 식각", "(1) 200mm FAB", "(3) 300mm", "1. Relief 밸브", "2. Air Regulator", "열전달", "1. 전도", "2. 대류", "3. 복사",
        "예전 200mm system (사람이 했던 시대)", "1. Gas", "(1) PVD", "(2) CVD", "2. Liquid"])
H2 = H2 - H3
cm = {"001c693a56df": ["이런 관점 배워가기"]}
cap = {1: "판서 — Gas 주입·배출 제어 설명 스케치", 2: "판서 — Wafer 가장자리 10 mm 영역(Edge · Bevel) 스케치"}
DESC = ('더인 교육 16일차: Etch 장비·소재·공정기술(극저온 Etch, 200mm/300mm 진공 Chamber, EFEM·Load Lock), Process Chamber 구성(ESC·Gas·MFC·Shower Head), '
        'Plasma·ICP, Etch 진단(OES·EOP), 진공 펌프·Chiller·Scrubber, Ashing·Bevel Etch, 이온주입·RTP, Thin Film(CVD·PVD·ALD) 정리 노트')
if __name__ == '__main__':
    G.build_page('d16', 'thein-day16', '더인 교육 16일차', '16일차', '2026-11-23', '교육', cm, cap, H2, H3, [], '들어가며', ('<b>들어가며</b>',), DESC)
