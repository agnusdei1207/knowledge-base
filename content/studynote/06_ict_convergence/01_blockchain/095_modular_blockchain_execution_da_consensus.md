+++
title = "95. 모듈러 블록체인 (Modular Blockchain) - 실행(Execution), 합의(Consensus), 정산(Settlement), 데이터 가용성(DA) 계층을 분리하여 확장성 극대화"

[taxonomies]
tags = ["ict_convergence"]

[extra]
tags = ["ict_convergence"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)러 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) (Modular [Blockchain](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/))은 연산, 합의, 정산, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장 등 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)의 모든 기능을 한 노드가 처리하던 모놀리식 (Monolithic) 구조를 깨고, 역할별로 계층(Layer)을 분리한 차세대 아키텍처다.
> 2. **가치**: 특정 계층(예: 실행이나 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장)만 전문적으로 처리하는 별도의 네트워크를 조립하여 사용함으로써, [탈중앙화](/knowledge-base/studynote/06_ict_convergence/01_blockchain/010_decentralization/)나 보안을 희생하지 않고도 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)(TPS)을 기하급수적으로 확장할 수 있다.
> 3. **판단 포인트**: 신규 앱체인 (AppChain)을 구축할 때 모든 인프라를 처음부터 개발할 필요 없이, 이더리움(보안/합의), 아비트럼(실행), 셀레스티아([데이터 가용성](/knowledge-base/studynote/06_ict_convergence/01_blockchain/094_data_availability_da_layer_celestia/)) 등 최적의 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)을 쇼핑하듯 플러그앤플레이(Plug & Play) 방식으로 결합하는 전략이 필수적이다.

## Ⅰ. 개요 및 필요성

초창기 비트코인 (Bitcoin)과 이더리움 (Ethereum)을 비롯한 대부분의 메인넷은 하나의 노드가 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 실행, 블록 합의, 장부 정산, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 보관까지 4가지 핵심 역할을 모두 수행하는 **[모놀리식 블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/096_monolithic_blockchain_solana/) ([Monolithic Blockchain](/knowledge-base/studynote/06_ict_convergence/01_blockchain/096_monolithic_blockchain_solana/))** 구조였다.

그러나 네트워크 참여자와 거래량이 급증하면서 한계가 명확해졌다. 모든 노드가 모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다운로드하고 똑같이 연산해야 하므로, 처리 속도가 느려지고(확장성 문제), 노드 운영 요구 사양이 높아져 소수에게 권력이 집중되는(중앙화 문제) [블록체인 트릴레마](/knowledge-base/studynote/06_ict_convergence/01_blockchain/040_blockchain_trilemma/) ([Blockchain Trilemma](/knowledge-base/studynote/06_ict_convergence/01_blockchain/482_blockchain_trilemma_scalability_decentralization_security/))에 직면한 것이다. 이를 해결하기 위해 "잘하는 놈에게 외주를 주자"는 철학 아래, 기능을 계층별로 쪼개어 레고 블록처럼 결합하는 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)러 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 패러다임이 등장했다.

- **📢 섹션 요약 비유**: 모놀리식 구조가 동네 중국집 사장님이 **혼자 전단지 돌리고, 요리하고, 철가방 들고 배달까지 뛰느라** 하루 50그릇밖에 못 파는 구조라면, [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)러 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)은 요리, 서빙, 계산, 배달을 완벽하게 분업화한 초대형 기업형 식당이다.

## Ⅱ. 아키텍처 및 핵심 원리

[모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)러 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)은 시스템을 크게 4개의 전문 계층(Layer)으로 분해한다.

| 계층 (Layer) | 주요 역할 | 담당 네트워크 예시 |
| :--- | :--- | :--- |
| **실행 (Execution)** | [스마트 컨트랙트](/knowledge-base/studynote/06_ict_convergence/01_blockchain/022_smart_contract/) 연산, 상태 업데이트 (덧셈/뺄셈 처리) | Arbitrum, Optimism (L2 [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)) |
| **[데이터 가용성](/knowledge-base/studynote/06_ict_convergence/01_blockchain/094_data_availability_da_layer_celestia/) ([DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/), [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/))** | [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 원본 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 저렴하게 영구 보관하고 누구나 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)할 수 있게 제공 | Celestia, EigenDA, Avail |
| **합의 (Consensus)** | [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)의 시간적 순서와 유효성 확정, 악의적 노드 차단 | Ethereum 메인넷 (L1) |
| **정산 (Settlement)** | 실행 계층의 결과 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), 분쟁 시 최종 판결, 자산 출금 승인 | Ethereum 메인넷 (L1) |

이 4가지 계층 중 일부만 특화하여 서비스하는 네트워크들이 등장하면서, 이들을 어떻게 조합하느냐에 따라 다양한 아키텍처가 파생된다.

```text
┌──────────────────────────────────────────────────────────────┐
│             모듈러 블록체인 아키텍처 및 계층 분리            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  [ 실행 계층 (L2 Rollup) ] ──▶ 연산만 10,000 TPS로 초고속 처리│
│       │ (트랜잭션 결과 및 증명 전달)                         │
│       ▼                                                      │
│  [ 정산 계층 (L1) ] ─────────▶ 롤업 사기 증명 검증, 최종 확정 │
│       │ (원시 데이터 백업)                                   │
│       ▼                                                      │
│  [ 데이터 가용성 계층 (DA) ] ──▶ 저비용 대용량 블록 데이터 저장 │
│       │                                                      │
│  [ 합의 계층 (L1) ] ─────────▶ 글로벌 노드 간 순서와 룰 합의 │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```
이 그림은 연산의 부담(실행)과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 용량의 부담([DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/))을 메인넷(합의/정산) 밖으로 빼내어 전체 병목을 해소하는 구조를 보여준다.

- **📢 섹션 요약 비유**: 실행 계층은 칠판에 미친 듯이 수식을 푸는 **'천재 수학자'**이고, [데이터 가용성](/knowledge-base/studynote/06_ict_convergence/01_blockchain/094_data_availability_da_layer_celestia/)([DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/)) 계층은 그 수학자가 쓴 모든 연습장 쪼가리를 버리지 않고 보관해 주는 **'거대 문서 창고'**다. 정산과 합의는 이 연습장을 검사하는 **'대법관'**이다.

## Ⅲ. 비교 및 연결

모놀리식 방식과 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)러 방식을 비교하면 기술의 진화 방향이 명확히 드러난다.

| 비교 항목 | [모놀리식 블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/096_monolithic_blockchain_solana/) (Monolithic) | [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)러 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) (Modular) |
| :--- | :--- | :--- |
| **아키텍처 구조** | 단일 노드가 4대 기능 모두 수행 | 역할별 특화 네트워크 결합 |
| **확장성 (Scalability)** | 노드 사양의 한계로 TPS 확장에 병목 | L2 [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) 및 전문 [DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 사용으로 무한 확장 가능 |
| **유연성 (Flexibility)** | 설계 변경 불가 (경직됨) | RaaS를 통해 원하는 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) 자유롭게 교체 |
| **대표 사례** | 솔라나 (Solana), 초창기 이더리움 | 이더리움 [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) 체계, 셀레스티아 (Celestia) |

모놀리식인 솔라나는 하드웨어 성능을 극대화하여 "무식하게 빠른 단일 컴퓨터"를 만드는 방향을 택했지만, 노드 운영 비용이 비싸 중앙화 우려가 있다. 반면 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)러를 택한 이더리움 생태계는 [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) ([Rollup](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/))과 [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) (Danksharding)을 결합하여 보안을 유지하면서도 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 늘리는 구조적 우위를 가져간다.

- **📢 섹션 요약 비유**: 모놀리식은 카메라, CPU, 배터리를 일체형으로 만들어 성능을 쥐어짜는 **'아이폰'** 방식이고, [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)러는 내가 원하는 부품을 마음대로 끼워 맞추는 **'조립식 데스크톱 [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)'** 방식이다.

## Ⅳ. 실무 적용 및 기술사 판단

웹3.0 기업이나 게임사가 자체 메인넷(AppChain)을 구축할 때, 처음부터 L1 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)을 만드는 것은 비용과 보안 측면에서 자살 행위다. 

### 실무 도입 판단 기준
1. **[RaaS](/knowledge-base/studynote/09_security/15_malware_attack_vectors/736_raas/) ([Rollup](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)-as-a-Service) 활용**: [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)러 아키텍처를 지원하는 플랫폼(예: [Caldera](/knowledge-base/studynote/09_security/14_threat_hunting_adversarial/715_caldera/), AltLayer)을 사용하여, 클릭 몇 번으로 실행 엔진(OP [Stack](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/))과 [DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 계층(Celestia)을 결합해 수일 내에 체인을 론칭해야 한다.
2. **보안 vs 비용 트레이드오프**: 금융([DeFi](/knowledge-base/studynote/06_ict_convergence/01_blockchain/033_defi_decentralized_finance/)) 앱은 보안이 최우선이므로 이더리움(L1)을 [DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 계층으로 쓰는 [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)([Rollup](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/))을 택하고, 게임(GameFi) 앱은 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 비용이 중요하므로 셀레스티아 같은 외부 DA를 쓰는 발리디움 (Validium) 구조를 택하는 판단이 필요하다.

### 기술사 관점
결국 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)러 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)은 소프트웨어 공학의 '[마이크로서비스 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/) ([MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/))'와 정확히 일치하는 진화 과정이다. 거대한 시스템을 역할별 독립 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)로 쪼개어 결합도를 낮추고 응집도를 높이는 설계 사상을 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 인프라에 적용한 것이다.

- **📢 섹션 요약 비유**: 앱체인을 만드는 것은 자동차 공장을 짓는 것과 같다. 예전엔 바퀴부터 엔진까지 다 자체 제작(모놀리식)했다면, 이제는 미쉐린 타이어([DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/))와 벤츠 엔진(실행)을 사 와서 뼈대(합의)에 조립만 하면 된다.

## Ⅴ. 기대효과 및 결론

[모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)러 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)은 [블록체인 트릴레마](/knowledge-base/studynote/06_ict_convergence/01_blockchain/040_blockchain_trilemma/)(확장성, [보안성](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/), [탈중앙화](/knowledge-base/studynote/06_ict_convergence/01_blockchain/010_decentralization/))를 극복하는 가장 현실적이고 강력한 돌파구다. 개발자는 인프라 걱정 없이 앱([DApp](/knowledge-base/studynote/06_ict_convergence/01_blockchain/032_dapp_decentralized_application/)) 자체의 논리에만 집중할 수 있고, 사용자들은 저렴한 수수료로 빠른 속도를 누리게 된다.

다만, 여러 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)이 얽히면서 서로 다른 [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) 간의 파편화 ([Fragmentation](/knowledge-base/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/))와 자산 이동([Bridge](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/))의 복잡성이 커지는 한계가 존재한다. 그럼에도 불구하고, 미래의 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)은 하나의 완벽한 메인넷이 독식하는 구조가 아니라, 특화된 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)들이 서로 얽혀 상호 운용되는 거대한 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)러 생태계로 진화할 것이다.

- **📢 섹션 요약 비유**: [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)러 시스템은 글로벌 경제의 **'자유 무역 비교 우위'**와 같다. 반도체를 잘 만드는 나라, 농사를 잘 짓는 나라가 서로 특화된 산업에 집중하고 무역(결합)을 통해 전 세계의 부를 극대화하는 것과 같다.

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
| :--- | :--- |
| **[데이터 가용성](/knowledge-base/studynote/06_ict_convergence/01_blockchain/094_data_availability_da_layer_celestia/) ([DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/), [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/))** | 노드가 전체 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다운받지 않고도 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 손실 없이 저장되었음을 증명하는 핵심 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) |
| **[롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/) ([Rollup](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)) (Optimistic / ZK)** | L2에서 실행을 처리하고 그 결과와 증명만 합의/정산 계층(L1)으로 보내는 기술 |
| **[블록체인 트릴레마](/knowledge-base/studynote/06_ict_convergence/01_blockchain/040_blockchain_trilemma/) ([Blockchain Trilemma](/knowledge-base/studynote/06_ict_convergence/01_blockchain/482_blockchain_trilemma_scalability_decentralization_security/))** | 확장성, [보안성](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/), [탈중앙화](/knowledge-base/studynote/06_ict_convergence/01_blockchain/010_decentralization/)의 3가지 요소를 동시에 달성하기 어려운 딜레마 ([모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)러로 극복) |
| **발리디움 (Validium)** | ZK [롤업](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/)과 유사하나, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장을 오프체인(외부 [DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/))에 맡겨 비용을 대폭 낮춘 구조 |

### 📈 관련 키워드 및 발전 흐름도
```text
비트코인 / 초기 이더리움 (Monolithic)
    │
    ▼
확장성 한계 직면 및 블록체인 트릴레마 발생
    │
    ▼
실행 계층 분리 (L2 롤업: Arbitrum, Optimism)
    │
    ▼
데이터 가용성(DA) 계층 독립 (Celestia, EigenDA)
    │
    ▼
완전한 모듈러 블록체인 생태계 및 RaaS (Rollup-as-a-Service) 대중화
```
이 흐름도는 모든 것을 혼자 처리하던 시스템이 속도 한계에 부딪힌 후, 실행을 떼어내고, 그다음 저장소([DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/))까지 분리해내어 최종적으로 조립식 인프라로 진화하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 예전에는 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 컴퓨터 혼자서 숙제 풀고, 검사하고, 일기장 정리까지 다 하느라 너무 느렸어요. (모놀리식)
2. 그래서 똑똑한 사람들이 "숙제 빨리 푸는 애", "검사 꼼꼼히 하는 애", "일기장 잘 보관하는 애"로 역할을 나눠주었어요. ([모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)러)
3. 각자 자기가 제일 잘하는 일만 집중해서 탁탁 맞춰보니까, 혼자 할 때보다 100배는 더 빨리 일을 끝낼 수 있게 되었답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 95 / 552

← **이전**: [94. 데이터 가용성 (Data Availability, DA) 계층](/knowledge-base/studynote/06_ict_convergence/01_blockchain/094_data_availability_da_layer_celestia/)
**다음**: [96. 모놀리식 블록체인 (Monolithic Blockchain) - 모든 작업을 단일 체인(솔라나, 앱토스 등)에서 처리](/knowledge-base/studynote/06_ict_convergence/01_blockchain/096_monolithic_blockchain_solana/) →

---
