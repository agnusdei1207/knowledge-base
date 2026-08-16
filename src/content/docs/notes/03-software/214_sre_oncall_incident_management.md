---
sidebar:
  order: 214
  label: "214. SRE 온콜 관리•인시던트 대응 (SRE Oncall Incident Management)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "SRE 온콜 관리•인시던트 대응 (SRE Oncall Incident Management)"
date: "2026-08-14T06:35:00+09:00"
tags: ["notes-software"]
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

- **SRE (Site Reliability Engineering)**: Software Engineering으로 신뢰성과 개발 속도를 균형화하는 운영 접근법
- **Incident Management**: 장애 호출•완화•복구•학습을 연결하는 대응 활동

- **사이트 신뢰성 엔지니어링(Site Reliability Engineering, SRE)**: 소프트웨어 엔지니어링 방법론을 IT 운영에 적용하여 SLI/SLO/SLA, 에러 예산(Error Budget), 장애 사후 분석(Blameless Postmortem)을 통해 시스템 가용성과 개발 속도를 동시에 달성하는 체계.
</details>

- 정의/개념: SLO 경보부터 완화•복구•학습까지 연결하는 **SRE 대응 체계**
- 배경/필요성: 개인 의존 대응은 **지휘 혼선•중복 조치•Burnout** 유발

#### 한줄 요약

- 사용자 영향 경보에 역할 기반으로 대응하고 **예방 자동화**로 환류

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Actionable Alert (실행 가능 경보)**: 사용자 영향과 즉시 수행할 조치가 명확한 경보

</details>

- **SLO 기반 경보**: 자원보다 사용자 오류•지연•Error Budget 감시
- **On-Call Rotation**: 1•2차 교대와 Escalation 경로 명시
- **Incident Command**: IC•Ops•Comm 역할과 단일 지휘 체계
- **학습 환류**: Postmortem을 Runbook•자동화•Backlog로 전환

#### 한줄 요약

- 낮은 Noise의 경보와 명확한 역할로 **복구 골든타임** 확보

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Incident Command**: IC•복구•소통 역할을 분리해 중대 장애를 통제하는 체계

</details>

```text
[SRE Incident Management]
 ├── [SLO Alerting | 사용자 영향•Error Budget]
 ├── [On-Call Rotation | 1•2차•Escalation]
 ├── [Incident Command | IC•Ops•Comm]
 ├── [Response Workspace | 조치•결정•Timeline]
 └── [Action Tracker | Owner•기한•완료]
```

| 구성요소 | 책임 |
|---|---|
| SLO Alerting | 사용자 영향 기반 **Actionable Alert** 발송 |
| On-Call Rotation | 24×7 당직•인계•**Escalation** 수행 |
| Incident Command | 우선순위•역할•자원•**의사결정** 통제 |
| Response Workspace | 조치•결정•상태•**Timeline** 공동 기록 |
| Action Tracker | 개선 과제의 Owner•기한•**완료** 추적 |

#### 한줄 요약

- 경보•당직•지휘•기록•후속 조치를 **단일 대응 체계**로 연결

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Blameless Postmortem**: 개인 비난 없이 시스템 조건과 재발 방지를 분석하는 활동

</details>

```text
[SLO 위반 경보]
          │
          ▼
[1. 심각도 분류]
          │
          ▼
[2. 대응 역할 지정]
          │
          ▼
[3. 사용자 영향 완화]
          │
          ▼
[4. Service 복구]
          │
          ▼
[5. 사후 조치 추적]
          │
          ▼
[복구 상태•교훈 반환]
```

### 동작 원리

1. 심각도 분류: 영향 고객•기능•Data•범위로 Severity 결정
2. 대응 역할 지정: IC•Ops•Comm 책임 분리
3. 사용자 영향 완화: Rollback•Failover•격리로 피해 축소
4. Service 복구: 원인 제거와 핵심 지표 안정 확인
5. 사후 조치 추적: Postmortem 과제를 자동화•Runbook에 반영

#### 한줄 요약

- 원인 분석보다 **사용자 영향 완화**를 먼저 수행 후 학습 환류

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Major Incident**: 핵심 업무와 다수 고객에 큰 영향을 주어 전담 지휘가 필요한 사고

</details>

| 비교 항목 | 일반 Incident | Major Incident | Security Incident |
|---|---|---|---|
| 영향 | 제한된 기능•사용자 | 핵심 업무•다수 고객 | 침해•Data•법적 위험 |
| 지휘 | 1차 On-Call | **IC•War Room** | **보안•법무•Forensics** |
| 우선 | Runbook 복구 | 영향 완화•전사 협업 | 격리•증거 보존•신고 |

#### 한줄 요약

- 범위•업무 영향•침해 여부에 따라 **대응 Track** 분리

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **On-Call Fatigue**: 저가치 경보와 반복 수동 대응으로 당직 집중력이 저하되는 현상

</details>

| 고려사항 | 대책 |
|---|---|
| 자원 경보 Noise | SLO•사용자 영향•**Runbook 연계**로 재설계 |
| 책임 Team Ping-Pong | Service Owner와 **자동 Escalation** 지정 |
| 교대 중 맥락 유실 | 공용 War Room•Timeline•**명시적 Hand-off** 적용 |
| 비난 중심 사후 분석 | Blameless Review와 **System Action** 추적 |

#### 한줄 요약

- 경보 품질•Owner•인계•심리 안전으로 **지속 가능한 On-Call** 운영

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- CPU가 높아도 사용자가 멀쩡하면 Ticket으로 보고, 결제가 실패하면 즉시 호출한다.

</details>

- SLO 영향은 **IC 중심 즉시 완화**, 저가치 자원 경보는 Ticket 처리
