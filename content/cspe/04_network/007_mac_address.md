---
title: "MAC 주소 구조 (MAC Address)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 7
---

# 📖 【암기용】 개념 완전 이해

> 목적: MAC 주소를 LAN 내부 프레임 전달 주소로 이해하게 만든다. 시험 답안 양식이 아니라, IP 주소와 MAC 주소의 차이를 설명한다.

## 한눈에
- **개요**: MAC 주소는 데이터링크 계층에서 네트워크 인터페이스를 식별하는 48bit 주소이다.
- **왜 필요한가**: 같은 LAN 안에서 이더넷 프레임을 어느 NIC로 전달할지 결정하기 위해 필요하다.
- **핵심 직관**: IP 주소가 건물 주소라면 MAC 주소는 같은 건물 안의 사무실 출입증 번호와 같다.

## 깊이 이해
- **배경·문제의식**: IP 주소는 라우팅을 위한 논리 주소라서 LAN 내부 실제 프레임 전달에는 링크 계층 주소가 필요하다. Ethernet은 NIC 단위 식별자로 MAC 주소를 사용한다.
- **작동 원리**: 일반 MAC 주소는 48bit이며 앞 24bit는 제조사 식별자 OUI, 뒤 24bit는 제조사가 부여한 NIC 식별자이다. 스위치는 source MAC을 학습해 MAC table을 만들고 destination MAC 기준으로 포트를 선택한다.
- **비유**: 우편물이 건물(IP)에 도착한 뒤, 건물 내부 우편함(MAC)으로 최종 배달되는 구조와 같다.
- **구체 예시**: `00:1A:2B:3C:4D:5E`에서 `00:1A:2B`는 OUI, `3C:4D:5E`는 장치 식별 영역이다.
- **흔한 오해·주의점**: MAC 주소는 전 세계 라우팅 주소가 아니다. 라우터를 지나면 다음 링크의 source/destination MAC으로 바뀐다.

## 연결 개념
- Ethernet frame: MAC 주소가 포함되는 L2 프레임
- ARP: IP 주소를 MAC 주소로 해석하는 프로토콜
- Switch MAC table: source MAC 학습 기반 프레임 전달

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 준수한다.
> 핵심: MAC 주소는 48bit 구조, OUI, unicast/multicast/broadcast, 스위치 학습, IP와의 차이를 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: MAC 주소는 IEEE 802 계열 LAN에서 NIC를 식별하고 Ethernet 프레임 전달에 사용하는 데이터링크 계층 주소이다.
> 2. **가치**: 같은 브로드캐스트 도메인 내부에서 스위치가 프레임을 포트 단위로 전달하게 해 LAN 통신을 구성한다.
> 3. **판단 포인트**: IP는 L3 라우팅 주소, MAC은 L2 링크 주소이며 라우터 경계에서 MAC 헤더가 재작성됨을 명확히 써야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| L2 주소 구조 이해 확인 | 48bit, OUI 24bit, device ID 24bit | MAC을 IP처럼 라우팅 주소로 설명 |
| Ethernet 전달 원리 확인 | source MAC 학습, destination MAC forwarding | 스위치와 라우터 역할 혼동 |
| 보안·운영 리스크 인식 확인 | MAC spoofing, flooding, port security | MAC 주소가 변경 불가하다고 단정 |

> 요약: MAC 주소 답안은 주소 구조와 스위치 학습·보안 통제를 함께 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

- 정의: 데이터링크 계층에서 NIC를 식별하는 48bit 주소
- 배경: IP는 라우팅 주소만 제공하므로 같은 LAN 내부의 실제 프레임 전달에는 별도 링크 주소가 필요
- 필요성: MAC 주소가 Ethernet 스위칭, ARP 주소 해석, 포트 보안(port security)의 기반이 됨

---

## Ⅱ. 구조 및 구성요소

```text
MAC Address 48bit
-> OUI 24bit: vendor identifier
-> NIC Specific 24bit: device identifier
-> I/G bit: unicast / multicast
-> U/L bit: universal / local
-> Ethernet Frame Addressing
```

| 구성요소 | 역할 | 대표 예시 |
|:---|:---|:---|
| OUI | 제조사 식별자 | IEEE 등록 24bit |
| NIC 식별자 | 제조사 내부 장치 식별 | 하위 24bit |
| I/G bit | unicast와 group address 구분 | multicast bit |
| U/L bit | globally unique와 locally administered 구분 | 가상 NIC, container MAC |
| Broadcast | LAN 전체 대상 프레임 | FF:FF:FF:FF:FF:FF |

> 요약: MAC 주소는 48bit 구조 안에 제조사, 장치, 주소 유형 정보를 포함하고 Ethernet 프레임의 L2 전달 기준이 된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Host A IP packet 생성
-> ARP로 next-hop MAC 확인
-> Ethernet frame에 source/destination MAC 기록
-> Switch가 source MAC 학습
-> destination MAC 기준 포트 전달 또는 flooding
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 목적지 IP가 같은 LAN인지 판단 | subnet mask, gateway |
| 2 | ARP cache에서 next-hop MAC 조회 | ARP entry age |
| 3 | Ethernet frame 생성 | destination/source MAC, EtherType |
| 4 | 스위치 MAC table 학습·조회 | MAC aging 300초 예시 |
| 5 | 해당 포트 전달 또는 unknown unicast flooding | unknown unicast rate |

> 요약: MAC 주소는 ARP로 해석되고 스위치 MAC table을 통해 같은 LAN 내부 프레임 전달에 사용된다.

---

## Ⅳ. 특징

| 구분 | MAC 주소 | IP 주소 | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 계층 | L2 데이터링크 | L3 네트워크 | IEEE 802, IETF IP |
| 길이 | 일반 Ethernet 48bit | IPv4 32bit, IPv6 128bit | EUI-48 |
| 범위 | 동일 링크·브로드캐스트 도메인 | 라우팅 가능한 논리 네트워크 | router hop마다 MAC 변경 |
| 관리 | OUI+장치 ID, 로컬 변경 가능 | IPAM, DHCP, RA | ARP/NDP로 매핑 |

> 요약: MAC은 링크 내부 전달 주소이고 IP는 네트워크 간 라우팅 주소이므로 적용 계층과 변경 범위가 다르다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 정적 MAC 관리 | 동적 MAC 학습 | 선택 기준 |
|:---|:---|:---|:---|
| 운영 | 수동 등록 | 스위치 source MAC 자동 학습 | 일반 LAN은 동적 학습 |
| 보안 | 허용 MAC 고정 | spoofing 가능 | 중요 포트는 port security 적용 |
| 확장 | 변경 작업 증가 | MAC table capacity 필요 | 가상화 환경은 table size 확인 |

> 요약: MAC 운영은 동적 학습을 기본으로 하되 서버·관리 포트는 port security와 MAC limit으로 통제한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| MAC spoofing | 소프트웨어로 source MAC 변경 | port security, 802.1X | violation count |
| MAC flooding | 대량 위조 MAC 학습 유도 | storm control, MAC limit | MAC table utilization |
| 가상화 충돌 | VM clone MAC 중복 | hypervisor MAC pool 관리 | duplicate MAC event |

> 요약: MAC 기반 리스크는 위조, flooding, 중복이며 스위치 포트 정책과 MAC table 관측으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| MAC table | utilization 80% 이하 | switch show mac address-table |
| 보안 이벤트 | port security violation 0건 | switch log, SIEM |
| 중복 여부 | duplicate MAC 0건 | ARP table, NMS event |

> 요약: MAC 주소 운영은 table 용량, 보안 위반, 중복 이벤트를 기준으로 점검한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 접근 통제: 중요 서버 포트에 sticky MAC 또는 802.1X를 적용하고 violation 발생 시 shutdown 또는 restrict 정책 선택
2. 가상화 관리: VM·컨테이너 MAC pool을 중앙 관리하고 clone 배포 시 duplicate MAC 검사를 CI에 포함
3. 관측: MAC table utilization 80%, unknown unicast, port security violation을 스위치 텔레메트리로 수집

**결론 (2줄):**
- 기술사 판단: 일반 사용자망은 동적 MAC 학습을 쓰고, 서버·관리망은 port security와 802.1X 기반 접근 통제를 적용함
- 향후 방향: SDN·가상화 환경에서는 물리 NIC MAC보다 workload identity와 L2 overlay 식별자 관리가 병행됨

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "MAC 주소 구조를 설명하시오" | ARP와 스위치 학습 흐름 | 48bit 구조와 IP 주소 비교 |
| 요구사항 명시형 | "MAC 보안 방안을 제시하시오", "IP와 비교하시오" | spoofing·flooding 대응 절차 | port security, 802.1X, 점검 지표 |

> 요약: 설명형은 주소 구조와 전달 원리를, 보안·비교형은 IP와의 차이 및 L2 통제 방안을 강조한다.
