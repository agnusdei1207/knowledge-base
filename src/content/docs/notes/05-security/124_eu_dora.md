---
sidebar:
  order: 124
  label: "124. EU DORA (디지털 운영 복원력 법)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "EU DORA (디지털 운영 복원력 법)"
date: "2026-08-02T23:54:00+09:00"
tags:
  - "notes-security"
weight: 124
extra:
  question_no: "124"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "138회 최신 규정이며 운영복원력·제3자 위험이 중요함"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **디지털 운영 복원력 법(Digital Operational Resilience Act, DORA)**: 유럽연합(European Union, EU) 금융 부문의 정보통신기술(Information and Communication Technology, ICT) 위험·사고 보고·복원력 시험·제3자 위험관리를 통합한 규정이다.

</details>

- 정의/개념: EU 금융 부문의 ICT 위험·사고·시험·제3자를 통합 관리하는 **운영 복원력 규정**
- 배경/필요성: 분절된 금융 ICT 규제로는 공급자 집중 장애의 **연쇄 피해 통제 곤란**

#### 한줄 요약

- 금융기관이 내부 시스템과 외부 ICT 공급자의 장애를 함께 견디고 복구하도록 정한 규칙임

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **정보통신기술 위험(Information and Communication Technology Risk, ICT 위험)**: 기술 장애·오류·공격이 금융 서비스에 손실을 일으킬 가능성이다.
- **중대 ICT 사고**: 서비스·고객·거래에 중대한 영향을 주어 보고해야 하는 정보통신기술 사고이다.
- **중요 정보통신기술 제3자 제공자(Critical ICT Third-Party Provider, CTPP)**: 유럽연합(European Union, EU) 금융 안정성에 중요한 서비스를 제공해 직접 감독을 받는 공급자이다.

</details>

- 경영기구 최종 책임의 **ICT 위험 거버넌스**
- 사고 보고·복원력 시험의 **EU 단일 체계**
- 계약 통제·CTPP 감독의 **제3자 위험관리**

#### 한줄 요약

- 보안 통제뿐 아니라 장애 중 중요 금융 서비스가 계속되는지를 경영진이 책임짐

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **위협 주도 침투시험(Threat-Led Penetration Testing, TLPT)**: 실제 위협정보와 전술로 중요 기능의 방어·복구를 검증하는 시험이다.
- **정보통신기술(Information and Communication Technology, ICT) 위험관리**: 기술 자산과 의존성을 식별하고 보호·탐지·대응·복구하는 관리 활동이다.
- **종료 전략**: 공급자 장애·계약 종료 시 중요 서비스를 이전·복구하는 계획이다.

</details>

```mermaid
block-beta
  columns 3
  R["ICT 위험관리"]
  I["ICT 사고관리·보고"]
  T["운영 복원력 시험"]
  P["ICT 제3자 위험관리"]
  S["사이버위협 정보공유"]
  R --- I --- T
  T --- P --- S
```

| 구성요소 | 책임 |
|:---|:---|
| ICT 위험관리 | **식별·보호·탐지·대응·복구** |
| ICT 사고관리·보고 | **분류·초기·중간·최종 보고** |
| 운영 복원력 시험 | 기본 시험과 중요 기능 **TLPT** |
| ICT 제3자 위험관리 | **계약·집중·종료 전략** 통제 |
| 사이버위협 정보공유 | 신뢰 공동체 내 **자발적 공유** |

#### 한줄 요약

- 내부 통제, 사고 보고, 시험, 공급자 관리, 위협정보 공유를 하나의 복원력 체계로 묶음

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **집중 위험**: 다수 금융기관의 소수 공급자 의존으로 단일 장애가 확산할 위험이다.
- **ICT·TLPT 판단**: 정보통신기술(Information and Communication Technology, ICT) 의존성과 위협 주도 침투시험(Threat-Led Penetration Testing, TLPT) 결과를 감독 증거로 연결하는 기준이다.

</details>

```mermaid
sequenceDiagram
  participant B as 경영기구
  participant R as 위험관리
  participant O as 금융 운영
  participant P as ICT 공급자
  participant A as 감독기관
  B->>R: 1. 적용 범위·위험 허용수준
  R->>O: 2. 중요 기능·ICT 의존성
  O->>P: 3. 계약 통제·종료 요구
  O->>A: 4. 중대 사고·TLPT 증거
  A->>B: 5. 감독 권고·개선 요구
```

**동작 원리**

1. **적용 범위·위험 허용수준**: 법인·경영기구 책임과 허용 가능한 ICT 위험 제공
2. **중요 기능·ICT 의존성**: 자산·공급자·집중 위험의 분석 결과 전달
3. **계약 통제·종료 요구**: 보안·복구·감사권·대체수단 조건 제공
4. **중대 사고·TLPT 증거**: 사고 분류·보고와 중요 기능 시험 결과 제출
5. **감독 권고·개선 요구**: 시험·감독 결함과 이행 기한 제공

#### 한줄 요약

- 중요 기능과 공급자 의존성을 먼저 파악하고 사고·시험·감독 결과를 경영진 통제에 되돌림

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **중요 정보통신기술 제3자 제공자(Critical ICT Third-Party Provider, CTPP)**: 유럽연합(European Union, EU) 금융 안정성에 중요해 직접 감독을 받는 정보통신기술 공급자이다.
- **디지털 운영 복원력 법(Digital Operational Resilience Act, DORA)**: 금융기관의 위험·사고·시험 의무와 공급자 감독을 규정한다.

</details>

| 적용 주체 | DORA상 위치 | 핵심 의무·통제 |
|:---|:---|:---|
| **금융기관** | 디지털 운영 복원력 법(Digital Operational Resilience Act, DORA)의 **직접 의무 주체** | 정보통신기술 위험·사고 보고·복원력 시험·제3자 관리 |
| **일반 정보통신기술 공급자** | 금융기관의 **계약·실사 대상** | 감사권·복구·재위탁·종료 조건 수용 |
| **중요 정보통신기술 제3자 제공자(Critical ICT Third-Party Provider, CTPP)** | 유럽연합이 지정한 **중요 공급자** | 계약 통제와 주관 감독자의 직접 감독 |

> 요약: 금융기관 직접 의무와 중요 공급자 감독을 결합함

#### 한줄 요약

- 금융기관은 DORA 의무를 직접 이행하고 CTPP는 계약 통제에 더해 EU 감독도 받음

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **유럽연합 규정(Regulation of the European Union, Regulation (EU)) 2022/2554**: 디지털 운영 복원력 법(Digital Operational Resilience Act, DORA)의 정식 법령으로 2025년 1월 17일부터 적용된다.
- **주관 감독자**: 중요 정보통신기술 제3자 제공자(Critical ICT Third-Party Provider, CTPP)의 위험 평가·검사·권고 이행을 총괄하는 유럽 감독기관이다.
- **위협 주도 침투시험(Threat-Led Penetration Testing, TLPT)**: 중요 금융 기능을 실제 위협 시나리오로 공격해 방어·복구 능력을 검증하는 시험이다.
- **정보통신기술(Information and Communication Technology, ICT) 공급자 집중**: 소수 기술 공급자의 장애가 금융권 전체로 확산할 수 있는 의존 위험이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 적용 범위·시점을 놓치면 법정 의무 이행 지연 | **Regulation (EU) 2022/2554** 적용 | 2025-01-17부터 **법정 의무 준수** |
| 중요 기능의 실전 공격·복구 검증이 부족 | **DORA 제26조 TLPT** 수행 | 실운영 기반 **방어·복구 역량** 검증 |
| 소수 ICT 공급자 집중으로 장애가 금융권에 확산 | **DORA 제28~44조** 통제 | **계약·감독·종료 전략** 확보 |

#### 한줄 요약

- 중요 금융 기능은 실제 위협 기반 TLPT로 검증하고 공급자별 계약 목록·집중도·대체 가능성·종료 계획을 함께 관리한다.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **운영 복원력**: 내부 시스템과 외부 공급자의 장애 중에도 중요 금융 서비스를 지속·복구하는 능력이다.
- **DORA·CTPP 감독**: 디지털 운영 복원력 법(Digital Operational Resilience Act, DORA)의 금융기관 직접 의무와 중요 정보통신기술 제3자 제공자(Critical ICT Third-Party Provider, CTPP)에 대한 유럽연합(European Union, EU) 감독을 구분하는 기준이다.

</details>

- 금융기관은 **DORA 직접 의무**, CTPP는 EU 직접 감독, 일반 공급자는 계약 통제 적용

#### 한줄 요약

- 내부 보안과 공급자 계약을 따로 보지 않고 금융 서비스의 지속성이라는 하나의 결과로 관리함
