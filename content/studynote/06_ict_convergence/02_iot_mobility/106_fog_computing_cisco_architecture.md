---
title: "106. Fog Computing Cisco Architecture"
tags:
  - "ict_convergence"
date: "2026-06-07"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 포그 컴퓨팅 (Fog Computing)은 중앙 집중형 클라우드와 말단 엣지 디바이스 사이에 라우터/게이트웨이 기반의 중간 연산 계층(포그 노드)을 두어 부하를 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)하는 아키텍처다.
> 2. **가치**: 클라우드로 가는 트래픽 폭증을 방지하고 필터링을 수행하여 응답 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)([Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))을 줄이며 네트워크 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 비용을 획기적으로 절감한다.
> 3. **판단 포인트**: 단말 자체 연산력이 부족하지만 초저지연 응답이 필요한 [스마트 시티](/studynote/06_ict_convergence/02_iot_mobility/171_smart_city_platform_architecture/)나 공장 자동화 환경에서, 근거리 네트워크 인프라에 지능을 부여할 때 도입한다.

---

## Ⅰ. 개요 및 필요성

포그 컴퓨팅 (Fog Computing)은 시스코([Cisco](/studynote/03_network/10_application_layer_dns_mgmt/539_netflow_sflow_traffic_monitoring/))가 제안한 개념으로, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 발생하는 물리적 환경(땅)과 거대한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 센터(클라우드) 사이에 컴퓨팅, 스토리지, 네트워킹 자원을 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 배치하는 계층적 처리 모델이다. 구름이 땅으로 내려와 안개(Fog)가 되었다는 뜻을 담고 있다.

[IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 디바이스가 폭발적으로 증가하면서 모든 기기가 발생시키는 로우 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)([Raw](/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 중앙 클라우드로 전부 전송하는 것은 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 고갈과 비용 폭탄을 초래했다. 특히 자율주행이나 산업 제어처럼 수 밀리초(ms)의 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)조차 치명적인 환경에서는 왕복 통신 시간이 긴 클라우드를 맹신할 수 없다. 그렇다고 배터리와 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 제약이 있는 말단 센서가 모든 연산을 감당할 수도 없기에 중간 [허브](/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/) 역할의 해결사가 필요해졌다.

- **📢 섹션 요약 비유**: 클라우드는 똑똑하지만 왕복 10시간이 걸리는 '서울 본사'이고, 단말기(센서)는 일은 하지만 판단력이 없는 '말단 사원'이다. 포그 컴퓨팅은 본사로 가는 연락을 1차로 걸러내고 즉석에서 의사결정을 내려주는 '동네 지역 본부장(포그 노드)'을 중간에 세우는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

포그 컴퓨팅은 크게 디바이스(단말) -> 포그 노드 -> 클라우드의 3계층(3-Tier) 아키텍처로 구성된다.

| 계층 | 주요 장비 | 핵심 역할 (기능) | 처리 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| :--- | :--- | :--- | :--- |
| **디바이스 (Edge)** | 스마트 가로등, 온도 센서, [CCTV](/studynote/09_security/18_iot_ot_physical/933_cctv/) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집 및 물리적 환경 제어 | 로우 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) ([Raw](/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) |
| **포그 층 (Fog Node)** | 라우터, 게이트웨이, [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/), 셋톱박스 | <strong>실시간 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 필터링, 로컬 제어, <a href="/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a></strong> | 시간 민감형 실시간 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| **클라우드 (Cloud)** | AWS, Azure 등 대형 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 센터 | 장기 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장, 딥러닝, 글로벌 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 수립 | 정제된 요약 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 및 빅데이터 |

```text
+--------------------------------------------------------------+
|             포그 컴퓨팅의 3계층 데이터 처리 흐름               |
+--------------------------------------------------------------+
|  [ 클라우드 층 (Cloud Layer) ]                               |
|  - 글로벌 분석, 딥러닝 훈련 (응답속도: 수 초 ~ 일 단위)      |
|          ^ (필터링된 알짜 데이터만 전송)                      |
|          |                                                   |
| - - - - -|- - - - - - WAN / 코어 네트워크 - - - - - - - - -  |
|          v (정책 및 모델 업데이트)                            |
|  [ 포그 층 (Fog Layer) ] ★ 핵심                             |
|  - 동네 라우터, 스마트 게이트웨이                             |
|  - 즉각적 제어, 쓰레기 데이터 폐기 (응답속도: ms 단위)         |
|          ^ (초당 수천 개의 로우 데이터 쏟아짐)                |
|          |                                                   |
| - - - - -|- - - - - - LAN / 무선 네트워크 - - - - - - - - -  |
|          |                                                   |
|  [ 디바이스 층 (Edge Devices) ]                              |
|  - CCTV 센서, 로봇 팔, 스마트 워치                           |
+--------------------------------------------------------------+
```

포그 노드는 통신망 기지국이나 사내 라우터 등 인프라 장비에 소규모 서버급 연산 능력을 탑재하여, 의미 없는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(예: "온도 변화 없음")는 즉시 폐기하고 중요 이벤트만 클라우드로 넘겨 트래픽 다이어트를 수행한다.

- **📢 섹션 요약 비유**: 정수기에 비유하자면, 댐(클라우드)에서 끌어온 흙탕물(로우 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 바로 마시는 게 아니라, 아파트 단지 입구에 대형 필터(포그 노드)를 설치해 불순물을 싹 걷어내고 맑은 물(의미 있는 정보)만 통과시키는 원리다.

---

## Ⅲ. 비교 및 연결

포그 컴퓨팅은 [엣지 컴퓨팅](/studynote/12_it_management/05_security_compliance/235_edge_computing_smart_factory/)([Edge Computing](/studynote/12_it_management/05_security_compliance/235_edge_computing_smart_factory/)) 및 [클라우드 컴퓨팅](/studynote/02_operating_system/01_overview_architecture/052_cloud_computing_os/)과 상호 보완적으로 작동하며, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리의 '물리적 위치'에 따라 경계가 나뉜다.

| 구분 | 위치 중심 | 컴퓨팅 파워 | [지연 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)([Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)) | 통신 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 절감 |
| :--- | :--- | :--- | :--- | :--- |
| <strong><a href="/studynote/02_operating_system/01_overview_architecture/052_cloud_computing_os/">클라우드 컴퓨팅</a></strong> | 중앙 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 센터 | 무한대 (가장 높음) | 100ms 이상 (가장 긺) | 없음 (모든 트래픽 발생) |
| **포그 컴퓨팅** | 근거리 인프라 (라우터 등) | 중간 (서버/PC급) | 수 ms (빠름) | 높음 (게이트웨이 단에서 필터링) |
| <strong><a href="/studynote/12_it_management/05_security_compliance/235_edge_computing_smart_factory/">엣지 컴퓨팅</a></strong> | 종단 기기 자체 (센서 칩 내부) | 낮음 (모바일 칩셋급) | < 1ms (초저지연) | 극도로 높음 (자체 처리 후 폐기) |

- **포그 vs 엣지**: 실무적으로 혼용되기도 하나, 엄밀히 말해 <strong>엣지</strong>는 자율주행차 본체 내부에 달린 칩셋에서 연산하는 것이고, <strong>포그</strong>는 그 도로변에 서 있는 신호등(게이트웨이)들이 모여 통신과 연산을 분담하는 인프라 관점이다.

- **📢 섹션 요약 비유**: 클라우드가 중앙 정부, 포그 컴퓨팅이 지방 자치 단체(도/시청)라면, [엣지 컴퓨팅](/studynote/12_it_management/05_security_compliance/235_edge_computing_smart_factory/)은 시민 개개인이 직접 판단하고 행동하는 자가 방범대다. 지방 자치 단체(포그)가 있어야 개별 시민(엣지)과 중앙 정부(클라우드) 사이의 행정 마비(트래픽 병목)가 발생하지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

포그 컴퓨팅 설계 시, 아키텍트는 "어떤 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 포그에 남기고 어떤 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 클라우드로 보낼 것인가"를 엄격히 분리해야 한다.

### 1. 실무 도입 판단 기준 (채택 시나리오)
- <strong>수천 대의 CCTV를 운영하는 <a href="/studynote/06_ict_convergence/02_iot_mobility/171_smart_city_platform_architecture/">스마트 시티</a></strong>: 모든 영상을 클라우드로 보내면 통신비가 감당 불가. 포그 노드(가로등 라우터)에서 번호판이나 사람 얼굴만 인식해 텍스트 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 클라우드로 전송.
- <strong>수 밀리초의 제어가 필요한 <a href="/studynote/06_ict_convergence/02_iot_mobility/166_smart_factory/">스마트 팩토리</a></strong>: 로봇 팔이 멈추는 긴급 정지 판단은 클라우드 통신을 기다리면 이미 사고가 발생하므로 포그 게이트웨이에서 즉각 명령 하달.

### 2. [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 포그 노드 장비에 대해 물리적/논리적 보안 방어를 누락하는 것. [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)된 라우터는 해커가 물리적으로 접근하기 가장 쉬운 타겟이다.

- **📢 섹션 요약 비유**: 동네 파출소(포그 노드)를 지어놨는데 문을 활짝 열어두고 비밀번호를 써 붙여놓는다면 동네 전체가 털린다. 포그는 클라우드보다 물리적으로 외부에 노출되어 있어 철저한 방패(보안)가 필수적이다.

---

## Ⅴ. 기대효과 및 결론

포그 컴퓨팅은 클라우드의 한계를 완벽히 보완하며, [지연 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) 최소화(Low [Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)), 위치 인식(Location Awareness), 광범위한 지리적 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/), [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 비용 절감이라는 막대한 이점을 제공한다.

하지만 수많은 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 노드를 관리하고 [오케스트레이션](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/)([Orchestration](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/))해야 하는 복잡성 증가와 노드 자체의 보안 취약성은 해결해야 할 과제로 남는다. 결론적으로 포그 컴퓨팅은 모든 기기가 인터넷에 연결되는 만물인터넷(IoE) 시대에, 클라우드의 뇌 과부하를 막아주는 필수적인 신경망(척수) 역할을 수행할 것이다.

- **📢 섹션 요약 비유**: 포그 컴퓨팅은 우리 몸의 척수 반사와 같다. 뜨거운 냄비에 손이 닿았을 때 뇌(클라우드)까지 신호가 가서 판단하기를 기다리지 않고, 척수(포그 노드)가 즉시 손을 떼라고 명령하여 화상을 막아주는 생존 시스템이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 클라우드 (Cloud) | 포그 노드가 정제한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 받아 최종 빅데이터 분석 및 모델링 수행 |
| [엣지 컴퓨팅](/studynote/12_it_management/05_security_compliance/235_edge_computing_smart_factory/) ([Edge Computing](/studynote/12_it_management/05_security_compliance/235_edge_computing_smart_factory/)) | 포그보다 더 말단 기기(센서 자체)에 지능을 부여하는 극단적 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 기법 |
| 만물인터넷 (IoE) | 수백억 개의 기기가 연결될 때 포그 컴퓨팅 도입을 강제하는 근본적 원인 |
| 실시간 분석 ([Real-time Analytics](/studynote/13_cloud_architecture/05_data_engineering/277_real_time_analytics_architecture/)) | 포그 층에서 로우 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 걸러내어 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 없이 수행해야 하는 핵심 임무 |

### 📈 관련 키워드 및 발전 흐름도

```text
중앙 집중형 클라우드 컴퓨팅 (Cloud)
    |
    v
모바일 통신 및 트래픽 폭증 · 지연(Latency) 한계 직면
    |
    v
포그 컴퓨팅 (Fog Computing) · 인프라/게이트웨이 단의 분산 처리
    |
    v
엣지 컴퓨팅 (Edge Computing) · 단말 기기 자체의 지능화 (AIoT)
    |
    v
클라우드-포그-엣지 협력 아키텍처 (Hybrid Distributed Architecture)
```

### 👶 어린이를 위한 3줄 비유 설명

1. 아주 먼 곳에 있는 '구름(클라우드)'에게 질문하면 대답을 듣는 데 시간이 너무 오래 걸려요.
2. 그래서 우리 동네 골목마다 똑똑한 '안개(포그)' 아저씨들을 세워두고 즉석에서 대답을 듣기로 했어요.
3. 포그 컴퓨팅은 모든 걸 멀리 있는 왕에게 묻지 않고, 동네 대장님(공유기/라우터)이 쓸데없는 잔심부름을 대신 처리해주는 똑똑한 시스템이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 106 / 552

<- **이전**: [105. 엣지 컴퓨팅 (Edge Computing) - 클라우드로 모든 데이터를 보내지 않고 디바이스 주변(엣지)에서 데이터를 실시간](/studynote/06_ict_convergence/02_iot_mobility/105_edge_computing_zero_latency/)
**다음**: [107. 초연결 사회 (Hyper-connected Society)](/studynote/06_ict_convergence/02_iot_mobility/107_hyper_connected_society/) ->

---
