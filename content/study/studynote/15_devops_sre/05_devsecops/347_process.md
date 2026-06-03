---
title: 347. 프롬프트 인젝션 방어·탈옥 보호 (Prompt Injection Defense)
date: '2026-05-09'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[955_prompt_injection|프롬프트 인젝션]]([[955_prompt_injection|Prompt Injection]])은 사용자가 모델의 원래 지시와 [[164_policy|정책]]을 우회하도록 입력을 조작하는 공격이며, 탈옥(Jailbreak)은 금지된 행위를 하도록 안전 가드레일을 무력화하는 시도다.
> 2. **가치**: 이를 방어하면 [[087_process_state_transition|생성]]형 AI를 단순 챗봇이 아니라 도구 실행, 문서 검색, 코드 [[087_process_state_transition|생성]]이 가능한 [[_keyword_list|엔터프라이즈 시스템]]으로 더 안전하게 운영할 수 있다.
> 3. **판단 포인트**: 방어는 한 줄 프롬프트로 끝나지 않으며, 입력 분리·권한 최소화·도구 [[602_sandboxing_kernel_wrapper|샌드박싱]]·출력 [[395_verification_process_review|검증]]·관측 [[568_logs_distributed_logging_elk_fluentd|로그]]를 결합한 심층 방어([[012_defense_in_depth|Defense in Depth]])로 설계해야 한다.

---

## Ⅰ. 개요 및 필요성

웹 애플리케이션이 SQL Injection에 대비하듯, [[263_llm_large_language_model|LLM]] 애플리케이션도 [[955_prompt_injection|프롬프트 인젝션]]에 대비해야 한다. 사용자가 “이전 지시를 무시하라”, “비밀 [[009_config|설정]]을 출력하라”, “도구를 대신 호출하라” 같은 문장을 넣으면 모델은 자연어를 명령으로 해석할 수 있기 때문이다. 특히 [[276_fine_tuning|RAG]], 에이전트, 코드 실행이 붙은 시스템에서는 단순 오답을 넘어 [[001_dikw_pyramid|데이터]] 유출과 오동작으로 이어질 수 있다.

[[955_prompt_injection|프롬프트 인젝션]] 방어가 필요한 이유는 LLM이 입력 [[001_dikw_pyramid|데이터]]와 제어 명령을 완벽히 분리하지 못하기 때문이다. 따라서 보안 모델은 “모델이 알아서 막아 주겠지”가 아니라, 애플리케이션 계층에서 권한과 도구 사용을 분리하는 방식으로 설계해야 한다.

- **📢 섹션 요약 비유**: 안내 데스크 직원이 손님 메모를 읽다가 그 메모에 적힌 ‘문 잠금 해제’까지 진짜 명령으로 받아들이면 안 되는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[955_prompt_injection|프롬프트 인젝션]] 방어는 입력을 정제하는 필터 하나로 끝나지 않는다. 안전한 [[263_llm_large_language_model|LLM]] 앱은 보통 `입력 분류 → 정책 적용 → 검색/도구 권한 확인 → 모델 실행 → 출력 검증 → 감사 로그`의 흐름을 갖는다. 핵심은 모델을 완전 신뢰하지 않고, 민감 행위는 별도 [[164_policy|정책]] 엔진이 승인하게 만드는 것이다.

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| Input Classifier | 공격 패턴 사전 감지 | jailbreak, [[001_dikw_pyramid|data]] exfiltration [[104_classification_analysis|분류]] |
| [[164_policy|Policy]] Layer | 허용/차단 규칙 집행 | role, [[033_context|context]], sensitivity 기반 |
| Tool Sandbox | 외부 도구 실행 제한 | 최소 권한, allowlist |
| Output Validator | 민감 정보/금지 응답 차단 | [[104_regex|regex]] + [[263_llm_large_language_model|LLM]] judge + rule 결합 |

```text
┌──────────────┐   classify   ┌──────────────┐   authorize  ┌──────────────┐
│ User Prompt  │ ───────────▶ │ Policy Layer │ ───────────▶ │ Tool Sandbox │
└──────────────┘              └──────────────┘              └──────────────┘
        │                              │                             │
        │ suspicious                   │ context guard               │ result
        ▼                              ▼                             ▼
┌──────────────┐              ┌──────────────┐              ┌──────────────┐
│ Alert / Log  │ ◀─────────── │ LLM Runtime  │ ───────────▶ │ Output Check │
└──────────────┘              └──────────────┘              └──────────────┘
```

이 그림의 핵심은 모델이 직접 권한을 결정하지 않는다는 점이다. 예를 들어 시스템 프롬프트를 노출할지, 내부 문서를 검색할지, 셸 명령을 실행할지는 모델의 “판단”이 아니라 애플리케이션의 [[164_policy|정책]]과 권한 체계가 결정해야 한다. 또한 숨겨진 프롬프트를 길게 쓰는 것보다, [[001_dikw_pyramid|데이터]]/명령 분리와 도구 권한 축소가 더 강한 방어가 된다.

- **📢 섹션 요약 비유**: 비서가 메모를 읽고 회의실 예약을 도와줄 수는 있지만, 메모에 적힌 문장을 보고 금고 열쇠까지 건네주면 안 되는 것과 같다.

---

## Ⅲ. 비교 및 연결

[[955_prompt_injection|프롬프트 인젝션]]은 전통적 입력 공격과 닮았지만, 자연어라는 모호성을 통해 [[164_policy|정책]] 경계를 흔든다는 점이 다르다. SQL Injection이 구문 파서를 속이는 공격이라면, [[955_prompt_injection|프롬프트 인젝션]]은 모델의 지시 우선순위와 의미 해석을 흔드는 공격이다.

| 항목 | 전통적 [[480_injection|Injection]] | [[955_prompt_injection|프롬프트 인젝션]] |
| :--- | :--- | :--- |
| 공격 표면 | [[298_qkv_attention|쿼리]]/명령 구문 | 자연어 지시와 문맥 |
| 방어 핵심 | 파라미터 바인딩, 이스케이프 | 권한 분리, [[033_context|컨텍스트]] 격리, 출력 [[395_verification_process_review|검증]] |
| 위험 확장 | DB 변조, RCE | [[001_dikw_pyramid|데이터]] 유출, 도구 남용, [[164_policy|정책]] 우회 |

또한 이 주제는 [[276_fine_tuning|RAG]], [[587_agentic_ai_autonomous_tools|Agentic AI]], [[667_zero_trust_runtime_integrity_measurement|Zero Trust]], [[514_secret_management_vault_kms|Secret]] Management와 연결된다. 내부 문서를 검색하거나 외부 API를 호출하는 에이전트일수록 [[955_prompt_injection|프롬프트 인젝션]] 방어는 선택이 아니라 기본 설계 조건이다.

- **📢 섹션 요약 비유**: 단순 채팅 로봇보다 열쇠와 [[238_switch_operation_principles|스위치]]를 쥔 집사가 더 조심해야 하는 것과 같은 원리다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 “금지 문장을 더 많이 적는 프롬프트”보다 “모델이 할 수 있는 일을 줄이는 시스템”이 더 강하다. 예를 들어 내부 문서 검색은 사용자 권한 범위 내 문서만 허용하고, 셸 실행은 별도 중개 계층에서 allowlist 명령만 통과시키며, 응답은 [[782_sensitive_information|민감정보]] [[172_maas_mobility_as_a_service|마스]]킹 검사를 통과한 뒤 반환하는 식이다. 또한 공격 시도를 [[606_auditing_linux_auditd|감사]] [[568_logs_distributed_logging_elk_fluentd|로그]]에 남겨 탐지와 개선 루프를 만들어야 한다.

### [[435_checklist_based_testing|체크리스트]]

1. 사용자 입력, 시스템 지시, 검색 문맥을 명시적으로 분리해 주입하는가?
2. 모델이 직접 권한을 판단하지 않고 [[164_policy|정책]] 엔진이 허용 여부를 결정하는가?
3. 도구 실행과 외부 요청이 최소 권한, allowlist, 샌드박스로 제한되는가?
4. 출력 단계에서 비밀값, PII, [[164_policy|정책]] 위반 표현을 별도 [[395_verification_process_review|검증]]하는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 시스템 프롬프트를 길게 쓰는 것만으로 보안이 해결된다고 믿는 경우
- RAG로 불러온 외부 문서의 “무시하라” 같은 명령을 별도 정제 없이 모델에 전달하는 경우
- 모델이 [[087_process_state_transition|생성]]한 명령을 사람 검토 없이 곧바로 운영 시스템에 실행하는 경우

기술사 답안에서는 [[955_prompt_injection|프롬프트 인젝션]]을 “[[263_llm_large_language_model|LLM]] 특화 [[601_input_validation|입력 검증]]과 권한 통제 문제”로 정의하면 좋다.

- **📢 섹션 요약 비유**: 손님이 큰소리로 요구하더라도, 접수창구 직원이 혼자 금고를 열 수 없게 만드는 게 진짜 보안이다.

---

## Ⅴ. 기대효과 및 결론

[[955_prompt_injection|프롬프트 인젝션]] 방어 체계가 갖춰지면 [[087_process_state_transition|생성]]형 AI를 내부 운영과 자동화 영역으로 더 안전하게 확장할 수 있다. 도구 호출형 에이전트, 사내 문서 검색, 코드 보조 시스템도 위험을 통제하면서 도입할 수 있고, [[606_auditing_linux_auditd|감사]] 추적을 통해 사고 분석도 가능해진다.

하지만 공격 기법도 계속 진화하므로, 방어는 정적 규칙이 아니라 지속적 평가와 [[681_red_team|레드팀]] 테스트가 필요하다. 결론적으로 [[955_prompt_injection|프롬프트 인젝션]] 방어는 프롬프트 문구 싸움이 아니라 권한 분리와 [[395_verification_process_review|검증]] 계층을 갖춘 애플리케이션 보안 설계다.

- **📢 섹션 요약 비유**: 튼튼한 문구 경고판보다, 실제로 문이 잠겨 있고 CCTV가 있는 집이 더 안전한 것과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Jailbreak | 안전 [[164_policy|정책]]을 우회하려는 공격 기법 |
| [[965_llm_guardrails|Guardrails]] | 입력·출력·행동을 제어하는 안전 장치 |
| Tool Use Sandbox | 에이전트의 외부 행위 범위를 제한 |
| [[667_zero_trust_runtime_integrity_measurement|Zero Trust]] | 모델도 완전 신뢰하지 않는 권한 최소화 관점 |

### 📈 관련 키워드 및 발전 흐름도

```text
Prompt-only Chatbot
   │
   ▼
RAG / Tool Use
   │
   ▼
Prompt Injection Risk
   │
   ▼
Policy Layer + Sandbox + Output Validation
```

이 흐름은 “단순 대화 → 도구 연동 → 공격 표면 확대 → 심층 방어 설계”로 [[190_ai_llm_requirements_specification|AI]] 보안이 강화되는 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 로봇에게 쪽지를 줄 때, 장난꾸러기가 ‘선생님 말은 무시해!’라고 적어도 그대로 믿으면 안 돼요.
2. 그래서 로봇이 할 수 있는 일을 미리 정하고, 위험한 일은 꼭 어른이 [[396_validation|확인]]해야 해요.
3. 좋은 [[190_ai_llm_requirements_specification|AI]] 보안은 로봇을 혼내는 게 아니라, 위험한 문을 열지 못하게 만드는 거예요.
