---
sidebar:
  order: 103
  label: "103. RoCE — RDMA over Converged Ethernet"
  badge:
    text: "미출 · 50%"
    variant: note
title: "이더넷 기반 무손실 고속 전송 : RoCE 및 RoCEv2"
date: "2026-08-26T14:12:14+09:00"
tags:
  - "notes-network"
weight: 103
extra:
  question_no: "103"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "RoCEv1(L2) vs RoCEv2(L3 UDP 4791), 무손실 이더넷(PFC/IEEE 802.1Qbb), ECN/DCQCN 혼잡 제어"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **RoCE (RDMA over Converged Ethernet)**: 범용 이더넷 상에서 InfiniBand 전송 계층 패킷을 캡슐화하여 RDMA를 제공하는 기술 (IBTA 표준).
- **RoCEv2 (Routable RoCE)**: IP 및 UDP 헤더(포트 4791)로 패킷을 캡슐화하여 대규모 L3 패브릭 라우팅을 지원하는 차세대 표준.

</details>

- 정의/개념: UDP 4791과 **PFC·ECN**으로 L3를 지원하는 이더넷 RDMA
- 배경/필요성: InfiniBand는 성능을 얻는 대신 **전용 스위치·케이블 비용과 기존 이더넷 비호환**을 치르므로, RDMA 전송을 UDP/IP에 캡슐화해 이미 깔린 이더넷 위에서 L3 라우팅까지 확장

#### 한줄 요약
- 범용 이더넷 상에서 무손실 흐름 제어와 UDP 캡슐화를 통해 L3 확장형 초저지연 RDMA를 구현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Lossless Ethernet (무손실 이더넷)**: 패킷 드롭이 발생하면 성능이 급락하는 RDMA를 위해 L2 PFC와 L3 ECN으로 버퍼 오버플로우를 원천 방지하는 네트워크.
- **DCQCN (Data Center QCN)**: 스위치의 ECN 마킹과 수신단의 CNP 알림을 기반으로 송신단 전송률을 동적 조절하는 혼잡 제어 알고리즘.

</details>

- **L3 라우팅**: UDP 4791로 리프-스파인 패브릭 지원
- **PFC 무손실 큐**: 버퍼 고갈 전에 우선순위 PAUSE 수행
- **DCQCN**: ECN·CNP 피드백으로 전송률 조절

#### 한줄 요약
- L3 라우팅 지원, PFC 무손실 보장, DCQCN 하드웨어 혼잡 제어를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **PFC vs ECN**: 버퍼 고갈 시 L2 PAUSE 프레임으로 송신을 일시 중단시키는 하드웨어 차단(PFC)과 버퍼 임계치 초과 시 IP 헤더 비트를 마킹하는 선제 제어(ECN).

</details>

```text
[RoCEv2 정적 구성]
|-- RoCEv2 RNIC
|-- PFC 제어기
|-- ECN 마킹 엔진
|-- CNP 생성기
`-- ECMP 패브릭
```

선의 의미: RoCEv2 데이터 패킷이 스위치 패브릭에서 ECN 마킹을 거쳐 수신단에 도착하고 수신 RNIC가 생성한 CNP 피드백을 통해 송신단이 레이트를 조절하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| RoCEv2 RNIC | **UDP 캡슐화·DCQCN 제어** | ConnectX |
| PFC 제어기 | **802.1Qbb PAUSE 전송** | Lossless Queue |
| ECN 마킹 엔진 | **혼잡 패킷 CE 마킹** | RFC 3168 |
| CNP 생성기 | **CE 감지·CNP 회신** | Congestion Signal |
| ECMP 패브릭 | **엔트로피 기반 경로 분산** | Load Balancing |

#### 한줄 요약
- PFC가 손실을 막는 최후 방어를 맡고 ECN·CNP가 그 정지 신호에 이르기 전에 송신 속도를 낮추므로, 무손실 유지와 데드락 회피가 서로 다른 계층에 나뉘어 담긴다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **CNP (Congestion Notification Packet)**: 수신 호스트 RNIC가 ECN 마킹을 감지했을 때 송신 호스트를 향해 전송 속도를 줄이라고 역방향으로 보내는 경보 패킷.

</details>

```text
GPU 전송 요청
    |
1. RoCEv2 패킷 송출
    |
2. ECN 선제 마킹
    |
3. CNP 역전송
    |
4. DCQCN 전송률 감속
    |
5. PFC 최후 방어
    |
수신 완료
```

- 1. RoCEv2 패킷 송출
- 2. ECN 선제 마킹
- 3. CNP 역전송
- 4. DCQCN 전송률 감속
- 5. PFC 최후 방어

#### 한줄 요약
- ECN 기반 감속이 먼저 반응하고 PFC는 그 뒤에야 동작하므로, DCQCN 조정이 늦을수록 무손실은 지켜도 데드락 위험을 대가로 치른다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **RoCEv1 (L2)** vs **RoCEv2 (L3 UDP/IP)** vs **Native InfiniBand**.

</details>

| 비교 항목 | RoCEv1 (IB over L2 Ethernet) | RoCEv2 (IB over UDP/IP) | 네이티브 인피니밴드 (InfiniBand) |
|:---|:---|:---|:---|
| 캡슐화 계층 | **L2 이더넷** | **UDP/IP 4791** | **InfiniBand 프레임** |
| L3 라우팅 지원 | **불가** | **지원** | 별도 라우터 필요 |
| 혼잡 제어 방식 | PFC | **ECN·CNP·DCQCN·PFC** | **Credit 기반** |
| 초기 구축 비용 | 낮음 | **낮음** | **매우 높음** |
| 주요 적용 영역 | 단일 랙 | **대규모 AI 패브릭** | HPC |

#### 한줄 요약
- RoCEv1은 소규모 L2 단일 랙용, RoCEv2는 초대규모 AI 클러스터 표준, InfiniBand는 최고 성능 전용망이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **PFC Deadlock**: 링 토폴로지나 버퍼 순환 구조에서 스위치들이 서로를 향해 PAUSE 프레임을 영구 전송하여 트래픽이 완전 마비되는 교착 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| PFC PAUSE에 따른 데드락·HoL | **데드락 워치독·ECN 튜닝** | 큐 교착 복구 |
| GPU 인캐스트로 버퍼 손실 | **WRED·ECN·DCQCN** | 버퍼 폭주 방지 |
| ECMP 경로 핫스팟 | **5-Tuple 엔트로피 해싱** | 경로 부하 분산 |
| Go-Back-N 재전송 비용 | **선택적 재전송 RNIC** | 재전송량 절감 |

#### 한줄 요약
- ECN/PFC 튜닝으로 데드락을 방지하고, DCQCN으로 인캐스트를 해소하며, 엔트로피 해싱으로 ECMP 부하를 분산한다.

## Ⅶ. 결론

- L3 AI 패브릭은 **RoCEv2·DCQCN**, 최고 성능 전용망은 **InfiniBand** 선택

#### 한줄 요약
- RoCEv2는 범용 이더넷 상에서 무손실 흐름 제어와 L3 라우팅을 지원하여 대규모 AI 분산 학습의 통신 병목을 해소하는 핵심 기술이다.
