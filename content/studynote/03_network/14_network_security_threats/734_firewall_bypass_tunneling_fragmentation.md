---
title: "734. Firewall Bypass Tunneling Fragmentation"
date: "2026-05-08"
tags:
  - "studynote-network"
weight: 734
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 우회기법은 [네트워크 보안](/studynote/03_network/20_performance_evaluation_advanced/1117_network_security_zero_trust_policy/) 위협과 대응에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 우회기법을 이해하면 탐지 가능성과 복구성 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

[방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)은 겉봉투의 주소(IP)와 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 번호를 보고 패킷을 차단합니다. 이를 속이는 방법은 크게 <strong>'내용물 숨기기(<a href="/studynote/03_network/07_network_layer_routing/377_tunneling_mechanism_overview/">터널링</a>)'</strong>와 <strong>'검사기 눈 피하기(<a href="/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/">단편화</a>)'</strong> 두 가지로 나뉩니다.

```text
[포트 스캐닝 도구 작동 메커니즘 (NMAP…]
    |
    v
[방화벽 우회기법]
    |
    +---> [비인가 AP]
```

- **📢 섹션 요약 비유**: [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 우회기법은 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

금지된 데이터를 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)이 허용하는 정상적인 프로토콜의 뱃속에 집어넣어(캡슐화) 검문소를 무사통과하는 가장 강력한 우회 기법입니다.

### 1. [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) / [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) [터널링](/studynote/03_network/07_network_layer_routing/377_tunneling_mechanism_overview/) ([포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 우회)
- **문제 상황**: 회사가 보안을 위해 80번([HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/))과 53번([DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/)) [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 빼고는 카카오톡이나 게임, 원격접속([SSH](/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/)) [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 싹 다 막아버렸습니다.
- <strong>해결(<a href="/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/">HTTP</a> 우회)</strong>: 해커는 막혀버린 [SSH](/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/)(22번) 원격접속 제어 데이터를 일반적인 웹페이지 HTML 소스코드인 척 <strong><a href="/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/">HTTP</a> 껍데기로 한 겹 포장(Encapsulation)</strong>합니다.
- [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)은 겉면에 '목적지 80번 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 패킷'이라고 적혀 있으니 "아, 평범한 웹서핑이네" 하고 통과시켜 줍니다. 집 밖의 해커 서버는 이 껍데기를 벗기고 안의 [SSH](/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) 데이터를 실행하여 사내 서버를 완벽히 통제합니다.
- <strong><a href="/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/">DNS</a> 우회</strong>: [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 요청(TXT 레코드 등) 안에 악성코드의 짧은 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 숨겨서 밖으로 빼내는 방식도 널리 쓰입니다. (DNS는 인터넷의 필수망이라 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)이 차단할 수가 없습니다.)

### 2. [VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) ([IPsec](/studynote/01_computer_architecture/15_advanced_topics/589_ipsec_offload/), [OpenVPN](/studynote/09_security/03_network_security/284_openvpn/)) 악용
- 직원이 사내망에서 불법 토렌트 사이트에 들어가려 합니다. 회사의 [차세대 방화벽](/studynote/09_security/05_web_app_security/216_ngfw_next_generation_firewall_dpi/)([NGFW](/studynote/03_network/13_network_security_basics/698_ngfw_next_generation_firewall/))이 패킷을 뜯어보고 차단합니다.
- 직원이 외부의 [VPN](/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) 서버로 <strong>강력한 암호화 터널(<a href="/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/">AES</a>)</strong>을 하나 뚫습니다. [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)은 직원이 외부와 뭔가 통신하는 것은 알지만, 데이터가 100% 암호화되어 있으므로 안에 토렌트가 들었는지 회사 기밀 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)([DLP](/studynote/01_computer_architecture/10_parallel_processing_architecture/386_dlp/) 회피)이 들었는지 뜯어보지 못하고 까막눈이 되어 통과시켜 줍니다.

```text
[포트 스캐닝 도구 작동 메커니즘 (NMAP…]
    |
    v
[방화벽 우회기법]
    |
    +---> [비인가 AP]
```

- **📢 섹션 요약 비유**: [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 우회기법의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

- **개념**: 앞서 715번에서 배운 [단편화](/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/)(조각내기)를 악용합니다. 해커가 보낼 악성 텍스트가 `ATTACK`이라면, 이걸 `AT`, `TA`, `CK` 로 잘게 쪼개서 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)으로 던집니다.
- **동작**: 구형 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)(상태 추적 기능이 약한)이나 멍청한 NIDS는 조각난 첫 번째 패킷 `AT`만 보고 "정상 패킷이네?" 하고 통과시키고, 뒤따라오는 조각들도 의미를 파악하지 못한 채 낱개로 무사통과 시켜 버립니다.
- 타겟 서버(피해자) 내부로 들어간 뒤에 이 조각들이 조립되어 거대한 악성코드 `ATTACK`으로 완성되어 폭발합니다.

[방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 우회기법을 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [포트 스캐닝](/studynote/02_operating_system/10_security/600_port_scanning/) 도구 작동 메커니즘 (NMAP…가 기반 조건을 만든다면, [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 우회기법은 그 위에서 핵심 메커니즘을 구현하고, 비인가 AP는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 탐지 가능성과 복구성에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [포트 스캐닝](/studynote/02_operating_system/10_security/600_port_scanning/) 도구 작동 메커니즘 (NMAP…의 기반 정리 | [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 우회기법의 핵심 동작 | 비인가 AP의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 탐지 가능성 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 우회기법은 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

- <strong><a href="/studynote/09_security/05_web_app_security/216_ngfw_next_generation_firewall_dpi/">차세대 방화벽</a>(<a href="/studynote/03_network/13_network_security_basics/698_ngfw_next_generation_firewall/">NGFW</a>)</strong>이나 고급 <strong><a href="/studynote/03_network/13_network_security_basics/696_waf_web_application_firewall/">WAF</a></strong>:
  - 아무리 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 껍데기를 씌워도, 패킷을 심층 분석(Deep Packet Inspection)하여 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 본문 안에 이상한 [SSH](/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 규격이 섞여 있으면 "[터널링](/studynote/03_network/07_network_layer_routing/377_tunneling_mechanism_overview/) 꼼수 쓰네!" 라며 찢어버립니다.
  - 조각난 패킷이 들어오면 입구에서 통과시키지 않고, <strong><a href="/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/">방화벽</a> 자신의 배때기 안에서 직접 100% 다 조립해 본 뒤(Reassembly)</strong> 악성코드인지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하고 나서야 내부로 들여보내는 철통 방어를 씁니다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: [터널링](/studynote/03_network/07_network_layer_routing/377_tunneling_mechanism_overview/) 우회는 감옥(사내망)에서 죄수(직원)가 밖으로 몰래 '탈옥 계획서'를 빼내는 수법입니다. 교도관([방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/))은 무조건 편지([HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/))만 내보내 줍니다. 죄수는 탈옥 계획서를 깨알같이 적은 뒤, 그 종이 겉면을 가족에게 쓰는 '안부 편지([HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 껍데기)' 봉투로 감싸서 제출합니다. 교도관은 겉봉투만 보고 무사통과시킵니다. [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 패킷 우회는 탈옥 계획서를 글자 하나씩 잘라서 100일 동안 매일 한 장씩 보내는 짓입니다. 멍청한 교도관은 글자 하나만 보고는 의미를 몰라 그냥 넘겨주고, 바깥의 공범이 이 조각들을 100일 치 모아 조립하면 완벽한 지도가 완성되는 원리입니다.

---

## Ⅴ. 기대효과 및 결론

[방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 우회기법은 [네트워크 보안](/studynote/03_network/20_performance_evaluation_advanced/1117_network_security_zero_trust_policy/) 위협과 대응을 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 탐지 가능성 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 비인가 [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/), 예측형 위협 대응, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 예측형 위협 대응 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 우회기법은 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [포트 스캐닝](/studynote/02_operating_system/10_security/600_port_scanning/) 도구 작동 메커니즘 (NMAP… | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 공격 표면 (Attack Surface) | 위협이 침투할 수 있는 노출 지점을 뜻한다. |
| [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) ([Anomaly Detection](/studynote/16_bigdata/05_analysis/111_anomaly_detection/)) | 정상 패턴과 다른 징후를 찾아낸다. |
| 비인가 [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: 포트 스캐닝 도구 작동 메커니즘 (NMAP…]
    |
    v
[현재 개념: 방화벽 우회기법]
    |
    +---> [확장 A: 비인가 AP]
    +---> [확장 B: 예측형 위협 대응]
```

[방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 우회기법는 [포트 스캐닝](/studynote/02_operating_system/10_security/600_port_scanning/) 도구 작동 메커니즘 (NMAP…에서 출발해 현재 메커니즘을 정교화하고, 이후 비인가 AP와 예측형 위협 대응 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 나쁜 친구가 놀이터 규칙을 깨뜨리면 바로 알아차리고 막아야 해요.
2. 이 개념은 어떤 장난이 위험한지 미리 알고, 문제가 생기면 어떻게 다시 정리할지도 알려줘요.
3. 그래서 놀이터를 더 안전하게 지킬 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 855 / 1120

<- **이전**: [733. 포트 스캐닝 도구 작동 메커니즘 (NMAP 스텔스 스캔](/studynote/03_network/14_network_security_threats/733_port_scanning_nmap_stealth_syn_scan/)
**다음**: [735. 비인가 AP (Rogue AP 무선망 트래픽 위조 가로채기 이블트윈 공격 / WIPS 방어 적용망)](/studynote/03_network/14_network_security_threats/735_rogue_ap_evil_twin_wips_defense/) ->

---
