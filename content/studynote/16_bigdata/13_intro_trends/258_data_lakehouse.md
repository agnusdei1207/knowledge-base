+++
title = "046. 데이터 레이크하우스 — Data Lakehouse"
date = 2026-04-05

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

> **핵심 인사이트**
> 1. [데이터 레이크하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/)([Data Lakehouse](/knowledge-base/studynote/12_it_management/05_security_compliance/210_data_lakehouse_delta_lake/))는 [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)의 유연성·저비용과 [데이터 웨어하우스](/knowledge-base/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/)의 ACID·[성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)·거버넌스를 결합한 하이브리드 아키텍처 — [Databricks](/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/)·Delta Lake가 선도하며, 클라우드 스토리지(S3, ADLS) 위에서 [OLAP](/knowledge-base/studynote/12_it_management/05_security_compliance/316_olap/) 수준의 분석 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 달성한다.
> 2. [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/)의 핵심 기술은 [오픈 테이블 포맷](/knowledge-base/studynote/14_data_engineering/01_infrastructure/054_open_table_format_iceberg_delta_hudi/)([Delta Lake](/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/), [Apache Iceberg](/knowledge-base/studynote/16_bigdata/07_data_lake/148_apache_iceberg/), [Apache Hudi](/knowledge-base/studynote/16_bigdata/07_data_lake/149_apache_hudi/)) — [파케이](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)([Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 위에 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 레이어를 추가해 ACID [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)·[스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 진화·타임 트래블(Time Travel)을 지원하며, 벤더 잠금 없이 [상호운용성](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/287_interoperability_tactics/)을 보장한다.
> 3. [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/)는 [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)→웨어하우스 이중 구조의 비효율을 해결 — 동일 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 레이크와 웨어하우스 양쪽에 중복 저장·[동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)하는 비용과 복잡성을 제거하며, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 사이언스(ML/[AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/))와 BI 분석을 단일 플랫폼에서 통합 지원한다.

---

## Ⅰ. [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) 등장 배경



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">데이터 아키텍처 진화:</div>
<div class="kb-diagram-note">1세대: 데이터 웨어하우스 (DW)</div>
<div class="kb-diagram-note">정형 데이터 + SQL + ACID</div>
<div class="kb-diagram-note">장점: 고성능 분석, 데이터 품질</div>
<div class="kb-diagram-note">단점: 비싸고, 비정형 데이터 미지원</div>
<div class="kb-diagram-note">예: Teradata, Oracle DW</div>
<div class="kb-diagram-note">2세대: 데이터 레이크</div>
<div class="kb-diagram-note">원시 데이터 + Hadoop/S3</div>
<div class="kb-diagram-note">장점: 저비용, 모든 데이터 유형</div>
<div class="kb-diagram-note">단점:</div>
<div class="kb-diagram-tree-item" style="--depth:1">ACID 없음 → 데이터 일관성 문제</div>
<div class="kb-diagram-tree-item" style="--depth:1">성능 낮음</div>
<div class="kb-diagram-tree-item" style="--depth:1">거버넌스 부재 ("데이터 늪")</div>
<div class="kb-diagram-tree-item" style="--depth:1">BI 도구 연동 어려움</div>
<div class="kb-diagram-note">예: Hadoop HDFS, S3 기반 레이크</div>
<div class="kb-diagram-note">현실: 이중 구조 비효율</div>
<div class="kb-diagram-note">레이크 ← ETL → 웨어하우스</div>
<div class="kb-diagram-note">문제:</div>
<div class="kb-diagram-note">데이터 중복 (2배 스토리지)</div>
<div class="kb-diagram-note">동기화 지연 (레이크 → DW ETL 지연)</div>
<div class="kb-diagram-note">ML: 레이크에서 학습</div>
<div class="kb-diagram-note">BI: 웨어하우스에서 쿼리</div>
<div class="kb-diagram-note">→ 두 팀 간 데이터 불일치</div>
<div class="kb-diagram-note">3세대: 레이크하우스</div>
<div class="kb-diagram-note">레이크 + 웨어하우스 통합</div>
<div class="kb-diagram-note">오픈 포맷 위에 ACID + 거버넌스</div>
<div class="kb-diagram-note">장점:</div>
<div class="kb-diagram-note">ML/AI + BI 단일 플랫폼</div>
<div class="kb-diagram-note">벤더 독립 (오픈 포맷)</div>
<div class="kb-diagram-note">비용 효율 (S3 기반)</div>
<div class="kb-diagram-note">실시간 + 배치 통합</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/)는 복합 쇼핑몰 — 재래시장(레이크: 다양하지만 지저분)과 백화점(웨어하우스: 정갈하지만 비쌈)을 합친 것. 다양하면서도 체계적, 저렴하면서도 품질 있는!

---

## Ⅱ. [오픈 테이블 포맷](/knowledge-base/studynote/14_data_engineering/01_infrastructure/054_open_table_format_iceberg_delta_hudi/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">오픈 테이블 포맷 (Open Table Format):</div>
<div class="kb-diagram-note">공통 구조:</div>
<div class="kb-diagram-note">클라우드 스토리지 (S3, GCS, ADLS)</div>
<div class="kb-diagram-note">파케이(Parquet) 파일 + 메타데이터 레이어</div>
<div class="kb-diagram-note">→ ACID, 타임 트래블, 스키마 관리</div>
<div class="kb-diagram-note">Delta Lake (Databricks, 2019):</div>
<div class="kb-diagram-note">트랜잭션 로그: JSON 기반</div>
<div class="kb-diagram-note">ACID: O</div>
<div class="kb-diagram-note">타임 트래블: O (버전 기반)</div>
<div class="kb-diagram-note">스키마 진화: O</div>
<div class="kb-diagram-note">통합: Spark, Delta Sharing</div>
<div class="kb-diagram-note">DELETE: 물리 삭제 대신 소프트 삭제 → Vacuum</div>
<div class="kb-diagram-note">MERGE INTO: Upsert (중요 기능)</div>
<div class="kb-diagram-note">예:</div>
<div class="kb-diagram-note">MERGE INTO target t</div>
<div class="kb-diagram-note">USING source s ON t.id = s.id</div>
<div class="kb-diagram-note">WHEN MATCHED THEN UPDATE SET t.value = s.value</div>
<div class="kb-diagram-note">WHEN NOT MATCHED THEN INSERT *</div>
<div class="kb-diagram-note">Apache Iceberg (Netflix, 2018):</div>
<div class="kb-diagram-note">메타데이터: Avro + Parquet</div>
<div class="kb-diagram-note">스냅샷 기반: 각 커밋 = 스냅샷</div>
<div class="kb-diagram-note">Partition Evolution: 스키마 변경 없이 파티셔닝 변경</div>
<div class="kb-diagram-note">Row-Level Delete: 효율적 개별 행 삭제</div>
<div class="kb-diagram-note">통합: Trino, Spark, Flink, Hive</div>
<div class="kb-diagram-note">Trino + Iceberg = 고성능 오픈 레이크하우스</div>
<div class="kb-diagram-note">Apache Hudi (Uber, 2016):</div>
<div class="kb-diagram-note">Incremental Processing 특화</div>
<div class="kb-diagram-note">COW (Copy-On-Write): 읽기 최적화</div>
<div class="kb-diagram-note">MOR (Merge-On-Read): 쓰기 최적화</div>
<div class="kb-diagram-note">통합: Spark, Presto</div>
<div class="kb-diagram-note">사용: Uber, Robinhood (실시간 업데이트)</div>
<div class="kb-diagram-note">비교:</div>
<div class="kb-diagram-note">Delta Lake: Databricks 생태계 강함</div>
<div class="kb-diagram-note">Iceberg: 가장 넓은 엔진 지원 (중립적)</div>
<div class="kb-diagram-note">Hudi: 실시간 증분 처리 특화</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [오픈 테이블 포맷](/knowledge-base/studynote/14_data_engineering/01_infrastructure/054_open_table_format_iceberg_delta_hudi/)은 스마트 서류 정리함 — [파케이](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(서류)에 이력 관리(ACID), 수정 기록(타임 트래블), 목차([메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/))를 추가. 어떤 직원([쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 엔진)도 읽을 수 있어요!

---

## Ⅲ. [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) 핵심 기능



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">레이크하우스 주요 기능:</div>
<div class="kb-diagram-note">1. ACID 트랜잭션:</div>
<div class="kb-diagram-note">동시 읽기/쓰기 안전</div>
<div class="kb-diagram-note">예: 두 작업 동시 실행</div>
<div class="kb-diagram-tree-item" style="--depth:1">파이프라인 A: 새 데이터 추가</div>
<div class="kb-diagram-tree-item" style="--depth:1">BI 도구: 현재 데이터 쿼리</div>
<div class="kb-diagram-note">→ 격리 보장 (쿼리가 중간 상태 보지 않음)</div>
<div class="kb-diagram-note">2. 타임 트래블 (Time Travel):</div>
<div class="kb-diagram-note">이전 버전 데이터 조회</div>
<div class="kb-diagram-note">예 (Delta Lake):</div>
<div class="kb-diagram-note">SELECT * FROM sales VERSION AS OF 5</div>
<div class="kb-diagram-note">SELECT * FROM sales TIMESTAMP AS OF '2024-01-01'</div>
<div class="kb-diagram-note">활용:</div>
<div class="kb-diagram-tree-item" style="--depth:1">실수로 삭제된 데이터 복구</div>
<div class="kb-diagram-tree-item" style="--depth:1">데이터 감사 (언제 어떤 값이었나)</div>
<div class="kb-diagram-tree-item" style="--depth:1">재현 가능한 ML 실험 (동일 데이터셋)</div>
<div class="kb-diagram-note">3. 스키마 진화 (Schema Evolution):</div>
<div class="kb-diagram-note">기존 데이터 마이그레이션 없이 컬럼 추가/변경</div>
<div class="kb-diagram-note">레거시 레코드: 새 컬럼 = NULL 처리</div>
<div class="kb-diagram-note">하위 호환 유지</div>
<div class="kb-diagram-note">4. 스트리밍 + 배치 통합:</div>
<div class="kb-diagram-note">동일 테이블에 실시간 + 배치 쓰기</div>
<div class="kb-diagram-note">예:</div>
<div class="kb-diagram-tree-item" style="--depth:1">Kafka → Flink → Delta Lake (스트리밍)</div>
<div class="kb-diagram-tree-item" style="--depth:1">Spark 배치 → 동일 Delta 테이블</div>
<div class="kb-diagram-note">→ BI가 하나의 테이블에서 모두 쿼리</div>
<div class="kb-diagram-note">5. DML (Data Manipulation Language):</div>
<div class="kb-diagram-note">UPDATE, DELETE, MERGE</div>
<div class="kb-diagram-note">→ 레이크에서 불가능하던 기능 지원</div>
<div class="kb-diagram-note">→ CDC (Change Data Capture) 적용 가능</div>
<div class="kb-diagram-note">6. 데이터 거버넌스:</div>
<div class="kb-diagram-note">Unity Catalog (Databricks): 통합 카탈로그</div>
<div class="kb-diagram-note">Apache Atlas: 오픈소스 메타데이터</div>
<div class="kb-diagram-note">Column-Level Security</div>
<div class="kb-diagram-note">Data Lineage (데이터 계보)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) 기능은 스마트 은행 통장 — ACID(안전한 거래), 타임 트래블(거래 내역 조회), [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 진화(통장 항목 추가). 단순 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 저장에서 완전한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리로!

---

## Ⅳ. [Databricks](/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/) [Lakehouse](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) 플랫폼



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Databricks Lakehouse Platform:</div>
<div class="kb-diagram-note">아키텍처:</div>
<div class="kb-diagram-note">클라우드 스토리지 (S3/ADLS/GCS)</div>
<div class="kb-diagram-note">Delta Lake (오픈 포맷)</div>
<div class="kb-diagram-note">Unity Catalog (거버넌스)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Delta Engine</div><div class="kb-diagram-cell">(쿼리 엔진)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(고성능 Spark)</div></div>
<div class="kb-diagram-note">ML/AI BI/SQL</div>
<div class="kb-diagram-note">(MLflow) (Databricks SQL)</div>
<div class="kb-diagram-note">Delta Engine:</div>
<div class="kb-diagram-note">Spark 기반 최적화 쿼리 엔진</div>
<div class="kb-diagram-note">10~100× 성능 향상 (표준 Spark 대비)</div>
<div class="kb-diagram-note">Photon: 네이티브 벡터화 C++ 엔진</div>
<div class="kb-diagram-note">MLflow:</div>
<div class="kb-diagram-note">ML 라이프사이클 관리</div>
<div class="kb-diagram-note">실험 추적, 모델 레지스트리</div>
<div class="kb-diagram-note">Feature Store</div>
<div class="kb-diagram-note">Databricks SQL:</div>
<div class="kb-diagram-note">BI 도구용 서버리스 SQL 웨어하우스</div>
<div class="kb-diagram-note">Tableau, Power BI 연결</div>
<div class="kb-diagram-note">Unity Catalog:</div>
<div class="kb-diagram-note">통합 메타데이터 카탈로그</div>
<div class="kb-diagram-note">3-레벨 이름공간: Catalog.Schema.Table</div>
<div class="kb-diagram-note">Column-Level ACL</div>
<div class="kb-diagram-note">Data Lineage</div>
<div class="kb-diagram-note">경쟁 제품:</div>
<div class="kb-diagram-note">Snowflake: 유사 통합 플랫폼 (독점 포맷)</div>
<div class="kb-diagram-note">BigQuery: Google의 서버리스 분석</div>
<div class="kb-diagram-note">Synapse Analytics: Azure 통합 플랫폼</div>
<div class="kb-diagram-note">차이: Databricks = 오픈 포맷 강조</div>
<div class="kb-diagram-note">Snowflake = 성능·관리 편의성 강조</div>
</div>
</div>



> 📢 **섹션 요약 비유**: Databricks는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 올인원 — 스토리지([Delta Lake](/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/)), [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)(SQL), ML([MLflow](/knowledge-base/studynote/10_ai/02_dl_architecture_new/180_mlflow/)), 거버넌스(Unity)를 하나로 묶은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼 슈퍼마켓. 벤더 잠금 없이!

---

## Ⅴ. 실무 시나리오 — 금융사 [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) 전환



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">핀테크 기업 레이크하우스 전환:</div>
<div class="kb-diagram-note">기존 구조 (이중 구조):</div>
<div class="kb-diagram-note">S3 레이크: 원시 거래 데이터, ML 학습</div>
<div class="kb-diagram-note">Redshift 웨어하우스: BI 분석</div>
<div class="kb-diagram-note">문제:</div>
<div class="kb-diagram-note">ETL 파이프라인 유지 비용: 월 500만원</div>
<div class="kb-diagram-note">레이크 → DW 지연: 3시간</div>
<div class="kb-diagram-note">데이터 불일치: 레이크 vs DW 수치 다름</div>
<div class="kb-diagram-note">Redshift 비용: 월 2,000만원</div>
<div class="kb-diagram-note">레이크하우스 전환 (Databricks + Delta Lake):</div>
<div class="kb-diagram-note">아키텍처:</div>
<div class="kb-diagram-note">S3 → Delta Lake 테이블</div>
<div class="kb-diagram-note">Databricks Spark: 처리 + ML</div>
<div class="kb-diagram-note">Databricks SQL: BI 쿼리</div>
<div class="kb-diagram-note">Unity Catalog: 거버넌스</div>
<div class="kb-diagram-note">핵심 마이그레이션:</div>
<div class="kb-diagram-note">Redshift 테이블 → Delta Lake 변환</div>
<div class="kb-diagram-note">Redshift 쿼리 → Databricks SQL 마이그레이션</div>
<div class="kb-diagram-note">타임 트래블 활용:</div>
<div class="kb-diagram-note">규제 감사: "2023년 12월 말 데이터 상태는?"</div>
<div class="kb-diagram-note">SELECT * FROM transactions</div>
<div class="kb-diagram-note">TIMESTAMP AS OF '2023-12-31 23:59:59'</div>
<div class="kb-diagram-note">스트리밍 통합:</div>
<div class="kb-diagram-note">실시간 사기 탐지:</div>
<div class="kb-diagram-note">Kafka → Structured Streaming → Delta Lake</div>
<div class="kb-diagram-note">→ ML 모델 실시간 스코어링</div>
<div class="kb-diagram-note">→ 결과 Delta 테이블에 저장</div>
<div class="kb-diagram-note">결과:</div>
<div class="kb-diagram-note">ETL 파이프라인: 제거 (단일 플랫폼)</div>
<div class="kb-diagram-note">데이터 신선도: 3시간 → 5분</div>
<div class="kb-diagram-note">데이터 불일치: 0 (단일 소스)</div>
<div class="kb-diagram-note">월 인프라 비용: 2,500만원 → 1,200만원</div>
<div class="kb-diagram-note">ML 학습 속도: 4배 향상 (Delta Cache)</div>
<div class="kb-diagram-note">규제 감사 대응 시간: 2주 → 2시간</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 금융사 [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/)는 단일 장부 — 레이크(창고 장부)와 웨어하우스(회계 장부) 이중으로 기록하다가, 하나의 스마트 장부([레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/))로 통합. 비용 반, 시간 1/36!

---

## 📌 관련 개념 맵

```
데이터 레이크하우스
+-- 오픈 테이블 포맷
|   +-- Delta Lake (Databricks)
|   +-- Apache Iceberg (Netflix)
|   +-- Apache Hudi (Uber)
+-- 핵심 기능
|   +-- ACID 트랜잭션
|   +-- 타임 트래블
|   +-- 스키마 진화
|   +-- 스트리밍+배치 통합
+-- 플랫폼
|   +-- Databricks Lakehouse
|   +-- Snowflake (유사)
+-- 관련 기술
    +-- Parquet (저장 포맷)
    +-- Spark (처리)
    +-- Unity Catalog (거버넌스)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[데이터 웨어하우스 (1990s)]
정형 데이터, 고비용
SQL + ACID
      |
      v
[Hadoop 데이터 레이크 (2006~)]
빅데이터, 저비용
ACID 없음, 성능 낮음
      |
      v
[이중 구조 문제 (2010s)]
레이크 + DW 동시 운영
중복, 불일치 문제
      |
      v
[Delta Lake 오픈소스 (2019)]
Databricks, ACID+레이크
레이크하우스 개념 구체화
      |
      v
[Iceberg, Hudi 경쟁 (2020~)]
오픈 포맷 경쟁
벤더 중립성 강조
      |
      v
[현재: 레이크하우스 주류화]
Databricks, Snowflake, BigQuery
AI+BI 통합 플랫폼 수렴
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/)는 복합 쇼핑몰 — 재래시장(레이크: 뭐든 있지만 복잡)과 백화점(웨어하우스: 정갈하지만 비쌈)을 하나로 합쳤어요!
2. 타임 트래블은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 되감기 — 어제 실수로 지운 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)? "어제 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 보여줘!" 한 줄로 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/). [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에도 타임머신이 있어요!
3. 오픈 포맷은 표준 [USB](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/359_usb/) — [Delta Lake](/knowledge-base/studynote/16_bigdata/07_data_lake/147_delta_lake/)/Iceberg/Hudi 모두 같은 [파케이](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/). 어떤 도구(Spark, Trino, Flink)로도 읽을 수 있는 표준 규격!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 258 / 262

← **이전**: [045. 데이터 패브릭 — Data Fabric](/knowledge-base/studynote/16_bigdata/13_intro_trends/257_data_fabric/)
**다음**: [047. 실시간 OLAP — ClickHouse·Druid·Pinot·StarRocks](/knowledge-base/studynote/16_bigdata/13_intro_trends/259_realtime_olap/) →

---
