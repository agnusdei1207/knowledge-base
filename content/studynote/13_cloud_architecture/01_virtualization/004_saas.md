---
title: "Google Workspace, Salesforce"
date: "2024-05-24"
tags:
  - "cloud_architecture"
  - "studynote-cloud-architecture"
weight: 4
---
# [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) (Software [as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: SaaS는 IaaS와 [PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) 인프라 위에서 구동되는 '완제품 소프트웨어'를 인터넷 브라우저나 API를 통해 최종 사용자에게 구독(Subscription) 형태로 제공하는 클라우드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 모델이다.
> 2. **가치**: 소프트웨어의 설치, 라이선스 관리, 패치 업데이트 책임을 사용자에서 [CSP](/studynote/09_security/05_web_app_security/475_csp/)(클라우드 제공자)로 완전히 이전하여, [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 도입 비용을 없애고 글로벌 어디서나 즉각적인 협업을 가능케 한다.
> 3. **융합**: SaaS의 백엔드는 수만 명의 고객(Tenant)이 동일한 애플리케이션 인스턴스를 공유하면서도 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 완벽히 격리되는 <strong><a href="/studynote/13_cloud_architecture/01_virtualization/014_multi_tenancy/">멀티 테넌시</a>(<a href="/studynote/13_cloud_architecture/01_virtualization/014_multi_tenancy/">Multi-Tenancy</a>)</strong> [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 설계와 강력한 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)([IAM](/studynote/09_security/11_iam_access_control/526_iam/)/[SSO](/studynote/09_security/11_iam_access_control/531_sso/)) 아키텍처가 결합되어야만 비즈니스 이윤을 창출할 수 있다.

---

### Ⅰ. 개요 및 필요성 ([Context](/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

[SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) (Software [as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))는 [클라우드 컴퓨팅](/studynote/02_operating_system/01_overview_architecture/052_cloud_computing_os/) 스택의 가장 꼭대기(최상위 계층)에 위치하며, 비 IT 직군을 포함한 모든 일반 소비자와 기업 고객이 일상적으로 접하는 클라우드 형태다. 대표적인 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 Google Workspace(문서/메일), Salesforce([CRM](/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/)), Slack(메신저), Zoom 등이 있다.

과거 '패키지 소프트웨어([On-Premise](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) Software)' 시대에는 기업이 MS 오피스나 [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) 시스템을 도입하려면 막대한 라이선스 비용(CapEx)을 지불하고, CD/DVD로 설치한 뒤, 사내 IT 직원이 일일이 버전을 업그레이드하고 보안 패치를 적용해야 했다. 이로 인해 부서마다 사용하는 S/W 버전이 달라 [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 문제가 빈번했고, 사무실 밖(외부 네트워크)에서는 시스템에 접근조차 어려웠다. SaaS는 이 소프트웨어 소유의 개념을 '접속(Access)'과 '구독(Subscription)'으로 혁신하여 유지보수의 수고를 제로(0)로 만들었다.

다음은 레거시 패키지 소프트웨어와 현대 SaaS의 사용자 경험(UX) 및 관리 흐름을 비교한 도식이다.

```text
[과거 패키지 소프트웨어 (On-Premise S/W) 흐름]
라이선스 대량 구매 -> IT팀: 직원 PC마다 설치 파일 배포 -> 개별 로컬 디스크에 데이터 저장 -> 수동 업데이트 패치
                   ^ (버전 파편화 및 외부 협업 불가능 병목)

[현재 SaaS (Cloud S/W) 흐름]
월 구독료 결제 -> 브라우저 로그인(SSO) -> 즉시 서비스 이용 & 중앙 클라우드에 데이터 동기화 -> 벤더가 백그라운드 무중단 업데이트
                   ^ (설치/관리 제로, 실시간 글로벌 협업 가능)
```

이 흐름도의 핵심은 소프트웨어의 실행 환경이 사용자의 로컬 단말기에서 클라우드의 중앙 서버로 완전히 이동했다는 점이다. 사용자의 PC나 스마트폰은 껍데기(Thin [Client](/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/)) 역할만 하고 무거운 연산과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장은 모두 [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) 벤더의 서버에서 처리된다. 따라서 사용자 단말기의 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 제약에서 해방되며, 중앙에서 기능이 업데이트되면 전 세계 수백만 명의 사용자가 새로고침 한 번으로 최신 기능을 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)받게 된다. 실무적으로 이는 섀도우 IT([Shadow IT](/studynote/12_it_management/01_governance_strategy/049_shadow_it/), 현업 부서가 IT팀 몰래 SaaS를 도입하는 현상)를 유발할 만큼 압도적인 편의성을 지닌다.

📢 **섹션 요약 비유**: 옛날에는 비싼 영화 DVD를 사서 집에 있는 플레이어에 넣고 봐야 했지만(패키지 S/W), 지금은 넷플릭스([SaaS](/studynote/12_it_management/05_security_compliance/951_saas/))에 매월 돈만 내면 인터넷이 되는 기기 어디서든, 업데이트된 최신 영화를 즉시 감상할 수 있는 것과 같습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

[SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) 아키텍처의 수익성을 결정짓는 가장 핵심적인 내부 원리는 <strong><a href="/studynote/13_cloud_architecture/01_virtualization/014_multi_tenancy/">멀티 테넌시</a> (<a href="/studynote/13_cloud_architecture/01_virtualization/014_multi_tenancy/">Multi-Tenancy</a>)</strong>이다. 수많은 고객사(Tenant)마다 서버를 따로 구축해 주면(Single-Tenant), 클라우드 벤더는 인프라 비용과 관리 비용을 감당할 수 없다.

| 구성 요소 | 역할 | 내부 설계/동작 메커니즘 | 실무 설계 과제 | 비유 |
|:---|:---|:---|:---|:---|
| **애플리케이션 계층** | 모든 테넌트가 동일한 소스코드/인스턴스 공유 | 논리적인 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)으로 사용자 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/). 코드는 하나, UI/설정만 테넌트별 동적 렌더링 | 무중단 전역 배포 파이프라인 | 하나의 거대한 오피스 빌딩 |
| <strong><a href="/studynote/03_network/17_sdn_nfv/888_multi_tenant_cloud_resource_isolation_noisy_neighbor/">멀티 테넌트</a> DB 계층</strong> | 고객(Tenant) 간 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 격리와 저장 | 1) DB 분리 2) [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 분리 3) 테이블 내 Tenant ID 컬럼 분리 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 프라이버시, 노이지 네이버 방어 | 빌딩 내 호수별 프라이빗 창고 |
| <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a> 및 <a href="/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/">인가</a> (<a href="/studynote/09_security/11_iam_access_control/526_iam/">IAM</a> / <a href="/studynote/09_security/11_iam_access_control/531_sso/">SSO</a>)</strong> | 권한 통제 및 보안 경계 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | SAML, OAuth 2.0 기반으로 고객사의 기존 AD([Active Directory](/studynote/09_security/11_iam_access_control/548_active_directory/))와 연동 통합 | [제로 트러스트](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)([Zero Trust](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)) [접근 통제](/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/) | 중앙 안내 데스크의 신분증 검사 |
| **미터링 및 과금 엔진** | 구독 플랜 기반 자원 사용량 통제 | [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호출 수, 활성 사용자 수, 스토리지 용량을 실시간 수집해 Tier(Free, Pro) 제어 | Stripe, Chargebee 등 빌링 연동 | 호수별 전기/수도 계량기 |

다음 구조도는 [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) 백엔드에서 하나의 애플리케이션 인스턴스가 여러 고객사의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 어떻게 격리하고 처리하는지([멀티 테넌시](/studynote/13_cloud_architecture/01_virtualization/014_multi_tenancy/) 모델)를 보여준다.

```text
이 도식은 비용 효율성이 가장 높은 최고 난이도의 SaaS DB 설계인 '공유 DB - 공유 스키마 (Shared DB - Shared Schema)' 방식을 보여준다.

+-------------- [SaaS Application Instance / SaaS 인스턴스] --------------+
|  [사용자 A (고객사 X)]         [사용자 B (고객사 Y)]      |
|          |                              |                 |
|          v (요청 시 Tenant ID = X 포함) v (Tenant ID = Y) |
|  +--------------------------------------------------+     |
|  |    [ Authentication & Authorization Filter ]     |     |
|  |    [ Tenant Context Resolver (Tenant 인식기) ]   |     |
|  +-----------------------|--------------------------+     |
+--------------------------|--------------------------------+
                           v (SQL 쿼리에 WHERE Tenant_ID 조건 강제 삽입)
+-------------- [ Multi-Tenant Database (공유 DB) ] --------+
|  [ Table : Users ]                                        |
|  Row 1: [Tenant: X] [Name: Alice] [Data: ...]             |
|  Row 2: [Tenant: X] [Name: Bob]   [Data: ...]             |
|  Row 3: [Tenant: Y] [Name: Charlie] [Data: ...]           |
|                                                           |
|  * DB 엔진 레벨의 RLS (Row-Level Security) 통제로 누출 원천 차단 *
+-----------------------------------------------------------+
```

이 구조도의 핵심은 고객사 X와 Y가 물리적으로 같은 DB의 같은 테이블에 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 쓰지만, 애플리케이션 프레임워크와 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)의 로우 레벨 보안(RLS) 정책이 결합하여 서로의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 절대 볼 수 없도록 논리적으로 완벽히 격리한다는 점이다. 만약 개발자의 코딩 실수로 `WHERE Tenant_ID = X` 조건이 누락되면, 고객사 Y의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 A에게 노출되는 치명적인 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 침해([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Breach)가 발생한다. 따라서 실무에서는 ORM(Object-Relational [Mapping](/studynote/05_database/01_db_architecture_relational/010_schema_mapping/)) 레벨이나 DB 엔진 레벨에서 테넌트 필터링을 강제로 주입하는 글로벌 인터셉터(Interceptor) 패턴을 반드시 아키텍처 베이스에 박아두어야 한다.

📢 **섹션 요약 비유**: [멀티 테넌시](/studynote/13_cloud_architecture/01_virtualization/014_multi_tenancy/) SaaS는 대형 은행의 공용 금고실과 같습니다. 모든 고객의 돈([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))이 물리적으로는 한 공간(동일 DB)에 모여 있지만, 각자의 고유한 지문 인식과 열쇠(Tenant ID와 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/))가 있어야만 정확히 자신의 서랍장(Row)만 열 수 있도록 철저히 통제됩니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

[SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) 비즈니스를 영위하거나 도입할 때, [멀티 테넌시](/studynote/13_cloud_architecture/01_virtualization/014_multi_tenancy/)의 3가지 DB 격리 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 명확히 비교하여 트레이드오프를 결정해야 한다.

| [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) DB 격리 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 구조적 특징 | 장점 (벤더 입장) | 단점 및 병목 | 실무 판단 포인트 |
|:---|:---|:---|:---|:---|
| <strong>1. <a href="/studynote/05_database/04_transactions_concurrency/501_database/">Database</a> per Tenant</strong><br>(격리 DB 모델) | 고객사마다 물리적 DB 서버(또는 인스턴스)를 1개씩 별도 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 완벽한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 격리, 특정 고객 트래픽 폭주가 타 고객에 영향 없음 | 인프라 비용 폭발, 수천 개 DB [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 업데이트의 지옥 | 극도의 보안(금융/의료)을 요구하는 대형 엔터프라이즈 고객용 |
| <strong>2. <a href="/studynote/05_database/04_transactions_concurrency/505_schema/">Schema</a> per Tenant</strong><br>(공유 DB, 격리 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)) | 1개 DB 내에 고객사별로 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)(Table Set)를 별도 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 컴퓨팅 비용 절감, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 논리적 분리로 어느 정도 보안 안심 | DB당 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)(테이블) 개수 한계 존재, 여전한 업데이트 부담 | B2B 중심의 중간 규모 [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 적합 |
| <strong>3. Shared DB / Shared <a href="/studynote/05_database/04_transactions_concurrency/505_schema/">Schema</a></strong><br>(완전 공유 모델) | 모든 고객이 같은 DB, 같은 테이블에 Tenant_ID만 구분해 적재 | 인프라 리소스 활용 최적화, [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 업데이트가 1번이면 끝남 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유출 [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 최고, 노이지 네이버 현상 심각 ([성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 간섭) | B2C 기반 수백만 명 대상의 저비용/고확장성 [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) (Notion 등) |

다음은 기업이 내부 시스템을 구축할 때 SaaS와 [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)/IaaS를 선택하는 기준을 보여주는 의사결정 비교도이다.

```text
이 매트릭스는 기업의 '데이터 보안 민감도'와 '핵심 비즈니스 차별화' 여부에 따라 도입해야 할 시스템의 형태를 분류한다.

+----------------+--------------------------------+---------------------------+
| 비즈니스 특성  | 높은 보안 & 차별화 핵심 로직   | 표준화 & 비차별화 로직      |
+----------------+--------------------------------+---------------------------+
| 예시 시스템    | 자체 결제 알고리즘, 핵심 설계도| 사내 메일, 화상회의, 경비처리|
+----------------+--------------------------------+---------------------------+
| 최적 도입 모델 | IaaS/PaaS 기반 자체 Custom 개발| SaaS 구독 (Google Work, SAP)|
+----------------+--------------------------------+---------------------------+
| 의사결정 사유  | 경쟁 우위 원천이므로 통제권 확보| 여기서 혁신해봤자 의미 없음.|
|                | 벤더 종속 회피 및 데이터 내재화| 즉시 도입하고 관리비용 절약 |
+----------------+--------------------------------+---------------------------+
```

기업의 모든 시스템을 직접 개발([IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/)/[PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/))하는 것은 거대한 낭비다. 이메일, 근태 관리, 일반 회계처럼 회사 간 차별성이 없는 표준(Standard) 업무는 검증된 글로벌 SaaS를 즉시 도입하여 IT 인력의 에너지를 아끼는 것이 올바른 IT [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다. 반대로, 배달의민족의 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 알고리즘처럼 회사의 심장(Core)이 되는 시스템을 상용 SaaS에 의존하면 비즈니스 확장에 치명적 한계를 맞이하게 된다.

📢 **섹션 요약 비유**: 회사의 핵심 비밀 레시피(차별화 로직)를 만드는 주방은 직접 돈을 들여 구축([IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/))해야 하지만, 직원들이 마실 믹스 커피와 정수기(표준 업무)는 굳이 직접 만들지 않고 렌탈 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)([SaaS](/studynote/12_it_management/05_security_compliance/951_saas/))를 구독하는 것이 현명한 기업 운영입니다.

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

SaaS를 기업에 전사적으로 도입하거나 [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) 아키텍처를 설계할 때는 보안과 통합(Integration) 관점의 방어적 실무 적용이 필수적이다.

1. <strong>섀도우 IT (<a href="/studynote/12_it_management/01_governance_strategy/049_shadow_it/">Shadow IT</a>) 및 <a href="/studynote/09_security/16_data_privacy/809_data_sovereignty/">데이터 주권</a> 통제</strong>: SaaS는 접근이 너무 쉽기 때문에, 마케팅 부서가 IT 부서 모르게 고객 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 외부 [CRM](/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/) [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/)(예: Hubspot)에 올려버리는 경우가 많다. 이는 [개인정보보호법](/studynote/09_security/16_data_privacy/783_pipa_korea/)([GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/)/망법) 위반으로 이어진다. 실무에서는 [CASB](/studynote/03_network/14_network_security_threats/741_casb_cloud_access_security_broker/)(Cloud Access [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Broker) 솔루션을 사내망에 도입하여, 비인가 [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) 접속을 탐지/차단하고 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유출([DLP](/studynote/01_computer_architecture/10_parallel_processing_architecture/386_dlp/))을 방어해야 한다.
2. <strong><a href="/studynote/09_security/11_iam_access_control/531_sso/">SSO</a>(<a href="/studynote/09_security/11_iam_access_control/531_sso/">Single Sign-On</a>) 및 권한 연동</strong>: 10개의 SaaS를 쓰면 임직원은 10개의 비밀번호를 기억해야 하고, 퇴사자 발생 시 10곳에서 계정을 지워야 한다(보안 구멍). 반드시 SAML 2.0이나 OAuth 기반의 사내 중앙 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)망([Active Directory](/studynote/09_security/11_iam_access_control/548_active_directory/), [Okta](/studynote/09_security/11_iam_access_control/551_okta_idaas/) 등)과 SaaS를 연동하여, 한 번의 로그인으로 접근하고 퇴사 시 즉시 전면 차단되는 [프로비저닝](/studynote/09_security/11_iam_access_control/528_provisioning/)(SCIM) 파이프라인을 구축해야 한다.
3. <strong><a href="/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a> 한도 (<a href="/studynote/09_security/05_web_app_security/520_rate_limiting/">Rate Limiting</a>) 및 <a href="/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/">백업</a></strong>: [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 '클라우드에 있으니 안전하겠지'라고 착각하지만, CSP의 장애나 [랜섬웨어](/studynote/09_security/15_malware_attack_vectors/730_ransomware/) 암호화 시 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 책임은 사용자에게 있다(공동 책임 모델). SaaS가 제공하는 Open API를 호출하여 주기적으로 로컬 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 레이크로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)하는 [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 파이프라인을 구성해야 하며, 이때 [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) 벤더의 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) Throttling(초당 호출 제한) 한도를 넘지 않도록 큐([Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/))를 설계해야 한다.

```text
[실무 SaaS 보안 통합 인증(SSO) 및 통제 아키텍처]
이 흐름도는 사내 직원이 외부 SaaS에 안전하게 접근하기 위한 제로 트러스트(Zero Trust) 및 연동 흐름을 보여준다.

[직원 단말 (Laptop)]
      v (1. 접근 시도)
+-----[ 사내 보안 프록시 (CASB / SWG) ]------+ --(비인가 SaaS 접속은 즉시 Drop 차단)
|     v (2. 트래픽 허용 및 인증 확인)        |
| [ 중앙 Identity Provider (Okta, AD) ]      | --(3. SAML Token 발행 및 2FA/MFA 검증)
+-----|--------------------------------------+
      v (4. 검증된 토큰 들고 접속)
+-----[ 외부 SaaS Provider (Salesforce) ]----+
| [SSO Endpoint / SSO 엔드포인트] -> 유효성 확인 후 로그인 승인|
| [API Gateway / API 게이트웨이] <- 사내 백업 서버에서 데이터 추출
+--------------------------------------------+
```

이 운영 플로우의 핵심은 SaaS라는 외부 블랙박스를 사내 IT 거버넌스의 통제망 안으로 강제로 끌고 들어오는 것이다. CASB를 통한 가시성 확보와 [IdP](/studynote/09_security/11_iam_access_control/536_idp_identity_provider/)([Identity Provider](/studynote/09_security/11_iam_access_control/536_idp_identity_provider/))를 통한 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 중앙화 없이는, [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) 도입이 오히려 기업의 보안 공격 표면(Attack Surface)을 기하급수적으로 넓히는 재앙이 된다.

📢 **섹션 요약 비유**: SaaS는 문이 수십 개 달린 외부 공유 오피스와 같습니다. 중앙 경비실([SSO](/studynote/09_security/11_iam_access_control/531_sso/) [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/))에서 발급한 출입증 하나로만 모든 방을 열 수 있게 통제하고, 물건을 빼내 갈 때 엑스레이 검사([CASB](/studynote/03_network/14_network_security_threats/741_casb_cloud_access_security_broker/))를 거치지 않으면 보안 사고를 막을 수 없습니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)

SaaS의 도입은 비즈니스의 운영 방식을 거대한 설치(Installation)의 시대에서 가벼운 연결(Connection)의 시대로 전환시켰다. 이를 통해 기업 본연의 핵심 비즈니스 집중도를 극대화할 수 있다.

| 지표 | 패치형 소프트웨어 도입 전 | [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) 전환 후 기대효과 |
|:---|:---|:---|
| [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 도입 비용 (CapEx) | 막대한 라이선스 구매비 선지출 | 제로(0), 매월 구독료(OpEx)로 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 지출 |
| 유지보수 및 패치 시간 | IT 부서의 야간/주말 수동 패치 | 벤더 자동 업데이트 (투입 리소스 0) |
| 확장성 및 [접근성](/studynote/04_software_engineering/05_devops_ci_cd/292_accessibility_kwcag_wcag/) | [VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) 없이는 사외 접근 및 모바일 불가 | 웹 브라우저만 있으면 전 세계 어디서든 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) |

[SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) 생태계는 향후 버티컬 [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/)(Vertical [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/), 특정 산업군이나 도메인에 극도로 특화된 [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/), 예: 제약 산업 전용 [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/))와 AI가 결합된 지능형 [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/)(예: 문서를 알아서 요약해 주는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) Copilot 내재화)로 진화하고 있다. 결론적으로 [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) 아키텍처는 [멀티 테넌시](/studynote/13_cloud_architecture/01_virtualization/014_multi_tenancy/) 기반의 압도적인 비용 효율성을 무기로 B2B 소프트웨어 시장을 완전히 장악했으며, 클라우드의 경제적 가치를 비 IT 직군에게까지 가장 직관적으로 전달하는 최전선의 기술로 자리매김했다.

📢 **섹션 요약 비유**: SaaS는 더 이상 소프트웨어를 '소유물'로 보지 않고 전기나 수도 같은 '유틸리티'로 보는 클라우드 철학의 최종 완성본입니다. 꽂고 켜면(Plug and Play) 혁신은 즉시 시작됩니다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- [멀티 테넌시](/studynote/13_cloud_architecture/01_virtualization/014_multi_tenancy/) ([Multi-Tenancy](/studynote/13_cloud_architecture/01_virtualization/014_multi_tenancy/)) | 하나의 인스턴스를 다수 고객이 논리적으로 분리/공유해 쓰는 [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) 핵심 아키텍처
- [CASB](/studynote/03_network/14_network_security_threats/741_casb_cloud_access_security_broker/) (Cloud Access [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Broker) | 임직원의 [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) 접속 트래픽을 감시하여 보안 및 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유출을 통제하는 게이트웨이
- [SSO](/studynote/09_security/11_iam_access_control/531_sso/) ([Single Sign-On](/studynote/09_security/11_iam_access_control/531_sso/)) & SAML | 한 번의 로그인으로 수십 개의 [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) 앱에 안전하게 접근하는 중앙 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)
- 섀도우 IT ([Shadow IT](/studynote/12_it_management/01_governance_strategy/049_shadow_it/)) | IT 부서 승인 없이 현업 부서가 임의로 SaaS를 결제/사용하여 발생하는 보안 사각지대
- [웹훅](/studynote/03_network/09_application_layer_web_email/498_webhook_rest_api_reverse_callback/) ([Webhook](/studynote/03_network/09_application_layer_web_email/498_webhook_rest_api_reverse_callback/)) & [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 연동 | 분리된 이기종 [SaaS](/studynote/12_it_management/05_security_compliance/951_saas/) [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간에 이벤트 발생 시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 실시간 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)하는 이벤트 주도 통합망

### 📈 관련 키워드 및 발전 흐름도

```text
[멀티 테넌시 (Multi-Tenancy)]
    |
    v
[CASB (Cloud Access Security Broker)]
    |
    v
[SSO (Single Sign-On) & SAML]
    |
    v
[섀도우 IT (Shadow IT)]
    |
    v
[웹훅 (Webhook) & API 연동]
```

이 흐름도는 [멀티 테넌시](/studynote/13_cloud_architecture/01_virtualization/014_multi_tenancy/) ([Multi-Tenancy](/studynote/13_cloud_architecture/01_virtualization/014_multi_tenancy/))에서 출발해 [웹훅](/studynote/03_network/09_application_layer_web_email/498_webhook_rest_api_reverse_callback/) ([Webhook](/studynote/03_network/09_application_layer_web_email/498_webhook_rest_api_reverse_callback/)) & [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 연동까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 예전에는 게임을 하려면 CD를 사서 컴퓨터에 힘들게 깔아야만 할 수 있었어요.
2. SaaS는 스마트폰에서 앱스토어나 인터넷 창만 켜면 설치 없이 바로 할 수 있는 재미있는 게임이나 그림 그리기 도구예요.
3. 만드는 아저씨들이 오류도 다 알아서 고쳐주니까, 우리는 언제 어디서나 편하게 로그인해서 즐기기만 하면 된답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 3 / 371

<- **이전**: [3. PaaS (Platform as a Service) - OS, 런타임, 미들웨어, DB가 세팅된 개발/운영 플랫폼 제공 (AWS](/studynote/13_cloud_architecture/01_virtualization/003_paas/)
**다음**: [5. BaaS (Backend as a Service) - 모바일/웹 앱을 위한 공통 백엔드 API (인증, 푸시, DB) 제공 (Firebase)](/studynote/13_cloud_architecture/01_virtualization/005_baas/) ->

---
