---
title: "Model Based Testing MBT Automation"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: MBT(Model-Based Testing)는 시스템의 동작을 FSM(Finite State Machine), Markov Chain, UML State/Activity Diagram, Decision Table 등의 **추상 모델**로 명세하고, 그 모델로부터 Coverage Criteria(State, Transition, Action, N-switch coverage 등)를 만족하는 테스트 케이스를 **알고리즘 기반으로 자동 생성·실행·평가**하는 테스팅 방법론이다. ISO/IEC/IEEE 29119-4에서 테스트 설계 표준으로 정의된다.
> 2. **가치**: 동일 Coverage 확보 시 수동 대비 **테스트 설계 시간 40~70% 단축**, 결함 검출률 15~30% 향상, 명세 변경 시 모델만 갱신하면 테스트가 자동 재생성되어 **회귀 테스트 자동화 비용 60% 절감** 효과가 보고되어 있다(대형 통신·금융 임베디드 도메인 사례 기준).
> 3. **판단 포인트**: 적용 ROI는 **(시스템 상태 공간 크기) × (변경 빈도) × (결함 단가)** 의 함수로 결정되며, 모델 작성·유지보수 오버헤드와 도구 종속성(Tool Lock-in), 비결정적(Nondeterministic) 시스템 처리가 핵심 Trade-off다. 임베디드 제어기·통신 프로토콜·금융 거래·의료기기 같은 **상태 폭발(State Explosion)** 위험 도메인에서 효과가 극대화된다.

---

## Ⅰ. 개요 및 필요성

### 1.1 정의 및 등장 배경

기존의 **테스트 자동화(Test Automation)**는 사람이 작성한 테스트 스크립트(Selenium, Appium, JUnit, Robot Framework 등)를 자동 실행하는 수준에 머물렀다. 이는 **"스크립트 자동화(Test Execution Automation)"** 이지 **"테스트 설계 자동화(Test Design Automation)"** 가 아니었다. 요구사항이 변경되면 매번 스크립트를 수동으로 다시 작성해야 했고, 시스템 상태 공간이 증가하면 결함을 누락(Skip)할 위험이 컸다.

MBT는 이 문제를 해결하기 위해 2000년대 초 유럽(핀란드 VTT, 독일 Fraunhofer, 이스라엘 IBM Haifa Lab 등)을 중심으로 학술·산업적으로 정립된 방법론으로, **테스트의 진리원(Ground Truth)을 "코드"가 아닌 "모델"로 전환**하는 패러다임이다. ISTQB가 2015년 CT-MBT(Foundation Level Specialist) 자격을 공식화하면서 글로벌 확산이 가속되었고, ISO/IEC/IEEE 29119-4(2015)가 테스트 설계 기법의 하나로 MBT를 표준화했다.

### 1.2 기존 테스팅과 비교

| 관점 | 수동 테스트 설계 | 스크립트 기반 자동화 | MBT |
|:-----|:----------------|:--------------------|:-----|
| 설계 자산 | 테스트 케이스 문서 | 코드(Selenium 등) | 추상 모델 |
| 변경 대응 | 문서 재작성 | 코드 재작성 | 모델 수정만 |
| Coverage 측정 | 담당자 경험 의존 | 분기·문장 단위 | State/Transition/Action/MCDC 등 |
| 산출물 | TC 목록 | 스크립트 | 모델 + 자동 생성 TC + Coverage 리포트 |
| 유지보수 비용 | 높음 | 매우 높음(회귀 시 누적) | 모델 1개 수정으로 전파 |

### 1.3 MBT 적용이 필요한 상황

- **상태 폭발 위험**: 임베디드 제어기(전장 ECU, 의료기기 펌웨어), 통신 프로토콜 스택(LTE/5G, Bluetooth LE state machine)에서 가능한 상태 조합이 10^4 이상
- **규제 인증**: IEC 61508(SIL 2~4), ISO 26262(ASIL B~D), FDA Medical Device Cyber Guidance 등에서 추적성(Traceability) 증적 요구
- **회귀 비용 폭증**: 레거시 금융 코어, 빌링 시스템 등 변경 빈도는 낮으나 한 번의 결함 단가가 수억원인 시스템

```text
       기존 자동화 패러다임                    MBT 패러다임
   +----------------------+            +--------------------------+
   |  요구사항 -> 테스트     |            |  요구사항 -> 모델(FSM/UML) |
   |  시나리오(문서/스크립트) |            |  + Coverage Criteria      |
   |  -> 코드 자동화        |            |  -> Test Generator        |
   |  -> 실행/리포팅        |            |  -> Abstract Test Case    |
   +----------------------+            |  -> Adapter(Concretizer)  |
        ^ 사람이 갱신                    |  -> SUT 실행 -> Coverage  |
                                       +--------------------------+
                                            ^ 모델 1개 수정으로 전파
```

- **📢 섹션 요약 비유**: 기존 자동화가 "이미 만들어진 시험지를 매번 손으로 베끼는 행위"라면, MBT는 "교과서(모델) 한 권만 고치면 시험지·정답·채점표가 자동으로 새로 인쇄되는 출판 자동화 시스템"이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 MBT 참조 아키텍처(Generic MBT Workflow)

ISO/IEC/IEEE 29119-4와 ISTQB CT-MBT Sylllabus v1.0의 MBT Process는 다음 6단계로 구성된다.

```text
  +---------------------------------------------------------------------+
  |                       MBT Process (Generic)                        |
  +---------------------------------------------------------------------+

  +----------+    Model     +--------------+  Abstract  +--------------+
  |  SUT     | -----------►| Test Model   |-----------►|  Abstract    |
  | 명세서·  |  Extraction  | (FSM, UML,   |  Test      |  Test Cases  |
  | 요구사항 |              |  Markov, DT) |  Generation| (Symbolic)   |
  +----------+              +--------------+            +------+-------+
                                                              |
                                                              v
  +----------+   Test    +------------------+  Concret.  +--------------+
  |  SUT     | ◄--------| Test Adapter /   |◄-----------|  Test Data   |
  | (System  |  Execution| SUT Interface    |            |  Selector    |
  | Under    |          +--------+---------+            +--------------+
  | Test)    |                   |
  +----+-----+                   v
       |              +--------------------+
       |  Oracle      | Test Verdict       |
       +-------------►| (Pass / Fail /     |
                      |  Inconclusive)     |
                      +--------+-----------+
                               v
                      +--------------------+
                      | Coverage Report    |
                      | (State 100%,       |
                      |  Transition 98%,   |
                      |  Path …)           |
                      +--------------------+
```

### 2.2 핵심 구성 요소

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---------|:-----|:----------------------|
| **Test Model (테스트 모델)** | SUT의 동작을 형식적으로 표현 | FSM, EFSM(Extended FSM: 변수·가드·액션 포함), Markov Chain, UML State/Activity/Sequence Diagram, Decision Table, Pre/Post-condition 기반 **OCL(Object Constraint Language)**, **Alloy** 등 경량 형식 언어 사용 |
| **Model Editor** | 모델 작성·편집 도구 | 그래픽 편집기(GraphWalker의 JSON/YAML, MaTeLo의 SysML Editor), Textual DSL(Conformiq Designer의 Java-like Action Language), 기존 모델 임포트(PlantUML, Eclipse EMF, Papyrus) |
| **Test Generator** | 모델 -> 테스트 케이스 자동 생성 | 그래프 알고리즘(DFS/BFS, Chinese Postman, Rural Postman), SMT Solver(Z3, CVC4)로 가드 조건 만족 입력값 산출, Search-Based(Many-Objective Genetic Algorithm: NSGA-II)로 Coverage 최대화·비용 최소화 Pareto 최적 |
| **Abstract Test Case** | 생성된 추상 TC | 심볼릭 시퀀스: `S0 --login(u,p)--> S1 --transfer(amt>0)--> S2` 형태. **구체 값 바인딩 전** 상태 |
| **Test Adapter (Concretizer)** | 추상 TC -> 실행 가능한 구체 TC 변환 | SUT 인터페이스(API, GUI Driver, Protocol Stub)와 매핑. 예: `transfer(amt>0)` -> `REST POST /api/transfer {"amount": 1000}` |
| **Test Oracle** | Pass/Fail 판정 | 사후조건 검증(DB 상태, 로그), Mutation Testing 기반 Oracle 추론, Cross-Checking(동일 모델 기반 다른 구현체 비교) |

### 2.3 테스트 생성 알고리즘 핵심

#### 2.3.1 Coverage Criteria

- **State Coverage**: 모든 상태 1회 이상 방문
- **Transition (Edge) Coverage**: 모든 전이 1회 이상 트리거
- **Action Coverage**: 모든 액션 1회 이상 호출
- **N-Switch Coverage**: N개 연속 전이 조합 검증 (보통 N=0,1,2)
- **Path Coverage**: 특정 경로 조건(가드 만족 시퀀스) 충족
- **MCDC(Modified Condition/Decision Coverage)**: 가드 내부 Boolean 분기 각각이 결과에 독립적으로 영향 검증

#### 2.3.2 생성 전략 3종

| 전략 | 방식 | 장점 | 단점 |
|:-----|:-----|:-----|:-----|
| **Offline Generation** | 시작 시 모든 TC 일괄 생성 | Coverage 최적화 용이, 결정적 | 모델 크기 큼 -> 시간·메모리 폭증 |
| **On-the-Fly Generation** | 실행 시점 다음 1스텝 생성 | 무한 상태 시스템 대응, 메모리 효율 | Non-determinism로 Coverage 검증 어려움 |
| **Search-Based (Metaheuristic)** | GA·PSO·Simulated Annealing으로 TC 진화 | 현실 제약(시간·비용) 반영 | Local Optima 수렴, 정당성 증명 어려움 |

#### 2.3.3 상태 폭발 완화 기법

- **Symbolic Execution (심볼릭 실행)**: 입력을 변수로 두고 Z3 SMT Solver로 경로 조건(Path Condition) 해결 -> 무한 입력 공간 유한화
- **Abstraction & Refinement (Cegar)**: Counterexample-Guided Abstraction Refinement로 불필요 변수 제거
- **Compositional Testing**: 시스템 모듈별 부분 모델 후 Composition operator로 통합 (LTS - Labelled Transition System의 Parallel Composition)

### 2.4 MBT 도구 생태계 (2024~2026 기준)

| 분류 | 도구 | 모델 표현 | 특징 |
|:-----|:-----|:----------|:-----|
| 오픈소스 | **GraphWalker** | FSM(Petri net 호환) | Java/SQL/JMS 어댑터, CI/CD 통합 |
| 오픈소스 | **Modbat** | Java 기반 FSM + 확률 | Markov Chain 기반 확률 모델, K-framework 연동 |
| 오픈소스 | **Microsoft Spec Explorer** | .NET Cord/AsmL 모델 | 모델 검증(Verification) 동시 지원, MVFS 아키텍처 |
| 상용 | **Conformiq Designer / Test Suite** | UML/State | 자동 어댑터 생성, GPT-LLM 연동 옵션 |
| 상용 | **Leirios Test Designer** | FSM + Decision Table | 상업 MBT 도구 1위급, 인증 도메인 특화 |
| 상용 | **T-VEC** | Simulink/Matlab 모델 | 임베디드·항공·전장 도메인, DO-178C 인증 |
| 상용 | **Reactis (Reactive Systems)** | Simulink/Stateflow | C 코드 자동 생성, 안전 분석(Safety Analysis) |
| 표준기반 | **CITLAB** | CIT(Catalog of Implementation Techniques) | 도구 독립, XMI/Ecore 교환 |
| 연구용 | **UMT-GPT, MBT-LLM** | 자연어 요구사항 -> 모델 | 2024~ LLM 기반 MBT 연구 활발 (NL -> FSM 자동 변환) |

- **📢 섹션 요약 비유**: MBT 엔진은 "도시의 모든 도로를 효율적으로 순회하는 우체부 알고리즘(Chinese Postman) + 그 도로의 신호등 통과 조건을 자동으로 풀어주는 수학 선생님(SMT Solver) + 실제 차량에 짐을 싣는 포장공(Adapter)"이 합쳐진 운영체제와 같다.

---

## Ⅲ. 비교 및 연결

### 3.1 유사/대안 테스팅 방법론 비교

| 구분 | MBT(Model-Based) | RBT(Risk-Based) | BDD(Behavior-Driven) | SBT(Search-Based) | Property-Based |
|:-----|:------------------|:----------------|:----------------------|:-------------------|:----------------|
| **입력 자산** | SUT 명세 모델 | 리스크 레지스트리 | 자연어 시나리오(Gherkin) | 코드 + 휴리스틱 | 속성(Property) 명세 |
| **TC 생성** | 알고리즘 자동 | 수동 우선순위화 | 수동(Step Def) | 유전 알고리즘 | 랜덤 + Shrinking |
| **Coverage 측정** | State/Transition/MCDC | Risk-Item | Scenario | Branch/Fault | Property 만족도 |
| **강점** | 추적성·재현성 | 비즈니스 가치 정렬 | 비개발자 협업 | 복잡 가드 처리 | 무한 입력 탐색 |
| **약점** | 모델 작성 비용 | Risk 식별 주관성 | TC 수동 관리 | Local Optima | Oracle 필요 |
| **대표 도구** | Conformiq, GraphWalker | Jama, Jira+Q-Test | Cucumber, SpecFlow | EvoSuite, AETG | QuickCheck, jqwik |
| **적합 도메인** | 임베디드, 통신, 인증 | 금융·비즈니스 우선순위 | 웹 B2C, Agile | 복잡 분기 코드 | 함수형·API |

### 3.2 MBT ↔ DevOps / DevSecOps 통합

```text
  +--------------------------------------------------------------+
  |                    MBT in CI/CD Pipeline                      |
  +--------------------------------------------------------------+

  Code Push -> Build -> Unit Test (SBT) -> Model Diff (Git LFS)
                                            |
                                            v
                                +-----------------------+
                                | MBT Generator         |
                                | (Conformiq/GraphWalker)|
                                +----------+------------+
                                           v
                                +-----------------------+
                                | Test Adapter Rebuild  |
                                | (CI Cache + Diff)     |
                                +----------+------------+
                                           v
                                +-----------------------+
                                | SUT Deploy (Staging)  |
                                +----------+------------+
                                           v
                                +-----------------------+
                                | Concretize + Execute  |
                                +----------+------------+
                                           v
                                +-----------------------+
                                | Coverage Report ->     |
                                | Quality Gate          |
                                +-----------------------+
```

핵심 통합 포인트:
- **GitOps로 모델 관리**: 모델 파일을 Git LFS에 저장, PR 단위로 모델 Diff 리뷰
- **Pipeline 단계 분리**: `model-validate` -> `test-gen` -> `test-execute` -> `coverage-gate`
- **Service Virtualization(Mountebank, WireMock)** 과 연동하여 SUT 미구현 인터페이스 Stub 자동화

### 3.3 MBT와 타 품질 활동 연결

| 활동 | 연결 포인트 |
|:-----|:-----------|
| **형식 검증(Formal Verification)** | 동일 모델로 Model Checking(NuSMV, SPIN) 수행 -> 안전성 증명 + 테스트 생성 동시 활용 |
| **Mutation Testing** | Mutation Operator로 모델 변형, 각 Mutant를 Kill하는 TC를 자동 탐색 -> 모델·코드 Fault Sensitivity 측정 |
| **Fuzz Testing** | Property-Based Generator의 QuickCheck 시드를 MBT 모델 가드 조건으로 제약 -> Smart Fuzzing |
| **Chaos Engineering** | MBT 모델의 Fault 상태 전이(주입 가능한 장애)를 Chaos Monkey 시나리오로 자동 추출 |
| **AIOps / 이상 탐지** | MBT 실행 로그의 정상 Coverage Sequence를 학습 데이터로 Anomaly Detection |

- **📢 섹션 요약 비유**: MBT는 자동화의 "설계도 단계"이고, 스크립트 자동화는 "시공 단계"다. 이 둘을
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 532 / 600

<- **이전**: [531. 뮤테이션 테스팅 결함 주입 효과](/studynote/11_design_supervision/06_exam_summary/531_mutation_testing_fault_injection_effecti)
**다음**: [533. 퍼포먼스 테스팅 부하 스트레스 엔듀런스](/studynote/11_design_supervision/06_exam_summary/533_performance_testing_load_stress_enduranc/) ->

---
