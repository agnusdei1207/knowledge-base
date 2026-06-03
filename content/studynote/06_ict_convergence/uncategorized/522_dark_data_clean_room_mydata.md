+++
title = "522. 다크 데이터, 클린 룸, 마이데이터 (Dark Data Clean Room MyData)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [다크 데이터](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/)([Dark Data](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/))는 수집됐으나 활용되지 않는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(전체의 80%+)이며, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 클린 룸([Data Clean Room](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/305_data_clean_room/))은 원시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 미공유 상태에서 두 기업이 집계 분석을 교환하고, [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/)([MyData](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/266_mydata_open_api_token_security/))는 개인이 자신의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통제권을 직접 행사하는 제도다.
> 2. **가치**: 세 개념은 각각 "잠든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 깨우기 → 안전한 협업 분석 → 개인 주권 [회복](/knowledge-base/studynote/05_database/04_transactions_concurrency/233_recovery_database_restoration_overview/)"이라는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 활용 패러다임의 연속 진화를 나타낸다.
> 3. **판단 포인트**: 기술사 논술에서 [개인정보보호법](/knowledge-base/studynote/09_security/16_data_privacy/783_pipa_korea/)·[GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) 컴플라이언스와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 활용 가치 사이의 트레이드오프, 그리고 클린 룸의 기술적 구현([차분 프라이버시](/knowledge-base/studynote/10_ai/05_data_science_ml/396_differential_privacy/), 집계 임계값)을 핵심 근거로 제시한다.

---

## Ⅰ. 개요 및 필요성

IDC 조사에 따르면 기업이 보유한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 **80% 이상이 [다크 데이터](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/)([Dark Data](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/))**로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)된다. 수집은 했지만 분석·활용되지 않아 저장 비용만 발생하는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)다. 반면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 무작정 공유하면 [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) 침해와 규제 위반 리스크가 따른다.

이 딜레마를 해결하기 위해 등장한 것이 **[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 클린 룸([Data Clean Room](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/305_data_clean_room/))**이다. 동시에 **[마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/)([MyData](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/266_mydata_open_api_token_security/))** 제도는 개인이 금융·의료·통신 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 이동과 활용을 직접 결정하도록 권한을 부여한다.

- **📢 섹션 요약 비유**: 창고에 쌓인 물건([다크 데이터](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/))을 꺼내 쓰려면 두 창고가 서로 목록만 교환하는 공동 열람실(클린 룸)을 만들거나, 물건 주인(개인)이 직접 열쇠를 쥐는([마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/)) 방법이 필요하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 클린 룸 구조

```
  기업 A (원시 데이터)          기업 B (원시 데이터)
        │                              │
        ▼                              ▼
  ┌─────────────────────────────────────────┐
  │            데이터 클린 룸               │
  │  ┌──────────┐      ┌──────────────┐    │
  │  │집계 엔진  │◄────►│ 쿼리 검증기  │    │
  │  │(k-익명성)│      │(임계값 적용) │    │
  │  └──────────┘      └──────────────┘    │
  │        │ 집계 결과만 반환               │
  └────────┼────────────────────────────────┘
           ▼
    공동 인사이트 (원시 데이터 미공유)
```

| 구분 | [다크 데이터](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 클린 룸 | [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/) |
|:---|:---|:---|:---|
| 주체 | 기업([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 보유자) | 기업 간(협업 분석) | 개인([데이터 주권](/knowledge-base/studynote/09_security/16_data_privacy/809_data_sovereignty/)자) |
| 핵심 과제 | [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)·활용 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 수립 | 원시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 비노출 집계 | 개인 동의 기반 이동권 |
| 주요 기술 | [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/), 태깅 | [차분 프라이버시](/knowledge-base/studynote/10_ai/05_data_science_ml/396_differential_privacy/), [k-익명성](/knowledge-base/studynote/14_data_engineering/04_mlops/185_k_anonymity_masking_data_pipeline/) | [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 표준([MyData](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/266_mydata_open_api_token_security/) [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/)), OAuth2 |
| 주요 사례 | [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/), 이메일 아카이브 | Google Ads [Data Hub](/knowledge-base/studynote/16_bigdata/09_platform/180_data_hub/), AWS Clean Rooms | 금융 [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/)(뱅크샐러드), 의료 PHR |

[차분 프라이버시](/knowledge-base/studynote/10_ai/05_data_science_ml/396_differential_privacy/)([Differential Privacy](/knowledge-base/studynote/09_security/16_data_privacy/817_differential_privacy/))는 클린 룸 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 결과에 수학적 노이즈를 추가해 개별 레코드 역추적을 방지하며, [k-익명성](/knowledge-base/studynote/14_data_engineering/04_mlops/185_k_anonymity_masking_data_pipeline/)은 집계 결과에 최소 k개 레코드가 포함되도록 임계값을 강제한다.

- **📢 섹션 요약 비유**: 클린 룸은 두 요리사가 서로 레시피를 공개하지 않고 "우리 재료로 만든 요리가 몇 그릇 팔렸나"만 공유하는 공동 회계 장부다.

---

## Ⅲ. 비교 및 연결

| 비교 축 | 클린 룸 | [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/) |
|:---|:---|:---|
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소유 관점 | 기업 간 협의 | 개인 주권 |
| 법적 근거 | NDA + 집계 계약 | [개인정보보호법](/knowledge-base/studynote/09_security/16_data_privacy/783_pipa_korea/) 제35조(열람권), 전송요구권 |
| [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) 연계 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 최소화 원칙 준수 | 정보주체 권리([Art](/knowledge-base/studynote/02_operating_system/10_security/621_art_android_runtime/). 20 이동권) |
| 적용 시나리오 | 광고 매칭, 공동 리타게팅 | 본인 금융 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 타 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 이동 |

[다크 데이터](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/)와 클린 룸은 연결된다. 기업이 [다크 데이터](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/)를 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하면 클린 룸을 통해 외부 파트너와 가치를 교환할 수 있다. [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/)는 이 생태계에 개인이 참여자로 진입하는 경로다.

- **📢 섹션 요약 비유**: [다크 데이터](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/)는 창고 속 먼지 쌓인 보물, 클린 룸은 보물 목록만 보여주는 유리 전시장, [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/)는 보물 주인이 직접 열쇠를 쥐는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**국내 [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/) 현황**: 2022년 금융 [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/) 본격 시행. 은행·카드·보험 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 본인 동의 하에 제3자 플랫폼(뱅크샐러드, 토스)으로 전송. 2024년 의료 [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/)(PHR, Personal Health Record) 시범 확대.

**[다크 데이터](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/) 관리 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)**:
1. [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)([Data Catalog](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)) 구축 → 태깅·[분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)
2. ROT(Redundant, Obsolete, Trivial) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 및 삭제
3. 잠재 가치 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/)([Lakehouse](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/))에 보관

**기술사 판단**: 클린 룸 도입 시 집계 임계값(최소 50건 이상 등)과 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 횟수 제한을 계약에 명시하여 모자이크 공격(여러 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 조합으로 개인 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/))을 방지해야 한다.

- **📢 섹션 요약 비유**: 은행이 고객 동의 없이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 팔면 범죄지만, 고객이 직접 허락하고 목록만 보여주면 합법 비즈니스가 된다—제도와 기술이 함께 맞물려야 한다.

---

## Ⅴ. 기대효과 및 결론

[다크 데이터](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/) 활용은 기업의 숨겨진 인사이트 발굴과 스토리지 비용 절감을 동시에 달성한다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 클린 룸은 경쟁사 간에도 프라이버시를 지키며 협업 분석을 가능하게 한다. [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/)는 개인 [데이터 주권](/knowledge-base/studynote/09_security/16_data_privacy/809_data_sovereignty/) 확립과 함께 핀테크·헬스케어 생태계의 혁신을 가속한다.

세 패러다임의 공통 방향은 **"[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 더 많이 쓰되, 프라이버시를 더 철저히 지킨다"**는 역설적 목표를 기술로 실현하는 것이다.

- **📢 섹션 요약 비유**: 잠자는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 깨워 안전하게 활용하는 것은, 도서관 책을 빌려주되 복사는 못 하게 하는 규칙처럼—규칙(법)과 기술(클린 룸)이 함께 있어야 가능하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [Dark Data](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/) | ROT [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/), 스토리지 최적화 |
| [Data Clean Room](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/305_data_clean_room/) | [차분 프라이버시](/knowledge-base/studynote/10_ai/05_data_science_ml/396_differential_privacy/), [k-익명성](/knowledge-base/studynote/14_data_engineering/04_mlops/185_k_anonymity_masking_data_pipeline/), AWS Clean Rooms |
| [MyData](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/266_mydata_open_api_token_security/) | 전송요구권, PHR, [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/) [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), OAuth2 |
| [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) | [Art](/knowledge-base/studynote/02_operating_system/10_security/621_art_android_runtime/).20 이동권, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 최소화, 동의 관리 |
| [개인정보보호법](/knowledge-base/studynote/09_security/16_data_privacy/783_pipa_korea/) | 열람권(35조), 삭제권, 가명처리 |

### 📈 관련 키워드 및 발전 흐름도

```text
[ROT 데이터 · 데이터 카탈로그] → [다크 데이터 · 클린 룸] → [열람권 · 삭제권]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [다크 데이터](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_darkdata/)는 장난감 상자에 있지만 꺼내지 않아 잊혀진 장난감이에요.
2. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 클린 룸은 친구와 각자 장난감 이름만 알려주고 함께 노는 규칙이에요.
3. [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/)는 내 장난감 열쇠를 내가 직접 갖고, 누구에게 빌려줄지 내가 정하는 거예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 522 / 552

← **이전**: [521. 동형 암호와 양자 내성 암호 전환 (Homomorphic Encryption Post-Quantum Cryptography)](/knowledge-base/studynote/06_ict_convergence/uncategorized/521_homomorphic_encryption_post_quantum_crypto/)
**다음**: [523. DataOps, 피처 플래그, 시민 개발자 노코드 (DataOps Feature Flag Citizen Developer No-Code)](/knowledge-base/studynote/06_ict_convergence/uncategorized/523_dataops_feature_flag_citizen_developer/) →

---
