+++
title = "121. CI/CD 파이프라인 자동화 - 빌드·테스트·배포의 지속적 통합/전달 체계"
date = 2026-04-19

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD는 코드 변경 시 <strong>빌드·테스트를 자동 실행(<a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/">CI</a>: <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/019_continuous_integration/">Continuous Integration</a>)</strong>하고, 검증된 코드를 <strong>스테이징·프로덕션에 자동 배포(CD: <a href="/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/164_continuous_delivery/">Continuous Delivery</a>/<a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/">Deployment</a>)</strong>하는 소프트웨어 엔지니어링의 핵심 자동화 체계다.
> 2. **가치**: 수동 빌드·배포는 인적 오류·시간 낭비·릴리스 공포(Fear of Release)를 유발하지만, [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 파이프라인은 <strong>커밋→빌드→테스트→배포를 30분 이내에 자동 완료</strong>하여 [DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 지표(배포 빈도·[리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/))를 극적으로 개선한다.
> 3. **판단 포인트**: [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)(통합) vs CD-Delivery(수동 승인 후 배포) vs CD-[Deployment](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/)(완전 자동 배포)를 구분하고, [트렁크 기반 개발](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/040_trunk_based_development/)(Trunk-Based Dev) + [피처 플래그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/) 조합이 Elite 팀의 표준이다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    CI/CD 파이프라인 단계                              │
├───────────────────────────────────────────────────────┤
│  [CI — Continuous Integration]                        │
│   커밋 → 빌드 → 단위 테스트 → 통합 테스트           │
│   → 코드 품질 검증 (린트·커버리지)                    │
│                                                       │
│  [CD — Continuous Delivery]                           │
│   CI 통과 → 스테이징 배포 → QA → 수동 승인 → Prod   │
│                                                       │
│  [CD — Continuous Deployment]                         │
│   CI 통과 → 자동 Prod 배포 (승인 없음)               │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: CI는 공장 조립 라인의 품질 검사(불량 자동 탐지)이고, CD는 검사 통과한 제품을 매장(프로덕션)에 자동 진열하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) vs CD 비교

| 구분 | [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) | CD (Delivery) | CD ([Deployment](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/)) |
|:---|:---|:---|:---|
| **자동화** | 빌드·테스트 | + 스테이징 배포 | **+ 프로덕션 배포** |
| **승인** | 자동 | **수동 승인** | 자동 |
| **위험** | 낮음 | 중간 | 높음 (자동 배포) |

### 파이프라인 도구

| 도구 | 특징 |
|:---|:---|
| **GitHub Actions** | GitHub 내장, YAML 정의 |
| <strong>GitLab <a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/">CI</a></strong> | GitLab 내장, .gitlab-[ci](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/).yml |
| <strong><a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/">Jenkins</a></strong> | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/), 플러그인 생태계 |
| **ArgoCD** | K8s [GitOps](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) CD |

- **📢 섹션 요약 비유**: [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 도구는 자동차 공장의 로봇 팔이다. 사람 없이 용접(빌드)→검사(테스트)→출고(배포)를 자동으로 한다.

---

## Ⅲ. 비교 및 연결

| 비교 | 수동 배포 | CI만 | [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD |
|:---|:---|:---|:---|
| **배포 빈도** | 월 1회 | 주 1회 | **하루 여러 번** |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/">리드 타임</a></strong> | 주~월 | 일 | **시간** |
| **인적 오류** | 빈번 | 줄어듦 | **최소** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 파이프라인 설계 [Best Practice](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/087_erp_package_advantages_best_practice/)
1. **빠른 피드백**: [단위 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/) 먼저, 느린 [E2E](/knowledge-base/studynote/15_devops_sre/05_devsecops/265_e2e_end_to_ui_selenium/) 테스트는 나중에.
2. <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/">피처 플래그</a></strong>: 불완전 기능도 main에 머지 → [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)로 숨김.
3. **트렁크 기반**: 장기 브랜치 금지 → 머지 충돌 최소화.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 수동 | [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD | 개선 |
|:---|:---|:---|:---|
| 배포 빈도 | 월 1회 | **하루 N회** | 30× |
| [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/) | 수 주 | **수 시간** | 100× |
| 변경 실패율 | 높음 | **낮음** | 테스트 자동화 |

[CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD는 현대 소프트웨어 개발의 <strong>기본 인프라</strong>이며, [GitOps](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/)·Progressive Delivery·AIOps와 결합하여 지속 진화하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/">CI</a></strong> | [지속적 통합](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/) (빌드+테스트 자동화) |
| **CD** | [지속적 전달](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/020_continuous_delivery/)/배포 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/">GitOps</a></strong> | CD의 선언적 구현 |
| <strong><a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/040_trunk_based_development/">트렁크 기반 개발</a></strong> | [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 최적화 브랜치 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/201_dora_metrics_devops_performance/">DORA Metrics</a></strong> | [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 성과 측정 지표 |

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 빌드·배포 (2000s)]
    │
    ▼
[CI 서버 (Jenkins, 2004~) — 자동 빌드·테스트]
    │
    ▼
[CD (Docker+K8s, 2014~) — 자동 배포 파이프라인]
    │
    ▼
[GitOps (2017~) — 선언적 CD (ArgoCD/Flux)]
    │
    ▼
[현재: Progressive Delivery + AIOps — AI 기반 배포 판단]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD는 공장의 <strong>자동 조립 라인</strong>이에요. 재료(코드)를 넣으면 검사(테스트)하고 완제품(배포)이 나와요.
2. 불량품(버그)이 발견되면 **즉시 라인이 멈추고** 알려줘요.
3. 덕분에 **하루에 여러 번** 새 제품(기능)을 안전하게 출시할 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 121 / 973

← **이전**: [120. 선언적 인프라와 멱등성 (Declarative Infrastructure & Idempotence) - IaC 핵심 원칙](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/120_declarative_infrastructure_idempotence/)
**다음**: [122. 컨테이너 오케스트레이션 (Container Orchestration) - K8s 핵심 개념과 아키텍처](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/122_container_orchestration_kubernetes_k8s/) →

---
