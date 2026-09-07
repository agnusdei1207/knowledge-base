---
sidebar:
  order: 109
  label: "109. WebRTC"
  badge:
    text: "기출 · 30%"
    variant: note
title: "웹 브라우저 기반 실시간 P2P 통신 : WebRTC"
date: "2026-09-07T14:00:00+09:00"
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
- 배경/필요성: 과거 웹 환경에서 실시간 음성/영상 통신을 구현하기 위해 Flash나 ActiveX 같은 서드파티 플러그인을 설치해야 했던 보안 취약점 및 플랫폼 종속성 문제와, HTTP 기반 스트리밍(HLS/DASH)의 수 초~수십 초 단위 청크 버퍼링 지연(High Latency) 한계를 극복하기 위해, 별도의 플러그인 설치 없이 웹 표준 브라우저 간에 초저지연($\le 200ms$)으로 미디어 및 데이터 스트림을 P2P로 직접 전송하는 WebRTC(Web Real-Time Communication) 표준을 도입하여 **무설치 크로스 플랫폼 실시간 통신 환경 구축, SDP/ICE(STUN/TURN) 기반 완벽한 NAT/방화벽 통과 및 DTLS-SRTP 전 구간 기본 암호화**를 달성할 필요

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
[WebRTC 통신 구조]
  │
  ├─ [세션 제어 평면]
  │    ├─ 시그널링 서버 (SDP 교환)
  │    └─ ICE 프레임워크 (경로 결정)
  │
  ├─ [NAT/방화벽 탐색]
  │    ├─ STUN 서버 (공인 IP 매핑)
  │    └─ TURN 서버 (릴레이 중계)
  │
  └─ [데이터·미디어 평면]
       ├─ RTCPeerConnection (SRTP 미디어)
       └─ RTCDataChannel (SCTP/DTLS)
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| **시그널링 서버** | SDP·**ICE Candidate 중계** |
| **STUN 서버** | NAT **공인 매핑 식별** |
| **TURN 서버** | 홀펀칭 실패 시 **릴레이** |
| **RTCPeerConnection** | 코덱·혼잡·**미디어 관리** |
| **RTCDataChannel** | **바이너리 데이터** 전송 |

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

- 플러그인 없는 웹 브라우저 표준 기술로서 화상회의(Zoom/Meet), 원격 진료, 클라우드 게이밍 및 메타버스 실시간 인터랙션을 지탱하는 **글로벌 실시간 인터랙티브 미디어 통신의 핵심 표준 프레임워크(W3C/IETF)**로 확립되었으며, QUIC 기반 WebTransport 및 차세대 미디어 코덱(AV1)과의 융합으로 진화하는 가운데, 실무 대규모 WebRTC 서비스 아키텍처 구축 시에는 **1:1 통화용 P2P 풀 메시를 넘어 수백 명 다자간 화상회의를 지원하는 SFU(Selective Forwarding Unit) 라우팅 서버 구축, 네트워크 대역폭에 따른 화질 적응을 보장하는 사이멀캐스트(Simulcast) 적용, 엄격한 기업 대칭형 NAT/방화벽을 100% 우회하는 글로벌 Anycast TURN(TLS 443) 릴레이 클러스터**를 결합하여 완벽한 실시간 연결성을 완성

#### 한줄 요약
- WebRTC는 플러그인 없이 브라우저 간 초저지연 P2P 통신을 지원하며 SFU 및 TURN과 결합하여 대규모 글로벌 실시간 통신을 실현한다.
