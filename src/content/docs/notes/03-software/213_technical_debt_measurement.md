---
sidebar:
  order: 213
  label: "213. 기술부채 측정•관리 (Technical Debt Measurement)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "기술부채 측정•관리 (Technical Debt Measurement)"
date: "2026-08-14T06:30:00+09:00"
tags: ["notes-software"]
weight: 213
extra:
  question_no: "213"
  source_status: "기출"
  source_history: "123회"
  priority: 50
  priority_note: "부채 식별•우선순위•상환 관리가 반복 출제됨"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Technical Debt (기술부채)**: 빠른 납기 등의 타협이 미래 변경 비용과 위험을 높이는 현상
- **Principal•Interest (원금•이자)**: 개선 일회성 비용과 방치 중 반복되는 손실

</details>

- 정의/개념: 기술부채의 원금•이자•위험으로 상환 순위를 정하는 **관리 체계**
- 배경/필요성: 비가시적 구조 결함은 **예산 근거•상환 우선순위** 제시 곤란

#### 한줄 요약

- 개선 비용과 방치 손실을 수치화해 **상환 투자** 결정

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Remediation (상환)**: Refactoring•재설계•Upgrade로 부채 원인을 제거하는 활동

</details>

- **원금 측정**: 정상 구조로 개선할 일회성 공수 산정
- **이자 측정**: 반복 변경 지연•Debug•장애 손실 산정
- **위험 결합**: 발생 가능성과 Business Impact로 순위 보정
- **재발 통제**: Quality Gate와 효과 측정으로 신규 부채 차단

#### 한줄 요약

- 쉬운 부채보다 **이자•업무 위험**이 큰 부채를 먼저 상환

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Debt Register (부채 등록부)**: 부채 원인•영향•Owner•비용•상태를 관리하는 장부

</details>

```text
[Technical Debt 관리]
 ├── [Debt Register | 항목•Owner•상태]
 ├── [Cost Meter | 원금•이자]
 ├── [Risk Assessor | 확률•영향]
 ├── [Remediation Plan | 일정•예산•의존성]
 └── [Quality Gate | 신규 부채 차단]
```

| 구성요소 | 책임 |
|---|---|
| Debt Register | 원인•영향•Owner•**상환 상태** 관리 |
| Cost Meter | 개선 원금과 반복 **생산성 손실** 측정 |
| Risk Assessor | 발생 확률×Business Impact **점수화** |
| Remediation Plan | 우선 부채를 **정규 Backlog**에 배치 |
| Quality Gate | 임계치 위반 Code의 **신규 유입** 차단 |

#### 한줄 요약

- 부채를 등록•평가•상환하고 Gate로 **재발 방지**

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Risk Acceptance (위험 수용)**: 상환 비용보다 잔여 위험이 낮을 때 감시하며 보유하는 결정

</details>

```text
[Code•운영 근거 입력]
          │
          ▼
[1. 부채 항목•근거 등록]
          │
          ▼
[2. 원금•이자•위험 평가]
          │
          ▼
[3. 위험 기반 상환 순위 결정]
          │
          ▼
[4. 상환 실행•신규 유입 차단]
          │
          ▼
[5. 효과•재발 기록]
          │
          ▼
[상환 성과 반환]
```

### 동작 원리

1. **부채 항목•근거 등록**: 분석•Review•사고 근거로 Ticket 생성
2. **원금•이자•위험 평가**: 공수•반복 손실•업무 영향을 산정
3. **위험 기반 상환 순위 결정**: 이자와 파급력이 큰 항목 우선
4. **상환 실행•신규 유입 차단**: Backlog 수행과 Gate 강화
5. **효과•재발 기록**: Lead Time•장애 감소와 재발 여부 측정

#### 한줄 요약

- 근거 등록부터 성과 측정까지 **위험 기반 상환** 수행

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Architecture Debt**: 잘못된 경계•의존성으로 변경 영향이 전체로 확산되는 부채

</details>

| 비교 항목 | Code Debt | Architecture Debt | Platform Debt |
|---|---|---|---|
| 대상 | 함수•Class•중복 | Service 경계•의존성 | OS•Framework•Library |
| 영향 | 국소 변경 지연 | **연쇄 변경•장애** | **EOL•보안 노출** |
| 상환 | Refactoring | 경계 재설계•분리 | Upgrade•Migration |

#### 한줄 요약

- Code•Architecture•Platform별 **원인과 상환 방식** 구분

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Metric Gaming (지표 게임화)**: 실제 품질보다 측정 점수만 높이는 편법 행동

</details>

| 고려사항 | 대책 |
|---|---|
| 정적 분석 점수 맹신 | APM•Git Hotspot•**사고 Log** 결합 |
| 원금만으로 순위 결정 | 이자•발생 빈도•**업무 영향** 결합 |
| 폐기 예정 Legacy 상환 | Migration Roadmap과 **TCO** 대조 |
| Metric Gaming | 장기 추세와 Senior **Sample Review** 병행 |

#### 한줄 요약

- Tool 점수보다 활성 Code의 **변경 이자•운영 위험**을 측정

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- 고치기 쉬운 Code보다 자주 바뀌고 장애 피해가 큰 핵심 Code부터 개선한다.

</details>

- 변경 이자•장애 위험이 큰 **활성 부채**부터 정규 Backlog로 상환
