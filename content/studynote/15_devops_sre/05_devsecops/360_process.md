+++
title = "360. 가치 흐름 매핑 낭비 병목 식별 린 사상망 (Value Stream Mapping VSM Waste and Bottleneck Identification in Lean)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [VSM](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/030_value_stream_mapping/) ([Value Stream Mapping](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/088_value_stream_mapping_vsm/))은 린([Lean](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/087_lean_software_development_7_principles/)) 사상에서 비롯된 기법으로, 고객 가치가 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되는 전체 흐름을 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)해 낭비(Muda)와 병목을 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)하고 개선 우선순위를 결정하는 프로세스 분석 도구다.
> 2. **가치**: [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 맥락에서 VSM은 소프트웨어 아이디어부터 프로덕션 배포까지의 리드타임을 흐름도로 표현해 PCE ([Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/) Cycle Efficiency)를 측정하고, [DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) ([DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) Research and Assessment) 4대 지표와 연결해 개선 방향을 구체화한다.
> 3. **판단 포인트**: [현재 상태](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/) 맵([Current](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/002_current/)-[State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) Map)과 미래 상태 맵(Future-[State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) Map)의 격차에서 카이젠 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)트(Kaizen Burst) 우선순위를 결정할 때, 처리 시간([Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/) Time)이 아닌 대기 시간(Wait Time) 비율이 가장 큰 구간이 최우선 개선 대상이다.

---

## Ⅰ. 개요 및 필요성

[VSM](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/030_value_stream_mapping/) ([Value Stream Mapping](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/088_value_stream_mapping_vsm/))은 Toyota Production System의 린 제조 기법에서 출발해 소프트웨어 개발·[DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 영역으로 확장됐다. Karen Martin & Mike Osterling의 저서 "[Value Stream Mapping](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/088_value_stream_mapping_vsm/)"과 Gene Kim의 "The Phoenix [Project](/knowledge-base/studynote/05_database/01_db_architecture_relational/042_relational_algebra_project/)"가 소프트웨어 [VSM](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/030_value_stream_mapping/) 실천을 대중화했다.

소프트웨어 개발에서 아이디어 제안부터 코드가 프로덕션에 배포되기까지 평균 리드타임이 수 주~수 개월에 달하는 조직이 많다. 그러나 실제 부가 가치를 창출하는 처리 시간([Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/) Time)은 전체의 5~20%에 불과하다. 나머지 80~95%는 승인 대기, 환경 [프로비저닝](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/) 대기, 수동 테스트 대기 등의 낭비다.

낭비의 7가지 유형(Muda): 재고(Inventory, 미완성 코드), 과잉 처리(Over-Processing, 불필요 문서), [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)(Defects), 과잉 생산(Over-Production), 대기(Waiting), 운반(Transportation, 핸드오프), 동작 낭비(Motion, [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 전환). [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) VSM에서는 여기에 8번째 낭비인 직원 역량 미활용(Non-utilized Talent)을 추가한다.

- 📢 섹션 요약 비유: VSM은 배달 주문에서 음식이 테이블에 오기까지 모든 단계를 지도로 그리는 것이다. 요리 시간(5분)보다 주문 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 대기(20분), 배달원 배정 대기(15분)가 훨씬 길다면, 개선할 곳은 요리가 아니라 대기 구간이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
┌──────────────────────────────────────────────────────────────────┐
│                  현재 상태 VSM 예시 (소프트웨어)                  │
├──────────────────────────────────────────────────────────────────┤
│  고객 요청 → [기획] → [설계] → [개발] → [코드 리뷰] → [QA] → 배포│
│            PT:2h     PT:4h    PT:3d    PT:4h          PT:2d     │
│            WT:2d     WT:1d    WT:0d    WT:3d           WT:5d     │
│                                                                  │
│  총 리드타임: ~15d  │  총 처리시간: ~3.5d  │  PCE: ~23%          │
│                                                                  │
│  PCE (Process Cycle Efficiency) = 처리시간 / 리드타임 × 100       │
└──────────────────────────────────────────────────────────────────┘
```

| 구성 요소           | 정의                                      | 목표               |
| :------------------ | :---------------------------------------- | :----------------- |
| PT ([Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/) Time)   | 실제 작업이 이루어지는 시간               | 최소화 (자동화)    |
| WT (Wait Time)      | 다음 단계 시작을 기다리는 시간            | 제거 (최우선 개선) |
| [Lead Time](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/)           | PT + WT 합계, 고객 관점 전체 시간         | 최소화             |
| PCE                 | PT / [Lead Time](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/) × 100 (%)                  | > 25% 목표         |
| Kaizen Burst        | 개선 기회 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 마크 (번개 모양)           | WT가 큰 구간에 배치|

**[현재 상태](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/) 맵 → 미래 상태 맵 전환 단계**
1. [현재 상태](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/) 맵 작성: 모든 단계의 PT·WT·재고·핸드오프 수 측정
2. PCE 계산 및 낭비 유형 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)
3. 카이젠 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)트 표시: WT가 가장 큰 2~3개 구간
4. 미래 상태 맵: 자동화·단계 통합으로 목표 리드타임 설계
5. 구현 로드맵: 카이젠 프로젝트 우선순위화

[DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) [DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 4지표와의 연결: 변경 리드타임([Lead Time for Changes](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/024_lead_time_for_changes/))은 VSM의 개발→배포 구간, 배포 빈도는 VSM의 릴리스 주기, MTTR은 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) VSM과 직결된다.

- �� 섹션 요약 비유: PCE는 8시간 근무 중 실제로 일한 시간 비율이다. 대부분 회의 대기·승인 대기로 채워진다면, 일하는 방식이 아니라 기다리는 구조를 바꿔야 한다.

---

## Ⅲ. 비교 및 연결

| 항목               | 전통적 프로세스 개선       | [VSM](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/030_value_stream_mapping/) 기반 린 개선                    |
| :----------------- | :-------------------------- | :---------------------------------- |
| 접근 방식          | 개별 단계 효율화            | 전체 흐름 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) 후 병목 집중       |
| 측정 기준          | 단계별 처리 시간            | 리드타임·PCE·낭비 유형             |
| 개선 우선순위      | 직관 또는 관리자 판단       | PCE + WT [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기반 객관적 선정   |
| 팀 참여            | 전문가 중심                 | 전체 가치 흐름 참여자 워크숍        |
| 지속성             | 일회성 프로젝트             | 반복 측정·개선 사이클               |

VSM은 Platform Engineering과도 연결된다. [개발자 경험](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/058_dx_developer_experience/)(DevEx) 개선을 위해 [IDP](/knowledge-base/studynote/09_security/11_iam_access_control/536_idp_identity_provider/) ([Internal Developer Platform](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/200_internal_developer_platform_backstage/))를 구축할 때, VSM으로 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)한 가장 큰 WT 구간(예: 환경 [프로비저닝](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/) 3일 → 셀프 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 15분)을 플랫폼 기능 개발 우선순위로 삼는다.

- 📢 섹션 요약 비유: VSM은 음식점 운영 컨설팅에서 주방 동선 분석이다. 셰프 실력(처리 속도)보다 재료 가져오는 경로(대기 시간)를 줄이면 테이블 회전율이 더 빨리 오른다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**[VSM](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/030_value_stream_mapping/) 워크숍 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)**
1. 고객 가치 정의: "배포된 기능이 고객에게 전달되는 것"으로 시작점·끝점 명확화
2. 현장 관찰(Gemba Walk): 실제 작업자와 함께 단계별 PT·WT 직접 측정
3. 핸드오프 수 계산: 팀 간 전달(핸드오프) 발생 횟수 = 낭비 증가 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)
4. PCE 목표: 현재 PCE × 3배 이상 개선을 미래 상태 목표로 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)
5. 카이젠 프로젝트 선정: WT 상위 3개 구간에 자동화·통합·권한 위임 적용

**판단 기준**
- WT > PT × 3 구간: 즉각 자동화 우선 ([CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인, 승인 자동화)
- 핸드오프 > 5회: 팀 통합 또는 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 기반 자동 전달 도입
- 재작업(Rework) 루프 발견: 테스트 자동화로 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)을 상류에서 차단

**[안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)**
- PCE 측정 없이 "모든 단계 동시에 개선" → 리소스 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)으로 효과 미미
- [현재 상태](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/) 맵만 그리고 미래 상태 맵 없음 → 개선 방향 부재
- 처리 시간(PT)만 줄이고 대기 시간(WT) 무시 → 진짜 병목 미해결

- 📢 섹션 요약 비유: [VSM](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/030_value_stream_mapping/) 없이 개선하는 것은 눈 감고 집 청소하는 것이다. 어디가 더럽고 어디가 깨끗한지 보지 않고 청소 도구만 바꾸면 같은 곳만 반복해서 닦는다.

---

## Ⅴ. 기대효과 및 결론

[VSM](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/030_value_stream_mapping/) 적용 조직은 리드타임을 평균 50~75% 단축하고 PCE를 5~15%에서 25~40%로 개선한 사례들이 보고된다. [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 전환 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)에 VSM으로 [현재 상태](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)를 가시화하면, 기술 투자 우선순위를 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기반으로 결정할 수 있어 [ROI](/knowledge-base/studynote/12_it_management/01_governance_strategy/012_roi_return_on_investment/)(투자 대비 효과)가 높아진다.

한계로는 [VSM](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/030_value_stream_mapping/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집이 수동이면 부정확하고, 디지털 작업의 WT를 정확히 측정하기 어렵다는 점이 있다. 지속적 측정 없이 일회성으로 끝나면 개선 효과가 사라진다.

미래 방향은 Value [Stream](/knowledge-base/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/) [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/) 플랫폼(ConnectALL, Tasktop, Plutora)을 통한 자동화된 실시간 VSM이다. [DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 지표·Jira·Git을 통합해 리드타임을 자동 추적하고, AI가 병목 구간을 자동 탐지하는 방향으로 발전한다.

- 📢 섹션 요약 비유: VSM은 X-레이다. 겉으로 멀쩡해 보이는 프로세스의 내부 뼈대(흐름)를 투과해 보여주고, 어디서 골절(병목)이 있는지 정확하게 짚어 준다.

---

### 📌 관련 개념 맵

| 개념                                        | 연결 포인트                                              |
| :------------------------------------------ | :------------------------------------------------------- |
| 린 ([Lean](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/087_lean_software_development_7_principles/)) 사상                               | VSM의 철학적 기반, Muda(낭비) 7유형 포함                 |
| PCE ([Process](/knowledge-base/studynote/12_it_management/05_security_compliance/300_process/) Cycle Efficiency)              | VSM의 핵심 지표, PT/[Lead Time](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/) 비율                       |
| [DORA 4](/knowledge-base/studynote/15_devops_sre/05_devsecops/285_dora_4/) [Metrics](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/567_metrics_time_series_prometheus_grafana/)                              | 변경 리드타임, 배포 빈도와 [VSM](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/030_value_stream_mapping/) 직결                      |
| Kaizen (카이젠)                              | 점진적 개선, 카이젠 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)트가 VSM에서 개선 우선순위 표시   |
| [Platform Engineering](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/109_platform_engineering_cognitive_load/) / [IDP](/knowledge-base/studynote/09_security/11_iam_access_control/536_idp_identity_provider/)                  | [VSM](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/030_value_stream_mapping/) 병목 구간 자동화의 구현 수단                         |
| Value [Stream](/knowledge-base/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/) [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/)                     | VSM을 디지털화·자동화한 플랫폼 도구 범주                 |

### 📈 관련 키워드 및 발전 흐름도

```text
린 (Lean) 제조 — Toyota Production System
    │
    ▼
VSM (Value Stream Mapping) — 흐름 시각화·낭비 식별
    │
    ▼
PCE 측정 — 처리시간/리드타임 비율
    │
    ▼
카이젠 버스트 — 우선순위 개선 구간 선정
    │
    ▼
DevOps DORA 지표 — 변경 리드타임·배포 빈도 연결
    │
    ▼
Value Stream Management 플랫폼 — 실시간 자동 측정
```

흐름은 "제조 린 → 소프트웨어 [VSM](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/030_value_stream_mapping/) → 정량 지표 → 자동화 → 플랫폼 통합"으로 발전한다.

### 👶 어린이를 위한 3줄 비유 설명

1. VSM은 내가 학교 숙제를 시작해서 제출하기까지 어디서 시간이 가장 많이 걸리는지 지도로 그리는 거예요.
2. "숙제하는 시간(1시간)"보다 "게임하다가 시작 못 한 시간(3시간)"이 더 크면, 게임 시간을 줄이는 게 정답이에요.
3. PCE는 전체 시간 중 진짜 일한 시간 비율인데, 이게 낮을수록 낭비가 많다는 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 360 / 373

← **이전**: [359. 시맨틱 캐시 RAG 비용 응답 단축 계층 (Semantic Cache for RAG Cost and Latency Reduction)](/knowledge-base/studynote/15_devops_sre/05_devsecops/359_metric/)
**다음**: [361. 컨웨이의 법칙 조직 구조 소프트웨어 반영 아키텍처 (Conway Law Organizational Structure Reflected](/knowledge-base/studynote/15_devops_sre/05_devsecops/361_architecture/) →

---
