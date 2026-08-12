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

- **TCP(Transmission Control Protocol)**: 전송 순서 보장 및 재전송 제어를 통해 신뢰성 높은 스트림 전송을 제공하는 프로토콜.
- **IP(Internet Protocol)**: 호스트 주소 지정을 기반으로 패킷의 라우팅과 전달을 담당하는 프로토콜.
- **TCP/IP 모델(TCP/IP Model)**: 인터넷 통신 기능을 공통 IP 계층 중심의 4개 계층으로 구조화한 모래시계형 실무 프로토콜 아키텍처.

</details>

- 정의/개념: 인터넷 통신 기능을 공통 IP 중심의 네 계층으로 묶은 **TCP/IP 모델(TCP/IP Model)**.
- 배경/필요성: 응용 및 통신 매체별 전용 규약 사용 시 이기종 네트워크 간 상호운용성 제약 발생.

#### 한줄 요약

- 이기종 네트워크 및 응용 간의 결합도 분리를 위해 IP 계층 중심의 모래시계(Thin-Waist) 아키텍처를 적용한다.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **얇은 허리 구조(Thin-Waist Architecture)**: 다양한 상위 응용과 하위 전송 매체 사이에서 공통 IP 계층을 중추로 연결하는 유연한 설계 아키텍처.
- **최선형 전달(Best-Effort Delivery)**: 수신 여부나 전송 순서를 보장하지 않고 최선의 경로로 패킷을 전송하는 비신뢰성 전달 방식.
- **종단 간 원칙(End-to-End Principle)**: 네트워크 코어는 단순화하고 데이터 신뢰성 및 흐름 제어를 종단 호스트에서 처리하는 아키텍처 규범.

</details>

- **얇은 허리 구조(Thin-Waist Architecture)**를 통한 응용과 통신 매체 간 의존성 완화.
- **IP(Internet Protocol)**의 **최선형 전달(Best-Effort Delivery)** 특성 활용.
- **종단 간 원칙(End-to-End Principle)** 기반 **TCP(Transmission Control Protocol)**의 신뢰성 확보 및 혼잡 제어 수행.

#### 한줄 요약

- 종단 간 원칙(End-to-End Principle)에 따라 중간 라우터는 최선형 패킷 전송만 수행하고 종단 호스트의 TCP가 신뢰성 및 혼잡 제어를 전담한다.


## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **포트(Port)**: 단일 호스트 내부에서 작동하는 응용 프로세스를 식별하기 위한 논리적 채널 번호.
- **IP 주소(IP Address)**: 패킷의 출발지와 목적지 호스트를 식별하여 상호 간 라우팅을 가능하게 하는 논리 주소.
- **네트워크 접근 계층(Network Access Layer)**: 물리적 전송 매체 제어 및 인접 노드 간 프레임 전송을 담당하는 최하위 계층.

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

선의 의미: 인접 계층 간 서비스 인터페이스로서 응용 메시지, 포트 기반 종단 전달, IP 기반 네트워크 전달, 링크 접근 책임을 상호 분리 및 결합하는 관계 표시.

| 구성요소 | 책임 |
|:---|:---|
| 응용 계층 | 응용 간 메시지 및 동작 규격 정의 |
| 전송 계층 | **포트(Port)** 기반 종단 간 신뢰성 전달 제어 |
| 인터넷 계층 | **IP 주소(IP Address)** 기반 네트워크 간 라우팅 수행 |
| **네트워크 접근 계층** | 링크 규칙 기반 인접 장치 간 프레임 전송 |

#### 한줄 요약

- Application Layer Message $\rightarrow$ Transport Layer Segment (Port No.) $\rightarrow$ Internet Layer Packet (IP Address) $\rightarrow$ Network Access Layer Frame (MAC Address) 수순으로 캡슐화된다.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **캡슐화(Encapsulation)**: 상위 계층 데이터에 하위 계층 제어 헤더를 부착하여 전송 단위를 생성하는 프로세스.
- **역캡슐화(Decapsulation)**: 수신 측에서 하위 계층 헤더를 순차적으로 제거하여 상위 응용 메시지를 추출하는 과정.

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

1. **캡슐화(Encapsulation)**: 포트, IP, 링크 제어 정보의 계층별 결합 수행.
2. **역캡슐화(Decapsulation)**: 계층 역순의 제어 정보 제거를 통한 메시지 복원.

#### 한줄 요약

- Data Encapsulation(Header Tagging) 및 Decapsulation (Header Stripping) 대칭 처리를 집행한다.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **개방형 시스템 간 상호접속 모델(Open Systems Interconnection Model, OSI Model)**: 국제표준화기구(ISO)에서 정의한 7계층 기준 통신 참조 아키텍처.

</details>

| 계층 모델 | **TCP/IP 모델** | **개방형 시스템 간 상호접속 모델(Open Systems Interconnection Model, OSI 모델)** |
|:---|:---|:---|
| 적용 기준 | 인터넷 통신 구현•분석 | 계층 책임•장애 분석 |
| 핵심 특징 | 프로토콜을 4계층으로 통합 | 통신 책임을 7계층으로 세분 |
| 한계 | 세부 계층 책임이 함께 묶임 | 프로토콜과 경계 불일치 |

> 요약: 실무 구현 측면의 TCP/IP 모델과 계층적 책임 분석 측면의 OSI 모델 간 역할 분담.

#### 한줄 요약

- TCP/IP 4-Layer는 Practical Internet Standard Protocol Suite, OSI 7-Layer는 Structural Reference & Diagnostic Model로 역할이 분이된다.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **사용자 데이터그램 프로토콜(User Datagram Protocol, UDP)**: 핸드셰이크와 재전송 없이 최속 전송을 수행하여 실시간 통신에 적합한 비연결형 전송 프로토콜.
- **최대 전송 단위(Maximum Transmission Unit, MTU)**: 데이터 링크에서 단편화 없이 한번에 전송할 수 있는 패킷의 최대 크기 규격.

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

- **모델 적용 기준(Model Application Criteria)**: 실무 구현 시 TCP/IP를, 정밀 진단 시 OSI 7계층 모델을 선택적으로 적용하는 분석 지침.

</details>

- **모델 적용 기준(Model Application Criteria)**에 따라 인터넷 시스템 구현 시 TCP/IP를 적용하고, 세부 장애 발생 시 OSI 모델 기반 체계적 진단 수행.

#### 한줄 요약

- 인터넷 표준 시스템 구축 시 TCP/IP Protocol Stack 구현과 PMTU (Path MTU Discovery) 및 Layered Troubleshooting 절차를 정립한다.


