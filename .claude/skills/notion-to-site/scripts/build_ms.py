"""기초반도체공학 김성호 교수님 MS 접합 빌드 (2026-11-24 추가)."""
import sys
sys.path.insert(0, '.')
import build_d101112 as B
import build_generic as G
S = B.S
cap = {
 1: "Junction(contact) — Homo-Junction(pn)과 Hetero-Junction(Schottky, Metal-silicon junction), 다이오드 기호와 바이어스 회로 (강의 영상 캡처)",
 2: "Metal-semiconductor contacts — Schottky Barrier(정류, pn diode와 유사)와 Ohmic Contact의 I–V 곡선 (강의 영상 캡처)",
 3: "About metal — Energy bandgap = 0 eV, 금속 안의 excess carrier는 즉시 재결합 (반도체와 금속의 밴드 비교) (강의 영상 캡처)",
 4: "Metal-semiconductor contacts — Workfunction(eφ<sub>m</sub>, eφ<sub>s</sub>)과 Electron affinity qχ, φ<sub>M</sub> > φ<sub>S</sub> (강의 영상 캡처)",
}
H2 = S([r"(1) Workfunction ($e\phi_m$, $e\phi_s$)", "(2) Electron Affinity"])
DESC = '기초반도체공학 김성호 교수님 [3.1] MS접합: Schottky contact와 Ohmic contact, 정류작용, 금속의 밴드(Eg = 0), Workfunction과 Electron Affinity 정리'
if __name__ == '__main__':
    G.build_page('ms', 'ms-junction', '기초반도체공학 김성호 교수님 MS 접합', 'MS 접합', '2026-11-21', '강의', {}, cap, H2, set(), [], 'MS 접합 (유튜브 강의)', (), DESC,
                 source='원본: 사용자 노션 필기 (기초반도체공학 김성호 교수님 MS 접합) · 영상: 기초반도체공학 3.1 MS접합')
