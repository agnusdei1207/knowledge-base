---
title: BASE 원칙 (Basically Available, Soft State, Eventual Consistency)
date: '2024-05-22'
tags:
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)
- **[[452_availability|가용성]] 우선([[452_availability|Availability]] First):** [[001_dikw_pyramid|데이터]]의 엄격한 [[194_consistency_database_integrity|일관성]](ACID)을 희생하더라도, 대규모 [[136_variance|분산]] 환경에서 중단 없는 [[090_service_kubernetes_network_load_balancing|서비스]]를 제공하는 NoSQL의 핵심 철학임.
- **[[650_eventual_consistency|결과적 일관성]]([[650_eventual_consistency|Eventual Consistency]]):** 실시간으로 [[001_dikw_pyramid|데이터]]가 일치하지 않을 수 있지만, 일정 시간이 지나면 모든 노드가 동일한 값을 갖게 됨을 보장함.
- **확장성 극대화:** [[136_variance|분산]] 시스템의 [[341_process|CAP]] 정리에서 [[452_availability|가용성]](A)과 [[514_partition_slice_volume|파티션]] 감내(P)를 선택하여 전 세계 사용자에게 빠른 응답 속도를 제공함.

### Ⅰ. 개요 ([[033_context|Context]] & Background)
1. **RDBMS의 한계:** 전통적인 ACID([[193_atomicity_all_or_nothing|원자성]], [[194_consistency_database_integrity|일관성]], [[443_isolation_concurrency_control|고립성]], 지속성)는 [[001_dikw_pyramid|데이터]]의 [[003_integrity|무결성]]을 보장하지만, 수천 개의 서버가 연결된 빅데이터 환경에서는 [[282_performance_tactics|성능]] 저하와 [[452_availability|가용성]] 하락을 유발함.
2. **BASE의 탄생:** 대규모 웹 [[090_service_kubernetes_network_load_balancing|서비스]](Amazon, Google)에서 수평 확장([[202_scale_out_distributed_horizontal_expansion|Scale-out]])을 위해 [[194_consistency_database_integrity|일관성]]을 "결과적"으로 타협하되, [[452_availability|가용성]]을 극대화하는 새로운 [[191_transaction_concept_states|트랜잭션]] 모델이 필요하게 됨.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **BASE Principle Workflow & Distributed [[016_replication_factor|Replication]]**
```text
[ Data Write (Node A) ]      [ Propagation Delay ]      [ Data Read (Node B) ]
+---------------------+      +-------------------+      +---------------------+
| Value = 10 (Update) | --- (Asynchronous Sync) ---> | Value = 5 (Soft State)|
+---------------------+                                 +---------------------+
                                       |                           |
                                       |                           v
                                       |                (Eventually Consistency)
                                       +--------------> | Value = 10 (Synced) |
                                                        +---------------------+
[ Key Pillars of BASE ]
1. BA: Basically Available (기본적 가용성)
2. S : Soft State (소프트 스테이트)
3. E : Eventual Consistency (결과적 일관성)
```

1. **Basically Available ([[103_ba_as_is_analysis|BA]]):**
   - 시스템의 일부분에 장애가 발생하더라도, 전체 시스템이 멈추지 않고 기본적인 응답을 제공함. 완벽한 응답은 아니더라도 가용한 상태를 유지함.
2. **Soft [[272_state_pattern|State]] (S):**
   - [[001_dikw_pyramid|데이터]]의 상태가 외부의 입력 없이도 시간이 지남에 따라 변할 수 있음. 노드 간 [[212_synchronization_mechanisms|동기화]]가 [[216_progress_in_synchronization|진행]] 중일 때, 특정 시점의 [[001_dikw_pyramid|데이터]]는 "확정된 상태"가 아닐 수 있음을 의미함.
3. **[[650_eventual_consistency|Eventual Consistency]] (E):**
   - 특정 시간 동안 새로운 업데이트가 없다면, 결국 모든 [[016_replication_factor|복제]]본(Replica)은 동일한 값으로 수렴함. 일시적인 불일치를 허용하여 [[282_performance_tactics|성능]] 병목을 제거함.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | ACID (RDBMS) | BASE ([[035_nosql|NoSQL]]) | 융합 분석 |
| :--- | :--- | :--- | :--- |
| **핵심 가치** | [[194_consistency_database_integrity|일관성]] ([[194_consistency_database_integrity|Consistency]]) | [[452_availability|가용성]] ([[452_availability|Availability]]) | ACID는 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]], BASE는 [[282_performance_tactics|성능]] |
| **시스템 상태** | 강한 [[194_consistency_database_integrity|일관성]] (Strong) | [[650_eventual_consistency|결과적 일관성]] (Eventual) | [[001_dikw_pyramid|데이터]] 중요도에 따라 혼용 |
| **[[191_transaction_concept_states|트랜잭션]] 관리** | 비관적 락 (Pessimistic) | 낙관적 방식 (Optimistic) | [[014_concurrency|동시성]] 제어 방식의 차이 |
| **확장성** | 수직 확장 ([[621_scale_up_system_bus|Scale-up]]) | 수평 확장 ([[202_scale_out_distributed_horizontal_expansion|Scale-out]]) | 빅데이터 처리는 수평 확장이 대세 |
| **사용 사례** | 금융, 결제, 인사 관리 | SNS, [[568_logs_distributed_logging_elk_fluentd|로그]], 카트, 댓글 | 정합성 vs 실시간성 선택 |

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)
1. **비즈니스 [[064_relation_domain|도메인]]별 선택 ([[268_strategy_pattern|Strategy]]):**
   - **SNS 뉴스피드:** 친구의 글이 1초 늦게 보여도 문제없으므로 BASE가 적합함.
   - **계좌 이체:** 1원이라도 틀리면 치명적이므로 반드시 ACID를 유지해야 함.
2. **기술사적 판단:** 현대 아키텍처는 "[[132_polyglot_persistence|Polyglot Persistence]]"를 지향함. 주문 정보는 RDBMS(ACID)에, 대량의 상품 조회 [[568_logs_distributed_logging_elk_fluentd|로그]]는 [[035_nosql|NoSQL]](BASE)에 저장하여 [[282_performance_tactics|성능]]과 안전성을 동시에 확보하는 것이 핵심 설계 역량임.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
1. **기대효과:** 전 지구적 규모의 [[136_variance|분산]] 시스템(Global Distribution)에서 [[141_latency|지연 시간]]([[141_latency|Latency]])을 최소화하고, 무한한 확장을 가능하게 하여 현대 인터넷 [[090_service_kubernetes_network_load_balancing|서비스]]의 기술적 근간이 됨.
2. **결론:** BASE는 [[194_consistency_database_integrity|일관성]]을 포기한 것이 아니라, [[282_performance_tactics|성능]]을 위해 "[[194_consistency_database_integrity|일관성]]의 시점"을 늦춘 지혜로운 타협임. [[136_variance|분산]] [[027_database_designer|데이터베이스 설계자]]는 BASE 원칙을 통해 [[090_service_kubernetes_network_load_balancing|서비스]] [[452_availability|가용성]]의 [[431_ssthresh_slow_start_threshold|임계치]]를 돌파할 수 있음.

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **상위 개념:** [[136_variance|분산]] [[002_database_definition|데이터베이스]], [[035_nosql|NoSQL]]
- **하위 개념:** [[650_eventual_consistency|결과적 일관성]], [[452_availability|가용성]] ([[452_availability|Availability]])
- **연관 개념:** [[341_process|CAP]] 정리, [[342_pacelc|PACELC]] 이론, ACID

### 📈 관련 키워드 및 발전 흐름도

```text
[상위 개념: 분산 데이터베이스, NoSQL]
    │
    ▼
[하위 개념: 결과적 일관성, 가용성 (Availability)]
    │
    ▼
[연관 개념: CAP 정리, PACELC 이론, ACID]
```

이 흐름도는 상위 개념: [[136_variance|분산]] [[002_database_definition|데이터베이스]], NoSQL에서 출발해 연관 개념: [[341_process|CAP]] 정리, [[342_pacelc|PACELC]] 이론, ACID까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
- **ACID 식당:** 주방장이 모든 테이블의 요리를 완벽하게 다 만들 때까지 손님을 한 명도 안 들여보내는 깐깐한 식당이에요.
- **BASE 식당:** 일단 손님을 다 받고 음식을 조금씩 주면서, 나중에는 모두가 맛있는 요리를 배부르게 먹을 수 있게 조절하는 인기 식당이에요.
- **결론:** 처음엔 조금 복잡해 보일 수 있어도, 결국에는 모두가 행복해지는 마법 같은 순서 맞추기랍니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 124 / 262

← **이전**: [[123_nosql_architecture|NoSQL 아키텍처와 분산 데이터 모델링 (NoSQL Architecture)]]
**다음**: [[125_cap_theorem_distributed_db|CAP 정리 (CAP Theorem)]] →

---
