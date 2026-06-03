---
title: 109. 플랫폼 엔지니어링 (Platform Engineering) - 개발자 인지 부하 해소와 IDP 셀프서비스
date: '2026-04-19'
tags:
- studynote-software-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 플랫폼 엔지니어링(Platform Engineering)은 [[652_devops_calms_culture|DevOps]] 실천 과정에서 폭증한 개발자 [[686_cognitive_load_team_topologies|인지 부하]]([[686_cognitive_load_team_topologies|Cognitive Load]])를 해소하기 위해, 인프라·[[090_configuration_item|CI]]/CD·보안 도구를 [[198_abstraction_control_data_process|추상화]]한 **[[110_idp_internal_developer_platform_backstage|내부 개발자 플랫폼]]([[536_idp_identity_provider|IDP]])**을 구축·운영하는 규율이다.
> 2. **가치**: 앱 개발자가 [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]]·K8s·[[526_iam|IAM]] 지식 없이도 **셀프서비스 포털 클릭 한 번으로 보안 [[395_verification_process_review|검증]]된 환경을 [[528_provisioning|프로비저닝]]**하여 Time-to-Market을 단축하고 Shadow IT를 원천 차단한다.
> 3. **판단 포인트**: 플랫폼 팀은 제품(Product)처럼 IDP를 운영해야 하며, Golden Path와 Escape Hatch의 균형 설계가 성공의 핵심이다.

---

## Ⅰ. 개요 및 필요성

[[652_devops_calms_culture|DevOps]] 철학("You build it, You run it")으로 배포 속도는 향상되었으나, 앱 개발자가 K8s 매니페스트·[[793_iac_idempotency_template|IaC]]·[[007_security_policy|보안 정책]]까지 직접 작성해야 하는 **[[686_cognitive_load_team_topologies|인지 부하]]([[686_cognitive_load_team_topologies|Cognitive Load]]) 폭발**이 심화되었다. Team Topologies의 Extraneous(업무 외 잡음) 부하가 번아웃과 줄퇴사의 직접 원인으로 지목된다.

```text
┌───────────────────────────────────────────────────────────────┐
│    DevOps 시대의 인지 부하 문제와 플랫폼 엔지니어링 해법       │
├───────────────────────────────────────────────────────────────┤
│  [ Before: DevOps 1.0 ]                                       │
│   App Code + K8s + Terraform + CI/CD + IAM + Monitoring       │
│        → Cognitive Load ▲▲▲  → Burnout                      │
│                                                               │
│  [ After: Platform Engineering ]                              │
│   ┌──────────────┐      ┌─────────────────────┐              │
│   │ App Developer │ ──▶  │  Platform Team      │              │
│   │ "DB 하나 주세요"│      │  IDP 포털 운영      │              │
│   └──────────────┘      │  Golden Path 템플릿  │              │
│     셀프서비스 클릭       └─────────────────────┘              │
│     → Cognitive Load ▼▼  → 비즈니스 집중                     │
└───────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[652_devops_calms_culture|DevOps]] [[459_quic_fec_forward_error_correction|초기]]에는 셰프에게 밀 베기부터 설거지까지 시켰다. 플랫폼 엔지니어링은 반죽 기계([[536_idp_identity_provider|IDP]])를 설치해 셰프가 토핑(비즈니스 코드)만 올리게 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 계층 | 역할 | 대표 도구 | 비유 |
|:---|:---|:---|:---|
| **개발자 포털 (UI)** | 셀프서비스 [[394_catalog_metadata|카탈로그]] 제공 | Backstage, [[446_port_and_bus|Port]], Humanitec | 자판기 화면 |
| **[[073_container_orchestration_tools|오케스트레이션]]** | [[528_provisioning|프로비저닝]] 워크플로 실행 | Crossplane, [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]] Cloud, ArgoCD | 로봇 팔 |
| **인프라 [[198_abstraction_control_data_process|추상화]]** | [[793_iac_idempotency_template|IaC]] [[192_module_independence|모듈]]·K8s [[565_operator_pattern_kubernetes_automation|Operator]]·[[007_security_policy|보안 정책]] | [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]] [[192_module_independence|Module]], [[056_helm_chart|Helm Chart]], [[237_opa_open_policy_agent_gatekeeper|OPA]] | 원재료 [[520_supply_chain_attack_and_ci_cd_security|공급망]] |
| **거버넌스** | [[164_policy|정책]] [[395_verification_process_review|검증]]·비용 통제·[[569_rbac|RBAC]] | [[237_opa_open_policy_agent_gatekeeper|OPA]] Gatekeeper, [[344_finops|FinOps]] 대시보드 | 품질 검수 라인 |

**Golden Path 설계 원칙**: 80%가 사용하는 표준 경로를 포장하되, 20% 파워 유저에게 Escape Hatch(직접 [[793_iac_idempotency_template|IaC]] 작성)를 열어둔다. IDP를 내부 제품으로 취급하여 NPS·릴리즈 노트·로드맵을 운영한다.

- **📢 섹션 요약 비유**: Golden Path는 고속도로(빠르고 안전), Escape Hatch는 국도(느리지만 자유)이다.

---

## Ⅲ. 비교 및 연결

| 비교 항목 | [[652_devops_calms_culture|DevOps]] (문화) | 플랫폼 엔지니어링 (구현) | [[100_sre_site_reliability_engineering_error_budget|SRE]] ([[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]) |
|:---|:---|:---|:---|
| **정의** | 개발·운영 협업 문화 | DevOps를 제품화한 [[536_idp_identity_provider|IDP]] 구축 | 운영 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]을 SLO로 관리 |
| **산출물** | [[090_configuration_item|CI]]/CD, 자동화 스크립트 | 셀프서비스 포털, Golden Path | [[101_error_budget_sre|Error Budget]], Runbook |
| **[[083_relationship_in_er_model|관계]]** | 상위 철학 | DevOps를 현실화하는 수단 | 운영 품질 보증 보완재 |

- **📢 섹션 요약 비유**: DevOps가 "운동하자!"라는 구호라면, 플랫폼 엔지니어링은 헬스장([[536_idp_identity_provider|IDP]])을 짓는 것이고, SRE는 트레이너를 배치하는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 도입 [[435_checklist_based_testing|체크리스트]]
1. Stream-aligned Team이 4개 이상, 인프라 티켓 [[085_sla|SLA]] 평균 3일 이상 → 플랫폼 팀 분리 시점.
2. [[459_quic_fec_forward_error_correction|초기]] [[036_mvp|MVP]]: Backstage + ArgoCD + Crossplane으로 "새 [[619_msa_traffic_hardware|MSA]] [[087_process_state_transition|생성]]" 셀프서비스 4주 내 제공.
3. 성공 지표: 플랫폼 채택률(WAU), 인프라 티켓 감소율, [[023_dora_deployment_frequency|DORA Deployment Frequency]].

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- **Ivory Tower**: 개발자 의견 무시 [[536_idp_identity_provider|IDP]] → 채택률 0%.
- **과잉 [[198_abstraction_control_data_process|추상화]]**: K8s를 완전히 숨겨 디버깅 불가능한 블랙박스 → 장애 시 속수무책.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 미도입 | 도입 후 | 개선 |
|:---|:---|:---|:---|
| 인프라 [[528_provisioning|프로비저닝]] | 3~5일 | **5분** | 98% 단축 |
| 개발자 온보딩 | 2~4주 | **1~2일** | 90% 단축 |
| [[049_shadow_it|Shadow IT]] | 높음 | **0%** | 거버넌스 확보 |
| 배포 빈도 | 주 1회 | **일 수회** | [[652_devops_calms_culture|DevOps]] 가속 |

Gartner는 2026년까지 대형 SW 조직 80%가 플랫폼 팀을 운영할 것으로 전망하며, IDP는 [[190_ai_llm_requirements_specification|AI]] 코드 [[087_process_state_transition|생성]] 도구와 결합해 "프롬프트 한 줄로 프로덕션 환경 즉시 [[528_provisioning|프로비저닝]]" 시대를 앞당길 것이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[652_devops_calms_culture|DevOps]]** | 플랫폼 엔지니어링이 구현하려는 상위 철학 |
| **[[536_idp_identity_provider|IDP]] ([[200_internal_developer_platform_backstage|Internal Developer Platform]])** | 핵심 산출물이자 셀프서비스 포털 |
| **Backstage** | [[536_idp_identity_provider|IDP]] 개발자 포털의 사실상 표준 [[191_oss_license_compliance|오픈소스]] |
| **Team Topologies** | 플랫폼 팀 역할·[[686_cognitive_load_team_topologies|인지 부하]] 유형 분류의 이론적 기반 |
| **Golden Path** | [[395_verification_process_review|검증]]된 표준 개발·배포 경로 템플릿 |
| **Crossplane** | K8s API로 클라우드 인프라를 선언적 [[528_provisioning|프로비저닝]]하는 엔진 |

### 📈 관련 키워드 및 발전 흐름도

```text
[DevOps 문화 확산 (2010s) — "You Build It, You Run It"]
    │
    ▼
[인지 부하 폭발 — 개발자가 인프라·보안·모니터링 전부 담당]
    │
    ▼
[Team Topologies (2019) — 플랫폼 팀 개념 정립]
    │
    ▼
[IDP 1세대 (2020~) — Backstage 오픈소스화]
    │
    ▼
[현재: Platform-as-a-Product — Golden Path + FinOps + AI 통합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 옛날에는 피자를 만들려면 밀 베기부터 오븐 만들기까지 전부 해야 해서 피자 장인(개발자)이 너무 힘들었어요.
2. 플랫폼 엔지니어링은 **자동 반죽 기계([[536_idp_identity_provider|IDP]])**를 설치해서, 장인은 버튼 한 번으로 반죽을 받고 맛있는 토핑만 올리면 돼요!
3. 덕분에 피자가 훨씬 빨리 나오고, 장인이 과로로 쓰러지는 일도 사라졌답니다!
