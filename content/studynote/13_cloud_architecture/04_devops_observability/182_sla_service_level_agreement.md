+++
title = "182. SLA (Service Level Agreement, 서비스 수준 협약)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) ([Service Level Agreement](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/))는 외부 고객에게 공개한 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 품질 약속을 측정 기준, 제외 조건, 보상 규칙까지 묶어 계약으로 고정한 문서다.
> 2. **가치**: SLA가 있어야 고객은 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 구매 가능한 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 상품으로 평가할 수 있고, 공급자는 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 투자를 비용이 아니라 계약 이행 의무로 관리하게 된다.
> 3. **판단 포인트**: 좋은 SLA는 높은 숫자보다 측정 가능성, 내부 [SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) ([Service Level Objective](/knowledge-base/studynote/15_devops_sre/03_sre_observability/123_slo_service_level_objective/))와의 완충 구간, 현실적인 크레딧 구조가 더 중요하며 이를 놓치면 마케팅 문구 이상의 의미를 갖기 어렵다.

---

## Ⅰ. 개요 및 필요성

[SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) ([Service Level Agreement](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/))는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 제공자와 고객이 "어떤 품질을 어느 기간 동안 보장하며, 못 지키면 어떻게 보상할 것인가"를 합의한 외부 계약이다. 내부 운영 문서인 SLO와 달리, SLA는 고객 청구·[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 크레딧·계약 해지 조항까지 연결되므로 법적·상업적 책임을 함께 가진다. 특히 클라우드 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)처럼 고객이 내부 인프라를 직접 통제할 수 없는 환경에서는, SLA가 사실상 신뢰의 최소 단위가 된다.

SLA가 필요한 이유는 장애 자체보다 장애 이후의 분쟁 비용이 더 크기 때문이다. 공급자는 "최선을 다했다"고 말하고 싶지만, 고객은 실제 매출 손실과 업무 중단을 기준으로 판단한다. 이때 미리 합의된 기준이 없으면 장애의 심각도, 책임 범위, 보상 수준이 모두 사후 협상으로 넘어가며, 기술 문제는 곧 영업·법무 문제로 번진다.

또한 SLA는 "99.9% [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)" 같은 숫자 하나로 끝나지 않는다. 어떤 기능이 대상인지, 어느 위치에서 측정하는지, 유지보수 창과 고객 귀책은 어떻게 제외하는지까지 정의해야 계약이 작동한다. 즉 SLA의 본질은 높은 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 광고가 아니라, **측정 가능한 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)을 외부에 판매 가능한 약속으로 변환하는 것**이다.

아래 그림은 SLA가 왜 단순 운영 지표가 아니라 분쟁 비용을 줄이는 계약 장치인지 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ Why SLA exists                                                          │
├──────────────────────────────────────────────────────────────────────────┤
│ Provider outage -> Customer impact -> dispute                           │
│                                                                          │
│ No SLA   : best effort only / blame fight                               │
│ With SLA : metric + window + exclusion + remedy are pre-agreed          │
└──────────────────────────────────────────────────────────────────────────┘
```

이 그림의 핵심은 SLA가 장애를 없애는 도구가 아니라, 장애가 발생했을 때 해석과 책임의 기준을 미리 고정하는 도구라는 점이다. 클라우드 아키텍처에서 SLA는 기술 스펙과 계약 스펙이 만나는 경계면이다.

- **📢 섹션 요약 비유**: SLA는 건물 임대 계약서와 같다. "엘리베이터가 몇 시간 이상 멈추면 관리비를 감면한다"는 조항이 있어야, 문제가 생겼을 때 감정 싸움이 아니라 약속된 기준으로 이야기할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

SLA가 실무에서 작동하려면 최소 여섯 요소가 맞물려야 한다. 첫째, 어떤 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와 기능이 계약 대상인지 범위를 정한다. 둘째, [SLI](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/) ([Service Level Indicator](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/))로 무엇을 재는지 정의한다. 셋째, 월간·분기별 같은 평가 창을 정한다. 넷째, 유지보수·불가항력·고객 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 오류 같은 제외 조항을 명시한다. 다섯째, 위반 시 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 크레딧이나 계약 해지 권리를 정한다. 여섯째, 이를 고객이 확인할 수 있도록 보고 체계를 갖춰야 한다.

| 구성 요소 | 반드시 답해야 할 질문 | 설계 포인트 |
| :--- | :--- | :--- |
| [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 범위 | 어떤 제품·[API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/)·기능이 계약 대상인가 | 핵심 경로와 부가 기능을 분리해야 함 |
| [SLI](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/) | 무엇을 어떻게 측정할 것인가 | 성공률, 지연시간, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 신선도 등 사용자 기준 |
| 평가 창 | 얼마 동안 누적해서 볼 것인가 | 30일 롤링 창이 가장 흔함 |
| 제외 조항 | 어떤 장애는 분모에서 뺄 것인가 | 예정 점검, 고객 귀책, 광역 재난 등을 명시 |
| 보상 규칙 | 위반 시 무엇을 제공할 것인가 | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 크레딧, 환불, 해지권, 지원 우선권 |
| 보고 방식 | 고객은 어디서 확인하는가 | [상태 페이지](/knowledge-base/studynote/15_devops_sre/03_sre_observability/182_status_page_public_sla/), 월간 리포트, 청구서 반영 자동화 |

[가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) SLA는 보통 다음 논리로 계산한다.

```text
Eligible Time   = Total Time - Excluded Time
Availability    = Good Time / Eligible Time × 100
```

여기서 중요한 것은 분모를 무엇으로 인정하느냐다. 예정 점검을 제외할지, 특정 리전 장애를 전체 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 장애로 볼지, 고객 네트워크 문제를 제외할지에 따라 결과가 달라진다. 따라서 숫자보다 먼저 분모 정의를 합의해야 한다.

아래 구조는 관측 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 외부 계약으로 변환되는 흐름을 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ From telemetry to contract                                              │
├──────────────────────────────────────────────────────────────────────────┤
│ Probe / logs -> SLI -> internal SLO -> public SLA -> credit / report   │
│                │          │               │                              │
│                │          │               └─ customer-facing promise     │
│                │          └─ safety buffer                               │
│                └─ measurable evidence                                    │
└──────────────────────────────────────────────────────────────────────────┘
```

이때 내부 SLO는 보통 SLA보다 더 엄격해야 한다. 예를 들어 실제 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 30일 동안 99.93%를 기록했다면, 내부 [SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) 99.95%는 놓쳤더라도 외부 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 99.9%는 지킨 상태가 될 수 있다. 이 완충 구간이 있어야 팀은 고객 보상 직전이 아니라 그 이전에 이상을 감지하고 대응할 수 있다.

| 월간 목표치 | 허용 다운타임(30일 기준) | 일반적 의미 |
| :--- | :--- | :--- |
| 99.5% | 약 3시간 36분 | 내부 업무 도구, 비핵심 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) |
| 99.9% | 약 43분 12초 | 일반 [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) (Software [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 외부 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) |
| 99.95% | 약 21분 36초 | 핵심 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) ([Application Programming Interface](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/)) |
| 99.99% | 약 4분 19초 | 결제·[인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)·통신 핵심 경로 |

숫자 한 자리 차이가 허용 실패 시간을 급격히 줄이므로, [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 상향은 단순 문구 수정이 아니라 [다중화](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/), 배포 통제, 장애 대응 자동화까지 포함한 아키텍처 변화다.

- **📢 섹션 요약 비유**: [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 설계는 "시험 90점 이상 보장"이라고 말하는 일이 아니라, 어떤 문제를 시험 범위에 넣고 어떤 실수는 감점에서 제외할지까지 채점표를 만드는 일과 같다.

---

## Ⅲ. 비교 및 연결

SLA를 정확히 이해하려면 [SLI](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/), [SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/), [OLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/086_ola/) ([Operational Level Agreement](/knowledge-base/studynote/12_it_management/02_itsm_itil/086_ola/))와의 경계를 나눠 봐야 한다. SLI는 현재 품질을 재는 실측값이고, SLO는 내부 운영 목표이며, SLA는 고객과 맺는 외부 약속이다. OLA는 그 SLA를 지키기 위해 내부 팀끼리 맞추는 운영 약속에 가깝다. 즉 외부 계약 하나를 지키려면 관측·운영·조직 약속이 여러 층으로 연결되어야 한다.

| 구분 | 대상 | 질문 | 예시 |
| :--- | :--- | :--- | :--- |
| [SLI](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/) | 측정값 | 지금 실제 품질은 얼마인가 | 성공률 99.93%, p95 280ms |
| [SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) | 내부 운영 | 어느 수준을 목표로 유지할 것인가 | 30일 성공률 99.95% |
| [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) | 외부 고객 | 어디까지 보장하고 못 지키면 어떻게 보상할 것인가 | 99.9% 미만 시 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)% 크레딧 |
| [OLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/086_ola/) | 내부 조직 | 각 팀은 어떤 수준으로 지원할 것인가 | P1 15분 응답, 1시간 내 우회 조치 |

또한 SLA는 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)만 의미하지 않는다. [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 특성에 따라 지연시간, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 신선도, 내구성, 지원 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)이 더 중요할 수 있다. 예를 들어 배치 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼은 "항상 켜져 있느냐"보다 "오전 7시까지 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 적재되느냐"가 더 의미 있는 SLA일 수 있다. 반대로 결제 API는 성공률과 지연시간이 핵심이다.

| [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 유형 | 언제 중요한가 | 대표 측정 예시 |
| :--- | :--- | :--- |
| [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) | 웹 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) | 월간 업타임 99.9% |
| 지연시간 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) | 실시간 검색, 결제, [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) | p95 300ms 이내 |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 신선도 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) | [데이터 파이프라인](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/), 리포팅 | 15분 내 반영률 99% |
| 지원 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) | 엔터프라이즈 고객 지원 | P1 15분 이내 응답 |
| 내구성 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) | 스토리지 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | 연간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손실 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) |

이 비교가 중요한 이유는 "높은 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/)"가 항상 좋은 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와 같은 말이 아니기 때문이다. 고객이 진짜 불편해하는 지점을 잘못 잡으면, 99.99% [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 지켜도 체감 품질은 낮을 수 있다. 결국 좋은 SLA는 가장 화려한 숫자가 아니라, 고객 가치와 비용 구조를 동시에 반영한 올바른 계약 축을 고르는 데서 시작한다.

- **📢 섹션 요약 비유**: [SLI](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/), [SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/), SLA의 관계는 체온계·건강 목표·보험 약관의 관계와 같다. 체온계는 현재 상태를 재고, 목표는 생활 습관을 정하며, 보험 약관은 문제가 생겼을 때 어떤 보장을 받을지 정한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 SLA를 설계할 때 가장 먼저 해야 할 일은 "무엇을 약속하지 않을 것인가"를 정하는 것이다. 모든 기능을 동일한 기준으로 묶으면 중요한 경로와 덜 중요한 경로가 섞여 계약이 흐려진다. 따라서 로그인, 결제, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 적재, 관리자 기능처럼 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 경로를 나누고, 고객이 실제로 돈을 지불하는 핵심 여정을 계약 대상으로 삼아야 한다.

| [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 유형 | 적합한 계약 초점 | 설계 시 주의점 |
| :--- | :--- | :--- |
| 일반 [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) 웹 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) + 기본 응답성 | 핵심 화면과 백오피스 기능을 분리 |
| 결제·[인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) | 성공률 + 지연시간 | 다중 리전, 빠른 우회 경로, 즉시 통지 체계 필요 |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 신선도 + 적재 성공률 | 단순 업타임보다 배치 완료 시각이 중요 |
| 엔터프라이즈 지원형 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | 지원 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) + 우선 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | 크레딧보다 전담 지원 절차가 더 중요할 수 있음 |

기술사 관점의 판단 포인트는 다음과 같다.

1. 측정 지점이 공급자 내부가 아니라 사용자 경계에 가까운가?
2. 내부 SLO가 외부 SLA보다 충분히 엄격해 완충 역할을 하는가?
3. 제외 조항이 넓어서 고객 체감 장애를 과도하게 숨기지 않는가?
4. [상태 페이지](/knowledge-base/studynote/15_devops_sre/03_sre_observability/182_status_page_public_sla/)와 월간 리포트가 계약 이행 근거로 자동 연결되는가?
5. [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 크레딧 산정과 청구 절차가 수작업 민원 처리로 남아 있지 않은가?

안티패턴도 명확하다. 첫째, 하이퍼스케일러 숫자만 보고 99.99% SLA를 복사하는 방식이다. 둘째, "불가항력"을 과도하게 넓혀 사실상 대부분의 장애를 제외하는 방식이다. 셋째, 고객이 직접 복잡한 증거를 모아 청구하도록 만들어 SLA를 형식화하는 방식이다. 넷째, [상태 페이지](/knowledge-base/studynote/15_devops_sre/03_sre_observability/182_status_page_public_sla/)를 같은 인프라에 올려 장애 시 오히려 공지 채널까지 사라지게 하는 방식이다.

실무적으로는 위반 단계를 계층형으로 설계하는 편이 좋다. 예를 들어 월 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 99.9% 미만이면 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)% 크레딧, 99.0% 미만이면 25% 크레딧처럼 계단형 보상을 두면, 경미한 실패와 중대한 실패를 같은 수준으로 취급하지 않아도 된다. 이는 고객 신뢰와 공급자 비용 사이의 현실적 균형 장치다.

- **📢 섹션 요약 비유**: [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 설계는 무조건 "절대 지각 없음"을 약속하는 담임보다, 지각 기준·결석 인정 사유·보충 수업 규칙까지 미리 정해 두는 학교 운영 규정에 가깝다.

---

## Ⅴ. 기대효과 및 결론

좋은 SLA는 고객에게는 구매 판단 기준을, 공급자에게는 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 투자 기준을 준다. 영업팀은 계약서로 약속을 설명할 수 있고, 운영팀은 어떤 장애가 비즈니스 손실로 직결되는지 명확히 볼 수 있다. 그 결과 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)은 "좋으면 좋은 것"이 아니라, 유지해야 하는 계약 품질이 된다.

하지만 SLA에는 분명한 한계도 있다. [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 크레딧은 고객의 실제 매출 손실을 전부 보상하지 못하며, 계약 문구가 좋아도 관측 체계가 부실하면 위반 여부를 입증하기 어렵다. 또한 지나치게 공격적인 SLA는 팀을 늘 만성 위반 상태로 몰아넣어, 오히려 고객 신뢰를 빠르게 깎아 먹는다.

앞으로는 퍼블릭 [상태 페이지](/knowledge-base/studynote/15_devops_sre/03_sre_observability/182_status_page_public_sla/), 자동 크레딧 정산, 티어별 차등 SLA가 더 중요해질 가능성이 높다. 특히 [멀티 리전](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/100_multi_region_deployment_pipeline_disaster_recovery/)·[멀티 테넌트](/knowledge-base/studynote/03_network/17_sdn_nfv/888_multi_tenant_cloud_resource_isolation_noisy_neighbor/) SaaS에서는 고객군별 기대치가 다르므로, 하나의 숫자만으로 모든 고객을 설명하기보다 표준 SLA와 프리미엄 SLA를 분리하는 전략이 현실적이다. 결론적으로 SLA는 **관측성의 숫자를 고객 계약으로 번역한 마지막 계층**으로 기억하는 것이 가장 정확하다.

- **📢 섹션 요약 비유**: SLA는 제품 설명서가 아니라 보증서와 같다. 설명서는 기능을 말하지만, 보증서는 문제가 생겼을 때 누가 어디까지 책임질지를 말한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [SLI](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/) ([Service Level Indicator](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/)) | SLA를 판단하는 실측 근거 |
| [SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) ([Service Level Objective](/knowledge-base/studynote/15_devops_sre/03_sre_observability/123_slo_service_level_objective/)) | SLA보다 엄격하게 잡아 두는 내부 운영 목표 |
| [OLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/086_ola/) ([Operational Level Agreement](/knowledge-base/studynote/12_it_management/02_itsm_itil/086_ola/)) | [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 이행을 위해 내부 팀끼리 맞추는 운영 약속 |
| [Error Budget](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/101_error_budget_sre/) | SLO와 실제 품질 사이의 허용 실패량 |
| [상태 페이지](/knowledge-base/studynote/15_devops_sre/03_sre_observability/182_status_page_public_sla/) ([Status Page](/knowledge-base/studynote/15_devops_sre/03_sre_observability/182_status_page_public_sla/)) | [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 이행 상황과 장애 이력을 고객에게 투명하게 공개하는 채널 |
| [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 크레딧 ([Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) Credit) | [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 위반 시 제공되는 대표 보상 수단 |
| [합성 모니터링](/knowledge-base/studynote/15_devops_sre/03_sre_observability/164_synthetic_monitoring_dummy_client/) ([Synthetic Monitoring](/knowledge-base/studynote/15_devops_sre/03_sre_observability/164_synthetic_monitoring_dummy_client/)) | 사용자 경계에서 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 근거 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 수집하는 방법 |

### 📈 관련 키워드 및 발전 흐름도

```text
Best effort service
    │
    ▼
SLI (Service Level Indicator) measurement
    │
    ▼
SLO (Service Level Objective) target setting
    │
    ▼
SLA (Service Level Agreement) contract
    │
    ├─ exclusion / remedy / claim process
    └─ public status page / monthly report
    │
    ▼
Tiered service credit and customer trust management
```

이 흐름은 단순 운영 지표가 내부 목표를 거쳐 외부 계약과 보상 체계로 확장되는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. SLA는 장난감 가게가 "일주일 안에 고장 나면 바꿔 줄게"라고 적어 둔 약속이에요.
2. 그냥 "좋은 장난감이에요"라고 말하는 것보다, 언제 어떻게 책임질지 적혀 있어야 믿을 수 있어요.
3. 그래서 가게는 그 약속을 지키려고 장난감을 더 튼튼하게 만들고, 문제 생기면 바로 알려 주게 돼요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 181 / 371

← **이전**: [181. SLO (Service Level Objective, 서비스 수준 목표)](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/)
**다음**: [183. 에러 예산 (Error Budget) - 혁신 속도와 신뢰성의 운영 균형](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/183_error_budget_sre_innovation_balance/) →

---
