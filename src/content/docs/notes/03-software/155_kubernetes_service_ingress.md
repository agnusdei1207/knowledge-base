---
sidebar:
  order: 155
  label: "155. 쿠버네티스 서비스•인그레스 (Kubernetes Service Ingress)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "쿠버네티스 서비스•인그레스 (Kubernetes Service Ingress)"
date: "2026-08-10T10:00:00+09:00"
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

<details><summary>핵심 용어</summary>

- **Kubernetes Service**: 수시로 IP가 생성/소멸하는 수십 개의 Pod들에 고정된 단일 Virtual IP(ClusterIP, NodePort, LoadBalancer)를 부여하여 L4 로드밸런싱 및 서비스 디스커버리를 제공하는 객체.
- **Kubernetes Ingress**: 클러스터 외부의 HTTP/HTTPS 트래픽을 URL 경로(`/api`, `/users`) 및 도메인 호스트 기반으로 백엔드 Service로 분기 라우팅하는 L7 로드밸런싱 관문.
- **Ingress Controller (NGINX / ALB Controller)**: Ingress YAML 명세서를 감지하여 실제 AWS ALB나 NGINX Reverse Proxy 설정으로 렌더링하고 TLS/SSL Certificate를 Termination 처리하는 실체 엔진.

</details>

- 정의/개념: 동적 Pod 집합에 단일 고정 VIP 및 L4 라우팅을 제공하는 **Service**와, 외부 트래픽을 도메인/URL 경로별로 L7 분기 전달하는 **Ingress**로 구성된 네트워크 서비스 노출 아키텍처
- Background: Pod 재시작 시 매번 변경되는 가변 IP 문제 해결, 외부 L4 로드밸런서(ELB) 난립 비용 폭증 차단 및 단일 Ingress L7 분기 통합 요구성

#### 한줄 요약

- 파드가 교체돼 주소가 바뀌어도 서비스라는 대표번호는 유지되고 Ingress는 외부 요청의 주소와 경로를 보고 대표번호를 선택한다.

## Ⅱ. 특징 (Service 4대 분류 및 Ingress L7 기능)

<details><summary>핵심 용어</summary>

- **Service Types**: ClusterIP(내부 전용 VIP), NodePort(노드 포트 오픈), LoadBalancer(CSP 클라우드 ELB 연동), ExternalName(외부 CNAME 맵핑).

</details>

- **Service (ClusterIP, NodePort, LoadBalancer, ExternalName 4대 노출 옵션)**
- **Ingress (L7 URL-based Path Routing `/api/v1`, Host-based Routing `api.company.com`)**
- **SSL/TLS Termination & Certificate Management (cert-manager 기반 자동 TLS 암호화)**

#### 한줄 요약

- 서비스는 준비된 파드 목록을 한 주소 뒤에 모으고 인그레스 컨트롤러는 선언된 웹 규칙을 실제 프록시 설정으로 바꾼다.

## Ⅲ. 구조 및 구성요소 (Service vs Ingress 2대 계층 아키텍처)

<details><summary>핵심 용어</summary>

- **kube-proxy & iptables/IPVS**: kube-proxy가 Node마다 상주하며 Service Virtual IP로 유입된 L4 패킷을 실제 Pod IP로 iptables/IPVS 환원 라우팅.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   Service & Ingress Network Topology                   │
├────────────────────────────────────────────────────────────────────────┤
│ [External Client Request] ──► [Ingress (L7 ALB / NGINX)]                │
│                                 │ (Host / Path Routing)                │
│                                 ▼                                      │
│                           [Service (L4 ClusterIP VIP)]                 │
│                                 │ (kube-proxy / IPVS)                  │
│                                 ▼                                      │
│                     [Pod 1 (10.244.1.5)]  [Pod 2 (10.244.2.8)]          │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 외부 트래픽이 Ingress (L7)를 거쳐 Service (L4) VIP로 들어가 백엔드 Pod IP로 도달하는 2단계 패킷 흐름.

| 구분 요소 | Kubernetes Service (L4) | Kubernetes Ingress (L7) |
|:---|:---|:---|
| **OSI 계층 레벨** | **Layer 4 (Transport Layer - TCP/UDP)** | **Layer 7 (Application Layer - HTTP/HTTPS)** |
| **핵심 라우팅 방식**| **Virtual IP (ClusterIP) 기반 로드밸런싱** | **Domain Host & URL Path (`/api`, `/web`) 분기** |
| **클라우드 자원 비용**| Type: LoadBalancer 사용 시 개별 ELB 생성 (비쌈) | **단 1개의 ALB로 수십 개 서비스 L7 통합 (가성비)** |
| **SSL/TLS 기능** | 불가능 | **SSL/TLS Termination 및 cert-manager 자동 연동** |

#### 한줄 요약

- DNS와 인증서가 건물 이름과 신분을 보장하면 인그레스가 안내하고 서비스가 준비된 파드 중 한 곳으로 연결한다.

## Ⅳ. 흐름도 (External Ingress Routing 4단계 흐름)

<details><summary>핵심 용어</summary>

- **Path-based Routing**: `app.com/api` $\rightarrow$ API Service 로, `app.com/pay` $\rightarrow$ Pay Service 로 L7 URL 경로 분기 처리.

</details>

```text
[HTTP Request: app.com/pay] ──► [AWS ALB Ingress Controller]
                                           │
                                           ▼ (Match Path /pay)
 [Pay Pods (10.244.x.x)] ◄── [kube-proxy IPVS] ◄── [Pay Service (ClusterIP)]
```

### 동작 원리

1. **Ingress Ingest**: Client가 `app.com/pay` 로 HTTPS 접속.
2. **L7 Matching**: ALB Ingress Controller가 L7 URL 경로 대조 후 `Pay-Service` 지정.
3. **L4 Forwarding**: `Pay-Service` 가 IPVS 룰을 통해 실시간 준비 완료된 Pay Pod로 패킷 전달 (**Service & Ingress 완결**).

#### 한줄 요약

- 외부 요청은 인그레스에서 호스트와 경로로 서비스가 정해지고 그 서비스의 준비된 파드에만 전달된다.

## Ⅴ. 종류 및 비교 (Service 4대 타입 1:1 비교)

<details><summary>핵심 용어</summary>

- **ClusterIP vs NodePort vs LoadBalancer**: ClusterIP는 클러스터 내부용, NodePort는 노드 IP:Port 개방, LoadBalancer는 Cloud ELB 맵핑.

</details>

| Service 타입 | 네트워크 노출 범위 | 주요 용도 및 특징 |
|:---|:---|:---|
| **ClusterIP (기본값)** | **클러스터 내부 전용** | DB, Internal Pod 간 통신 (외부 접근 100% 불가) |
| **NodePort** | **모든 Node의 동일 포트(30000~32767) 개방**| 온프레미스 노드 테스트, 간단한 외부 노출 |
| **LoadBalancer** | **AWS/Azure Cloud 외부 ELB 자동 프로비저닝**| 대국민 운영 서비스 L4 노출 표준 |
| **ExternalName** | **외부 DNS CNAME 맵핑 제공** | 외부 오라클 DB를 서비스 이름으로 내부 연동 |

#### 한줄 요약

- 서비스는 파드 교체를 숨기는 내부 접점이고 Ingress는 여러 접점을 하나의 외부 주소와 인증서 뒤에 배치하는 규칙이다.

## Ⅵ. 실무 고려사항 및 대책 (Service & Ingress 실무 3대 파행 대책)

<details><summary>핵심 용어</summary>

- **AWS ALB Ingress Controller Target-Type**: `instance` 방식(NodePort 경유) 대신 `ip` 방식(Pod IP 직접 타겟팅)으로 설정하여 L4 노드포트 병목 레이턴시 50% 절감.

</details>

| 3대 네트워크 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Extra Node Hop Latency** | ALB $\rightarrow$ NodePort $\rightarrow$ Pod 2번 점프 | **ALB target-type: ip 로 Pod 직접 타겟팅 튜닝** |
| **2. ELB Cost Surge** | Service 20개마다 LoadBalancer 생성해 비용 폭발| **Ingress 1개로 통합하고 Path-based 라우팅** |
| **3. SSL Certificate Expire**| HTTPS SSL 인증서 만료로 접속 장애 | **cert-manager 연동 Let's Encrypt 자동 갱신** |

> 사례: **카카오 / 당근마켓 / 쿠팡 AWS ALB Ingress Controller & cert-manager 기반 L7 트래픽 통합**

#### 한줄 요약

- 배포 중 파드가 바뀌어도 내부 호출은 서비스 이름을 사용하고 준비 해제와 연결 배출을 묶어 기존 요청이 끝날 시간을 확보해야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Service/Ingress 수립 기준(Networking Standards)**: ClusterIP(내부), Ingress(L7 외부), Target-Type IP 및 cert-manager SSL 자동화성에 의거한 체계.

</details>

- **Service/Ingress 수립 기준**에 따라 전사 K8s 네트워크 구축 시 **Ingress Controller & ClusterIP Service** 필수 적용

#### 한줄 요약

- 내부 통신은 서비스 이름을 기준으로 하고 외부 웹 진입만 Ingress에 모아 주소 안정성과 경로 정책을 분리해야 한다.
