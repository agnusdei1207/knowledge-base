---
sidebar:
  order: 216
  label: "216. 플랫폼 엔지니어링 셀프서비스"
  badge:
    text: "기출 · 85%"
    variant: note
title: "플랫폼 엔지니어링 셀프서비스 (Platform Engineering Self-Service)"
date: "2026-08-25T11:00:00+09:00"
tags:
  - "notes-software"
weight: 216
extra:
  question_no: "216"
  source_status: "기출"
  source_history: "134회, 135회"
  priority: 85
  priority_note: "셀프서비스•골든 패스 설계가 반복 출제됨"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Platform Engineering (플랫폼 엔지니어링)**: 개발팀의 인지 부하를 줄이기 위해 내부 개발자 플랫폼(IDP)을 구축하여 인프라를 제품처럼 제공하는 규율.
- **Golden Path (골든 패스 / Paved Road)**: 보안과 아키텍처 모범 사례가 내장되어 개발자가 고민 없이 안전하게 배포할 수 있는 표준 경로.

</details>

- 정의/개념: 내부 개발자 플랫폼(IDP)을 통해 **인프라와 배포 파이프라인을 셀프서비스 골든 패스(Golden Path)로 제공하는 엔지니어링 패러다임**
- 배경/필요성: 인프라팀에 대한 수동 티켓 요청 및 승인 대기로 인한 **배포 리드타임 지연, 인프라 운영 병목 및 섀도우 IT 확산 해결 불가**

#### 한줄 요약
- Backstage 기반 개발자 포털과 Policy-as-Code 가드레일을 결합하여 티켓 없는 안전한 셀프서비스를 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Cognitive Load Reduction (인지 부하 감소)**: 복잡한 K8s YAML, 네트워크 보안 설정을 플랫폼 뒤로 추상화하여 비즈니스 로직에만 집중시키는 효과.
- **Policy-as-Code Guardrails**: Open Policy Agent(OPA) 등을 통해 개발자의 셀프서비스 신청이 규정에 맞는지 자동 검증하는 안전 장치.

</details>

- 개발자가 웹 포털에서 인프라와 배포 파이프라인을 즉시 발급받는 **노-티켓 셀프서비스**
- 복잡한 인프라 상세를 추상화하여 비즈니스 로직에 집중시키는 **개발자 인지 부하 감소**
- 보안 및 비용 규정을 코드로 강제하는 **Policy-as-Code 기반 자동 가드레일**

#### 한줄 요약
- 노-티켓 셀프서비스, 인지 부하 감소, Policy-as-Code 가드레일을 통해 개발 생산성을 극대화한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **IDP 4대 핵심 구조**: Developer Portal(Backstage 단일 진입점), Golden Path Templates(스캐폴딩), Policy Engine(OPA 가드레일), Control Plane(Crossplane 인프라 생성).

</details>

```text
[내부 개발자 플랫폼(IDP) 셀프서비스 및 프로비저닝 구조]
|-- 1. Developer Portal Layer (Spotify Backstage: 서비스 카탈로그, 템플릿 검색)
`-- 2. Golden Path Templates Layer (표준 Spring Boot/Node.js, Dockerfile, CI/CD 스캐폴딩)
`-- 3. Policy & Governance Gate Layer (Open Policy Agent OPA / Kyverno 가드레일)
`-- 4. Infrastructure Control Plane (Crossplane / Terraform Operator 선언적 IaC)
    |-- Kubernetes Namespace & EKS 클러스터 자원 자동 프로비저닝
    `-- AWS RDS PostgreSQL & S3 버킷 생성 및 GitHub Repo/ArgoCD 파이프라인 결합
```

선의 의미: 계층 및 개발자가 포털에서 골든 패스를 선택하면 정책 엔진이 가드레일을 심사한 후 제어 평면이 인프라와 GitOps 파이프라인을 자동 생성하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **개발자 포털 (Backstage)** | 서비스 카탈로그, **골든 패스 템플릿 검색, 자원 신청 및 전사 소유권 가시성 단일 제공** | 단일 웹 진입점 |
| **골든 패스 템플릿 (Templates)**| 보안, 로깅, CI/CD가 내장된 **표준 마이크로서비스 및 인프라 스캐폴딩 패키지 제공** | Paved Road 템플릿 |
| **정책 가드레일 (Policy)** | OPA/Rego를 통해 **신청된 자원의 보안 규정, 비용 한도, 권한 적합성을 실시간 자동 검증** | Policy-as-Code |
| **플랫폼 제어 평면 (Crossplane)**| 선언적 IaC를 실행하여 **K8s 클러스터, 데이터베이스, 스토리지 자원을 즉시 자동 프로비저닝**| 선언적 인프라 엔진 |
| **피드백 분석기 (Telemetry)** | 개발자 채택률, **배포 리드타임, 마찰 지표(Friction Metric)를 수집하여 플랫폼 개선** | DevEx 분석 |

#### 한줄 요약
- 개발자 포털, 골든 패스, 정책 가드레일, 제어 평면, 피드백 분석기가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **셀프서비스 프로비저닝 5단계**: 템플릿 선택 $\to$ OPA 가드레일 자동 검증 $\to$ Crossplane 자원 프로비저닝 $\to$ ArgoCD 배포 구성 $\to$ 카탈로그 자동 등록.

</details>

```text
개발자 신규 마이크로서비스 생성 요청
        │
   1. [템플릿 선택] Backstage 포털에서 'Spring Boot + RDS PostgreSQL' 골든 패스 선택
        │
   2. [정책 검증] OPA가 요청된 DB 인스턴스 크기(t4g.medium)와 비용이 팀 예산 내임을 자동 승인
   ┌────┴───────────────────────────┐
  정책 적합 (승인)                  정책 위반 (초과)
   │                                 │
3A. [자원 선언적 프로비저닝]        3B. [예외 신청 안내]
   Crossplane이 RDS와 EKS 네임스페이스 생성     관리자 수동 승인 요청 안내
   │                                 │
   ▼                                 │
4. [배포 파이프라인 자동 구성]       │
   GitHub Repo 생성 및 ArgoCD 연동   │
   │                                 │
   └────┬────────────────────────────┘
        ▼
   5. [카탈로그 등록] 서비스 API 문서와 소유자 메타데이터가 Backstage 포털에 즉시 등록 완료
```

#### 한줄 요약
- 템플릿 선택 → 정책 검증 → 자원 프로비저닝 → 배포 구성 → 카탈로그 등록 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **가드레일 셀프서비스 vs 티켓 기반 수동 발급 vs 완전 자율 방임**: 자동 가드레일(IDP), 수동 승인 대기(티켓팅), 무단 개발(섀도우 IT).

</details>

| 비교 항목 | 가드레일 셀프서비스 (IDP) | 티켓 기반 수동 발급 (Ticket-Based) | 완전 자율 방임 (Shadow IT) |
|:---|:---|:---|:---|
| 핵심 운영 방식 | **사전 검증된 골든 패스 + Policy 자동 승인** | **Jira 티켓 발행 $\to$ 인프라팀 수동 검토** | **개발자가 클라우드 콘솔에서 직접 수동 생성**|
| 자원 발급 리드타임 | **5분 이내 (완전 자동화)** | 수일 ~ 수주일 (인프라팀 병목) | 수 분 (즉시 생성 가능) |
| 보안 및 비용 통제 | **Policy-as-Code로 100% 자동 통제** | 인프라팀 검토로 높으나 인적 실수 가능 | **통제 전무 (보안 구멍 및 비용 낭비 폭증)** |
| 개발자 경험(DevEx) | **최고 (인지 부하 극소화, 셀프서비스)** | 최악 (긴 대기 시간, 마찰 발생) | 보통 (인프라 관리 부담 개발자 전가) |

#### 한줄 요약
- 표준 인프라는 IDP 셀프서비스, 복잡한 특수 예외는 티켓팅 심사, 방임형 섀도우 IT는 차단한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Escape Hatch (이스케이프 해치)**: 골든 패스가 지원하지 않는 특수 프레임워크가 필요할 때 플랫폼을 우회하여 합법적으로 수동 승인을 받는 경로.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 골든 패스의 지나친 강제로 특수 요구 개발팀의 반발 및 갈등 | **합법적 우회 승인 절차인 `이스케이프 해치(Escape Hatch)` 제공** | 표준화 거버넌스와 개발 자율성의 조화 |
| 셀프서비스 허용 후 개발자의 방치로 클라우드 유휴 비용 폭증 | **`FinOps 자동화` 연동(미사용 개발용 DB 야간 자동 셧다운)** | 클라우드 인프라 비용 30% 이상 절감 |
| 플랫폼 구축 후 개발자가 사용하지 않아 채택률(Adoption) 바닥 | **플랫폼 팀에 `전담 PM`을 배치하고 개발자 경험(DevEx) 설문 환류** | 플랫폼 자발적 채택률 90% 이상 달성 |
| 플랫폼 자체 장애 시 전사 개발 및 배포 전면 마비 | **플랫폼 제어 평면의 Multi-AZ 고가용성 및 로컬 상태 캐싱** | 플랫폼 장애 격리 및 비상 배포 보장 |

#### 한줄 요약
- 이스케이프 해치 마련, FinOps 비용 자동화, 제품 중심 PM 운영, 플랫폼 고가용성으로 운영한다.

## Ⅶ. 결론

- 대규모 엔터프라이즈 환경에서 DevOps의 이상을 실현하고 개발자 생산성을 극대화하기 위해 **Backstage 기반의 내부 개발자 플랫폼(IDP)과 검증된 골든 패스(Golden Path)를 전사 도입**하고, **Policy-as-Code 가드레일과 FinOps 비용 최적화**를 결합하여 티켓 없는 안전한 셀프서비스 엔지니어링 완성

#### 한줄 요약
- 플랫폼 엔지니어링 셀프서비스는 골든 패스 템플릿과 Policy-as-Code 가드레일을 통해 인지 부하를 줄이고 배포 속도를 극대화하는 핵심 인프라 패러다임이다.