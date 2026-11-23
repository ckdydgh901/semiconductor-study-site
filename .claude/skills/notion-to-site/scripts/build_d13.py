import sys
sys.path.insert(0, '.')
import build_d101112 as B

cm13 = dict(B.cm12)
cm13["001c6f6e361f"] = ["이건 이렇게 일반론적으로 말할 수 있는건가 싶음"]
cm13["001cb92225f5"] = ["더 디테일하게 어떤 Gas 를 사용했을 때 어떤 부산물이 생기는 데 그 부산물의 m.p이 어떻게 되어서 다마신 공정을 도입하게 되었다. 라고 말할 수 있도록 정리하기"]

cap13 = {}
for k in range(1, 8):
    cap13[k] = B.cap12[k]
cap13[8] = "Claude가 그려준 N-type · P-type 에너지 밴드: E<sub>c</sub> · E<sub>d</sub> · E<sub>F</sub> · E<sub>i</sub> · E<sub>a</sub> · E<sub>v</sub> (Claude 그림 캡처)"
for k in range(8, 40):
    cap13[k + 1] = B.cap12[k]

DESC13 = B.DESC12.replace('더인 교육 12일차', '더인 교육 13일차')
B.build('d13', 'thein-day13', '더인 교육 13일차', '2026-11-19', cm13, cap13, B.H2_12, B.H3_12, [], 'B.D', (), DESC13)
