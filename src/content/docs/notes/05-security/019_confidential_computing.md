---
sidebar:
  order: 19
  label: "019. 기밀 컴퓨팅 (Confidential Computing)"
  badge:
    text: "미출제 • 50%"
    variant: note
title: "기밀 컴퓨팅 (Confidential Computing)"
date: "2026-08-13T18:48:54+09:00"
tags:
  - "notes-security"
weight: 19
extra:
  question_no: "019"
  source_status: "미출제"
  source_history: ""
  priority: 50
  priority_note: "클라우드•AI의 사용 중 데이터 보호 설계로 독립성이 큼"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **기밀 컴퓨팅(Confidential Computing)**: 하드웨어 기반 신뢰 실행 환경(TEE)과 원격 증명(Remote Attestation)을 통해 데이터 처리 및 사용 중(Data in Use) 기밀성과 무결성을 보장하는 기술.
- **사용 중 데이터(Data in Use)**: 응용 프로그램이 RAM 메모리에 적재되어 CPU/GPU 레지스터 및 캐시에서 연산 수행 중인 데이터.

</details>

- 정의/개념: TEE와 원격 증명으로 사용 중 데이터를 보호하는 **기밀 컴퓨팅**
- 배경/필요성: 저장•전송 암호화만으로는 **RAM 평문•관리자 권한** 노출이 남는다.

#### 한줄 요약

- 하드웨어 TEE 격리 및 원격 증명(Remote Attestation)을 통해 처리 중 데이터(Data-in-Use)의 기밀성과 무결성을 보장하는 클라우드 보안 기술

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **신뢰 실행 환경(Trusted Execution Environment, TEE)**: CPU/SoC 내부의 하드웨어 수준 격리 영역으로, 호스트 OS나 하이퍼바이저조차 내부 데이터에 접근 불가능한 안심 구역 (Intel SGX/TDX, AMD SEV 등).
- **원격 증명(Remote Attestation)**: TEE 내부에서 실행 중인 워크로드의 신원, 초기화 측정값 및 보안 상태를 서명된 암호학적 증거로 원격 검증기관에 입증하는 절차.
- **부채널 별도 통제(Side-channel Control)**: TEE 물리 경계 외부에 존재하는 캐시 타이밍, 전력 파형, 메모리 액세스 패턴 기반 측채널 공격을 방어하기 위한 추가 통제.

</details>

- **TEE** 하드웨어 암호화 엔진을 통한 CPU/RAM 상의 평문 연산 구간 완결적 격리
- **원격 증명** 메커니즘으로 무단 변조되지 않은 정당 워크로드의 초기화 상태 검증
- 검증 승인된 정상 TEE 워크로드에만 키 브로커가 암호키를 동적 배포
- 메모리 버스 이외의 캐시 및 물리 버스 통로에 대한 **부채널 별도 통제** 기법 병행

#### 한줄 요약

- 하드웨어 메모리 암호화, 원격 증명 기반 암호키 동적 바인딩 및 부채널(Side-channel) 위협 통제

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **워크로드(Workload)**: TEE 격리 구역 내부에서 안전하게 실행되는 대상 애플리케이션 및 연산 컨테이너.
- **측정값(Measurement)**: TEE 부팅 및 워크로드 로딩 시 바이너리, 코드, 초기 상태를 하드웨어 측에서 암호학적으로 해싱한 고유값 (MRTD, MRENCLAVE).
- **키 브로커(Key Broker Service, KBS)**: 원격 증명 검증기 결과가 정책을 완전 충족할 때에만 TEE 내부 워크로드로 대칭 세션키를 바인딩 전달하는 주체.

</details>

```text
기밀 컴퓨팅 구조
├─ TEE 하드웨어
├─ 보호 워크로드
├─ 증명 검증기
└─ 키 브로커
```

가지의 의미: 하드웨어 격리, 보호 워크로드, 암호학적 측정값 검증 및 보안키 분배 책임을 분리한 구조

| 구성요소 | 책임 |
|:---|:---|
| TEE 하드웨어 | CPU/SoC 차원의 하드웨어 기반 메모리 암호화 및 격리 환경(TEE) 제공 |
| 보호 워크로드 | TEE 내부 엔클레이브 또는 기밀 VM에서 실행되는 민감 연산 프로그램 |
| 증명 검증기 | TEE 서명 증명서 및 측정값(Measurement)을 보안 정책과 검증 대조 |
| 키 브로커 | 원격 증명을 통과한 정당 TEE로만 세션키 및 민감 데이터 래핑 제공 |


#### 한줄 요약

- TEE 하드웨어, 보호 워크로드, 측정값(Measurement) 검증기 및 키 브로커(Key Broker) 아키텍처

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **신뢰 컴퓨팅 기반(Trusted Computing Base, TCB)**: 시스템의 보안성을 유지하기 위해 신뢰해야 하는 필수 하드웨어, 펌웨어 및 소프트웨어 전체 영역.
- **측정값•증거 생성**: TEE 초기화 시 하드웨어 비밀키(Attestation Key)로 측정값에 서명하여 증명 패킷을 생성하는 단계.
- **증명•정책 검증**: 외부 증명 검증기가 제조사 CA 서명, TCB 버전에 따른 서명 패킷 및 측정값을 정책과 심사 대조하는 단계.
- **키 해제 승인**: 검증 성공 시 키 브로커가 래핑키 발급을 승인하는 단계.
- **워크로드용 비밀 래핑**: 수신자 TEE 전용 공개키로 대칭키를 암호화(Wrapping)하여 반환하는 단계.

</details>

```text
TEE 실행 요청
        │
        ▼
1. 측정값•증거 생성
        │
        └── 증명 증거 제출
                    │
                    ▼
2. 증명•정책 검증
        ├─ 실패: 키 제공 차단
        └─ 성공
             │
             ▼
     3. 키 해제 승인
             │
             ▼
     4. 워크로드용 비밀 래핑
             │
             └── 암호화된 비밀 반환
```

### 동작 원리

1. **측정값•증거 생성**: TEE 로딩 시 하드웨어 주도 측정값 산출 및 루트 키 기반 암호 서명 증거 생성
2. **증명•정책 검증**: **RFC 9334** 규격 기반 검증기의 측정값, 제조사 서명 및 TCB 패치 수준 심사
3. **키 해제 승인**: 검증 통과 시 키 브로커(KBS)에 대한 키 유도 및 해제 승인 부여
4. **워크로드용 비밀 래핑**: 승인된 target TEE의 임시 공개키로 암호키를 안전하게 래핑(Wrapping) 전달


#### 한줄 요약

- TEE 측정값 및 TCB 증명 증거 생성, RFC 9334 정책 검증, 키 해제 승인 및 세션키 래핑 반환 흐름

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **엔클레이브(Enclave)**: 애플리케이션의 특정 민감 함수/코드 블록 단위만 TEE로 물리 격리하는 방식 (Intel SGX 등).
- **기밀 가상머신(Confidential VM, CVM)**: 수정 없이 가상머신(VM) 전체의 게스트 OS 및 메모리를 호스트로부터 격리 암호화하는 방식 (AMD SEV-SNP, Intel TDX).
- **가속기 TEE(Accelerator TEE)**: GPU, NPU 등 외장 가속 장치 모듈과의 PCIe 통신 및 연산 메모리를 격리 암호화하는 아키텍처 (NVIDIA H100 Confidential Computing).

</details>

| 기밀 컴퓨팅 방식 | **애플리케이션 엔클레이브** | **기밀 가상머신 (Confidential VM)** | **가속기 TEE (Accelerator TEE)** |
|:---|:---|:---|:---|
| 적용 기준 | 민감 모듈 중심 보안 정밀화 | 기존 레거시 앱 무수정 클라우드 이관 | 대규모 AI/ML 모델 및 GPU 연산 보호 |
| 핵심 특징 | **엔클레이브** 기반 함수 단위 극소 격리 | **기밀 VM** 기반 게스트 OS 전면 암호화 | PCIe 인터페이스 및 GPU 메모리 격리 |
| 한계 | 소스코드 재설계 및 리팩토링 부담 | 상대적으로 큰 TCB 및 공격 표면 | 장치 드라이버 및 버스 인터페이스 통제 복잡성 |

> 요약: 워크로드 수정 가능 여부, TCB 크기 및 가속기(GPU) 사용 요구에 따른 TEE 모델 선택

#### 한줄 요약

- 애플리케이션 엔클레이브(Enclave), 기밀 VM(Confidential VM), 가속기 TEE(GPU/NPU)의 보호 영역별 비교 선택

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **부채널 공격(Side-channel Attack)**: 캐시 메모리 액세스 타임, 전력 소비량, 미세 전자기파를 관측하여 TEE 내부 암호키를 추론하는 공격.
- **IETF RFC 9334(Remote Attestation Procedures, RATS)**: 원격 증명 프로토콜의 표준 아키텍처 및 역할(Attester, Verifier, Relying Party) 규정 문서.
- **IETF RFC 9711 / EAT(Entity Attestation Token)**: TEE 증명 클레임 패킷 전송을 위한 표준 JWT/CBOE 토큰 포맷 규격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 원격 증명 표준 미비 | **IETF RFC 9334 (RATS)** 및 **RFC 9711 (EAT)** 준수 | 원격 증명 및 클레임 토큰 호환성 확보 |
| 측정 불일치 및 취약 TCB | **TCB 최소화 및 자동 보안 패치 연동** | 노후 TCB 기반 증명 거부 및 위험 완화 |
| 캐시/타이밍 **부채널 공격** | **Constant-time 연산 코드 및 캐시 플러시** | 측채널 정보 유출 가능성 방어 |
| 가속기 Bus 통로 노출 | **PCIe IDE(Integrity & Data Encryption) 적용** | 호스트 버스 상의 데이터 패킷 도청 차단 |

#### 한줄 요약

- IETF RFC 9334/9711(EAT) 준수, TCB 최소화, DMA 메모리 암호화 및 원격 증명 실패 시 키 해제 즉시 차단

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **기밀 컴퓨팅 아키텍처 선택(Confidential Computing Selection)**: 보호 대상 크기(TCB), 코드 수정 가능성 및 GPU 연산 여부를 감안한 TEE 구현 지침.

</details>

- 워크로드 성격에 따라 응용 일부는 **엔클레이브**, 전체 이관은 **기밀 VM(Confidential VM)**, AI 처리는 **가속기 TEE** 선택 적용

#### 한줄 요약

- **TEE 선택•원격 증명•키 브로커 차단**을 함께 적용
