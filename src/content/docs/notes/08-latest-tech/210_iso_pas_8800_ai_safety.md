---
sidebar:
  order: 210
  label: "210. ISO/PAS 8800 AI Safety (ISO/PAS 8800)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "ISO/PAS 8800 AI Safety (ISO/PAS 8800)"
date: "2026-07-25T03:39:00+09:00"
tags:
  - "notes-latest-tech"
weight: 210
extra:
  question_no: "210"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "ISO PAS 8800 AI 안전 수명주기가 최근 출제됨"
---

## 미리 알고가기

- **ISO/PAS 8800 (AI Safety in Road Vehicles)**: 자동차 AI의 안전 개발 및 통제 사양
- **ISO 26262 (Functional Safety)**: 전기·전자 시스템의 고장 방지 기능 안전 표준
- **ISO 21448 (SOTIF)**: 의도된 기능의 한계로 인한 위험 안전성 표준
- **AI Element (AI Element)**: 차량 제어에 활용되는 학습 모델·시스템 단위
- **Insufficiency (Insufficient Performance)**: 입력 대비 안전 요구를 못 맞추는 출력 상황
- **Assurance Argument (Evidence-based)**: 안전성 입증을 위한 증거 기반 논리 구조



## Ⅰ. 개요

- **정의/개념**: 차량 AI 안전 위험을 수명주기 증거로 통제
- **배경/필요성**: 데이터·모델 불확실성의 안전 영향을 보완

### 쉽게 이해하기 (학습용)

- 규칙 확인이 어려운 차량 AI에 대해 데이터부터 실제 운행까지 안전 증거를 마련하는 생애주기임

## Ⅱ. 특징

- 입·출력 요구와 위험 경로를 함께 분석한다.
- 알려진 약점 통제와 현장 감시를 병행한다.
- 데이터·모델 수명주기를 추적·검증한다.
- 안전 증거가 배포·운영 재평가를 뒷받침한다.

### 쉽게 이해하기 (학습용)

- 알려진 약점은 미리 대응책을 마련하고, 모르는 약점은 실제 운행 감시로 찾아 고치는 방식임

## Ⅲ. 아키텍처 및 구성요소

```text
[AI Safety Assurance Argument]
├─ claim: [Vehicle Safety Goal·AI Requirement]
├─ development: [Dataset·Model Evidence]
├─ verification: [V&V·Insufficiency Evidence]
└─ operation: [Field Monitoring·Change Evidence]
```

| 설계 요소 | 설명 |
|:---|:---|
| AI system definition·context | 기능 경계·운행 맥락을 정의함 |
| AI safety requirement·insufficiency | 안전 요구와 성능 부족을 연결함 |
| dataset engineering | 조건별 데이터 적합성을 입증함 |
| model·architecture development | 모델 설계·학습 변경을 추적함 |
| V&V·assurance argument | 검증 증거로 안전 주장을 구성함 |
| operation·change control | 현장 위험과 변경을 재평가함 |

> 요약: 차량 안전 목표를 AI 요구·증거로 연결

### 쉽게 이해하기 (학습용)

- 안전 약속을 AI 조건으로 나눈 뒤 검증 자료를 붙이고, 출시 후에도 약속을 지키는지 확인함

## Ⅳ. 원리 및 절차 흐름도

```text
[상황 분석]
      ↓
[요구사항 정의]
      ↓
[모델 개발]
      ↓
[안전성 검증]
      ↓
[운행 감시]
```

| 절차 | 설명 |
|:---|:---|
| context·hazard 정의 | context·hazard 정의을 수행하고 결과를 검증함 |
| insufficiency·requirement 도출 | insufficiency·requir을 수행하고 결과를 검증함 |
| data·model 개발 | data·model 개발을 수행하고 결과를 검증함 |
| V&V·assurance | V&V·assurance을 수행하고 결과를 검증함 |
| field monitoring·재승인 | field monitoring·재승인을 수행하고 결과를 검증함 |

> 요약: 출시 전 검증과 현장 위험 재승인을 순환

### 쉽게 이해하기 (학습용)

- 위험 구역을 정하고 검증을 거친 뒤 출시 후 약점 발견 시 되돌리거나 다시 승인함

## Ⅴ. 종류 및 비교

| 판단 기준 | ISO/PAS 8800 | ISO 26262 | ISO 21448 SOTIF |
|:---|:---|:---|:---|
| 핵심 특징 | 차량 AI 요소의 안전 증거 | E/E 고장 기반 기능안전 | 의도 기능의 성능 한계 안전 |
| 적용 기준 | 데이터·모델·현장 변화 통제 | 고장률·진단·안전 메커니즘 | triggering condition·기능 한계 |
| 주요 위험 | 알려지지 않은 AI 부족성 | AI 성능 부족을 단독 포괄 못함 | AI 수명주기 증거가 부족함 |

> 요약: AI 안전 증거를 차량 안전 체계와 연결

### 쉽게 이해하기 (학습용)

- 고장은 기능안전, 기능 한계는 SOTIF, AI 한계는 이 사양으로 관리함

## Ⅵ. 실무 사례

1. 대상 환경의 도입 조건과 설계를 검증함
2. 운영 위험과 성과 지표를 검증함

### 쉽게 이해하기 (학습용)

- 전방 camera 보행자 detector는 역광·가림·희귀 자세를 input subdomain으로 나눠 known miss와 confidence limitation을 검증하고, 불확실하면 sensor fusion·감속 fallback을 작동시키며 field near-miss를 수집해 assurance argument를 재평가함
- driver monitoring model은 안경·피부톤·좌석 위치별 dataset coverage와 false-negative safety requirement를 trace하고, fleet drift나 model update 때 shadow evaluation·rollback·독립 승인 후에만 새 version을 배포함

## Ⅶ. 결론

- AI 한계·안전 증거로 배포와 현장 재평가 결정

### 쉽게 이해하기 (학습용)

- AI 안전은 운행 중에도 증거를 추적하여 위험이 없음을 입증해야 함
