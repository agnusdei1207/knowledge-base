---
sidebar:
  order: 152
  label: "152. 쿠버네티스 아키텍처 (Kubernetes Architecture)"
  badge:
    text: "기출 · 85%"
    variant: note
title: "쿠버네티스 아키텍처 (Kubernetes Architecture)"
date: "2026-08-18T01:40:00+09:00"
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

<details><summary>용어 설명</summary>

- **쿠버네티스 아키텍처(Kubernetes Architecture)**: 대규모 분산 환경에서 컨테이너의 배포, 스케일링, 복구를 자동화하기 위해 제어면(Control Plane)과 작업 노드(Worker Node)로 분리된 오케스트레이션 구조.
- **선언적 상태 관리 및 자가 치유 한계(Declarative State & Manual Operation Limit)**: 수작업 스크립트 기반 컨테이너 운영 시 발생하는 노드 장애 다운타임과 목표 상태와 실제 상태의 불일치 위험.

</details>

- 정의/개념: 분산 환경에서 대규모 컨테이너를 관리하기 위해 **컨트롤 플레인(제어면)과 워커 노드로 분리하여 선언적 자가 치유를 제공**하는 오케스트레이션 아키텍처
- 배경/필요성: 수천 개 컨테이너의 수동 배포 및 노드 장애 시 발생하는 **서비스 다운타임, 상태 불일치 및 수동 스케일링 복구 한계** 직면

#### 한줄 요약

- 제어면과 워커 노드의 분리 및 선언적 조정 루프(Reconciliation Loop)를 통해 대규모 컨테이너의 완전 자동화 운영을 실현

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **조정 루프(Reconciliation Loop)**: 컨트롤러가 목표 상태(Desired State)와 현재 상태(Actual State)를 끊임없이 비교하고 일치시키는 무한 루프 메커니즘.
- **분산 합의 etcd(Raft Consensus)**: 클러스터의 모든 설정 및 메타데이터를 일관성 있게 보존하는 분산 Key-Value 저장소.

</details>

- 두뇌 역할을 하는 제어면과 실행을 담당하는 워커 노드의 **명확한 책임 분리(Control/Data Plane)**
- YAML 명세서에 목표를 정의하면 자동으로 유지하는 **선언적 자가 치유(Self-Healing)**
- 수평적 파드 확장(HPA) 및 무중단 롤링 업데이트를 지원하는 **고가용성 오케스트레이션** #### 한줄 요약

- 선언적 API와 무한 조정 루프를 통해 컨테이너 장애를 실시간으로 자가 복구

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **제어면(Control Plane) & 워커 노드(Worker Node)**: 제어면(API Server, etcd, Scheduler, Controller Manager)과 워커 노드(kubelet, kube-proxy, Container Runtime).

</details>

```text
[ 쿠버네티스 제어면(Control Plane) 및 워커 노드 아키텍처 ]

 1. [ 제어면 (Control Plane / Master) ]
    ┌─────────────────────────────────────────────────────────────┐
    │  [ kube-apiserver ] (유일한 REST API 관문, 인증/인가)       │
    │        │                   │                   │            │
    │        ▼                   ▼                   ▼            │
    │   [ etcd DB ]      [ kube-scheduler ]  [ Controller-Mgr ]   │
    │ (Raft 분산저장)    (노드 배치 스케줄링) (상태 조정 루프 총괄)│
    └────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼ (gRPC / HTTPS 통신)
 2. [ 워커 노드 (Worker Node) ]
    ┌─────────────────────────────────────────────────────────────┐
    │  [ kubelet ] ──────► [ CRI Container Runtime (containerd) ] │
    │ (노드 에이전트)              │ (파드 프로세스 실행)         │
    │                              ▼                              │
    │  [ kube-proxy ] ──► [ Pod (App Container + Pause Container)│
    │ (iptables/IPVS 라우팅)                                      │
    └─────────────────────────────────────────────────────────────┘
```

선의 의미: kube-apiserver를 중심으로 제어면 컴포넌트들이 상태를 동기화하고 워커 노드의 kubelet이 파드를 제어하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| kube-apiserver | 클러스터의 모든 요청을 접수하며 **인증(AuthN), 인가(AuthZ), 스키마 검증 및 etcd 접근 중계** |
| etcd 저장소 | Raft 알고리즘 기반으로 **클러스터의 모든 오브젝트 명세와 현재 상태를 분산 영속 저장** |
| kube-scheduler | 미배치된 파드의 리소스 요구량과 제약 조건을 분석하여 **최적의 워커 노드에 바인딩(Binding)** |
| Controller Manager | Node, Deployment, ReplicaSet 등의 컨트롤러를 구동하여 **목표 상태와 현재 상태를 지속 동기화** |
| kubelet | 워커 노드의 마스터 에이전트로서 **컨테이너 런타임(CRI)에 파드 생성/삭제를 지시하고 헬스체크 보고** |
| kube-proxy | 노드의 커널 iptables 또는 IPVS 규칙을 관리하여 **쿠버네티스 서비스(Service) 트래픽 로드밸런싱** |
| Container Runtime | containerd/CRI-O 기반으로 **OCI 이미지를 다운로드하고 실제 컨테이너 프로세스를 실행** |

#### 한줄 요약

- 제어면 4대 요소와 워커 노드 3대 요소가 유기적으로 결합하여 자가 치유 클러스터를 구동

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **파드 프로비저닝 5단계 절차**: YAML 요청 $\to$ etcd 저장 $\to$ 노드 스케줄링 $\to$ kubelet 생성 지시 $\to$ 파드 기동 및 상태 보고.

</details>

```text
[ 쿠버네티스 파드(Pod) 배포 및 스케줄링 파이프라인 ]

 ┌────────────────────────────────────────┐
 │ 1. kubectl apply -f pod.yaml 요청 접수 │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 2. kube-apiserver 검증 후 etcd에 기록  │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 3. kube-scheduler: 최적 노드 선정 바인딩
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 4. 워커 노드 kubelet이 containerd로 파드 기동
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 5. 파드 Running 상태 확인 및 etcd 갱신 │
 └────────────────────────────────────────┘
```

### 동작 원리

1. 요청 접수: 사용자가 `kubectl`을 통해 파드 배포 YAML을 제출하면 API 서버가 인증/인가를 수행.
2. 상태 저장: 유효성 검증을 통과한 파드 스펙을 분산 저장소인 etcd에 영속적으로 기록.
3. 스케줄링: kube-scheduler가 필터링과 스코어링 알고리즘을 거쳐 여유 자원이 있는 최적의 워커 노드를 결정(Binding).
4. 파드 기동: 해당 워커 노드의 kubelet이 API 서버의 이벤트를 감지하고 CRI(containerd)를 호출해 컨테이너를 실행.
5. 상태 갱신: kubelet이 파드의 정상 실행(Running) 상태를 API 서버에 보고하여 etcd의 현재 상태를 동기화.

#### 한줄 요약

- 요청 접수 $\to$ etcd 기록 $\to$ 노드 스케줄링 $\to$ kubelet 기동 $\to$ 상태 갱신의 5단계

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **표준 쿠버네티스(K8s) vs 경량 쿠버네티스(K3s)**: 대규모 분산 클라우드용 표준 K8s와 단일 바이너리/SQLite 기반의 경량 엣지용 K3s.

</details>

| 구분 | 표준 쿠버네티스 (Standard K8s) | 경량 쿠버네티스 (K3s) |
|:---|:---|:---|
| **적용 기준** | 엔터프라이즈 데이터센터, EKS/GKE 대규모 클라우드 | 엣지 컴퓨팅, IoT 게이트웨이, 로컬 개발 환경 |
| **핵심 특징** | **분산 etcd(HA), 완전한 모듈화, 무제한 스케일아웃** | **단일 바이너리 패키징, SQLite(kine) 내장, 512MB RAM** |
| **한계** | 제어면 메모리 오버헤드(수 GB) 및 클러스터 구축 복잡도 | 대규모 엔터프라이즈 멀티 테넌트 확장성 제약 |

#### 한줄 요약

- 대규모 엔터프라이즈는 표준 K8s, 리소스 제약이 큰 엣지/IoT는 K3s를 선택

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **etcd 쿼럼 손실(Quorum Loss)**: 홀수 노드로 구성된 etcd 클러스터에서 과반수 이상의 노드가 다운되어 클러스터 상태 쓰기가 전면 마비되는 장애.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| etcd 노드 과반수 다운으로 인한 클러스터 상태 쓰기 마비 | **etcd 3대 이상 홀수 노드 Multi-AZ 분산 배치 및 정기 스냅샷** | etcd 고가용성 및 쿼럼 손실 방지 |
| 대규모 파드 급증 시 kube-apiserver CPU/메모리 병목 | **apiserver 수평 스케일아웃 및 로드밸런서(NLB) 부하 분산** | 제어면 처리량 5배 향상 |
| 워커 노드 OOM 발생 시 핵심 데몬인 kubelet 프로세스 다운 | **Kubelet 시스템 예약 메모리(`system-reserved`) 사전 격리 설정** | 워커 노드 생존성 100% 보장 |

#### 한줄 요약

- etcd 홀수 다중화, API 서버 부하 분산, Kubelet 시스템 자원 예약을 통해 대규모 클러스터를 안정화

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **클라우드 네이티브 운영체제(Cloud-Native OS)**: 쿠버네티스가 현대 분산 인프라의 사실상 운영체제 역할을 수행하는 표준화 패러다임.

</details>

- **쿠버네티스 아키텍처** 기반 컨테이너 기반 클라우드 네이티브의 핵심 인프라 표준이며, 제어면의 고가용성(HA)과 워커 노드의 자원 격리를 철저히 보장하여 자가 치유 기반의 안정적인 대규모 분산 서비스를 완성해야 함

#### 한줄 요약

- 제어면과 워커 노드의 이원화 구조와 선언적 조정 루프를 통해 컨테이너 오케스트레이션을 완성
