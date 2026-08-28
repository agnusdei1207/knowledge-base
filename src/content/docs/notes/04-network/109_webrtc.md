---
sidebar:
  order: 109
  label: "109. WebRTC"
  badge:
    text: "기출 · 30%"
    variant: note
title: "웹 브라우저 기반 실시간 P2P 통신 : WebRTC"
date: "2026-08-26T14:20:31+09:00"
tags:
  - "notes-network"
weight: 109
extra:
  question_no: "109"
  source_status: "기출"
  source_history: "122회"
  priority: 30
  priority_note: "SDP 시그널링, NAT 통과(ICE/STUN/TURN), 보안 전송(DTLS/SRTP), 다자간 토폴로지(Mesh/SFU/MCU)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **WebRTC (Web Real-Time Communication)**: 플러그인 없이 브라우저 간에 음성, 영상, 데이터를 초저지연($\le 200\text{ms}$)으로 P2P 통신하는 W3C/IETF 오픈 표준.
- **Signaling (시그널링)**: P2P 연결 전 WebSocket/HTTPS를 통해 SDP 미디어 파라미터와 ICE 네트워크 주소 후보를 상호 교환하는 절차.

</details>

- 정의/개념: **SDP·ICE·DTLS-SRTP** 기반 브라우저 실시간 통신
- 배경/필요성: 플러그인 기반 통신과 HLS 전달은 각각 **설치 종속과 수 초 단위 버퍼 지연**을 치르므로, 브라우저에 미디어 스택을 내장하고 ICE로 NAT를 통과시켜 중계 서버 경유 구간 자체를 걷어냄

#### 한줄 요약
- 플러그인 없이 브라우저 간 초저지연 미디어 스트림과 암호화 데이터 채널을 P2P로 직접 연결한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **ICE (Interactive Connectivity Establishment)**: STUN(직접 홀펀칭)과 TURN(릴레이 중계)을 통합하여 최적의 P2P 통신 경로를 자동으로 찾아내는 프레임워크.
- **DTLS-SRTP**: UDP 상에서 DTLS 1.2/1.3 핸드셰이크로 암호키를 교환하고 오디오/비디오 페이로드를 SRTP로 고속 암호화하는 표준.

</details>

- **플러그인 없는 저지연**: 브라우저에서 200ms 이하 전송
- **ICE NAT 통과**: STUN 직접 경로와 TURN 릴레이 선택
- **필수 암호화**: 미디어 SRTP·제어 DTLS 적용

#### 한줄 요약
- 무설치 초저지연, ICE 기반 완벽한 NAT 통과, 전 구간 강제 암호화 보안을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **STUN vs TURN**: 클라이언트의 공인 IP/Port를 확인해 주는 STUN(경량)과 대칭형 NAT 환경에서 트래픽을 중계해 주는 TURN(대역폭 소모).

</details>

```text
[WebRTC 정적 구성]
|-- 시그널링 서버
|-- STUN 서버
|-- TURN 서버
|-- RTCPeerConnection
`-- RTCDataChannel
```

선의 의미: 시그널링 서버를 통해 SDP와 ICE 후보를 교환하고 STUN/TURN을 활용해 NAT를 통과한 후 브라우저 간 직결 미디어 스트림을 전송하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| 시그널링 서버 | **SDP·ICE Candidate 중계** | WebSocket / SIP |
| STUN 서버 | **NAT 공인 매핑 식별** | UDP 3478 |
| TURN 서버 | **홀펀칭 실패 시 릴레이** | UDP/TCP 3478 |
| RTCPeerConnection | **코덱·혼잡·미디어 관리** | W3C API |
| RTCDataChannel | **바이너리 데이터 전송** | SCTP over DTLS |

#### 한줄 요약
- 시그널링 서버는 연결 정보 교환까지만 관여하고 이후 미디어는 P2P 경로로 흐르므로, 서버가 감당하는 대역폭이 참가자 수에 비례하지 않는다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Trickle ICE (트릭클 ICE)**: 모든 후보 수집을 기다리지 않고 발견되는 즉시 시그널링 채널로 상대방에게 전송하여 연결 시간을 수 초 단축하는 기법.

</details>

```text
브라우저 연결 요청
    |
1. SDP Offer 전송
    |
2. SDP Answer 회신
    |
3. Trickle ICE 후보 교환
    |
4. ICE 연결성 검사
    +-- 실패: TURN 릴레이
    |
5. DTLS-SRTP 스트리밍
    |
실시간 미디어
```

- 1. SDP Offer 전송
- 2. SDP Answer 회신
- 3. Trickle ICE 후보 교환
- 4. ICE 연결성 검사
- 5. DTLS-SRTP 스트리밍

#### 한줄 요약
- ICE 연결성 검사 결과에서 P2P 직결과 TURN 중계로 갈리며, 후자는 서버 대역폭 비용을 치르고 연결 성공률을 사들인다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Mesh vs SFU vs MCU**: P2P 직결, 중앙 패킷 라우터(SFU), 중앙 미디어 믹싱 서버(MCU).

</details>

| 비교 항목 | P2P 풀 메시 (Mesh) | SFU (Selective Forwarding Unit) | MCU (Multipoint Control Unit) |
|:---|:---|:---|:---|
| 서버 역할 | **없음** | **패킷 라우팅** | **디코딩·합성·인코딩** |
| 단말 업링크 부하 | $N-1$ | **1개** | **1개** |
| 단말 다운링크 부하 | $N-1$ | $N-1$ | **1개 합성본** |
| 서버 CPU 연산 부하 | **없음** | **낮음** | **매우 높음** |
| 지연 시간 | **100ms 이하** | **200ms 이하** | 300~500ms |
| 주요 적용 분야 | 소규모 통화 | **대규모 회의** | 저사양 단말 |

#### 한줄 요약
- P2P Mesh는 1:1용, SFU는 대규모 다자간 표준(라우팅 위주), MCU는 레거시 단말용(서버 합성)이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Simulcast (사이멀캐스트)**: 송신 단말이 고/중/저 3개 해상도를 동시 송출하고, SFU 서버가 수신자의 대역폭에 맞춰 최적 화질을 동적 선별 전송하는 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 대칭 NAT에서 홀펀칭 실패 | **TURN TLS 443 릴레이** | 연결성 확보 |
| 무선망 저하로 영상 끊김 | **Simulcast·SFU 비트레이트** | 화질 적응 |
| ICE 후보 수집 지연 | **Trickle ICE** | 연결 시간 단축 |
| 지터·손실로 음성 왜곡 | **NetEQ·Opus FEC** | 음성 품질 유지 |

#### 한줄 요약
- TURN 폴백으로 연결성을 확보하고, Simulcast로 화질을 최적화하며, Trickle ICE로 셋업 시간을 단축한다.

## Ⅶ. 결론

- 소규모는 **Mesh**, 대규모 회의는 **SFU·Simulcast·TURN** 선택

#### 한줄 요약
- WebRTC는 플러그인 없이 브라우저 간 초저지연 P2P 통신을 지원하며 SFU 및 TURN과 결합하여 대규모 글로벌 실시간 통신을 실현한다.
