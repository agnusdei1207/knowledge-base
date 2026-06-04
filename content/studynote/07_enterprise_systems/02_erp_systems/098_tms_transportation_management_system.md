+++
title = "98. TMS (Transportation Management System) - 운송 관리 시스템"

[taxonomies]
tags = ["enterprise_systems"]

[extra]
tags = ["enterprise_systems"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: TMS (Transportation [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/1013_management/) System)는 물류 창고에서 출고된 화물이 최종 목적지에 도달하기까지의 배차, 경로 최적화, 운송 추적, 운임 정산의 전 과정을 통제하는 물류 관제 플랫폼이다.
> 2. **가치**: 수많은 차량과 목적지가 얽힌 복잡한 [외판원 문제](/knowledge-base/studynote/12_it_management/03_ea_isp/106_fenwick_tree/) ([TSP](/knowledge-base/studynote/12_it_management/03_ea_isp/106_fenwick_tree/), Traveling Salesperson Problem)를 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로 풀어내어 유류비, 인건비 등 핵심 물류 비용을 획기적으로 절감한다.
> 3. **판단 포인트**: 창고 내부의 재고와 위치는 [WMS](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/097_wms_warehouse_management_system/) ([Warehouse Management System](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/097_wms_warehouse_management_system/))로 관리하지만, 문 밖을 나서는 순간부터의 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)([지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 노선 비효율) 통제는 반드시 TMS와 GPS, 지도 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 연동을 통해 해결해야 한다.

---

## Ⅰ. 개요 및 필요성

TMS (Transportation [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/1013_management/) System)는 기업의 [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 관리 ([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Supply Chain](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/1013_management/))에서 '이동'의 효율성을 책임지는 핵심 소프트웨어다. 화물이 출발지에서 목적지까지 이동할 때 어떤 수단(트럭, 선박, 항공)을 이용하고, 어떤 경로를 거치는 것이 가장 경제적인지 결정한다.

과거에는 수백 개의 배송지를 담당자들의 감과 수기(Excel)에 의존해 배차했다. 이로 인해 트럭이 텅 빈 채로 돌아오는 공차율 증가, 비효율적인 우회 경로 탑승, 기사와의 운임 정산 분쟁 등 막대한 숨은 비용이 발생했다. 전자상거래의 폭발적 성장으로 당일 배송, 새벽 배송 등 다빈도 소량 운송이 일상화되면서 인간의 두뇌로는 수천 대 트럭의 배차 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 감당할 수 없게 되었고, 이를 자동화하는 TMS의 도입은 생존 필수가 되었다.

- **📢 섹션 요약 비유**: 아무리 주방(창고)에서 요리(포장)를 완벽하고 빠르게 해내도, 배달 기사님(TMS)이 길을 잃거나 한 번에 여러 집을 효율적으로 돌지 못하면 짜장면은 불어 터진다. TMS는 최고의 배달 동선을 짜주는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 배차 반장이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

TMS는 계획, 실행, 정산의 3단계 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인으로 동작하며, VRP (Vehicle [Routing](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) Problem)와 적재 최적화 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 시스템의 두뇌 역할을 한다.

```text
+--------------------------------------------------------------+
|                TMS (운송 관리 시스템) 프로세스 아키텍처        |
+--------------------------------------------------------------+
|  [ 입력 데이터 ]                                              |
|  - WMS 출고 오더, 차량 제원(적재량), 교통 상황 API, 배송 기한 |
|         |                                                    |
|         v                                                    |
|  +------------------------ TMS Core -----------------------+ |
|  | 1. 라우팅 & 배차 (Routing & Dispatching)                | |
|  |    : VRP 알고리즘 --> 최단 거리, 최소 요금 경로 도출         | |
|  |    : 3D 적재 테트리스 (LIFO 하차 순서 고려)               | |
|  |                                                         | |
|  | 2. 가시성 및 실시간 관제 (Visibility & Tracking)         | |
|  |    : GPS / 모바일 App 연동 --> 트럭 실시간 위치 모니터링   | |
|  |                                                         | |
|  | 3. 운임 정산 (Freight Settlement)                       | |
|  |    : 운송 거리, 유류 할증료, 톨게이트 비용 자동 계산      | |
|  +---------------------------------------------------------+ |
|         |                                                    |
|         v                                                    |
|  [ 출력 및 결과 ]                                             |
|  최적 배차 지시서, 고객 실시간 배송조회, 협력사 자동 대금 지급 |
+--------------------------------------------------------------+
```

가장 핵심이 되는 <strong><a href="/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/">라우팅</a> 및 배차</strong>는 차량의 최대 중량/부피 한계, 운전자의 법정 근로 시간, 고객의 수령 가능 시간 (Time Window) 등 수많은 제약 조건을 만족하면서 전체 비용 함수를 최소화하는 복잡한 수리계획법 모델을 푼다. 또한 하차 지점이 여러 곳일 경우, 마지막 목적지 물건을 트럭 가장 안쪽에, 첫 목적지 물건을 문 앞에 싣도록 지시하는 3D 적재 최적화(테트리스) 기능도 함께 작동한다.

- **📢 섹션 요약 비유**: TMS는 택시 기사의 '내비게이션(경로)'과 '앱미터기(정산)', 그리고 트렁크에 짐을 싣는 '공간 지각 능력(적재)'을 하나로 합친 완벽한 자율 주행 지휘소다.

---

## Ⅲ. 비교 및 연결

물류의 흐름 속에서 시스템의 통제 범위를 기준으로 WMS와 TMS를 명확히 비교해야 단절 없는 연동을 설계할 수 있다. 이 둘은 서로를 보완하며 [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) ([Enterprise Resource Planning](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/))라는 큰 우산 아래 연동된다.

| 비교 항목 | [WMS](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/097_wms_warehouse_management_system/) ([Warehouse Management System](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/097_wms_warehouse_management_system/)) | TMS (Transportation [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/1013_management/) System) |
| :--- | :--- | :--- |
| **통제 공간** | 창고 **내부** (입고, 보관, 피킹, 출고) | 창고 **외부** (도로망, 해운, 항로 등) |
| **핵심 목표** | 재고 정확도 100%, 공간 최적화, 피킹 동선 단축 | 유류비 및 운임 절감, 정시 도착(납기) 준수 |
| <strong>주요 <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong> | 존(Zone) 배정, 파도([Wave](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/590_wave_ieee_802_11p_dsrc_v2x/)) 피킹 | 차량 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) (VRP), 화물 혼재 (Consolidation) |
| **추적 대상** | 선반 위 팔레트(Pallet)와 바코드 | 도로 위 트럭의 GPS 좌표와 주행 상태 |

최근에는 창고 안에서 트럭에 짐을 싣는 도크(Dock) [스케줄](/knowledge-base/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/)링이 중요해지면서, WMS와 TMS의 경계가 허물어지고 유기적으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 주고받는 통합 물류 플랫폼 형태로 진화하고 있다.

- **📢 섹션 요약 비유**: WMS가 집 안에서 나갈 짐을 깔끔하게 캐리어에 싸두는 '정리정돈의 달인'이라면, TMS는 그 캐리어를 들고 비행기, 기차, [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)를 어떻게 갈아타야 가장 싸고 빨리 도착할지 짜주는 '최고의 여행 가이드'다.

---

## Ⅳ. 실무 적용 및 기술사 판단

[SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/) 컨설팅이나 [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) 구축 프로젝트에서 TMS는 단순한 내비게이션 이상의 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 가치를 지닌다.

### 판단 포인트
- **언제 TMS 고도화가 필요한가?**: 자가 물류 (1PL)를 하든 외주 물류 ([3PL](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/101_3pl_third_party_logistics_4pl/))를 쓰든, 배송비 정산 과정에서 엑셀 수작업으로 인한 오류와 마찰이 빈번하고 화물차의 적재율(Fill Rate)이 70%를 밑도는 구간이 존재한다면 즉시 TMS [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 도입을 검토해야 한다.
- <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 통합의 중요성</strong>: TMS 단독으로는 힘을 쓰지 못한다. ERP의 주문(Order) 정보, WMS의 부피/무게(CBM) 정보, 외부의 실시간 교통 API가 실시간으로 연동되는 [EAI](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/143_eai_enterprise_application_integration_hub/) ([Enterprise Application Integration](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/143_eai_enterprise_application_integration_hub/)) 아키텍처가 필수다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 가장 싼 화물차 기사만 무작정 배정하는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/). 운송 품질(파손, [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/))을 고려하지 않고 요금만 최적화하면 결국 고객 이탈로 이어지는 맹점에 빠진다.

- **📢 섹션 요약 비유**: 좋은 TMS 도입은 단순히 '빠른 길'을 찾는 것이 아니라, 빈 트럭으로 돌아오는 낭비(공차)를 없애고 기름값 정산 영수증을 엑셀로 맞추느라 밤새는 직원들의 야근을 없애는 기업 체질 개선 수술이다.

---

## Ⅴ. 기대효과 및 결론

TMS 도입의 가장 큰 기대효과는 <strong>운송비 절감</strong>과 <strong>가시성 (Visibility) 확보</strong>다. 경로 최적화와 혼재 배송을 통해 물류비를 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~20% 절감할 수 있으며, 배송 상태의 실시간 투명성은 고객 만족도를 극대화한다. 또한 디지털화된 운임 정산은 [3PL](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/101_3pl_third_party_logistics_4pl/) 협력사와의 투명한 거래 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 구축한다.

미래의 TMS는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반의 기상 예측, 실시간 교통 체증을 반영한 [동적 라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/341_dynamic_routing_protocol_operation/) ([Dynamic Routing](/knowledge-base/studynote/03_network/07_network_layer_routing/341_dynamic_routing_protocol_operation/)), 친환경 규제에 대응하는 탄소 배출량 최소화 경로 탐색 영역으로 확장되고 있다. 결론적으로 TMS는 물리적 재화를 움직이는 기업이 시장 경쟁력을 유지하기 위한 디지털 물류의 관제탑이다.

- **📢 섹션 요약 비유**: 수백 대의 미니카가 각자의 목적지로 마구잡이로 달리면 금방 배터리가 닳고 길도 막히지만, TMS라는 관제탑이 위에서 길을 통제해주면 모두가 가장 적은 전기로 안전하게 목적지에 골인할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| <strong><a href="/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/097_wms_warehouse_management_system/">WMS</a> (<a href="/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/097_wms_warehouse_management_system/">Warehouse Management System</a>)</strong> | TMS가 일하기 전, 창고 내 재고를 관리하고 트럭에 실을 준비를 마치는 선행 시스템 |
| <strong>VRP (Vehicle <a href="/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/">Routing</a> Problem)</strong> | 여러 대의 차량이 여러 목적지를 방문할 때 총 비용을 최소화하는 경로를 찾는 수학적 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |
| <strong><a href="/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/">SCM</a> (<a href="/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/">Supply Chain</a> <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/1013_management/">Management</a>)</strong> | 원자재부터 최종 소비자까지의 전체 [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/)을 관리하는 상위 개념 |
| <strong><a href="/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/101_3pl_third_party_logistics_4pl/">3PL</a> (Third-Party Logistics)</strong> | 기업의 물류 부문을 전문 물류업체에 아웃소싱하는 것, 이들과의 정산에 TMS가 필수 |

### 📈 관련 키워드 및 발전 흐름도

```text
수기 배차 및 엑셀 기반 정산 (비효율의 극치)
    |
    v
기본형 TMS : 고정 경로 배차 및 요율표 기반 자동 정산
    |
    v
최적화 TMS : VRP 알고리즘, 3D 적재 테트리스, GPS 가시성 확보
    |
    v
AI 및 클라우드 TMS : 실시간 동적 경로 변경, 기상 정보 반영
    |
    v
지속가능 TMS (Green Logistics) : 탄소 배출량 최소화 라우팅
```

### 👶 어린이를 위한 3줄 비유 설명

1. 마트에서 산 물건 1,000개를 전국 100명의 친구에게 나눠줘야 해요.
2. TMS는 "큰 트럭 1대에는 어느 동네 물건을 싣고, 작은 트럭 5대에는 어디를 돌게 할까?"를 초능력 컴퓨터로 계산해 주는 똑똑한 지도장관이에요.
3. 이 장관님 덕분에 트럭 아저씨들은 기름을 아끼면서 안 막히는 길로 가장 빨리 배달을 끝낼 수 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 98 / 482

<- **이전**: [97. WMS (Warehouse Management System) - 창고 관리 시스템](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/097_wms_warehouse_management_system/)
**다음**: [99. VMI (Vendor Managed Inventory) - 공급자 주도 재고 관리 (월마트 방식, 유통업체 재고를 제조사가 직접](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/099_vmi_vendor_managed_inventory/) ->

---
