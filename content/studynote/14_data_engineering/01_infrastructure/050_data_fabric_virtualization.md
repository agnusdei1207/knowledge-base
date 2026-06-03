+++
title = "데이터 패브릭 가상화 (Data Fabric Virtualization)"
description = "데이터 패브릭의 개념, 데이터 가상화와의 차이, AI 기반 메타데이터 관리, 실시간 데이터 통합 아키텍처를 다룬다."
date = 2025-01-01

[taxonomies]
tags = ["AI-driven", "data catalog", "data fabric", "data mesh", "data virtualization", "federated query", "metadata", "studynote-dataeng"]

[extra]
tags = ["AI-driven", "data catalog", "data fabric", "data mesh", "data virtualization", "federated query", "metadata", "studynote-dataeng"]
+++

> **핵심 인사이트 3줄**
> 1. [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)([Data Fabric](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/))은 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소스를 물리적으로 이동하지 않고 단일 통합 레이어를 통해 접근할 수 있게 하는 아키텍처 패턴이다.
> 2. 핵심은 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [메타데이터 관리](/knowledge-base/studynote/16_bigdata/10_governance/203_metadata_management/)로, [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)와 [지식 그래프](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/)가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)·계보·품질을 자동으로 발견·추천한다.
> 3. [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)은 [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)([Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/))와 상호보완적으로, 패브릭은 기술 통합 레이어, [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)는 조직·소유권 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 원칙에 초점을 둔다.

---

## Ⅰ. [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/) 개요

### 1.1 기존 문제와 패브릭 등장



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">기존:</div>
<div class="kb-diagram-note">온프레미스 DW + 클라우드 DW + SaaS 앱 + 레거시 DB</div>
<div class="kb-diagram-note">→ 각각 별도 ETL, 중복 파이프라인</div>
<div class="kb-diagram-note">→ 데이터 사일로, 거버넌스 불일치</div>
<div class="kb-diagram-note">데이터 패브릭:</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">단일 통합 레이어 (메타데이터 + 가상화 + 거버넌스)</div></div>
<div class="kb-diagram-note">↕ ↕ ↕ ↕</div>
<div class="kb-diagram-note">온프레미스 클라우드 SaaS 레거시</div>
</div>
</div>



### 1.2 핵심 구성 요소

| 구성 요소         | 역할                                          |
|----------------|----------------------------------------------|
| [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)  | [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 수집·[분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)·검색                     |
| [지식 그래프](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/)      | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)·계보(lineage) [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)               |
| [데이터 가상화](/knowledge-base/studynote/05_database/06_dw_olap_trends/360_data_virtualization/)    | 물리 이동 없이 연합 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 실행                 |
| [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 추천 엔진    | 사용 패턴 기반 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋 자동 추천              |
| 통합 거버넌스    | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 자동 적용 (마스킹, [접근 통제](/knowledge-base/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/))            |

📢 **섹션 요약 비유**: [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)은 도서관 통합 검색 시스템 — 어느 서가(소스)에 있든 하나의 검색창으로 찾고, 없으면 즉시 빌려온다.

---

## Ⅱ. [데이터 가상화](/knowledge-base/studynote/05_database/06_dw_olap_trends/360_data_virtualization/) ([Data Virtualization](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/247_data_virtualization_federated_query/))

### 2.1 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) vs [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">ETL 복제:</div>
<div class="kb-diagram-note">소스 DB → (추출·변환·적재) → 중앙 DW</div>
<div class="kb-diagram-note">장점: 빠른 쿼리 단점: 데이터 최신성 지연, 중복</div>
<div class="kb-diagram-note">데이터 가상화:</div>
<div class="kb-diagram-note">쿼리 → 가상 레이어 → 각 소스에 실시간 위임</div>
<div class="kb-diagram-note">장점: 최신 데이터, 중복 없음 단점: 소스 성능 의존</div>
</div>
</div>



### 2.2 연합 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) ([Federated Query](/knowledge-base/studynote/14_data_engineering/04_mlops/195_federated_query_data_fabric_distributed_join/))

```sql
-- 가상 레이어에서 여러 소스를 단일 SQL로 조회
SELECT c.name, o.total
FROM virtual.crm.customers c        -- CRM 소스
JOIN virtual.erp.orders o            -- ERP 소스
ON c.id = o.customer_id
WHERE o.date >= '2024-01-01';
-- 실제로는 CRM DB + ERP DB에 각각 쿼리 위임 후 결합
```

📢 **섹션 요약 비유**: 연합 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)는 배달 앱 — 여러 식당(소스)에 동시 주문하고 내 앞에 한 번에 모아놓는 것.

---

## Ⅲ. [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [메타데이터 관리](/knowledge-base/studynote/16_bigdata/10_governance/203_metadata_management/)

### 3.1 자동 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 발견



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">데이터 소스 연결</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">AI 크롤러: 컬럼명, 데이터 타입, 값 분포 분석</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">자동 분류: PII 탐지, 비즈니스 용어 매핑</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">데이터 카탈로그 자동 업데이트</div>
</div>
</div>



### 3.2 [Active](/knowledge-base/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) [Metadata](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)

기존 수동 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) → [Active](/knowledge-base/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) [Metadata](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/):
- 실시간 사용 패턴 수집 (누가, 언제, 얼마나)
- 머신러닝으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 이슈 예측
- 자동 추천: "이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋 쓰는 사람들은 X도 함께 씀"

**주요 플랫폼**: Alation, Collibra, Atlan, Apache Atlas

📢 **섹션 요약 비유**: [Active](/knowledge-base/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) Metadata는 넷플릭스 추천 알고리즘처럼 — [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소비 패턴을 분석해 "이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 보셨다면 이것도 필요할 것"을 제안.

---

## Ⅳ. [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/) vs [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)

### 4.1 핵심 차이

| 관점      | [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)              | [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)              |
|---------|--------------------------|------------------------|
| 초점     | 기술 통합 레이어           | 조직·소유권 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)         |
| 방식     | 중앙 통합 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 레이어    | 도메인별 [데이터 제품](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/) 자율 |
| [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 활용  | 핵심 ([메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 자동화)   | 보조                    |
| 거버넌스 | 중앙 집중                  | 연합(Federated)         |

### 4.2 상호보완 아키텍처

```
데이터 메시 (도메인 소유권 분산)
    ↕
데이터 패브릭 (기술 통합 레이어)
→ 메시의 자율성 + 패브릭의 통합 가시성
```

📢 **섹션 요약 비유**: [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)는 각 팀이 자신의 가게를 운영, 패브릭은 모든 가게를 연결하는 배달 플랫폼 — 둘은 층이 다르다.

---

## Ⅴ. 구현 패턴과 플랫폼

### 5.1 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 아키텍처



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">비즈니스 사용자</div></div>
<div class="kb-diagram-note">↓ 단일 접근</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">데이터 패브릭 레이어</div></div>
<div class="kb-diagram-tree-item" style="--depth:1">카탈로그 (Collibra/Atlan)</div>
<div class="kb-diagram-tree-item" style="--depth:1">가상화 엔진 (Denodo/Dremio/Starburst)</div>
<div class="kb-diagram-tree-item" style="--depth:1">거버넌스 정책 (Apache Ranger/Privacera)</div>
<div class="kb-diagram-note">↕ ↕ ↕</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">온프레미스</div><div class="kb-diagram-node">AWS</div><div class="kb-diagram-node">Azure/GCP</div></div>
</div>
</div>



### 5.2 주요 플랫폼 비교

| 플랫폼       | 특징                                     |
|-----------|------------------------------------------|
| Denodo    | 엔터프라이즈 [데이터 가상화](/knowledge-base/studynote/05_database/06_dw_olap_trends/360_data_virtualization/) 선두            |
| Dremio    | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 기반, Apache Arrow 최적화        |
| Starburst | Trino(Presto) 기반 연합 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)             |
| IBM Watson | [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 통합 [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)                    |

📢 **섹션 요약 비유**: [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 엔진은 번역기 — 각기 다른 방언([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소스)을 하나의 공통 언어(SQL)로 통역해준다.

---

## 📌 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">데이터 패브릭</div>
<div class="kb-diagram-tree-item" style="--depth:0">핵심 기술</div>
<div class="kb-diagram-note">── 데이터 가상화 (Denodo, Dremio)</div>
<div class="kb-diagram-note">── 데이터 카탈로그 (Alation, Collibra)</div>
<div class="kb-diagram-note">── Active Metadata (AI 기반)</div>
<div class="kb-diagram-tree-item" style="--depth:0">관련 패턴</div>
<div class="kb-diagram-note">── 데이터 메시 (보완 관계)</div>
<div class="kb-diagram-note">── 데이터 레이크하우스</div>
<div class="kb-diagram-note">── 연합 쿼리</div>
<div class="kb-diagram-tree-item" style="--depth:0">거버넌스</div>
<div class="kb-diagram-tree-item" style="--depth:2">중앙 집중 정책</div>
<div class="kb-diagram-tree-item" style="--depth:2">Apache Ranger / Privacera</div>
</div>
</div>



---

## 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">ETL + 중앙 DW (1990s~2000s)</div>
<div class="kb-diagram-note">다중 소스·클라우드 확산</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">데이터 가상화 (2010s, EII/EAI)</div>
<div class="kb-diagram-note">메타데이터 자동화 필요</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">데이터 패브릭 (2019, Gartner 선정)</div>
<div class="kb-diagram-note">조직 분산 필요</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">데이터 메시 + 패브릭 하이브리드 (2021~)</div>
<div class="kb-diagram-note">AI 기반 Active Metadata</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">지능형 데이터 패브릭 (현재)</div>
</div>
</div>



**핵심 키워드**: [데이터 가상화](/knowledge-base/studynote/05_database/06_dw_olap_trends/360_data_virtualization/), 연합 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/), [Active](/knowledge-base/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) [Metadata](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/), [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/), [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/), Denodo, Starburst

---

## 👶 어린이를 위한 3줄 비유 설명

1. [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)은 도서관 통합 검색 시스템 — 어느 서가(클라우드)에 있어도 하나의 검색창으로 찾아줘.
2. [데이터 가상화](/knowledge-base/studynote/05_database/06_dw_olap_trends/360_data_virtualization/)는 음식 배달 앱처럼 — 각 식당(DB)에 있는 음식을 이동 없이 내 앞에 바로 가져와.
3. [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)는 스마트 사서 — "이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 쓰는 사람은 저것도 필요해요"라고 자동으로 추천해줘.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 50 / 258

← **이전**: [049. 데이터 메시 — Data Mesh Distributed Ownership](/knowledge-base/studynote/14_data_engineering/01_infrastructure/049_data_mesh_distributed_ownership/)
**다음**: [51. 데이터 카탈로그 (Data Catalog) - 메타데이터 검색 및 자산화](/knowledge-base/studynote/14_data_engineering/01_infrastructure/051_data_catalog_metadata_discovery/) →

---
