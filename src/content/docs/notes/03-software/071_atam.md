---
sidebar:
  order: 71
  label: "071. ATAM 아키텍처 트레이드오프 분석 방법"
  badge:
    text: "기출 · 50%"
    variant: note
title: "ATAM 아키텍처 트레이드오프 분석 방법 (Architecture Tradeoff Analysis Method)"
date: "2026-08-26T17:32:00+09:00"
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

- **ATAM(Architecture Tradeoff Analysis Method)**: 미국 SEI에서 개발한, 소프트웨어 아키텍처가 비즈니스 목표 및 품질 속성을 충족하는지 트레이드오프 관점에서 평가하는 방법론.
- **유틸리티 트리(Utility Tree)**: 전사 비즈니스 요구사항을 성능, 가용성, 보안 등 품질 속성별 세부 시나리오로 구조화한 트리.

</details>

- 정의/개념: 비즈니스 목표 달성을 위해 **유틸리티 트리(Utility Tree) 기반 품질 시나리오와 민감점·절충점(Trade-off)** 을 평가하는 아키텍처 검증 방법론
- 배경/필요성: 단일 품질 편향 설계로 **타 품질 침해·재구축 위험**

#### 한줄 요약
- 유틸리티 트리와 시나리오를 바탕으로 아키텍처의 민감점, 절충점, 위험 요소를 체계적으로 분석한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Sensitivity vs Trade-off**: 단일 품질에 크게 영향을 주는 설계 결정(민감점)과 두 개 이상의 품질이 상충하는 설계 결정(절충점).
- **Risk vs Non-Risk**: 품질 목표 달성을 저해하는 잠재적 설계 결함(위험)과 긍정적으로 기여하는 안전한 설계 결정(비위험).

</details>

- 비즈니스 동인(Business Drivers)과 **유틸리티 트리 기반의 체계적 품질 분해**
- 아키텍처 4대 산출물(**Risk, Non-Risk, Sensitivity Point, Tradeoff Point**) 도출
- 아키텍트, 개발자, 고객 등 전 이해관계자가 참여하는 **합의 기반 시나리오 우선순위화**

#### 한줄 요약
- 유틸리티 트리로 시나리오를 구체화하고 4대 산출물(위험/비위험/민감점/절충점)을 도출한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **품질 시나리오 6요소**: 자극원(Source), 자극(Stimulus), 환경(Environment), 대상(Artifact), 응답(Response), 측정치(Measure).

</details>

```text
[ATAM 분석 프레임워크 및 유틸리티 트리 구조]
|-- 비즈니스 동인 (Business Drivers: 시장 진입 속도, 금융 무결성)
|-- 유틸리티 트리 (Utility Tree: 품질 속성 계층화)
|   |-- 성능 (Performance: 초당 1,000건 주문 인입 시 99% 응답 < 200ms)
|   |-- 가용성 (Availability: DB 장애 시 10초 내 Standby Failover)
|   `-- 보안성 (Security: 결제 패킷 100% AES-256 종단 간 암호화)
`-- 아키텍처 4대 평가 산출물
    |-- Sensitivity Point (민감점: DB 인덱싱 전략 -> 성능에 민감)
    |-- Tradeoff Point (절충점: 전송 구간 암호화 -> 보안 상승, 성능 저하)
    |-- Risk (위험 요소: 단일 Redis 클러스터 장애 시 전체 세션 유실)
    `-- Non-Risk (비위험 요소: 표준 OAuth 2.0 도입으로 인증 안전)
```

선의 의미: 계층 및 비즈니스 동인-유틸리티 트리-4대 산출물 연계 구조

| 구성요소 | 책임 |
|:---|:---|
| 유틸리티 트리 | 목표의 **품질 시나리오 구조화** |
| 민감점 | 단일 품질에 민감한 **설계 요소 식별** |
| 절충점 | 복수 품질의 **상충 결정 분석** |
| 위험·비위험 | 목표를 위협·지원하는 **설계 판정** |

#### 한줄 요약
- 유틸리티 트리, 품질 시나리오 6요소, 4대 평가 산출물(위험/비위험/민감점/절충점)이 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **ATAM 4단계 Phase**: Phase 0(준비 및 파트너십) $\to$ Phase 1(아키텍트 중심 1차 평가) $\to$ Phase 2(이해관계자 2차 평가) $\to$ Phase 3(결과 보고 및 후속 조치).

</details>

```text
비즈니스 동인(Business Drivers) 및 후보 아키텍처 접근법 소개
        │
   유틸리티 트리 구성 및 품질 시나리오 6요소 도출
        │
   시나리오 우선순위 투표 (중요도 x 난이도: High/Medium/Low 매트릭스)
        │
   아키텍처 설계 결정을 시나리오에 대입하여 민감점 및 절충점(Trade-off) 분석
        │
   식별된 위험 요소를 '위험 테마(Risk Themes)'로 범주화하여 최종 개선 리포트 산출
```

#### 한줄 요약
- 소개 → 유틸리티 트리 작성 → 시나리오 우선화 → 설계 대입 및 트레이드오프 분석 → 결과 보고 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **SAAM vs ATAM vs CBAM**: 변경 용이성 중심의 SAAM, 다중 품질 절충 중심의 ATAM, 경제성/ROI 중심의 CBAM.

</details>

| 비교 항목 | SAAM (Software Architecture Analysis) | ATAM (Tradeoff Analysis) | CBAM (Cost-Benefit Analysis) |
|:---|:---|:---|:---|
| 핵심 평가 관점 | **모듈 변경 용이성 (Modifiability)** | **다중 품질 속성 간 상충 관계 절충** | **아키텍처 대안별 경제성 및 ROI** |
| 주요 산출물 | 변경 시나리오별 영향도 및 결합도 | **민감점, 절충점, 위험/비위험 요소** | **비용 대 편익 비율, 투자 우선순위** |
| 평가 기법 | 시나리오 기반 정성적 분석 | **유틸리티 트리 기반 정량/정성 절충** | 효용 점수화 및 경제적 가치 산정 |

#### 한줄 요약
- 단일 변경성은 SAAM, 다중 품질 절충은 ATAM, 경제성 투자는 CBAM을 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Mini-ATAM**: 수 주가 걸리는 풀버전 대신, 핵심 시나리오 5~10개만 선별하여 1~2일 내에 끝내는 경량 아키텍처 평가.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 모호한 시나리오로 인한 주관적 평가 논쟁 | **6요소(자극원, 자극, 환경, 대상, 응답, 응답측정치) 표준 작성** | 수치화된 객관적 검증 기준 확립 |
| 특정 이해관계자의 발언권 독점으로 편향 발생 | **High/Medium/Low 브레인스토밍 및 스티커 투표(Dot Voting)** | 공정하고 중립적인 우선순위 도출 |
| 정규 ATAM 수행 기간(2~3주)의 일정 부담 | **핵심 비즈니스 시나리오 5개 중심의 Mini-ATAM 기법 적용** | 평가 기간 2일 이내 단축 및 신속 피드백 |
| 평가 후 도출된 위험 요소 방치 | **도출된 위험을 아키텍처 의사결정 기록(ADR) 및 백로그에 반영** | 후속 개발 시 위험 조기 완화 보장 |

#### 한줄 요약
- 6요소 시나리오 표준화, Dot Voting 투표, Mini-ATAM 경량화, ADR 반영으로 실효성을 높인다.

## Ⅶ. 결론

- 품질 상충 평가는 **ATAM**, 경제성 판단은 **CBAM** 선택

#### 한줄 요약
- ATAM은 다중 품질 속성 간의 충돌을 선제적으로 가시화하고 최적의 아키텍처 절충안을 도출하는 국제 표준 아키텍처 평가 방법론이다.
