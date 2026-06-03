+++
title = "113. AWS SAM (Serverless Application Model) - CloudFormation 네이티브 FaaS 배포"
date = 2026-04-19

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: AWS SAM([Serverless](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) Application Model)은 <strong>CloudFormation의 확장 문법</strong>으로, [Lambda](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)·[API Gateway](/knowledge-base/studynote/04_software_engineering/11_testing_validation/542_api_gateway/)·[DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/)·Step Functions 등 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 리소스를 <strong>간결한 YAML로 선언</strong>하고 `sam deploy`로 배포하는 AWS 공식 [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) 도구다.
> 2. **가치**: CloudFormation으로 Lambda를 배포하면 50+ 줄 YAML이 필요하지만, SAM은 `AWS::Serverless::Function` 매크로로 <strong>10줄로 축약</strong>하며, `sam local invoke`로 <strong>로컬에서 Lambda를 <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/">Docker</a> 에뮬레이션</strong>하여 배포 전 테스트가 가능하다.
> 3. **판단 포인트**: SAM은 AWS 전용([벤더 종속](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/))이지만 CloudFormation 네이티브이므로 <strong>기존 CF <a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/">스택</a>과 완벽 호환</strong>되며, [Serverless](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) Framework(멀티클라우드)·SST(TypeScript 네이티브)와 비교하여 AWS 올인 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)에서 가장 자연스러운 선택이다.

---

## Ⅰ. 개요 및 필요성

CloudFormation으로 [Lambda](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) + [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) Gateway를 배포하려면 `AWS::Lambda::Function`, `AWS::Lambda::Permission`, `AWS::ApiGateway::RestApi`, `AWS::ApiGateway::Method` 등 <strong>5~10개 리소스를 각각 정의</strong>해야 한다.

```text
┌───────────────────────────────────────────────────────┐
│    CloudFormation vs SAM: 코드량 비교                  │
├───────────────────────────────────────────────────────┤
│  [CloudFormation 직접]                                │
│   Lambda Function:     15줄                           │
│   Lambda Permission:    8줄                           │
│   API Gateway RestApi: 10줄                           │
│   API Gateway Method:  12줄                           │
│   API Gateway Stage:    8줄                           │
│   IAM Role:            15줄                           │
│   합계: ~68줄                                         │
│                                                       │
│  [SAM]                                                │
│   AWS::Serverless::Function:                          │
│     Handler, Runtime, Events(Api) → 10줄              │
│   → SAM이 나머지를 CloudFormation으로 자동 변환       │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: CloudFormation이 레시피의 모든 재료와 조리법을 일일이 적는 요리책이라면, SAM은 "카레 세트"라고만 쓰면 재료가 자동으로 준비되는 밀키트다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### SAM 핵심 리소스 타입

| SAM 타입 | 확장 대상 | 자동 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 리소스 |
|:---|:---|:---|
| `AWS::Serverless::Function` | [Lambda](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) | [IAM](/knowledge-base/studynote/09_security/11_iam_access_control/526_iam/) Role, CloudWatch [Logs](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) |
| `AWS::Serverless::Api` | [API Gateway](/knowledge-base/studynote/04_software_engineering/11_testing_validation/542_api_gateway/) | RestApi, Stage, [Deployment](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/) |
| `AWS::Serverless::SimpleTable` | [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/) | 단일 키 테이블 |
| `AWS::Serverless::StateMachine` | Step Functions | 상태 머신 |

### SAM CLI 핵심 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)

| 명령 | 역할 |
|:---|:---|
| `sam init` | 프로젝트 스캐폴딩 |
| `sam build` | [종속성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 설치 + 패키징 |
| `sam local invoke` | <strong>로컬 Docker에서 <a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/">Lambda</a> 실행</strong> |
| `sam local start-api` | 로컬에서 [API Gateway](/knowledge-base/studynote/04_software_engineering/11_testing_validation/542_api_gateway/) 에뮬레이션 |
| `sam deploy --guided` | CloudFormation [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 배포 |

- **📢 섹션 요약 비유**: `sam local invoke`는 요리를 손님에게 내기 전 <strong>주방에서 맛보기</strong>하는 것이다.

---

## Ⅲ. 비교 및 연결

| 비교 | SAM | [Serverless](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) Framework | SST |
|:---|:---|:---|:---|
| **클라우드** | AWS 전용 | 멀티클라우드 | AWS 전용 |
| **기반** | CloudFormation | CF + 자체 플러그인 | CDK (TypeScript) |
| **로컬 테스트** | <strong>sam local (<a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/">Docker</a>)</strong> | [serverless](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)-offline | Live [Lambda](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) Dev |
| **생태계** | AWS 공식 | 플러그인 풍부 | TypeScript 네이티브 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 통합
```yaml
# GitHub Actions 예시
- run: sam build
- run: sam deploy --no-confirm-changeset --stack-name prod
```

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **SAM으로 비서버리스 리소스 관리**: EC2·RDS 등은 SAM이 아닌 CDK/CF로 관리하는 것이 적합.

---

## Ⅴ. 기대효과 및 결론

| 지표 | CF 직접 | SAM | 개선 |
|:---|:---|:---|:---|
| YAML 코드량 | 68줄 | **10줄** | 85% 감소 |
| 로컬 테스트 | 불가 | <strong><a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/">Docker</a> 에뮬레이션</strong> | 배포 전 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| 배포 속도 | 동일 | 동일 (CF 기반) | - |

SAM은 AWS의 공식 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) IaC로, CDK(Cloud Development Kit)와 통합하여 TypeScript/Python으로 SAM 템플릿을 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하는 **SAM + CDK 하이브리드** 패턴이 주류가 되고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **CloudFormation** | SAM의 기반, SAM 템플릿은 CF로 변환됨 |
| <strong><a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/">Lambda</a></strong> | SAM이 관리하는 핵심 컴퓨팅 리소스 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/542_api_gateway/">API Gateway</a></strong> | SAM Events로 자동 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되는 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 엔드포인트 |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/">Serverless</a> Framework</strong> | 멀티클라우드 경쟁 [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) 도구 |
| **CDK** | SAM과 통합하여 프로그래밍 언어로 인프라 정의 |

### 📈 관련 키워드 및 발전 흐름도

```text
[CloudFormation (2011) — AWS IaC 표준]
    │
    ▼
[AWS SAM (2016) — 서버리스 전용 CF 확장]
    │
    ▼
[SAM CLI (2018~) — 로컬 테스트·디버깅 지원]
    │
    ▼
[SAM + CDK 통합 (2021~) — TypeScript로 SAM 템플릿 생성]
    │
    ▼
[현재: SAM Accelerate — 핫 리로드, 빠른 개발 루프]
```

### 👶 어린이를 위한 3줄 비유 설명
1. CloudFormation은 레시피를 **재료부터 조리법까지 전부 적어야** 하는 두꺼운 요리책이에요.
2. SAM은 <strong>"카레 세트"</strong>라고만 쓰면 재료가 자동으로 준비되는 편리한 밀키트예요!
3. `sam local`은 손님에게 내기 전 <strong>주방에서 맛보기</strong>하는 것처럼, 배포 전에 테스트할 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 113 / 373

← **이전**: [112. 서버리스 프레임워크 배포 (Serverless Framework Deployment) - FaaS IaC 자동화](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/112_serverless_framework_deployment/)
**다음**: [114. Kayenta 카나리 분석 (Kayenta Canary Analysis) - 자동 배포 판단·ACA](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/114_kayenta_canary_analysis/) →

---
