---
sidebar:
  order: 1
  label: "001. OSI 7계층 모델 (OSI 7-Layer Model)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "OSI 7계층 모델 (OSI 7-Layer Model)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-network"
weight: 1
extra:
  question_no: "001"
  source_status: "기출"
  source_history: "120회, 125회, 134회"
  priority: 70
  priority_note: "설명형: 120•134회 단답•서술, 계층 기능•PDU"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **개방형 시스템 간 상호접속 7계층 모델(Open Systems Interconnection 7-Layer Model, OSI 7계층 모델)**: 통신 기능과 책임을 일곱 계층으로 나누어 이기종 시스템의 상호운용 기준을 제공하는 참조 모델이다.

</details>

- 정의/개념: 통신 기능과 책임을 분리한 **개방형 시스템 간 상호접속 7계층 모델(Open Systems Interconnection 7-Layer Model, OSI 7계층 모델)**이다.
- 배경/필요성: 공통 계층 기준이 없으면 이기종 장비의 상호운용이 제약된다.

#### 한줄 요약

- Heterogeneous System 간의 상호운용성(Interoperability) 보장 및 Layered Architecture 기반의 Fault Isolation(장애 격리)을 제공한다.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **계층 인터페이스**: 인접한 두 계층이 서비스를 요청하고 처리 결과를 전달하는 경계이다.
- **프로토콜 데이터 단위(Protocol Data Unit, PDU)**: 각 계층이 자신의 제어 정보를 붙여 처리하는 데이터 단위이다.
- **캡슐화(Encapsulation)**: 송신 계층이 데이터에 제어 정보를 붙이는 과정이다.
- **역캡슐화(Decapsulation)**: 수신 계층이 제어 정보를 반대 순서로 제거하는 과정이다.

</details>

- **계층 인터페이스**로 구현 변경 영향을 격리한다.
- **프로토콜 데이터 단위(Protocol Data Unit, PDU)**로 처리 책임과 장애 범위를 구분한다.
- **캡슐화(Encapsulation)**와 **역캡슐화(Decapsulation)**로 제어 정보를 대칭 처리한다.

#### 한줄 요약

- Layer Decoupling 및 Defined Service Interface(SAP)를 통해 하위 계층 구현 변경이 상위 계층에 미치는 영향도를 억제한다.


## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **전송 제어 프로토콜(Transmission Control Protocol, TCP)**: 포트로 응용을 구분하고 순서와 재전송을 제어하는 전송 계층 프로토콜이다.
- **인터넷 프로토콜(Internet Protocol, IP)**: 출발지와 목적지 주소를 사용하여 패킷 전달 경로를 정하는 네트워크 계층 프로토콜이다.
- **매체 접근 제어(Media Access Control, MAC)**: 같은 링크의 장치를 식별하고 프레임을 전달하는 데이터링크 계층 기능이다.

</details>

```text
응용 계층
│
표현 계층
│
세션 계층
│
전송 계층
│
네트워크 계층
│
데이터링크 계층
│
물리 계층
```

선의 의미: 각 선은 인접 계층 사이의 서비스 인터페이스이며, 상위 데이터 의미와 종단 전달•경로•프레임•신호 책임을 분리하면서 결합하는 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| 응용 계층 | 사용자 네트워크 서비스 제공 |
| 표현 계층 | 데이터 형식•암호화•압축 변환 |
| 세션 계층 | 통신 대화•동기화 상태 관리 |
| 전송 계층 | **전송 제어 프로토콜(Transmission Control Protocol, TCP)** 등 포트 기반 종단 전달 제어 |
| 네트워크 계층 | **인터넷 프로토콜(Internet Protocol, IP)** 주소 기반 경로 선택 |
| 데이터링크 계층 | **매체 접근 제어(Media Access Control, MAC)** 주소 기반 프레임 전달 |
| 물리 계층 | 비트를 전기•광•무선 신호로 전송 |

#### 한줄 요약

- 위층은 사용자 데이터의 의미를 다루고 아래층으로 갈수록 전달 경로와 실제 신호를 다룬다.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **세그먼트(Segment)**: 전송 계층이 처리하는 데이터 단위이다.
- **패킷(Packet)**: 네트워크 계층이 처리하는 데이터 단위이다.
- **프레임(Frame)**: 데이터링크 계층이 처리하는 데이터 단위이다.
- **비트(Bit)**: 물리 계층이 처리하는 데이터 단위이다.

</details>

```text
송신 응용 데이터
      |
      v
1. 캡슐화
      |
      +-- 응용•표현•세션 ---- 데이터
      +-- 전송 계층 -------- 세그먼트
      +-- 네트워크 계층 ---- 패킷
      +-- 데이터링크 계층 -- 프레임
      `-- 물리 계층 -------- 비트
                                  |
                              전송 매체
                                  |
                                  v
                           2. 역캡슐화
                                  |
                                  +-- 비트
                                  +-- 프레임
                                  +-- 패킷
                                  +-- 세그먼트
                                  `-- 수신 응용 데이터
```

### 동작 원리

1. **캡슐화(Encapsulation)**: 계층별 헤더를 붙여 **프로토콜 데이터 단위(Protocol Data Unit, PDU)**를 생성한다.
2. **역캡슐화(Decapsulation)**: **비트(Bit)**•**프레임(Frame)**•**패킷(Packet)**•**세그먼트(Segment)** 순으로 헤더를 제거해 원본을 복원한다.

#### 한줄 요약

- 송신자는 계층별 주소표를 붙여 보내고 수신자는 아래층부터 주소표를 떼어 원본을 복원한다.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **전송 제어 프로토콜/인터넷 프로토콜(Transmission Control Protocol/Internet Protocol, TCP/IP) 모델**: 인터넷 통신 기능을 네 계층으로 묶은 모델이다.

</details>

| 계층 모델 | **개방형 시스템 간 상호접속 7계층 모델(Open Systems Interconnection 7-Layer Model, OSI 7계층 모델)** | **전송 제어 프로토콜/인터넷 프로토콜(Transmission Control Protocol/Internet Protocol, TCP/IP) 모델** |
|:---|:---|:---|
| 적용 기준 | 계층 책임•장애 분석 | 실제 인터넷 통신 구현 |
| 핵심 특징 | 기능•책임을 7계층으로 분리 | 실제 프로토콜을 4계층으로 통합 |
| 한계 | 실제 프로토콜과 경계 불일치 | 세부 계층 책임 분석 제한 |

> 요약: 책임 분석은 OSI, 구현은 TCP/IP가 핵심이다.

#### 한줄 요약

- OSI는 통신 업무를 세밀히 나눈 설계도이고 TCP/IP는 인터넷에서 실제 쓰는 묶음이다.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **최대 전송 단위(Maximum Transmission Unit, MTU)**: 한 링크에서 단편화 없이 전달할 수 있는 최대 패킷 크기이다.
- **방화벽(Firewall)**: 주소•포트•연결 상태 등의 규칙으로 네트워크 트래픽을 허용하거나 차단하는 보안 장치이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 계층 간 증상이 혼재된 장애 | 물리 계층부터 **프로토콜 데이터 단위(Protocol Data Unit, PDU)** 상향 추적 | 장애 범위 축소 |
| 주소•포트•응용 필드가 혼재된 정책 | 통제 대상에 맞춰 **방화벽(Firewall)** 배치 | 정책 오탐•누락 감소 |
| 헤더 누적으로 MTU 초과 | **최대 전송 단위(Maximum Transmission Unit, MTU)** 산정 | 단편화•폐기 예방 |
| 실제 프로토콜 경계와 모델 불일치 | TCP/IP 경계로 구현 재매핑 | 설계 해석 오류 감소 |

#### 한줄 요약

- 케이블부터 IP와 포트까지 계층 순서로 확인하면 장애 범위를 빠르게 좁힐 수 있다.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **계층별 장애 분석**: 관찰한 프로토콜 데이터 단위와 주소 종류를 기준으로 문제가 시작된 통신 계층을 좁히는 방법이다.
- **점검 시작점 결정**: 오류 데이터 단위와 주소 종류에 해당하는 OSI 계층부터 장애 원인을 확인하는 판단이다.

</details>

- **계층별 장애 분석**과 **점검 시작점 결정**에 따라 PDU•주소 종류에 해당하는 OSI 계층부터 확인한다.

#### 한줄 요약

- 오류가 난 데이터 단위와 주소를 확인하면 어느 계층부터 점검할지 정할 수 있다.
