---
title: 360. 가치 흐름 매핑 낭비 병목 식별 린 사상망 (Value Stream Mapping VSM Waste and Bottleneck
  Identification in Lean)
date: '2026-05-09'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[030_value_stream_mapping|VSM]] ([[088_value_stream_mapping_vsm|Value Stream Mapping]])은 린([[087_lean_software_development_7_principles|Lean]]) 사상에서 비롯된 기법으로, 고객 가치가 [[087_process_state_transition|생성]]되는 전체 흐름을 [[003_bigdata_7v|시각화]]해 낭비(Muda)와 병목을 [[655_ir_detection_analysis|식별]]하고 개선 우선순위를 결정하는 프로세스 분석 도구다.
> 2. **가치**: [[652_devops_calms_culture|DevOps]] 맥락에서 VSM은 소프트웨어 아이디어부터 프로덕션 배포까지의 리드타임을 흐름도로 표현해 PCE ([[300_process|Process]] Cycle Efficiency)를 측정하고, [[523_dhcp_dora_process|DORA]] ([[652_devops_calms_culture|DevOps]] Research and Assessment) 4대 지표와 연결해 개선 방향을 구체화한다.
> 3. **판단 포인트**: [[178_as_is_to_be_analysis|현재 상태]] 맵([[002_current|Current]]-[[272_state_pattern|State]] Map)과 미래 상태 맵(Future-[[272_state_pattern|State]] Map)의 격차에서 카이젠 [[344_bus|버스]]트(Kaizen Burst) 우선순위를 결정할 때, 처리 시간([[300_process|Process]] Time)이 아닌 대기 시간(Wait Time) 비율이 가장 큰 구간이 최우선 개선 대상이다.

---

## Ⅰ. 개요 및 필요성

[[030_value_stream_mapping|VSM]] ([[088_value_stream_mapping_vsm|Value Stream Mapping]])은 Toyota Production System의 린 제조 기법에서 출발해 소프트웨어 개발·[[652_devops_calms_culture|DevOps]] 영역으로 확장됐다. Karen Martin & Mike Osterling의 저서 "[[088_value_stream_mapping_vsm|Value Stream Mapping]]"과 Gene Kim의 "The Phoenix [[042_relational_algebra_project|Project]]"가 소프트웨어 [[030_value_stream_mapping|VSM]] 실천을 대중화했다.

소프트웨어 개발에서 아이디어 제안부터 코드가 프로덕션에 배포되기까지 평균 리드타임이 수 주~수 개월에 달하는 조직이 많다. 그러나 실제 부가 가치를 창출하는 처리 시간([[300_process|Process]] Time)은 전체의 5~20%에 불과하다. 나머지 80~95%는 승인 대기, 환경 [[528_provisioning|프로비저닝]] 대기, 수동 테스트 대기 등의 낭비다.

낭비의 7가지 유형(Muda): 재고(Inventory, 미완성 코드), 과잉 처리(Over-Processing, 불필요 문서), [[352_defect_definition|결함]](Defects), 과잉 생산(Over-Production), 대기(Waiting), 운반(Transportation, 핸드오프), 동작 낭비(Motion, [[033_context|컨텍스트]] 전환). [[652_devops_calms_culture|DevOps]] VSM에서는 여기에 8번째 낭비인 직원 역량 미활용(Non-utilized Talent)을 추가한다.

- 📢 섹션 요약 비유: VSM은 배달 주문에서 음식이 테이블에 오기까지 모든 단계를 지도로 그리는 것이다. 요리 시간(5분)보다 주문 [[396_validation|확인]] 대기(20분), 배달원 배정 대기(15분)가 훨씬 길다면, 개선할 곳은 요리가 아니라 대기 구간이다.

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
| PT ([[300_process|Process]] Time)   | 실제 작업이 이루어지는 시간               | 최소화 (자동화)    |
| WT (Wait Time)      | 다음 단계 시작을 기다리는 시간            | 제거 (최우선 개선) |
| [[085_lead_time_cycle_time|Lead Time]]           | PT + WT 합계, 고객 관점 전체 시간         | 최소화             |
| PCE                 | PT / [[085_lead_time_cycle_time|Lead Time]] × 100 (%)                  | > 25% 목표         |
| Kaizen Burst        | 개선 기회 [[655_ir_detection_analysis|식별]] 마크 (번개 모양)           | WT가 큰 구간에 배치|

**[[178_as_is_to_be_analysis|현재 상태]] 맵 → 미래 상태 맵 전환 단계**
1. [[178_as_is_to_be_analysis|현재 상태]] 맵 작성: 모든 단계의 PT·WT·재고·핸드오프 수 측정
2. PCE 계산 및 낭비 유형 [[104_classification_analysis|분류]]
3. 카이젠 [[344_bus|버스]]트 표시: WT가 가장 큰 2~3개 구간
4. 미래 상태 맵: 자동화·단계 통합으로 목표 리드타임 설계
5. 구현 로드맵: 카이젠 프로젝트 우선순위화

[[652_devops_calms_culture|DevOps]] [[523_dhcp_dora_process|DORA]] 4지표와의 연결: 변경 리드타임([[024_lead_time_for_changes|Lead Time for Changes]])은 VSM의 개발→배포 구간, 배포 빈도는 VSM의 릴리스 주기, MTTR은 장애 [[658_ir_recovery|복구]] VSM과 직결된다.

- �� 섹션 요약 비유: PCE는 8시간 근무 중 실제로 일한 시간 비율이다. 대부분 회의 대기·승인 대기로 채워진다면, 일하는 방식이 아니라 기다리는 구조를 바꿔야 한다.

---

## Ⅲ. 비교 및 연결

| 항목               | 전통적 프로세스 개선       | [[030_value_stream_mapping|VSM]] 기반 린 개선                    |
| :----------------- | :-------------------------- | :---------------------------------- |
| 접근 방식          | 개별 단계 효율화            | 전체 흐름 [[003_bigdata_7v|시각화]] 후 병목 집중       |
| 측정 기준          | 단계별 처리 시간            | 리드타임·PCE·낭비 유형             |
| 개선 우선순위      | 직관 또는 관리자 판단       | PCE + WT [[001_dikw_pyramid|데이터]] 기반 객관적 선정   |
| 팀 참여            | 전문가 중심                 | 전체 가치 흐름 참여자 워크숍        |
| 지속성             | 일회성 프로젝트             | 반복 측정·개선 사이클               |

VSM은 Platform Engineering과도 연결된다. [[058_dx_developer_experience|개발자 경험]](DevEx) 개선을 위해 [[536_idp_identity_provider|IDP]] ([[200_internal_developer_platform_backstage|Internal Developer Platform]])를 구축할 때, VSM으로 [[655_ir_detection_analysis|식별]]한 가장 큰 WT 구간(예: 환경 [[528_provisioning|프로비저닝]] 3일 → 셀프 [[090_service_kubernetes_network_load_balancing|서비스]] 15분)을 플랫폼 기능 개발 우선순위로 삼는다.

- 📢 섹션 요약 비유: VSM은 음식점 운영 컨설팅에서 주방 동선 분석이다. 셰프 실력(처리 속도)보다 재료 가져오는 경로(대기 시간)를 줄이면 테이블 회전율이 더 빨리 오른다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**[[030_value_stream_mapping|VSM]] 워크숍 [[216_progress_in_synchronization|진행]] [[435_checklist_based_testing|체크리스트]]**
1. 고객 가치 정의: "배포된 기능이 고객에게 전달되는 것"으로 시작점·끝점 명확화
2. 현장 관찰(Gemba Walk): 실제 작업자와 함께 단계별 PT·WT 직접 측정
3. 핸드오프 수 계산: 팀 간 전달(핸드오프) 발생 횟수 = 낭비 증가 [[130_signal|신호]]
4. PCE 목표: 현재 PCE × 3배 이상 개선을 미래 상태 목표로 [[009_config|설정]]
5. 카이젠 프로젝트 선정: WT 상위 3개 구간에 자동화·통합·권한 위임 적용

**판단 기준**
- WT > PT × 3 구간: 즉각 자동화 우선 ([[090_configuration_item|CI]] [[123_pipe|파이프]]라인, 승인 자동화)
- 핸드오프 > 5회: 팀 통합 또는 [[014_api_posix|API]] 기반 자동 전달 도입
- 재작업(Rework) 루프 발견: 테스트 자동화로 [[352_defect_definition|결함]]을 상류에서 차단

**[[128_water_scrum_fall_anti_pattern|안티패턴]]**
- PCE 측정 없이 "모든 단계 동시에 개선" → 리소스 [[136_variance|분산]]으로 효과 미미
- [[178_as_is_to_be_analysis|현재 상태]] 맵만 그리고 미래 상태 맵 없음 → 개선 방향 부재
- 처리 시간(PT)만 줄이고 대기 시간(WT) 무시 → 진짜 병목 미해결

- 📢 섹션 요약 비유: [[030_value_stream_mapping|VSM]] 없이 개선하는 것은 눈 감고 집 청소하는 것이다. 어디가 더럽고 어디가 깨끗한지 보지 않고 청소 도구만 바꾸면 같은 곳만 반복해서 닦는다.

---

## Ⅴ. 기대효과 및 결론

[[030_value_stream_mapping|VSM]] 적용 조직은 리드타임을 평균 50~75% 단축하고 PCE를 5~15%에서 25~40%로 개선한 사례들이 보고된다. [[652_devops_calms_culture|DevOps]] 전환 [[459_quic_fec_forward_error_correction|초기]]에 VSM으로 [[178_as_is_to_be_analysis|현재 상태]]를 가시화하면, 기술 투자 우선순위를 [[001_dikw_pyramid|데이터]] 기반으로 결정할 수 있어 [[012_roi_return_on_investment|ROI]](투자 대비 효과)가 높아진다.

한계로는 [[030_value_stream_mapping|VSM]] [[001_dikw_pyramid|데이터]] 수집이 수동이면 부정확하고, 디지털 작업의 WT를 정확히 측정하기 어렵다는 점이 있다. 지속적 측정 없이 일회성으로 끝나면 개선 효과가 사라진다.

미래 방향은 Value [[467_http2_stream_multiplexing_tcp_hol|Stream]] [[372_management|Management]] 플랫폼(ConnectALL, Tasktop, Plutora)을 통한 자동화된 실시간 VSM이다. [[523_dhcp_dora_process|DORA]] 지표·Jira·Git을 통합해 리드타임을 자동 추적하고, AI가 병목 구간을 자동 탐지하는 방향으로 발전한다.

- 📢 섹션 요약 비유: VSM은 X-레이다. 겉으로 멀쩡해 보이는 프로세스의 내부 뼈대(흐름)를 투과해 보여주고, 어디서 골절(병목)이 있는지 정확하게 짚어 준다.

---

### 📌 관련 개념 맵

| 개념                                        | 연결 포인트                                              |
| :------------------------------------------ | :------------------------------------------------------- |
| 린 ([[087_lean_software_development_7_principles|Lean]]) 사상                               | VSM의 철학적 기반, Muda(낭비) 7유형 포함                 |
| PCE ([[300_process|Process]] Cycle Efficiency)              | VSM의 핵심 지표, PT/[[085_lead_time_cycle_time|Lead Time]] 비율                       |
| [[285_dora_4|DORA 4]] [[567_metrics_time_series_prometheus_grafana|Metrics]]                              | 변경 리드타임, 배포 빈도와 [[030_value_stream_mapping|VSM]] 직결                      |
| Kaizen (카이젠)                              | 점진적 개선, 카이젠 [[344_bus|버스]]트가 VSM에서 개선 우선순위 표시   |
| [[109_platform_engineering_cognitive_load|Platform Engineering]] / [[536_idp_identity_provider|IDP]]                  | [[030_value_stream_mapping|VSM]] 병목 구간 자동화의 구현 수단                         |
| Value [[467_http2_stream_multiplexing_tcp_hol|Stream]] [[372_management|Management]]                     | VSM을 디지털화·자동화한 플랫폼 도구 범주                 |

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

흐름은 "제조 린 → 소프트웨어 [[030_value_stream_mapping|VSM]] → 정량 지표 → 자동화 → 플랫폼 통합"으로 발전한다.

### 👶 어린이를 위한 3줄 비유 설명

1. VSM은 내가 학교 숙제를 시작해서 제출하기까지 어디서 시간이 가장 많이 걸리는지 지도로 그리는 거예요.
2. "숙제하는 시간(1시간)"보다 "게임하다가 시작 못 한 시간(3시간)"이 더 크면, 게임 시간을 줄이는 게 정답이에요.
3. PCE는 전체 시간 중 진짜 일한 시간 비율인데, 이게 낮을수록 낭비가 많다는 [[130_signal|신호]]예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 360 / 373

← **이전**: [[359_metric|359. 시맨틱 캐시 RAG 비용 응답 단축 계층 (Semantic Cache for RAG Cost and Latency Reduction)]]
**다음**: [[361_architecture|361. 컨웨이의 법칙 조직 구조 소프트웨어 반영 아키텍처 (Conway Law Organizational Structure Reflected]] →

---
