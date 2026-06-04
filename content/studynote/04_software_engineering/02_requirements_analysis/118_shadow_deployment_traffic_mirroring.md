+++
title = "118. 섀도 배포 (Shadow Deployment) - 트래픽 미러링·무위험 프로덕션 검증"
date = 2026-04-19

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 섀도 배포는 실제 프로덕션 트래픽을 <strong>신버전에 <a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/">복제</a>(<a href="/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/">미러링</a>)</strong>하되, 신버전의 응답은 **사용자에게 반환하지 않고 버리는** 방식으로 실 트래픽 기반 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 수행하는 배포 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.
> 2. **가치**: [카나리 배포](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/)는 실제 사용자 1%가 신버전 응답을 받으므로 장애 영향이 있지만, 섀도 배포는 <strong>사용자 영향 제로(<a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/">Zero</a> Impact)</strong>로 신버전을 프로덕션 트래픽으로 테스트한다.
> 3. **판단 포인트**: [Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/) VirtualService의 `mirror` 기능으로 구현하며, <strong>부작용(Side Effect)이 있는 <a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> 요청(POST/PUT/DELETE)</strong>은 [미러링](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/) 시 중복 처리 위험이 있어 <strong>읽기 전용(GET) 트래픽만 <a href="/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/">미러링</a></strong>하거나 격리된 DB를 사용해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    섀도 배포 트래픽 흐름                               |
+-------------------------------------------------------+
|  사용자 요청 ---> LB ---> v1 (응답 반환) ✅            |
|                    |                                  |
|                    +---> v2 (복제본, 응답 버림) 🗑️     |
|                         +-- 로그·메트릭만 수집        |
|                                                       |
|  사용자: v1 응답만 받음 (영향 제로)                   |
|  엔지니어: v2 로그·에러·레이턴시 비교 분석            |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 섀도 배포는 신인 배우(v2)가 무대 뒤에서 동시에 연기하지만, 관객(사용자)은 베테랑(v1)만 보는 드레스 리허설이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 배포 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 비교

| [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 사용자 영향 | 실 트래픽 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 인프라 |
|:---|:---|:---|:---|
| **블루/그린** | 전환 시 전체 | 전환 후 | 2배 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/">카나리</a></strong> | 1~5% | ✅ | +α |
| **섀도** | **제로** | <strong>✅ (<a href="/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/">미러링</a>)</strong> | +α |

### [Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/) [미러링](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
spec:
  http:
  - route:
    - destination:
        host: v1-service
    mirror:
      host: v2-service
    mirrorPercentage:
      value: 100.0
```

- **📢 섹션 요약 비유**: [미러링](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)은 시험지를 복사해서 다른 사람(v2)에게도 풀게 하는 것이다. 채점(응답)은 원본(v1)만 한다.

---

## Ⅲ. 비교 및 연결

| 비교 | [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) | 섀도 |
|:---|:---|:---|
| **사용자 영향** | 1~5% | **제로** |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a> <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a></strong> | 실 응답 | [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·메트릭만 |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> 요청</strong> | 실제 처리 | **격리 필요** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 적합 시나리오
1. **ML 모델 교체**: 추천 모델 v2의 응답 품질을 실 트래픽으로 비교.
2. **DB 마이그레이션**: 읽기 쿼리를 신 DB에 [미러링](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)하여 결과 비교.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong><a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> 요청 무분별 <a href="/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/">미러링</a></strong>: 주문·결제가 중복 처리 -> 반드시 읽기 전용 또는 격리 DB.

---

## Ⅴ. 기대효과 및 결론

| 지표 | [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) | 섀도 | 개선 |
|:---|:---|:---|:---|
| 사용자 장애 위험 | 1~5% | **0%** | 무위험 |
| [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 현실성 | 높음 | **높음 (실 트래픽)** | 동등 |

섀도 배포는 <strong>위험 제로로 프로덕션 트래픽 <a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a>이 필요한</strong> ML 모델 교체·인프라 마이그레이션에 최적이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>트래픽 <a href="/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/">미러링</a></strong> | 섀도 배포의 핵심 메커니즘 |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/">Istio</a> VirtualService mirror</strong> | 구현 도구 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/">카나리 배포</a></strong> | 사용자 영향이 있는 대안 |
| **A/B 테스트** | 두 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 비교 (사용자 응답 포함) |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/197_dark_launching_traffic_shadow/">Dark Launching</a></strong> | [피처 플래그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/) 기반 비공개 테스트 |

### 📈 관련 키워드 및 발전 흐름도

```text
[스테이징 테스트 (합성 트래픽)]
    |
    v
[카나리 배포 (실 트래픽 1~5%, 사용자 영향 있음)]
    |
    v
[섀도 배포 (실 트래픽 미러링, 사용자 영향 제로)]
    |
    v
[Istio mirror (2018~) — Service Mesh 기반 자동 미러링]
    |
    v
[현재: AI 기반 섀도 분석 — 미러링 결과 자동 비교·판정]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 섀도 배포는 신인 배우(v2)가 <strong>무대 뒤에서 같이 연기</strong>하지만 관객은 못 보는 거예요.
2. 연기 결과만 비교해서 "신인이 더 잘하면" 다음에 무대에 올려요.
3. 관객(사용자)은 **아무 영향 없이** 베테랑(v1) 공연만 보니까 안전하답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 118 / 973

<- **이전**: [117. 롤링 업데이트 (Rolling Update Deployment) - K8s 기본 무중단 배포 전략](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/117_rolling_update_deployment/)
**다음**: [119. GitOps (Single Source of Truth) - Git을 단일 진실 원천으로 한 선언적 운영](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) ->

---
