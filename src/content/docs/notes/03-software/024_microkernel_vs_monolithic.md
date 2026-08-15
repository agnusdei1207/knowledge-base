---
sidebar:
  order: 24
  label: "024. 마이크로커널 vs 모놀리식 커널 (Microkernel vs Monolithic)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "마이크로커널 vs 모놀리식 커널 (Microkernel vs Monolithic)"
date: "2026-08-13T13:54:00+09:00"
tags:
  - "notes-software"
weight: 24
extra:
  question_no: "024"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "138회 기출, 커널 구조•격리 절충"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Monolithic Kernel (모놀리식 커널)**: OS의 주요 기능(프로세스, 메모리, 파일 시스템, 네트워크, 디바이스 드라이버)을 단일 대형 커널 주소 공간(Ring 0)에 통째로 묶어 고속 구동시키는 커널 구조.
- **Microkernel (마이크로커널)**: 커널 공간(Ring 0)에는 최소한의 핵심 기능(IPC, 메모리 관리, 기본 스케줄링)만 남기고, 파일 시스템, 디바이스 드라이버 등은 유저 공간(Ring 3 User Server)으로 분리 격리시킨 커널 구조.
- **Hybrid Kernel (하이브리드 커널)**: 모놀리식의 고성능 속성과 마이크로커널의 모듈형 보안 격리성을 혼합한 구조 (Windows, macOS XNU 커널).

</details>

- 정의/개념: OS 커널 공간(Ring 0)의 기능 집적도 및 보안 격리 범위에 따른 OS 핵심 엔진 2대 설계 철학인 **Monolithic Kernel vs Microkernel**
- 배경/필요성: 커널 내 서비스 결함은 전체 시스템의 **장애 범위 확대** 가능

#### 한줄 요약

- 마이크로커널과 모놀리식 커널은 운영체제 서비스의 배치 경계가 다르다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **IPC Overhead**: 마이크로커널 환경에서 유저 서버 간 통신 시 커널을 경유하는 문맥 전환(Context Switch)이 빈번히 발생하여 발생하는 처리 지연.
- **Fault Isolation**: 드라이버나 파일 시스템 모듈이 유저 공간 서버 프로세스로 구동되어 해당 모듈이 붕괴되어도 OS 커널이 마비되지 않고 개별 재부팅(Restart) 가능한 속성.

</details>

- 단일 주소 공간의 직접 호출 경로를 쓰는 **Monolithic Kernel**
- **User Space Server** 분리로 서비스 결함 범위를 줄이는 Microkernel
- **IPC Overhead** 및 문맥 전환 수치 대 시스템 결함 격리성의 트레이드오프

#### 한줄 요약

- 결함 격리와 직접 호출 성능의 절충이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **User-Space Server**: 마이크로커널 구조에서 파일 시스템(VFS), 네트워크 스택, 디바이스 드라이버가 유저 모드 프로세스 형태(Server)로 독립 구동되는 모듈.

</details>

```text
+---------------- 마이크로커널 구조 ----------------+
|                                                   |
|  [마이크로커널] -------- [사용자 공간 서버]       |
|                                                   |
+---------------------------------------------------+

+---------------- 모놀리식 구조 --------------------+
|                                                   |
|                 [모놀리식 커널]                   |
|                                                   |
+---------------------------------------------------+
```

선의 의미: 마이크로커널은 IPC 통신 채널로 유저 공간 서버와 커널을 결합하는 반면, 모놀리식 커널은 하나의 거대한 통주소 공간으로 구성됨을 의미.

| 구성요소 | 책임 |
|:---|:---|
| 마이크로커널 | IPC•스케줄링•주소 공간 등 최소 기능 제공 |
| 사용자 공간 서버 | 파일•장치 서비스를 독립 프로세스로 실행 |
| 모놀리식 커널 | 주요 운영체제 서비스를 단일 커널 공간에 배치 |

#### 한줄 요약

- IPC와 스케줄링이 분리된 서비스를 연결한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Context Switch Penalty**: 마이크로커널에서 I/O 연산 처리 시 `User App -> Microkernel -> User Server -> Microkernel -> User App` 4단계 전환 지연 파급.

</details>

```text
마이크로커널 호출 경로

[시스템 호출] ──► [1. IPC 서비스 요청•응답] ──► [결과 반환]

모놀리식 커널 호출 경로

[시스템 호출] ──► [2. 커널 내부 직접 호출] ──► [결과 반환]
```

### 동작 원리

1. **IPC 서비스 요청·응답**: 커널이 사용자 서버로 메시지를 전달하고 응답 중계
2. **커널 내부 직접 호출**: 커널 주소 공간의 서비스 함수를 호출

#### 한줄 요약

- 마이크로커널은 IPC 서비스 요청, 모놀리식은 커널 내부 직접 호출이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **seL4**: 특정 구성과 가정에서 구현의 정형 명세 준수를 기계 검증한 마이크로커널.

</details>

| 비교 항목 | Monolithic (Linux) | Microkernel (QNX / seL4) |
|:---|:---|:---|
| 검증 범위 | 큰 신뢰 컴퓨팅 기반으로 검증 부담 증가 | 작은 **TCB**로 정형 검증 범위 축소 가능 |
| 모듈 핫 리로딩 | LKM(Loadable Kernel Module) 수용 | **User Server 프로세스 Kill & Restart** |
| 보안 검증성 | 모듈별 검사와 런타임 보호 중심 | 핵심 커널의 **정형 검증** 가능성 확대 |
| 주요 활용 분야 | 범용 서버, PC, 스마트폰(Android) | 자동차 ECU(AUTOSAR), 의료기기, 우주항공 |

#### 한줄 요약

- 서비스 재시작은 마이크로커널, 낮은 주소 공간 전환 비용은 모놀리식 커널의 강점이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Zero-Copy IPC**: 마이크로커널의 잦은 IPC 오버헤드를 막기 위해, 커널과 유저 서버 간 메모리 버퍼를 공유(Shared Memory)하여 복사 횟수를 0으로 줄이는 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Microkernel의 IPC 전환과 복사 비용 | **공유 메모리 IPC**와 요청 묶음 적용 | IPC 전환•복사 횟수 감소 |
| Monolithic Kernel의 3rd Party 드라이버 버그로 전체 OS Panic | **LKM (Loadable Kernel Module)** 검증 및 eBPF 적용 | 커널 크래시 위험 억제 |
| 자동차/전장 장비의 하드 실시간 및 최고 수준 안정성 요구 | **QNX / seL4 (Microkernel)** 기반 RTOS 도입 | **Fault Isolation** 및 안전성 확보 |

> 사례: 자동차 커넥티드 카 표준 **QNX RTOS** 및 스마트폰 OS **Google Fuchsia (Zircon Kernel)** 적용

#### 한줄 요약

- 요청 묶음, 감독, TCB 최소화 기반 운영이 핵심이다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **커널 아키텍처 선택 기준(Kernel Architecture Selection Criteria)**: 시스템 성능 타깃, 하드 실시간 제약, 무결성/보안성 수치에 기반한 설계 체계.

</details>

- **커널 아키텍처 선택 기준**에 따라 초고속 대용량 범용 시스템은 **Monolithic / Hybrid**, 미션 크리티컬 인프라는 **Microkernel** 채택

#### 한줄 요약

- 서비스 단위 복구와 호출 지연을 함께 평가하는 것이 핵심이다.
