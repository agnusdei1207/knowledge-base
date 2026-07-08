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
- 두 메모리는 속도와 집적도와 전력 특성이 달라 계층 구조에서 역할이 다름

## Ⅰ. 개요

- **정의/개념**: DRAM은 1T1C 셀에 전하를 저장해 높은 집적도로 큰 용량을 제공하는 동적 메모리이고, SRAM은 플립플롭 기반 셀로 빠른 접근과 안정된 유지 특성을 제공하는 정적 메모리임
- **배경/필요성**: 시스템은 CPU에 가까운 초저지연 저장층과 대용량 주기억장치를 동시에 요구하므로, 속도 중심의 SRAM과 용량 중심의 DRAM을 계층적으로 함께 사용함

## Ⅱ. 특징

- DRAM은 집적도와 비용 효율이 좋아 주기억장치로 적합함
- SRAM은 refresh가 없어 지연이 짧고 캐시로 쓰기에 유리함
- DRAM은 refresh와 row access 제약 때문에 대역폭과 지연 최적화가 중요함
- SRAM은 면적과 누설 전력이 커서 대용량 확장이 어렵고 비용 부담이 큼

## Ⅲ. 종류 및 비교

| 판단 기준 | DRAM | SRAM |
|:---|:---|:---|
| 저장 방식 | 커패시터 전하를 저장하고 주기적으로 refresh함 | 플립플롭 회로 상태를 유지해 refresh가 필요 없음 |
| 속도 | 상대적으로 느리지만 대용량화가 쉬움 | 매우 빠르지만 면적당 용량이 작음 |
| 비용 | 비트당 비용이 낮음 | 비트당 비용이 높음 |
| 대표 용도 | 메인 메모리와 대용량 버퍼 | L1, L2, L3 캐시와 소형 고속 버퍼 |

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

## Ⅵ. 문제점 및 해결 방안

1. 문제: DRAM은 refresh와 row conflict가 겹치면 지연이 길어져 CPU가 memory stall에 자주 빠질 수 있음
   - 해결방안: bank interleaving과 row policy tuning을 적용하고 DRAM access latency와 row buffer hit rate로 검증함
2. 문제: SRAM은 용량을 늘릴수록 칩 면적과 누설 전력이 급격히 커져 캐시 확장 효율이 떨어짐
   - 해결방안: cache partitioning과 low-leakage design을 적용하고 cache energy per access와 area efficiency로 검증함
3. 문제: AI와 HPC 워크로드는 DRAM의 대역폭 한계를 빠르게 드러내 상위 연산기의 활용률을 떨어뜨릴 수 있음
   - 해결방안: HBM이나 3D stacked memory를 적용하고 memory bandwidth utilization과 accelerator idle ratio로 검증함

## Ⅶ. 적용 사례

- 범용 서버는 SRAM 기반 L3 캐시와 DRAM 주기억장치를 조합해 평균 지연을 낮추고 확인 지표는 cache miss rate와 memory stall ratio임
- 그래픽과 AI 가속기는 DRAM 대역폭을 넓힌 GDDR이나 HBM을 사용해 연산 유휴를 줄이고 확인 지표는 memory bandwidth utilization과 accelerator idle ratio임
- 저전력 임베디드 장치는 소용량 SRAM 중심 구성을 채택해 단순성과 응답성을 확보하고 확인 지표는 standby power와 interrupt response time임

## Ⅷ. 결론

DRAM과 SRAM의 선택은 어느 메모리가 더 우수한지의 문제가 아니라 속도와 용량과 비용을 어느 계층에 배치해야 전체 시스템이 가장 효율적으로 동작하는지의 문제임.
