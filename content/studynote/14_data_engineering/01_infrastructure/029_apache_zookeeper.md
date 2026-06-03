+++
title = "29. Apache ZooKeeper"
date = 2026-04-29

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Apache ZooKeeper는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템의 조율(Coordination) [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)다. [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 잠금(Distributed [Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/)), 리더 선출(Leader Election), [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 관리([Config](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)), [서비스 디스커버리](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/306_service_discovery_pattern/)([Service Discovery](/knowledge-base/studynote/12_it_management/05_security_compliance/303_service_discovery/))를 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 있게 제공하는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) 시스템이다.
> 2. **가치**: [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에서 "두 노드가 동시에 같은 결정을 내리는 것"([스플릿 브레인](/knowledge-base/studynote/14_data_engineering/04_mlops/190_split_brain_zookeeper_fencing_quorum/), [Split Brain](/knowledge-base/studynote/14_data_engineering/04_mlops/190_split_brain_zookeeper_fencing_quorum/))을 방지한다. ZAB([ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) Atomic Broadcast) [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)로 과반수(쿼럼) 합의를 보장하여 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 제공한다.
> 3. **판단 포인트**: ZooKeeper는 [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/), [HBase](/knowledge-base/studynote/05_database/04_transactions_concurrency/543_hbase/), [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) [YARN](/knowledge-base/studynote/14_data_engineering/01_infrastructure/020_yarn/), Solr의 핵심 의존성이었으나 운영 복잡성으로 인해 대안이 등장했다. Kafka는 KRaft(내장 [Raft](/knowledge-base/studynote/05_database/04_transactions_concurrency/259_raft_paxos/))로 [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) 의존성 제거([Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 3.3+), [etcd](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/)([쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)), Consul이 현대적 대안이다.

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

- **📢 섹션 요약 비유**: ZooKeeper는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템의 신뢰할 수 있는 공증인이다. 여러 서버가 "내가 리더야!"라고 주장할 때, ZooKeeper라는 공증인이 공정하게 하나만 인정하고 나머지에게 통보한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) znode ([데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/))

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

### ZAB [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)

```text
ZAB (ZooKeeper Atomic Broadcast):
  1. Leader가 변경 사항 제안 (Proposal)
  2. 과반수(n/2+1) Follower가 ACK
  3. Leader가 COMMIT 전파
  → 모든 노드 동일 순서로 상태 업데이트 보장
```

- **📢 섹션 요약 비유**: ZAB [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)은 민주주의 투표 시스템이다. 대통령(Leader)이 법안(변경사항)을 제출하면 국회의원(Follower) 과반수가 동의해야 통과된다. 과반수 미달이면 부결된다.

---

## Ⅲ. 비교 및 연결

| 비교 | [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) | [etcd](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/) | Consul |
|:---|:---|:---|:---|
| 합의 | ZAB | [Raft](/knowledge-base/studynote/05_database/04_transactions_concurrency/259_raft_paxos/) | [Raft](/knowledge-base/studynote/05_database/04_transactions_concurrency/259_raft_paxos/) |
| 사용처 | [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/), [Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) | [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) | [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/) |
| 복잡성 | 높음 | 낮음 | 중간 |
| 현황 | 레거시 의존 | [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 표준 | HashiCorp |

- **📢 섹션 요약 비유**: [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) vs [etcd](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/) vs Consul은 공증인 세 명이다. ZooKeeper는 오래된 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 있는 공증인(복잡하지만 검증됨), etcd는 [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 마을의 공식 공증인(간단·현대적), Consul은 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 환경 전문 공증인이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) 의존성 제거

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

### [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) 적용 사례

```text
HBase: 마스터 서버 선출, RegionServer 등록
Hadoop YARN: ResourceManager HA
SolrCloud: 클러스터 상태·컬렉션 메타데이터 관리
Kafka (2.x 이하): 컨트롤러 선출, 토픽 메타데이터
```

- **�� 섹션 요약 비유**: [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) KRaft는 공증인([ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/))을 회사 내부로 인수한 것이다. 외부 공증인에게 매번 의뢰하는 대신, 회사 내부 법무팀(KRaft)을 만들어서 더 빠르고 간편하게 처리한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a></strong> | 과반수 합의로 [Split Brain](/knowledge-base/studynote/14_data_engineering/04_mlops/190_split_brain_zookeeper_fencing_quorum/) 방지 |
| **고가용성** | 앙상블로 장애 내성 |
| **범용 조율** | 잠금·리더·[설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)·디스커버리 통합 |

ZooKeeper는 대규모 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템의 조율 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 표준을 정립했다. 현재는 [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) KRaft, [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) etcd로 대체되는 추세지만, ZooKeeper가 해결한 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 조율 문제(리더 선출, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 잠금, [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/))는 모든 현대 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템에서 여전히 핵심 과제다.

- **📢 섹션 요약 비유**: ZooKeeper의 레거시는 고등학교 수학의 기초와 같다. 지금은 계산기([Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) KRaft, [etcd](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/))를 쓰지만, ZooKeeper가 해결한 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 조율 원리를 이해하면 모든 현대 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템을 더 깊이 이해할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/259_raft_paxos/">Raft</a>/ZAB</strong> | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 합의 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/">etcd</a></strong> | [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 핵심 조율 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) |
| **KRaft** | [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 내장 [ZooKeeper](/knowledge-base/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/) 대체 |
| **리더 선출** | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템 핵심 조율 패턴 |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/">CAP</a> 정리</strong> | ZooKeeper는 [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) 시스템 |

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
2. 리더 선출, 잠금 관리, [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 공유 등 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템의 핵심 문제를 해결해줘요!
3. 요즘 Kafka는 ZooKeeper를 없애고 내부 직접 조율(KRaft)로 더 간단하게 운영한답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 29 / 258

← **이전**: [28. Apache Hive](/knowledge-base/studynote/14_data_engineering/01_infrastructure/028_apache_hive/)
**다음**: [30. 스플릿 브레인과 쿼럼 — 분산 시스템 합의 문제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/030_split_brain_quorum/) →

---
