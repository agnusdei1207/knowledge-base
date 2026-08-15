---
sidebar:
  order: 59
  label: "059. VXLAN과 오버레이 네트워크 (VXLAN Overlay)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "VXLAN과 오버레이 네트워크 (VXLAN Overlay)"
date: "2026-08-13T16:02:00+09:00"
tags:
  - "notes-network"
weight: 59
extra:
  question_no: "059"
  source_status: "기출"
  source_history: "135회"
  priority: 50
  priority_note: "구조•설계형: 135회 VXLAN 장문 출제"
---

## Ⅰ. 개요

<details>
<summary>용어 설명</summary>

- **가상 확장성 무선/유선 가상 랜(Virtual Extensible LAN, VXLAN)**: L2 이더넷 프레임을 L4 UDP 패킷으로 캡슐화(MAC-in-UDP)하여 L3 네트워크를 가로지르는 대규모 오버레이 가상 네트워크를 구축하는 IETF 표준 프로토콜이다.
- **오버레이 네트워크(Overlay Network)**: 물리적 인프라(Underlay) 위에 터널링 기술을 적용하여 상위에 구축된 논리적 가상 네트워크층이다.
- **언더레이 네트워크(Underlay Network)**: VTEP 장비 간의 L3 IP Reachability 및 높은 전송 대역폭을 보장하는 스파인-리프(Spine-Leaf) 물리 네트워크 인프라이다.

</details>

- 정의/개념: **VXLAN(Virtual Extensible LAN)**은 기존 L2 VLAN의 4,094개 세그먼트 수량 한계를 극복하기 위해 L2 이더넷 프레임을 L4 UDP 패킷으로 캡슐화(MAC-in-UDP)하여, L3 IP 라우팅 인프라(Underlay) 상위에 독립된 L2 가상 네트워크(Overlay)를 대규모 구축하는 캡슐화 프로토콜 기술이다.
- 배경/필요성: VLAN 식별자 부족과 L2 도메인의 물리망 종속으로 대규모 멀티 테넌트 확장이 제한되어 제정되었다.

#### 한줄 요약

- L2 이더넷 프레임을 L4 UDP 패킷으로 캡슐화(MAC-in-UDP)하여 L3 라우팅망 위에 1,600만 개의 가상 네트워크(VNI)를 형성하는 오버레이 기술.

## Ⅱ. 특징

<details>
<summary>용어 설명</summary>

- **가상 네트워크 식별자(VXLAN Network Identifier, VNI)**: 기존 12비트 VLAN ID를 대체하여 최대 약 1,600만 개(24비트)의 개별 가상 세그먼트를 식별하는 고유 테넌트 ID이다.
- **VXLAN 터널 종단점(VXLAN Tunnel Endpoint, VTEP)**: 원본 L2 프레임에 Outer IP/UDP/VXLAN 헤더를 캡슐화(Encapsulation)하고 역캡슐화(Decapsulation)를 수행하는 가상/물리 스위치 노드이다.
- **이더넷 가상 사설망(Ethernet VPN, EVPN)**: MP-BGP 프로토콜을 이용해 호스트의 MAC 및 IP 주소를 VTEP 간에 사전 교환하여 BUM 트래픽 플러딩을 억제하는 제어 평면 규격이다.

</details>

- **24비트 VNI 기반 세그먼트 확장**: 약 1,600만 개 식별 공간으로 대규모 멀티 테넌트 분리를 지원한다.
- **MAC-in-UDP 패킷 캡슐화**: 원본 이더넷 프레임에 Outer Ethernet, Outer IP, Outer UDP(Port 4789), 8바이트 VXLAN 헤더를 결합하여 L3 망을 통해 유연 수송한다.
- **MP-BGP EVPN 제어 평면 기반 BUM 억제**: 호스트 MAC/IP 주소를 Control Plane에서 BGP Type-2 패킷으로 미리 공유하여 불필요한 브로드캐스트 플러딩을 방지한다.

#### 한줄 요약

- 24비트 VNI 식별자 적용, MAC-in-UDP 캡슐화 전송, MP-BGP EVPN 제어 평면 연동을 통한 대규모 SDDC 가상화 제공.

## Ⅲ. 구조 및 구성요소

<details>
<summary>용어 설명</summary>

- **브로드캐스트·미지의 유니캐스트·멀티캐스트(Broadcast, Unknown Unicast, Multicast, BUM Traffic)**: 수신 VTEP 위치를 모를 때 물리 언더레이망으로 복제 전송되는 무선/유선 플러딩 트래픽 세트이다.
- **등가 다중 경로(Equal-Cost Multi-Path, ECMP)**: 동일 비용의 L3 경로에 흐름을 분산하는 라우팅 기술이다.

</details>

```text
VXLAN 오버레이-언더레이 이중 구조
├─ 오케스트레이션 오버레이 계층 (Overlay Layer - Virtual L2 Networks)
│  ├─ 테넌트 가상 세그먼트 (Tenant VNI 100, VNI 200)
│  ├─ VXLAN 터널 종단점 (VTEP - VXLAN Tunnel Endpoint)
│  ├─ VXLAN 헤더 (VXLAN Header)
│  └─ MP-BGP EVPN 제어 평면 (EVPN Control Plane)
└─ 물리적 전송 언더레이 계층 (Underlay Layer - Physical L3 Fabric)
   └─ IP 언더레이 패브릭 (Spine-Leaf L3 Fabric & ECMP)
```

선의 의미: 상위 테넌트의 L2 오버레이 패킷이 VTEP에서 캡슐화되어 하부 L3 스파인-리프 언더레이 패브릭을 타고 ECMP 경로로 수송되는 2계층 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| VXLAN 터널 종단점 (VTEP) | hypervisor 스위치나 리프 스위치에 위치하며 L2 프레임의 VNI 매핑 및 UDP 캡슐화/역캡슐화 실행 |
| VXLAN 헤더 (VXLAN Header) | 24비트 VNI 식별자와 캡슐화 플래그 정보를 보유한 8바이트 크기의 전용 헤더 모듈 |
| IP 언더레이 패브릭 | L3 Spine-Leaf 토폴로지 상에서 VTEP 간 IP 도달성을 제공하고 L3 ECMP 대역폭 분산 수용 |
| MP-BGP EVPN (Control Plane) | 호스트 MAC/IP 위치(Type-2) 및 VTEP 자동 발견(Type-3) 정보를 BGP 메시지로 전파 |
| 테넌트 VNI 세그먼트 | 24비트 ID로 지정된 논리적 L2 브로드캐스트 도메인 분리 |

#### 한줄 요약

- VTEP 장비가 원본 프레임을 UDP 패킷으로 캡슐화하여 L3 스파인-리프 언더레이망을 통해 수송하고 EVPN 제어 평면이 MAC/IP 매핑을 공유하는 아키텍처.

## Ⅳ. 흐름도

<details>
<summary>용어 설명</summary>

- **MAC·IP 위치 경로(MAC/IP Advertisement Route / EVPN Type-2)**: MP-BGP EVPN을 통해 단말의 MAC/IP 및 수용 VTEP IP 주소를 타 VTEP로 전달하는 경로 정보이다.
- **최대 전송 단위(Maximum Transmission Unit, MTU)**: 패킷 단편화를 막기 위해 무선/유선 라우터 인터페이스에 설정하는 최대 프레임 크기이다.

</details>

```text
1. 송신 호스트 원본 L2 이더넷 프레임 발신 (Original Frame)
      │
      v
2. 송신 VTEP: EVPN Type-2 테이블에서 목적지 MAC 매핑 조회 (VTEP Table Lookup)
      │
      ├─ 매핑 성공 ── Unicast 목적지 VTEP 지정
      └─ 매핑 실패 ── BUM 복제 대상 지정
            │
            v
      3. Outer 헤더 캡슐화
            │
            v
      4. L3 언더레이 전송
            │
            v
      5. 역캡슐화 및 목적지 전달
```

### 동작 원리

1. **송신 호스트 원본 L2 이더넷 프레임 발신**
2. **송신 VTEP의 목적지 MAC 매핑 조회**
3. **Outer 헤더 캡슐화**
4. **L3 언더레이 전송**
5. **역캡슐화 및 목적지 전달**

#### 한줄 요약

- 원본 프레임 발신, 송신 VTEP 매핑 조회, Unicast/BUM 캡슐화, L3 언더레이 ECMP 수송 및 수신 VTEP 역캡슐화 절차.

## Ⅴ. 종류 및 비교

<details>
<summary>용어 설명</summary>

- **VLAN 식별자(VLAN Identifier, VID)**: IEEE 802.1Q 프레임 헤더 내 12비트 크기로 위치하여 기존 L2 가상망을 구별하던 식별자이다.

</details>

| 비교 항목 | **VXLAN (Virtual Extensible LAN)** | **VLAN (Virtual Local Area Network)** |
|:---|:---|:---|
| 캡슐화 방식 | MAC-in-UDP (L4 UDP 4789번 터널링) | IEEE 802.1Q (L2 이더넷 Tagging) |
| 세그먼트 식별자 | 24비트 VNI (최대 16,777,216개 지원) | 12비트 VID (최대 4,094개 한계) |
| 전송 기반 인프라 | L3 IP 라우팅 언더레이망 (Spine-Leaf) | L2 물리 스위칭 네트워크 직접 종속 |
| 경로 효율성 | L3 ECMP 기반 다중 경로 활용 | STP 구성 시 차단 포트 발생 가능 |
| 제어 및 관리 | MP-BGP EVPN 연동 컨트롤 플레인 자동화 | 개별 스위치 수동 VLAN DB 및 Trunk 설정 |

> 요약: VLAN은 4,094개 수량 한계 및 STP 포트 블로킹이 발생하나, VXLAN은 1,600만 개 VNI와 L3 ECMP 대역폭 활용을 제공.

#### 한줄 요약

- VLAN은 4,094개 수량 한계 및 STP 포트 블로킹이 발생하나, VXLAN은 1,600만 개 VNI와 L3 ECMP 대역폭 활용을 제공.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>용어 설명</summary>

- **점보 프레임(Jumbo Frame / MTU Expansion)**: VXLAN 캡슐화 헤더 50바이트 오버헤드로 인한 IP 단편화를 막기 위해 언더레이 MTU를 1,550~9,216바이트로 확장하는 설정이다.

</details>

| 문제점 | 발생 원인 | 실무 대응 대책 | 기대 효과 |
|:---|:---|:---|:---|
| 캡슐화 패킷 단편화 (Fragmentation) | 50Byte 헤더 부가로 언더레이 MTU(1500b) 초과 | 언더레이 스위치/라우터 MTU 1550b 이상 점보 설정 | 패킷 분할 재조합 오버헤드 제거 및 속도 저하 차단 |
| 데이터 평면 BUM 폭주 | 목적지 MAC 미학습 시 전체 VTEP로 플러딩 | MP-BGP EVPN 및 ARP Suppression 기술 도입 | 데이터 평면 플러딩 최소화 및 언더레이 대역폭 보존 |
| 터널 캡슐화 연산 부하 | 백엔드 NIC CPU에서 캡슐화/역캡슐화 처리 | SmartNIC / DPU 하드웨어 VXLAN Offload 채택 | 호스트 CPU 사용률 절감 및 라인 레이트 처리 |
| VTEP 경로 갱신 지연 | 수신 VTEP IP 변경 시 오버레이 경로 단절 | BFD 연동 ECMP 절체와 EVPN 경로 회수 | 장애 감지 및 우회 시간 단축 |

#### 한줄 요약

- 언더레이 점보 프레임(MTU 1550+ Byte) 활성화, EVPN ARP Suppression 적용, BFD 연동 ECMP 기반 가용성 확립으로 VXLAN 오버레이 완성.

## Ⅶ. 결론

- 대규모 멀티 테넌트는 **VXLAN**, 소규모 L2 분리는 **VLAN** 선택.

#### 한줄 요약

- 24비트 VNI 기반 VXLAN 오버레이 및 MP-BGP EVPN 제어 평면 수립과 점보 프레임(MTU 1550+) 설정 필수.
