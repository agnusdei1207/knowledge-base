+++
title = "87. 다중 접속 (Multiple Access) 개념 (MAC 계층 연관)"
description = "중앙 통제가 없는 공유 매체 환경에서 충돌을 극복하고 자원을 분배하는 MAC 계층의 매체 접근 제어 원리"
date = 2026-03-30

[taxonomies]
tags = ["network"]

[extra]
tags = ["network"]
+++

## 핵심 인사이트 (3줄 요약)

    > 1. **본질**: 다중 접속 (Multiple Access)은 [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) (Medium [Access Control](/knowledge-base/studynote/02_operating_system/09_file_system/547_access_control_rwx/)) 계층에서 여러 사용자가 하나의 공유 [매체](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)를 어떻게 나눠 쓰는지 정하는 기술이다.
    > 2. **가치**: [FDMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/088_주파수_분할_다중접속_FDMA/), [TDMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/089_시분할_다중접속_TDMA/), [CDMA](/knowledge-base/studynote/03_network/19_frequent_topics_terms/957_cdma_code_division_multiple_access_dsss_orthogonality/), [OFDMA](/knowledge-base/studynote/03_network/19_frequent_topics_terms/945_ofdma_orthogonal_frequency_division_multiple_access_resource_block/), [CSMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/104_csma/) 계열은 자원을 나누는 기준이 달라서 충돌, [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 효율의 균형이 서로 다르다.
    > 3. **판단 포인트**: 무선·유선·실시간 환경마다 적합한 방식이 다르므로, 공유 [매체](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)의 물리적 제약을 먼저 봐야 한다.

    ---

    ## Ⅰ. 개요 및 필요성

    다중 접속 (Multiple Access)은 한정된 채널을 여러 단말이 함께 사용할 때 충돌과 혼잡을 줄이는 방법이다. [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) (Medium [Access Control](/knowledge-base/studynote/02_operating_system/09_file_system/547_access_control_rwx/)) 계층은 누가, 언제, 어떤 자원을 사용할지 정한다.

이 기술이 중요한 이유는 대역폭이 항상 부족하기 때문이다. 유선이든 무선이든 같은 [매체](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)를 동시에 쓰려 하면 충돌이 생기므로, 시간을 나누거나 주파수를 나누거나 코드를 나누는 방식이 필요하다.

    - **📢 섹션 요약 비유**: 하나의 운동장을 여러 반이 함께 쓰되, 줄과 시간표를 정하는 느낌이다.

    ---

    ## Ⅱ. 아키텍처 및 핵심 원리

    다중 접속 방식은 크게 채널 분할형, 경쟁형, 통제형으로 나눌 수 있다.

| [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 대표 방식 | 충돌 처리 | 특징 |
| :-- | :-- | :-- | :-- |
| 채널 분할형 | [FDMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/088_주파수_분할_다중접속_FDMA/), [TDMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/089_시분할_다중접속_TDMA/), [CDMA](/knowledge-base/studynote/03_network/19_frequent_topics_terms/957_cdma_code_division_multiple_access_dsss_orthogonality/), [OFDMA](/knowledge-base/studynote/03_network/19_frequent_topics_terms/945_ofdma_orthogonal_frequency_division_multiple_access_resource_block/) | 사전 [자원 할당](/knowledge-base/studynote/02_operating_system/01_overview_architecture/041_resource_allocation/) | 예측 가능, 스케줄링 친화적 |
| 경쟁형 | [ALOHA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/111_aloha_protocol/), [CSMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/104_csma/)/CD, [CSMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/104_csma/)/[CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) | 충돌과 백오프 | 단순하지만 혼잡에 약함 |
| 통제형 | [polling](/knowledge-base/studynote/02_operating_system/11_exam_summary/747_io_polling_overhead/), [token passing](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/115_token_passing/) | 순번 통제 | [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 예측이 쉽다 |

```text
시간 분할: | A | B | C | D |
주파수 분할: | A | B | C | D |
코드 분할:   codeA codeB codeC codeD
```

핵심은 자원을 단순히 나누는 것이 아니라, 충돌이 생기기 쉬운 조건을 미리 설계로 흡수하는 데 있다.

    - **📢 섹션 요약 비유**: 같은 간식을 나눌 때, 먼저 줄을 설지 시간표를 만들지 방법이 다르다.

    ---

    ## Ⅲ. 비교 및 연결

    경쟁형과 스케줄형을 비교하면 선택 기준이 분명해진다.

| 항목 | 경쟁형 | 스케줄형 |
| :-- | :-- | :-- |
| 충돌 | 발생 가능 | 거의 없음 |
| [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 예측 | 어려움 | 쉬움 |
| 구현 | 단순 | 복잡 |
| 적합 환경 | 트래픽이 가변적인 공유 [매체](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) | QoS가 중요한 관리형 네트워크 |

예를 들어 Wi-Fi는 충돌 감지가 어렵기 때문에 [CSMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/104_csma/)/[CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) (Carrier Sense Multiple Access with [Collision](/knowledge-base/studynote/05_database/04_transactions_concurrency/563_hash_collision_chaining_linear_probing/) Avoidance)를 쓴다. 반면 [LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/)/5G는 중앙 스케줄러가 자원을 배분하는 [OFDMA](/knowledge-base/studynote/03_network/19_frequent_topics_terms/945_ofdma_orthogonal_frequency_division_multiple_access_resource_block/) (Orthogonal Frequency [Division](/knowledge-base/studynote/05_database/07_exam_summary/411_division_operation/) Multiple Access) 계열을 활용해 더 정교한 QoS를 제공한다. 유선 Ethernet의 과거 [CSMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/104_csma/)/CD (Carrier Sense Multiple Access with [Collision Detection](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/106_CSMA_CD_유선이더넷_충돌감지/))는 충돌 검출이 가능했지만, 반이중 환경에서만 의미가 있었다.

    - **📢 섹션 요약 비유**: Wi-Fi는 피해서 들어가고, 5G는 먼저 자리를 배정받는 방식에 가깝다.

    ---

    ## Ⅳ. 실무 적용 및 기술사 판단

    실무에서는 트래픽 성격과 물리 [매체](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)가 먼저다. 실시간 제어처럼 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 상한이 중요하면 TDMA나 token 방식이 맞고, 사용량이 급변하는 무선 환경이면 경쟁형과 스케줄형을 혼합한 설계가 필요하다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. [매체](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)가 충돌 검출을 지원하는가, 아니면 회피만 가능한가?
2. [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 상한과 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 중 무엇이 더 중요한가?
3. 숨은 단말(hidden node)이나 노출 단말(exposed node) 문제가 있는가?
4. 사용량 패턴이 예측 가능한가, 버스트형인가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 모든 환경에 동일한 접근 방식을 적용하는 것
- 무선에서 [CSMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/104_csma/)/CD처럼 충돌 검출을 기대하는 것
- 실시간 서비스에 경쟁형 접속만 두는 것

    - **📢 섹션 요약 비유**: 줄을 못 보면 서로 부딪히고, 줄을 잘 세우면 덜 기다린다.

    ---

    ## Ⅴ. 기대효과 및 결론

    다중 접속은 공유 [매체](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)를 효율적으로 쓰게 하지만, 물리적 한계를 없애지는 못한다. 따라서 좋은 방식이란 "모든 상황에 가장 빠른 것"이 아니라 "해당 환경의 제약을 가장 잘 감당하는 것"이다.

결국 [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 계층의 설계는 자원 분배, 충돌 제어, [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 예측을 동시에 다루는 균형 문제로 기억해야 한다.

    - **📢 섹션 요약 비유**: 놀이터를 같이 쓰되, 누가 언제 그네를 탈지 정하는 규칙이 필요하다.

    ---

    ### 📌 관련 개념 맵

    | 개념 | 연결 포인트 |
| :-- | :-- |
| [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) (Medium [Access Control](/knowledge-base/studynote/02_operating_system/09_file_system/547_access_control_rwx/)) | 공유 [매체](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) 제어 계층 |
| [FDMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/088_주파수_분할_다중접속_FDMA/) | [주파수 분할 방식](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/552_fdd_vs_tdd_wireless_duplexing/) |
| [TDMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/089_시분할_다중접속_TDMA/) | 시간 분할 방식 |
| [CDMA](/knowledge-base/studynote/03_network/19_frequent_topics_terms/957_cdma_code_division_multiple_access_dsss_orthogonality/) | 코드 분할 방식 |
| [CSMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/104_csma/)/[CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) | 무선 충돌 회피 방식 |

    ### 📈 관련 키워드 및 발전 흐름도

    공유 [매체](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) 등장
    │
    ▼
[FDMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/088_주파수_분할_다중접속_FDMA/) / [TDMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/089_시분할_다중접속_TDMA/) / [CDMA](/knowledge-base/studynote/03_network/19_frequent_topics_terms/957_cdma_code_division_multiple_access_dsss_orthogonality/)
    │
    ▼
[CSMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/104_csma/) / [ALOHA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/111_aloha_protocol/) 계열
    │
    ▼
[OFDMA](/knowledge-base/studynote/03_network/19_frequent_topics_terms/945_ofdma_orthogonal_frequency_division_multiple_access_resource_block/) / 스케줄링 / [QoS](/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 중심 설계

    ### 👶 어린이를 위한 3줄 비유 설명

    1. 놀이터를 여러 반이 같이 쓰면 줄을 정해야 해요.
    2. 먼저 줄을 설지, 시간이 올 때까지 기다릴지 방법이 달라요.
    3. 그래서 통신도 누가 언제 쓰는지 규칙이 필요해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 87 / 1120

← **이전**: [86. CP (Cyclic Prefix) / GI (Guard Interval) - ISI 방지](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/)
**다음**: [88. FDMA (Frequency Division Multiple Access)](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/088_주파수_분할_다중접속_FDMA/) →

---
