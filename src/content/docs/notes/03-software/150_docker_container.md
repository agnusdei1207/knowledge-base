---
sidebar:
  order: 150
  label: "150. Docker 컨테이너"
  badge:
    text: "기출 · 70%"
    variant: note
title: "Docker 컨테이너 (Docker Container)"
date: "2026-08-26T09:59:00+09:00"
tags:
  - "notes-software"
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

- **Docker Container**: 호스트 OS 커널을 공유하며 리눅스 네임스페이스와 cgroups로 애플리케이션과 의존성을 불변 이미지로 격리 실행하는 기술.
- **Namespaces & cgroups**: 프로세스 뷰(PID, NET, MNT)를 격리하는 Namespaces와 CPU, Memory 자원 사용량을 제한하는 cgroups.

</details>

- 정의/개념: 호스트 OS 커널을 공유하면서 **리눅스 네임스페이스와 cgroups를 통해 애플리케이션과 의존성을 불변 이미지로 격리 실행하는 기술**
- 배경/필요성: 개발-운영 환경 간 라이브러리 불일치 및 **기존 가상머신의 Guest OS 탑재에 따른 부팅 지연과 메모리 자원 낭비 해결 불가**

#### 한줄 요약
- 호스트 커널을 공유하는 경량 프로세스 격리와 레이어드 불변 이미지로 환경 일치성을 보장한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **OverlayFS**: 읽기 전용 이미지 레이어들을 하단에 공유하고 변경분만 최상단 쓰기 레이어에 기록하는 CoW(Copy-on-Write) 파일시스템.
- **OCI(Open Container Initiative)**: 컨테이너 이미지 포맷(image-spec)과 런타임 인터페이스(runtime-spec/runc)의 국제 표준 규격.

</details>

- Guest OS 없이 프로세스 단위로 실행되어 **초 단위의 고속 부팅 및 경량성**
- 불변 인프라(Immutable Infrastructure)를 보장하는 **Dockerfile 기반 이미지 빌드**
- cgroups 및 Namespaces를 통한 **호스트 커널 수준의 정밀한 자원 격리**

#### 한줄 요약
- 프로세스 수준의 경량 격리와 불변 이미지 빌드로 이식성과 자원 효율을 극대화한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Docker 런타임 스택**: Docker Client, dockerd 데몬, containerd, runc(OCI 런타임), OverlayFS 스토리지.

</details>

```text
[Docker 컨테이너 런타임 및 계층 아키텍처]
|-- 1. Docker Management Engine
|   |-- Docker CLI -> dockerd 데몬 -> containerd -> runc (OCI 런타임)
|-- 2. Linux Kernel Isolation Layer
|   |-- Namespaces (PID, NET, MNT, IPC, UTS, USER 독립 격리)
|   `-- cgroups (CPU 코어 할당, Memory 상한, Disk I/O 대역폭 제한)
`-- 3. Storage Layer (OverlayFS Union File System)
    |-- Container Writable Layer (최상단 Copy-on-Write 임시 쓰기 계층)
    `-- Read-Only Image Layers (App Code -> Python -> Alpine OS Base)
```

선의 의미: 계층 및 Docker CLI 명령이 runc를 거쳐 커널 격리 프로세스를 생성하고 OverlayFS 레이어에 연결되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| Docker Client & 데몬 | CLI 명령어를 수신하여 **이미지 빌드, 컨테이너 생성 및 네트워크 생명주기 총괄** | dockerd, REST API |
| containerd & runc | OCI 표준에 따라 **호스트 커널 시스템 콜을 호출하여 격리된 컨테이너 프로세스 실행** | OCI 표준 런타임 |
| 네임스페이스 (Namespaces) | 프로세스 ID(PID), 네트워크(NET), 파일시스템(MNT)의 **가시 영역을 독립 격리** | 프로세스 뷰 격리 |
| 컨트롤 그룹 (cgroups) | 컨테이너별 **CPU 코어 수, RAM 최대 메모리, 디스크 I/O 대역폭 사용량 제한** | 자원 독점 방지 |
| 스토리지 (OverlayFS) | 읽기 전용 이미지 레이어와 **컨테이너 전용 쓰기 레이어를 병합(CoW) 제공** | 레이어 재사용 |

#### 한줄 요약
- Docker 데몬, OCI 런타임(runc), 커널 격리(NS/cgroups), OverlayFS 스토리지가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **컨테이너 빌드 및 실행 5단계**: Multi-stage 빌드 $\to$ 레지스트리 푸시 $\to$ 노드 Pull $\to$ 네임스페이스/cgroup 생성 $\to$ runc 프로세스 기동.

</details>

```text
개발자의 애플리케이션 컨테이너 배포 요청
        │
   [Multi-stage 빌드] 컴파일러를 배제한 경량 프로덕션 이미지 생성
        │
   [레지스트리 저장] 이미지 다이제스트(SHA-256) 및 서명을 포함하여 ECR/Harbor 푸시
        │
   [호스트 노드 Pull] 대상 서버가 레지스트리로부터 레이어를 병렬 다운로드 및 무결성 검증
        │
   [커널 격리 공간 생성] 리눅스 커널에서 PID/NET 네임스페이스와 cgroups 메모리 제한 할당
        │
   runc 런타임이 격리된 파일시스템 마운트 위에서 엔트리포인트 프로세스를 즉각 기동
```

#### 한줄 요약
- Multi-stage 빌드 → 레지스트리 저장 → 노드 Pull → 커널 격리 → runc 프로세스 기동 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **가상머신 vs Docker 컨테이너**: 하이퍼바이저 기반 하드웨어 가상화(VM)와 OS 커널 공유 프로세스 격리(컨테이너).

</details>

| 비교 항목 | 가상머신 (Virtual Machine) | Docker 컨테이너 (Container) |
|:---|:---|:---|
| 가상화 대상 계층 | **하드웨어 가상화 (Guest OS 독립 탑재)** | **OS 커널 가상화 (Host OS 커널 공유)** |
| 부팅 및 시작 속도 | OS 부팅 필요로 수 분(Minutes) 소요 | **프로세스 기동 수준으로 수 초(Seconds) 이내** |
| 이미지 용량 크기 | 수 GB ~ 수십 GB (Guest OS 포함) | **수십 MB ~ 수백 MB (경량 의존성만 포함)** |
| 보안 격리 수준 | **하이퍼바이저 기반 완벽한 커널 격리** | 동일 커널 공유로 잠재적 취약점 전파 위험 |

#### 한줄 요약
- 완전한 커널 격리는 가상머신, 초고속 경량 배포와 마이크로서비스는 Docker 컨테이너를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Container Escape**: 컨테이너 내부 프로세스가 루트 권한으로 실행될 때 커널 취약점을 악용하여 호스트 OS 제어권을 탈취하는 보안 사고.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 빌드 도구가 이미지에 남아 수 GB로 비대화 | **Multi-stage Build 적용 및 Distroless 최소 베이스 이미지 사용** | 이미지 용량 90% 축소 및 배포 가속 |
| Root 권한 실행으로 인한 호스트 커널 탈출 해킹 위험 | **Dockerfile 내 `USER nonroot` 명시 및 Rootless 런타임 강제** | 컨테이너 권한 상승 원천 차단 |
| 컨테이너 재시작 시 내부 생성 데이터 유실 | **호스트 볼륨 마운트 (`docker volume` / K8s PersistentVolume)** | 영속적 상태 데이터 무손실 보존 |
| 컨테이너의 무제한 메모리 점유로 호스트 OOM 다운 | **cgroups 기반 `memory: 2Gi` 및 CPU Limit 리소스 상한 명시** | 노드 안정성 100% 확보 |

#### 한줄 요약
- 멀티 스테이지 빌드, Non-root 실행, 외부 볼륨 마운트, 리소스 상한 설정으로 운영한다.

## Ⅶ. 결론

- 환경 일치성은 **Docker 컨테이너**, 경량화는 **멀티 스테이지** 선택

#### 한줄 요약
- Docker 컨테이너는 리눅스 커널 격리와 레이어드 불변 이미지를 통해 환경 일치성과 경량 배포를 실현하는 클라우드 네이티브의 핵심 배포 기술이다.