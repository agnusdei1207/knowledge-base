---
title: "IGMP·멀티캐스트 (Internet Group Management Protocol/Multicast)"
date: "2026-06-30"
weight: 42
tags:
  - "exam-cspe-network"
---

## Ⅰ. 정의
> 멀티캐스트는 하나의 송신으로 특정 그룹의 다수 수신자에게 전달하는 1:N 통신이며, IGMP(Internet Group Management Protocol)는 호스트가 멀티캐스트 그룹에 가입/탈퇴를 관리하는 프로토콜이다.

## Ⅱ. 구성요소 / 원리
- 멀티캐스트 주소: IPv4 D클래스 224.0.0.0/4(224~239), 그룹 식별자 역할
- IGMP: 호스트↔로컬 라우터 간 그룹 멤버십 관리(Join/Leave/Query/Report)
- IGMP 버전: v1(가입/질의), v2(Leave 추가), v3(SSM, 송신지 지정)
- PIM(Protocol Independent Multicast): 라우터 간 멀티캐스트 라우팅(PIM-SM/DM)
- 멀티캐스트 트리: Source Tree(SPT)·Shared Tree(RP 중심)로 전달 경로 구성

## Ⅲ. 흐름도 / 구조
```text
[송신자] → 224.x.x.x 그룹으로 1회 송신
   라우터(PIM) ── 멀티캐스트 트리 ──┐
   IGMP Report(가입) ↑              ▼
[수신A] [수신B] ... 그룹 멤버만 수신
   IGMP Leave → 트리에서 가지치기(Prune)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 동일 콘텐츠를 다수에게 효율 전달, 대역폭 절감(중복 전송 제거) |
| 장점 | 송신 1회로 N 수신, 유니캐스트 대비 트래픽·서버 부하 감소 |
| 한계 | UDP 기반 비신뢰, 망 전체 멀티캐스트 라우팅 구성 복잡, WAN 확장성 제약 |

## Ⅴ. 기술사적 적용
- IPTV·실시간 스트리밍·증권 시세 배포 등 일대다 서비스에 적용
- L2 스위치의 IGMP Snooping으로 불필요한 멀티캐스트 플러딩 억제
- IPv6에서는 IGMP 대신 MLD(Multicast Listener Discovery)가 동일 역할 수행
