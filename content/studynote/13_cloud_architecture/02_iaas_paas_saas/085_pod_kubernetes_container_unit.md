---
title: 85. Pod (파드) - K8s의 최소 배포 및 스케일링 단위
date: '2026-04-10'
tags:
- studynote-cloud-architecture
---

## 핵심 인사이트 (3줄 요약)

> **본질**: Pod는 [[205_kubernetes_container_orchestration|Kubernetes]] (K8s)에서 [[208_schedule_history_transaction_execution_order|스케줄]]링·배포되는 가장 작은 단위이며, 하나 이상의 [[561_container_based_deployment|컨테이너]]를 묶어 같은 네트워크와 저장소를 공유하게 만든다.
> **가치**: [[561_container_based_deployment|컨테이너]]는 실행 단위이고, Pod는 운영 단위다. 이 차이를 알아야 [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]]([[546_sidecar_proxy_pattern|Sidecar]]), 초기화 [[561_container_based_deployment|컨테이너]], 공유 볼륨을 올바르게 설계할 수 있다.
> **판단 포인트**: 서로 강하게 결합된 프로세스만 한 Pod에 넣고, 느슨한 [[090_service_kubernetes_network_load_balancing|서비스]]는 분리해야 Pod가 "작은 [[598_vm_migration_nic|VM]]"으로 오해되지 않는다.

---

## Ⅰ. 개요 및 필요성

Pod는 Kubernetes에서 [[561_container_based_deployment|컨테이너]]를 함께 묶어 배치하는 최소 단위다. 각 [[561_container_based_deployment|컨테이너]]는 별도 프로세스지만, [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 안에서는 같은 IP (Internet [[295_protocol_field_tcp_udp_icmp|Protocol]]) 주소, 네트워크 [[061_namespace|네임스페이스]], 볼륨을 공유한다.

이 구조가 필요한 이유는 "한 프로세스 한 [[561_container_based_deployment|컨테이너]]"만으로는 부족하기 때문이다. [[568_logs_distributed_logging_elk_fluentd|로그]] 수집기, [[264_proxy_pattern_surrogate_access_control|프록시]], 보조 작업자처럼 같은 생명주기를 공유해야 하는 프로세스를 함께 배치하면, 배포와 복구를 더 단순하게 만들 수 있다.

- 📢 섹션 요약 비유: 같은 주소의 룸메이트

---

## Ⅱ. 아키텍처 및 핵심 원리

Pod는 보통 애플리케이션 [[561_container_based_deployment|컨테이너]], [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] [[561_container_based_deployment|컨테이너]], 초기화 [[561_container_based_deployment|컨테이너]], 공유 볼륨으로 구성된다. 네트워크는 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 수준에서 하나로 보이기 때문에 [[561_container_based_deployment|컨테이너]]끼리 localhost로 통신할 수 있고, 저장소는 볼륨을 통해 함께 본다.

```text
Pod
├─ app container
├─ sidecar container
├─ init container
└─ shared volume / shared IP
```

| 구성 요소 | 역할 |
| --- | --- |
| App [[194_container_virtualization_docker_namespace|Container]] | 핵심 [[090_service_kubernetes_network_load_balancing|서비스]] 실행 |
| [[546_sidecar_proxy_pattern|Sidecar]] | [[568_logs_distributed_logging_elk_fluentd|로그]], [[264_proxy_pattern_surrogate_access_control|프록시]], 보조 기능 |
| Init [[194_container_virtualization_docker_namespace|Container]] | 시작 전 준비 작업 |
| Shared [[001_bigdata_3v_5v|Volume]] | [[561_container_based_deployment|컨테이너]] 간 [[501_file_definition_logical_record|파일]] 공유 |

핵심은 Pod가 [[561_container_based_deployment|컨테이너]]를 "더 크게 만드는 것"이 아니라, 같은 생명주기를 묶는 운영 경계라는 점이다.

- 📢 섹션 요약 비유: 같이 시작하고 같이 끝난다

---

## Ⅲ. 비교 및 연결

[[561_container_based_deployment|컨테이너]]는 애플리케이션 패키징 단위이고, Pod는 그 패키지를 함께 운영하는 [[208_schedule_history_transaction_execution_order|스케줄]]링 단위다. Deployment는 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 복제와 롤링 업데이트를 담당하고, Node는 Pod가 실제로 올라가는 물리/가상 머신이다. 따라서 Pod를 이해해야 Deployment와 Service의 역할도 정확히 보인다.

| 비교 대상 | 차이점 |
| --- | --- |
| [[194_container_virtualization_docker_namespace|Container]] | 프로세스 실행 단위 |
| [[198_pod_kubernetes_minimum_deployment_unit|Pod]] | 네트워크/볼륨을 공유하는 배포 단위 |
| [[087_deployment_kubernetes_workload_rolling_update|Deployment]] | [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 개수와 업데이트 [[268_strategy_pattern|전략]] 관리 |
| Node | Pod가 배치되는 인프라 자원 |
| [[598_vm_migration_nic|VM]] | 더 무거운 [[015_virtualization|가상화]] 경계 |

즉 Pod는 [[561_container_based_deployment|컨테이너]]의 상위 포장재가 아니라, "같이 죽고 같이 살아야 하는 프로세스 묶음"이다.

- 📢 섹션 요약 비유: 포장 상자와 배달 박스

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 같은 네트워크와 볼륨을 공유해야 하는 [[561_container_based_deployment|컨테이너]]만 하나의 Pod에 넣는다. 예를 들어 애플리케이션과 [[264_proxy_pattern_surrogate_access_control|프록시]], [[568_logs_distributed_logging_elk_fluentd|로그]] 수집기는 함께 둘 수 있지만, 서로 독립적으로 확장해야 하는 [[090_service_kubernetes_network_load_balancing|서비스]]는 분리하는 편이 좋다. 또 readiness/liveness probe를 제대로 두지 않으면 Pod가 살아 있어도 [[090_service_kubernetes_network_load_balancing|서비스]]는 죽어 보일 수 있다.

### [[435_checklist_based_testing|체크리스트]]
1. [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 안의 [[561_container_based_deployment|컨테이너]]가 같은 생명주기를 공유하는가?
2. 상태를 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 로컬 [[501_file_definition_logical_record|파일]]시스템에만 저장하고 있지 않은가?
3. Probe 설정으로 실제 [[090_service_kubernetes_network_load_balancing|서비스]] 준비 상태를 판별하는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- 서로 독립적인 [[090_service_kubernetes_network_load_balancing|서비스]]를 하나의 Pod에 넣는 것
- [[198_pod_kubernetes_minimum_deployment_unit|Pod]] IP가 영구적이라고 가정하는 것
- 재시작 시 사라질 데이터를 로컬 디스크에만 두는 것

- 📢 섹션 요약 비유: 같은 보트에 탈 사람만 태우기

---

## Ⅴ. 기대효과 및 결론

[[198_pod_kubernetes_minimum_deployment_unit|Pod]] 개념을 제대로 쓰면 배포와 복구가 간단해지고, [[561_container_based_deployment|컨테이너]] 간 공통 자원을 명확히 관리할 수 있다. 반대로 Pod를 너무 크게 쓰면 확장성과 장애 격리가 떨어진다. 그래서 Pod는 "작은 [[598_vm_migration_nic|VM]]"이 아니라 "같이 움직여야 하는 [[561_container_based_deployment|컨테이너]] 묶음"으로 기억하는 것이 맞다.

결론적으로 Pod는 [[205_kubernetes_container_orchestration|Kubernetes]] 운영의 기본 벽돌이다. 이 벽돌을 잘 쌓아야 [[087_deployment_kubernetes_workload_rolling_update|Deployment]], [[090_service_kubernetes_network_load_balancing|Service]], [[095_hpa_horizontal_pod_autoscaler_kubernetes|HPA]] 같은 상위 제어가 의미를 가진다.

- 📢 섹션 요약 비유: 한 방에 묶은 룸메이트

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| --- | --- |
| [[205_kubernetes_container_orchestration|Kubernetes]] (K8s) | Pod를 관리하는 [[073_container_orchestration_tools|오케스트레이션]] 플랫폼 |
| [[198_pod_kubernetes_minimum_deployment_unit|Pod]] | 최소 배포/[[208_schedule_history_transaction_execution_order|스케줄]] 단위 |
| [[194_container_virtualization_docker_namespace|Container]] | 실제 애플리케이션 프로세스 |
| [[087_deployment_kubernetes_workload_rolling_update|Deployment]] | [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 복제와 업데이트 관리 |
| Node | Pod가 올라가는 실행 자원 |
| Probe | [[090_service_kubernetes_network_load_balancing|서비스]] 준비 상태 [[396_validation|확인]] |

### 📈 관련 키워드 및 발전 흐름도

```text
Container Image
   ↓
Pod 생성
   ↓
같은 IP / 볼륨 공유
   ↓
Node에 스케줄링
   ↓
Deployment가 복제 및 롤링 업데이트
```

### 👶 어린이를 위한 3줄 비유 설명

1. Pod는 같은 집에 사는 가족처럼 주소를 같이 쓰는 상자예요.
2. 방은 여러 개일 수 있지만 우편함은 하나예요.
3. 그래서 같이 움직여야 하는 친구들만 한 집에 살아요.
