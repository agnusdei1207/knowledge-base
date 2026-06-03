+++
title = "200. IDP / Backstage (Internal Developer Platform)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [IDP](/knowledge-base/studynote/09_security/11_iam_access_control/536_idp_identity_provider/)(Internal Developer Platform)는 개발자가 인프라·[CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD·[서비스 카탈로그](/knowledge-base/studynote/12_it_management/02_itsm_itil/088_service_catalog/)를 티켓 없이 셀프서비스로 사용할 수 있는 내부 개발자 포털이다.
> 2. **가치**: Spotify의 Backstage([CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) 졸업 프로젝트)는 플러그인 아키텍처로 조직의 모든 도구([Jenkins](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/), PagerDuty, AWS, [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/))를 하나의 포털에 통합하여 [개발자 경험](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/058_dx_developer_experience/)을 혁신한다.
> 3. **판단 포인트**: [IDP](/knowledge-base/studynote/09_security/11_iam_access_control/536_idp_identity_provider/) 구축의 성패는 기술이 아닌 거버넌스다. [서비스 카탈로그](/knowledge-base/studynote/12_it_management/02_itsm_itil/088_service_catalog/) 등록·유지 관리의 책임을 누가 질 것인지, 골든 패스 템플릿을 누가 최신화할 것인지가 핵심 과제다.

---

## Ⅰ. 개요 및 필요성

[IDP](/knowledge-base/studynote/09_security/11_iam_access_control/536_idp_identity_provider/)(Internal Developer Platform)는 [플랫폼 엔지니어링](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/109_platform_engineering_cognitive_load/)의 구체적 산출물이다. 개발자가 새 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 만들거나 인프라를 프로비저닝하거나 배포 파이프라인을 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)할 때 다양한 도구(Jira, [Jenkins](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/), [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/), [Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/), PagerDuty 등)로 분산된 작업을 **하나의 포털에서** 수행할 수 있게 한다.

Spotify는 2016년부터 이 문제를 해결하기 위해 내부 도구 Backstage를 개발했다. 수천 명의 엔지니어와 수백 개의 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 관리하면서, "이 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 어디에 배포됐는지", "담당자가 누군지", "어떤 버전이 운영 중인지"를 파악하는 것 자체가 엄청난 인지 부하가 됐다. Backstage의 [서비스 카탈로그](/knowledge-base/studynote/12_it_management/02_itsm_itil/088_service_catalog/)가 이 문제를 해결했다.

2020년 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/)로 공개된 Backstage는 2022년 CNCF에 기부되었고, 현재 1,000개 이상의 조직에서 사용된다. Airbnb, LinkedIn, [Splunk](/knowledge-base/studynote/09_security/13_secops_ir_forensics/630_splunk/) 등이 Backstage를 기반으로 자체 IDP를 구축했다.

📢 **섹션 요약 비유**: IDP는 회사 내부의 아마존 쇼핑몰과 같다. 개발자가 "[Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 캐시 인스턴스 1개"를 검색하고 클릭하면, 즉시 프로비저닝되어 연결 정보가 전달된다. 운영팀에 이메일 보내고 기다릴 필요가 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Backstage 핵심 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)

```
  ┌─────────────────────────────────────────────────────────┐
  │                 Backstage IDP 포털                        │
  ├─────────────────────────────────────────────────────────┤
  │                                                          │
  │  ┌─────────────────┐    ┌─────────────────────────────┐ │
  │  │  Service Catalog │    │      Software Templates      │ │
  │  │  (서비스 카탈로그)│    │      (골든 패스 스캐폴딩)    │ │
  │  │                  │    │                              │ │
  │  │ - 서비스 목록     │    │ - 서비스 생성 워크플로우      │ │
  │  │ - 소유자·팀       │    │ - CI/CD 파이프라인 자동 구성  │ │
  │  │ - API 문서        │    │ - IaC 코드 생성              │ │
  │  │ - 의존성 맵       │    │ - 보안·모니터링 기본값 포함   │ │
  │  └─────────────────┘    └─────────────────────────────┘ │
  │                                                          │
  │  ┌────────────────────────────────────────────────────┐ │
  │  │                   Plugin 생태계                      │ │
  │  │  [K8s] [GitHub] [Jenkins] [PagerDuty] [Datadog]    │ │
  │  │  [SonarQube] [Vault] [AWS] [Terraform Cloud] ...   │ │
  │  └────────────────────────────────────────────────────┘ │
  └─────────────────────────────────────────────────────────┘
```

### catalog-info.yaml ([서비스 카탈로그](/knowledge-base/studynote/12_it_management/02_itsm_itil/088_service_catalog/) 등록)

```yaml
# 모든 서비스의 루트 디렉토리에 배치
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: payment-service
  description: "결제 처리 마이크로서비스"
  annotations:
    github.com/project-slug: myorg/payment-service
    backstage.io/techdocs-ref: dir:.
    pagerduty.com/service-id: P123456
  tags:
    - java
    - payment
    - critical
spec:
  type: service
  lifecycle: production
  owner: team-payments
  system: checkout-platform
  dependsOn:
    - component:order-service
    - resource:payments-db
  providesApis:
    - payment-api-v2
```

### Software Template ([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 스캐폴딩)

```yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: springboot-microservice
  title: "Spring Boot 마이크로서비스 생성"
spec:
  parameters:
    - title: "서비스 기본 정보"
      properties:
        serviceName:
          title: 서비스명
          type: string
        owner:
          title: 담당 팀
          type: string
  steps:
    - id: fetch-template
      action: fetch:template
      input:
        url: ./skeleton         # 표준 프로젝트 구조
    - id: create-repo
      action: github:repo:create
    - id: create-pipeline
      action: jenkins:pipeline:create  # CI/CD 자동 구성
    - id: register-catalog
      action: catalog:register         # 카탈로그 자동 등록
```

📢 **섹션 요약 비유**: Software Template은 집 건축의 표준 설계도와 같다. 개발자가 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)명·팀명만 입력하면, 표준 설계도에 따라 깃허브 저장소·[Jenkins](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/) 파이프라인·K8s [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)·모니터링 대시보드가 자동으로 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)된다.

---

## Ⅲ. 비교 및 연결

### [IDP](/knowledge-base/studynote/09_security/11_iam_access_control/536_idp_identity_provider/) 구축 방식 비교

| 방식 | 장점 | 단점 | 적합 규모 |
|:---|:---|:---|:---:|
| Backstage | [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/), 대규모 플러그인 | 운영 복잡성, React/Node.js 필요 | 대형 |
| [Port](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) | [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/), 빠른 구축 | 비용, 커스터마이징 한계 | 중소형 |
| OpsLevel | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 성숙도 스코어카드 강점 | 가격 | 중형 |
| 직접 구축 | 완전한 커스터마이징 | 유지보수 비용 | 초대형 |

### [서비스 카탈로그](/knowledge-base/studynote/12_it_management/02_itsm_itil/088_service_catalog/) vs [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이 [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/)

| 항목 | Backstage [서비스 카탈로그](/knowledge-base/studynote/12_it_management/02_itsm_itil/088_service_catalog/) | [API Gateway](/knowledge-base/studynote/04_software_engineering/11_testing_validation/542_api_gateway/) [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) |
|:---|:---|:---|
| 대상 | 내부 개발자 | 외부/내부 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 소비자 |
| 정보 범위 | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 전체 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) | [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 스펙(OpenAPI) |
| 소유자 정보 | ✅ 팀·담당자 포함 | ❌ 미포함 |

📢 **섹션 요약 비유**: Backstage [서비스 카탈로그](/knowledge-base/studynote/12_it_management/02_itsm_itil/088_service_catalog/)는 회사 내부 전화번호부와 같다. 어떤 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 있는지, 누가 책임자인지, 어떻게 연락하는지([API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/)), 어떤 상태인지(health) 한눈에 볼 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**Backstage 도입 단계별 로드맵**:
```
Phase 1 (1~2개월): 서비스 카탈로그 구축
  - 기존 서비스에 catalog-info.yaml 추가
  - 소유자·의존성 맵 가시화

Phase 2 (2~3개월): 통합 플러그인 연결
  - GitHub Actions, PagerDuty, Datadog 통합
  - TechDocs로 문서 통합

Phase 3 (3~6개월): Software Templates 구축
  - 표준 서비스 생성 템플릿 (Spring Boot, FastAPI)
  - 자동화된 CI/CD 파이프라인 연결

Phase 4 (지속): 골든 패스 확장 및 DX 측정
  - 개발자 만족도 NPS 측정
  - 서비스 생성 소요 시간 추적
```

**기술사 판단 포인트**:
- Backstage의 가장 큰 도전은 [서비스 카탈로그](/knowledge-base/studynote/12_it_management/02_itsm_itil/088_service_catalog/)의 <strong>최신성 유지</strong>다. catalog-info.yaml 업데이트 의무화와 자동 스캔 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)이 필수다.
- 플러그인 수가 많아질수록 Backstage 운영 복잡성이 증가하므로, 처음에는 3~5개 핵심 플러그인만으로 시작한다.
- 기술적 성숙도 점수(TechScorecard)를 통해 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 표준 준수 여부를 가시화하면 자발적 개선을 유도한다.

📢 **섹션 요약 비유**: Backstage 도입 실패의 가장 흔한 원인은 "너무 한 번에 모든 것을 구현하려는 것"이다. [MVP](/knowledge-base/studynote/12_it_management/01_governance_strategy/036_mvp/)([서비스 카탈로그](/knowledge-base/studynote/12_it_management/02_itsm_itil/088_service_catalog/))부터 시작해서 개발자의 피드백으로 점진적으로 확장하는 것이 성공 패턴이다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 설명 |
|:---|:---|
| [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 가시성 | 전사 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 현황·의존성·소유자 즉시 파악 |
| 온보딩 가속 | 신규 팀원이 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 전체 구조 파악 시간 단축 |
| 표준화 강화 | Software Template로 신규 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 표준 자동 적용 |
| 도구 통합 | 여러 도구 탭 전환 없이 하나의 포털에서 작업 |

IDP는 [플랫폼 엔지니어링](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/109_platform_engineering_cognitive_load/)의 얼굴이다. 아무리 훌륭한 인프라를 구축해도 개발자가 사용하지 않으면 의미가 없다. Backstage는 [개발자 경험](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/058_dx_developer_experience/)([DX](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/726_platform_engineering_idp_dx/))을 중심에 두고, 조직의 모든 도구와 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 연결하는 <strong>개발자 생태계의 <a href="/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/">허브</a></strong>가 되는 것을 목표로 한다.

📢 **섹션 요약 비유**: IDP는 스마트폰의 홈 화면과 같다. 각 앱(도구)은 따로 존재하지만, 홈 화면([IDP](/knowledge-base/studynote/09_security/11_iam_access_control/536_idp_identity_provider/))을 통해 모든 앱을 하나의 인터페이스에서 접근할 수 있다. 개발자는 홈 화면만 알면 된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [플랫폼 엔지니어링](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/109_platform_engineering_cognitive_load/) | IDP는 [플랫폼 엔지니어링](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/109_platform_engineering_cognitive_load/)의 핵심 산출물 |
| 골든 패스 | Software Template으로 IDP에서 즉시 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 가능 |
| [CNCF](/knowledge-base/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) Backstage | 가장 널리 사용되는 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [IDP](/knowledge-base/studynote/09_security/11_iam_access_control/536_idp_identity_provider/) 프레임워크 |
| [서비스 카탈로그](/knowledge-base/studynote/12_it_management/02_itsm_itil/088_service_catalog/) | 전사 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 가시성의 핵심, catalog-info.yaml |
| [개발자 경험](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/058_dx_developer_experience/) ([DX](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/726_platform_engineering_idp_dx/)) | [IDP](/knowledge-base/studynote/09_security/11_iam_access_control/536_idp_identity_provider/) 성패를 결정하는 유일한 기준 |
| Team Topologies | IDP를 제공하는 Platform Team의 조직 설계 이론 |

### 👶 어린이를 위한 3줄 비유 설명

1. IDP는 학교 스마트패드처럼, 한 화면에서 숙제(GitHub), 수업 영상(Confluence), 성적(Datadog)을 모두 볼 수 있게 해줘.

### 📈 관련 키워드 및 발전 흐름도

```text
개발자: 여러 도구 분산 사용 (컨텍스트 스위칭)
    │
    ▼
IDP: 서비스 카탈로그 + 템플릿 + 문서 통합
    ├─► Backstage (Spotify 오픈소스)
    └─► 플러그인 생태계: K8s · CI/CD · 비용 연동
    │
    ▼
개발자 경험(DX) 극대화 → 생산성 향상
```
2. 새 친구(신규 입사자)가 와도 스마트패드만 켜면 학교 전체가 어떻게 돌아가는지 바로 알 수 있어.
3. 새 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 만들고 싶으면? 버튼 하나 누르면 표준 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)으로 서버가 뚝딱 생겨.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 199 / 371

← **이전**: [199. 플랫폼 엔지니어링 (Platform 엔진ering)](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/199_platform_engineering_idp_golden_path/)
**다음**: [201. DORA 메트릭스 (DORA Metrics)](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/201_dora_metrics_devops_performance/) →

---
