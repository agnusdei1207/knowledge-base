---
title: 113. 카오스 엔지니어링 (Chaos Engineering) - Chaos Monkey·정상 상태 가설·실험 설계
date: '2026-04-19'
tags:
- studynote-software-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[751_chaos_engineering|카오스 엔지니어링]]은 프로덕션 환경에 **의도적으로 장애(서버 종료·[[1002_network_delay_rtt_oneway_delay_components|네트워크 지연]]·디스크 고장)를 주입**하여, 시스템의 복원력(Resilience)을 사전 [[395_verification_process_review|검증]]하는 실험 기반 규율이다.
> 2. **가치**: "장애는 반드시 온다"는 전제 하에, **Game Day(장애 훈련)**를 통해 모니터링·오토스케일링·[[307_circuit_breaker_pattern|서킷 브레이커]] 등 방어 메커니즘이 **실제로 작동하는지** [[395_verification_process_review|검증]]한다. 금요일 오후 5시에 서버가 죽어도 자동 [[658_ir_recovery|복구]]되는 시스템이 목표다.
> 3. **판단 포인트**: Netflix [[149_chaos_monkey_chaos_mesh|Chaos Monkey]](인스턴스 랜덤 종료)에서 시작하여, **Litmus·Gremlin·Chaos [[389_mesh_topology|Mesh]]**가 K8s 네이티브 카오스 도구로 진화했으며, 실험은 반드시 **정상 상태 가설([[151_steady_state_hypothesis_validation|Steady State Hypothesis]]) → 주입 → 관찰 → [[395_verification_process_review|검증]]**의 과학적 방법론을 따른다.

---

## Ⅰ. 개요 및 필요성

[[619_msa_traffic_hardware|MSA]] 100개 [[090_service_kubernetes_network_load_balancing|서비스]]가 그물망처럼 연결된 환경에서, "[[090_service_kubernetes_network_load_balancing|서비스]] A가 죽으면 B→C→D가 연쇄 장애를 일으키는가?"를 사전에 [[395_verification_process_review|검증]]하지 않으면, **실제 장애 시 [[451_mttr|MTTR]]([[658_ir_recovery|복구]] 시간)이 수시간**으로 폭발한다.

```text
┌───────────────────────────────────────────────────────┐
│    카오스 엔지니어링 실험 사이클                        │
├───────────────────────────────────────────────────────┤
│  1. 정상 상태 정의 (Steady State)                     │
│     "주문 API 응답 시간 < 200ms, 에러율 < 0.1%"      │
│                 │                                     │
│  2. 가설 수립                                         │
│     "결제 서비스 1대 종료해도 정상 상태 유지"          │
│                 │                                     │
│  3. 장애 주입 (Fault Injection)                       │
│     Chaos Monkey가 결제 서비스 Pod 1개 Kill           │
│                 │                                     │
│  4. 관찰 및 검증                                      │
│     Grafana에서 응답 시간·에러율 모니터링              │
│     → 200ms 이하 유지? ✅ 통과 / ❌ 개선 필요         │
│                 │                                     │
│  5. 개선 후 반복                                      │
│     서킷 브레이커 미작동 발견 → 설정 수정 → 재실험    │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[751_chaos_engineering|카오스 엔지니어링]]은 건물(시스템)에 인공 지진을 일으켜 내진 설계가 진짜 작동하는지 [[396_validation|확인]]하는 **내진 테스트**다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 장애 유형별 주입 도구

| 장애 유형 | 주입 내용 | 대표 도구 |
|:---|:---|:---|
| **인스턴스 종료** | [[198_pod_kubernetes_minimum_deployment_unit|Pod]]/[[598_vm_migration_nic|VM]] 랜덤 Kill | [[149_chaos_monkey_chaos_mesh|Chaos Monkey]], Litmus |
| **[[1002_network_delay_rtt_oneway_delay_components|네트워크 지연]]** | 100~5000ms 인위적 레이턴시 | Chaos [[389_mesh_topology|Mesh]], Gremlin |
| **네트워크 [[514_partition_slice_volume|파티션]]** | [[090_service_kubernetes_network_load_balancing|서비스]] 간 통신 차단 | Toxiproxy |
| **디스크 고장** | I/O 에러 주입 | Litmus |
| **CPU/메모리 스트레스** | 자원 고갈 시뮬레이션 | Gremlin |

### 폭발 반경 (Blast [[541_radius_remote_authentication_aaa|Radius]]) 관리

카오스 실험은 반드시 **소규모 → 확대**로 진행한다. Dev → Staging → [[595_canary_stack_smashing_protector|Canary]](프로덕션 5%) → 전체.

- **📢 섹션 요약 비유**: 소방 훈련에서 처음에는 작은 불(Dev)을 끄는 연습을 하고, 자신감이 생기면 큰 불(프로덕션)로 확대하는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 전통 테스트 | [[751_chaos_engineering|카오스 엔지니어링]] |
|:---|:---|:---|
| **환경** | 테스트 환경 | **프로덕션** (가능 시) |
| **대상** | 기능 [[002_bigdata_5v|정확성]] | **복원력 (Resilience)** |
| **장애** | 예측된 시나리오 | **미지의 장애 탐색** |
| **주기** | 릴리즈 시 | **상시 (자동화)** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### Game Day [[435_checklist_based_testing|체크리스트]]
1. **범위 확정**: 어떤 [[090_service_kubernetes_network_load_balancing|서비스]]에 어떤 장애를 주입할지 사전 정의.
2. **관찰 도구 [[396_validation|확인]]**: [[168_grafana|Grafana]]·Datadog 대시보드가 실시간 반영되는지 [[396_validation|확인]].
3. **[[098_rollback_strategy_pipeline_error_threshold|롤백]] 계획**: 실험이 제어 불능 시 즉시 장애 주입을 중단하는 Kill [[238_switch_operation_principles|Switch]].
4. **사후 분석**: 실험 결과 문서화, 발견된 취약점 이슈 등록.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- **Game Day 없이 프로덕션 카오스**: 관찰 도구·[[098_rollback_strategy_pipeline_error_threshold|롤백]] 계획 없이 장애 주입 → 실제 [[090_service_kubernetes_network_load_balancing|서비스]] 장애 유발.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 카오스 미실시 | 카오스 실시 후 | 개선 |
|:---|:---|:---|:---|
| [[451_mttr|MTTR]] ([[658_ir_recovery|복구]] 시간) | 2시간+ | **15분 이하** | 87% 단축 |
| 미발견 취약점 | 잠재 | **사전 제거** | 장애 예방 |
| 운영 자신감 | 불안 | **[[395_verification_process_review|검증]]된 복원력** | [[100_sre_site_reliability_engineering_error_budget|SRE]] 성숙 |

[[751_chaos_engineering|카오스 엔지니어링]]은 [[190_ai_llm_requirements_specification|AI]] 기반 자동 실험 설계·자동 결과 분석과 결합하여 "자율 복원 시스템(Self-healing)"의 핵심 기반이 되고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[149_chaos_monkey_chaos_mesh|Chaos Monkey]]** | Netflix 최초의 카오스 도구, 인스턴스 랜덤 종료 |
| **Litmus / Chaos [[389_mesh_topology|Mesh]]** | K8s 네이티브 [[751_chaos_engineering|카오스 엔지니어링]] 도구 |
| **[[307_circuit_breaker_pattern|서킷 브레이커]]** | 카오스 실험으로 [[395_verification_process_review|검증]]해야 할 방어 패턴 |
| **Game Day** | 조직 차원의 장애 훈련 이벤트 |
| **[[100_sre_site_reliability_engineering_error_budget|SRE]] ([[100_sre_site_reliability_engineering_error_budget|Site Reliability Engineering]])** | [[751_chaos_engineering|카오스 엔지니어링]]을 품는 상위 규율 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Netflix Chaos Monkey (2011) — 인스턴스 랜덤 Kill]
    │
    ▼
[Principles of Chaos Engineering (2014) — 방법론 체계화]
    │
    ▼
[Gremlin SaaS (2016~) — 상용 카오스 플랫폼]
    │
    ▼
[Litmus / Chaos Mesh (2020~) — K8s 네이티브 CNCF]
    │
    ▼
[현재: AI 기반 자동 카오스 — 자율 장애 탐색·자동 복원]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [[751_chaos_engineering|카오스 엔지니어링]]은 건물에 **일부러 약한 지진**을 일으켜서, 건물이 안 무너지는지 [[396_validation|확인]]하는 거예요.
2. 만약 벽이 금이 가면, 지진이 진짜 오기 **전에 미리 보수**할 수 있어요!
3. 덕분에 진짜 지진(장애)이 와도 **건물([[090_service_kubernetes_network_load_balancing|서비스]])이 안전하게** 버틸 수 있답니다!
