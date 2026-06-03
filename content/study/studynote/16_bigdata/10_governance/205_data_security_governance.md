---
title: 199. 데이터 보안 거버넌스 (Data Security Governance) — 암호화/접근제어/감사로그
date: '2026-04-21'
tags:
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)

- **본질**: [[001_dikw_pyramid|데이터]] [[006_security_governance|보안 거버넌스]]는 암호화(저장/전송/키 관리)·접근 제어([[569_rbac|RBAC]]/[[572_abac|ABAC]]/[[575_rebac|ReBAC]])·[[819_data_masking|데이터 마스킹]](정적/동적)·[[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]]·[[386_dlp|DLP]]([[823_dlp|Data Loss Prevention]])의 다층 방어 체계로 [[001_dikw_pyramid|데이터]] 자산을 [[571_protection_vs_security|보호]]한다.
- **가치**: [[667_zero_trust_runtime_integrity_measurement|Zero Trust]] 원칙("절대 신뢰하지 않고, 항상 [[395_verification_process_review|검증]]")을 [[001_dikw_pyramid|데이터]] 접근에 적용하면, 내부자 위협과 침해사고 모두에 대한 강력한 방어선을 구축할 수 있다.
- **판단 포인트**: 컬럼 수준·행 수준 보안([[150_unity_catalog|Unity Catalog]], [[263_storage_compute_separation_bigquery|BigQuery]] Authorized [[151_sql_view_virtual_table|View]])과 동적 [[819_data_masking|데이터 마스킹]](DDM)의 조합이 현대 클라우드 [[001_dikw_pyramid|데이터]] 플랫폼에서 [[010_least_privilege|최소 권한 원칙]]을 실현하는 핵심 기법이다.

---

## Ⅰ. 개요 및 필요성

[[001_dikw_pyramid|데이터]] [[006_security_governance|보안 거버넌스]]는 [[001_dikw_pyramid|데이터]]의 **[[002_confidentiality|기밀성]]([[002_confidentiality|Confidentiality]])·[[003_integrity|무결성]]([[003_integrity|Integrity]])·[[452_availability|가용성]]([[452_availability|Availability]], [[001_cia_triad|CIA Triad]])**을 보장하면서, 동시에 비즈니스 활용을 최대화하는 균형을 추구한다.

### 주요 위협과 [[571_protection_vs_security|보호]] 목표

| 위협 유형 | 예시 | [[571_protection_vs_security|보호]] 수단 |
|:---|:---|:---|
| 외부 침해 | 해킹, SQL [[480_injection|인젝션]] | 암호화, 접근 제어, [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]] |
| 내부자 위협 | 직원 [[001_dikw_pyramid|데이터]] 유출 | 최소 권한 접근, [[386_dlp|DLP]], [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]] |
| 무단 접근 | 권한 없는 [[298_qkv_attention|쿼리]] | [[569_rbac|RBAC]]/[[572_abac|ABAC]], 행/컬럼 수준 보안 |
| [[001_dikw_pyramid|데이터]] 유출 | 대량 [[001_dikw_pyramid|데이터]] export | [[386_dlp|DLP]], 다운로드 제한 |
| 규정 위반 | PII 노출 | [[819_data_masking|데이터 마스킹]], [[606_auditing_linux_auditd|감사]] 추적 |

**📢 섹션 요약 비유**: [[001_dikw_pyramid|데이터]] [[006_security_governance|보안 거버넌스]]는 **은행 금고 시스템**이다. 암호화(금고 잠금장치), 접근 제어(출입 [[303_authentication_authorization_patterns|인증]]), [[172_maas_mobility_as_a_service|마스]]킹(가림판으로 금액 일부 가림), [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]]([[933_cctv|CCTV]]+입출기록), [[386_dlp|DLP]](대량 현금 반출 경보)의 다층 보안으로 자산을 [[571_protection_vs_security|보호]]한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[001_dikw_pyramid|데이터]] 보안 다층 방어 구조

```
┌─────────────────────────────────────────────────────────────┐
│               데이터 보안 거버넌스 다층 방어                  │
├─────────────────────────────────────────────────────────────┤
│  Layer 1: 암호화 (Encryption)                               │
│  ┌──────────────┬────────────────┬─────────────────────┐    │
│  │  저장 암호화 │   전송 암호화  │   키 관리           │    │
│  │  (At Rest)   │  (In Transit)  │   (Key Mgmt)        │    │
│  │  AES-256-GCM │   TLS 1.3      │  HSM / AWS KMS      │    │
│  └──────────────┴────────────────┴─────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│  Layer 2: 접근 제어 (Access Control)                        │
│  ┌───────────┬───────────────┬──────────────────────────┐   │
│  │   RBAC    │     ABAC      │         ReBAC            │   │
│  │ 역할 기반 │   속성 기반   │    관계 기반             │   │
│  │ 접근 제어 │   접근 제어   │  (Google Zanzibar)       │   │
│  └───────────┴───────────────┴──────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  Layer 3: 데이터 마스킹 (Data Masking)                      │
│  ┌──────────────────────┬──────────────────────────────┐    │
│  │  정적 마스킹 (SDM)   │   동적 마스킹 (DDM)          │    │
│  │  비프로덕션 복사본   │  쿼리 시점 역할별 마스킹     │    │
│  │  에 마스킹 적용      │  (컬럼별 정책)               │    │
│  └──────────────────────┴──────────────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│  Layer 4: 감사 로그 (Audit Log)                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Who(누가) + When(언제) + What(무엇을) + How(어떻게) │   │
│  │  불변 저장 (Immutable, Append-only, WORM Storage)    │   │
│  └──────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  Layer 5: DLP (Data Loss Prevention)                       │
│  정책 기반 데이터 반출 차단 (대량 export, 외부 전송 감지)   │
└─────────────────────────────────────────────────────────────┘
```

### 접근 제어 모델 비교

| 모델 | 정의 | 장점 | 단점 | 예시 |
|:---|:---|:---|:---|:---|
| **[[569_rbac|RBAC]]** (Role-Based) | 역할에 권한 부여, 사용자를 역할에 할당 | 관리 단순, 이해 쉬움 | 세밀한 제어 한계 | "분석가 역할 = 읽기 권한" |
| **[[572_abac|ABAC]]** ([[082_attribute_types_er_model|Attribute]]-Based) | 사용자·[[001_dikw_pyramid|데이터]]·환경 [[082_attribute_types_er_model|속성]] 기반 [[164_policy|정책]] | 세밀한 제어 | [[164_policy|정책]] 복잡 | "자국 [[001_dikw_pyramid|데이터]]만 접근 가능" |
| **[[575_rebac|ReBAC]]** ([[083_relationship_in_er_model|Relationship]]-Based) | [[083_relationship_in_er_model|관계]] [[070_graph_datastructure|그래프]] 기반 권한 | 직관적, 확장성 | 구현 복잡 | Google [[576_zanzibar|Zanzibar]] "이 문서 공유받은 사람" |

### [[819_data_masking|데이터 마스킹]] 방식

```
실제 데이터:     주민등록번호 851231-1234567
                 신용카드번호 4532-1234-5678-9012

SDM (정적 마스킹):  개발/테스트 환경용 복사본 생성 시 영구 치환
                 → 851231-*******
                 → 4532-****-****-9012

DDM (동적 마스킹):  프로덕션 데이터 유지, 쿼리 시점에 역할별 표시 변경
  일반 사용자:   → 85****-*******
  고급 사용자:   → 851231-1234567 (완전 표시)
  외부 파트너:   → ***-***-**** (완전 마스킹)
```

**📢 섹션 요약 비유**: [[569_rbac|RBAC]] vs ABAC는 **건물 출입 카드 vs 지문+역할+시간 복합 [[303_authentication_authorization_patterns|인증]]** 차이다. 출입 카드([[569_rbac|RBAC]])는 카드만 있으면 들어갈 수 있지만, 복합 [[303_authentication_authorization_patterns|인증]]([[572_abac|ABAC]])은 누구인지, 어떤 용무인지, 몇 시인지 모두 [[396_validation|확인]]한다.

---

## Ⅲ. 비교 및 연결

### [[667_zero_trust_runtime_integrity_measurement|Zero Trust]] [[001_dikw_pyramid|데이터]] 접근 원칙

기존 경계 보안 모델("내부망은 신뢰, 외부는 차단")에서 **[[667_zero_trust_runtime_integrity_measurement|Zero Trust]]** 모델로의 전환:

| 기존 경계 보안 | [[667_zero_trust_runtime_integrity_measurement|Zero Trust]] |
|:---|:---|
| "내부망 = 안전" 전제 | "아무것도 신뢰하지 않는다" 원칙 |
| [[983_vpn_virtual_private_network|VPN]] 연결 후 전체 접근 | 모든 요청을 매번 [[303_authentication_authorization_patterns|인증]]·[[395_verification_process_review|검증]] |
| 역할 기반 광범위 접근 | 최소 권한([[010_least_privilege|Least Privilege]]) |
| 정기적 [[606_auditing_linux_auditd|감사]] | 상시 지속 [[229_monitor|모니터]]링 |

### 컬럼/행 수준 보안 ([[399_fine_grained_multithreading|Fine-grained]] [[283_security_tactics|Security]])

현대 클라우드 [[001_dikw_pyramid|데이터]] 플랫폼은 테이블 전체가 아닌 **컬럼·행 수준의 세밀한 접근 제어**를 지원한다:

- **[[074_photon_engine|Databricks]] [[150_unity_catalog|Unity Catalog]]**: [[394_catalog_metadata|카탈로그]]·[[005_schema|스키마]]·테이블·컬럼·행 수준 권한 통합 관리
- **[[263_storage_compute_separation_bigquery|BigQuery]] Authorized Views**: 뷰를 통한 컬럼 [[172_maas_mobility_as_a_service|마스]]킹, 행 필터
- **[[541_cassandra|Snowflake]] Dynamic [[819_data_masking|Data Masking]]**: 컬럼별 [[172_maas_mobility_as_a_service|마스]]킹 [[164_policy|정책]], 역할 기반 표시

**📢 섹션 요약 비유**: 컬럼·행 수준 보안은 **투명한 색안경**과 같다. 같은 표를 보더라도, 일반 직원은 이름·전화번호 컬럼이 흐릿하게 보이고, 권한이 있는 관리자만 선명하게 볼 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 암호화 [[268_strategy_pattern|전략]]

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

### [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]] 불변성 보장

[[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]]의 **[[003_integrity|무결성]](Tamper-Evidence)**이 중요한 이유: [[568_logs_distributed_logging_elk_fluentd|로그]]를 삭제·변조하면 규정 준수 증거로서의 가치가 없다.

- **[[590_worm|WORM]] ([[693_worm_storage|Write Once Read Many]]) 스토리지**: AWS S3 Object [[510_lock|Lock]], Azure [[298_immutable|Immutable]] Blob
- **[[004_blockchain|블록체인]] 해시 체인**: [[568_logs_distributed_logging_elk_fluentd|로그]] 항목을 이전 해시와 연결하여 위변조 감지
- **[[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]] 접근 제어**: [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]] 자체에 대한 접근도 로깅 ([[568_logs_distributed_logging_elk_fluentd|로그]]의 [[568_logs_distributed_logging_elk_fluentd|로그]])

**📢 섹션 요약 비유**: [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]]의 불변성은 **법정 증거 봉인**과 같다. 한 번 봉인된 증거는 수정·삭제가 불가하며, 위변조 흔적이 남는다.

---

## Ⅴ. 기대효과 및 결론

### [[001_dikw_pyramid|데이터]] [[006_security_governance|보안 거버넌스]] 도입 효과

| 영역 | 효과 |
|:---|:---|
| **침해 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]]** | [[001_dikw_pyramid|데이터]] 침해 비용 평균 432만 달러(IBM 2023) 예방 |
| **규정 준수** | [[791_gdpr_eu|GDPR]]/PIPA 위반 과징금 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] 최소화 |
| **내부자 위협** | 이상 접근 탐지 시간 대폭 단축 |
| **[[667_zero_trust_runtime_integrity_measurement|Zero Trust]] 달성** | 최소 권한 + 지속 [[395_verification_process_review|검증]]으로 공격 표면 최소화 |

### 결론

[[001_dikw_pyramid|데이터]] [[006_security_governance|보안 거버넌스]]는 **[[001_dikw_pyramid|데이터]] 자산 [[571_protection_vs_security|보호]]와 비즈니스 활용 가능성의 균형**을 추구한다. 지나친 보안은 [[001_dikw_pyramid|데이터]] 활용을 막고, 과도한 개방은 침해 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]]를 높인다. 암호화·접근 제어·[[172_maas_mobility_as_a_service|마스]]킹·[[606_auditing_linux_auditd|감사]]·DLP의 다층 방어를 [[667_zero_trust_runtime_integrity_measurement|Zero Trust]] 원칙 하에 설계하고, [[531_cloud_native_architecture|클라우드 네이티브]] 보안 도구([[150_unity_catalog|Unity Catalog]], [[127_kms_knowledge_management_system|KMS]], CloudTrail)를 활용한 자동화가 현대 [[001_dikw_pyramid|데이터]] [[006_security_governance|보안 거버넌스]]의 방향이다.

**📢 섹션 요약 비유**: [[001_dikw_pyramid|데이터]] [[006_security_governance|보안 거버넌스]]는 **양파 껍질 구조**다. 암호화·접근제어·[[172_maas_mobility_as_a_service|마스]]킹·[[606_auditing_linux_auditd|감사]]·[[386_dlp|DLP]] 레이어가 마치 양파처럼 겹겹이 쌓여 있어, 한 레이어가 뚫려도 다음 레이어가 방어한다.

---

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---|:---|:---|
| [[656_aes_advanced_encryption_standard_rijndael|AES]]-256-[[659_gcm_galois_counter_mode_aead|GCM]] | [[504_cryptography_algorithms_aes_rsa_sha|암호화 알고리즘]] | 저장 [[001_dikw_pyramid|데이터]] 암호화 표준 |
| [[694_thread_local_storage_tls|TLS]] 1.3 | 전송 암호화 | [[001_dikw_pyramid|데이터]] 전송 [[571_protection_vs_security|보호]] 최신 [[295_protocol_field_tcp_udp_icmp|프로토콜]] |
| [[569_rbac|RBAC]] | 접근 제어 모델 | 역할 기반 권한 관리 |
| [[572_abac|ABAC]] | 접근 제어 모델 | [[082_attribute_types_er_model|속성]] 기반 세밀한 [[164_policy|정책]] |
| DDM | [[172_maas_mobility_as_a_service|마스]]킹 방식 | [[298_qkv_attention|쿼리]] 시점 동적 [[819_data_masking|데이터 마스킹]] |
| [[667_zero_trust_runtime_integrity_measurement|Zero Trust]] | 보안 원칙 | 아무것도 신뢰하지 않고 항상 [[395_verification_process_review|검증]] |
| [[150_unity_catalog|Unity Catalog]] | 플랫폼 | [[074_photon_engine|Databricks]] 컬럼·행 수준 보안 통합 |
| [[590_worm|WORM]] 스토리지 | [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]] | [[693_worm_storage|Write Once Read Many]] 불변 저장 |


### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 분류 (Data Classification) — 민감도 수준별 데이터 목록화, 보안 정책의 출발점]
    │
    ▼
[접근 제어 (RBAC·ABAC) — 역할·속성 기반 세분화 권한 관리, 최소 권한 원칙 적용]
    │
    ▼
[암호화 (AES-256-GCM 저장·TLS 1.3 전송) + 데이터 마스킹 — 저장·전송·쿼리 시점 데이터 보호]
    │
    ▼
[감사 로그 (Audit Log) + WORM 스토리지 — 불변 로그로 침해 사고 추적·규정 준수 증명]
    │
    ▼
[Zero Trust + Unity Catalog — 컬럼·행 수준까지 보안을 통합 거버넌스]
```

이 흐름은 [[808_data_classification|데이터 분류]]를 출발점으로 접근 제어→암호화·[[172_maas_mobility_as_a_service|마스]]킹→불변 [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]]로 [[001_dikw_pyramid|데이터]] 보안의 계층을 쌓고, 최종적으로 [[667_zero_trust_runtime_integrity_measurement|Zero Trust]] 원칙과 Unity Catalog가 컬럼·행 수준까지 통합 거버넌스를 구현하는 [[001_dikw_pyramid|데이터]] [[006_security_governance|보안 거버넌스]]의 성숙 계보를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

- [[001_dikw_pyramid|데이터]] [[006_security_governance|보안 거버넌스]]는 **학교 귀중품 보관 시스템**이에요: 자물쇠(암호화), 출입 카드(접근 제어), 가리개([[172_maas_mobility_as_a_service|마스]]킹), [[933_cctv|CCTV]]([[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]]), 대량 반출 경보([[386_dlp|DLP]])가 모두 함께 작동해요.
- [[585_zero_skipping|Zero]] Trust는 "학교 교직원도 매번 신분증을 [[396_validation|확인]]한다"는 원칙이에요 — 내부 사람이라도 항상 [[395_verification_process_review|검증]]해야 더 안전해요.
- [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]]는 **절대 지울 수 없는 출입 기록부**예요: 언제, 누가, 무엇을 보았는지 기록이 남아 나중에 문제가 생겼을 때 반드시 추적할 수 있어요.
