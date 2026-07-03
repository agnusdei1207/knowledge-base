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
- **개요**: B-Tree와 LSM-Tree는 데이터베이스의 **저장 엔진 인덱스 구조**로, 데이터를 디스크에 어떻게 쓰고 읽을지를 결정하는 근본 설계다. B-Tree는 정렬된 페이지를 제자리에서 고쳐 쓰는 구조, LSM-Tree(Log-Structured Merge-Tree)는 메모리에 먼저 쓰고 정렬된 파일로 순차 병합해 나가는 구조다.
- **왜 필요한가**: 디스크(특히 HDD, 정도는 약하지만 SSD도)는 여기저기 흩어진 랜덤 쓰기보다 한 방향으로 이어지는 순차 쓰기가 훨씬 빠르다. 읽기 위주 워크로드와 쓰기 위주 워크로드는 이 특성을 다르게 활용해야 하므로 구조가 갈린다.
- **핵심 직관**: B-Tree는 가나다 순 서류철에서 해당 페이지를 바로 찾아 고쳐 끼우는 방식이고, LSM-Tree는 새 서류를 일단 임시함에 모았다가 어느 정도 차면 정렬된 묶음으로 만들어 기존 묶음과 합치는 방식이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 저장 엔진 인덱스 구조(Storage Engine Index) | DB가 데이터를 디스크에 배치하고 찾아가는 근본 자료구조 — 이 개념의 상위 범주 | 도서관이 책을 정리하는 방식 자체 |
| B-Tree(B+Tree) | 루트-브랜치-리프 페이지로 구성된 정렬 트리, 리프 페이지를 직접 찾아 제자리 갱신 | 가나다 순 서류철을 바로 고쳐 끼우기 |
| 제자리 갱신(In-place Update) | 값을 바꿀 때 원래 저장 위치를 그대로 찾아가 덮어쓰는 방식 | 서류철의 해당 페이지를 직접 펴서 수정 |
| Page Split(페이지 분할) | 꽉 찬 리프 페이지에 새 행을 넣어야 할 때 페이지를 둘로 쪼개고 상위 포인터를 갱신하는 동작 | 서류철 한 칸이 꽉 차서 새 칸을 만들고 절반을 옮기기 |
| LSM-Tree(Log-Structured Merge-Tree) | WAL·메모리 버퍼·정렬된 디스크 파일·병합(Compaction)으로 구성된 로그 구조 인덱스 | 편지를 모아뒀다 정렬해서 기존 묶음과 합치는 우체국 |
| WAL(Write-Ahead Log) | 실제 반영 전에 먼저 순차 기록해 두는 로그 — 장애 시 복구 기준 | 통장에 기록하기 전에 적어두는 메모장 |
| MemTable | 새로 들어온 쓰기를 메모리의 정렬 자료구조(스킵리스트 등)에 우선 반영하는 버퍼 | 접수대 위의 임시 서류함 |
| Immutable MemTable | 가득 찬 MemTable을 디스크로 내려보내기 직전, 더 이상 수정하지 않고 얼린 상태 | 다 찬 임시함을 봉인해 옮길 준비 |
| SSTable(Sorted String Table) | 디스크에 기록된, 키 순으로 정렬되고 더 이상 수정하지 않는 불변 파일 | 정렬해서 묶어놓은 편지 다발 |
| Compaction(컴팩션) | 여러 SSTable을 병합해 중복 키·삭제 표시(tombstone)를 정리하고 레벨을 재구성하는 백그라운드 작업 | 여러 다발을 하나로 재정렬해 합치는 작업 |
| Tombstone(삭제 표시) | LSM에서 즉시 지우지 않고 "삭제됨" 표식만 남겨둔 항목, compaction 때 실제로 제거됨 | 지운 게 아니라 "폐기 예정" 딱지만 붙여둠 |
| Bloom Filter | 어떤 키가 "이 파일에 절대 없다"를 빠르게 판단해 불필요한 파일 조회를 건너뛰게 하는 확률적 자료구조 | 도서관 입구에서 "이 책 이 서가엔 없어요"를 미리 알려주는 안내판 |
| Read Amplification(읽기 증폭) | 논리적으로 1건을 읽기 위해 실제로 여러 파일·레벨을 조회해야 하는 배수 | 편지 한 통 찾으려고 여러 다발을 들춰봐야 하는 수고 |
| Write Amplification(쓰기 증폭) | 논리적으로 1바이트를 쓰기 위해 compaction 등으로 실제 디스크에 여러 번 다시 쓰이는 배수 | 편지 한 통이 여러 번 재정렬되며 반복해서 옮겨 적히는 수고 |

## 깊이 이해

### B-Tree의 동작 — 숫자로 보는 트리 높이와 페이지 분할
- B+Tree는 각 페이지(보통 8KB)에 여러 키를 담아 팬아웃(fanout)을 높인다. 팬아웃이 약 100이면, 1억 행을 담은 트리의 높이는 log₁₀₀(100,000,000) ≈ 4단계에 불과하다. 즉 점 조회(point lookup) 1건이 최악의 경우 페이지 4번만 읽으면 끝난다 — 상위 1~2단계는 메모리 캐시에 상주하는 경우가 많아 실제 디스크 I/O는 1~2회 수준으로 더 줄어든다.
- 문제는 쓰기다. 리프 페이지가 100건으로 꽉 찬 상태에서 중간 값(예: 50번째 자리)에 새 행을 넣어야 하면, 그 페이지는 50건씩 두 페이지로 쪼개지고(Page Split) 부모 페이지의 포인터도 갱신해야 한다. 이 분할은 디스크 상에서 임의 위치(random I/O)로 발생하므로, 쓰기가 몰리면 랜덤 I/O 비용이 누적된다.

### LSM-Tree의 동작 — 쓰기를 순차로 바꾸는 대신 무엇을 대가로 치르나
- 쓰기 요청이 들어오면 ① WAL에 순차로 기록해 내구성을 확보하고, ② 동시에 메모리의 MemTable(정렬 자료구조)에 반영한다. 이 시점에서 디스크에는 오직 이어붙이기(append-only) 방식의 순차 쓰기만 발생한다 — B-Tree의 페이지 분할 같은 랜덤 쓰기가 없다.
- MemTable이 가득 차면(예: 64MB) Immutable MemTable로 얼리고 새 MemTable을 받기 시작하며, 백그라운드에서 Immutable MemTable을 정렬된 SSTable 파일로 flush한다.
- SSTable이 여러 개 쌓이면 Compaction이 이들을 병합해 레벨(L0, L1, L2...)을 재구성한다. 레벨 간 크기 비율이 보통 10배(L1이 640MB면 L2는 약 6.4GB 식)이므로, 데이터 1건은 L0에서 최하위 레벨까지 여러 번 다시 읽히고 다시 쓰인다. 이 반복 재기록이 **쓰기 증폭**이며, 실무에서 흔히 10~30배 수준으로 보고된다 — 즉 사용자가 논리적으로 1MB를 써도 디스크에는 실제로 10~30MB가 기록될 수 있다.

### 읽기 경로 — Bloom Filter가 없으면 왜 느려지는가
- LSM에서 점 조회는 먼저 MemTable을 확인하고, 없으면 SSTable을 최신 레벨부터 순서대로 확인해야 한다. 레벨이 5개면 최악의 경우 파일 5개를 다 열어봐야 하므로 읽기 증폭이 5배에 이를 수 있다.
- Bloom Filter는 각 SSTable에 대해 "이 키가 여기 있을 수도 있다/절대 없다"를 매우 빠르게(메모리 내 비트 배열 조회) 판별한다. 오탐률(false positive rate)이 1% 수준이면, 실제로 키가 없는 파일의 99%는 디스크를 열어보지 않고 건너뛸 수 있어 읽기 증폭을 크게 낮춘다.

### 판별 원리 — 언제 B-Tree, 언제 LSM-Tree
- 읽기:쓰기 비율이 8:2 수준으로 읽기 위주이고 point read·range scan 지연이 중요한 OLTP(주문, 결제 원장)는 **B-Tree** 계열(MySQL InnoDB 등)이 유리하다 — 트리 높이가 낮아 조회가 예측 가능하게 빠르다.
- 반대로 로그·IoT 센서·메시지처럼 초당 수만~수십만 건의 쓰기를 흡수해야 하고 읽기:쓰기가 2:8 수준으로 쓰기 위주라면 **LSM-Tree** 계열(RocksDB, Cassandra 등)이 유리하다 — 순차 쓰기로 쓰기 처리량을 확보하는 대신, 쓰기·읽기 증폭과 compaction 부하를 감수한다.

### 비유와 흔한 오해
- **비유**: B-Tree는 가나다 서류철을 바로 고쳐 끼우는 사서, LSM-Tree는 접수함에 모았다가 밤에 정렬해 합치는 우체국 야간 작업자다.
- **오해**: "LSM은 쓰기가 공짜다"는 틀렸다 — WAL·MemTable 반영 자체는 빠르지만, 그 대가로 백그라운드 compaction이 쓰기 증폭을 만들고, 이것이 디스크 대역폭과 CPU를 잠식해 foreground 읽기의 꼬리 지연(tail latency)을 늘릴 수 있다.

## 연결 개념
- WAL — 두 구조 모두에서 장애 복구를 보장하는 선기록 로그, LSM에서는 특히 필수 경로
- SSTable·Compaction — LSM 고유의 쓰기 흡수·정리 메커니즘
- 파티셔닝(111) — 저장 엔진 선택과 별개로, 단일 DB 내부에서 데이터를 물리적으로 나누는 또 다른 축

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

- 개요: B-Tree·LSM은 저장 엔진 인덱스이다.
- 배경: B-Tree는 정렬 page를 제자리 갱신하고 LSM-Tree는 WAL, MemTable, SSTable, Compaction으로 쓰기를 흡수한다.
- 필요성: read amplification, write amplification, compaction debt, tail latency를 워크로드별로 비교해야 한다.

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
