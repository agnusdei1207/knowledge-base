---
sidebar:
  order: 17
  label: "017. STP•RSTP 루프 방지"
  badge:
    text: "기출 · 70%"
    variant: note
title: "STP•RSTP 루프 방지 (Spanning Tree Protocol)"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 17
extra:
  question_no: "17"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "L2 이중화 링크 루프 방지 및 고속 수렴(RSTP) 메커니즘"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **STP (Spanning Tree Protocol, IEEE 802.1D)**: L2 이중화 링크에서 브로드캐스트 스톰과 루프를 차단하기 위해 비순환 논리 트리를 구성하는 프로토콜.
- **RSTP (Rapid STP, IEEE 802.1w)**: Proposal/Agreement 핸드셰이크 방식을 도입하여 30~50초의 수렴 시간을 1초 이내로 단축한 고속 표준.

</details>

- 정의/개념: L2 이더넷 이중화 네트워크에서 **BPDU 교환을 통해 잉여 링크를 논리적으로 차단(Blocking)하여 루프 없는 트리를 구성하는 프로토콜**
- 배경/필요성: 가용성 확보를 위한 중복 링크 구성 시 발생하는 **L2 브로드캐스트 스톰, 다중 프레임 복제 및 CAM 테이블 무한 플래핑 마비 해결 불가**

#### 한줄 요약
- BPDU 교환을 통해 루트 브리지와 포트 역할을 결정하고, 잉여 링크를 논리 차단하여 루프를 방지한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Bridge ID (BID)**: 스위치 우선순위(2바이트, 기본값 32768)와 스위치 MAC 주소(6바이트)로 구성된 8바이트 고유 식별자 (낮을수록 루트 브리지로 선출).
- **Proposal/Agreement Handshake**: RSTP에서 타이머 대기 없이 인접 스위치 간 양방향 동기화 핸드셰이크를 통해 1초 미만으로 포워딩 상태로 전이하는 기법.

</details>

- 도메인 내 최저 **Bridge ID (우선순위+MAC)**를 보유한 단일 루트 브리지(Root Bridge) 선출
- 최저 누적 **경로 비용(Path Cost)**을 기준으로 루트 포트(RP) 및 지정 포트(DP) 선출
- 잔여 포트를 **대체 포트(Alternate Port, 차단)**로 격리하고 **RSTP 기반 1초 미만 고속 절체**

#### 한줄 요약
- 최저 BID 루트 선출, 경로 비용 기반 RP/DP 결정, 잔여 포트 차단 및 RSTP 고속 수렴을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **BPDU (Bridge Protocol Data Unit)**: 루트 브리지 선출 및 트리 계산을 위해 스위치 간 2초 주기로 교환하는 L2 제어 프레임.

</details>

```text
[STP / RSTP 무루프 활성 트리 토폴로지 구조]
|-- Root Bridge (최저 Bridge ID 보유 스위치, 모든 포트 DP Forwarding)
|   |-- Designated Port 1 (DP: Segment A 포워딩)
|   `-- Designated Port 2 (DP: Segment B 포워딩)
|-- Non-Root Switch A
|   |-- Root Port (RP: 루트 브리지로 향하는 최저 비용 포트, Forwarding)
|   `-- Designated Port (DP: Segment C 포워딩)
`-- Non-Root Switch B
    |-- Root Port (RP: 루트 브리지로 향하는 포트, Forwarding)
    `-- Alternate Port (AP: 루프 방지를 위해 논리 차단 Discarding/Blocking)
```

선의 의미: 계층 및 루트 브리지로부터 BPDU가 전파되어 RP, DP는 활성화되고 잉여 링크의 AP는 차단되어 루프가 제거되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **루트 브리지 (Root)** | 전체 L2 브로드캐스트 도메인의 기준점이 되는 **최상위 스위치로 모든 활성 포트가 지정 포트(DP)** | 최저 BID 선출 |
| **루트 포트 (RP)** | 비루트 스위치에서 **루트 브리지로 향하는 최소 누적 경로 비용을 가진 유일한 수신 포트** | Forwarding 상태 |
| **지정 포트 (DP)** | 각 물리 링크 세그먼트마다 **루트 도달 비용이 가장 낮은 스위치의 프레임 송출 포트** | Forwarding 상태 |
| **대체 포트 (AP)** | RP나 DP로 선출되지 못하고 **루프 방지를 위해 프레임을 차단하고 대기하는 예비 백업 포트** | Discarding / Blocking |
| **BPDU 프레임** | 루트 ID, 송신자 BID, **경로 비용, 포트 ID를 담아 2초 주기로 멀티캐스트 송출하는 제어 PDU** | 802.1D / 802.1w |

#### 한줄 요약
- 루트 브리지, 루트 포트(RP), 지정 포트(DP), 대체 포트(AP), BPDU 제어 프레임이 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **BPDU 4단계 우선순위 비교**: 1순위 Lowest Root BID $\to$ 2순위 Lowest Path Cost to Root $\to$ 3순위 Lowest Sender BID $\to$ 4순위 Lowest Port ID.

</details>

```text
STP 토폴로지 계산 및 루프 차단
        │
   1. [BPDU 전파] 모든 스위치가 2초 주기로 Configuration BPDU 멀티캐스트 교환
        │
   2. [루트 브리지 선출] 도메인 내 최저 Bridge ID(Priority + MAC) 보유 스위치 확정
        │
   3. [루트 포트(RP) 선정] 비루트 스위치별 루트 도달 최저 누적 비용 인터페이스 선출
        │
   4. [지정 포트(DP) 선정] 링크 세그먼트별 루트 도달 비용이 더 적은 스위치 포트 선출
        │
   5. [대체 포트(AP) 차단] 잔여 비지정 포트를 Discarding/Blocking 전이하여 루프 차단 완료
```

#### 한줄 요약
- BPDU 교환 → 루트 브리지 선출 → RP/DP 선정 → 잔여 포트 차단 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **STP (802.1D)** vs **RSTP (802.1w)** vs **PVST+ / MSTP (802.1s)**: 단일 트리 타이머 수렴, 고속 핸드셰이크 수렴, VLAN별 다중 인스턴스 로드 밸런싱.

</details>

| 비교 항목 | 전통적 STP (IEEE 802.1D) | 고속 RSTP (IEEE 802.1w) | PVST+ / MSTP (IEEE 802.1s) |
|:---|:---|:---|:---|
| **수렴 메커니즘** | **타이머 기반 대기 (Max Age 20s + Fwd Delay 30s)**| **Proposal / Agreement 핸드셰이크** | **VLAN별 / 인스턴스별 독립 계산** |
| **수렴 소요 시간** | **30 ~ 50초 (장애 시 서비스 지연 심각)** | **1초 이내 (Sub-second)** | **1초 이내 (RSTP 기반 고속 수렴)** |
| **링크 대역폭 활용**| 단일 공통 트리(CST)로 차단 링크 완전 유휴 | 단일 트리로 차단 링크 유휴 | **VLAN별 루트 분산으로 로드 밸런싱 지원**|
| **포트 상태 구성** | 5단계 (Disabled, Blocking, Listening, Learning, Fwd)| **3단계 (Discarding, Learning, Forwarding)**| 3단계 (Discarding, Learning, Forwarding)|

#### 한줄 요약
- 802.1D는 30~50초 수렴, 802.1w는 1초 내 수렴, PVST+/MSTP는 VLAN별 로드 밸런싱을 지원한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **BPDU Guard**: PortFast가 설정된 단말 포트에 스위치가 연결되어 BPDU가 수신되면 즉시 포트를 에러 셧다운(Err-Disable)시키는 보안 기능.
- **Root Guard**: 하위 다운링크 포트에서 더 우수한(낮은) BID BPDU가 유입될 때 해당 포트를 차단하여 루트 탈취를 방지하는 기능.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 비인가 스위치의 낮은 BID 설정으로 인한 루트 브리지 권한 탈취 | 다운링크 포트에 **`Root Guard` 활성화** | 비인가 스위치의 루트 선점 차단 및 토폴로지 안정성 사수 |
| PC 단말 접속 시 STP 30초 대기로 인한 DHCP IP 획득 타임아웃 | 엣지 포트에 **`PortFast (Edge Port)` 설정 적용** | 포트 연결 즉시 Forwarding 상태 전이 및 지연 해소 |
| 사용자가 임의로 허브/스위치를 연결하여 의도치 않은 L2 루프 발생 | PortFast 포트에 **`BPDU Guard` 연동** | BPDU 수신 즉시 포트 에러 셧다운(Err-Disable) 차단 |
| 광섬유 2가닥 중 단방향 단선으로 인한 차단 포트 오동작 및 루프 | 파이버 링크에 **`UDLD (Aggressive Mode) 및 Loop Guard`** | 단방향 링크 감지 즉시 포트 차단 및 루프 원천 방지 |

#### 한줄 요약
- Root Guard, PortFast, BPDU Guard, UDLD/Loop Guard로 운영한다.

## Ⅶ. 결론

- L2 스위칭 인프라의 가용성과 루프 방지를 위해 **RSTP(IEEE 802.1w) 및 MSTP(IEEE 802.1s) 기반의 무루프 이중화 설계를 기본 표준화**하고, **루트 브리지 우선순위 고정(Priority 4096), PortFast/BPDU Guard 및 Root Guard, UDLD**의 4대 보호 메커니즘을 계층별로 결합하여 무결점 L2 인프라 완성

#### 한줄 요약
- STP/RSTP는 BPDU 기반의 포트 차단과 고속 수렴을 통해 L2 루프를 방지하며, BPDU Guard 및 Root Guard와 결합하여 고가용성을 보장하는 핵심 L2 기술이다.