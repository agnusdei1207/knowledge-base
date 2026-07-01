---
title: "ICMP·IGMP (ICMP IGMP)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 17
---

# 📖 【암기용】 개념 완전 이해

> 목적: ICMP와 IGMP를 처음 봐도 제어 메시지와 멀티캐스트 그룹 관리의 차이를 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: ICMP는 IP 오류·진단 메시지, IGMP는 IPv4 멀티캐스트 그룹 가입 관리를 담당하는 제어 프로토콜
- **왜 필요한가**: IP는 비연결형 전달만 수행하므로 오류 원인과 경로 상태를 별도 메시지로 알려야 한다. 멀티캐스트는 수신 의사가 있는 호스트에게만 트래픽을 보내기 위해 그룹 가입 정보가 필요하다.
- **핵심 직관**: ICMP는 배송 실패 사유서이고, IGMP는 방송 채널 구독 명단이다.

## 깊이 이해
- **배경·문제의식**: ping, traceroute, PMTUD는 ICMP 없이는 동작하기 어렵다. IPTV, 증권 시세, 대규모 스트리밍 같은 1:N 전송은 IGMP로 수신 그룹을 관리해야 L2 스위치에서 불필요한 flooding을 줄인다.
- **작동 원리**: ICMP는 Echo Request/Reply, Destination Unreachable, Time Exceeded 등을 IP 위에서 전달한다. IGMP는 호스트가 멀티캐스트 그룹에 Membership Report를 보내고 라우터가 Query로 구성원을 확인한다.
- **비유**: ICMP는 길이 막힌 이유를 알려주는 도로 표지판이고, IGMP는 특정 강의실에 들어올 학생 명단을 확인하는 출석부다.
- **구체 예시**: traceroute는 TTL을 1부터 늘려 ICMP Time Exceeded를 받아 경유 라우터를 확인한다. IGMPv3는 source-specific multicast로 특정 송신자만 허용할 수 있다.
- **흔한 오해·주의점**: ICMP를 모두 차단하면 ping 차단뿐 아니라 Path MTU Discovery와 장애 분석도 훼손될 수 있다. 필요한 type/code만 통제해야 한다.

## 연결 개념
- PMTUD — ICMP Fragmentation Needed로 경로 MTU 확인
- IGMP Snooping — L2 스위치가 그룹 가입 정보를 보고 포트별 멀티캐스트 전달
- PIM — 라우터 간 멀티캐스트 라우팅 프로토콜

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: ICMP/IGMP는 데이터 전달 프로토콜이 아니라 IP 제어와 멀티캐스트 멤버십 관리 프로토콜로 구분한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ICMP는 IP 오류·진단 제어 메시지, IGMP는 IPv4 멀티캐스트 그룹 가입·탈퇴 관리 프로토콜이다.
> 2. **가치**: ICMP는 장애 위치·MTU 문제를 식별하고, IGMP는 멀티캐스트 트래픽을 필요한 수신 포트로 제한한다.
> 3. **판단 포인트**: ICMP type/code, TTL, PMTUD, IGMPv2/v3, IGMP snooping, querier 동작을 구분해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| IP 제어 프로토콜 이해 확인 | ICMP 오류·진단, IGMP 그룹 관리 | 둘 다 ping 프로토콜로 서술 |
| 장애 분석 역량 확인 | Echo, Time Exceeded, Destination Unreachable | ICMP 전체 차단을 권고 |
| 멀티캐스트 운영 판단 확인 | Membership Report, Query, snooping | 브로드캐스트와 멀티캐스트 혼동 |

> 요약: ICMP/IGMP 문제는 제어 메시지 type과 멀티캐스트 그룹 관리 흐름을 분리해 작성해야 한다.

---

## Ⅰ. 개요 및 필요성

ICMP와 IGMP는 IP 계층을 보완하는 제어 프로토콜이다. ICMP는 오류·진단 메시지로 ping, traceroute, PMTUD에 사용된다. IGMP는 IPv4 멀티캐스트 수신 그룹을 관리해 불필요한 트래픽 확산을 줄인다.

---

## Ⅱ. 구조 및 구성요소

```text
IP Network Control
  / ICMP: Error and Diagnostic Message
  / IGMP: Multicast Membership Management
Host -> Router or Switch -> Monitoring and Forwarding Control
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| ICMP Echo | 도달성 확인 | ping request/reply |
| ICMP Error | 오류 원인 전달 | Time Exceeded, Unreachable |
| IGMP Host | 그룹 가입·탈퇴 보고 | Membership Report |
| IGMP Querier | 그룹 구성원 확인 | Query interval 운영 |

> 요약: ICMP는 IP 오류·진단 메시지, IGMP는 멀티캐스트 수신 그룹 상태를 관리한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
ICMP: Packet Event -> Type/Code Generate -> Sender Receives Diagnosis
IGMP: Host Join -> Membership Report -> Querier Tracks Group
  -> Switch Snooping Table Update -> Multicast Forwarding
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | ICMP Echo 또는 오류 type/code 생성 | ICMP type, code 확인 |
| 2 | TTL 초과 시 Time Exceeded 반환 | traceroute hop 확인 |
| 3 | Host가 IGMP Membership Report 전송 | group address 224/4 |
| 4 | 스위치가 snooping table로 포트 제한 | multicast flooding 감소 |

> 요약: ICMP는 이벤트 기반 진단 메시지, IGMP는 가입 보고와 Query 기반 그룹 상태 관리로 동작한다.

---

## Ⅳ. 특징

| 구분 | ICMP | IGMP | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 목적 | 오류·진단 제어 | 멀티캐스트 가입 관리 | ICMP RFC 792, IGMP RFC 3376 |
| 대상 | 송신자와 라우터/호스트 | 호스트와 멀티캐스트 라우터 | IPv4 224.0.0.0/4 |
| 대표 기능 | ping, traceroute, PMTUD | Membership Query/Report | IGMPv3 SSM |
| 운영 통제 | type/code별 허용 | snooping, querier 설정 | TTL, MTU 확인 |

> 요약: ICMP는 경로 진단, IGMP는 멀티캐스트 수신 범위 통제를 담당한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 전체 차단 | 선택적 허용 | 선택 기준 |
|:---|:---|:---|:---|
| ICMP 운영 | ping·PMTUD 장애 가능 | Echo 제한, 오류 type 허용 | PMTUD 필요 구간은 type 3 code 4 허용 |
| IGMP 운영 | 멀티캐스트 flooding | snooping과 querier 적용 | IPTV·시세망은 IGMPv3 고려 |
| 보안 통제 | 탐지 회피 가능 | rate-limit, ACL, logging | ICMP flood 임계치 설정 |

> 요약: ICMP와 IGMP는 전체 차단보다 필요한 type과 그룹을 제한적으로 허용하는 정책이 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| PMTUD 실패 | ICMP Fragmentation Needed 차단 | type/code 기반 ACL 허용 | TCP MSS 조정 건수 |
| ICMP Flood | 대량 Echo 요청 | rate-limit, CoPP | ICMP pps |
| 멀티캐스트 확산 | IGMP snooping 미적용 | snooping, querier 설정 | multicast unknown flooding |

> 요약: 제어 프로토콜 리스크는 필요한 메시지 허용과 rate-limit, snooping으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 경로 진단 | 핵심 구간 ping/traceroute 가능 | ICMP type별 테스트 |
| MTU 탐지 | DF bit 테스트 통과 | PMTUD, packet capture |
| 멀티캐스트 전달 | 가입 포트에만 전달 | IGMP snooping table |

> 요약: ICMP/IGMP 운영 품질은 진단 가능성, MTU 탐지, 멀티캐스트 포트 제한으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 외부 경계는 ICMP Echo를 rate-limit하고 PMTUD에 필요한 Destination Unreachable type/code는 업무 구간별로 허용함
2. 멀티캐스트 VLAN은 IGMP snooping과 querier를 설정하고 그룹별 수신 포트를 주기 점검함
3. 장애 분석 표준 절차에 ping, traceroute, DF ping, packet capture를 포함해 type/code 기준으로 원인을 분류함

**결론 (2줄):**
- 기술사 판단: ICMP는 진단·MTU에 필요한 type만 허용하고, IGMP는 멀티캐스트 서비스가 있는 VLAN에 snooping과 querier를 적용함
- 향후 방향: 제어 평면 보호(CoPP)와 telemetry로 ICMP/IGMP pps, group state 변화를 지속 관측해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "ICMP와 IGMP를 설명하시오" | type/code, Query/Report 흐름 | ICMP와 IGMP 목적 비교 |
| 요구사항 명시형 | "멀티캐스트 운영 방안을 제시하시오" | IGMP snooping, querier | flooding 리스크와 지표 |

> 요약: ICMP/IGMP는 설명형이면 제어 메시지 차이, 운영형이면 허용 정책과 snooping 지표 중심으로 전환한다.
