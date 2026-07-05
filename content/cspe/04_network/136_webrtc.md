---
title: "WebRTC (WebRTC)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 136
---

# 📖 【암기용】 개념 완전 이해

> 목적: WebRTC를 브라우저 간 실시간 미디어·데이터 통신과 NAT traversal 구조로 이해하게 만든다.

## 한눈에
- **개요**: 브라우저·앱 간 실시간 음성·영상·데이터 통신 표준
- **왜 필요한가**: 화상회의·원격제어·라이브 협업은 서버를 경유한 지연이 사용자 체감 품질에 직접 영향을 준다. WebRTC는 가능하면 P2P로 연결하고, 불가하면 TURN relay를 사용한다.
- **핵심 직관**: 두 사용자가 직접 통화하려고 먼저 서로의 주소 후보를 교환하고, 길이 막히면 중계 교환기를 거치는 방식이다.

## 깊이 이해
- **배경·문제의식**: 대부분 단말은 NAT·방화벽 뒤에 있다. 브라우저가 상대 브라우저에 직접 UDP 패킷을 보내려면 ICE, STUN, TURN 절차가 필요하다.
- **작동 원리**: Signaling 서버가 SDP offer/answer와 ICE candidate를 교환한다. ICE는 host, server-reflexive, relay candidate를 검사해 동작하는 경로를 선택한다.
- **비유**: 모임 장소를 정할 때 집 주소, 근처 우체국 주소, 중계 사무실 주소를 모두 제출한 뒤 실제로 통하는 길을 시험하는 절차이다.
- **구체 예시**: RFC 8445 ICE는 STUN과 TURN을 활용한다. TURN RFC 8656은 직접 경로가 막힌 경우 relay 서버를 통해 미디어 패킷을 전달한다.
- **흔한 오해·주의점**: WebRTC는 signaling 프로토콜을 표준으로 고정하지 않는다. SDP 교환은 WebSocket, HTTPS, SIP 등 서비스가 직접 설계한다.

## 연결 개념
- ICE / STUN / TURN — NAT traversal 핵심 프로토콜
- DTLS-SRTP — WebRTC 미디어 암호화
- SFU / MCU — 다자 화상회의 미디어 서버 구조

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식이다.
> 핵심: WebRTC 답안은 signaling, ICE/STUN/TURN, DTLS-SRTP, SFU 운영 지표를 분리해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: WebRTC는 브라우저와 앱에서 음성·영상·데이터를 실시간으로 교환하는 P2P 기반 통신 프레임워크이다.
> 2. **가치**: ICE/STUN/TURN으로 NAT traversal을 수행하고 DTLS-SRTP로 미디어 기밀성과 무결성을 제공한다.
> 3. **판단 포인트**: 직접 연결 성공률, TURN relay 비율, packet loss, jitter, SFU egress 비용을 함께 판단한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 실시간 통신 구조 이해 확인 | signaling, SDP, ICE, STUN, TURN, DTLS-SRTP | WebRTC를 단순 영상 API로 설명 |
| NAT traversal 원리 확인 | candidate gathering, connectivity check, selected pair | STUN과 TURN 역할 혼동 |
| 운영 품질 판단 확인 | jitter, packet loss, RTT, relay ratio, SFU | QoE 지표 없이 기능만 나열 |

> 요약: 출제자는 WebRTC 연결 성립 절차와 미디어 품질 운영 지표를 함께 보길 요구한다.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **WebRTC** | WebRTC (WebRTC)의 핵심 개념 | "이 주제의 본질" |
| **프로토콜** | 통신 규칙의 표준화된 집합 | "공용 언어" |
| **패킷** | 네트워크를 통해 전송되는 데이터의 단위 | "택배 상자" |

---

## Ⅰ. 개요 및 필요성

- 개요: 브라우저 실시간 통신
- 배경: NAT·방화벽 환경에서는 단말 간 UDP 직접 연결이 항상 성립하지 않음
- 필요성: ICE/STUN/TURN과 DTLS-SRTP로 실시간 미디어 연결, 암호화, fallback을 처리함
- 판단 기준: ICE success rate, TURN relay ratio, RTT, jitter, packet loss로 서비스 품질 검증

---

## Ⅱ. 구조 및 구성요소

```text
Browser A -> Signaling Server -> Browser B
Browser A -> ICE/STUN/TURN -> Candidate Pair -> DTLS-SRTP Media Path
                         +-> SFU for multiparty session
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Signaling | SDP offer/answer와 candidate 교환 | 표준 고정 없음, 서비스가 구현 |
| ICE | 후보 경로 수집·검사·선택 | RFC 8445, STUN/TURN 활용 |
| STUN | 공인 주소와 포트 확인 | server-reflexive candidate 생성 |
| TURN | 직접 경로 실패 시 relay 제공 | 대역폭 비용과 지연 증가 |
| DTLS-SRTP | 미디어 암호화와 키 교환 | 브라우저 간 미디어 보호 |

> 요약: WebRTC는 signaling으로 협상하고 ICE/STUN/TURN으로 경로를 찾은 뒤 DTLS-SRTP로 미디어를 전달한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
getUserMedia -> SDP offer 생성 -> signaling 교환
-> ICE candidate 수집 -> STUN check / TURN fallback
-> DTLS handshake -> SRTP media / SCTP data 전송
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 미디어 장치 권한 획득과 track 생성 | permission error, device count |
| 2 | SDP offer/answer와 codec 협상 | codec, bitrate, direction 일치 |
| 3 | ICE candidate 수집과 연결성 검사 | selected candidate pair |
| 4 | DTLS handshake 후 SRTP 키 생성 | DTLS state connected |
| 5 | RTP/RTCP와 DataChannel 전송 | jitter, packet loss, RTT |

> 요약: WebRTC는 장치 획득, SDP 협상, ICE 경로 선택, DTLS-SRTP 전송 순서로 연결된다.

---

## Ⅳ. 특징

| 구분 | 서버 중계 스트리밍 | WebRTC | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 연결 방식 | 서버 중심 전달 | P2P 또는 SFU relay | 직접 연결 성공률 |
| NAT 대응 | 서버 경유로 단순화 | ICE/STUN/TURN 필요 | TURN relay ratio |
| 지연 | HLS/DASH 수초 단위 가능 | 대화형 RTT 관리 | RTT 150ms 이하 목표 |
| 보안 | TLS 전송 보호 | DTLS-SRTP 미디어 보호 | key exchange, SRTP |

> 요약: WebRTC는 대화형 지연을 목표로 하나 NAT traversal과 TURN 비용을 운영 지표로 관리해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | WebRTC | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | HLS/DASH 단방향 스트리밍 | P2P/SFU 실시간 통신 | 양방향 지연 요구 300ms 이하 |
| 비용/성능 | CDN 중심 egress | TURN/SFU egress | relay ratio와 동시 접속자 |
| 운영/위험 | 캐시·플레이어 운영 | NAT·codec·media server 운영 | 브라우저 호환성과 QoE 지표 |

> 요약: WebRTC는 양방향 지연 요구가 명확할 때 선택하고, relay 비용과 미디어 서버 용량을 사전에 산정한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 연결 실패 | symmetric NAT, UDP 차단 | TURN/TCP/TLS fallback | ICE failure rate |
| 미디어 품질 저하 | packet loss, jitter, CPU 부족 | adaptive bitrate, simulcast, FEC | MOS, jitter, loss |
| 비용 증가 | TURN relay·SFU egress 증가 | region routing, relay quota | egress GB, relay minutes |

> 요약: WebRTC 운영 리스크는 연결 실패, 미디어 품질, relay 비용으로 분리해 측정한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 연결성 | ICE success rate 98% 이상 | client telemetry |
| 품질 | packet loss 1% 이하, jitter 30ms 이하 | getStats, RTCP report |
| 비용 | TURN relay ratio 20% 이하 | TURN log, billing |

> 요약: WebRTC 성공 여부는 연결 성공률, 미디어 품질, relay 비용을 함께 충족하는지로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수):**
1. STUN/TURN 서버를 다중 리전에 배치하고 UDP 3478, TCP/TLS 443 fallback 경로를 구성한다.
2. 다자 회의는 mesh 대신 SFU 구조를 선택하고 simulcast/SVC로 단말 uplink와 CPU 사용률을 제한한다.
3. 브라우저 getStats 기반으로 RTT, jitter, packet loss, candidate pair, codec을 세션 단위로 수집한다.

**결론 (2줄):**
- 기술사 판단: 1:1·소규모 상호작용은 P2P 우선, 다자 회의와 녹화·모더레이션 요구는 SFU 중심 설계를 선택한다.
- 향후 방향: WebRTC는 실시간 협업, 원격제어, AI 상담 인터페이스의 기본 미디어 전송 계층으로 확장된다.

### 🔀 문제 유형별 목차 전환

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "WebRTC를 설명하시오" | SDP, ICE, DTLS-SRTP 연결 흐름 | 서버 중계 대비 차이 |
| 요구사항 명시형 | "화상회의 구조를 설계하시오" | SFU, TURN fallback, QoE 수집 | relay ratio, jitter, packet loss |

> 요약: 설명형은 연결 원리를, 설계형은 SFU·TURN·QoE 운영 기준을 중심으로 전환한다.
