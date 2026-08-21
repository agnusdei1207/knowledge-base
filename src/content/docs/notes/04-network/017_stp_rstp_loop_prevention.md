---
sidebar:
  order: 17
  label: "017. STP•RSTP 루프 방지 (STP•RSTP)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "스패닝 트리 루프 방지: STP•RSTP•PVST+ (Spanning Tree Protocol)"
date: "2026-08-22T07:15:00+09:00"
tags:
  - "notes-network"
weight: 17
extra:
  question_no: "017"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "L2 이중화 링크 루프 방지 및 고속 수렴(RSTP) 메커니즘"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **스패닝 트리 프로토콜(Spanning Tree Protocol, STP)**: L2 이더넷 네트워크의 다중 이중화 링크 환경에서 브로드캐스트 스톰(Broadcast Storm) 및 MAC 테이블 불안정(MAC Flapping)을 유발하는 순환 경로(Loop)를 차단하기 위해 비순환 논리 트리(Active Tree)를 구성하는 프로토콜(IEEE 802.1D).
- **고속 스패닝 트리 프로토콜(Rapid STP, RSTP)**: 30~50초에 달하는 기존 STP의 토폴로지 변경 수렴 시간을 1초 이내로 단축하기 위해 제안/동의(Proposal/Agreement) 핸드셰이크 방식을 도입한 표준(IEEE 802.1w/802.1Q).
- **PVST+(Per-VLAN Spanning Tree Plus)**: 단일 공통 트리(CST)의 링크 유휴 한계를 극복하기 위해 VLAN마다 독립적인 스패닝 트리 인스턴스를 유지하여 로드 밸런싱을 지원하는 기술.

</details>

- 정의/개념: L2 이중화 스위치 토폴로지에서 중복 링크를 논리적으로 차단(Blocking)하여 순환 루프를 방지하고 링크 장애 시 예비 경로를 활성화하는 **비순환 트리 구축 프로토콜**
- 배경/필요성: 단일 링크 장애 대비를 위한 물리적 이중화 구성 시 발생하는 브로드캐스트 스톰, 다중 프레임 복제 및 MAC 테이블 플래핑(Flapping) 장애 해소 요구

#### 한줄 요약
- L2 이중화 링크에서 논리적 블로킹을 통해 루프를 방지하고 장애 시 우회 경로를 자동 활성화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **브리지 ID(Bridge ID, BID)**: 스위치의 서열을 결정하기 위해 2바이트 Bridge Priority와 6바이트 기본 MAC 주소로 구성된 8바이트 고유 식별자.
- **경로 비용(Path Cost)**: 대역폭(Bandwidth)에 반비례하여 정의된 링크 비용 값으로, 루트 브리지까지의 최저 누적 비용 경로를 산출하는 기준.

</details>

- 네트워크 전체에서 **Bridge ID(BID)** 가 가장 낮은 스위치를 유일한 **루트 브리지(Root Bridge)** 로 선출
- 누적 **경로 비용(Path Cost)** 을 기준으로 각 스위치별 **루트 포트(RP)** 및 세그먼트별 **지정 포트(DP)** 선출
- 잔여 비지정 포트를 **대체 포트(Alternate Port, 차단 상태)** 로 격리하여 루프 차단 및 **RSTP** 기반 서브세컨드 고속 절체 지원

#### 한줄 요약
- 브리지 ID와 경로 비용을 계산하여 루트 및 포트 역할을 결정하고 잉여 포트를 논리적으로 차단한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **루트 포트(Root Port, RP)**: 비루트 스위치에서 루트 브리지로 향하는 최소 누적 경로 비용을 갖는 유일한 수신 포트(전달 상태).
- **지정 포트(Designated Port, DP)**: 각 물리 링크 세그먼트에서 루트 브리지 방향의 최소 비용을 제공하여 프레임 포워딩을 담당하는 포트(전달 상태).
- **대체 포트(Alternate Port, AP)**: RP나 DP로 선출되지 못하고 루프 방지를 위해 프레임을 차단(Discarding/Blocking)하는 백업 포트.
- **브리지 프로토콜 데이터 단위(BPDU)**: 스위치 간 토폴로지 계산 및 상태 유지를 위해 2초 주기로 교환하는 L2 제어 프레임.

</details>

```text
[ 루트 브리지 (Root Bridge / 최저 BID) ]
           │(DP)                    │(DP)
           │                        │
           │(RP)                    │(RP)
    [ 스위치 A ]               [ 스위치 B ]
           │(DP)                    │(AP, 차단 포트)
           └────── (이중화 링크) ─────┘
```

선의 의미: 루트 브리지로부터 BPDU가 전파되며 지정 포트(DP), 루트 포트(RP) 및 차단된 대체 포트(AP)로 구성되는 활성 트리

| 구성요소 | 책임 | 포트 상태 |
|:---|:---|:---|
| **루트 브리지** | 전체 L2 브로드캐스트 도메인의 기준점이 되는 최상위 스위치 | 모든 활성 포트가 DP(전달) |
| **루트 포트 (RP)** | 비루트 스위치에서 루트 브리지로 트래픽을 전달하는 최적 단일 포트 | Forwarding (전달) |
| **지정 포트 (DP)** | 각 이더넷 링크 세그먼트에서 트래픽 송수신 책임을 위임받은 포트 | Forwarding (전달) |
| **대체 포트 (AP)** | 루프 방지를 위해 트래픽 전달을 차단하고 대기하는 예비 백업 포트 | Discarding / Blocking |
| **BPDU 프레임** | 루트 ID, 송신자 BID, 경로 비용, 포트 ID를 교환하는 제어 PDU | 주기적 전송(2초) |

#### 한줄 요약
- 루트 브리지를 정점으로 RP, DP를 포워딩 상태로 두고, 루프 경로의 AP를 차단하여 트리를 완성한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **BPDU 4단계 우선순위 비교**: 1순위 Lowest Root BID $\rightarrow$ 2순위 Lowest Path Cost to Root $\rightarrow$ 3순위 Lowest Sender BID $\rightarrow$ 4순위 Lowest Port ID.

</details>

```text
1. BPDU 멀티캐스트 전송 및 상호 수신 (기본 주기 2초)
            │
            ▼
2. 루트 브리지(Root Bridge) 선출: 도메인 내 최저 Bridge ID(우선순위+MAC) 보유 스위치 확정
            │
            ▼
3. 루트 포트(RP) 선출: 비루트 스위치별 루트 도달 최저 누적 비용 인터페이스 선정
            │
            ▼
4. 지정 포트(DP) 선출: 각 링크 세그먼트별 최저 비용 스위치의 송출 인터페이스 선정
            │
            ▼
5. 잔여 비지정 포트 대체 포트(AP) 지정 및 차단(Blocking) 완료 (활성 트리 수렴)
```

**동작 원리**

1. **BPDU 교환**: 전원 인가 시 모든 스위치가 자신을 루트로 선언하는 Configuration BPDU 발송
2. **루트 선출**: 수신된 BPDU를 비교하여 가장 낮은 BID를 가진 단일 스위치를 루트 브리지로 확정
3. **RP 선정**: 각 비루트 스위치가 루트 브리지까지의 누적 경로 비용이 가장 적은 포트 1개를 RP로 지정
4. **DP 선정**: 스위치 간 연결된 각 링크 세그먼트마다 루트 도달 비용이 더 적은 쪽의 포트를 DP로 지정
5. **차단 및 수렴**: RP도 DP도 아닌 나머지 포트를 AP(차단) 상태로 전이시켜 루프 프리 토폴로지 구축

#### 한줄 요약
- BPDU 교환을 통해 루트 브리지 선출, RP/DP 선정, 잔여 포트 차단 순으로 루프 프리 트리를 구축한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **IEEE 802.1D (STP)**: Listening(15초) $\rightarrow$ Learning(15초) $\rightarrow$ Forwarding 타이머 기반으로 수렴에 최대 50초가 소요되는 표준.
- **IEEE 802.1w (RSTP)**: 포트 상태를 Discarding, Learning, Forwarding으로 단순화하고 핸드셰이크를 통해 즉각 수렴하는 표준.

</details>

| 비교 항목 | 전통적 STP (IEEE 802.1D) | 고속 RSTP (IEEE 802.1w) | PVST+ (Per-VLAN STP) |
|:---|:---|:---|:---|
| **수렴 메커니즘** | 타이머 기반 대기 (Max Age 20s + Fwd Delay 30s) | **제안/동의(Proposal/Agreement)** 핸드셰이크 | VLAN별 독립 RSTP/STP 인스턴스 운용 |
| **수렴 소요 시간** | **30 ~ 50초** (장애 시 서비스 지연) | **1초 이내 (Sub-second)** | 1초 이내 (RSTP 기반 PVST) |
| **링크 대역폭 활용** | 단일 트리(CST)로 차단 링크는 완전 유휴 | 단일 트리로 차단 링크 유휴 | VLAN별 루트 분산으로 **로드 밸런싱 지원** |
| **스위치 CPU 부하** | 낮음 (단일 인스턴스 계산) | 낮음 | VLAN 수에 비례하여 CPU 자원 소모 증가 |

#### 한줄 요약
- 타이머 기반의 802.1D 대비 802.1w는 제안/동의 핸드셰이크로 1초 내 수렴하며, PVST+는 VLAN별 로드 밸런싱을 지원한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **루트 가드(Root Guard)**: 하위 액세스 포트에서 더 우수한(낮은) BID를 가진 BPDU가 수신될 경우 해당 포트를 Root-Inconsistent 상태로 차단하여 루트 권한 탈취를 방지하는 기능.
- **BPDU 가드(BPDU Guard)**: PortFast가 설정된 단말 연결 포트에 비인가 스위치가 접속되어 BPDU가 수신되면 즉시 포트를 에러 셧다운(Err-Disable)시키는 보안 기능.
- **단방향 링크 탐지(UniDirectional Link Detection, UDLD)**: 광케이블 2가닥 중 단방향 단선 발생 시 차단 포트의 비정상 활성화로 인한 루프를 방지하기 위해 링크를 차단하는 L2 프로토콜.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 비인가 스위치의 낮은 BID 설정으로 인한 루트 브리지 탈취 | 다운링크 포트에 **루트 가드(Root Guard)** 활성화 | 비인가 스위치의 루트 선점 차단 및 토폴로지 안정성 사수 |
| PC 단말 연결 시 STP 30초 대기로 인한 DHCP 타임아웃 | 엣지 포트에 **PortFast** 설정 적용 | 포트 연결 즉시 Forwarding 상태로 전이하여 지연 해소 |
| 사용자 임의 스위치 연결로 인한 의도치 않은 브로드캐스트 루프 | PortFast 포트에 **BPDU Guard** 연동 | BPDU 인입 시 즉각 포트 차단(Err-Disable) 및 루프 원천 방지 |
| 광섬유 케이블의 단방향 통신 장애로 인한 차단 포트 오동작 | 파이버 링크에 **UDLD(Aggressive Mode)** 및 Loop Guard 적용 | 단방향 링크 감지 즉시 포트 셧다운 및 루프 방지 |

#### 한줄 요약
- 루트 가드로 루트 탈취를 방지하고, PortFast/BPDU 가드로 단말 포트를 보호하며, UDLD로 단방향 장애를 방어한다.

## Ⅶ. 결론

- L2 네트워크 가용성 확보를 위해 **RSTP(802.1w)** 및 **MSTP(802.1s)** 기반의 무루프 이중화 설계를 기본으로 적용하되, 루트 브리지 우선순위 고정과 함께 **BPDU Guard, Root Guard, Loop Guard**의 STP 보호 메커니즘을 계층별로 필히 구성하여 예기치 못한 L2 루프 장애를 원천 차단

#### 한줄 요약
- RSTP/MSTP와 다계층 보호 기법(BPDU/Root Guard, UDLD)을 연계하여 고가용성 L2 인프라를 확립한다.
