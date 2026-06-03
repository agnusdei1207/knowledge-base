+++
title = "127. 정보공학 방법론 (IE, Information 엔진ering) - 데이터 중심 시스템 개발"
date = 2026-04-19

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: IE(Information 엔진ering)는 <strong>기업 전체 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 중심으로 정보 시스템을 체계적으로 개발</strong>하는 방법론으로, [ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/101_isp_information_strategy_planning_4_steps/)(정보전략계획)→BAA(업무영역분석)→BSD(시스템 설계)→SC(구축)의 4단계로 구성된다.
> 2. **가치**: 프로세스 중심 개발은 시스템마다 독립적으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 설계하여 <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 중복·불일치</strong>가 발생하지만, IE는 <strong>전사 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/">데이터 모델</a>을 먼저 수립</strong>하여 시스템 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 보장한다.
> 3. **판단 포인트**: IE는 James Martin(1981)이 제안했으며, 구조적 방법론과 달리 <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>(What)를 프로세스(How)보다 우선</strong>시한다. ERD·CRUD 매트릭스가 핵심 산출물이다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    IE 4단계                                           │
├───────────────────────────────────────────────────────┤
│  1단계: ISP (정보전략계획)                            │
│   → 전사 데이터 모델·업무 기능 정의                  │
│  2단계: BAA (업무영역분석)                            │
│   → 엔터티·관계·프로세스 상세 분석                   │
│  3단계: BSD (시스템 설계)                              │
│   → 논리·물리 데이터 모델·프로그램 설계              │
│  4단계: SC (시스템 구축)                               │
│   → 코딩·테스트·이행                                 │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: IE는 도시 계획([ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/101_isp_information_strategy_planning_4_steps/))→구역 설계(BAA)→건물 설계(BSD)→시공(SC)처럼 <strong>큰 그림(전사)에서 세부(시스템)</strong>로 내려가는 [Top-Down](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/402_top_down_integration/) 접근이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### IE vs 구조적 vs 객체지향

| 비교 | 구조적 | IE | 객체지향 |
|:---|:---|:---|:---|
| **중심** | 프로세스 | <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a></strong> | 객체 |
| **산출물** | [DFD](/knowledge-base/studynote/04_software_engineering/03_design_architecture/144_dfd_data_flow_diagram/) | **ERD** | [Class Diagram](/knowledge-base/studynote/04_software_engineering/04_testing_quality/233_class_diagram_static_structure_uml/) |
| **접근** | [Bottom-Up](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/403_bottom_up_integration/) | <strong><a href="/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/402_top_down_integration/">Top-Down</a></strong> | Iterative |

- **📢 섹션 요약 비유**: 구조적은 "무엇을 하는가(프로세스)", IE는 "무엇을 관리하는가([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))", 객체지향은 "누가 하는가(객체)"에 초점.

---

## Ⅲ. 비교 및 연결

| 비교 | 프로세스 중심 | [데이터 중심](/knowledge-base/studynote/04_software_engineering/06_software_architecture/383_data_centric_architecture/) (IE) |
|:---|:---|:---|
| **중복** | 시스템마다 독립 | **전사 통합** |
| **변경** | 프로세스 변경 시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)도 | <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 안정</strong> |
| <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a></strong> | 낮음 | **높음** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### IE 핵심 산출물
1. **ERD**: 엔터티-관계 다이어그램.
2. **CRUD 매트릭스**: 프로세스×엔터티 매핑.
3. **엔터티 정의서**: [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)·[도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)·규칙 정의.

---

## Ⅴ. 기대효과 및 결론

IE는 <strong>전사 <a href="/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/">데이터 아키텍처</a>의 이론적 기반</strong>이며, 현대의 [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/)·MDM의 뿌리이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/12_it_management/03_ea_isp/101_isp_information_strategy_planning_4_steps/">ISP</a></strong> | IE 1단계 (전사 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)) |
| **ERD** | IE의 핵심 산출물 |
| **CRUD 매트릭스** | 프로세스-엔터티 매핑 |
| **James Martin** | IE 창시자 |
| <strong><a href="/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/">DA</a> (<a href="/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/">데이터 아키텍처</a>)</strong> | IE의 현대적 진화 |

### 📈 관련 키워드 및 발전 흐름도

```text
[구조적 방법론 (DFD, 1970s)]
    │
    ▼
[정보공학 (IE, James Martin, 1981) — 데이터 중심]
    │
    ▼
[객체지향 (UML, 1990s)]
    │
    ▼
[Agile + DDD (2000s~)]
    │
    ▼
[현재: 데이터 아키텍처 + 데이터 메시 — IE의 진화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. IE는 <strong>도시 계획</strong>이에요. 도시(회사) 전체 지도를 먼저 그리고, 건물(시스템)을 짓는 거예요.
2. 지도(전사 [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/)) 없이 건물만 짓면 <strong>도로(<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>)가 안 맞아요</strong>.
3. 큰 그림부터 그리면 **모든 건물이 조화롭게** 연결된답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 127 / 600

← **이전**: [126. 데이터 표준화 (단어·도메인·용어) - 전사 데이터 용어 통일 체계](/knowledge-base/studynote/05_database/02_modeling_normalization/126_data_standardization_word_domain_term/)
**다음**: [128. 논리적 데이터 독립성 & 뷰 (Logical Data Independence & View)](/knowledge-base/studynote/05_database/02_modeling_normalization/128_logical_data_independence_view/) →

---
