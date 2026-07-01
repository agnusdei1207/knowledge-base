---
title: "컨테이너 런타임 - containerd·CRI-O (Container Runtime)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 172
---

# 📖 【암기용】 개념 완전 이해

> 목적: 컨테이너 런타임을 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 컨테이너 이미지를 내려받고 프로세스 격리, 파일시스템, 네트워크, 자원 제한을 적용해 실행하는 계층
- **왜 필요한가**: Kubernetes는 Pod를 선언하지만 실제 프로세스를 만들고 cgroup과 namespace를 적용하는 구성요소가 별도로 필요하다.
- **핵심 직관**: Kubernetes가 배차 명령을 내리면 런타임은 실제 차량 문을 열고 승객을 태워 출발시키는 운행 담당자이다.

## 깊이 이해
- **배경·문제의식**: Docker는 개발자 경험을 통합했지만 오케스트레이션에서는 이미지 pull, container create, start, stop 같은 실행 기능만 필요하다. Kubernetes는 CRI(Container Runtime Interface)로 kubelet과 런타임을 분리했다.
- **작동 원리**: kubelet이 CRI gRPC로 Pod sandbox와 container 생성을 요청하면 containerd 또는 CRI-O가 OCI runtime인 runc를 호출해 Linux namespace, cgroup, mount를 적용한다.
- **비유**: 레스토랑 주문서가 Kubernetes manifest라면, 런타임은 주방에서 실제 재료를 꺼내 요리하고 접시에 담는 역할이다.
- **구체 예시**: kubelet -> containerd -> runc 경로에서 image pull, snapshot mount, container start가 수행되며, cgroup v2로 CPU 500m, Memory 512Mi 제한을 적용한다.
- **흔한 오해·주의점**: containerd와 CRI-O는 Docker CLI 대체가 아니라 Kubernetes 노드에서 컨테이너 실행을 담당하는 런타임 계층이다.

## 연결 개념
- OCI Image/Runtime - 이미지 형식과 실행 표준
- CRI - kubelet과 런타임 사이 gRPC 인터페이스
- runc - Linux 커널 기능을 사용해 컨테이너 프로세스 생성

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 런타임 답안은 Docker 명령어 설명이 아니라 CRI, OCI, kubelet, containerd/CRI-O, runc의 경계로 써야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 컨테이너 런타임은 OCI 이미지를 받아 Linux 격리 기능으로 컨테이너 프로세스를 실행하는 노드 계층임.
> 2. **가치**: CRI 표준으로 Kubernetes와 런타임을 분리해 containerd, CRI-O 등 구현체 교체가 가능함.
> 3. **판단 포인트**: 선택 기준은 Kubernetes 적합성, 보안 프로파일, 이미지 처리, 운영 생태계, 노드 관측성임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 컨테이너 실행 계층 이해 확인 | kubelet, CRI, containerd/CRI-O, runc | Docker와 런타임을 동일시 |
| 표준 인터페이스 이해 확인 | CRI, OCI Image, OCI Runtime | Kubernetes 제어평면만 설명 |
| 운영 선택 판단 확인 | 보안 설정, 노드 장애, 이미지 pull | cgroup/namespace 누락 |

> 요약: 런타임 문제는 컨테이너 실행 경로와 표준 경계를 연결해야 점수를 확보함.

---

## Ⅰ. 개요 및 필요성

컨테이너 런타임은 이미지를 프로세스로 실행하는 계층임. Kubernetes는 선언과 스케줄링을 담당하지만, 노드에서 실제 컨테이너를 생성하려면 CRI 호환 런타임이 필요하다. 런타임 이해는 장애 분석, 보안 통제, 노드 표준화의 기준이 된다.

---

## Ⅱ. 구조 및 구성요소

```text
Kubelet -> CRI gRPC -> containerd/CRI-O -> OCI Runtime runc -> Linux Kernel
  / image pull
  / sandbox create
  / container start
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| kubelet | PodSpec를 런타임 요청으로 변환 | CRI client |
| CRI | RunPodSandbox, CreateContainer, StartContainer | gRPC API |
| containerd/CRI-O | 이미지, snapshot, 컨테이너 생명주기 | Kubernetes 노드 런타임 |
| runc | namespace, cgroup, mount 적용 | OCI runtime |

> 요약: 런타임 구조는 kubelet 요청을 CRI와 OCI runtime으로 연결해 커널 격리 기능을 적용함.

---

## Ⅲ. 동작원리 및 흐름도

```text
PodSpec 수신 -> 이미지 확인 -> Pod sandbox 생성 -> 컨테이너 생성 -> 프로세스 시작 -> 상태 보고
  / 실패 시 ImagePullBackOff
  / 종료 시 ExitCode 보고
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | kubelet이 PodSpec을 CRI 요청으로 변환 | CRI socket 연결 |
| 2 | registry에서 OCI image pull | digest 검증, pull latency |
| 3 | sandbox와 network namespace 생성 | pause container 상태 |
| 4 | runc가 cgroup, mount, seccomp 적용 | CPU/Memory limit 반영 |
| 5 | 컨테이너 상태를 kubelet에 보고 | Ready, ExitCode, logs |

> 요약: 런타임은 이미지 확보부터 커널 격리 적용, 상태 보고까지 노드 실행 전 과정을 담당함.

---

## Ⅳ. 특징

| 구분 | Docker 중심 | containerd/CRI-O | 수치/판단 포인트 |
|:---|:---|:---|:---|
| 인터페이스 | Docker API | CRI gRPC | kubelet 연동 |
| 범위 | 빌드, 실행, CLI | 실행 중심 | 노드 구성 단순화 |
| 표준 | Docker image | OCI image/runtime | registry 호환 |
| 운영 | 개발 도구 포함 | Kubernetes 친화 구성 | 노드 장애 범위 |

> 요약: Kubernetes 노드에서는 개발자 CLI보다 CRI 호환성과 OCI 표준 준수가 선택 기준임.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Docker Engine 의존 | containerd/CRI-O 직접 연동 | Kubernetes 표준 노드 |
| 비용/처리 | daemon 기능 범위 큼 | 실행 기능 집중 | 노드 부하, pull latency |
| 운영/위험 | 도구 통합 | 런타임 경계 명확 | 장애 분석과 패치 책임 |

> 요약: 운영 클러스터는 CRI 호환 런타임을 표준화하고 개발 빌드 도구와 실행 계층을 분리해야 함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| ImagePull 지연 | registry 병목, 큰 이미지 | registry mirror, image pre-pull | pull p95 30초 이하 |
| 런타임 장애 | socket 오류, shim 누수 | node drain, runtime restart runbook | NotReady 노드 수 |
| 권한 과다 | privileged container | seccomp, AppArmor, Pod Security | privileged 0건 |

> 요약: 런타임 리스크는 이미지 공급, 노드 상태, 권한 통제 세 축으로 관리함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 시작 시간 | container start p95 5초 이하 | kubelet event |
| 이미지 보안 | critical CVE 0건 | Trivy, registry scan |
| 노드 상태 | RuntimeReady 99.9% | kubelet metric |

> 요약: 런타임 운영 품질은 시작 시간, 이미지 취약점, RuntimeReady 지표로 검증함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 런타임 표준화: Kubernetes 노드는 containerd 또는 CRI-O 중 1종으로 표준화하고 CRI socket 경로를 IaC로 고정
2. 이미지 공급 통제: private registry, digest pinning, image scan critical 0건 정책을 admission 단계에 연결
3. 장애 대응: ImagePullBackOff, CrashLoopBackOff, RuntimeReady false에 대한 node drain과 runtime restart runbook 작성

**결론 (2줄):**
- 기술사 판단: Kubernetes 운영 환경은 CRI 호환 런타임과 OCI 표준을 기준으로 선택해야 함
- 향후 방향: cgroup v2, rootless container, sandbox runtime과 결합해 노드 실행 경계가 세분화됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "컨테이너 런타임을 설명하시오" | PodSpec에서 프로세스 시작까지 실행 흐름 | Docker, containerd, CRI-O 비교 |
| 요구사항 명시형 | "선택 기준을 제시하시오", "장애 대응 방안을 설명하시오" | 이미지 pull, sandbox, runc 단계별 장애 지점 | CRI 표준, 보안 프로파일, 운영 지표 |

> 요약: 설명형은 실행 계층, 요구사항형은 런타임 선택과 장애 대응 중심으로 전환함.
