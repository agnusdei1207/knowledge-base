+++
title = "068. 암호학 (Cryptography) — 기밀성·무결성·인증·부인방지 제공"
date = "2026-04-05"
weight = 68
[extra]
categories = "studynote-security"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 암호학은 [[002_confidentiality|기밀성]], [[003_integrity|무결성]], [[303_authentication_authorization_patterns|인증]], 부인방지를 제공하는 수학 기반 보안 기술이다.
> 2. **가치**: 대칭키, 공개키, 해시, 서명 같은 요소를 조합해 다양한 보안 요구를 해결한다.
> 3. **판단**: 암호화와 해시, 서명의 역할을 구분해야 적절한 보안 설계를 할 수 있다.

---

## Ⅰ. 개요 및 필요성

네트워크와 저장소가 열려 있는 환경에서 [[001_dikw_pyramid|데이터]]를 안전하게 다루려면 암호학이 필요하다.

암호학은 단순한 암호화가 아니라, 여러 보안 [[082_attribute_types_er_model|속성]]을 구현하는 기반 기술이다.

- **📢 섹션 요약 비유**: 비밀 편지, 봉인 도장, 서명, 확인표를 모두 만드는 기술이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Plaintext
  ↓
Crypto Primitive
  ↓
Ciphertext / Signature / Digest
```

| 요소 | 역할 |
| :-- | :-- |
| [[653_symmetric_key_cryptography_fast_speed|Symmetric Key]] | 빠른 암호화 |
| Public [[067_db_key_uniqueness_minimality|Key]] | 키 교환/서명 |
| Hash | [[003_integrity|무결성]] |
| [[675_digital_signature_process_asymmetric_key|Digital Signature]] | [[303_authentication_authorization_patterns|인증]]/부인방지 |

암호학은 목적에 따라 도구가 다르다. [[002_confidentiality|기밀성]]이 필요하면 암호화, [[003_integrity|무결성]]이 필요하면 해시, [[303_authentication_authorization_patterns|인증]]이 필요하면 서명을 쓴다.

- **📢 섹션 요약 비유**: 자물쇠, 도장, 확인서가 각각 다른 일을 하는 것과 같다.

---

## Ⅲ. 비교 및 연결

| 기법 | 특징 | 용도 |
| :-- | :-- | :-- |
| Symmetric | 빠름 | 대용량 암호화 |
| Asymmetric | 키 분리 | 키 교환, 서명 |
| Hash | 역변환 불가 | [[003_integrity|무결성]], 비밀번호 |

| 보안 [[082_attribute_types_er_model|속성]] | 의미 |
| :-- | :-- |
| [[002_confidentiality|Confidentiality]] | [[002_confidentiality|기밀성]] |
| [[003_integrity|Integrity]] | [[003_integrity|무결성]] |
| [[604_authentication_factors|Authentication]] | [[303_authentication_authorization_patterns|인증]] |
| Non-repudiation | 부인방지 |

암호학은 단일 기능이 아니라 보안 [[082_attribute_types_er_model|속성]]의 조합이다.

- **📢 섹션 요약 비유**: 잠그고, 확인하고, 기록하는 도구를 함께 쓰는 셈이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. 목적에 맞는 암호 기법을 선택했는가?
2. 키 관리가 포함되어 있는가?
3. 해시와 암호화를 혼동하지 않는가?
4. 서명과 [[303_authentication_authorization_patterns|인증]]을 구분하는가?
5. [[001_algorithm_definition|알고리즘]]/키 길이/운영 정책이 적절한가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 만능 암호화 도구처럼 쓰는 설계
- 키 관리 없이 [[001_algorithm_definition|알고리즘]]만 보는 설계
- 해시를 암호화로 오해하는 설계
- 보안 [[082_attribute_types_er_model|속성]]을 한 가지로만 보는 설계

기술사 관점에서는 암호학을 "수학적 보안 도구 상자"로 보고, 목적별로 적절히 조합해야 한다.

- **📢 섹션 요약 비유**: 열쇠도, 도장도, 확인표도 상황에 맞게 써야 한다.

---

## Ⅴ. 기대효과 및 결론

암호학을 정확히 이해하면 보안 설계, [[303_authentication_authorization_patterns|인증]], [[001_dikw_pyramid|데이터]] 보호를 훨씬 체계적으로 설명할 수 있다.

결론적으로 암호학은 다양한 보안 [[082_attribute_types_er_model|속성]]을 제공하는 기반 기술이다.

- **📢 섹션 요약 비유**: 비밀을 지키는 여러 가지 도구를 다루는 학문이다.

---

## 관련 개념 맵

```text
Cryptography
  ↓
Symmetric / Asymmetric / Hash
  ↓
Security Properties
  ↓
Secure Design
```

---

## 관련 키워드 및 발전 흐름도

```text
Classic Cipher
  ↓
Modern Cryptography
  ↓
Public Key / Hash
  ↓
Security Protocols
```

---

## 어린이를 위한 3줄 비유 설명

비밀을 지키는 도구들이 있어요.  
자물쇠, 도장, 확인서가 각각 달라요.  
암호학은 그런 도구를 다루는 거예요.
