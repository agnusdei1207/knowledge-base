+++
weight = 112
title = "112. 응집도 (Cohesion)"
date = "2026-05-10"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[193_cohesion_levels|응집도]] ([[193_cohesion_levels|Cohesion]])는 하나의 [[192_module_independence|모듈]](함수·클래스·패키지) 내부 요소들이 얼마나 하나의 목적을 위해 강하게 연결되어 있는지를 측정하는 척도로, 높을수록 단일 책임이 명확하고 이해하기 쉬운 [[192_module_independence|모듈]]임을 의미한다.
> 2. **가치**: [[193_cohesion_levels|응집도]]가 높은 [[192_module_independence|모듈]]은 변경 이유가 하나이므로 수정 시 영향 범위가 좁고 예측 가능하다. 반대로 [[193_cohesion_levels|응집도]]가 낮은 [[192_module_independence|모듈]]은 하나의 변경이 내부 여러 기능에 예상치 못한 사이드 이펙트(side effect)를 유발한다.
> 3. **판단 포인트**: 콘스탄틴(Larry Constantine)이 정의한 7단계 [[193_cohesion_levels|응집도]] 중 기능적 [[193_cohesion_levels|응집도]](Functional [[193_cohesion_levels|Cohesion]])가 최고이며, 우연적 [[193_cohesion_levels|응집도]](Coincidental [[193_cohesion_levels|Cohesion]])가 최저다. 실무에서는 "이 [[192_module_independence|모듈]]의 변경 이유가 몇 가지인가?"로 [[193_cohesion_levels|응집도]]를 판단한다.

---

## Ⅰ. 개요 및 필요성

[[193_cohesion_levels|응집도]]는 1974년 웨인 스티븐스(Wayne Stevens), 래리 콘스탄틴(Larry Constantine), 글렌 마이어스(Glenford Myers)가 공동 발표한 논문에서 소프트웨어 [[192_module_independence|모듈]]화의 핵심 지표로 제시되었다. 이 개념은 [[242_solid_object_oriented_design_principles|SOLID]] 원칙 중 [[243_srp_single_responsibility_principle|SRP]] ([[243_srp_single_responsibility_principle|Single Responsibility Principle]], [[355_process|단일 책임 원칙]])의 직접적 기원이 되었다.

[[193_cohesion_levels|응집도]]가 낮은 [[192_module_independence|모듈]]의 전형적 형태는 "유틸리티 클래스(utility class)"다. `StringUtil`, `CommonHelper` 같은 이름으로 관련 없는 기능들이 한 곳에 모여 있는 것이다. 이런 [[192_module_independence|모듈]]은 담당 기능이 확장될 때 [[192_module_independence|모듈]] 크기만 커지고, 특정 기능만 재사용하기 어렵다.

```text
┌─────────────────────────────────────────────────────────────┐
│          응집도 수준: 낮음 → 높음 7단계 계층                 │
├─────────────────────────────────────────────────────────────┤
│  1. 우연적 응집도 (Coincidental) ← 가장 나쁨                │
│     └─ 관련 없는 기능들이 임의로 한 모듈에 묶임              │
│  2. 논리적 응집도 (Logical)                                 │
│     └─ "이런 종류의 것"이라는 분류로 묶임                    │
│  3. 시간적 응집도 (Temporal)                                │
│     └─ 같은 시점(초기화, 종료)에 실행되어 묶임               │
│  4. 절차적 응집도 (Procedural)                              │
│     └─ 순서대로 실행되어야 해서 묶임                         │
│  5. 교환적 응집도 (Communicational)                         │
│     └─ 같은 데이터를 사용해서 묶임                           │
│  6. 순차적 응집도 (Sequential)                              │
│     └─ 한 모듈의 출력이 다음 모듈 입력이 되어 묶임           │
│  7. 기능적 응집도 (Functional) ← 가장 좋음                  │
│     └─ 단 하나의 명확한 기능을 수행                          │
└─────────────────────────────────────────────────────────────┘
```

[[193_cohesion_levels|응집도]]가 낮은 [[192_module_independence|모듈]]은 재사용성이 낮고, [[397_unit_test|단위 테스트]] 작성이 어렵고, 변경 시 예상치 못한 다른 기능에 영향을 미친다. 기술사 시험에서 [[193_cohesion_levels|응집도]]는 반드시 [[195_coupling_levels|결합도]]([[195_coupling_levels|Coupling]])와 함께 "높은 [[193_cohesion_levels|응집도]] + 낮은 [[195_coupling_levels|결합도]]"를 목표로 제시해야 한다.

- **📢 섹션 요약 비유**: 주방에서 "칼, 도마, 냄비"는 요리 도구라는 하나의 목적으로 응집되어 있다. 주방에 "칼, 도마, 드라이버, 청진기, 계산기"가 있으면 [[193_cohesion_levels|응집도]]가 낮아 필요한 도구를 찾기 어렵다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[193_cohesion_levels|응집도]]를 높이는 핵심 원칙은 SRP다. 클래스나 함수가 변경되는 이유가 단 하나여야 한다. "이 [[192_module_independence|모듈]]이 변경되려면 어떤 이유가 있어야 하는가?"라는 질문에 두 가지 이상의 답이 나오면 분리를 검토한다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 우연적 | `Utils.sendEmail(), Utils.calcTax(), Utils.readFile()` | 기능별 클래스 분리 |
| 논리적 | `IOHelper.read(), IOHelper.write(), IOHelper.compress()` | 입출력·[[347_compaction|압축]] 클래스 분리 |
| 시간적 | `init() { openDB(); loadConfig(); startLog(); }` | 각 초기화 관심사 분리 |
| 기능적 | `TaxCalculator.calculate(price)` | 이미 최적. 단일 책임 유지 |

```text
┌─────────────────────────────────────────────────────────────┐
│      기능적 응집도 설계: 단일 책임 모듈 구조                 │
├─────────────────────────────────────────────────────────────┤
│  낮은 응집도 (CommonService)                                │
│  ┌────────────────────────────────┐                         │
│  │ sendEmail()  ← 이메일 담당     │                         │
│  │ calcTax()    ← 세금 담당       │ ← 변경 이유 3가지       │
│  │ validateAge() ← 검증 담당      │                         │
│  └────────────────────────────────┘                         │
│                                                             │
│  높은 응집도 (분리 후)                                      │
│  [EmailService] [TaxPolicy] [AgeValidator]                  │
│  각자 단일 목적 → 변경 이유 각각 1가지                       │
└─────────────────────────────────────────────────────────────┘
```

패키지(package) 수준에서도 [[193_cohesion_levels|응집도]] 원칙이 적용된다. 패키지 [[193_cohesion_levels|응집도]] 원칙(Package [[193_cohesion_levels|Cohesion]] Principles) 중 REP (Reuse-Release Equivalence Principle, 재사용-릴리즈 등가 원칙)는 함께 재사용되는 클래스들이 같은 패키지에 있어야 한다는 [[193_cohesion_levels|응집도]] 관점이다.

- **📢 섹션 요약 비유**: 도서관에서 경영학 서적, 프로그래밍 책, 요리책, 여행 가이드가 하나의 서가에 섞여 있으면 원하는 책을 찾기 어렵다. 주제별로 응집되어야 빠르게 원하는 정보를 얻을 수 있다.

---
## Ⅲ. 비교 및 연결

[[193_cohesion_levels|응집도]]와 [[195_coupling_levels|결합도]]([[195_coupling_levels|Coupling]])는 항상 함께 이야기되며, 소프트웨어 설계 품질의 양대 축이다.

| 비교 축 | A | B |
|:---|:---|:---|
| **대상** | [[192_module_independence|모듈]] 내부 요소 간 [[083_relationship_in_er_model|관계]] | 서로 다른 [[192_module_independence|모듈]] 간 [[083_relationship_in_er_model|관계]] |
| **목표** | 높을수록 좋음 | 낮을수록 좋음 |
| **위반 결과** | 변경 파급 범위 확산 | 연쇄 변경 필요 |
| **측정 기준** | 변경 이유의 수 | 의존성 연결의 수 |

[[193_cohesion_levels|응집도]]와 SRP의 [[083_relationship_in_er_model|관계]]는 표리부동하다. SRP는 "클래스의 변경 이유는 하나여야 한다"는 원칙이고, 이를 만족하면 자연스럽게 기능적 [[193_cohesion_levels|응집도]]가 달성된다. 반면 SRP를 너무 작은 단위로 쪼개면 오히려 [[193_cohesion_levels|응집도]]는 높지만 협력을 위한 [[195_coupling_levels|결합도]]가 높아지는 트레이드오프가 생긴다.

- **📢 섹션 요약 비유**: 프로야구 팀에서 투수는 투수 역할만(높은 [[193_cohesion_levels|응집도]]), 포수는 포수 역할만 한다. 하지만 팀 안에서 서로 [[130_signal|신호]]([[195_coupling_levels|결합도]])로 긴밀하게 협력한다. [[193_cohesion_levels|응집도]]와 [[195_coupling_levels|결합도]]는 분리되지만 함께 관리해야 한다.

---
## Ⅳ. 실무 적용 및 기술사 판단

실무 코드 리뷰에서 [[193_cohesion_levels|응집도]] 점검의 가장 빠른 방법은 클래스의 인스턴스 변수들이 모든 메서드에서 공통으로 사용되는지 확인하는 것이다. 특정 메서드들만 일부 인스턴스 변수를 사용하면 해당 그룹을 별도 클래스로 분리하는 것을 검토해야 한다.

### 판단 [[435_checklist_based_testing|체크리스트]]
1. 이 [[192_module_independence|모듈]](클래스/함수)의 변경 이유가 두 가지 이상인가?
2. 클래스 내 일부 메서드들이 다른 인스턴스 변수에 전혀 접근하지 않는가?
3. "Utils", "Helper", "Common"이라는 이름이 붙은 클래스인가? (위험 [[130_signal|신호]])
4. 7단계 [[193_cohesion_levels|응집도]] 중 어느 수준에 해당하는지 분류할 수 있는가?
5. 패키지 내 클래스들이 함께 릴리즈·재사용되는 응집된 단위를 구성하는가?

- **📢 섹션 요약 비유**: 병원에서 내과·외과·소아과가 각각의 진료실로 분리된 것은 [[193_cohesion_levels|응집도]]가 높은 구조다. 한 방에서 모든 진료를 보면 의사도 환자도 혼란스럽다.

---

## Ⅴ. 기대효과 및 결론

[[193_cohesion_levels|응집도]]가 높은 [[192_module_independence|모듈]]은 재사용성이 높고 독립적으로 테스트할 수 있다. 변경 이유가 하나이므로 수정 시 영향 범위를 사전에 예측할 수 있어 유지보수 비용이 감소한다. [[213_msa_microservices_architecture|마이크로서비스 아키텍처]]([[619_msa_traffic_hardware|MSA]])에서 [[090_service_kubernetes_network_load_balancing|서비스]] 경계를 [[064_relation_domain|도메인]] 기능 [[193_cohesion_levels|응집도]]를 기준으로 나누면 [[090_service_kubernetes_network_load_balancing|서비스]] 간 불필요한 통신이 줄어든다.

한계는 [[193_cohesion_levels|응집도]]를 높이기 위한 과도한 분리가 오히려 작은 클래스가 폭발적으로 늘어나는 "클래스 폭발(class explosion)" 문제로 이어질 수 있다는 점이다. 특히 빈약한 [[064_relation_domain|도메인]] 모델(Anemic [[064_relation_domain|Domain]] Model)이나 지나치게 세분화된 [[090_service_kubernetes_network_load_balancing|서비스]]들이 여러 홉(hop)의 통신을 필요로 하는 [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]] 문제를 일으킬 수 있다.

미래 방향으로는 ① [[190_ai_llm_requirements_specification|AI]] 정적 분석으로 [[193_cohesion_levels|응집도]] 자동 측정 및 [[213_refactoring_cloud_native_rearchitecture|리팩토링]] 제안, ② [[619_msa_traffic_hardware|MSA]] [[090_service_kubernetes_network_load_balancing|서비스]] 경계 자동 최적화, ③ [[310_architecture|도메인 주도 설계]]([[310_architecture|DDD]]) [[221_bounded_context_ddd_msa_boundary|바운디드 컨텍스트]]가 [[193_cohesion_levels|응집도]]의 아키텍처 수준 표현으로 정착되는 흐름이 있다.

[[193_cohesion_levels|응집도]]는 단순히 "기능을 묶어라"가 아니라 "하나의 변경 이유를 공유하는 것들을 하나의 경계 안에 담아라"는 정밀한 설계 판단의 결과물로 기억해야 한다.

- **📢 섹션 요약 비유**: 훌륭한 소설가는 각 챕터가 하나의 주제를 가지도록 글을 쓴다. 한 챕터에 연애, 요리, 미스터리, 스포츠가 뒤섞이면 독자는 무엇을 읽고 있는지 잃어버린다.

---

### 📌 관련 개념 맵

[모듈화] → [응집도] → [[[243_srp_single_responsibility_principle|SRP]]] → [패키지 [[193_cohesion_levels|응집도]] 원칙] → [[[619_msa_traffic_hardware|MSA]] [[090_service_kubernetes_network_load_balancing|서비스]] 경계 설계]

| 개념 | 연결 포인트 |
|:---|:---|
| [[243_srp_single_responsibility_principle|SRP]] ([[355_process|단일 책임 원칙]]) | [[193_cohesion_levels|응집도]]의 클래스 수준 구체화 원칙 |
| [[195_coupling_levels|결합도]] ([[195_coupling_levels|Coupling]]) | [[193_cohesion_levels|응집도]]와 함께 [[192_module_independence|모듈]] 설계 품질의 양대 축 |
| [[310_architecture|DDD]] [[221_bounded_context_ddd_msa_boundary|바운디드 컨텍스트]] | [[193_cohesion_levels|응집도]]의 아키텍처 수준 표현 |
| [[619_msa_traffic_hardware|MSA]] [[090_service_kubernetes_network_load_balancing|서비스]] 분해 | 높은 [[193_cohesion_levels|응집도]]를 기준으로 [[090_service_kubernetes_network_load_balancing|서비스]] 경계를 [[009_config|설정]] |

### 📈 관련 키워드 및 발전 흐름도

[모듈화 연구] → [응집도 7단계 정립(콘스탄틴)] → [[[243_srp_single_responsibility_principle|SRP]]·[[242_solid_object_oriented_design_principles|SOLID]] 원칙] → [[[310_architecture|DDD]] 바운디드 컨텍스트] → [[[619_msa_traffic_hardware|MSA]] [[090_service_kubernetes_network_load_balancing|서비스]] 경계 설계] → [[[190_ai_llm_requirements_specification|AI]] 기반 [[193_cohesion_levels|응집도]] 자동 측정]

### 👶 어린이를 위한 3줄 비유 설명

1. 책가방에 국어책, 수학책, 영어책만 넣으면 학교 공부 준비가 잘 된 거예요 (높은 [[193_cohesion_levels|응집도]]).
2. 책가방에 교과서, 운동화, 점심 도시락, 우산이 섞여 있으면 책 찾기가 힘들어요 (낮은 [[193_cohesion_levels|응집도]]).
3. 같은 목적의 것들끼리 묶어두면 필요할 때 바로 꺼낼 수 있어요!
