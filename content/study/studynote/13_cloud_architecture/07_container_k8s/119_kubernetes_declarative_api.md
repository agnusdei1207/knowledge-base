+++
weight = 119
title = "119. K8s 선언적 API (Declarative API) - Desired State·Reconciliation Loop"
date = "2026-04-19"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: K8s 선언적 API는 **"무엇을 원하는가([[080_kube_controller_manager_desired_state|Desired State]])"를 YAML로 선언**하면, K8s 컨트롤러가 [[178_as_is_to_be_analysis|현재 상태]]를 Desired State에 **자동으로 수렴시키는(Reconciliation)** 운영 모델이다.
> 2. **가치**: 명령형(Imperative)은 "Pod를 3개 만들어라"(How)이고, 선언적([[219_declarative_yaml|Declarative]])은 "Pod가 3개인 상태를 유지하라"(What)이다. Pod가 죽으면 선언적 모델은 **자동으로 3개를 복원**하지만, 명령형은 수동 개입이 필요하다.
> 3. **판단 포인트**: Reconciliation Loop(관찰→비교→행동)가 K8s 컨트롤러의 핵심이며, Custom Resource + Custom Controller로 **어떤 리소스든 선언적으로 관리**할 수 있다([[565_operator_pattern|Operator Pattern]]).

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    명령형 vs 선언적                                   │
├───────────────────────────────────────────────────────┤
│  [명령형 (Imperative)]                                │
│   kubectl run nginx --image=nginx                     │
│   kubectl scale --replicas=3 deploy/nginx             │
│   → "어떻게(How)"를 지시, 상태 보장 없음             │
│                                                       │
│  [선언적 (Declarative)]                               │
│   apiVersion: apps/v1                                 │
│   kind: Deployment                                    │
│   spec:                                               │
│     replicas: 3                                       │
│   → "무엇(What)"을 선언, K8s가 자동 유지             │
│   Pod 1개 죽으면 → 자동으로 1개 재생성               │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 명령형은 "에어컨을 켜라, 온도를 25도로 맞춰라"(수동)이고, 선언적은 "실내 온도 25도 유지"(자동 항온기)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Reconciliation Loop

| 단계 | 설명 |
|:---|:---|
| **Observe** | [[178_as_is_to_be_analysis|현재 상태]] [[396_validation|확인]] ([[198_pod_kubernetes_minimum_deployment_unit|Pod]] 2개) |
| **Diff** | Desired(3개) vs [[002_current|Current]](2개) = 1개 부족 |
| **Act** | [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 1개 [[087_process_state_transition|생성]] → 3개 달성 |
| **반복** | 무한 루프로 상태 유지 |

### [[565_operator_pattern|Operator Pattern]]
- **Custom Resource (CR)**: 사용자 정의 리소스 (e.g., `PostgreSQL`).
- **Custom Controller**: CR의 Desired State를 Reconcile하는 로직.
- 결과: `kubectl apply -f postgres.yaml`로 **DB 클러스터 자동 [[528_provisioning|프로비저닝]]**.

- **📢 섹션 요약 비유**: Operator는 전문 기술자 로봇이다. "PostgreSQL 3대 클러스터"를 선언하면, 로봇이 설치·[[009_config|설정]]·[[555_backup_and_restore_strategy|백업]]·스케일링을 전부 자동으로 한다.

---

## Ⅲ. 비교 및 연결

| 비교 | 명령형 | 선언적 |
|:---|:---|:---|
| **표현** | How (방법) | **What (목표)** |
| **상태 보장** | 없음 | **자동 복원** |
| **[[119_gitops_single_source_of_truth|GitOps]]** | 불가 | **자연스러운 결합** |
| **[[098_rollback_strategy_pipeline_error_threshold|롤백]]** | 수동 | **git revert → 자동** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 선언적 관리 [[087_erp_package_advantages_best_practice|Best Practice]]
1. 모든 리소스를 YAML로 정의 → Git 관리.
2. `kubectl apply -f` (선언적) 사용, `kubectl create/run` (명령형) 지양.
3. [[091_kustomize_kubernetes_declarative_overlay_manifest|Kustomize]]/Helm으로 환경별 분기.

---

## Ⅴ. 기대효과 및 결론

선언적 API는 K8s의 **철학적 핵심**이며, 이 원칙 덕분에 [[119_gitops_single_source_of_truth|GitOps]]·[[565_operator_pattern_kubernetes_automation|Operator]]·Self-healing이 자연스럽게 구현된다. 모든 [[531_cloud_native_architecture|클라우드 네이티브]] 도구가 이 패러다임을 따른다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[080_kube_controller_manager_desired_state|Desired State]]** | YAML로 선언한 목표 상태 |
| **Reconciliation Loop** | 현재→목표 자동 수렴 |
| **[[565_operator_pattern|Operator Pattern]]** | CR + Controller로 선언적 확장 |
| **[[119_gitops_single_source_of_truth|GitOps]]** | 선언적 [[014_api_posix|API]] 위에 Git 기반 운영 |
| **Self-healing** | Reconciliation의 자동 [[658_ir_recovery|복구]] 효과 |

### 📈 관련 키워드 및 발전 흐름도

```text
[명령형 인프라 관리 (스크립트, 2000s)]
    │
    ▼
[K8s 선언적 API (2014~) — Desired State + Reconciliation]
    │
    ▼
[Custom Resource + Operator (2016~) — 선언적 확장]
    │
    ▼
[GitOps (2017~) — Git + 선언적 API 결합]
    │
    ▼
[현재: Crossplane — 클라우드 리소스까지 선언적 관리]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 명령형은 "에어컨 켜, 온도 25도로 맞춰"라고 **하나하나 지시**하는 거예요.
2. 선언적은 "방 온도 25도 유지해"라고 **목표만 말하면** 항온기(K8s)가 알아서 조절해요.
3. 온도가 올라가면 **자동으로 에어컨을 켜서** 다시 25도로 맞춰주니까 편리하답니다!
