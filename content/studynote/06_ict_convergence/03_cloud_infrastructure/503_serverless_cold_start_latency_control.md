---
title: "Serverless Cold Start Latency Control"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)([Serverless](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)/[FaaS](/studynote/12_it_management/05_security_compliance/342_faas/))의 [콜드 스타트](/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/)([Cold Start](/studynote/06_ict_convergence/05_data_science/347_cold_start_problem/))는 최초 호출 시 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 초기화 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)(수백ms~수 초)으로, 대기 중인 인스턴스가 없을 때 발생하는 비용-성능 트레이드오프다.
> 2. **가치**: [프로비저닝된 동시성](/studynote/06_ict_convergence/03_cloud_infrastructure/202_provisioned_concurrency_serverless_cold_start/)([Provisioned Concurrency](/studynote/06_ict_convergence/03_cloud_infrastructure/202_provisioned_concurrency_serverless_cold_start/)), 경량 런타임, 워밍업 [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)로 [콜드 스타트](/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/)를 제어하면 [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)의 비용 이점을 유지하면서 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 최소화할 수 있다.
> 3. **판단 포인트**: [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)는 상태 비저장([Stateless](/studynote/15_devops_sre/05_devsecops/239_stateless_redis/)) 구조이므로, 상태가 필요한 경우 반드시 외부 캐시([Redis](/studynote/05_database/04_transactions_concurrency/542_redis/)) 또는 DB를 통해 상태를 관리해야 한다.

---

## Ⅰ. 개요 및 필요성

[FaaS](/studynote/12_it_management/05_security_compliance/342_faas/)(Function [as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))는 개발자가 서버를 관리하지 않고 함수 단위로 코드를 실행하는 모델이다. AWS [Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/), Azure Functions, Google Cloud Functions가 대표 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)다. 요청이 없을 때는 인프라가 완전히 반납되어(Scale-to-Zero) 비용이 0원이 되지만, 이 대신 최초 호출 시 초기화 시간이 발생한다.

<strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/">콜드 스타트</a> 발생 원인</strong>:
1. [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지 다운로드
2. 런타임(JVM, Python 인터프리터 등) 초기화
3. 의존성 [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 로딩
4. 애플리케이션 초기화 코드 실행

[콜드 스타트](/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/)는 Java/Python 등 무거운 런타임에서 수 초, Go/[Rust](/studynote/04_software_engineering/10_trends_pm_quality/782_memory_safety_rust_compiler_verification/) 등 경량 런타임에서 수십 ms 수준이다.

- **📢 섹션 요약 비유**: [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)는 필요할 때만 전원을 켜는 전등이다. 에너지 절약은 되지만, 처음 켤 때 예열 시간이 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

<strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/">콜드 스타트</a> vs 웜 스타트(Warm Start) 흐름</strong>:

```
[콜드 스타트 흐름]
요청 -> 컨테이너 생성 -> 런타임 로드 -> 의존성 로드 -> 핸들러 실행
       ^ 수백ms~수 초 소요

[웜 스타트 흐름]
요청 -> (이미 실행 중인 인스턴스) -> 핸들러 실행
       ^ 수ms 소요

[프로비저닝된 동시성 (Provisioned Concurrency)]
사전에 지정한 수의 인스턴스를 항상 웜(Warm) 상태로 유지
-> 콜드 스타트 완전 제거, 비용 증가
```

| 해결책 | 방법 | 효과 | 비용 |
|:---|:---|:---|:---|
| [프로비저닝된 동시성](/studynote/06_ict_convergence/03_cloud_infrastructure/202_provisioned_concurrency_serverless_cold_start/) ([Provisioned Concurrency](/studynote/06_ict_convergence/03_cloud_infrastructure/202_provisioned_concurrency_serverless_cold_start/)) | 미리 N개 인스턴스 대기 | [콜드 스타트](/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/) 제거 | 상시 과금 |
| 워밍업 [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) (Warm-up Scheduler) | 주기적 [더미](/studynote/04_software_engineering/11_testing_validation/851_dummy_test_double/) 호출 | [콜드 스타트](/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/) 감소 | 간헐적 과금 |
| 경량 런타임 | Go, [Rust](/studynote/04_software_engineering/10_trends_pm_quality/782_memory_safety_rust_compiler_verification/), Node.js 사용 | 초기화 시간 단축 | 없음 |
| 마이크로VM (Firecracker) | 경량 VM으로 빠른 격리 | 100ms 이하 기동 | 없음(인프라 교체) |
| 이미지 최적화 | 의존성 최소화, 레이어 축소 | 다운로드 시간 단축 | 없음 |

**비용 모델**: 호출 수 × 단가 + 실행 시간 × 메모리(GB-초). 예: AWS [Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) 무료 티어 월 100만 건, 400,000 GB-초. [프로비저닝된 동시성](/studynote/06_ict_convergence/03_cloud_infrastructure/202_provisioned_concurrency_serverless_cold_start/)은 별도 시간 단위 과금.

- **📢 섹션 요약 비유**: [프로비저닝된 동시성](/studynote/06_ict_convergence/03_cloud_infrastructure/202_provisioned_concurrency_serverless_cold_start/)은 대기 택시를 미리 잡아두는 것 — 빠른 출발은 보장되지만, 기다리는 시간에도 요금이 나간다.

---

## Ⅲ. 비교 및 연결

<strong><a href="/studynote/12_it_management/05_security_compliance/342_faas/">FaaS</a> 실행 제약</strong>:
- 실행 시간 제한: AWS [Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) 최대 15분, Azure Functions 10분(Consumption Plan)
- 메모리 제한: 128MB~10GB(AWS [Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/))
- 로컬 스토리지: `/tmp` 512MB~10GB, 함수 종료 시 삭제

<strong>상태 비저장(<a href="/studynote/15_devops_sre/05_devsecops/239_stateless_redis/">Stateless</a>) 아키텍처 패턴</strong>:
- [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 토큰: [JWT](/studynote/03_network/10_application_layer_dns_mgmt/549_jwt_json_web_token/)([JSON Web Token](/studynote/03_network/10_application_layer_dns_mgmt/549_jwt_json_web_token/)) — 서버 측 [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 없이 [클레임](/studynote/09_security/11_iam_access_control/539_claims/) 자체 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)
- 캐시: ElastiCache([Redis](/studynote/05_database/04_transactions_concurrency/542_redis/)) — [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 임시 결과 저장
- 큐: SQS, [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) — 이벤트 드리븐 처리, 재시도 보장

**Firecracker(마이크로VM)**: AWS가 오픈소스로 공개한 경량 [KVM](/studynote/01_computer_architecture/15_advanced_topics/713_kvm_over_ip/) 기반 [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/). 125ms 이내 기동, [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 수준 경량 + [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 수준 격리. Lambda와 Fargate의 기반 기술.

- **📢 섹션 요약 비유**: 상태 비저장 함수는 매번 새 칠판에 계산하는 수학자다. 이전 계산 결과는 노트(외부 DB)에 써두지 않으면 사라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**기술사 시험 판단 포인트**:
1. [콜드 스타트](/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/) 원인([컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 초기화 단계)과 해결책을 비용 관점에서 비교한다.
2. [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 비용 모델(호출 수 + 실행 시간 × 메모리)을 [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 비용 모델(시간 단위 고정)과 대비하여 설명한다.
3. [Stateless](/studynote/15_devops_sre/05_devsecops/239_stateless_redis/) 제약과 외부 상태 관리 패턴([Redis](/studynote/05_database/04_transactions_concurrency/542_redis/), S3)을 아키텍처 다이어그램으로 제시한다.

**실무 시나리오**: 이미지 리사이징 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) — S3 업로드 이벤트 [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/) -> [Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) 호출(Go 런타임, 256MB) -> 처리 후 S3 저장. 하루 수만 건 간헐적 요청, [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 대비 월 비용 90% 절감. 단, [SLA](/studynote/12_it_management/02_itsm_itil/869_sla/)([Service Level Agreement](/studynote/12_it_management/02_itsm_itil/869_sla/)) 99.9% 필요 시 [프로비저닝된 동시성](/studynote/06_ict_convergence/03_cloud_infrastructure/202_provisioned_concurrency_serverless_cold_start/)(최소 5) [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/).

- **📢 섹션 요약 비유**: [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 아키텍처는 자동 주차 타워다 — 빈 공간 없이 효율적이지만, 차를 꺼내는 데 [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 주차장보다 약간 더 걸린다.

---

## Ⅴ. 기대효과 및 결론

[서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) [콜드 스타트](/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/)를 제대로 관리하면:
- **비용 혁신**: 사용량 기반 과금으로 유휴 비용 [제로화](/studynote/01_computer_architecture/15_advanced_topics/784_zeroization_circuit/)
- **운영 제로**: 서버 패치, OS 관리 완전 위임
- **무한 스케일**: 초당 수만 건 요청도 자동 확장
- **개발 속도**: 인프라 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 없이 함수 코드만 배포

[서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)는 이벤트 드리븐, 단발성, 경량 로직에 최적화된 패러다임이며, [콜드 스타트](/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/) 제어 기술을 이해하면 성능과 비용을 동시에 최적화할 수 있다.

- **📢 섹션 요약 비유**: [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)는 공유 킥보드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)다 — 필요할 때 쓰고, 쓴 만큼만 내고, 주차 공간 걱정도 없다. 단, 처음 앱 켜는 시간([콜드 스타트](/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/))이 약간 아쉽다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [FaaS](/studynote/12_it_management/05_security_compliance/342_faas/) (Function [as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) | [Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/), 이벤트 드리븐, Scale-to-Zero · 499 |
| Firecracker (마이크로VM) | [KVM](/studynote/01_computer_architecture/15_advanced_topics/713_kvm_over_ip/), 경량 격리, AWS [Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) 기반 · 501 |
| [프로비저닝된 동시성](/studynote/06_ict_convergence/03_cloud_infrastructure/202_provisioned_concurrency_serverless_cold_start/) ([Provisioned Concurrency](/studynote/06_ict_convergence/03_cloud_infrastructure/202_provisioned_concurrency_serverless_cold_start/)) | 웜 스타트, 상시 인스턴스 · 502 |
| [Redis](/studynote/05_database/04_transactions_concurrency/542_redis/) | 외부 캐시, [세션 관리](/studynote/04_software_engineering/08_security_compliance_devsecops/507_session_management_security/), 상태 저장 · 506 |
| 이벤트 드리븐 (Event-Driven) | SQS, [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/), [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/) · 506 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Lambda · 이벤트 드리븐] -> [서버리스 콜드 스타트 지연 제어] -> [SQS · Kafka]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)는 필요할 때만 불을 켜는 전등이에요 — 아무도 없을 때는 전기를 아끼지만, 처음 켤 때 잠깐 기다려야 해요.
2. [콜드 스타트](/studynote/04_software_engineering/09_cloud_native_ai_architecture/559_serverless_cold_start_mitigation/)는 겨울에 차 시동 거는 것처럼, 처음엔 시간이 걸리지만 한 번 달궈지면 빨라요.
3. 기억 없는 함수([Stateless](/studynote/15_devops_sre/05_devsecops/239_stateless_redis/))는 매번 새로 태어나는 금붕어처럼, 이전에 뭘 했는지 노트(외부 DB)에 적어두지 않으면 잊어버려요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 503 / 552

<- **이전**: [502. 쿠버네티스 Pod 오케스트레이션 배포 (Kubernetes Pod Orchestration Deployment)](/studynote/06_ict_convergence/03_cloud_infrastructure/502_kubernetes_pod_orchestration_deployment/)
**다음**: [504. IaC 테라폼과 불변 인프라 선언 (IaC Terraform Immutable Infrastructure)](/studynote/06_ict_convergence/03_cloud_infrastructure/504_iac_terraform_immutable_infrastructure/) ->

---
