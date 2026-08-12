---
sidebar:
  order: 6
  label: "006. MAC 주소 구조 (MAC Address)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "MAC 주소 구조 (MAC Address)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-network"
weight: 6
extra:
  question_no: "006"
  source_status: "기출"
  source_history: "128회"
  priority: 30
  priority_note: "설명형: 128회 주소 구조의 2계층 식별 요소"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **매체 접근 제어 주소(Media Access Control Address, MAC Address)**: 데이터링크 계층(L2)의 이더넷 프레임 통신에서 각 네트워크 인터페이스 카드(NIC)를 고유하게 식별하기 위해 부여된 48비트(6바이트) 물리적 하드웨어 주소.
- **인터넷 프로토콜(Internet Protocol, IP)**: 네트워크 계층(L3)에서 종단 간 패킷 라우팅을 위해 할당되는 32비트(IPv4) 또는 128비트(IPv6) 논리적 주소.

</details>

- 정의/개념: 동일 데이터 링크(Broadcast Domain) 내에서 장치 간 프레임 송수신을 위한 48비트 하드웨어 식별자인 **매체 접근 제어 주소(Media Access Control Address, MAC Address)**.
- 배경/필요성: L3 **인터넷 프로토콜(Internet Protocol, IP)** 주소만으로는 물리적 매체 상의 인접 노드에 프레임을 직접 전송할 수 없으므로, L2 스위칭 및 프레임 전달을 위한 전용 하드웨어 물리 주소 체계 구축이 필수적임.

#### 한줄 요약

- 48비트 L2 물리 주소 체계 표준화 및 인접 노드 간 이더넷 프레임 전달 체계 구현.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **옥텟(Octet)**: 8개의 비트로 구성된 1바이트 크기의 기본 2진 데이터 단위.
- **개별/그룹 비트(Individual/Group Bit, I/G Bit)**: MAC 주소 첫 번째 옥텟의 최하위 비트(LSB)로, 단일 대상 전송(Unicast, 0)과 그룹 대상 전송(Multicast/Broadcast, 1)을 구별하는 제어 비트.
- **전역/로컬 비트(Universal/Local Bit, U/L Bit)**: MAC 주소 첫 번째 옥텟의 하위 두 번째 비트로, IEEE 전역 할당 주소(UAA, 0)와 소프트웨어 로컬 지정 주소(LAA, 1)를 구별하는 제어 비트.

</details>

- 48비트(6개 **옥텟(Octet)**)를 16진수 표기법(예: `00:1A:2B:3C:4D:5E`)으로 구조화.
- **개별/그룹 비트(Individual/Group Bit, I/G Bit)**를 통해 유니캐스트/멀티캐스트 프레임을 수신단에서 즉각 분기 처리.
- **전역/로컬 비트(Universal/Local Bit, U/L Bit)**를 통해 제조사 각인 주소와 소프트웨어(가상화/MAC Randomization) 할당 주소를 구분.
- 소프트웨어적 주소 변조(**MAC Spoofing**)가 가능하므로 순수 MAC 주소만으로 보안 인증을 대체하는 것은 불가능.

#### 한줄 요약

- OUI 제조사 코드, I/G-U/L 제어 비트를 활용한 6옥텟 물리 주소 식별 체계 구축.


## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **조직 고유 식별자(Organizationally Unique Identifier, OUI)**: IEEE가 제조회사(NIC 메이커)에 할당하는 MAC 주소 상위 24비트(3옥텟) 제조사 고유 코드.
- **인터페이스 식별자(Interface Identifier / Serial Number)**: NIC 제조사가 각 개별 제품 카드에 중복 없이 부여하는 하위 24비트(3옥텟) 시리얼 일련번호.

</details>

```text
+-----------------------------------------------------------------------------------+
|                            48비트 (6옥텟) MAC 주소                                |
+---------------------------------------------------+-------------------------------+
|  상위 24비트: OUI (조직 고유 식별자)              |  하위 24비트: NIC 시리얼 번호  |
|  [ 옥텟 1 ]       [ 옥텟 2 ]       [ 옥텟 3 ]     |  [ 옥텟 4 ][ 옥텟 5 ][ 옥텟 6 ]
|  xxxxxx[U/L][I/G]                                 |                               |
+---------------------------------------------------+-------------------------------+
 * I/G 비트: 0 = 유니캐스트, 1 = 멀티캐스트/브로드캐스트
 * U/L 비트: 0 = 전역 관리 (UAA), 1 = 로컬 관리 (LAA)
```

*IEEE 지정 24비트 OUI 영역과 24비트 장비 고유 일련번호 영역의 결합 구조.*

| 구성요소 | 비트 범위 | 역할 및 세부 기능 | 비고 |
|:---|:---|:---|:---|
| **조직 고유 식별자 (OUI)** | 1 ~ 24 비트 (1~3 옥텟) | IEEE 등록 제조회사 식별 (예: Cisco, Intel, Samsung) | 상위 3바이트 |
| **I/G 비트** | 1번째 옥텟 8번째 비트 | 0: 단일 호스트(Unicast) / 1: 그룹 호스트(Multicast/Broadcast) | 프레임 전송 범주 판단 |
| **U/L 비트** | 1번째 옥텟 7번째 비트 | 0: 전역 할당 주소 (UAA) / 1: 로컬 관리 주소 (LAA) | 관리 주체 판별 |
| **인터페이스 식별자** | 25 ~ 48 비트 (4~6 옥텟) | 특정 제조사 내에서 인터페이스 카드마다 유일하게 부여한 시리얼 | 하위 3바이트 |

#### 한줄 요약

- 상위 24비트 OUI 및 하위 24비트 NIC 식별자의 결합을 통한 전역 유일 주소 구조 준수.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **포워딩 테이블(Forwarding Table / CAM Table)**: L2 스위치가 스위치 포트 번호와 해당 포트에 연결된 장비의 MAC 주소를 매핑하여 보관하는 고속 메모리 테이블.
- **플러딩(Flooding)**: 수신 프레임의 목적지 MAC 주소가 CAM 테이블에 없을 때, 수신 포트를 제외한 동일 VLAN 내 전 포트로 패킷을 복사 전송하는 동작.
- **출발지 주소 학습(Source MAC Learning)**: 스위치 포트로 프레임이 유입될 때 해당 프레임의 출발지 MAC 주소를 CAM 테이블에 기록하는 프로세스.
- **목적지 주소 조회(Destination MAC Lookup)**: 수신 프레임의 목적지 MAC 주소를 CAM 테이블에서 조회하여 스위칭 경로를 확정하는 프로세스.
- **단일 포트 전달(Unicast Forwarding)**: CAM 테이블에 매핑된 특정 포트로만 프레임을 정확히 1:1 포워딩하는 동작.

</details>

```text
[ 이더넷 프레임 유입 ]
          |
          v
[ 1. 출발지 주소 학습 (출발지 MAC 학습) ] -------> [CAM 테이블] 포트-MAC 매핑 업데이트
          |
          v
[ 2. 목적지 주소 조회 (목적지 MAC 조회) ] -------> CAM 테이블 검색
          |
          +-----------------------------------+
          | (적중)                            | (미적중 / 브로드캐스트)
          v                                   v
[ 3. 단일 포트 전달 (유니캐스트 전달) ]       [ 4. 플러딩 (플러딩) ]
 (해당 매핑 포트로 1:1 전송)                 (수신 포트 제외 VLAN 전체 전송)
```

### 동작 원리

1. **MAC 주소 학습 단계 (Source MAC Learning)**: 스위치는 유입 프레임의 출발지 MAC 주소를 확인하여 유입된 물리 포트 번호와 함께 **포워딩 테이블(CAM Table)**에 등록.
2. **프레임 포워딩 및 플러딩 단계 (Lookup & Forwarding)**: 목적지 MAC 주소를 **포워딩 테이블**에서 조회(**Destination MAC Lookup**)하여 매핑된 포트로 **단일 포트 전달(Unicast Forwarding)**을 수행하고, 미학습 MAC 주소인 경우 동일 VLAN 전체 포트로 **플러딩(Flooding)** 진행.

#### 한줄 요약

- 스위치 MAC 학습, CAM 테이블 룩업 및 미학습 프레임 플러딩 제어 프로세스 구동.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **전역 관리 MAC(Universally Administered Address, UAA)**: NIC 제조 시 하드웨어 롬(ROM)에 물리적으로 각인(Burned-In)되어 전 세계 고유성을 보장받는 주소.
- **로컬 관리 MAC(Locally Administered Address, LAA)**: 가상화 Hypervisor(ESXi, KVM)나 네트워크 관리자가 임의로 소프트웨어 변경하여 사용하는 주소.

</details>

| 비교 항목 | **전역 관리 MAC (UAA)** | **로컬 관리 MAC (LAA)** |
|:---|:---|:---|
| 주소 생성 주체 | 하드웨어 제조사 (IEEE OUI 규격 준수) | 가상화 솔루션, OS 관리자, 무선 프라이버시 기능 |
| U/L 비트 값 | 0 (Universal) | 1 (Local) |
| 활용 분야 | 물리 NIC 카드, 이더넷 스위치/라우터 포트 | VM(가상머신), Docker 컨테이너, Wi-Fi MAC Randomization |
| 장단점 | 세계적 고유성 보장 / 이동 추적 및 프라이버시 노출 | 주소 유연성 확보 / 동일 L2 구간 내 주소 중복 위험 존재 |

> 요약: 하드웨어 고정 식별용 UAA 주소와 가상화/보안 임시 할당용 LAA 주소의 구별 및 U/L 비트에 의한 투명 제어.

#### 한줄 요약

- 물리 각인 전역 주소(UAA) 및 동적 소프트웨어 주소(LAA)의 역할 분담 체계 수립.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **MAC 스푸핑(MAC Spoofing)**: 송신 프레임의 출발지 MAC 주소를 인가된 타깃 장비의 MAC 주소로 변조하여 스위치 CAM 테이블을 교란하고 트래픽을 도청하는 위협.
- **IEEE 802.1X(Institute of Electrical and Electronics Engineers 802.1X)**: L2 포트 단에서 EAPOL 프로토콜을 통해 사용자/장비의 인증을 수행하는 포트 기반 접근 통제 규격.
- **가상 근거리 통신망(Virtual Local Area Network, VLAN)**: 스위치 내 물리 포트들을 논리적 브로드캐스트 도메인으로 격리하여 L2 트래픽 전파를 통제하는 기술.

</details>

| 장애/위협 요소 | 원인 분석 | 실무 대책 및 해결방안 | 기대 효과 |
|:---|:---|:---|:---|
| **MAC 스푸핑** 공격 | L2 프레임의 출발지 주소 변조 용이성 | L2 스위치 **포트 보안(Port Security)** 및 Dynamic ARP Inspection(DAI) 적용 | 위조 MAC 프레임 차단 및 포트 셧다운 |
| CAM Table Overflow 공격 | 공격자가 랜덤 MAC 프레임을 대량 발송하여 테이블 고갈 | 스위치 포트별 학습 가능 최대 MAC 개수 제한 (Sticky MAC) | 스위치의 Dummy Hub화(플러딩) 예방 |
| 비인가 장비 무단 접속 | MAC 주소 필터링만 적용 시 스푸핑 우회 가능 | **IEEE 802.1X** RADIUS 연동 기반 포트 사용자 인증 체계 구축 | 무단 NIC 디바이스 접근 원천 차단 |

#### 한줄 요약

- MAC 스푸핑 방지용 Port Security, 802.1X 인증 및 VLAN 격리를 통한 L2 보안 체계 수립.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **포트 보안(Port Security)**: 스위치 포트에 연결 가능한 MAC 주소를 정적으로 바인딩하거나 개수를 제한하여 L2 침입을 방어하는 보안 기술.
- **통제 선택(Security Control Selection)**: 위변조가 용이한 MAC 주소의 한계를 인지하고 802.1X, DAI, Port Security를 다층으로 결합하는 보안 전략.

</details>

- L2 데이터링크 통신의 신뢰성과 안정적인 이더넷 프레임 전송을 위해 **포트 보안(Port Security)** 및 **통제 선택(Security Control Selection)**에 기반한 802.1X 포트 인증 모듈 적용 필수.

#### 한줄 요약

- IEEE 802.1X 기반 사용자 인증 및 MAC Port Security 통제 체계 적용.
