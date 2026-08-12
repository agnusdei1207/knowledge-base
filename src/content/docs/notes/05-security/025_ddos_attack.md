---
sidebar:
  order: 25
  label: "025. DDoS 공격•대응 - SYN Flood•반사 증폭 (DDoS Attack)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "DDoS 공격•대응 - SYN Flood•반사 증폭 (DDoS Attack)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-security"
weight: 25
extra:
  question_no: "025"
  source_status: "기출"
  source_history: "125회"
  priority: 30
  priority_note: "125회 기출이나 공격유형 단독 반복은 상대적으로 낮음"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **분산 서비스 거부(Distributed Denial of Service, DDoS)**: 감염된 다수의 봇넷 및 외부 서버를 동원하여 타깃 시스템의 대역폭, 세션 테이블, 애플리케이션 자원을 고갈시켜 정상 서비스를 불능으로 만드는 공격.
- **봇넷(Botnet)**: 악성코드(Mirai 등)에 감염되어 공격자의 C2(Command and Control) 서버 명령에 따라 일제히 둔갑 공격을 수행하는 단말 집단.

</details>

- 정의/개념: 감염된 봇넷(Botnet) 및 반사 서버들을 동원하여 대역폭, TCP 세션 연결 테이블 또는 L7 응용 자원을 의도적으로 고갈시켜 서비스 불능 상태로 만드는 **DDoS 공격** 및 대응 기법
- 배경/필요성: 단일 시스템 방화벽 처리 한계를 넘어서는 대규모 대역폭(Terabit급) 포화 및 정교한 L7 애플리케이션 고비용 질의 공격 증가

#### 한줄 요약

- 대규모 봇넷 및 반사 서버를 동원하여 네트워크 대역폭, L4 TCP 세션 및 L7 응용 자원을 고갈시키는 공격

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **반사 증폭(Reflective Amplification)**: DNS, NTP, Memcached 등 공개 UDP 서버로 출발지 IP를 피해자 주소로 위조하여 유발한 대용량 반사 응답(기존 대비 10~500배)으로 대역폭을 포화시키는 기법.
- **4계층(Layer 4, L4)**: TCP/UDP 프로토콜 계층으로 SYN Flood, ACK Flood 등 세션 연결 자원을 타깃하는 영역.
- **7계층(Layer 7, L7)**: HTTP/HTTPS 및 API 응용 계층으로 HTTP GET/POST Flood, Slowloris 등 서버 CPU/DB 연산 자원을 고갈시키는 영역.
- **대역폭형 공격(Volumetric Attack)**: UDP/ICMP 패킷 및 반사 증폭을 이용하여 회선 용량(Gbps/Tbps)을 완전 포화시키는 공격.
- **프로토콜형 공격(Protocol Attack)**: TCP SYN, FIN, RST 패킷으로 방화벽/서버의 세션 테이블(State Table) 및 백로그 큐를 소진시키는 공격.
- **응용형 공격(Application Attack)**: 정상적인 HTTP 요청 형태로 가장하여 DB 쿼리나 고비용 로직을 반복 유도함으로써 CPU 자원을 소진시키는 공격.

</details>

- **대역폭형 공격**은 대규모 **봇넷**과 UDP **반사 증폭** 기법을 결합하여 상류 백본 회선 포화
- **프로토콜형 공격**은 위조된 SYN 패킷으로 **L4** TCP 백로그 큐(SYN Flood) 소진
- **응용형 공격**은 정상 요청을 가장하여 **L7** 고비용 DB 검색 및 복호화 연산 자원 즉시 고갈

#### 한줄 요약

- L4 대역폭 포화, TCP 연결 상태표 고갈(SYN Flood) 및 L7 HTTP/API 고비용 자원 소진의 공격 유형별 분화

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **스크러빙(Scrubbing Center)**: 대규모 DDoS 공격 발생 시 BGP 딜레이/DNS 변경을 통해 트래픽을 정제 센터로 우회(Bypass)시켜 유해 트래픽을 드롭하고 정상 패킷만 원본으로 회환하는 처리.
- **애니캐스트(Anycast BGP Routing)**: 동일한 IP 주소를 전 세계 여러 PoP(Point of Presence) 노드에 동시 배포하여 DDoS 트래픽을 근거리로 분산 흡수하는 라우팅 기법.
- **CDN(Content Delivery Network)**: 에지(Edge) 서버망을 통해 정적/동적 웹 콘텐츠 처리 부담을 분산하고 L7 공격을 1차적으로 흡수하는 분산 인프라.
- **WAF(Web Application Firewall)**: L7 HTTP/HTTPS 요청 페이로드, 요청 비율(Rate Limiting) 및 자바스크립트 챌린지를 심사하는 보안 장비.

</details>

`	ext
DDoS 방어 구조
├─ 봇넷•반사원
├─ 상류 스크러빙
├─ CDN•애니캐스트
├─ WAF•연결 보호
└─ 원본 서비스
`

가지의 의미: 공격자 트래픽 발생원, ISP 상류 대역폭 정제, CDN 분산 흡수, L7 웹 애플리케이션 방어 및 원본 보호 책임을 분리한 구조

| 구성요소 | 책임 |
|:---|:---|
| 봇넷•반사원 | C2 제어 기반 봇 단말 및 Open Reflector 서버를 통한 분산 공격 트래픽 발송 |
| 상류 스크러빙 | ISP 상류 구간에서 대용량 대역폭 공격(Volumetric) 정제 및 우회/회환 처리 |
| CDN•애니캐스트 | Anycast BGP 분산 라우팅 및 CDN 에지망 기반 공격 트래픽 다원 흡수 |
| WAF•연결 보호 | SYN Cookie 기반 L4 세션 보호 및 L7 Rate Limiting / JS Challenge 수행 |
| 원본 서비스 | 정제 과정을 통과한 정당 고객 트래픽의 최종 업무 연산 처리 |


#### 한줄 요약

- 봇넷/반사원, 상류 스크러빙 센터(Scrubbing Center), CDN/Anycast 분산 및 WAF/L7 필터링 방어 아키텍처

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **서비스 수준 지표(Service Level Indicator, SLI)**: 정상 요청 성공률, Latency, 응답 시간 등 시스템 가용성 유지 상태를 측정하는 정량적 서비스 지표.
- **고갈 자원 식별**: 네트워크 대역폭(Gbps), L4 세션 테이블(CPS), L7 CPU/DB 연산량 중 병목이 발생한 정확한 공격 레이어를 판별하는 단계.
- **계층별 완화 적용**: 판별된 공격 레이어에 맞춰 BGP 스크러빙, SYN Cookie, HTTP Rate Limiting 조치를 적재적소 투입하는 단계.
- **정상 요청 SLI 검증**: 방어 정책 투입 후 정상 고객의 SLI 지표(성공률 99% 이상) 회복을 검증하여 방어 지속 및 복귀를 결정하는 단계.

</details>

`	ext
공격 트래픽 관측
        │
        ▼
1. 고갈 자원 식별
        │
        ▼
2. 계층별 완화 적용
        ├─ 회선 용량 ── 상류 스크러빙•애니캐스트
        ├─ 연결 상태 ── SYN 쿠키•연결률 제한
        └─ 응용 연산 ── WAF•요청률 제한
        │
        ▼
3. 정상 요청 SLI 검증
        ├─ 미달 ── 1. 고갈 자원 재식별
        └─ 충족 ── 방어 유지•단계적 복귀
`

### 동작 원리

1. **고갈 자원 식별**: 트래픽 감시 센서를 통해 병목 공격 레이어(L4 대역폭/세션 vs L7 연산) 정밀 판정
2. **계층별 완화 적용**: 대역폭 포화 시 BGP Anycast/스크러빙 전환, SYN Flood 시 SYN Cookie 적용, L7 공격 시 Rate Limit/WAF 챌린지 집행
3. **정상 요청 SLI 검증**: 정상 고객 요청 성공률 및 지연 시간(SLI) 대조 검증을 거쳐 안정화 시 단계적 정상 경로 BGP 복귀 완료


#### 한줄 요약

- 자원 고갈(대역폭/세션/앱) 식별, 계층별 대응(스크러빙/SYN 쿠키/WAF), SLI 기반 검증 및 정류 우회 제어 흐름

## Ⅴ. 종류 및 비교

| DDoS 공격 유형 | **대역폭형 (Volumetric)** | **프로토콜형 (State-Exhaustion)** | **응용형 (Application Layer)** |
|:---|:---|:---|:---|
| 타깃 자원 | 네트워크 대역폭 (Gbps/Tbps) | Firewall/Server 세션 테이블 (CPS) | Web/DB Server CPU 및 RAM 연산 |
| 주요 공격 기법 | UDP/NTP/DNS 반사 증폭, ICMP Flood | TCP SYN Flood, ACK Flood, RST Flood | HTTP GET/POST Flood, Slowloris, Slow Read |
| 패킷 특징 | 대용량 및 위조 출발지 IP 중심 | 미완결 TCP 세션 패킷 대량 유입 | 정상 파라미터 기반 L7 HTTP 요청 형태 |
| 핵심 완화 기술 | **BGP Anycast, 상류 스크러빙 센터** | **SYN Cookie, TCP Intercept, Rate Limit** | **WAF, JS Challenge, CAPTCHA, Rate Limit** |

> 요약: 타깃 고갈 자원의 계층(L4 대역폭/세션 vs L7 응용)에 부합하는 계층별 차등 방어

#### 한줄 요약

- 대역폭형(NTP/DNS 반사), 프로토콜형(SYN Flood), 응용형(HTTP Slowloris/GET Flood)의 공격 기법 및 완화 기술 비교

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **SYN 쿠키(SYN Cookie)**: TCP SYN-ACK 송신 시 연결 상태를 메모리 백로그 큐에 저장하지 않고, sequence number에 암호학적 해시 쿠키를 인코딩하여 ACK 수신 시 검증하는 기법.
- **IETF BCP 38(Best Current Practice 38)**: 출발지 IP 주소 위조를 사전에 차단하기 위한 에지 라우터 필터링 규격.
- **IETF RFC 4732(DoS Protection Requirements)**: 서비스 거부 공격에 대해 시스템 및 프로토콜 레벨에서 갖추어야 할 강건성 지침.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| IP 변조 기반 반사 증폭 공격 | **IETF BCP 38 출발지 필터링 & Ingress Control** | 불법 변조 출발지 IP 응답 증폭 차단 |
| DoS 프로토콜 설계 약점 | **IETF RFC 4732 강건성 기준 준수** | 타깃 시스템의 DoS 복원력 확보 |
| L4 SYN 백로그 큐 소진 | **SYN Cookie 및 TCP Reset Proxy** | 메모리 백로그 큐 고갈 방지 |
| 백본 대역폭 포화 대형 DDoS | **BGP Flowspec & 클라우드 스크러빙 연동** | 상류망 중심 트래픽 드롭 및 우회 |
| 조기 모드 복귀에 따른 2차 장애 | **SLI 가용성 지표 기반 단계적 정상 복귀** | 정제 후 불완전 복귀에 따른 재장애 차단 |

#### 한줄 요약

- IETF BCP 38/RFC 4732 준수, SYN 쿠키 적용, 상류 스크러빙 BGP 우회 연동 및 SLI 성공률 기반 복귀

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **SLI 기반 DDoS 방어(SLI-driven Defense)**: 공격 트래픽 차단 수치에 연연하지 않고 최종 사용자 관점의 가용성 지표(SLI)를 유지하는 방어 원칙.

</details>

- 자원 고갈 지점에 따라 회선은 **스크러빙**, 세션은 **SYN 쿠키**, HTTP 응용은 **WAF**를 적용하여 서비스 가용성 확보

#### 한줄 요약

- IETF BCP 38/RFC 4732 준수, 계층별 완화(스크러빙, SYN 쿠키, WAF) 및 SLI 가용성 지표 기반 DDoS 방어 체계 구축 필수