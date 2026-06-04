---
title: "219. CAP 정리 (CAP Theorem)와 PACELC 정리 분산 트레이드오프"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리([CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/) Theorem)는 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템에서 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)([Consistency](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/))·[가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)([Availability](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/))·[파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 내결함성([Partition](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) Tolerance) 세 가지를 <strong>동시에 모두 보장하는 것은 불가능</strong>함을 수학적으로 증명한 원칙이다.
> 2. **가치**: [PACELC](/studynote/13_cloud_architecture/05_data_engineering/342_pacelc/) 정리는 CAP의 P([파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 발생 시) 이외에도 <strong>E(정상 운영 시)의 <a href="/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a>-<a href="/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a> 트레이드오프</strong>를 추가하여 더 현실적인 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) DB 선택 기준을 제공한다.
> 3. **판단 포인트**: "[일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) vs [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)"은 단순한 기술 선택이 아니라 <strong>비즈니스 요건(금융거래 vs 소셜피드)</strong>에 따른 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 판단이므로, 기술사 논술에서는 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 맥락과 함께 선택 근거를 반드시 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

### [CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리 등장 배경

2000년 에릭 브루어(Eric Brewer)가 PODC(Principles of Distributed Computing) 컨퍼런스에서 가설로 제시하고, 2002년 세스 길버트(Seth Gilbert)와 낸시 린치(Nancy Lynch)가 수학적으로 증명한 이론이다.

인터넷 서비스의 폭발적 성장으로 단일 서버로는 처리 불가능한 규모의 시스템이 등장했고, [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템 설계 원칙에 대한 체계적 이해가 필요해졌다.

### [CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/) 세 가지 [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 정의

| [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) | 영문 | 정의 |
|:---|:---|:---|
| <strong><a href="/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a></strong> | [Consistency](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 모든 노드가 동시에 동일한 최신 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 반환 |
| <strong><a href="/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a></strong> | [Availability](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) | 모든 요청이 (오류 없이) 응답을 반환 |
| <strong><a href="/studynote/02_operating_system/09_file_system/514_partition_slice_volume/">파티션</a> 내결함성</strong> | [Partition](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) Tolerance | 네트워크 분단(메시지 손실)이 발생해도 시스템이 계속 동작 |

**핵심 명제**: [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템에서 네트워크 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)(P)은 피할 수 없으므로, [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 발생 시 C와 A 중 하나를 선택해야 한다.

📢 **섹션 요약 비유**: 두 지점 은행이 있는데 통신이 끊겼다. **같은 잔액을 보여주려면 거래를 멈춰야 하고(C 선택)**, **계속 거래하려면 잔액이 달라질 수 있다(A 선택)**. 둘 다는 불가능하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/) [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)에 따른 DB 유형

```
+---------------------------------------------------------+
|                    CAP 트라이앵글                        |
|                                                         |
|                    +-------------+                     |
|                    | Consistency |                     |
|                    |     (C)     |                     |
|                    +------+------+                     |
|                           |                            |
|          CA               |              CP            |
|   +--------------+        |      +--------------+     |
|   | Traditional  |        |      |  MongoDB     |     |
|   | RDBMS        |        |      |  HBase       |     |
|   | (단일 서버)  |        |      |  Zookeeper   |     |
|   +--------------+        |      +--------------+     |
|                           |                            |
|   +---------+-------------+--------------+---------+  |
|   |Availab  |                            |Partition|  |
|   |ility(A) |                            | Tol.(P) |  |
|   +---------+                            +---------+  |
|                     AP                                 |
|              +--------------+                         |
|              |  Cassandra   |                         |
|              |  DynamoDB    |                         |
|              |  CouchDB     |                         |
|              +--------------+                         |
+---------------------------------------------------------+
```

### [PACELC](/studynote/13_cloud_architecture/05_data_engineering/342_pacelc/) 정리 (Extended [CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/))

다니엘 아베이드(Daniel Abadi, 2012)가 제안. CAP은 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 발생 시의 선택만 다루지만, <strong>정상 운영(Else) 상황에서도 <a href="/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a>(<a href="/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/">Latency</a>) vs <a href="/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a>(<a href="/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">Consistency</a>) 트레이드오프</strong>가 존재함을 추가.

```
PACELC 표기법:
P -> [A 또는 C]  (파티션 발생 시)
E -> [L 또는 C]  (정상 시)

예시:
Cassandra: PA/EL (파티션 시 가용성 우선, 정상 시 지연 우선)
BigTable:  PC/EC (파티션 시 일관성 우선, 정상 시 일관성 우선)
DynamoDB:  PA/EL (기본, 설정 변경 가능)
```

| DB | [CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/) [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) | [PACELC](/studynote/13_cloud_architecture/05_data_engineering/342_pacelc/) | 특징 |
|:---|:---|:---|:---|
| <strong><a href="/studynote/05_database/04_transactions_concurrency/541_cassandra/">Cassandra</a></strong> | [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) | PA/EL | [결과적 일관성](/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/), 고가용성 |
| <strong><a href="/studynote/05_database/04_transactions_concurrency/543_hbase/">HBase</a></strong> | [CP](/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) | [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)/EC | 강한 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 시 대기 |
| <strong><a href="/studynote/05_database/04_transactions_concurrency/540_mongodb/">MongoDB</a></strong> | [CP](/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) (기본) | [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)/EC | 리더 기반 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) |
| <strong><a href="/studynote/05_database/04_transactions_concurrency/545_dynamodb/">DynamoDB</a></strong> | [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) (기본) | PA/EL | 튜닝 가능한 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) |
| <strong><a href="/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/">Zookeeper</a></strong> | [CP](/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) | [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)/EC | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 합의(Consensus) |
| <strong><a href="/studynote/05_database/04_transactions_concurrency/542_redis/">Redis</a> Cluster</strong> | [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) | PA/EL | 고속 캐시, [결과적 일관성](/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/) |

📢 **섹션 요약 비유**: PACELC는 CAP에 <strong>평소 날씨 요금표</strong>를 추가한 것이다. 태풍([파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)) 때는 어쩔 수 없지만, 맑은 날에도 빠른 배달(저지연)과 정확한 재고 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)([일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)) 중 무엇을 우선할지 정해야 한다.

---

## Ⅲ. 비교 및 연결

### CAP의 한계와 오해

**한계:**
1. "2개만 선택" 표현이 오해를 유발 -> 실제로는 P는 필수, C와 A의 **정도(degree)** 조절
2. [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)과 [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)은 0/1이 아닌 스펙트럼 (Tunable [Consistency](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/))
3. 네트워크 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 빈도가 낮을 때는 C+A에 근접 가능

<strong><a href="/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/">결과적 일관성</a>(<a href="/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/">Eventual Consistency</a>)의 현실:</strong>
- 모든 업데이트가 결국 전파되면 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 달성
- [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) [지연 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)(Lag): 수ms ~ 수초
- 충돌 해결(Conflict Resolution): 최신 타임스탬프, LWW(Last Write Wins), CRDT

### [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [합의 알고리즘](/studynote/06_ict_convergence/01_blockchain/011_consensus_algorithm/)과의 연계

[CP](/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) 시스템은 강한 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 위해 <strong><a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 합의(<a href="/studynote/07_enterprise_systems/09_digital_transformation/403_consensus_pow_pos_bft/">Distributed Consensus</a>)</strong> [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 필요:
- **Paxos**: 리더 선출과 값 합의 (Chubby, [ZooKeeper](/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/))
- <strong><a href="/studynote/05_database/04_transactions_concurrency/259_raft_paxos/">Raft</a></strong>: Paxos보다 이해하기 쉬운 [합의 알고리즘](/studynote/06_ict_convergence/01_blockchain/011_consensus_algorithm/) ([etcd](/studynote/13_cloud_architecture/02_iaas_paas_saas/078_etcd_distributed_key_value_store/), TiKV)
- **Multi-Paxos**: 고성능 스트림 합의 (Spanner, Chubby)

📢 **섹션 요약 비유**: [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 합의는 <strong>위원회 의결</strong>과 같다. 과반수가 동의해야 결정이 나고, 한 명이 자리를 비워도 회의가 계속될 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)별 [CP](/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) vs [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 선택 기준

| [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) | 권장 선택 | 이유 |
|:---|:---|:---|
| **금융 거래** | [CP](/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) ([일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 우선) | 잔액 불일치 = 치명적 비즈니스 오류 |
| **SNS 피드** | [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) ([가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 우선) | 잠깐 다른 피드를 보여줘도 무해 |
| **의료 시스템** | [CP](/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) | 환자 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [정확성](/studynote/16_bigdata/01_intro/002_bigdata_5v/)이 생명과 직결 |
| **상품 재고** | 혼합 (Tunable) | 주문 시 [CP](/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/), 재고 표시 시 [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) |
| <strong><a href="/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/">DNS</a> 시스템</strong> | [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) | 전 세계 고가용성이 최우선 |
| <strong><a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 잠금</strong> | [CP](/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) | [동시성](/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 제어 [정확성](/studynote/16_bigdata/01_intro/002_bigdata_5v/) 필수 |

### Tunable [Consistency](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) (조정 가능한 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/))

Cassandra의 예:
```
쓰기 일관성: QUORUM (과반수 노드 확인)
읽기 일관성: QUORUM (과반수 노드에서 읽기)
-> 강한 일관성 달성

쓰기 일관성: ONE (1개 노드 확인)
읽기 일관성: ONE
-> 최고 성능, 결과적 일관성
```

📢 **섹션 요약 비유**: Tunable Consistency는 <strong>자동차 서스펜션 조절</strong>과 같다. 고속도로([성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/))냐 비포장도로(안정성)냐에 따라 세팅을 바꿀 수 있다.

---

## Ⅴ. 기대효과 및 결론

### [CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/)/[PACELC](/studynote/13_cloud_architecture/05_data_engineering/342_pacelc/) 이해의 실무 가치

| 가치 | 설명 |
|:---|:---|
| DB 선택 근거 제시 | 요건에 맞는 [NoSQL](/studynote/14_data_engineering/01_infrastructure/035_nosql/)/[NewSQL](/studynote/14_data_engineering/01_infrastructure/058_newsql_google_spanner_truetime_distributed_transaction/) 선택 체계화 |
| 장애 시나리오 설계 | 네트워크 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 발생 시 시스템 동작 예측 |
| [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 수준 협상 | 비즈니스 팀과 기술 팀의 트레이드오프 논의 |
| 아키텍처 문서화 | 설계 결정의 명시적 근거 제공 |

### 결론

[CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리와 [PACELC](/studynote/13_cloud_architecture/05_data_engineering/342_pacelc/) 정리는 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 설계의 <strong>나침반</strong>이다. "무엇이 최고인가"가 아니라 "어떤 상황에서 무엇을 포기할 것인가"를 명확히 하는 도구다. 기술사 논술에서는 선택한 DB가 [CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/)/[PACELC](/studynote/13_cloud_architecture/05_data_engineering/342_pacelc/) 상 어디에 위치하는지, 그 선택이 비즈니스 요건과 어떻게 정합하는지를 논리적으로 전개해야 한다.

📢 **섹션 요약 비유**: [CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리는 <strong>삼각형 균형 퍼즐</strong>이다. 한쪽을 늘리면 다른 쪽이 줄어든다. 완벽한 삼각형은 없지만, 용도에 맞는 모양을 고르는 것이 기술자의 역할이다.

---

### 📌 관련 개념 맵

| [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 이론적 기반 | [CAP](/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리 | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템 3속성 불가능성 증명 |
| 확장 이론 | [PACELC](/studynote/13_cloud_architecture/05_data_engineering/342_pacelc/) 정리 | 정상 운영 시 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)-[일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 추가 |
| [CP](/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) 예시 | [HBase](/studynote/05_database/04_transactions_concurrency/543_hbase/), [ZooKeeper](/studynote/02_operating_system/11_exam_summary/798_distributed_lock_zookeeper_consensus/), [MongoDB](/studynote/05_database/04_transactions_concurrency/540_mongodb/) | [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 우선 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) DB |
| [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 예시 | [Cassandra](/studynote/05_database/04_transactions_concurrency/541_cassandra/), [DynamoDB](/studynote/05_database/04_transactions_concurrency/545_dynamodb/), CouchDB | [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 우선 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) DB |
| [합의 알고리즘](/studynote/06_ict_convergence/01_blockchain/011_consensus_algorithm/) | Paxos, [Raft](/studynote/05_database/04_transactions_concurrency/259_raft_paxos/) | [CP](/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) 시스템 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 구현 |
| 유연 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | Tunable [Consistency](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 요청별 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 수준 조정 |
| 충돌 해결 | CRDT, LWW | [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 시스템 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 병합 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |

### 👶 어린이를 위한 3줄 비유 설명

1. 두 개의 장난감 창고가 있는데 전화가 끊겼어. <strong>"재고가 정확해야 해"(<a href="/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a>)</strong>를 선택하면 전화 고칠 때까지 팔 수 없고, <strong>"일단 계속 팔기"(<a href="/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a>)</strong>를 선택하면 재고가 달라질 수 있어.

### 📈 관련 키워드 및 발전 흐름도

```text
CAP 정리: C(일관성) · A(가용성) · P(파티션 내성) — 3개 동시 불가
    |
    v
CP 시스템: HBase · ZooKeeper (일관성 우선)
AP 시스템: Cassandra · DynamoDB (가용성 우선)
    |
    v
PACELC: 정상 시 Latency vs Consistency 트레이드오프 추가
    |
    v
Tunable Consistency: 워크로드별 일관성 수준 조절
```
2. CAP은 이 두 개를 <strong>동시에 완벽하게 할 수는 없다</strong>는 수학적 증명이야.
3. PACELC는 여기서 더 나아가 **평소 전화가 잘 될 때도** 빠른 응답과 정확한 재고 중 뭘 더 중요하게 볼지 물어보는 거야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 219 / 258

<- **이전**: [218. NoSQL BASE (Basically Available, Soft-state, Eventually Consistent) 결과적](/studynote/14_data_engineering/05_exam_keywords/218_nosql_base_eventual_consistency_sharding/)
**다음**: [220. NoSQL 유형 비교: 키-값·도큐먼트·Wide-Column·그래프 (NoSQL Types Comparison)](/studynote/14_data_engineering/05_exam_keywords/220_nosql_types_keyvalue_document_wide_column_graph/) ->

---
