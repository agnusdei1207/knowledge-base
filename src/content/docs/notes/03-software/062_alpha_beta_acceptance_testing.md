---
sidebar:
  order: 62
  label: "062. 알파•베타•인수 테스트 (Alpha Beta Acceptance Testing)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "알파•베타•인수 테스트 (Alpha Beta Acceptance Testing)"
date: "2026-08-10T23:40:00+09:00"
tags:
  - "notes-software"
weight: 62
extra:
  question_no: "062"
  source_status: "기출"
  source_history: "129회"
  priority: 50
  priority_note: "129회 기출, 사용자 검증 단계 비교"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Acceptance Testing (인수 테스트)**: 개발이 완료된 소프트웨어가 발주자/사용자의 요구사항(SRS) 및 사업 계약 기준을 최종 충족하는지 검증하고 시스템 인수 여부를 판정하는 최상위 테스트 단계.
- **Alpha Testing (알파 테스트)**: 릴리스 전 개발 조직 내부 통제 환경(Lab)에서 개발자와 내부 사용자가 상주하며 진행하는 첫 번째 수용 검증.
- **Beta Testing (베타 테스트)**: 알파 테스트를 통과한 소프트웨어를 실제 실운영 환경(Field)에서 불특정 다수의 외부 표본 사용자들에게 오픈하여 필드 적합성을 검증하는 단계.

</details>

- 정의/개념: 소프트웨어의 최종 릴리스 및 수용 승인을 목표로 내부 통제 환경 검증(Alpha) 대 외부 실환경 필드 검증(Beta) 대 계약 기준 판정(Acceptance)을 수행하는 사용자 검증 체계인 **Alpha / Beta / Acceptance Testing**
- 배경/필요성: 연구소 내부 개발 환경과 실운영 타깃 환경 간의 파이프라인 격차 소멸, 실제 사용자의 미처 예측하지 못한 패턴 결함 조기 발견 요구성

#### 한줄 요약

- 내부•현장 사용자 검증 증거에 기반한 인수 테스트가 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Controlled vs Uncontrolled Environment**: 알파 테스트는 개발자의 개입이 가능한 통제된 개발사 내부 환경, 베타 테스트는 외부 사용자의 실제 장치/네트워크 통제 불가능한 오픈 환경.
- **UAT (User Acceptance Testing)**: 발주사 현업 담당자들이 수용 기준(Acceptance Criteria) 시나리오에 의거하여 시스템을 직접 테스트하는 유저 인수 테스트.

</details>

- 개발사 내부 통제 환경 검증 (**Alpha Testing**)
- 불특정 실사용자 파편화(OS, Device) 환경 검증 (**Beta Testing**)
- 수용 기준(**Acceptance Criteria**) 기반의 계약적/사업적 수용 결정 (**Acceptance Testing**)

#### 한줄 요약

- 알파 테스트, 베타, 인수 기준에 따른 검증 목적 구분이 핵심이다.

## Ⅲ. 구조 및 구성요소 (사용자 검증 3대 스펙트럼)

<details><summary>핵심 용어</summary>

- **Acceptance Criteria (수용 기준)**: 프로젝트 계약서나 User Story에 정의된 완료 정의(Definition of Done)의 정량적 평가 판정 기준.

</details>

```text
[개발 완료 시스템] ──► [1. Alpha Test (통제 Lab 환경)]
                              │
                              ▼ (내부 결함 제거 완료)
                       [2. Beta Test (외부 Field 환경)]
                              │
                              ▼ (필드 피드백 보환)
                       [3. Acceptance Test (UAT 수용 판정)] ──► [최종 인수 & 운영 전환]
```

선의 의미: Alpha Test(내부 Lab) $\rightarrow$ Beta Test(외부 Field) $\rightarrow$ Acceptance Test(계약 UAT)를 거쳐 운영 시스템으로 릴리스 전환되는 3단계 검증 아키텍처.

| 검증 단계 명칭 | 주 수행 장소 및 대상 | 주요 목적 및 발견 결함 유형 |
|:---|:---|:---|
| **Alpha Testing (알파)** | 개발사 내부 통제 환경 (Lab), 개발자 + 내부 사용자 | 시스템 치명적 crash 결함 조기 발견 및 인터페이스 오류 정제 |
| **Beta Testing (베타)** | 불특정 외부 사용자의 실제 환경 (Field) | 다양한 OS/장치 파편화 현장 적합성 및 사용성(UX) 결함 수거 |
| **Acceptance Testing (인수)**| 발주사 지정 인수 환경, 최종 발주자/고객사 | 계약서 및 **Acceptance Criteria** 준수 여부 정량 판정 |

#### 한줄 요약

- 테스트 근거, 증거 저장소, 승인권자의 수용 판정 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Operational Acceptance Testing (OAT)**: 기능 수용(UAT) 외에 백업/복구, 보안, 재해복구(DR), 성능 등 운영팀 관점의 시스템 유지보수 가능성을 검증하는 운영 인수 테스트.

</details>

```text
┌──────────────────────────────┐
│ 시스템 개발 & 시스템 테스트  │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. Alpha Test (내부 Lab)     │
│ 2. Beta Test (외부 Field)    │
│ 3. UAT (기능 인수 테스트)    │
│ 4. OAT (운영 인수 테스트)    │
│ 5. Sign-off (최종 인수 승인) │
└──────────────┬───────────────┘
               ▼
     [상용 릴리스 / 대금 지급]
```

### 동작 원리

1. **Alpha Test Execution**: 개발사 내부 랩에서 내부 테스터들이 시나리오 기반 테스트 후 치명적 결함 조기 수정.
2. **Beta Test Rollout**: 오픈 베타/클로즈 베타 형태로 외부 유저 1,000명에게 바이너리 배포 및 텔레메트리 피드백 수거.
3. **UAT (User Acceptance)**: 발주사 현업이 계약 시나리오 전 시점 통과 검증.
4. **OAT (Operational Acceptance)**: 운영팀이 백업/복구, 장애 Failover, 보안 모니터링 수용 가능성 체크.
5. **Sign-off**: 최종 **Acceptance Criteria** 통과 판정서 서명 및 시스템 승인.

#### 한줄 요약

- 인수 기준•테스트 근거 확정부터 기준별 테스트 증거 판정까지의 수용 결정 흐름이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Contractual vs Regulatory Acceptance**: 계약서 명세를 검증하는 계약 인수(Contractual) 대 정부 보안/법률 규제 준수 여부를 검증하는 규정 인수(Regulatory).

</details>

| 비교 항목 | Alpha Testing (알파) | Beta Testing (베타) | Acceptance Testing (인수/UAT) |
|:---|:---|:---|:---|
| 테스트 장소 | **개발자 조직 내부 (Lab)** | **외부 사용자 실제 환경 (Field)** | **발주사/고객사 환경** |
| 테스트 주체 | 개발자 + 내부 사용자 | 불특정 다수 외부 유저 | **발주사 현업 담당자 / 검수관** |
| 환경 통제성 | **100% 통제 가능** | **통제 불가능 (Uncontrolled)** | **통제된 고객사 환경** |
| 주요 목표 | 내부 인터페이스 및 라인 결함 조기 수습 | 실환경 파편화 및 UX 피드백 확보 | **사업 계약 수용 승인 (Sign-off)** |

#### 한줄 요약

- 알파는 결함 재현, 베타는 현장 적합성 확인, UAT는 업무 수용 판정이 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Beta Fatigue**: 베타 테스터들이 불성실하게 피드백을 내거나 유휴 상태로 방치되는 현상으로, 적절한 리워드 및 피드백 수집 텔레메트리 자동화 필수.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 알파 테스트 시 개발자 편향으로 결함 은폐 | 내부 전담 독립 QA 조직 구축 및 블랙박스 기반 테스트 | 결함 객관성 확보 |
| 베타 테스터들의 피드백 수집률 저하 (**Beta Fatigue**) | **Crashlytics / Sentry 크래시 텔레메트리 SDK** 자동 수집 | 자동 피드백 수거 |
| UAT 수용 기준이 모호하여 최종 인수 거부 파행 | 프로젝트 초기 **Acceptance Criteria (완료 정의)** 구체적 명시 | 최종 분쟁 차단 |

> 사례: 모바일 게임 릴리스 시 **내부 Alpha $\rightarrow$ Google Play Store Closed Beta $\rightarrow$ UAT Sign-off** 체계

#### 한줄 요약

- 대표 사용자, 진단 정보, 잔여 위험, 위험 책임자를 함께 관리하는 것이 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **인수 검증 수립 기준(Acceptance Testing Standards)**: 시스템 도메인 특성(B2C vs B2B), 계약 조건 및 릴리스 타깃에 의거한 체계.

</details>

- **인수 검증 수립 기준**에 따라 B2C 서비스 시 **Alpha $\rightarrow$ Beta Test**, B2B 엔터프라이즈 구축 시 **UAT / OAT Sign-off** 필수 인가

#### 한줄 요약

- 목적에 맞는 사용자 검증 방식 선택 기준과 증거 기반 수용 판정이 핵심이다.
