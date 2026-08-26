---
sidebar:
  order: 70
  label: "070. CMMI 성숙도 모델"
  badge:
    text: "기출 · 50%"
    variant: note
title: "CMMI 성숙도 모델 (Capability Maturity Model Integration)"
date: "2026-08-26T13:04:07+09:00"
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

<details><summary>용어 설명</summary>

- **CMMI**: 조직의 개발·서비스 프로세스 역량을 평가하고 개선하는 성숙도 모델.
- **Maturity Level 1~5**: Initial(초기) $\to$ Managed(관리) $\to$ Defined(정의) $\to$ Quantitatively Managed(정량관리) $\to$ Optimizing(최적화) 5단계 성숙도.

</details>

- 정의/개념: 소프트웨어 개발 프로세스 역량을 평가하고 개선하기 위해 **5단계 성숙도(Level 1~5)와 실천 영역(Practice Area)** 을 체계화한 프로세스 개선 모델
- 배경/필요성: 비공식적 영웅주의 개발 의존으로 인한 **프로젝트 납기 지연, 품질 편차 폭증 및 프로세스 재현 불가 해결 불가**

#### 한줄 요약
- 조직의 프로세스 성숙도를 5단계로 진단하고 지속적 품질 개선 경로를 제시한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Staged vs Continuous**: 조직 전체 성숙도를 Level 1~5로 단일 평가하는 단계적 표현(Staged)과 특정 실천영역별 역량을 개별 평가하는 연속적 표현(Continuous).
- **PAL(Process Asset Library)**: 전사 표준 프로세스, 가이드라인, 템플릿을 중앙 축적하여 프로젝트별 테일러링(Tailoring)을 지원하는 공정 자산 저장소.

</details>

- 조직 전체 성숙도(Staged) 및 개별 영역 역량(Continuous)의 **2가지 유연한 평가 표현 방식**
- 프로젝트 관리(L2), 전사 표준(L3), 통계적 제어(L4), 지속적 혁신(L5)의 **5단계 발전 경로**
- 공식 심사 방법론(Appraisal Method) 기반의 **객관적 데이터 증적(Work Product) 검증**

#### 한줄 요약
- 5단계 성숙도 피라미드와 증적 기반 심사로 전사 프로세스 표준화를 실현한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Practice Area(실천 영역)**: 요구사항 개발(RD), 프로젝트 계획(PP), 품질 보증(QA), 형상 관리(CM) 등 성숙도를 구성하는 엔지니어링 실천 단위.

</details>

```text
[CMMI 5단계 성숙도 피라미드 구조]
|-- Level 5: Optimizing (최적화: 결함 근본 원인 제거, 프로세스 혁신 및 자동화)
|-- Level 4: Quantitatively Managed (정량적 관리: 통계적 공정 제어 및 메트릭 분석)
|-- Level 3: Defined (정의됨: 전사 표준 프로세스 수립, 조직 공정 자산 PAL, 테일러링)
|-- Level 2: Managed (관리됨: 프로젝트 단위 계획, 요구사항 추적, 형상 관리)
`-- Level 1: Initial (초기: 비공식적 프로세스, 개인의 영웅적 역량 의존, 혼돈)
```

선의 의미: 가지는 성숙도 수준의 서열 관계

| 구성요소 | 책임 |
|:---|:---|
| Level 1 초기 | 비정형 프로세스의 수행 결과 확인 |
| Level 2 관리 | **프로젝트 계획·요구·형상** 관리 |
| Level 3 정의 | **조직 표준 프로세스**와 테일러링 적용 |
| Level 4 정량 관리 | 통계 기법으로 품질·성능 변동 관리 |
| Level 5 최적화 | 근본 원인 분석과 프로세스 개선 |

#### 한줄 요약
- L1(혼돈) → L2(프로젝트 관리) → L3(전사 표준) → L4(통계 제어) → L5(지속 혁신)로 진화한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **CMMI Appraisal(심사 절차)**: 공인 심사원(Lead Appraiser)이 투입되어 조직의 산출물과 인터뷰를 분석해 최종 성숙도 등급을 부여하는 공식 절차.

</details>

```text
비즈니스 성과 목표 수립 및 CMMI 심사 대상 실천 영역(PA) 선정
        │
   [증거 수집] Git 커밋 로그, Jira 이슈, 테스트 결과서 등 산출물 증적 수집
        │
   [격차 분석] 목표 성숙도 레벨 요건 대비 미충족 프로세스 갭(Gap) 식별
        │
   [표준 개선] 전사 표준 프로세스(PAL) 개정 및 프로젝트 테일러링 가이드 배포
        │
   [공식 심사] 심사원 인터뷰와 증적 검증으로 성숙도 평정
```

#### 한줄 요약
- 목표 수립 → 증적 수집 → 격차 분석 → 프로세스 개선 → 공식 심사 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Staged vs Continuous Representation**: 조직 전체 등급 인증을 위한 Staged 모델과 특정 취약점 집중 개선을 위한 Continuous 모델.

</details>

| 비교 항목 | 단계적 표현 (Staged Model) | 연속적 표현 (Continuous Model) |
|:---|:---|:---|
| 평가 관점 | **조직 전체의 종합적 성숙도 평가** | **특정 프로세스 영역(PA)별 개별 역량 평가** |
| 결과 지표 | **Maturity Level (레벨 1 ~ 5)** | Capability Level (레벨 0 ~ 3) |
| 주 활용처 | 조직 전체의 대외 **성숙도 평정** | 특정 실천 영역의 역량 개선 |
| 장단점 | 대외 신뢰도 높으나 전 영역 충족 부담 | 유연하게 취약 영역 집중 개선 가능 |

#### 한줄 요약
- 대외 공인 인증과 입찰은 Staged, 사내 취약 프로세스 맞춤 개선은 Continuous를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Paperwork Overkill**: CMMI 인증 통과만을 위해 실제 개발과 무관한 수백 장의 허위/형식 문서를 양산하는 부작용.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 심사용 형식 문서 과다 생성 | **개발 도구 연계 증적 자동화** | 문서 부담 감소와 증적 추적성 향상 |
| 애자일/CI-CD 배포 주기와 무거운 프로세스의 충돌 | **CMMI Agile/DevOps 가이드 적용 및 경량 테일러링 허용** | 빠른 릴리즈와 프로세스 거버넌스의 양립 |
| 인증 획득 후 프로세스 미준수 및 형해화 | **전사 품질보증(QA) 상시 감사 및 PAL 프로세스 정기 업데이트** | 획득 레벨의 지속적 유지 및 품질 표준화 |
| 소규모 조직의 CMMI 도입 비용 부담 | 필요한 **실천 영역부터 점진 적용** | 초기 도입 범위와 비용 제한 |

#### 한줄 요약
- 도구 연동 증적 자동화, 애자일 경량 테일러링, 상시 내부 감사로 실효성을 확보한다.

## Ⅶ. 결론

- 조직 전체 평정은 **Staged**, 영역 개선은 **Continuous** 선택

#### 한줄 요약
- CMMI는 개인의 영웅적 역량에 의존하던 소프트웨어 개발을 조직의 정량적이고 지속 가능한 자산으로 발전시키는 성숙도 프레임워크다.
