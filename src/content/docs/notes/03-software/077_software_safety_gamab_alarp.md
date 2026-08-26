---
sidebar:
  order: 77
  label: "077. 소프트웨어 안전: GAMAB•ALARP"
  badge:
    text: "기출 · 50%"
    variant: note
title: "소프트웨어 안전: GAMAB•ALARP (Software Safety GAMAB ALARP)"
date: "2026-08-26T17:50:00+09:00"
tags:
  - "notes-software"
weight: 77
extra:
  question_no: "077"
  source_status: "기출"
  source_history: "128회"
  priority: 50
  priority_note: "128회 기출, 허용 위험 판단의 안전 기준"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **GAMAB(Globalement Au Moins Aussi Bon)**: 프랑스/철도 표준 원칙으로, 신규 시스템의 전체 위험 수준이 기존 레퍼런스 시스템보다 "적어도 동등 이상으로 안전해야 한다"는 원칙.
- **ALARP(As Low As Reasonably Practicable)**: 영국/IEC 61508 표준 원칙으로, 위험 저감 비용이 편익 대비 현저히 불균형하지 않는 한 "합리적으로 실행 가능한 한 낮추어야 한다"는 원칙.

</details>

- 정의/개념: 기능 안전 시스템 구축 시 **기존 대비 동등 이상 안전(GAMAB)과 비용 대비 합리적 저감(ALARP)** 을 규정한 위험 통제 원칙
- 배경/필요성: 위험 수용 기준 부재로 **과잉 투자·안전 대책 누락**

#### 한줄 요약
- 동등 안전성(GAMAB)과 합리적 저감(ALARP) 원칙을 통해 허용 가능한 잔여 위험을 통제한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Gross Disproportion Test(현저한 불균형 시험)**: 추가적인 위험 저감에 소요되는 비용이 얻게 되는 안전 편익보다 10배 이상 비현실적으로 큼을 입증하는 판정 기준.
- **Safety Case(안전성 보증 사례)**: GSN(Goal Structuring Notation) 등을 활용해 시스템이 안전 목표를 충족함을 논리적 증거로 입증하는 문서.

</details>

- 레퍼런스 시스템과의 비교를 통한 **상대적 안전 동등성(GAMAB) 입증**
- 위험도를 **불허용(Intolerable), ALARP(합리적 저감), 광범위 허용(Acceptable) 3대 영역 분할**
- 독립 안전 평가원(ISA)과 **안전 보증 사례(Safety Case) 기반의 객관적 증적 검증**

#### 한줄 요약
- 3대 위험 영역 분할과 레퍼런스 비교 평가로 안전성과 경제성의 최적 균형점을 도출한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **ALARP 3대 영역**: 불허용(운행 불가, 무조건 제거), ALARP(비용편익 저감 영역), 광범위 허용(잔여 위험 공식 수용).

</details>

```text
[ALARP 3대 위험 영역 및 GAMAB 비교 구조]
|-- 1. Intolerable Region (불허용 영역: 위험 극심, 어떤 비용으로도 용납 불가, 무조건 제거)
|-- 2. ALARP Region (합리적 저감 영역: 비용과 편익이 극단적 불균형이 아닌 한 위험 저감 필수)
|   `-- [GAMAB 원칙 적용] 신규 시스템의 위험도가 기존 레퍼런스 시스템 대비 동등 이하로 유지
`-- 3. Broadly Acceptable Region (광범위 허용 영역: 위험이 극히 미미하여 추가 대책 없이 수용)
```

선의 의미: 계층 및 상위 고위험부터 하위 잔여 위험 수용까지의 3단계 통제 구조

| 구성요소 | 책임 |
|:---|:---|
| GAMAB | 기존 시스템 대비 **동등 이상 안전 입증** |
| 불허용 영역 | 운행 중단과 **위험 원천 제거** |
| ALARP 영역 | 비용·편익이 합리적이면 **지속 저감** |
| 광범위 허용 영역 | 미미한 **잔여 위험 공식 수용** |

#### 한줄 요약
- 불허용, ALARP, 광범위 허용의 3대 영역으로 위험을 계층화하고 동등성을 입증한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **ISA(Independent Safety Assessor)**: 시스템 개발 조직과 완전히 독립되어 안전성 프로세스와 산출물을 제3자 입장에서 평가하는 공인 평가원.

</details>

```text
위험원 식별(Hazard Identification) 및 위험도 산정 (FMEA, FTA 분석)
        │
   [불허용 검사] 위험도가 Intolerable 영역인가? -> (예: 즉시 아키텍처 재설계 및 위험 제거)
        │ (아니오)
   [GAMAB 검사] 기존 운영 시스템 대비 동등 이상 안전한가? -> (미달 시 보완 조치)
        │
   [ALARP 저감] 추가 안전 장치(이중화, 소프트웨어 감시 타이머) 도입 비용편익 분석
        │
   추가 저감 비용이 얻는 안전 이익 대비 현저히 불균형(Gross Disproportion)한가?
   ┌────┴─────┐
  예           아니오 (합리적 비용)
   │             │
[저감 중단]    [추가 안전 대책 구현]
잔여 위험 수용  위험도 추가 강하
        │
   독립 안전 평가원(ISA)에게 Safety Case 제출 및 최종 안전 인증(Sign-off)
```

#### 한줄 요약
- 위험 식별 → GAMAB 동등성 검사 → ALARP 비용편익 분석 → 저감 대책 구현 → ISA 승인 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **GAMAB vs ALARP vs MEM**: 프랑스식 레퍼런스 동등성(GAMAB), 영국식 비용편익 저감(ALARP), 독일식 자연 사망률 기반 절대 기준(MEM).

</details>

| 비교 항목 | GAMAB (프랑스/철도 표준) | ALARP (영국/IEC 61508 표준) | MEM (독일/절대 안전 표준) |
|:---|:---|:---|:---|
| 안전 기준 관점 | **기존 레퍼런스 시스템 대비 상대적 동등성** | **비용 대 위험 저감 편익의 합리적 균형** | **인간 자연 사망률 기반 절대 수치 한계** |
| 판단 공식 | $\text{Risk}_{\text{New}} \le \text{Risk}_{\text{Old}}$ | $\text{Cost} / \Delta \text{Risk} \le \text{Disproportion Factor}$ | 사망 위험 $< 10^{-5} / \text{year}$ |
| 장점 | 기존 시스템 데이터 활용으로 입증 용이 | 경제성과 안전성의 현실적 최적화 | 가장 엄격하고 명확한 인명 보호 |
| 한계 | 혁신 신기술 적용 시 비교 대상 부재 | 불균형 판단 시 주관적 개입 가능 | 극단적 기준으로 개발 비용 천문학적 폭증 |

#### 한줄 요약
- 레퍼런스 비교는 GAMAB, 경제적 균형 저감은 ALARP, 절대 수치 제한은 MEM을 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **GSN(Goal Structuring Notation)**: 안전 목표(Goal), 전략(Strategy), 솔루션(Evidence) 간의 논리적 인과관계를 그래프로 시각화하는 표기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| ALARP 판단 시 비용 절감을 위한 주관적 위험 축소 | **독립 안전 평가원(ISA)의 제3자 검증 및 승인 의무화** | 안전 평가의 객관성 및 신뢰성 100% 확보 |
| 신기술(자율주행, AI) 적용 시 비교 레퍼런스 부재 | **IEC 61508 / ISO 26262 규격의 정량적 안전 등급(SIL/ASIL)으로 전환** | 표준 기반 정량적 안전 목표 수립 |
| 안전 증빙 문서 파편화로 인한 인증 실패 | **GSN(Goal Structuring Notation) 기반 정형화된 Safety Case 구축** | 논리적 안전성 입증 및 심사 기간 50% 단축 |
| 소프트웨어 단독 결함으로 인한 하드웨어 폭주 | **SW/HW 연계 결함 주입 테스트(Fault Injection) 수행** | Fail-Safe 안전 상태 전환 완벽 검증 |

#### 한줄 요약
- ISA 독립 평가, SIL/ASIL 표준 연계, GSN Safety Case 구축, 결함 주입 테스트로 안전성을 보증한다.

## Ⅶ. 결론

- 동등 안전성은 **GAMAB**, 합리적 저감은 **ALARP** 선택

#### 한줄 요약
- GAMAB과 ALARP는 절대적 제로 리스크가 불가능한 복잡계에서 공학적이고 합리적인 안전 기준선을 제시하는 핵심 안전 공학 원칙이다.
