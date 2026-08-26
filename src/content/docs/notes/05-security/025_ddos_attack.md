---
sidebar:
  order: 25
  label: "025. DDoS 공격•대응 - SYN Flood•반사 증폭"
  badge:
    text: "기출 · 30%"
    variant: note
title: "분산 서비스 거부 공격 유형 및 계층별 완화 : DDoS"
date: "2026-08-26T14:29:42+09:00"
tags:
  - "notes-security"
weight: 25
extra:
  question_no: "25"
  source_status: "기출"
  source_history: "125회"
  priority: 30
  priority_note: "대역폭형(DRDoS/반사증폭), 프로토콜형(TCP SYN Flood/SYN Cookie), 응용형(HTTP Flood/Slowloris), Anycast 및 BGP 스크러빙 센터"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **DDoS (Distributed Denial of Service)**: 다수의 좀비 봇넷을 조종하여 대역폭과 자원을 고갈시켜 서비스 가용성을 마비시키는 공격.
- **Botnet (봇넷)**: C2 서버의 명령을 받아 악성 트래픽을 일제히 송출하는 감염된 단말/IoT 군단.

</details>

- 정의/개념: 분산 봇넷으로 자원을 고갈시키는 **서비스 거부 공격**
- 배경/필요성: 로컬 방화벽은 **Tbps 공격 회선 포화 방어 불가**

#### 한줄 요약
- Anycast 분산망과 L4 SYN Cookie 및 L7 WAF를 통해 대규모 분산 공격을 계층별로 완화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **DRDoS (Distributed Reflection DoS)**: 출발지 IP를 피해자 IP로 위조하여 DNS/NTP 서버로 질의를 보내 수십 배 증폭된 응답을 피해자에게 폭격하는 반사 공격.
- **SYN Cookie (RFC 4987)**: TCP 3-Way Handshake 시 서버 메모리에 세션 상태를 저장하지 않고 초기 시퀀스 번호에 암호화 인코딩하여 SYN Flooding을 무력화하는 기술.

</details>

- **다계층 복합 공격**: 회선·세션·**웹 자원 동시 고갈**
- **반사 증폭**: DNS·NTP·Memcached의 **증폭률 악용**
- **BGP Anycast 분산**: 공격을 여러 **엣지 PoP**으로 분산

#### 한줄 요약
- 다계층 복합 공격, 대규모 비대칭 증폭, BGP Anycast 기반 분산 완화를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Scrubbing Center (스크러빙 센터)**: 인터넷 상류에서 Tbps급 대규모 트래픽을 인라인 정제하여 정상 패킷만 원본 서버로 전달하는 클라우드 정제소.

</details>

```text
[DDoS 방어 체계]
|-- Anycast 망       : 공격 트래픽 분산
|-- 스크러빙 센터    : 대역폭 공격 정제
|-- SYN 방어기       : 세션 상태 보호
|-- L7 봇 완화기     : 요청 속도·봇 통제
`-- BGP Flowspec     : 상류 차단 규칙 배포
```

선의 의미: 봇넷의 공격 트래픽이 글로벌 Anycast 엣지 및 스크러빙 센터로 분산 유입되어 계층별 필터링을 거친 후 정제된 정상 트래픽만 원본 서버로 전달되는 구조

| 구성요소 | 책임 |
|:---|:---|
| Anycast 망 | 공격 트래픽의 **지리적 분산** |
| 스크러빙 센터 | Tbps 트래픽 **정제·폐기** |
| SYN 방어기 | **SYN Cookie·Proxy**로 상태 보호 |
| L7 봇 완화기 | **Rate Limit·JS Challenge** 적용 |
| BGP Flowspec | ISP 상류에 **차단 규칙 배포** |

#### 한줄 요약
- BGP Anycast 분산망, 스크러빙 센터, SYN 프록시/쿠키, L7 봇 완화 엔진, BGP Flowspec이 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **BGP Anycast Swing (경로 전환)**: 대규모 DDoS 탐지 시 BGP 라우팅을 스크러빙 센터로 전환하여 인바운드 트래픽을 강제 우회 정제시키는 기법.

</details>

```text
트래픽 이상
      |
  1. 공격 유형 판별
      +-- 대역폭형: 스크러빙·Flowspec
      +-- 상태형  : SYN Cookie·Proxy
      `-- 응용형  : WAF·봇 완화
                         |
                    정상 트래픽 전달
```

동작 원리

1. 공격 유형 판별

#### 한줄 요약
- 이상 트래픽 탐지 → 공격 유형 판별 → BGP Anycast 우회 → L4/L7 계층별 완화 집행 → 클린 트래픽 전달 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **대역폭형 (Volumetric)** vs **프로토콜 상태형 (State Exhaustion)** vs **응용 계층형 (Application/L7)**.

</details>

| 비교 항목 | 대역폭형 공격 (Volumetric) | 프로토콜 상태형 공격 (State Exhaustion) | 응용 계층형 공격 (Application / L7) |
|:---|:---|:---|:---|
| 주요 공격 표적 | 회선 대역폭 | 세션 테이블 | 웹·WAS·DB 자원 |
| 핵심 공격 기법 | **UDP·반사 증폭** | **SYN·ACK Flood** | **HTTP Flood·Slowloris** |
| 공격 규모 척도 | Gbps·Tbps | PPS·CPS | RPS·QPS |
| 탐지 난이도 | 낮음 | 중간 | 정상 요청과 유사해 높음 |
| 핵심 완화 대책 | **Anycast·스크러빙** | **SYN Cookie·Proxy** | **WAF·Rate Limit** |

#### 한줄 요약
- 대역폭형은 회선 Gbps 포화, 프로토콜형은 상태 테이블 PPS 고갈, 응용형은 웹/DB RPS 연산 고갈을 노린다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Slowloris Attack**: HTTP 요청 헤더를 비정상적으로 느리게 전송하여 웹 서버의 동시 연결 스레드 풀을 고갈시키는 L7 저속 자원 고갈 공격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 반사 공격으로 **회선 포화** | **Anycast·스크러빙·Flowspec** | 원본 회선 보호 |
| SYN Flood로 **상태 큐 고갈** | **SYN Cookie·Proxy** | 정상 연결 유지 |
| HTTP Flood로 **서버 자원 고갈** | **WAF·Rate Limit·타임아웃** | 봇 격리와 가용성 확보 |
| 과도한 방어로 **정상 요청 차단** | **행동 분석·IP 평판** 결합 | 오차단 최소화 |

#### 한줄 요약
- 스크러빙으로 대역폭을 보호하고, SYN Cookie로 백로그를 방어하며, WAF/타임아웃으로 L7 고갈을 차단한다.

## Ⅶ. 결론

- 회선 공격은 **스크러빙**, 상태 공격은 **SYN Cookie**, L7은 WAF

#### 한줄 요약
- DDoS 대응은 BGP Anycast 스크러빙, L4 SYN Cookie, L7 WAF 봇 완화를 결합하여 테라비트급 복합 공격을 완벽히 방어해야 한다.
