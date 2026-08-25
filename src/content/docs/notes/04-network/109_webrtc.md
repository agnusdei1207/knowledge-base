---
sidebar:
  order: 109
  label: "109. WebRTC"
  badge:
    text: "기출 · 30%"
    variant: note
title: "웹 브라우저 기반 실시간 P2P 통신 : WebRTC"
date: "2026-08-25T12:00:00+09:00"
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

- 정의/개념: 브라우저 간에 **SDP 시그널링, ICE/STUN/TURN NAT 트래버설, DTLS-SRTP 암호화를 통해 초저지연 실시간 미디어를 P2P 전송하는 프레임워크**
- 배경/필요성: 액티브X/플러그인 의존성과 HLS/DASH의 수 초 전송 지연으로 인한 **실시간 양방향 대화 불가 및 모바일 웹 호환성 단절**

#### 한줄 요약
- 플러그인 없이 브라우저 간 초저지연 미디어 스트림과 암호화 데이터 채널을 P2P로 직접 연결한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **ICE (Interactive Connectivity Establishment)**: STUN(직접 홀펀칭)과 TURN(릴레이 중계)을 통합하여 최적의 P2P 통신 경로를 자동으로 찾아내는 프레임워크.
- **DTLS-SRTP**: UDP 상에서 DTLS 1.2/1.3 핸드셰이크로 암호키를 교환하고 오디오/비디오 페이로드를 SRTP로 고속 암호화하는 표준.

</details>

- **플러그인 프리(Plugin-Free) 초저지연**: 별도 설치 없이 브라우저 네이티브로 **지연 시간 200ms 이하 실시간 음성/영상 전송**
- **강력한 NAT/방화벽 통과(ICE Framework)**: STUN 홀펀칭과 TURN 릴레이를 결합하여 **복잡한 사설망 환경에서도 100% 연결 보장**
- **기본 암호화 보안(Mandatory Encryption)**: 미디어는 **SRTP, 제어/데이터는 DTLS로 전 구간 필수 암호화 통신 강제**

#### 한줄 요약
- 무설치 초저지연, ICE 기반 완벽한 NAT 통과, 전 구간 강제 암호화 보안을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **STUN vs TURN**: 클라이언트의 공인 IP/Port를 확인해 주는 STUN(경량)과 대칭형 NAT 환경에서 트래픽을 중계해 주는 TURN(대역폭 소모).

</details>

```text
[WebRTC 시그널링 및 P2P 미디어 연결 아키텍처]
|-- Browser A (Caller: SDP Offer 생성, Local ICE Candidates 수집)
`-- Signaling Server (WebSocket / HTTPS: SDP 및 ICE 정보 중계)
`-- Browser B (Callee: SDP Answer 생성, Remote ICE Candidates 교환)
`-- STUN / TURN Infrastructure
|   |-- STUN Server (RFC 5389: 공인 IP/Port 매핑 반환)
|   `-- TURN Server (RFC 5766: Symmetric NAT 환경 릴레이 중계)
`-- Direct P2P Media Stream (DTLS-SRTP: Audio Opus, Video VP9/AV1, RTCDataChannel SCTP)
```

선의 의미: 시그널링 서버를 통해 SDP와 ICE 후보를 교환하고 STUN/TURN을 활용해 NAT를 통과한 후 브라우저 간 직결 미디어 스트림을 전송하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **시그널링 서버** | SDP Offer/Answer 및 **ICE Candidate 정보를 양 브라우저 간에 중계 교환** | WebSocket / SIP |
| **STUN 서버 (RFC 5389)**| 클라이언트의 **NAT 매핑 공인 IP/Port(Server Reflexive)를 식별하여 회신** | UDP 3478 |
| **TURN 서버 (RFC 5766)**| P2P 홀펀칭 실패 시 **미디어 패킷을 양방향 릴레이 중계 (최후 수단)** | UDP/TCP 3478 |
| **RTCPeerConnection** | 오디오/비디오 스트림 생애주기 관리, **코덱 협상, 혼잡 제어(GCC/BWE) 수행** | W3C API |
| **RTCDataChannel** | 게이밍, 파일 공유용 **임의 바이너리 데이터를 신뢰/비신뢰 모드로 전송** | SCTP over DTLS |

#### 한줄 요약
- 시그널링 서버, STUN/TURN 서버, RTCPeerConnection, RTCDataChannel이 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Trickle ICE (트릭클 ICE)**: 모든 후보 수집을 기다리지 않고 발견되는 즉시 시그널링 채널로 상대방에게 전송하여 연결 시간을 수 초 단축하는 기법.

</details>

```text
WebRTC SDP 협상, Trickle ICE 후보 교환 및 DTLS-SRTP 파이프라인
        │
   1. [SDP Offer 생성 및 전송] 브라우저 A가 미디어 능력을 기술한 SDP Offer를 시그널링 서버로 전송
        │
   2. [SDP Answer 생성 및 회신] 브라우저 B가 수신 후 자신의 능력을 담은 SDP Answer를 회신
        │
   3. [Trickle ICE 후보 교환] 양단이 STUN/TURN 서버와 통신하여 ICE 후보를 비동기 점진 교환
        │
   4. [ICE 연결성 검사] STUN Binding Request로 P2P 경로를 검사하고 최적 경로 결정
        │
   ├─ [홀펀칭 실패 시] ➔ TURN 릴레이 경로로 자동 전환
   ▼
5. [DTLS 키 교환 및 미디어 스트리밍] DTLS 핸드셰이크로 SRTP 키 유도 후 암호화 미디어 초저지연 전송
```

#### 한줄 요약
- SDP Offer/Answer 협상 → Trickle ICE 후보 수집 → STUN 연결성 검사 → DTLS 키 교환 → SRTP 암호화 스트리밍 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Mesh vs SFU vs MCU**: P2P 직결, 중앙 패킷 라우터(SFU), 중앙 미디어 믹싱 서버(MCU).

</details>

| 비교 항목 | P2P 풀 메시 (Mesh) | SFU (Selective Forwarding Unit) | MCU (Multipoint Control Unit) |
|:---|:---|:---|:---|
| **서버 역할** | **서버 불필요 (단말 간 직접 교환)** | **미디어 디코딩 없이 패킷 라우팅만 수행** | **미디어 완전 디코딩, 합성/인코딩 후 전송**|
| **단말 업링크 부하** | $N-1$개 스트림 송신 (참여자 증가 시 폭발)| **단 1개 스트림만 서버로 송신** | **단 1개 스트림만 서버로 송신** |
| **단말 다운링크 부하**| $N-1$개 스트림 수신 | $N-1$개 스트림 수신 (Simulcast 최적화) | **합성된 단 1개 스트림만 수신** |
| **서버 CPU 연산 부하**| **0% (서버 미사용)** | **매우 낮음 (단순 패킷 복사 및 포워딩)**| **매우 높음 (수십 채널 비디오 믹싱/트랜스코딩)**|
| **지연 시간 (Latency)**| **$\le 100\text{ms}$ (초극저지연)** | **$\le 200\text{ms}$ (실시간 대화 최적)** | $300\sim 500\text{ms}$ (합성 렌더링 지연)|
| **주요 적용 분야** | 1:1 통화, 3~4인 소규모 화상 회의 | **Zoom, Google Meet, 대규모 세미나**| 레거시 하드웨어 화상 장비, 저사양 단말 환경 |

#### 한줄 요약
- P2P Mesh는 1:1용, SFU는 대규모 다자간 표준(라우팅 위주), MCU는 레거시 단말용(서버 합성)이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Simulcast (사이멀캐스트)**: 송신 단말이 고/중/저 3개 해상도를 동시 송출하고, SFU 서버가 수신자의 대역폭에 맞춰 최적 화질을 동적 선별 전송하는 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 엄격한 기업 방화벽/Symmetric NAT에서 P2P 홀펀칭 실패로 인한 **통화 실패** | **`글로벌 TURN 서버 클러스터(TLS 443 TCP 릴레이 지원)`** 구축 | 100% 통화 연결 성공률(Reachability) 확보 |
| 모바일 수신자의 무선망 저하 시 다자 회의 전체 비디오 끊김 발생 | **`Simulcast(다중 해상도 동시 송출)` 및 SFU 동적 비트레이트 조절** | 저대역폭 사용자 맞춤 서빙으로 통화 연속성 보장 |
| ICE 후보 수집 완료 대기로 인한 초기 연결 지연($\sim 3\text{초}$) 발생 | **`트릭클 ICE(Trickle ICE) 비동기 후보 전송`** 적용 | 초기 연결 수립 시간 500ms 이내로 단축 |
| 음성 패킷 지터 및 네트워크 버퍼링으로 인한 오디오 끊김/왜곡 | **`적응형 지터 버퍼(NetEQ) 및 Opus FEC(전방 오류 정정)`** 활성화 | 패킷 손실률 20% 환경에서도 명료한 음성 통화 품질 유지 |

#### 한줄 요약
- TURN 폴백으로 연결성을 확보하고, Simulcast로 화질을 최적화하며, Trickle ICE로 셋업 시간을 단축한다.

## Ⅶ. 결론

- 비대면 원격 협업, 텔레헬스 및 메타버스 플랫폼의 실시간 상호작용을 구현하기 위해 **WebRTC 아키텍처를 인터랙티브 미디어 표준으로 채택**하되, 엔터프라이즈 환경에서의 안정적인 서비스를 위해 **SFU 기반 대규모 미디어 라우팅, 글로벌 Anycast TURN 릴레이 인프라, Simulcast 및 AV1 차세대 코덱**을 통합 구현하여 초저지연·고화질 실시간 통신 환경 완성

#### 한줄 요약
- WebRTC는 플러그인 없이 브라우저 간 초저지연 P2P 통신을 지원하며 SFU 및 TURN과 결합하여 대규모 글로벌 실시간 통신을 실현한다.