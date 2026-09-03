---
sidebar:
  order: 64
  label: "064. Arm TrustZone 보안 확장 (Arm TrustZone)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "Arm TrustZone 보안 확장 (Arm TrustZone)"
date: "2026-08-31T09:55:00+09:00"
tags:
  - "notes-hardware"
weight: 64
extra:
  question_no: "064"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "하드웨어 보안 격리와 TEE 신뢰 실행 환경의 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Arm TrustZone**: 프로세서와 시스템 자원을 일반 영역과 보안 영역으로 분리하는 Arm 보안 확장 아키텍처.
- **신뢰 실행 환경(Trusted Execution Environment, TEE)**: 범용 운영체제(Android, Linux)와 물리적/논리적으로 분리되어 인증, 결제, 암호 키 관리, DRM 등 민감 연산을 안전하게 실행하는 격리 실행 환경.

</details>

- 정의/개념: 단일 프로세서 코어와 시스템 버스를 **Normal World**와 **Secure World**로 분할하여 신뢰 실행 환경(TEE)을 구축하는 **Arm TrustZone 보안 확장 아키텍처**
- 배경/필요성: 리치 OS(Android, Linux) 커널의 방대한 공격 표면 및 권한 탈취 시 **암호 키, 생체 인증 등 핵심 보안 자산의 동반 유출 위험**

#### 한줄 요약
- Arm TrustZone은 시스템 버스 신호 레벨에서 하드웨어 격리를 강제하여 일반 OS가 해킹되어도 Secure World의 암호 자산을 보호한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **NS(Non-Secure) 제어 비트**: AXI/AMBA 시스템 버스 트랜잭션 신호선에 하드웨어로 포함되어 현재 메모리/I/O 접근이 보안 영역인지 비보안 영역인지를 칩 레벨에서 판별하는 비트.
- **보안 모니터(Secure Monitor)**: EL3 최고 특권 예외 레벨에서 동작하며, Secure World와 Normal World 간의 하드웨어 레지스터 문맥 전환을 안전하게 중계하는 전용 펌웨어.

</details>

- 버스 레벨 하드웨어 격리: AXI 버스의 **NS(Non-Secure) 비트**를 통해 메모리 컨트롤러와 주변장치가 Normal World의 불법 접근을 하드웨어로 차단
- 안전한 문맥 전환 관문: **보안 모니터(EL3)**를 유일한 전환 관문으로 삼아 레지스터 정화 및 문맥 교환 보장
- 최소 신뢰 코드 베이스(TCB): Secure World에는 필수적인 경량 **신뢰 OS(OP-TEE)**와 신뢰 앱(TA)만 상주시켜 공격 표면 극소화

#### 한줄 요약
- AXI 버스의 NS 제어 비트로 하드웨어 격리를 강제하고, EL3 보안 모니터를 통해 안전하게 문맥을 교환한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **TZASC(TrustZone Address Space Controller)**: DRAM 메인 메모리의 특정 주소 범위를 보안 영역과 일반 영역으로 동적 분할 보호하는 하드웨어 컨트롤러.
- **TZPC(TrustZone Protection Controller)**: 타이머, 인터럽트 컨트롤러(GIC), 암호 가속기 등 온칩 주변장치의 보안 속성을 설정하는 하드웨어 모듈.

</details>

```text
[Arm TrustZone 시스템 하드웨어 격리 아키텍처]
 ├─ 일반 영역 (Normal World)
 │   ├─ 클라이언트 애플리케이션 (CA)
 │   └─ 범용 리치 OS (Android, Linux - EL1)
 ├─ 보안 영역 (Secure World - TEE)
 │   ├─ 신뢰 애플리케이션 (TA: 결제, 생체, 키)
 │   └─ 신뢰 OS (OP-TEE, Trusted OS - S-EL1)
 ├─ 보안 모니터 (Secure Monitor - EL3) ── 레지스터 정화 및 문맥 전환
 └─ 시스템 버스 보호 하드웨어
     ├─ TZASC ── DRAM 메모리 영역 보안/비보안 분할 격리
     └─ TZPC ─── 온칩 암호 엔진 및 주변장치 보안 잠금
```

선의 의미: 가지(`├─`, `└─`)는 계층 및 하드웨어 보안 경계; SMC 호출 시 EL3 보안 모니터가 문맥을 전환하고, AXI 버스의 NS 비트로 메모리 접근을 통제함

| 구성요소 | 책임 |
|:---|:---|
| 일반 영역 | 범용 OS와 클라이언트 앱 실행 |
| 보안 영역 | **암호 키·생체 정보** 격리 연산 |
| 보안 모니터 | **SMC** 처리와 두 영역의 문맥 전환 |
| TZASC | DRAM 주소 영역별 보안 속성 통제 |
| TZPC | 온칩 주변장치의 보안 속성 통제 |

#### 한줄 요약
- TZASC와 TZPC가 버스와 메모리·주변장치 사이에 끼어들어 접근마다 보안 속성을 확인하므로 일반 OS의 소프트웨어 권한 검사에 기댈 필요가 없어지고, 두 영역을 오가는 통로는 EL3 보안 모니터 한 곳으로만 좁혀진다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **SMC(Secure Monitor Call)**: Normal World에서 Secure World의 보안 서비스를 호출하기 위해 하드웨어 트랩을 발생시키는 특권 명령어.

</details>

```text
일반 영역 요청
      │
      ▼
1. SMC 호출
      │
      ▼
2. 호출 검증
 ┌────┴────┐
 │ 실패    │ 성공
 ▼         ▼
오류 반환  3. 보안 문맥 전환
                │
                ▼
           4. 신뢰 연산
                │
                ▼
           5. 문맥 정화·복원
                │
                ▼
             결과 반환
```

동작 원리:

1. SMC 호출: 일반 영역에서 보안 서비스 진입
2. 호출 검증: 매개변수와 호출 권한 확인
3. 보안 문맥 전환: 일반 문맥 저장 후 영역 절체
4. 신뢰 연산: 보호 자원으로 보안 기능 수행
5. 문맥 정화·복원: 잔여 정보 제거 후 복귀

#### 한줄 요약
- TrustZone은 코어를 둘로 늘리지 않고 시분할로 두 세계를 오가 면적 비용을 아끼는 대신 호출마다 문맥 저장과 정화 비용을 치르므로, 보안 서비스 호출이 잦을수록 이득이 줄어든다.

## Ⅴ. 종류 및 비교

| 하드웨어 보안 격리 기술 | Arm TrustZone | Intel SGX (Software Guard Extensions) | 하이퍼바이저 기반 가상화 격리 | 전용 보안 칩 (TPM / SE) |
|:---|:---|:---|:---|:---|
| 격리 단위 및 범위 | **SoC 전체 시스템 분할** (2개 World) | 프로세스 내부 특정 **엔클레이브(Enclave)** | 가상 머신(VM) 단위 파티셔닝 | 독립된 물리 외장 실리콘 칩 |
| 하드웨어 구현 방식 | **AXI 버스 NS 비트** 및 TZASC/TZPC | CPU 내부 메모리 암호화 엔진(MEE) | CPU 하드웨어 가상화 확장 | 별도 SPI/I2C 버스 직결 칩셋 |
| 신뢰 코드 베이스 (TCB) | 작음 (경량 Trusted OS) | **매우 작음** (엔클레이브 코드) | 큼 (하이퍼바이저 전체 코드) | **최소** (독립 보안 OS) |
| 주요 적용 분야 | **스마트폰, 자동차 전장 SoC** | **클라우드 기밀 컴퓨팅** | 멀티테넌트 퍼블릭 클라우드 서버 | PC 보안 부팅 키 저장, 스마트카드 |

#### 한줄 요약
- 스마트폰 및 임베디드 SoC 전역 보안에는 TrustZone이 표준이며, 클라우드 프로세스 격리에는 SGX가, 외장 키 저장에는 TPM이 쓰인다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **TOCTOU(Time-of-Check to Time-of-Use)**: 검사 시점과 실제 사용 시점 사이에 악의적인 일반 OS가 공유 메모리 데이터를 비동기로 바꿔치기하는 공격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 공유 버퍼 참조 시 TOCTOU 변조 위험 | **보안 DRAM 내부 복사** 후 파라미터 유효성 검증 | 검사 후 사용 시점 사이의 데이터 위변조 차단 |
| 비보안 DMA 마스터의 보안 메모리 우회 접근 | **SMMU 연동** 장치별 NS 비트 강제 검증 | DMA 우회 경로를 통한 메모리 탈취 차단 |
| 단일 신뢰 앱 취약점 시 TEE 침해 위험 | **신뢰 앱 간 공간 격리** 및 최소 권한 원칙 적용 | 특정 TA 손상 시 Secure World 전체 피해 방지 |

#### 한줄 요약
- 실무에서는 보안 메모리 복사로 TOCTOU를 막고, SMMU로 DMA 우회를 차단하며, TA 간 메모리 격리로 안전성을 완성한다.

## Ⅶ. 결론

- 모바일, IoT 및 차량용 SoC의 **하드웨어 기반 신뢰 실행 환경(TEE) 구축을 위한 지배적 산업 표준**으로 안착되었으며, 최근에는 Armv9 **기밀 컴퓨팅 아키텍처(CCA, Confidential Compute Architecture)의 렐름(Realm) 관리 확장**과 결합하여 클라우드 및 멀티테넌트 엣지 기밀 보호로 진화 지속

#### 한줄 요약
- Arm TrustZone은 버스 신호 레벨의 물리적 격리를 통해 일반 OS 침해 시에도 핵심 암호 자산을 보호하는 모바일 보안의 핵심 뼈대다.
