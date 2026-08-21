---
sidebar:
  order: 42
  label: "042. 서비스 메시: Istio•Envoy"
  badge:
    text: "기출 · 70%"
    variant: note
title: "서비스 메시: Istio•Envoy (Service Mesh)"
date: "2026-08-17T19:25:00+09:00"
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

- **사이드카 및 컨트롤 플레인(Envoy & Istiod)**: 서비스 컨테이너 옆에서 트래픽을 가로채는 데이터 플레인(Envoy)과 정책 및 인증서를 중앙 배포하는 제어부(Istiod).
- **SDK 파편화 및 관측 부재(SDK Fragmentation & Blind Spot)**: 마이크로서비스마다 언어별 클라이언트 라이브러리를 내장하여 업데이트 비용이 폭증하고 서비스 간 전파 경로를 추적하지 못하는 한계.

</details>

- 정의/개념: 마이크로서비스 간 통신(East-West)에 **사이드카 프록시(Envoy)와 컨트롤 플레인(Istiod)** 을 배치하여 mTLS 보안과 관측성을 제공하는 전용 인프라 계층
- 배경/필요성: 애플리케이션 코드 내 통신 라이브러리(SDK) 하드코딩 시 발생하는 **버전 파편화 및 언어별 재구현 오버헤드와 관측 부재** 직면

#### 한줄 요약

- 애플리케이션 코드 변경 없이 사이드카 프록시가 서비스 간 통신·보안·관측을 인프라 수준에서 처리

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **사이드카 패턴(Sidecar Pattern)**: 애플리케이션 컨테이너와 동일한 Pod에 프록시 컨테이너를 함께 배치하여 트래픽을 가로채 처리하는 배치 구조.
- **상호 TLS(mTLS, Mutual TLS)**: 클라이언트와 서버가 상호 인증서를 교환하여 신원을 검증하고 통신을 암호화하는 Zero Trust 기반 보안 프로토콜.

</details>

- **컨트롤 플레인(Istiod)** 과 **데이터 플레인(Envoy)** 역할 분리로 정책과 실행을 분리
- 애플리케이션 코드 수정 없이 **사이드카 프록시** 삽입으로 카나리 배포·트래픽 분할 구현
- 서비스 간 통신을 **mTLS** 기반 강제 암호화하여 Zero Trust 보안 달성

#### 한줄 요약

- 컨트롤·데이터 플레인 분리로 정책을 중앙화하고 사이드카와 mTLS로 애플리케이션 독립 보안을 구현

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Envoy Proxy**: C++ 기반 고성능 L7 프록시로 서비스 메시 데이터 플레인의 표준 구현체.
- **Istiod**: Istio의 컨트롤 플레인 단일 바이너리로 파일럿(라우팅)·시타델(인증서)·갤리(설정)를 통합.

</details>

```text
[ Istio 서비스 메시 구조 ]
Istiod (Control Plane)
└─ 라우팅 정책·mTLS 인증서 생성·xDS로 Envoy에 배포
   │
   ├─ Envoy 사이드카 (주문 Pod)
   │    └─ 주문 워크로드 ↔ Envoy (트래픽 가로채기)
   │         mTLS 암호화 통신
   └─ Envoy 사이드카 (결제 Pod)
        └─ 결제 워크로드 ↔ Envoy (트래픽 가로채기)
```

선의 의미: Istiod에서 Envoy로의 가지는 xDS 기반 정책 배포 관계, Envoy 간 양방향 화살표는 mTLS 암호화 통신 관계

| 구성요소 | 책임 |
|:---|:---|
| **Istiod (컨트롤 플레인)** | 라우팅 정책·mTLS 인증서 생성·xDS로 Envoy 동적 구성 |
| **Envoy (데이터 플레인)** | 사이드카로 트래픽 가로채기·mTLS 암호화·라우팅 실행 |
| 워크로드 (비즈니스 앱) | 비즈니스 로직 실행·네트워크 제어는 Envoy에 위임 |
| 텔레메트리 (Jaeger 등) | Envoy 수집 트레이스·메트릭 기반 분산 추적 |

#### 한줄 요약

- Istiod가 정책을 생성하면 Envoy가 사이드카로 트래픽을 가로채 정책을 집행하고 텔레메트리를 수집

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **xDS 프로토콜(xDS Protocol)**: Istiod가 Envoy에 라우팅(RDS)·클러스터(CDS) 등 구성 정보를 프록시 재시작 없이 실시간 동적으로 전달하는 gRPC 기반 프로토콜.

</details>

```text
1. 정책 동기화 (Istiod → Envoy, xDS)
   └─ 라우팅 룰·mTLS 인증서를 Envoy에 실시간 배포
   │
   ▼
2. 아웃바운드 트래픽 가로채기 (앱 → 발신 Envoy)
   └─ 앱이 발신하는 트래픽을 사이드카 Envoy가 수신
   │
   ▼
3. Envoy 간 mTLS 암호화 통신
   └─ 발신 Envoy↔수신 Envoy 상호 인증서 교환·암호화
   │
   ▼
4. 인바운드 인가 검증 (수신 Envoy)
   └─ 접근 제어 정책(AuthorizationPolicy) 기준 허용 여부 판정
   │
   ▼
5. 목적지 워크로드 전달 및 텔레메트리 수집
```

**동작 원리** 1. **정책 셋업**: Istiod가 xDS로 라우팅 룰·인증서를 Envoy에 실시간 배포
2. **가로채기**: 애플리케이션 발신 트래픽을 사이드카 Envoy가 iptables 기반으로 가로챔
3. **mTLS 통신**: 발신 Envoy와 수신 Envoy 간 상호 TLS 인증 및 암호화 통신 수행
4. **인가 검증**: 수신 Envoy가 AuthorizationPolicy 기준 트래픽 허용 여부 판정
5. **전달**: 인가 통과 시 목적지 애플리케이션에 전달하고 텔레메트리를 수집

#### 한줄 요약

- 정책 배포→트래픽 가로채기→mTLS 암호화→인가 검증→목적지 전달·텔레메트리 수집의 순환 흐름

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **앰비언트 메시(Ambient Mesh)**: 사이드카 대신 노드당 L4 프록시(ztunnel)와 선택적 L7 프록시(Waypoint)로 구성하여 사이드카 자원 오버헤드를 제거한 Istio의 최신 운영 모드.

</details>

| 구분 | 사이드카 모드 (전통 Istio) | 앰비언트 모드 (Ambient Mesh) |
|:---|:---|:---|
| 적용 기준 | 완전한 L7 제어·Pod별 격리 필요 | 자원 효율 우선·사이드카 오버헤드 최소화 |
| 핵심 특징 | Pod별 사이드카·완전한 L4~L7 처리 | 노드당 ztunnel(L4)+선택적 Waypoint(L7) |
| 한계 | 사이드카 자원 오버헤드·Pod 재시작 필요 | L7 세분화 제어에 추가 Waypoint 구성 필요 |

#### 한줄 요약

- 완전한 L7 제어가 필요하면 사이드카, 자원 효율 우선이면 앰비언트 모드 선택

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **사이드카 풋프린트(Sidecar Footprint)**: 대규모 Pod 환경에서 사이드카 프록시가 인프라 자원(메모리·CPU)을 과도하게 소비하는 오버헤드 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 대규모 Pod 환경에서 사이드카 **자원 오버헤드** 급증 | **Ambient Mesh** 전환 또는 불필요한 서비스에서 사이드카 인젝션 비활성화 | 인프라 자원 절감 |
| 사이드카 이중 프록시 경유로 통신 지연 증가 | 미사용 L7 필터 비활성화·타임아웃 설정 최적화 | 프록시 홉 지연 최소화 |
| Istio 정책 업데이트 중 라우팅 오류로 서비스 장애 | **Revision** 기반 카나리 업데이트로 점진 배포·장애 시 롤백 | 전체 통신망 영향 없는 안전한 정책 업데이트 |

#### 한줄 요약

- 자원 오버헤드는 앰비언트로, 통신 지연은 필터 최적화로, 업데이트 장애는 Revision 카나리로 제어

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **서비스 메시 도입 기준**: 서비스 수·Zero Trust 보안 요구·폴리글랏 환경·운영 역량을 종합하여 서비스 메시와 라이브러리 기반 방식을 결정하는 판단 기준.

</details>

- 다수 서비스·이기종 기술 스택·Zero Trust mTLS 요구 환경은 **서비스 메시(Istio)**, 소수 서비스 환경은 **라이브러리(Spring Cloud 등)** 선택

#### 한줄 요약

- 서비스 수가 많고 Zero Trust mTLS 보안이 필요한 환경에서 서비스 메시 도입을 결정
