+++
title = "308. Static NAT (1:1) / Dynamic NAT (M:N) / PAT (Port Address Translation = NAPT, 1:N)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Static [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) / Dynamic [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/)…는 네트워크 계층과 IP에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: Static [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) / Dynamic [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/)…를 이해하면 주소 효율과 도달성 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) 테이블을 구성하는 3가지 세부 방식이다.
  - <strong>Static <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/">NAT</a></strong>: 1 대 1 정적 맵핑
  - <strong>Dynamic <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/">NAT</a></strong>: 다 대 다(M:N) 동적 맵핑 (먼저 온 놈이 쓴다)
  - <strong>PAT (NAPT - Network Address <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">Port</a> Translation)</strong>: 1 대 다(1:N) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 변환
- **필요성**: 상황마다 필요한 변환 방식이 다르다. 사내 웹서버를 돌린다면 누군가 외부에서 `211.x.x.5`를 쳤을 때 무조건 그 서버(사설 IP `192.168.0.50`)로 꽂아줘야 하니 Static이 필요하다. 반면 직원 100명이 네이버 웹서핑만 할 거라면, 공인 IP 100개를 사는 건 미친 짓이므로 공인 IP 딱 1개에 [포트 번호](/knowledge-base/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/)([Port](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)) 100개를 붙여서 쪼개 쓰는 PAT가 압도적으로 경제적이다.

- **💡 비유**: 
  - <strong>Static <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/">NAT</a></strong>: 사장님 전용 **"고정 주차 구역(1:1)"**. 사장님 차 번호와 주차 칸 번호가 영구 매칭되어 있습니다.
  - <strong>Dynamic <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/">NAT</a></strong>: 회사 공용 주차장 **"자율 주차(M:N)"**. 주차 칸(공인 IP)이 5개면, 출근 빨리한 직원 5명만 주차하고, 6번째 직원은 퇴근차가 나올 때까지 빙빙 돌아야 합니다.
  - **PAT**: 놀이공원의 **"거대한 공용 사물함(1:N)"**. 사물함(공인 IP)은 1개지만, 안에 열쇠 번호([포트 번호](/knowledge-base/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/))가 수만 개 달려 있어서, 열쇠 번호만 다르면 수천 명이 동시에 한 사물함을 나누어 쓸 수 있습니다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">NAT</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Static NAT / Dynamic NAT…</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">헤어핀 NAT</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: ** 우리가 집에서 쓰는 'ipTime 공유기'는 사실 공유기가 아니라 **"PAT([포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 주소 변환기)"**라고 부르는 것이 기술적으로 가장 정확한 명칭입니다. IP 하나를 [포트 번호](/knowledge-base/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/)로 썰어서 가족 모두에게 나눠주는 기계이기 때문입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. Static [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) (1:1 매핑)
- 관리자가 라우터에 `ip nat inside source static 192.168.0.100 211.1.1.100`이라고 박아버린다.
- 그러면 외부 해커가 `211.1.1.100`으로 핑을 때리면, 라우터는 묻지도 따지지도 않고 무조건 내부의 `192.168.0.100` 서버로 전달해 버린다.
- <strong><a href="/knowledge-base/studynote/03_network/14_network_security_threats/736_port_forwarding_jump_station_bastion_host/">포트 포워딩</a>(<a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">Port</a> Forwarding)</strong>: Static NAT의 변형으로, "211.1.1.100의 <strong>80번 <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">포트</a></strong>로 오면 192.168.0.100 서버로 주고, <strong>21번 <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">포트</a></strong>로 오면 192.168.0.101 서버로 줘!"라고 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 단위로 정밀하게 꺾어버리는 기술이다. 홈 네트워크에서 CCTV나 [NAS](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/492_nas_network_attached_storage/) 서버를 외부에서 접속할 때 필수로 쓴다.

### 2. Dynamic [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) (M:N 매핑)
- 회사가 공인 IP를 10개(Pool) 샀고, 직원이 50명이다.
- 직원이 웹서핑을 시도할 때마다 라우터가 남는 공인 IP 하나를 빌려준다.
- 만약 직원 10명이 동시에 다운로드를 걸어 공인 IP 10개를 꽉 채웠다면? <strong>11번째 직원은 공인 IP가 반납될 때까지 인터넷 접속이 완전히 멈춰버리는 끔찍한 현상</strong>이 발생한다. IP 절약 효과가 거의 없어서 요즘엔 안 쓴다.

### 3. PAT ([Port](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) Address Translation / NAPT) - 인터넷의 구원자
[TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/[UDP](/knowledge-base/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) 헤더에 있는 '출발지 [포트 번호](/knowledge-base/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/)(16비트)'는 약 6만 개다. 라우터는 이걸 악용(응용)한다.

- **나갈 때**:
  - 내 폰(`192.168.0.2:3000`)이 구글로 나간다. 공유기는 이걸 `공유기IP:5000`으로 바꾼다.
  - 내 [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)(`192.168.0.3:3000`)도 구글로 나간다. 공유기는 이걸 `공유기IP:5001`로 바꾼다.
  - 공유기 [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) 장부: "5000번 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)는 내 폰꺼, 5001번 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)는 내 PC꺼"라고 적어둔다.
- **들어올 때**:
  - 구글이 `공유기IP:5000`으로 답장을 쏜다.
  - 공유기는 장부를 뒤져보고 "아 5000번은 아까 내 폰(`192.168.0.2`)이 보낸 거네!" 하고 정확하게 내 폰으로만 패킷을 돌려준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">PAT (NAPT)의 1:N 포트 변환 마법 도식</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">집안 식구들</div><div class="kb-diagram-node">공유기 (211.x.x.x)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(NAT 장부)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">211.x.x.x : 포트 10001</div><div class="kb-diagram-connector">▶</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">211.x.x.x : 포트 10002</div><div class="kb-diagram-connector">▶</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">211.x.x.x : 포트 10003</div><div class="kb-diagram-connector">▶</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">▶ 결과: 공유기 밖(인터넷)에서 보면 그냥 211.x.x.x 라는 놈 혼자서</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">포트 번호만 바꿔가며 수만 개의 인터넷 창을 띄운 것처럼 보임!</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: ** PAT는 우체국 사서함과 같습니다. 우체국 건물 주소(공인 IP)는 단 1개지만, 건물 벽면에 뚫린 수만 개의 **"작은 사서함 칸([포트 번호](/knowledge-base/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/))"** 덕분에 수만 명의 사람이 절대 우편물을 헷갈리지 않고 안전하게 받아볼 수 있습니다.

---

## Ⅲ. 비교 및 연결

Static [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) / Dynamic [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/)…를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. NAT가 기반 조건을 만든다면, Static [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) / Dynamic [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/)…는 그 위에서 핵심 메커니즘을 구현하고, 헤어핀 NAT는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 주소 효율과 도달성에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | NAT의 기반 정리 | Static [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) / Dynamic [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/)…의 핵심 동작 | 헤어핀 NAT의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 주소 효율 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: Static [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) / Dynamic [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/)…는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 Static [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) / Dynamic [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/)…를 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) 수준의 기본 대책으로 충분한지, 아니면 Static [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) / Dynamic [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/)…가 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 헤어핀 NAT와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 주소 효율 부족인지, 도달성 악화인지 먼저 분리한다.
2. Static [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) / Dynamic [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/)…가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 헤어핀 NAT와의 연계 방식을 함께 검증한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- Static [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) / Dynamic [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/)…의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- NAT와의 경계를 정리하지 않아 중복 투자나 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: Static [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) / Dynamic [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/)…를 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

Static [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) / Dynamic [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/)…는 네트워크 계층과 IP를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 주소 효율 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 헤어핀 [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/), 대규모 주소 자동화, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 대규모 주소 자동화 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: Static [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) / Dynamic [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/)…는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| IP 주소 (Internet [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) Address) | 종단 위치를 논리적으로 식별한다. |
| 서브넷 (Subnet) | 주소 공간을 쪼개 관리 단위를 만든다. |
| 헤어핀 [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">선행 개념: NAT</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">현재 개념: Static NAT / Dynamic NAT…</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">확장 A: 헤어핀 NAT</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">확장 B: 대규모 주소 자동화</div></div>
</div>
</div>



Static [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/) / Dynamic [NAT](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/)…는 NAT에서 출발해 현재 메커니즘을 정교화하고, 이후 헤어핀 NAT와 대규모 주소 자동화 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 택배를 보내려면 집 주소가 정확해야 길을 잃지 않아요.
2. 이 개념은 인터넷 세상에서 주소를 정하고 다음 길을 찾는 지도와 같아요.
3. 그래서 멀리 있는 친구 컴퓨터까지도 편지가 도착할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 429 / 1120

← **이전**: [307. NAT (Network Address Translation)](/knowledge-base/studynote/03_network/06_network_layer_ip/307_nat_network_address_translation_router_principles/)
**다음**: [309. 헤어핀 NAT (Hairpin NAT, NAT Loopback)](/knowledge-base/studynote/03_network/06_network_layer_ip/309_hairpin_nat_loopback/) →

---
