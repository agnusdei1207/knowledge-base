---
sidebar:
  order: 25
  label: "025. DDoS 공격•대응 - SYN Flood•반사 증폭"
  badge:
    text: "기출 · 30%"
    variant: note
title: "분산 서비스 거부 공격 유형 및 계층별 완화 : DDoS"
date: "2026-08-25T13:00:00+09:00"
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

- 정의/개념: 분산 봇넷을 통해 대역폭(L3/L4), 프로토콜 상태(L4), 웹 자원(L7)을 고갈시켜 **정상 서비스 가용성을 마비시키는 공격 및 Anycast 기반 계층별 완화 기술**
- 배경/필요성: 단일 로컬 방화벽의 회선 대역폭 초과 및 세션 메모리 한계로 인한 **Tbps급 대규모 공격 트래픽 수용 불가 및 서비스 전면 마비**

#### 한줄 요약
- Anycast 분산망과 L4 SYN Cookie 및 L7 WAF를 통해 대규모 분산 공격을 계층별로 완화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **DRDoS (Distributed Reflection DoS)**: 출발지 IP를 피해자 IP로 위조하여 DNS/NTP 서버로 질의를 보내 수십 배 증폭된 응답을 피해자에게 폭격하는 반사 공격.
- **SYN Cookie (RFC 4987)**: TCP 3-Way Handshake 시 서버 메모리에 세션 상태를 저장하지 않고 초기 시퀀스 번호에 암호화 인코딩하여 SYN Flooding을 무력화하는 기술.

</details>

- **공격 벡터의 다계층 복합화(Multi-Vector Attack)**: 회선 포화(UDP 반사), **세션 고갈(SYN Flood), 웹 자원 고갈(HTTP Flood)의 동시 다발적 결합**
- **비대칭 증폭 공격(Amplification Factor)**: DNS(50배), **NTP(550배), Memcached(50,000배) 증폭률을 악용하여 소량의 트래픽으로 대규모 공격 수행**
- **BGP Anycast 기반 글로벌 트래픽 분산**: 전 세계 수백 개 엣지 PoP으로 **공격 트래픽을 분할 유입시켜 단일 노드 과부하 방지**

#### 한줄 요약
- 다계층 복합 공격, 대규모 비대칭 증폭, BGP Anycast 기반 분산 완화를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Scrubbing Center (스크러빙 센터)**: 인터넷 상류에서 Tbps급 대규모 트래픽을 인라인 정제하여 정상 패킷만 원본 서버로 전달하는 클라우드 정제소.

</details>

```text
[DDoS 글로벌 분산 방어 및 스크러빙 아키텍처]
|-- Distributed Botnet (공격 트래픽 폭격)
`-- Global BGP Anycast Edge Network (Cloudflare / Akamai)
    |-- Anycast PoP Routing (글로벌 엣지로 트래픽 지리적 분산 유입)
    `-- Cloud Scrubbing Center
        |-- 1. L3/L4 Volumetric Filtering (uRPF, BCP 38, BGP Flowspec)
        |-- 2. L4 TCP State Protection (SYN Cookie / SYN Proxy 하드웨어 엔진)
        `-- 3. L7 WAF & Bot Mitigation (JS Challenge, CAPTCHA, Rate-Limiting)
`-- Clean Traffic Delivery (GRE 터널 / Direct Connect -> 원본 서버 Origin Server 전달)
```

선의 의미: 봇넷의 공격 트래픽이 글로벌 Anycast 엣지 및 스크러빙 센터로 분산 유입되어 계층별 필터링을 거친 후 정제된 정상 트래픽만 원본 서버로 전달되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **BGP Anycast 망** | 동일 글로벌 IP를 전 세계 PoP에 광고하여 **공격 트래픽을 지리적으로 분산 분할** | Anycast BGP |
| **스크러빙 센터** | Tbps급 공격 트래픽을 **인라인 정제하고 악성 패킷을 폐기하는 클라우드 정제소** | Scrubbing Center |
| **SYN 프록시/쿠키** | TCP 3-Way Handshake를 대신 종단하여 **서버 백로그 큐 고갈을 완벽 방어** | RFC 4987 |
| **L7 봇 완화 엔진**| 브라우저 핑거프린팅, **자바스크립트 챌린지, 요청 속도 제한(Rate Limiting)** | Bot Mitigation |
| **BGP Flowspec** | 중앙 제어기가 공격 트래픽 룰셋을 **ISP 상류 라우터로 신속 배포하여 차단** | RFC 5575 |

#### 한줄 요약
- BGP Anycast 분산망, 스크러빙 센터, SYN 프록시/쿠키, L7 봇 완화 엔진, BGP Flowspec이 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **BGP Anycast Swing (경로 전환)**: 대규모 DDoS 탐지 시 BGP 라우팅을 스크러빙 센터로 전환하여 인바운드 트래픽을 강제 우회 정제시키는 기법.

</details>

```text
DDoS 트래픽 탐지, Anycast 경로 전환 및 계층별 완화 파이프라인
        │
   1. [이상 트래픽 탐지] sFlow/NetFlow 센서가 Gbps/PPS 임계치 초과를 실시간 식별
        │
   2. [공격 유형 판별] L3/L4 대역폭 공격 vs L4 SYN Flood vs L7 HTTP GET Flood 판별
        │
   ├─ [L3/L4 대용량 공격 시] ➔ BGP Anycast 라우팅을 스크러빙 센터로 전환하여 반사 증폭 패킷 드롭
   │
   ├─ [L4 SYN Flood 시] ➔ 인라인 방어 장비의 SYN Cookie 메커니즘 활성화 (백로그 큐 보호)
   │
   ▼
3. [L7 HTTP 공격 시] ➔ WAF Rate Limiting 및 브라우저 JavaScript 챌린지 강제 집행 후 정상 트래픽 전달
```

#### 한줄 요약
- 이상 트래픽 탐지 → 공격 유형 판별 → BGP Anycast 우회 → L4/L7 계층별 완화 집행 → 클린 트래픽 전달 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **대역폭형 (Volumetric)** vs **프로토콜 상태형 (State Exhaustion)** vs **응용 계층형 (Application/L7)**.

</details>

| 비교 항목 | 대역폭형 공격 (Volumetric) | 프로토콜 상태형 공격 (State Exhaustion) | 응용 계층형 공격 (Application / L7) |
|:---|:---|:---|:---|
| **주요 공격 표적** | **네트워크 회선 대역폭 (인터넷 파이프)** | **방화벽/서버 세션 테이블 (State Memory)** | **웹/WAS/DB CPU, 메모리, 스레드 풀** |
| **핵심 공격 기법** | **UDP/ICMP Flood, DNS/NTP 반사 증폭** | **TCP SYN Flood, ACK Flood, RST Flood** | **HTTP GET/POST Flood, Slowloris, RUDY**|
| **공격 규모 척도** | **Gbps / Tbps (초당 데이터 전송량)** | **PPS / CPS (초당 패킷/연결 생성수)** | **RPS / QPS (초당 HTTP 요청/질의수)** |
| **탐지 난이도** | 쉬움 (트래픽 급증 즉시 식별) | 중간 (정상 TCP 플래그 위장) | **매우 높음 (정상 HTTP 트래픽과 구별 난해)**|
| **핵심 완화 대책** | **BGP Anycast 및 상류 스크러빙 센터** | **SYN Cookie, TCP SYN Proxy, 세션 타임아웃**| **WAF Rate Limiting, JS Challenge, CAPTCHA**|

#### 한줄 요약
- 대역폭형은 회선 Gbps 포화, 프로토콜형은 상태 테이블 PPS 고갈, 응용형은 웹/DB RPS 연산 고갈을 노린다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Slowloris Attack**: HTTP 요청 헤더를 비정상적으로 느리게 전송하여 웹 서버의 동시 연결 스레드 풀을 고갈시키는 L7 저속 자원 고갈 공격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 수백 Gbps 반사 증폭 공격으로 인한 **온프레미스 인터넷 인입 회선 대역폭 완전 포화** | **클라우드 기반 `글로벌 BGP Anycast 스크러빙 센터 연동 및 BGP Flowspec 상류 차단`** | 원본 회선 대역폭 포화 차단 및 대용량 트래픽 100% 흡수 |
| 대규모 TCP SYN Flood로 인한 **방화벽 세션 테이블 및 서버 SYN 백로그 큐 고갈** | **OS 커널 `SYN Cookie(tcp_syncookies=1) 활성화` 및 인라인 SYN Proxy 배치** | 세션 사전 할당 오버헤드 제거로 정상 연결 100% 유지 |
| Slowloris 및 HTTP GET Flood로 인한 **웹 서버 스레드 고갈 및 CPU 100% 과부하** | **리버스 프록시 요청 타임아웃 단축, `WAF Rate-Limiting 및 JS Challenge`** | 느린 연결 강제 종료 및 매크로 봇 격리로 가용성 보존 |
| 정상 트래픽까지 일괄 차단하는 과도한 DDoS 방어로 인한 서비스 오작동 | **행동 기반 `AI 봇 탐지 및 IP 평판(Reputation) 데이터베이스` 결합** | 정상 고객 오차단 최소화 및 비즈니스 연속성 확보 |

#### 한줄 요약
- 스크러빙으로 대역폭을 보호하고, SYN Cookie로 백로그를 방어하며, WAF/타임아웃으로 L7 고갈을 차단한다.

## Ⅶ. 결론

- 공격 기술의 고도화와 IoT 봇넷의 확산으로 인해 일상화된 **DDoS 공격 대응 아키텍처는 단일 장비의 차단 한계를 넘어 글로벌 인프라 기반의 계층형 완화 체계를 요구**하며, 실무 구현 시 **BGP Anycast 기반 글로벌 스크러빙 센터 확보, L4 커널 레벨 SYN Cookie 적용, L7 WAF 및 행동 기반 봇 완화 파이프라인**을 상호 연계 구축하여 99.99% 이상의 서비스 가용성을 보장하는 다계층 DDoS 방어 환경 완성

#### 한줄 요약
- DDoS 대응은 BGP Anycast 스크러빙, L4 SYN Cookie, L7 WAF 봇 완화를 결합하여 테라비트급 복합 공격을 완벽히 방어해야 한다.