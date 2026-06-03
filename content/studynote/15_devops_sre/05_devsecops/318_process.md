---
title: Toil SRE Automation
date: '2026-05-09'
tags:
- studynote-devops-sre
---

> **핵심 인사이트**
> - [[685_toil_automation_sre|Toil]] ([[685_toil_automation_sre|토일]])은 수동적·반복적·자동화 가능하지만 아직 자동화되지 않은 운영 업무로, SRE가 줄여야 할 핵심 대상이다.
> - Toil이 [[100_sre_site_reliability_engineering_error_budget|SRE]] 업무의 50%를 넘으면 조직이 엔지니어링 역량을 소모하고 있다는 [[130_signal|신호]]다.
> - [[685_toil_automation_sre|Toil]] 제거는 단순 자동화가 아니라, 문제 자체를 없애는 근본 해결(Elimination)을 목표로 한다.

---

## Ⅰ. Toil의 정의와 특성

Toil은 다음 6가지 특성을 모두 가진 업무다:

| 특성            | 설명                                            |
|-----------------|-------------------------------------------------|
| Manual          | 사람이 직접 수행                                |
| Repetitive      | 반복적으로 발생                                 |
| Automatable     | 자동화 가능하지만 아직 안 됨                    |
| Tactical        | 장기적 가치 없이 즉각적 반응만 함               |
| No Lasting Value| 완료 후 [[090_service_kubernetes_network_load_balancing|서비스]] 상태를 영구 개선하지 않음        |
| Scales linearly | [[090_service_kubernetes_network_load_balancing|서비스]] 성장에 비례해 업무량 증가                |

```
┌───────────────────────────────────────────────────┐
│                Toil 판별 흐름                     │
│                                                   │
│  반복 작업 발견                                   │
│      │                                            │
│      ├─ 자동화 가능? ─── No ──▶ Toil 아님        │
│      │       │                                   │
│      │      Yes                                  │
│      │       │                                   │
│      └──▶  Toil ──▶ 자동화 우선순위 큐에 등록    │
└───────────────────────────────────────────────────┘
```

> 📢 **Ⅰ 섹션 요약 비유**
> Toil은 매일 아침 똑같은 방법으로 청소하는 것 — 청소 로봇을 사면 그 시간을 더 창의적인 일에 쓸 수 있다.

---

## Ⅱ. Toil과 Overhead의 구분

| 구분        | 정의                                     | 예시                     |
|-------------|------------------------------------------|--------------------------|
| [[685_toil_automation_sre|Toil]]        | 자동화 가능한 반복 수동 작업              | 수동 배포, 반복 재시작    |
| Overhead    | 조직 운영을 위한 필수 비생산적 업무       | 회의, 문서 작성, 채용     |
| Engineering | 장기적 가치를 창출하는 프로젝트 업무      | 자동화 도구 개발          |

SRE는 Overhead는 줄이되, 제거하는 것이 목표인 Toil에 집중한다.

> 📢 **Ⅱ 섹션 요약 비유**
> 출퇴근 시간(Overhead)은 줄이기 어렵지만 꼭 필요하고, 반복되는 수기 보고서 작성([[685_toil_automation_sre|Toil]])은 엑셀 매크로로 없앨 수 있다.

---

## Ⅲ. [[685_toil_automation_sre|Toil]] 제거 [[268_strategy_pattern|전략]]

3단계 접근:

1. **Measure**: [[685_toil_automation_sre|Toil]] 양을 측정 (주 단위 시간 [[568_logs_distributed_logging_elk_fluentd|로그]])
2. **Prioritize**: [[012_roi_return_on_investment|ROI]] 기준 우선순위 [[009_config|설정]] (자동화 비용 vs 절감 시간)
3. **Eliminate**: 자동화 또는 문제 근원 제거

실무 도구:
- **Runbook 자동화**: 수동 런북 → [[198_ansible_os_configuration_management_ssh|Ansible]]/Python 스크립트화
- **Self-healing**: 장애 자동 감지 → 자동 재시작
- **[[207_chatops_slack_bot_deployment|ChatOps]]**: Slack [[158_instruction|명령어]]로 운영 작업 실행

> 📢 **Ⅲ 섹션 요약 비유**
> [[685_toil_automation_sre|Toil]] 제거는 계산기 발명 — 덧셈을 손으로 하던 시간을 분석·해석에 쓸 수 있게 된다.

---

## Ⅳ. [[685_toil_automation_sre|Toil]] 측정과 [[100_sre_site_reliability_engineering_error_budget|SRE]] 건강 지표

```
Toil 비율(%) = Toil 업무 시간 / 전체 업무 시간 × 100

권고 상한: 50%
이상 신호: 연속 분기 50% 초과
```

Toil이 지속적으로 높으면:
- 자동화 투자 시작
- [[090_service_kubernetes_network_load_balancing|서비스]] 소유권 재검토
- 팀 증원 또는 기능 범위 축소

> 📢 **Ⅳ 섹션 요약 비유**
> [[685_toil_automation_sre|Toil]] 비율 50% 초과는 "직원이 복사·붙여넣기에만 시간을 쓰고 있다"는 [[130_signal|신호]] — 즉시 자동화 검토가 필요하다.

---

## Ⅴ. 개념 맵 및 발전 흐름도

### 개념 맵

| 구성 요소       | 역할                                    |
|-----------------|-----------------------------------------|
| [[685_toil_automation_sre|Toil]]            | 자동화 가능한 반복 수동 운영 업무        |
| Overhead        | 조직 운영 필수 비엔지니어링 업무         |
| Engineering     | 장기 가치 창출 엔지니어링 업무           |
| 50% Rule        | Toil은 [[100_sre_site_reliability_engineering_error_budget|SRE]] 업무의 절반 이하여야 함      |
| Self-healing    | 자동 장애 감지·[[658_ir_recovery|복구]] 메커니즘            |
| [[207_chatops_slack_bot_deployment|ChatOps]]         | 채팅 인터페이스 기반 운영 자동화        |

### 관련 키워드 및 발전 흐름도

```
Toil
    ├── 측정 → 주단위 Toil 시간 로그
    ├── 자동화 → Runbook 스크립트화, Ansible
    ├── Self-healing → 장애 자동 감지·재시작
    └── SRE 건강 지표 → Toil 50% 상한 모니터링
```

> 🧒 **어린이 비유**
> Toil은 매일 같은 숙제를 손으로 쓰는 것이에요. 타자를 배우면(자동화) 그 시간에 더 재미있는 공부를 할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 318 / 373

← **이전**: [[317_sli_slo_sla|SLI SLO SLA Error Budget]]
**다음**: [[319_process|Blameless Postmortem]] →

---
