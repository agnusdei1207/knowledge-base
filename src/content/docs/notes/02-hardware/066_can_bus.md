---
sidebar:
  order: 66
  label: "066. CAN 통신 (Controller Area Network)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "CAN 통신 (Controller Area Network)"
date: "2026-08-13T12:00:06+09:00"
tags:
  - "notes-hardware"
weight: 66
extra:
  question_no: "066"
  source_status: "기출"
  source_history: "129회"
  priority: 50
  priority_note: "CAN 중재•오류 격리의 단일 기출 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **CAN(Controller Area Network)**: 차량 및 산업용 분산 제어 환경에서 중앙 호스트 없이 복수의 ECU가 2선 꼬임선(CAN-H, CAN-L) 버스 상에서 통신하는 표준 네트워크 프로토콜.
- **다중 마스터(Multi-Master)**: 버스의 모든 노드가 유휴 상태에서 메시지 전송을 시도할 수 있는 자율 구조.
- **비파괴 중재(Non-Destructive Arbitration)**: 복수 노드가 동시 송신 시, 메시지 ID의 bit-wise 논리 비교를 통해 높은 우선순위 메시지의 훼손 없이 버스 주도권을 할당하는 메커니즘.

- **캔 버스(Controller Area Network, CAN)**: 차량 내 전자제어장치(ECU) 간에 호스트 컴퓨터 없이 차동 전압 2선(CAN_H, CAN_L) 기반으로 충돌 방지(CSMA/CD+AMP) 통신을 수행하는 차량용 네트워크 버스.
</details>

- 정의/개념: 차동 신호선(CAN-H/CAN-L) 상에서 메시지 식별자(ID) 비트 단위 논리 비교를 통해 **비파괴 중재**를 수행하는 **다중 마스터** 버스 프로토콜인 **CAN**
- 배경/필요성: 차량 내 전자제어장치(ECU) 급증에 따른 1:1 점대점(Point-to-Point) 와이어링 하네스 중량 감소 및 통신 신뢰성 확보 필요성

#### 한줄 요약

- CAN은 메시지 ID 기반 **비파괴 중재**를 사용하는 다중 마스터 방송 버스이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **메시지 ID(Message Identifier)**: 프레임의 우선순위를 결정함과 동시에 수신 노드에서 필요 여부를 필터링하는 11비트(표준)/29비트(확장) 식별자.
- **발행·구독(Publish-Subscribe)**: 송신 노드가 특정 노드 주소를 지정하지 않고 브로드캐스트하면, 필요한 노드들이 메시지 ID를 수신 필터링하는 방식.
- **우성/열성 비트(Dominant/Recessive Bit)**: 버스 물리 레벨에서 논리 0(Dominant, 우성)이 논리 1(Recessive, 열성)을 덮어씌우는 전기적 비트 신호 규격.
- **WCRT(Worst-Case Response Time)**: 버스 최고 혼잡 시 특정 CAN 프레임이 송신 요청부터 최종 수신 완료까지 걸리는 최대 지연시간.

</details>

- 노드 주소가 아닌 메시지 의미 기반의 **발행**•**구독** 방송 통신 방식
- **우성 비트(Dominant, 0)** 충돌 시 수치가 낮은 ID가 전송 주도권을 차지하는 **비파괴 중재**
- 하드웨어 오류 카운터(TEC/REC) 기반의 결함 노드 자동 **버스 오프** 및 물리선 노이즈 차단

#### 한줄 요약

- CAN의 **WCRT**는 ID 우선순위와 버스 부하에 따라 결정되며, 오류 카운터는 고장 노드를 격리한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **CAN 컨트롤러(CAN Controller)**: 프레임 패킹, 비트 스터핑, CRC 계산, 중재 및 오류 처리를 관장하는 논리 레이어 칩셋.
- **CAN 트랜시버(CAN Transceiver)**: 컨트롤러의 TTL/CMOS 논리 신호를 버스 차동 전압(CAN-H, CAN-L) 물리 신호로 상호 변환하는 드라이버.
- **차동 버스·종단(Differential Bus & Termination)**: 노이즈 상쇄용 꼬임선 및 신호 반사파 억제를 위해 버스 양단에 결합하는 120Ω 종단 저항.

</details>

```text
[응용 소프트웨어] -- [CAN 컨트롤러] -- [CAN 트랜시버] -- [차동 버스•종단]
```

선의 의미: 애플리케이션 제어 프레임이 CAN 컨트롤러와 트랜시버를 거쳐 120Ω 종단 저항이 장착된 차동 버스로 연동되는 노드 구조.

| 구성요소 | 책임 |
|:---|:---|
| 응용 소프트웨어 | 센서 제어량 도출, **메시지 ID** 할당 및 프레임 갱신 주기 관리 |
| CAN 컨트롤러 | 프레임 빌드, 비트 스터핑(Bit Stuffing), **CRC** 인코딩 및 중재 관장 |
| CAN 트랜시버 | 논리 TXD/RXD 신호와 물리 차동 전압(CAN-H/CAN-L) 간 직렬 변환 |
| 차동 버스•종단 | 꼬임선 차동 전달 및 120Ω 종단 저항 기반 신호 반사파 상쇄 |

#### 한줄 요약

- CAN 노드는 프레임 제어와 차동 신호 변환을 거쳐 공유 버스와 통신한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **경쟁 ID 비트열(Contending ID Bits)**: 버스 유휴 시 동시 송신을 시도하는 ECU들이 보낸 메시지 ID 비트 파형.
- **CRC(Cyclic Redundancy Check)**: 프레임 전송 무결성 검증을 위한 15비트 순환 중복 검사 필드.
- **ACK(Acknowledgement)**: 프레임을 정상 수신한 노드가 ACK 슬롯에 우성 비트를 인가하는 확인 신호.

</details>

```text
┌────────────── 보류 프레임 반복 ──────────────┐
│ 송신 ECU 집합          CAN 버스          수신 ECU 집합
│      │                    │                   │
│      ├─ 1. ID 비트 중재 ─►│                   │
│      │◄─ 2. 중재 승패 ────┤                   │
│      │                    │                   │
│      ├─ 3. 승자 프레임 ──►│──────────────────►│
│      │                    │                   │
│      │                    │   4. 프레임 검증  │
│      │                    │                   │
│      │                    │◄─ 5. ACK•오류 플래그
│      │◄──── 완료 또는 재전송 상태 ───────────┤
│      │                                        │
│      └── 패자는 버스 유휴 후 재중재 ─────────┘
└───────────────────────────────────────────────┘
```

### 동작 원리

1. ID 비트 중재: 버스 유휴 상태 감지 시, 동시 송신 ECU들이 메시지 **ID 비트열**을 1비트씩 인가.
2. 중재 승패: 자신이 송신한 열성 비트(1)가 버스 상에서 우성 비트(0)로 읽힌 노드는 즉시 중재 포기 및 수신 모드 전환.
3. 승자 프레임: 중재에서 최종 승리한 최우선순위 메시지가 버스 상에 무파괴(Non-destructive) 연속 전송.
4. 프레임 검증: 버스 수신 노드들의 비트 스터핑 검사 및 **CRC** 데이터 무결성 검증.
5. ACK·오류 플래그: 정상 수신 노드가 ACK 슬롯에 우성(0) 출력, 에러 감지 시 **Error Flag** 인가 및 재전송 트리거.

#### 한줄 요약

- **비파괴 중재**의 패자는 버스가 비면 다시 경쟁하고, 오류 프레임은 검출 후 재전송된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **CAN FD(CAN Flexible Data-Rate)**: 데이터 구간의 비트율을 높이고 페이로드를 최대 64바이트로 확장한 CAN 규격.
- **Automotive Ethernet**: 100BASE-T1/1000BASE-T1 스위치 기반 고속(100Mbps~10Gbps) 차량용 백본 인프라.

</details>

| 차량 통신 방식 | Classical CAN | CAN FD | Automotive Ethernet |
|:---|:---|:---|:---|
| 적용 기준 | 섀시, 바디, 센서 등의 소형 제어 메시지 전송 시 | Powertrain, ADAS 센서 등 대용량 제어 및 펌웨어 갱신 시 | 카메라, LiDAR, 중앙 Compute 백본 등 대용량 텐서 전송 시 |
| 핵심 특징 | **CAN** 고정 비트율, 8바이트 페이로드 | **CAN FD** 가변 데이터 비트율, 64바이트 확장 | **Automotive Ethernet** 스위칭 기반 고속 통신 |
| 한계 | 저속 대역폭 및 대용량 데이터 전송 한계 | 기존 Classical CAN 노드와의 물리 혼용 제약 | 시스템 구성 비용 상승 및 보안 위협 방어 필요 |

#### 한줄 요약

- 요구하는 **페이로드**•**대역폭**에 따라 CAN, CAN FD, 자동차 이더넷을 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **버스 부하(Bus Load)**: 단위 시간 중 CAN 버스가 프레임 전송에 점유되는 실효 비율.
- **버스 오프(Bus-Off)**: 송신 에러 카운터(TEC)가 255를 초과한 노드가 다른 노드의 통신을 보호하기 위해 물리 버스에서 자동 이탈하는 상태.
- **SecOC(Secure Onboard Communication)**: CAN 메시지에 신선도 값(Freshness Value)과 MAC(Message Authentication Code)을 부가하는 AUTOSAR 보안 규격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 높은 **버스 부하**로 낮은 우선순위 ID 지연 증가 | 응답시간 분석 기반 ID 재배정과 부하 상한 설정 | 메시지 **WCRT**의 마감시간 충족 검증 |
| 물리 노이즈 지속 발생으로 인한 노드 **버스 오프** 사태 | 트랜시버 차동 라인 필터링 및 120Ω 종단 임피던스 교정 | 하드웨어 전송 노이즈 및 버스 튕김 차단 |
| CAN 버스 위조/스푸핑 및 재전송(Replay) 보안 공격 | AUTOSAR **SecOC** 규격 적용 및 MAC/Freshness 검증 | 메시지 위변조 및 스푸핑 차단 |

> 사례: **SecOC** 기반 메시지 인증 코드(MAC) 적용을 통한 차량 CAN 통신 보안 체계 구축

#### 한줄 요약

- 긴급 메시지에는 **작은 ID**를 배정하고 WCRT와 버스 부하를 함께 검증해야 한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **차량 통신 선택 기준(Automotive Network Selection Criteria)**: 메시지 실시간성, 대역폭 요구량, 데이터 페이로드 크기 및 TCO에 기반한 네트워크 통제 체계.

</details>

- **차량 통신 선택 기준**에 따라 섀시 제어는 **CAN**, 고속 제어는 **CAN FD**, ADAS 비전 백본은 **Automotive Ethernet** 채택

#### 한줄 요약

- 소형 제어는 CAN, 확장 프레임은 CAN FD, 고대역폭 백본은 자동차 이더넷을 선택한다.
