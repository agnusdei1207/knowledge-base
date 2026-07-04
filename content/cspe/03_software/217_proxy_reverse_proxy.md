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
- **개요**: 프록시는 클라이언트와 서버 사이에서 요청을 대신 전달·통제하는 **중계 계층(Intermediary Layer)**이며, 누구를 대신하느냐에 따라 **정방향 프록시(Forward Proxy)**와 **역방향 프록시(Reverse Proxy)**로 나뉜다.
- **왜 필요한가**: 클라이언트와 서버가 직접 연결되는 구조만으로는 접근 통제, 캐싱, 로깅, TLS 종료, 내부 서버 은닉을 각 서버마다 중복 구현해야 해 관리가 어렵다.
- **핵심 직관**: 정방향 프록시는 사용자를 대신해 밖으로 나가는 창구이고, 역방향 프록시는 서버를 대신해 밖에서 들어오는 요청을 받는 교환대다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| Forward Proxy(정방향 프록시) | 내부 클라이언트를 대신해 외부로 나가는 요청을 중계 | 회사 직원의 대외 창구 |
| Reverse Proxy(역방향 프록시) | 외부 요청을 받아 내부 서버로 대신 전달 | 회사 대표번호가 내선으로 연결해주는 교환대 |
| TLS Termination(TLS 종료) | 암호화된 접속을 프록시 지점에서 해제하고, 그 뒤 내부 구간은 평문(또는 별도 TLS)으로 전달 | 검문소에서 신원을 확인한 뒤 안쪽은 통행증만 확인 |
| X-Forwarded-For | 원래 클라이언트의 IP를 뒤 서버에 전달하기 위한 HTTP 헤더 | 소포 겉면에 원 발신자 주소를 적어 다음 배송지로 전달 |
| Origin 은닉(내부망 보호) | Reverse Proxy 뒤에 있는 실제 서버 주소를 외부에 감추는 효과 | 대표번호 뒤 내선번호는 외부에 공개되지 않음 |
| ACL(접근 통제 목록) | 특정 IP·사용자만 허용하거나 차단하는 규칙 목록 | 출입이 허용된 방문자 명단 |
| 헤더 위조(Header Spoofing) | 클라이언트가 X-Forwarded-For 같은 신뢰 헤더를 직접 조작해 속이는 공격 | 발신자 주소를 거짓으로 적은 소포 |
| Trusted Proxy(신뢰 경계) | 어느 프록시가 보낸 헤더까지만 믿을지 정하는 경계 | 검문소를 통과한 소포만 주소를 신뢰 |

## 깊이 이해

### 왜 필요했나 (배경)
- 기업망은 내부 직원의 외부 접속을 통제·기록해야 하고(악성 사이트 차단, 감사 로그), 웹 서비스는 내부 WAS를 외부에 직접 노출하지 않아야 한다(공격 표면 축소). 이 두 요구가 각각 Forward Proxy와 Reverse Proxy로 분리돼 발전했다.

### Forward vs Reverse 판별 원리
- 판별 기준은 두 가지다. ① 누구를 보호·통제하는가 ② 누가 프록시를 사용하도록 설정하는가.
- Forward Proxy는 클라이언트 쪽(사내 사용자)이 스스로 프록시 주소를 설정해서 쓴다. 목적은 클라이언트 통제·보호(URL 필터링, 악성코드 검사, 접속 로깅)다.
- Reverse Proxy는 서버 관리자가 서버 앞단에 배치한다. 클라이언트는 프록시가 있는지도 모른 채 접속하며, 목적은 서버 보호·분산(TLS 종료, 로드 밸런싱, 캐싱, WAF)이다.
- 실무 판단: "누구의 정체를 감추고 누구를 지키는가"를 먼저 확인하면 두 방향이 헷갈리지 않는다.

### TLS Termination을 수치로 이해하기
- TLS 핸드셰이크는 RSA/ECDHE 연산 때문에 평문 처리보다 CPU 비용이 훨씬 크다. 내부 WAS 10대가 각각 TLS를 처리하면 10대 모두 암호화 연산 비용을 부담한다.
- Reverse Proxy 1대에서 TLS를 종료(복호화)하고, 그 뒤 내부 구간(프록시-WAS)은 평문 또는 경량 TLS로 전달하면, 암호화 비용이 프록시 1곳으로 집중돼 WAS 10대는 그 비용에서 벗어나 요청 처리에만 CPU를 쓸 수 있다.

### 헤더 신뢰 경계를 수치로 이해하기
- X-Forwarded-For는 원 클라이언트 IP를 뒤 서버에 알려주는 헤더인데, 외부에서 이 헤더를 직접 조작해 보내면(헤더 위조) 접근 통제나 로그가 왜곡될 수 있다.
- 대응은 "신뢰할 수 있는 프록시 목록(trusted proxy)"을 정해, 그 목록 밖에서 들어온 X-Forwarded-For 값은 무시하고 프록시 자신이 실제로 확인한 연결 IP로 덮어쓰는 것이다. 예: 사내망 10.0.0.0/8 대역에서만 온 헤더는 신뢰하고, 그 외 구간에서 온 값은 재작성(reset)한다.

### 비유와 흔한 오해
- **비유**: Forward Proxy는 회사 직원의 대외 창구, Reverse Proxy는 회사 대표번호가 내부 부서로 연결해주는 교환대다.
- **오해**: 둘 다 "중계 서버"라서 같다고 생각하기 쉽지만, 보호 대상이 정반대다. Forward Proxy는 클라이언트를 보호·통제하고, Reverse Proxy는 서버를 보호·분산한다. 이 방향을 헷갈리면 답안에서 기능(캐싱, TLS, 라우팅)을 엉뚱한 쪽에 배치하게 된다.

## 연결 개념
- API Gateway - Reverse Proxy 기능에 인증·쿼터·라우팅을 더한 상위 확장
- CDN - 전 세계에 흩어진 edge Reverse Proxy와 캐시의 집합
- WAF - Reverse Proxy 앞단 또는 내부에서 웹 공격을 걸러내는 보안 계층

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

- 개요: 클라이언트·서버 중계 계층
- 배경: 직접 연결 구조는 접근 통제, 관측, 내부망 보호를 각 서버에 중복 구현하게 만든다.
- 필요성: 인증, 로깅, TLS 종료, 내부망 노출 제어를 공통 정책으로 처리해야 한다.

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

| 구분 | 기존/대안 | Proxy/Reverse Proxy | 선택 기준 |
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
