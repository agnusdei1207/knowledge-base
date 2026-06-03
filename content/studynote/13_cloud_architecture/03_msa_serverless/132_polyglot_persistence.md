---
title: 132. Polyglot Persistence - MSA 서비스별 최적 DB 선택
date: '2026-04-19'
tags:
- studynote-cloud-architecture
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Polyglot Persistence는 **각 마이크로서비스가 자신의 [[001_dikw_pyramid|데이터]] 특성에 가장 적합한 DB 기술을 독립적으로 선택**하는 패턴이며, DB per Service의 자연스러운 확장이다.
> 2. **가치**: 모든 [[090_service_kubernetes_network_load_balancing|서비스]]가 같은 RDBMS를 사용하면 **[[070_graph_datastructure|그래프]] [[001_dikw_pyramid|데이터]]에 [[521_join|JOIN]] 지옥, 시계열에 비효율 [[298_qkv_attention|쿼리]]**가 발생하지만, Polyglot은 **주문=RDB, 추천=[[070_graph_datastructure|그래프]]DB, [[568_logs_distributed_logging_elk_fluentd|로그]]=시계열DB**로 최적화한다.
> 3. **판단 포인트**: 운영 복잡도(다양한 DB 관리)가 증가하므로, **관리형 [[090_service_kubernetes_network_load_balancing|서비스]](RDS·[[545_dynamodb|DynamoDB]]·Neptune)**로 운영 부담을 줄이는 것이 현실적이다.

---

## Ⅰ. 개요 및 필요성

```text
주문 서비스 → PostgreSQL (관계형, ACID)
카탈로그    → MongoDB (문서형, 유연 스키마)
추천        → Neo4j (그래프, 관계 탐색)
캐시        → Redis (인메모리, 고속)
로그        → InfluxDB (시계열)
```

- **📢 섹션 요약 비유**: Polyglot은 **요리마다 최적의 칼(도구)을 쓰는 것**이다. 모든 요리에 식빵 칼만 쓸 순 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| [[001_dikw_pyramid|데이터]] 유형 | 최적 DB |
|:---|:---|
| **관계형** | PostgreSQL, MySQL |
| **문서** | [[540_mongodb|MongoDB]] |
| **[[070_graph_datastructure|그래프]]** | Neo4j |
| **키-값** | [[542_redis|Redis]], [[545_dynamodb|DynamoDB]] |
| **시계열** | [[255_time_series_rollup_retention_compression|InfluxDB]], TimescaleDB |

---

## Ⅲ~Ⅴ. 결론

Polyglot Persistence는 **MSA의 [[001_dikw_pyramid|데이터]] 최적화 [[268_strategy_pattern|전략]]**이며, 관리형 [[090_service_kubernetes_network_load_balancing|서비스]]로 운영 부담을 줄이는 것이 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Polyglot** | [[090_service_kubernetes_network_load_balancing|서비스]]별 최적 DB |
| **DB per [[090_service_kubernetes_network_load_balancing|Service]]** | Polyglot의 전제 |
| **[[035_nosql|NoSQL]]** | 비관계형 DB |
| **관리형 [[090_service_kubernetes_network_load_balancing|서비스]]** | 운영 부담 감소 |
| **[[341_process|CAP]] 정리** | DB 선택 기준 |

### 📈 관련 키워드 및 발전 흐름도

```text
[단일 RDBMS (모노리스)] → [NoSQL 등장 (2010s)]
    → [Polyglot Persistence (MSA, 2014~)]
    → [관리형 서비스 (AWS RDS/DynamoDB)]
    → [현재: NewSQL + Polyglot — 최적 조합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Polyglot은 **요리마다 최적의 칼**을 쓰는 거예요. 빵에는 빵 칼, 고기에는 고기 칼!
2. 모든 요리에 **식빵 칼만 쓰면** 비효율적이에요.
3. 각 [[090_service_kubernetes_network_load_balancing|서비스]]에 **가장 잘 맞는 DB**를 골라주면 성능이 좋아진답니다!
