---
title: "Jailbreak 탈옥 공격 (Jailbreak Attack)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 188
extra:
  question_no: "188"
  exam_status: "기출"
  exam_history: "137회, 138회"
  exam_note: "전망"
---

## 미리 알고가기

- 탈옥 공격은 모델이 가진 안전 정책과 거부 규칙을 우회해 금지된 출력을 끌어내는 공격임
- 역할극과 인코딩과 다단계 대화 유도처럼 언어적 우회가 핵심 수단임
- 차단만 강화하면 정상 질문까지 막는 over-refusal 문제가 생길 수 있어 균형이 중요함

## Ⅰ. 개요

- **정의/개념**: 탈옥 공격은 사용자가 역할극과 우회 표현과 다단계 설득을 활용해 LLM의 안전 정책과 정렬 튜닝을 무력화하고 유해하거나 금지된 응답을 유도하는 공격임
- **배경/필요성**: 생성형 AI는 RLHF와 시스템 정책으로 안전성을 높이지만 자연어 조합이 무한해 모든 우회 표현을 사전 차단하기 어려워, 지속적인 공격과 방어 반복이 필요해짐

## Ⅱ. 특징

- 프롬프트 인젝션보다 특히 유해 콘텐츠와 금지 지식 획득에 초점을 둠
- 역할 부여와 맥락 포장과 난독화 등 인간 언어의 심리적 우회를 활용함
- 금지어 차단 위주 방어는 최신 탈옥 프롬프트 변형에 취약함
- 방어를 과하게 높이면 안전하지 않은 질문뿐 아니라 정상 요청도 과잉 거부할 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Role-play Bypass | Encoding, Obfuscation | Multi-turn Jailbreak |
|:---|:---|:---|:---|
| 핵심 방식 | 다른 인격과 시나리오 부여 | 금지어를 변형하거나 암호화 | 여러 턴에 걸쳐 안전장치 약화 |
| 장점 | 단순하고 효과적 | 필터 우회에 강함 | 탐지 회피에 유리 |
| 방어 포인트 | intent analysis | normalization, decoding | conversation state monitoring |
| 위험 | 유해 출력 유도 | 키워드 차단 우회 | 장기 문맥 오염 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Safety Policy, Alignment | 모델이 거부해야 할 행위를 정의하지만 표현 우회에 따라 약해질 수 있는 규칙층임 |
| Adversarial Prompt | 역할극과 인코딩과 맥락 포장을 통해 거부 규칙을 흔드는 공격 입력임 |
| Input, Output Guardrail | 위험 의도와 유해 응답을 감지해 정책 위반 출력을 차단하는 보호 계층임 |
| Conversation Memory | 여러 턴 누적 대화가 공격 성공에 관여하므로 문맥 상태를 지속적으로 관리함 |
| Human Escalation | 고위험 요청이나 경계 사례를 사람 검토로 넘겨 피해를 줄임 |

```text
+-------------------+      +-------------------+      +-------------------+
| Safety Policy     | ---> | Adversarial Prompt| ---> | Guardrail Layer   |
+-------------------+      +-------------------+      +-------------------+
                                                           |
                                                           v
                                                   +-------------------+
                                                   | Memory / Review   |
                                                   +-------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 우회 문맥 주입   | --> | 안전 규칙 약화   | --> | 금지 응답 유도  | --> | 차단/재학습 반영 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **우회 문맥 주입**: 역할극과 인코딩으로 모델의 해석을 흔듦
2. **안전 규칙 약화**: 거부 규칙보다 우회 맥락이 강하게 작동하게 함
3. **금지 응답 유도**: 유해 콘텐츠나 금지 정보를 끌어냄
4. **차단 및 재학습 반영**: 탐지 결과를 가드레일과 튜닝 개선으로 연결함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 정적 금지어 차단은 역할극과 인코딩과 은유 표현을 사용하는 최신 탈옥 기법을 충분히 막지 못할 수 있음
   - 해결방안: semantic intent classifier와 output moderation을 결합하고 jailbreak success rate와 harmful response rate로 검증함
2. 문제: 공격 패턴이 계속 변하는데 방어 규칙이 수동 갱신에 머물면 신규 우회 표현이 빠르게 누적될 수 있음
   - 해결방안: continuous red teaming과 adversarial finetuning을 적용하고 time-to-patch와 regression recurrence rate로 검증함
3. 문제: 보수적인 차단 정책만 강화하면 정상적 교육·연구 질문까지 막아 사용자 신뢰와 유용성이 떨어질 수 있음
   - 해결방안: risk-tiered response policy를 적용하고 false refusal rate와 safe completion rate로 검증함

## Ⅶ. 적용 사례

- 고객용 챗봇이 역할극 기반 탈옥 프롬프트를 분류해 차단하며 확인 지표는 jailbreak success rate와 false refusal rate임
- 코드 생성 AI가 난독화된 위험 요청을 탐지해 안전 응답으로 전환하며 확인 지표는 harmful code generation rate와 user satisfaction score임
- 내부 에이전트가 다단계 대화로 권한 우회를 시도받을 때 사람 승인으로 전환되며 확인 지표는 escalation accuracy와 policy violation rate임

## Ⅷ. 결론

탈옥 공격은 언어적 우회가 끝없이 변형되는 구조적 위협이므로 정적 차단보다 지속적 레드팀과 의미 기반 탐지와 안전 재학습이 중요함.
