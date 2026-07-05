---
title: 쿠버네티스 아키텍처 — 컨트롤 플레인·노드 (K8s Architecture)
date: 2026-07-05
tags: ["cspe-software"]
weight: 37
---

## Ⅰ. 개요
- 정의: 클러스터를 관리하는 컨트롤 플레인과 워크로드를 실행하는 노드로 구성된 분산 시스템 구조.
- 출제 의도: 내부 핵심 컴포넌트 간의 통신 방식 및 역할 분담 체계의 기술적 심화 이해도 평가.

## Ⅱ. 구성요소
- ASCII 구조도
  < Control Plane >              < Worker Node >
  [ API Server ] <------------> [ Kubelet      ]
  [ etcd       ]                [ Kube-proxy   ]
  [ Scheduler  ]                [ Container Runtime ]
  [ Controller Manager ]        [ (Pod) (Pod)  ]
- 구성요소 표
| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| API Server | 클러스터의 모든 요청을 처리하는 관문 | 안내 데스크 |
| etcd | 모든 클러스터 데이터(상태 정보)를 저장하는 키-값 저장소 | 등기소 |
| Kubelet | 각 노드에서 컨테이너의 실행 상태를 관리하는 에이전트 | 현장 소장 |
> 요약: 마스터(Control Plane)가 명령을 내리고, 워커(Node)가 실무를 수행하는 수직적 협력 구조임.

## Ⅲ. 절차
- ASCII 흐름도
  [Request] -> [API Server Validation] -> [etcd Storage] -> [Scheduler/Node Assignment]
- 4단계 설명
1. 사용자가 API Server에 리소스 생성 요청을 전송함.
2. 요청 내용을 검증 후 클러스터의 상태 DB인 etcd에 저장함.
3. 스케줄러가 etcd를 모니터링하다 미할당 Pod 발견 시 노드 선정함.
4. 선정된 노드의 Kubelet이 컨테이너 런타임을 통해 Pod를 기동함.
> 요약: 상태 저장(etcd) -> 비동기 감지 -> 액션 수행의 메커니즘으로 동작함.

## Ⅳ. 문제점
- etcd 성능 병목: 대규모 클러스터에서 etcd 입출력 지연 시 전체 클러스터 반응 속도 저하됨.
- 마스터 가용성: 컨트롤 플레인 장애 시 전체 클러스터의 제어 불능 상태(SPOF) 발생함.

## Ⅴ. 개선방안
- 고가용성(HA) 구성: 컨트롤 플레인을 3대 이상의 홀수 개로 다중화하여 쿼럼(Quorum) 유지함.
- 고속 스토리지: etcd 전용의 고성능 SSD(NVMe) 및 격리된 네트워크 대역폭 할당 필요함.

## Ⅵ. 전망
- Cluster API(CAPI)를 통한 인프라 프로비저닝의 표준화 및 자동화 기술 고도화될 것임.
- 서버리스 노드(AWS Fargate 등) 도입으로 노드 관리 부담을 없애는 노드리스(Nodeless) 추세 확산됨.
- 하드웨어 가속기(GPU, TPU)의 효율적 스케줄링을 위한 DRA(Dynamic Resource Allocation) 도입 가속화됨.
