---
title: "containerd, CRI-O, runc"
tags:
  - "cloud_architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 런타임은 이미지를 실제 프로세스로 실행하는 저수준 엔진이다.
> 2. **가치**: containerd, CRI-O, [runc](/studynote/01_computer_architecture/15_advanced_topics/667_container_runtime_hw_isolation/) 같은 런타임이 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 생명주기를 담당한다.
> 3. **판단**: 오케스트레이터와 런타임의 역할을 구분해야 한다.

---

## Ⅰ. 개요 및 필요성

이미지를 저장하는 것과 실제로 실행하는 것은 다르다. 런타임이 실행을 맡는다.

그래서 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 생태계에서 중요하다.

- **📢 섹션 요약 비유**: 상자를 열어 실제로 움직이게 하는 기계다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Image
  v runtime
Container Process
```

| 요소 | 의미 |
| :-- | :-- |
| [runc](/studynote/01_computer_architecture/15_advanced_topics/667_container_runtime_hw_isolation/) | [OCI](/studynote/13_cloud_architecture/05_data_engineering/333_process/) 런타임 |
| containerd | 상위 관리 |
| CRI-O | K8s 친화 런타임 |

런타임은 [프로세스 생성](/studynote/02_operating_system/02_process_thread/104_process_creation/), 격리, [cgroups](/studynote/02_operating_system/01_overview_architecture/062_cgroups/), namespaces를 통해 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 실제로 구동한다.

- **📢 섹션 요약 비유**: 그림 속 자동차를 실제 도로에 올리는 것이다.

---

## Ⅲ. 비교 및 연결

| 구분 | containerd | CRI-O | [runc](/studynote/01_computer_architecture/15_advanced_topics/667_container_runtime_hw_isolation/) |
| :-- | :-- | :-- | :-- |
| 역할 | 상위 관리 | K8s 연동 | 실행 |
| 범위 | 넓음 | 좁음 | 가장 하위 |

| 연결 | 의미 |
| :-- | :-- |
| [OCI](/studynote/13_cloud_architecture/05_data_engineering/333_process/) | 표준 |
| [Kubelet](/studynote/13_cloud_architecture/02_iaas_paas_saas/082_kubelet_node_agent/) | 관리 |

런타임은 오케스트레이션과 달리 실제 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 실행을 담당한다.

- **📢 섹션 요약 비유**: 지휘자와 연주자를 구분하는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 런타임과 오케스트레이터를 구분하는가?
2. [OCI](/studynote/13_cloud_architecture/05_data_engineering/333_process/) 표준을 따르는가?
3. 격리 메커니즘을 아는가?
4. containerd/CRI-O/[runc](/studynote/01_computer_architecture/15_advanced_topics/667_container_runtime_hw_isolation/) 차이를 아는가?
5. 보안과 자원 제어를 고려하는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 런타임과 이미지 저장소를 혼동하는 설계
- 오케스트레이터가 직접 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 실행한다고 오해하는 설계
- 표준을 무시하는 설계
- 자원 격리를 무시하는 설계

기술사 관점에서는 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 런타임을 "실행 계층의 저수준 엔진"으로 설명해야 한다.

- **📢 섹션 요약 비유**: 자동차 엔진과 운전대는 다르다.

---

## Ⅴ. 기대효과 및 결론

런타임은 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)의 실행과 격리를 담당한다.

결론적으로 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 런타임은 실제 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 구동하는 엔진이다.

- **📢 섹션 요약 비유**: 이미지를 진짜 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)로 움직이게 한다.

---

## 관련 개념 맵

```text
Image
  v
Runtime
  v
Container
  v
Kubernetes
```

---

## 관련 키워드 및 발전 흐름도

```text
OCI
  v
containerd / CRI-O / runc
  v
Runtime
  v
Container Execution
```

---

## 어린이를 위한 3줄 비유 설명

그림을 실제로 움직여요.
그 일을 하는 엔진이에요.
런타임은 그런 도구예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 71 / 371

<- **이전**: [71. OCI (Open Container Initiative) - 컨테이너 이미지 포맷과 런타임에 대한 글로벌 표준 규격 (도커 종속성](/studynote/13_cloud_architecture/02_iaas_paas_saas/071_oci_open_container_initiative_standard/)
**다음**: [73. 오케스트레이션 (Orchestration) 도구 - 수백~수만 개의 컨테이너를 자동 배치, 스케일링, 로드밸런싱, 장애 복구(Self-healing)하는](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) ->

---
