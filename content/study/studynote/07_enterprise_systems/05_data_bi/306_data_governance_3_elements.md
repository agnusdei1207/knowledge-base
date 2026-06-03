+++
weight = 306
title = "306. 데이터 거버넌스 3요소 원칙 조직 프로세스 IT시스템 (Data Governance)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[052_data_governance_framework|데이터 거버넌스]]는 [[001_dikw_pyramid|데이터]]를 기업 자산으로 관리하는 원칙([[164_policy|정책]])·조직(역할)·프로세스+IT 시스템의 3요소 체계다.
> 2. **가치**: [[117_dama|DAMA]]-DMBOK ([[001_dikw_pyramid|Data]] [[372_management|Management]] Body of Knowledge) 기반 거버넌스 도입 기업은 [[001_dikw_pyramid|데이터]] 품질 인시던트 50~70% 감소와 규제 [[606_auditing_linux_auditd|감사]] 대응 시간 60% 단축을 경험한다.
> 3. **판단 포인트**: [[213_data_catalog_metadata|데이터 카탈로그]]([[012_metadata|메타데이터]])가 없으면 어떤 [[001_dikw_pyramid|데이터]]가 어디 있는지 모르는 "[[288_data_swamp_metadata_management_absence|데이터 늪]]([[288_data_swamp_metadata_management_absence|Data Swamp]])"이 되어 모든 거버넌스 활동이 무력화된다.

## Ⅰ. 개요 및 필요성

기업 [[001_dikw_pyramid|데이터]]가 급증하면서 "[[001_dikw_pyramid|데이터]]는 많은데 믿을 수 없다", "어디 있는지 모른다", "누가 책임자인지 모른다"는 문제가 만연해졌다.
[[052_data_governance_framework|데이터 거버넌스]]([[052_data_governance_framework|Data Governance]])는 [[001_dikw_pyramid|데이터]]의 [[452_availability|가용성]]·[[003_integrity|무결성]]·보안·[[286_usability_tactics|사용성]]을 확보하기 위한 [[164_policy|정책]], 조직, 프로세스, IT 시스템의 통합 프레임워크다.

국제 표준 [[117_dama|DAMA]]-DMBOK는 [[052_data_governance_framework|데이터 거버넌스]]를 11개 지식 영역의 중심에 위치시키며, 모든 [[001_dikw_pyramid|데이터]] 관리 활동의 방향을 결정하는 상위 프레임워크로 정의한다.

[[522_group_by|데이터 거버넌스 3요소]]:
1. **원칙(Principles)**: [[001_dikw_pyramid|데이터]] 품질 [[164_policy|정책]], [[007_security_policy|보안 정책]], [[808_data_classification|데이터 분류]] 기준
2. **조직(Organization)**: [[068_cdo_cio_role_separation_governance|CDO]] ([[068_cdo_cio_role_separation_governance|Chief Data Officer]]), [[067_data_steward_data_quality|Data Steward]], [[200_data_owner|Data Owner]], [[246_data_governance_council_operation|Data Governance Council]]
3. **프로세스+IT 시스템**: [[203_metadata_management|메타데이터 관리]], [[213_data_catalog_metadata|데이터 카탈로그]], [[001_dikw_pyramid|데이터]] 계보, 품질 측정

📢 **섹션 요약 비유**: [[052_data_governance_framework|데이터 거버넌스]]는 도서관 운영 체계다. 규칙(원칙), 사서(조직), 도서 [[104_classification_analysis|분류]] 시스템(프로세스+IT)이 갖춰져야 어떤 책이 어디 있는지 믿고 찾을 수 있다.

## Ⅱ. 아키텍처 및 핵심 원리

### 거버넌스 조직 구조

| 역할 | 책임 범위 | 주요 활동 |
|:---|:---|:---|
| [[068_cdo_cio_role_separation_governance|CDO]] ([[068_cdo_cio_role_separation_governance|Chief Data Officer]]) | 전사 [[001_dikw_pyramid|데이터]] [[268_strategy_pattern|전략]] | 거버넌스 [[164_policy|정책]] 승인, 이사회 보고 |
| [[246_data_governance_council_operation|Data Governance Council]] | 부서 간 의사결정 | [[164_policy|정책]] 심의, 분쟁 조정 |
| [[200_data_owner|Data Owner]] | 비즈니스 [[064_relation_domain|도메인]]별 소유 | [[001_dikw_pyramid|데이터]] 정의, 품질 기준 결정 |
| [[067_data_steward_data_quality|Data Steward]] | 실무 [[001_dikw_pyramid|데이터]] 관리 | [[012_metadata|메타데이터]] 유지, 품질 [[229_monitor|모니터]]링 |

### [[001_dikw_pyramid|데이터]] 품질 [[018_kpi|KPI]]

| [[018_kpi|KPI]] | 측정 방법 | 목표 기준 |
|:---|:---|:---|
| 완전성 (Completeness) | NULL 비율 | 핵심 필드 99% 이상 |
| [[002_bigdata_5v|정확성]] (Accuracy) | 원천 대비 오차율 | 오차 <0.1% |
| [[194_consistency_database_integrity|일관성]] ([[194_consistency_database_integrity|Consistency]]) | 시스템 간 동일 값 비율 | 99.5% 이상 |
| 적시성 (Timeliness) | [[001_dikw_pyramid|데이터]] [[141_latency|지연 시간]] | [[085_sla|SLA]] 내 갱신 95% 이상 |
| 유일성 (Uniqueness) | 중복 레코드 비율 | 중복 0.01% 이하 |

### [[103_ascii|ASCII]] 다이어그램: 거버넌스 3요소 + IT 지원 레이어

```
  ┌──────────────────────────────────────────────────────────────┐
  │               데이터 거버넌스 프레임워크                       │
  │                                                              │
  │  ① 원칙 (Principles)                                         │
  │  ┌─────────────────────────────────────────────────────────┐ │
  │  │ 데이터 분류 정책 │ 품질 기준 │ 보안 정책 │ 생명주기 정책  │ │
  │  └─────────────────────────────────────────────────────────┘ │
  │                           │                                  │
  │  ② 조직 (Organization)    ▼                                  │
  │  ┌─────────────────────────────────────────────────────────┐ │
  │  │  CDO → Governance Council → Data Owner → Data Steward  │ │
  │  └─────────────────────────────────────────────────────────┘ │
  │                           │                                  │
  │  ③ 프로세스 + IT 시스템   ▼                                  │
  │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌──────────┐  │
  │  │데이터 카탈로그│  │ 데이터 계보 │  │품질 모니터링│  │메타데이터│  │
  │  │(Atlas/   │  │(OpenLinea-│  │(dbt test/ │  │  관리    │  │
  │  │ Alation) │  │  ge)      │  │ GE)       │  │          │  │
  │  └───────────┘  └───────────┘  └───────────┘  └──────────┘  │
  └──────────────────────────────────────────────────────────────┘
```

### [[213_data_catalog_metadata|데이터 카탈로그]] 비교

| 제품 | 유형 | 주요 특징 |
|:---|:---|:---|
| Apache Atlas | [[191_oss_license_compliance|오픈소스]] | [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 생태계 연동, 자동 계보 |
| Alation | 상용 | ML 기반 자동 [[104_classification_analysis|분류]], 사용자 협업 |
| DataHub (LinkedIn) | [[191_oss_license_compliance|오픈소스]] | 실시간 [[012_metadata|메타데이터]] [[070_graph_datastructure|그래프]] |
| OpenMetadata | [[191_oss_license_compliance|오픈소스]] | All-in-one, 빠른 성장 |

📢 **섹션 요약 비유**: [[213_data_catalog_metadata|데이터 카탈로그]]는 도서관 목록 시스템이다. 책 제목([[001_dikw_pyramid|데이터]]명), 위치(저장소), 빌린 사람(사용자)을 기록해 누구나 원하는 [[001_dikw_pyramid|데이터]]를 찾을 수 있다.

## Ⅲ. 비교 및 연결

### [[117_dama|DAMA]]-DMBOK 11개 지식 영역 (핵심)

| 영역 | 핵심 내용 |
|:---|:---|
| [[052_data_governance_framework|데이터 거버넌스]] (중심) | 전체 관리 방향 결정 |
| [[104_da_as_is_analysis|데이터 아키텍처]] | 엔터프라이즈 [[014_data_model_components|데이터 모델]] |
| [[316_reference_pattern_nosql|참조]]·[[539_mdm_master_data_management|마스터 데이터]] | [[539_mdm_master_data_management|MDM]] (Master [[001_dikw_pyramid|Data]] [[372_management|Management]]) |
| [[001_dikw_pyramid|데이터]] 웨어하우징·BI | [[209_data_warehouse_schema_on_write|DW]], 분석 레이어 |
| [[203_metadata_management|메타데이터 관리]] | [[394_catalog_metadata|카탈로그]], 계보 |
| [[001_dikw_pyramid|데이터]] 품질 | [[018_kpi|KPI]], [[613_profiling_gprof|프로파일링]] |

📢 **섹션 요약 비유**: [[117_dama|DAMA]]-DMBOK는 [[001_dikw_pyramid|데이터]] 관리의 헌법이다. 11개 조항이 있고, [[052_data_governance_framework|데이터 거버넌스]]는 그 헌법의 전문(前文)이다.

## Ⅳ. 실무 적용 및 기술사 판단

### 거버넌스 도입 [[435_checklist_based_testing|체크리스트]]

- [ ] [[068_cdo_cio_role_separation_governance|CDO]] 또는 [[052_data_governance_framework|데이터 거버넌스]] 전담 조직 존재 여부
- [ ] 핵심 [[001_dikw_pyramid|데이터]] 자산 목록([[001_dikw_pyramid|Data]] Asset Inventory) 작성
- [ ] [[213_data_catalog_metadata|데이터 카탈로그]] 도구 도입 및 [[012_metadata|메타데이터]] 입력
- [ ] [[001_dikw_pyramid|데이터]] 품질 [[018_kpi|KPI]] 5가지 측정 자동화
- [ ] [[001_dikw_pyramid|데이터]] 계보(Lineage) 자동 수집 [[123_pipe|파이프]]라인 구축

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

| [[128_water_scrum_fall_anti_pattern|안티패턴]] | 문제 | 해결 방법 |
|:---|:---|:---|
| 거버넌스 규정 너무 엄격 | [[001_dikw_pyramid|데이터]] 민첩성 저하, 현업 반발 | 최소 필수 규정만 우선 적용 |
| [[394_catalog_metadata|카탈로그]]만 도입, [[012_metadata|메타데이터]] 미입력 | 빈 껍데기 도구 | [[012_metadata|메타데이터]] 입력 전담 Steward 지정 |

📢 **섹션 요약 비유**: 거버넌스 성숙도는 학생의 공부 습관 성장과 같다. 1단계는 시험 전날 벼락치기, 5단계는 매일 계획적으로 공부하며 스스로 취약점을 찾아 보완하는 수준이다.

## Ⅴ. 기대효과 및 결론

| 항목 | 거버넌스 미도입 | 도입 후 |
|:---|:---|:---|
| [[001_dikw_pyramid|데이터]] [[085_confidence_association_rule_conditional_probability|신뢰도]] | "이 수치 믿어도 되나?" | [[018_kpi|KPI]] 기반 품질 점수 공개 |
| [[001_dikw_pyramid|데이터]] [[324_seek_time|탐색 시간]] | 평균 4~8시간/건 | [[394_catalog_metadata|카탈로그]]로 15분 이내 |
| 규제 [[606_auditing_linux_auditd|감사]] 대응 | 수주~수개월 | 계보·[[012_metadata|메타데이터]]로 수일 |

📢 **섹션 요약 비유**: [[052_data_governance_framework|데이터 거버넌스]]는 교통 법규다. 규칙이 없으면 사고가 나지만, 규칙이 너무 많으면 아무도 차를 못 몬다. 적절한 균형이 핵심이다.

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---|:---|:---|
| [[068_cdo_cio_role_separation_governance|CDO]] | 조직 | [[068_cdo_cio_role_separation_governance|Chief Data Officer]], 거버넌스 총괄 |
| [[067_data_steward_data_quality|Data Steward]] | 조직 | 실무 [[012_metadata|메타데이터]]·품질 관리자 |
| [[213_data_catalog_metadata|Data Catalog]] | IT 시스템 | [[012_metadata|메타데이터]] 중앙 저장·검색 |
| [[117_dama|DAMA]]-DMBOK | 표준 프레임워크 | [[001_dikw_pyramid|데이터]] 관리 지식 체계 |
| [[539_mdm_master_data_management|MDM]] | 연관 영역 | [[539_mdm_master_data_management|마스터 데이터]] 단일 진실 원천 관리 |

### 📈 관련 키워드 및 발전 흐름도

```
데이터 품질 문제 인식 - 임시방편 대응
    │
    ▼
데이터 관리 정책 수립 (조직·프로세스·IT 3요소)
    │
    ▼
Data Catalog + Data Steward 체계화
    │
    ▼
DAMA-DMBOK 기반 거버넌스 성숙도 모델 적용
    │
    ▼
능동적 거버넌스 (Active Metadata + AI 자동화)
```

> **키워드**: [[052_data_governance_framework|Data Governance]], [[067_data_steward_data_quality|Data Steward]], [[213_data_catalog_metadata|Data Catalog]], [[068_cdo_cio_role_separation_governance|CDO]], [[117_dama|DAMA]]-DMBOK, [[539_mdm_master_data_management|MDM]], [[270_data_quality_great_expectations|Data Quality]], [[483_active_vs_passive_ftp|Active]] [[012_metadata|Metadata]]

### 👶 어린이를 위한 3줄 비유 설명

1. [[052_data_governance_framework|데이터 거버넌스]]는 도서관 운영 규칙이에요. 어떤 책이 어디 있는지, 누가 관리하는지, 빌리는 규칙은 뭔지 정해두는 거예요.
2. CDO는 도서관장이고, [[001_dikw_pyramid|Data]] Steward는 각 서가를 담당하는 사서예요.
3. [[213_data_catalog_metadata|데이터 카탈로그]]는 컴퓨터 검색 시스템이에요. 원하는 [[001_dikw_pyramid|데이터]]를 검색하면 어디 있는지, 누가 만들었는지 바로 알 수 있어요.
