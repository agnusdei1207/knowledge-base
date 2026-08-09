---
sidebar:
  order: 2
  label: "002. TCP/IP 4계층 모델 (TCP/IP Model)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "TCP/IP 4계층 모델 (TCP/IP Model)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-network"
weight: 2
extra:
  question_no: "002"
  source_status: "기출"
  source_history: "120회, 125회, 128회, 129회, 132회"
  priority: 70
  priority_note: "비교형: 다회차 전송 문제의 공통 4계층 기준"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **TCP(Transmission Control Protocol)**: 순서와 재전송을 제어하여 신뢰성 있는 바이트 흐름을 제공하는 전송 프로토콜이다.
- **IP(Internet Protocol)**: 주소를 기반으로 네트워크 사이에서 패킷을 전달하는 프로토콜이다.
- **TCP/IP 모델**: 인터넷 통신 기능을 공통 IP 계층 중심의 네 계층으로 묶은 구현 모델이다.

</details>

- 정의/개념: 인터넷 통신 기능을 공통 IP 중심의 네 계층으로 묶은 **TCP/IP 모델**이다.
- 배경/필요성: 응용•매체별 전용 규약은 이기종 통신 확장을 제약한다.

#### 한줄 요약

- Heterogeneous Network & Application 간의 Decoupling을 위해 IP(Internet Protocol) 계층을 중심으로 하는 Hourglass (Thin-Waist) Architecture를 적용한다.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **얇은 허리 구조**: 다양한 응용과 통신 매체가 공통 인터넷 프로토콜 계층을 사이에 두고 독립적으로 발전하는 구조이다.
- **최선형 전달**: 인터넷 프로토콜이 패킷의 도착•순서•중복 제거를 보장하지 않고 가능한 범위에서 전달하는 방식이다.
- **종단 간 원칙**: 신뢰성이나 혼잡 제어 기능을 중간망보다 송수신 호스트에서 완성하는 설계 원칙이다.

</details>

- **얇은 허리 구조**로 응용•통신 매체 결합을 완화한다.
- **IP(Internet Protocol)**의 **최선형 전달**을 사용한다.
- **종단 간 원칙**에 따라 **TCP(Transmission Control Protocol)**가 신뢰성과 혼잡을 제어한다.

#### 한줄 요약

- End-to-End Principle에 따라 Intermediate Routers는 Best-Effort Packet Forwarding만 수행하고, End-Host Transport Layer(TCP)에서 Reliability and Congestion Control을 전담한다.


## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **포트**: 한 호스트 안에서 데이터가 도착할 응용 프로세스를 구분하는 번호이다.
- **IP 주소**: 패킷의 출발지와 목적지 호스트를 식별해 네트워크 간 전달 경로를 정하는 주소이다.
- **네트워크 접근 계층**: 링크별 프레임과 매체 규칙으로 인접 장치 사이의 전송을 담당하는 계층이다.

</details>

```text
응용 계층
│
전송 계층
│
인터넷 계층
│
네트워크 접근 계층
```

선의 의미: 각 선은 인접 계층의 서비스 인터페이스이며, 응용 메시지•포트 기반 종단 전달•IP 기반 네트워크 전달•링크 접근 책임을 분리하면서 결합하는 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| 응용 계층 | 응용 간 메시지•동작 정의 |
| 전송 계층 | **포트** 기반 종단 간 전달 제어 |
| 인터넷 계층 | **IP 주소** 기반 네트워크 간 전달 |
| **네트워크 접근 계층** | 링크 규칙으로 인접 장치 전달 |

#### 한줄 요약

- Application Layer Message $\rightarrow$ Transport Layer Segment (Port No.) $\rightarrow$ Internet Layer Packet (IP Address) $\rightarrow$ Network Access Layer Frame (MAC Address) 수순으로 캡슐화된다.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **캡슐화**: 응용 데이터에 포트•IP•링크 제어 정보를 계층 순서대로 결합하는 과정이다.
- **역캡슐화**: 수신 측이 계층의 반대 순서로 제어 정보를 제거하여 응용 메시지를 복원하는 과정이다.

</details>

```text
송신 응용 메시지
      |
      v
1. 캡슐화
      |
      +-- 응용 계층 -------- 메시지
      +-- 전송 계층 -------- TCP 세그먼트•UDP 데이터그램
      +-- 인터넷 계층 ------ IP 패킷
      `-- 네트워크 접근 ---- 링크 프레임
                                  |
                                  v
                              라우터 경로
                                  |
                                  +-- 링크별 프레임 교체
                                  `-- 공통 IP 패킷 전달
                                             |
                                             v
                                      2. 역캡슐화
                                             |
                                             `-- 수신 응용 메시지
```

### 동작 원리

1. **캡슐화**: 포트•IP•링크 제어 정보를 계층별로 결합한다.
2. **역캡슐화**: 계층 역순으로 제어 정보를 제거해 메시지를 복원한다.

#### 한줄 요약

- Data Encapsulation(Header Tagging) 및 Decapsulation (Header Stripping) 대칭 처리를 집행한다.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **개방형 시스템 간 상호접속 모델(Open Systems Interconnection Model, OSI 모델)**: 통신 책임을 일곱 계층으로 세분한 설계와 장애 분석의 참조 모델이다.

</details>

| 계층 모델 | **TCP/IP 모델** | **개방형 시스템 간 상호접속 모델(Open Systems Interconnection Model, OSI 모델)** |
|:---|:---|:---|
| 적용 기준 | 인터넷 통신 구현•분석 | 계층 책임•장애 분석 |
| 핵심 특징 | 실제 프로토콜을 4계층으로 통합 | 통신 책임을 7계층으로 세분 |
| 한계 | 세부 계층 책임이 함께 묶임 | 실제 프로토콜과 경계 불일치 |

> 요약: 구현은 TCP/IP, 책임 분석은 OSI가 핵심이다.

#### 한줄 요약

- TCP/IP 4-Layer는 Practical Internet Standard Protocol Suite, OSI 7-Layer는 Structural Reference & Diagnostic Model로 역할이 분이된다.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **사용자 데이터그램 프로토콜(User Datagram Protocol, UDP)**: 연결 설정과 재전송 없이 데이터그램을 보내 전송 지연과 제어 부담을 줄이는 전송 프로토콜이다.
- **최대 전송 단위(Maximum Transmission Unit, MTU)**: 한 링크에서 단편화 없이 전달할 수 있는 최대 패킷 크기이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 여러 계층의 장애 증상이 혼재 | 링크•IP•포트•응용 순 계층 진단 | 원인 범위 축소 |
| 손실•순서•지연 요구가 불명확 | **TCP(Transmission Control Protocol)**•**사용자 데이터그램 프로토콜(User Datagram Protocol, UDP)** 선택 | 전송 동작과 요구 일치 |
| 캡슐화 헤더로 MTU 초과 | **최대 전송 단위(Maximum Transmission Unit, MTU)**•헤더 크기 산정 | 단편화•전송 실패 예방 |
| 중간망의 응용별 상태 의존 증가 | **종단 간 원칙**으로 중간망 기능 최소화 | 새 응용•매체의 추가 영향 감소 |

#### 한줄 요약

- Network Access $\rightarrow$ Internet (IP) $\rightarrow$ Transport (Port) $\rightarrow$ Application 계층 순으로 Bottom-Up Troubleshooting을 수행한다.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **모델 적용 기준**: 인터넷 구현은 TCP/IP, 세부 책임 분석은 OSI 모델을 적용하는 기준이다.

</details>

- **모델 적용 기준**에 따라 인터넷 구현은 TCP/IP, 세부 장애 책임은 OSI 모델로 분석한다.

#### 한줄 요약

- 인터넷 표준 시스템 구축 시 TCP/IP Protocol Stack 구현과 PMTU (Path MTU Discovery) 및 Layered Troubleshooting 절차를 정립한다.

