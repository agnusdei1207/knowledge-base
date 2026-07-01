---
title: "I/O 관리·디스크 스케줄링 (I/O Management Disk Scheduling)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 24
---

# 📖 【암기용】 개념 완전 이해

> 목적: I/O 관리와 디스크 스케줄링을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: OS가 장치 요청을 버퍼링·순서화·완료 처리하는 I/O 제어 계층
- **왜 필요한가**: CPU는 ns 단위로 동작하지만 디스크와 네트워크 I/O는 us~ms 단위 지연을 가진다. OS는 DMA, interrupt, buffer cache, scheduler로 CPU 대기와 장치 병목을 줄인다.
- **핵심 직관**: I/O 관리는 식당 주문 대기열처럼 주문을 모으고, 이동 동선을 줄이며, 완료 알림을 받아 다음 작업을 깨우는 절차이다.

## 깊이 이해
- **배경·문제의식**: 저장장치 접근은 CPU 연산보다 지연시간이 크고, HDD는 헤드 이동, SSD는 병렬 채널과 erase block 제약을 가진다. 무작위 요청을 그대로 처리하면 대기열 지연과 처리량 손실이 생긴다.
- **작동 원리**: 애플리케이션의 read/write는 system call로 커널에 진입하고, buffer/page cache를 확인한 뒤 block layer가 요청을 병합·정렬한다. 장치는 DMA로 메모리와 직접 데이터를 주고받고 완료 시 interrupt 또는 polling으로 CPU에 알린다.
- **비유**: 택배 기사가 요청 순서대로만 움직이면 이동 거리가 늘어난다. 같은 동네 주문을 묶고 경로를 정렬하면 전체 배송 시간이 줄어든다.
- **구체 예시**: HDD는 SCAN/C-SCAN으로 seek distance를 줄이고, SSD는 물리 seek가 없어 FCFS, deadline, NVMe multi-queue가 latency tail 제어에 적합하다.
- **흔한 오해·주의점**: 디스크 스케줄링은 HDD에만 의미가 있는 것이 아니다. SSD에서도 queue depth, starvation, write amplification, tail latency 제어가 필요하다.

## 연결 개념
- DMA — CPU 개입 없이 메모리와 장치 간 데이터 전송
- interrupt/polling — I/O 완료 통지 방식
- NVMe multi-queue — CPU 코어별 큐로 lock contention을 줄이는 SSD I/O 구조

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: I/O 관리는 장치 드라이버만이 아니라 캐시, DMA, interrupt, block scheduler, 저장장치 특성까지 연결해 답안을 구성한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: I/O 관리는 애플리케이션 요청을 장치 명령으로 변환하고 버퍼링·스케줄링·완료 처리를 수행하는 OS 계층이다.
> 2. **가치**: DMA와 interrupt로 CPU 점유를 줄이고, buffer cache와 elevator 알고리즘으로 장치 지연을 통제한다.
> 3. **판단 포인트**: HDD는 seek 최소화, SSD/NVMe는 queue depth·tail latency·multi-queue contention이 선택 기준이다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| OS I/O 경로 이해 확인 | syscall, VFS, buffer cache, block layer, driver | 디스크 알고리즘만 나열 |
| 스케줄링 알고리즘 비교 확인 | FCFS, SSTF, SCAN, C-SCAN, deadline | HDD와 SSD 차이 누락 |
| 실무 병목 분석 확인 | DMA, interrupt, queue depth, iowait | 처리량만 쓰고 p95/p99 지연 미제시 |

> 요약: 이 문제는 요청 경로와 저장장치 특성별 스케줄링 선택 기준을 함께 요구한다.

---

## Ⅰ. 개요 및 필요성

I/O 관리는 OS가 장치 요청을 제어하는 계층이다. CPU와 저장장치 지연 격차가 크기 때문에 캐시, DMA, interrupt, I/O scheduler가 필요하다. 디스크 스케줄링은 요청 순서를 조정해 HDD seek와 SSD tail latency를 줄이는 역할을 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Process -> System Call -> VFS / Buffer Cache -> Block Layer
  -> I/O Scheduler -> Device Driver -> DMA / Interrupt -> Disk or SSD
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| System Call | 사용자 I/O 요청을 커널로 전달 | read, write, fsync |
| Buffer/Page Cache | 반복 읽기와 지연 쓰기 처리 | cache hit ratio 관리 |
| Block Layer | 요청 병합·분할·정렬 | bio, request queue |
| I/O Scheduler | 요청 순서 결정 | FCFS, SSTF, SCAN, deadline |
| Device Driver | 장치 명령 변환과 완료 처리 | DMA, interrupt, polling |

> 요약: I/O 경로는 시스템콜에서 시작해 캐시, 블록 계층, 스케줄러, 드라이버, 장치 완료 처리로 이어진다.

---

## Ⅲ. 동작원리 및 흐름도

```text
read/write 요청 -> 캐시 확인 -> 블록 요청 생성
  -> 큐 병합 / 정렬 -> DMA 전송 -> interrupt 완료 -> 프로세스 깨움
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 애플리케이션이 read/write/fsync 호출 | syscall rate |
| 2 | page cache hit이면 메모리에서 반환 | cache hit ratio 90% 이상 |
| 3 | miss 또는 writeback이면 block request 생성 | queue depth, merge ratio |
| 4 | scheduler가 FCFS/SSTF/SCAN/C-SCAN 등으로 순서 결정 | seek distance, wait time |
| 5 | DMA 전송 후 interrupt로 완료 통지 | p99 latency, iowait |

> 요약: OS는 캐시로 장치 접근을 줄이고, 스케줄러로 요청 순서를 조정하며, DMA와 interrupt로 완료를 처리한다.

---

## Ⅳ. 특징

| 구분 | 기존/대안 | 본 기술 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| FCFS | 요청 도착순 처리 | 구현 단순 | starvation 없음, seek 증가 |
| SSTF | 가까운 트랙 우선 | 평균 seek 감소 | 먼 요청 starvation 가능 |
| SCAN | 한 방향으로 이동하며 처리 | elevator 방식 | HDD 순차성 활용 |
| C-SCAN | 단방향 순환 스캔 | 대기시간 편차 감소 | 대용량 HDD 공정성 |
| SSD/NVMe | seek 개념 약함 | deadline, mq-deadline, none | p99 latency, queue depth |

> 요약: HDD는 seek 최소화 알고리즘, SSD는 tail latency와 multi-queue 경합 제어가 선택 기준이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 동기 blocking I/O | 캐시+큐+DMA+interrupt | CPU iowait 10% 이하 목표 |
| 비용/성능 | FCFS 단순 처리 | SSTF/SCAN/deadline 조정 | p95 지연과 starvation 동시 판단 |
| 운영/위험 | 장치 기본값 | 워크로드별 scheduler 선택 | DB, 로그, 백업 I/O 분리 |

> 요약: I/O 정책은 저장장치 종류와 워크로드 지연 목표를 기준으로 선택해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| starvation | SSTF가 가까운 요청만 처리 | deadline, C-SCAN, priority aging | max wait time |
| tail latency 증가 | queue depth 과다·writeback 집중 | cgroup I/O limit, dirty ratio 조정 | p99 latency 100ms 이하 |
| CPU interrupt 폭증 | 작은 I/O 과다 | interrupt coalescing, batching | interrupt/sec, CPU softirq |

> 요약: I/O 리스크는 starvation, p99 지연, interrupt 비용이며 큐 정책과 커널 파라미터로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 성능/지연 | p95 20ms 이하, p99 100ms 이하 | fio, iostat, blktrace |
| 품질/공정성 | max wait time 500ms 이하 | scheduler trace |
| 운영/자원 | iowait 10% 이하, queue depth 적정 | sar, perf, eBPF |

> 요약: 도입 효과는 p95/p99 지연, 최대 대기시간, iowait와 queue depth로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. HDD 로그·백업 볼륨은 SCAN/C-SCAN 계열로 순차성을 활용하고 평균 seek distance와 max wait time을 함께 측정한다.
2. SSD/NVMe 서버는 mq-deadline 또는 none을 비교하고 fio로 p99 latency 100ms 이하, queue depth별 처리량을 측정한다.
3. DB와 배치 I/O는 cgroup I/O limit, dirty_ratio, 별도 볼륨 분리로 fsync 지연과 writeback 집중을 차단한다.

**결론 (2줄):**
- 기술사 판단: HDD는 seek 최적화, SSD는 queue depth와 p99 지연, 혼합 워크로드는 deadline과 cgroup I/O 제어를 선택한다.
- 향후 방향: NVMe multi-queue와 eBPF 기반 I/O 관측으로 코어별 큐 경합과 tail latency를 직접 통제하는 운영이 확대된다.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "I/O 관리를 설명하시오" | syscall부터 DMA·interrupt까지 전체 흐름 | 디스크 스케줄링 알고리즘 |
| 요구사항 명시형 | "비교하시오", "성능 개선 방안을 제시하시오" | HDD/SSD별 큐 처리 흐름 | p99 지연, starvation, scheduler 선택 |

> 요약: 설명형은 I/O stack 전체를, 개선형은 장치 특성별 알고리즘과 지표를 중심으로 작성한다.
