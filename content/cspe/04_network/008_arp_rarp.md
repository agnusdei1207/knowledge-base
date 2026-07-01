---
title: "ARP·RARP (ARP RARP)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 8
---

# 📖 【암기용】 개념 완전 이해

> 목적: ARP와 RARP를 IP 주소와 MAC 주소 매핑 관점에서 이해하게 만든다. 시험 답안 양식이 아니라, LAN 내부 전달 과정을 설명한다.

## 한눈에
- **개요**: ARP는 IP 주소로 MAC 주소를 찾고, RARP는 MAC 주소로 IP 주소를 얻는 프로토콜이다.
- **왜 필요한가**: IP 패킷을 같은 LAN에서 전달하려면 Ethernet frame의 destination MAC이 필요하다.
- **핵심 직관**: 주소록에서 이름으로 전화번호를 찾는 과정이 ARP이고, 전화기 고유번호로 배정 주소를 묻는 과정이 RARP이다.

## 깊이 이해
- **배경·문제의식**: IP 주소는 L3 라우팅에 쓰이고 MAC 주소는 L2 프레임 전달에 쓰인다. 두 주소 체계를 연결하지 못하면 같은 LAN에서도 프레임을 만들 수 없다.
- **작동 원리**: 송신자는 목적지 또는 기본 게이트웨이 IP에 대한 ARP Request를 broadcast로 보내고, 해당 IP를 가진 장비가 ARP Reply로 MAC 주소를 알려준다. 결과는 ARP cache에 일정 시간 저장된다.
- **비유**: 사무실 전체에 "이 IP를 쓰는 사람 누구인가"라고 물으면 대상자가 자기 자리 번호인 MAC을 답하는 방식이다.
- **구체 예시**: `192.168.1.10`이 게이트웨이 `192.168.1.1`로 패킷을 보내려면 먼저 `192.168.1.1`의 MAC 주소를 ARP로 확인한다.
- **흔한 오해·주의점**: 원격 네트워크 목적지의 MAC을 직접 찾지 않는다. 다른 서브넷은 기본 게이트웨이 MAC을 ARP로 찾는다.

## 연결 개념
- MAC 주소: ARP가 찾는 L2 주소
- DHCP: RARP를 대체한 동적 IP 설정 방식
- ARP spoofing: ARP의 인증 부재를 악용한 공격

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 준수한다.
> 핵심: ARP는 IP-MAC 해석, RARP는 과거 MAC-IP 해석이며 동작 흐름과 보안 취약점을 함께 제시한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ARP는 IPv4 LAN에서 IP 주소에 대응하는 MAC 주소를 찾는 주소 해석 프로토콜이고, RARP는 MAC 주소 기반 IP 획득 프로토콜이다.
> 2. **가치**: L3 IP 패킷을 L2 Ethernet 프레임으로 캡슐화할 수 있게 하여 같은 브로드캐스트 도메인 내부 전달을 가능하게 한다.
> 3. **판단 포인트**: ARP broadcast, ARP cache, gateway MAC 해석, spoofing 대응, RARP의 DHCP 대체 관계를 써야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| L2/L3 주소 매핑 이해 확인 | ARP Request/Reply, ARP cache | 원격 목적지 MAC을 직접 찾는다고 설명 |
| RARP와 DHCP 관계 확인 | RARP는 과거 diskless host IP 획득 | RARP를 현재 일반 IP 할당 방식으로 과장 |
| 보안 취약점 인식 확인 | ARP spoofing, DAI, static ARP | ARP 인증 부재 누락 |

> 요약: ARP·RARP 답안은 주소 해석 흐름과 인증 부재에 따른 보안 통제를 함께 다루어야 한다.

---

## Ⅰ. 개요 및 필요성

ARP·RARP는 L2 MAC 주소와 L3 IP 주소를 상호 연결하는 주소 해석 프로토콜이다. IP 패킷을 Ethernet 프레임에 담으려면 destination MAC이 필요하다. ARP는 현재 IPv4 LAN의 필수 기능이고, RARP는 DHCP로 대체된 과거 부트스트랩 방식이다.

---

## Ⅱ. 구조 및 구성요소

```text
IPv4 Host
-> ARP Cache 확인
-> ARP Request broadcast
-> ARP Reply unicast
-> IP packet inside Ethernet frame
-> Switch forwarding
```

| 구성요소 | 역할 | 대표 값·특징 |
|:---|:---|:---|
| ARP Request | 대상 IP의 MAC 질의 | broadcast FF:FF:FF:FF:FF:FF |
| ARP Reply | 대상 MAC 응답 | unicast reply |
| ARP Cache | IP-MAC 매핑 임시 저장 | aging time OS별 상이 |
| RARP Server | MAC 기반 IP 응답 | DHCP 이전 방식 |
| 보안 통제 | 위조 응답 차단 | Dynamic ARP Inspection |

> 요약: ARP는 질의·응답·캐시로 구성되며, broadcast 질의와 인증 부재 때문에 보안 통제가 필요하다.

---

## Ⅲ. 동작원리 및 흐름도

```text
송신 host가 목적지 IP 확인
-> 같은 subnet이면 목적지 IP ARP 조회
-> 다른 subnet이면 gateway IP ARP 조회
-> ARP Request broadcast
-> ARP Reply 수신 후 cache 저장
-> Ethernet frame 전송
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | subnet mask로 직접 전달 여부 판단 | local subnet 또는 gateway |
| 2 | ARP cache 조회 | stale, reachable entry |
| 3 | ARP Request broadcast 송신 | opcode 1, target IP |
| 4 | ARP Reply 수신 | opcode 2, sender MAC |
| 5 | 프레임 생성 후 전달 | EtherType 0x0806/0x0800 |

> 요약: ARP는 목적지가 로컬이면 대상 MAC, 원격이면 게이트웨이 MAC을 조회해 Ethernet frame을 만든다.

---

## Ⅳ. 특징

| 구분 | ARP | RARP | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 방향 | IP -> MAC | MAC -> IP | RFC 826, RFC 903 |
| 사용 환경 | IPv4 Ethernet LAN | 과거 diskless boot | DHCP가 대체 |
| 전송 방식 | request broadcast, reply unicast | server 응답 필요 | EtherType 0x0806 |
| 보안 | 인증 부재 | 서버 신뢰 필요 | DAI, static ARP |

> 요약: ARP는 현재 IPv4 LAN의 주소 해석 핵심이고 RARP는 DHCP 등장 후 일반 운영에서 사용 빈도가 낮다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | ARP | DHCP | 선택 기준 |
|:---|:---|:---|:---|
| 목적 | IP에 대한 MAC 해석 | IP 주소·옵션 할당 | 통신 직전 L2 해석은 ARP |
| 계층 | L2/L3 경계 | 응용 계층 기반 UDP | 주소 설정은 DHCP |
| 보안 통제 | DAI, static ARP | DHCP snooping | 스위치 보안 기능 연동 |

> 요약: ARP는 주소 해석, DHCP는 주소 할당이므로 목적과 통제 방식이 다르다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| ARP spoofing | 인증 없는 ARP Reply | DAI, DHCP snooping binding | ARP inspection drop count |
| ARP storm | 대량 broadcast | storm control, subnet 분리 | broadcast pps |
| stale cache | MAC 변경 후 캐시 미갱신 | gratuitous ARP, cache flush | duplicate IP, failed ping |

> 요약: ARP 리스크는 위조, broadcast 증가, 캐시 불일치이며 스위치 보안과 캐시 관리로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| ARP 오류 | unresolved ARP 0건 | arp table, host log |
| 보안 이벤트 | DAI drop 이상 징후 탐지 | switch log, SIEM |
| broadcast | broadcast traffic 5% 이하 | switch telemetry |

> 요약: ARP 운영 품질은 unresolved entry, DAI drop, broadcast 비율로 확인한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 보안 설정: access switch에 DHCP snooping과 Dynamic ARP Inspection을 적용하고 trusted port를 uplink로 제한
2. 장애 대응: ping 실패 시 ARP cache, gateway MAC, VLAN, DAI drop log 순서로 원인 분리
3. 운영 관리: gateway 이중화 변경 시 gratuitous ARP 송신과 ARP cache aging 영향을 배포 절차에 포함

**결론 (2줄):**
- 기술사 판단: IPv4 LAN 장애와 보안 문제는 ARP cache·broadcast·DAI 지표를 우선 확인하고, IP 할당 문제는 DHCP로 분리함
- 향후 방향: IPv6 환경에서는 ARP 대신 ICMPv6 기반 NDP가 사용되므로 RA Guard와 NDP inspection 운영이 병행됨

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "ARP와 RARP를 설명하시오" | ARP Request/Reply와 cache 흐름 | ARP·RARP·DHCP 차이 |
| 요구사항 명시형 | "ARP spoofing 대응 방안을 제시하시오" | 공격·탐지·차단 흐름 | DAI, DHCP snooping, 지표 점검 |

> 요약: 설명형은 주소 해석 원리를, 보안형은 ARP spoofing 통제와 스위치 지표를 중심으로 전환한다.
