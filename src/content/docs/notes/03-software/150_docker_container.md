---
sidebar:
  order: 150
  label: "150. Docker 컨테이너 (Docker Container)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "Docker 컨테이너 (Docker Container)"
date: "2026-08-18T01:30:00+09:00"
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

- **Docker Container**: 호스트 OS의 커널(Kernel)을 공유하면서 리눅스 네임스페이스(Namespaces)와 cgroups를 통해 애플리케이션과 런타임 의존성을 불변 이미지(Immutable Image)로 패키징하여 격리 실행하는 기술.
- **환경 불일치 및 Guest OS 오버헤드(Environment Inconsistency & VM Overhead)**: 개발/운영 환경 간 패키지 버전 차이로 인한 배포 실패와 가상머신(VM)의 무거운 Guest OS로 인한 부팅 지연 및 자원 낭비.

</details>

- 정의/개념: 호스트 OS 커널을 공유하며 **리눅스 네임스페이스와 cgroups로 격리된 경량 불변 실행 환경을 제공**하는 컨테이너 가상화 기술
- 배경/필요성: 환경 간 라이브러리 버전 불일치("내 컴퓨터에선 되는데") 및 **기존 가상머신의 무거운 Guest OS 부팅 오버헤드와 자원 낭비 위험** 직면

#### 한줄 요약

- 호스트 커널을 공유하는 경량 프로세스 격리와 레이어드 불변 이미지를 통해 수 초 내의 초고속 배포와 환경 일치성을 보장

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **네임스페이스(Namespaces) & cgroups**: PID, 네트워크, 마운트 등의 가시 범위를 격리하는 Namespaces와 CPU, 메모리, 블록 I/O 할당량을 제한하는 cgroups.
- **OverlayFS (Union File System)**: 읽기 전용 이미지 레이어들을 하단에 공유하고 변경사항만 최상단 쓰기 레이어에 기록하는 CoW(Copy-on-Write) 파일시스템.

</details>

- Guest OS 없이 프로세스 단위로 실행되어 **수 초 이내의 초고속 부팅 및 경량화**
- 불변 인프라(Immutable Infrastructure)를 보장하는 **Dockerfile 기반 이미지 패키징**
- cgroups 및 Namespaces를 통한 **프로세스 수준의 안전한 자원 격리**

#### 한줄 요약

- OS 커널 수준의 경량 가상화를 통해 하드웨어 자원 낭비를 없애고 마이크로서비스 배포를 표준화

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Docker Engine 계층**: Docker Client(CLI), dockerd 데몬, containerd(컨테이너 생명주기), runc(OCI 저수준 런타임).

</details>

```text
[ Docker 컨테이너 런타임 및 이미지 레이어 아키텍처 ]

 1. [ Docker Engine 계층 ]
    [ Docker CLI ] ──► [ dockerd ] ──► [ containerd ] ──► [ runc (OCI) ]
                                                                │
                                                                ▼
 2. [ 격리된 컨테이너 프로세스 (Host Kernel) ] ──────────────────────────┐
    - cgroups: CPU / Memory 제한                                       │
    - Namespaces: PID, NET, MNT, IPC, UTS, USER 격리                   │
                                                                       │
 3. [ OverlayFS 레이어드 스토리지 ]                                    │
    ┌─────────────────────────────────────────────────────────────┐    │
    │ Container Writable Layer (CoW 임시 쓰기 계층)               │◄───┘
    ├─────────────────────────────────────────────────────────────┤
    │ Read-Only Image Layers (App Code ➔ Python ➔ Alpine OS Base) │
    └─────────────────────────────────────────────────────────────┘
```

선의 의미: Docker CLI 명령이 dockerd와 runc를 거쳐 커널 격리 프로세스를 생성하고 OverlayFS 레이어에 연결되는 구조.

| 구성요소 | 책임 |
|:---|:---|
| Docker Client & 데몬 | CLI 명령어를 수신하여 **이미지 빌드, 컨테이너 생성 및 네트워크 생명주기 총괄** |
| containerd & runc | OCI 표준에 따라 **호스트 커널 시스템 콜을 호출하여 격리된 컨테이너 프로세스 실행** |
| Namespaces (커널 격리) | 프로세스 ID(PID), 네트워크(NET), 파일시스템(MNT)의 **가시 영역을 독립 격리** |
| cgroups (자원 통제) | 컨테이너별 **CPU 코어 수, RAM 최대 메모리, 디스크 I/O 대역폭 사용량 제한** |
| OverlayFS (스토리지) | 읽기 전용 이미지 레이어와 **컨테이너 전용 쓰기 레이어를 병합(CoW) 제공** |

#### 한줄 요약

- Docker 데몬, OCI 런타임(runc), 커널 격리(NS/cgroups), OverlayFS 스토리지가 결합

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **컨테이너 빌드 및 실행 5단계 파이프라인**: Dockerfile 빌드 $\to$ 레지스트리 푸시 $\to$ 노드 Pull $\to$ 네임스페이스/cgroup 생성 $\to$ runc 프로세스 기동.

</details>

```text
[ Docker 이미지 빌드 및 컨테이너 실행 파이프라인 ]

 ┌────────────────────────────────────────┐
 │ 1. Dockerfile 기반 Multi-stage 빌드    │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 2. Docker Registry 이미지 푸시 및 서명 │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 3. 호스트 노드 이미지 Pull 및 무결성 검증
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 4. Namespaces & cgroups 격리 공간 생성 │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 5. runc 기반 컨테이너 프로세스 즉시 시작│
 └────────────────────────────────────────┘
```

### 동작 원리

1. 이미지 빌드: Multi-stage Dockerfile을 통해 컴파일러를 배제한 최소 용량의 프로덕션 이미지를 생성.
2. 레지스트리 저장: 이미지 다이제스트(SHA-256) 및 서명을 포함하여 프라이빗 레지스트리(ECR/Harbor)에 푸시.
3. 이미지 풀: 타깃 호스트 서버가 레지스트리에서 레이어를 병렬 다운로드하고 체크섬을 검증.
4. 격리 생성: 리눅스 커널에서 PID/NET 네임스페이스와 cgroups 메모리 제한(`--memory=2g`) 공간을 할당.
5. 프로세스 실행: runc 런타임이 격리된 파일시스템 마운트 위에서 엔트리포인트 프로세스를 기동.

#### 한줄 요약

- 빌드 $\to$ 레지스트리 저장 $\to$ 노드 풀 $\to$ 커널 격리 $\to$ 프로세스 실행의 5단계

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **가상머신(VM) vs 컨테이너**: 하드웨어 가상화 기반 Guest OS 탑재(VM)와 OS 커널 레벨 프로세스 격리(컨테이너).

</details>

| 구분 | 가상머신 (Virtual Machine) | Docker 컨테이너 (Container) |
|:---|:---|:---|
| **적용 기준** | 커널 수준의 완전한 다중 테넌트 격리 및 이종 OS 구동 | 마이크로서비스, CI/CD 고속 배포, 고밀도 자원 집적 |
| **핵심 특징** | **하이퍼바이저 기반 하드웨어 가상화, Guest OS 독립 탑재** | **호스트 OS 커널 공유, Namespaces/cgroups 프로세스 격리** |
| **한계** | 수 기가바이트의 무거운 용량 및 수 분의 부팅 지연 | 동일 커널 공유로 인한 잠재적 커널 취약점 전파 위험 |

#### 한줄 요약

- 엄격한 커널 분리는 가상머신, 초고속 경량 배포와 마이크로서비스는 Docker 컨테이너를 선택

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **컨테이너 탈출(Container Escape)**: 컨테이너 내부 프로세스가 Root 권한으로 실행될 때 커널 취약점을 악용하여 호스트 OS 제어권을 탈취하는 치명적 보안 위협.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 빌드 도구가 이미지에 남아 수 GB로 비대화 | **Multi-stage Build 적용 및 Distroless 최소 베이스 이미지 사용** | 이미지 용량 90% 축소 및 배포 속도 가속 |
| Root 권한 실행으로 인한 호스트 커널 탈출 해킹 위험 | **Dockerfile 내 `USER nonroot` 명시 및 Rootless 런타임 강제** | 컨테이너 권한 상승 원천 차단 |
| 컨테이너 재시작 시 내부 생성 데이터 유실 | **호스트 볼륨 마운트 (`docker volume` / K8s PersistentVolume)** | 영속적 상태 데이터 무손실 보존 |

#### 한줄 요약

- 멀티 스테이지 빌드, 비루트(Non-root) 실행, 외부 볼륨 마운트를 통해 안전하고 최적화된 컨테이너를 운용

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **클라우드 네이티브 표준(OCI Standard)**: Open Container Initiative 표준을 통해 빌드된 컨테이너가 K8s, Fargate 등 어디서든 완벽히 동작하는 생태계.

</details>

- **Docker 컨테이너**는 모던 소프트웨어 엔지니어링의 사실상 표준(De-facto Standard) 배포 단위이며, 멀티 스테이지 최소 빌드와 비루트 보안 수칙을 준수하여 쿠버네티스 오케스트레이션의 기반을 완성해야 함

#### 한줄 요약

- 리눅스 커널 격리와 레이어드 이미지를 기반으로 클라우드 네이티브 배포의 표준을 완성
