---
sidebar:
  order: 87
  label: "087. 하이퍼바이저 유형: Type 1 vs Type 2"
  badge:
    text: "기출 · 85%"
    variant: note
title: "하이퍼바이저 유형: Type 1 vs Type 2 (Hypervisor Types)"
date: "2026-08-25T10:25:00+09:00"
tags:
  - "notes-hardware"
weight: 87
extra:
  question_no: "087"
  source_status: "기출"
  source_history: "128회, 131회, 132회, 137회"
  priority: 85
  priority_note: "네 번 반복 출제된 베어메탈과 호스티드 가상화 아키텍처 비교"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **하이퍼바이저(Hypervisor, VMM)**: 단일 물리 서버의 하드웨어 자원을 논리적으로 분할하여 다수의 독립된 가상 머신(VM)을 생성·통제하는 가상화 계층.
- **베어메탈(Bare-Metal)**: 호스트 운영체제(Windows/Linux)의 개입 없이 물리 하드웨어 실리콘 위에 하이퍼바이저가 직접 설치되는 네이티브 실행 환경.

</details>

- 정의/개념: 하드웨어 상주 위치와 호스트 OS 유무에 따라 베어메탈형(Type 1)과 호스티드형(Type 2)으로 분류하는 **하이퍼바이저 유형**
- 배경/필요성: 단일 OS 기반 서버 운영 시 **자원 활용률 저하 및 멀티테넌트 독립 격리 환경 구축 불가**

#### 한줄 요약
- 하드웨어 직결형 Type 1과 호스트 OS 기반 Type 2로 구분되어 성능과 유연성을 차별화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **장애 도메인(Failure Domain)**: 시스템 내부의 특정 소프트웨어가 고장 났을 때 그 여파로 인해 함께 중단되는 서비스의 물리적·논리적 영향 범위.
- **이중 스케줄링(Double Scheduling)**: Type 2 환경에서 게스트 OS 스케줄러와 호스트 OS 스케줄러가 2중으로 CPU 사이클을 조율하여 발생하는 지연.

</details>

- Type 1: 하이퍼바이저가 하드웨어에 직접 상주하여 OS 오버헤드 없는 초저지연 및 고성능 제공
- Type 2: 범용 OS 위 애플리케이션 형태로 구동되어 설치가 간편하나 **이중 스케줄링** 지연 발생
- **장애 도메인** 분리: Type 1은 VM 단위 격리, Type 2는 호스트 OS 크래시 시 전체 VM 동반 장애

#### 한줄 요약
- Type 1은 엔터프라이즈급 성능과 격리를, Type 2는 데스크톱 및 개발 편의성을 목표로 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **게스트 VM(Guest Virtual Machine)**: 하이퍼바이저가 할당한 vCPU, vRAM, vDisk를 기반으로 독립 실행되는 가상 운영체제 인스턴스.
- **호스트 OS(Host Operating System)**: Type 2 환경에서 물리 하드웨어를 직접 제어하며 하이퍼바이저 앱에 프로세스 자원을 공급하는 기본 OS.

</details>

```text
[하이퍼바이저 아키텍처 비교]
|-- Type 1 (Bare-Metal 하이퍼바이저)
|   |-- 게스트 VM 어레이 (VM 1, VM 2, VM N)
|   |-- Type 1 하이퍼바이저 (ESXi, KVM, Xen - 하드웨어 직접 제어)
|   `-- 물리 하드웨어 (CPU VT-x·메모리 EPT·SR-IOV 장치)
`-- Type 2 (Hosted 하이퍼바이저)
    |-- 게스트 VM 어레이 (VM 1, VM 2)
    |-- Type 2 하이퍼바이저 (VMware Workstation, VirtualBox)
    |-- 범용 호스트 OS (Windows, macOS, Ubuntu Linux)
    `-- 물리 하드웨어 (호스트 드라이버 경유 제어)
```

선의 의미: 계층 및 하드웨어 가상화 구조

| 구성요소 | Type 1 (Bare-Metal) 책임 | Type 2 (Hosted) 책임 |
|:---|:---|:---|
| 하이퍼바이저 계층 | 베어메탈 하드웨어 직접 제어 및 vCPU/vRAM 스케줄링 | 호스트 OS 위의 사용자 공간 프로세스로 동작 |
| 호스트 OS 계층 | **부재 (OS 없음)** | 물리 장치 드라이버 구동 및 기본 시스템 관리 |
| I/O 접근 경로 | 하이퍼바이저 내장 드라이버로 물리 버스 직결 | 게스트 $\to$ 하이퍼바이저 $\to$ 호스트 OS $\to$ 장치 3단계 경유 |
| 장애 격리성 | 단일 VM 장애가 타 VM에 영향 없음 (고신뢰성) | 호스트 OS 블루스크린 시 모든 게스트 동시 다운 |

#### 한줄 요약
- Type 1은 중간 OS 없이 하드웨어에 직결되며, Type 2는 범용 호스트 OS 계층 위에서 중계 실행된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **가상 I/O 패스(Virtual I/O Path)**: 게스트 VM 내부 디바이스 드라이버가 발행한 쓰기/읽기 요청이 물리 스토리지 컨트롤러에 도달하기까지의 계층별 처리 경로.

</details>

```text
게스트 VM 애플리케이션에서 디스크 I/O 요청 발생
        │
   게스트 OS 커널이 가상 블록 디바이스 드라이버에 명령 전달
        │
   하이퍼바이저 유형에 따른 I/O 처리 경로
   ┌────┴─────┐
[Type 1 베어메탈] [Type 2 호스티드]
   │             │
하이퍼바이저 드라이버가  가상 I/O 요청을 호스트 OS 시스템 콜로 변환
물리 디스크에 직접 커밋   │
   │             호스트 OS 파일시스템 드라이버가 물리 디스크에 전달
   │             │
   └────┬────────┘
        │
   물리 장치 처리 완료 후 하이퍼바이저를 통해 게스트로 가상 인터럽트 주입
```

#### 한줄 요약
- Type 1은 1단계 직결 I/O를 수행하고, Type 2는 호스트 OS를 거치는 3단계 변환 I/O를 수행한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **마이크로VM(MicroVM)**: Firecracker처럼 서버리스 및 컨테이너 격리를 위해 불필요한 장치 모델을 제거하고 수 밀리초 내에 기동하는 초경량 VM.

</details>

| 가상화 아키텍처 | Type 1 (Bare-Metal) | Type 2 (Hosted) | OS 컨테이너 (Docker) | 마이크로VM (Firecracker) |
|:---|:---|:---|:---|:---|
| 대표 제품 | VMware ESXi, KVM, Xen | VMware Workstation, VirtualBox | Docker, Podman, containerd | AWS Firecracker, Cloud-Hypervisor |
| 주 적용처 | 엔터프라이즈 클라우드, 데이터센터 | PC 개발/테스트, 교육 환경 | 마이크로서비스(MSA), CI/CD | 서버리스(Lambda), FaaS 환경 |
| 오버헤드 및 성능 | 네이티브 대비 95~99% 초고성능 | 호스트 OS 오버헤드로 성능 저하 | 99%+ (프로세스 수준 격리) | 98%+ (5ms 초고속 부팅) |
| 보안 격리성 | 하드웨어 지원 완전 격리 | 호스트 OS 종속적 격리 | 호스트 커널 공유로 취약 | 경량 하드웨어 하이퍼바이저 격리 |

#### 한줄 요약
- 엔터프라이즈 인프라는 Type 1, PC 개발은 Type 2, 클라우드 네이티브에는 컨테이너 및 MicroVM을 채택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **vCPU 오버커밋(vCPU Overcommit)**: 물리 코어 수보다 더 많은 가상 vCPU를 VM들에 할당하여 서버 집적도를 극대화하는 기법.
- **CPU 레디 타임(CPU Ready Time)**: vCPU가 실행 준비를 마쳤으나 물리 CPU 코어를 점유하지 못하고 대기열에서 지연되는 시간 백분율.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 과도한 **vCPU 오버커밋**으로 인한 성능 병목 | **CPU 레디 타임(%RDY < 5%)** 상시 모니터링 및 할당 조정 | 스케줄링 대기열 지연 해소 및 성능 균일화 |
| Type 1 스토리지 I/O 집중 시 처리 지연 | Virtio 반가상화 드라이버 및 SR-IOV 패스스루 적용 | VM-Exit 오버헤드 90% 감축 및 I/O 극대화 |
| 물리 서버 장애 시 다수 VM 동반 다운 | vSphere HA / KVM 클러스터 기반 자동 페일오버 구축 | 1분 이내 타 정상 노드로 무중단 재기동 |
| 멀티테넌트 환경의 CPU 캐시 사이드채널 공격 | 코어 스케줄링(Core Scheduling) 적용 및 테넌트 코어 격리 | 스펙터 등 이웃 VM 간 메모리 유출 차단 |

#### 한줄 요약
- CPU 레디 타임 관리, 반가상화 드라이버, 클러스터 HA, 코어 스케줄링으로 가용성과 성능을 확보한다.

## Ⅶ. 결론

- 대규모 클라우드 및 미션 크리티컬 인프라는 **Type 1 베어메탈 하이퍼바이저**를 구축하고, 초경량 격리 환경은 **MicroVM 및 컨테이너**와 연계한 하이브리드 가상화 확립

#### 한줄 요약
- 하이퍼바이저 아키텍처는 서비스의 성능, 가용성, 격리 요구수준에 따라 Type 1과 Type 2를 명확히 구분하여 설계해야 한다.