---
title: "로드 밸런서 L4·L7 (Load Balancer L4 L7)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 22
---

# 📖 【암기용】 개념 완전 이해

> 목적: L4·L7 로드 밸런서를 처음 봐도 어떤 기준으로 서버를 고르고 장애 서버를 제외하는지 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 클라이언트 요청을 여러 서버로 분산하고 장애 서버를 제외해 서비스 접속을 유지하는 트래픽 중계 장치
- **왜 필요한가**: 단일 서버는 CPU, connection, NIC, 장애 한계가 있다. 로드 밸런서는 VIP 하나 뒤에 여러 서버를 묶어 처리량, 장애 격리, 무중단 배포를 지원한다.
- **핵심 직관**: 식당 대기줄에서 안내자가 빈 테이블과 주문 종류를 보고 손님을 배정하는 구조다.

## 깊이 이해
- **배경·문제의식**: 웹 서비스는 요청량이 시간대별로 바뀌고 서버 장애가 발생한다. DNS만으로 분산하면 장애 감지와 세션 유지가 제한되므로 로드 밸런서가 health check, 알고리즘, NAT, TLS 처리를 맡는다.
- **작동 원리**: L4는 IP와 TCP/UDP port, connection 정보를 보고 서버를 선택한다. L7은 HTTP Host, URI, header, cookie, gRPC method 같은 애플리케이션 정보를 보고 정책을 적용한다.
- **비유**: L4는 창구 번호만 보고 줄을 나누는 방식이고, L7은 민원 종류와 서류 내용을 보고 담당자를 배정하는 방식이다.
- **구체 예시**: L4 예시 — `VIP 203.0.113.10:443`으로 들어온 요청을 L4가 경로와 무관하게 round-robin으로 3대 서버에 분산한다. L7 예시 — HTTP를 파싱하는 별도의 L7 계층에서 `/api/pay`는 결제 서버 풀로, `/static`은 캐시 서버 풀로 경로 기반 라우팅한다.
- **흔한 오해·주의점**: health check가 통과해도 애플리케이션 오류가 0건이라는 뜻은 아니다. TCP check는 포트 열림만 확인할 수 있고, HTTP check는 status code, body keyword, 응답시간까지 설계해야 한다.

## 연결 개념
- VIP·Real Server — 외부 접속점과 실제 서버 풀
- Health Check — 장애 서버 제외 기준
- Reverse Proxy·API Gateway — L7 정책과 인증·라우팅 확장

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 로드 밸런서 답안은 L4/L7 차이, 분산 알고리즘, health check, session persistence, TLS offload, 장애 우회 지표를 함께 제시한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 로드 밸런서는 VIP로 수신한 트래픽을 L4 connection 또는 L7 request 기준으로 서버 풀에 분산하는 장치이다.
> 2. **가치**: 단일 서버 장애를 pool 단위로 격리하고, CPU·connection·RPS 증가를 수평 확장으로 흡수한다.
> 3. **판단 포인트**: L4는 지연과 처리량, L7은 URI 정책·TLS·쿠키 기반 세션 유지와 p95 latency를 기준으로 선택한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| L4·L7 분산 기준 확인 | TCP/UDP port vs HTTP Host/URI/header | 두 계층 차이를 포트 번호만으로 설명 |
| 고가용성 설계 역량 확인 | health check, failover, persistence | 서버 추가만 쓰고 장애 제외 조건 누락 |
| 운영 지표 이해 확인 | CPS, RPS, active connection, p95 latency | 처리량 지표와 애플리케이션 오류율 분리 누락 |

> 요약: 이 문제는 분산 알고리즘보다 장애 서버 제외와 계층별 정책 선택 근거를 보여야 한다.

---

## Ⅰ. 개요 및 필요성

- 정의: 클라이언트 요청을 여러 서버로 분산하는 네트워크 장치
- 분산 기준: L4는 IP·port·connection 기준, L7은 HTTP Host·URI·header·cookie 기준으로 서버를 선택
- 필요성: 서비스 규모 증가, 서버 장애, 무중단 배포 요구에 대응하려면 VIP, 서버 풀, health check, session persistence 설계가 필요

---

## Ⅱ. 구조 및 구성요소

```text
Client -> VIP Listener
  -> L4 Policy: IP/TCP/UDP Port/Connection
  -> L7 Policy: Host/URI/Header/Cookie
  -> Health Check -> Server Pool
  -> Log/Metric Export
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| VIP/Listener | 클라이언트 접속 대표 주소 | TCP 80/443, UDP 서비스 |
| Algorithm | 서버 선택 규칙 | round-robin, least-connection, hash |
| Health Check | 비정상 서버 제외 | TCP, HTTP status, 응답시간 |
| Persistence | 동일 사용자 세션 유지 | source IP, cookie, consistent hash |
| TLS Offload | LB가 인증서로 TLS를 종단하고 암호화·복호화를 대신 수행 | SNI, cipher suite, cert rotation |

> 요약: 로드 밸런서는 VIP, 알고리즘, 상태 점검, 세션 유지, TLS 처리를 조합해 서버 풀 앞단을 구성한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Request In -> Listener Match -> Health State Check
  -> Algorithm Select -> Persistence Apply
  -> Server Forward -> Response Return -> Metric Record
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | VIP와 port로 listener 선택 | listener hit, SYN accept |
| 2 | health check 결과가 up인 서버만 후보화 | failed check count |
| 3 | 알고리즘과 persistence로 서버 확정 | distribution ratio, stickiness |
| 4 | 응답 반환 후 connection, latency, status code 기록 | p95 latency, HTTP 5xx rate |

> 요약: 로드 밸런싱은 정상 서버 후보를 먼저 좁힌 뒤 알고리즘과 세션 정책으로 서버를 결정한다.

---

## Ⅳ. 특징

| 구분 | L4 로드 밸런서 | L7 로드 밸런서 | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 처리 기준 | IP, TCP/UDP port, connection | HTTP Host, URI, header, cookie | TCP 80/443, TLS SNI |
| 정책 범위 | NAT, DSR, connection 분산 | path routing, header rewrite, WAF 연계 | HTTP status, gRPC method |
| 지연 요인 | session table lookup | TLS offload, HTTP parsing | p95 latency, RPS |
| 세션 유지 | source IP hash | cookie insertion, header affinity | timeout, cookie TTL |

> 요약: L4는 connection 처리량, L7은 애플리케이션 정책과 TLS 처리 요구가 선택 기준이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | L4 | L7 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | transport 계층 proxy 또는 NAT | reverse proxy 기반 request 처리 | URI·header 정책이 없으면 L4 우선 |
| 비용/성능 | parsing 범위 제한, CPS 중심 | CPU·메모리·TLS 비용 증가 | TLS TPS와 p95 latency 목표 |
| 운영/위험 | 포트·세션 중심 장애 | rule 순서, 인증서, HTTP 오류 | 변경 검증과 rollback 체계 |

> 요약: 단순 TCP 분산은 L4, 애플리케이션 라우팅과 보안 정책은 L7로 배치한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 세션 불균형 | source IP hash 편중, long-lived connection | least-connection, weight 조정 | server active connection 편차 |
| 장애 미탐지 | TCP check만 사용 | HTTP `/healthz`와 의존성 점검 분리 | false healthy count |
| TLS 장애 | 인증서 만료, cipher mismatch | 자동 갱신, staging 검증 | cert expiry day, handshake error |

> 요약: 로드 밸런서 운영은 분산 균형, health check 정확도, TLS 수명주기 지표로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 처리량 | CPS/RPS 목표치와 NIC 사용률 70% 이하 | LB metric, interface counter |
| 지연 | p95 latency SLO 준수 | APM, synthetic transaction |
| 가용성 | pool member 장애 시 자동 제외 3회 check 이내 | failover test, event log |

> 요약: 도입 후 성공 여부는 CPS/RPS, p95 latency, health check 기반 자동 제외 시간으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. TCP 기반 내부 서비스는 L4 VIP와 least-connection을 적용하고 active connection 편차 20% 이하를 점검함
2. 웹/API 서비스는 L7 Host·URI routing, cookie persistence, TLS offload를 적용하고 p95 latency와 5xx rate를 배포 기준으로 설정함
3. health check는 TCP port, HTTP status, 응답 body keyword를 분리하고 장애 서버 제외 임계값을 3회 실패 등으로 명시함

**결론 (2줄):**
- 기술사 판단: transport 단순 분산은 L4, HTTP 정책·TLS·WAF 연계는 L7을 선택함
- 향후 방향: Kubernetes Ingress, Gateway API, service mesh와 연동해 LB 정책을 선언형으로 관리하고 telemetry로 검증해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "로드 밸런서를 설명하시오" | VIP, health check, 알고리즘 흐름 | L4·L7 차이와 세션 유지 |
| 요구사항 명시형 | "고가용성 방안을 제시하시오" | 장애 감지, pool 제외, failover | 지표, 리스크, TLS 운영 기준 |

> 요약: 설명형은 분산 원리, 방안형은 장애 제외와 검증 지표 중심으로 답안 축을 바꾼다.
