+++
title = "709. DoS (Denial of Service 가용성 타격 위협 목적)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DoS는 [네트워크 보안](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1117_network_security_zero_trust_policy/) 위협과 대응에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: DoS를 이해하면 탐지 가능성과 복구성 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 서버의 네트워크 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)이나 CPU, 메모리, [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 연산 자원 등 <strong>시스템 자원(Resource)을 대량의 쓰레기 트래픽으로 고갈시켜 버려, 정당한 권한을 가진 일반 사용자들이 정상적인 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>를 이용할 수 없도록(거부되도록) 마비시키는 악의적 공격 행위</strong>입니다.
- **보안 목적 타격**: CIA 트라이어드([기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/), [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/), [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)) 중에서, 시스템이 원할 때 응답해야 한다는 <strong>'<a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a>(<a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">Availability</a>)'</strong>을 정면으로 파괴하는 것이 유일한 목적입니다.

```text
[재생 공격]
    |
    v
[DoS]
    |
    +---> [분산 서비스 거부 공격 봇넷 시스템 C&C…]
```

- **📢 섹션 요약 비유**: DoS는 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

서버를 기절시키는 방법은 크게 두 가지 패턴으로 나뉩니다.

### 1. 트래픽 폭주 기반 고갈 공격 ([대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 고갈)
- **원리**: 10차선 고속도로에 수만 대의 쓰레기 덤프트럭(가짜 패킷)을 일제히 밀어 넣어 도로 자체를 꽉 막아버리는 무식하지만 확실한 물리적 공격입니다.
- 진짜 정상 고객이 접속하려 해도 이미 고속도로(네트워크 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/))가 100% 미어터진 상태라 데이터가 서버까지 도달하지 못하고 버려집니다(Drop). (예: [ICMP](/knowledge-base/studynote/03_network/06_network_layer_ip/318_icmp_internet_control_message_protocol_diagnostics/) Flood, [UDP Flood](/knowledge-base/studynote/09_security/03_network_security/256_udp_flood/) 등)

### 2. [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 약점 기반 자원 고갈 공격 (시스템 자원 고갈)
- **원리**: 무식하게 트래픽을 쏟아붓지 않습니다. 트래픽은 적지만, <strong>서버의 <a href="/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/">TCP</a>/IP 운영체제나 애플리케이션 설계의 논리적 <a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/">결함</a>(취약점)을 얄밉게 파고들어 서버 CPU나 메모리를 극심하게 소모시켜 기절하게 만드는 똑똑한 공격</strong>입니다.
- 1시간 동안 기다려야 하는 복잡한 암호 풀기 연산을 요청하거나, 전화([TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) SYN)를 걸고서 대답도 안 하고 끊어버려 서버가 전화기를 든 채 하루 종일 기다리게([세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 메모리 낭비) 만듭니다. (예: [SYN Flood](/knowledge-base/studynote/09_security/03_network_security/255_syn_flood/), [Slowloris](/knowledge-base/studynote/09_security/03_network_security/258_slowloris/) 등)

```text
[재생 공격]
    |
    v
[DoS]
    |
    +---> [분산 서비스 거부 공격 봇넷 시스템 C&C…]
```

- **📢 섹션 요약 비유**: DoS의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

- <strong>과거의 <a href="/knowledge-base/studynote/02_operating_system/10_security/599_dos_ddos_attack/">DoS</a></strong>: 1990년대 초창기에는 해커 1명이 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 좋은 슈퍼컴퓨터 1대를 돌려서 타겟 서버 1대를 마비시키는 1:1 싸움이었습니다.
- **몰락**: 하지만 타겟 서버들의 방어막([IPS](/knowledge-base/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/), 클라우드 로드밸런싱)이 강력해지고 네트워크 파이프가 기가급으로 커지자, 해커 1대의 컴퓨터가 아무리 뿜어대 봤자 서버가 간지럼만 느낄 뿐 마비되지 않게 되었습니다. 게다가 해커 컴퓨터의 IP 주소가 방화벽에 딱 걸려서 1초 만에 차단당하는 허무한 결과를 낳았습니다.
- **진화 (DDoS의 탄생)**: 혼자서는 안 되겠다고 깨달은 해커가, 전 세계 수백만 대의 남의 컴퓨터(좀비 [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/))를 바이러스로 감염시켜 노예 부대로 만든 뒤, "다 같이 돌격!" 명령을 내려 수백만 대 1의 싸움으로 체급을 우주급으로 키운 것이 바로 오늘날 악명 높은 <strong>DDoS(<a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> <a href="/knowledge-base/studynote/03_network/19_frequent_topics_terms/989_dos_denial_of_service/">서비스 거부 공격</a>, 710번 문서 <a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/">참조</a>)</strong>입니다.

DoS를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [재생 공격](/knowledge-base/studynote/03_network/14_network_security_threats/708_replay_attack_timestamp_nonce/)이 기반 조건을 만든다면, DoS는 그 위에서 핵심 메커니즘을 구현하고, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [서비스 거부 공격](/knowledge-base/studynote/03_network/19_frequent_topics_terms/989_dos_denial_of_service/) [봇넷](/knowledge-base/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/) 시스템 C&C…는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 탐지 가능성과 복구성에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [재생 공격](/knowledge-base/studynote/03_network/14_network_security_threats/708_replay_attack_timestamp_nonce/)의 기반 정리 | DoS의 핵심 동작 | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [서비스 거부 공격](/knowledge-base/studynote/03_network/19_frequent_topics_terms/989_dos_denial_of_service/) [봇넷](/knowledge-base/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/) 시스템 C&C…의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 탐지 가능성 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: [DoS](/knowledge-base/studynote/02_operating_system/10_security/599_dos_ddos_attack/) 공격은 유명 맛집(서버)을 망하게 하려는 경쟁 식당 주인의 수작입니다. 식당 문 앞 도로에 대형 트럭 수백 대를 억지로 주차해 진짜 손님의 차가 진입하지 못하게 도로를 틀어막거나(네트워크 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 고갈), 혹은 매장 안의 테이블 50개에 노숙자 50명을 앉혀놓고 메뉴판만 보며 주문은 하루 종일 안 하고 자리만 꽉 채우게 만들어(서버 자원/[세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 고갈), 밖에서 기다리는 진짜 돈을 낼 손님들이 짜증을 내며 돌아가게([서비스 거부](/knowledge-base/studynote/02_operating_system/10_security/599_dos_ddos_attack/)) 만드는 아주 얄밉고 치명적인 영업 방해 행위입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 DoS를 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [재생 공격](/knowledge-base/studynote/03_network/14_network_security_threats/708_replay_attack_timestamp_nonce/) 수준의 기본 대책으로 충분한지, 아니면 DoS가 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [서비스 거부 공격](/knowledge-base/studynote/03_network/19_frequent_topics_terms/989_dos_denial_of_service/) [봇넷](/knowledge-base/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/) 시스템 C&C…와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 탐지 가능성 부족인지, 복구성 악화인지 먼저 분리한다.
2. DoS가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [서비스 거부 공격](/knowledge-base/studynote/03_network/19_frequent_topics_terms/989_dos_denial_of_service/) [봇넷](/knowledge-base/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/) 시스템 C&C…와의 연계 방식을 함께 검증한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- DoS의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- [재생 공격](/knowledge-base/studynote/03_network/14_network_security_threats/708_replay_attack_timestamp_nonce/)와의 경계를 정리하지 않아 중복 투자나 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: DoS를 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

DoS는 [네트워크 보안](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1117_network_security_zero_trust_policy/) 위협과 대응을 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 탐지 가능성 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [서비스 거부 공격](/knowledge-base/studynote/03_network/19_frequent_topics_terms/989_dos_denial_of_service/) [봇넷](/knowledge-base/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/) 시스템 C&C…, 예측형 위협 대응, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 예측형 위협 대응 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: DoS는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [재생 공격](/knowledge-base/studynote/03_network/14_network_security_threats/708_replay_attack_timestamp_nonce/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 공격 표면 (Attack Surface) | 위협이 침투할 수 있는 노출 지점을 뜻한다. |
| [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) ([Anomaly Detection](/knowledge-base/studynote/16_bigdata/05_analysis/111_anomaly_detection/)) | 정상 패턴과 다른 징후를 찾아낸다. |
| [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [서비스 거부 공격](/knowledge-base/studynote/03_network/19_frequent_topics_terms/989_dos_denial_of_service/) [봇넷](/knowledge-base/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/) 시스템 C&C… | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: 재생 공격]
    |
    v
[현재 개념: DoS]
    |
    +---> [확장 A: 분산 서비스 거부 공격 봇넷 시스템 C&C…]
    +---> [확장 B: 예측형 위협 대응]
```

DoS는 [재생 공격](/knowledge-base/studynote/03_network/14_network_security_threats/708_replay_attack_timestamp_nonce/)에서 출발해 현재 메커니즘을 정교화하고, 이후 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [서비스 거부 공격](/knowledge-base/studynote/03_network/19_frequent_topics_terms/989_dos_denial_of_service/) [봇넷](/knowledge-base/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/) 시스템 C&C…와 예측형 위협 대응 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 나쁜 친구가 놀이터 규칙을 깨뜨리면 바로 알아차리고 막아야 해요.
2. 이 개념은 어떤 장난이 위험한지 미리 알고, 문제가 생기면 어떻게 다시 정리할지도 알려줘요.
3. 그래서 놀이터를 더 안전하게 지킬 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 830 / 1120

<- **이전**: [708. 재생 공격 (Replay Attack 방어 타임스탬프 원리 / 비표 넌스 Nonce 적용)](/knowledge-base/studynote/03_network/14_network_security_threats/708_replay_attack_timestamp_nonce/)
**다음**: [710. 분산 서비스 거부 공격 (DDoS, Distributed DoS 위협) 봇넷 시스템 C&C 서버 증폭, 감염 및 반사](/knowledge-base/studynote/03_network/14_network_security_threats/710_ddos_distributed_denial_of_service_botnet/) ->

---
