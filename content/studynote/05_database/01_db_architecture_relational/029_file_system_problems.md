+++
title = "29. 파일 시스템의 문제점 (File System Problems)"
date = 2026-04-29

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 이전 시대의 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 기반 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중복, [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 부재, [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 제어 불가, 보안 취약이라는 5대 문제를 구조적으로 가지고 있었다. DBMS는 이를 해결하기 위해 탄생했다.
> 2. **가치**: [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 문제를 이해하면 DBMS가 제공하는 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 레이어([데이터 독립성](/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/), [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/), [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/), 접근 제어)의 가치가 명확해진다. 현대 [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)에서도 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 로컬 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 저장은 동일한 문제를 반복한다.
> 3. **판단 포인트**: [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 문제가 현대에도 반복되는 패턴이 있다. [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) DB를 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템처럼 사용하거나, [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)가 로컬 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에 의존하거나, CSV [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 교환하는 패턴에서 동일한 중복·불일치·[무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 문제가 재발한다.

---

## Ⅰ. 개요 및 필요성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">파일 시스템 5대 문제</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1. 데이터 중복성 (Data Redundancy)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 같은 고객 정보가 주문파일·배송파일·결제파일에 반복</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2. 데이터 불일치 (Data Inconsistency)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 한 파일 고객 주소 변경 시 다른 파일은 미반영</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3. 데이터 종속성 (Data Dependency)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 파일 구조 변경 시 모든 프로그램 수정 필요</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">4. 무결성 제약 없음 (No Integrity Constraints)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 잘못된 값(음수 나이, 존재하지 않는 외래 키) 저장 가능</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">5. 동시성·보안 부재 (No Concurrency/Security)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 여러 사용자 동시 수정 → 데이터 손상</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 문제는 포스트잇 관리 방식이다. 각 부서가 각자 포스트잇([파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))에 고객 정보를 적으면 중복·불일치·분실이 발생한다. DB는 모든 부서가 공유하는 화이트보드(중앙 관리)다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### DBMS가 제공하는 해결책

| [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 문제 | [DBMS](/knowledge-base/studynote/05_database/04_transactions_concurrency/502_dbms/) 해결책 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 중복</strong> | [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)([Normalization](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)), 단일 진실 소스 |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 불일치</strong> | [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) ACID, [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 제약 |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/">종속성</a></strong> | 물리적·[논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 [데이터 독립성](/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/) |
| <strong><a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">무결성</a> 부재</strong> | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)·[참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)·[개체 무결성](/knowledge-base/studynote/05_database/02_modeling_normalization/074_entity_integrity_primary_key/) 제약 |
| <strong><a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/">동시성</a> 부재</strong> | 락([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/)), [MVCC](/knowledge-base/studynote/11_design_supervision/06_exam_summary/449_mvcc/), [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 격리 |
| **보안 부재** | 뷰, GRANT/REVOKE, 역할 기반 접근 제어 |

### [데이터 독립성](/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">물리적 독립성: 저장 구조 변경 → 논리 스키마 불변</div>
<div class="kb-diagram-note">(예: HDD → SSD 마이그레이션, 파티셔닝)</div>
<div class="kb-diagram-note">논리적 독립성: 논리 스키마 변경 → 응용 프로그램 불변</div>
<div class="kb-diagram-note">(예: 테이블 컬럼 추가 시 기존 앱 수정 불필요)</div>
</div>
</div>



- **📢 섹션 요약 비유**: [데이터 독립성](/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/)은 건물 리모델링과 같다. 건물 내부(물리 저장)를 바꿔도 주소([논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/))는 유지되고, 방 배치([논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/))를 바꿔도 입주자(앱)는 계속 거주한다.

---

## Ⅲ. 비교 및 연결

| 비교 | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 | RDBMS |
|:---|:---|:---|
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중복 | 높음 | [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)로 최소화 |
| [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) | 앱 담당 | DB 레벨 보장 |
| [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) | 미지원 | [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)·락 |
| 독립성 | 낮음 | 3-Level [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) |
| 표준 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) | 없음 | SQL 표준 |

- **📢 섹션 요약 비유**: [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 vs DBMS는 개인 노트 vs 공유 협업 도구다. 개인 노트([파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))는 편하지만 공유하면 혼란이 생기고, 협업 도구(DB)는 모두가 최신 정보를 공유하며 충돌을 자동으로 해결한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 현대에도 반복되는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 문제 패턴



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">마이크로서비스 로컬 파일 저장:</div>
<div class="kb-diagram-note">서비스 A: /data/users.json</div>
<div class="kb-diagram-note">서비스 B: /data/users.json (별도 복사본)</div>
<div class="kb-diagram-note">→ 중복·불일치 재발 → 이벤트 소싱/공유 DB 필요</div>
<div class="kb-diagram-note">CSV 기반 데이터 교환:</div>
<div class="kb-diagram-note">각 팀이 Excel/CSV로 데이터 공유</div>
<div class="kb-diagram-note">→ 버전 불일치, 무결성 미보장</div>
<div class="kb-diagram-note">→ 데이터 허브/API 기반 교환으로 전환 필요</div>
<div class="kb-diagram-note">로그 파일 기반 상태 관리:</div>
<div class="kb-diagram-note">앱 상태를 로그 파일에 저장</div>
<div class="kb-diagram-note">→ 동시 접근 충돌, 일관성 보장 불가</div>
</div>
</div>



- **📢 섹션 요약 비유**: [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 로컬 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 부서별 포스트잇의 현대판이다. 각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 자신의 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 관리하면, 50년 전 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템이 겪었던 중복·불일치 문제가 그대로 재발한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a></strong> | ACID [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)으로 항상 일관 상태 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/">유지보수성</a></strong> | [데이터 독립성](/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/)으로 앱 수정 최소화 |
| **보안** | 중앙 접근 제어로 세밀한 권한 관리 |

[파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 문제는 현대 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템에서 변형된 형태로 재등장한다. [분산 파일 시스템](/knowledge-base/studynote/02_operating_system/09_file_system/553_distributed_file_system/)([HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/)), [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)(S3), [NoSQL](/knowledge-base/studynote/14_data_engineering/01_infrastructure/035_nosql/) DB는 각각 다른 방식으로 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템의 확장성 문제를 해결하면서도 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 문제는 새로운 방식으로 다룬다([CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리).

- **📢 섹션 요약 비유**: [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 문제의 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이다. "[일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)·[가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)·[파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 내성 중 두 가지만 선택하라"는 CAP는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템의 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 문제가 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에서 더욱 복잡해진다는 것을 보여준다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/004_data_independence/">데이터 독립성</a></strong> | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 문제의 해결책 |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/">정규화</a></strong> | [데이터 중복 제거](/knowledge-base/studynote/02_operating_system/09_file_system/546_data_deduplication/) |
| **ACID** | [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)·[동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 보장 |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/">CAP</a> 정리</strong> | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경의 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 트레이드오프 |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/">이벤트 소싱</a></strong> | [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 상태 관리 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">파일 시스템 — 데이터 중복·불일치·종속성 5대 문제</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">RDBMS — 정규화·ACID·SQL로 파일 시스템 문제 해결</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">분산 DB — CAP 정리, 일관성·가용성 트레이드오프</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">NoSQL — 스키마 유연성, 수평 확장</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">레이크하우스 — 파일 형식(Parquet)+ACID(Delta/Iceberg) 통합</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 문제는 각 부서가 따로 포스트잇을 쓸 때 생기는 혼란이에요! DB는 모두가 공유하는 화이트보드예요.
2. DB는 중복·불일치·[무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 문제를 자동으로 해결해줘서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 항상 최신·정확하게 유지해요!
3. 요즘 [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)에서도 똑같은 문제가 재발해서 [이벤트 소싱](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)이나 공유 DB 같은 해결책이 필요하답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 29 / 600

← **이전**: [28. 데이터베이스 사용자 유형 (Database Users)](/knowledge-base/studynote/05_database/01_db_architecture_relational/028_database_users/)
**다음**: [30. 데이터 무결성과 보안 — 데이터베이스 안전의 두 축](/knowledge-base/studynote/05_database/01_db_architecture_relational/030_data_integrity_security/) →

---
