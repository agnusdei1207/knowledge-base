---
title: "프록시·리버스 프록시 (Proxy Reverse Proxy)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 217
---

# 📖 【암기용】 개념 완전 이해

> 목적: 프록시와 리버스 프록시를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 클라이언트와 서버 사이에서 요청을 대신 전달하고 통제하는 중계 계층
- **왜 필요한가**: 직접 연결만으로는 접근 통제, 캐싱, 로깅, TLS 종료, 내부 서버 은닉을 체계적으로 처리하기 어렵다
- **핵심 직관**: 프록시는 사용자를 대신해 밖으로 나가고, 리버스 프록시는 서버를 대신해 밖에서 들어오는 요청을 받음

## 깊이 이해
- **배경·문제의식**: 기업망은 외부 접속을 통제해야 하고, 웹 서비스는 내부 WAS를 직접 노출하지 않아야 한다. 두 요구가 각각 Forward Proxy와 Reverse Proxy로 분리된다.
- **작동 원리**: Forward Proxy는 클라이언트가 명시적으로 설정해 외부 서버로 요청을 중계한다. Reverse Proxy는 서버 앞에 위치해 외부 요청을 내부 backend로 전달한다.
- **비유**: Forward Proxy는 회사 직원의 대외 창구, Reverse Proxy는 회사 대표번호가 내부 부서로 전화를 연결하는 교환대임
- **구체 예시**: Nginx는 TLS 종료 후 `/api`는 WAS, `/static`은 object storage로 보내고, Squid는 사내 사용자 외부 웹 접근을 로깅한다.
- **흔한 오해·주의점**: 둘 다 중계 계층이지만 보호 대상이 다르다. Forward Proxy는 클라이언트 보호·통제, Reverse Proxy는 서버 보호·분산이 목적임

## 연결 개념
- API Gateway - 리버스 프록시 기능에 인증·쿼터·라우팅 추가
- CDN - 전세계 edge 리버스 프록시와 캐시
- WAF - 리버스 프록시 앞단 또는 내부에서 웹 공격 차단

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 프록시 방향, 보호 대상, 보안·캐시·로드밸런싱 기능 차이를 명확히 분리한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Proxy는 클라이언트 대리, Reverse Proxy는 서버 대리로 요청을 중계·통제하는 네트워크 애플리케이션 계층이다.
> 2. **가치**: 접근 제어, 캐싱, 로깅, TLS 종료, 내부망 은닉, 로드 밸런싱을 중앙에서 수행한다.
> 3. **판단 포인트**: 어느 쪽을 숨기고 보호하는지, L7 정책과 보안 경계가 어디인지가 답안의 핵심이다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 중계 계층 구조 이해 확인 | Forward Proxy vs Reverse Proxy 방향·보호 대상 | 둘을 같은 캐시 서버로 설명 |
| 웹 아키텍처 설계 확인 | TLS termination, header forwarding, backend routing | X-Forwarded-For, Host header 누락 |
| 보안 통제 확인 | 인증, 접근통제, WAF, 내부 IP 은닉 | 프록시 우회와 로그 위변조 리스크 누락 |

> 요약: 프록시 문제는 요청 방향과 보호 대상을 먼저 고정한 뒤 기능과 보안 경계를 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

프록시는 클라이언트와 서버 사이의 중계 계층이다. 직접 연결 구조는 접근 통제, 관측, 내부망 보호를 각 서버에 중복 구현하게 만든다. 프록시는 공통 정책을 중앙화하고 서버 또는 클라이언트 노출을 줄인다.

---

## Ⅱ. 구조 및 구성요소

```text
Forward Proxy: Client -> Proxy -> Internet Server
Reverse Proxy: Client -> Reverse Proxy -> Backend Server Pool
Proxy Layer -> Auth/ACL -> Cache/TLS -> Log/Metric
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Forward Proxy | 내부 클라이언트의 외부 접속 중계 | 사내망 ACL, URL filtering |
| Reverse Proxy | 외부 요청을 내부 서버로 전달 | Nginx, Envoy, HAProxy |
| Policy Engine | 인증·인가·헤더 제어 | JWT, mTLS, IP allowlist |
| Cache/TLS Layer | 응답 캐시와 TLS 종료 | 인증 응답 cache bypass |

> 요약: 프록시는 방향에 따라 클라이언트 보호와 서버 보호로 나뉘며 정책·캐시·TLS 계층을 포함한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Request Receive -> Policy Check -> Header Normalize
-> Cache Lookup or Route Match -> Backend Forward
-> Response Filter -> Log/Metric -> Client Response
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 요청 수신과 출처 확인 | IP, mTLS, JWT 검증 |
| 2 | 정책·헤더 정규화 | X-Forwarded-For 신뢰 경계 |
| 3 | 캐시 조회 또는 backend 라우팅 | cache hit, route match |
| 4 | 응답 필터링과 로그 기록 | access log 100%, trace id |

> 요약: 프록시는 요청을 그대로 넘기지 않고 정책, 헤더, 캐시, 로깅을 거쳐 통제된 요청으로 변환한다.

---

## Ⅳ. 특징

| 구분 | Forward Proxy | Reverse Proxy | 판단 수치 |
|:---|:---|:---|:---|
| 보호 대상 | 내부 클라이언트 | 내부 서버 | 보호 경계가 사용자측인지 서버측인지 |
| 주요 기능 | URL 필터링, 익명화, 캐시 | TLS 종료, LB, WAF, routing | L7 rule 100개 이상이면 관리 체계 필요 |
| 위치 | 클라이언트 egress 경로 | 서버 ingress 경로 | DMZ/Ingress 구간 배치 |
| 로그 관점 | 사용자별 외부 접속 | 서비스별 inbound 요청 | trace id 포함률 100% |

> 요약: Forward Proxy는 egress 통제, Reverse Proxy는 ingress 통제와 backend 보호가 중심이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | Proxy/Reverse Proxy | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 직접 연결 | 중앙 중계 계층 | 공통 정책 3개 이상 중복 시 도입 |
| 비용/성능 | 각 서버 기능 중복 | TLS·캐시·로그 중앙 처리 | TLS CPU, cache hit, p95 지연 측정 |
| 운영/위험 | 서버 직접 노출 | 프록시 병목·우회 리스크 | HA 2대 이상, bypass 차단 |

> 요약: 프록시는 공통 정책 중복을 줄이지만 중계 계층 병목과 우회 경로를 관리해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 헤더 위조 | 외부가 X-Forwarded-For 삽입 | trusted proxy reset, mTLS | spoofed header reject |
| 단일 장애점 | 프록시 1대 구성 | active-active, health check | proxy availability 99.9% |
| 민감정보 캐시 | 사용자별 응답 캐싱 | `Cache-Control: private/no-store` | cache leak incident 0건 |

> 요약: 헤더 신뢰, 이중화, 개인정보 캐시 금지가 프록시 운영의 주요 통제이다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 지연 | proxy added latency p95 20ms 이하 | APM, ingress metric |
| 정책 적용 | ACL/WAF rule hit log 100% | access log, SIEM |
| 가용성 | active-active, failover 30초 이하 | synthetic check |

> 요약: 프록시 도입 후 추가 지연, 정책 로그, failover 시간을 지속 측정한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 외부 ingress는 Nginx/Envoy reverse proxy로 TLS 1.3 종료, WAF, Host/Path routing, access log 100% 수집 구성
2. 사내 egress는 forward proxy로 URL category, malware scan, 사용자별 audit log, DLP 연계 적용
3. `X-Forwarded-*` 헤더는 trusted proxy에서 재작성하고 backend는 proxy subnet과 mTLS만 허용

**결론 (2줄):**
- 기술사 판단: 클라이언트 외부 접속 통제는 Forward Proxy, 서버 내부망 보호와 L7 라우팅은 Reverse Proxy 선택
- 향후 방향: API Gateway와 Service Mesh가 리버스 프록시 기능을 인증, observability, mTLS와 통합하는 방향으로 발전

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "프록시와 리버스 프록시를 설명하시오" | 요청 중계와 정책 적용 흐름 | 방향·보호 대상·기능 비교 |
| 요구사항 명시형 | "웹 서비스 보안 경계를 설계하시오" | TLS, 헤더, WAF, backend 라우팅 | 우회 차단과 로그·지표 |

> 요약: 설명형은 방향 비교, 설계형은 보안 경계와 헤더 신뢰 체계를 중심으로 작성한다.
