---
sidebar:
  order: 207
  label: "207. AI 기반 테스트 자동화 (AI Test Automation)"
  badge:
    text: "미출 • 70%"
    variant: note
title: "AI 기반 테스트 자동화 (AI Test Automation)"
date: "2026-08-14T06:00:00+09:00"
tags: ["notes-software"]
weight: 207
extra:
  question_no: "207"
  source_status: "미출"
  source_history: ""
  priority: 70
  priority_note: "테스트 생성•선택•판정 통제가 최신 응용축임"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **AI Test Automation**: 요구•Code•실행 이력으로 Test 생성•선택•분석을 보조하는 기술
- **Regression Test (회귀 테스트)**: 변경이 기존 정상 기능에 결함을 만들지 않았는지 확인하는 활동

</details>

- 정의/개념: Test 생성•회귀 선택•실패 분석을 지능화하는 **자동화 기술**
- 배경/필요성: 전체 회귀 실행과 수작업 Script가 **CI/CD 병목** 유발

#### 한줄 요약

- 변경•결함 이력으로 Test를 선별하고 **Oracle**로 판정 통제

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Test Oracle (테스트 오라클)**: 실행 결과의 참•거짓을 판정하는 기대값과 규칙
- **Failure Clustering (실패 군집화)**: 유사 Log•Stack•증상을 묶어 근본 원인을 찾는 기법

</details>

- **변경 영향 선택**: 의존성과 결함 이력으로 회귀 Test 압축
- **후보 생성**: 요구•Code 문맥으로 Edge Case 초안 생성
- **Oracle 통제**: 규칙과 Human Review로 오탐•미탐 억제
- **실패 군집화**: 유사 실패를 묶어 Root Cause 분석 보조

#### 한줄 요약

- AI는 생성•선택을 보조하고 **정답 판정**은 검증된 규칙으로 통제

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Isolated Runner (격리 실행기)**: 생성 Test가 외부 시스템에 영향을 주지 않게 실행하는 환경

</details>

```text
[AI Test Automation]
 ├── [Test Generator | 후보 Script]
 ├── [Regression Selector | 변경 영향•이력]
 ├── [Oracle•Review Gate | 정답•보안•중복]
 ├── [Isolated Runner | 격리 실행]
 └── [Detection Evaluator | 변이•재현성]
```

| 구성요소 | 책임 |
|---|---|
| Test Generator | 요구•Code 기반 **Test 후보** 생성 |
| Regression Selector | 변경 영향•실패 이력으로 **실행 대상** 선별 |
| Oracle•Review Gate | 기대값•보안•중복•**업무 유효성** 검증 |
| Isolated Runner | 승인 Test를 **Sandbox**에서 실행 |
| Detection Evaluator | Mutation Score•**재현성** 평가 |

#### 한줄 요약

- 생성•선택 후보는 Gate를 거쳐 격리 실행 후 **탐지력** 평가

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Mutation Score (변이 점수)**: 인위적 Code 결함 중 Test가 탐지한 비율

</details>

```text
[요구•Code•실패 이력]
          │
          ▼
[1. 후보•변경 정보 분석]
          │
          ▼
[2. 실행 대상 제출]
          │
          ▼
[3. 승인 Test 전달]
          │
          ▼
[4. 실행 결과 전달]
          │
          ▼
┌────[5. 탐지력 Feedback]────┐
│ 미달: 시나리오 보강       │
│ 충족: 자동화 범위 확대    │
└─────────────────────────────┘
```

### 동작 원리

1. **후보•변경 정보 분석**: 요구와 변경 Code의 영향 범위 연결
2. **실행 대상 제출**: 의존성과 결함 Hotspot으로 Test 선별
3. **승인 Test 전달**: Oracle•보안•중복 Gate 통과
4. **실행 결과 전달**: 성공•실패•Flaky•Log 기록
5. **탐지력 Feedback**: 변이 검출률과 재현성으로 후보 보강

#### 한줄 요약

- 변경 후보부터 Mutation 탐지까지 **AI 품질**을 순환 검증

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Generative AI (생성형 AI)**: 요구•Code 문맥으로 새 Test 시나리오를 생성하는 모델

</details>

| 비교 항목 | Rule 기반 | ML 기반 | 생성형 AI |
|---|---|---|---|
| 목적 | 결정적 반복 실행 | Test 선택•실패 분류 | 새 Test 후보 생성 |
| 강점 | **Oracle 신뢰성** | **이력 기반 효율** | **문맥 기반 확장** |
| 한계 | 유지보수 비용 | 편향•초기 Data 필요 | 환각•악성 Code 위험 |

#### 한줄 요약

- Rule은 판정, ML은 선별, 생성형 AI는 **후보 확장** 담당

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Flaky Test (불안정 테스트)**: Code 변경 없이 환경•Timing에 따라 결과가 달라지는 Test

</details>

| 고려사항 | 대책 |
|---|---|
| AI의 Oracle 오류 | Rule과 **Human Review** 교차 검증 |
| 사내 Code 외부 노출 | 비식별화•사설 Model•**접근 통제** 적용 |
| Flaky Test 증가 | Random Seed•환경 고정과 **재현 정보** 기록 |
| Coverage 착시 | Line Coverage와 **Mutation Score** 병행 |

#### 한줄 요약

- Oracle•보안•재현성•변이 탐지로 **생성 Test 신뢰성** 확보

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- AI가 만든 Test 수보다 같은 조건에서 실제 결함을 반복 탐지하는지가 중요하다.

</details>

- Oracle•보안•**Mutation Score•재현성**을 통과한 영역부터 자동화 확대
