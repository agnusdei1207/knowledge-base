---
title: "069. 고전 암호 — 치환 암호, 전치 암호"
date: "2026-04-05"
tags:
  - "studynote-security"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 고전 암호는 문자나 위치를 바꾸는 방식으로 정보를 숨기는 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 암호 체계다.
> 2. **가치**: 현대 암호학의 출발점으로, 치환과 전치의 기본 발상을 이해하게 해 준다.
> 3. **판단**: 단순해서 깨지기 쉽지만, 암호 설계의 역사와 원리를 배우는 데 유용하다.

---

## Ⅰ. 개요 및 필요성

오래된 암호는 수학보다 규칙 변화에 의존했다. 그래서 사람이 직접 만들고 해독하기 쉬웠다.

하지만 그만큼 공격에도 취약했다.

- **📢 섹션 요약 비유**: 글자를 다른 모양으로 바꾸거나 순서를 바꾸는 놀이 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Plaintext
  v
Substitution / Transposition
  v
Ciphertext
```

| 방식 | 의미 |
| :-- | :-- |
| Substitution | 문자 바꾸기 |
| Transposition | 위치 바꾸기 |

치환 암호는 글자 자체를 바꾸고, 전치 암호는 글자의 순서를 바꾼다. 둘 다 단순하지만 아이디어가 중요하다.

- **📢 섹션 요약 비유**: 같은 블록을 다른 색으로 바꾸거나, 순서만 다시 배열하는 것이다.

---

## Ⅲ. 비교 및 연결

| 구분 | 치환 암호 | 전치 암호 |
| :-- | :-- | :-- |
| 방식 | 문자 대체 | 순서 변경 |
| 난이도 | 단순 | 단순 |
| 약점 | 빈도 분석 | 패턴 분석 |

| 역사 | 의미 |
| :-- | :-- |
| Caesar | 대표 치환 |
| Rail Fence | 대표 전치 |

고전 암호는 현대 암호와 달리 키 관리와 수학적 안전성 측면에서 매우 약하다.

- **📢 섹션 요약 비유**: 퍼즐을 다시 맞추기 쉽도록 일부만 바꾸는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 치환과 전치를 구분하는가?
2. 빈도 분석 약점을 아는가?
3. 현대 암호와 차이를 설명할 수 있는가?
4. 역사적 의미를 이해하는가?
5. 교육용 예제로 적절한가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 고전 암호를 실무 보안으로 쓰는 설계
- 치환과 전치를 혼동하는 설계
- 빈도 분석 취약성을 무시하는 설계
- 현대 암호와 같은 수준으로 보는 설계

기술사 관점에서는 고전 암호를 "현대 암호의 전사"로 설명해야 한다.

- **📢 섹션 요약 비유**: 옛날 방식이라도 암호의 기본 생각은 담고 있다.

---

## Ⅴ. 기대효과 및 결론

고전 암호를 이해하면 현대 암호학의 필요성과 발전을 더 잘 이해할 수 있다.

결론적으로 고전 암호는 치환과 전치를 중심으로 한 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 암호 방식이다.

- **📢 섹션 요약 비유**: 옛날 자물쇠를 알아야 새 자물쇠가 왜 나왔는지 안다.

---

## 관련 개념 맵

```text
Plaintext
  v
Classical Cipher
  v
Substitution / Transposition
  v
Modern Cryptography
```

---

## 관련 키워드 및 발전 흐름도

```text
Classical Cipher
  v
Frequency Analysis
  v
Modern Cipher
  v
Cryptography
```

---

## 어린이를 위한 3줄 비유 설명

글자를 바꾸거나 순서를 바꿔요.
옛날 암호는 그런 방식이었어요.
고전 암호는 오래된 비밀놀이예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 69 / 1108

<- **이전**: [068. 암호학 (Cryptography) — 기밀성·무결성·인증·부인방지 제공](/studynote/09_security/02_crypto/068_cryptography/)
**다음**: [070. 카이사르 암호 (Caesar Cipher) — 알파벳 3자리 이동](/studynote/09_security/02_crypto/070_caesar_cipher/) ->

---
