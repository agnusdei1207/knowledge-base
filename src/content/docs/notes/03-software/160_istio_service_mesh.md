---
sidebar:
  order: 160
  label: "160. 서비스 메시 Istio (Service Mesh Istio)"
  badge:
    text: "기출 · 85%"
    variant: note
title: "서비스 메시 Istio (Service Mesh Istio)"
date: "2026-08-18T02:10:00+09:00"
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

<details><summary>용어 설명</summary>

- **서비스 메시(Service Mesh) 및 Istio**: 마이크로서비스 간 통신을 제어하기 위해 파드 옆에 Envoy 사이드카 프록시를 배치하고, 중앙 제어면인 `istiod`를 통해 mTLS 암호화, 지능형 트래픽 라우팅, 분산 관측성을 제공하는 전용 인프라 계층.
- **통신 제어 코드 파편화 및 가시성 부재(Communication Fragmentation & Observability Gap)**: 언어별(Java/Node/Go)로 재시도, 서킷 브레이커, TLS 로직을 개별 구현함에 따른 유지보수 파편화와 서비스 간 호출 경로 추적 불가의 한계.

</details>

- 정의/개념: 마이크로서비스 간 통신을 제어하기 위해 **Envoy 사이드카와 istiod 제어면을 통해 mTLS, 트래픽 라우팅, 관측성을 제공**하는 서비스 메시 인프라
- 배경/필요성: 수백 개 마이크로서비스 간 통신에서 발생하는 **mTLS 보안 부재, 카나리 트래픽 분기 난제 및 분산 추적 관측 불가 위험** 직면

#### 한줄 요약

- 애플리케이션 코드 수정 없이 프록시 계층에서 마이크로서비스 간 보안(mTLS), 트래픽 라우팅, 분산 추적을 통합 제어

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **상호 TLS 인증(mTLS: Mutual TLS)**: 서비스 간 통신 시 양단간 X.509 인증서를 상호 검증하여 전 구간 암호화 및 제로 트러스트(Zero Trust) 신원을 증명.
- **트래픽 분기(VirtualService & DestinationRule)**: 가중치(Weight) 기반으로 트래픽을 90:10 비율로 분기하여 위험 없는 카나리(Canary) 배포를 수행.

</details>

- 애플리케이션 코드 변경 없이 투명하게 주입되는 **사이드카 프록시 패턴(Sidecar Pattern)**
- 전 구간 패킷 암호화 및 SPIFFE 신원 기반의 **자동 mTLS 제로 트러스트 보안**
- 헤더, 쿠키, 가중치 기반으로 트래픽을 분할하는 **지능형 카나리 배포 및 서킷 브레이커**

#### 한줄 요약

- 제어면(`istiod`)과 데이터면(Envoy)의 분리를 통해 마이크로서비스 통신의 보안과 가시성을 완성

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Istio 제어면 및 데이터면 계층**: 제어면(`istiod`: Pilot, Citadel, Galley 통합)과 데이터면(Envoy Proxy 사이드카, Ingress/Egress Gateway).

</details>

```text
[ Istio 서비스 메시 제어면 및 데이터면 아키텍처 ]

 1. [ 제어면 계층 (Control Plane: istiod) ]
    ┌─────────────────────────────────────────────────────────────┐
    │  • Pilot (xDS 동적 설정 배포)   • Citadel (CA 인증서 발급)  │
    │  • Galley (설정 검증/변환)      • Telemetry (지표/추적 수집)│
    └────────────────────────────┬────────────────────────────────┘
                                 │ (xDS gRPC 설정 및 mTLS 인증서 전달)
                                 ▼
 2. [ 데이터면 계층 (Data Plane: Envoy Proxy Sidecars) ]
    ┌───────────────────────────┐       mTLS 암호화       ┌───────────────────────────┐
    │ [ Order Service Pod ]     │ ──────────────────────► │ [ Payment Service Pod ]   │
    │  • App Container (Port 80)│                         │  • App Container (Port 80)│
    │  • Envoy Sidecar (Proxy)  │ ◄────────────────────── │  • Envoy Sidecar (Proxy)  │
    └───────────────────────────┘    (Tracing/Metrics)    └───────────────────────────┘
```

선의 의미: `istiod` 제어면이 Envoy 프록시들에 xDS 설정과 mTLS 인증서를 배포하고 프록시 간 암호화 통신을 중계하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| istiod (제어면) | xDS API로 프록시 설정을 동적 배포하고 **CA 인증서 발급 및 서비스 디스커버리 총괄** |
| Envoy 프록시 (데이터면) | 파드 내 통신을 가로채 **mTLS 암호화, L7 로드밸런싱, 서킷 브레이커, 메트릭 수집 집행** |
| VirtualService (CRD) | URL 경로, 헤더, **가중치(Weight)에 따른 트래픽 라우팅 규칙 선언** |
| DestinationRule (CRD) | 서브셋(v1/v2) 정의, **로드밸런싱 알고리즘, 연결 풀 및 서킷 브레이커 정책 선언** |
| Ingress/Egress Gateway | 서비스 메시 클러스터의 **외부 진입 및 외부 반출 트래픽 전담 제어** |

#### 한줄 요약

- istiod(정책/인증서 제어), Envoy 프록시(데이터 전달/암호화), VirtualService, DestinationRule이 결합

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **서비스 메시 mTLS 라우팅 5단계 절차**: 요청 가로채기 $\to$ mTLS 상호 인증 $\to$ VirtualService 매칭 $\to$ 서브셋 라우팅 $\to$ 분산 추적 기록.

</details>

```text
[ Istio 프록시 간 mTLS 암호화 및 트래픽 라우팅 파이프라인 ]

 ┌────────────────────────────────────────┐
 │ 1. 송신 파드 앱 요청을 Envoy가 가로챔 │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 2. Citadel 발급 인증서 기반 mTLS 세션 수립
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 3. VirtualService 가중치(90:10) 룰 평가 │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 4. DestinationRule 타깃 서브셋(v2) 전달│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 5. Jaeger/Zipkin 분산 추적 Span 메트릭 기록
 └────────────────────────────────────────┘
```

### 동작 원리

1. 요청 가로채기: iptables에 의해 Order 앱의 모든 아웃바운드 패킷이 로컬 Envoy 사이드카로 투명하게 리다이렉트.
2. mTLS 수립: 송신 측 Envoy와 수신 측 Envoy가 상호 인증서를 교환하여 SPIFFE 신원을 검증하고 세션을 암호화.
3. 규칙 평가: VirtualService 설정을 대조하여 신규 v2 버전으로 10%의 트래픽을 분기(Canary Routing).
4. 서브셋 전달: DestinationRule에 정의된 타깃 파드 IP로 HTTP/2 gRPC 암호화 요청을 전송.
5. 추적 기록: Envoy가 W3C Trace Context 헤더(`traceparent`)를 주입하고 실행 통계를 Jaeger로 회신.

#### 한줄 요약

- 가로채기 $\to$ mTLS 수립 $\to$ 가중치 평가 $\to$ 서브셋 전달 $\to$ 추적 기록의 5단계

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Sidecar Architecture vs Ambient Mesh**: 파드별 1:1 Envoy 주입 방식(Sidecar)과 노드 단위 공유 L4 ztunnel + 선택적 L7 Waypoint 방식(Ambient).

</details>

| 구분 | 사이드카 모델 (Sidecar Architecture) | 앰비언트 메시 (Ambient Mesh: Sidecarless) |
|:---|:---|:---|
| **적용 기준** | 모든 파드에 대해 정밀한 L7 보안 및 트래픽 제어가 필수인 환경 | 대규모 클러스터에서 프록시 메모리 오버헤드를 대폭 절감하려는 환경 |
| **핵심 특징** | **파드마다 Envoy 1:1 주입, 완벽한 L7 정책 및 격리** | **노드당 1개 ztunnel (L4 mTLS) + 필요 시 Waypoint (L7)** |
| **한계** | 파드 수백 개 급증 시 막대한 메모리 낭비 및 파드 재시작 오버헤드 | 신규 아키텍처로서 생태계 및 서드파티 플러그인 성숙도 발전 중 |

#### 한줄 요약

- 정밀 L7 제어는 전통적 Sidecar, 대규모 클러스터 메모리 절감은 Ambient Mesh를 선택

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Envoy 메모리 비대화(Memory Bloat)**: 클러스터 내 모든 서비스의 엔드포인트 정보가 전 Envoy에 브로드캐스트되어 메모리가 수십 MB씩 낭비되는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 전사 서비스 엔드포인트 덤프로 인한 Envoy 메모리 폭증 | **`Sidecar` CRD 도입으로 통신 필요한 타깃 서비스만 명시 제한** | Envoy 메모리 사용량 70% 즉시 절감 |
| 2번의 프록시 홉(Hop)으로 인한 트래픽 레이턴시(5ms) 증가 | **Ambient Mesh (ztunnel) 적용 또는 불필요한 필터 체인 제거** | L4 mTLS 레이턴시 80% 단축 |
| mTLS 미적용 레거시 파드와의 통신 단절 사고 | **`PeerAuthentication` 모드를 `PERMISSIVE` 거쳐 `STRICT` 전환** | 무중단 점진적 mTLS 전환 완수 |

#### 한줄 요약

- Sidecar CRD 스코프 제한, Ambient Mesh 검토, Permissive 점진 전환을 통해 서비스 메시를 안정화

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **클라우드 네이티브 서비스 거버넌스(Cloud-Native Service Governance)**: 서비스 메시(Istio)와 관측성(OpenTelemetry)을 결합하여 전사 마이크로서비스를 통합 통제하는 체계.

</details>

- **Istio 서비스 메시** 기반 마이크로서비스 아키텍처(MSA)의 보안, 트래픽 통제, 관측성을 인프라 계층으로 외재화하는 핵심 플랫폼이며, 사이드카 스코프 최적화와 점진적 mTLS 전환을 통해 운영 안정성을 극대화해야 함

#### 한줄 요약

- Envoy 프록시와 istiod 제어면을 통해 제로 트러스트 보안과 지능형 트래픽 제어를 완성
