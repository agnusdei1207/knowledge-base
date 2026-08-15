---
sidebar:
  order: 111
  label: "111. NIST Cybersecurity Framework (NIST CSF)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "NIST Cybersecurity Framework (NIST CSF)"
date: "2026-08-13T21:44:00+09:00"
tags:
  - "notes-security"
weight: 111
extra:
  question_no: "111"
  source_status: "기출"
  source_history: "137회"
  priority: 70
  priority_note: "137회 기출에 CSF 2.0 Govern 확장까지 흡수함"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **미국 국립표준기술연구소(National Institute of Standards and Technology, NIST)**: 기술 표준 및 사이버보안 가이드를 발행하는 미국 정부 기관.
- **사이버보안 프레임워크(Cybersecurity Framework, CSF)**: 사이버보안 위험 관리 전략과 성과를 공통 표준 언어로 체계화한 프레임워크.

</details>

- 정의/개념: **NIST**의 **CSF**는 사이버 위험관리 결과를 공통 언어로 정한 프레임워크.
- 배경/필요성: 부서별 통제•용어만으로는 경영 위험과 보안 성과 우선순위를 연결하기 어려움.

#### 한줄 요약

- 달성할 결과를 공유하고 구체적인 수단은 조직이 선택한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **결과 중심(Outcome-based Approach)**: 통제 및 기술 방식보다 조직이 최종 도출해야 하는 보안 결과에 집중하는 방식.
- **조직 프로파일(Organizational Profile)**: 조직의 사업 목표와 위험 수용도를 반영하여 현재 및 목표 성과를 정의한 문서.
- **Govern(Govern Function)**: 조직의 사이버보안 위험 관리 전략, 거버넌스 및 책임을 의결하는 CSF 2.0의 신설 기능.
- **Implementation Tier(Implementation Tier)**: 조직의 사이버보안 위험 관리 관행의 정교함과 이행 수준을 4단계로 평가하는 도구.

</details>

- 특정 제품•통제를 강제하지 않는 **결과 중심** 적용.
- **Govern** 포함 6개 기능의 전사 위험 연결.
- **조직 프로파일**의 격차와 **Implementation Tier**로 개선 결정.

#### 한줄 요약

- 현재와 목표 결과의 차이로 예산과 개선 순서를 정한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **CSF 핵심부(CSF Core)**: 거버넌스, 식별, 보호, 탐지, 대응, 복구의 6대 핵심 기능과 세부 카테고리로 구성된 체계.

</details>

```text
CSF 핵심부
├─ Govern
│  └─ 전략 · 정책 · 역할 · 공급망 위험
├─ Identify
│  └─ 자산 · 환경 · 위험 식별
├─ Protect
│  └─ 식별 위험의 보호조치
├─ Detect
│  └─ 지속 감시 · 사건 분석
├─ Respond
│  └─ 사고 관리 · 완화 · 소통
└─ Recover
   └─ 자산 · 운영 복원 · 개선
```

| 구성요소 | 책임 |
|:---|:---|
| Govern | **Govern**이 전략•정책•역할•공급망 위험 관리 |
| Identify | 자산•환경•위험 식별 |
| Protect | 식별 위험의 보호조치 적용 |
| Detect | 지속 감시•분석 기반 사건 발견 |
| Respond | 사고 관리•완화•보고•소통 |
| Recover | 자산•운영 복원•복구 개선 |

#### 한줄 요약

- 거버넌스 아래 식별•보호•탐지•대응•복구를 지속한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **현재•목표 프로파일(Current and Target Profile)**: 현재의 보안 성과 수준과 향후 달성하고자 하는 목표 성과 수준을 대조하는 도구.
- **조직 상황•위험 허용 설정(Context and Risk Tolerance Setup)**: 조직 비즈니스 목적과 위험 허용 수준을 설정하는 단계.
- **현재 프로파일•증적 구성(Current Profile and Evidence Composition)**: 현재 수행 중인 보안 통제 성과와 이행 증적을 수집하는 단계.
- **목표 프로파일•격차 분석(Target Profile and Gap Analysis)**: 목표 성과 수준을 설정하고 현재 수준과의 격차를 도출하는 단계.
- **개선 계획•성과지표 수립(Action Plan and KPI Formulation)**: 도출된 격차를 해소하기 위한 세부 개선 계획 및 KPI를 정의하는 단계.
- **투자•개선 우선순위 결정(Investment and Priority Decision)**: 개선 계획의 우선순위를 정하고 자원 투입을 결정하는 단계.

</details>

```text
1. 조직 상황•위험 허용 설정
              │
              ▼
2. 현재 프로파일•증적 구성
              │
              ▼
3. 목표 프로파일•격차 분석
              │
              ▼
4. 개선 계획•성과지표 수립
              │
              ▼
5. 투자•개선 우선순위 결정
              │
              └──── 실행 · 성과평가 ────┐
                                        └─ 현재 프로파일 갱신
```

### 동작 원리

1. **조직 상황·위험 허용 설정**: 임무·위협·자원 확인
2. **현재 프로파일·증적 구성**: 달성 결과·근거 구성
3. **목표 프로파일·격차 분석**: 현재·목표 차이 분석
4. **개선 계획·성과지표 수립**: 위험·비용별 실행안 수립
5. **투자·개선 우선순위 결정**: 성과별 자원 배분

#### 한줄 요약

- 현재와 목표 프로파일의 차이부터 개선한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Core 역할(Core Role)**: 공통된 사이버보안 기능과 목표 결과를 범주별로 분류하는 역할.
- **Profile 역할(Profile Role)**: 조직 고유의 현재 보안 상태와 목표 수준 간의 격차를 시각화하는 역할.
- **Tier 역할(Tier Role)**: 사이버보안 위험 대응 절차의 조직화 및 성숙도 수준을 평가하는 역할.

</details>

| CSF 요소 | 역할 | 산출물 |
|:---|:---|:---|
| **CSF Core** | **Core 역할** | 기능•범주•하위범주 |
| **조직 프로파일** | **Profile 역할** | 현재 프로파일•목표 프로파일 |
| **Implementation Tier** | **Tier 역할** | Tier 1~4의 관행 수준 |

#### 한줄 요약

- Core는 결과, Profile은 목표, Tier는 관행의 엄격성이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **사이버보안 백서(Cybersecurity White Paper, CSWP)**: NIST가 사이버보안 기술 주제를 상술하여 발간하는 공식 보고서 문서.
- **특별 간행물(Special Publication, SP)**: NIST가 가이드라인 및 모범 사례를 제시하는 표준 지침서.
- **NIST CSWP 29(NIST CSWP 29)**: NIST CSF 2.0 규격 및 설명서를 정의한 공식 문서.
- **NIST SP 1301(NIST SP 1301)**: CSF 조직 프로파일 작성 및 관리 지침을 제시하는 문서.
- **NIST SP 1302(NIST SP 1302)**: Implementation Tier 활용 및 평가 가이드를 제공하는 문서.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| CSF 2.0 적용 | **CSWP** **NIST CSWP 29** 활용 | 위험 소통 표준화 |
| 프로파일 작성 | **SP** **NIST SP 1301** 적용 | 목표•격차 명확화 |
| Tier 활용 | **NIST SP 1302** 적용 | 등급 오용 방지 |

#### 한줄 요약

- 업무 위험을 가장 크게 줄이는 프로파일 격차부터 투자한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **공통 결과 기준(Common Outcome Baseline)**: 경영진과 실무진이 균일한 언어로 사이버 위험과 성과 목표를 소통하는 기준.

</details>

- **공통 결과 기준**에 따라 보안 결과는 **CSF Core**, 현재•목표 격차는 **조직 프로파일**, 관행 엄격성은 **Implementation Tier**로 설명.

#### 한줄 요약

- 경영진과 실무자가 같은 결과 기준으로 투자 순서를 합의한다.
