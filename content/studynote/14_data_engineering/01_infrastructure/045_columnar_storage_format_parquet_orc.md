+++
title = "045. 컬럼형 저장 형식 — Parquet & ORC"
date = 2026-04-05

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

> **핵심 인사이트**
> 1. 컬럼형 저장 형식([Columnar Storage](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/234_columnar_storage_parquet_orc/) Format)은 행(Row) 대신 열(Column) 단위로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 저장해 분석 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)의 I/O를 극적으로 줄이는 빅데이터 핵심 기술 — 수백만 행에서 특정 열 5개만 조회할 때 행 기반은 전체 행을 읽지만, 컬럼형은 해당 열만 읽는다.
> 2. Apache Parquet와 ORC(Optimized Row Columnar)는 현재 빅데이터 생태계의 양대 표준 — Parquet는 Spark·다중 언어 생태계에서 강점, ORC는 [Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/) 최적화와 ACID [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 지원에서 강점이며, 두 형식 모두 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)·술어 푸시다운(Predicate Pushdown)을 지원한다.
> 3. [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)/ORC의 핵심 최적화 기법은 Row Group + Column Chunk + [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) + 통계(Min/Max/[Bloom Filter](/knowledge-base/studynote/12_it_management/02_itsm_itil/061_bloomfilter/)) — [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 엔진이 Row Group 통계를 이용해 불필요한 Row Group 자체를 건너뛰는 "스킵핑"이 성능의 핵심이다.

---

## Ⅰ. 행 기반 vs 컬럼 기반



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">저장 형식 비교:</div>
<div class="kb-diagram-note">샘플 데이터 (3행 × 4열):</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">id</div><div class="kb-diagram-cell">name</div><div class="kb-diagram-cell">age</div><div class="kb-diagram-cell">salary</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1</div><div class="kb-diagram-cell">Alice</div><div class="kb-diagram-cell">30</div><div class="kb-diagram-cell">5000</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2</div><div class="kb-diagram-cell">Bob</div><div class="kb-diagram-cell">25</div><div class="kb-diagram-cell">4000</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3</div><div class="kb-diagram-cell">Carol</div><div class="kb-diagram-cell">35</div><div class="kb-diagram-cell">6000</div></div>
<div class="kb-diagram-note">행 기반 (Row-Oriented):</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">저장:</div><div class="kb-diagram-node">1,Alice,30,5000</div><div class="kb-diagram-node">2,Bob,25,4000</div><div class="kb-diagram-node">3,Carol,35,6000</div></div>
<div class="kb-diagram-note">장점: 행 단위 CRUD 빠름 (OLTP)</div>
<div class="kb-diagram-note">단점: 전체 열 다 읽어야 함 (분석)</div>
<div class="kb-diagram-note">컬럼 기반 (Column-Oriented):</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">저장:</div><div class="kb-diagram-node">1,2,3</div><div class="kb-diagram-node">Alice,Bob,Carol</div><div class="kb-diagram-node">30,25,35</div><div class="kb-diagram-node">5000,4000,6000</div></div>
<div class="kb-diagram-note">장점: 필요한 열만 읽음 (OLAP)</div>
<div class="kb-diagram-note">압축률 높음 (같은 타입 데이터)</div>
<div class="kb-diagram-note">쿼리 차이:</div>
<div class="kb-diagram-note">SELECT AVG(salary) FROM employees</div>
<div class="kb-diagram-note">행 기반: id, name, age, salary 모두 읽음 (100%)</div>
<div class="kb-diagram-note">컬럼형: salary 열만 읽음 (25%)</div>
<div class="kb-diagram-note">1억 행, 100열 테이블:</div>
<div class="kb-diagram-note">행 기반: 5개 열 쿼리 → 100열 전부 읽음</div>
<div class="kb-diagram-note">컬럼형: 5개 열 쿼리 → 5열만 읽음 (95% I/O 절감)</div>
<div class="kb-diagram-note">압축 효율:</div>
<div class="kb-diagram-note">컬럼 내 데이터 = 동일 타입 + 유사 값</div>
<div class="kb-diagram-note">salary열: 4000, 5000, 4500, 5200...</div>
<div class="kb-diagram-note">→ 델타 인코딩: +0, +1000, -500, +700</div>
<div class="kb-diagram-note">→ RLE: 같은 값 반복 (부서 코드 등)</div>
<div class="kb-diagram-note">→ 압축률 5~10× 일반적</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 컬럼형은 책장 정리법 — 행 기반은 책 한 권씩(행) 정리, 컬럼형은 같은 색 책(열)끼리 정리. "빨간 책 몇 권?" 물으면 빨간 칸만 보면 OK!

---

## Ⅱ. Apache [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Apache Parquet:</div>
<div class="kb-diagram-note">Apache Foundation 오픈소스 (2013)</div>
<div class="kb-diagram-note">Twitter + Cloudera 공동 개발</div>
<div class="kb-diagram-note">파일 구조:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Magic Number (PAR1)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Row Group 1</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Column Chunk A</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Page 1, Page 2, ...</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Column Chunk B</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Page 1, Page 2, ...</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Row Group 2</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">...</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Footer (메타데이터)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">스키마, 통계(Min/Max)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Row Group 오프셋</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Magic Number (PAR1)</div></div>
<div class="kb-diagram-note">핵심 구성:</div>
<div class="kb-diagram-note">Row Group: 기본 128MB~1GB</div>
<div class="kb-diagram-note">→ 병렬 처리 단위</div>
<div class="kb-diagram-note">Column Chunk: 열 데이터 블록</div>
<div class="kb-diagram-note">Page: 인코딩·압축 단위 (1MB)</div>
<div class="kb-diagram-note">인코딩:</div>
<div class="kb-diagram-note">Dictionary Encoding: 반복 값 사전화</div>
<div class="kb-diagram-note">RLE (Run-Length Encoding): 연속 값 압축</div>
<div class="kb-diagram-note">Bit Packing: 정수 소형 비트 패킹</div>
<div class="kb-diagram-note">Delta Encoding: 연속 증가 값</div>
<div class="kb-diagram-note">압축 코덱:</div>
<div class="kb-diagram-note">Snappy (기본): 빠름, 적당한 압축률</div>
<div class="kb-diagram-note">GZIP: 높은 압축률, 느림</div>
<div class="kb-diagram-note">LZ4: 초고속, 중간 압축률</div>
<div class="kb-diagram-note">ZSTD: 빠름 + 높은 압축률 (권장)</div>
<div class="kb-diagram-note">술어 푸시다운:</div>
<div class="kb-diagram-note">Row Group Footer 통계:</div>
<div class="kb-diagram-note">min_value=1000, max_value=5000</div>
<div class="kb-diagram-note">WHERE salary &gt; 6000:</div>
<div class="kb-diagram-note">→ 이 Row Group 건너뜀! (I/O 절감)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: Parquet는 목차 있는 백과사전 — Row Group = 챕터, 목차(Footer 통계)로 "이 챕터에 찾는 내용 있나?" [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/). 없으면 챕터 통째로 건너뜀!

---

## Ⅲ. Apache ORC



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Apache ORC (Optimized Row Columnar):</div>
<div class="kb-diagram-note">Hive 프로젝트에서 탄생 (2013)</div>
<div class="kb-diagram-note">Hortonworks 개발</div>
<div class="kb-diagram-note">파일 구조:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">ORC Header (Magic: ORC)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Stripe 1</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Index Data</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Row Data (컬럼별)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Stripe Footer</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Stripe 2</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">...</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">File Footer</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Stripe 목록</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">스키마</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">통계</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Postscript</div></div>
<div class="kb-diagram-note">Stripe = Parquet Row Group (기본 256MB)</div>
<div class="kb-diagram-note">ORC 특화 기능:</div>
<div class="kb-diagram-note">1. ACID 트랜잭션:</div>
<div class="kb-diagram-note">Hive 3.0+ 지원</div>
<div class="kb-diagram-note">INSERT, UPDATE, DELETE 지원</div>
<div class="kb-diagram-note">(Parquet는 기본 append-only)</div>
<div class="kb-diagram-note">2. Bloom Filter:</div>
<div class="kb-diagram-note">특정 값 존재 여부 빠른 확인</div>
<div class="kb-diagram-note">WHERE id = 12345 → Bloom Filter로 Stripe 스킵</div>
<div class="kb-diagram-note">3. 경량 인덱스:</div>
<div class="kb-diagram-note">Row Index (10,000행마다 통계)</div>
<div class="kb-diagram-note">Bloom Filter Index</div>
<div class="kb-diagram-note">4. LLAP (Live Long and Process):</div>
<div class="kb-diagram-note">Hive LLAP과 통합 최적화</div>
<div class="kb-diagram-note">인메모리 캐시</div>
<div class="kb-diagram-note">ORC 적합 환경:</div>
<div class="kb-diagram-note">Hive 기반 데이터 웨어하우스</div>
<div class="kb-diagram-note">UPDATE/DELETE 필요한 SCD(천천히 변하는 차원)</div>
<div class="kb-diagram-note">Hive ACID 트랜잭션</div>
</div>
</div>



> 📢 **섹션 요약 비유**: ORC는 [Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/) 최적화 선반 — [Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/) 창고([Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/) 웨어하우스)에 최적화된 정리 방식. 특히 물건 교체(UPDATE/ACID)가 필요할 때 강점!

---

## Ⅳ. [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) vs ORC vs CSV



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">비교표:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">항목</div><div class="kb-diagram-cell">CSV</div><div class="kb-diagram-cell">Parquet</div><div class="kb-diagram-cell">ORC</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">저장 방식</div><div class="kb-diagram-cell">행 기반</div><div class="kb-diagram-cell">컬럼 기반</div><div class="kb-diagram-cell">컬럼 기반</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">압축 지원</div><div class="kb-diagram-cell">없음</div><div class="kb-diagram-cell">있음</div><div class="kb-diagram-cell">있음</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">스키마 내장</div><div class="kb-diagram-cell">없음</div><div class="kb-diagram-cell">있음</div><div class="kb-diagram-cell">있음</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">읽기 성능 (분석)</div><div class="kb-diagram-cell">낮음</div><div class="kb-diagram-cell">높음</div><div class="kb-diagram-cell">높음</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">ACID 트랜잭션</div><div class="kb-diagram-cell">없음</div><div class="kb-diagram-cell">없음(기본)</div><div class="kb-diagram-cell">있음 (Hive)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">파싱 오버헤드</div><div class="kb-diagram-cell">없음</div><div class="kb-diagram-cell">있음</div><div class="kb-diagram-cell">있음</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">생태계 지원</div><div class="kb-diagram-cell">범용</div><div class="kb-diagram-cell">Spark 최적</div><div class="kb-diagram-cell">Hive 최적</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Bloom Filter</div><div class="kb-diagram-cell">없음</div><div class="kb-diagram-cell">있음(선택)</div><div class="kb-diagram-cell">있음</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">복잡 타입 지원</div><div class="kb-diagram-cell">없음</div><div class="kb-diagram-cell">중첩 스키마</div><div class="kb-diagram-cell">중첩 스키마</div></div>
<div class="kb-diagram-note">선택 가이드:</div>
<div class="kb-diagram-note">CSV: 소규모 데이터, 호환성 최우선</div>
<div class="kb-diagram-note">Parquet: Spark, Presto/Trino, Athena, Iceberg</div>
<div class="kb-diagram-note">ORC: Hive, Hive ACID 트랜잭션 필요 시</div>
<div class="kb-diagram-note">현재 트렌드:</div>
<div class="kb-diagram-note">Parquet → Apache Iceberg, Delta Lake 표준</div>
<div class="kb-diagram-note">ORC → Hive 기반 환경</div>
<div class="kb-diagram-note">Delta Lake: Parquet 기반 + ACID 보완</div>
<div class="kb-diagram-note">Apache Iceberg: Parquet/ORC/Avro 지원</div>
<div class="kb-diagram-note">성능 벤치마크 (1억 행, 10열 중 3열 쿼리):</div>
<div class="kb-diagram-note">CSV: 100s</div>
<div class="kb-diagram-note">Parquet: 8s (ZSTD 압축, 술어 푸시다운)</div>
<div class="kb-diagram-note">ORC: 10s (ZLIB 압축, Bloom Filter)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/) vs ORC는 삼성 vs LG 가전 — 둘 다 훌륭하지만, Spark 집(생태계)에는 Parquet가, [Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/) 집에는 ORC가 잘 맞아요!

---

## Ⅴ. 실무 시나리오 — [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) 최적화



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">전자상거래 데이터 레이크 최적화:</div>
<div class="kb-diagram-note">초기 상황:</div>
<div class="kb-diagram-note">S3에 CSV 파일 적재</div>
<div class="kb-diagram-note">Athena 쿼리: 일 주문 분석 → 10~30분</div>
<div class="kb-diagram-note">비용: 쿼리당 $50~200 (스캔 비용)</div>
<div class="kb-diagram-note">문제 진단:</div>
<div class="kb-diagram-note">Athena = Presto 기반 (S3 스캔)</div>
<div class="kb-diagram-note">CSV: 스키마 없음, 압축 없음, 전체 스캔</div>
<div class="kb-diagram-note">일 주문 테이블: 5억 행, 50열</div>
<div class="kb-diagram-note">주요 쿼리: 5열만 사용, 날짜 필터링</div>
<div class="kb-diagram-note">최적화 전략:</div>
<div class="kb-diagram-note">1. CSV → Parquet 변환 (ZSTD 압축):</div>
<div class="kb-diagram-note">Glue ETL로 일배치 변환</div>
<div class="kb-diagram-note">결과:</div>
<div class="kb-diagram-note">CSV: 500GB/일 → Parquet: 80GB/일 (84% 압축)</div>
<div class="kb-diagram-note">2. Hive 파티셔닝:</div>
<div class="kb-diagram-note">S3 키: s3://bucket/orders/year=2024/month=01/day=15/</div>
<div class="kb-diagram-note">WHERE order_date = '2024-01-15'</div>
<div class="kb-diagram-note">→ 해당 파티션만 스캔</div>
<div class="kb-diagram-note">3. Row Group 크기 최적화:</div>
<div class="kb-diagram-note">Row Group = 256MB (대용량 배치 쿼리 최적)</div>
<div class="kb-diagram-note">4. 술어 푸시다운 최적화:</div>
<div class="kb-diagram-note">컬럼 순서 = 카디널리티 높은 것 먼저</div>
<div class="kb-diagram-note">→ Bloom Filter 효과 극대화</div>
<div class="kb-diagram-note">결과:</div>
<div class="kb-diagram-note">쿼리 시간: 10~30분 → 30~90초</div>
<div class="kb-diagram-note">스캔 비용: $50~200 → $2~8 (96% 절감)</div>
<div class="kb-diagram-note">월 Athena 비용: 500만원 → 20만원</div>
<div class="kb-diagram-note">추가: Delta Lake 전환으로 ACID 지원</div>
<div class="kb-diagram-note">(일 데이터 수정 필요 케이스 처리)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/) 최적화는 창고 정리 — CSV(무분류 박스) → [Parquet](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)(카테고리별 투명 박스). "1월 주문"만 찾을 때 해당 칸만 보면 OK. 비용 96% 절감!

---

## 📌 관련 개념 맵

```
컬럼형 저장 형식
+-- Apache Parquet
|   +-- Row Group / Column Chunk / Page
|   +-- 압축 (Snappy, ZSTD)
|   +-- 술어 푸시다운
+-- Apache ORC
|   +-- Stripe / Index / Bloom Filter
|   +-- Hive ACID
+-- 비교
|   +-- CSV (행 기반)
|   +-- Avro (직렬화)
+-- 상위 기술
    +-- Delta Lake (Parquet + ACID)
    +-- Apache Iceberg (Parquet/ORC)
    +-- Apache Hudi
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[RC File / SequenceFile (2000s)]
Hadoop 초기 컬럼형 시도
제한적 기능
      |
      v
[Parquet + ORC 등장 (2013)]
Hadoop 생태계 표준 컬럼형
Twitter/Hortonworks 주도
      |
      v
[Delta Lake / Iceberg / Hudi (2016~)]
컬럼형 + ACID + 스냅샷
레이크하우스 패러다임
      |
      v
[현재: 오픈 테이블 포맷]
Apache Iceberg 표준 부상
Parquet 기반 멀티엔진
AWS, Snowflake, Databricks 지원
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 컬럼형은 같은 종류끼리 묶기 — CSV가 "1번 사람 모든 정보"를 묶으면, Parquet는 "모든 사람의 나이"를 묶어요. 나이만 필요할 때 엄청 빠르죠!
2. 술어 푸시다운은 목차 이용하기 — "1월 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)"를 찾을 때 목차(Row Group 통계) 보고 12월 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 통째로 건너뛰어요!
3. Parquet는 Spark 친구, ORC는 [Hive](/knowledge-base/studynote/05_database/04_transactions_concurrency/544_hive/) 친구 — 같은 기능이지만 각자 잘 맞는 생태계가 달라요. 쓰는 도구에 맞게 선택!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 45 / 258

← **이전**: [044. 카파 아키텍처 — 단일 스트리밍 레이어](/knowledge-base/studynote/14_data_engineering/01_infrastructure/044_kappa_architecture_single_streaming_layer/)
**다음**: [046. LSM 트리 — Log-Structured Merge-Tree](/knowledge-base/studynote/14_data_engineering/01_infrastructure/046_lsm_tree_log_structured_merge/) →

---
