---
sidebar:
  order: 160
  label: "160. 서비스 메시 Istio"
  badge:
    text: "기출 · 85%"
    variant: note
title: "서비스 메시 Istio (Service Mesh Istio)"
date: "2026-08-26T13:13:34+09:00"
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

- **서비스 메시(Service Mesh) & Istio**: 마이크로서비스 간 통신을 제어하기 위해 파드 옆에 Envoy 사이드카 프록시를 배치하고, 중앙 제어면인 `istiod`를 통해 mTLS, 트래픽 라우팅, 관측성을 제공하는 전용 인프라 계층.
- **xDS API**: Envoy 프록시가 `istiod` 제어면으로부터 라우팅(RDS), 리스너(LDS), 클러스터(CDS), 엔드포인트(EDS) 설정을 동적으로 주입받는 gRPC 프로토콜.

</details>

- 정의/개념: 마이크로서비스 간 통신을 제어하기 위해 **Envoy 프록시와 istiod 제어면을 통해 mTLS 보안, 트래픽 라우팅, 분산 관측성을 제공하는 인프라 아키텍처**
- 배경/필요성: 재시도·타임아웃·암호화·추적을 언어별 SDK로 중복 구현하면 정책 하나를 바꿀 때마다 전 서비스 재빌드·재배포 비용이 재발하므로, 파드 옆 프록시라는 별도 인프라 계층으로 통신 로직을 걷어내 코드 변경 없이 정책만 갱신할 필요

#### 한줄 요약
- 애플리케이션 코드 수정 없이 인프라 프록시 계층에서 보안, 트래픽 라우팅, 분산 추적을 통합 제어한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **mTLS(Mutual TLS)**: 서비스 간 통신 시 양단간 X.509 인증서를 상호 교환 검증하여 전 구간 암호화 및 제로 트러스트 신원을 증명.
- **VirtualService & DestinationRule**: 가중치 기반 카나리 라우팅(VirtualService)과 서브셋 정의 및 서킷 브레이커(DestinationRule)를 선언하는 CRD.

</details>

- 비즈니스 코드 변경 없이 투명하게 주입되는 **사이드카 프록시 패턴(Sidecar Pattern)**
- 전 구간 패킷 암호화 및 SPIFFE 신원 기반의 **자동 mTLS 제로 트러스트 보안**
- 가중치 및 헤더 기반으로 트래픽을 분할하는 **지능형 카나리 배포 및 서킷 브레이커**

#### 한줄 요약
- 통신 로직을 애플리케이션에서 걷어낸 대가로 프록시 홉과 파드별 리소스 점유를 새로 지불하므로, 서비스 수가 적으면 표준화 이득보다 오버헤드가 앞선다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Istio 2대 계층**: Control Plane(`istiod`: Pilot, Citadel, Galley 통합), Data Plane(Envoy Proxy Sidecars).

</details>

```text
[Istio 서비스 메시 구성]
|-- istiod
|-- Envoy 프록시
|-- VirtualService
|-- DestinationRule
`-- Ingress / Egress Gateway
```

선의 의미: 계층 및 istiod 제어면이 Envoy 프록시들에 xDS 설정과 mTLS 인증서를 배포하고 프록시 간 암호화 통신을 중계하는 구조

| 구성요소 | 책임 | 주요 특징 |
|:---|:---|:---|
| istiod (제어면) | xDS API로 프록시 설정을 동적 배포하고 **CA 인증서 발급 및 서비스 디스커버리 총괄** | 단일 통합 컨트롤러 |
| Envoy 프록시 (데이터면) | 파드 내 통신을 가로채 **mTLS 암호화, L7 로드밸런싱, 서킷 브레이커 집행** | C++ 고성능 프록시 |
| VirtualService (CRD) | URL 경로, 헤더, **가중치(Weight)에 따른 트래픽 라우팅 규칙 선언** | 카나리 배포 규칙 |
| DestinationRule (CRD) | 서브셋(v1/v2) 정의, **로드밸런싱 알고리즘, 연결 풀 및 서킷 브레이커 정책 선언** | 정책 및 타깃 정의 |
| Ingress / Egress Gateway | 서비스 메시 클러스터의 **외부 진입 및 외부 반출 트래픽 전담 제어** | 경계 게이트웨이 |

#### 한줄 요약
- istiod가 정책을 xDS로 배포하고 Envoy가 파드를 대신해 통신을 수행하므로, 애플리케이션은 자신이 암호화·재시도·가중치 분기의 대상이 되고 있다는 사실조차 알지 못한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **mTLS 카나리 라우팅 5단계**: 요청 가로채기 $\to$ mTLS 상호 인증 $\to$ VirtualService 평가 $\to$ 서브셋 전달 $\to$ 분산 추적 Span 기록.

</details>

```text
Order 서비스에서 Payment 서비스로 결제 요청 발생
        │
   [요청 가로채기] iptables 규칙에 의해 Order 앱의 아웃바운드 패킷이 Envoy 사이드카로 리다이렉트
        │
   [mTLS 상호 인증] Citadel 발급 X.509 인증서로 Payment 측 Envoy와 mTLS 세션 수립
        │
   [가중치 룰 평가] VirtualService 명세를 대조하여 신규 v2 버전으로 10% 트래픽 분기 결정
        │
   [서브셋 전달] DestinationRule에 정의된 v2 Payment Pod IP로 암호화 gRPC 요청 전송
        │
   Envoy가 W3C Trace Context(`traceparent`) 헤더를 주입하고 실행 통계를 Jaeger로 회신
```

#### 한줄 요약
- 가로채기·암호화·라우팅·추적이 프록시 한 계층에 모여 앱의 구현 비용은 0이 되지만, 그 대가로 모든 요청이 프록시 홉을 왕복하는 고정 지연을 새로 부담한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Sidecar Architecture vs Ambient Mesh**: 파드별 1:1 Envoy 주입(Sidecar)과 노드 공유 L4 ztunnel + 선택적 L7 Waypoint(Ambient Mesh).

</details>

| 비교 항목 | 사이드카 모델 (Sidecar Architecture) | 앰비언트 메시 (Ambient Mesh: Sidecarless) |
|:---|:---|:---|
| 프록시 배치 방식 | **파드마다 Envoy 컨테이너 1:1 주입** | **노드당 1개 ztunnel (L4) + 전용 Waypoint (L7)** |
| 메모리 오버헤드 | 파드 수백 개 급증 시 막대한 메모리 점유 | **노드 공유형으로 메모리 오버헤드 90% 이상 절감** |
| 파드 생명주기 결합 | 메시 설정 변경 시 파드 재시작 필요 | **파드 재시작 없이 무중단 메시 적용 가능** |
| 최적 적용 환경 | **정밀한 L7 헤더 라우팅 및 완전한 파드 격리** | **대규모 클러스터, 리소스 비용 최적화 환경** |

#### 한줄 요약
- 정밀 L7 제어는 전통적 Sidecar, 대규모 클러스터 메모리 절감은 Ambient Mesh를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Sidecar Memory Bloat**: 클러스터 내 모든 서비스의 엔드포인트 정보가 전 Envoy에 브로드캐스트되어 메모리가 낭비되는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 전사 서비스 엔드포인트 덤프로 인한 Envoy 메모리 폭증 | **`Sidecar` CRD 도입으로 통신 필요한 타깃 서비스만 명시 제한** | Envoy 메모리 사용량 70% 즉시 절감 |
| 2번의 프록시 홉(Hop)으로 인한 트래픽 레이턴시(5ms) 증가 | **Ambient Mesh (ztunnel) 적용 또는 불필요한 필터 체인 제거** | L4 mTLS 레이턴시 80% 단축 |
| mTLS 미적용 레거시 파드와의 통신 단절 사고 | **`PeerAuthentication` 모드를 `PERMISSIVE` 거쳐 `STRICT` 전환** | 무중단 점진적 mTLS 전환 완수 |
| 서비스 장애 시 연쇄적인 다운타임 전파 | **DestinationRule에 `outlierDetection` 서킷 브레이커 설정** | 결함 파드 즉시 자동 격리 |

#### 한줄 요약
- 네 대책은 프록시를 파드마다 둔 대가인 메모리·지연 비용을 스코프 축소나 토폴로지 변경으로 되사는 선택이며, 점진 전환은 즉시 STRICT 적용의 보안 완결성을 전환 기간과 맞바꾼다.

## Ⅶ. 결론

- 통신 보안은 **Istio mTLS**, 트래픽 제어는 **Envoy** 선택

#### 한줄 요약
- Istio 서비스 메시는 Envoy 프록시와 istiod 제어면을 통해 애플리케이션 코드 변경 없이 제로 트러스트 보안과 지능형 트래픽 라우팅을 실현하는 핵심 마이크로서비스 네트워킹 기술이다.
