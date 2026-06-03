---
title: 117. 롤링 업데이트 (Rolling Update Deployment) - K8s 기본 무중단 배포 전략
date: '2026-04-19'
tags:
- studynote-software-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 롤링 업데이트는 **구버전 Pod를 하나씩 종료하고 신버전 Pod를 하나씩 [[087_process_state_transition|생성]]**하여, [[090_service_kubernetes_network_load_balancing|서비스]] 중단 없이 점진적으로 전체 인스턴스를 교체하는 **K8s Deployment의 기본 배포 [[268_strategy_pattern|전략]]**이다.
> 2. **가치**: 추가 인프라 없이 기존 리소스 내에서 무중단 배포가 가능하며, `maxSurge`(동시 추가 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 수)와 `maxUnavailable`(동시 제거 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 수)로 교체 속도를 제어한다.
> 3. **판단 포인트**: 롤링 업데이트는 **신·구 [[288_version_ihl_tos_total_length|버전]]이 일시적으로 공존**하므로, [[014_api_posix|API]]·DB 스키마의 **하위 [[344_compatibility_usability|호환성]](Backward [[344_compatibility_usability|Compatibility]])**이 보장되어야 한다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    롤링 업데이트 과정 (Replicas=4)                     │
├───────────────────────────────────────────────────────┤
│  Step 0: [v1][v1][v1][v1]  ← 100% v1                │
│  Step 1: [v1][v1][v1][v2]  ← v2 1개 추가, v1 1개 종료│
│  Step 2: [v1][v1][v2][v2]  ← 50/50                   │
│  Step 3: [v1][v2][v2][v2]                            │
│  Step 4: [v2][v2][v2][v2]  ← 100% v2 완료            │
│                                                       │
│  특징: 신·구 공존 → 하위 호환성 필수!                 │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 놀이공원 관람차의 좌석을 하나씩 교체하는 것이다. 운행([[090_service_kubernetes_network_load_balancing|서비스]])을 멈추지 않고 한 칸씩 새 좌석으로 바꾼다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### K8s 롤링 업데이트 파라미터

| 파라미터 | 설명 | 기본값 |
|:---|:---|:---|
| `maxSurge` | 한 번에 추가 가능한 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 수(%) | 25% |
| `maxUnavailable` | 한 번에 제거 가능한 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 수(%) | 25% |
| `minReadySeconds` | 신규 Pod가 Ready 상태로 유지해야 하는 시간 | 0 |

### Readiness Probe 연동
신규 Pod가 `readinessProbe`를 통과해야만 트래픽을 받으므로, 준비되지 않은 Pod에 요청이 가는 것을 방지한다.

- **📢 섹션 요약 비유**: readinessProbe는 "새 직원이 업무 준비 완료인지 [[396_validation|확인]]"하는 것이다. 준비 안 된 직원에게 고객을 보내지 않는다.

---

## Ⅲ. 비교 및 연결

| 비교 | 롤링 업데이트 | 블루/그린 | [[595_canary_stack_smashing_protector|카나리]] |
|:---|:---|:---|:---|
| **인프라 비용** | **1배** | 2배 | 1+α배 |
| **신·구 공존** | **있음** | 없음 | 있음 |
| **[[098_rollback_strategy_pipeline_error_threshold|롤백]] 속도** | 느림 (역 롤링) | **즉시** | 즉시 |
| **복잡도** | **낮음** | 중간 | 높음 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 하위 [[344_compatibility_usability|호환성]] 보장 방법
1. **[[014_api_posix|API]] [[288_version_ihl_tos_total_length|버전]] 관리**: `/v1`과 `/v2` 동시 제공.
2. **DB Expand and Contract**: 신컬럼 추가(Expand) → 코드 배포 → 구컬럼 삭제(Contract).

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- **breaking change + 롤링 업데이트**: 신버전 API가 구버전과 비호환 → 공존 시간 동안 에러 발생.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 재기동 배포 | 롤링 업데이트 | 개선 |
|:---|:---|:---|:---|
| 다운타임 | 분~시간 | **0** | 무중단 |
| 추가 인프라 | 불필요 | **불필요** | 비용 0 |
| [[098_rollback_strategy_pipeline_error_threshold|롤백]] | 수동 재배포 | 역 롤링 | 자동화 |

롤링 업데이트는 K8s의 기본 [[268_strategy_pattern|전략]]이며, 더 정밀한 제어가 필요하면 [[595_canary_stack_smashing_protector|카나리]]·블루/그린으로 확장한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **K8s [[087_deployment_kubernetes_workload_rolling_update|Deployment]]** | 롤링 업데이트의 기본 배포 [[268_strategy_pattern|전략]] |
| **maxSurge / maxUnavailable** | 교체 속도 제어 파라미터 |
| **readinessProbe** | 준비되지 않은 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 트래픽 차단 |
| **블루/그린** | 공존 없는 대안 배포 [[268_strategy_pattern|전략]] |
| **[[595_canary_stack_smashing_protector|카나리]]** | 트래픽 비율 제어 대안 |

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 재기동 배포 (다운타임 발생)]
    │
    ▼
[롤링 업데이트 (K8s 기본, 2014~) — 무중단, 순차 교체]
    │
    ▼
[블루/그린 (2010s) — 100% 전환, 즉시 롤백]
    │
    ▼
[카나리 (2015~) — 1%→100% 점진 확대]
    │
    ▼
[현재: Progressive Delivery — 롤링+카나리+ACA 통합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 롤링 업데이트는 놀이공원 관람차의 **좌석을 하나씩 새 것으로 바꾸는** 거예요.
2. 관람차([[090_service_kubernetes_network_load_balancing|서비스]])는 **멈추지 않고 계속 돌아가면서** 한 칸씩 교체해요.
3. 단, 새 좌석과 옛 좌석이 **잠깐 같이 있으니까**, 둘 다 잘 맞아야([[344_compatibility_usability|호환성]]) 해요!
