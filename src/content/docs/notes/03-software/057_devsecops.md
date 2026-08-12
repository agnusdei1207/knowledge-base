---
sidebar:
  order: 57
  label: "057. DevSecOps"
  badge:
    text: "기출 • 70%"
    variant: note
title: "DevSecOps"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 57
extra:
  question_no: "057"
  source_status: "기출"
  source_history: "128회, 134회, 135회"
  priority: 70
  priority_note: "128•134•135회 반복, 보안 내재화 핵심"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **DevSecOps (Development + Security + Operations)**: 기존 DevOps 파이프라인의 전 단계(Plan부터 Deploy/Operate)에 보안(Security)을 내재화(Shift-Left)하여, 속도 저하 없이 자동화된 보안 검증 및 규정 준수를 달성하는 소프트웨어 공학 패러다임.
- **Shift-Left Security**: 출시 직전이나 운영 단계에 수동으로 수행하던 보안 점검을 소프트웨어 개발 생명주기(SDLC)의 가장 왼쪽(초기 코딩/빌드 단계)으로 앞당겨 결함을 조기 발견/수정하는 전략.
- **Policy as Code (PaC)**: 보안/컴플라이언스 규정 정책(e.g., K8s 보안 룰, AWS IAM 정책)을 OPA(Open Policy Agent)나 Kyverno 코드 형태로 작성하여 CI/CD에서 자동 검증하는 기술.

</details>

- 정의/개념: DevOps 파이프라인 전반에 보안(Security)을 문화이자 자동화된 코드 검증 단계로 내재화(Shift-Left)하는 아키텍처 방법론인 **DevSecOps**
- 배경/필요성: 릴리스 직전 사후 보안 검사로 인한 배포 지연 및 Open Source 오픈소스 라이선스/취약점(Log4j 등) 폭증에 따른 대처 요구성

#### 한줄 요약

- 개발•운영 전반에 보안 내재화를 적용하는 데브섹옵스가 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Automated Security Gate**: CI/CD 파이프라인 상에 SAST, DAST, SCA 도구를 자동 연동하여 Critical 등급 취약점 발견 시 빌드를 파기시키는 자동 차단 장치.
- **Continuous Compliance**: 소스코드 및 IaC(Infrastructure as Code) 보안 컴플라이언스 준수 여부를 상시 감시하여 규제 준수를 입증하는 속성.

</details>

- 보안 검증의 좌향 이동 (**Shift-Left Security**)
- **Policy as Code (PaC)** 및 **Automated Security Gate** 구현
- 개발-보안-운영 3개 조직의 **Shared Security Responsibility (보안 공동 책임)** 문화

#### 한줄 요약

- 시프트 레프트, 정책 코드화, 공동 책임이 핵심이다.

## Ⅲ. 구조 및 구성요소 (Shift-Left 4대 보안 검사)

<details><summary>핵심 용어</summary>

- **SAST (Static Application Security Testing)**: 소스코드나 바이너리를 직접 실행하지 않고 정적으로 분석하여 SQL Injection, XSS 등의 취약점을 조기 탐지하는 정적 보안 분석 (e.g. SonarQube, Fortify).
- **DAST (Dynamic Application Security Testing)**: 구동 중인 실환경 웹 애플리케이션에 모의 침투 공격 쿼리를 동적으로 전송하여 런타임 취약점을 탐지하는 동적 보안 분석 (e.g. OWASP ZAP, Burp Suite).
- **SCA (Software Composition Analysis)**: 오픈소스 라이브러리의 알려진 취약점(CVE) 및 라이선스 위반 여부를 점검하는 소프트웨어 구성 분석 (e.g. Snyk, Dependency-Check).
- **IAST (Interactive Application Security Testing)**: SAST와 DAST의 장점을 결합하여 애플리케이션 내부에 에이전트를 주입해 런타임 코드 실행 경로를 분석하는 대화형 보안 분석.

</details>

```text
[코드 작성 (IDE)] ──► [CI Build (SAST/SCA)] ──► [Container Reg (Image Scan)] ──► [Deploy (DAST/PaC)]
        │                         │                           │                       │
 [Secret Scanning]       [SonarQube/Snyk]            [Trivy/Clair]           [OWASP ZAP/OPA]
```

선의 의미: 개발자의 IDE 코드 작성 단계부터 CI 빌드, 이미지 저장, 배포 및 운영에 이르기까지 연속적인 보안 검사 도구가 자동 배치된 구조.

| DevSecOps 4대 기술 | 대상 및 시점 | 주요 역할 및 대표 도구 |
|:---|:---|:---|
| **SAST (정적 분석)** | 소스코드 (Coding/Build 단계)| 소스코드 내 취약 패턴(SQLi, XSS) 정적 분석 (SonarQube, Fortify) |
| **SCA (구성요소 분석)** | 오픈소스 라이브러리 (Dependencies)| 오픈소스 CVE 취약점 및 라이선스 위반 검사 (Snyk, BlackDuck) |
| **Secret Scanning** | Git Repository (Commit 시점)| 코드 내 하드코딩된 API Key/비밀키 실수 탐지 (Gitleaks, TruffleHog) |
| **Container Scan** | Docker/OCI Container Image | 컨테이너 OS 패키지 취약점 및 Root 실행 방지 (Trivy, Clair) |
| **DAST (동적 분석)** | 구동 중인 App (Staging 단계) | 모의 침투(Pentest) 기반 런타임 취약점 점검 (OWASP ZAP) |
| **IaC & PaC Scan** | Terraform / K8s Manifest | 인프라 코드의 보안 취약 설정 정적 검증 (Checkov, OPA/Kyverno) |

#### 한줄 요약

- 위협 모델링, 보안 파이프라인, 보안 게이트, 보안 관측의 연결 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Container Image Scanning (Trivy)**: 컨테이너 Base Image 상의 OS 패키지(Debian, Alpine) 및 라이브러리에 포함된 CVE 취약점을 릴리스 직전 차단 검사하는 기법.

</details>

```text
┌──────────────────────────────┐
│ Git Commit (Pre-commit Hook) │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. Secret Scanning (Gitleaks)│
│ 2. SAST (SonarQube)          │
│ 3. SCA 오픈소스 (Snyk)       │
│ 4. Image Scanning (Trivy)    │
│ 5. Security Gate (Pass/Fail) │
└──────────────┬───────────────┘
               ▼
   [안전한 K8s 배포 완결]
```

### 동작 원리

1. **Pre-commit**: 개발자 local 커밋 시 Gitleaks가 API Key 포함 여부 사전 차단.
2. **SAST & SCA**: PR 생성 시 SonarQube가 OWASP Top 10 취약점 스캔 및 Snyk이 CVE 오픈소스 패키지 검사.
3. **Image Scan**: 빌드된 Docker 이미지에 대해 Trivy가 OS level 취약점 스캔.
4. **Security Gate**: Critical/High 등급 취약점 감지 시 파이프라인 즉시 파기 및 개발자에 피드백.
5. **Prod Deploy**: 검증을 완결한 불변 이미지 및 OPA 정책 검증 후 K8s 배포.

#### 한줄 요약

- 보안 요구 도출부터 운영 위험 관측•환류까지의 통제 흐름이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **DevOps vs DevSecOps**: DevOps는 속도와 민첩성 중심, DevSecOps는 속도와 보안의 균형(Shift-Left) 중심으로 개발 초기부터 보안팀 참여.

</details>

| 비교 항목 | Traditional Security (사후 점검) | DevSecOps (지속적 내재화) |
|:---|:---|:---|
| 검사 시점 | 배포 직전 수동 침투 테스트 (Right Stage) | **개발 초기 커밋부터 상시 자동 분석 (Shift-Left)** |
| 검사 속도 | 수일~수주일 소요 (배포 병목) | **수분 이내 자동 검사 (Pipeline 내 완결)** |
| 담당 주체 | 전담 보안팀 독립 수행 | **개발자 + 보안팀 + 운영팀 보안 공동 책임** |
| 피드백 반영 | 배포 거부 후 대규모 소스 재작성 | **커밋 단위 즉시 수정을 통한 최소 비용 해결** |

#### 한줄 요약

- 네 검사 방식의 서로 다른 탐지 근거를 결합하는 것이 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **False Positive (오탐)**: 취약점이 아님에도 보안 도구가 위험으로 오판하여 빌드를 차단하는 현상으로, 오탐 룰셋(Exclusion List)튜닝 필수.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 지나친 오탐(**False Positive**)으로 파이프라인이 계속 무단 차단됨 | 보안 도구의 룰셋 튜닝 및 프로젝트 특화 바인딩 | 개발 생산성 보존 |
| 보안 도구 도입으로 파이프라인 빌드 시간이 1시간으로 연장 | **SAST 델타(증분) 스캔 & 스케줄링 야간 풀스캔 분리** | 파이프라인 속도 유지 |
| 개발자들의 보안 지식 부족으로 인한 저항 | **Security Champion** 제도 운용 및 개발자 IDE 자동 교정 플러그인 제공 | 문화적 충격 완화 |

> 사례: **GitHub Enterprise + SonarQube + Snyk + Trivy + OPA** 기반 DevSecOps 표준 파이프라인

#### 한줄 요약

- 위험별 검사, 소프트웨어 자재 명세서, 서명 검증이 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **DevSecOps 구축 기준(DevSecOps Selection Criteria)**: Shift-Left 달성도, 4대 보안 도구 연동 및 Security Gate 자동화 수준에 의거한 체계.

</details>

- **DevSecOps 구축 기준**에 따라 Cloud-Native 엔터프라이즈 시스템 구축 시 **Shift-Left DevSecOps 파이프라인** 필수 인가

#### 한줄 요약

- 변경 전 조기 차단과 운영 중 런타임 검증을 결합하는 것이 핵심이다.
