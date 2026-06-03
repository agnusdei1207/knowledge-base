---
title: 120. Pod Eviction과 QoS Class (K8s 리소스 관리) - Guaranteed·Burstable·BestEffort
date: '2026-04-19'
tags:
- studynote-cloud-architecture
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: K8s [[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] Class는 Pod의 리소스 요청(requests)·제한(limits) [[009_config|설정]]에 따라 **Guaranteed·Burstable·BestEffort** 3등급으로 자동 분류되며, 노드 리소스 부족 시 **[[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] 등급이 낮은 Pod부터 Eviction(퇴거)**된다.
> 2. **가치**: 노드의 메모리가 부족하면 K8s가 Pod를 강제 종료(OOMKilled)하는데, [[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] Class에 따라 **중요 [[198_pod_kubernetes_minimum_deployment_unit|Pod]](Guaranteed)는 [[571_protection_vs_security|보호]]**하고 **비중요 [[198_pod_kubernetes_minimum_deployment_unit|Pod]](BestEffort)부터 제거**하여 [[090_service_kubernetes_network_load_balancing|서비스]] 안정성을 유지한다.
> 3. **판단 포인트**: `requests == limits`이면 **Guaranteed**, `requests < limits`이면 **Burstable**, [[009_config|설정]] 없으면 **BestEffort**이며, 프로덕션 워크로드는 반드시 **Guaranteed 또는 Burstable(requests 필수)**로 [[009_config|설정]]해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    QoS Class 결정 규칙                                │
├───────────────────────────────────────────────────────┤
│  [Guaranteed] requests == limits (CPU + Memory 모두)  │
│   → 최우선 보호, Eviction 가장 마지막               │
│                                                       │
│  [Burstable] requests < limits (일부만 설정도 포함)   │
│   → 중간 우선순위                                     │
│                                                       │
│  [BestEffort] requests·limits 없음                    │
│   → 최저 우선순위, Eviction 1순위                    │
│                                                       │
│  Eviction 순서: BestEffort → Burstable → Guaranteed  │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] Class는 비행기 좌석 등급이다. 1등석(Guaranteed)은 오버부킹 시에도 [[571_protection_vs_security|보호]]되고, 이코노미(BestEffort)부터 내려야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Eviction 순서

| 순서 | [[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] | 조건 | [[571_protection_vs_security|보호]] 수준 |
|:---|:---|:---|:---|
| **1순위** | BestEffort | requests 없음 | 최저 |
| **2순위** | Burstable | requests 초과 사용 중 | 중간 |
| **3순위** | Guaranteed | requests == limits | **최고** |

### [[009_config|설정]] 예시
```yaml
# Guaranteed: requests == limits
resources:
  requests:
    cpu: 500m
    memory: 256Mi
  limits:
    cpu: 500m
    memory: 256Mi
```

- **📢 섹션 요약 비유**: Guaranteed는 "예약한 만큼만 쓰고 더 안 쓰겠다"는 약속이다. 약속을 지키므로 K8s가 가장 신뢰한다.

---

## Ⅲ. 비교 및 연결

| 비교 | BestEffort | Burstable | Guaranteed |
|:---|:---|:---|:---|
| **requests** | 없음 | 있음 | **== limits** |
| **Eviction** | 1순위 | 2순위 | **마지막** |
| **적합** | 배치·테스트 | 일반 워크로드 | **프로덕션 핵심** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[087_erp_package_advantages_best_practice|Best Practice]]
1. **프로덕션**: Guaranteed (requests == limits).
2. **개발/테스트**: Burstable (requests < limits).
3. **BestEffort**: 절대 프로덕션 금지.
4. LimitRange·ResourceQuota로 [[061_namespace|네임스페이스]] 전체 관리.

---

## Ⅴ. 기대효과 및 결론

| 지표 | [[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] 미설정 | [[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] [[009_config|설정]] | 개선 |
|:---|:---|:---|:---|
| OOMKilled 대상 | 무작위 | **등급순** | 핵심 [[571_protection_vs_security|보호]] |
| 리소스 예측 | 불가 | **requests 기반** | 스케줄링 최적화 |

[[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] Class는 K8s 리소스 관리의 기본이며, [[096_vpa_vertical_pod_autoscaler_kubernetes|VPA]]([[096_vpa_vertical_pod_autoscaler_kubernetes|Vertical Pod Autoscaler]])가 requests/limits를 자동 조정하는 방향으로 진화하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Guaranteed** | requests == limits, 최고 [[571_protection_vs_security|보호]] |
| **Eviction** | 리소스 부족 시 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 강제 종료 |
| **OOMKilled** | 메모리 초과 시 커널이 [[107_process_termination|프로세스 종료]] |
| **LimitRange** | [[061_namespace|네임스페이스]] 기본 requests/limits [[009_config|설정]] |
| **[[096_vpa_vertical_pod_autoscaler_kubernetes|VPA]]** | requests/limits 자동 조정 도구 |

### 📈 관련 키워드 및 발전 흐름도

```text
[K8s 초기 (리소스 미설정, OOMKill 빈발)]
    │
    ▼
[QoS Class 도입 (2016~) — 3등급 Eviction 우선순위]
    │
    ▼
[LimitRange/ResourceQuota (네임스페이스 관리)]
    │
    ▼
[VPA (2019~) — requests/limits 자동 조정]
    │
    ▼
[현재: Karpenter — 노드 자체를 자동 스케일링]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] Class는 비행기 좌석 등급이에요. **1등석(Guaranteed)**은 가장 안전해요.
2. 비행기(노드)가 너무 무거우면 **이코노미(BestEffort) 짐부터 내려요** (Eviction).
3. 중요한 짐(프로덕션 [[198_pod_kubernetes_minimum_deployment_unit|Pod]])은 **1등석에 놓아야** 안전하답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 119 / 371

← **이전**: [[119_kubernetes_declarative_api|119. K8s 선언적 API (Declarative API) - Desired State·Reconciliation Loop]]
**다음**: [[121_monolithic_architecture|121. 모놀리식 아키텍처 (Monolithic Architecture) - 단일체 구조의 특징과 한계]] →

---
