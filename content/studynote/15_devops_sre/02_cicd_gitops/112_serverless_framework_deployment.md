---
title: "112. Serverless Framework Deployment"
date: "2026-04-19"
tags:
  - "studynote-devops-sre"
weight: 112
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [Serverless](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) Framework는 AWS [Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)·Azure Functions·GCP Cloud Functions 등 <strong><a href="/studynote/12_it_management/05_security_compliance/342_faas/">FaaS</a>(Function <a href="/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/">as</a> a <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">Service</a>)의 인프라·코드·이벤트 <a href="/studynote/05_database/04_transactions_concurrency/507_acid_properties/">트리거</a>를 <code>serverless.yml</code> 하나로 선언</strong>하고, `sls deploy` 한 줄로 클라우드에 배포하는 [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)([Infrastructure as Code](/studynote/15_devops_sre/02_cicd_gitops/062_infrastructure_as_code/)) 도구다.
> 2. **가치**: [Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) 함수 1개를 수동 배포하려면 [IAM](/studynote/09_security/11_iam_access_control/526_iam/) Role·[API Gateway](/studynote/04_software_engineering/11_testing_validation/934_api_gateway/)·CloudWatch·DLQ를 콘솔에서 각각 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)해야 하지만, [Serverless](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) Framework는 YAML 선언만으로 <strong>모든 종속 리소스를 CloudFormation <a href="/studynote/08_algorithm_stats/04_datastructure/057_stack/">스택</a>으로 자동 <a href="/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a></strong>한다.
> 3. **판단 포인트**: [Serverless](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) Framework(범용)·[AWS SAM](/studynote/15_devops_sre/02_cicd_gitops/113_aws_sam_serverless_model/)(AWS 전용)·SST(TypeScript 네이티브)의 트레이드오프를 이해하고, <strong><a href="/studynote/06_ict_convergence/05_data_science/347_cold_start_problem/">Cold Start</a> 최적화·<a href="/studynote/02_operating_system/04_synchronization/229_monitor/">모니터</a>링 통합·<a href="/studynote/12_it_management/02_itsm_itil/874_configuration_item/">CI</a>/CD <a href="/studynote/02_operating_system/02_process_thread/123_pipe/">파이프</a>라인 연결</strong>까지 고려해야 프로덕션 수준이 된다.

---

## Ⅰ. 개요 및 필요성

FaaS는 서버 관리 없이 함수 단위로 코드를 실행하지만, 실제 배포 시에는 <strong><a href="/studynote/09_security/11_iam_access_control/526_iam/">IAM</a> <a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a>·<a href="/studynote/04_software_engineering/11_testing_validation/934_api_gateway/">API Gateway</a> 엔드포인트·DLQ(Dead Letter <a href="/studynote/08_algorithm_stats/04_datastructure/058_queue/">Queue</a>)·<a href="/studynote/03_network/16_data_center_cloud/836_vpc_virtual_private_cloud_subnet_isolation/">VPC</a> <a href="/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a>·<a href="/studynote/02_operating_system/02_process_thread/156_environment_variables/">환경 변수</a></strong> 등 수십 가지 인프라를 구성해야 한다.

```text
+-------------------------------------------------------+
|    수동 배포 vs Serverless Framework 배포               |
+-------------------------------------------------------+
|  [수동 배포]                                          |
|   AWS 콘솔 -> Lambda 생성 -> IAM Role 설정             |
|   -> API Gateway 연동 -> CloudWatch 설정               |
|   -> DLQ 연결 -> 환경 변수 -> (30분+)                   |
|                                                       |
|  [Serverless Framework]                               |
|   serverless.yml 작성 -> sls deploy -> 끝!             |
|   모든 리소스가 CloudFormation으로 자동 생성           |
|   (3분)                                               |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 수동 배포는 레고 설명서 없이 100조각을 맞추는 것이고, [Serverless](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) Framework는 설명서(YAML) 대로 로봇이 자동으로 조립하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [serverless](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/).yml 핵심 구조

```yaml
service: my-api
provider:
  name: aws
  runtime: nodejs20.x
  region: ap-northeast-2
functions:
  hello:
    handler: handler.hello
    events:
      - http:
          path: /hello
          method: get
    timeout: 10
    memorySize: 256
```

### 프레임워크 비교

| 도구 | 멀티클라우드 | 언어 | 특징 |
|:---|:---|:---|:---|
| <strong><a href="/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/">Serverless</a> Framework</strong> | ✅ (AWS/Azure/GCP) | YAML | 범용, 플러그인 생태계 풍부 |
| <strong><a href="/studynote/15_devops_sre/02_cicd_gitops/113_aws_sam_serverless_model/">AWS SAM</a></strong> | AWS 전용 | YAML | CloudFormation 네이티브 |
| **SST (v3)** | AWS 전용 | TypeScript | 타입 안전, 핫 리로드 |
| **Pulumi** | ✅ | 범용 언어 | 코드로 인프라 (TypeScript/Python) |

- **📢 섹션 요약 비유**: [Serverless](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) Framework는 만능 리모컨(멀티클라우드)이고, SAM은 삼성 TV 전용 리모컨이며, SST는 스마트폰 앱(타입 안전)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 수동 콘솔 | [Serverless](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) Framework |
|:---|:---|:---|
| **배포 시간** | 30분+ | **3분** |
| **재현성** | 수동 (실수 위험) | **YAML 선언, 100% 재현** |
| <strong><a href="/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/">버전</a> 관리</strong> | 불가 | <strong>Git으로 <a href="/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/">IaC</a> 이력 관리</strong> |
| <strong><a href="/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/">롤백</a></strong> | 수동 복원 | <strong>sls <a href="/studynote/02_operating_system/05_deadlock/313_rollback/">rollback</a> (자동)</strong> |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD 통합 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. **GitHub Actions**: `on: push` -> `sls deploy --stage prod`.
2. **스테이지 분리**: `--stage dev/staging/prod`로 환경별 독립 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/).
3. <strong><a href="/studynote/06_ict_convergence/05_data_science/347_cold_start_problem/">Cold Start</a> 최적화</strong>: [Provisioned Concurrency](/studynote/06_ict_convergence/03_cloud_infrastructure/202_provisioned_concurrency_serverless_cold_start/) 또는 WarmUp 플러그인.
4. <strong><a href="/studynote/02_operating_system/04_synchronization/229_monitor/">모니터</a>링</strong>: [Serverless](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) Dashboard 또는 Datadog [Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) Layer.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **단일 거대 함수**: [Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) 1개에 모든 로직 -> 모놀리스 회귀. 함수별 [단일 책임 원칙](/studynote/11_design_supervision/06_exam_summary/355_process/) 준수.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 수동 배포 | [Serverless](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) Framework | 개선 |
|:---|:---|:---|:---|
| 배포 시간 | 30분+ | **3분** | 90% 단축 |
| 인프라 재현성 | 낮음 | **100%** | [IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) 확보 |
| 운영 비용 | 인스턴스 상시 과금 | **요청당 과금** | 유휴 비용 0 |

[Serverless](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) Framework v4는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 자동 최적화(메모리·[타임아웃](/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) 자동 튜닝)를 내장하여, 함수 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 비용의 최적점을 자동으로 찾아주는 방향으로 진화하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/12_it_management/05_security_compliance/342_faas/">FaaS</a> (<a href="/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/">Lambda</a>)</strong> | [Serverless](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) Framework가 배포하는 대상 |
| <strong><a href="/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/">IaC</a> (<a href="/studynote/15_devops_sre/02_cicd_gitops/062_infrastructure_as_code/">Infrastructure as Code</a>)</strong> | YAML 선언으로 인프라를 코드화 |
| **CloudFormation** | AWS에서 YAML -> 실제 리소스 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 엔진 |
| <strong><a href="/studynote/04_software_engineering/11_testing_validation/934_api_gateway/">API Gateway</a></strong> | [Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/), [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 엔드포인트 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| <strong><a href="/studynote/06_ict_convergence/05_data_science/347_cold_start_problem/">Cold Start</a></strong> | [FaaS](/studynote/12_it_management/05_security_compliance/342_faas/) 최초 실행 시 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 최적화 필수 |

### 📈 관련 키워드 및 발전 흐름도

```text
[AWS Lambda 출시 (2014) — FaaS 개념 탄생]
    |
    v
[Serverless Framework (2015) — FaaS IaC 자동화]
    |
    v
[AWS SAM (2016) — AWS 전용 FaaS 배포 도구]
    |
    v
[SST (2021~) — TypeScript 네이티브, 핫 리로드]
    |
    v
[현재: AI 기반 자동 튜닝 — 메모리·타임아웃 최적화 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 옛날에는 레고를 만들 때 <strong>설명서 없이 100조각</strong>을 혼자 맞춰야 했어요.
2. [Serverless](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) Framework는 <strong>설명서(YAML)</strong>를 주면 로봇이 자동으로 조립해줘요!
3. 덕분에 개발자는 레고 디자인(코드)에만 집중하고, 조립(배포)은 로봇에게 맡길 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 112 / 373

<- **이전**: [111. 마이크로 프론트엔드 배포 (Micro Frontends Deployment) - 독립 배포·Module Federation](/studynote/15_devops_sre/02_cicd_gitops/111_micro_frontends_deployment/)
**다음**: [113. AWS SAM (Serverless Application Model) - CloudFormation 네이티브 FaaS 배포](/studynote/15_devops_sre/02_cicd_gitops/113_aws_sam_serverless_model/) ->

---
