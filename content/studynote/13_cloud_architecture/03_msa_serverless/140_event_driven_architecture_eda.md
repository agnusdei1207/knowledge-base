---
title: "140. Event Driven Architecture Eda"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: EDA는 <strong>이벤트(상태 변화 알림)를 중심으로 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 간 통신을 설계</strong>하는 아키텍처이며, 이벤트 생산자->이벤트 브로커([Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/))->이벤트 소비자의 비동기·느슨 결합 구조이다.
> 2. **가치**: 동기 호출([REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/))은 호출자가 <strong>응답까지 블로킹</strong>되고 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 강결합이지만, EDA는 <strong>비동기·느슨 결합</strong>으로 확장성·탄력성이 높다.
> 3. **판단 포인트**: Event Notification(알림)·Event-Carried [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) Transfer(상태 전달)·[Event Sourcing](/studynote/12_it_management/05_security_compliance/307_event_sourcing/)(이벤트 저장) 3가지 패턴을 구분하며, [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/)·EventBridge·SNS/SQS가 핵심 인프라이다.

---

## Ⅰ. 개요 및 필요성

```text
동기 (REST): A->B->C (체이닝, 블로킹)
비동기 (EDA): A->이벤트->Kafka->B, C (독립 소비, 비블로킹)
  -> 생산자·소비자 독립 -> 느슨 결합 -> 확장성^
```

- **📢 섹션 요약 비유**: REST는 전화(응답 대기), EDA는 <strong>게시판(올리면 관심있는 사람이 봄)</strong>이다.

---

## Ⅱ~Ⅴ. 결론

EDA는 <strong>MSA의 느슨 결합·확장성을 실현하는 핵심 아키텍처</strong>이며, Kafka가 이벤트 브로커의 사실상 표준이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/12_it_management/02_itsm_itil/064_eda/">EDA</a></strong> | [이벤트 기반 아키텍처](/studynote/04_software_engineering/09_cloud_native_ai_architecture/538_event_driven_architecture_eda/) |
| <strong><a href="/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/">Kafka</a></strong> | 이벤트 브로커 |
| **Pub/Sub** | 발행/구독 패턴 |
| <strong><a href="/studynote/12_it_management/05_security_compliance/307_event_sourcing/">Event Sourcing</a></strong> | [EDA](/studynote/12_it_management/02_itsm_itil/064_eda/) 고급 패턴 |
| <strong><a href="/studynote/12_it_management/05_security_compliance/306_cqrs/">CQRS</a></strong> | EDA와 결합 |

### 📈 관련 키워드 및 발전 흐름도

```text
[동기 RPC (2000s)] -> [메시지 큐 (RabbitMQ, 2007)]
    -> [Kafka (2011, 대용량 이벤트)]
    -> [EDA + MSA (2016~)]
    -> [현재: EventBridge·Eventarc — 서버리스 EDA]
```

### 👶 어린이를 위한 3줄 비유 설명
1. EDA는 <strong>게시판</strong>이에요. 소식(이벤트)을 올리면 **관심있는 사람이 봐요**.
2. 전화([REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/))처럼 **기다리지 않아도** 돼서 빨라요.
3. 새 소식을 **여러 사람이 동시에** 볼 수 있어서 효율적이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 139 / 371

<- **이전**: [139. CQRS (Command Query Responsibility Segregation) - 명령·조회 분리](/studynote/13_cloud_architecture/03_msa_serverless/139_cqrs_msa/)
**다음**: [141. Microservice Chassis - MSA 공통 관심사 프레임워크](/studynote/13_cloud_architecture/03_msa_serverless/141_microservice_chassis/) ->

---
