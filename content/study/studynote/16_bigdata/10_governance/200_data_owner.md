+++
weight = 200
title = "194. 데이터 소유자 (Data Owner) — 비즈니스 책임자와 접근 승인"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)

- **본질**: [[001_dikw_pyramid|데이터]] 소유자([[001_dikw_pyramid|Data]] Owner)는 특정 [[001_dikw_pyramid|데이터]] [[064_relation_domain|도메인]]에 대해 [[268_strategy_pattern|전략]]적·법적 책임을 지는 시니어 비즈니스 임원으로, [[001_dikw_pyramid|데이터]] 접근 [[164_policy|정책]] 결정과 규제 준수에 대한 최종 책임을 진다.
- **가치**: [[052_data_governance_framework|데이터 거버넌스]] 체계에서 Owner가 명확해야 접근 승인·규제 대응·품질 기준 결정이 일원화되고, 분쟁 발생 시 책임 소재가 명확해진다.
- **판단 포인트**: [[001_dikw_pyramid|Data]] Owner는 기술적 역할이 아니라 **비즈니스 책임 역할**이며, GDPR의 [[001_dikw_pyramid|데이터]] 컨트롤러([[001_dikw_pyramid|Data]] Controller) 개념과 유사하다는 점이 기술사 답안의 핵심 포인트다.

---

## Ⅰ. 개요 및 필요성

### 1.1 [[001_dikw_pyramid|Data]] Owner 정의

[[001_dikw_pyramid|Data]] Owner([[001_dikw_pyramid|데이터]] 소유자)는 특정 [[001_dikw_pyramid|데이터]] [[064_relation_domain|도메인]](예: 고객 [[001_dikw_pyramid|데이터]], 재무 [[001_dikw_pyramid|데이터]], 인사 [[001_dikw_pyramid|데이터]])에 대해:
- **누가 접근할 수 있는지** 결정하는 접근 [[164_policy|정책]] 권한
- **[[001_dikw_pyramid|데이터]]가 규제를 준수하는지** 보장하는 컴플라이언스 책임
- **[[001_dikw_pyramid|데이터]]를 얼마나 보관하고 언제 삭제하는지** 결정하는 생명주기 책임

을 갖는 **시니어 비즈니스 임원급** 역할이다.

### 1.2 필요성 — 소유자가 없으면 생기는 문제

| 문제 | 원인 |
|:---|:---|
| 접근 요청 승인 [[015_지연_데이터_관점|지연]] | 누가 승인 권한자인지 불명확 |
| 규제 대응 실패 | [[791_gdpr_eu|GDPR]] 위반 시 책임 소재 불분명 |
| 과도한 접근 권한 | [[010_least_privilege|최소 권한 원칙]] 집행자 부재 |
| [[001_dikw_pyramid|데이터]] 삭제 불이행 | 보유 기간 [[095_determinant_dependent|결정자]] 부재 → 불필요 [[001_dikw_pyramid|데이터]] 무한 축적 |
| [[001_dikw_pyramid|데이터]] 품질 방치 | 품질 기준 결정 권한자 없음 |

**📢 섹션 요약 비유**: [[001_dikw_pyramid|Data]] Owner가 없는 [[001_dikw_pyramid|데이터]]는 **무주공산(無主空山)**과 같다. 아무도 책임지지 않으면 누구나 사용하다가 결국 아무도 관리하지 않게 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 [[001_dikw_pyramid|Data]] Owner 위치와 책임 구조

```
┌───────────────────────────────────────────────────────────────┐
│                    데이터 거버넌스 책임 계층                     │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  CDO (Chief Data Officer)                               │  │
│  │  전사 데이터 전략 및 거버넌스 총괄                         │  │
│  └───────────────────────────────────┬─────────────────────┘  │
│                                      │ 도메인별 위임             │
│  ┌──────────────┬──────────────┬─────▼─────────────────────┐  │
│  │ Customer DO  │ Finance DO   │    Product DO              │  │
│  │ (CMO급)      │ (CFO급)      │    (CPO급)                 │  │
│  │              │              │                            │  │
│  │ 고객 도메인   │ 재무 도메인   │ 제품 도메인                │  │
│  │ 접근정책 결정 │ 접근정책 결정 │ 접근정책 결정              │  │
│  └──────┬───────┴──────┬───────┴────────────┬──────────────┘  │
│         │              │                    │                 │
│         ▼              ▼                    ▼                 │
│     Data Steward   Data Steward         Data Steward         │
│     (운영 위임)     (운영 위임)           (운영 위임)           │
└───────────────────────────────────────────────────────────────┘
```

### 2.2 [[001_dikw_pyramid|Data]] Owner의 핵심 책임 6가지

| 책임 영역 | 세부 내용 |
|:---|:---|
| 접근 [[164_policy|정책]] 결정 | [[010_least_privilege|최소 권한 원칙]]에 따른 역할별 접근 수준 정의 |
| 접근 요청 최종 승인 | [[067_data_steward_data_quality|Data Steward]] 검토 후 최종 승인/거부 |
| 규제 준수 보장 | [[791_gdpr_eu|GDPR]]·PIPA에서 [[001_dikw_pyramid|Data]] Controller 역할 수행 |
| [[001_dikw_pyramid|데이터]] 품질 기준 [[009_config|설정]] | 허용 품질 수준([[085_sla|SLA]]) 결정 |
| 보유/삭제 [[164_policy|정책]] 결정 | 법적 보관 기간 + 비즈니스 필요 기간 결정 |
| [[808_data_classification|데이터 분류]] 결정 | Public/Internal/Confidential/[[514_secret_management_vault_kms|Secret]] [[104_classification_analysis|분류]] |

### 2.3 [[791_gdpr_eu|GDPR]] 연계 — [[001_dikw_pyramid|Data]] Controller 개념

| 개념 | [[791_gdpr_eu|GDPR]] 용어 | [[052_data_governance_framework|데이터 거버넌스]] 용어 |
|:---|:---|:---|
| [[001_dikw_pyramid|데이터]] 처리 목적·방법 [[095_determinant_dependent|결정자]] | [[001_dikw_pyramid|Data]] Controller ([[621_art_android_runtime|Art]].4(7)) | [[001_dikw_pyramid|Data]] Owner |
| [[001_dikw_pyramid|데이터]] 처리 실행자 | [[001_dikw_pyramid|Data]] Processor ([[621_art_android_runtime|Art]].4(8)) | [[001_dikw_pyramid|Data]] Custodian / IT |
| [[001_dikw_pyramid|데이터]] 주체 | [[001_dikw_pyramid|Data]] Subject | [[001_dikw_pyramid|Data]] Consumer (고객 기준) |

**📢 섹션 요약 비유**: [[001_dikw_pyramid|Data]] Owner는 **아파트 입주자 대표**와 같다. 공용 공간([[001_dikw_pyramid|데이터]]) 사용 규칙을 정하고, 외부인(외부 접근자) 출입을 승인하며, 관리비(보유 비용) 결정도 책임진다.

---

## Ⅲ. 비교 및 연결

### 3.1 3대 역할 완전 비교

| 구분 | [[001_dikw_pyramid|Data]] Owner | [[067_data_steward_data_quality|Data Steward]] | [[001_dikw_pyramid|Data]] Custodian |
|:---|:---|:---|:---|
| 직급 | C-level, VP, 부서장 | 시니어 업무 담당자 | [[025_dba_database_administrator|DBA]], 인프라 엔지니어 |
| 역할 성격 | [[268_strategy_pattern|전략]]적·법적 책임 | 운영적·[[064_relation_domain|도메인]] 관리 | 기술적·인프라 구현 |
| 시간 할애 | 비정기(결정 필요 시) | 정기(주 30~50%) | 상시(기술 운영) |
| [[001_dikw_pyramid|데이터]] 지식 | 비즈니스 가치·위험 | 비즈니스 규칙·정의 | 기술 구조·저장 방식 |
| RACI 위치 | Accountable | Responsible | Responsible (기술) |
| [[791_gdpr_eu|GDPR]] 대응 | [[001_dikw_pyramid|Data]] Controller | - | [[001_dikw_pyramid|Data]] Processor |

### 3.2 [[064_relation_domain|도메인]] 매핑 예시

| [[001_dikw_pyramid|데이터]] [[064_relation_domain|도메인]] | [[001_dikw_pyramid|Data]] Owner 직책 | 예시 |
|:---|:---|:---|
| 고객([[026_three_c_analysis|Customer]]) | CMO (Chief Marketing Officer) | 고객 [[781_personal_information|개인정보]], [[107_crm_customer_relationship_management|CRM]] [[001_dikw_pyramid|데이터]] |
| 재무(Finance) | CFO (Chief Financial Officer) | 매출, 비용, 예산 [[001_dikw_pyramid|데이터]] |
| 인사(HR) | CHRO (Chief Human Resources Officer) | 직원 정보, 급여 [[001_dikw_pyramid|데이터]] |
| 제품(Product) | CPO (Chief Product Officer) | 제품 [[394_catalog_metadata|카탈로그]], 재고 [[001_dikw_pyramid|데이터]] |
| 운영(Operations) | COO (Chief Operating Officer) | 주문, 물류, 공정 [[001_dikw_pyramid|데이터]] |

**📢 섹션 요약 비유**: [[001_dikw_pyramid|데이터]] [[064_relation_domain|도메인]]별 Owner 매핑은 **부서별 예산 책임자** 지정과 같다. CFO가 재무 예산을 책임지듯, 각 [[001_dikw_pyramid|데이터]] [[064_relation_domain|도메인]]의 Owner가 그 [[064_relation_domain|도메인]] [[001_dikw_pyramid|데이터]]의 "예산(가치와 위험)"을 책임진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 접근 요청 승인 프로세스

```
[접근 요청자가 시스템에 요청]
         │
         ▼
[Data Steward: 비즈니스 필요성·위험 검토]
         │
    ┌────▼────┐
    │ 저위험  │──▶ Steward가 직접 승인 (위임 권한 내)
    └────┬────┘
         │고위험 / 대량 데이터
         ▼
[Data Owner: 최종 승인/거부]
         │
         ▼
[Data Custodian: 기술적 권한 부여]
         │
         ▼
[감사 로그에 이력 기록]
```

### 4.2 [[001_dikw_pyramid|Data]] Owner 지정 실패 패턴

- **공동 소유 함정**: "모든 임원이 [[001_dikw_pyramid|데이터]] Owner"라고 선언 → 실질적 책임자 없음
- **IT 위임 함정**: IT 팀장을 Owner로 지정 → 비즈니스 맥락 없는 기술적 결정
- **겸직 과부하**: 한 임원이 10개 이상 [[064_relation_domain|도메인]] Owner → 형식적 역할만 유지

### 4.3 기술사 답안 핵심 포인트

- [[001_dikw_pyramid|Data]] Owner ≠ [[001_dikw_pyramid|데이터]]를 물리적으로 소유한다는 의미 (법적 소유권 개념 아님)
- [[791_gdpr_eu|GDPR]] Article 24: Controller는 [[001_dikw_pyramid|Data]] Subject 권리 [[571_protection_vs_security|보호]]를 위한 적절한 기술·조직적 조치를 취해야 함 → [[001_dikw_pyramid|Data]] Owner 역할의 법적 근거
- 조직이 클수록 [[064_relation_domain|도메인]] Owner를 세분화하고, 작은 조직은 CDO가 Owner 기능 겸직 가능

**📢 섹션 요약 비유**: [[001_dikw_pyramid|Data]] Owner 지정 실패는 **선장 없는 배**와 같다. 선원(Steward, Custodian)이 아무리 잘 해도, 배의 방향([[164_policy|정책]])을 결정하는 선장이 없으면 항구에 도착하지 못한다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 기대효과

| 기대효과 | 세부 내용 |
|:---|:---|
| 명확한 책임 소재 | [[001_dikw_pyramid|데이터]] 관련 사고 발생 시 책임자 명확 |
| 신속한 의사결정 | 접근 요청 처리 시간 단축 (임원 권한 위임 구조) |
| 규제 준수 | [[791_gdpr_eu|GDPR]] Controller 역할 공식화로 [[606_auditing_linux_auditd|감사]] 대응 용이 |
| 품질 기준 현실화 | 비즈니스 맥락을 이해한 Owner가 실용적 기준 [[009_config|설정]] |
| [[001_dikw_pyramid|데이터]] 가치 인식 | 임원이 직접 관여함으로써 [[001_dikw_pyramid|데이터]]를 [[268_strategy_pattern|전략]] 자산으로 인식 |

### 5.2 결론

[[001_dikw_pyramid|Data]] Owner는 [[052_data_governance_framework|데이터 거버넌스]]의 **정치적(organizational) 중심축**이다. 아무리 좋은 기술 도구와 프로세스가 있어도, 비즈니스 임원이 [[001_dikw_pyramid|데이터]] 책임을 받아들이지 않으면 거버넌스는 형식화된다. 기술사는 조직 설계(organizational design) 관점에서 [[001_dikw_pyramid|Data]] Owner 역할을 제도화하는 방법을 제시해야 한다.

**📢 섹션 요약 비유**: [[001_dikw_pyramid|Data]] Owner는 **국가의 장관**이다. 각 부처([[064_relation_domain|도메인]]) 장관이 그 부처 [[001_dikw_pyramid|데이터]](예산·[[164_policy|정책]])를 책임지고, 국무총리([[068_cdo_cio_role_separation_governance|CDO]])가 전체를 조율하며, 대통령(이사회)이 [[268_strategy_pattern|전략]] 방향을 제시한다.

---

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---|:---|:---|
| [[068_cdo_cio_role_separation_governance|CDO]] | 상위 역할 | 전사 [[001_dikw_pyramid|데이터]] [[268_strategy_pattern|전략]]·거버넌스 총괄 |
| [[067_data_steward_data_quality|Data Steward]] | 위임 역할 | Owner가 운영 책임 위임, 일상 관리 수행 |
| [[001_dikw_pyramid|Data]] Custodian | 기술 실행 | Owner [[164_policy|정책]]을 기술적으로 구현 |
| [[791_gdpr_eu|GDPR]] [[001_dikw_pyramid|Data]] Controller | 규제 연계 | [[001_dikw_pyramid|Data]] Owner의 법적 대응 개념 |
| RACI Accountable | 책임 구조 | Owner는 RACI의 Accountable 역할 |
| [[808_data_classification|Data Classification]] | 핵심 결정 | Owner가 [[001_dikw_pyramid|데이터]] 민감도 [[104_classification_analysis|분류]] 결정 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 생성 (Data Creation) — 비즈니스 프로세스에서 데이터 발생]
    │
    ▼
[데이터 오너 (Data Owner) — 데이터 자산의 최종 책임자 지정]
    │
    ▼
[데이터 스튜어드 (Data Steward) — 일상적 품질·분류 관리 담당자]
    │
    ▼
[데이터 거버넌스 위원회 (DGC) — 정책 수립·충돌 조정 조직]
    │
    ▼
[데이터 메시 도메인 오너십 — 도메인팀이 데이터 제품 소유·배포]
    │
    ▼
[GDPR / 개인정보 책임 — 법적 데이터 오너십과 컴플라이언스 통합]
```
[[001_dikw_pyramid|데이터]] 오너는 [[052_data_governance_framework|데이터 거버넌스]]의 핵심 책임 주체로, 스튜어드와의 역할 분담을 통해 [[001_dikw_pyramid|데이터]] 품질·보안·컴플라이언스를 조직적으로 보장한다.

### 👶 어린이를 위한 3줄 비유 설명

1. 학교 도서관의 책을 "누가 빌릴 수 있고, 어떤 책은 선생님만 볼 수 있는지" 결정하는 사람이 교장 선생님인 것처럼, [[001_dikw_pyramid|Data]] Owner는 회사 [[001_dikw_pyramid|데이터]]의 교장 선생님이야.
2. [[001_dikw_pyramid|Data]] Owner는 컴퓨터를 직접 다루지 않아도 돼 — "이 [[001_dikw_pyramid|데이터]]는 마케팅 팀만 볼 수 있어"처럼 규칙을 결정하는 게 역할이거든.
3. [[001_dikw_pyramid|데이터]]가 잘못 사용되거나 [[781_personal_information|개인정보]]가 유출되면, [[001_dikw_pyramid|Data]] Owner가 최종 책임을 지기 때문에 가장 신중하게 역할을 수행해야 해.
