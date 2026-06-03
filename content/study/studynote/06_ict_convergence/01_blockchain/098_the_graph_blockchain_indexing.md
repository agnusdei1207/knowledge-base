+++
weight = 98
title = "98. 블록체인 데이터 인덱싱 (The Graph Blockchain Indexing Protocol)"
date = "2026-04-21"
[extra]
categories = "studynote-ict-convergence"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: The Graph는 이더리움 등 [[004_blockchain|블록체인]]의 방대한 [[001_dikw_pyramid|데이터]]를 서브그래프 (Subgraph) 형태로 색인(인덱싱)하여 [[246_graphql_query_language_overfetching_solution|GraphQL]] API로 빠르게 조회할 수 있게 해주는 [[010_decentralization|탈중앙화]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]이다.
> 2. **가치**: 특정 [[022_smart_contract|스마트 컨트랙트]]의 이벤트 로그를 찾기 위해 제네시스 블록부터 전체를 훑는 O(N)의 비효율을 제거하고, [[001_dikw_pyramid|데이터]]를 밀리초 단위로 응답하여 Web3 [[090_service_kubernetes_network_load_balancing|서비스]]([[033_defi_decentralized_finance|DeFi]], NFT)의 UX를 극적으로 향상시킨다.
> 3. **판단 포인트**: [[454_spof|단일 장애점]] ([[454_spof|SPOF]], Single Point of Failure)이 있는 중앙화된 [[126_rpc|RPC]] 노드 제공자에 의존하지 않고, 인덱서 (Indexer), 큐레이터 (Curator), 위임자 (Delegator) 간의 GRT 토큰 경제를 통해 검열 저항성과 [[001_dikw_pyramid|데이터]] 품질을 유지하는 아키텍처를 채택해야 할 때 필수적이다.

---

## Ⅰ. 개요 및 필요성

[[004_blockchain|블록체인]]은 [[001_dikw_pyramid|데이터]]를 안전하게 저장하는 데는 탁월하지만, 그 [[001_dikw_pyramid|데이터]]를 효율적으로 검색하고 [[298_qkv_attention|쿼리]]하는 데는 최악의 구조를 가졌다. 이더리움에서 특정 유저가 발행한 NFT 목록이나 스왑 내역을 조회하려면, 이론적으로 과거의 모든 블록 [[001_dikw_pyramid|데이터]]를 순차적으로 스캔하고 [[022_smart_contract|스마트 컨트랙트]] 이벤트 로그를 직접 파싱해야 한다. 

초기에는 개발자들이 개별적으로 서버를 띄워 [[004_blockchain|블록체인]] 노드를 [[212_synchronization_mechanisms|동기화]]하고 자체 DB에 [[001_dikw_pyramid|데이터]]를 밀어 넣는 방식을 썼지만, 이는 개발 비용이 막대하고 [[454_spof|단일 장애점]] ([[454_spof|SPOF]])을 만들어 [[010_decentralization|탈중앙화]] 철학을 훼손했다. The Graph는 이 문제를 해결하기 위해 등장한 **[[010_decentralization|탈중앙화]] [[001_dikw_pyramid|데이터]] 인덱싱 레이어**다. 개발자가 "어떤 [[001_dikw_pyramid|데이터]]를 어떻게 정리할 것인가"를 정의해 올리면, 전 세계의 노드들이 이를 대신 색인화해주고 안정적인 API를 제공한다.

- **📢 섹션 요약 비유**: [[004_blockchain|블록체인]]이 전 세계의 모든 영수증을 시간순으로 구겨 넣은 거대한 박스라면, The Graph는 이 박스를 뒤져서 "A마트 영수증", "B식당 영수증"으로 깔끔하게 장부를 만들어주는 엑셀 자동화 프로그램과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

The [[104_graph|Graph]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]은 [[001_dikw_pyramid|데이터]]를 색인하는 주체와 이를 [[395_verification_process_review|검증]]·지원하는 주체들이 GRT ([[104_graph|Graph]] Token) 생태계 안에서 상호작용하는 구조다. 핵심 개발 단위는 **서브그래프 (Subgraph)**로, 특정 컨트랙트의 이벤트를 어떻게 가공할지 정의한 명세서다.

```text
┌──────────────────────────────────────────────────────────────┐
│           The Graph 분산형 인덱싱 및 쿼리 아키텍처           │
├──────────────────────────────────────────────────────────────┤
│  [블록체인 네트워크] (Ethereum, Polygon 등)                  │
│          │                                                   │
│          │ 이벤트 로그 / 블록 데이터 발생                    │
│          ▼                                                   │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ The Graph Network (탈중앙화 노드 그룹)                 │  │
│  │                                                        │  │
│  │   [ 인덱서 (Indexer) ] ◀── GRT 위임 ── [ 위임자 ]     │  │
│  │   - 블록 파싱, Subgraph DB 업데이트                    │  │
│  │   - 쿼리 응답 및 증명 생성                             │  │
│  │                                                        │  │
│  │   [ 큐레이터 (Curator) ]                               │  │
│  │   - 유망한 Subgraph에 GRT 토큰 예치 (Signal)           │  │
│  └────────────────────────────────────────────────────────┘  │
│          │                                                   │
│          │ GraphQL Query (요청/응답)                         │
│          ▼                                                   │
│  [Web3 DApp 클라이언트] (DeFi 대시보드, NFT 마켓플레이스)    │
└──────────────────────────────────────────────────────────────┘
```

서브그래프는 매니페스트 (YAML), [[005_schema|스키마]] ([[246_graphql_query_language_overfetching_solution|GraphQL]]), 매핑 스크립트 (AssemblyScript)로 구성된다. 인덱서는 서브그래프 명세에 따라 이더리움 블록을 수집해 PostgreSQL 같은 DB에 저장한다. 클라이언트는 복잡한 블록 탐색 없이 [[156_rest_representational_state_transfer|REST]] API보다 유연한 [[246_graphql_query_language_overfetching_solution|GraphQL]] [[298_qkv_attention|쿼리]]로 원하는 [[001_dikw_pyramid|데이터]](예: 상위 10명의 홀더)를 단번에 가져온다.

- **📢 섹션 요약 비유**: 인덱서는 도서관 사서, 큐레이터는 베스트셀러에 추천 딱지를 붙이는 평론가, 위임자는 사서에게 돈을 투자하는 주주다. 이들이 모여 엉망진창인 책([[004_blockchain|블록체인]])의 완벽한 색인(Subgraph)을 유지한다.

---

## Ⅲ. 비교 및 연결

Web3 환경에서 [[001_dikw_pyramid|데이터]]를 읽어오는 방식은 직접 [[126_rpc|RPC]] 호출, 중앙화 공급자, 그리고 The Graph와 같은 [[010_decentralization|탈중앙화]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]로 나뉜다.

| 비교 항목 | 직접 [[126_rpc|RPC]] 파싱 ([[083_full_node_complete_ledger|Full Node]]) | 중앙화 [[014_api_posix|API]] (Alchemy, Infura 등) | The [[104_graph|Graph]] ([[010_decentralization|탈중앙화]] 인덱싱) |
| :--- | :--- | :--- | :--- |
| **속도 및 [[282_performance_tactics|성능]]** | 수 분 ~ 수 시간 소요 | 비교적 빠르나 [[298_qkv_attention|쿼리]] 한계 존재 | **밀리초 (ms) 단위** |
| **[[010_decentralization|탈중앙화]] 수준** | 매우 높음 (직접 [[395_verification_process_review|검증]]) | 낮음 (서버 다운 시 [[090_service_kubernetes_network_load_balancing|서비스]] 마비) | **높음** (다수의 독립 인덱서) |
| **[[298_qkv_attention|쿼리]] 유연성** | 매우 낮음 ([[225_raw|Raw]] [[001_dikw_pyramid|Data]]) | 중간 ([[477_rest_api_architecture|REST API]] 의존) | **매우 높음** ([[246_graphql_query_language_overfetching_solution|GraphQL]] 기반) |
| **운영 비용** | 인프라 유지비 높음 | 월 구독료 | [[298_qkv_attention|쿼리]] 건당 초소액 수수료 (GRT) |

The Graph는 단순히 속도만 빠른 것이 아니라, [[055_ipfs_interplanetary_file_system|IPFS]] ([[055_ipfs_interplanetary_file_system|InterPlanetary File System]])와 연동하여 서브그래프 정의 [[501_file_definition_logical_record|파일]] 자체도 [[010_decentralization|탈중앙화]]된 방식으로 저장함으로써 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 수준의 무결성을 유지한다.

- **📢 섹션 요약 비유**: 직접 파싱이 도서관의 모든 책을 직접 넘기며 단어를 찾는 것이고, 중앙화 API가 알바생에게 돈을 주고 찾아달라고 하는 것이라면, The Graph는 구글 검색엔진을 켜고 원하는 단어만 정확히 검색하는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

Web3 아키텍처 설계 시 백엔드 [[001_dikw_pyramid|데이터]] 계층에 대한 결정은 전체 시스템의 가용성과 직결된다.

### 판단 포인트
- **[[033_defi_decentralized_finance|DeFi]]/NFT 대시보드 구축**: Uniswap의 TVL (Total Value Locked) 변화나 OpenSea의 거래 히스토리를 사용자에게 실시간으로 보여주려면 The [[104_graph|Graph]] 도입이 사실상 필수적이다.
- **실시간성(Real-time) vs 완전성**: 서브그래프는 블록이 생성된 후 인덱서가 이를 파싱하는 약간의 [[015_지연_데이터_관점|지연]](Sync Delay)이 발생한다. 따라서 초단타 아비트리지 봇처럼 1블록(12초) 내의 극단적인 실시간성이 필요한 [[191_transaction_concept_states|트랜잭션]] [[395_verification_process_review|검증]]에는 적합하지 않고, 집계 및 히스토리 조회용으로 써야 한다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- [[004_blockchain|블록체인]]에 저장된 모든 [[225_raw|Raw]] Data를 백엔드 서버에서 `eth_getLogs`로 계속 긁어와 직접 RDBMS에 저장하는 휠(Wheel) 재발명 로직. 인프라 비용과 [[212_synchronization_mechanisms|동기화]] 오류 리스크만 폭증한다.

- **📢 섹션 요약 비유**: 실시간 뉴스 속보를 보기 위해 윤전기에서 방금 나온 신문을 가로채는 것(직접 파싱)은 극소수에게만 필요하다. 대부분의 독자는 잘 편집된 포털 사이트 메인 화면(The [[104_graph|Graph]])을 보는 것이 훨씬 효율적이다.

---

## Ⅴ. 기대효과 및 결론

The Graph를 적용하면 [[032_dapp_decentralized_application|DApp]] 개발팀은 복잡한 백엔드 인프라와 [[001_dikw_pyramid|데이터]] 파싱 로직을 유지보수할 필요가 없어져 개발 생산성이 극대화된다. 또한 중앙화된 노드 [[090_service_kubernetes_network_load_balancing|서비스]]의 다운타임이나 [[014_api_posix|API]] 검열 리스크에서 벗어나 진정한 Web3 철학에 부합하는 [[010_decentralization|탈중앙화]] 프론트엔드를 구축할 수 있다.

다만, 멀티 체인 환경이 복잡해지면서 서브그래프를 여러 체인에 맞게 관리해야 하는 복잡도가 존재한다. 결론적으로 The Graph는 [[022_smart_contract|스마트 컨트랙트]](백엔드)와 사용자 인터페이스(프론트엔드)를 연결하는 가장 표준적이고 강력한 [[010_decentralization|탈중앙화]] 미들웨어 (Middleware)로 자리매김하고 있다.

- **📢 섹션 요약 비유**: 복잡한 도로망([[004_blockchain|블록체인]]) 위를 달리는 수많은 자동차([[001_dikw_pyramid|데이터]])의 궤적을 CCTV로 하나하나 분석하는 대신, 모든 경로를 완벽하게 집계해 주는 네비게이션 교통 통제소(The [[104_graph|Graph]])를 무료로 이용하는 것과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **[[246_graphql_query_language_overfetching_solution|GraphQL]]** | The Graph에서 클라이언트가 [[001_dikw_pyramid|데이터]]를 요청할 때 사용하는 선언적 [[298_qkv_attention|쿼리]] 언어 |
| **GRT ([[104_graph|Graph]] Token)** | 인덱서, 큐레이터, 위임자에게 경제적 유인을 제공하는 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 유틸리티 토큰 |
| **[[055_ipfs_interplanetary_file_system|IPFS]] ([[055_ipfs_interplanetary_file_system|InterPlanetary File System]])** | 서브그래프의 정의 [[501_file_definition_logical_record|파일]](매니페스트 등)이 변조되지 않도록 저장하는 [[553_distributed_file_system|분산 파일 시스템]] |
| **[[454_spof|SPOF]] (Single Point of Failure)** | The Graph가 [[136_variance|분산]]형 인덱서를 통해 제거하고자 하는 중앙화 [[090_service_kubernetes_network_load_balancing|서비스]]의 약점 |

### 📈 관련 키워드 및 발전 흐름도

```text
Full Node 자체 운영 (비용 극대화, 데이터 파싱 어려움)
    │
    ▼
중앙화 RPC 노드 제공자 (Infura, Alchemy 등 - SPOF 발생)
    │
    ▼
서브그래프 (Subgraph) 기반 특정 이벤트 정의
    │
    ▼
The Graph 프로토콜 (탈중앙화 인덱서 네트워크 형성)
    │
    ▼
멀티체인 및 L2 네트워크 인덱싱 지원 확장
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[004_blockchain|블록체인]]은 아주 두껍고 내용이 섞여 있는 백과사전이라서, 내가 좋아하는 공룡 이야기만 찾기가 너무 힘들어요.
2. The Graph는 이 백과사전에 미리 '공룡', '우주', '로봇' 같은 꼬리표를 예쁘게 달아둔 똑똑한 요정이에요.
3. 요정에게 "티라노사우루스 얘기만 모아줘!"라고 말하면 1초 만에 깔끔하게 정리된 노트를 건네준답니다.
