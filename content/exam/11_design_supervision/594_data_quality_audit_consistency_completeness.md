---
title: "Data Quality Audit Consistency Completeness"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데이터 품질 감리는 DAMA DMBOK의 6대 차원(완전성·정합성·정확성·적시성·유일성·유효성)을 대상으로 메타데이터, 데이터 프로파일링, 참조 무결성, CRUD 매트릭스, 데이터 리니지 분석을 통해 결함률(DQ-Score)을 정량화하고 임계치 기반으로 합격/경고/불합격을 판정하는 체계적 검증 활동이다.
> 2. **가치**: Gartner 보고에 따르면 데이터 품질 결함으로 인한 기업 평균 손실은 연 매출의 15~25%이며, 완전성·정합성 진단 자동화 시 데이터 거버넌스 ROI가 3.2배, ETL 재작업 시간 60% 감소, 규제 준수(개인정보보호법, IFRS, Basel III) 감사 리스크 45% 저감 효과를 달성한다.
> 3. **판단 포인트**: 감리 깊이(샘플링 vs 전수검사), 정합성 검증 레벨(컬럼/레코드/테이블/시스템/업무규칙), 진단 도구 선정(상용: Informatica vs 오픈소스: Great Expectations/Apache Griffin), 자동화 수준(스케줄링 + CI/CD 통합 vs 수동), 그리고 진단 결과를 마스터데이터 거버넌스·데이터 카탈로그·DLP와 어떻게 통합할지가 핵심 의사결정 축이다.

---

## Ⅰ. 개요 및 필요성

데이터 품질(Data Quality)이란 의사결정·운영·규제 준수를 위해 수집·저장·처리되는 데이터가 **사용 목적에 부합하는 정도( Fitness for Use )**를 의미한다. 그러나 글로벌 기업의 평균 데이터 결함률은 27%(Experian Global Data Management Benchmark)에 달하며, 국내 금융권의 경우 고객 정보 중복률 18%, 핵심 엔터티(Customer, Account)의 정합성 위반이 12~15% 수준으로 조사된다. 이러한 데이터 품질 저하는 **"Garbage In, Garbage Out"** 원칙에 따라 분석 결과의 신뢰도 붕괴, AI 모델의 편향, 규제 위반 과징금, 그리고 고객 신뢰도 하락으로 직결된다.

특히 2020년 개인정보보호법 개정, EU의 GDPR, 그리고 2024년 시행된 데이터산업법·신용정보법에 따라 **데이터 품질 관리 의무가 법적 책임**으로 강화됨에 따라, 정보시스템 감리(Software Audit) 영역에서도 **데이터 품질 감리**가 필수 검증 항목으로 부상했다. 한국정보통신기술협회(TTA)의 「정보시스템 감리 기준」과 행정안전부의 「데이터 품질관리 가이드라인」, 그리고 DAMA DMBOK2(Data Management Body of Knowledge) 프레임워크를 기반으로, **정합성(Consistency)**과 **완전성(Completeness)**은 6대 품질 차원 중에서도 가장 빈번하게 위반되는 핵심 지표이다.

```text
+--------------------------------------------------------------------------+
|                    데이터 품질 문제 발생의 계층적 원인 구조                 |
+--------------------------------------------------------------------------+
|                                                                          |
|   [업무·규제 계층]   "주문 고객은 실재하는 회원이어야 한다"                |
|        |                  (업무규칙, Business Rule)                       |
|        |                                                                |
|   [시스템·인터페이스]   주문ERP --► CRM --► 회원DB --► 데이터웨어하우스     |
|        |                  (Legacy/Main/Stat/Cloud 4-tier 동기화)         |
|        |                                                                |
|   [데이터 모델 계층]   Customer(PK=cust_id)  ◄-- FK 무결성, 도메인 제약   |
|        |                                                                |
|   [물리·저장 계층]     Oracle 19c / PostgreSQL 15 / Hadoop HDFS / S3      |
|                                                                          |
|   v  문제 발생 시 파급 경로 (Propagation)                                |
|   +----------------------------------------------------------------+    |
|   |  소스 결함 1건 --► ETL 증식 --► 분석 오류 --► 의사결정 실패       |    |
|   |                  --► API 응답 불일치 --► 고객 클레임             |    |
|   |                  --► 레포트 재발행 --► 비용 발생                 |    |
|   +----------------------------------------------------------------+    |
|                                                                          |
+--------------------------------------------------------------------------+
```

기존 패러다임은 **"데이터는 저장되면 끝"**이라는 Storage-Centric 사고였으나, 현재는 **"데이터는 흐르고 사용되어야 가치를 가진다"**는 Data-Centric 사고로 전환되었다. 이에 따라 정합성은 단순한 NULL/NOT NULL 제약을 넘어 **교차 시스템 간, 시간축 간, 도메인 간 일관성**을 포괄하며, 완전성은 **레코드 존재 여부**뿐 아니라 **속성(필드) 채움 정도, 참조 대상의 실재성, 비즈니스 이벤트 누락**까지 확장되었다.

- **📢 섹션 요약 비유**: 데이터 품질 감리는 **'도시 상하수도 감리'**와 같다. 수도꼭지(분석·리포트)에서 물이 나오지 않거나 오염되어 있을 때, 문제는 상류의 정수장·배관·펌프장(소스·ETL·모델) 어디에나 있을 수 있으므로, **수질검사원(감리인)**이 채수 지점·배관 연결·저수조 수위까지 전수 진단해야 깨끗한 물(신뢰 가능한 데이터)이 가정(의사결정자)에 도달한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

데이터 품질 감리는 일반적으로 **5-Layer 진단 아키텍처**로 구성된다. 각 계층은 서로 다른 검증 기법과 도구를 사용하며, 상위 계층은 하위 계층의 결과를 종합하여 최종 DQ-Score를 산출한다.

```text
+--------------------------------------------------------------------------+
|         데이터 품질 감리 5-Layer 아키텍처 (정합성·완전성 중심)             |
+--------------------------------------------------------------------------+
|                                                                          |
|  [Layer 1]  메타데이터 진단 (Metadata Audit)                             |
|             |                                                            |
|             +-► 스키마 진화 추적 (Schema Drift Detection)                |
|             +-► 데이터 사전(Data Dictionary) 완전성                       |
|             +-► 데이터 리니지 자동 수집 (Apache Atlas, DataHub)            |
|                          |                                               |
|                          v                                               |
|  [Layer 2]  프로파일링 진단 (Profiling Audit)                            |
|             |                                                            |
|             +-► 컬럼 단위 통계: NULL%, Distinct%, Min/Max, 분포도         |
|             +-► 패턴 분석: 정규식, 신용카드/이메일/전화번호 형식           |
|             +-► 이상치 탐지: IQR, Z-Score, Isolation Forest               |
|                          |                                               |
|                          v                                               |
|  [Layer 3]  무결성·제약 진단 (Constraint Audit)                          |
|             |                                                            |
|             +-► 완전성: NOT NULL, 필수값, 참조무결성(FK)                   |
|             +-► 정합성: PK 유일성, CHECK 제약, 도메인 값                  |
|             +-► 교차테이블: 합산값 일치, 차감 잔액 무결성                  |
|                          |                                               |
|                          v                                               |
|  [Layer 4]  비즈니스 규칙 진단 (Business Rule Audit)                     |
|             |                                                            |
|             +-► 업무규칙: "주문총액 = 단가×수량+세금"                      |
|             +-► 상태전이: 주문상태 ∈ {접수, 출하, 배송, 완료}              |
|             +-► 시간정합성: 입금일자 ≤ 주문일자+7일                       |
|                          |                                               |
|                          v                                               |
|  [Layer 5]  보고서·의사결정 (Reporting & Decision)                       |
|             |                                                            |
|             +-► DQ-Score 산출 (가중평균 모델)                            |
|             +-► 합격/경고/불합격 판정                                     |
|             +-► 개선 권고(Remediation) 및 마스터데이터 반영                |
|                                                                          |
+--------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **메타데이터 수집기 (Metadata Crawler)** | 스키마·리니지·태그 자동 수집 | Apache Atlas(분산 추적), DataHub(LinkedIn, GraphQL 기반), AWS Glue Catalog, Azure Purview, OpenMetadata; JDBC/ODBC 드라이버로 메타정보를 Graph DB(JanusGraph, Neo4j)에 저장 |
| **데이터 프로파일러 (Data Profiler)** | 컬럼/테이블 단위 통계 산출 | MIN/MAX/AVG/STDDEV, 카디널리티, NULL 분포, Frequency 분석; **Great Expectations**(Python DSL, Expectation Suite), **Apache Griffin**(Spark 기반, 배치+스트리밍), **Deequ**(Amazon, Spark+스케줄러), **pandas-profiling(ydata-profiling)** |
| **규칙 엔진 (Rule Engine)** | 정합성·완전성 룰셋 실행 | Drools(Java BRMS), OpenL Tablets, Excel 기반 룰 정의; **DQLabs**, **Trifacta**, **Talend Data Quality**(tMatchGroup, tRuleSurvive); 룰 표현식: `IS NULL`, `REGEX`, `LOOKUP`, `CUSTOM_SQL` |
| **참조 무결성 검증기 (Reconciliation Engine)** | 교차 시스템·교차 테이블 일치율 측정 | ETL 전후 Row Count·Sum·Hash 비교, HASHBYTES, CHECKSUM_AGG; **Informatica Data Reconciliation**, **PowerCenter**, **Matillion**, **dbt tests**(소스/타겟 row count equality) |
| **이상치 탐지 모델 (Anomaly Detector)** | 통계/ML 기반 비정상 패턴 식별 | Z-Score(임계 ±3σ), IQR(1.5×IQR Rule), DBSCAN, Isolation Forest, AutoEncoder; 시계열 데이터의 경우 Prophet, LSTM 기반 drift detection |
| **DQ-Score 산출기 (Quality Scorer)** | 가중치 기반 종합 점수 산출 | $\text{DQ-Score} = \sum_{i=1}^{n} w_i \cdot s_i$, 여기서 $w_i$는 차원별 가중치, $s_i$는 0~100의 개별 점수; **DAMA 가이드**(정합성 25%, 완전성 20%, 유일성 15%, 정확성 15%, 유효성 15%, 적시성 10%) 또는 조직별 커스텀 가중치 |
| **리포터·대시보드 (Quality Dashboard)** | 시각화 및 임계치 알림 | Grafana + Prometheus, Tableau DQ View, Power BI; KPI: 결함률(%), 일치율(%), 처리량(건/초), 감리 소요 시간; 임계치 초과 시 Alertmanager -> Slack/Teams/Webhook |

#### 핵심 알고리즘 및 정량 지표

**1) 완전성(Completeness) 측정**

$$\text{Completeness}(\%) = \left(1 - \frac{\text{NULL Count} + \text{Empty Count} + \text{Invalid Count}}{\text{Total Records}}\right) \times 100$$

- **컬럼 단위**: 필수 컬럼(NULL 금지) -> 100% 채워져야 합격
- **엔터티 단위**: 레코드의 핵심 속성 집합(예: 고객의 7대 필수정보: 성명, 생년월일, 연락처, 주소, 성별, 국적, CI/DI) 누락 시 무결 레코드 미인정
- **참조 무결성**: 부모 테이블에 존재하지 않는 FK 비율

**2) 정합성(Consistency) 측정**

$$\text{Consistency}(\%) = \left(1 - \frac{\text{Violation Count}}{\text{Total Rules Evaluated}}\right) \times 100$$

- **내부 정합성(Internal)**: 단일 시스템 내 도메인/제약/상태 일관성
- **외부 정합성(External)**: 다중 시스템 간 동일 엔터티의 속성 일치 (예: ERP 고객잔액 = CRM 여신한도 × 0.8 ± 5%)
- **시간 정합성(Temporal)**: 이력 테이블의 유효시작일/유효종료일 논리 오류 (종료일 < 시작일 등)
- **교차 합산 정합성**: 부모-자식 합산 무결성 (예: 일별 매출 합산 = 월별 매출)

**3) 데이터 프로파일링 핵심 통계량**

| 통계량 | 산출 공식/방법 | 진단 활용 |
| :--- | :--- | :--- |
| 카디널리티(Cardinality) | `COUNT(DISTINCT col) / COUNT(*)` | 0에 가까우면 상수 컬럼, 1에 가까우면 PK 가능성 |
| NULL 분포 | `GROUP BY IS_NULL(col)` | NULL이 도메인 일부인지 결측치인지 판별 |
| 데이터 타입 일치율 | `SUM(CASE WHEN typeof=col) / COUNT(*)` | 암묵적 형변환 발생 여부 |
| 패턴 빈도 | Top-K 정규식 패턴 + 잔여 비율 | 데이터 입력 표준화 정도 측정 |
| 값 분포 엔트로피 | $H = -\sum p_i \log_2 p_i$ | 정보량, 비정상 집중 여부 |

**4) 유일성(Uniqueness) 및 중복 탐지**

- **정확 매칭(Exact Match)**: 동일 PK, 동일 SSN, 동일 전화번호
- **퍼지 매칭(Fuzzy Match)**: Jaro-Winkler, Levenshtein, Cosine Similarity 기반; 임계치 0.85 이상이면 동일 개체로 간주
- **블로킹(Blocking)**: 전체 N² 비교 불가하므로 우편번호/성씨 등으로 블록화 후 매칭
- **Survivorship Rule**: 중복 레코드 병합 시 어느 값을 채택할지 우선순위 (가장 최근 / 가장 완전 / 가장 빈번)

**5) 데이터 리니지(Data Lineage)**

```text
[Source DB] --SQL/CDC--► [Raw Zone] --Spark--► [Staging] --dbt--► [Mart]
     |                       |                      |              |
     +-- Atlas Tag -----------+----------------------+---- Column-level Lineage
                    (OpenLineage 표준, Marquez)
```

- **컬럼 단위 리니지**: `final.customer_lifetime_value` <- `mart.orders.total` <- `staging.raw_orders.amount` <- `erp.SAP.ZSDT0010.NETWR`
- 자동화 도구: **Apache Atlas**(분산), **DataHub**(LinkedIn), **OpenMetadata**, **Marquez**(Lyft)

- **📢 섹션 요약 비유**: 데이터 품질 감리는 **'건강검진 5단계'**와 같다. 1단계 문진표(메타데이터), 2단계 기초혈액검사(프로파일링), 3단계 CT/MRI(제약/무결성), 4단계 전문의 소견(비즈니스 규칙), 5단계 종합 리포트(DQ-Score). 각 단계가 독립적이지만 **누락 시 오진**으로 이어진다.

---

## Ⅲ. 비교 및 연결

데이터 품질 진단 기법들은 상호보완적이며, 목적·규모·자동화 수준에 따라 적절히 조합해야 한다. 또한 데이터 거버넌스, 마스터데이터 관리(MDM), 데이터 카탈로그 등 인접 영역
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 594 / 600

<- **이전**: [593. 클라우드 환경 감리 가상화 검증](/studynote/11_design_supervision/06_exam_summary/593_cloud_environment_audit_virtualization/)
**다음**: [595. 보안 감리 제로 트러스트 적합성 평가](/studynote/11_design_supervision/06_exam_summary/595_security_audit_zero_trust_fitness/) ->

---
