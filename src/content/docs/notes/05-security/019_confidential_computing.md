---
sidebar:
  order: 19
  label: "019. 기밀 컴퓨팅"
  badge:
    text: "미출 · 50%"
    variant: note
title: "하드웨어 격리 기반 사용 중 데이터 보호 : 기밀 컴퓨팅"
date: "2026-08-25T13:00:00+09:00"
tags:
  - "notes-security"
weight: 19
extra:
  question_no: "19"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "하드웨어 신뢰 실행 환경(TEE / Enclave / CVM), 원격 증명(Remote Attestation / RFC 9334 RATS), TCB 축소 및 PCIe IDE"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Confidential Computing (기밀 컴퓨팅)**: 하드웨어 TEE를 통해 메모리를 실시간 암호화하여 연산 중인 데이터(Data in Use)의 기밀성과 무결성을 보장하는 기술.
- **TEE (Trusted Execution Environment)**: 하이퍼바이저나 루트 관리자조차 내부 메모리를 열람하거나 변조할 수 없도록 격리된 하드웨어 보안 영역.

</details>

- 정의/개념: CPU/GPU 하드웨어 메모리 암호화 엔진(TEE)과 원격 증명을 결합하여 **호스트 OS조차 접근 불가능하도록 '사용 중 데이터'를 실시간 보호하는 기밀 연산 기술**
- 배경/필요성: 스토리지와 네트워크 암호화에도 불구하고 **메모리 로드 시 평문 노출로 인한 클라우드 관리자 침해 위협 및 메모리 덤프 도청 방어 불가**

#### 한줄 요약
- 하드웨어 TEE 메모리 암호화와 원격 증명을 통해 연산 중인 데이터의 기밀성을 완벽히 보호한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Remote Attestation (원격 증명, RFC 9334 RATS)**: TEE 내부에서 실행 중인 펌웨어와 코드의 해시 측정값을 하드웨어 개인키로 서명하여 외부 검증자에게 진본성을 증명하는 절차.
- **TCB (Trusted Computing Base)**: 시스템의 보안성을 보장하기 위해 반드시 신뢰해야만 하는 최소한의 하드웨어/소프트웨어 구성요소 집합.

</details>

- **데이터 사용 중(Data-in-Use) 하드웨어 암호화**: 메모리 버스 상의 모든 데이터를 **하드웨어 내장 AES 엔진으로 실시간 암복호화**
- **TCB(신뢰 컴퓨팅 기반)의 극적 축소**: 클라우드 호스트 OS, **하이퍼바이저, 루트 관리자를 잠재적 공격자로 간주하여 신뢰 영역에서 제외**
- **원격 증명(Remote Attestation) 기반 무결성 보증**: 칩셋 고유 키로 서명된 **바이너리 측정값(PCR)을 검증하여 백도어 변조 여부 완벽 판정**

#### 한줄 요약
- Data-in-Use 암호화, TCB 극소화, 원격 증명(Attestation) 기반 무결성 보증을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **KBS (Key Broker Service)**: 원격 증명을 통과한 정상 TEE 인스턴스에 대해서만 데이터 복호화 키를 안전하게 주입(Key Provisioning)하는 신뢰 키 금고.

</details>

```text
[기밀 컴퓨팅 TEE 및 원격 증명(RATS) 아키텍처]
|-- Untrusted Cloud Host (호스트 OS, 하이퍼바이저 관리자 침해 영역)
`-- Hardware TEE (Intel TDX / AMD SEV-SNP / NVIDIA H100)
    |-- Protected Workload (기밀 가상머신 CVM / Enclave)
    `-- Memory Encryption Engine (AES-128/256 하드웨어 메모리 실시간 암호화)
`-- Remote Attestation Verifier (RFC 9334 RATS: 칩셋 제조사 서명 및 해시 검증)
`-- Key Broker Service (KBS: 증명 통과 시 TEE 전용으로 Key Wrapping하여 주입)
```

선의 의미: 신뢰할 수 없는 클라우드 호스트 상의 TEE가 하드웨어 측정값을 검증기에 제출하여 승인을 받고 KBS로부터 안전하게 암호키를 주입받아 연산을 개시하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **하드웨어 TEE** | CPU 칩셋 내부에서 **독립된 메모리 암호화 키를 관리하고 물리적 접근 차단** | TDX / SEV-SNP |
| **보호 워크로드** | TEE 엔클레이브 또는 **기밀 가상머신(CVM) 내부에서 구동되는 민감 응용 프로그램** | Protected App |
| **원격 증명 검증기** | TEE 증거의 제조사 서명 유효성 및 **코드 해시(Measurement) 정책 심사** | RFC 9334 RATS |
| **키 브로커 (KBS)** | 증명 검증을 통과한 유효한 TEE에 대해서만 **암호화된 세션키(Wrapped Key) 주입** | Key Provisioning |
| **PCIe IDE 가속기** | CPU와 외장 GPU(NVIDIA H100) 간 **PCIe 버스 전송 구간의 링크 암호화 집행** | PCIe 5.0 IDE |

#### 한줄 요약
- 하드웨어 TEE, 보호 워크로드, 원격 증명 검증기, 키 브로커(KBS), PCIe IDE 가속기가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Key Wrapping (RFC 3394)**: 키 브로커가 마스터 대칭키를 TEE에 전송할 때 오직 해당 TEE의 임시 개인키로만 풀 수 있도록 공개키로 캡슐화하여 배포하는 기법.

</details>

```text
TEE 부팅 측정, Attestation 리포트 생성, 검증 및 키 주입 파이프라인
        │
   1. [하드웨어 부팅 측정] 클라우드 상에서 TEE(CVM) 초기화 ➔ 하드웨어가 바이너리의 해시 측정값(PCR) 산출
        │
   2. [Attestation 리포트 생성] TEE가 칩셋 내부 고유 비밀키로 서명된 원격 증명 리포트 생성
        │
   3. [독립 검증기 신뢰 심사] 외부 검증기(Verifier)가 CPU 제조사 체인 및 코드 측정값의 불변 무결성 검증
        │
   4. [EAT 증명 토큰 발급] 검증 성공 시 서명된 EAT 토큰을 발급하여 키 브로커(KBS)로 전달
        │
   ▼
5. [Key Wrapping 주입 및 연산] KBS가 TEE의 임시 공개키로 키를 래핑하여 주입 ➔ TEE 내에서 안전한 연산 완수
```

#### 한줄 요약
- 하드웨어 측정값 산출 → Attestation 서명 리포트 생성 → 독립 검증기 심사 → EAT 토큰 발급 → Key Wrapping 주입 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **애플리케이션 엔클레이브 (SGX)** vs **기밀 가상머신 (SEV/TDX)** vs **가속기 TEE (H100)**.

</details>

| 비교 항목 | 애플리케이션 엔클레이브 (Intel SGX) | 기밀 가상머신 (AMD SEV-SNP / Intel TDX) | 가속기 TEE (NVIDIA H100 / Hopper) |
|:---|:---|:---|:---|
| **격리 단위** | **특정 프로세스/함수 단위 (Process)** | **가상머신 전체 (Guest OS + VM 전체)** | **외장 GPU 가속기 및 고대역 메모리(HBM)**|
| **TCB(신뢰 범위) 크기**| **최소 (애플리케이션 코드만 포함)** | 중간 (Guest OS 커널 포함으로 다소 큼) | 가속기 펌웨어 및 드라이버 포함 |
| **코드 리팩토링 필요성**| **필수 (전용 SDK로 코드 분리 개발)** | **불필요 (Lift & Shift 무수정 이전)** | 최소 수정 (CUDA 기밀 컴퓨팅 모드) |
| **주요 장점** | 가장 강력한 물리적 공격 표면 최소화 | 기존 클라우드 VM을 그대로 마이그레이션 | **초거대 LLM 모델 훈련/추론 실시간 가속** |
| **주요 적용 사례** | **암호화 키 관리(HSM), 생체 서명 인증** | **엔터프라이즈 ERP/DB 클라우드 이전** | **의료 AI 모델 학습, 기밀 LLM 서비스** |

#### 한줄 요약
- 엔클레이브는 최소 TCB 최고 보안, 기밀 VM은 무수정 클라우드 이전, 가속기 TEE는 대규모 AI 모델 기밀 처리에 최적화된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Side-Channel Timing Attack**: 공유 CPU 캐시의 접근 시간차(Flush+Reload)를 측정하여 TEE 내부의 암호키를 역산하는 하드웨어 취약점 공격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 공유 CPU 캐시 접근 시간차를 악용한 **부채널 타이밍(Side-Channel) 암호키 유출** | **`Constant-Time 알고리즘, 캐시 파티셔닝(Intel CAT) 및 주기적 플러시`** | 연산 시간 및 캐시 적중률 의존성 제거로 부채널 누설 차단 |
| CPU와 외장 GPU 간 PCIe 버스 라인을 물리적으로 도청하는 **버스 스누핑(Bus Snooping)** | **`PCIe 5.0 IDE(Integrity and Data Encryption) 표준 하드웨어 링크 암호화`** 강제 | 마더보드 물리 버스 전송 중 데이터 노출 및 변조 완벽 방어 |
| 이종 CSP 간 TEE 증명 프로토콜 파편화로 인한 **원격 증명 연동 실패 및 벤더 종속** | **`IETF RFC 9334 RATS 표준 아키텍처 및 공통 EAT 토큰`** 채택 | 멀티 클라우드 환경에서의 표준화된 원격 증명 상호운용성 확보 |
| TEE 내부 메모리 암복호화 연산 오버헤드로 인한 시스템 성능 저하 | **`하드웨어 전용 AES-XTS 가속 엔진` 및 대규모 페이지(Huge Page) 최적화** | 연산 오버헤드 5% 이내 최소화 및 라인레이트 처리율 달성 |

#### 한줄 요약
- Constant-Time 코딩으로 부채널을 막고, PCIe IDE로 버스를 암호화하며, RFC 9334 RATS로 상호운용성을 보장한다.

## Ⅶ. 결론

- 클라우드 컴퓨팅 환경에서 '저장 중', '전송 중' 보안에 이어 마지막 난제였던 '사용 중' 데이터 보안을 완성하는 **기밀 컴퓨팅(Confidential Computing) 아키텍처는 제로 트러스트 인프라의 필수 요건**이며, 실무 구현 시 **요구 보안 수준에 따른 엔클레이브와 CVM의 전략적 선택, RFC 9334 RATS 표준 원격 증명 파이프라인 구축, GPU 가속기 TEE 및 PCIe IDE 링크 암호화 결합**을 통합 추진하여 완벽한 엔드투엔드 데이터 보호 환경 완성

#### 한줄 요약
- 기밀 컴퓨팅은 하드웨어 TEE 메모리 암호화와 RFC 9334 원격 증명 및 PCIe IDE 링크 보안을 결합하여 완벽한 사용 중 데이터 보호를 실현하는 인프라 보안 기술이다.