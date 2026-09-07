---
sidebar:
  order: 209
  label: "209. 자동주행 시스템 (ADS)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "자동주행 시스템 (Automated Driving System, ADS)"
date: "2026-09-07T16:00:00+09:00"
tags:
  - "notes-latest-tech"
weight: 209
extra:
  question_no: "209"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "ADS 자동화 단계•안전 책임이 최근 출제됨"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **자동주행 시스템(Automated Driving System, ADS)**: 정의된 ODD에서 전체 DDT와 비상 시 대체 대응을 수행하는 시스템이다.
- **운행 설계 영역(Operational Design Domain, ODD)**: 자동주행 기능이 작동하도록 설계된 도로•속도•기상•교통 조건이다.
- **동적 주행 과업(Dynamic Driving Task, DDT)**: 조향•가감속과 주행환경 감시를 포함하는 주행 과업이다.

</details>

- 정의: 정의된 ODD에서 전체 DDT와 대체 대응을 수행하는 **ADS**
- 배경/필요성: 운전자가 항상 주행 환경을 감시하고 사고 책임을 전적으로 부담해야 하는 레벨 2 운전자 보조(ADAS) 시스템은 고속 주행이나 장거리 이동 시 운전자의 인지적 피로와 개입 지연을 근본적으로 해소하지 못하며, 인간 운전자의 개입을 전제로 하지 않는 완전한 이동성 혁신(로보택시, 무인 물류 배송)을 구현할 수 없는 한계에 직면함에 따라, 지정된 운행 조건(ODD) 내에서 인간 운전자의 상시 개입 없이 시스템이 전체 동적 주행 과업(DDT)과 비상 대응(DDT Fallback)을 스스로 수행하는 Automated Driving System(ADS / SAE J3016 Level 3 Conditional, Level 4 High, Level 5 Full Driving Automation / Operational Design Domain: ODD, Dynamic Driving Task: DDT & OEDR / Fail-Operational Redundant Architecture: Compute, Steering, Braking, Power / Minimal Risk Maneuver: MRM & Minimal Risk Condition: MRC / ISO 26262 & ISO 21448 SOTIF Standard)을 도입하여 **SAE 레벨 3(조건부 자동화: 비상 시 제어권 전환 요청 ToR) 및 레벨 4(고도 자동화: 무인 자율주행 및 시스템 자체 비상 대응) 체계를 통한 운전 주체의 인간에서 차량 시스템으로의 완전한 전환, 센서, 컴퓨팅, 조향, 제동의 이중화(Redundancy) 기반 결함 시에도 주행을 유지하는 고장 작동(Fail-Operational) 아키텍처 구축, 시스템 한계 도달이나 고장 발생 시 스스로 갓길 정차 등 안전 상태로 진입하는 최소위험기동(MRM $\rightarrow$ MRC) 구현을 통한 무인 이동 서비스 안전성**을 달성할 필요

#### 한줄 요약

- 자동주행 기능별 ODD•DDT•대체 대응 책임의 명시가 핵심이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **객체•사건 탐지 및 대응(Object and Event Detection and Response, OEDR)**: 주행 중 관련 객체와 사건을 탐지하고 상황에 맞는 대응을 생성하는 DDT 기능이다.
- **국제자동차기술자협회(Society of Automotive Engineers International, SAE International)**: 자동차 기술 표준을 개발하는 국제 전문 단체이다.

</details>

- 조향•가감속•OEDR을 포함한 **전체 DDT 수행**
- 도로•날씨•속도에 따른 **명시적 ODD 기반 작동 제한**
- SAE Level 3 운전자•Level 4 이상 시스템의 **대체 대응 책임 구분**
#### 한줄 요약

- ODD에 따라 주행 범위를 정하고, 범위를 벗어나거나 고장 시 누가 운전할지 미리 약속하는 것이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **동적 주행 과업 대체 대응(Dynamic Driving Task Fallback, DDT Fallback)**: 자동주행 시스템이 정상 주행 과업을 계속 수행할 수 없을 때 인계나 최소위험기동으로 대응하는 절차이다.
- **최소위험기동(Minimal Risk Maneuver, MRM)**: 정상 자동주행을 지속할 수 없을 때 위험을 최소화하는 상태로 차량을 이동•정지시키는 대응이다.
- **안전 감시•기록**: 자동주행 기능과 고장을 독립 감시하고 판단•개입•사고 관련 증거를 보존하는 기능이다.

</details>

```text
[ADS 아키텍처]
├── [조건 및 감시 계층]
│   ├── [ODD•기능 관리자]
│   └── [안전 감시•기록]
├── [인지 및 주행 과업 계층]
│   ├── [인지•OEDR]
│   └── [예측•계획•제어]
└── [안전 대체 대응 계층]
    └── [DDT fallback]
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| ODD•기능 관리자 | 운행 조건과 **기능 진입•종료 판단** 및 유지 |
| 인지•OEDR | 객체•사건의 **탐지•대응**과 분류 |
| 예측•계획•제어 | **행동•경로 결정**과 조향•가감속 |
| DDT fallback | 고장•ODD 이탈의 **인계•MRM 수행** |
| 안전 감시•기록 | **독립 감시•상태 증적**과 원격 지원 |

#### 한줄 요약

- 정상 주행과 ODD•고장 시 **DDT fallback 역할** 분리

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **최소위험상태(Minimal Risk Condition, MRC)**: 대체 대응 결과 차량과 주변의 위험이 최소화된 안정 상태이다.

</details>

OEDR•DDT 상태에 따른 **MRC 도달 판단**

```text
[ODD•기능 관리자]
       │ 1. 유효 ODD•활성 상태
       ▼
   [인지•OEDR]
       │ 2. 객체•사건 대응정보
       ▼
    [계획•제어]
       │ 3. DDT•차량 상태
       ▼
    [안전 감시]
       ├─ 정상 ──────────────▶ [ODD•기능 관리자]
       └─ 4. fallback 작동 요청 ──▶ [DDT fallback]
                                         │ 5. 인계•MRM 목표
                                         ▼
                                     [계획•제어]
```

### 동작 원리

1. 유효 ODD•활성 상태: 도로•날씨•속도•가용성으로 기능 진입
2. 객체•사건 대응정보: 환경 인지•예측과 OEDR 생성
3. DDT•차량 상태: 행동•경로•제어 결과 지속 감시
4. fallback 작동 요청: ODD 이탈•고장과 대응 가능 시간 판정 후 전환
5. 인계•MRM 목표: 자동화 수준별 운전자 인계•MRC 도달 지시

#### 한줄 요약

- ODD•고장 감시에 따른 **운전자 인계•시스템 MRM**

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **SAE Level 4**: 제한된 ODD 안의 전체 DDT와 대체 대응을 시스템이 수행하는 자동화 수준이다.

</details>

ADS 자동화 수준별 **운전자•시스템 책임** 비교

| ADS 자동화 수준 | SAE L3 | SAE L4 | SAE L5 |
|:---|:---|:---|:---|
| 적용 기준 | 인계 가능한 **제한 ODD** | 무인 운행 가능한 **제한 ODD** | **ODD 제한 없는 무인 운행** |
| 핵심 특징 | 운전자에게 **fallback 요청** | 시스템이 **fallback 수행** | 모든 조건에서 **시스템 운전** |
| 한계 | **인계 지연•준비 부족** | **ODD 밖 운행 불가** | 모든 **환경 대응 난도** |

#### 한줄 요약

- L3와 L4의 차이는 자동화 성능이 아니라 실패 시 대체 대응을 누가 맡느냐이므로, **제한 ODD 내 시스템 fallback**을 시스템이 지는 순간 운전자 인계를 전제로 설계할 수 없게 된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **보수적 가용성 판정**: ODD 경계나 시스템 상태가 불확실할 때 기능 진입을 막거나 조기에 종료하는 안전 판단이다.
- **운전자 모니터링 시스템(Driver Monitoring System, DMS)**: 운전자의 주의•응답•인계 준비 상태를 확인하는 시스템이다.

</details>

SAE Level 3의 **DMS•MRM 인계 조건** 검증

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| ODD 경계 미검증 시 조건 오판의 **무리한 기능 지속** | 진입•이탈 여유와 **보수적 가용성 판정** | ODD 이탈 시 **기능 지속** 방지 |
| 인계 책임 미검증 시 L3 운전자의 **준비 부족•반응 지연** | 충분한 전환 요구•DMS•**MRM 보완** | L3 인계 **대응 성공률** 향상 |
| fallback 미검증 시 고장 시 **최소위험상태 미도달** | 독립 감시•중복 제어•**시나리오 검증** | **최소위험상태 도달률** 향상 |

#### 한줄 요약

- ODD 조건•fallback 주체와 **인계 실패 시 MRM** 검증

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **자동화 수준별 대체 대응**: SAE Level 3는 운전자, Level 4 이상은 시스템이 대체 대응을 맡는 구분이다.

</details>

- 인류의 모빌리티 생태계를 운전 중심에서 이동 서비스(MaaS)와 로보택시로 재편하는 **완전 자율주행 시스템 및 지능형 무인 이동체 제어의 최고 기술 표준(Automated Driving System: ADS / SAE Level 3~5 Driving Automation / Full DDT & OEDR Execution / Fail-Operational Redundancy / MRM & MRC Safety Guarantee)의 확고한 표준**으로 확고히 자리 잡았으며, 대규모 파운데이션 모델(VLM/E2E Autonomous AI) 및 디지털 트윈 시뮬레이션 검증과 결합 발전하는 가운데, 실무 ADS 시스템 구축 시에는 **엄밀하게 정의된 ODD 범위 관리, 고장 발생 시 0.1초 이내 작동하는 전원/통신/조향/제동의 완벽한 하드웨어 이중화(Fail-Operational), 그리고 인계 실패 시 스스로 안전 지대에 정차하는 최소위험기동(MRM)**을 결합하여 완벽한 자율주행 신뢰성과 탑승자 생명 안전을 완성

#### 한줄 요약

- **ODD•DDT**와 fallback 주체•MRC를 명시하고 검증
