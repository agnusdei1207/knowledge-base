---
title: 503. 서버리스 콜드 스타트 지연 제어 (Serverless Cold Start Latency Control)
date: '2026-05-09'
tags:
- studynote-ict-convergence
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[206_serverless_cold_start|서버리스]]([[206_serverless_cold_start|Serverless]]/[[342_faas|FaaS]])의 [[559_serverless_cold_start_mitigation|콜드 스타트]]([[347_cold_start_problem|Cold Start]])는 최초 호출 시 [[561_container_based_deployment|컨테이너]] 초기화 [[015_지연_데이터_관점|지연]](수백ms~수 초)으로, 대기 중인 인스턴스가 없을 때 발생하는 비용-성능 트레이드오프다.
> 2. **가치**: [[202_provisioned_concurrency_serverless_cold_start|프로비저닝된 동시성]]([[202_provisioned_concurrency_serverless_cold_start|Provisioned Concurrency]]), 경량 런타임, 워밍업 [[079_kube_scheduler_pod_placement|스케줄러]]로 [[559_serverless_cold_start_mitigation|콜드 스타트]]를 제어하면 [[206_serverless_cold_start|서버리스]]의 비용 이점을 유지하면서 [[015_지연_데이터_관점|지연]]을 최소화할 수 있다.
> 3. **판단 포인트**: [[206_serverless_cold_start|서버리스]]는 상태 비저장([[239_stateless_redis|Stateless]]) 구조이므로, 상태가 필요한 경우 반드시 외부 캐시([[542_redis|Redis]]) 또는 DB를 통해 상태를 관리해야 한다.

---

## Ⅰ. 개요 및 필요성

[[342_faas|FaaS]](Function [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]])는 개발자가 서버를 관리하지 않고 함수 단위로 코드를 실행하는 모델이다. AWS [[216_lambda_kappa_architecture_batch_realtime|Lambda]], Azure Functions, Google Cloud Functions가 대표 [[090_service_kubernetes_network_load_balancing|서비스]]다. 요청이 없을 때는 인프라가 완전히 반납되어(Scale-to-Zero) 비용이 0원이 되지만, 이 대신 최초 호출 시 초기화 시간이 발생한다.

**[[559_serverless_cold_start_mitigation|콜드 스타트]] 발생 원인**:
1. [[561_container_based_deployment|컨테이너]] 이미지 다운로드
2. 런타임(JVM, Python 인터프리터 등) 초기화
3. 의존성 [[336_library_vs_framework|라이브러리]] 로딩
4. 애플리케이션 초기화 코드 실행

[[559_serverless_cold_start_mitigation|콜드 스타트]]는 Java/Python 등 무거운 런타임에서 수 초, Go/[[782_memory_safety_rust_compiler_verification|Rust]] 등 경량 런타임에서 수십 ms 수준이다.

- **📢 섹션 요약 비유**: [[206_serverless_cold_start|서버리스]]는 필요할 때만 전원을 켜는 전등이다. 에너지 절약은 되지만, 처음 켤 때 예열 시간이 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

**[[559_serverless_cold_start_mitigation|콜드 스타트]] vs 웜 스타트(Warm Start) 흐름**:

```
[콜드 스타트 흐름]
요청 → 컨테이너 생성 → 런타임 로드 → 의존성 로드 → 핸들러 실행
       ↑ 수백ms~수 초 소요

[웜 스타트 흐름]
요청 → (이미 실행 중인 인스턴스) → 핸들러 실행
       ↑ 수ms 소요

[프로비저닝된 동시성 (Provisioned Concurrency)]
사전에 지정한 수의 인스턴스를 항상 웜(Warm) 상태로 유지
→ 콜드 스타트 완전 제거, 비용 증가
```

| 해결책 | 방법 | 효과 | 비용 |
|:---|:---|:---|:---|
| [[202_provisioned_concurrency_serverless_cold_start|프로비저닝된 동시성]] ([[202_provisioned_concurrency_serverless_cold_start|Provisioned Concurrency]]) | 미리 N개 인스턴스 대기 | [[559_serverless_cold_start_mitigation|콜드 스타트]] 제거 | 상시 과금 |
| 워밍업 [[079_kube_scheduler_pod_placement|스케줄러]] (Warm-up Scheduler) | 주기적 [[459_dummy_test_double|더미]] 호출 | [[559_serverless_cold_start_mitigation|콜드 스타트]] 감소 | 간헐적 과금 |
| 경량 런타임 | Go, [[782_memory_safety_rust_compiler_verification|Rust]], Node.js 사용 | 초기화 시간 단축 | 없음 |
| 마이크로VM (Firecracker) | 경량 VM으로 빠른 격리 | 100ms 이하 기동 | 없음(인프라 교체) |
| 이미지 최적화 | 의존성 최소화, 레이어 축소 | 다운로드 시간 단축 | 없음 |

**비용 모델**: 호출 수 × 단가 + 실행 시간 × 메모리(GB-초). 예: AWS [[216_lambda_kappa_architecture_batch_realtime|Lambda]] 무료 티어 월 100만 건, 400,000 GB-초. [[202_provisioned_concurrency_serverless_cold_start|프로비저닝된 동시성]]은 별도 시간 단위 과금.

- **📢 섹션 요약 비유**: [[202_provisioned_concurrency_serverless_cold_start|프로비저닝된 동시성]]은 대기 택시를 미리 잡아두는 것 — 빠른 출발은 보장되지만, 기다리는 시간에도 요금이 나간다.

---

## Ⅲ. 비교 및 연결

**[[342_faas|FaaS]] 실행 제약**:
- 실행 시간 제한: AWS [[216_lambda_kappa_architecture_batch_realtime|Lambda]] 최대 15분, Azure Functions 10분(Consumption Plan)
- 메모리 제한: 128MB~10GB(AWS [[216_lambda_kappa_architecture_batch_realtime|Lambda]])
- 로컬 스토리지: `/tmp` 512MB~10GB, 함수 종료 시 삭제

**상태 비저장([[239_stateless_redis|Stateless]]) 아키텍처 패턴**:
- [[303_authentication_authorization_patterns|인증]] 토큰: [[549_jwt_json_web_token|JWT]]([[549_jwt_json_web_token|JSON Web Token]]) — 서버 측 [[160_session_controlling_terminal|세션]] 없이 [[539_claims|클레임]] 자체 [[395_verification_process_review|검증]]
- 캐시: ElastiCache([[542_redis|Redis]]) — [[160_session_controlling_terminal|세션]] [[001_dikw_pyramid|데이터]], 임시 결과 저장
- 큐: SQS, [[179_kafka_flink_watermark_time_window|Kafka]] — 이벤트 드리븐 처리, 재시도 보장

**Firecracker(마이크로VM)**: AWS가 오픈소스로 공개한 경량 [[713_kvm_over_ip|KVM]] 기반 [[598_vm_migration_nic|VM]]. 125ms 이내 기동, [[561_container_based_deployment|컨테이너]] 수준 경량 + [[598_vm_migration_nic|VM]] 수준 격리. Lambda와 Fargate의 기반 기술.

- **📢 섹션 요약 비유**: 상태 비저장 함수는 매번 새 칠판에 계산하는 수학자다. 이전 계산 결과는 노트(외부 DB)에 써두지 않으면 사라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**기술사 시험 판단 포인트**:
1. [[559_serverless_cold_start_mitigation|콜드 스타트]] 원인([[561_container_based_deployment|컨테이너]] 초기화 단계)과 해결책을 비용 관점에서 비교한다.
2. [[206_serverless_cold_start|서버리스]] 비용 모델(호출 수 + 실행 시간 × 메모리)을 [[598_vm_migration_nic|VM]] 비용 모델(시간 단위 고정)과 대비하여 설명한다.
3. [[239_stateless_redis|Stateless]] 제약과 외부 상태 관리 패턴([[542_redis|Redis]], S3)을 아키텍처 다이어그램으로 제시한다.

**실무 시나리오**: 이미지 리사이징 [[090_service_kubernetes_network_load_balancing|서비스]] — S3 업로드 이벤트 [[507_acid_properties|트리거]] → [[216_lambda_kappa_architecture_batch_realtime|Lambda]] 호출(Go 런타임, 256MB) → 처리 후 S3 저장. 하루 수만 건 간헐적 요청, [[598_vm_migration_nic|VM]] 대비 월 비용 90% 절감. 단, [[085_sla|SLA]]([[085_sla|Service Level Agreement]]) 99.9% 필요 시 [[202_provisioned_concurrency_serverless_cold_start|프로비저닝된 동시성]](최소 5) [[009_config|설정]].

- **📢 섹션 요약 비유**: [[206_serverless_cold_start|서버리스]] 아키텍처는 자동 주차 타워다 — 빈 공간 없이 효율적이지만, 차를 꺼내는 데 [[598_vm_migration_nic|VM]] 주차장보다 약간 더 걸린다.

---

## Ⅴ. 기대효과 및 결론

[[206_serverless_cold_start|서버리스]] [[559_serverless_cold_start_mitigation|콜드 스타트]]를 제대로 관리하면:
- **비용 혁신**: 사용량 기반 과금으로 유휴 비용 [[784_zeroization_circuit|제로화]]
- **운영 제로**: 서버 패치, OS 관리 완전 위임
- **무한 스케일**: 초당 수만 건 요청도 자동 확장
- **개발 속도**: 인프라 [[009_config|설정]] 없이 함수 코드만 배포

[[206_serverless_cold_start|서버리스]]는 이벤트 드리븐, 단발성, 경량 로직에 최적화된 패러다임이며, [[559_serverless_cold_start_mitigation|콜드 스타트]] 제어 기술을 이해하면 성능과 비용을 동시에 최적화할 수 있다.

- **📢 섹션 요약 비유**: [[206_serverless_cold_start|서버리스]]는 공유 킥보드 [[090_service_kubernetes_network_load_balancing|서비스]]다 — 필요할 때 쓰고, 쓴 만큼만 내고, 주차 공간 걱정도 없다. 단, 처음 앱 켜는 시간([[559_serverless_cold_start_mitigation|콜드 스타트]])이 약간 아쉽다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[342_faas|FaaS]] (Function [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]]) | [[216_lambda_kappa_architecture_batch_realtime|Lambda]], 이벤트 드리븐, Scale-to-Zero · 499 |
| Firecracker (마이크로VM) | [[713_kvm_over_ip|KVM]], 경량 격리, AWS [[216_lambda_kappa_architecture_batch_realtime|Lambda]] 기반 · 501 |
| [[202_provisioned_concurrency_serverless_cold_start|프로비저닝된 동시성]] ([[202_provisioned_concurrency_serverless_cold_start|Provisioned Concurrency]]) | 웜 스타트, 상시 인스턴스 · 502 |
| [[542_redis|Redis]] | 외부 캐시, [[507_session_management_security|세션 관리]], 상태 저장 · 506 |
| 이벤트 드리븐 (Event-Driven) | SQS, [[179_kafka_flink_watermark_time_window|Kafka]], [[507_acid_properties|트리거]] · 506 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Lambda · 이벤트 드리븐] → [서버리스 콜드 스타트 지연 제어] → [SQS · Kafka]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[206_serverless_cold_start|서버리스]]는 필요할 때만 불을 켜는 전등이에요 — 아무도 없을 때는 전기를 아끼지만, 처음 켤 때 잠깐 기다려야 해요.
2. [[559_serverless_cold_start_mitigation|콜드 스타트]]는 겨울에 차 시동 거는 것처럼, 처음엔 시간이 걸리지만 한 번 달궈지면 빨라요.
3. 기억 없는 함수([[239_stateless_redis|Stateless]])는 매번 새로 태어나는 금붕어처럼, 이전에 뭘 했는지 노트(외부 DB)에 적어두지 않으면 잊어버려요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 503 / 552

← **이전**: [[502_kubernetes_pod_orchestration_deployment|502. 쿠버네티스 Pod 오케스트레이션 배포 (Kubernetes Pod Orchestration Deployment)]]
**다음**: [[504_iac_terraform_immutable_infrastructure|504. IaC 테라폼과 불변 인프라 선언 (IaC Terraform Immutable Infrastructure)]] →

---
