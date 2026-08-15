---
sidebar:
  order: 19
  label: "019. 전가상화•반가상화•컨테이너 비교 (Full•Para•Container Virtualization)"
  badge:
    text: "기출 • 50%"
    variant: note
title: 전가상화•반가상화•컨테이너 비교 (Full•Para•Container Virtualization)
date: "2026-08-13T13:37:00+09:00"
tags: [notes-software]
weight: 19
extra:
  question_no: "019"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "137회 기출, 가상화•컨테이너 경계 비교"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Full Virtualization (전가상화)**: 게스트 OS 수정 없이 하드웨어 전체를 하이퍼바이저가 완전 흉내내어(Binary Translation / Hardware-Assist) 구동시키는 가상화 방식.
- **Paravirtualization (반가상화)**: 게스트 OS 커널 소스 코드를 일부 수정하여 특권 명령 실행 시 하이퍼바이저에 하이퍼콜(Hypercall)을 직접 호출하는 고성능 가상화 방식.
- **Container Virtualization (컨테이너 가상화)**: 하이퍼바이저와 게스트 OS를 완전히 배제하고, Host Linux 커널(cgroups, namespaces)을 공유하며 프로세스를 경량 격리 구동시키는 방식.

</details>

- 정의/개념: 자원 추상화 계층 및 게스트 OS 커널 수정/상주 여부에 따른 3대 격리 아키텍처 비교인 **전가상화 vs 반가상화 vs 컨테이너 가상화**
- 배경/필요성: 단일 격리 방식은 OS 호환성과 **배치 밀도**를 함께 충족 곤란

#### 한줄 요약

- 게스트 수정과 커널 공유 범위에 따라 전가상화, 반가상화, 컨테이너를 구분한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Hypercall**: 반가상화 환경에서 게스트 OS가 하이퍼바이저 제어 서비스를 직접 호출하기 위해 사용하는 전용 소프트웨어 인터럽트/시스템 콜.
- **Namespaces & Cgroups**: Linux 커널 기능으로, 프로세스의 리소스 뷰(PID, Net, Mount)를 격리(Namespaces)하고 자원 사용량(CPU, RAM)을 제어(Cgroups)하는 컨테이너 핵심 기술.

</details>

- 지원 아키텍처의 미수정 게스트를 실행하는 **Full Virtualization**
- **Hypercall** 기반 커널 튜닝을 통한 가상화 트랩 오버헤드 억제 (**Paravirtualization**)
- Host Kernel 공유로 시작 비용과 메모리를 줄이는 **Container**

#### 한줄 요약

- 미수정 게스트, 하이퍼콜, 호스트 커널 공유의 경계 차이가 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **virtio**: Linux KVM/QEMU 환경에서 반가상화(Paravirtualization) 디스크/네트워크 I/O 고속 드라이버 표준 API 프레임워크.

</details>

```text
[격리 실행 구조]
 ├─ 워크로드
 ├─ 게스트 OS
 │   └─ 하이퍼바이저
 └─ 컨테이너 프로세스
     └─ 호스트 커널
```

선의 의미: 전가상화/반가상화는 하이퍼바이저 및 게스트 OS 상주 레이어를 갖추는 반면, 컨테이너는 Host Kernel 직결 프로세스 격리 구조를 형성함을 의미.

| 구성요소 | 책임 |
|:---|:---|
| 워크로드 | 격리 환경에서 애플리케이션 실행 |
| 게스트 OS | 전가상화•반가상화의 독립 커널 제공 |
| 하이퍼바이저 | 게스트의 CPU•메모리•I/O 자원 중재 |
| 컨테이너 프로세스 | 호스트 커널을 공유하며 격리된 실행 뷰 사용 |
| 호스트 커널 | **Namespaces•Cgroups**로 격리와 자원 제어 |

#### 한줄 요약

- 워크로드 아래의 게스트 또는 컨테이너와 하이퍼바이저의 중재 경계가 핵심이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Binary Translation**: 전가상화에서 하드웨어 지원이 없을 때 게스트의 Ring 0 특권 명령어를 런타임에 동적으로 동등한 안전 코드로 번역하여 하이퍼바이저에 넘기는 기법.

</details>

```text
┌──────────────────────────────┐
│ 워크로드 격리 방식 결정     │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 커널 공유 허용 판정      │
└───────┬──────────────────────┘
        ├─ 허용 ────────────────▶ [2. 컨테이너 선택]
        │ 불가
        ▼
┌──────────────────────────────┐
│ 2. 게스트 수정 가능성 판정  │
└───────┬──────────────────────┘
        ├─ 수정 가능 ───────────▶ [4. 반가상화 선택]
        └─ 수정 불가 ───────────▶ [5. 전가상화 선택]
```

### 동작 원리

1. **커널 공유 허용 판정**: 보안/OS 이종성 요구에 따라 Host Kernel 공유 가능 여부 체크.
2. **컨테이너 선택**: 커널 공유 가능 시 Namespaces•Cgroups 적용
3. **게스트 수정 가능성 판정**: 가상머신 전환 시 게스트 커널의 Hypercall 코드 이식 가능 여부 검증.
4. **반가상화 선택**: 게스트 수정 가능 시 하이퍼콜 인터페이스 적용
5. **전가상화 선택**: 게스트 수정 불가 시 하드웨어 지원 가상화 적용

#### 한줄 요약

- 커널 공유 허용 판정과 게스트 수정 가능성 판정으로 실행 방식을 선택한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Kata Containers**: 컨테이너의 경량성/속도 장점과 VM의 완벽한 커널 보안 격리 장점을 융합한 MicroVM 기반 컨테이너 기술.

</details>

| 비교 항목 | 전통적 VM (Full/Para) | Container (Docker/Podman) | MicroVM (Kata Containers / Firecracker) |
|:---|:---|:---|:---|
| 격리 메커니즘 | 하이퍼바이저 + 독립 커널 | Host Kernel Cgroups/Namespaces | 초경량 하이퍼바이저 + 전용 린 커널 |
| 메모리 점유 | 게스트 OS 메모리 포함 | 애플리케이션•런타임 중심 | 경량 게스트 커널 메모리 포함 |
| 시작 시간 | 게스트 OS 부팅 필요 | 프로세스 생성 중심 | 경량 VM 부팅 필요 |
| 주요 용도 | legacy OS, 타 OS 호환, IaaS | Cloud Native, Microservices, PaaS | Serverless FaaS, Multi-tenant K8s |

#### 한줄 요약

- 미수정은 전가상화, 수정 가능은 반가상화, 커널 공유는 컨테이너가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Kernel Shared Vulnerability (Dirty COW 등)**: 컨테이너 가상화 환경에서 Host Kernel 공유로 인해 단 1개의 컨테이너 취약점이 Host OS 전체 권한 탈취로 전파되는 보안 리스크.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Container의 Host Kernel 공유에 따른 보안 취약점 파급 | **seccomp, AppArmor, Rootless Container** 설정 | 커널 공격면 최소화 |
| Paravirtualization 적용 시 Windows 등 미지원 OS 구동 불가 | **virtio Guest Driver** 설치 패키지 인가 | 반가상화 드라이버 확장 |
| 전가상화 I/O 중재에 따른 지연 | **SR-IOV**와 NVMe 직접 할당 검토 | 가상 I/O 경로 단축 |

> 사례: Kubernetes 환경 상에서 **Docker/Containerd** 기본 구동 및 멀티테넌트 서버리스 환경 내 **Kata Containers / Firecracker** 구축

#### 한줄 요약

- 최소 권한, 제어 그룹, 공급망 신뢰성으로 커널 공격면과 자원 간섭을 통제한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **가상화 격리 선택 기준(Virtualization Isolation Criteria)**: OS 이종성, 보안 격리수준, 부팅 속도 타깃 및 리소스 가용성에 기반한 체계.

</details>

- **가상화 격리 선택 기준**에 따라 Microservice/DevOps는 **Container**, 강력한 보안 IaaS는 **Full Virt / MicroVM** 채택

#### 한줄 요약

- 커널 공유와 게스트 수정 여부 및 배치 밀도를 함께 평가하는 것이 핵심이다.
