---
sidebar:
  order: 142
  label: "142. 클라우드 배포 모델: 퍼블릭•프라이빗•하이브리드•멀티 (Cloud Deployment Models)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "클라우드 배포 모델: 퍼블릭•프라이빗•하이브리드•멀티 (Cloud Deployment Models)"
date: "2026-08-14T01:12:00+09:00"
tags:
  - "notes-software"
weight: 142
extra:
  question_no: "142"
  source_status: "기출"
  source_history: "131회"
  priority: 70
  priority_note: "배포 위치별 통제•비용 비교가 설계 기준임"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Cloud Deployment Models (클라우드 배포 모델)**: 클라우드 인프라의 물리적/논리적 위치, 점유 독점성, 연결 형태에 따라 분류하는 4대 배포 환경 (Public, Private, Hybrid, Multi-Cloud).
- **Public Cloud**: CSP(AWS, Azure, GCP)가 멀티테넌시(Multi-Tenancy) 형태로 일반 대중에게 인프라 자원을 빌려주는 공개형 클라우드.
- **Private Cloud**: 단일 기업 전용 온프레미스 IDC 또는 온프레미스 전용 랙(AWS Outposts) 기반의 독점적 보안 클라우드.
- **Hybrid & Multi-Cloud**: Hybrid는 On-Premise Private와 Public의 이종 결합, Multi-Cloud는 AWS+GCP 등 2개 이상의 이종 퍼블릭 CSP 병용 전략.

</details>

- 정의/개념: 위치•점유•사업자 조합의 **Cloud Deployment Models**
- 배경/필요성: 워크로드마다 **규제•지연•탄력성•비용** 요구 상충

#### 한줄 요약

- 공용 건물·전용 건물 중 어디에 업무를 둘지, 여러 건물을 어떻게 연결할지 정한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Multi-Tenancy vs Single-Tenancy**: 퍼블릭은 자원을 다수가 분할 점유(Multi), 프라이빗은 단일 기업이 물리적/논리적 100% 독점(Single).

</details>

- **Public Cloud (Elastic Auto-scaling & CAPEX $\rightarrow$ OPEX 비용 전환)**
- **Private Cloud**: 전용 자원•운영 통제와 자체 책임
- **Hybrid / Multi-Cloud (Cloud Bursting, Vendor Lock-in 방지 및 DR 고가용성)**

#### 한줄 요약

- 장소를 늘리면 선택지는 많아지지만 출입증·도로·장부·요금도 함께 관리해야 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **AWS DirectConnect / VPN**: On-Premise Private IDC와 AWS Public Cloud 간의 전용회선(DirectConnect)을 뚫어 이종 환경을 안전하게 연결.

</details>

| 구성요소 | 책임 |
|:---|:---|
| Public Cloud | 공유 CSP 자원의 탄력적 서비스 제공 |
| Private Cloud | 단일 조직 전용 자원과 통제 제공 |
| Hybrid Cloud | Private•Public 간 배치•연결•복구 조정 |
| Multi-Cloud | 복수 CSP의 역할•정책•비용 통합 관리 |

#### 한줄 요약

- 공용·전용 건물에 업무를 배치하고 출입증과 연결 도로를 함께 관리한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Cloud Bursting**: 평시에는 온프레미스 Private Cloud만 쓰다가, 이벤트 시 트래픽이 평시의 10배로 폭증하면 퍼블릭 클라우드(Public)로 자동으로 넘어가 스케일아웃(Burst)하는 기법.

</details>

```text
[워크로드 요구]
      │
      ▼
1. 데이터•규제 분류
      │
      ▼
2. 지연•탄력성 평가
      │
      ▼
3. 배치 모델 선택
      │
      ▼
4. 연결•IAM•복구 설계
      │
      ▼
5. 장애•비용 검증
```

### 동작 원리

1. **데이터•규제 분류**: 주권•민감도•감사 의무 식별
2. **지연•탄력성 평가**: 사용자 위치•부하 변동•용량 예측
3. **배치 모델 선택**: Public•Private•Hybrid•Multi 결정
4. **연결•IAM•복구 설계**: 경로•신뢰•상태 동기화 정의
5. **장애•비용 검증**: 단절•Egress•복구 시나리오 시험

#### 한줄 요약

- 공용 접수창구가 전용 금고의 필요한 결과만 받아오고 양쪽 기록을 같은 거래 번호로 묶는다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Deployment Model Selection**: 데이터 보안 규제성, 트래픽 변동성, 비용 예격성 3가지 축으로 배포 모델 최종 판정.

</details>

| 비교 항목 | Public Cloud | Private Cloud | Hybrid Cloud | Multi-Cloud |
|:---|:---|:---|:---|:---|
| 자원 점유 방식 | Multi-Tenant | **Single-Tenant (독점)** | 혼합형 | Multi-CSP |
| 비용 모델 | OPEX (종량제) | **CAPEX (초기 투자)** | CAPEX + OPEX | OPEX |
| 보안 및 규제 | CSP 통제와 고객 설정 | 전용 통제와 자체 책임 | 경계 간 통제 필요 | CSP별 정책 통합 필요 |
| 운영 복잡도 | **최저 (CSP가 전담)** | 높음 (자체 인력 필요) | **높음 (이종 망 관리)** | **최고 (멀티 솔루션)**|

#### 한줄 요약

- 하이브리드는 공용·전용 장소의 조합, 멀티 클라우드는 여러 임대업체를 쓰는 전략이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **데이터 아웃바운드 비용(Egress Fee Risk)**: 하이브리드 및 멀티 클라우드 환경에서 클라우드 서비스 제공자(CSP) 간 또는 온프레미스로의 대용량 데이터 전송 시 발생하는 네트워크 전송 비용 위험.
- **통합 계정 관리(Federated IAM)**: 서로 다른 클라우드 환경의 접근 제어 정책과 사용자 인증을 단일 창구로 일원화하는 체계.
- **클라우드 버스팅(Cloud Bursting)**: 프라이빗 클라우드 용량 초과 시 퍼블릭 클라우드 자원을 동적으로 확장 활용하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 이종 클라우드 간 데이터 이동에 따른 전송 비용 급증 | 데이터 상주 영역 최적화 및 전용선(Direct Connect) 구축 | **네트워크 전송 비용 절감** |
| 클라우드별 인증 체계 상이로 인한 보안 관리 복잡성 | HashiCorp Vault 및 OIDC 기반 통합 IAM 구축 | **중앙 집중형 접근 제어** |
| 프라이빗 클라우드 자원 고갈 시 서비스 지연 | Kubernetes 기반 **클라우드 버스팅** 연계 구성 | **유연한 처리 용량 확보** |

> 요약: 규제 데이터와 대외 서비스를 분리하고 전용선과 통합 IAM으로 비용과 보안 위험을 통제.

#### 한줄 요약

- 데이터 전송 비용과 보안 정책을 표준화하여 하이브리드·멀티 클라우드 운영 안정성을 확보한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **배포 모델 수립 기준(Deployment Model Standards)**: 보안 규제성, 트래픽 유연성, 전송 비용 및 확장성을 종합 고려하여 최적 클라우드 배포 모델을 선정하는 기준.

</details>

- 탄력성은 **퍼블릭**, 전용 통제는 **프라이빗**, 병행 요구는 **하이브리드** 선택

#### 한줄 요약

- 장소를 늘리기 전에 왜 나누는지와 끊겼을 때 버틸 수 있는지를 증명해야 한다.
