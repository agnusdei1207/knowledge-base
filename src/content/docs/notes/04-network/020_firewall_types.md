---
sidebar:
  order: 20
  label: "020. 방화벽 패킷 필터•NGFW"
  badge:
    text: "기출 · 70%"
    variant: note
title: "방화벽 : 패킷 필터•상태기반•NGFW (Firewall Types)"
date: "2026-08-26T13:40:42+09:00"
tags:
  - "notes-network"
weight: 20
extra:
  question_no: "20"
  source_status: "기출"
  source_history: "129회, 137회"
  priority: 70
  priority_note: "패킷 필터, 상태 기반 및 차세대 방화벽(NGFW) 계층별 동작"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Firewall (방화벽)**: 서로 다른 신뢰 수준의 네트워크 경계(Trust/Untrust/DMZ)에서 보안 정책(ACL)에 따라 인가된 패킷만 통과시키는 보안 장치.
- **Default Deny (기본 차단)**: 명시적으로 허용된 규칙 외의 모든 인바운드/아웃바운드 트래픽을 최종적으로 전부 드롭(Drop)하는 제로 트러스트 보안 원칙.

</details>

- 정의/개념: 네트워크 경계에서 **Default Deny 원칙 하에 L3/L4 헤더 및 L7 페이로드를 검사하여 트래픽 유입·유출을 제어하는 경계 보안 시스템**
- 배경/필요성: 1세대 단순 패킷 필터링의 한계로 인한 **동적 포트 기반 세션 추적 불가, 80/443 포트로 은닉 침투하는 L7 애플리케이션 위협 방어 불가**를 겪으므로, 경계에 연결 상태 테이블과 L7 페이로드 검사 계층을 차례로 덧대어 패킷 한 장씩 내리던 판단을 세션 문맥과 애플리케이션 문맥 위로 끌어올릴 필요

#### 한줄 요약
- Default Deny 원칙과 세션 상태 추적 및 L7 DPI 검사를 통해 경계 네트워크를 방어한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Stateful Inspection (상태 기반 추적)**: TCP 3-Way Handshake 및 5-튜플 상태를 메모리 테이블에 기록하여 아웃바운드 세션의 응답 패킷을 자동 허용하는 기술.
- **DPI (Deep Packet Inspection)**: 전송 계층 헤더를 넘어 L7 응용 페이로드 내부를 심층 파싱하여 악성코드 및 App-ID를 식별하는 기술.

</details>

- 명시적 허용 규칙 외 모든 트래픽을 차단하는 **기본 차단(Default Deny) 및 최소 권한 원칙**
- 세션 테이블 기반의 **상태 추적(Stateful Inspection)**을 통해 아웃바운드 요청의 회신 패킷 자동 통과
- 차세대 방화벽(NGFW)의 **심층 패킷 검사(DPI)**를 통한 포트 비종속적 애플리케이션 식별 및 IPS 연동

#### 한줄 요약
- Default Deny 원칙, 상태 테이블 세션 추적, DPI 기반 L7 애플리케이션 제어를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Security Zone (보안 존)**: 동일한 신뢰 수준과 보안 정책이 적용되는 인터페이스 논리 그룹 (Trust, Untrust, DMZ).
- **State Table (상태 테이블)**: 활성 세션의 5-튜플, TCP 상태 머신, 세션 수명 타이머를 실시간 저장하는 RAM 테이블.

</details>

```text
[방화벽 보안 존 분리 및 계층별 패킷 검사 아키텍처]
|-- Untrust Zone (외부 인터넷 / 공중망)
`-- Firewall Security Gateway
    |-- Zone-Based Policy Router (Untrust -> DMZ, Untrust -> Trust 인입 식별)
    |-- Stateful Session Engine (State Table 선행 조회 -> 기존 세션 자동 통과)
    |-- Rulebase Policy Engine (Top-Down 순차적 ACL 매칭 -> Allow / Deny 판정)
    `-- DPI & Threat Engine (L7 App-ID, IPS, Antivirus, SSL Decryption)
|-- DMZ Zone (외부 공개 서버군: Web, DNS, Mail)
`-- Trust Zone (사내 내부 업무망 / 데이터베이스 서버군)
```

선의 의미: 계층 및 외부 Untrust 패킷이 세션 테이블 조회와 Top-Down ACL 매칭 및 DPI 검사를 거쳐 DMZ 또는 내부 Trust로 전달되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **보안 존 (Security Zone)**| 신뢰 수준별 네트워크 구획화(**Trust 업무망, Untrust 외부망, DMZ 공개망**) | 존 기반 정책 |
| **정책 규칙 베이스 (ACL)**| 상단부터 순차적으로 평가되는 **패킷 허용/차단/로깅 규칙 집합 (Top-Down 순차 평가)** | 순차 룰 매칭 |
| **상태 테이블 (State Table)**| 활성 세션의 **5-튜플 및 TCP 연결 상태를 메모리에 유지하여 회신 트래픽 자동 통과** | 메모리 상주 |
| **DPI 위협 엔진 (NGFW)** | L7 애플리케이션 제어(**App-ID**), IPS 시그니처 검사, 안티바이러스 및 SSL 복호화 | 심층 보안 검사 |

#### 한줄 요약
- 상태 테이블은 규칙 베이스 앞에 놓인 세션 사본 계층이라 이미 허용된 연결의 회신 패킷은 Top-Down ACL 전수 평가를 건너뛰고, 세션 첫 패킷만 DPI까지 이르는 온전한 검사 비용을 치른다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Top-Down Rule Evaluation (규칙 순차 평가)**: 인입 패킷에 대해 방화벽 룰셋을 1번부터 차례대로 매칭하여 최초로 일치하는 규칙의 액션을 즉시 실행하는 방식.

</details>

```text
방화벽 인입 패킷 검사 및 포워딩 파이프라인
        │
   1. [패킷 인입 및 보안 존 확인] 인입 인터페이스와 목적지 인터페이스의 Zone 식별
        │
   2. [상태 테이블 선행 조회] 메모리 내 활성 세션 테이블 조회
   ┌────┴───────────────────────────┐
  기존 세션 일치 (Established)    신규 세션 인입 (SYN 패킷)
   │                                 │
   │                            3. [Top-Down 보안 정책 매칭]
   │                               상단부터 룰 순차 평가 (Allow / Deny)
   │                               ┌─ Deny 매칭: 패킷 폐기(Drop) 및 로그
   │                               └─ Allow 매칭: 4단계 DPI 진입
   │                                 │
   ├─────────────────────────────────┘
   ▼
4. [DPI 위협 검사 (NGFW)] L7 App-ID 식별 및 IPS 취약점 스캔
        │
   5. [상태 테이블 등록 및 전달] 신규 세션 상태 테이블 등록 후 최종 목적지로 포워딩
```

#### 한줄 요약
- 상태 테이블 선행 조회 후 신규 연결에 대해 Top-Down ACL 매칭과 DPI 검사를 거쳐 포워딩한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **1세대 Packet Filter** vs **2세대 Stateful Inspection** vs **3세대 Next-Generation Firewall (NGFW)**.

</details>

| 비교 항목 | 1세대 패킷 필터링 | 2세대 상태 기반 (Stateful) | 3세대 차세대 방화벽 (NGFW) |
|:---|:---|:---|:---|
| **검사 계층 및 깊이** | **L3 네트워크, L4 전송 계층** | **L3, L4 (연결 문맥 포함)** | **L3 ~ L7 전 계층 (심층 페이로드)** |
| **세션 상태 추적** | **미지원 (비상태형, Stateless)** | **지원 (세션 상태 테이블 관리)** | **지원 (세션 + 앱 컨텍스트 추적)** |
| **애플리케이션 제어** | 포트 번호 기반 단순 판별 | 포트 번호 기반 단순 판별 | **포트 비종속적 앱 식별 (App-ID)** |
| **보안 위협 차단** | 단순 IP / Port 접근 통제 | SYN Flood 등 세션 기반 방어 | **IPS, 안티바이러스, SSL 복호화 연동** |

#### 한줄 요약
- 단순 헤더 검사(1세대)에서 세션 상태 추적(2세대), L7 DPI 및 App-ID 식별 기반(NGFW)으로 발전했다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Rule Shadowing (규칙 섀도잉)**: 상단의 포괄적인 허용/차단 규칙으로 인해 하단의 세부 보안 규칙이 영원히 매칭되지 못하고 무력화되는 정책 결함.
- **SSL Decryption (SSL 복호화)**: HTTPS 암호화 트래픽을 방화벽에서 복호화하여 L7 페이로드 내 악성코드 유무를 검사하는 기능.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 공개 웹서버 침해 시 내부 업무망 및 DB로의 횡적 이동(Lateral Movement) | **`DMZ 보안 존 분리` 및 Zone 간 엄격한 단방향 트래픽 정책** | 웹 서버 해킹 시에도 내부망 2차 침투(Pivot) 차단 |
| 상단 포괄적 규칙으로 하단 세부 규칙이 무력화되는 Rule Shadowing | **방화벽 정책 분석 도구 적용 및 `구체적 규칙 상단 배치 원칙`** | 정책 사각지대 및 비인가 보안 구멍 원천 차단 |
| HTTPS 암호화로 인해 L7 악성코드 및 C2 통신 검사 불가 | **NGFW의 `Inbound/Outbound SSL/TLS 복호화(SSL Decryption)`** | 암호화 악성코드 탐지 및 가시성 100% 확보 |
| 방화벽 장비 장애 시 전사 인터넷 단절 단일 장애점(SPOF) | **Active-Standby / Active-Active `HA 이중화 및 상태 동기화`** | 장비 장애 시 서브세컨드 무중단 절체 보장 |

#### 한줄 요약
- DMZ 존 분리, 구체적 규칙 상단 배치, SSL 복호화, HA 이중화로 운영한다.

## Ⅶ. 결론

- 단순 헤더 통제는 **상태 기반**, L7 위협은 **NGFW** 선택

#### 한줄 요약
- 방화벽은 Default Deny 원칙과 세션 추적 및 L7 DPI 검사를 통해 비인가 트래픽을 차단하는 핵심 네트워크 경계 보안 기술이다.
