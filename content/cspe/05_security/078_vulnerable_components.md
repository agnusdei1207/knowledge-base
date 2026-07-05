---
title: "취약한 의존성 컴포넌트 (Vulnerable Components)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 78
---

# 📖 【암기용】 개념 완전 이해

> 목적: 취약한 의존성 컴포넌트를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 애플리케이션이 사용하는 라이브러리·프레임워크·컨테이너 이미지에 알려진 취약점이 포함된 상태
- **왜 필요한가**: 직접 작성한 코드가 안전해도 Log4j, OpenSSL, Spring, base image 같은 의존성 하나가 RCE·정보유출 경로가 될 수 있음.
- **핵심 직관**: 집을 직접 지었어도 문손잡이, 보일러, 공유기 부품에 리콜 결함이 있으면 전체 집이 위험해짐.

## 깊이 이해
- **배경·문제의식**: 현대 소프트웨어는 오픈소스와 SaaS SDK에 의존한다. transitive dependency는 개발자가 직접 선언하지 않아도 빌드 결과물에 포함되며, 취약 버전이 운영 이미지에 남을 수 있다.
- **작동 원리**: SBOM으로 구성품 목록을 만들고, SCA가 CVE/NVD/OSV와 버전을 대조한다. CVSS, EPSS, KEV, exploit 가능성, 자산 중요도로 패치 우선순위를 정함.
- **비유**: 식품 제조사가 원재료 공급망의 알레르기 성분과 리콜 이력을 관리하듯, 소프트웨어도 패키지와 하위 패키지 이력을 추적해야 함.
- **구체 예시**: `log4j-core 2.14.1`이 포함된 서비스는 직접 로깅 코드를 보지 않아도 CVE-2021-44228 영향권이다. SCA로 탐지 후 2.17.1 이상 업그레이드와 재빌드가 필요함.
- **흔한 오해·주의점**: 취약점 수가 많다고 모두 즉시 패치하는 것이 아니다. internet-facing RCE, KEV 등재, exploit code, 데이터 접근 권한을 기준으로 SLA를 나눠야 함.

## 연결 개념
- SBOM - SPDX, CycloneDX 형식의 소프트웨어 구성품 명세
- SCA - 의존성 버전과 CVE 정보를 자동 대조하는 분석
- Patch Management - 버전 고정, 테스트, 배포, 재검증 절차

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 취약 컴포넌트 답안은 CVE 나열이 아니라 SBOM 기반 식별, SCA 탐지, 우선순위, 패치 SLA, 재빌드 검증으로 구성해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Vulnerable Components는 라이브러리, 프레임워크, OS package, container image에 알려진 취약 버전이 포함된 상태임.
> 2. **가치**: SBOM, SCA, CVE/CVSS, EPSS, KEV, version pinning으로 공급망 취약점을 추적·조치함.
> 3. **판단 포인트**: 영향 자산, exploit 가능성, 패치 호환성, 배포 SLA, 재스캔 결과를 연결해 작성해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 의존성 위험 이해 확인 | direct/transitive dependency, container base image | 라이브러리 업데이트만 단순 기재 |
| 공급망 통제 설계 확인 | SBOM, SCA, CVE, version pinning, patch SLA | SBOM·CI/CD 검증 누락 |
| 운영 우선순위 판단 확인 | CVSS, EPSS, KEV, 인터넷 노출, exploit code | CVSS 점수만으로 조치 순서 결정 |

> 요약: 이 문제는 취약 버전 식별보다 어떤 서비스부터 어떤 SLA로 패치하고 재검증할지 묻는 공급망 보안 문제임.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **개요** | 애플리케이션이 사용하는 라이브러리·프레임워크·컨테이너 이미지에 알려진 취약점이 포함된 상태 | "이 개념의 핵심" |
| **왜 필요한가** | 직접 작성한 코드가 안전해도 Log4j, OpenSSL, Spring, base image 같은 의존성 하나가 RCE·정보유출 경로가 될 ... | "일지 기록" |
| **핵심 직관** | 집을 직접 지었어도 문손잡이, 보일러, 공유기 부품에 리콜 결함이 있으면 전체 집이 위험해짐 | "이 개념의 핵심" |
| **배경·문제의식** | 현대 소프트웨어는 오픈소스와 SaaS SDK에 의존한다 | "요리 도구 세트" |
| **작동 원리** | SBOM으로 구성품 목록을 만들고, SCA가 CVE/NVD/OSV와 버전을 대조한다 | "이 개념의 핵심" |
| **비유** | 식품 제조사가 원재료 공급망의 알레르기 성분과 리콜 이력을 관리하듯, 소프트웨어도 패키지와 하위 패키지 이력을 추적해야 함 | "이 개념의 핵심" |
| **구체 예시** | `log4j-core 2 | "일지 기록" |

---


## Ⅰ. 개요 및 필요성

- 개요: 의존성 기반 취약점
- 배경: 오픈소스, OS package, container image, SaaS SDK는 transitive dependency로 포함되어 운영자가 직접 선언하지 않은 취약 버전이 배포될 수 있음.
- 필요성: SBOM, SCA, CVE/NVD feed, SPDX·CycloneDX 형식을 CI/CD에 연결해 배포 전·후 취약 버전을 식별해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
소스/패키지 선언 -> 의존성 해석 -> SBOM 생성 -> SCA 대조 -> 우선순위 -> 패치/재빌드 -> 재스캔
  / direct, transitive, OS package, container image
  / CVE, CVSS, EPSS, KEV, exploit code
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| SBOM | 소프트웨어 구성품, 버전, 라이선스 목록화 | SPDX, CycloneDX |
| SCA Engine | 패키지 버전과 취약점 DB 대조 | NVD, OSV, GitHub Advisory |
| Risk Scoring | 자산 중요도와 exploit 가능성 반영 | CVSS, EPSS, KEV, internet-facing |
| Patch Pipeline | version pinning, 테스트, 재빌드, 배포 | lockfile, container rebuild |

> 요약: 취약 컴포넌트 관리는 SBOM으로 목록을 만들고 SCA와 위험 점수로 조치 순서를 정하는 구조임.

---

## Ⅲ. 동작원리 및 흐름도

```text
commit/package update -> dependency resolve -> SBOM 생성
  / library, framework, base image
CVE 대조 -> 위험도 산정 -> merge 차단/예외 승인 -> 패치 -> 재스캔
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | manifest, lockfile, image에서 구성품 추출 | SBOM 생성률 95% 이상 |
| 2 | SCA가 CVE, CVSS, EPSS, KEV와 매칭 | critical 누락 0건 |
| 3 | 노출도·업무 중요도·exploit로 우선순위 산정 | KEV/RCE 24시간 SLA |
| 4 | 버전 고정, 테스트, 재빌드, 재배포 후 재스캔 | critical/high 잔존 0건 |

> 요약: 의존성 추출, 취약점 대조, 위험 기반 우선순위, 패치 재검증 순서로 운영됨.

---

## Ⅳ. 특징

| 구분 | 수동 업데이트 | SBOM/SCA 기반 관리 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 식별 범위 | 직접 선언 패키지 | direct, transitive, OS package | 구성품 coverage 95% 이상 |
| 우선순위 | 개발팀 판단 | CVSS+EPSS+KEV+노출도 | KEV/RCE 24시간 |
| 배포 통제 | 릴리스 후 확인 | PR/CI merge gate | critical merge 차단 100% |
| 증거 | 업데이트 내역 | SBOM, scan report, ticket | 감사 증적 보존 1년 |

> 요약: 취약 컴포넌트 대응은 업데이트 작업보다 구성품 식별 범위와 CI/CD 차단 기준이 핵심임.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 패키지명 수동 관리 | SBOM + SCA + artifact scan | 서비스 수 10개 이상, 이미지 배포 빈도 주 1회 이상 |
| 비용/성능 | 즉시 최신 버전 반영 | version pinning + staged rollout | 호환성 테스트 실패율과 exploit 위험 비교 |
| 운영/위험 | 월간 패치 | 위험기반 SLA | 인터넷 노출 RCE, KEV 등재 시 emergency patch |

> 요약: 취약 컴포넌트는 모든 업데이트를 동일하게 처리하지 않고 exploit 가능성과 업무 영향으로 SLA를 나눠야 함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Transitive 누락 | 하위 의존성 추적 부재 | lockfile scan, dependency graph | transitive coverage 95% 이상 |
| 패치 회귀 | major version 변경 | regression test, canary 10%, rollback plan | 배포 실패율 5% 이하 |
| 이미지 잔존 | base image 재빌드 누락 | image digest pinning, registry scan | critical image 0건 |

> 요약: 하위 의존성, 회귀, 이미지 잔존을 lockfile, canary, registry scan으로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 식별 | SBOM 생성률 95% 이상 | CI artifact, CycloneDX report |
| 조치 | critical/KEV 24시간, high 7일 | vulnerability ticket, SLA dashboard |
| 검증 | 재스캔 critical/high 0건 | SCA, container registry scan |

> 요약: 성공 여부는 SBOM 생성률, 패치 SLA, 재스캔 잔존 취약점으로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 식별 체계: 모든 build artifact에 CycloneDX SBOM을 생성하고 package lockfile, container image digest, OS package 목록을 보관함.
2. CI/CD 통제: SCA와 registry scan을 merge gate로 연결해 KEV/RCE critical은 배포 차단, 예외는 owner·만료일·보완통제를 기록함.
3. 패치 운영: version pinning, regression test, canary 10%, rollback plan을 적용하고 critical 24시간, high 7일 SLA로 재스캔까지 완료함.

**결론 (2줄):**
- 기술사 판단: 인터넷 노출 RCE와 KEV 등재 취약점은 emergency patch, 내부 저위험 라이브러리는 정기 릴리스와 회귀 테스트를 병행함.
- 향후 방향: 취약 컴포넌트 관리는 SBOM 의무화, VEX, SLSA provenance, artifact signing과 결합한 공급망 보안으로 확장되어야 함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "취약 컴포넌트를 설명하시오" | SBOM 생성, SCA 대조, 패치 재검증 흐름 | 수동 업데이트와 공급망 관리 차이 |
| 요구사항 명시형 | "대응 방안을 제시하시오", "CI/CD 적용을 설계하시오" | merge gate, patch SLA, canary, rollback | CVSS·EPSS·KEV 기반 우선순위 |

> 요약: 설명형은 구성품 식별을, 설계형은 SBOM/SCA를 배포 파이프라인에 넣는 방안을 중심으로 구성함.
