---
title: "OWASP Top 10 (OWASP Top 10)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 69
---

# 📖 【암기용】 개념 완전 이해

> 목적: OWASP Top 10을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 웹 애플리케이션에서 가장 중요한 보안 위험 10개를 정리한 OWASP의 인식·교육 기준
- **왜 필요한가**: 웹 보안은 취약점 종류가 많아 우선순위가 흐려지기 쉽다. Top 10은 접근통제, 오설정, 공급망, 암호, 인젝션 등 고위험군을 먼저 보게 한다.
- **핵심 직관**: 병원 응급실의 중증도 분류처럼 모든 약점을 같은 무게로 보지 않고 자주 발생하고 피해가 큰 위험군부터 관리하는 목록이다.

## 깊이 이해
- **배경·문제의식**: 개발팀은 SQL Injection, XSS 같은 공격명을 외워도 실제 설계에서는 인증, 권한, 로깅, 공급망 통제를 놓친다. OWASP Top 10은 기술 결함을 위험군으로 묶어 SSDLC와 보안 테스트 우선순위를 제시한다.
- **작동 원리**: 2025 기준은 Broken Access Control, Security Misconfiguration, Software Supply Chain Failures, Cryptographic Failures, Injection, Insecure Design, Authentication Failures, Software or Data Integrity Failures, Security Logging and Alerting Failures, Mishandling of Exceptional Conditions를 포함한다.
- **비유**: 자동차 정비에서 엔진, 브레이크, 타이어, 전자장치, 사고기록을 우선 점검하는 표준 체크리스트와 같다.
- **구체 예시**: 신규 API 출시 전 threat modeling, SAST/DAST, SCA/SBOM, access control test, security header, structured logging을 pipeline gate로 구성하면 Top 10 위험군을 SDLC 단계에서 줄일 수 있다.
- **흔한 오해·주의점**: OWASP Top 10은 상세 보안 요구사항 전체가 아니다. ASVS, SAMM, Cheat Sheet, Testing Guide와 함께 써야 설계·구현·검증 수준을 정량화할 수 있다.

## 연결 개념
- SSDLC - 요구사항, 설계, 구현, 테스트, 운영 단계 보안 내재화
- ASVS/SAMM - OWASP Top 10을 상세 요구사항과 성숙도로 확장
- SAST/DAST/SCA - 코드, 실행, 의존성 관점의 검증 도구

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: OWASP Top 10 답안은 위험군 암기가 아니라 신뢰 경계, 공격 흐름, SSDLC 통제, 로그 지표를 연결해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: OWASP Top 10은 웹 애플리케이션의 주요 보안 위험군을 우선순위화한 표준 인식 문서임.
> 2. **가치**: 개발·테스트·운영 단계에서 접근통제, 오설정, 공급망, 암호, 인젝션 등 반복 위험을 선별해 통제함.
> 3. **판단 포인트**: Top 10 항목을 취약점 이름으로 외우지 말고 ASVS, SAST/DAST/SCA, 로그·알림, 재검증과 연결해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 웹 보안 위험군 이해 확인 | 2025 Top 10, 2021 기출 관점, 위험군 개념 | SQLi·XSS만 나열 |
| SSDLC 적용 판단 확인 | threat modeling, secure coding, test gate, SCA/SBOM | 개발 이후 점검만 제시 |
| 운영 통제 확인 | logging, alerting, WAF, retest, KPI | 탐지·재검증 지표 누락 |

> 요약: 이 문제는 OWASP Top 10을 웹 보안 우선순위와 SSDLC 통제 체계로 전환하는 답안을 요구함.

---

## Ⅰ. 개요 및 필요성

- 개요: 웹 위험 우선순위
- 배경: 웹 애플리케이션은 외부 입력, 인증, 세션, API, DB, 의존성 경계가 많아 Injection, 접근통제 실패, 오설정이 반복됨.
- 필요성: OWASP Top 10 2021과 ASVS 기준으로 설계 리뷰, SAST·DAST, 침투테스트 항목을 매핑해 릴리스 전 취약군을 선별해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
요구사항/설계 -> OWASP Top 10 위험군 매핑 -> SSDLC 통제
              -> SAST/DAST/SCA/API test -> WAF/Logging
              -> 취약점 조치 -> 재검증/지표 관리
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| 위험군 목록 | 웹 보안 우선순위 제시 | 2025 A01~A10, 2021 기출 관점 병기 |
| SSDLC 통제 | 설계부터 운영까지 보안 내재화 | threat modeling, secure coding |
| 검증 도구 | 코드·실행·의존성 취약점 확인 | SAST, DAST, SCA, API fuzzing |
| 운영 통제 | 공격 탐지와 보완 통제 | WAF, SIEM, alert, rate limit |
| 개선 지표 | 조치율과 재발률 측정 | critical SLA 7일, 재검증 통과율 |

> 요약: OWASP Top 10은 목록 자체보다 위험군을 SSDLC, 테스트, 운영 로그, 재검증 지표로 연결하는 구조가 핵심임.

---

## Ⅲ. 동작원리 및 흐름도

```text
기능 요구 분석 -> 신뢰 경계 식별 -> Top 10 위험 매핑
-> 설계 통제 선정 -> 구현/테스트 gate -> 배포
-> 로그/알림 모니터링 -> 조치와 retest
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | API, 인증, 데이터 흐름, 외부 의존성 식별 | data flow diagram 작성 |
| 2 | A01~A10 위험군과 통제 매핑 | ASVS requirement 매핑률 90% |
| 3 | SAST/DAST/SCA/API test 수행 | critical 배포 차단 100% |
| 4 | WAF, 로그, alert로 운영 탐지 | security event 누락 0건 |
| 5 | 취약점 조치 후 재검증 | critical 7일, high 30일 SLA |

> 요약: Top 10 적용은 설계 단계의 신뢰 경계 분석부터 배포 후 로그 기반 재검증까지 이어지는 SSDLC 흐름임.

---

## Ⅳ. 특징

| 구분 | 단순 취약점 목록 | OWASP Top 10 기반 관리 | 수치/판단 포인트 |
|:---|:---|:---|:---|
| 관점 | 공격명 중심 | 위험군과 통제 우선순위 | A01~A10 coverage 90% |
| 적용 시점 | 진단 후 조치 | 요구사항, 설계, 개발, 운영 | pipeline gate 100% |
| 검증 범위 | SQLi, XSS 편중 | 접근통제, 오설정, 공급망 포함 | SCA/SBOM 적용률 100% |
| 운영 연계 | 보고서 종료 | 로그, 알림, retest | critical SLA 7일 |

> 요약: OWASP Top 10은 취약점 암기표가 아니라 웹 보안 통제를 SDLC와 운영 지표로 묶는 우선순위 체계임.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 점검 항목 기반 보안 | 위험군 기반 SSDLC | 신규 웹/API 서비스 개발 시 |
| 비용/운영 | 출시 후 진단 | pipeline gate와 자동화 검사 | 배포 주기 주 1회 이상 |
| 위험 통제 | 발견 취약점 조치 | 설계 결함과 공급망까지 통제 | 개인정보·결제·외부 API 보유 |

> 요약: 배포 빈도가 높고 외부 API가 많은 시스템은 출시 후 진단보다 Top 10 기반 SSDLC gate가 적합함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 목록 암기화 | 항목명만 교육 | ASVS 요구사항과 테스트 케이스 연결 | requirement mapping 90% |
| 설계 결함 누락 | 구현 취약점 검사 편중 | threat modeling, abuse case | 설계 리뷰 100% |
| 공급망 공백 | SCA/SBOM 미적용 | dependency scan, SBOM, VEX | critical CVE SLA 7일 |
| 탐지 부재 | 로깅·알림 설계 누락 | structured log, SIEM use case | alert false negative 0건 목표 |

> 요약: Top 10의 실패 원인은 목록 암기와 후행 점검이며, ASVS·threat modeling·SCA·로그 설계로 보완함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 위험군 커버리지 | A01~A10 테스트 90% 이상 | test case matrix |
| 배포 차단 | critical 취약점 gate 100% | CI/CD 보안 검사 로그 |
| 조치 속도 | critical 7일, high 30일 | vulnerability ticket |
| 재검증 | retest pass 95% 이상 | DAST/SAST 재실행 결과 |

> 요약: 성과는 Top 10 항목 암기가 아니라 테스트 커버리지, gate 차단률, 조치 SLA, 재검증 통과율로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 설계 단계: DFD와 threat modeling으로 접근통제, 인증, 외부 호출, 데이터 저장 신뢰 경계를 식별하고 ASVS 요구사항에 매핑함.
2. 개발·검증 단계: SAST, DAST, SCA, API fuzzing, secret scan을 CI/CD gate에 연결해 critical 취약점 배포를 100% 차단함.
3. 운영 단계: WAF, API gateway, structured logging, SIEM alert를 적용하고 critical 7일, high 30일 SLA와 retest pass 95%를 관리함.

**결론 (2줄):**
- 기술사 판단: 교육·우선순위 목적은 OWASP Top 10, 상세 요구사항과 평가 기준은 ASVS/SAMM을 함께 적용해야 함.
- 향후 방향: 2025 기준의 공급망, 오설정, 예외 처리 위험을 포함해 웹 보안을 코드, 의존성, 운영 로그까지 확장해야 함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "OWASP Top 10을 설명하시오" | A01~A10 위험군과 SSDLC 적용 흐름 | 단순 취약점 목록과 위험군 관리 차이 |
| 요구사항 명시형 | "웹 보안 적용 방안을 제시하시오", "개발보안 체계를 설계하시오" | SAST/DAST/SCA, ASVS, 로그·알림 gate | 조치 SLA, retest, 운영 지표 |

> 요약: 설명형은 위험군과 의의, 방안형은 SSDLC gate와 운영 재검증 중심으로 답안을 전환함.
