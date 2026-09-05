---
sidebar:
  order: 152
  label: "152. 쿠버네티스 아키텍처"
  badge:
    text: "기출 · 85%"
    variant: note
title: "쿠버네티스 아키텍처 (Kubernetes Architecture)"
date: "2026-08-31T10:48:00+09:00"
tags:
  - "notes-software"
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

- **쿠버네티스 아키텍처**: 클러스터 전체를 관할하는 Control Plane(제어면)과 실제 컨테이너 Pod를 실행하는 Worker Node(작업 노드)로 분리된 분산 구조.
- **선언적 상태 관리(Declarative State)**: 사용자가 YAML에 희망 상태(Desired State)를 선언하면 컨트롤러가 현재 상태를 자동으로 맞추는 메커니즘.

</details>

- 정의/개념: 분산 환경에서 대규모 컨테이너의 배포, 스케일링, 복구를 위해 컨트롤 플레인과 워커 노드로 이원화하여 선언적 자가 치유를 제공하는 오케스트레이션 아키텍처
- 배경/필요성: 대규모 분산 환경에서 컨테이너 수동 관리 시 발생하는 노드 장애 대응 지연, IP 변경에 따른 라우팅 붕괴 및 자원 단편화 한계

#### 한줄 요약
- 선언적 조정은 장애 복구를 자동화하는 대신 사람이 직접 조작한 변경까지 목표 상태로 되돌리므로, 클러스터의 진실은 실행 중인 자원이 아니라 선언에 있다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Reconciliation Loop**: 목표 상태(Desired State)와 현재 상태(Actual State)의 차이를 계산하여 끊임없이 일치시키는 무한 제어 루프.
- **etcd**: Raft 분산 합의 알고리즘 기반으로 클러스터의 모든 상태와 설정을 저장하는 고가용성 Key-Value 저장소.

</details>

- 두뇌 역할을 하는 제어면과 실행을 담당하는 워커 노드의 명확한 책임 분리(Control/Data Plane)
- 선언된 명세(YAML)를 기반으로 장애 발생 시 자동 복구하는 선언적 자가 치유(Self-Healing)
- 수평적 Pod 확장(HPA) 및 무중단 배포를 지원하는 고가용성 분산 오케스트레이션

#### 한줄 요약
- 선언적 API와 무한 조정 루프를 통해 컨테이너 장애를 실시간으로 자가 복구한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **제어면 & 워커노드 컴포넌트**: Control Plane(apiserver, etcd, scheduler, controller-manager), Worker Node(kubelet, kube-proxy, containerd).

</details>

```text
[쿠버네티스 마스터 제어면 및 워커 노드 아키텍처]
|-- Control Plane (마스터 제어면)
|   |-- kube-apiserver (중앙 REST API 게이트웨이, AuthN/AuthZ, etcd 통신 전담)
|   |-- etcd (Raft 분산 Key-Value 저장소: 클러스터 상태 및 메타데이터 영속 저장)
|   |-- kube-scheduler (Pod의 자원 요구량 분석 및 최적 워커 노드 필터링/바인딩)
|   `-- kube-controller-manager (Node, Deployment, Endpoint 조정 루프 총괄)
`-- Worker Node (작업 노드)
    |-- kubelet (노드 마스터 에이전트: CRI 호출을 통한 Pod 생명주기 및 헬스체크)
    |-- kube-proxy (iptables / IPVS 커널 라우팅을 통한 Service 트래픽 로드밸런싱)
    `-- Container Runtime (CRI 표준 containerd / CRI-O: 실제 Pod 컨테이너 기동)
```

선의 의미: 계층 및 kube-apiserver를 중심으로 제어면 컴포넌트들이 상태를 동기화하고 워커 노드의 kubelet이 파드를 제어하는 구조

| 구성요소 | 책임 | 주요 특징 |
|:---|:---|:---|
| kube-apiserver | 클러스터의 모든 요청을 접수하며 인증(AuthN), 인가(AuthZ), 스키마 검증 및 etcd 접근 중계 | 수평 스케일아웃 |
| etcd 저장소 | Raft 알고리즘 기반으로 클러스터의 모든 오브젝트 명세와 현재 상태를 분산 영속 저장 | 3/5대 홀수 쿼럼 |
| kube-scheduler | 미배치된 파드의 리소스 요구량과 제약 조건을 분석하여 최적의 워커 노드에 바인딩(Binding) | 필터링 및 스코어링 |
| Controller Manager | Node, Deployment, ReplicaSet 등의 컨트롤러를 구동하여 목표 상태와 현재 상태를 지속 동기화 | Reconciliation Loop |
| kubelet | 워커 노드의 마스터 에이전트로서 컨테이너 런타임(CRI)에 파드 생성/삭제를 지시하고 헬스체크 보고 | 노드 에이전트 |
| kube-proxy | 노드의 커널 iptables 또는 IPVS 규칙을 관리하여 쿠버네티스 서비스(Service) 트래픽 로드밸런싱 | L4 프록시 |
| Container Runtime | containerd/CRI-O 기반으로 OCI 이미지를 다운로드하고 실제 컨테이너 프로세스를 실행 | CRI 인터페이스 |

#### 한줄 요약
- 제어면은 목표 상태를 결정할 뿐 컨테이너를 직접 만들지 않고 kubelet이 CRI 호출로 그 실행을 대신 떠맡으므로, 노드가 사라져도 선언은 제어면에 남고 kube-proxy가 커널 규칙을 고쳐 트래픽 경로만 갱신한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **파드 프로비저닝 5단계**: YAML 요청 $\to$ etcd 기록 $\to$ 노드 스케줄링 $\to$ kubelet 실행 지시 $\to$ 상태 보고 및 etcd 갱신.

</details>

```text
개발자의 kubectl apply -f pod.yaml 배포 요청
        │
   [요청 접수 및 인증] kube-apiserver가 요청자의 권한을 인증(RBAC)하고 스키마 유효성 검증
        │
   [etcd 영속 저장] 검증 완료된 Pod 명세를 etcd에 기록 (상태: Pending)
        │
   [노드 스케줄링] kube-scheduler가 노드 리소스와 어피니티를 평가하여 최적 노드 선정 및 바인딩
        │
   [워커 노드 파드 기동] 대상 노드의 kubelet이 이벤트를 감지하고 CRI(containerd)로 컨테이너 실행
        │
   [상태 동기화] kubelet이 파드의 Running 상태를 apiserver에 보고하여 etcd에 최종 갱신
```

#### 한줄 요약
- 모든 요청이 API 서버를 거쳐 etcd에 기록된 뒤에야 실행되므로 etcd의 쓰기 성능이 클러스터 전체 변경 속도의 상한이 되고, 노드 수보다 오브젝트 수가 먼저 확장 한계를 만든다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **표준 K8s vs 경량 K3s**: 대규모 분산 클라우드용 표준 K8s와 단일 바이너리/SQLite 기반의 경량 엣지용 K3s.

</details>

| 비교 항목 | 표준 쿠버네티스 (Standard K8s) | 경량 쿠버네티스 (K3s) |
|:---|:---|:---|
| 최적 적용 환경 | 엔터프라이즈 데이터센터, EKS/GKE 대규모 클러스터 | 엣지 컴퓨팅, IoT 게이트웨이, 로컬 개발 환경 |
| 상태 저장소 | 외부 분산 etcd 클러스터 (Raft 기반 고가용) | 내장 SQLite (kine 확장) 또는 경량 DB |
| 제어면 메모리 요구량 | 수 GB 이상의 대용량 메모리 필요 | 512MB RAM 미만의 초경량 단일 바이너리 |
| 확장성 한계 | 수천 대 노드 및 수만 개 Pod 확장 지원 | 소규모 엣지 및 단일 노드 운영에 최적화 |

#### 한줄 요약
- 대규모 엔터프라이즈는 표준 K8s, 리소스 제약이 큰 엣지/IoT는 K3s를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **etcd Quorum Loss**: 홀수(3/5대) 노드로 구성된 etcd에서 과반수 이상 다운 시 클러스터 상태 쓰기가 전면 마비되는 장애.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| etcd 노드 과반수 다운으로 인한 클러스터 상태 쓰기 마비 | etcd 3대 이상 홀수 노드 Multi-AZ 분산 배치 및 정기 스냅샷 | etcd 고가용성 및 쿼럼 손실 방지 |
| 대규모 파드 급증 시 kube-apiserver CPU/메모리 병목 | apiserver 수평 스케일아웃 및 로드밸런서(NLB) 부하 분산 | 제어면 처리량 5배 향상 |
| 워커 노드 OOM 발생 시 핵심 데몬인 kubelet 프로세스 다운 | Kubelet 시스템 예약 메모리(`system-reserved`) 사전 격리 설정 | 워커 노드 생존성 100% 보장 |
| 마스터 노드 장애 시 전체 클러스터 제어 불능 | Control Plane 다중화(Multi-Master HA) 및 리더 선출 체계 구축 | 마스터 SPOF 완전 제거 |

#### 한줄 요약
- etcd 홀수 다중화, API 서버 수평 확장, Kubelet 시스템 자원 예약으로 안정성을 보장한다.

## Ⅶ. 결론

- 클라우드 네이티브 컴퓨팅 및 현대 엔터프라이즈 인프라의 가장 지배적인 분산 컨테이너 오케스트레이션 사실상 표준(De-facto Standard)으로 확립되었으며, 실무 구축 시에는 etcd 3/5대 홀수 쿼럼(Quorum) Multi-AZ 분산 및 고속 NVMe 스토리지 배치, kube-apiserver 수평 스케일아웃, 워커 노드 OOM 시 에이전트 다운을 방지하는 kubelet `system-reserved` 자원 예약 격리, 대규모 파드 스케줄링 병목을 해소하는 Karpenter 연동을 결합하여 무결점 제어면 고가용성과 대규모 분산 탄력성을 보증

#### 한줄 요약
- 쿠버네티스는 제어면과 워커 노드의 명확한 이원화와 선언적 자가 치유를 통해 대규모 컨테이너를 무결점으로 오케스트레이션하는 클라우드 네이티브의 핵심 운영체제다.
