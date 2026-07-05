---
title: "K8s 아키텍처 (Kubernetes Architecture)"
date: "2026-07-05"
tags:
  - "cspe-software"
weight: 67
---

## Ⅰ. 개요
- **정의**: Control Plane과 Data Plane(Worker Node)으로 분리된 K8s 클러스터의 내부 구조
- **배경/필요성**: 오케스트레이션(066 참조) 동작 원리를 이해하려면 각 컴포넌트의 역할과 통신 흐름을 파악해야 함
- **비유**: 본사(Control Plane)가 정책을 결정하고 각 지점(Worker Node)이 실행하는 프랜차이즈 구조

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 컴포넌트 역할과 통신 흐름 | Master/Worker 분리, 각 컴포넌트 책임 | API Server 중심 통신 구조를 누락하지 않을 것 |

> 요약: Control Plane-Worker Node 분리 구조에서 API Server를 중심으로 모든 통신이 이루어지는 아키텍처임

## Ⅱ. 구성요소
```text
+-- Control Plane --------+     +-- Worker Node ----------+
|  API Server              |     |  Kubelet                 |
|  etcd                    |     |  kube-proxy              |
|  Scheduler               |<--->|  Container Runtime (CRI) |
|  Controller Manager      |     |  Pod  Pod  Pod           |
+--------------------------+     +--------------------------+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| API Server | 클러스터의 유일한 통신 허브, 인증·인가·Admission 처리 | 본사 접수 창구 |
| etcd | 클러스터 메타데이터를 저장하는 분산 합의 저장소 | 본사 장부 |
| Kubelet | 각 Node에서 Pod 생명주기를 관리하는 에이전트 | 지점 매니저 |
| kube-proxy | Service IP를 Pod IP로 라우팅하는 네트워크 프록시 | 지점 안내데스크 |

> 요약: Control Plane 4개 컴포넌트와 Worker Node 3개 컴포넌트가 API Server를 허브로 협업함

## Ⅲ. 절차
```text
kubectl --> API Server --> etcd(store)
                |
                +--> Scheduler(assign node)
                |
                +--> Kubelet(create pod)
                |
                +--> Controller(reconcile)
```
- 1단계: 사용자가 `kubectl`로 API Server에 오브젝트 생성을 요청함
- 2단계: API Server가 etcd에 오브젝트 상태를 저장함
- 3단계: Scheduler가 미배치 Pod를 감지하고 적합한 Node를 할당함
- 4단계: 해당 Node의 Kubelet이 Container Runtime을 호출하여 Pod를 생성함

> 요약: 요청-저장-스케줄-생성의 4단계로 Pod가 실행됨

## Ⅳ. 문제점
- 단일 API Server 병목: 대규모 클러스터에서 API Server 과부하 시 전체 제어가 지연됨
- etcd 쓰기 지연: 오브젝트 수가 수만 개 이상이면 etcd 응답 시간이 증가함
- Kubelet 장애 전파: Node 내 Kubelet 비정상 시 해당 Node의 모든 Pod가 영향받음

> 요약: API Server 병목, etcd 지연, Kubelet 장애 전파가 주요 문제임

## Ⅴ. 개선방안
1. 단기: API Server를 다중 인스턴스로 구성하고 로드밸런서를 전면에 배치함
2. 중기: etcd 클러스터를 3~5노드 구성하고 주기적 스냅샷·컴팩션을 자동화함
3. 장기: Node 장애 감지 시간(`node-monitor-grace-period`)을 튜닝하고 Pod Disruption Budget을 설정함

> 요약: API Server 이중화, etcd 고가용성, 장애 감지 튜닝으로 개선함

## Ⅵ. 전망
- 발전 방향: 경량 K8s(K3s·MicroK8s)로 엣지·IoT 환경까지 아키텍처가 확장됨
- 기술사적 판단: 아키텍처 이해가 Pod·Service·Deployment(068 참조) 설계의 전제 조건임
- 기술사 제언: 컨트롤 플레인 컴포넌트별 장애 시나리오와 대응 방안을 숙지할 필요
