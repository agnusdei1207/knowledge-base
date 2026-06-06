---
title: "030. Data Integrity Security"
date: "2026-04-29"
tags:
  - "studynote-database"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성](/studynote/09_security/01_intro_principles/003_integrity/)([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Integrity](/studynote/09_security/01_intro_principles/003_integrity/))은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 정확하고 일관되게 유지되는 성질이며, [데이터베이스 보안](/studynote/09_security/16_data_privacy/830_db_security/)([DB Security](/studynote/09_security/16_data_privacy/830_db_security/))은 허가된 사용자만 접근할 수 있도록 하는 통제 체계다. [무결성](/studynote/09_security/01_intro_principles/003_integrity/)은 "올바른 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)", 보안은 "올바른 사람"을 보장한다.
> 2. **가치**: [무결성](/studynote/09_security/01_intro_principles/003_integrity/) 제약은 DBMS가 자동으로 시행하며 잘못된 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 입력을 차단한다. 보안은 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)([Authentication](/studynote/02_operating_system/10_security/604_authentication_factors/))·권한 부여([Authorization](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/))·[감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)([Audit](/studynote/12_it_management/05_security_compliance/363_audit/))의 3A 체계로 구현된다.
> 3. **판단 포인트**: [무결성](/studynote/09_security/01_intro_principles/003_integrity/) 제약이 지나치게 엄격하면 정상 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 입력이 차단될 수 있고, 보안이 지나치게 강화되면 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 [사용성](/studynote/04_software_engineering/05_devops_ci_cd/286_usability_tactics/)이 저하된다. [무결성](/studynote/09_security/01_intro_principles/003_integrity/)·보안·[가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)의 균형이 DB 설계의 핵심이다.

---

## Ⅰ. 개요 및 필요성

```text
데이터 무결성 유형:
  +-----------------------------------------+
  |  개체 무결성:  기본키 ≠ NULL, 고유      |
  |  참조 무결성:  외래키 -> 부모 행 존재    |
  |  도메인 무결성: 열 값이 허용 범위 내    |
  |  사용자 정의:  비즈니스 규칙 제약       |
  +-----------------------------------------+

DB 보안 3A:
  인증(Authentication) -> 권한 부여(Authorization) -> 감사(Audit)
  "누구냐?"              "무엇을 할 수 있냐?"         "무엇을 했냐?"
```

- **📢 섹션 요약 비유**: DB [무결성](/studynote/09_security/01_intro_principles/003_integrity/)과 보안은 은행 금고의 두 안전장치다. [무결성](/studynote/09_security/01_intro_principles/003_integrity/)(금고 안 돈의 [정확성](/studynote/16_bigdata/01_intro/002_bigdata_5v/))은 잘못된 금액 입력을 막고, 보안(금고 [접근 통제](/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/))은 허가된 직원만 금고에 접근할 수 있게 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [참조 무결성](/studynote/05_database/02_modeling_normalization/075_referential_integrity_foreign_key_cascade/) 위반 처리

| 옵션 | 동작 |
|:---|:---|
| **RESTRICT** | 부모 삭제/수정 차단 |
| **CASCADE** | 자식 자동 삭제/수정 |
| **SET NULL** | 자식 외래키를 NULL로 |
| **SET DEFAULT** | 자식 외래키를 기본값으로 |
| **NO ACTION** | 기본값 ([트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 완료 후 검사) |

### DB [접근 통제](/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/) 모델

```text
DAC (Discretionary Access Control — 임의 접근 제어):
  - 데이터 소유자가 접근 권한 결정
  - GRANT/REVOKE 명령
  - 유연하지만 권한 남용 가능

MAC (Mandatory Access Control — 강제 접근 제어):
  - 시스템이 보안 레벨 기준으로 결정
  - Top Secret > Secret > Confidential > Unclassified
  - 군사·정부 시스템에서 사용

RBAC (Role-Based Access Control — 역할 기반):
  - 역할(Role)에 권한 부여 후 사용자에게 역할 할당
  - 현대 DBMS 표준 방식
  - 권한 관리 단순화
```

- **📢 섹션 요약 비유**: DAC·[MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)·RBAC는 아파트 출입 통제 방식이다. DAC(각 세대 주인이 열쇠 복사 결정), [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)(건물 보안등급별 자동 통제), [RBAC](/studynote/09_security/11_iam_access_control/569_rbac/)(입주민·직원·방문객 역할별 카드키 발급)에 해당한다.

---

## Ⅲ. 비교 및 연결

| 비교 | [무결성](/studynote/09_security/01_intro_principles/003_integrity/) | 보안 |
|:---|:---|:---|
| 목표 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [정확성](/studynote/16_bigdata/01_intro/002_bigdata_5v/)·[일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 허가된 [접근 통제](/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/) |
| 구현 | 제약 조건, [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/) | [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), 권한, 암호화 |
| 위협 | 잘못된 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 입력 | 불법 접근·[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유출 |
| 법규 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 표준·품질 | [개인정보보호법](/studynote/09_security/16_data_privacy/783_pipa_korea/)·[GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/) |

- **📢 섹션 요약 비유**: [무결성](/studynote/09_security/01_intro_principles/003_integrity/)과 보안은 식품 안전의 두 축이다. [무결성](/studynote/09_security/01_intro_principles/003_integrity/)(유통기한 관리, 성분 표시 정확)은 식품 자체의 품질이고, 보안(냉장 보관, 위생 [접근 통제](/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/))은 식품을 다루는 환경의 안전이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 현대 DB 보안 레이어

```text
애플리케이션 레이어:
  - 입력값 검증, SQL 인젝션 방지
  - 준비된 문(Prepared Statement)

DB 서버 레이어:
  - 사용자 인증 (OS 인증, DB 인증, LDAP)
  - 열(Column) 수준 암호화
  - 뷰(View)를 통한 행(Row) 수준 보안

네트워크 레이어:
  - TLS/SSL 암호화 전송
  - IP 화이트리스트

감사(Audit):
  - DDL/DML 작업 로그
  - 특권 계정 접근 로그
  - SIEM 연동
```

- **📢 섹션 요약 비유**: DB 보안 레이어는 양파 껍질이다. 외부(네트워크 암호화)에서 내부(열 수준 암호화)까지 여러 겹의 보안이 공격자가 중심([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))에 도달하지 못하게 막는다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 품질</strong> | 제약으로 잘못된 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 입력 차단 |
| **컴플라이언스** | [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/)·[개인정보보호법](/studynote/09_security/16_data_privacy/783_pipa_korea/) 준수 |
| <strong><a href="/studynote/02_operating_system/10_security/606_auditing_linux_auditd/">감사</a> 추적</strong> | 누가 언제 무엇을 했는지 기록 |

[데이터 메시](/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)([Data Mesh](/studynote/12_it_management/05_security_compliance/320_data_mesh/)) 환경에서는 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)된 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 각각이 자체 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)·[보안 정책](/studynote/09_security/01_intro_principles/007_security_policy/)을 가지며, 연합 거버넌스(Federated Governance)가 전사 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)과 조율한다. 이는 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)·보안의 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 관리 패러다임으로의 전환이다.

- **📢 섹션 요약 비유**: [데이터 메시](/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)의 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [무결성](/studynote/09_security/01_intro_principles/003_integrity/)·보안은 연방제 나라의 법 시스템이다. 각 주([도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/))가 자체 법([정책](/studynote/10_ai/02_dl_architecture_new/164_policy/))을 가지지만, 연방(전사 거버넌스) 헌법의 테두리 안에서 운영된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **ACID** | [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [무결성 보장](/studynote/05_database/07_exam_summary/442_consistency_integrity/) |
| <strong><a href="/studynote/09_security/11_iam_access_control/569_rbac/">RBAC</a></strong> | 역할 기반 [접근 통제](/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/) 표준 |
| <strong><a href="/studynote/09_security/16_data_privacy/791_gdpr_eu/">GDPR</a></strong> | [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) 보안·[무결성](/studynote/09_security/01_intro_principles/003_integrity/) 법규 |
| <strong>SQL <a href="/studynote/04_software_engineering/11_testing_validation/872_injection/">인젝션</a></strong> | DB 보안 주요 위협 |
| <strong><a href="/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/">데이터 메시</a></strong> | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [무결성](/studynote/09_security/01_intro_principles/003_integrity/)·보안 패러다임 |

### 📈 관련 키워드 및 발전 흐름도

```text
[파일 시스템 — 무결성·보안 미흡]
    |
    v
[RDBMS 제약 조건 — 개체·참조·도메인 무결성]
    |
    v
[RBAC·DAC·MAC — 접근 통제 모델 표준화]
    |
    v
[암호화·감사 — 열 수준 암호화, 감사 로그]
    |
    v
[제로 트러스트 DB — 내부 사용자도 항상 검증]
    |
    v
[데이터 메시 — 분산 도메인별 무결성·보안 자치]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성](/studynote/09_security/01_intro_principles/003_integrity/)은 은행 장부가 항상 정확해야 하는 거예요 — 잘못된 금액 입력은 자동으로 차단돼요!
2. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 보안은 금고 [접근 통제](/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/)예요 — 허가된 사람만 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 접근할 수 있어요!
3. 현대 DB는 여러 겹의 보안(양파 껍질)으로 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)과 보안을 동시에 지켜요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 30 / 600

<- **이전**: [29. 파일 시스템의 문제점 (File System Problems)](/studynote/05_database/01_db_architecture_relational/029_file_system_problems/)
**다음**: [31. 클라이언트-서버 DBMS 아키텍처 — DB 접근 구조](/studynote/05_database/01_db_architecture_relational/031_client_server_dbms_architecture/) ->

---
