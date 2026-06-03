+++
weight = 113
title = "113. 결합도 (Coupling)"
date = "2026-05-10"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)
- [[195_coupling_levels|결합도]]는 서로 다른 [[192_module_independence|모듈]]이 얼마나 강하게 서로에게 의존하는지를 나타내는 지표이며, 낮을수록 좋다.
- [[195_coupling_levels|결합도]]가 높으면 한 [[192_module_independence|모듈]]의 구조 변경이 다른 [[192_module_independence|모듈]]의 수정과 장애로 쉽게 전파된다.
- 좋은 설계는 [[001_dikw_pyramid|데이터]] [[195_coupling_levels|결합도]] 수준을 지향하고, 내용 [[195_coupling_levels|결합도]]·공통 [[195_coupling_levels|결합도]] 같은 강한 연결을 피한다.

## Ⅰ. 개요 및 필요성
[[195_coupling_levels|결합도]]는 [[192_module_independence|모듈]] 간 변화 전파의 크기를 보여 주는 대표 지표다. 두 [[192_module_independence|모듈]]이 구체 구현, 전역 상태, 내부 메모리 구조까지 공유하면 작은 변경도 시스템 전체 수정으로 번진다. 반대로 인터페이스와 최소 [[001_dikw_pyramid|데이터]]만 주고받으면 각 [[192_module_independence|모듈]]은 독립적으로 개발·테스트·배포되기 쉬워진다.

```text
┌────────────┐    전역상태 공유    ┌────────────┐
│ Module A   │◀──────────────────▶│ Module B   │
└────────────┘                    └────────────┘
       │                                  │
       └──── 내부 구조까지 엮이면 변경이 서로에게 바로 전염됨 ────┘
```

그래서 [[195_coupling_levels|결합도]] 평가는 단순한 연결 개수보다도, "무엇을 공유하는가"를 묻는 작업이다. [[001_dikw_pyramid|데이터]]만 공유하는지, 제어 신호를 넘기는지, 내부 내용을 침범하는지가 품질 차이를 만든다.
- **📢 섹션 요약 비유**: 레고 블록은 살짝 끼워서 필요할 때 떼어낼 수 있지만, 본드로 붙여 버리면 하나를 바꾸려다 전부 망가집니다.

## Ⅱ. 아키텍처 및 핵심 원리
[[195_coupling_levels|결합도]]는 약한 쪽에서 강한 쪽으로 갈수록 설계 품질이 나빠진다. 이상적인 방향은 필요한 [[001_dikw_pyramid|데이터]]만 계약에 맞춰 주고받는 구조다.

```text
┌──────────────┐
│ 데이터 결합도 │  자료 요소만 전달, 가장 바람직
├──────────────┤
│ 스탬프 결합도 │  구조체·객체 전체 전달
├──────────────┤
│ 제어 결합도   │  처리 분기를 제어 플래그로 전달
├──────────────┤
│ 외부 결합도   │  파일·프로토콜·장치 규약 공동 의존
├──────────────┤
│ 공통 결합도   │  전역 변수·공유 메모리 사용
├──────────────┤
│ 내용 결합도   │  타 모듈 내부를 직접 참조, 최악
└──────────────┘
```

| 결합 유형 | 설명 | 설계 판단 |
| :--- | :--- | :--- |
| [[001_dikw_pyramid|데이터]] [[195_coupling_levels|결합도]] | 필요한 값만 파라미터로 전달한다. | 가장 권장되는 형태 |
| 스탬프 [[195_coupling_levels|결합도]] | 객체 전체를 넘겨 일부만 사용한다. | 과한 [[001_dikw_pyramid|데이터]] 전달 여부 점검 |
| 제어 [[195_coupling_levels|결합도]] | [[186_character_stuffing_dle_stx_etx|플래그]] 값으로 상대 [[192_module_independence|모듈]] 로직을 지시한다. | 책임 분리 재검토 필요 |
| 외부 [[195_coupling_levels|결합도]] | 동일한 외부 포맷·장비·프로토콜에 묶인다. | 표준화·[[259_adapter_pattern_interface_wrapper|어댑터]] 고려 |
| 공통 [[195_coupling_levels|결합도]] | 전역 변수나 공유 상태를 함께 사용한다. | 장애 전파 위험 큼 |
| 내용 [[195_coupling_levels|결합도]] | 다른 [[192_module_independence|모듈]]의 내부 자료·코드를 직접 건드린다. | 즉시 제거 대상 |

낮은 [[195_coupling_levels|결합도]]는 무조건 연결을 끊는 뜻이 아니다. 필요한 연결은 유지하되, 계약을 단순화하고 공유 범위를 최소화하여 변경 영향을 국소화하는 것이 핵심이다.
- **📢 섹션 요약 비유**: 필요한 말만 메모지로 주고받으면 되는데, 서로의 공책 전체를 늘 바꿔 써 버리면 숙제 한 줄 바뀔 때마다 모두 다시 써야 합니다.

## Ⅲ. 비교 및 연결
| 항목 | 낮은 [[195_coupling_levels|결합도]] | 높은 [[195_coupling_levels|결합도]] | 연결 개념 |
| :--- | :--- | :--- | :--- |
| 변경 영향 | 계약 범위 안에서 국소적으로 수정된다. | 한쪽 변경이 여러 [[192_module_independence|모듈]]로 확산된다. | [[346_maintainability_portability|Maintainability]] |
| 테스트성 | 대역 객체와 인터페이스 기반 테스트가 쉽다. | 실제 환경과 전체 연결을 띄워야 검증된다. | Test [[195_isolation_concurrency_control|Isolation]] |
| 배포 유연성 | [[192_module_independence|모듈]]별 [[430_index_fast_full_scan|병렬]] 개발과 교체가 쉽다. | 동시 수정·동시 배포 압력이 커진다. | Modularity |
| [[193_cohesion_levels|응집도]]와 [[083_relationship_in_er_model|관계]] | 내부 책임이 단단할수록 낮추기 쉽다. | 내부 책임이 흐릴수록 외부 의존이 늘어난다. | High [[193_cohesion_levels|Cohesion]] |

[[195_coupling_levels|결합도]]는 [[193_cohesion_levels|응집도]]와 함께 봐야 의미가 완성된다. 외부 연결이 단순하면서 내부 책임이 분명할 때 비로소 안정적인 [[192_module_independence|모듈]] 경계가 만들어진다.
- **📢 섹션 요약 비유**: 반 친구끼리 필요한 연락만 주고받으면 반이 조용하지만, 모두가 서로의 일기장까지 공유하면 사소한 일도 큰 소동이 됩니다.

## Ⅳ. 실무 적용 및 기술사 판단
실무에서는 인터페이스 기반 설계, [[337_dependency_injection|의존성 주입]], 이벤트 발행/구독, [[263_facade_pattern_simplified_interface|퍼사드]], 안티코럽션 계층이 [[195_coupling_levels|결합도]] 저감 수단으로 자주 쓰인다. 기술사 판단에서는 단순히 [[090_service_kubernetes_network_load_balancing|서비스]] 수를 늘리는 것보다, [[192_module_independence|모듈]] 간 계약이 얼마나 단순하고 안정적인지, 전역 상태와 내부 침범이 얼마나 제거되었는지가 핵심이다.

특히 MSA나 외부 연계 시스템에서는 네트워크 호출 자체보다 계약 변화와 장애 전파가 더 큰 문제다. 따라서 느슨한 결합은 코드 차원을 넘어 [[014_api_posix|API]] [[288_version_ihl_tos_total_length|버전]] [[268_strategy_pattern|전략]], 메시지 [[005_schema|스키마]] 관리, 공통 [[336_library_vs_framework|라이브러리]] 의존 통제까지 포함해 봐야 한다.

### 판단 [[435_checklist_based_testing|체크리스트]]
- [[192_module_independence|모듈]] 간에 필요한 [[001_dikw_pyramid|데이터]]만 전달하고, 불필요한 객체 전체를 넘기지 않는가?
- 전역 변수, 싱글턴 상태, 공유 캐시를 통해 암묵적으로 강하게 연결되어 있지 않은가?
- 제어 [[186_character_stuffing_dle_stx_etx|플래그]]로 상대 [[192_module_independence|모듈]]의 세부 동작을 지시하고 있지 않은가?
- 외부 시스템 변경이 내부 여러 [[192_module_independence|모듈]]에 동시 수정으로 번지지 않도록 [[259_adapter_pattern_interface_wrapper|어댑터]]나 [[263_facade_pattern_simplified_interface|퍼사드]]를 두었는가?
- 내부 구현 교체 시 외부 계약을 유지할 수 있는 [[198_abstraction_control_data_process|추상화]] 경계가 있는가?

- **📢 섹션 요약 비유**: 아파트 세대마다 현관문만 통해 드나들면 편하지만, 벽을 뚫어 서로 연결해 두면 한 집 공사할 때 온 동네가 시끄러워집니다.

## Ⅴ. 기대효과 및 결론
[[195_coupling_levels|결합도]]를 낮추면 변경이 국소화되고, 단위 테스트가 쉬워지며, 팀 간 [[430_index_fast_full_scan|병렬]] 개발과 기능 교체가 수월해진다. 또한 장애가 발생해도 전파 범위가 작아져 운영 안정성과 [[658_ir_recovery|복구]] 속도가 좋아진다.

결론적으로 낮은 [[195_coupling_levels|결합도]]는 유연한 아키텍처의 필수 조건이다. [[193_cohesion_levels|응집도]] 높은 [[192_module_independence|모듈]]들이 단순한 계약으로 연결될 때, 시스템은 커져도 통제 가능성을 잃지 않는다.
- **📢 섹션 요약 비유**: 전자제품을 콘센트 규격만 맞춰 꽂으면 교체가 쉽듯이, [[192_module_independence|모듈]]도 연결 규칙만 단순하면 오래 [[289_cqrs_db|쓰기]] 편합니다.

### 📌 관련 개념 맵
- **[[247_dip_dependency_inversion_principle|DIP]]**: 구체 구현 대신 [[198_abstraction_control_data_process|추상화]]에 의존해 결합을 낮춘다.
- **[[190_enterprise_di_framework_lifecycle|DI]]**: 객체 생성과 사용을 분리하여 직접 의존을 줄인다.
- **[[064_eda|EDA]]**: 직접 호출 대신 이벤트를 통해 시공간 결합을 완화한다.
- **[[193_cohesion_levels|응집도]]**: 내부 책임이 단단할수록 외부 [[195_coupling_levels|결합도]]는 낮추기 쉽다.

### 📈 관련 키워드 및 발전 흐름도
```text
모듈 간 직접 참조와 전역상태 증가
    │
    ▼
변경 파급·테스트 곤란·동시 배포 압박
    │
    ▼
인터페이스·DI·이벤트 기반 분리 적용
    │
    ▼
데이터 중심 계약으로 단순화
    │
    ▼
느슨한 결합과 독립 배포 역량 확보
```

### 👶 어린이를 위한 3줄 비유 설명
1. 블록을 살짝 끼워 놓으면 하나를 떼어 다른 모양으로 쉽게 바꿀 수 있어요.
2. 그런데 풀로 꽉 붙여 버리면 작은 블록 하나 바꾸려다 다 망가져요.
3. [[195_coupling_levels|결합도]]는 "서로 얼마나 세게 붙어 있나"를 보는 기준이에요.
