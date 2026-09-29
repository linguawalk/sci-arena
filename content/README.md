# sci-arena 레슨 스키마 v1.0

경로: content/level{N}/{course}/ch{NN}/l{NN}.json
- 코스 목록: content/level{N}/{course}/course.json
- 챕터 목록: content/level{N}/{course}/ch{NN}/chapter.json
- 챕터 복습 세트: content/level{N}/{course}/ch{NN}/review.json

## 레슨 파일
- course / chapter / lesson: id, 번호, 제목 (lesson.minutes = 예상 소요 시간)
- tags.domain: 학문 분과 태그(물리·화학·생명·지구·융합), tags.region, tags.curriculum
- screens: 화면 배열. 순서대로 표시. stage = intro | discover | summary | apply
- 분량 기준: 레슨당 화면 20~24개, 문항 15~17개

## 복습 세트 파일(review.json)
- review: id, title, minutes
- questions: 문항 10개(레슨 문항과 같은 형식), stage = review, source_lesson = 출제 레슨 id
- 챕터의 모든 레슨에서 출제. 간격 복습과 진단 문항 풀로 재사용

## 화면 유형
- explain: title, body(문단 배열), figure(선택, 정적 위젯: number_line, area_model, right_triangle, graph)
  - area_model: config.rows / config.cols 에 변 이름 배열, 칸마다 행×열 넓이를 표시
  - right_triangle: config.legs·hypotenuse(변 이름), squares(각 변 위 정사각형 표시), angle·labels(삼각비 기준각과 변 이름)
- question: qtype별 필드
  - numeric: answer(문자열), answer_format(integer | fraction | decimal), tolerance
    - fraction은 동치 분수 허용 여부를 플레이어에서 결정(권장: 기약분수만 정답)
  - fill_blank: prompt 안 {{n}} 자리, blanks[n].answers(허용 답 목록), unordered_groups(순서 무관 빈칸 묶음)
    - 허용 답에는 마이너스(- / −)와 거듭제곱(² / ^2) 표기 변형이 미리 들어 있음
    - 플레이어는 비교 전 공백 제거 권장
  - ordering: items(표시 순서), answer_order(정답 id 순서)
  - diagram: widget별 설정
    - number_line: config(min, max, step), answer.value, answer.tolerance
    - coordinate_plane: config(xmin, xmax, ymin, ymax, xstep, ystep), answer.x, answer.y, answer.tolerance
  - written: rubric(visibility=hidden, keyword_groups, min_groups_matched), model_answer
    - 채점: 각 그룹 중 하나라도 포함되면 그룹 일치, 일치 그룹 수가 기준 이상이면 통과
    - rubric은 화면에 노출하지 않음
- 공통: hint(선택), explanation(정답 확인 후 표시), figure(선택, 문제 아래에 표시할 정적 그림)

## graph 위젯
- config: xmin, xmax, ymin, ymax, xstep, ystep, curves, points(선택, [x, y, 라벨]), xpi(선택, true이면 x축 눈금을 π/2, π처럼 표시)
- curves 종류(kind)
  - poly: coef = 오름차순 계수 [c0, c1, c2, …]
  - circle: cx, cy, r
  - rational: y = k/(x − p) + q
  - sqrt: y = a√(b(x − p)) + q
  - abs: y = a|x − p| + q
  - exp: y = a·b^(x − p) + q
  - log: y = a·log_b(x − p) + q
  - trig: y = a·fn(b(x − p)) + q, fn = sin | cos | tan
  - vline: x / hline: y (점선, 점근선·경계 표시용)
  - ellipse: 중심 (cx, cy), 반축 a(가로), b(세로)
  - hyperbola: 중심 (cx, cy), a, b, axis = x(좌우로 열림) | y(위아래로 열림)
  - parab_x: (y − cy)² = 4p(x − cx), 옆으로 열리는 포물선
  - arrow: (x1, y1)에서 (x2, y2)로 향하는 화살표, label(선택)
  - normal: 평균 m, 표준편차 s인 정규분포 밀도 곡선 (scale로 세로 배율 조정)
  - shade: curve와 x축(또는 curve2) 사이를 from~to 구간에서 칠함 (넓이 표시용)
  - 공통 선택 키: from, to(그릴 x 범위), color
- coordinate_plane 문항도 config.curves를 넣으면 곡선 위에 점을 찍게 할 수 있음

## geo 위젯 (도형 그림)
- config: elements(요소 배열), alt(대체 텍스트), maxh(최대 높이)
- 좌표는 수학 좌표(위쪽이 +y)이고, 전체 요소가 들어가도록 자동으로 크기를 맞춤
- 요소(t)
  - pt: 점 p, label(이름), pos(n/s/e/w/ne/nw/se/sw, 생략하면 도형 바깥쪽), hide(점 숨김)
  - seg: 선분 a–b, dash(점선), hl(강조)
  - poly: 다각형 pts, fill(false면 테두리만), hl(강조 색)
  - circle: 중심 c, 반지름 r, dash
  - right: 꼭짓점 p에서 a, b 방향 사이의 직각 표시
  - arc: 꼭짓점 p에서 a, b 방향 사이의 각 표시, label, r(화면 픽셀 반지름)
  - text: 위치 p에 글자 s (길이·기호 표시)
- 입체(정육면체, 각뿔)는 제작 단계에서 (x, y, z) → (x + 0.5y, z + 0.32y)로 투영하고, 보이지 않는 모서리는 점선으로 그림
- 도형 그림은 빌드 뒤 add_figs.py로 주입함. 레슨을 다시 생성하면 add_figs.py도 다시 실행할 것

## 예제 화면(example)과 풀이 기준
- example: title, problem(문제), steps(풀이 단계 배열), answer, figure(선택). 플레이어가 "풀이 보기 → 다음 단계"로 한 단계씩 펼침
- explanation은 줄바꿈(\n)으로 단계를 나누면 번호 목록으로 표시됨
- 보강을 마친 챕터는 엄격 검사(strict)를 켬: 모든 채점형 문항에 20자 이상 풀이, 적용·복습 문항에 힌트가 없으면 생성 실패
- 보강 데이터는 enrich_c{코스}_ch{NN}.py에 두고 빌드 때 자동 적용

## 단계별 기준(A·B·C)
- A(코스 0): 풀이 20자 이상, 예제 레슨당 3개
- B(코스 1·2): 풀이 40자 이상·2단계 이상, 설명 화면 110자 이상("왜 그런지" 문단 포함)
- C(코스 3~6): 풀이 60자 이상·3단계 이상, 설명 화면 160자 이상
- check_enrich.py로 보강 파일을 빌드 전에 검사할 수 있음


## sci-arena 차이점
- 채점 정규화: 아래·위 첨자를 일반 문자로 통일(H₂O = H2O, Mg²⁺ = Mg2+ = Mg^2+), ° 기호 무시, 대소문자는 구분(CO와 Co는 다른 답)
- 기호 입력줄: ₂ ₃ ₄ ² ³ ⁺ ⁻ → −
- graph 위젯: config.xlabel / config.ylabel로 축 이름 지정(예: "분", "°C")
- 레슨 생성: tools/build_c{코스}_ch{NN}.py (공용 도구 tools/sk.py). 빌드 때 단계 A 엄격 검사를 항상 적용
  - 레슨당 문항 15~17개, 화면 20~24개, 예제 3개, 채점형 문항 풀이 20자 이상, 적용·복습 문항 힌트 필수
- 빌드: python3 tools/build_c0_ch01.py content && python3 tools/make_course_index.py content

## 진입 진단 (placement)
- 문항 풀: content/level1/placement.json (tools/make_placement.py가 생성, 페이지는 placement_tpl.html → placement.html)
  - 챕터마다 5문항, 각 챕터 review.json에서 선별. 서술형, 앞 문항에 기대는 문항("위 문제에서…"), 그림 없이 그림·그래프를 언급하는 문항 제외
  - 후보 5문항은 레슨별로 번갈아 뽑아, 실제 출제 후보(앞 3문항)가 서로 다른 레슨에서 오게 함. 출제는 그중 무작위 1문항
  - pass_rate 0.7: 8챕터 코스는 6문항, 6챕터 코스(c0)는 5문항 이상 맞히면 통과. 탈락이 확정되면 그 코스는 즉시 종료
- 구조: 기초(c0) + 과목 트랙 4개 — 물리(c1→c5), 화학(c2→c6), 생명(c3→c7), 지구(c4→c8)
- 흐름(placement.html)
  - 학습 수준 선택: 중학 과학이 자신 없음(c0부터) / 중학 과학 마침(Ⅰ부터) / Ⅰ 과목까지 공부(Ⅰ 통과 시 같은 과목 Ⅱ 자동 진단)
  - 진단할 과목 선택(1~4개)
  - c0에서 탈락하면 과목 진단은 뒤로 미룸. Ⅰ 코스에서 크게 탈락(정답 < 오답)하면 c0를 추가로 진단
  - 결과 화면에서 진단하지 않은 코스(Ⅰ, 또는 Ⅰ 통과 뒤 Ⅱ)를 이어서 진단 가능
- 저장: localStorage "sci-arena:placement" (version 2)
  - start {c, ch, chTitle, chNo}: 가장 먼저 시작할 곳(c0 > Ⅰ > Ⅱ 순)
  - starts {코스: {c, ch, chTitle, chNo}}: 과목별 시작 위치
  - status {코스: pass | assumed | start | later | untested}
  - chapters {"c2-ch03": ok | weak | miss | start} (browse.html 챕터 표시)

## 레벨2·3 가이드 (guide)
- 트랙 목록: content/guides.json (5트랙: 물리·화학·생명과학·지구과학·융합, 과목별 level·available)
- 과목: content/level{2|3}/{트랙}/{과목}/subject.json
  - overview(분야 개요 3문단), tagline, level_note(수준과 목차 검증 기준)
  - prereq: text, links(레벨1 챕터·math-arena), questions(선수 점검, id p1~)
  - units: no, title, hours, after(먼저 볼 단원), file / total_hours / next(다음 과목)
- 단원: uNN.json (math-arena·tech-arena 공통 단원 템플릿)
  - objectives, checklist, advice(1~2문단, 문단당 80자 이상), resources(kind lecture|video|book|web, provider, title, part, url, lang), hours, selfcheck(레벨1 문항 스키마, stage = selfcheck)
- 제작: tools/guide_{과목}.py (공용 도구 tools/gk.py — 저장 전에 단원 번호·선수 단원·분량·서술형 모범 답안 채점 통과를 검사)
- 페이지: guide.html (?lv=&t=&s=&u=) — tools/make_guide.py가 player.html 공용 코드로 생성
- 저장: localStorage "sci-arena:guide" = {단원 id: {checks: [체크한 항목 번호], sc: {문항 id: 정답 여부}}}
- 추천 자료는 무료 공개 자료(OpenStax, MIT OCW, BCcampus, SEP 등)를 우선하고, 유료 교재는 URL 없이 장 번호만 적음
