---
title: "B-Tree vs LSM-Tree 비교 (B-Tree vs LSM-Tree)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 110
---

# 📖 【암기용】 개념 완전 이해

> 목적: B-Tree와 LSM-Tree를 처음 보는 사람도 읽기·쓰기 증폭과 OLTP·쓰기 집약 워크로드 선택 기준을 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: B-Tree는 제자리 갱신 중심의 정렬 인덱스, LSM-Tree는 메모리 쓰기 후 디스크 정렬 파일로 내려보내는 로그 구조 인덱스이다.
- **왜 필요한가**: 읽기 위주 OLTP는 낮은 point lookup 지연이 필요하고, 로그·IoT·메시지 저장소는 초당 수십만 건 쓰기를 흡수해야 한다. 구조 선택이 읽기·쓰기 비용을 바꾼다.
- **핵심 직관**: B-Tree는 가나다 순 파일철을 바로 고쳐 끼우는 방식, LSM-Tree는 새 문서를 임시함에 모았다가 정렬된 묶음으로 합치는 방식이다.

## 깊이 이해
- **배경·문제의식**: 디스크는 랜덤 쓰기보다 순차 쓰기에 유리하다. B-Tree는 leaf page를 찾아 제자리 갱신하며 page split이 생긴다. LSM-Tree는 WAL에 기록하고 MemTable에 쓴 뒤 SSTable로 flush하여 순차 쓰기를 늘린다.
- **작동 원리**: LSM은 WAL, MemTable, Immutable MemTable, SSTable, Compaction 계층으로 구성된다. 읽기는 MemTable과 여러 SSTable을 확인하고 Bloom Filter로 불필요한 파일 탐색을 줄인다. Compaction은 중복 key와 tombstone을 병합·정리한다.
- **비유**: 우체국에서 편지를 매번 주소 순 서랍에 꽂는 것은 B-Tree, 하루치 편지를 모아 정렬한 뒤 기존 묶음과 병합하는 것은 LSM-Tree이다.
- **구체 예시**: MySQL InnoDB는 B+Tree 기반으로 OLTP point read와 range scan에 적합하다. RocksDB, Cassandra는 LSM 기반으로 write-heavy workload에서 sequential write와 compaction을 활용한다.
- **흔한 오해·주의점**: LSM은 쓰기 경로가 짧지만 compaction으로 write amplification이 발생한다. 읽기 경로는 여러 level 조회와 tombstone 처리로 tail latency가 증가할 수 있다.

## 연결 개념
- WAL — 장애 복구를 위한 선기록 로그
- SSTable — 정렬된 불변 디스크 파일
- Compaction — LSM level 병합과 삭제 표시 정리

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: B-Tree와 LSM-Tree 비교는 자료구조 설명이 아니라 read/write amplification과 workload 적합성 판단이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: B-Tree는 page 기반 제자리 갱신 정렬 구조, LSM-Tree는 WAL+MemTable+SSTable+Compaction으로 구성된 로그 구조 병합 트리이다.
> 2. **가치**: B-Tree는 point read·range scan 지연을 낮추고, LSM-Tree는 순차 쓰기와 배치 병합으로 쓰기 처리량을 확보한다.
> 3. **판단 포인트**: read amplification, write amplification, compaction debt, tail latency, OLTP vs write-heavy workload를 기준으로 선택한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 저장 엔진 구조 비교 이해 확인 | B-Tree page, WAL, MemTable, SSTable, Compaction | B-Tree와 LSM을 단순 인덱스 종류로만 설명 |
| 워크로드별 선택 기준 확인 | OLTP read, write-heavy, range scan, tail latency | LSM을 쓰기 비용 0으로 표현 |
| 운영 리스크 판단 확인 | compaction, tombstone, cache, Bloom Filter | compaction 부하와 읽기 증폭 누락 |

> 요약: 이 문제는 저장 엔진 구조를 읽기·쓰기 증폭과 운영 지표로 비교하는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

B-Tree와 LSM-Tree는 DB 저장 엔진의 대표 인덱스 구조이다. B-Tree는 정렬 page를 제자리 갱신하고, LSM-Tree는 메모리 쓰기 후 정렬 파일로 flush·compaction한다. 워크로드의 읽기·쓰기 비율에 따라 선택 기준이 달라진다.

---

## Ⅱ. 구조 및 구성요소

```text
B-Tree: Root -> Branch -> Leaf Page -> Row
LSM-Tree: WAL -> MemTable -> Immutable MemTable -> SSTable Levels -> Compaction
          / Bloom Filter
          / Block Cache
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| B-Tree Page | 정렬 key와 pointer 저장 | page split, random write 발생 |
| WAL | LSM 쓰기 내구성 보장 | crash recovery 기준 |
| MemTable | 메모리 정렬 구조에 신규 쓰기 반영 | skiplist, red-black tree 사용 |
| SSTable | 불변 정렬 파일 | level별 병합 대상 |
| Compaction | 중복 key·tombstone 정리 | write amplification 주요 원인 |

> 요약: B-Tree는 계층 page 탐색 구조이고, LSM-Tree는 메모리 버퍼와 정렬 파일 병합으로 쓰기를 흡수하는 구조이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
쓰기 요청 -> WAL 기록 -> 메모리 반영 -> 디스크 flush -> compaction -> 읽기 시 cache/filter 탐색
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | B-Tree는 leaf page 탐색 후 제자리 갱신 | page split rate 확인 |
| 2 | LSM은 WAL 기록 후 MemTable에 반영 | fsync 지연, WAL size 확인 |
| 3 | MemTable 가득 차면 SSTable로 flush | flush latency 측정 |
| 4 | level compaction으로 파일 병합 | compaction debt 0 유지 |
| 5 | 읽기 시 cache, Bloom Filter, level 탐색 | read amplification 측정 |

> 요약: B-Tree는 즉시 page 갱신, LSM은 WAL·MemTable·SSTable·compaction 경로로 쓰기를 처리한다.

---

## Ⅳ. 특징

| 구분 | B-Tree | LSM-Tree | 판단 포인트 |
|:---|:---|:---|:---|
| 쓰기 경로 | leaf page random write | WAL+MemTable sequential write | write throughput 목표 |
| 읽기 경로 | root부터 leaf 탐색 | MemTable+여러 SSTable 탐색 | read amplification, Bloom Filter |
| 범위 조회 | leaf linked scan | level별 merge scan | range scan 빈도 |
| 운영 비용 | fragmentation, page split | compaction, tombstone | tail latency와 background I/O |

> 요약: B-Tree는 읽기 예측성이 높고, LSM-Tree는 쓰기 흡수력이 크지만 compaction과 읽기 증폭을 관리해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | B-Tree 저장 엔진 | LSM-Tree 저장 엔진 | OLTP read-heavy vs write-heavy |
| 비용/성능 | point read, range scan 중심 | sequential write, compaction 중심 | read:write 비율 8:2 또는 2:8 |
| 운영/위험 | page split, vacuum/rebuild | compaction debt, tombstone 폭증 | p99 latency와 background I/O |

> 요약: 읽기 지연과 범위 조회가 핵심이면 B-Tree, 쓰기 처리량과 순차 적재가 핵심이면 LSM-Tree를 우선 검토한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Read Amplification | 여러 SSTable level 조회 | Bloom Filter, block cache, compaction tuning | files checked per read |
| Write Amplification | 반복 compaction | level size, compaction thread 조정 | write amplification factor |
| Tail Latency 증가 | compaction과 foreground read 충돌 | rate limit, priority 설정 | p99 latency 100ms 이하 |

> 요약: LSM 운영은 읽기 증폭, 쓰기 증폭, compaction으로 인한 p99 지연을 지표로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 읽기 성능 | p99 100ms 이하, cache hit 95% 이상 | DB metrics, tracing |
| 쓰기 성능 | ingest 100K ops/sec 목표 충족 | benchmark, WAL metrics |
| Compaction | compaction debt 0, pending bytes 임계 이하 | RocksDB/Cassandra metrics |

> 요약: 저장 엔진 선택 후에는 p99 지연, 쓰기 처리량, compaction backlog를 함께 측정해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 금융 원장·주문 OLTP처럼 point read와 range scan이 많은 업무는 B-Tree 기반 엔진을 선택하고 buffer cache hit 95% 이상을 목표로 함
2. 로그·IoT·메시지 저장처럼 write-heavy 업무는 LSM 기반 엔진을 선택하고 WAL fsync, MemTable size, compaction thread를 workload로 조정함
3. LSM 운영 시 Bloom Filter, block cache, tombstone GC, compaction rate limit을 설정해 p99 100ms 이하와 compaction debt 0을 유지함

**결론 (2줄):**
- 기술사 판단: read-heavy OLTP는 B-Tree, write-heavy ingest는 LSM-Tree가 적합하며 혼합 업무는 지표 기반 PoC로 결정함
- 향후 방향: tiered storage, learned index, adaptive compaction을 활용하되 read/write amplification 지표를 SLA와 연결해야 함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "B-Tree와 LSM-Tree를 설명하시오" | write path와 read path 흐름 | 구조·비용·운영 차이 비교 |
| 요구사항 명시형 | "비교하시오", "선택 방안을 제시하시오" | read/write amplification 기반 선택 절차 | OLTP vs write-heavy 적용 기준 |

> 요약: 설명형은 구조와 원리, 비교형은 workload와 증폭 지표 중심으로 작성한다.
