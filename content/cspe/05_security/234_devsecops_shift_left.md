---
title: "DevSecOps 보안 시프트 레프트 (DevSecOps Shift-Left)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 234
---

# 📖 【암기용】 개념 완전 이해

> 목적: DevSecOps Shift-Left를 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 보안 점검을 배포 직전이 아니라 요구사항·코딩·빌드 단계로 앞당기는 개발 보안 운영 방식
- **왜 필요한가**: 운영 배포 직전 취약점이 발견되면 수정 비용과 일정 지연이 커진다. 개발자가 코드를 작성하는 시점에 취약점을 발견해야 MTTR을 줄일 수 있다.
- **핵심 직관**: 완성품 출고 검사만 하는 대신 설계도·부품·조립 공정마다 결함을 바로 잡는 품질관리 방식이다.

## 깊이 이해
- **배경·문제의식**: 애자일·마이크로서비스·CI/CD 환경에서는 하루에도 여러 번 배포가 발생한다. 수동 보안 진단 중심 프로세스는 배포 속도와 맞지 않고, 취약점 수정이 스프린트 이후로 밀린다.
- **작동 원리**: 개발자는 IDE와 Pull Request에서 SAST·Secret Scan·SCA 결과를 확인한다. CI/CD는 IaC Scan, Container Scan, DAST를 실행하고, 정책 위반 시 Quality Gate가 배포를 중단한다. 예외는 Policy as Code로 승인·만료·감사를 남긴다.
- **비유**: 시험 전날 전체 교재를 다시 보는 방식이 아니라, 매 단원 문제를 풀 때 오답을 즉시 고치는 학습 방식이다.
- **구체 예시**: PR 생성 시 하드코딩된 AWS Key는 Secret Scan으로 즉시 차단하고, Log4j CVSS 9.8 취약 라이브러리는 SCA Quality Gate에서 merge를 막는다.
- **흔한 오해·주의점**: Shift-Left는 보안팀 책임을 개발팀에 떠넘기는 방식이 아니다. 자동화된 도구, 정책 기준, 예외 절차, 보안 코칭을 함께 제공해야 지속 가능하다.

## 연결 개념
- SAST/SCA/Secret Scan - 코드와 의존성 단계에서 취약점을 찾는 대표 도구이다.
- Policy as Code - 보안 기준을 코드로 표현해 CI/CD에서 자동 판정한다.
- Quality Gate - 기준 미달 산출물의 merge·배포를 막는 통제 지점이다.

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: DevSecOps Shift-Left는 도구 나열이 아니라 CI/CD 품질 게이트, 오탐 관리, MTTR 지표, 예외 승인까지 포함한 보안 운영 모델로 답한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DevSecOps Shift-Left는 SAST/SCA/Secret/IaC/Container Scan을 개발 초기와 CI/CD에 배치해 취약점 발견 시점을 앞당기는 방식이다.
> 2. **가치**: 운영 배포 후 수정하던 취약점을 PR·빌드 단계에서 차단해 보안 결함 MTTR을 30일에서 7일 이하로 줄이는 것을 목표로 한다.
> 3. **판단 포인트**: 정책 기준, Quality Gate 임계치, 오탐 처리, 개발자 피드백 시간, 예외 만료가 실제 적용 성패를 좌우한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| DevSecOps 개념과 Shift-Left 차이 확인 | 보안 자동화, 개발 초기 점검, CI/CD 통합 | 보안 도구 목록만 나열 |
| 파이프라인 설계 역량 확인 | SAST, SCA, Secret, IaC, Container, DAST 배치 | 런타임·운영 탐지와의 연계 누락 |
| 운영 지표와 예외 통제 확인 | MTTR, 오탐률, Gate 실패율, 승인 만료 | 전면 차단만 답하고 개발 생산성 저하 누락 |

> 요약: 이 문제는 Shift-Left 원리와 품질 게이트를 MTTR·오탐 관리 지표로 연결하는 판단을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 개발 초기 보안검사 배치 방식
- 배경: 배포 직전 수동 진단은 수정 비용과 일정 지연을 키우고, CI/CD 환경에서는 취약점 조치가 다음 릴리스로 밀릴 수 있음
- 필요성: PR·CI 단계에 SAST, SCA, Secret, IaC, Container Scan을 배치하고 Critical 0건, High 7일 SLA, PR 피드백 10분 이하 기준으로 운영해야 함

---

## Ⅱ. 구조 및 구성요소

```text
Developer IDE -> Pull Request -> CI Security Scan -> Quality Gate
              +-> SAST/SCA/Secret/IaC/Container -> Policy as Code
Quality Gate -> Deploy/Block/Exception -> SIEM/Jira Feedback
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| SAST | 소스코드 취약 패턴 분석 | SQL Injection, XSS, 인증 누락 |
| SCA | 오픈소스 라이브러리 CVE·라이선스 분석 | CVSS, EPSS, SBOM |
| Secret Scan | API Key, Token, 인증서 유출 탐지 | Git hook, PR scan |
| IaC/Container Scan | Terraform, Kubernetes, Image 취약 설정 탐지 | CIS Benchmark, CVE |
| Quality Gate | 정책 기준 미달 시 merge·배포 차단 | Policy as Code, 예외 만료 |

> 요약: Shift-Left는 코드·의존성·비밀값·인프라·컨테이너 검사를 CI/CD 품질 게이트로 묶는 구조이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요구사항 보안 기준 -> 코드 작성 -> PR 자동 검사 -> 정책 판정
-> Gate 통과/차단 -> 예외 승인 -> 배포 -> 운영 피드백
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 보안 요구사항과 정책을 코드화 | OWASP ASVS, CIS, 조직 정책 |
| 2 | PR에서 SAST/SCA/Secret Scan 실행 | Critical 0건, High SLA 7일 |
| 3 | CI에서 IaC·Container Scan 수행 | root 실행 금지, CVSS 9.0 이상 차단 |
| 4 | Quality Gate가 merge·배포 여부 결정 | 정책 위반 시 실패, 예외 만료일 기록 |
| 5 | 운영 탐지 결과를 백로그로 환류 | Jira 티켓, MTTR, 재발률 |

> 요약: Shift-Left는 정책을 코드화하고 PR·CI 단계에서 자동 판정한 뒤 운영 결과를 개발 백로그로 되돌린다.

---

## Ⅳ. 특징

| 구분 | 기존 보안 점검 | Shift-Left | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 점검 시점 | 배포 전·운영 후 | IDE, PR, CI/CD | PR 피드백 10분 이하 |
| 통제 방식 | 수동 진단 보고서 | 자동 스캔+Quality Gate | Critical 0건, High 7일 SLA |
| 책임 구조 | 보안팀 중심 | 개발·보안·운영 공동 | 보안 챔피언, 예외 승인 |
| 한계 | 배포 지연 | 오탐·Gate 피로 | 오탐률 10% 이하 목표 |

> 요약: Shift-Left는 발견 시점을 앞당기지만 오탐과 Gate 피로를 줄이는 정책 튜닝이 병행되어야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 배포 전 수동 점검 | PR/CI 자동 보안 검사 | 일 배포 1회 이상, MSA 서비스 다수 |
| 비용/성능 | 취약점 수정 후반 집중 | 개발 단계 수정 | PR 보안 피드백 10분 이하 |
| 운영/위험 | 보안팀 병목 | 정책 코드와 예외 승인 | MTTR 7일 이하 목표 시 |

> 요약: Shift-Left는 배포 빈도가 높고 취약점 수정 지연이 반복되는 조직에서 우선 적용한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 오탐 피로 | 도구 기본 룰 과다 적용 | 언어·프레임워크별 룰 튜닝 | 오탐률 10% 이하 |
| 배포 지연 | 모든 취약점 차단 정책 | Critical 차단, High SLA 관리 | Gate 실패율, 리드타임 |
| 책임 공백 | 보안팀·개발팀 역할 불명확 | 보안 챔피언, RACI, 예외 승인 | 티켓 소유자 지정률 100% |

> 요약: Shift-Left 리스크는 오탐과 배포 지연이며 위험도 기반 Gate와 책임 매트릭스로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 취약점 MTTR | Critical 3일, High 7일 이하 | Jira, 취약점 관리 대시보드 |
| 파이프라인 품질 | 스캔 시간 10분 이하, Gate 실패율 추적 | CI 로그, DORA 지표 |
| 정책 준수 | 예외 만료 30일 이하, SBOM 생성률 100% | Policy as Code 리포트 |

> 요약: Shift-Left 성과는 MTTR, 스캔 피드백 시간, 예외 만료, SBOM 생성률로 평가한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. PR 단계에 SAST·SCA·Secret Scan을 배치하고 Critical 0건, CVSS 9.0 이상 라이브러리 merge 차단 정책을 적용함
2. CI 단계에 IaC·Container Scan과 SBOM 생성을 넣고, Kubernetes root 컨테이너·privileged 옵션은 Policy as Code로 차단함
3. 오탐은 보안 챔피언이 48시간 내 분류하고, 예외는 만료 30일·승인자·대체 통제를 티켓에 기록함

**결론 (2줄):**
- 기술사 판단: 배포 빈도가 높고 수동 진단 병목이 있는 조직은 Shift-Left를 우선 도입하되, Critical 차단과 High SLA 관리로 Gate 기준을 구분해야 함
- 향후 방향: DevSecOps는 SBOM, SLSA, Sigstore, 런타임 탐지를 결합해 소프트웨어 공급망 전반 통제로 발전함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "DevSecOps를 설명하시오", "Shift-Left를 기술하시오" | PR·CI/CD 보안 검사 흐름 | 기존 보안 점검 대비 시점·책임 차이 |
| 요구사항 명시형 | "구축 방안을 제시하시오", "CI/CD 보안을 설계하시오" | 도구 배치, Gate 기준, 예외 승인 | MTTR, 오탐률, 배포 지연 대응 |

> 요약: 설명형은 원리와 구성요소를, 설계·방안형은 파이프라인 배치와 운영 지표를 중심으로 전개한다.
