---
sidebar:
  order: 21
  label: "021. 방화벽 - 패킷 필터•상태기반•NGFW"
  badge:
    text: "기출 · 70%"
    variant: note
title: "네트워크 경계 접근 통제 기술 : 방화벽 및 차세대 방화벽"
date: "2026-08-26T14:24:15+09:00"
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

- 정의/개념: 정책에 따라 트래픽을 선별하는 **경계 접근 통제 기술**
- 배경/필요성: 포트 필터만으로는 **L7·암호화 위협 식별 불가**

#### 한줄 요약
- 상태기반 세션 추적과 L7 DPI 심층 검사를 통해 네트워크 경계의 비인가 접근을 실시간 차단한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Stateful Inspection (상태기반 검사)**: TCP 3-Way Handshake 세션 테이블을 유지하여 정상 수립된 세션의 반환 패킷을 고속 통과시키는 기술.
- **App-ID & User-ID**: 단순 포트 번호가 아닌 페이로드 시그니처와 Active Directory 사용자 계정을 매핑하여 정책을 집행하는 NGFW 핵심 기능.

</details>

- **Default Deny**: 명시적 허용 외 **비인가 트래픽 차단**
- **상태기반 검사**: 기존 세션은 **상태 테이블**로 판정
- **NGFW**: **App-ID·User-ID·DPI** 기반 L7 통제

#### 한줄 요약
- Default Deny 원칙, 동적 상태 테이블 기반 고속 통과, L7 App-ID/User-ID 제어를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SSL Forward Proxy (SSL Inspection)**: 방화벽이 프록시 인증서를 발급하여 암호화된 HTTPS 트래픽을 중간에서 복호화해 악성코드를 검사하는 엔진.

</details>

```text
[방화벽 처리 체계]
|-- 5-Tuple 파서     : L3/L4 헤더 추출
|-- 상태 테이블      : 세션 상태 추적
|-- 정책 엔진        : ACL·기본 차단 집행
|-- TLS 복호화기     : 암호화 가시성 확보
`-- L7 검사기        : DPI·App-ID 식별
```

선의 의미: 인입된 패킷이 5-Tuple 추출, 상태 테이블 대조, 정책 룰셋 평가, SSL 복호화 및 L7 DPI 검사를 거쳐 DMZ 또는 내부망으로 선별 포워딩되는 구조

| 구성요소 | 책임 |
|:---|:---|
| 5-Tuple 파서 | IP·포트·프로토콜 **헤더 추출** |
| 상태 테이블 | TCP 상태 추적과 **스푸핑 차단** |
| 정책 엔진 | **Top-Down ACL·Default Deny** 집행 |
| TLS 복호화기 | HTTPS **복호화 검사** |
| L7 검사기 | **DPI·App-ID** 기반 애플리케이션 통제 |

#### 한줄 요약
- 5-Tuple 파서, 세션 상태 테이블, 정책 룰셋 엔진, SSL 복호화기, L7 DPI App-ID 엔진이 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Top-Down First-Match**: 최상단 1번 규칙부터 순차 평가하여 최초로 일치하는 규칙의 액션을 즉시 실행하고 평가를 종료하는 원칙.

</details>

```text
외부 패킷
    |
 1. 5-Tuple 파싱
    |
 2. 상태 테이블 대조
    +-- 신규: 3. Top-Down 정책 평가
    |              `-- 불일치: 차단·기록
    `-- 기존 세션
           |
      4. TLS·L7 검사
           |
        내부·DMZ 전달
```

동작 원리

1. 5-Tuple 파싱
2. 상태 테이블 대조
3. Top-Down 정책 평가
4. TLS·L7 검사

#### 한줄 요약
- 5-Tuple 추출 → 상태 테이블 대조 → Top-Down 룰 매칭 → SSL 복호화 및 L7 DPI 검사 → 최종 포워딩 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **1세대 패킷 필터링** vs **2세대 상태기반** vs **3세대 차세대 방화벽 (NGFW)**.

</details>

| 비교 항목 | 1세대 패킷 필터링 (Packet Filter) | 2세대 상태기반 방화벽 (Stateful) | 3세대 차세대 방화벽 (NGFW) |
|:---|:---|:---|:---|
| 검사 계층 | **L3/L4** | L3/L4와 **세션 상태** | **L3~L7** |
| 검사 기준 | **5-Tuple** | 5-Tuple·TCP 상태 | **App-ID·User-ID·DPI** |
| 처리 성능 | 높음 | 높음 | 복호화·DPI로 중간 |
| 포트 우회 방어 | 불가 | 불가 | **애플리케이션 식별** |
| 주요 적용 영역 | 백본 ACL | 경계 방화벽 | 기업 경계·클라우드 DMZ |

#### 한줄 요약
- 1세대는 초고속 정적 필터링, 2세대는 세션 추적 표준, 3세대 NGFW는 L7 DPI 및 SSL 복호화 통합 보안이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Shadowed Rule (음영 규칙)**: 상위의 포괄적 허용 규칙(예: `ALLOW ANY`)으로 인해 하위 세부 차단 규칙이 무력화되는 정책 오류.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 상위 포괄 규칙으로 **음영 규칙 발생** | **정책 감사·중복 규칙 정제** | 우회 경로와 평가 지연 제거 |
| DMZ 침해 후 **내부망 횡적 이동** | **Double DMZ 이중 격리** | 내부 DB 보호 |
| HTTPS 내부 **위협 가시성 부재** | **TLS 복호화 가속·선별 정책** | 암호화 위협 탐지와 부하 완화 |
| 단일 장애로 **인터넷 접속 중단** | **이중화·세션 동기화** | 무중단 절체 보장 |

#### 한줄 요약
- 룰 감사로 음영 규칙을 제거하고, Double DMZ로 내부망을 보호하며, SSL Inspection으로 암호화 위협을 제거한다.

## Ⅶ. 결론

- 고속 1차 통제는 **상태기반**, L7·암호화 위협은 **NGFW** 선택

#### 한줄 요약
- 방화벽은 상태기반 세션 추적과 L7 App-ID/DPI 심층 검사 및 Default Deny 정책을 통해 고신뢰 경계 보안을 실현하는 핵심 시스템이다.
