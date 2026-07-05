---
title: "패스키 비밀번호 없는 인증 (Passkey Passwordless)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 95
---

# 📖 【암기용】 개념 완전 이해

> 목적: 패스키 기반 비밀번호 없는 인증을 처음 봐도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 사용자가 비밀번호를 입력하지 않고 장치의 FIDO credential로 로그인하는 인증 방식
- **왜 필요한가**: 비밀번호는 재사용, 유출, 피싱, reset 공격의 중심이다. 패스키는 공개키 기반 credential을 장치나 클라우드 키체인에 저장해 공유 비밀 입력을 없앤다.
- **핵심 직관**: 사용자는 사이트마다 다른 디지털 열쇠를 갖고 있고, 로그인할 때 열쇠 자체가 아니라 서명 결과만 보여준다.

## 깊이 이해
- **배경·문제의식**: FIDO2는 피싱 저항성이 있으나 보안키 보급과 분실 복구가 장벽이었다. 패스키는 platform authenticator, discoverable credential, 동기화 키체인을 결합해 사용자에게 비밀번호 없는 로그인을 제공한다.
- **작동 원리**: 등록 시 사이트(RP)는 passkey credential을 만들고 공개키를 저장한다. 로그인 시 사용자는 계정 ID를 입력하지 않아도 discoverable credential을 선택할 수 있고, 단말 생체/PIN으로 user verification 후 challenge에 서명한다.
- **비유**: 비밀번호 수첩을 들고 다니는 대신, 휴대폰 지갑 안에 사이트별 열쇠를 넣어두고 문 앞에서 일회용 서명을 제출하는 구조이다.
- **구체 예시**: synced passkey는 휴대폰과 노트북의 계정 키체인에 동기화되고, device-bound passkey는 특정 보안키나 단말에만 존재한다. 금융·관리자 계정은 device-bound를 우선 검토한다.
- **흔한 오해·주의점**: 패스키가 복구 문제를 자동으로 해결하지 않는다. 계정 복구가 이메일 링크만으로 가능하면 공격자는 복구 절차로 패스키를 우회할 수 있다.

## 연결 개념
- FIDO2/WebAuthn - 패스키의 표준 기반
- Account Recovery - 패스키 분실과 동기화 실패 대응
- Risk-Based Authentication - 새 장치 등록과 복구 시 재인증

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 패스키 답안은 "비밀번호 없음"만 쓰지 않고 synced/device-bound, discoverable credential, user verification, account recovery를 연결해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 패스키는 FIDO2/WebAuthn 기반 공개키 credential을 사용해 비밀번호 입력 없이 challenge 서명으로 로그인하는 방식임
> 2. **가치**: 서버 비밀번호 DB와 피싱 입력값을 제거하고, RP별 credential과 origin binding으로 credential stuffing과 피싱 중계를 차단함
> 3. **판단 포인트**: synced passkey와 device-bound passkey 선택, discoverable credential UX, 계정 복구 우회 방지를 함께 설계해야 함

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Passwordless 구조 이해 확인 | public-key credential, discoverable credential, user verification | 단순 자동 로그인으로 설명 |
| 패스키 유형 판단 확인 | synced vs device-bound, platform vs roaming authenticator | 동기화 패스키를 모든 업무에 동일 적용 |
| 복구·운영 위험 확인 | account recovery, device loss, credential lifecycle log | 이메일 복구 우회와 등록 해제 로그 누락 |

> 요약: 이 문제는 비밀번호 제거 효과보다 credential 유형과 복구 통제를 설계하는 능력을 본다.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **패스키 비밀번호 없는 인증** | 패스키 비밀번호 없는 인증 (Passkey Passwordless)의 핵심 개념 | 이 주제의 본질 |

---

## Ⅰ. 개요 및 필요성

- 개요: 비밀번호 없는 공개키 인증
- 배경: 비밀번호는 피싱 입력, 유출 DB 대입, 서비스 간 재사용 공격에서 동일한 침해 경로가 된다.
- 필요성: 패스키는 FIDO2 동기화 credential과 장치 내 서명으로 로그인해 서버 저장 비밀값과 사용자 입력 비밀값을 제거한다.

---

## Ⅱ. 구조 및 구성요소

```text
User Device -> Platform Authenticator -> Passkey Credential -> WebAuthn RP
              / Synced Passkey
              / Device-Bound Passkey
              / User Verification
RP -> Public Key Store -> Session -> Recovery/Audit
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Passkey Credential | RP별 공개키 자격 증명 | discoverable credential 가능 |
| Platform Authenticator | 단말 내 서명과 사용자 확인 | 생체, PIN, secure enclave |
| Sync Provider | 기기 간 credential 동기화 | 계정 키체인, 종단 간 암호화 |
| Device-Bound Key | 특정 장치에 묶인 credential | 보안키, 고위험 계정 |
| Recovery/Audit | 분실·교체·등록 해제 통제 | 복구 코드, 2인 승인, SIEM 로그 |

> 요약: 패스키는 credential 저장 위치와 동기화 방식에 따라 적용 대상과 복구 통제 기준이 달라진다.

---

## Ⅲ. 동작원리 및 흐름도

```text
패스키 등록 -> 공개키 저장 -> 로그인 요청 -> discoverable credential 선택
-> 생체/PIN 확인 -> challenge 서명 -> RP 검증 -> 세션 발급
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Passkey 등록 | RP ID, origin, user verification required |
| 2 | Credential 저장 | synced 또는 device-bound 정책 |
| 3 | 로그인 challenge 수신 | nonce 128bit 이상, HTTPS |
| 4 | 사용자 확인 후 서명 | 생체/PIN, authenticator assertion |
| 5 | 세션·복구 로그 처리 | credential 등록/삭제, 새 장치 등록 경보 |

> 요약: 패스키 로그인은 계정 선택, 장치 내 사용자 확인, 공개키 서명 검증 순서로 동작한다.

---

## Ⅳ. 특징

| 구분 | 기존/대안 | 패스키 적용 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 비밀번호 | hash DB와 reset 절차 | passwordless, 공개키 저장 | credential stuffing 경로 제거 |
| 피싱 | 사용자가 secret 입력 | origin binding, RP ID | 피싱 도메인 서명 실패 |
| 유형 | 보안키 단독 | synced/device-bound 선택 | 소비자 synced, 관리자 device-bound |
| 복구 | 이메일 reset | recovery code, 보조 장치, step-up | 새 장치 등록 24시간 위험 표시 |

> 요약: 패스키는 비밀번호 입력을 없애지만, 동기화와 복구 절차가 새 신뢰 경계가 된다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 소비자 서비스 | password+SMS OTP | synced passkey | 가입 전환율, 분실 복구 빈도 |
| 관리자 계정 | TOTP MFA | device-bound passkey 또는 보안키 | 피싱 위험, 장치 통제 가능성 |
| 계정 복구 | 이메일 링크 | recovery code+기존 장치 step-up | helpdesk 사칭과 계정 탈취 방지 |

> 요약: 대규모 사용자 서비스는 synced passkey, 고위험 내부 계정은 device-bound passkey를 우선 검토한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 복구 우회 | 이메일 계정 탈취 | 기존 패스키 step-up, recovery code, 지연 처리 | 복구 후 24시간 민감 기능 제한 |
| 동기화 계정 탈취 | 클라우드 키체인 계정 침해 | sync provider MFA, 새 장치 경보 | 새 장치 등록 이벤트 |
| 계정 잠김 | 장치 분실, 동기화 실패 | 보조 패스키 2개 등록, 오프라인 복구 코드 | 계정 복구 요청률 |

> 요약: 패스키 운영 위험은 복구 우회, 동기화 계정 침해, 장치 분실이며 등록·복구 로그로 추적한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 등록률 | 대상 계정 passkey 등록률 80% 이상 | IdP/WebAuthn report |
| Passwordless 전환 | 비밀번호 로그인 비율 월 10%p 감소 | authentication method metric |
| 복구 통제 | 복구 이벤트 100% audit, 새 장치 24시간 위험 표시 | SIEM, IAM workflow |

> 요약: 패스키 성과는 등록률, 비밀번호 로그인 감소, 복구 이벤트 감사율로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 적용 범위: 소비자 웹·모바일은 synced passkey와 discoverable credential, 관리자·개발자 계정은 device-bound passkey 또는 FIDO2 보안키 적용
2. 검증 구현: WebAuthn에서 RP ID, origin, challenge 128bit 이상, user verification, credential ID, signCount를 검증하고 부정 테스트를 CI에 포함
3. 복구 운영: 보조 패스키 2개 등록, recovery code, 새 장치 등록 24시간 민감 기능 제한, 등록·삭제 이벤트 SIEM 전송

**결론 (2줄):**
- 기술사 판단: 패스키는 대규모 사용자 인증에는 synced 방식, 고위험 업무에는 device-bound 방식과 복구 지연 통제를 결합해야 함
- 향후 방향: 인증 체계는 비밀번호 reset 중심에서 passkey lifecycle, 장치 신뢰, 위험 기반 복구 통제로 이동함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "패스키를 설명하시오", "기술하시오" | 등록, credential 선택, challenge 서명 흐름 | synced/device-bound, discoverable credential |
| 요구사항 명시형 | "도입 방안을 제시하시오", "비교하시오", "설계하시오" | 계정군별 적용과 복구 절차 | 비밀번호 대비, FIDO2 대비, 복구 위험 기준 |

> 요약: 설명형은 WebAuthn 기반 동작을, 설계형은 패스키 유형과 계정 복구 통제를 중심으로 전개한다.
