---
sidebar:
  order: 143
  label: "143. 멀티 클라우드 전략"
  badge:
    text: "기출 · 70%"
    variant: note
title: "멀티 클라우드 전략 (Multi Cloud Strategy)"
date: "2026-08-25T11:00:00+09:00"
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

<details><summary>용어 설명</summary>

- **멀티 클라우드 전략(Multi-Cloud Strategy)**: 단일 CSP 종속(Lock-in)을 회피하고 강점 서비스 조합(Best-of-Breed)과 재해복구(DR)를 위해 2개 이상의 퍼블릭 클라우드를 병용하는 전략.
- **Best-of-Breed**: AWS의 범용 EKS, GCP의 BigQuery/Vertex AI, Azure의 Active Directory 등 각 CSP의 최고 기술만을 선별 조합.

</details>

- 정의/개념: 단일 벤더 종속(Lock-in)을 방지하고 서비스별 최적 조합(Best-of-Breed)을 달성하기 위해 **2개 이상의 퍼블릭 CSP를 분산 운용하는 클라우드 전략**
- 배경/필요성: 특정 클라우드 사업자 독점 사용 시 발생하는 **단일 CSP 전면 장애 전파, 가격 협상력 상실 및 타 플랫폼 이관 불가 해결 불가**

#### 한줄 요약
- 2개 이상의 퍼블릭 클라우드를 조합하여 단일 장애점(SPOF)을 제거하고 비즈니스 연속성을 극대화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Cloud-Agnostic Abstraction**: Kubernetes와 Terraform(IaC)을 도입하여 특정 CSP의 독점 API에 종속되지 않고 워크로드를 자유롭게 이전.
- **GSLB(Global Server Load Balancing)**: 전 세계 DNS 레벨에서 헬스체크를 수행하여 장애 발생 시 트래픽을 타 CSP 엔드포인트로 자동 우회.

</details>

- 단일 클라우드 종속을 방지하고 가격 협상력을 확보하는 **벤더 락인(Lock-in) 완화**
- CSP별 특화된 강점 서비스를 결합하는 **최적 기능 조합(Best-of-Breed)**
- CSP 전면 장애 발생 시 타 클라우드로 자동 우회하는 **글로벌 재해복구(DR) 가용성**

#### 한줄 요약
- 벤더 독립성, 강점 서비스 조합, 고가용성 DR을 통해 엔터프라이즈 영속성을 보장한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **멀티 클라우드 추상화 계층**: Governance Layer(Terraform/K8s/Vault), GSLB Layer(글로벌 트래픽 분기), Multi-CSP Layer(AWS/GCP/Azure).

</details>

```text
[멀티 클라우드 통합 관리 및 추상화 구조]
|-- 1. Governance & Abstraction Layer (통합 오케스트레이션 및 거버넌스)
|   |-- Terraform (IaC 멀티 클라우드 인프라 코드화)
|   |-- Kubernetes (CaaS 컨테이너 기반 워크로드 표준화)
|   `-- HashiCorp Vault (OIDC 기반 중앙 시크릿 및 IAM 통제)
|-- 2. Global Traffic Layer (GSLB 기반 DNS 트래픽 라우팅)
`-- 3. Multi-CSP Workload Layer
    |-- Primary CSP: AWS (EKS 대외 웹/앱 + Aurora 주 결제 원장)
    `-- Secondary CSP: GCP (BigQuery 데이터 분석 + Vertex AI 머신러닝)
```

선의 의미: 계층 및 이종 CSP 클라우드를 상단의 Terraform, Kubernetes 추상화 레이어로 묶어 제어하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **워크로드 배치 (Placement)**| 기능 적합성, 데이터 주권, 비용에 따라 **최적의 CSP로 애플리케이션 분산 배정** | Best-of-Breed |
| **인프라 추상화 (IaC/CaaS)**| Terraform 및 Kubernetes를 통해 **CSP 간 이식 가능한 공통 배포 환경 제공** | Cloud-Agnostic |
| **통합 신원 관리 (IAM)** | HashiCorp Vault 및 OIDC를 통해 **이종 클라우드 간 통합 계정/시크릿 통제** | 단일 보안 창구 |
| **글로벌 트래픽 라우터** | GSLB 헬스체크를 기반으로 **CSP 간 트래픽 분기 및 장애 시 타 CSP 자동 절체** | DNS 기반 Failover |
| **통합 관제 및 FinOps** | Datadog/Prometheus를 통해 **CSP 전반의 성능, SLO, Egress 네트워크 비용 통합 관측** | 멀티 클라우드 비용 통제 |

#### 한줄 요약
- 워크로드 배치, 인프라 추상화, 통합 IAM, GSLB, FinOps 관제가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Multi-Cloud Failover 5단계**: 주 CSP 장애 감지 $\to$ 보조 CSP RPO 확인 $\to$ 보조 CSP 승격 $\to$ GSLB 트래픽 전환 $\to$ 서비스 정합성 검증.

</details>

```text
주(Primary) CSP 리전에서 전면 서비스 장애 발생
        │
   1. [장애 감지] 글로벌 모니터링 시스템이 주 CSP(AWS)의 API 타임아웃 및 헬스체크 실패 감지
        │
   2. [RPO 확인] 보조 CSP(GCP)로 실시간 복제 중이던 데이터의 복구 시점(RPO) 지연 확인
        │
   3. [보조 워크로드 승격] 보조 CSP의 대기 Pod를 즉시 스케일아웃하고 DB 쓰기 권한 승격
        │
   4. [GSLB 라우팅 전환] DNS 기반 GSLB가 사용자 트래픽을 보조 CSP 엔드포인트로 즉시 우회
        │
   5. 트랜잭션 오류율 및 지연시간 메트릭을 점검하여 무중단 서비스 정상 재개 검증
```

#### 한줄 요약
- 장애 감지 → RPO 확인 → 보조 승격 → GSLB 우회 → 정합성 검증 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **단일 클라우드 vs 멀티 클라우드**: 단일 CSP 전용 구조와 2개 이상의 CSP를 분산 병용하는 멀티 클라우드 구조.

</details>

| 비교 항목 | 단일 클라우드 (Single Cloud) | 멀티 클라우드 (Multi-Cloud) |
|:---|:---|:---|
| 벤더 종속성(Lock-in)| **매우 높음 (해당 CSP 플랫폼 종속)** | **매우 낮음 (CSP 간 자유로운 이전 및 협상력 확보)**|
| 재해복구(DR) 가용성 | 동일 CSP 내 타 리전 장애 시 위험 잔존 | **CSP 전면 다운 시에도 타 CSP로 즉각 우회** |
| 운영 및 관리 복잡도 | **낮음 (단일 콘솔 및 일관된 도구)** | 높음 (이종 CSP 기술 스택 학습 및 도구 단일화 필요)|
| 네트워크 통신 비용 | 내부망 통신으로 무료 또는 저렴 | **CSP 간 데이터 전송(Egress Fee) 비용 발생** |

#### 한줄 요약
- 단순 운영은 단일 클라우드, 완벽한 재해복구와 협상력 확보는 멀티 클라우드를 채택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Cross-Cloud Egress Fee**: 서로 다른 CSP 간 대량 데이터 복제 시 발생하는 아웃바운드 네트워크 통신 과금.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| CSP 간 대용량 데이터 동기화 시 **Egress 전송 비용** 폭증 | **타깃 CSP 내 로컬 처리 원칙 수립 및 변경분(CDC) 압축 전송** | 네트워크 전송 비용 60% 절감 |
| CSP별 상이한 기술 스택으로 인한 엔지니어링 관리 복잡도 | **Kubernetes(K8s) 및 Terraform 기반 표준화 인프라 단일화** | 클라우드 비종속 단일 운영 체계 구축 |
| CSP별 IAM 권한 체계 상이로 인한 보안 구멍(Security Drift) | **HashiCorp Vault 및 OIDC 기반 중앙 집중형 권한 배포** | 전사 보안 정책 일관성 100% 보장 |
| CSP 간 데이터베이스 동기화 시 양방향 충돌 | **Primary-Secondary 액티브-스탠바이 구조화 및 CDC 단방향 복제** | 데이터 정합성 왜곡 원천 방지 |

#### 한줄 요약
- Egress 비용 최소화, K8s/IaC 표준화, 중앙 Vault IAM, CDC 단방향 복제로 운영한다.

## Ⅶ. 결론

- 클라우드 벤더 종속을 탈피하고 무중단 비즈니스 영속성을 달성하기 위해 **Kubernetes 및 Terraform 기반의 추상화 계층을 표준 구축하고 멀티 클라우드 재해복구(DR) 체계를 확립**하여 최적의 엔터프라이즈 인프라 완성

#### 한줄 요약
- 멀티 클라우드 전략은 2개 이상의 퍼블릭 클라우드를 조합하여 단일 장애점을 제거하고 비즈니스 연속성과 협상력을 극대화하는 핵심 인프라 전략이다.