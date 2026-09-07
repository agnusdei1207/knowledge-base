---
sidebar:
  order: 111
  label: "111. NIST Cybersecurity Framework (NIST CSF)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "사이버보안 위험 관리 및 전사 거버넌스 프레임워크 : NIST CSF 2.0 (Govern & 6 Functions)"
date: "2026-09-07T14:00:00+09:00"
tags:
  - "notes-security"
weight: 111
extra:
  question_no: "111"
  source_status: "기출"
  source_history: "137회"
  priority: 70
  priority_note: "137회 기출, NIST CSF 2.0(Cybersecurity Framework 2.0), 6대 핵심 기능(Govern 거버넌스 신설, Identify 식별, Protect 보호, Detect 탐지, Respond 대응, Recover 복구), 3대 구조(Core 코어, Profiles 프로파일, Tiers 티어), NIST CSWP 29, SP 1301/1302"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **NIST CSF (National Institute of Standards and Technology Cybersecurity Framework / NIST CSF 2.0)**: 미국 국립표준기술연구소(NIST)가 제정한 글로벌 사이버보안 위험 관리 프레임워크로, 모든 규모와 산업군의 조직이 비즈니스 목표에 부합하도록 사이버보안 위험을 식별, 평가, 관리할 수 있도록 **6대 핵심 기능(Govern, Identify, Protect, Detect, Respond, Recover)** 을 기반으로 공통 언어와 체계를 제공하는 프레임워크.
- **기술 보안과 경영 거버넌스 간의 언어 단절 결함(Technical vs Governance Disconnect Defect)**: 엔지니어링 중심의 기술 용어(IP, CVE, 방화벽 포트 등)와 경영진의 비즈니스 리스크 언어(재무 손실, 투자 대비 효과, 공급망 지속성)가 일치하지 않아, 최고경영진이 보안 투자 우선순위를 올바르게 판단하지 못하고 거버넌스 통제력이 마비되는 구조적 결함.

</details>

- 정의/개념: **6대 기능**과 프로파일·티어로 위험을 관리하는 **NIST CSF 2.0**
- 배경/필요성: 엔지니어링 중심의 기술 보안 지표(IP, CVE, 방화벽 로그 등)와 경영진의 비즈니스 리스크 언어(재무 손실, 투자 대비 효과, 공급망 지속성) 간의 단절로 인해 최고경영진이 보안 투자 우선순위를 올바르게 판단하지 못하고, 공급망 위험(C-SCRM)과 이사회 거버넌스가 배제된 채 사후 대응적 통제에만 머무르는 한계가 존재함에 따라, NIST CSF 2.0 표준에 기반하여 최상위 거버넌스(Govern)를 포함한 6대 핵심 기능(Govern, Identify, Protect, Detect, Respond, Recover), 현재-목표 간 갭을 분석하는 조직 프로파일(Profiles), 4단계 구현 티어(Tiers) 및 타 표준(ISO 27001 등) 정보 참조를 결합하는 사이버보안 위험 관리 프레임워크를 도입하여 **경영진과 엔지니어 간의 공통 언어 확립, 공급망을 아우르는 전사적 위험 통제력 확보 및 지속 가능한 사이버 복원력(Cyber Resilience)**을 달성할 필요

#### 한줄 요약
- CSF 2.0은 Govern 기능을 포함한 6대 핵심 기능과 프로파일, 티어를 통해 전사 사이버보안 위험을 관리한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **NIST CSF 2.0의 3대 핵심 기둥**:
  - **CSF Core (코어)**: 6대 기능(Function), 22개 범주(Category), 106개 하위 범주(Subcategory)로 구성된 사이버보안 기대 결과 목록.
  - **CSF Profiles (조직 프로파일)**: 현재 상태(Current Profile)와 목표 상태(Target Profile)를 대조하여 보안 갭(Gap)을 식별하고 우선순위를 도출하는 도구.
  - **CSF Tiers (구현 티어)**: 조직의 사이버보안 위험 관리 관행의 엄격성과 정교함을 4개 등급(Tier 1 Partial ~ Tier 4 Adaptive)으로 측정하는 척도.

</details>

- 기술을 강제하지 않는 **결과 지향적 접근**으로 구현 유연성 확보
- **Govern**에서 전략·법규·공급망 위험을 전사적으로 조율
- **정보 참조**로 ISO 27001 등 구현 표준과 교차 매핑

#### 한줄 요약
- 결과 중심 6대 기능(Govern 포함), 프로파일 갭 분석, 4단계 구현 티어, 타 글로벌 표준과의 상호운용성을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **NIST CSF 2.0 6대 핵심 기능 (Functions)**:
  1. **Govern (GV, 지배)**: 사이버보안 전략, 위험 관리 정책, 이사회 리더십, 공급망 위험 관리(C-SCRM).
  2. **Identify (ID, 식별)**: 자산 관리, 비즈니스 환경 이해, 위험 평가, 개선 기회 식별.
  3. **Protect (PR, 보호)**: 신원 및 접근통제, 데이터 보안, 플랫폼 보안, 보안 교육.
  4. **Detect (DE, 탐지)**: 이상 징후 분석, 지속적 모니터링, 침해 지표(IoC) 탐지.
  5. **Respond (RS, 대응)**: 사고 대응 계획 실행, 이해관계자 소통, 침해 확산 완화 및 분석.
  6. **Recover (RC, 복구)**: 재해 복구 계획 실행, 시스템 복원, 사후 교훈(AAR)을 통한 복원력 강화.

</details>

```text
[NIST CSF 2.0]
├── [CSF Core (6대 기능)]
│   ├── Govern (지배·전략)
│   ├── Identify (자산·위험 식별)
│   ├── Protect (방어·접근통제)
│   ├── Detect (이상 징후 탐지)
│   ├── Respond (사고 대응 완화)
│   └── Recover (업무 복구·복원)
├── [Profiles (조직 프로파일)]
│   ├── 현재 상태 프로파일 (Current)
│   └── 목표 상태 프로파일 (Target)
├── [Tiers (구현 티어)]
│   └── Tier 1(부분) ~ Tier 4(적응)
└── [Informative References]
    └── ISO 27001·NIST SP 800-53 연계
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| **CSF Core** | 6대 기능의 사이버보안 기대 결과 정의 |
| **Profiles** | 현재·목표 상태를 비교해 개선 과제 도출 |
| **Tiers** | 위험 관리 관행을 4단계로 평가 |
| **정보 참조** | 하위 범주와 구현 표준을 교차 매핑 |

#### 한줄 요약
- Core는 달성할 결과만 규정하고 구현 수단은 정보 참조로 외부 표준에 넘기므로, CSF는 자체 통제 목록을 소유하는 대신 조직이 이미 쓰는 표준 위에 얹히는 상위 계층으로 놓인다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **NIST CSF 적용 5단계 실행 프로세스**:
  1. 조직 상황 및 위험 한도 설정 (Context & Risk Tolerance)
  2. 현재 상태 프로파일 작성 (Current Profile Creation)
  3. 목표 상태 프로파일 정의 (Target Profile Definition)
  4. 갭 분석 및 우선순위 위험 처리 계획 수립 (Gap Analysis & Action Plan)
  5. 보안 조치 이행 및 성숙도 티어(Tier) 모니터링 (Implementation & Tier Review)

</details>

```text
1. 조직 상황 및 위험 한도 설정
              │
              ▼
2. 현재 프로파일 작성
              │
              ▼
3. 목표 프로파일 정의
              │
              ▼
4. 갭 분석 및 실행 계획 수립
              │
              ▼
5. 조치 이행 및 티어 검토
```

**동작 원리**

1. **조직 상황 및 위험 한도 설정**: 경영 목표와 위험 허용 수준 승인
2. **현재 프로파일 작성**: 증적에 따라 하위 범주별 현재 상태 기록
3. **목표 프로파일 정의**: 법규와 위험도에 맞춘 목표 상태 결정
4. **갭 분석 및 실행 계획 수립**: 격차별 우선순위·예산·일정 배정
5. **조치 이행 및 티어 검토**: 개선 결과를 프로파일과 티어에 반영

#### 한줄 요약
- CSF는 무엇을 구현하라고 지시하지 않고 현재와 목표의 격차만 드러내므로, 프레임워크의 값어치는 목표 프로파일을 조직의 위험 수용 수준에 맞게 정하는 판단에서 나온다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **NIST CSF 4대 구현 티어 (Implementation Tiers)**:
  - **Tier 1 (Partial, 부분적)**: 비정형적, 사후 대응적, 위험 인식이 부서 수준에 머무름.
  - **Tier 2 (Risk-Informed, 위험 반영)**: 정책은 있으나 전사적이지 못하고 자원 배분이 부분적임.
  - **Tier 3 (Repeatable, 반복 가능)**: 전사적 공식 정책 및 위험 관리 프로세스가 수립되어 일관되게 실행됨.
  - **Tier 4 (Adaptive, 적응형)**: 위협 인텔리전스(CTI)를 기반으로 예측적 방어 및 지속적 프로세스 진화 달성.

</details>

| 비교 항목 | Tier 1 (Partial) | Tier 2 (Risk-Informed) | Tier 3 (Repeatable) | Tier 4 (Adaptive) |
|:---|:---|:---|:---|:---|
| **위험 관리** | **비정형 대응** | **위험 반영 정책** | **반복 가능 절차** | **적응형 개선** |
| **전사 통합** | 부서별 수행 | 경영진 일부 참여 | **전사 정책화** | **전략과 통합** |
| **공급망 협력** | 정보 공유 부재 | 위험 인식 | **SLA·평가 공식화** | **실시간 위협 공조** |
| **선택 기준** | 초기 대응 조직 | 부분 관리 조직 | 반복 운영 조직 | **예측 대응 조직** |

#### 한줄 요약
- Tier 1(부분적), Tier 2(위험 반영), Tier 3(반복 가능), Tier 4(적응형)의 4단계 성숙도로 분류된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **NIST CSWP 29 (CSF 2.0 공식 가이드) 및 NIST SP 1301/1302**: 프로파일 작성 방법론 및 구현 티어 평가 가이드라인.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 기술 기능에 치우쳐 **Govern**과 공급망 위험 누락 | **CSWP 29**로 전사 정책과 공급망 지표 수립 | 이사회 중심 위험 관리 확보 |
| 주관적 프로파일로 **투자 중복** 발생 | **SP 1301**에 따라 증적 기반 갭 분석 | 고위험 격차에 예산 집중 |
| 역량보다 높은 **티어**를 자의적으로 지정 | **SP 1302**로 단계별 승격 계획 수립 | 실제 역량에 맞는 성숙도 개선 |

#### 한줄 요약
- Govern 기능으로 거버넌스를 강화하고, SP 1301로 갭을 정량화하며, SP 1302로 현실적 티어를 평가한다.

## Ⅶ. 결론

- 사이버보안을 단순 IT 기술 문제를 넘어 이사회와 최고경영진이 비즈니스 목표와 연계하여 전략적으로 지배하는 **전사 사이버보안 위험 거버넌스(NIST CSF 2.0 / Govern 중심 6대 기능)의 글로벌 공통 프레임워크**로 확고히 자리 잡았으며, 제로 트러스트(NIST SP 800-207) 및 AI 위험 관리(NIST AI RMF)와의 통합으로 진화하는 가운데, 실무 기업 보안 거버넌스 구축 시에는 **Govern 기능 중심의 이사회 보고 체계 및 사이버 공급망 위험(C-SCRM) 정책 수립, 현재 상태와 목표 상태 간의 프로파일 갭 분석을 통한 보안 투자 우선순위 결정, 4단계 구현 티어(Tier 1 Partial $\rightarrow$ Tier 3/4 Repeatable·Adaptive) 로드맵 기반의 단계적 성숙도 고도화**를 결합하여 완벽한 전사 사이버보안 거버넌스를 완성

#### 한줄 요약
- Govern 중심 6대 기능과 프로파일 갭 분석 및 티어 평가를 통해 무결점 NIST CSF 2.0 거버넌스를 완성한다.
