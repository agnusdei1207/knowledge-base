---
sidebar:
  order: 128
  label: "128. ARM TrustZone 하드웨어 보안"
  badge:
    text: "기출 · 50%"
    variant: note
title: "ARM TrustZone 하드웨어 보안 (ARM TrustZone TEE)"
date: "2026-08-21T23:42:00+09:00"
tags:
  - "notes-security"
weight: 128
extra:
  question_no: "128"
  source_status: "기출"
  source_history: "119회, 126회, 131회"
  priority: 50
  priority_note: "모바일·임베디드 하드웨어 신뢰 실행 환경(TEE) 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **ARM TrustZone**: 단일 물리적 프로세서 코어를 하드웨어 수준에서 일반 세계(Normal World)와 보안 세계(Secure World)로 공간 격리하는 시스템 보안 아키텍처.
- **신뢰 실행 환경(Trusted Execution Environment, TEE)**: 보안 세계(Secure World)에서 실행되는 격리된 운영체제(Secure OS) 및 신뢰 애플리케이션(TA) 구동 환경.
- **보안 모니터(Secure Monitor)**: SMC(Secure Monitor Call) 인스트럭션을 통해 일반 세계와 보안 세계 간 컨텍스트 스위칭을 관장하는 최상위 권한 계층(EL3).

</details>

- 정의/개념: 단일 CPU 코어와 버스 인프라를 **하드웨어 수준에서 일반 세계(Normal World)와 보안 세계(Secure World)로 시분할·공간 격리**하여 중요 연산과 암호키를 보호하는 시스템 보안 기술
- 배경/필요성: 범용 OS(Android, Linux)의 방대한 코드베이스로 인한 커널 취약점 공격으로부터 결제 인증, 생체 정보, DRM 암호키를 안전하게 보호할 하드웨어 격리 영역 필요

#### 한줄 요약

- 단일 CPU를 하드웨어적으로 분할하여 일반 OS와 격리된 보안 실행 환경(TEE)을 제공

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Non-Secure(NS) 비트**: AXI 시스템 버스 신호에 포함되어 현재 접근 요청이 일반 세계(NS=1)인지 보안 세계(NS=0)인지를 하드웨어적으로 식별하는 제어 비트.
- **TZASC(TrustZone Address Space Controller)**: 메인 메모리(DRAM)를 여러 영역으로 분할하고 각 영역에 대한 보안/비보안 접근 권한을 동적으로 제어하는 메모리 보안 컨트롤러.

</details>

- 하드웨어 버스 수준에서 **NS 비트 기반 메모리 및 주변장치 접근 통제**
- 최상위 권한 계층(**EL3 Secure Monitor**)을 통한 안전한 세계 전환(Context Switching)
- 보안 메모리(SRAM/DRAM) 및 보안 주변장치(암호 가속기, 타이머)의 **물리적 분리 없이 논리적 완전 격리** #### 한줄 요약

- NS 비트와 보안 모니터를 통해 버스 및 메모리 수준에서 일반 세계의 보안 자원 접근을 원천 차단

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **TZPC(TrustZone Protection Controller)**: 특정 입출력 주변장치(키패드, 지문 센서 등)를 보안 세계 전용 또는 비보안 전용으로 설정하는 주변장치 보호 컨트롤러.

</details>

```text
[ 일반 세계 (Normal World / Rich Execution Environment) ]       [ 보안 세계 (Secure World / Trusted Execution Environment) ]
  일반 애플리케이션 (Android Apps) ── Client API                   신뢰 애플리케이션 (Trusted Apps: 생체인증/키관리)
            │                                                                    │
  풍부한 범용 OS 커널 (Linux Kernel / Driver)                     보안 마이크로커널 (Secure OS: OP-TEE, Trusty)
            │                                                                    │
            └─────────────── SMC (Secure Monitor Call) ──────────────────────────┘
                                        │
                         [ 보안 모니터 (Secure Monitor / EL3) ]
                                        │
           (AXI System Bus: NS=0 보안 접근 / NS=1 비보안 접근 필터링)
                                        │
              ┌─────────────────────────┴─────────────────────────┐
              ▼                                                   ▼
  [ TZASC (DRAM 영역 보안 통제) ]                     [ TZPC (보안 주변장치 통제) ]
```

선의 의미: 일반 세계와 보안 세계가 SMC 명령 및 EL3 보안 모니터를 거쳐 AXI 버스 상에서 격리 접근하는 구조

| 구성요소 | 책임 |
|:---|:---|
| 일반 세계 (Normal World) | 풍부한 사용자 경험(Rich OS)을 제공하며 **보안 세계로의 직접 메모리 접근이 차단된 비보안 영역** |
| 보안 세계 (Secure World) | 최소화된 보안 OS(Secure OS) 기반으로 **생체 정보 처리, 키 생성 및 결제 서명 연산 수행** |
| 보안 모니터 (Secure Monitor / EL3) | 일반/보안 세계 간의 **CPU 레지스터 상태 저장·복원 및 안전한 컨텍스트 스위칭 제어** |
| TZASC (메모리 제어기) | DRAM 주소 공간을 분할하여 **일반 세계의 보안 메모리 영역 접근 시도 차단** |
| TZPC (주변장치 제어기) | 암호 엔진, 난수생성기(TRNG), 디스플레이를 **보안 세계 전용 하드웨어로 지정 통제** |

#### 한줄 요약

- Normal World와 Secure World가 보안 모니터와 AXI 버스 제어기를 통해 하드웨어 수준에서 격리

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **SMC(Secure Monitor Call)**: 일반 세계의 OS 커널이 보안 세계의 서비스를 호출하기 위해 CPU 예외를 발생시켜 EL3 보안 모니터로 진입하는 명령어.

</details>

```text
[ 1. 일반 앱: TEE Client API 경유 생체인증 요청 ]
                       │
                       ▼
[ 2. 일반 OS 커널: SMC 인스트럭션 실행 ]
                       │
                       ▼
[ 3. EL3 보안 모니터: 일반 세계 레지스터 백업 및 Secure World 전환 ]
                       │
                       ▼
[ 4. Secure OS / 신뢰 앱(TA): 보안 메모리 및 하드웨어 암호 엔진 접근 처리 ]
                       │
                       ▼
[ 5. EL3 보안 모니터: 결과 반환 및 Normal World 복귀 ]
```

**동작 원리** 1. **서비스 요청**: 일반 애플리케이션이 결제 서명을 위해 TEE 드라이버 호출
2. **SMC 전환**: 일반 OS 커널이 `SMC` 명령을 실행하여 EL3 권한 계층 진입
3. **모니터 스위칭**: 보안 모니터가 일반 세계 상태를 저장하고 AXI NS 비트를 `0`으로 전환
4. **보안 연산**: Secure OS 상의 신뢰 애플리케이션(TA)이 암호키 연산 및 지문 매칭 수행
5. **결과 복귀**: 연산 완료 후 성공/실패 코드만 일반 세계로 전달하고 복귀

#### 한줄 요약

- 일반 OS 요청 $\to$ SMC 호출 $\to$ EL3 모니터 전환 $\to$ 보안 연산 수행 $\to$ 일반 세계 안전 복귀

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **SE(Secure Element)**: CPU와 완전히 물리적으로 분리된 전용 칩셋(스마트카드 칩 등)으로 최고 수준의 물리적 보안을 제공하나 연산 능력이 제한됨.

</details>

| 보안 실행 아키텍처 | ARM TrustZone (TEE) | 보안 요소 (Secure Element, SE) | 범용 소프트웨어 암호화 |
|:---|:---|:---|:---|
| 적용 기준 | **고성능 연산(생체인증, DRM)** 및  하드웨어 격리가 모두 필요한 모바일/IoT | **금융 IC칩, eSIM, 암호화폐 하드웨어 지갑** 등 초고도 위변조 방지 | 단순 로컬 파일 암호화 등 **저비용 범용 시스템** |
| 격리 수준 | **단일 칩 내 하드웨어 논리적 분할 (Bus/Core 격리)** | **완전 독립된 물리적 보안 전용 칩셋 (HW 분리)** | OS 메모리 내 **소프트웨어 프로세스 격리** |
| 핵심 특징 | 고속 CPU 연산 능력, 대용량 보안 메모리 지원 | 물리적 탬퍼링(Tampering) 방어, 전력 분석 공격 차단 | 하드웨어 추가 비용 없음, 구현 용이성 |
| 한계 | Secure OS 취약점 및 부채널(Microarchitectural) 공격 노출 가능 | CPU 연산 속도 및 저장 용량 극히 제한, 단가 상승 | **OS 커널 탈취 시 암호키 및 평문 메모리 전면 유출** |

#### 한줄 요약

- SE는 물리적 칩 격리로 최고 보안을 제공하고, TrustZone은 고성능 연산과 하드웨어 격리의 최적 균형을 제공

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **최소 권한의 법칙(Principle of Least Privilege)**: 보안 세계(Secure World)에 포함되는 코드 라인 수(TCB)를 최소화하여 공격 표면을 극소화하는 설계 원칙.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Secure OS 내 코드 비대화로 인한 **신뢰 기반(TCB) 취약점 증가** | **마이크로커널 아키텍처 적용 및 필수 TA만 선별 배포** | 보안 세계 공격 표면(Attack Surface) 최소화 |
| 일반 세계와 보안 세계 간 공유 메모리를 통한 **레이스 컨디션(TOC-TOU) 공격** | **공유 메모리 입력값의 보안 세계 로컬 스택 복사 후 검증** | 버퍼 오염 및 메모리 변조 차단 |
| CPU 투기적 실행(Speculative Execution) 및 **부채널 캐시 분석 공격** | **코어 파티셔닝, 캐시 플러시(Flush) 및 사이드채널 방어 패치 적용** | 비밀키 추론 및 마이크로아키텍처 정보 유출 방지 |

#### 한줄 요약

- TCB 최소화, 입력 복사 검증, 부채널 방어 패치를 적용하여 TrustZone 보안성을 극대화

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **기밀 컴퓨팅(Confidential Computing)**: ARM CCA(Confidential Compute Architecture) 등 하드웨어 격리 영역을 하이퍼바이저로부터도 보호하는 차세대 신뢰 실행 기술.

</details>

- ARM TrustZone은 스마트폰, 스마트 자동차(ADAS), IoT 기기의 신뢰 닻(Root of Trust) 역할을 수행하는 핵심 하드웨어 보안 기술이며, 향후 클라우드 및 가상화 환경으로의 확장을 위해 ARM Realm(CCA)과 결합하여 런타임 데이터 보호 수준을 지속 고도화해야 함

#### 한줄 요약

- TCB 최소화와 버스 수준 격리를 통해 시스템 전반의 하드웨어 신뢰 실행 환경(TEE)을 확립
