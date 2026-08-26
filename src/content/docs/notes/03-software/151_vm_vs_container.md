---
sidebar:
  order: 151
  label: "151. VM vs 컨테이너 비교"
  badge:
    text: "기출 · 70%"
    variant: note
title: "VM vs 컨테이너 비교 (VM vs Container)"
date: "2026-08-26T13:11:10+09:00"
tags:
  - "notes-software"
weight: 151
extra:
  question_no: "151"
  source_status: "기출"
  source_history: "128회, 131회, 132회, 137회"
  priority: 70
  priority_note: "가상머신•컨테이너 격리 비교가 반복 출제됨"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **가상머신(VM) vs 컨테이너(Container)**: 하이퍼바이저 기반 독립 Guest OS를 실행하는 가상머신과 호스트 커널을 공유하며 리눅스 Namespaces/cgroups로 격리하는 경량 컨테이너.
- **MicroVM(Firecracker / Kata)**: 컨테이너의 빠른 시작 속도(수 밀리초)와 VM의 독립 커널 보안 격리를 결합한 초경량 하이퍼바이저 기술.

</details>

- 정의/개념: 하드웨어 가상화 기반의 **독립 Guest OS를 구동하는 가상머신(VM)과 호스트 커널을 공유하는 경량 격리 컨테이너(Container)의 가상화 패러다임**
- 배경/필요성: 단일 가상화 방식 고수 시 발생하는 **완벽한 커널 보안 격리 요구와 초고속 마이크로서비스 배포 탄력성 간의 상충 해결 불가**

#### 한줄 요약
- 보안 격리가 최우선이면 VM, 초고속 기동과 고밀도 자원 효율이 최우선이면 컨테이너를 선택한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Hypervisor**: 물리 하드웨어를 가상화하여 복수의 독립된 Guest OS를 실행시키는 계층(Type 1: KVM/ESXi).
- **Container Runtime**: OCI 규격에 따라 커널 시스템 콜을 호출하여 네임스페이스와 cgroups 격리 프로세스를 생성하는 엔진(runc).

</details>

- 하드웨어 가상화를 통한 **완벽한 Guest OS 및 커널 수준의 보안 격리(VM)**
- 호스트 커널 공유를 통한 **수 밀리초 단위 초고속 부팅 및 고밀도 집적(Container)**
- 워크로드의 신뢰 수준과 오토스케일링 주기에 따른 **명확한 기술 선택 기준 제공**

#### 한줄 요약
- 커널 격리 강도와 자원 운영 효율성 간의 균형을 통해 최적의 가상화 계층을 설계한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **가상화 스택 구조**: VM 계층(App + Guest OS + Hypervisor), Container 계층(App + containerd/runc + Host Kernel).

</details>

| 구성요소 | 책임 | 주요 특징 |
|:---|:---|:---|
| 가상머신 (VM) | 하이퍼바이저 기반으로 **독립된 Guest OS 커널을 실행하여 완벽한 하드웨어 격리 보장** | 완벽한 커널 격리 |
| 컨테이너 (Container) | 호스트 커널을 공유하며 **Namespaces와 cgroups를 통해 격리된 프로세스 환경 제공** | 초경량 고속 기동 |
| 하이퍼바이저 | CPU, 메모리, I/O 하드웨어를 가상화하여 **다중 OS 간의 자원 충돌 및 간섭 방지** | Type 1 (KVM, ESXi) |
| 컨테이너 런타임 | OCI 표준 명세에 따라 **리눅스 시스템 콜을 직접 호출하여 격리 프로세스 즉시 생성** | runc, containerd |

#### 한줄 요약
- VM(하드웨어 가상화), 컨테이너(OS 커널 격리), 하이퍼바이저, 컨테이너 런타임이 상호 비교된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **가상화 실행 5단계**: 요구 분석 $\to$ 모델 분기 $\to$ 자원 할당 $\to$ 부팅/마운트 $\to$ 프로세스 실행.

</details>

```text
워크로드 실행 환경 선택 및 기동 요청
        │
   [요구 분석] 다중 테넌트 커널 격리가 필수인지, MSA 초고속 확장이 필요한지 분석
        │
   [실행 모델 분기] 커널 분리는 VM 경로, 경량 고밀도 배치는 Container 경로 분기
   ┌────┴───────────────────────────┐
  VM 경로                           Container 경로
   │                                 │
[가상 하드웨어 할당]                [네임스페이스/cgroups 생성]
vCPU, vRAM, vDisk 할당            PID, NET 네임스페이스 및 메모리 상한 할당
   │                                 │
[Guest OS 부팅]                     [불변 이미지 즉시 마운트]
OS 커널 로딩 (수 분 소요)         OverlayFS 레이어 마운트 (수 밀리초)
   │                                 │
   └────┬───────────────────────────┘
        ▼
   애플리케이션 엔트리포인트 프로세스 가동 및 서비스 트래픽 개시
```

#### 한줄 요약
- 요구 분석 → 모델 분기 → 자원 할당 → 부팅/마운트 → 프로세스 가동 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Pure VM vs Pure Container vs Secure Container**: 전통 VM, 표준 컨테이너, 둘을 융합한 MicroVM(Firecracker/Kata).

</details>

| 비교 항목 | 순수 가상머신 (Pure VM) | 순수 컨테이너 (Pure Container) | 보안 컨테이너 (MicroVM: Firecracker) |
|:---|:---|:---|:---|
| 커널 격리 수준 | **완벽한 독립 Guest OS 커널 격리**| 호스트 OS 커널 공유 (공유 취약점)| **경량 독립 커널 탑재 (완벽 격리)** |
| 부팅 기동 속도 | 수 분(Minutes) 소요 (느림) | **수 초 ~ 수 밀리초 (매우 빠름)** | **수 밀리초(5ms 이내: 매우 빠름)** |
| 이미지 디스크 용량| 수 GB ~ 수십 GB (OS 포함) | **수십 MB ~ 수백 MB (경량)** | 수 MB ~ 수십 MB (최소 커널) |
| 최적 적용 사례 | **금융 코어 원장, 윈도우 레거시** | **마이크로서비스, 웹/API, CI/CD** | **AWS Lambda 서버리스, 멀티테넌트**|

#### 한줄 요약
- 엄격한 격리는 VM, 초고속 배포는 컨테이너, 서버리스 멀티테넌트는 Secure Container(MicroVM)를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Multi-Tenant Container Escape**: 다중 고객 코드가 동일 호스트 커널에서 돌 때 악성 컨테이너가 커널 취약점을 뚫고 타 고객 데이터를 탈취하는 사고.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 멀티테넌트 환경에서 컨테이너 탈출 해킹으로 타 테넌트 침해 | **테넌트 경계마다 VM 분리 또는 Kata Containers(MicroVM) 적용** | 커널 수준 완전 격리 달성 |
| 수천 개 컨테이너 급증 시 호스트 커널 리소스 고갈 | **Kubernetes Resource Request/Limit 및 cgroups 엄격 통제** | 단일 컨테이너의 호스트 자원 고갈 방지 |
| 리눅스 컨테이너 환경에서 윈도우 기반 레거시 앱 구동 불가 | **Hyper-V 기반 Windows 가상머신(VM) 전용 인스턴스 구축** | OS 아키텍처 호환성 완벽 보장 |
| VM의 느린 확장 속도로 인한 스파이크 트래픽 대응 실패 | **사전 프로비저닝된 VM 풀 위에서 K8s 컨테이너 오토스케일링** | 초 단위 급속 확장 가용성 확보 |

#### 한줄 요약
- 테넌트 격리(MicroVM), K8s 자원 상한 설정, VM 풀 기반 컨테이너 확장으로 안정성을 확보한다.

## Ⅶ. 결론

- 보안 격리는 **가상머신**, 초고속 배포는 **컨테이너** 선택

#### 한줄 요약
- VM과 컨테이너는 대립 관계가 아닌 상호 보완재로서, 커널 보안 격리와 경량 배포 탄력성을 결합하여 현대 클라우드 인프라를 완성하는 핵심 가상화 기술이다.
