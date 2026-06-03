---
title: SLI SLO SLA Error Budget
date: '2026-05-09'
tags:
- studynote-devops-sre
---

> **핵심 인사이트**
> - [[102_sli_slo_service_level_indicator_objective|SLI]] ([[102_sli_slo_service_level_indicator_objective|Service Level Indicator]])는 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]을 측정하는 지표, [[181_slo_service_level_objective|SLO]] ([[123_slo_service_level_objective|Service Level Objective]])는 내부 목표, [[085_sla|SLA]] ([[085_sla|Service Level Agreement]])는 외부 계약이다.
> - [[101_error_budget_sre|Error Budget]] (에러 버짓)은 SLO에서 도출되며, 개발팀이 혁신을 추진할 수 있는 "허용 가능한 불안정성"의 양이다.
> - SLO는 SLA보다 항상 엄격하게 [[009_config|설정]]해 예산 초과 전에 내부 경보가 울리게 해야 한다.

---

## Ⅰ. [[102_sli_slo_service_level_indicator_objective|SLI]] / [[181_slo_service_level_objective|SLO]] / [[085_sla|SLA]] 계층 구조

```
┌──────────────────────────────────────────────────────┐
│                   신뢰성 지표 계층                   │
│                                                      │
│  SLA  (계약) : 99.9% 가용성 — 위반 시 환불 조항     │
│    └─ SLO  (목표) : 99.95% — 내부 엄격 목표         │
│         └─ SLI  (지표) : 실제 측정값 (현재 99.97%)  │
└──────────────────────────────────────────────────────┘
```

| 개념  | 정의                                      | 주체           |
|-------|-------------------------------------------|----------------|
| [[102_sli_slo_service_level_indicator_objective|SLI]]   | [[090_service_kubernetes_network_load_balancing|서비스]] [[282_performance_tactics|성능]]을 정량화한 측정 지표           | 엔지니어링     |
| [[181_slo_service_level_objective|SLO]]   | SLI의 달성 목표값 (내부 약속)              | 팀 내부        |
| [[085_sla|SLA]]   | 고객과 체결한 법적/계약적 [[090_service_kubernetes_network_load_balancing|서비스]] 수준 협약 | 비즈니스·법무  |

> 📢 **Ⅰ 섹션 요약 비유**
> SLI는 체온계, SLO는 "36.5도 유지 목표", SLA는 "발열 시 환불"이라는 보험 계약이다.

---

## Ⅱ. 좋은 SLI의 조건

SLI는 사용자가 체감하는 품질을 직접 반영해야 한다.

**4 Golden [[611_conditional_access_signals|Signals]] (4대 황금 [[130_signal|신호]])**:

| [[130_signal|신호]]        | 설명                              | [[102_sli_slo_service_level_indicator_objective|SLI]] 예시                     |
|-------------|-----------------------------------|------------------------------|
| [[141_latency|Latency]]     | 요청 [[019_처리_지연|처리 지연]]                     | p99 응답시간 < 200ms          |
| Traffic     | [[139_throughput|처리량]]                            | 초당 요청수 (RPS)             |
| Errors      | 오류율                            | 5xx 비율 < 0.1%              |
| Saturation  | 자원 포화도                       | CPU 사용률 < 80%             |

> 📢 **Ⅱ 섹션 요약 비유**
> 4 Golden Signals는 자동차 계기판의 속도계·연료·온도·경고등 — 가장 중요한 지표 4개만 [[229_monitor|모니터]]링한다.

---

## Ⅲ. [[101_error_budget_sre|Error Budget]] 계산과 활용

```
Error Budget = 1 - SLO

SLO 99.9% → 월 43.8분 허용 다운타임
SLO 99.99% → 월 4.38분 허용 다운타임
```

[[101_error_budget_sre|Error Budget]] [[164_policy|정책]]:

```
남은 예산 > 50%  →  적극적 실험·배포 허용
남은 예산 < 10%  →  배포 속도 제한, 안정화 우선
예산 소진        →  기능 동결, 신뢰성 개선 집중
```

[[101_error_budget_sre|Error Budget]] 번 레이트(Burn Rate): 예산 소진 속도. 1시간 만에 1주치 예산이 소진되면 즉각 알림을 발생시킨다.

> 📢 **Ⅲ 섹션 요약 비유**
> Error Budget은 월 용돈 — 다 쓰면 새 물건 구매(새 기능 배포)는 다음 달까지 기다려야 한다.

---

## Ⅳ. [[181_slo_service_level_objective|SLO]] [[009_config|설정]] 원칙

1. **SLA보다 엄격하게**: [[181_slo_service_level_objective|SLO]] 99.95% > [[085_sla|SLA]] 99.9% — 내부 경보가 먼저 울려야 한다.
2. **사용자 여정 기반**: [[014_api_posix|API]] 응답시간보다 "결제 완료까지 전체 흐름의 성공률"이 더 의미 있다.
3. **점진적 강화**: 처음부터 99.99%를 목표로 하면 Error Budget이 너무 작아 혁신이 멈춘다.

```
SLO 99.9%  →  Error Budget = 월 43.8분
SLO 99.99% →  Error Budget = 월 4.38분  ← 배포 한 번 실패하면 소진
```

> 📢 **Ⅳ 섹션 요약 비유**
> SLO는 시험 합격선 — 60점([[085_sla|SLA]])이 통과선이지만 자신의 목표는 80점([[181_slo_service_level_objective|SLO]])으로 높게 잡아 여유를 만든다.

---

## Ⅴ. 개념 맵 및 발전 흐름도

### 개념 맵

| 구성 요소       | 역할                                          |
|-----------------|-----------------------------------------------|
| [[102_sli_slo_service_level_indicator_objective|SLI]]             | [[090_service_kubernetes_network_load_balancing|서비스]] [[282_performance_tactics|성능]] 측정 지표                          |
| [[181_slo_service_level_objective|SLO]]             | 내부 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 달성 목표값                        |
| [[085_sla|SLA]]             | 고객과의 [[090_service_kubernetes_network_load_balancing|서비스]] 수준 계약                      |
| [[101_error_budget_sre|Error Budget]]    | [[181_slo_service_level_objective|SLO]] 기반 허용 다운타임 예산                    |
| Burn Rate       | [[101_error_budget_sre|Error Budget]] 소진 속도                        |
| 4 Golden [[130_signal|Signal]] | [[141_latency|Latency]]·Traffic·Errors·Saturation 핵심 지표   |

### 관련 키워드 및 발전 흐름도

```
SLI/SLO/SLA
    ├── Error Budget → 혁신-안정성 균형
    ├── Burn Rate Alert → 예산 조기 경보
    ├── 4 Golden Signals → 핵심 SLI 선정
    └── Multi-window Alerting → SLO 기반 고급 알림 설계
```

> 🧒 **어린이 비유**
> SLO는 "이번 달 지각 허용 횟수 2번" 같은 규칙이에요. 2번 다 쓰면 새 방과후 활동(기능 추가)은 다음 달로 미뤄야 해요.
