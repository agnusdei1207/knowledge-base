---
title: "정적 분석 SAST (Static Application Security Testing)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 75
---

# 📖 【암기용】 개념 완전 이해

> 목적: SAST를 처음 봐도 소스 코드 기반 보안 결함 탐지와 PR gate 관점에서 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다. 이 파일은 SAST를 **CWE 분류 체계와 PR 게이트 운영 지표(심각도·SLA)** 관점에서 다룬다(분석 엔진의 원리·AST·SCA/IAST 비교는 075_sast_static_analysis.md 참고).

## 한눈에
- **개요**: **SAST(정적 애플리케이션 보안 테스트)**는 소스코드를 실행하지 않고 정적으로 분석해 **CWE(Common Weakness Enumeration)** 취약 패턴을 찾아내고, 그 결과를 PR(Pull Request) 병합 여부를 결정하는 **보안 게이트**로 운영하는 테스트다.
- **왜 필요한가**: 취약점을 찾는 것보다 "찾은 취약점을 누가, 언제까지, 어떤 기준으로 처리할지"가 더 중요하다. 이 기준이 없으면 경고만 쌓이고 아무도 고치지 않는다. CWE 분류와 심각도(Severity)·SLA(처리 기한) 기준을 세워야 SAST가 실제로 운영된다.
- **핵심 직관**: SAST 결과는 판결문이 아니라 공항 검문소의 통과/차단 규칙이다. 위험도(심각도)에 따라 어떤 것은 즉시 병합을 막고(critical), 어떤 것은 티켓만 만들어 나중에 처리한다(low/medium).

## 핵심 용어 정리
| 용어 | 의미 | 비유 |
|:---|:---|:---|
| SAST | 실행 전 소스코드를 정적 분석해 취약점을 찾는 테스트 | 원고 교정 |
| CWE (Common Weakness Enumeration) | 취약점 유형을 번호로 표준화한 분류 체계 | 질병을 코드 번호로 통일한 분류표 |
| Source / Sink / Sanitizer | 오염원 입력 / 위험한 실행 지점 / 이를 안전하게 걸러주는 필터 | 오염수 발생지 / 취수구 / 정수 필터 |
| Taint Analysis | source에서 sink까지 값이 sanitizer 없이 도달하는지 추적하는 분석 | 물줄기를 끝까지 따라가 보는 것 |
| Severity (심각도) | 발견된 취약점의 위험 등급(critical/high/medium/low) | 응급실 트리아지 등급 |
| PR Gate (보안 게이트) | 심각도 기준으로 코드 병합을 자동 차단·승인하는 CI 관문 | 공항 보안검색대 |
| SLA (처리 기한) | 심각도별로 며칠 안에 고쳐야 하는지 정한 약속 | 민원 처리 기한 |
| False Positive / False Negative | 안전한데 위험하다고 오판 / 위험한데 못 잡음 | 가짜 경보 / 못 본 척 지나감 |

## 깊이 이해

### CWE로 분류하는 이유 — 구체 번호 예
- 같은 "입력 검증 누락"이라도 그 값이 어디로 흘러가는지에 따라 다르게 분류된다. SQL 문자열에 들어가면 CWE-89(SQL Injection), HTML에 그대로 출력되면 CWE-79(XSS), 파일 경로에 들어가면 CWE-22(Path Traversal), 시스템 명령어에 들어가면 CWE-78(OS Command Injection)로 번호가 갈린다.
- 번호로 통일하면 SonarQube, CodeQL, Semgrep처럼 도구가 달라도 같은 취약점을 같은 이름(CWE ID)으로 취급할 수 있어, 조직 전체의 보안 지표를 하나의 기준으로 집계할 수 있다.

### source/sink/sanitizer 판정 흐름 — 구체 예제
- `request.getParameter("id")`가 source, `executeQuery(sql)`가 sink다. 이 둘 사이에 `PreparedStatement`처럼 파라미터를 바인딩하는 처리(sanitizer)가 있으면 안전 판정, 문자열을 그대로 이어붙이면(`"SELECT ... WHERE id=" + id`) 위험 판정한다. source에서 sink까지 이 경로를 추적하는 과정이 Taint Analysis다.

### 심각도-SLA를 수치로 운영하는 법
- critical(원격 코드 실행, SQL 인젝션 등)은 발견 즉시 PR 병합 자체를 막는다(허용 건수 0).
- high는 7일 이내, medium은 30일 이내, low는 90일 이내 처리를 SLA로 정해 Jira 티켓의 기한으로 관리한다.
- 이렇게 숫자로 정해두지 않으면 심각도가 낮은 경고 수천 건에 묻혀 정작 critical 항목도 방치되는 일이 발생한다.

### 오탐·미탐 관리 원리
- 오탐률(false positive rate)을 지표로 관리한다(예: 20% 이하를 목표로 삼는 식). 오탐이 계속 나오는 규칙은 사내 프레임워크의 sanitizer 함수를 SAST 엔진에 등록해 줄인다.
- 반대로 SAST가 원천적으로 볼 수 없는 영역(인증 우회, 런타임 설정 같은 미탐 가능 영역)은 DAST와 수동 보안 점검으로 보완한다. 오탐은 규칙 튜닝으로, 미탐은 다른 테스트 기법 병행으로 다루는 것이 원리다.

### PR 병합을 막을지 판별하는 원리
- "이 PR을 막을 것인가"는 심각도 하나만 보지 않는다. CWE 유형(원격에서 악용 가능한지)과 sanitizer 존재 여부를 함께 본다 — 동일한 CWE라도 sanitizer가 확인되면 위험도를 낮춰 자동 승인할 수 있고, sanitizer가 없으면 심각도와 무관하게 리뷰를 요구할 수 있다.

## 연결 개념
- DAST — 런타임에서 외부 공격을 재현해 SAST가 못 보는 영역을 보완하는 테스트
- DevSecOps — 심각도·SLA·PR 게이트를 CI/CD에 내재화하는 운영 철학
- 075_sast_static_analysis — 같은 SAST를 AST 파싱·결함 비용 곡선·SCA/IAST 비교 같은 분석 원리와 파이프라인 구조 관점에서 다룸

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

- 개요: 실행 전 코드 보안 분석
- 배경: 소프트웨어 취약점은 운영 배포 후 발견되면 수정 범위, 노출 시간, 재배포 절차가 함께 증가한다.
- 필요성: SAST는 CWE·OWASP 기준으로 입력 검증 누락, 위험 API 사용, 인증·인가 코드 결함을 PR 단계에서 차단하는 Shift-Left 통제이다.

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

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
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
