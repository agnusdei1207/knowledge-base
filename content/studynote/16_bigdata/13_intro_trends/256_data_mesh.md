+++
title = "044. 데이터 메시 — Data Mesh"
date = 2026-04-05

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

> **핵심 인사이트**
> 1. [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)([Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/))는 Zhamak Dehghani(2019)가 제안한 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터 아키텍처](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 패러다임으로 — 중앙집중식 [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)/[데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)의 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 병목([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Bottleneck](/knowledge-base/studynote/02_operating_system/10_security/617_io_bottleneck/))"을 해결하기 위해 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀이 직접 [데이터 제품](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/)([Data Product](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/))을 소유·운영하는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터 거버넌스](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/) 모델이다.
> 2. [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)의 4대 원칙은 — [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소유권([Domain](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) Ownership), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 제품으로([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a Product), 셀프서비스 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼(Self-Serve [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Platform), 연합 컴퓨팅 거버넌스(Federated Computational Governance)로 구성되며, 이 네 가지의 균형이 구현 성패를 결정한다.
> 3. [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)는 조직 변화(Conway의 법칙: 시스템 구조 = 팀 구조)를 전제하므로 — 기술 도입보다 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어링 역량을 갖추는 조직 변화가 더 어렵고 핵심적이며, 이를 무시한 [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/) 도입은 "[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 카오스"를 초래한다.

---

## Ⅰ. [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/) 탄생 배경



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">데이터 메시 탄생 배경:</div>
<div class="kb-diagram-note">중앙집중식 데이터 아키텍처의 문제:</div>
<div class="kb-diagram-note">데이터 레이크/웨어하우스 → 중앙 데이터팀 관리</div>
<div class="kb-diagram-note">문제점:</div>
<div class="kb-diagram-note">1. 병목 (Bottleneck):</div>
<div class="kb-diagram-note">모든 데이터 요청 → 중앙 데이터팀 경유</div>
<div class="kb-diagram-note">우선순위 경쟁, 대기 시간 증가</div>
<div class="kb-diagram-note">2. 컨텍스트 손실:</div>
<div class="kb-diagram-note">도메인 팀이 데이터 의미를 알지만</div>
<div class="kb-diagram-note">중앙팀은 맥락 없이 파이프라인만 구축</div>
<div class="kb-diagram-note">→ 데이터 품질 저하, 오용 증가</div>
<div class="kb-diagram-note">3. 확장성 한계:</div>
<div class="kb-diagram-note">데이터 소스/소비 증가 → 중앙팀 과부하</div>
<div class="kb-diagram-note">4. 오너십 부재:</div>
<div class="kb-diagram-note">중앙팀: "파이프라인만 책임"</div>
<div class="kb-diagram-note">도메인팀: "데이터 품질 아웃소싱"</div>
<div class="kb-diagram-note">→ 책임 공백</div>
<div class="kb-diagram-note">데이터 메시 제안:</div>
<div class="kb-diagram-note">2019년 Zhamak Dehghani (ThoughtWorks)</div>
<div class="kb-diagram-note">"How to Move Beyond a Monolithic Data Lake"</div>
<div class="kb-diagram-note">핵심 아이디어:</div>
<div class="kb-diagram-note">도메인 팀이 데이터를 직접 소유·운영</div>
<div class="kb-diagram-note">= 마이크로서비스 아키텍처의 데이터 버전</div>
<div class="kb-diagram-note">MSA와 데이터 메시 비교:</div>
<div class="kb-diagram-note">MSA: 도메인별 독립 서비스, API로 소통</div>
<div class="kb-diagram-note">데이터 메시: 도메인별 독립 데이터 제품, 표준 인터페이스</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)는 동네 빵집 → [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 베이커리 — 중앙 공장([데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/))에서 모든 빵을 굽는 대신, 각 동네([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀)가 자기 빵을 굽고 표준 진열대(플랫폼)에 올려요.

---

## Ⅱ. 4대 원칙



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">데이터 메시 4대 원칙:</div>
<div class="kb-diagram-note">1. 도메인 데이터 소유권 (Domain Ownership):</div>
<div class="kb-diagram-note">데이터 소비에서 소스 지향적(Source-Oriented) 소유권으로</div>
<div class="kb-diagram-note">"주문 데이터" → 주문 도메인 팀이 소유·운영</div>
<div class="kb-diagram-note">"고객 데이터" → 고객 도메인 팀이 소유·운영</div>
<div class="kb-diagram-note">도메인 팀 책임:</div>
<div class="kb-diagram-tree-item" style="--depth:1">데이터 품질 보장</div>
<div class="kb-diagram-tree-item" style="--depth:1">파이프라인 운영</div>
<div class="kb-diagram-tree-item" style="--depth:1">문서화 및 메타데이터 관리</div>
<div class="kb-diagram-note">2. 데이터를 제품으로 (Data as a Product):</div>
<div class="kb-diagram-note">데이터는 고품질 제품 = 사용성·신뢰성·접근성 필요</div>
<div class="kb-diagram-note">데이터 제품 속성:</div>
<div class="kb-diagram-tree-item" style="--depth:1">Discoverable: 검색 가능</div>
<div class="kb-diagram-tree-item" style="--depth:1">Addressable: 명확한 주소 (URL/URN)</div>
<div class="kb-diagram-tree-item" style="--depth:1">Trustworthy: 품질 SLA 보장</div>
<div class="kb-diagram-tree-item" style="--depth:1">Self-describing: 스키마, 문서 포함</div>
<div class="kb-diagram-tree-item" style="--depth:1">Interoperable: 표준 형식</div>
<div class="kb-diagram-tree-item" style="--depth:1">Secure: 접근 제어</div>
<div class="kb-diagram-note">예: "주문 이력 데이터 제품"</div>
<div class="kb-diagram-note">URL: data://orders.company.com/order-history/v2</div>
<div class="kb-diagram-note">SLA: 신선도 1시간, 가용성 99.9%</div>
<div class="kb-diagram-note">3. 셀프서비스 데이터 플랫폼:</div>
<div class="kb-diagram-note">도메인 팀이 스스로 데이터 제품 구축 가능한 인프라</div>
<div class="kb-diagram-note">플랫폼 제공 기능:</div>
<div class="kb-diagram-tree-item" style="--depth:1">저장소 (S3, BigQuery)</div>
<div class="kb-diagram-tree-item" style="--depth:1">처리 (Spark, Flink)</div>
<div class="kb-diagram-tree-item" style="--depth:1">오케스트레이션 (Airflow)</div>
<div class="kb-diagram-tree-item" style="--depth:1">카탈로그 (Datahub, Amundsen)</div>
<div class="kb-diagram-tree-item" style="--depth:1">모니터링 (Great Expectations)</div>
<div class="kb-diagram-note">4. 연합 컴퓨팅 거버넌스:</div>
<div class="kb-diagram-note">중앙 정책 + 도메인 자율성 균형</div>
<div class="kb-diagram-note">중앙 정의: 데이터 형식 표준, 보안 정책, 개인정보 처리</div>
<div class="kb-diagram-note">도메인 자율: 구현 방법, 도구 선택, 내부 스키마</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 4대 원칙은 도시 계획 — 각 건물([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/))은 스스로 설계하되, 도시(플랫폼)는 도로 표준(거버넌스)을 제공. 자율성과 표준의 균형.

---

## Ⅲ. [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/) vs [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">데이터 메시 vs 데이터 레이크 비교:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">항목</div><div class="kb-diagram-cell">데이터 레이크</div><div class="kb-diagram-cell">데이터 메시</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">소유권</div><div class="kb-diagram-cell">중앙 데이터팀</div><div class="kb-diagram-cell">도메인 팀</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">아키텍처</div><div class="kb-diagram-cell">중앙집중</div><div class="kb-diagram-cell">분산</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">데이터 제공 방식</div><div class="kb-diagram-cell">파이프라인</div><div class="kb-diagram-cell">데이터 제품</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">거버넌스</div><div class="kb-diagram-cell">중앙 통제</div><div class="kb-diagram-cell">연합 (분산+표준)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">확장 방식</div><div class="kb-diagram-cell">팀 확장</div><div class="kb-diagram-cell">도메인 확장</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">강점</div><div class="kb-diagram-cell">단순, 초기 비용</div><div class="kb-diagram-cell">확장성, 자율성</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">약점</div><div class="kb-diagram-cell">병목, 컨텍스트 손실</div><div class="kb-diagram-cell">조직 변화 필요</div></div>
<div class="kb-diagram-note">데이터 메시 도입 적합:</div>
<div class="kb-diagram-note">조직 규모: 100+ 엔지니어</div>
<div class="kb-diagram-note">도메인: 5+ 명확한 비즈니스 도메인</div>
<div class="kb-diagram-note">성숙도: 각 도메인 팀이 데이터 엔지 역량 보유</div>
<div class="kb-diagram-note">데이터 레이크 적합:</div>
<div class="kb-diagram-note">소규모 조직 (50명 이하)</div>
<div class="kb-diagram-note">단일 도메인 중심</div>
<div class="kb-diagram-note">데이터 팀 집중 필요</div>
<div class="kb-diagram-note">Conway의 법칙:</div>
<div class="kb-diagram-note">"시스템 설계는 그것을 만든 조직의 커뮤니케이션 구조를 반영"</div>
<div class="kb-diagram-note">데이터 메시: 조직이 먼저, 기술이 다음</div>
<div class="kb-diagram-note">도메인 팀 역량 없이 데이터 메시 도입 → 실패</div>
<div class="kb-diagram-note">실패 사례:</div>
<div class="kb-diagram-note">"데이터 메시 플랫폼 구축 완료"</div>
<div class="kb-diagram-note">→ 도메인 팀은 여전히 중앙 데이터팀 의존</div>
<div class="kb-diagram-note">→ 분산 데이터 카오스 발생</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/) vs 레이크는 중앙 수돗물 vs 개인 우물 — [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 모든 집에 중앙 수돗물 공급, [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)는 각 집이 우물([데이터 제품](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/))을 파되 수질 기준(거버넌스)은 동일.

---

## Ⅳ. 구현 도구

```
데이터 메시 구현 도구:

데이터 카탈로그 (Data Catalog):
  DataHub (LinkedIn 오픈소스):
    데이터 제품 검색, 계보, 소유권
  Amundsen (Lyft 오픈소스)
  Collibra (상용)
  
  역할: 데이터 제품의 "전화번호부"
  사용자: "주문 데이터 어디 있어?" → 카탈로그 검색

데이터 제품 레지스트리:
  각 도메인이 자신의 데이터 제품 등록
  스키마, 소유자, SLA, 접근 방법

오케스트레이션:
  Apache Airflow: DAG 기반 파이프라인
  Prefect, Dagster: 더 현대적인 대안
  
  각 도메인 팀이 자신의 파이프라인 소유

스토리지:
  도메인별 독립 스토리지 (S3 버킷, BigQuery 데이터셋)
  
  공통 형식: Parquet, Delta Lake, Apache Iceberg
  (상호운용성을 위한 표준 형식)

연합 거버넌스 도구:
  Open Policy Agent (OPA): 정책을 코드로
  Apache Atlas: 메타데이터 거버넌스
  dbt: 데이터 변환 + 문서화 통합

실제 구현 예시 (3도메인):
  주문 도메인 팀:
    S3: s3://orders-domain/data-products/
    제품: order-history-v2, daily-order-summary-v1
    
  고객 도메인 팀:
    S3: s3://customer-domain/data-products/
    제품: customer-profile-v3, churn-risk-score-v1
    
  상품 도메인 팀:
    S3: s3://product-domain/data-products/
    제품: product-catalog-v2, inventory-snapshot-v1
    
  공통 플랫폼:
    DataHub: 전체 카탈로그
    Airflow: 도메인별 워크스페이스
    Great Expectations: 품질 표준
```

> 📢 **섹션 요약 비유**: [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/) 도구는 도시 인프라 — DataHub는 지도(어디 있는지), Airflow는 도로(어떻게 이동), S3는 창고(저장). [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀은 자기 건물([데이터 제품](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/))을 관리.

---

## Ⅴ. 실무 시나리오 — 글로벌 핀테크 [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">글로벌 핀테크 기업 데이터 메시 전환:</div>
<div class="kb-diagram-note">배경:</div>
<div class="kb-diagram-note">5개 비즈니스 도메인: 결제, 대출, 투자, 고객, 규제</div>
<div class="kb-diagram-note">문제: 중앙 데이터팀 9명이 400개 파이프라인 운영</div>
<div class="kb-diagram-note">현상: 새 파이프라인 요청 → 4주 대기</div>
<div class="kb-diagram-note">Phase 1 — 도메인 데이터 제품 정의:</div>
<div class="kb-diagram-note">결제 도메인:</div>
<div class="kb-diagram-note">데이터 제품: "실시간 트랜잭션" (Kafka), "일간 정산 요약" (Parquet)</div>
<div class="kb-diagram-note">소유자: 결제 팀 (데이터 엔지니어 2명 추가)</div>
<div class="kb-diagram-note">Phase 2 — 셀프서비스 플랫폼 구축:</div>
<div class="kb-diagram-note">중앙 플랫폼 팀: 인프라 자동화 제공</div>
<div class="kb-diagram-tree-item" style="--depth:1">Terraform 모듈: "데이터 제품 인프라 원클릭"</div>
<div class="kb-diagram-tree-item" style="--depth:1">Airflow 템플릿: 표준 파이프라인 패턴</div>
<div class="kb-diagram-tree-item" style="--depth:1">DataHub: 자동 등록</div>
<div class="kb-diagram-note">Phase 3 — 연합 거버넌스:</div>
<div class="kb-diagram-note">GDPR 데이터 마스킹: 플랫폼 레벨 자동 적용</div>
<div class="kb-diagram-note">스키마 레지스트리: Confluent Schema Registry</div>
<div class="kb-diagram-note">품질 기준: Great Expectations 공통 Suite</div>
<div class="kb-diagram-note">결과 (1년 후):</div>
<div class="kb-diagram-note">새 데이터 제품 출시: 4주 → 3일</div>
<div class="kb-diagram-note">데이터 품질 이슈: 70% 감소 (도메인 오너십)</div>
<div class="kb-diagram-note">중앙 데이터팀 의존도: 90% → 30%</div>
<div class="kb-diagram-note">데이터 제품 수: 45개 → 280개</div>
<div class="kb-diagram-note">교훈:</div>
<div class="kb-diagram-note">"도메인 팀 역량이 플랫폼보다 먼저"</div>
<div class="kb-diagram-note">처음 6개월: 팀 역량 교육에 투자</div>
<div class="kb-diagram-note">플랫폼 도구는 역량이 생긴 후 도입</div>
<div class="kb-diagram-note">실패 패턴: 플랫폼 먼저, 팀 역량 나중</div>
<div class="kb-diagram-note">→ 아무도 안 씀</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 핀테크 [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)는 공방 → [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 공방 전환 — 중앙 공방([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)팀) 9명이 400개 주문을 처리하다가, 각 동네 장인([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀)이 자기 제품을 만드는 구조로 변신!

---

## 📌 관련 개념 맵

```
데이터 메시 (Data Mesh)
+-- 4대 원칙
|   +-- 도메인 소유권
|   +-- 데이터를 제품으로
|   +-- 셀프서비스 플랫폼
|   +-- 연합 거버넌스
+-- 대비
|   +-- 데이터 레이크 (중앙집중)
|   +-- 데이터 패브릭 (자동화 통합)
+-- 도구
|   +-- DataHub, Amundsen (카탈로그)
|   +-- Apache Iceberg, Delta Lake (형식)
|   +-- Great Expectations (품질)
+-- 전제조건
|   +-- Conway의 법칙
|   +-- 도메인 팀 역량
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[데이터 웨어하우스 (1990s)]
중앙집중식 분석 데이터
ETL 파이프라인
      |
      v
[데이터 레이크 (2010s)]
Hadoop, S3 기반 대규모 저장
스키마 온 리드
      |
      v
[MSA + 데이터 문제 (2015~)]
서비스 분산화 → 데이터 여전히 중앙
데이터 병목 가속화
      |
      v
[데이터 메시 제안 (2019)]
Zhamak Dehghani: 4대 원칙
도메인 소유권 패러다임
      |
      v
[현재: 데이터 메시 vs 패브릭]
데이터 패브릭 (자동화 통합)과 경쟁
기업별 최적 아키텍처 선택
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 빵집 — 중앙 공장([데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)) 대신, 각 동네([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀)가 자기 빵([데이터 제품](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/))을 굽고 표준 진열대(플랫폼)에 올려요!
2. 4대 원칙 — 각 팀이 소유하고, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 제품처럼, 혼자서도 할 수 있는 플랫폼, 공통 규칙. 이 네 가지가 균형 잡혀야 [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)가 작동해요.
3. 조직 변화가 더 중요 — 도구(플랫폼)보다 각 팀의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 역량 키우기가 먼저. 역량 없이 도구만 도입하면 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 카오스!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 256 / 262

← **이전**: [043. 데이터 옵저버빌리티](/knowledge-base/studynote/16_bigdata/13_intro_trends/255_data_observability/)
**다음**: [045. 데이터 패브릭 — Data Fabric](/knowledge-base/studynote/16_bigdata/13_intro_trends/257_data_fabric/) →

---
