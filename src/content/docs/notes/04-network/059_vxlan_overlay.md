---
sidebar:
  order: 59
  label: "059. VXLAN과 오버레이 네트워크 (VXLAN Overlay Network)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "VXLAN과 오버레이 네트워크 (VXLAN Overlay Network)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-network"
weight: 59
extra:
  question_no: "059"
  source_status: "기출"
  source_history: "123회"
  priority: 50
  pr## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **가상 확장 근거리 통신망(Virtual Extensible LAN, VXLAN)**: 기존 L2 이더넷 프레임을 L4 UDP 및 L3 IP 패킷으로 캡슐화(MAC-in-UDP)하여 L3 라우팅 네트워크 상에서 논리적인 L2 오버레이 네트워크를 구축하는 광역 터널링 기술이다.
- **가상 근거리 통신망(Virtual Local Area Network, VLAN)**: 12비트 IEEE 802.1Q 태그 식별자를 활용하여 단일 물리적 L2 브로드캐스트 도메인을 논리적으로 분할하는 네트워크 가상화 기술이다.
- **사용자 데이터그램 프로토콜(User Datagram Protocol, UDP)**: 송수신 간 연결 설정 과정 없이 패킷을 빠른 속도로 전송하는 4계층 전송 프로토콜이다.
- **인터넷 프로토콜(Internet Protocol, IP)**: 패킷의 논리적 주소 지정(Addressing)과 경로 설정(Routing)을 담당하는 3계층 네트워크 프로토콜이다.
- **계층 3(Layer 3, L3 네트워크)**: IP 주소 기반의 라우팅 기능을 제공하는 OSI 3계층 네트워크 영역이다.
- **계층 2(Layer 2, L2 네트워크)**: MAC 주소 기반의 프레임 전송 및 스위칭 기능을 제공하는 OSI 2계층 네트워크 영역이다.

</details>

- 정의/개념: **VXLAN**은 이더넷 프레임을 **UDP**(Destination Port 4789) 및 **IP** 패킷으로 캡슐화(MAC-in-UDP)하여, L3 IP 라우팅 언더레이 인프라 위에 대규모 멀티테넌트 가상 L2 오버레이 네트워크를 구성하는 포장 전송 기술이다.
- 배경/필요성: 기존 **VLAN**은 12비트 VID 한계로 최대 4,094개의 세그먼트만 지원하며, 스패닝 트리 프로토콜(STP)에 따른 대역폭 손실과 L2 확장성 한계가 존재하여, 클라우드 데이터센터의 대규모 VM/컨테이너 이동성을 보장하기 위해 도입되었다.

#### 한줄 요약

- 서버의 이더넷 프레임을 UDP/IP 소포에 캡슐화하여 L3 언더레이 망을 통해 멀리 떨어진 데이터센터 간 L2 연결을 확장한다.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **VXLAN 네트워크 식별자(VXLAN Network Identifier, VNI)**: 멀티테넌트 환경에서 각각의 논리적 L2 오버레이 세그먼트를 독자적으로 구분하기 위해 사용하는 24비트 확장 식별자이다.
- **이더넷 가상 사설망(Ethernet Virtual Private Network, EVPN)**: MP-BGP 프로토콜을 활용하여 MAC/IP 주소 및 VTEP 위치 정보를 데이터 평면의 플러딩 없이 제어 평면에서 동적으로 학습·배포하는 메커니즘이다.
- **경계 경로 프로토콜(Border Gateway Protocol, BGP)**: 자율시스템(AS) 간 또는 AS 내부 라우터 간에 경로 정보 및 제어 메타데이터를 교환하는 외부 라우팅 프로토콜이다.
- **매체 접근 제어 주소(Media Access Control Address, MAC Address)**: 네트워크 인터페이스 카드(NIC)에 부여된 하드웨어 고유 식별 주소이다.
- **VXLAN 터널 종단점(VXLAN Tunnel Endpoint, VTEP)**: 원본 이더넷 프레임의 VXLAN 캡슐화(Encapsulation) 및 역캡슐화(Decapsulation)를 직접 처리하는 물리 스위치 또는 가상 스위치 장치이다.
- **등가 비용 다중 경로(Equal-Cost Multi-Path, ECMP)**: 동일한 라우팅 메트릭을 가진 복수의 L3 라우팅 경로로 트래픽을 균등하게 로드밸런싱하는 기법이다.
- **최대 전송 단위(Maximum Transmission Unit, MTU)**: 네트워크 패킷 단편화 없이 전송할 수 있는 데이터의 최대 바이트 크기이다.
- **BUM 트래픽(Broadcast, Unknown Unicast, Multicast Traffic)**: 목적지 MAC 주소를 알 수 없거나 전체 호스트에 전송해야 하여 오버레이 상에서 복제 전송이 발생하는 트래픽 종류이다.

</details>

- **VNI**는 24비트 식별자를 도입해 최대 1,600만 개(16,777,216개)의 논리 세그먼트를 분리함으로써 초대형 멀티테넌트 클라우드 환경을 지원한다.
- **VTEP**는 원본 L2 프레임에 50바이트의 Outer 헤더(UDP/IP/VXLAN)를 덧붙이는 캡슐화를 수행하고, **ECMP**를 통해 L3 언더레이의 모든 경로를 활성화하여 대역폭 사용률을 극대화한다.
- **EVPN** 제어 평면은 **BGP** Type-2/Type-3 경로를 통해 호스트의 **MAC** 및 IP 정보를 사전 배포하여 불필요한 **BUM 트래픽** 플러딩을 획기적으로 차단한다.
- VXLAN 추가 헤더 오버헤드(50바이트)로 인한 패킷 단편화를 방지하기 위해 물리 언더레이 네트워크의 **MTU**를 1,550바이트 이상(Jumbo Frame 설정)으로 확대해야 한다.

#### 한줄 요약

- 24비트 VNI로 테넌트를 분리하고 EVPN 제어 평면과 VTEP 캡슐화를 통해 L3 ECMP 경로 기반 고성능 오버레이를 구현한다.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **언더레이 네트워크(Underlay Network)**: VTEP 상호 간의 IP 도달성(IP Reachability)과 높은 전송 대역폭을 제공하는 물리적 L3 스파인-리프(Spine-Leaf) 라우팅 인프라이다.
- **오버레이 네트워크(Overlay Network)**: 물리 언더레이 인프라 상위에 VXLAN 터널을 형성하여 독립적인 L2/L3 가상 상호연결 서비스를 제공하는 논리적 네트워크이다.

</details>

- **언더레이 네트워크**는 VTEP 장비 간 완전한 IP 도달성을 보장하고, **오버레이 네트워크**는 물리 망의 토폴로지 변경 없이 독립적인 L2 방송 도메인을 논리적으로 생성한다.

```text
VXLAN 오버레이 아키텍처
├─ 제어 평면 (Control Plane)
│  └─ MP-BGP EVPN (MAC/IP 주소 동적 학습 및 라우팅 정보 배포)
└─ 데이터 평면 (Data Plane)
   ├─ 종단 호스트 (VM, Container, Bare-metal Server)
   ├─ VTEP (가상/물리 스위치 캡슐화 및 역캡슐화 처리)
   ├─ IP 언더레이 (Spine-Leaf L3 Fabric, ECMP 지원)
   └─ VXLAN 게이트웨이 (VNI 간 라우팅 및 엑스테널 L3 연결)
```

가지의 의미: Control Plane(EVPN 제어 정보 교환)과 Data Plane(실제 VXLAN 캡슐화 패킷 전송)의 기능적 분리를 나타낸다.

| 구성요소 | 책임 및 실무 역할 |
|:---|:---|
| 종단 호스트 | 원본 L2 이더넷 프레임 송수신 및 가상화 테넌트 업무 수행 |
| VTEP | VNI 매핑, 50바이트 Outer 헤더(IP/UDP/VXLAN) 캡슐화 및 역캡슐화 |
| IP 언더레이 | Spine-Leaf 구조 상에서 VTEP 간 IP 도달성 보장 및 ECMP 로드 분산 |
| EVPN 제어 평면 | BGP 기반 MAC/IP 도달성 정보 배포로 Data-Plane Flooding 예방 |
| VXLAN 게이트웨이 | 서로 다른 VNI 간 L3 라우팅(Inter-VNI Routing) 및 외부 망 연동 |

#### 한줄 요약

- EVPN 제어 평면이 수신 VTEP 위치를 미리 학습시키면 송신 VTEP가 원본 프레임을 UDP 패킷으로 감싸 L3 언더레이망으로 수송한다.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **MAC·IP 위치 경로(MAC/IP Advertisement Route)**: EVPN BGP(Type-2)를 통해 특정 호스트의 MAC/IP 주소와 이를 수용하는 VTEP IP를 매핑하여 전송하는 정보이다.
- **원격 VTEP 경로(Remote VTEP Route)**: 목적지 MAC 주소로 패킷을 보내기 위해 캡슐화 대상이 되는 원격 VTEP의 IP 주소 매핑 테이블이다.
- **VXLAN 패킷(VXLAN Encapsulated Packet)**: 원본 L2 이더넷 프레임 전면에 Outer Ethernet, Outer IP, Outer UDP, VXLAN 헤더가 부가된 캡슐화 데이터 단위이다.

</details>

```text
1. MP-BGP EVPN MAC/IP 경로 광고 (Type-2 Route)
        │
        ▼
2. 원격 VTEP 매핑 테이블 구성 (VTEP IP <-> 호스트 MAC)
        │
        ▼
송신 호스트의 원본 L2 이더넷 프레임 생성
        │
        ▼
VTEP 테이블 내 목적지 MAC 매핑 존재 여부
        ├─ 미존재: 대상 VNI의 Head-end Replication / Multicast로 BUM 플러딩
        └─ 존재: 3. VXLAN 헤더 캡슐화 (UDP 4789 지정)
                         │
                         ▼
                   IP 언더레이망을 통한 ECMP 라우팅 전송
                         │
                         ▼
                   수신 VTEP 역캡슐화 후 원본 L2 프레임 복원
                         │
                         ▼
                   목적지 호스트로 최종 L2 프레임 전달
```

### 동작 원리

1. **MAC·IP 위치 경로 광고**: 수신 VTEP는 로컬에 접속된 호스트의 MAC 및 IP 주소를 감지하고, MP-BGP EVPN Type-2 메시지를 통해 전체 VTEP에 동적으로 배포한다.
2. **원격 VTEP 경로 매핑**: 송신 VTEP는 수신한 EVPN 경로 정보를 기반으로 [목적지 MAC → 원격 VTEP IP] 매핑 테이블을 갱신한다.
3. **VXLAN 패킷 캡슐화 및 전송**: 송신 호스트가 프레임을 발신하면 VTEP가 Outer IP/UDP/VXLAN 헤더를 결합하여 언더레이 망으로 전송하고, 수신 VTEP는 이를 역캡슐화하여 실제 호스트에 전달한다.

#### 한줄 요약

- 목적지 VTEP IP를 알면 unicast 캡슐화로 직접 전송하고, 모를 경우 BUM 복제 터널 전송을 통해 트래픽을 처리한다.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **VLAN 식별자(VLAN Identifier, VID)**: IEEE 802.1Q 프레임 헤더에 위치하며 12비트로 구성된 가상 LAN 식별자이다.

</details>

| 비교 항목 | VXLAN (Virtual Extensible LAN) | VLAN (Virtual Local Area Network) |
|:---|:---|:---|
| 적용 분야 | 대규모 멀티테넌트 클라우드, SDDC, DCI 환경 | 소규모 온프레미스 기업망, 단일 L2 스위치 구간 |
| 세그먼트 식별자 | 24비트 **VNI** (최대 약 1,600만 개 지원) | 12비트 **VLAN 식별자** (최대 4,094개 지원) |
| 전송 메커니즘 | L3 IP 언더레이 기반 L2 over UDP 터널링 | 물리 L2 이더넷 트렁크 및 802.1Q 태깅 방식 |
| 경로 최적화 | L3 **ECMP** 기반 멀티패스 활성화 및 대역폭 활용 | **STP** 기반 블로킹 포트 발생으로 대역폭 제한 |
| 기술적 한계 | 50바이트 헤더 오버헤드, MTU 조정 필수, BUM 제어 필요 | 식별자 수 부족, L2 브로드캐스트 도메인 확산 한계 |

> 요약: 소규모 단일 L2 브로드캐스트 영역 분리에는 **VLAN**, 대규모 SDDC 및 L3 경계 초과 테넌트 가상화에는 **VXLAN** 패러다임을 적용한다.

#### 한줄 요약

- VLAN은 4K 개 세그먼트 한계와 STP 한계가 존재하나, VXLAN은 16M 개 VNI와 L3 ECMP 인프라를 활용하여 광역 가상화를 구현한다.

## Ⅵ. 실무 고려사항 및 대책

| 실무 문제점 | 발생 원인 | 대응 대책 및 최적화 방안 | 기대 효과 |
|:---|:---|:---|:---|
| **오버레이 패킷 폐기** | 50바이트 추가 헤더로 인해 언더레이 MTU(1500b) 초과 단편화 발생 | 언더레이 스위치 및 호스트 **MTU**를 1,550~9,216바이트(Jumbo Frame)로 일괄 확대 | 패킷 단편화 방지 및 캡슐화 오버헤드로 인한 전송 성능 저하 해결 |
| **BUM 트래픽 폭증** | 목적지 MAC 미학습 시 전체 VTEP로 브로드캐스트 복제 트래픽 가중 | Control Plane에 **MP-BGP EVPN** 및 ARP Suppression 기술 도입 | 불필요한 데이터 평면 플러딩 차단 및 언더레이 대역폭 보존 |
| **터널 단절 및 비대칭** | 언더레이 물리 링크 장애 또는 VTEP 라우팅 재수렴 지연 | **ECMP** 다중 경로 구성 및 BFD(Bidirectional Forwarding Detection) 연동 | 하위 링크 장애 시 ms 단위의 초고속 경로 전환 및 가용성 유지 |

#### 한줄 요약

- 점보 프레임 적용으로 MTU를 확보하고 EVPN 제어 평면을 적용하여 BUM 트래픽을 억제하며 ECMP로 high availability를 확보한다.

## Ⅶ. 결론

- 초거대 데이터센터 및 멀티테넌트 SDDC 네트워킹 구축 시에는 **MP-BGP EVPN** 제어 평면과 **VXLAN** 데이터 평면 터널링의 결합 구조 적용이 표준이다.

#### 한줄 요약

- 대규모 데이터센터 가상화를 위한 24비트 VNI 기반 VXLAN 오버레이 및 MP-BGP EVPN 제어 평면 통합 네트워킹 구조 수립 및 MTU 최적화 체계 적용.
��. 흐름도

<details>
<summary>핵심 용어</summary>

- **MAC•IP 위치 경로**: 종단 주소와 수용 VTEP를 연결해 EVPN으로 배포하는 정보이다.
- **원격 VTEP 경로**: 목적 MAC 주소와 해당 종단을 수용한 원격 VTEP의 대응 정보이다.
- **VXLAN 패킷**: 원본 프레임에 VNI•UDP•IP 헤더를 붙인 캡슐화 패킷이다.

</details>

```text
1. MAC•IP 위치 경로
        │
        ▼
2. 원격 VTEP 경로
        │
        ▼
송신 호스트의 이더넷 프레임
        │
        ▼
원격 VTEP 위치 보유 여부
        ├─ 없음: 대상 VNI에 BUM 복제
        └─ 있음: 3. VXLAN 패킷
                         │
                         ▼
                  원격 VTEP 역캡슐화
                         │
                         ▼
                  수신 호스트에 프레임 전달
```

### 동작 원리

1. **MAC•IP 위치 경로**: **MAC•IP 위치 경로**는 수신 VTEP가 종단 호스트의 위치를 EVPN에 광고해 만든다.
2. **원격 VTEP 경로**: **원격 VTEP 경로**는 EVPN이 목적 MAC과 원격 VTEP의 대응 정보를 배포해 만든다.
3. **VXLAN 패킷**: **VXLAN 패킷**은 송신 VTEP가 VNI•UDP•IP 헤더를 붙여 원격 VTEP로 전달한다.

#### 한줄 요약

- 목적 서버 위치를 알면 한 터널로 보내고 모르면 필요한 VTEP들에 프레임을 복제한다.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **VLAN 식별자(VLAN Identifier, VID)**: VLAN을 구분하는 12비트 식별자이다.

</details>

| 네트워크 세그먼트 | VXLAN | VLAN |
|:---|:---|:---|
| 적용 기준 | 대규모 테넌트•다중 경로 | 소규모 단일 L2 영역 |
| 핵심 특징 | 24비트 **VNI**•L3 터널 | 12비트 **VLAN 식별자**•L2 구간 |
| 한계 | MTU•BUM•제어 평면 복잡성 | 식별자 한계•광역 L2 장애 확산 |

> 요약: 소규모 단일 L2는 **VLAN**, 대규모 오버레이는 **VXLAN**가 핵심이다.

#### 한줄 요약

- 한 건물의 작은 망은 VLAN, IP망을 넘어 많은 세입자를 나누려면 VXLAN이 맞다.

## Ⅵ. 실무 고려사항 및 대책

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 캡슐화 헤더로 언더레이 MTU를 초과하면 패킷 폐기 | VXLAN 헤더를 포함해 **MTU** 설정 | 단편화•폐기를 방지해 전송 안정성 확보 |
| 미지 목적지 학습이 부족하면 BUM 복제 폭증 | EVPN으로 **MAC•IP 위치 경로** 배포 | 불필요한 복제 트래픽 감소 |
| VTEP 간 언더레이 단절로 오버레이 경로 상실 | **ECMP**•신속 장애 감지•경로 재수렴 시험 | 경로 장애 중 **오버레이** 가용성 유지 |

#### 한줄 요약

- 원래 프레임에 터널 포장이 더해져도 잘리지 않도록 물리망의 최대 패킷 크기를 키운다.

## Ⅶ. 결론

- 대규모 테넌트•L3 확장에는 **EVPN**과 **VXLAN**, 소규모 단일 구간에는 **VLAN**을 선택한다.

#### 한줄 요약

- 대규모 논리망의 이득과 터널 헤더•BUM 복제 비용을 함께 감당할 수 있어야 한다.
