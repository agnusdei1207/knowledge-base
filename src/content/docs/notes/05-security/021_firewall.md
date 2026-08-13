---
sidebar:
  order: 21
  label: "021. 방화벽 - 패킷 필터•상태기반•NGFW (Firewall)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "방화벽 - 패킷 필터•상태기반•NGFW (Firewall)"
date: "2026-08-13T18:48:54+09:00"
tags:
  - "notes-security"
weight: 21
extra:
  question_no: "021"
  source_status: "기출"
  source_history: "129회, 137회"
  priority: 70
  priority_note: "129•137회 반복이며 경계 보안 설계의 기본 축임"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **방화벽(Firewall)**: 서로 다른 보안 수준을 갖는 네트워크 경계 간 트래픽을 미리 정의된 보안 정책에 따라 차단 또는 허용하는 네트워크 보안 시스템.
- **비무장지대(Demilitarized Zone, DMZ)**: 외부 인터넷에 공개되는 서버(Web, DNS 등)를 내부 핵심 데이터 망과 격리 배치하는 중간 완충 보안 구역.

</details>

- 정의/개념: 보안 구역 경계의 트래픽을 정책으로 통제하는 **방화벽**
- 배경/필요성: 경계 통제 없이는 **비인가 침입•악성 유입•자료 유출**이 가능하다.

#### 한줄 요약

- 보안 구역(Zone) 경계에서 5-Tuple, 세션 상태 및 L7 응용 문맥 기반 통제 정책을 수행하는 경계 보안 시스템

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **기본 거부(Default Deny)**: 보안 정책 룰셋 맨 마지막에 위치하여 명시적으로 허용(Allow)되지 않은 모든 패킷을 무조건 차단(Drop/Reject)하는 원칙.
- **동서 트래픽(East-West Traffic)**: 데이터센터 또는 내부망 서버 간(서버 대 서버) 오가는 수평적 내부 트래픽.

</details>

- IP/Port 5-Tuple 검사부터 L7 애플리케이션 및 위협 서명 심층 검사(DPI)까지 다계층 검사 수행
- 정책 상단부터 순차 매칭(Top-down) 평가 후 최종 **기본 거부(Default Deny)** 적용
- 내부망 수평 침투(Lateral Movement) 차단을 위한 **동서 트래픽(East-West)** 마이크로 세그멘테이션 통제

#### 한줄 요약

- 명시적 허용 이외 차단하는 기본 거부(Default Deny) 원칙, 동서 트래픽(East-West) 격리 및 룰셋 최적화 적용

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **상태 기반 검사(Stateful Inspection)**: TCP 3-Way Handshake 세션의 생성, 유효성, 종료 상태를 상태 테이블(State Table)에 기록하여 정상 세션의 응답 패킷을 자동 허용하는 방식.
- **네트워크 주소 변환(Network Address Translation, NAT)**: 사설 IP 주소를 공인 IP 주소로 변환하여 내부 IP 구조를 숨기고 주소 공간을 절약하는 기술.
- **앱•위협 검사(App & Threat Inspection)**: 포트 번호에 의존하지 않고 L7 페이로드를 분석하여 실제 애플리케이션(L7 App ID) 및 쉘코드/악성코드 서명을 검사하는 엔진.

</details>

```text
방화벽 구조
├─ 정책 룰셋
├─ 상태•NAT
└─ 앱•위협 검사
```

가지의 의미: 정책 매칭, 세션 상태 추적/NAT, L7 앱 및 위협 탐지 책임을 분리한 구조

| 구성요소 | 책임 |
|:---|:---|
| 정책 룰셋 | Top-down 방식의 순차적 허용/차단 보안 규칙 매칭 및 가시성 제공 |
| 상태•NAT | 세션 상태 테이블(State Table) 유지 및 IP/Port NAT 변환 연산 |
| 앱•위협 검사 | L7 DPI 기반 App-ID 식별, IPS 서명 대조 및 샌드박스 연동 위협 차단 |


#### 한줄 요약

- 정책 룰셋 엔진, 상태표(State Table) 기반 상태 검사(Stateful Inspection) 및 L7 애플리케이션 위협 검사 아키텍처

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **5-튜플(5-Tuple)**: 패킷 헤더에서 추출한 출발지 IP, 목적지 IP, 출발지 Port, 목적지 Port, 프로토콜(Protocol) 5개 식별 정보.
- **5-튜플 연결 상태 조회**: 입력 패킷의 5-Tuple 정보를 기존 세션 상태 테이블(State Table)과 매칭 대조하는 단계.
- **룰셋•위협 검사**: 미등록 세션에 대해 방화벽 보안 룰셋 및 L7 위협 서명을 순차 검사하는 단계.
- **세션 상태 갱신**: 허용 결정된 패킷의 세션 정보를 상태 테이블에 즉시 등록(State Update)하는 단계.

</details>

```text
신규 패킷
        │
        ▼
1. 5-튜플 연결 상태 조회
        │
        ▼
2. 룰셋•위협 검사
        ├─ 차단: 차단 결과 반환
        └─ 허용
             │
             ▼
     3. 세션 상태 갱신
             │
             └── 허용 패킷 전달
```

### 동작 원리

1. **5-튜플 연결 상태 조회**: 수신 패킷의 5-Tuple 추출 후 세션 상태 테이블 존재 여부 확인
2. **룰셋•위협 검사**: 상태 미등록 신규 세션에 대해 Top-down 정책 룰셋 및 L7 App/위협 패턴 검사
3. **세션 상태 갱신**: 검사 통과 시 세션 상태 테이블에 신규 등록 후 역방향 응답 패킷 자동 허용 및 전달 완료


#### 한줄 요약

- 5-Tuple 세션 상태 테이블 조회, 룰셋/위협 검사, 세션 상태 표 갱신(State Update) 및 패킷 전달 흐름

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **차세대 방화벽(Next-Generation Firewall, NGFW)**: 전통적 상태 기반 방화벽에 DPI, L7 App-ID, 사용자 식별(User-ID), IPS 및 샌드박스를 일체형 통합한 방화벽.
- **패킷 필터(Packet Filter)**: L3/L4 헤더(5-Tuple) 정보만으로 단순 차단/허용을 판정하는 1세대 방화벽.
- **상태 기반 방화벽(Stateful Inspection Firewall)**: TCP 세션 연결 상태를 상태표로 관리하여 5-Tuple 오버헤드를 줄인 2세대 방화벽.

</details>

| 방화벽 방식 | **패킷 필터 (1세대)** | **상태 기반 방화벽 (2세대)** | **차세대 방화벽 (NGFW, 3세대)** |
|:---|:---|:---|:---|
| 적용 기준 | 라우터/L3 스위치 기본 통제 | 일반 네트워크 경계 기본 방어 | L7 애플리케이션 및 멀티위협 종합 방어 |
| 핵심 특징 | L3/L4 5-Tuple 단순 정적 필터링 | 세션 상태 테이블 기반 동적 상태 추적 | L7 DPI, App-ID, User-ID, IPS 통합 |
| 한계 | 포트 스푸핑 및 L7 공격 미탐 | 상태 테이블 고갈(Syn Flood) 공격 | SSL/TLS 복호화 성능 오버헤드 |

> 요약: 검사 깊이(L3/L4 vs L7) 및 요구 성능 오버헤드에 따른 방화벽 세대별 채택

#### 한줄 요약

- 1세대 패킷 필터, 2세대 상태 기반(Stateful), 3세대 차세대 방화벽(NGFW)의 기능 계층 및 성능 오버헤드 비교 선택

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **음영 규칙(Shadowed Rule)**: 상위에 배치된 넓은 허용 범위 규칙에 의해 하위의 구체적 차단 규칙이 실행되지 못하고 무효화되는 우회 룰 오류.
- **NIST SP 800-41 Rev. 1(NIST SP 800-41 Standard)**: 조직의 방화벽 정책 수립, 위치 선정 및 룰셋 아키텍처 권고 지침.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 방화벽 설계/정책 기준 미비 | **NIST SP 800-41 Rev. 1** 준수 | 객관적 룰셋 구성 및 배치 표준화 |
| 과다/보안 우회 **음영 규칙** | 정기적 **룰셋 감사(Rule Audit) 및 최적화** | 정책 우회 구멍 소거 및 검사 속도 향상 |
| DMZ 경과 수평 침투 위험 | **Zone 기반 격리 및 2중 방화벽(Double DMZ)** | 내부 핵심 망으로의 수평 이동(Lateral Movement) 차단 |
| 암호화 트래픽 내 은닉 공격 | **SSL/TLS 복호화(Inbound/Outbound SSL Inspection)** | 암호화 팩 내 악성 코드 및 유출 통제 |

#### 한줄 요약

- NIST SP 800-41 Rev. 1 준수, 음영 규칙(Shadowed Rule) 주기적 감사 및 DMZ 구역 분리 통제

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **정책 실효성(Policy Effectiveness)**: 방화벽 룰셋의 최소 권한(Least Privilege) 준수 및 정기 감사를 통해 유지되는 보안 통제 성능.

</details>

- 보안 요구수준에 따라 헤더 통제는 **패킷 필터**, 세션 추적은 **상태 기반 방화벽**, L7 위협 방어는 **차세대 방화벽(NGFW)** 적용

#### 한줄 요약

- **기본 거부•상태 추적•L7 검사•룰셋 감사**를 함께 적용
