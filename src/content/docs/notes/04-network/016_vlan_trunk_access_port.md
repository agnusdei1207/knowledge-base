---
sidebar:
  order: 16
  label: "016. VLAN•트렁크•액세스 포트"
  badge:
    text: "기출 · 70%"
    variant: note
title: "VLAN•트렁크•액세스 포트 (VLAN Trunk Access Port)"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 16
extra:
  question_no: "16"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "IEEE 802.1Q 태깅, PVID, Native VLAN 및 SVI 계층간 라우팅"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **VLAN (Virtual Local Area Network)**: 물리적 스위치 인프라를 논리적 브로드캐스트 도메인(1~4094)으로 분할하는 L2 가상화 기술.
- **802.1Q Trunk Port**: 단일 물리 링크를 통해 복수의 VLAN 트래픽을 4바이트 태그(TPID+TCI)를 부착하여 집적 전송하는 포트.

</details>

- 정의/개념: L2 물리 스위치를 논리적 브로드캐스트 도메인으로 분할하는 **VLAN과 단일 VLAN을 수용하는 액세스 포트 및 IEEE 802.1Q 4B 태깅을 수행하는 트렁크 포트**
- 배경/필요성: 단일 물리 LAN 내 브로드캐스트 스톰으로 인한 **대역폭 고갈, 물리 배선 변경 없는 부서별 보안 격리 불가 및 유연한 망 구성 한계 해결 불가**

#### 한줄 요약
- VLAN으로 브로드캐스트 도메인을 격리하고, 802.1Q 트렁킹으로 스위치 간 복수 VLAN을 집적 전송한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **PVID (Port VLAN ID)**: 액세스 포트로 인입되는 비태그(Untagged) 프레임에 스위치 내부적으로 부여하는 기본 VLAN ID.
- **SVI (Switched Virtual Interface)**: L3 스위치 내부에서 특정 VLAN의 기본 게이트웨이 역할을 수행하는 가상 IP 인터페이스.

</details>

- 브로드캐스트 패킷의 전파 범위를 해당 VLAN 내부로만 제한하는 **L2 도메인 격리 및 보안성 강화**
- 스위치 간 연결 시 단일 링크로 4,094개 VLAN을 다중화 전송하는 **IEEE 802.1Q 4바이트 태깅 트렁크**
- L3 스위치 내부에서 VLAN 간 트래픽을 고속 라우팅하는 **SVI(Switched Virtual Interface) Inter-VLAN**

#### 한줄 요약
- 브로드캐스트 도메인 격리, 802.1Q 다중화 트렁킹, SVI 기반 고속 Inter-VLAN 라우팅을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Native VLAN**: 트렁크 링크 상에서 802.1Q 태그 없이 비태그(Untagged) 상태로 전송하도록 약속된 기본 VLAN (양단 일치 필수, 기본 VLAN 1).

</details>

```text
[VLAN 액세스 포트, 802.1Q 트렁크 포트 및 SVI 아키텍처]
|-- Access Port (Untagged: 단말 PC 연결, PVID 10 매핑)
`-- L2 / L3 Switch A
    |-- 802.1Q Tagging Engine (4 Bytes Header: TPID `0x8100` + VID 10)
    `-- Trunk Port (Tagged Frame 송출, Native VLAN 1은 Untagged)
`-- 802.1Q Trunk Link (단일 물리 케이블로 VLAN 10, 20, 30 멀티플렉싱 전송)
`-- L3 Switch B
    |-- Trunk Port (Allowed VLAN List 검증 및 태그 파싱)
    `-- SVI Gateway (VLAN 10 IP <-> VLAN 20 IP Inter-VLAN 하드웨어 라우팅)
```

선의 의미: 계층 및 단말의 비태그 프레임이 PVID로 분류되어 트렁크에서 802.1Q 태깅되어 전송되고 SVI를 통해 라우팅되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **액세스 포트 (Access)** | 종단 단말(PC/서버) 연결, **비태그 프레임에 PVID를 매핑하고 송출 시 태그 제거(Untag)** | 단일 VLAN 수용 |
| **트렁크 포트 (Trunk)** | 스위치 간 백본 연결, **4바이트 802.1Q 태그를 부착하여 복수 VLAN 트래픽 멀티플렉싱** | 1~4094 VLAN 수용 |
| **PVID (Port VLAN ID)**| 액세스 포트로 유입되는 **비태그(Untagged) 프레임의 소속 VLAN ID 결정** | 포트 기본 속성 |
| **Native VLAN** | 트렁크 링크 상에서 **태그 없이(Untagged) 전송되는 기본 VLAN (양단 스위치 일치 필수)** | 기본값 VLAN 1 |
| **허용 VLAN 목록 (Allowed)**| 트렁크 링크를 통과할 수 있는 **VLAN ID 범위를 명시적으로 제한하여 대역폭 최적화** | 트래픽 필터링 |
| **SVI (L3 가상 인터페이스)**| L3 스위치 내부에서 **VLAN 간 패킷 라우팅을 수행하는 논리적 IP 게이트웨이 제공** | Inter-VLAN 라우팅 |

#### 한줄 요약
- 액세스 포트, 트렁크 포트, PVID, Native VLAN, Allowed List, SVI가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **802.1Q 4바이트 태그 포맷**: 2바이트 TPID (`0x8100`) + 2바이트 TCI (PCP 우선순위 3bit + DEI 1bit + VLAN ID 12bit).

</details>

```text
VLAN 프레임 생성 및 트렁크 전송 파이프라인
        │
   1. [단말 비태그 송신] PC가 일반 이더넷 프레임을 스위치 1번 포트(액세스)로 전송
        │
   2. [PVID 태깅] 스위치 1번 포트의 PVID(VLAN 10)를 확인하여 내부 스위칭 버스에 태깅
        │
   3. [트렁크 포트 송출] 스위치 간 트렁크 링크 통과 시 4바이트 802.1Q 헤더 삽입 (Native 제외)
        │
   4. [대향 스위치 수신] 트렁크 포트에서 Allowed List 검증 후 802.1Q 태그 파싱 (VLAN 10 확인)
   ┌────┴───────────────────────────┐
  동일 VLAN 목적지 포트 도착      타 VLAN(VLAN 20) 목적지 통신
   │                                 │
5A. [태그 제거 및 단말 전달]         5B. [SVI Inter-VLAN L3 라우팅]
   802.1Q 태그 제거 후 비태그 송출       SVI 게이트웨이를 통해 VLAN 20으로 라우팅 전달
```

#### 한줄 요약
- 인입 시 PVID 매핑 → 트렁크 802.1Q 태깅 → 대향 수신 태그 파싱 → 태그 제거 단말 송출 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Access Port vs Trunk Port**: 단일 VLAN 비태그 포트(Access)와 복수 VLAN 802.1Q 태그 포트(Trunk).

</details>

| 비교 항목 | 액세스 포트 (Access Port) | 트렁크 포트 (Trunk Port) |
|:---|:---|:---|
| **수용 가용 VLAN 수** | **단일 VLAN만 수용 (1개)** | **복수 VLAN 동시 수용 (1~4094개)** |
| **802.1Q 태깅 동작** | **비태그 전송 (Untagged Frame)** | **태그 부착 전송 (Tagged Frame / Native만 Untag)** |
| **물리 연결 대상 장비**| 일반 호스트 (PC, 서버, 프린터, IP 전화기) | **네트워크 장비 (스위치, 라우터, 하이퍼바이저)** |
| **주요 보안 제어 기법**| **Port Security (MAC 학습 제한, Sticky)** | **허용 VLAN 목록 (Allowed VLAN List) 필터링** |
| **주요 엔지니어링 목적**| 종단 단말의 VLAN 소속 분류 | **스위칭 패브릭 간 다중 VLAN 백본 집적** |

#### 한줄 요약
- 액세스 포트는 단일 단말 연결용이며, 트렁크 포트는 다중 VLAN 스위치 백본 집적용이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **VLAN Hopping Attack**: 공격자가 DTP(Dynamic Trunking Protocol)를 악용해 트렁크를 강제 협상하거나, 802.1Q 이중 태깅(Double Tagging)으로 격리된 타 VLAN 패킷을 가로채는 공격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 트렁크 양단 Native VLAN 불일치로 인한 타 VLAN 트래픽 유입 및 루프 | **트렁크 양단 `Native VLAN ID 통일` 및 미사용 전용 VLAN(예: 999) 격리** | 트래픽 오라우팅 방지 및 L2 루프 차단 |
| DTP 협상 및 이중 태깅을 악용한 **VLAN Hopping 공격** | **DTP 비활성화(`switchport nonegotiate`) 및 정적 트렁크 고정** | 비인가 트렁크 전환 차단 및 VLAN 보안 유지 |
| 전체 VLAN 브로드캐스트가 트렁크를 통해 불필요하게 전파되어 대역폭 낭비 | **트렁크 포트에 `Allowed VLAN List (예: 10,20,30)` 명시적 필터링** | 불필요한 브로드캐스트 플러딩 차단 및 대역폭 절약 |
| SVI 인터페이스 개방으로 인한 비인가 VLAN 간 무제한 접근 발생 | **SVI 인터페이스 및 VLAN 인터페이스에 `VACL / L3 ACL` 적용** | 부서/보안 등급별 최소 권한 통제 확립 |

#### 한줄 요약
- Native VLAN 일치, DTP 비활성화, Allowed List 필터링, SVI VACL 제어로 운영한다.

## Ⅶ. 결론

- 대규모 엔터프라이즈 네트워크의 확장성과 보안성을 확보하기 위해 **VLAN 기반의 L2 브로드캐스트 도메인 격리와 IEEE 802.1Q 트렁크 설계를 표준 채택**하고, **DTP 비활성화, Native VLAN 격리, Allowed List 최소화 및 SVI VACL 방화벽 연동**을 결합하여 강력한 제로 트러스트 L2/L3 네트워크 인프라 완성

#### 한줄 요약
- VLAN과 802.1Q 트렁킹 및 SVI 라우팅을 통해 브로드캐스트 도메인을 논리 분할하고 트래픽을 안전하게 집적·전달하는 핵심 L2 가상화 기술이다.