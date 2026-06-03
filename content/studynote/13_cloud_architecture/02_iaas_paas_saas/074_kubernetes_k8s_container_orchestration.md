---
title: 74. 쿠버네티스 (Kubernetes, K8s) - 컨테이너 오케스트레이션 플랫폼
date: '2026-04-07'
tags:
- studynote-cloud
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 쿠버네티스는 [[561_container_based_deployment|컨테이너]]를 배치하고 운영하는 [[073_container_orchestration_tools|오케스트레이션]] 플랫폼이다.
> 2. **가치**: 자동 [[658_ir_recovery|복구]], 확장, [[090_service_kubernetes_network_load_balancing|서비스]] 관리가 가능하다.
> 3. **판단**: [[198_pod_kubernetes_minimum_deployment_unit|Pod]], [[090_service_kubernetes_network_load_balancing|Service]], Deployment의 관계를 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

[[561_container_based_deployment|컨테이너]]가 많아지면 운영이 어려워진다.

쿠버네티스는 이를 자동화한다.

- **📢 섹션 요약 비유**: 수많은 방을 한꺼번에 관리하는 아파트 관리사무소다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Pod
  ↓ Service
  ↓ Deployment
  ↓ Cluster
```

| 구성 | 의미 |
| :-- | :-- |
| [[198_pod_kubernetes_minimum_deployment_unit|Pod]] | 실행 단위 |
| [[090_service_kubernetes_network_load_balancing|Service]] | 접근점 |
| [[087_deployment_kubernetes_workload_rolling_update|Deployment]] | 배포 관리 |

쿠버네티스는 [[561_container_based_deployment|컨테이너]] 생명주기를 자동으로 관리한다.

- **📢 섹션 요약 비유**: 방 배정, 주소, 증축을 자동으로 관리하는 것이다.

---

## Ⅲ. 비교 및 연결

| 개념 | 의미 |
| :-- | :-- |
| K8s | [[073_container_orchestration_tools|오케스트레이션]] |
| [[063_docker_architecture|Docker]] | [[561_container_based_deployment|컨테이너]] 도구 |
| Runtime | 실제 실행 |

| 기능 | 설명 |
| :-- | :-- |
| Self-healing | 자동 [[658_ir_recovery|복구]] |
| Autoscaling | 자동 확장 |

쿠버네티스는 런타임 위에서 [[561_container_based_deployment|컨테이너]]를 체계적으로 운영한다.

- **📢 섹션 요약 비유**: 건물을 자동으로 관리하는 똑똑한 관리자다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. [[198_pod_kubernetes_minimum_deployment_unit|Pod]]/[[090_service_kubernetes_network_load_balancing|Service]]/Deployment를 구분하는가?
2. 자동 [[658_ir_recovery|복구]]/확장을 아는가?
3. 클러스터 개념을 아는가?
4. [[090_service_kubernetes_network_load_balancing|서비스]] 디스커버리를 이해하는가?
5. 런타임과의 계층을 구분하는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 쿠버네티스를 단순 배포 도구로 보는 설계
- Pod와 [[561_container_based_deployment|컨테이너]]를 혼동하는 설계
- Service와 Deployment를 헷갈리는 설계
- 클러스터 운영을 수동으로만 하는 설계

기술사 관점에서는 K8s를 "[[561_container_based_deployment|컨테이너]] 운영의 표준 [[073_container_orchestration_tools|오케스트레이션]] 플랫폼"으로 설명해야 한다.

- **📢 섹션 요약 비유**: 방과 복도와 관리 규칙을 한 번에 정리한다.

---

## Ⅴ. 기대효과 및 결론

쿠버네티스는 대규모 [[561_container_based_deployment|컨테이너]] 운영을 가능하게 한다.

결론적으로 Kubernetes는 [[205_kubernetes_container_orchestration|컨테이너 오케스트레이션]] 플랫폼이다.

- **📢 섹션 요약 비유**: [[561_container_based_deployment|컨테이너]] 아파트를 운영하는 시스템이다.

---

## 관련 개념 맵

```text
Pod
  ↓
Service
  ↓
Deployment
```

---

## 관련 키워드 및 발전 흐름도

```text
Container Runtime
  ↓
Kubernetes
  ↓
Orchestration Platform
```

---

## 어린이를 위한 3줄 비유 설명

방을 나눠서 관리해요.  
문도 자동으로 연결해요.  
쿠버네티스는 그런 도구예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 73 / 371

← **이전**: [[073_container_orchestration_tools|73. 오케스트레이션 (Orchestration) 도구 - 수백~수만 개의 컨테이너를 자동 배치, 스케일링, 로드밸런싱, 장애 복구(Self-healing)하는]]
**다음**: [[075_kubernetes_k8s_cluster_architecture|75. K8s 클러스터 아키텍처 - 1개 이상의 컨트롤 플레인(마스터 노드)과 여러 개의 데이터 플레인(워커 노드)으로 구성]] →

---
