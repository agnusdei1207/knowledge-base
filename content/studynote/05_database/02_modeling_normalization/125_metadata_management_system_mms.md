+++
title = "125. 메타데이터 관리 시스템 (MMS) - 데이터에 대한 데이터 관리"
date = 2026-04-19

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MMS([Metadata Management](/knowledge-base/studynote/16_bigdata/10_governance/203_metadata_management/) System)는 <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>의 정의·구조·형식·<a href="/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a>·출처·변환 규칙 등 '<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>에 대한 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>(<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/">메타데이터</a>)'를 체계적으로 수집·저장·검색·관리</strong>하는 시스템이다.
> 2. **가치**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 레이크에 수백만 테이블이 있어도 "이 컬럼이 무슨 뜻이고 어디서 왔는지" 모르면 활용이 불가능하며, MMS가 <strong><a href="/knowledge-base/studynote/05_database/07_exam_summary/393_data_dictionary/">데이터 사전</a>·리니지·검색 기능</strong>을 제공하여 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 활용도를 극대화한다.
> 3. **판단 포인트**: 기술 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)([스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)·타입)·비즈니스 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)(용어 정의·담당자)·운영 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)([ETL](/knowledge-base/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 이력·품질)를 구분하고, [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)가 현대적 MMS의 대표 형태이다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    메타데이터 유형                                    |
+-------------------------------------------------------+
|  [기술 메타데이터]   스키마·컬럼·타입·인덱스         |
|  [비즈니스 메타데이터] 용어 정의·담당자·분류         |
|  [운영 메타데이터]   ETL 실행 이력·데이터 품질·리니지|
|                                                       |
|  -> 데이터 카탈로그: 3가지 메타데이터를 통합 검색     |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)는 도서관의 <strong>카드 목록</strong>이다. 책([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) 자체가 아니라 "이 책이 어디에 있고, 누가 썼고, 무슨 내용인지"를 알려준다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) 핵심 기능

| 기능 | 설명 |
|:---|:---|
| **검색·디스커버리** | 키워드로 테이블·컬럼 검색 |
| **리니지** | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 출처->변환->목적지 추적 |
| <strong><a href="/knowledge-base/studynote/05_database/07_exam_summary/393_data_dictionary/">데이터 사전</a></strong> | 용어 정의·표준 관리 |
| **소유권** | [데이터 스튜어드](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/067_data_steward_data_quality/)·담당팀 |
| **품질 점수** | 테이블별 품질 지표 |

- **📢 섹션 요약 비유**: [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)는 넷플릭스의 검색 화면이다. 영화([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 쉽게 찾고, 감독·출연진([메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/))·줄거리(정의)를 확인할 수 있다.

---

## Ⅲ. 비교 및 연결

| 비교 | MMS 없음 | MMS 적용 |
|:---|:---|:---|
| **검색** | 담당자에게 질문 | **자체 검색** |
| **리니지** | 모름 | **출처 추적** |
| **표준** | 용어 불일치 | <strong><a href="/knowledge-base/studynote/05_database/07_exam_summary/393_data_dictionary/">데이터 사전</a></strong> |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 대표 도구
- **DataHub** (LinkedIn): [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 플랫폼.
- **Amundsen** (Lyft): [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 디스커버리.
- **Collibra**: 엔터프라이즈 [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/).
- **OpenMetadata**: [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/), 표준 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/).

---

## Ⅴ. 기대효과 및 결론

MMS/[데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)는 <strong><a href="/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/">데이터 거버넌스</a>의 기술적 핵심</strong>이며, [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/) 아키텍처에서 셀프서비스 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼의 기반이 된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/">메타데이터</a></strong> | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 대한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/">데이터 카탈로그</a></strong> | 현대적 MMS |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/">데이터 리니지</a></strong> | 출처->변환->목적지 추적 |
| <strong><a href="/knowledge-base/studynote/05_database/07_exam_summary/393_data_dictionary/">데이터 사전</a></strong> | 용어·정의 표준 |
| <strong><a href="/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/">데이터 거버넌스</a></strong> | MMS의 상위 관리 체계 |

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 데이터 사전 (엑셀, 2000s)]
    |
    v
[메타데이터 리포지토리 (2010s)]
    |
    v
[데이터 카탈로그 (DataHub/Amundsen, 2018~)]
    |
    v
[Active Metadata (2022~) — 자동 메타데이터 수집·활용]
    |
    v
[현재: AI 카탈로그 — 자연어로 데이터 검색·이해]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)는 도서관의 <strong>카드 목록</strong>이에요. 책이 <strong>어디에 있고 무슨 내용</strong>인지 알려줘요.
2. 카드 목록(MMS)이 없으면 수백만 권의 책 중에서 **원하는 책을 찾을 수 없어요**.
3. [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) 덕분에 "매출 테이블이 어디 있지?"를 <strong>바로 검색</strong>할 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 125 / 600

<- **이전**: [124. 데이터 거버넌스 (Data Governance) - 데이터 품질·보안·표준의 전사 관리 체계](/knowledge-base/studynote/05_database/02_modeling_normalization/124_data_governance_db_perspective/)
**다음**: [126. 데이터 표준화 (단어·도메인·용어) - 전사 데이터 용어 통일 체계](/knowledge-base/studynote/05_database/02_modeling_normalization/126_data_standardization_word_domain_term/) ->

---
