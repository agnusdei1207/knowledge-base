---
sidebar:
  order: 112
  label: "112. 정보보호 거버넌스 (Information Security Governance)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "정보보호 거버넌스 (Information Security Governance)"
date: "2026-08-13T21:46:00+09:00"
tags:
  - "notes-security"
weight: 112
extra:
  question_no: "112"
  source_status: "기출"
  source_history: "120회"
  priority: 50
  priority_note: "120회 기출이며 위험•책임•성과 정렬의 상위축임"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **정보보호 거버넌스(Information Security Governance)**: 조직의 비즈니스 목적에 부합하도록 정보보호 전략, 투자, 위험 관리를 감독하는 의사결정 체계.

</details>

- 정의/개념: **정보보호 거버넌스**는 경영진이 사업 목표와 위험수용 기준에 따라 보안을 평가•지시•감시하고 책임•성과를 소통하는 의사결정 체계.
- 배경/필요성: 보안 조직의 통제 운영만으로는 사업 위험의 수용•투자 책임을 결정하기 어려움.

#### 한줄 요약

- 경영진이 보안 위험을 어디까지 감수하고 어디에 투자할지 정한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **위험 허용 수준(Risk Tolerance Level)**: 사업 목적 달성을 위해 조직이 수용할 수 있는 최고 수준의 위험 한계.
- **독립 보증(Independent Assurance)**: 보안 관리 조직과 독립된 감사 주체가 통제의 적합성과 유효성을 검증하는 활동.

</details>

- 사업 목표•법적 요구를 보안 전략에 연결.
- 승인•실행•감사의 책임과 권한 분리.
- **위험 허용 수준**을 경영진이 승인하고 **독립 보증**으로 결과 확인.

#### 한줄 요약

- 실무팀이 통제를 운영해도 사업 위험의 수용 책임은 경영진에게 있다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **평가(Evaluate)**: 사업 환경, 위협 및 정보보호 전략의 적정성을 종합적으로 분석하는 활동.
- **지시(Direct)**: 최고경영진이 정보보호 정책, 자원 배분 및 책임을 결정하여 하달하는 활동.
- **감시(Monitor)**: 정보보호 성과, 준수 상태 및 침해 위험을 지속적으로 모니터링하는 활동.
- **소통(Communicate)**: 정보보호 위험, 투자 성과 및 의사결정 사항을 이해관계자에게 보고하는 활동.

</details>

```text
정보보호 거버넌스
├─ 방향 · 전략
│  └─ 사업 목표 · 위험 허용 수준
├─ 책임 · 권한 구조
│  └─ 승인 · 실행 · 감사 권한
├─ 정책 · 위험 기준
│  └─ 경영 방향 · 수용 한계
├─ 위험 · 자원 의사결정
│  └─ 처리 · 예외 · 투자 우선순위
└─ 성과 · 독립 보증
   └─ 지표 · 감사 · 준수 확인
```

| 구성요소 | 책임 |
|:---|:---|
| 방향•전략 | **평가** 결과에 따라 사업 목표•위험 허용 수준 연결 |
| 책임•권한 구조 | **지시**로 승인•실행•감사 권한 분리 |
| 정책•위험 기준 | 경영 방향•수용 한계 구체화 |
| 위험•자원 의사결정 | 처리•예외•투자 우선순위 승인 |
| 성과•독립 보증 | **감시**와 **소통**으로 효과•준수 확인 |

#### 한줄 요약

- 경영진이 방향과 책임을 정하고 독립 감사로 실행 결과를 확인한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **위험 소유자(Risk Owner)**: 담당 업무의 위험 수준을 판단하고 위험 처리 및 수용 여부를 최종 승인하는 책임자.
- **최고정보보호책임자(Chief Information Security Officer, CISO)**: 전사 정보보호 전략 수립, 위험 관리 및 보안 통제를 총괄하는 임원급 책임자.
- **사업•보안 위험 평가(Business and Security Risk Evaluation)**: 사업 목표와 법적 규제를 분석하여 경영진 심의 대상 위험을 정의하는 단계.
- **방향•위험 허용 수준 승인(Governance Direction and Tolerance Approval)**: 정보보호 목표, 예산 및 위험 허용 한도를 경영진이 의결하는 단계.
- **처리•예산•책임 배정(Treatment, Budget and Responsibility Assignment)**: 위험 소유자 및 CISO에게 통제 이행 자원과 책임을 배정하는 단계.
- **성과•준수 증적 생성(Performance and Compliance Evidence Generation)**: 보안 통제 이행 내역 및 준수 상태 증적을 생성하는 단계.
- **개선 방향•우선순위 결정(Improvement Direction and Priority Setting)**: 감사 및 성과 측정 결과를 바탕으로 전략과 투자를 재조정하는 단계.

</details>

```text
1. 사업•보안 위험 평가
             │
             ▼
2. 방향•위험 허용 수준 승인
             │
             ▼
3. 처리•예산•책임 배정
             │
             ▼
4. 성과•준수 증적 생성
             │
        독립 보증 보고
             ▼
5. 개선 방향•우선순위 결정
             │
             └──── 전략 · 투자 조정 ────┐
                                        └─ 위험 평가로 환류
```

### 동작 원리

1. **사업·보안 위험 평가**: 사업 영향·법적 요구 평가
2. **방향·위험 허용 수준 승인**: 목표·수용 한계 승인
3. **처리·예산·책임 배정**: 통제·자원·담당 배정
4. **성과·준수 증적 생성**: 효과·준수 근거 기록
5. **개선 방향·우선순위 결정**: 전략·투자 조정

#### 한줄 요약

- 위험 보고가 경영진의 투자 승인과 개선 지시로 이어진다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **거버넌스(Governance)**: 최고경영진 관점에서 위험 수용, 투자 및 방향을 결정하고 성과를 감시하는 활동.
- **관리(Management)**: 거버넌스 방향에 따라 보안 통제를 계획, 수립, 운영, 측정하는 실행 활동.

</details>

| 운영축 | 책임 | 산출•환류 |
|:---|:---|:---|
| 거버넌스 | 위험•투자•책임의 방향 승인과 감독 | 목표•위험 선호•책임자 결정 후 성과 감시 |
| 관리 | 통제 계획•구축•운영•점검 | 실행 결과와 잔여 위험을 거버넌스에 보고 |

#### 한줄 요약

- 거버넌스가 방향과 책임을 정하면 관리조직이 통제를 실행한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **ISO(International Organization for Standardization)**: 국제 표준을 개발•발행하는 국제 기구.
- **IEC(International Electrotechnical Commission)**: 전기•전자 분야 국제 표준을 개발하는 협력 기구.
- **ISO/IEC 27014(Information Security Governance, ISO 27014)**: 정보보호 거버넌스의 평가, 지시, 감시, 소통 지침을 제공하는 국제 규격.
- **정보와 기술(Information and Technology, I&T)**: 기업의 비즈니스 가치 창출을 위해 활용되는 정보 자산과 IT 인프라.
- **정보 및 관련 기술 통제 목표(Control Objectives for Information and Related Technologies, COBIT)**: Enterprise IT 거버넌스와 관리를 표준화한 프레임워크.
- **정보시스템감사통제협회(Information Systems Audit and Control Association, ISACA)**: COBIT 개발 및 IT 거버넌스 전문 자격을 관리하는 국제 협회.
- **평가•지시•감시(Evaluate, Direct and Monitor, EDM)**: COBIT 거버넌스 도메인의 5개 세부 프로세스로 구성된 핵심 영역.
- **미국 국립표준기술연구소(National Institute of Standards and Technology, NIST)**: 사이버보안 및 기술 가이드를 발행하는 미국 정부 기관.
- **사이버보안 프레임워크(Cybersecurity Framework, CSF)**: 사이버 위험 관리 성과를 공유 언어로 체계화한 프레임워크.
- **Govern(Govern Domain)**: NIST CSF 2.0에서 조직의 위험 관리 전략과 책임 거버넌스를 명시한 도메인.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 보안 거버넌스 절차 | **ISO**와 **IEC**의 **ISO/IEC 27014** 적용 | 평가•지시•감시 정렬 |
| **I&T** 책임 분리 | **ISACA**의 **COBIT**과 **EDM** 연계 | 거버넌스•관리 구분 |
| 사이버 위험 거버넌스 | **NIST** **CSF**의 **Govern** 활용 | 전사 위험관리 연계 |

#### 한줄 요약

- 이사회는 보안 도구 수가 아니라 핵심 업무 위험과 예상 감소 효과•비용•잔여위험을 검토해 투자와 위험 수용을 승인한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **추적 가능한 위험 수용(Traceable Risk Acceptance)**: 잔여위험의 수용 근거 및 승인 주체를 문서 기록으로 보존하는 원칙.

</details>

- **추적 가능한 위험 수용**을 위해 위험 수용•투자는 **거버넌스**, 통제 계획•운영은 **관리**, 효과 확인은 **독립 보증**으로 구별 및 관리.

#### 한줄 요약

- 사고 전에 누가 위험을 수용했는지 추적할 수 있어야 한다.
