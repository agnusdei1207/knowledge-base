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

- **쿠버네티스 아키텍처(Kubernetes Architecture)**: 클러스터 상태를 관리하는 제어면(Control Plane)과 실제 워크로드를 가동하는 작업 노드(Worker Node)로 분리된 오케스트레이션(Orchestration) 구조.
- **제어면(Control Plane)**: API 서버, etcd, 스케줄러, 컨트롤러 관리자로 구성되어 클러스터 전체의 제어 기능을 담당하는 핵심 관리 서버.
- **작업 노드(Worker Node)**: kubelet, kube-proxy, 컨테이너 런타임(containerd)으로 구성되어 실제 파드(Pod)를 실행하는 컴퓨팅 서버.

</details>

- 정의: 컨테이너화된 애플리케이션의 자동 배포, 확장, 자가 치유(Self-healing)를 위해 제어면과 작업 노드로 역할을 분리한 아키텍처.
- 배경: 대규모 컨테이너의 수동 관리 한계 극복 및 선언적 API(Declarative API) 기반의 자동 오케스트레이션 요구.

#### 한줄 요약

- 운영자가 파드 수만 선언하면 제어면은 빈자리를 찾아 배치하고 장애로 사라진 파드를 다시 만들기 때문에 목표와 현실의 차이를 자동으로 좁힐 수 있다.

## Ⅱ. 특징 (쿠버네티스 3대 핵심 운용 메커니즘)

<details><summary>핵심 용어</summary>

- **조정 루프(Reconciliation Loop)**: 클러스터의 '목표 상태(Desired State)'와 '현재 상태(Current State)'를 지속적으로 비교하고 격차를 해소하여 클러스터 상태를 동기화하는 자가 치유(Self-healing) 메커니즘.

</details>

- **제어면과 작업 노드 분리**: 지능형 제어와 실제 워크로드 실행의 물리적·논리적 분리.
- **선언적 상태 관리**: YAML 명세서 기반 목표 상태 선언 및 조정 루프(Reconciliation Loop)의 상시 작동.
- **자가 치유와 자동 복구**: 파드 장애 시 타 노드 자동 재생성 및 무중단 롤링 배포 수행.

#### 한줄 요약

- 실행 순서를 일일이 명령하는 대신 원하는 결과를 적어 두면 여러 제어기가 각자 맡은 차이를 계속 바로잡는 방식이다.

## Ⅲ. 구조 및 구성요소 (Control Plane vs Worker Node 8대 핵심 컴포넌트)

<details><summary>핵심 용어</summary>

- **kube-apiserver & etcd**: kube-apiserver는 클러스터의 유일한 REST API 입구, etcd는 클러스터의 모든 상태값을 보존하는 분산 Key-Value DB.

</details>

```text
┌────────────────────────────────────────┬──────────────────────────────────────────┐
│             제어면(Control Plane)      │           작업 노드(Worker Node)         │
├────────────────────────────────────────┼──────────────────────────────────────────┤
│ API 서버 ──► etcd DB                   │ kubelet ──► kube-proxy ──► 런타임        │
│ 스케줄러 ──► 컨트롤러 관리자           │ └─► 파드(Pod)                            │
└────────────────────────────────────────┴──────────────────────────────────────────┘
```

선의 의미: Control Plane의 API 서버가 명령을 수신하여 etcd에 기재 후 Worker Node의 kubelet으로 하달되어 containerd가 Pod를 구동하는 구조.

| 파트 영역 | 핵심 구성요소 | 역할 및 메커니즘 |
|:---|:---|:---|
| **제어면**| **API 서버** | 클러스터 통신 게이트웨이 (REST API) |
| **제어면**| **etcd** | 클러스터 전체 상태 저장 고가용성 DB |
| **제어면**| **스케줄러** | 파드 배치를 위한 최적 노드 선택 |
| **제어면**| **컨트롤러 관리자** | 조정 루프(Reconciliation Loop) 작동 |
| **작업 노드** | **kubelet** | 노드별 에이전트, 파드 생성/상태 보고 |
| **작업 노드** | **kube-proxy** | 네트워크 라우팅 및 서비스 처리 |
| **작업 노드** | **컨테이너 런타임**| 실제 파드 내 컨테이너 구동 (containerd) |

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

1. **API 수신 및 etcd 저장**: 유저 YAML 제출 시 API 서버 검증 후 etcd에 상태 저장.
2. **스케줄링**: 스케줄러가 여유 노드를 선택하여 API 서버 갱신.
3. **kubelet 실행**: kubelet이 이를 감지하여 런타임에 파드 생성 명령 및 가동.

#### 한줄 요약

- 배포 객체를 제출하면 제어기가 부족한 파드를 만들고 스케줄러가 노드를 정한 뒤 kubelet이 런타임에 실행을 맡기는 한 흐름으로 이어진다.

## Ⅴ. 종류 및 비교 (Control Plane DB: etcd 대 K3s SQLite)

<details><summary>핵심 용어</summary>

- **etcd Raft Consensus**: etcd는 분산 합의 알고리즘(Raft)을 사용하여 3대 이상 홀수(3, 5, 7)로 구성해야 쿼럼(Quorum) 유지 가능.

</details>

| 비교 항목 | 엔터프라이즈 쿠버네티스 | 경량 쿠버네티스 (K3s) |
|:---|:---|:---|
| **DB** | etcd (분산 Key-Value DB) | SQLite (kine 엔진) |
| **배치 환경** | 대규모 엔터프라이즈/금융 클라우드 | 엣지 컴퓨팅, IoT, 로컬 개발 |
| **최소 노드** | 홀수 마스터 노드 (HA 필수) | 단일 노드 |
| **메모리 오버헤드**| 수 GB (Heavy) | 512MB 이하 (Light) |

#### 한줄 요약

- 제어면은 어디서 무엇을 실행할지 결정하고 작업 노드는 받은 명세대로 컨테이너를 움직인다는 경계로 구분하면 구성요소가 섞이지 않는다.

## Ⅵ. 실무 고려사항 및 대책 (K8s 아키텍처 3대 실무 지침)

<details><summary>핵심 용어</summary>

- **etcd Quorum Failure**: etcd 노드 3대 중 2대가 동시 다운되면 쿼럼(과반수)이 깨져 클러스터 전체가 읽기 전용 락에 걸리는 참사.

</details>

| 3대 K8s 난제 | 원인 | 실무 대책 |
|:---|:---|:---|
| **1. etcd 쿼럼 손실** | 노드 과반수 다운으로 락 발생 | etcd 분산 배치 및 주기적 백업 |
| **2. API 서버 병목** | 과도한 파드 요청 | API 서버 스케일아웃 및 캐싱 튜닝 |
| **3. kubelet 메모리 부족**| 노드 메모리 고갈 | kubelet 시스템 예약 메모리 확보 |

> 사례: **카카오 / 당근마켓 / 쿠팡 EKS / GKE 기반 대규모 마스터 노드 HA 멀티 클러스터 운용**

#### 한줄 요약

- 제어면만 이중화해도 요청량이 틀리거나 배치 제약이 충돌하면 파드가 멈추므로 상태 저장, 권한, 용량, 배치 조건을 함께 점검해야 한다.

## Ⅶ. 결론

- **고가용성 제어면 및 분산 상태 관리 체계 준수**
- **클러스터 워크로드 자가 치유 메커니즘 적용 필수**
