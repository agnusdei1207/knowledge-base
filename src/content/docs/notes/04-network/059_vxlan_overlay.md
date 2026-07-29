---
sidebar:
  order: 59
  label: "059. VXLAN과 오버레이 네트워크 (VXLAN Overlay Network)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "VXLAN과 오버레이 네트워크 (VXLAN Overlay Network)"
date: "2026-07-29T23:30:00+09:00"
tags:
  - "notes-network"
weight: 59
extra:
  question_no: "059"
  source_status: "기출"
  source_history: "123회"
  priority: 50
  priority_note: "설계형: 123회 VXLAN과 EVPN 통합 우산"
---

## 미리 알고가기

- **가상 확장 근거리망(Virtual eXtensible Local Area Network, VXLAN)**: 이더넷 프레임을 UDP/IP로 캡슐화해 3계층망 위에 2계층 오버레이를 만드는 기술
- **VXLAN 네트워크 식별자(VXLAN Network Identifier, VNI)**: VXLAN 논리 세그먼트를 구분하는 24비트 식별자
- **VXLAN 터널 종단점(VXLAN Tunnel Endpoint, VTEP)**: 이더넷 프레임의 VXLAN 캡슐화·역캡슐화를 수행하는 장치
- **이더넷 가상 사설망(Ethernet Virtual Private Network, EVPN)**: BGP로 MAC·IP와 VTEP 위치 정보를 배포하는 제어 평면
- **언더레이(Underlay)**: VTEP 사이 IP 도달성과 물리 전송 경로를 제공하는 기반망
- **오버레이(Overlay)**: 언더레이 위의 터널로 논리적 연결과 테넌트 분리를 제공하는 가상망
- **동일 비용 다중 경로(Equal-Cost Multi-Path, ECMP)**: 비용이 같은 여러 IP 경로로 흐름을 분산하는 방식
- **방송·미상 유니캐스트·멀티캐스트(Broadcast, Unknown Unicast, Multicast, BUM)**: 목적 VTEP를 하나로 정할 수 없어 복제 전달이 필요한 트래픽
- **최대 전송 단위(Maximum Transmission Unit, MTU)**: 한 링크에서 분할 없이 보낼 수 있는 최대 패킷 크기
- **VXLAN·VNI·VTEP·EVPN**: VXLAN은 L2 프레임을 L3망에 캡슐화하고, VNI는 논리망을 식별하며, VTEP는 터널을 종단하고, EVPN은 단말 위치와 경로를 배포함
- **UDP·IP·BGP·MAC·ECMP·BUM·MTU**: VXLAN의 캡슐화 전송·경로 배포·주소 식별·다중 경로·복제 트래픽·패킷 크기를 구성하는 기반 요소
- **계층 기호(L2·L3, 엘투·엘쓰리)**: Layer의 L과 계층 번호를 결합한 표기이며, L2는 이더넷 전달, L3는 IP 라우팅 계층을 뜻함

## Ⅰ. 개요

- 정의/개념: 이더넷 프레임을 **UDP/IP로 캡슐화한 L2 오버레이**
- 배경/필요성: VLAN은 **12비트 식별자·L2 장애 범위 확장 한계**

### 쉽게 이해하기 (학습용)

- 서버의 이더넷 프레임을 IP 소포에 넣어 멀리 떨어진 데이터센터 스위치까지 운반한다

## Ⅱ. 특징

- **24비트 VNI**로 대규모 테넌트 논리망을 분리한다.
- **VTEP의 UDP/IP 캡슐화**로 L3 언더레이·ECMP를 활용한다.
- **EVPN 위치 배포**는 BUM을 줄이나 캡슐화 MTU가 필요하다.

### 쉽게 이해하기 (학습용)

- VNI가 같은 세입자끼리 묶고 EVPN이 목적 서버가 어느 터널 끝에 있는지 알려 준다

## Ⅲ. 구조 및 구성요소

```mermaid
block
    columns 1
    A["VTEP | VNI별 캡슐화·역캡슐화"]
    B["IP 언더레이 | VTEP 도달성·ECMP 제공"]
    C["EVPN 제어 평면 | MAC·IP·VTEP 위치 배포"]
    D["VXLAN 게이트웨이 | VNI 간 패킷 라우팅"]
    A --- B
    B --- C
    C --- D
```

| 구성요소 | 책임 |
|:---|:---|
| VTEP | VNI별 캡슐화·역캡슐화 |
| IP 언더레이 | VTEP 도달성·ECMP 제공 |
| EVPN 제어 평면 | MAC·IP·VTEP 위치 배포 |
| VXLAN 게이트웨이 | VNI 간 패킷 라우팅 |

### 쉽게 이해하기 (학습용)

- EVPN이 목적 서버의 터널 끝을 알려 주면 송신 VTEP가 프레임을 싸서 IP망으로 보낸다

## Ⅳ. 흐름도

```mermaid
sequenceDiagram
    participant 수신VTEP
    participant EVPN
    participant 송신VTEP
    participant 송신호스트
    수신VTEP->>EVPN: 1. EVPN MAC·IP 경로 광고
    EVPN->>송신VTEP: 2. 원격 MAC·VTEP 경로 배포
    송신호스트->>송신VTEP: 3. 이더넷 프레임 전달
    송신VTEP->>EVPN: 4. VNI·목적 MAC 조회
    송신VTEP->>수신VTEP: 5. UDP/IP VXLAN 캡슐화
```

**동작 원리**

1. **EVPN MAC·IP 경로 광고**: 수신 VTEP가 종단 위치를 광고
2. **원격 MAC·VTEP 경로 배포**: EVPN이 송신 VTEP에 경로 전달
3. **이더넷 프레임 전달**: 송신 호스트가 원래 프레임 전송
4. **VNI·목적 MAC 조회**: 설치된 경로로 원격 VTEP 확인
5. **UDP/IP VXLAN 캡슐화**: VNI·UDP·IP 헤더를 붙여 전달

### 쉽게 이해하기 (학습용)

- 목적 서버 위치를 알면 한 터널로 보내고 모르면 필요한 VTEP들에 프레임을 복제한다

## Ⅴ. 종류 및 비교

| 네트워크 세그먼트 | VXLAN | VLAN |
|:---|:---|:---|
| 적용 기준 | 대규모 테넌트·다중 경로 | 소규모 단일 L2 영역 |
| 핵심 특징 | 24비트 VNI·L3 터널 | 12비트 VID·L2 구간 |
| 한계 | MTU·BUM·제어 평면 복잡성 | 식별자·장애 범위 확장 한계 |

> 요약: 소규모는 VLAN, 대규모 오버레이는 VXLAN이다

### 쉽게 이해하기 (학습용)

- 한 건물의 작은 망은 VLAN, IP망을 넘어 많은 세입자를 나누려면 VXLAN이 맞다

## Ⅵ. 실무 고려사항 및 대책

| 고려사항 | 대책 | 효과 |
|:---|:---|:---|
| 캡슐화 MTU 초과 | VXLAN 헤더 포함 언더레이 MTU | 단편화·폐기 방지 |
| 미지 목적지 BUM 폭증 | EVPN MAC·IP 경로 배포 | 복제 트래픽 감소 |
| VTEP 언더레이 단절 | ECMP·BFD·경로 재수렴 시험 | 오버레이 가용성 |

### 쉽게 이해하기 (학습용)

- 원래 프레임에 터널 포장이 더해져도 잘리지 않도록 물리망의 최대 패킷 크기를 키운다

## Ⅶ. 결론

- **VNI·EVPN·언더레이 MTU를 검증한 VXLAN 오버레이**

### 쉽게 이해하기 (학습용)

- 대규모 논리망의 이득과 터널 헤더·BUM 복제 비용을 함께 감당할 수 있어야 한다.
