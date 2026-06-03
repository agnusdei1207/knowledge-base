---
title: 26. MTTR (Mean Time to Recover) — 평균 복구 시간
date: '2026-04-29'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[451_mttr|MTTR]] (Mean Time to Recover/Repair, 평균 [[658_ir_recovery|복구]] 시간)은 시스템 장애 발생부터 정상 [[658_ir_recovery|복구]]까지 걸린 평균 시간으로, [[100_sre_site_reliability_engineering_error_budget|SRE]]([[100_sre_site_reliability_engineering_error_budget|Site Reliability Engineering]])의 4대 [[523_dhcp_dora_process|DORA]] [[342_routing_metric_hop_bandwidth_delay|메트릭]] 중 "복원력([[345_reliability_security|Reliability]])"을 측정하는 핵심 지표다.
> 2. **가치**: MTTR은 단순히 빠른 [[658_ir_recovery|복구]]만을 의미하지 않는다. 장애 탐지([[961_deepfake_detection|Detection]]) → 대응(Response) → 원인 파악(Diagnosis) → [[658_ir_recovery|복구]]([[658_ir_recovery|Recovery]])의 4단계 [[123_pipe|파이프]]라인 전체를 최적화해야 낮출 수 있다. 어느 한 단계의 병목이 전체 MTTR을 지배한다.
> 3. **판단 포인트**: MTTR이 낮다고 무조건 좋은 것은 아니다. 빠른 [[658_ir_recovery|복구]]를 위해 원인 파악을 건너뛰면 재발 빈도([[450_mtbf|MTBF]] 단축)가 높아진다. 이상적인 [[100_sre_site_reliability_engineering_error_budget|SRE]] 팀은 "빠른 일시 [[658_ir_recovery|복구]]([[313_rollback|Rollback]]) + 철저한 사후 분석(Post-mortem)"을 병행하여 MTTR과 [[450_mtbf|MTBF]] 모두 개선한다.

---

## Ⅰ. 개요 및 필요성

```text
┌────────────────────────────────────────────────────────┐
│              MTTR 4단계 파이프라인                       │
├────────────────────────────────────────────────────────┤
│                                                         │
│  장애 발생 ──> [1. 탐지] ──> [2. 대응] ──> [3. 진단]     │
│                                         ──> [4. 복구]   │
│                                                         │
│  MTTR = 탐지 시간 + 대응 시간 + 진단 시간 + 복구 시간    │
│                                                         │
│  목표: 각 단계를 자동화하여 MTTR을 시간 → 분 → 초로 단축 │
└────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: MTTR은 화재 진압 시간이다. 화재 감지기(탐지) → 소방차 출동(대응) → 불 위치 파악(진단) → 진화([[658_ir_recovery|복구]])의 4단계. 어느 한 단계가 느리면 전체 피해가 커진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[451_mttr|MTTR]] 단계별 단축 기법

| 단계 | 병목 원인 | 단축 기법 |
|:---|:---|:---|
| **탐지** | [[229_monitor|모니터]]링 부재 | [[162_apm_application_performance_management|APM]], [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]](Jaeger), 알림 임계값 최적화 |
| **대응** | 수동 에스컬레이션 | PagerDuty 자동화, 런북(Runbook) 자동 실행 |
| **진단** | [[568_logs_distributed_logging_elk_fluentd|로그]] [[136_variance|분산]] | ELK [[057_stack|Stack]], 중앙화 로깅, [[190_ai_llm_requirements_specification|AI]] [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]] |
| **[[658_ir_recovery|복구]]** | 수동 배포 | Blue/Green 배포, 자동 [[098_rollback_strategy_pipeline_error_threshold|롤백]], [[595_canary_stack_smashing_protector|Canary]] 릴리즈 |

### 관련 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 지표 4종

```text
MTTD (Mean Time to Detect)   : 장애 발생 ~ 탐지까지
MTTR (Mean Time to Recover)  : 장애 발생 ~ 복구까지
MTBF (Mean Time Between Failures) : 복구 ~ 다음 장애까지
MTTF (Mean Time to Failure)  : 최초 가동 ~ 첫 장애까지

가용성 = MTBF / (MTBF + MTTR)
```

- **📢 섹션 요약 비유**: [[452_availability|가용성]] 공식은 선생님이 쉬는 시간 비율이다. 수업 시간([[450_mtbf|MTBF]])이 길고 쉬는 시간([[451_mttr|MTTR]])이 짧을수록 [[452_availability|가용성]](수업 비율)이 높다.

---

## Ⅲ. 비교 및 연결

| [[342_routing_metric_hop_bandwidth_delay|메트릭]] | [[523_dhcp_dora_process|DORA]] [[104_classification_analysis|분류]] | 측정 대상 |
|:---|:---|:---|
| **[[087_deployment_kubernetes_workload_rolling_update|Deployment]] Frequency** | 속도 | 배포 얼마나 자주 하는가 |
| **[[024_lead_time_for_changes|Lead Time for Changes]]** | 속도 | 코드 → 운영 환경 소요 시간 |
| **[[025_change_failure_rate_cfr|Change Failure Rate]]** | 안정성 | 배포 후 장애 발생 비율 |
| **[[451_mttr|MTTR]]** | 안정성 | 장애 발생 후 [[658_ir_recovery|복구]] 소요 시간 |

- **📢 섹션 요약 비유**: [[523_dhcp_dora_process|DORA]] 4대 지표는 레이싱 팀 성과 지표다. 속도(얼마나 빠르게 달리는가)와 안전(사고 시 얼마나 빨리 [[658_ir_recovery|복구]]하는가) 두 축을 동시에 측정한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[100_sre_site_reliability_engineering_error_budget|SRE]] 팀 [[451_mttr|MTTR]] 개선 로드맵
1. **현황 측정**: MTTD, 대응 시간, 진단 시간, [[658_ir_recovery|복구]] 시간 각각 측정.
2. **병목 [[655_ir_detection_analysis|식별]]**: 4단계 중 가장 긴 단계 파악.
3. **자동화 우선**: 탐지→알림→런북 실행 자동화 (0단계 자동화 달성).
4. **Post-mortem 문화**: [[658_ir_recovery|복구]] 후 반드시 근본 원인 분석 → 재발 방지.

### 목표 [[451_mttr|MTTR]] 산업 벤치마크
- Elite 조직: [[451_mttr|MTTR]] < 1시간.
- High 조직: [[451_mttr|MTTR]] < 1일.
- Medium 조직: [[451_mttr|MTTR]] < 1주.
- Low 조직: [[451_mttr|MTTR]] > 1주.

- **📢 섹션 요약 비유**: [[451_mttr|MTTR]] 벤치마크는 응급실 대기 시간이다. Elite 병원은 1시간 이내 처치, 일반 병원은 하루, 의료 취약 지역은 일주일 이상. 환자(사용자)에게는 대기 시간이 생사를 가른다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **사용자 신뢰** | 빠른 [[658_ir_recovery|복구]]로 [[090_service_kubernetes_network_load_balancing|서비스]] [[085_sla|SLA]] 준수 |
| **비즈니스 손실 최소화** | 장애 시간 × 비용/분 직접 절감 |
| **팀 역량 향상** | Post-mortem을 통한 지속 개선 |

[[099_aiops_chatbot_itsm_automation|AIOps]]([[190_ai_llm_requirements_specification|AI]] for IT Operations)는 ML 기반 [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]]로 MTTD를 초 단위로 단축하고, 자동 런북 실행으로 MTTR을 수분 이내로 낮추는 방향으로 발전하고 있다.

- **📢 섹션 요약 비유**: AIOps는 자동 운전 소방차다. AI가 화재를 먼저 탐지하고 자동으로 최적 경로로 출동하여 진압한다. 사람 운전사(운영팀)보다 탐지→[[658_ir_recovery|복구]] 사이클이 훨씬 빠르다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[181_slo_service_level_objective|SLO]]/[[085_sla|SLA]]** | [[451_mttr|MTTR]] 목표값 [[009_config|설정]]의 계약적 근거 |
| **[[201_dora_metrics_devops_performance|DORA Metrics]]** | MTTR을 포함하는 [[652_devops_calms_culture|DevOps]] 성과 지표 4종 |
| **Post-mortem** | [[451_mttr|MTTR]] 사후 근본 원인 분석 활동 |
| **[[099_aiops_chatbot_itsm_automation|AIOps]]** | [[190_ai_llm_requirements_specification|AI]] 기반 MTTD+[[451_mttr|MTTR]] 자동 단축 기술 |
| **Blue/Green 배포** | 빠른 자동 [[098_rollback_strategy_pipeline_error_threshold|롤백]]으로 [[451_mttr|MTTR]] 단축 |

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 장애 대응 — 장시간 MTTR, 사람 의존]
    │
    ▼
[모니터링 도구 — APM, ELK, Prometheus 도입]
    │
    ▼
[DORA 메트릭 체계화 — MTTR 정량 측정 시작]
    │
    ▼
[자동화 런북 — PagerDuty + Runbook 자동 실행]
    │
    ▼
[AIOps — AI 이상 탐지 + 자동 복구 파이프라인]
```

### 👶 어린이를 위한 3줄 비유 설명

1. MTTR은 게임에서 다시 살아나는 데 걸리는 시간이에요! 빠를수록 좋고, 방법을 알아야 빠르게 살아날 수 있어요.
2. 화재 탐지기 → 소방차 출동 → 불 위치 파악 → 진화처럼, 장애도 탐지→대응→진단→[[658_ir_recovery|복구]] 4단계로 줄여야 해요.
3. AI가 알아서 불을 탐지하고 자동으로 진압하는 세상([[099_aiops_chatbot_itsm_automation|AIOps]])이 되면 MTTR이 몇 초로 줄어든답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 26 / 373

← **이전**: [[025_change_failure_rate_cfr|25. CFR (Change Failure Rate) — 변경 실패율]]
**다음**: [[027_space_framework|27. SPACE 프레임워크 — 개발자 생산성 5차원 측정]] →

---
