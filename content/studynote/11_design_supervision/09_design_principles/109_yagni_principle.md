+++
title = "109. YAGNI 원칙 (You Aren't Gonna Need It)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)
- YAGNI는 아직 요구되지 않은 기능·계층·확장 포인트를 미리 만들지 말라는 실용주의 설계 원칙이다.
- 오버엔지니어링을 줄이면 개발 속도, 테스트 범위, 유지보수 비용이 함께 낮아진다.
- 핵심은 미래를 무시하는 것이 아니라, 실제 요구가 생겼을 때 안전하게 리팩터링할 수 있도록 단순하게 시작하는 데 있다.

## Ⅰ. 개요 및 필요성
YAGNI는 "언젠가 필요할지도 모른다"는 추측을 설계 근거로 삼지 말라고 요구한다. 사용되지 않는 옵션 컬럼, 호출되지 않는 인터페이스, 한 번도 연결되지 않은 확장 포인트는 모두 시스템을 무겁게 만드는 설계 부채다. 특히 감리나 아키텍처 검토에서는 이런 선행 구현이 기능 범위 왜곡과 예산 낭비의 신호로 해석된다.

```text
+------------------------------+
| 추측 기반 설계의 전개        |
+------------------------------+
| 현재 요구 1개                |
|        |                     |
|        +- "나중에 다국어?"   |
|        +- "나중에 멀티DB?"   |
|        +- "나중에 SaaS?"     |
|              |               |
|      미사용 코드·테이블·API  |
|              |               |
|         복잡도와 비용 증가    |
+------------------------------+
```

요구가 불확실할수록 정답은 거대한 선행 설계가 아니라 변경하기 쉬운 작은 구조다. 그래서 YAGNI는 [MVP](/knowledge-base/studynote/12_it_management/01_governance_strategy/036_mvp/), [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/), 점진적 리팩터링을 가능하게 하는 출발점으로 다뤄진다.
- **📢 섹션 요약 비유**: 아직 손님도 오지 않았는데 의자 100개를 먼저 사 두는 식당은 공간과 청소비만 늘어납니다.

## Ⅱ. 아키텍처 및 핵심 원리
YAGNI의 핵심은 "지금 필요한 최소 구조 + 나중에 바꿀 수 있는 여지"의 균형이다. 미래 대비는 거대한 틀을 선행 구축하는 일이 아니라, 변경 비용을 낮추는 설계 습관을 만드는 일에 가깝다.

```text
+------------+    +------------+    +------------+    +------------+
| 실제 요구   |--->| 최소 구현   |--->| 운영 피드백 |--->| 필요한 만큼 |
| 확인        |    | 배포        |    | 수집        |    | 리팩터링    |
+------------+    +------------+    +------------+    +------------+
```

| 실천 원리 | 설명 | 설계 판단 포인트 |
| :--- | :--- | :--- |
| 현재 요구 우선 | 승인된 요구사항과 실제 사용 시나리오에만 코드를 맞춘다. | "이 기능을 지금 누가 언제 쓰는가?" |
| 단순한 시작 | [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)는 반복되는 변화가 확인된 뒤 도입한다. | "중복이 현실인가, 상상인가?" |
| 리팩터링 전제 | 미래 확장은 선행 구현이 아니라 구조 개선으로 대응한다. | "변경을 받쳐 줄 테스트와 경계가 있는가?" |

YAGNI는 KISS와 함께 복잡성을 덜어내고, DRY와는 무리한 조기 통합을 경계하는 보완 관계를 만든다. 즉 "미리 만들지 말 것"과 "나중에 쉽게 고칠 것"을 동시에 요구하는 원칙이다.
- **📢 섹션 요약 비유**: 아이가 아직 걷지도 않았는데 성인용 자전거를 사 주기보다, 지금 맞는 신발을 신기고 크면 바꾸는 편이 더 현명합니다.

## Ⅲ. 비교 및 연결
| 원칙 | 핵심 질문 | YAGNI와의 공통점 | 차이점 |
| :--- | :--- | :--- | :--- |
| [YAGNI](/knowledge-base/studynote/11_design_supervision/06_exam_summary/362_yagni/) | "지금 꼭 필요한가?" | 현재 가치 중심으로 설계를 줄인다. | 기능 선행 구현 자체를 직접 금지한다. |
| [KISS](/knowledge-base/studynote/04_software_engineering/04_testing_quality/249_kiss_keep_it_simple_stupid/) | "더 단순하게 풀 수 있는가?" | 복잡도를 줄여 이해와 수정을 쉽게 한다. | 구현 방식의 단순화에 더 초점을 둔다. |
| DRY | "같은 지식이 중복되는가?" | 불필요한 코드 증식을 막는다. | 너무 이른 공통화는 오히려 [YAGNI](/knowledge-base/studynote/11_design_supervision/06_exam_summary/362_yagni/) 위반이 될 수 있다. |
| [OCP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/746_ocp/) | "변경 없이 확장 가능한가?" | 변화 대응력을 중시한다. | YAGNI는 확장 지점의 조기 도입을 경계한다. |

YAGNI는 다른 설계 원칙을 부정하지 않는다. 다만 원칙 적용의 시점을 늦춰, 실제 변화 패턴이 확인된 뒤 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)와 일반화를 하라고 요구한다.
- **📢 섹션 요약 비유**: 여행 짐을 쌀 때 YAGNI는 "혹시 모르니"라는 이유로 가져가는 물건부터 빼내는 정리 원칙입니다.

## Ⅳ. 실무 적용 및 기술사 판단
실무에서는 API의 예비 파라미터, 데이터베이스의 `extra1`, `extra2` 같은 컬럼, 인터페이스 하나에 구현체 하나뿐인 구조가 대표적인 [YAGNI](/knowledge-base/studynote/11_design_supervision/06_exam_summary/362_yagni/) 위반 신호다. 기술사 판단에서는 단순히 기능을 적게 만드는 태도가 아니라, 실제 수요와 변경 비용을 근거로 설계 범위를 통제하는 능력이 중요하다.

요구가 확실해질 때까지는 단순하게 유지하되, [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 경계와 테스트를 확보해 두어야 한다. 그래야 나중에 기능이 추가되어도 "미리 만들지 않았던 비용"보다 "뒤늦게 바꾸는 이익"이 더 커진다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- 현재 백로그·요구사항 문서·사용 시나리오에 없는 기능을 선행 구현하고 있지 않은가?
- 단 하나의 예상 고객이나 막연한 미래 시나리오 때문에 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 계층을 늘리고 있지 않은가?
- 실제로 호출되지 않는 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 필드, DB 컬럼, [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 키가 배포 산출물에 포함되어 있지 않은가?
- 확장이 필요해질 경우를 대비한 테스트, [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 경계, 리팩터링 여지는 확보되어 있는가?
- "나중에 필요할 수 있음"이 아니라 "언제, 누가, 왜 필요함"으로 설명할 수 있는가?

- **📢 섹션 요약 비유**: 비가 올지 몰라 우산 창고를 짓는 것보다, 일기예보를 보고 필요할 때 우산을 꺼내는 집이 훨씬 경제적입니다.

## Ⅴ. 기대효과 및 결론
YAGNI를 지키면 코드량이 줄고, 테스트 범위가 작아지며, 팀이 진짜 필요한 기능에 집중할 수 있다. 또한 사용되지 않는 설계 가설을 제거하므로 장애 분석과 인수인계가 쉬워지고, 변경 시 영향 범위도 더 명확해진다.

결론적으로 YAGNI는 미래를 포기하는 원칙이 아니라, 미래 예측 실패의 비용을 최소화하는 원칙이다. "작성하지 않은 코드가 가장 싸고 안전한 코드"라는 사실을 조직적으로 실천하게 만든다.
- **📢 섹션 요약 비유**: 집 안에 쓰지도 않을 방을 미리 열 개 더 짓기보다, 정말 필요할 때 증축하는 집이 관리도 쉽고 돈도 덜 듭니다.

### 📌 관련 개념 맵
- <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/073_xp_extreme_programming/">XP</a></strong>: "가장 단순하게 동작하는 것"을 우선 구현한다.
- <strong><a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/249_kiss_keep_it_simple_stupid/">KISS</a></strong>: 현재 구현의 복잡도를 줄이는 방향으로 함께 작동한다.
- <strong><a href="/knowledge-base/studynote/12_it_management/01_governance_strategy/036_mvp/">MVP</a></strong>: 최소 기능으로 시장 검증을 수행한다.
- <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/078_refactoring_code_smells/">Refactoring</a></strong>: 실제 요구가 생긴 뒤 구조를 안전하게 확장한다.

### 📈 관련 키워드 및 발전 흐름도
```text
요구 불확실성 증가
    |
    v
추측성 설계와 오버엔지니어링 발생
    |
    v
YAGNI 원칙 적용
    |
    v
MVP 출시와 사용자 피드백 확보
    |
    v
리팩터링 기반의 점진 확장 정착
```

### 👶 어린이를 위한 3줄 비유 설명
1. 내일 뭘 입을지 모르는데 옷을 열 벌씩 껴입고 학교에 가면 너무 불편해요.
2. 오늘 필요한 옷만 입고, 날씨가 바뀌면 그때 맞게 갈아입는 게 더 똑똑해요.
3. YAGNI는 "아직 안 필요한 건 지금 만들지 말자"라고 말해 주는 원칙이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 160 / 530

<- **이전**: [108. KISS 원칙 (Keep It Simple, Stupid)](/knowledge-base/studynote/11_design_supervision/09_design_principles/108_kiss_principle/)
**다음**: [109. 불필요한 기능 구현 금지 원칙 (YAGNI, You Aren't Gonna Need It)](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/109_yagni_you_arent_gonna_need_it/) ->

---
