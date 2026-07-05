---
title: "DHCP (Dynamic Host Configuration Protocol)"
date: "2026-07-05"
tags:
  - "cspe-network"
weight: 9
---

## Ⅰ. 개요
- **정의**: 네트워크에 접속하는 호스트에 IP·서브넷·게이트웨이·DNS를 자동 할당하는 프로토콜임
- **배경/필요성**: 대규모 네트워크에서 수동 IP 할당은 오류와 관리 부담이 크므로 자동화가 필요함
- **비유**: 호텔 체크인 시 프론트에서 방 번호를 자동 배정받는 것과 같음

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| DORA 4단계 동작 이해 | Discover→Offer→Request→Ack 흐름 | 임대(Lease) 갱신·릴레이 에이전트 개념 포함 |

> 요약: DHCP는 DORA 4단계로 IP를 자동 할당하여 네트워크 관리를 자동화함

## Ⅱ. 구성요소
```text
[Client] --Discover(브로드캐스트)--> [DHCP Server]
         <--Offer--
         --Request-->
         <--Ack-- (IP 임대 완료)
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| DHCP Server | IP 풀을 관리하고 임대 정보를 제공하는 서버 | 호텔 프론트 데스크 |
| DHCP Client | IP 할당을 요청하는 호스트 | 체크인 고객 |
| DHCP Relay Agent | 서브넷 간 DHCP 메시지를 중계하는 라우터 | 다른 층의 안내 데스크 |

> 요약: 서버가 IP 풀을 관리하고, 클라이언트가 요청하며, 릴레이가 서브넷 간 중계함

## Ⅲ. 절차
```text
Discover --> Offer --> Request --> Acknowledge
```
- 1단계: Discover — 클라이언트가 브로드캐스트로 DHCP 서버를 탐색함
- 2단계: Offer — 서버가 할당 가능한 IP·옵션을 클라이언트에 제안함
- 3단계: Request — 클라이언트가 특정 서버의 Offer를 선택하여 요청함
- 4단계: Acknowledge — 서버가 IP 임대를 확정하고 임대 기간(Lease Time)을 통보함

> 요약: DORA 4단계로 IP 주소의 탐색·제안·요청·확정이 완료됨

## Ⅳ. 문제점
- DHCP 스푸핑: 인증 부재 — 위조 서버가 잘못된 게이트웨이·DNS를 배포하여 MITM 공격 유발
- 단일 장애점: 서버 집중 — DHCP 서버 장애 시 신규 접속 호스트에 IP 할당 불가
- 주소 풀 고갈: 임대 관리 미흡 — 유휴 장비가 IP를 점유하여 가용 주소 부족 발생

> 요약: 스푸핑·단일 장애점·주소 풀 고갈이 DHCP 운영의 주요 위험임

## Ⅴ. 개선방안
1. 단기: DHCP Snooping 활성화로 비인가 DHCP 서버를 차단함
2. 중기: DHCP 이중화(Failover/Split-Scope)로 가용성을 확보함
3. 장기: Lease Time 최적화 및 IP 사용 모니터링으로 주소 풀을 효율 관리함

> 요약: Snooping → 이중화 → Lease 최적화로 DHCP 보안과 가용성을 확보함

## Ⅵ. 전망
- 발전 방향: DHCPv6와 SLAAC 병행으로 IPv6 환경의 주소 자동 설정이 진화함
- 기술사적 판단: DHCP Snooping은 L2 보안의 기본 구성 요소로 DAI와 연계 운영이 필수임
- 기술사 제언: Zero Trust 환경에서 DHCP+802.1X 연동 인증 체계를 구축할 것을 제안함
