---
title: "TCP/IP 4계층 모델 (TCP/IP Model)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 2
---

# 📖 【암기용】 개념 완전 이해

> 목적: TCP/IP 4계층 모델을 인터넷 구현 관점에서 이해하게 만든다. 시험 답안 양식이 아니라, 실제 통신 흐름을 이해하기 위한 설명이다.

## 한눈에
- **개요**: 인터넷 통신을 응용, 전송, 인터넷, 네트워크 접근 계층으로 나눈 구현 모델
- **왜 필요한가**: 웹, 메일, DNS, 파일 전송이 서로 다른 응용이어도 IP 기반 패킷 전달과 TCP/UDP 전송 위에서 동작하게 하기 위함이다.
- **핵심 직관**: TCP/IP는 OSI보다 덜 세분하지만, 실제 인터넷 장비와 운영 절차가 따르는 프로토콜 묶음이다.

## 깊이 이해
- **배경·문제의식**: ARPANET에서 시작된 인터넷은 이기종 네트워크를 하나의 IP 계층으로 연결해야 했다. TCP/IP는 특정 장비보다 프로토콜 상호 운용에 초점을 두고 발전했다.
- **작동 원리**: 응용 계층은 HTTP·DNS 같은 서비스를 제공하고, 전송 계층은 TCP/UDP 포트로 프로세스를 식별한다. 인터넷 계층은 IP 주소와 라우팅으로 목적지까지 패킷을 보내고, 네트워크 접근 계층은 Ethernet·Wi-Fi로 실제 매체에 싣는다.
- **비유**: 택배에서 물품 내용(응용), 송장 번호와 배송 보장(전송), 목적지 주소(인터넷), 트럭·도로(네트워크 접근)를 나눈 구조와 같다.
- **구체 예시**: HTTPS 접속은 HTTP over TLS가 응용 계층, TCP 443이 전송 계층, IPv4/IPv6가 인터넷 계층, Ethernet/Wi-Fi가 네트워크 접근 계층이다.
- **흔한 오해·주의점**: TCP/IP 모델은 TCP와 IP만 의미하지 않는다. UDP, ICMP, ARP, DNS, BGP 등 인터넷 프로토콜군 전체를 포함한다.

## 연결 개념
- OSI 7계층 모델: 설명·진단용 7계층 참조 모델
- TCP/UDP: 전송 계층의 신뢰성·지연 특성 차이
- IP 라우팅: 인터넷 계층의 경로 선택 기능

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 준수한다.
> 핵심: TCP/IP는 인터넷 구현 스택이므로 OSI 매핑, 계층별 프로토콜, 캡슐화 흐름, 운영 지표를 함께 제시한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: TCP/IP 4계층 모델은 인터넷 통신을 Application, Transport, Internet, Network Access 계층으로 구분한 프로토콜 스택이다.
> 2. **가치**: IP 기반 이기종 네트워크 연결과 TCP/UDP 기반 종단 간 통신을 통해 전 세계 인터넷 상호 운용을 제공한다.
> 3. **판단 포인트**: OSI 7계층과의 대응, TCP/UDP 선택 기준, IP 라우팅과 링크 계층의 분리를 명확히 써야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 인터넷 프로토콜 스택 이해 확인 | 4계층 역할, 대표 프로토콜, OSI 매핑 | TCP/IP를 TCP와 IP 2개 프로토콜로 축소 |
| 종단 간 통신 구조 판단 확인 | TCP 연결, UDP 데이터그램, IP best effort | 포트와 IP 주소 역할 혼동 |
| 운영·장애 분석 역량 확인 | DNS, route, MTU, TCP retransmission 지표 | L2 장애와 L4 장애를 같은 원인으로 처리 |

> 요약: TCP/IP 답안은 계층별 역할과 실제 인터넷 프로토콜 흐름을 함께 보여야 한다.

---

## Ⅰ. 개요 및 필요성

TCP/IP 4계층 모델은 인터넷 프로토콜군의 구현 중심 계층 모델이다. 이기종 LAN, WAN, 무선망을 IP 계층으로 연결하고, 응용은 TCP/UDP 포트 위에서 독립적으로 동작한다. 인터넷 규모의 상호 운용과 장애 분석을 위해 4계층 역할 분리가 필요하다.

---

## Ⅱ. 구조 및 구성요소

```text
User Service
-> Application: HTTP / DNS / SMTP
-> Transport: TCP / UDP / QUIC
-> Internet: IPv4 / IPv6 / ICMP / Routing
-> Network Access: Ethernet / Wi-Fi / PPP
-> Physical Medium
```

| 계층 | 역할 | 대표 프로토콜·장비 |
|:---|:---|:---|
| Application | 사용자 서비스와 데이터 형식 처리 | HTTP, DNS, SMTP, SSH |
| Transport | 프로세스 간 전송, 포트, 신뢰성 | TCP, UDP, QUIC |
| Internet | 논리 주소와 경로 선택 | IPv4, IPv6, ICMP, Router |
| Network Access | 프레임 전달과 매체 접근 | Ethernet, Wi-Fi, Switch |

> 요약: TCP/IP는 응용 서비스를 TCP/UDP와 IP 계층 위에 올리고, 실제 매체 전달은 네트워크 접근 계층에 위임한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Application Data
-> Transport Header 추가: port / sequence / checksum
-> IP Header 추가: source IP / destination IP / TTL
-> Link Header 추가: source MAC / destination MAC / FCS
-> Medium 전송 -> 수신 측 역캡슐화
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | DNS로 서비스 이름을 IP로 변환 | A/AAAA record, TTL |
| 2 | TCP 3-way handshake 또는 UDP 송신 | SYN/SYN-ACK/ACK, port 0~65535 |
| 3 | IP 패킷 생성과 라우팅 | TTL/Hop Limit, routing table |
| 4 | L2 프레임 생성과 next-hop 전달 | ARP/ND, MTU 1500 |
| 5 | 수신 측 계층별 헤더 제거 | p95 RTT, retransmission, packet loss |

> 요약: TCP/IP 통신은 이름 해석, 전송 세션, IP 라우팅, 링크 전달, 역캡슐화 순서로 처리된다.

---

## Ⅳ. 특징

| 구분 | OSI 7계층 | TCP/IP 4계층 | 수치·표준 포인트 |
|:---|:---|:---|:---|
| 목적 | 참조·교육·진단 모델 | 실제 인터넷 구현 모델 | IETF RFC 기반 |
| 계층 | 7개 세분 계층 | 4개 통합 계층 | L5~L7은 Application으로 통합 |
| 전송 | 개념적 전송 계층 | TCP/UDP/QUIC 구현 | TCP port 16bit, UDP header 8byte |
| 주소 | 네트워크 계층 주소 | IPv4 32bit, IPv6 128bit | CIDR prefix 사용 |

> 요약: TCP/IP는 OSI보다 계층 수는 적지만 실제 인터넷 프로토콜과 운영 지표를 직접 설명한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | TCP | UDP | 선택 기준 |
|:---|:---|:---|:---|
| 연결 | 3-way handshake | 비연결 데이터그램 | 신뢰성 필요 시 TCP, 지연 민감 시 UDP |
| 오류 처리 | 재전송, 순서 제어 | 응용에서 처리 | 손실 허용 스트리밍은 UDP |
| 헤더 | 최소 20byte | 8byte | 오버헤드와 지연 요구 확인 |

> 요약: 전송 계층 선택은 신뢰성, 지연, 오버헤드, 응용 복구 능력을 기준으로 판단한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| MTU 블랙홀 | ICMP 차단으로 PMTUD 실패 | MSS clamping, ICMP 허용 | fragmentation needed, retransmission |
| DNS 장애 | resolver 오류·TTL 과다 | 다중 resolver, TTL 60~300초 조정 | NXDOMAIN, SERVFAIL 비율 |
| TCP 재전송 증가 | loss, congestion, window 제한 | QoS, congestion control, window scaling | retransmission 1% 이하 |

> 요약: TCP/IP 운영 리스크는 DNS, MTU, 재전송 지표를 우선 관측해야 조기 분리된다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 연결성 | packet loss 0.1% 이하, RTT p95 50ms 이하 | ping, mtr, traceroute |
| 전송 품질 | TCP retransmission 1% 이하, handshake p95 100ms 이하 | tcpdump, APM |
| 이름 해석 | DNS 응답 p95 50ms 이하, TTL 정책 준수 | dig, resolver log |

> 요약: TCP/IP 품질은 L3 연결성, L4 전송 상태, L7 이름 해석 지표를 분리해 측정한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 설계: 서비스별 TCP/UDP/QUIC 선택 기준을 SLA, p95 latency, loss tolerance 기준으로 문서화
2. 운영: DNS TTL 60~300초, MTU 1500 또는 jumbo 9000 일치, TCP retransmission 1% 이하 경보 설정
3. 장애 대응: dig -> ping/mtr -> traceroute -> tcpdump -> application log 순서로 계층별 원인 분리

**결론 (2줄):**
- 기술사 판단: 구현·운영 문제는 TCP/IP 4계층을 기준으로 쓰고, 설명·진단 문제는 OSI 7계층 매핑을 병기함
- 향후 방향: IPv6, QUIC, HTTP/3 확산으로 TCP/IP 모델은 유지되나 전송 계층 운영 지표는 UDP 기반으로 확대됨

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "TCP/IP 모델을 설명하시오" | 캡슐화 흐름과 계층별 프로토콜 | OSI 매핑과 전송 계층 특징 |
| 요구사항 명시형 | "OSI와 비교하시오", "장애 대응 방안을 제시하시오" | 비교표 또는 계층별 점검 절차 | TCP/UDP 선택 기준, DNS·MTU·재전송 지표 |

> 요약: 설명형은 4계층 구조를, 비교·운영형은 OSI 매핑과 실측 지표 중심으로 답안을 전환한다.
