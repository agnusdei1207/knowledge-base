---
title: "이더넷 프레임 구조·IEEE 802.3 (Ethernet Frame)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 18
---

# 📖 【암기용】 개념 완전 이해

> 목적: 이더넷 프레임을 처음 봐도 L2에서 MAC 주소, EtherType, FCS가 어떤 역할을 하는지 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: LAN에서 데이터를 전달하기 위해 MAC 주소와 오류 검출 정보를 담는 IEEE 802.3 L2 데이터 단위
- **왜 필요한가**: IP 패킷은 같은 LAN 안에서 실제 NIC까지 전달되려면 MAC 주소 기반 프레임으로 캡슐화되어야 한다. 이더넷 프레임은 목적지 MAC, 출발지 MAC, 유형/길이, payload, FCS로 L2 전달과 오류 검출을 수행한다.
- **핵심 직관**: IP 패킷이 편지 내용이라면 이더넷 프레임은 같은 건물 안에서 어느 방으로 보낼지 적은 봉투다.

## 깊이 이해
- **배경·문제의식**: LAN 장비는 IP보다 아래 계층에서 동작하며, 스위치는 MAC 주소 테이블로 프레임을 전달한다. 프레임 구조를 알아야 VLAN tagging, MTU, jumbo frame, CRC 오류를 해석할 수 있다.
- **작동 원리**: 송신 NIC는 payload 앞에 목적지/출발지 MAC과 EtherType 또는 Length를 붙이고 끝에 FCS를 추가한다. 수신 NIC는 FCS를 검사하고 목적지 MAC이 자신 또는 브로드캐스트/멀티캐스트이면 상위 계층으로 전달한다.
- **비유**: 물류 박스 겉면의 받는 사람, 보내는 사람, 물품 종류, 훼손 확인 봉인과 같다.
- **구체 예시**: Ethernet II 프레임은 Destination MAC 6B, Source MAC 6B, EtherType 2B, Payload 46~1500B, FCS 4B로 구성된다. IPv4 EtherType은 0x0800, ARP는 0x0806, IPv6는 0x86DD이다.
- **흔한 오해·주의점**: MTU 1500은 일반적으로 IP payload 기준이며, L2 헤더와 FCS를 포함한 wire size와 다르다. 802.1Q VLAN tag는 4바이트를 추가한다.

## 연결 개념
- MAC 주소 — L2 식별자, OUI 24비트와 NIC 식별자 구성
- VLAN 802.1Q — 이더넷 프레임에 4바이트 tag 삽입
- CRC/FCS — 프레임 오류 검출, 복구는 상위 계층이 담당

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 이더넷 프레임 답안은 필드 길이, EtherType, MTU, FCS, VLAN tag 영향을 수치로 제시한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 이더넷 프레임은 MAC 주소 기반 L2 전달을 위해 목적지/출발지 MAC, Type/Length, Payload, FCS를 담는 IEEE 802.3 데이터 단위이다.
> 2. **가치**: LAN 스위칭, 상위 프로토콜 식별, 오류 검출, VLAN 확장, MTU 설계의 공통 기준이 된다.
> 3. **판단 포인트**: 64~1518B 프레임, payload 46~1500B, FCS 4B, 802.1Q tag 4B, jumbo frame 지원 여부를 확인한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| L2 프레임 구조 이해 확인 | MAC, EtherType/Length, Payload, FCS | IP 패킷 구조와 혼동 |
| 표준 수치 확인 | 64~1518B, MTU 1500, FCS 4B | 프레임 크기와 MTU 혼동 |
| 운영 장애 분석 확인 | CRC error, VLAN tag, jumbo frame | FCS가 오류 수정까지 한다고 서술 |

> 요약: 이더넷 프레임 문제는 필드별 역할과 크기를 수치로 쓰는 것이 핵심이다.

---

## Ⅰ. 개요 및 필요성

이더넷 프레임은 LAN에서 MAC 주소 기반 전달을 수행하는 L2 데이터 단위이다. IP 패킷은 이더넷 프레임 payload에 캡슐화되어 스위치와 NIC를 통과한다. 프레임 구조는 MTU, VLAN, CRC 오류 분석의 기준이다.

---

## Ⅱ. 구조 및 구성요소

```text
Preamble -> Destination MAC -> Source MAC -> Type or Length
  -> Payload -> FCS
  / Optional 802.1Q VLAN Tag between Source MAC and Type
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Destination/Source MAC | L2 송수신자 식별 | 각 6바이트 |
| Type/Length | 상위 프로토콜 또는 길이 표시 | IPv4 0x0800, IPv6 0x86DD |
| Payload | IP, ARP 등 상위 데이터 | 46~1500바이트 |
| FCS | CRC 기반 오류 검출 | 4바이트 |

> 요약: 이더넷 프레임은 MAC 주소, 상위 프로토콜 식별자, payload, FCS로 L2 전달과 오류 검출을 수행한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Upper Packet Receive -> MAC Header Add -> FCS Calculate
  -> Switch MAC Lookup -> Frame Forward
  -> Receiver FCS Check -> EtherType Demultiplex
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | NIC가 상위 패킷을 payload에 적재 | payload 46~1500B |
| 2 | 목적지·출발지 MAC과 EtherType 삽입 | ARP로 목적지 MAC 확보 |
| 3 | 스위치가 MAC table 기반 포트 전달 | aging time, unknown flooding |
| 4 | 수신 측이 FCS 검사 후 상위 계층 전달 | CRC error count |

> 요약: 이더넷은 송신 캡슐화, 스위치 MAC 조회, 수신 FCS 검사, EtherType 분기 순서로 동작한다.

---

## Ⅳ. 특징

| 구분 | Ethernet II/IEEE 802.3 | IP 계층 | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 주소 체계 | MAC 48비트 | IPv4 32비트, IPv6 128비트 | OUI 24비트 |
| 데이터 단위 | Frame | Packet | 64~1518B |
| 오류 처리 | FCS 오류 검출 | TTL, checksum 등 | CRC 32비트 |
| 확장 | 802.1Q VLAN tag | DSCP, routing | tag 4바이트 |

> 요약: 이더넷 프레임은 L2 전달과 오류 검출 기준이며, IP 계층의 라우팅 기능과 역할이 다르다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 표준 프레임 | Jumbo Frame | 선택 기준 |
|:---|:---|:---|:---|
| 크기 | MTU 1500 기준 | 9000B 등 장비별 지원 | 스토리지·백업망에서 검토 |
| 비용/성능 | 호환성 높음 | 패킷 수 감소 | 전 구간 MTU 일치 필요 |
| 운영/위험 | 단편화 적음 | blackhole 가능 | DF ping으로 검증 |

> 요약: Jumbo frame은 전 구간 MTU가 일치할 때만 적용하고, 혼재 구간은 표준 MTU 1500을 유지한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| CRC 오류 | 케이블, 포트, duplex 문제 | 케이블 교체, 포트 협상 점검 | FCS error count |
| MTU blackhole | 중간 장비 MTU 불일치 | PMTUD, MSS clamping | DF ping 실패율 |
| VLAN tag 누락 | trunk/access 설정 오류 | 802.1Q 설정 검증 | VLAN mismatch log |

> 요약: 이더넷 장애는 CRC, MTU, VLAN tag 오류를 포트 카운터와 패킷 캡처로 확인한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 프레임 오류 | CRC/FCS error 0에 근접 | switch interface counter |
| MTU 일치 | 경로 전 구간 동일 MTU | DF ping, packet capture |
| 프로토콜 식별 | EtherType 정상 분기 | Wireshark decode |

> 요약: 프레임 품질은 오류 카운터, MTU 검증, EtherType 식별로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 일반 업무망은 MTU 1500과 802.1Q tag 4바이트 영향을 기준으로 스위치·방화벽 인터페이스를 점검함
2. 스토리지망에서 jumbo frame을 쓰면 서버 NIC, 스위치, 라우터 전 구간 MTU를 동일하게 맞추고 DF ping으로 검증함
3. 장애 분석 시 CRC, runts, giants, alignment error 카운터와 패킷 캡처의 EtherType 값을 함께 확인함

**결론 (2줄):**
- 기술사 판단: 범용 LAN은 표준 MTU 1500, 대량 백업·스토리지망은 전 구간 검증 후 jumbo frame을 선택함
- 향후 방향: 고속 Ethernet 환경에서는 MTU, FEC, telemetry 포트 카운터를 연계해 프레임 손실 원인을 자동 분류해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "이더넷 프레임을 설명하시오" | 캡슐화, FCS 검사, EtherType 분기 | 필드 크기와 IP 패킷 비교 |
| 요구사항 명시형 | "MTU 장애 분석 방안을 제시하시오" | DF ping, PMTUD, 캡처 흐름 | jumbo frame 리스크와 지표 |

> 요약: 이더넷 프레임은 설명형이면 필드 구조, 장애형이면 MTU·CRC·VLAN tag 지표 중심으로 전환한다.
