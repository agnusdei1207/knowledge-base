---
title: "폴락의 법칙 (Pollack's Rule)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 15
---

## 미리 알고가기

- Die area: 칩 위에서 코어, 캐시, 인터커넥트가 차지하는 면적임
- 전력·성능·면적(Power, Performance, Area, PPA): 반도체 설계에서 세 요소를 함께 보는 평가 축임
- Diminishing return: 투입 자원 증가 대비 성능 증가가 점차 줄어드는 현상임
- Throughput core: 단일 성능보다 전력 대비 처리량을 중시한 작은 코어 설계임

## Ⅰ. 개요

- **정의**: 폴락의 법칙은 단일 프로세서 코어의 성능 향상이 해당 코어에 투입한 면적 증가의 제곱근 정도에 그친다는 경험 법칙임. 복잡한 큰 코어와 여러 작은 코어 중 어떤 구성이 PPA 측면에서 유리한지 판단하는 데 쓰임.
- **배경/필요성**: OoO, superscalar, cache, predictor를 키우면 면적과 전력은 크게 늘지만 단일 스레드 성능은 제한적으로 증가함. 이 법칙은 단일 코어 대형화보다 멀티코어와 특화 가속기 전략이 등장한 배경을 설명함.
- **비유**: 한 작업자의 책상과 장비를 네 배로 늘려도 작업 속도가 네 배가 되지 않고 두 배 안팎에 그치는 상황임.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 단일 코어 복잡도와 멀티코어 전환 배경 설명 | 성능~면적 제곱근, PPA, 병렬성, 한계 | 수학 법칙처럼 절대값으로 적용 |

> 요약: 폴락의 법칙은 큰 코어 대형화의 수익 체감을 설명하는 설계 판단 도구임.

## Ⅱ. 특징/비교

| 판단 기준 | 큰 단일 코어 확대 | 여러 작은 코어 구성 |
|:---|:---|:---|
| 성능 증가 | 단일 스레드 성능은 개선되지만 면적 대비 수익이 감소함 | 병렬 작업 처리량을 면적 대비 높일 수 있음 |
| 전력 특성 | 복잡한 control과 wide datapath로 전력 밀도가 높음 | 낮은 클록과 단순 구조로 perf/W가 유리할 수 있음 |
| 소프트웨어 조건 | 순차 프로그램에 유리함 | 병렬화 가능한 workload가 필요함 |
| 적용 기준 | latency-critical core, big core | throughput server, many-core, heterogeneous SoC |

> 요약: 큰 코어는 지연시간, 작은 코어 다수는 병렬 처리량과 perf/W를 선택하는 방향임.

## Ⅲ. 구성요소

```text
+-------------+      +------------------+      +---------------+
| Area Budget | ---> | Core Complexity  | ---> | Performance   |
+-------------+      +---------+--------+      +-------+-------+
                             |                       |
                             v                       v
                       +-----------+           +-------------+
                       | Power     |           | PPA Choice  |
                       +-----------+           +-------------+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| 면적 예산 | 코어, 캐시, 인터커넥트에 배분할 수 있는 물리 자원임 | 건축 부지 |
| 복잡도 요소 | OoO window, issue width, predictor, cache 같은 성능 구조임 | 설비 고급화 |
| 성능 곡선 | 면적 증가 대비 성능 증가가 점차 완만해지는 관계임 | 체력 한계 |
| PPA 판단 | 전력, 성능, 면적을 함께 고려해 코어 수와 크기를 정함 | 예산 심사 |

> 요약: 폴락의 법칙은 면적 투입, 코어 복잡도, 성능 증가, 전력 비용의 관계를 보는 구조임.

## Ⅳ. 절차

```text
+----------+     +----------+     +----------+     +----------+
| Workload | --> | Estimate | --> | Compare  | --> | Decide   |
+----------+     +----------+     +----------+     +----------+
 latency/TP       perf-area        big/small        PPA target
```

1. **업무 특성 파악** - 단일 스레드 지연시간과 병렬 처리량 중 우선순위를 정함
2. **면적-성능 추정** - 코어 복잡도 증가가 성능과 전력에 주는 효과를 추정함
3. **대안 비교** - 큰 코어 1개, 작은 코어 다수, heterogeneous 구성을 비교함
4. **구조 결정** - PPA와 소프트웨어 병렬화율을 기준으로 최종 아키텍처를 선택함

> 요약: 폴락의 법칙은 workload별 PPA 대안을 비교해 단일 코어 확대의 한계를 판단하는 절차임.

## Ⅴ. 문제점 및 개선방안

- **P1 경험 법칙의 단순화**: 공정, 캐시, 메모리, workload에 따라 관계가 달라져 절대 공식처럼 쓰면 오류가 큼
- **P1 대응**: 실제 benchmark, cycle model, silicon telemetry로 면적-성능 가정을 보정함 (확인: 표준 성능 평가 협회(Standard Performance Evaluation Corporation, SPEC) benchmark, workload IPC)
- **P2 병렬화 전제 부족**: 작은 코어 다수가 유리하려면 소프트웨어가 충분히 병렬화되어야 함
- **P2 대응**: Amdahl/Gustafson 분석과 병렬 런타임 검증으로 코어 수 확장성을 확인함 (확인: speedup, CPU utilization)
- **P3 전력·메모리 무시 위험**: 면적만 보고 판단하면 thermal, memory bandwidth, interconnect 병목을 놓칠 수 있음
- **P3 대응**: roofline model, thermal model, memory bandwidth model을 함께 적용함 (확인: bandwidth saturation, throttling)

> 요약: 폴락의 법칙은 방향성을 주지만 실제 설계는 workload와 PPA 전체로 보정·검증해야 함.

## Ⅵ. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| 중앙처리장치(Central Processing Unit, CPU) 코어 포트폴리오 | big core 확대와 throughput core 다수 배치를 단일 스레드 지연시간, 병렬화율, 전력·성능·면적(Power, Performance, Area, PPA) 목표로 비교함 | p95 latency, speedup, 와트당 성능(performance per watt, perf/W) |
| 서버 many-core 설계 | 면적을 코어 수, 최종 단계 캐시(Last-Level Cache, LLC), 메모리 컨트롤러에 배분하기 전에 memory bandwidth와 interconnect 병목을 모델링함 | bandwidth saturation, LLC miss, 면적당 성능(performance per square millimeter, perf/mm2) |
| 시스템온칩(System on Chip, SoC) 가속기 선택 | 범용 코어 확대보다 특정 kernel 전용 accelerator가 PPA를 개선하는지 workload별로 검증함 | area budget, accelerator utilization, energy/op |

> 요약: 폴락의 법칙은 큰 코어 확대, 작은 코어 다수, 전용 가속기 중 무엇이 PPA 목표를 만족하는지 가르는 초기 판단 기준임.

## Ⅶ. 전망

- **발전 방향**: 단일 큰 코어 확대보다 big.LITTLE, chiplet, accelerator, near-memory computing처럼 면적을 기능별로 배분하는 이기종 설계가 확대됨
- **기술사적 판단**: 큰 코어와 작은 코어의 비율은 단일 스레드 지연, 처리량, `perf/W`, `perf/mm2`, scheduler 정책, 메모리 대역폭을 기준으로 정해야 함; 폴락의 법칙은 경험식이므로 실제 silicon, thermal limit, workload benchmark, 병렬화율을 측정해 초기 추정을 보정함
- **기술사 제언**: "면적 2배면 성능은 선형 증가하지 않는다"는 직관을 멀티코어·이기종 전환 배경과 함께 설명해야 함
