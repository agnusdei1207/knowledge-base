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

- **가상머신(VM, Virtual Machine)**: 하이퍼바이저(Hypervisor)가 하드웨어를 추상화하여 게스트 OS(Guest OS)를 독립 실행하는 중량급 하드웨어 가상화 기술.
- **컨테이너(Container)**: 호스트 OS(Host OS) 커널을 공유하며 리눅스 cgroups/Namespaces로 프로세스 수준에서 격리하는 경량 가상화 기술.
- **하이퍼바이저(Hypervisor)**: 물리적 자원을 가상화하여 다수의 Guest OS가 하드웨어를 공유하도록 제어하는 가상화 엔진.

</details>

- 정의: 하이퍼바이저 기반 Guest OS 독점적 하드웨어 가상화(VM)와 호스트 커널 공유 기반 프로세스 격리(Container)의 구조적 비교.
- 배경: 완전 격리(VM)의 보안성과 고속 배포/확장성(Container) 간 트레이드오프에 따른 상황별 기술 선택.

#### 한줄 요약

- VM은 하드웨어 단위, 컨테이너는 커널 공유 기반 프로세스 단위 격리로 성능과 격리 강도 차이 발생.

## Ⅱ. 특징 (VM 대 Container 3대 격리 차원 비교)

- **커널 공유 취약점(Kernel Sharing Risk)**: 컨테이너는 호스트 커널 공유로, 커널 취약점 발생 시 호스트 및 타 컨테이너로 영향 전파 위험.

- **VM (Hardware-level Virtualization)**: Guest OS 구동, 커널 분리, 고립된 보안 수준(수 GB 단위).
- **Container (OS-level Virtualization)**: Host Kernel 공유, 프로세스 격리, 경량 실행(수 MB 단위).
- **격리 강도(Isolation Strength)**: 하드웨어 수준(VM) 대비 프로세스 수준(Container) 격리 보안성 차이.

- VM은 하드웨어 분리로 안정적이나 무거움, 컨테이너는 커널 공유로 빠르나 공동 경계 보안 위협 상존.

## Ⅲ. 구조 및 구성요소 (VM vs Container 스택 1:1 아키텍처 비교)

<details><summary>핵심 용어</summary>

- **하이퍼바이저 vs 도커 엔진(Hypervisor vs Docker Engine)**: VM은 하이퍼바이저(Hypervisor)가 가상 하드웨어를 생성, 컨테이너는 도커 엔진(Docker Engine)이 커널 cgroups/Namespaces를 제어.

</details>

```text
┌────────────────────────────────────────┬──────────────────────────────────────────┐
│           가상머신 아키텍처             │            컨테이너 아키텍처              │
├────────────────────────────────────────┼──────────────────────────────────────────┤
│ 앱 A       │ 앱 B                      │ 앱 A             │ 앱 B                  │
│ 라이브러리 │ 라이브러리                │ 라이브러리       │ 라이브러리            │
│ 게스트 OS  │ 게스트 OS                 │ 컨테이너 엔진(cgroups/NS)                │
│ 하이퍼바이저 (ESXi/KVM)                │ 호스트 OS (리눅스 커널)                  │
│ 물리 하드웨어 인프라                   │ 물리 하드웨어 인프라                     │
└────────────────────────────────────────┴──────────────────────────────────────────┘
```

- 구조 차이: VM은 앱마다 Guest OS 탑재, 컨테이너는 Guest OS 제거 후 Host 커널 직접 공유.

| 비교 항목 | 가상머신(VM) | 컨테이너(Container) |
|:---|:---|:---|
| **가상화 계층** | 하드웨어 수준 (Hypervisor) | OS 커널 수준 (Container Engine) |
| **운영체제(OS)** | 개별 독립 Guest OS 탑재 | Guest OS 없음 (Host Kernel 공유) |
| **부팅 속도** | 느림 (분 단위) | 초고속 (초 단위) |
| **자원 효율성** | 낮음 (Guest OS 메모리 점유) | 높음 (프로세스 메모리만 사용) |
| **보안 격리성** | 최상 (커널 수준 격리) | 보통 (커널 공유 취약점 노출) |

- VM은 게스트 OS를 포함하여 독립적이나 무거움, 컨테이너는 호스트 커널 공유로 효율적이나 의존성 존재.

## Ⅳ. 흐름도 (VM 대 Container 배포 프로세스 흐름)

- **시동 지연(Startup Latency)**: VM은 BIOS/OS 로딩으로 수 분 소요, 컨테이너는 `execve()` 시스템 콜로 수 밀리초(ms) 단위 즉시 실행.

```text
[VM 배포]        ──► 하이퍼바이저 ──► 게스트 OS 부팅(분) ──► 앱 실행
[컨테이너 배포]  ──► 컨테이너 엔진 ──► 시스템 콜(ms) ──► 앱 실행
```

### 동작 원리

1. **VM 실행**: 하이퍼바이저 기반 가상 메모리 할당 및 Guest OS 커널 부팅(분 단위).
2. **컨테이너 실행**: 도커 엔진이 Host Kernel에 cgroups/Namespaces 적용 및 `execve()` 시스템 콜 호출(즉시 가동).

- VM은 OS까지 모두 켜고 입주, 컨테이너는 켜진 호스트 커널 위에서 환경만 생성하여 즉시 가동.

## Ⅴ. 종류 및 비교 (VM과 Container의 하이브리드 조합: Kata Containers)

- **카타 컨테이너 / 파이어크래커(Kata Containers / Firecracker)**: 컨테이너의 고속 부팅과 VM의 커널 격리 장점을 융합한 MicroVM / Secure Container 기술.

| 비교 기술 | Pure VM | Pure Container | Secure Container |
|:---|:---|:---|:---|
| **격리 경계** | Hypervisor/Guest OS | Host Kernel | MicroVM Hypervisor |
| **부팅 속도** | 분 단위 | 0.1초 이내 | 0.5초 이내 |
| **보안 수준** | 최상 | 보통 | 최상 |
| **도메인** | 금융 코어 | 일반 MSA | AWS Lambda, SaaS |

- 보안 및 OS 독립성 필요 시 VM, 고속 복제 및 효율성 필요 시 컨테이너 적용.

## Ⅵ. 실무 고려사항 및 대책 (실무 선택 3대 의사결정 지침)

- **멀티테넌트 보안 위협(Multi-Tenant Security Risk)**: 이종 고객을 동일 호스트에서 구동 시 커널 분리가 가능한 VM 사용 필수.

| 3대 구축 의사결정 상황 | 최적 추천 아키텍처 기술 | 선택 사유 및 실무 대책 |
|:---|:---|:---|
| **1. 멀티테넌트 SaaS 보안** | **VM 또는 Kata Containers** | **타 고객사 데이터 유출 0% 완전 커널 격리** |
| **2. K8s 수평 오토스케일링**| **Docker Container** | **트래픽 폭발 시 1초 내 수백 개 Pod 확장** |
| **3. Windows 레거시 SW** | **VM (Windows Guest OS)** | Linux Host 커널에서 Windows SW 구동 불가 |

> 사례: **AWS Lambda (Firecracker MicroVM 사용) 및 쿠팡 / 당근마켓 K8s Container 혼용**

- 보안 격리가 필요한 멀티테넌트 환경은 VM, 고밀도 오토스케일링은 컨테이너 아키텍처 채택.

## Ⅶ. 결론

- **VM/컨테이너 수립 기준(VM vs Container Standards)**: 하드웨어 가상화(VM), OS 가상화(Container), MicroVM 보안성에 의거한 가상화 체계.

- VM(독점 자원)과 컨테이너(Stateless 앱)의 하이브리드 아키텍처 적용.

- 하이브리드 격리 및 밀도 기반 아키텍처 최적화 구현 필수.
