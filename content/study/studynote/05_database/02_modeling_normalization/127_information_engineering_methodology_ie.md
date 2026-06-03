---
title: 127. 정보공학 방법론 (IE, Information Engineering) - 데이터 중심 시스템 개발
date: '2026-04-19'
tags:
- studynote-database
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: IE(Information Engineering)는 **기업 전체 [[001_dikw_pyramid|데이터]]를 중심으로 정보 시스템을 체계적으로 개발**하는 방법론으로, [[101_isp_information_strategy_planning_4_steps|ISP]](정보전략계획)→BAA(업무영역분석)→BSD(시스템 설계)→SC(구축)의 4단계로 구성된다.
> 2. **가치**: 프로세스 중심 개발은 시스템마다 독립적으로 [[001_dikw_pyramid|데이터]]를 설계하여 **[[001_dikw_pyramid|데이터]] 중복·불일치**가 발생하지만, IE는 **전사 [[014_data_model_components|데이터 모델]]을 먼저 수립**하여 시스템 간 [[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]]을 보장한다.
> 3. **판단 포인트**: IE는 James Martin(1981)이 제안했으며, 구조적 방법론과 달리 **[[001_dikw_pyramid|데이터]](What)를 프로세스(How)보다 우선**시한다. ERD·CRUD 매트릭스가 핵심 산출물이다.

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

- **📢 섹션 요약 비유**: IE는 도시 계획([[101_isp_information_strategy_planning_4_steps|ISP]])→구역 설계(BAA)→건물 설계(BSD)→시공(SC)처럼 **큰 그림(전사)에서 세부(시스템)**로 내려가는 [[402_top_down_integration|Top-Down]] 접근이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### IE vs 구조적 vs 객체지향

| 비교 | 구조적 | IE | 객체지향 |
|:---|:---|:---|:---|
| **중심** | 프로세스 | **[[001_dikw_pyramid|데이터]]** | 객체 |
| **산출물** | [[144_dfd_data_flow_diagram|DFD]] | **ERD** | [[233_class_diagram_static_structure_uml|Class Diagram]] |
| **접근** | [[403_bottom_up_integration|Bottom-Up]] | **[[402_top_down_integration|Top-Down]]** | Iterative |

- **📢 섹션 요약 비유**: 구조적은 "무엇을 하는가(프로세스)", IE는 "무엇을 관리하는가([[001_dikw_pyramid|데이터]])", 객체지향은 "누가 하는가(객체)"에 초점.

---

## Ⅲ. 비교 및 연결

| 비교 | 프로세스 중심 | [[383_data_centric_architecture|데이터 중심]] (IE) |
|:---|:---|:---|
| **중복** | 시스템마다 독립 | **전사 통합** |
| **변경** | 프로세스 변경 시 [[001_dikw_pyramid|데이터]]도 | **[[001_dikw_pyramid|데이터]] 안정** |
| **[[194_consistency_database_integrity|일관성]]** | 낮음 | **높음** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### IE 핵심 산출물
1. **ERD**: 엔터티-관계 다이어그램.
2. **CRUD 매트릭스**: 프로세스×엔터티 매핑.
3. **엔터티 정의서**: [[082_attribute_types_er_model|속성]]·[[064_relation_domain|도메인]]·규칙 정의.

---

## Ⅴ. 기대효과 및 결론

IE는 **전사 [[104_da_as_is_analysis|데이터 아키텍처]]의 이론적 기반**이며, 현대의 [[052_data_governance_framework|데이터 거버넌스]]·MDM의 뿌리이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[101_isp_information_strategy_planning_4_steps|ISP]]** | IE 1단계 (전사 [[268_strategy_pattern|전략]]) |
| **ERD** | IE의 핵심 산출물 |
| **CRUD 매트릭스** | 프로세스-엔터티 매핑 |
| **James Martin** | IE 창시자 |
| **[[104_da_as_is_analysis|DA]] ([[104_da_as_is_analysis|데이터 아키텍처]])** | IE의 현대적 진화 |

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
1. IE는 **도시 계획**이에요. 도시(회사) 전체 지도를 먼저 그리고, 건물(시스템)을 짓는 거예요.
2. 지도(전사 [[014_data_model_components|데이터 모델]]) 없이 건물만 짓면 **도로([[001_dikw_pyramid|데이터]])가 안 맞아요**.
3. 큰 그림부터 그리면 **모든 건물이 조화롭게** 연결된답니다!
