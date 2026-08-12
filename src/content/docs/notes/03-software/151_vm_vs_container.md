---
sidebar:
  order: 151
  label: "151. VM vs 컨테이너 비교 (VM vs Container)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "VM vs 컨테이너 비교 (VM vs Container)"
date: "2026-08-06T23:27:50+09:00"
tags: ["notes-software"]
weight: 151
extra:
  question_no: "151"
  source_status: "기출"
  source_history: "128회, 131회, 132회, 137회"
  priority: 70
  priority_note: "가상머신•컨테이너 격리 비교가 반복 출제됨"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Virtual Machine (VM / 가상머신)**: 하이퍼바이저(Hypervisor)가 하드웨어를 추상화하여 게스트 OS(Guest OS) 커널을 독자적으로 돌리는 중량급 하드웨어 가상화 기술.
- **Container (컨테이너)**: 호스트 OS(Host OS)의 커널을 공용으로 공유하면서, 리눅스 cgroups/Namespaces 격리로 프로세스 레벨만 가볍게 가상화하는 경량 가상화 기술.
- **Hypervisor Layer (하이퍼바이저 계층)**: Type-1 (Bare-metal: ESXi) 및 Type-2 (Hosted: VirtualBox) 로 물리 하드웨어 자원을 VM별로 나눌 수 있게 중계하는 하드웨어 추상화 엔진.

</details>

- 정의/개념: 하이퍼바이저 기반 Guest OS 레벨의 무거운 하드웨어 가상화(VM)와 호스트 커널 공유 기반 프로세스 레벨의 초경량 가상화(Container)를 기술 구조별로 대비하는 체계인 **VM vs Container**
- 배경/필요성: 100% 완전한 보안/OS 독점 격리성(VM)과 초고속 1초 배포/수평 오토스케일링(Container)의 기술적 트레이드오프 선택 지침 요구성

#### 한줄 요약

- VM은 집마다 전기·배관까지 따로 두고 컨테이너는 한 건물 설비를 공유한 채 방만 나누듯, 커널 분리 여부가 격리 강도와 실행 무게를 가른다.

## Ⅱ. 특징 (VM 대 Container 3대 격리 차원 비교)

<details><summary>핵심 용어</summary>

- **Kernel Sharing Risk**: 컨테이너는 호스트 커널을 100% 공유하므로, 커널 취약점 해킹 시 호스트 전체 및 타 컨테이너로 파형 유출될 위험 보유.

</details>

- **VM (Hardware-level Virtualization: Guest OS 전체 구동, 100% 완전 커널 격리, 수 GB Heavy)**
- **Container (OS-level Virtualization: Host OS Kernel 공유, 초고속 1초 부팅, 수 MB Light)**
- **Isolation Strength (VM은 하드웨어 수준 최상 보안, Container는 프로세스 수준 보통 보안)**

#### 한줄 요약

- 집 설비까지 분리하면 무겁지만 이웃 고장의 영향이 작고, 한 건물 설비를 공유하면 방은 빨리 만들 수 있지만 커널 결함이 공동 경계를 흔든다.

## Ⅲ. 구조 및 구성요소 (VM vs Container 스택 1:1 아키텍처 비교)

<details><summary>핵심 용어</summary>

- **Hypervisor vs Docker Engine**: VM은 Hypervisor(ESXi)가 가상 하드웨어를 만듦, Container는 Docker Engine(containerd)이 커널 cgroups/NS를 엮음.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                     VM vs Container Architecture                       │
├──────────────────────────────────┬─────────────────────────────────────┤
│ [ Virtual Machine Architecture ] │ [ Container Architecture ]          │
├──────────────────────────────────┼─────────────────────────────────────┤
│ App A          │ App B           │ App A            │ App B            │
│ Bins/Libs      │ Bins/Libs       │ Bins/Libs        │ Bins/Libs        │
│ Guest OS       │ Guest OS        │ Docker Engine (cgroups/NS)         │
│ Hypervisor (ESXi / KVM)          │ Host Operating System (Linux Kernel)│
│ Physical Server Infrastructure   │ Physical Server Infrastructure      │
└──────────────────────────────────┴─────────────────────────────────────┘
```

선의 의미: VM은 각 앱마다 무거운 Guest OS를 통째로 얹고 가고, Container는 Guest OS를 제거하고 Host OS 커널을 직접 공유하는 차이점.

| 비교 항목 | Virtual Machine (VM / 가상머신) | Container (도커 컨테이너) |
|:---|:---|:---|
| **가상화 계층** | **하드웨어 수준 가상화 (Hypervisor)** | **OS 커널 수준 가상화 (Container Engine)** |
| **운영체제(OS)** | **개별 독립 Guest OS 100% 탑재** | **Guest OS 0% (Host OS Kernel 공유)** |
| **부팅 속도 (Boot)** | 느림 (수분 소요) | **초고속 (수 밀리초 ~ 1초 이내)** |
| **자원 효율성** | 낮음 (Guest OS 자체 메모리 먹음) | **최상 (프로세스 실행 메모리만 소비)** |
| **보안 격리성** | **최상 (Guest OS 붕괴되어도 타 VM 안전)**| 보통 (Host Kernel 유출 시 전 파동 위험)|

#### 한줄 요약

- 하이퍼바이저와 게스트 OS는 집마다 설비를 나누고, 호스트 커널과 런타임은 같은 건물 안에서 방과 사용량 경계만 나눈다.

## Ⅳ. 흐름도 (VM 대 Container 배포 프로세스 흐름)

<details><summary>핵심 용어</summary>

- **Startup Latency**: VM은 BIOS init 및 OS 커널 로딩에 2분 소요, Container는 `execve()` 커널 시스템 콜로 0.1초 소요.

</details>

```text
[VM Deployment]        ──► Hypervisor ──► Guest OS Boot (2-Min) ──► App Execution
[Container Deployment] ──► Docker Engine ──► execve() Syscall (0.1s) ──► App Execution
```

### 동작 원리

1. **VM Launch**: 하이퍼바이저가 가상 메모리를 떼어 주고 Guest OS 커널 부팅 2분 소요.
2. **Container Launch**: 도커 엔진이 이미 켜져 있는 Host Kernel에 cgroups/NS만 걸어 `execve()` 시스템 콜 즉시 가동 (**VM vs Container 완결**).

#### 한줄 요약

- VM은 빈 집의 설비와 운영체제를 모두 켠 뒤 입주하고, 컨테이너는 이미 켜진 건물에 새 방과 전기 한도만 만들어 들어간다.

## Ⅴ. 종류 및 비교 (VM과 Container의 하이브리드 조합: Kata Containers)

<details><summary>핵심 용어</summary>

- **Kata Containers / Firecracker**: Container의 초고속 부팅 속도와 VM의 100% 완전 커널 격리 장점만을 융합한 MicroVM / Secure Container 기술.

</details>

| 비교 기술 | Pure VM | Pure Container | Secure Container (Kata / Firecracker) |
|:---|:---|:---|:---|
| **격리 경계** | Hypervisor / Guest OS | Host Kernel Sharing | **MicroVM Lightweight Hypervisor** |
| **부팅 속도** | 2분 내외 | **0.1초 이내** | **0.5초 이내 (초경량 MicroVM)** |
| **보안 수준** | 최상 | 보통 | **최상 (독자 MicroVM 커널 보유)** |
| **사용 도메인**| 금융 코어 시스템 | 일반 MSA 웹/앱 API | **AWS Lambda, 멀티테넌트 SaaS** |

#### 한줄 요약

- 서로 믿지 못하거나 다른 운영체제가 필요하면 집을 나누는 VM을, 같은 커널에서 빠르게 복제해야 하면 방을 나누는 컨테이너를 선택한다.

## Ⅵ. 실무 고려사항 및 대책 (실무 선택 3대 의사결정 지침)

<details><summary>핵심 용어</summary>

- **Multi-Tenant Security Risk**: 이종 고객사(Tenant A vs Tenant B)를 동일 호스트 인프라에서 구동할 시 컨테이너 대신 VM 사용 필수.

</details>

| 3대 구축 의사결정 상황 | 최적 추천 아키텍처 기술 | 선택 사유 및 실무 대책 |
|:---|:---|:---|
| **1. 멀티테넌트 SaaS 보안** | **VM 또는 Kata Containers** | **타 고객사 데이터 유출 0% 완전 커널 격리** |
| **2. K8s 수평 오토스케일링**| **Docker Container** | **트래픽 폭발 시 1초 내 수백 개 Pod 확장** |
| **3. Windows 레거시 SW** | **VM (Windows Guest OS)** | Linux Host 커널에서 Windows SW 구동 불가 |

> 사례: **AWS Lambda (Firecracker MicroVM 사용) 및 쿠팡 / 당근마켓 K8s Container 혼용**

#### 한줄 요약

- 서로 다른 고객은 건물 설비까지 VM으로 나누고, 한 고객 안의 서비스는 같은 건물의 컨테이너 방으로 배치해 격리와 교체 속도를 함께 맞춘다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **VM vs Container 수립 기준(VM and Container Standards)**: 하드웨어 가상화(VM), OS 가상화(Container), Kata MicroVM 및 Multi-Tenancy 보안성에 의거한 체계.

</details>

- **VM vs Container 수립 기준**에 따라 Enterprise 아키텍처 설계 시 **VM (Core Storage) + Container (Stateless App)** 필수 혼용 적용

#### 한줄 요약

- 서로 믿지 못하거나 운영체제가 다르면 집을 나누고, 같은 커널을 믿을 수 있으면 한 건물 안의 방을 늘려 배포 속도와 밀도를 높인다.
