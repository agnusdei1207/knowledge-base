+++
title = "193. 데이터 스튜어드 (Data Steward) — 도메인 데이터 책임자"
date = 2026-04-21

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)

- **본질**: [데이터 스튜어드](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/)([Data Steward](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/))는 특정 비즈니스 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질·정의·사용 기준을 일상적으로 관리하는 역할로, 비즈니스와 IT를 연결하는 **현장 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리자**다.
- **가치**: [Data Owner](/knowledge-base/studynote/16_bigdata/10_governance/200_data_owner/)([전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 책임)와 [DBA](/knowledge-base/studynote/05_database/01_db_architecture_relational/025_dba_database_administrator/)(기술적 구현) 사이의 간극을 메워, [데이터 사전](/knowledge-base/studynote/05_database/07_exam_summary/393_data_dictionary/)([Data Dictionary](/knowledge-base/studynote/05_database/04_transactions_concurrency/509_data_dictionary/)) 작성부터 품질 이슈 해결까지 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 지식 기반의 실질적 거버넌스를 수행한다.
- **판단 포인트**: 스튜어드는 "비즈니스 규칙을 가장 잘 아는 사람"이어야 하며, IT 역할이 아닌 업무 역할(business role)임을 명심해야 기술사 답안이 정확해진다.

---

## Ⅰ. 개요 및 필요성

### 1.1 [데이터 스튜어드](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/)의 정의

[Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Steward는 특정 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)(고객, 제품, 재무 등)에 대해 **비즈니스 관점의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리 책임**을 지는 역할이다. "Steward"는 영어로 "청지기, 관리인"을 의미하며, 자산을 소유하지는 않지만 그 자산을 일상적으로 돌보는 역할을 한다.

도서관 사서([Library](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) Cataloger)에 비유할 수 있다: 책을 소유하지는 않지만, 책의 내용을 가장 잘 알고, 목록을 관리하고, 올바른 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 기준을 정하는 사람이다.

### 1.2 필요성

| 문제 상황 | 스튜어드가 해결하는 방식 |
|:---|:---|
| "고객 ID 정의가 시스템마다 다르다" | 비즈니스 공통 정의([data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) definition) 확립 |
| "NULL 값이 너무 많다" | 수집 시점 품질 기준 정의, 입력 규칙 시행 |
| "같은 제품명이 여러 형태로 입력된다" | 표준화 규칙 정의 및 변환 로직 지원 |
| "이 테이블이 무엇을 위한 건지 모른다" | [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)(비즈니스 용어) 문서화 |
| "접근 권한을 누구에게 줄지 모르겠다" | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 맥락에 맞는 접근 가이드라인 제공 |

**📢 섹션 요약 비유**: [데이터 스튜어드](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/)는 **마을 이장**과 같다. 마을([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/))의 규칙을 가장 잘 알고, 주민([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 사용자)과 시청([Data Owner](/knowledge-base/studynote/16_bigdata/10_governance/200_data_owner/)/IT) 사이를 연결하며, 일상적인 문제를 현장에서 해결한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 [데이터 스튜어드 역할](/knowledge-base/studynote/12_it_management/01_governance_strategy/053_data_stewardship_role/) 구조

```
┌─────────────────────────────────────────────────────────────────┐
│                     거버넌스 역할 계층                           │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Data Owner (비즈니스 임원)                                │  │
│  │  · 전략적 책임, 접근 정책 최종 승인, 규제 준수 책임          │  │
│  └───────────────────────────┬───────────────────────────────┘  │
│                              │ 위임                             │
│  ┌───────────────────────────▼───────────────────────────────┐  │
│  │  Data Steward (업무 담당자)   ◀── 핵심 역할                │  │
│  │  · 데이터 정의/사전 관리                                    │  │
│  │  · 품질 기준 수립 및 이슈 해결                              │  │
│  │  · 메타데이터 관리 및 승인                                  │  │
│  │  · 접근 요청 검토 및 Data Owner 추천                        │  │
│  │  · 비즈니스 규칙 문서화                                     │  │
│  └───────────────────────────┬───────────────────────────────┘  │
│                              │ 기술 요청                         │
│  ┌───────────────────────────▼───────────────────────────────┐  │
│  │  Data Custodian (IT/DBA)                                  │  │
│  │  · 저장, 백업, 암호화, 인프라 구현                          │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 스튜어드 유형

| 유형 | 역할 초점 | 주요 활동 |
|:---|:---|:---|
| Business [Data Steward](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/) | 비즈니스 규칙·정의 | [데이터 사전](/knowledge-base/studynote/05_database/07_exam_summary/393_data_dictionary/) 작성, 품질 기준 수립, 접근 가이드 |
| Technical [Data Steward](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/) | 기술 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) | [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 관리, 리니지 추적, [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/) 유지 |
| Operational [Data Steward](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/) | 일상적 품질 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링 | [품질 대시보드](/knowledge-base/studynote/04_software_engineering/06_software_architecture/367_quality_dashboard/) [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링, 이슈 티켓 처리 |

### 2.3 주요 산출물

| 산출물 | 설명 |
|:---|:---|
| [데이터 사전](/knowledge-base/studynote/05_database/07_exam_summary/393_data_dictionary/) ([Data Dictionary](/knowledge-base/studynote/05_database/04_transactions_concurrency/509_data_dictionary/)) | 각 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 항목의 비즈니스 정의, 형식, 허용값, 소유자 |
| 비즈니스 용어집 (Business Glossary) | 조직 공통 비즈니스 용어 정의 |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 규칙 문서 | 완전성·[정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/)·유효성 기준 및 측정 방법 |
| 접근 가이드라인 | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근 요청 시 판단 기준 |

**📢 섹션 요약 비유**: [데이터 스튜어드](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/)의 주요 산출물은 **요리책**과 같다. 어떤 재료([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를, 어떤 기준으로, 어떻게 다루는지 정리해 두어야 누가 주방(시스템)에 들어와도 일관된 요리(분석 결과)가 나온다.

---

## Ⅲ. 비교 및 연결

### 3.1 거버넌스 3대 역할 비교

| 구분 | [Data Owner](/knowledge-base/studynote/16_bigdata/10_governance/200_data_owner/) | [Data Steward](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/) | [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Custodian |
|:---|:---|:---|:---|
| 역할 성격 | [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 책임 | 운영적 관리 | 기술적 구현 |
| 소속 | 비즈니스 임원급 | 업무 부서 담당자 | IT 부서 ([DBA](/knowledge-base/studynote/05_database/01_db_architecture_relational/025_dba_database_administrator/), 인프라) |
| 주요 활동 | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 결정, 접근 승인 | 정의 관리, 품질 이슈 해결 | 저장, [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/), 보안 구현 |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변경 권한 | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 수준 | 비즈니스 규칙 수준 | 기술 구현 수준 |
| RACI | Accountable | Responsible | Responsible (기술) |

### 3.2 이중 역할 과부하 문제

[데이터 스튜어드](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/)의 가장 큰 도전은 **이중 역할 부담**이다:
- 본업(업무 분석가, 마케터, 재무 담당자) + 스튜어드 역할 병행
- 해결책: 전담 스튜어드 임명(대기업), 스튜어드 업무 시간 공식 배정(30% 이상)

**📢 섹션 요약 비유**: 스튜어드 vs 오너 vs 커스토디안은 **부동산 임대 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)**와 같다. 소유자(Owner)가 건물 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 결정하고, 관리인(Steward)이 입주자 민원을 해결하며, 경비원(Custodian)이 열쇠와 잠금장치를 관리한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 스튜어드 일상 업무 흐름

```
[데이터 품질 이슈 발생]
         │
         ▼
스튜어드가 이슈 분류
(비즈니스 규칙 문제 vs 기술 문제)
         │
    ┌────▼────┐
    │규칙 문제 │──▶ 스튜어드가 직접 정의 수정 + 문서화
    └────┬────┘
         │기술 문제
         ▼
Custodian(DBA)에 수정 요청
         │
         ▼
수정 완료 후 스튜어드 검증 승인
         │
         ▼
Data Owner에 주요 변경사항 보고
```

### 4.2 스튜어드 성과 지표

| [KPI](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/) | 측정 방법 |
|:---|:---|
| [데이터 사전](/knowledge-base/studynote/05_database/07_exam_summary/393_data_dictionary/) 커버리지 | 정의된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 항목 수 / 전체 항목 수 |
| 품질 이슈 해결 시간 | 이슈 오픈~종료 평균 일수 |
| [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 완성도 | 비즈니스 정의 채워진 칼럼 비율 |
| 접근 요청 처리 시간 | 요청~승인 평균 시간(목표: 24시간 이내) |

**📢 섹션 요약 비유**: 스튜어드의 일은 **분실물 센터 운영**과 같다. 누군가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 문제(분실물)를 가져오면, 어느 창구(Owner vs Custodian)로 보낼지 판단하고 직접 해결하거나 연결한다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 기대효과

| 기대효과 | 세부 내용 |
|:---|:---|
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 향상 | 비즈니스 규칙을 아는 담당자가 직접 품질 기준 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) |
| [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 지식 보존 | 암묵적 비즈니스 규칙을 문서화하여 조직 자산으로 전환 |
| 의사소통 비용 절감 | IT↔비즈니스 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관련 오해와 재작업 감소 |
| 거버넌스 실효성 | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 현장에서 실질적으로 적용됨 |
| 규제 준수 용이 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 근거·승인 이력을 체계적으로 유지 |

### 5.2 결론

[데이터 스튜어드](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/)는 거버넌스가 종이 위 선언에 머물지 않고 **현장에서 살아 움직이게 만드는 핵심 역할**이다. 기술사는 스튜어드가 비즈니스 역할임을 명확히 이해하고, [Data Owner](/knowledge-base/studynote/16_bigdata/10_governance/200_data_owner/)·Custodian과의 협력 구조, 이중 역할 부담 해소 방안, 성과 지표 설계까지 포괄적으로 제시할 수 있어야 한다.

**📢 섹션 요약 비유**: [데이터 스튜어드](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/)가 있는 조직의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 **잘 관리된 도서관** 같다. 사서(스튜어드)가 있어야 책([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))이 제자리에 있고, 찾기 쉽고, 낡은 책은 정리된다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| [Data Owner](/knowledge-base/studynote/16_bigdata/10_governance/200_data_owner/) | 상위 역할 | [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 책임자, 스튜어드에게 운영 위임 |
| [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Custodian | 협력 역할 | 기술 구현 담당, 스튜어드 요청 수행 |
| [Data Dictionary](/knowledge-base/studynote/05_database/04_transactions_concurrency/509_data_dictionary/) | 핵심 산출물 | 스튜어드가 관리하는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 항목 정의서 |
| Business Glossary | 핵심 산출물 | 조직 공통 비즈니스 용어 정의집 |
| [Data Quality](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/270_data_quality_great_expectations/) | 관리 대상 | 스튜어드의 핵심 관리 목표 |
| [Data Catalog](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) | 작업 도구 | 스튜어드가 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)를 등록·관리하는 플랫폼 |
| RACI Matrix | 책임 구조 | 스튜어드=Responsible, Owner=Accountable |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 거버넌스 필요]
    │
    ▼
[데이터 소유자 지정]
    │
    ▼
[데이터 스튜어드(Data Steward) 역할]
    │
    ▼
[데이터 카탈로그 관리]
    │
    ▼
[MDM(마스터 데이터 관리)]
```

[데이터 스튜어드](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/)는 거버넌스와 [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/), MDM을 연결하는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 책임자 역할이다.

### 👶 어린이를 위한 3줄 비유 설명

1. 학교 도서관에서 사서 선생님이 책마다 어떤 책인지, 어디에 두는지, 누가 빌릴 수 있는지 관리하는 것처럼, [데이터 스튜어드](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/)는 회사의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 그렇게 돌봐.
2. [데이터 스튜어드](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/)는 "이 숫자는 무엇을 뜻하는지" 가장 잘 아는 사람이라서, 컴퓨터 전문가(IT)와 회사 대표([Data Owner](/knowledge-base/studynote/16_bigdata/10_governance/200_data_owner/)) 사이에서 통역사 역할도 해.
3. 이 역할이 없으면 같은 "고객 수"라도 부서마다 다른 숫자를 쓰는 일이 생겨서 회의에서 싸우게 돼.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 199 / 262

← **이전**: [192. 데이터 거버넌스 구성 요소 (Data Governance Components) — 정책/표준/역할/프로세스/도구](/knowledge-base/studynote/16_bigdata/10_governance/198_data_governance_components/)
**다음**: [194. 데이터 소유자 (Data Owner) — 비즈니스 책임자와 접근 승인](/knowledge-base/studynote/16_bigdata/10_governance/200_data_owner/) →

---
