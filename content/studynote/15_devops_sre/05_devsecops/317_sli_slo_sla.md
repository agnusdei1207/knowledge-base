---
title: "SLI SLO SLA Error Budget"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
weight: 317
---
> **핵심 인사이트**
> - [SLI](/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/) ([Service Level Indicator](/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/))는 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)을 측정하는 지표, [SLO](/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) ([Service Level Objective](/studynote/15_devops_sre/03_sre_observability/123_slo_service_level_objective/))는 내부 목표, [SLA](/studynote/12_it_management/02_itsm_itil/869_sla/) ([Service Level Agreement](/studynote/12_it_management/02_itsm_itil/869_sla/))는 외부 계약이다.
> - [Error Budget](/studynote/04_software_engineering/02_requirements_analysis/101_error_budget_sre/) (에러 버짓)은 SLO에서 도출되며, 개발팀이 혁신을 추진할 수 있는 "허용 가능한 불안정성"의 양이다.
> - SLO는 SLA보다 항상 엄격하게 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)해 예산 초과 전에 내부 경보가 울리게 해야 한다.

---

## Ⅰ. [SLI](/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/) / [SLO](/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) / [SLA](/studynote/12_it_management/02_itsm_itil/869_sla/) 계층 구조

```
+------------------------------------------------------+
|                   신뢰성 지표 계층                   |
|                                                      |
|  SLA  (계약) : 99.9% 가용성 — 위반 시 환불 조항     |
|    +- SLO  (목표) : 99.95% — 내부 엄격 목표         |
|         +- SLI  (지표) : 실제 측정값 (현재 99.97%)  |
+------------------------------------------------------+
```

| 개념  | 정의                                      | 주체           |
|-------|-------------------------------------------|----------------|
| [SLI](/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/)   | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 정량화한 측정 지표           | 엔지니어링     |
| [SLO](/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/)   | SLI의 달성 목표값 (내부 약속)              | 팀 내부        |
| [SLA](/studynote/12_it_management/02_itsm_itil/869_sla/)   | 고객과 체결한 법적/계약적 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준 협약 | 비즈니스·법무  |

> 📢 **Ⅰ 섹션 요약 비유**
> SLI는 체온계, SLO는 "36.5도 유지 목표", SLA는 "발열 시 환불"이라는 보험 계약이다.

---

## Ⅱ. 좋은 SLI의 조건

SLI는 사용자가 체감하는 품질을 직접 반영해야 한다.

<strong>4 Golden <a href="/studynote/09_security/12_identity_threat_advanced/611_conditional_access_signals/">Signals</a> (4대 황금 <a href="/studynote/02_operating_system/02_process_thread/130_signal/">신호</a>)</strong>:

| [신호](/studynote/02_operating_system/02_process_thread/130_signal/)        | 설명                              | [SLI](/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/) 예시                     |
|-------------|-----------------------------------|------------------------------|
| [Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)     | 요청 [처리 지연](/studynote/03_network/01_data_communication/019_처리_지연/)                     | p99 응답시간 < 200ms          |
| Traffic     | [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)                            | 초당 요청수 (RPS)             |
| Errors      | 오류율                            | 5xx 비율 < 0.1%              |
| Saturation  | 자원 포화도                       | CPU 사용률 < 80%             |

> 📢 **Ⅱ 섹션 요약 비유**
> 4 Golden Signals는 자동차 계기판의 속도계·연료·온도·경고등 — 가장 중요한 지표 4개만 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링한다.

---

## Ⅲ. [Error Budget](/studynote/04_software_engineering/02_requirements_analysis/101_error_budget_sre/) 계산과 활용

```
Error Budget = 1 - SLO

SLO 99.9% -> 월 43.8분 허용 다운타임
SLO 99.99% -> 월 4.38분 허용 다운타임
```

[Error Budget](/studynote/04_software_engineering/02_requirements_analysis/101_error_budget_sre/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/):

```
남은 예산 > 50%  ->  적극적 실험·배포 허용
남은 예산 < 10%  ->  배포 속도 제한, 안정화 우선
예산 소진        ->  기능 동결, 신뢰성 개선 집중
```

[Error Budget](/studynote/04_software_engineering/02_requirements_analysis/101_error_budget_sre/) 번 레이트(Burn Rate): 예산 소진 속도. 1시간 만에 1주치 예산이 소진되면 즉각 알림을 발생시킨다.

> 📢 **Ⅲ 섹션 요약 비유**
> Error Budget은 월 용돈 — 다 쓰면 새 물건 구매(새 기능 배포)는 다음 달까지 기다려야 한다.

---

## Ⅳ. [SLO](/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 원칙

1. **SLA보다 엄격하게**: [SLO](/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) 99.95% > [SLA](/studynote/12_it_management/02_itsm_itil/869_sla/) 99.9% — 내부 경보가 먼저 울려야 한다.
2. **사용자 여정 기반**: [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 응답시간보다 "결제 완료까지 전체 흐름의 성공률"이 더 의미 있다.
3. **점진적 강화**: 처음부터 99.99%를 목표로 하면 Error Budget이 너무 작아 혁신이 멈춘다.

```
SLO 99.9%  ->  Error Budget = 월 43.8분
SLO 99.99% ->  Error Budget = 월 4.38분  <- 배포 한 번 실패하면 소진
```

> 📢 **Ⅳ 섹션 요약 비유**
> SLO는 시험 합격선 — 60점([SLA](/studynote/12_it_management/02_itsm_itil/869_sla/))이 통과선이지만 자신의 목표는 80점([SLO](/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/))으로 높게 잡아 여유를 만든다.

---

## Ⅴ. 개념 맵 및 발전 흐름도

### 개념 맵

| 구성 요소       | 역할                                          |
|-----------------|-----------------------------------------------|
| [SLI](/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/)             | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 측정 지표                          |
| [SLO](/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/)             | 내부 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 달성 목표값                        |
| [SLA](/studynote/12_it_management/02_itsm_itil/869_sla/)             | 고객과의 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준 계약                      |
| [Error Budget](/studynote/04_software_engineering/02_requirements_analysis/101_error_budget_sre/)    | [SLO](/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) 기반 허용 다운타임 예산                    |
| Burn Rate       | [Error Budget](/studynote/04_software_engineering/02_requirements_analysis/101_error_budget_sre/) 소진 속도                        |
| 4 Golden [Signal](/studynote/02_operating_system/02_process_thread/130_signal/) | [Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)·Traffic·Errors·Saturation 핵심 지표   |

### 관련 키워드 및 발전 흐름도

```
SLI/SLO/SLA
    +-- Error Budget -> 혁신-안정성 균형
    +-- Burn Rate Alert -> 예산 조기 경보
    +-- 4 Golden Signals -> 핵심 SLI 선정
    +-- Multi-window Alerting -> SLO 기반 고급 알림 설계
```

> 🧒 **어린이 비유**
> SLO는 "이번 달 지각 허용 횟수 2번" 같은 규칙이에요. 2번 다 쓰면 새 방과후 활동(기능 추가)은 다음 달로 미뤄야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 317 / 373

<- **이전**: [SRE Site Reliability 엔진ering](/studynote/15_devops_sre/05_devsecops/316_management/)
**다음**: [Toil SRE Automation](/studynote/13_cloud_architecture/05_data_engineering/318_process/) ->

---
