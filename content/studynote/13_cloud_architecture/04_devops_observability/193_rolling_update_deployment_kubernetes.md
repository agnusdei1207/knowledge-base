---
title: 193. 롤링 배포 (Rolling Update Deployment)
date: '2026-04-21'
tags:
- studynote-cloud-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 구버전 인스턴스를 하나씩 끄고 신버전을 하나씩 켜면서 트래픽을 점진적으로 이전하는 가장 보편적인 [[082_zero_downtime_deployment_rolling_blue_green_canary|무중단 배포]] 방식이다.
> 2. **가치**: 추가 인프라 비용 없이 [[082_zero_downtime_deployment_rolling_blue_green_canary|무중단 배포]]를 구현할 수 있으나, 배포 중 구/신 [[288_version_ihl_tos_total_length|버전]]이 공존하는 혼재 기간이 반드시 존재한다.
> 3. **판단 포인트**: `maxSurge`(최대 추가 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 수)와 `maxUnavailable`(최대 불가 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 수)의 조합으로 속도와 [[452_availability|가용성]]의 트레이드오프를 조절한다.

---

## Ⅰ. 개요 및 필요성

[[117_rolling_update_deployment|롤링 업데이트]]([[083_rolling_update_deployment_zero_downtime_version_inconsistency|Rolling Update]])는 [[205_kubernetes_container_orchestration|Kubernetes]] Deployment의 기본 배포 [[268_strategy_pattern|전략]]으로, 전체 [[090_service_kubernetes_network_load_balancing|서비스]]를 중단하지 않고 인스턴스를 순차적으로 교체한다. 롤링이라는 이름은 파도처럼 점진적으로 변경이 흘러가는 모습에서 유래했다.

가장 큰 장점은 **추가 인프라 비용이 거의 없다**는 점이다. 10개의 Pod을 운영하는 [[090_service_kubernetes_network_load_balancing|서비스]]라면, 동시에 최대 `maxSurge`개의 신버전 Pod만 추가 [[087_process_state_transition|생성]]되므로 자원 효율이 높다. 또한 K8s Deployment가 기본으로 지원하므로 별도 구성 없이 사용 가능하다.

단점은 배포 중 **구버전(v1)과 신버전(v2)이 동시에 트래픽을 처리**한다는 것이다. [[014_api_posix|API]] 응답 형식이 [[288_version_ihl_tos_total_length|버전]] 간 호환되지 않는다면 클라이언트가 [[288_version_ihl_tos_total_length|버전]]에 따라 다른 응답을 받아 예기치 못한 오류가 발생한다. DB [[005_schema|스키마]]가 변경된 경우라면 구버전 코드가 새 [[005_schema|스키마]]를 처리하지 못하거나, 신버전 코드가 구 [[005_schema|스키마]] 데이터를 잘못 해석할 수 있다.

📢 **섹션 요약 비유**: [[117_rolling_update_deployment|롤링 업데이트]]는 마치 고속도로의 차선 개보수 공사와 같다. 전체 차선을 한꺼번에 막지 않고 한 차선씩 막아 작업하면서 나머지 차선으로 차량이 계속 통행하도록 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### K8s [[117_rolling_update_deployment|롤링 업데이트]] 핵심 파라미터

| 파라미터 | 설명 | 기본값 |
|:---|:---|:---:|
| `maxSurge` | 원하는 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 수 초과 [[087_process_state_transition|생성]] 허용 최대치 (절대값 또는 %) | 25% |
| `maxUnavailable` | 업데이트 중 [[090_service_kubernetes_network_load_balancing|서비스]] 불가 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 최대 허용 수 | 25% |
| `minReadySeconds` | 새 Pod가 준비 완료로 간주되기 전 최소 대기 시간(초) | 0 |
| `progressDeadlineSeconds` | 배포 [[216_progress_in_synchronization|진행]] [[573_timeout_retry_backoff_strategy|타임아웃]] (초과 시 실패 처리) | 600 |

### 배포 단계 흐름

```
초기 상태 (v1 x4):
  [v1] [v1] [v1] [v1]    총 4개 Pod

maxSurge=1, maxUnavailable=1 설정 시:

단계 1: v2 1개 생성 → [v1][v1][v1][v1][v2]  (5개)
단계 2: v1 1개 종료 → [v1][v1][v1][v2]      (4개)
단계 3: v2 1개 생성 → [v1][v1][v1][v2][v2]  (5개)
단계 4: v1 1개 종료 → [v1][v1][v2][v2]      (4개)
  ... 반복 ...
완료: [v2] [v2] [v2] [v2]    총 4개 Pod
```

### K8s [[087_deployment_kubernetes_workload_rolling_update|Deployment]] YAML

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1          # 최대 5개까지 허용 (4+1)
      maxUnavailable: 0    # 서비스 불가 Pod 0개 (고가용성 우선)
  template:
    spec:
      containers:
      - name: my-app
        image: my-app:v2
        readinessProbe:    # 준비 완료 확인 후 트래픽 수신
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
```

📢 **섹션 요약 비유**: `maxSurge`는 "공사 중 임시로 만들 수 있는 우회로 수", `maxUnavailable`은 "동시에 막을 수 있는 차선 수"다. 두 값의 조합이 공사 속도와 교통 흐름을 결정한다.

---

## Ⅲ. 비교 및 연결

### maxSurge/maxUnavailable 조합 [[268_strategy_pattern|전략]]

| [[009_config|설정]] | 특징 | 사용 시나리오 |
|:---|:---|:---|
| maxSurge=1, maxUnavailable=0 | 최대 [[452_availability|가용성]], 느린 배포 | 프로덕션 핵심 [[090_service_kubernetes_network_load_balancing|서비스]] |
| maxSurge=0, maxUnavailable=1 | 자원 절약, 중간 속도 | 자원 제약 환경 |
| maxSurge=25%, maxUnavailable=25% | 기본값, 균형 | 일반 [[090_service_kubernetes_network_load_balancing|서비스]] |
| maxSurge=100%, maxUnavailable=0 | 빠른 배포 (자원 2배) | 빠른 릴리즈 필요 |

### [[098_rollback_strategy_pipeline_error_threshold|롤백]] 방법

```bash
# 직전 버전으로 즉시 롤백
kubectl rollout undo deployment/my-app

# 특정 리비전으로 롤백
kubectl rollout undo deployment/my-app --to-revision=3

# 배포 상태 확인
kubectl rollout status deployment/my-app
kubectl rollout history deployment/my-app
```

📢 **섹션 요약 비유**: maxSurge와 maxUnavailable의 관계는 다리 공사에서 "임시 가교를 몇 개나 만들 수 있는지(maxSurge)"와 "동시에 몇 개 교각을 공사할 수 있는지(maxUnavailable)"의 관계다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**구/신 [[288_version_ihl_tos_total_length|버전]] 공존 문제 해결 방법**:
1. **[[014_api_posix|API]] [[288_version_ihl_tos_total_length|버전]] [[344_compatibility_usability|호환성]] 유지**: 신버전 코드가 구버전 [[014_api_posix|API]] 형식도 처리할 수 있도록 하위 호환 설계
2. **DB 마이그레이션 선행**: expand-contract 패턴으로 [[005_schema|스키마]]를 먼저 추가(호환)하고 배포 후 구버전 컬럼 제거
3. **readinessProbe [[009_config|설정]]**: 헬스체크 실패 Pod에는 트래픽을 보내지 않아 오류 전파 방지

**배포 속도 최적화**:
- `minReadySeconds` 줄이기 (단, 충분한 워밍업 필요)
- `maxSurge` 값 높이기 (자원 여유 있을 때)
- [[198_pod_kubernetes_minimum_deployment_unit|Pod]] Disruption Budget(PDB)과 함께 [[009_config|설정]]하여 최소 가용 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 수 보장

**기술사 판단 포인트**:
- [[117_rolling_update_deployment|롤링 업데이트]] 중 에러율이 급등하면 즉시 `kubectl rollout pause`로 일시 중지 후 원인 파악
- readinessProbe가 없으면 준비되지 않은 Pod에 트래픽이 유입되어 502/503 에러 발생
- [[087_deployment_kubernetes_workload_rolling_update|Deployment]] revision 이력을 통해 [[098_rollback_strategy_pipeline_error_threshold|롤백]] 지점 관리가 핵심이다

📢 **섹션 요약 비유**: 롤링 배포 중 에러 발생 시 즉시 멈추는 것은 고속도로 공사 중 사고가 나면 공사를 일시 중단하고 통행을 원상 복구하는 것과 같다. 빠른 감지와 빠른 중단이 피해를 최소화한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 설명 |
|:---|:---|
| [[082_zero_downtime_deployment_rolling_blue_green_canary|무중단 배포]] | [[090_service_kubernetes_network_load_balancing|서비스]] 중단 없이 업데이트 [[216_progress_in_synchronization|진행]] |
| 자원 효율 | 추가 인프라 비용 최소화 |
| K8s 표준 통합 | 별도 도구 없이 Deployment로 관리 |
| 점진적 [[395_verification_process_review|검증]] | 일부 Pod의 동작을 [[396_validation|확인]]하며 전체 교체 |

[[117_rolling_update_deployment|롤링 업데이트]]는 구버전 [[344_compatibility_usability|호환성]]이 보장된 대부분의 [[090_service_kubernetes_network_load_balancing|서비스]] 배포에서 최선의 선택이다. 특히 K8s 환경에서는 `readinessProbe`, `maxSurge`, `maxUnavailable` 세 가지를 제대로 [[009_config|설정]]하는 것만으로도 안정적인 [[082_zero_downtime_deployment_rolling_blue_green_canary|무중단 배포]]가 가능하다.

📢 **섹션 요약 비유**: [[117_rolling_update_deployment|롤링 업데이트]]를 제대로 [[009_config|설정]]하는 것은 고속도로 공사 계획서를 꼼꼼히 작성하는 것과 같다. 차선 수, 공사 순서, 안전 거리를 미리 정해두어야 공사 중에도 사고 없이 차가 달릴 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| K8s [[087_deployment_kubernetes_workload_rolling_update|Deployment]] | [[117_rolling_update_deployment|롤링 업데이트]]의 기본 구현체 |
| readinessProbe | 트래픽 수신 전 준비 완료 여부 [[396_validation|확인]] 핵심 [[009_config|설정]] |
| [[198_pod_kubernetes_minimum_deployment_unit|Pod]] Disruption Budget | 최소 가용 [[198_pod_kubernetes_minimum_deployment_unit|Pod]] 수 보장으로 롤링 중 [[085_sla|SLA]] 유지 |
| expand-contract 패턴 | DB [[005_schema|스키마]] 변경 시 롤링 배포와 호환 가능한 마이그레이션 |
| [[077_kube_api_server_k8s_hub|kubectl]] rollout | 배포 상태 [[396_validation|확인]]·일시 중지·[[098_rollback_strategy_pipeline_error_threshold|롤백]] [[158_instruction|명령어]] |
| Blue-Green / [[595_canary_stack_smashing_protector|Canary]] | [[117_rolling_update_deployment|롤링 업데이트]]로 해결이 어려운 상황을 커버하는 대안 [[268_strategy_pattern|전략]] |

### 👶 어린이를 위한 3줄 비유 설명

1. 롤링 배포는 식당에서 의자를 하나씩 교체하는 것처럼, 손님이 앉아있는 동안 빈 의자부터 하나씩 새 의자로 바꿔.

### 📈 관련 키워드 및 발전 흐름도

```text
K8s Deployment: maxSurge · maxUnavailable 설정
    │
    ▼
Rolling Update: 기존 Pod 종료 → 신규 Pod 생성 (순차)
    ├─► Readiness Probe: 트래픽 수신 준비 확인
    └─► Graceful Shutdown: 기존 연결 완료 대기
    │
    ▼
롤백: kubectl rollout undo → 이전 ReplicaSet 복원
```
2. 한 번에 다 바꾸면 손님이 앉을 의자가 없으니까, 하나 바꾸고→하나 돌아오고→또 하나 바꾸고 반복해.
3. `maxSurge`는 "의자를 최대 몇 개까지 동시에 밖에 내보낼 수 있는지", `maxUnavailable`은 "동시에 몇 개 자리를 비울 수 있는지"야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 192 / 371

← **이전**: [[192_zero_downtime_deployment_strategies|192. 무중단 배포 전략 3총사 (Zero Downtime Deployment Strategies)]]
**다음**: [[194_blue_green_deployment_strategy|194. 블루-그린 배포 (Blue-Green Deployment)]] →

---
