+++
weight = 124
title = "124. 데이터 거버넌스 (Data Governance) - 데이터 품질·보안·표준의 전사 관리 체계"
date = "2026-04-19"
[extra]
categories = "studynote-database"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[052_data_governance_framework|데이터 거버넌스]]는 **[[001_dikw_pyramid|데이터]]의 [[452_availability|가용성]]·[[003_integrity|무결성]]·보안·품질을 보장하기 위한 [[164_policy|정책]]·프로세스·조직·기술의 통합 관리 체계**이며, [[001_dikw_pyramid|데이터]]를 기업 자산으로 관리하는 전사적 프레임워크다.
> 2. **가치**: 거버넌스 없이는 [[001_dikw_pyramid|데이터]] 중복·불일치·보안 사고·규제 위반이 발생하며, [[791_gdpr_eu|GDPR]]·[[783_pipa_korea|개인정보보호법]] 등 **규제 준수([[058_it_compliance_sox_basel_gdpr_isms|Compliance]])**를 위해서도 필수적이다.
> 3. **판단 포인트**: DAMA-DMBOK이 [[001_dikw_pyramid|데이터]] 관리 11개 영역을 정의하며, [[067_data_steward_data_quality|데이터 스튜어드]]([[067_data_steward_data_quality|Data Steward]])가 도메인별 [[001_dikw_pyramid|데이터]] 품질의 책임자 역할을 수행한다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    데이터 거버넌스 프레임워크                          │
├───────────────────────────────────────────────────────┤
│  [전략] 데이터 전략·비전·원칙                        │
│  [조직] CDO · 데이터 스튜어드 · 거버넌스 위원회      │
│  [정책] 데이터 표준·품질 규칙·보안 정책·접근 제어    │
│  [프로세스] 메타데이터 관리·MDM·품질 모니터링        │
│  [기술] 데이터 카탈로그·리니지 추적·DQ 도구          │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[052_data_governance_framework|데이터 거버넌스]]는 도시의 **도로교통법**이다. 차([[001_dikw_pyramid|데이터]])가 많아지면 법([[164_policy|정책]])·경찰(스튜어드)·신호등(기술)이 없으면 사고([[001_dikw_pyramid|데이터]] 오류)가 난다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### DAMA-DMBOK 11대 영역

| 영역 | 설명 |
|:---|:---|
| **[[052_data_governance_framework|데이터 거버넌스]]** | 전사 의사결정 체계 |
| **[[104_da_as_is_analysis|데이터 아키텍처]]** | [[014_data_model_components|데이터 모델]]·흐름 설계 |
| **[[014_data_model_components|데이터 모델]]링** | ERD·[[369_logic_bomb|논리]]/물리 모델 |
| **[[001_dikw_pyramid|데이터]] 품질** | [[002_bigdata_5v|정확성]]·완전성·[[194_consistency_database_integrity|일관성]] |
| **[[012_metadata|메타데이터]]** | [[001_dikw_pyramid|데이터]]에 대한 [[001_dikw_pyramid|데이터]] |
| **[[001_dikw_pyramid|데이터]] 보안** | 접근 제어·암호화 |

- **📢 섹션 요약 비유**: DAMA-DMBOK는 [[001_dikw_pyramid|데이터]] 관리의 **백과사전**이며, 거버넌스는 그 백과사전의 **총론** 챕터이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 거버넌스 없음 | 거버넌스 적용 |
|:---|:---|:---|
| **[[001_dikw_pyramid|데이터]] 품질** | 오류 빈발 | **정제·모니터링** |
| **규제 준수** | 위반 위험 | **[[791_gdpr_eu|GDPR]]·PIPA 준수** |
| **의사결정** | 불신 | **신뢰 가능 [[001_dikw_pyramid|데이터]]** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 거버넌스 도구
- **[[213_data_catalog_metadata|데이터 카탈로그]]**: DataHub, Amundsen.
- **[[214_data_lineage_tracking|데이터 리니지]]**: Apache Atlas, dbt lineage.
- **DQ 도구**: Great Expectations, Soda.

---

## Ⅴ. 기대효과 및 결론

[[052_data_governance_framework|데이터 거버넌스]]는 **[[001_dikw_pyramid|데이터]]를 기업의 [[268_strategy_pattern|전략]] 자산으로 관리**하는 체계이며, [[190_ai_llm_requirements_specification|AI]] 시대에 학습 [[001_dikw_pyramid|데이터]] 품질 보장·편향 방지를 위해 더욱 중요해지고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **DAMA-DMBOK** | [[001_dikw_pyramid|데이터]] 관리 표준 프레임워크 |
| **[[067_data_steward_data_quality|데이터 스튜어드]]** | 도메인별 [[001_dikw_pyramid|데이터]] 품질 책임자 |
| **[[539_mdm_master_data_management|MDM]]** | 거버넌스의 기술적 구현 |
| **[[213_data_catalog_metadata|데이터 카탈로그]]** | [[012_metadata|메타데이터]] 검색·관리 도구 |
| **[[214_data_lineage_tracking|데이터 리니지]]** | [[001_dikw_pyramid|데이터]] 흐름 추적 |

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 데이터 관리 (엑셀, 2000s)]
    │
    ▼
[DAMA-DMBOK 1판 (2009) — 데이터 관리 표준]
    │
    ▼
[데이터 거버넌스 솔루션 (Collibra, 2015~)]
    │
    ▼
[데이터 메시 (2020~) — 분산 거버넌스]
    │
    ▼
[현재: AI 거버넌스 — 모델·학습 데이터 품질 관리]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [[052_data_governance_framework|데이터 거버넌스]]는 도시의 **교통법규**예요. 차([[001_dikw_pyramid|데이터]])가 많으면 법이 필요해요.
2. **경찰([[067_data_steward_data_quality|데이터 스튜어드]])**이 교통([[001_dikw_pyramid|데이터]] 품질)을 관리하고, **신호등(기술 도구)**이 흐름을 조절해요.
3. 법규가 없으면 사고([[001_dikw_pyramid|데이터]] 오류)가 나서 **모두가 불편**해진답니다!
