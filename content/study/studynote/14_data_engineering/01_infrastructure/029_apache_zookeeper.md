---
title: 29. Apache ZooKeeper
date: '2026-04-29'
tags:
- studynote-data-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Apache ZooKeeper는 [[136_variance|분산]] 시스템의 조율(Coordination) [[090_service_kubernetes_network_load_balancing|서비스]]다. [[136_variance|분산]] 잠금(Distributed [[510_lock|Lock]]), 리더 선출(Leader Election), [[009_config|설정]] 관리([[009_config|Config]]), [[306_service_discovery_pattern|서비스 디스커버리]]([[303_service_discovery|Service Discovery]])를 [[194_consistency_database_integrity|일관성]] 있게 제공하는 [[136_variance|분산]] [[086_CP_순환_전치_GI|CP]] 시스템이다.
> 2. **가치**: [[136_variance|분산]] 환경에서 "두 노드가 동시에 같은 결정을 내리는 것"([[190_split_brain_zookeeper_fencing_quorum|스플릿 브레인]], [[190_split_brain_zookeeper_fencing_quorum|Split Brain]])을 방지한다. ZAB([[798_distributed_lock_zookeeper_consensus|ZooKeeper]] Atomic Broadcast) [[295_protocol_field_tcp_udp_icmp|프로토콜]]로 과반수(쿼럼) 합의를 보장하여 [[194_consistency_database_integrity|일관성]]을 제공한다.
> 3. **판단 포인트**: ZooKeeper는 [[179_kafka_flink_watermark_time_window|Kafka]], [[543_hbase|HBase]], [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] [[020_yarn|YARN]], Solr의 핵심 의존성이었으나 운영 복잡성으로 인해 대안이 등장했다. Kafka는 KRaft(내장 [[259_raft_paxos|Raft]])로 [[798_distributed_lock_zookeeper_consensus|ZooKeeper]] 의존성 제거([[179_kafka_flink_watermark_time_window|Kafka]] 3.3+), [[078_etcd_distributed_key_value_store|etcd]]([[196_kubernetes_k8s_container_orchestration|쿠버네티스]]), Consul이 현대적 대안이다.

---

## Ⅰ. 개요 및 필요성

```text
┌──────────────────────────────────────────────────────────┐
│          ZooKeeper 분산 조율 서비스                        │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  분산 잠금:    노드 A      ZooKeeper     노드 B           │
│               "잠금 요청" →  [Lock Znode] ← "대기"       │
│               잠금 획득 → 작업 수행 → 잠금 해제           │
│                                                           │
│  리더 선출:   노드1, 노드2, 노드3가 경쟁                   │
│               → ZooKeeper가 공정한 리더 선출              │
│               → 리더 장애 시 자동 재선출                  │
│                                                           │
│  ZooKeeper 앙상블 (최소 3개, 홀수 권장):                   │
│  [ZK1] [ZK2] [ZK3]  → 과반수(2개) 살아있으면 정상 운영   │
└──────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: ZooKeeper는 [[136_variance|분산]] 시스템의 신뢰할 수 있는 공증인이다. 여러 서버가 "내가 리더야!"라고 주장할 때, ZooKeeper라는 공증인이 공정하게 하나만 인정하고 나머지에게 통보한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[798_distributed_lock_zookeeper_consensus|ZooKeeper]] znode ([[014_data_model_components|데이터 모델]])

```text
ZooKeeper 데이터 트리 (/):
  /kafka/
    /brokers/
      /0001  → broker 1 연결 정보
      /0002  → broker 2 연결 정보
    /controller → 현재 컨트롤러(리더) 브로커 ID

znode 타입:
  persistent: 클라이언트 연결 끊겨도 유지
  ephemeral:  클라이언트 세션 종료 시 자동 삭제 (리더 선출에 활용)
  sequential: 순서 번호 자동 부여 (공정한 잠금 구현)
```

### ZAB [[295_protocol_field_tcp_udp_icmp|프로토콜]]

```text
ZAB (ZooKeeper Atomic Broadcast):
  1. Leader가 변경 사항 제안 (Proposal)
  2. 과반수(n/2+1) Follower가 ACK
  3. Leader가 COMMIT 전파
  → 모든 노드 동일 순서로 상태 업데이트 보장
```

- **📢 섹션 요약 비유**: ZAB [[295_protocol_field_tcp_udp_icmp|프로토콜]]은 민주주의 투표 시스템이다. 대통령(Leader)이 법안(변경사항)을 제출하면 국회의원(Follower) 과반수가 동의해야 통과된다. 과반수 미달이면 부결된다.

---

## Ⅲ. 비교 및 연결

| 비교 | [[798_distributed_lock_zookeeper_consensus|ZooKeeper]] | [[078_etcd_distributed_key_value_store|etcd]] | Consul |
|:---|:---|:---|:---|
| 합의 | ZAB | [[259_raft_paxos|Raft]] | [[259_raft_paxos|Raft]] |
| 사용처 | [[179_kafka_flink_watermark_time_window|Kafka]], [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] | [[205_kubernetes_container_orchestration|Kubernetes]] | [[302_service_mesh_istio|서비스 메시]] |
| 복잡성 | 높음 | 낮음 | 중간 |
| 현황 | 레거시 의존 | [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 표준 | HashiCorp |

- **📢 섹션 요약 비유**: [[798_distributed_lock_zookeeper_consensus|ZooKeeper]] vs [[078_etcd_distributed_key_value_store|etcd]] vs Consul은 공증인 세 명이다. ZooKeeper는 오래된 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 있는 공증인(복잡하지만 검증됨), etcd는 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 마을의 공식 공증인(간단·현대적), Consul은 [[531_cloud_native_architecture|클라우드 네이티브]] 환경 전문 공증인이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[179_kafka_flink_watermark_time_window|Kafka]] [[798_distributed_lock_zookeeper_consensus|ZooKeeper]] 의존성 제거

```text
전통 Kafka 아키텍처:
  Kafka Broker + ZooKeeper 앙상블 분리 운영
  → ZooKeeper 관리 부담, ZK-Kafka 버전 호환 이슈

Kafka KRaft (Kafka 3.3+, 2022):
  Kafka 내장 Raft 합의 프로토콜
  → ZooKeeper 완전 제거 가능
  → 단일 클러스터 운영, 관리 단순화
  → 메타데이터 처리 성능 10배 향상
```

### [[798_distributed_lock_zookeeper_consensus|ZooKeeper]] 적용 사례

```text
HBase: 마스터 서버 선출, RegionServer 등록
Hadoop YARN: ResourceManager HA
SolrCloud: 클러스터 상태·컬렉션 메타데이터 관리
Kafka (2.x 이하): 컨트롤러 선출, 토픽 메타데이터
```

- **�� 섹션 요약 비유**: [[179_kafka_flink_watermark_time_window|Kafka]] KRaft는 공증인([[798_distributed_lock_zookeeper_consensus|ZooKeeper]])을 회사 내부로 인수한 것이다. 외부 공증인에게 매번 의뢰하는 대신, 회사 내부 법무팀(KRaft)을 만들어서 더 빠르고 간편하게 처리한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **[[136_variance|분산]] [[194_consistency_database_integrity|일관성]]** | 과반수 합의로 [[190_split_brain_zookeeper_fencing_quorum|Split Brain]] 방지 |
| **고가용성** | 앙상블로 장애 내성 |
| **범용 조율** | 잠금·리더·[[009_config|설정]]·디스커버리 통합 |

ZooKeeper는 대규모 [[136_variance|분산]] 시스템의 조율 [[090_service_kubernetes_network_load_balancing|서비스]] 표준을 정립했다. 현재는 [[179_kafka_flink_watermark_time_window|Kafka]] KRaft, [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] etcd로 대체되는 추세지만, ZooKeeper가 해결한 [[136_variance|분산]] 조율 문제(리더 선출, [[136_variance|분산]] 잠금, [[194_consistency_database_integrity|일관성]])는 모든 현대 [[136_variance|분산]] 시스템에서 여전히 핵심 과제다.

- **📢 섹션 요약 비유**: ZooKeeper의 레거시는 고등학교 수학의 기초와 같다. 지금은 계산기([[179_kafka_flink_watermark_time_window|Kafka]] KRaft, [[078_etcd_distributed_key_value_store|etcd]])를 쓰지만, ZooKeeper가 해결한 [[136_variance|분산]] 조율 원리를 이해하면 모든 현대 [[136_variance|분산]] 시스템을 더 깊이 이해할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[259_raft_paxos|Raft]]/ZAB** | [[136_variance|분산]] 합의 [[295_protocol_field_tcp_udp_icmp|프로토콜]] |
| **[[078_etcd_distributed_key_value_store|etcd]]** | [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 핵심 조율 [[090_service_kubernetes_network_load_balancing|서비스]] |
| **KRaft** | [[179_kafka_flink_watermark_time_window|Kafka]] 내장 [[798_distributed_lock_zookeeper_consensus|ZooKeeper]] 대체 |
| **리더 선출** | [[136_variance|분산]] 시스템 핵심 조율 패턴 |
| **[[341_process|CAP]] 정리** | ZooKeeper는 [[086_CP_순환_전치_GI|CP]] 시스템 |

### 📈 관련 키워드 및 발전 흐름도

```text
[분산 시스템 조율 문제 — Split Brain, 리더 선출]
    │
    ▼
[Apache ZooKeeper — ZAB 프로토콜, 범용 조율 서비스]
    │
    ▼
[etcd — Raft 기반, Kubernetes 표준 조율]
    │
    ▼
[Kafka KRaft — ZooKeeper 의존성 제거]
    │
    ▼
[서비스 메시 — Consul 기반 서비스 디스커버리]
```

### 👶 어린이를 위한 3줄 비유 설명

1. ZooKeeper는 여러 컴퓨터가 동시에 같은 결정을 내리지 않도록 조율하는 공증인이에요!
2. 리더 선출, 잠금 관리, [[009_config|설정]] 공유 등 [[136_variance|분산]] 시스템의 핵심 문제를 해결해줘요!
3. 요즘 Kafka는 ZooKeeper를 없애고 내부 직접 조율(KRaft)로 더 간단하게 운영한답니다!
