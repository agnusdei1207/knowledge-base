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

- **매체 접근 제어 주소(Media Access Control Address, MAC Address)**: 동일 데이터 링크 내에서 이더넷 프레임의 송수신 인터페이스를 식별하는 48비트 물리 주소.
- **인터넷 프로토콜(Internet Protocol, IP)**: 네트워크 계층에서 수신처 호스트의 논리적 위치를 지정하여 라우팅을 수행하는 프로토콜.

</details>

- 정의/개념: 동일 L2 데이터 링크 상의 인터페이스를 식별하는 **매체 접근 제어 주소(Media Access Control Address, MAC Address)**.
- 배경/필요성: L3 **인터넷 프로토콜(Internet Protocol, IP)** 주소만으로 인접 데이터 링크 내 물리적 프레임 전송 불가에 따른 L2 전용 식별 체계 필요성 대두.

#### 한줄 요약

- MAC 주소는 같은 건물 안에서 프레임을 정확한 장치 포트로 보내는 호실 번호처럼 쓰인다.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **옥텟(Octet)**: 8개의 비트로 구성된 바이너리 데이터 단위.
- **개별/그룹 비트(Individual/Group Bit, I/G Bit)**: MAC 주소의 첫 번째 옥텟 최하위 비트로, 단일(Unicast) 주소와 그룹(Multicast/Broadcast) 주소를 구분하는 제어 비트.
- **전역/로컬 비트(Universal/Local Bit, U/L Bit)**: MAC 주소의 첫 번째 옥텟 두 번째 비트로, IEEE 전역 할당 주소와 사용자 로컬 임의 주소를 구분하는 제어 비트.

</details>

- 48비트(6개 **옥텟(Octet)**) 표기를 통한 이더넷 MAC 주소 식별.
- **개별/그룹 비트(Individual/Group Bit, I/G Bit)**를 통한 수신 범주의 구별 및 **전역/로컬 비트(Universal/Local Bit, U/L Bit)**를 통한 관리 주체 구별.
- 주소 소프트웨어 변경(Spoofing) 가능성에 따른 신원 증명 대체 불가성.

#### 한줄 요약

- 장치가 주소를 바꿔 다른 장치처럼 보일 수 있으므로 MAC 주소만 보고 사람이나 장치를 믿을 수는 없다.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **조직 고유 식별자(Organizationally Unique Identifier, OUI)**: IEEE에서 제조업체에 할당하는 MAC 주소의 상위 24비트 고유 코드.
- **인터페이스 식별자(Interface Identifier)**: OUI 할당 조직이 자체 제품 및 인터페이스마다 부여하는 하위 24비트 식별 번호.

</details>

```text
MAC 주소 48비트
├── 상위 24비트 OUI
│   └── 첫 옥텟 I/G•U/L 비트
└── 하위 24비트 인터페이스 식별자
```

선의 의미: 상위 24비트 OUI(제조사 코드) 및 하위 24비트 인터페이스 식별 영역의 구성을 통한 고유 물리 주소 형성 표시.

| 구성요소 | 책임 |
|:---|:---|
| 상위 24비트 OUI | **조직 고유 식별자(Organizationally Unique Identifier, OUI)**를 활용한 제조 조직 식별 |
| 하위 24비트 인터페이스 식별자 | **인터페이스 식별자(Interface Identifier)** 기반 제품 개별 인터페이스 구분 |
| 첫 옥텟 I/G•U/L 비트 | **I/G 비트** 기반 유니캐스트/멀티캐스트 구분 및 **U/L 비트** 기반 전역/로컬 주소 구별 |

#### 한줄 요약

- 주소 앞의 두 제어 비트가 성격을 밝히고 나머지 부분이 할당 조직과 인터페이스를 구분한다.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **포워딩 테이블(Forwarding Table)**: 스위치가 포트별로 학습한 출발지 MAC 주소와 포트 매핑 정보를 저장하는 메모리 테이블.
- **플러딩(Flooding)**: 수신된 프레임의 목적지 MAC 주소가 테이블에 없을 때, 수신 포트를 제외한 동일 VLAN의 모든 포트로 프레임을 복제 전송하는 동작.
- **출발지 주소 학습(Source MAC Learning)**: 프레임 수신 시 헤더의 출발지 MAC 주소와 입력 포트를 매핑하여 저장하는 절차.
- **목적지 주소 조회(Destination MAC Lookup)**: 수신 프레임의 목적지 MAC 주소를 포워딩 테이블에서 검색하는 절차.
- **단일 포트 전달(Unicast Forwarding)**: 목적지 MAC 주소가 매핑된 특정 포트로만 프레임을 전달하는 동작.

</details>

```text
이더넷 프레임 수신
        |
        v
1. 출발지 주소 학습
        |
        v
2. 목적지 주소 조회
        |
        +-- 목적지 학습 완료
        |          |
        |          v
        |   3. 단일 포트 전달
        |
        `-- 목적지 미등록
                   |
                   v
             4. 포트 플러딩
```

### 동작 원리

1. **출발지 주소 학습(Source MAC Learning)**: 수신 프레임의 MAC 주소와 입력 포트를 **포워딩 테이블(Forwarding Table)**에 저장.
2. **목적지 주소 조회(Destination MAC Lookup)**: **포워딩 테이블(Forwarding Table)** 내 목적지 포트 검색.
3. **단일 포트 전달(Unicast Forwarding)**: 바인딩된 포트로 프레임 전송.
4. **플러딩(Flooding)**: 미학습 목적지 프레임의 동일 VLAN 내 모든 포트 복제 전송.

#### 한줄 요약

- 스위치는 들어온 주소로 위치표를 배우고 목적지 위치를 알면 그 포트에만, 모르면 여러 포트에 보낸다.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **전역 관리 MAC(Universally Administered Address, UAA)**: 제조 시 장비에 고정적으로 각인(Burned-In)되어 전 세계적으로 유일성이 보장되는 주소.
- **로컬 관리 MAC(Locally Administered Address, LAA)**: 네트워크 관리자나 가상화 소프트웨어에 의해 임의 지정되어 사용되는 주소.

</details>

| MAC 관리 방식 | **전역 관리 MAC** | **로컬 관리 MAC** |
|:---|:---|:---|
| 적용 기준 | 장치의 기본 주소 식별 | 가상 인터페이스•프라이버시 보호 |
| 핵심 특징 | **OUI** 기반 조직•장치 할당 | **U/L 비트**로 로컬 관리 표시 |
| 한계 | 장기 식별자 노출•추적 | 같은 링크의 주소 중복 |

> 요약: 전역 할당 주소(UAA)와 소프트웨어 지정 주소(LAA)의 범위 및 제어 메커니즘 차이.

#### 한줄 요약

- 전역 주소는 할당 기관이 나눠 주고 로컬 주소는 운영자가 만들지만 같은 링크에서 겹치면 전달이 어긋난다.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **MAC 스푸핑(MAC Spoofing)**: 송신 프레임의 출발지 MAC 주소를 정상 타깃의 MAC 주소로 위조하여 보안 통제를 우회하는 공격.
- **IEEE 802.1X(Institute of Electrical and Electronics Engineers 802.1X)**: 포트 기반 네트워크 접근 제어(PNAC)를 통해 접속 노드를 인증하는 보안 규격.
- **가상 근거리 통신망(Virtual Local Area Network, VLAN)**: L2 스위치 상에서 브로드캐스트 도메인을 논리적으로 격리하는 네트워크 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| **MAC 스푸핑(MAC Spoofing)**으로 장치 신원 위조 | **IEEE 802.1X**로 접속 주체 인증 | 주소 위조 접속 차단 |
| 대량 위조 주소로 MAC 테이블 고갈 | 포트별 MAC 학습 수 제한 | **플러딩(Flooding)** 전환 방지 |
| 가상 머신 이동으로 MAC 포트가 변경 | 이동 통지 후 MAC 재학습 | 잘못된 포트 전달 시간 단축 |
| 대형 링크에 브로드캐스트가 확산 | **가상 근거리 통신망(Virtual Local Area Network, VLAN)**으로 링크 영역 분리 | 장애•공격 확산 범위 축소 |

#### 한줄 요약

- 스위치는 출발지 MAC 주소를 학습하고 목적지 MAC 주소에 대응하는 포트로만 프레임을 전달한다.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **포트 보안(Port Security)**: 스위치 포트에 연결될 수 있는 MAC 주소를 고정 또는 제한하여 무단 장치 연결을 차단하는 기술.
- **통제 선택(Security Control Selection)**: 프레임 스위칭을 위한 L2 MAC 처리와 보안 강화를 위한 IEEE 802.1X 인증을 상호 보완적으로 적용하는 판단.

</details>

- **통제 선택(Security Control Selection)**을 통한 L2 전송 중심의 **MAC 주소** 활용과 L2 접근 통제를 위한 **IEEE 802.1X** 인증 및 **포트 보안(Port Security)** 병행 적용.

#### 한줄 요약

- MAC 주소는 바꿀 수 있는 전달표이므로 신원 확인에는 별도 인증이 필요하다.

