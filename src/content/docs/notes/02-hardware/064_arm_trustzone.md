---
sidebar:
  order: 64
  label: "064. Arm TrustZone 보안 확장"
  badge:
    text: "기출 • 50%"
    variant: note
title: "Arm TrustZone 보안 확장"
date: "2026-08-13T12:00:06+09:00"
tags:
  - "notes-hardware"
weight: 64
extra:
  question_no: "064"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "보안 상태•전환•자원 속성 검증"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Arm TrustZone**: 시스템을 보안(Secure)과 비보안(Non-secure)의 2개 도메인으로 수평 격리하는 하드웨어 기술
- **보안 상태(Secure State)**: 암호 키, TEE 및 보안 자원에 하드웨어 직결 접근이 허용되는 실행 도메인
- **비보안 상태(Non-Secure State)**: 범용 OS 및 일반 애플리케이션이 구동되며 보안 자원 접근이 차단되는 도메인

</details>

- 정의/개념: 하드웨어 기반 2개 실행 도메인(Secure World vs Normal World) 및 버스 트랜잭션 속성을 통해 시스템 전반을 수평 격리하는 **Arm TrustZone**
- 배경/필요성: 리눅스/안드로이드 등 범용 OS 커널 탈취(Kernel Compromise) 시에도 암호 키, DRM, 생체 정보 등 핵심 보안 자산의 하드웨어 보호 요구성

#### 한줄 요약

- TrustZone은 일반 OS가 실행되는 비보안 상태와 민감 서비스를 실행하는 보안 상태를 분리하고, 버스·자원 속성으로 접근 경계를 강제한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **NS 비트(Non-Secure Bit)**: 버스 트랜잭션 신호선에 탑재되어 요청 발원지를 파악하는 하드웨어 제어 신호
- **공유 버퍼(Shared Buffer)**: 비보안 영역과 보안 영역 간 데이터를 교환하기 위해 지정된 비보안 영역 메모리

</details>

- 프로세서 상태에 따른 **Normal World**와 **Secure World**의 시스템 차원 수평 격리
- AMBA 버스 상의 **NS 비트**를 통한 메모리 및 주변장치 하드웨어 물리 접근 통제
- **공유 버퍼** 검증 및 안전한 모니터(Secure Monitor) 진입점을 통한 도메인 상호 전환

#### 한줄 요약

- 프로파일별 상태 전환 경로와 트랜잭션·자원 보안 속성 검사가 보안 메모리·장치의 접근 경계를 강제한다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **SMC(Secure Monitor Call)**: A-profile 상에서 Non-secure 구역에서 Secure World로 전환하기 위해 발생시키는 예외 인스트럭션.
- **TEE(Trusted Execution Environment)**: TrustZone Secure World 상에서 구동되는 경량 보안 OS(OP-TEE, QSEE 등).
- **TCB(Trusted Computing Base)**: 시스템의 보안성을 유지하기 위해 무조건 신뢰해야 하는 하드웨어/소프트웨어 컴포넌트의 집합.
- **TZASC/TZPC**: 메모리(DRAM) 및 주변장치(Peripheral)의 Secure/Non-secure 귀속 속성을 프로그래밍 관리하는 하드웨어 컨트롤러.

</details>

```text
┌──────── 비보안 상태 ────────┐     ┌──────── 보안 상태 ─────────┐
│       [비보안 영역]         │-----│   [신뢰 펌웨어•TEE]        │
└─────────────┬───────────────┘     └─────────────┬──────────────┘
              └----- [보안 전환 경로] ------------┘
                         |
                  [자원 보안 제어]
```

선의 의미: 비보안 OS와 Secure World TEE가 보안 전환 경로(SMC) 및 하드웨어 자원 보안 제어기(TZASC/TZPC)에 의해 상호 격리/연동되는 구조.

| 구성요소 | 책임 |
|:---|:---|
| 비보안 영역 | 범용 Rich OS(Linux/Android) 및 일반 사용자 App 구동 |
| 보안 전환 경로 | **SMC** 명령 및 Secure Monitor/SG 가드를 통한 모드 전환 제어 |
| 신뢰 펌웨어•TEE | 보안 펌웨어(ATF), **TEE** 보안 OS 및 보안 App(TA) 구동 |
| 자원 보안 제어 | **TZASC**(메모리), **TZPC**(주변장치) 컨트롤러 기반 **NS 비트** 바인딩 |

#### 한줄 요약

- A-profile의 SMC·보안 모니터 또는 M-profile의 Secure Gateway 같은 전환 경로와 자원 보안 제어가 실행 상태와 자원을 격리한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Secure Monitor**: Normal World와 Secure World 간의 Context Switch(레지스터 저장/복원)를 관장하는 최고 권한 펌웨어 계층.
- **공유 버퍼 검증(Shared-Buffer Validation)**: Normal World에서 인가된 주소 파라미터가 NS 영역 내에 존재하는지 TEE가 사전에 검증하는 보안 절차.

</details>

```text
[비보안 OS•응용의 보안 서비스 요청]
                  │
                  ▼
1. 보안 전환 진입점 검증
   - 승인된 진입점
   - 공유 버퍼 주소•길이
                  │
                  ▼
2. 보안 상태•자원 속성 강제
   - TrustZone 상태 전환
   - 버스 거래•자원 귀속 비교
                  │
                  ▼
3. TEE 보안 연산
   - 보안 메모리•장치 접근
   - 키•비밀 데이터 내부 처리
                  │
                  ▼
[비민감 결과만 비보안 영역에 반환]
```

### 동작 원리

1. **보안 전환 진입점 검증**: Normal World에서 **SMC** 수행 및 **Secure Monitor**를 통해 **공유 버퍼 검증** 진행.
2. **보안 상태·자원 속성 강제**: CPU 코어의 보안 상태 전환 및 AMBA **NS 비트** 하드웨어 통제 가동.
3. **TEE 보안 연산**: TEE와 신뢰 애플리케이션이 보안 메모리 안에서 비밀 키 연산 수행.

#### 한줄 요약

- 승인된 보안 서비스는 공유 입력을 검증하고 키 연산을 보안 자원 안에서 수행한 뒤 비민감 결과만 비보안 영역에 반환한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **OS 권한 격리**: Ring/EL(Execution Level) 기반 소프트웨어 관점 프로세스 간 페이지 테이블(MMU) 보호 방식.

</details>

| 격리 방식 | Arm TrustZone (Hardware Isolation) | OS 권한 격리 (Software Isolation) |
|:---|:---|:---|
| 적용 기준 | 암호 키, 부팅 로직, 생체 정보 보호 시 | 일반 애플리케이션과 사용자 프로세스 격리 시 |
| 핵심 특징 | 하드웨어 **NS 비트** 및 물리 상태(Secure/NS) 수평 분리 | MMU 페이지 테이블 및 커널 링(Ring 0~3) 기반 수직 분리 |
| 한계 | TEE 펌웨어 및 **SMC** 진입점 취약점 관리 요구 | **커널 침해**(Rooting/Exploit) 발생 시 전체 보안 와해 |

#### 한줄 요약

- 커널 침해와 분리해야 하는 키·부팅 코드는 TrustZone에, 일반 응용 프로세스의 상호 격리는 운영체제 페이지 권한에 맡긴다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **TCB 최소화(TCB Minimization)**: 공격 표면(Attack Surface)을 줄이기 위해 TEE 내부 코드 및 드라이버 수용을 극소화하는 원칙.
- **경계 취약점(Boundary Vulnerability)**: Normal World에서 전달된 잘못된 포인터(Point-to-Secure)를 TEE가 무비판 수용 시 발생하는 메모리 침범.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| TEE 내부 팽창에 따른 **TCB** 공격 표면 확대 | 보안 펌웨어 기능 극소화(**TCB 최소화**) 및 TA 분리 | 하드웨어 보안 영역 안정성 확보 |
| Normal World 포인터 수용 시 **경계 취약점** 발생 | **공유 버퍼 검증** 및 NS 영역 주소 범위 강제 바인딩 | Secure World 메모리 오염 방지 |
| DMA 컨트롤러를 통한 보안 메모리 무단 접근 위험 | SMMU 및 DMA 컨트롤러의 **NS 비트** 속성 통제 | DMA의 보안 메모리 무단 접근 차단 |

> 사례: **Arm TrustZone** 기반 암호화 키 보관 및 TEE 결제 모듈 구동

#### 한줄 요약

- TCB를 최소화하고 공유 입력 범위와 CPU·DMA의 자원 보안 속성을 함께 검증한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **보안 격리 지표(Security Isolation Metrics)**: 보호 데이터 치명도 및 커널 신뢰성 기반 TrustZone 채택 기준

</details>

- OS 침해와 격리할 키·부팅 코드는 **TrustZone**, 일반 프로세스는 **OS 권한 격리** 적용

#### 한줄 요약

- OS 침해와 격리할 자산은 TrustZone, 일반 프로세스는 OS 권한으로 보호한다.
