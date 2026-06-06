---
title: "Data Observability Anomaly Detection SLO"
date: "2026-05-09"
tags:
  - "studynote-data-engineering"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데이터 자산의 5대 관측 차원(**Freshness, Volume, Schema, Quality, Lineage**)을 SLI로 정량화하고, 통계·ML 기반 이상탐지(Statistical / ML / Time-Series)를 통해 SLO(예: 1시간 내 99.5% 신선도)와 **Error Budget Burn Rate**로 데이터 신뢰성을 엔지니어링하는 운영 체계이다. Monte Carlo, Bigeye, Soda, Great Expectations, Elementary, Datafold 등의 도구가 OpenLineage/OpenTelemetry 기반 메타데이터 패브릭 위에서 상호 운용된다.
> 2. **가치**: 업계 사례(Monte Carlo 2024 State of Data Quality 보고서) 기준 데이터 인시던트 **MTTD를 평균 4.2시간 -> 12분, MTTR을 8.1시간 -> 47분**으로 단축하며, 데이터 다운타임 50~80% 감소, 컴플라이언스(SOX/PIPA) 감사 자동화, 연간 의사결정 오류 60~80% 절감의 정량 효과를 창출한다.
> 3. **판단 포인트**: ① **임계치 기반(Rule)** vs **통계분포(Z-score/IQR/MAD)** vs **딥러닝(AE/LSTM/Prophet)** 알고리즘 트레이드오프, ② **배치(일 1회)** vs **Near-Real-Time(1~5분)** 탐지 빈도 vs 비용, ③ False Positive 관리(쿨다운·휴면기간·Snooze), ④ **Data Contract**(data Mesh)·**리니지**(DataHub/Unity Catalog)·**카탈로그** 통합 깊이, ⑤ Tier-1/2/3 등급별 SLO 차별화 정책이 핵심 의사결정 축이다.

---

## Ⅰ. 개요 및 필요성

데이터 레이크·레이크하우스(Iceberg/Delta/Hudi)와 MPP 웨어하우스(Snowflake/BigQuery/Redshift/Databricks), 그리고 SaaS 애플리케이션(CRM/ERP/Marketing) 간 데이터 파이프라인이 폭증하면서 **"데이터는 있는데 신뢰할 수 없는"** 현상이 빈번해졌다. 전통적인 ETL 스키마 검증과 dbt 단위 테스트만으로는 **분포 드리프트(Distribution Drift), 신규 컬럼 등장, 지연 도착(Late Arriving Data), 소스 시스템 오류** 같은 무형의 결함을 사전에 탐지하기 어렵다.

Google SRE 워크북이 정의한 **SLI/SLO/Error Budget** 프레임워크를 데이터 영역으로 확장한 것이 **데이터 관측가능성 이상탐지 SLO**이다. 이는 메타데이터(스키마, 리니지, 통계), 프로파일(샘플), 로그(쿼리 패턴), 트레이스(OpenLineage 이벤트)를 통합 수집·분석하여 데이터 자산의 **가용성·정확성·신선도·완전성**을 4대 SLI로 측정하고, 통계적·ML적 이상탐지로 자동 평가한 뒤 SLO 위반 시 **Multi-Window Multi-Burn-Rate** 알림을 통해 PagerDuty/Jira로 라우팅한다.

```text
+---------------------------------------------------------------------+
|         데이터 관측가능성 이상탐지 SLO의 진화적 배경과 필요성        |
+---------------------------------------------------------------------+

  [전통적 ETL 시대]                [현재: Data+AI 시대]
  -----------------                ---------------------
  - 스키마 매칭만 검증             - 분포 드리프트, 신규 컬럼,
  - 배치 야간 검증                   Late Arrival, Silent Corruption
  - 야간 실패 -> 아침 인지            - 실시간 의사결정 -> 즉시 영향
  - 단일 시스템                      - 수십~수백 다운스트림 의존성
  - SQL 단위 테스트                  - ML·GenAI까지 다운스트림 전파
       |                                   |
       +----------- 패러다임 전환 ----------+
                          |
                          v
         +------------------------------------+
         |  "데이터 다운타임(Data Downtime)"  |
         |   = 정확하지만 신뢰 못하는 데이터  |
         |   =
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 293 / 300

<- **이전**: [292. 데이터 레이크하우스 메달리온 아키텍처 (Data Lakehouse Medallion Architecture)](/studynote/14_data_engineering/05_exam_keywords/292_lakehouse_medallion/)
**다음**: [294. 자동 ML 하이퍼파라미터 NAS 탐색 (AutoML Hyperparameter NAS Search)](/studynote/14_data_engineering/05_exam_keywords/294_automl_hyperparameter/) ->

---
