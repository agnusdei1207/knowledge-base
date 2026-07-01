---
title: "정적 분석 SAST (Static Application Security Testing)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 75
---

# 📖 【암기용】 개념 완전 이해

> 목적: SAST를 처음 봐도 소스 코드 기반 보안 결함 탐지와 PR gate 관점에서 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: SAST는 실행 전 소스 코드·바이트코드·바이너리를 분석해 취약 패턴을 찾는 보안 테스트임
- **왜 필요한가**: 취약점은 운영 배포 후 발견하면 수정 비용과 노출 시간이 커짐. SAST는 개발 단계에서 CWE 기반 결함을 차단함.
- **핵심 직관**: 자동차를 도로에 내보내기 전 설계도와 배선을 검사해 화재 가능 지점을 찾는 방식임.

## 깊이 이해
- **배경·문제의식**: SQL Injection, XSS, Command Injection은 입력값이 검증 없이 위험 함수로 흐를 때 발생함. 코드 리뷰만으로 모든 경로를 찾기 어려워 자동 분석이 필요함.
- **작동 원리**: SAST는 source, sink, sanitizer를 모델링하고 taint analysis로 데이터 흐름을 추적함. 규칙은 CWE, OWASP ASVS, 사내 secure coding 기준과 매핑함.
- **비유**: 수도관 도면에서 오염원이 정수 필터를 거치지 않고 식수관으로 연결되는 경로를 찾는 작업과 같음.
- **구체 예시**: 사용자 입력 `request.getParameter()`가 검증 없이 SQL 문자열 결합 후 `executeQuery()`로 전달되면 CWE-89로 탐지하고 PR 병합을 차단함.
- **흔한 오해·주의점**: SAST는 실행 환경 취약점을 모두 찾지 못함. 인증 우회, 런타임 설정, 비즈니스 로직 결함은 DAST·수동 점검과 병행해야 함.

## 연결 개념
- DAST — 실행 중 애플리케이션을 외부에서 점검하는 보완 테스트
- CWE — 취약 패턴 분류 체계
- DevSecOps — CI/CD에 보안 테스트를 내재화하는 운영 방식

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: SAST는 코드 실행 전 source/sink/taint 분석으로 CWE 결함을 찾아 PR 단계에서 차단하는 Shift-Left 보안 통제이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SAST는 소스 코드 또는 중간 산출물을 정적으로 분석해 보안 취약 패턴과 데이터 흐름 결함을 탐지하는 테스트이다.
> 2. **가치**: PR gate에서 critical 취약점 0건, CWE 매핑 100%, 수정 리드타임 7일 이하를 목표로 개발 초기에 결함을 제거함.
> 3. **판단 포인트**: false positive를 줄이기 위한 rule tuning과 DAST·SCA·수동 점검 보완이 필요함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 보안 테스트 원리 확인 | source/sink/sanitizer, taint analysis, CWE | 단순 코드 스타일 검사로 축소 |
| DevSecOps 적용 판단 확인 | PR gate, CI 연동, severity 기준 | 운영 배포 후 스캔만 제시 |
| 한계 인식 확인 | false positive, 런타임 맥락 부족, DAST 보완 | SAST로 모든 취약점 탐지 가능하다고 단정 |

> 요약: 이 문제는 정적 분석 원리와 CI 보안 게이트 설계를 함께 쓰는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

SAST는 실행 전 코드 보안 분석이다.
소프트웨어 취약점은 개발 단계에서 발견할수록 수정 비용과 노출 시간이 감소함.
SAST는 CWE·OWASP 기준으로 입력 검증 누락, 위험 API 사용, 인증·인가 코드 결함을 PR 단계에서 차단하는 Shift-Left 통제임.

---

## Ⅱ. 구조 및 구성요소

```text
Source Code -> Parser / AST -> Data Flow Graph
  -> Source / Sink / Sanitizer Model
  -> Rule Engine -> CWE Finding -> PR Gate
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Parser/AST | 언어별 구문 구조 분석 | Java, JS, Python별 모델 필요 |
| Taint Engine | 입력값 흐름 추적 | source -> sanitizer -> sink 검증 |
| Rule Set | 취약 패턴 기준 | CWE, OWASP Top 10, 사내 규칙 |
| Finding DB | 탐지 결과 저장·추적 | severity, owner, SLA |
| PR Gate | 병합 허용 여부 결정 | critical 0건, high SLA 7일 |

> 요약: SAST 구조는 코드 파싱, 데이터 흐름 추적, 규칙 매칭, 결과 추적, PR 게이트로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Developer PR -> SAST Scan -> Source/Sink Trace
  -> CWE Mapping -> Severity Scoring
  -> False Positive Triage -> Block / Approve / Ticket
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | PR 생성 시 코드 스캔 실행 | 변경 라인 포함, scan time 10분 이하 |
| 2 | source에서 sink까지 taint path 분석 | sanitizer 존재 여부 확인 |
| 3 | CWE·OWASP 항목으로 취약점 분류 | CWE-79, CWE-89 등 매핑 |
| 4 | 심각도와 오탐 여부 판정 | critical/high 우선 triage |
| 5 | 차단·승인·티켓화 결정 | critical 0건, SLA 추적 |

> 요약: SAST는 PR 단위로 데이터 흐름을 추적하고 CWE와 심각도를 기준으로 병합 허용 여부를 결정한다.

---

## Ⅳ. 특징

| 구분 | 수동 코드 리뷰 | SAST | 정량 기준 |
|:---|:---|:---|:---|
| 시점 | 리뷰어 확인 시 | commit·PR·nightly | PR마다 자동 실행 |
| 범위 | 리뷰 변경분 중심 | 전체 코드·호출 경로 | scan coverage 90% 이상 |
| 원리 | 경험 기반 판정 | AST, CFG, taint analysis | CWE 매핑 100% |
| 한계 | 누락 가능성 | false positive 발생 | 오탐률 20% 이하 목표 |
| 통제 | 리뷰 코멘트 | quality/security gate | critical 0건 |

> 요약: SAST는 반복 가능한 자동 보안 분석을 제공하지만 오탐 관리와 런타임 보완 테스트가 필요하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | DAST는 실행 앱 점검 | SAST는 코드 흐름 분석 | 개발 초기 결함 제거 시 SAST |
| 비용/성능 | 수동 리뷰는 인력 의존 | 자동 스캔으로 반복 통제 | PR scan 10분 이하 |
| 운영/위험 | 배포 후 탐지 | 병합 전 차단 | critical 취약점 릴리스 차단 |
| 보완 | SCA는 오픈소스 취약점 | SAST는 자체 코드 결함 | 둘 다 CI에 포함 |

> 요약: SAST는 자체 코드 취약점 조기 탐지에 적합하며, 런타임 취약점은 DAST로 보완한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| false positive | 프레임워크 sanitizer 미인식 | rule tuning, suppress 승인 | 오탐률 20% 이하 |
| false negative | 동적 실행 경로 미분석 | DAST, 보안 리뷰 병행 | 운영 취약점 재발률 |
| 개발 지연 | 스캔 시간 과다 | incremental scan, cache | PR scan 10분 이하 |
| 경고 무시 | finding 과다 | severity gate, SLA 분리 | high SLA 준수율 |

> 요약: SAST 리스크는 규칙 튜닝, 보완 테스트, 스캔 시간, 경고 SLA로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 보안 품질 | critical 0건, high 7일 내 조치 | SAST dashboard |
| 분석 범위 | 주요 repo scan coverage 90% 이상 | CI 실행 이력 |
| 탐지 정확도 | false positive 20% 이하 | triage 결과 집계 |
| 처리 속도 | PR scan 10분 이하 | CI duration metric |

> 요약: SAST 성공 여부는 critical 차단, 분석 범위, 오탐률, PR 스캔 시간으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. GitHub Actions 또는 Jenkins PR pipeline에 CodeQL, Semgrep, SonarQube를 연결하고 critical/high finding은 병합 차단으로 설정함.
2. CWE-79, CWE-89, CWE-22, CWE-78 등 사내 사고 유형을 우선 규칙으로 구성하고 framework sanitizer를 등록해 오탐률을 낮춤.
3. SAST 결과를 Jira 티켓과 연동해 owner, severity, SLA 7/30/90일을 추적하고 보안 예외는 만료일과 승인자를 기록함.

**결론 (2줄):**
- 기술사 판단: 자체 코드 취약점이 주요 리스크인 서비스는 SAST를 PR gate에 배치하고, 인증·세션·런타임 결함은 DAST와 수동 점검을 병행함.
- 향후 방향: SAST는 AI code review, SBOM, SCA, 정책형 보안 게이트와 결합해 DevSecOps 표준 통제로 발전함.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "SAST를 설명하시오", "기술하시오" | taint analysis, CWE mapping, PR gate 흐름 | 수동 리뷰·DAST와 차이 |
| 요구사항 명시형 | "보안 테스트 방안을 제시하시오", "비교하시오" | severity gate, false positive triage | SAST·DAST·SCA 조합과 운영 지표 |

> 요약: 설명형은 분석 원리를, 방안형은 CI 게이트와 오탐 관리, 보완 테스트 중심으로 전개한다.
