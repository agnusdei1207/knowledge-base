+++
title = "192. 데이터 거버넌스 구성 요소 (Data Governance Components) — 정책/표준/역할/프로세스/도구"
date = 2026-04-21

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)

- **본질**: [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/)는 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)([Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/))·표준(Standard)·역할(Role)·프로세스([Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/))·도구(Tool)의 5대 기둥으로 구성되며, 이 다섯 요소가 균형을 이룰 때 실효성 있는 거버넌스가 완성된다.
- **가치**: 각 구성 요소가 RACI (Responsible, Accountable, Consulted, Informed) 매트릭스로 연결되어 책임이 명확해지고, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관련 분쟁·품질 문제를 체계적으로 해소할 수 있다.
- **판단 포인트**: 운영 모델(중앙집중·연방·하이브리드)과 성숙도 단계(CMM 1~5)에 따라 5대 구성 요소의 비중과 적용 방식을 달리해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 왜 5대 구성 요소인가?

[데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/)를 "[정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)만 만들면 끝"이라고 오해하는 조직이 많다. 그러나 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)(What)이 있어도 이를 실행할 역할(Who), 절차(How), 도구(With What)가 없으면 선언에 그친다. [DAMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/117_dama/) DMBOK이 제시하는 5대 구성 요소는 이 간극을 메운다:

```
정책 ──▶ 무엇을 해야 하는가?
표준 ──▶ 어떤 형식/기준으로?
역할 ──▶ 누가 책임지는가?
프로세스 ─▶ 어떤 절차로?
도구 ──▶ 어떤 시스템으로?
```

### 1.2 구성 요소 개요

| 구성 요소 | 정의 | 예시 |
|:---|:---|:---|
| [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)([Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관련 의사결정 원칙·허용/금지 기준 | [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) 접근은 업무 필요 원칙 적용 |
| 표준(Standard) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 형식·명명·[분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)의 일관된 기준 | 날짜 형식 YYYY-MM-[DD](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/769_architecture/), 테이블명 snake_case |
| 역할(Role) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관련 책임·권한을 가진 역할 정의 | [Data Owner](/knowledge-base/studynote/16_bigdata/10_governance/200_data_owner/), [Data Steward](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/), [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Custodian |
| 프로세스([Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/)) | 거버넌스 의사결정·문제해결·변경 절차 | 접근 신청 승인, 품질 이슈 해결 워크플로 |
| 도구(Tool) | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)·표준·프로세스를 실행·자동화하는 시스템 | [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/), 품질 검사 툴, [MDM](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) 시스템 |

**📢 섹션 요약 비유**: 5대 구성 요소는 <strong>레스토랑 운영 시스템</strong>과 같다. 메뉴판([정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)), 레시피(표준), 셰프·웨이터 역할(역할), 주문 처리 절차(프로세스), 주방 기기(도구)가 모두 갖춰져야 맛있는 요리([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))가 나온다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 5대 구성 요소 상세

```
┌──────────────────────────────────────────────────────────────────┐
│                  데이터 거버넌스 5대 구성 요소                     │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  1. 정책 (Policy)                                         │    │
│  │   · 접근 정책 (Access Policy): 최소 권한 원칙              │    │
│  │   · 보유/삭제 정책 (Retention Policy): 법적 보관 기간       │    │
│  │   · 품질 정책 (Quality Policy): 허용 오류율 ≤ 0.1%         │    │
│  │   · 보안 분류 정책: Public/Internal/Confidential/Secret    │    │
│  └──────────────────────────────────────────────────────────┘    │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  2. 표준 (Standard)                                       │    │
│  │   · 명명 규칙 (Naming Convention): DB, 테이블, 칼럼 명명    │    │
│  │   · 데이터 형식 (Format Standard): 날짜, 전화번호, 주소     │    │
│  │   · 마스터 데이터 표준: 코드 목록, 분류 체계                │    │
│  └──────────────────────────────────────────────────────────┘    │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  3. 역할 (Role) — RACI Matrix                             │    │
│  │   · Data Owner: 전략적 책임, 접근 최종 승인                │    │
│  │   · Data Steward: 일상적 품질·정의 관리                    │    │
│  │   · Data Custodian: IT 인프라·보안 구현                    │    │
│  │   · Data Consumer: 데이터 사용자, 품질 피드백 제공          │    │
│  └──────────────────────────────────────────────────────────┘    │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  4. 프로세스 (Process)                                    │    │
│  │   · 접근 신청·승인 워크플로                                │    │
│  │   · 데이터 품질 이슈 해결 절차                             │    │
│  │   · 변경 관리 (Change Management): 스키마 변경 승인         │    │
│  │   · 데이터 인증 (Data Certification): 공식 데이터셋 지정    │    │
│  └──────────────────────────────────────────────────────────┘    │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  5. 도구 (Tool)                                           │    │
│  │   · 데이터 카탈로그: DataHub, Collibra, Apache Atlas       │    │
│  │   · 데이터 품질: Great Expectations, Deequ, Soda Core      │    │
│  │   · 데이터 리니지: OpenLineage, Marquez                    │    │
│  │   · MDM: Informatica MDM, IBM InfoSphere                  │    │
│  └──────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────┘
```

### 2.2 성숙도 모델 (CMM 기반)

| 단계 | 수준명 | 특징 | 5대 요소 적용 상태 |
|:---:|:---|:---|:---|
| 1 | Initial | 임시방편, 개인 역량 의존 | 거의 없음 |
| 2 | Managed | 프로젝트 단위 존재 | 일부 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)·역할 정의 |
| 3 | Defined | 조직 전체 표준화 | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)·표준·역할 공식화 |
| 4 | Measured | [KPI](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/) 측정·[모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링 | 모든 요소 + 자동 측정 |
| 5 | Optimizing | 지속적 개선, [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 자동화 | 전 요소 통합·최적화 |

**📢 섹션 요약 비유**: 거버넌스 성숙도는 **운전 실력** 같다. 처음에는 눈으로만 보고 운전하다가(레벨 1), 결국 자동 주행(레벨 5)으로 진화하는 것이다.

---

## Ⅲ. 비교 및 연결

### 3.1 운영 모델 비교

| 모델 | 특징 | 장점 | 단점 |
|:---|:---|:---|:---|
| 중앙집중형 | [CDO](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/068_cdo_cio_role_separation_governance/) 산하 단일 팀이 전체 거버넌스 수행 | [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 높음, 규제 대응 용이 | 속도 느림, [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 지식 부족 |
| 연방형 | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)별 자체 거버넌스 + 공통 최소 표준 | 속도·민첩성 우수 | [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 유지 어려움 |
| 하이브리드 | 핵심 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)은 중앙, 세부는 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 자율 | 균형 | 조율 비용 발생 |

### 3.2 타 프레임워크와의 연계

| 프레임워크 | 연계 내용 |
|:---|:---|
| [Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/) | 연방형 거버넌스 모델을 아키텍처 원칙으로 채택 |
| [DataOps](/knowledge-base/studynote/12_it_management/05_security_compliance/324_dataops/) | 거버넌스 프로세스(품질 검사, 접근 제어)를 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인에 자동화 |
| [Zero Trust](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) | 거버넌스 접근 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 [Zero Trust](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) 보안 모델과 연계 |
| ISO 8000 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 표준 — 거버넌스 품질 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)의 기준 |

**📢 섹션 요약 비유**: 거버넌스 운영 모델은 <strong>학교 교칙 운영 방식</strong>이다. 전교 공통 규칙(중앙집중)만 있으면 경직되고, 반마다 다른 규칙(연방형)만 있으면 혼란스럽다. 두 가지를 조화시키는 것이 하이브리드다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 RACI 매트릭스 예시

| 거버넌스 활동 | [Data Owner](/knowledge-base/studynote/16_bigdata/10_governance/200_data_owner/) | [Data Steward](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/) | [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Custodian | [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Consumer |
|:---|:---:|:---:|:---:|:---:|
| [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 수립 | A | R | C | I |
| 접근 신청 승인 | A | C | R | I |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 정의 | C | R | I | I |
| [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 변경 승인 | A | C | R | I |
| 품질 이슈 해결 | I | A,R | C | I |

*A=Accountable(책임자), R=Responsible(실행자), C=Consulted(자문), I=Informed(통보)*

### 4.2 구성 요소별 도입 순서

```
Step 1: 역할 정의 ─▶ 누가 책임지는지 먼저 확정
Step 2: 정책 수립 ─▶ 핵심 4대 정책(접근/보유/품질/보안) 우선
Step 3: 표준화 ──▶ 명명 규칙·코드 목록부터 시작
Step 4: 프로세스 ─▶ 접근 신청·이슈 해결 워크플로 자동화
Step 5: 도구 도입 ─▶ 데이터 카탈로그, 품질 도구 도입
```

**📢 섹션 요약 비유**: 구성 요소 도입은 **집 짓기** 순서와 같다. 설계도(역할·[정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)) 없이 벽돌(도구)부터 사는 실수를 범하지 말아야 한다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 기대효과

| 요소 | 기대효과 |
|:---|:---|
| [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) | 규제 준수 비용 절감, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 남용 예방 |
| 표준 | 시스템 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 확보, 통합 비용 절감 |
| 역할 | 책임 명확화로 분쟁 감소, 의사결정 속도 향상 |
| 프로세스 | 품질 이슈 해결 시간 단축, [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 준비 자동화 |
| 도구 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 검색 시간 단축, 품질 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링 자동화 |

### 5.2 결론

[데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/)의 5대 구성 요소는 단독으로 존재할 수 없고 <strong>유기적으로 연결</strong>되어야 한다. 조직의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 성숙도를 진단하고(현재 레벨 파악), 부족한 요소부터 우선순위를 정해 점진적으로 고도화하는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 현실적이다. 기술사는 각 구성 요소의 설계 방법과 도구 선택 기준을 명확히 제시할 수 있어야 한다.

**📢 섹션 요약 비유**: 5대 구성 요소는 <strong>오케스트라의 파트</strong>다. 바이올린([정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/))만 잘 해도 전체 연주는 엉망이 된다. 지휘자([CDO](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/068_cdo_cio_role_separation_governance/))가 모든 파트를 조화시켜야 아름다운 음악(신뢰할 수 있는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))이 나온다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| [Data Owner](/knowledge-base/studynote/16_bigdata/10_governance/200_data_owner/) | 역할 요소 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)의 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 책임자 |
| [Data Steward](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/) | 역할 요소 | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 일상적 관리자 |
| [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Custodian | 역할 요소 | IT 인프라 담당, 기술적 구현 책임 |
| RACI Matrix | 프로세스 도구 | 역할별 책임 명확화 매트릭스 |
| [Data Catalog](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) | 도구 요소 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자산 목록·[메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)·리니지 관리 |
| CMM | 성숙도 모델 | Capability [Maturity Model](/knowledge-base/studynote/12_it_management/01_governance_strategy/011_maturity_model/) — 거버넌스 수준 측정 |
| [Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/) | 연계 아키텍처 | 연방형 거버넌스 모델을 전제로 함 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 소유권 (Data Ownership) — Owner/Steward/Custodian]
    │
    ▼
[데이터 정책 (Data Policy) / 표준 (Data Standard)]
    │
    ▼
[데이터 카탈로그 (Data Catalog) — 메타데이터 목록]
    │
    ▼
[데이터 거버넌스 (Data Governance) — 5대 구성 요소]
    │
    ▼
[데이터 메시 (Data Mesh) — 연방형 거버넌스]
```

[데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/)가 역할 정의에서 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)·표준·[카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/)를 거쳐 조직 전체의 연방형 자율 관리로 발전한 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명

1. 학교에서 선생님([Data Owner](/knowledge-base/studynote/16_bigdata/10_governance/200_data_owner/)), 반장([Data Steward](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/)), 청소 당번([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Custodian)이 각자 역할을 정해두면 교실이 깨끗하게 유지되는 것처럼, 회사에서도 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 관리하는 역할을 나눠 정해.
2. 규칙([정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/))은 "교실에서는 뛰지 말자"처럼 기본 원칙이고, 표준은 "책을 책꽂이 순서대로 꽂는 방법"처럼 일관된 방식이야.
3. 이 다섯 가지([정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)·표준·역할·절차·도구)가 모두 갖춰지면 "어디에 무슨 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 있고, 누가 책임지는지" 한눈에 알 수 있어.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 198 / 262

← **이전**: [191. 데이터 거버넌스 정의 (Data Governance Definition) — 데이터 소유·관리·사용 원칙 체계](/knowledge-base/studynote/16_bigdata/10_governance/197_data_governance_definition/)
**다음**: [193. 데이터 스튜어드 (Data Steward) — 도메인 데이터 책임자](/knowledge-base/studynote/16_bigdata/10_governance/199_data_steward/) →

---
