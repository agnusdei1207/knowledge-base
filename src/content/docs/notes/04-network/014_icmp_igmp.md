---
sidebar:
  order: 14
  label: "014. ICMP•IGMP (ICMP IGMP)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "ICMP•IGMP (ICMP IGMP)"
date: "2026-08-04T14:56:00+09:00"
tags:
  - "notes-network"
weight: 14
extra:
  question_no: "014"
  source_status: "기출"
  source_history: "132회"
  priority: 30
  priority_note: "비교형: 132회 ICMP•IGMP 역할 직접 비교"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **ICMP(Internet Control Message Protocol)**: IP 전달 오류와 진단 상태를 알리는 프로토콜이다.
- **IGMP(Internet Group Management Protocol)**: IPv4 멀티캐스트 그룹 가입을 관리하는 프로토콜이다.
- **인터넷 프로토콜(Internet Protocol, IP)**: 주소를 기반으로 패킷을 목적지까지 전달하는 네트워크 계층 프로토콜이다.
- **인터넷 프로토콜 버전 4(Internet Protocol version 4, IPv4)**: 32비트 주소를 사용해 패킷을 목적지까지 전달하는 네트워크 계층 프로토콜이다.

</details>

- 정의/개념: **ICMP와 IGMP** — 각각 IP 전달 오류•진단 상태를 통보하고 IPv4 멀티캐스트 그룹의 가입 상태를 관리하는 **네트워크 제어 프로토콜**
- 배경/필요성: IP 단독 전달의 **실패 원인•그룹 수신자 미관리**

#### 한줄 요약

- ICMP는 배달 실패를 알리고 IGMP는 방송 수신자를 관리한다

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **ICMP 유형(Type)**: ICMP 메시지의 종류를 구분하는 필드이다.
- **ICMP 코드(Code)**: 같은 유형 안에서 세부 오류와 상태 원인을 구분하는 필드이다.
- **IGMP 질의(Query)**: 라우터가 호스트의 그룹 가입 상태를 확인하는 메시지이다.
- **IGMP 보고(Report)**: 호스트가 가입한 멀티캐스트 그룹을 알리는 메시지이다.
- **IGMP 탈퇴(Leave)**: 호스트가 멀티캐스트 그룹 탈퇴를 알리는 메시지이다.

</details>

- ICMP 유형•코드의 **오류 원인•진단 구분**
- ICMP 원 패킷 인용의 **실패 흐름 식별**
- IGMP 질의•보고•탈퇴의 **가입 상태 갱신**

#### 한줄 요약

- ICMP는 원 패킷 일부를 실어 실패 흐름을 식별하고 IGMP는 호스트의 멀티캐스트 그룹 가입 상태를 갱신한다

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **IGMP 스누핑(IGMP Snooping)**: 스위치가 가입 메시지를 관찰해 그룹별 수신 포트를 학습하는 기능이다.
- **IGMP 질의자(IGMP Querier)**: 호스트에 가입 상태를 주기적으로 묻는 라우터이다.
- **가상 근거리 통신망(Virtual Local Area Network, VLAN)**: 하나의 물리 스위치망을 논리적인 브로드캐스트 영역으로 분리한 네트워크이다.

</details>

```mermaid
block-beta
    columns 1
    H["IP•멀티캐스트 호스트"]
    block:CONTROL
        columns 2
        I["ICMP 처리기"]
        Q["IGMP 질의자"]
    end
    S[("IGMP 스누핑 표")]
    H --- I
    H --- Q
    Q --- S
```

| 구성요소 | 책임 |
|:---|:---|
| IP•멀티캐스트 호스트 | **ICMP 오류 수신•IGMP 가입 보고** |
| ICMP 처리기 | **유형•코드** 와 원 패킷 일부 반환 |
| IGMP 질의자 | 그룹별 **수신자 존재 여부** 질의 |
| IGMP 스누핑 표 | **VLAN•그룹•가입 포트** 관계 저장 |

#### 한줄 요약

- ICMP는 실패 원인을 보내고 IGMP는 방송 가입자를 관리해 서로 다른 문제를 해결한다

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **멀티캐스트(Multicast)**: 하나의 송신 데이터를 특정 그룹에 가입한 여러 수신자에게 전달하는 방식이다.

</details>

```mermaid
sequenceDiagram
    participant R as 라우터
    participant H as 호스트
    participant S as 스위치
    participant T as IGMP 스누핑 표
    alt IP 전달 실패
        R-->>H: 1. ICMP 유형•코드
    else 멀티캐스트 가입 확인
        R->>H: 2. IGMP 질의
        H->>S: 3. IGMP 보고
        S->>T: 4. 가입 포트 갱신
        S-->>R: IGMP 보고
    end
```

**동작 원리**

1. **ICMP 유형•코드**: 실패 원인과 원 패킷 일부로 흐름 식별
2. **IGMP 질의**: 링크의 그룹 수신자 존재 여부 확인
3. **IGMP 보고**: 호스트가 가입 그룹을 알리고 스위치가 입력 포트 관찰
4. **가입 포트 갱신**: VLAN별 그룹•가입 포트 관계 저장

#### 한줄 요약

- 전달 오류는 송신자에게 알리고 방송 가입 변화는 수신 포트 표에 반영한다

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **경로 최대 전송 단위 탐색(Path Maximum Transmission Unit Discovery, PMTUD)**: ICMP 오류로 경로에서 단편화 없는 최대 패킷 크기를 찾는 절차이다.

</details>

| 제어 프로토콜 | ICMP | IGMP |
|:---|:---|:---|
| 적용 기준 | 도달성•경로•**패킷 크기 진단** | 멀티캐스트 **수신자•가입 포트 관리** |
| 핵심 특징 | 유형•코드의 **IP 오류•상태 통보** | 질의•보고•탈퇴의 **가입 교환** |
| 한계 | 과도 차단 시 **진단•PMTUD 실패** | 상태 오류 시 **과다 전달•수신 단절** |

> 요약: ICMP는 오류 진단, IGMP는 그룹 가입 관리

#### 한줄 요약

- ICMP는 배달 실패를 알리고 IGMP는 방송 가입 상태를 관리한다

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **ICMP 전송률 제한**: 일정 시간에 처리할 ICMP 메시지 수를 제한해 과부하•반사 트래픽을 줄이는 기능이다.
- **알 수 없는 멀티캐스트 플러딩(Unknown Multicast Flooding)**: 가입 포트를 모르는 프레임을 VLAN의 여러 포트로 전달하는 동작이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| ICMP 일괄 차단으로 PMTUD•진단 실패 | **PMTUD•진단 유형** 선별 허용 | **전송 실패 원인** 확인 |
| 위조 요청에 ICMP 응답이 과다 발생 | 유형별 **전송률•발신 범위** 제한 | **반사 공격 트래픽** 축소 |
| 질의자 중단으로 IGMP 상태가 만료 | **질의자•스누핑 상태** 감시 | **멀티캐스트 수신 단절** 예방 |
| 미가입 포트로 멀티캐스트가 확산 | VLAN별 **IGMP 스누핑** 적용 | **불필요 트래픽** 감소 |

#### 한줄 요약

- ICMP를 전부 차단하면 큰 패킷이 막힌 이유를 몰라 전송이 계속 실패할 수 있다

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **ICMP 선별 허용**: 필요한 ICMP 유형만 통과시키는 통제 원칙이다.
- **IGMP 가입 범위 제한**: 가입 포트에만 멀티캐스트를 전달하는 통제 원칙이다.

</details>

- 도달성•PMTUD에는 **ICMP 선별 허용**, 멀티캐스트 포트에는 **IGMP 스누핑** 적용

#### 한줄 요약

- IP 실패 알림과 멀티캐스트 가입 관리는 역할이 다르므로 허용 규칙을 나눠야 한다.
