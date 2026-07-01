---
title: "DevSecOps (DevSecOps)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 63
---

# 📖 【암기용】 개념 완전 이해

> 목적: DevSecOps를 개발 생명주기와 보안 통제 관점에서 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 개발·운영 파이프라인에 보안 검증을 내장하는 방식
- **왜 필요한가**: 배포 직전 보안 점검은 취약점 수정 비용과 일정 지연을 키움. DevSecOps는 코드 작성, 빌드, 배포, 운영 단계마다 보안 gate를 배치함.
- **핵심 직관**: 보안팀이 마지막 검문소에 서는 것이 아니라, 생산 라인 곳곳에 자동 검사 장비를 넣는 방식임.

## 깊이 이해
- **배경·문제의식**: MSA, 컨테이너, 오픈소스 의존성이 증가하면서 취약점은 코드, 라이브러리, 이미지, IaC, 런타임 전 영역에서 발생함. 후행 점검만으로는 CVE 대응 시간과 배포 리드타임을 동시에 맞추기 어렵다.
- **작동 원리**: Shift-left로 SAST, SCA, secret scan, IaC scan을 PR 단계에 배치하고, Shift-right로 DAST, RASP, runtime detection을 운영 단계에 배치함. Policy as Code가 통과 여부를 자동 판단함.
- **비유**: 공항 보안처럼 입구, 수하물, 탑승구, 기내 감시가 단계별로 나뉘어 위험을 줄임.
- **구체 예시**: PR에서 SCA가 CVSS 9.8 취약 라이브러리를 차단하고, 컨테이너 registry에서 critical CVE 0건 이미지만 운영 배포를 허용함.
- **흔한 오해·주의점**: DevSecOps는 보안 도구 추가가 전부가 아님. 정책 예외 승인, false positive 관리, 운영 탐지까지 포함해야 파이프라인 병목을 줄임.

## 연결 개념
- SAST/SCA/DAST: 코드, 의존성, 실행 환경 취약점 검사
- Policy as Code: 보안 기준을 코드로 작성하고 자동 판정
- SBOM: 오픈소스 구성과 취약점 영향 범위 추적

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: DevSecOps는 보안 활동을 shift-left/right로 분산하고 policy gate로 배포 허용 여부를 판정하는 파이프라인 통제 체계임.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DevSecOps는 개발, 보안, 운영 책임을 통합해 SAST/SCA/DAST/IaC/container 검증을 CI/CD에 내장하는 방식임.
> 2. **가치**: CVSS 9.0 이상 취약점, secret 노출, IaC misconfig를 PR 단계에서 차단해 후행 보안 수정 비용을 낮춤.
> 3. **판단 포인트**: shift-left만 쓰면 런타임 공격을 놓치므로 shift-right 탐지, 예외 승인, 감사로그를 함께 설계해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 보안 내재화 이해 확인 | shift-left, shift-right, security gate | 보안팀 사후 점검으로 설명 |
| 도구별 적용 위치 확인 | SAST, SCA, DAST, IaC, container scan | 도구명을 나열하고 단계 연결 누락 |
| 정책·운영 통제 판단 확인 | Policy as Code, 예외관리, SBOM, audit | false positive와 gate 우회 리스크 누락 |

> 요약: DevSecOps 문제는 보안 검증을 파이프라인 단계별 gate와 운영 탐지로 연결하는 설계 능력을 요구한다.

---

## Ⅰ. 개요 및 필요성

DevSecOps는 보안을 DevOps 파이프라인 전 과정에 내장하는 개발·운영 방식이다. 오픈소스, 컨테이너, IaC 사용 증가로 취약점 유입 경로가 코드 저장소부터 런타임까지 확장되었다. 따라서 보안 검증을 자동화 gate로 전환해 배포 전 차단과 운영 탐지를 함께 수행해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Code/PR -> SAST/SCA/Secret Scan -> Build/Image Scan
IaC -> Policy as Code -> Deploy Gate -> Runtime Monitoring
Alert -> Triage -> Exception/Audit -> Backlog
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Shift-left 검사 | 코드·의존성·secret 조기 탐지 | SAST, SCA, Gitleaks |
| Build/Artifact 검사 | 이미지, SBOM, 서명 검증 | Trivy, Syft, Cosign |
| Policy Gate | 배포 허용 기준 자동 판정 | OPA, Conftest, admission controller |
| Shift-right 탐지 | 운영 공격, 이상 행위 감지 | SIEM, EDR, Falco |

> 요약: DevSecOps 구조는 PR, 빌드, 배포, 운영 단계마다 보안 검사를 배치하고 정책 코드로 통과 기준을 판정한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요구 변경 -> PR 보안검사 -> Artifact 생성
-> SBOM/서명 -> 배포 정책 판정 -> 운영 배포
-> 런타임 탐지 -> 취약점 Backlog
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 개발자가 PR 생성, SAST와 secret scan 수행 | high 취약점 0건 |
| 2 | SCA로 오픈소스 CVE와 라이선스 검사 | CVSS 9.0 이상 차단 |
| 3 | 컨테이너 이미지와 IaC 설정 검사 | critical CVE 0건, privileged false |
| 4 | Policy as Code로 배포 gate 판정 | 예외 승인 ticket 필수 |
| 5 | 운영에서 DAST, WAF, runtime 탐지 수행 | MTTD 10분 이하 |

> 요약: DevSecOps는 개발 초기에 취약점을 차단하고 운영 단계에서 탐지·대응해 보안 통제를 지속 흐름으로 만든다.

---

## Ⅳ. 특징

| 구분 | 사후 보안 점검 | DevSecOps | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 검사 시점 | 릴리스 직전 | PR, build, deploy, runtime | 취약점 발견 리드타임 1일 이하 |
| 검사 범위 | 코드 중심 | 코드, OSS, IaC, image, runtime | SBOM 100% 생성 |
| 판정 방식 | 보안 담당자 수동 승인 | policy gate 자동 차단 | critical CVE 0건 기준 |
| 운영 대응 | 취약점 공지 후 조치 | 탐지, 격리, backlog 연계 | MTTD 10분, MTTR 4시간 목표 |

> 요약: DevSecOps는 보안 통제를 후행 승인에서 단계별 자동 gate와 운영 탐지로 전환한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 보안팀 최종 승인 | 파이프라인 내장 gate | 주 1회 이상 배포 조직 |
| 비용/성능 | 릴리스 지연, 재작업 | PR 단계 조기 수정 | critical 수정 리드타임 24시간 이하 |
| 운영/위험 | 운영 공격 탐지 분리 | shift-left/right 연결 | 클라우드·컨테이너 운영 필수 |
| 감사/규제 | 문서 증적 수작업 | scan report, SBOM, audit log | ISMS-P, ISO 27001 대응 |

> 요약: DevSecOps는 배포 빈도가 높고 오픈소스 의존성이 많은 환경에서 보안 승인 병목을 자동 gate로 전환할 때 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| False positive 증가 | 규칙 과다, 컨텍스트 부족 | severity tuning, baseline 관리 | 오탐률 20% 이하 |
| Gate 우회 | 긴급 배포 남용 | break-glass 승인, 사후 review | 우회 월 1건 이하 |
| Secret 유출 | 토큰 평문 commit | pre-commit hook, vault 연동 | secret leak 0건 |
| 공급망 공격 | 이미지·패키지 위변조 | SBOM, Cosign 서명, provenance | 서명 검증률 100% |

> 요약: DevSecOps 리스크는 오탐, gate 우회, secret 유출, 공급망 위변조이며 정책 튜닝과 서명 검증으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 취약점 차단 | critical CVE 운영 반영 0건 | SCA, image scan |
| 검출 시간 | MTTD 10분 이하 | SIEM, alert timestamp |
| 수정 시간 | critical MTTR 24시간 이하 | ticket, merge time |
| 증적 관리 | scan report 100% 보관 | artifact, audit log |

> 요약: DevSecOps 효과는 취약점 차단률, 탐지 시간, 수정 시간, 증적 보관률로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. PR 단계에 Semgrep SAST, Snyk/OWASP Dependency-Check SCA, Gitleaks를 배치하고 high 이상 0건을 merge 기준으로 설정함.
2. 컨테이너 registry에 Trivy scan, Syft SBOM, Cosign 서명을 적용하고 admission controller에서 미서명 이미지를 차단함.
3. 운영 단계에 WAF, Falco, SIEM 연계를 구성하고 critical alert는 10분 내 triage, 24시간 내 patch SLA로 관리함.

**결론 (2줄):**
- 기술사 판단: 고빈도 배포와 오픈소스 의존성이 큰 서비스는 DevSecOps를 필수 gate로 적용하고, 저빈도 내부 시스템은 SCA·secret scan부터 단계 도입함.
- 향후 방향: DevSecOps는 SBOM, SLSA, Sigstore 기반 소프트웨어 공급망 보안 통제로 확장됨.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "DevSecOps를 설명하시오" | shift-left/right, SAST/SCA/DAST 단계 | 사후 점검과 pipeline gate 비교 |
| 요구사항 명시형 | "보안 파이프라인을 설계하시오", "도입 방안을 제시하시오" | 정책 gate, SBOM, runtime 탐지 흐름 | 예외관리, CVE SLA, 감사 증적 |

> 요약: 설명형은 단계별 보안 내재화를, 설계형은 정책 자동화와 운영 대응 기준을 중심으로 목차를 전환한다.
