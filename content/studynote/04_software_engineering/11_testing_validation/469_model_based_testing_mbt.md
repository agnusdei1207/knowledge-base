+++
title = "469. 모델 기반 테스팅 (MBT, Model-Based Testing)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 모델 기반 테스팅(MBT, Model-Based Testing)은 소프트웨어의 동작을 공식적인 모델(상태 기계, UML 다이어그램, 결정 테이블 등)로 표현하고, 그 모델에서 테스트 케이스를 자동 또는 반자동으로 생성하는 고급 테스트 기법이다.
> 2. **가치**: 복잡한 상태 전이(State Transition)와 분기 로직을 가진 시스템에서 사람이 수작업으로 테스트 케이스를 작성하는 것보다 훨씬 높은 커버리지와 일관성을 제공하며, 요구사항 변경 시 모델만 수정하면 테스트 케이스가 자동 재생성되는 유지보수 효율을 가져다 준다.
> 3. **판단 포인트**: MBT 도입 효과는 시스템의 상태 복잡성에 비례한다. 상태가 단순한 CRUD(Create, Read, Update, Delete) 중심 시스템보다, 통신 프로토콜·워크플로우 엔진·임베디드 제어 시스템처럼 복잡한 상태 전이를 가진 영역에 적합하다. 모델의 정확성이 곧 테스트 품질의 상한선이 된다.

---

## Ⅰ. 개요 및 필요성

### 등장 배경

소프트웨어 시스템이 복잡해질수록 수동 테스트 케이스 작성의 한계가 분명해졌다. 특히 1990년대 통신 프로토콜, 항공기 제어 소프트웨어, 의료 기기 소프트웨어처럼 안전성(Safety-Critical)이 중요한 영역에서는 모든 가능한 상태 조합을 인간이 직접 추적하고 테스트하는 것이 사실상 불가능했다.

모델 기반 접근은 이러한 문제를 해결하기 위해 형식적 명세(Formal Specification) 이론에서 출발했다. 하드웨어 설계에서는 이미 모델 검증(Model Checking)이 보편화되어 있었는데, 소프트웨어 분야에서도 유사한 접근을 적용하자는 시도가 MBT의 시초가 되었다. 1990년대 Conformiq, Telelogic 같은 기업들이 통신 프로토콜 테스트를 위한 MBT 도구를 개발하면서 상업적으로 실용화되었다.

### 왜 MBT가 필요한가

전통적 수동 테스트의 한계는 세 가지다. 첫째, '탐색 공간의 폭발(State Space Explosion)' 문제다. 상태가 10개인 시스템도 모든 전이 조합은 수백 가지가 될 수 있으며, 상태가 20개만 되어도 실질적으로 완전한 수동 커버리지는 불가능하다. 둘째, 인간의 일관성 한계다. 여러 테스터가 시간을 두고 작성한 테스트 케이스에는 중복, 누락, 해석 차이가 발생한다. 셋째, 요구사항 변경 시 유지보수 비용이다. 수작업 테스트 케이스는 요구사항이 바뀔 때마다 전면 재검토가 필요하다.

MBT는 이 세 가지 문제를 모두 해결한다. 모델이 상태 공간을 체계적으로 표현하므로 커버리지 계산이 가능하고, 모델에서 생성되는 테스트는 항상 일관성이 있으며, 요구사항이 바뀌면 모델만 수정하면 테스트 케이스가 자동 재생성된다.

MBT가 실제 적용된 사례로는 미국 항공우주국(NASA)의 화성 탐사선 소프트웨어 검증, 유럽 철도 제어 시스템(ERTMS), 통신사의 VoIP(Voice over Internet Protocol) 프로토콜 적합성 테스트 등이 있다.

- **📢 섹션 요약 비유**: 지도(모델) 한 장을 정확하게 그려두면, 그 지도에서 필요한 경로들을 자동으로 추출할 수 있다. 지도가 정확할수록 뽑아낸 경로의 신뢰도도 높아진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### MBT의 전체 프로세스



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">MBT 전체 프로세스 흐름</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">요구사항/명세</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">모델 작성</div><div class="kb-diagram-connector">←</div><div class="kb-diagram-note">상태 기계(FSM), UML, 결정 테이블 등</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">모델 검증</div><div class="kb-diagram-connector">←</div><div class="kb-diagram-note">논리적 완전성, 일관성 검사</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">테스트 선택 기준 설정</div><div class="kb-diagram-connector">←</div><div class="kb-diagram-note">커버리지 목표 정의</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(모든 상태 커버? 모든 전이 커버? 모든 경로 커버?)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">테스트 케이스 자동 생성</div><div class="kb-diagram-connector">←</div><div class="kb-diagram-note">MBT 도구 실행</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">테스트 실행 및 결과 비교</div><div class="kb-diagram-connector">←</div><div class="kb-diagram-note">오라클(Oracle) 비교</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">모델 정제/보완</div><div class="kb-diagram-connector">←</div><div class="kb-diagram-note">불일치 발견 시 모델 재검토</div></div>
</div>
</div>



### MBT에서 사용되는 모델 유형

| 모델 유형 | 설명 | 적합한 시스템 | 표현력 |
|:---|:---|:---|:---|
| 유한 상태 기계(FSM, Finite State Machine) | 상태와 전이로 동작 표현 | UI 흐름, 프로토콜 | 중간 |
| 확장 상태 기계(EFSM) | FSM + 변수·조건 | 복잡한 비즈니스 로직 | 높음 |
| 마르코프 체인(Markov Chain) | 확률 기반 상태 전이 | 통계적 사용 패턴 | 중간 |
| UML 활동 다이어그램 | 제어 흐름 모델링 | 비즈니스 프로세스 | 높음 |
| UML 상태 다이어그램 | 상태/이벤트/행동 | 반응형 시스템 | 높음 |
| 결정 테이블(Decision Table) | 조건-행동 매핑 | 규칙 기반 시스템 | 중간 |
| EBNF/문법(Grammar) | 입력 언어 명세 | 파서, 컴파일러 | 높음 |

### 상태 기계(FSM) 기반 MBT 예시: 로그인 시스템



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">초기 상태: 로그아웃</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">로그인 시도</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">인증 성공</div><div class="kb-diagram-node">인증 실패</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">↓</div><div class="kb-diagram-node">재시도 카운터 증가</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">로그인 상태</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">3회 초과?</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">로그아웃 요청</div><div class="kb-diagram-note">↙ ↘</div></div>
<div class="kb-diagram-note">예 아니오</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">로그아웃 상태</div><div class="kb-diagram-node">계정 잠금</div><div class="kb-diagram-node">다시 로그인 시도</div></div>
<div class="kb-diagram-note">생성되는 테스트 케이스:</div>
<div class="kb-diagram-note">TC-001: 정상 로그인 → 로그인 성공 확인</div>
<div class="kb-diagram-note">TC-002: 잘못된 비밀번호 1회 → 재시도 가능 확인</div>
<div class="kb-diagram-note">TC-003: 잘못된 비밀번호 3회 → 계정 잠금 확인</div>
<div class="kb-diagram-note">TC-004: 로그인 후 로그아웃 → 로그아웃 상태 확인</div>
<div class="kb-diagram-note">TC-005: 잠긴 계정 로그인 시도 → 잠금 유지 확인</div>
</div>
</div>



### 테스트 커버리지 기준 비교

| 커버리지 기준 | 설명 | 생성 케이스 수 | 비용 |
|:---|:---|:---|:---|
| 상태 커버리지(State Coverage) | 모든 상태를 최소 1회 방문 | 적음 | 낮음 |
| 전이 커버리지(Transition Coverage) | 모든 상태 전이를 최소 1회 수행 | 중간 | 중간 |
| 전이 쌍 커버리지(Transition-Pair) | 연속된 전이 쌍 모두 커버 | 많음 | 높음 |
| 모든 경로 커버리지(All-Path) | 가능한 모든 경로 커버 | 매우 많음 | 매우 높음 |

### 주요 MBT 도구

| 도구명 | 주요 기능 | 지원 모델 |
|:---|:---|:---|
| Conformiq | 상태 기계 기반 자동 케이스 생성 | EFSM |
| GraphWalker | 그래프 기반 탐색적 케이스 생성 | FSM |
| Smartesting Yest | 비즈니스 규칙 모델 기반 | 결정 테이블 |
| Microsoft Spec Explorer | 코드 기반 모델 명세 | FSM/행동 모델 |
| UPPAAL | 시간 자동자(Timed Automata) | EFSM + 시간 |

- **📢 섹션 요약 비유**: 보드게임 규칙표(모델)가 정확하면, 가능한 모든 게임 전략(테스트 케이스)을 자동으로 열거할 수 있다. 규칙표가 틀리면 잘못된 전략이 나온다.

---

## Ⅲ. 비교 및 연결

### 수동 테스트 vs MBT

| 구분 | 수동 테스트 케이스 작성 | 모델 기반 테스팅(MBT) |
|:---|:---|:---|
| 케이스 생성 방식 | 테스터가 직접 작성 | 모델에서 자동 생성 |
| 일관성 | 테스터 간 편차 발생 | 모델 기준으로 일관 |
| 커버리지 추적 | 어려움 | 수치로 측정 가능 |
| 유지보수 | 요구사항 변경 시 전면 수정 | 모델 수정 후 재생성 |
| 초기 비용 | 낮음(도구 불필요) | 높음(모델링 학습 필요) |
| 장기 비용 | 높음(누적 수작업) | 낮음(자동화 효과 누적) |
| 오류 발견 유형 | 테스터 경험 의존 | 체계적 경로 탐색 |
| 적합 영역 | 단순 기능, UI | 복잡한 상태 시스템 |

### MBT vs 탐색적 테스팅(Exploratory Testing)

| 구분 | MBT | 탐색적 테스팅 |
|:---|:---|:---|
| 방식 | 체계적·구조적 | 직관적·창의적 |
| 기반 | 모델(공식 명세) | 테스터의 경험과 지식 |
| 강점 | 상태 공간 완전 커버 | 예상치 못한 문제 발견 |
| 적합 시점 | 명세가 안정된 시스템 | 명세가 불완전하거나 초기 단계 |
| 결합 | 두 기법을 상호 보완적으로 결합 권장 | |

### 관련 개념 연결

| 관련 개념 | 연결 내용 |
|:---|:---|
| [상태 전이 다이어그램 테스트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/) | MBT의 핵심 모델 유형. 상태 기계를 직접 활용 |
| [UML](/knowledge-base/studynote/04_software_engineering/04_testing_quality/232_uml_unified_modeling_language_overview/) | MBT 모델 표현의 공통 언어. 활동/상태 다이어그램 활용 |
| [시퀀스 다이어그램](/knowledge-base/studynote/04_software_engineering/04_testing_quality/235_sequence_diagram_dynamic_interaction_uml/) | 상호작용 기반 MBT 모델로 활용 |
| [TDD(테스트 주도 개발)](/knowledge-base/studynote/04_software_engineering/11_testing_validation/470_tdd_lifecycle/) | TDD와 MBT는 상호 보완. TDD는 구현 중심, MBT는 명세 중심 |
| [테스트 케이스](/knowledge-base/studynote/04_software_engineering/11_testing_validation/441_test_case/) | MBT의 직접적 산출물 |

- **📢 섹션 요약 비유**: 설계 도면(모델)이 정확하면 공장에서 부품을 자동으로 제조(테스트 케이스 생성)할 수 있고, 설계가 바뀌어도 설계도만 수정하면 새로운 부품이 자동 생산된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### MBT 적용 적합성 평가

| 평가 항목 | MBT 적합 | MBT 부적합 |
|:---|:---|:---|
| 상태 수 | 10개 이상의 복잡한 상태 | 3개 이하의 단순 상태 |
| 요구사항 안정성 | 명세가 확정되고 안정적 | 명세가 자주 변경 |
| 시스템 유형 | 프로토콜, 워크플로우, 임베디드 | 단순 CRUD UI |
| 팀 역량 | 모델링 능력 보유 또는 학습 의지 | 모델링 경험 전무 |
| 프로젝트 기간 | 중장기 (6개월 이상) | 단기 (1개월 이내) |

### 설계 판단 체크리스트

1. **시스템의 상태 복잡성을 정량화했는가?** - 상태 수, 전이 수, 가능한 경로 수를 계산해 MBT 투자 대비 효과를 평가한다.
2. **모델 작성 능력이 팀 내에 있는가?** - UML 상태 다이어그램 또는 FSM을 정확하게 작성할 수 있는 역량이 없으면 MBT 도입 전 교육이 선행되어야 한다.
3. **테스트 오라클(Oracle)이 정의되었는가?** - 자동 생성된 테스트의 기대 결과를 어떻게 정의하고 검증할 것인지 명확해야 한다.
4. **MBT 도구와 CI/CD 파이프라인 연계를 계획했는가?** - 요구사항 변경 시 모델 갱신 → 케이스 재생성 → 자동 실행 흐름이 파이프라인에 통합되어야 효과가 극대화된다.
5. **모델 버전 관리 체계를 갖췄는가?** - 소스 코드와 마찬가지로 모델도 Git 등으로 버전 관리되어야 한다.
6. **커버리지 목표를 결정했는가?** - 전이 커버리지 100%인지, 경로 커버리지인지 비용 대비 목표를 설정한다.

### 안티패턴

- **부정확한 모델의 무비판적 사용**: 모델이 잘못 작성되었음에도 "MBT가 생성했으니 맞겠지"라고 신뢰하는 경우. 모델의 오류가 테스트 케이스 전체의 오류로 확산된다. "Garbage In, Garbage Out(나쁜 입력, 나쁜 출력)" 원칙이 MBT에도 그대로 적용된다.
- **모델과 구현의 불일치 방치**: 구현 코드가 변경되었을 때 모델을 업데이트하지 않아 점차 모델이 현실을 반영하지 못하게 되는 경우. 오래된 모델에서 생성된 테스트는 현재 시스템을 제대로 검증하지 못한다.
- **모든 경로 커버리지 맹목적 추구**: 이론적으로 완전한 경로 커버리지를 목표로 삼아 실용적이지 않은 수의 테스트 케이스를 생성하는 경우. 실행 시간이 폭발적으로 늘어 CI/CD 파이프라인이 무력화된다.
- **단순 시스템에 MBT 적용**: 상태가 3개뿐인 단순 기능에 MBT를 도입하여 모델링 오버헤드가 실제 테스트 작성 비용보다 커지는 경우. 투자 대비 효과가 마이너스가 된다.
- **오라클 없는 자동 테스트**: 테스트 케이스는 생성했지만 기대 결과(Oracle)를 정의하지 않아 테스트의 합격/불합격을 판단할 수 없는 상황.

- **📢 섹션 요약 비유**: 정확한 지도로 최적 경로를 자동으로 계산할 수 있지만, 지도 자체가 틀리면 잘못된 경로를 안내받는다. MBT에서 모델의 정확성은 GPS에서 지도 데이터의 정확성과 같다.

---

## Ⅴ. 기대효과 및 결론

MBT를 성숙하게 적용한 조직에서 나타나는 대표적 성과는 다음과 같다. 첫째, 테스트 커버리지의 정량적 측정이 가능해진다. 임의적으로 작성된 수동 케이스와 달리, MBT의 커버리지는 모델 대비 몇 퍼센트를 검증했는지 수치로 보고할 수 있다. 이는 품질 감리나 기술사 시험에서 중요한 논거가 된다. 둘째, 요구사항 변경에 대한 적응력이 높아진다. 스펙이 바뀌면 모델을 수정하고 테스트를 재생성하면 되므로, 변경 비용이 대폭 감소한다. 셋째, 초기에 발견하기 어려운 상태 조합 버그를 사전에 탐지한다. 특히 임베디드 소프트웨어나 안전 핵심 시스템에서 이러한 효과가 두드러진다.

단, MBT는 만능이 아니다. 모델 작성과 유지보수에 상당한 초기 투자가 필요하고, 팀의 모델링 역량이 부족하면 오히려 불정확한 모델이 잘못된 자신감으로 이어질 위험도 있다. 따라서 MBT 도입은 복잡도가 높고 안전성이 중요한 시스템 영역에 선별적으로 적용하고, 수동 테스트 및 탐색적 테스팅과 병행하는 것이 바람직하다.

결론적으로 MBT는 "모델의 정확성이 테스트 품질의 상한을 결정하는 체계적 테스트 자동화 전략"이다. 상태 복잡성이 높은 시스템에 도입 시, 장기적으로 테스트 유지보수 비용을 줄이고 품질 가시성을 높이는 강력한 도구가 된다.

- **📢 섹션 요약 비유**: 정밀한 설계도(모델)와 CNC 기계(MBT 도구)가 만나면 동일한 품질의 부품(테스트 케이스)을 대량으로 자동 생산할 수 있다. 설계도의 정밀도가 모든 것을 결정한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [상태 전이 다이어그램 테스트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/) | MBT의 핵심 모델. 상태 기계를 직접 테스트 입력으로 활용 |
| [UML](/knowledge-base/studynote/04_software_engineering/04_testing_quality/232_uml_unified_modeling_language_overview/) | MBT 모델 표현의 표준 언어 |
| [TDD 생명주기](/knowledge-base/studynote/04_software_engineering/11_testing_validation/470_tdd_lifecycle/) | MBT와 상호 보완. TDD는 구현 중심, MBT는 명세 중심 |
| [테스트 케이스](/knowledge-base/studynote/04_software_engineering/11_testing_validation/441_test_case/) | MBT의 직접 산출물 |
| [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) | MBT의 상위 학문 체계 |
| [소프트웨어 생명주기 (SDLC)](/knowledge-base/studynote/04_software_engineering/01_overview_principles/003_sdlc/) | MBT는 SDLC의 설계~테스트 단계에 걸쳐 적용 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">형식적 명세 이론 (Formal Specification, 1970-80s)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">모델 검증 (Model Checking, 1980s) ← 하드웨어 검증에서 출발</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">소프트웨어 MBT 연구 시작 (1990s)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">통신 프로토콜 적합성 테스트 도구 상용화 (Conformiq 등)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">UML 기반 MBT 확산 (2000s)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">GraphWalker 등 오픈소스 도구 등장</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">CI/CD와 MBT 통합 (자동화 파이프라인)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">AI/ML 보조 모델 생성 및 최적화 경로 탐색 (2020s)</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 미로 찾기 게임의 지도(모델)를 컴퓨터에 입력하면, 컴퓨터가 가능한 모든 길(테스트 케이스)을 자동으로 찾아내는 것이 MBT예요.
2. 손으로 직접 길을 찾으면 중간에 빠뜨리는 길이 생기지만, 지도가 있으면 빠짐없이 모든 길을 확인할 수 있어요.
3. 지도가 틀리면 잘못된 길을 알려주니까, 지도(모델)를 정확하게 그리는 것이 가장 중요해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 529 / 973

← **이전**: [468. 운영 환경 테스트 (Testing in Production / TiP)](/knowledge-base/studynote/04_software_engineering/11_testing_validation/468_testing_in_production/)
**다음**: [470. TDD 생명주기 (TDD Lifecycle)](/knowledge-base/studynote/04_software_engineering/11_testing_validation/470_tdd_lifecycle/) →

---
