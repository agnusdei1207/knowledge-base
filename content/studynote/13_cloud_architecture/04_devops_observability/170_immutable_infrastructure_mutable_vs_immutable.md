---
title: 170. 가변 인프라 (Mutable Infrastructure) vs 불변 인프라 (Immutable Infrastructure)
date: '2026-04-21'
tags:
- studynote-cloud-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 가변 인프라는 실행 중인 서버를 직접 고치는 운영 방식이고, [[204_immutable_infrastructure_configuration_drift_prevention|불변 인프라]]는 변경을 새 이미지와 새 인스턴스로 표현하는 배포 방식이다.
> 2. **가치**: [[204_immutable_infrastructure_configuration_drift_prevention|불변 인프라]]는 [[193_configuration_drift|구성 편류]] ([[193_configuration_drift|Configuration Drift]])를 줄여 재현성, [[606_auditing_linux_auditd|감사]] 추적, [[098_rollback_strategy_pipeline_error_threshold|롤백]] 속도를 함께 높인다.
> 3. **판단 포인트**: 현대 [[531_cloud_native_architecture|클라우드 네이티브]] [[090_service_kubernetes_network_load_balancing|서비스]]는 불변을 기본값으로 두고, 상태 저장 레거시나 긴급 [[658_ir_recovery|복구]]처럼 불가피한 경우에만 제한적으로 가변 운영을 허용해야 한다.

---

## Ⅰ. 개요 및 필요성

가변 인프라 (Mutable Infrastructure)는 운영 중인 서버에 [[538_ssh_vs_telnet_secure_remote|SSH]] ([[538_ssh_vs_telnet_secure_remote|Secure Shell]])로 접속해 패키지를 설치하고 [[009_config|설정]] [[501_file_definition_logical_record|파일]]을 바꾸며 상태를 누적시키는 방식이다. 반대로 [[204_immutable_infrastructure_configuration_drift_prevention|불변 인프라]] ([[204_immutable_infrastructure_configuration_drift_prevention|Immutable Infrastructure]])는 서버나 [[561_container_based_deployment|컨테이너]]를 "수정 대상"이 아니라 "교체 대상"으로 본다. 코드나 [[009_config|설정]]이 바뀌면 기존 서버를 손대지 않고, 새 이미지로 만든 인스턴스를 배포한 뒤 이전 것을 폐기한다.

이 차이가 중요해진 이유는 운영 환경이 커질수록 사람 손으로 만든 미세한 차이가 장애 원인이 되기 때문이다. 같은 애플리케이션을 띄운 두 서버라도 한쪽만 긴급 패치를 먼저 받거나, [[568_logs_distributed_logging_elk_fluentd|로그]] [[009_config|설정]]이 다르거나, [[336_library_vs_framework|라이브러리]] [[288_version_ihl_tos_total_length|버전]]이 섞이면 어느 순간 "왜 이 서버만 다르게 동작하는가"를 설명할 수 없어진다. 이런 누적 차이가 바로 [[193_configuration_drift|구성 편류]]이며, 전형적인 눈송이 서버 ([[541_cassandra|Snowflake]] Server) 문제다.

다음 그림은 시간이 지날수록 가변 인프라가 왜 예측하기 어려워지는지 보여준다.

```text
┌──────────────────────────────────────────────────────────────┐
│        같은 서비스라도 변경 방식에 따라 상태 이력이 달라진다 │
├───────────────────────────┬──────────────────────────────────┤
│ 가변 인프라               │ 불변 인프라                      │
├───────────────────────────┼──────────────────────────────────┤
│ v1 서버                    │ image:v1                         │
│   └─ SSH hotfix A          │   └─ 인스턴스 A/B 기동          │
│       └─ 수동 설정 변경 B  │ image:v2 빌드                    │
│           └─ 임시 패치 C   │   └─ 인스턴스 C/D 기동          │
│               = 서버마다 다름│       └─ 트래픽 전환 후 v1 폐기 │
└───────────────────────────┴──────────────────────────────────┘
```

[[204_immutable_infrastructure_configuration_drift_prevention|불변 인프라]]가 필요한 이유는 단순히 "새것이 좋아서"가 아니다. 운영의 핵심 질문을 "누가 이 서버를 어떻게 고쳤는가"에서 "어떤 [[288_version_ihl_tos_total_length|버전]]의 이미지가 언제 배포되었는가"로 바꾸기 위해서다. 질문이 바뀌면 [[606_auditing_linux_auditd|감사]], [[658_ir_recovery|복구]], 보안 패치, 확장 [[268_strategy_pattern|전략]]도 훨씬 단순해진다.

- **📢 섹션 요약 비유**: 가변 인프라는 오래된 건물을 그때그때 덧대며 수리하는 방식이고, [[204_immutable_infrastructure_configuration_drift_prevention|불변 인프라]]는 설계도가 바뀌면 새 건물을 지어 입주자를 옮기는 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[204_immutable_infrastructure_configuration_drift_prevention|불변 인프라]]의 핵심 원리는 **Build Once, Deploy Many**다. 한 번 검증한 [[075_artifact_management_nexus_docker_registry|아티팩트]]를 여러 환경에 반복 배포해야 하며, 배포 시점에 서버 내부에서 패키지 설치나 임시 수정이 일어나면 안 된다. 그래서 불변 배포는 보통 이미지 빌드, 취약점 검사, 서명, [[235_registry_immutable_tag|레지스트리]] 저장, 새 인스턴스 기동, 헬스체크, 트래픽 전환, 구버전 폐기 순서로 진행된다.

```text
┌────────────────────────────────────────────────────────────────────┐
│           Immutable Delivery Pipeline: 수정 대신 교체              │
├────────────────────────────────────────────────────────────────────┤
│ Source / Dockerfile / Packer / IaC                                │
│                 │                                                  │
│                 ▼                                                  │
│      CI/CD (Continuous Integration / Continuous Delivery)          │
│   ├─ 테스트                                                       │
│   ├─ 이미지 빌드                                                  │
│   ├─ 취약점 스캔·서명                                             │
│   └─ image:v2 생성                                                │
│                 │                                                  │
│                 ▼                                                  │
│      Registry / AMI (Amazon Machine Image) Catalog                │
│                 │                                                  │
│                 ▼                                                  │
│ Deployment Controller / Orchestrator                              │
│   ├─ 새 Pod·VM (Virtual Machine) 기동                             │
│   ├─ Readiness Check 통과                                         │
│   ├─ Canary / Blue-Green으로 트래픽 전환                          │
│   └─ 이전 버전 종료                                               │
└────────────────────────────────────────────────────────────────────┘
```

[[204_immutable_infrastructure_configuration_drift_prevention|불변 인프라]]가 성립하려면 [[001_dikw_pyramid|데이터]]와 실행 환경을 분리해야 한다. 애플리케이션 바이너리, [[001_operating_system_purpose|운영체제]] 패키지, 에이전트는 이미지 안에 굳히고, [[160_session_controlling_terminal|세션]] [[001_dikw_pyramid|데이터]]나 업로드 [[501_file_definition_logical_record|파일]]은 [[002_database_definition|데이터베이스]], [[494_object_storage|오브젝트 스토리지]], 외부 볼륨으로 분리한다. 그래야 인스턴스를 언제든 버려도 [[090_service_kubernetes_network_load_balancing|서비스]] 상태를 잃지 않는다.

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| 베이스 이미지 | 공통 [[001_operating_system_purpose|운영체제]]·보안 패치 제공 | 골든 이미지 (Golden Image) 주기적 갱신 |
| 이미지 [[256_builder_pattern_step_by_step_creation|빌더]] | [[067_dockerfile_container_image_build_script|Dockerfile]], [[199_packer_aws_ami_baking|Packer]] 등으로 [[075_artifact_management_nexus_docker_registry|아티팩트]] [[087_process_state_transition|생성]] | 환경별 분기보다 템플릿화 우선 |
| [[235_registry_immutable_tag|레지스트리]] | [[288_version_ihl_tos_total_length|버전]] 보관, 재배포 기준점 | 태그보다 불변 Digest 사용 권장 |
| 오케스트레이터 | 새 인스턴스 기동과 트래픽 제어 | Readiness / [[313_rollback|Rollback]] 자동화 |
| 외부 상태 저장소 | [[001_dikw_pyramid|데이터]] [[196_durability_permanent_storage|영속성]] 유지 | [[561_container_based_deployment|컨테이너]] 내부 로컬 디스크 의존 금지 |

여기서 자주 생기는 오해가 "불변이면 [[009_config|설정]]을 바꿀 수 없다"는 생각이다. 실제로는 실행 이미지는 불변이지만, [[156_environment_variables|환경 변수]], 비밀 값 ([[514_secret_management_vault_kms|Secret]]), [[306_service_discovery_pattern|서비스 디스커버리]], [[247_feature_label_variables|피처]] 플래그는 외부에서 주입된다. 즉, **코드와 런타임 환경의 경계를 엄격히 관리하는 것**이지, 모든 값을 하드코딩하는 것이 아니다.

- **📢 섹션 요약 비유**: [[204_immutable_infrastructure_configuration_drift_prevention|불변 인프라]]는 매장에서 요리하지 않고 중앙 공장에서 같은 도시락을 만들어 보내는 체계라서, 어느 지점에서 먹어도 품질이 크게 흔들리지 않는다.

---

## Ⅲ. 비교 및 연결

가변과 불변의 차이는 배포 방식만의 문제가 아니라 운영 철학의 차이다. 가변 인프라는 "서버를 보살피는 운영"에 가깝고, [[204_immutable_infrastructure_configuration_drift_prevention|불변 인프라]]는 "서버를 대량 교체하는 운영"에 가깝다. 따라서 디버깅 방식, 보안 패치 방식, 자동화 범위가 모두 달라진다.

| 비교 축 | 가변 인프라 | [[204_immutable_infrastructure_configuration_drift_prevention|불변 인프라]] |
| :--- | :--- | :--- |
| 변경 단위 | 서버 내부 상태 | [[288_version_ihl_tos_total_length|버전]]된 이미지·[[075_artifact_management_nexus_docker_registry|아티팩트]] |
| 장애 원인 추적 | 사람 작업 기록에 의존 | 이미지 [[288_version_ihl_tos_total_length|버전]]과 배포 이력 중심 |
| [[098_rollback_strategy_pipeline_error_threshold|롤백]] 방식 | 수동 [[658_ir_recovery|복구]]·재패치 | 이전 이미지 재배포 |
| 확장성 | 서버마다 차이 누적 가능 | 동일 이미지 수평 확장 |
| 보안 패치 | 운영 중 개별 서버 패치 | 패치된 이미지 재빌드 후 교체 |
| 디버깅 | [[538_ssh_vs_telnet_secure_remote|SSH]] 접속으로 즉시 [[396_validation|확인]] | [[568_logs_distributed_logging_elk_fluentd|로그]]·[[342_routing_metric_hop_bandwidth_delay|메트릭]]·트레이스로 분석 우선 |

[[204_immutable_infrastructure_configuration_drift_prevention|불변 인프라]]는 [[793_iac_idempotency_template|IaC]] ([[062_infrastructure_as_code|Infrastructure as Code]]), [[194_blue_green_deployment_strategy|블루-그린 배포]] ([[304_process|Blue-Green Deployment]]), [[115_canary_deployment_gradual_rollout|카나리 배포]] ([[115_canary_deployment_gradual_rollout|Canary Deployment]]), GitOps와 자연스럽게 연결된다. IaC는 "기반 인프라를 코드로 만드는 기술"이고, [[204_immutable_infrastructure_configuration_drift_prevention|불변 인프라]]는 "그 위에 올라가는 실행 단위를 교체하는 기술"이다. 다시 말해 IaC가 땅과 도로를 정리한다면, [[204_immutable_infrastructure_configuration_drift_prevention|불변 인프라]]는 같은 규격의 건물을 찍어내는 공장에 가깝다.

반면 [[089_configuration_management|구성 관리]] 도구인 [[198_ansible_os_configuration_management_ssh|Ansible]], Chef, Puppet은 역사적으로 가변 인프라와 친했다. 다만 오늘날에는 이 도구들도 부팅 직후 [[459_quic_fec_forward_error_correction|초기]] 구성이나 이미지 빌드 단계에서 사용되며, 운영 중 반복 [[538_ssh_vs_telnet_secure_remote|SSH]] 패치보다 "이미지 [[087_process_state_transition|생성]] 과정 자동화" 쪽으로 역할이 이동하고 있다. 즉, 도구의 문제가 아니라 **언제 변경을 적용하느냐**가 본질이다.

- **📢 섹션 요약 비유**: 가변 인프라가 현장에서 목수가 집을 계속 손보는 방식이라면, [[204_immutable_infrastructure_configuration_drift_prevention|불변 인프라]]는 공장에서 규격화된 모듈을 만들어 현장에서 교체하는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 "무조건 불변"보다 "어디까지를 불변으로 둘 것인가"를 판단해야 한다. 웹 애플리케이션, [[014_api_posix|API]] 서버, 배치 워커처럼 무상태에 가까운 워크로드는 불변이 기본값이다. 반면 [[002_database_definition|데이터베이스]], 대용량 스토리지 서버, 네트워크 어플라이언스처럼 상태가 강한 시스템은 교체 [[268_strategy_pattern|전략]]을 세밀하게 설계하지 않으면 배포보다 마이그레이션이 더 큰 위험이 될 수 있다.

### 채택 판단 기준

1. **불변을 기본 채택할 때**
   - 자동 확장과 잦은 배포가 필요한 [[090_service_kubernetes_network_load_balancing|서비스]]
   - 동일 환경 재현성과 [[606_auditing_linux_auditd|감사]] 추적이 중요한 조직
   - [[561_container_based_deployment|컨테이너]], [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] ([[205_kubernetes_container_orchestration|Kubernetes]]), 오토스케일링을 이미 사용 중인 환경

2. **하이브리드가 필요한 때**
   - 상태 저장 서버가 크고 교체 시간이 긴 경우
   - [[022_kernel_role|커널]] 라이브 패치나 긴급 보안 완화가 필요한 특수 시스템
   - 레거시 미들웨어가 이미지 재기동보다 현장 수정에 더 강하게 묶인 경우

3. **가변 운영을 허용하더라도 지켜야 할 원칙**
   - 운영 중 수동 수정은 임시 조치로만 취급
   - 수정 내용을 반드시 코드와 이미지로 환원
   - 다음 배포에서 해당 수동 변경이 사라지도록 표준화

다음 체크리스트는 시험 답안과 실무 설계 모두에서 유효하다.

| 체크 항목 | 왜 중요한가 | 권장 판단 |
| :--- | :--- | :--- |
| 상태 외부화 | 서버 교체 가능성의 전제 | [[160_session_controlling_terminal|세션]]·[[501_file_definition_logical_record|파일]]·캐시는 외부 저장소로 분리 |
| 이미지 [[288_version_ihl_tos_total_length|버전]] 관리 | [[098_rollback_strategy_pipeline_error_threshold|롤백]]과 [[606_auditing_linux_auditd|감사]]의 기준 | Digest, 태그 [[164_policy|정책]], 배포 이력 보존 |
| 배포 관문 | 불변이라도 잘못된 이미지는 위험 | 테스트, 스캔, 서명, 헬스체크 필수 |
| 관측성 | [[538_ssh_vs_telnet_secure_remote|SSH]] 없는 운영의 전제 | [[568_logs_distributed_logging_elk_fluentd|로그]]·[[342_routing_metric_hop_bandwidth_delay|메트릭]]·트레이스 선행 구축 |
| 긴급 조치 프로세스 | 현실적 예외 처리 | 핫픽스 후 이미지 재생성 의무화 |

안티패턴도 분명하다. [[561_container_based_deployment|컨테이너]]를 쓰면서 배포 스크립트 안에서 운영 서버에 접속해 패키지를 설치하는 것은 불변 철학을 무너뜨린다. 또한 불변을 말하면서 업로드 [[501_file_definition_logical_record|파일]]과 [[160_session_controlling_terminal|세션]]을 로컬 디스크에 두면 인스턴스 교체 때마다 [[001_dikw_pyramid|데이터]] 유실 위험이 생긴다. [[204_immutable_infrastructure_configuration_drift_prevention|불변 인프라]]는 도구 이름이 아니라 **운영 계약**이라는 점을 놓치면 안 된다.

- **📢 섹션 요약 비유**: [[204_immutable_infrastructure_configuration_drift_prevention|불변 인프라]] 운영은 공연 중 악기를 즉석 수리하는 대신, 미리 튜닝된 예비 악기를 바로 교체해 연주를 이어 가는 방식과 같다.

---

## Ⅴ. 기대효과 및 결론

[[204_immutable_infrastructure_configuration_drift_prevention|불변 인프라]]를 정착시키면 배포가 "서버를 고치는 사건"에서 "[[288_version_ihl_tos_total_length|버전]]을 교체하는 반복 작업"으로 바뀐다. 그 결과 [[098_rollback_strategy_pipeline_error_threshold|롤백]]은 빨라지고, 환경 차이로 인한 장애는 줄며, 보안 패치도 개별 서버 점검이 아니라 이미지 재발행 프로세스로 표준화된다. 특히 수평 확장과 자동 [[658_ir_recovery|복구]]가 많은 클라우드 환경에서는 이 예측 가능성이 큰 장점이 된다.

물론 전제조건도 있다. 이미지 빌드 시간이 너무 길면 배포 민첩성이 떨어지고, [[568_logs_distributed_logging_elk_fluentd|로그]]·[[342_routing_metric_hop_bandwidth_delay|메트릭]] 체계가 부족하면 [[538_ssh_vs_telnet_secure_remote|SSH]] 없는 운영이 오히려 불편할 수 있다. 또한 상태 저장 워크로드는 별도의 [[001_dikw_pyramid|데이터]] 분리와 마이그레이션 [[268_strategy_pattern|전략]] 없이는 단순한 교체 모델로 해결되지 않는다.

결국 기억해야 할 문장은 간단하다. **[[204_immutable_infrastructure_configuration_drift_prevention|불변 인프라]]는 서버를 완벽하게 만들겠다는 발상이 아니라, 서버를 쉽게 버릴 수 있게 만들어 운영을 단순화하겠다는 발상**이다. 현대 DevOps와 플랫폼 엔지니어링에서 중요한 것은 잘 고치는 능력보다, 안전하게 다시 만들어 교체하는 능력이다.

- **📢 섹션 요약 비유**: [[204_immutable_infrastructure_configuration_drift_prevention|불변 인프라]]는 낡은 전구를 현장에서 뜯어 수리하는 것이 아니라, 규격화된 새 전구로 바로 갈아 끼우는 유지보수 방식이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[193_configuration_drift|구성 편류]] ([[193_configuration_drift|Configuration Drift]]) | 가변 인프라에서 누적되는 상태 차이, [[204_immutable_infrastructure_configuration_drift_prevention|불변 인프라]]의 직접적인 해결 대상 |
| 골든 이미지 (Golden Image) | 공통 보안 패치와 기본 에이전트를 고정한 기준 이미지 |
| [[793_iac_idempotency_template|IaC]] ([[062_infrastructure_as_code|Infrastructure as Code]]) | 기반 자원 [[087_process_state_transition|생성]] 자동화, 불변 이미지 배포의 토대 |
| 블루-그린 / [[115_canary_deployment_gradual_rollout|카나리 배포]] | 새 [[288_version_ihl_tos_total_length|버전]] 교체 시 무중단 전환을 돕는 트래픽 [[268_strategy_pattern|전략]] |
| [[119_gitops_single_source_of_truth|GitOps]] | 원하는 상태를 Git에 선언하고 실제 환경을 지속적으로 일치시키는 운영 모델 |
| 관측성 ([[642_observability_telemetry|Observability]]) | [[538_ssh_vs_telnet_secure_remote|SSH]] 접속 대신 [[568_logs_distributed_logging_elk_fluentd|로그]]·[[342_routing_metric_hop_bandwidth_delay|메트릭]]·트레이스로 운영 상태를 파악하는 기반 |

### 📈 관련 키워드 및 발전 흐름도

```text
수동 서버 관리
    │
    ▼
가변 인프라 + SSH 운영
    │
    ├─ 문제: 구성 편류 · 눈송이 서버 · 느린 롤백
    ▼
이미지 빌드 자동화 (Packer · Dockerfile)
    │
    ▼
불변 인프라 + Blue-Green / Canary
    │
    ▼
IaC + GitOps + 오토스케일링 기반 플랫폼 운영
```

이 흐름은 "서버 개체를 보수하는 운영"에서 "[[288_version_ihl_tos_total_length|버전]]된 [[075_artifact_management_nexus_docker_registry|아티팩트]]를 대량 교체하는 운영"으로 무게중심이 이동하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 가변 인프라는 장난감 자동차가 고장 날 때마다 테이프를 붙여 계속 쓰는 방법이에요.
2. [[204_immutable_infrastructure_configuration_drift_prevention|불변 인프라]]는 새로 만든 똑같은 자동차로 바로 바꾸는 방법이라서 항상 상태를 예측하기 쉬워요.
3. 그래서 친구들이 여러 대를 같이 써도 "왜 이 차만 이상하지?" 같은 일이 훨씬 적어져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 169 / 371

← **이전**: [[169_iac_infrastructure_as_code_terraform|169. 인프라스트럭처 애즈 코드 (IaC, Infrastructure as Code)]]
**다음**: [[171_idempotency_iac_terraform|171. 멱등성 (Idempotency in IaC)]] →

---
