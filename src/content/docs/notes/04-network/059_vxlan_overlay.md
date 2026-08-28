---
sidebar:
  order: 59
  label: "059. VXLAN과 오버레이 네트워크"
  badge:
    text: "기출 · 50%"
    variant: note
title: "데이터센터 오버레이 터널링 기술 : VXLAN (Virtual Extensible LAN)"
date: "2026-08-26T13:54:57+09:00"
tags:
  - "notes-network"
weight: 59
extra:
  question_no: "59"
  source_status: "기출"
  source_history: "135회"
  priority: 50
  priority_note: "MAC-in-UDP 캡슐화, 24비트 VNI, VTEP 터널링 및 MP-BGP EVPN 제어 평면 연동"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **VXLAN (Virtual Extensible LAN)**: L3 IP 언더레이 위에 L2 이더넷 프레임을 UDP 패킷으로 캡슐화(MAC-in-UDP)하는 오버레이 터널링 기술 (RFC 7348).
- **Underlay vs Overlay**: 물리 스파인-리프 IP 라우팅 인프라(언더레이)와 그 상단에 터널링으로 생성된 논리 가상망(오버레이).

</details>

- 정의/개념: 물리 L3 IP 망 위에 **MAC-in-UDP 캡슐화와 24비트 VNI를 적용하여 1,600만 개 가상망을 제공하는 데이터센터 오버레이 가상화 기술**
- 배경/필요성: 12비트 VLAN 한계(4,094개) 및 L2 STP 링크 차단으로 인한 **멀티 테넌트 수용 불가, 대역폭 유휴화 및 L3 경계를 넘는 VM 무중단 마이그레이션 실패**를 겪으므로, L2 프레임을 UDP로 감싸 기존 L3 IP 망 위에 얹는 오버레이 계층을 두어 물리망 재설계 비용 없이 테넌트 식별자를 24비트로 넓히고 ECMP로 전 링크를 쓰게 할 필요

#### 한줄 요약
- VXLAN은 물리망을 재설계하지 않고 확장성과 이동성을 얻지만, 캡슐화 헤더만큼 페이로드가 줄어 언더레이 전 구간에 MTU 상향이라는 비용을 함께 부과한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **24-bit VNI (VXLAN Network Identifier)**: 최대 16,777,216개의 가상 브로드캐스트 도메인을 1:1 식별하는 24비트 가상망 ID.
- **MP-BGP EVPN (RFC 8365)**: BUM 트래픽의 무차별 플러딩을 방지하기 위해 BGP를 통해 MAC/IP 바인딩을 사전에 제어 평면으로 학습·광고하는 기술.

</details>

- **24비트 VNI 대규모 확장성**: 기존 12비트 VLAN 대비 수용 용량을 4,096배 확장하여 멀티 테넌시 완벽 지원
- **L3 패브릭 기반 L2 확장 (MAC-in-UDP)**: 물리 라우터를 그대로 통과하여 **STP 링크 차단 없이 L3 ECMP 대역폭 100% 활용**
- **MP-BGP EVPN 제어 평면 결합**: 사전 BGP 경로(Type-2/Type-5) 광고를 통해 데이터 평면 BUM 플러딩 억제

#### 한줄 요약
- 24비트 VNI 확장성, MAC-in-UDP 터널링, L3 ECMP 활용, MP-BGP EVPN 연계를 통한 BUM 억제를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **VTEP (VXLAN Tunnel Endpoint)**: 원본 L2 프레임에 Outer IP/UDP/VXLAN 헤더(50바이트)를 캡슐화 및 역캡슐화하는 터널 종단점.

</details>

```text
[VXLAN 구성]
|-- VTEP
|-- VNI
|-- 언더레이 패브릭
`-- MP-BGP EVPN
```

선의 의미: 테넌트 VM의 L2 프레임이 송신 VTEP에서 50바이트 외부 헤더로 캡슐화되어 L3 언더레이를 고속 통과한 후 수신 VTEP에서 복원되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **VTEP (터널 종단점)** | 원본 L2 프레임에 **Outer IP/UDP/VXLAN 헤더(50B) 캡슐화 및 역캡슐화 수행** | SW(OVS) 또는 HW(ASIC) |
| **VNI (가상망 식별자)**| **24비트 필드로 개별 가상 브로드캐스트 도메인을 1:1 식별 (1,600만 개)** | VXLAN Header (8B) |
| **언더레이 패브릭** | BGP/OSPF 라우팅 및 **L3 ECMP를 통해 VTEP 간 UDP 패킷을 라인 레이트 전달** | IP 스파인-리프 |
| **MP-BGP EVPN** | 호스트 MAC/IP 바인딩을 **BGP 경로(Type-2, Type-5)로 사전 광고하여 플러딩 방지** | 제어 평면 표준 |

#### 한줄 요약
- VTEP가 원본 프레임 앞에 50바이트 외부 헤더를 씌워 L2 확장 부담을 언더레이의 L3 라우팅으로 넘기고, MP-BGP EVPN이 MAC 위치를 미리 광고해 데이터 평면이 BUM 플러딩으로 학습하던 비용을 대신한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **VXLAN 50-Byte Overhead**: Outer Ethernet(14B) + Outer IP(20B) + Outer UDP(8B, 목적지 포트 4789) + VXLAN Header(8B).

</details>

```text
VXLAN 캡슐화 및 L3 언더레이 포워딩 파이프라인
        │
   1. [L2 프레임 송출] 테넌트 VM A가 목적지 VM B의 MAC을 지정하여 L2 프레임 송출
        │
   2. [EVPN 테이블 조회] 송신 VTEP가 MP-BGP EVPN을 조회하여 원격 VTEP IP 식별
        │
   3. [50B 헤더 캡슐화] VNI 10000 및 Outer UDP(포트 4789)/IP 헤더 부착
        │
   4. [L3 ECMP 고속 수송] 언더레이 스파인-리프 스위치가 외부 IP만으로 ECMP 라우팅
        │
   ▼
5. [수신 VTEP 역캡슐화] 수신 VTEP가 Outer 헤더를 제거하고 원본 L2 프레임을 VM B로 전달
```

#### 한줄 요약
- EVPN이 MAC 위치를 미리 광고해 둔 덕에 캡슐화 시점에 플러딩 없이 목적지 VTEP이 정해지고, 그 대신 50바이트 헤더만큼 페이로드 여유를 내준다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **VXLAN (오버레이)** vs **VLAN (전통적 802.1Q)**: 1,600만 VNI(VXLAN)와 4,094 VID(VLAN).

</details>

| 비교 항목 | VXLAN (오버레이 네트워크) | 전통적 VLAN (IEEE 802.1Q) |
|:---|:---|:---|
| **가상망 식별자 크기**| **24비트 VNI (최대 16,777,216개)** | **12비트 VID (최대 4,094개)** |
| **캡슐화 방식** | **MAC-in-UDP 캡슐화 (L4 페이로드 전달)** | 프레임 내 4바이트 802.1Q 태그 삽입 |
| **물리 인프라 제약** | **L3 IP 언더레이 구축 시 장비 무관 동작** | 물리 스위치 전 구간 L2 직결 요구 |
| **경로 대역폭 활용** | **L3 ECMP(등가 다중 경로)로 모든 링크 100% 활용**| STP로 인해 예비 링크 강제 차단 |
| **L2 이동성 (Migration)**| **L3 라우터 경계를 넘어 동일 서브넷 유지 이동** | 동일 L2 브로드캐스트 도메인 내 제한 |

#### 한줄 요약
- VXLAN은 1,600만 세그먼트, L3 ECMP 대역폭 활용, L3 경계를 넘는 L2 이동성을 제공한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Jumbo Frame (점보 프레임)**: 50바이트 VXLAN 오버헤드로 인한 IP 단편화(Fragmentation)를 방지하기 위해 MTU를 1550~9000바이트로 확장하는 설정.
- **DPU / SmartNIC Offload**: VXLAN 캡슐화 연산을 서버 CPU 대신 전용 DPU 하드웨어에서 라인 레이트로 가속 처리하는 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 50바이트 VXLAN 오버헤드로 인한 MTU 초과 및 IP 단편화 지연 | 언더레이 물리 패브릭 전 구간에 **`점보 프레임(MTU 9000B)` 적용** | 패킷 단편화 원천 방지 및 전송 성능 보증 |
| 목적지 미식별 시 언더레이 망으로의 무차별 BUM 플러딩 발생 | **`MP-BGP EVPN 및 ARP 억제(ARP Suppression)` 결합** | 데이터 평면 플러딩 90% 이상 제거 및 대역폭 보존 |
| 대규모 캡슐화/역캡슐화 연산으로 인한 호스트 CPU 점유율 과다 | **`SmartNIC / DPU 기반 VXLAN 하드웨어 오프로딩` 적용** | 호스트 CPU 부하 제거 및 100Gbps 라인 레이트 달성 |
| 서로 다른 테넌트 간의 가상 네트워크 침해 및 횡적 이동 위험 | **`테넌트별 분리된 VRF (Virtual Routing and Forwarding)` 격리** | 테넌트 간 완벽한 트래픽 보안 격리 달성 |

#### 한줄 요약
- 점보 프레임 단편화 방지, MP-BGP EVPN BUM 억제, SmartNIC 가속, VRF 격리로 운영한다.

## Ⅶ. 결론

- L3 위 L2 확장은 **VXLAN**, BUM 억제는 **MP-BGP EVPN** 적용

#### 한줄 요약
- VXLAN은 MAC-in-UDP 캡슐화와 24비트 VNI를 통해 L3 망 위에서 대규모 가상 L2 네트워크를 실현하는 핵심 데이터센터 오버레이 기술이다.
