---
title: "DRAM vs SRAM (DRAM SRAM)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 28
extra:
  question_no: "028"
  exam_status: "기출"
  exam_history: "125회"
---

## 미리 알고가기

- DRAM은 커패시터 전하로 비트를 저장해 주기적 refresh가 필요함
- SRAM은 플립플롭 회로로 상태를 유지해 refresh 없이 빠르게 동작함
- 두 메모리는 속도·집적도·전력 특성이 달라 계층 구조에서 역할이 다름

## Ⅰ. 개요

- **정의/개념**: DRAM은 1T1C 셀에 전하를 저장해 높은 집적도로 큰 용량을 제공하는 동적 메모리이고, SRAM은 플립플롭 기반 셀로 빠른 접근과 refresh 없는 유지 특성을 제공하는 정적 메모리임
- **배경/필요성**: 시스템은 CPU에 가까운 초저지연 저장층과 대용량 주기억장치를 동시에 요구하므로, 속도 중심의 SRAM과 용량 중심의 DRAM을 계층적으로 함께 사용함

## Ⅱ. 특징

- DRAM은 집적도와 비용 효율이 높아 주기억장치로 적합함
- SRAM은 refresh가 없어 지연이 짧고 캐시로 쓰기에 유리함
- DRAM은 refresh와 row access 제약 때문에 대역폭과 지연 최적화가 중요함
- SRAM은 면적과 누설 전력이 커서 대용량 확장이 어렵고 비용 부담이 큼

## Ⅲ. 종류 및 비교

| 판단 기준 | DRAM | SRAM |
|:---|:---|:---|
| 저장 방식 | 커패시터 전하를 저장하고 주기적으로 refresh함 | 플립플롭 회로 상태를 유지해 refresh가 필요 없음 |
| 속도 | 상대적으로 느리지만 대용량화가 쉬움 | 빠르지만 면적당 용량이 작음 |
| 비용 | 비트당 비용이 낮음 | 비트당 비용이 높음 |
| 대표 용도 | 메인 메모리와 대용량 버퍼 | L1, L2, L3 캐시와 소형 고속 버퍼 |

> 요약: DRAM은 용량·비용, SRAM은 지연·캐시 응답에 강점이 있음.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| DRAM 1T1C Cell | 트랜지스터와 커패시터 조합으로 비트를 저장해 고집적 구성이 가능하지만 refresh가 필요함 |
| SRAM 6T Cell | 플립플롭 회로로 데이터를 유지해 즉시 읽고 쓸 수 있으나 셀 면적이 큼 |
| Memory Controller | DRAM의 row activation과 refresh를 제어하고 캐시 miss 시 데이터 이동을 조율함 |
| Cache and Main Memory Placement | SRAM은 CPU 가까운 상위 계층에, DRAM은 큰 작업 집합을 담는 하위 계층에 배치되어 상호 보완함 |

```text
+-----------+     +----------------+     +-------------+
| CPU Core  | --> | SRAM Cache     | --> | DRAM Memory |
+-----------+     +----------------+     +-------------+
                                       ^
                                       |
                               +----------------+
                               | Refresh Control|
                               +----------------+
```

> 요약: SRAM은 CPU 가까운 캐시에, DRAM은 refresh 제어를 받는 주기억장치에 배치됨.

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| CPU 데이터 요청  | --> | SRAM cache 조회  | --> | miss 시 DRAM 접근  | --> | 데이터 상향 적재   |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **CPU 데이터 요청**: 프로세서가 필요한 데이터 접근을 시작함
2. **SRAM cache 조회**: 가장 빠른 상위 계층에서 즉시 hit 여부를 판단함
3. **miss 시 DRAM 접근**: 없으면 메모리 컨트롤러가 DRAM row와 column을 열어 데이터를 읽음
4. **데이터 상향 적재**: 읽은 데이터를 SRAM cache에 올려 이후 접근을 가속함

> 요약: CPU 요청은 SRAM cache에서 먼저 찾고 miss 시 DRAM에서 읽어 다시 cache에 올림.

## Ⅵ. 실무 적용 및 유의점

1. DRAM은 refresh와 row conflict가 겹치면 memory stall이 늘어나므로 bank interleaving과 row policy tuning을 적용하고 DRAM access latency, row buffer hit rate로 확인함
2. SRAM은 용량을 늘리면 면적과 누설 전력이 커지므로 cache partitioning과 low-leakage design을 적용하고 cache energy per access, area efficiency로 확인함
3. AI·HPC는 DRAM 대역폭 한계로 연산기가 유휴 상태가 될 수 있으므로 HBM이나 3D stacked memory를 적용하고 memory bandwidth utilization, accelerator idle ratio로 확인함

## Ⅶ. 결론

DRAM·SRAM 선택은 우열이 아니라 속도·용량·비용을 어느 계층에 배치해야 전체 지연과 전력 비용이 줄어드는지의 문제임.

## 작성 근거(검토용)

- DRAM과 SRAM은 셀 구조, refresh, 캐시·주기억장치 배치 차이로 설명함
- 모호한 표현은 DRAM access latency, row buffer hit rate, cache energy per access로 구체화함
- 결론은 메모리 우열이 아니라 계층별 속도·용량·비용 배치로 정리함
