---
sidebar:
  order: 52
  label: "052. 병렬 컴퓨터 분류: Flynn 분류 (Flynn's Taxonomy)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "병렬 컴퓨터 분류: Flynn 분류 (Flynn's Taxonomy)"
date: "2026-08-13T12:00:06+09:00"
tags:
  - "notes-hardware"
weight: 52
extra:
  question_no: "052"
  source_status: "기출"
  source_history: "131회, 134회"
  priority: 70
  priority_note: "명령•데이터 스트림 2×2 분류"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **플린 분류(Flynn's Taxonomy)**: 컴퓨터 아키텍처를 독립적인 인스트럭션 스트림과 데이터 스트림의 수량(단일/다중)에 따라 4가지로 분류한 체계.
- **명령 스트림(Instruction Stream)**: 제어 유닛(Control Unit)에 의해 읽혀 수행되는 인스트럭션 실행의 직렬/병렬 시퀀스.
- **데이터 스트림(Data Stream)**: 프로세서 연산 장치(ALU)로 인가되는 피연산 수치 데이터 시퀀스.

</details>

- 정의/개념: 분석 경계 내 **명령 스트림**과 **데이터 스트림** 수의 조합으로 병렬 컴퓨터 구조를 분류하는 **플린 분류**
- 배경/필요성: 단순 처리기(ALU) 수량 분류 방식의 한계를 극복하고 제어 흐름과 데이터 병렬화 방식을 명확히 구분할 체계 필요

#### 한줄 요약

- 플린 분류는 독립 명령·데이터 스트림 수를 각각 단일·다중으로 판정해 SISD·SIMD·MISD·MIMD로 구분한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **독립 명령 스트림(Independent Instruction Stream)**: 개별 제어 유닛이 독자적으로 분기하고 실행하는 명령 시퀀스.
- **독립 데이터 스트림(Independent Data Stream)**: 병렬 ALU 레인으로 동시에 독립 공급되는 피연산 텐서/벡터 배열.
- **분석 경계(Analysis Boundary)**: 분류 대상 프로세서를 코어, 칩, 멀티 노드 등 어느 레이어 관점에서 바라볼 것인지 정하는 기준 선정.

</details>

- 제어 주체 유닛 수량을 판정하는 **독립 명령 스트림** 기준 분류
- 동시 연산 처리 대역폭을 결정하는 **독립 데이터 스트림** 조합
- 분석 대상 관점의 혼선을 방지하기 위한 **분석 경계** 지정

#### 한줄 요약

- 처리기 수가 아니라 고정한 분석 경계 안의 독립 제어 흐름과 동시 데이터 흐름 수로 병렬 구조를 판정한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **2×2 분류 행렬(2×2 Classification Matrix)**: Instruction Stream(S/M)과 Data Stream(S/M)의 조합으로 교차 매핑하는 분류 매트릭스.
- **코어/칩/노드(Core/Chip/Node)**: 플린 분류를 적용하는 시스템 분석 계층의 단위 레벨.

</details>

| 구성요소 | 책임 |
|:---|:---|
| 분석 경계 | 코어, 칩, 멀티 칩 클러스터 노드 관점 레이어 지정 |
| 명령 스트림 수 | 단일(Single) 제어 유닛 vs 다중(Multiple) 제어 유닛 판정 |
| 데이터 스트림 수 | 단일(Single) 데이터 파이프라인 vs 다중(Multiple) 데이터 파이프라인 판정 |
| 2×2 분류 행렬 | 조합에 따라 SISD, SIMD, MISD, MIMD로 최종 분류 매핑 |

#### 한줄 요약

- 분석 범위를 정한 뒤 명령과 데이터 흐름 수를 조합해 네 구조로 분류한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **스트림 계수(Stream Counting)**: 타깃 아키텍처 내부의 제어 흐름과 데이터 레인 수를 정확히 계측하는 작업.
- **분류 일관성(Classification Consistency)**: 동일 분석 경계 레이어를 유지함으로써 유형 평가 오해를 방지하는 원칙.

</details>

```text
1. 분석 경계 설정
        |
2. 명령 스트림 수 판정
   ├─ 단일
   └─ 다중
        |
3. 데이터 스트림 수 판정
   ├─ 단일
   └─ 다중
        |
4. 2×2 행렬에 매핑
   ├─ 단일·단일: SISD
   ├─ 단일·다중: SIMD
   ├─ 다중·단일: MISD
   └─ 다중·다중: MIMD
```

### 동작 원리

1. **분석 경계 설정**: 시스템 내 **스트림 계수**를 위한 코어/칩/노드 수준 기준 계층 정의.
2. **명령 스트림 수 판정**: 지정 경계 내 독자 분기 제어를 수행하는 **명령 스트림** 수(Single vs Multiple) 판정.
3. **데이터 스트림 수 판정**: 동일 시점에 연산 인가되는 **데이터 스트림** 수(Single vs Multiple) 판정.
4. **2×2 행렬 매핑**: 판정된 두 조합을 **2×2 분류 행렬**에 대입하여 최종 분류 지정.

#### 한줄 요약

- 코어·칩·노드 중 분석 경계를 고정한 뒤 독립 명령·데이터 스트림 수를 2×2 행렬에 대응한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **SISD(Single Instruction, Single Data)**: 단일 명령어로 단일 데이터를 순차 연산 처리하는 클래식 구조(예: 파이프라인 스칼라 CPU).
- **SIMD(Single Instruction, Multiple Data)**: 하나의 명령어로 다수의 데이터 레인을 동시 병렬 처리하는 구조(예: AVX-512, 2D 텐서 연산기).
- **MISD(Multiple Instruction, Single Data)**: 다수의 명령어가 하나의 데이터 스트림을 중복 검증 처리하는 구조(예: 우주/결함 허용 시스템).
- **MIMD(Multiple Instruction, Multiple Data)**: 다수의 제어기가 각자 독립된 명령으로 서로 다른 데이터를 처리하는 멀티코어/분산 컴퓨팅 구조.

</details>

| Flynn 분류 | 명령 스트림 | 데이터 스트림 | 아키텍처 특성 | 적용 예시 |
|:---|:---|:---|:---|:---|
| **SISD** | 단일 (Single) | 단일 (Single) | 단일 제어유닛 기반 스칼라 순차 처리 | 클래식 단일 코어 CPU 파이프라인 |
| **SIMD** | 단일 (Single) | 다중 (Multiple) | 단일 제어유닛으로 다중 ALU 데이터 벡터 연산 | CPU AVX/NEON, GPU 텐서 코어 |
| **MISD** | 다중 (Multiple) | 단일 (Single) | 동일 입력 데이터 대상 복수 파이프라인 다중 검증 | 우주 항공 결함 허용(Fault-tolerant) 시스템 |
| **MIMD** | 다중 (Multiple) | 다중 (Multiple) | 독립 제어유닛 기반 비동기 파이프라인 동시 구동 | 멀티코어 CPU, 분산 데이터센터 노드 |

#### 한줄 요약

- 하나의 명령을 여러 데이터에 적용하면 SIMD, 여러 독립 명령이 서로 다른 데이터를 처리하면 MIMD로 분류한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **SIMT(Single Instruction, Multiple Threads)**: GPU에서 다수 스레드에 공통 명령을 내리되 스레드별 활성화 마스크와 레지스터를 분리 구동하는 실행 모델.
- **혼합 병렬성(Hybrid Parallelism)**: 단일 시스템 내에서 SIMD(벡터/GPU 코어)와 MIMD(멀티코어/분산 노드)가 복합 계층으로 공존하는 구조.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 분석 레이어(코어 vs 칩 vs 노드) 미지정으로 인한 분류 혼선 | **분석 경계** 사전 명시 및 계층별 수용 범위 고정 | **분류 일관성** 및 객관적 아키텍처 평가 확보 |
| GPU **SIMT** 모델을 하드웨어 SIMD와 단순 동일시 오인 | SW 스레드 제어(SIMT)와 HW 연산 레인(SIMD)의 분리 명시 | 하드웨어 아키텍처의 명확한 분류 식별 |
| 최신 이기종 AI 시스템의 단순 단일 클래스 분류 불가 | 시스템 계층에 따른 **혼합 병렬성** 하이브리드 표기 적용 | 복합 분산 아키텍처의 다중 계층 특성 수용 |

> 사례: 멀티코어 CPU(MIMD 관점) 내부의 AVX-512 레인(SIMD 관점) 계층적 분류

#### 한줄 요약

- GPU 워프는 SIMD형 공통 명령 발행과 SIMT 스레드 상태를 함께 구분하고, 여러 GPU·노드는 독립 명령 흐름을 가진 MIMD 관점으로 분류한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **플린 유형 판정 기준(Flynn's Classification Criteria)**: 시스템 분석 레이어, 독립 명령 제어 유닛 수 및 데이터 파이프라인 수에 근거한 분류 평가 지표.

</details>

- 명령·데이터 스트림의 단일·다중 조합으로 **SISD·SIMD·MISD·MIMD** 판정

#### 한줄 요약

- 분석 경계를 고정하고 명령·데이터 스트림 수의 조합으로 유형을 판정한다.
