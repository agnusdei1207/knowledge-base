---
title: "SSO 단일 로그인 (Single Sign-On SSO)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 98
---

# 📖 【암기용】 개념 완전 이해

> 목적: SSO를 단순 편의 기능이 아니라 IdP 중심 인증, SP 인가, 세션 수명 통제 구조로 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: SSO는 한 번의 IdP 인증으로 여러 서비스에 접근하는 인증 연계 구조
- **왜 필요한가**: 사용자가 서비스마다 비밀번호를 관리하면 재사용, 퇴사자 계정 잔존, 감사 누락 문제가 생긴다. 중앙 IdP는 MFA, 계정 회수, 접속 기록을 한 지점에 모은다.
- **핵심 직관**: SSO는 "한 번 로그인하면 모든 권한이 열림"이 아니라 "인증은 중앙화하고, 인가는 각 서비스가 정책으로 판단"하는 구조임.

## 깊이 이해
- **배경·문제의식**: 기업 SaaS와 내부 시스템이 늘어나면 계정 생성·변경·삭제가 분산된다. SSO는 IdP를 신뢰 중심으로 두고 SP들이 SAML Assertion 또는 OIDC Token을 받아 서비스 세션을 발급하게 함.
- **작동 원리**: 사용자가 SP에 접근하면 SP는 IdP로 리다이렉트한다. IdP는 사용자 인증과 MFA를 수행하고 SAML/OIDC 결과를 SP에 전달한다. SP는 issuer, audience, expiry, signature를 검증한 뒤 로컬 세션과 권한 정책을 적용함.
- **비유**: 회사 본관에서 출입증을 한 번 발급받고 여러 회의실에 들어가지만, 회의실마다 출입 가능 부서는 별도 확인하는 구조임.
- **구체 예시**: 직원 5,000명, SaaS 30개 조직에서 IdP 세션 8시간, SP 세션 1시간, 퇴사자 deprovisioning 4시간 SLA, 관리자 앱은 MFA step-up 적용.
- **흔한 오해·주의점**: SSO는 인증 편의만 주는 기능이 아니다. 단일 장애점, 세션 탈취, 과도한 federation trust가 생기므로 가용성·감사·권한 검토가 함께 필요함.

## 연결 개념
- SAML 2.0 - 기업 브라우저 SSO의 대표 프로토콜
- OIDC - API·모바일·클라우드 SSO의 대표 프로토콜
- RBAC/ABAC - SSO 이후 서비스 권한 결정을 수행하는 모델

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. SSO 편의 설명이 아니라 IdP/SP 신뢰, 세션 수명, 단일 장애점, 인가 정책과 감사 지표를 연결한다.
> 핵심: 인증 중앙화와 인가 분산을 구분하고, 토큰/assertion 검증 위치와 세션 수명 통제를 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SSO는 IdP가 인증을 담당하고 SP가 검증 결과를 받아 서비스 세션과 인가 정책을 적용하는 구조이다.
> 2. **가치**: 계정 수명주기, MFA, 접속 감사, 퇴사자 차단을 중앙 IdP에서 통제한다.
> 3. **판단 포인트**: IdP 가용성, 세션 수명, federation trust, SP 권한 정책, 감사 로그를 함께 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| SSO 구조 이해 확인 | IdP, SP, federation, SAML/OIDC, 서비스 세션 | "한 번 로그인" 편의만 설명 |
| 인증과 인가 분리 확인 | IdP 인증 결과 검증 후 SP가 RBAC/ABAC 적용 | SSO 토큰만 있으면 모든 권한 허용으로 서술 |
| 운영 리스크 판단 확인 | 단일 장애점, 세션 탈취, logout, access review | 가용성·감사·계정 회수 지표 누락 |

> 요약: SSO 답안은 중앙 인증과 서비스별 인가를 분리하고, 세션·장애·감사 통제를 함께 제시해야 한다.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **SSO 단일 로그인** | SSO 단일 로그인 (Single Sign-On SSO)의 핵심 개념 | 이 주제의 본질 |

---

## Ⅰ. 개요 및 필요성

- 개요: 단일 인증 연계 구조
- 배경: SaaS와 내부 업무시스템별 로그인이 분산되면 비밀번호 재사용, 퇴사자 계정 잔존, MFA 정책 누락이 발생한다.
- 필요성: SAML 2.0, OIDC 기반 IdP 중심 SSO로 계정 회수, MFA, 접속 로그를 중앙 감사 기준에 맞춰 통합해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
User -> Service Provider -> Identity Provider
Identity Provider -> SAML Assertion / OIDC Token -> Service Provider
Service Provider -> Session / RBAC or ABAC -> Audit
```

| 구성요소 | 역할 | 검증 포인트 |
|:---|:---|:---|
| User/Device | 인증 요청 주체 | device posture, MFA, risk score |
| IdP | 인증, MFA, 토큰/assertion 발급 | issuer, signing key, availability |
| SP | 인증 결과 검증과 서비스 세션 발급 | audience, expiry, local policy |
| Federation Trust | IdP와 SP 간 신뢰 설정 | metadata, client registration, certificate |
| Audit/Provisioning | 계정 동기화와 접속 기록 | SCIM, SIEM, deprovisioning SLA |

> 요약: SSO는 IdP가 인증을 표준화하고 SP가 검증 결과를 권한 정책과 감사 로그로 연결하는 구조이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
SP Access -> IdP Redirect -> User Authentication / MFA
-> Assertion or Token Issue -> SP Verify -> Session Issue
-> RBAC or ABAC Policy -> Access Log / Logout
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 사용자가 SP 접근 | 보호 리소스, return URL |
| 2 | SP가 IdP로 인증 요청 | SAML AuthnRequest 또는 OIDC request |
| 3 | IdP 인증과 MFA 수행 | 세션 수명, risk-based step-up |
| 4 | SP가 결과 검증 | signature, issuer, audience, expiry |
| 5 | SP 세션·인가·감사 | role/attribute 매핑, access log |

> 요약: SSO 흐름은 IdP 인증 후 SP 검증으로 끝나지 않고, 서비스별 인가 정책과 로그 기록까지 이어져야 한다.

---

## Ⅳ. 특징

| 구분 | 기존/대안 | SSO | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 계정 관리 | 앱별 계정 | 중앙 IdP 계정·MFA | SCIM 2.0, 퇴사 차단 4시간 이하 |
| 인증 방식 | 앱별 로그인 | SAML/OIDC Federation | SAML 2.0, OIDC Core |
| 인가 방식 | 앱 내부 권한 | SP별 RBAC/ABAC 정책 | role mapping, attribute mapping |
| 운영 리스크 | 분산 장애 | IdP 단일 장애점 | IdP SLA 99.9%, DR RTO 1시간 |

> 요약: SSO는 계정과 인증을 중앙화하지만, IdP 장애와 세션 탈취가 전체 서비스 접근에 영향을 준다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | SSO | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 앱별 인증 | IdP 중심 Federation | 서비스 5개 이상, 사용자 1,000명 이상 |
| 비용/성능 | 계정 운영 분산 | IdP 운영·연동 비용 집중 | 계정 생성/삭제 요청 월 100건 이상 |
| 운영/위험 | 개별 장애 | IdP 장애 시 다수 SP 영향 | HA, DR, break-glass 계정 필요 |

> 요약: SSO는 서비스 수와 사용자 수가 늘수록 가치가 커지며, IdP 장애 대응 설계가 선택 조건이다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 단일 장애점 | IdP 장애 또는 DNS 장애 | Active-Active IdP, DR, break-glass 계정 | IdP 가용성 99.9%, RTO 1시간 |
| 세션 탈취 | 장기 쿠키, 공용 PC | 세션 1시간, idle timeout 15분, step-up MFA | 이상 로그인 탐지 건수 |
| 권한 과다 | SP role mapping 오류 | access review 분기 1회, SoD rule | 과다 권한 회수 건수 |

> 요약: SSO 운영은 장애 복구, 세션 수명, 권한 검토 지표를 동시에 관리해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 인증 연계 | SAML/OIDC 검증 실패율 0.1% 이하 | IdP/SP 로그 대조 |
| 계정 회수 | 퇴사자 deprovisioning 4시간 이하 | HRIS-SCIM 동기화 리포트 |
| 감사 추적 | 로그인·권한 변경 로그 1년 보관 | SIEM, 감사 샘플링 |

> 요약: SSO 도입 성과는 로그인 편의보다 계정 회수 시간, 검증 실패율, 감사 로그 완전성으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. IdP는 HA 2개 AZ 이상, DR RTO 1시간, 관리자 break-glass 계정 2개 이하로 운영함.
2. SP는 SAML/OIDC signature, issuer, audience, expiry를 검증하고 RBAC/ABAC 정책을 별도로 적용함.
3. SCIM 2.0으로 입사·전보·퇴사 동기화, 분기 1회 access review, SIEM 로그인 감사 1년 보관을 수행함.

**결론 (2줄):**
- 기술사 판단: SSO는 인증 중앙화에는 적합하나, 서비스 권한은 SP 정책으로 분리해야 과다 권한을 통제함.
- 향후 방향: 제로트러스트 기반 conditional access, device posture, risk-based MFA와 결합해 세션 중심에서 지속 검증으로 전환함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "SSO를 설명하시오" | IdP 인증, SP 검증, 세션 발급 흐름 | SAML/OIDC, 장점·리스크 비교 |
| 요구사항 명시형 | "SSO 구축 방안을 제시하시오", "운영 방안을 설명하시오" | 세션 수명, 장애 대응, 권한 정책 흐름 | IdP HA, SCIM, access review, 감사 지표 |

> 요약: 포괄형은 구조와 프로토콜, 운영형은 IdP 장애·세션·계정 회수 지표를 중심으로 작성한다.
