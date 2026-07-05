---
title: "ICMP (Internet Control Message Protocol)"
date: "2026-07-05"
tags:
  - "cspe-network"
weight: 13
---

## Ⅰ. 개요
- **정의**: IP 네트워크에서 오류 보고 및 진단 메시지를 전달하는 L3 제어 프로토콜
- **배경/필요성**: IP는 비연결·비신뢰 프로토콜이므로 전송 오류나 경로 문제를 알릴 별도 메커니즘이 필요함
- **비유**: 배달 실패 시 우체국이 발신자에게 보내는 반송 사유 통지서와 유사함

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 네트워크 진단 원리 | Type/Code 체계, ping/traceroute 동작 | ICMP는 IP 위에 캡슐화되지만 L4가 아닌 L3 제어 프로토콜 |

> 요약: IP 계층의 오류·진단 정보를 전달하는 네트워크 제어 프로토콜임

## Ⅱ. 구성요소
```text
IP Header | ICMP Header (Type/Code/Checksum) | ICMP Data
             |
             +-- Type 0/8 : Echo Reply/Request
             +-- Type 3   : Destination Unreachable
             +-- Type 11  : Time Exceeded
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Type | 메시지 종류 구분 (0~255) | 반송 사유 분류 코드 |
| Code | Type 내 세부 원인 구분 | 반송 사유의 상세 항목 |
| Echo Request/Reply | 종단 간 도달 가능 여부 확인용 메시지 쌍 | "잘 들리나요?" 호출과 응답 |
| TTL Exceeded | 패킷의 홉 카운트 소진 시 라우터가 생성하는 메시지 | 배달 기한 초과 통지 |

> 요약: Type/Code 기반 메시지 분류로 오류 보고와 네트워크 진단을 수행함

## Ⅲ. 절차
```text
Host A --Echo Request(TTL=n)--> Router1 --> Router2 --> Host B
Host A <--Echo Reply------------------------------------- Host B
          (RTT 측정)
```
- 1단계: 송신 호스트가 ICMP Echo Request 생성 후 목적지로 전송
- 2단계: 중간 라우터가 TTL 감소 처리, 0 도달 시 Time Exceeded 메시지 회신
- 3단계: 목적지 호스트가 Echo Reply를 송신 호스트로 반환
- 4단계: 송신 호스트가 RTT 계산 및 도달 가능성 판정 (ping/traceroute 결과 출력)

> 요약: 요청-라우팅-응답-결과판정의 4단계로 네트워크 상태를 진단함

## Ⅳ. 문제점
- ICMP Flood: 대량 Echo Request로 대역폭을 소진함 — 별도 인증 없이 수신 측이 응답을 생성하는 구조를 악용
- Smurf 공격: 브로드캐스트 주소로 위조 출발지 Echo Request를 전송함 — 네트워크 전체가 피해 호스트에 응답을 집중
- 정보 노출: traceroute로 내부 토폴로지가 드러남 — 라우터별 TTL Exceeded 응답이 경로 정보를 외부에 공개

> 요약: 인증 부재로 DDoS 도구화 및 내부 토폴로지 노출 위험이 존재함

## Ⅴ. 개선방안
1. 단기: 방화벽에서 불필요 ICMP Type 필터링 및 Rate Limiting 적용
2. 중기: Directed Broadcast 비활성화 및 소스 IP 검증(BCP38) 적용으로 Smurf 차단
3. 장기: 내부 네트워크 ICMP 응답 정책을 세분화하여 토폴로지 노출 최소화

> 요약: 트래픽 제한, 소스 검증, 응답 정책 세분화의 단계적 방어가 필요함

## Ⅵ. 전망
- 발전 방향: ICMPv6은 NDP·PMTUD 등 필수 기능을 통합하여 완전 차단이 불가능한 구조로 전환됨
- 기술사적 판단: ICMP 허용 범위 설계는 보안과 운영 가시성 간 균형 문제임
- 기술사 제언: 보안 정책에서 ICMP를 일률 차단하지 않고 Type별 허용 정책을 수립할 필요가 있음
