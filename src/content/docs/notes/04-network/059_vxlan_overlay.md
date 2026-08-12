---
sidebar:
  order: 59
  label: "059. VXLAN과 오버레이 네트워크 (VXLAN Overlay)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "VXLAN과 오버레이 네트워크 (VXLAN Overlay)"
date: "2026-08-06T23:27:50+09:00"
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
<summary>핵심 용어</summary>

- **가상 확장성 무선/유선 가상 랜(Virtual Extensible LAN, VXLAN)**: L2 이더넷 프레임을 L4 UDP 패킷으로 캡슐화(MAC-in-UDP)하여 L3 네트워크를 가로지르는 대규모 오버레이 가상 네트워크를 구축하는 IETF 표준 프로토콜이다.
- **오버레이 네트워크(Overlay Network)**: 물리적 인프라(Underlay) 위에 터널링 기술을 적용하여 상위에 구축된 논리적 가상 네트워크층이다.
- **언더레이 네트워크(Underlay Network)**: VTEP 장비 간의 L3 IP Reachability 및 높은 전송 대역폭을 보장하는 스파인-리프(Spine-Leaf) 물리 네트워크 인프라이다.

</details>

- 정의/개념: **VXLAN(Virtual Extensible LAN)**은 기존 L2 VLAN의 4,094개 세그먼트 수량 한계를 극복하기 위해 L2 이더넷 프레임을 L4 UDP 패킷으로 캡슐화(MAC-in-UDP)하여, L3 IP 라우팅 인프라(Underlay) 상위에 독립된 L2 가상 네트워크(Overlay)를 대규모 구축하는 캡슐화 프로토콜 기술이다.
- 배경/필요성: 대규모 클라우드 데이터센터(SDDC)의 멀티 테넌트 가상머신(VM) 및 컨테이너 폭증으로 인한 L2 세그먼트 부족 문제와, L3 경계를 넘어선 VM Live Migration을 무손실 보장하기 위해 IETF RFC 7348로 제정되었다.

#### 한줄 요약

- L2 이더넷 프레임을 L4 UDP 패킷으로 캡슐화(MAC-in-UDP)하여 L3 라우팅망 위에 1,600만 개의 가상 네트워크(VNI)를 형성하는 오버레이 기술.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **가상 네트워크 식별자(VXLAN Network Identifier, VNI)**: 기존 12비트 VLAN ID를 대체하여 최대 약 1,600만 개(24비트)의 개별 가상 세그먼트를 식별하는 고유 테넌트 ID이다.
- **VXLAN 터널 종단점(VXLAN Tunnel Endpoint, VTEP)**: 원본 L2 프레임에 Outer IP/UDP/VXLAN 헤더를 캡슐화(Encapsulation)하고 역캡슐화(Decapsulation)를 수행하는 가상/물리 스위치 노드이다.
- **이더넷 가상 사설망(Ethernet VPN, EVPN)**: MP-BGP 프로토콜을 이용해 호스트의 MAC 및 IP 주소를 VTEP 간에 사전 교환하여 BUM 트래픽 플러딩을 억제하는 제어 평면 규격이다.

</details>

- **24비트 VNI 기반 세그먼트 극대화**: 16,777,216개의 VNI 식별자를 보장하여 대규모 클라우드 센터의 멀티 테넌트 격리 및 세그먼트 생성을 완벽히 수용한다.
- **MAC-in-UDP 패킷 캡슐화**: 원본 이더넷 프레임에 Outer Ethernet, Outer IP, Outer UDP(Port 4789), 8바이트 VXLAN 헤더를 결합하여 L3 망을 통해 유연 수송한다.
- **MP-BGP EVPN 제어 평면 기반 BUM 억제**: 호스트 MAC/IP 주소를 Control Plane에서 BGP Type-2 패킷으로 미리 공유하여 불필요한 브로드캐스트 플러딩을 방지한다.

#### 한줄 요약

- 24비트 VNI 식별자 적용, MAC-in-UDP 캡슐화 전송, MP-BGP EVPN 제어 평면 연동을 통한 대규모 SDDC 가상화 제공.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **브로드캐스트·미지의 유니캐스트·멀티캐스트(Broadcast, Unknown Unicast, Multicast, BUM Traffic)**: 수신 VTEP 위치를 모를 때 물리 언더레이망으로 복제 전송되는 무선/유선 플러딩 트래픽 세트이다.
- **등가 다중 경로(Equal-Cost Multi-Path, ECMP)**: L3 스파인-리프 인프라에서 모든 이중화 물리 링크 대역폭을 100% 동시에 활용하는 라우팅 기술이다.

</details>

```text
VXLAN 오버레이-언더레이 이중 구조
├─ 오케스트레이션 오버레이 계층 (Overlay Layer - Virtual L2 Networks)
│  ├─ 테넌트 가상 세그먼트 (Tenant VNI 100, VNI 200)
│  └─ VXLAN 터널 종단점 (VTEP - VXLAN Tunnel Endpoint)
└─ 물리적 전송 언더레이 계층 (Underlay Layer - Physical L3 Fabric)
   ├─ L3 스파인-리프 패브릭 (Spine-Leaf L3 Fabric & ECMP)
   └─ MP-BGP EVPN 제어 평면 (EVPN Control Plane - Type-2 / Type-3)
```

선의 의미: 상위 테넌트의 L2 오버레이 패킷이 VTEP에서 캡슐화되어 하부 L3 스파인-리프 언더레이 패브릭을 타고 ECMP 경로로 수송되는 2계층 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| VXLAN 터널 종단점 (VTEP) | hypervisor 스위치나 리프 스위치에 위치하며 L2 프레임의 VNI 매핑 및 UDP 캡슐화/역캡슐화 실행 |
| VXLAN 헤더 (VXLAN Header) | 24비트 VNI 식별자와 캡슐화 플래그 정보를 보유한 8바이트 크기의 전용 헤더 모듈 |
| IP 언더레이 패브릭 | L3 Spine-Leaf 토폴로지 상에서 VTEP 간 IP 도달성을 제공하고 L3 ECMP 대역폭 분산 수용 |
| MP-BGP EVPN (Control Plane) | 호스트 MAC/IP 위치(Type-2) 및 VTEP 자동 발견(Type-3) 정보를 BGP 메시지로 전파 |
| 테넌트 VNI 세그먼트 | 24비트 고유 ID로 지정된 가상 L2 세그먼트로, 상호 간 완전한 세그먼트 보안 격리 보장 |

#### 한줄 요약

- VTEP 장비가 원본 프레임을 UDP 패킷으로 캡슐화하여 L3 스파인-리프 언더레이망을 통해 수송하고 EVPN 제어 평면이 MAC/IP 매핑을 공유하는 아키텍처.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **MAC·IP 위치 경로(MAC/IP Advertisement Route / EVPN Type-2)**: MP-BGP EVPN을 통해 단말의 MAC/IP 및 수용 VTEP IP 주소를 타 VTEP로 전달하는 경로 정보이다.
- **최대 전송 단위(Maximum Transmission Unit, MTU)**: 패킷 단편화를 막기 위해 무선/유선 라우터 인터페이스에 설정하는 최대 프레임 크기이다.

</details>

```text
1. 송신 호스트 원본 L2 이더넷 프레임 발신 (Original Frame)
      │
      v
2. 송신 VTEP: EVPN Type-2 테이블에서 목적지 MAC 매핑 조회 (VTEP Table Lookup)
      │
      ├─ 매핑 성공 ── 3a. Unicast 목적지 VTEP IP 주소 지정 및 캡슐화
      └─ 매핑 실패 ── 3b. BUM Multicast / Ingress Replication 복제
            │
            v
      4. L3 IP 언더레이 패브릭을 통한 UDP 패킷 무선/유선 전달 (Underlay ECMP)
            │
            v
      5. 수신 VTEP: Outer 헤더 역캡슐화 후 목적지 호스트로 전달 (Decapsulation)
```

### 동작 원리

1. **원본 L2 프레임 송신**: 테넌트 가상머신(VM)이 목적지 MAC 주소를 포함한 기본 이더넷 프레임을 발신한다.
2. **VTEP 매핑 조회**: 송신 VTEP가 MP-BGP EVPN으로 수집된 전역 테이블에서 [목적지 MAC → 수신 VTEP IP] 엔트리를 검색한다.
3. **Outer 헤더 캡슐화**: 목적지 VTEP IP를 수신자로 설정하고 Outer IP/UDP(4789번) 및 24비트 VNI 헤더( 총 50바이트 추가)를 캡슐화한다.
4. **L3 언더레이 전송**: L3 스파인-리프 인프라의 ECMP 다중 경로를 활용하여 IP 패킷을 고속 수송한다.
5. **역캡슐화 및 전달**: 수신 VTEP가 Outer 헤더를 제거(Decapsulation)하고 VNI를 확인한 뒤 원본 L2 프레임만 목적지 VM에 전달한다.

#### 한줄 요약

- 원본 프레임 발신, 송신 VTEP 매핑 조회, Unicast/BUM 캡슐화, L3 언더레이 ECMP 수송 및 수신 VTEP 역캡슐화 절차.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **VLAN 식별자(VLAN Identifier, VID)**: IEEE 802.1Q 프레임 헤더 내 12비트 크기로 위치하여 기존 L2 가상망을 구별하던 식별자이다.

</details>

| 비교 항목 | **VXLAN (Virtual Extensible LAN)** | **VLAN (Virtual Local Area Network)** |
|:---|:---|:---|
| 캡슐화 방식 | MAC-in-UDP (L4 UDP 4789번 터널링) | IEEE 802.1Q (L2 이더넷 Tagging) |
| 세그먼트 식별자 | 24비트 VNI (최대 16,777,216개 지원) | 12비트 VID (최대 4,094개 한계) |
| 전송 기반 인프라 | L3 IP 라우팅 언더레이망 (Spine-Leaf) | L2 물리 스위칭 네트워크 직접 종속 |
| 경로 효율성 | L3 ECMP 지원으로 모든 이중화 경로 100% 사용 | STP(Spanning Tree)에 의한 차단 포트 발생 |
| 제어 및 관리 | MP-BGP EVPN 연동 컨트롤 플레인 자동화 | 개별 스위치 수동 VLAN DB 및 Trunk 설정 |

> 요약: VLAN은 4,094개 수량 한계 및 STP 포트 블로킹이 발생하나, VXLAN은 1,600만 개 VNI와 L3 ECMP 대역폭 활용을 제공.

#### 한줄 요약

- VLAN은 4,094개 수량 한계 및 STP 포트 블로킹이 발생하나, VXLAN은 1,600만 개 VNI와 L3 ECMP 대역폭 활용을 제공.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **점보 프레임(Jumbo Frame / MTU Expansion)**: VXLAN 캡슐화 헤더 50바이트 오버헤드로 인한 IP 단편화를 막기 위해 언더레이 MTU를 1,550~9,216바이트로 확장하는 설정이다.

</details>

| 문제점 | 발생 원인 | 실무 대응 대책 | 기대 효과 |
|:---|:---|:---|:---|
| 캡슐화 패킷 단편화 (Fragmentation) | 50Byte 헤더 부가로 언더레이 MTU(1500b) 초과 | 언더레이 스위치/라우터 MTU 1550b 이상 점보 설정 | 패킷 분할 재조합 오버헤드 제거 및 속도 저하 차단 |
| 데이터 평면 BUM 폭주 | 목적지 MAC 미학습 시 전체 VTEP로 플러딩 | MP-BGP EVPN 및 ARP Suppression 기술 도입 | 데이터 평면 플러딩 최소화 및 언더레이 대역폭 보존 |
| 터널 캡슐화 연산 부하 | 백엔드 NIC CPU에서 캡슐화/역캡슐화 처리 | SmartNIC / DPU 하드웨어 VXLAN Offload 채택 | 호스트 CPU 사용률 절감 및 라인 레이트 처리 |
| VTEP 간 동기화 오손 | 수신 VTEP IP 정보 변경 시 오버레이 경로 차단 | BFD(Bidirectional Forwarding) 연동 ECMP 절체 | ms 단위 초고속 장애 회복 및 고가용성 보장 |

#### 한줄 요약

- 언더레이 점보 프레임(MTU 1550+ Byte) 활성화, EVPN ARP Suppression 적용, BFD 연동 ECMP 기반 가용성 확립으로 VXLAN 오버레이 완성.

## Ⅶ. 결론

- SDDC 데이터센터 가상화 구축 시 **24비트 VNI 기반 VXLAN 오버레이 도입**, **MP-BGP EVPN 제어 평면 연동**, **언더레이 MTU 점보 프레임 설정 필수**.

#### 한줄 요약

- 24비트 VNI 기반 VXLAN 오버레이 및 MP-BGP EVPN 제어 평면 수립과 점보 프레임(MTU 1550+) 설정 필수.