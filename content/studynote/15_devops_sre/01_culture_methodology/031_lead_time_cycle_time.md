+++
title = "31. 리드 타임과 사이클 타임 — DevOps 흐름 핵심 지표"
date = 2026-04-29

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/)([Lead Time](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/))은 고객 요청부터 배포까지 총 시간이고, 사이클 타임(Cycle Time)은 개발 시작부터 배포까지 시간이다. [Lead Time](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/) ≥ Cycle Time이며, 둘의 차이가 "요청 대기 시간"이다.
> 2. **가치**: [DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/)([DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) Research and Assessment) [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)의 4대 지표 중 하나가 "변경 [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/)([Lead Time for Changes](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/024_lead_time_for_changes/))"이다. Elite 팀은 [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/)이 1시간 미만이고, Low 팀은 6개월 이상이다.
> 3. **판단 포인트**: [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/) 단축의 최대 레버는 배치 크기([Batch Size](/knowledge-base/studynote/10_ai/05_data_science_ml/346_batch_size_generalization/)) 축소다. 작은 변경을 자주 배포하면([Continuous Delivery](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/164_continuous_delivery/)) [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/)이 극적으로 줄고 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 위험도 낮아진다.

---

## Ⅰ. 개요 및 필요성

```text
리드 타임 vs 사이클 타임:

요청 ────────────────────────── 배포
 │                                 │
 │<──────── Lead Time ──────────>│
           │<── Cycle Time ────>│
           │                    │
          개발 시작            배포

차이 = 대기 시간 (요청 접수 → 개발 시작)
```

- **📢 섹션 요약 비유**: [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/) vs 사이클 타임은 피자 주문과 요리 시간이다. 주문에서 수령까지([리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/))에는 주문 대기(리드-사이클 차이)와 실제 요리 시간(사이클 타임)이 포함된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 성숙도 등급

| 지표 | Elite | High | Medium | Low |
|:---|:---|:---|:---|:---|
| **배포 빈도** | 하루 여러 번 | 하루 1번~주1 | 주1~월1 | 월1 미만 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/">리드 타임</a></strong> | < 1시간 | 1일~1주 | 1주~1개월 | 1~6개월+ |
| <strong><a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a> 시간</strong> | < 1시간 | < 1일 | < 1주 | 1~6개월 |
| **변경 실패율** | 0~15% | 16~30% | 16~30% | 16~30% |

### [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/) 단축 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

```text
배치 크기 축소:
  Before: 2주마다 100개 변경 → 리드 타임 2주+
  After:  매일 5~10개 변경  → 리드 타임 1일 미만

핵심 단계별 최적화:
  요청 대기:   자동 티켓 생성, 스프린트 즉시 배정
  개발:        Feature Flag, Trunk-based Development
  코드 리뷰:   소규모 PR, AI 코드 리뷰
  CI 파이프라인: 병렬화, 캐싱으로 10분 → 5분
  배포 승인:   자동화 테스트 통과 시 자동 배포 (CD)
```

- **📢 섹션 요약 비유**: 배치 크기 축소는 배달 방식 개선이다. 하루치 배달을 한 번에 큰 트럭으로 하면 오래 기다리지만, 여러 번 소량 배달하면 각 고객이 더 빨리 받는다. 소프트웨어도 작게 자주 배포하면 [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/)이 줄어든다.

---

## Ⅲ. 비교 및 연결

| 비교 | [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/) | 사이클 타임 | [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) |
|:---|:---|:---|:---|
| 측정 범위 | 요청→배포 (전체) | 개발→배포 | 단위 시간 완료 수 |
| 고객 관점 | 직접적 (대기 경험) | 간접적 | 생산성 지표 |
| 개선 포인트 | 대기 제거 | 개발 속도 | [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화 |

- **📢 섹션 요약 비유**: 리드·사이클·[처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)은 음식점 [KPI](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/) 세 가지다. 주문부터 수령 시간([리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/)), 실제 조리 시간(사이클 타임), 시간당 서빙 수([처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/))를 함께 관리해야 완전한 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 품질을 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/) 측정 도구

```text
JIRA:
  생성 시간 → 완료 시간 = 리드 타임 자동 계산
  사이클 타임 보고서: "In Progress" → "Done"

GitHub Insights:
  PR 생성 → 머지: 사이클 타임 일부

LinearB / Swarmia:
  Git 이벤트 + JIRA를 통합 분석
  DORA 메트릭 자동 대시보드

배포 추적:
  ArgoCD → 배포 시점 기록
  Feature Flag → 기능 릴리즈 시점
```

### Little's Law 적용

```text
리틀의 법칙:
  평균 리드 타임 = 평균 WIP / 평균 처리량

  WIP = 20개 (진행 중인 작업)
  처리량 = 4개/일
  리드 타임 = 20/4 = 5일

  WIP 감소(10개) → 리드 타임 = 10/4 = 2.5일
  → WIP 제한이 리드 타임 단축의 가장 확실한 방법!
```

- **📢 섹션 요약 비유**: 리틀의 법칙은 줄 서기 대기 이론이다. 계산대([처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/))가 같아도 줄(WIP)이 짧으면 결제 대기 시간([리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/))이 줄어든다. 한 번에 너무 많은 일을 시작하면 모든 일이 늦어진다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **고객 가치** | 빠른 기능 전달 → 경쟁 우위 |
| **품질** | 소규모 변경 → [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 쉬움·버그 감소 |
| <strong><a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/058_dx_developer_experience/">개발자 경험</a></strong> | 빠른 피드백 → 높은 만족도 |

[AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) [코드 리뷰](/knowledge-base/studynote/04_software_engineering/06_software_architecture/330_code_review/)(GitHub Copilot for [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/))·자동화 테스트 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·[AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 배포 의사결정이 사이클 타임 단축의 새로운 레버가 되고 있다. AI가 [코드 리뷰](/knowledge-base/studynote/04_software_engineering/06_software_architecture/330_code_review/) 시간을 시간 단위에서 분 단위로 단축하면 Elite 팀의 [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/) 1시간 미만 목표가 대부분의 팀에게 현실이 될 수 있다.

- **📢 섹션 요약 비유**: [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) [코드 리뷰](/knowledge-base/studynote/04_software_engineering/06_software_architecture/330_code_review/)는 즉각 피드백 교사다. 학생(개발자)이 숙제(코드)를 제출하면 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 선생님이 1분 안에 피드백을 주어 기다림([리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/)) 없이 다음 단계로 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/)할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/">DORA</a> <a href="/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/">메트릭</a></strong> | [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/) 성숙도 벤치마크 |
| **WIP 제한** | 리틀의 법칙 기반 [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/) 단축 |
| **배치 크기** | 소규모 빈번 배포 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/084_kanban_board_wip_limit/">칸반</a></strong> | WIP 제한 시각적 관리 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> <a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/330_code_review/">코드 리뷰</a></strong> | 사이클 타임 단축 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 레버 |

### 📈 관련 키워드 및 발전 흐름도

```text
[전통 폭포수 — 리드 타임 수개월, 배치 크기 대규모]
    │
    ▼
[애자일 스프린트 — 2주 배치, 리드 타임 수주]
    │
    ▼
[Continuous Delivery — 소규모 자주 배포, 리드 타임 일]
    │
    ▼
[DORA Elite — 리드 타임 1시간 미만, 자동화 CD]
    │
    ▼
[AI 지원 DevOps — AI 리뷰·테스트로 사이클 타임 분 단위]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/)은 피자 주문부터 수령까지, 사이클 타임은 실제 요리 시간이에요!
2. 작은 변경을 자주 배포하면 [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/)이 줄어들고 문제가 생겨도 쉽게 되돌릴 수 있어요!
3. [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) [코드 리뷰](/knowledge-base/studynote/04_software_engineering/06_software_architecture/330_code_review/) 덕분에 기다리는 시간([리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/))을 1시간 이내로 줄이는 Elite 팀이 늘고 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 31 / 373

← **이전**: [30. 가치 흐름 맵핑 (VSM) — 낭비를 찾아 흐름을 최적화](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/030_value_stream_mapping/)
**다음**: [콘웨이의 법칙 (Conway's Law)](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/032_conways_law/) →

---
