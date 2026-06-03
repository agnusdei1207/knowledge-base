+++
title = "045. 데이터 패브릭 — Data Fabric"
date = 2026-04-05

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

> **핵심 인사이트**
> 1. [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)([Data Fabric](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/))은 이기종 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소스를 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)와 AI로 통합·자동화하는 아키텍처 패러다임 — [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)([Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/))가 조직·[도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 중심의 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)이라면, [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)은 기술 자동화 중심의 통합으로 두 접근법은 상호 보완적이다.
> 2. [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)의 핵심은 "지능형 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 레이어" — 능동 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)([Active](/knowledge-base/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) [Metadata](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/))가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계보(Lineage), 품질, 접근 패턴을 자동 학습하여 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 발견·통합·관리를 자동화하는 것이 기존 [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/)와의 핵심 차별점이다.
> 3. Gartner는 2022년 [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)을 탑 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리 트렌드로 선정 — 기업 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 조직의 75%가 2026년까지 [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/) 도입을 검토할 것으로 예측하며, IBM, Microsoft, Informatica 등이 주요 벤더다.

---

## Ⅰ. [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/) 개념



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">데이터 패브릭 (Data Fabric):</div>
<div class="kb-diagram-note">정의:</div>
<div class="kb-diagram-note">이기종 데이터 소스·플랫폼을</div>
<div class="kb-diagram-note">메타데이터·AI로 자동 통합하는</div>
<div class="kb-diagram-note">통합 데이터 관리 아키텍처</div>
<div class="kb-diagram-note">배경:</div>
<div class="kb-diagram-note">데이터 사일로 (Data Silo):</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">HR DB</div><div class="kb-diagram-cell">CRM DB</div><div class="kb-diagram-cell">IoT</div><div class="kb-diagram-cell">S3 레이크</div><div class="kb-diagram-cell">ERP</div></div>
<div class="kb-diagram-note">→ 각각 분리, 연결 어려움</div>
<div class="kb-diagram-note">데이터 엔지니어: 각 연결 수동 구축</div>
<div class="kb-diagram-note">→ 파이프라인 수백 개 → 유지보수 지옥</div>
<div class="kb-diagram-note">데이터 패브릭 접근:</div>
<div class="kb-diagram-note">메타데이터 레이어:</div>
<div class="kb-diagram-note">모든 데이터 소스 → 메타데이터 수집</div>
<div class="kb-diagram-note">→ 자동 관계 발견, 계보 추적</div>
<div class="kb-diagram-note">AI 추천:</div>
<div class="kb-diagram-note">"이 쿼리에 필요한 데이터가 여기 있습니다"</div>
<div class="kb-diagram-note">"이 파이프라인과 저 파이프라인은 같은 소스"</div>
<div class="kb-diagram-note">특성:</div>
<div class="kb-diagram-note">자동화 우선 (Automation First)</div>
<div class="kb-diagram-note">어디서든 연결 (Universal Connectivity)</div>
<div class="kb-diagram-note">지능적 발견 (Intelligent Discovery)</div>
<div class="kb-diagram-note">데이터 패브릭 vs 데이터 메시:</div>
<div class="kb-diagram-note">패브릭: 기술 자동화 중심</div>
<div class="kb-diagram-note">메시: 조직 도메인 중심</div>
<div class="kb-diagram-note">공통: 분산 데이터 문제 해결</div>
<div class="kb-diagram-note">→ 상호 보완 가능 (메시 + 패브릭)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)은 스마트 번역기 — 각나라 말([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소스)을 자동으로 이해하고 연결. [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)(언어 사전)가 AI로 학습해 자동 통역!

---

## Ⅱ. 능동 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">능동 메타데이터 (Active Metadata):</div>
<div class="kb-diagram-note">전통 메타데이터 (Passive):</div>
<div class="kb-diagram-note">기술 메타데이터: 스키마, 데이터 타입</div>
<div class="kb-diagram-note">비즈니스 메타데이터: 설명, 소유자</div>
<div class="kb-diagram-note">수동 업데이트, 검색만 가능</div>
<div class="kb-diagram-note">능동 메타데이터 (Active):</div>
<div class="kb-diagram-note">학습:</div>
<div class="kb-diagram-tree-item" style="--depth:1">데이터 사용 패턴 관찰</div>
<div class="kb-diagram-tree-item" style="--depth:1">쿼리 이력 분석</div>
<div class="kb-diagram-tree-item" style="--depth:1">데이터 품질 측정 자동화</div>
<div class="kb-diagram-note">행동:</div>
<div class="kb-diagram-tree-item" style="--depth:1">관련 데이터셋 자동 추천</div>
<div class="kb-diagram-tree-item" style="--depth:1">데이터 품질 이슈 자동 알림</div>
<div class="kb-diagram-tree-item" style="--depth:1">잠재적 보안 위반 감지</div>
<div class="kb-diagram-note">예:</div>
<div class="kb-diagram-note">사용자가 "매출" 검색</div>
<div class="kb-diagram-note">→ AI: "매출 테이블과 함께 자주 사용되는:</div>
<div class="kb-diagram-note">제품 테이블, 지역 테이블 추천"</div>
<div class="kb-diagram-note">데이터 계보 (Data Lineage):</div>
<div class="kb-diagram-note">데이터가 어디서 왔는지 자동 추적</div>
<div class="kb-diagram-note">Source DB → ETL → Data Lake → Report</div>
<div class="kb-diagram-note">영향 분석:</div>
<div class="kb-diagram-note">"Source DB의 컬럼 변경 시</div>
<div class="kb-diagram-note">어떤 리포트가 영향 받나?" → 자동 계산</div>
<div class="kb-diagram-note">컴플라이언스:</div>
<div class="kb-diagram-note">GDPR: "이 개인정보는 어디서 왔나?"</div>
<div class="kb-diagram-note">→ 계보로 자동 증명</div>
<div class="kb-diagram-note">메타데이터 그래프:</div>
<div class="kb-diagram-note">지식 그래프 (Knowledge Graph) 형태</div>
<div class="kb-diagram-note">개체 (테이블, 컬럼, 파이프라인)</div>
<div class="kb-diagram-note">관계 (변환, 참조, 파생)</div>
<div class="kb-diagram-note">→ 복잡한 데이터 관계 시각화</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 능동 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 사서 — 도서관 책([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))에 대한 기록([메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/))을 AI가 자동 업데이트. "이 책 보면 저 책도 봐요" 자동 추천!

---

## Ⅲ. [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/) 기술 구성

```
데이터 패브릭 기술 아키텍처:

계층 1 — 연결 (Connectivity):
  다양한 소스 커넥터
  - 관계형 DB (Oracle, SQL Server)
  - 클라우드 스토리지 (S3, ADLS)
  - SaaS API (Salesforce, Workday)
  - 스트리밍 (Kafka)
  - 온프레미스 + 멀티클라우드

계층 2 — 메타데이터 관리:
  데이터 카탈로그 (Data Catalog)
  데이터 계보 (Lineage)
  데이터 품질 프로파일링
  
  도구: Informatica Axon, IBM Watson Knowledge Catalog

계층 3 — 통합 (Integration):
  ETL/ELT 오케스트레이션
  데이터 가상화 (Data Virtualization)
    → 물리적 이동 없이 쿼리
  API 레이어

계층 4 — 거버넌스:
  접근 제어 (RBAC, ABAC)
  데이터 마스킹
  GDPR/CCPA 컴플라이언스

계층 5 — AI/ML 추천:
  관련 데이터셋 추천
  이상 데이터 자동 감지
  메타데이터 자동 태깅

주요 벤더:
  IBM Cloud Pak for Data
  Informatica Intelligent Data Management Cloud
  Microsoft Purview
  Talend Data Fabric
  Denodo (데이터 가상화 특화)
```

> 📢 **섹션 요약 비유**: [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/) 아키텍처는 스마트 물류 센터 — 여러 공급처(소스)에서 물건([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) 받아 자동 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)([메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)), [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 추천 경로(통합), 보안 관리(거버넌스)!

---

## Ⅳ. [데이터 가상화](/knowledge-base/studynote/05_database/06_dw_olap_trends/360_data_virtualization/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">데이터 가상화 (Data Virtualization):</div>
<div class="kb-diagram-note">데이터 패브릭의 핵심 구현 기술 중 하나</div>
<div class="kb-diagram-note">개념:</div>
<div class="kb-diagram-note">물리적으로 데이터를 이동하지 않고</div>
<div class="kb-diagram-note">마치 하나의 통합 뷰처럼 쿼리</div>
<div class="kb-diagram-note">비유:</div>
<div class="kb-diagram-note">여러 은행 계좌를 앱 하나로 조회</div>
<div class="kb-diagram-note">→ 실제 돈은 각 은행에 있지만</div>
<div class="kb-diagram-note">→ 잔액은 앱에서 통합 표시</div>
<div class="kb-diagram-note">구조:</div>
<div class="kb-diagram-note">가상화 레이어 (Logical Layer):</div>
<div class="kb-diagram-note">모든 소스를 단일 엔드포인트로 노출</div>
<div class="kb-diagram-note">SQL 인터페이스</div>
<div class="kb-diagram-note">소스들:</div>
<div class="kb-diagram-note">Oracle DB ←→</div>
<div class="kb-diagram-note">S3 Data Lake ←→ 가상화 레이어 → 사용자</div>
<div class="kb-diagram-note">Salesforce API ←→</div>
<div class="kb-diagram-note">장점:</div>
<div class="kb-diagram-note">데이터 중복 없음 (저장 비용 절감)</div>
<div class="kb-diagram-note">실시간 소스 데이터 접근</div>
<div class="kb-diagram-note">ETL 파이프라인 단순화</div>
<div class="kb-diagram-note">단점:</div>
<div class="kb-diagram-note">소스 DB 부하 (직접 쿼리)</div>
<div class="kb-diagram-note">네트워크 지연</div>
<div class="kb-diagram-note">복잡한 쿼리 성능 저하</div>
<div class="kb-diagram-note">도구:</div>
<div class="kb-diagram-note">Denodo Platform</div>
<div class="kb-diagram-note">IBM Db2 Big SQL</div>
<div class="kb-diagram-note">Dremio (Apache Arrow 기반)</div>
<div class="kb-diagram-note">Starburst (Trino 기반)</div>
<div class="kb-diagram-note">활용:</div>
<div class="kb-diagram-note">사용 빈도 낮은 히스토리 데이터</div>
<div class="kb-diagram-note">실시간 소스가 중요한 경우</div>
<div class="kb-diagram-note">ETL 구축 이전 빠른 프로토타입</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [데이터 가상화](/knowledge-base/studynote/05_database/06_dw_olap_trends/360_data_virtualization/)는 통합 은행 앱 — 여러 은행(소스) 계좌를 앱([가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/))으로 한 번에 조회. 실제 돈([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))은 각 은행에, 잔액 표시만 통합!

---

## Ⅴ. 실무 시나리오 — 금융그룹 [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">대형 금융그룹 데이터 패브릭 구축:</div>
<div class="kb-diagram-note">배경:</div>
<div class="kb-diagram-note">은행·증권·보험 3개 계열사</div>
<div class="kb-diagram-note">각자 데이터 플랫폼 (사일로)</div>
<div class="kb-diagram-note">고객 360도 뷰 불가</div>
<div class="kb-diagram-note">마케팅팀: "고객 데이터 통합해줘" → 수개월 대기</div>
<div class="kb-diagram-note">문제:</div>
<div class="kb-diagram-note">수동 데이터 요청 → 데이터팀 병목</div>
<div class="kb-diagram-note">데이터 파이프라인 300개 운영 (중복 다수)</div>
<div class="kb-diagram-note">계열사 간 고객 식별 불일치 (동명이인 처리)</div>
<div class="kb-diagram-note">데이터 패브릭 구축:</div>
<div class="kb-diagram-note">1. 메타데이터 통합:</div>
<div class="kb-diagram-note">Microsoft Purview 도입</div>
<div class="kb-diagram-note">3개 계열사 DB 스캔 → 메타데이터 자동 수집</div>
<div class="kb-diagram-note">데이터 계보 자동 구축</div>
<div class="kb-diagram-note">2. 데이터 가상화:</div>
<div class="kb-diagram-note">Starburst (Trino 기반) 도입</div>
<div class="kb-diagram-note">SQL 한 번으로 3개 계열사 조회</div>
<div class="kb-diagram-note">SELECT c.name, b.balance, s.portfolio_value</div>
<div class="kb-diagram-note">FROM bank.customers c</div>
<div class="kb-diagram-note">JOIN securities.accounts s ON c.ssn = s.ssn</div>
<div class="kb-diagram-note">JOIN insurance.policies i ON c.ssn = i.ssn</div>
<div class="kb-diagram-note">3. AI 메타데이터:</div>
<div class="kb-diagram-note">고객 ID 매핑 AI 자동화</div>
<div class="kb-diagram-note">유사 데이터셋 자동 추천</div>
<div class="kb-diagram-note">품질 이슈 자동 알림</div>
<div class="kb-diagram-note">결과 (1년):</div>
<div class="kb-diagram-note">데이터 요청 처리 시간: 3개월 → 3일</div>
<div class="kb-diagram-note">데이터 파이프라인: 300개 → 150개 (중복 제거)</div>
<div class="kb-diagram-note">고객 360도 뷰 달성 (3계열사 통합)</div>
<div class="kb-diagram-note">마케팅 캠페인 대상 정확도: +35%</div>
<div class="kb-diagram-note">데이터 관련 컴플라이언스 위반: 0건 (계보 추적)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 금융 [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)은 가족 통합 다이어리 — 은행·증권·보험(3형제)이 각자 쓰던 일기(DB)를 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 비서(패브릭)가 자동 통합해서 가족 전체 상황(고객 360도) 한눈에!

---

## 📌 관련 개념 맵

```
데이터 패브릭
+-- 핵심 기술
|   +-- 능동 메타데이터
|   +-- 데이터 카탈로그
|   +-- 데이터 가상화
|   +-- AI/ML 추천
+-- 비교
|   +-- 데이터 메시 (조직 중심)
|   +-- 데이터 레이크 (중앙 저장)
+-- 벤더
|   +-- IBM Cloud Pak for Data
|   +-- Informatica IDMC
|   +-- Microsoft Purview
|   +-- Denodo, Starburst
+-- 적용
    +-- 데이터 계보 (GDPR)
    +-- 고객 360도
    +-- 멀티클라우드 통합
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[데이터 통합 레거시 (2000s)]
ETL 수동 구축
마스터 데이터 관리 (MDM)
      |
      v
[데이터 가상화 (2010s)]
Denodo, Composite Software
물리적 이동 없는 통합
      |
      v
[Gartner 데이터 패브릭 명명 (2019)]
메타데이터 중심 통합
AI 자동화 추가
      |
      v
[현재: AI 주도 패브릭 (2022~)]
능동 메타데이터 성숙
LLM 기반 자연어 데이터 질의
데이터 메시 + 패브릭 융합
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. [데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)은 스마트 도서관 — 여러 도서관(DB)의 책([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 사서([메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/))가 자동으로 목록 만들고, "이 책 찾으면 저 책도 봐요" 추천!
2. [데이터 가상화](/knowledge-base/studynote/05_database/06_dw_olap_trends/360_data_virtualization/)는 통합 앱 — 여러 은행 계좌를 하나의 앱으로! 실제 돈은 각 은행에 있지만 앱에서 통합 조회.
3. [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/) vs 패브릭 — [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)는 "각 팀이 자기 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리", 패브릭은 "AI가 자동 통합". 둘 다 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 문제 해결, 방법이 달라요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 257 / 262

← **이전**: [044. 데이터 메시 — Data Mesh](/knowledge-base/studynote/16_bigdata/13_intro_trends/256_data_mesh/)
**다음**: [046. 데이터 레이크하우스 — Data Lakehouse](/knowledge-base/studynote/16_bigdata/13_intro_trends/258_data_lakehouse/) →

---
