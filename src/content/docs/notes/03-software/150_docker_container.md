---
sidebar:
  order: 150
  label: "150. Docker 컨테이너"
  badge:
    text: "기출 · 70%"
    variant: note
title: "Docker 컨테이너 (Docker Container)"
date: "2026-09-07T10:05:00+09:00"
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

- 정의/개념: 호스트 OS 커널을 공유하면서 리눅스 네임스페이스와 cgroups를 통해 애플리케이션과 의존성을 불변 이미지로 격리 실행하는 기술
- 배경/필요성: 전통적 가상머신(VM)의 Guest OS 중복 구동으로 인한 막대한 메모리 오버헤드, 느린 부팅 지연 및 개발-운영 간 환경 불일치(Matrix of Hell) 한계

#### 한줄 요약
- 컨테이너는 커널을 공유해 기동 시간과 메모리를 절감하는 대신 격리 경계가 그 커널 하나에 걸려 있으므로, 커널이 뚫리면 격리 자체가 무너지는 위험을 함께 산 것이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **OverlayFS**: 읽기 전용 이미지 레이어들을 하단에 공유하고 변경분만 최상단 쓰기 레이어에 기록하는 CoW(Copy-on-Write) 파일시스템.
- **OCI(Open Container Initiative)**: 컨테이너 이미지 포맷(image-spec)과 런타임 인터페이스(runtime-spec/runc)의 국제 표준 규격.

</details>

- Guest OS 없이 프로세스 단위로 실행되어 초 단위의 고속 부팅 및 경량성
- 불변 인프라(Immutable Infrastructure)를 보장하는 Dockerfile 기반 이미지 빌드
- cgroups 및 Namespaces를 통한 호스트 커널 수준의 정밀한 자원 격리

#### 한줄 요약
- 프로세스 수준의 경량 격리와 불변 이미지 빌드로 이식성과 자원 효율을 극대화한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Docker 런타임 스택**: Docker Client, dockerd 데몬, containerd, runc(OCI 런타임), OverlayFS 스토리지.

</details>

```text
[Docker 컨테이너 런타임]
├─ [제어 및 관리 계층]
│  ├─ Docker Client (CLI 인터페이스)
│  └─ Docker Daemon (API 및 빌드 관리)
├─ [OCI 런타임 계층]
│  ├─ containerd (컨테이너 수명주기 제어)
│  └─ runc (OCI 표준 프로세스 생성)
└─ [리눅스 커널 격리 계층]
   ├─ Namespaces (PID·NET·MNT 뷰 격리)
   ├─ cgroups (CPU·메모리 자원 제한)
   └─ OverlayFS (CoW 레이어 결합)
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| Docker Client·Daemon | 이미지·컨테이너의 생명주기 관리 |
| containerd·runc | OCI 기반 격리 프로세스 실행 |
| Namespaces | PID·NET·MNT의 가시 영역 격리 |
| cgroups | CPU·메모리·I/O 사용량 제한 |
| OverlayFS | 읽기·쓰기 레이어 병합·재사용 |

#### 한줄 요약
- Namespaces와 cgroups는 하이퍼바이저와 Guest OS가 맡던 격리를 호스트 커널 안에서 대신 세우고, OverlayFS는 이미지 전체 복제를 읽기 레이어 재사용으로 대신하여 배포 단위를 프로세스 수준까지 낮춘다.

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
- 이미지가 레이어로 쌓여 변경된 층만 전송되므로 배포 비용이 이미지 전체 크기가 아니라 변경 범위에 비례하며, 그래서 자주 바뀌는 층을 뒤에 두는 순서 설계가 배포 속도를 좌우한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **가상머신 vs Docker 컨테이너**: 하이퍼바이저 기반 하드웨어 가상화(VM)와 OS 커널 공유 프로세스 격리(컨테이너).

</details>

| 비교 항목 | 가상머신 (Virtual Machine) | Docker 컨테이너 (Container) |
|:---|:---|:---|
| 가상화 대상 계층 | 하드웨어 가상화 (Guest OS 독립 탑재) | OS 커널 가상화 (Host OS 커널 공유) |
| 부팅 및 시작 속도 | OS 부팅 필요로 수 분(Minutes) 소요 | 프로세스 기동 수준으로 수 초(Seconds) 이내 |
| 이미지 용량 크기 | 수 GB ~ 수십 GB (Guest OS 포함) | 수십 MB ~ 수백 MB (경량 의존성만 포함) |
| 보안 격리 수준 | 하이퍼바이저 기반 완벽한 커널 격리 | 동일 커널 공유로 잠재적 취약점 전파 위험 |

#### 한줄 요약
- 완전한 커널 격리는 가상머신, 초고속 경량 배포와 마이크로서비스는 Docker 컨테이너를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Container Escape**: 컨테이너 내부 프로세스가 루트 권한으로 실행될 때 커널 취약점을 악용하여 호스트 OS 제어권을 탈취하는 보안 사고.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 빌드 도구가 이미지에 남아 수 GB로 비대화 | Multi-stage Build 적용 및 Distroless 최소 베이스 이미지 사용 | 이미지 용량 90% 축소 및 배포 가속 |
| Root 권한 실행으로 인한 호스트 커널 탈출 해킹 위험 | Dockerfile 내 `USER nonroot` 명시 및 Rootless 런타임 강제 | 컨테이너 권한 상승 원천 차단 |
| 컨테이너 재시작 시 내부 생성 데이터 유실 | 호스트 볼륨 마운트 (`docker volume` / K8s PersistentVolume) | 영속적 상태 데이터 무손실 보존 |
| 컨테이너의 무제한 메모리 점유로 호스트 OOM 다운 | cgroups 기반 `memory: 2Gi` 및 CPU Limit 리소스 상한 명시 | 노드 안정성 100% 확보 |

#### 한줄 요약
- 멀티 스테이지 빌드, Non-root 실행, 외부 볼륨 마운트, 리소스 상한 설정으로 운영한다.

## Ⅶ. 결론

- 현대 클라우드 네이티브 컴퓨팅, 마이크로서비스 아키텍처(MSA) 및 CI/CD 배포 파이프라인의 가장 지배적인 표준 패키징·실행 단위 기술로 확립되었으며, 실무 구축 시에는 공격 표면을 최소화하는 Multi-stage 빌드 및 Distroless/Alpine 경량 베이스 이미지 채택, 컨테이너 탈출(Container Escape)을 방어하는 Non-root 유저 실행과 Seccomp/AppArmor 프로파일 적용, 리소스 독점을 방어하는 cgroups 메모리/CPU Limit 설정을 결합하여 고속 배포성과 프로덕션 보안성을 동시 보증

#### 한줄 요약
- Docker 컨테이너는 리눅스 커널 격리와 레이어드 불변 이미지를 통해 환경 일치성과 경량 배포를 실현하는 클라우드 네이티브의 핵심 배포 기술이다.
