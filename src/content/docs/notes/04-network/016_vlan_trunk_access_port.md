---
sidebar:
  order: 16
  label: "016. VLAN•트렁크•액세스 포트 (VLAN Trunk Access Port)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "VLAN•트렁크•액세스 포트 (VLAN Trunk Access Port)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-network"
weight: 16
extra:
  question_no: "016"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "설계형: 138회 VLAN•Trunk 설계 직접 출제"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **가상 근거리 통신망(Virtual Local Area Network, VLAN)**: 하나의 물리 스위치망을 여러 논리 구역으로 나누는 기술이다.
- **브로드캐스트 영역(Broadcast Domain)**: 브로드캐스트 프레임이 직접 도달하는 범위이다.

</details>

- 정의/개념: **VLAN**은 물리 스위치망을 여러 **브로드캐스트 영역**으로 나누는 기술이다.
- 배경/필요성: 물리망의 단일 영역만으로는 브로드캐스트를 제한하고 논리적으로 격리할 수 없다.

#### 한줄 요약

- 같은 스위치의 단말도 구역 번호가 다르면 분리하고 공용 링크에서는 프레임에 구역표를 붙여 함께 운반한다.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **액세스 포트(Access Port)**: 일반 단말의 무태그 프레임을 하나의 VLAN에 연결하는 포트이다.
- **포트 VLAN 식별자(Port VLAN Identifier, PVID)**: 무태그 프레임을 소속 VLAN에 귀속시키는 설정값이다.
- **트렁크 포트(Trunk Port)**: 여러 VLAN의 태그 프레임을 한 링크로 전달하는 포트이다.
- **IEEE 802.1Q(Institute of Electrical and Electronics Engineers 802.1Q)**: 프레임에 VLAN 식별 정보와 우선순위를 삽입하는 표준이다.
- **매체 접근 제어 주소(Media Access Control Address, MAC 주소)**: VLAN별로 학습되어 링크 인터페이스를 식별하는 주소이다.

</details>

- **VLAN** 식별자는 브로드캐스트와 **MAC 주소** 학습 범위를 분리한다.
- **액세스 포트**는 **PVID**로 무태그 프레임을 VLAN에 귀속한다.
- **트렁크 포트**는 **IEEE 802.1Q** 태그로 여러 VLAN을 구분한다.

#### 한줄 요약

- 같은 스위치라도 VLAN 간 통신은 라우터 관문을 거침이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **허용 VLAN 목록(Allowed VLAN List)**: 트렁크에서 전달할 VLAN 집합을 제한하는 설정이다.
- **네이티브 VLAN(Native VLAN)**: 트렁크의 태그 없는 프레임을 소속시키는 VLAN이다.
- **스위치 가상 인터페이스(Switched Virtual Interface, SVI)**: VLAN에 IP 주소와 다른 VLAN으로 가는 게이트웨이 기능을 제공하는 가상 인터페이스이다.
- **인터넷 프로토콜(Internet Protocol, IP)**: SVI가 VLAN 사이의 네트워크 계층 전달에 사용하는 프로토콜이다.

</details>

```text
VLAN 식별자
├── 액세스 포트•PVID
├── 트렁크•허용 목록
│   └── 네이티브 VLAN
└── SVI•게이트웨이
```

선의 의미: 액세스 포트•PVID와 트렁크•허용 목록은 VLAN 식별자를 공유하는 2계층 경계를 이루며, VLAN 식별자에는 계층 간 경로를 제공하는 SVI•게이트웨이가, 트렁크에는 무태그 분류 기준인 네이티브 VLAN이 결합되는 정적 네트워크 구조를 뜻한다.

| 구성요소 | 책임 |
|:---|:---|
| 액세스 포트•PVID | **액세스 포트**의 **PVID**로 무태그 프레임 분류 |
| VLAN 식별자 | **VLAN**별 브로드캐스트•MAC 학습 범위 구분 |
| 트렁크•허용 목록 | **트렁크 포트**에서 **허용 VLAN 목록**만 전달 |
| 네이티브 VLAN | **네이티브 VLAN**으로 트렁크의 무태그 프레임 분류 |
| SVI•게이트웨이 | **SVI**에서 **IP** 기반 VLAN 간 경로 제공 |

#### 한줄 요약

- 액세스 포트가 VLAN을 정하고 트렁크는 허용한 VLAN 태그만 운반한다.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **VLAN 태그 부착(Tag Insertion)**: 액세스에서 분류한 VLAN을 트렁크 프레임에 표시하는 동작이다.
- **VLAN 태그 제거(Tag Removal)**: 목적 액세스 포트에서 VLAN 태그를 없애는 동작이다.
- **PVID 귀속**: 액세스 포트로 들어온 무태그 프레임을 포트 VLAN에 분류하는 절차이다.
- **허용 VLAN 전달**: 트렁크의 허용 VLAN 목록을 확인하여 등록된 VLAN 프레임만 중계하는 절차이다.

</details>

```text
송신 단말의 무태그 프레임
          |
          v
     1. PVID 귀속
          |
          v
  2. VLAN 태그 부착
          |
          v
  3. 허용 VLAN 전달
          |
          +-- 허용 목록 제외 ---- 프레임 폐기
          |
          `-- 허용 목록 포함
                   |
                   v
           4. VLAN 태그 제거
                   |
                   `-- 수신 단말의 무태그 프레임
```

### 동작 원리

1. **PVID 귀속**: 무태그 프레임을 포트 VLAN에 분류한다.
2. **VLAN 태그 부착**: 식별자를 붙여 트렁크로 전달한다.
3. **허용 VLAN 전달**: 허용 목록 확인 후 목적 포트를 중계한다.
4. **VLAN 태그 제거**: 목적 액세스에서 태그를 제거한다.

#### 한줄 요약

- 입구 스위치가 구역표를 붙이고 목적 액세스 포트가 떼어 단말에 보낸다.

## Ⅴ. 종류 및 비교

| VLAN 포트 방식 | **액세스 포트** | **트렁크 포트** |
|:---|:---|:---|
| 적용 기준 | 일반 단말•단일 VLAN 연결 | 스위치 간 다중 VLAN 전달 |
| 핵심 특징 | **PVID**로 무태그 프레임 귀속 | **IEEE 802.1Q** 태그로 VLAN 구분 |
| 한계 | PVID 오류의 VLAN 오분류 | 허용•네이티브 VLAN 불일치 |

> 요약: 액세스는 단일 VLAN, 트렁크는 다수 VLAN을 처리한다.

#### 한줄 요약

- 액세스 포트는 한 구역 단말을 받고 트렁크 포트는 여러 구역 프레임을 함께 나른다.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **네이티브 VLAN 불일치**: 트렁크 양단의 무태그 프레임 소속 VLAN이 다른 상태이다.
- **접근 제어 목록(Access Control List, ACL)**: 트래픽 조건에 따라 통신을 허용하거나 차단하는 규칙 목록이다.
- **SVI ACL**: VLAN 간 네트워크 계층 경로에 적용하는 접근 제어 규칙이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| **네이티브 VLAN 불일치** | 양단 PVID•태그 정책 대조 | VLAN 혼입 방지 |
| 트렁크의 전체 VLAN 허용 | **허용 VLAN 목록**에 필요 VLAN만 등록 | 공격 노출 범위 축소 |
| 액세스 포트의 태그 수용 | 포트 유형•태그 처리 고정 | 비인가 VLAN 접속 차단 |
| SVI에서 비인가 VLAN 간 경로 허용 | **ACL** 기반 **SVI ACL**•경로 정책 적용 | 논리 격리 유지 |

#### 한줄 요약

- 공용 링크 양쪽의 허용 구역과 무태그 구역이 다르면 특정 VLAN 프레임만 사라지거나 엉뚱한 구역으로 들어간다.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **최소 VLAN 허용**: 트렁크에 업무상 필요한 VLAN만 등록하는 원칙이다.

</details>

- **최소 VLAN 허용** 원칙에 따라 단말 연결은 **액세스 포트**, 다중 VLAN 링크는 **트렁크 포트**를 선택한다.

#### 한줄 요약

- 액세스 포트는 한 구역, 트렁크는 허용된 여러 구역을 태그로 구분해 운반한다.
