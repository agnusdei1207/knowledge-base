---
sidebar:
  order: 87
  label: "087. DDoS 공격 기법 및 다단 방어 체계"
  badge:
    text: "기출 · 50%"
    variant: note
title: "분산 서비스 거부 공격 및 계층형 방어 체계 : DDoS 완화"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 87
extra:
  question_no: "87"
  source_status: "기출"
  source_history: "125회"
  priority: 50
  priority_note: "대역폭 고갈(Volumetric), 프로토콜 상태 고갈(SYN Flood), L7 웹 공격 및 CDN/스크러빙 다단 완화"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **DDoS (Distributed Denial of Service)**: 대규모 분산 봇넷으로 표적 인프라의 대역폭과 세션 자원을 고갈시키는 가용성 침해 공격.
- **Multi-Layer Mitigation (다단 방어 체계)**: 상위 ISP, Anycast CDN, 클라우드 스크러빙 센터, 온프레미스 WAF로 계층 분할 정화하는 아키텍처.

</details>

- 정의/개념: 대용량 볼륨 공격부터 L4 세션 및 L7 애플리케이션 자원 고갈 공격까지 **상위 ISP, Anycast CDN, 스크러빙 센터, WAF를 통해 단계별로 정화하는 다단 방어 체계**
- 배경/필요성: 단일 방화벽 기반 방어의 한계로 인한 **수백 Gbps 대역폭 포화 시 인입 회선 마비, 세션 테이블 고갈 및 비즈니스 서비스 전면 중단**

#### 한줄 요약
- BGP Anycast 분산 흡수, 스크러빙 센터 세탁, WAF 정밀 필터링을 통해 서비스 가용성을 보장한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **BGP Anycast Routing**: 동일한 IP 주소를 전 세계 수십 개 데이터센터 PoP에서 동시 광고하여 공격 트래픽을 지리적으로 분산 흡수하는 기술.
- **Scrubbing Center (스크러빙 센터)**: 대규모 인입 트래픽 중 악성 패킷만 선택적으로 제거하고 정상 트래픽만 원본 서버로 전달하는 전문 정화 센터.

</details>

- **계층별 분할 완화(Tiered Mitigation)**: L3/L4 볼륨 공격은 **상위 ISP/CDN에서 흡수하고 L7 웹 공격은 WAF에서 정밀 차단**
- **BGP Anycast 기반 글로벌 분산 흡수**: 단일 표적 IP 트래픽을 수십 개 글로벌 PoP로 분산시켜 **Tbps급 공격을 국소화**
- **오탐(False Positive) 최소화 및 정상 트래픽 보존**: **SYN Cookie, JS Challenge, CAPTCHA**를 통해 악성 봇과 사용자 실시간 선별

#### 한줄 요약
- 계층별 다단 완화, BGP Anycast 분산 흡수, 스크러빙 센터 정화 및 챌린지 검증을 통한 오탐 방지를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SYN Cookie (RFC 4987)**: TCP 3-Way Handshake 시 서버 TCB 메모리를 할당하지 않고 암호화된 시퀀스 번호로 최종 ACK를 검증하는 방어 기술.

</details>

```text
[DDoS 계층형 다단 방어 파이프라인 아키텍처]
|-- Tier 1: Global ISP / CDN Anycast Edge (Tbps급 L3/L4 볼륨 공격 분산 흡수, BGP Flowspec)
|-- Tier 2: Cloud Scrubbing Center (대용량 트래픽 세탁)
|   |-- L4 Filter: SYN Proxy, SYN Cookie, UDP Rate Limiting
|   `-- L7 Filter: JavaScript Challenge, Client TLS Fingerprint
`-- Tier 3: Enterprise Origin Infrastructure (WAF / API Gateway / Origin App Server)
    `-- Protected Traffic via GRE / IPsec Tunnel (정상 비즈니스 트래픽만 무손실 수신)
```

선의 의미: 대규모 공격 트래픽이 글로벌 Anycast CDN과 스크러빙 센터를 거치며 계층별로 필터링되어 정화된 정상 트래픽만 원본 서버에 도달하는 구조

| 방어 계층 | 핵심 엔지니어링 책임 | 주요 특징 | 방어 대상 공격 |
|:---|:---|:---|:---|
| **상위 ISP / CDN 계층** | **BGP Anycast, BGP Flowspec으로 초대용량 트래픽 분산 및 회선 보호** | Tier 1 | NTP/DNS 증폭, UDP Flood |
| **스크러빙 센터 계층** | **트래픽 세탁, SYN Cookie 검증, 딥 패킷 필터링으로 정상 패킷 선별** | Tier 2 | SYN Flood, Slowloris |
| **온프레미스 / WAF 계층**| **L7 HTTP 트래픽 검사, 클라이언트 행동 분석, 정밀 Rate Limiting** | Tier 3 | HTTP GET/POST Flood |

#### 한줄 요약
- 상위 ISP/CDN Anycast, 클라우드 스크러빙 센터, 온프레미스 WAF의 3계층 다단 방어로 인프라를 보호한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **BGP Flowspec (RFC 5575)**: 컨트롤러가 BGP를 통해 라우터 FIB에 세부 패킷 필터링 룰(Src/Dst, 포트 등)과 액션(Drop, Redirect)을 자동 주입하는 기술.

</details>

```text
DDoS 이상 감지, 트래픽 우회 및 스크러빙 정화 파이프라인
        │
   1. [트래픽 이상 감지] 텔레메트리 모니터링이 Baseline 대비 bps/pps 임계치 초과 감지
        │
   2. [스크러빙 센터 우회] BGP Flowspec 또는 DNS CNAME 변경으로 인입 트래픽을 스크러빙 센터로 절체
        │
   3. [L4 프로토콜 정화] 스크러빙 센터에서 SYN Proxy/Cookie 및 UDP Rate Limiting 집행
        │
   4. [L7 봇넷 챌린지 검증] WAF가 JavaScript Challenge 및 TLS Fingerprint 분석으로 악성 봇 차단
        │
   ▼
5. [정상 트래픽 터널 전송] 세탁된 정상 패킷만 전용 GRE/IPsec 터널을 통해 원본 서버로 전달
```

#### 한줄 요약
- Baseline 이상 감지 → BGP 트래픽 우회 → L4/L7 단계별 필터링 → GRE 정상 패킷 전달 → 서비스 가용성 유지 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Volumetric vs State-Exhaustion vs Application (L7)**: 대역폭 포화(bps), 세션 테이블 고갈(pps), 웹서버 컴퓨팅 고갈.

</details>

| 비교 항목 | 볼륨형 공격 (Volumetric Attack) | 프로토콜 상태 고갈 (State-Exhaustion) | 애플리케이션 공격 (L7 App Attack) |
|:---|:---|:---|:---|
| **공격 대상 자원** | **네트워크 회선 인입 대역폭 (bps)** | **방화벽/로드밸런서 세션 테이블 (pps)** | **웹 서버 CPU, 메모리, DB 커넥션** |
| **대표 공격 기법** | **NTP/DNS/SSDP 반사 증폭, UDP Flood** | **TCP SYN Flood, ACK Flood, RST Flood** | **HTTP GET/POST Flood, Slowloris** |
| **패킷 특성** | 무차별 대용량 비인가 UDP/ICMP 패킷 | 대량의 위조 플래그 TCP 제어 패킷 | 정상적인 규격의 정상 HTTP/HTTPS 요청 |
| **핵심 방어 대책** | **BGP Anycast, CDN, 스크러빙 센터** | **SYN Proxy, SYN Cookie, TCB 관리** | **WAF, JS Challenge, Rate Limiting** |

#### 한줄 요약
- 볼륨형은 대역폭 분산, 프로토콜형은 SYN Cookie, L7 공격은 WAF/Rate Limiting으로 방어한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Slowloris (슬로우로리스)**: HTTP 헤더 끝(`\r\n\r\n`)을 완성하지 않고 미완성 헤더를 느리게 전송하여 웹서버 스레드 풀을 장시간 고갈시키는 L7 저속 공격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 500Gbps 이상 초대용량 UDP 반사 공격으로 전용 회선 대역폭 포화 | **`상위 ISP BGP Flowspec` 차단 및 글로벌 Anycast 스크러빙** 우회 | 인입 회선 포화 사전 방지 및 비즈니스 대역폭 보존 |
| 대규모 위조 SYN Flood 공격으로 방화벽/서버 TCB 세션 고갈 | L4 방화벽 전단에 **`하드웨어 기반 SYN Cookie` 및 SYN Proxy 활성화** | 가짜 반개방 세션 저장 원천 제거 및 신규 연결 보장 |
| 정상 트래픽과 동일한 패턴의 L7 Slowloris 및 무차별 웹 크롤링 폭주 | **`L7 클라이언트 지문(JA3/TLS) 분석` 및 비용 기반 레이트 리미팅** | 백엔드 서버 CPU 고갈 차단 및 99.9% 오탐 없는 정상 수용 |
| 스크러빙 센터 우회 후 직접 원본 서버(Origin) IP로 공격 집중 | **`Origin IP 은폐` 및 스크러빙 PoP IP만 인가하는 Ingress 화이트리스트** | 백엔드 원본 직접 타격 원천 차단 |

#### 한줄 요약
- BGP Flowspec으로 회선을 방어하고, SYN Cookie로 세션 고갈을 차단하며, TLS 지문 분석으로 L7 공격을 무력화한다.

## Ⅶ. 결론

- 진화하는 하이브리드 멀티벡터 사이버 공격으로부터 엔터프라이즈 서비스의 무중단 가용성을 사수하기 위해 **ISP-CDN-Scrubbing-WAF로 이어지는 다단 DDoS 방어 체계를 필수 구현**하되, 운영 효율성을 극대화하기 위해 **BGP Anycast 분산 인프라, 하드웨어 가속 SYN Proxy/Cookie, AI 기반 행동 프로파일링 및 자동화된 챌린지 검증**을 통합 연계하여 제로 다운타임(Zero-Downtime) 보안 아키텍처 완성

#### 한줄 요약
- DDoS 방어는 BGP Anycast 분산 흡수와 스크러빙 센터 세탁 및 WAF 정밀 필터링을 결합한 다단 완화 아키텍처로 실현된다.