---
sidebar:
  order: 18
  label: "018. 가상화•하이퍼바이저"
  badge:
    text: "기출 · 70%"
    variant: note
title: "가상화•하이퍼바이저 (Virtualization•Hypervisor)"
date: "2026-08-26T09:34:00+09:00"
tags: [notes-software]
weight: 18
extra:
  question_no: "018"
  source_status: "기출"
  source_history: "125회, 129회"
  priority: 70
  priority_note: "125•129회 기출, 하이퍼바이저 타입·구조 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **하이퍼바이저(Hypervisor / VMM)**: 단일 물리 서버에서 복수의 가상 머신(VM)과 게스트 OS를 독립적으로 실행하도록 하드웨어 자원을 중재하는 가상화 계층.
- **가상 머신(VM, Virtual Machine)**: 하이퍼바이저로부터 가상 CPU, 메모리, 디스크를 독점 할당받아 구동되는 독립된 가상 컴퓨터 인스턴스.

</details>

- 정의/개념: 단일 물리 하드웨어 위에 복수의 게스트 OS를 격리 실행하기 위해 하드웨어를 추상화·중재하는 **가상 머신 모니터(Hypervisor/VMM)**
- 배경/필요성: 물리 서버 한 대를 OS 하나가 점유하면 평균 10~20% 이용률의 유휴 자원을 그대로 버리므로, 하드웨어와 게스트 OS 사이에 물리 자원을 분할·다중화하는 하이퍼바이저 계층을 끼워 넣어 한 대 위에서 이기종 OS를 격리 구동할 필요

#### 한줄 요약
- 하드웨어 자원을 추상화하여 복수의 게스트 OS를 독립된 가상 머신(VM)으로 격리 구동한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **VM Exit / Entry**: 게스트 OS가 특권 명령(I/O, 제어 레지스터 변경)을 실행할 때 CPU가 하이퍼바이저로 제어권을 넘겼다가(Exit) 처리 후 복귀(Entry)하는 하드웨어 상태 전환.
- **하드웨어 지원 가상화(Intel VT-x / AMD-V)**: CPU 내부에 비특권 게스트 모드(Non-Root)와 특권 하이퍼바이저 모드(Root)를 분리하여 가상화 오버헤드를 줄이는 기술.

</details>

- VM별 독립 가상 하드웨어 할당을 통한 완벽한 결함 및 보안 **격리 경계(Isolation)**
- **Intel VT-x / AMD-V** 하드웨어 가상화 확장을 통한 고속 VM Exit/Entry 전환
- 베어메탈 직결 **Type 1 (Native)** 과 호스트 OS 기반 **Type 2 (Hosted)** 로 아키텍처 분류

#### 한줄 요약
- 하이퍼바이저는 OS 수준 격리와 통합률을 모든 특권 명령에 개입하는 비용으로 사며, VT-x는 그 개입을 하드웨어로 내려 비용만 낮춘다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **EPT(Extended Page Tables)**: 게스트 가상 주소(GVA) $\to$ 게스트 물리 주소(GPA) $\to$ 호스트 물리 주소(HPA)의 2단계 주소 변환을 CPU 하드웨어가 직접 처리하는 2단계 페이징 기술.

</details>

```text
[하이퍼바이저 아키텍처 비교]
|-- Type 1 하이퍼바이저 (Bare-Metal / Native)
|   |-- 물리 하드웨어 (CPU VT-x, Memory EPT, NIC SR-IOV)
|   |-- Type 1 하이퍼바이저 커널 (KVM, ESXi, Xen, Hyper-V)
|   `-- 게스트 VM 1, 게스트 VM 2 (독립 게스트 OS 및 앱)
`-- Type 2 하이퍼바이저 (Hosted)
    |-- 물리 하드웨어
    |-- 호스트 OS (Windows, macOS, Linux)
    |-- Type 2 하이퍼바이저 앱 (VirtualBox, VMware Workstation)
    `-- 게스트 VM 1, 게스트 VM 2
```

선의 의미: 계층 및 가상화 실행 아키텍처

| 구성요소 | 책임 |
|:---|:---|
| Type 1 하이퍼바이저 | 하드웨어 위 직접 상주하여 VM 스케줄링, 메모리 분배, 하드웨어 중재를 전담 |
| Type 2 하이퍼바이저 | 호스트 OS 위 일반 애플리케이션으로 동작하며 호스트 커널 시스템 콜을 경유하여 VM 제어 |
| vCPU & EPT | 게스트 OS의 vCPU 스케줄링 및 2단계 메모리 주소 변환(**GVA $\to$ GPA $\to$ HPA**) 가속 |
| 가상 디바이스 에뮬레이터 | virtio / QEMU를 통해 가상 디스크, 가상 NIC 인터페이스를 VM에 에뮬레이션 |

#### 한줄 요약
- Type 1은 하이퍼바이저를 하드웨어 바로 위에 두어 호스트 OS 경유를 없애고 Type 2는 그 경유를 감수하는 대신 기존 OS 환경을 그대로 쓰므로, 계층 위치 하나가 성능과 편의성을 가른다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Trap-and-Emulate**: 게스트 OS가 하드웨어 민감 명령어를 실행하면 하드웨어 트랩을 걸어 하이퍼바이저가 가상화하여 에뮬레이션하는 기법.

</details>

```text
게스트 OS에서 민감/특권 명령어(I/O 접근, 페이지 테이블 변경 등) 실행 시도
        │
   하드웨어 CPU가 VM Exit 트리거 (Guest Non-Root -> Hypervisor Root 모드 전환)
        │
   하이퍼바이저의 Trap-and-Emulate 핸들러 진입
        │
   하이퍼바이저가 물리 자원을 직접 제어하여 요청 작업 안전 처리
   ┌────┴───────────────────────────┐
[Type 1 베어메탈]                [Type 2 호스트]
물리 디바이스 드라이버 직접 호출       호스트 OS 시스템 콜 경유 호출
   │                                │
   └────┬───────────────────────────┘
        │
   하드웨어 CPU가 VM Entry 트리거 (Hypervisor Root -> Guest Non-Root 모드 복귀)
        │
   게스트 OS 레지스터 값 갱신 후 정상 실행 재개
```

#### 한줄 요약
- 특권 명령마다 VM Exit과 Entry를 왕복하는 것이 가상화의 고정 비용이므로, 하드웨어 보조와 반가상화는 이 왕복 횟수를 줄이는 방향으로만 성능을 개선한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **컨테이너 가상화**: 하이퍼바이저 없이 호스트 OS 커널의 cgroups, namespaces를 활용하여 프로세스 단위로 격리하는 경량 가상화.

</details>

| 비교 항목 | Type 1 하이퍼바이저 (Bare-Metal) | Type 2 하이퍼바이저 (Hosted) | 컨테이너 (Container) |
|:---|:---|:---|:---|
| 구동 계층 | **물리 하드웨어 직접 위 (Bare-Metal)** | **호스트 OS 위 애플리케이션** | **호스트 커널 공유 (OS 가상화)** |
| 오버헤드 | **매우 낮음 (베어메탈 95~98% 성능)** | 높음 (호스트 OS 이중 경유) | **전무 (네이티브 프로세스 속도)** |
| 격리 및 보안 | **완벽한 OS/하드웨어 레벨 격리** | OS 레벨 격리 (호스트 취약점 공유) | 프로세스 레벨 격리 (커널 공유) |
| 부팅 시간 | 수십 초 ~ 수 분 (OS 풀 부팅) | 수십 초 ~ 수 분 | **수 밀리초 ~ 수 초 (프로세스 시작)** |
| 주요 솔루션 | VMware ESXi, KVM, Hyper-V | Oracle VirtualBox, VMware Workstation | Docker, containerd, Kubernetes |

#### 한줄 요약
- 클라우드 IaaS는 Type 1, 개인 개발/테스트는 Type 2, 클라우드 네이티브 MSA는 컨테이너를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **SR-IOV(Single Root I/O Virtualization)**: 단일 물리 PCIe 디바이스(NIC)를 여러 가상 기능(VF)으로 분할하여 VM이 하이퍼바이저 없이 직접 통신하는 하드웨어 가속 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 네트워크 I/O 시 VM Exit 빈발로 인한 지연 증가 | **SR-IOV(PCIe Passthrough) 및 virtio 드라이버** 적용 | 하이퍼바이저 오버헤드 제거 및 베어메탈 99% 네트워크 처리율 달성 |
| 2단계 페이징으로 인한 메모리 접근 지연 | CPU 하드웨어 **EPT/NPT 및 HugePages** 활성화 | TLB 미스 및 메모리 워크 시간 70% 단축 |
| 과도한 vCPU/메모리 오버서브스크립션(Overcommit) | **동적 자원 조절(Ballooning) 및 CPU Quota** 상한 통제 | 특정 VM의 자원 독점 방지 및 시스템 안정성 보장 |
| 물리 노드 장애 시 전체 VM 다운 위험 | **실시간 라이브 마이그레이션(Live Migration)** 구축 | 무중단 서비스 이전 및 고가용성(HA) 완성 |

#### 한줄 요약
- 하이퍼바이저 계층은 통합률을 얻는 대신 모든 I/O에 개입 비용을 더하므로, SR-IOV·EPT 거대 페이지로 그 개입을 우회시키고 Ballooning은 과할당 이득과 게스트 성능 저하를 맞바꾸는 수단으로만 쓴다.

## Ⅶ. 결론

- 클라우드 인프라는 **Type 1**, 서비스 계층은 **컨테이너** 선택

#### 한줄 요약
- 하이퍼바이저는 서버 가상화와 클라우드 컴퓨팅의 기반 기술이며, 하드웨어 가속과의 결합을 통해 베어메탈급 성능을 제공한다.