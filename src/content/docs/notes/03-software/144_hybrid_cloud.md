---
sidebar:
  order: 144
  label: "144. 하이브리드 클라우드 (Hybrid Cloud)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "하이브리드 클라우드 (Hybrid Cloud)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 144
extra:
  question_no: "144"
  source_status: "기출"
  source_history: "135회"
  priority: 70
  priority_note: "공용•사설 환경 연결과 책임 분리가 핵심임"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Hybrid Cloud (하이브리드 클라우드)**: 자체 프라이빗 클라우드(On-Premise IDC, Private Cloud)와 공용 퍼블릭 클라우드(AWS, GCP Public Cloud)를 암호화 전용회선(AWS DirectConnect)이나 VPN으로 상호 통합 연결하여, 데이터와 워크로드를 보안 등급별로 유연하게 분산 배치하는 통합 아키텍처.
- **Data Sovereignty (데이터 주권)**: 금융/공공/의료 등 법률적 규제 데이터(개인정보, 금융 계정)를 반드시 국경 내부의 프라이빗 IDC에 저장 보존해야 하는 규제 준수 수칙.
- **AWS DirectConnect / Azure ExpressRoute**: 온프레미스 기업 IDC와 퍼블릭 클라우드 데이터센터 간을 1G~100Gbps 대역폭으로 잇는 전용 물리 회선.

</details>

- 정의/개념: 온프레미스 프라이빗 클라우드의 100% 데이터 주권 보안성과 퍼블릭 클라우드의 유연한 무제한 확장성을 전용회선(DirectConnect)으로 결합한 통합 아키텍처인 **Hybrid Cloud**
- 배경/필요성: 금융/공공 기관의 데이터 외부 유출 금지 법적 규제(Private) 준수와 대국민 웹/앱 이벤트의 오토스케일링(Public) 요구성 동시에 수용 요구

#### 한줄 요약

- 내부 금고는 유지하고 외부의 넓은 접수창구와 필요한 길만 연결한다.

## Ⅱ. 특징 (Hybrid Cloud 3대 핵심 운용 사상)

<details><summary>핵심 용어</summary>

- **Workload Partitioning**: 보안 우려가 큰 RDBMS Core DB는 Private에, 웹 프론트엔드/API 서버는 Public에 분산 배치.
- **Cloud Bursting**: 평시 온프레미스 가동, 트래픽 10배 폭발 시 퍼블릭 클라우드로 스케일아웃.

</details>

- **Regulatory Compliance & Data Sovereignty (민감 데이터의 온프레미스 IDC 완전 보존)**
- **Cloud Bursting Capability (트래픽 폭증 시 퍼블릭 클라우드로 즉시 자동 스케일아웃)**
- **Seamless Secure Connectivity (DirectConnect / IPsec VPN 기반 암호화 통신)**

#### 한줄 요약

- 두 장소를 잇는 순간 길의 지연과 끊김, 양쪽 장부의 차이까지 관리해야 한다.

## Ⅲ. 구조 및 구성요소 (Hybrid Cloud 3대 레이어 파이프라인)

<details><summary>핵심 용어</summary>

- **Hybrid Network Interconnect**: On-Premise IDC와 AWS VPC를 BGP 라우팅 전용회선(DirectConnect) 및 IPsec VPN으로 묶어 단일 사설망(10.x.x.x)처럼 통합.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Hybrid Cloud Topology                           │
├────────────────────────────────────────────────────────────────────────┤
│ [On-Premise Private IDC] ◄─── (AWS DirectConnect) ───► [AWS Public Cloud]│
│  • Main Oracle Core DB         Dedicated Line         • Elastic App Web│
│  • Financial PII Vault         10Gbps Latency<2ms     • AI Analytics   │
├────────────────────────────────────────────────────────────────────────┤
│ Control Plane: [HashiCorp Vault (IAM)]  [Kubernetes Anthos / Outposts] │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 데이터 주권이 필요한 Core DB는 Private IDC에 두고, 웹/앱 서비스는 DirectConnect 전용회선을 경유하여 Public Cloud와 초저지연 연동되는 구조.

| 구성요소 (Element) | 역할 및 구현 기술 | 실무 핵심 포인트 |
|:---|:---|:---|
| **Private Data Center**| **주민번호, 결제 정보 등 1급 민감 DB 보존** | **Oracle, PostgreSQL RDBMS** |
| **Public Cloud Region**| **웹/앱 API, AI/ML 학습, 대국민 서빙 렌더링** | **AWS EKS, EC2, Lambda** |
| **Dedicated Network** | **Private과 Public을 잇는 dedicated 파이프** | **AWS DirectConnect (2ms 이내)** |
| **Hybrid Management** | **온프레미스와 퍼블릭을 단일 쿠버네티스로 제어**| **Google Anthos, AWS Outposts** |

#### 한줄 요약

- 내부 금고와 외부 창구를 필요한 경로로 연결한다.

## Ⅳ. 흐름도 (Hybrid Cloud Data Routing & Security 흐름)

<details><summary>핵심 용어</summary>

- **Hybrid Transit Gateway**: 온프레미스 인프라와 여러 퍼블릭 VPC 라우팅을 중앙에서 묶어 라우팅을 제어하는 가상 라우터.

</details>

```text
[Public App (AWS EC2)] ──► [Transit Gateway] ──► [DirectConnect (2ms)] ──► [Private Core DB (Oracle)]
```

### 동작 원리

1. **User Request**: 대국민 앱 요청이 AWS EC2 퍼블릭 웹 서버로 수신.
2. **Secure Query**: 결제 승인을 위해 EC2가 사설 DirectConnect 망을 통해 온프레미스 Private IDC Oracle DB 조회.
3. **Encrypted Return**: 결과만 암호화 수신받아 유저에게 즉시 서빙 표출 (**Hybrid Cloud 완결**).

#### 한줄 요약

- 외부 창구가 권한을 확인한 뒤 내부 금고에서 필요한 결과만 받아오고 양쪽 기록을 연결한다.

## Ⅴ. 종류 및 비교 (Pure Public vs Pure Private vs Hybrid Cloud)

<details><summary>핵심 용어</summary>

- **Hybrid Positioning**: 퍼블릭의 고성능/가성비와 프라이빗의 최고 보안성 2가지 장점만을 취합한 최상위 모델.

</details>

| 비교 항목 | Pure Public Cloud | Pure Private Cloud | Hybrid Cloud (하이브리드) |
|:---|:---|:---|:---|
| **데이터 보안/주권** | 보통 (CSP 표준 보안) | **최상 (물리적 유출 0%)** | **최상 (민감 데이터는 Private 보존)** |
| **트래픽 확장성** | **무제한 (Auto-scaling)** | 제한적 (물리 서버 인프라 한계) | **유연함 (Cloud Bursting 활용)** |
| **네트워크 Latency**| 상 (인터넷 통신) | **최상 (로컬 LAN 통신)** | **상 (DirectConnect 2ms 이내 통신)** |
| **초기 구축 CAPEX** | **0원** | 매우 비쌈 (자체 서버 구입) | 중간 (기존 IDC 활용 + Cloud) |

#### 한줄 요약

- 하이브리드는 전용·공용 장소의 연결이고 멀티 클라우드는 여러 공급자를 쓰는 전략이다.

## Ⅵ. 실무 고려사항 및 대책 (하이브리드 클라우드 3대 구축 난제)

<details><summary>핵심 용어</summary>

- **Split-Brain Risk in Data Sync**: 온프레미스 DB와 퍼블릭 DB 간 네트워크 단선 시 양쪽에서 CUD가 각자 발생하여 데이터 정합성이 깨지는 현상.

</details>

| 3대 하이브리드 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. DirectConnect Line Fail**| 전용회선 공사 중 물리적 단선 사고 발생 | **IPsec VPN 자동 백업 경로 (Backup Route) 이중화** |
| **2. Cross-Boundary Latency**| 온프레미스와 퍼블릭 잦은 API 핑퐁 호출| **퍼블릭 캐싱 레이어(Redis) 구축으로 쿼리 차단** |
| **3. Hybrid IAM Governance**| 온프레미스 LDAP과 AWS IAM 계정 불일치| **Azure AD / Okta SSO 기반 계정 연동 (SAML/OIDC)**|

> 사례: **카카오뱅크 / KB국민은행 / 삼성전자 하이브리드 클라우드 전용회선 아키텍처**

#### 한줄 요약

- 고객 금고와 외부 창구 사이의 길이 끊기거나 느려질 때도 안전하게 처리되는지 확인한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Hybrid Cloud 수립 기준(Hybrid Standards)**: DirectConnect 전용회선, Cloud Bursting, Anthos/Outposts 통합 관리 및 CASB 보안 통제성에 의거한 체계.

</details>

- **Hybrid Cloud 수립 기준**에 따라 금융/엔터프라이즈 모던 클라우드 구축 시 **Hybrid Cloud & AWS DirectConnect** 필수 적용

#### 한줄 요약

- 외부 자원의 이점이 두 장소를 잇고 함께 운영하는 비용보다 커야 한다.
