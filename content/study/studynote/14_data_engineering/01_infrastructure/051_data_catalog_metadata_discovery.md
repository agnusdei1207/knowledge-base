+++
weight = 51
title = "51. 데이터 카탈로그 (Data Catalog) - 메타데이터 검색 및 자산화"
date = "2026-04-10"
[extra]
categories = "studynote-data-engineering"
+++

# 51. [[213_data_catalog_metadata|데이터 카탈로그]] ([[213_data_catalog_metadata|Data Catalog]])

> ⚠️ 이 문서는 기업 내 수천 개의 [[001_dikw_pyramid|데이터]]베이스와 [[208_data_lake_schema_on_read|데이터 레이크]]에 흩어진 테이블들이 어떤 의미를 담고 있고, 누가 만들었으며, 언제 마지막으로 업데이트되었는지에 대한 '[[001_dikw_pyramid|데이터]]의 [[001_dikw_pyramid|데이터]]([[012_metadata|메타데이터]])'를 긁어모아, **분석가와 현업 직원이 구글 검색하듯 사내 [[001_dikw_pyramid|데이터]]를 쉽게 찾아 쓸 수 있게 해주는 '[[001_dikw_pyramid|데이터]] 도서관의 색인([[154_database_index_b_tree_search_optimization|Index]]) 시스템'**을 다룹니다.

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: "우리 회사에 20대 여성 고객의 최근 한 달 구매 이력 [[001_dikw_pyramid|데이터]]가 있나? 있다면 어느 DB의 어떤 테이블에 있지?"라는 질문에 1초 만에 답을 찾아주는 지능형 [[001_dikw_pyramid|데이터]] 탐색([[001_dikw_pyramid|Data]] Discovery) 포털이다.
> 2. **가치**: [[001_dikw_pyramid|데이터]] 엔지니어에게 "그 테이블 이름이 뭐예요?"라고 묻고 기다리는 엄청난 커뮤니케이션 낭비를 없애고, 버려진 쓰레기 [[001_dikw_pyramid|데이터]]([[288_data_swamp_metadata_management_absence|Data Swamp]])에 의미(Tag)를 부여해 가치 있는 '[[001_dikw_pyramid|데이터]] 자산(Asset)'으로 탈바꿈시킨다.
> 3. **기술 체계**: 사내 모든 DB의 [[005_schema|스키마]]를 봇(Crawler)이 주기적으로 훑어서 [[012_metadata|메타데이터]]를 자동 수집하고, [[001_dikw_pyramid|데이터]]의 출처와 가공 과정을 보여주는 혈통([[214_data_lineage_tracking|Data Lineage]]), 민감 정보 마스킹 및 권한 통제([[052_data_governance_framework|Data Governance]]) 기능이 결합되어 있다 (예: AWS Glue, Amundsen).

---

### Ⅰ. 흩어진 [[001_dikw_pyramid|데이터]]의 늪과 분석가의 고통
[[001_dikw_pyramid|데이터]]가 많아질수록 아이러니하게도 [[001_dikw_pyramid|데이터]]를 찾지 못하는 기현상이 벌어진다.

1. **암호 같은 테이블 명과 파편화**:
   - 회사 DB에 들어가 보면 `TB_CUST_MST_2023_V2`, `TEMP_ORDER_DUMP` 같은 암호문 수준의 테이블이 수만 개 쌓여 있다.
   - 마케팅 분석가는 이 테이블이 어떤 컬럼을 가졌는지, 어제 자 [[001_dikw_pyramid|데이터]]가 반영된 최신 본인지 알 방법이 없어 결국 아는 엔지니어에게 메신저로 물어보느라 하루를 허비한다.
2. **[[001_dikw_pyramid|데이터]] 사일로와 [[085_confidence_association_rule_conditional_probability|신뢰도]] 하락**:
   - 영업팀이 만든 고객 테이블과 마케팅팀이 만든 고객 테이블이 내용이 다르다. 어떤 [[001_dikw_pyramid|데이터]]가 "회사 공식 [[303_authentication_authorization_patterns|인증]]" [[001_dikw_pyramid|데이터]]인지 알 수 없어 잘못된 분석 보고서가 사장님께 올라가는 대참사가 터진다.

📢 섹션 요약 비유: 세계 최대의 거대한 도서관([[208_data_lake_schema_on_read|데이터 레이크]])을 지어놓고 책을 산더미처럼 쌓아 놨지만, 책등에 제목도 없고 저자도 안 적혀 있으며 검색용 컴퓨터조차 없는 상황입니다. 책 하나를 찾으려면 사서(엔지니어)를 붙잡고 하루 종일 창고를 뒤져야 하는 끔찍한 미로와 같습니다.

---

### Ⅱ. [[213_data_catalog_metadata|데이터 카탈로그]]의 3대 핵심 기능
[[394_catalog_metadata|카탈로그]]는 단순한 엑셀 명세서가 아니라 살아 숨 쉬는 포털이다.

1. **[[001_dikw_pyramid|데이터]] 탐색 ([[001_dikw_pyramid|Data]] Discovery) 및 [[012_metadata|메타데이터]] 자동화**:
   - 검색창에 '매출액'이라고 치면 관련된 모든 사내 테이블이 나열된다.
   - 크롤러(예: AWS Glue Crawler)가 밤마다 사내망의 MySQL, S3, MongoDB를 돌아다니며 테이블 이름, 컬럼 타입, 로우(Row) 수 등 물리적 [[012_metadata|메타데이터]]를 자동으로 긁어와([[009_schema_on_read|Schema-on-read]]) [[394_catalog_metadata|카탈로그]]를 갱신한다.
2. **비즈니스 용어집 (Business Glossary)과 태깅**:
   - 물리적 컬럼명 `CUST_NM`에 "고객의 실명"이라는 한글 비즈니스 설명을 매핑한다.
   - 개인정보가 포함된 컬럼에는 빨간색으로 `[PII(개인정보) 경고]` 태그를 달아 분석가가 무단으로 조회하지 못하게 시각적으로 통제한다.
3. **[[214_data_lineage_tracking|데이터 리니지]] ([[214_data_lineage_tracking|Data Lineage]] / 혈통 추적)**:
   - "이 훌륭한 대시보드 테이블은 도대체 원본 [[001_dikw_pyramid|데이터]]가 어디서 온 거지?"
   - [[213_data_catalog_metadata|데이터 카탈로그]]는 원본 DB -> 전처리 스크립트([[215_etl_vs_elt_pipeline|ETL]]) -> 최종 마트 테이블까지 [[001_dikw_pyramid|데이터]]가 어떤 파이프라인을 타고 흘러왔는지 지하철 노선도처럼 시각화하여 [[001_dikw_pyramid|데이터]]의 투명성을 보장한다.

📢 섹션 요약 비유: 아무렇게나 쌓인 책들에 바코드를 붙여서 도서관 검색용 컴퓨터([[394_catalog_metadata|카탈로그]])를 만든 것입니다. "해리포터"를 검색하면 책의 위치(DB), 줄거리(비즈니스 용어), 이 책을 번역한 사람(리니지), 19세 미만 구독 불가(보안 태그) 딱지까지 한 화면에 완벽하게 보여주는 시스템입니다.

---

### Ⅲ. [[052_data_governance_framework|데이터 거버넌스]]의 척추 ([[001_dikw_pyramid|Data]] Mesh와의 결합)
[[394_catalog_metadata|카탈로그]] 없이는 현대적 [[001_dikw_pyramid|데이터]] 조직론이 성립할 수 없다.

1. **규제 준수 ([[058_it_compliance_sox_basel_gdpr_isms|Compliance]] & [[283_security_tactics|Security]])**:
   - [[001_dikw_pyramid|데이터]] 3법([[783_pipa_korea|개인정보보호법]] 등)이 강화되면서, [[606_auditing_linux_auditd|감사]]관이 "당신네 회사는 고객 주민번호가 어느 DB에 저장되어 있소?"라고 물을 때, [[394_catalog_metadata|카탈로그]]가 없으면 대답할 수조차 없어 막대한 과징금을 맞는다. [[394_catalog_metadata|카탈로그]]는 민감 정보의 중앙 통제소 역할을 한다.
2. **[[211_data_mesh_domain_ownership|데이터 메시]] ([[320_data_mesh|Data Mesh]])의 쇼핑몰 창구**:
   - [[211_data_mesh_domain_ownership|데이터 메시]] 사상에서는 각 부서([[064_relation_domain|도메인]])가 [[001_dikw_pyramid|데이터]]를 가공해 '상품(Product)'으로 내놓아야 한다고 했다.
   - 그 부서들이 만든 상품들을 예쁘게 진열해 놓고 전사 직원들이 장바구니에 담아([[014_api_posix|API]] 권한 신청) 가져다 쓸 수 있게 해 주는 거대한 아마존/쿠팡 쇼핑몰 같은 플랫폼 창구가 바로 [[213_data_catalog_metadata|데이터 카탈로그]](Amundsen, Datahub 등)다.

📢 섹션 요약 비유: [[213_data_catalog_metadata|데이터 카탈로그]]는 단순한 전화번호부가 아니라, 회사 내의 모든 정보 자산이 합법적으로 거래되고 교환되도록 보증하는 '정부 공인 부동산 등기소'이자, 흩어진 상인(부서)들의 물건을 한곳에 모아 파는 '디지털 오픈마켓 플랫폼'입니다.

---

### Ⅳ. 실무 적용 및 기술사 판단

#### 주요 [[213_data_catalog_metadata|데이터 카탈로그]] 도구 비교

| 도구 | 출처 | 특징 | 비용 |
|:---|:---|:---|:---|
| **AWS Glue [[213_data_catalog_metadata|Data Catalog]]** | AWS | Glue Crawler 자동 수집, Athena·Redshift 연동 | 종량제 |
| **Amundsen** | Lyft [[191_oss_license_compliance|오픈소스]] | Neo4j [[070_graph_datastructure|그래프]] 기반 검색, [[214_data_lineage_tracking|데이터 리니지]] | 무료 |
| **DataHub** | LinkedIn [[191_oss_license_compliance|오픈소스]] | [[477_rest_api_architecture|REST API]] 기반, 실시간 [[012_metadata|메타데이터]] 인제스트 | 무료 |
| **Apache Atlas** | Apache | [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 에코시스템 통합, JanusGraph 기반 | 무료 |
| **Google [[213_data_catalog_metadata|Data Catalog]]** | GCP | [[263_storage_compute_separation_bigquery|BigQuery]]·GCS 네이티브 통합, Tag Template | 종량제 |
| **Collibra / Alation** | 상용 | 거버넌스 중심, 비즈니스 용어집 강점 | 고가 라이선스 |

#### 의사결정 [[435_checklist_based_testing|체크리스트]]

- **클라우드 올인 (AWS)** → Glue [[213_data_catalog_metadata|Data Catalog]]: 네이티브 연동, [[009_config|설정]] 최소
- **[[191_oss_license_compliance|오픈소스]]·멀티클라우드** → DataHub: 확장성, [[156_rest_representational_state_transfer|REST]]/[[246_graphql_query_language_overfetching_solution|GraphQL]] [[014_api_posix|API]] 풍부
- **거버넌스·규제 최우선** → Collibra/Alation: [[273_data_stewardship|데이터 스튜어드십]], [[606_auditing_linux_auditd|감사]] 추적
- **[[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] 레거시** → Apache Atlas: [[544_hive|Hive]]·[[543_hbase|HBase]]·[[179_kafka_flink_watermark_time_window|Kafka]] [[012_metadata|메타데이터]] 수집

#### [[128_water_scrum_fall_anti_pattern|안티패턴]]

**[[394_catalog_metadata|카탈로그]] = 엑셀 명세서**: 컨플루언스(Confluence)나 구글 시트에 테이블 명세를 수동으로 관리하면, [[005_schema|스키마]]가 바뀔 때마다 문서가 뒤쳐진다. **[[394_catalog_metadata|카탈로그]]는 크롤러가 자동으로 갱신하는 '살아 있는 시스템'이어야 한다**. 문서와 실제 DB가 달라지는 순간 신뢰가 깨지고, 결국 아무도 문서를 보지 않게 된다.

📢 섹션 요약 비유: 엑셀 명세서로 [[001_dikw_pyramid|데이터]]를 관리하는 것은 **전화번호부를 손으로 쓰는 것**과 같습니다. 연락처가 바뀔 때마다 지우고 다시 쓰는 사이에 이미 정보가 틀려져 있습니다. 자동 동기화되는 스마트폰 연락처([[394_catalog_metadata|카탈로그]])가 정답입니다.

---

### Ⅴ. 기대효과 및 결론

[[213_data_catalog_metadata|데이터 카탈로그]]를 도입한 조직은 **분석가의 [[001_dikw_pyramid|데이터]] 탐색 시간을 70~80% 단축**하고, [[001_dikw_pyramid|데이터]] 품질 이슈를 리니지 추적으로 근본 원인까지 30분 내에 파악할 수 있다. 더 중요한 것은, [[001_dikw_pyramid|데이터]]가 '누군가의 노트북에 있는 [[501_file_definition_logical_record|파일]]'이 아니라 **조직 자산(Asset)**으로 공식 등록되어, 재사용·[[606_auditing_linux_auditd|감사]]·보호가 가능해진다는 점이다.

**한계**: [[394_catalog_metadata|카탈로그]]에 [[012_metadata|메타데이터]]를 등록해도 비즈니스 설명(Business Glossary)은 사람이 작성해야 한다. 자동 크롤링은 물리적 [[012_metadata|메타데이터]](컬럼명·타입)만 수집하지, "이 컬럼이 무슨 의미인가?"라는 비즈니스 맥락까지 이해하지 못한다. [[190_ai_llm_requirements_specification|AI]] 기반 자동 태깅과 [[263_llm_large_language_model|LLM]] 기반 [[012_metadata|메타데이터]] 생성이 이 한계를 점차 극복하고 있다.

[[213_data_catalog_metadata|데이터 카탈로그]]는 "[[001_dikw_pyramid|데이터]]를 정리하는 것"이 아니라, **"[[001_dikw_pyramid|데이터]]를 찾을 수 있게 만드는 것"** — 찾을 수 없는 [[001_dikw_pyramid|데이터]]는 존재하지 않는 것과 같다.

📢 섹션 요약 비유: [[213_data_catalog_metadata|데이터 카탈로그]]는 **국세청의 부동산 등기부**와 같습니다. 등기부에 올라가지 않은 부동산은 공식적으로 존재하지 않고, 매매도 불가능합니다. [[001_dikw_pyramid|데이터]]도 [[394_catalog_metadata|카탈로그]]에 등록되어야 비로소 '자산'이 됩니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[214_data_lineage_tracking|데이터 리니지]] ([[214_data_lineage_tracking|Data Lineage]])** | [[001_dikw_pyramid|데이터]]의 원본 → 가공 → 최종 저장까지 흐름 추적; [[394_catalog_metadata|카탈로그]]의 핵심 기능 |
| **[[211_data_mesh_domain_ownership|데이터 메시]] ([[320_data_mesh|Data Mesh]])** | [[064_relation_domain|도메인]]별 [[001_dikw_pyramid|데이터]] 제품화; [[394_catalog_metadata|카탈로그]]가 제품 진열대 역할 |
| **[[052_data_governance_framework|데이터 거버넌스]]** | [[001_dikw_pyramid|데이터]] 품질·보안·규정 준수; [[394_catalog_metadata|카탈로그]]가 중앙 통제소 |
| **[[203_metadata_management|메타데이터 관리]]** | 물리적([[005_schema|스키마]]) + 비즈니스(의미) + 운영(갱신 주기) [[012_metadata|메타데이터]] 통합 |
| **[[067_data_steward_data_quality|데이터 스튜어드]] ([[067_data_steward_data_quality|Data Steward]])** | [[001_dikw_pyramid|데이터]] 자산의 품질과 의미를 관리하는 담당자; [[394_catalog_metadata|카탈로그]]의 핵심 사용자 |

### 📈 관련 키워드 및 발전 흐름도

```text
데이터 사일로 → 데이터 늪(Data Swamp) 위기
    │
    ▼
데이터 카탈로그 등장
    ├─► 크롤러 자동 메타데이터 수집 (물리적 메타데이터)
    ├─► 비즈니스 용어집 (Business Glossary) 수동 매핑
    └─► 데이터 리니지 — ETL 흐름 시각화
    │
    ▼
데이터 거버넌스 통합 (PII 태깅 · 접근 제어)
    │
    ▼
데이터 메시 + 카탈로그 = 데이터 마켓플레이스
    │
    ▼
AI 기반 자동 태깅 · LLM 메타데이터 생성 (미래)
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[213_data_catalog_metadata|데이터 카탈로그]]는 **'거대한 도서관의 검색 컴퓨터'** 예요. "공룡 책"을 검색하면 그 책이 3층 A구역 5번 선반에 있다고 바로 알려주는 시스템이에요!
2. 로봇 사서(크롤러)가 매일 밤 새로 들어온 책을 자동으로 바코드 스캔해서 목록을 업데이트하고, 19금 딱지(보안 태그)도 자동으로 붙여줘요.
3. [[394_catalog_metadata|카탈로그]]가 없으면 **100만 권의 책이 쌓인 창고에서 눈 감고 책 찾기**를 해야 해요. 그래서 [[394_catalog_metadata|카탈로그]]는 [[001_dikw_pyramid|데이터]]를 가치 있게 만드는 첫 번째 단계랍니다!
