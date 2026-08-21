---
sidebar:
  order: 25
  label: "025. DDoS 공격•대응 - SYN Flood•반사 증폭 (DDoS Attack)"
  badge:
    text: "기출 · 30%"
    variant: note
title: "분산 서비스 거부 공격 유형 및 계층별 완화 : DDoS (Distributed Denial of Service)"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-security"
weight: 25
extra:
  question_no: "025"
  source_status: "기출"
  source_history: "125회"
  priority: 30
  priority_note: "대역폭형(DRDoS/반사증폭), 프로토콜형(TCP SYN Flood/SYN Cookie), 응용형(HTTP Flood/Slowloris), Anycast 및 BGP 스크러빙 센터"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **DDoS(분산 서비스 거부 공격 / Distributed Denial of Service)**: 악성코드에 감염된 다수의 분산 좀비 단말 군단(Botnet)을 원격 조종하여 표적 서버, 네트워크 장비, 대역폭 자원에 동시 다발적인 대규모 트래픽을 집중 투하함으로써, 정상 사용자의 서비스 접근 및 가용성(Availability)을 완전히 마비시키는 사이버 공격.
- **봇넷(Botnet)**: 명령제어(C2) 서버의 지령을 받아 일제히 악성 패킷을 생성 및 발송하는 감염된 PC, 서버, IoT(공유기, IP 카메라) 기기들의 집합체.

</details>

- 정의/개념: 고갈 대상 자원에 따라 **대역폭 고갈(Volumetric / DRDoS)**, **프로토콜 상태 고갈(Stateful / SYN Flood)**, **애플리케이션 자원 고갈(L7 / HTTP GET/POST Flood)** 로 분류되며, BGP Anycast 및 스크러빙 센터를 통해 트래픽을 분산 정제하는 **DDoS 방어 및 완화 아키텍처**
- 배경/필요성: 단일 기업의 온프레미스 회선 용량(수 Gbps)을 수십~수백 배 초과하는 테라비트(Tbps)급 대규모 공격과, 소량의 트래픽으로 CPU를 100% 고갈시키는 저대역폭 애플리케이션 공격의 복합화에 대응할 요구

#### 한줄 요약
- 봇넷 트래픽의 자원 고갈 메커니즘을 식별하고 BGP Anycast 스크러빙 및 L4/L7 계층별 완화로 가용성을 방어한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **반사 증폭 공격(DRDoS / Distributed Reflection Denial of Service)**: 공격자가 출발지 IP를 피해자 IP로 변조(IP Spoofing)한 후 증폭 계수가 높은 비연결형 UDP 공개 서버(DNS, NTP, Memcached)로 질의를 전송하여, 요청 크기 대비 수십~수만 배로 증폭된 응답 트래픽이 피해자 서버로 집중 반사되도록 유도하는 공격.
- **SYN 쿠키(SYN Cookie / RFC 4987)**: TCP 3-Way Handshake 시 서버가 메모리(SYN Backlog Queue)에 연결 상태를 사전 할당하지 않고, 초기 시퀀스 번호(ISN) 내에 세션 암호화 해시값을 인코딩하여 반환함으로써 SYN Flood 공격에 의한 메모리 고갈을 방어하는 기법.

</details>

- **3계층 공격 벡터 분류**: 대역폭 포화(L3/L4 Gbps/Tbps), 세션 장부 포화(L4 CPS/PPS), 시스템 CPU/메모리 연산 고갈(L7 RPS)
- **비대칭 비용 공격**: 소량의 요청 패킷으로 피해자 측에 극단적인 대역폭 유입(DRDoS) 또는 복잡한 데이터베이스 조인 연산(L7 Slowloris/HTTP Flood) 유발
- **클라우드 글로벌 Anycast 완화 의존성**: 온프레미스 장비 용량을 초과하는 공격 트래픽은 글로벌 분산 BGP Anycast 망을 통해 지리적으로 흡수 정제 필수

#### 한줄 요약
- 3계층 공격 벡터 분류, 비대칭 증폭/연산 고갈, BGP Anycast 및 스크러빙 센터 기반 흡수를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **스크러빙 센터(Scrubbing Center)**: 글로벌 ISP 상류(Upstream) 또는 클라우드 DDoS 방어 전문 센터에 위치하여, BGP 라우팅 공표(BGP Hijacking/Diversion)를 통해 유입 트래픽을 가로챈 후 악성 트래픽을 여과(Filtering)하고 정상 트래픽만 GRE 터널을 통해 원본 서버(Origin)로 전달하는 대용량 트래픽 정제 인프라.

</details>

```text
[ 분산 봇넷 (Mirai Botnet) & 반사 증폭 서버 (DNS/NTP) ]
                      │ (Tbps 단위의 초대용량 공격 트래픽 발송)
                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 글로벌 BGP Anycast 분산 에지 네트워크 (Cloudflare / Akamai) ]          │
│  ├─ 전 세계 수백 개 에지 PoP으로 공격 트래픽 지리적 분산 유입           │
│  │                                                                      │
│  └─ [ 스크러빙 센터 (Scrubbing Center) ]                                │
│       ├─ 1. L3/L4 볼류메트릭 필터링 (uRPF, BCP 38, BGP Flowspec)         │
│       ├─ 2. L4 TCP 상태 보호 (SYN Proxy / SYN Cookie 하드웨어 엔진)     │
│       └─ 3. L7 WAF & 봇 완화 (JS Challenge, CAPTCHA, Rate-Limiting)     │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (정제 완료된 정상 클린 트래픽만 전송)
                                     ▼ (GRE 터널 / 전용선 Direct Connect)
[ 온프레미스 기업 데이터센터 원본 서버 (Origin Server) ]
```

선의 의미: 봇넷의 공격 트래픽이 글로벌 Anycast 에지 및 스크러빙 센터로 분산 유입되어 계층별 필터링을 거친 후, 정제된 정상 트래픽만 원본 서버로 전달되는 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **BGP Anycast 망** | 동일한 글로벌 IP를 전 세계 수백 개 PoP에 광고하여 공격 트래픽을 지리적으로 분산 분할 | Anycast BGP |
| **스크러빙 센터** | Tbps급 공격 트래픽을 인라인 정제하고 악성 패킷을 폐기하는 클라우드 정제소 | Scrubbing |
| **SYN 프록시/쿠키** | 불완전한 TCP 3-Way Handshake를 대신 종단하여 서버 백로그 큐 고갈을 완벽 방어 | RFC 4987 |
| **L7 봇 완화 엔진 (WAF)**| 브라우저 핑거프린팅, 자바스크립트 챌린지, 요청 속도 제한(Rate Limiting) 수행 | Bot Mitigation |
| **BGP Flowspec (RFC 5575)**| 중앙 제어기가 공격 트래픽 룰셋을 ISP 상류 라우터로 신속 배포하여 상류 차단 | Flowspec |

#### 한줄 요약
- BGP Anycast 분산망, 스크러빙 센터, SYN 프록시/쿠키, L7 봇 완화 엔진, BGP Flowspec이 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **BGP 라우팅 전환(BGP Diversion / Anycast Swing)**: 평상시에는 로컬 ISP로 트래픽을 직접 수신하다가, 대규모 DDoS 공격 탐지 시 BGP 라우팅 경로를 글로벌 스크러빙 센터로 즉시 전환하여 모든 인바운드 트래픽을 강제 우회 정제시키는 운영 기법.

</details>

```text
1. 네트워크 센서(NetFlow/sFlow)가 비정상적인 트래픽 폭증(Gbps/PPS 임계치 초과) 실시간 탐지
            │
            ▼
2. [공격 유형 식별]: L3/L4 대역폭 공격 vs L4 SYN Flood vs L7 HTTP GET Flood 판별
            │
            ├─ [L3/L4 대용량 공격 시] ➔ BGP 라우팅을 스크러빙 센터로 전환 (Anycast Diversion)
            │     │
            │     ▼
            │   상류 스크러빙 센터에서 NTP/DNS 반사 증폭 패킷 드롭 및 정상 트래픽만 GRE로 원본 전달
            │
            ├─ [L4 SYN Flood 시] ➔ 인라인 방어 장비의 SYN Cookie 메커니즘 즉각 활성화 (백로그 큐 보호)
            │
            └─ [L7 HTTP/API 공격 시] ➔ WAF Rate Limiting 및 브라우저 JavaScript 챌린지 강제 집행
```

**동작 원리**

1. **실시간 트래픽 텔레메트리**: sFlow/IPFIX를 분석하여 프로토콜 분포 및 이상 엔트로피 계산
2. **트래픽 동적 우회**: BGP Anycast 경로 전환을 통해 대규모 공격을 클라우드 방어선으로 유도
3. **L3 반사 패킷 폐기**: 출발지 포트(123/NTP, 53/DNS, 11211/Memcached) 기반 ACL 차단
4. **L4 세션 연결 검증**: 정상 3-Way Handshake를 완료한 클라이언트의 세션만 백엔드 전달
5. **L7 유효 사용자 식별**: 헤드리스 브라우저 및 매크로 봇을 스크립트 실행 검증으로 즉시 격리

#### 한줄 요약
- 이상 트래픽 탐지, 공격 유형 판별, BGP Anycast 우회, L4/L7 계층별 완화 집행, 클린 트래픽 전달 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **DDoS 3대 공격 유형 비교**: 대역폭형(Volumetric), 프로토콜 상태형(State Exhaustion), 응용 계층형(Application Layer)의 비교.

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

- **슬로로리스(Slowloris) 공격**: HTTP 요청 헤더의 끝을 알리는 빈 줄(`\r\n\r\n`)을 전송하지 않고, 극도로 느린 속도로 불완전한 헤더를 주기적으로 쪼개어 전송함으로써 웹 서버의 동시 연결 스레드 풀(Thread Pool)을 장시간 점유하여 고갈시키는 L7 저속 자원 고갈 공격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 수백 Gbps 규모의 DNS/NTP 반사 증폭 공격으로 인한 **온프레미스 인터넷 인입 회선 대역폭 완전 포화** | **클라우드 기반 글로벌 BGP Anycast 스크러빙 센터 연동 및 BGP Flowspec 상류 차단** | 원본 회선 대역폭 포화 0% 차단 및 글로벌 에지 기반 대용량 트래픽 100% 흡수 |
| 대규모 TCP SYN Flood 공격으로 인한 **방화벽 세션 테이블 및 서버 SYN 백로그 큐 고갈 장애** | **OS 커널 레벨 SYN Cookie(`tcp_syncookies=1`) 활성화 및 인라인 SYN Proxy 장비 배치** | 세션 상태 사전 할당 오버헤드 제거로 수천만 PPS 공격 환경에서도 정상 연결 유지 |
| Slowloris 및 HTTP GET Flood로 인한 **웹 애플리케이션 서버 스레드 고갈 및 CPU 100% 과부하** | **리버스 프록시(Nginx/Envoy) 요청 타임아웃 단축, WAF Rate-Limiting 및 JS Challenge** | 느린 연결 강제 종료 및 매크로 봇 요청 완벽 격리로 웹 서버 가용성 100% 보존 |

#### 한줄 요약
- 스크러빙으로 대역폭을 보호하고, SYN Cookie로 백로그를 방어하며, WAF/타임아웃으로 L7 고갈을 차단한다.

## Ⅶ. 결론

- 공격 기술의 고도화와 IoT 봇넷의 확산으로 인해 일상화된 **DDoS 공격 대응 아키텍처**는 단일 장비의 차단 한계를 넘어 글로벌 인프라 기반의 계층형 완화 체계를 요구하며, 실무 구현 시 **BGP Anycast 기반 글로벌 스크러빙 센터 확보**, **L4 커널 레벨 SYN Cookie 적용**, **L7 WAF 및 행동 기반 봇 완화 파이프라인**을 상호 연계 구축하여 99.99% 이상의 서비스 가용성을 보장하는 다계층 DDoS 방어 환경을 완성

#### 한줄 요약
- BGP Anycast 스크러빙, L4 SYN Cookie, L7 WAF 봇 완화를 결합하여 테라비트급 복합 DDoS 위협을 완벽히 방어한다.
