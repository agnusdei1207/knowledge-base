---
title: "Verifiable Credential 검증가능 자격증명 (Verifiable Credential)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 351
---

# 📖 【암기용】 개념 완전 이해

> 목적: VC를 발급자 주장을 암호학적으로 검증 가능한 디지털 자격증명으로 이해하게 만든다.

## 한눈에
- **개요**: W3C VC Data Model 기반의 서명된 디지털 자격증명
- **왜 필요한가**: 학력, 면허, 재직, 출입권한 같은 자격을 매번 원기관 API로 조회하면 개인정보 노출과 기관 간 연계 비용이 커진다.
- **핵심 직관**: 종이 증명서에 기관 직인이 있듯, VC는 발급자의 디지털 서명으로 위변조 여부와 발급자를 검증한다.

## 깊이 이해
- **배경·문제의식**: 기존 증명서는 스캔본 위변조, API 의존, 과다 정보 제출 문제가 있다. VC는 issuer, holder, verifier 3자 모델로 자격증명을 지갑에 보관하고 필요한 때 제출한다.
- **작동 원리**: issuer가 subject claims를 포함한 credential을 서명해 holder에게 발급하고, holder는 presentation으로 묶어 verifier에게 제출한다.
- **비유**: 학교가 졸업증명서에 직인을 찍어 학생에게 주고, 회사는 학교에 매번 전화하지 않고 직인과 폐기 여부를 확인하는 구조다.
- **구체 예시**: 모바일 신분증은 이름, 생년월일, 발급기관, 만료일, cryptographic proof를 포함하고 검증자는 발급자 공개키와 상태 목록으로 유효성을 확인한다.
- **흔한 오해·주의점**: VC는 모든 정보를 공개하라는 형식이 아니다. selective disclosure와 presentation 정책으로 필요한 속성만 제출하도록 설계해야 한다.

## 연결 개념
- DID — issuer와 holder 식별 및 공개키 조회
- Verifiable Presentation — holder가 검증자에게 제출하는 증명 묶음
- Selective Disclosure — 필요한 속성만 공개하는 프라이버시 기법

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: VC는 issuer-holder-verifier 3자 모델과 W3C VC Data Model로 자격증명을 발급·보관·제출·검증하는 구조다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: VC는 발급자가 주체에 대한 claims를 서명해 holder가 보관하고 verifier가 검증하는 디지털 자격증명이다.
> 2. **가치**: 기관 API 실시간 조회 없이도 위변조 확인, 발급자 확인, 선택적 제출을 가능하게 한다.
> 3. **판단 포인트**: issuer 신뢰, credential status, revocation, selective disclosure, 지갑 보안이 핵심이다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| VC 구조 이해 확인 | issuer, holder, verifier, presentation | 단순 PDF 증명서로 설명 |
| DID와 관계 확인 | DID는 식별·검증키, VC는 claims | DID와 VC를 같은 개념으로 처리 |
| 개인정보 통제 확인 | 선택적 공개, 폐기·상태 확인 | 모든 속성 제출로 설계 |

> 요약: 이 문제는 발급·보관·제출·검증의 3자 모델과 프라이버시 통제를 함께 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: 서명된 디지털 자격증명
- 배경: 종이·PDF 증명서는 위변조 검증, 기관 간 조회, 개인정보 최소 제출에 한계가 있음.
- 필요성: W3C VC Data Model로 자격증명 발급자, 보유자, 검증자 간 상호운용과 위변조 검증을 구현해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Issuer -> Verifiable Credential -> Holder Wallet
Holder -> Verifiable Presentation -> Verifier
Verifier -> DID/Trust Registry/Credential Status -> Verification Result
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Issuer | claims를 서명해 VC 발급 | 기관 신뢰 정책 |
| Holder | VC를 지갑에 보관하고 제출 | key custody |
| Verifier | VP와 issuer 서명을 검증 | policy decision |
| Credential Status | 폐기·정지 상태 확인 | status list |

> 요약: VC는 발급자 신뢰, 보유자 제어, 검증자 정책, 상태 확인이 결합된 자격증명 모델이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
자격 확인 -> VC 발급/서명 -> 지갑 저장
-> VP 생성 -> 발급자 서명·상태 검증 -> 서비스 접근 판단
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | issuer가 subject claims와 만료일을 구성함 | schema match |
| 2 | issuer가 VC에 proof를 생성해 holder에게 발급함 | signature valid |
| 3 | holder가 필요한 속성으로 VP를 생성함 | presentation policy |
| 4 | verifier가 서명, 상태, 만료, 신뢰목록을 확인함 | verification result |

> 요약: VC 검증은 서명 확인만이 아니라 발급자 신뢰와 폐기 상태까지 포함한다.

---

## Ⅳ. 특징

| 구분 | 기존 증명서/API | VC | 판단 기준 |
|:---|:---|:---|:---|
| 보관 | 기관 DB·PDF | holder wallet | 사용자 제어 |
| 검증 | 원기관 조회 | cryptographic proof | 오프라인 검증 가능성 |
| 개인정보 | 전체 문서 제출 | selective disclosure | 최소 제출 |
| 상태관리 | 기관 API 의존 | status list/revocation | 최신 상태 요구 |

> 요약: VC는 자격증명을 사용자 지갑으로 이동시키지만 issuer 신뢰와 폐기 상태 확인 체계가 필요하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 신원 확인 | OIDC profile | VC 제출 | 자격증명 휴대성 |
| 검증 방식 | API callback | 서명·상태 검증 | 원기관 부하 |
| 개인정보 | 전체 속성 제공 | 속성 최소 공개 | 규제 요구 |

> 요약: VC는 자격증명 재사용과 최소 공개가 필요한 업무에서 API 조회를 대체하거나 보완한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 폐기 미반영 | status 조회 누락 | status list, short expiry | revoked VC accept rate |
| issuer 위조 | 신뢰목록 부재 | trust registry, DID verification | unknown issuer block |
| 지갑 탈취 | 개인키 유출 | hardware-backed key, recovery | wallet compromise |

> 요약: VC 리스크는 발급자 신뢰, 폐기 상태, 지갑 키 보호에서 발생한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 표준 준수 | W3C VC Data Model 표현 | conformance test |
| 검증 성공 | 유효 VC 검증 오류율 관리 | verifier log |
| 프라이버시 | 최소 속성 제출 정책 준수 | presentation audit |

> 요약: VC 도입 성과는 발급 건수가 아니라 검증 성공률, 폐기 반영, 최소 공개 준수로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 발급기관, schema, claims, 만료일, credential status 방식을 정의하고 issuer trust registry를 구축함.
2. holder 지갑에서 selective disclosure와 VP 생성을 지원하고 원문 개인정보를 검증자 서버에 저장하지 않음.
3. verifier는 issuer 서명, DID resolution, status, 만료, 업무 정책을 순서대로 검증하는 정책 엔진을 구성함.

**결론 (2줄):**
- 기술사 판단: 기관 간 자격증명 재사용과 개인정보 최소 제출이 요구되면 VC를 적용하고, 단일 기관 내부 조회는 기존 IAM이 단순함.
- 향후 방향: VC는 DID, mobile wallet, ZKP 기반 선택적 공개와 결합해 디지털 신원 인프라로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "VC를 설명하시오" | 발급·보관·제출·검증 흐름 | 기존 증명서와 차이 |
| 요구사항 명시형 | "디지털 자격증명 구축 방안을 제시하시오" | issuer 신뢰와 폐기 검증 | 최소 공개·지갑 보안 |

> 요약: 설명형은 3자 모델을, 구축형은 trust registry와 status 검증을 중심으로 작성한다.
