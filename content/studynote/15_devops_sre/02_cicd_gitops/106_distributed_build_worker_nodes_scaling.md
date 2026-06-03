---
title: '분산 빌드: 워커 노드 스케일링을 통한 빌드 병렬화'
date: '2026-03-04'
tags:
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[136_variance|분산]] 빌드 (Distributed Build)는 소프트웨어 통합 및 테스트 작업을 단일 서버([[621_scale_up_system_bus|Scale-up]])에서 처리하지 않고, 다수의 워커 노드(Worker Nodes)로 쪼개어 수평적([[202_scale_out_distributed_horizontal_expansion|Scale-out]])으로 동시 처리하는 [[090_configuration_item|CI]]/CD 아키텍처다.
> 2. **가치**: 대규모 [[532_microservices_decomposition_patterns|마이크로서비스]] ([[619_msa_traffic_hardware|MSA]]) 환경에서 수만 개의 테스트와 빌드 작업이 유발하는 병목([[058_queue|Queue]])을 해소하여, 개발자에게 피드백을 주는 [[085_lead_time_cycle_time|리드 타임]]을 물리적 한계까지 단축시킨다.
> 3. **판단 포인트**: [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] (K8s)와 결합한 동적 [[528_provisioning|프로비저닝]] (Dynamic [[528_provisioning|Provisioning]])을 통해, 빌드 수요가 폭증할 때만 노드를 늘리고 끝나면 삭제하여 클라우드 인프라 비용과 [[283_security_tactics|보안성]]을 동시에 최적화해야 한다.

---

## Ⅰ. 개요 및 필요성
소프트웨어 프로젝트 규모가 커지고 개발자가 늘어나면 하루에도 수십 번씩 코드가 병합(Merge)된다. 과거의 [[090_configuration_item|CI]] ([[019_continuous_integration|Continuous Integration]]) 서버는 [[071_jenkins_ci_cd_pipeline_automation|젠킨스]]([[071_jenkins_ci_cd_pipeline_automation|Jenkins]]) [[172_maas_mobility_as_a_service|마스]]터 한 대가 소스코드를 내려받고, 컴파일하고, 테스트하는 모든 과정을 독점했다. 이 방식은 앞선 누군가의 빌드가 끝나기 전까지 뒤에 줄 선 수많은 개발자들이 기약 없이 대기해야 하는 병목 현상을 유발했다.

이를 해결하기 위해 작업을 조율하는 '컨트롤러(Master)'와 실제 작업을 수행하는 일꾼인 '워커 노드(Worker Node)'를 분리하는 [[136_variance|분산]] 빌드 아키텍처가 필요해졌다. 작업을 쪼개어 10대의 서버가 동시에 테스트를 수행하면 빌드 시간은 이론적으로 1/10로 줄어든다. 빠른 빌드는 곧 빠른 [[352_defect_definition|결함]] 발견으로 이어져 전체 소프트웨어 생명 주기([[131_sdlc_system_development_life_cycle_waterfall_agile|SDLC]])의 생산성을 폭발적으로 끌어올린다.

- **📢 섹션 요약 비유**: 혼자서 1,000인분의 요리를 순서대로 하느라 손님들이 다 도망가게 생겼을 때, 주방장([[172_maas_mobility_as_a_service|마스]]터)은 지시만 내리고 100명의 요리사(워커)를 일시적으로 고용해 동시에 요리하게 만드는 것이 [[136_variance|분산]] 빌드다.

---

## Ⅱ. 아키텍처 및 핵심 원리
[[136_variance|분산]] 빌드의 핵심 메커니즘은 **작업 [[208_schedule_history_transaction_execution_order|스케줄]]링([[150_task|Task]] Scheduling)** 과 **동적 [[249_scaling_normalization_standardization|스케일링]](Dynamic Scaling)** 의 결합이다. 현대의 [[090_configuration_item|CI]] 도구들은 고정된 서버를 유지하지 않고, [[531_cloud_native_architecture|클라우드 네이티브]] 기술을 활용해 빌드가 필요한 순간에만 워커를 [[087_process_state_transition|생성]](Ephemeral)한다.

```text
┌──────────────────────────────────────────────────────────────┐
│           Kubernetes 기반 동적 분산 빌드 아키텍처                   │
├──────────────────────────────────────────────────────────────┤
│ [Git Repository] ──(Webhook)──▶ [CI Master / Controller]     │
│                                       │ (작업 분배 및 조율)      │
│                                       ▼                      │
│                ┌────────────────────────────────────┐        │
│                │      Kubernetes Cluster (Node)     │        │
│                │                                    │        │
│ Task 분할 ──▶  │  [Pod Worker 1] ─▶ 단위 테스트 1~100  │        │
│ (Matrix)       │  [Pod Worker 2] ─▶ 단위 테스트 101~200│        │
│                │  [Pod Worker 3] ─▶ 정적 분석 (Lint)   │        │
│                └────────────────────────────────────┘        │
│                                       │                      │
│ 빌드 완료 후 자동 소멸 (Ephemeral) ◀──┴──▶ [Artifact Storage]  │
└──────────────────────────────────────────────────────────────┘
```

1. **[[507_acid_properties|트리거]] 및 [[528_provisioning|프로비저닝]]**: 코드가 푸시되면 [[172_maas_mobility_as_a_service|마스]]터가 K8s API를 호출하여 필요한 워커 [[085_pod_kubernetes_container_unit|파드]]([[198_pod_kubernetes_minimum_deployment_unit|Pod]])를 필요한 개수만큼 즉시 [[087_process_state_transition|생성]]한다.
2. **매트릭스 빌드 (Matrix Build)**: OS 다변화, 브라우저 다변화, [[441_test_case|테스트 케이스]] 분할 등 작업을 독립적인 단위로 쪼개어 각각의 워커에 [[430_index_fast_full_scan|병렬]]로 던진다.
3. **산출물 [[212_synchronization_mechanisms|동기화]]**: [[136_variance|분산]]된 워커들이 만들어낸 결과물(바이너리, 테스트 리포트)은 중앙 스토리지(S3, Nexus 등)로 모아 하나로 병합한 뒤, 워커 노드는 즉시 삭제된다.

- **📢 섹션 요약 비유**: 배달 주문이 밀려올 때만 오토바이 라이더(워커 노드)들을 단기 호출앱으로 부르고, 배달이 끝나면 바로 퇴근시켜 고정 인건비(클라우드 유지비)를 0으로 만드는 시스템이다.

---

## Ⅲ. 비교 및 연결
빌드 [[123_pipe|파이프]]라인의 [[282_performance_tactics|성능]]을 높이는 [[268_strategy_pattern|전략]]은 크게 수직 확장([[621_scale_up_system_bus|Scale-up]])과 수평 확장([[202_scale_out_distributed_horizontal_expansion|Scale-out]])으로 나뉜다.

| 항목 | 단일 빌드 ([[621_scale_up_system_bus|Scale-up]]) | [[136_variance|분산]] 빌드 ([[202_scale_out_distributed_horizontal_expansion|Scale-out]]) |
| :--- | :--- | :--- |
| **확장 방식** | 단일 빌드 서버의 CPU, RAM [[282_performance_tactics|성능]]을 높임 | **작업을 수행하는 노드 개수를 늘림** |
| **병목 지점** | 물리적 하드웨어 한계에 부딪힘 | **[[075_kubernetes_k8s_cluster_architecture|마스터 노드]]의 [[208_schedule_history_transaction_execution_order|스케줄]]링 부하, 네트워크** |
| **비용 효율** | 유휴 시간(새벽 등)에도 서버 유지 비용 발생 | K8s 동적 [[528_provisioning|프로비저닝]] 시 **유휴 비용 [[784_zeroization_circuit|제로화]]** |
| **보안 및 격리** | 이전 빌드의 찌꺼기(캐시)가 다음 빌드 오염 가능 | **일회성(Ephemeral) [[561_container_based_deployment|컨테이너]]**로 완벽히 격리 |
| **복잡도** | 매우 단순함 | 네트워크 [[212_synchronization_mechanisms|동기화]], 캐시 [[136_variance|분산]] 관리 로직 필요 |

[[136_variance|분산]] 빌드는 [[459_quic_fec_forward_error_correction|초기]] 구축 난이도가 높고, 각 워커가 필요한 [[336_library_vs_framework|라이브러리]]를 매번 새로 다운로드해야 하므로 '네트워크 오버헤드'라는 새로운 단점이 생긴다. 이를 보완하기 위해 워커 노드와 가까운 곳에 [[136_variance|분산]] 캐시 (Distributed Cache) 서버를 두는 것이 필수적으로 연결된다.

- **📢 섹션 요약 비유**: 수직 확장은 가장 빠르고 비싼 슈퍼컴퓨터 한 대를 사는 것이고, 수평 확장([[136_variance|분산]] 빌드)은 평범한 컴퓨터 수십 대를 그물처럼 묶어서 한 번에 돌리는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단
엔터프라이즈 환경에서 [[136_variance|분산]] 빌드를 설계할 때 가장 중요한 것은 **클라우드 비용([[016_tco|TCO]]) 최적화**와 **빌드 안정성 확보**다.

1. **[[209_spot_instance_cloud_cost_optimization|스팟 인스턴스]] ([[209_spot_instance_cloud_cost_optimization|Spot Instance]]) 적극 활용**:
   - 빌드 작업은 중간에 서버가 죽어도 다시 실행하면 그만인 상태 비저장([[239_stateless_redis|Stateless]]) 작업이다. 따라서 정가보다 70~90% 저렴한 AWS Spot Instance나 GCP Preemptible VM을 워커 노드 풀(Pool)로 활용하는 것이 기술사의 핵심 설계 포인트다.
2. **캐시 [[268_strategy_pattern|전략]] ([[456_caching|Caching]] [[268_strategy_pattern|Strategy]]) 수립**:
   - 수십 대의 워커 노드가 매번 npm, Maven 패키지를 인터넷에서 받아오면 빌드보다 다운로드 시간이 더 걸린다. ECR, S3 엔드포인트나 사내 Nexus [[235_registry_immutable_tag|레지스트리]]를 같은 가용 영역(AZ)에 배치하여 [[1002_network_delay_rtt_oneway_delay_components|네트워크 지연]]을 없애야 한다.

**기술사 판단 포인트**: 
[[136_variance|분산]] 빌드가 무조건 빠른 것은 아니다. 테스트 코드가 DB에 강하게 결합되어 있어 서로 독립적이지 않다면(의존성), 작업을 [[430_index_fast_full_scan|병렬]]로 쪼갤 수 없다. 도입 전 [[201_software_architecture_definition|소프트웨어 아키텍처]] 자체가 독립적인 테스트가 가능한 구조([[192_module_independence|모듈]]화)인지 [[395_verification_process_review|검증]]하는 것이 선행되어야 한다.

- **📢 섹션 요약 비유**: [[136_variance|분산]] 빌드는 여러 공장이 부품을 나눠서 만드는 것이다. 공장 간 거리가 너무 멀면 부품 나르는 데 시간이 다 걸리므로(네트워크 병목), 반드시 공장 가운데에 공동 자재창고([[136_variance|분산]] 캐시) 지어야 한다.

---

## Ⅴ. 기대효과 및 결론
[[136_variance|분산]] 빌드를 도입하면 [[090_configuration_item|CI]] [[123_pipe|파이프]]라인의 [[085_lead_time_cycle_time|리드 타임]]이 수십 분에서 수 분 단위로 단축된다. 이는 개발자가 [[034_context_switch|컨텍스트 스위칭]] 없이 즉각적으로 버그를 수정할 수 있는 환경을 제공하며, 하루 배포 횟수를 기하급수적으로 늘려 [[004_agile_relation|애자일]]([[004_agile_relation|Agile]]) 조직의 민첩성을 극대화한다.

결론적으로 [[136_variance|분산]] 빌드는 단순히 "서버를 여러 대 쓴다"는 개념을 넘어, [[561_container_based_deployment|컨테이너]] 기반의 일회성 환경(Ephemeral), 클라우드 경제성(Spot), 테스트 [[430_index_fast_full_scan|병렬]]화 [[268_strategy_pattern|전략]]이 총합된 현대 [[652_devops_calms_culture|데브옵스]]([[652_devops_calms_culture|DevOps]]) 엔지니어링의 정수다. 

- **📢 섹션 요약 비유**: [[136_variance|분산]] 빌드는 혼자서 1시간 걸리던 대청소를 온 가족이 방마다 흩어져서 10분 만에 끝내는 마법이다. 덕분에 남는 시간에 더 재미있는 일(핵심 개발)을 할 수 있게 된다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
| :--- | :--- |
| **Ephemeral [[066_gitlab_flow_environment_branch_strategy|Environment]] (일회성 환경)** | 빌드가 끝난 즉시 워커 [[561_container_based_deployment|컨테이너]]를 삭제하여, 찌꺼기에 의한 빌드 오염을 방지하는 보안/격리 개념 |
| **Matrix Build (매트릭스 빌드)** | 다양한 OS, 브라우저 [[288_version_ihl_tos_total_length|버전]]을 조합하여 수십 개의 독립된 단위로 빌드를 쪼개 [[430_index_fast_full_scan|병렬]] 실행하는 기법 |
| **[[209_spot_instance_cloud_cost_optimization|스팟 인스턴스]] ([[209_spot_instance_cloud_cost_optimization|Spot Instance]])** | 언제든 회수될 수 있지만 매우 저렴한 클라우드 자원으로, [[136_variance|분산]] 빌드 워커 노드 구성 시 비용 최적화의 핵심 |
| **[[136_variance|분산]] 캐시 (Distributed Cache)** | 워커 노드가 흩어져 있을 때 공통 [[336_library_vs_framework|라이브러리]] 및 빌드 산출물을 빠르게 공유하기 위한 네트워크 최적화 장치 |

### 📈 관련 키워드 및 발전 흐름도
```text
단일 CI 서버 (Scale-up)
(Jenkins Master 독점 빌드, 병목 발생)
    │
    ▼
마스터-워커 분리 (Master-Worker Architecture)
(정적 워커 노드 할당, 자원 낭비 존재)
    │
    ▼
동적 프로비저닝 기반 분산 빌드 (Dynamic Scaling)
(K8s 기반 일회성 파드 생성 및 자동 삭제)
    │
    ▼
서버리스 / 스팟 인스턴스 결합 (Serverless & Spot)
(초저비용 무제한 수평 확장 파이프라인)
```

### 👶 어린이를 위한 3줄 비유 설명
1. 학교 숙제 100문제를 혼자 풀면 밤을 새워야 해서 너무 힘들어요.
2. 그래서 똑똑한 반장([[172_maas_mobility_as_a_service|마스]]터)이 친구 10명(워커 노드)을 불러서 숙제를 10문제씩 나눠 주었어요.
3. 10명이 동시에 문제를 푸니까 1시간 만에 숙제가 전부 끝나버렸고, 도와준 친구들은 바로 집으로 돌아갔답니다(동적 [[249_scaling_normalization_standardization|스케일링]])!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 106 / 373

← **이전**: [[105_build_caching_optimization_docker_layer|빌드 캐싱 최적화: CI/CD 병목을 뚫는 레이어 전략]]
**다음**: [[107_nightly_build_scheduled_cron_pipeline|나이트 빌드: 예약된 크론(Cron) 기반의 정적/동적 정기 점검]] →

---
