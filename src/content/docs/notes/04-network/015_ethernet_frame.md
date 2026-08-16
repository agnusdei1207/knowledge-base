---
sidebar:
  order: 15
  label: "015. 이더넷 프레임 구조•IEEE 802.3 (Ethernet Frame)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "이더넷 프레임 구조•IEEE 802.3 (Ethernet Frame)"
date: "2026-08-13T16:31:00+09:00"
tags:
  - "notes-network"
weight: 15
extra:
  question_no: "015"
  source_status: "기출"
  source_history: "128회, 129회"
  priority: 50
  priority_note: "설명형: 129회 IEEE 802.3 Frame 서술"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **이더넷 프레임(Ethernet Frame)**: 데이터링크 계층(L2)에서 송수신 물리 주소(MAC), 상위 데이터(Payload), 에러 검출 트레일러(FCS)를 캡슐화한 기본 전송 데이터 단위(PDU).
- **매체 접근 제어 주소(Media Access Control Address, MAC Address)**: 48비트(6바이트) 크기로 구성되어 동일 L2 네트워크 내 송수신 인터페이스를 고유하게 구분하는 물리적 하드웨어 주소.

</details>

- 정의/개념: MAC•페이로드•FCS를 구조화한 **이더넷 프레임**
- 배경/필요성: 비트스트림만으로는 **경계•수신자•손상 식별 불가**

#### 한줄 요약

- L2 주소와 오류 검출 정보를 프레임으로 캡슐화

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **프리앰블(Preamble)**: 수신측 NIC가 동기화 비트 클록(Clock)을 맞출 수 있도록 송신하는 7바이트의 `10101010` 비트 패턴.
- **프레임 시작 구분자(Start Frame Delimiter, SFD)**: 프리앰블 바로 뒤에 위치하여 이더넷 프레임의 실제 시작점임을 알리는 1바이트의 `10101011` 비트 패턴.
- **프레임 검사 시퀀스(Frame Check Sequence, FCS)**: 프레임 전송 과정 중 비트 변조 에러 발생 여부를 수신측에서 검출하기 위해 프레임 맨 끝에 부착하는 4바이트(32비트) 트레일러 필드.

</details>

- **프리앰블** 및 **프레임 시작 구분자** 필드를 통한 물리적 수신 동기화 및 프레임 시작점 명확화.
- 목적지/출발지 6바이트 MAC 주소를 통해 L2 도메인 내 정확한 포트 스위칭 수행.
- **프레임 검사 시퀀스** 기반 오류 검출 시 손상된 프레임을 즉시 폐기(Drop)하고 재전송 책임은 L4 상위 계층으로 이관.

#### 한줄 요약

- Preamble/SFD 동기화, MAC 주소 식별 및 CRC-32 FCS 비트 에러 검출 체계 구축.


## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **이더타입(EtherType)**: Ethernet II 프레임에서 페이로드에 포함된 상위 3계층 프로토콜(예: 0x0800=IPv4, 0x0806=ARP, 0x86DD=IPv6)을 식별하는 2바이트 필드 (값 >= 0x0600).
- **논리 링크 제어(Logical Link Control, LLC)**: IEEE 802.3 프레임에서 상위 프로토콜을 다중화(DSAP/SSAP)하고 흐름 제어를 수행하는 L2 상위 부계층.
- **순환 중복 검사(Cyclic Redundancy Check, CRC)**: 다항식 연산을 기반으로 데이터 전송 중 에러를 탐지하는 무결성 검증 수학적 다항식 알고리즘.
- **32비트 순환 중복 검사(Cyclic Redundancy Check-32, CRC-32)**: 이더넷 프레임 트레일러(FCS)에 탑재되는 32비트 표준 오류 검출 알고리즘.
- **전기전자공학자협회 802.3(Institute of Electrical and Electronics Engineers 802.3, IEEE 802.3)**: CSMA/CD 및 이더넷 물리/데이터링크 계층을 규정하는 IEEE 국제 표준 규격.

</details>

```text
+---------------------------------------------------------------------------------------------------+
| Preamble | SFD | Dest MAC | Src MAC  | EtherType / Length |    Data Payload    | Pad  |    FCS    |
| (7 Bytes)|(1 B)| (6 Bytes)| (6 Bytes)|     (2 Bytes)      | (46 ~ 1500 Bytes)  | (v)  | (4 Bytes) |
+---------------------------------------------------------------------------------------------------+
 * Ethernet II  : 2 Bytes 필드가 >= 0x0600 (예: 0x0800 -> IPv4, 0x0806 -> ARP)
 * IEEE 802.3   : 2 Bytes 필드가 <= 0x05DC (Payload Length) + LLC/SNAP Header (8 Bytes)
```

*Ethernet II 및 IEEE 802.3 표준 프레임 레이아웃.*

| 구성요소 | 바이트 크기 | 주요 역할 및 기능 |
|:---|:---|:---|
| **Preamble + SFD** | 7 + 1 Bytes | 수신 비트 클록 동기화 (Preamble) 및 본 프레임 시작 알림 (SFD) |
| **Destination MAC** | 6 Bytes (48-bit) | 수신 호스트/인터페이스 물리 주소 (Unicast, Multicast, Broadcast) |
| **Source MAC** | 6 Bytes (48-bit) | 송신 호스트/인터페이스 물리 주소 (스위치 CAM 테이블 학습의 기준) |
| **EtherType / Length** | 2 Bytes | 0x0600 이상: **EtherType** (상위 L3 프로토콜) / 0x05DC 이하: **IEEE 802.3** 데이터 길이 |
| **Payload + Pad** | 46 ~ 1500 Bytes | L3 IP 패킷 데이터 (최소 46바이트 미달 시 Pad 비트로 채움) |
| **FCS (Trailer)** | 4 Bytes (32-bit) | Destination MAC부터 Pad까지 연산한 **CRC-32** 오류 검출값 |

#### 한줄 요약

- Ethernet II (EtherType 0x0800/0x0806) 및 IEEE 802.3 LLC/SNAP 프레임 레이아웃 준수.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **네트워크 인터페이스 카드(Network Interface Card, NIC)**: 이더넷 프레임을 물리 신호로 직렬화하여 송수신하고, MAC 주소 및 CRC 오류 검증을 담당하는 하드웨어 장치.
- **프레임 전송(Frame Transmission)**: L3 패킷을 수신하여 L2 헤더/트레일러(FCS)를 캡슐화하고 매체로 송출하는 과정.
- **MAC 주소 조회(Destination MAC Lookup)**: 수신 스위치에서 프레임의 목적지 MAC 주소를 CAM 테이블과 대조하여 포워딩 출력을 결정하는 과정.
- **출력 포트 중계(Output Port Forwarding)**: CAM 테이블에 매핑된 물리 스위치 포트로 프레임을 1:1 전달하는 과정.
- **FCS 오류 검증(FCS Error Validation)**: 수신 NIC에서 CRC-32 다항식을 재연산하여 FCS 필드와 대조, 비트 에러 발생 시 수신 패킷을 디스카드(Discard)하는 과정.

</details>

```text
[ 송신 상위 L3 패킷 ]
          |
          v
[ 1. 프레임 캡슐화 및 전송 (NIC) ] -----> L2 Header(MAC, Type) + Payload + FCS(CRC-32) 직렬화 송출
          |
          v
[ 2. 스위치 목적지 MAC 조회 ] ---------> CAM Table 룩업 (Destination MAC Match)
          |
          v
[ 3. 출력 포트 중계 (Forwarding) ] ----> 해당 포트로 프레임 스위칭 전송
          |
          v
[ 4. 수신 NIC FCS 오류 검증 ] ---------> CRC-32 연산 대조
          |
          +-----------------------------------+
          | (Match / Normal)                  | (Mismatch / Bit Error)
          v                                   v
[ 5. 상위 L3 프로토콜 전달 ]                 [ 프레임 즉시 폐기 (Drop) ]
```

### 동작 원리

1. **프레임 캡슐화 및 전송**: MAC•Type•FCS 부착
2. **스위치 목적지 MAC 조회**: CAM 테이블 검색
3. **출력 포트 중계**: 매핑 포트로 프레임 전달
4. **수신 NIC FCS 오류 검증**: CRC-32 대조
5. **상위 L3 프로토콜 전달**: 정상 페이로드 역캡슐화

#### 한줄 요약

- 프레임 동기화•MAC 조회•CRC-32 검증

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **이더넷 II(Ethernet II / DIX Ethernet)**: 디지털, 인텔, 제록스(DIX)가 규정한 프레임으로 Type 필드를 통해 L3 프로토콜을 직접 식별하여 상용 인터넷에서 표준으로 사용되는 방식.
- **IEEE 802.3 LLC(Institute of Electrical and Electronics Engineers 802.3 LLC)**: 2바이트 필드를 Length로 사용하고 뒤에 802.2 LLC 및 SNAP 헤더를 추가하여 프로토콜을 식별하는 산업 표준 방식.

</details>

| 비교 항목 | **이더넷 II (Ethernet II)** | **IEEE 802.3 LLC / SNAP** |
|:---|:---|:---|
| 헤더 오버헤드 | 14 바이트 (MAC 12B + Type 2B) | 22 바이트 (MAC 12B + Length 2B + LLC 3B + SNAP 5B) |
| 프로토콜 식별 방식 | 2바이트 **EtherType** 사용 (예: 0x0800 = IPv4) | 8바이트 LLC/SNAP 헤더 내부의 Protocol ID 사용 |
| 주 활용 분야 | TCP/IP 기반 상용 전 인터넷 네트워크 트래픽 | STP(802.1D), CDP, BPDU 등 L2 제어 프로토콜 |
| 최소/최대 페이로드 | 46 ~ 1500 바이트 | 38 ~ 1492 바이트 (LLC 오버헤드로 페이로드 축소) |

> 요약: 인터넷 환경의 99% 이상에서 활용되는 효율적인 Ethernet II 프레임 규격과 L2 제어용 IEEE 802.3 LLC 규격의 상호 보완.

#### 한줄 요약

- EtherType 기반 Ethernet II 규격과 Length/LLC 기반 IEEE 802.3 규격의 정합적 활용 체계 수립.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **최대 전송 단위(Maximum Transmission Unit, MTU)**: 프레임 페이로드로 실을 수 있는 최대 L3 IP 패킷 바이트 규격 (표준 이더넷: 1500바이트).
- **점보 프레임(Jumbo Frame)**: 표준 MTU(1500바이트)보다 큰 최대 9000바이트의 페이로드를 수용하여 프레임 오버헤드와 CPU 인터럽트를 효과적으로 줄이는 기술.
- **가상 근거리 통신망 태그(Virtual Local Area Network Tag, VLAN Tag / 802.1Q Tag)**: 스위치 트렁크 포트 통신 시 L2 헤더의 Source MAC과 EtherType 사이에 추가 삽입되는 4바이트 VLAN 식별자 (TPID=0x8100 + TCI=VLAN ID/Priority).
- **IEEE 802.1Q**: 이더넷 프레임에 4바이트 VLAN 태그를 추가하여 논리적 네트워크를 격리하는 이더넷 트렁킹 국제 표준.

</details>

| 장애/위험 요소 | 원인 분석 | 실무 대책 및 해결방안 | 기대 효과 |
|:---|:---|:---|:---|
| **VLAN 태그** 프레임 드롭 | 802.1Q 태그 삽입으로 프레임 크기가 1522바이트로 증가 | 스위치 포트 Baby Giant / **IEEE 802.1Q** 허용 설정 | VLAN 트렁크 프레임 드롭 방지 |
| 고속 데이터센터 전송 병목 | 1500바이트 표준 MTU 사용 시 대량의 프레임 오버헤드 발생 | 스위치 및 서버 NIC **점보 프레임(9000바이트)** 활성화 | CPU 인터럽트 감소 및 전송 풋프린트 향상 |
| L1/L2 물리 신호 에러 (FCS Error) | UTP 케이블 꺾임, 불량 광모듈 또는 노이즈 간섭 | 스위치 포트 `show interface` CRC Error 카운터 점검 및 케이블 교체 | 프레임 패킷 드롭 예방 |

#### 한줄 요약

- 802.1Q VLAN Tagging (4바이트 추가), Jumbo Frame (9000바이트) 튜닝 및 PMTU 정합성 확보 체계 수립.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **경로 MTU 일치(Path MTU Alignment)**: 송수신 호스트부터 중간 L2/L3 스위치, 라우터 전 구간의 MTU 및 점보 프레임 설정을 동일하게 맞추는 최적화 가이드라인.

</details>

- VLAN 태그 구간은 **경로 MTU**를 맞추고 CRC 오류 감시

#### 한줄 요약

- 태그 오버헤드와 경로 MTU 기준으로 프레임 크기 결정
