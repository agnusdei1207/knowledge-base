---
title: "Auto Scaling"
date: "2026-04-29"
tags:
  - "studynote-cloud-architecture"
weight: 30
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 오토 [스케일링](/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/)(Auto Scaling)은 부하 변화에 따라 서버 인스턴스 수([스케일 아웃](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)/인) 또는 인스턴스 크기([스케일 업](/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/)/다운)를 자동으로 조정하는 클라우드 핵심 기능이다.
> 2. **가치**: [스케일 아웃](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)(수평 확장)은 여러 소형 인스턴스 추가로 선형 확장이 가능하고 장애 격리([단일 장애점](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) 제거)에 유리하다. [스케일 업](/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/)(수직 확장)은 단순하지만 하드웨어 한계가 있고 재시작이 필요한 경우가 있다.
> 3. **판단 포인트**: 오토 [스케일링](/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 설계의 핵심은 [스케일 아웃](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)(Cooldown)과 스케일 인 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)(Scale-in [Protection](/studynote/02_operating_system/10_security/571_protection_vs_security/))다. 지나치게 빠른 스케일 인은 부하 급증 시 인스턴스 부족으로 장애를 일으킬 수 있다.

---

## Ⅰ. 개요 및 필요성

```text
Auto Scaling 작동 원리:

  CloudWatch 메트릭
  (CPU > 70% 5분)
      |
      v
  Auto Scaling Policy
  (스케일 아웃: +2 인스턴스)
      |
      v
  로드 밸런서 등록
  -> 트래픽 자동 분배

  메트릭 예시:
  - CPU 사용률
  - 요청 수 (Request Count)
  - 응답 시간 (Latency)
  - 메모리 사용률 (커스텀)
  - SQS 큐 길이
```

- **📢 섹션 요약 비유**: 오토 [스케일링](/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/)은 자동 인력 관리다. 손님(트래픽)이 많으면 아르바이트(인스턴스)를 더 고용하고, 한산하면 퇴근시킨다. 사람을 직접 부르는 대신 시스템이 자동으로 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [스케일링](/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 유형

| [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) | 설명 | 사용 시나리오 |
|:---|:---|:---|
| **반응형 (Reactive)** | [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 임계값 초과 시 [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/) | 예측 불가 트래픽 |
| **예측형 (Predictive)** | 과거 패턴 ML 분석 예측 | 주기적 트래픽 패턴 |
| <strong><a href="/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/">스케줄</a> 기반</strong> | 시간 [스케줄](/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/)로 사전 스케일 | 알려진 이벤트 (세일 등) |
| **목표 추적** | [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) 목표값 유지 | CPU 50% 유지 등 |

### AWS Auto Scaling 구성 예시

```text
Auto Scaling Group:
  최소 인스턴스: 2
  원하는 인스턴스: 4
  최대 인스턴스: 20

Scale Out 정책:
  CPU > 70% -> 5분 유지 -> +2 인스턴스
  Cooldown: 300초 (스케일 후 대기)

Scale In 정책:
  CPU < 30% -> 10분 유지 -> -1 인스턴스
  Scale-in Protection: 최소 2 유지
```

- **📢 섹션 요약 비유**: Auto Scaling Group 설정은 음식점 직원 관리 규칙이다. 최소 2명(최소), 평소 4명(원하는), 최대 20명(최대)을 유지하며, 손님 급증 시 즉시 추가 고용, 한산할 때 천천히 퇴근시킨다.

---

## Ⅲ. 비교 및 연결

| 비교 | [스케일 아웃](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/) | [스케일 업](/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/) |
|:---|:---|:---|
| 방법 | 인스턴스 수 증가 | 인스턴스 크기 증가 |
| 한계 | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 설계 필요 | 하드웨어 한계 |
| [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) | 장애 격리 가능 | [단일 장애점](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/) 위험 |
| 비용 | 소형 × 여러 개 | 대형 × 1개 |
| 적합 | 웹 서버, [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) | DB, 레거시 앱 |

- **📢 섹션 요약 비유**: [스케일 아웃](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/) vs [스케일 업](/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/)은 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) vs 리무진이다. [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)([스케일 아웃](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/))는 여러 대를 증편해 많은 승객을 수용하고, 리무진([스케일 업](/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/))은 더 큰 차로 교체하는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) [HPA](/studynote/13_cloud_architecture/02_iaas_paas_saas/095_hpa_horizontal_pod_autoscaler_kubernetes/) ([Horizontal Pod Autoscaler](/studynote/13_cloud_architecture/02_iaas_paas_saas/095_hpa_horizontal_pod_autoscaler_kubernetes/))

```text
HPA 작동:
  메트릭 서버 -> 파드 CPU/메모리 수집
      |
      v
  HPA 컨트롤러:
    현재 CPU = 80%, 목표 = 50%
    원하는 파드 수 = 현재 파드 수 × (현재/목표)
                   = 4 × (80/50) = 6.4 -> 7 파드

  스케일 업 속도: 최대 2배/분
  스케일 다운: 5분 안정화 윈도우 대기
```

### 스케일 인 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 실패 패턴

```text
문제: 스케일 인이 너무 빨리 발생
  트래픽 증가 -> 스케일 아웃 (+5 인스턴스)
  트래픽 잠시 감소 -> 빠른 스케일 인 (-5 인스턴스)
  트래픽 재증가 -> 인스턴스 부족 -> 장애

해결: Cooldown 기간 증가 + Scale-in 임계값 강화
  스케일 아웃 Cooldown: 60초
  스케일 인 Cooldown: 300초 (더 보수적으로)
```

- **📢 섹션 요약 비유**: 스케일 인 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 실패는 급격한 직원 해고 후 갑자기 손님이 몰리는 것이다. 잠깐 한산하다고 직원을 너무 빨리 퇴근시키면, 갑자기 손님이 몰릴 때 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 불가 상태가 된다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **비용 최적화** | 필요 시에만 인스턴스 확장 |
| <strong><a href="/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a></strong> | 장애 시 자동 대체 인스턴스 |
| <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong> | 부하 급증 자동 대응 |

KEDA([Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) Event-Driven Autoscaling)는 [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)이 아닌 이벤트(SQS 메시지 수, [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 랙)로 [스케일링](/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/)을 [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/)하는 차세대 오토스케일러다. [배치 처리](/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/)·이벤트 드리븐 아키텍처에서 0-to-1(0개 -> 1개) [스케일링](/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/)까지 지원하여 [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 오토스케일링을 실현한다.

- **📢 섹션 요약 비유**: KEDA는 주문서 쌓이는 것 보고 직원 부르는 시스템이다. CPU 측정(반응적)이 아니라, 주문서(이벤트) 수로 "지금 바빠지겠다"를 미리 예측해서 직원을 선제 배치한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/095_hpa_horizontal_pod_autoscaler_kubernetes/">HPA</a></strong> | [Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) 수평 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/) 오토스케일러 |
| **로드 밸런서** | 오토스케일링 인스턴스 트래픽 분배 |
| **Cooldown** | [스케일링](/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/) 후 안정화 대기 시간 |
| **KEDA** | 이벤트 기반 [쿠버네티스 오토스케일링](/studynote/06_ict_convergence/03_cloud_infrastructure/206_kubernetes_autoscaling_hpa_vpa_ca/) |
| <strong><a href="/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/">서버리스</a></strong> | 극단적 오토스케일링 (인스턴스 0->N) |

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 용량 계획 — 피크 트래픽 대비 과프로비저닝]
    |
    v
[Auto Scaling — CPU/메모리 기반 자동 스케일 아웃/인]
    |
    v
[예측적 스케일링 — ML 패턴 분석 사전 스케일]
    |
    v
[Kubernetes HPA/VPA — 컨테이너 수평/수직 오토스케일]
    |
    v
[KEDA — 이벤트 드리븐 0->N 서버리스 오토스케일]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 오토 [스케일링](/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/)은 손님이 많으면 자동으로 직원을 더 부르는 시스템이에요!
2. 손님이 없을 때는 직원을 퇴근시켜서 비용을 아끼고, 손님이 몰릴 때 자동으로 더 불러요!
3. 현대 클라우드는 AI가 손님 패턴을 분석해서 미리 직원을 준비시키는 예측 [스케일링](/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/)도 해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 29 / 371

<- **이전**: [29. 스케일 업 vs 스케일 아웃 (Scale Up vs Scale Out)](/studynote/13_cloud_architecture/01_virtualization/029_scale_up_scale_out/)
**다음**: [31. 로드 밸런서 — 트래픽 분산의 핵심 기술](/studynote/13_cloud_architecture/01_virtualization/031_load_balancer/) ->

---
