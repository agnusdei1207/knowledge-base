---
title: "OpenConfig"
date: "2026-05-08"
tags:
  - "studynote-network"
weight: 878
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 오픈컨피그는 [SDN](/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/)/NFV에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: 오픈컨피그를 이해하면 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 유연성과 자동화 수준 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- YANG 모델 도입 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/), 표준화된 뼈대가 없다 보니(Native YANG), 제조사들은 각자 자기 장비의 특성을 뽐내기 위해 파편화된 서식([Schema](/studynote/05_database/04_transactions_concurrency/505_schema/))을 만들었습니다.
- **개발자의 지옥**: 자동화 프로그램(파이썬 스크립트)을 짤 때, 시스코 장비로 IP를 보낼 때는 `{"ipv4-address": "1.1.1.1"}`, 주니퍼 장비로 보낼 때는 `{"address-v4": "1.1.1.1"}`이라고 일일이 if문을 걸어 분기 처리를 해줘야 했습니다. 제조사 [벤더 종속](/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/)([Lock-in](/studynote/12_it_management/05_security_compliance/362_lock_in_portability/))이 여전했습니다.

```text
[RESTCONF]
    |
    v
[오픈컨피그]
    |
    +---> [텔레메트리]
```

- **📢 섹션 요약 비유**: 오픈컨피그는 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

- **개념**: 구글, AT&T, 마이크로소프트 등 거대 네트워크 소비자(망을 직접 깔아 쓰는 빅테크/통신사)들이 주도하는 실무 연합체입니다. 특정 벤더(제조사)의 입김을 완전히 배제하고, <strong>전 세계 모든 라우터와 <a href="/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/">스위치</a> 장비들이 100% 동일하게 사용해야 하는 '벤더 중립적인 공통 YANG <a href="/studynote/05_database/01_db_architecture_relational/014_data_model_components/">데이터 모델</a>(Standardized YANG Models)' 스키마를 찍어내어 배포하는 <a href="/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/">오픈소스</a> 프로젝트</strong>입니다.

```text
[RESTCONF]
    |
    v
[오픈컨피그]
    |
    +---> [텔레메트리]
```

- **📢 섹션 요약 비유**: 오픈컨피그의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

### 1. 단일 자동화 스크립트의 기적 (Write Once, Run Anywhere)
- 관리자가 OpenConfig가 정해준 표준 YANG 서식(`openconfig-interfaces.yang`)에 맞춰서 IP 주소를 셋팅하는 파이썬 코드를 딱 1줄 짭니다.
- [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 안에 시스코([Cisco](/studynote/03_network/10_application_layer_dns_mgmt/539_netflow_sflow_traffic_monitoring/)), 주니퍼(Juniper), 아리스타(Arista), 노키아 장비 수천 대가 마구 섞여(멀티 벤더 환경) 있어도 상관없습니다.
- 이 파이썬 코드를 1만 대의 잡탕 장비에 동시에 쏴버리면, 모든 기계가 "아! 오픈컨피그 표준 서식으로 왔네!" 하고 **제조사에 상관없이 똑같이 IP를 착착찰칵 바꿔버립니다.** (진정한 인프라 자동화 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD의 완성)

### 2. 제조사(벤더)의 굴복
- 처음엔 시스코 같은 하드웨어 벤더들이 "우리만의 고급 기능을 못 쓰잖아!"라며 반발했습니다.
- 하지만 구글이나 MS 같은 빅테크(슈퍼 갑)들이 "너네 장비가 OpenConfig 표준 서식 지원 안 해? 그럼 너네 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 1조 원어치 안 사. 딴 회사 꺼 살게."라고 협박(?)하자, 전 세계 모든 네트워크 제조사가 울며 겨자 먹기로 자사 장비 OS에 OpenConfig 번역기를 100% 내장하여 출하하게 되었습니다. 소비자(사용자)가 제조사를 이긴 위대한 생태계 전복입니다.

오픈컨피그를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. RESTCONF가 기반 조건을 만든다면, 오픈컨피그는 그 위에서 핵심 메커니즘을 구현하고, 텔레메트리는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 유연성과 자동화 수준에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | RESTCONF의 기반 정리 | 오픈컨피그의 핵심 동작 | 텔레메트리의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 유연성 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: 오픈컨피그는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

오픈컨피그는 단순히 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)([Config](/studynote/15_devops_sre/01_culture_methodology/009_config/)) 양식만 통일한 게 아닙니다. 다음 879번 문서에서 다룰 <strong><a href="/studynote/03_network/17_sdn_nfv/879_streaming_telemetry_grpc_push_based_monitoring/">스트리밍 텔레메트리</a>(<a href="/studynote/03_network/20_performance_evaluation_advanced/1058_streaming_telemetry_network_monitoring/">Streaming Telemetry</a>)</strong>의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송 양식까지 통일해 버렸습니다.
- 전국의 수만 대 이기종 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)들이 1초마다 중앙 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)(그라파나, [Grafana](/studynote/16_bigdata/08_visualization/168_grafana/))로 자신의 CPU 온도와 트래픽 양을 보고합니다.
- 제조사가 달라도 쏘아 보내는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 형식이 100% 일치(OpenConfig 모델)하므로, 중앙 서버는 복잡한 파싱이나 번역 툴 없이 수만 대의 빅데이터를 1초 만에 모아 글로벌 시야(Global [View](/studynote/05_database/03_relational_model/151_sql_view_virtual_table/)) 대시보드로 띄울 수 있습니다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: 옛날엔 회사에 이력서를 낼 때, 시스코 전용 이력서, 주니퍼 전용 이력서 등 100가지의 각기 다른 양식에 맞춰 지원자(개발자)가 일일이 내용을 고쳐서 써야 하는 미친듯한 비효율([벤더 종속](/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/))이 있었습니다. <strong>오픈컨피그(OpenConfig)</strong>는 거대 대기업(구글) 연합이 빡쳐서 선언한 '전국 공통 표준 이력서 양식'입니다. 구글은 선언합니다. "앞으로 우리와 거래하고 싶은 모든 기업은 무조건 이 '오픈컨피그 표준 이력서 1장'만 써라! 주민번호는 3번 칸, 이름은 1번 칸 무조건 고정이다!" 지원자(엔지니어)는 이제 단 한 번만 이력서(자동화 스크립트)를 작성해 두면, 전 세계 수만 개의 각기 다른 회사(이종 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 장비)에 똑같은 종이를 팩스로 밀어 넣어도 100% 서류 심사가 통과되는 마법 같은 범용 자동화 인프라를 손에 쥐게 되었습니다.

---

## Ⅴ. 기대효과 및 결론

오픈컨피그는 [SDN](/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/)/NFV를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 유연성 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 텔레메트리, 프로그래머블 네트워크, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 프로그래머블 네트워크 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: 오픈컨피그는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| RESTCONF | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 제어 평면 (Control Plane) | [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)과 경로 결정을 담당한다. |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 평면 ([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Plane) | 실제 패킷 전달을 수행한다. |
| 텔레메트리 | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: RESTCONF]
    |
    v
[현재 개념: 오픈컨피그]
    |
    +---> [확장 A: 텔레메트리]
    +---> [확장 B: 프로그래머블 네트워크]
```

오픈컨피그는 RESTCONF에서 출발해 현재 메커니즘을 정교화하고, 이후 텔레메트리와 프로그래머블 네트워크 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 장난감 차를 움직이는 조종기와 차체를 따로 생각하면 바꾸기 쉬워져요.
2. 이 개념은 네트워크의 머리와 몸을 나눠 더 쉽게 프로그램하게 해줘요.
3. 그래서 새 규칙을 더 빨리 넣고 바꿀 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 999 / 1120

<- **이전**: [877. RESTCONF 프로토콜](/studynote/03_network/17_sdn_nfv/877_restconf_http_json_yang_api_network_config/)
**다음**: [879. 스트리밍 텔레메트리](/studynote/03_network/17_sdn_nfv/879_streaming_telemetry_grpc_push_based_monitoring/) ->

---
