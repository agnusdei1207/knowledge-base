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
- **개요**: **CRI(Container Runtime Interface)** 표준을 통해 쿠버네티스 **kubelet**과, 실제 컨테이너 프로세스를 만드는 **컨테이너 런타임** 계층을 연결하는 구조를 가리킨다 — containerd·CRI-O가 대표 구현체다.
- **왜 필요한가**: Kubernetes는 "이런 Pod를 띄워라"라고 선언만 할 뿐, 실제로 프로세스를 만들고 namespace·cgroup을 적용하는 일은 별도 구성요소가 해야 한다. 이 실행 담당 계층이 없으면 선언은 선언으로 그친다.
- **핵심 직관**: Kubernetes가 "이런 손님을 태운 차를 준비하라"는 배차 명령이라면, 런타임은 실제 차 문을 열고 승객을 태워 출발시키는 운행 담당자다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| CRI(Container Runtime Interface) | kubelet과 런타임 구현체를 분리하는 gRPC 표준 인터페이스 — 이 개념의 핵심 상위 표준 | 전기 콘센트 규격(어떤 제조사 플러그든 꽂히게 함) |
| OCI(Open Container Initiative) | 이미지 형식(Image Spec)과 실행 방식(Runtime Spec)을 정한 업계 공통 규격 | 만국 공통 도량형 |
| kubelet | 각 노드에서 PodSpec을 해석해 CRI 요청으로 바꾸는 에이전트 | 배차 지시를 받는 운행 관리자 |
| containerd | Docker에서 분리돼 CNCF에 기부된 범용 CRI 런타임 구현체 | 종합 운행 대행사 |
| CRI-O | Kubernetes 전용으로 처음부터 설계된 경량 CRI 런타임 구현체 | 택시 회사 전용 배차 시스템 |
| runc | OCI Runtime Spec의 기준 구현체 — 실제 격리 프로세스를 만드는 도구 | 실제로 차 시동을 걸고 문을 여는 기사 |
| shim | 컨테이너 프로세스를 감독하며 runc가 종료돼도 계속 살아있는 중간 프로세스 | 기사가 내린 뒤에도 승객을 지켜보는 보조 요원 |
| sandbox(pause 컨테이너) | Pod 안 여러 컨테이너가 네트워크 namespace를 공유하도록 붙잡아두는 최소 프로세스 | 여러 승객이 함께 탈 차체(껍데기)만 먼저 세워둠 |
| dockershim | 과거 kubelet에 내장돼 있던 Docker 전용 연결 코드(현재는 제거됨) | 예전에 쓰던 특정 회사 전용 어댑터 |

## 깊이 이해

### 배경 — Docker 중심에서 CRI 표준으로
- Kubernetes 초기(2014~2016)에는 Docker Engine 전용으로 설계되어 kubelet 안에 Docker를 직접 호출하는 dockershim 코드가 내장돼 있었다. 하지만 Docker Engine은 컨테이너 실행 외에 이미지 빌드, CLI, 네트워크 관리까지 포함한 무거운 데몬이라, 오케스트레이션 입장에서는 불필요한 기능이 많았다.
- 그래서 2016년 Kubernetes 1.5에서 **CRI(Container Runtime Interface)**라는 gRPC 표준을 도입해 kubelet과 런타임 구현체를 분리했다. 이후 2022년 Kubernetes 1.24에서 내장 dockershim이 완전히 제거되어, 이제는 containerd나 CRI-O처럼 CRI를 직접 구현한 런타임만 노드에서 쓸 수 있다.

### CRI 실행 흐름 — 단계로 이해
- kubelet이 PodSpec을 해석해 CRI gRPC 호출(`RunPodSandbox`, `CreateContainer`, `StartContainer`)을 런타임에 보낸다.
- containerd(또는 CRI-O)가 이 요청을 받아 ① registry에서 OCI 이미지를 pull하고, ② pause 컨테이너로 sandbox(네트워크 namespace의 기준점)를 먼저 만들고, ③ 실제 컨테이너는 `containerd-shim`을 통해 OCI Runtime Spec을 만족하는 `runc`를 호출한다.
- 하나의 Pod 안에 컨테이너가 여러 개 있으면(사이드카 패턴 등) 모두 같은 sandbox의 네트워크 namespace를 공유한다 — 그래서 Pod 안의 컨테이너들은 `localhost`로 서로 통신할 수 있다.

### runc 작동 원리 — 커널 관점에서 이해
- `runc`는 Linux의 `clone()` 시스템콜에 `CLONE_NEWPID`, `CLONE_NEWNET` 등 namespace 플래그를 넘겨 격리된 프로세스를 만들고, cgroup 파일시스템에 CPU·메모리 제한 값을 쓴 뒤(예: cgroup v2 기준 CPU 500m는 `cpu.max`에 `50000 100000`으로 기록, Memory 512Mi는 `memory.max`에 `536870912` 바이트로 기록) `execve()`로 실제 애플리케이션 프로세스를 실행한다.
- `runc`는 이 작업을 마치면 곧바로 종료된다 — 오래 떠 있는 데몬이 아니라 "한 번 실행되고 사라지는" 도구다. 그래서 만들어진 컨테이너 프로세스가 부모 없이 남지 않도록 `shim` 프로세스가 계속 붙어서 표준출력·종료 코드를 감독하고 kubelet에 상태를 보고한다.

### containerd vs CRI-O — 언제 무엇을 쓰나 (판별 원리)
- **containerd**는 원래 Docker Engine 내부의 실행 엔진을 떼어내 CNCF에 기부한 것으로, 이미지 관리·스토리지 스냅샷 기능까지 포함해 범용성이 넓다(Docker Desktop과 Kubernetes 양쪽에서 쓰인다).
- **CRI-O**는 Red Hat이 Kubernetes 전용으로 처음부터 설계해 CRI·OCI 표준만 최소로 구현한 경량 런타임이다(OpenShift 기본 런타임).
- 판별 기준: 기존 Docker 생태계 도구·워크플로를 그대로 쓰고 싶다면 containerd, Kubernetes에만 특화된 최소 구성과 좁은 공격 표면을 원한다면 CRI-O를 선택한다.

### 비유와 흔한 오해
- **비유**: kubelet이 "이런 방과 가구를 갖춘 컨테이너를 만들어달라"는 주문서(PodSpec)를 CRI라는 공통 양식으로 넘기면, containerd/CRI-O는 이 주문서를 받아 재료(이미지)를 창고(registry)에서 꺼내오는 총괄 매니저이고, runc는 그 재료로 실제 벽(namespace)을 세우고 전기 용량(cgroup)을 배정하는 시공팀이다. 시공이 끝나면 시공팀(runc)은 철수하고, 완성된 방(컨테이너 프로세스)만 남아 감독자(shim)가 지켜본다.
- **오해**: containerd·CRI-O는 "Docker CLI의 대체품"이 아니다. 사용자가 직접 명령어를 치는 도구가 아니라 kubelet이 내부적으로 호출하는 실행 계층이며, 사람은 보통 `crictl` 같은 저수준 디버깅 도구로만 직접 접한다.

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

- 개요: 컨테이너 런타임은 이미지를 프로세스로 실행하는 계층임.
- 배경: Kubernetes는 선언과 스케줄링을 담당하지만, 노드에서 실제 컨테이너를 생성하려면 CRI 호환 런타임이 필요하다.
- 필요성: containerd, CRI-O, runc 계층을 기준으로 장애 분석, 보안 통제, 노드 표준화를 수행한다.

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

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
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
