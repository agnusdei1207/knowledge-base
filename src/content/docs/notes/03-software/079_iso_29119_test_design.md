---
sidebar:
  order: 79
  label: "079. ISO 29119 테스트 설계 (ISO 29119 Test Design)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "ISO 29119 테스트 설계 (ISO 29119 Test Design)"
date: "2026-08-13T18:08:00+09:00"
tags:
  - "notes-software"
weight: 79
extra:
  question_no: "079"
  source_status: "기출"
  source_history: "128회"
  priority: 30
  priority_note: "128회 기출, 테스트 설계기법 표준화 주제"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **ISO/IEC/IEEE 29119**: 파편화되어 있던 기존 소프트웨어 테스트 관련 국제 표준들(IEEE 829, IEEE 1008, BS 7925 등)을 하나로 통합 개편하여, 테스트 개념, 프로세스, 서식 및 기법을 국제적으로 규정한 표준 시리즈.
- **Part 4: Test Techniques (ISO 29119-4)**: 동적/정적 테스트 설계 기법(블랙박스, 화이트박스, 경험기반 기법 등) 및 커버리지 측정식을 상세 명시한 Part.
- **Test Design Process**: 테스트 베이시스 분석 $\rightarrow$ 테스트 조건 도출 $\rightarrow$ 테스트 케이스 설계 $\rightarrow$ 테스트 집합/절차(Procedure) 생성의 4단계 국제 표준 절차.

</details>

- 정의/개념: 소프트웨어 테스트 공정을 체계화하기 위해 ISO/IEC/IEEE가 공동 개발한 국제 표준 체계로, 테스트 프로세스(Part 2), 문서화 서식(Part 3), 및 테스트 설계 기법(Part 4)을 규정한 **ISO/IEC/IEEE 29119**
- 배경/필요성: 시험 용어•절차 파편화는 **증거 비교•요구 추적** 제한

#### 한줄 요약

- 국제표준화기구, 국제전기기술위원회, 전기전자공학자협회가 공동 제시한 표준 테스트 설계가 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Risk-Based Testing (RBT, 위험 기반 테스트)**: ISO 29119의 기본 아키텍처 사상으로, 시스템 위험도에 따라 테스트 우선순위 및 테스트 설계를 차등 배정하는 방식.
- **Standard Part Structure (5개 파트 구성)**: Part 1(개념/용어), Part 2(프로세스), Part 3(문서 양식), Part 4(설계 기법), Part 5(기능 기반 테스트).

</details>

- **Risk-Based Testing (RBT)** 사상 반영
- 국제 통용 표준 프로세스(**Part 2**) 및 설계 기법(**Part 4**) 제공
- 요구사항(SRS) $\rightarrow$ 테스트 조건(Condition) $\rightarrow$ 테스트 케이스(Case) $\rightarrow$ 절차(Procedure) 간 **양방향 추적성**

#### 한줄 요약

- 위험 수준과 네 추적 관계에 기반한 양방향 추적이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Specification-based vs Structure-based vs Experience-based**: 명세 기반(블랙박스: 동등분할, 경계값), 구조 기반(화이트박스: 구문, 분기, MC/DC), 경험 기반(탐색적 테스트, 오류 추정).

</details>

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                    ISO/IEC/IEEE 29119-4 Test Techniques                 │
├─────────────────────────┬─────────────────────────┬─────────────────────┤
│ Specification-based     │ Structure-based         │ Experience-based    │
│ (명세 기반 / 블랙박스)  │ (구조 기반 / 화이트박스)│ (경험 기반)         │
├─────────────────────────┼─────────────────────────┼─────────────────────┤
│ • 동등 분할             │ • 구문 커버리지 ($C_0$) │ • 오류 추정기법     │
│ • 경계값 분석           │ • 분기 커버리지 ($C_1$) │ (Error Guessing)    │
│ • 의사결정 테이블       │ • 조건 커버리지 ($C_2$) │ • 탐색적 테스트     │
│ • 상태 전이 테스트      │ • MC/DC Coverage        │ (Exploratory Test)  │
│ • 유스케이스 테스트     │ • 데이터 흐름 검증     │ • 체크리스트 기반   │
└─────────────────────────┴─────────────────────────┴─────────────────────┘
```

선의 의미: ISO 29119-4가 명세 기반, 구조 기반, 경험 기반 3대 영역으로 소프트웨어 테스트 설계 기법을 정형화 분류하는 체계.

| 분류 (Category) | 주요 설계 기법 (Test Techniques) | 대표적인 적용 레벨 및 성격 |
|:---|:---|:---|
| **Specification-based**<br/>(명세 기반 기법) | **Equivalence Partitioning, Boundary Value Analysis, Decision Table, State Transition** | 요구사항 명세서(SRS) 기반, 시스템/인수 테스트 수준 적용 |
| **Structure-based**<br/>(구조 기반 기법) | **Statement, Branch, Condition, MC/DC Coverage, Data Flow Testing** | 소스코드 구조 기반, 개발자 단위/통합 테스트 수준 적용 |
| **Experience-based**<br/>(경험 기반 기법) | **Error Guessing, Exploratory Testing, Checklist-based Testing** | 테스터의 도메인 직관 및 경험 기반, 보완적 적용 |

#### 한줄 요약

- 테스트 베이시스, 테스트 조건, 테스트 케이스, 테스트 절차의 설계 계층이 핵심이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Test Condition & Test Procedure**: Test Condition은 '무엇을 테스트할 것인가', Test Case는 '입력값과 기대출력값', Test Procedure는 '실행 순서(Script)'.

</details>

```text
[1. 테스트 베이시스 분석] ──► [2. 테스트 조건 도출] ──► [3. 테스트 케이스 설계] ──► [4. 테스트 절차 생성]
  (요구사항/SRS 수거)      (테스트 조건 식별)            (입력값/기대출력 정의)    (테스트 스크립트화)
```

### 동작 원리

1. **테스트 베이시스 분석**: 요구•설계•위험에서 시험 근거 수집.
2. **테스트 조건 도출**: 기능•품질별 확인할 조건 식별.
3. **테스트 케이스 설계**: 기법을 적용해 입력•기대 결과 정의.
4. **테스트 절차 생성**: 케이스를 실행 순서와 환경으로 구성.

#### 한줄 요약

- 테스트 베이시스 분석부터 커버리지 공백•잔여 위험 평가까지의 추적이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **IEEE 829 vs ISO 29119**: IEEE 829는 주로 테스트 문서 양식(Test Documentation)에 치중한 반면, ISO 29119는 프로세스, 서식, 설계 기법, 키워드 동적 테스트까지 포괄 통합.

</details>

| 비교 항목 | 기존 IEEE 829 표준 | ISO/IEC/IEEE 29119 통합 표준 |
|:---|:---|:---|
| 표준 적용 범위 | 단순 테스트 문서화 서식 위주 (Documentation) | **개념, 프로세스, 문서 서식, 설계 기법 종합 통합** |
| 위험 수용성 | 리스크 개념 반영 저조 | **Risk-Based Testing (RBT) 위험 기반 프로세스 전면 채택**|
| 애자일/DevOps 수용성| 전통적 폭포수 모형 위주 | **Agile, DevOps 및 연속적 테스트(Continuous Testing) 수용**|
| 국제적 통용성 | IEEE 중심의 단일 기관 표준 | **ISO / IEC / IEEE 3개 세계 최대 표준 기관 공인** |

#### 한줄 요약

- 빠른 탐색은 비형식, 반복•감사는 표준 설계가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Test Traceability Matrix (TTM)**: 요구사항 ID $\rightarrow$ Test Condition $\rightarrow$ Test Case $\rightarrow$ Execution Result 간의 추적성 테이블.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 지나치게 엄격한 ISO 29119 문진 작성으로 문서화 비용 폭증 | **프로젝트 규모/위험도에 따른 표준 프로세스 재단 (Tailoring)** | 소요 비용 최적화 |
| 요구사항 변경 시 테스트 케이스 추적 파열 | **Test Traceability Matrix (TTM) 및 Jira/Xray 자동 연동** | 양방향 추적성 확보 |
| 테스터별 가중치/커버리지 해석 오차 | **Part 4 내 규정된 정량적 커버리지 산식 공식 적용** | 객관적 측정치 인가 |

> 사례: **국방/항공/금융 IT 프로젝트 내 ISO 29119 기반 테스트 프로세스 적용 및 TTA 검증**

#### 한줄 요약

- 위험 기반 재단, 추적 링크로 영향 케이스 식별, 측정 오라클이 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **ISO 29119 수용 기준(ISO 29119 Standards)**: 시스템 중요도, Part 1~5 표준 체계 및 TTA/SW 감리 기준성에 의거한 체계.

</details>

- 반복•감사 증거는 **표준 설계**, 불확실 탐색은 **경량 재단** 적용

#### 한줄 요약

- 검증 위험과 증거 요구에 맞는 테스트 설계 수준 선택 기준이 핵심이다.
