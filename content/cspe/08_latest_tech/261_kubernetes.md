---
title: "Kubernetes 쿠버네티스 (Kubernetes)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 261
extra:
  question_no: "261"
  exam_status: "기출"
  exam_history: "135회, 136회, 137회"
---

## 미리 알고가기

- Kubernetes는 컨테이너를 선언형으로 배포하고 확장하고 복구하는 오케스트레이션 플랫폼임
- 핵심은 개별 컨테이너 관리가 아니라 클러스터 전체의 desired state 유지에 있음
- Pod와 Node와 Control Plane 관계를 먼저 잡으면 전체 구조 이해가 쉬움

## Ⅰ. 개요

- **정의/개념**: Kubernetes는 컨테이너화된 애플리케이션을 클러스터 단위로 배포하고 스케일링하고 자가 복구하며 서비스 디스커버리와 롤링 업데이트를 자동화하는 오픈소스 컨테이너 오케스트레이션 플랫폼임
- **배경/필요성**: 마이크로서비스와 클라우드 네이티브 환경이 확산되면서 수많은 컨테이너를 수동으로 운영하기 어려워 선언형 배포와 자동 복구를 제공하는 표준 플랫폼이 필요해짐

## Ⅱ. 특징

- desired state 기반으로 현재 상태를 지속 교정함
- 스케줄링과 자가 복구와 서비스 노출을 통합 제공함
- 멀티노드 환경에서 확장성과 고가용성을 확보하기 좋음
- 오브젝트 수가 많아질수록 운영 표준화와 관측성이 중요해짐

## Ⅲ. 종류 및 비교

| 판단 기준 | Kubernetes | Docker Swarm | Nomad |
|:---|:---|:---|:---|
| 생태계 성숙도 | 매우 높음 | 중간 | 높음 |
| 기능 범위 | 광범위 | 비교적 단순 | 유연한 스케줄링 |
| 운영 복잡도 | 높음 | 낮음 | 중간 |
| 적합 환경 | 대규모 클라우드 네이티브 | 소규모 단순 환경 | 혼합 워크로드 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Control Plane | API Server와 Scheduler와 Controller Manager가 원하는 상태를 유지하도록 전체 클러스터를 제어하는 중앙 관리 계층임 |
| Node | 실제 컨테이너가 실행되는 워커 서버로 kubelet과 container runtime이 Pod 생명주기를 관리함 |
| Pod | 하나 이상의 컨테이너를 함께 배치하는 최소 실행 단위로 네트워크와 스토리지를 공유함 |
| Service and Ingress | Pod 집합을 안정적으로 노출하고 외부 트래픽을 라우팅하는 서비스 접속 계층임 |
| etcd | 클러스터 상태와 설정을 저장해 컨트롤 플레인이 일관된 판단을 하게 하는 분산 키값 저장소임 |

```text
+---------------------- Control Plane ----------------------+
| API Server | Scheduler | Controller Manager | etcd       |
+-----------------------------------------------------------+
                 |                         |
                 v                         v
           +-----------+             +-----------+
           |  Node 1   |             |  Node 2   |
           |  Pods     |             |  Pods     |
           +-----------+             +-----------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 선언형 배포 작성 | -> | API 등록    | -> | 스케줄링    | -> | Pod 실행     | -> | 상태 감시 및 복구 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **선언형 배포 작성**: 사용자가 원하는 상태를 매니페스트로 정의함
2. **API 등록**: API Server가 요청을 받아 클러스터 상태로 저장함
3. **스케줄링**: Scheduler가 적절한 Node를 선택함
4. **Pod 실행**: kubelet이 컨테이너를 기동함
5. **상태 감시 및 복구**: Controller가 목표 상태와 실제 상태 차이를 계속 보정함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 리소스 요청과 제한 설정이 부정확하면 특정 노드에 과부하가 몰려 성능 저하와 재스케줄링이 반복될 수 있음
   - 해결방안: resource quota와 vertical horizontal autoscaling policy를 적용하고 node pressure incident rate와 pod eviction count로 검증함
2. 문제: 오브젝트와 네트워크 정책이 복잡해질수록 운영자가 장애 원인과 의존 관계를 추적하기 어려워질 수 있음
   - 해결방안: standardized manifest template와 observability stack을 적용하고 mean time to diagnose와 configuration drift count로 검증함
3. 문제: 컨트롤 플레인과 etcd 고가용성이 부족하면 클러스터 전체 제어 기능이 단일 장애점이 될 수 있음
   - 해결방안: HA control plane과 etcd quorum design을 적용하고 control plane availability와 failover recovery time으로 검증함

## Ⅶ. 적용 사례

- 전자상거래 플랫폼이 HPA와 리소스 정책을 운영하며 확인 지표는 node pressure incident rate와 pod eviction count임
- 금융 마이크로서비스가 표준 매니페스트와 관측 스택을 적용하며 확인 지표는 mean time to diagnose와 configuration drift count임
- 공공 클라우드 환경이 HA 컨트롤 플레인을 구성하며 확인 지표는 control plane availability와 failover recovery time임

## Ⅷ. 결론

Kubernetes는 컨테이너 운영의 사실상 표준이지만 선언형 자동화만큼 자원 정책과 관측성과 고가용성 설계가 함께 성숙해야 안정성이 확보됨.
