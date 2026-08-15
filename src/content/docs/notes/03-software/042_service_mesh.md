---
sidebar:
  order: 42
  label: "042. 서비스 메시: Istio•Envoy (Service Mesh)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "서비스 메시: Istio•Envoy (Service Mesh)"
date: "2026-08-13T14:54:00+09:00"
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

- **Service Mesh**: 마이크로서비스 간(East-West) 네트워크 통신 제어, 라우팅, 보안(mTLS), 분산 트레이싱을 애플리케이션 코드 수정 없이 인프라 레이어(Sidecar Proxy)에서 투명하게 처리하는 아키텍처 계층.
- **Control Plane**: 서비스 메시 전체의 정책 설정, 라우팅 규칙, mTLS 인증서 발급(CA)을 관장하여 데이터 플레인으로 동기화 배포하는 제어 서브시스템 (e.g. Istiod).
- **Data Plane**: 마이크로서비스 컨테이너 옆에 Sidecar 형태로 주입되어, 실제 동기/비동기 네트워크 트래픽 통제를 직접 수행하는 경량 프록시 집합 (e.g. Envoy Proxy).

</details>

- 정의/개념: 마이크로서비스 애플리케이션 코드의 외부 변경 없이, Sidecar Proxy 레이어를 통해 서비스 간(East-West) 트래픽 통제, mTLS 보안 및 분산 관측성을 일관 집행하는 인프라 아키텍처인 **Service Mesh (Istio / Envoy)**
- 배경/필요성: 서비스별 통신 라이브러리는 **정책 편차•업그레이드 중복** 유발

#### 한줄 요약

- 서비스 코드 밖에서 서비스 메시가 통신 정책을 일관되게 집행한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Sidecar Pattern**: 비즈니스 서비스 컨테이너가 존재하는 동일 Pod 내에 Envoy Proxy 컨테이너를 함께 띄워, 모든 인바운드/아바운드 네트워크 트래픽을 가로채어(iptables) 중계 제어하는 배치 구조.
- **mTLS (Mutual TLS)**: 통신하는 양측 마이크로서비스(Sidecar Proxy 간)가 상호 TLS 디지털 인증서를 검증하고 데이터를 암호화하여 제로 트러스트(Zero Trust) 네트워크 보안을 구현하는 기술.

</details>

- **Control Plane (Istiod)** 대 **Data Plane (Envoy Sidecar)** 2대 레이어 분리
- 애플리케이션 코드 밖의 프록시 계층에서 통신 정책 집행
- **mTLS** 기반 자동 암호화 보안 및 **East-West Traffic** 정밀 제어 (Canary, Blue-Green)

#### 한줄 요약

- 제어 플레인, 데이터 플레인, 프록시의 역할 분리가 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

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

| 구성요소 | 책임 |
|:---|:---|
| Istio 제어 플레인 | 정책•인증서•서비스 구성을 **xDS**로 배포 |
| 호출 워크로드 | 대상 서비스 호출 생성 |
| Envoy 데이터 플레인 | 라우팅•mTLS•복원력 정책 집행 |
| 대상 워크로드 | 프록시가 검증한 업무 요청 처리 |
| 텔레메트리 백엔드 | 메트릭•로그•분산 추적 수집 |

#### 한줄 요약

- Istio, Envoy, 서비스 탐색, 텔레메트리가 제어와 요청 경로를 연결한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **xDS Protocol**: Envoy 프록시가 컨트롤 플레인(Istiod)으로부터 라우팅(RDS), 엔드포인트(EDS), 클러스터(CDS), 리스너(LDS) 구성을 동적으로 수신하는 gRPC 기반 제어 프로토콜.

</details>

```text
┌──────────────────────────────┐
│ Istiod Control Plane         │
└──────────────┬───────────────┘
               ▼ 1. xDS 구성 동기화
┌──────────────────────────────┐
│ 2. 아웃바운드 트래픽 포착   │
│ 3. mTLS 보호 통신           │
│ 4. 인바운드 인가 검증       │
│ 5. 대상 워크로드 전달       │
└──────────────────────────────┘
```

### 동작 원리

1. **xDS 구성 동기화**: 제어 플레인이 프록시에 정책•엔드포인트 배포
2. **아웃바운드 트래픽 포착**: 호출을 데이터 플레인 프록시로 전달
3. **mTLS 보호 통신**: 워크로드 신원을 검증하고 트래픽 암호화
4. **인바운드 인가 검증**: 대상 프록시가 정책에 따라 호출 허용 판정
5. **대상 워크로드 전달**: 허용 요청을 애플리케이션 포트로 전달

#### 한줄 요약

- 구성•인증서 배포와 mTLS 신원•인가 판정의 분리가 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Ambient Mesh (Ambient Mode)**: Sidecar Proxy 주입에 따른 Pod 메모리/CPU 오버헤드를 소멸시키기 위해, 노드 단위 ztunnel(L4)과 전용 Waypoint Proxy(L7)로 분리 구동하는 Sidecarless Service Mesh 아키텍처.

</details>

| 비교 항목 | Sidecar Mode (전통적 Istio) | Ambient Mode (최신 Sidecarless) |
|:---|:---|:---|
| 프록시 주입 위치 | 각 Pod 내 **Sidecar Container** 배치 | **노드당 1개 ztunnel (L4)** + **Waypoint Proxy (L7)** |
| 적용 단위 | 워크로드별 프록시 주입•업데이트 | 노드 L4와 선택적 L7 프록시 적용 |
| 자원 비용 | 워크로드 수에 따라 프록시 비용 증가 | 노드 공유로 중복 프록시 비용 감소 가능 |
| 통신 보안 수준 | L4 ~ L7 풀 스택 Sidecar 처리 | L4(ztunnel mTLS) + 선택적 L7(Waypoint) |

#### 한줄 요약

- 세밀 정책은 사이드카, 비용 절감은 앰비언트가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Sidecar Footprint**: 워크로드별 프록시가 사용하는 메모리•CPU와 추가 네트워크 처리 비용.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Sidecar 프록시 대량 주입으로 인한 클러스터 메모리 고갈 (**Sidecar Footprint**) | **Istio Ambient Mode** 전환 또는 `Sidecar` CRD로 이웃 억세스 스코프 제한 | 자원 낭비 최소화 |
| 프록시 홉 추가에 따른 통신 지연 | 불필요한 L7 필터 제거와 지연 예산 측정 | 프록시 처리 비용 제한 |
| 제어•데이터 플레인 업그레이드 위험 | **Revision 기반 Canary Upgrade** 적용 | 점진적 버전 전환과 롤백 |

> 사례: Kubernetes 클러스터 상의 **Istio 1.20+ Ambient Mesh** 구축 및 Kiali / Jaeger 관측성 연동

#### 한줄 요약

- 카나리아 적용, 인증서 자동 순환, 라벨 허용 목록으로 운영 비용을 통제한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **서비스 메시 도입 기준(Service Mesh Adoption Criteria)**: 마이크로서비스 개수 수량, Polyglot 스택 유무, Zero-Trust mTLS 요구 및 K8s 성숙도에 기반한 채택 체계.

</details>

- 다언어 공통 통신 정책은 **Service Mesh**, 단순 환경은 **라이브러리** 선택

#### 한줄 요약

- L7 정책과 L4 보안 요구를 함께 평가하는 것이 핵심이다.
