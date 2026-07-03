---
title: "쿠버네티스 아키텍처 (Kubernetes Architecture)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 173
---

# 📖 【암기용】 개념 완전 이해

> 목적: 쿠버네티스 아키텍처를 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 쿠버네티스 아키텍처는 다수 컨테이너의 배치·복구·확장·설정을 자동으로 관리하는 **컨테이너 오케스트레이션** 구조이며, 그 핵심 동작 방식은 **선언형 API**와 **제어 루프(Reconciliation Loop)**다.
- **왜 필요한가**: 컨테이너는 실행 단위일 뿐이라 배치 위치·장애 복구·롤링 배포·서비스 발견을 스스로 처리하지 않는다. 컨테이너 수가 수십 개를 넘으면 이 조합을 사람이 수동으로 맞추기 어렵다.
- **핵심 직관**: 사용자는 "원하는 최종 상태(Desired State)"만 선언하고, Kubernetes는 "지금 상태(Current State)"를 계속 관찰해 그 차이를 줄여나가는 제어 시스템이다 — 명령을 하나하나 실행시키는 게 아니라 목표를 유지시킨다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 컨테이너 오케스트레이션 | 다수 컨테이너의 배치·복구·확장·설정을 자동으로 관리하는 체계 — 이 아키텍처가 속한 **상위 개념** | 공장의 자동 생산관리 시스템 |
| 선언형 API | "어떻게 할지"가 아니라 "무엇이 되길 원하는지"만 기술하면 시스템이 알아서 그 상태를 만들어내는 방식 | 목적지만 말하면 경로는 알아서 찾는 내비게이션 |
| Control Plane | 클러스터의 두뇌 — 상태를 저장하고 배치·복구를 결정하는 컴포넌트 묶음(API Server·etcd·Scheduler·Controller Manager) | 건물의 관리사무소 |
| Worker Node | 실제 컨테이너(Pod)가 실행되는 서버 | 건물의 각 층 사무실 |
| API Server | 모든 요청이 반드시 거치는 단일 관문. 인증·인가·admission 검증 후 etcd에 기록 | 민원 접수창구 |
| etcd | Key-Value 분산 저장소이자 클러스터의 유일한 상태 저장소(Single Source of Truth) | 마을 등기소의 원본 장부 |
| Scheduler | Pending 상태 Pod를 감지해 어느 Node에 배치할지 결정하는 컴포넌트 | 배치 담당 심사관 |
| Controller Manager | Deployment·ReplicaSet 등 각 객체의 Desired State를 감시하며 Current State를 맞추는 여러 제어 루프의 묶음 | 유지보수팀장 |
| kubelet | Worker Node에 상주하는 에이전트. API Server가 지시한 Pod를 실제로 실행·감시·보고 | 각 층 현장관리자 |
| Container Runtime (CRI) | kubelet의 지시를 받아 실제 컨테이너 프로세스를 뜨고 내리는 엔진(containerd, CRI-O) | 엔진룸 |
| Desired State / Reconciliation Loop | "원하는 상태"와 "현재 상태"의 차이를 반복 관찰해 계속 줄이는 제어 원리 | 설정온도(목표)와 현재온도를 비교하는 온도조절기 |

## 깊이 이해

### 왜 이런 구조가 됐나 (배경)
- 컨테이너(Docker 등)는 프로세스를 격리 실행하는 단위일 뿐, "어느 서버에 놓을지", "죽으면 누가 다시 살릴지", "새 버전을 어떻게 무중단으로 바꿀지"는 스스로 해결하지 못한다.
- Kubernetes는 Google 내부의 대규모 클러스터 관리 시스템 Borg의 운영 경험을 바탕으로 2014년 공개됐고, 이 문제를 "사용자는 목표 상태를 선언하고, 여러 제어 루프가 그 목표에 계속 수렴시킨다"는 방식으로 표준화했다.

### API Server 요청 처리 파이프라인 — 수치로 이해
- `kubectl apply -f deployment.yaml`(replicas=3)을 실행하면 API Server는 ① 인증(누가 요청했나, 인증서/토큰 확인) ② 인가(RBAC — 이 사용자가 Deployment를 만들 권한이 있나) ③ Admission Controller(정책 검증·기본값 주입, 예: resource request가 없으면 LimitRange로 기본값을 채움) 순으로 처리한 뒤 etcd에 최종 기록한다.
- 이때 etcd에 저장된 객체는 resourceVersion이라는 버전 번호를 새로 부여받는다(예: 1024 → 1025). Controller Manager는 이 변화를 폴링이 아니라 **Watch**(변경 시 즉시 통보받는 구독 방식)로 감지하므로 실제 반응 지연은 보통 수십 ms 수준이다.

### etcd와 쿼럼(정족수) — 왜 홀수 대수로 구성하나
- etcd는 Raft 합의 알고리즘으로 여러 노드 간 데이터를 복제한다. 쓰기가 확정되려면 "과반수(정족수)"가 동의해야 한다.
- 노드 3대 구성이면 과반수는 2대이므로 1대까지 장애를 견딘다. 노드 5대 구성이면 과반수는 3대이므로 2대까지 장애를 견딘다.
- 노드 4대는 과반수가 3대가 되어 여전히 1대 장애만 견디는데(3대와 동일한 내결함성) 노드 수만 늘어난다 — 그래서 짝수 구성은 이득이 없고 3 또는 5 같은 홀수를 쓴다.

### Reconciliation Loop — Deployment(replicas=3) 워크드 예제
1. 사용자가 replicas=3 Deployment를 제출 → etcd에 Desired State(3)로 저장.
2. ReplicaSet Controller가 현재 Pod 수(0)와 목표(3)의 차이를 감지 → Pod 3개 생성을 API Server에 요청.
3. Scheduler가 Pending Pod 3개를 각각 Node1, Node2, Node3에 배치(Bind).
4. kubelet이 각 Node에서 Pod를 실행 → Running으로 상태 보고.
5. 이후 Node2가 장애로 다운되면, Controller Manager는 기본값 node-monitor-grace-period(약 40초) 뒤에 Node2를 NotReady로 판정하고 그 안의 Pod를 비정상 처리한다. ReplicaSet Controller는 다시 Current(2) vs Desired(3)의 차이를 감지해 다른 정상 Node에 Pod 1개를 재생성 요청한다. 이 "감지 → 차이 계산 → 조정 요청"의 반복이 Reconciliation Loop다.

### kubelet과 Container Runtime (CRI)
- kubelet은 Docker를 직접 다루지 않는다(1.24부터 dockershim 제거). 대신 CRI(Container Runtime Interface) 표준을 통해 containerd나 CRI-O 같은 런타임에 "이 이미지를 이 스펙으로 띄워라"를 지시하고, 런타임이 다시 runc를 호출해 실제 컨테이너 프로세스를 만든다.

### 비유
- 건물 관리 시스템에서 입주 신청(API Server), 등기 장부(etcd), 방 배정 담당(Scheduler), 유지보수팀(Controller Manager), 각 층 현장관리자(kubelet)가 역할을 나눠 맡는 구조와 같다.

### 흔한 오해·주의점
- Kubernetes는 애플리케이션 코드의 버그를 대신 고쳐주지 않는다. health check(probe), resource request, 보안 정책, rollout 전략을 사용자가 명시해야만 자동 복구·자동 확장이 실제로 작동한다.

## 연결 개념
- Pod 생명주기(174) — 여기서 배치된 Pod가 Pending → Running → Ready로 전이하는 과정
- Pod 스케줄링(175) — Scheduler가 Node를 고르는 세부 알고리즘(Filter-Score-Bind)
- Service/Ingress(176) — kubelet이 실행한 Pod의 IP 변동을 감추는 접근 계층

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Kubernetes 아키텍처는 구성요소 나열이 아니라 선언형 API와 제어 루프가 상태 차이를 수렴시키는 구조로 설명해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Kubernetes는 API Server 중심의 선언형 컨테이너 오케스트레이션 플랫폼임.
> 2. **가치**: Scheduler, Controller, kubelet이 Desired State를 지속 조정해 배포, 복구, 확장을 자동화함.
> 3. **판단 포인트**: 설계 시 control plane HA, etcd 백업, resource request, RBAC, observability를 함께 검토해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 아키텍처 구성 이해 확인 | Control Plane, Worker Node, Add-on | Pod 실행만 설명 |
| 선언형 제어 원리 확인 | Desired State, Reconciliation | 명령형 배포 도구로 오해 |
| 운영 설계 역량 확인 | HA, etcd backup, RBAC, monitoring | 장애 도메인과 보안 통제 누락 |

> 요약: Kubernetes 답안은 제어평면과 워커노드의 역할 분리, 상태 수렴 원리, 운영 통제를 함께 제시해야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: Kubernetes는 컨테이너 오케스트레이션 플랫폼임.
- 배경: MSA와 클라우드 환경에서는 컨테이너 배치, 장애 복구, 서비스 발견, 확장, 설정 관리가 반복된다.
- 필요성: 선언형 API와 컨트롤러 루프로 배치, 복구, 확장, 설정 관리 상태를 지속적으로 조정한다.

---

## Ⅱ. 구조 및 구성요소

```text
User/YAML -> API Server -> etcd
API Server -> Scheduler -> Worker Node
API Server -> Controller Manager -> Desired State 조정
Worker Node -> kubelet -> container runtime -> Pod
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| API Server | 인증, 인가, 객체 저장 관문 | RBAC, Admission |
| etcd | 클러스터 상태 저장 | quorum, snapshot |
| Scheduler | Pod를 Node에 배치 | request, affinity, taint |
| kubelet | 노드의 Pod 실행 상태 관리 | CRI 연동 |

> 요약: Control Plane은 상태 결정을 담당하고 Worker Node는 kubelet과 런타임으로 Pod 실행을 담당함.

---

## Ⅲ. 동작원리 및 흐름도

```text
Manifest 제출 -> API 검증/저장 -> Controller 감지 -> Scheduler 배치 -> kubelet 실행 -> 상태 보고
  / 불일치 발생 -> Controller 재조정
  / 노드 장애 -> 재스케줄링
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | kubectl 또는 CI/CD가 YAML 제출 | schema, admission 통과 |
| 2 | API Server가 etcd에 Desired State 저장 | resourceVersion 생성 |
| 3 | Controller가 필요한 Pod 수 계산 | replica 일치 |
| 4 | Scheduler가 Node 선택 | request 충족, 정책 충족 |
| 5 | kubelet이 Runtime으로 Pod 실행 | Ready 상태, event |

> 요약: Kubernetes는 상태 저장, 감지, 배치, 실행, 보고를 반복해 선언한 상태에 수렴함.

---

## Ⅳ. 특징

| 구분 | 수동 컨테이너 운영 | Kubernetes | 수치/판단 포인트 |
|:---|:---|:---|:---|
| 배포 | 서버별 명령 실행 | Deployment, rollout | 배포 실패율 5% 이하 |
| 복구 | 운영자 개입 | Controller 재생성 | MTTR 10분 이하 |
| 확장 | VM/서버 증설 | HPA, Cluster Autoscaler | CPU 70% 기준 |
| 접근 | 고정 IP 의존 | Service, Ingress | endpoint 자동 갱신 |

> 요약: Kubernetes는 컨테이너 실행보다 상태 기반 운영 자동화와 서비스 추상화에 가치가 있음.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | VM/수동 스크립트 | Control Plane + Worker Node | 컨테이너 50개 이상 |
| 비용/처리 | 서버별 배포 | 선언형 rollout | 배포 주기 일 1회 이상 |
| 운영/위험 | 운영자 의존 복구 | controller 기반 복구 | SLO 99.9% 요구 |

> 요약: 컨테이너 수와 배포 빈도가 커질수록 Kubernetes의 선언형 운영 구조가 필요함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Control Plane 장애 | API Server, etcd 단일 장애 | 3/5 node HA, etcd snapshot | API p99, etcd quorum |
| 자원 경합 | request/limit 미설정 | LimitRange, ResourceQuota | CPU throttling, OOMKilled |
| 권한 과다 | cluster-admin 남용 | RBAC least privilege, audit log | cluster-admin 사용자 수 |

> 요약: Kubernetes 운영 리스크는 제어평면 가용성, 자원 모델, 권한 통제로 관리함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| API 지연 | API Server p99 1초 이하 | apiserver metric |
| 복구 시간 | Pod 재생성 2분 이하 | event, Prometheus |
| 보안 통제 | RBAC audit 위반 0건 | audit log, OPA |

> 요약: 아키텍처 검증은 API 응답, 복구 시간, 권한 감사 지표로 수행함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 제어평면 설계: API Server 3대, etcd 3/5대 quorum, snapshot 주기 1시간 이하로 Control Plane HA 구성
2. 워크로드 표준: request/limit, liveness/readiness probe, PDB, rollout strategy를 기본 템플릿에 포함
3. 운영 통제: RBAC least privilege, audit log 180일 보관, Prometheus/Grafana 기반 SLO dashboard 구축

**결론 (2줄):**
- 기술사 판단: Kubernetes는 컨테이너 실행 도구가 아니라 선언형 상태 제어 플랫폼으로 도입해야 함
- 향후 방향: GitOps, Service Mesh, Policy as Code와 결합해 플랫폼 엔지니어링의 실행 기반이 됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "쿠버네티스 아키텍처를 설명하시오" | 선언형 상태 수렴 흐름 | Control Plane/Worker Node 역할 |
| 요구사항 명시형 | "설계하시오", "운영 방안을 제시하시오" | HA, 배포, 복구, 관측 흐름 | SLO, RBAC, etcd 백업 기준 |

> 요약: 설명형은 구성과 원리, 설계형은 HA와 운영 통제 중심으로 전환함.
