---
title: "쿠버네티스 네트워킹 - CNI·Ingress (Kubernetes Networking)"
date: "2026-07-08"
tags:
  - "cspe-network"
weight: 75
extra:
  question_no: "075"
  exam_status: "기출"
  exam_history: "127회, 137회"
---

## 미리 알고가기

- Pod는 쿠버네티스에서 애플리케이션 컨테이너가 실행되는 기본 단위임
- CNI는 Pod에 IP를 할당하고 네트워크 연결을 만드는 플러그인 표준임
- Service는 여러 Pod 앞에 고정된 접근점과 로드밸런싱을 제공하는 가상 서비스임
- Ingress는 외부 HTTP, HTTPS 요청을 내부 Service로 라우팅하는 L7 진입점임

## Ⅰ. 개요

- **정의/개념**: 쿠버네티스 네트워킹은 CNI로 Pod 네트워크를 만들고 Service로 내부 접근을 추상화하며 Ingress로 외부 유입을 제어하는 컨테이너 중심 네트워크 구조임
- **배경/필요성**: Pod는 생성과 삭제, 이동이 잦아 고정 IP 기반 서버 운영 방식이 맞지 않으므로, 동적인 Pod 수명주기와 분리된 연결 경로와 서비스 식별 체계가 필요함

## Ⅱ. 특징

- 각 Pod가 고유 IP를 갖고 직접 통신할 수 있는 평면 네트워크 모델을 지향함
- Service와 DNS로 Pod 변경과 무관한 고정 접근점을 제공함
- Ingress와 Ingress Controller로 외부 HTTP, HTTPS 유입을 중앙에서 제어할 수 있음
- NetworkPolicy와 CNI 특성에 따라 보안, 성능, MTU, 가시성이 크게 달라질 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | CNI | Service | Ingress |
|:---|:---|:---|:---|
| 주된 역할 | Pod에 IP와 경로를 만들어 내부 네트워크를 구성함 | Pod 집합 앞에 고정된 L4 접근점과 로드밸런싱을 제공함 | 외부 HTTP, HTTPS 요청을 내부 Service로 연결함 |
| 적용 계층 | 주로 L3, L4 연결 기반을 다룸 | 클러스터 내부 서비스 추상화에 집중함 | L7 경로, 호스트, TLS 규칙을 다룸 |
| 대표 요소 | Calico, Cilium, Flannel 같은 플러그인이 여기에 속함 | ClusterIP, NodePort, LoadBalancer 같은 타입이 있음 | NGINX, Envoy, HAProxy 기반 컨트롤러가 많이 쓰임 |
| 설계 포인트 | MTU, 오버레이, 라우팅 방식 선택이 중요함 | 서비스 발견과 내부 로드밸런싱 구조가 중요함 | 외부 진입, TLS 종료, 경로 라우팅 정책이 중요함 |

> 요약: CNI는 Pod 연결 기반이고 Service는 내부 추상화이며 Ingress는 외부 유입 제어임.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Pod와 CNI 플러그인 | Pod 생성 시 IP, veth, 라우팅을 구성해 클러스터 네트워크에 편입시키는 계층임 |
| Service와 EndpointSlice | 여러 Pod를 하나의 논리 서비스로 묶고 실제 대상 목록을 관리하는 계층임 |
| kube-proxy 또는 eBPF | Service 가상 IP를 실제 Pod 대상으로 변환해 로드밸런싱을 수행하는 처리 계층임 |
| CoreDNS | Service 이름과 클러스터 내부 도메인 해석을 제공하는 서비스 발견 계층임 |
| Ingress Controller | 외부 HTTP, HTTPS 요청을 규칙에 따라 Service로 전달하는 진입 제어 계층임 |

```text
+-------------+     +----------------+     +----------------+     +----------------+
| Pod·CNI       | --> | Service·Endpoint | --> | kube-proxy/eBPF | --> | Ingress Controller |
+-------------+     +----------------+     +----------------+     +----------------+
                 \____________________ CoreDNS ____________________/
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +----------------+     +------------------+     +----------------+
| Pod 생성       | --> | CNI 네트워크 구성  | --> | Service 발견·분산   | --> | Ingress 외부 라우팅 |
+-------------+     +----------------+     +------------------+     +----------------+
```

1. **Pod 생성**: 스케줄러와 kubelet이 새 Pod를 노드에 배치함
2. **CNI 네트워크 구성**: CNI 플러그인이 Pod IP와 인터페이스, 라우팅을 생성함
3. **Service 발견과 분산**: CoreDNS와 Service가 고정 이름과 가상 IP를 제공하고 실제 Pod로 분산함
4. **Ingress 외부 라우팅**: 외부 요청이 Ingress Controller를 거쳐 내부 Service로 전달됨

## Ⅵ. 실무 적용 및 유의점

1. 대규모 마이크로서비스 클러스터에서는 CNI 선택이 성능과 운영 복잡도를 좌우하므로 오버레이 여부, eBPF 지원, 네트워크 정책 구현 방식을 먼저 정하고 Pod 간 지연 시간과 MTU 관련 드롭 건수로 확인함
2. 외부 서비스 공개가 많은 환경에서는 Service와 Ingress 역할을 섞어 설계하면 장애 분석이 어려워지므로 내부 접근과 외부 진입을 분리하고 DNS 응답 시간과 Ingress 오류율, 정책 차단 건수로 확인함

## Ⅶ. 결론

쿠버네티스 네트워킹의 핵심은 동적인 Pod 수명주기를 CNI, Service, Ingress로 안정적으로 추상화하는 데 있으므로 계층별 역할 구분이 먼저 명확해야 함.
