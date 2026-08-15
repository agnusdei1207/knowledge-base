---
sidebar:
  order: 53
  label: "053. CI/CD 파이프라인 (CI/CD Pipeline)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "CI/CD 파이프라인 (CI/CD Pipeline)"
date: "2026-08-13T15:36:00+09:00"
tags:
  - "notes-software"
weight: 53
extra:
  question_no: "053"
  source_status: "기출"
  source_history: "120회"
  priority: 50
  priority_note: "120회 기출, 빌드•시험•배포 자동화"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Continuous Integration (CI, 지속적 통합)**: 개발자들이 수시로 소스코드를 중앙 저장소에 통합하고, 자동화된 빌드 및 정적 분석, 단위 테스트를 실행하여 결함을 조기에 발견하는 과정.
- **Continuous Delivery (CD, 지속적 전달)**: CI 과정을 통과한 소프트웨어를 언제든지 검증/운영 환경으로 프로덕션 릴리스할 수 있도록 준비(Staging 준비 완료)해 두는 수동 승인형 자동화 단계.
- **Continuous Deployment (CD, 지속적 배포)**: 모든 품질 게이트(Quality Gate) 테스트를 통과한 소스코드가 사람의 개입 없이(No Human Touch) 실운영(Prod) 환경으로 자동 배포 완료되는 완결형 단계.

</details>

- 정의/개념: 개발자의 소스코드 커밋부터 컴파일, 테스트, 정적 분석, 컨테이너 빌드 및 실운영 환경 배포까지 전 과정을 자동화 파이프라인으로 연결한 **CI/CD Pipeline**
- 배경/필요성: 수동 빌드•배포는 **환경 편차•누락•복구 지연** 유발

#### 한줄 요약

- 변경 통합•검증•승격을 연결한 CI/CD 파이프라인이 핵심이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Pipeline as Code (PaC)**: 파이프라인 빌드/배포 절차를 GUI 클릭이 아닌, `Jenkinsfile` 또는 `.github/workflows/ci.yml` 형태의 코드 형태로 선언하여 Git 버전 관리하는 방식.
- **Quality Gate**: SonarQube 정적 코드 분석 점수, 코드 커버리지(e.g., Min 80%), 보안 취약점 패스 여부를 검증하여 통과 못 하면 파이프라인을 즉시 중단(Fail-Fast)시키는 차단벽.

</details>

- **Fail-Fast** 원칙 기반 자동 단위•통합 테스트 및 정적 분석
- **Pipeline as Code (PaC)** 선언식 파이프라인을 통한 버전 통제
- **Quality Gate** 통과 및 불변 산출물(**Immutable Artifact**) 생성/저장

#### 한줄 요약

- 조기 검증, 불변 아티팩트, 품질 게이트, 추적성이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Artifact Repository (산출물 저장소)**: CI 과정에서 빌드 완료된 최종 실행 바이너리(Jar, War) 및 컨테이너 이미지(Docker Image)를 버저닝하여 보관하는 전용 저장소 (e.g. Nexus, JFrog, Harbor).

</details>

```text
[소스 저장소 (Git)]
       | (Webhook / Trigger)
[파이프라인 실행기 (Runner)] ──► [빌드 & 테스트 & 정적분석]
       |
 [품질 게이트 (Quality Gate)]
       | (Pass)
[아티팩트 저장소 (Harbor/Nexus)]
       |
 [배포 제어기 (ArgoCD/K8s)] ──► [운영 환경 (Prod)]
```

선의 의미: Git 코드 커밋 시 Webhook이 Runner를 구동하여 빌드/테스트 후 Quality Gate 검증을 거쳐 Artifact 저장소 기재 및 K8s로 최종 배포되는 파이프라인 구조.

| 구성요소 | 책임 |
|:---|:---|
| 소스 저장소 (Git) | 변경 원본과 파이프라인 정의 보관 |
| 파이프라인 실행기 (Runner) | 격리 작업 공간에서 단계 실행 |
| 빌드•테스트•정적분석 | 실행물 생성과 기능•보안 검증 |
| 품질 게이트 (Quality Gate) | 정책 기준에 따라 승격 허용 판정 |
| 아티팩트 저장소 (Harbor/Nexus) | 불변 실행물과 출처•버전 보관 |
| 배포 제어기 (ArgoCD/K8s) | 승인 버전을 대상 환경에 승격 |
| 운영 환경 (Prod) | 배포 버전 실행과 상태•SLO 관측 |

#### 한줄 요약

- 저장소•실행기•게이트•배포 제어기의 연결이 핵심이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **GitOps (ArgoCD)**: Git 리포지토리를 시스템 상태의 유일한 진실의 원천(Single Source of Truth)으로 삼아, K8s 매니페스트 변경 시 ArgoCD가 클러스터 상태를 자동 동기화하는 배포 패러다임.

</details>

```text
┌──────────────────────────────┐
│ Git Push / Pull Request      │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 빌드•테스트 실행          │
│ 2. 품질 게이트 판정          │
│ 3. 불변 아티팩트 생성        │
│ 4. 아티팩트 저장소 게시      │
│ 5. 승인 버전 배포            │
└──────────────┬───────────────┘
               ▼
       [배포 결과•상태 관측]
```

### 동작 원리

1. **빌드•테스트 실행**: Runner가 컴파일•시험•정적 분석 수행.
2. **품질 게이트 판정**: 정책 기준 미달 변경의 승격 차단.
3. **불변 아티팩트 생성**: 커밋 식별자를 포함한 실행물 생성.
4. **아티팩트 저장소 게시**: 검증된 실행물과 메타데이터 보관.
5. **승인 버전 배포**: 승인 정책에 따라 대상 환경으로 승격.

#### 한줄 요약

- 변경 감지•실행부터 승인 버전 승격까지의 자동 검증 흐름이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Continuous Delivery vs Continuous Deployment**: Delivery는 Staging 통과 후 Production 배포 전 "사람의 수동 승인(Manual Gate)" 단계 존재, Deployment는 수동 개입 없이 자동 Prod 배포.

</details>

| 비교 항목 | Continuous Integration (CI) | Continuous Delivery (CD-Delivery) | Continuous Deployment (CD-Deployment) |
|:---|:---|:---|:---|
| 자동화 범위 | 소스 빌드 ~ 테스트 완결 | **운영 배포 가능 상태까지 자동 준비** | **품질 게이트 통과 변경을 운영까지 자동 반영** |
| 수동 승인 여부 | 없음 | **운영 승격 전 수동•정책 승인 가능** | **정책에 따라 자동 운영 승격** |
| 적합한 환경 | 모든 소프트웨어 프로젝트 | 엔터프라이즈, 금융/의료 시스템 | SaaS 서비스, 모바일/웹 서비스 |

#### 한줄 요약

- CI는 통합, 전달은 배포 준비, 배포는 운영 자동 반영이 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Flaky Test**: 코드 결함이 없음에도 네트워크 지연이나 멀티스레드 race condition으로 성공과 실패를 무작위 반복하는 불안정 테스트 (파이프라인 신뢰성 파손 요소).

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 파이프라인 피드백 지연 | **캐시•병렬화**와 변경 범위 기반 시험 | 검증 신뢰도를 유지하며 리드타임 단축 |
| **Flaky Test**로 인한 CI 빌드 무조건 실패 방치 | Flaky 테스트 격리(Quarantine) 및 격리 트래킹 리팩토링 | CI 빌드 신뢰도 회복 |
| CI 파이프라인 스크립트에 AWS Secret Key 노출 | **HashiCorp Vault / OIDC (OpenID Connect)** 연동 | 장기 비밀키 저장 제거 |

> 사례: **GitHub Actions + SonarQube + Harbor + ArgoCD GitOps** 표준 파이프라인 체계 구축

#### 한줄 요약

- 불변 아티팩트, 단계 배포, 복귀에 기반한 배포 통제가 핵심이다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **CI/CD 파이프라인 구축 기준(CI/CD Pipeline Build Standards)**: 테스트 자동화율, 배포 위험도 및 PaC(Pipeline as Code) 도입에 의거한 체계.

</details>

- 규제 승인 환경은 **Continuous Delivery**, 자동 승격 환경은 **Deployment** 선택

#### 한줄 요약

- 승인 필요성에 맞는 자동화된 전달 범위와 지속적 배포 여부를 정하는 것이 핵심이다.
