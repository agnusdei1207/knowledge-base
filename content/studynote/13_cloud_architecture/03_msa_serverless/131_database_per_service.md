---
title: 131. Database per Service - MSA 데이터 분리 패턴
date: '2026-04-19'
tags:
- studynote-cloud-architecture
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[501_database|Database]] per Service는 **각 마이크로서비스가 독립적인 [[001_dikw_pyramid|데이터]]베이스를 소유**하여 다른 [[090_service_kubernetes_network_load_balancing|서비스]]가 직접 DB에 접근하지 못하고 **오직 API로만 통신**하는 [[619_msa_traffic_hardware|MSA]] [[001_dikw_pyramid|데이터]] 패턴이다.
> 2. **가치**: 공유 DB에서는 한 [[090_service_kubernetes_network_load_balancing|서비스]]의 [[005_schema|스키마]] 변경이 **다른 모든 [[090_service_kubernetes_network_load_balancing|서비스]]에 영향**을 주지만, DB per Service는 **독립 배포·독립 [[249_scaling_normalization_standardization|스케일링]]·기술 다양성([[132_polyglot_persistence|Polyglot Persistence]])**을 보장한다.
> 3. **판단 포인트**: [[090_service_kubernetes_network_load_balancing|서비스]] 간 JOIN이 불가능해지므로 **[[305_saga|Saga]]([[248_distributed_transaction_multiple_nodes|분산 트랜잭션]])·[[306_cqrs|CQRS]]([[298_qkv_attention|쿼리]] 분리)·[[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]]**이 함께 필요하며, [[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]]은 **[[650_eventual_consistency|Eventual Consistency]]**로 관리한다.

---

## Ⅰ. 개요 및 필요성

```text
공유 DB: 서비스 A·B·C → 같은 DB (커플링)
DB per Service: A→DB_A, B→DB_B, C→DB_C (독립)
  서비스 간: API·이벤트로만 통신
```

- **📢 섹션 요약 비유**: 공유 DB는 **공동 냉장고**(한 사람이 정리하면 다른 사람 물건이 밀려남), DB per Service는 **각자 냉장고**(독립 관리).

---

## Ⅱ. 아키텍처 및 핵심 원리

| 비교 | 공유 DB | DB per [[090_service_kubernetes_network_load_balancing|Service]] |
|:---|:---|:---|
| **커플링** | 높음 | **낮음** |
| **배포** | 종속 | **독립** |
| **[[521_join|JOIN]]** | 가능 | **불가 → [[014_api_posix|API]]/이벤트** |
| **[[194_consistency_database_integrity|일관성]]** | Strong | **Eventual** |

---

## Ⅲ~Ⅴ. 결론

DB per Service는 **MSA의 [[004_data_independence|데이터 독립성]] 핵심 원칙**이며, [[305_saga|Saga]]·[[306_cqrs|CQRS]]·[[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]]과 함께 적용해야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **DB per [[090_service_kubernetes_network_load_balancing|Service]]** | [[090_service_kubernetes_network_load_balancing|서비스]]별 독립 DB |
| **[[305_saga|Saga]]** | [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]] 패턴 |
| **[[306_cqrs|CQRS]]** | 명령/[[298_qkv_attention|쿼리]] 분리 |
| **[[650_eventual_consistency|Eventual Consistency]]** | 최종 [[194_consistency_database_integrity|일관성]] |
| **[[132_polyglot_persistence|Polyglot Persistence]]** | [[090_service_kubernetes_network_load_balancing|서비스]]별 다른 DB 기술 |

### 📈 관련 키워드 및 발전 흐름도

```text
[공유 DB (모노리스)] → [DB per Service (MSA, 2014~)]
    → [Saga 패턴 (분산 트랜잭션)]
    → [CQRS + Event Sourcing (2016~)]
    → [현재: 데이터 메시 — 도메인별 데이터 소유]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 공유 DB는 **공동 냉장고**예요. 한 사람이 정리하면 **다른 사람 물건이 밀려나요**.
2. DB per Service는 **각자 냉장고**예요. 자기 냉장고를 **독립적으로 관리**해요.
3. 대신 남의 냉장고 물건이 필요하면 **부탁([[014_api_posix|API]])**해야 한답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 130 / 371

← **이전**: [[130_bulkhead_pattern|130. Bulkhead 패턴 - 격벽으로 장애 격리]]
**다음**: [[132_polyglot_persistence|132. Polyglot Persistence - MSA 서비스별 최적 DB 선택]] →

---
