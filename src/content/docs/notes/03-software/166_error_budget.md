---
sidebar:
  order: 166
  label: "166. 오류 예산 (Error Budget)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "오류 예산 (Error Budget)"
date: "2026-08-14T02:56:00+09:00"
tags:
  - "notes-software"
weight: 166
extra:
  question_no: "166"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "신뢰성 목표와 변경 속도의 운영 판단 출제"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Error Budget (오류 예산)**: 100% 가용성에서 조직이 목표로 합의한 SLO(Service Level Objective)를 뺀 수치로, 한 달 동안 합법적으로 허용된 서비스 중단 가능 시간.
- **Velocity vs Reliability Trade-off**: 기능 배포 속도(Velocity)와 서비스 신뢰성(Reliability) 사이에서 SRE 조직이 Error Budget을 잣대로 우선순위를 통제하는 합의 기제.
- **Budget Depletion (예산 소진)**: 월간 오류 예산(예: 43분)이 전액 소진될 경우, 신규 배포를 동결(Code Freeze)하고 신뢰성 안정화 및 Toil 제거 개발에만 집중하는 정책.

</details>

- 정의/개념: SLO가 허용하는 실패량인 **Error Budget**
- 배경/필요성: 무장애 목표는 **신뢰성 비용•변경 속도**의 합리적 절충 불가

#### 한줄 요약

- 한 달에 허용할 실패 쿠폰을 정해 두고 빠르게 소비되면 새 기능보다 복구를 먼저 선택하는 운영 기준이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Burn Rate (예산 소진율)**: 남은 오류 예산이 평소 대비 몇 배속으로 고갈되고 있는지를 계산하여, 1시간 뒤 예산 파산이 예상되면 즉시 Page(온콜 알림)를 발생시키는 지표.

</details>

![가용성 SLO가 높아질수록 줄어드는 월간 오류 예산](/study/diagrams/slo-error-budget.svg)

> 파란 선은 30일을 가정할 때 99.9% SLO가 약 43.2분의 중단을 허용하며 SLO가 높아질수록 오류 예산이 급격히 작아지는 관계를 나타낸다.

- **Objective Metric (SLO 기반 월간 최대 장애 허용 시간 43.2분 명문화)**
- **Feature Release Valve (예산 잔여 시 배포 자유화, 예산 고갈 시 배포 전면 동결)**
- **Burn Rate Alerting (단기/장기 예산 소진 속도 기반 예측적 장애 온콜 발생)**

#### 한줄 요약

- 남은 실패량만 보면 짧은 대형 장애를 늦게 알 수 있으므로 현재 소비 속도까지 함께 봐야 평가 기간이 끝나기 전에 목표 위반을 막을 수 있다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Rolling Window (이동 구간)**: 달력 기준 1일~말일이 아닌, "최근 30일" 등 이동하는 기간 슬라이딩 윈도우 방식으로 Error Budget 복원력을 계산하는 기법.

</details>

```text
[Error Budget Policy]
 ├── [SLO]
 ├── [Error Budget]
 ├── [Burn Rate]
 └── [Consequence]
```

| 구성요소 | 책임 |
|---|---|
| SLO | 기간별 **허용 품질 목표** 정의 |
| Error Budget | 목표 밖에서 허용할 **실패량** 산출 |
| Burn Rate | 실제 오류율의 **예산 소비 속도** 계산 |
| Consequence | 소진 상태별 **배포•복구 행동** 합의 |

#### 한줄 요약

- SLI가 사용 내역, SLO가 월간 한도, 계산기가 잔액과 소비 속도, 정책이 잔액 상태별 행동표 역할을 한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Multi-Window Alerting**: 5분 동안 예산의 5%를 태우는 초특급 장애와, 3일 동안 예산의 10%를 갉아먹는 미세 장애를 동시에 잡기 위한 듀얼 윈도우 알림 기법.

</details>

```text
[Service Event]
      │
      ▼
1. SLI 오류율 계산
      │
      ▼
2. 허용 오류율 산출
      │
      ▼
3. Multi-window Burn Rate 계산
      │
      ▼
4. 경보•운영 정책 선택
      │
      ▼
5. 복구•변경 통제 실행
      │
      ▼
[예산 상태 갱신]
```

### 동작 원리

1. **SLI 오류율 계산**: 유효 Event의 실패 비율 측정
2. **허용 오류율 산출**: SLO로 기간별 Budget 계산
3. **Multi-window Burn Rate 계산**: 단기•장기 소진 속도 대조
4. **경보•운영 정책 선택**: Page•Ticket•변경 정책 결정
5. **복구•변경 통제 실행**: Rollback•Freeze•안정화 수행

#### 한줄 요약

- 최근 배포 뒤 결제 실패 속도가 급증하면 계산기가 조기 위험을 알리고 정책이 신규 배포를 줄인 뒤 이전 버전으로 복구하게 한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Fast Burn vs Slow Burn**: 수십 분 내로 예산을 전소시키는 Fast Burn은 즉각 개입(Page), 며칠에 걸쳐 갉아먹는 Slow Burn은 티켓(Ticket) 기반 처리.

</details>

| 알림 유형 | Burn Rate 배수 | 예산 100% 소진 소요 시간 | 알림(Action) 채널 지정 |
|:---|:---|:---|:---|
| **Catastrophic (치명적)**| **144x** | **약 5시간 이내 예산 전소** | **즉각 Pager / 전화 (On-Call)** |
| **Critical (심각)** | **60x** | **약 12시간 이내 예산 전소** | **즉각 Pager / 전화 (On-Call)** |
| **Warning (경고)** | **6x** | **약 5일 내 예산 고갈 예상** | **Jira Ticket 또는 Slack 평일 처리**|
| **Normal (정상)** | **1x 이하** | 30일(한 달) 꽉 채워 정상 소모 | 알림 없음 (배포 계속 진행) |

#### 한줄 요약

- 소진 비율은 이번 달에 쓴 쿠폰 수를 보여 주고 소진 속도는 지금 속도로 쓰면 언제 쿠폰이 바닥날지를 알려 준다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Calendar Window Reset Illusion**: 매월 1일 자정에 예산이 100%로 리셋되었다고 해서, 31일에 낸 장애의 근본 원인이 고쳐지지 않았음에도 다시 배포를 강행하는 꼼수.

</details>

| 3대 Error Budget 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. 달력 기반 리셋 꼼수** | 1일 리셋을 핑계로 미해결 장애 방치 | **Rolling Window(최근 30일) 기반으로 전환** |
| **2. 경영진의 100% SLO 압박**| 무장애를 원하여 Budget이 0에 수렴 | **100% 달성 비용(다중화)이 사업 이익을 초과함 입증**|
| **3. 예산 고갈 시 반발** | PO/개발팀이 Feature Freeze를 무시함 | **CTO 레벨에서 Error Budget Policy 강제 서명 합의**|

> 사례: **토스 / 당근마켓 / 카카오 SRE 조직의 99.9% Error Budget 합의 및 Datadog Burn Rate 알람 적용**

#### 한줄 요약

- 월초에 예산이 다시 생겼다고 장애 원인이 사라지는 것은 아니므로 이동 구간의 소진 추세와 지난 기간의 반복 원인을 함께 확인해야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Error Budget 수립 기준(Budget Standards)**: SLO 허용치(0.1%), Burn Rate (144x/60x), Feature Freeze Policy 및 Rolling Window 계산법에 의거한 체계.

</details>

- 예산 여유면 **변경 진행**, 빠른 소진이면 복구•안정화 우선

#### 한줄 요약

- 예산 여유는 반드시 소비할 할당량이 아니며 빠른 소진은 사용자 피해를 줄이는 복구와 안정화로 우선순위를 바꾸는 신호다.
