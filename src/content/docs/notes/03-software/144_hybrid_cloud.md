---
sidebar:
  order: 144
  label: "144. 하이브리드 클라우드 (Hybrid Cloud)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "하이브리드 클라우드 (Hybrid Cloud)"
date: "2026-08-14T01:26:00+09:00"
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

<details><summary>용어 설명</summary>

- **Hybrid Cloud (하이브리드 클라우드)**: 자체 프라이빗 클라우드(On-Premise IDC, Private Cloud)와 공용 퍼블릭 클라우드(AWS, GCP Public Cloud)를 암호화 전용회선(AWS DirectConnect)이나 VPN으로 상호 통합 연결하여, 데이터와 워크로드를 보안 등급별로 유연하게 분산 배치하는 통합 아키텍처.
- **Data Sovereignty (데이터 주권)**: 금융/공공/의료 등 법률적 규제 데이터(개인정보, 금융 계정)를 반드시 국경 내부의 프라이빗 IDC에 저장 보존해야 하는 규제 준수 수칙.
- **AWS DirectConnect / Azure ExpressRoute**: 온프레미스 기업 IDC와 퍼블릭 클라우드 데이터센터 간을 1G~100Gbps 대역폭으로 잇는 전용 물리 회선.

</details>

- 정의/개념: Private•Public 환경을 연결•배치하는 **Hybrid Cloud**
- 배경/필요성: 규제 데이터 통제와 **탄력적 서비스 확장** 요구 상충

#### 한줄 요약

- 내부 금고는 유지하고 외부의 넓은 접수창구와 필요한 길만 연결한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Workload Partitioning**: 보안 우려가 큰 RDBMS Core DB는 Private에, 웹 프론트엔드/API 서버는 Public에 분산 배치.
- **Cloud Bursting**: 평시 온프레미스 가동, 트래픽 10배 폭발 시 퍼블릭 클라우드로 스케일아웃.

</details>

- 규제 데이터는 **Private 경계**에서 통제
- 정책•용량에 따라 **Public 자원**으로 확장
- **전용회선•VPN** 기반 경계 간 암호화 통신

#### 한줄 요약

- 두 장소를 잇는 순간 길의 지연과 끊김, 양쪽 장부의 차이까지 관리해야 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Hybrid Network Interconnect**: On-Premise IDC와 AWS VPC를 BGP 라우팅 전용회선(DirectConnect) 및 IPsec VPN으로 묶어 단일 사설망(10.x.x.x)처럼 통합.

</details>

```text
[Private Cloud] ───── [전용회선•VPN]
      │                       │
[Public Cloud] ────── [통합 IAM•관리]
```

| 구성요소 | 책임 |
|---|---|
| Private Cloud | **규제 데이터**•핵심 워크로드 통제 |
| Public Cloud | **탄력적 앱**•분석 워크로드 처리 |
| 전용회선•VPN | **라우팅•암호화**와 경로 이중화 |
| 통합 IAM•관리 | **신원•정책**과 관측•배포 통합 |

#### 한줄 요약

- 내부 금고와 외부 창구를 필요한 경로로 연결한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Hybrid Transit Gateway**: 온프레미스 인프라와 여러 퍼블릭 VPC 라우팅을 중앙에서 묶어 라우팅을 제어하는 가상 라우터.

</details>

```text
[하이브리드 요청]
        │
        ▼
1. 데이터•워크로드 분류
        │
        ▼
2. 배치 경계 결정
        │
        ▼
3. 연결•권한 확인
        │
        ▼
4. 경계 간 요청 처리
        │
        ▼
5. 상태•비용 감시
        │
        ▼
   [결과 반환]
```

### 동작 원리

1. **데이터•워크로드 분류**: 규제•지연•확장 요구 식별
2. **배치 경계 결정**: Private•Public 실행 위치 선택
3. **연결•권한 확인**: 경로•암호화•신원 정책 검증
4. **경계 간 요청 처리**: 승인된 데이터와 호출만 전달
5. **상태•비용 감시**: 성능•장애•사용량 지속 관측

#### 한줄 요약

- 외부 창구가 권한을 확인한 뒤 내부 금고에서 필요한 결과만 받아오고 양쪽 기록을 연결한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Hybrid Positioning**: 퍼블릭의 고성능/가성비와 프라이빗의 최고 보안성 2가지 장점만을 취합한 최상위 모델.

</details>

| 비교 항목 | Pure Public Cloud | Pure Private Cloud | Hybrid Cloud (하이브리드) |
|:---|:---|:---|:---|
| **데이터 보안/주권** | 사업자 책임 공유 | 자체 정책 중심 | **데이터별 경계 분리** |
| **트래픽 확장성** | 공급자 한도 내 탄력적 | 보유 용량에 종속 | **정책 기반 Bursting** |
| **네트워크 Latency**| 외부 경로 영향 | 내부 경로 중심 | **연결 구조별 상이** |
| **초기 구축 CAPEX** | 서비스별 비용 발생 | 인프라 구축 비용 | 기존•공용 자원 병행 |

#### 한줄 요약

- 하이브리드는 전용·공용 장소의 연결이고 멀티 클라우드는 여러 공급자를 쓰는 전략이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

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

<details><summary>용어 설명</summary>

- **Hybrid Cloud 수립 기준(Hybrid Standards)**: DirectConnect 전용회선, Cloud Bursting, Anthos/Outposts 통합 관리 및 CASB 보안 통제성에 의거한 체계.

</details>

- 규제•저지연 코어는 **Private**, 탄력적 앱•분석은 Public 배치

#### 한줄 요약

- 외부 자원의 이점이 두 장소를 잇고 함께 운영하는 비용보다 커야 한다.
