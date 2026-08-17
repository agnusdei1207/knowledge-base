---
sidebar:
  order: 40
  label: "040. API 게이트웨이"
  badge:
    text: "기출 • 50%"
    variant: note
title: "API 게이트웨이 (API Gateway)"
date: "2026-08-17T19:20:00+09:00"
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

- **L7 라우팅 및 횡단 관심사(Routing & Cross-Cutting Concerns)**: URI 경로 기반 서비스 분배와 더불어 인증/인가, 로깅, SSL 종료, 속도 제한(Rate Limiting)을 단일 지점에서 처리하는 기능.
- **엔드포인트 노출 및 중복 구현(Direct Exposure & Duplication)**: 내부 마이크로서비스들의 IP/포트가 외부에 노출되어 공격 대상이 되고 공통 보안 로직이 파편화되는 문제.

</details>

- 정의/개념: 외부 클라이언트와 내부 마이크로서비스 간의 경계에서 **L7 동적 라우팅, 인증/인가(JWT), 트래픽 제어(Rate Limiting)**를 일원화하는 진입점 프록시
- 배경/필요성: 각 백엔드 서비스의 엔드포인트 직접 노출에 따른 **보안 취약점 증가 및 서비스별 횡단 관심사 중복 구현 비용** 직면

#### 한줄 요약

- MSA 외부 요청의 단일 진입점으로 인증·라우팅·트래픽 제어를 집중 처리하는 엣지 서버

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **트래픽 제어(Rate Limiting)**: 단위 시간당 허용 요청 수를 초과하는 트래픽을 차단하여 백엔드 과부하와 서비스 거부 공격을 방어하는 제어 메커니즘.
- **SSL 종료(SSL Termination)**: HTTPS 복호화를 게이트웨이에서 집중 처리하고 내부는 HTTP로 통신하여 백엔드 암호화 처리 오버헤드를 감소시키는 기법.

</details>

- 내부 서비스 위치를 외부에 노출하지 않는 **단일 진입점** 및 캡슐화 역할
- **인증(JWT 검증)·트래픽 제어(Rate Limiting)·SSL 종료** 등 공통 횡단 기능 집중 처리
- **BFF 패턴**으로 클라이언트별 응답 데이터 조합 제공

#### 한줄 요약

- 내부 서비스를 캡슐화하고 인증·보안·라우팅을 집중 처리하며 BFF로 클라이언트별 응답을 최적화

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **필터 체인(Filter Chain)**: 요청이 백엔드 서비스에 도달하기 전 인증·로깅·헤더 조작 등의 필터를 순차 통과하는 파이프라인 구조.

</details>

```text
[ API 게이트웨이 파이프라인 구조 ]
외부 클라이언트 (Web/App, HTTPS)
   │
1. TLS 종료 (SSL 복호화)
2. 인증 엔진 (JWT 검증)
3. 트래픽 제어 (Rate Limiting)
4. 필터 체인 (헤더 조작·변환)
5. L7 라우터 (경로 기반 라우팅)
   │
주문 서비스 / 결제 서비스 / 배송 서비스
```

선의 의미: 파이프라인 단계는 요청이 통과하는 필터 체인의 순서를 나타내며, 각 단계에서 정책 위반 시 요청이 차단됨

| 구성요소 | 책임 |
|:---|:---|
| 진입 정책 엔진 | JWT 토큰 검증·Rate Limiting 기반 트래픽 제어 |
| 경로 라우터 | URL 경로·헤더 기반 L7 라우팅으로 대상 서비스 결정 |
| 요청·응답 변환기 | 복수 서비스 응답을 조합하여 클라이언트 최적화 응답 생성 |
| 관측 처리기 | Trace ID 부여·분산 추적 및 메트릭 수집 |

#### 한줄 요약

- 토큰 검증·트래픽 제어·라우팅·응답 조합의 필터 체인으로 요청을 처리하고 관측 데이터를 수집

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **토큰 버킷 알고리즘(Token Bucket)**: 버킷에 일정 속도로 토큰을 채우고 요청마다 토큰을 소비하여 버킷 고갈 시 요청을 차단하는 Rate Limiting 알고리즘.

</details>

```text
클라이언트 HTTPS 요청
   │
   ▼
1. TLS 종료: HTTPS 복호화 후 내부 HTTP 변환
   │
   ▼
2. 인증·인가: JWT 서명 검증·권한 확인
   │
   ▼
3. 트래픽 제어: Token Bucket 기반 Rate Limiting
   │
   ▼
4. L7 라우팅: 서비스 디스커버리 조회 → 대상 서비스 결정
   │
   ▼
5. 백엔드 서비스 호출 및 응답 조합 (BFF)
   │
   ▼
클라이언트 응답 반환
```

**동작 원리**

1. **TLS 종료**: 게이트웨이가 HTTPS를 복호화하고 내부는 HTTP로 전달하여 백엔드 오버헤드 감소
2. **인증**: JWT 서명·만료 시간 검증으로 미인증 요청을 게이트웨이에서 차단
3. **트래픽 제어**: Token Bucket 알고리즘으로 초과 트래픽을 차단
4. **라우팅**: 서비스 디스커버리를 조회하여 URL 경로 기반으로 대상 서비스에 라우팅
5. **응답 조합**: BFF 패턴으로 복수 서비스 응답을 조합하여 클라이언트 최적화 응답 생성

#### 한줄 요약

- TLS 종료→인증→Rate Limiting→라우팅→응답 조합의 순서로 요청을 처리하는 파이프라인

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Spring Cloud Gateway vs Kong**: Java/Spring WebFlux 기반으로 스프링 생태계와 통합성이 높은 Spring Cloud Gateway와 Nginx/Lua 기반 고성능·플러그인 확장성의 Kong.

</details>

| 구현체 | 기반 기술 | 핵심 특징·적용 기준 |
|:---|:---|:---|
| **Kong Gateway** | Nginx / C / Lua | 고성능·플러그인 확장성·비-Java 대규모 트래픽 환경 |
| **Spring Cloud Gateway** | Java / Spring WebFlux | Spring 생태계 통합·비동기 논블로킹(Netty) 지원 |
| **AWS API Gateway** | AWS 관리형 서비스 | 관리형 운영 자동화·트래픽 급증 시 비용 증가 주의 |
| **Envoy Proxy** | C++ | 경량·서비스 메시 사이드카 용도로 주로 활용 |

#### 한줄 요약

- 고성능 범용은 Kong, Spring 생태계는 Spring Cloud Gateway, 관리형 서버리스는 AWS API Gateway 선택

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **단일 장애점(SPOF, Single Point of Failure)**: API 게이트웨이 단일 인스턴스가 장애 시 전체 외부 트래픽이 차단되는 고가용성 위협.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 단일 게이트웨이 인스턴스 장애로 전체 서비스 차단(**SPOF**) | **L4 로드밸런서** 앞단 배치·게이트웨이 다중 인스턴스 구성 | 단일 인스턴스 장애 시에도 서비스 연속성 확보 |
| 비즈니스 로직을 게이트웨이에 구현하여 성능 병목 발생 | 게이트웨이에는 **공통 횡단 기능(인증·라우팅)**만 유지 | 게이트웨이 비대화·병목 방지 |
| 자동화 봇의 과도한 API 호출로 백엔드 과부하 발생 | **Token Bucket 기반 Rate Limiting + Circuit Breaker** 적용 | 백엔드 과부하 및 연쇄 장애 방어 |

#### 한줄 요약

- SPOF는 다중 인스턴스로, 비즈니스 로직 혼입은 횡단 기능 분리로, 봇 트래픽은 Rate Limiting으로 제어

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **API 게이트웨이 도입 기준**: 마이크로서비스 수·공통 보안 정책 필요성·BFF 요구·운영 역량을 기준으로 도입 여부를 결정하는 판단 기준.

</details>

- 분산 MSA 환경에서는 **API 게이트웨이**로 공통 횡단 기능을 집중 처리하고, 단일 모놀리식 환경은 직접 호출 방식을 유지

#### 한줄 요약

- MSA 환경에서 공통 인증·라우팅·트래픽 제어를 API 게이트웨이에 집중하여 서비스 간 정책 일관성을 확보
