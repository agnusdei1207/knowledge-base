---
sidebar:
  order: 16
  label: "016. VLAN•트렁크•액세스 포트 (VLAN Trunk Access Port)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "VLAN•트렁크•액세스 포트 (VLAN Trunk Access Port)"
date: "2026-08-13T16:33:00+09:00"
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

<details><summary>용어 설명</summary>

- **가상 근거리 통신망(Virtual Local Area Network, VLAN)**: 물리적 스위치 토폴로지와 무관하게 L2 스위치 상에서 논리적으로 브로드캐스트 도메인을 분할하는 네트워크 가상화 기술.
- **브로드캐스트 영역(Broadcast Domain)**: 스위치 단에서 발송된 브로드캐스트 패킷(FF:FF:FF:FF:FF:FF)이 직접 도달하는 L2 논리적 통신 범위.

</details>

- 정의/개념: L2 브로드캐스트 영역을 논리 분할하는 **VLAN**
- 배경/필요성: 단일 물리망은 **브로드캐스트•부서 트래픽 격리 불가**

#### 한줄 요약

- L2 브로드캐스트 도메인 분리 및 논리적 VLAN 격리 아키텍처 구현.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **액세스 포트(Access Port)**: PC, 서버 등 일반 단말과 연결되어 단 하나의 VLAN(Untagged)에만 속하는 스위치 물리 포트.
- **포트 VLAN 식별자(Port VLAN Identifier, PVID)**: Access Port로 유입되는 일반 프레임(Untagged Frame)에 내부적으로 부여할 기본 VLAN ID 값.
- **트렁크 포트(Trunk Port)**: 스위치 간 또는 스위치-라우터 간 연결 시 복수 개의 VLAN 트래픽을 단일 링크로 동시에 전달하는 포트.
- **IEEE 802.1Q(Institute of Electrical and Electronics Engineers 802.1Q)**: 이더넷 프레임 헤더에 4바이트 VLAN Tag(VLAN ID 1~4094, Priority)를 추가 삽입하는 표준 트렁킹 프로토콜.
- **매체 접근 제어 주소(Media Access Control Address, MAC 주소)**: L2 스위치에서 각 VLAN ID별로 독립적인 CAM 테이블(Per-VLAN MAC Table)을 유지하여 수신 노드를 식별하는 물리 주소.

</details>

- 스위치 내부에서 **포트 VLAN 식별자(Port VLAN Identifier, PVID)** 및 **IEEE 802.1Q** 헤더 태깅 기반으로 브로드캐스트와 **MAC 주소** 학습 범위를 완벽히 격리.
- 일반 단말 연결용 **액세스 포트(Access Port)**와 스위치 간 연결용 **트렁크 포트(Trunk Port)**로 역할을 분리하여 스위칭 효율화.
- 서로 다른 VLAN 간 통신은 L3 라우터 또는 L3 스위치의 Inter-VLAN Routing(SVI)을 거치도록 강제하여 보안 정책 수립 지원.

#### 한줄 요약

- Access Port(Untagged) 및 Trunk Port(802.1Q Tagged) 기반 L2 네트워크 구별 체계 구축.


## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **허용 VLAN 목록(Allowed VLAN List)**: Trunk Port 통과 시 물리적 보안을 위해 인가된 VLAN ID 트래픽만 전송을 허용하도록 제한하는 필터링 명세.
- **네이티브 VLAN(Native VLAN)**: 802.1Q Trunk Port에서 태그(Tag)가 붙지 않은 일반 Untagged 프레임이 유입되었을 때 기본 귀속되는 VLAN (기본값: VLAN 1).
- **스위치 가상 인터페이스(Switched Virtual Interface, SVI)**: L3 스위치 내부에서 특정 VLAN 전용 게이트웨이 역할을 수행하도록 생성된 논리적 계층 3 가상 인터페이스.
- **인터넷 프로토콜(Internet Protocol, IP)**: SVI 인터페이스에 할당되어 Inter-VLAN 라우팅을 수행하는 L3 주소.

</details>

```text
[ Access Port (PVID 10) ] ---> (Switch A) === [ Trunk Port (802.1Q Tagged) ] ===> (Switch B)
 (PC: Untagged Frame)          Tagging VLAN 10   (Allowed List: 10, 20)           Untagged Port 10
                                                      |
                                                      v
                                        [ SVI (L3 Gateway: 192.168.10.1) ]
                                        (Inter-VLAN Routing to VLAN 20)
```

*Access Port(PVID), 802.1Q Trunk Port 및 SVI L3 게이트웨이 간의 상호 작용 구조.*

| 구성요소 | 역할 및 세부 기능 | 비고 |
|:---|:---|:---|
| **Access Port & PVID** | 일반 호스트 접속용 포트, 유입 프레임에 **PVID** 바인딩 (수신/송신 시 Untagged) | 1개 VLAN 수용 |
| **Trunk Port** | 스위치 간 멀티 VLAN 연동, 프레임 헤더에 4B **IEEE 802.1Q Tag** 부착 후 전송 | 다수 VLAN 수용 |
| **Native VLAN** | Trunk Port에서 802.1Q Tag 없이 전송되는 예외적인 기본 VLAN (양 스위치 일치 필수) | 기본 VLAN 1 |
| **Allowed VLAN List** | Trunk에서 승인할 VLAN ID 목록 명시 | 보안 강화 기능 |
| **SVI (L3 Interface)** | VLAN 간 통신(Inter-VLAN Routing)을 위해 L3 스위치에 부여하는 3계층 IP 게이트웨이 | L3 스위칭 중계 |

#### 한줄 요약

- Allowed VLAN List, Native VLAN 및 L3 Inter-VLAN Routing용 SVI 구성 체계 준수.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **VLAN 태그 부착(Tag Insertion)**: Access Port로 들어온 Untagged 프레임이 Trunk Port로 나갈 때 802.1Q Tag(4바이트)를 헤더에 삽입하는 동작.
- **VLAN 태그 제거(Tag Removal)**: Trunk Port를 타고 들어온 Tagged 프레임이 목적지 Access Port로 나갈 때 802.1Q Tag를 탈거하여 순수 이더넷 프레임으로 복원하는 동작.
- **PVID 귀속(PVID Classification)**: Access Port로 유입된 프레임을 해당 포트의 PVID 값으로 분류하는 과정.
- **허용 VLAN 전달(Allowed VLAN Forwarding)**: Trunk Port 송출 시 프레임의 VLAN ID가 Allowed List에 등록되어 있는지 검증하는 과정.

</details>

```text
[ 송신 호스트 (Untagged Frame) ]
               |
               v
[ 1. Ingress Access Port (PVID 귀속) ] -------> 포트에 설정된 PVID(예: VLAN 10) 부여
               |
               v
[ 2. Trunk Port 송출 (VLAN 태그 부착) ] ------> 802.1Q 4Byte Tag(VLAN ID 10) 삽입
               |
               v
[ 3. Trunk 통과 (허용 VLAN 전달 검증) ] ------> Trunk Allowed List 상의 VLAN 10 등록 여부 검증
               | (Allowed List 일치)
               v
[ 4. Egress Access Port (VLAN 태그 제거) ] ----> 802.1Q Tag 탈거 후 수신 호스트로 Untagged 전송
```

### 동작 원리

1. **Ingress Access Port (PVID 귀속)**: 포트 VLAN으로 분류
2. **Trunk Port 송출 (VLAN 태그 부착)**: 802.1Q 태그 삽입
3. **Trunk 통과 (허용 VLAN 전달 검증)**: 허용 목록 대조
4. **Egress Access Port (VLAN 태그 제거)**: 태그 제거 후 전달

#### 한줄 요약

- Ingress PVID 분류, 802.1Q Tag Insertion, Allowed List 검증 및 Egress Tag Stripping 프로세스 구동.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **액세스 포트(Access Port)**: 단일 VLAN에만 속하여 802.1Q 태깅 없이 순수 이더넷 프레임만 단말과 주고받는 포트 모드.
- **트렁크 포트(Trunk Port)**: 복수의 VLAN 트래픽을 식별하기 위해 802.1Q 헤더를 부착하여 다중 VLAN 트래픽을 상호 중계하는 포트 모드.

</details>

| 비교 항목 | **액세스 포트 (Access Port)** | **트렁크 포트 (Trunk Port)** |
|:---|:---|:---|
| 수용 VLAN 개수 | 단 1개의 VLAN만 수용 가능 | 복수 개(1~4094)의 VLAN 동시 수용 |
| 프레임 헤더 형태 | 일반 Untagged 이더넷 프레임 송수신 | 4바이트 **IEEE 802.1Q** Tagged 프레임 송수신 (Native 제외) |
| 주 연결 대상 장비 | 엔드포인트 단말 (PC, IP Phone, Server, Printer) | 네트워크 장비 간 (Switch-to-Switch, Switch-to-Router/Firewall) |
| 주요 보안 설정 | Port Security, Dynamic ARP Inspection(DAI) | **Allowed VLAN List** 명시, **Native VLAN** 변경 및 Tagging |

> 요약: 단말 접속용 Access Port와 장비 간 다중 VLAN 통신용 Trunk Port의 기능 및 헤더 처리 방식 차이.

#### 한줄 요약

- 단일 VLAN 수용 Access Port와 Multi-VLAN 수용 Trunk Port의 역할 분담 체계 수립.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **네이티브 VLAN 불일치(Native VLAN Mismatch)**: Trunk Link로 연결된 두 스위치 간 Native VLAN 설정이 달라(예: Switch A=VLAN 1, Switch B=VLAN 99) 무태그 패킷이 엉뚱한 VLAN으로 오유입되는 보안/통신 장애.
- **접근 제어 목록(Access Control List, ACL)**: L3/L4 IP 및 Port 조건에 따라 패킷 허용(Permit) 및 차단(Deny)을 수행하는 정책 리스트.
- **SVI 접근 제어 목록(SVI ACL / VACL)**: SVI 게이트웨이에 ACL을 결합하여 VLAN 간(Inter-VLAN) 무단 라우팅을 차단하는 보안 기법.

</details>

| 장애/위험 요소 | 원인 분석 | 실무 대책 및 해결방안 | 기대 효과 |
|:---|:---|:---|:---|
| **Native VLAN Mismatch** | 트렁크 양단 Native VLAN 미일치로 CDP/STP 경고 발생 | 양단 Native VLAN ID 동일화 또는 Native VLAN Tagging 적용 | VLAN 트래픽 혼입 및 L2 루프 예방 |
| VLAN Hopping 보안 공격 | 트렁크 포트 모드 Auto 설정 시 위조 802.1Q 프레임 유입 | 사용하지 않는 포트 Shutdown 및 Trunk 모드 정적(Desirable) 고정 | 비인가 VLAN 침입 원천 차단 |
| 불필요한 Broadcast 전파 | Trunk Port에 `switchport trunk allowed vlan all` 설정 | **허용 VLAN 목록(Allowed List)**에 필요한 VLAN만 최소 정의 | 불필요한 L2 트래픽 전파 방지 |
| Inter-VLAN 무단 접근 | SVI 생성 후 VLAN 간 라우팅이 기본적으로 승인됨 | **SVI ACL**을 적용하여 업무별/부서별 L3 통신 필터링 | VLAN 간 논리적 장벽 완벽 유지 |

#### 한줄 요약

- Native VLAN Mismatch 예방, Trunk Allowed List 최소화 및 SVI ACL 기반 라우팅 통제 체계 수립.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **최소 VLAN 허용 원칙(Least VLAN Allowance Principle)**: 보안 및 성능 최적화를 위해 Trunk 포트에는 실제로 통신이 필요한 최소한의 VLAN만 Allowed List에 등록하여 운영하는 정책.

</details>

- 트렁크는 **최소 VLAN만 허용**, VLAN 간 통신은 **SVI ACL** 적용

#### 한줄 요약

- IEEE 802.1Q 기반 Trunking 및 최소 VLAN 수용 원칙을 통한 L2/L3 네트워크 보안 체계 적용.
