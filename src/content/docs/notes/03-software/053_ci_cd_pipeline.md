---
sidebar:
  order: 53
  label: "053. CI/CD 파이프라인"
  badge:
    text: "기출 · 50%"
    variant: note
title: "CI/CD 파이프라인 (CI/CD Pipeline)"
date: "2026-08-26T09:40:00+09:00"
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

- **CI/CD 파이프라인**: 지속적 통합(Continuous Integration)과 지속적 제공/배포(Continuous Delivery/Deployment)를 자동화한 소프트웨어 전달 체계.
- **불변 아티팩트(Immutable Artifact)**: 한 번 빌드되어 테스트를 통과한 컨테이너 이미지를 수정 없이 모든 환경(Dev, Stg, Prod)에 동일하게 배포하는 원칙.

</details>

- 정의/개념: 소스 코드 커밋부터 **자동 빌드·테스트(CI) 및 품질 게이트 통과 후 불변 아티팩트 배포(CD)** 를 수행하는 소프트웨어 전달 파이프라인
- 배경/필요성: 수동 빌드·배포 시 발생하는 **인적 오류(Human Error) 및 릴리즈 지연과 결함 늑장 발견 위험 해결 불가**

#### 한줄 요약
- 코드 커밋에서 운영 배포까지 전 단계를 자동화하여 신속하고 안정적인 소프트웨어 전달을 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Fail-Fast**: 결함이나 테스트 실패 발생 시 파이프라인을 즉시 중단하여 결함의 하위 단계 전파를 차단하는 원칙.
- **PaC(Pipeline as Code)**: Jenkinsfile, GitHub Actions YAML 등 파이프라인 설정을 소스 코드와 함께 Git으로 버전 관리하는 방식.

</details>

- 결함 발견 즉시 파이프라인을 중단하고 피드백을 전달하는 **Fail-Fast** 원칙
- 배포 파이프라인 정의를 코드로 버전 관리하는 **Pipeline as Code (PaC)**
- **품질 게이트(Quality Gate)** 검증을 거친 **불변 아티팩트(Immutable Container Image)** 환경별 배포

#### 한줄 요약
- Fail-Fast 원칙, Pipeline as Code, 불변 아티팩트를 통해 일관된 배포 신뢰성을 확보한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **품질 게이트(Quality Gate)**: SonarQube 등에서 코드 커버리지, 코드 냄새, 보안 취약점 기준을 검사하여 미달 시 빌드를 강제 중단하는 관문.

</details>

```text
[CI/CD 파이프라인 아키텍처]
|-- 소스 저장소 (Git Repository: GitHub / GitLab - Webhook 트리거)
|-- CI 빌드 및 테스트 계층 (GitHub Actions / Jenkins Runner)
|   |-- 소스 코드 컴파일 & 종속성 패키징
|   `-- 단위 테스트 (Unit Test) & 통합 테스트 (Integration Test)
|-- 품질 게이트 계층 (Quality Gate: SonarQube 정적 분석, Trivy 보안 취약점 스캔)
|-- 아티팩트 저장소 (Artifact Registry: Harbor / ECR - 불변 도커 이미지 저장)
`-- CD 배포 제어 계층 (ArgoCD / Spinnaker)
    |-- 스테이징 환경 배포 (자동)
    `-- 프로덕션 환경 배포 (Delivery: 수동 승인 / Deployment: 완전 자동화)
```

선의 의미: 계층 및 단계별 CI/CD 자동화 파이프라인

| 구성요소 | 책임 |
|:---|:---|
| 소스 저장소 (Git) | 소스 코드 및 파이프라인 정의(**Pipeline as Code**) 형상 관리 |
| CI 러너 (Runner) | 격리된 컨테이너 환경에서 **빌드, 단위/통합 테스트 자동 실행** |
| 품질 게이트 (SonarQube) | 코드 커버리지(80% 이상), 시큐어 코딩 규칙 검증 및 **Fail-Fast 집행** |
| 아티팩트 저장소 (Harbor) | 검증 완료된 **불변 컨테이너 이미지(Tag)** 저장 및 무결성 검증 |
| CD 배포 제어기 (ArgoCD) | 대상 K8s 클러스터에 무중단(Blue/Green, Canary) 배포 실행 |

#### 한줄 요약
- Git 저장소, CI 러너, 품질 게이트, 아티팩트 레지스트리, CD 배포 제어기가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Trivy**: 컨테이너 이미지 내부의 OS 패키지 및 애플리케이션 라이브러리 보안 취약점(CVE)을 스캔하는 오픈소스 도구.

</details>

```text
개발자가 Git 저장소로 코드 푸시 (Push / PR)
        │
   [CI 단계] Webhook 트리거로 CI 러너 기동 -> 빌드 및 단위/통합 테스트 실행
        │
   [검증 단계] SonarQube 정적 분석 및 Trivy 보안 취약점 스캔 수행
        │
   품질 게이트 기준(테스트 100% 통과, Critical 취약점 0건)을 충족하는가?
   ┌────┴─────┐
  예           아니오
   │             │
[아티팩트 생성]   [Fail-Fast 즉시 중단 및 개발자에게 Slack 알림]
Docker 이미지 빌드 후
Harbor 저장소에 Push
   │
   [CD 단계] 배포 방식에 따른 분기
   ┌────┴───────────────────────────┐
[Continuous Delivery]             [Continuous Deployment]
스테이징 자동 배포 후             프로덕션 환경까지 완전 자동화 배포
관리자 수동 승인 거쳐 프로덕션 배포     (ArgoCD GitOps 동기화)
```

#### 한줄 요약
- 코드 푸시 → CI 빌드/테스트 → 품질 게이트 검증 → 아티팩트 저장 → CD 배포 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Continuous Delivery vs Continuous Deployment**: 프로덕션 배포 직전 수동 승인 단계를 두는 Delivery와 프로덕션까지 완전 자동 배포되는 Deployment.

</details>

| 파이프라인 단계 | CI (지속적 통합) | CD (지속적 제공: Delivery) | CD (지속적 배포: Deployment) |
|:---|:---|:---|:---|
| 핵심 역할 | **빌드, 테스트, 정적 분석 자동화** | 스테이징 배포 및 **프로덕션 수동 승인** | **프로덕션 환경까지 완전 자동 배포** |
| 트리거 방식 | 코드 Push / PR 생성 시 즉시 | CI 통과 후 자동 스테이징 배포 | CI 통과 즉시 프로덕션 릴리즈 |
| 적합한 환경 | 모든 소프트웨어 프로젝트 기본 | 금융, 의료, 엄격한 규제 준수 시스템 | **고빈도 SaaS, 빅테크 웹/모바일 서비스** |
| 주요 위험 | 없음 (필수 인프라) | 승인 지연으로 인한 리드타임 증가 | 테스트 미흡 시 운영 장애 즉시 전파 |

#### 한줄 요약
- 빌드/테스트 자동화는 CI, 수동 승인 배포는 Delivery, 무인 완전 자동 배포는 Deployment를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Flaky Test(불안정한 테스트)**: 코드 변경이 없음에도 네트워크 타이밍이나 동시성 문제로 간헐적으로 실패하여 CI 신뢰도를 떨어뜨리는 테스트.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 파이프라인 실행 시간 장기화로 피드백 지연 | **도커 레이어 캐싱, 의존성 캐싱 및 테스트 병렬화** | CI 파이프라인 수행 시간 70% 단축 |
| 간헐적 실패를 유발하는 **플래키 테스트(Flaky Test)** | 불안정 테스트 **격리(Quarantine) 및 독립 Mocking** | CI 빌드 성공 신뢰도 99% 회복 |
| 파이프라인 설정 파일에 클라우드 API Key 노출 | **OIDC(OpenID Connect) 기반 무자격증명(Keyless) 인증** | 장기 자격 증명 유출 원천 방어 |
| 배포 직후 프로덕션 장애 발생 | **Argo Rollouts 기반 Canary 점진 배포 및 자동 롤백** | 장애 영향도 5% 이내 격리 및 즉시 복원 |

#### 한줄 요약
- 캐싱/병렬화, 플래키 테스트 격리, OIDC 무자격증명, Canary 점진 배포로 안정성을 극대화한다.

## Ⅶ. 결론

- 통합 자동화는 **CI 품질 게이트**, 배포는 **GitOps** 선택

#### 한줄 요약
- CI/CD 파이프라인은 소프트웨어 품질 검증과 배포를 자동화하여 납기 단축과 장애 예방을 동시에 달성하는 DevOps의 핵심 엔진이다.