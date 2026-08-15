---
sidebar:
  order: 152
  label: "152. 쿠버네티스 아키텍처 (Kubernetes Architecture)"
  badge:
    text: "기출 • 85%"
    variant: note
title: "쿠버네티스 아키텍처 (Kubernetes Architecture)"
date: "2026-08-14T02:00:00+09:00"
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

- **쿠버네티스 아키텍처(Kubernetes Architecture)**: 클러스터 상태를 관리하는 제어면(Control Plane)과 워크로드를 가동하는 작업 노드(Worker Node)로 분리된 컨테이너 오케스트레이션(Container Orchestration) 구조.
- **제어면(Control Plane)**: API 서버(API Server), etcd(Distributed Key-Value Store), 스케줄러(Scheduler), 컨트롤러 관리자(Controller Manager)로 구성된 클러스터 관리 핵심 서버.
- **작업 노드(Worker Node)**: 큐블릿(Kubelet), 큐브 프록시(Kube-proxy), 컨테이너 런타임(Container Runtime)으로 구성되어 파드(Pod)를 실행하는 컴퓨팅 서버.

</details>

- 정의/개념: 제어면과 작업 노드로 나눈 **Kubernetes Architecture**
- 배경/필요성: 수동 Container 관리는 **상태 편차•장애 복구**에 한계

#### 한줄 요약

- 운영자가 파드 수만 선언하면 제어면은 빈자리를 찾아 배치하고 장애로 사라진 파드를 다시 만들기 때문에 목표와 현실의 차이를 자동으로 좁힐 수 있다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **조정 루프(Reconciliation Loop)**: 클러스터의 '목표 상태(Desired State)'와 '현재 상태(Current State)'를 지속적으로 비교하고 격차를 해소하여 클러스터 상태를 동기화하는 자가 치유(Self-healing) 메커니즘.

</details>

- **제어면/작업 노드 분리**: 지능형 제어와 실제 워크로드 실행의 물리적·논리적 분리.
- **선언적 상태 관리(Declarative API)**: YAML 명세서 기반 목표 상태 선언 및 조정 루프(Reconciliation Loop) 상시 작동.
- **자가 치유(Self-healing)**: 파드 장애 시 타 노드 자동 재생성 및 무중단 롤링 배포 수행.

#### 한줄 요약

- 실행 순서를 일일이 명령하는 대신 원하는 결과를 적어 두면 여러 제어기가 각자 맡은 차이를 계속 바로잡는 방식이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **kube-apiserver & etcd**: kube-apiserver는 클러스터의 유일한 REST API 입구, etcd는 클러스터의 모든 상태값을 보존하는 분산 Key-Value DB.

</details>

```text
┌──────────── 제어면 ────────────┐
│ API 서버 │ etcd                │
│ 스케줄러 │ 컨트롤러 관리자     │
├────────── 작업 노드 ───────────┤
│ Kubelet │ Kube-proxy │ 런타임  │
└────────────────────────────────┘
```

| 구성요소 | 책임 |
|---|---|
| API 서버 | **인증•검증**과 Cluster API 제공 |
| etcd | **목표•현재 상태**의 일관된 저장 |
| 스케줄러 | 미배치 Pod의 **실행 Node** 선택 |
| 컨트롤러 관리자 | **조정 루프**로 상태 편차 해소 |
| Kubelet | Pod 명세 실행과 **Node 상태** 보고 |
| Kube-proxy | Service의 **Network 전달 규칙** 관리 |
| 런타임 | OCI Image로 **Container Process** 실행 |

#### 한줄 요약

- API 서버가 주문을 받고 장부에 기록하면 스케줄러가 작업 장소를 정하고 kubelet과 런타임이 현장에서 파드를 실행한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Pod Provisioning Flow**: `kubectl apply` YAML 전달 $\rightarrow$ apiserver validation $\rightarrow$ etcd write $\rightarrow$ scheduler node selection $\rightarrow$ kubelet pod run.

</details>

```text
[배포 명세 제출]
      │
      ▼
1. API 인증•검증
      │
      ▼
2. 목표 상태 저장
      │
      ▼
3. Node 선택
      │
      ▼
4. Pod 실행
      │
      ▼
5. 상태 보고•조정
      │
      ▼
[서비스 상태 반환]
```

### 동작 원리

1. **API 인증•검증**: 사용자와 Resource 명세 승인
2. **목표 상태 저장**: API 서버가 etcd에 Object 기록
3. **Node 선택**: 스케줄러가 제약•자원에 맞춰 Binding
4. **Pod 실행**: Kubelet이 Runtime에 Container 생성 요청
5. **상태 보고•조정**: 현재 상태 갱신과 편차 재조정

#### 한줄 요약

- 배포 객체를 제출하면 제어기가 부족한 파드를 만들고 스케줄러가 노드를 정한 뒤 kubelet이 런타임에 실행을 맡기는 한 흐름으로 이어진다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

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

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **etcd 쿼럼 손실(etcd Quorum Loss)**: etcd 클러스터의 과반수 노드가 이탈하여 분산 합의가 불가능해지고 클러스터 상태 쓰기가 중단되는 장애 현상.
- **API 서버 병목(API Server Bottleneck)**: 대규모 파드 증설 및 컨트롤러 폴링 요청 폭증으로 API 서버의 응답 지연이 발생하는 현상.
- **시스템 자원 고갈(System OOM)**: 워크로드 파드가 노드 메모리를 과점유하여 kubelet 및 핵심 데몬이 강제 종료되는 장애.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| etcd 과반수 장애로 인한 상태 쓰기 불능 | etcd 홀수(3/5) 노드 분산 배치 및 정기 스냅샷 백업 | **클러스터 상태 지속성 보장** |
| 과도한 파드 생성 요청 시 API 서버 병목 | API 서버 수평 확장 및 etcd 캐시 튜닝 | **제어면 처리량 향상** |
| 파드 메모리 과다 점유로 kubelet 정지 | 노드별 시스템/kubelet 예약 메모리(Reserved) 설정 | **노드 안정성 확보** |

> 요약: etcd 쿼럼 보장과 제어면 스케일아웃 및 노드 자원 격리로 대규모 클러스터 안정성 확보.

#### 한줄 요약

- 상태 저장소의 쿼럼 유지와 제어면·노드 자원 격리로 대규모 클러스터 가용성을 사수한다.

## Ⅶ. 결론

- 핵심 Cluster는 **제어면•etcd HA**, Edge는 경량 배포 선택

#### 한줄 요약

- 장애 허용 범위와 운영 규모에 맞춰 제어면 저장 구조와 노드 실행 구조를 선택한다.
