---
title: "PIM 메모리 내 처리 (Processing-in-Memory)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 243
---

# 📖 【암기용】 개념 완전 이해

> 목적: PIM을 데이터 이동을 줄이기 위해 DRAM 내부에 연산 유닛을 넣는 구조로 이해하게 만든다.

## 한눈에
- **개요**: DRAM bank 내부 또는 주변에 연산 유닛을 배치해 데이터를 메모리 밖으로 옮기지 않고 처리하는 방식
- **왜 필요한가**: AI 추론의 GEMV, embedding lookup, filtering은 연산보다 데이터 이동이 전력과 지연을 지배하는 경우가 많다.
- **핵심 직관**: 창고 안에 소형 가공 장비를 넣어 물건을 공장까지 옮기지 않고 현장에서 처리하는 방식이다.

## 깊이 이해
- **배경·문제의식**: von Neumann 구조는 연산기와 메모리가 분리되어 있어 대량 데이터를 버스로 옮기는 과정이 에너지와 지연의 병목이 된다.
- **작동 원리**: PIM은 DRAM bank 근처에 MAC 또는 bitwise 연산 유닛을 두고 bank 내부 데이터를 직접 읽어 부분합을 만든 뒤 결과만 host로 반환한다.
- **비유**: 물류센터가 모든 박스를 본사로 보내 검수하는 대신, 각 선반 옆 검수대에서 필요한 항목만 확인하고 결과표만 보내는 방식이다.
- **구체 예시**: HBM-PIM과 GDDR6-AiM은 메모리 bank 병렬성을 활용해 matrix-vector 연산 일부를 메모리 내부에서 수행하는 사례로 소개된다.
- **흔한 오해·주의점**: PIM은 범용 CPU나 GPU를 대체하지 않으며, DRAM 공정의 로직 제약 때문에 단순·반복 연산 중심으로 적용 범위가 제한된다.

## 연결 개념
- In-Memory Computing — 메모리 상주 처리까지 포함하는 상위 개념
- Near-Memory Computing — 연산기를 별도 logic die에 두는 대비 개념
- HBM — PIM이 결합되는 대표 메모리 스택

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: PIM은 데이터 이동 제거 효과와 DRAM 공정 기반 연산 한계를 동시에 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: PIM은 DRAM 내부 또는 bank 근처의 연산 유닛이 데이터를 외부 연산기로 이동시키지 않고 처리하는 구조임.
> 2. **가치**: memory-bound AI 연산에서 bus traffic과 data movement energy를 줄임.
> 3. **판단 포인트**: GEMV·MAC·bitwise처럼 단순 반복 연산에 적용하고, 복잡 연산은 GPU/PNM 경로로 남겨야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 메모리 병목 원리 확인 | von Neumann bottleneck, data movement | 캐시 미스 문제로만 축소 |
| PIM 구조 이해 확인 | DRAM bank, processing unit, 결과 반환 | PNM과 위치 기준 혼동 |
| 적용 한계 판단 확인 | DRAM 공정 로직 제약, 지원 연산 제한 | 범용 연산 대체로 과장 |

> 요약: PIM 문제는 데이터 이동을 줄이는 구조와 적용 가능한 연산 범위를 구분하는지를 확인한다.

---

## Ⅰ. 개요 및 필요성

- 개요: DRAM 내부 연산 구조
- 배경: AI 추론의 데이터 이동이 연산보다 전력·지연을 더 크게 만드는 memory wall이 발생함.
- 필요성: bank 내부 연산으로 원본 데이터 이동량을 줄이고 결과만 host로 반환해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Host CPU / GPU -> PIM Command -> DRAM Bank
DRAM Bank -> Processing Unit(MAC / bitwise) -> Partial Sum
Partial Sum -> Reduction -> Result -> Host
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| DRAM Bank | 데이터 저장과 로컬 접근 제공 | bank 병렬성이 연산 병렬성으로 전환 |
| Processing Unit | MAC, bitwise, 누산 수행 | DRAM 공정 기반 경량 로직 |
| PIM Command | host가 연산 대상과 명령 전달 | 기존 DRAM 명령 확장 필요 |
| Reduction Logic | bank별 부분합 결합 | 결과 크기만 host로 반환 |

> 요약: PIM은 DRAM bank와 processing unit을 결합해 bank별 로컬 데이터를 처리하고 결과만 외부로 보낸다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Host가 연산 명령 전송 -> 대상 bank 선택 -> PU 활성화
-> bank local data로 MAC / bitwise 처리 -> partial sum 생성
-> reduction -> 최종 결과 반환
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | host가 PIM 명령과 operand 위치 전달 | 명령 decoding 정확도 |
| 2 | bank별 PU가 local data 접근 | bank conflict 비율 |
| 3 | PU가 단순 반복 연산 수행 | 결과 오차율 |
| 4 | partial sum을 결합해 반환 | host traffic 감소율 |

> 요약: PIM은 bank 단위 병렬 연산으로 원본 데이터 이동을 줄이고 결과 반환만 수행한다.

---

## Ⅳ. 특징

| 구분 | 기존 CPU/GPU 처리 | PIM | 수치·판단 기준 |
|:---|:---|:---|:---|
| 데이터 이동 | DRAM에서 연산기로 원본 이동 | bank 내부 처리 후 결과 이동 | traffic reduction |
| 연산 범위 | 범용 연산 가능 | MAC, GEMV, bitwise 중심 | 지원 op coverage |
| 공정 | logic 공정 | DRAM 공정 기반 | 복잡 로직 제약 |
| 소프트웨어 | CUDA, BLAS 등 성숙 | 전용 compiler·SDK 필요 | toolchain maturity |

> 요약: PIM은 데이터 이동량 감소가 장점이고, 지원 연산과 소프트웨어 생태계가 제약이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | processor-centric | memory-centric bank PU | 데이터 이동량이 연산량보다 큰지 |
| 비용/성능 | 범용성, 높은 bus traffic | 낮은 traffic, 제한된 연산 | 지원 op 비율 80% 이상 |
| 운영/위험 | 성숙한 tooling | 전용 SDK와 검증 필요 | 개발 생태계 수용 가능성 |

> 요약: PIM은 memory-bound 단순 연산 비중이 큰 구간에 한정해 적용해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 연산 불일치 | DRAM 내부 정밀도·누산 차이 | golden output 비교, 오차 허용 기준 | accuracy loss |
| SDK 미성숙 | 전용 compiler 부족 | 특정 kernel만 pilot 적용 | build success rate |
| 열·전력 집중 | bank 내부 연산 활성화 증가 | power gating, thermal policy | die temperature |

> 요약: PIM 리스크는 정확도, SDK, 열이며 제한된 kernel부터 검증하는 접근이 필요하다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| traffic | host memory traffic 30% 이상 감소 | performance counter |
| 정확도 | baseline 대비 오차 허용 범위 이내 | output comparison |
| 처리량 | target kernel throughput 개선 | microbenchmark |

> 요약: PIM 도입 성과는 traffic 감소, 정확도, kernel 처리량으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. LLM inference의 GEMV, 추천 embedding 연산처럼 memory-bound kernel을 식별해 PIM offload 후보로 선정함.
2. 미지원 연산은 GPU/CPU 경로로 유지하고 PIM 지원 kernel만 compiler pass로 분리함.
3. golden output과 telemetry를 기준으로 정확도 손실, traffic 감소, die temperature를 운영 검증함.

**결론 (2줄):**
- 기술사 판단: 단순 반복 memory-bound 연산은 PIM, 복잡 연산과 생태계 의존 업무는 GPU 또는 PNM을 선택함.
- 향후 방향: PIM은 HBM, CXL memory expander, AI serving과 결합해 데이터 이동 절감 계층으로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "PIM을 설명하시오" | bank 내부 연산 흐름 | 기존 처리 대비 데이터 이동 차이 |
| 요구사항 명시형 | "메모리 병목 개선 방안을 제시하시오" | offload kernel 식별 절차 | 지원 연산·SDK·정확도 리스크 |

> 요약: 설명형은 bank 내부 동작을, 방안형은 offload 대상 선정과 검증 기준을 중심으로 작성한다.
