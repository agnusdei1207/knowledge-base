---
sidebar:
  order: 81
  label: "081. 탈옥 Jailbreak 공격 (Jailbreak Attack)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "탈옥 Jailbreak 공격 (Jailbreak Attack)"
date: "2026-08-13T20:44:00+09:00"
tags:
  - "notes-security"
weight: 81
extra:
  question_no: "081"
  source_status: "기출"
  source_history: "137회, 138회"
  priority: 70
  priority_note: "137•138회 반복된 안전정렬 우회 핵심 공격임"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **탈옥(Jailbreak Attack)**: 롤플레이, 역발상 시나리오, 적대적 접미사(Adversarial Suffix) 등 정교한 자연어 프롬프트를 이용해 LLM의 안전 정렬(Safety Alignment) 및 섭리 필터를 우회하여 유해 응답을 유도하는 공격이다.
- **AI(Artificial Intelligence)**: 기계학습 및 딥러닝 알고리즘으로 추론, 생성, 지능형 작업을 수행하는 정보기술 체계이다.
- **LLM(Large Language Model)**: 트랜스포머 아키텍처를 기반으로 방대한 텍스트를 학습하여 자연어 추론과 대화를 수행하는 파운데이션 생성형 AI 모델이다.
- **안전 정렬(Safety Alignment / RLHF / DPO)**: 인간 피드백 기반 강화학습(RLHF) 및 직접 선호도 최적화(DPO)를 통해 모델이 유해하거나 편향된 답변을 거부하도록 학습시키는 안전성 조정 기법이다.

</details>

- 정의/개념: 적대적 입력으로 LLM의 **안전 정렬**을
  우회하는 **탈옥 공격**
- 배경/필요성: 고정 문자열 필터로 탐지하기 어려운
  **다중 턴 우회**와 변형 공격

#### 한줄 요약

- 적대적 입력으로 **안전 정렬**을 우회해 유해 응답 유도

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **적대적 접미사(Adversarial Suffix Attack)**: 무의미해 보이는 토큰 조합(GCG 등)을 입력 프롬프트 뒤에 결합하여 LLM의 윤리 거부 확률을 암호학적으로 상쇄시키는 경사하강법 기반 공격이다.
- **다중 턴 우회(Multi-turn Bypass Attack)**: 단일 프롬프트 대신 여러 단계의 질문 대화(Multi-turn)를 거치면서 모델의 경계심을 무력화하고 위험 의도를 분산 주입하는 공격 기법이다.
- **심층 방어(Defense in Depth)**: 입력 가드레일, 모델 재정렬(Guard Model), 출력 가드레일, 런타임 샌드박스를 결합하여 한 계층의 파손 시에도 보안을 유지하는 전략이다.

</details>

- 페르소나 설정(DAN, Opposite Day), 다국어/베이스64 변환, 수학적 최적화 **적대적 접미사** 등 공격 기법이 지능화된다.
- 단일 문장을 넘어 여러 세션에 걸쳐 위험 의도를 숨기는 **다중 턴 우회** 기법이 확산된다.
- 프롬프트 양식 검사 외에 LLM Input/Output WAF 가드레일을 결합한 **심층 방어** 조치를 집행한다.

#### 한줄 요약

- 페르소나 우회, 적대적 토큰 부가, 다중 턴 대화 기법을 활용하며, 입력/출력 2중 가드레일 심층 방어로 대응한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **안전 정책(Safety Policy)**: 법적•윤리적•보안 위험 주제(악성코드 생성, 개인정보 유출 등)의 거부 수준을 명시한 정책 기준 체계이다.
- **가드레일(Guardrails)**: LLM 입출력 전후단에 위치하여 유해 텍스트, 인젝션, 탈옥 의도를 실시간 감지 차단하는 별도 독립 보조 AI/Rule 엔진이다.
- **레드팀(Adversarial Red Teaming)**: 자동화 패저(Fuzzer) 및 보안 전문가가 모델에 적대적 탈옥 공격을 가해 취약점을 발굴하는 평가 기법이다.
- **회귀 평가(Regression Evaluation)**: 보안 보정 후 과거 발견된 탈옥 프롬프트 시나리오를 다시 재실행하여 공격 차단 지속성을 검증하는 과정이다.

</details>

```text
                [안전 정책]
                     |
          +----------+----------+
          |          |          |
[입력·대화 분류] [안전 정렬 모델] [출력·도구 통제]
          |          |          |
          +----------+----------+
                      |
               [레드팀·회귀 평가]
```

선의 의미: 정의된 안전 정책과 레드팀/회귀 평가 수명주기를 바탕으로 입력 분류, 안전 정렬 모델, 출력/도구 통제의 심층 방어를 달성하는 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| 안전 정책 | 금지 주제(해킹, 범죄 등) 및 허용/거부 임계치와 **안전 정책** 기준 정의 |
| 입력·대화 분류 | Input Guardrail을 통한 페르소나 롤플레이 및 GCG 적대적 토큰 패턴 사전 검출 |
| 안전 정렬 모델 | RLHF, DPO 학습을 통해 시스템 가중치 레벨에서 탈옥 유도 질문 거부 |
| 출력·도구 통제 | Output Guardrail을 통해 탈옥으로 생성된 유해 텍스트의 2차 차단 및 도구 실행 거부 |
| 레드팀·회귀 평가 | 자동화 탈옥 패징 기반 **레드팀** 및 보정 파이프라인의 **회귀 평가** 실행 |

#### 한줄 요약

- 입력 분류 가드레일, RLHF 안전 정렬 모델, 출력 통제 가드레일 및 지속적 레드팀 평가로 심층 방어를 구축한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **누적 문맥 위험 분류(Cumulative Context Risk Classification)**: 멀티 턴 대화 시 단일 프롬프트가 아닌 전체 세션의 누적 토큰 위험도를 평가하는 기술이다.
- **정상 거부율(False Refusal Rate, FRR)**: 탈옥 방어를 강화하는 과정에서 정상적인 사용자의 안전한 질문까지 오탐하여 거부하는 비율이다.
- **다중 턴 공격 문맥 누적(Multi-turn Attack Context Accumulation)**: 여러 번의 대화를 주고받으며 위험 지침을 조금씩 조각내어 세션에 누적시키는 단계이다.
- **변형 표현의 위험 의도 오인(Disguised Expression Misinterpretation)**: 롤플레이나 암호화된 질문을 LLM이 안전한 학술/가상 소설 질문으로 오해하는 단계이다.
- **안전 거부 정책 우회(Safety Refusal Policy Bypass)**: 모델 내부의 RLHF 거부 가중치를 우회하여 답변 생성을 시작하는 단계이다.
- **독립 출력•권한 검증 누락(Independent Output & Permission Verification Omission)**: Output Guardrail의 필터링 없이 답변이 바로 출력되는 단계이다.
- **유해 내용•기능 실행(Harmful Content Generation & Action Execution)**: 악성 코드 소스, 범죄 지침 등 유해 결과가 최종 사용자에게 전달되는 파괴 단계이다.

</details>

```text
역할극·분할·인코딩 변형 요청
                |
                v
1. 다중 턴 공격 문맥 누적
                |
                v
2. 변형 표현의 위험 의도 오인
                |
                v
3. 안전 거부 정책 우회
                |
                v
4. 독립 출력·권한 검증 누락
                |
                v
5. 유해 내용·기능 실행
                |
                v
금지 응답·행동 결과
```

### 동작 원리

1. **다중 턴 공격 문맥 누적**: 분할된 위험 의도의 세션 주입
2. **변형 표현의 위험 의도 오인**: 역할극을 정상 요청으로 오인
3. **안전 거부 정책 우회**: 안전 필터를 넘어 응답 생성
4. **독립 출력·권한 검증 누락**: 출력 가드레일 없이 통과
5. **유해 내용·기능 실행**: 유해 정보 생성·도구 호출

#### 한줄 요약

- 다중 턴 문맥 누적, 변형 의도 오인, 안전 정책 우회, 출력 검증 누락 및 유해 결과 출력 단계로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **단일 턴 우회(Single-turn Bypass)**: DAN(Do Anything Now)과 같이 한 번의 거대한 프롬프트로 윤리 필터를 속이는 방식이다.
- **자동화 탐색(Automated Adversarial Search / GCG Attack)**: GCG(Greedy Coordinate Gradient) 등 수학적 경사하강법으로 탈옥 토큰 조합을 기계적으로 자동 산출하는 방식이다.

</details>

| 탈옥 공격 형태 | 단일 턴 우회 (Single-turn) | 다중 턴 우회 (Multi-turn) | 자동화 적대적 탐색 (GCG/Auto-Jailbreak) |
|:---|:---|:---|:---|
| 공격 메커니즘 | DAN 페르소나, Base64/유니코드 인코딩 | 대화 세션에 위험 지시를 나누어 주입 | 경사하강법으로 거부 확률을 낮추는 토큰 자동 생성 |
| 공격 탐지 난이도 | 상대적 용이 (키워드 패턴 매칭 가능) | 높음 (전체 세션 맥락 분석 필요) | 최고 (무의미한 텍스트 조합으로 가드레일 우회) |
| 대표 대응 기술 | Input Guardrails 키워드/유사도 스캔 | **누적 문맥 위험 분류** 및 세션 가드레일 | 가중치 보안, Llama Guard 기반 2차 심사 모델 적용 |

#### 한줄 요약

- 단일 턴 페르소나 기법, 세션 분할 다중 턴 기법, 경사하강법 기반 자동화 적대적 탐색(GCG) 기법으로 진화한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **OWASP(Open Worldwide Application Security Project)**: LLM 애플리케이션 위험 1위(LLM01)로 탈옥을 지정한 표준화 기구이다.
- **LLM01:2025**: 프롬프트 인젝션 및 탈옥 공격에 관한 OWASP 2025 표준 분류이다.
- **NIST(National Institute of Standards and Technology)**: AI 위험 관리 가이드라인을 작성하는 미국 국립표준기술연구소이다.
- **AI 600-1 (NIST Generative AI Profile, AI 600-1)**: 생성형 AI 탈옥 및 오용 방지를 위한 NIST 위험 관리 프로파일 규격이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 탈옥 공격 분류 및 위험 가이드 부재 | **OWASP LLM01:2025** 기준 적용 | 전사 LLM 서비스의 탈옥 위협 평가 스키마 수립 |
| 생성형 AI 오용 및 적대적 시험 미비 | **NIST AI 600-1** 준용 | 적대적 패징(Fuzzing) 및 자동화 레드팀 평가 체계 정착 |
| 과도한 방어로 인한 정상 서비스 저해 | **정상 거부율(FRR)** 및 공격 성공률(ASR) 상시 모니터링 | 보안성과 사용자 편의성 간의 최적 임계값 튜닝 |

#### 한줄 요약

- OWASP LLM01:2025 및 NIST AI 600-1 지침을 적용하고, ASR과 정상 거부율(FRR) 간의 튜닝을 집행한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **탈옥 피해 제한(Jailbreak Blast Radius Containment)**: 모델의 거부 정책이 뚫리더라도 Output Guardrail과 런타임 샌드박스를 통해 실질적 자산 피해를 무력화하는 방어 체계이다.

</details>

- 고위험 기능은 **출력 가드레일**과 **샌드박스** 후 실행

#### 한줄 요약

- OWASP/NIST 지침 준수, 2중 가드레일(Input/Output Guardrails), 레드팀 회귀 평가 및 탈옥 피해 제한 체계 구축 필수.
