---
sidebar:
  order: 57
  label: "057. DevSecOps"
  badge:
    text: "기출 • 70%"
    variant: note
title: "DevSecOps"
date: "2026-08-13T15:57:00+09:00"
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

<details><summary>용어 설명</summary>

- **DevSecOps (Development + Security + Operations)**: 기존 DevOps 파이프라인의 전 단계(Plan부터 Deploy/Operate)에 보안(Security)을 내재화(Shift-Left)하여, 속도 저하 없이 자동화된 보안 검증 및 규정 준수를 달성하는 소프트웨어 공학 패러다임.
- **Shift-Left Security**: 출시 직전이나 운영 단계에 수동으로 수행하던 보안 점검을 소프트웨어 개발 생명주기(SDLC)의 가장 왼쪽(초기 코딩/빌드 단계)으로 앞당겨 결함을 조기 발견/수정하는 전략.
- **Policy as Code (PaC)**: 보안/컴플라이언스 규정 정책(e.g., K8s 보안 룰, AWS IAM 정책)을 OPA(Open Policy Agent)나 Kyverno 코드 형태로 작성하여 CI/CD에서 자동 검증하는 기술.

</details>

- 정의/개념: DevOps 파이프라인 전반에 보안(Security)을 문화이자 자동화된 코드 검증 단계로 내재화(Shift-Left)하는 아키텍처 방법론인 **DevSecOps**
- 배경/필요성: 릴리스 직전 보안 검사는 **수정 비용•배포 지연** 유발

#### 한줄 요약

- 개발•운영 전반에 보안 내재화를 적용하는 데브섹옵스가 핵심이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Automated Security Gate**: CI/CD 파이프라인 상에 SAST, DAST, SCA 도구를 자동 연동하여 Critical 등급 취약점 발견 시 빌드를 파기시키는 자동 차단 장치.
- **Continuous Compliance**: 소스코드 및 IaC(Infrastructure as Code) 보안 컴플라이언스 준수 여부를 상시 감시하여 규제 준수를 입증하는 속성.

</details>

- 보안 검증의 좌향 이동 (**Shift-Left Security**)
- **Policy as Code (PaC)** 및 **Automated Security Gate** 구현
- 개발-보안-운영 3개 조직의 **Shared Security Responsibility (보안 공동 책임)** 문화

#### 한줄 요약

- 시프트 레프트, 정책 코드화, 공동 책임이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SAST (Static Application Security Testing)**: 소스코드나 바이너리를 직접 실행하지 않고 정적으로 분석하여 SQL Injection, XSS 등의 취약점을 조기 탐지하는 정적 보안 분석 (e.g. SonarQube, Fortify).
- **DAST (Dynamic Application Security Testing)**: 구동 중인 실환경 웹 애플리케이션에 모의 침투 공격 쿼리를 동적으로 전송하여 런타임 취약점을 탐지하는 동적 보안 분석 (e.g. OWASP ZAP, Burp Suite).
- **SCA (Software Composition Analysis)**: 오픈소스 라이브러리의 알려진 취약점(CVE) 및 라이선스 위반 여부를 점검하는 소프트웨어 구성 분석 (e.g. Snyk, Dependency-Check).
- **IAST (Interactive Application Security Testing)**: SAST와 DAST의 장점을 결합하여 애플리케이션 내부에 에이전트를 주입해 런타임 코드 실행 경로를 분석하는 대화형 보안 분석.

</details>

```text
 [위협 모델링] ─── [보안 파이프라인]
       │                  │
 [보안 관측] ───── [보안 게이트]
```

선의 의미: 개발자의 IDE 코드 작성 단계부터 CI 빌드, 이미지 저장, 배포 및 운영에 이르기까지 연속적인 보안 검사 도구가 자동 배치된 구조.

| 구성요소 | 책임 |
|:---|:---|
| 위협 모델링 | 자산•공격면•보안 요구 식별 |
| 보안 파이프라인 | SAST•SCA•DAST•이미지 검사 자동 실행 |
| 보안 게이트 | 위험도와 정책에 따라 승격 허용 판정 |
| 보안 관측 | 운영 위협 탐지와 규칙 개선 피드백 |

#### 한줄 요약

- 위협 모델링, 보안 파이프라인, 보안 게이트, 보안 관측의 연결 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Container Image Scanning (Trivy)**: 컨테이너 Base Image 상의 OS 패키지(Debian, Alpine) 및 라이브러리에 포함된 CVE 취약점을 릴리스 직전 차단 검사하는 기법.

</details>

```text
┌──────────────────────────────┐
│ Git Commit (Pre-commit Hook) │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 비밀정보 검사             │
│ 2. 정적•구성요소 분석        │
│ 3. 컨테이너 이미지 검사      │
│ 4. 보안 게이트 판정          │
│ 5. 정책 검증•배포            │
└──────────────┬───────────────┘
               ▼
   [안전한 K8s 배포 완결]
```

### 동작 원리

1. **비밀정보 검사**: 커밋 전 API 키•토큰 포함 여부 검사.
2. **정적•구성요소 분석**: 코드 취약점과 CVE•라이선스 검사.
3. **컨테이너 이미지 검사**: OS 패키지와 설정 취약점 분석.
4. **보안 게이트 판정**: 위험도•예외 정책으로 승격 여부 결정.
5. **정책 검증•배포**: IaC 정책을 확인하고 검증 산출물 배포.

#### 한줄 요약

- 보안 요구 도출부터 운영 위험 관측•환류까지의 통제 흐름이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **DevOps vs DevSecOps**: DevOps는 속도와 민첩성 중심, DevSecOps는 속도와 보안의 균형(Shift-Left) 중심으로 개발 초기부터 보안팀 참여.

</details>

| 비교 항목 | Traditional Security (사후 점검) | DevSecOps (지속적 내재화) |
|:---|:---|:---|
| 검사 시점 | 배포 직전 수동 침투 테스트 (Right Stage) | **개발 초기 커밋부터 상시 자동 분석 (Shift-Left)** |
| 검사 속도 | 수동 일정과 분석 범위에 따라 지연 | **변경 범위 자동 검사로 조기 피드백** |
| 담당 주체 | 전담 보안팀 독립 수행 | **개발자 + 보안팀 + 운영팀 보안 공동 책임** |
| 피드백 반영 | 배포 거부 후 대규모 소스 재작성 | **커밋 단위 즉시 수정을 통한 최소 비용 해결** |

#### 한줄 요약

- 네 검사 방식의 서로 다른 탐지 근거를 결합하는 것이 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **False Positive (오탐)**: 취약점이 아님에도 보안 도구가 위험으로 오판하여 빌드를 차단하는 현상으로, 오탐 룰셋(Exclusion List)튜닝 필수.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 오탐(**False Positive**)으로 정상 변경 승격 차단 | 룰셋 튜닝과 근거•만료일 있는 예외 관리 | 개발 생산성과 통제력 균형 |
| 보안 검사 확대로 파이프라인 피드백 지연 | **SAST 증분 검사**와 예약 전체 검사 분리 | 검사 범위와 피드백 속도 균형 |
| 개발자들의 보안 지식 부족으로 인한 저항 | **Security Champion** 제도 운용 및 개발자 IDE 자동 교정 플러그인 제공 | 문화적 충격 완화 |

> 사례: **GitHub Enterprise + SonarQube + Snyk + Trivy + OPA** 기반 DevSecOps 표준 파이프라인

#### 한줄 요약

- 위험별 검사, 소프트웨어 자재 명세서, 서명 검증이 핵심이다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **DevSecOps 구축 기준(DevSecOps Selection Criteria)**: Shift-Left 달성도, 4대 보안 도구 연동 및 Security Gate 자동화 수준에 의거한 체계.

</details>

- 코드 결함은 **Shift-Left**, 운영 공격은 **런타임 보안 관측**으로 통제

#### 한줄 요약

- 변경 전 조기 차단과 운영 중 런타임 검증을 결합하는 것이 핵심이다.
