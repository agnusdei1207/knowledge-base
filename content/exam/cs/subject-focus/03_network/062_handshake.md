---
title: "3/4-way 핸드셰이크 (3/4-way Handshake)"
date: "2026-06-30"
weight: 62
tags:
  - "exam-cspe-network"
---

## Ⅰ. 정의
> TCP가 연결 수립을 위해 3단계(3-way), 연결 종료를 위해 4단계(4-way) 메시지를 교환하여 양방향 통신 준비와 안전한 해제를 보장하는 절차이다.

## Ⅱ. 구성요소 / 원리
- 연결 수립(3-way): SYN → SYN+ACK → ACK 로 양측 시퀀스 동기화
- ISN(Initial Sequence Number): 각 측이 임의 초기 순서번호 교환·확인
- 연결 종료(4-way): FIN → ACK → FIN → ACK 로 양방향 독립 해제
- Half-Close: 한 방향 먼저 종료, 반대 방향은 데이터 전송 지속 가능
- 상태전이: LISTEN→SYN_RCVD→ESTABLISHED, FIN_WAIT/CLOSE_WAIT→TIME_WAIT→CLOSED

## Ⅲ. 흐름도 / 구조
```text
연결(3-way)            종료(4-way)
Client      Server     Client      Server
 |--SYN----->|          |--FIN----->|
 |<-SYN+ACK--|          |<--ACK-----|
 |--ACK----->|          |<--FIN-----|
 [ESTABLISHED]          |--ACK----->| (TIME_WAIT)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 양방향 연결 신뢰 수립과 데이터 유실 없는 안전 종료 |
| 장점 | 시퀀스 동기화로 신뢰성 확보, 독립 방향 종료 지원 |
| 한계 | 수립 지연(RTT 소요), SYN Flood 등 DoS 취약 |

## Ⅴ. 기술사적 적용
- SYN Flood 대응: SYN Cookie, 백로그 큐 튜닝으로 자원고갈 방지
- 종료 후 TIME_WAIT(2MSL) 대기로 지연패킷·재전송 처리 보장
- TCP Fast Open(TFO)으로 재연결 시 핸드셰이크 지연 감소
