---
sidebar:
  order: 40
  label: "040. API 게이트웨이 (API Gateway)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "API 게이트웨이 (API Gateway)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 40
extra:
  question_no: "040"
  source_status: "기출"
  source_history: "120회"
  priority: 50
  priority_note: "120회 기출, API 진입점•정책 집중 구조"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **API Gateway**: 클라이언트와 백엔드 마이크로서비스들 사이에 위치하는 단일 진입점(Single Entry Point) 프록시 서버로, 라우팅, 인증/인가, Rate Limiting, SSL Termination, 응답 변환 등의 공통 정책을 일괄 처리하는 중앙 엣지 서비스.
- **Reverse Proxy**: 외부 클라이언트의 요청을 받아 내부의 여러 백엔드 서버로 요청을 분산 라우팅하고 내부 네트워크 구조를 은닉하는 프록시 서버 구조.
- **BFF (Backend For Frontend)**: 프론트엔드 플랫폼(Web, Mobile, App)별로 최적화된 API 게이트웨이를 각각 별도로 두어 응답 데이터 조합(Aggregation)을 지원하는 아키텍처 패턴.

</details>

- 정의/개념: 마이크로서비스 내부 복잡도를 은닉하고 외부 요청의 단일 관문으로서 라우팅, 보안, 트래픽 차단 및 프로토콜 변환을 일괄 수행하는 중앙 서버인 **API Gateway**
- 배경/필요성: 클라이언트가 수십 개의 마이크로서비스 주소를 개별 관리하는 비효율성 차단, 공통 라우팅/인증 로직의 중복 구현 소멸 및 보안 인프라 일체화 요구성

#### 한줄 요약

- 외부 계약과 내부 서비스를 분리하는 API 게이트웨이가 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Rate Limiting (트래픽 제어)**: 특정 클라이언트(IP/API Key)의 디도스(DDoS) 공격 및 과도한 요청 폭주를 막기 위해 시간당/초당 최대 요청 건수(TPS)를 제한하는 억제 메커니즘.
- **SSL Termination**: 게이트웨이 전단에서 외부 HTTPS 통신 암호화를 해제(SSL 복호화)하여 내부 서비스 간 통신 오버헤드를 줄이는 라우팅 처리.

</details>

- 클라이언트 단일 진입점 역할 및 백엔드 IP 주소 은닉 (**Encapsulation**)
- **Rate Limiting**, **Authentication (JWT)**, **SSL Termination** 등 횡단 관심사 공통 집행
- **BFF (Backend For Frontend)** 패턴 적용을 통한 클라이언트 맞춤형 응답 데이터 필터링/조합

#### 한줄 요약

- 공통 진입 정책과 서비스의 업무 인가 책임을 분리한다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Filter Chain (필터 체인)**: 게이트웨이 내부에 요청(Pre-Filter), 라우팅(Route-Filter), 응답(Post-Filter) 단계별로 커스텀 정책(인증, 헤더 조작, 캐싱)을 순차 적용하는 파이프라인.

</details>

```text
          [경로 라우터]
                 |
         [진입 정책 엔진]
                 |
          [요청 변환기]
                 |
      [응답 변환•조합기]
                 |
          [관측 처리기]
```

선의 의미: 외부 클라이언트의 API 호출이 Gateway 경로 라우터 및 Filter Chain(인증/Rate Limit)을 통과하여 내부 서비스로 전달되고 응답이 재가공되어 반환되는 구조.

| 구성요소 | 핵심 역할 및 기능 | 주요 구현체 및 기술 |
|:---|:---|:---|
| **L7 Router** | URL Path, Header, HTTP Method 기반 백엔드 서비스 동기 매핑 라우팅 | Path Matching, Host Routing |
| **Authentication Filter** | JWT 토큰 검증, OAuth2 인증 인가 검사, **SSL Termination** | Spring Security, Keycloak 연동 |
| **Rate Limiter Filter** | Redis 기반 **Token Bucket / Leaky Bucket** 알고리즘 적용 트래픽 억제 | Redis Rate Limiter |
| **Protocol Translator** | External REST/JSON $\leftrightarrow$ Internal gRPC/Protobuf 간 통신 규약 상호 변환 | gRPC Web, GraphQL Gateway |
| **Circuit Breaker Filter** | 백엔드 장애 수반 시 타임아웃 래칭 및 Fallback 응답 즉시 인가 | Resilience4j |

#### 한줄 요약

- L7 라우팅, 프로토콜 변환, 상관 식별자, 출처 정책, 내부 계약이 결합된다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Token Bucket Algorithm**: 정해진 주기로 버킷에 토큰을 생성하고, 요청 수용 시 토큰을 소비하여 트래픽 제한(Rate Limiting)을 정밀 구현하는 대표적 알고리즘.

</details>

```text
┌──────────────────────────────┐
│ 외부 API 요청 (HTTPS)        │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. SSL Termination           │
│ 2. Pre-Filter (JWT/RateLimit)│
│ 3. L7 Routing & Service Find │
│ 4. 백엔드 서비스 처리        │
│ 5. Post-Filter (Response Agg)│
└──────────────┬───────────────┘
               ▼
        [클라이언트 응답]
```

### 동작 원리

1. **SSL Termination**: 게이트웨이 전단에서 클라이언트 HTTPS SSL 복호화 수행.
2. **Pre-Filter 검증**: JWT 토큰 유효성 검사 및 Redis 기반 **Token Bucket Rate Limiting** 집행 (실패 시 401/429 반환).
3. **L7 Routing**: **Service Discovery (Eureka/K8s)** 참조하여 목적지 Microservice Pod IP 인출.
4. **백엔드 서비스 처리**: 내부 비동기 HTTP / gRPC 라우팅 호출 및 런타임 연산 수행.
5. **Post-Filter & Aggregation**: 서비스 응답 데이터 필터링, CORS 헤더 추가 및 클라이언트 전달.

#### 한줄 요약

- 진입 정책 검증과 업무 인가•서비스 처리를 분리한 흐름이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Kong vs Spring Cloud Gateway**: Kong은 Nginx/Lua 기반의 초고속 API 게이트웨이, Spring Cloud Gateway는 Java/Netty 기반의 Reactive 웹플럭스 지원 게이트웨이.

</details>

| 구현체 및 솔루션 | 기술 기반 | 주요 특징 및 장단점 |
|:---|:---|:---|
| **Kong Gateway** | Nginx / OpenResty (Lua) | 초고속 성능, 풍부한 플러그인 생태계, C/Lua 오버헤드 최저 |
| **Spring Cloud Gateway** | Java / Netty (Spring WebFlux) | **Spring 생태계와 완벽 결합, Non-blocking Async I/O 지원** |
| **AWS API Gateway** | Managed Cloud Service | 완벽한 서버리스(Serverless) 연동, 트래픽 비례 비용 과금 |
| **Envoy Proxy** | C++ | Service Mesh 및 Gateway 겸용 가능, 고성능 L7 라우팅 |

#### 한줄 요약

- 반복 정책이 많으면 API 게이트웨이, 단순 경로는 직접 호출이 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Single Point of Failure (SPOF)**: API 게이트웨이 단일 인스턴스가 다운되면 전체 마이크로서비스 접근이 전면 차단되는 치명적 위험.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| API Gateway 장애 발생 시 전면 서비스 마비 (**SPOF**) | 게이트웨이 수평 이중화(Scale-out) 및 L4 Load Balancer 무장애 라우팅 | 고가용성(HA) 확보 |
| 게이트웨이에 비즈니스 로직(Business Logic) 오염 | 공통 횡단 로직(인증, 라우팅)만 게이트웨이에 두고 비즈니스 로직 철저히 배제 | 게이트웨이 병목 예방 |
| 대용량 트래픽 블로킹 발생 | **Non-blocking Reactive I/O (Spring Cloud Gateway / Envoy)** 선택 | C10K 동시성 무제한 수용 |

> 사례: **Spring Cloud Gateway + Redis Rate Limiter + Keycloak JWT** 엣지 인프라 정착

#### 한줄 요약

- 상태 점검, 선언형 정책, 타임아웃, mTLS로 게이트웨이를 통제한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **API 게이트웨이 선택 기준(API Gateway Selection Criteria)**: 트래픽 규모(TPS), 프레임워크 생태계, 확장성 및 BFF 필요성에 기반한 체계.

</details>

- **API 게이트웨이 선택 기준**에 따라 MSA 시스템 구축 시 **Spring Cloud Gateway 또는 Kong** 기반 중앙 엣지 구축 인가

#### 한줄 요약

- 반복 정책 이익과 추가 홉 비용을 함께 평가하는 것이 핵심이다.
