---
sidebar:
  order: 214
  label: "214. SRE 온콜 관리•인시던트 대응"
  badge:
    text: "기출 · 50%"
    variant: note
title: "SRE 온콜 관리•인시던트 대응 (SRE Oncall Incident Management)"
date: "2026-08-25T11:00:00+09:00"
tags:
  - "notes-software"
weight: 214
extra:
  question_no: "214"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "온콜•사고 대응 폐루프가 최근 출제됨"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **SRE On-Call & Incident Management**: SLO 위반 시 온콜 엔지니어가 PagerDuty로 호출되어 IC 단일 지휘 하에 완화, 복구, 포스트모텀을 수행하는 운영 체계.
- **Incident Commander (IC)**: 장애 워룸(War Room)의 최고 지휘관으로서 복구 전략과 역할 분담을 총괄하는 단일 의사결정권자.

</details>

- 정의/개념: SLO 경보 발령부터 온콜 호출, 인시던트 지휘, 완화 및 비난 없는 사후 검토까지 **장애 대응 전 주기를 표준화하는 SRE 신뢰성 체계**
- 배경/필요성: 단순 자원 임계치 노이즈 경보로 인한 **경보 피로(Alert Fatigue), 장애 복구 시간(MTTR) 지연, 지휘 혼선 및 엔지니어 번아웃 해결 불가**

#### 한줄 요약
- Actionable Alert와 IC 단일 지휘 및 비난 없는 포스트모텀(Blameless Postmortem)을 통해 시스템 복원력을 극대화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Actionable Alert**: 당직 엔지니어가 즉시 조치를 취해야만 하는 의미 있는 경보 (단순 정보성 알림 배제).
- **Blameless Postmortem**: 장애 원인을 개인의 실수가 아닌 시스템 결함으로 규명하여 재발 방지 자동화 과제를 도출하는 문화.

</details>

- 단순 인프라 메트릭이 아닌 에러 예산 소진율에 기반한 **SLO 기반 실행 가능 경보(Actionable Alert)**
- 복구 방향 결정, 작업 위임, 상황 전파를 일원화하는 **인시던트 커맨더(IC) 단일 지휘**
- 원인 규명보다 사용자 피해 중단을 우선하는 **완화 우선(Mitigation First) 복구**

#### 한줄 요약
- SLO 기반 경보, IC 단일 지휘, 완화 우선 복구를 통해 MTTR을 극소화한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **인시던트 대응 4대 역할 체계**: Alerting Engine(SLO 경보), Incident Commander(단일 지휘관), Operations Lead(런북 조치), Communications Lead(상황 전파).

</details>

```text
[SRE 인시던트 지휘 및 대응 거버넌스 구조]
|-- 1. Automated Detection & Paging (Prometheus SLO Alert -> PagerDuty 온콜 에스컬레이션)
`-- 2. Incident Command System (War Room 단일 지휘 체계)
    |-- Incident Commander (IC: 복구 전략 결정, 우선순위 및 역할 분담 단일 지휘)
    |-- Operations Lead (Ops: 런북 실행, 카나리 롤백, 트래픽 우회 실무 조치)
    `-- Communications Lead (Comm: Status Page 및 경영진/고객 상황 브리핑)
`-- 3. Recovery & Postmortem Layer (72시간 이내 Blameless Postmortem 작성 및 재발 방지 백로그 등록)
```

선의 의미: 계층 및 SLO 경보로 호출된 온콜 팀이 IC 지휘 하에 역할을 분담하여 서비스를 완화 복구하고 포스트모텀으로 환류하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **SLO 경보 엔진 (Alerting)** | 사용자 경험과 에러 예산 소진율을 감시하여 **실제 조치가 필요한 Actionable Alert 발송** | Prometheus Burn Rate |
| **온콜 로테이션 (Pager)** | 24x7 교대 근무를 관리하고 **5분 내 미응답 시 상위 조직으로 자동 Escalation 호출** | PagerDuty, Opsgenie |
| **인시던트 커맨더 (IC)** | 장애 상황의 최고 의사결정권자로서 **우선순위 결정, 역할 분담, 복구 방향 단일 지휘** | 단일 의사결정권자 |
| **복구 운영자 (Ops Lead)** | 사전에 정의된 런북(Runbook)에 따라 **카나리 롤백, 트래픽 우회, 파드 재기동 등 실무 조치** | 기술적 복구 전담 |
| **커뮤니케이션 담당 (Comm)** | 기술적 복구와 분리되어 **경영진 및 고객 상태 페이지(Status Page)에 정기 상황 전파**| 대외 소통 전담 |

#### 한줄 요약
- SLO 경보 엔진, 온콜 로테이션, IC 지휘관, Ops 운영자, Comm 소통자가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **인시던트 대응 5단계**: SLO 위반 경보 $\to$ IC 지정 및 War Room 개설 $\to$ 완화 우선 롤백 $\to$ 정상화 확인 $\to$ Blameless Postmortem.

</details>

```text
SLO 99.9% 위반 경보 및 인시던트 발생
        │
   1. [경보 수신] 결제 API 에러율 급증으로 PagerDuty가 1차 온콜 엔지니어 스마트폰 호출
        │
   2. [IC 지정 및 War Room] 결제 마비(Sev-1) 판정 후 IC가 슬랙 비상 채널(`#incident-warroom`) 개설
        │
   3. [완화 조치 우선] 원인 디버깅 대신 최근 배포된 서비스 버전을 1분 만에 이전 정상 버전으로 롤백
   ┌────┴───────────────────────────┐
  지표 회복 (완화 성공)           지표 지속 악화
   │                                 │
4A. [상황 종료 선언]                4B. [2차 우회 경로 전환]
   결제 성공률 99.95% 회복 확인          Standby 인프라로 트래픽 전면 절체
   │                                 │
   └────┬────────────────────────────┘
        ▼
   5. [사후 분석] 72시간 내 Blameless Postmortem 작성 및 커넥션 풀 가드레일 액션 Jira 등록
```

#### 한줄 요약
- 경보 수신 → IC War Room 개설 → 완화 조치 → 정상화 확인 → 사후 분석 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Severity 등급 분류**: Minor(Sev-3: 국소 결함), Major(Sev-1: 전사 핵심 마비), Security(보안 침해).

</details>

| 비교 항목 | 일반 인시던트 (Minor: Sev-3) | 중대 인시던트 (Major: Sev-1) | 보안 인시던트 (Security Incident) |
|:---|:---|:---|:---|
| 핵심 적용 기준 | **비핵심 부가 기능 장애, 소수 고객 간헐 오류**| **핵심 결제/로그인 전면 마비, 다수 고객 피해** | **개인정보 유출, 랜섬웨어 감염, 인프라 침해**|
| 지휘 및 소집 체계 | 1차 온콜 엔지니어 단독 처리 (War Room 불필요)| **전담 IC 중심 비상 War Room 소집, 전사 공조** | **CISO 및 보안팀 주도 침해사고 대응팀 가동** |
| 핵심 복구 우선순위 | 업무 시간 내 런북 기반 점진 수정 | **원인 규명보다 '즉각적 트래픽 완화/롤백'** | **빠른 복구보다 '포렌식 증거 보존 및 네트워크 격리'**|
| 평균 목표 MTTR | 수 시간 ~ 1영업일 이내 | **30분 이내 (SLO 에러 예산 방어)** | 보안 무결성 입증 시까지 장기화 가능 |

#### 한줄 요약
- 경미한 결함은 Minor, 핵심 마비는 완화 중심 Major, 침해 사고는 증거 보존 중심 보안 트랙으로 대응한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Alert Fatigue (경보 피로)**: 밤새 울리는 수백 건의 무의미한 거짓 경보로 인해 당직 엔지니어가 실제 치명적 알림을 무시하게 되는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| CPU 80% 등 단순 자원 임계치 노이즈 경보로 온콜 번아웃 | **사용자 관점의 `SLO 에러 예산 소진율` 기반 Actionable Alert 전환** | 거짓 알람(False Alarm) 80% 삭감 |
| 1차 온콜 담당자가 수면 중이거나 부재하여 장애 인지 지체 | **5분 미응답 시 2차 당직자 및 매니저 자동 `Escalation 페이징`** | 장애 인지 시간(MTTA) 5분 이내 보장 |
| 장애 원인을 개인 실수로 몰아가 숨기거나 소극적 보고 유발 | **개인을 비난하지 않는 `Blameless Postmortem` 문화 및 포상제 정착** | 장애 투명성 및 근본적 재발 방지 달성 |
| 복구 중 통제되지 않은 다수 인원의 임의 명령으로 2차 장애 | **모든 프로덕션 조치는 반드시 IC의 사전 승인을 거치도록 지휘 단일화** | 2차 장애 및 지휘 혼선 100% 방지 |

#### 한줄 요약
- SLO 기반 경보 정제, 자동 에스컬레이션, 비난 없는 사후 분석, IC 단일 승인으로 운영한다.

## Ⅶ. 결론

- 복잡한 분산 클라우드 환경에서 장애는 피할 수 없는 현실임을 전제하고 **SLO 기반의 실행 가능 경보와 IC 단일 지휘 체계를 표준화**하며, **완화 우선 원칙과 비난 없는 포스트모텀(Blameless Postmortem) 환류 문화**를 정착시켜 지속적으로 회복 탄력성을 진화시키는 SRE 운영 완성

#### 한줄 요약
- SRE 온콜 관리는 Actionable Alert, IC 단일 지휘, 완화 우선 조치, 포스트모텀을 통해 다운타임을 극소화하는 핵심 신뢰성 엔지니어링 실천법이다.