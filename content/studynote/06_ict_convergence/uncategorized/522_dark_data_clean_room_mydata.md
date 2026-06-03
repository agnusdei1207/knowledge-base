---
title: 522. 다크 데이터, 클린 룸, 마이데이터 (Dark Data Clean Room MyData)
date: '2026-05-09'
tags:
- studynote-ict-convergence
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[062_darkdata|다크 데이터]]([[062_darkdata|Dark Data]])는 수집됐으나 활용되지 않는 [[001_dikw_pyramid|데이터]](전체의 80%+)이며, [[001_dikw_pyramid|데이터]] 클린 룸([[305_data_clean_room|Data Clean Room]])은 원시 [[001_dikw_pyramid|데이터]] 미공유 상태에서 두 기업이 집계 분석을 교환하고, [[012_mydata|마이데이터]]([[266_mydata_open_api_token_security|MyData]])는 개인이 자신의 [[001_dikw_pyramid|데이터]] 통제권을 직접 행사하는 제도다.
> 2. **가치**: 세 개념은 각각 "잠든 [[001_dikw_pyramid|데이터]] 깨우기 → 안전한 협업 분석 → 개인 주권 [[233_recovery_database_restoration_overview|회복]]"이라는 [[001_dikw_pyramid|데이터]] 활용 패러다임의 연속 진화를 나타낸다.
> 3. **판단 포인트**: 기술사 논술에서 [[783_pipa_korea|개인정보보호법]]·[[791_gdpr_eu|GDPR]] 컴플라이언스와 [[001_dikw_pyramid|데이터]] 활용 가치 사이의 트레이드오프, 그리고 클린 룸의 기술적 구현([[396_differential_privacy|차분 프라이버시]], 집계 임계값)을 핵심 근거로 제시한다.

---

## Ⅰ. 개요 및 필요성

IDC 조사에 따르면 기업이 보유한 [[001_dikw_pyramid|데이터]]의 **80% 이상이 [[062_darkdata|다크 데이터]]([[062_darkdata|Dark Data]])**로 [[104_classification_analysis|분류]]된다. 수집은 했지만 분석·활용되지 않아 저장 비용만 발생하는 [[001_dikw_pyramid|데이터]]다. 반면 [[001_dikw_pyramid|데이터]]를 무작정 공유하면 [[781_personal_information|개인정보]] 침해와 규제 위반 리스크가 따른다.

이 딜레마를 해결하기 위해 등장한 것이 **[[001_dikw_pyramid|데이터]] 클린 룸([[305_data_clean_room|Data Clean Room]])**이다. 동시에 **[[012_mydata|마이데이터]]([[266_mydata_open_api_token_security|MyData]])** 제도는 개인이 금융·의료·통신 [[001_dikw_pyramid|데이터]]의 이동과 활용을 직접 결정하도록 권한을 부여한다.

- **📢 섹션 요약 비유**: 창고에 쌓인 물건([[062_darkdata|다크 데이터]])을 꺼내 쓰려면 두 창고가 서로 목록만 교환하는 공동 열람실(클린 룸)을 만들거나, 물건 주인(개인)이 직접 열쇠를 쥐는([[012_mydata|마이데이터]]) 방법이 필요하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[001_dikw_pyramid|데이터]] 클린 룸 구조

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

| 구분 | [[062_darkdata|다크 데이터]] | [[001_dikw_pyramid|데이터]] 클린 룸 | [[012_mydata|마이데이터]] |
|:---|:---|:---|:---|
| 주체 | 기업([[001_dikw_pyramid|데이터]] 보유자) | 기업 간(협업 분석) | 개인([[809_data_sovereignty|데이터 주권]]자) |
| 핵심 과제 | [[104_classification_analysis|분류]]·활용 [[268_strategy_pattern|전략]] 수립 | 원시 [[001_dikw_pyramid|데이터]] 비노출 집계 | 개인 동의 기반 이동권 |
| 주요 기술 | [[213_data_catalog_metadata|데이터 카탈로그]], 태깅 | [[396_differential_privacy|차분 프라이버시]], [[185_k_anonymity_masking_data_pipeline|k-익명성]] | [[014_api_posix|API]] 표준([[266_mydata_open_api_token_security|MyData]] [[014_api_posix|API]]), OAuth2 |
| 주요 사례 | [[568_logs_distributed_logging_elk_fluentd|로그]] [[501_file_definition_logical_record|파일]], 이메일 아카이브 | Google Ads [[180_data_hub|Data Hub]], AWS Clean Rooms | 금융 [[012_mydata|마이데이터]](뱅크샐러드), 의료 PHR |

[[396_differential_privacy|차분 프라이버시]]([[817_differential_privacy|Differential Privacy]])는 클린 룸 [[298_qkv_attention|쿼리]] 결과에 수학적 노이즈를 추가해 개별 레코드 역추적을 방지하며, [[185_k_anonymity_masking_data_pipeline|k-익명성]]은 집계 결과에 최소 k개 레코드가 포함되도록 임계값을 강제한다.

- **📢 섹션 요약 비유**: 클린 룸은 두 요리사가 서로 레시피를 공개하지 않고 "우리 재료로 만든 요리가 몇 그릇 팔렸나"만 공유하는 공동 회계 장부다.

---

## Ⅲ. 비교 및 연결

| 비교 축 | 클린 룸 | [[012_mydata|마이데이터]] |
|:---|:---|:---|
| [[001_dikw_pyramid|데이터]] 소유 관점 | 기업 간 협의 | 개인 주권 |
| 법적 근거 | NDA + 집계 계약 | [[783_pipa_korea|개인정보보호법]] 제35조(열람권), 전송요구권 |
| [[791_gdpr_eu|GDPR]] 연계 | [[001_dikw_pyramid|데이터]] 최소화 원칙 준수 | 정보주체 권리([[621_art_android_runtime|Art]]. 20 이동권) |
| 적용 시나리오 | 광고 매칭, 공동 리타게팅 | 본인 금융 [[001_dikw_pyramid|데이터]] 타 [[090_service_kubernetes_network_load_balancing|서비스]] 이동 |

[[062_darkdata|다크 데이터]]와 클린 룸은 연결된다. 기업이 [[062_darkdata|다크 데이터]]를 [[104_classification_analysis|분류]]하면 클린 룸을 통해 외부 파트너와 가치를 교환할 수 있다. [[012_mydata|마이데이터]]는 이 생태계에 개인이 참여자로 진입하는 경로다.

- **📢 섹션 요약 비유**: [[062_darkdata|다크 데이터]]는 창고 속 먼지 쌓인 보물, 클린 룸은 보물 목록만 보여주는 유리 전시장, [[012_mydata|마이데이터]]는 보물 주인이 직접 열쇠를 쥐는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**국내 [[012_mydata|마이데이터]] 현황**: 2022년 금융 [[012_mydata|마이데이터]] 본격 시행. 은행·카드·보험 [[001_dikw_pyramid|데이터]]를 본인 동의 하에 제3자 플랫폼(뱅크샐러드, 토스)으로 전송. 2024년 의료 [[012_mydata|마이데이터]](PHR, Personal Health Record) 시범 확대.

**[[062_darkdata|다크 데이터]] 관리 [[268_strategy_pattern|전략]]**:
1. [[213_data_catalog_metadata|데이터 카탈로그]]([[213_data_catalog_metadata|Data Catalog]]) 구축 → 태깅·[[104_classification_analysis|분류]]
2. ROT(Redundant, Obsolete, Trivial) [[001_dikw_pyramid|데이터]] [[655_ir_detection_analysis|식별]] 및 삭제
3. 잠재 가치 [[001_dikw_pyramid|데이터]]는 [[146_lakehouse|레이크하우스]]([[146_lakehouse|Lakehouse]])에 보관

**기술사 판단**: 클린 룸 도입 시 집계 임계값(최소 50건 이상 등)과 [[298_qkv_attention|쿼리]] 횟수 제한을 계약에 명시하여 모자이크 공격(여러 [[298_qkv_attention|쿼리]] 조합으로 개인 [[655_ir_detection_analysis|식별]])을 방지해야 한다.

- **📢 섹션 요약 비유**: 은행이 고객 동의 없이 [[001_dikw_pyramid|데이터]]를 팔면 범죄지만, 고객이 직접 허락하고 목록만 보여주면 합법 비즈니스가 된다—제도와 기술이 함께 맞물려야 한다.

---

## Ⅴ. 기대효과 및 결론

[[062_darkdata|다크 데이터]] 활용은 기업의 숨겨진 인사이트 발굴과 스토리지 비용 절감을 동시에 달성한다. [[001_dikw_pyramid|데이터]] 클린 룸은 경쟁사 간에도 프라이버시를 지키며 협업 분석을 가능하게 한다. [[012_mydata|마이데이터]]는 개인 [[809_data_sovereignty|데이터 주권]] 확립과 함께 핀테크·헬스케어 생태계의 혁신을 가속한다.

세 패러다임의 공통 방향은 **"[[001_dikw_pyramid|데이터]]를 더 많이 쓰되, 프라이버시를 더 철저히 지킨다"**는 역설적 목표를 기술로 실현하는 것이다.

- **📢 섹션 요약 비유**: 잠자는 [[001_dikw_pyramid|데이터]]를 깨워 안전하게 활용하는 것은, 도서관 책을 빌려주되 복사는 못 하게 하는 규칙처럼—규칙(법)과 기술(클린 룸)이 함께 있어야 가능하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[062_darkdata|Dark Data]] | ROT [[001_dikw_pyramid|데이터]], [[213_data_catalog_metadata|데이터 카탈로그]], 스토리지 최적화 |
| [[305_data_clean_room|Data Clean Room]] | [[396_differential_privacy|차분 프라이버시]], [[185_k_anonymity_masking_data_pipeline|k-익명성]], AWS Clean Rooms |
| [[266_mydata_open_api_token_security|MyData]] | 전송요구권, PHR, [[012_mydata|마이데이터]] [[014_api_posix|API]], OAuth2 |
| [[791_gdpr_eu|GDPR]] | [[621_art_android_runtime|Art]].20 이동권, [[001_dikw_pyramid|데이터]] 최소화, 동의 관리 |
| [[783_pipa_korea|개인정보보호법]] | 열람권(35조), 삭제권, 가명처리 |

### 📈 관련 키워드 및 발전 흐름도

```text
[ROT 데이터 · 데이터 카탈로그] → [다크 데이터 · 클린 룸] → [열람권 · 삭제권]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[062_darkdata|다크 데이터]]는 장난감 상자에 있지만 꺼내지 않아 잊혀진 장난감이에요.
2. [[001_dikw_pyramid|데이터]] 클린 룸은 친구와 각자 장난감 이름만 알려주고 함께 노는 규칙이에요.
3. [[012_mydata|마이데이터]]는 내 장난감 열쇠를 내가 직접 갖고, 누구에게 빌려줄지 내가 정하는 거예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 522 / 552

← **이전**: [[521_homomorphic_encryption_post_quantum_crypto|521. 동형 암호와 양자 내성 암호 전환 (Homomorphic Encryption Post-Quantum Cryptography)]]
**다음**: [[523_dataops_feature_flag_citizen_developer|523. DataOps, 피처 플래그, 시민 개발자 노코드 (DataOps Feature Flag Citizen Developer No-Code)]] →

---
