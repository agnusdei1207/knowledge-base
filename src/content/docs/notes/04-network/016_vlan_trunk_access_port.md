---
sidebar:
  order: 16
  label: "016. VLAN•트렁크•액세스 포트 (VLAN Trunk Access Port)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "L2 가상 랜 및 스위치 포트 아키텍처 : VLAN•트렁크•액세스 포트"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-network"
weight: 16
extra:
  question_no: "016"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "IEEE 802.1Q 태깅, PVID, Native VLAN 및 SVI 계층간 라우팅"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **가상 로컬 영역 네트워크(VLAN, Virtual Local Area Network)**: 단일 물리적 L2 스위치 인프라 내에서 MAC 브로드캐스트 도메인을 논리적으로 분할하여 보안성과 대역폭 효율을 격리하는 네트워크 가상화 기술.
- **브로드캐스트 도메인(Broadcast Domain)**: 특정 노드가 전송한 L2 브로드캐스트 프레임(`FF:FF:FF:FF:FF:FF`)이 도달할 수 있는 논리적 네트워크 경계 범위.

</details>

- 정의/개념: 물리적 스위칭 인프라를 논리적 브로드캐스트 도메인 단위로 분할하는 **VLAN** 과, 단일 VLAN을 수용하는 **액세스 포트(Access Port)** 및 복수 VLAN 트래픽을 집적 전송하는 **트렁크 포트(Trunk Port, IEEE 802.1Q)**
- 배경/필요성: 단일 물리 LAN 세그먼트 내 브로드캐스트 트래픽 범람(Storm)을 억제하고, 물리적 배선 변경 없이 부서/용도별 논리적 보안 격리를 실현할 요구

#### 한줄 요약
- 단일 물리 스위치에서 브로드캐스트 도메인을 분할하고 액세스 및 트렁크 포트로 트래픽을 제어한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **액세스 포트(Access Port)**: 단일 VLAN에만 소속되며, 종단 단말(PC, 서버)과 통신 시 802.1Q 태그가 없는 비태그(Untagged) 프레임만을 송수신하는 포트.
- **트렁크 포트(Trunk Port)**: 스위치 간 또는 스위치와 라우터 간에 복수의 VLAN 트래픽을 단일 물리 링크로 집적 전송하기 위해 802.1Q VLAN 태그를 부착하는 포트.
- **IEEE 802.1Q**: 표준 이더넷 프레임의 출발지 MAC 주소와 이더타입 사이에 4바이트(TPID 2B + TCI 2B) VLAN 제어 헤더를 삽입하는 국제 표준 태깅 규격.

</details>

- **브로드캐스트 및 결함 도메인 격리**: VLAN별로 독립된 MAC 주소 테이블 및 브로드캐스트 영역을 할당하여 불필요한 트래픽 전파 차단
- **표준 IEEE 802.1Q 프레임 태깅**: 트렁크 링크 통과 시 12비트 VLAN ID(VID, 1~4094)를 프레임에 캡슐화하여 다중 VLAN 식별
- **L3 라우팅 연계 격리**: 서로 다른 VLAN 간 통신은 L2 스위칭으로 불가능하며, 반드시 상위 라우터나 **SVI(Switched Virtual Interface)** 를 경유하도록 강제

#### 한줄 요약
- 브로드캐스트 도메인 논리 격리, 802.1Q 태깅을 통한 트렁킹, SVI 기반 계층간 라우팅을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **포트 기본 VLAN ID(Port VLAN ID, PVID)**: 비태그(Untagged) 프레임이 액세스 포트로 인입될 때 스위치가 해당 프레임에 내부적으로 부여하는 기본 VLAN 식별자.
- **네이티브 VLAN(Native VLAN)**: 트렁크 포트에서 802.1Q 태그 없이 비태그(Untagged) 상태로 통과하도록 사전에 상호 약속된 단 하나의 기본 VLAN (기본값: VLAN 1).
- **스위치 가상 인터페이스(Switched Virtual Interface, SVI)**: L3 스위치 내부에서 특정 VLAN의 기본 게이트웨이 역할을 수행하는 논리적 L3 IP 인터페이스.

</details>

```text
[ 단말 (PC / VLAN 10) ] ── (Untagged 프레임) ──▶ [ 액세스 포트 (PVID 10) ]
                                                        │ (스위치 내부: VLAN 10 맵핑)
                                                        ▼
                                                 [ 트렁크 포트 (802.1Q) ]
                                                        │ (802.1Q 4B 태그 부착 전송)
                                                        ▼
                                                 [ 트렁크 포트 (802.1Q) ]
                                                        │ (태그 파싱)
                                                        ▼
                                                 [ SVI (L3 게이트웨이) ] ──▶ [ VLAN 20으로 L3 라우팅 ]
```

선의 의미: 단말의 비태그 프레임이 PVID에 의해 분류된 후, 트렁크 링크에서 802.1Q 태그가 부착되어 전송되고 SVI를 통해 라우팅되는 엔드투엔드 경로

| 구성요소 | 책임 | 비고 |
|:---|:---|:---|
| **액세스 포트 (Access Port)** | 종단 단말 연결, 수신 프레임에 PVID 매핑 및 송신 시 태그 제거(Untag) | 단일 VLAN |
| **트렁크 포트 (Trunk Port)** | 스위치 간 상호 연결, 802.1Q 태그 부착 및 다중 VLAN 프레임 멀티플렉싱 | 다중 VLAN (1~4094) |
| **PVID (Port VLAN ID)** | 액세스 포트로 들어오는 비태그 프레임의 소속 VLAN 결정 | 포트 기본값 |
| **Native VLAN** | 트렁크 링크 상에서 비태그 프레임이 인입되었을 때 매핑할 기본 VLAN | 양단 일치 필수 |
| **허용 VLAN 목록 (Allowed List)**| 트렁크 링크를 통과할 수 있는 VLAN ID 범위를 제한하여 불필요한 트래픽 필터링 | 대역폭 최적화 |
| **SVI (L3 가상 인터페이스)** | VLAN 간 트래픽 라우팅을 위한 L3 논리 IP 게이트웨이 제공 | Inter-VLAN 라우팅 |

#### 한줄 요약
- 액세스 포트, 트렁크 포트, PVID, Native VLAN, SVI가 결합하여 L2 격리와 L3 인터페이스를 구성한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **802.1Q 태그 필드 구조**: 2바이트 프로토콜 식별자(TPID `0x8100`)와 2바이트 제어 정보(TCI: 우선순위 PCP 3bit + 드롭 지시 DEI 1bit + VLAN ID 12bit)로 구성.

</details>

```text
1. 단말이 비태그(Untagged) 표준 이더넷 프레임을 액세스 포트로 전송
            │
            ▼
2. 스위치가 액세스 포트의 PVID(예: VLAN 10)를 확인하여 내부 스위칭 버스에 태깅
            │
            ▼
3. 트렁크 포트 송출 시 802.1Q 헤더(4바이트)를 프레임에 삽입 (Native VLAN 제외)
            │
            ▼
4. 대향 스위치가 트렁크 수신 시 Allowed List 검증 후 태그 파싱 ➔ 대상 액세스 포트 전달
            │
            ▼
5. 최종 송신 액세스 포트에서 802.1Q 태그를 제거(Strip)하고 단말로 비태그 프레임 전달
```

**동작 원리**

1. **프레임 인입**: 단말은 VLAN의 존재를 인식하지 않고 표준 프레임 전송
2. **PVID 태깅**: 스위치 인입 포트에 설정된 PVID를 기준으로 내부 포워딩 도메인 결정
3. **트렁크 전송**: 스위치 간 전송 시 802.1Q 헤더를 부착하여 VLAN ID를 보존하되, Native VLAN 트래픽은 태그 없이 전송
4. **태그 제거 및 전달**: 목적지 포트가 액세스 모드일 경우 헤더를 제거하여 순수 이더넷 프레임으로 단말에 송출

#### 한줄 요약
- 인입 시 PVID 매핑, 트렁크 송출 시 802.1Q 태깅, 대향 수신 시 태그 파싱 및 액세스 포트 태그 제거 순으로 처리된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **태그 포트(Tagged) vs 비태그 포트(Untagged)**: 프레임 전송 시 802.1Q 헤더를 포함하여 송출하는 포트 모드와 헤더를 제거하여 순수 프레임으로 송출하는 포트 모드.

</details>

| 비교 항목 | 액세스 포트 (Access Port) | 트렁크 포트 (Trunk Port) |
|:---|:---|:---|
| **수용 VLAN 수** | **단일 VLAN만 수용 (1개)** | **복수 VLAN 동시 수용 (1~4094)** |
| **802.1Q 태깅 방식** | **비태그 (Untagged 프레임 전송)** | **태그 (Tagged 프레임 전송 / Native만 Untag)** |
| **연결 대상 장비** | 일반 호스트(PC, 서버, 프린터, IP 전화기) | 네트워크 장비(스위치, 라우터, 하이퍼바이저) |
| **보안 및 제어** | 포트 보안(Port Security, MAC 제한) | **허용 VLAN 목록(Allowed VLAN List) 필터링** |
| **용도** | 단말 인입 트래픽의 VLAN 분류 | 스위칭 패브릭 간 다중 VLAN 백본 집적 |

#### 한줄 요약
- 액세스 포트는 단일 비태그 단말 연결용이며, 트렁크 포트는 다중 태그 스위치 간 백본 집적용이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Native VLAN 불일치(Native VLAN Mismatch)**: 트렁크 링크 양단의 스위치 간에 Native VLAN ID가 서로 다르게 설정되어 패킷이 비정상 VLAN으로 유입되거나 STP 루프가 발생하는 장애.
- **VLAN 호핑 공격(VLAN Hopping Attack)**: 공격자가 DTP(Dynamic Trunking Protocol)를 악용하여 트렁크 포트를 강제 협상하거나, 이중 802.1Q 태그를 삽입하여 격리된 타 VLAN으로 패킷을 탈취하는 L2 보안 위협.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 트렁크 양단 Native VLAN 불일치로 인한 타 VLAN 트래픽 유입 및 루프 | 트렁크 양단 **Native VLAN ID 통일** 및 미사용 고유 VLAN(예: 999) 할당 | 트래픽 오라우팅 방지 및 L2 프로토콜 안정성 확보 |
| DTP 자동 협상 및 이중 태깅을 악용한 **VLAN 호핑(VLAN Hopping)** 공격 | DTP 비활성화(`switchport nonegotiate`), 미사용 포트 차단 및 정적 트렁크 구성 | 비인가 트렁크 전환 차단 및 VLAN 간 보안 격리 유지 |
| 전체 VLAN 브로드캐스트가 트렁크를 통해 불필요하게 전파되어 대역폭 낭비 | 트렁크 포트에 **허용 VLAN 목록(Allowed VLAN List)** 명시적 구성 | 불필요한 브로드캐스트 플러딩 차단 및 링크 대역폭 최적화 |
| SVI 라우팅 개방으로 인한 비인가 VLAN 간 무제한 통신 발생 | SVI 인터페이스 및 VLAN 인터페이스에 **접근 제어 목록(VACL / ACL)** 적용 | 부서/보안 등급별 최소 권한 통신 통제 |

#### 한줄 요약
- Native VLAN 일치, DTP 비활성화를 통한 호핑 차단, Allowed List 필터링, SVI ACL 적용으로 L2/L3 안정성을 확립한다.

## Ⅶ. 결론

- 엔터프라이즈 네트워크의 확장성과 보안성을 달성하기 위해 **VLAN** 기반의 브로드캐스트 도메인 격리와 **IEEE 802.1Q 표준 트렁킹**을 필수 아키텍처로 적용하되, L2 보안 취약점을 방어하기 위해 **DTP 비활성화, Native VLAN 분리, Allowed List 최소화, SVI 접근 제어(ACL)** 를 통합 적용하여 고신뢰 L2/L3 네트워크 인프라를 완성

#### 한줄 요약
- VLAN 도메인 격리와 802.1Q 트렁킹 및 SVI 보안 제어를 결합하여 고신뢰 네트워크 인프라를 구현한다.
