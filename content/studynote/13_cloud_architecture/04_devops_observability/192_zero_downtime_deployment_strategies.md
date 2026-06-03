+++
title = "192. 무중단 배포 전략 3총사 (Zero Downtime Deployment Strategies)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Rolling · Blue-Green · Canary는 각각 "점진 교체 / 완전 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 후 순간 전환 / 소수 선택 노출"이라는 서로 다른 트레이드오프를 가진 [무중단 배포](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/082_zero_downtime_deployment_rolling_blue_green_canary/) 패턴이다.
> 2. **가치**: [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 선택의 핵심 기준은 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 속도, 자원 비용, 구/신 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 혼재 허용 여부 세 가지다.
> 3. **판단 포인트**: DB [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 변경 동반 시 Rolling/Canary는 구/신 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 공존 문제가 발생하므로 Blue-Green이 안전하다.

---

## Ⅰ. 개요 및 필요성

[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 중단 없이 업데이트되어야 한다. 전통적 배포("서버 내려서 교체 후 다시 올리기")는 수 분~수십 분의 다운타임을 유발하여 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 위반과 매출 손실로 이어진다. [무중단 배포](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/082_zero_downtime_deployment_rolling_blue_green_canary/)([Zero Downtime Deployment](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/082_zero_downtime_deployment_rolling_blue_green_canary/))는 이 문제를 해결하기 위한 배포 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.

[무중단 배포](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/082_zero_downtime_deployment_rolling_blue_green_canary/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)의 선택은 단순한 기술 선택이 아니라 비즈니스 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 허용 수준, 인프라 비용 예산, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 특성에 따른 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 결정이다. 넷플릭스·아마존 같은 기업들은 하루에도 수천 번 배포하면서 99.99% 가용성을 유지하기 위해 이 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)들을 정교하게 조합한다.

세 가지 핵심 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)—[Rolling Update](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/083_rolling_update_deployment_zero_downtime_version_inconsistency/), Blue-Green, [Canary](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)—은 상호 배타적이지 않다. 실무에서는 이 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)들을 조합하거나 Feature Flag과 함께 사용하여 최적의 배포 파이프라인을 구성한다.

📢 **섹션 요약 비유**: 세 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 마치 기차를 달리면서 객차를 교체하는 방법 세 가지와 같다. 하나씩 조용히 바꾸거나(Rolling), 새 기차를 옆에 만들어 두고 승객을 한 번에 옮기거나(Blue-Green), 일부 승객만 새 기차에 태워 테스트하거나([Canary](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/))다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 세 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 핵심 비교

| 기준 | [Rolling Update](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/083_rolling_update_deployment_zero_downtime_version_inconsistency/) | Blue-Green | [Canary](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) |
|:---|:---:|:---:|:---:|
| [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 속도 | 느림 (단계적) | 즉시 (라우터 전환) | 빠름 ([가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 0%) |
| 자원 비용 | 1배 (순차 교체) | 2배 (동시 운영) | ~1.x배 (소량 추가) |
| 구/신 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 혼재 | ✅ (배포 중) | ❌ (순간 전환) | ✅ (의도적 혼재) |
| DB [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 변경 | 위험 | 안전 | 주의 필요 |
| K8s 기본 지원 | ✅ [Deployment](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/) | 별도 구성 | 별도 구성 |
| 적합 규모 | 소~중 | 중~대 | 대규모 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) |

### 배포 흐름 다이어그램

```
[Rolling Update]
v1 v1 v1 v1
     ↓ 순차 교체
v2 v1 v1 v1  →  v2 v2 v1 v1  →  v2 v2 v2 v1  →  v2 v2 v2 v2

[Blue-Green]
  현재: LB → [Blue: v1 v1 v1 v1]
                              ↓ 신버전 준비 완료 후 LB 전환
  전환: LB → [Green: v2 v2 v2 v2]
        (Blue는 롤백 대기로 유지)

[Canary]
  1단계: LB → 95% → [v1] / 5% → [v2-canary]
  2단계: LB → 80% → [v1] / 20% → [v2-canary]
  3단계: LB → 0%  → [v1] / 100% → [v2]
```

📢 **섹션 요약 비유**: Rolling은 달리는 버스의 바퀴를 하나씩 교체하는 것, Blue-Green은 새 버스를 완전히 만든 뒤 승객을 한 번에 이동시키는 것, Canary는 일부 승객만 새 버스에 먼저 태워보는 것이다.

---

## Ⅲ. 비교 및 연결

### [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)별 사용 시나리오

| [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 이상적인 상황 | 피해야 할 상황 |
|:---|:---|:---|
| [Rolling Update](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/083_rolling_update_deployment_zero_downtime_version_inconsistency/) | 빠른 배포, 자원 제약 환경, K8s 표준 워크플로우 | DB [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 변경 동반, 구버전 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 비호환 |
| Blue-Green | 즉각 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 필수, 규제 산업, DB 마이그레이션 | 자원 비용 민감, 상태 저장 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) |
| [Canary](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) | [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 민감 신기능, A/B 테스트 연계, 대규모 사용자 | 인프라 복잡도 수용 불가 환경 |

### K8s 구현 방식

| [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | K8s 구현 방법 |
|:---|:---|
| [Rolling Update](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/083_rolling_update_deployment_zero_downtime_version_inconsistency/) | `Deployment` 기본 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) (`RollingUpdate`) |
| Blue-Green | 두 개의 `Deployment` + `Service` 셀렉터 전환 |
| [Canary](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) | `Ingress` [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) or [Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/) `VirtualService` |

📢 **섹션 요약 비유**: 세 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 레스토랑 메뉴 교체 방법과 같다. Rolling은 메뉴를 하나씩 교체, Blue-Green은 별도 지점을 열어 완전히 준비된 뒤 이전, Canary는 VIP 고객에게만 신메뉴를 먼저 내놓는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong>배포 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a> 선택 결정 트리</strong>:
```
DB 스키마 변경 있는가?
  └─ Yes → Blue-Green (가장 안전)
  └─ No → 트래픽 규모가 크고 리스크 최소화 필요?
              └─ Yes → Canary (점진적 가중치)
              └─ No → 자원 제약 있는가?
                         └─ Yes → Rolling Update
                         └─ No → Blue-Green 또는 Canary
```

<strong><a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/">롤백</a> 시간 비교</strong>:
- Rolling: 역방향 [롤링 배포](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/193_rolling_update_deployment_kubernetes/), 수 분 소요
- Blue-Green: 로드밸런서 전환 1~2초, 즉시
- [Canary](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/): 신버전 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 0%로 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/), 수 초 이내

**기술사 판단 포인트**:
- 금융·의료 규제 환경에서는 Blue-Green이 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적과 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 명확성에서 유리하다.
- Canary는 Feature Flag과 결합하면 코드 배포 없는 기능 제어가 가능하다.
- [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 환경에서 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별로 다른 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 적용하는 것이 현실적이다.

📢 **섹션 요약 비유**: 배포 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 선택은 수술 방법 선택과 같다. 작은 시술은 국소마취(Rolling)로 충분하지만, 심장 수술(DB [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 변경)은 전신마취 후 완전한 준비(Blue-Green)가 필요하다.

---

## Ⅴ. 기대효과 및 결론

| [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 주요 기대효과 |
|:---|:---|
| [Rolling Update](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/083_rolling_update_deployment_zero_downtime_version_inconsistency/) | 자원 효율적 [무중단 배포](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/082_zero_downtime_deployment_rolling_blue_green_canary/), K8s 표준화 |
| Blue-Green | 즉각 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/), 완전한 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 분리, [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 용이 |
| [Canary](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) | [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 최소화, 실사용자 피드백 기반 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |

세 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 이해하고 상황에 맞게 선택하는 능력이 실무 [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 엔지니어의 핵심 역량이다. 하나의 "정답" [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 없으며, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 특성·팀 역량·비용 제약을 종합적으로 고려해야 한다.

📢 **섹션 요약 비유**: 세 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 모두 이해하는 것은 공구함에 망치·드라이버·렌치를 모두 갖추는 것이다. 어떤 나사에는 드라이버, 어떤 볼트에는 렌치가 맞듯, 상황에 맞는 도구를 고르는 것이 진짜 실력이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| K8s [Deployment](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/) | Rolling Update의 기본 구현체 (`strategy: RollingUpdate`) |
| [Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/) VirtualService | [Canary](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 트래픽 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 분배 [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/) 활용 |
| [Feature Flag](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/) | [Canary](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 배포와 결합하여 코드 배포 없는 기능 제어 |
| DB 마이그레이션 | 배포 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 선택의 핵심 결정 변수 |
| ArgoCD / Flux | [GitOps](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) 기반 세 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 모두 구현 가능한 CD 도구 |
| [Error Budget](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/101_error_budget_sre/) | [Canary](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 실험 중 에러율 임계치를 Error Budget으로 관리 |

### 👶 어린이를 위한 3줄 비유 설명

1. 롤링 업데이트는 달리는 버스에서 의자를 하나씩 교체하는 것처럼, 서버를 하나씩 새것으로 바꿔.

### 📈 관련 키워드 및 발전 흐름도

```text
다운타임 배포 (서비스 중단 후 교체)
    │
    ▼
무중단 배포 전략
    ├─► Rolling Update: 순차 교체
    ├─► Blue-Green: 환경 전환 (즉시 롤백)
    ├─► Canary: 소수 트래픽 → 점진 확대
    └─► Shadow: 트래픽 미러링 (무영향 검증)
    │
    ▼
Progressive Delivery + 자동 판단 (Argo Rollouts)
```
2. 블루-그린은 새 버스를 완전히 만들어 놓고 "자, 모두 옮겨 타세요!" 하고 한 번에 이동하는 것이야.
3. 카나리는 몇 명의 친구한테만 새 버스를 먼저 태워봐서 안전한지 확인한 다음 모두를 옮기는 방법이야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 191 / 371

← **이전**: [191. 카오스 엔지니어링 (Chaos 엔진ering)](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/191_chaos_engineering_chaos_monkey/)
**다음**: [193. 롤링 배포 (Rolling Update Deployment)](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/193_rolling_update_deployment_kubernetes/) →

---
