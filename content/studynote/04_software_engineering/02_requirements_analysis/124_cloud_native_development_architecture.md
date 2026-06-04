+++
title = "124. 클라우드 네이티브 아키텍처 - CNCF 기반 현대 소프트웨어 개발 패러다임"
date = 2026-04-19

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/)는 <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/">컨테이너</a>·<a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/">MSA</a>·<a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/">CI</a>/CD·선언적 <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a></strong>를 핵심으로 하여 클라우드 환경의 <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/571_resiliency_fault_tolerance_patterns/">탄력성</a>·확장성·복원력을 최대한 활용</strong>하는 소프트웨어 개발·운영 패러다임이다.
> 2. **가치**: [Lift](/knowledge-base/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/) & Shift(기존 시스템을 그대로 클라우드로 이전)로는 클라우드의 이점을 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)%도 활용하지 못하지만, [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/)로 설계하면 <strong>오토스케일링·셀프힐링·글로벌 배포</strong>가 자연스럽게 구현된다.
> 3. **판단 포인트**: [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/)([Cloud Native](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/199_cloud_native_architecture_msa_cicd_devops/) Computing Foundation)의 **Trail Map**([컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)화->[CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD->[오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/)->관측성->[서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/))이 도입 로드맵이며, <strong>12 Factor App</strong>이 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 설계 원칙이다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    클라우드 네이티브 4대 핵심                          |
+-------------------------------------------------------+
|  1. 컨테이너 (Docker/containerd)                      |
|  2. MSA (마이크로서비스)                              |
|  3. CI/CD (지속적 통합·배포)                          |
|  4. 선언적 API (K8s Desired State)                    |
|                                                       |
|  + DevOps 문화 + 관측성 + 서비스 메시                 |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/)는 처음부터 <strong>바다(클라우드)에서 살도록 진화한 물고기</strong>이고, [Lift](/knowledge-base/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/) & Shift는 육지 동물이 바다에 던져진 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 12 Factor App (주요)

| Factor | 설명 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/007_codebase/">코드베이스</a></strong> | 1앱 = 1리포 |
| **의존성** | 명시적 선언 |
| <strong><a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a></strong> | 환경 변수로 분리 |
| <strong><a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/013_port_binding/">포트 바인딩</a></strong> | 자체 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 서버 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a></strong> | stdout 스트림 |
| **프로세스** | [Stateless](/knowledge-base/studynote/15_devops_sre/05_devsecops/239_stateless_redis/) |

- **📢 섹션 요약 비유**: 12 Factor는 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/)의 <strong>건축 법규</strong>다. 이 규칙을 따라야 건물(앱)이 안전하다.

---

## Ⅲ. 비교 및 연결

| 비교 | 전통 | [Lift](/knowledge-base/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/) & Shift | [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) |
|:---|:---|:---|:---|
| **아키텍처** | 모놀리식 | 모놀리식 | <strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/">MSA</a></strong> |
| **배포** | 수동 | 수동 | <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/">CI</a>/CD</strong> |
| <strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/">스케일링</a></strong> | 수동 | 반자동 | **자동** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) Trail Map
1. [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)화 -> 2. [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD -> 3. K8s -> 4. 관측성([Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/)) -> 5. [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)([Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)) -> 6. 보안([OPA](/knowledge-base/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/)).

---

## Ⅴ. 기대효과 및 결론

[클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/)는 <strong>현대 소프트웨어 개발의 표준 패러다임</strong>이며, [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) 생태계가 사실상 모든 기술 스택을 포괄한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/">CNCF</a></strong> | [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 재단 |
| **12 Factor** | 설계 원칙 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/">컨테이너</a></strong> | 핵심 런타임 |
| **K8s** | [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) 표준 |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/">서비스 메시</a></strong> | 통신 인프라 ([Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)) |

### 📈 관련 키워드 및 발전 흐름도

```text
[온프레미스 (전통, ~2010s)]
    |
    v
[Lift & Shift (IaaS, 2010~)]
    |
    v
[클라우드 네이티브 (CNCF, 2015~) — 컨테이너+MSA+CI/CD]
    |
    v
[서비스 메시 + GitOps (2018~)]
    |
    v
[현재: Platform Engineering — 개발자 경험 최적화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/)는 처음부터 <strong>바다(클라우드)에서 살도록 태어난 물고기</strong>예요.
2. 옛날 방식은 <strong>육지 동물을 바다에 던지는(<a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/">Lift</a> &amp; Shift)</strong> 거라 잘 못 수영해요.
3. 물고기처럼 설계하면 **파도(트래픽)가 커도 자유롭게** 헤엄칠 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 124 / 973

<- **이전**: [123. 서버리스 & FaaS (Serverless / AWS Lambda) - 인프라 없는 함수 단위 컴퓨팅](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/123_serverless_faas_aws_lambda/)
**다음**: [125. 12 Factor App - 클라우드 네이티브 애플리케이션 설계 12원칙](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/125_12_factor_app_cloud_native_architecture/) ->

---
