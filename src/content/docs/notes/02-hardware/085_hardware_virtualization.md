---
sidebar:
  order: 85
  label: "085. 하드웨어 가상화: VT-x•AMD-V"
  badge:
    text: "기출 • 70%"
    variant: note
title: "하드웨어 가상화: VT-x•AMD-V (Hardware Virtualization)"
date: "2026-08-17T09:25:00+09:00"
tags:
  - "notes-hardware"
weight: 85
extra:
  question_no: "085"
  source_status: "기출"
  source_history: "137회"
  priority: 70
  priority_note: "VMX 모드 전환과 2단계 중첩 페이징(EPT)의 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **하드웨어 지원 가상화(Hardware-Assisted Virtualization)**: CPU 명령어 세트 수준에서 가상화 전용 실행 모드(Intel VT-x / AMD-V)를 지원하여 게스트 OS를 수정 없이 물리 CPU에서 직접 실행하는 기술.
- **EPT(Extended Page Tables)**: 게스트 물리 주소(GPA)를 호스트 물리 주소(HPA)로 CPU 하드웨어 MMU가 2단계로 직접 변환해 주는 중첩 페이징 기술(AMD는 NPT).

</details>

- 정의/개념: CPU 하드웨어 전용 가상화 모드(VMX)와 **2단계 중첩 페이징(EPT/NPT)** 을 지원하여 게스트 OS를 무수정 네이티브 속도로 구동하는 가상화 기술
- 배경/필요성: 순수 소프트웨어 바이너리 변환(BT) 시 발생하는 **극심한 CPU 에뮬레이션 오버헤드 및 x86 특권 명령 트랩 한계** 직면

#### 한줄 요약
- CPU 칩셋이 직접 가상 머신 전용 모드와 2단계 메모리 번역기를 제공하여 소프트웨어 손실 없이 고속 가상화를 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **VMX Root / Non-Root 모드**: 하이퍼바이저가 제어권을 갖는 특권 영역(Root)과 게스트 OS 및 앱이 격리 구동되는 비특권 가상화 영역(Non-Root).
- **VMCS(Virtual Machine Control Structure)**: 게스트/호스트 레지스터 상태와 VM-Exit 트랩 조건을 하드웨어적으로 저장하는 4KB 물리 메모리 블록(AMD는 VMCB).

</details>

- 하이퍼바이저와 게스트 VM 간의 완벽한 물리적 보안 격리를 지원하는 **VMX Root / Non-Root 모드**
- 레지스터 문맥 저장 및 VM 전환 조건을 하드웨어가 직접 추적하는 **VMCS 하드웨어 제어 블록**
- 섀도 페이지 테이블 소프트웨어 오버헤드를 제거하는 **EPT/NPT 2단계 중첩 페이징**

#### 한줄 요약
- 하이퍼바이저는 Root 모드, 가상 머신은 Non-Root 모드로 돌리고, VMCS와 EPT가 상태 전환과 메모리 번역을 하드웨어로 처리한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **VM-Exit & VM-Entry**: 하이퍼바이저에서 게스트로 진입하는 동작(VM-Entry)과 게스트의 특권 명령 실행 시 하이퍼바이저로 트랩되는 동작(VM-Exit).
- **VT-d(Intel Virtualization Technology for Directed I/O)**: PCIe 디바이스(NIC, GPU)를 게스트 VM에 1:1 패스스루 직결할 때 하드웨어 DMA 주소 변환 및 인터럽트 격리를 제공하는 기술.

</details>

```text
┌─────────────────────────────────────────────────────────────┐
│ 하드웨어 지원 가상화 아키텍처 및 제어 구조                  │
│                                                             │
│  [ 게스트 VM 계층 (VMX Non-Root Mode : Guest OS + Apps) ]    │
│  └──────────────────────────┬───────────────────────────────┘│
│                             │ (직접 CPU 명령어 실행 / EPT 접근)
│  ┌──────────────────────────▼───────────────────────────────┐│
│  │ CPU 하드웨어 가상화 엔진 (Intel VT-x / AMD-V)             ││
│  │  ├─ VMCS 하드웨어 제어 블록 (Guest State / Host State)   ││
│  │  ├─ EPT / NPT 하드웨어 MMU (GPA ──► HPA 2단계 주소 변환) ││
│  │  └─ VT-d / AMD-Vi IOMMU (PCIe 패스스루 DMA / IRQ 리매핑) ││
│  └──────────────────────────┬───────────────────────────────┘│
│                             │ (특권 명령 시 VM-Exit 하드웨어 트랩)
│  ┌──────────────────────────▼───────────────────────────────┐│
│  │ 하이퍼바이저 (VMX Root Mode : KVM, VMware ESXi, Xen)      ││
│  └──────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

선의 의미: 게스트 OS는 Non-Root 모드에서 직접 실행되다 특권 명령 실행 시 VM-Exit를 통해 Root 모드 하이퍼바이저로 트랩됨

| 구성요소 | 책임 |
|:---|:---|
| 게스트 VM (Non-Root) | 수정되지 않은 표준 OS(Windows/Linux)가 독립 가상 머신 환경에서 직접 CPU 실행 |
| 하이퍼바이저 (Root) | VMX Root 모드에서 가상 CPU(vCPU)를 스케줄링하고 시스템 전체 자원 통제 |
| VMCS 제어 블록 | vCPU 레지스터 상태, 호스트 레지스터, 인터럽트 제어, VM-Exit 발생 원인 기록 |
| EPT / NPT MMU | 게스트 물리 주소(GPA)를 호스트 물리 주소(HPA)로 하드웨어가 2단계 고속 번역 |
| VT-d / AMD-Vi | 고성능 NIC/GPU 장치를 VM에 직결(Passthrough)할 때 DMA 메모리 보호 및 IRQ 전달 |

#### 한줄 요약
- 게스트 VM, 하이퍼바이저, VMCS 제어 블록, EPT 2단계 MMU, VT-d I/O 가속기가 통합 가상화 엔진을 구성한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **GPA to HPA 변환**: 게스트 OS가 인식하는 물리 주소(Guest Physical Address)를 실제 호스트 머신의 물리 메모리 주소(Host Physical Address)로 매핑하는 과정.

</details>

```text
하이퍼바이저의 가상 머신(vCPU) 실행 요청
      │
      ▼
1. VMCS 설정: 하이퍼바이저가 VMCS에 게스트 상태 및 VM-Exit 조건 구성
      │
      ▼
2. VM-Entry 실행: VMLAUNCH/VMRESUME 명령으로 VMX Non-Root 모드 진입
      │
      ▼
3. 게스트 직접 연산: 일반 CPU 연산 및 EPT 기반 메모리 접근을 베어메탈 속도로 수행
      │
      ▼
4. VM-Exit 트랩 발생: 게스트가 특권 레지스터(CR3) 조작 또는 HLT 명령 실행 시 CPU가 자동 트랩
      │
      ▼
5. 하이퍼바이저 에뮬레이션 처리 후 VMCS 갱신 및 VM-Entry 재진입
```

**동작 원리**

1. **초기화**: 하이퍼바이저가 VMCS 메모리에 게스트의 초기 레지스터 상태와 EPT 루트 포인터를 기록
2. **제어권 이양**: `VMRESUME` 명령어로 CPU를 Non-Root 모드로 전환하여 게스트 OS 부팅 시작
3. **직접 실행**: 사용자 애플리케이션 및 일반 커널 연산은 에뮬레이션 없이 물리 CPU 코어에서 직접 연산
4. **하드웨어 트랩**: I/O 포트 접근이나 특권 레지스터 조작 발생 시 CPU가 상태를 VMCS에 저장하고 Root 모드로 탈출
5. **대행 및 복귀**: 하이퍼바이저가 해당 요청을 소프트웨어로 대행 처리한 후 다시 VM-Entry로 게스트 복귀

#### 한줄 요약
- VMCS 설정 → VM-Entry 진입 → 게스트 직접 실행(EPT) → 특권 명령 시 VM-Exit 트랩 → 에뮬레이션 후 복귀 순으로 동작한다.

## Ⅴ. 종류 및 비교

| CPU 가상화 기술 | 하드웨어 지원 가상화 (VT-x) | 바이너리 변환 전가상화 | 준가상화 (Para-Virt) | OS 컨테이너 가상화 |
|:---|:---|:---|:---|:---|
| 적용 기준 | 현대 클라우드/엔터프라이즈 가상화 | 레거시 하드웨어 전가상화 | 고성능 전용 리눅스 환경 | 경량 마이크로서비스 배포 환경 |
| 핵심 특징 | CPU VMX 모드 및 EPT 하드웨어 가속 | 소프트웨어가 특권 명령 실시간 패치 | 게스트 OS 커널 수정(Hypercall) | 단일 호스트 커널 공유(cgroups/ns) |
| 한계 | 빈번한 VM-Exit 발생 시 전환 오버헤드 | 소프트웨어 바이너리 변환 오버헤드 극심 | Windows 등 상용 비공개 OS 수정 불가 | 호스트 커널 공유로 인한 보안 격리 취약 |

#### 한줄 요약
- 현대 클라우드는 하드웨어 가상화(VT-x), 레거시는 바이너리 변환, 커널 수정은 준가상화, 경량 배포는 컨테이너를 쓴다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **SR-IOV(Single Root I/O Virtualization)**: 단일 물리 PCIe 장치를 다수의 독립된 가상 기능(VF)으로 분할하여 VM에 하이퍼바이저 경유 없이 직결하는 기술.
- **휴지 페이지(Huge Pages, 2MB/1GB)**: 기본 4KB 대신 대용량 페이지를 사용하여 EPT 2단계 주소 변환 시 TLB 캐시 미스(Miss)를 대폭 줄이는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 빈번한 I/O 요청 시 **과도한 VM-Exit 발생으로 CPU 성능 저하** | **SR-IOV** 장치 직결 및 **Virtio vHost-Net 폴링 드라이버** 적용 | VM-Exit 오버헤드 제로화 및 베어메탈급 네트워크 성능 달성 |
| EPT 2단계 주소 변환 오버헤드로 인한 **TLB 미스 및 메모리 지연** | **대용량 페이지(Huge Pages: 2MB/1GB)** 메모리 매핑 적용 | 페이지 테이블 계층 축소 및 TLB 히트율 95% 이상 확보 |
| vCPU와 물리 메모리가 서로 다른 노드에 배치되는 **NUMA 원격 접근 지연** | 하이퍼바이저 상에서 **vCPU-메모리 간 NUMA 노드 고정(Pinning)** | 크로스 소켓 인터커넥트 병목 원천 차단 |
| 가상화 환경에서의 CPU 취약점을 악용한 **사이드채널 공격(Spectre/L1TF)** | **Intel eIBRS 하드웨어 완화책** 및 코어 간 vCPU 스케줄링 격리 | 테넌트 간 메모리 기밀 정보 탈취 완벽 방어 |

#### 한줄 요약
- SR-IOV로 VM-Exit를 없애고, Huge Pages로 EPT 지연을 잡으며, NUMA 핀닝으로 메모리 병목을 해소한다.

## Ⅶ. 결론

- 클라우드 컴퓨팅 및 데이터센터 가상화 구축 시 **Intel VT-x / AMD-V 하드웨어 가상화와 SR-IOV 네트워크 가속** 표준 채택 필수

#### 한줄 요약
- VMX 모드와 EPT 하드웨어 가속, IOMMU 장치 직결을 융합하여 네이티브 머신 대비 99% 이상의 고성능 가상화를 실현해야 한다.
