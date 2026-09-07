---
sidebar:
  order: 16
  label: "016. VLAN•트렁크•액세스 포트"
  badge:
    text: "기출 · 70%"
    variant: note
title: "VLAN•트렁크•액세스 포트 (VLAN Trunk Access Port)"
date: "2026-09-07T14:00:00+09:00"
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
- 배경/필요성: 단일 물리 스위치 인프라에서 모든 호스트가 동일한 브로드캐스트 도메인에 속함에 따라 발생하는 브로드캐스트 스톰(Storm) 대역폭 잠식, 도청 및 무단 횡적 이동(Lateral Movement) 보안 취약점, 그리고 조직 변경 시 물리적 배선 재공사의 막대한 비용 한계를 극복하기 위해, 물리 포트를 논리적 브로드캐스트 도메인(1~4094)으로 격리하는 VLAN과 단일 단말용 액세스 포트, 복수 VLAN을 단일 링크로 집적 전송하는 IEEE 802.1Q 4바이트 태깅 트렁크 포트 및 L3 SVI 라우팅 기술을 도입하여 **네트워크 자원의 유연한 가상화 분할과 부서/보안 등급별 트래픽 격리 통제**를 달성할 필요

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
[VLAN 및 802.1Q 트렁킹 아키텍처]
  │
  ├─ [단말 접속부 (Access Port)] (Untagged 처리)
  │     ├─ 단말 인터페이스 연결 (PC, 서버, 프린터)
  │     ├─ PVID 매핑 (유입 비태그 프레임에 소속 VLAN ID 할당)
  │     └─ 태그 제거 송출 (단말 방향 송출 시 VLAN 태그 탈락)
  │
  ├─ [스위치 백본부 (Trunk Port)] (Tagged 멀티플렉싱)
  │     ├─ IEEE 802.1Q 태깅 엔진 (4B 태그: TPID 0x8100 + VID 12bit)
  │     ├─ Native VLAN 제어 (트렁크 구간 비태그 전송 기본 VLAN)
  │     └─ Allowed VLAN 필터 (통과 허용 VLAN 목록 명시적 제한)
  │
  └─ [VLAN 간 라우팅부 (Inter-VLAN)] (L3 스위칭)
        ├─ SVI (Switched Virtual Interface, 논리 게이트웨이 IP)
        └─ L3 라우팅 엔진 (ASIC 기반 VLAN 간 라인레이트 라우팅)
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| 액세스 포트 (Access) | 종단 단말 연결, 비태그 프레임에 PVID 매핑 및 송출 시 태그 제거 |
| 트렁크 포트 (Trunk) | 스위치 간 백본 연결, 4바이트 802.1Q 태그를 통한 복수 VLAN 다중화 전송 |
| PVID (Port VLAN ID) | 액세스 포트로 유입되는 비태그 프레임의 소속 VLAN ID 결정 |
| Native VLAN | 트렁크 링크 상에서 태그 없이(Untagged) 전송되는 기본 VLAN |
| 허용 VLAN 목록 (Allowed) | 트렁크 링크를 통과할 수 있는 VLAN 범위를 제한하여 대역폭 최적화 |
| SVI (L3 가상 인터페이스) | L3 스위치 내부에서 VLAN 간 패킷 라우팅을 수행하는 논리적 게이트웨이 제공 |

#### 한줄 요약
- 802.1Q 태그가 프레임 안에 소속 도메인을 실어 나르므로, VLAN마다 따로 깔아야 했을 물리 링크를 트렁크 한 가닥과 양단의 PVID·허용 VLAN 목록 설정이 대신한다.

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
- 같은 VLAN이면 태그만 떼어 L2에서 끝나지만 다른 VLAN이면 SVI를 경유하는 L3 라우팅 비용이 더해지므로, 도메인을 잘게 쪼갤수록 격리는 얻고 게이트웨이 부하는 늘어난다.

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

- 캠퍼스 엔터프라이즈망부터 서버 가상화 하이퍼바이저 및 쿠버네티스 CNI 오버레이에 이르기까지 **L2 네트워크 세그멘테이션과 멀티테넌트 트래픽 격리의 가장 기본적이고 확고한 인프라 표준**으로 자리잡았으며, 실무 구축 시에는 **VLAN Hopping 공격을 차단하기 위한 DTP 비활성화(switchport nonegotiate) 및 Native VLAN 전용 격리, 트렁크 대역폭을 보호하는 Allowed VLAN List 명시적 제한, VLAN 간 트래픽을 정밀 통제하는 SVI VACL(VLAN Access Control List) 및 방화벽 연계**를 결합하여 제로트러스트 마이크로세그멘테이션의 기틀을 완성

#### 한줄 요약
- VLAN과 802.1Q 트렁킹 및 SVI 라우팅을 통해 브로드캐스트 도메인을 논리 분할하고 트래픽을 안전하게 집적·전달하는 핵심 L2 가상화 기술이다.
