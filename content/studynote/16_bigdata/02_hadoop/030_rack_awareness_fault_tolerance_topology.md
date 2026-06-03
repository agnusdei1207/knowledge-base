---
title: 08. 랙 인지 (Rack Awareness) - 물리적 장애 격리를 위한 데이터 복제 전략
date: '2026-03-04'
tags:
- hadoop
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)
- **물리적 장애 그룹 인지**: 수많은 서버가 꽂혀 있는 '랙(Rack)' 단위의 장애([[238_switch_operation_principles|스위치]] 고전압, 전원 차단 등)에 대비하여 [[001_dikw_pyramid|데이터]]를 물리적으로 [[136_variance|분산]] 배치하는 지능형 [[001_algorithm_definition|알고리즘]]입니다.
- **기본 [[016_replication_factor|복제]] 규칙 (3-Replica)**: 하나의 블록은 로컬 랙에 1개, 멀티 랙(다른 랙)에 2개를 [[136_variance|분산]] 저장하여 [[452_availability|가용성]]과 네트워크 [[282_performance_tactics|성능]]의 균형을 맞춥니다.
- **[[282_performance_tactics|성능]]과 안정성의 타협**: 모든 [[016_replication_factor|복제]]본을 다른 랙에 두면 안전하지만 네트워크 비용이 비싸지므로, [[017_rack_awareness|랙 인지]]는 '적절한 거리'를 계산하여 최적의 경로를 도출합니다.

### Ⅰ. 개요 ([[033_context|Context]] & Background)
대규모 [[843_hadoop_rack_awareness_data_replication_topology|하둡]] 클러스터는 수십 개의 랙으로 구성되며, 각 랙은 상단 [[238_switch_operation_principles|스위치]](Top-of-Rack [[238_switch_operation_principles|Switch]])를 통해 연결됩니다. 만약 랙 [[238_switch_operation_principles|스위치]]가 고장 나면 해당 랙의 모든 서버에 접근할 수 없게 됩니다. [[014_namenode|네임노드]]가 [[015_datanode|데이터노드]]들의 물리적 위치(Topology)를 모른 채 랜덤하게 [[016_replication_factor|복제]]본을 저장한다면, 운 나쁘게 모든 [[016_replication_factor|복제]]본이 같은 랙에 들어가 랙 전체 장애 시 [[001_dikw_pyramid|데이터]]가 유실될 수 있습니다. 이를 방지하는 기술이 [[017_rack_awareness|랙 인지]]([[017_rack_awareness|Rack Awareness]])입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
[[014_namenode|네임노드]]는 랙 토폴로지 스크립트를 통해 각 노드의 `/rack_id`를 파악하고 [[016_replication_factor|복제]]본 위치를 결정합니다.

```text
[ HDFS Default Rack Awareness Strategy ]

Block Replication (Factor = 3):
1. Replica 1: Same Node as Client (or Local Node).
2. Replica 2: Different Rack from Replica 1 (Remote Rack).
3. Replica 3: Same Rack as Replica 2 (But different Node).

[ Diagram: Network Topology ]
      [ Switch Layer 1 ]
      /              \
 [ Rack 1 ]      [ Rack 2 ]
  /      \        /      \
[DN1]  [DN2]    [DN3]  [DN4]
 (R1)            (R2)   (R3)

* Distance Calculation:
- Same Node: 0
- Same Rack (different nodes): 2
- Different Rack: 4
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
랜덤 배치와 [[017_rack_awareness|랙 인지]] 배치를 비교합니다.

| 비교 항목 | 랜덤 배치 (Random) | [[017_rack_awareness|랙 인지]] (Rack Aware) |
| :--- | :--- | :--- |
| **[[001_dikw_pyramid|데이터]] 안전성** | 낮음 (랙 장애 시 유실 위험) | **높음 (랙 장애에도 [[001_dikw_pyramid|데이터]] 유지)** |
| **네트워크 부하** | 낮음~높음 (예측 불가) | **최적화 (랙 내부 통신 활용)** |
| **[[658_ir_recovery|복구]] 속도** | 빠를 수도 느릴 수도 있음 | **예측 가능하고 안정적임** |
| **[[009_config|설정]] 복잡도** | 없음 (기본값) | **토폴로지 맵 구성 필요** |

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)
1. **토폴로지 스크립트 작성**: 클라우드가 아닌 [[061_on_premise_legacy_infrastructure|온프레미스]] 환경에서는 IP 대역이나 [[238_switch_operation_principles|스위치]] [[446_port_and_bus|포트]]를 기반으로 `/dc1/rack1` 형태의 계층 구조를 정의하는 스크립트를 반드시 적용해야 합니다.
2. **읽기 [[282_performance_tactics|성능]] 최적화**: HDFS는 클라이언트와 가장 가까운(Distance가 낮은) 노드에서 [[001_dikw_pyramid|데이터]]를 먼저 읽도록 하여 클러스터 전체 네트워크 트래픽을 절감합니다.
3. **기술사적 판단**: [[017_rack_awareness|랙 인지]]는 '계란을 한 바구니에 담지 마라'는 격언의 공학적 실천입니다. [[452_availability|가용성]]뿐만 아니라 랙 간(Inter-rack) [[140_bandwidth|대역폭]] 부족 문제를 해결하는 [[282_performance_tactics|성능]] 튜닝의 핵심 지표로 관리해야 합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
[[017_rack_awareness|랙 인지]]는 [[843_hadoop_rack_awareness_data_replication_topology|하둡]]의 고가용성(High [[452_availability|Availability]])을 완성하는 숨은 공신입니다. 최신 클라우드 환경에서는 '가용 영역([[452_availability|Availability]] Zone)' 인지 기술로 확장되어, 도시 전체의 재난에서도 [[001_dikw_pyramid|데이터]]를 지켜내는 기술적 근간이 되고 있습니다. 인프라의 물리적 한계를 소프트웨어 [[001_algorithm_definition|알고리즘]]으로 극복하는 대표적인 사례입니다.

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **상위 개념**: [[013_hdfs|HDFS]] 내결함성([[800_system_architecture_fault_tolerance_dual|Fault Tolerance]]), [[016_replication_factor|복제]]([[016_replication_factor|Replication]])
- **핵심 [[001_algorithm_definition|알고리즘]]**: [[016_replication_factor|복제]]본 배치 [[164_policy|정책]](Replica Placement [[164_policy|Policy]])
- **확장 개념**: 가용 영역(AZ), 리전(Region), [[001_dikw_pyramid|데이터]] 센터 토폴로지

### 📈 관련 키워드 및 발전 흐름도

```text
[HDFS 복제 (Replication) — 기본 복제 계수 3]
    │
    ▼
[랙 인지 (Rack Awareness) — 랙 단위 장애 격리]
    │
    ▼
[복제본 배치 정책 (Replica Placement Policy)]
    │
    ▼
[가용 영역 (AZ, Availability Zone) — 클라우드 확장]
    │
    ▼
[리전 복제 (Cross-Region Replication) — 지역 재해 대비]
```

[[553_distributed_file_system|분산 파일 시스템]]의 내결함성 [[268_strategy_pattern|전략]]이 [[017_rack_awareness|랙 인지]]에서 클라우드 가용 영역과 리전 수준 [[016_replication_factor|복제]]로 발전한 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명
1. 중요한 보물 지도 3장을 똑같은 상자 안에 다 넣어두면, 상자를 잃어버렸을 때 지도가 다 없어져요.
2. [[017_rack_awareness|랙 인지]]는 지도 한 장은 우리 집(랙 1)에 두고, 나머지 두 장은 옆집(랙 2)에 나눠서 보관하는 규칙이에요.
3. 이렇게 하면 우리 집에 불이 나도 옆집에 지도가 남아 있어서 보물을 찾을 수 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 30 / 262

← **이전**: [[029_datanode_block_storage_heartbeat|07. 데이터노드 (DataNode) - HDFS 분산 저장의 워커 노드 및 블록 관리]]
**다음**: [[031_mapreduce_programming_model_parallel_processing|09. 맵리듀스 (MapReduce) - 대규모 데이터 병렬 처리를 위한 분산 프로그래밍 모델]] →

---
