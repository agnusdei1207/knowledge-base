---
title: "인메모리 컴퓨팅 (In-Memory Computing)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 249
---

# 📖 【암기용】 개념 완전 이해

> 목적: 인메모리 컴퓨팅을 디스크 I/O를 줄이는 소프트웨어 아키텍처와 메모리 내부 연산까지 포함하는 넓은 개념으로 이해하게 만든다.

## 한눈에
- **개요**: 데이터를 디스크가 아니라 메모리에 상주시켜 처리하거나, 메모리 가까이에서 연산해 데이터 이동을 줄이는 컴퓨팅 방식
- **왜 필요한가**: 디스크 접근은 ms 단위, DRAM 접근은 ns 단위이므로 실시간 분석과 고빈도 트랜잭션은 디스크 왕복을 줄여야 한다.
- **핵심 직관**: 매번 창고에 가서 물건을 찾는 대신 책상 위에 올려두고 바로 처리하는 방식이다.

## 깊이 이해
- **배경·문제의식**: 전통 DB는 디스크를 정본 저장소로 두고 일부만 cache에 올리므로 cache miss와 random I/O가 p95 응답시간을 지배한다.
- **작동 원리**: 인메모리 DB는 row/column store를 DRAM에 유지하고 WAL, snapshot, replication으로 휘발성 리스크를 보완한다.
- **비유**: 도서관 서가에서 매번 책을 가져오는 대신 자주 쓰는 책을 상담대 위에 올리고 변경 내역은 장부에 계속 적는 방식이다.
- **구체 예시**: SAP HANA는 columnar in-memory store로 HTAP를 지원하고 Redis는 key-value 데이터를 DRAM에 두며 AOF/RDB로 복구 경로를 제공한다.
- **흔한 오해·주의점**: caching은 정본 DB 앞 보조 계층이고, 인메모리 DB는 메모리 상주 데이터가 정본 역할을 수행할 수 있다. 두 개념을 구분해야 한다.

## 연결 개념
- PIM — 메모리 내부 연산으로 데이터 이동을 줄이는 하위 접근
- CXL Memory Pooling — 인메모리 데이터셋 확장을 돕는 메모리 pool
- HTAP — 트랜잭션과 분석을 같은 인메모리 구조에서 처리하는 방식

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: 인메모리 컴퓨팅은 응답시간 이점뿐 아니라 내구성, 용량, 비용 리스크를 함께 설계해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: In-Memory Computing은 데이터를 DRAM에 상주시켜 디스크 I/O 없이 처리하거나 메모리 근접 연산으로 이동량을 줄이는 방식임.
> 2. **가치**: ms 단위 디스크 접근을 ns~us 단위 메모리 접근으로 대체해 p95 응답시간과 분석 처리량을 개선함.
> 3. **판단 포인트**: WAL, snapshot, replication으로 휘발성 리스크를 통제하고 DRAM 용량·비용을 산정해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 디스크 기반 대비 차이 확인 | DRAM 상주, 디스크 I/O 제거 | "처리가 빠름" 같은 근거 없는 표현 |
| 내구성 설계 확인 | WAL, snapshot, replication | 휘발성 문제 누락 |
| 개념 구분 확인 | cache vs in-memory DB vs PIM | Redis cache와 정본 DB를 동일시 |

> 요약: 이 문제는 메모리 상주 구조와 내구성 보완, 개념 경계 구분을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 메모리 상주 처리 방식
- 배경: 디스크 기반 처리의 cache miss와 random I/O가 실시간 SLA를 제한함.
- 필요성: p95 응답시간 ms 이하, HTAP 분석, 고빈도 transaction 처리를 위해 DRAM 중심 구조가 필요함.

---

## Ⅱ. 구조 및 구성요소

```text
Client -> In-Memory Engine -> Row / Column Store in DRAM
Write Path -> WAL -> Snapshot -> Replica
Read Path -> Memory Scan / Index -> Result
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| In-Memory Store | 데이터셋을 DRAM에 유지 | row 또는 column 구성 |
| Query Engine | 메모리 주소 기반 질의 수행 | vectorized execution 가능 |
| WAL | 변경 이력 순차 기록 | crash recovery 기준 |
| Snapshot/Replica | 복구와 장애 전환 지원 | RTO/RPO 충족 필요 |

> 요약: 인메모리 컴퓨팅은 DRAM 상주 저장소와 WAL·snapshot·replica로 속도와 내구성을 함께 구성한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Write request -> DRAM update -> WAL append -> ack
-> periodic snapshot -> replica sync -> failure 시 WAL replay / failover
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 요청을 DRAM 구조에 반영 | write latency |
| 2 | WAL을 디스크·NVMe에 기록 | fsync policy |
| 3 | snapshot과 replica를 갱신 | replication lag |
| 4 | 장애 시 WAL replay 또는 failover | RTO, RPO |

> 요약: 인메모리 구조는 DRAM 처리 후 WAL·snapshot·replica로 장애 복구 경로를 만든다.

---

## Ⅳ. 특징

| 구분 | 디스크 기반 DB | 인메모리 컴퓨팅 | 수치·판단 기준 |
|:---|:---|:---|:---|
| 접근 지연 | ms 단위 I/O 영향 | ns~us 단위 메모리 접근 | p95 latency |
| 내구성 | 디스크 저장 기본 | WAL·snapshot 필요 | RPO/RTO |
| 비용 | GB당 비용 낮음 | DRAM 비용 높음 | dataset size |
| 적용 | 대용량 보관 | 실시간 분석·HTAP | hot data 비율 |

> 요약: 인메모리 컴퓨팅은 지연시간 이점을 얻는 대신 내구성 설계와 DRAM 비용을 감수한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | disk-first + buffer cache | memory-first + WAL | hot dataset이 DRAM에 적재 가능한지 |
| 비용/성능 | 낮은 비용, 높은 p95 | 높은 비용, 낮은 p95 | SLA와 TCO |
| 운영/위험 | 복구 체계 성숙 | 휘발성·capacity risk | RPO/RTO와 DRAM 사용률 |

> 요약: 데이터셋과 SLA가 DRAM 비용을 정당화하면 인메모리, 장기 보관 중심이면 디스크 기반을 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 데이터 유실 | WAL 반영 전 장애 | synchronous replication, fsync 조정 | RPO |
| 용량 초과 | 데이터셋 증가 | sharding, eviction, CXL pool | memory utilization |
| 복구 지연 | snapshot 주기와 WAL 크기 | incremental snapshot | RTO |

> 요약: 인메모리 리스크는 유실, 용량, 복구 지연이며 RPO/RTO와 메모리 사용률로 관리한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 지연 | p95 latency 목표 이하 | APM, query log |
| 내구성 | RPO/RTO 목표 충족 | failover drill |
| 비용 | GB당 비용과 SLA 이득 비교 | FinOps report |

> 요약: 인메모리 성과는 p95 지연, RPO/RTO, 비용 대비 SLA 이득으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. hot data와 real-time query를 식별해 인메모리 store에 상주시키고 cold data는 disk/object storage에 유지함.
2. WAL fsync, snapshot interval, replica 수를 업무 RPO/RTO 기준으로 설정함.
3. DRAM 사용률 80% 이상 지속 시 sharding, compression, CXL memory pool 확장을 검토함.

**결론 (2줄):**
- 기술사 판단: 실시간 SLA와 hot dataset 규모가 명확하면 인메모리, 보관·비용 중심이면 disk-first 구조를 선택함.
- 향후 방향: CXL, PMem, PIM과 결합해 메모리 중심 데이터 처리 플랫폼으로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "인메모리 컴퓨팅을 설명하시오" | WAL·snapshot·replica 흐름 | 디스크 기반 대비 지연·내구성 차이 |
| 요구사항 명시형 | "실시간 분석 시스템을 설계하시오" | hot/cold data 분리와 복구 절차 | SLA·RPO/RTO·비용 판단 |

> 요약: 설명형은 메모리 상주와 복구 흐름을, 설계형은 SLA와 내구성 기준을 중심으로 작성한다.
