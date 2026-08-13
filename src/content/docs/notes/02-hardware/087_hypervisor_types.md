---
sidebar:
  order: 87
  label: "087. 서버 가상화: Type 1•Type 2 하이퍼바이저 (Hypervisor Types)"
  badge:
    text: "기출 • 85%"
    variant: note
title: "서버 가상화: Type 1•Type 2 하이퍼바이저 (Hypervisor Types)"
date: "2026-08-13T12:21:04+09:00"
tags:
  - "notes-hardware"
weight: 87
extra:
  question_no: "087"
  source_status: "기출"
  source_history: "128회, 131회, 132회, 137회"
  priority: 85
  priority_note: "네 회 반복 출제된 서버 가상화 핵심 비교"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **하이퍼바이저(Hypervisor/VMM)**: 단일 물리 하드웨어 상에서 복수의 VM(Virtual Machine)들을 구동하기 위해 CPU, 메모리, 입출력 자원을 동적 추상화/스케줄링하는 하드웨어/소프트웨어 레이어.
- **Type 1 (Bare-Metal)**: 호스트 OS 없이 물리 하드웨어 직상(Bare-Metal)에 직접 탑재되어 하드웨어를 직접 통제하는 하이퍼바이저.
- **Type 2 (Hosted)**: 윈도우/리눅스 등 기존 호스트 OS 상의 애플리케이션 형태로 탑재되어 호스트 OS 드라이버를 거쳐 구동되는 하이퍼바이저.

</details>

- 정의/개념: 서버 하드웨어 상의 실행 레이어 위치(Bare-Metal vs Hosted) 및 호스트 OS 종속성 유무에 따른 하이퍼바이저 분류 체계인 **Type 1 vs Type 2**
- 배경/필요성: 상시 서버 운영과 개발 PC는 **성능·장애 경계·드라이버 요구가 상이**

#### 한줄 요약

- 하이퍼바이저의 실행 위치에 따라 Type 1과 Type 2를 구분한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Bare-Metal 실행**: 호스트 OS 개입 없이 물리 CPU 커널 모드(VMX Root Operation)에서 하드웨어를 직결 제어하는 구조.
- **Hosted 실행**: 호스트 OS 상의 한 개 유저 프로세스 형태로 실행되어 입출력 트랜잭션을 호스트 OS 커널 드라이버에 위임하는 구조.

</details>

- 하드웨어 자원을 직접 중재하는 **Type 1 (Bare-Metal)**
- 호스트 OS의 드라이버와 사용자 환경을 재사용하는 **Type 2 (Hosted)**
- 상시 서버 운영(Type 1)과 개발·시험 환경(Type 2)의 장애 경계 구분

#### 한줄 요약

- 직접 자원 중재와 호스트 OS 재사용이라는 배치 차이가 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Guest VM**: 하이퍼바이저에 의해 할당된 vCPU, vRAM 상에서 독립적으로 구동되는 가상 머신.
- **Host OS**: Type 2 환경에서 물리 하드웨어를 구동하고 하이퍼바이저를 애플리케이션으로 포용하는 메인 OS.

</details>

```text
          [게스트 VM]
               |
         [하이퍼바이저 제어부]
           /          \
 Type 1 직접          Type 2 매개
       /                \
[물리 하드웨어] ----- [호스트 OS]
```

선의 의미: Type 1은 하이퍼바이저 제어부가 물리 하드웨어에 직결되고, Type 2는 중간에 호스트 OS 레이어를 거쳐 물리 하드웨어를 오프로드하는 계층 구조.

| 구성요소 | 책임 |
|:---|:---|
| 물리 하드웨어 | 물리 CPU(VT-x/AMD-V), DRAM 메모리 및 **IOMMU** 입출력 소자 전송 |
| 호스트 OS | Type 2 환경 상에서 하드웨어 장치 드라이버 및 호스트 커널 스케줄링 |
| 하이퍼바이저 제어부 | **vCPU** 스케줄링, EPT/NPT 페이지 테이블 관리 및 VM 간 보안 격리 |
| 게스트 VM | 미수정 또는 수정된 독립 게스트 OS 커널 및 유저 애플리케이션 수용 |

#### 한줄 요약

- 하이퍼바이저 제어부가 물리 하드웨어에 직접 배치되거나 호스트 OS를 매개하는 구조를 구분한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **가상 I/O 패스**: 게스트 VM의 입출력 요청이 물리 하드웨어 장치로 도달하는 트랜잭션 수송 경로.

</details>

```text
[게스트 가상 I/O 디스크립터]
              │
              ▼
1. 가상 장치 요청 해석
              │
              ▼
2. I/O 실행 경로 선택
       ┌──────┴────────┐
       │ Type 1        │ Type 2
       ▼               ▼
[하이퍼바이저 드라이버] [호스트 시스템 호출]
       │               │
       │        3. 호스트 드라이버 변환
       │               │
       └───────┬───────┘
               ▼
4. 물리 I/O 실행
               │
               ▼
      [가상 I/O 완료 반환]
```

### 동작 원리

1. **가상 장치 요청 해석**: **게스트 VM**의 입출력 TLP/블록 요청 인가 및 가상 장치 제어부 수용.
2. **I/O 실행 경로 선택**: **Type 1**의 경우 하이퍼바이저 직접 드라이버 전송, **Type 2**의 경우 **호스트 OS System Call** 전송 분기.
3. **호스트 드라이버 변환**: Type 2 경로에서 호스트 시스템 호출을 물리 장치 요청으로 변환.
4. **물리 I/O 실행**: 선택된 드라이버 경로로 물리 장치 I/O 수행.

#### 한줄 요약

- Type 1 하이퍼바이저는 자원을 직접 중재하고, Type 2 하이퍼바이저는 호스트 OS 장치 계층을 추가로 거쳐 I/O를 수행한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **VMM 오버헤드**: 하이퍼바이저 층을 경유함으로 인해 발생하는 CPU/메모리/I/O 자원 손실 비율.

</details>

| 비교 항목 | Type 1 (Bare-Metal Hypervisor) | Type 2 (Hosted Hypervisor) |
|:---|:---|:---|
| 아키텍처 위치 | 물리 하드웨어 직상 (Bare-Metal 탑재) | 호스트 OS 상의 애플리케이션 소프트웨어 형태 |
| 주요 대표 제품 | VMware ESXi, Xen, Microsoft Hyper-V, KVM | VMware Workstation, Oracle VirtualBox, QEMU |
| 성능 및 오버헤드 | 관리 계층이 짧고 자원 통제가 직접적 | 호스트 OS 스케줄링·I/O 경유 비용 추가 |
| 하드웨어 호환성 | 검증된 서버 장치·드라이버 중심 | 호스트 OS가 지원하는 장치 활용 |
| 장애 파급성 | 하이퍼바이저·관리 도메인 장애가 전체에 영향 | **호스트 OS 장애** 시 모든 게스트에 영향 |

#### 한줄 요약

- 베어메탈은 상시 운영, 호스티드는 개발•시험 조건에 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **vCPU Overcommit**: 물리 CPU 코어 수 대비 초과된 가상 vCPU를 배정하여 활용률을 극대화하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| **Type 2** 호스트 OS 장애 시 모든 VM 중단 | 상시 운영 서버에 **Type 1**과 관리면 이중화 적용 | 호스트 데스크톱 장애 경계 제거 |
| 과도한 **vCPU Overcommit**으로 CPU Ready 지연 | 워크로드별 Ready Time 측정과 할당 상한 설정 | 게스트 반응 지연 억제 |
| 가상 I/O 처리 시 호스트 CPU 자원 소모 | **SR-IOV** 또는 Virtio 가속 경로 적용 | I/O 중재와 복사 오버헤드 감소 |

> 사례: 클라우드 인프라 상의 **Type 1 하이퍼바이저(KVM)** 구축 및 **SR-IOV** 수용

#### 한줄 요약

- Type 1의 관리면을 최소화하고 Type 2의 호스트 자원을 통제한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **하이퍼바이저 선택 기준(Hypervisor Type Selection Criteria)**: 운영 환경, 성능·장애 경계와 드라이버 요구에 따른 체계.

</details>

- **하이퍼바이저 선택 기준**에 따라 기업 데이터센터 및 클라우드는 **Type 1**, 개인 개발/테스트 장비는 **Type 2** 채택

#### 한줄 요약

- 상시 서버 운영은 Type 1, 개인 개발·시험은 Type 2를 선택한다.
