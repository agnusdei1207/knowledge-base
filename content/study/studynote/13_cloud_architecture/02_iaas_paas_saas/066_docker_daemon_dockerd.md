+++
weight = 66
title = "66. 도커 데몬 (Docker Daemon, dockerd) - 컨테이너 라이프사이클 관리 프로세스"
date = "2026-04-07"
[extra]
categories = "studynote-cloud"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: dockerd는 [[063_docker_architecture|Docker]] API를 받아 이미지, [[561_container_based_deployment|컨테이너]], 네트워크, 볼륨을 관리하는 백그라운드 데몬이다.
> 2. **가치**: CLI와 실제 실행 계층을 분리해 [[561_container_based_deployment|컨테이너]] 라이프사이클을 일관되게 제어한다.
> 3. **판단**: dockerd를 이해하면 [[063_docker_architecture|Docker]] 플랫폼의 실행 흐름과 장애 지점을 더 정확히 볼 수 있다.

---

## Ⅰ. 개요 및 필요성

Docker에서 사용자가 명령을 입력하면 그 뒤에서 실제로 처리하는 주체가 dockerd다.

즉, dockerd는 [[063_docker_architecture|Docker]] 생태계의 중앙 제어실이다.

- **📢 섹션 요약 비유**: 음식 주문을 받으면 주방과 배달을 모두 조율하는 매니저다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
CLI / API
  ↓
dockerd
  ↓
containerd
  ↓
runc
  ↓
Linux Kernel
```

| 구성 요소 | 역할 |
| :-- | :-- |
| dockerd | [[063_docker_architecture|Docker]] [[014_api_posix|API]] 처리 및 [[073_container_orchestration_tools|오케스트레이션]] |
| containerd | [[561_container_based_deployment|컨테이너]] 수명주기 관리 |
| [[667_container_runtime_hw_isolation|runc]] | 실제 실행 |
| [[235_registry_immutable_tag|Registry]] | 이미지 저장 |

dockerd는 이미지 pull, build, run, stop, [[197_rm_rate_monotonic_scheduling|rm]] 같은 작업을 하나의 [[164_policy|정책]] 아래 조정한다. 그래서 [[561_container_based_deployment|컨테이너]] 관리가 표준화된다.

- **📢 섹션 요약 비유**: 배달 접수, 조리 지시, 상태 확인을 모두 맡는 본부다.

---

## Ⅲ. 비교 및 연결

| 구분 | dockerd | containerd | [[667_container_runtime_hw_isolation|runc]] |
| :-- | :-- | :-- | :-- |
| 역할 | 상위 제어 | [[561_container_based_deployment|컨테이너]] 관리 | 실행 |
| 범위 | 플랫폼 | 런타임 관리 | [[104_process_creation|프로세스 생성]] |

| 관련 기능 | 설명 |
| :-- | :-- |
| Image Build | 이미지 [[087_process_state_transition|생성]] |
| Network | 네트워크 [[009_config|설정]] |
| [[001_bigdata_3v_5v|Volume]] | 스토리지 관리 |
| [[526_security_logging_and_monitoring_failures|Logging]] | 상태/이벤트 추적 |

dockerd는 단순 실행기가 아니라 Docker의 제어면(control plane)이다. 문제를 볼 때는 [[014_api_posix|API]], daemon, runtime을 분리해야 한다.

- **📢 섹션 요약 비유**: 지휘자, 무대 매니저, 실제 연주자가 각각 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. dockerd와 containerd의 역할을 구분하는가?
2. API와 데몬의 경계를 이해하는가?
3. [[561_container_based_deployment|컨테이너]] [[087_process_state_transition|생성]]/삭제 흐름을 설명할 수 있는가?
4. 로그와 네트워크/볼륨 이슈를 찾을 수 있는가?
5. 장애 시 어느 계층을 먼저 보는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- dockerd를 [[561_container_based_deployment|컨테이너]] 자체로 보는 설계
- CLI 문제와 데몬 문제를 섞는 설계
- runtime과 control plane을 구분하지 않는 설계
- 이미지/네트워크/볼륨 상태를 무시하는 설계

기술사 관점에서는 dockerd를 "Docker의 엔진 제어 계층"으로 설명해야 한다.

- **📢 섹션 요약 비유**: 주방의 불, 재료, 조리 순서를 한꺼번에 관리하는 본부다.

---

## Ⅴ. 기대효과 및 결론

dockerd를 이해하면 [[063_docker_architecture|Docker]] 관련 장애 원인과 제어 흐름을 더 정확히 추적할 수 있다.

결론적으로 dockerd는 [[063_docker_architecture|Docker]] 플랫폼의 중앙 데몬이다.

- **📢 섹션 요약 비유**: 접수창구가 있어야 일이 잘 돌아간다.

---

## 관련 개념 맵

```text
Docker CLI
  ↓
dockerd
  ↓
containerd / runc
  ↓
Container Lifecycle
```

---

## 관련 키워드 및 발전 흐름도

```text
Docker Platform
  ↓
dockerd
  ↓
containerd
  ↓
Runtime Control
```

---

## 어린이를 위한 3줄 비유 설명

주문을 받는 본부가 있어야 일이 시작돼요.  
[[063_docker_architecture|도커]] 데몬이 그 본부예요.  
그래서 [[561_container_based_deployment|컨테이너]]를 만들고 멈추는 일을 관리해요.
