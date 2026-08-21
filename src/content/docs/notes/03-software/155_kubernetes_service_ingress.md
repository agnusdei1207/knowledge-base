---
sidebar:
  order: 155
  label: "155. 쿠버네티스 서비스•인그레스 (Kubernetes Service Ingress)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "쿠버네티스 서비스•인그레스 (Kubernetes Service Ingress)"
date: "2026-08-18T01:55:00+09:00"
tags:
  - "notes-software"
weight: 155
extra:
  question_no: "155"
  source_status: "기출"
  source_history: "137회"
  priority: 70
  priority_note: "서비스 노출과 경로 제어가 최근 설계축임"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **쿠버네티스 서비스(Service)**: 동적으로 생성/소멸되는 파드들에 고정된 가상 IP(VIP)와 내부 DNS 이름을 부여하여 L4 로드밸런싱과 서비스 디스커버리를 제공하는 객체.
- **쿠버네티스 인그레스(Ingress)**: 외부에서 유입되는 HTTP/HTTPS 트래픽을 단일 진입점에서 접수하여 호스트(Host) 및 URL 경로(Path) 기반으로 백엔드 서비스에 분기 라우팅하는 L7 계층 객체.

</details>

- 정의/개념: 동적으로 변하는 파드 IP를 추상화하여 **단일 진입 VIP를 제공하는 Service(L4)와 경로 기반 라우팅을 제공하는 Ingress(L7)** 네트워킹 아키텍처
- 배경/필요성: 파드의 잦은 재시작과 IP 변경으로 인한 **서비스 탐색(Discovery) 불가 및 L7 경로 기반 외부 트래픽 분기 라우팅 한계** 직면

#### 한줄 요약

- L4 계층의 서비스(Service)와 L7 계층의 인그레스(Ingress)를 결합하여 안정적인 내부 서비스 탐색과 지능형 외부 트래픽 라우팅을 실현

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **4대 서비스 타입**: 내부 전용 ClusterIP, 노드 포트 개방 NodePort, 클라우드 연동 LoadBalancer, 외부 CNAME 매핑 ExternalName.
- **TLS 종료(TLS Termination)**: Ingress 계층에서 HTTPS 인증서를 일괄 복호화(cert-manager 연동)하여 백엔드 파드의 암복호화 연산 부담을 제거.

</details>

- 파드가 교체되어도 변하지 않는 **안정적인 내부 가상 IP(VIP) 및 CoreDNS 도메인 제공**
- 단일 IP/로드밸런서 뒤에서 복수의 마이크로서비스로 분기하는 **L7 URL 경로 기반 라우팅**
- cert-manager 기반의 **SSL/TLS 인증서 자동 발급 및 갱신(TLS Termination)** #### 한줄 요약

- L4 가상 IP 로드밸런싱과 L7 호스트/경로 기반 프록시를 통해 마이크로서비스 네트워킹을 완성

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **인그레스 및 서비스 트래픽 계층**: Ingress Controller(L7 NGINX/ALB), Service VIP(kube-proxy iptables/IPVS), Endpoints(실제 Pod IP 목록).

</details>

```text
[ 쿠버네티스 인그레스(L7) 및 서비스(L4) 트래픽 흐름도 ]

 [ 외부 클라이언트 (HTTPS Request) ]
                 │
                 ▼
 1. [ Ingress Controller (AWS ALB / NGINX Ingress) ] (L7 TLS Termination)
    • Host: `api.example.com` ──► Path: `/order` ➔ Order Service
    • Host: `api.example.com` ──► Path: `/pay`   ➔ Pay Service
                 │
                 ▼
 2. [ Kubernetes Service (ClusterIP VIP: 10.96.0.1) ] (L4 iptables/IPVS)
                 │
                 ▼
 3. [ EndpointSlice (파드 IP 목록: 10.244.1.5, 10.244.2.8) ]
                 │
        ┌────────┴────────┐
        ▼                 ▼
 4. [ Order Pod 1 ]   [ Order Pod 2 ] (Readiness Probe 통과 파드)
```

선의 의미: 외부 HTTPS 요청이 Ingress Controller(L7)에서 경로 매핑 후 Service(L4)와 Endpoints를 거쳐 최종 파드로 전달되는 구조.

| 구성요소 | 책임 |
|:---|:---|
| 인그레스 컨트롤러 (Ingress) | 외부 HTTP/HTTPS 트래픽을 접수하여 **TLS 복호화 및 도메인/URL 경로별 분기 라우팅** |
| 쿠버네티스 서비스 (Service) | 파드 집합에 **고정 가상 IP(VIP)를 부여하고 내부 CoreDNS 질의를 지원(L4)** |
| 엔드포인트슬라이스 (Endpoints)| Readiness Probe를 통과한 **유효한 백엔드 파드들의 실제 IP/Port 목록 실시간 관리** |
| kube-proxy (L4 프록시) | 노드의 커널 iptables 또는 IPVS 규칙을 갱신하여 **Service VIP 트래픽을 파드로 부하분산** |

#### 한줄 요약

- 인그레스 컨트롤러(L7 분기), 서비스 VIP(L4 추상화), EndpointSlice(파드 목록)가 결합

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **인그레스 트래픽 전달 5단계 파이프라인**: HTTPS 요청 수신 $\to$ TLS 복호화 $\to$ Ingress Path 매칭 $\to$ Service VIP 전달 $\to$ 파드 수신.

</details>

```text
[ 쿠버네티스 외부 트래픽 유입 및 서비스 라우팅 파이프라인 ]

 ┌────────────────────────────────────────┐
 │ 1. 외부 사용자 HTTPS 도메인 요청 접수  │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 2. Ingress: TLS 인증서 종료(Termination)│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 3. Ingress: URL Path 룰 매칭 (Service 결정)
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 4. kube-proxy / IPVS: 준비된 Pod IP 선택│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 5. 타깃 파드 컨테이너로 HTTP 요청 전달 │
 └────────────────────────────────────────┘
```

### 동작 원리

1. 요청 접수: 외부 사용자가 `https://app.com/order` URL로 DNS 질의 후 인그레스 로드밸런서로 접속.
2. TLS 복호화: Ingress Controller가 보유한 TLS 인증서(Secret)로 HTTPS 패킷을 복호화(TLS Termination).
3. Path 매칭: Ingress 규칙(`spec.rules.http.paths`)을 대조하여 `/order` 경로에 지정된 `order-service`를 선정.
4. 파드 IP 선택: Endpoints에서 Readiness 점검을 통과한 건강한 파드 IP(`10.244.1.5`)를 로드밸런싱 알고리즘으로 선정.
5. 요청 전달: 선택된 백엔드 파드 컨테이너의 타깃 포트(8080)로 평문 HTTP 요청을 즉시 프록시 전달.

#### 한줄 요약

- 요청 접수 $\to$ TLS 복호화 $\to$ Path 매칭 $\to$ 파드 IP 선택 $\to$ 컨테이너 전달의 5단계

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Service(L4) vs Ingress(L7)**: L4 전송 계층 패킷 전달(Service)과 L7 응용 계층 경로 라우팅(Ingress).

</details>

| 구분 | 쿠버네티스 서비스 (Service: L4) | 쿠버네티스 인그레스 (Ingress: L7) |
|:---|:---|:---|
| **적용 기준** | 클러스터 내부 마이크로서비스 간 통신, 단순 L4 TCP/UDP 노출 | 대외 웹 서비스 도메인 통합, URL 경로 기반 마이크로서비스 라우팅 |
| **핵심 특징** | **고정 가상 IP(VIP), CoreDNS 탐색, iptables/IPVS 분산** | **Host/Path 기반 라우팅, TLS Termination, 쿠키 세션 고정** |
| **한계** | HTTP 헤더나 URL 경로 기반의 세부 분기 라우팅 불가 | 별도의 Ingress Controller(NGINX/ALB 등) 설치 및 운영 필수 |

#### 한줄 요약

- 내부 통신과 L4 로드밸런싱은 Service, 외부 웹 도메인 통합과 L7 라우팅은 Ingress를 선택

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **AWS ALB Ingress Controller Target-Type IP**: NodePort를 거치는 불필요한 네트워크 홉(Hop)을 건너뛰고 ALB가 VPC CNI 파드 IP로 직접 트래픽을 쏘아주는 고성능 최적화 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| NodePort 경유로 인한 2단계 네트워크 점프 및 불필요한 레이턴시 | **AWS ALB Ingress의 `alb.ingress.kubernetes.io/target-type: ip` 설정** | 네트워크 홉 제거 및 응답 지연 50% 단축 |
| 마이크로서비스마다 LoadBalancer 생성 시 클라우드 ELB 비용 폭증 | **단일 Ingress Controller로 통합하고 Host/Path 기반 분기** | 클라우드 로드밸런서 비용 80% 이상 절감 |
| SSL/TLS 인증서 갱신 누락으로 인한 서비스 접속 불가 사고 | **`cert-manager` 도입 및 Let's Encrypt 자동 갱신 파이프라인 구축** | 인증서 만료 장애 0건 보장 |

#### 한줄 요약

- Target-Type IP 최적화, Ingress 단일 통합, cert-manager 자동화를 통해 네트워크 성능과 비용을 최적화

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **게이트웨이 API(Kubernetes Gateway API)**: Ingress의 기능적 한계를 극복하기 위해 역할 기반(인프라/개발자)으로 L4~L7 라우팅을 고도화한 차세대 네트워킹 표준.

</details>

- **쿠버네티스 서비스 및 인그레스** 기반 클라우드 네이티브 네트워크 트래픽 제어의 핵심 근간이며, 내부 서비스는 Service VIP로 추상화하고 외부 유입은 Ingress와 Gateway API를 통해 지능적으로 라우팅해야 함

#### 한줄 요약

- L4 서비스 가상 IP와 L7 인그레스 경로 라우팅을 결합하여 고성능 클라우드 네트워킹을 완성
