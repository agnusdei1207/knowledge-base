---
sidebar:
  order: 128
  label: "128. ARM TrustZone (ARM TrustZone)"
  badge:
    text: "기출 · 70%"
    variant: note
title: ARM TrustZone (ARM TrustZone)
date: "2026-07-27T23:59:59+09:00"
tags:
  - notes-security
weight: 128
extra:
  question_no: "128"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "138회 기출이며 TEE·격리 비교에 활용되는 하드웨어임"
---

## 미리 알고가기

- **Arm TrustZone**: 암 트러스트존으로 읽는 Arm 기술명이며, SoC 자원을 보안·비보안 상태로 분리
- **SoC (System on Chip)**: 처리·메모리·장치를 한 칩에 통합함
- **Secure World**: 보안 서비스 실행 영역임
- **Normal World**: 일반 운영체제·응용 실행 영역임
- **TEE (Trusted Execution Environment)**: 격리 보안 실행 환경임
- **REE (Rich Execution Environment)**: 범용 실행 환경임
- **SMC (Secure Monitor Call)**: 보안 상태 전환 요청임
- **TA (Trusted Application)**: TEE 보안 서비스 단위임
- **DMA (Direct Memory Access)**: CPU를 거치지 않고 장치가 메모리를 직접 읽고 쓰는 기능
- **SAU (Security Attribution Unit)**: Arm M-profile에서 메모리 영역의 보안 속성을 설정하는 장치
- **TOCTOU (Time of Check to Time of Use)**: 검증한 시점과 사용 시점 사이에 공유 데이터가 바뀌어 생기는 취약점
- **TCB (Trusted Computing Base)**: 시스템 보안을 위해 반드시 신뢰해야 하는 최소 하드웨어·소프트웨어 집합
- **부채널**: 캐시·시간·전력 등 공유 자원의 실행 흔적으로 비밀이 새는 경로



## Ⅰ. 개요

- 정의: SoC 자원의 **보안·비보안 상태 격리**
- 기존 한계: 범용 실행환경 침해의 **비밀 자원 노출**

### 쉽게 이해하기 (학습용)

- 같은 칩 안에 일반 업무 공간과 보호 공간을 만들고 하드웨어가 접근 가능 자원을 구분함

## Ⅱ. 특징

- CPU·메모리·버스의 **보안 상태 전파**
- Secure·Normal World의 **하드웨어 격리**
- SMC·Monitor 기반 **보안 상태 전환**

### 쉽게 이해하기 (학습용)

- 벽은 하드웨어가 만들지만 보호 공간의 프로그램과 출입구가 안전한지는 소프트웨어가 책임져야 함

## Ⅲ. 아키텍처 및 구성요소

```text
[Normal] <-> [ 경계 ] <-> [Secure]
   |           |           |
[OS/APP]    [SMC/HW]    [TA/TEE]
   +-------------------------------+
   | SoC 자원 보안 속성 격리 기반 |
   +-------------------------------+
```

| 설계 요소 | 설명 |
|:---|:---|
| Secure World | TEE·TA 보안 서비스 실행 |
| Normal World | 범용 OS·응용 실행 |
| Monitor·SMC | 실행 세계 전환 통제 |
| 메모리·버스 통제 | 보안 속성별 접근 분리 |
| 주변장치 통제 | DMA·인터럽트 접근 제한 |

### 쉽게 이해하기 (학습용)

- 일반 앱은 정해진 요청으로 TEE의 제한된 서비스를 사용함

## Ⅳ. 원리 및 절차 흐름도

```text
검증
 ↓
전환
 ↓
실행
 ↓
정제
 ↓
복귀
```

| 절차 | 설명 |
|:---|:---|
| 검증 | 호출·버퍼 범위를 검증함 |
| 전환 | 보안 상태로 전환함 |
| 실행 | TA가 자원을 사용함 |
| 정제 | 반환값을 검증함 |
| 복귀 | 일반 상태로 복귀함 |

### 쉽게 이해하기 (학습용)

- 보호 영역 입구에서 요청과 메모리를 확인하고 필요한 결과만 일반 영역으로 돌려보냄

## Ⅴ. 종류 및 비교

| 실행환경 격리 방식 | A-profile | M-profile | 하이퍼바이저 |
|:---|:---|:---|:---|
| 적용 기준 | 범용 OS에서 키·인증 서비스를 격리할 때 | 소형 장치의 펌웨어·메모리를 분리할 때 | 여러 OS와 자원 할당을 격리할 때 |
| 핵심 특징 | 두 실행 세계 분리 | MCU 보안 영역 분리 | 다중 OS·가상머신 분리 |
| 한계 | SMC·공유 메모리 검증 오류 | SAU·주변장치 속성 누락 | 취약점의 전 게스트 영향 |

> 요약: SoC 전반의 보안 상태 및 격리 구조 필요

### 쉽게 이해하기 (학습용)

- A-profile은 범용 OS, M-profile은 소형 장치의 보안 영역을 나눔

## Ⅵ. 실무 사례

1. TEE 호출의 **공유 메모리·TOCTOU 검증**

### 쉽게 이해하기 (학습용)

- Normal World가 전달한 공유 메모리의 주소·길이·권한을 Secure World에서 복사·재검증해 검사 후 변경되는 TOCTOU 공격을 막는다.

## Ⅶ. 결론

- 일반 실행환경 침해로부터 핵심 비밀을 보호하기 위해 Secure World 경계·공유 메모리·DMA·TCB·부채널을 검토하여, 최소 신뢰 서비스만 ARM TrustZone에 격리해야 한다.

### 쉽게 이해하기 (학습용)

- 격리 효과는 Secure World라는 이름보다 경계 검증과 최소 신뢰 코드 운영 품질에 달려 있음
