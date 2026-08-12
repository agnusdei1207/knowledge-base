---
sidebar:
  order: 18
  label: "018. 가상화: Type 1•Type 2 하이퍼바이저 (Virtualization•Hypervisor)"
  badge:
    text: "기출 • 85%"
    variant: note
title: "가상화: Type 1•Type 2 하이퍼바이저 (Virtualization•Hypervisor)"
date: "2026-08-06T23:27:50+09:00"
tags: [notes-software]
weight: 18
extra:
  question_no: "018"
  source_status: "기출"
  source_history: "128회, 131회, 132회, 137회"
  priority: 85
  priority_note: "4회 반복, 하이퍼바이저 구조•선택 핵심"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Hypervisor (VMM, Virtual Machine Monitor)**: 물리 하드웨어 자원 위에 위치하여 하드웨어를 추상화하고 여러 개의 게스트 OS(VM)가 개별 독립 자원으로 구동될 수 있도록 동적 자원 배분 및 스케줄링을 중재하는 소프트웨어 레이어.
- **Type 1 (Bare-Metal) Hypervisor**: 물리 하드웨어(Bare-Metal) 바로 위에 직접 설치되어 중간 Host OS 없이 최고 수준의 성능과 격리성을 제공하는 하이퍼바이저.
- **Type 2 (Hosted) Hypervisor**: 기존 Host OS(Windows, Linux 등) 위에서 응용 프로그램 형태로 구동되는 하이퍼바이저.

</details>

- 정의/개념: 단일 물리 하드웨어 자원을 추상화(Abstraction)하여 복수의 격리된 가상머신(Virtual Machine) 환경을 제공하는 커널 엔진인 **Hypervisor(VMM) 및 Type 1/Type 2 구분 구조**
- 배경/필요성: 베어메탈 서버의 자원 유휴 소멸, 멀티테넌시(Multi-tenancy) 클라우드 인프라 구축 및 보안 격리성 보장 요구성

#### 한줄 요약

- 가상화로 물리 자원을 격리된 논리 실행 환경으로 추상화하는 것이 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **VM Exit / VM Entry**: 게스트 OS의 특권 명령어(Privileged Instruction) 실행 시 하드웨어에 의해 하이퍼바이저 트랩이 발동되어 하이퍼바이저로 전환(VM Exit)되거나 다시 게스트로 복귀(VM Entry)하는 동작.
- **Hardware-Assisted Virtualization**: Intel VT-x 및 AMD-V 기술을 적용하여 특권 명령어 가상화 트랩 및 주소 변환(EPT/NPT)을 하드웨어 레벨에서 직접 고속 지원하는 기술.

</details>

- 게스트 OS 간 완벽한 자원 격리(Fault & Security Isolation)
- **Intel VT-x / AMD-V** 하드웨어 가상화 지원 및 **EPT(Extended Page Table)** 주소 변환
- **Type 1 (고성능/고격리)** vs **Type 2 (개발/편의성)** 간 실행 레이어 및 문맥 전환 오버헤드 차이

#### 한줄 요약

- 직접 실행과 VM Exit•VM Entry 전환 기반 자원 중재가 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **vCPU (Virtual CPU)**: 게스트 OS에게 할당된 논리적 CPU 코어로, 하이퍼바이저의 스케줄러에 의해 물리 CPU pCPU에 매핑 디스패치되는 단위.
- **EPT/NPT (Extended Page Tables / Nested Page Tables)**: 하드웨어가 2단계 주소 변환 (Guest Virtual $\to$ Guest Physical $\to$ Host Physical)을 직접 지원하여 MMU 가상화 오버헤드를 억제하는 기술.

</details>

```text
     Type 1 스택               Type 2 스택

    [가상머신 집합]              [가상머신 집합]
           |                            |
 [Type 1 하이퍼바이저]          [Type 2 하이퍼바이저]
           |                            |
    [물리 하드웨어]                 [호스트 OS]
                                        |
                                 [물리 하드웨어]
```

선의 의미: Type 1은 Bare-metal 하드웨어 직결 레이어인 반면, Type 2는 Host OS 인터페이스를 거쳐 드라이버 I/O 및 시스템 콜을 우회 중재하는 아키텍처.

| 구분 항목 | Type 1 (Bare-Metal / Native) | Type 2 (Hosted) |
|:---|:---|:---|
| 구동 레이어 | **물리 하드웨어 위 직접 구동** (No Host OS) | **Host OS 위 응용 프로그램으로 구동** |
| 대표 솔루션 | **VMware ESXi, Xen, KVM, Microsoft Hyper-V** | **VMware Workstation, VirtualBox** |
| 오버헤드 / 성능 | 오버헤드 매우 낮음, 베어메탈 급 고성능 | Host OS 우회로 인한 오버헤드 큼 |
| 보안 / 안정성 | 매우 높음 (Host OS 취약점 영향 없음) | 상대적으로 낮음 (Host OS 패치/장애 파급) |

#### 한줄 요약

- Type 1 하이퍼바이저의 직접 배치와 Type 2 하이퍼바이저의 호스트 운영체제 경유 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Trap-and-Emulate**: 게스트 OS가 비특권 모드에서 Ring 0 특권 명령어를 실행할 때 하드웨어 예외를 유발(Trap)시켜 하이퍼바이저가 이를 가상화 모사(Emulate)해 주는 기본 동작.

</details>

```text
Type 1 제어 경로

[게스트 직접 실행] ──► [민감 명령 발생] ──► [VM Exit] ──► [Type 1 직접 중재] ──► [VM Entry] ──► [게스트 복귀]

Type 2 제어 경로

[게스트 직접 실행] ──► [민감 명령 발생] ──► [VM Exit] ──► [Type 2 호스트 경유] ──► [Host OS System Call] ──► [VM Entry]
```

### 동작 원리

1. **Guest Execution**: 일반 비민감 명령어는 물리 CPU 상에서 하드웨어 지원(**Intel VT-x**)으로 게스트가 직결 수행.
2. **VM Exit**: 특권 명령어(I/O, CR3 페이지 매핑 변경 등) 시 하드웨어 트랩발동 및 **VM Exit** 전환.
3. **Hypervisor Emulation**: Type 1은 하이퍼바이저가 물리 자원 직접 조율, Type 2는 **Host OS System Call** 호출 우회.
4. **VM Entry**: 상태 복원 후 **VM Entry**를 통해 게스트 OS로 제어권 넘김 재개.

#### 한줄 요약

- Type 1은 Type 1 직접 중재, Type 2는 Type 2 호스트 경유가 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **KVM (Kernel-based Virtual Machine)**: Linux 커널을 Type 1 하이퍼바이저 모듈로 직접 변환시키는 커널 기반 가상화 기술.

</details>

| 비교 항목 | Type 1 (Hyper-V, ESXi, KVM) | Type 2 (VirtualBox) | Container (Docker, LXC) |
|:---|:---|:---|:---|
| 가상화 대상 | 전체 하드웨어 (Full Hardware) | 전체 하드웨어 (Full Hardware) | **OS 커널 공유 (Process Isolation)** |
| 게스트 OS 필수 | **독립 게스트 OS 탑재 필수** | **독립 게스트 OS 탑재 필수** | 게스트 OS 없음 (Host Kernel 수용) |
| 부팅 속도 | 수십 초 ~ 수 분 | 수십 초 ~ 수 분 | **수초 이내 (밀리초 단위)** |
| 오버헤드 크기 | 소형 (~수 %) | 중형/대형 (~수십 %) | **극소 (하드웨어 오버헤드 제로)** |

#### 한줄 요약

- 운영 격리는 Type 1, 호스트 호환은 Type 2가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **SR-IOV (Single Root I/O Virtualization)**: 물리 NIC 장치를 논리 가상 기능(VF)으로 분할하여 VM이 하이퍼바이저 패킷 중재 없이 직접 I/O 바이패스(Pass-Through)하게 하는 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 가상화 I/O 스택 거침에 따른 네트워크/디스크 패킷 지연 | **SR-IOV** 및 **Device Pass-Through** 적용 | 하드웨어 바운더리 레벨 초저지연 I/O 보장 |
| 가상 메모리 변환 오버헤드로 인한 성능 저하 | **EPT (Extended Page Tables)** 하드웨어 주소 변환 적용 | MMU 가상화 지연 소멸 |
| 게스트 OS 간 무분별한 CPU/Memory 과도 할당 | **Oversubscription** 관리 및 cgroups/vCPU 쿼터 제한 | 물리 자원 낭비 및 스레싱 방지 |

> 사례: AWS EC2 **Nitro System (Type 1 전용 카드)** 및 KVM/OpenStack 대규모 엔터프라이즈 구동

#### 한줄 요약

- vCPU 준비 시간, 관리면, 상태 정합성 중심 운영이 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **가상화 알고리즘 선택 기준(Virtualization Selection Criteria)**: 워크로드 I/O 지연 민감도, 밀도, 격리 수준 및 운영 관리에 기반한 수립 체계.

</details>

- **가상화 알고리즘 선택 기준**에 따라 대규모 클라우드 IaaS 인프라는 **Type 1 (KVM/ESXi/Nitro)**, 개발 환경은 **Type 2 / Container** 채택

#### 한줄 요약

- 운영 격리와 호스트 장치 활용의 우선순위를 함께 평가하는 것이 핵심이다.
