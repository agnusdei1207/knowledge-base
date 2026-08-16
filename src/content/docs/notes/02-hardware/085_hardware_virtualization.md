---
sidebar:
  order: 85
  label: "085. 하드웨어 가상화: VT-x•AMD-V (Hardware Virtualization)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "하드웨어 가상화: VT-x•AMD-V (Hardware Virtualization)"
date: "2026-08-13T12:21:04+09:00"
tags:
  - "notes-hardware"
weight: 85
extra:
  question_no: "085"
  source_status: "기출"
  source_history: "137회"
  priority: 70
  priority_note: "VM 전환•2단계 주소 변환 병목"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **하드웨어 가상화(Hardware-Assisted Virtualization)**: CPU 하드웨어 차원에서 가상화 전용 실행 모드(Root vs Non-Root)와 하이퍼바이저 지원 명령어를 내장하여 게스트 OS를 직접 수행하는 가상화 기술.
- **하이퍼바이저(Hypervisor/VMM)**: 하드웨어와 가상 머신(VM) 사이에서 물리 자원을 추상화하고 VM 간 격리 및 스케줄링을 통제하는 가상화 제어 미들웨어.
- **VM(Virtual Machine)**: 하이퍼바이저에 의해 물리 자원을 할당받아 독립된 게스트 OS를 구동하는 가상 컴퓨터 환경.

</details>

- 정의/개념: CPU의 가상화 명령어(VT-x/AMD-V) 및 하드웨어 매핑 구조(VMCS/VMCB, EPT/NPT)를 통해 게스트 OS 명령을 전용 실행시키는 **하드웨어 가상화**
- 배경/필요성: 소프트웨어 명령 변환은 **특권 명령·페이지 변환 오버헤드 증가**

#### 한줄 요약

- 하드웨어 가상화는 게스트의 일반 명령을 직접 실행하고 통제가 필요한 사건에서만 하이퍼바이저로 전환한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **VT-x / AMD-V**: Intel(VT-x) 및 AMD(AMD-V) x86 CPU 하드웨어 가상화 전용 명령어 집합.
- **VMCS/VMCB(Virtual Machine Control Structure/Block)**: VMM 상태, 게스트 섀도 레지스터 상태 및 VM Exit 조건 메타데이터를 저장하는 하드웨어 메모리 데이터 구조.
- **EPT/NPT(Extended/Nested Page Tables)**: GVA에서 GPA를 거쳐 HPA로 변환하는 2단계 주소 변환을 하드웨어가 지원하는 기술.

</details>

- 하이퍼바이저(VMX Root Operation)와 게스트(VMX Non-Root Operation)의 물리 실행 모드 수평 분리
- **VMCS/VMCB** 제어 구조를 통한 VM 진입·이탈 상태 관리
- **EPT/NPT** 기반 2단계 주소 변환으로 섀도 페이지 테이블 부담 감소

#### 한줄 요약

- VM 전환과 2단계 주소 변환 빈도가 높을수록 오버헤드가 증가한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **IOMMU(Input-Output MMU)**: 가상 머신(VM) 및 PCI 장치 간의 DMA(Direct Memory Access) 주소 변환과 장치 가상화 보안 격리를 담당하는 하드웨어 (Intel VT-d / AMD-Vi).
- **vCPU(Virtual CPU)**: 하이퍼바이저가 물리 CPU 코어에 대한 연산 시간을 스케줄링하여 VM에 할당하는 가상 프로세서 단원.

- **VMX 루트/비루트 모드(VMX Root / Non-Root Mode)**: 인텔 VT-x에서 하이퍼바이저가 실행되는 특권 모드(Root)와 게스트 OS가 직접 실행되는 격리 모드(Non-Root).
- **입출력 가상화 기술(VT-d / AMD-Vi)**: 게스트 가상머신이 물리 PCIe 장치에 직접 DMA 접근할 수 있도록 I/O 주소를 변환·보호하는 하드웨어 IOMMU 기능.
</details>

```text
                         [EPT•NPT]
                              |
                              |
[게스트 VM] -- [CPU 가상화 확장] -- [하이퍼바이저 제어부] -- [가상 I/O•IOMMU]
```

선의 의미: 게스트 VM 요청이 CPU 가상화 확장(VT-x) 및 하이퍼바이저 제어부 상에서 EPT/NPT 주소 변환과 IOMMU 하드웨어 가상화 파이프라인으로 처리되는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| 게스트 VM | 미수정(Unmodified) OS 구동 및 하드웨어 직접 비특권 명령어 수행 |
| CPU 가상화 확장 | **VMX Root/Non-Root** 모드 제어 및 **VMCS/VMCB** 구조체 오프로드 |
| 하이퍼바이저 제어부 | **vCPU** 스케줄링, 물리 자원 분배 및 민감 명령 에러 핸들링 |
| EPT•NPT | 하드웨어 기반 GVA·GPA·HPA 2단계 페이지 변환 관장 |
| 가상 I/O•IOMMU | **VT-d/AMD-Vi** 기반 PCI 장치 직결(Passthrough) 및 DMA 격리 |

#### 한줄 요약

- 게스트 VM, CPU 가상화 확장, 하이퍼바이저 제어부와 메모리•장치 격리 구성의 구조이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **VM Entry**: 하이퍼바이저(Root)에서 게스트 OS(Non-Root)로 실행 제어권을 넘기는 하드웨어 상태 전환 동작 (VMLAUNCH/VMRESUME).
- **VM Exit**: 게스트 OS 실행 중 특권 명령(PRIV) 인가 또는 I/O 발생 시 하이퍼바이저(Root)로 제어권이 강제 트랩(Trap) 이행되는 현상.

</details>

```text
1. VM 제어 상태 적재
          │
          ▼
2. VM Entry•게스트 직접 실행
          │
          ▼
┌──────────── 게스트 실행 반복 ───────────┐
│ 3. EPT•NPT 주소 변환                    │
│          │                               │
│          ▼                               │
│   [민감 명령•I/O•예외 발생]             │
│       ┌──┴─────────┐                     │
│       │ 없음       │ 발생                │
│       │            ▼                     │
│       │     4. VM Exit•상태 저장         │
│       │            │                     │
│       │            ▼                     │
│       │     5. 하이퍼바이저 중재         │
│       │            │                     │
│       └────────────┴── VM Entry로 복귀   │
└──────────────────────────────────────────┘
```

### 동작 원리

1. VM 제어 상태 적재: 하이퍼바이저가 **VMCS/VMCB** 상에 게스트 레지스터 및 인터럽트 트랩 조건을 세팅.
2. VM Entry·게스트 직접 실행: **VM Entry**를 수행하여 VMX Non-Root 모드로 전환 후 일반 명령을 물리 CPU에서 직접(Direct Execution) 구동.
3. EPT·NPT 주소 변환: 메모리 접근 시 하드웨어 **EPT/NPT**가 GVA·GPA·HPA 주소 변환 수행.
4. VM Exit·상태 저장: 설정된 민감 사건 발생 시 **VM Exit**하고 제어 상태를 VMCS/VMCB에 기록.
5. 하이퍼바이저 중재: 하이퍼바이저가 특권 트랩 에뮬레이션 완결 후 다시 **VM Entry**를 인가하여 게스트 재개.

#### 한줄 요약

- 민감 명령 같은 통제 사건에서만 VM Exit하고 하이퍼바이저가 정책을 처리한 뒤 VM Entry로 재진입한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Binary Translation**: 하드웨어 지원이 없던 시절, 게스트 특권 명령을 동적으로 탐지하여 하이퍼바이저 안전 코드로 치환(BT)하던 소프트웨어 방식.

</details>

| 비교 항목 | 하드웨어 가상화 (VT-x / AMD-V) | 전가상화 BT (Binary Translation) | 반가상화 (Para-Virtualization) |
|:---|:---|:---|:---|
| 구현 방식 | **CPU HW 전용 명령어** (VMCS, EPT) | SW 동적 특권 명령어 패칭 및 감시 | 게스트 OS 커널 소스 코드 수정 (Hypercall) |
| 게스트 OS | 미수정(Unmodified) OS 적용 가능 | 미수정(Unmodified) OS 적용 가능 | 게스트 OS 코드 수정 필수 |
| 주요 오버헤드 | **VM Exit** 횟수 및 EPT TLB Miss | 동적 이진 변환 및 SW 섀도 페이지 테이블 | Hypercall 소프트웨어 호출 오버헤드 |

#### 한줄 요약

- 호스트와 같은 ISA의 게스트는 하드웨어 가상화, 다른 ISA의 게스트는 에뮬레이션과 이진 변환을 사용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **SR-IOV(Single Root I/O Virtualization)**: 단일 PCIe 가상화 장치를 복수의 Virtual Function(VF)으로 분할하여 VM에 직결 인가하는 하드웨어 통제.
- **Virtio**: 가상 I/O 장치 에뮬레이션 비용을 줄이기 위해 준가상화(Paravirtualized) ring-buffer 기반 드라이버 구조.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 빈번한 I/O 트랩에 따른 **VM Exit** 오버헤드 | **Virtio** 준가상 드라이버 및 **SR-IOV** 직결 | I/O 트랩 감소와 처리량 향상 |
| 2단계 주소 변환으로 인한 TLB Miss 증가 | **Huge Pages**와 VPID TLB 태깅 활성화 | 주소 변환과 TLB 무효화 부담 감소 |
| vCPU와 메모리 배치 불일치로 인한 NUMA 지연 | vCPU·메모리·장치의 NUMA 친화도 정렬 | 원격 메모리 접근 감소 |

> 사례: KVM/QEMU 하이퍼바이저 기반 **VT-x/EPT** 및 **SR-IOV** 수용 고성능 클라우드 VM 인프라 구축

#### 한줄 요약

- 인터럽트 병합과 준가상 장치로 VM Exit 빈도를 줄인다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **가상화 선택 기준(Virtualization Technology Selection Criteria)**: 게스트 OS 수정 가능성, I/O 스루풋 타깃 및 HW CPU 지원 여부에 따른 체계.

</details>

- 동일 ISA 게스트는 **하드웨어 가상화**, I/O 협력은 **준가상화**, 다른 ISA는 **에뮬레이션** 선택

#### 한줄 요약

- 동일 ISA 게스트는 하드웨어 가상화, 다른 ISA는 에뮬레이션을 선택한다.
