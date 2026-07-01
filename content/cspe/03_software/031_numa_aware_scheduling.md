---
title: "NUMA 인지 스케줄링 (NUMA-aware Scheduling)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 31
---

# 📖 【암기용】 개념 완전 이해

> 목적: NUMA 인지 스케줄링을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: CPU가 가까운 메모리를 우선 사용하도록 태스크와 페이지를 같은 NUMA 노드에 배치하는 스케줄링 기법
- **왜 필요한가**: 다소켓 서버에서는 모든 메모리 접근 시간이 같지 않다. 다른 소켓의 메모리에 접근하면 local memory보다 지연이 커지고 대역폭 경합이 발생한다.
- **핵심 직관**: 내 책상 서랍의 문서는 즉시 꺼내지만 옆 건물 창고 문서는 이동 시간이 추가되는 상황과 같다.

## 깊이 이해
- **배경·문제의식**: SMP처럼 모든 CPU가 같은 비용으로 메모리를 접근한다고 가정하면 대형 서버에서 remote memory access가 증가한다. DB, JVM, 인메모리 캐시처럼 메모리 집약 워크로드는 NUMA 배치에 따라 p99 지연이 달라진다.
- **작동 원리**: OS는 CPU, 메모리 bank, I/O 장치를 NUMA node topology로 파악한다. 태스크가 주로 접근하는 페이지와 실행 CPU를 같은 노드에 두기 위해 node affinity, automatic NUMA balancing, page migration을 사용한다.
- **비유**: 팀원이 자주 쓰는 자료를 자기 자리 근처 캐비닛에 두면 왕복 시간이 줄어든다. 팀을 다른 층으로 옮기면 자료도 같이 옮겨야 한다.
- **구체 예시**: 2-socket 서버에서 local memory access가 80ns, remote memory access가 130ns 수준이면 remote 비율 40%인 DB는 lock 대기와 cache miss가 증가할 수 있다.
- **흔한 오해·주의점**: CPU 사용률이 낮아도 NUMA 배치가 틀리면 지연이 커진다. 스케줄러가 태스크만 옮기고 페이지를 옮기지 않으면 remote access가 유지된다.

## 연결 개념
- NUMA topology — CPU·메모리·I/O 장치의 거리 정보
- Node affinity — 태스크와 메모리를 특정 노드에 묶는 정책
- Page migration — 자주 쓰는 메모리 페이지를 가까운 노드로 이동

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: NUMA-aware scheduling은 CPU 배치만이 아니라 memory locality, page migration, remote access latency, node affinity를 함께 다룬다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: NUMA 인지 스케줄링은 태스크 실행 CPU와 해당 태스크가 자주 접근하는 메모리 페이지를 같은 NUMA 노드에 배치하는 기법이다.
> 2. **가치**: remote memory access를 줄여 인메모리 DB, JVM, 캐시 서버의 p99 지연과 메모리 대역폭 경합을 통제한다.
> 3. **판단 포인트**: node affinity, automatic NUMA balancing, page migration, remote/local access ratio를 함께 확인해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| NUMA 구조 이해 확인 | local/remote memory, node topology | 멀티코어 부하분산으로만 설명 |
| 스케줄링·메모리 결합 확인 | task placement, page migration, affinity | CPU 이동만 쓰고 페이지 이동 누락 |
| 성능 분석 판단 확인 | remote latency, bandwidth, cache miss | CPU 사용률만 지표로 제시 |

> 요약: 이 문제는 CPU 스케줄링과 메모리 배치를 결합해 remote access를 줄이는 판단을 요구한다.

---

## Ⅰ. 개요 및 필요성

NUMA 인지 스케줄링은 CPU와 메모리의 거리 차이를 고려한 배치 기법이다. 다소켓 서버에서는 local memory와 remote memory 접근 지연이 다르다. 태스크와 메모리 페이지를 같은 노드에 배치해야 p99 지연과 메모리 대역폭 경합을 줄일 수 있다.

---

## Ⅱ. 구조 및 구성요소

```text
NUMA Topology -> Node0 CPU / Memory, Node1 CPU / Memory
  -> Task Placement -> Memory Policy -> Page Migration
  -> Local Access 우선 / Remote Access 측정
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| NUMA Node | CPU 코어와 지역 메모리 묶음 | socket 또는 memory domain |
| Scheduler | 태스크 실행 CPU 선택 | node load와 locality 고려 |
| Memory Policy | 페이지 할당 노드 결정 | bind, interleave, preferred |
| Page Migration | 접근 패턴에 따라 페이지 이동 | migration cost 존재 |
| NUMA Metric | local/remote 접근 비율 측정 | numastat, perf mem |

> 요약: NUMA-aware 구조는 topology 파악, 태스크 배치, 메모리 정책, 페이지 이동, remote access 측정으로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
프로세스 실행 -> 첫 메모리 할당 -> node 기록
  -> scheduler가 CPU 선택 -> remote access 감지
  -> task 이동 / page migration -> locality 재측정
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 프로세스 시작 시 NUMA policy와 cpuset 확인 | numactl policy |
| 2 | first-touch 원칙으로 페이지 할당 | page node distribution |
| 3 | 스케줄러가 node load와 affinity로 CPU 선택 | node utilization |
| 4 | remote access가 크면 task 또는 page 이동 | remote ratio, migration/sec |
| 5 | 이동 후 p99 latency와 bandwidth 재측정 | perf mem, numastat |

> 요약: NUMA 인지 스케줄링은 first-touch 배치 후 접근 패턴을 보고 태스크와 페이지를 가까운 노드로 재배치한다.

---

## Ⅳ. 특징

| 구분 | 기존/대안 | 본 기술 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| UMA 가정 | 메모리 접근 비용 동일 | local/remote latency 구분 | remote 130ns, local 80ns 예시 |
| 일반 스케줄링 | CPU 부하 중심 | memory locality 포함 | remote access 20% 이하 목표 |
| 수동 정책 | 관리자 numactl 지정 | automatic NUMA balancing | page migration 비용 |
| 한계 | 부하 균등 우선 | locality와 balance 절충 | node imbalance 10% 이하 |

> 요약: NUMA-aware scheduling은 CPU 사용률보다 memory locality를 포함해 p99 지연을 관리한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | CPU 부하 기반 배치 | CPU+메모리 노드 배치 | 다소켓, 메모리 집약 워크로드 |
| 비용/성능 | remote access 방치 | node affinity와 page migration | p99 latency, remote ratio |
| 운영/위험 | 자동 balancing 기본값 | 수동 bind/interleave 조합 | DB, JVM heap, cache 특성 |

> 요약: NUMA 정책은 워크로드 메모리 접근 패턴과 노드별 부하를 동시에 측정해 결정한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| remote access 증가 | 태스크와 페이지가 다른 노드에 위치 | numactl bind, cpuset, page migration | remote ratio 20% 이하 |
| 노드 불균형 | 특정 노드에 CPU·메모리 집중 | interleave, load balancing | node utilization 편차 10% 이하 |
| migration 비용 | 페이지 이동이 잦아 TLB·cache 손실 | migration threshold 조정 | migration/sec, LLC miss |

> 요약: NUMA 리스크는 remote access, node imbalance, migration 비용이며 세 지표를 동시에 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 성능/지연 | p99 latency 20% 이상 감소 | benchmark, APM |
| 품질/지역성 | remote access 20% 이하 | numastat, perf mem |
| 운영/자원 | node utilization 편차 10% 이하, migration/sec 기준선 유지 | mpstat, ftrace |

> 요약: NUMA-aware 도입 효과는 p99 지연, remote access 비율, 노드 부하 편차로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. DB·JVM·캐시 서버는 `numactl --hardware`, `numastat`, `perf mem`으로 topology와 remote access 기준선을 측정한다.
2. 지연 민감 프로세스는 cpuset과 memory bind로 CPU·메모리를 같은 노드에 묶고 p99 latency 20% 감소 여부를 검증한다.
3. 워크로드가 노드 전체 메모리를 고르게 쓰면 interleave 정책을 적용하고 migration/sec와 node imbalance를 모니터링한다.

**결론 (2줄):**
- 기술사 판단: 메모리 집약·다소켓 서버는 NUMA-aware scheduling, 단일 소켓 또는 I/O-bound 서비스는 일반 load balancing을 우선 적용한다.
- 향후 방향: 스케줄러는 CPU, 메모리, I/O 장치 locality를 통합한 topology-aware resource management로 확장된다.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "NUMA 인지 스케줄링을 설명하시오" | first-touch, task/page 이동 흐름 | local/remote memory 특징 |
| 요구사항 명시형 | "개선 방안을 제시하시오", "설계하시오" | remote access 측정과 재배치 흐름 | bind/interleave 선택 기준과 지표 |

> 요약: 설명형은 NUMA 원리, 개선형은 remote access 측정과 배치 정책 중심으로 작성한다.
