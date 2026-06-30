---
title: "IPsec (Internet Protocol Security)"
date: "2026-06-30"
weight: 54
tags:
  - "exam-cspe-network"
---

## Ⅰ. 정의
> IP 계층에서 데이터의 기밀성·무결성·인증을 제공하는 보안 프로토콜 집합으로, AH·ESP 보안 프로토콜과 IKE 키 관리로 안전한 통신 채널을 구성한다.

## Ⅱ. 구성요소 / 원리
- AH(Authentication Header): 무결성·인증·재전송방지 제공(암호화 X)
- ESP(Encapsulating Security Payload): 기밀성(암호화)+무결성·인증 제공
- IKE(Internet Key Exchange): SA 협상·키 교환(Phase1 IKE SA, Phase2 IPsec SA)
- 전송모드(Transport): 페이로드만 보호, 종단 간 통신
- 터널모드(Tunnel): IP 헤더 포함 전체 캡슐화, 게이트웨이 간 VPN

## Ⅲ. 흐름도 / 구조
```text
[IKE Phase1] -> 인증·DH로 IKE SA 수립
       |
[IKE Phase2] -> IPsec SA(암호스위트,키) 협상
       |
   ESP/AH 적용 -> SPI로 SA 식별 -> 암호화/인증 전송
   (Transport: 페이로드 / Tunnel: 전체 패킷)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | IP 계층 종단/게이트웨이 간 기밀성·무결성·인증 보장 |
| 장점 | 애플리케이션 투명, 표준 기반, VPN 핵심 기술 |
| 한계 | NAT 통과 문제(→ NAT-T), 설정 복잡, 헤더 오버헤드 |

## Ⅴ. 기술사적 적용
- 사이트투사이트 IPsec VPN(터널모드)으로 본사-지사 보안 연결
- SSL VPN과 비교: IPsec은 네트워크 계층 전체, SSL은 응용 세션 단위
- SA(Security Association) 단방향 특성상 양방향 2개 SA 필요, IKEv2로 효율화
