---
title: "EDA, Event-Driven Architecture"
date: "2026-05-08"
tags:
  - "studynote-devops-sre"
weight: 214
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기반 Pub/Sub 플랫폼으로 대규모 이벤트 스트림을 처리하는 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)징 시스템.
> 2. **가치**: [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 비동기 결합과 [데이터 파이프라인](/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/)의 중심 축이 된다.
> 3. **판단 포인트**: [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키와 소비자 재처리 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 중요하다.

---

## Ⅰ. 개요 및 필요성

[이벤트 주도 아키텍처](/studynote/11_design_supervision/06_exam_summary/367_architecture/) ([EDA](/studynote/12_it_management/02_itsm_itil/064_eda/), [Event-Driven Architecture](/studynote/13_cloud_architecture/03_msa_serverless/140_event_driven_architecture_eda/))는 [DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)/[SRE](/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) 환경에서 반복되는 운영 문제를 구조적으로 다루기 위해 등장한 개념이다. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 워크로드는 수집, 변환, 학습, 서빙 단계가 길어 한 지점의 병목이 전체 가치를 떨어뜨리기 쉽다. 핵심은 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기반 Pub/Sub 플랫폼으로 대규모 이벤트 스트림을 처리하는 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)징 시스템에 있다. 이 관점에서 보면, 이 주제는 단순 기술 소개가 아니라 속도와 안정성을 동시에 맞추기 위한 운영 설계 기준에 가깝다.

[파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 경계와 품질 기준이 없으면 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 드리프트, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 불일치가 누적된다. 따라서 [이벤트 주도 아키텍처](/studynote/11_design_supervision/06_exam_summary/367_architecture/)를 이해할 때는 "무엇을 자동화하는가"보다 "어떤 실패와 편차를 줄이려는가"를 먼저 붙잡아야 한다.

```text
Deployment / Control / Feedback Flow

+----------------------+   +----------------------+   +----------------------+   +----------------------+
| Ingestion            |--->| Processing           |--->| Serving              |--->| Governance           |
+----------------------+   +----------------------+   +----------------------+   +----------------------+
```

이 그림은 [이벤트 주도 아키텍처](/studynote/11_design_supervision/06_exam_summary/367_architecture/)가 입력, 실행, [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), 환류를 한 흐름으로 묶는다는 점을 보여준다. 즉 기술 자체보다도 제어 루프와 피드백 구조가 본질이다.

- **📢 섹션 요약 비유**: 수도관처럼 취수, 정수, 저장, 배급이 모두 이어져야 깨끗한 물이 나온다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[이벤트 주도 아키텍처](/studynote/11_design_supervision/06_exam_summary/367_architecture/)의 핵심 원리는 구성 요소를 나열하는 데 있지 않고, 목표 상태를 어떻게 해석하고 실제 상태에 어떻게 반영하며 그 결과를 어떻게 다시 측정하는지에 있다. 특히 전통 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 큐와 달리 [이벤트 주도 아키텍처](/studynote/11_design_supervision/06_exam_summary/367_architecture/)는 실행 전후의 차이와 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 함께 본다는 점에서 운영 품질 차이를 만든다.

| 요소 | 역할 | 기술사 판단 포인트 |
|:---|:---|:---|
| Ingestion | 이벤트, [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), [CDC](/studynote/14_data_engineering/05_exam_keywords/217_cdc_binlog_change_capture_debezium/), 배치 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 수집 | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 [무결성](/studynote/09_security/01_intro_principles/003_integrity/) 기준을 먼저 정의 |
| Processing | 변환, 집계, 모델링, 학습을 수행 | [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)와 품질 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 자동화가 중요 |
| Serving | [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/), 대시보드, 모델 엔드포인트로 제공 | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 캐시, 비용을 함께 고려 |
| Governance | [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/), 라인리지, 드리프트, [접근 통제](/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/)를 관리 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [신뢰도](/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/)와 규제 대응의 핵심 |

```text
Reference Architecture

+----------------------+   +----------------------+   +----------------------+   +----------------------+
| Ingestion            |--->| Processing           |--->| Serving              |--->| Governance           |
+----------------------+   +----------------------+   +----------------------+   +----------------------+
```

위 구조에서 중요한 것은 각 계층의 책임을 분리하면서도, 마지막에 반드시 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) [신호](/studynote/02_operating_system/02_process_thread/130_signal/)가 다시 제어 계층으로 돌아오게 만드는 것이다. 그래야 변경 실패가 누적되지 않고, 재현성과 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 가능성을 함께 확보할 수 있다.

- **📢 섹션 요약 비유**: 창고 물류처럼 입고, [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/), 출고 규칙이 있어야 물건이 쌓여도 흐름이 멈추지 않는다.

---

## Ⅲ. 비교 및 연결

[이벤트 주도 아키텍처](/studynote/11_design_supervision/06_exam_summary/367_architecture/)는 보통 전통 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 큐와 비교할 때 경계가 선명해진다. [이벤트 주도 아키텍처](/studynote/11_design_supervision/06_exam_summary/367_architecture/)가 더 많은 자동화와 제어를 제공하더라도, 모든 상황에서 무조건 우월한 것은 아니다. 시스템 규모, 팀 성숙도, 규제 수준, 운영 복잡도가 함께 맞아야 장점이 실제 성과로 이어진다.

| 비교 축 | [이벤트 주도 아키텍처](/studynote/11_design_supervision/06_exam_summary/367_architecture/) | 전통 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 큐 |
|:---|:---|:---|
| 중심 목표 | [이벤트 주도 아키텍처](/studynote/11_design_supervision/06_exam_summary/367_architecture/)의 목적에 맞춘 제어와 자동화 | 더 전통적이거나 대안적인 운영 방식 |
| 강점 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 비동기 결합과 [데이터 파이프라인](/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/)의 중심 축이 된다. | 구조가 단순하거나 도입 장벽이 낮음 |
| 위험 | [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)와 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 약하면 기대효과가 줄어듦 | 확장성·가시성·자동화 한계가 빨리 드러남 |
| 적합한 상황 | 여러 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소스와 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 팀이 공통 분석·[AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 플랫폼을 공유할 때 특히 효과가 크다. | 변화가 적거나 단순한 환경 |

또한 이 주제는 Topic, [Partition](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/), Offset처럼 주변 개념과 강하게 연결된다. 기술사 관점에서는 개별 정의보다도 이런 연결 구조를 설명해야 답안의 깊이가 생긴다.

- **📢 섹션 요약 비유**: 도서관 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)체계처럼 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)가 있어야 필요한 정보를 빠르게 찾는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [이벤트 주도 아키텍처](/studynote/11_design_supervision/06_exam_summary/367_architecture/)를 도입하는 것 자체보다, 어떤 전제조건이 갖춰졌을 때 효과가 나는지를 묻는 것이 더 중요하다. 여러 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소스와 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 팀이 공통 분석·[AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 플랫폼을 공유할 때 특히 효과가 크다. 따라서 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)와 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)을 함께 보는 습관이 필요하다.

### 적용 체크포인트

1. [이벤트 주도 아키텍처](/studynote/11_design_supervision/06_exam_summary/367_architecture/)의 목표 지표가 명확한가?
2. 자동화 실패 시 되돌릴 절차와 책임이 정의되어 있는가?
3. 관측 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)와 운영 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 실제 배포/운영 루프와 연결되어 있는가?

### 주의할 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 도구만 도입하고 기준·지표·예외 절차를 정하지 않는 경우
- 운영 현실보다 이상적인 그림만 따르고 [피드백 루프](/studynote/15_devops_sre/01_culture_methodology/005_feedback_loop/)를 닫지 못하는 경우

기술사 답안에서는 "도입"만 쓰지 말고, [이벤트 주도 아키텍처](/studynote/11_design_supervision/06_exam_summary/367_architecture/)가 어떤 상황에서는 채택되고 어떤 상황에서는 단계적으로 적용되어야 하는지를 비용, 복잡도, 보안, 운영 역량 기준으로 분리해 적는 것이 좋다.

- **📢 섹션 요약 비유**: 정원 관리처럼 씨앗만 뿌리는 것이 아니라 상태를 보며 물과 비료를 조절해야 좋은 결과가 난다.

---

## Ⅴ. 기대효과 및 결론

[이벤트 주도 아키텍처](/studynote/11_design_supervision/06_exam_summary/367_architecture/)를 잘 적용하면 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름의 재현성과 품질 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 높여 분석과 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 안정적으로 운영하게 만든다. 반면 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)와 거버넌스가 약하면 저장소만 늘고 실제 [신뢰도](/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/)는 오르지 않는다. 결국 핵심은 도구 이름을 외우는 것이 아니라, 제어 기준·상태 정합성·[피드백 루프](/studynote/15_devops_sre/01_culture_methodology/005_feedback_loop/)를 하나의 설계 문제로 보는 것이다.

앞으로는 스트리밍, [Feature Store](/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/), [Vector DB](/studynote/14_data_engineering/03_ml_dl_llm/151_vector_database_embedding_ann_search/), [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 기반 거버넌스가 더 촘촘히 결합된다. 따라서 [이벤트 주도 아키텍처](/studynote/11_design_supervision/06_exam_summary/367_architecture/)는 "한 번 도입하는 기술"이 아니라, 변화가 잦은 시스템을 어떻게 안정적으로 운영할 것인지에 대한 사고 틀로 기억하는 것이 맞다.

- **📢 섹션 요약 비유**: 교통 환승센터처럼 서로 다른 노선과 수단이 연결되어야 이동 효율이 높아진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Topic | [이벤트 주도 아키텍처](/studynote/11_design_supervision/06_exam_summary/367_architecture/)를 이해할 때 직접 연결되는 기반 개념 |
| [Partition](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) | [이벤트 주도 아키텍처](/studynote/11_design_supervision/06_exam_summary/367_architecture/)의 설계·운영 판단 기준을 보완하는 개념 |
| Offset | [이벤트 주도 아키텍처](/studynote/11_design_supervision/06_exam_summary/367_architecture/)를 자동화·확장 측면에서 연결하는 개념 |
| [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) | [이벤트 주도 아키텍처](/studynote/11_design_supervision/06_exam_summary/367_architecture/) 적용 후 후속 발전 방향을 설명하는 개념 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Topic]
    |
    v
[이벤트 주도 아키텍처]
    |
    +---> [Partition]
    +---> [Offset]
    +---> [Kafka]
```

이 흐름도는 [이벤트 주도 아키텍처](/studynote/11_design_supervision/06_exam_summary/367_architecture/)가 선행 개념 위에 서서 운영 자동화, 보안, 확장, 가시성 중 어떤 축으로 확장되는지를 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)해서 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. [이벤트 주도 아키텍처](/studynote/11_design_supervision/06_exam_summary/367_architecture/)는 복잡한 일을 순서와 규칙으로 정리해서 실수하지 않게 도와주는 방법이에요.
2. Topic 같은 친구들과 같이 움직여야 더 잘 작동해요.
3. 그래서 문제가 생겨도 어디서 틀렸는지 빨리 찾고 다시 고치기 쉬워져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 214 / 373

<- **이전**: [213. 데이터베이스 퍼 서비스 (Database per Service)](/studynote/15_devops_sre/05_devsecops/213_database_per_service_db_api/)
**다음**: [215. 서버리스 (Serverless / FaaS) 아키텍처](/studynote/15_devops_sre/05_devsecops/215_serverless_faas_1_aws_lambda/) ->

---
