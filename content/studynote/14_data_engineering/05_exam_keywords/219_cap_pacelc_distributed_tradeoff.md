---
title: 219. CAP 정리 (CAP Theorem)와 PACELC 정리 분산 트레이드오프
date: '2026-04-21'
tags:
- studynote-data-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[341_process|CAP]] 정리([[341_process|CAP]] Theorem)는 [[136_variance|분산]] 시스템에서 [[194_consistency_database_integrity|일관성]]([[194_consistency_database_integrity|Consistency]])·[[452_availability|가용성]]([[452_availability|Availability]])·[[514_partition_slice_volume|파티션]] 내결함성([[514_partition_slice_volume|Partition]] Tolerance) 세 가지를 **동시에 모두 보장하는 것은 불가능**함을 수학적으로 증명한 원칙이다.
> 2. **가치**: [[342_pacelc|PACELC]] 정리는 CAP의 P([[514_partition_slice_volume|파티션]] 발생 시) 이외에도 **E(정상 운영 시)의 [[015_지연_데이터_관점|지연]]-[[194_consistency_database_integrity|일관성]] 트레이드오프**를 추가하여 더 현실적인 [[136_variance|분산]] DB 선택 기준을 제공한다.
> 3. **판단 포인트**: "[[194_consistency_database_integrity|일관성]] vs [[452_availability|가용성]]"은 단순한 기술 선택이 아니라 **비즈니스 요건(금융거래 vs 소셜피드)**에 따른 [[268_strategy_pattern|전략]]적 판단이므로, 기술사 논술에서는 [[064_relation_domain|도메인]] 맥락과 함께 선택 근거를 반드시 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

### [[341_process|CAP]] 정리 등장 배경

2000년 에릭 브루어(Eric Brewer)가 PODC(Principles of Distributed Computing) 컨퍼런스에서 가설로 제시하고, 2002년 세스 길버트(Seth Gilbert)와 낸시 린치(Nancy Lynch)가 수학적으로 증명한 이론이다.

인터넷 서비스의 폭발적 성장으로 단일 서버로는 처리 불가능한 규모의 시스템이 등장했고, [[136_variance|분산]] 시스템 설계 원칙에 대한 체계적 이해가 필요해졌다.

### [[341_process|CAP]] 세 가지 [[082_attribute_types_er_model|속성]] 정의

| [[082_attribute_types_er_model|속성]] | 영문 | 정의 |
|:---|:---|:---|
| **[[194_consistency_database_integrity|일관성]]** | [[194_consistency_database_integrity|Consistency]] | 모든 노드가 동시에 동일한 최신 [[001_dikw_pyramid|데이터]]를 반환 |
| **[[452_availability|가용성]]** | [[452_availability|Availability]] | 모든 요청이 (오류 없이) 응답을 반환 |
| **[[514_partition_slice_volume|파티션]] 내결함성** | [[514_partition_slice_volume|Partition]] Tolerance | 네트워크 분단(메시지 손실)이 발생해도 시스템이 계속 동작 |

**핵심 명제**: [[136_variance|분산]] 시스템에서 네트워크 [[514_partition_slice_volume|파티션]](P)은 피할 수 없으므로, [[514_partition_slice_volume|파티션]] 발생 시 C와 A 중 하나를 선택해야 한다.

📢 **섹션 요약 비유**: 두 지점 은행이 있는데 통신이 끊겼다. **같은 잔액을 보여주려면 거래를 멈춰야 하고(C 선택)**, **계속 거래하려면 잔액이 달라질 수 있다(A 선택)**. 둘 다는 불가능하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[341_process|CAP]] [[104_classification_analysis|분류]]에 따른 DB 유형

```
┌─────────────────────────────────────────────────────────┐
│                    CAP 트라이앵글                        │
│                                                         │
│                    ┌─────────────┐                     │
│                    │ Consistency │                     │
│                    │     (C)     │                     │
│                    └──────┬──────┘                     │
│                           │                            │
│          CA               │              CP            │
│   ┌──────────────┐        │      ┌──────────────┐     │
│   │ Traditional  │        │      │  MongoDB     │     │
│   │ RDBMS        │        │      │  HBase       │     │
│   │ (단일 서버)  │        │      │  Zookeeper   │     │
│   └──────────────┘        │      └──────────────┘     │
│                           │                            │
│   ┌─────────┐─────────────┴──────────────┬─────────┐  │
│   │Availab  │                            │Partition│  │
│   │ility(A) │                            │ Tol.(P) │  │
│   └─────────┘                            └─────────┘  │
│                     AP                                 │
│              ┌──────────────┐                         │
│              │  Cassandra   │                         │
│              │  DynamoDB    │                         │
│              │  CouchDB     │                         │
│              └──────────────┘                         │
└─────────────────────────────────────────────────────────┘
```

### [[342_pacelc|PACELC]] 정리 (Extended [[341_process|CAP]])

다니엘 아베이드(Daniel Abadi, 2012)가 제안. CAP은 [[514_partition_slice_volume|파티션]] 발생 시의 선택만 다루지만, **정상 운영(Else) 상황에서도 [[015_지연_데이터_관점|지연]]([[141_latency|Latency]]) vs [[194_consistency_database_integrity|일관성]]([[194_consistency_database_integrity|Consistency]]) 트레이드오프**가 존재함을 추가.

```
PACELC 표기법:
P → [A 또는 C]  (파티션 발생 시)
E → [L 또는 C]  (정상 시)

예시:
Cassandra: PA/EL (파티션 시 가용성 우선, 정상 시 지연 우선)
BigTable:  PC/EC (파티션 시 일관성 우선, 정상 시 일관성 우선)
DynamoDB:  PA/EL (기본, 설정 변경 가능)
```

| DB | [[341_process|CAP]] [[104_classification_analysis|분류]] | [[342_pacelc|PACELC]] | 특징 |
|:---|:---|:---|:---|
| **[[541_cassandra|Cassandra]]** | [[572_ap_access_point_ds_distribution_system|AP]] | PA/EL | [[650_eventual_consistency|결과적 일관성]], 고가용성 |
| **[[543_hbase|HBase]]** | [[086_CP_순환_전치_GI|CP]] | [[164_pc|PC]]/EC | 강한 [[194_consistency_database_integrity|일관성]], [[514_partition_slice_volume|파티션]] 시 대기 |
| **[[540_mongodb|MongoDB]]** | [[086_CP_순환_전치_GI|CP]] (기본) | [[164_pc|PC]]/EC | 리더 기반 [[194_consistency_database_integrity|일관성]] |
| **[[545_dynamodb|DynamoDB]]** | [[572_ap_access_point_ds_distribution_system|AP]] (기본) | PA/EL | 튜닝 가능한 [[194_consistency_database_integrity|일관성]] |
| **[[798_distributed_lock_zookeeper_consensus|Zookeeper]]** | [[086_CP_순환_전치_GI|CP]] | [[164_pc|PC]]/EC | [[136_variance|분산]] 합의(Consensus) |
| **[[542_redis|Redis]] Cluster** | [[572_ap_access_point_ds_distribution_system|AP]] | PA/EL | 고속 캐시, [[650_eventual_consistency|결과적 일관성]] |

📢 **섹션 요약 비유**: PACELC는 CAP에 **평소 날씨 요금표**를 추가한 것이다. 태풍([[514_partition_slice_volume|파티션]]) 때는 어쩔 수 없지만, 맑은 날에도 빠른 배달(저지연)과 정확한 재고 [[396_validation|확인]]([[194_consistency_database_integrity|일관성]]) 중 무엇을 우선할지 정해야 한다.

---

## Ⅲ. 비교 및 연결

### CAP의 한계와 오해

**한계:**
1. "2개만 선택" 표현이 오해를 유발 → 실제로는 P는 필수, C와 A의 **정도(degree)** 조절
2. [[194_consistency_database_integrity|일관성]]과 [[452_availability|가용성]]은 0/1이 아닌 스펙트럼 (Tunable [[194_consistency_database_integrity|Consistency]])
3. 네트워크 [[514_partition_slice_volume|파티션]] 빈도가 낮을 때는 C+A에 근접 가능

**[[650_eventual_consistency|결과적 일관성]]([[650_eventual_consistency|Eventual Consistency]])의 현실:**
- 모든 업데이트가 결국 전파되면 [[194_consistency_database_integrity|일관성]] 달성
- [[212_synchronization_mechanisms|동기화]] [[141_latency|지연 시간]](Lag): 수ms ~ 수초
- 충돌 해결(Conflict Resolution): 최신 타임스탬프, LWW(Last Write Wins), CRDT

### [[136_variance|분산]] [[011_consensus_algorithm|합의 알고리즘]]과의 연계

[[086_CP_순환_전치_GI|CP]] 시스템은 강한 [[194_consistency_database_integrity|일관성]]을 위해 **[[136_variance|분산]] 합의([[403_consensus_pow_pos_bft|Distributed Consensus]])** [[001_algorithm_definition|알고리즘]] 필요:
- **Paxos**: 리더 선출과 값 합의 (Chubby, [[798_distributed_lock_zookeeper_consensus|ZooKeeper]])
- **[[259_raft_paxos|Raft]]**: Paxos보다 이해하기 쉬운 [[011_consensus_algorithm|합의 알고리즘]] ([[078_etcd_distributed_key_value_store|etcd]], TiKV)
- **Multi-Paxos**: 고성능 스트림 합의 (Spanner, Chubby)

📢 **섹션 요약 비유**: [[136_variance|분산]] 합의는 **위원회 의결**과 같다. 과반수가 동의해야 결정이 나고, 한 명이 자리를 비워도 회의가 계속될 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[064_relation_domain|도메인]]별 [[086_CP_순환_전치_GI|CP]] vs [[572_ap_access_point_ds_distribution_system|AP]] 선택 기준

| [[064_relation_domain|도메인]] | 권장 선택 | 이유 |
|:---|:---|:---|
| **금융 거래** | [[086_CP_순환_전치_GI|CP]] ([[194_consistency_database_integrity|일관성]] 우선) | 잔액 불일치 = 치명적 비즈니스 오류 |
| **SNS 피드** | [[572_ap_access_point_ds_distribution_system|AP]] ([[452_availability|가용성]] 우선) | 잠깐 다른 피드를 보여줘도 무해 |
| **의료 시스템** | [[086_CP_순환_전치_GI|CP]] | 환자 [[001_dikw_pyramid|데이터]] [[002_bigdata_5v|정확성]]이 생명과 직결 |
| **상품 재고** | 혼합 (Tunable) | 주문 시 [[086_CP_순환_전치_GI|CP]], 재고 표시 시 [[572_ap_access_point_ds_distribution_system|AP]] |
| **[[511_dns_hierarchical_distributed_architecture|DNS]] 시스템** | [[572_ap_access_point_ds_distribution_system|AP]] | 전 세계 고가용성이 최우선 |
| **[[136_variance|분산]] 잠금** | [[086_CP_순환_전치_GI|CP]] | [[014_concurrency|동시성]] 제어 [[002_bigdata_5v|정확성]] 필수 |

### Tunable [[194_consistency_database_integrity|Consistency]] (조정 가능한 [[194_consistency_database_integrity|일관성]])

Cassandra의 예:
```
쓰기 일관성: QUORUM (과반수 노드 확인)
읽기 일관성: QUORUM (과반수 노드에서 읽기)
→ 강한 일관성 달성

쓰기 일관성: ONE (1개 노드 확인)
읽기 일관성: ONE
→ 최고 성능, 결과적 일관성
```

📢 **섹션 요약 비유**: Tunable Consistency는 **자동차 서스펜션 조절**과 같다. 고속도로([[282_performance_tactics|성능]])냐 비포장도로(안정성)냐에 따라 세팅을 바꿀 수 있다.

---

## Ⅴ. 기대효과 및 결론

### [[341_process|CAP]]/[[342_pacelc|PACELC]] 이해의 실무 가치

| 가치 | 설명 |
|:---|:---|
| DB 선택 근거 제시 | 요건에 맞는 [[035_nosql|NoSQL]]/[[058_newsql_google_spanner_truetime_distributed_transaction|NewSQL]] 선택 체계화 |
| 장애 시나리오 설계 | 네트워크 [[514_partition_slice_volume|파티션]] 발생 시 시스템 동작 예측 |
| [[194_consistency_database_integrity|일관성]] 수준 협상 | 비즈니스 팀과 기술 팀의 트레이드오프 논의 |
| 아키텍처 문서화 | 설계 결정의 명시적 근거 제공 |

### 결론

[[341_process|CAP]] 정리와 [[342_pacelc|PACELC]] 정리는 [[136_variance|분산]] [[002_database_definition|데이터베이스]] 설계의 **나침반**이다. "무엇이 최고인가"가 아니라 "어떤 상황에서 무엇을 포기할 것인가"를 명확히 하는 도구다. 기술사 논술에서는 선택한 DB가 [[341_process|CAP]]/[[342_pacelc|PACELC]] 상 어디에 위치하는지, 그 선택이 비즈니스 요건과 어떻게 정합하는지를 논리적으로 전개해야 한다.

📢 **섹션 요약 비유**: [[341_process|CAP]] 정리는 **삼각형 균형 퍼즐**이다. 한쪽을 늘리면 다른 쪽이 줄어든다. 완벽한 삼각형은 없지만, 용도에 맞는 모양을 고르는 것이 기술자의 역할이다.

---

### 📌 관련 개념 맵

| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| 이론적 기반 | [[341_process|CAP]] 정리 | [[136_variance|분산]] 시스템 3속성 불가능성 증명 |
| 확장 이론 | [[342_pacelc|PACELC]] 정리 | 정상 운영 시 [[015_지연_데이터_관점|지연]]-[[194_consistency_database_integrity|일관성]] 추가 |
| [[086_CP_순환_전치_GI|CP]] 예시 | [[543_hbase|HBase]], [[798_distributed_lock_zookeeper_consensus|ZooKeeper]], [[540_mongodb|MongoDB]] | [[194_consistency_database_integrity|일관성]] 우선 [[136_variance|분산]] DB |
| [[572_ap_access_point_ds_distribution_system|AP]] 예시 | [[541_cassandra|Cassandra]], [[545_dynamodb|DynamoDB]], CouchDB | [[452_availability|가용성]] 우선 [[136_variance|분산]] DB |
| [[011_consensus_algorithm|합의 알고리즘]] | Paxos, [[259_raft_paxos|Raft]] | [[086_CP_순환_전치_GI|CP]] 시스템 [[194_consistency_database_integrity|일관성]] 구현 |
| 유연 [[194_consistency_database_integrity|일관성]] | Tunable [[194_consistency_database_integrity|Consistency]] | 요청별 [[194_consistency_database_integrity|일관성]] 수준 조정 |
| 충돌 해결 | CRDT, LWW | [[572_ap_access_point_ds_distribution_system|AP]] 시스템 [[001_dikw_pyramid|데이터]] 병합 [[268_strategy_pattern|전략]] |

### 👶 어린이를 위한 3줄 비유 설명

1. 두 개의 장난감 창고가 있는데 전화가 끊겼어. **"재고가 정확해야 해"([[194_consistency_database_integrity|일관성]])**를 선택하면 전화 고칠 때까지 팔 수 없고, **"일단 계속 팔기"([[452_availability|가용성]])**를 선택하면 재고가 달라질 수 있어.

### 📈 관련 키워드 및 발전 흐름도

```text
CAP 정리: C(일관성) · A(가용성) · P(파티션 내성) — 3개 동시 불가
    │
    ▼
CP 시스템: HBase · ZooKeeper (일관성 우선)
AP 시스템: Cassandra · DynamoDB (가용성 우선)
    │
    ▼
PACELC: 정상 시 Latency vs Consistency 트레이드오프 추가
    │
    ▼
Tunable Consistency: 워크로드별 일관성 수준 조절
```
2. CAP은 이 두 개를 **동시에 완벽하게 할 수는 없다**는 수학적 증명이야.
3. PACELC는 여기서 더 나아가 **평소 전화가 잘 될 때도** 빠른 응답과 정확한 재고 중 뭘 더 중요하게 볼지 물어보는 거야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 219 / 258

← **이전**: [[218_nosql_base_eventual_consistency_sharding|218. NoSQL BASE (Basically Available, Soft-state, Eventually Consistent) 결과적]]
**다음**: [[220_nosql_types_keyvalue_document_wide_column_graph|220. NoSQL 유형 비교: 키-값·도큐먼트·Wide-Column·그래프 (NoSQL Types Comparison)]] →

---
