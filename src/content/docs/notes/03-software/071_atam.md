---
sidebar:
  order: 71
  label: "071. ATAM 아키텍처 트레이드오프 분석 방법 (Architecture Tradeoff Analysis Method)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "ATAM 아키텍처 트레이드오프 분석 방법 (Architecture Tradeoff Analysis Method)"
date: "2026-08-13T17:20:00+09:00"
tags:
  - "notes-software"
weight: 71
extra:
  question_no: "071"
  source_status: "기출"
  source_history: "131회"
  priority: 50
  priority_note: "131회 기출, 품질속성 절충 분석 절차"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **ATAM (Architecture Tradeoff Analysis Method, 아키텍처 상충관계 분석 기법)**: 카네기 멜론 대학 SEI가 개발한 소프트웨어 아키텍처 평가 방법론으로, 다수의 품질 속성(Quality Attributes: 성능, 보안성, 가용성 등) 간의 상충/절충 관계(Tradeoff)를 분석하여 시스템 위험 요소를 평가하는 기법.
- **Tradeoff Point (절충점)**: 둘 이상의 품질 속성에 동시에 영향을 미치며, 한 품질 속성을 높이면 다른 품질 속성이 저하되는 아키텍처 결정 지점 (e.g., 암호화 적용으로 보안성$\uparrow$, 처리 성능 $\downarrow$).
- **Sensitivity Point (민감점)**: 단 하나의 품질 속성에 직접적이고 결정적인 영향을 미치는 아키텍처 요소 (e.g., DB 커넥션 풀 크기가 응답 시간에 민감 영향).

</details>

- 정의/개념: 비즈니스 목표(Business Drivers) 및 품질 속성 시나리오를 바탕으로 아키텍처 결정에 따른 민감점, 절충점, 위험(Risk) 및 비위험 요소를 도출하는 정형적 평가 기법인 **ATAM**
- 배경/필요성: 단일 품질 최적화는 **숨은 절충•아키텍처 위험** 유발

#### 한줄 요약

- 품질 시나리오에 기반한 아키텍처 트레이드오프 분석 방법이 핵심이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Utility Tree (유틸리티 트리)**: 아키텍처 평가의 핵심 도구로, 최고 품질 목표(Utility)를 성능, 보안성, 가용성 등 세부 품질 속성 및 concrete 시나리오로 체계화한 4단계 층위 구조 트리.
- **Risk & Non-Risk**: Risk는 요구사항을 충족시키지 못할 위험한 아키텍처 결정, Non-Risk는 품질 속성을 안전하게 달성하는 우수 결정.

</details>

- 비즈니스 동인(**Business Drivers**) 및 **Utility Tree (유틸리티 트리)** 기반 조망
- 4대 평가 산출물 도출 (**Risk, Non-Risk, Sensitivity Point, Tradeoff Point**)
- 이해관계자 전체(발주사, 아키텍트, 개발자, 운영자)가 동시 참여하는 시나리오 평가

#### 한줄 요약

- 우선 시나리오에서 민감점, 절충점, 위험 주제를 찾는 것이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Risk Theme (위험 테마)**: 개별 도출된 Risk 항목들을 상위 차원에서 그룹핑하여 아키텍처의 근본적이고 전사적인 위협 요소를 파악하는 범주.

</details>

```text
 [유틸리티 트리] ─── [아키텍처 접근법]
         │                    │
 [응답 측정값] ───── [품질 응답]
```

선의 의미: Business Drivers로부터 Utility Tree를 도출하고, 이를 시나리오로 대조하여 4대 평가 결과물(Risk/Non-Risk/Sensitivity/Tradeoff)을 수확하는 아키텍처 구조.

| 구성요소 | 책임 |
|:---|:---|
| 유틸리티 트리 | 품질 목표를 우선 시나리오로 구체화 |
| 아키텍처 접근법 | 시나리오에 영향을 주는 설계 결정 설명 |
| 품질 응답 | 자극에 대한 시스템 동작 정의 |
| 응답 측정값 | 품질 충족 여부의 정량 판정 기준 제공 |

#### 한줄 요약

- 유틸리티 트리, 아키텍처 접근법, 품질 응답, 응답 측정값의 분석 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **ATAM 4대 단계 (Phase 0 ~ 3)**: Phase 0(준비 및 커뮤니케이션), Phase 1(아키텍트 중심 평가), Phase 2(이해관계자 동시 평가), Phase 3(최종 결과 리포팅 및 후속조치).

</details>

```text
┌──────────────────────────────┐
│ 사업 동인•아키텍처 설명      │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 유틸리티 트리 구성        │
│ 2. 품질 시나리오 우선화      │
│ 3. 설계 결정 대입            │
│ 4. 위험•민감점•절충점 도출   │
│ 5. 위험 주제•개선안 기록     │
└──────────────┬───────────────┘
               ▼
       [평가 결과 보고]
```

### 동작 원리

1. 유틸리티 트리 구성: 사업 목표를 품질 속성으로 분해.
2. 품질 시나리오 우선화: 중요도•난이도로 분석 순서 결정.
3. 설계 결정 대입: 접근법이 품질 응답에 미치는 영향 분석.
4. 위험•민감점•절충점 도출: 결정별 품질 영향 기록.
5. 위험 주제•개선안 기록: 공통 원인과 후속 조치 연결.

#### 한줄 요약

- 우선 시나리오•설계 대입과 위험•민감점•절충점 도출이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **SAAM vs ATAM vs CBAM**: SAAM은 변경 용이성(Modifiability) 위주 초기 기법, ATAM은 다중 품질속성 상충관계(Tradeoff) 기법, CBAM은 경제성/비용(Cost-Benefit) 중심 기법.

</details>

| 비교 항목 | SAAM (Software Architecture Analysis) | ATAM (Architecture Tradeoff Analysis) | CBAM (Cost Benefit Analysis Method) |
|:---|:---|:---|:---|
| 핵심 평가 목표 | **변경 용이성 (Modifiability) 단일 평가** | **다중 품질 속성 간 상충 관계 **| **아키텍처 투자 대비 경제성/ROI (Cost/Benefit)** |
| 주 주요 분석 도구 | 변경 시나리오 대입 | **Utility Tree & 4대 산출물 매트릭스** | **ROI 계산식 (Benefit / Cost Ratio)** |
| 시나리오 종류 | 변경 시나리오 | **품질 속성 시나리오 (성능, 보안, 가용 등)** | 경제 가치 시나리오 |

#### 한줄 요약

- 품질 절충은 아키텍처 트레이드오프 분석 방법, 국소 변경은 동료 검토가 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Six-Part Quality Attribute Scenario**: 자극원(Source), 자극(Stimulus), 환경(Environment), 대상(Artifact), 응답(Response), 응답 측정치(Response Measure)로 구성된 시나리오 구조.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 시나리오가 모호하여 객관적 아키텍처 평가 불가 | **Six-Part Scenario (6요소 표준 시나리오) 양식 규격화** | 객관적 시나리오 확보 |
| 특정 직군의 이해관계자 의견만 강하게 반영됨 | **이해관계자 투표(Voting) 및 Utility Tree (High/Medium/Low) 기법**| 우선순위 중립성 확보 |
| ATAM 수용 비용과 평가 기간(수주일) 오버헤드 | **핵심 비즈니스 유스케이스 중심의 Mini-ATAM 수행** | 시간 및 비용 절감 |

> 사례: 대형 금융 당계 아키텍처 구축 시 **ATAM 기반 보안성-성능 Tradeoff 평가** 수행

#### 한줄 요약

- 시나리오 6요소, 균형 참여, 백로그 연결이 핵심이다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **ATAM 평가 수립 기준(ATAM Evaluation Standards)**: 시스템 도메인 복잡도, 품질 속성 간 상충성 및 CBAM으로의 연계성에 의거한 체계.

</details>

- 다중 품질 절충은 **ATAM**, 투자 우선순위는 **CBAM**으로 연계 판단

#### 한줄 요약

- 평가 범위와 품질 충돌에 맞는 아키텍처 평가 방식 선택 기준이 핵심이다.
