---
sidebar:
  order: 206
  label: "206. AUTOSAR Adaptive (AUTOSAR Adaptive)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "AUTOSAR Adaptive (AUTOSAR Adaptive)"
date: "2026-07-25T03:35:00+09:00"
tags:
  - "notes-latest-tech"
weight: 206
extra:
  question_no: "206"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "AUTOSAR Adaptive 서비스 구조가 최근 출제됨"
---

## 미리 알고가기

- **AUTOSAR Adaptive (AUTOSAR Adaptive) Platform**: 서비스 지향 고성능 차량 SW 플랫폼
- **Classic AUTOSAR (Classic AUTOSAR) Control**: 실시간 MCU 제어용 SW 표준 플랫폼
- **POSIX (Portable Operating System Interface) Runtime**: Adaptive 구동 기반 OS 환경
- **ARA (AUTOSAR Runtime for Adaptive) Service**: Adaptive 플랫폼의 통신·실행·관리 API
- **SDV (Software Defined Vehicle) Architecture**: SW 중심 차량 아키텍처 환경
- **Mixed-criticality (Mixed-criticality) Separation**: 중요도 기반 SW 격리 설계



## Ⅰ. 개요

- **정의/개념**: 고성능 ECU용 서비스 지향 차량 SW 플랫폼
- **배경/필요성**: 자율주행·센서 융합의 연산·변경 요구를 수용

### 쉽게 이해하기 (학습용)

- 차량용 고성능 컴퓨터에서 앱이 공통 통신·저장·보안 서비스를 사용하게 하는 표준 설계도임

## Ⅱ. 특징

- Adaptive 앱이 POSIX 프로세스로 독립 실행된다.
- ARA가 통신·상태·암호 서비스 API를 제공한다.
- 동적 발견·바인딩이 서비스 변경을 유연화한다.
- Classic 연계가 고성능·실시간 제어를 분리한다.

### 쉽게 이해하기 (학습용)

- 앱은 실행 설명서에 따라 차량 컴퓨터에서 구동하고 필요한 서비스를 찾아 쓰며, 새 앱은 업데이트 관리자로 설치함

## Ⅲ. 아키텍처 및 구성요소

```text
[Adaptive Applications]
      ↓ ara::com
[Management Services]
      ↓ POSIX API
[POSIX OS Partition]
      ↓
[Classic Control]
```

| 설계 요소 | 설명 |
|:---|:---|
| POSIX OS·machine·partition | 앱의 격리 실행 환경을 제공함 |
| Adaptive Application·manifest | 앱 요구·배포·실행 정보를 선언함 |
| ara::com·service interface | 서비스를 발견하고 통신함 |
| platform management services | 실행·상태·업데이트를 관리함 |
| Classic·safety/security boundary | 강실시간 제어와 안전하게 연계함 |

> 요약: 서비스 플랫폼이 앱 수명주기와 통신을 관리

### 쉽게 이해하기 (학습용)

- 앱은 실행 명세에 따라 동작하고 운영체제가 자원을 격리하며 제동 제어기는 별도 권한을 거쳐 보호됨

## Ⅳ. 원리 및 절차 흐름도

```text
[기능 안전 설계]
       ↓
[Manifest 명세화]
       ↓
[UCM 패키지 설치]
       ↓
[프로세스 실행]
       ↓
[상태 관리·복구]
```

| 절차 | 설명 |
|:---|:---|
| 기능·안전 분할 | 기능·안전 분할을 수행하고 결과를 검증함 |
| service·manifest 설계 | service·manifest 설계을 수행하고 결과를 검증함 |
| package 설치 | package 설치을 수행하고 결과를 검증함 |
| 실행·발견 | 실행·발견을 수행하고 결과를 검증함 |
| 상태·갱신 관리 | 상태·갱신 관리을 수행하고 결과를 검증함 |

> 요약: manifest로 설치·실행·상태를 관리

### 쉽게 이해하기 (학습용)

- 역할 분담 후 명세 기반 패키지를 설치하여 안전하게 앱을 운영함

## Ⅴ. 종류 및 비교

| 판단 기준 | AUTOSAR Classic | AUTOSAR Adaptive | 혼합 E/E 역할 분담 |
|:---|:---|:---|:---|
| 핵심 특징 | 정적 구성·강실시간 MCU 제어 | POSIX 기반 동적 서비스·HPC 처리 | Classic·Adaptive 역할 분담 |
| 적용 기준 | chassis·powertrain 안전 제어 | 인지·융합·데이터·서비스 | gateway·E2E로 두 플랫폼 연계 |
| 주요 위험 | 동적 변경·고성능 처리 제약 | 자원·상태·업데이트 복잡성 | 경계 통신·안전 책임 불명확 |

> 요약: Adaptive와 Classic의 역할·안전 경계 구분

### 쉽게 이해하기 (학습용)

- Adaptive가 데이터를 처리하고 Classic이 실시간 제어를 수행함

## Ⅵ. 실무 사례

1. 대상 환경의 도입 조건과 설계를 검증함
2. 운영 위험과 성과 지표를 검증함

### 쉽게 이해하기 (학습용)

- 중앙 ADAS ECU는 Adaptive Application으로 카메라·레이더 융합과 주행 목표를 계산하고 Classic 제동 ECU는 hard real-time 제어를 수행하며 E2E 보호 service로 목표값을 전달함
- cockpit HPC는 진단·차량 데이터 service의 provider를 ara::com으로 발견하고 새 application package를 UCM으로 설치하되 service instance ID·manifest와 safety partition 회귀 검증 후 활성화함

## Ⅶ. 결론

- 동적 서비스는 Adaptive, 강실시간 제어는 Classic

### 쉽게 이해하기 (학습용)

- 고성능 앱의 유연함은 제어기와의 분리와 안전한 연결을 전제로 함
