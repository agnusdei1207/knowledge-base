---
sidebar:
  order: 109
  label: "109. WebRTC (WebRTC)"
  badge:
    text: "기출 · 30%"
    variant: note
title: "웹 브라우저 기반 실시간 P2P 통신 : WebRTC (Web Real-Time Communication)"
date: "2026-08-22T08:15:00+09:00"
tags: ["notes-network"]
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

- **WebRTC(Web Real-Time Communication)**: 별도의 플러그인(ActiveX/플래시)이나 애플리케이션 설치 없이, 표준 웹 브라우저 간에 오디오, 비디오, 임의의 바이너리 데이터를 초저지연(Sub-500ms)으로 실시간 P2P 암호화 통신할 수 있도록 W3C와 IETF가 공동 표준화한 오픈 프레임워크 (RFC 8825).
- **시그널링(Signaling)**: P2P 미디어 스트림이 시작되기 전에, 양 브라우저 간에 세션 제어 메시지(미디어 코덱, 해상도, 암호화 키, 네트워크 IP/Port 후보)를 교환하는 대역 외(Out-of-Band) 사전 협상 프로세스 (WebSocket, SIP, HTTPS 활용).

</details>

- 정의/개념: 브라우저 간에 **SDP(Session Description Protocol)** 를 교환하는 **시그널링 계층** 과, NAT/방화벽을 극복하는 **ICE/STUN/TURN 프레임워크**, 미디어 및 데이터를 암호화 전송하는 **DTLS-SRTP 및 SCTP 데이터 채널** 로 구성된 **실시간 멀티미디어 통신 아키텍처**
- 배경/필요성: 브라우저 기반의 화상 회의, 원격 진료, 클라우드 게이밍에서 기존 HTTP 폴링/스트리밍의 수 초 단위 전송 지연과 사설망(NAT) 환경에서의 P2P 연결 실패 한계를 극복할 요구

#### 한줄 요약
- 플러그인 없이 브라우저 간에 SDP 시그널링과 ICE NAT 통과를 통해 실시간 미디어를 P2P 암호화 전송한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **ICE(Interactive Connectivity Establishment, RFC 8445)**: 호스트의 사설 IP(Host Candidate), STUN 서버가 식별한 공인 IP(Server Reflexive Candidate), TURN 중계 서버 IP(Relay Candidate)를 모두 수집하여 우선순위 기반으로 최적의 P2P 통신 경로를 자동 수립하는 NAT 트래버설 프레임워크.
- **DTLS-SRTP(RFC 5763 / 5764)**: UDP 상에서 TLS 핸드셰이크를 수행하여 종단 간 상호 인증 및 마스터 키를 합의(DTLS)한 후, 오디오/비디오 RTP 패킷을 AES 암호화(SRTP)하여 도청을 원천 차단하는 보안 전송 프로토콜.

</details>

- **플러그인 프리(Plugin-Free) 표준 웹 API 지원**: HTML5 `<video>`, `getUserMedia()`, `RTCPeerConnection` 네이티브 제공
- **지능형 다계층 NAT 트래버설 (ICE/STUN/TURN)**: 사설 IP 간 직결 $\rightarrow$ 공유기 공인 IP 홀펀칭 $\rightarrow$ 방화벽 차단 시 TURN 릴레이 순으로 100% 연결 성공률 보장
- **기본 내장된 엔드투엔드 암호화 (E2EE)**: 미디어 스트림은 DTLS-SRTP, 제어/데이터는 DTLS/SCTP로 전 구간 필수 암호화 강제

#### 한줄 요약
- 무설치 웹 API, ICE 기반 다계층 NAT 홀펀칭, DTLS-SRTP 전 구간 암호화를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **STUN(Session Traversal Utilities for NAT, RFC 5389)**: 클라이언트가 자신의 공유기(NAT) 외부에 매핑된 공인 IP와 포트 번호를 질의하여 획득하는 경량 프로토콜.
- **TURN(Traversal Using Relays around NAT, RFC 5766)**: 대칭형 NAT(Symmetric NAT)이나 엄격한 기업 방화벽으로 인해 P2P 직결이 불가능할 때 미디어 트래픽을 중계해 주는 릴레이 서버.

</details>

```text
[ 브라우저 A (Caller) ] <════ (1. 시그널링: SDP Offer/Answer 교환) ════> [ 브라우저 B (Callee) ]
          │ (WebSocket / HTTPS)                                                   │
          ├──────────────────────────┐                    ┌───────────────────────┤
          ▼                          ▼                    ▼                       ▼
   [ STUN 서버 ]              [ TURN 릴레이 서버 ] ◀═══════════╝            [ STUN 서버 ]
 (공인 IP/Port 반환)         (Symmetric NAT 우회 중계)                     (공인 IP/Port 반환)
          │                                                                       │
          └──────────────── (2. ICE 홀펀칭 성공 시 P2P 직결) ─────────────────────┘
                             ├─ 미디어 스트림: SRTP (Audio: Opus, Video: VP9/AV1)
                             └─ 데이터 채널: SCTP over DTLS (바이너리/텍스트)
```

선의 의미: 시그널링 서버를 통해 SDP와 ICE 후보를 교환하고, STUN/TURN을 활용해 NAT를 통과한 후 브라우저 간 DTLS-SRTP 직결 미디어 스트림을 전송하는 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **시그널링 서버** | SDP Offer/Answer 및 ICE Candidate 정보를 양 브라우저 간에 중계 교환 | WebSocket / SIP |
| **STUN 서버 (RFC 5389)**| 클라이언트의 NAT 매핑 공인 IP/Port(Server Reflexive)를 식별하여 회신 | UDP 3478 |
| **TURN 서버 (RFC 5766)**| P2P 홀펀칭 실패 시 미디어 패킷을 양방향 릴레이 중계 (최후 수단) | UDP/TCP 3478 |
| **RTCPeerConnection** | 오디오/비디오 스트림 생애주기 관리, 코덱 협상, 혼잡 제어(GCC/BWE) 수행 | W3C API |
| **RTCDataChannel** | 게이밍, 파일 공유, 채팅용 임의 바이너리 데이터를 신뢰/비신뢰 모드로 전송 | SCTP over DTLS |

#### 한줄 요약
- 시그널링 서버, STUN/TURN 서버, RTCPeerConnection, RTCDataChannel이 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **트릭클 ICE(Trickle ICE)**: 모든 ICE 후보(Candidate) 수집이 끝날 때까지 기다리지 않고, 발견되는 즉시 시그널링 채널을 통해 상대방에게 점진적으로 전송하여 연결 수립 지연을 수초 단축하는 최적화 기법.

</details>

```text
1. 브라우저 A가 'RTCPeerConnection'을 생성하고 미디어 능력을 기술한 SDP Offer 생성
            │
            ▼
2. 시그널링 서버(WebSocket)를 통해 브라우저 B로 SDP Offer 전송 ➔ 브라우저 B가 SDP Answer 생성 및 회신
            │
            ▼
3. 양 브라우저가 STUN/TURN 서버와 통신하여 ICE 후보(Host, Srflx, Relay)를 비동기 수집(Trickle ICE)
            │
            ▼
4. 양단 간 ICE 연결성 검사(Connectivity Check: STUN Binding Request) 병렬 수행 ➔ 최적 P2P 경로 결정
            │
            ├─ [직접 P2P 실패 / Symmetric NAT] ➔ TURN 릴레이 경로로 자동 전환
            ▼
5. [연결 확정] ➔ DTLS 1.2/1.3 핸드셰이크로 SRTP 키 교환 완료 ➔ 암호화된 오디오/비디오 초저지연 실시간 송수신
```

**동작 원리**

1. **미디어 협상**: SDP를 통해 사용할 코덱(Opus, H.264, VP9), 해상도, 대역폭 사전 조율
2. **후보 탐색**: 로컬 인터페이스, STUN 공인 IP, TURN 릴레이 엔드포인트를 실시간 추출
3. **연결성 평가**: 우선순위가 높은 직접 경로(Host $\rightarrow$ Srflx $\rightarrow$ Relay) 순으로 핑/바인딩 검사
4. **암호화 핸드셰이크**: UDP 패킷 상에서 DTLS 핸드셰이크를 완료하여 마스터 비밀키 유도
5. **적응형 스트리밍**: 구글 혼잡 제어(GCC) 알고리즘이 네트워크 대역폭을 실시간 추정하여 비트레이트 조절

#### 한줄 요약
- SDP Offer/Answer 협상, Trickle ICE 후보 수집, STUN 연결성 검사, DTLS 키 교환, SRTP 암호화 스트리밍 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **다자간 화상 회의 아키텍처 비교**: P2P Mesh, SFU(선택적 전달 유닛), MCU(다중점 제어 유닛)의 서버 부하 및 대역폭 비교.

</details>

| 비교 항목 | P2P 풀 메시 (Mesh) | SFU (Selective Forwarding Unit) | MCU (Multipoint Control Unit) |
|:---|:---|:---|:---|
| **서버 역할** | **서버 불필요 (단말 간 직접 교환)** | **미디어 디코딩 없이 패킷 라우팅만 수행** | **미디어 완전 디코딩, 합성/인코딩 후 전송**|
| **단말 업링크 부하** | $N-1$개 스트림 송신 (참여자 증가 시 폭발)| **단 1개 스트림만 서버로 송신** | **단 1개 스트림만 서버로 송신** |
| **단말 다운링크 부하**| $N-1$개 스트림 수신 | $N-1$개 스트림 수신 (Simulcast 최적화) | **합성된 단 1개 스트림만 수신** |
| **서버 CPU 연산 부하**| **0% (서버 미사용)** | **매우 낮음 (단순 패킷 복사 및 포워딩)**| **매우 높음 (수십 채널 비디오 믹싱/트랜스코딩)**|
| **지연 시간 (Latency)**| **$\le 100\text{ms}$ (초극저지연)** | **$\le 200\text{ms}$ (실시간 대화 최적)** | $300\sim 500\text{ms}$ (합성 렌더링 지연)|
| **주요 적용 분야** | 1:1 통화, 3~4인 소규모 화상 회의 | **Zoom, Google Meet, 수백 명 대규모 세미나**| 레거시 하드웨어 화상 장비, 저사양 단말 환경 |

#### 한줄 요약
- P2P Mesh는 1:1용, SFU는 대규모 다자간 표준(라우팅 위주), MCU는 레거시 단말용(서버 합성)이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **사이멀캐스트(Simulcast)**: 송신 단말이 고화질(1080p), 중간화질(720p), 저화질(360p)의 3가지 해상도 스트림을 동시 송출하고, SFU 서버가 수신 단말의 네트워크 대역폭에 맞춰 적절한 화질을 선택 포워딩하는 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 엄격한 기업 방화벽/Symmetric NAT 환경에서 P2P 홀펀칭 실패로 인한 **통화 연결 실패** | 전 세계 분산 **TURN 서버 클러스터 구축(TLS 443 TCP 릴레이 폴백 지원)** | 100% 통화 연결 성공률(Reachability) 확보 |
| 모바일 수신자의 무선망 품질 저하 시 다자 회의 전체 비디오 끊김 및 버퍼링 발생 | **Simulcast(다중 해상도 동시 송출) 및 SFU 기반 동적 비트레이트 조절** | 저대역폭 사용자에게 저화질 스트림을 맞춤 서빙하여 통화 연속성 보장 |
| ICE 후보 수집 완료 대기로 인한 초기 통화 연결 지연($\sim 3\text{초}$) 발생 | **트릭클 ICE(Trickle ICE) 비동기 후보 전송 기법** 적용 | 초기 연결 수립 시간(Call Setup Latency) 500ms 이내로 단축 |

#### 한줄 요약
- TURN 폴백으로 연결성을 확보하고, Simulcast로 화질을 최적화하며, Trickle ICE로 셋업 시간을 단축한다.

## Ⅶ. 결론

- 비대면 원격 협업, 텔레헬스 및 메타버스 플랫폼의 실시간 상호작용을 구현하기 위해 **WebRTC 아키텍처**는 핵심 표준으로 자리 잡았으며, 엔터프라이즈 환경에서의 안정적인 서비스를 위해 **SFU 기반 대규모 미디어 라우팅**, **글로벌 Anycast TURN 릴레이 인프라**, **Simulcast 및 AV1 차세대 코덱**을 통합 구현하여 초저지연·고화질 실시간 통신 환경을 완성

#### 한줄 요약
- WebRTC와 SFU 라우팅 및 TURN 인프라를 결합하여 고품질 글로벌 실시간 P2P/다자간 통신을 실현한다.
