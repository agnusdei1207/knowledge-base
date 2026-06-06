---
title: "076. Value Stream Mapping Lean"
date: "2026-04-07"
tags:
  - "studynote-enterprise"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [VSM](/studynote/15_devops_sre/01_culture_methodology/030_value_stream_mapping/)([Value Stream Mapping](/studynote/04_software_engineering/02_requirements_analysis/088_value_stream_mapping_vsm/), [가치 흐름 매핑](/studynote/07_enterprise_systems/04_process_consulting/224_vsm_value_stream_mapping/))은 고객 요청부터 최종 인도까지의 흐름을 한 장에 그려 낭비(Muda)와 병목을 찾는 [Lean](/studynote/04_software_engineering/02_requirements_analysis/087_lean_software_development_7_principles/) 도구다.
> 2. **가치**: 개발 자체는 빠른데 승인과 대기 때문에 배포가 늦다면, VSM은 그 보이지 않는 시간을 숫자로 드러낸다.
> 3. **판단 포인트**: VSM은 부서별 효율이 아니라 전체 Lead Time을 줄이는 도구이므로, 한 부서만 빠르게 만드는 개선은 정답이 아니다.

---

## Ⅰ. 개요 및 필요성

가치 흐름은 고객이 원하는 결과가 만들어지는 전체 경로다. VSM은 이 경로를 [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/)해, 어디서 실제 가치가 생기고 어디서 시간만 소비되는지 드러낸다. 그래서 Lean과 DevOps가 만날 때 가장 자주 쓰이는 진단 도구가 된다.

소프트웨어 조직에서는 코딩보다 대기 시간이 더 길다. 개발이 1시간인데 보안 검토와 승인 대기가 2주라면, 전체 [리드 타임](/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/)은 사실상 2주다. VSM은 이 숨은 대기를 눈에 보이게 한다.

```text
고객 요청 -> 개발 -> QA 대기 -> 보안 승인 -> 배포
   |          |          |           |        |
   +- 가치 시간은 짧고, 대기 시간이 길다 -----+
```

이 그림처럼 VSM은 "일이 얼마나 빨리 끝났는가"보다 "고객이 얼마나 오래 기다렸는가"를 먼저 묻는다.

- **📢 섹션 요약 비유**: 고속도로에서 자동차 한 대가 빨라도 톨게이트에 줄이 길면 전체 여행은 느리다. 길 전체를 봐야 막힌 곳이 보인다.

---

## Ⅱ. 아키텍처 및 핵심 원리

VSM은 프로세스 박스, 정보 흐름, 재공품(WIP, [Work In Progress](/studynote/04_software_engineering/uncategorized/661_kanban_wip_limit/)), Cycle Time, [Lead Time](/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/), Takt Time을 함께 본다. 가치 시간과 대기 시간을 나눠 적으면 개선 포인트가 선명해진다.

| 지표 | 뜻 | 왜 중요한가 |
| :-- | :-- | :-- |
| Cycle Time | 실제 작업 시간 | 팀 역량 측정 |
| [Lead Time](/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/) | 요청부터 인도까지 총시간 | 고객 체감 시간 |
| WIP([Work In Progress](/studynote/04_software_engineering/uncategorized/661_kanban_wip_limit/)) | [진행](/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 중 작업량 | 병목과 혼잡의 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) |
| Takt Time | 고객 수요가 요구하는 리듬 | 공급 속도 기준 |

```text
[현재 상태]
요청 --> 개발 --> QA 대기 --> 승인 대기 --> 배포
 |        |         |           |
 |        +- value -+-----------+
 +- wait time이 대부분
```

VSM의 힘은 각 단계의 소요 시간을 숫자로 적는 데 있다. 숫자가 있어야 낭비를 논쟁이 아니라 사실로 바꿀 수 있다.

- **📢 섹션 요약 비유**: 지도를 그리면 산이 어디에 있는지 보인다. 발로만 걸으면 길 전체가 막혔는지 알기 어렵다.

---

## Ⅲ. 비교 및 연결

VSM은 Flowchart, [Kanban](/studynote/04_software_engineering/02_requirements_analysis/084_kanban_board_wip_limit/), Gantt chart와 자주 비교된다. 각 도구는 보는 것이 다르다.

| 도구 | 무엇을 보여주는가 | 강점 | 한계 |
| :-- | :-- | :-- | :-- |
| [VSM](/studynote/15_devops_sre/01_culture_methodology/030_value_stream_mapping/) | 가치와 대기의 흐름 | 병목과 낭비 가시화 | 작성에 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 필요 |
| Flowchart | 절차와 분기 | [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) 구조 파악 | 시간 정보 약함 |
| [Kanban](/studynote/04_software_engineering/02_requirements_analysis/084_kanban_board_wip_limit/) | 작업 상태와 WIP | [흐름 제어](/studynote/03_network/04_data_link_layer_error/213_flow_control_buffer_overflow/) | 전체 [리드 타임](/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/)은 약함 |
| Gantt | 일정과 기간 | 계획 관리 | 실제 흐름 낭비는 잘 안 보임 |

Lean의 관점에서는 VSM이 가장 직관적으로 "전체 최적화"를 말해 준다. 개별 팀의 생산성보다 최종 인도 시간을 줄이는 것이 목표이기 때문이다.

- **📢 섹션 요약 비유**: 운동선수 한 명이 빠르다고 팀이 빨라지는 건 아니다. 릴레이는 바통이 빨리 넘어가야 전체가 빨라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

VSM을 제대로 하려면 특정 제품군이나 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 흐름 하나를 정하고, 실제 시간 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 모아야 한다. 감으로 그린 지도는 보통 낙관적이다. 실제 시간을 적으면 대기와 재작업이 드러난다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 하나의 가치 흐름(제품/[서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))을 선택했는가?
2. 각 단계의 실제 시간이 기록됐는가?
3. 대기 시간과 작업 시간을 분리했는가?
4. 병목이 부서가 아니라 흐름 관점에서 정의됐는가?
5. 미래 상태(Future [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/))와 개선 항목이 있는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 희망 사항을 [현재 상태](/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)처럼 그림
- 한 부서만 빠르게 만드는 로컬 최적화
- 대기 시간을 측정하지 않음
- 현황도 없이 미래도만 그리기

기술사 답안에서는 "VSM은 개선 도구가 아니라 대기 시간을 드러내는 진단 도구"라고 써야 한다. 그래야 Lean의 핵심이 살아난다.

- **📢 섹션 요약 비유**: 병원에서 진료실만 빠르면 소용없다. 접수, 검사, 수납, 약국까지 모두 봐야 실제 기다림이 줄어든다.

---

## Ⅴ. 기대효과 및 결론

VSM을 쓰면 [리드 타임](/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/)이 줄고, 협업 병목이 보이며, 개선 우선순위가 숫자로 바뀐다. 특히 DevOps에서는 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인의 어느 구간이 가장 오래 멈추는지 찾는 데 효과적이다.

다만 VSM은 한 번 그려 놓고 끝나는 문서가 아니다. 프로세스가 바뀌면 다시 측정해야 한다. 결국 VSM은 "흐름을 보는 습관"으로 기억해야 한다.

- **📢 섹션 요약 비유**: 지도를 한 번 그렸다고 길이 변하지 않는 건 아니다. 길이 바뀌면 다시 그려야 한다.

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [VSM](/studynote/15_devops_sre/01_culture_methodology/030_value_stream_mapping/)([Value Stream Mapping](/studynote/04_software_engineering/02_requirements_analysis/088_value_stream_mapping_vsm/)) | 전체 흐름 [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/) |
| [Lean](/studynote/04_software_engineering/02_requirements_analysis/087_lean_software_development_7_principles/) | 낭비 제거 철학 |
| Muda | 가치 없는 낭비 |
| WIP([Work In Progress](/studynote/04_software_engineering/uncategorized/661_kanban_wip_limit/)) | [진행](/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 중 작업 |
| [Lead Time](/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/) | 요청부터 인도까지 |
| TPS(Toyota Production System) | VSM의 뿌리 |

### 📈 관련 키워드 및 발전 흐름도

```text
Toyota Production System
    |
    v
Lean / Muda 제거
    |
    v
Value Stream Mapping
    |
    v
DevOps 파이프라인 진단
    |
    v
Lead Time 단축 / Flow 개선
```

이 흐름은 제조업의 낭비 제거 철학이 소프트웨어 흐름 진단으로 확장된 과정을 보여준다. 앞으로는 자동 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 수집과 결합해 더 자주, 더 정확하게 흐름을 볼 수 있다.

### 👶 어린이를 위한 3줄 비유 설명

1. 소풍길 지도를 보면 어디서 오래 멈추는지 알 수 있어요.
2. 길만 빠르면 소풍이 빨라지는 건 아니에요.
3. VSM은 전체 길을 그려서 막힌 곳을 찾는 지도예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 76 / 482

<- **이전**: [75. 애자일 PMO (Project Management Office) - 폭포수 통제를 넘어 애자일 지원 조직으로의 전환](/studynote/07_enterprise_systems/01_strategy_governance/075_agile_pmo_project_management_office/)
**다음**: [77. 엔터프라이즈 포털 (EP / EIP) - 기업 내 분산된 정보를 단일 창구로 통합 웹 제공](/studynote/07_enterprise_systems/01_strategy_governance/077_enterprise_portal_eip/) ->

---
