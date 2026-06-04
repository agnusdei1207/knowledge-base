+++
title = "199. 데이터 보안 거버넌스 (Data Security Governance) — 암호화/접근제어/감사로그"
date = 2026-04-21

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)

- **본질**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [보안 거버넌스](/knowledge-base/studynote/09_security/01_intro_principles/006_security_governance/)는 암호화(저장/전송/키 관리)·접근 제어([RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/)/[ABAC](/knowledge-base/studynote/09_security/11_iam_access_control/572_abac/)/[ReBAC](/knowledge-base/studynote/09_security/11_iam_access_control/575_rebac/))·[데이터 마스킹](/knowledge-base/studynote/09_security/16_data_privacy/819_data_masking/)(정적/동적)·[감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·[DLP](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/386_dlp/)([Data Loss Prevention](/knowledge-base/studynote/09_security/16_data_privacy/823_dlp/))의 다층 방어 체계로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자산을 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)한다.
- **가치**: [Zero Trust](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) 원칙("절대 신뢰하지 않고, 항상 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)")을 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근에 적용하면, 내부자 위협과 침해사고 모두에 대한 강력한 방어선을 구축할 수 있다.
- **판단 포인트**: 컬럼 수준·행 수준 보안([Unity Catalog](/knowledge-base/studynote/16_bigdata/07_data_lake/150_unity_catalog/), [BigQuery](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/) Authorized [View](/knowledge-base/studynote/05_database/03_relational_model/151_sql_view_virtual_table/))과 동적 [데이터 마스킹](/knowledge-base/studynote/09_security/16_data_privacy/819_data_masking/)(DDM)의 조합이 현대 클라우드 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼에서 [최소 권한 원칙](/knowledge-base/studynote/09_security/01_intro_principles/010_least_privilege/)을 실현하는 핵심 기법이다.

---

## Ⅰ. 개요 및 필요성

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [보안 거버넌스](/knowledge-base/studynote/09_security/01_intro_principles/006_security_governance/)는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 <strong><a href="/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/">기밀성</a>(<a href="/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/">Confidentiality</a>)·<a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">무결성</a>(<a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">Integrity</a>)·<a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a>(<a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">Availability</a>, <a href="/knowledge-base/studynote/09_security/01_intro_principles/001_cia_triad/">CIA Triad</a>)</strong>을 보장하면서, 동시에 비즈니스 활용을 최대화하는 균형을 추구한다.

### 주요 위협과 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 목표

| 위협 유형 | 예시 | [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 수단 |
|:---|:---|:---|
| 외부 침해 | 해킹, SQL [인젝션](/knowledge-base/studynote/04_software_engineering/11_testing_validation/872_injection/) | 암호화, 접근 제어, [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) |
| 내부자 위협 | 직원 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유출 | 최소 권한 접근, [DLP](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/386_dlp/), [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) |
| 무단 접근 | 권한 없는 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) | [RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/)/[ABAC](/knowledge-base/studynote/09_security/11_iam_access_control/572_abac/), 행/컬럼 수준 보안 |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유출 | 대량 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) export | [DLP](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/386_dlp/), 다운로드 제한 |
| 규정 위반 | PII 노출 | [데이터 마스킹](/knowledge-base/studynote/09_security/16_data_privacy/819_data_masking/), [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적 |

**📢 섹션 요약 비유**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [보안 거버넌스](/knowledge-base/studynote/09_security/01_intro_principles/006_security_governance/)는 <strong>은행 금고 시스템</strong>이다. 암호화(금고 잠금장치), 접근 제어(출입 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)), [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)킹(가림판으로 금액 일부 가림), [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)([CCTV](/knowledge-base/studynote/09_security/18_iot_ot_physical/933_cctv/)+입출기록), [DLP](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/386_dlp/)(대량 현금 반출 경보)의 다층 보안으로 자산을 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 보안 다층 방어 구조

```
+-------------------------------------------------------------+
|               데이터 보안 거버넌스 다층 방어                  |
+-------------------------------------------------------------+
|  Layer 1: 암호화 (Encryption)                               |
|  +--------------+----------------+---------------------+    |
|  |  저장 암호화 |   전송 암호화  |   키 관리           |    |
|  |  (At Rest)   |  (In Transit)  |   (Key Mgmt)        |    |
|  |  AES-256-GCM |   TLS 1.3      |  HSM / AWS KMS      |    |
|  +--------------+----------------+---------------------+    |
+-------------------------------------------------------------+
|  Layer 2: 접근 제어 (Access Control)                        |
|  +-----------+---------------+--------------------------+   |
|  |   RBAC    |     ABAC      |         ReBAC            |   |
|  | 역할 기반 |   속성 기반   |    관계 기반             |   |
|  | 접근 제어 |   접근 제어   |  (Google Zanzibar)       |   |
|  +-----------+---------------+--------------------------+   |
+-------------------------------------------------------------+
|  Layer 3: 데이터 마스킹 (Data Masking)                      |
|  +----------------------+------------------------------+    |
|  |  정적 마스킹 (SDM)   |   동적 마스킹 (DDM)          |    |
|  |  비프로덕션 복사본   |  쿼리 시점 역할별 마스킹     |    |
|  |  에 마스킹 적용      |  (컬럼별 정책)               |    |
|  +----------------------+------------------------------+    |
+-------------------------------------------------------------+
|  Layer 4: 감사 로그 (Audit Log)                             |
|  +------------------------------------------------------+   |
|  |  Who(누가) + When(언제) + What(무엇을) + How(어떻게) |   |
|  |  불변 저장 (Immutable, Append-only, WORM Storage)    |   |
|  +------------------------------------------------------+   |
+-------------------------------------------------------------+
|  Layer 5: DLP (Data Loss Prevention)                       |
|  정책 기반 데이터 반출 차단 (대량 export, 외부 전송 감지)   |
+-------------------------------------------------------------+
```

### 접근 제어 모델 비교

| 모델 | 정의 | 장점 | 단점 | 예시 |
|:---|:---|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/">RBAC</a></strong> (Role-Based) | 역할에 권한 부여, 사용자를 역할에 할당 | 관리 단순, 이해 쉬움 | 세밀한 제어 한계 | "분석가 역할 = 읽기 권한" |
| <strong><a href="/knowledge-base/studynote/09_security/11_iam_access_control/572_abac/">ABAC</a></strong> ([Attribute](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)-Based) | 사용자·[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·환경 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 기반 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) | 세밀한 제어 | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 복잡 | "자국 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 접근 가능" |
| <strong><a href="/knowledge-base/studynote/09_security/11_iam_access_control/575_rebac/">ReBAC</a></strong> ([Relationship](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)-Based) | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 기반 권한 | 직관적, 확장성 | 구현 복잡 | Google [Zanzibar](/knowledge-base/studynote/09_security/11_iam_access_control/576_zanzibar/) "이 문서 공유받은 사람" |

### [데이터 마스킹](/knowledge-base/studynote/09_security/16_data_privacy/819_data_masking/) 방식

```
실제 데이터:     주민등록번호 851231-1234567
                 신용카드번호 4532-1234-5678-9012

SDM (정적 마스킹):  개발/테스트 환경용 복사본 생성 시 영구 치환
                 -> 851231-*******
                 -> 4532-****-****-9012

DDM (동적 마스킹):  프로덕션 데이터 유지, 쿼리 시점에 역할별 표시 변경
  일반 사용자:   -> 85****-*******
  고급 사용자:   -> 851231-1234567 (완전 표시)
  외부 파트너:   -> ***-***-**** (완전 마스킹)
```

**📢 섹션 요약 비유**: [RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/) vs ABAC는 <strong>건물 출입 카드 vs 지문+역할+시간 복합 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a></strong> 차이다. 출입 카드([RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/))는 카드만 있으면 들어갈 수 있지만, 복합 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)([ABAC](/knowledge-base/studynote/09_security/11_iam_access_control/572_abac/))은 누구인지, 어떤 용무인지, 몇 시인지 모두 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.

---

## Ⅲ. 비교 및 연결

### [Zero Trust](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근 원칙

기존 경계 보안 모델("내부망은 신뢰, 외부는 차단")에서 <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/">Zero Trust</a></strong> 모델로의 전환:

| 기존 경계 보안 | [Zero Trust](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) |
|:---|:---|
| "내부망 = 안전" 전제 | "아무것도 신뢰하지 않는다" 원칙 |
| [VPN](/knowledge-base/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) 연결 후 전체 접근 | 모든 요청을 매번 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)·[검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| 역할 기반 광범위 접근 | 최소 권한([Least Privilege](/knowledge-base/studynote/09_security/01_intro_principles/010_least_privilege/)) |
| 정기적 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) | 상시 지속 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링 |

### 컬럼/행 수준 보안 ([Fine-grained](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/399_fine_grained_multithreading/) [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/))

현대 클라우드 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼은 테이블 전체가 아닌 <strong>컬럼·행 수준의 세밀한 접근 제어</strong>를 지원한다:

- <strong><a href="/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/">Databricks</a> <a href="/knowledge-base/studynote/16_bigdata/07_data_lake/150_unity_catalog/">Unity Catalog</a></strong>: [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/)·[스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)·테이블·컬럼·행 수준 권한 통합 관리
- <strong><a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/263_storage_compute_separation_bigquery/">BigQuery</a> Authorized Views</strong>: 뷰를 통한 컬럼 [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)킹, 행 필터
- <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/">Snowflake</a> Dynamic <a href="/knowledge-base/studynote/09_security/16_data_privacy/819_data_masking/">Data Masking</a></strong>: 컬럼별 [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)킹 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/), 역할 기반 표시

**📢 섹션 요약 비유**: 컬럼·행 수준 보안은 <strong>투명한 색안경</strong>과 같다. 같은 표를 보더라도, 일반 직원은 이름·전화번호 컬럼이 흐릿하게 보이고, 권한이 있는 관리자만 선명하게 볼 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 암호화 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

```
저장 암호화 (At-Rest):
  - AES-256-GCM: 블록 암호화, GCM 모드로 인증+암호화 동시
  - 클라우드 관리 키 (CMK): AWS S3 SSE-S3 / SSE-KMS
  - 고객 관리 키 (CMEK): 키를 직접 관리, 더 강한 통제
  - HSM (Hardware Security Module): 물리적 키 보호 장치

전송 암호화 (In-Transit):
  - TLS 1.3: 가장 최신 버전, 0-RTT 핸드셰이크, 취약 알고리즘 제거
  - MTLS (Mutual TLS): 서버+클라이언트 양방향 인증
  - 데이터베이스 연결: SSL/TLS 강제화 설정

키 관리 서비스:
  - AWS KMS: 클라우드 관리형 키 서비스, CloudHSM 연동 가능
  - Azure Key Vault: 비밀·키·인증서 중앙 관리
  - HashiCorp Vault: 멀티클라우드·온프렘 범용
```

### [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 불변성 보장

[감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)의 <strong><a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">무결성</a>(Tamper-Evidence)</strong>이 중요한 이유: [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 삭제·변조하면 규정 준수 증거로서의 가치가 없다.

- <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/590_worm/">WORM</a> (<a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/693_worm_storage/">Write Once Read Many</a>) 스토리지</strong>: AWS S3 Object [Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/), Azure [Immutable](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/298_immutable/) Blob
- <strong><a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/">블록체인</a> 해시 체인</strong>: [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 항목을 이전 해시와 연결하여 위변조 감지
- <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/">감사</a> <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a> 접근 제어</strong>: [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 자체에 대한 접근도 로깅 ([로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)의 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/))

**📢 섹션 요약 비유**: [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)의 불변성은 <strong>법정 증거 봉인</strong>과 같다. 한 번 봉인된 증거는 수정·삭제가 불가하며, 위변조 흔적이 남는다.

---

## Ⅴ. 기대효과 및 결론

### [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [보안 거버넌스](/knowledge-base/studynote/09_security/01_intro_principles/006_security_governance/) 도입 효과

| 영역 | 효과 |
|:---|:---|
| <strong>침해 <a href="/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/">리스크</a></strong> | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 침해 비용 평균 432만 달러(IBM 2023) 예방 |
| **규정 준수** | [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/)/PIPA 위반 과징금 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 최소화 |
| **내부자 위협** | 이상 접근 탐지 시간 대폭 단축 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/">Zero Trust</a> 달성</strong> | 최소 권한 + 지속 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)으로 공격 표면 최소화 |

### 결론

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [보안 거버넌스](/knowledge-base/studynote/09_security/01_intro_principles/006_security_governance/)는 <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 자산 <a href="/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/">보호</a>와 비즈니스 활용 가능성의 균형</strong>을 추구한다. 지나친 보안은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 활용을 막고, 과도한 개방은 침해 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)를 높인다. 암호화·접근 제어·[마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)킹·[감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)·DLP의 다층 방어를 [Zero Trust](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) 원칙 하에 설계하고, [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 보안 도구([Unity Catalog](/knowledge-base/studynote/16_bigdata/07_data_lake/150_unity_catalog/), [KMS](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/127_kms_knowledge_management_system/), CloudTrail)를 활용한 자동화가 현대 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [보안 거버넌스](/knowledge-base/studynote/09_security/01_intro_principles/006_security_governance/)의 방향이다.

**📢 섹션 요약 비유**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [보안 거버넌스](/knowledge-base/studynote/09_security/01_intro_principles/006_security_governance/)는 <strong>양파 껍질 구조</strong>다. 암호화·접근제어·[마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)킹·[감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)·[DLP](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/386_dlp/) 레이어가 마치 양파처럼 겹겹이 쌓여 있어, 한 레이어가 뚫려도 다음 레이어가 방어한다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| [AES](/knowledge-base/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/)-256-[GCM](/knowledge-base/studynote/03_network/13_network_security_basics/659_gcm_galois_counter_mode_aead/) | [암호화 알고리즘](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/504_cryptography_algorithms_aes_rsa_sha/) | 저장 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 암호화 표준 |
| [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 | 전송 암호화 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 최신 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) |
| [RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/) | 접근 제어 모델 | 역할 기반 권한 관리 |
| [ABAC](/knowledge-base/studynote/09_security/11_iam_access_control/572_abac/) | 접근 제어 모델 | [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 기반 세밀한 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) |
| DDM | [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)킹 방식 | [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 시점 동적 [데이터 마스킹](/knowledge-base/studynote/09_security/16_data_privacy/819_data_masking/) |
| [Zero Trust](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) | 보안 원칙 | 아무것도 신뢰하지 않고 항상 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| [Unity Catalog](/knowledge-base/studynote/16_bigdata/07_data_lake/150_unity_catalog/) | 플랫폼 | [Databricks](/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/) 컬럼·행 수준 보안 통합 |
| [WORM](/knowledge-base/studynote/02_operating_system/10_security/590_worm/) 스토리지 | [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) | [Write Once Read Many](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/693_worm_storage/) 불변 저장 |


### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 분류 (Data Classification) — 민감도 수준별 데이터 목록화, 보안 정책의 출발점]
    |
    v
[접근 제어 (RBAC·ABAC) — 역할·속성 기반 세분화 권한 관리, 최소 권한 원칙 적용]
    |
    v
[암호화 (AES-256-GCM 저장·TLS 1.3 전송) + 데이터 마스킹 — 저장·전송·쿼리 시점 데이터 보호]
    |
    v
[감사 로그 (Audit Log) + WORM 스토리지 — 불변 로그로 침해 사고 추적·규정 준수 증명]
    |
    v
[Zero Trust + Unity Catalog — 컬럼·행 수준까지 보안을 통합 거버넌스]
```

이 흐름은 [데이터 분류](/knowledge-base/studynote/09_security/16_data_privacy/808_data_classification/)를 출발점으로 접근 제어->암호화·[마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)킹->불변 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 보안의 계층을 쌓고, 최종적으로 [Zero Trust](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) 원칙과 Unity Catalog가 컬럼·행 수준까지 통합 거버넌스를 구현하는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [보안 거버넌스](/knowledge-base/studynote/09_security/01_intro_principles/006_security_governance/)의 성숙 계보를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

- [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [보안 거버넌스](/knowledge-base/studynote/09_security/01_intro_principles/006_security_governance/)는 <strong>학교 귀중품 보관 시스템</strong>이에요: 자물쇠(암호화), 출입 카드(접근 제어), 가리개([마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)킹), [CCTV](/knowledge-base/studynote/09_security/18_iot_ot_physical/933_cctv/)([감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)), 대량 반출 경보([DLP](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/386_dlp/))가 모두 함께 작동해요.
- [Zero](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/) Trust는 "학교 교직원도 매번 신분증을 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다"는 원칙이에요 — 내부 사람이라도 항상 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)해야 더 안전해요.
- [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 <strong>절대 지울 수 없는 출입 기록부</strong>예요: 언제, 누가, 무엇을 보았는지 기록이 남아 나중에 문제가 생겼을 때 반드시 추적할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 205 / 262

<- **이전**: [198. 마스터 데이터 관리 (MDM, Master Data Management) — 황금 레코드 생성](/knowledge-base/studynote/16_bigdata/10_governance/204_mdm/)
**다음**: [200. 개인정보보호법 빅데이터 특례 (PIPA Big Data Exception) — 가명처리 허용 데이터 3법](/knowledge-base/studynote/16_bigdata/10_governance/206_pipa_bigdata_exception/) ->

---
