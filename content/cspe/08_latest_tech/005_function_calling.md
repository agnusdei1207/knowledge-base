---
title: "Function Calling (함수 호출)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-latest-tech"
weight: 5
---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **개요**: **Function Calling**은 사용자의 자연어 요청을 분석하여, 사전에 정의된 특정 함수의 이름과 파라미터를 JSON 형식으로 출력하도록 학습된 LLM의 기능이다.
- **필요성**: LLM의 응답은 기본적으로 비정형 텍스트이다. 이를 코드에서 활용하려면 파싱(Parsing) 과정이 필요한데, Function Calling은 모델이 직접 **정형화된 JSON**을 내뱉게 함으로써 시스템 간 연동의 정확도를 획기적으로 높인다.
- **핵심 직관**: **"말을 코드로 번역해주는 API 브릿지"**. 사용자의 "서울 날씨 알려줘"를 `get_weather(location="Seoul")`라는 데이터로 바꿔주는 기능이다.

## 깊이 이해
- **배경 (From Parsing to Calling)**: 과거에는 "JSON으로만 답해줘"라고 강하게 프롬프팅했지만, 모델이 형식을 어기는 경우가 잦았다. OpenAI를 필두로 모델의 미세조정(Fine-tuning)을 통해 함수 호출 규격을 내재화한 기능이 출시되면서 대세가 되었다.
- **작동 원리 (The Cycle)**:
    1. **Function Registration**: 개발자가 사용할 함수의 명세(Name, Description, Parameters)를 API 호출 시 전달.
    2. **Model Reasoning**: 사용자의 발화가 함수 호출이 필요한 상황인지 판단.
    3. **Function Call Response**: 모델이 텍스트 대신 `finish_reason: "function_call"`과 함께 JSON 데이터를 반환.
    4. **Local Execution**: 개발자의 코드 환경에서 실제 함수를 실행.
    5. **Result Feedback**: 함수의 실행 결과를 다시 모델에게 전달하여 최종 답변 생성.
- **비유**: 외국인 고객(사용자)의 모호한 주문을 전문 통역사(LLM)가 주방장(개발자/함수)이 바로 이해할 수 있는 표준 주문서(JSON)로 정확히 작성해주는 것과 같다.
- **구체 예시**: OpenAI `gpt-4o-2024-08-06` 버전부터 지원하는 **Structured Outputs**는 Function Calling의 정확도를 100% 보장하도록 업그레이드된 형태다.
- **주의점**: 모델은 함수를 **직접 실행하지 않는다**. 실행에 필요한 '데이터'만 만들 뿐이며, 실제 호출은 애플리케이션 코드 단에서 수행해야 한다.

## 연결 개념
- **Tool Use (004)**: Function Calling을 포함한 더 넓은 범위의 도구 활용 개념.
- **JSON Schema (115)**: 함수 파라미터의 규격을 정의하는 표준 언어.
- **Structured Output**: Function Calling의 안정성을 극복하기 위해 등장한 강제 출력 기술.

---

# 📝 【답안용】 시험 답안 템플릿

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 비정형 자연어를 정형화된 프로그래밍 명령(JSON)으로 변환하도록 미세조정된 LLM의 핵심 기능.
> 2. **가치**: 텍스트 생성의 불확실성을 제거하고, 외부 시스템과의 신뢰성 있는 인터페이스(Reliable Interfacing) 제공.
> 3. **판단 포인트**: 모델이 함수를 직접 실행하는 것이 아닌, **'호출 의사(Intent)'와 '인자(Arguments)'만 생성**한다는 점을 명확히 인지해야 함.

## 출제 의도 및 답안 포인트
- **출제 의도**: 에이전트 구현의 핵심 기술인 Function Calling의 작동 메커니즘과 정합성 보장 방안 이해.
- **핵심 포인트**: JSON Schema, 파싱 에러 제로, 미세조정(Fine-tuning), 구조화 출력(Structured Outputs).

---

## Ⅰ. Function Calling(함수 호출)의 개념 및 핵심 목적
### 1. Function Calling의 정의
- LLM이 사용자의 질문에 답하기 위해 외부 프로그래밍 함수가 필요하다고 판단될 경우, 해당 함수의 규격에 맞는 **구조화된 데이터(JSON)**를 생성하는 기술.
### 2. 핵심 목적
- **비정형 데이터의 구조화**: 자유 양식의 텍스트를 기계가 읽을 수 있는 데이터로 변환.
- **외부 시스템 연동**: API 호출, DB 쿼리, 코드 실행 등과의 연동 신뢰성 확보.
- **워크플로우 자동화**: 자연어 명령으로 시작되는 복잡한 업무 프로세스의 트리거 역할.

---

## Ⅱ. Function Calling의 작동 아키텍처 및 데이터 흐름
- **LLM과 애플리케이션 간의 5단계 인터랙션**
```text
[ User Query ] -> [ LLM (Reasoning) ] 
                       ↓ (Function Call: JSON 반환)
[ App Logic (Execute Function) ] 
                       ↓ (Result: 실행 결과 수집)
[ LLM (Answer Generation) ] -> [ Final Response ]
```

| 단계 | 주체 | 동작 상세 |
|:---:|:---:|:---|
| **Step 1: 명세 전달** | App -> LLM | 사용 가능한 함수들의 JSON Schema 목록을 프롬프트와 함께 전달 |
| **Step 2: 의도 파악** | LLM | 질문 분석 후 '함수 호출'이 필요한지 결정 |
| **Step 3: JSON 생성** | LLM | 함수의 인자(Arguments)를 추출하여 유효한 JSON 포맷으로 출력 |
| **Step 4: 실제 실행** | App Code | JSON 데이터를 파싱하여 로컬/원격 함수를 실제로 실행 |
| **Step 5: 최종 응답** | LLM | 실행 결과를 컨텍스트에 추가하여 사용자에게 줄 최종 문장 생성 |

---

## Ⅲ. 기술적 신뢰성 보장: Structured Outputs
- **기존 Function Calling의 한계**: 모델이 드물게 스키마를 어기거나 잘못된 데이터 타입을 생성하는 문제.
- **Structured Outputs (OpenAI 최신 기능)**:
    - **Strict Mode**: 모델 응답이 사전에 정의된 JSON Schema와 100% 일치하도록 보장.
    - **Constrained Decoding**: 생성 과정에서 문법적으로 스키마에 어긋나는 토큰의 확률을 0으로 만들어 오류 원천 차단.

---

## Ⅳ. 주요 활용 시나리오 및 사례

| 활용 분야 | 동작 예시 | 기대 효과 |
|:---:|:---|:---|
| **API 커넥터** | "이메일 보내줘" -> `send_email(to, subject, body)` 생성 | 자연어 기반 서비스 제어 |
| **데이터 추출** | 긴 뉴스 기사 -> `{ summary, entities: [], sentiment }` 추출 | 비정형 문서의 정형화 보관 |
| **DB 쿼리 생성** | "지난달 매출 얼마야?" -> `query_sales(month="2024-06")` | 노코드 데이터 분석 구현 |
| **멀티 턴 대화** | "제주도 항공권 예약해줘" -> 부족한 정보(날짜 등) 확인 루프 | 업무 완결성 보장 |

---

## Ⅴ. Function Calling 구현 시 주의사항 및 고려사항
- **스키마 설계의 단순화**: 파라미터가 너무 많거나 설명(Description)이 모호하면 모델이 혼동하여 잘못된 값을 추출할 수 있음.
- **보안 가드레일**: 모델이 생성한 JSON 데이터를 검증 없이 시스템에 바로 주입하지 말고, 반드시 유효성 검사(Validation) 및 권한 확인(Auth) 후 실행.
- **예외 처리**: 함수 실행 결과가 에러일 경우, 이를 다시 모델에게 전달하여 모델이 사용자에게 정중히 설명하거나 대안을 찾도록 설계.

---

## Ⅵ. 기술사 관점의 결론 및 제언
- **본질적 가치**: Function Calling은 AI가 '말 잘하는 생성기'에서 **'시스템 제어기'**로 넘어가는 핵심 관문임.
- **미래 방향**: 앞으로 모든 API 명세는 인간용 문서와 더불어 AI가 즉시 이해할 수 있는 **에이전트용 명세(MCP 등)**를 필수로 포함하게 될 것임.

### 🔀 문제 유형별 목차 전환
- **설명형**: Ⅱ. 아키텍처 및 데이터 흐름을 상세 도식화하여 기술.
- **비교/심화형**: Ⅲ. Structured Outputs의 원리(Constrained Decoding)를 통해 신뢰성 확보 방안 강조.
