+++
title = "071. 단일 치환 암호 — 하나의 알파벳을 하나의 문자로 치환"
date = 2026-04-05

[taxonomies]
tags = ["studynote-security"]

[extra]
tags = ["studynote-security"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 단일 치환 암호는 각 평문 문자를 다른 한 문자로 고정적으로 바꾸는 암호다.
> 2. **가치**: 카이사르 암호보다 일반적이지만 여전히 단순한 고전 암호다.
> 3. **판단**: 치환 규칙이 고정되어 있어 빈도 분석에 취약하다.

---

## Ⅰ. 개요 및 필요성

문자를 한 칸씩 미는 것보다 더 일반적인 방식으로 바꾸고 싶을 때 단일 치환을 쓴다.

하지만 원리는 여전히 단순하다.

- **📢 섹션 요약 비유**: 글자마다 다른 스티커를 붙이는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Plaintext
  v substitution map
Ciphertext
```

| 요소 | 의미 |
| :-- | :-- |
| [Mapping](/knowledge-base/studynote/05_database/01_db_architecture_relational/010_schema_mapping/) | 문자 대응표 |
| [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) | 치환 규칙 |
| [One-to-One](/knowledge-base/studynote/02_operating_system/02_process_thread/099_one_to_one_model/) | [일대일](/knowledge-base/studynote/02_operating_system/02_process_thread/099_one_to_one_model/) 대응 |

단일 치환은 문자 하나를 다른 문자 하나로 바꾸는 방식이므로, 문자 빈도 패턴이 남을 수 있다.

- **📢 섹션 요약 비유**: 같은 글자에 다른 이름표만 붙이는 셈이다.

---

## Ⅲ. 비교 및 연결

| 개념 | 의미 |
| :-- | :-- |
| Caesar | 고정 이동 |
| Monoalphabetic | 일반 치환 |
| Frequency Analysis | 취약점 |

| 약점 | 설명 |
| :-- | :-- |
| Pattern Leak | 패턴 노출 |
| Small [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) | 낮은 보안 |

단일 치환은 고전 암호 중 중요한 단계지만, 현대 보안에는 부족하다.

- **📢 섹션 요약 비유**: 모양은 바뀌어도 흔적은 남는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [일대일](/knowledge-base/studynote/02_operating_system/02_process_thread/099_one_to_one_model/) 치환임을 아는가?
2. 빈도 분석 취약성을 아는가?
3. 카이사르 암호와 비교할 수 있는가?
4. 현대 암호와 구분하는가?
5. 교육용 예제로 적절한가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 실무 보안에 쓰는 설계
- 빈도 분석을 무시하는 설계
- 키 공간이 충분하다고 착각하는 설계
- 고전 암호와 현대 암호를 혼동하는 설계

기술사 관점에서는 단일 치환 암호를 "빈도 분석에 취약한 고전 암호"로 설명해야 한다.

- **📢 섹션 요약 비유**: 글자 모양만 바꿔도 내용 패턴은 남는다.

---

## Ⅴ. 기대효과 및 결론

단일 치환 암호는 암호 기본 원리를 배우는 데 좋다.

결론적으로 단일 치환 암호는 하나의 문자를 하나의 다른 문자로 치환하는 방식이다.

- **📢 섹션 요약 비유**: 글자마다 다른 이름표를 붙이는 암호다.

---

## 관련 개념 맵

```text
Plaintext
  v
Monoalphabetic Cipher
  v
Substitution
  v
Ciphertext
```

---

## 관련 키워드 및 발전 흐름도

```text
Substitution Cipher
  v
Monoalphabetic Cipher
  v
Frequency Analysis
```

---

## 어린이를 위한 3줄 비유 설명

글자마다 다른 이름표를 붙여요.
그래도 흔적은 남아요.
단일 치환 암호는 그런 방식이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 71 / 1108

<- **이전**: [070. 카이사르 암호 (Caesar Cipher) — 알파벳 3자리 이동](/knowledge-base/studynote/09_security/02_crypto/070_caesar_cipher/)
**다음**: [072. 다중 치환 암호 (Vigenère Cipher) — 키워드 기반 복수 치환](/knowledge-base/studynote/09_security/02_crypto/072_vigenere_cipher/) ->

---
