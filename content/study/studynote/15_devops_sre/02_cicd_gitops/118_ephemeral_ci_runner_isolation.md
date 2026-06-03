+++
weight = 118
title = "118. 일회성 CI 러너 (Ephemeral CI Runner) - 격리·보안·클린 빌드 보장"
date = "2026-04-19"
[extra]
categories = "studynote-devops-sre"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Ephemeral [[090_configuration_item|CI]] Runner는 **빌드마다 새로운 러너([[561_container_based_deployment|컨테이너]]/[[598_vm_migration_nic|VM]])를 [[087_process_state_transition|생성]]하고, 빌드 완료 후 즉시 삭제**하는 [[090_configuration_item|CI]] 실행 [[268_strategy_pattern|전략]]으로, 이전 빌드의 잔여물(캐시·[[501_file_definition_logical_record|파일]]·프로세스)이 다음 빌드에 영향을 주지 않는 **완전 격리(Clean Room)**를 보장한다.
> 2. **가치**: 영구 러너(Persistent Runner)는 이전 빌드의 `node_modules`·악성 [[501_file_definition_logical_record|파일]]·[[156_environment_variables|환경 변수]]가 남아 **빌드 오염(Build Pollution)·보안 침해**를 유발하지만, Ephemeral 러너는 매번 깨끗한 상태에서 시작한다.
> 3. **판단 포인트**: GitHub Actions(기본 Ephemeral)·GitLab Runner([[063_docker_architecture|Docker]] executor)·[[071_jenkins_ci_cd_pipeline_automation|Jenkins]](K8s [[198_pod_kubernetes_minimum_deployment_unit|Pod]] agent)가 대표 구현이며, **빌드 시간 vs 격리 보안**의 트레이드오프(캐시 활용 어려움)를 관리해야 한다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    Persistent vs Ephemeral Runner                     │
├───────────────────────────────────────────────────────┤
│  [Persistent (영구)]                                  │
│   Build 1 → Runner A (파일 잔여) →                   │
│   Build 2 → Runner A (오염된 환경!) ⚠️               │
│   → 재현 불가, 보안 취약                              │
│                                                       │
│  [Ephemeral (일회성)]                                 │
│   Build 1 → Runner X (새 생성) → 빌드 → 삭제 🗑️     │
│   Build 2 → Runner Y (새 생성) → 빌드 → 삭제 🗑️     │
│   → 완전 격리, 재현 가능, 보안 강화                   │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Persistent Runner는 매번 같은 접시에 음식을 담는 것(이전 음식 잔여물 위험)이고, Ephemeral Runner는 매번 새 일회용 접시를 사용하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[090_configuration_item|CI]] 도구별 Ephemeral 구현

| [[090_configuration_item|CI]] 도구 | 구현 방식 | 기본 모드 |
|:---|:---|:---|
| **GitHub Actions** | 매 워크플로마다 새 [[598_vm_migration_nic|VM]] | **Ephemeral (기본)** |
| **GitLab Runner** | [[063_docker_architecture|Docker]] executor | [[009_config|설정]] 필요 |
| **[[071_jenkins_ci_cd_pipeline_automation|Jenkins]]** | K8s [[198_pod_kubernetes_minimum_deployment_unit|Pod]] agent | [[009_config|설정]] 필요 |
| **Buildkite** | [[209_spot_instance_cloud_cost_optimization|스팟 인스턴스]] + 자동 종료 | [[009_config|설정]] 필요 |

### 캐시 트레이드오프

| [[268_strategy_pattern|전략]] | 격리 | 속도 |
|:---|:---|:---|
| **완전 Ephemeral** | **최고** | 느림 (매번 설치) |
| **캐시 레이어 분리** | 높음 | **빠름 (캐시 재사용)** |

- **📢 섹션 요약 비유**: 완전 Ephemeral은 매번 새 주방을 짓는 것이고, 캐시 분리는 냉장고(캐시)만 공유하고 조리대(러너)는 새로 만드는 절충안이다.

---

## Ⅲ. 비교 및 연결

| 비교 | Persistent | Ephemeral |
|:---|:---|:---|
| **격리** | 없음 | **완전** |
| **보안** | 취약 | **강화** |
| **재현성** | 낮음 | **높음** |
| **속도** | 빠름 (캐시) | 느림 (해결: 캐시 레이어) |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[087_erp_package_advantages_best_practice|Best Practice]]
1. **러너**: Ephemeral 기본, 캐시는 외부 저장소(S3) 활용.
2. **[[514_secret_management_vault_kms|시크릿]]**: 러너 종료 시 메모리에서 삭제 → 유출 방지.
3. **Self-hosted**: K8s [[198_pod_kubernetes_minimum_deployment_unit|Pod]] agent로 자동 [[087_process_state_transition|생성]]·삭제.

---

## Ⅴ. 기대효과 및 결론

| 지표 | Persistent | Ephemeral | 개선 |
|:---|:---|:---|:---|
| 빌드 오염 | 빈번 | **0건** | 완전 제거 |
| [[514_secret_management_vault_kms|시크릿]] 유출 | [[038_residual_risk|잔여 위험]] | **삭제 보장** | 보안 강화 |
| 재현성 | 환경 의존 | **100%** | [[090_configuration_item|CI]]/CD 신뢰 |

Ephemeral Runner는 **[[090_configuration_item|CI]]/CD 보안의 기본 원칙**이며, SLSA Level 3 이상에서는 격리된 빌드 환경이 필수 요구 사항이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **빌드 오염 (Build Pollution)** | Persistent Runner의 핵심 위험 |
| **GitHub Actions** | 기본 Ephemeral Runner |
| **K8s [[198_pod_kubernetes_minimum_deployment_unit|Pod]] Agent** | [[071_jenkins_ci_cd_pipeline_automation|Jenkins]]/GitLab의 Ephemeral 구현 |
| **SLSA** | 격리 빌드를 요구하는 [[374_supply_chain_security|공급망 보안]] 프레임워크 |
| **캐시 레이어** | Ephemeral + 속도의 절충안 |

### 📈 관련 키워드 및 발전 흐름도

```text
[물리 빌드 서버 (Persistent, 2000s)]
    │
    ▼
[Docker 기반 CI (GitLab Runner, 2015~)]
    │
    ▼
[GitHub Actions (2019) — 기본 Ephemeral VM]
    │
    ▼
[K8s Pod Agent (2020~) — 자동 생성·삭제]
    │
    ▼
[현재: SLSA + Ephemeral — 공급망 보안 필수 요건]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 영구 러너는 **같은 접시를 계속 쓰는** 거예요. 이전 음식 찌꺼기가 남아있을 수 있어요 ⚠️
2. 일회성 러너는 **매번 새 일회용 접시**를 사용해서 항상 깨끗해요! 🧹
3. 덕분에 이전 빌드의 나쁜 것이 **다음 빌드에 절대 영향을 주지 않아서** 안전하답니다!
