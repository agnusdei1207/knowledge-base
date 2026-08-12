---
sidebar:
  order: 164
  label: "164. SRE 사이트 신뢰성 공학 (Site Reliability Engineering)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "SRE 사이트 신뢰성 공학 (Site Reliability Engineering)"
date: "2026-08-06T23:27:50+09:00"
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

<details><summary>핵심 용어</summary>

- **SRE (Site Reliability Engineering)**: 구글(Google)이 창안한 모델로, 소프트웨어 공학(개발) 방법론을 IT 인프라 운영(Ops) 문제에 적용하여 시스템 신뢰성과 확장성을 달성하는 실천적 엔지니어링 체계.
- **SLO (Service Level Objective)**: 고객과 약속한 가용성 목표치(예: 월간 성공률 99.9%). SLA(계약)를 지키기 위해 내부적으로 설정하는 척도.
- **Error Budget (오류 예산)**: 100%에서 SLO를 뺀 나머지 공간(예: 100% - 99.9% = 0.1% 허용 실패율)으로, 이 예산이 남아있으면 신규 배포를 허용하고 고갈되면 배포를 동결하는 기준.
- **Toil (토일)**: 운영 업무 중 수작업으로 반복되고, 자동화 가능하며, 서비스 성장에 비례해 선형적으로 증가하는 "가치 없는 노가다"성 운영 부하.

</details>

- 정의/개념: 인프라 운영 작업을 소프트웨어 개발 관점으로 접근하여 시스템 신뢰성(Reliability)을 수치화하고 Toil(수작업)을 자동화로 제거하는 구글의 DevOps 구현 방법론인 **SRE**
- 배경/필요성: 개발팀(Agile 배포 속도)과 운영팀(안정성 유지) 간의 사일로(Silo) 대립을 극복하고, 무조건적인 무장애주의가 아닌 비즈니스 타협점(Error Budget)을 찾으려는 조직적 요구성

#### 한줄 요약

- 무조건 장애를 없애려는 대신 사용자가 허용할 실패량을 정하고 남은 여유에 따라 기능 배포와 안정화 작업의 순서를 바꾼다.

## Ⅱ. 특징 (SRE 3대 핵심 철학)

<details><summary>핵심 용어</summary>

- **Blameless Post-Mortem (비난 없는 사후 분석)**: 장애 발생 시 "누가" 잘못했는지가 아니라, "어떤 시스템적 허점"이 장애를 유발했는지 집중하여 재발 방지책을 도출하는 SRE 핵심 문화.

</details>

- **Operations as Software Engineering (운영의 소프트웨어 공학화 및 Toil 자동화)**
- **Data-Driven Reliability (SLI/SLO 기반 서비스 수준 정량화 측정)**
- **Error Budgeting (개발 속도와 시스템 안정성 간의 수학적 합의 기준 마련)**

#### 한줄 요약

- 서버 한 대의 CPU가 아니라 결제 성공률과 지연을 보고 약속 위반 속도가 빨라지면 새 배포보다 복구와 재발 방지를 먼저 수행한다.

## Ⅲ. 구조 및 구성요소 (SRE 5대 실천 프레임워크)

<details><summary>핵심 용어</summary>

- **SLI (Service Level Indicator)**: 사용자 관점에서 실제 측정된 서비스 지표(예: 최근 5분간 HTTP 200 OK 응답 비율 99.95%).

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   SRE (Site Reliability Engineering) Model             │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Define (정의) : [SLI (측정 지표)] ──► [SLO (목표치 99.9%)]          │
│ 2. Budget (예산) : [Error Budget (0.1%)] ──► [배포 속도(Velocity) 결정]│
│ 3. Ops (운영)    : [Toil 50% 미만 제한] ──► [나머지 50%는 자동화 개발] │
│ 4. Detect (탐지) : [Observability (OTel/Prometheus) 기반 모니터링]     │
│ 5. Review (회고) : [Blameless Postmortem (근본 원인 Action Item 도출)] │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: SLI로 현황을 측정해 SLO 달성 여부를 보고 Error Budget에 따라 배포 밸브를 열거나 잠그며, 나머지 시간은 Toil 감축 개발에 투자하는 구조.

| SRE 핵심 구성요소 | 역할 및 정의 | 실무 예시 |
|:---|:---|:---|
| **SLI (지표)** | **실제 사용자 경험 기준 서비스 품질 측정값** | 성공한 HTTP 요청 / 전체 요청 수 |
| **SLO (목표)** | **SLI가 달성해야 할 내부 목표 타겟치** | 월간 SLI 99.9% 유지 |
| **Error Budget**| **SLO에 의해 허용되는 월간 장애 허용 시간**| 월간 43분 다운타임 허용 |
| **Toil 자동화** | **반복적인 수동 운영 업무를 스크립트로 제거** | 서버 재시작 자동화 (Terraform) |
| **Post-Mortem** | **장애 후 비난 없이 시스템적 원인 파악 및 개선**| Five Whys 분석 회고 문서화 |

#### 한줄 요약

- SLO가 약속, 오류 예산이 남은 실패 쿠폰, 경보가 사용 알림, 온콜이 긴급 대응, 자동화가 같은 사고를 줄이는 개선 장치다.

## Ⅳ. 흐름도 (Error Budget 기반 배포 파이프라인 흐름)

<details><summary>핵심 용어</summary>

- **Burn Rate (예산 소진율)**: 한 달 치 Error Budget(43분)이 특정 장애로 인해 얼마나 빠르게 소모되고 있는지를 나타내는 속도 지표.

</details>

```text
[New Feature Release Request]
             │
             ▼
[Calculate Current Error Budget]
             │
   ┌─────────┴─────────┐
   ▼                   ▼
[Budget 남아있음]   [Budget 모두 소진됨]
   │                   │
   ▼                   ▼
[배포 승인 (Go)]    [신규 피처 배포 전면 중단 (Freeze)]
                       │
                       ▼
            [안정성 개선 및 버그 수정(Toil 감축)에 100% 리소스 투입]
```

### 동작 원리

1. **SLO Measurement**: Prometheus가 실시간 SLI(성공률 99.95%)를 계측.
2. **Budget Check**: 이번 달 허용치(0.1%) 중 0.05%를 써서 아직 예산이 남았는지 확인.
3. **Decision Making**: 예산이 남았으므로 신규 서비스 배포를 승인 진행, 만약 예산이 바닥났다면 배포를 즉각 멈추고 서버 안정화 작업(SRE)에만 전념 (**SRE 합의 완결**).

#### 한줄 요약

- 결제 실패가 오류 예산을 빠르게 소비하면 배포 시스템이 변경을 제한하고 온콜은 롤백으로 사용자의 피해부터 줄인다.

## Ⅴ. 종류 및 비교 (DevOps 대 SRE 1:1 비교)

<details><summary>핵심 용어</summary>

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

## Ⅵ. 실무 고려사항 및 대책 (SRE 3대 실무 난제 대책)

<details><summary>핵심 용어</summary>

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

<details><summary>핵심 용어</summary>

- **SRE 수립 기준(SRE Standards)**: SLI/SLO 정의, Error Budget 배포 통제, Toil 50% Rule 및 Blameless Postmortem에 의거한 체계.

</details>

- **SRE 수립 기준**에 따라 Cloud-Native MSA 전환 시 **DevOps 조직 내 SRE 프랙티스(SLO/Error Budget)** 필수 적용

#### 한줄 요약

- 오류 예산에 여유가 있으면 변경을 진행하고 빠르게 소진되면 배포를 줄여 복구와 토일 자동화에 먼저 투자해야 한다.
