/*
 * 영역(areas)과 주제(topics) 목록 — 상단 탭, 하위 탭, 홈 화면의 유일한 원본입니다.
 *
 * [영역 areas]  사이트를 나누는 큰 칸. 상단 탭에 그대로 나타납니다.
 *   id    : 영문 소문자 (topics의 area 값과 같아야 함)
 *   name  : 탭에 표시되는 이름
 *   desc  : 홈 화면에서 영역 제목 아래에 표시되는 설명
 *   (주제가 하나도 없는 영역도 탭과 홈 섹션이 만들어지고 "준비 중"으로 표시됩니다)
 *
 * [주제 topics]  새 주제를 추가하면 배열 맨 끝에 항목 하나만 더하면 됩니다.
 *   id       : 폴더 이름 (topics/<id>/index.html). 영문 소문자·숫자·하이픈
 *   area     : 어느 영역에 속하는지 (areas의 id)
 *   title    : 홈 카드 제목
 *   short    : 하위 탭에 표시되는 짧은 이름 (선택, 없으면 title)
 *   category : 카드 위쪽 작은 분류 글자 (예: "DRAM 공정", "단위 공정")
 *   summary  : 홈 카드에 표시되는 한두 줄 설명
 *   tags     : 검색용 키워드 배열
 *   date     : 노션 "날짜" 속성 (YYYY-MM-DD). 홈 카드 표시·정렬 기준(오래된 순). 노션 원본이 없으면 생략
 *   updated  : 사이트를 마지막으로 수정한 날 (YYYY-MM-DD). 주제 페이지 하단에 표시
 *   notion   : 노션 원본 링크 (선택). 있으면 주제 페이지 하단에 링크가 표시됨
 */
window.SITE = {
  name: "나의 공부 공간",
  areas: [
    {
      id: "study",
      name: "반도체 공부",
      desc: "Dr.Sammy 영상 등으로 내가 따로 공부한 반도체 공정·소자 내용"
    },
    {
      id: "news",
      name: "반도체 시사",
      desc: "반도체 업계 뉴스와 시사 이슈를 공부한 기록"
    },
    {
      id: "thein",
      name: "더인 교육",
      desc: "더인 반도체 교육을 들으며 공부한 내용"
    },
    {
      id: "notes",
      name: "반도체 정리노트",
      desc: "Word 등으로 따로 정리한 반도체 질문·답변 노트와 연습 (더인 교육 내용만 담지 않는 모음)"
    }
  ],
  topics: [
    {
      id: "dram-feol",
      area: "study",
      title: "10nm급 DRAM FEOL 공정 정리",
      short: "DRAM FEOL 공정",
      category: "DRAM 공정",
      summary: "Isolation(STI)부터 Well, Vt 조정, BCAT 셀 트랜지스터, Peri 트랜지스터(LDD·Halo)까지 FEOL 전 과정을 1부·2부 통합으로 정리한 노트.",
      tags: ["DRAM", "FEOL", "STI", "Well", "BCAT", "RCAT", "LDD", "Halo", "CMP", "임플란트", "Vt"],
      date: "2026-09-18",
      updated: "2026-11-07",
      notion: "https://app.notion.com/p/3de6b8b7c6bb80aa8684d24c5f1e2c0e"
    },
    {
      id: "dram-meol",
      area: "study",
      title: "10nm급 DRAM MEOL 공정 정리",
      short: "DRAM MEOL 공정",
      category: "DRAM 공정",
      summary: "ILD1·Direct Contact·W 플러그·Bit Line(Air gap)·Landing Pad까지와, Mold·Supporter·하부전극·High-k·상부전극으로 이어지는 캐패시터 형성 과정을 정리한 노트.",
      tags: ["DRAM", "MEOL", "Bit Line", "Capacitor", "Landing Pad", "Air gap", "ILD", "High-k", "ZAZ", "Supporter", "텅스텐"],
      date: "2026-10-29",
      updated: "2026-11-07",
      notion: "https://app.notion.com/p/4086b8b7c6bb80fc9ff8ddb40c429b10"
    },
    {
      id: "dram-beol",
      area: "study",
      title: "10nm급 DRAM BEOL 공정 정리",
      short: "DRAM BEOL 공정",
      category: "DRAM 공정",
      summary: "PMD 증착과 단차 해소, M1(W)·M2/M3(Cu 듀얼 다마신)·M4(Al) 배선, Trench first vs Via first, Passivation과 Micro bump까지 정리한 노트.",
      tags: ["DRAM", "BEOL", "PMD", "M1C", "Dual Damascene", "Cu", "IMD", "low-k", "Passivation", "Bump", "Via"],
      date: "2026-10-30",
      updated: "2026-11-07",
      notion: "https://app.notion.com/p/4096b8b7c6bb80ec9157c9556557d948"
    },
    {
      id: "plasma",
      area: "study",
      title: "플라즈마와 식각 정리",
      short: "플라즈마",
      category: "단위 공정",
      summary: "DC/RF 플라즈마, Sheath와 이온 충돌, RIE의 비등방성 식각 원리에서 HDP(ICP·ECR), DRIE(Bosch), ALE, Cryogenic·펄스 플라즈마까지 정리한 노트.",
      tags: ["플라즈마", "식각", "Etch", "RIE", "CCP", "ICP", "ECR", "Sheath", "Bosch", "ALE", "Cryogenic", "HARC"],
      date: "2026-10-28",
      updated: "2026-11-07",
      notion: "https://app.notion.com/p/4076b8b7c6bb80028ea4ccfe497f3e95"
    },
    {
      id: "cmp",
      area: "study",
      title: "CMP(화학기계연마) 정리",
      short: "CMP",
      category: "단위 공정",
      summary: "CMP가 필요한 이유(DOF), 화학+기계 원리와 Preston 방정식, 장비·패드·엔드포인트, 슬러리, Dishing·Erosion 등 결함과 공정 통합까지 정리한 노트.",
      tags: ["CMP", "평탄화", "슬러리", "Preston", "Dishing", "Erosion", "DOF", "패드", "컨디셔너", "엔드포인트"],
      date: "2026-10-31",
      updated: "2026-11-07",
      notion: "https://app.notion.com/p/40a6b8b7c6bb80878cc4d032dd3d865d"
    }
    ,{
      id: "kocw-oxidation",
      area: "study",
      title: "KOCW 세종대 이원준 교수님 — SiO₂와 Oxidation 정리",
      short: "KOCW 산화",
      category: "KOCW 강의",
      summary: "KOCW 세종대 이원준 교수님 강의(SIO 02 & OXIDATION 01): 산화막의 종류와 용도(LOCOS·Pad·Sacrificial·Gate), 산화 메커니즘, Dry vs Wet, Deal-Grove 모델의 Flux(F₁·F₂·F₃)를 정리한 노트. (Oxidation2 15분까지 시청)",
      tags: ["KOCW", "산화", "Oxidation", "SiO2", "LOCOS", "Pad oxide", "Gate oxide", "Dry", "Wet", "Deal-Grove", "Flux", "RCA Clean"],
      date: "2026-11-07",
      updated: "2026-11-09",
      notion: "https://app.notion.com/p/4116b8b7c6bb80c098f1e9b9c842db40"
    }
    ,{
      id: "kocw-etching",
      area: "study",
      title: "KOCW 세종대 이원준 교수님 — Etching 정리",
      short: "KOCW 식각",
      category: "KOCW 강의",
      summary: "KOCW 세종대 이원준 교수님 Etching 강의(01~03): 플라즈마와 Etch 기초, Etch Rate·균일도·선택비·이방성, Loading Effect, Wet Etch와 Etchant, PE·SE·RIE, ICP·ECR·HWP, ESC·세라믹 부품, 에칭 가스를 정리한 노트.",
      tags: ["KOCW", "Etching", "식각", "Wet Etch", "Dry Etch", "RIE", "ICP", "ECR", "HWP", "ESC", "Loading Effect", "선택비", "이방성", "플라즈마"],
      date: "2026-11-09",
      updated: "2026-11-10",
      notion: "https://app.notion.com/p/4136b8b7c6bb801b8d20c5c72fab4480"
    },
    {
      id: "thein-day1",
      area: "thein",
      title: "더인 교육 1일차 정리",
      short: "1일차",
      category: "더인 교육",
      summary: "오리엔테이션·팀 스터디, 반도체 역사, HBM·미세화·기술 방향, FinFET/GAA, Photo 공정 맛보기, 메모리/비메모리, Wafer, Particle 예습과 수업 질문(EUV 확률적 결함 등)을 정리한 노트.",
      tags: ["더인 교육", "1일차", "반도체 역사", "HBM", "미세화", "EUV", "FinFET", "GAA", "Wafer", "Particle", "수율"],
      date: "2026-11-02",
      updated: "2026-11-07",
      notion: "https://app.notion.com/p/40b6b8b7c6bb801ebb44d081e95a8fbd"
    },
    {
      id: "thein-day2",
      area: "thein",
      title: "더인 교육 2일차 정리",
      short: "2일차",
      category: "더인 교육",
      summary: "FOUP·OHT·AGV, ESD, Particle, 반도체 구조와 계측 장비, Ge vs Si, N/P-type, 유전체·유전상수, Capacitor, RC delay, 단결정 성장, SiO₂ 산화(Deal-Grove)를 정리한 노트.",
      tags: ["더인 교육", "2일차", "FOUP", "ESD", "Particle", "유전상수", "High-k", "Low-k", "초크랄스키", "산화", "Deal-Grove"],
      date: "2026-11-03",
      updated: "2026-11-07",
      notion: "https://app.notion.com/p/40d6b8b7c6bb8098af83d37d706637a0"
    },
    {
      id: "thein-day4",
      area: "thein",
      title: "더인 교육 4일차 정리",
      short: "4일차",
      category: "더인 교육",
      summary: "반도체 정의(전기전도도·비저항·Energy band gap), 반도체 종류, 유전체와 유전상수(High-k/Low-k), 8대 공정, Photo 공정(Snell 법칙·간섭·회절), Positive/Negative PR을 정리한 노트.",
      tags: ["더인 교육", "4일차", "반도체 정의", "유전체", "High-k", "Low-k", "8대 공정", "Photo", "Snell", "간섭", "회절", "PR"],
      date: "2026-11-05",
      updated: "2026-11-13",
      notion: "https://app.notion.com/p/40f6b8b7c6bb80c8baf2ca4317536f8a"
    },
    {
      id: "thein-day5",
      area: "thein",
      title: "더인 교육 5일차 정리",
      short: "5일차",
      category: "더인 교육",
      summary: "PR(NUV·DUV·EUV)과 현상 메커니즘, DUV 화학 증폭형 레지스트(CAR) 추가 공부, NA와 해상도, Soft/Hard Bake·PEB·HMDS, Carrier mobility, 공정 변동과 엔지니어 역할, Presentation(FLASH MEMORY Program/Erase)과 발표 피드백을 정리한 노트.",
      tags: ["더인 교육", "5일차", "PR", "DNQ", "CAR", "PAG", "PEB", "화학 증폭", "NA", "해상도", "PEB", "HMDS", "Passivation", "FLASH MEMORY", "발표 피드백"],
      date: "2026-11-06",
      updated: "2026-11-13",
      notion: "https://app.notion.com/p/40f6b8b7c6bb80d7a4d4ce3b3ecba790"
    },
    {
      id: "thein-day6",
      area: "thein",
      title: "더인 교육 6일차 정리",
      short: "6일차",
      category: "더인 교육",
      summary: "Dry Etch vs Wet Etch, 식각 파라미터(선택비·이방성·균일도)와 식각 이후 현상, 진공(Conductance·Throughput·Residence Time), ESC, Plasma 조건과 방전·Sheath, RF Plasma와 DC Self-bias(87pg 토론 문제)를 정리한 노트.",
      tags: ["더인 교육", "6일차", "Dry Etch", "Wet Etch", "식각", "이방성", "Conductance", "Throughput", "진공", "ESC", "Plasma", "디바이 차폐", "Sheath", "Presheath", "RF", "DC Self-bias", "Blocking capacitor"],
      date: "2026-11-09",
      updated: "2026-11-13",
      notion: "https://app.notion.com/p/4136b8b7c6bb80d98216dcb107624403"
    },
    {
      id: "thein-day7",
      area: "thein",
      title: "더인 교육 7일차 정리",
      short: "7일차",
      category: "더인 교육",
      summary: "Plasma etching 원리(Chemical·Sputter·Ion Enhanced·Inhibitor·DRIE), 식각 장비 분류(CCP·MERIE·ICP·ECR·Helicon), RIE의 Self bias와 Blocking capacitor, Pulsed Plasma, Si·SiO₂·Si₃N₄ 식각 화학과 선택비, Loading effect·ARDE·Uniformity, ALE와 스터디 질문을 정리한 노트.",
      tags: ["더인 교육", "7일차", "Plasma", "Etch", "RIE", "CCP", "ICP", "MERIE", "ECR", "Helicon", "Pulsed Plasma", "선택비", "Loading effect", "ARDE", "Uniformity", "ALE", "Self bias"],
      date: "2026-11-10",
      updated: "2026-11-13",
      notion: "https://app.notion.com/p/4146b8b7c6bb80979b63ec579225dff0"
    },
    {
      id: "thein-day8",
      area: "thein",
      title: "더인 교육 8일차 정리",
      short: "8일차",
      category: "더인 교육",
      summary: "5nm 노드의 의미와 트랜지스터 전류(μ·C_ox·W/L, 단채널 효과, HKMG, FinFET/GAA), Gate 금속의 변천(Al→Poly-Si→HKMG, 메모리/비메모리), Dielectric·Metal·Thin film, CVD(기체상/표면 반응, Film Growth Kinetics, APCVD·LPCVD·PECVD 응력, TEOS, SOG), PVD(Al-Cu, Electromigration), ALD, Step coverage와 Gap fill, Epi 층을 정리한 노트.",
      tags: ["더인 교육", "8일차", "5nm", "노드", "Thin film", "CVD", "PVD", "ALD", "LPCVD", "PECVD", "Film Growth Kinetics", "Electromigration", "Step coverage", "HDPCVD", "HKMG", "단채널 효과", "Gate 금속", "TEOS", "SOG", "Epi", "PECVD 응력"],
      date: "2026-11-11",
      updated: "2026-11-14",
      notion: "https://app.notion.com/p/4156b8b7c6bb8059adc8fb3b58f31b6a"
    },
    {
      id: "notes-qa",
      area: "notes",
      title: "반도체 정리노트 Q&A 연습",
      short: "Q&A 연습",
      category: "반도체 정리노트",
      summary: "Word로 정리한 반도체 질문 47개와 답변. 질문만 보고 먼저 답해 본 뒤 눌러서 답을 확인하는 연습용 페이지.",
      tags: ["반도체 정리노트", "Q&A", "면접 연습", "질문", "답변", "반도체 정리노트", "Word"],
      updated: "2026-11-07"
    },
    {
      id: "thein-insider",
      area: "thein",
      title: "현직자 관점 배워가기",
      short: "현직자 관점",
      category: "더인 교육",
      summary: "강사님들이 풀어 주신 현직 이야기와 실제 현장에서 발생하는 문제들을 한 곳에 모아 두는 페이지. 강사님1(노하우·혼자 일하는 경험·엔지니어의 성장), 강사님2(공정/설비 엔지니어가 하는 일) 썰을 정리했다.",
      tags: ["더인 교육", "현직자", "현장", "썰", "실제 문제", "공정기술", "설비기술", "Spec in", "레시피", "트렌드"],
      updated: "2026-11-07"
    },
    {
      id: "thein-homework",
      area: "thein",
      title: "과제",
      short: "과제",
      category: "더인 교육",
      summary: "더인 교육의 숙제, 토론 등 과제 내용을 한 곳에 모아 두는 페이지. ①반도체의 역사(반도체 개론 5pg) ②Particle이 미치는 영향(반도체 개론 111pg, 정답 슬라이드 포함) ③SiO₂ 성장은 Si/SiO₂ 계면에서 발생하는 이유(8대공정 1 교재 29pg) ④SiO₂ 두께-시간 그래프(교재 56pg) ⑤산화공정이란? 5분 발표 준비(대본 포함) ⑥조별과제: FLASH MEMORY의 동작원리(Program/Erase) 발표 내용·대본.",
      tags: ["더인 교육", "과제", "숙제", "토론", "반도체 역사", "트랜지스터", "VLSI", "SoC", "TSMC", "엘피다", "Particle", "산화공정", "SiO₂", "Deal-Grove", "발표 준비", "조별과제", "FLASH MEMORY", "Program", "Erase"],
      updated: "2026-11-07"
    }
  ]
};

/* 노션 날짜(date) 오래된 순으로 정렬한다. 홈 카드·하위 탭이 모두 이 순서를 따른다.
   date가 없는 주제(모음 페이지 등)는 같은 영역의 맨 뒤에 두고, 같은 날짜면 위 배열 순서를 유지한다. */
window.SITE.topics = window.SITE.topics
  .map(function (t, i) { return { t: t, i: i }; })
  .sort(function (a, b) {
    var x = a.t.date || '9999-99-99', y = b.t.date || '9999-99-99';
    return x < y ? -1 : x > y ? 1 : a.i - b.i;
  })
  .map(function (o) { return o.t; });
