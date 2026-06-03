+++
weight = 115
title = "115. 카나리 배포 (Canary Deployment) - 점진적 롤아웃과 트래픽 분배 전략"
date = "2026-04-19"
[extra]
categories = "studynote-software-engineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[595_canary_stack_smashing_protector|카나리]] 배포는 신버전을 **전체 트래픽의 1~5%에만 먼저 노출**하고, [[342_routing_metric_hop_bandwidth_delay|메트릭]](에러율·레이턴시)을 관찰하여 안전하면 점진적으로 확대([[489_raid_10_hybrid|10]]%→50%→100%)하는 **위험 최소화 배포 [[268_strategy_pattern|전략]]**이다.
> 2. **가치**: 블루/그린이 "한 번에 100% 전환"이라면, [[595_canary_stack_smashing_protector|카나리]]는 "1%→5%→25%→100%"로 **단계적 [[395_verification_process_review|검증]]** 후 전환하므로 장애 시 영향 범위가 극히 제한된다.
> 3. **판단 포인트**: [[302_service_mesh_istio|Istio]] VirtualService·Argo Rollouts·AWS ALB [[267_weight_bias_activation|가중치]]로 트래픽 비율을 제어하며, Kayenta 같은 **자동 [[595_canary_stack_smashing_protector|카나리]] 분석(ACA)**과 결합하면 사람 개입 없는 완전 자동 롤아웃이 가능하다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    카나리 배포 트래픽 점진 확대                         │
├───────────────────────────────────────────────────────┤
│  Phase 1: v2 → 1% 트래픽 (카나리)                    │
│           v1 → 99% 트래픽 (베이스라인)                │
│           → 메트릭 관찰 (에러율, 레이턴시)             │
│  Phase 2: v2 → 10% 트래픽                            │
│  Phase 3: v2 → 50% 트래픽                            │
│  Phase 4: v2 → 100% 트래픽 (완전 전환)               │
│                                                       │
│  문제 발생 시: 즉시 v2 → 0%, v1 → 100% (롤백)       │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[595_canary_stack_smashing_protector|카나리]]는 탄광의 [[595_canary_stack_smashing_protector|카나리]]아 새에서 유래했다. 새가 먼저 들어가서 유독 [[024_gas|가스]](버그)를 감지하면 광부(사용자 전체)가 들어가지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 트래픽 분배 방식

| 방식 | 도구 | 특징 |
|:---|:---|:---|
| **[[828_service_mesh_microservice_communication_infrastructure|Service Mesh]]** | [[302_service_mesh_istio|Istio]] VirtualService | L7 [[267_weight_bias_activation|가중치]], 헤더 기반 [[339_routing_overview_best_path_selection|라우팅]] |
| **K8s Native** | Argo Rollouts | AnalysisRun으로 자동 판정 |
| **[[031_load_balancer|Load Balancer]]** | AWS ALB [[267_weight_bias_activation|가중치]] | 인프라 레벨, 간단 |
| **[[511_dns_hierarchical_distributed_architecture|DNS]]** | Route 53 [[267_weight_bias_activation|가중치]] | 글로벌 트래픽 분배 |

### [[595_canary_stack_smashing_protector|카나리]] vs 블루/그린

| 비교 | 블루/그린 | [[595_canary_stack_smashing_protector|카나리]] |
|:---|:---|:---|
| **전환** | 100% 한 번에 | **1%→[[489_raid_10_hybrid|10]]%→100% 점진** |
| **리소스** | 2배 (구/신 동시 운영) | **+α만 추가** |
| **위험** | 100% 사용자 영향 | **[[459_quic_fec_forward_error_correction|초기]] 1%만 영향** |
| **[[395_verification_process_review|검증]] 깊이** | 배포 전 테스트 | **실 트래픽으로 [[395_verification_process_review|검증]]** |

- **📢 섹션 요약 비유**: 블루/그린은 전등 [[238_switch_operation_principles|스위치]](ON/OFF), [[595_canary_stack_smashing_protector|카나리]]는 디머(Dimmer, 밝기 조절)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [[117_rolling_update_deployment|롤링 업데이트]] | 블루/그린 | [[595_canary_stack_smashing_protector|카나리]] |
|:---|:---|:---|:---|
| **속도** | 중간 | 빠름 | **느림 (단계적)** |
| **위험** | 중간 | 중간 | **최저** |
| **복잡도** | 낮음 | 중간 | **높음** |
| **[[098_rollback_strategy_pipeline_error_threshold|롤백]]** | 느림 | 즉시 | **즉시** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### Argo Rollouts [[595_canary_stack_smashing_protector|카나리]] [[009_config|설정]] 예시
```yaml
strategy:
  canary:
    steps:
    - setWeight: 5
    - pause: {duration: 5m}
    - setWeight: 25
    - pause: {duration: 10m}
    - setWeight: 100
```

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- **[[595_canary_stack_smashing_protector|카나리]] 비율 즉시 100%**: 1%→100% 한 번에 올리면 [[595_canary_stack_smashing_protector|카나리]] 배포가 아니라 빅뱅 배포.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 빅뱅 배포 | [[595_canary_stack_smashing_protector|카나리]] 배포 | 개선 |
|:---|:---|:---|:---|
| 장애 영향 사용자 | 100% | **1~5%** | 95% 감소 |
| [[098_rollback_strategy_pipeline_error_threshold|롤백]] 속도 | 분 단위 | **초 단위** | 즉시 |
| 배포 자신감 | 낮음 | **높음** | [[001_dikw_pyramid|데이터]] 기반 |

[[595_canary_stack_smashing_protector|카나리]] 배포는 [[576_feature_flag_ab_testing_rollout|피처 플래그]]·ACA(Kayenta)와 결합하여 "배포→관찰→자동 판정→확대/[[098_rollback_strategy_pipeline_error_threshold|롤백]]"이 완전 자동화되는 Progressive Delivery의 핵심 요소다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **블루/그린 배포** | [[595_canary_stack_smashing_protector|카나리]]의 대안 배포 [[268_strategy_pattern|전략]] |
| **Argo Rollouts** | K8s 네이티브 [[595_canary_stack_smashing_protector|카나리]] 배포 도구 |
| **[[302_service_mesh_istio|Istio]] VirtualService** | [[828_service_mesh_microservice_communication_infrastructure|Service Mesh]] 기반 트래픽 [[267_weight_bias_activation|가중치]] |
| **Kayenta ACA** | 자동 [[595_canary_stack_smashing_protector|카나리]] 분석 (통계적 판정) |
| **[[576_feature_flag_ab_testing_rollout|피처 플래그]]** | 코드 레벨 점진적 릴리즈 |

### 📈 관련 키워드 및 발전 흐름도

```text
[롤링 업데이트 (2000s) — Pod 순차 교체]
    │
    ▼
[블루/그린 배포 (2010s) — 100% 전환]
    │
    ▼
[카나리 배포 (2015~) — 1%→100% 점진 확대]
    │
    ▼
[ACA + Argo Rollouts (2020~) — 자동 판정·자동 확대]
    │
    ▼
[현재: Progressive Delivery — 카나리+피처플래그+ACA 통합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 새 요리를 만들면 처음에 **10명 중 1명에게만** 맛보게 해요 ([[595_canary_stack_smashing_protector|카나리]]).
2. "맛있다!"라고 하면 점점 더 많은 사람에게 주고, "맛없다!"라고 하면 즉시 멈춰요.
3. 이렇게 하면 **모든 손님이 한꺼번에 맛없는 요리를 먹는 사고**를 막을 수 있답니다!
