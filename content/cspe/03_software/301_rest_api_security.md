---
title: "REST API 보안 - API Key·OAuth·mTLS (REST API Security)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 301
---

# 📖 【암기용】 개념 완전 이해

> 목적: REST API 보안을 처음 봐도 인증·인가·채널 보호의 차이를 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: REST API 호출 주체와 권한, 전송 구간을 통제하는 보안 체계
- **왜 필요한가**: API는 모바일, SPA, 파트너, 내부 서비스가 같은 엔드포인트를 사용하므로 키 유출·토큰 탈취·권한 초과 호출이 즉시 데이터 노출로 이어짐
- **핵심 직관**: API Key는 출입증 번호, OAuth는 역할이 적힌 임시 허가증, mTLS는 양쪽 신분증을 서로 확인하는 보안 통로임

## 깊이 이해
- **배경·문제의식**: REST는 무상태 요청이어서 서버가 매 호출마다 주체와 권한을 판단해야 함. 쿠키 기반 세션만으로는 외부 연동, 서버 간 호출, 모바일 앱 배포 환경을 모두 다루기 어렵다.
- **작동 원리**: API Key는 애플리케이션 식별과 호출량 제어에 적합함. OAuth 2.0/OIDC는 사용자 위임 권한을 Access Token·Scope·Audience로 표현함. mTLS는 TLS 핸드셰이크에서 서버와 클라이언트 인증서를 함께 검증함.
- **비유**: 건물 출입에서 카드 번호는 API Key, 임시 방문증은 OAuth 토큰, 신분증 대조와 전용 통로는 mTLS에 해당함.
- **구체 예시**: 결제 API는 API Key로 파트너를 식별하고, OAuth scope `payment:write`로 결제 권한을 제한하며, mTLS로 파트너 서버 인증서 지문을 확인함.
- **흔한 오해·주의점**: API Key는 사용자 권한을 증명하지 못함. OAuth 토큰도 TLS, 만료 시간 5~15분, 재발급 토큰 회전 없이는 탈취 대응이 제한됨.

## 연결 개념
- API Gateway: 인증·인가·Rate Limit을 중앙에서 집행
- OAuth 2.0/OIDC: 위임 권한과 사용자 인증 정보 분리
- Zero Trust: 네트워크 위치보다 주체·기기·권한을 매 요청 검증

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. API 보안은 인증 수단 나열이 아니라 호출 주체, 권한 범위, 전송 채널, 감사 추적을 연결해 답안을 구성한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: REST API 보안은 API Key, OAuth 2.0/OIDC, mTLS, Rate Limit, 감사 로그로 호출 주체와 권한을 매 요청 검증하는 통제 구조이다.
> 2. **가치**: 무상태 API에서 키 유출, 토큰 탈취, 권한 초과 호출, 중간자 공격을 인증·인가·암호화·탐지 계층으로 분리 통제한다.
> 3. **판단 포인트**: 외부 파트너는 API Key+mTLS, 사용자 위임은 OAuth/OIDC, 내부 서비스 간 호출은 mTLS+JWT audience 검증 조합을 선택한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| REST API 공격면 이해 확인 | 인증, 인가, 전송 보호, Rate Limit, 감사 로그 | API Key를 사용자 인증으로 단정 |
| OAuth·mTLS 적용 판단 확인 | Token 만료, Scope, Audience, Client Certificate 검증 | TLS만 쓰면 API 보안이 끝난다고 서술 |
| 운영 통제 역량 확인 | 키 회전, 토큰 폐기, 429 제어, SIEM 연계 | 비밀값 저장소와 로그 마스킹 누락 |

> 요약: REST API 보안 답안은 수단별 역할을 분리하고, 요청 단위 검증과 운영 지표를 함께 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: API 호출의 신원·권한·채널 통제
- 배경: 공개 API, 모바일 앱, MSA 내부 호출은 HTTP 기반으로 노출되어 인증 실패가 데이터 유출로 이어짐
- 필요성: 무상태 요청마다 OAuth 2.0/OIDC, TLS, Rate Limit로 주체·권한·호출량을 검증해야 함

---

## Ⅱ. 구조 및 구성요소

```text
Client -> API Gateway -> Auth Server -> Resource Server -> Audit Log
  / API Key 검증
  / OAuth Token 검증
  / mTLS Client Cert 검증
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| API Key | 앱·파트너 식별, Rate Limit 기준 | 사용자 권한 증명 아님, 90일 회전 |
| OAuth/OIDC | 사용자 위임 권한, Scope·Audience 검증 | Access Token 5~15분 만료 |
| mTLS | 서버·클라이언트 상호 인증 | 인증서 CN/SAN, 지문, CRL/OCSP 확인 |
| API Gateway | 인증 전처리, WAF, 429 제어 | 정책 일관성·로그 수집 지점 |

> 요약: API Key는 식별, OAuth는 권한 위임, mTLS는 채널 신뢰를 담당하며 Gateway가 정책 집행 지점이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Request 수신 -> TLS/mTLS 검증 -> Key/Token 검증 -> Scope 판단 -> Service 호출 -> Log 저장
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | TLS 또는 mTLS 핸드셰이크 | TLS 1.2 이상, 인증서 만료·폐기 확인 |
| 2 | API Key 또는 JWT 파싱 | 서명, issuer, audience, exp 검증 |
| 3 | 인가 정책 평가 | HTTP Method, URL, scope 매핑 |
| 4 | 호출량·위협 제어 | 429, IP reputation, WAF rule |
| 5 | 감사 로그 저장 | Trace ID, subject, status, latency 기록 |

> 요약: 요청은 채널 검증, 신원 확인, 권한 평가, 호출량 통제, 감사 기록 순서로 처리된다.

---

## Ⅳ. 특징

| 구분 | 기존/단일 인증 | REST API 보안 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 인증 | Session Cookie 중심 | Key, OAuth, mTLS 병행 | 외부 API 401/403 분리 |
| 권한 | 서버 내부 Role 확인 | Scope·Audience·ABAC 평가 | 최소권한 scope 1~3개 단위 |
| 전송 | TLS 서버 인증 | mTLS 상호 인증 | 인증서 397일 이하 갱신 |
| 운영 | 수동 키 관리 | Secret Manager, 회전, 감사 | 키 90일 회전, p95 401 분석 |

> 요약: REST API 보안은 단일 로그인보다 호출 주체·권한 범위·채널 신뢰를 요청 단위로 분리 검증한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 외부 연동 | API Key 단독 | API Key+mTLS | 파트너 서버 고정, B2B 계약 |
| 사용자 위임 | ID/PW 전달 | OAuth 2.0 Authorization Code+PKCE | 모바일·SPA 사용자 권한 위임 |
| 내부 호출 | 네트워크 ACL | mTLS+JWT audience | Zero Trust, 서비스 메시 |

> 요약: API 보안 수단은 하나를 고르는 문제가 아니라 호출 주체와 위임 여부에 따라 조합하는 문제이다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 키 유출 | 소스 저장소·로그 노출 | Secret Manager, 키 회전, 로그 마스킹 | 노출 키 0건, 회전 준수율 100% |
| 토큰 탈취 | XSS, 저장소 평문 보관 | PKCE, HttpOnly, 짧은 exp, refresh 회전 | 재사용 탐지 건수 |
| 권한 초과 | Scope 설계 누락 | Endpoint-scope 매핑표, ABAC | 403 비율, 정책 테스트 통과율 |

> 요약: 핵심 리스크는 비밀값 노출과 과권한이며, 회전·마스킹·정책 테스트로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 인증 실패 | 401/403 원인별 추적 | Gateway 로그, SIEM |
| 호출량 제어 | 429 정책, 초당 요청 한도 | Rate Limit 대시보드 |
| 암호화·인증서 | TLS 1.2 이상, 만료 30일 전 알림 | 인증서 스캐너, OCSP 로그 |

> 요약: 도입 후에는 인증 실패 원인, 호출량, 인증서 상태를 운영 지표로 관리한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수):**
1. 외부 공개 API는 API Gateway에서 API Key, JWT 서명, Rate Limit 1,000 RPM, WAF OWASP CRS를 일괄 적용함.
2. 사용자 위임 API는 OAuth 2.0 Authorization Code+PKCE, Access Token 10분, Refresh Token 회전, scope 최소화를 적용함.
3. 파트너·내부 서비스 API는 mTLS, 인증서 자동 갱신, SPIFFE ID 또는 SAN 매핑, 감사 로그 1년 보관을 적용함.

**결론 (2줄):**
- 기술사 판단: 단순 식별이면 API Key, 사용자 위임이면 OAuth/OIDC, 서버 간 고신뢰 호출이면 mTLS를 조합함.
- 향후 방향: API 보안은 Gateway 중심에서 서비스 메시, Zero Trust, 정책 코드화(OPA) 기반으로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "REST API 보안을 설명하시오" | Key, OAuth, mTLS 처리 흐름 | 인증·인가·채널 보호 특징 |
| 요구사항 명시형 | "설계하시오", "방안을 제시하시오" | 위협별 통제 매핑, Gateway 정책 | 키 회전·토큰 만료·mTLS 선택 기준 |

> 요약: 설명형은 보안 계층을 폭넓게, 설계형은 호출 주체별 인증 조합과 운영 지표를 중심으로 전개한다.
