---
title: 218. NoSQL BASE (Basically Available, Soft-state, Eventually Consistent) 결과적
  일관성 샤딩
date: '2026-04-21'
tags:
- studynote-data-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: NoSQL의 BASE(Basically Available, Soft-state, Eventually Consistent) [[082_attribute_types_er_model|속성]]은 RDBMS의 ACID([[193_atomicity_all_or_nothing|Atomicity]]·[[194_consistency_database_integrity|Consistency]]·[[195_isolation_concurrency_control|Isolation]]·[[196_durability_permanent_storage|Durability]])와 정반대로, [[136_variance|분산]] 환경에서 강한 [[194_consistency_database_integrity|일관성]] 대신 [[452_availability|가용성]]과 [[282_performance_tactics|성능]]을 택하는 설계 철학이다.
> 2. **가치**: [[650_eventual_consistency|결과적 일관성]]([[650_eventual_consistency|Eventual Consistency]])은 모든 [[016_replication_factor|복제]]본이 시간이 지나면 같은 상태가 된다는 보장으로, 네트워크 [[514_partition_slice_volume|파티션]] 상황에서도 [[090_service_kubernetes_network_load_balancing|서비스]]를 중단하지 않고 계속 응답할 수 있게 한다.
> 3. **판단 포인트**: 금융 계좌 잔액(절대 [[194_consistency_database_integrity|일관성]] 필요)에는 ACID, 소셜미디어 좋아요 수(약간의 불일치 허용)에는 BASE — 비즈니스 [[001_dikw_pyramid|데이터]]의 [[194_consistency_database_integrity|일관성]] 요구 수준이 ACID vs BASE 선택의 기준이다.

---

## Ⅰ. 개요 및 필요성

### 1.1 [[136_variance|분산]] 시스템에서 [[194_consistency_database_integrity|일관성]]의 딜레마

단일 서버 RDBMS는 ACID를 쉽게 보장하지만, 수십 대 서버에 걸친 [[136_variance|분산]] 시스템에서 강한 [[194_consistency_database_integrity|일관성]](Strong [[194_consistency_database_integrity|Consistency]])을 유지하면 막대한 통신 비용과 [[015_지연_데이터_관점|지연]]이 발생한다.

```
ACID 분산 트랜잭션 문제:
  서버 A  ──── 락 획득 ────► 서버 B (응답 대기)
          ◄─── 커밋 확인 ────          │
                                      │ 네트워크 지연
                                      ▼ 50ms 지연
  → 50ms × 수백만 TPS = 시스템 마비
```

Eric Brewer는 2000년 [[341_process|CAP]] 정리로 "[[136_variance|분산]] 시스템은 [[194_consistency_database_integrity|일관성]], [[452_availability|가용성]], [[514_partition_slice_volume|파티션]] 허용성 3가지를 동시에 완벽하게 지킬 수 없다"고 증명했다. NoSQL의 BASE는 이 현실을 반영한 실용적 절충이다.

### 1.2 ACID vs BASE 비교

| 항목 | ACID ([[083_relationship_in_er_model|관계]]형 DB) | BASE ([[035_nosql|NoSQL]]) |
|:---|:---|:---|
| **A** | [[193_atomicity_all_or_nothing|Atomicity]] ([[193_atomicity_all_or_nothing|원자성]]) | Basically Available (기본적 [[452_availability|가용성]]) |
| **C** | [[194_consistency_database_integrity|Consistency]] ([[194_consistency_database_integrity|일관성]]) | Soft-state (소프트 상태) |
| **I** | [[195_isolation_concurrency_control|Isolation]] ([[195_isolation_concurrency_control|격리성]]) | Eventually Consistent ([[650_eventual_consistency|결과적 일관성]]) |
| **D** | [[196_durability_permanent_storage|Durability]] (내구성) | — |
| **우선순위** | [[194_consistency_database_integrity|일관성]] > [[452_availability|가용성]] | [[452_availability|가용성]] > [[194_consistency_database_integrity|일관성]] |
| **장애 시** | [[191_transaction_concept_states|트랜잭션]] 실패, [[090_service_kubernetes_network_load_balancing|서비스]] 대기 | [[090_service_kubernetes_network_load_balancing|서비스]] 계속, 나중에 [[194_consistency_database_integrity|일관성]] [[233_recovery_database_restoration_overview|회복]] |

📢 **섹션 요약 비유**: ACID는 '엄격한 은행 금고' — 문을 열려면 모든 절차가 완벽해야 하고, 뭔가 문제 있으면 문을 잠근다. BASE는 '편의점 셀프 계산대' — 약간의 오류가 있어도 일단 가게는 계속 돌아간다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 BASE [[082_attribute_types_er_model|속성]] 상세 설명

**Basically Available (기본적 [[452_availability|가용성]])**:
네트워크 [[514_partition_slice_volume|파티션]]이나 일부 서버 장애가 발생해도 시스템은 계속 응답한다. 정확하지 않을 수 있지만 오류보다는 부분적 [[001_dikw_pyramid|데이터]]를 반환한다.

```
예: 쇼핑몰 상품 재고 조회
  ACID (RDBMS): 재고 서버 장애 → 전체 쇼핑몰 접속 불가
  BASE (NoSQL): 재고 서버 장애 → "재고 정보 임시 불가" 표시 후 나머지 기능 정상
```

**Soft-state (소프트 상태)**:
시스템의 상태는 고정되지 않고, 시간이 지남에 따라 업데이트 없이도 변할 수 있다. [[016_replication_factor|복제]]([[016_replication_factor|Replication]]) 중인 [[001_dikw_pyramid|데이터]]는 노드마다 잠시 다를 수 있다.

**Eventually Consistent ([[650_eventual_consistency|결과적 일관성]])**:
모든 업데이트가 충분한 시간이 지나면 모든 [[016_replication_factor|복제]]본에 전파된다. "항상 일관적"이 아닌 "결국 일관적"이 됨을 보장한다.

```
결과적 일관성 타임라인:
  t=0  : Node A에 "user=홍길동, 등급=VIP" 업데이트
  t=10ms: Node A 반영 완료, Node B·C는 여전히 "GOLD"
  t=50ms: Node B에 복제 완료
  t=100ms: Node C에 복제 완료 → 모든 노드 일치!

  → 100ms 동안은 노드마다 다른 값을 반환할 수 있음
```

### 2.2 [[280_sharding|샤딩]] ([[243_sharding_horizontal_scaling_database|Sharding]]) — 수평 [[136_variance|분산]] 설계

[[280_sharding|샤딩]]([[243_sharding_horizontal_scaling_database|Sharding]])은 하나의 [[001_dikw_pyramid|데이터]]셋을 여러 서버에 [[136_variance|분산]] 저장하는 수평 [[179_table_partitioning_concept|파티셔닝]](Horizontal [[179_table_partitioning_concept|Partitioning]]) 기법이다.

| [[280_sharding|샤딩]] [[268_strategy_pattern|전략]] | 방식 | 장점 | 단점 |
|:---|:---|:---|:---|
| **[[282_embedded_document_pattern|해시 샤딩]]** | `shard = hash(key) % N` | 균등 [[136_variance|분산]] | 범위 [[298_qkv_attention|쿼리]] 불가 |
| **범위 [[280_sharding|샤딩]]** | `shard = key의 범위 구간` | 범위 [[298_qkv_attention|쿼리]] 용이 | 핫스팟(Hotspot) 위험 |
| **디렉토리 [[280_sharding|샤딩]]** | 별도 매핑 테이블 | 유연한 재배치 | 매핑 테이블 병목 |
| **지리 [[280_sharding|샤딩]]** | 지역별 분리 | [[809_data_sovereignty|데이터 주권]], [[015_지연_데이터_관점|지연]] 감소 | 교차 지역 [[298_qkv_attention|쿼리]] 어려움 |

### 2.3 [[282_embedded_document_pattern|해시 샤딩]] 상세

```
해시 샤딩 (Consistent Hashing, 일관 해시):

사용자 ID → 해시 함수 → 샤드 번호

user_id=1001 → hash=2847  → 샤드 0 (0~3000)
user_id=1002 → hash=7231  → 샤드 2 (6000~9000)
user_id=1003 → hash=5119  → 샤드 1 (3000~6000)

┌──────────┐  ┌──────────┐  ┌──────────┐
│  샤드 0  │  │  샤드 1  │  │  샤드 2  │
│ user 1001│  │ user 1003│  │ user 1002│
│ user ...  │  │ user ...  │  │ user ...  │
└──────────┘  └──────────┘  └──────────┘
   서버 A         서버 B         서버 C
```

**일관 해시([[244_consistent_hashing_ring_distribution|Consistent Hashing]])**: 서버 추가/제거 시 재분배되는 키의 수를 최소화하는 해시 기법. 일반 해시 대비 서버 N개 변경 시 O(K/N) 키만 이동(K=전체 키 수).

### 2.4 [[016_replication_factor|복제]] [[268_strategy_pattern|전략]]과 [[194_consistency_database_integrity|일관성]] 수준

```
Cassandra의 일관성 수준 (Consistency Level):

쓰기 요청
  Client ──────────────────► 코디네이터 노드
                                  │
              ┌───────────────────┼────────────────┐
              ▼                   ▼                ▼
           노드 A              노드 B           노드 C
         (Primary)           (Replica)        (Replica)

Consistency Level 설정:
  ONE    : 1개 노드 확인 → 빠름, 일관성 약함
  QUORUM : (N/2+1)개 확인 → 균형
  ALL    : 모든 노드 확인 → 느림, 일관성 강함
```

📢 **섹션 요약 비유**: [[280_sharding|샤딩]]은 큰 도서관을 여러 분관으로 나눈 것이다 — 과학책은 1분관, 소설책은 2분관처럼 분류하면 각 분관이 독립적으로 작동해서 방문객이 몰려도 한 분관만 막힌다.

---

## Ⅲ. 비교 및 연결

### 3.1 [[650_eventual_consistency|결과적 일관성]] 패턴

| 패턴 | 설명 | 예시 |
|:---|:---|:---|
| **Read Your Writes** | 자신이 쓴 [[001_dikw_pyramid|데이터]]는 항상 읽을 수 있음 | 내 프로필 수정 후 즉시 반영 |
| **Monotonic Read** | 한 번 읽은 버전보다 이전 버전은 안 읽음 | 타임라인이 거꾸로 안 감 |
| **Causal [[194_consistency_database_integrity|Consistency]]** | 인과 [[083_relationship_in_er_model|관계]] 있는 이벤트는 순서 보장 | 답글은 원글 다음에 표시 |

### 3.2 [[035_nosql|NoSQL]] vs RDBMS 선택 기준

```
데이터 구조가 고정적이고 트랜잭션이 중요한가?
  YES → RDBMS (PostgreSQL, MySQL)

데이터 구조가 동적이거나 수평 확장이 필요한가?
  YES → NoSQL

   ├── 단순 키-값 빠른 조회   → Redis / DynamoDB
   ├── JSON 도큐먼트 저장     → MongoDB
   ├── 시계열/대용량 쓰기     → Cassandra / HBase
   └── 관계 탐색              → Neo4j
```

📢 **섹션 요약 비유**: [[650_eventual_consistency|결과적 일관성]]은 인터넷 뉴스 기사가 수정될 때 네이버·다음·구글에 동시에 반영되지 않는 것과 같다 — 잠시 차이가 있지만, 결국 모든 플랫폼이 같은 내용을 보여주게 된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 BASE 설계 패턴 적용 사례

| [[090_service_kubernetes_network_load_balancing|서비스]] | [[001_dikw_pyramid|데이터]] | BASE 이유 |
|:---|:---|:---|
| SNS 좋아요 수 | 수십억 건 | 1~2초 불일치 허용 가능 |
| 전자상거래 장바구니 | 사용자별 상태 | [[160_session_controlling_terminal|세션]] 내 [[194_consistency_database_integrity|일관성]]만 필요 |
| [[511_dns_hierarchical_distributed_architecture|DNS]] 조회 | IP 매핑 | [[016_전파_지연|전파 지연]] 허용 |
| [[506_cdn_content_delivery_network_edge_caching|CDN]] 캐시 | 정적 [[501_file_definition_logical_record|파일]] | [[294_ttl_time_to_live_looping_prevention|TTL]] 기반 [[194_consistency_database_integrity|일관성]] |

### 4.2 [[280_sharding|샤딩]] 시 주의사항

| 항목 | 문제 | 해법 |
|:---|:---|:---|
| **핫스팟** | 특정 샤드에 트래픽 집중 | [[282_embedded_document_pattern|해시 샤딩]] + 가상 노드(Virtual Node) |
| **교차 샤드 [[298_qkv_attention|쿼리]]** | JOIN이 여러 서버 걸침 | 비정규화, [[298_qkv_attention|쿼리]] 라우터 |
| **리샤딩** | 서버 추가 시 [[001_dikw_pyramid|데이터]] 이동 | Consistent Hashing으로 최소화 |
| **[[191_transaction_concept_states|트랜잭션]]** | 멀티 샤드 [[191_transaction_concept_states|트랜잭션]] 불가 | [[312_saga_pattern_choreography_orchestration|사가]]([[305_saga|Saga]]) 패턴, [[549_2pc_two_phase_commit_limitations_msa|2PC]]([[549_2pc_two_phase_commit_limitations_msa|Two-Phase Commit]]) |

📢 **섹션 요약 비유**: [[280_sharding|샤딩]]의 핫스팟 문제는 모든 학생이 학교 앞 한 문구점에 몰리는 것이다 — 여러 문구점으로 [[136_variance|분산]](가상 노드)하거나, 학번 범위를 재배정(리샤딩)해서 부하를 나눠야 한다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 BASE + [[280_sharding|샤딩]] 도입 효과

| 효과 | 내용 |
|:---|:---|
| **[[452_availability|가용성]]** | 단일 노드 장애 시에도 [[090_service_kubernetes_network_load_balancing|서비스]] 계속 가능 |
| **확장성** | 샤드 추가만으로 [[139_throughput|처리량]] 선형 증가 |
| **[[282_performance_tactics|성능]]** | 지역 [[016_replication_factor|복제]]로 읽기 [[015_지연_데이터_관점|지연]] 감소 |
| **비용** | 고가 단일 서버 대신 범용 서버 수평 확장 |

### 5.2 결론 — 기술사 작성 포인트

기술사 답안에서는 **"BASE vs ACID를 단순 대립이 아닌 비즈니스 요건에 따른 트레이드오프"**로 서술해야 한다. "언제 BASE가 적합한가"를 [[650_eventual_consistency|결과적 일관성]]이 허용되는 [[064_relation_domain|도메인]](SNS, 캐시, [[511_dns_hierarchical_distributed_architecture|DNS]])과 허용되지 않는 [[064_relation_domain|도메인]](금융, 재고)을 구분해 논술하고, [[282_embedded_document_pattern|해시 샤딩]]과 일관 해시의 차이를 ASCII로 표현하면 차별화된다.

📢 **섹션 요약 비유**: BASE는 '완벽한 정확성보다 지금 당장 답하는 것'을 선택한 시스템이다 — 선거 출구조사처럼 100% 정확하지 않아도 빠른 예측이 필요한 상황에서 BASE가 빛을 발한다.

---

### 📌 관련 개념 맵

| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| BASE [[082_attribute_types_er_model|속성]] | Basically Available | 부분 장애에도 계속 응답 |
| BASE [[082_attribute_types_er_model|속성]] | Soft-state | [[016_replication_factor|복제]] 중 노드마다 상태 불일치 허용 |
| BASE [[082_attribute_types_er_model|속성]] | Eventually Consistent | 시간 경과 후 모든 노드 일치 |
| 수평 [[136_variance|분산]] | [[280_sharding|샤딩]] ([[243_sharding_horizontal_scaling_database|Sharding]]) | [[001_dikw_pyramid|데이터]]를 여러 서버에 [[136_variance|분산]] |
| [[136_variance|분산]] 해시 | 일관 해시 ([[244_consistent_hashing_ring_distribution|Consistent Hashing]]) | 노드 변경 시 최소 재배치 |
| 비교 개념 | ACID (A·C·I·D) | [[083_relationship_in_er_model|관계]]형 DB [[191_transaction_concept_states|트랜잭션]] 보장 |
| [[341_process|CAP]] 연결 | [[341_process|CAP]] 정리 ([[219_cap_pacelc_distributed_tradeoff|CAP Theorem]]) | [[136_variance|분산]] 시스템 [[194_consistency_database_integrity|일관성]]·[[452_availability|가용성]] 한계 |

### 👶 어린이를 위한 3줄 비유 설명

1. BASE는 '대충 맞아도 괜찮은 학교 투표 결과'야 — 반장 선거에서 딱 맞지 않아도 모두가 결과를 알 수 있으면 돼.

### 📈 관련 키워드 및 발전 흐름도

```text
ACID (RDBMS: 강한 일관성)
    │
    ▼
BASE (NoSQL: 유연한 일관성)
    ├─► Basically Available: 항상 응답
    ├─► Soft State: 시간이 지나면 변할 수 있음
    └─► Eventual Consistency: 최종적 일관성 보장
    │
    ▼
Sharding: 수평 분할 · Consistent Hashing
```
2. [[280_sharding|샤딩]]은 학교 급식 배식대를 여러 줄로 나눈 것이야 — 줄이 많을수록 밥을 빨리 받을 수 있어!
3. [[650_eventual_consistency|결과적 일관성]]은 SNS에서 내가 올린 사진이 모든 친구에게 5초 뒤에 뜨는 것 — 동시에 안 보여도 결국은 다 보게 되잖아?
