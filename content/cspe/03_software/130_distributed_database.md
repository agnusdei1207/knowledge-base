---
title: "분산 데이터베이스 (Distributed Database)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 130
---

# 📖 【암기용】 개념 완전 이해

> 목적: 분산 데이터베이스를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 여러 노드·지역에 데이터를 나누거나 복제해 하나의 DB처럼 사용하는 시스템
- **왜 필요한가**: 단일 DB는 용량, 처리량, 지역 지연, 장애 허용에 한계가 있다. 분산 DB는 파티셔닝과 복제로 확장과 가용성을 확보하지만 일관성·트랜잭션·운영 복잡도가 증가한다.
- **핵심 직관**: 한 금고에 모든 문서를 넣지 않고 여러 지점 금고에 나누어 보관하되, 사용자는 하나의 문서 창구처럼 이용하는 구조임

## 깊이 이해
- **배경·문제의식**: 서비스 규모가 커지면 단일 서버 증설만으로 저장량과 요청량을 감당하기 어렵다. 분산 DB는 horizontal partitioning, replication, distributed transaction을 통해 데이터를 여러 노드에 배치한다.
- **작동 원리**: 데이터는 샤드 키로 분산되고 복제본으로 보호된다. 질의 라우터나 coordinator가 요청을 적절한 노드로 보내며, 트랜잭션은 2PC, consensus, MVCC 같은 기법으로 정합성을 맞춘다.
- **비유**: 전국 택배망처럼 물건을 지역 허브에 나눠 보관하고, 중앙 시스템은 어느 허브에 있는지 찾아 배송을 조정하는 방식임
- **구체 예시**: 사용자 1억 명을 user_id 해시 기준 64개 샤드로 분산하고, 각 샤드 RF=3으로 복제하면 특정 노드 장애 시에도 서비스 지속이 가능함
- **흔한 오해·주의점**: 분산 DB는 무조건 확장을 보장하지 않는다. 잘못된 샤드 키, cross-shard transaction, 글로벌 보조 인덱스는 지연과 장애 전파 원인이 된다.

## 연결 개념
- 샤딩(Sharding) - 데이터 수평 분할
- 복제(Replication) - 가용성과 읽기 분산
- CAP/PACELC - 분산 DB 일관성 판단 틀

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 분산 DB 답안은 파티셔닝·복제·분산 트랜잭션·CAP 선택을 하나의 구조로 묶어야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 분산 DB는 데이터를 여러 노드에 분산·복제하고 단일 논리 DB처럼 제공하는 시스템임.
> 2. **가치**: 저장 용량, 처리량, 지역 지연, 장애 허용을 노드 확장과 복제로 처리함.
> 3. **판단 포인트**: shard key, replication, consensus/2PC, consistency level, cross-shard query 비용이 설계 핵심임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 분산 저장 구조 이해 확인 | partition, replication, coordinator | 단순 백업 DB와 혼동하지 않음 |
| 일관성 트레이드오프 판단 확인 | CAP, quorum, consensus, 2PC | 가용성과 강한 일관성을 동시에 무제한 제공한다고 쓰지 않음 |
| 운영 리스크 확인 | hot shard, split brain, rebalance | 샤드 키와 장애조치 기준 누락 방지 |

> 요약: 분산 DB 문제는 확장 이점보다 일관성·장애·운영 비용 판단이 채점 핵심임.

---

## Ⅰ. 개요 및 필요성

분산 데이터베이스는 여러 노드에 데이터를 배치한 DB이다. 단일 DB는 저장량, 처리량, 지역 지연, 장애 허용에서 한계를 가진다. 분산 DB는 파티셔닝과 복제를 통해 확장을 제공하지만 일관성과 운영 통제를 함께 설계해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Client -> Router/Coordinator -> Shard/Partition -> Replica Group -> Storage
                         +-> Metadata/Catalog
                         +-> Transaction/Consensus
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Router/Coordinator | 요청 라우팅과 결과 병합 | scatter-gather 비용 |
| Shard/Partition | 데이터 수평 분할 | shard key 분포 필요 |
| Replica Group | 장애 허용과 읽기 분산 | leader/follower, quorum |
| Metadata/Catalog | 샤드 위치와 스키마 관리 | 장애 시 라우팅 영향 |

> 요약: 분산 DB는 라우터, 샤드, 복제그룹, 메타데이터 계층으로 단일 논리 DB를 구성함.

---

## Ⅲ. 동작원리 및 흐름도

```text
Request -> Shard Key Resolve -> Replica Select -> Local Execute -> Consensus/Commit -> Merge Result
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 요청에서 shard key 추출 | single-shard 비율 |
| 2 | 메타데이터로 대상 노드 결정 | routing latency |
| 3 | 복제그룹에서 읽기·쓰기 수행 | quorum 충족 여부 |
| 4 | 필요 시 2PC 또는 consensus 수행 | commit latency p95 |
| 5 | cross-shard 결과 병합 | fan-out shard count |

> 요약: 분산 DB는 샤드 위치 결정 후 로컬 실행을 우선하고, 필요 시 분산 합의와 결과 병합을 수행함.

---

## Ⅳ. 특징

| 구분 | 단일 DB | 분산 DB | 판단 포인트 |
|:---|:---|:---|:---|
| 확장 | 수직 증설 중심 | 수평 분할·복제 | 데이터·요청 증가율 |
| 일관성 | 단일 노드 ACID | quorum, 2PC, consensus | CAP/PACELC 선택 |
| 운영 | 장애 범위 단순 | rebalance, failover, split brain | 자동화·관측성 필요 |

> 요약: 분산 DB는 확장과 가용성을 얻는 대신, 일관성 지연과 운영 복잡도를 감수함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 단일 RDB | sharding + replication | 저장량 TB 단위, TPS 증가율 |
| 비용/성능 | 고사양 서버 | 노드 수평 확장 | cross-shard 비율 10% 이하 |
| 운영/위험 | 단일 장애 도메인 | 노드·네트워크 장애 도메인 | quorum, failover 자동화 |

> 요약: 분산 DB는 single-shard 접근 비율이 높고 노드 장애 통제가 가능한 업무에 적합함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Hot Shard | 편향된 shard key | 해시 키, composite key, rebalance | shard별 QPS 편차 |
| Cross-Shard 지연 | 트랜잭션·조인 분산 | aggregate 단위 설계, saga | distributed transaction rate |
| Split Brain | 네트워크 분할 | quorum, fencing token | leader count, election log |

> 요약: 분산 DB 리스크는 키 편향, 분산 트랜잭션, 네트워크 분할을 중심으로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 라우팅 | single-shard query 90% 이상 | query router log |
| 복제 | replication lag p95 2초 이하 | replica metrics |
| 장애 | failover RTO 5분 이하 | chaos test, drill |

> 요약: 분산 DB는 단일 샤드 비율, 복제 지연, 장애조치 시간으로 운영 적합성을 평가함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 도메인 aggregate와 접근 패턴을 기준으로 shard key를 정하고, cross-shard transaction 비율을 10% 이하로 관리함.
2. RF=3, quorum read/write, fencing token으로 장애조치와 split brain을 통제함.
3. 리밸런싱, 백업 복구, 장애조치 훈련을 자동화하고 shard별 QPS·용량 편차를 대시보드화함.

**결론 (2줄):**
- 기술사 판단: 단일 DB 한계가 명확하고 shard key가 안정되면 분산 DB, 복잡 조인·강한 ACID 중심이면 단일 RDB 확장을 우선함.
- 향후 방향: NewSQL과 서버리스 분산 DB는 consensus와 자동 리밸런싱을 결합해 운영 부담을 낮추는 방향으로 발전함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "분산 DB를 설명하시오" | 라우팅, 복제, 커밋 흐름 | 단일 DB와 분산 DB 비교 |
| 요구사항 명시형 | "대규모 DB 설계 방안을 제시하시오" | shard key, quorum, 장애조치 | hot shard, cross-shard, split brain 대응 |

> 요약: 설명형은 구조와 원리, 설계형은 샤드 키와 장애 통제 기준을 중심으로 작성함.
