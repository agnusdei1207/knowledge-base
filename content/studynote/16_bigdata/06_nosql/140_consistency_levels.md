+++
title = "140. 일관성 수준 선택 (Consistency Levels) — Strong/Eventual/Bounded Staleness"
date = 2026-04-21

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
- **본질**: [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템의 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 수준은 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 얼마나 최신이어야 하는가"와 "그 대가로 얼마나 느리고 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)이 낮아지는가"의 연속적 트레이드오프 스펙트럼이다.
- **가치**: Azure Cosmos DB가 제시한 5가지 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 수준(Strong->Bounded Staleness->[Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)->Consistent Prefix->Eventual)은 워크로드별 최적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)-[성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 균형점을 명시적으로 선택하게 해준다.
- **판단 포인트**: 금융 거래·재고 차감은 Strong, 사용자 프로필 읽기는 [Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/), 소셜 피드는 Eventual로 연산별로 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 수준을 차별화하는 것이 대규모 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 표준 설계 원칙이다.

---

## Ⅰ. 개요 및 필요성

### [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 약화의 필요성

```text
단일 노드 DB: 강한 일관성 자동 보장 (문제 없음)

분산 DB: 노드 간 복제 지연이 항상 존재
          쓰기 -> Node A -> 복제 -> Node B, C, D
          지연: 수ms ~ 수백ms (리전 간)

선택:
  강한 일관성: 모든 복제 확인 후 응답 -> 지연 증가
  약한 일관성: 일부 복제 후 응답 -> 빠르지만 오래된 데이터 가능
```

### Cosmos DB 5가지 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 수준 스펙트럼

```text
+--------------------------------------------------------------+
|          일관성 수준 스펙트럼 (강함 -> 약함)                    |
|                                                              |
|  Strong     Bounded    Session   Consistent   Eventual       |
|    |        Staleness    |         Prefix         |          |
|    |           |         |            |           |          |
|    ●-----------●---------●------------●-----------●          |
|                                                              |
|  일관성: ████████████████████░░░░░░░░░░░░░░░░░░░             |
|  가용성: ░░░░░░░░░░░░░░░░░░░░████████████████████             |
|  지연:   높음 -------------------------------> 낮음            |
|  처리량: 낮음 -------------------------------> 높음            |
+--------------------------------------------------------------+
```

📢 **섹션 요약 비유**
> [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 수준은 뉴스 속보의 신선도 기준과 같다. 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)은 "방금 일어난 사건만" 보도(가장 최신), 최종 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)은 "어제 뉴스도 오늘 보도 가능"(결국 동일). 속보의 정확도를 높일수록 방송이 느려지는 것처럼, [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 강화할수록 응답이 느려진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 5가지 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 수준 상세

```text
+-----------------------------------------------------------------+
|  1. Strong (선형화 가능, Linearizability)                         |
|                                                                 |
|  Write -> [복제 완료 확인] -> Read                                  |
|  보장: 모든 읽기가 가장 최신 쓰기를 반영                            |
|  비용: 가장 높은 지연, 단일 마스터에 의존                           |
|  적합: 금융 거래, 재고 관리, 선거 투표                              |
+-----------------------------------------------------------------+
|  2. Bounded Staleness (한계 있는 부실함)                          |
|                                                                 |
|  최대 K 버전 또는 T 시간만큼 오래된 데이터 허용                      |
|  보장: 지정된 시간/버전 범위 내 일관성                              |
|  비용: Strong보다 낮은 지연                                        |
|  적합: 주가 표시(1초 지연 허용), 실시간 순위표                       |
+-----------------------------------------------------------------+
|  3. Session (세션 일관성)                                         |
|                                                                 |
|  같은 클라이언트 세션 내 읽기-자신의-쓰기 보장                       |
|  다른 세션: Eventual                                             |
|  보장: 내가 쓴 것은 내가 즉시 읽을 수 있음                          |
|  비용: 중간                                                       |
|  적합: 사용자 프로필 수정, SNS 게시글 작성                          |
+-----------------------------------------------------------------+
|  4. Consistent Prefix (일관된 접두사)                             |
|                                                                 |
|  쓰기 순서는 보장, 최신 여부는 미보장                               |
|  A->B->C 순으로 쓰면 읽을 때 A, A+B, A+B+C (순서 역전 없음)         |
|  보장: 인과 관계 순서 유지                                         |
|  적합: 댓글 스레드, 채팅 메시지 순서                                |
+-----------------------------------------------------------------+
|  5. Eventual (최종 일관성)                                        |
|                                                                 |
|  최종적으로 모든 복제본이 동일한 값에 수렴                           |
|  타이밍 보장 없음                                                 |
|  비용: 가장 낮은 지연, 가장 높은 가용성                             |
|  적합: 소셜 좋아요 수, 상품 조회수, DNS                            |
+-----------------------------------------------------------------+
```

### [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 수준과 [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)

```text
CAP 정리와 일관성 스펙트럼:

CP 시스템 (일관성 + 분할 내성):
  -> Strong Consistency 가능
  -> Partition 발생 시 가용성 포기

AP 시스템 (가용성 + 분할 내성):
  -> Eventual Consistency
  -> Partition 발생 시 오래된 데이터 반환 가능

Cosmos DB:
  Strong -> CP 동작
  Eventual -> AP 동작
  Bounded/Session/Prefix -> 중간 지점
```

| [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 수준 | [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 읽기 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/869_sla/) |
|:---:|:---:|:---:|:---:|
| Strong | [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) | 높음 | 99.99% |
| Bounded Staleness | [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) (단일 리전) / [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) | 중간 | 99.99% |
| [Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) | 중간 | 낮음 | 99.999% |
| Consistent Prefix | [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) | 매우 낮음 | 99.999% |
| Eventual | [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) | 최저 | 99.999% |

📢 **섹션 요약 비유**
> 5가지 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 수준은 정보 보고 체계와 같다. Strong은 최고 지휘관(단일 진실)에게 직접 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/), Bounded는 "1시간 이내 보고서만 믿음", Session은 "내가 보낸 것은 내가 즉시 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)", Consistent Prefix는 "순서는 틀리지 않음", Eventual은 "언젠가는 모두 같은 내용을 알게 됨".

---

## Ⅲ. 비교 및 연결

### 시스템별 기본 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 수준

| 시스템 | 기본 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 옵션 |
|:---:|:---:|:---:|
| PostgreSQL/MySQL | [Serializable](/knowledge-base/studynote/05_database/04_transactions_concurrency/231_serializable_isolation_level/) | [READ COMMITTED](/knowledge-base/studynote/05_database/04_transactions_concurrency/229_read_committed_isolation_level/), [REPEATABLE READ](/knowledge-base/studynote/05_database/04_transactions_concurrency/230_repeatable_read_isolation_level/) |
| [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) (단일 노드) | Strong | — |
| [Cassandra](/knowledge-base/studynote/05_database/04_transactions_concurrency/541_cassandra/) | 튜너블 | ONE~ALL (QUORUM 권장) |
| [DynamoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/545_dynamodb/) | Eventual | Strong 읽기 (비용 2배) |
| [MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/) | 주 노드 읽기 | ReadPreference [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) |
| Cosmos DB | [Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) (기본) | 5가지 전부 선택 가능 |

### 벡터 클록 ([Vector Clock](/knowledge-base/studynote/05_database/04_transactions_concurrency/258_vector_clock/))을 통한 인과 순서 추적

```text
벡터 클록: 분산 시스템에서 이벤트 인과 관계 추적

Node A 쓰기: [A:1, B:0, C:0]
Node B가 A 읽고 쓰기: [A:1, B:1, C:0]  <- A의 쓰기가 원인
Node C 독립 쓰기: [A:0, B:0, C:1]      <- A와 무관

충돌 감지: [A:1, B:1] vs [A:1, C:1] -> 동시 쓰기 충돌
해결: Last-Write-Wins, 앱 레벨 병합, CRDT
```

📢 **섹션 요약 비유**
> 벡터 클록은 편지의 발신 날짜와 같다. 편지를 받고 답장을 쓴다면(인과 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)), 내 답장 날짜가 원본 편지 날짜보다 늦어야 한다. 두 편지의 날짜가 같다면([동시 쓰기](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/276_write_through/)), 어느 것이 원본인지 알 수 없어 충돌을 해결해야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 워크로드별 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 수준 결정 가이드

```text
Q1. 금융 거래(계좌 이체, 재고 차감)?
    -> Strong (선형화 필수)

Q2. 사용자가 자신의 프로필을 즉시 확인?
    -> Session (Read-Your-Own-Write)

Q3. 실시간 주가/환율 표시 (1초 지연 허용)?
    -> Bounded Staleness (K=10초)

Q4. 게시글 댓글 순서가 중요?
    -> Consistent Prefix (순서 역전 금지)

Q5. 좋아요 수, 공유 수 (약간 오래된 값 허용)?
    -> Eventual (최대 성능, 최소 비용)
```

### 혼합 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) (Best Practices)

| 연산 | [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 수준 | 이유 |
|:---:|:---:|:---|
| 결제·출금 | Strong | 중복 차감 절대 불가 |
| 재고 조회 | Bounded (5초) | 약간 오래된 재고도 허용 |
| 장바구니 | [Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) | 내가 추가한 것 즉시 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |
| 추천 상품 | Eventual | 약간 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)되어도 무관 |
| 공지사항 | Consistent Prefix | 순서 보장 필요 |

📢 **섹션 요약 비유**
> 혼합 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 병원 정보 시스템과 같다. 수술 기록(Strong)은 정확해야 하고, 병원 식단 메뉴(Eventual)는 어제 것이 나와도 큰 문제없다. 환자 본인의 검사 결과([Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/))는 즉시 볼 수 있어야 하지만, 다른 환자의 병실 번호(Consistent Prefix)는 순서 역전만 없으면 된다.

---

## Ⅴ. 기대효과 및 결론

### [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 수준 선택에 따른 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 영향

| 수준 | 읽기 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) | [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) (P99) | [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 후 읽기 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) |
|:---:|:---:|:---:|:---:|
| Strong | 1× | 높음 | 즉시 최신 |
| Bounded (10s) | 2× | 중간 | 최대 10초 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) |
| [Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) | 3× | 낮음 | 같은 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 즉시 |
| Consistent Prefix | 4× | 매우 낮음 | 순서 보장 |
| Eventual | 5× | 최저 | 미보장 |

### 결론
[일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 수준은 단순한 기술 선택이 아니라 비즈니스 요구 사항의 직접적 반영이다. 연산의 비즈니스 중요도에 따라 차별화된 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 수준을 적용하는 <strong>혼합 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a> <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>이 현대 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 표준이다. 기술사 시험에서는 <strong>5가지 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a> 수준 정의와 적합 워크로드</strong>, <strong><a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/">CAP</a> 정리와 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a> 스펙트럼의 <a href="/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a></strong>, **벡터 클록 기반 충돌 탐지**, <strong>혼합 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a> 설계 패턴</strong>이 핵심 논점이다.

📢 **섹션 요약 비유**
> [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 수준은 자동차 안전 등급처럼 비용과 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 수준의 트레이드오프다. 5성급(Strong)은 비싸지만 가장 안전하고, 3성급([Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/))은 합리적 가격으로 일상 운전에 충분하며, 1성급(Eventual)은 저렴하지만 가벼운 용도에만 적합하다. 용도에 맞는 등급을 선택하는 것이 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---:|:---:|:---|
| [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리 | 이론적 기반 | C, A, P 중 2가지 선택 |
| [PACELC](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/342_pacelc/) | 확장 이론 | 정상 시 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)-[일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 트레이드오프 |
| 선형화 가능성 | Strong 정의 | 전역 단일 복사본처럼 동작 |
| 벡터 클록 | 충돌 탐지 | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 이벤트 인과 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 추적 |
| CRDT | 충돌 해결 | 자동 병합 가능한 자료구조 |


### 📈 관련 키워드 및 발전 흐름도

```text
[CAP 이론 (CAP Theorem) — 일관성·가용성·분할 허용성 트레이드오프]
    |
    v
[강한 일관성 (Strong Consistency) — 모든 노드 즉시 동기화, 지연 증가]
    |
    v
[결과적 일관성 (Eventual Consistency) — 최종 동기화, 성능 우선]
    |
    v
[일관성 수준 조정 (Consistency Level Tuning) — Quorum·ONE·ALL 선택]
    |
    v
[PACELC 모델 — 네트워크 분할 없을 때도 지연 vs 일관성 트레이드오프]
```
[일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 수준은 [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 이론의 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)-[가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 트레이드오프를 운영 환경에서 세분화하여, [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 단위로 강도를 선택할 수 있게 한 NoSQL의 핵심 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)이다.
### 👶 어린이를 위한 3줄 비유 설명
1. [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 수준은 정보의 신선도 기준 — "방금 막 나온 뉴스"(Strong)부터 "어제 뉴스도 OK"(Eventual)까지 얼마나 최신 정보가 필요한지에 따라 골라요.
2. [Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)은 "내가 방금 쓴 일기는 내가 바로 읽을 수 있지만, 다른 친구는 조금 후에 볼 수도 있어요" — 자신의 작업은 즉시 반영돼요.
3. [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 강하게 할수록 DB가 모든 복사본에 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하느라 느려지는 것처럼, 세상에는 빠름과 정확함을 동시에 최대로 얻을 수 없는 트레이드오프가 항상 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 140 / 262

<- **이전**: [139. 인메모리 데이터베이스 (In-Memory DB) — Redis/Memcached/SAP HANA](/knowledge-base/studynote/16_bigdata/06_nosql/139_inmemory_db/)
**다음**: [141. 멀티 마스터 복제 (Multi-Master Replication) — CouchDB/DynamoDB Global Tables](/knowledge-base/studynote/16_bigdata/06_nosql/141_multi_master_replication/) ->

---
