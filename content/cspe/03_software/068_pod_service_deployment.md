---
title: "Pod·Service·Deployment (Pod Service Deployment)"
date: "2026-07-05"
tags:
  - "cspe-software"
weight: 68
---

## Ⅰ. 개요
- **정의**: K8s의 핵심 워크로드 오브젝트로, Pod는 실행 단위, Deployment는 선언적 배포 관리, Service는 네트워크 접근을 추상화함
- **배경/필요성**: 컨테이너 단독 실행만으로는 복제·롤링업데이트·서비스 디스커버리가 불가하므로, 이를 추상화하는 상위 오브젝트가 필요함
- **비유**: Pod는 승객, Deployment는 버스 배차표, Service는 버스 정류장 — 정류장 위치는 고정이나 버스(Pod)는 교체 가능함

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 3개 오브젝트 관계와 역할 구분 | Pod 임시성, Deployment의 ReplicaSet 관리, Service의 안정 IP | Pod를 직접 관리하는 안티패턴을 언급할 것 |

> 요약: Pod-Deployment-Service의 3계층으로 실행·배포·접근을 분리 관리하는 구조임

## Ⅱ. 구성요소
```text
Deployment --> ReplicaSet --> Pod(1)
                          --> Pod(2)
                          --> Pod(N)
                               ^
                               |
                            Service (ClusterIP/NodePort/LB)
                               ^
                               |
                            Client
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Pod | 1개 이상 컨테이너를 묶은 최소 배포 단위, IP 할당 | 승객(교체 가능) |
| ReplicaSet | 지정 수의 Pod 복제본을 유지하는 컨트롤러 | 배차 관리 시스템 |
| Deployment | ReplicaSet을 관리하며 롤링업데이트·롤백을 수행 | 배차표 |
| Service | 안정된 ClusterIP·DNS로 Pod 집합에 트래픽을 분배 | 버스 정류장 |

> 요약: Deployment가 ReplicaSet을 통해 Pod 수를 유지하고, Service가 안정 접점을 제공함

## Ⅲ. 절차
```text
Create Deployment --> RS creates Pods --> Service selects Pods --> Client access
```
- 1단계: Deployment YAML에 이미지·레플리카 수·업데이트 전략을 선언함
- 2단계: Deployment가 ReplicaSet을 생성하고, ReplicaSet이 Pod를 원하는 수만큼 기동함
- 3단계: Service가 Label Selector로 대상 Pod를 자동 등록하고 ClusterIP를 할당함
- 4단계: 클라이언트가 Service DNS/IP로 요청하면 kube-proxy가 Pod에 분배함

> 요약: 선언-복제-셀렉팅-라우팅의 4단계로 워크로드가 서빙됨

## Ⅳ. 문제점
- Pod 재시작 시 IP 변경: Pod는 일시적이므로 IP 기반 직접 접근 시 연결이 끊어짐
- 롤링업데이트 중 트래픽 유실: 구버전 Pod 종료와 신버전 Pod 준비 사이 요청이 실패할 수 있음
- 리소스 미설정: `requests`/`limits` 미지정 시 Pod 간 자원 경합이 발생함

> 요약: IP 불안정, 업데이트 중 트래픽 유실, 리소스 경합이 주요 문제임

## Ⅴ. 개선방안
1. 단기: Service를 통한 접근을 의무화하고 Pod 직접 참조를 금지함
2. 중기: `readinessProbe`를 설정하여 준비된 Pod만 트래픽을 수신하도록 함
3. 장기: LimitRange·ResourceQuota로 네임스페이스 수준 자원 거버넌스를 적용함

> 요약: Service 의무화, Readiness Probe, 자원 거버넌스로 개선함

## Ⅵ. 전망
- 발전 방향: Gateway API가 Ingress를 대체하며 Service 계층의 표현력이 확대됨
- 기술사적 판단: 3개 오브젝트 관계는 K8s 문제의 기본 출제 영역이며, Helm(069 참조)으로 패키징하는 흐름과 연결됨
- 기술사 제언: Pod 설계 시 사이드카 패턴·Init Container 활용과 함께 리소스 정책을 기본 설정할 필요
