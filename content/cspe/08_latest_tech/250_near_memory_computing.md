---
title: "근접 메모리 컴퓨팅 (Near-Memory Computing)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 250
---

# 📖 【암기용】 개념 완전 이해

> 목적: 근접 메모리 컴퓨팅을 PIM과 구분해, 연산기를 DRAM 내부가 아니라 가까운 logic die나 controller에 배치하는 구조로 이해하게 만든다.

## 한눈에
- **개요**: 연산 유닛을 메모리 내부가 아닌 base die, buffer chip, CXL controller 같은 메모리 근접 logic 위치에 배치하는 방식
- **왜 필요한가**: PIM은 DRAM 공정 제약으로 복잡 연산 처리가 제한되므로, logic 공정 성능을 활용하면서 데이터 이동 거리를 줄이는 절충 구조가 필요하다.
- **핵심 직관**: 창고 내부에 소형 도구를 넣는 PIM과 달리, 창고 바로 옆 작업실에 정식 장비를 두는 방식이다.

## 깊이 이해
- **배경·문제의식**: 데이터 이동을 줄이려면 연산기를 메모리 가까이 두어야 하지만, DRAM 내부에 복잡 로직을 넣으면 면적·전력·공정 제약이 발생한다.
- **작동 원리**: Near-Memory Computing은 HBM base die, DIMM buffer, CXL memory controller에 vector engine, filtering unit, compression engine을 넣어 DRAM과 짧은 경로로 데이터를 주고받는다.
- **비유**: 원재료 창고 안에서 가공하지 않고, 창고 옆 작업실에서 바로 처리해 운반 거리를 줄이는 구조다.
- **구체 예시**: HBM stack의 base die에 연산기를 넣거나 CXL memory expander controller에서 scan·filter·compression을 수행하는 방식이 해당된다.
- **흔한 오해·주의점**: 메모리 가까운 연산을 모두 PIM이라고 부르면 안 된다. 기준은 연산 로직 위치이며, DRAM die 내부면 PIM, 별도 logic die면 Near-Memory 또는 PNM이다.

## 연결 개념
- PIM — DRAM die 내부 연산 구조
- CXL Memory Pooling — controller 근접 연산과 결합 가능한 메모리 확장 구조
- HBM Base Die — near-memory 연산 유닛이 위치할 수 있는 대표 logic die

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: Near-Memory Computing은 위치·공정 기준으로 PIM과 구분하고, logic 공정의 연산 범위 이점을 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Near-Memory Computing은 연산 유닛을 DRAM die가 아닌 근접 logic die나 controller에 배치해 데이터 이동 거리를 줄이는 구조임.
> 2. **가치**: DRAM 공정 제약을 피하면서 filtering, aggregation, compression 같은 복잡 연산을 메모리 가까이에서 처리함.
> 3. **판단 포인트**: PIM보다 이동 거리는 길지만 logic 성능과 지원 연산 범위가 넓다는 trade-off로 판단해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| PIM과 구분 확인 | DRAM 내부 vs 별도 logic die | 거리만으로 PIM/PNM 구분 |
| 구조 이해 확인 | base die, buffer chip, CXL controller | 구현 위치 없이 개념만 서술 |
| 적용 판단 확인 | 데이터 이동 감소와 logic 성능 균형 | 범용 CPU 대체로 과장 |

> 요약: 이 문제는 연산 로직 위치와 공정 차이를 기준으로 PIM과 Near-Memory를 구분하는지를 확인한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 메모리 근접 logic 연산
- 배경: PIM은 DRAM 공정 제약으로 복잡한 연산과 고클럭 logic 구현에 한계가 있음.
- 필요성: 데이터 이동 거리를 줄이면서 logic 공정 기반 연산기 성능을 활용해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Host CPU / GPU -> Near-Memory Command -> Logic Die / Controller
Logic Die / Controller -> Short Link -> DRAM / HBM Stack
Logic Engine -> filter / aggregate / compress -> Result -> Host
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Logic Die/Base Die | 연산 유닛 탑재 | DRAM die와 분리 |
| Memory Controller | 주소 변환과 명령 실행 | CXL controller에 위치 가능 |
| Short Link | logic과 DRAM 간 근거리 연결 | TSV, bus, package link |
| Offload Engine | filter, aggregate, compress 수행 | PIM보다 복잡한 연산 가능 |

> 요약: Near-Memory는 DRAM 근처의 logic die나 controller가 데이터를 짧은 경로로 가져와 처리하는 구조다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Host가 offload 명령 전송 -> controller가 대상 address 확인
-> logic engine이 DRAM data를 근거리 접근 -> 연산 수행
-> 결과만 host로 반환 -> telemetry 기록
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | host가 offload 명령과 주소 범위 전달 | command validation |
| 2 | controller가 DRAM 접근 계획 수립 | address mapping |
| 3 | logic engine이 filter·aggregate 수행 | output correctness |
| 4 | 결과 반환과 성능 지표 기록 | traffic reduction |

> 요약: Near-Memory는 host 명령을 controller가 받아 근접 logic에서 처리하고 결과만 반환한다.

---

## Ⅳ. 특징

| 구분 | PIM | Near-Memory Computing | 수치·판단 기준 |
|:---|:---|:---|:---|
| 연산 위치 | DRAM die 내부 | base die, buffer, controller | 위치 기준 명확화 |
| 공정 | DRAM 공정 | logic 공정 | 복잡 연산 지원 |
| 데이터 이동 | bank 내부로 최소 | 짧은 다이·controller 경로 | 이동거리와 대역폭 |
| 적용 연산 | MAC, bitwise 중심 | filter, aggregate, compression | offload op coverage |

> 요약: Near-Memory는 PIM보다 데이터 이동은 남지만 logic 공정으로 더 넓은 연산 범위를 지원한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | PIM bank PU | near-memory logic die | 연산 복잡도 |
| 비용/성능 | 최소 이동, 제한된 logic | 짧은 이동, 복잡 연산 가능 | filter·aggregate 비중 |
| 운영/위험 | 전용 PIM SDK | controller offload API 필요 | driver·runtime 성숙도 |

> 요약: 단순 MAC 중심이면 PIM, filter·aggregate·compression은 Near-Memory가 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 인터커넥트 병목 | logic die와 DRAM 간 대역폭 부족 | TSV·package link sizing | link utilization |
| API 미성숙 | offload programming model 부족 | vendor SDK 검증 | API failure rate |
| 데이터 정합성 | host와 offload engine 동시 접근 | cache flush, coherence policy | consistency error |

> 요약: Near-Memory 리스크는 link 병목, API 성숙도, 정합성이며 controller 수준 검증이 필요하다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| traffic | host 이동량 30% 이상 감소 | performance counter |
| latency | offload 포함 p95 목표 충족 | benchmark trace |
| 정확도 | host 처리 결과와 동일 | golden output comparison |

> 요약: Near-Memory 성과는 이동량 감소, 지연시간, 결과 정합성으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. scan, filter, aggregation, compression처럼 데이터 이동량이 큰 연산을 Near-Memory offload 후보로 분류함.
2. host CPU/GPU와 offload engine의 cache coherence와 memory ordering 정책을 설계 문서에 명시함.
3. CXL controller나 HBM base die 기반 pilot에서 traffic 감소와 p95 latency를 먼저 검증함.

**결론 (2줄):**
- 기술사 판단: 데이터 이동 최소화가 목표이면 PIM, 복잡 연산과 logic 성능이 필요하면 Near-Memory를 선택함.
- 향후 방향: Near-Memory는 CXL memory expander와 HBM base die에 결합되어 메모리 중심 offload 계층으로 확대됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "근접 메모리 컴퓨팅을 설명하시오" | controller 기반 offload 흐름 | PIM 대비 위치·공정 차이 |
| 요구사항 명시형 | "메모리 병목 완화 방안을 제시하시오" | offload 대상 선정과 정합성 절차 | link·API·coherence 리스크 |

> 요약: 설명형은 위치와 동작 구조를, 방안형은 offload 선정과 검증 기준을 중심으로 작성한다.
