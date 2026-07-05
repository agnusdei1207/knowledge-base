---
title: "ARP·RARP (Address Resolution Protocol)"
date: "2026-07-05"
tags:
  - "cspe-network"
weight: 8
---

## Ⅰ. 개요
- **정의**: IP 주소와 MAC 주소 간 매핑을 수행하는 L2/L3 연계 프로토콜임
- **배경/필요성**: IP 패킷을 LAN에서 전달하려면 목적지의 물리 주소(MAC)를 알아야 함
- **비유**: 이름(IP)을 알고 있을 때 전화번호부(ARP 테이블)에서 전화번호(MAC)를 찾는 것과 같음

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| IP↔MAC 변환 메커니즘 | ARP Request(브로드캐스트)·Reply(유니캐스트) 흐름 | ARP 스푸핑 공격과 GARP 개념 언급 |

> 요약: ARP는 IP→MAC 변환, RARP는 MAC→IP 변환을 수행하는 주소 해석 프로토콜임

## Ⅱ. 구성요소
```text
[호스트A] --ARP Request(브로드캐스트)--> [LAN 전체]
[호스트B] --ARP Reply(유니캐스트)--> [호스트A]
          --> ARP Cache 저장
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| ARP Request | 목적지 IP의 MAC을 묻는 브로드캐스트 패킷 | 교실에서 "김철수 누구?" 외치기 |
| ARP Reply | 해당 IP 소유자가 자신의 MAC을 알려주는 유니캐스트 | "저 여기요" 하고 손드는 것 |
| ARP Cache | IP↔MAC 매핑을 임시 저장하는 테이블(TTL 기반 만료) | 주소록 메모 |

> 요약: 브로드캐스트 질의 → 유니캐스트 응답 → 캐시 저장 구조로 동작함

## Ⅲ. 절차
```text
IP 확인 --> ARP Cache 조회 --> ARP Request --> ARP Reply/캐시 갱신
```
- 1단계: IP 확인 — 목적지 IP가 동일 서브넷인지 판별함
- 2단계: 캐시 조회 — ARP Cache에 해당 IP의 MAC 매핑이 존재하는지 확인함
- 3단계: ARP Request — 캐시 미스 시 브로드캐스트로 MAC 주소를 질의함
- 4단계: ARP Reply — 대상 호스트가 MAC을 유니캐스트로 응답하고 양측 캐시를 갱신함

> 요약: 캐시 조회 → 미스 시 브로드캐스트 질의 → 응답 수신 → 캐시 갱신 순으로 동작함

## Ⅳ. 문제점
- ARP 스푸핑: 인증 부재 — 공격자가 위조 Reply를 전송하여 트래픽을 가로챔(MITM)
- 브로드캐스트 부하: 대규모 LAN — 호스트 수 증가 시 ARP 브로드캐스트 폭주로 대역폭 낭비
- 캐시 오염: 무검증 갱신 — Gratuitous ARP로 캐시가 오염되어 통신 장애 발생

> 요약: 인증 없는 구조로 스푸핑·캐시 오염·브로드캐스트 폭주에 취약함

## Ⅴ. 개선방안
1. 단기: Dynamic ARP Inspection(DAI)으로 스위치 단에서 위조 ARP를 차단함
2. 중기: VLAN 분할로 브로드캐스트 도메인을 축소하여 ARP 트래픽 경감
3. 장기: IPv6 NDP(Neighbor Discovery Protocol)로 전환하여 ARP 의존성 제거

> 요약: DAI 적용 → VLAN 분할 → IPv6 NDP 전환으로 ARP 취약점을 해소함

## Ⅵ. 전망
- 발전 방향: IPv6 환경에서는 ARP가 NDP로 대체되어 보안성이 향상됨
- 기술사적 판단: IPv4 잔존 기간 동안 ARP 보안 대책은 L2 보안의 기본 요소임
- 기술사 제언: DAI·DHCP Snooping을 연계한 L2 보안 체계를 구축할 것을 제안함
