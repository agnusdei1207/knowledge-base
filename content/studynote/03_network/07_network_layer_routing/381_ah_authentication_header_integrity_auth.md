---
title: "381. AH (Authentication Header)"
date: "2026-05-08"
tags:
  - "studynote-network"
weight: 381
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: AH는 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)과 경로 제어에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: AH를 이해하면 수렴 속도과 확장성 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: IP [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)그램에 대한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성](/studynote/09_security/01_intro_principles/003_integrity/)([Integrity](/studynote/09_security/01_intro_principles/003_integrity/)), [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 원천 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)([Authentication](/studynote/02_operating_system/10_security/604_authentication_factors/)), 그리고 [재전송 공격](/studynote/09_security/03_network_security/274_replay_attack/) 방지(Anti-replay) 기능을 제공하는 [IPsec](/studynote/01_computer_architecture/15_advanced_topics/589_ipsec_offload/) 확장 헤더 (RFC 4302). IP [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 번호 51번을 사용한다.
- **필요성**: 인터넷 초기에는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 몰래 훔쳐보는 것(스니핑)보다, 남의 이름으로 송금 패킷을 조작해서 보내는 위조/변조 공격이 더 두려웠다. "야, 암호화는 컴퓨터가 계산하느라 너무 느리니까 빼고, 대신 **누가 보냈는지 확실히 서명하고 중간에 단 1바이트라도 조작되면 즉각 알아채서 버리는 도장(해시값)만 찍어 보내자!**"라는 가벼운 보안 목적으로 탄생했다.

- **💡 비유**: AH는 편지에 찍는 <strong>"투명한 밀랍 씰(봉인)"</strong>과 같습니다.
  - 편지 봉투가 투명해서 우체부나 길가는 사람(해커) 누구나 **안의 내용을 다 읽을 수 있습니다 (암호화 ❌)**.
  - 하지만 밀랍 씰(해시값)이 찍혀 있어서, 누군가 편지 내용을 단 한 글자라도 고치려고 봉투를 뜯으면 씰이 깨집니다.
  - 수취인은 씰이 깨진 편지를 받으면 즉시 <strong>"조작된 가짜 편지!"라고 인식하고 찢어버립니다 (<a href="/studynote/09_security/01_intro_principles/003_integrity/">무결성</a> ⭕)</strong>.

```text
[IPSec 메커니즘]
    |
    v
[AH]
    |
    +---> [ESP]
```

- **📢 섹션 요약 비유**: ** AH는 내용물이 훤히 보이는 **"투명 강화 유리 금고"**입니다. 도둑이 금고 안의 금괴([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 가져갈 수는 없지만, 금괴에 적힌 일련번호(비밀번호)는 밖에서 빤히 다 들여다볼 수 있어 진정한 의미의 보안([기밀성](/studynote/09_security/01_intro_principles/002_confidentiality/))이라고 부를 수 없습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. [무결성](/studynote/09_security/01_intro_principles/003_integrity/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) ([HMAC](/studynote/03_network/13_network_security_basics/674_hmac_hash_based_mac_ipsec/))
AH는 패킷을 보낼 때 SHA-256이나 [MD5](/studynote/03_network/13_network_security_basics/668_md5_hash_collision_vulnerability/) 같은 해시(Hash) 알고리즘을 돌린다.
- 보낼 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 덩어리를 믹서기에 넣고 갈아서 `A1B2C3`라는 짤막한 암구호([MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 값)를 만든 뒤 AH 헤더에 붙여 보낸다.
- 받는 쪽도 똑같이 믹서기에 갈아보고, 자기가 갈아본 결과와 겉면에 적힌 `A1B2C3`가 완벽히 똑같은지 비교한다.
- 단 1비트라도 해커가 중간에서 조작했다면 결과가 `Z9Y8X7`로 완전히 다르게 나오므로 즉각 폐기(Drop)한다.

### 2. AH의 치명적인 한계: NAT와의 충돌 (왜 멸종했는가?)
이것이 네트워크 실무와 시험에서 AH를 쓰레기통에 처박은 핵심 이유다.
- **AH의 계산 범위**: AH는 [무결성](/studynote/09_security/01_intro_principles/003_integrity/) 믹서기를 돌릴 때, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)뿐만 아니라 <strong>"IP 헤더의 출발지/목적지 주소"</strong>까지 통째로 갈아서 도장([MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/))을 찍는다.
- <strong><a href="/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/">NAT</a>(공유기)의 개입</strong>: 내 [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)(`192.168.0.5`)에서 AH 도장을 찍고 패킷을 던졌다. 이 패킷이 우리 집 공유기를 통과할 때, 공유기([NAT](/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/))는 출발지 주소를 공인 IP(`211.200.x.x`)로 <strong>바꿔치기(변조)</strong>한다.
- **목적지의 판정**: 목적지 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)이 패킷을 받아 믹서기를 돌려본다. "어? 내가 받은 패킷의 출발지 IP(`211.x.x.x`)로 계산해 보니, 아까 네가 찍은 도장(`192.x.x.x`로 만든 값)이랑 안 맞네? **너 중간에 해커한테 조작당했지! (사실 공유기가 바꾼 건데)**"라며 무조건 패킷을 다 버려버린다.

```text
 +-------------------------------------------------------------+
 |                AH와 NAT(공유기)의 처절한 충돌 시나리오           |
 +-------------------------------------------------------------+
 |                                                             |
 |   [ 내 PC (사설 IP 10.x) ]                                     |
 |       |                                                     |
 |       | 1. "출발지가 10.x 라는 걸 포함해서 무결성 도장 쾅!" (AH 생성) |
 |       v                                                     |
 |   [ 집 공유기 (NAT) ]                                         |
 |       |                                                     |
 |       | 2. "오 밖으로 나가네? 출발지를 내 공인 IP(211.x)로 바꿔야지!" |
 |       v                                                     |
 |   [ 목적지 방화벽 (VPN 서버) ]                                   |
 |                                                             |
 |   * 검사 결과: "출발지 IP가 211.x로 바뀌었네? 근데 AH 도장은 10.x를  |
 |               기준으로 찍혀있잖아? 중간에 누가 IP를 뜯어고쳤네! 버려!" |
 |                                                             |
 |   -> 결과: 세상 모든 집/회사는 공유기(NAT)를 쓰므로 AH는 100% 연결 실패함!|
 +-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: AH의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

AH를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [IPSec](/studynote/01_computer_architecture/15_advanced_topics/589_ipsec_offload/) 메커니즘이 기반 조건을 만든다면, AH는 그 위에서 핵심 메커니즘을 구현하고, ESP는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 수렴 속도과 확장성에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [IPSec](/studynote/01_computer_architecture/15_advanced_topics/589_ipsec_offload/) 메커니즘의 기반 정리 | AH의 핵심 동작 | ESP의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 수렴 속도 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: AH는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

보안 솔루션 현업에서 [VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) 세팅을 할 때, AH를 선택하는 옵션조차 제공하지 않는 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 장비들이 태반이다. 오직 다음 장에서 배울 <strong><a href="/studynote/03_network/07_network_layer_routing/382_esp_encapsulating_security_payload_confidentiality/">ESP</a>(암호화 + <a href="/studynote/09_security/01_intro_principles/003_integrity/">무결성</a> 동시 지원)</strong>만이 유일한 정답으로 쓰이고 있다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: ** AH는 서류에 **"내 사설 IP([10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/).x.x.x)를 적어 넣고 인감도장"**을 찍어 보낸 꼴입니다. 우체국([NAT](/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/))이 배달 편의를 위해 겉면 주소를 공인 IP로 덧칠하는 순간, 원본 인감도장과 내용이 불일치하게 되어 서류 전체가 위조 문서로 판정받고 파쇄기에 들어갑니다.

---

## Ⅴ. 기대효과 및 결론

AH는 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)과 경로 제어를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 수렴 속도 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [ESP](/studynote/03_network/07_network_layer_routing/382_esp_encapsulating_security_payload_confidentiality/), 의도 기반 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/), 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 의도 기반 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: AH는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [IPSec](/studynote/01_computer_architecture/15_advanced_topics/589_ipsec_offload/) 메커니즘 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 테이블 ([Routing](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) Table) | 패킷 전달 의사결정의 기준이 된다. |
| [메트릭](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) ([Metric](/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)) | 최적 경로를 선택하는 비교 척도다. |
| [ESP](/studynote/03_network/07_network_layer_routing/382_esp_encapsulating_security_payload_confidentiality/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: IPSec 메커니즘]
    |
    v
[현재 개념: AH]
    |
    +---> [확장 A: ESP]
    +---> [확장 B: 의도 기반 라우팅]
```

AH는 [IPSec](/studynote/01_computer_architecture/15_advanced_topics/589_ipsec_offload/) 메커니즘에서 출발해 현재 메커니즘을 정교화하고, 이후 ESP와 의도 기반 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 여러 갈림길이 있는 미로에서 가장 좋은 길을 고르는 게임과 같아요.
2. 이 개념은 길이 막히면 다른 길로 빨리 바꾸는 규칙도 알려줘요.
3. 그래서 인터넷 길찾기가 덜 헤매고 더 똑똑해져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 502 / 1120

<- **이전**: [380. IPSec (IP Security Framework) 메커니즘](/studynote/03_network/07_network_layer_routing/380_ipsec_ip_security_framework/)
**다음**: [382. ESP (Encapsulating Security Payload)](/studynote/03_network/07_network_layer_routing/382_esp_encapsulating_security_payload_confidentiality/) ->

---
