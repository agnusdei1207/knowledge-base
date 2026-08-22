---
sidebar:
  order: 141
  label: "141. 보안 접근 서비스 경계(Secure Access Service Edge, SASE) 아키텍처"
  badge:
    text: "기출 · 70%"
    variant: note
title: "클라우드 네이티브 네트워크 및 보안 융합 아키텍처 : SASE 및 SSE (NIST SP 800-207 & MEF 117)"
date: "2026-08-22T08:15:00+09:00"
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
- 배경/필요성: 멀티 클라우드 확산과 하이브리드 근무(Work from Anywhere)의 일상화에 따라, 물리적 경계 기반 네트워크의 한계를 극복하고 사용자와 앱 간 최단 거리 보안 연결을 보증할 클라우드 네이티브 보안 모델 요구

#### 한줄 요약
- SASE는 SD-WAN 네트워크와 SSE 클라우드 보안 서비스를 단일 PoP 에지 플랫폼으로 융합 제공한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **SASE 3대 핵심 융합 축**:
  - **SD-WAN 기반 지능형 연결성 (Intelligent Routing)**: 애플리케이션 유형(음성, 비디오, 데이터)에 따라 최적의 광역 통신 경로를 동적 선택.
  - **SSE 기반 포괄적 클라우드 보안 (Unified Security Edge)**: SWG(웹 보호), CASB(SaaS 통제), ZTNA(비공개 앱 접근), FWaaS(L7 방화벽)를 단일 패스(Single-pass)로 검사.
  - **글로벌 분산 PoP 및 전용 백본 (Global PoP Fabric)**: 전 세계 주요 인터넷 교환 노드에 에지 거점을 배치하여 10ms 이내 초저지연 보장.

</details>

- **신원 및 맥락 기반 동적 정책(Identity-driven Contextual Policy)**: IP나 위치가 아닌 사용자 신원, 기기 무결성(컴플라이언스 상태), 접근 대상 데이터 민감도를 결합하여 실시간 인가
- **단일 패스 병렬 처리 아키텍처(Single-pass Parallel Architecture)**: 트래픽을 여러 보안 장비로 연속 전달(Chaining)하지 않고, PoP 메모리 내에서 복호화 후 복수의 보안 엔진이 1회 동시 검사하여 지연 시간 최소화
- **완벽한 클라우드 탄력성(Cloud-native Multi-tenant Elasticity)**: 하드웨어 증설 없이 트래픽 급증 시 글로벌 클라우드 인프라가 자동 오토스케일링 수행

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
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 1. 분산 엔드포인트 계층 (Remote Users, Branches & IoT Devices) ]       │
│  ├─ [ 재택/원격 사용자 ] ➔ 경량 클라우드 에이전트 (ZTNA Client)         │
│  └─ [ 지사/공장 브랜치 ] ➔ SD-WAN 에지 어플라이언스 (지능형 트래픽 분기) │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (가장 가까운 에지로 최단 경로 연결)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 2. 글로벌 분산 에지 거점 (Global SASE PoP Fabric / Single-Pass Engine)│
├───────────────────────────────────┬─────────────────────────────────────┤
│ [ 네트워크 서비스 (SD-WAN Services) ]│ [ 보안 서비스 (Security Services: SSE) ]│
│ ├─ 동적 경로 최적화 (SLA 기반)   │ ├─ ZTNA: 1:1 비공개 앱 암호 격리 터널 │
│ ├─ 패킷 복제 및 지터/손실 보정    │ ├─ CASB: SaaS API 가시성 및 DLP 통제  │
│ └─ 대역폭 통합 (인터넷 + 5G/MPLS) │ ├─ SWG & RBI: 웹 악성코드 격리 무해화│
│                                   │ └─ FWaaS: 클라우드 L7 애플리케이션 방화벽│
└───────────────────────────────────┴─────────────────────────────────────┘
                                     │ (신원 및 정책 검증)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 3. 중앙 통합 제어 플레인 (Unified Management & Identity/Context) ]    │
│  ├─ IdP 연동 (Entra ID, Okta) ➔ MFA 및 기기 신뢰도(Device Posture) 판정 │
│  └─ [ 단일 콘솔 정책 관리 ➔ 전 세계 PoP에 0.1초 내 동일 정책 동기화 ]  │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (인가된 애플리케이션 최단 연결)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 4. 대상 애플리케이션 및 데이터 계층 (Enterprise Apps & Multi-Cloud) ]  │
│  ├─ 엔터프라이즈 사내 데이터센터 (On-premise Private Apps)               │
│  └─ 퍼블릭 클라우드 IaaS(AWS/Azure) 및 SaaS 서비스(M365/Salesforce)     │
└─────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 엔드포인트가 가장 가까운 PoP로 연결되어 단일 패스 검사와 중앙 정책 판정을 거친 후 최적 경로로 앱에 연결되는 구조

| 컴포넌트 | 핵심 기능 및 역할 | 주요 기술 및 프로토콜 | 비고 |
|:---|:---|:---|:---|
| **SD-WAN** | 회선 품질(지연, 패킷 손실)을 실시간 측정하여 최적 경로로 패킷 분기 | Dynamic Multipath Optimization | Network |
| **ZTNA** | 명시적 인가 전까지 네트워크를 은폐(Darkening)하고 1:1 앱 터널 제공 | Software-Defined Perimeter (SDP) | Security |
| **CASB** | 인가/비인가 클라우드 SaaS(Shadow IT) 가시성 확보 및 데이터 유출 통제| API 연동, Inline Proxy, OAuth | Security |
| **SWG / RBI** | 악성 웹 URL 차단 및 위험 웹페이지를 클라우드 컨테이너에서 원격 렌더링| URL Filtering, Remote Browser Isolation| Security |
| **FWaaS** | L3~L7 심층 패킷 검사, 차세대 침입 방지(IPS), DNS 보안 일괄 수행 | Next-Gen Cloud Firewall, TLS Inspection| Security |
| **통합 PoP** | 전 세계 단일 홉(Single-hop) 연결을 보증하는 클라우드 분산 거점 | Anycast BGP Routing, 글로벌 백본 | Infrastructure |

#### 한줄 요약
- SD-WAN, ZTNA, CASB, SWG/RBI, FWaaS, 글로벌 통합 PoP 에지로 구성된다.

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
1. [지리적 근접 PoP 접속]
    ├─ 원격 근무자가 노트북 부팅 ➔ Anycast IP 기반 최단 거리 PoP(예: 서울 PoP) 자동 터널링
    └─ [지연시간 5ms 이내 연결 완료]
            │
            ▼
2. [신원 및 기기 태세 검증]
    ├─ IdP(Okta/Entra ID) SAML/OIDC 연동 ➔ 사용자 MFA 인증
    ├─ 단말 보안 점검 ➔ 백신 최신 업데이트 여부, 디스크 암호화(BitLocker) 확인
    └─ [신뢰도 충족 확인 ➔ 세션 개시 허용]
            │
            ▼
3. [단일 패스 복합 보안 검사 (SSE)]
    ├─ TLS 트래픽 1회 복호화 ➔ SWG(피싱 차단), CASB(DLP 검사), FWaaS(IPS) 병렬 검사
    └─ [요청된 사내 ERP 앱 접근 권한(ZTNA) 화이트리스트 대조 ➔ 통과]
            │
            ▼
4. [SD-WAN 최적 경로 전송]
    ├─ SASE 글로벌 백본망을 통해 AWS 서울 리전 ERP 서버로 1:1 다이렉트 패킷 전달
    └─ [지연 시간 및 패킷 손실 0% 유지]
            │
            ▼
5. [지속적 위험 평가 및 동적 차단]
    ├─ 세션 유지 중 사용자가 대용량 고객 DB 일괄 다운로드 시도 (이상 행위 탐지)
    ├─ 단말의 백신이 실시간 비활성화되는 상태 변화 발생
    └─ [즉각 세션 격리 및 인가 토큰 강제 회수(Step-up MFA 요구 또는 차단)]
```

**동작 원리**

1. **백홀 병목 제거**: 본사 데이터센터를 거치지 않고 PoP에서 클라우드 SaaS로 직접 통신(Direct-to-Cloud)
2. **단일 에이전트 통합**: 단말에 VPN, 백신, DLP 등 수십 개 에이전트를 설치하지 않고 단일 통합 SASE 에이전트로 단순화
3. **제로 트러스트 네트워크 은폐**: ZTNA를 통해 사내 네트워크 IP 대역 자체를 인터넷에서 완전히 숨겨 포트 스캐닝 차단
4. **지속적 적응형 보안(CARTA)**: 최초 1회 인증에 그치지 않고 마우스 클릭과 데이터 이동을 세션 내내 실시간 감시
5. **글로벌 통일 거버넌스**: 전 세계 모든 지사와 재택 사용자가 본사와 100% 동일한 보안 정책 룰셋을 실시간 적용

#### 한줄 요약
- 근접 PoP 접속, 신원/태세 검증, 단일 패스 SSE 검사, SD-WAN 최단 전송, 지속적 위험 평가 순으로 동작한다.

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

- 클라우드 네이티브 시대의 분산 인프라와 하이브리드 업무 환경을 지탱하는 차세대 엔터프라이즈 인프라의 표준인 **SASE 아키텍처**는 네트워크와 보안의 경계를 허문 패러다임의 대전환이며, 실무 구현 시 **MEF 117 및 NIST SP 800-207 국제 표준 기반의 아키텍처 정립**, **지능형 SD-WAN과 SSE 4대 보안 엔진의 단일 패스 융합**, **단말-PoP-클라우드 전 구간의 글로벌 Anycast 패브릭 구축**, **지속적 적응형 위험 평가(CARTA) 기반의 무결점 제로 트러스트 통제**를 통합 완성하여 최고 수준의 비즈니스 민첩성과 엔드투엔드 사이버 복원력을 완성

#### 한줄 요약
- SD-WAN과 SSE의 클라우드 단일 패스 융합을 통해 완벽한 SASE 제로 트러스트 아키텍처를 완성한다.
