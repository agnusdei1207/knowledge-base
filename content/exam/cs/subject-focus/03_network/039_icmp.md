---
title: "ICMP (Internet Control Message Protocol)"
date: "2026-06-30"
weight: 39
tags:
  - "exam-cspe-network"
---

## Ⅰ. 정의
> ICMP(Internet Control Message Protocol)는 IP 패킷 전달 과정의 오류 보고와 네트워크 상태 진단·제어 메시지를 전달하는 IP 계층 보조 프로토콜이다.

## Ⅱ. 구성요소 / 원리
- IP 헤더의 프로토콜 번호 1로 캡슐화되어 동작
- Type(메시지 종류) + Code(세부 사유) + Checksum 구조
- 오류 보고: Destination Unreachable(Type 3), Time Exceeded(Type 11), Redirect(Type 5)
- 진단/제어: Echo Request/Reply(Type 8/0, Ping), Source Quench(혼잡)
- 오류 메시지는 원 패킷의 IP 헤더+선두 8바이트를 포함해 회신

## Ⅲ. 흐름도 / 구조
```text
[Ping] Echo Request(Type8) → [Target]
       Echo Reply(Type0)   ← 응답 → RTT 측정
[Traceroute] TTL 1,2,3.. 송신
   각 라우터: TTL=0 → Time Exceeded(Type11)
   목적지 도달: Port Unreachable(Type3)
오류: 라우터 → Destination Unreachable(Type3)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | IP 전달 오류 통지 및 도달성·경로 진단 지원 |
| 장점 | Ping/Traceroute 등 핵심 진단 도구의 기반, 경량 제어 메시지 |
| 한계 | 신뢰성·재전송 미보장, ICMP Flood·Smurf 등 DDoS 악용 및 정보 노출 위험 |

## Ⅴ. 기술사적 적용
- 네트워크 장애 1차 진단(Ping 도달성, Traceroute 경로) 표준 활용
- 보안상 경계 라우터에서 ICMP 일부 타입 필터링(스캐닝 차단)
- PMTUD(Path MTU Discovery)는 ICMP Type3/Code4(Fragmentation Needed) 의존
