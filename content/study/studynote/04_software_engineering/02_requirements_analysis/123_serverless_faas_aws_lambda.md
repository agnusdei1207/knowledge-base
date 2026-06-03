+++
weight = 123
title = "123. 서버리스 & FaaS (Serverless / AWS Lambda) - 인프라 없는 함수 단위 컴퓨팅"
date = "2026-04-19"
[extra]
categories = "studynote-software-engineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[206_serverless_cold_start|서버리스]]([[206_serverless_cold_start|Serverless]])는 **서버 [[528_provisioning|프로비저닝]]·관리 없이 코드만 배포하면 클라우드가 자동 실행·[[249_scaling_normalization_standardization|스케일링]]·과금**하는 컴퓨팅 모델이며, [[342_faas|FaaS]](Function [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]])는 **함수 단위로 실행**되는 [[206_serverless_cold_start|서버리스]]의 대표 형태이다.
> 2. **가치**: [[598_vm_migration_nic|VM]]·K8s는 서버 관리(패치·[[249_scaling_normalization_standardization|스케일링]])가 필요하지만, [[206_serverless_cold_start|서버리스]]는 **코드만 작성하면 실행 횟수·시간 기반으로 과금**되어 유휴 비용이 0이다.
> 3. **판단 포인트**: **[[347_cold_start_problem|Cold Start]](첫 실행 [[015_지연_데이터_관점|지연]])**·**실행 시간 제한(15분)**·**상태 비저장([[239_stateless_redis|Stateless]])**의 제약이 있으므로, 이벤트 기반 단기 작업에 적합하고 장기 실행·상태 유지 워크로드에는 부적합하다.

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

- **📢 섹션 요약 비유**: [[206_serverless_cold_start|서버리스]]는 택시(필요할 때만 호출, 탄 만큼 과금)이고, VM은 자가용(항상 유지비 발생)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[206_serverless_cold_start|서버리스]] vs [[561_container_based_deployment|컨테이너]]

| 비교 | [[206_serverless_cold_start|서버리스]] ([[216_lambda_kappa_architecture_batch_realtime|Lambda]]) | [[561_container_based_deployment|컨테이너]] (K8s) |
|:---|:---|:---|
| **관리** | **없음** | 클러스터 관리 |
| **[[249_scaling_normalization_standardization|스케일링]]** | **자동 (0→∞)** | [[095_hpa_horizontal_pod_autoscaler_kubernetes|HPA]] [[009_config|설정]] |
| **과금** | 실행 시간 | 노드 상시 |
| **[[347_cold_start_problem|Cold Start]]** | **있음 ([[015_지연_데이터_관점|지연]])** | 없음 |
| **실행 제한** | 15분 | 없음 |

- **📢 섹션 요약 비유**: Lambda는 렌터카(필요할 때만), K8s는 자가용 차고(항상 준비, 유지비 발생).

---

## Ⅲ. 비교 및 연결

| 비교 | [[183_iaas_infrastructure_as_a_service|IaaS]] | [[184_paas_platform_as_a_service|PaaS]] | **[[342_faas|FaaS]]** |
|:---|:---|:---|:---|
| **관리** | OS+미들웨어 | 런타임 | **없음** |
| **단위** | [[598_vm_migration_nic|VM]] | 앱 | **함수** |
| **대표** | EC2 | App Engine | **[[216_lambda_kappa_architecture_batch_realtime|Lambda]]** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 적합 시나리오
- ✅ 이미지 리사이즈, [[498_webhook_rest_api_reverse_callback|웹훅]] 처리, [[208_schedule_history_transaction_execution_order|스케줄]] 배치.
- ❌ 실시간 스트리밍, 장기 배치(15분+), 상태 유지.

---

## Ⅴ. 기대효과 및 결론

[[206_serverless_cold_start|서버리스]]는 **운영 부담 제로·유휴 비용 제로**를 실현하며, Edge Function(Cloudflare Workers)·[[190_ai_llm_requirements_specification|AI]] 추론 [[206_serverless_cold_start|서버리스]](Bedrock)로 확장되고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[342_faas|FaaS]]** | 함수 단위 [[206_serverless_cold_start|서버리스]] ([[216_lambda_kappa_architecture_batch_realtime|Lambda]]) |
| **[[347_cold_start_problem|Cold Start]]** | [[206_serverless_cold_start|서버리스]]의 핵심 제약 |
| **[[186_baas_backend_as_a_service_firebase|BaaS]]** | Backend [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]] (Firebase) |
| **Edge Function** | [[506_cdn_content_delivery_network_edge_caching|CDN]] 엣지에서 실행하는 [[206_serverless_cold_start|서버리스]] |
| **이벤트 기반** | [[206_serverless_cold_start|서버리스]]의 [[507_acid_properties|트리거]] 모델 |

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
1. [[206_serverless_cold_start|서버리스]]는 **택시**예요. 필요할 때만 부르고 **탄 만큼만 내면** 돼요.
2. [[598_vm_migration_nic|VM]](자가용)은 안 타도 **주차비·보험료**가 나가지만, 택시는 안 타면 **공짜**예요.
3. 하지만 택시는 **부르면 오는 데 시간([[347_cold_start_problem|Cold Start]])**이 걸리는 단점이 있어요!
