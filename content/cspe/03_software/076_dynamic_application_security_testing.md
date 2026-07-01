---
title: "동적 분석 DAST (Dynamic Application Security Testing)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 76
---

# 📖 【암기용】 개념 완전 이해

> 목적: DAST를 처음 봐도 실행 중인 애플리케이션을 외부 공격자 관점에서 점검하는 방식으로 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: DAST는 실행 중인 웹·API 애플리케이션을 블랙박스 방식으로 스캔해 취약 동작을 찾는 보안 테스트임
- **왜 필요한가**: 코드는 문제없어 보여도 배포 설정, 인증 흐름, 세션 처리, 런타임 구성에서 취약점이 생김. DAST는 실제 요청·응답을 관찰함.
- **핵심 직관**: 완성된 건물에 침입 테스트를 수행해 문, 창문, 출입증 시스템이 실제로 버티는지 확인하는 방식임.

## 깊이 이해
- **배경·문제의식**: 운영 환경의 프록시, WAF, 세션 쿠키, API Gateway 설정은 소스 코드만으로 확인하기 어렵다. DAST는 HTTP 요청을 보내고 응답을 분석해 취약 동작을 확인함.
- **작동 원리**: 크롤러가 화면과 API를 탐색하고, 인증 세션을 유지한 상태에서 SQL Injection, XSS, 인증 우회, 민감정보 노출 페이로드를 전송함.
- **비유**: 설계도가 아니라 실제 매장에 손님과 공격자 역할로 들어가 계산대, 창고, 출입문을 점검하는 방식임.
- **구체 예시**: staging 환경에서 `/api/orders?id=1'` 요청을 보내 SQL 오류 메시지 또는 응답 지연 패턴을 확인해 Injection 가능성을 탐지함.
- **흔한 오해·주의점**: DAST는 코드 내부 경로를 보지 못하므로 false negative가 생김. 인증 크롤링 실패 시 보호된 API는 스캔 범위에서 빠질 수 있음.

## 연결 개념
- SAST — 코드 내부 흐름을 보는 보완 테스트
- API Security Testing — OpenAPI 명세 기반 엔드포인트 점검
- Penetration Test — 수동 공격 시나리오 기반 심층 점검

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: DAST는 실행 애플리케이션을 블랙박스 관점에서 공격해 인증, 세션, API, 배포 설정 관련 런타임 취약점을 검증하는 통제이다.

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: DAST는 실행 중인 웹·API 서비스에 실제 HTTP 요청을 보내 취약 응답과 비정상 동작을 탐지하는 보안 테스트이다.
> 2. **가치**: staging gate에서 OWASP Top 10, 인증 크롤링, API scan을 수행해 배포 전 critical 취약점 0건을 목표로 함.
> 3. **판단 포인트**: 블랙박스 특성상 false negative가 있으므로 인증 설정, 스캔 범위, SAST·수동 점검 보완이 필수임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 동적 보안 테스트 원리 확인 | running app, black-box, request/response 분석 | 소스 코드 분석인 SAST와 혼동 |
| 운영 적용 판단 확인 | auth crawling, API scan, staging gate | 로그인 필요 화면 스캔 누락 |
| 한계와 보완 이해 확인 | false negative, 스캔 범위, SAST 병행 | DAST만으로 전체 보안 검증 완료 주장 |

> 요약: 이 문제는 실행 환경 취약점 검증과 배포 게이트 운영을 함께 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

DAST는 실행 앱 대상 블랙박스 보안 테스트이다.
소스 코드 분석으로는 런타임 설정, 인증 흐름, 세션 쿠키, 서버 오류 노출을 확인하기 어려움.
DAST는 staging 또는 pre-prod 환경에서 실제 공격 페이로드를 전송해 배포 전 취약 동작을 차단함.

---

## Ⅱ. 구조 및 구성요소

```text
Running Web/API App -> Crawler / OpenAPI Import
  -> Auth Session -> Attack Payload Engine
  -> Response Analyzer -> Finding -> Staging Gate
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Crawler | 화면·링크·폼 탐색 | SPA는 JS 렌더링 지원 필요 |
| Auth Handler | 로그인·토큰·세션 유지 | MFA, refresh token 처리 |
| Payload Engine | 공격 입력 생성 | XSS, SQLi, SSRF, path traversal |
| Response Analyzer | 오류·반사·지연 응답 분석 | evidence 기반 finding |
| Staging Gate | 배포 허용 여부 결정 | critical 0건, high 예외 승인 |

> 요약: DAST 구조는 실행 앱 탐색, 인증 유지, 공격 페이로드 전송, 응답 분석, 배포 게이트로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Deploy to Staging -> Seed URL / OpenAPI Spec
  -> Login Session -> Crawl / API Enumerate
  -> Attack Requests -> Analyze Evidence
  -> Block / Approve Release
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | staging 환경에 배포 후 scan target 등록 | 운영 데이터 미사용, 테스트 계정 사용 |
| 2 | 인증 세션 생성과 크롤링 수행 | authenticated coverage 80% 이상 |
| 3 | 웹·API 엔드포인트에 페이로드 전송 | rate limit, WAF 예외 범위 설정 |
| 4 | 응답 코드·본문·시간 기반 evidence 분석 | 재현 가능한 finding 확보 |
| 5 | 배포 승인·차단·예외 처리 | critical 0건, high 승인 기록 |

> 요약: DAST는 staging 배포 후 인증 크롤링과 공격 요청을 수행하고 evidence 기준으로 배포 허용 여부를 결정한다.

---

## Ⅳ. 특징

| 구분 | SAST | DAST | 정량 기준 |
|:---|:---|:---|:---|
| 분석 대상 | 코드·바이트코드 | 실행 앱·API | staging URL, OpenAPI |
| 관점 | 내부 경로 | 외부 공격자 관점 | black-box |
| 탐지 강점 | 코드 흐름 취약점 | 런타임·설정·인증 취약점 | OWASP Top 10 |
| 한계 | 오탐 가능 | 미탐 가능 | authenticated coverage |
| 적용 시점 | PR·CI | staging·pre-prod | release gate |

> 요약: DAST는 실행 환경 취약점 확인에 강점이 있으며 SAST와 결합할 때 탐지 범위가 넓어진다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | SAST는 내부 코드 분석 | DAST는 외부 요청 분석 | 런타임 설정 검증 시 DAST |
| 비용/성능 | 수동 모의해킹 | 자동 반복 스캔 | 릴리스마다 staging scan 필요 시 |
| 운영/위험 | 운영 직접 점검 | 격리 staging 점검 | 운영 데이터 영향 0건 필요 |
| API | 화면 크롤링 중심 | OpenAPI 기반 API scan | API 서비스는 명세 기반 병행 |

> 요약: DAST는 실행 환경과 인증 흐름 검증이 필요한 릴리스 게이트에 적합하며, 코드 결함은 SAST로 보완한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| false negative | 크롤링·인증 실패 | seed URL, OpenAPI, test account 제공 | authenticated coverage 80% 이상 |
| 테스트 장애 | 공격 페이로드로 데이터 변조 | staging 격리, mock payment, rollback seed | 데이터 오염 0건 |
| 스캔 장기화 | 엔드포인트 과다 | risk-based scan, parallel worker | scan time 60분 이하 |
| 오탐 논쟁 | evidence 불충분 | 재현 요청·응답 저장 | 재현율 90% 이상 |

> 요약: DAST 리스크는 인증 범위, 테스트 데이터 격리, 스캔 시간, evidence 재현성으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 배포 차단 | critical 0건, high 승인 기록 100% | DAST report, release log |
| 탐색 범위 | authenticated coverage 80% 이상 | crawler coverage |
| API 점검 | OpenAPI endpoint coverage 90% 이상 | spec 대비 호출 결과 |
| 처리 시간 | staging scan 60분 이하 | CI/CD duration |

> 요약: DAST 성공 여부는 critical 차단, 인증 탐색 범위, API 커버리지, 스캔 시간으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. OWASP ZAP, Burp Suite Enterprise, Arachni 등을 staging pipeline에 연결하고 release gate에서 critical 취약점 0건을 조건으로 설정함.
2. 테스트 계정, seed URL, OpenAPI 명세, JWT refresh 절차를 제공해 인증 화면과 API 커버리지를 80~90% 이상으로 유지함.
3. 운영 데이터 복제 금지, 결제·메일·외부 연동 mock 처리, rate limit 설정으로 스캔 중 부작용을 차단함.

**결론 (2줄):**
- 기술사 판단: 웹·API 런타임 취약점과 배포 설정 검증이 목적이면 DAST를 staging gate에 배치하고, 코드 흐름 결함은 SAST로 병행함.
- 향후 방향: DAST는 API 보안 테스트, IAST, 인증 자동화, CI/CD evidence 관리와 결합해 릴리스 보안 통제로 발전함.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "DAST를 설명하시오", "기술하시오" | 인증 크롤링, 공격 요청, evidence 분석 흐름 | SAST와 차이, black-box 특성 |
| 요구사항 명시형 | "보안 검증 방안을 제시하시오", "비교하시오" | staging gate, API scan, false negative 대응 | SAST·DAST 조합과 release 차단 기준 |

> 요약: 설명형은 실행 앱 공격 원리를, 방안형은 staging 게이트와 인증·API 커버리지 확보를 중심으로 전개한다.
