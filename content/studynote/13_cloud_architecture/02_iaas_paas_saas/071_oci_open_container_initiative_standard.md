+++
title = "71. OCI (Open Container Initiative) - 컨테이너 이미지 포맷과 런타임에 대한 글로벌 표준 규격 (도커 종속성 탈피 목적)"
date = 2026-04-07

[taxonomies]
tags = ["studynote-cloud"]

[extra]
tags = ["studynote-cloud"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: OCI는 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지와 런타임의 표준 규격을 정의한 개방형 프로젝트다.
> 2. **가치**: 벤더 종속성을 줄이고 서로 다른 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 도구 간 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)을 높인다.
> 3. **판단**: 이미지 포맷과 런타임 표준을 구분해서 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

[컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)가 널리 쓰이면서 한 회사의 방식에만 묶이지 않는 표준이 필요해졌다.

OCI는 그 표준을 제공한다.

- **📢 섹션 요약 비유**: 서로 다른 자물쇠도 맞게 하려는 공통 규격이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Image Spec
  v
Runtime Spec
  v
OCI
```

| 요소 | 의미 |
| :-- | :-- |
| Image [Specification](/knowledge-base/studynote/04_software_engineering/03_design_architecture/148_requirements_specification_formal_informal/) | 이미지 포맷 |
| Runtime [Specification](/knowledge-base/studynote/04_software_engineering/03_design_architecture/148_requirements_specification_formal_informal/) | 실행 규격 |
| Standardization | [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) |

OCI는 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지와 실행 환경의 공통 규격을 정해 도구 간 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)을 높인다.

- **📢 섹션 요약 비유**: 모두 같은 규격의 상자와 문을 쓰게 만드는 것이다.

---

## Ⅲ. 비교 및 연결

| 개념 | 역할 | 차이 |
| :-- | :-- | :-- |
| [Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) | 구현체 | 도구 |
| [OCI](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/333_process/) | 표준 | 규격 |
| Runtime | 실행 | 실제 동작 |

| 효과 | 의미 |
| :-- | :-- |
| Portability | 이식성 |
| [Interoperability](/knowledge-base/studynote/06_ict_convergence/01_blockchain/084_blockchain_interoperability_polkadot_cosmos/) | 상호 운용 |

[OCI](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/333_process/) 덕분에 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 생태계는 특정 도구에만 묶이지 않게 되었다.

- **📢 섹션 요약 비유**: 상자 규격이 같으면 운송회사가 달라도 옮길 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 이미지와 런타임 표준을 구분하는가?
2. 도구 종속성을 줄이는가?
3. [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)을 고려하는가?
4. 배포/실행 환경을 일치시키는가?
5. [OCI](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/333_process/) 기반인지 확인하는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- Docker와 OCI를 혼동하는 설계
- 표준보다 특정 도구만 보는 설계
- [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 없이 배포하는 설계
- 이미지/런타임 구분이 없는 설계

기술사 관점에서는 OCI를 "[컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 생태계의 공통 표준"으로 설명해야 한다.

- **📢 섹션 요약 비유**: 다른 공장에서 만든 상자도 같은 문으로 지나가게 한다.

---

## Ⅴ. 기대효과 및 결론

OCI는 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 기술의 상호 운용성과 이식성을 높인다.

결론적으로 OCI는 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지와 런타임의 표준 규격이다.

- **📢 섹션 요약 비유**: 공통 규격이 있어야 모두 함께 쓸 수 있다.

---

## 관련 개념 맵

```text
OCI
  v
Image Spec
  v
Runtime Spec
  v
Container Portability
```

---

## 관련 키워드 및 발전 흐름도

```text
Docker
  v
OCI
  v
Open Standard
  v
Interoperability
```

---

## 어린이를 위한 3줄 비유 설명

모두 같은 규격을 써요.
그래야 서로 잘 맞아요.
OCI는 그런 약속이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 70 / 371

<- **이전**: [70. 컨테이너 레지스트리 (Container Registry) - 이미지를 저장, 공유, 배포하는 중앙 저장소 (Docker Hub,](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/070_container_registry_docker_hub_ecr/)
**다음**: [72. 컨테이너 런타임 (Container Runtime) - 실제 컨테이너를 구동하는 저수준 엔진 (containerd, CRI-O,](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/072_container_runtime_containerd_crio_runc/) ->

---
