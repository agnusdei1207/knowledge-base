---
sidebar:
  order: 69
  label: "069. ISO/IEC 25010 소프트웨어 제품 품질 모델 (Software Product Quality Model)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "ISO/IEC 25010 소프트웨어 제품 품질 모델 (Software Product Quality Model)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 69
extra:
  question_no: "069"
  source_status: "기출"
  source_history: "120회, 128회"
  priority: 70
  priority_note: "120•128회 반복, 품질 특성 상위 모델"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **ISO/IEC 25010**: SQuaRE(Software Product Quality Requirements and Evaluation) 시리즈의 핵심 표준으로, 소프트웨어 제품의 품질 특성(Product Quality Model)을 체계적으로 분류 및 정의한 국제 표준.
- **Product Quality Model (제품 품질 모델)**: 소프트웨어의 내/외부 특성을 8대 주특성(25010:2011) 및 9대 주특성(25010:2023 개정판)으로 세분화한 평가 프레임워크.
- **SQuaRE (Software Quality Requirements and Evaluation)**: ISO/IEC 9126과 14598을 통합 개편하여 소프트웨어 제품 품질 요구사항 수립 및 평가 절차를 규정한 종합 표준군 (ISO/IEC 25000 시리즈).

</details>

- 정의/개념: 소프트웨어 제품의 품질 요구사항 정의, 측정 및 객관적 수용 평가를 위해 9대 주특성(2023년 개정판 기준) 및 세부 부특성으로 체계화한 국제 제품 품질 표준 모델인 **ISO/IEC 25010**
- 배경/필요성: 정성적이고 모호한 '품질' 개념의 객관적 수치화(Metrics) 필요성, 발주자-개발자-감리원 간의 정량적 품질 수용 평가 기준 표준화 요구성

#### 한줄 요약

- 국제표준화기구와 국제전기기술위원회가 제시한 9개 제품 품질 특성의 공통 분류가 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Quality in Use vs Product Quality**: 제품 품질(Product Quality)은 소프트웨어의 고유한 시스템적 특성, 사용 품질(Quality in Use, ISO/IEC 25019)은 특정 사용 맥락에서의 실제 유저 만족도 및 효과성.

</details>

- **System & Software Product Quality Model** 9대 주특성 규정 (2023년 개정: Safety 추가)
- 정량적 측정 메트릭(**Quality Metrics**)과 연계한 객관적 평가 가능
- 발주사 요구사항(SRS) 작성부터 최종 TTA GS 인증 시험의 근거 표준

#### 한줄 요약

- 공통 품질 어휘, 측정값, 허용 기준이 핵심이다.

## Ⅲ. 구조 및 구성요소 (ISO/IEC 25010:2023 9대 품질 주특성)

<details><summary>핵심 용어</summary>

- **9대 주특성 (2023 개정판)**: Functional Suitability, Performance Efficiency, Compatibility, Interaction Capability(기존 Usability), Reliability, Security, Maintainability, Flexibility(기존 Portability), Safety(신규 추가).

</details>

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                 ISO/IEC 25010:2023 제품 품질 9대 주특성                 │
├──────────────┬──────────────┬──────────────┬──────────────┬─────────────┤
│ Functional   │ Performance  │ Compatibility│ Interaction  │ Reliability │
│ Suitability  │ Efficiency   │ (호환성)     │ Capability   │ (신뢰성)    │
│ (기능적합성) │ (성능효율성) │              │ (상호작용성) │             │
├──────────────┴──────────────┼──────────────┴──────────────┼─────────────┤
│ Security (보안성)           │ Maintainability(유지보수성) │ Flexibility │
│                             │                             │ (유연성)    │
├─────────────────────────────┴─────────────────────────────┴─────────────┤
│ Safety (안전성 - 2023년 신규 추가 특성)                                │
└─────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 소프트웨어 제품 품질을 평가하기 위한 9가지 독립적 주특성 범주 아키텍처.

| 9대 주특성 (2023 기준) | 주특성 정의 | 대표적인 세부 부특성 (Sub-characteristics) |
|:---|:---|:---|
| **1. Functional Suitability** | 명시된 기능적 요구를 만족하는 정도 | 기능 완결성, 기능 정확성, 기능 적절성 |
| **2. Performance Efficiency** | 자원 사용량 대비 성능 응답 수준 | 시간 반응성(Latency), 자원 활용성, 용량성(Capacity)|
| **3. Compatibility** | 타 제품과 공존하고 정보를 교환하는 정도| 공존성 (Co-existence), 상호운용성 (Interoperability)|
| **4. Interaction Capability**| 유저가 편리하게 학습하고 상호작용하는 정도| 사용자 오류 방지성, 오용 방지성, 접근성(Accessibility)|
| **5. Reliability** | 지정 조건에서 기능을 무결하게 유지하는 정도| 성숙성, 결함 허용성(Fault Tolerance), 복구성 |
| **6. Security** | 정보 및 데이터를 미인가 접근으로부터 보호 | 기밀성, 무결성, 부인방지성, 책임추적성, 진본성 |
| **7. Maintainability** | 모듈을 분석, 수정 및 시험하기 쉬운 정도| 모듈성(Modularity), 재사용성, 수정성, 시험가능성|
| **8. Flexibility** | 다른 환경으로 적응 및 이식되는 정도 | 적응성(Adaptability), 설치성, 이식성(Replaceability)|
| **9. Safety (2023 신규)** | 사람, 재산, 환경에 해를 입히지 않는 정도 | 자율 위험 통제성, 안전 격리성 |

#### 한줄 요약

- 사용 맥락, 품질 특성, 부특성, 품질 측정값, 허용 기준의 계층 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Quality Requirement & Evaluation Process**: SQuaRE 표준 절차에 따라 요구사항 정립 $\rightarrow$ 측정 항목 메트릭 설계 $\rightarrow$ 테스트 실행 및 측정 $\rightarrow$ 수용 기준 대조.

</details>

```text
┌──────────────────────────────┐
│ 사업 발주 요구사항(RFP) 수거 │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. ISO 25010 9대 주특성 매핑 │
│ 2. 정량 메트릭 (Metrics) 설정│
│ 3. 시험 환경 수립 & Test 실행│
│ 4. 측정값 대 수용 기준 비교  │
└──────────────┬───────────────┘
               ▼
   [TTA GS 인증 / 최종 인수 합격]
```

### 동작 원리

1. **품질 특성 매핑**: 발주사 비기능 요구사항을 ISO 25010 9대 주특성으로 체계적 분류.
2. **Metrics 정의**: 시간 반응성(응답시간 1초 이내), 결함 허용성(HA 자동 failover 3초 이내) 등 수치화.
3. **Measurement**: 부하 테스트 도구(JMeter) 및 정적 도구로 정량 수치 수거.
4. **Evaluation**: 수집된 수치 대 수용 기준(Acceptance Threshold) 대조 후 GS 인증 또는 최종 합격 판정.

#### 한줄 요약

- 사용 맥락•실패 영향 분석을 품질 요구•허용 기준 정의로 변환하는 것이 핵심이다.

## Ⅴ. 종류 및 개정 비교 (2011년 판 대 2023년 판)

<details><summary>핵심 용어</summary>

- **2011 vs 2023 ISO 25010 Revision**: 2011년 8대 주특성 구조에서 2023년 개정을 통해 Usability $\rightarrow$ Interaction Capability로 명칭 변경, Portability $\rightarrow$ Flexibility로 통합 개편, **Safety(안전성)** 주특기 신규 추가.

</details>

| 개정 비교 항목 | ISO/IEC 25010:2011 (구판) | ISO/IEC 25010:2023 (신판 개정) |
|:---|:---|:---|
| 주특성 개수 | 8대 주특성 체계 | **9대 주특성 체계 (Safety 추가)** |
| 안전성 (Safety) | 신뢰성/품질 영역 일부에 산재 | **독립 주특성으로 'Safety' 신규 승격 (자율주행, AI 대비)** |
| 사용성 명칭 | Usability (사용성) | **Interaction Capability (상호작용 능력으로 명칭 변경)** |
| 이식성 명칭 | Portability (이식성) | **Flexibility (유연성으로 확장 통합 명칭 변경)** |

#### 한줄 요약

- 기존 계약은 명시 판본, 신규 제품은 ISO/IEC 25010:2023을 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Quality Trade-off**: 성능 효율성(속도)을 높이려다 보안성(암호화 검사)이 떨어지거나, 신뢰성을 높이려다 성능 오버헤드가 발생하는 특성 간 상충 관계.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 품질 특성 간 상충 관계(**Quality Trade-off**) 발생 | 비즈니스 중요도에 따른 특성별 가중치(Weight) 사전 합의 | 아키텍처 타협점 정립 |
| 정성적인 요구사항으로 인해 객관적 감리/평가 불가능 | **SQuaRE 25023 정량 측정 메트릭(Metrics) 표준 적용** | 객관적 수치 검증 |
| AI / 로봇 / 자율주행 SW 품질 평가 기준 부재 | **2023 개정판 Safety(안전성) 및 Flexibility 주특성 수용** | 모빌리티 SW 검증 대응 |

> 사례: **TTA 소프트웨어 시험인증연구소 GS(Good Software) 인증 1등급** 평가 가이드

#### 한줄 요약

- 실패 위험, 측정 조건, 품질 절충에 기반한 기준화가 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **ISO/IEC 25010 수용 기준(ISO 25010 Adoption Standards)**: 시스템 도메인 특성, SQuaRE 평가 지침 및 2023년 9대 주특기 표준에 의거한 체계.

</details>

- **ISO/IEC 25010 수용 기준**에 따라 GS 인증 및 SW 품질 평가 시 **ISO/IEC 25010:2023 9대 품질 주특성** 필수 수용

#### 한줄 요약

- 맥락•위험•검증 가능성에 기반한 품질 요구 우선순위가 핵심이다.
