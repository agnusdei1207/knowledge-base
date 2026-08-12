---
sidebar:
  order: 48
  label: "048. CSRF (Cross-Site Request Forgery)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "CSRF (Cross-Site Request Forgery)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-security"
weight: 48
extra:
  question_no: "048"
  source_status: "기출"
  source_history: "131회"
  priority: 50
  priority_note: "131회 기출이며 세션•브라우저 보안 비교에 유용함"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **교차 사이트 요청 위조(Cross-Site Request Forgery, CSRF)**: 사용자가 자신의 의지와 무관하게 공격자가 의도한 비승인 수신처로 비밀번호 변경, 자금이체 등 상태 변경(State-changing) 요청을 전송하도록 유도하는 취약점.

</details>

- 정의/개념: 브라우저가 대상 사이트로 HTTP 요청을 보낼 때 쿠키 기반 세션 인증정보를 자동 첨부하는 메커니즘을 악용하여, 인가된 사용자의 권한으로 비승인 행위를 집행하게 만드는 공격.
- 배경/필요성: 단순 쿠키/세션 인증만으로는 요청이 사용자의 실제 의도(Intent)에 의해 발생한 것인지 검증할 수 없는 한계 극복.

#### 한줄 요약

- 브라우저의 자동 쿠키 첨부를 악용한 위조 요청을 막기 위해 서버 측에서 난수 기반 Anti-CSRF 토큰 및 출처를 검증함.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **세션 쿠키(Session Cookie)**: 브라우저가 특정 도메인에 대한 요청 전송 시 매번 자동 첨부하는 인증 식별자.
- **CSRF 토큰(Anti-CSRF Token)**: 세션별로 난수 생성되어 상태 변경 요청 폼/헤더에 포함되는 일회성/추측 불가능한 검증 키.
- **SameSite 쿠키(SameSite Cookie Attribute)**: Cross-Site 요청 시 세션 쿠키의 자동 전송 범위를 Strict/Lax/None으로 제어하는 속성.

</details>

- 브라우저의 **세션 쿠키(Session Cookie)** 자동 첨부 특성을 이용한 사용자 권한 대리 악용.
- 상태 변경 HTTP 메서드(POST, PUT, DELETE)에 대한 동적 **CSRF 토큰(Anti-CSRF Token)** 및 Origin/Referer 검증.
- **SameSite** 쿠키 속성을 적용하여 서드파티 컨텍스트의 자동 쿠키 전송 차단.

#### 한줄 요약

- Anti-CSRF 토큰, Origin/Referer 출처 검증 및 SameSite 쿠키 속성을 연계하여 위조된 교차 요청을 차단함.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **Origin**: HTTP 요청 헤더에 포함되는 요청 발신 출처(Scheme, Host, Port) 정보.
- **Referer**: 요청이 유발된 직전 URL 주소를 포함하는 HTTP 헤더.
- **안전 메서드(Safe Methods)**: GET, HEAD, OPTIONS 등 서버 데이터 상태 변경을 유발하지 않아야 하는 HTTP 조회용 메서드.

</details>

```text
CSRF 검증 구조
├─ 세션 쿠키: 자동 첨부 인증 상태
├─ 상태 변경 경로: 자금•계정 변경 처리
├─ CSRF 토큰: 요청 의도 검증값
├─ 출처 정책: Origin•Referer 검증
└─ 쿠키 정책: SameSite•안전 메서드 적용
```

| 구성요소 | 책임 |
|:---|:---|
| 세션 쿠키 | 자동 첨부되는 **세션 쿠키** 기반 사용자 인증 유지 |
| 상태 변경 경로 | 계정 정보 변경, 비밀번호 수정, 이체 등 POST/PUT 경로 통제 |
| CSRF 토큰 | 폼 또는 custom HTTP 헤더 상의 **CSRF 토큰** 검증 |
| 출처 정책 | **Origin** 및 **Referer** 헤더 기반 교차 사이트 발신 검증 |
| 쿠키 정책 | **SameSite=Lax/Strict** 속성 및 **안전 메서드(GET)**의 무상태성 준수 |

#### 한줄 요약

- 토큰 검증과 출처 헤더 확인을 통해 외부 악성 사이트에서 발송된 권한 대리 요청을 수신 거부함.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **의도 검증(User Intent Verification)**: 요청에 포함된 Anti-CSRF 토큰의 세션 일치성 및 출처 헤더의 정당성을 확인하는 절차.
- **위조 상태 변경 요청 생성**: 타깃 사이트의 POST 폼을 태그나 JS로 자동 전송하게 구성하는 단계.
- **세션 쿠키 자동 첨부**: 브라우저가 타깃 사이트의 인증 쿠키를 무단 요청에 결합하는 단계.
- **세션 인증 통과**: 백엔드 서버가 쿠키 유효성만 보고 사용자를 인가하는 단계.
- **사용자 의도 검증 누락**: Anti-CSRF 토큰이 없어 검증을 건너뛰는 단계.
- **비승인 상태 변경 실행**: 공격자가 의도한 비밀번호 변경, 이체 등이 실제 집행되는 단계.

</details>

```text
위조 폼•링크
      │
      ▼
1. 위조 상태 변경 요청 생성
      │
      ▼
2. 세션 쿠키 자동 첨부
      │
      ▼
3. 세션 인증 통과
      │
      ▼
4. 사용자 의도 검증 누락
      │
      ▼
5. 비승인 상태 변경 실행
      │
      ▼
처리 결과
```

### 동작 원리

1. **위조 상태 변경 요청 생성**: <iframe> 또는 <img> 태그를 통해 타깃 POST/GET 요청 구성.
2. **세션 쿠키 자동 첨부**: 피해자가 로그인 상태인 타깃 도메인 쿠키 자동 전송.
3. **세션 인증 통과**: 서버가 쿠키만 확인하고 인가 처리 집행.
4. **사용자 의도 검증 누락**: Anti-CSRF 토큰 검증이 없거나 검사 예외 로직 존재.
5. **비승인 상태 변경 실행**: 피해자의 계정 권한으로 이체 및 정보 변경 완전 수행.

#### 한줄 요약

- 자동 세션 인증을 우회하려는 위조 요청을 Anti-CSRF 토큰 및 사용자 의도 재검증으로 억제함.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **CSRF 방어 선택 기준(CSRF Mitigation Criteria)**: 요청 의도는 Anti-CSRF 토큰, 자동 쿠키 제한은 SameSite, 발신 위치는 Origin 헤더로 상호 보완 적용하는 원칙.

</details>

| CSRF 방어 유형 | CSRF 토큰 | SameSite 쿠키 | 출처 검증 |
|:---|:---|:---|:---|
| 적용 기준 | 의도 직접 검증 | 쿠키 전송 제한 | 요청 출처 판정 |
| 핵심 특징 | **CSRF 토큰**으로 의도 확인 | **SameSite**로 교차 쿠키 전송 제한 | **Origin**•**Referer** 확인 |
| 한계 | 토큰 노출•검증 누락 | 구형 브라우저 미지원 | 헤더 부재•중계 처리 오류 |

#### 한줄 요약

- 요청 의도를 직접 확인하는 CSRF 토큰과, 브라우저 차원에서 쿠키를 제한하는 SameSite/출처 검증을 조합함.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **MITRE CWE-352**: 교차 사이트 요청 위조(Cross-Site Request Forgery) 취약점 명세.
- **IETF RFC 9110**: HTTP 신구 규격을 정리하여 GET/HEAD 메서드의 무상태 조회를 명시한 표준.
- **교차 사이트 스크립팅(XSS)**: XSS 발생 시 저장된 Anti-CSRF 토큰이 탈취되므로 XSS 선제 차단이 필수적.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 세션 쿠키만 검증 시 위조 성립 | **MITRE CWE-352** 기준 Anti-CSRF 토큰 검증 | 비승인 상태 변경 완전 차단 |
| GET 메서드로 상태 변경 유발 | **IETF RFC 9110** 준수하여 GET은 조회 전용화 | 단순 이미지 링크를 통한 공격 차단 |
| XSS에 의한 토큰 탈취 | **XSS** 선제 제거 및 중요한 업무 시 비밀번호 **재인증** | 토큰 유출 시에도 최종 변경 집행 방지 |

#### 한줄 요약

- 비밀번호 변경 및 송금 시 예측 불가능한 Anti-CSRF 토큰을 검증하고, 고위험 작업에는 재인증(Re-authentication)을 집행함.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **재인증(Re-authentication)**: 비밀번호 변경, 자금이체 등 고위험 작업 실행 직전 사용자의 비밀번호나 MFA를 재요청하여 본인 의사를 확정하는 방어책.

</details>

- **CSRF 다층 통제 기준**에 따라 상태 변경 연산은 **CSRF 토큰** 및 Origin 검증, 고위험 업무는 **재인증**을 추가 적용.

#### 한줄 요약

- CSRF 방어를 위한 Anti-CSRF 토큰 및 SameSite 쿠키•출처 검증 심층 방어 체계 구축 필수.

