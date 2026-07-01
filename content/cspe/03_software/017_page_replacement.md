---
title: "페이지 교체 알고리즘 (Page Replacement)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 17
---

# 📖 【암기용】 개념 완전 이해

> 목적: 페이지 교체 알고리즘을 처음 봐도 메모리에 남길 page를 고르는 정책으로 이해하게 만든다. 시험 답안 양식이 아니라, page fault 비용을 줄이는 원리를 설명한다.

## 한눈에
- **개요**: 페이지 교체는 물리 frame이 부족할 때 내보낼 victim page를 선택하는 정책이다.
- **왜 필요한가**: demand paging은 필요한 page를 나중에 적재하지만, 메모리가 꽉 차면 새 page를 넣기 위해 기존 page를 제거해야 한다.
- **핵심 직관**: 책상 위 공간이 부족할 때 앞으로 다시 볼 가능성이 낮은 책을 치우는 판단이다.

## 깊이 이해
- **배경·문제의식**: victim 선택이 나쁘면 곧 다시 필요한 page를 내보내 page fault가 반복된다. 교체 정책은 locality를 이용해 미래 참조를 추정한다.
- **작동 원리**: OPT는 미래에 가장 늦게 쓰일 page를 내보내 이론적 하한을 제공한다. FIFO는 먼저 들어온 page를 제거하고, LRU는 오래 안 쓴 page를 제거하며, Clock은 reference bit로 LRU를 근사한다.
- **비유**: 냉장고에서 가장 오래 손대지 않은 재료를 버리는 방식이 LRU이고, 들어온 순서대로 버리는 방식이 FIFO다.
- **구체 예시**: 참조열 1,2,3,4,1,2,5에서 frame 3개인 FIFO는 page fault가 연속 발생할 수 있고, frame 증가가 fault 감소를 보장하지 않는 Belady anomaly가 나타난다.
- **흔한 오해·주의점**: LRU가 항상 구현 가능한 최선은 아니다. 정확한 LRU는 접근 순서 갱신 비용이 커서 OS는 Clock, NRU, Aging 등 근사 알고리즘을 쓴다.

## 연결 개념
- Locality — 최근·인접 참조가 다시 발생하는 성질
- Belady Anomaly — frame 수 증가에도 FIFO fault가 늘어나는 현상
- Working Set — 교체 정책보다 상위에서 필요한 page 집합을 관리하는 개념

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 페이지 교체는 알고리즘 이름 나열이 아니라 page fault rate, 구현 비용, locality 추정 정확도 비교로 답한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 페이지 교체 알고리즘은 frame 부족 시 victim page를 선택해 page fault 비용을 최소화하려는 메모리 관리 정책이다.
> 2. **가치**: 적절한 교체는 major fault와 swap I/O를 줄이고 CPU utilization 하락을 막는다.
> 3. **판단 포인트**: OPT는 기준선, LRU는 locality 추정, Clock은 구현 비용 절감, FIFO는 Belady anomaly 위험으로 구분한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 알고리즘 비교 확인 | FIFO, OPT, LRU, Clock, LFU | 이름만 쓰고 victim 기준 누락하지 않음 |
| page fault 영향 이해 확인 | fault rate, dirty writeback, swap I/O | frame 수 증가가 항상 fault 감소라고 단정하지 않음 |
| 적용 판단 확인 | 구현 비용, reference bit, workload locality | OPT를 실제 구현 정책으로 쓰지 않음 |

> 요약: 이 문제는 victim 선택 기준과 page fault rate 영향을 비교해 운영 가능한 정책을 고르는 능력을 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: 페이지 교체는 victim page 선택 정책이다.
- 배경: 물리 frame이 부족할 때 임의로 page를 내보내면 곧 다시 참조되는 page가 제거되어 page fault storm과 thrashing이 발생한다.
- 필요성: OS는 locality, reference bit, dirty bit를 활용해 page fault rate, writeback I/O, major fault/sec 기준으로 victim을 선택해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Page Fault -> Free Frame Check
  / No Free Frame -> Replacement Policy -> Victim Page
  -> Dirty Writeback -> Page In -> Page Table / TLB Update
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Replacement Policy | victim page 선택 | FIFO, LRU, Clock, LFU |
| Reference/Dirty Bit | 참조·수정 여부 기록 | Clock, NRU 판단 입력 |
| Page Fault Handler | writeback, page-in, mapping 갱신 | major fault는 ms 단위 비용 |

> 요약: 교체 구조는 fault 발생 후 정책이 victim을 고르고 dirty writeback과 mapping 갱신을 수행하는 흐름이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Memory Access -> Page Miss -> Select Victim
  -> If Dirty Write Back -> Load Requested Page
  -> Update Page Table / TLB -> Resume Process
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | page table valid bit 확인 | minor/major fault 구분 |
| 2 | free frame 없으면 victim 선택 | victim selection latency |
| 3 | dirty page이면 disk write 수행 | writeback count |
| 4 | 새 page 적재 후 매핑 갱신 | page fault rate |

> 요약: 교체 비용은 victim 선택 자체보다 dirty writeback과 page-in I/O에서 크게 발생한다.

---

## Ⅳ. 특징

| 구분 | Victim 기준 | 장점 | 한계·수치 |
|:---|:---|:---|:---|
| FIFO | 가장 먼저 적재된 page | 구현 단순 | Belady anomaly 가능 |
| OPT | 가장 늦게 참조될 page | fault 하한 기준 | 미래 참조 필요 |
| LRU | 가장 오래 미참조 page | locality 반영 | 정확 구현 비용 큼 |
| Clock | reference bit 0 page | LRU 근사, O(1) 근접 | scan 길이 증가 가능 |

> 요약: 실제 OS는 LRU 정확도와 구현 비용 사이에서 Clock 계열 근사 정책을 주로 사용한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | FIFO queue | Clock/LRU approximation | locality가 있는 workload |
| 비용/성능 | 낮은 메타데이터 비용 | reference bit scan 비용 | fault 감소가 scan 비용보다 클 때 |
| 운영/위험 | 단순 eviction | dirty/writeback 제어 | writeback burst 방지 필요 |

> 요약: 교체 정책은 fault rate 감소와 victim 선택 오버헤드의 균형으로 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Belady Anomaly | FIFO의 적재 순서 의존 | LRU, Clock 전환 | frame 증가 대비 fault 변화 |
| Writeback Burst | dirty page 동시 eviction | background flush, dirty ratio 제한 | dirty pages, writeback MB/s |
| Thrashing | WSS 대비 frame 부족 | working set, PFF 제어 | major fault/sec, iowait |

> 요약: 교체 정책 리스크는 anomaly, writeback burst, thrashing이며 fault와 writeback 지표로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| Fault Rate | 기준선 대비 major fault 50% 이하 | vmstat, perf |
| Writeback | dirty writeback p95 지연 관리 | iostat, kernel trace |
| 정책 비용 | replacement scan CPU 3% 이하 | perf, ftrace |

> 요약: 교체 정책 평가는 page fault만이 아니라 dirty writeback과 scan CPU 비용까지 포함한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 범용 OS는 Clock/active-inactive list 계열로 LRU를 근사하고 reference bit를 주기적으로 샘플링함.
2. DB workload는 OS page cache와 DB buffer cache 중복을 줄이기 위해 direct I/O 또는 cache 크기 상한을 설정함.
3. dirty ratio, background writeback, cgroup memory pressure를 조정해 eviction이 tail latency p99를 만들지 않게 함.

**결론 (2줄):**
- 기술사 판단: 이론 비교는 OPT·LRU·FIFO로 설명하고, 실무 선택은 Clock 계열과 working set 제어로 답안을 마무리함.
- 향후 방향: NUMA, SSD, persistent memory 환경에서는 page migration과 tiered memory 정책까지 함께 고려함.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "페이지 교체 알고리즘을 설명하시오" | fault 처리와 victim 선택 흐름 | FIFO, OPT, LRU, Clock 비교 |
| 요구사항 명시형 | "비교하시오", "방안을 제시하시오" | fault rate 진단, dirty writeback 제어 | Belady anomaly와 Clock 선택 기준 |

> 요약: 비교형은 victim 기준, 구현 비용, page fault rate를 표로 압축해 제시한다.
