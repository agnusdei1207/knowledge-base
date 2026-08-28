---
sidebar:
  order: 141
  label: "141. 보안 접근 서비스 경계(Secure Access Service Edge, SASE) 아키텍처"
  badge:
    text: "기출 · 70%"
    variant: note
title: "클라우드 네이티브 네트워크 및 보안 융합 아키텍처 : SASE 및 SSE (NIST SP 800-207 & MEF 117)"
date: "2026-08-26T15:19:11+09:00"
tags:
  - "notes-security"
weight: 141
extra:
  question_no: "141"
  source_status: "기출"
  source_history: "135회"
  priority: 70
  priority_note: "135회 기출, SASE(Secure Access Service Edge), WAN 에지(SD-WAN)와 보안 서비스(SSE: SWG, CASB, ZTNA, FWaaS)의 클라우드 네이티브 단일 플랫폼 융합, 전 세계 분산 PoP(Point of Presence), 지속적 위험 평가(Continuous Risk Assessment), NIST SP 800-207(ZTA) 및 MEF 117/118 표준"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **보안 접근 서비스 경계(SASE: Secure Access Service Edge / Gartner 2019 & MEF 117)**: 광역 네트워크(SD-WAN: Software-Defined WAN) 기능과 포괄적 클라우드 보안 서비스(SSE: Security Service Edge — SWG, CASB, ZTNA, FWaaS)를 클라우드 네이티브 단일 아키텍처로 통합하여, 사용자의 위치(본사, 지사, 재택, 이동 중)와 무관하게 전 세계 분산 PoP(Point of Presence)를 통해 초저지연 연결과 일관된 제로 트러스트 보안 정책을 서비스(As-a-Service) 형태로 제공하는 프레임워크.
- **기존 중앙 집중식 트래픽 백홀(Backhaul) 및 포인트 솔루션 파편화 결함(Hairpinning & Silo Defect)**: 원격 근무자가 클라우드 SaaS(M365, Salesforce)에 접근할 때 모든 트래픽을 본사 데이터센터 방화벽으로 강제 우회(Hairpinning)시킴으로써 발생하는 네트워크 병목, 지연 시간(Latency) 폭증, 그리고 지사마다 서로 다른 개별 보안 하드웨어 운용에 따른 정책 불일치 결함.

</details>

- 정의/개념: 분산 업무 환경의 연결성과 보안성을 일원화하기 위해 **글로벌 분산 PoP 인입 $\rightarrow$ IdP 연동 신원 및 단말 상태 검증 $\rightarrow$ SSE 보안 엔진(SWG/CASB/ZTNA/FWaaS) 실시간 검사 $\rightarrow$ SD-WAN 기반 최적 지능형 라우팅 $\rightarrow$ 세션 수명주기 전반의 지속적 위험 평가(Continuous Risk Assessment)** 를 집행하는 **네트워크-보안 융합 클라우드 에지 아키텍처**
- 배경/필요성: 원격 트래픽을 본사로 백홀해 장비를 통과시키면 사용자 수만큼 왕복 지연과 장비별 정책 동기화 비용이 늘어나므로, 검사 기능을 사용자 근처 **PoP의 클라우드 에지**로 내리고 정책은 신원 기준 단일 평면으로 합친 것

#### 한줄 요약
- SASE는 SD-WAN 네트워크와 SSE 클라우드 보안 서비스를 단일 PoP 에지 플랫폼으로 융합 제공한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **SASE 3대 핵심 융합 축**:
  - **SD-WAN 기반 지능형 연결성 (Intelligent Routing)**: 애플리케이션 유형(음성, 비디오, 데이터)에 따라 최적의 광역 통신 경로를 동적 선택.
  - **SSE 기반 포괄적 클라우드 보안 (Unified Security Edge)**: SWG(웹 보호), CASB(SaaS 통제), ZTNA(비공개 앱 접근), FWaaS(L7 방화벽)를 단일 패스(Single-pass)로 검사.
  - **글로벌 분산 PoP 및 전용 백본 (Global PoP Fabric)**: 전 세계 주요 인터넷 교환 노드에 에지 거점을 배치하여 10ms 이내 초저지연 보장.

</details>

- 신원·단말·데이터를 결합한 **맥락 기반 동적 정책**
- PoP에서 복수 엔진을 실행하는 **단일 패스 검사**
- 트래픽 변화에 자동 대응하는 **클라우드 탄력성**

#### 한줄 요약
- SD-WAN/SSE 원바디 융합, 글로벌 PoP 분산 에지, 단일 패스 병렬 검사, 신원 기반 동적 정책을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SASE 아키텍처 4대 핵심 컴포넌트 도메인**:
  1. **Edge Client & Branch SD-WAN**: 사용자 단말 경량 에이전트 및 지사 SD-WAN 라우터.
  2. **Global PoP Fabric**: 전 세계 분산 데이터센터에 구축된 SASE 에지 처리 노드.
  3. **Security Service Edge (SSE Engine)**: SWG, CASB, ZTNA, FWaaS, DLP, RBI, DNS Security.
  4. **Unified Cloud Control Plane**: 중앙 집중형 단일 정책 관리 콘솔 및 모니터링 엔진.

</details>

```text
SASE 아키텍처
├─ Edge Client·Branch SD-WAN
├─ Global PoP Fabric
├─ Security Service Edge
│  └─ SWG·CASB·ZTNA·FWaaS·DLP·RBI
└─ Unified Cloud Control Plane
```

선의 의미: 엔드포인트가 가장 가까운 PoP로 연결되어 단일 패스 검사와 중앙 정책 판정을 거친 후 최적 경로로 앱에 연결되는 구조

| 구성요소 | 책임 |
|:---|:---|
| **Edge Client·Branch SD-WAN** | 단말 접속과 회선별 최적 경로 선택 |
| **Global PoP Fabric** | 사용자와 가까운 에지에서 트래픽 처리 |
| **Security Service Edge** | SWG·CASB·ZTNA·FWaaS 단일 패스 검사 |
| **Unified Cloud Control Plane** | 신원·단말 정책 관리와 PoP 동기화 |

#### 한줄 요약
- 접근 허용의 근거가 사내망이라는 네트워크 위치에서 사용자와 단말의 신원으로 바뀌므로, 정책 판정은 단일 클라우드 관리 평면에 모으고 집행만 사용자와 가까운 PoP에 분산해 두는 배치가 된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **SASE 안전 접근 5단계 트랜잭션 수명주기**:
  1. 원격 단말이 Anycast DNS를 통해 가장 가까운 지리적 PoP로 자동 연결
  2. IdP 및 단말 무결성 검증을 통한 사용자 신원 및 보안 태세(Posture) 평가
  3. PoP 내부의 단일 패스(Single-pass) 엔진에서 복호화 및 복합 보안 정책(SSE) 검사
  4. SD-WAN 지능형 경로 라우팅을 통해 대상 사내 앱 또는 SaaS로 최단 전송
  5. 세션 유지 중 행위 이상 징후 실시간 재평가(Continuous Posture Check)

</details>

```text
사용자        SASE PoP        제어 플레인        애플리케이션
  | 접속 요청     |                 |                    |
  |------------->|                 |                    |
  |               | 1. 신원·태세 검증                  |
  |               |---------------->|                    |
  |               | 2. 접근 정책 판정                  |
  |               |<----------------|                    |
  |               | 3. 단일 패스 검사                  |
  |               |-------          |                    |
  |               |      |          |                    |
  |               |<------          |                    |
  |               | 4. 최적 경로 전달                  |
  |               |------------------------------------>|
  |               | 5. 지속적 위험 재평가             |
  |               |---------------->|                    |
  |               |<------------- 응답 -----------------|
  |<------------- 응답              |                    |
```

**동작 원리**

1. **신원·태세 검증**: IdP와 단말 상태를 결합한 신뢰 평가
2. **접근 정책 판정**: 신원·자원 맥락에 따른 최소 권한 결정
3. **단일 패스 검사**: 복호화한 트래픽의 SSE 병렬 검사
4. **최적 경로 전달**: SD-WAN 품질 측정에 따른 경로 선택
5. **지속적 위험 재평가**: 세션 중 행위와 단말 상태 재검증

#### 한줄 요약
- 검사 지점을 클라우드로 옮겨 지연과 장비 운영 부담을 덜어 낸 대신 트래픽 가시성과 정책 통제권을 사업자에 맡기게 되므로, SASE는 통제 위치를 신뢰 위탁과 맞바꾼 구조다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **SASE vs SSE vs 전통적 허브-앤-스포크(Hub-and-Spoke) 비교**:
  - SASE (Secure Access Service Edge): SD-WAN(네트워크) + SSE(보안) 완전 융합 클라우드 플랫폼.
  - SSE (Security Service Edge): 보안 서비스(SWG/CASB/ZTNA/FWaaS)만을 클라우드로 통합한 형태.
  - 전통적 경계 보안: 온프레미스 본사 방화벽으로 모든 트래픽을 VPN 백홀 집중 처리.

</details>

| 비교 항목 | 전통적 허브-앤-스포크 (VPN) | 보안 서비스 에지 (SSE) | 완벽한 융합 아키텍처 (SASE) |
|:---|:---|:---|:---|
| **트래픽 경로** | **본사 데이터센터 강제 백홀 (병목)**| Direct-to-Cloud (보안 중심) | **최적 지능형 Direct-to-Cloud (SD-WAN)**|
| **네트워크 제어** | MPLS 전용선 기반 고비용 라우팅 | 기존 네트워크 인프라 유지 (미관여)| **SD-WAN 기반 글로벌 패브릭 완전 통합** |
| **보안 서비스** | 본사 물리 하드웨어 방화벽/IPS | **클라우드 SWG, CASB, ZTNA, FWaaS**| **클라우드 SWG, CASB, ZTNA, FWaaS**|
| **접근 제어 모델** | 네트워크 망 전체 개방 (IP 기반) | 애플리케이션 단위 1:1 격리 (ZTNA)| **글로벌 제로 트러스트(ZTNA) 완전 통합**|
| **도입 적합 조직** | 온프레미스 레거시 단일 본사 | 기존 SD-WAN 보유 기업의 보안 혁신 | **글로벌 다국적 기업, 전면 클라우드 전환**|

#### 한줄 요약
- 전통 방식은 본사 백홀 병목, SSE는 보안 기능의 클라우드화, SASE는 네트워크와 보안의 완전 융합이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **MEF 117 (SASE 서비스 표준) 및 NIST SP 800-207 (제로 트러스트)**: SASE 품질 보증 및 제로 트러스트 아키텍처 구축 가이드라인.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 특정 SASE 클라우드 벤더의 단일 PoP 데이터센터 장애 발생 시 **전 세계 지사의 인터넷 연결 및 사내 업무망이 동시 블랙아웃 마비** | **Anycast 기반 멀티 리전 이중화(Alternative PoP) 아키텍처를 구성하고 BGP 자동 장애 전환(Failover) 구현** | 단일 PoP 장애 시 1초 이내 무중단 가용성 100% 보장 |
| 본사-지사 간 트래픽을 SASE 클라우드로 전면 이관 시 화상회의(Zoom) 등 실시간 트래픽에 **지연 시간(Latency) 및 지터가 발생하여 통화 품질 저하** | **MEF 117 준수, 음성/영상 트래픽에 대한 SD-WAN 우선순위 QoS(품질 보장) 정책 및 로컬 브레이크아웃(Local Breakout) 적용** | 화상회의 지연 30ms 이하 및 통신 품질 안정성 확보 |
| 사내 내부망을 안전지대로 맹신하여 사내 유선 LAN 접속자에 대해 **보안 검사를 생략했다가 내부 감염 PC를 통한 측면 이동(Lateral Movement) 발생** | **NIST SP 800-207 준수, 사내/사외 구분 없이 전사 모든 단말에 ZTNA 에이전트를 강제 적용하여 완전한 제로 트러스트 달성** | 내부 침해 시 측면 공격 및 랜섬웨어 확산 100% 차단 |

#### 한줄 요약
- Anycast 다중화로 장애를 막고, SD-WAN QoS로 실시간 품질을 보장하며, 전사 ZTNA로 내부 측면 이동을 차단한다.

## Ⅶ. 결론

- WAN 최적화가 필요하면 **SASE**, 기존 망 유지 시 **SSE** 선택

#### 한줄 요약
- SD-WAN과 SSE의 클라우드 단일 패스 융합을 통해 완벽한 SASE 제로 트러스트 아키텍처를 완성한다.
