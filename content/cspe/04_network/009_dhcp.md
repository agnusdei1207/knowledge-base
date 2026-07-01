---
title: "DHCP (DHCP)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 9
---

# 📖 【암기용】 개념 완전 이해

> 목적: DHCP를 IP 주소 자동 할당과 임대 관리 프로토콜로 이해하게 만든다. 시험 답안 양식이 아니라, 단말이 네트워크 설정을 얻는 과정을 설명한다.

## 한눈에
- **개요**: DHCP는 단말에 IP 주소와 네트워크 옵션을 자동 할당하는 프로토콜이다.
- **왜 필요한가**: 수백·수천 대 단말에 IP, gateway, DNS를 수동 설정하면 중복과 오류가 발생하므로 중앙 임대 관리가 필요하다.
- **핵심 직관**: 회의장 입구에서 좌석표와 안내문을 받아 지정된 시간 동안 자리를 쓰는 방식과 같다.

## 깊이 이해
- **배경·문제의식**: 고정 IP 수동 설정은 단말 이동, 주소 중복, DNS 변경 대응에 취약하다. DHCP는 주소 풀과 lease time을 기반으로 자동 할당과 회수를 수행한다.
- **작동 원리**: 클라이언트는 broadcast로 DHCP Discover를 보내고, 서버는 Offer를 제안한다. 클라이언트가 Request로 선택하면 서버가 ACK로 임대를 확정한다.
- **비유**: 호텔 체크인에서 빈 방을 제안받고, 손님이 선택하면 프런트가 숙박 기간과 출입카드를 발급하는 구조이다.
- **구체 예시**: 사무실 VLAN `10.10.20.0/24`에서 DHCP 서버는 `10.10.20.50~200`, gateway `10.10.20.1`, DNS `10.10.1.10`을 8시간 lease로 제공할 수 있다.
- **흔한 오해·주의점**: DHCP는 IP 주소만 주지 않는다. subnet mask, default gateway, DNS server, domain, NTP 등 다양한 option을 제공한다.

## 연결 개념
- ARP: IP 사용 전 중복 확인과 gateway MAC 해석
- DHCP relay: 다른 서브넷의 DHCP 서버로 요청 전달
- DHCP snooping: rogue DHCP 차단과 ARP 보안 연계

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 준수한다.
> 핵심: DHCP는 DORA 절차, UDP 67/68, lease, option, relay, snooping을 함께 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DHCP는 클라이언트에 IP 주소와 gateway, DNS, lease time 등 네트워크 설정을 자동 할당하는 프로토콜이다.
> 2. **가치**: 주소 중복과 수동 설정 오류를 줄이고, 단말 이동과 대규모 사용자망 운영을 중앙 정책으로 관리한다.
> 3. **판단 포인트**: DORA 절차, DHCP relay, lease time, address pool, rogue DHCP 대응을 답안에 포함해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| DHCP 동작 절차 확인 | Discover, Offer, Request, ACK | 네 단계 순서와 broadcast/unicast 구분 누락 |
| 네트워크 옵션 관리 이해 확인 | IP, mask, gateway, DNS, lease | IP 주소 할당만 설명 |
| 운영·보안 대응 확인 | relay agent, scope, snooping | rogue DHCP와 pool exhaustion 누락 |

> 요약: DHCP 답안은 자동 할당 절차와 운영 통제·보안 리스크를 함께 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

DHCP는 단말의 IP 주소와 네트워크 옵션을 자동 할당하는 프로토콜이다. 사용자망·무선망·VDI처럼 단말 수와 위치가 변하는 환경에서 수동 IP 관리는 중복과 누락을 만든다. DHCP는 주소 풀, lease, option으로 중앙 관리와 회수를 수행한다.

---

## Ⅱ. 구조 및 구성요소

```text
DHCP Client
-> Broadcast Discover
-> DHCP Server / Relay Agent
-> Address Pool / Lease DB / Options
-> Offer / Request / ACK
-> IP Configuration Applied
```

| 구성요소 | 역할 | 대표 값·특징 |
|:---|:---|:---|
| DHCP Client | 주소와 옵션 요청 | UDP 68 |
| DHCP Server | pool에서 주소 임대 | UDP 67 |
| Relay Agent | 다른 subnet 서버로 요청 전달 | giaddr, IP helper |
| Address Pool | 할당 가능한 주소 범위 | scope, exclusion |
| Lease DB | 임대 상태와 만료 시간 관리 | lease time 8시간 예시 |

> 요약: DHCP는 클라이언트, 서버, relay, 주소 풀, lease DB로 구성되어 자동 설정을 제공한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Client 부팅
-> DHCP Discover broadcast
-> DHCP Offer 수신
-> DHCP Request 송신
-> DHCP ACK 수신
-> IP / Gateway / DNS / Lease 적용
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Discover로 서버 탐색 | source 0.0.0.0, broadcast |
| 2 | Offer로 주소·옵션 제안 | yiaddr, option 3 gateway, option 6 DNS |
| 3 | Request로 특정 서버 제안 선택 | requested IP option |
| 4 | ACK로 lease 확정 | lease time, T1/T2 renewal |
| 5 | lease 갱신 또는 반납 | renewal success, DHCP Release |

> 요약: DHCP는 DORA 절차로 주소를 임대하고 lease 갱신을 통해 주소 풀을 회수·재사용한다.

---

## Ⅳ. 특징

| 구분 | 수동 IP | DHCP | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 설정 | 단말별 수작업 | 중앙 pool·option 배포 | RFC 2131 |
| 변경 대응 | 단말 재설정 필요 | scope option 변경 | UDP 67/68 |
| 주소 회수 | 미사용 IP 추적 어려움 | lease 만료 후 회수 | T1 50%, T2 87.5% 예시 |
| 보안 | rogue 서버 영향 제한적 | rogue DHCP 위험 | DHCP snooping |

> 요약: DHCP는 대규모 단말 설정을 중앙화하지만 rogue DHCP와 pool exhaustion 통제가 필요하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | DHCP | Static IP | 선택 기준 |
|:---|:---|:---|:---|
| 대상 | 사용자 단말, 무선, VDI | 서버, 네트워크 장비 | 이동 단말은 DHCP, 핵심 장비는 static |
| 운영 | lease와 scope 관리 | IPAM 수동 등록 | 단말 수 100대 이상은 DHCP 우선 |
| 장애 영향 | 서버·relay 장애 시 신규 할당 실패 | 설정 오류 시 개별 장애 | 이중화와 relay 설계 필요 |

> 요약: DHCP는 사용자·동적 단말에 적합하고, 서버·장비는 IPAM 기반 정적 주소가 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| pool exhaustion | 주소 범위 부족, lease 과다 | scope 확장, lease time 조정 | utilization 80% 경보 |
| rogue DHCP | 비인가 서버 응답 | DHCP snooping, trusted port 제한 | snooping drop count |
| relay 장애 | IP helper 누락 | relay 이중화, gateway 설정 점검 | Discover 대비 ACK 비율 |

> 요약: DHCP 리스크는 주소 고갈, 비인가 서버, relay 누락이며 utilization과 DORA 성공률로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 할당 성공률 | DHCP ACK success 99.9% 이상 | server log, packet capture |
| 주소 풀 | pool utilization 80% 이하 | DHCP scope monitoring |
| 보안 이벤트 | rogue DHCP 0건 | DHCP snooping, SIEM |

> 요약: DHCP 운영 품질은 ACK 성공률, pool 사용률, snooping 이벤트로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. scope 설계: VLAN별 DHCP scope, exclusion range, lease time 8~24시간, gateway·DNS option을 표준화
2. 가용성: DHCP failover 또는 split scope를 구성하고 relay agent를 L3 gateway 이중화와 함께 점검
3. 보안 통제: access switch DHCP snooping 활성화, trusted port를 uplink로 제한, binding table을 DAI와 연계

**결론 (2줄):**
- 기술사 판단: 사용자·무선·VDI망은 DHCP를 기본으로 하고, 서버·네트워크 장비는 IPAM 승인 기반 static IP를 적용함
- 향후 방향: IPv6 환경에서는 DHCPv6와 SLAAC가 병행되므로 RA, DNS option, 보안 정책을 함께 설계해야 함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "DHCP를 설명하시오" | DORA 절차와 lease 갱신 흐름 | 수동 IP 대비 특징 |
| 요구사항 명시형 | "DHCP 장애 대응 방안을 제시하시오", "보안 대책을 설명하시오" | Discover-to-ACK 분석 절차 | pool, relay, snooping, 지표 중심 |

> 요약: 설명형은 DORA를, 장애·보안형은 scope·relay·rogue DHCP 통제를 중심으로 전환한다.
