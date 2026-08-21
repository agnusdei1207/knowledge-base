---
sidebar:
  order: 59
  label: "059. VXLAN과 오버레이 네트워크"
  badge:
    text: "기출 · 50%"
    variant: note
title: "데이터센터 오버레이 터널링 기술 : VXLAN (Virtual Extensible LAN)"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-network"
weight: 59
extra:
  question_no: "059"
  source_status: "기출"
  source_history: "135회"
  priority: 50
  priority_note: "MAC-in-UDP 캡슐화, 24비트 VNI, VTEP 터널링 및 MP-BGP EVPN 제어 평면 연동"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **VXLAN(Virtual Extensible LAN)**: 물리적 L3 IP 언더레이 네트워크 위에 L2 이더넷 프레임을 L4 UDP 패킷으로 캡슐화(MAC-in-UDP)하여 대규모 가상화 L2 오버레이 네트워크를 구축하는 표준 터널링 프로토콜 (RFC 7348).
- **언더레이(Underlay)와 오버레이(Overlay)**: 물리적 IP 라우팅 패브릭(스파인-리프 토폴로지)을 언더레이라 하고, 그 상단에 터널링으로 생성된 논리적 가상 네트워크를 오버레이라 명명.

</details>

- 정의/개념: 기존 VLAN의 4,094개 식별자 한계와 L2 STP 루프 차단에 따른 대역폭 낭비를 극복하기 위해, **24비트 VNI(1,600만 개 가상망)** 와 **MAC-in-UDP 캡슐화** 를 적용하여 물리 L3 패브릭 위에 멀티 테넌트 가상 네트워크를 구축하는 **오버레이 가상화 기술(VXLAN)**
- 배경/필요성: 대규모 퍼블릭/프라이빗 클라우드 데이터센터에서 수만 개의 독립 테넌트 격리 요구를 충족하고, L3 라우팅 도메인을 가로지르는 가상 머신(VM) 및 컨테이너의 무중단 실시간 마이그레이션(L2 이동성)을 보장할 요구

#### 한줄 요약
- L2 프레임을 UDP로 캡슐화하여 L3 언더레이 위에서 1,600만 개의 가상 L2 오버레이를 제공한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **VXLAN 네트워크 식별자(VXLAN Network Identifier, VNI)**: 24비트로 구성되어 최대 16,777,216($2^{24}$)개의 고유한 가상 L2 세그먼트를 식별하는 태그 필드.
- **VXLAN 터널 종단점(VXLAN Tunnel Endpoint, VTEP)**: 하이퍼바이저 가상 스위치(OVS) 또는 물리 ToR 스위치에 위치하여 원본 L2 프레임의 VXLAN 캡슐화 및 수신 측 역캡슐화를 전담하는 터널 게이트웨이.

</details>

- **24비트 VNI 대규모 확장성**: 기존 12비트 VLAN 대비 가상 네트워크 수용 용량을 4,096배 확장하여 클라우드 멀티 테넌시 완벽 지원
- **L3 패브릭 기반 L2 확장 (MAC-in-UDP)**: 물리 IP 라우터 망을 그대로 통과하므로 L2 스패닝 트리(STP) 링크 차단 없이 **L3 ECMP(등가 다중 경로)** 를 통한 대역폭 100% 활용
- **MP-BGP EVPN 제어 평면 결합**: 데이터 평면 플러딩(Data-Plane Flooding)에 의존하던 전통 방식 대신, BGP EVPN(RFC 8365)을 통해 MAC/IP 라우팅 정보를 사전에 제어 평면으로 동기화하여 BUM 트래픽 억제

#### 한줄 요약
- 24비트 VNI 확장성, MAC-in-UDP 터널링, L3 ECMP 활용, MP-BGP EVPN 연계를 통한 BUM 억제를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **BUM 트래픽(Broadcast, Unknown Unicast, Multicast)**: 수신지 MAC 주소가 학습되지 않아 스위치가 모든 활성 포트로 복제 전송해야 하는 플러딩 트래픽.

</details>

```text
[ 오버레이 가상 네트워크 (Overlay: VM/Container / VNI 10000, 20000) ]
   │ (원본 Ethernet 프레임)
   ▼
[ VTEP (VXLAN Tunnel Endpoint: 하이퍼바이저 OVS 또는 ToR 스위치) ]
   │ (Outer IP + Outer UDP + VXLAN Header 50B 캡슐화)
   ▼
┌────────────────────────────────────────────────────────────┐
│ [ 언더레이 물리 패브릭 (Underlay: L3 IP 스파인-리프 패브릭) ]│
│  ├─ Leaf Switch ──── (L3 ECMP 다중 링크) ────▶ Spine Switch │
│  └─ Spine Switch ─── (L3 ECMP 다중 링크) ────▶ Leaf Switch │
└─────────────────────────────┬──────────────────────────────┘
                              │ (Outer 헤더 파싱 및 역캡슐화)
                              ▼
[ 수신 VTEP ➔ 대상 가상머신 (VM B) ]
```

선의 의미: 테넌트 VM의 L2 프레임이 송신 VTEP에서 50바이트 외부 헤더로 캡슐화되어 L3 언더레이를 고속 통과한 후 수신 VTEP에서 복원되는 계층 구조

| 구성요소 | 책임 및 역할 | 비고 |
|:---|:---|:---|
| **VTEP (터널 종단점)** | 원본 L2 프레임에 Outer IP/UDP/VXLAN 헤더 캡슐화 및 역캡슐화 수행 | SW(OVS) 또는 HW(ASIC) |
| **VNI (가상망 식별자)** | 24비트 필드로 개별 가상 브로드캐스트 도메인을 1:1 식별 | VXLAN Header (8B) |
| **언더레이 패브릭** | BGP/OSPF 라우팅 및 ECMP를 통해 VTEP 간 UDP 패킷을 라인 레이트 전달 | IP 스파인-리프 |
| **MP-BGP EVPN** | 호스트 MAC/IP 바인딩을 BGP 경로(Type-2, Type-5)로 사전 광고하여 플러딩 방지 | 제어 평면 표준 |

#### 한줄 요약
- VTEP 터널 종단점, 24비트 VNI 식별자, L3 언더레이 패브릭, MP-BGP EVPN 제어 평면이 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **VXLAN 헤더 오버헤드 (총 50바이트)**: Outer Ethernet(14B) + Outer IP(20B) + Outer UDP(8B, 목적지 포트 4789) + VXLAN Header(8B)로 구성.

</details>

```text
1. 테넌트 가상머신(VM A)이 목적지 VM B의 MAC 주소를 지정하여 표준 L2 프레임 송출
            │
            ▼
2. 송신 VTEP가 MP-BGP EVPN 라우팅 테이블을 조회하여 목적지 VM B가 수용된 원격 VTEP IP 식별
            │
            ▼
3. 송신 VTEP가 원본 프레임 앞에 VXLAN 헤더(VNI 100) 및 Outer UDP/IP 헤더를 부착 (캡슐화)
            │
            ▼
4. 물리 언더레이 네트워크가 Outer IP를 기준으로 L3 스파인-리프 ECMP 경로를 통해 패킷 고속 수송
            │
            ▼
5. 수신 VTEP가 Outer 헤더를 검증 및 제거(역캡슐화) ➔ 원본 L2 프레임만 목적지 VM B로 전달
```

**동작 원리**

1. **로컬 L2 인입**: 가상 인터페이스를 통해 인입된 프레임의 VLAN ID를 VNI로 매핑
2. **원격 VTEP 식별**: EVPN 테이블을 대조하여 목적지 MAC이 위치한 원격 VTEP의 언더레이 IP 주소 검색
3. **Outer 헤더 캡슐화**: 목적지 포트 4789(IANA 표준) UDP 헤더 및 외부 IP 헤더를 삽입
4. **L3 고속 스위칭**: 언더레이 라우터들은 내부 가상화 내용을 파싱하지 않고 오직 외부 IP만으로 ECMP 라우팅
5. **역캡슐화 및 전달**: 수신 VTEP가 VNI를 확인하여 해당 테넌트 가상 포트로 원본 프레임 주입

#### 한줄 요약
- L2 프레임 인입, EVPN 기반 VTEP 매핑, 50B 캡슐화, L3 ECMP 수송, 수신 VTEP 역캡슐화 순으로 처리된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **스패닝 트리 프로토콜(STP)**: L2 스위치 네트워크에서 루프를 차단하기 위해 중복 링크를 차단(Blocking)하여 링크 대역폭의 절반을 유휴화시키는 고전적 프로토콜.

</details>

| 비교 항목 | VXLAN (오버레이 네트워크) | 전통적 VLAN (IEEE 802.1Q) |
|:---|:---|:---|
| **가상망 식별자 크기** | **24비트 VNI (최대 16,777,216개)** | **12비트 VID (최대 4,094개)** |
| **캡슐화 방식** | **MAC-in-UDP 캡슐화 (L4 페이로드 전달)** | 프레임 내 4바이트 802.1Q 태그 삽입 |
| **물리 네트워크 제약** | **L3 IP 언더레이만 구축되면 장비 무관 동작** | 물리 스위치 전 구간이 L2 링크로 직결 요구 |
| **경로 대역폭 활용** | **L3 ECMP(등가 다중 경로)로 모든 링크 100% 활용** | STP(스패닝 트리)로 인해 예비 링크 강제 차단 |
| **L2 이동성 (VM Migration)**| **L3 라우터 경계를 넘어 동일 서브넷 유지 이동** | 동일 L2 스위치 브로드캐스트 도메인 내로 제한 |

#### 한줄 요약
- VXLAN은 1,600만 세그먼트, L3 ECMP 대역폭 활용, L3 경계를 넘는 L2 이동성을 제공한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **점보 프레임(Jumbo Frame)**: 표준 MTU(1500바이트)보다 큰 최대 9000~9216바이트 크기의 이더넷 프레임을 수용하여 패킷 단편화와 CPU 인터럽트를 방지하는 설정.
- **SmartNIC / DPU 하드웨어 오프로드**: VXLAN 캡슐화/역캡슐화 연산을 호스트 CPU 대신 네트워크 가속 칩(DPU)에서 라인 레이트로 하드웨어 처리하는 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 50바이트 VXLAN 오버헤드로 인한 MTU(1500B) 초과 및 언더레이 IP 단편화 지연 | 언더레이 물리 스위치/라우터 전 구간에 **점보 프레임(MTU 1550~9000B)** 적용 | IP 패킷 단편화 원천 방지 및 전송 오버헤드 제거 |
| 목적지 미식별 시 언더레이 망으로의 무차별 BUM 멀티캐스트 플러딩 발생 | **MP-BGP EVPN 및 ARP 억제(ARP Suppression)** 제어 평면 결합 | 데이터 평면 플러딩 트래픽 90% 이상 제거 및 대역폭 보존 |
| 대규모 패킷 캡슐화/역캡슐화 연산으로 인한 호스트 서버 CPU 점유율 과다 | **SmartNIC / DPU 기반 VXLAN 하드웨어 오프로딩** 적용 | 호스트 CPU 자원 회수 및 100Gbps 라인 레이트 포워딩 |

#### 한줄 요약
- 점보 프레임으로 단편화를 방지하고, BGP EVPN으로 BUM 플러딩을 억제하며, SmartNIC으로 CPU 부하를 제거한다.

## Ⅶ. 결론

- 클라우드 데이터센터의 대규모 멀티 테넌시와 VM 무중단 마이그레이션을 구현하기 위해 **VXLAN 기반 오버레이 네트워크**를 표준으로 적용하되, 운영 오버헤드를 제어하기 위해 **언더레이 점보 프레임(MTU 9000)**, **MP-BGP EVPN 제어 평면**, **SmartNIC 가속 엔진**을 통합 구축하여 고성능·고확장성 클라우드 패브릭을 완성

#### 한줄 요약
- MAC-in-UDP 캡슐화와 MP-BGP EVPN을 결합하여 고성능 대규모 데이터센터 오버레이를 실현한다.
