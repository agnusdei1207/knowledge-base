---
title: 507. 카오스 엔지니어링, 섀도 배포, 서킷 브레이커 (Chaos Engineering Shadow Deployment Circuit
  Breaker)
date: '2026-05-09'
tags:
- studynote-ict-convergence
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 복원력(Resilience) 기술은 "장애가 일어나지 않을 것"을 가정하는 대신 "장애는 반드시 일어난다"를 전제로, 사전에 시스템을 [[395_verification_process_review|검증]]하고 [[571_protection_vs_security|보호]]한다.
> 2. **가치**: [[751_chaos_engineering|카오스 엔지니어링]]([[751_chaos_engineering|Chaos Engineering]])은 프로덕션에서 의도적 장애를 주입하여 숨겨진 취약점을 미리 발견하고, [[118_shadow_deployment_traffic_mirroring|섀도 배포]]([[118_shadow_deployment_traffic_mirroring|Shadow Deployment]])는 실제 사용자 영향 없이 새 [[288_version_ihl_tos_total_length|버전]]을 [[395_verification_process_review|검증]]한다.
> 3. **판단 포인트**: [[307_circuit_breaker_pattern|서킷 브레이커]]([[304_circuit_breaker|Circuit Breaker]])의 Open 상태 임계값 설정이 너무 민감하면 정상 요청도 차단되고, 너무 느슨하면 장애 전파를 막지 못한다.

---

## Ⅰ. 개요 및 필요성

클라우드 [[136_variance|분산]] 시스템에서 장애는 불가피하다. Netflix는 AWS로 전환한 뒤 서버 장애, 네트워크 분단, 의존 [[090_service_kubernetes_network_load_balancing|서비스]] 다운 등 예상치 못한 장애로 심각한 [[090_service_kubernetes_network_load_balancing|서비스]] 중단을 경험했다. 이 경험에서 탄생한 것이 **[[751_chaos_engineering|카오스 엔지니어링]]**이다.

**복원력 3대 [[268_strategy_pattern|전략]]**:
1. **사전 [[395_verification_process_review|검증]]**: [[751_chaos_engineering|카오스 엔지니어링]]으로 약점 발견
2. **안전한 배포**: 섀도/[[595_canary_stack_smashing_protector|카나리]]/[[194_blue_green_deployment_strategy|블루-그린 배포]]로 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] [[136_variance|분산]]
3. **실시간 [[571_protection_vs_security|보호]]**: [[307_circuit_breaker_pattern|서킷 브레이커]]로 장애 전파 차단

- **📢 섹션 요약 비유**: 복원력 설계는 소방 훈련과 같다 — 실제 화재가 나기 전에 연습하고(카오스), 새 소화기를 몰래 테스트하며([[118_shadow_deployment_traffic_mirroring|섀도 배포]]), 불이 번지면 자동으로 막는 방화문([[307_circuit_breaker_pattern|서킷 브레이커]])을 갖추는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

**[[307_circuit_breaker_pattern|서킷 브레이커]] 상태 전환**:

```
          실패율 < 임계값           실패율 ≥ 임계값
┌──────────────────────────────────────────────────────┐
│                                                      │
│  ┌─────────┐  실패율 초과  ┌──────────┐              │
│  │ CLOSED  │────────────→ │  OPEN    │              │
│  │ (정상)  │              │ (즉시 거부)│              │
│  └─────────┘              └──────────┘              │
│       ↑                        │                    │
│  성공률 회복                  타임아웃 경과           │
│       │                        ↓                    │
│       └──────────────── ┌────────────┐              │
│                         │ HALF-OPEN  │              │
│                         │ (소수 허용) │              │
│                         └────────────┘              │
└──────────────────────────────────────────────────────┘
```

| 기술 | 목적 | 적용 시점 | 트래픽 영향 |
|:---|:---|:---|:---|
| [[751_chaos_engineering|카오스 엔지니어링]] ([[751_chaos_engineering|Chaos Engineering]]) | 약점 사전 발견 | 정기적 실험 | 의도적 장애 주입 |
| [[118_shadow_deployment_traffic_mirroring|섀도 배포]] ([[118_shadow_deployment_traffic_mirroring|Shadow Deployment]]) | 새 [[288_version_ihl_tos_total_length|버전]] [[446_load_test|부하 테스트]] | 배포 전 | 없음 ([[333_raid_1|미러링]]) |
| [[115_canary_deployment_gradual_rollout|카나리 배포]] ([[115_canary_deployment_gradual_rollout|Canary Deployment]]) | 점진적 트래픽 전환 | 배포 중 | 소수 사용자만 |
| [[194_blue_green_deployment_strategy|블루-그린 배포]] ([[304_process|Blue-Green Deployment]]) | 순간 전환, 빠른 [[098_rollback_strategy_pipeline_error_threshold|롤백]] | 배포 시 | 전체 or 0 |

**[[751_chaos_engineering|카오스 엔지니어링]] 실험 원칙**:
1. 안정 상태(Steady [[272_state_pattern|State]]) 정의: 정상 시스템의 측정 가능한 지표([[138_response_time|응답 시간]] 200ms 이하, 에러율 0.1% 이하)
2. 가설 수립: "서버 1대를 종료해도 안정 상태를 유지할 것이다"
3. 장애 주입: 서버 종료, [[1002_network_delay_rtt_oneway_delay_components|네트워크 지연]] 추가, 의존 [[090_service_kubernetes_network_load_balancing|서비스]] 응답 중단
4. 결과 측정: 안정 상태 유지 여부 [[396_validation|확인]], 이탈 시 약점 기록 및 개선

**Netflix [[149_chaos_monkey_chaos_mesh|Chaos Monkey]]**: K8s 클러스터에서 무작위로 Pod를 종료. Chaos Kong은 전체 AWS 가용 영역(AZ) 단위 장애 시뮬레이션.

- **📢 섹션 요약 비유**: [[751_chaos_engineering|카오스 엔지니어링]]은 백신 접종과 같다 — 약한 [[589_virus|바이러스]](모의 장애)를 주입해서 몸(시스템)이 미리 면역(복원력)을 키우게 한다.

---

## Ⅲ. 비교 및 연결

**[[118_shadow_deployment_traffic_mirroring|섀도 배포]](Shadow/Dark Launch) vs [[115_canary_deployment_gradual_rollout|카나리 배포]]**:
- **[[118_shadow_deployment_traffic_mirroring|섀도 배포]]**: 실제 트래픽을 새 [[288_version_ihl_tos_total_length|버전]]으로 [[333_raid_1|미러링]], 응답을 실제 사용자에게는 반환하지 않음. 사용자 영향 0%로 [[282_performance_tactics|성능]]/[[002_bigdata_5v|정확성]] 테스트. 단, 부하가 2배 발생.
- **[[115_canary_deployment_gradual_rollout|카나리 배포]]**: 전체 트래픽의 5~[[489_raid_10_hybrid|10]]%만 새 [[288_version_ihl_tos_total_length|버전]]으로 전환. 실제 사용자 일부 영향 있으나 조기 문제 발견. 점진적 확대.

**[[194_blue_green_deployment_strategy|블루-그린 배포]]**: 두 개의 동일한 환경 운영. 트래픽을 Blue(구 [[288_version_ihl_tos_total_length|버전]])에서 Green(새 [[288_version_ihl_tos_total_length|버전]])으로 순간 전환. 문제 발생 시 [[511_dns_hierarchical_distributed_architecture|DNS]]/로드밸런서 변경만으로 즉시 [[098_rollback_strategy_pipeline_error_threshold|롤백]] 가능. 단, 인프라 비용 2배.

- **📢 섹션 요약 비유**: 블루-그린은 새 레스토랑을 구 레스토랑 옆에 지어두고, 문을 바꿔 다는 것이다. 손님(트래픽)은 즉시 새 레스토랑으로 안내되고, 문제 시 옆 레스토랑 문을 다시 연다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**기술사 시험 판단 포인트**:
1. [[751_chaos_engineering|카오스 엔지니어링]]의 4단계 실험 방법론(안정 상태 → 가설 → 주입 → 측정)을 체계적으로 기술한다.
2. [[307_circuit_breaker_pattern|서킷 브레이커]] 세 상태 전환 조건과 [[171_fallback_resilience_pattern|폴백]]([[129_fallback|Fallback]]) 응답 [[268_strategy_pattern|전략]](캐시 응답, 기본값 반환)을 설명한다.
3. 섀도/[[595_canary_stack_smashing_protector|카나리]]/블루-그린의 트레이드오프를 표로 정리하면 고득점 요인이다.

**실무 시나리오**: 결제 [[090_service_kubernetes_network_load_balancing|서비스]] 배포 시 — [[118_shadow_deployment_traffic_mirroring|섀도 배포]]로 1주일간 실제 트래픽 [[333_raid_1|미러링]] → [[282_performance_tactics|성능]]/정확도 이상 없음 [[396_validation|확인]] → [[595_canary_stack_smashing_protector|카나리]] 1% → 5% → 20% → 100% 순차 증가 → 각 단계에서 에러율과 [[138_response_time|응답 시간]] 모니터링 → 이상 시 즉시 [[595_canary_stack_smashing_protector|카나리]] 비율 0%로 [[658_ir_recovery|복구]].

- **📢 섹션 요약 비유**: 섀도 + [[595_canary_stack_smashing_protector|카나리]] + 블루-그린 조합은 새 다리를 개통할 때 — 먼저 몰래 차를 1대 테스트(섀도)하고, 트럭 몇 대 통행([[595_canary_stack_smashing_protector|카나리]])하다가, 구 다리 완전 철거(블루-그린 전환)하는 순서와 같다.

---

## Ⅴ. 기대효과 및 결론

복원력 기술을 체계적으로 적용하면:
- **장애 [[451_mttr|MTTR]](Mean Time to Repair) 단축**: 자동 [[307_circuit_breaker_pattern|서킷 브레이커]]로 장애 감지~차단 시간 수 초
- **배포 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] 최소화**: 섀도/[[595_canary_stack_smashing_protector|카나리]]로 프로덕션 영향 없이 새 [[288_version_ihl_tos_total_length|버전]] [[395_verification_process_review|검증]]
- **선제적 약점 제거**: [[751_chaos_engineering|카오스 엔지니어링]]으로 장애 발생 전 취약점 [[655_ir_detection_analysis|식별]]
- **[[085_sla|SLA]]([[090_service_kubernetes_network_load_balancing|서비스]] 수준 협약) 달성**: 99.9~99.99% [[452_availability|가용성]] 목표 현실화

복원력 엔지니어링은 "장애를 막는 것"에서 "장애에서 빠르게 회복하는 것"으로 패러다임을 전환한다.

- **📢 섹션 요약 비유**: 복원력 시스템은 아이언맨 수트처럼, 맞아도 쓰러지지 않는 구조다 — 장갑이 날아가도 수트 전체는 작동하고, 취약 부위를 미리 강화한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[307_circuit_breaker_pattern|서킷 브레이커]] ([[304_circuit_breaker|Circuit Breaker]]) | Resilience4j, [[171_fallback_resilience_pattern|폴백]], Hystrix · 505 |
| [[619_msa_traffic_hardware|MSA]] ([[365_msa_microservice_architecture|Microservice Architecture]]) | [[136_variance|분산]] 장애, [[090_service_kubernetes_network_load_balancing|서비스]] 의존 · 505 |
| [[181_slo_service_level_objective|SLO]]/[[085_sla|SLA]] ([[090_service_kubernetes_network_load_balancing|서비스]] 수준 목표/협약) | [[452_availability|가용성]], [[451_mttr|MTTR]], [[101_error_budget_sre|에러 예산]] · 540 |
| [[205_kubernetes_container_orchestration|Kubernetes]] | [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 종료, 카오스 실험 환경 · 502 |
| [[194_blue_green_deployment_strategy|블루-그린 배포]] ([[304_process|Blue-Green Deployment]]) | [[511_dns_hierarchical_distributed_architecture|DNS]] 전환, 인프라 [[456_dual_redundancy|이중화]] · 504 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Resilience4j · 폴백] → [카오스 엔지니어링 · 섀도 배포] → [DNS 전환 · 인프라 이중화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[751_chaos_engineering|카오스 엔지니어링]]은 지진 대피 훈련이에요 — 실제 지진 전에 연습해서, 진짜 지진이 나도 당황하지 않도록 해요.
2. [[118_shadow_deployment_traffic_mirroring|섀도 배포]]는 새 선생님이 수업을 몰래 참관하는 것처럼, 학생들(사용자)은 모르지만 미리 실력을 [[395_verification_process_review|검증]]해요.
3. [[307_circuit_breaker_pattern|서킷 브레이커]]는 두꺼비집이에요 — 전기(요청)가 너무 많이 흐르면 자동으로 끊어서 집 전체가 타지 않게 해요.
