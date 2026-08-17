---
sidebar:
  order: 64
  label: "064. Arm TrustZone 보안 확장"
  badge:
    text: "기출 • 50%"
    variant: note
title: "Arm TrustZone 보안 확장"
date: "2026-08-17T09:25:00+09:00"
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

<details><summary>용어 설명</summary>

- **Arm TrustZone**: 단일 물리 코어와 버스를 논리적으로 보안(Secure)과 비보안(Non-Secure) 두 도메인으로 분할하는 시스템 수준의 하드웨어 보안 확장 아키텍처.
- **Secure World(보안 세계)**: 암호 키, 생체 정보, DRM 등 고신뢰 자산이 상주하는 신뢰 실행 환경(TEE).
- **Normal World(일반 세계)**: Android, Linux 등 범용 OS(Rich OS) 및 사용자 앱이 동작하는 비보안 환경.

</details>

- 정의/개념: 단일 물리 프로세서 및 시스템 버스를 논리적으로 보안 세계(Secure World)와 일반 비보안 세계(Normal World)로 2분할하여 하드웨어 수준의 시스템 격리를 제공하는 Arm 아키텍처 보안 확장 기술
- 배경/필요성: 범용 OS(Android, Linux)의 취약점 및 루트 권한 탈취 시에도 **암호화 키, 생체 인증(지문/홍채), 결제 정보 및 보안 부팅 루트 오브 트러스트(RoT) 보호**

#### 한줄 요약

- 단일 칩을 **보안/비보안 세계(Secure/Normal World)로 2분할하는 하드웨어 수준 보안 격리**

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **NS-Bit(Non-Secure Bit)**: AXI/AMBA 버스 트랜잭션마다 하드웨어 신호선으로 전달되어 해당 요청이 비보안(NS=1)인지 보안(NS=0)인지를 명시하는 보안 태그.
- **Shared Memory(공유 메모리)**: Normal World와 Secure World 간에 파라미터를 교환하기 위해 Normal World 메모리 영역에 할당된 통신 버퍼.

</details>

- 프로세서 상태를 **보안 상태(Secure State)**와 **비보안 상태(Non-Secure State)**로 시스템 차원 수평 격리
- AMBA 시스템 버스에 **NS-Bit(Non-Secure Bit)**를 추가하여 하드웨어 차원에서 비인가 메모리/장치 접근 원천 차단
- Normal World에서 Secure World로 전환 시 **SMC(Secure Monitor Call)** 명령어 및 최고 권한 모니터(EL3)를 통한 엄격한 진입 통제

#### 한줄 요약

- **NS-Bit 기반 시스템 버스 하드웨어 격리·SMC 기반 도메인 전환·Secure Monitor 검열**

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SMC(Secure Monitor Call)**: Normal World에서 Secure World로의 도메인 전환을 요청하는 전용 트랩 명령어.
- **TEE(Trusted Execution Environment)**: Secure World 내부에서 동작하는 초경량 보안 마이크로커널 OS (OP-TEE, QSEE, Knox).
- **TZASC / TZPC**: DRAM 메모리 영역(TZASC) 및 주변 장치(TZPC)의 보안/비보안 속성을 하드웨어 레지스터로 분할 설정하는 컨트롤러.

</details>

```text
[ Arm TrustZone 하드웨어 2분할 아키텍처 ]
┌──────────────────────────────┐        ┌──────────────────────────────┐
│ Normal World (비보안 세계)   │        │ Secure World (보안 세계)     │
│  ├─ User Space (카카오톡, 앱)│        │  ├─ Trusted Apps (생체, 결제)│
│  └─ Rich OS (Android/Linux)  │        │  └─ TEE OS (OP-TEE, MicroOS) │
└──────────────┬───────────────┘        └──────────────┬───────────────┘
               │ (SMC 호출)                            │ (결과 반환)
┌──────────────┴───────────────────────────────────────┴──────────────┐
│ Secure Monitor (EL3 모니터 펌웨어 : 문맥 전환 및 보안 상태 전이)   │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ [ AMBA AXI Bus (NS-Bit) ]
┌──────────────────────────────┴──────────────────────────────────────┐
│ 하드웨어 보안 제어 블록 (TZASC : 메모리 보호, TZPC : 주변장치 보호) │
└─────────────────────────────────────────────────────────────────────┘
```

선의 의미: 비보안 세계(Normal World/Rich OS), SMC 모니터 콜, 시큐어 모니터(EL3), 보안 세계(Secure World/TEE) 및 TZASC/TZPC 하드웨어 격리 간의 TrustZone 아키텍처 구조도.

| 구성요소 | 책임 |
|:---|:---|
| 일반 비보안 상태 영역 | 해커가 언제든 뚫을 수 있는 안드로이드나 카카오톡 같은 범용(Rich) OS와 앱들이 뛰노는 무방비 운동장 |
| 에스엠씨 보안 전환 검열소 | 안드로이드가 보안 영역에 노크할 때, "멈춰!" 하고 몸수색을 하는 문지기 명령어(**에스엠씨**) 및 모니터 |
| 깐깐한 티이이 신뢰 실행 구역 | 해킹이 불가능한 방탄유리 안에서 암호 키를 관리하고 지문 인식을 돌리는 초경량 보안 OS(**티이이**) |
| 티지컨트롤러 하드웨어 철조망 | "이 메모리와 장치는 귀족(보안) 전용이니 천민(일반)이 건드리면 쫓아낸다"고 설정하는 하드웨어 통제 칩 |

#### 한줄 요약

- **Normal World(Rich OS)·SMC 명령어·Secure Monitor(EL3)·Secure World(TEE)·TZASC/TZPC**

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Secure Monitor**: EL3(Exception Level 3)에서 동작하며 Normal/Secure World 간 CPU 레지스터 백업/복원 및 NS-Bit 상태 전이를 총괄하는 펌웨어.

</details>

```text
[ TrustZone SMC 호출 및 보안 연산 시퀀스 ]
                         │
                         ▼
   [ 1. Normal World 앱이 커널을 통해 SMC(Secure Monitor Call) 명령어 실행 ]
                         │
                         ▼
   [ 2. EL3 Secure Monitor 진입 : Normal World CPU 레지스터 문맥 저장 ]
                         │
                         ▼
   [ 3. CPU 상태를 Secure State(NS=0)로 전환 후 TEE 커널로 디스패치 ]
                         │
                         ▼
   [ 4. TEE 내부에서 비밀 키 및 생체 인증 데이터 기반 보안 연산 수행 ]
                         │
                         ▼
   [ 5. 공유 메모리에 결과(Status Code)만 기록 후 SMC 복귀 (NS=1 전환) ]
```

**동작 원리**

1. **SMC 요청**: Rich OS가 지문 검증을 위해 공유 버퍼 주소를 레지스터에 담고 SMC 호출
2. **모니터 트랩**: CPU가 EL3 Secure Monitor로 트랩되어 Normal World 레지스터를 TCB에 저장
3. **도메인 전환**: Secure Monitor가 SCR(Secure Configuration Register)의 NS-Bit를 0으로 클리어
4. **TEE 연산**: Secure World의 TEE가 하드웨어 보안 메모리에서 암호 키를 꺼내 지문 템플릿 매칭 수행
5. **결과 반환**: 암호 키는 절대 유출하지 않고 "인증 성공/실패" 결과만 공유 메모리에 기록 후 Normal World로 복귀

#### 한줄 요약

- SMC 노크 $\to$ **Secure Monitor 문맥 보존 & NS=0 전환 $\to$ TEE 보안 연산 $\to$ 공유 메모리 검증 $\to$ 결과 반환**

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **TrustZone vs OS 커널 권한 vs Hypervisor**:
  - TrustZone: 하드웨어 버스 NS-Bit 2분할, 커널 해킹 시에도 TEE 불침
  - OS 권한 격리: Ring 0/Ring 3 소프트웨어 분리, 루트 탈취 시 붕괴
  - Hypervisor: EL2 가상화, VM 간 격리, 실시간 지연 오버헤드

</details>

| 비교 항목 | Arm TrustZone (하드웨어 2분할 격리) | OS 커널 권한 격리 (Ring 0 / Ring 3) | 가상화 하이퍼바이저 격리 (Type-1 Hypervisor) |
|:---|:---|:---|:---|
| 격리 메커니즘 | 하드웨어 버스 NS-Bit 태깅 수평 2분할 | MMU 페이지 테이블 및 CPU Privilege 레벨 | 하이퍼바이저(EL2) 가상화 및 2단계 페이징 |
| 보안 신뢰 수준 | OS 커널 탈취 시에도 Secure World 불침 | OS 커널 취약점(루팅) 시 전체 보안 붕괴 | 하이퍼바이저 손상 시 모든 VM 위험 노출 |
| 한계 및 적합 분야 | TEE 펌웨어/SMC 핸들러 취약점 분석 난제 | 프로세스 간 단순 격리 (보안 자산 보호 불가) | VM 오버헤드 및 실시간 지연시간 발생 |

#### 한줄 요약

- 루트 보호는 **TrustZone**, 일반 프로세스는 **OS 권한**, 멀티 OS는 **하이퍼바이저**

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **TCB(Trusted Computing Base) 최소화**: Secure World 내부 코드 라인 수를 수만 라인 이하로 극소화하여 공격 표면(Attack Surface)을 원천 축소하는 설계.
- **SMMU(System MMU) 격리**: DMA 컨트롤러나 GPU가 비보안 상태에서 보안 메모리를 직접 읽지 못하도록 I/O 가상화 단에서 NS-Bit 검증을 강제하는 하드웨어.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 방탄유리(TEE) 안에 쓸데없이 앱을 너무 많이 깔아놔서(TCB 팽창) 해커가 뚫고 들어올 쥐구멍이 많아지는 공격 표면 확대 비상 | 방탄유리 안에는 지문과 암호 키만 남기고 싹 다 쫓아내는 극한의 다이어트(**티씨비 최소화**) 강제 적용 | 방탄유리가 깨질 확률(공격 표면)을 극소화하여 가장 핵심적인 하드웨어 보안 영역 안정성 사수 달성 |
| 안드로이드가 방탄유리 문구멍으로 독극물 포인터(잘못된 메모리 주소)를 밀어 넣어 보안 램을 오염시키는 **경계 취약점** | 문구멍(**공유 버퍼**)으로 들어오는 파라미터 주소가 진짜 안드로이드 구역(NS) 맞는지 뼈와 살을 분리하며 깐깐하게 **공유 버퍼 검증** | 독극물 파라미터 주입으로 인한 Secure World 내부의 핵심 보안 메모리 오염 및 통제권 탈취 완벽 방어 |
| 해커가 CPU 대신 DMA(직접 메모리 접근 칩)를 꼬드겨서 보안 메모리를 몰래 짐수레로 빼돌리는 우회 공격 꼼수 위험 발발 | SMMU와 DMA 컨트롤러 장치에도 **엔에스 비트**(NS) 완장 검열을 똑같이 떡칠하여 하드웨어 접근 원천 통제 | DMA 칩이 미쳐 날뛰며 보안 메모리를 털어가는 하드웨어 우회(Bypass) 탈취 공격 100% 얄짤없이 차단 |

#### 한줄 요약

- **TCB 최소화(Microkernel TEE)·공유 메모리 포인터 무결성 검증·SMMU 기반 DMA 격리**

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **Armv9 CCA(Confidential Compute Architecture)**: 기존 TrustZone의 2분할을 넘어 렐름(Realm) 기반의 동적 기밀 컴퓨팅으로 진화하여 하이퍼바이저조차 신뢰하지 않는 완전 격리 지원.

</details>

- 모바일, IoT 및 자동차 ECU 보안에서 **Arm TrustZone 기반 TEE(OP-TEE/Samsung Knox) 및 하드웨어 Root of Trust 표준 채택**

#### 한줄 요약

- **보안 자산의 중요도와 TCB 최소화 원칙**에 맞춘 TrustZone 격리 아키텍처 설계
