+++
title = "115. 카나리 배포 (Canary Deployment) - 점진적 롤아웃과 트래픽 분배 전략"
date = 2026-04-19

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 배포는 신버전을 <strong>전체 트래픽의 1~5%에만 먼저 노출</strong>하고, [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)(에러율·레이턴시)을 관찰하여 안전하면 점진적으로 확대([10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)%->50%->100%)하는 <strong>위험 최소화 배포 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>이다.
> 2. **가치**: 블루/그린이 "한 번에 100% 전환"이라면, [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)는 "1%->5%->25%->100%"로 <strong>단계적 <a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a></strong> 후 전환하므로 장애 시 영향 범위가 극히 제한된다.
> 3. **판단 포인트**: [Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/) VirtualService·Argo Rollouts·AWS ALB [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)로 트래픽 비율을 제어하며, Kayenta 같은 <strong>자동 <a href="/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/">카나리</a> 분석(ACA)</strong>과 결합하면 사람 개입 없는 완전 자동 롤아웃이 가능하다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    카나리 배포 트래픽 점진 확대                         |
+-------------------------------------------------------+
|  Phase 1: v2 -> 1% 트래픽 (카나리)                    |
|           v1 -> 99% 트래픽 (베이스라인)                |
|           -> 메트릭 관찰 (에러율, 레이턴시)             |
|  Phase 2: v2 -> 10% 트래픽                            |
|  Phase 3: v2 -> 50% 트래픽                            |
|  Phase 4: v2 -> 100% 트래픽 (완전 전환)               |
|                                                       |
|  문제 발생 시: 즉시 v2 -> 0%, v1 -> 100% (롤백)       |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)는 탄광의 [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)아 새에서 유래했다. 새가 먼저 들어가서 유독 [가스](/knowledge-base/studynote/06_ict_convergence/01_blockchain/024_gas/)(버그)를 감지하면 광부(사용자 전체)가 들어가지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 트래픽 분배 방식

| 방식 | 도구 | 특징 |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/">Service Mesh</a></strong> | [Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/) VirtualService | L7 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/), 헤더 기반 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) |
| **K8s Native** | Argo Rollouts | AnalysisRun으로 자동 판정 |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/01_virtualization/031_load_balancer/">Load Balancer</a></strong> | AWS ALB [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) | 인프라 레벨, 간단 |
| <strong><a href="/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/">DNS</a></strong> | Route 53 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) | 글로벌 트래픽 분배 |

### [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) vs 블루/그린

| 비교 | 블루/그린 | [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) |
|:---|:---|:---|
| **전환** | 100% 한 번에 | <strong>1%-><a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/">10</a>%->100% 점진</strong> |
| **리소스** | 2배 (구/신 동시 운영) | **+α만 추가** |
| **위험** | 100% 사용자 영향 | <strong><a href="/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/">초기</a> 1%만 영향</strong> |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a> 깊이</strong> | 배포 전 테스트 | <strong>실 트래픽으로 <a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a></strong> |

- **📢 섹션 요약 비유**: 블루/그린은 전등 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)(ON/OFF), [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)는 디머(Dimmer, 밝기 조절)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [롤링 업데이트](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/117_rolling_update_deployment/) | 블루/그린 | [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) |
|:---|:---|:---|:---|
| **속도** | 중간 | 빠름 | **느림 (단계적)** |
| **위험** | 중간 | 중간 | **최저** |
| **복잡도** | 낮음 | 중간 | **높음** |
| <strong><a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/">롤백</a></strong> | 느림 | 즉시 | **즉시** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### Argo Rollouts [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 예시
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

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/">카나리</a> 비율 즉시 100%</strong>: 1%->100% 한 번에 올리면 [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 배포가 아니라 빅뱅 배포.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 빅뱅 배포 | [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 배포 | 개선 |
|:---|:---|:---|:---|
| 장애 영향 사용자 | 100% | **1~5%** | 95% 감소 |
| [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 속도 | 분 단위 | **초 단위** | 즉시 |
| 배포 자신감 | 낮음 | **높음** | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기반 |

[카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 배포는 [피처 플래그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/)·ACA(Kayenta)와 결합하여 "배포->관찰->자동 판정->확대/[롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)"이 완전 자동화되는 Progressive Delivery의 핵심 요소다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **블루/그린 배포** | [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)의 대안 배포 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| **Argo Rollouts** | K8s 네이티브 [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 배포 도구 |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/">Istio</a> VirtualService</strong> | [Service Mesh](/knowledge-base/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/) 기반 트래픽 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) |
| **Kayenta ACA** | 자동 [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 분석 (통계적 판정) |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/">피처 플래그</a></strong> | 코드 레벨 점진적 릴리즈 |

### 📈 관련 키워드 및 발전 흐름도

```text
[롤링 업데이트 (2000s) — Pod 순차 교체]
    |
    v
[블루/그린 배포 (2010s) — 100% 전환]
    |
    v
[카나리 배포 (2015~) — 1%->100% 점진 확대]
    |
    v
[ACA + Argo Rollouts (2020~) — 자동 판정·자동 확대]
    |
    v
[현재: Progressive Delivery — 카나리+피처플래그+ACA 통합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 새 요리를 만들면 처음에 **10명 중 1명에게만** 맛보게 해요 ([카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)).
2. "맛있다!"라고 하면 점점 더 많은 사람에게 주고, "맛없다!"라고 하면 즉시 멈춰요.
3. 이렇게 하면 <strong>모든 손님이 한꺼번에 맛없는 요리를 먹는 사고</strong>를 막을 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 115 / 973

<- **이전**: [114. 피처 플래그 (Feature Flag/Toggle) - 배포와 릴리즈 분리·다크 런칭](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/114_feature_flag_toggle_deployment/)
**다음**: [116. 블루/그린 배포 (Blue/Green Deployment) - 무중단 전환과 즉시 롤백](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/116_blue_green_deployment/) ->

---
