---
sidebar:
  order: 21
  label: "021. 방화벽 - 패킷 필터•상태기반•NGFW"
  badge:
    text: "기출 · 70%"
    variant: note
title: "네트워크 경계 접근 통제 기술 : 방화벽 및 차세대 방화벽"
date: "2026-08-25T13:00:00+09:00"
tags:
  - "notes-security"
weight: 21
extra:
  question_no: "21"
  source_status: "기출"
  source_history: "129회, 137회"
  priority: 70
  priority_note: "1세대(패킷 필터링), 2세대(상태기반 Stateful), 3세대(차세대 방화벽 NGFW/DPI/App-ID), Default Deny 및 SSL 가시성"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Firewall (방화벽)**: 보안 정책 룰셋에 따라 인가된 트래픽만 선별 허용하고 비인가 패킷을 차단하는 경계 방어 시스템.
- **DMZ (Demilitarized Zone, 완충 구역)**: 외부 공개 서버를 내부 핵심 데이터베이스망과 분리하여 횡적 이동을 차단하는 완충 영역.

</details>

- 정의/개념: L3/L4 5-Tuple과 세션 상태 추적(Stateful) 및 L7 App-ID/DPI 심층 검사를 통해 **인가된 트래픽만 선별 허용하는 네트워크 경계 접근 통제 기술**
- 배경/필요성: 1세대 단순 포트 필터링의 **정상 포트(80/443) 위장 악성 트래픽 투과, 암호화 세션 내 위협 은닉 및 L7 애플리케이션 식별 불가**

#### 한줄 요약
- 상태기반 세션 추적과 L7 DPI 심층 검사를 통해 네트워크 경계의 비인가 접근을 실시간 차단한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Stateful Inspection (상태기반 검사)**: TCP 3-Way Handshake 세션 테이블을 유지하여 정상 수립된 세션의 반환 패킷을 고속 통과시키는 기술.
- **App-ID & User-ID**: 단순 포트 번호가 아닌 페이로드 시그니처와 Active Directory 사용자 계정을 매핑하여 정책을 집행하는 NGFW 핵심 기능.

</details>

- **기본 차단 원칙(Default Deny)**: 명시적으로 허용된 규칙 외의 **모든 비인가 인바운드/아웃바운드 트래픽을 원천 폐기(Drop)**
- **동적 상태 테이블 기반 고속 필터링**: 기 수립된 세션의 패킷은 **복잡한 룰셋 재평가 없이 상태 테이블로 초고속 통과**
- **L7 애플리케이션 및 사용자 인식(NGFW)**: 포트 번호 변조와 무관하게 **실제 앱(BitTorrent, Webex 등)을 식별하고 사용자별 ACL 집행**

#### 한줄 요약
- Default Deny 원칙, 동적 상태 테이블 기반 고속 통과, L7 App-ID/User-ID 제어를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SSL Forward Proxy (SSL Inspection)**: 방화벽이 프록시 인증서를 발급하여 암호화된 HTTPS 트래픽을 중간에서 복호화해 악성코드를 검사하는 엔진.

</details>

```text
[방화벽 내부 패킷 처리 파이프라인 및 망 분리]
|-- Ingress Network Packet (외부 비신뢰 인터넷 트래픽 유입)
`-- Firewall Core Engine
    |-- 1. 5-Tuple Parser (L3/L4 헤더 고속 파싱: IP, Port, Protocol)
    |-- 2. State Table Lookup (기존 ESTABLISHED 세션 즉시 통과)
    |-- 3. Top-Down Policy Rule Engine (신규 세션: ACL 순차 매칭 / Default Deny)
    |-- 4. SSL Decryption Proxy (HTTPS 암호화 해제)
    `-- 5. L7 DPI & App-ID Engine (실제 응용 식별: C2 통신 차단)
`-- Zone Forwarding (DMZ 웹 서버 / Trust LAN 내부 업무망)
```

선의 의미: 인입된 패킷이 5-Tuple 추출, 상태 테이블 대조, 정책 룰셋 평가, SSL 복호화 및 L7 DPI 검사를 거쳐 DMZ 또는 내부망으로 선별 포워딩되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **5-Tuple 파서** | L3/L4 헤더를 고속 추출하여 **1차 정적 규칙 일치 여부 검사** | L3/L4 Filter |
| **세션 상태 테이블** | 기 수립된 세션의 **TCP Sequence 번호와 상태를 추적하여 스푸핑 차단** | State Table |
| **정책 룰셋 엔진** | 관리자가 구성한 ACL 규칙을 **최상단부터 순차(Top-Down) 평가 집행** | Policy Engine |
| **SSL 복호화 엔진** | 프록시 인증서를 사용하여 **HTTPS 트래픽을 실시간 복호화 검사** | SSL Inspection |
| **L7 DPI / App-ID** | 페이로드 시그니처를 분석하여 **실제 응용 프로그램 식별 및 차단** | App-ID Engine |

#### 한줄 요약
- 5-Tuple 파서, 세션 상태 테이블, 정책 룰셋 엔진, SSL 복호화기, L7 DPI App-ID 엔진이 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Top-Down First-Match**: 최상단 1번 규칙부터 순차 평가하여 최초로 일치하는 규칙의 액션을 즉시 실행하고 평가를 종료하는 원칙.

</details>

```text
패킷 인입, 상태 테이블 대조, Top-Down 룰 매칭, L7 DPI 및 포워딩 파이프라인
        │
   1. [5-Tuple 파싱] 신규 패킷 인입 시 L3/L4 헤더(출발지/목적지 IP, 포트, 프로토콜) 추출
        │
   2. [상태 테이블 대조] State Table 조회 ➔ [기존 ESTABLISHED 세션 일치 시] ➔ 4단계로 즉시 이동
        │
   ├─ [일치 세션 없음: 신규 세션 요청(TCP SYN)]
   ▼
3. [Top-Down 정책 평가] ACL 룰셋을 최상단부터 순차 평가 ➔ [일치 시] Allow 및 상태 테이블 등록
        │     └─ [일치 규칙 없음: Default Deny] ➔ 패킷 즉시 폐기(Drop) 및 감사 로그 기록
        ▼
4. [L7 DPI 및 SSL 검사] SSL 복호화 후 L7 DPI 및 IPS 시그니처 정밀 스캔 ➔ [악성 탐지 시] TCP RST 차단
        │
   ▼
5. [최종 포워딩] 모든 검사 통과 시 NAT 변환 및 라우팅을 거쳐 대상 인터페이스로 최종 전송
```

#### 한줄 요약
- 5-Tuple 추출 → 상태 테이블 대조 → Top-Down 룰 매칭 → SSL 복호화 및 L7 DPI 검사 → 최종 포워딩 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **1세대 패킷 필터링** vs **2세대 상태기반** vs **3세대 차세대 방화벽 (NGFW)**.

</details>

| 비교 항목 | 1세대 패킷 필터링 (Packet Filter) | 2세대 상태기반 방화벽 (Stateful) | 3세대 차세대 방화벽 (NGFW) |
|:---|:---|:---|:---|
| **검사 계층** | **L3 / L4 (네트워크 / 전송 계층)** | **L3 / L4 + 세션 상태 추적** | **L3 ~ L7 (애플리케이션 계층 전수 검사)**|
| **검사 기준** | **단순 5-Tuple (IP, Port, Protocol)** | **5-Tuple + TCP 세션 연결 상태** | **App-ID, User-ID, 콘텐츠(DPI), IPS 통합** |
| **처리 성능** | **초고속 (하드웨어 ASIC 기반)** | **빠름 (State Table 기반 고속 통과)** | 중간 (DPI 및 SSL 복호화로 연산 부하 큼) |
| **포트 우회 공격 방어**| **불가 (80 포트로 유입되는 악성코드 허용)**| 불가 (정상 TCP 핸드셰이크 시 통과) | **완벽 방어 (실제 앱 페이로드 식별 차단)** |
| **주요 적용 영역** | 백본 라우터 ACL, 대용량 트래픽 1차 정제 | **엔터프라이즈 레거시 경계 방화벽** | **현대 기업 경계망, 클라우드 DMZ, 데이터센터**|

#### 한줄 요약
- 1세대는 초고속 정적 필터링, 2세대는 세션 추적 표준, 3세대 NGFW는 L7 DPI 및 SSL 복호화 통합 보안이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Shadowed Rule (음영 규칙)**: 상위의 포괄적 허용 규칙(예: `ALLOW ANY`)으로 인해 하위 세부 차단 규칙이 무력화되는 정책 오류.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 상위 포괄 룰로 인해 하위 정책이 평가되지 않는 **음영 규칙(Shadowed Rule) 발생** | **자동화된 `방화벽 정책 감사 툴 도입 및 미사용/중복 룰 정기 정제`** | 정책 우회 경로 원천 제거 및 룰셋 평가 지연 단축 |
| DMZ 웹 서버 침해 후 내부 DB망으로 직결 침투하는 **단일 방화벽 붕괴 및 횡적 이동** | **외부-DMZ, DMZ-내부를 서로 다른 벤더로 이중 격리하는 `Double DMZ`** 구성 | 1차 방화벽 침해 시에도 2차 방화벽으로 내부 DB 보호 |
| 443(HTTPS) 암호화 트래픽 내부에 은닉된 **악성코드 및 C2 통신 가시성 부재** | **`NGFW 전용 SSL 복호화 가속 카드 탑재` 및 선택적 복호화 정책** 수립 | 암호화 트래픽 내 위협 100% 탐지 및 성능 병목 해소 |
| 방화벽 단일 장애(SPOF) 발생 시 전사 인터넷 접속 두절 | **`Active-Standby 또는 Active-Active 이중화(VRRP/HSRP)` 및 세션 동기화** | 장비 장애 시 1초 내 무중단 자동 절체(Failover) 보장 |

#### 한줄 요약
- 룰 감사로 음영 규칙을 제거하고, Double DMZ로 내부망을 보호하며, SSL Inspection으로 암호화 위협을 제거한다.

## Ⅶ. 결론

- 엔터프라이즈 네트워크 인프라의 가장 기본적인 1차 방어선인 **방화벽 및 차세대 방화벽(NGFW) 아키텍처는 제로 트러스트(Micro-Segmentation)로 진화하는 현대 보안의 핵심 기반**이며, 실무 구현 시 **엄격한 Default Deny 원칙 준수, Double DMZ 기반 계층형 망 분리, SSL 복호화 및 L7 App-ID 정책 고도화**를 통합 구축하여 무결점 경계 접근 통제 환경 완성

#### 한줄 요약
- 방화벽은 상태기반 세션 추적과 L7 App-ID/DPI 심층 검사 및 Default Deny 정책을 통해 고신뢰 경계 보안을 실현하는 핵심 시스템이다.