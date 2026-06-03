---
title: 62. 시큐어 코딩 (Secure Coding)
date: '2026-04-05'
tags:
- studynote-security
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[190_secure_coding_guideline|시큐어 코딩]]([[190_secure_coding_guideline|Secure Coding]])은 입력을 검증하고 출력과 오류를 안전하게 처리해 취약점을 원천 차단하는 코딩 원칙이다.
> 2. **가치**: SQL [[480_injection|인젝션]], [[726_xss_cross_site_scripting_types|XSS]], 경로 조작, [[591_buffer_overflow|버퍼 오버플로우]] 같은 대표 취약점을 코드 단계에서 줄인다.
> 3. **융합**: [[416_owasp_top_10|OWASP Top 10]], [[491_sast_static_analysis|SAST]] (Static Application [[283_security_tactics|Security]] Testing), DevSecOps와 결합해 개발 파이프라인에 보안을 녹인다.

---

## Ⅰ. 개요 및 필요성

대부분의 해킹은 복잡한 초고급 기술보다 "입력 검증이 없었다"는 단순한 실수에서 시작된다. 즉, 코드를 잘못 쓰면 방화벽이 있어도 뚫린다.

[[190_secure_coding_guideline|시큐어 코딩]]은 처음부터 안전한 코드를 작성해 애플리케이션의 공격면을 줄이는 방법이다. 사후 대응보다 훨씬 근본적이다.

- **📢 섹션 요약 비유**: 문을 열어 둔 집보다, 애초에 문을 튼튼하게 만드는 것이 더 중요하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
입력 -> 검증 -> 처리 -> 출력 인코딩 -> 로그
```

| 원칙 | 의미 |
| :-- | :-- |
| [[601_input_validation|Input Validation]] | 들어오는 값을 반드시 [[396_validation|확인]] |
| Output Encoding | 화면 출력 시 악성 문자 무력화 |
| [[093_safe_scaled_agile_framework_art_pi|Safe]] Error Handling | 내부 정보 노출 금지 |
| Prepared Statement | SQL 구조와 값 분리 |
| [[010_least_privilege|Least Privilege]] | 최소 권한으로 실행 |

[[190_secure_coding_guideline|시큐어 코딩]]은 외부 입력을 신뢰하지 않는 것에서 시작한다. 사용자가 넣는 값, [[501_file_definition_logical_record|파일]], 네트워크 데이터는 모두 잠재적 공격 벡터로 봐야 한다.

- **📢 섹션 요약 비유**: 처음 들어오는 손님은 모두 검문소를 거쳐야 하는 공항 보안이다.

---

## Ⅲ. 비교 및 연결

| 방식 | 특징 | 한계 |
| :-- | :-- | :-- |
| [[059_bolt_on_security|Bolt-on Security]] | 나중에 [[696_waf_web_application_firewall|WAF]], 필터를 붙임 | 근본 취약점이 남음 |
| [[190_secure_coding_guideline|Secure Coding]] | 코드 단계에서 차단 | 개발 규율이 필요 |
| [[061_secure_by_default|Secure by Default]] | 기본 설정이 안전 | 제품 전체 설계 필요 |
| [[058_security_by_design|Security by Design]] | 전반적인 설계 철학 | 범위가 넓음 |

[[190_secure_coding_guideline|시큐어 코딩]]은 Secure by Default와 충돌하지 않는다. 오히려 기본값과 코드가 함께 안전해야 실제 보안이 완성된다.

- **📢 섹션 요약 비유**: 문만 잠그는 것과, 열쇠 복사까지 막는 것이 함께 있어야 진짜 안전하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. 입력 검증과 출력 인코딩을 모두 적용했는가?
2. SQL은 Prepared Statement를 사용하는가?
3. 에러 메시지에 내부 정보가 노출되지 않는가?
4. 비밀키와 인증정보가 코드에 하드코딩되지 않았는가?
5. [[491_sast_static_analysis|SAST]]/DAST로 자동 점검하는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 문자열 연결로 SQL을 만드는 설계
- HTML/JS 출력 인코딩을 생략하는 설계
- [[057_stack|스택]] 트레이스를 사용자 화면에 노출하는 설계
- 비밀키를 소스코드에 직접 넣는 설계

기술사 관점에서는 "잘 돌아가는 코드"보다 "안전하게 돌아가는 코드"를 우선 봐야 한다. 보안은 추가 기능이 아니라 기본 품질이다.

- **📢 섹션 요약 비유**: 독을 걸러 내지 않는 주방은 아무리 빨라도 위험하다.

---

## Ⅴ. 기대효과 및 결론

[[190_secure_coding_guideline|시큐어 코딩]]은 취약점 발생 가능성을 낮추고, 나중에 붙이는 보안 장치의 부담도 줄인다. 그래서 가장 근본적인 보안 투자다.

결국 좋은 보안은 방화벽보다 먼저 코드에서 시작된다.

- **📢 섹션 요약 비유**: 처음부터 튼튼한 재료로 요리해야 식중독을 막을 수 있다.

---

## 관련 개념 맵

```text
Input Validation
   ↓
Secure Coding
   ↓
OWASP Top 10
   ↓
SAST / DevSecOps
   ↓
Secure SDLC
```

---

## 관련 키워드 및 발전 흐름도

```text
취약한 코드
   ↓
시큐어 코딩
   ↓
자동 보안 점검
   ↓
DevSecOps
```

---

## 어린이를 위한 3줄 비유 설명

먹기 전에 음식이 안전한지 먼저 보는 거예요.  
문자도 화면에 바로 보여 주지 말고 한 번 걸러야 해요.  
그래야 나쁜 코드가 사고를 만들지 않아요.
