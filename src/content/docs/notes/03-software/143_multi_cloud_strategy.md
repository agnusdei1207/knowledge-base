---
sidebar:
  order: 143
  label: "143. 멀티 클라우드 전략 (Multi Cloud Strategy)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "멀티 클라우드 전략 (Multi Cloud Strategy)"
date: "2026-08-14T01:19:00+09:00"
tags:
  - "notes-software"
weight: 143
extra:
  question_no: "143"
  source_status: "기출"
  source_history: "135회"
  priority: 70
  priority_note: "복수 클라우드의 종속•운영 통제가 최근 출제됨"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Multi-Cloud Strategy (멀티 클라우드 전략)**: 단일 CSP(AWS) 종속 위험(Vendor Lock-in)을 차단하고, 최적의 서비스 결합(Best-of-Breed) 및 장애 대응(DR)을 위해 2개 이상의 퍼블릭 클라우드(AWS + GCP + Azure)를 혼용 운용하는 클라우드 거버넌스 전략.
- **Vendor Lock-in (베타/베어 종속성)**: 특정 클라우드 사업자 특유의 프로프라이어터리 API 및 서비스에 지나치게 종속되어 다른 클라우드로의 이관이 불가능해지는 위험.
- **Best-of-Breed (최적 조합)**: 각 CSP의 가장 우수한 전용 서비스(AWS EC2 컴퓨팅, GCP BigQuery AI, Azure AD 보안)만을 선별 조합하는 아키텍처 사상.

</details>

- 정의/개념: 복수 CSP의 역할을 조합하는 **Multi-Cloud Strategy**
- 배경/필요성: 단일 CSP는 **서비스 종속•가격•규제•장애 범위** 집중

#### 한줄 요약

- 가게를 여러 곳 쓰는 것보다 무엇을 나누고 어떻게 바꿔 살지를 정하는 것이 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Cloud Agnostic Architecture (클라우드 중립적 아키텍처)**: 특정 CSP에 종속되지 않고 컨테이너(Docker/K8s), IaC(Terraform)를 통해 언제든 다른 클라우드로 즉시 이관 가능하도록 구축.

</details>

- **Vendor Lock-in 완화**: 대체 경로•계약 협상력 확보
- **Best-of-Breed Capabilities (AWS 인프라 + GCP BigQuery/AI 엔진 특화 조합)**
- **High Availability & Disaster Recovery (CSP 간 100% 장애 우회 DR 구축)**

#### 한줄 요약

- 예비 가게가 있어도 재고와 출입증을 맞추고 실제로 손님을 돌려보는 연습이 필요하다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Abstraction Layer (추상화 레이어)**: Kubernetes(CaaS), Terraform(IaC), OpenMetadata 등을 활용해 이종 CSP 간의 차이점을 은폐하고 단일 제어판으로 관리.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   Multi-Cloud Abstraction Architecture                 │
├────────────────────────────────────────────────────────────────────────┤
│ Unified Portal: [Terraform (IaC)]  [Kubernetes (K8s)]  [HashiCorp Vault│
├────────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────────┐  ┌────────────────────────┐                │
│  │   AWS (Primary Infra)  │  │ GCP (BigQuery & AI)    │                │
│  │   • EC2 / EKS / S3     │  │ • Vertex AI / BigQuery │                │
│  └────────────────────────┘  └────────────────────────┘                │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 하단의 AWS, GCP 이종 CSP 클라우드를 상단의 Terraform, Kubernetes 추상화 레이어로 묶어 제어하는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| **Workload Placement** | CSP별 기능•지역•규제에 따라 역할 배치 |
| **IaC•CaaS** | 공통 배포와 이식 가능한 실행 단위 제공 |
| **Unified Identity** | 사용자•서비스 신뢰와 권한 정책 연계 |
| **Network•GSLB** | CSP 간 연결•라우팅•장애전환 관리 |
| **Observability•FinOps** | 상태•SLO•비용•Egress 통합 관측 |

#### 한줄 요약

- 여러 가게를 쓰되 역할과 전환 방법을 미리 정한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Global Server Load Balancing (GSLB)**: DNS 기반으로 멀티 클라우드(AWS vs GCP) 간의 헬스체크를 수행하여 장애 발생 시 트래픽을 타 CSP로 자동으로 우회 렌더링.

</details>

```text
[주 CSP 장애]
      │
      ▼
1. 다중 신호 장애 판정
      │
      ▼
2. 데이터 복구점 확인
      │
      ▼
3. 보조 CSP 승격
      │
      ▼
4. GSLB 트래픽 전환
      │
      ▼
5. 정합성•성능 검증
```

### 동작 원리

1. **다중 신호 장애 판정**: 리전•앱•의존 서비스 실패 확인
2. **데이터 복구점 확인**: 보조 환경의 RPO•복제 지연 판정
3. **보조 CSP 승격**: 쓰기 권한과 의존 서비스를 활성화
4. **GSLB 트래픽 전환**: 점진적으로 사용자 요청 우회
5. **정합성•성능 검증**: 오류율•지연•중복 처리 확인

#### 한줄 요약

- 주 가게가 멈추면 복제된 마지막 재고를 확인한 예비 가게로 손님을 돌린다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Deployment Multiplicity**: 단일 CSP(Single), 온프레미스+퍼블릭(Hybrid), 2개 이상 퍼블릭 CSP(Multi).

</details>

| 비교 항목 | Single Cloud (AWS 전용) | Hybrid Cloud | Multi-Cloud |
|:---|:---|:---|:---|
| **CSP 개수** | **단 1개 (AWS 100%)** | 1개 퍼블릭 + 온프레미스 IDC | **2개 이상 (AWS + GCP + Azure)** |
| **사업자 종속** | 단일 CSP 기능에 집중 | CSP•온프레미스 결합 | 복수 CSP이나 공통 계층 종속 가능 |
| **운영 및 관리 비용** | 최저 (단일 통합 포털) | 중간 | **높음 (다중 기술 스택 인력 필요)**|
| **장애 복구력 (DR)** | 단일 CSP 리전 장애 시 위험 | IDC 복구 가능 | **CSP 수준의 전역 장애 우회** |

#### 한줄 요약

- 분할은 일을 나눠 맡기고 중복은 같은 일을 대신할 준비를 한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Cross-Cloud Egress Cost Danger**: AWS S3 데이터를 GCP BigQuery로 매일 전송할 때 발생하는 CSP 네트워크 이그레스 전송료(Egress Fee) 비용 폭탄.

</details>

| 3대 멀티 클라우드 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Data Egress Fee 폭탄**| CSP 간 대용량 데이터 잦은 이동 | **데이터 이동 최소화 및 타깃 CSP 내부 전처리**|
| **2. Operational Complexity**| AWS, GCP 전용 기술 지식 파편화 | **Kubernetes & Terraform 기반 기술 추상화** |
| **3. Security Policy Drift**| CSP별 IAM 권한 설정 불일치 | **HashiCorp Vault / Cloudflare 서비스 메시 통합** |

> 사례: **당근마켓 / 카카오 / 당근 AWS (앱 서비스) + GCP (BigQuery 및 AI) 멀티 클라우드 전략**

#### 한줄 요약

- 싼 분석 도구라도 데이터를 옮기는 요금과 시간이 더 크면 분할 이점이 사라진다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Multi-Cloud 수립 기준(Multi-Cloud Standards)**: Best-of-Breed 서비스 선별, Kubernetes Cloud Agnostic, Egress Fee 통제 및 GSLB DR에 의거한 체계.

</details>

- 독립 기능 조합•CSP DR 가치가 **운영•Egress 비용**보다 크면 채택

#### 한줄 요약

- 가게를 늘려 얻는 기능과 복원력이 재고 동기화·인력·이동 비용보다 커야 한다.
