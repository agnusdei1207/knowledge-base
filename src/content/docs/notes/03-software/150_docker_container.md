---
sidebar:
  order: 150
  label: "150. Docker 컨테이너 (Docker Container)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "Docker 컨테이너 (Docker Container)"
date: "2026-08-14T01:52:00+09:00"
tags: ["notes-software"]
weight: 150
extra:
  question_no: "150"
  source_status: "기출"
  source_history: "120회, 128회, 131회, 132회"
  priority: 70
  priority_note: "컨테이너 격리•이미지 구조는 반복 출제됐음"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Docker Container (도커 컨테이너)**: 호스트 OS의 커널(Kernel)을 공유하면서, 애플리케이션 실행에 필요한 코드, 라이브러리, 의존성 패키지를 불변 이미지(Immutable Image)로 패키징하여 격리된 프로세스로 빠르게 실행하는 리눅스 가상화 기술.
- **cgroups & Namespaces**: 리눅스 커널의 핵심 격리 메커니즘으로, cgroups(Control Groups)는 CPU/Memory 자원 사용량을 제한하고, Namespaces는 PID/Net/IPC 등 가시 범위를 철저히 분리.
- **OverlayFS (Union File System)**: 이미지 레이어를 읽기 전용(Read-Only) 계층으로 공유하고, 변경사항만 제일 위 쓰기 계층(Writable Layer)에 기록하는 초경량 레이어드 파일시스템.

</details>

- 정의/개념: Image를 커널 격리 프로세스로 실행하는 **Docker Container**
- 배경/필요성: 호스트별 의존성 차이와 **Guest OS 중복**으로 배포 지연

#### 한줄 요약

- 도커파일로 정의한 애플리케이션과 의존성을 불변 이미지로 패키징하면 어떤 호스트에서든 동일한 실행 환경을 재현할 수 있다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Immutable Infrastructure**: 한번 빌드된 Docker 이미지는 절대 수정되지 않으며, 변경 시 새 이미지를 빌드해 교체 배포.

</details>

- Host Kernel 공유로 **Guest OS 중복** 제거
- **Namespaces•cgroups**로 가시 범위와 자원 사용 격리
- **OverlayFS•CoW**로 Image Layer 재사용

#### 한줄 요약

- 같은 건물의 방들이 벽과 전기 차단기를 나눠 쓰듯, 네임스페이스가 보이는 자원을 가르고 제어 그룹이 각 컨테이너의 사용량을 제한한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Docker Engine & containerd**: Docker Client (CLI) $\rightarrow$ Docker Daemon (dockerd) $\rightarrow$ containerd $\rightarrow$ runc (OCI Runtime)로 이어지는 격리 프로세스 생성 체계.

</details>

```text
[Docker Engine]
 ├── [Docker Client•Daemon]
 ├── [containerd•runc]
 ├── [Image•OverlayFS]
 └── [Kernel 격리 기능]
```

| 구성요소 | 책임 |
|---|---|
| Docker Client•Daemon | **명령 API**와 Image•Container 수명주기 관리 |
| containerd•runc | OCI Bundle로 **Container Process** 생성 |
| Image•OverlayFS | 읽기 전용 Layer와 **CoW 변경층** 제공 |
| Kernel 격리 기능 | **Namespaces•cgroups**로 범위•자원 제한 |

#### 한줄 요약

- 빌더가 만든 봉인 상자를 레지스트리에 두면 런타임이 이를 받아 개인 방과 전기 한도를 붙이고, 버려지면 안 되는 자료는 외부 보관함에 연결한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Multi-stage Build**: Dockerfile 내에서 빌드용 이미지와 실행용 이미지를 분리하여 최종 이미지 용량을 1GB에서 20MB로 파격 축소하는 기술.

</details>

```text
[배포 명세]
    │
    ▼
1. Image Layer 빌드
    │
    ▼
2. Image 서명•저장
    │
    ▼
3. Image Pull•검증
    │
    ▼
4. 격리 환경 생성
    │
    ▼
5. Container Process 실행
    │
    ▼
[서비스 제공]
```

### 동작 원리

1. **Image Layer 빌드**: Dockerfile로 재사용 Layer 생성
2. **Image 서명•저장**: Digest•서명을 Registry에 보관
3. **Image Pull•검증**: 대상 Image 무결성과 출처 확인
4. **격리 환경 생성**: Namespace•cgroup•Mount 구성
5. **Container Process 실행**: runc가 지정 Process 시작

#### 한줄 요약

- 레지스트리에서 이미지의 다이제스트를 검증해 풀한 뒤 네임스페이스와 cgroup으로 격리하고, 컨테이너를 교체해도 유지할 데이터는 외부 볼륨에 마운트한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Hypervisor vs Container**: VM은 하이퍼바이저 기반 Guest OS 전체 탑재, Docker는 Host OS 커널 공유 격리 프로세스.

</details>

| 비교 항목 | Virtual Machine (가상머신) | Docker Container (컨테이너) |
|:---|:---|:---|
| **가상화 수준** | **하드웨어 가상화 (Guest OS 전체 탑재)** | **OS 커널 레벨 가상화 (Host OS 커널 공유)** |
| **부팅 속도** | Guest OS 시작 필요 | **Process 중심 빠른 시작** |
| **자원 용량 (Size)**| OS Image 포함 | **App•의존성 Layer 중심** |
| **격리 및 보안성** | Guest Kernel 경계 | **Host Kernel 공유 경계** |

#### 한줄 요약

- 컨테이너는 같은 건물 안의 잠긴 방이라 빨리 만들 수 있고, 가상 머신은 기초 설비까지 나눈 별도 건물이라 무겁지만 커널 경계가 더 분명하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Non-root Container User**: 컨테이너 내부 프로세스를 root 계정이 아닌 일반 유저(`USER appuser`)로 돌려 컨테이너 탈출 해킹(Container Escape)을 예방.

</details>

| 3대 컨테이너 보안 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Image Fatness (대용량)**| 빌드 도구, 컴파일러가 이미지에 잔존 | **Multi-stage Build & Distroless 최소 이미지 적용**|
| **2. Container Escape Risk**| Root 권한 실행으로 호스트 커널 탈출해킹| **Dockerfile 내 `USER node` 비루트 계정 지정** |
| **3. Ephemeral Storage Loss**| 컨테이너 재시작 시 내부 데이터 소멸 | **Docker Volume / K8s PersistentVolume 마운트**|

> 사례: **토스 / 당근마켓 / 쿠팡 Docker & Kubernetes 기반 전사 마이크로서비스 배포**

#### 한줄 요약

- 조립 공구는 최종 배송 상자에서 빼고 상자 지문을 고정하며, 상자를 버려도 남아야 할 자료와 기록은 외부 보관함에 둔다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **Docker 수립 기준(Docker Container Standards)**: OCI 규격, Multi-stage Build, Non-root 계정, OverlayFS 및 cgroups/NS 리소스 제어성에 의거한 체계.

</details>

- 빠른 교체는 **Container**, Kernel 경계가 필요하면 VM 선택

#### 한줄 요약

- 같은 커널에서 빠르게 교체할 서비스는 컨테이너로 묶고, 커널 자체를 분리해야 하는 신뢰 경계라면 가상 머신을 선택한다.
