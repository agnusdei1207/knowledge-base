---
sidebar:
  order: 87
  label: "087. DDoS 공격 기법 및 다단 방어 체계"
  badge:
    text: "기출 · 50%"
    variant: note
title: "분산 서비스 거부 공격 및 계층형 방어 체계 : DDoS 완화 (DDoS Attack Mitigation)"
date: "2026-08-22T08:15:00+09:00"
tags: ["notes-network"]
weight: 87
extra:
  question_no: "087"
  source_status: "기출"
  source_history: "125회"
  priority: 50
  priority_note: "대역폭 고갈(Volumetric), 프로토콜 상태 고갈(SYN Flood), L7 웹 공격 및 CDN/스크러빙 다단 완화"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **분산 서비스 거부 공격(Distributed Denial of Service, DDoS)**: 대규모 악성 봇넷(Botnet) 또는 분산 호스트를 악용하여 표적 서버나 네트워크 인프라의 회선 대역폭, 커넥션 테이블, 컴퓨팅 자원을 고갈시켜 정상 사용자의 서비스 이용을 차단하는 가용성(Availability) 침해 공격.
- **다단 방어 체계(Multi-Layer DDoS Mitigation)**: 공격 트래픽의 유형(L3/L4 볼륨형 vs L7 애플리케이션형)과 규모에 맞춰 상위 ISP 백본, 글로벌 CDN Anycast 엣지, 전용 클라우드 스크러빙 센터(Scrubbing Center), 온프레미스 WAF/Anti-DDoS 장비로 계층 분할 방어하는 아키텍처.

</details>

- 정의/개념: 인프라 대역폭을 마비시키는 볼륨 공격부터 TCP/IP 스택 및 L7 애플리케이션 자원을 고갈시키는 정밀 공격을 단계별로 탐지·흡수·정화(Scrubbing)하여 **서비스 가용성을 100% 지속 보증하는 계층형 네트워크 방어 체계**
- 배경/필요성: 테라비트급(Tbps) 초대규모 반사 증폭 공격과 정상 트래픽으로 위장한 정밀 L7 HTTP Flooding이 결합된 하이브리드 멀티벡터 공격이 증가함에 따라, 단일 온프레미스 방화벽 용량 한계를 극복할 요구

#### 한줄 요약
- L3/L4/L7 다계층 공격에 대응하여 ISP, CDN Anycast, 스크러빙 센터를 연계한 다단 완화 체계를 구축한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **스크러빙 센터(Scrubbing Center)**: BGP Anycast 또는 DNS 라우팅을 통해 이상 트래픽을 대용량 정화 인프라로 우회(Diversion)시켜 악성 패킷만 필터링하고 정상 패킷만을 GRE/IPsec 터널로 원본 서버에 전달하는 특화 정화 시설.
- **BGP Anycast 라우팅**: 동일한 IP 주소를 전 세계 복수의 PoP(Point of Presence)에 BGP 경로로 광고하여 대규모 공격 트래픽을 지리적으로 분산 흡수하는 네트워크 라우팅 기법.

</details>

- **공격 벡터별 계층 분할 방어**: L3/L4 초대용량 볼륨 트래픽은 상위 CDN/스크러빙 센터에서 흡수하고, 정밀 L7 공격은 WAF/API 게이트웨이에서 인텔리전트 차단
- **BGP Anycast 기반 트래픽 분산 분할**: 단일 목적지로 집중되는 수백 Gbps 트래픽을 전 세계 수십 개 엣지 PoP로 분산시켜 인프라 포화 방지
- **오탐(False Positive) 최소화 및 정상 트래픽 보존**: 정교한 챌린지 검증(SYN Cookie, JavaScript Challenge, CAPTCHA)을 통해 악성 봇과 정상 사용자를 실시간 선별

#### 한줄 요약
- 계층별 다단 완화, BGP Anycast 분산 흡수, 스크러빙 센터 정화 및 챌린지 검증을 통한 오탐 방지를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SYN 쿠키(SYN Cookie)**: TCP 3-Way Handshake 시 서버 메모리에 반개방(Half-Open) TCB 연결 상태를 저장하지 않고, 암호화된 시퀀스 번호(Cookie)를 생성하여 클라이언트의 최종 ACK 검증 시에만 세션을 할당하는 방어 기술 (RFC 4987).

</details>

```text
[ 대규모 분산 봇넷 (Botnet Attackers) ] ── (수백 Gbps 악성 트래픽 송출)
                     │
                     ▼ (BGP Anycast 라우팅을 통한 지리적 분산 유입)
[ 1단계: 상위 ISP / 글로벌 CDN Anycast 엣지 ] ── (L3/L4 대역폭 고갈 볼륨 공격 1차 흡수)
                     │
                     ▼ (이상 임계치 초과 시 BGP Flowspec / DNS 변경으로 트래픽 우회)
[ 2단계: 클라우드 스크러빙 센터 (Scrubbing Center) ]
 ├─ L4 필터: SYN Proxy, SYN Cookie, UDP Rate Limiting
 └─ L7 필터: JavaScript Challenge, 행위 기반 봇 탐지
                     │ (정화된 정상 트래픽만 GRE / IPsec 터널로 전달)
                     ▼
[ 3단계: 엔터프라이즈 인프라 (WAF / Anti-DDoS / Origin) ] ──▶ [ 정상 웹 애플리케이션 서비스 ]
```

선의 의미: 대규모 공격 트래픽이 글로벌 Anycast CDN과 스크러빙 센터를 거치며 계층별로 필터링되어 최종적으로 정화된 정상 트래픽만 원본 서버에 도달하는 다단 방어 파이프라인

| 방어 계층 | 주요 구성요소 | 핵심 책임 및 역할 | 방어 대상 공격 |
|:---|:---|:---|:---|
| **상위 ISP / CDN 계층** | BGP Anycast, BGP Flowspec, Blackholing | 수백 Gbps~Tbps급 초대용량 트래픽 분산 및 회선 대역폭 보호 | NTP/DNS 증폭, UDP Flooding |
| **스크러빙 센터 계층** | 전용 하드웨어 방어 섀시, 딥 패킷 필터링 | 트래픽 세탁, SYN Cookie 검증, 시그니처/행위 기반 필터링 | SYN Flood, ACK Flood, Slowloris |
| **온프레미스 / WAF 계층**| WAF, API Gateway, Anti-DDoS Appliance | 세밀한 L7 HTTP 트래픽 검사, 사용자 행동 분석, Rate Limiting | HTTP GET/POST Flood, CC Attack |

#### 한줄 요약
- 상위 ISP/CDN Anycast, 클라우드 스크러빙 센터, 온프레미스 WAF의 3계층 다단 방어로 인프라를 보호한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **BGP Flowspec(RFC 5575)**: 네트워크 제어기가 BGP 프로토콜을 활용하여 라우터의 FIB에 세부 패킷 필터링 룰(Src/Dst IP, L4 Port, 패킷 길이 등)과 액션(Drop, Rate-limit, Redirect)을 실시간 자동 주입하는 고속 완화 기술.

</details>

```text
1. 텔레메트리 모니터링 시스템이 정상 트래픽 기준선(Baseline) 대비 임계치 초과 공격 트래픽 감지
            │
            ▼
2. BGP Flowspec 또는 DNS CNAME 변경을 통해 인입 트래픽을 전용 클라우드 스크러빙 센터로 긴급 우회
            │
            ▼
3. 스크러빙 센터에서 L3/L4 대역폭 필터링(Blackholing/Rate Limiting) 및 TCP SYN Proxy/Cookie 검증 집행
            │
            ▼
4. L7 애플리케이션 트래픽에 대해 WAF가 브라우저 무결성 검증(JS Challenge) 및 Rate Limiting 수행
            │
            ▼
5. 악성 패킷을 전량 차단하고, 세탁된 정상 패킷만 전용 GRE 터널을 통해 원본 서버(Origin)로 무손실 전달
```

**동작 원리**

1. **실시간 이상 감지**: NetFlow/IPFIX 수집기가 pps 및 bps 급증을 감지하여 알람 트리거
2. **트래픽 동적 우회**: BGP Anycast 광고를 활성화하여 인입 경로를 스크러빙 PoP로 즉각 절체
3. **L4 상태 검증**: SYN Proxy가 3-Way Handshake를 대신 완료하고 정상 클라이언트의 세션만 백엔드로 연계
4. **L7 봇넷 선별**: HTTP 요청 헤더 검증 및 토큰 기반 챌린지를 인가하여 자동화된 스크립트 차단
5. **정상 서비스 유지**: 백엔드 원본 IP를 외부에 은폐하고 스크러빙 센터를 경유한 트래픽만 허용

#### 한줄 요약
- Baseline 이상 감지, BGP 트래픽 우회, L4/L7 단계별 필터링, GRE 정상 패킷 전달, 서비스 가용성 유지 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **볼륨형(Volumetric) vs 프로토콜(Protocol) vs 애플리케이션(L7) 공격**: 회선 대역폭 포화, 방화벽/스위치 커넥션 테이블 고갈, 웹서버 CPU/DB 자원 고갈을 목적으로 하는 3대 DDoS 유형.

</details>

| 비교 항목 | 볼륨형 공격 (Volumetric Attack) | 프로토콜 상태 고갈 (State-Exhaustion) | 애플리케이션 공격 (L7 App Attack) |
|:---|:---|:---|:---|
| **공격 대상 자원** | **네트워크 회선 인입 대역폭 (bps)** | **방화벽/로드밸런서 세션 테이블 (pps)** | **웹 서버 CPU, 메모리, DB 커넥션** |
| **대표 공격 기법** | **NTP/DNS/SSDP/Memcached 반사 증폭** | **TCP SYN Flood, ACK Flood, RST Flood** | **HTTP GET/POST Flood, Slowloris** |
| **패킷 특성** | 무차별 대용량 비인가 UDP/ICMP 패킷 | 대량의 위조 플래그 TCP 제어 패킷 | 정상적인 규격의 정상 HTTP/HTTPS 요청 |
| **핵심 방어 대책** | **BGP Anycast, CDN, 스크러빙 센터** | **SYN Proxy, SYN Cookie, TCB 관리** | **WAF, JS Challenge, Rate Limiting** |

#### 한줄 요약
- 볼륨형은 대역폭 분산, 프로토콜형은 SYN Cookie, L7 공격은 WAF/Rate Limiting으로 방어한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **슬로우로리스(Slowloris)**: HTTP 요청 헤더의 끝(`\r\n\r\n`)을 고의로 완성하지 않고 불완전한 헤더를 매우 느린 속도로 주기적 전송하여 웹서버의 모든 가용 스레드와 커넥션을 장시간 점유 고갈시키는 지능형 L7 저속 공격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 500Gbps 이상 초대용량 UDP 반사 증폭 공격 유입 시 전용 회선 대역폭 완전 포화 | **상위 ISP BGP Flowspec 기반 유입지 차단** 및 **글로벌 Anycast 스크러빙** 우회 | 인입 회선 포화 사전 방지 및 정상 비즈니스 대역폭 보존 |
| 대규모 위조 SYN Flood 공격으로 인한 방화벽/서버의 TCB(세션 메모리) 고갈 붕괴 | L4 방화벽 전단에 **하드웨어 기반 SYN Cookie** 및 **SYN Proxy** 활성화 | 가짜 반개방 세션 저장 원천 제거 및 신규 정상 TCP 연결 완벽 보장 |
| 정상 트래픽과 동일한 패턴의 L7 Slowloris 및 무차별 HTTP 검색 매크로 폭주 | **L7 클라이언트 지문 분석(JA3/TLS Fingerprint)** 및 **비용 기반 레이트 리미팅** | 백엔드 DB/서버 CPU 고갈 차단 및 99.9% 오탐 없는 정상 요청 수용 |

#### 한줄 요약
- BGP Flowspec으로 회선을 방어하고, SYN Cookie로 세션 고갈을 차단하며, TLS 지문 분석으로 L7 공격을 무력화한다.

## Ⅶ. 결론

- 진화하는 하이브리드 멀티벡터 사이버 공격으로부터 엔터프라이즈 서비스의 무중단 가용성을 사수하기 위해 **ISP-CDN-Scrubbing-WAF로 이어지는 다단 DDoS 방어 체계**를 필수 구현하되, 운영 효율성을 극대화하기 위해 **BGP Anycast 분산 인프라**, **하드웨어 가속 SYN Proxy/Cookie**, **AI 기반 행동 프로파일링 및 자동화된 챌린지 검증**을 통합 연계하여 제로 다운타임(Zero-Downtime) 보안 아키텍처를 완성

#### 한줄 요약
- 다단 방어 체계와 BGP Anycast, 스크러빙 센터를 결합하여 고신뢰 DDoS 완화 인프라를 실현한다.
