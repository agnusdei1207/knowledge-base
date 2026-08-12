---
sidebar:
  order: 160
  label: "160. 서비스 메시 Istio (Service Mesh Istio)"
  badge:
    text: "기출 • 85%"
    variant: note
title: "서비스 메시 Istio (Service Mesh Istio)"
date: "2026-08-10T10:00:00+09:00"
tags:
  - "notes-software"
weight: 160
extra:
  question_no: "160"
  source_status: "기출"
  source_history: "123회, 138회"
  priority: 85
  priority_note: "데이터면•제어면과 트래픽 통제가 최근 출제됨"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Service Mesh (서비스 메시)**: MSA(마이크로서비스) 환경에서 서비스 간 통신(East-West Traffic)을 가시화, mTLS 보안 암호화, 카나리(Canary) 라우팅 및 서킷 브레이커(Circuit Breaker)로 통합 제어하는 전용 인프라 레이어.
- **Istio**: Envoy Sidecar 프록시를 각 Pod 옆에 투입하고, 중앙의 `istiod` 데몬이 정책 및 mTLS 인증서를 일괄 배포 관리하는 대표 오픈소스 서비스 메시 플랫폼.
- **Sidecar Proxy Pattern (Envoy)**: 애플리케이션 코드를 전혀 수정하지 않고, Pod 내부 컨테이너 옆에 Envoy 프록시를 1:1 동반 배치(Sidecar)하여 모든 네트워크 트래픽을 가로채 제어하는 디자인 패턴.

</details>

- 정의/개념: 마이크로서비스 간 통신 네트워크 레이어 상에 Envoy Sidecar 프록시를 주입하고, 중앙 Control Plane(istiod)을 통해 mTLS 보안, L7 트래픽 제어, Tracing을 투명하게 수용하는 분산 프레임워크인 **Service Mesh Istio**
- 배경/필요성: 서비스 수가 수백 개로 증가 시 각 개발언어 라이브러리(Java, Go, Node)별로 재시도, 서킷 브레이커, TLS 암호화 코드를 중복 개발하는 비효율 혁신 요구성

#### 한줄 요약

- 각 서비스가 인증서와 재시도 코드를 따로 만들지 않고 통신 전담 프록시가 동일한 보안·경로 규칙을 적용하도록 책임을 옮긴다.

## Ⅱ. 특징 (Istio 3대 핵심 운용 기능)

<details><summary>핵심 용어</summary>

- **mTLS (Mutual TLS)**: 서비스 A와 서비스 B 간 통신 시 양단간 TLS 인증서를 서로 검증하여 100% 암호화 및 0-Trust 보안 구현.

</details>

- **Traffic Management (VirtualService, DestinationRule 기반 카나리 배포 & Traffic Splitting)**
- **Zero-Trust Security (Automatic mTLS encryption & SPIFFE/SPIRE 기반 워크로드 신원 인증)**
- **Observability (Kiali, Jaeger, Prometheus 연동으로 전사 서비스 맵 및 Distributed Tracing 시각화)**

#### 한줄 요약

- Istiod는 교통 규칙을 배포하고 데이터면 프록시는 각 통신 지점에서 신원 확인, 경로 선택, 기록 생성을 수행한다.

## Ⅲ. 구조 및 구성요소 (Control Plane vs Data Plane 아키텍처)

<details><summary>핵심 용어</summary>

- **istiod (Control Plane) & Envoy (Data Plane)**: istiod가 YAML 정책을 번역해 각 Envoy 프록시로 동적 전달(xDS API).

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Istio Service Mesh Topology                     │
├────────────────────────────────────────────────────────────────────────┤
│ CONTROL PLANE: [istiod (Pilot + Citadel + Galley)]                     │
│                     │ (xDS Config / mTLS Cert Push)                    │
│                     ▼                                                  │
│ DATA PLANE (Pod A)                       DATA PLANE (Pod B)            │
│ ┌─────────────────────────────┐  mTLS    ┌───────────────────────────┐ │
│ │ [App A] ◄─► [Envoy Proxy A] │ ───────► │ [Envoy Proxy B] ◄─►[App B]│ │
│ └─────────────────────────────┘ Encrypted└───────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: Control Plane(istiod)이 수많은 Data Plane(Envoy)으로 xDS 설정을 밀어주고, Envoy끼리 mTLS로 암호화 통신하는 구조.

| 구성요소 레이어 | 핵심 컴포넌트 | 실무 역할 및 기술 메커니즘 |
|:---|:---|:---|
| **Control Plane**| **istiod** | **Pilot(라우팅), Citadel(mTLS인증서), Galley(설정검증) 통합**|
| **Data Plane** | **Envoy Sidecar Proxy**| **Pod 옆에 배치되어 트래픽 가로채기, mTLS, 서킷브레이크** |
| **Ingress/Egress**| **Istio Ingress Gateway**| **클러스터 외곽 경계 L7 진입 트래픽 제어** |
| **Traffic Rules** | **VirtualService / DestinationRule**| **카나리 배포 90%:10% 트래픽 분할 및 Circuit Breaking**|

#### 한줄 요약

- Istiod가 관제실이라면 데이터면은 도로의 검문소, 게이트웨이는 도시 경계의 관문, 관측 연동은 전체 이동 기록을 모으는 장치다.

## Ⅳ. 흐름도 (Canary Deployment Traffic Splitting 흐름)

<details><summary>핵심 용어</summary>

- **VirtualService & DestinationRule**: `weight: 90` (v1) 과 `weight: 10` (v2) 파라미터로 무중단 카나리 배포 트래픽을 제어하는 Istio CRD 객체.

</details>

```text
[User Request] ──► [Istio Ingress Gateway] ──► [VirtualService (Weight Split)]
                                                           │
                                   ┌───────────────────────┴───────────────────────┐
                                   ▼ (90%)                                         ▼ (10%)
                     [DestinationRule v1 Pods]                       [DestinationRule v2 Pods]
```

### 동작 원리

1. **Ingress Ingest**: 트래픽이 Istio Ingress Gateway로 인가 수신.
2. **VirtualService Split**: VirtualService CRD가 트래픽의 90%를 v1으로, 10%를 v2 신규 서비스로 분기 결정.
3. **Envoy Routing**: Envoy 프록시가 DestinationRule 가중치에 따라 백엔드 Pod로 무중단 라우팅 (**Istio Canary 완결**).

#### 한줄 요약

- 주문 서비스의 요청은 양쪽 프록시가 신원을 확인하고 허용 경로를 고른 뒤 결제 서비스로 전달되며 같은 지점에서 지연과 오류도 기록된다.

## Ⅴ. 종류 및 비교 (Sidecar Architecture 대 Ambient Mesh Architecture)

<details><summary>핵심 용어</summary>

- **Istio Ambient Mesh (Sidecarless)**: Pod 마다 Envoy를 붙이던 Sidecar의 메모리 오버헤드를 줄이기 위해, Node 단위 짱짱한 ztunnel(L4)과 Waypoint(L7)로 프록시를 차출하는 차세대 무-사이드카 아키텍처.

</details>

| 비교 항목 | Traditional Sidecar Architecture | Modern Ambient Mesh (Sidecarless) |
|:---|:---|:---|
| **프록시 배치 방식** | **모든 Pod 1개당 Envoy 1개 주입 (1:1)** | **Node당 1개 ztunnel (L4) + 필요시 Waypoint (L7)** |
| **메모리 오버헤드** | 높음 (Pod 1,000개 시 Envoy 1,000개 뜸) | **최저 (Pod 메모리 오버헤드 0MB)** |
| **앱 Pod 재시작** | Envoy 주입/변경 시 Pod 재시작 필요 | **Pod 재시작 0% (Zero-Downtime 설치)** |
| **적용 성숙도** | 엔터프라이즈 검증 완료 표준 | 최신 차세대 표준 전환 중 |

#### 한줄 요약

- Sidecar는 파드마다 Envoy를 두어 L7 기능을 바로 제공하고 Ambient는 노드 L4를 공유한 뒤 필요한 경로에만 웨이포인트를 추가한다.

## Ⅵ. 실무 고려사항 및 대책 (Istio 실무 3대 파행 대책)

<details><summary>핵심 용어</summary>

- **Envoy Sidecar Memory Bloat**: Pod 마다 Envoy가 50MB~100MB씩 차올라 전사 마이크로서비스 전체 메모리 사용량이 수십 GB 추가 폭증하는 현상.

</details>

| 3대 Istio 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Envoy Memory Bloat** | 모든 서비스 설정이 전 Envoy에 덤프됨 | **`Sidecar` CRD로 필요한 타겟 서비스만 핑퐁 제한**|
| **2. High Traffic Latency**| Envoy 2번 거치며 5ms 지연 추가 | **Ambient Mesh (ztunnel) 전환으로 L4 속도 확보** |
| **3. Strict mTLS Crash** | mTLS 안 붙은 미적용 Pod와 통신 불통 | **`PERMISSIVE` 모드 경유 후 `STRICT` 모드 격상**|

> 사례: **토스 / 당근마켓 / 쿠팡 Istio Service Mesh 및 Kiali / Jaeger 관제 운용**

#### 한줄 요약

- 일부 서비스에서 암호화 전환과 재시도 정책을 먼저 관찰하면 숨은 평문 호출과 애플리케이션 재시도의 중첩을 전체 적용 전에 찾을 수 있다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Service Mesh 수립 기준(Service Mesh Standards)**: Istio VirtualService/DestinationRule, Automatic mTLS, Sidecar CRD optimization 및 Ambient Mesh 선제성에 의거한 체계.

</details>

- **Service Mesh 수립 기준**에 따라 차세대 대규모 MSA 구축 시 **Istio Service Mesh & Ambient Mesh** 필수 적용

#### 한줄 요약

- 모든 워크로드에 L7 통제가 필요하면 Sidecar를, L4 암호화가 중심이면 Ambient를 기준으로 삼고 필요한 경로에만 웨이포인트를 배치해야 한다.
