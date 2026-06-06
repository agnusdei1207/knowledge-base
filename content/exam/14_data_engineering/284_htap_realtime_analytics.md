---
title: "Real-time Analytics HTAP Hybrid Transaction"
date: "2026-05-09"
tags:
  - "studynote-data-engineering"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: HTAP(Hybrid Transactional/Analytical Processing)는 Gartner가 2014년 명명한 아키텍처 패러다임으로, OLTP(온라인 트랜잭션 처리)와 OLAP(온라인 분석 처리)를 별도 시스템으로 분리하지 않고 **단일 데이터 사본(Single Source of Truth)** 위에서 동시 실행하기 위해, 이원화된 스토리지 엔진(예: TiKV 행 저장 + TiFlash 컬럼너 저장)을 Raft Learner, MVCC 스냅샷, CDC(Change Data Capture) 등으로 동기화하는 구조다.
> 2. **가치**: 전통적인 ETL 기반 T+1(일배치) 의사결정 지연을 수 초~수십 초 단위로 축소하고, 데이터 사일로 제거를 통해 분석-트랜잭션 정합성 불일치를 원천 차단한다. PingCAP 내부 사례 기준 TiDB+TiFlash는 동일 클러스터에서 약 100배 압축률의 컬럼너 분석을 1초 이내 P99 지연으로 수행하면서 OLTP QPS 저하를 5% 이내로 유지한다.
> 3. **판단 포인트**: 트레이드오프의 핵심은 (a) **단일 엔진 메모리형(HANA, Oracle In-Memory)** vs **분산 이원 엔진형(TiDB, SingleStore)** vs **CDC 결합형(MySQL+Debezium+ClickHouse)** 중 어느 통합 수준을 채택할지, (b) **리소스 경합**을 워크로드 격리(노드/리전 레벨) vs 우선순위 큐로 해결할지, (c) **읽기 일관성(SI/RC)** vs **분석 처리량** 사이에서 CDC lag SLA를 어디에 둘지다.

---

## Ⅰ. 개요 및 필요성

전통적인 데이터 아키텍처는 **OLTP 시스템(예: MySQL, PostgreSQL)**과 **OLAP 시스템(예: Teradata, Redshift, BigQuery)**을 물리적으로 분리하고, 이를 **ETL(Extract-Transform-Load)** 파이프라인으로 연결하는 것이 표준이었다. 이 구조는 Kimball/Inmon 데이터웨어하우스 방법론 하에서 수십 년간 안정적으로 운영되어 왔으나, 다음의 한계가 2010년대 들어 폭발적으로 부각되었다.

1. **시간 지연(Time-to-Insight)**: 일배치 ETL 기준 D+1(익일) 의사결정은 실시간 사기 탐지, IoT 이상 감지, 동적 가격 결정 등 **밀리초~초 단위** 응답이 필요한 비즈니스에 사용 불가능했다.
2. **데이터 사일로와 정합성**: OLTP-DW 양쪽에 동일 데이터가 이중 저장되어 동기화 누락 시 *Dual-Write Inconsistency* 문제가 발생한다(예: 주문 트랜잭션은 반영되었으나 DW 합계는 미반영).
3. **운영 비용과 복잡도**: ETL 스케줄러(Airflow), CDC(Kafka Connect + Debezium), ODS(Operational Data Store), Staging/Aggregation 레이어를 별도 운영해야 하므로 클러스터·라이선스·모니터링 비용이 N배로 증가한다.
4. **스키마 진화 부담**: 양쪽 저장소의 스키마를 동기화하기 위한 Avro/Schema Registry 운영이 필요하며, 컬럼 추가/삭제 시 다운타임 또는 dual-write 코드가 강제된다.

HTAP는 2014년 Gartner가 처음 명명한 개념으로, **단일 시스템에서 트랜잭션과 분석 워크로드를 모두 처리**함으로써 위 문제를 해결한다. 초기 구현은 SAP HANA(2010), Oracle Database In-Memory(2014) 같은 **메모리 가속형 단일 엔진**이었으며, 이후 2017년 TiDB/Greenplum 6(Polymorphic Storage), 2018년 SingleStore(Universal Storage), 2021년 Google AlloyDB(Columnar Engine) 등 **클라우드 네이티브 분산형**으로 세대교체가 일어났다.

```text
[기존 이원화 아키텍처 vs HTAP 아키텍처 비교]

  (A) Traditional ETL (T+1)                  (B) HTAP (Real-time)
  +------------+  ETL(T+1)  +------------+   +--------------------------+
  |   OLTP     | ---------> |    DW      |   |      HTAP System         |
  |  MySQL/    |            | Redshift/  |   | +----------+ +--------+  |
  |  Oracle    | <--------- | Snowflake  |   | |  OLTP    |↔|  OLAP  |  |
  +------------+  BI Query  +------------+   | | Engine   | | Engine |  |
        ^                      ^             | | (TiKV /  | |(TiFlash|  |
        |                      |             | | Rowstore)| |/Colstr)|  |
   +----+----+           +----+----+        | +----+-----+ +---+----+  |
   | Web/App |           | BI Tool |        |      +-----+-----+       |
   +---------+           +---------+        |        Single KV         |
                                            |        Storage          |
   - 지연: 수시간~1일                       |   - 지연: <1초            |
   - 사일로: 2곳 이상                       |   - 사일로: 0             |
   - 정합성: eventual/주기적                |   - 정합성: 강한/준강한   |
   +----------------------------+            +--------------------------+
```

- **📢 섹션 요약 비유**: 이원화 아키텍처는 "주방(OLTP)과 창고(OLAP)를 따로 두고 매일 새벽 트럭으로 재고를 옮기는 식당"이고, HTAP는 "주방 안에서 즉시 회계 보고서까지 뽑아내는 통합 키친"이다. 트럭이 늦으면 음식(데이터)이 상하고, 옮기는 동안 양이 어긋난다.

---

## Ⅱ. 아키텍처 및 핵심 원리

HTAP는 구현 방식에 따라 **① 메모리형 단일 엔진, ② 분산 이원 엔진, ③ CDC 결합형**의 세 가지 아키텍처 계열로 분류된다. 각각의 동작 원리를 실제 제품 사례로 깊이 있게 살펴본다.

### 가. 메모리형 단일 엔진 (SAP HANA, Oracle Database In-Memory)

SAP HANA는 **컬럼너 + 로우 스토어를 메모
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 284 / 300

<- **이전**: [283. 데이터 웨어하우스 모더나이제이션 클라우드 이관 (DW Modernization Cloud Migration)](/studynote/14_data_engineering/05_exam_keywords/283_dw_modernization/)
**다음**: [285. 멀티모달 데이터 처리 통합 분석 (Multimodal Data Processing Unified Analytics)](/studynote/14_data_engineering/05_exam_keywords/285_multimodal_data/) ->

---
