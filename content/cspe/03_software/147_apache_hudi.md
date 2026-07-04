---
title: "Apache Hudi"
date: "2026-07-04"
tags:
  - "cspe-software"
weight: 147
---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **개요**: 데이터 레이크 상에서 빈번한 업데이트(Upsert)와 삭제(Delete)를 빠르게 처리하기 위해 고안된 오픈 테이블 포맷이다.
- **왜 필요한가**: 일반적인 레이크(Parquet)는 파일 단위라서 한 줄만 수정하고 싶어도 파일 전체를 다시 써야 한다. Hudi는 이를 해결하여 스트리밍 데이터의 지연 없는 갱신을 가능하게 한다.
- **핵심 직관**: 원래 책(데이터 파일)을 통째로 새로 인쇄해야만 오타를 고칠 수 있었다면, Hudi는 책은 그대로 두고 오타 수정용 포스트잇(로그 파일)만 잔뜩 붙여둔 뒤, 나중에 한가할 때 책을 다시 인쇄(Compaction)하는 방식이다.

## 핵심 용어 정리

| 용어/표기 | 의미 | 비유·예 |
|:---|:---|:---|
| Apache Hudi | Hadoop Upserts Deletes and Incrementals (Uber 개발) | 수정이 잦은 장부 |
| Copy On Write (CoW) | 데이터를 쓸 때마다 이전 파일을 통째로 다시 써서 최신 상태로 만드는 저장 방식 | 매번 새 책 인쇄 |
| Merge On Read (MoR) | 데이터 쓸 때는 로그(포스트잇)만 남기고, 읽을 때 원본과 합쳐서 보여주는 방식 | 포스트잇 + 원본 책 |
| Upsert | Update(수정) + Insert(삽입). 있으면 수정하고 없으면 새로 넣는 연산 | 상태 동기화의 핵심 |
| Incremental Pull | 마지막으로 읽은 이후에 '새로 변경된 데이터'만 쏙 뽑아오는 기능 | 새로 붙은 포스트잇만 읽기 |

## 깊이 이해
- **배경·문제의식**: Uber처럼 실시간으로 드라이버의 위치와 승객 상태가 초단위로 바뀌는 환경에서는, 데이터 레이크(HDFS)에 데이터를 넣는 족족 갱신(Update)이 일어나야 했다. 하지만 기존 Parquet 포맷은 'Append(추가)'만 잘 되고 'Update'는 파일 전체를 다시 써야 해서 엄청난 병목이 생겼다.
- **작동 원리**: Hudi는 'MoR(Merge On Read)' 테이블을 제공한다. 데이터가 갱신되면 무거운 Parquet 파일을 다시 쓰지 않고, 가벼운 Avro 기반의 행(Row) 단위 로그 파일에 변경 사항만 빠르게 기록한다. 이후 쿼리가 들어오면 Parquet 원본과 Avro 로그를 즉시 합쳐서(Merge) 보여주고, 주기적으로 백그라운드에서 둘을 병합(Compaction)하여 새 Parquet 파일을 만든다.
- **비유**: CoW(Copy On Write)가 '보고서에 오타 하나 날 때마다 전체를 다시 프린트하는 꼼꼼한 직원'이라면, MoR(Merge On Read)은 '일단 오타 부분에 포스트잇만 붙여두고 회의에 들어가는 실용적인 직원'이다.
- **구체 예시**: 드라이버 A의 상태가 '운행 중'에서 '완료'로 바뀌면, Hudi는 기존 Parquet 파일의 드라이버 A 레코드를 덮어쓰지 않고, 델타 로그에 '드라이버 A: 완료'라는 이벤트만 추가하여 쓰기 지연을 1초 미만으로 낮춘다.
- **흔한 오해·주의점**: Hudi, Delta Lake, Iceberg는 모두 테이블 포맷이지만 출발점이 다르다. Hudi는 '빠른 Upsert/스트리밍'에서 출발했고, Iceberg는 '거대한 테이블의 쿼리 최적화'에서, Delta Lake는 'Spark 기반 파이프라인 안전성'에서 출발했다.

## 연결 개념
- 변경 데이터 캡처 (CDC) — DB의 변경 내역을 스트리밍으로 쏠 때 Hudi가 이를 받아 레이크에 Upsert함
- Lambda 아키텍처 — Hudi를 쓰면 스트리밍/배치 파이프라인을 통합할 수 있어 람다 아키텍처를 대체함
- 오픈 테이블 포맷 비교 — Hudi vs Iceberg vs Delta Lake

---

# 📝 【답안용】 시험 답안 템플릿

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데이터 레이크 환경에서 레코드 수준의 갱신(Update), 삽입(Insert), 삭제(Delete)를 최적화하여 스트리밍 처리에 특화된 오픈 테이블 포맷이다.
> 2. **가치**: 기존 HDFS/S3의 파일 단위 덮어쓰기 한계를 극복하고, MoR(Merge On Read) 방식을 통해 쓰기 지연(Write Latency)을 최소화하여 실시간 분석을 지원한다.
> 3. **판단 포인트**: CDC(Change Data Capture) 연동 등 잦은 레코드 업데이트가 발생하는 스트리밍 데이터 파이프라인 구축 시 가장 강력한 성능을 발휘한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 스트리밍 데이터 레이크의 한계 및 해결책 이해 | Upsert/Delete 지원, CoW vs MoR 비교, Incremental Pull | 다른 포맷(Iceberg 등)과의 차별점인 MoR 최적화와 스트리밍 특성 누락 |

> 요약: Hudi가 어떻게 데이터 레이크에서 고비용의 Update 연산을 저비용으로 처리하여 실시간 데이터 동기화를 이뤄내는지 서술해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: Apache Hudi(Hadoop Upserts Deletes and Incrementals)는 데이터 레이크 스토리지에서 트랜잭션, 레코드 수준 갱신/삭제, 증분 처리를 지원하는 오픈 테이블 포맷이다.
- 배경: 기존 컬럼형 파일 포맷(Parquet)은 추가(Append)는 효율적이나 갱신(Update) 시 전체 파일을 재작성해야 하여 스트리밍 환경에서 심각한 쓰기 병목 유발함
- 필요성: RDBMS의 변경 사항(CDC)을 데이터 레이크에 실시간 지연 없이 동기화(Upsert)하고, 분석 쿼리의 일관성을 보장할 스토리지 계층 필수

---

## Ⅱ. 구조 및 구성요소

```text
Stream Data (CDC) -> Hudi Writer -> Hudi Table (Timeline / Data Files) -> Query Engine (Spark/Presto)
                                      |
                                      +-> Base File (Parquet)
                                      +-> Log File (Avro, 변경분)
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Timeline (트랜잭션) | 테이블에서 발생한 모든 동작(커밋, 클린 등)을 시간 순서대로 기록 | 스냅샷 및 증분 처리의 기준 |
| Base File | 데이터를 안정적이고 빠르게 읽기 위한 컬럼형 원본 파일 | Apache Parquet 포맷 사용 |
| Log File (Delta) | Base File 생성 이후의 변경(Upsert) 사항을 임시로 기록한 행형 파일 | Apache Avro 포맷 사용 |
| Compactor | 백그라운드에서 Base File과 Log File을 병합하여 새로운 Base File 생성 | 읽기 성능 최적화를 위한 과정 |

> 요약: Hudi는 무거운 Base File(Parquet)과 가벼운 Log File(Avro)을 분리하여 쓰기 성능과 읽기 성능의 트레이드오프를 관리한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
데이터 인입 (Upsert) -> MoR 기반 로그 기록 -> 쿼리 시 Merge 수행 -> 백그라운드 Compaction
```

- 1단계 [레코드 인입]: CDC 등으로부터 Update/Insert 스트리밍 데이터가 Hudi 인덱스를 통해 기존 파일과 매핑됨
- 2단계 [로그 기록(MoR)]: 전체 파일을 덮어쓰지 않고, 변경된 레코드만 Avro 포맷의 Log File에 즉시(Low-Latency) 기록(Append)함
- 3단계 [읽기 시점 Merge]: 클라이언트가 쿼리를 요청하면, 최신 Timeline을 기준으로 Parquet 원본과 Avro 로그를 메모리상에서 병합하여 반환
- 4단계 [Compaction]: 백그라운드 프로세스가 비동기적으로 Log 파일들을 Parquet Base 파일로 병합하여 쿼리 성능(읽기 속도) 복구

> 요약: Hudi의 MoR 방식은 쓰기 시점의 비용을 읽기 시점과 백그라운드 작업으로 지연시켜 스트리밍 데이터의 실시간 적재를 가능하게 한다.

---

## Ⅳ. 특징
- 고속 Upsert / Delete: 레코드 수준의 인덱싱(Bloom Filter, HBase 등)을 통해 갱신 대상 파일을 빠르게 찾고 수정
- Copy on Write (CoW)와 Merge on Read (MoR) 테이블 유형 분리 제공: 읽기 성능이 중요하면 CoW, 쓰기 지연 최소화가 중요하면 MoR 선택
- Incremental Pull (증분 쿼리): 마지막으로 쿼리한 시점(Timeline) 이후 변경된 데이터만 스트리밍처럼 당겨올(Pull) 수 있어 ETL 효율 극대화
- 동시성 제어 및 원자성: Timeline 기반의 낙관적 동시성 제어(OCC)를 통해 여러 Writer가 안전하게 동일 테이블에 기록

> 요약: Hudi는 RDBMS와 유사한 갱신/삭제 유연성을 제공하면서도 객체 스토리지의 저비용을 유지하는 스트리밍 친화적 포맷이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | Copy on Write (CoW) 테이블 | Merge on Read (MoR) 테이블 | 선택 기준 |
|:---|:---|:---|:---|
| 데이터 쓰기 | 매 갱신마다 Parquet 파일 전체 재작성 | Avro 로그 파일에 변경 레코드만 추가 기록 | 쓰기 지연(Latency) 허용도 |
| 데이터 읽기 | 순수 Parquet만 읽으므로 속도 매우 빠름 | Parquet + Avro 병합 수행으로 속도 상대적 느림 | 조회 쿼리 성능 중요도 |
| 최적 유스케이스 | 일 단위 배치 ETL, 읽기 중심 분석 테이블 | 실시간 스트리밍 적재, CDC 기반 실시간 동기화 | 데이터 인입 주기 및 갱신 빈도 |

> 요약: 읽기 성능이 최우선이면 CoW를, 쓰기 지연(스트리밍)이 최우선이면 MoR을 선택하여 워크로드에 맞게 튜닝한다.

**리스크·대응 (기본 불릿):**
- Compaction 지연: MoR 테이블에서 로그 파일 누적으로 읽기 성능(Merge 오버헤드) 급감 → 비동기 Compaction 주기 단축 및 리소스 증대 (지표: 로그 파일 개수 및 병합 시간)
- 작은 파일(Small Files) 문제: 스트리밍 적재 시 작은 Parquet 파일 양산으로 I/O 저하 → 쓰기 시점의 Auto File Sizing 연동 및 Clustering 작업 스케줄링 (지표: 평균 파일 사이즈)
- 인덱스 오버헤드: Upsert 대상 레코드를 찾는 인덱스 로드 시간 증가 → 레코드 수가 매우 많을 경우 인덱스를 메모리가 아닌 별도 외부 저장소(HBase 등)로 오프로딩

**도입 후 점검 지표 (기본 불릿):**
- 성능/효율: 원본 DB 갱신 후 Hudi 테이블 적재까지의 End-to-End 지연 시간 p95 3분 이내 — 스트리밍 지연 모니터링
- 품질/운영: Incremental Pull을 통한 증분 ETL 실행 시간 감소율 — 기존 배치 스캔(Full Scan) 소요 시간과 비교

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 실시간 CDC 레이크하우스 구축: Debezium 이벤트 스트림을 Kafka로 받아 Hudi MoR 테이블에 실시간 Upsert하여 RDBMS 상태를 1분 내로 레이크에 동기화
2. GDPR 준수를 위한 개인정보 삭제: 잊힐 권리(Right to be forgotten) 요청 시 Hudi의 하드 삭제(Hard Delete) API를 호출하여 비용 효율적으로 특정 유저 레코드 파기
3. 증분(Incremental) 데이터 파이프라인 연계: 메달리온 아키텍처(Bronze -> Silver -> Gold) 구성 시, 매번 전체를 재가공하지 않고 Hudi의 Incremental Pull로 변경분만 다음 계층으로 전파

**결론:**
- 기술사 판단: 변경(Update/Delete)이 빈번하게 발생하는 스트리밍 데이터와 CDC 연동 아키텍처에서는, 쓰기 비용을 줄여주는 MoR 기능을 갖춘 Hudi가 가장 적합한 테이블 포맷이다.
- 향후 방향: 최근 Hudi, Iceberg, Delta Lake 간 상호 변환 없이 읽을 수 있게 하는 Onetable(Apache XTable) 프로젝트가 등장하며 테이블 포맷 간 장벽이 허물어지고 있다.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 | Ⅴ·Ⅵ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "설명하시오" | Hudi Timeline 메커니즘과 Base/Log 구조 | CoW vs MoR 비교표 및 Incremental Pull 기능 |
| 비교형 | "오픈 테이블 포맷과 비교하시오" | Upsert 중심의 MoR 최적화 원리 | 스트리밍 적합성 평가 및 CDC 연동 사례 |
| 방안형 | "데이터 레이크 갱신 문제 해결 방안" | Parquet의 Append 제약과 Hudi 갱신 흐름 | Compaction 운영 방안 및 GDPR 삭제 통제 방안 |
