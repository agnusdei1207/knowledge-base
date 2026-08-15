---
sidebar:
  order: 30
  label: "030. 소프트웨어 개발 생명주기 SDLC (Software Development Lifecycle)"
  badge:
    text: "미출제 • 50%"
    variant: note
title: "소프트웨어 개발 생명주기 SDLC (Software Development Lifecycle)"
date: "2026-08-13T14:15:00+09:00"
tags:
  - "notes-software"
weight: 30
extra:
  question_no: "030"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "개발 관리 기본, 방법론•DevOps 연결"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **SDLC (Software Development Lifecycle)**: 소프트웨어의 요구사항 정의부터 설계, 구현, 테스트, 배포, 유지보수 및 폐기(Deprecation)까지의 전 과정을 체계화한 품질 통제 개발 수명주기 프레임워크.
- **Traceability (추적성)**: 요구사항 명세서(SRS)부터 설계(Architecture), 소스코드, 테스트 케이스(Test Matrix)까지 양방향(Bidirectional)으로 매핑하여 요구 충족을 입증하는 연결성.
- **Stage Gate (단계별 게이트 검토)**: 각 개발 단계 완료 시 다음 단계 진입 여부를 검증하고 산출물(Artifact)의 품질 합격을 판정하는 품질 관문.

</details>

- 정의/개념: 소프트웨어 제품의 요구사항 수립부터 폐기까지 전 과정을 구조화하여 일정, 비용, 품질 무결성을 체계적으로 통제하는 프레임워크인 **SDLC (Software Development Lifecycle)**
- 배경/필요성: 단계 기준선 부재는 **누락•재작업•승인 책임 불명확** 유발

#### 한줄 요약

- SDLC는 요구부터 운영•폐기까지 산출물과 승인을 통제한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Artifact (산출물)**: 요구사항 정의서, 유스케이스 명세서, ERD, 아키텍처 정의서, 테스트 결과서 등 각 단계별로 산출되는 공식 문서/코드 결과물.
- **Feedback Loop**: 이전 단계의 오류나 신규 요구사항 변경을 상위 단계로 되돌려 반영(Iteration)하는 피드백 순환 구조.

</details>

- 단계별 **Artifact** 산출 및 **Stage Gate**를 통한 진입/종료 조건 통제
- 요구사항-설계-코드-테스트 간 **Traceability (양방향 추적성)** 보장
- 개발 모델(Waterfall, Agile, DevOps) 수용성 및 런타임 **Feedback Loop** 상주

#### 한줄 요약

- 단계 게이트, 추적성, 피드백 루프의 결합이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SDLC Models**: Waterfall(폭포수), Prototyping(시작품), Spiral(나선형), Agile(애자일), DevOps 등 사업 성격에 따라 선택하는 생명주기 방법론 모형.

</details>

```text
                         [생명주기 모델]
                                |
[산출물•추적성 저장소] -- [단계 게이트] -- [수행 활동]
```

선의 의미: SDLC 모델에 의거하여 각 단계별 수행 활동이 진행되고, Stage Gate 검토를 통과한 산출물과 추적성이 저장소에 보존되는 체계적인 구조.

| 구성요소 | 책임 |
|:---|:---|
| 생명주기 모델 | 사업 특성에 맞는 단계•반복 구조 정의 |
| 수행 활동 | 요구•설계•구현•검증•운영•폐기 수행 |
| 단계 게이트 | 진입•종료 기준과 **승인 여부** 판정 |
| 산출물•추적성 저장소 | 요구부터 테스트까지 **양방향 추적** 보존 |

#### 한줄 요약

- 생명주기 모델과 승인 증적 저장소가 단계 통제를 지원한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **V-Model**: 요구사항-수용테스트, 구조설계-시스템테스트, 상세설계-통합테스트, 코딩-단위테스트를 1:1 대칭 매핑하여 검증을 강조하는 V자형 SDLC 모형.

</details>

```text
┌──────────────────────────────┐
│ 1. 요구•추적 기준선 설정   │
│ 2. 설계•구현 수행          │
│ 3. 검증•증적 생성          │
│ 4. 단계 게이트 판정        │
└───────┬──────────────────────┘
        ├─ 미충족 ─▶ [재작업 범위 (Rework)]
        │ 충족
        ▼
┌──────────────────────────────┐
│ 5. 운영 피드백•폐기 판정   │
└──────────────────────────────┘
```

### 동작 원리

1. **요구·추적 기준선 설정**: SRS 정의 및 Traceability Matrix 기반 ID 체계 정립.
2. **설계·구현 수행**: 요구사항 ID 매핑 기반 아키텍처 설계 및 구현 연산.
3. **검증·증적 생성**: 단위/통합/시스템 테스트 및 **V-Model** 대칭 검증 수행.
4. **단계 게이트 판정**: 산출물 결함율 및 기준 충족 검증 (미충족 시 Rework 회귀).
5. **운영 피드백·폐기 판정**: 배포 후 런타임 Telemetry 피드백 및 생명주기 완결 시 안전 폐기.

#### 한줄 요약

- 요구•추적 기준선 설정부터 운영 피드백•폐기 판정까지 순환한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Waterfall Model**: 각 단계를 순차적으로 명확히 완결짓고 넘어가며, 변동이 적은 명확한 사업에 적합한 모델.
- **Agile / DevOps**: 짧은 이터레이션(Sprint) 단위로 빠르게 배포하고 연속 피드백(CI/CD)을 반영하는 가변형 SDLC 모델.

</details>

| 비교 항목 | Waterfall Model (전통적) | Spiral Model (나선형) | Agile / DevOps (현대적) |
|:---|:---|:---|:---|
| 중심 철학 | 순차적 완전 통제 및 산출물 정립 | 위험 분석(Risk Analysis) 및 반복 | **고객 가치 빠른 전달 및 연속 피드백** |
| 위험 관리 | 후반부 통합 시점 위험 도출 | **매 단계 위험 분석 활동 포함** | 짧은 이터레이션(Sprint)으로 조기 해소 |
| 변경 수용성 | 매우 낮음 (변경 시 재작업 큼) | 중간 (반복 단계별 반영) | **매우 높음 (수시 백로그 재우선순위화)** |
| 적합한 프로젝트 | 정부 공공사업, 금융 차세대, 방산 | 대규모 고위험 연구개발(R&D) 프로젝트 | SaaS, 모바일 앱, Cloud-Native 웹 |

#### 한줄 요약

- 감사 중심은 단계 게이트, 변화 중심은 DevOps와 자동화 파이프라인이 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Shift-Left Testing**: 보안 및 품질 검증(SAST, Unit Test)을 SDLC 후반부에서 구현/설계 극초반부(Left)로 전진 배치하여 결함 수정 비용을 획기적으로 낮추는 전원배치 전략.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 후반부 검증 시 결함 발견으로 인한 재작업 비용 폭증 | **Shift-Left Testing / Shift-Left Security** 전략 인가 | 결함 조기 발굴 및 수정 비용 감소 |
| 수작업 단계 게이트 검토에 따른 리드 타임 지연 | **CI/CD 파이프라인 연동 자동화 게이트** (SonarQube 품질지표) | 연속 배포 속도 향상 |
| 요구사항 변경 시 영향도 파악 불가 | **Traceability Matrix (양방향 추적표)** 자동화 유지 | 변경 영향 범위 명확화 |

> 사례: ISO/IEC/IEEE 12207 표준 SDLC 기반 엔터프라이즈 DevSecOps 파이프라인 정착

#### 한줄 요약

- 변경 영향, 감사 증적, 개선 백로그를 연결한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **SDLC 프레임워크 수립 기준(SDLC Framework Adoption Criteria)**: 규제 준성(Compliance), 프로젝트 위험도, 요구사항 변동성과 배포 주기에 기반한 선정 체계.

</details>

- **SDLC 프레임워크 수립 기준**에 따라 공정 관리 중심 사업은 **Waterfall/V-Model**, 고속 요구 변화 사업은 **Agile/DevOps SDLC** 채택

#### 한줄 요약

- 감사 강도와 변화 속도를 함께 평가하는 것이 핵심이다.
