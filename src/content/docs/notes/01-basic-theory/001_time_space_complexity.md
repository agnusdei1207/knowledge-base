---
sidebar:
  order: 1
  label: "001. 알고리즘 시간복잡도•공간복잡도 (Time/Space Complexity)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "알고리즘 시간복잡도•공간복잡도 (Time/Space Complexity)"
date: "2026-08-08T01:58:00+09:00"
tags:
  - "notes-basic-theory"
weight: 1
extra:
  question_no: "001"
  source_status: "기출"
  source_history: "131회"
  priority: 50
  priority_note: "131회 기출, 시간•공간 절충의 공통 근거"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **알고리즘 복잡도(Algorithmic Complexity)**: 입력 크기(Input Size)에 따른 연산량 및 추가 메모리의 증가율을 하드웨어 의존성 없이 수학적으로 추상화하여 분석하는 상위 개념 (시간/공간 복잡도로 구분)
- **점근 분석(Asymptotic Analysis)**: 상수와 하위항을 배제하고 대규모 입력이 주어졌을 때 지배항(Dominant Term) 중심으로 자원 소모의 점근적 상·하한을 평가하는 방법
- **자원 한도(Resource Limit)**: 시스템 아키텍처 및 서비스 수준 협약(SLA)에서 허용하는 최대 요청 처리 시간 및 가용 메모리 임계치

</details>

- 정의/개념: 입력 데이터 규모(Input Size)가 증가함에 따라 요구되는 연산 횟수와 추가 메모리의 점근적 증가율을 수학적으로 추상화한 성능 평가 지표인 **알고리즘 복잡도(Algorithmic Complexity)**
- 배경/필요성: 소규모 테스트 환경의 실측값만으로는 실운영 환경의 대규모 데이터 유입 시 발생할 수 있는 자원 고갈(OOM) 및 타임아웃을 예측하기 어려워, 하드웨어 독립적인 분석 체계가 필수적임

#### 한줄 요약

- 입력 데이터 규모(N) 증가에 따른 연산 횟수(Operation Count) 및 메모리 점유(Memory Footprint)의 점근적 증가율 분석

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **지배항(Dominant Term)**: 입력이 커질수록 전체 증가율을 결정하는 가장 빠르게 증가하는 항
- **빅오(Big-O)**: 입력 증가에 따른 비용의 점근적 상한(Asymptotic Upper Bound) 표기
- **빅세타(Big-Theta)**: 입력 증가에 따른 비용의 정확한 점근 차수(Asymptotic Tight Bound) 표기
- **빅오메가(Big-Omega)**: 입력 증가에 따른 비용의 점근적 하한(Asymptotic Lower Bound) 표기
- **시간•공간 상충(Time-Space Tradeoff)**: 중간 결과를 저장해 재계산 시간을 줄이는 대신 추가 메모리를 사용하는 관계
- **최선 사례(Best Case)**: 동일 입력 크기에서 자원 소모가 가장 적은 입력 사례
- **평균 사례(Average Case)**: 입력 분포 확률을 반영한 기대 자원 소모(Expected Cost) 사례
- **최악 사례(Worst Case)**: 동일 입력 크기에서 자원 소모가 가장 큰 입력 사례

</details>

![대표 시간복잡도의 입력 크기별 증가율](/study/diagrams/complexity-growth-rates.svg)

> 입력 크기가 커질수록 붉은 O(n²)와 초록 O(n log n)이 파란 O(log n)•O(n)보다 빠르게 벌어지며, 기본 연산(Basic Operation)량을 정규화한 이론적 증가율임

- 하드웨어 성능과 무관한 **점근 증가율(Asymptotic Growth Rate) 및 Big-O 표기**를 통해 최악의 시나리오에서도 자원 한도를 초과하지 않음을 입증
- 정확 차수와 하한을 명확히 구분하는 **Theta 및 Omega 표기**를 활용하여 알고리즘의 평균 및 최선의 성능 특성을 세밀하게 분석
- 재계산과 중간 결과 저장 간의 **시간•공간 상충(Time-Space Tradeoff)** 관계를 고려하여, 메모리 여유분에 따라 처리 속도를 최적화하는 전략 적용
- **최선•평균•최악(Best/Average/Worst)** 입력 사례별 자원 소모 비용 범위를 분리하여, 운영 환경의 데이터 분포에 적합한 기법 선택

#### 한줄 요약

- 하드웨어 의존성을 배제하고, 입력 규모 변화에 따른 시간·공간 자원의 점근적 상·하한 증가율을 추상화하여 비교·평가

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **계산 모델(Computational Model)**: 기본 연산 비용을 균일하다고 가정하여 하드웨어 차이를 배제하는 분석 모델
- **기본 연산(Basic Operation)**: 비교·대입 등 실행 횟수로 전체 시간 비용을 대변하는 핵심 연산
- **보조 공간(Auxiliary Space)**: 입력 데이터 자체를 제외하고 알고리즘 수행 시 추가로 요구되는 메모리
- **점근 차수(Asymptotic Order)**: 상수와 하위항을 배제하고 지배항의 증가율을 기준으로 분류한 비용 등급

</details>

```text
복잡도 분석 구조
├─ 계산 모델 (Computational Model)
├─ 시간 분석기 (Time Analyzer)
├─ 공간 분석기 (Space Analyzer)
└─ 점근 차수 판정기 (Asymptotic Order Evaluator)
```

가지의 의미: 동일 계산 모델을 공유하는 정적 분석(Static Analysis) 구성 요소 집합

| 구성요소 | 책임 |
|:---|:---|
| 계산 모델 | **기본 연산(Basic Operation)**의 단위 비용 규정 |
| 시간 분석기 | 입력 크기별 **기본 연산** 수행 횟수 산정 |
| 공간 분석기 | 입력 크기별 최대 **보조 공간(Auxiliary Space)** 산정 |
| 점근 차수 판정기 | **지배항·상하한** 기준 점근적 증가율 분류 |

#### 한줄 요약

- 계산 모델 기반으로 단위 연산을 정의하고, 분석기를 통해 산정된 연산 횟수와 보조 공간을 점근 차수로 분류 및 평가

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **비용 함수(Cost Function)**: 입력 크기에 따른 시간 또는 공간 사용량의 증가 추세를 나타내는 함수
- **상한•하한(Upper/Lower Bound)**: 입력이 극단적으로 커질 때 비용 함수가 넘지 않는 위쪽 경계 및 반드시 도달하는 아래쪽 경계

</details>

- 시간 및 공간 비용 함수(Cost Function)의 **점근 차수(Asymptotic Order)**를 각각 산출

#### 한줄 요약

- 시간 및 공간 비용 함수의 연산 횟수와 보조 공간 증가율을 동일한 점근 표기법(Asymptotic Notation)으로 일관되게 평가

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **시간복잡도(Time Complexity)**: 입력 크기(N) 증가에 따른 기본 연산 횟수의 점근적 증가 정도
- **공간복잡도(Space Complexity)**: 입력 크기(N) 증가에 따른 최대 메모리 사용량의 점근적 증가 정도
- **추가 공간(Extra Space)**: 호출 스택(Call Stack), 캐시(Cache), 중간 결과 저장 등에 사용되는 메모리
- **점유 공간(Occupied Space)**: 프로그램 실행 중 알고리즘이 실질적으로 차지하는 전체 메모리 영역
- **할당기 비용(Allocator Overhead)**: 메모리 동적 할당·해제 및 배치 과정에서 발생하는 공간적 오버헤드
- **런타임 비용(Runtime Overhead)**: 프로그램 실행 환경(VM, GC 등)이 자체적으로 요구하는 추가 공간 비용
- **상수 계수(Constant Factor)**: 입력 크기와 무관하게 동일 점근 차수 내에서 비용의 절대 크기를 결정짓는 계수

</details>

| 복잡도 | 시간복잡도 (Time Complexity) | 공간복잡도 (Space Complexity) |
|:---|:---|:---|
| 적용 기준 | **응답시간(Response Time)** 확보가 서비스의 핵심일 때 | **메모리 예산(Memory Budget)** 준수가 시스템의 핵심일 때 |
| 핵심 특징 | **기본 연산(Basic Operation)** 횟수의 점근적 증가율 | 최대 **점유 공간(Occupied Space)**의 점근적 증가율 |
| 한계 | 동일 차수 내 **상수 계수(Constant Factor)** 격차 미반영 | 할당기 및 런타임 환경의 **추가 공간(Overhead)** 누락 가능성 |

> 요약: 중간 결과 저장을 통한 재계산 생략 등 **시간•공간 상충(Time-Space Tradeoff)** 관계 형성

#### 한줄 요약

- 중간 결과의 메모이제이션(Memoization)은 재연산 시간(Time)을 단축하나 보조 공간(Space) 점유율을 증가시키는 상충(Tradeoff) 관계 유발

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **대표 기본 연산(Representative Basic Operation)**: 전체 실행 시간 증가 추세를 대변하는 핵심 연산(예: 루프 내 비교·대입)
- **벤치마크(Benchmark)**: 동일 입력 및 실행 환경에서 다수 알고리즘 후보의 실제 시간·공간 비용을 측정 및 비교하는 성능 평가

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 비대표 **기본 연산** 산정으로 인한 병목 지점 불일치 | 지배 반복문(Dominant Loop) 내 단일 기본 연산 기준으로 **비용 함수** 도출 | 입력 증가에 따른 **시간복잡도** 예측의 정확성 확보 |
| 평균 입력 분석에 의존하여 **최악 사례(Worst Case)** 자원 초과 위험 은폐 | 실제 입력 분포별 **평균•최악 사례** 산정 및 최대 허용 **자원 한도** 교차 검증 | 극단적 부하 상황에서의 **자원 한도 초과(OOM, Timeout)** 선제적 예방 |
| 재귀 스택 및 캐시 누락으로 인한 **보조 공간(Auxiliary Space)** 과소평가 | 최대 호출 깊이(Call Depth) 및 중간 저장소 크기를 전체 공간 비용에 합산 | 런타임 **공간복잡도(Space Complexity)** 예측 정확도 극대화 |
| 동일 점근 차수 내 **상수 계수(Constant Factor)** 차이로 인한 응답시간 역전 현상 | 실제 운영 대상 입력 구간 및 동일 환경에서의 실증적 **벤치마크(Benchmark)** 병행 | 운영 환경에 가장 적합한 실질적 최적 알고리즘(Optimal Candidate) 식별 |

#### 한줄 요약

- 최악 사례(Worst Case) 입력에 대한 연산 횟수 산정 및 재귀 호출 스택(Call Stack)을 포함한 보조 공간의 정밀한 측정이 필수적임

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **응답시간 한도(Response Time Limit)**: 시스템이 요청을 처리하고 결과를 반환해야 하는 최대 허용 지연 시간
- **메모리 한도(Memory Limit)**: 알고리즘 실행 과정에서 동적으로 할당받아 사용할 수 있는 최대 메모리 임계치

</details>

- **응답시간(Response Time) 및 메모리(Memory) 한도** 중 선행 초과가 예상되는 임계 자원(Critical Resource)을 기준으로 알고리즘 최적 대안 채택

#### 한줄 요약

- 임계 자원(Critical Resource: 응답시간/메모리 한도)의 병목(Bottleneck) 여부를 최우선으로 판단하여, 실무 환경에 최적화된 시간·공간 복잡도(Time/Space Complexity) 기반 알고리즘 선정 필수
