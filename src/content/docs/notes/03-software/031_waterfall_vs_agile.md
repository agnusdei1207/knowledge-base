---
sidebar:
  order: 31
  label: "031. 폭포수 모델 vs 애자일 (Waterfall vs Agile)"
  badge:
    text: "미출제 • 30%"
    variant: note
title: "폭포수 모델 vs 애자일 (Waterfall vs Agile)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 31
extra:
  question_no: "031"
  source_status: "미출"
  source_history: ""
  priority: 30
  priority_note: "미출제, 개발 생명주기 비교 기초"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Waterfall Model (폭포수 모델)**: 각 개발 단계(요구-설계-구현-테스트-배포)를 순차적으로 완전 완결 짓고 다음 단계로 넘어가며 산출물 검증을 강조하는 선형 순차적(Sequential) SDLC 모형.
- **Agile Methodology (애자일 방법론)**: 변화에 대한 신속 대응을 최우선으로, 1~4주 단위의 짧은 피드백 반복(Sprint/Iteration)을 통해 작동하는 소프트웨어(Working Software)를 조기 배포하는 개발 철학.

</details>

- 정의/개념: 요구사항의 정적 고정성 및 프로세스 산출물 통제 위주의 **Waterfall Model** 대 변경의 수용성 및 빠른 가치 전달 위주의 **Agile Methodology**
- 배경/필요성: 프로젝트 초기 요구 불확실성(Uncertainty) 수용 및 고객 피드백 기반 조기 가치 창출(Time-to-Market) 요구성

#### 한줄 요약

- 폭포수 모델과 애자일은 요구 안정성과 피드백 빈도에 따라 선택한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Product Increment (제품 증분)**: 각 스프린트/이터레이션이 완료되었을 때 배포 가능한 상태로 완성되는 기능들의 합.
- **Scope Creep**: 폭포수 프로젝트 진행 중 통제되지 않은 요구사항 변경이 지속 추가되어 일정과 비용이 폭발하는 현상.

</details>

- 요구사항 사전 정적 동결(Requirements Freeze) 및 **Stage Gate** 산출물 검증 (**Waterfall**)
- 고객 피드백 기반 **Product Increment** 단위 지속 배포 및 수시 백로그 재정렬 (**Agile**)
- 일정/비용 고정 후 범위 가변 (**Agile**) vs 범위 고정 후 일정/비용 산정 (**Waterfall**)

#### 한줄 요약

- 폭포수는 단계 승인, 애자일은 증분 피드백 중심이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Product Backlog**: 애자일에서 구현해야 할 모든 요구사항, 기능 개선, 결함들을 우선순위(Priority) 순으로 정렬한 단일 관리 목록.

</details>

```text
[요구 기준선] -- [단계 승인]

[제품 백로그] -- [제품 증분]
```

선의 의미: 폭포수는 정적 요구 기준선 기반 단계 승인을 거치고, 애자일은 제품 백로그를 통해 스프린트 단위 제품 증분을 도출하는 구조.

| 구분 항목 | Waterfall Model (폭포수) | Agile Methodology (애자일) |
|:---|:---|:---|
| 핵심 관리 축 | **프로세스, 산출물(Document), 단계 통제** | **고객 협업, 작동하는 SW, 변화 대응** |
| 요구사항 변경 | 거부 및 엄격한 변경 통제 절차(CCB) 수용 | **수시 수용 (Product Backlog 재우선순위화)** |
| 개발 단위 | 전 프로젝트 1회 통통합 딜리버리 | **1~4주 단위의 짧은 Sprint/Iteration** |
| 테스트 시점 | 구현 완료 후 후반부 통합 테스트 | **매 이터레이션 내부 단위/통합 테스트 자동화** |
| 위험 관리 | 후반부 폭발적 위험 발견 (Late Risk) | **초기 스프린트 조기 위험 해소 (Early Risk)** |

#### 한줄 요약

- 요구 기준선•단계 승인과 제품 백로그•제품 증분 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Rework Cascade**: 폭포수 모델 통합 테스트 시점에서 발견된 요구사항 오류로 인해 요구-설계-코딩 전 과정을 대대적으로 재작업(Rework)하는 악순환.

</details>

```text
폭포수 흐름

[요구 기준선] ──► [설계•구현] ──► [검증 산출물] ──► [단계 승인] ──► [후반부 릴리스] (오류 시 Rework)

애자일 흐름

[제품 백로그] ──► [스프린트 선택] ──► [증분 구현•검증] ──► [고객 피드백] ──► [백로그 재정렬]
```

### 동작 원리

1. **Waterfall 동작**: 요구사항 동결 $\to$ 시스템 설계 $\to$ 모듈 구현 $\to$ 후반부 통합 검증 $\to$ 최종 릴리스 (**Rework Cascade** 주의).
2. **Agile 동작**: Product Backlog 정렬 $\to$ Sprint Planning (전반 2주 범위) $\to$ Daily Standup/구현 $\to$ Sprint Review (고객 피드백 수용) $\to$ Retrospective 완결.

#### 한줄 요약

- 폭포수는 재작업 경로, 애자일은 백로그 재정렬로 피드백을 반영한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Hybrid Agile (하이브리드 애자일)**: 상위 계약 및 아키텍처 수립은 Waterfall 방식을 취하고, 세부 모듈 구현 및 테스트는 Agile 방식을 혼용하는 기법.

</details>

| 프로젝트 상황 | 추천 모델 | 이유 |
|:---|:---|:---|
| 요구사항이 명확하고 법적/규제 산출물 엄격 | **Waterfall Model** | 단계별 서명 승인 및 Traceability 증적 필수 |
| 요구사항 변화가 무쌍하고 조기 시장 출시 핵심 | **Agile (Scrum / Kanban)** | 매주 동작하는 SW 배포 및 가치 검증 |
| 대규모 시스템 개편 중 일부 신규 서비스 도출 | **Hybrid Model** | 엔터프라이즈 코어 안정성 + 신규 서비스 민첩성 결합 |

#### 한줄 요약

- 안정 요구는 폭포수, 잦은 변경은 애자일이 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Definition of Done (DoD)**: 애자일 팀에서 특정 스토리가 완료되었는지 판정하기 위해 수립한 공통 품질 기준 (코딩, 단위테스트, 문서, CI Pass 등).

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Waterfall 프로젝트 통합 단계에서의 무더기 결함 발굴 | **V-Model 및 Early Prototyping** 인가 | 결함 발견 시점 전진 배치 |
| Agile 적용 시 문서화 및 품질 통제 부재 오해 | **Definition of Done (DoD)** 기준 강화 | 스프린트 배포 안정성 확보 |
| 발주자-수주자 간 정가 계약(Fixed-price Contract) 구조 갈등 | **Target-cost / Flexible Scope 계약** 파트너십 변경 | 애자일 스프린트 변경 수용성 증대 |

> 사례: 공정 감사가 엄격한 금융 차세대 프로젝트의 **Hybrid Waterfall-Agile** 적용

#### 한줄 요약

- 폭포수는 조기 검증, 애자일은 완료 정의 강화가 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **개발 방법론 선택 기준(Methodology Selection Criteria)**: 요구 불확실성, 발주자 참여도, 품질 규제 및 Time-to-Market 속도에 기반한 수립 체계.

</details>

- **개발 방법론 선택 기준**에 따라 정적 공공 사업은 **Waterfall**, 가변 SaaS 벤처 사업은 **Agile (Scrum)** 채택

#### 한줄 요약

- 요구 변화와 승인 방식을 함께 평가하는 것이 핵심이다.
