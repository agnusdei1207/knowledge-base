---
sidebar:
  order: 152
  label: "152. 쿠버네티스 아키텍처 (Kubernetes Architecture)"
  badge:
    text: "기출 • 85%"
    variant: note
title: "쿠버네티스 아키텍처 (Kubernetes Architecture)"
date: "2026-08-06T23:27:50+09:00"
tags: ["notes-software"]
weight: 152
extra:
  question_no: "152"
  source_status: "기출"
  source_history: "122회, 135회, 137회"
  priority: 85
  priority_note: "제어면과 작업 노드의 역할 및 상태 조정 원리 반복 출제"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Kubernetes Architecture (쿠버네티스 아키텍처)**: 클러스터의 상태를 관리하고 스케줄링하는 마스터 제어면(Control Plane)과 실제 컨테이너 파드(Pod)를 띄워 가동하는 워커 노드(Worker Node)로 분리된 컨테이너 오케스트레이션 아키텍처.
- **Control Plane (마스터/제어면)**: kube-apiserver, etcd, kube-scheduler, kube-controller-manager로 구성된 클러스터의 뇌(Brain) 역할을 담당하는 관리 서버.
- **Worker Node (작업 노드)**: kubelet, kube-proxy, Container Runtime(containerd)으로 구성된 실제 수백 개의 컨테이너 워크로드가 실행되는 컴퓨팅 서버.

</details>

- 정의/개념: 컨테이너화된 애플리케이션의 분산 배포, 수평 확장, 자가 치유(Self-healing), 롤링 업그레이드를 자동화하기 위해 Control Plane과 Worker Node로 물리적/논리적 역할을 분리한 아키텍처인 **Kubernetes Architecture**
- 배경/필요성: 수백~수천 개의 Docker 컨테이너를 수동 배포/관리하는 한계 극복, 선언적 API(Declarative API) 기반 100% 자가 치유 오케스트레이션 요구성

#### 한줄 요약

- 운영자가 파드 수만 선언하면 제어면은 빈자리를 찾아 배치하고 장애로 사라진 파드를 다시 만들기 때문에 목표와 현실의 차이를 자동으로 좁힐 수 있다.

## Ⅱ. 특징 (쿠버네티스 3대 핵심 운용 메커니즘)

<details><summary>핵심 용어</summary>

- **Reconciliation Loop (조정 루프)**: `Desired State (목표 상태)`와 `Current State (현재 상태)`를 매초 비교하여 일치시키는 지속적 자가 치유 메커니즘.

</details>

- **Control Plane & Worker Node Separation (지능형 제어와 실제 워크로드 실행의 완전 분리)**
- **Declarative State Management (YAML 명세서 기반 Desired State 선언 및 Reconciliation Loop)**
- **Self-Healing & Auto-Recovery (Pod 다운 시 타 노드에 자동 재생성 및 롤링 배포)**

#### 한줄 요약

- 실행 순서를 일일이 명령하는 대신 원하는 결과를 적어 두면 여러 제어기가 각자 맡은 차이를 계속 바로잡는 방식이다.

## Ⅲ. 구조 및 구성요소 (Control Plane vs Worker Node 8대 핵심 컴포넌트)

<details><summary>핵심 용어</summary>

- **kube-apiserver & etcd**: kube-apiserver는 클러스터의 유일한 REST API 입구, etcd는 클러스터의 모든 상태값을 보존하는 분산 Key-Value DB.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   Kubernetes Cluster Architecture                      │
├────────────────────────────────────────────────────────────────────────┤
│ CONTROL PLANE (Master Node)                                            │
│  [kube-apiserver] ──► [etcd DB]                                        │
│  [kube-scheduler] ──► [kube-controller-manager]                        │
├────────────────────────────────────────────────────────────────────────┤
│ WORKER NODE (Node 1, Node 2...)                                        │
│  [kubelet] ──► [kube-proxy] ──► [Container Runtime (containerd)]       │
│  └─► Pod 1 (App), Pod 2 (App)                                          │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: Control Plane의 API 서버가 명령을 수신하여 etcd에 기재 후 Worker Node의 kubelet으로 하달되어 containerd가 Pod를 구동하는 구조.

| 파트 영역 | 핵심 구성요소 | 역할 및 실무 기술 메커니즘 |
|:---|:---|:---|
| **Control Plane**| **kube-apiserver** | **클러스터의 유일한 통신 게이트웨이 (REST API 받음)** |
| **Control Plane**| **etcd** | **클러스터 전체 상태(Desired State) 저장 고가용성 DB**|
| **Control Plane**| **kube-scheduler** | **Pod를 어느 Worker Node에 배치할지 최적 선택**|
| **Control Plane**| **kube-controller-manager**| **Reconciliation Loop 작동 (Replica, Node 컨트롤러)**|
| **Worker Node** | **kubelet** | **Node마다 설치된 에이전트, Pod 생성/상태 API 보고** |
| **Worker Node** | **kube-proxy** | **Node의 네트워크 라우팅 및 iptables/IPVS 서비스 처리**|
| **Worker Node** | **Container Runtime**| **실제 Pod 내부 컨테이너를 가동하는 runc / containerd**|

#### 한줄 요약

- API 서버가 주문을 받고 장부에 기록하면 스케줄러가 작업 장소를 정하고 kubelet과 런타임이 현장에서 파드를 실행한다.

## Ⅳ. 흐름도 (kubectl apply ~ Pod Running 5단계 렌더링 흐름)

<details><summary>핵심 용어</summary>

- **Pod Provisioning Flow**: `kubectl apply` YAML 전달 $\rightarrow$ apiserver validation $\rightarrow$ etcd write $\rightarrow$ scheduler node selection $\rightarrow$ kubelet pod run.

</details>

```text
[User: kubectl apply -f pod.yaml] ──► [kube-apiserver] ──► [etcd Store]
                                             │
                                             ▼
[Pod Running Status Update] ◄── [kubelet & containerd] ◄── [kube-scheduler (Node Pick)]
```

### 동작 원리

1. **API Receive & Etcd Write**: 유저가 YAML 제출 시 `kube-apiserver`가 검증 후 `etcd`에 `Pending` 상태 저장.
2. **Scheduling**: `kube-scheduler`가 가장 여유로운 Node 2를 선택하여 `kube-apiserver`에 갱신.
3. **Kubelet Execution**: Node 2의 `kubelet`이 이를 감지하여 `containerd` 런타임에 Pod 생성 명령 후 가동 (**K8s Architecture 완결**).

#### 한줄 요약

- 배포 객체를 제출하면 제어기가 부족한 파드를 만들고 스케줄러가 노드를 정한 뒤 kubelet이 런타임에 실행을 맡기는 한 흐름으로 이어진다.

## Ⅴ. 종류 및 비교 (Control Plane DB: etcd 대 K3s SQLite)

<details><summary>핵심 용어</summary>

- **etcd Raft Consensus**: etcd는 분산 합의 알고리즘(Raft)을 사용하여 3대 이상 홀수(3, 5, 7)로 구성해야 쿼럼(Quorum) 유지 가능.

</details>

| 비교 항목 | Production Kubernetes (etcd) | Lightweight K3s (SQLite/kine) |
|:---|:---|:---|
| **Control Plane DB**| **etcd (Raft 기반 분산 Key-Value DB)** | **SQLite / Embedded MySQL (kine 엔진)** |
| **추천 배치 환경** | **대규모 엔터프라이즈, 금융 Cloud** | **Edge computing, IoT, 개발용 로컬** |
| **최소 노드 구성** | 3대 이상 홀수 마스터 노드 (HA) | **단일 1대 노드로 통째 구동 가능** |
| **메모리 오버헤드**| 수 GB 이상의 Heavy한 마스터 메모리 | **512MB 이하 초경량 오버헤드** |

#### 한줄 요약

- 제어면은 어디서 무엇을 실행할지 결정하고 작업 노드는 받은 명세대로 컨테이너를 움직인다는 경계로 구분하면 구성요소가 섞이지 않는다.

## Ⅵ. 실무 고려사항 및 대책 (K8s 아키텍처 3대 실무 지침)

<details><summary>핵심 용어</summary>

- **etcd Quorum Failure**: etcd 노드 3대 중 2대가 동시 다운되면 쿼럼(과반수)이 깨져 클러스터 전체가 읽기 전용 락에 걸리는 참사.

</details>

| 3대 K8s 참사 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. etcd Quorum Loss** | etcd 3대 중 2대 동시 다운으로 락 걸림| **etcd 3/5대 Multi-AZ 분산 및 주기적 Snapshot**|
| **2. apiserver Bottleneck**| 수만 개 Pod 쿼리로 apiserver 다운 | **apiserver 수평 스케일아웃 및 캐싱 레이어 튜닝**|
| **3. Kubelet Memory OOM** | Node 메모리가 꽉 차서 kubelet 먹통됨 | **kubelet 용으로 Memory 1GB 예약 (system-reserved)**|

> 사례: **카카오 / 당근마켓 / 쿠팡 EKS / GKE 기반 대규모 마스터 노드 HA 멀티 클러스터 운용**

#### 한줄 요약

- 제어면만 이중화해도 요청량이 틀리거나 배치 제약이 충돌하면 파드가 멈추므로 상태 저장, 권한, 용량, 배치 조건을 함께 점검해야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **K8s Architecture 수립 기준(Kubernetes Standards)**: Control Plane 3대 Multi-AZ, etcd Snapshot, kubelet System-Reserved 메모리 확보 및 EKS/GKE 관리형 서비스 도입성에 의거한 체계.

</details>

- **K8s Architecture 수립 기준**에 따라 전사 클러스터 구축 시 **Kubernetes Architecture & Managed K8s (EKS/GKE)** 필수 적용

#### 한줄 요약

- 관리 기능이 멈춰도 기존 파드는 잠시 동작할 수 있지만 새 배치와 복구는 중단되므로 요구 복구 시간에 맞춰 제어면과 노드를 각각 설계해야 한다.
