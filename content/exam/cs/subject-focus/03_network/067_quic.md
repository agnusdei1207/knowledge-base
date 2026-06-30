---
title: "QUIC (Quick UDP Internet Connections)"
date: "2026-06-30"
weight: 67
tags:
  - "exam-cspe-network"
---

## Ⅰ. 1교시 핵심 답안

> QUIC은 UDP 기반 위에 신뢰성, 혼잡 제어, TLS 1.3, 다중 스트림을 통합한 차세대 전송 프로토콜로, HTTP/3의 기반이 된다.

- **핵심 특징**: `1-RTT/0-RTT`, `Multiplexing`, `TLS 1.3`, `Connection ID`
- **목적**: 지연 단축, HOL Blocking 완화, 모바일 이동성 강화
- **기반**: UDP + 사용자 공간 구현
- **출제 포인트**: TCP+TLS 대비 개선점

## Ⅱ. 구조 및 동작 원리

```text
HTTP/3
  |
 QUIC  = Stream + Reliability + TLS 1.3
  |
 UDP
  |
 IP
```

- **0/1-RTT**: 연결 수립 지연 감소
- **독립 스트림**: 일부 손실이 전체 스트림 정지를 유발하지 않음
- **Connection ID**: IP 변경 시에도 연결 유지
- **사용자 공간 구현**: 커널 업데이트 없이 빠른 진화 가능

## Ⅲ. 비교표

| 구분 | TCP + TLS | QUIC |
|:---|:---|:---|
| 연결 수립 | 단계적 | 통합형 |
| HOL 문제 | TCP 수준 존재 | 스트림 단위 완화 |
| 이동성 | IP 변경에 취약 | Connection Migration 지원 |
| 배치 | 커널 의존 큼 | 사용자 공간 구현 가능 |

## Ⅳ. 기술사 답안 포인트

- **웹 성능**: HTTP/3와 결합하여 초기 응답 지연 단축
- **모바일 환경**: Wi-Fi/LTE 전환 시 세션 지속성 우수
- **보안**: TLS 1.3 내장으로 암호화 기본화
- **한계**: UDP 차단 정책, 운영 가시성, CPU 부담

## Ⅴ. 결론

QUIC의 핵심은 UDP 사용 자체보다 `전송·보안·다중화를 하나로 묶어 지연을 줄인 구조`에 있다.  
QUIC은 UDP 위에서 TLS 1.3, 신뢰성, 혼잡 제어, 독립 스트림을 통합해 연결 수립 지연과 HOL Blocking을 줄인다. HTTP/3 환경에서는 모바일 이동성, 사용자 공간 배포, 보안 기본화를 통해 웹 전송 구조를 개선한다.
