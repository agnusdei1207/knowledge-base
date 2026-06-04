+++
title = "11. 빌드, 릴리스, 실행 (Build, Release, Run) 단계의 엄격한 분리"
date = 2026-04-05

[taxonomies]
tags = ["devops_sre"]

[extra]
tags = ["devops_sre"]
+++

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 빌드, 릴리스, 실행 원칙은 코드를 프로덕션에 배포하는 과정을 세 개의 엄격히 분리된 단계로 나누어야 한다는 12팩터 앱의 제5원칙이다. 빌드 단계에서 소스코드를 실행 가능한 바이너리로 변환하고, 릴리스 단계에서 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)과 결합하여 배포 가능한 패키지를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하며, 실행 단계에서 그 패키지를 런타임에서 실행한다.
> 2. **가치**: 이 세 단계를 분리하면 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)이 특정 단계로 한정되어 신속 정확해지고, 각 단계의 책임이 명확해져 운영 효율성과 시스템 안정성이 향상된다.
> 3. **융합**: [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인에서 이 원칙은 명시적 단계 분리로 구현되고, GitOps에서는 빌드/릴리스/실행이 자동화된 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인으로 연결된다.

---

### Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

소프트웨어 배포 프로세스는 본질적으로 세 가지 핵심 활동으로 구성된다. 첫째, 소스코드를 실행 가능한 산출물로 변환하는 활동(빌드)이고, 둘째, 그 산출물에 환경별 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)을 부여하여 배포 가능한 패키지로 완성하는 활동(릴리스)이며, 셋째, 그 패키지를 실제 런타임 환경에서 실행하는 활동(실행)이다.

전통적인 방식에서는 이 단계들이 혼재되는 경우가 많았다. 빌드 스크립트 내에서 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)을 직접 하드코딩하거나, 실행 단계에서 갑자기 소스코드를 수정하거나, 빌드 산출물에 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)이 포함되어 환경 간 차이가 발생등현상이 그것이다. 이러한 혼재는 다음과 같은 문제를 야기한다:
- **추적 불가능성**: 어떤 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)의 코드가 어떤 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)과 함께 배포되었는지 알 수 없다.
- <strong><a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/">롤백</a>의 어려움</strong>: 문제가 발생했을 때 이전 상태로 돌아가려면 여러 요소를 동시에 원복해야 한다.
- **재현성의 부재**: 동일 환경에서의 재배포가 보장되지 않는다.

12팩터 앱의 빌드, 릴리스, 실행 원칙은 이 세 단계를 엄격히 분리하고 각각을 독립적으로 관리할 것을 요구한다. 이렇게 하면 문제는"빌드에러 -> 빌드만 다시, [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)오류 -> 릴리스만 다시"로 특정할 수 있어 수정이 용이하다.

아래 다이어그램은 전통적 혼재 방식과 세 단계 분리의 차이를 보여준다.

```text
[단계 혼재 vs 단계 분리]

❌ 전통적 혼재 방식 (문제: 무엇이 무엇을 cause했는지 불분명)
+-------------------------------------------------------------+
|  소스 코드 --+--- 빌드 ---+--- 설정 ---+--- 실행 ----> 실행 중인 앱
|             |    |        |    |       |                     |
|             |  코드 수정  | 설정 수정 | 런타임 수정          |
|             |  (언제? 누가?)| (어디에?)  | (왜?)              |
+-------------------------------------------------------------+
  문제: 각 단계의 변경 이력이 혼잡, 롤백 시 무엇을 롤백해야?

✓ 12팩터 방식 (세 단계 엄격 분리)
+-------------------------------------------------------------+
|                                                             |
|  [Stage 1: BUILD]                                           |
|  +-----------------------------------------------------+   |
|  | 소스 코드 (Git Commit a1b2c3d)                       |   |
|  |          |                                            |   |
|  |          v                                            |   |
|  | 실행 가능한 아티팩트 (Docker Image: app:v1.2.3)      |   |
|  +-----------------------------------------------------+   |
|                        |                                   |
|                        v                                   |
|  [Stage 2: RELEASE]                                         |
|  +-----------------------------------------------------+   |
|  | 아티팩트 (app:v1.2.3) + 설정 (production config)    |   |
|  |          |                                            |   |
|  |          v                                            |   |
|  | 배포 가능한 패키지 (Release v1.2.3-prod-20240405)   |   |
|  +-----------------------------------------------------+   |
|                        |                                   |
|                        v                                   |
|  [Stage 3: RUN]                                            |
|  +-----------------------------------------------------+   |
|  | 런타임에서 실행 (컨테이너/프로세스)                          |   |
|  | - 특정 버전의 앱이 특정 설정으로 동작                     |   |
|  +-----------------------------------------------------+   |
|                                                             |
|  장점: 각 단계가 독립적으로 추적/관리 가능                    |
+-------------------------------------------------------------+
```

> 📢 **섹션 요약 비유**: 빌드/릴리스/실행 분리는"음식의 조리 단계"와 같다. 요리(빌드)는 요리사가 하고, 플레이팅(릴리스)은 웨이터가 하며, 서빙(실행)은 호스트가 한다. 만약 맛([설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/))이 잘못되었으면 요리사는 플레이팅 담당자에게 돌아가서 새 음식을 요청할 수 있고(릴리스 재실행), 서빙 단계에서 문제가 있으면 호스트가 새로운 접시를 요청할 수 있다(재실행).

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

세 단계가 어떻게 구현되고, [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인에서 어떻게 활용되는지 상세히 분석한다.

| 단계 | 입력 | 출력 | 담당 | 핵심 특성 |
|:---|:---|:---|:---|:---|
| **빌드 (Build)** | 소스코드 (Git Commit) | 실행 가능한 [아티팩트](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/) (바이너리/이미지) | [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/) [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 | 불변성 (같은 입력 = 같은 출력) |
| **릴리스 (Release)** | [아티팩트](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/) + 환경 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) | 배포 가능한 패키지 | CD [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 | 추적 가능성 ([버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) + [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 조합) |
| **실행 (Run)** | 배포 패키지 | 런타임 프로세스 | [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 오케스트레이터 | [멱등성](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/) (재실행해도 동일 결과) |

아래는 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인에서의 빌드/릴리스/실행 단계를 보여주는 [ASCII](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램이다.

```text
[CI/CD 파이프라인에서의 빌드/릴리스/실행]

+---------------------------------------------------------------------+
|                        CI/CD 파이프라인                              |
+---------------------------------------------------------------------+
|                                                                      |
|  1. BUILD 단계                                                       |
|  +---------------------------------------------------------------+  |
|  |  Git Repository                    CI Pipeline                |  |
|  |  +--------------+                  +----------------------+   |  |
|  |  | Commit       | --WebHook 트리거--> | 빌드 (Build)         |   |  |
|  |  | a1b2c3d      |                  | - 의존성 설치         |   |  |
|  |  | (소스 코드)   |                  | - 컴파일/번들링       |   |  |
|  |  +--------------+                  | - 테스트 실행         |   |  |
|  |                                      | = Docker Image       |   |  |
|  |                                      |   app:a1b2c3d        |   |  |
|  |                                      +----------+-----------+  |  |
|  +-------------------------------------------------+--------------+  |
|                                                      |                 |
|                                                      v                 |
|  2. RELEASE 단계                                                      |
|  +---------------------------------------------------------------+  |
|  |                           CD Pipeline                          |  |
|  |  +----------------------+    +--------------------------+   |  |
|  |  | 아티팩트 (Build)      |    | 릴리스 (Release)          |   |  |
|  |  | app:a1b2c3d          | +  | - 환경 설정 injection   |   |  |
|  |  +----------------------+    | - 버전 태그 생성          |   |  |
|  |                               | = Release a1b2c3d-prod   |   |  |
|  |                               +----------+-----------+   |  |
|  +----------------------------------------------+--------------+  |
|                                                     |                 |
|                                                     v                 |
|  3. RUN 단계                                                           |
|  +---------------------------------------------------------------+  |
|  |                        Kubernetes / Container Runtime          |  |
|  |  +------------------------------------------------------+   |  |
|  |  |  실행 (Run)                                           |   |  |
|  |  |  - Release a1b2c3d-prod 이미지 가져옴                  |   |  |
|  |  |  - 환경 변수/시크릿 주입                              |   |  |
|  |  |  - 컨테이너 시작                                       |   |  |
|  |  |  = 실행 중인 앱 (a1b2c3d, production 환경)             |   |  |
|  |  +------------------------------------------------------+   |  |
|  +---------------------------------------------------------------+  |
+---------------------------------------------------------------------+
```

> 📢 **섹션 요약 비유**: 빌드/릴리스/실행은"영화 제작의 단계"와 같다. 빌드는 촬영(소스 -> 영상물)으로, 릴리스는 편집과 배급용 Master [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)(영상물 + 자막/[설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)), 실행은 영화관 상영(Master -> 스크린투영)과 같다. 만약 자막에 문제가 있으면([설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 문제) 편집 단계만 다시 하고, 영화관 장비 문제면(실행 문제) 장비만 다시 조정하면 된다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

빌드/릴리스/실행 원칙은 [GitOps](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/), [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/), [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 기술과 결합하여 현대적 DevOps의 핵심 토대가 된다.

| 관련 개념 | 빌드/릴리스/실행 원칙과의 결합 | 시너지 효과 |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/">GitOps</a></strong> | 빌드 -> Git Commit, 릴리스 -> Git Tag, 실행 -> ArgoCD Sync | 변경 이력 완벽 추적 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/">IaC</a></strong> | 빌드 = 코드 컴파일, 릴리스 = 인프라 [프로비저닝](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/), 실행 = 인프라 가동 | 인프라도 동일한 원칙 적용 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/">Docker</a></strong> | 빌드 = [Dockerfile](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/067_dockerfile_container_image_build_script/) 빌드, 릴리스 = 이미지 + [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/), 실행 = [docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) run | [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)의 불변성 보장 |
| <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/">CI</a>/CD</strong> | 각 단계가 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인의 Stage로 구현 | 자동화된 빌드/릴리스/실행 |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/193_rolling_update_deployment_kubernetes/">롤링 배포</a></strong> | 새 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 빌드 -> 새 릴리스 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) -> 점진적 실행 전환 | 무중단 업데이트 |

특히 GitOps와의 결합은 빌드/릴리스/실행 원칙의 추적 가능성을 완벽하게 한다. Git Repo의 커밋 히스토리가 빌드 이력이 되고, 릴리스 태그가 실행 환경을 결정하며, ArgoCD나 FluxCD가 실행 단계를 자동화한다.

```text
[GitOps + 빌드/릴리스/실행의 결합]

Git Repository
+-------------------------------------------------------------+
|  Commit a1b2c3d: "버그 픽스 - 결제 API 오류 수정"              |
|       |                                                      |
|       +---> CI Pipeline: Build (Docker Image: app:a1b2c3d)   |
|       |                                                      |
|       +---> Git Tag: v1.2.3-prod                                |
|                   |                                           |
|                   v                                           |
|  ArgoCD / FluxCD (GitOps 에이전트)                              |
|       |                                                       |
|       +-- "v1.2.3-prod" 태그 감시                             |
|       |                                                       |
|       +---> Kubernetes: Run (app:a1b2c3d with prod 설정)       |
|                                                             |
|  모니터링/알람 ---> 문제 발견 ---> "v1.2.3-prod" 롤백 요청       |
|       |                                                       |
|       +---> Git Tag: v1.2.2-prod (이전 버전)로 변경            |
|                   |                                           |
|                   v                                           |
|           ArgoCD가 이전 버전으로 Sync 실행                       |
```

> 📢 **섹션 요약 비유**: 빌드/릴리스/실행과 GitOps의 결합은"음악 녹음과 음원 배포"에 비유할 수 있다. 녹음실(빌드)에서 음원을 녹음하고, 녹음 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에 자막/음향 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)(릴리스)을 추가하여 음원 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 완성하고, 음원 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 음악 스트리밍 플랫폼(실행)에 올려 청중이 들을 수 있게 한다. 만약 음원 자체에 문제가 있으면(빌드) 녹음실로 돌아가서 다시 녹음하고, 음원 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 문제면(릴리스) 편집실에서 수정하면 된다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

실무에서 빌드/릴리스/실행 원칙을 적용할 때 흔히 발생하는 문제와 해결 방안을 분석한다.

**1. 실무 의사결정 시나리오**
- <strong>시나리오 A: 빌드 단계에서 <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a>이 포함되어 환경 이미지를 공통 무법한 상황</strong>
  - **상황**: [Dockerfile](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/067_dockerfile_container_image_build_script/) 내에서 DATABASE_URL을 하드코딩하여, 개발/프로덕션에 다른 이미지를 사용해야 함.
  - **판단**: 이것은 빌드/릴리스/실행 원칙 위반이다. [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)은 빌드가 아닌 릴리스 단계에서 주입되어야 한다. Dockerfile을 수정하여 모든 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)을 제거하고, 런타임에 [환경 변수](/knowledge-base/studynote/02_operating_system/02_process_thread/156_environment_variables/)나 명령행 인자로 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)할 수 있게 해야 한다.

- <strong>시나리오 B: 프로덕션 배포 후 문제 발생 시 빠른 <a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/">롤백</a>이 필요할 때</strong>
  - **상황**: 새 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 배포 직후 예상치 못한 에러가 발생하여 이전 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)으로 빠른 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)이 필요함.
  - **판단**: 빌드/릴리스/실행 원칙이 제대로 적용되어 있으면, [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)은 단순히 이전 릴리스([버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 태그)로 실행 환경만 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)하면 된다. GitOps를 사용하면 이전 태그로 되돌리고 ArgoCD가 자동으로 그것을검출し고 실행을 시작한다.

```text
[빌드/릴리스/실행 원칙 적용 체크리스트]

□ 빌드 단계
  □ 소스 코드가 동일하면 항상 같은 아티팩트 생성 (불변성)
  □ 설정값이 아티팩트에 하드코딩되지 않음
  □ 빌드가 독립적으로 실행됨 (네트워크 상태 등에 영향 없음)

□ 릴리스 단계
  □ 환경별 설정이 명시적으로 관리됨
  □ 각 릴리스가 고유한 버전으로 식별됨
  □ 이전 릴리스를 추적/취소할 수 있음

□ 실행 단계
  □ 동일한 릴리스의 재실행이 동일한 결과를 보장 (멱등성)
  □ 실행 환경이ephemeral (일회용 컨테이너)
  □ graceful shutdown 지원
```

> 📢 **섹션 요약 비유**: 빌드/릴리스/실행 원칙의 부재는"그릇에 음식을 담아 서빙하는 과정에서 요리 단계까지 하는" 것에 비유할 수 있다. 요리(빌드), 플레이팅(릴리스), 서빙(실행)을 한 그릇에서 모두 하면출료문제시 요리가 맛이 없는지, 그릇 선택이 문제인지, 서빙 방법이 문제인지 알 수 없다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

빌드/릴리스/실행 원칙의 올바른 적용은 배포의 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/), 추적 가능성, 그리고 운영 효율성을 크게 향상시킨다.

| 관점 | 단계 혼재 ([AS-IS](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)) | 단계 분리 (TO-BE) | [핵심 성과 지표](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/) |
|:---|:---|:---|:---|
| **추적 가능성** | 어떤 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)+[설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)이 배포되었는지 불분명 | 모든 배포가"[버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)+[설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)" 조합으로 추적 가능 | 배포 이력 100% 투명 |
| <strong><a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/">롤백</a> 속도</strong> | 빌드부터 다시 시작하므로 수십 분 | 이전 릴리스로 즉시 전환 (수초~수분) | [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) 70% 단축 |
| **빌드 재현성** | 환경에 따라 빌드 결과 다름 | 동일한 입력 = 동일한 출력 | 빌드 [신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) 100% |
| <strong>배포 <a href="/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/">신뢰성</a></strong> | [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)이 빌드에 포함되어 오류 발생 가능 | [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)은 런타임에 주입 | 배포 실패율 감소 |

**미래 전망 및 결론**:
빌드/릴리스/실행 원칙은 [Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/), [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) 기술과 결합하여 현대 소프트웨어 배포의 표준이 되었다. 특히 [불변 인프라](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/) 개념과 결합하면, 한번 빌드된 이미지는 결코 변경되지 않고, [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)만 달리하여 여러 환경에 배포되는"[설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) 코드"패턴으로 발전했다.

결론적으로, 빌드/릴리스/실행 원칙은 12팩터 앱의 제5원칙으로, 소프트웨어 배포의 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)과 효율성을 보장하는 기본적인 방법론이다. 이 원칙을 엄격히 준수하면 문제 발생 시 빠른 근본 원인 분석과 빠른 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)이 가능해지며, 궁극적으로 더 안정적인 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 제공과 더 빠른 기능 업데이트가 가능해진다.

> 📢 **섹션 요약 비유**: 빌드/릴리스/실행 원칙은"자동차 제조의 생산라인"과 같다. 공장에서 자동차 본체(빌드)를 만들고, 색상과 옵션을 선택(릴리스)하여 완성된 자동차로 만들고, 고객에게 인도하여 운행(실행)한다. 만약 색상([설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/))에 문제가 있으면 페인트 공정(릴리스)만 다시 하면 되고, 엔진 문제면(빌드) 제조 공정을 다시 해야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>12팩터 앱 (<a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/200_12_factor_app_cloud_native_principles/">12-Factor App</a>)</strong> | 빌드/릴리스/실행 분리가 5번째 원칙으로 명시된 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 방법론 |
| <strong>불변 <a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/">아티팩트</a> (<a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/298_immutable/">Immutable</a> <a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/">Artifact</a>)</strong> | 빌드 단계에서 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)된 후 변경되지 않는 배포 단위 |
| <strong><a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a> 외부화 (Externalized <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">Config</a>)</strong> | 환경별 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)을 [아티팩트](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/) 외부에서 주입하는 릴리스 단계의 핵심 원칙 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/">컨테이너</a> (<a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/194_container_virtualization_docker_namespace/">Container</a>)</strong> | 불변 이미지 기반의 일회용 실행 환경으로 실행 단계를 구현하는 기술 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/">GitOps</a></strong> | 릴리스 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)을 Git으로 선언적 관리하고 자동 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)하는 현대 배포 패턴 |
### 📈 관련 키워드 및 발전 흐름도

```text
[소스 코드 커밋 (Source Code Commit) — 기능 완료 후 버전 관리 저장]
    |
    v
[빌드 (Build) — 코드 컴파일·의존성 번들링, 불변 아티팩트 생성]
    |
    v
[릴리스 (Release) — 환경별 설정 주입, 배포 가능한 단위로 패키징]
    |
    v
[실행 (Run) — 컨테이너 런타임에서 멱등적 프로세스 실행]
    |
    v
[불변 인프라 (Immutable Infrastructure) — 롤백 시 재빌드 없이 이전 릴리스로 즉시 전환]
```

이 흐름은 12팩터 앱 제5원칙인 빌드-릴리스-실행 분리가 [불변 인프라](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/) 패턴으로 발전하는 배포 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인을 나타낸다.

### 👶 어린이를 위한 3줄 비유 설명

1. 빌드는 레고 블록을 조립하는 공장, 릴리스는 색깔과 스티커를 붙이는 포장 단계, 실행은 완성된 장난감을 실제로 갖고 노는 것이에요.
2. 색깔이 마음에 안 들면 공장에서 다시 만들 필요 없이 포장만 바꾸면 되는 것처럼, [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 문제는 릴리스만 바꾸면 된답니다.
3. 이렇게 단계를 딱딱 나눠두면 어디서 문제가 생겼는지 바로 알 수 있어서 더 빠르게 고칠 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 11 / 373

<- **이전**: [10. 백엔드 서비스 (Backing Services) - DB, 큐, 캐시 등을 네트워크로 연결된 자원(Attached Resource)으로](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/010_backend_services/)
**다음**: [12. 무상태 프로세스 (Stateless Processes) - 애플리케이션은 상태를 공유하지 않고 무상태로 실행되며, 상태는 DB](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/012_stateless_processes/) ->

---
