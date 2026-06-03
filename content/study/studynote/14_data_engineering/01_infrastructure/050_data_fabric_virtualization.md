+++
title = "데이터 패브릭 가상화 (Data Fabric Virtualization)"
date = 2025-01-01
description = "데이터 패브릭의 개념, 데이터 가상화와의 차이, AI 기반 메타데이터 관리, 실시간 데이터 통합 아키텍처를 다룬다."
categories = "studynote-dataeng"
tags = ["data fabric", "data virtualization", "metadata", "data catalog", "AI-driven", "federated query", "data mesh"]
+++

> **핵심 인사이트 3줄**
> 1. [[212_data_fabric_virtualization|데이터 패브릭]]([[212_data_fabric_virtualization|Data Fabric]])은 [[136_variance|분산]]된 [[001_dikw_pyramid|데이터]] 소스를 물리적으로 이동하지 않고 단일 통합 레이어를 통해 접근할 수 있게 하는 아키텍처 패턴이다.
> 2. 핵심은 [[190_ai_llm_requirements_specification|AI]] 기반 [[203_metadata_management|메타데이터 관리]]로, [[213_data_catalog_metadata|데이터 카탈로그]]와 [[160_knowledge_graph_graphrag_integration|지식 그래프]]가 [[001_dikw_pyramid|데이터]] [[083_relationship_in_er_model|관계]]·계보·품질을 자동으로 발견·추천한다.
> 3. [[212_data_fabric_virtualization|데이터 패브릭]]은 [[211_data_mesh_domain_ownership|데이터 메시]]([[320_data_mesh|Data Mesh]])와 상호보완적으로, 패브릭은 기술 통합 레이어, [[389_mesh_topology|메시]]는 조직·소유권 [[136_variance|분산]] 원칙에 초점을 둔다.

---

## Ⅰ. [[212_data_fabric_virtualization|데이터 패브릭]] 개요

### 1.1 기존 문제와 패브릭 등장

```
기존:
  온프레미스 DW + 클라우드 DW + SaaS 앱 + 레거시 DB
      → 각각 별도 ETL, 중복 파이프라인
      → 데이터 사일로, 거버넌스 불일치

데이터 패브릭:
  [단일 통합 레이어 (메타데이터 + 가상화 + 거버넌스)]
      ↕      ↕      ↕      ↕
  온프레미스  클라우드  SaaS  레거시
```

### 1.2 핵심 구성 요소

| 구성 요소         | 역할                                          |
|----------------|----------------------------------------------|
| [[213_data_catalog_metadata|데이터 카탈로그]]  | [[012_metadata|메타데이터]] 수집·[[104_classification_analysis|분류]]·검색                     |
| [[160_knowledge_graph_graphrag_integration|지식 그래프]]      | [[001_dikw_pyramid|데이터]] [[083_relationship_in_er_model|관계]]·계보(lineage) [[003_bigdata_7v|시각화]]               |
| [[360_data_virtualization|데이터 가상화]]    | 물리 이동 없이 연합 [[298_qkv_attention|쿼리]] 실행                 |
| [[190_ai_llm_requirements_specification|AI]] 추천 엔진    | 사용 패턴 기반 [[001_dikw_pyramid|데이터]]셋 자동 추천              |
| 통합 거버넌스    | [[164_policy|정책]] 자동 적용 (마스킹, [[387_access_control_pattern|접근 통제]])            |

📢 **섹션 요약 비유**: [[212_data_fabric_virtualization|데이터 패브릭]]은 도서관 통합 검색 시스템 — 어느 서가(소스)에 있든 하나의 검색창으로 찾고, 없으면 즉시 빌려온다.

---

## Ⅱ. [[360_data_virtualization|데이터 가상화]] ([[247_data_virtualization_federated_query|Data Virtualization]])

### 2.1 [[015_virtualization|가상화]] vs [[016_replication_factor|복제]]

```
ETL 복제:
  소스 DB → (추출·변환·적재) → 중앙 DW
  장점: 빠른 쿼리  단점: 데이터 최신성 지연, 중복

데이터 가상화:
  쿼리 → 가상 레이어 → 각 소스에 실시간 위임
  장점: 최신 데이터, 중복 없음  단점: 소스 성능 의존
```

### 2.2 연합 [[298_qkv_attention|쿼리]] ([[195_federated_query_data_fabric_distributed_join|Federated Query]])

```sql
-- 가상 레이어에서 여러 소스를 단일 SQL로 조회
SELECT c.name, o.total
FROM virtual.crm.customers c        -- CRM 소스
JOIN virtual.erp.orders o            -- ERP 소스
ON c.id = o.customer_id
WHERE o.date >= '2024-01-01';
-- 실제로는 CRM DB + ERP DB에 각각 쿼리 위임 후 결합
```

📢 **섹션 요약 비유**: 연합 [[298_qkv_attention|쿼리]]는 배달 앱 — 여러 식당(소스)에 동시 주문하고 내 앞에 한 번에 모아놓는 것.

---

## Ⅲ. [[190_ai_llm_requirements_specification|AI]] 기반 [[203_metadata_management|메타데이터 관리]]

### 3.1 자동 [[012_metadata|메타데이터]] 발견

```
데이터 소스 연결
    ↓
AI 크롤러: 컬럼명, 데이터 타입, 값 분포 분석
    ↓
자동 분류: PII 탐지, 비즈니스 용어 매핑
    ↓
데이터 카탈로그 자동 업데이트
```

### 3.2 [[483_active_vs_passive_ftp|Active]] [[012_metadata|Metadata]]

기존 수동 [[012_metadata|메타데이터]] → [[483_active_vs_passive_ftp|Active]] [[012_metadata|Metadata]]:
- 실시간 사용 패턴 수집 (누가, 언제, 얼마나)
- 머신러닝으로 [[001_dikw_pyramid|데이터]] 품질 이슈 예측
- 자동 추천: "이 [[001_dikw_pyramid|데이터]]셋 쓰는 사람들은 X도 함께 씀"

**주요 플랫폼**: Alation, Collibra, Atlan, Apache Atlas

📢 **섹션 요약 비유**: [[483_active_vs_passive_ftp|Active]] Metadata는 넷플릭스 추천 알고리즘처럼 — [[001_dikw_pyramid|데이터]] 소비 패턴을 분석해 "이 [[001_dikw_pyramid|데이터]]를 보셨다면 이것도 필요할 것"을 제안.

---

## Ⅳ. [[212_data_fabric_virtualization|데이터 패브릭]] vs [[211_data_mesh_domain_ownership|데이터 메시]]

### 4.1 핵심 차이

| 관점      | [[212_data_fabric_virtualization|데이터 패브릭]]              | [[211_data_mesh_domain_ownership|데이터 메시]]              |
|---------|--------------------------|------------------------|
| 초점     | 기술 통합 레이어           | 조직·소유권 [[136_variance|분산]]         |
| 방식     | 중앙 통합 [[015_virtualization|가상화]] 레이어    | 도메인별 [[154_data_product|데이터 제품]] 자율 |
| [[190_ai_llm_requirements_specification|AI]] 활용  | 핵심 ([[012_metadata|메타데이터]] 자동화)   | 보조                    |
| 거버넌스 | 중앙 집중                  | 연합(Federated)         |

### 4.2 상호보완 아키텍처

```
데이터 메시 (도메인 소유권 분산)
    ↕
데이터 패브릭 (기술 통합 레이어)
→ 메시의 자율성 + 패브릭의 통합 가시성
```

📢 **섹션 요약 비유**: [[389_mesh_topology|메시]]는 각 팀이 자신의 가게를 운영, 패브릭은 모든 가게를 연결하는 배달 플랫폼 — 둘은 층이 다르다.

---

## Ⅴ. 구현 패턴과 플랫폼

### 5.1 [[316_reference_pattern_nosql|참조]] 아키텍처

```
[비즈니스 사용자]
      ↓ 단일 접근
[데이터 패브릭 레이어]
  ├── 카탈로그 (Collibra/Atlan)
  ├── 가상화 엔진 (Denodo/Dremio/Starburst)
  └── 거버넌스 정책 (Apache Ranger/Privacera)
      ↕         ↕         ↕
  [온프레미스]  [AWS]    [Azure/GCP]
```

### 5.2 주요 플랫폼 비교

| 플랫폼       | 특징                                     |
|-----------|------------------------------------------|
| Denodo    | 엔터프라이즈 [[360_data_virtualization|데이터 가상화]] 선두            |
| Dremio    | [[191_oss_license_compliance|오픈소스]] 기반, Apache Arrow 최적화        |
| Starburst | Trino(Presto) 기반 연합 [[298_qkv_attention|쿼리]]             |
| IBM Watson | [[190_ai_llm_requirements_specification|AI]] 통합 [[212_data_fabric_virtualization|데이터 패브릭]]                    |

📢 **섹션 요약 비유**: [[015_virtualization|가상화]] 엔진은 번역기 — 각기 다른 방언([[001_dikw_pyramid|데이터]] 소스)을 하나의 공통 언어(SQL)로 통역해준다.

---

## 📌 관련 개념 맵

```
데이터 패브릭
├── 핵심 기술
│   ├── 데이터 가상화 (Denodo, Dremio)
│   ├── 데이터 카탈로그 (Alation, Collibra)
│   └── Active Metadata (AI 기반)
├── 관련 패턴
│   ├── 데이터 메시 (보완 관계)
│   ├── 데이터 레이크하우스
│   └── 연합 쿼리
└── 거버넌스
    ├── 중앙 집중 정책
    └── Apache Ranger / Privacera
```

---

## 📈 관련 키워드 및 발전 흐름도

```
ETL + 중앙 DW (1990s~2000s)
     │  다중 소스·클라우드 확산
     ▼
데이터 가상화 (2010s, EII/EAI)
     │  메타데이터 자동화 필요
     ▼
데이터 패브릭 (2019, Gartner 선정)
     │  조직 분산 필요
     ▼
데이터 메시 + 패브릭 하이브리드 (2021~)
     │  AI 기반 Active Metadata
     ▼
지능형 데이터 패브릭 (현재)
```

**핵심 키워드**: [[360_data_virtualization|데이터 가상화]], 연합 [[298_qkv_attention|쿼리]], [[483_active_vs_passive_ftp|Active]] [[012_metadata|Metadata]], [[213_data_catalog_metadata|데이터 카탈로그]], [[211_data_mesh_domain_ownership|데이터 메시]], Denodo, Starburst

---

## 👶 어린이를 위한 3줄 비유 설명

1. [[212_data_fabric_virtualization|데이터 패브릭]]은 도서관 통합 검색 시스템 — 어느 서가(클라우드)에 있어도 하나의 검색창으로 찾아줘.
2. [[360_data_virtualization|데이터 가상화]]는 음식 배달 앱처럼 — 각 식당(DB)에 있는 음식을 이동 없이 내 앞에 바로 가져와.
3. [[190_ai_llm_requirements_specification|AI]] [[012_metadata|메타데이터]]는 스마트 사서 — "이 [[001_dikw_pyramid|데이터]] 쓰는 사람은 저것도 필요해요"라고 자동으로 추천해줘.
