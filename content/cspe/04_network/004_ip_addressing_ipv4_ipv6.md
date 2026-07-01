---
title: "IP 주소 체계 - IPv4·IPv6 (IP Addressing IPv4 IPv6)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 4
---

# 📖 【암기용】 개념 완전 이해

> 목적: IP 주소 체계를 논리 주소와 라우팅 관점에서 이해하게 만든다. 시험 답안 양식이 아니라, IPv4와 IPv6의 차이를 직관적으로 설명한다.

## 한눈에
- **개요**: IP 주소는 네트워크에서 호스트와 라우팅 위치를 식별하는 논리 주소이다.
- **왜 필요한가**: LAN 안의 MAC 주소만으로는 전 세계 목적지를 찾을 수 없으므로 네트워크 계층 주소와 prefix 기반 경로 선택이 필요하다.
- **핵심 직관**: IP 주소는 건물 주소처럼 지역(prefix)과 개별 위치(host)를 함께 표현한다.

## 깊이 이해
- **배경·문제의식**: IPv4는 32bit 주소로 약 43억 개를 표현하지만 인터넷 단말, 모바일, IoT 증가로 고갈 문제가 발생했다. IPv6는 128bit 주소와 자동 구성, 확장 헤더를 제공한다.
- **작동 원리**: IPv4는 dotted decimal과 CIDR prefix를 사용하고, IPv6는 16bit 단위 8그룹의 hexadecimal 표기를 사용한다. 라우터는 목적지 주소의 longest prefix match로 다음 홉을 선택한다.
- **비유**: 우편번호가 지역을 좁히고 상세 주소가 집을 찾게 하듯, prefix는 네트워크를 찾고 host part는 노드를 찾게 한다.
- **구체 예시**: `192.168.10.25/24`는 네트워크 `192.168.10.0`, 호스트 범위 `192.168.10.1~254`를 의미한다. `2001:db8::1/64`는 IPv6 문서용 prefix RFC 3849 예시이다.
- **흔한 오해·주의점**: IPv6는 주소 길이만 늘린 기술이 아니다. ARP 대신 NDP를 쓰고, broadcast 대신 multicast 기반 동작을 사용한다.

## 연결 개념
- CIDR: prefix length 기반 주소 집계
- 라우팅: longest prefix match로 경로 선택
- IPv6 전환: dual stack, tunneling, translation

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 준수한다.
> 핵심: IP 주소 문제는 주소 길이, 표기법, prefix, 라우팅, IPv4/IPv6 차이를 수치로 제시해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IP 주소 체계는 네트워크 계층에서 호스트 위치를 식별하고 라우팅 경로 선택에 사용하는 논리 주소 구조이다.
> 2. **가치**: IPv4 32bit와 IPv6 128bit 주소를 통해 LAN 범위를 넘어 전역 경로 선택과 주소 집계를 가능하게 한다.
> 3. **판단 포인트**: IPv4 사설주소·NAT·CIDR 한계와 IPv6 prefix·NDP·자동 구성 차이를 함께 써야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| IP 주소의 논리 주소 역할 확인 | network part, host part, prefix length | IP와 MAC 주소 역할 혼동 |
| IPv4와 IPv6 차이 이해 확인 | 32bit vs 128bit, broadcast vs multicast, ARP vs NDP | 주소 길이 차이만 서술 |
| 라우팅·주소 설계 판단 확인 | CIDR, longest prefix match, 주소 집계 | classful 주소 체계만 설명 |

> 요약: IP 주소 답안은 수치 기반 주소 구조와 라우팅 기준을 함께 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

IP 주소는 네트워크 계층에서 노드의 논리 위치를 나타내는 주소이다. 인터넷은 여러 네트워크의 집합이므로 MAC 주소만으로 전역 목적지를 찾을 수 없다. IPv4·IPv6 주소와 prefix 설계는 라우팅, 보안 정책, 주소 관리의 기준이다.

---

## Ⅱ. 구조 및 구성요소

```text
IP Address
-> Prefix / Network Part
-> Host / Interface Identifier
-> Routing Table Longest Prefix Match
-> Next Hop -> Destination Network
```

| 구성요소 | IPv4 | IPv6 |
|:---|:---|:---|
| 주소 길이 | 32bit, 약 4.3 billion | 128bit, 2^128 |
| 표기 | dotted decimal, 예: 192.0.2.1 | hexadecimal, 예: 2001:db8::1 |
| 주소 분리 | network/host, CIDR prefix | prefix/interface ID, 보통 /64 LAN |
| 보조 프로토콜 | ARP, ICMPv4 | NDP, ICMPv6 |

> 요약: IPv4와 IPv6는 모두 prefix 기반 논리 주소이나 길이, 표기, 이웃 탐색, 브로드캐스트 처리 방식이 다르다.

---

## Ⅲ. 동작원리 및 흐름도

```text
송신 데이터
-> 목적지 IP 확인
-> routing table longest prefix match
-> next-hop IP 결정
-> ARP 또는 NDP로 L2 주소 확인
-> frame 전송
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 목적지 IP와 prefix 확인 | IPv4 /0~32, IPv6 /0~128 |
| 2 | 라우팅 테이블에서 longest prefix match 수행 | route entry, default route |
| 3 | next-hop 또는 directly connected 판단 | gateway IP, interface |
| 4 | L2 주소 해석 수행 | ARP cache, IPv6 neighbor cache |
| 5 | MTU와 TTL/Hop Limit 적용 후 송신 | MTU 1500, TTL/Hop Limit 감소 |

> 요약: IP 패킷 전달은 prefix 기반 경로 선택 후 ARP/NDP로 링크 주소를 구해 다음 홉으로 보내는 과정이다.

---

## Ⅳ. 특징

| 구분 | IPv4 | IPv6 | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 주소 공간 | 32bit | 128bit | IPv6 주소 공간 2^128 |
| 주소 관리 | 사설주소+NAT 광범위 | 전역 주소와 prefix delegation | RFC 1918, RFC 4291 |
| 이웃 탐색 | ARP broadcast | NDP multicast | ICMPv6 필수 |
| 헤더 | 기본 20byte 가변 옵션 | 기본 40byte, 확장 헤더 | IPv6는 헤더 checksum 필드 제거 |

> 요약: IPv6는 주소 공간뿐 아니라 NDP, multicast, 확장 헤더, 자동 구성까지 포함한 네트워크 계층 변화이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | IPv4 유지 | IPv6 도입 | 선택 기준 |
|:---|:---|:---|:---|
| 주소 확보 | NAT, CGNAT 의존 | /48, /56, /64 prefix 설계 | 신규 대규모 단말은 IPv6 우선 |
| 운영 | 기존 장비·정책 유지 | RA, NDP, ICMPv6 운영 필요 | 방화벽·모니터링 IPv6 지원 확인 |
| 전환 | 단일 스택 단순성 | dual stack, tunneling, translation | 외부 연동 요구와 SLA 기준 판단 |

> 요약: IPv6 도입은 주소 공간만이 아니라 방화벽, DNS, 관측성, 운영 절차의 동시 전환이 필요하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 주소 설계 오류 | prefix 과소 할당 | site /48, subnet /64 기준 설계 | prefix utilization |
| IPv6 보안 누락 | IPv4 ACL만 적용 | IPv6 ACL, RA Guard, NDP inspection | IPv6 blocked/allowed log |
| PMTU 장애 | ICMPv6 차단 | ICMPv6 Packet Too Big 허용 | path MTU discovery 성공률 |

> 요약: IPv6 운영 리스크는 prefix 설계, IPv6 보안 정책, ICMPv6 처리 누락에서 발생한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 주소 정확성 | subnet prefix 중복 0건 | IPAM, route table audit |
| 라우팅 | default route, longest match 정상 | traceroute, BGP/OSPF table |
| 전송 품질 | packet loss 0.1% 이하, PMTU 실패 0건 | ping, tracepath, flow log |

> 요약: IP 주소 체계는 IPAM, 라우팅 테이블, PMTU·손실 지표로 운영 품질을 확인한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 주소 설계: IPv4는 RFC 1918 대역과 CIDR 집계를 적용하고, IPv6는 site /48, LAN /64 기준으로 IPAM 등록
2. 보안 정책: IPv4 ACL과 IPv6 ACL을 동시 관리하고 RA Guard, NDP inspection, ICMPv6 허용 정책 반영
3. 운영 점검: DNS A/AAAA, route table, ARP/NDP cache, MTU 1500/9000 일치 여부를 배포 전 점검표에 포함

**결론 (2줄):**
- 기술사 판단: 단기 운영은 IPv4+NAT 현실을 인정하되 신규 서비스와 공공·글로벌 연동은 IPv6 prefix 기반 설계를 선택함
- 향후 방향: dual stack 과도기를 지나 IPv6-only와 NAT64/DNS64 기반 운영 지표가 확대됨

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "IP 주소 체계를 설명하시오" | prefix 기반 라우팅과 ARP/NDP 흐름 | IPv4·IPv6 구조 차이 |
| 요구사항 명시형 | "IPv4와 IPv6를 비교하시오", "주소 설계 방안을 제시하시오" | longest prefix match와 주소 할당 절차 | 전환 기준, 리스크, 점검 지표 |

> 요약: 설명형은 주소 구조와 라우팅 원리를, 비교·설계형은 IPv4/IPv6 차이와 prefix 설계 기준을 강조한다.
