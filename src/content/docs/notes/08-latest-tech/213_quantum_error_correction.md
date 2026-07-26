---
sidebar:
  order: 213
  label: "213. Quantum Error Correction 양자 오류 정정 (Quantum Error Correction)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "Quantum Error Correction 양자 오류 정정 (Quantum Error Correction)"
date: "2026-07-25T03:42:00+09:00"
tags:
  - "notes-latest-tech"
weight: 213
extra:
  question_no: "213"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "양자 오류 정정의 신드롬·복구가 138회 출제됨"
---

## 미리 알고가기

- **양자 오류 정정**: 물리 큐비트로 논리 큐비트를 보호하는 기술
- **코드 거리 ($d$)**: 오류 보정 능력을 결정하는 지표이며 $t = \lfloor (d-1)/2 \rfloor$ 임
- **신드롬 측정**: 정보를 유지한 채 오류 정보만 간접 측정함



## Ⅰ. 개요

- **정의/개념**: 논리 정보를 다수 물리 큐비트로 보호하는 기술
- **배경/필요성**: 복제 없이 물리 오류 누적을 억제해 계산 유지

### 쉽게 이해하기 (학습용)

- 원문을 직접 보지 않고 오류의 흔적만 찾아 고치는 보호 기술임

## Ⅱ. 특징

- 비국소 인코딩이 복제 없이 정보를 보호한다.
- 신드롬 측정이 논리 상태 노출 없이 오류를 찾는다.
- 임계값 아래에서 코드 거리가 오류를 억제한다.
- 보호·논리 연산이 많은 물리 자원을 요구한다.

### 쉽게 이해하기 (학습용)

- 상태 보존을 위한 검사와 추정을 짧은 주기로 계속 반복하는 구조임

## Ⅲ. 아키텍처 및 구성요소

| 설계 요소 | 설명 |
|:---|:---|
| 물리 큐비트 | 데이터 유지 큐비트와 측정용 검사 큐비트 |
| 코드 설계 | 서피스 코드 등 논리 정보 배치 기법 |
| 신드롬 회로 | 오류 정보 추출을 위한 주기적인 상태 검사 |
| 해독 엔진 | 수집된 증상 기반 오류 경로 추정 및 적용 |
| 연산 레이어 | 보호된 상태에서 논리적 연산 수행 수행함 |

> 요약: 정보 인코딩 후 반복 검사·추정으로 오류 정정

### 쉽게 이해하기 (학습용)

- 정보를 분산하고 장부 기록을 갱신하며 연산을 지속하는 구조임

## Ⅳ. 원리 및 절차 흐름도


```text
노이즈분석
  ↓
코드선택
  ↓
상태인코딩
  ↓
주기검사
  ↓
오류보정
```

| 절차 | 설명 |
|:---|:---|
| 노이즈분석 | 장비 오류 특성에 맞는 목표치 설정함 |
| 코드선택 | 작업 환경에 적합한 보호 코드 적용함 |
| 상태인코딩 | 물리 큐비트에 논리 정보를 매핑함 |
| 주기검사 | 오류 증상을 주기적으로 수집함 |
| 오류보정 | 추정된 오류를 바탕으로 보정함 |

> 요약: 상태 인코딩 후 검사·보정을 반복

### 쉽게 이해하기 (학습용)

- 고장 습관을 분석하여 보호 구조를 정하고 계속 검사하며 보정함

## Ⅴ. 종류 및 비교

| 판단 기준 | 오류 정정(QEC) | 오류 완화(Mitigation) | 오류 억제(Suppression) |
|:---|:---|:---|:---|
| 핵심 특징 | 인코딩 후 반복적인 오류 정정 | 결과 통계 처리로 오차 편향 감소 | 하드웨어 개선으로 오류 발생 자체 감소 |
| 적용 기준 | 논리적 중복으로 신뢰성 지속 확보 | 장기 수행 시 신뢰성 보장 어려움 | 근본적 오류 해결 불가 |
| 주요 위험 | 대규모 큐비트 자원 필요 | 고전 컴퓨팅 자원 활용 | 제어 기술 및 보정 위주 |

> 요약: 오류 억제·완화·정정의 개입 시점 구분

### 쉽게 이해하기 (학습용)

- 정비와 통계적 보정, 구조적 정정은 목적과 비용이 확연히 다름

## Ⅵ. 실무 사례

1. 대상 환경의 도입 조건과 설계를 검증함
2. 운영 위험과 성과 지표를 검증함

### 쉽게 이해하기 (학습용)

- Google Quantum AI의 surface-code experiment는 physical qubit lattice를 distance 3·5·7로 키우며 repeated parity check와 decoder를 적용해 below-threshold에서 code size 증가에 따른 logical error suppression을 보였지만 useful algorithm까지의 logical gate·error·resource 격차는 별도로 남음
- fault-tolerant architecture 팀은 chemistry phase-estimation의 target failure probability에서 logical T-state 수와 cycle을 역산해 code distance·logical qubit·magic-state factory·decoder throughput을 산정하고 correlated burst·leakage를 포함한 sensitivity analysis로 hardware roadmap을 정함

## Ⅶ. 결론

- 물리 오류율·자원 예산으로 코드 거리와 QEC 선택

### 쉽게 이해하기 (학습용)

- 보호망을 키우는 것뿐 아니라 해독 속도와 정확도도 중요함
