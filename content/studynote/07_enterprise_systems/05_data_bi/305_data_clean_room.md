---
title: "Data Clean Room"
date: "2026-04-21"
tags:
  - "studynote-enterprise-systems"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Clean Room은 양사가 원시 PII (Personally Identifiable Information) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 공유하지 않고 집계 인사이트만 교환하는 프라이버시 보존 협업 환경이다.
> 2. **가치**: [쿠키](/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/)리스 시대에 퍼블리셔-광고주 간 캠페인 효과 측정과 제약사-병원 간 임상 분석이 법적 위험 없이 가능해진다.
> 3. **판단 포인트**: 프라이버시 예산(ε, epsilon)이 작을수록 [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)가 강하지만 분석 정확도가 낮아지는 트레이드오프를 사전에 설계해야 한다.

## Ⅰ. 개요 및 필요성

Google, Apple의 프라이버시 강화 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)과 [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/), [CCPA](/studynote/09_security/16_data_privacy/800_ccpa/) 등 [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) 규제가 강화되면서 기업 간 고객 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 직접 공유는 법적 [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)가 매우 높아졌다.
그러나 광고 효과 측정, 공동 마케팅, 임상 연구 등에서 기업 간 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 결합은 비즈니스적으로 반드시 필요하다.

[Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Clean Room은 이 딜레마를 해결한다. 원시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)([Raw](/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) PII)를 직접 교환하지 않고, 안전한 격리 환경에서 분석을 실행하여 집계 결과만 반환한다.

주요 기술:
- [SMPC](/studynote/09_security/20_extra_exam_prep/1018_secure_multi_party_computation/) ([Secure Multi-Party Computation](/studynote/09_security/20_extra_exam_prep/1018_secure_multi_party_computation/)): 각자 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 암호화한 채로 공동 계산
- [Differential Privacy](/studynote/09_security/16_data_privacy/817_differential_privacy/) ([차등 프라이버시](/studynote/16_bigdata/10_governance/209_differential_privacy/)): 결과에 노이즈를 추가해 개인 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 불가
- [TEE](/studynote/01_computer_architecture/14_hardware_security_trends/478_tee/) ([Trusted Execution Environment](/studynote/09_security/19_ai_advanced_security/972_tee_based_ml/)): [Intel SGX](/studynote/01_computer_architecture/14_hardware_security_trends/480_intel_sgx/) 등 하드웨어 보안 격리 실행

클라우드 기반 제품: AWS Clean Rooms, Google Ads [Data Hub](/studynote/16_bigdata/09_platform/180_data_hub/), [Snowflake](/studynote/05_database/04_transactions_concurrency/541_cassandra/) [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Clean Room

📢 **섹션 요약 비유**: 클린 룸은 밀봉된 투표함이다. 양측이 자기 표를 넣고 집계 결과만 보지, 상대방 표지를 직접 볼 수 없다.

## Ⅱ. 아키텍처 및 핵심 원리

### 클린 룸 프로세스

| 단계 | 설명 |
|:---|:---|
| 1. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 준비 | 양사가 자체 PII를 해시 처리 (SHA-256) |
| 2. 격리 환경 구성 | 클라우드 클린 룸 환경 [프로비저닝](/studynote/09_security/11_iam_access_control/528_provisioning/) |
| 3. 익명 조인 실행 | 해시된 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) 기준으로 교차 분석 |
| 4. 집계 임계값 적용 | 그룹 크기 <50명이면 결과 [억제](/studynote/09_security/13_secops_ir_forensics/656_ir_containment/) ([k-anonymity](/studynote/14_data_engineering/04_mlops/185_k_anonymity_masking_data_pipeline/)) |
| 5. 결과 반환 | 집계 통계만 반환, 개별 레코드 비공개 |

### [Differential Privacy](/studynote/09_security/16_data_privacy/817_differential_privacy/) 핵심

- ε=0.1: 매우 강한 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) (노이즈 크다)
- ε=1.0: 균형 (Google Chrome DP 적용값)
- ε=[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/).0: 약한 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) (실용적 분석 가능)

### [ASCII](/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램: [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Clean Room 흐름

```
  기업 A (광고주)                    기업 B (퍼블리셔)
  +------------------+              +------------------+
  | 고객 구매 데이터   |              | 방문자 행동 로그   |
  | (해시 처리 후)     |              | (해시 처리 후)     |
  | email_hash, age  |              | email_hash, page  |
  +--------+---------+              +--------+---------+
           |  해시 키만 제공                   |  해시 키만 제공
           +--------------+------------------+
                          v
           +-----------------------------------+
           |        DATA CLEAN ROOM            |
           |  (격리 실행 환경 / TEE)             |
           |  ① 해시 키 기반 익명 조인           |
           |  ② 집계 쿼리 실행                  |
           |  ③ k-anonymity 임계값 적용          |
           |  ④ Differential Privacy 노이즈 추가 |
           +--------------+--------------------+
                          v
           +------------------------------------+
           |  집계 결과만 반환                   |
           |  예) "캠페인 전환율: 12%"            |
           |  원시 PII는 어느 쪽도 볼 수 없음      |
           +------------------------------------+
```

### 클린 룸 유형 비교

| 유형 | 예시 | 특징 |
|:---|:---|:---|
| 클라우드 기반 | AWS Clean Rooms, Google ADH | 관리형, 빠른 도입 |
| 독립 클린 룸 | InfoSum, Habu | 멀티클라우드, 중립 |
| [연합 학습](/studynote/14_data_engineering/05_exam_keywords/256_federated_learning_privacy_model_security/) | FL 기반 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 없이 모델 학습 |

📢 **섹션 요약 비유**: 클린 룸은 복면을 쓴 채로 의사를 보는 원격 진료실이다. 의사는 증상(집계 결과)만 보고 처방하며, 얼굴(PII)은 절대 보지 않는다.

## Ⅲ. 비교 및 연결

### [SMPC](/studynote/09_security/20_extra_exam_prep/1018_secure_multi_party_computation/) vs [Differential Privacy](/studynote/09_security/16_data_privacy/817_differential_privacy/)

| 항목 | [SMPC](/studynote/09_security/20_extra_exam_prep/1018_secure_multi_party_computation/) | [Differential Privacy](/studynote/09_security/16_data_privacy/817_differential_privacy/) |
|:---|:---|:---|
| 원리 | 암호화 상태로 공동 계산 | 결과에 통계적 노이즈 추가 |
| 정확도 | 정확 (노이즈 없음) | 근사치 (ε에 따라 오차) |
| 계산 비용 | 매우 높음 | 낮음 |
| 적합 상황 | 소규모 정밀 분석 | 대규모 통계 분석 |

📢 **섹션 요약 비유**: SMPC는 귓속말로 정확한 비밀을 나누는 것, DP는 소음이 가득한 공간에서 대화하여 [도청](/studynote/03_network/14_network_security_threats/701_sniffing_eavesdropping_promiscuous/)자가 내용을 알아듣지 못하게 하는 것이다.

## Ⅳ. 실무 적용 및 기술사 판단

### 클린 룸 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

- [ ] 양사 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 법적 근거 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) ([GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/) 제6조, [개인정보보호법](/studynote/09_security/16_data_privacy/783_pipa_korea/) 제15조)
- [ ] [해시 함수](/studynote/03_network/13_network_security_basics/667_hash_function_integrity_one_way/) 표준 합의 (SHA-256 + [salt](/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/) 권장)
- [ ] [k-anonymity](/studynote/14_data_engineering/04_mlops/185_k_anonymity_masking_data_pipeline/) 임계값 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) (최소 그룹 크기 50명 이상 권장)
- [ ] 프라이버시 예산(ε) [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 및 소진 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링
- [ ] [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 유지 (규제 대응)

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

| [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/) | 문제 | 해결 방법 |
|:---|:---|:---|
| 집계 결과에서 개인 역추적 | 소규모 그룹 -> PII 노출 | [k-anonymity](/studynote/14_data_engineering/04_mlops/185_k_anonymity_masking_data_pipeline/) 임계값 강제 |
| 무한 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 허용 | DP 예산 소진 -> 프라이버시 붕괴 | [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 횟수·유형 제한 |

📢 **섹션 요약 비유**: 프라이버시 예산은 통장 잔고다. [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 날릴 때마다 잔고가 줄어들고, 다 쓰면 더 이상 조회할 수 없다.

## Ⅴ. 기대효과 및 결론

| 항목 | 클린 룸 미사용 | 클린 룸 사용 |
|:---|:---|:---|
| [데이터 공유](/studynote/05_database/06_dw_olap_trends/386_data_clean_room_sharing/) 법적 [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) | 높음 (직접 PII 공유) | 낮음 (집계만 노출) |
| 캠페인 측정 정확도 | 불가 ([쿠키](/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/) 폐기) | 가능 ([1st party](/studynote/12_it_management/05_security_compliance/928_cdp_first_party/) [해시 조인](/studynote/05_database/03_relational_model/174_hash_join/)) |
| 규제 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 대비 | 취약 | [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·DP [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)으로 대응 |

📢 **섹션 요약 비유**: 클린 룸은 두 나라가 국경 근처 중립지대에서 정보를 교환하는 외교 채널이다. 서로의 영토(원시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))엔 들어가지 않고도 협업할 수 있다.

### 📌 관련 개념 맵

| 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Clean Room | 핵심 플랫폼 | 프라이버시 보존 협업 환경 |
| [Differential Privacy](/studynote/09_security/16_data_privacy/817_differential_privacy/) | [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 기술 | ε 예산 기반 노이즈 추가 |
| [SMPC](/studynote/09_security/20_extra_exam_prep/1018_secure_multi_party_computation/) | [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 기술 | 암호화 상태 공동 계산 |
| [k-anonymity](/studynote/14_data_engineering/04_mlops/185_k_anonymity_masking_data_pipeline/) | [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 기준 | 최소 그룹 크기 보장 |
| Privacy Budget | 제어 매개변수 | DP [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 횟수 한도 |

### 📈 관련 키워드 및 발전 흐름도

```
쿠키 기반 광고 타겟팅 (서드파티 데이터)
    |
    v
개인정보 규제 강화 (GDPR, 쿠키리스 시대)
    |
    v
Data Clean Room - 원시 데이터 비공개 협업 분석
    |
    v
MPC/차분 프라이버시/동형암호 프라이버시 기술 통합
    |
    v
Snowflake/Google Ads DCR 플랫폼 상용화
```

> **키워드**: [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Clean Room, Privacy-Preserving Analytics, MPC, [Differential Privacy](/studynote/09_security/16_data_privacy/817_differential_privacy/), Cookieless, First-Party [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)

### 👶 어린이를 위한 3줄 비유 설명

1. 클린 룸은 두 친구가 서로의 일기를 직접 보여주지 않고, 공통 내용만 알려주는 비밀 규칙이에요.
2. Differential Privacy는 답을 알려줄 때 일부러 살짝 틀린 숫자를 섞어서 진짜 정보를 감추는 거예요.
3. k-anonymity는 50명 이상이 같은 그룹일 때만 결과를 알려줘서, 특정 한 사람을 골라낼 수 없게 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 305 / 482

<- **이전**: [304. 실시간 CDP 아키텍처 1st Party 클릭 로그 수집 통합 (Real-time CDP Architecture)](/studynote/07_enterprise_systems/05_data_bi/304_realtime_cdp_architecture/)
**다음**: [306. 데이터 거버넌스 3요소 원칙 조직 프로세스 IT시스템 (Data Governance)](/studynote/07_enterprise_systems/05_data_bi/306_data_governance_3_elements/) ->

---
