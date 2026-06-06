---
title: "535. 접근성 테스팅 WCAG 규정 준수 (Accessibility Testing WCAG Compliance)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 접근성 테스팅은 WCAG 2.1/2.2의 4대 원칙(Perceivable·Operable·Understandable·Robust)과 13개 가이드라인, 총 86개 성공 기준을 인지·운동·시각·청각 장애가 있는 사용자 환경(보조기술: 스크린리더 NVDA/JAWS/VoiceOver, 스위치 입력, 화면확대 등)에서 검증하는 **규범 기반(Conformance-based) 품질 보증 활동**이다.
> 2. **가치**: 글로벌 시장 진입(미국 ADA Title III, 유럽 EAA 2025, 한국 장애차별금지법·지능정보화 기본법 2024년 전면시행)의 법적 리스크를 제거하고, OECD 기준 약 15% 인구의 구매력(연 13조 달러+)을 확보하며, SEO·모바일 사용성·코드 유지보수성까지 동시에 개선하는 **"1석 4조(4 Birds)"** 효과를 제공한다.
> 3. **판단 포인트**: 자동화 도구(axe-core, Pa11y, Lighthouse)의 검출률 한계(전체 WCAG 실패 중 약 30~40%만 검출)와 수동·사용자 테스팅의 비용·시간 부담, 그리고 SPA/동적 콘텐츠/Rich Widget의 ARIA 적용 시 **"False Positive 최소화 vs 진짜 사용자 경험(Real User Experience) 검증"** 사이의 균형점 설계가 핵심 아키텍처 의사결정이다.

---

## Ⅰ. 개요 및 필요성

웹 접근성(Web Accessibility)이 단순한 '좋은 실천 사항(Good Practice)'에서 **'강제 법적 의무(Compliance Mandate)'**로 전환된 것은 2017년 미국 Domino's Pizza 사건(Supreme Court 상고 기각) 이후 전 세계적인 흐름이 되었다. 한국은 2008년 「장애인차별금지 및 권리구제 등에 관한 법률」, 「국가정보화 기본법」, 2024년 전면 개정된 「지능정보화 기본법」 제45조의2(웹접근성 준수) 및 2025년 시행되는 「전사적 기업활동 디지털 포용법(EAA, European Accessibility Act)」의 영향으로, 공공기관은 **KWCAG 2.1**, 민간 전자상거래·금융·통신·교통·전자책·e커머스 사업자는 **WCAG 2.1 Level AA** 이상 준수가 사실상 의무화되었다.

기술사적 관점에서 접근성 테스팅은 **"기능적 결함(Functional Defect) + UX 결함 + 법적 컴플라이언스"** 3중 결함을 단일 테스트 사이클에서 모두 잡아야 하는 **Cross-Cutting Quality Attribute**다. 일반 QA(기능·성능·보안)와 달리 장애 시나리오를 가상으로 모델링해야 하므로, 페르소나 기반 테스트 설계(시각장애, 전맹, 색약, 운동장애, 인지장애, 전신마비)라는 특수한 기법이 필요하다.

```text
[접근성 테스팅의 3차원적 결함 공간 모델]

                    법적 컴플라이언스
                  (KWCAG/WCAG/ADA/EAA)
                          ^
                         /|\
                        / | \
                       /  |  \
                      /   |   \
                     /  ◈  |    \      ◈ = 테스트 대상 결함
                    / 결함 | 공간 \
                   /  공간  |  (Defect  \
                  /         |   Space)   \
                 /----------+-------------\
                /           |              \
               v------------+--------------v
         기능적 결함 --------► UX/인지적 결함
        (Form 깨짐,        (인지 부하, 색만으로 정보전달,
         키보드 함정)        모호한 레이블, 일관성 부재)
```

**구(old) 패러다임 vs 신(new) 패러다임 비교**

- **구(Old)**: QA 사이클 종료 후 1회성 점검, "스크린리더로 한 번 읽어보기", 디자인 완료 후 사후 검증(After-the-fact)
- **신(New)**: SDLC 전 단계 통합(Shift-Left), Design Token 단계의 색대비 자동 검증, CI/CD의 axe-core/Pa11y 게이트, Storybook + Chromatic 시각 회귀 + 접근성 매트릭스, **Accessibility as Code**(테스트 코드로 WCAG 기준을 명세)

- **📢 섹션 요약 비유**: 접근성 테스팅은 "문 앞에 난간(Handrail)을 설치하는 일"과 같다. 법적으로도, 윤리적으로도, 실용적으로도(휠체어·유모차·노약자 모두 사용) 반드시 필요하지만, 입구 하나만 보고 설계하면 안 되고 건물 전체의 경사로, 점자 안내, 음성 방송 시스템, 비상구 사인까지 통합적으로 설계해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

접근성 테스팅 아키텍처는 크게 **3-Layer Testing Pyramid**(자동화 -> 반자동 -> 사용자 평가)로 구성된다. 이는 Martin Fowler의 Test Pyramid를 접근성 도메인에 맞게 재해석한 것이다.

```text
[접근성 테스팅 3-Layer Pyramid 아키텍처]

                    ^
                   ╱ ╲
                  ╱   ╲         Layer 3: 사용자 테스팅(User Testing)
                 ╱ 실사용 \      - 실제 보조기술 사용자 5~10명 패널
                ╱  장애    \     - NVDA/JAWS/VoiceOver/TalkBack
               ╱   사용자    \   - Task-based Scenario
              ╱   페르소나    \  - 정성적 데이터 수집
             ╱---------------\
            ╱                 \  Layer 2: 반자동·전문가 검증
           ╱ 반자동·전문가 검증 \ - 수동 코딩 리뷰(ARIA 패턴)
          ╱  WAVE, ANDI,        \ - 키보드 only 트래버설
         ╱   Contrast Analyzer, \ - 인지 워크스루(Cognitive Walkthrough)
        ╱     Accessibility Tree  \ - 진동·포커스 시각화
       ╱     Inspection           \
      ╱-----------------------------\
     ╱                               \  Layer 1: 자동화(Automated)
    ╱    CI/CD 내장 자동화 도구        \ - axe-core(Deque)
   ╱     Lighthouse CI, Pa11y,        \ - Lighthouse, ALFA
  ╱      eslint-plugin-jsx-a11y,      \ - HTML CodeSniffer
 ╱       react-axe, ng-aXe            \ - 단위·통합·E2E 단계
╱-------------------------------------\    게이트(Gate)
              ╲
               ╲--------► 빌드 실패/경고
                          (예: 0 errors of
                           'critical' severity)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Layer 1: 자동화 엔진 (Automated Engine)** | 정적·동적 분석으로 객관적·반복 가능한 WCAG 실패 패턴 검출 | **axe-core**: 90+ 규칙, ARIA·HTML5 명세 기반, REST API `POST /analyze`로 1회 호출 시 평균 200~500ms 내 결과. **Pa11y/Pa11y CI**: HTML_CodeSniffer 후속, Node.js CLI, exit code 기반 CI 게이트. **Lighthouse** v11+: `lighthouse --only-categories=accessibility` 로 0~100 점수. **eslint-plugin-jsx-a11y**: 빌드 시점 lint(shift-left) |
| **Layer 2: 반자동·전문가 도구 (Semi-Automated)** | 자동화로 못 잡는 논리적·맥락적 결함(예: 알맞은 ARIA role인지, focus trap이 작동하는지) | **WAVE** (webaim.org): 브라우저 익스텐션, DOM 오버레이 시각화(아이콘 13종). **ANDI** (SSA): 미국 SSA 개발, 9개 카테고리 모듈(Structure, Images, Tables 등). **Colour Contrast Analyser** (CCA): 픽셀 단위 WCAG 1.4.3·1.4.11·1.4.6 측정(AA: 4.5:1, AAA: 7:1, 비활성 UI 컴포넌트는 3:1) |
| **Layer 3: 보조기술 (Assistive Technology, AT)** | 실제 사용자 환경과 1:1 매칭, 인터랙션 가능성·인지 부하 검증 | **스크린리더**: NVDA(Windows, 무료, 가장 광범위), JAWS(Windows, 유료, 금융권 표준), VoiceOver(macOS/iOS 내장), TalkBack(Android 내장), ChromeVox(ChromeOS). **키보드 전용**: Tab, Shift+Tab, Enter, Space, Arrow Keys, Esc. **스위치 입력**: Single Switch·Sip-and-Puff. **화면확대**: ZoomText, macOS Zoom(200%+) |
| **Accessibility Tree (의미론적 트리)** | 브라우저가 노출하는 플랫폼 중립적 의미 표현, AT의 입력 데이터 | DOM ≠ AX Tree. ARIA가 AX Tree를 풍부하게 함. 예: `<div role="button" aria-label="닫기">` -> AX Tree에서 `AXButton` 노드. **Chrome DevTools**의 Accessibility 탭에서 확인 가능 |
| **Conformance Validator (규격 검증기)** | 명세·스키마 수준에서 위반 가능성 사전 차단 | **W3C HTML Validator**: 잘못된 마크업 -> ARIA 역할 매핑 실패 원인의 60%. **ARIA Authoring Practices Guide (APG)** 1.2: combobox, listbox, dialog, tab 등 12개 디자인 패턴별 키보드·ARIA 표준 |

**핵심 파라미터와 알고리즘 (Deep Dive)**

WCAG 2.1 SC(성공 기준)별 검증 알고리즘은 의사결정 로직으로 표현된다. 기술사 시험에는 대표 사례 2~3개를 정확히 암기해야 한다.

- **1.4.3 Contrast (Minimum)**: `relativeLuminance(L1, L2) ≥ 4.5` (일반 텍스트, AA). 상대 휘도 공식: `L = 0.2126·R + 0.7152·G + 0.0722·B` (각 채널은 sRGB -> Linear 변환). WCAG 3의 APCA(Advanced Perpendicular Contrast Algorithm)는 휘도 대신 인지 대비 모델로 폴리필 제공.
- **2.1.1 Keyboard**: 모든 기능을 키보드로 달성 가능. 예외: 자유 입력(typing 자체), 본질적으로 경로가 필요한 동작(손글씨)
- **2.4.7 Focus Visible**: `:focus-visible` CSS 의사 클래스(2023년 Baseline). 기본 UA 스타일 제거 시 반드시 재정의 필요
- **3.3.1 Error Identification**: 입력 오류 시 `aria-invalid="true"` + `aria-describedby="error-msg-id"` + `role="alert"` (라이브 영역)
- **4.1.2 Name, Role, Value**: AT가 인식 가능한 이름(Named)을 가져야 함. `aria-label` > `aria-labelledby` > `<label for>` > `title` > `alt` > 텍스트 콘텐츠(우선순위 계산 알고리즘: Accessible Name and Description Computation 1.1)

- **📢 섹션 요약 비유**: 접근성 테스팅 아키텍처는 **"3단 망원경"**과 같다. 자동화(Layer 1)는 손으로 들고 하늘을 훑는 **망원경의 왼쪽 접안렌즈(광시야, 저배율)**: 빠르고 넓게 보지만 미세한 별은 못 잡음. 반자동(Layer 2)은 **중앙 프리즘(중배율)**: 검증자가 직접 들여다보며 형태를 분석. 사용자 테스팅(Layer 3)는 **대물렌즈(고배율, 협시야)**: 한 번에 한 사람만 보지만, 그 사람이 보는 우주의 별 색깔·궤적까지 모두 포착한다.

---

## Ⅲ. 비교 및 연결

| 구분 | **WCAG 2.1** | **WCAG 2.2** | **KWCAG 2.1** (한국형) | **Section 508 (US)** | **EN 301 549 (EU/EAA)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **발행 연도** | 2017 | 2023 (10월) | 2014 / 개정 2021 | 2017 (Rehab Act 갱신) | 3.2.1 (2021) |
| **성공 기준 수** | 78 -> 86 (WCAG 2.1) | 86 -> 95 (WCAG 2.2: 9개 추가) | 26개 (한국 고유 항목 포함) | WCAG 2.0 AA + ICT 항목 | WCAG 2.1 AA + ICT·서비스·문서 |
| **주요 신규 항목** | 모바일·저시력·인지 추가 (1.3.4, 1.3.5, 2.5.x) | 2.4.11 Focus Not Obscured, 2.4.13 Focus Appearance, 2.5.7 Dragging, 2.5.8 Target Size, 3.2.6 Consistent Help, 3.3.7 Redundant Entry, 3.3.8 Accessible Authentication | 4.1 웹사이트, 4.2 웹앱, 4.3 모바일앱 구분. 시간제한(2.2.1)에 "음성 자동재생"·"깜빡임" 한국형 항목 | 1) Functional Performance Criteria 2) Hardware 3) Software 4) Support Documentation | EU 공공조달·2025 EAA 적용 |
| **자동화 가능률** | ~30~40% | ~30~35% (신규는 더 낮음) | ~30% | ~30% | ~30% |
| **한국 적용** | 권고 | 미반영(2024 현재) | **공공기관 의무(행정안전부)** | 미적용 | 민간 일부 |

**연관 시스템·도구 통합 아키텍처**

- **JIRA/Xray + Zephyr**: 접근성 결함 -> Epic/Story 등록. Severity = Blocker(예: 1.1.1 Non-text Content 핵심 위반)
- **GitHub Actions / Jenkins + axe-core**: PR 단위 검사, Step `npx pa11y-ci --json > report.json` -> SARIF 변환 -> GitHub Code Scanning
- **Figma 플러그인(Stark, A11y Annotation Kit, Able)**: 디자인 단계 색대비·포커스 순서 사전 검증
- **Storybook + a11y addon**: 컴포넌트 단위 시각화 + 접근성 위반 표시
- **Cypress + cypress-axe**: E2E 흐름 중 동적 콘텐츠 검증(SPA 라우팅 후 페이지)
- **Playwright + @axe-core/playwright**: 멀티 브라우저(Chromium/Firefox/WebKit) 동시 검증
- **눈으로 보는 결과**(비-자동화 영역): 키보드 트래버설, 200% 줌 시 가로·세로 스크롤, 화면 흔들림(Seizure 2.3.1: 1초 3회 이상 깜빡임 금지)

- **📢 섹션 요약 비유**: WCAG 2.1과 2.2의 관계는 **"운전면허 시험 개정판"**과 같다. 2.1이 일반도로·고속도로·교통신호까지 본다면, 2.2는 **"스마트 하이웨이 시대"의 새로운 상황**까지 추가: 드래그 모션 없이 클릭만으로(Focus Appearance), 일관된 도움말, 다시 인증 불필요(Accessible Authentication) 같은 **UX 정밀도**를 다룬다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **컴플라이언스 레벨 결정**: 한국 공공 = KWCAG 2.1(웹·앱). 민간 e커머스·금융·ISP = WCAG 2.1 AA (EAA 2025 대비 AA 이상 권장). "AAA를 전사 표준으로 채택"은 비용 대비 효과 미흡, **AA가 Sweet Spot**.
2. **Shift-Left 게이트 설계**: PR 단계에서 `eslint-plugin-jsx-a11y` + `axe-core` 빌드 시점 강제. Build fail 조건: `violations.filter(v => v.impact==='critical' || v.impact==='serious')` ≥ 1. 단,
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 535 / 600

<- **이전**: [534. 보안 테스팅 OWASP 취약점 진단](/studynote/11_design_supervision/06_exam_summary/534_security_testing_owasp_vulnerability)
**다음**: [536. 회귀 테스팅 자동화 전략 효율화](/studynote/11_design_supervision/06_exam_summary/536_regression_testing_automation_strategy/) ->

---
