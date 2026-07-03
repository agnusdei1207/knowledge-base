---
title: "Apache Hudi (Apache Hudi)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 147
---

# 📖 【암기용】 개념 완전 이해

> 목적: Apache Hudi를 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: Apache Hudi는 데이터 레이크 위에서 **record key 기반 upsert·delete**와 **incremental query**(변경분만 조회)를 지원하는 오픈 테이블 포맷이다.
- **왜 필요한가**: 순수 레이크는 파일을 append하는 데는 강하지만, CDC처럼 "특정 레코드 하나를 갱신·삭제"하려면 파일 전체를 재작성해야 한다. Hudi는 레코드를 키로 식별해 해당 레코드가 속한 파일만 갱신하도록 만든다.
- **핵심 직관**: 매일 전체 회원 명부를 새로 인쇄하는 대신, 회원번호(record key)를 기준으로 바뀐 카드만 교체하는 카드형 인덱스 시스템이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| Record Key | 레코드를 유일하게 식별하는 키(PK) — Hudi upsert의 **정체성**을 이루는 핵심 | 회원번호 |
| Precombine Field | 같은 키의 레코드가 여럿일 때 "어느 것이 최신인지" 고르는 기준 컬럼(보통 timestamp) | 여러 이력 카드 중 발급일이 가장 최근인 카드를 채택 |
| Timeline | commit·delta commit·compaction·clean 등 테이블에 가해진 모든 행위를 순서대로 기록한 이력 | 회원 카드 시스템의 전체 작업 로그 |
| File Group | 하나의 논리 레코드 그룹이 속하는 base file(+log file) 묶음, file id로 식별 | 특정 구역을 담당하는 서랍 하나 |
| Index | record key가 어느 file group에 있는지 빠르게 찾는 조회 구조(Bloom filter, metadata table 등) | 회원번호로 서랍 위치를 즉시 알려주는 색인 카드 |
| Copy-on-Write (CoW) | upsert 시 base file(Parquet)을 바로 재작성 — 쓰기 비용↑, 읽기 빠름 | 카드를 수정할 때마다 새 카드를 통째로 다시 인쇄 |
| Merge-on-Read (MoR) | upsert를 log file(델타)에 append만 하고, 읽을 때 base+log를 병합 — 쓰기 빠름, 읽기 시 병합 비용 | 카드는 그대로 두고 "정정 스티커"만 붙였다가, 열람 시 같이 보여줌 |
| Compaction | MoR의 log file들을 base file에 병합해 log 누적을 정리하는 작업 | 쌓인 정정 스티커를 새 카드로 정식 반영 |
| Incremental Query | 특정 시점 이후 변경된 레코드만 조회하는 쿼리 모드 | "지난 커밋 이후 바뀐 회원만" 필터링해서 보기 |

## 깊이 이해

### 왜 upsert가 어려운 문제였나 — 수치 예제
- 예: 파티션 하나에 파일 1,000개(각 256MB, 총 256GB)가 있는데 CDC로 들어온 변경 레코드는 그중 5,000건뿐(변경률 0.5% 수준)이라 하자. 전통적 append-only 레이크는 "어느 파일에 있는지 모르니" 파티션 전체(256GB)를 다시 읽고 다시 써야 할 수 있다.
- Hudi는 Index로 5,000건의 record key가 어느 file group(예: 20개 파일, 5GB)에 속하는지 먼저 찾아, 그 20개 파일만 갱신한다 — 재작성 범위가 256GB에서 5GB로, 약 1/50 수준으로 줄어든다.

### CoW vs MoR 선택 — 워크드 비교
- **CoW**: 위 예에서 20개 파일(5GB)을 매번 Parquet로 통째 재작성한다. 쓰기 지연은 크지만(재작성 비용) 읽기는 순수 Parquet라 빠르다(별도 병합 불필요). 배치성 CDC 반영(예: 1시간마다)에 적합하다.
- **MoR**: 같은 변경분(5,000건)을 log file(예: Avro, 수십 MB)에 append만 한다. 쓰기는 수 초 내로 매우 빠르지만, real-time view로 읽을 때는 base file + 누적된 log file을 병합해야 하므로 log가 쌓일수록(예: compaction 없이 delta commit 50회 누적) 읽기 지연이 커진다. 초 단위 스트리밍 반영에 적합하다.
- 판별 기준: 쓰기 빈도가 분 단위 이하로 잦고 읽기 지연을 어느 정도 감내 가능하면 MoR, 조회 성능이 최우선이고 배치 주기가 시간 단위면 CoW를 선택한다.

### Timeline과 commit — 예제로 이해
- CDC 이벤트가 5분마다 batch로 들어온다면, 매 batch가 timeline에 하나의 (delta) commit으로 기록된다. `.commit`(CoW) 또는 `.deltacommit`(MoR) 파일이 timeline 디렉터리에 쌓이고, 각 commit은 어떤 file group이 갱신됐는지 기록한다.
- Downstream 파이프라인은 "마지막으로 처리한 커밋 시각 이후"만 incremental query로 가져가면 되므로 매번 전체 테이블을 다시 읽을 필요가 없다 — 예: 하루 1억 건 테이블에서 변경분만 5만 건이면 조회량이 약 1/2,000로 줄어든다.

### Compaction 지연이 만드는 문제 — 수치 예제
- MoR에서 compaction을 안 돌리고 하루 288개(5분마다) delta commit이 log file로 계속 쌓이면, 하나의 file group을 읽을 때 base file 1개 + log file 288개를 병합해야 해서 조회 시간이 log 수에 비례해 늘어난다.
- compaction을 4시간마다(하루 6회) 실행하도록 스케줄링하면 병합해야 할 log 수가 최대 48개 수준으로 줄어 읽기 지연을 통제할 수 있다 — 이것이 compaction backlog 관리다.

### 비유와 오해
- **비유**: 매일 전체 회원 명부를 새로 찍어내지 않고, 회원번호(record key) 기준으로 바뀐 카드만 교체·삭제·조회하는 카드형 재고 시스템이다.
- **오해 1**: Hudi가 스트리밍 엔진이다 — 아니다. Hudi는 테이블 포맷·라이브러리이고, 실제 쓰기·읽기는 Spark나 Flink 엔진이 수행한다.
- **오해 2**: upsert만 쓰면 끝이다 — 아니다. precombine 기준이 잘못되면(예: timestamp 대신 도착 순서로 판단) 늦게 도착한 오래된 이벤트가 최신 값을 덮어써 데이터가 역행할 수 있다. 순서 보장·idempotent 처리가 함께 필요하다.

## 연결 개념
- CDC: Hudi upsert와 incremental query의 주요 입력원
- Delta Lake: `_delta_log` 트랜잭션 로그 기반 대안 포맷 (145에서 상세)
- Apache Iceberg: 다중 엔진·snapshot 중심 대안 포맷 (146에서 상세)

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Hudi 답안은 upsert 기능만 쓰지 말고 CoW/MoR, timeline, incremental query, compaction 선택 기준을 제시해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Apache Hudi는 레이크 파일에 record-level upsert/delete와 commit timeline을 제공하는 오픈 테이블 포맷이다.
> 2. **가치**: CDC 기반 변경 데이터를 레이크에 반영하고 downstream은 incremental query로 변경분만 소비한다.
> 3. **판단 포인트**: 읽기 지연, 쓰기 빈도, compaction 비용에 따라 Copy-on-Write와 Merge-on-Read를 선택한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Hudi 구조 이해 | record key, timeline, file group, index | 단순 upsert 라이브러리로 설명 |
| 테이블 타입 선택 | CoW vs MoR, compaction, incremental query | 읽기·쓰기 trade-off 누락 |
| CDC 적용 판단 | precombine, idempotent write, delete 처리 | 중복 이벤트와 순서 보장 미기재 |

> 요약: Hudi는 변경 데이터 처리에 초점을 둔 포맷이며, CoW/MoR 선택과 compaction 운영이 답안의 중심이다.

---

## Ⅰ. 개요 및 필요성

- 개요: Apache Hudi는 데이터 레이크용 변경 처리 테이블 포맷이다.
- 배경: CDC와 스트리밍 적재가 많은 환경은 객체 스토리지 파일의 upsert, delete, incremental query가 필요하다.
- 필요성: record key 기반 변경 처리로 전체 재작성 없이 데이터 레이크 변경분을 관리한다.

---

## Ⅱ. 구조 및 구성요소

```text
CDC / Batch Input -> Hudi Writer -> Timeline -> File Group / Index -> Query Engine
                              +-> CoW / MoR Table
                              +-> Compaction / Cleaning
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Record Key | 레코드 식별 | PK, precombine field |
| Timeline | commit, delta commit, compaction 이력 | incremental query 기준 |
| File Group | base file과 log file 묶음 | MoR에서 log merge |
| Index | key 위치 탐색 | Bloom, metadata table |

> 요약: Hudi는 record key와 timeline을 중심으로 파일 그룹 내 변경분을 추적한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
CDC 이벤트 수신 -> record key / precombine 적용 -> index 조회
-> base file 또는 log file 기록 -> timeline commit -> incremental query 제공
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 입력 이벤트에서 key와 최신성 기준 추출 | key null 0건 |
| 2 | index로 기존 레코드 위치 확인 | lookup latency |
| 3 | CoW는 base file 재작성, MoR은 log file 기록 | write amplification |
| 4 | timeline commit 후 compaction/cleaning 수행 | compaction backlog |

> 요약: Hudi는 키 기반으로 변경 대상 위치를 찾고, 테이블 타입에 따라 base file 재작성 또는 log file 병합을 수행한다.

---

## Ⅳ. 특징

| 구분 | 일반 레이크 적재 | Apache Hudi | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 변경 처리 | append 후 재처리 | upsert/delete 지원 | CDC 반영 주기 5분 이하 |
| 조회 방식 | 전체 스캔 | snapshot, read optimized, incremental | downstream 변경분 소비 |
| 테이블 타입 | 단일 파일 모델 | CoW, MoR 선택 | 읽기 p95 vs 쓰기 처리량 |
| 운영 | 파일 정리 수동 | compaction, cleaning | backlog 임계치 설정 |

> 요약: Hudi는 변경 빈도가 높은 레이크 테이블에 적합하나 compaction 지연과 index 비용을 관리해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | Apache Hudi | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | append-only Parquet | record key+timeline | CDC upsert 필수 |
| 비용/성능 | 전체 파티션 재작성 | key 기반 부분 반영 | 변경률 20% 이하 |
| 운영/위험 | 단순 적재 | index, compaction 운영 | compaction backlog 통제 가능 |

> 요약: Hudi는 CDC 중심 변경 반영과 incremental pipeline이 필요한 경우 선택 가치가 크다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 중복·역전 이벤트 | CDC 순서 불일치 | precombine timestamp, idempotent write | duplicate key 0건 |
| 조회 지연 | MoR log file 누적 | compaction schedule | log file count, p95 query |
| 인덱스 비용 | 대규모 key lookup | metadata table, partition pruning | index lookup p95 |

> 요약: Hudi 리스크는 이벤트 최신성, log file 누적, index 비용이며 각각 별도 지표가 필요하다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 쓰기 | commit latency 5분 이하 | Hudi timeline |
| 조회 | read optimized p95 10초 이하 | query profile |
| 운영 | compaction backlog 3회 이하 | Hudi cleaner/compactor metric |

> 요약: Hudi 운영 성공은 commit 지연, 조회 p95, compaction backlog로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. CDC 원천은 record key와 precombine timestamp를 정의하고 duplicate key 0건을 목표로 idempotent write 구현
2. 조회 중심 테이블은 CoW, 쓰기 빈도 높은 테이블은 MoR로 분리하고 compaction backlog 3회 이하 유지
3. incremental query를 downstream ETL에 적용해 전체 스캔을 변경분 처리로 전환하고 timeline 기반 재처리 절차 수립

**결론 (2줄):**
- 기술사 판단: CDC upsert와 incremental query가 핵심이면 Hudi, 다중 엔진 개방성과 파티션 진화가 중심이면 Iceberg 검토
- 향후 방향: Hudi는 스트리밍 레이크하우스와 CDC 파이프라인에서 변경 데이터 운영 포맷으로 활용 범위가 확대

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Apache Hudi를 설명하시오" | record key, timeline, CoW/MoR 흐름 | append-only 대비 upsert·incremental 차이 |
| 요구사항 명시형 | "Delta/Iceberg와 비교", "CDC 설계", "운영 방안" | precombine, compaction, incremental query | 읽기·쓰기·compaction 선택 기준 |

> 요약: 설명형은 Hudi 내부 구조, 설계형은 CDC와 CoW/MoR 선택 조건으로 전환한다.
