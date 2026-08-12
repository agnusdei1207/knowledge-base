---
sidebar:
  order: 42
  label: "042. 서비스 메시: Istio•Envoy (Service Mesh)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "서비스 메시: Istio•Envoy (Service Mesh)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 42
extra:
  question_no: "042"
  source_status: "기출"
  source_history: "123회, 138회"
  priority: 70
  priority_note: "123•138회 반복, 메시 기반 통신 제어"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Service Mesh**: 마이크로서비스 간(East-West) 네트워크 통신 제어, 라우팅, 보안(mTLS), 분산 트레이싱을 애플리케이션 코드 수정 없이 인프라 레이어(Sidecar Proxy)에서 투명하게 처리하는 아키텍처 계층.
- **Control Plane**: 서비스 메시 전체의 정책 설정, 라우팅 규칙, mTLS 인증서 발급(CA)을 관장하여 데이터 플레인으로 동기화 배포하는 제어 서브시스템 (e.g. Istiod).
- **Data Plane**: 마이크로서비스 컨테이너 옆에 Sidecar 형태로 주입되어, 실제 동기/비동기 네트워크 트래픽 통제를 직접 수행하는 경량 프록시 집합 (e.g. Envoy Proxy).

</details>

- 정의/개념: 마이크로서비스 애플리케이션 코드의 외부 변경 없이, Sidecar Proxy 레이어를 통해 서비스 간(East-West) 트래픽 통제, mTLS 보안 및 분산 관측성을 일관 집행하는 인프라 아키텍처인 **Service Mesh (Istio / Envoy)**
- 배경/필요성: 각 서비스 소스코드 내 통신 라이브러리(Circuit Breaker, Retry, Tracing) 중복 작성 부담 소멸, 언어 독립적(Polyglot) 네트워크 거버넌스 단일화 요구성

#### 한줄 요약

- 서비스 코드 밖에서 서비스 메시가 통신 정책을 일관되게 집행한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Sidecar Pattern**: 비즈니스 서비스 컨테이너가 존재하는 동일 Pod 내에 Envoy Proxy 컨테이너를 함께 띄워, 모든 인바운드/아바운드 네트워크 트래픽을 가로채어(iptables) 중계 제어하는 배치 구조.
- **mTLS (Mutual TLS)**: 통신하는 양측 마이크로서비스(Sidecar Proxy 간)가 상호 TLS 디지털 인증서를 검증하고 데이터를 암호화하여 제로 트러스트(Zero Trust) 네트워크 보안을 구현하는 기술.

</details>

- **Control Plane (Istiod)** 대 **Data Plane (Envoy Sidecar)** 2대 레이어 분리
- 애플리케이션 소스코드 침범 0% (**Zero-code modification**)
- **mTLS** 기반 자동 암호화 보안 및 **East-West Traffic** 정밀 제어 (Canary, Blue-Green)

#### 한줄 요약

- 제어 플레인, 데이터 플레인, 프록시의 역할 분리가 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Envoy Proxy**: C++로 작성된 초고속 L7 프록시로, Dynamic Configuration(xDS API)을 수용하여 Service Mesh의 표준 Data Plane 역할을 수행.
- **Istiod**: 기존 Pilot, Citadel, Galley 통제 시스템이 단일 바이너리로 통합되어 컨트롤 플레인 기능을 총괄 수행하는 Istio의 중앙 제어 daemon.

</details>

```text
                         [Istio 제어 플레인]
                                  |
                                  |
[호출 워크로드] -------- [Envoy 데이터 플레인] -------- [대상 워크로드]
                                  |
                                  |
                         [텔레메트리 백엔드]
```

선의 의미: Istiod 컨트롤 플레인이 xDS API로 Envoy 데이터 플레인에 정책을 하달하고, Sidecar Envoy 프록시 간 mTLS 트래픽 통제 및 텔레메트리 모니터링이 집행되는 구조.

| 구성요소 | 핵심 역할 및 기능 | 주요 기술 사양 |
|:---|:---|:---|
| **Istiod (Control Plane)** | xDS API 기반 Envoy 프록시 동적 설정 배포, Citadel 인증서 발급(CA) | Pilot, Citadel, Galley 통합체 |
| **Envoy (Data Plane)** | **iptables** 트래픽 가로채기, L7 라우팅, **mTLS 암호화**, Circuit Breaker | C++ 기반 고성능 Sidecar Proxy |
| **VirtualService (CRD)** | 서비스 진입 트래픽 라우팅 규칙 및 가중치(Canary 90:10) 설정 | Kubernetes Custom Resource |
| **DestinationRule (CRD)**| 라우팅 후 마운트될 서비스 서브셋(v1/v2), Load Balancing, **mTLS** 정책 | Kubernetes Custom Resource |

#### 한줄 요약

- Istio, Envoy, 서비스 탐색, 텔레메트리가 제어와 요청 경로를 연결한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **xDS Protocol**: Envoy 프록시가 컨트롤 플레인(Istiod)으로부터 라우팅(RDS), 엔드포인트(EDS), 클러스터(CDS), 리스너(LDS) 구성을 동적으로 수신하는 gRPC 기반 제어 프로토콜.

</details>

```text
┌──────────────────────────────┐
│ Istiod Control Plane         │
└──────────────┬───────────────┘
               ▼ (xDS API 동기화)
┌──────────────────────────────┐
│ 1. iptables 트래픽 가로채기  │
│ 2. Sidecar Envoy (Outbound)  │
│ 3. mTLS 암호화 터널링 통신   │
│ 4. Sidecar Envoy (Inbound)   │
│ 5. Target Pod 서비스 전달    │
└──────────────────────────────┘
```

### 동작 원리

1. **xDS 동기화**: Istiod가 VirtualService/DestinationRule 설정을 **xDS API**로 Envoy 프록시들에 실시간 전파.
2. **iptables 가로채기**: App Pod의 Outbound HTTP 요청 발생 시 **iptables** 룰에 의해 Sidecar Envoy로 즉시 굴절.
3. **mTLS 암호화 터널링**: Envoy 간 상호 **mTLS 인증서** 검증 및 TLS 암호화 데이터 송신.
4. **Inbound 수신 & Decrypt**: 타깃 Pod의 Inbound Envoy가 수신하여 mTLS 복호화 및 인가(AuthorizationPolicy) 검증.
5. **Target Pod 전달**: 검증 완결 후 `localhost` 포트를 경유하여 실제 App Container로 클린 요청 하달.

#### 한줄 요약

- 구성•인증서 배포와 mTLS 신원•인가 판정의 분리가 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Ambient Mesh (Ambient Mode)**: Sidecar Proxy 주입에 따른 Pod 메모리/CPU 오버헤드를 소멸시키기 위해, 노드 단위 ztunnel(L4)과 전용 Waypoint Proxy(L7)로 분리 구동하는 Sidecarless Service Mesh 아키텍처.

</details>

| 비교 항목 | Sidecar Mode (전통적 Istio) | Ambient Mode (최신 Sidecarless) |
|:---|:---|:---|
| 프록시 주입 위치 | 각 Pod 내 **Sidecar Container** 배치 | **노드당 1개 ztunnel (L4)** + **Waypoint Proxy (L7)** |
| 애플리케이션 재부팅 | Sidecar 주입 시 Pod 재시작 필요 | **Pod 재시작 0% (Zero Restart)** |
| 메모리/CPU 리소스 오버헤드| 수백 개 Pod 확장 시 프록시 리소스 오버헤드 중복 폭증 | **노드 단위 공유로 자원 소모 60~80% 대폭 절감** |
| 통신 보안 수준 | L4 ~ L7 풀 스택 Sidecar 처리 | L4(ztunnel mTLS) + 선택적 L7(Waypoint) |

#### 한줄 요약

- 세밀 정책은 사이드카, 비용 절감은 앰비언트가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Sidecar Footprint**: 수백~수천 개의 Pod가 배포된 K8s 클러스터에서 각 Pod마다 주입된 Envoy Sidecar가 점유하는 메모리(약 50MB/Pod) 및 CPU 리소스 합산 비용.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Sidecar 프록시 대량 주입으로 인한 클러스터 메모리 고갈 (**Sidecar Footprint**) | **Istio Ambient Mode** 전환 또는 `Sidecar` CRD로 이웃 억세스 스코프 제한 | 자원 낭비 최소화 |
| 프록시 홉(Hop) 추가에 따른 통신 지연(Latency) 증가 | Envoy C++ 라우팅 최적화 및 불필요한 L7 텔레메트리 필터 오프 | latency 1~2ms 수준 유지 |
| Istio 버전 업그레이드 시 서비스 중단 위험 | **Revision 기반 인플레이스 카나리아 업그레이드 (Istio Canary Upgrade)** | 무장애 모듈 업그레이드 |

> 사례: Kubernetes 클러스터 상의 **Istio 1.20+ Ambient Mesh** 구축 및 Kiali / Jaeger 관측성 연동

#### 한줄 요약

- 카나리아 적용, 인증서 자동 순환, 라벨 허용 목록으로 운영 비용을 통제한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **서비스 메시 도입 기준(Service Mesh Adoption Criteria)**: 마이크로서비스 개수 수량, Polyglot 스택 유무, Zero-Trust mTLS 요구 및 K8s 성숙도에 기반한 채택 체계.

</details>

- **서비스 메시 도입 기준**에 따라 마이크로서비스 50개 이상 및 Zero-Trust 보안 인프라 구축 시 **Istio Service Mesh** 인가

#### 한줄 요약

- L7 정책과 L4 보안 요구를 함께 평가하는 것이 핵심이다.
