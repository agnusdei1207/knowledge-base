---
sidebar:
  order: 70
  label: "070. CMMI 성숙도 모델 (Capability Maturity Model Integration)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "CMMI 성숙도 모델 (Capability Maturity Model Integration)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 70
extra:
  question_no: "070"
  source_status: "기출"
  source_history: "122회, 125회"
  priority: 50
  priority_note: "122•125회 반복, 프로세스 성숙도 평가"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **CMMI (Capability Maturity Model Integration)**: 카네기 멜론 대학 소프트웨어 공학 연구소(SEI / CMMI Institute)가 정립한 프레임워크로, 조직의 소프트웨어 개발 및 서비스 프로세스 성숙도(Maturity)를 1~5단계 등급으로 평가하고 지속적 프로세스 개선(Process Improvement)을 가이드하는 모델.
- **Maturity Level vs Capability Level**: 성숙도 단계(Maturity Level)는 조직 전체의 단계적 표현(Staged Representation, 1~5단계), 역량 단계(Capability Level)는 특정 프로세스 영역별 연속적 표현(Continuous Representation, 0~3단계).
- **CMMI V2.0 / V3.0**: 기존 V1.3 체계를 개편하여 애자일(Agile), DevOps, 및 비즈니스 성과(Business Performance) 연계성을 강화한 최신 CMMI 모델 버전.

</details>

- 정의/개념: 조직의 SW 제품 개발, 시스템 엔지니어링 및 서비스 프로세스 능력을 정량적으로 평가하고(Level 1~5) 단계적 프로세스 개선 길잡이를 제공하는 국제 평가 표준 프레임워크인 **CMMI**
- 배경/필요성: 특정 영웅적 개발자(Heroism) 개인 역량 의존에서 탈피, 조직 전체의 균일하고 예측 가능한 표준 프로세스 정립 및 품질/비용/납기(QCD) 통제 요구성

#### 한줄 요약

- 역량 진단과 역량 개선을 연결하는 역량 성숙도 모델 통합이 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **SCAMPI (Standard CMMI Appraisal Method for Process Improvement)**: 조직의 프로세스 성숙도를 정식 심사(Audit)하여 CMMI 등급을 인증 부여하는 CMMI 표준 심사 방법론 (Class A, B, C).

</details>

- 2가지 표현 방법 제공 (**단계적 표현 - Staged / 연속적 표현 - Continuous**)
- **SCAMPI 심사 방법론**을 통한 정량적 심사 및 등급 인증 (Maturity Level 1~5)
- **Practice Areas (PA) & Governance** 중심의 프로세스 표준화

#### 한줄 요약

- 수준 체계, 객관적 증거, 사업 성과 개선이 핵심이다.

## Ⅲ. 구조 및 구성요소 (CMMI 성숙도 5단계: Maturity Levels)

<details><summary>핵심 용어</summary>

- **5대 성숙도 단계**: Level 1 (Initial - 혼돈), Level 2 (Managed - 프로젝트 단위 관리), Level 3 (Defined - 조직 차원 표준화), Level 4 (Quantitatively Managed - 정량 통계적 관리), Level 5 (Optimizing - 지속적 혁신).

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│ Level 5: Optimizing (최적화) ──► 지속적 프로세스 혁신 & 원인 통제       │
├────────────────────────────────────────────────────────────────────────┤
│ Level 4: Quantitatively Managed (정량적 관리) ──► 통계적 성과 측정이 통제 │
├────────────────────────────────────────────────────────────────────────┤
│ Level 3: Defined (정의됨) ──► 전사 조직 표준 프로세스 수립 및 재단(Tailor)│
├────────────────────────────────────────────────────────────────────────┤
│ Level 2: Managed (관리됨) ──► 프로젝트 단위의 요구사항/일정/품질 관리 │
├────────────────────────────────────────────────────────────────────────┤
│ Level 1: Initial (초기) ──► 예측 불가능, 영웅주의 개발자에 의존, 혼돈  │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: Level 1(혼돈)에서 시작하여 Level 5(지속적 최적화)로 진화하는 5단계 성숙도 피라미드 아키텍처.

| 성숙도 단계 (Staged) | 수준 명칭 | 핵심 특징 및 프로세스 상태 |
|:---|:---|:---|
| **Level 1** | **Initial (초기)** | 작업 프로세스가 부재하고 개인 영웅주의에 의존하는 혼돈 상태 |
| **Level 2** | **Managed (관리됨)** | **프로젝트 단위**의 요구사항, 일정, 비용 통제 및 재현성 확보 |
| **Level 3** | **Defined (정의됨)** | **전사 차원**의 표준 프로세스(PAL)가 정립되고 프로젝트별 재단(Tailoring) |
| **Level 4** | **Quantitatively Managed**| **통계적/정량적 기술**로 프로세스 성과 및 변동성을 예측 통제 |
| **Level 5** | **Optimizing (최적화)** | **결함 근본 원인 분석(RCA)** 과 신기술 도입을 통한 지속적 개선 |

#### 한줄 요약

- 실천 영역, 평가, 수준 격차 원인, 개선 조치의 연결 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Process Assets Library (PAL)**: CMMI Level 3 이상 조직이 전사 차원에서 축적 및 공유하는 조직 표준 프로세스, 가이드라인, 매뉴얼 및 산출물 템플릿 저장소.

</details>

```text
┌──────────────────────────────┐
│ 사업 목표 & CMMI 심사 신청  │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 전사 표준 프로세스(PAL)정립│
│ 2. 프로젝트 재단(Tailoring)  │
│ 3. SCAMPI 심사 (증거 확인)   │
│ 4. Maturity Level 등급 인증  │
└──────────────┬───────────────┘
               ▼
 [지속적 최적화 Level 5 이행]
```

### 동작 원리

1. **표준 수립**: 전사 차원의 프로세스 자산 라이브러리(**PAL**) 정립.
2. **Tailoring**: 개별 SI/SM 프로젝트 특성에 맞춰 표준 프로세스를 **재단(Tailoring)** 하여 적용.
3. **SCAMPI Class A 심사**: 전문 심사원(Lead Appraiser)이 프로젝트 산출물 및 인터뷰 검증.
4. **Grading**: 요건 충족 시 CMMI Level 2~5 정식 등급 부여 및 성과 피드백.

#### 한줄 요약

- 실천•증거 매핑과 격차 평가 및 개선 실행•성과 재측정의 순환이 핵심이다.

## Ⅴ. 종류 및 비교 (표현 방법 비교: Staged vs Continuous)

<details><summary>핵심 용어</summary>

- **Staged vs Continuous Representation**: Staged(단계적)는 조직 전체의 1~5단계 성숙도 등급 표시, Continuous(연속적)는 특정 PA(프로세스 영역)별로 0~3단계 능력을 세밀히 평가.

</details>

| 비교 항목 | 단계적 표현 (Staged Representation) | 연속적 표현 (Continuous Representation) |
|:---|:---|:---|
| 중심 개념 | **조직 전체의 성숙도 (Maturity Level)** | **특정 프로세스 영역의 역량 (Capability Level)**|
| 등급 범위 | **Level 1 ~ Level 5 (5단계)** | **Level 0 ~ Level 3 (4단계)** |
| 장점 | **조직 간 성숙도 비교가 명확함 (인증 목적)** | **조직이 원하는 특정 영역을 핀포인트 개선 가능** |
| 적용 목적 | 대형 SI 입찰, 조직 전체 등급 인증 | 수주 목적이 아닌 조직 내부 자체 프로세스 개선 |

#### 한줄 요약

- 조직 전체는 성숙도 수준, 개별 영역은 능력도 수준으로 평가한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Paperwork Overkill**: CMMI 등급 획득에만 치중하여 실제 개발 현장과 맞지 않는 형식적 문서 및 서류만 과도하게 양산하는 안티패턴.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 등급 심사만을 위한 형식적 서류 폭증 (**Paperwork Overkill**) | **CMMI V2.0 / V3.0 지침 수용 및 개발 도구 자동 산출 연동** | 서류 오버헤드 해소 |
| 애자일/DevOps 배포 환경과 CMMI 프로세스 충돌 | **Agile/DevOps 융합 CMMI 프랙티스(CMMI for Agile) 도입** | 빠른 배포와 프로세스 조화 |
| CMMI 등급 획득 후 프로세스 사장 | 전사 프로세스 자산 라이브러리(PAL) 상시 모니터링 체계 구축 | 품질 일관성 지속 |

> 사례: 대형 IT SI 기업의 **CMMI Level 3 / Level 5 정식 인증** 취득 및 전사 재단(Tailoring) 지침 운용

#### 한줄 요약

- 재단, 종단 흐름, 증거 자동 축적, 목표 필요 수준이 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **CMMI 평가 수립 기준(CMMI Appraisal Standards)**: 수주 입찰 요건, 전사 프로세스 표준화 수준 및 Agile/DevOps 통합성에 의거한 체계.

</details>

- **CMMI 평가 수립 기준**에 따라 공공/국방 SI 사업 수행 및 품질 가시화 도출 시 **CMMI Level 3+ 인증 및 CMMI V3.0** 수용

#### 한줄 요약

- 개선 범위에 맞는 평가 범위 선택 기준이 핵심이다.
