---
title: 31. 리드 타임과 사이클 타임 — DevOps 흐름 핵심 지표
date: '2026-04-29'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[085_lead_time_cycle_time|리드 타임]]([[085_lead_time_cycle_time|Lead Time]])은 고객 요청부터 배포까지 총 시간이고, 사이클 타임(Cycle Time)은 개발 시작부터 배포까지 시간이다. [[085_lead_time_cycle_time|Lead Time]] ≥ Cycle Time이며, 둘의 차이가 "요청 대기 시간"이다.
> 2. **가치**: [[523_dhcp_dora_process|DORA]]([[652_devops_calms_culture|DevOps]] Research and Assessment) [[342_routing_metric_hop_bandwidth_delay|메트릭]]의 4대 지표 중 하나가 "변경 [[085_lead_time_cycle_time|리드 타임]]([[024_lead_time_for_changes|Lead Time for Changes]])"이다. Elite 팀은 [[085_lead_time_cycle_time|리드 타임]]이 1시간 미만이고, Low 팀은 6개월 이상이다.
> 3. **판단 포인트**: [[085_lead_time_cycle_time|리드 타임]] 단축의 최대 레버는 배치 크기([[346_batch_size_generalization|Batch Size]]) 축소다. 작은 변경을 자주 배포하면([[164_continuous_delivery|Continuous Delivery]]) [[085_lead_time_cycle_time|리드 타임]]이 극적으로 줄고 [[098_rollback_strategy_pipeline_error_threshold|롤백]] 위험도 낮아진다.

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

- **📢 섹션 요약 비유**: [[085_lead_time_cycle_time|리드 타임]] vs 사이클 타임은 피자 주문과 요리 시간이다. 주문에서 수령까지([[085_lead_time_cycle_time|리드 타임]])에는 주문 대기(리드-사이클 차이)와 실제 요리 시간(사이클 타임)이 포함된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[523_dhcp_dora_process|DORA]] [[342_routing_metric_hop_bandwidth_delay|메트릭]] 성숙도 등급

| 지표 | Elite | High | Medium | Low |
|:---|:---|:---|:---|:---|
| **배포 빈도** | 하루 여러 번 | 하루 1번~주1 | 주1~월1 | 월1 미만 |
| **[[085_lead_time_cycle_time|리드 타임]]** | < 1시간 | 1일~1주 | 1주~1개월 | 1~6개월+ |
| **[[658_ir_recovery|복구]] 시간** | < 1시간 | < 1일 | < 1주 | 1~6개월 |
| **변경 실패율** | 0~15% | 16~30% | 16~30% | 16~30% |

### [[085_lead_time_cycle_time|리드 타임]] 단축 [[268_strategy_pattern|전략]]

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

- **📢 섹션 요약 비유**: 배치 크기 축소는 배달 방식 개선이다. 하루치 배달을 한 번에 큰 트럭으로 하면 오래 기다리지만, 여러 번 소량 배달하면 각 고객이 더 빨리 받는다. 소프트웨어도 작게 자주 배포하면 [[085_lead_time_cycle_time|리드 타임]]이 줄어든다.

---

## Ⅲ. 비교 및 연결

| 비교 | [[085_lead_time_cycle_time|리드 타임]] | 사이클 타임 | [[139_throughput|처리량]] |
|:---|:---|:---|:---|
| 측정 범위 | 요청→배포 (전체) | 개발→배포 | 단위 시간 완료 수 |
| 고객 관점 | 직접적 (대기 경험) | 간접적 | 생산성 지표 |
| 개선 포인트 | 대기 제거 | 개발 속도 | [[430_index_fast_full_scan|병렬]]화 |

- **📢 섹션 요약 비유**: 리드·사이클·[[139_throughput|처리량]]은 음식점 [[018_kpi|KPI]] 세 가지다. 주문부터 수령 시간([[085_lead_time_cycle_time|리드 타임]]), 실제 조리 시간(사이클 타임), 시간당 서빙 수([[139_throughput|처리량]])를 함께 관리해야 완전한 [[090_service_kubernetes_network_load_balancing|서비스]] 품질을 [[396_validation|확인]]할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[085_lead_time_cycle_time|리드 타임]] 측정 도구

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

- **📢 섹션 요약 비유**: 리틀의 법칙은 줄 서기 대기 이론이다. 계산대([[139_throughput|처리량]])가 같아도 줄(WIP)이 짧으면 결제 대기 시간([[085_lead_time_cycle_time|리드 타임]])이 줄어든다. 한 번에 너무 많은 일을 시작하면 모든 일이 늦어진다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **고객 가치** | 빠른 기능 전달 → 경쟁 우위 |
| **품질** | 소규모 변경 → [[098_rollback_strategy_pipeline_error_threshold|롤백]] 쉬움·버그 감소 |
| **[[058_dx_developer_experience|개발자 경험]]** | 빠른 피드백 → 높은 만족도 |

[[190_ai_llm_requirements_specification|AI]] [[330_code_review|코드 리뷰]](GitHub Copilot for [[067_pull_request_pr_merge_request_code_review|PR]])·자동화 테스트 [[087_process_state_transition|생성]]·[[190_ai_llm_requirements_specification|AI]] 배포 의사결정이 사이클 타임 단축의 새로운 레버가 되고 있다. AI가 [[330_code_review|코드 리뷰]] 시간을 시간 단위에서 분 단위로 단축하면 Elite 팀의 [[085_lead_time_cycle_time|리드 타임]] 1시간 미만 목표가 대부분의 팀에게 현실이 될 수 있다.

- **📢 섹션 요약 비유**: [[190_ai_llm_requirements_specification|AI]] [[330_code_review|코드 리뷰]]는 즉각 피드백 교사다. 학생(개발자)이 숙제(코드)를 제출하면 [[190_ai_llm_requirements_specification|AI]] 선생님이 1분 안에 피드백을 주어 기다림([[085_lead_time_cycle_time|리드 타임]]) 없이 다음 단계로 [[216_progress_in_synchronization|진행]]할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[523_dhcp_dora_process|DORA]] [[342_routing_metric_hop_bandwidth_delay|메트릭]]** | [[085_lead_time_cycle_time|리드 타임]] 성숙도 벤치마크 |
| **WIP 제한** | 리틀의 법칙 기반 [[085_lead_time_cycle_time|리드 타임]] 단축 |
| **배치 크기** | 소규모 빈번 배포 [[268_strategy_pattern|전략]] |
| **[[084_kanban_board_wip_limit|칸반]]** | WIP 제한 시각적 관리 |
| **[[190_ai_llm_requirements_specification|AI]] [[330_code_review|코드 리뷰]]** | 사이클 타임 단축 [[190_ai_llm_requirements_specification|AI]] 레버 |

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

1. [[085_lead_time_cycle_time|리드 타임]]은 피자 주문부터 수령까지, 사이클 타임은 실제 요리 시간이에요!
2. 작은 변경을 자주 배포하면 [[085_lead_time_cycle_time|리드 타임]]이 줄어들고 문제가 생겨도 쉽게 되돌릴 수 있어요!
3. [[190_ai_llm_requirements_specification|AI]] [[330_code_review|코드 리뷰]] 덕분에 기다리는 시간([[085_lead_time_cycle_time|리드 타임]])을 1시간 이내로 줄이는 Elite 팀이 늘고 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 31 / 373

← **이전**: [[030_value_stream_mapping|30. 가치 흐름 맵핑 (VSM) — 낭비를 찾아 흐름을 최적화]]
**다음**: [[032_conways_law|콘웨이의 법칙 (Conway's Law)]] →

---
