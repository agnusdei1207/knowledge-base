---
title: 877. RESTCONF 프로토콜
date: '2026-05-08'
tags:
- studynote-network
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: RESTCONF [[295_protocol_field_tcp_udp_icmp|프로토콜]]은 [[633_sdn_whitebox|SDN]]/NFV에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: RESTCONF [[295_protocol_field_tcp_udp_icmp|프로토콜]]을 이해하면 [[164_policy|정책]] 유연성과 자동화 수준 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **NETCONF의 진입 장벽**: 완벽한 [[191_transaction_concept_states|트랜잭션]](Commit/[[313_rollback|Rollback]])을 보장하지만, [[538_ssh_vs_telnet_secure_remote|SSH]] 터널을 뚫고 무거운 XML 트리 구조를 파싱해야 해서 웹 앱(모바일 대시보드 등)에서 가볍게 [[238_switch_operation_principles|스위치]]를 조종하기엔 너무 무겁고 코딩하기 빡셌습니다.
- **RESTCONF의 탄생**: IETF는 876번에서 만들어둔 뼈대(**YANG 모델**)는 그대로 재활용하되, 배달 오토바이(NETCONF [[295_protocol_field_tcp_udp_icmp|프로토콜]])만 전 세계 웹 표준인 **[[974_restful_api_stateless_http_methods_uri|RESTful API]] ([[461_http_stateless_connection_oriented|HTTP]] 기반)**로 싹 바꿔 치기 한 가벼운 버전의 통신 규약을 발표했습니다.

```text
[YANG (Yet Another Next G…]
    │
    ▼
[RESTCONF 프로토콜]
    │
    └──▶ [오픈컨피그]
```

- **📢 섹션 요약 비유**: RESTCONF [[295_protocol_field_tcp_udp_icmp|프로토콜]]은 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [[170_selectivity_cardinality_distribution_tuning|선택도]] 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 전 세계 웹 표준: [[461_http_stateless_connection_oriented|HTTP]] Methods (CRUD 맵핑)
웹 개발자들이 숨 쉬듯 쓰는 [[461_http_stateless_connection_oriented|HTTP]] 방식을 [[238_switch_operation_principles|스위치]] 조작에 1:1로 박아 넣었습니다.
- `GET`: [[238_switch_operation_principles|스위치]]의 현재 [[009_config|설정]]이나 [[339_routing_overview_best_path_selection|라우팅]] 테이블(상태) 좀 읽어와! (Read)
- `POST`: [[238_switch_operation_principles|스위치]]에 새로운 [[224_vlan_virtual_lan_broadcast_domain|VLAN]] 방 하나 새로 파라! (Create)
- `PUT / PATCH`: [[238_switch_operation_principles|스위치]] 1번 [[446_port_and_bus|포트]]의 IP 주소를 이걸로 덮어씌워라! (Update)
- `DELETE`: 아까 만든 [[224_vlan_virtual_lan_broadcast_domain|VLAN]] 방 삭제해! (Delete)
- **장점**: 이제 통신 장비 매뉴얼을 배울 필요 없이, 평범한 파이썬이나 자바스크립트 개발자가 `fetch()` 함수 한 줄만 날리면 시스코 코어 라우터의 IP가 1초 만에 바뀝니다.

### 2. 가벼운 [[001_dikw_pyramid|데이터]] 포맷 ([[343_json|JSON]] 지원) 🌟
- NETCONF는 오직 답답하고 꺾쇠가 많은 무거운 **XML**만 지원했습니다.
- RESTCONF는 XML은 물론이고, 현대 웹 개발의 영혼인 **[[343_json|JSON]] (JavaScript Object Notation)** [[001_dikw_pyramid|데이터]] 형식을 완벽하게 지원합니다. 브라우저에서 [[238_switch_operation_principles|스위치]] 상태를 JSON으로 받아 0.1초 만에 모니터링 대시보드 그래프로 예쁘게 그려낼 수 있습니다.

### 3. URL 기반의 직관적인 [[001_dikw_pyramid|데이터]] 트리 접근
- YANG 모델이 잡아둔 계층 구조를, 그냥 인터넷 주소(URL)처럼 접근합니다.
- 예: `GET https://스위치IP/restconf/data/interfaces/interface=eth1` 
- 주소창에 저렇게만 치고 엔터를 누르면, [[238_switch_operation_principles|스위치]]의 1번 랜선 [[446_port_and_bus|포트]] [[009_config|설정]]값이 JSON으로 주르륵 쏟아져 나옵니다. 미치도록 직관적입니다.

```text
[YANG (Yet Another Next G…]
    │
    ▼
[RESTCONF 프로토콜]
    │
    └──▶ [오픈컨피그]
```

- **📢 섹션 요약 비유**: RESTCONF [[295_protocol_field_tcp_udp_icmp|프로토콜]]의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

RESTCONF가 다 좋은데 왜 아직도 핵심 코어망에서는 NETCONF를 쓸까요?

- **치명적 단점 ([[191_transaction_concept_states|트랜잭션]] 부재)**: RESTCONF는 [[461_http_stateless_connection_oriented|HTTP]] 기반의 가벼운 [[239_stateless_redis|Stateless]](무상태) 통신이라, NETCONF의 최고 존엄 기능인 **[Candidate 예비 저장소 ➜ 완벽할 때 한 번에 Commit ➜ 에러 시 [[313_rollback|Rollback]]]** 이라는 거대한 국가망 [[238_switch_operation_principles|스위치]] 동시 [[009_config|설정]] 덮어쓰기([[193_atomicity_all_or_nothing|원자성]]) 기능이 없습니다. 
- 한 줄 치면 한 줄이 바로 [[238_switch_operation_principles|스위치]]에 바로 꽂히기 때문에(실시간 덮어쓰기), 1,000대를 튜닝하다가 500대째에서 인터넷이 끊기면 망 전체가 짝짝이가 되는 대재앙([[098_rollback_strategy_pipeline_error_threshold|롤백]] 불가)이 터질 위험이 있습니다.

RESTCONF [[295_protocol_field_tcp_udp_icmp|프로토콜]]을 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. YANG (Yet Another Next G…가 기반 조건을 만든다면, RESTCONF [[295_protocol_field_tcp_udp_icmp|프로토콜]]은 그 위에서 핵심 메커니즘을 구현하고, [[878_openconfig_vendor_neutral_yang_model|오픈컨피그]]는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 [[164_policy|정책]] 유연성과 자동화 수준에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | YANG (Yet Another Next G…의 기반 정리 | RESTCONF [[295_protocol_field_tcp_udp_icmp|프로토콜]]의 핵심 동작 | [[878_openconfig_vendor_neutral_yang_model|오픈컨피그]]의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | [[164_policy|정책]] 유연성 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [[396_validation|확인]] | 현재 메커니즘의 적합성 판단 | 운영·확장 [[268_strategy_pattern|전략]] 연결 |

- **📢 섹션 요약 비유**: RESTCONF [[295_protocol_field_tcp_udp_icmp|프로토콜]]은 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

- **컨트롤러 ➜ [[238_switch_operation_principles|스위치]] 기계 (사우스바운드)**: [[191_transaction_concept_states|트랜잭션]]과 생사 [[396_validation|확인]]이 목숨같이 중요한 밑바닥 기계 조작에는 여전히 무겁고 단단한 **NETCONF**를 주로 씁니다.
- **앱 ➜ 컨트롤러 (노스바운드)**: 외부의 웹 개발자나 사내 모바일 앱이 컨트롤러에게 명령을 던질 때는, 조작이 편한 **RESTCONF([[477_rest_api_architecture|REST API]])**를 뚫어주어 웹과 통신망의 융합 생태계를 완성합니다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: **NETCONF**가 변호사와 회계사(통신 엔지니어)들이 서류를 챙겨 팩스와 인감도장([[538_ssh_vs_telnet_secure_remote|SSH]]/XML/Commit)으로 깐깐하게 계약서를 작성하는 '무겁지만 절대 실수 없는 정통 계약 방식'이라면, **RESTCONF**는 배달의 민족 앱(웹 프로그래밍)으로 햄버거를 시키는 '초간편 터치 주문 방식([[461_http_stateless_connection_oriented|HTTP]]/[[343_json|JSON]])'입니다. 햄버거를 시킬 때 메뉴 장바구니(YANG 모델) 규격은 똑같이 지키지만, 복잡한 인감도장 [[396_validation|확인]] 절차 없이 그냥 스마트폰에서 결제 버튼(POST/GET)만 틱 누르면 주방([[238_switch_operation_principles|스위치]] 장비)에 명령이 즉시 전달됩니다. 주문이 너무 쉬워져서 전 세계 웹 개발자 누구나 통신망을 장난감처럼 다룰 수 있게 해준 혁명적인 인터페이스 간소화 모델입니다.

---

## Ⅴ. 기대효과 및 결론

RESTCONF [[295_protocol_field_tcp_udp_icmp|프로토콜]]은 [[633_sdn_whitebox|SDN]]/NFV를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 [[164_policy|정책]] 유연성 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [[878_openconfig_vendor_neutral_yang_model|오픈컨피그]], 프로그래머블 네트워크, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 프로그래머블 네트워크 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: RESTCONF [[295_protocol_field_tcp_udp_icmp|프로토콜]]은 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| YANG (Yet Another Next G… | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 제어 평면 (Control Plane) | [[164_policy|정책]]과 경로 결정을 담당한다. |
| [[001_dikw_pyramid|데이터]] 평면 ([[001_dikw_pyramid|Data]] Plane) | 실제 패킷 전달을 수행한다. |
| [[878_openconfig_vendor_neutral_yang_model|오픈컨피그]] | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: YANG (Yet Another Next G…]
    │
    ▼
[현재 개념: RESTCONF 프로토콜]
    │
    ├──▶ [확장 A: 오픈컨피그]
    └──▶ [확장 B: 프로그래머블 네트워크]
```

RESTCONF [[295_protocol_field_tcp_udp_icmp|프로토콜]]는 YANG (Yet Another Next G…에서 출발해 현재 메커니즘을 정교화하고, 이후 [[878_openconfig_vendor_neutral_yang_model|오픈컨피그]]와 프로그래머블 네트워크 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 장난감 차를 움직이는 조종기와 차체를 따로 생각하면 바꾸기 쉬워져요.
2. 이 개념은 네트워크의 머리와 몸을 나눠 더 쉽게 프로그램하게 해줘요.
3. 그래서 새 규칙을 더 빨리 넣고 바꿀 수 있어요.
