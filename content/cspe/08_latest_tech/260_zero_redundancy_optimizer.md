---
title: "ZeRO Optimizer 제로 중복 최적화 (Zero Redundancy Optimizer)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 260
---

# 📖 【암기용】 개념 완전 이해

> 목적: ZeRO를 데이터 병렬에서 모든 GPU가 중복 보유하던 학습 상태를 나누어 저장하는 메모리 최적화로 이해하게 만든다.

## 한눈에
- **개요**: Data Parallel 학습의 optimizer state, gradient, parameter 중복을 rank별 shard로 분산하는 최적화 기법
- **왜 필요한가**: 대형 모델은 parameter보다 optimizer state와 gradient까지 합친 학습 메모리가 커서 단순 DDP만으로 GPU memory가 부족하다.
- **핵심 직관**: 모든 사람이 같은 두꺼운 장부 전체를 들고 다니는 대신, 각자 담당 페이지를 보관하고 필요할 때만 빌려 보는 방식이다.

## 깊이 이해
- **배경·문제의식**: Adam optimizer는 parameter 외에 momentum, variance 같은 상태를 저장해 학습 메모리를 크게 만든다. Data Parallel은 이 상태를 모든 rank가 중복 보유한다.
- **작동 원리**: ZeRO Stage 1은 optimizer state, Stage 2는 optimizer state와 gradient, Stage 3은 optimizer state, gradient, parameter까지 rank별로 분할한다.
- **비유**: 공동 프로젝트 자료를 모두가 복사해 갖는 대신, 문서 페이지를 나눠 맡고 회의 때 필요한 페이지를 서로 공유하는 방식이다.
- **구체 예시**: ZeRO-3는 forward/backward 시점에 필요한 parameter shard를 모아 쓰고, 사용 후 다시 shard 상태로 유지해 peak memory를 줄인다.
- **흔한 오해·주의점**: ZeRO는 모델 구조를 바꾸는 병렬화가 아니다. Data Parallel의 중복 상태를 분산하는 메모리 최적화이며 통신량은 stage가 깊어질수록 증가할 수 있다.

## 연결 개념
- Data Parallelism — ZeRO가 최적화하는 기본 학습 구조
- Reduce-Scatter / All-Gather — ZeRO 통신의 핵심 collective
- Offload — CPU/NVMe로 state를 넘겨 GPU memory를 더 줄이는 방식

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: ZeRO는 stage별 sharding 대상과 memory/communication trade-off를 구분해 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ZeRO는 Data Parallel rank가 중복 보유하던 optimizer state, gradient, parameter를 shard로 나누는 메모리 최적화임.
> 2. **가치**: 대형 모델 학습에서 GPU당 학습 상태 memory를 줄여 더 큰 모델 또는 batch를 실행하게 함.
> 3. **판단 포인트**: Stage 1/2/3의 메모리 절감 범위와 all-gather/reduce-scatter 통신 증가를 함께 평가해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| ZeRO 단계 이해 확인 | Stage 1 optimizer, Stage 2 gradient, Stage 3 parameter | 세 단계를 구분하지 않음 |
| DP redundancy 원인 확인 | replica별 학습 상태 중복 | 모델 병렬과 혼동 |
| 적용 판단 확인 | memory 절감 vs 통신/오프로딩 비용 | 메모리 절감만 쓰고 step time 누락 |

> 요약: 이 문제는 ZeRO를 data parallel state sharding으로 설명하고 stage별 trade-off를 판단하는지를 확인한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 학습 상태 중복 제거
- 배경: Data Parallel은 각 GPU가 parameter, gradient, optimizer state를 중복 보유해 대형 모델 학습 시 GPU memory가 부족해짐.
- 필요성: 학습 상태를 rank별 shard로 나누고 필요한 시점에 collective로 모아 memory와 통신 비용을 균형화해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Data Parallel Ranks -> State Partition Planner
-> Optimizer State Shard / Gradient Shard / Parameter Shard
-> Reduce-Scatter / All-Gather -> Forward / Backward / Optimizer Step
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Optimizer State Shard | Adam momentum/variance 분산 저장 | ZeRO-1부터 적용 |
| Gradient Shard | rank별 gradient partition 유지 | ZeRO-2부터 적용 |
| Parameter Shard | parameter도 분산 저장 | ZeRO-3에서 적용 |
| Offload Engine | CPU/NVMe로 state 이동 | bandwidth와 latency 영향 |

> 요약: ZeRO는 optimizer, gradient, parameter를 단계별로 shard하고 collective로 필요한 상태를 교환한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Model 초기화 -> State Sharding -> Forward 시 Parameter Gather
-> Backward 시 Gradient Reduce-Scatter -> Optimizer State Shard Update -> Checkpoint 저장
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 학습 상태를 rank별 shard로 분할 | shard metadata |
| 2 | forward에 필요한 parameter를 all-gather | gather latency |
| 3 | backward gradient를 reduce-scatter | gradient parity |
| 4 | 각 rank가 담당 optimizer state 갱신 | optimizer state checksum |

> 요약: ZeRO는 필요한 순간에 parameter를 모으고 gradient를 다시 나누어 각 rank가 담당 shard만 갱신한다.

---

## Ⅳ. 특징

| 구분 | DDP | ZeRO-1 | ZeRO-2 | ZeRO-3 |
|:---|:---|:---|:---|:---|
| Optimizer state | 전체 중복 | shard | shard | shard |
| Gradient | 전체 중복 | 전체 중복 | shard | shard |
| Parameter | 전체 중복 | 전체 중복 | 전체 중복 | shard |
| 통신 부담 | All-Reduce 중심 | 낮음 | 중간 | 높음 |

> 요약: ZeRO는 단계가 깊어질수록 GPU memory 중복은 줄지만 parameter gather와 shard 통신이 증가한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | DDP full replica | ZeRO sharded state | peak memory 부족 여부 |
| 비용/성능 | 통신 단순 | collective와 offload 비용 추가 | memory 절감 대비 step time |
| 운영/위험 | checkpoint 단순 | sharded checkpoint 관리 | 재시작 절차 |

> 요약: ZeRO는 memory 부족 문제를 직접 해결하지만 stage 선택은 통신 비용과 checkpoint 운영을 포함해 결정해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 통신 증가 | parameter gather와 reduce-scatter 반복 | bucket sizing, overlap | communication time |
| offload 병목 | CPU/NVMe bandwidth 부족 | pin memory, NVMe throughput 검증 | offload wait time |
| checkpoint 복잡도 | shard metadata 불일치 | periodic restore test | restore success rate |

> 요약: ZeRO 운영 리스크는 통신, offload, checkpoint이며 stage별 복구 테스트가 필요하다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| memory | rank별 peak memory 한도 이내 | GPU memory stats |
| step time | ZeRO stage 변경 후 허용 범위 | profiler |
| 복구 | sharded checkpoint restore 성공 | disaster recovery drill |

> 요약: ZeRO 적용은 memory 절감과 step time, checkpoint 복구 가능성을 함께 통과해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. DDP baseline의 parameter, gradient, optimizer state memory를 산정한 뒤 ZeRO stage를 1 -> 2 -> 3 순서로 올리며 검증함.
2. Stage 3 또는 offload 적용 시 all-gather, reduce-scatter, offload wait time을 profiler로 분해함.
3. Sharded checkpoint 저장·복구 절차를 job preemption과 node 장애 시나리오로 테스트함.

**결론 (2줄):**
- 기술사 판단: 모델은 GPU에 들어가지만 학습 상태가 memory를 초과하면 ZeRO를 우선 적용하고, 모델 자체가 초과하면 tensor/pipeline parallel을 병행함.
- 향후 방향: ZeRO는 3D parallel training과 CPU/NVMe offload를 결합해 trillion-parameter 학습의 기본 memory 계층으로 활용됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "ZeRO Optimizer를 설명하시오" | state sharding과 gather/scatter 흐름 | Stage 1/2/3 차이 |
| 요구사항 명시형 | "대형 모델 memory 절감 방안을 제시하시오" | stage 선택과 offload 검증 절차 | 통신·checkpoint 리스크 |

> 요약: 설명형은 ZeRO 단계 구조를, 방안형은 memory 산정과 stage별 운영 기준을 중심으로 작성한다.
