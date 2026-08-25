---
sidebar:
  order: 90
  label: "090. SASE: SD-WAN•CASB•SWG•ZTNA"
  badge:
    text: "기출 · 50%"
    variant: note
title: "클라우드 네트워크 보안 융합 : SASE 및 SSE"
date: "2026-08-25T12:00:00+09:00"
tags:
  - "notes-network"
weight: 90
extra:
  question_no: "90"
  source_status: "기출"
  source_history: "135회"
  priority: 50
  priority_note: "네트워크(SD-WAN)와 보안(SSE: CASB, SWG, ZTNA, FWaaS)의 글로벌 엣지 PoP 통합 아키텍처"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **SASE (Secure Access Service Edge)**: 광역 네트워크(SD-WAN)와 종합 보안 서비스(SSE)를 글로벌 클라우드 엣지 PoP에 단일 패스로 통합한 아키텍처.
- **SSE (Security Service Edge)**: SASE에서 네트워크 전송 계층을 분리하고 SWG, CASB, ZTNA, FWaaS 보안 기능에 집중한 통합 클라우드 보안 스택.

</details>

- 정의/개념: 광역 네트워크(SD-WAN)와 포괄적 보안 스택(SSE: CASB, SWG, ZTNA, FWaaS)을 **글로벌 클라우드 엣지 PoP에 통합하여 일관된 정책을 제공하는 서비스 프레임워크**
- 배경/필요성: 멀티클라우드 및 원격근무 확산 시 본사 경유(Hairpinning) 방식의 **회선 병목 지연, 하드웨어 장비 파편화 및 클라우드 SaaS 가시성 부재**

#### 한줄 요약
- SD-WAN 경로 최적화와 SSE 제로 트러스트 보안을 글로벌 클라우드 엣지 PoP에서 단일 패스로 통합 제공한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Single-Pass Architecture**: 트래픽을 단 한 번만 복호화하여 SWG, CASB, DLP, IPS 등 복수의 보안 엔진이 병렬로 검사하는 고속 처리 구조.
- **ZTNA (Zero Trust Network Access)**: 사용자와 단말의 신원을 연속 검증하여 인가된 특정 애플리케이션에만 일대일 격리 터널을 제공하는 기술.

</details>

- **네트워크와 보안의 클라우드 네이티브 융합**: SD-WAN의 동적 경로 제어와 SSE의 **다계층 보안 기능을 단일 클라우드 플랫폼으로 통합**
- **단일 패스(Single-Pass) 병렬 검사 엔진**: 트래픽을 1회만 복호화하여 **모든 보안 엔진을 동시 병렬 수행함으로써 처리 지연 극소화**
- **전 세계 글로벌 분산 엣지 PoP 기반 통제**: 사용자 근접 위치에서 **보안 정책을 집행하여 인터넷 백본 지연 없는 쾌적한 접속 보장**

#### 한줄 요약
- 네트워크·보안 융합, 단일 패스 병렬 검사, 글로벌 엣지 PoP 기반 제로 트러스트 통제를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Global SASE PoP**: 전 세계 거점에 분산 배치되어 애니캐스트(Anycast) 라우팅을 통해 사용자와 가장 가까운 위치에서 보안과 트래픽을 중계하는 클라우드 거점.

</details>

```text
[SASE 클라우드 네이티브 융합 아키텍처]
|-- Distributed Endpoints (재택근무자 모바일/PC 단말, 지사 Branch 라우터, IoT 기기)
`-- Global Distributed SASE Edge PoPs (초저지연 Anycast 인입)
|   |-- Network as a Service: SD-WAN (동적 경로 최적화, QoS, 멀티클라우드 연동)
|   `-- Security as a Service: SSE Stack (Single-Pass 복호화 및 병렬 검사)
|       |-- SWG (Secure Web Gateway: 악성 URL/파일 검사, 웹 격리)
|       |-- CASB (Cloud Access Security Broker: SaaS 가시성, Shadow IT 통제, DLP)
|       |-- ZTNA (Zero Trust Network Access: 앱 단위 마이크로 세그멘테이션)
|       `-- FWaaS (Firewall as a Service: 클라우드 차세대 L7 방화벽/IPS)
`-- Target Destinations (M365, AWS/Azure 클라우드, 사내 온프레미스 DC)
```

선의 의미: 사용자가 근접 SASE PoP로 접속하여 SD-WAN 경로 최적화와 SSE 보안 검사를 단일 패스로 통과한 후 대상 리소스로 분기되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **SD-WAN** | 인터넷, MPLS, 5G 회선을 가상화하여 **앱 품질 기반 최적 경로 라우팅** | Network as a Service |
| **SWG** | 웹 트래픽 암복호화 검사, **악성 사이트 차단 및 웹 바이러스 필터링** | L7 Web Security |
| **CASB** | 인가/비인가 SaaS 모니터링, **API 연동 데이터 감사, 클라우드 DLP 통제** | Cloud Security |
| **ZTNA** | SDP 기반 인프라 은폐 및 **앱 단위 세분화 일대일 제로트러스트 접근** | Zero Trust Edge |
| **FWaaS** | 클라우드 상에서 구동되는 **탄력적 L7 차세대 방화벽 및 침입 방지(IPS)** | Firewall as a Service |

#### 한줄 요약
- SD-WAN, SWG, CASB, ZTNA, FWaaS가 글로벌 PoP 상에서 단일 패스 구조로 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **CARTA (Continuous Adaptive Risk and Trust Assessment)**: 세션 유지 중에도 사용자의 이상 행동과 단말 보안 상태를 실시간 재평가하여 위험도에 따라 권한을 동적 회수하는 평가 모델.

</details>

```text
SASE 근접 접속, 단일 패스 검사 및 트래픽 분기 파이프라인
        │
   1. [근접 PoP Anycast 인입] 단말 트래픽이 지리적으로 가장 가까운 SASE PoP으로 초저지연 연결
        │
   2. [IdP 및 단말 맥락 검증] IdP 연동 MFA 인증 및 엔드포인트 EDR 상태(보안 패치) 동시 검증
        │
   3. [단일 패스 병렬 보안 검사] 1회 SSL 복호화로 SWG, CASB, DLP, IPS 보안 정책 일괄 집행
        │
   ├─ [일반 웹 트래픽] ➔ SWG 악성 사이트 필터링 후 공용 인터넷 직결
   ├─ [SaaS 클라우드] ➔ CASB 인가 및 DLP 검사 후 SaaS(M365 등) 직결
   └─ [사내 프라이빗 앱] ➔ ZTNA 컨트롤러를 통해 인프라 은폐 후 일대일 세션 중계
        │
   ▼
4. [CARTA 동적 세션 제어] 세션 중 이상 징후 감지 시 실시간 스텝업 인증 요구 또는 즉각 차단
```

#### 한줄 요약
- 근접 PoP 인입 → 신원/맥락 인증 → 단일 패스 보안 검사 → 목적지 직결 → 실시간 위험 재평가 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **레거시 VPN vs SSE vs SASE**: 본사 헤어핀 방식, 보안 기능 중심 클라우드화, 네트워크와 보안의 완전한 클라우드 네이티브 융합.

</details>

| 비교 항목 | 전통적 본사 중심 보안 (레거시 VPN) | 보안 서비스 엣지 (SSE) | 보안 액세스 서비스 엣지 (SASE) |
|:---|:---|:---|:---|
| **트래픽 전송 경로**| 본사 데이터센터 우회 (헤어피닝) | 사용자 $\rightarrow$ 클라우드 보안 PoP | **사용자 $\rightarrow$ SD-WAN 최적화 PoP $\rightarrow$ 목적지** |
| **통합 아키텍처** | 온프레미스 방화벽 개별 운영 | **보안 서비스(SWG/CASB/ZTNA) 통합** | **네트워크(SD-WAN) + 보안(SSE) 완전 통합** |
| **접근 제어 모델** | 서브넷/VLAN 기반 광범위 접속 | **신원 및 앱 기반 제로 트러스트(ZTNA)**| **신원, 단말, 네트워크 경로 통합 제어** |
| **성능 및 지연** | 원격 접속 증가 시 본사 회선 병목 | 클라우드 직결로 인터넷 지연 개선 | **SD-WAN 동적 경로 제어로 최상의 QoS 보장** |
| **도입 목적** | 과거 폐쇄망 환경 유지 | 보안 스택 클라우드 전환에 최적 | **전사 디지털 전환(DX)의 최종 지향점** |

#### 한줄 요약
- 레거시는 본사 병목 유발, SSE는 보안 기능 클라우드화, SASE는 네트워크와 보안의 완전한 통합 완성형이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Single Pane of Glass (단일 콘솔)**: 복잡하게 분산된 SD-WAN 네트워크 정책과 SSE 다계층 보안 규칙을 단 하나의 중앙 웹 콘솔에서 일괄 관리하는 거버넌스 체계.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 특정 지역 SASE PoP 장애 시 해당 권역 지사의 전사 네트워크 단절 | SD-WAN 기반 **`인접 다중 PoP 자동 헬스체크 및 서브초 페일오버`** | PoP 단일 장애점(SPOF) 제거 및 99.999% 가용성 보장 |
| 네트워크 팀(SD-WAN)과 보안 팀(SSE) 간의 정책 불일치로 오차단 발생 | SASE **`단일 콘솔(Single Pane of Glass) 기반 통합 거버넌스`** | 정책 충돌 제거 및 관리 오버헤드 50% 절감 |
| 레거시 VPN 허용으로 인한 감염 단말의 사내망 횡적 확산 위협 | VPN 전면 폐기 및 **`ZTNA 기반 앱 단위 마이크로 세그멘테이션`** | 감염 PC의 타 사내 시스템 접근 차단 및 공격 표면 축소 |
| SSL/TLS 트래픽 암호화 비중(95% 이상) 증가로 인한 복호화 연산 병목 | **`단일 패스(Single-Pass) 하드웨어 가속` 및 도메인 바이패스** | 보안 검사 지연 극소화 및 대역폭 처리량 극대화 |

#### 한줄 요약
- 다중 PoP 페일오버로 가용성을 확보하고, 단일 콘솔로 정책 충돌을 방지하며, ZTNA로 횡적 확산을 차단한다.

## Ⅶ. 결론

- 멀티클라우드와 하이브리드 워크 환경의 확산에 대응하여 엔터프라이즈 인프라를 보호하기 위해 **SD-WAN과 SSE를 결합한 SASE 표준 아키텍처를 전면 도입**하되, 글로벌 운영의 안정성을 보장하기 위해 **다중 PoP 이중화, 단일 콘솔 기반 통합 정책 운영, ZTNA 연속 신원 검증**을 통합 구축하여 안전하고 민첩한 제로 트러스트 클라우드 네트워크 완성

#### 한줄 요약
- SASE는 SD-WAN 네트워크 최적화와 SSE 제로 트러스트 보안을 단일 클라우드 엣지에서 융합하는 차세대 엔터프라이즈 아키텍처다.