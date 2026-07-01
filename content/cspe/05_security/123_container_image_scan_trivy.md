---
title: "컨테이너 이미지 취약점 스캔 - Trivy (Container Image Scan)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 123
---
# 📖 【암기용】 개념 완전 이해

> 목적: 컨테이너 이미지 취약점 스캔과 Trivy의 역할을 처음 보는 사람도 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.
## 한눈에
- **개요**: Trivy는 컨테이너 이미지와 코드 저장소에서 CVE, 설정 오류, Secret, 라이선스 위험을 탐지하는 보안 스캐너임
- **왜 필요한가**: 컨테이너 이미지는 OS 패키지, 언어 라이브러리, 애플리케이션 파일, 설정 파일이 한 번에 묶인다. 취약한 base image나 Secret이 이미지에 들어가면 모든 배포 환경으로 복제된다.
- **핵심 직관**: 택배 상자를 출고하기 전에 내용물, 송장, 위험물, 금지 물품을 검사하고 기준을 넘으면 출고를 막는 절차임
## 깊이 이해
- **배경·문제의식**: 컨테이너는 동일 이미지를 개발, 테스트, 운영에 배포하므로 이미지 단계에서 취약점을 잡지 못하면 클러스터 전체에 동일 위험이 퍼진다. 운영 중 패치보다 빌드 단계 차단이 조치 비용을 줄인다.
- **작동 원리**: Trivy는 이미지 레이어를 분석해 OS 패키지와 애플리케이션 의존성을 식별하고 NVD, vendor advisory, GitHub Advisory 등 취약점 DB와 대조한다. Dockerfile/IaC 설정 오류, 하드코딩 Secret, SBOM 생성·검증도 함께 수행할 수 있다.
- **비유**: 공항 보안검색처럼 짐을 분해해 금속, 액체, 위험물을 검사하고 위험 등급별로 탑승 허용 여부를 결정하는 방식임
- **구체 예시**: `nginx:1.21` 이미지에서 OpenSSL Critical CVE와 Dockerfile `USER root`가 발견되면 CI 파이프라인에서 실패 처리하고 `nginx:1.25-alpine` 또는 distroless 기반으로 교체함
- **흔한 오해·주의점**: 스캔 결과 0건이 무취약을 뜻하지 않는다. 패키지 식별 실패, vendor patch backport, DB 갱신 지연, 오탐 예외 정책을 같이 관리해야 함

## 연결 개념
- SBOM — 이미지 구성요소를 CycloneDX/SPDX로 기록
- CI/CD Security Gate — Critical CVE와 Secret을 배포 전 차단
- OPA Gatekeeper — 스캔·서명 결과를 Admission 정책으로 검증

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Trivy 답안은 도구 사용법이 아니라 이미지 공급망에서 취약점·Secret·설정 오류를 빌드 단계에서 차단하고 운영 증거로 연결하는 구조로 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 컨테이너 이미지 스캔은 이미지 레이어의 OS 패키지, 언어 라이브러리, 설정, Secret을 분석해 배포 전 위험을 식별하는 공급망 보안 통제이다.
> 2. **가치**: Trivy는 Container Image, Filesystem, Git Repository, Kubernetes 대상에서 CVE, IaC Misconfiguration, Secret, License 위험을 탐지해 CI/CD 게이트로 사용할 수 있다.
> 3. **판단 포인트**: Critical CVE 0건, Secret 0건, SBOM 생성, 서명 검증, 예외 만료일을 기준으로 배포 허용 여부를 결정해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 컨테이너 공급망 위험 이해 확인 | base image, OS package, language dependency, Secret | 컨테이너 런타임 보안으로만 설명 |
| CI/CD 보안 게이트 설계 확인 | Trivy scan, SBOM, severity threshold, fail pipeline | CVE 목록만 나열하고 차단 기준 누락 |
| 운영 예외 관리 역량 확인 | false positive, vendor backport, allowlist, 만료일 | "스캔하면 안전"으로 단정 |

> 요약: Trivy 문제는 이미지 분석 결과를 배포 차단 기준, SBOM, 예외 관리, Admission 검증으로 연결해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 배포 전 이미지 취약점 검증
- 배경: 이미지는 OS 패키지, 라이브러리, 설정, Secret을 포함하므로 동일 위험이 여러 Pod로 확산될 수 있음.
- 필요성: CI/CD에서 Trivy로 CVSS 9.0 이상 Critical CVE, Secret, 설정 오류를 차단 기준으로 운영해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Source/Dockerfile -> Image Build -> Trivy Scan -> SBOM/Report
  / Vulnerability DB, Misconfig Rules, Secret Rules, License Rules
SBOM/Report -> CI Gate -> Registry -> Admission/Runtime Evidence
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Image Analyzer | 레이어, OS 패키지, 언어 의존성 식별 | dpkg, rpm, apk, pip, npm, Maven |
| Vulnerability DB | 패키지 버전과 CVE 매칭 | NVD, vendor advisory, GitHub Advisory |
| Misconfig Scanner | Dockerfile, Kubernetes YAML, Terraform 오류 탐지 | root 실행, Privileged, 공개 포트 |
| Secret Scanner | 토큰, API Key, Private Key 패턴 탐지 | Git history와 이미지 파일 모두 점검 |
| CI Gate | Severity, CVSS, allowlist 기준으로 배포 차단 | Critical 0건, High 예외 승인 |
| SBOM Reporter | CycloneDX/SPDX 산출 및 감사 증거 보관 | 이미지 digest와 함께 저장 |

> 요약: Trivy는 이미지 구성요소를 식별해 취약점 DB와 정책 룰에 대조하고 CI/CD 게이트와 SBOM 증거로 연결한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
이미지 빌드 -> 이미지 digest 고정 -> Trivy DB 갱신
-> OS/라이브러리/설정/Secret 분석 -> 심각도 산정
-> 기준 위반 시 Pipeline Fail -> SBOM/리포트 보관
-> Registry Push 또는 배포 차단
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Dockerfile과 base image로 이미지 빌드 | digest 고정, latest 태그 금지 |
| 2 | Trivy 취약점 DB 갱신 후 이미지 분석 | DB age 24시간 이하 |
| 3 | CVE, Misconfig, Secret, License 스캔 | Critical CVE 0건, Secret 0건 |
| 4 | 예외 정책과 severity threshold 적용 | 예외 만료 30일, 승인자 기록 |
| 5 | SBOM, JSON, SARIF 리포트 저장 | CycloneDX/SPDX와 CI 로그 보관 |

> 요약: Trivy 스캔은 빌드 직후 digest 기준으로 수행하고 기준 위반 시 파이프라인을 실패 처리한다.

---

## Ⅳ. 특징

| 구분 | 기존/대안 | Trivy 이미지 스캔 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 검사 범위 | OS 패키지 위주 CVE 점검 | CVE, IaC Misconfig, Secret, License | Critical 0건, Secret 0건 |
| 적용 시점 | 운영 배포 후 취약점 점검 | Pull Request, Build, Registry, Cluster | 배포 전 차단률 100% |
| 증거 | 텍스트 리포트 | SBOM, JSON, SARIF, image digest | CycloneDX/SPDX 보관 |
| 한계 | DB와 매칭 품질 의존 | 오탐·누락·vendor backport 검토 필요 | 예외 만료 30일, 재스캔 24시간 |

> 요약: Trivy는 이미지 위험을 배포 전에 정량 기준으로 차단하지만 DB 품질과 예외 관리 절차가 함께 필요하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | Trivy 이미지 스캔 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 수동 CVE 확인 | CI/CD 자동 스캔과 Registry 재스캔 | 일 배포 10회 이상, 이미지 50개 이상 |
| 비용/성능 | 운영 패치 중심 | 빌드 단계 실패 처리로 조치 비용 감소 | 빌드 지연 허용 2분 이내 |
| 운영/위험 | 운영 중 탐지 후 조치 | 배포 전 차단, SBOM 증거, 예외 만료 | 규제·감사 대상 워크로드 |

> 요약: 컨테이너 배포 빈도가 높으면 운영 사후 조치보다 Trivy 기반 CI/CD 게이트가 조치 비용을 줄인다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 오탐 | vendor backport, CVE 매칭 오류 | allowlist, 근거 URL, 만료일 지정 | 예외 30일 만료율 100% |
| 누락 | 패키지 식별 실패, 정적 링크 바이너리 | SBOM 보강, 다중 스캐너 교차검증 | 미식별 패키지 비율 5% 이하 |
| DB 지연 | 취약점 DB 갱신 지연 | DB age 24시간 이하, 재스캔 | DB 갱신 실패 0건 |
| 우회 배포 | CI 외부 Registry Push | Registry 정책, Admission digest 검증 | unsigned image 0건 |

> 요약: 스캔 품질은 오탐·누락·DB 지연·우회 배포를 예외 정책과 Admission 검증으로 통제해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 취약점 기준 | Critical 0건, High는 승인 예외만 허용 | Trivy JSON, CI 로그 |
| Secret 기준 | API Key·Private Key 0건 | Trivy secret scan, Git secret scan |
| SBOM 기준 | 운영 이미지 100% CycloneDX/SPDX 보관 | Registry digest와 SBOM 매핑 |
| 재스캔 기준 | 운영 이미지 24시간 또는 신규 CVE 발생 시 | Registry scheduled scan |

> 요약: Trivy 운영 성과는 Critical·Secret 0건, SBOM 100%, 재스캔 주기 준수로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 1단계: Pull Request에서 Dockerfile, IaC, Secret Scan을 수행하고 Secret 0건 기준 미달 시 병합 차단
2. 2단계: Build 후 Trivy image scan으로 Critical CVE 0건, High CVE 예외 30일, DB age 24시간 이하 기준 적용
3. 3단계: SBOM을 CycloneDX/SPDX로 저장하고 Cosign 서명, OPA Gatekeeper Admission 정책으로 서명·스캔 증거 검증

**결론 (2줄):**
- 기술사 판단: 테스트용 이미지 10개 미만은 수동 재스캔으로 시작 가능하나, 운영 배포는 Trivy 기반 CI/CD 게이트와 Admission 검증을 결합해야 함
- 향후 방향: SBOM, VEX, 이미지 서명, 런타임 탐지를 연결해 빌드 시점 위험과 실행 시점 위험을 동일 증거 체계로 관리해야 함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "컨테이너 이미지 스캔을 설명하시오", "Trivy를 기술하시오" | 이미지 분석, CVE 매칭, SBOM 산출 흐름 | Trivy의 검사 범위와 한계 |
| 요구사항 명시형 | "CI/CD 적용 방안을 제시하시오", "이미지 보안 게이트를 설계하시오" | Pipeline Fail 기준, 예외 만료, Registry 재스캔 | Critical 0건, Secret 0건, 서명 100% 방안 |

> 요약: 설명형은 스캔 원리를 쓰고, 설계형은 CI/CD 차단 기준과 예외 관리 지표를 중심으로 답안을 전개한다.
