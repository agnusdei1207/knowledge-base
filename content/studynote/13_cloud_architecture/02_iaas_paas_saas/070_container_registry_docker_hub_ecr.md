+++
title = "70. 컨테이너 레지스트리 (Container Registry) - 이미지를 저장, 공유, 배포하는 중앙 저장소 (Docker Hub, AWS ECR)"
date = 2026-04-07

[taxonomies]
tags = ["studynote-cloud"]

[extra]
tags = ["studynote-cloud"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)는 [Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) 이미지 같은 산출물을 저장·배포하는 중앙 저장소다.
> 2. **가치**: 이미지 공유, [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리, 배포 자동화를 지원한다.
> 3. **판단**: 공용 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)와 사설 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)의 보안/운영 차이를 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

이미지를 여러 서버에 흩어 놓으면 관리가 어렵다. [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)는 이를 중앙화한다.

그래서 배포 파이프라인의 핵심이 된다.

- **📢 섹션 요약 비유**: 도시락 상자를 모아 두는 냉장 창고다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Build Image
  ↓ push
Registry
  ↓ pull
Deploy
```

| 요소 | 의미 |
| :-- | :-- |
| Repository | 이미지 저장소 |
| Tag | [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 표시 |
| [Authentication](/knowledge-base/studynote/02_operating_system/10_security/604_authentication_factors/) | 접근 제어 |

[레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)는 이미지를 push/pull하는 중심 허브다. 그래서 인증과 권한 관리가 중요하다.

- **📢 섹션 요약 비유**: 상자에 이름표와 자물쇠를 붙여 보관하는 창고다.

---

## Ⅲ. 비교 및 연결

| 구분 | [Docker](/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) [Hub](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/) | AWS ECR |
| :-- | :-- | :-- |
| 성격 | 공용/호스팅 | [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) |
| 보안 | 계정 기반 | [IAM](/knowledge-base/studynote/09_security/11_iam_access_control/526_iam/) 연동 |
| 사용 | 공개 이미지 | 기업용 배포 |

| 관련 개념 | 의미 |
| :-- | :-- |
| Image Tag | [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) |
| Pull [Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) | 가져오기 |

[레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)는 이미지 빌드와 실행 사이의 다리다.

- **📢 섹션 요약 비유**: 만든 상자를 배달하는 중앙 우체국이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 인증과 권한을 제어하는가?
2. 태그 정책이 있는가?
3. 공용/사설을 구분하는가?
4. 취약 이미지 스캔을 하는가?
5. 배포 자동화와 연결되는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- latest만 쓰는 설계
- 무인증 공개 저장소에 민감 이미지를 두는 설계
- 태그 정책이 없는 설계
- [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) 스캔을 안 하는 설계

기술사 관점에서는 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)를 "[컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 배포의 중앙 저장소"로 설명해야 한다.

- **📢 섹션 요약 비유**: 안전하게 맡겨 두는 창고다.

---

## Ⅴ. 기대효과 및 결론

[컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)는 배포 재현성과 운영 효율을 높인다.

결론적으로 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)는 이미지를 저장·공유·배포하는 중앙 저장소다.

- **📢 섹션 요약 비유**: 상자를 모아 두고 필요할 때 꺼내 쓰는 곳이다.

---

## 관련 개념 맵

```text
Image
  ↓ push/pull
Container Registry
  ↓
Deployment
```

---

## 관련 키워드 및 발전 흐름도

```text
Docker Hub
  ↓
Container Registry
  ↓
ECR
  ↓
CI/CD Deployment
```

---

## 어린이를 위한 3줄 비유 설명

상자를 모아 두는 창고예요.  
필요할 때 꺼내서 써요.  
[컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)는 그런 곳이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 69 / 371

← **이전**: [69. 레이어드 파일 시스템 (Layered File System / UnionFS) - 도커 이미지의 핵심. 변경된 레이어(Layer)만](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/069_layered_file_system_unionfs/)
**다음**: [71. OCI (Open Container Initiative) - 컨테이너 이미지 포맷과 런타임에 대한 글로벌 표준 규격 (도커 종속성](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/071_oci_open_container_initiative_standard/) →

---
