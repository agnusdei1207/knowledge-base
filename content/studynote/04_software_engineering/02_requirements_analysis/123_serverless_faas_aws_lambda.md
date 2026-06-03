+++
title = "123. 서버리스 & FaaS (Serverless / AWS Lambda) - 인프라 없는 함수 단위 컴퓨팅"
date = 2026-04-19

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)([Serverless](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/))는 <strong>서버 <a href="/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/">프로비저닝</a>·관리 없이 코드만 배포하면 클라우드가 자동 실행·<a href="/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/">스케일링</a>·과금</strong>하는 컴퓨팅 모델이며, [FaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/)(Function [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))는 <strong>함수 단위로 실행</strong>되는 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)의 대표 형태이다.
> 2. **가치**: [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)·K8s는 서버 관리(패치·[스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/))가 필요하지만, [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)는 <strong>코드만 작성하면 실행 횟수·시간 기반으로 과금</strong>되어 유휴 비용이 0이다.
> 3. **판단 포인트**: <strong><a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/347_cold_start_problem/">Cold Start</a>(첫 실행 <a href="/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a>)</strong>·**실행 시간 제한(15분)**·<strong>상태 비저장(<a href="/knowledge-base/studynote/15_devops_sre/05_devsecops/239_stateless_redis/">Stateless</a>)</strong>의 제약이 있으므로, 이벤트 기반 단기 작업에 적합하고 장기 실행·상태 유지 워크로드에는 부적합하다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    서버리스 실행 모델                                  │
├───────────────────────────────────────────────────────┤
│  [이벤트 발생]                                        │
│   API Gateway 요청 / S3 업로드 / SNS 메시지           │
│      │                                                │
│      ▼                                                │
│  [Lambda 함수 실행]                                    │
│   → 코드 실행 (최대 15분)                            │
│   → 결과 반환                                         │
│   → 실행 종료 (유휴 시 과금 0)                       │
│                                                       │
│  자동 스케일링: 동시 1000건 → 자동 1000 인스턴스     │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)는 택시(필요할 때만 호출, 탄 만큼 과금)이고, VM은 자가용(항상 유지비 발생)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) vs [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)

| 비교 | [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) ([Lambda](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)) | [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) (K8s) |
|:---|:---|:---|
| **관리** | **없음** | 클러스터 관리 |
| <strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/">스케일링</a></strong> | **자동 (0→∞)** | [HPA](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/095_hpa_horizontal_pod_autoscaler_kubernetes/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) |
| **과금** | 실행 시간 | 노드 상시 |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/347_cold_start_problem/">Cold Start</a></strong> | <strong>있음 (<a href="/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a>)</strong> | 없음 |
| **실행 제한** | 15분 | 없음 |

- **📢 섹션 요약 비유**: Lambda는 렌터카(필요할 때만), K8s는 자가용 차고(항상 준비, 유지비 발생).

---

## Ⅲ. 비교 및 연결

| 비교 | [IaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) | [PaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) | <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/">FaaS</a></strong> |
|:---|:---|:---|:---|
| **관리** | OS+미들웨어 | 런타임 | **없음** |
| **단위** | [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) | 앱 | **함수** |
| **대표** | EC2 | App 엔진 | <strong><a href="/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/">Lambda</a></strong> |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 적합 시나리오
- ✅ 이미지 리사이즈, [웹훅](/knowledge-base/studynote/03_network/09_application_layer_web_email/498_webhook_rest_api_reverse_callback/) 처리, [스케줄](/knowledge-base/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/) 배치.
- ❌ 실시간 스트리밍, 장기 배치(15분+), 상태 유지.

---

## Ⅴ. 기대효과 및 결론

[서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)는 <strong>운영 부담 제로·유휴 비용 제로</strong>를 실현하며, Edge Function(Cloudflare Workers)·[AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 추론 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)(Bedrock)로 확장되고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/">FaaS</a></strong> | 함수 단위 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) ([Lambda](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)) |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/347_cold_start_problem/">Cold Start</a></strong> | [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)의 핵심 제약 |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/186_baas_backend_as_a_service_firebase/">BaaS</a></strong> | Backend [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) (Firebase) |
| **Edge Function** | [CDN](/knowledge-base/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/) 엣지에서 실행하는 [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) |
| **이벤트 기반** | [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)의 [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 모델 |

### 📈 관련 키워드 및 발전 흐름도

```text
[IaaS (EC2, 2006)]
    │
    ▼
[PaaS (Heroku, 2009)]
    │
    ▼
[FaaS (AWS Lambda, 2014) — 서버리스 시대]
    │
    ▼
[Edge Function (Cloudflare Workers, 2018~)]
    │
    ▼
[현재: AI 서버리스 — 추론 API 서버리스화 (Bedrock)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)는 <strong>택시</strong>예요. 필요할 때만 부르고 **탄 만큼만 내면** 돼요.
2. [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)(자가용)은 안 타도 <strong>주차비·보험료</strong>가 나가지만, 택시는 안 타면 <strong>공짜</strong>예요.
3. 하지만 택시는 <strong>부르면 오는 데 시간(<a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/347_cold_start_problem/">Cold Start</a>)</strong>이 걸리는 단점이 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 123 / 973

← **이전**: [122. 컨테이너 오케스트레이션 (Container Orchestration) - K8s 핵심 개념과 아키텍처](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/122_container_orchestration_kubernetes_k8s/)
**다음**: [124. 클라우드 네이티브 아키텍처 - CNCF 기반 현대 소프트웨어 개발 패러다임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/124_cloud_native_development_architecture/) →

---
