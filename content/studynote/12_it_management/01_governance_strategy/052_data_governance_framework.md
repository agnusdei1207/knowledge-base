---
title: 52. 데이터 거버넌스 (Data Governance)
date: '2026-05-01'
tags:
- studynote-it-management
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[001_dikw_pyramid|데이터]] 거버넌스 ([[001_dikw_pyramid|Data]] Governance)는 [[001_dikw_pyramid|데이터]]의 품질, 보안, 표준, 책임을 전사적으로 다루는 운영 체계다.
> 2. **가치**: [[001_dikw_pyramid|데이터]] 오너 (Owner), [[067_data_steward_data_quality|데이터 스튜어드]] (Steward), [[001_dikw_pyramid|데이터]] 카운슬 (Council) 같은 역할을 명확히 해 [[001_dikw_pyramid|데이터]] 사일로와 책임 공백을 줄인다.
> 3. **판단 포인트**: 거버넌스는 도구만으로 성립하지 않는다. [[164_policy|정책]], 프로세스, [[012_metadata|메타데이터]], 품질 지표가 함께 있어야 한다.

---

## Ⅰ. 개요 및 필요성

[[001_dikw_pyramid|데이터]]가 조직의 핵심 자산이 되면서, 누가 어떤 기준으로 [[001_dikw_pyramid|데이터]]를 만들고 고치고 쓰는지 정해야 한다. [[001_dikw_pyramid|데이터]] 거버넌스는 이 기준을 조직적으로 정리하는 체계다. 단순한 DB 관리가 아니라, 경영과 현업이 함께 참여하는 [[001_dikw_pyramid|데이터]] 운영 규약이다.

이 체계가 필요한 이유는 [[001_dikw_pyramid|데이터]]가 여러 시스템으로 퍼지면서 의미가 달라지고 품질이 깨지기 때문이다. 특히 AI와 분석이 중요해질수록 잘못된 [[001_dikw_pyramid|데이터]]는 잘못된 의사결정으로 바로 연결된다.

- **📢 섹션 요약 비유**: [[001_dikw_pyramid|데이터]] 거버넌스는 학교 도서관의 [[104_classification_analysis|분류]] 규칙과 사서 역할을 정하는 일과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[001_dikw_pyramid|데이터]] 거버넌스는 조직, [[164_policy|정책]], 프로세스, 시스템의 네 축으로 돌아간다. 누가 책임지는지, 어떤 표준을 따를지, 문제가 나면 어떻게 고칠지, 어디서 상태를 볼지를 함께 정해야 한다.

```text
┌──────────────────────────────────────────────────────────────┐
│                 Data Governance Framework                    │
├──────────────────────────────────────────────────────────────┤
│ Strategy → Organization → Policy → Process → System          │
│                        │                                     │
│                        ▼                                     │
│               Data Quality / Metadata / Catalog              │
└──────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 예시 |
| :--- | :--- | :--- |
| [[200_data_owner|Data Owner]] | [[001_dikw_pyramid|데이터]]의 최종 책임 | 부서장, [[090_service_kubernetes_network_load_balancing|서비스]] 오너 |
| [[067_data_steward_data_quality|Data Steward]] | 품질과 표준 운영 | 현업 담당자 |
| [[001_dikw_pyramid|Data]] Council | [[164_policy|정책]] 결정 | 전사 위원회 |
| [[213_data_catalog_metadata|Data Catalog]] | 찾기와 이해 지원 | [[012_metadata|메타데이터]] 포털 |
| DQ Rule | 품질 규칙 | 완전성, [[002_bigdata_5v|정확성]], [[194_consistency_database_integrity|일관성]] |

핵심 원리는 "[[001_dikw_pyramid|데이터]]를 통제할 사람과, 통제할 기준과, 통제 결과를 볼 수 있는 구조"를 함께 만드는 것이다. 그래서 품질, 보안, 계보, 표준이 분리되지 않고 하나의 체계로 움직여야 한다.

- **📢 섹션 요약 비유**: [[001_dikw_pyramid|데이터]] 거버넌스는 도시의 교통 규칙, 신호등, 교통경찰, 도로 표지판을 한 번에 설계하는 일과 같다.

---

## Ⅲ. 비교 및 연결

[[001_dikw_pyramid|데이터]] 거버넌스는 [[001_dikw_pyramid|데이터]] 관리, [[001_dikw_pyramid|데이터]] 품질, [[539_mdm_master_data_management|MDM]] (Master [[001_dikw_pyramid|Data]] [[372_management|Management]]), [[213_data_catalog_metadata|데이터 카탈로그]]와 연결된다. 관리가 "[[001_dikw_pyramid|데이터]]를 어떻게 운영할지"라면, 거버넌스는 "누가 어떤 원칙으로 운영할지"를 정한다.

| 항목 | [[001_dikw_pyramid|데이터]] 거버넌스 | [[001_dikw_pyramid|데이터]] 관리 | [[001_dikw_pyramid|데이터]] 품질 |
| :--- | :--- | :--- | :--- |
| 초점 | 책임과 원칙 | 운영 | 품질 측정 |
| 질문 | 누가 결정하는가 | 어떻게 실행하는가 | 얼마나 좋은가 |
| 산출물 | [[164_policy|정책]], 역할, 표준 | 운영 절차 | 품질 지표 |

[[001_dikw_pyramid|데이터]] 거버넌스가 잘 되면 [[213_data_catalog_metadata|데이터 카탈로그]], 라인리지, [[539_mdm_master_data_management|마스터 데이터]], [[211_data_mesh_domain_ownership|데이터 메시]] 같은 기술과 조직 구조가 서로 맞물린다. 결국 거버넌스는 기술보다 조직 설계를 먼저 바꾸는 일이다.

- **📢 섹션 요약 비유**: 거버넌스는 건물의 설계도, [[001_dikw_pyramid|데이터]] 관리는 건물 관리, [[001_dikw_pyramid|데이터]] 품질은 매일 점검하는 안전 검사와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 작은 [[001_dikw_pyramid|데이터]]부터 시작해 기준을 잡는다. 중요한 도메인부터 오너와 스튜어드를 지정하고, 표준명, 품질 규칙, [[394_catalog_metadata|카탈로그]], 라인리지를 연결한다. 이후 KPI로 품질을 측정해야 한다.

### [[435_checklist_based_testing|체크리스트]]

1. [[001_dikw_pyramid|데이터]] 오너와 스튜어드가 지정되어 있는가?
2. 핵심 [[001_dikw_pyramid|데이터]] 표준과 용어가 합의되어 있는가?
3. 품질 지표를 자동 측정하는가?
4. [[012_metadata|메타데이터]]와 라인리지를 검색할 수 있는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 도구만 사고 역할은 정하지 않는 경우
- IT 부서만의 일로 몰아가는 경우
- 품질 문제가 나도 책임자를 모르는 경우

기술사 관점에서는 [[001_dikw_pyramid|데이터]] 거버넌스가 왜 필요한지보다, 어떻게 조직의 책임 구조와 품질 체계를 만드는지 설명하는 것이 중요하다. 특히 [[190_ai_llm_requirements_specification|AI]] 학습 [[001_dikw_pyramid|데이터]]와 규제 대응에서는 거버넌스가 곧 경쟁력이다.

- **📢 섹션 요약 비유**: [[001_dikw_pyramid|데이터]] 거버넌스는 도서관에서 책을 [[104_classification_analysis|분류]]하고, 누가 관리할지 정하고, 잘못 꽂힌 책을 바로잡는 규칙이다.

---

## Ⅴ. 기대효과 및 결론

[[001_dikw_pyramid|데이터]] 거버넌스는 신뢰할 수 있는 [[001_dikw_pyramid|데이터]]를 만드는 기반이다. [[001_dikw_pyramid|데이터]]를 잘 찾고, 의미를 이해하고, 책임을 나눌 수 있어야 분석과 AI가 제대로 작동한다.

즉 거버넌스는 [[001_dikw_pyramid|데이터]] 프로젝트의 바닥 공사다. 도구보다 먼저 조직과 기준을 세워야 오래 버틴다.

- **📢 섹션 요약 비유**: [[001_dikw_pyramid|데이터]] 거버넌스는 집을 짓기 전에 기초를 다지는 일이다. 기초가 흔들리면 아무리 멋진 집도 무너진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[200_data_owner|Data Owner]] | 책임자 |
| [[067_data_steward_data_quality|Data Steward]] | 운영 담당자 |
| [[213_data_catalog_metadata|Data Catalog]] | 검색/이해 지원 |
| [[214_data_lineage_tracking|Data Lineage]] | 출처와 흐름 추적 |
| [[539_mdm_master_data_management|MDM]] | 기준 [[001_dikw_pyramid|데이터]] 통합 |

### 📈 관련 키워드 및 발전 흐름도

```text
데이터 표준
    │
    ▼
Data Owner / Steward
    │
    ▼
품질 관리 (DQ)
    │
    ▼
메타데이터 / 카탈로그 / 라인리지
    │
    ▼
연합형 거버넌스 / 데이터 메시
```

이 흐름은 단순 규칙에서 운영 체계로, 다시 [[136_variance|분산]] 거버넌스로 확장되는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[001_dikw_pyramid|데이터]] 거버넌스는 책에 이름표를 붙이고, 누가 빌릴지 정하는 규칙이에요.
2. 규칙이 없으면 책이 어디 갔는지 모르고 다 섞여 버려요.
3. 규칙이 있으면 필요한 책을 빨리 찾을 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 94 / 587

← **이전**: [[052_data_governance|52. 데이터 거버넌스 (Data Governance)]]
**다음**: [[053_data_stewardship|53. 데이터 스튜어드십 (Data Stewardship)]] →

---
