---
title: "병렬 알고리즘 — PRAM 모델 (Parallel Algorithm PRAM)"
date: "2026-07-07"
tags:
  - "cspe-basic-theory"
weight: 79
---


## Ⅰ. 개요

- **정의/개념**: 다수의 프로세서가 공유 메모리($Shared$ $Memory$)를 통해 데이터를 주고받으며 문제를 독립적인 부문제($Sub$-$tasks$)로 분할하여 동시에 해결하는 알고리즘과, 이를 분석하기 위한 추상적 계산 모델임
- **배경/필요성**: 단일 코어의 물리적 한계($Power$ $Wall$) 직면으로 인해 멀티코어 및 $GPU$ 기반 병렬 처리가 필수화됨. 알고리즘의 순수한 병렬적 잠재력($Potential$ $Parallelism$)을 평가하고, 통신 지연이 배제된 상태에서의 이상적인 성능 가속도를 측정하기 위해 $PRAM$($Parallel$ $Random$ $Access$ $Machine$) 모델 기반 분석이 요구됨

## Ⅱ. 특징 및 비교

### 1. $PRAM$ 메모리 접근 모델별 비교

| 모델명 | 읽기 ($Read$) | 쓰기 ($Write$) | 특징 및 하드웨어 정합성 |
|:---|:---:|:---:|:---|
| **$EREW$** | 배타적 ($Exclusive$) | 배타적 ($Exclusive$) | 가장 엄격한 모델, 물리적 충돌 방지 로직 불필요 |
| **$CREW$** | **동시적 ($Concurrent$)** | 배타적 ($Exclusive$) | 보편적인 병렬 모델 (읽기 공유 가능, 쓰기 순차화) |
| **$CRCW$** | **동시적 ($Concurrent$)** | **동시적 ($Concurrent$)** | 가장 강력한 표현력, 충돌 해결 정책($Conflict$ $Policy$) 필수 |

> 요약: $EREW$는 하드웨어 구현이 용이하나 알고리즘 설계가 까다롭고, $CRCW$는 알고리즘적 성능은 높으나 복잡한 동기화 제어가 요구됨

### 2. $PPA$ 및 트레이드오프 ($Trade$-$offs$)
- **Performance**: 가속도($Speedup$) $S = \frac{T_1}{T_p}$는 이론적으로 프로세서 수 $p$에 비례해야 하나, 실제로는 동기화 지연으로 인해 상한선에 수렴함
- **Amdahl's Law**: $S = \frac{1}{(1-f) + \frac{f}{p}}$ 수식에 따라, 병렬화 불가능한 순차적 영역($1-f$)이 전체 성능 향상의 병목($Bottleneck$)이 됨
- **Trade-off**: 프로세서 수를 늘릴수록 처리량($Throughput$)은 증가하나, 프로세서 간 데이터 정합성 유지 비용($Coherency$ $Cost$)이 기하급수적으로 증가하여 효율성($Efficiency$)은 저하됨

## Ⅲ. 구성요소/구조

### 1. $PRAM$ 모델 아키텍처 인사이트 ($Architecture$ $Insight$)
- **Processing Elements ($PEs$)**: 동일한 성능을 가진 $p$개의 독립적인 연산 유닛
- **Global Shared Memory**: 모든 $PE$가 $O(1)$ 시간에 접근 가능하다고 가정한 논리적 메모리 공간
- **Read/Write Conflict Resolution**: $CRCW$ 모델에서의 동시 쓰기 전략
  - **Common**: 모든 $PE$가 동일한 값을 쓸 때만 수용
  - **Priority**: $PE$의 고유 $ID$ 순서에 따라 우선순위 부여
  - **Random**: 임의의 $PE$ 하나만 쓰기 성공 처리

### 2. 병렬 처리 파이프라인
```text
[Input Data] -> [Task Decomposition] -> [Data Mapping] -> [Parallel Execution] -> [Reduction/Merge]
      |                |                      |                   |                   |
   전체 문제       독립 작업 분할         PE별 메모리 할당      동시 연산 수행        최종 결과 합산
```

## Ⅳ. 문제점 및 개선방안

### 1. 실무적 문제점 및 대응 전략
1. **[이론과 실제의 괴리 (Communication Delay)]**: $PRAM$은 실제 하드웨어의 메모리 레이턴시와 네트워크 버스 병목을 무시함
   - **개선방안**: 실제 설계 시 통신 비용을 반영한 $LogP$ 모델이나 $BSP$($Bulk$ $Synchronous$ $Parallel$) 모델을 활용하여 성능 예측 정밀도 향상 (확인: 실제 측정치와 오차율)
2. **[부하 불균형 (Load Imbalance)]**: 데이터 분포 불균등으로 특정 $PE$만 과부하가 걸리고 나머지는 대기 상태($Idle$)가 되는 문제
   - **개선방안**: 작업을 정적으로 나누지 않고 런타임에 유휴 $PE$가 작업을 가져가는 $Work$ $Stealing$ 기법 도입 (확인: $PE$별 사용률 편차)
3. **[거짓 공유 (False Sharing)]**: 서로 다른 $PE$가 동일한 캐시 라인 내의 다른 데이터를 수정할 때 불필요한 무효화($Invalidation$)가 발생하는 현상
   - **개선방안**: 데이터 구조체 사이에 패딩($Padding$)을 추가하여 캐시 라인을 격리함 (확인: $L1/L2$ 캐시 미스율)

### 2. 리얼월드 트러블슈팅 ($Real$-$world$ $Troubleshooting$)
- **상황**: $GPU$ 기반 행렬 연산 중 스레드 수($p$)를 늘렸음에도 불구하고 성능이 오히려 하락하는 '병렬화 역전' 발생
- **해결**: 작고 빈번한 데이터 전송 오버헤드가 연산 이득을 초과함을 식별하고, $Batch$ 처리를 통해 전송 횟수를 줄이고 연산 밀도($Arithmetic$ $Intensity$)를 높임

## Ⅴ. 실무 적용 사례

| 적용 영역 | 적용 기술 | 확인 지표 |
|:---|:---|:---|
| **$GPU$ 가속 ($CUDA$)** | $SIMT$ 아키텍처 | $Memory$ $Bandwidth$, $Kernel$ $Execution$ $Time$ |
| **빅데이터 분산 처리** | $MapReduce$ / $Spark$ | 데이터 파티셔닝 균형도, 셔플링($Shuffling$) 비용 |
| **금융 공학 시뮬레이션** | $OpenMP$ ($Multi$-$threading$) | $Speedup$ $Ratio$, $CPU$ 가동률 |

## Ⅵ. 결론

병렬 알고리즘은 '순차적 사고'라는 인간의 본능적 한계를 넘어 '동시적 실행'이라는 기계적 잠재력을 극대화하는 기술임. $PRAM$ 모델은 비록 하드웨어적 제약을 추상화했으나, 알고리즘의 순수한 확장성을 검증하는 데 여전히 유효한 잣대임. 최근에는 대규모 언어 모델($LLM$) 학습을 위한 분산 병렬화($Pipeline/Tensor$ $Parallelism$)가 핵심 경쟁력으로 부상하고 있으며, 기술사는 하드웨어 토폴로지를 고려한 최적의 병렬 구조 설계 역량을 갖춰야 함.
