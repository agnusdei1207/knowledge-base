---
title: "IPv4 헤더 (IPv4 Header)"
date: "2026-06-30"
weight: 31
tags:
  - "exam-cspe-network"
---

## Ⅰ. 정의
> 네트워크 계층에서 패킷의 라우팅·단편화·오류제어에 필요한 제어정보를 담은 최소 20바이트(옵션 제외)의 헤더 구조.

## Ⅱ. 구성요소 / 원리
- Version/IHL: 버전(4)과 헤더 길이(Internet Header Length, 4바이트 단위)
- TOS/DSCP: 서비스 품질·우선순위 지정
- TTL(Time To Live): 홉마다 1 감소, 0이면 폐기(루프 방지)
- Protocol: 상위 프로토콜 식별(TCP=6, UDP=17, ICMP=1)
- Header Checksum: 헤더 무결성 검증(홉마다 재계산), 출발/목적 주소(각 32비트)

## Ⅲ. 흐름도 / 구조
```text
0      4      8           16                 31
+------+------+-----------+-------------------+
|Ver|IHL| TOS |        Total Length          |
+-----------+--------+----+------------------+
| Identification |Flags|  Fragment Offset    |
+--------+--------+-----+--------------------+
|  TTL   |Protocol|     Header Checksum      |
+--------+--------+-------------------------+
|       Source / Destination Address        |
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 패킷 라우팅·단편화·수명관리에 필요한 제어정보 제공 |
| 장점 | 단순·범용 구조, 옵션 확장성, 비연결형 전달 |
| 한계 | 주소 32비트 고갈, 홉마다 체크섬 재계산 부담, 헤더 가변 |

## Ⅴ. 기술사적 적용
- IPv6는 고정 40바이트 헤더·체크섬 제거로 라우팅 효율 개선
- DSCP 필드로 QoS·DiffServ 정책 적용
- TTL은 traceroute·루프 방지, Protocol은 역다중화 기준
