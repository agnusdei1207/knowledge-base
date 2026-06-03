+++
weight = 194
title = "194. 블루-그린 배포 (Blue-Green Deployment)"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 현재 운영 환경(Blue)과 완전히 동일한 규모의 신버전 환경(Green)을 사전 구성해두고, 트래픽을 한 번에 전환하는 '즉시 스위칭' 배포 패턴이다.
> 2. **가치**: [[098_rollback_strategy_pipeline_error_threshold|롤백]]이 로드밸런서 포인터 변경 한 번으로 1~2초 내 완료되며, 구/신 [[288_version_ihl_tos_total_length|버전]] 혼재 문제가 없어 DB [[005_schema|스키마]] 변경 동반 배포에서 가장 안전하다.
> 3. **판단 포인트**: 자원이 일시적으로 2배 소모되므로 비용 대 안전성 트레이드오프와 상태 비저장([[239_stateless_redis|Stateless]]) [[090_service_kubernetes_network_load_balancing|서비스]] 여부 [[396_validation|확인]]이 핵심이다.

---

## Ⅰ. 개요 및 필요성

블루-그린 배포는 1990년대 Daniel Terhorst-North와 Jez Humble이 『[[164_continuous_delivery|Continuous Delivery]]』에서 정립한 패턴이다. 이름의 유래는 두 환경을 Blue(구버전)와 Green(신버전)으로 색으로 구분하는 데서 왔다.

핵심 아이디어는 단순하다: 언제든지 즉시 이전 [[288_version_ihl_tos_total_length|버전]]으로 돌아갈 수 있는 **완전한 환경을 항상 유지**하는 것이다. 신버전(Green)이 완전히 준비되고 테스트가 완료된 이후에야 로드밸런서가 트래픽을 Green으로 전환한다. 문제가 발생하면 로드밸런서를 다시 Blue로 돌리면 된다.

이 방식이 특히 강력한 상황은 **DB [[005_schema|스키마]] 변경이 동반되는 배포**다. 신버전용 DB를 별도로 마이그레이션하고 Green 환경에서 완전히 [[395_verification_process_review|검증]]한 뒤 전환하면, 구버전 코드와 신버전 DB가 섞이는 상황을 원천적으로 방지할 수 있다.

📢 **섹션 요약 비유**: 블루-그린 배포는 공연 무대를 교체하는 것과 같다. 한 무대(Blue)에서 공연 중인 동안 백스테이지에서 새 무대 세트(Green)를 완전히 준비하고, 막간에 한 번에 전환한다. 문제 생기면 다시 블루 무대로 돌아가면 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 블루-그린 배포 구조

```
  ┌─────────────────────────────────────────────────────────────┐
  │                     Load Balancer / DNS                      │
  └──────────────────────────┬──────────────────────────────────┘
                             │
           ┌─────────────────┼─────────────────┐
           ▼                                   ▼
  ┌─────────────────┐                ┌─────────────────┐
  │  Blue 환경 (v1) │  ←── 현재 운영 │  Green 환경(v2) │ ←── 준비 중
  │  [App v1 x4]    │                │  [App v2 x4]    │
  │  [DB: Schema A] │                │  [DB: Schema B] │
  └─────────────────┘                └─────────────────┘
           │
           ▼
  [트래픽 전환 후]
  LB → Green 100% / Blue 대기 (즉시 롤백 대기)
```

### 배포 절차

| 단계 | 행동 |
|:---:|:---|
| 1 | Green 환경 [[528_provisioning|프로비저닝]] (Blue와 동일 인프라) |
| 2 | Green에 신버전 코드·DB 마이그레이션 적용 |
| 3 | Green 환경에서 스모크 테스트·[[400_integration_testing|통합 테스트]] 수행 |
| 4 | 로드밸런서 / [[511_dns_hierarchical_distributed_architecture|DNS]] 레코드를 Green으로 전환 |
| 5 | 모니터링 (수 분~수 시간 안정화 관찰) |
| 6 | 안정화 [[396_validation|확인]] → Blue 환경 자원 해제 (또는 다음 배포까지 유지) |

### K8s에서의 구현

```yaml
# Blue Service (현재 운영)
apiVersion: v1
kind: Service
metadata:
  name: my-app
spec:
  selector:
    app: my-app
    version: blue    # ← 이 셀렉터를 green으로 변경하면 전환 완료
  ports:
  - port: 80
    targetPort: 8080
---
# Blue Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-blue
spec:
  replicas: 4
  selector:
    matchLabels:
      app: my-app
      version: blue
  template:
    metadata:
      labels:
        app: my-app
        version: blue
    spec:
      containers:
      - name: my-app
        image: my-app:v1
---
# Green Deployment (신버전 준비)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-green
spec:
  replicas: 4
  selector:
    matchLabels:
      app: my-app
      version: green
  template:
    metadata:
      labels:
        app: my-app
        version: green
    spec:
      containers:
      - name: my-app
        image: my-app:v2
```

📢 **섹션 요약 비유**: K8s Service의 `selector`가 Blue/Green을 가리키는 방향키다. 전환은 YAML 한 줄 변경으로 완료되며, [[098_rollback_strategy_pipeline_error_threshold|롤백]]도 마찬가지로 한 줄 되돌리기면 충분하다.

---

## Ⅲ. 비교 및 연결

### 블루-그린 vs 롤링 비교

| 항목 | Blue-Green | [[083_rolling_update_deployment_zero_downtime_version_inconsistency|Rolling Update]] |
|:---|:---:|:---:|
| 구/신 [[288_version_ihl_tos_total_length|버전]] 혼재 | ❌ (순간 전환) | ✅ (배포 중) |
| 자원 비용 | 2배 (동시 운영) | ~1.25배 |
| [[098_rollback_strategy_pipeline_error_threshold|롤백]] 속도 | 1~2초 | 수 분 |
| DB [[005_schema|스키마]] 변경 | ✅ 안전 | ⚠️ 위험 |
| 구현 복잡도 | 중간 | 낮음 (K8s 기본) |

### Warm Standby vs Blue-Green

| 항목 | Blue-Green | Warm Standby ([[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]]) |
|:---|:---|:---|
| 목적 | 배포 [[268_strategy_pattern|전략]] | [[379_dr_architecture|재해 복구]] |
| Green/Standby [[288_version_ihl_tos_total_length|버전]] | 신버전 (다른 코드) | 동일 [[288_version_ihl_tos_total_length|버전]] ([[016_replication_factor|복제]]) |
| 전환 계기 | 배포 완료 | 장애 발생 |

📢 **섹션 요약 비유**: 블루-그린은 TV 방송국의 스튜디오 교체와 같다. A 스튜디오에서 방송 중 B 스튜디오를 완전히 셋업하고, 광고 시간에 "지금부터 B 스튜디오에서 진행합니다"로 전환한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**비용 최적화 [[268_strategy_pattern|전략]]**:
1. 클라우드 환경에서는 Green 환경을 배포 직전에 자동 [[528_provisioning|프로비저닝]]하고, 안정화 후 Blue를 즉시 삭제하여 비용 절감
2. [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]]/Pulumi로 환경을 코드화하면 Green 환경 생성에 5분 미만 소요
3. [[001_dikw_pyramid|데이터]]베이스는 공유 DB + [[005_schema|스키마]] [[288_version_ihl_tos_total_length|버전]] 관리를 통해 DB [[016_replication_factor|복제]] 비용 절약 가능

**상태 있는 [[090_service_kubernetes_network_load_balancing|서비스]](Stateful) 주의**:
- [[160_session_controlling_terminal|세션]] [[001_dikw_pyramid|데이터]]를 서버 로컬에 저장하는 [[090_service_kubernetes_network_load_balancing|서비스]]는 전환 시 [[160_session_controlling_terminal|세션]] 유실
- 해결책: [[542_redis|Redis]] 같은 외부 [[160_session_controlling_terminal|세션]] 저장소 사용 ([[239_stateless_redis|Stateless]] 아키텍처 선행 필요)

**기술사 판단 포인트**:
- 금융, 의료 등 규제 산업에서는 배포 전 완전한 [[395_verification_process_review|검증]]이 필수 → Blue-Green 최적
- [[511_dns_hierarchical_distributed_architecture|DNS]] [[294_ttl_time_to_live_looping_prevention|TTL]] 고려: [[511_dns_hierarchical_distributed_architecture|DNS]] 기반 전환 시 TTL만큼 구버전 응답이 섞일 수 있음 (IP 직접 전환 또는 짧은 [[294_ttl_time_to_live_looping_prevention|TTL]] [[009_config|설정]])
- Blue 환경 유지 기간: 안정화 [[396_validation|확인]] 전까지 최소 1~24시간 유지 권장

📢 **섹션 요약 비유**: 블루-그린은 인수인계와 같다. 전임자(Blue)가 업무를 완전히 넘기기 전까지 후임자(Green)가 모든 준비를 마치고, 인수인계 완료 후에야 전임자가 퇴장한다. 중간에 문제가 생기면 전임자가 즉시 복귀한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 설명 |
|:---|:---|
| 즉시 [[098_rollback_strategy_pipeline_error_threshold|롤백]] | LB 전환 1~2초로 이전 [[288_version_ihl_tos_total_length|버전]] [[658_ir_recovery|복구]] |
| 완전한 [[288_version_ihl_tos_total_length|버전]] 분리 | 구/신 [[288_version_ihl_tos_total_length|버전]] 혼재 없어 [[014_api_posix|API]] 호환 문제 없음 |
| 프리-프로덕션 [[395_verification_process_review|검증]] | Green에서 실서비스 환경과 동일한 테스트 가능 |
| 규제 [[606_auditing_linux_auditd|감사]] 용이 | 배포 이력과 [[098_rollback_strategy_pipeline_error_threshold|롤백]] 증적이 명확 |

**한계**: 자원 비용 2배는 실제로는 단기간(수 시간~1일)에 불과하며, 클라우드 환경에서는 그 비용이 크지 않다. 진정한 한계는 Stateful [[090_service_kubernetes_network_load_balancing|서비스]]에서 DB [[001_dikw_pyramid|데이터]] [[212_synchronization_mechanisms|동기화]] 복잡성과, 실시간 [[160_session_controlling_terminal|세션]]이 Blue에서 Green으로 이어지지 않는 문제다.

📢 **섹션 요약 비유**: 블루-그린의 "2배 비용"은 마치 이사할 때 잠깐 두 집 월세를 내는 것과 같다. 짧은 기간이고 안전한 이사를 보장하는 비용이라면 충분히 납득 가능하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[031_load_balancer|Load Balancer]] | 트래픽 전환의 물리적 [[238_switch_operation_principles|스위치]] 역할 |
| DB 마이그레이션 | Blue-Green의 가장 강력한 적용 시나리오 |
| [[239_stateless_redis|Stateless]] 아키텍처 | Blue-Green [[160_session_controlling_terminal|세션]] 유실 문제의 근본적 해결책 |
| [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]] / [[793_iac_idempotency_template|IaC]] | Green 환경 자동 [[528_provisioning|프로비저닝]]으로 비용 최적화 |
| [[511_dns_hierarchical_distributed_architecture|DNS]] [[294_ttl_time_to_live_looping_prevention|TTL]] | 전환 지연의 원인, 짧게 [[009_config|설정]]하여 최소화 필요 |
| [[595_canary_stack_smashing_protector|Canary]] 배포 | Blue-Green 이후 더 세밀한 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] [[136_variance|분산]] [[268_strategy_pattern|전략]] |

### 👶 어린이를 위한 3줄 비유 설명

1. 블루-그린은 다음 공연을 위해 백스테이지에서 완전히 새 무대를 만들어 놓고, 막간에 한 번에 교체하는 거야.

### 📈 관련 키워드 및 발전 흐름도

```text
Blue (현재 운영) ↔ Green (대기 환경)
    │
    ▼
배포: Green에 신버전 → 검증 → 라우터 전환
    │
    ▼
롤백: 라우터를 Blue로 되돌림 (즉시)
    │
    ▼
비용 절감: 클라우드 Auto-Provision Green 환경
```
2. 새 무대에 문제가 생기면 5초 만에 다시 옛날 무대로 돌아갈 수 있어서 관객은 거의 눈치채지 못해.
3. 대신 무대 두 개를 동시에 준비해야 하니까, 잠깐 비용이 2배가 돼. 하지만 그게 안전을 보장하는 값어치야.
