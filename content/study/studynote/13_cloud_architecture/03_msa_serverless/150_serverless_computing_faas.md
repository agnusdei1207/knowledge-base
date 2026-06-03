+++
weight = 150
title = "150. 서버리스 컴퓨팅 (Serverless Computing / FaaS)"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[206_serverless_cold_start|서버리스]] ([[206_serverless_cold_start|Serverless]])는 서버가 없는 것이 아니라 개발자가 서버를 관리할 필요 없이 비즈니스 함수만 배포하면 클라우드 벤더가 인프라·확장·과금을 자동 처리하는 모델이다.
> 2. **가치**: [[342_faas|FaaS]] (Function [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]]) 덕분에 호출당 밀리초 단위 과금으로 유휴 비용 제로에 수렴하고, 트래픽 폭증 시에도 자동 수평 확장으로 [[090_service_kubernetes_network_load_balancing|서비스]]가 끊기지 않는다.
> 3. **판단 포인트**: 이벤트 기반 단발성 작업·비정기적 트래픽에 최적이나 [[152_cold_start_latency_serverless|콜드 스타트 지연]]과 상태 비저장([[239_stateless_redis|Stateless]]) 제약으로 인해 장시간 실행·상태 유지가 필요한 [[090_service_kubernetes_network_load_balancing|서비스]]에는 부적합하다.

---

## Ⅰ. 개요 및 필요성

클라우드 도입 초기에는 [[183_iaas_infrastructure_as_a_service|IaaS]] (Infrastructure [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]])로 VM을 직접 관리했고, 이후 [[184_paas_platform_as_a_service|PaaS]] (Platform [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]])로 런타임 관리를 위임했다. [[206_serverless_cold_start|서버리스]]는 그 위 단계로, OS·미들웨어·런타임·용량 계획까지 전부 벤더가 담당하고 개발자는 함수(Function) 코드만 작성한다.

[[342_faas|FaaS]] (Function [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]])는 [[206_serverless_cold_start|서버리스]]의 핵심 실행 모델이다. 이벤트([[461_http_stateless_connection_oriented|HTTP]] 요청, [[501_file_definition_logical_record|파일]] 업로드, 메시지 큐 메시지 등)가 발생하면 클라우드 플랫폼이 함수 인스턴스를 즉시 생성해 실행하고, 처리 완료 후 인스턴스를 회수한다. 인스턴스가 실행 중인 시간(밀리초 단위)과 호출 횟수에 따라 과금되므로 트래픽 없는 새벽 시간대에는 비용이 사실상 0에 수렴한다.

진정한 [[531_cloud_native_architecture|클라우드 네이티브]] ([[199_cloud_native_architecture_msa_cicd_devops|Cloud Native]]) 환경을 구현하려면 [[206_serverless_cold_start|서버리스]]가 핵심 레고 블록이다. 이미지 처리, 알림 발송, [[001_dikw_pyramid|데이터]] 변환, [[014_api_posix|API]] 백엔드 등 이벤트 중심 작업에서 [[206_serverless_cold_start|서버리스]]는 기존 [[561_container_based_deployment|컨테이너]] 기반보다 운영 부담을 80% 이상 줄인다.

📢 **섹션 요약 비유**: [[206_serverless_cold_start|서버리스]]는 택시 앱 — 내 차(서버)를 소유·유지할 필요 없이 필요할 때만 부르고 탄 만큼만 요금을 낸다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 항목 | 내용 | 특징 |
|:---|:---|:---|
| 실행 단위 | 함수 (Function) | [[355_process|단일 책임 원칙]] 적용 |
| [[507_acid_properties|트리거]] 유형 | [[461_http_stateless_connection_oriented|HTTP]], [[208_schedule_history_transaction_execution_order|스케줄]], 메시지, 스토리지 이벤트 | 이벤트 소스 매핑 |
| 과금 모델 | 호출 횟수 + 실행 시간(ms) | 유휴 비용 없음 |
| 확장 방식 | 자동 수평 확장 (Auto [[202_scale_out_distributed_horizontal_expansion|Scale-out]]) | 용량 계획 불필요 |
| 상태 관리 | 무상태 ([[239_stateless_redis|Stateless]]) | 외부 스토리지 필수 |
| 제한 시간 | 최대 15분 (AWS [[216_lambda_kappa_architecture_batch_realtime|Lambda]] 기준) | 장시간 작업 부적합 |

```text
┌─────────────────────────────────────────────────────────────────────┐
│                     서버리스 실행 흐름                              │
│                                                                     │
│  이벤트 소스                 FaaS 플랫폼              실행 환경     │
│  ┌──────────┐  트리거         ┌──────────────┐      ┌──────────┐   │
│  │ HTTP API │────────────────►│              │ 생성 │ Function │   │
│  │ S3 업로드│                 │  이벤트       │─────►│ Instance │   │
│  │ SQS 큐   │                 │  라우터       │      │          │   │
│  │ 스케줄러 │                 │              │◄─────│  결과 반환│   │
│  └──────────┘                 └──────────────┘ 소멸 └──────────┘   │
│                                      │                              │
│                               과금: 실행ms × 메모리                  │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  외부 연동 (상태 저장)                                        │   │
│  │  DynamoDB / S3 / RDS Proxy / ElastiCache / SQS              │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: [[342_faas|FaaS]] 함수는 자판기 — 동전(이벤트)을 넣으면 그때만 모터가 돌아가고 음료가 나오면 멈춘다. 24시간 가동하지 않는다.

---

## Ⅲ. 비교 및 연결

| 구분 | [[206_serverless_cold_start|서버리스]] ([[342_faas|FaaS]]) | [[561_container_based_deployment|컨테이너]] (CaaS) | [[598_vm_migration_nic|VM]] ([[183_iaas_infrastructure_as_a_service|IaaS]]) |
|:---|:---|:---|:---|
| 관리 범위 | 코드만 | [[561_container_based_deployment|컨테이너]]+[[073_container_orchestration_tools|오케스트레이션]] | OS+미들웨어 전부 |
| 과금 단위 | 호출·ms | 실행 시간·CPU | 시간당 |
| 확장성 | 완전 자동 | 오토스케일러 필요 | 수동·반자동 |
| [[559_serverless_cold_start_mitigation|콜드 스타트]] | 있음 | 거의 없음 | 없음 |
| 상태 관리 | 불가 (외부 필수) | 가능 ([[269_pvc_vs_svc_virtual_circuits|PVC]] 등) | 자유롭게 |
| 최적 워크로드 | 이벤트·단발성 | 상시 실행 [[090_service_kubernetes_network_load_balancing|서비스]] | 레거시·범용 |

📢 **섹션 요약 비유**: FaaS는 전기 요금처럼 쓴 만큼만 내는 방식 — VM은 기본료가 나오는 정액제, [[561_container_based_deployment|컨테이너]]는 [[001_dikw_pyramid|데이터]] 요금제에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**[[206_serverless_cold_start|서버리스]] 적합 시나리오**
- 이미지·동영상 변환(S3 이벤트 → [[216_lambda_kappa_architecture_batch_realtime|Lambda]] → 변환 완료 저장)
- 정기 배치 작업([[208_schedule_history_transaction_execution_order|스케줄]] [[507_acid_properties|트리거]] → [[001_dikw_pyramid|데이터]] 집계 → DB 저장)
- [[101_iot_concept|IoT]] 이벤트 처리(수천 개 디바이스 → 이벤트 큐 → 함수 [[430_index_fast_full_scan|병렬]] 처리)
- 챗봇·[[498_webhook_rest_api_reverse_callback|웹훅]] 수신([[542_api_gateway|API Gateway]] → [[216_lambda_kappa_architecture_batch_realtime|Lambda]] → 응답)

**부적합 시나리오**
- 수 시간 실행이 필요한 ML 학습 파이프라인
- [[480_websocket_full_duplex|WebSocket]] 지속 연결이 필요한 실시간 채팅 서버
- 낮은 레이턴시(< 10ms)가 필수인 금융 거래 코어

📢 **섹션 요약 비유**: [[206_serverless_cold_start|서버리스]]는 배달 음식 — 매일 일정 시간 먹는다면 자취([[598_vm_migration_nic|VM]])가 저렴하지만, 불규칙하게 가끔 먹는다면 배달이 훨씬 경제적이다.

---

## Ⅴ. 기대효과 및 결론

[[206_serverless_cold_start|서버리스]]는 운영 비용 절감(유휴 제로), 인프라 관리 부담 제거, 자동 확장이라는 세 가지 가치를 동시에 제공한다. 스타트업이나 소규모 팀이 빠르게 프로토타입을 출시하고 트래픽에 따라 자연스럽게 확장하는 데 탁월한 선택이다.

한계로는 [[152_cold_start_latency_serverless|콜드 스타트 지연]], 상태 비저장 제약, [[051_vendor_lock_in_cloud_computing|벤더 종속]]([[254_cloud_vendor_lock_in_avoidance_portability_multi_cloud|Vendor Lock-in]]), 디버깅·모니터링의 어려움이 있다. 이를 극복하기 위해 [[202_provisioned_concurrency_serverless_cold_start|Provisioned Concurrency]], Knative([[191_oss_license_compliance|오픈소스]] [[342_faas|FaaS]]), [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]] 도구(X-Ray, [[146_opentelemetry_otel_observability_standard|OpenTelemetry]])를 함께 도입해야 한다.

📢 **섹션 요약 비유**: [[206_serverless_cold_start|서버리스]]는 클라우드의 완성형 — 자동차 렌탈에서 카셰어링으로 진화하듯, 인프라 소유에서 완전한 사용 중심으로 패러다임이 이동한 결과물이다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| [[342_faas|FaaS]] (Function [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]]) | [[206_serverless_cold_start|서버리스]]의 핵심 실행 모델 |
| [[559_serverless_cold_start_mitigation|콜드 스타트]] ([[347_cold_start_problem|Cold Start]]) | 유휴 후 첫 호출 시 레이턴시 발생 |
| 이벤트 [[507_acid_properties|트리거]] | 함수 실행의 시작점 |
| [[200_12_factor_app_cloud_native_principles|12-Factor App]] | 상태 비저장 원칙과 동일 철학 |
| [[542_api_gateway|API Gateway]] | [[461_http_stateless_connection_oriented|HTTP]] [[507_acid_properties|트리거]]를 FaaS로 연결하는 [[264_proxy_pattern_surrogate_access_control|프록시]] |
| [[186_baas_backend_as_a_service_firebase|BaaS]] (Backend [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]]) | FaaS와 결합해 완전한 [[206_serverless_cold_start|서버리스]] [[057_stack|스택]] 구성 |

### 👶 어린이를 위한 3줄 비유 설명
1. [[206_serverless_cold_start|서버리스]]는 켜 두지 않아도 되는 전등 — 방에 들어갈 때만 자동으로 켜지고, 나가면 꺼져서 전기세를 아낀다.

### 📈 관련 키워드 및 발전 흐름도

```text
항상 가동 서버 (유휴 비용 발생)
    │
    ▼
Serverless / FaaS: 이벤트 기반 · Pay-per-Use
    ├─► AWS Lambda · GCP Cloud Functions · Azure Functions
    └─► BaaS: Firebase · Supabase (백엔드 서비스)
    │
    ▼
Cold Start 최적화 · Knative (K8s 기반 서버리스)
```
2. 개발자는 전구(코드) 디자인만 하면 되고, 전선 공사(서버 관리)는 클라우드 회사가 다 해준다.
3. 손님이 100명 오면 전등이 100개 켜지고, 손님이 0명이면 전등이 꺼져서 요금이 0원이 된다.
