---
sidebar:
  order: 62
  label: "062. 쿠버네티스 네트워킹 - CNI•Ingress (Kubernetes Networking)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "쿠버네티스 네트워킹 - CNI•Ingress (Kubernetes Networking)"
date: "2026-08-10T10:00:00+09:00"
tags:
  - "notes-network"
weight: 62
extra:
  question_no: "062"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "설계형: 137회 CNI•Ingress•Policy 장문"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **쿠버네티스 네트워킹(Kubernetes Networking)**: 클러스터 내 동적으로 생성•소멸되는 파드(Pod) 간 direct IP 통신, 서비스 발견, L7 인그레스 노출 및 네트워크 보안 정책을 제공하는 통합 가상 네트워크 모델이다.
- **쿠버네티스(Kubernetes, K8s)**: 컨테이너화된 애플리케이션의 자동 배포, 스케일링, 복구를 선언적으로 관리하는 오픈소스 오케스트레이션 플랫폼이다.
- **인터넷 프로토콜(Internet Protocol, IP)**: 패킷의 논리적 주소 지정과 3계층 라우팅을 담당하는 기본 통신 프로토콜이다.
- **파드(Pod)**: 하나 이상의 컨테이너가 동일한 네트워크 네임스페이스(Linux Network Namespace) 및 IP 주소를 공유하며 실행되는 쿠버네티스의 최소 배포 단위이다.
- **컨테이너 네트워크 인터페이스(Container Network Interface, CNI)**: 파드 생성 시 가상 veth 인터페이스 생성, IP 주소 할당 및 라우팅 테이블을 구성을 담당하는 플러그인 표준 규격이다.
- **서비스(Service)**: 동적으로 IP가 변동되는 파드 집합 전면에 단일 고정 가상 IP(ClusterIP) 및 DNS 이름을 제공하는 L4 로드밸런싱 객체이다.
- **인그레스(Ingress)**: 클러스터 외부의 HTTP/HTTPS 트래픽을 L7 라우팅 규칙(Host/Path)에 따라 클러스터 내부의 Service로 전달하는 프록시 객체이다.

</details>

- 정의/개념: **쿠버네티스 네트워킹**(Kubernetes Networking)은 모든 **파드**(Pod)가 NAT 없이 상호 통신 가능한 독자적 **IP**를 보유하도록 **CNI**(Container Network Interface) 플러그인으로 구성하고, **서비스**(Service) 및 **인그레스**(Ingress)를 통해 가상 IP 로드밸런싱과 외부 L7 트래픽 진입 경로를 제공하는 클라우드 네이티브 네트워크 체계이다.
- 배경/필요성: 컨테이너 오토스케일링 및 재시작으로 인해 파드 IP가 유동적으로 변경되므로, 서비스 디스커버리를 위한 고정 접근점과 오버레이/언더레이 L2/L3 통신 격리 및 보안 정책 수립이 필수적이다.

#### 한줄 요약

- 파드의 동적 IP 생명주기를 CNI 및 가상 IP 서비스 계층으로 추상화하여 고가용성 인그레스 트래픽을 수용하는 네트워킹 아키텍처 적용.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **가상 IP 주소(Virtual IP Address, VIP)**: 물리적인 NIC가 아닌 소프트웨어 정의 프록시(kube-proxy/eBPF)에 의해 제어되며 복수의 파드 종단으로 분산되는 고정 대표 IP 주소이다.
- **준비 상태(Readiness Probe / Readiness State)**: 파드 내부 트래픽 수용 가능 여부를 진단하여 서비스 로드밸런싱 엔드포인트 등록 여부를 동적으로 결정하는 상태 지표이다.

</details>

- 모든 파드는 독자적인 고유 **IP 주소**를 할당받아 컨테이너 간 포트 중복 충돌 없이 1:1 직접 통신(Pod-to-Pod)이 가능하다.
- **서비스** 객체는 **가상 IP 주소**(VIP)를 부여하여 헬스체크를 통과한 **준비 상태**(Readiness)의 파드 엔드포인트로 패킷을 자동으로 로드밸런싱한다.
- **인그레스**는 L7 영역에서 TLS 종단(TLS Termination), 도메인 기반 네임 기반 호스팅, URL 경로 기반 가우팅을 일관되게 선언 및 실행한다.

#### 한줄 요약

- CNI 기반 Flat IP 모델과 VIP 서비스 분산, L7 Ingress 라우팅을 융합하여 서비스 연속성을 확보하는 기본 원칙 준수.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **엔드포인트슬라이스(EndpointSlice)**: 기존 Endpoint 객체의 대규모 클러스터 성능 한계를 극복하기 위해 파드의 IP•포트•준비 상태 정보를 100개 단위로 분할 관리하는 확장성 개체이다.
- **네트워크 정책(NetworkPolicy)**: 파드 라벨(Label) 및 IP CIDR 기반으로 Ingress/Egress 트래픽의 허용/차단을 선언하여 클러스터 내부 Zero-Trust를 구현하는 보안 객체이다.
- **전송 계층 보안(Transport Layer Security, TLS)**: 외부 사용자 및 인그레스 게이트웨이 간 패킷 암호화 및 Server 인증서 검증을 수행하는 보안 프로토콜이다.
- **확장 버클리 패킷 필터(extended Berkeley Packet Filter, eBPF)**: 리눅스 커널 이벤트 영역에서 IPTables 오버헤드 없이 고성능 바이패스 라우팅 및 NetworkPolicy를 커널 레벨에서 즉시 실행하는 기술이다.

</details>

- **EndpointSlice** 객체는 파드 Scale-Out 시 API 서버와 kube-proxy 간 전송 데이터를 최적화하고, **NetworkPolicy**는 L3/L4 격리 정책을 선언한다.
- Cilium 등의 고성능 CNI는 리눅스 커널 내 **eBPF** 엔진을 활용하여 iptables 병목 없이 바이패스 데이터 패스 전송을 수행하며, 인그레스 컨트롤러는 **TLS** 암호화를 지원한다.

```text
쿠버네티스 네트워킹 아키텍처 (Kubernetes Networking Architecture)
├─ 외부 L7 진입: 인그레스 컨트롤러 (Ingress Controller: NGINX / Envoy / Gateway API)
├─ 서비스 디스커버리 계층
│  ├─ 서비스 객체 (Service: ClusterIP / NodePort / LoadBalancer)
│  └─ 엔드포인트 분할 (EndpointSlice Object)
└─ 파드 데이터 패스 & 보안
   ├─ 네트워크 정책 (NetworkPolicy Definition)
   └─ CNI 데이터 패스 (Cilium eBPF / Calico IPTables / Flannel VXLAN)
```

| 구성요소 | 역할 및 핵심 기능 |
|:---|:---|
| **인그레스 컨트롤러 (Ingress Controller)** | External L7 Host/Path 라우팅 규칙 해석 및 SSL/TLS Termination 실행 |
| **서비스 객체 (Service)** | ClusterIP, NodePort, LoadBalancer 타잎의 고정 VIP 제공 및 로드밸런싱 |
| **엔드포인트슬라이스 (EndpointSlice)** | Pod 개수 증가 시 준비 상태(Readiness)의 Pod IP/Port 맵핑 정보를 분할 수용 |
| **네트워크 정책 (NetworkPolicy)** | Pod Label Selector 기반 Ingress/Egress 트래픽의 L3/L4 접근제어 허용 목록(Allow-list) 설정 |
| **CNI 데이터 패스 (CNI Data Path)** | eBPF/iptables/OVS 기반 CNI 터널링(VXLAN/Geneve) 및 커널 레벨 패킷 포워딩 |

#### 한줄 요약

- Ingress 컨트롤러, EndpointSlice 기반 디스커버리, eBPF CNI 패킷 포워딩이 결합된 클라우드 네이티브 네트워크 아키텍처 구현 필수.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **데이터 경로(Data Path)**: 패킷이 파드 간 또는 외부에서 내부로 수신될 때 eBPF/iptables/IPVS 모듈을 통해 포워딩되는 실물 통신 경로이다.
- **프록시(Proxy / kube-proxy)**: 각 노드에서 서비스 VIP로 들어오는 요청을 탐지하여 엔드포인트 파드로 라우팅 룰을 업데이트하는 데몬 프로세스이다.
- **응용 프로그래밍 인터페이스(Application Programming Interface, API)**: K8s 컨트롤 플레인 자원과 클라이언트 간 통신을 정의하는 REST API 명세이다.
- **API 서버(API Server / kube-apiserver)**: 클러스터의 모든 리소스 상태 변경 요청을 검증하고 etcd에 수용하며 이벤트를 알리는 중앙 컨트롤 플레인 모듈이다.
- **하이퍼텍스트 전송 프로토콜(Hypertext Transfer Protocol, HTTP)**: L7 웹 트래픽 전송 표준 규격이다.
- **보안 하이퍼텍스트 전송 프로토콜(Hypertext Transfer Protocol Secure, HTTPS)**: TLS 상에서 동작하여 데이터 패킷을 암호화 전송하는 L7 프로토콜이다.
- **Ingress 규칙 통지(Ingress Rule Notification)**: API 서버가 인그레스 설정 변경 이벤트를 인그레스 컨트롤러로 릴레이하는 단계이다.
- **외부 경로 설치(External Route Provisioning)**: NGINX/Envoy 프록시에 L7 VirtualHost 및 Upstream 서버 구성을 동적으로 반영하는 단계이다.
- **EndpointSlice·정책 통지(EndpointSlice & Policy Notification)**: 엔드포인트 파드의 헬스체크 및 보안 정책 업데이트 이벤트를 감지하는 단계이다.
- **종단·정책 규칙 설치(Endpoint & Policy Rule Installation)**: eBPF 맵 또는 iptables 룰셋에 로드밸런싱 테이블과 차단 정책을 적용하는 단계이다.
- **허용 종단 전달(Forwarding to Allowed Endpoint)**: NetworkPolicy 패킷 검사를 통과한 요청을 최종 Pod 가상 인터페이스로 포워딩하는 단계이다.

</details>

```text
1. Ingress 규칙 변경 등록 (API Server Notify)
        │
        ▼
2. 외부 경로 및 TLS 설정 반영 (Ingress Controller Reload)
        │
        ▼
3. EndpointSlice & NetworkPolicy 변경 알림 (Kube-apiserver Watch)
        │
        ▼
4. eBPF / iptables 패킷 포워딩 규칙 설치 (CNI & Kube-proxy)
        │
        ▼
외부 HTTP / HTTPS Client 요청 진입
        │
        ▼
NetworkPolicy 수신(Ingress) 검사 & Readiness Probe 검증
        ├─ [불충족/비정상] 패킷 Drop 또는 HTTP 503 Service Unavailable 반환
        └─ [충족/정상] 5. 허용 종단 Pod 전달 (Pod-to-Pod Direct Forwarding)
```

### 동작 원리

1. **Ingress 규칙 통지**: 사용자가 Ingress 룰을 생성하면 **API 서버**가 이벤트를 감지하여 Ingress 컨트롤러에 전달한다.
2. **외부 경로 설치**: Ingress 컨트롤러가 Envoy/NGINX 내부 라우팅 테이블 및 **TLS** 인증서를 동적으로 갱신한다.
3. **EndpointSlice·정책 통지**: 파드 생성/삭제에 따른 **EndpointSlice** 변화와 **NetworkPolicy**를 CNI 데몬에 전달한다.
4. **종단·정책 규칙 설치**: CNI 데몬이 커널 레벨의 **eBPF** 맵이나 iptables에 로드밸런싱 대상 및 접근제어 규칙을 반영한다.
5. **허용 종단 전달**: 외부 **HTTPS** 요청 진입 시 L7 라우팅 및 보안 검사를 통과한 요청을 최종 **파드**로 안전하게 전달한다.

#### 한줄 요약

- Control Plane 이벤트 관측 기반으로 Ingress 프록시 및 eBPF 커널 맵을 동적 업데이트하여 파드에 패킷을 전달하는 프로세스 준수.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **게이트웨이 응용 프로그래밍 인터페이스(Gateway Application Programming Interface, Gateway API)**: 기존 Ingress의 기능적 한계를 극복하고 Infra Provider, Cluster Admin, App Developer 간 역할(Role-oriented)을 분리하여 L4/L7 라우팅을 유연하게 선언하는 차세대 K8s 네트워크 표준 API이다.

</details>

| 비교 항목 | Ingress API | Gateway API (차세대 K8s 표준) |
|:---|:---|:---|
| **적용 목적** | 단일 팀 환경의 단순 HTTP/HTTPS 웹 서비스 외부 노출 | 멀티 테넌트, 다중 팀(인프라/개발) 역할 분리 및 L4~L7 고급 라우팅 |
| **리소스 모델** | 단일 Ingress 리소스 내 모든 규칙 기술 | GatewayClass, Gateway, HTTPRoute, TLSRoute 등 역할별 객체 분리 |
| **지원 프로토콜** | HTTP, HTTPS 중심 (L7) | HTTP, HTTPS, gRPC, TCP, UDP (L4~L7 통합 지원) |
| **트래픽 제어** | 벤더 전용 Annotation(주석)에 의존적 | 가중치 기반 분판(Traffic Splitting), Header 삽입/수정 표준 지원 |
| **주요 한계** | 벤더 간 Annotation 호환성 부재, 복잡한 정책 표현 한계 | 초기 학습 곡선 존재, CNI/컨트롤러의 Gateway API 지원 여부 확인 필요 |

> 요약: 단순 웹 애플리케이션 외부 단일 경로 노출에는 **Ingress**, 대규모 조직의 역할 분리 및 gRPC/L4 다중 트래픽 제어에는 **Gateway API**를 선정한다.

#### 한줄 요약

- 단순 L7 호스팅 인그레스와 역할 기반 L4~L7 확장성을 제공하는 Gateway API 특성 비교 분석 모델 수용.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **서비스 불가(Service Unavailable, HTTP 503)**: 백엔드 파드가 준비 상태(Readiness)를 달성하지 못했거나 Endpoint가 비어있을 때 Ingress 컨트롤러가 Client에 반환하는 L7 에러 응답 코드이다.

</details>

| 실무 문제점 | 발생 원인 | 해결 대책 | 기대 효과 |
|:---|:---|:---|:---|
| **보안 정책 미작동** | NetworkPolicy 객체를 작성하였으나 미지원 CNI(Flannel 등) 사용 | Calico, Cilium 등 **NetworkPolicy** 지원 **CNI** 선택 및 eBPF 검증 | 파드 간 무단 통신 차단 및 Zero-Trust 보안 격리 달성 |
| **503 에러 발생** | 파드 생성 직후 Readiness Probe 설정 누락으로 미준비 파드에 요청 전송 | 적절한 **Readiness Probe** 딜레이 설정 및 **EndpointSlice** 동기화 | 트래픽 핑퐁 및 서비스 503 오류 발생 방지 |
| **Ingress 설정 혼선** | 단일 Ingress 파일에 개발팀과 인프라팀 설정이 뒤섞여 충돌 발생 | **Gateway API** 도입을 통한 역할별(Gateway/HTTPRoute) 권한 분리 | 운영 조직 간 변경 간섭 제거 및 유연한 라우팅 제어 |
| **대규모 커널 병목** | 수만 개 파드 환경에서 iptables 룰 폭증으로 인한 성능 저하 | iptables를 대체하는 **eBPF** 기반 CNI(Cilium) 전면 도입 | 커널 패킷 처리 지연(Latency) 최소화 및 10배 이상 처리량 향상 |

#### 한줄 요약

- eBPF CNI 기반 NetworkPolicy 실행 검증과 Readiness Probe 최적화, Gateway API 도입을 통한 실무 운영성 확보 체계 구축.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **외부 경로 선택(External Routing Model Selection)**: 조직의 가용 역량과 라우팅 복잡도에 따라 Ingress 또는 Gateway API 모델을 체계적으로 결정하는 설계 원칙이다.

</details>

- **외부 경로 선택** 시 단순 L7 라우팅은 **Ingress**, 멀티테넌트 역할 분리 및 gRPC 제어에는 **Gateway API**를 표준으로 채택하고, 리눅스 커널 내 **eBPF** 기반 CNI를 연동하여 보안과 데이터 패스 성능을 동시에 확보하는 쿠버네티스 통합 네트워킹 구축 체계 적용.

#### 한줄 요약

- eBPF 기반 CNI 패스트 패스 연동 및 Gateway API 표준 적용을 통한 차세대 쿠버네티스 네트워킹 수용 체계 구축.
