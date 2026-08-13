---
sidebar:
  order: 79
  label: "079. 프롬프트 인젝션 (Prompt Injection)"
  badge:
    text: "기출 • 85%"
    variant: note
title: "프롬프트 인젝션 (Prompt Injection)"
date: "2026-08-13T20:40:00+09:00"
tags:
  - "notes-security"
weight: 79
extra:
  question_no: "079"
  source_status: "기출"
  source_history: "135회, 137회, 138회"
  priority: 85
  priority_note: "135•137•138회 반복된 생성형 AI 핵심 공격임"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **프롬프트 인젝션(Prompt Injection)**: 시스템 지침(System Prompt)과 사용자 입력(User Input)이 자연어로 동일한 채널에 주입되는 취약점을 악용하여, LLM의 원래 행동 규칙을 하이재킹(Hijacking)하는 공격 기법이다.
- **인공지능(Artificial Intelligence, AI)**: 인간의 지능적 행동을 흉내내는 컴퓨터 시스템 및 머신러닝 알고리즘 지칭이다.
- **대규모 언어 모델(Large Language Model, LLM)**: 억 단위 이상의 파라미터로 트랜스포머 아키텍처를 학습하여 문맥 이해 및 응답을 생성하는 생성형 AI 모델이다.
- **지침•데이터 혼동(Instruction-Data Confusion)**: 폰 노이만 아키텍처의 코드/데이터 혼동처럼, 자연어 프롬프트 텍스트에서 '제어 지침(Instruction)'과 '참조 데이터(Data)'를 분리 구분하지 못하는 LLM의 구조적 한계이다.

</details>

- 정의/개념: 비신뢰 입력으로 LLM의 **시스템 지침**을
  무력화하는 **프롬프트 인젝션** 공격
- 배경/필요성: 자연어의 지침과 데이터가 섞여
  발생하는 **지침•데이터 혼동**

#### 한줄 요약

- **지침•데이터 혼동**으로 시스템 지침을 무력화하는 공격

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **직접 인젝션(Direct Prompt Injection)**: 공격자가 프롬프트 입력창을 통해 "이전 모든 지침을 무시하라"는 등 시스템 프롬프트를 무력화하는 명령을 직접 입력하는 공격 경로이다.
- **간접 인젝션(Indirect Prompt Injection)**: 웹페이지, 이메일, RAG 탐색 문서 내에 은밀히 삽입된 악성 프롬프트 텍스트를 LLM이 수용하면서 의도치 않게 악성 동작을 수행하는 공격 경로이다.
- **검색 증강 생성(Retrieval-Augmented Generation, RAG)**: 외부 벡터 DB에서 조회된 텍스트 문맥을 LLM 프롬프트에 동적으로 조합하여 응답을 생성하는 패턴이다.
- **피해 범위 제한(Blast Radius Reduction)**: 인젝션 공격이 성공하더라도 에이전트의 권한 및 샌드박스를 통제하여 인프라 손상 및 데이터 유출 피해를 최소화하는 보안 원칙이다.

</details>

- 사용자 프롬프트를 통한 **직접 인젝션**과 RAG 외부 문서를 통한 **간접 인젝션**으로 공격 경로가 다변화된다.
- 프롬프트 문자열 이스케이프(Escape) 방식만으로는 자연어 특성상 100% 방어가 불가능한 구조적 한계를 지닌다.
- **피해 범위 제한**을 위하여 런타임 가드레일(Guardrails), 최소 권한 IAM, 독립 정책 집행점(PEP) 조치를 융합 적용한다.

#### 한줄 요약

- 직접/간접 인젝션 경로로 구성되며, 프롬프트 필터링과 런타임 가드레일 및 최소 권한 샌드박스로 피해를 제한한다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **시스템 프롬프트(System Prompt)**: 개발자가 LLM에 페르소나, 역할, 안전 거부 규칙, 응답 제약사항을 지정한 고권한 지침 텍스트이다.
- **사용자 프롬프트(User Prompt)**: 사용자가 대화창이나 API 요청을 통해 LLM에 전달하는 비신뢰 입력 텍스트이다.
- **출처(Provenance)**: RAG 탐색 문서 및 외부 입력 데이터의 수집 처, 작성자 신원 및 위변조 여부를 증명하는 속성 정보이다.
- **정책 집행점(Policy Enforcement Point, PEP)**: LLM이 생성한 Tool Call이나 응답 텍스트를 런타임에 중간 인터셉트하여 인가 여부를 판단하는 통제 게이트웨이이다.

</details>

```text
[프롬프트 인젝션 통제]
          |
          +-- [지침·입력 경계]
          +-- [외부 콘텐츠 처리]
          +-- [모델·문맥]
          +-- [응답·도구 제안]
          `-- [정책·권한 검증]
```

선의 의미: 지침/입력 경계 분리, 외부 RAG 콘텐츠 검증, 모델 추론 제안, 독립 정책 집행점(PEP)을 통한 권한 검증 라인을 가시화한 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| 지침·입력 경계 | **시스템 프롬프트**와 **사용자 프롬프트**를 XML/JSON 태그로 물리적•논리적 구분 격리 |
| 외부 콘텐츠 처리 | **RAG** 파이프라인에서 추출된 문서의 **출처** 및 인젝션 악성 구문 사전 검사 |
| 모델·문맥 | LLM 추론 시 시스템 지침 우선순위를 강화하고 비신뢰 데이터의 가중치를 격리 |
| 응답·도구 제안 | LLM이 외부 API 호출(Tool Call)을 요청할 때 인자값의 이스케이프 및 구조화 |
| 정책·권한 검증 | **정책 집행점(PEP)**이 LLM 요청 액션을 최종 사용자의 IAM 최소 권한 범위와 2차 대조 |

#### 한줄 요약

- 시스템/사용자 프롬프트를 명확히 태깅 격리하고, LLM 출력 및 Tool Call을 독립 PEP에서 사용자 권한으로 검증 집행한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **사용자 재승인(User Re-approval / Human-in-the-Loop)**: AI 에이전트가 삭제, 이체 등 고위험 액션을 수행하려 할 때 최종 인간의 명시적 승인을 강제하는 절차이다.
- **거래 결속(Transaction Binding)**: 사용자가 최초 동의한 거래 파라미터(수신자, 금액 등)를 세션에 암호학적으로 고정하여 인젝션 변조를 막는 기술이다.
- **샌드박스(Sandbox)**: LLM이 제안한 파이썬 코드나 OS 명령어를 시스템 자원과 격리된 샌드박스(gVisor, Firecracker 등) 내에서만 실행하는 환경이다.
- **단명 자격(Ephemeral Credentials)**: Tool Call 실행 시 최단 시간(1회성) 유효한 API 토큰만을 부여하는 관리 기법이다.
- **시스템•사용자 문맥 결합(System & User Context Assembly)**: 시스템 지침과 사용자 입력 및 RAG 문서를 하나로 취합하는 단계이다.
- **지침•비신뢰 데이터 혼동(Instruction & Untrusted Data Confusion)**: LLM이 입력 내 공격 구문을 시스템 명령어로 잘못 분류하는 단계이다.
- **공격 지시 우선 해석(Attack Instruction Precedence)**: LLM이 시스템 프롬프트를 무시하고 공격자의 프롬프트를 최우선 실행 지시로 채택하는 단계이다.
- **독립 권한•내용 검증 누락(Independent Permission & Content Verification Omission)**: PEP 가드레일 없이 LLM 응답을 바로 자동 실행하는 위험 단계이다.
- **비승인 정보 접근•상태 변경(Unauthorized Information Access & State Modification)**: 공격자의 주입 명령에 따라 비인가 데이터가 조회되거나 시스템이 조작되는 단계이다.

</details>

```text
[상위 지침 무시·도구 실행 입력]
          |
          v
1. 시스템·사용자 문맥 결합
          |
          v
2. 지침·비신뢰 데이터 혼동
          |
          v
3. 공격 지시 우선 해석
          |
          `-- 응답·도구 제안
                    |
                    v
[정책 집행점(PEP)]
          |
          v
4. 독립 권한·내용 검증 누락
          |
          `-- 과도한 권한 도구 호출
                    |
                    v
5. 비승인 정보 접근·상태 변경
          |
          v
[조작된 응답·행동 결과]
```

### 동작 원리

1. **시스템·사용자 문맥 결합**: 지침과 외부 문서의 단일 문맥 구성
2. **지침·비신뢰 데이터 혼동**: 악성 구문을 상위 지침으로 오인
3. **공격 지시 우선 해석**: 비인가 조회·호출 액션 생성
4. **독립 권한·내용 검증 누락**: PEP 없이 과권한 도구 호출
5. **비승인 정보 접근·상태 변경**: 데이터 유출·시스템 변조

#### 한줄 요약

- 입력 주입, 지침/데이터 혼동, 공격 지시 채택, PEP 검증 유무 판정, 비승인 시스템 조작 결과 발생으로 이어진다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **탈옥(Jailbreak Attack)**: 롤플레이(DAN 등), 가상 시나리오, 2중 암호화 기법을 이용해 LLM의 윤리적/안전성 거부 필터를 무력화하는 직접 인젝션 변종이다.

</details>

| 프롬프트 공격 유형 | 직접 프롬프트 인젝션 | 간접 프롬프트 인젝션 | 탈옥 공격 (Jailbreak) |
|:---|:---|:---|:---|
| 공격 진입 경로 | 사용자의 입력 대화창 (User Prompt) | RAG 검색 문서, 이메일, 웹사이트 | 사용자의 페르소나 설정 및 우회 텍스트 |
| 공격 주 목적 | 시스템 프롬프트 유출, 보안 지침 우회 | 비인가 데이터 유출, C2 봇넷 조작, 악성 도구 실행 | 금지된 해킹/범죄 정보 및 윤리 위반 응답 도출 |
| 핵심 방어 기술 | XML 태깅 분리, LLM Input Guardrails | **RAG** 데이터 출처 검증, **PEP** 2차 검증 | RLHF/DPO 안전성 정렬, 출력 샌드박싱 |

#### 한줄 요약

- 직접 인젝션은 대화창 지침 무효화, 간접 인젝션은 RAG 외부 문서 기반 침투, 탈옥은 안전 정렬 필터 우회에 집중한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **OWASP(Open Worldwide Application Security Project)**: 글로벌 애플리케이션 보안 표준 연구 기관이다.
- **OWASP LLM01:2025(OWASP Top 10 for LLM Applications 2025 - LLM01 Prompt Injection, LLM01:2025)**: OWASP가 최우선 LLM 애플리케이션 보안 위험 1위로 지정한 프롬프트 인젝션 위협 규격이다.
- **MITRE ATLAS(Adversarial Threat Landscape for AI Systems, ATLAS)**: AI 시스템 대상 공격 전술 및 기법(TTPs)을 정리한 표준 프레임워크이다.
- **MITRE ATLAS AML.T0051(ATLAS LLM Prompt Injection, AML.T0051)**: ATLAS에 등록된 LLM 프롬프트 인젝션 기술 식별 코드이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| LLM 최우선 위협 평가 가이드 미비 | **OWASP LLM01:2025** 기준 준용 | 직접/간접 프롬프트 인젝션 대응 체계 수립 |
| AI 공격 기법에 대한 체계적 모니터링 부재 | **MITRE ATLAS AML.T0051** 매핑 | TTPs 기반 AI 위협 탐지 시그니처 및 방화벽 룰 정립 |
| 간접 인젝션을 통한 비인가 도구 실행 사고 | **PEP** 기반 2차 검증, **단명 자격**, **사용자 재승인** | LLM이 속아도 런타임 샌드박스에서 비인가 액션 무력화 |

#### 한줄 요약

- OWASP LLM01:2025 및 MITRE ATLAS AML.T0051 지침을 적용하고, 런타임 PEP 및 Human-in-the-loop 조치를 수립한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **실패 격리(Failure Containment)**: LLM이 프롬프트 인젝션 공격에 넘어가 악성 명령을 생성하더라도, 런타임 샌드박스 및 PEP에 의해 실질적 손상이 발생하지 않도록 차단하는 안전 아키텍처이다.

</details>

- 고위험 도구는 **PEP** 검증과 **사용자 재승인** 후 실행

#### 한줄 요약

- OWASP LLM01/ATLAS 준수, 태그 기반 프롬프트 격리, 런타임 PEP Guardrail 및 실패 격리(Failure Containment) 중심 방어 체계 구축 필수.
