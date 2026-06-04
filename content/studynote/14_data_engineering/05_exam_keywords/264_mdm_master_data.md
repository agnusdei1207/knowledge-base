+++
title = "264. 마스터 데이터 관리 MDM 골든 레코드 (Master Data Management MDM Golden Record)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: **MDM(Master Data Management) 골든 레코드(Golden Record)**는 다수의 이기종 시스템(CRM, ERP, SCM, 레거시 DB)에 분산된 동일 실재 개체(Real-world Entity)의 중복 레코드들을 **결정론·확률론·퍼지(Fuzzy) 매칭**(예: Fellegi-Sunter, Levenshtein, Jaro-Winkler)으로 식별하고, **Survivorship Rule**(소스 신뢰도, 최신성, 완전성, 최장값, 가중합산)에 근거하여 단일 권위 레코드(Single Source of Truth)로 통합한 후, **Data Steward**가 이를 인증·승인(Stewardship)하여 전사 시스템에 **Publish/Subscribe** 방식으로 배포하는 데이터 거버넌스의 핵심 산출물이다.
> 2. **가치**: Gartner 보고에 따르면 전사 데이터의 70~80%가 중복·불일치 상태로 존재하며, 골든 레코드 도입 시 **마케팅 ROI 15~20% 향상, 우편·인쇄 비용 30% 절감, 고객 식별 오류로 인한 CS 비용 25% 감소, ERP·CRM 통합 프로젝트 기간 40% 단축** 등 정량적 효과가 검증되어 있다. ISO 8000·DAMA-DMBOK·DCAM 기반의 데이터 품질 8개 차원(정확성·완전성·일관성·적합성·시의성·유일성·유효성·무결성)을 모두 충족시키는 유일한 방법론이다.
> 3. **판단 포인트**: Gartner의 4대 MDM 아키텍처 스타일(Registry / Consolidation / Coexistence / Centralized) 중 어느 것을 채택할지, **Match-Threshold**를 결정론·확률론 어느 모델로 설정할지, **Survivorship 우선순위**를 도메인(고객·제품·공급사·자산·위치)별로 어떻게 차등 적용할지, 그리고 **Stewardship Workflow**(자동 승인 vs 수동 검토)의 Human-in-the-Loop 비중을 어느 선에서 끊을지가 아키텍처 성패를 가른다.

---

## Ⅰ. 개요 및 필요성

### 1.1 데이터 비대칭과 실재 개체 부재의 문제

현대 기업의 데이터 환경은 **다중 채널·다중 시스템·다중 국가**라는 3중 다중성(Multi-X) 환경에서 운영된다. 동일한 고객이 ERP에는 `CUST_ID=0012345`, CRM에는 `CustomerKey=ACME-2024-001`, 모바일 앱에는 `UUID=x8a2f-...`, 데이터 레이크에는 `email_hash=...`로 분산 저장되며, M&A·조직개편·레거시 마이그레이션이 반복되면서 **고객 1인당 평균 3~5개의 중복 레코드(Duplicate)**가 발생한다(Experian Data Quality Report 2023, 평균 3.4배).

이 상태에서 다음 문제가 발생한다:
- **고객 단일성 부재**: 영업팀이 동일 기업을 서로 다른 영업사원에게 중복 할당하여 Cannibalization(고객 자기 잠식) 발생
- **규제 컴플라이언스 실패**: GDPR·개인정보보호법의 데이터 정정권 행사 시 어느 시스템이 '진실'인지 입증 불가
- **분석 왜곡**: 360° Customer View를 요구하는 마케팅·리스크 분석에서 KPI 1.2~1.8배 과대 계상
- **운영상실**: 제품 마스터 불일치로 BOM(Bill of Materials) 누락, 재고 회전율 왜곡

### 1.2 개념 흐름도: 분산 레코드 -> 실재 개체 -> 골든 레코드

```text
   +--------------------------------------------------------------------------+
   |                  출처(Source) 시스템 - 다중 도메인 레코드                  |
   +----------+----------+----------+----------+----------+-------------------+
   |   ERP    |   CRM    |  POS     | Mobile   | Web      |  Legacy Mainframe |
   | (SAP S/4)|(Salesf.) |(Oracle)  | App      | Portal   |  (AS/400)         |
   +----+-----+----+-----+----+-----+----+-----+----+-----+----+--------------+
        |          |          |          |          |          |
        | ID=001   | ID=AC-9  | ID=P-22  | UUID=x8  | email    | ID=9001
        | "홍길동" | "(주)ABC"| "Hong"   | "ABC Inc"| "abc.com"| "(주)에이비씨"
        | 010-1234 | 02-555   | -        | -        | -        | 02-555-1234
        +----------+----------+----------+----------+----------+
                              |
                              v  (ETL / CDC / API Streaming)
        +----------------------------------------------------------+
        |        Staging Zone - 원천 무변경 적재 (Raw Layer)         |
        |        - Data Profiling: 결측률·도메인위반률 측정           |
        |        - Profiling Tool: Informatica IDMC, Talend DQ      |
        +------------------------+---------------------------------+
                                 |  Parsing / Standardization
                                 v
        +----------------------------------------------------------+
        |  Standardization & Cleansing Zone                         |
        |  - 주소: 행정안전부 도로명주소 API (JIBUN↔ROAD)            |
        |  - 전화: E.164 국제표준 010-XXXX-XXXX 정규화              |
        |  - 법인등기번호: 사업자등록번호 검증(국세청 API 13자리)      |
        |  - 한글/영문/약어 동음이의어 토큰화(Tokenization)          |
        +------------------------+---------------------------------+
                                 |  Match Engine
                                 v
        +----------------------------------------------------------+
        |   Matching Zone - 실재 개체(Entity) 식별                   |
        |   - Blocking: (성, 우편번호앞3자리) 기준 후보군 축소        |
        |   - Pair-wise: Levenshtein≤2, Jaro-Winkler≥0.88, Soundex  |
        |   - Probabilistic: Fellegi-Sunter m/u 가중치 산출          |
        |   - ML: Graph-based Entity Resolution (DGI)               |
        +------------------------+---------------------------------+
                                 |  Merge & Survivorship
                                 v
        +----------------------------------------------------------+
        |   ★ Golden Record Zone ★  <-  본 노트가 다루는 핵심         |
        |   Survivorship Rule 적용 -> 단일 권위 레코드 생성            |
        |   - Source Authority: SAP MDG > Salesforce > Web          |
        |   - Most Recent:  updated_at DESC 우선                    |
        |   - Most Complete: NULL 아닌 필드 수 DESC                  |
        |   - Longest Value: 주소 문자열 길이 DESC                   |
        |   - Cust. Rule: 결제이력은 '인증'필드 오버라이드          |
        +------------------------+---------------------------------+
                                 |  Stewardship Workflow
                                 v
        +----------------------------------------------------------+
        |   Steward Review & Publish (인간 검토·승인)                 |
        |   - 자동승인(Confidence≥0.95), 수동승인(0.7≤Conf<0.95)     |
        |   - Reject & Split(Conf<0.7) - 별도 클러스터 보류         |
        |   - Data Lineage 추적: Graph DB (Neo4j, TigerGraph)        |
        +------------------------+---------------------------------+
                                 |  Distribution (Pub/Sub)
                                 v
   +--------------------------------------------------------------------+
   |  Downstream 시스템 - Golden Record 기반 단일 참조                  |
   |  - CDP(Customer Data Platform), DWH, Lake, API Gateway, BI/AI     |
   +--------------------------------------------------------------------+
```

### 1.3 도입 필요성: Old Paradigm vs New Paradigm

| 구분 | Old Paradigm (Pre-MDM) | New Paradigm (MDM + Golden Record) |
| :--- | :--- | :--- |
| **데이터 거버넌스** | 시스템별 Owner 분산, 정책 부재 | 전사 Data Governance Council + 도메인별 Steward 조직 |
| **고객 식별** | 시스템별 ID 별도, 주민번호 활용(PII 과다) | 결정적·비결정적 키(이메일·휴대폰·법인번호) 다중 키 전략 |
| **중복 처리** | 야간 배치 후 수작업 정리 (월 1회) | Streaming CDC(Change Data Capture) 기반 실시간 매칭·머지 |
| **품질 측정** | 무측정 (보이지 않는 비용) | 데이터 품질 8차원 KPI 대시보드(완전성≥99.5% 등) |
| **규제 대응** | 요청 시 일제히 시스템에서 수동 검색 | GDPR Art. 15·17 요청 시 골든 레코드 1개 PATCH로 전사 일괄 |
| **분석 활용** | ID별 카운팅(과대 계상), JOIN 실패 | 엔티티 키 1개로 360° View, Graph 분석 가능 |
| **비용** | 야간 정합 배치 운영비, CS 비용 25% 추가 | 초기 구축비 1.2억 / 연 절감 3.5억(예: 글로벌 제조사 사례) |

- **📢 섹션 요약 비유**: 골든 레코드는 마치 **"전사 표준 가족관계증명서"**와 같다. 같은 사람이 호적·여권·운전면허·학적부에 다르게 기재되어 있을 때, 어느 한 곳이 '표준 진본'으로 인정되어 다른 모든 시스템이 그 내용을 따라 적도록 하는 단일 진실의 원천(SSOT, Single Source of Truth)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 Gartner 4대 MDM 아키텍처 스타일 (Architectural Style)

```text
  +--------------------------------------------------------------------------+
  |                       Gartner's 4 MDM Styles                             |
  +----------------+----------------+----------------+---------------------+
  |   (a) Registry | (b)Consolidat. |(c)Coexistence  |   (d) Centralized   |
  |  레지스트리     |  통합형         |  공존형         |   집중형             |
  |                |                |                |                      |
  |  [App A] --+   | [App A]--+     | [App A]-+      |     [App A]          |
  |            |   |         |     |         |      |         |             |
  |  [App B] --+   | [App B]--+     | [App B]-+      |     [App B]          |
  |            |   |         |     |         |      |         |             |
  |  [App C] --+   | [App C]--+     | [App C]-+      |     [App C]          |
  |            v   |         v      |         v      |         v             |
  |         +----+ |       +----+   |       +----+   |       +----+          |
  |         |MDM | |       |MDM |   |       |MDM |   |       |MDM |          |
  |         |Index| |       |Hub |   |       |Hub |   |       |Store|         |
  |         +----+ |       +----+   |       +----+   |       +----+          |
  |     Index only |      Publish   |     양방향 동기 |  Source of Truth      |
  |     (Pointer)  |      Only      |     (Bi-sync) |  App Read-Only        |
  |                |                |                |                      |
  |  <-- 최소투자  | <-- 분석·BI 우세 | <-- 실무 표준   | <-- 일관성 최우선      |
  |    CRM/ERP간   |    DWH 구축 시  |    대기업 표준 |    금융·의료 규제     |
  |    ID연결 용도 |    적합         |    (Informatica|    (GDPR·HIPAA)      |
  |                |                |     Reltio)   |                      |
  +----------------+----------------+----------------+----------------------+
```

### 2.2 골든 레코드 5단계 처리 파이프라인 (Zero-Touch & Human-in-the-Loop)

```text
   +-------------------------------------------------------------------------+
   |              Step 1: Data Profiling & Census                          |
   |  - 컬럼별 카디널리티, NULL%, 도메인 위반률(정규식·Lookup 위반) 측정     |
   |  - 한글 초성/중성/종성 분리 후 통계, KCPD 한국어 풀어쓰기 검사          |
   +-------------------------------------+-----------------------------------+
                                         v
   +-------------------------------------------------------------------------+
   |              Step 2: Standardization & Parsing                          |
   |  - 주소: 행정안전부 PNU(Parcel Number) 표준화, 도로명주소(ROAD)↔지번(JIBUN)|
   |  - 이름: 한글 조사/공백 제거, (주)/(유) 법인 접두사 분리, 한자 변형 정규화 |
   |  - 사업자번호: 13자리 검증 모듈로(10) Check Digit, 폐업 여부(국세청 API)  |
   |  - 연락처: E.164(+82), 이메일 RFC 5321 검증, 도메인 MX 조회              |
   +-------------------------------------+-----------------------------------+
                                         v
   +-------------------------------------------------------------------------+
   |              Step 3: Match - Blocking & Pair-wise                      |
   |  +--------------------------------------------------------------+       |
   |  |  ① Blocking: O(N²) -> O(N·k
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 264 / 300

<- **이전**: [263. 데이터 품질 관리 프로파일링 정합성 검증 (Data Quality Management Profiling Validation)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/263_data_quality/)
**다음**: [265. 데이터 거버넌스 프레임워크 정책 표준 (Data Governance Framework DAMA DMBOK)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/265_data_governance_framework/) ->

---
