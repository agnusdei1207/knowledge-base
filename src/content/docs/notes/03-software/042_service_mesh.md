---
sidebar:
  order: 42
  label: "042. 서비스 메시: Istio•Envoy"
  badge:
    text: "기출 · 70%"
    variant: note
title: "서비스 메시: Istio•Envoy (Service Mesh)"
date: "2026-08-26T17:05:00+09:00"
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

<details><summary>용어 설명</summary>

- **서비스 메시(Service Mesh)**: 마이크로서비스 간의 통신(East-West)을 제어, 보호 및 관측하기 위해 애플리케이션 외부에 구축하는 전용 인프라 계층.
- **사이드카 프록시(Sidecar Proxy)**: 비즈니스 컨테이너와 동일한 Pod에 배치되어 모든 인/아웃바운드 네트워크 트래픽을 가로채는 고성능 프록시(Envoy).

</details>

- 정의/개념: 마이크로서비스 간 통신(East-West)에 **사이드카 프록시(Envoy)와 컨트롤 플레인(Istiod)** 을 배치하여 mTLS 보안과 관측성을 제공하는 전용 인프라 계층
- 배경/필요성: 재시도·타임아웃·mTLS를 언어별 SDK로 구현하면 언어 수만큼 중복하고 정책이 바뀔 때마다 전 서비스를 재배포해야 하므로, 통신 제어를 애플리케이션 밖 사이드카 프록시 계층으로 내려 정책을 코드와 분리해 배포할 필요

#### 한줄 요약
- 코드 수정 없이 사이드카 프록시를 통해 서비스 간 통신, 보안, 트래픽 라우팅을 인프라로 전담한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **상호 TLS(mTLS: Mutual TLS)**: 클라이언트와 서버가 서로의 X.509 인증서를 상호 검증하고 통신 패킷을 종단 간 암호화하는 제로 트러스트 보안.
- **컨트롤 플레인 vs 데이터 플레인**: 정책 및 인증서를 중앙 관리 배포하는 컨트롤 플레인(Istiod)과 실제 패킷을 프록시하는 데이터 플레인(Envoy).

</details>

- **컨트롤 플레인(Istiod)과 데이터 플레인(Envoy)** 분리를 통한 중앙 집중형 정책 통제
- 소스 코드 변경 없는 **사이드카 프록시 주입** 기반의 카나리(Canary) 배포 및 트래픽 분할
- 서비스 간 전송 구간에 대한 **자동 mTLS 암호화 및 제로 트러스트(Zero Trust)** 보안

#### 한줄 요약
- 사이드카는 코드 수정 없이 통신 정책을 얻는 대신 홉마다 프록시 지연과 자원을 추가하므로, 서비스 수가 많을수록 이득과 비용이 함께 커진다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **xDS API**: Istiod가 Envoy 프록시들에게 라우팅(RDS), 엔드포인트(EDS), 클러스터(CDS), 리스너(LDS) 구성을 동적 전달하는 gRPC 프로토콜.

</details>

```text
[Istio / Envoy 서비스 메시 아키텍처]
|-- 컨트롤 플레인 (Control Plane: Istiod)
|   |-- 파일럿 (Pilot: xDS API 기반 Envoy 동적 라우팅 설정 배포)
|   |-- 시타델 (Citadel: mTLS CA 인증서 자동 발급 및 순환)
|   `-- 갤리 (Galley: K8s 매니페스트 설정 검증 및 변환)
`-- 데이터 플레인 (Data Plane: Envoy Sidecar)
    |-- [주문 Pod] -> 비즈니스 컨테이너 <-> Envoy 사이드카 (iptables 트래픽 가로채기)
    |                     │ (mTLS 암호화 통신 & Trace ID 주입)
    `-- [결제 Pod] -> Envoy 사이드카 <-> 비즈니스 컨테이너
```

선의 의미: 계층 및 컨트롤 플레인-데이터 플레인 간 통신 구조

| 구성요소 | 책임 |
|:---|:---|
| Istiod | 정책·인증서의 **xDS 배포** |
| Envoy | 트래픽 가로채기와 **mTLS·회복성 실행** |
| 비즈니스 워크로드 | 비즈니스 로직과 **통신 관심사 위임** |
| 관측성 플랫폼 | 트레이스·메트릭 **집계·시각화** |

#### 한줄 요약
- 제어 평면과 데이터 평면이 분리돼 있어 정책 변경이 애플리케이션 재배포 없이 사이드카에만 반영되며, 관측 데이터도 같은 지점에서 자동으로 수집된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **iptables 가로채기**: Pod 기동 시 init 컨테이너가 iptables 룰을 설정하여 애플리케이션의 모든 네트워크 인/아웃바운드를 Envoy로 자동 리다이렉트하는 기법.

</details>

```text
Istiod가 xDS gRPC 프로토콜로 Envoy에 라우팅 룰 및 mTLS 인증서 배포
        │
   주문 서비스가 결제 서비스로 HTTP 호출 (iptables에 의해 Envoy로 가로채짐)
        │
   발신 Envoy가 결제 Envoy와 상호 X.509 인증서 검증 및 mTLS 암호화 터널 수립
        │
   발신 Envoy가 카나리 가중치(90:10)에 맞춰 목적지 결제 Pod 선택 및 전달
        │
   수신 Envoy가 권한 정책(AuthorizationPolicy) 검증 후 결제 컨테이너로 전달
        │
   양측 Envoy가 Jaeger로 분산 트레이싱 Span 데이터 비동기 전송
```

#### 한줄 요약
- mTLS 수립과 인가 검증이 홉마다 반복되는 고정 비용이지만, 그 대가로 서비스 코드는 인증서와 정책을 전혀 알지 않아도 된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **사이드카 모드 vs 앰비언트 메시(Ambient Mesh)**: Pod마다 프록시를 띄우는 전통 방식과 노드당 L4 프록시(ztunnel)와 선택적 Waypoint(L7)를 쓰는 차세대 무사이드카(Sidecarless) 방식.

</details>

| 비교 항목 | 사이드카 모드 (전통 Istio) | 앰비언트 모드 (Istio Ambient Mesh) |
|:---|:---|:---|
| 프록시 배치 | **Pod당 1개 Envoy 사이드카 컨테이너** | **노드당 1개 ztunnel (L4) + 공유 Waypoint (L7)** |
| 인프라 리소스 소비 | Pod 수에 비례하여 메모리/CPU 소비 극심 | **사이드카 오버헤드 90% 이상 절감** |
| 애플리케이션 침투성 | Pod 재시작 필수 (사이드카 주입) | **Pod 재시작 없이 투명하게 메시 적용** |
| 보안 격리성 | 완벽한 Pod 수준 L7 보안 격리 | 노드 레벨 공유 L4 + 네임스페이스 L7 |

#### 한줄 요약
- 완벽한 L7 격리는 사이드카 모드, 대규모 클러스터 자원 절감은 앰비언트 메시를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Sidecar Footprint**: 수천 개의 Pod에 Envoy가 주입될 때 발생하는 클러스터 전체 메모리/CPU 낭비 문제.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 대규모 Pod 환경에서 사이드카 메모리 과소비(Footprint) | **Istio Ambient Mesh 도입 또는 Sidecar 리소스 CRD 최소화** | 인프라 메모리 비용 80% 절감 |
| 프록시 2회 경유로 인한 1~3ms 네트워크 레이턴시 증가 | 불필요한 L7 필터 비활성화 및 **eBPF 기반 소켓 가속(Cilium)** | 프록시 홉 지연 0.5ms 이내로 단축 |
| Istio 버전 업그레이드 시 서비스 순단 위험 | **Revision 기반 카나리 컨트롤 플레인 롤아웃** 적용 | 무중단 점진적 메시 업그레이드 보장 |
| 서비스 간 호출 권한 통제 부재 | **`AuthorizationPolicy` 기반 최소 권한 통제** | 승인되지 않은 서비스 간 통신 원천 차단 |

#### 한줄 요약
- 사이드카는 정책을 코드에서 떼어내는 대신 홉마다 프록시 지연과 메모리를 추가하므로, Ambient Mesh·eBPF로 그 비용을 줄이고 업그레이드는 Revision 카나리로 위험을 나눈다.

## Ⅶ. 결론

- 서비스 통신 보안은 **Istio**, 자원 절감은 **Ambient** 선택

#### 한줄 요약
- 서비스 메시는 애플리케이션과 통신 인프라를 분리하여 보안, 라우팅, 관측성을 일원화하는 클라우드 네이티브의 핵심 계층이다.
