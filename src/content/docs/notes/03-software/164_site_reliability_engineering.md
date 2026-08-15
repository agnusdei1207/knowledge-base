---
sidebar:
  order: 164
  label: "164. SRE 사이트 신뢰성 공학 (Site Reliability Engineering)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "SRE 사이트 신뢰성 공학 (Site Reliability Engineering)"
date: "2026-08-14T02:48:00+09:00"
tags:
  - "notes-software"
weight: 164
extra:
  question_no: "164"
  source_status: "기출"
  source_history: "137회"
  priority: 70
  priority_note: "신뢰성 목표와 운영 자동화의 연결 구조 출제"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **SRE (Site Reliability Engineering)**: 구글(Google)이 창안한 모델로, 소프트웨어 공학(개발) 방법론을 IT 인프라 운영(Ops) 문제에 적용하여 시스템 신뢰성과 확장성을 달성하는 실천적 엔지니어링 체계.
- **SLO (Service Level Objective)**: 고객과 약속한 가용성 목표치(예: 월간 성공률 99.9%). SLA(계약)를 지키기 위해 내부적으로 설정하는 척도.
- **Error Budget (오류 예산)**: 100%에서 SLO를 뺀 나머지 공간(예: 100% - 99.9% = 0.1% 허용 실패율)으로, 이 예산이 남아있으면 신규 배포를 허용하고 고갈되면 배포를 동결하는 기준.
- **Toil (토일)**: 운영 업무 중 수작업으로 반복되고, 자동화 가능하며, 서비스 성장에 비례해 선형적으로 증가하는 "가치 없는 노가다"성 운영 부하.

</details>

- 정의/개념: Software Engineering으로 신뢰성을 운영하는 **SRE**
- 배경/필요성: 변경 속도와 안정성 목표의 충돌을 **정량 기준** 없이 조정 곤란

#### 한줄 요약

- 무조건 장애를 없애려는 대신 사용자가 허용할 실패량을 정하고 남은 여유에 따라 기능 배포와 안정화 작업의 순서를 바꾼다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Blameless Post-Mortem (비난 없는 사후 분석)**: 장애 발생 시 "누가" 잘못했는지가 아니라, "어떤 시스템적 허점"이 장애를 유발했는지 집중하여 재발 방지책을 도출하는 SRE 핵심 문화.

</details>

- **Operations as Software Engineering (운영의 소프트웨어 공학화 및 Toil 자동화)**
- **Data-Driven Reliability (SLI/SLO 기반 서비스 수준 정량화 측정)**
- **Error Budgeting (개발 속도와 시스템 안정성 간의 수학적 합의 기준 마련)**

#### 한줄 요약

- 서버 한 대의 CPU가 아니라 결제 성공률과 지연을 보고 약속 위반 속도가 빨라지면 새 배포보다 복구와 재발 방지를 먼저 수행한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SLI (Service Level Indicator)**: 사용자 관점에서 실제 측정된 서비스 지표(예: 최근 5분간 HTTP 200 OK 응답 비율 99.95%).

</details>

```text
[SRE]
 ├── [SLI]
 ├── [SLO]
 ├── [Error Budget]
 ├── [Toil Automation]
 └── [Blameless Postmortem]
```

| 구성요소 | 책임 |
|---|---|
| SLI | 사용자 관점의 **품질 측정값** 정의 |
| SLO | 기간별 **신뢰성 목표** 설정 |
| Error Budget | 허용 실패량과 **변경 판단 여유** 제공 |
| Toil Automation | 반복 수작업을 **Software로 제거** |
| Blameless Postmortem | 장애의 **System 원인•재발 방지** 도출 |

#### 한줄 요약

- SLO가 약속, 오류 예산이 남은 실패 쿠폰, 경보가 사용 알림, 온콜이 긴급 대응, 자동화가 같은 사고를 줄이는 개선 장치다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Burn Rate (예산 소진율)**: 한 달 치 Error Budget(43분)이 특정 장애로 인해 얼마나 빠르게 소모되고 있는지를 나타내는 속도 지표.

</details>

```text
[변경 요청]
    │
    ▼
1. SLI 측정
    │
    ▼
2. SLO 대비 Error Budget 계산
    │
    ▼
3. Burn Rate 평가
 ┌──┴────────────┐
 │ 정상          │ 초과
4. 변경 우선순위 결정
 │ 변경 진행     │ 복구 우선
 └──┬────────────┘
5. 결정 실행•결과 측정
    │
    ▼
[운영 결정 반환]
```

### 동작 원리

1. **SLI 측정**: 성공률•지연 등 사용자 품질 계산
2. **SLO 대비 Error Budget 계산**: 기간 내 허용 실패량 산출
3. **Burn Rate 평가**: 단기•장기 예산 소진 속도 비교
4. **변경 우선순위 결정**: 여유면 배포, 초과면 복구 우선
5. **결정 실행•결과 측정**: 효과와 예산 정책 보정

#### 한줄 요약

- 결제 실패가 오류 예산을 빠르게 소비하면 배포 시스템이 변경을 제한하고 온콜은 롤백으로 사용자의 피해부터 줄인다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Class SRE Implements DevOps**: "SRE는 DevOps라는 철학을 구현하는 구체적인 실천(Class) 방법론이다"라는 구글의 정의.

</details>

| 비교 항목 | DevOps (데브옵스) | SRE (사이트 신뢰성 공학) |
|:---|:---|:---|
| **포지셔닝** | **문화적 철학 및 개발/운영의 사일로 타파** | **DevOps 철학을 구현하는 엔지니어링 직무**|
| **장벽 제거 방법** | **CI/CD 파이프라인 및 소통 강조** | **SLO 및 Error Budget이라는 수학적 잣대 사용**|
| **실패에 대한 태도**| "실패를 두려워 말고 빨리 실패하라" | **"Error Budget 한도 내에서 통제된 실패만 허용"**|
| **핵심 결과물** | 배포 속도 향상 (Time to Market) | **안정성 유지 속 배포 극대화 (Reliability)** |

#### 한줄 요약

- SRE는 장비가 켜졌는지가 아니라 사용자가 약속한 성공률과 지연을 받았는지로 변경 가능 여부를 판단한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Alert Fatigue (경고 피로)**: 너무 사소한 CPU 80% 알람이 수천 개씩 쏟아져 온콜(On-Call) 엔지니어가 중요한 진짜 장애 알림을 무시하게 되는 현상.

</details>

| 3대 SRE 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Alert Fatigue** | CPU/RAM 튀었다고 무의미한 슬랙 알림 남발 | **SLI/SLO 기반 Error Budget 소진 알람으로 통합** |
| **2. Toil Overload** | SRE 팀이 배포/권한 부여 노가다만 하고 있음| **SRE 직무의 Toil 비중을 50% 이하로 상한 규정**|
| **3. Blaming Culture** | 장애 시 개발팀/운영팀 서로 범인 찾기 | **비난 없는 Post-Mortem(사후 회고) 문서 제도화** |

> 사례: **토스 / 당근마켓 SRE 팀의 Toil 감소 Terraform IaC 및 Datadog SLO 기반 경보 도입**

#### 한줄 요약

- 월간 목표만 보면 짧고 큰 장애를 늦게 찾을 수 있으므로 한 시간과 한 달의 소진율을 함께 보고 빠른 사고와 누적 악화를 나눠 대응한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **SRE 수립 기준(SRE Standards)**: SLI/SLO 정의, Error Budget 배포 통제, Toil 50% Rule 및 Blameless Postmortem에 의거한 체계.

</details>

- 예산 여유는 **변경 진행**, Burn Rate 초과는 복구•자동화 우선

#### 한줄 요약

- 오류 예산에 여유가 있으면 변경을 진행하고 빠르게 소진되면 배포를 줄여 복구와 토일 자동화에 먼저 투자해야 한다.
