---
title: "480. VxLAN 오버레이 네트워크 멀티 테넌트 (VxLAN Overlay Network Multi Tenant)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: VxLAN(Virtual Extensible LAN, RFC 7348)은 24비트 VNI(VxLAN Network Identifier)를 통해 16M개의 논리적 L2 세그먼트를 제공하며, MAC-in-UDP 캡슐화(Encapsulation)를 통해 L3 Underlay 네트워크 위에서 확장 가능한 멀티 테넌트 오버레이를 구성하는 네트워크 가상화 기술이다.
> 2. **가치**: 기존 VLAN의 4,094개 세그먼트 한계를 16M으로 확장하고, EVPN(Ethernet VPN, RFC 7432) 기반 BGP(Border Gateway Protocol) 제어 평면을 결합하여 MAC 학습의 BUM(Broadcast, Unknown unicast, Multicast) Flood-and-Learn 문제를 Type-2/Type-3 경로로 해결, 데이터센터 Spine-Leaf 패브릭에서 테넌트당 독립된 L2/L3 도메인을 제공한다.
> 3. **판단 포인트**: Multi-Tenancy 구현 시 Tenant-VRF(Virtual Routing and Forwarding) ↔ VNI 매핑 정책, L2VNI(브리지 도메인)/L3VNI(VRF 라우팅) 분리 여부, Ingress Replication vs Multicast Underlay, Anycast Gateway 배치, RT(Route Target) 설계, 그리고 MTU 50Byte 오버헤드(Outer IP 20+UDP 8+VXLAN 8+Inner Ethernet 14 = 50 Bytes) 대응이 핵심 의사결정 사안이다.

---

## Ⅰ. 개요 및 필요성

기존 데이터센터는 STP(Spanning Tree Protocol) 기반의 L2 도메인을 VLAN(802.1Q, 12비트 VID)으로 분할하여 운용했으나, 최대 4,094개의 세그먼트 제한, STP에 의한 블록 포트(50% 대역폭 손실), 그리고 L2 도메인의 데이터센터 간 확장이 불가능한 한계가 존재했다. 클라우드 및 대규모 멀티 테넌트 환경에서는 수백~수천 개의 고객/조직/프로젝트를 동시에 수용해야 하므로 VLAN만으로는 Tenant 분리 요구사항을 충족할 수 없게 되었다.

VxLAN은 IETF RFC 7348로 표준화되었으며, 원래의 L2 이더넷 프레임을 UDP(User Datagram Protocol) 페이로드로 캡슐화하고 Outer IP 헤더를 통해 L3 Underlay 망으로 전달한다. 이 구조는 L2 도메인을 IP 라우팅이 가능한 모든 위치로 확장할 수 있게 해주며, 24비트 VNI 공간(2^24 = 16,777,216개)을 통해 이론적으로 1,600만 개 이상의 독립된 Tenant 세그먼트를 제공한다. 여기에 EVPN을 제어 평면으로 채택하면, 데이터 평면의 Flood-and-Learn 동작을 BGP 경로 배포로 대체하여 효율적인 MAC/IP 학습과 Tenant 간 경로 분리가 가능하다.

```text
[ VxLAN 캡슐화 구조 (MAC-in-UDP Encapsulation) ]

  +-------------------+-------------------+--------------------+---------------------+----------------+
  | Outer Dst MAC (14B)| Outer Src MAC     | Outer IPv4 (20B)   | Outer UDP (8B)      | VxLAN Header    |
  | Outer EtherType    |                   | TTL/Proto=UDP      | Dst Port 4789       | + Inner Payload |
  +-------------------+-------------------+--------------------+---------------------+----------------+
   <---------- Underlay L2 Header -------->  <-- Underlay L3 -->  <-- UDP -->         <--- Overlay --->
   Outer DMAC = Next-hop VTEP MAC           Src/Dst IP=VTEP IP   Src=Random/Entropic  VNI 24bit, Flags
                                                                                       50 Byte overhead total

[ 멀티 테넌트 VxLAN 오버레이 개념도 ]

                +---- Tenant-A VNI 10001 (L2VNI) ----+    +---- Tenant-B VNI 20001 ----+
                |  Subnet 10.1.1.0/24  (Web Tier)  |    |  Subnet 10.2.1.0/24         |
                |  Subnet 10.1.2.0/24  (App Tier)  |    |  Subnet 10.2.2.0/24         |
                +---- L3VNI 100000 (Tenant-A VRF) -+    +-- L3VNI 200000 (Tenant-B VRF)-+
                            \                       \  /                          /
                             \   EVPN Type-2/3/5    \/    EVPN Type-2/3/5        /
                              \   (BGP Route)      /\    (BGP Route)           /
                               \                  /  \                        /
                          +-----+----------------+----+-----------------+-----+
                          |  Leaf-1 (VTEP)        |     Leaf-2 (VTEP)   |
                          |  Tenant-A: VNI 10001  |     Tenant-B: VNI   |
                          |  Tenant-B: VNI 20001  |     20001            |
                          +-----------------------+----------------------+
                                          |            |
                              +-----------+------------+
                              |  Spine-1   Spine-2    |  (Anycast Loopback, eBGP)
                              +-------+---------------+
                                      |
                              [ L3 Underlay IP Fabric ]
```

기존의 1:1 VLAN 매핑 및 STP 기반 구조에서는 Tenant 추가 시마다 VLAN ID를 점진적으로 고갈시키고, STP 토폴로지 재계산으로 인한 트래픽 손실이 불가피했다. VxLAN-EVPN 멀티 테넌트 구조에서는 Tenant 추가가 BGP 경로 업데이트와 VTEP(VxLAN Tunnel Endpoint) 설정 변경만으로 처리되며, STP는 완전히 제거되어 모든 링크가 Active/Active로 동작한다. 이를 통해 Tenant별 독립된 L2 도메인을 L3 라우팅 가능한 임의의 Underlay 위에 오버레이 형태로 구성할 수 있다.

- **📢 섹션 요약 비유**: 기존 VLAN 방식이 아파트 단지 내 4094개 호수만 표기할 수 있는 좁은 번호판이라면, VxLAN 멀티 테넌트는 1,600만 호가 넘는 광역 택지개발 신도시의 주소 체계와 같다. 각 테넌트(단지)는 자신만의 VNI(동·호수)를 부여받고, 우편배달부(Underlay IP 라우터)는 단지 내 상세 주소(MAC/IP)를 알 필요 없이 단지 번호(VNI)와 택배함 위치(VTEP)만으로 정확히 전달한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

EVPN-VxLAN 멀티 테넌트 아키텍처는 크게 **Underlay 네트워크**(Spine-Leaf IP 패브릭), **Overlay 네트워크**(VxLAN 터널), **제어 평면**(BGP EVPN), **데이터 평면**(VTEP), 그리고 **Tenant 분리 메커니즘**(VRF/VNI/RT)의 5개 계층으로 구성된다.

```text
[ EVPN-VxLAN Multi-Tenant 상세 아키텍처 ]

  Tenant-A                                  Tenant-B
  +-------+-------+-------+                +-------+-------+-------+
  |Web    |App    |DB     |                |Web    |App    |DB     |
  |VLAN 11|VLAN 12|VLAN 13|                |VLAN 21|VLAN 22|VLAN 23|
  |.1.0/24|.2.0/24|.3.0/24|                |.1.0/24|.2.0/24|.3.0/24|
  +---+---+---+---+---+---+                +---+---+---+---+---+---+
      |       |       |                        |       |       |
  +---+-------+-------+-------+         +------+-------+-------+----+
  |        Leaf-1 (VTEP-A1)         |         |        Leaf-3 (VTEP-B1)       |
  |  Lo0=10.0.0.11/32 (AnycastGW)  |         |  Lo0=10.0.0.13/32               |
  |  Tenant-A: VNI 10001, 10002    |         |  Tenant-B: VNI 20001, 20002    |
  |  Tenant-B: VNI 20001 (Shared)  |         |  Tenant-A: VNI 10001 (Shared)  |
  |  VRF Tenant-A: L3VNI 100000    |         |  VRF Tenant-A: L3VNI 100000    |
  |  VRF Tenant-B: L3VNI 200000    |         |  VRF Tenant-B: L3VNI 200000    |
  +-----------+--------------------+         +-----------------+--------------+
              |  |                                          |  |
   eBGP       |  |  P2P Link (eBGP)                       |  |  eBGP
   over       |  +----------------------+------------------+  |  over
   Loopback   |                         |                     |  Loopback
              |       +-----------------+----------------+    |
              |       |                                  |    |
              |  +----+----+    +-------+    +----+----+  |    |
              |  |Spine-1  |    |Spine-2|    | Spine-3 |  |    |
              |  |10.0.0.1 |    |.0.0.2 |    | .0.0.3  |  |    |
              |  +---------+    +-------+    +---------+  |    |
              |     eBGP RR (Route Reflector Cluster)    |    |
              |                                           |    |
              +-------+-----------------------+-----------+----+
                      |                       |
              +-------+-------+       +-------+-------+
              |   Leaf-2      |       |   Leaf-4      |
              |  (VTEP-A2)    |       |  (VTEP-B2)    |
              |  Shared Svc   |       |  Standalone   |
              +---------------+       +---------------+

  EVPN RT 설계:
    Tenant-A VRF:  RT 65000:100001 (Import/Export 동일)
    Tenant-B VRF:  RT 65000:200001
    Shared Svc:    RT 65000:99999   (모든 Tenant Import)
```

**핵심 동작 메커니즘:**

1. **캡슐화/디캡슐화**: Leaf 스위치의 VTEP는 호스트에서 수신한 일반 이더넷 프레임에 VxLAN Header(8 Bytes: Flags 1B + Reserved 3B + VNI 3B + Reserved 1B)를 추가하고, UDP 헤더(Source: VTEP IP Hash, Dest: 4789), Outer IP 헤더, Outer Ethernet 헤더를 순차로 더해 Underlay로 포워딩한다. 수신측 VTEP는 Outer 헤더를 제거하고 원본 프레임을 호스트에 전달한다.

2. **BUM 트래픽 처리**: ARP 요청, 알 수 없는 유니캐스트, 브로드캐스트는 Head-End Replication(또는 Ingress Replication) 방식으로 동일 Tenant VNI의 모든 원격 VTEP에 유니캐스트 복제되어 전달된다. EVPN Type-3(IMET, Inclusive Multicast Ethernet Tag) 경로가 각 VTEP의 PMSI(Provider Multicast Service Interface) 정보를 광고하여, 데이터 평면의 멀티캐스트 그룹이나 유니캐스트 복제 대상 리스트를 구성한다.

3. **EVPN 경로 타입 (RFC 7432 + Extensions)**:
   - **Type-1 (Ethernet Auto-Discovery)**: 이더넷 세그먼트(ESI, Ethernet Segment Identifier) 알림, Multi-homing(All-Active) ALB(Anycast Loopback) 구성
   - **Type-2 (MAC/IP Advertisement)**: 호스트의 MAC + IP(IPv4/IPv6) + L2VNI + L3VNI를 광고, MAC 학습을 BGP로 대체
   - **Type-3 (Inclusive Multicast Ethernet Tag)**: BUM 트래픽 복제 대상 VTEP 리스트
   - **Type-5 (IP Prefix Route)**: L3VNI(Inter-Subnet) 라우팅, Tenant VRF 간 또는 외부 네트워크 Prefix 광고

4. **멀티 테넌트 분리 메커니즘**:
   - **VNI 공간 분리**: 각 Tenant는 고유한 L2VNI(예: 10001, 20001)와 L3VNI(예: 100000, 200000)를 부여받음
   - **VRF 분리**: Tenant별 VRF 인스턴스를 생성하고 L3VNI와 1:1 매핑
   - **RT(Route Target)**: BGP Extended Community로, `Target:100001`을 Export/Import 정책으로 활용하여 Tenant 간 경로 격리
   - **RD(Route Distinguisher)**: 동일 Tenant 내에서도 VPNv4/v6 주소 충돌 방지를 위해 VPNv4 경로 Prefix 앞에 8Byte RD 부착

5. **Anycast Gateway (DAG, Distributed Anycast Gateway)**: 모든 Leaf에 동일한 Anycast Gateway IP/MAC을 가상 게이트웨이로 설정(예: 10.1.1.1/24, MAC 0000.1111.1111). 호스트가 어느 Leaf에 접속하든 동일한 GW에 도달하며, Leaf 간 호스트 이동 시 ARP/GW 재설정이 불필요하다. L3VNI를 통해 Leaf-to-Leaf VXLAN 터널로 직접 라우팅된다(Stretched L3 Gateway, No Subnet Stickiness).

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **VTEP (VxLAN Tunnel Endpoint)** | 캡슐화/디캡슐화 수행, VNI ↔ Tenant 매핑 | Loopback 인터페이스(보통 /32) IP로 식별, 동일 Leaf 내에서도 VRF별로 NVE(Network Virtualization Edge) 인터페이스가 생성됨. Hardware-based VTEP(ASIC)와 Software-based VTEP(OVS/DPDK) 구분 |
| **Spine (Super-Spine)** | Underlay 라우팅, eBGP Route Reflector 역할 | Tenant/VXLAN 정보를 알지 못하며 순수 IP 라우터로 동작. eBGP 패밀리 `evpn`(AFI 25/SAFI 70) 및 `ipv4/ipv6 unicast`
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 480 / 800

<- **이전**: [479. 클라우드 네트워크 SDN NFV 가상화](/studynote/13_cloud_architecture/06_exam_summary/479_cloud_network_sdn_nfv_virtualization/)
**다음**: [481. SD-WAN 소프트웨어 정의 광역 네트워크](/studynote/13_cloud_architecture/06_exam_summary/481_sd_wan_software_defined_wide_area_network/) ->

---
