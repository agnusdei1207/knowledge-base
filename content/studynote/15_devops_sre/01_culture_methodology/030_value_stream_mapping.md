+++
title = "30. 가치 흐름 맵핑 (VSM) — 낭비를 찾아 흐름을 최적화"
date = 2026-04-29

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: VSM([Value Stream Mapping](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/088_value_stream_mapping_vsm/), 가치 흐름 맵핑)은 린([Lean](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/087_lean_software_development_7_principles/)) 제조에서 소프트웨어 전달로 이식된 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) 도구로, 아이디어부터 고객 전달까지 모든 단계의 작업 시간·대기 시간·낭비를 맵으로 그려서 분석한다.
> 2. **가치**: 소프트웨어 전달에서 전체 [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/)의 85~95%는 실제 작업이 아닌 대기 시간([Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/) Time)이다. VSM은 이 대기 시간의 원인을 가시화하여 가장 큰 개선 레버를 찾아준다.
> 3. **판단 포인트**: VSM은 [현재 상태](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)([Current](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/002_current/) [State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/))와 미래 상태(Future [State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/)) 두 맵을 그리는 것이 핵심이다. 현재 맵으로 낭비를 찾고, 미래 맵으로 개선 목표를 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)하여 팀 공감대를 형성한다.

---

## Ⅰ. 개요 및 필요성

```text
VSM 소프트웨어 전달 예시:

단계          작업 시간  대기 시간
아이디어->기획   0.5일      3일
기획->개발       0일        2일 (스프린트 대기)
개발            5일        1일 (코드 리뷰 대기)
테스트          2일        3일 (환경 대기)
배포 승인       0.5일      5일 (승인 대기)

총 리드 타임: 22일
총 작업 시간:  8일 (36%)
총 대기 시간: 14일 (64%) <- 여기서 낭비 제거!
```

- **📢 섹션 요약 비유**: VSM은 택배 배송 경로 분석이다. 택배 포장(1분)+운반(2분)+검수(1분)+배달(10분) 총 작업 14분인데, 총 배달 시간이 3일이라면 나머지 2일 23시간 46분이 대기 시간이다. VSM은 이 낭비를 찾는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### VSM 핵심 기호와 측정

| 기호/개념 | 의미 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/943_process/">Process</a> Box</strong> | 실제 작업 단계 |
| **Push 화살표** | 이전 단계가 밀어주는 흐름 |
| **Pull 화살표** | 다음 단계가 당기는 흐름 |
| **재고 삼각형** | 작업 대기 중인 항목 수 |
| **작업 시간(PT)** | 실제 가치 창출 시간 |
| **대기 시간(WT)** | 다음 단계로 이동 대기 |
| **PCE** | [Process](/knowledge-base/studynote/12_it_management/05_security_compliance/943_process/) Cycle Efficiency = PT/(PT+WT) |

### 린 낭비 8가지 ([TIM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/737_thermal_paste_tim/) WOODS)

```text
T: Transport — 불필요한 이동·핸드오프
I: Inventory — 재고·작업 대기 (WIP)
M: Motion — 불필요한 움직임
W: Waiting — 대기 시간
O: Over-processing — 과잉 처리
O: Over-production — 불필요한 기능 개발
D: Defects — 버그·재작업
S: Skills — 인재 미활용
```

- **📢 섹션 요약 비유**: [TIM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/737_thermal_paste_tim/) WOODS 8 낭비는 식당 낭비 8가지다. 주방 동선 낭비(Motion), 재료 과잉 준비(Inventory), 손님 대기(Waiting), 불필요한 조리 단계(Over-processing) 등 모든 낭비가 매출(전달 속도)을 갉아먹는다.

---

## Ⅲ. 비교 및 연결

| 비교 | VSM | [DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) | [OKR](/knowledge-base/studynote/12_it_management/01_governance_strategy/831_okr_objectives_key_results/) |
|:---|:---|:---|:---|
| 초점 | 현재 흐름 분석 | 성과 측정 | 목표·결과 추적 |
| 산출물 | 시각적 맵 | 4대 [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) | 분기 목표 |
| 피드백 주기 | 분기·연간 | 지속적 | 분기 |

- **📢 섹션 요약 비유**: VSM·[DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/)·OKR은 공장 개선 3단계다. VSM으로 현재 문제를 찾고(진단), [DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)으로 개선을 측정하며([모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링), OKR로 개선 목표를 달성한다(목표 추진).

---

## Ⅳ. 실무 적용 및 기술사 판단

### VSM 실시 절차

```text
1. 제품 패밀리 선택 (VSM 범위 정의)
2. 현재 상태 맵 작성 (As-Is)
   - 모든 단계 작업 시간·대기 시간 측정
   - 재고(WIP) 수량 기록
   - PCE 계산
3. 낭비 식별 및 근본 원인 분석
4. 미래 상태 맵 작성 (To-Be)
   - 낭비 제거 후 목표 상태
   - 연속 흐름(Continuous Flow) 설계
5. 개선 계획 수립 및 실행
6. 개선 효과 측정 -> 반복
```

### 공공 IT 사업 VSM 적용

```text
현재 상태 병목:
  요구사항 -> 설계 승인: 15일 대기 (PMO 검토)
  개발 완료 -> 테스트 환경: 7일 대기 (환경 구성)
  테스트 -> 운영 배포: 21일 대기 (감리 보고)

개선 방향:
  PMO 자동화 검토 -> 승인 대기 5일로 단축
  IaC 온디맨드 테스트 환경 -> 당일 구성
  CD 파이프라인 -> 배포 대기 3일로 단축
```

- **📢 섹션 요약 비유**: 공공 IT VSM 개선은 행정 절차 간소화다. 민원 처리 21일 걸리던 것을 전자정부 시스템으로 3일로 단축한 것처럼, IT 배포 프로세스의 불필요한 대기를 자동화로 제거한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/">리드 타임</a> 단축</strong> | 대기 시간 제거로 배포 속도 향상 |
| **팀 공감대** | 시각적 맵으로 전체 흐름 이해 공유 |
| **PCE 향상** | 실제 작업 비율 증가 |

[AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 자동 VSM [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 도구가 등장하고 있다. GitHub Actions [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·JIRA 이슈·배포 이력을 자동 수집하여 [현재 상태](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/) VSM을 자동 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하고, AI가 주요 병목을 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)하여 개선 방안을 제안하는 엔진ering Intelligence 플랫폼이 LinearB·Swarmia 등에서 실용화되고 있다.

- **📢 섹션 요약 비유**: [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) VSM 자동화는 스마트 공장 생산성 분석이다. 공장 모든 센서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 AI가 분석해서 "라인 3번이 병목이에요"라고 실시간 알려주는 것처럼, AI가 개발 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 병목을 자동 진단한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **린 소프트웨어** | VSM 이론적 기원 |
| <strong><a href="/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/">DORA</a> <a href="/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/">메트릭</a></strong> | VSM 개선 측정 지표 |
| **WIP 제한** | 재고 낭비 제거 수단 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/084_kanban_board_wip_limit/">칸반</a></strong> | VSM 흐름 관리 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) |
| **엔진ering Intelligence** | [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 자동 VSM |

### 📈 관련 키워드 및 발전 흐름도

```text
[린 제조 VSM — 공장 생산 흐름 낭비 분석]
    |
    v
[소프트웨어 VSM — IT 전달 파이프라인 적용]
    |
    v
[DORA 메트릭 — VSM 개선 성과 측정]
    |
    v
[칸반·WIP 제한 — 흐름 최적화 실천 도구]
    |
    v
[AI VSM — 자동 생성·실시간 병목 분석]
```

### 👶 어린이를 위한 3줄 비유 설명

1. VSM은 택배 배송 경로 분석이에요 — 포장·운반·배달 중 어디서 시간이 가장 많이 낭비되는지 찾아요!
2. 소프트웨어 전달의 64%는 실제 작업이 아닌 대기 시간이에요 — VSM으로 이걸 찾아서 제거해요!
3. AI가 개발 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인을 분석해서 병목을 자동으로 알려주는 시대가 오고 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 30 / 373

<- **이전**: [29. 골든 패스와 가치 흐름 (Golden Path & Value Stream)](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/029_golden_path_value_stream/)
**다음**: [31. 리드 타임과 사이클 타임 — DevOps 흐름 핵심 지표](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/031_lead_time_cycle_time/) ->

---
