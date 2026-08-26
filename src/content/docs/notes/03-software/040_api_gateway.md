---
sidebar:
  order: 40
  label: "040. API 게이트웨이"
  badge:
    text: "기출 · 50%"
    variant: note
title: "API 게이트웨이 (API Gateway)"
date: "2026-08-27T00:29:00+09:00"
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

<details><summary>용어 설명</summary>

- **API 게이트웨이(API Gateway)**: 클라이언트와 마이크로서비스들 사이에 위치하여 인증/인가, L7 라우팅, 로드밸런싱, 트래픽 제한을 단일 지점에서 전담하는 리버스 프록시.
- **횡단 관심사(Cross-Cutting Concerns)**: 인증, 로깅, 모니터링, SSL 종료, Rate Limiting 등 모든 서비스에 공통으로 필요한 기능.

</details>

- 정의/개념: 외부 클라이언트와 마이크로서비스 간 경계에서 **L7 동적 라우팅, 인증/인가(JWT), 트래픽 제어(Rate Limiting)** 를 일원화하는 단일 진입점 프록시
- 배경/필요성: 백엔드 마이크로서비스의 내부 IP 직접 노출에 따른 **보안 취약점 증가 및 횡단 관심사의 서비스별 중복 구현 해결 불가**

#### 한줄 요약
- MSA 외부 요청의 단일 진입점으로 인증, 라우팅, 보안 및 트래픽 제어를 집중 처리한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Rate Limiting(속도 제한)**: 토큰 버킷(Token Bucket) 등의 알고리즘으로 클라이언트별 초당 요청 수를 제한하여 백엔드 과부하를 방어하는 기제.
- **BFF(Backend For Frontend)**: 모바일 앱, 웹 브라우저 등 클라이언트 플랫폼별로 최적화된 API 게이트웨이를 분리 구축하는 패턴.

</details>

- 내부 마이크로서비스의 위치를 은닉하는 **단일 진입점(Single Entry Point)** 제공
- **인증(JWT 검증)·트래픽 제어(Rate Limiting)·SSL 종단(Termination)** 등 횡단 관심사 중앙화
- 플랫폼별(Web, iOS, Android) 데이터 애그리게이션을 지원하는 **BFF 패턴(Backend For Frontend)** 지원

#### 한줄 요약
- 단일 진입점 캡슐화, 횡단 관심사 중앙 처리, BFF 플랫폼 최적화를 지원한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **필터 체인(Filter Chain)**: 요청이 인입되어 라우팅되기 전후에 Pre-Filter(인증/로깅), Routing-Filter, Post-Filter(응답 가공)를 거치는 파이프라인.

</details>

| 구성요소 | 책임 |
|:---|:---|
| SSL 종단기 | HTTPS 암호화를 게이트웨이에서 해제하여 내부 백엔드 CPU 부하 절감 |
| 인증/인가 엔진 | OAuth 2.0 / JWT 서명을 검증하고 미인증 요청을 **엣지(Edge)에서 즉시 차단** |
| 트래픽 제어기 | **Token Bucket / Leaky Bucket** 기반 클라이언트별 Rate Limiting 강제 |
| 동적 라우터 | URI 패스(`/api/orders/**`) 및 서비스 레지스트리를 조회하여 백엔드로 디스패치 |

#### 한줄 요약
- SSL 종단, 인증 필터, 트래픽 제어기, 동적 라우터 파이프라인으로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **토큰 버킷(Token Bucket)**: 고정된 용량의 버킷에 일정 주기로 토큰을 채우고 요청 시 토큰을 소모하여 버킷이 비면 429 Too Many Requests를 반환하는 알고리즘.

</details>

```text
클라이언트가 HTTPS로 API 호출 (예: GET /api/v1/orders/10)
        │
   SSL/TLS 종단 및 HTTP 복호화 수행
        │
   JWT 토큰 서명 유효성 및 만료 시간 검증 (실패 시 401 Unauthorized 반환)
        │
   Token Bucket 기반 Rate Limiting 검사 (초과 시 429 Too Many Requests 반환)
        │
   서비스 디스커버리(Eureka/Consul) 조회 -> 인스턴스 IP/Port 확인
        │
   로드밸런싱(Round Robin) 적용하여 대상 마이크로서비스로 요청 전달
        │
   마이크로서비스 응답 수신 후 사후 필터(CORS 헤더 추가 등) 처리 후 클라이언트 반환
```

#### 한줄 요약
- TLS 종단 → JWT 인증 → Rate Limiting 검사 → 디스커버리 라우팅 → 사후 필터 반환 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Spring Cloud Gateway vs Kong vs AWS API Gateway**: Spring 생태계 전용 Netty 게이트웨이, C/Lua 기반 초고성능 Kong, 완전 관리형 클라우드 서비스 AWS API Gateway.

</details>

| 구현 솔루션 | 기반 기술 스택 | 핵심 특징 | 주 적용 환경 |
|:---|:---|:---|:---|
| Spring Cloud Gateway | Java / Spring WebFlux (Netty) | Spring 생태계 완벽 통합, 비동기 논블로킹 | Java/Spring 백엔드 엔터프라이즈 |
| Kong Gateway | Nginx / OpenResty / Lua | **초저지연, 수만 RPS 초고성능**, 풍부한 플러그인 | 폴리글랏 환경, 대규모 글로벌 트래픽 |
| AWS API Gateway | AWS 완전 관리형 클라우드 | 서버리스 연동(Lambda), 인프라 관리 0화 | AWS 클라우드 네이티브 서버리스 |
| Envoy Proxy | C++ | 초경량 고성능, Service Mesh 사이드카 표준 | Kubernetes 이스티오(Istio) 인프라 |

#### 한줄 요약
- Java 환경은 Spring Cloud Gateway, 고성능 폴리글랏은 Kong, 서버리스는 AWS API Gateway를 채택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **SPOF(Single Point of Failure)**: 단일 API 게이트웨이 인스턴스가 다운되면 전체 시스템 접근이 전면 차단되는 단일 장애점 위험.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 단일 게이트웨이 장애 시 전사 서비스 마비(**SPOF**) | 앞단에 **L4 로드밸런서(ALB) 및 게이트웨이 Multi-AZ 오토스케일링** | 단일 인스턴스 무관 99.99% 고가용성 보장 |
| 게이트웨이에 비즈니스 로직 구현으로 성능 병목(Fat Gateway) | 비즈니스 로직 금지 및 **순수 횡단 관심사(인증/라우팅)** 만 격리 | 게이트웨이 경량화 및 5ms 이내 처리 지연 유지 |
| 악의적 크롤러/DDoS 공격으로 백엔드 리소스 고갈 | **Redis 기반 분산 Rate Limiting + IP 블랙리스트 WAF 연동** | 비정상 트래픽 엣지 차단 및 백엔드 보호 |
| 다중 서비스 응답 조합 시 네트워크 오버헤드 | 플랫폼별 전용 게이트웨이를 분리하는 **BFF(Backend For Frontend) 패턴** | 모바일 맞춤형 응답 압축 및 레이턴시 단축 |

#### 한줄 요약
- L4 ALB 다중화, 횡단 기능만 격리, Redis Rate Limiting, BFF 패턴으로 게이트웨이를 최적화한다.

## Ⅶ. 결론

- 단일 진입점은 **API 게이트웨이**, 플랫폼 분기는 **BFF** 선택

#### 한줄 요약
- API 게이트웨이는 내부 마이크로서비스를 안전하게 은닉하고 횡단 정책을 일원화하여 분산 시스템의 복잡도를 해소하는 필수 관문이다.
