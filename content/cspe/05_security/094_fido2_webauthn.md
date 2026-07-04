---
title: "FIDO2·WebAuthn (FIDO2 WebAuthn)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 94
---

# 📖 【암기용】 개념 완전 이해

> 목적: FIDO2와 WebAuthn을 처음 봐도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 비밀번호 대신 공개키 credential과 origin binding으로 사용자를 인증하는 표준
- **왜 필요한가**: 비밀번호와 OTP는 피싱 사이트가 입력값을 받아 중계할 수 있다. FIDO2는 사이트별 공개키를 만들고 실제 origin에서 온 challenge에만 서명하게 해 피싱 성공 조건을 어렵게 만든다.
- **핵심 직관**: 사용자는 비밀번호를 서버에 보내지 않고, 자기 장치 안의 개인키로 "이 사이트가 보낸 일회용 문제"에 서명한다.

## 깊이 이해
- **배경·문제의식**: 계정 탈취의 핵심은 공유 비밀(secret)을 입력하게 만드는 것이다. FIDO2/WebAuthn은 서버가 비밀번호를 저장하지 않고, 사용자 장치의 authenticator가 RP ID와 origin에 묶인 키쌍을 생성해 서명 검증만 수행한다.
- **작동 원리**: 등록 시 RP는 challenge를 보내고 authenticator는 RP ID별 공개키 credential을 생성한다. 로그인 시 RP가 새 challenge를 보내면 authenticator가 user presence 또는 user verification 후 개인키로 서명하고, 서버는 공개키·counter·origin을 검증한다.
- **비유**: 도장을 서버에 맡기는 것이 아니라, 매번 새 문서에 본인 도장으로 찍은 서명만 제출하는 방식이다. 도장은 장치 밖으로 나오지 않는다.
- **구체 예시**: `login.example.com`의 credential은 `evil.example.net`에서 재사용되지 않는다. RP ID hash와 origin이 맞지 않으면 authenticator가 유효한 assertion을 만들지 않는다.
- **흔한 오해·주의점**: FIDO2는 "생체 인증" 그 자체가 아니다. 생체는 장치 잠금 해제나 user verification 수단이고, 서버가 검증하는 핵심은 공개키 서명이다.

## 연결 개념
- Passkey - FIDO credential의 사용자 친화적 구현
- MFA - 피싱 저항 소유 요소
- WebAuthn - 브라우저와 RP 간 공개키 인증 API

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: FIDO2 답안은 생체 인증 설명이 아니라 public-key credential, authenticator, RP ID, challenge, origin binding을 연결해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: FIDO2/WebAuthn은 RP별 공개키 credential과 authenticator 서명으로 사용자를 검증하는 비밀번호 없는 인증 표준임
> 2. **가치**: 비밀번호·OTP 공유 비밀을 서버로 보내지 않고, origin-bound challenge 서명으로 피싱 중계와 credential stuffing을 차단함
> 3. **판단 포인트**: RP ID, origin, challenge, user verification, attestation/assertion, counter 검증을 누락하면 공개키 인증 원리 설명이 결여됨

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 공개키 인증 구조 이해 확인 | credential key pair, authenticator, RP, browser | 생체 인증으로만 설명 |
| 피싱 저항성 원리 확인 | origin binding, RP ID hash, challenge 서명 | OTP보다 편한 로그인으로만 서술 |
| 도입·운영 판단 확인 | attestation, user verification, recovery, device loss | 복구 절차와 등록 해제 로그 누락 |

> 요약: 이 문제는 FIDO2의 핵심인 사이트별 공개키와 origin-bound 서명 검증을 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: 공개키 기반 사용자 인증
- 배경: 비밀번호와 OTP는 피싱 프록시가 입력값을 실시간 중계하면 사용자가 정상 사이트와 공격 사이트를 구분하기 어렵다.
- 필요성: FIDO2/WebAuthn은 RP ID에 묶인 credential과 challenge 서명 검증으로 공유 비밀 전송을 제거한다.

---

## Ⅱ. 구조 및 구성요소

```text
User -> Browser/WebAuthn -> Authenticator -> Public-Key Credential
RP Server -> Challenge -> Assertion Verification -> Session
           / RP ID
           / Origin
           / Credential Store
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| RP Server | challenge 발급, 공개키 저장, assertion 검증 | RP ID, origin allowlist |
| Browser/WebAuthn | RP와 authenticator 연결 | WebAuthn API, HTTPS 필수 |
| Authenticator | 개인키 보관, user presence/verification 수행 | platform, roaming, security key |
| Credential | RP별 공개키 자격 증명 | discoverable 또는 server-side credential |
| Attestation/Assertion | 등록 증명과 로그인 서명 | attestation 정책, signCount |

> 요약: FIDO2는 RP, 브라우저, authenticator, credential이 공개키 challenge-response를 수행하는 구조이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
등록 요청 -> RP challenge 발급 -> authenticator key pair 생성
-> public key 저장 -> 로그인 challenge -> 개인키 서명 -> RP 검증 -> 세션 발급
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Registration challenge 생성 | nonce 128bit 이상, HTTPS origin |
| 2 | Authenticator가 credential 생성 | RP ID hash, user presence, user verification |
| 3 | 서버가 공개키와 credential ID 저장 | attestation policy, AAGUID 허용 |
| 4 | Authentication challenge 서명 | challenge, origin, RP ID, signCount |
| 5 | 세션 발급·로그 저장 | 실패 사유, 등록/해제 audit log |

> 요약: 등록은 공개키 저장, 로그인은 challenge 서명 검증이며 개인키는 authenticator 밖으로 나오지 않는다.

---

## Ⅳ. 특징

| 구분 | 기존/대안 | FIDO2/WebAuthn | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 비밀 관리 | password hash 저장 | 공개키 저장, 개인키 단말 보관 | 서버 비밀번호 DB 제거 |
| 피싱 대응 | OTP 코드 입력 | origin binding, RP ID hash | 피싱 도메인 assertion 실패 |
| 사용자 확인 | password 재입력 | UV PIN, 지문, 얼굴 | user verification required |
| 운영 | 비밀번호 초기화 | credential 등록·해제·복구 | 보안키 2개 이상 등록 |

> 요약: FIDO2의 차별점은 공개키 credential과 origin binding이며, 생체는 서버 인증 값이 아니라 장치 내 사용자 확인 수단이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 인증 강도 | password+TOTP | FIDO2 security key | 관리자, 개발자, 금융 업무 |
| 사용자 경험 | 매번 OTP 입력 | platform authenticator | 소비자 서비스, 모바일 앱 |
| 운영 통제 | 수동 reset | recovery code, 보조 키 등록 | 분실·교체 빈도와 helpdesk 부담 |

> 요약: 보안키는 고위험 계정, platform authenticator는 대규모 사용자 서비스에 우선 적용한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 계정 잠김 | authenticator 분실 | 보조 credential 2개 등록, recovery code | 복구 요청 건수 |
| 등록 우회 | 약한 본인확인 후 credential 추가 | 기존 MFA step-up, 이메일 단독 등록 금지 | credential 등록 실패/성공 로그 |
| 장치 신뢰 오판 | attestation 미검증 | 허용 AAGUID, enterprise attestation | 미승인 authenticator 비율 |

> 요약: FIDO2 도입 리스크는 분실 복구와 등록 우회이며, credential lifecycle 로그가 핵심 지표이다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 등록률 | 관리자 FIDO2 95% 이상, 보조 키 2개 등록 | IdP/WebAuthn report |
| 피싱 저항성 | passwordless 또는 FIDO2 MFA 적용 계정 비율 | auth method inventory |
| 검증 품질 | origin/RP ID/challenge negative test 100% 실패 | WebAuthn test suite, CI |

> 요약: FIDO2 운영 품질은 등록률, 보조 키 등록, origin/RP ID 부정 테스트 통과로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 등록 정책: 관리자와 개발자는 FIDO2 보안키 2개 이상 등록, credential 추가 시 기존 MFA step-up과 등록 audit log 저장
2. 검증 구현: WebAuthn 서버에서 challenge 128bit 이상, RP ID, origin, user verification, signCount, credential ID를 모두 검증
3. 복구 운영: recovery code, 보조 키, helpdesk 2인 승인 절차를 분리하고 credential 삭제·등록 이벤트를 SIEM에 전송

**결론 (2줄):**
- 기술사 판단: 피싱 위험이 큰 관리자·개발자·금융 계정은 TOTP보다 FIDO2/WebAuthn을 우선 적용해야 함
- 향후 방향: FIDO2는 passkey와 결합해 passwordless 인증의 기본 기반으로 확산됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "FIDO2/WebAuthn을 설명하시오", "기술하시오" | 등록과 인증 challenge-response 흐름 | 공개키 credential, origin binding, authenticator |
| 요구사항 명시형 | "도입 방안을 제시하시오", "비교하시오", "설계하시오" | RP ID/origin 검증과 복구 절차 | TOTP 대비 피싱 저항성, 보안키 등록 기준 |

> 요약: 설명형은 공개키 인증 원리, 설계형은 등록·검증·복구 운영을 중심으로 목차를 전환한다.
