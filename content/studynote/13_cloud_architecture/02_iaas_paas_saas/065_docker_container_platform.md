+++
title = "65. 도커 (Docker) - 컨테이너 기술을 대중화시킨 오픈소스 플랫폼"
date = 2026-04-07

[taxonomies]
tags = ["studynote-cloud"]

[extra]
tags = ["studynote-cloud"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Docker는 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지를 만들고, 배포하고, 실행하는 표준화된 플랫폼이다.
> 2. **가치**: 이미지, [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/), 엔진, 런타임을 연결해 "어디서나 같은 방식으로 실행"을 가능하게 한다.
> 3. **판단**: Docker는 단순한 실행기보다 더 넓은 생태계이며, [OCI](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/333_process/)([Open Container Initiative](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/205_container_image_layer_oci_standard/)) 표준과 함께 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

Docker는 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 기술을 대중화시킨 대표 플랫폼이다. 개발 환경과 운영 환경의 차이를 줄이는 것이 가장 큰 목적이다.

그래서 Docker를 이해하면 이미지, [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/), 런타임, 배포 워크플로를 한 번에 설명할 수 있다.

- **📢 섹션 요약 비유**: 같은 도시락을 어디서든 열어도 같은 맛이 나게 만드는 포장 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
CLI
  ↓
Docker Engine
  ↓
containerd
  ↓
runc
  ↓
Linux Kernel
```

| 구성 요소 | 역할 |
| :-- | :-- |
| [Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) CLI | 사용자 명령 입력 |
| [Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) 엔진 | 전체 제어 |
| containerd | [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 생명주기 관리 |
| [runc](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/667_container_runtime_hw_isolation/) | 실제 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 실행 |
| [Registry](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) | 이미지 저장/배포 |

Docker는 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)의 "사용자 경험"을 표준화한다. 즉, 이미지를 빌드하고, [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)에 올리고, 어디서든 실행하는 흐름을 단순하게 만든다.

- **📢 섹션 요약 비유**: 주문, 포장, 배송, 조리를 한 번에 이어 주는 배달 플랫폼이다.

---

## Ⅲ. 비교 및 연결

| 구분 | Image | [Container](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/194_container_virtualization_docker_namespace/) | [Registry](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) |
| :-- | :-- | :-- | :-- |
| 상태 | 정적 템플릿 | 실행 인스턴스 | 저장소 |
| 역할 | 실행 재료 | 실제 동작 | 배포 공유 |

| 관련 기술 | 의미 |
| :-- | :-- |
| [OCI](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/333_process/) | [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 표준 |
| [Namespace](/knowledge-base/studynote/02_operating_system/01_overview_architecture/061_namespace/) + [cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) | 격리/자원 제한 |
| OverlayFS | 계층형 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 |

[Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) 플랫폼은 이미지 계층과 실행 계층을 분리한다. 이 구조 덕분에 재현성과 확장성이 좋아진다.

- **📢 섹션 요약 비유**: 레시피책, 반찬통, 주방이 분리되어 있으면 어디서든 같은 요리를 만들 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 이미지를 재현 가능하게 빌드하는가?
2. 태그와 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 정책이 있는가?
3. [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) 보안과 접근 통제가 있는가?
4. [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 런타임과 호스트 격리를 이해하는가?
5. 배포와 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 절차가 표준화되어 있는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- latest 태그만 쓰는 설계
- 이미지가 지나치게 큰 설계
- [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 VM처럼 오래 유지하는 설계
- 플랫폼과 런타임을 혼동하는 설계

기술사 관점에서는 Docker를 "[컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 실행 명령"으로만 보면 부족하다. 이미지 생태계와 배포 흐름까지 봐야 플랫폼을 이해한 것이다.

- **📢 섹션 요약 비유**: 도구 하나가 아니라, 포장부터 배달까지 이어지는 시스템이다.

---

## Ⅴ. 기대효과 및 결론

Docker를 활용하면 개발과 운영의 차이를 줄이고, 배포 표준을 통일할 수 있다. 그래서 클라우드 네이티브의 기본 도구가 되었다.

결론적으로 Docker는 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 대중화한 통합 플랫폼이다.

- **📢 섹션 요약 비유**: 상자를 표준 규격으로 만들면 어디서나 쉽게 옮길 수 있다.

---

## 관련 개념 맵

```text
Docker
  ↓
Image / Registry
  ↓
containerd / runc
  ↓
Container Platform
```

---

## 관련 키워드 및 발전 흐름도

```text
컨테이너 기술
  ↓
Docker
  ↓
OCI
  ↓
Container Platform
```

---

## 어린이를 위한 3줄 비유 설명

도커는 도시락을 표준 상자에 담는 시스템이에요.
그 상자는 어디서나 똑같이 열 수 있어요.
그래서 프로그램을 쉽게 옮길 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 64 / 371

← **이전**: [64. cgroups (Control Groups) - 컨테이너가 사용할 수 있는 CPU, 메모리 자원의 상한선을 제한(Limit)하고](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/064_cgroups_control_groups_resource_limit/)
**다음**: [66. 도커 데몬 (Docker Daemon, dockerd) - 컨테이너 라이프사이클 관리 프로세스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/066_docker_daemon_dockerd/) →

---
