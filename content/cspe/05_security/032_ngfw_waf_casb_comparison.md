---
title: "차세대 방화벽 NGFW vs WAF vs CASB 비교 (NGFW WAF CASB Comparison)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 32
---

# 📖 【암기용】 개념 완전 이해

> 목적: NGFW, WAF, CASB를 보호 대상과 배치 위치 기준으로 구분하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: NGFW는 네트워크·애플리케이션 경계, WAF는 웹 요청, CASB는 클라우드 SaaS 사용을 통제하는 보안 게이트웨이이다.
- **왜 필요한가**: 공격자는 네트워크 포트, 웹 취약점, SaaS 데이터 유출 경로를 각각 이용한다. 한 장비로 세 영역을 모두 통제할 수 없음.
- **핵심 직관**: NGFW는 회사 출입문, WAF는 웹 접수창구, CASB는 외부 클라우드 사용 승인대장에 해당함.

## 깊이 이해
- **배경·문제의식**: 업무가 웹과 SaaS로 이동하면서 포트 기반 방화벽만으로는 `443/tcp` 내부의 공격을 구분하기 어렵다. HTTP 공격은 WAF, SaaS 사용과 데이터 반출은 CASB가 담당함.
- **작동 원리**: NGFW는 App-ID, User-ID, IPS, URL Filtering으로 네트워크 세션을 검사한다. WAF는 HTTP 메서드, URL, 파라미터, 쿠키, OWASP Top 10 패턴을 검사한다. CASB는 API 또는 프록시 방식으로 SaaS 접근, DLP, Shadow IT, 사용자 행위를 분석함.
- **비유**: 같은 출입 통제라도 정문 경비, 민원 창구 심사, 외부 협력 서비스 사용 감사는 담당 위치와 확인 항목이 다르다.
- **구체 예시**: 인터넷 사용자는 NGFW에서 미승인 원격제어 앱을 차단하고, 외부 고객의 `/login` 요청은 WAF가 SQL Injection 패턴을 차단하며, 직원의 Google Drive 외부 공유는 CASB가 DLP 정책으로 격리함.
- **흔한 오해·주의점**: WAF가 있으면 NGFW가 필요 없거나 CASB가 방화벽을 대체한다는 주장은 틀림. 보호 대상, 트래픽 방향, 정책 기준이 다르므로 계층 통제가 필요함.

## 연결 개념
- 방화벽: L3/L4 세션 통제의 기본
- OWASP Top 10: WAF 정책의 대표 공격 분류
- SASE/SSE: CASB, SWG, ZTNA를 클라우드 보안 경계로 통합

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: NGFW/WAF/CASB 비교는 기능 나열이 아니라 보호 대상, 배치 위치, 검사 계층, 로그 연계 기준을 분리해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: NGFW, WAF, CASB는 각각 네트워크 경계, 웹 애플리케이션, 클라우드 서비스 사용을 통제하는 보안 통제점이다.
> 2. **가치**: 동일한 `443/tcp`라도 앱 식별, HTTP 공격 차단, SaaS 데이터 반출 통제를 역할별로 분담한다.
> 3. **판단 포인트**: 보호 자산이 네트워크 세션인지, 웹 요청인지, SaaS 데이터인지에 따라 배치 위치와 운영 지표가 달라진다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 보안 솔루션 역할 분리 확인 | NGFW=네트워크/앱, WAF=HTTP, CASB=SaaS/DLP | 모두 방화벽으로 묶어 설명 |
| 보호 대상과 배치 위치 판단 확인 | inline, reverse proxy, API mode, forward proxy | 제품 기능 나열 후 아키텍처 누락 |
| 운영 연계 역량 확인 | SIEM, SOAR, DLP, 계정 로그 상관분석 | 탐지·차단·감사 지표 미제시 |

> 요약: 이 문제는 세 솔루션의 우열이 아니라 보호 대상별 통제 위치를 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: 공격면별 보안 게이트웨이 비교
- 배경: 클라우드·웹 업무에서는 동일한 `443/tcp` 안에서도 네트워크 앱, HTTP 공격, SaaS 데이터 반출이 서로 다른 경로로 발생함.
- 필요성: NGFW·WAF·CASB는 보호 대상과 배치 위치를 분리하고, SIEM 상관분석에서 사용자·세션·파일 이벤트 연결률 95%를 목표로 운영해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
User/Internet -> NGFW -> Web Zone -> WAF -> Web/App Server
Enterprise User -> SWG/CASB Proxy -> SaaS
SaaS API -> CASB API Connector -> DLP/SIEM
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| NGFW | 애플리케이션·사용자·위협 기반 네트워크 통제 | App-ID, IPS, URL Filtering |
| WAF | HTTP 요청·응답의 웹 공격 통제 | OWASP Top 10, positive/negative policy |
| CASB | SaaS 접근, DLP, Shadow IT 통제 | API mode, forward/reverse proxy |
| SIEM/SOAR | 이벤트 상관분석과 대응 자동화 | 사용자·세션·파일 이벤트 연결 |

> 요약: 세 솔루션은 동일한 보안 영역이 아니라 네트워크, 웹, SaaS 공격면별 통제점을 구성함.

---

## Ⅲ. 동작원리 및 흐름도

```text
Traffic 식별 -> 보호 대상 판단 -> 통제점 선택
-> NGFW 세션/App 검사 / WAF HTTP 검사 / CASB SaaS·DLP 검사
-> 차단·허용·격리 -> 로그 전송
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 트래픽 방향과 보호 자산 식별 | north-south, east-west, SaaS API |
| 2 | 검사 계층 결정 | L3/L4/L7, HTTP, SaaS object |
| 3 | 정책 적용 | IPS signature, WAF rule, DLP pattern |
| 4 | 이벤트 대응 | block, alert, quarantine, ticket 생성 |

> 요약: 트래픽과 자산을 먼저 분류한 뒤 NGFW, WAF, CASB 중 적합한 통제점을 선택함.

---

## Ⅳ. 특징

| 구분 | NGFW | WAF | CASB |
|:---|:---|:---|:---|
| 보호 대상 | 네트워크 세션, 앱, 사용자 | 웹 애플리케이션 요청·응답 | SaaS 계정, 파일, 공유 링크 |
| 배치 위치 | 경계망 inline, 내부 세그먼트 | Reverse Proxy, LB 앞단 | API, forward/reverse proxy |
| 주요 지표 | app unknown 5% 이하, IPS hit | false positive 3% 이하, blocked attack | DLP incident, risky share count |
| 대표 공격 | C2, 스캔, 악성 앱 | SQLi, XSS, Path Traversal | Shadow IT, 외부 공유, 토큰 오남용 |

> 요약: NGFW는 세션, WAF는 HTTP, CASB는 SaaS 객체와 사용자 행위를 중심으로 통제함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 단일 방화벽 | NGFW+WAF+CASB 계층 통제 | 웹·SaaS 업무 비중 50% 이상이면 분리 적용 |
| 비용/성능 | 장비 단일화 | 검사 지점 다중화 | p95 지연, TLS 복호화 부하, 운영 인력 판단 |
| 운영/위험 | 로그 분산 | SIEM 상관분석 | 사용자 ID, IP, 세션, 파일 이벤트 연결률 95% |

> 요약: 보호 대상이 다르면 단일 장비보다 계층형 통제와 로그 상관분석이 채점 포인트임.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 중복 차단 | NGFW IPS와 WAF 룰 충돌 | 정책 우선순위와 예외 승인 표준화 | false positive 3% 이하 |
| 사각지대 | SaaS API 미연동, 개인 계정 사용 | CASB API connector, Shadow IT 탐지 | 미승인 SaaS 월별 감소율 |
| 개인정보 노출 | 외부 공유 링크·첨부 업로드 | DLP 정규식, OCR, 격리 정책 | PII 외부 공유 0건 |

> 요약: 운영 리스크는 중복 차단과 SaaS 사각지대이며, 예외 승인과 DLP 지표로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 탐지·차단 | WAF OWASP Top 10 룰 적용률 100% | 모의공격, 룰셋 감사 |
| 클라우드 통제 | 승인 SaaS 목록 100%, risky share 0건 | CASB 대시보드, API 로그 |
| 로그 연계 | 사용자·세션·파일 이벤트 상관률 95% 이상 | SIEM correlation test |

> 요약: 도입 효과는 웹 공격 차단, SaaS 데이터 통제, 로그 상관분석 지표로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 경계 통제: NGFW를 인터넷·내부 세그먼트 경계에 배치하고 App-ID, IPS, URL category 정책을 업무 앱 기준으로 적용
2. 웹 통제: WAF를 LB 앞단 reverse proxy로 배치하고 OWASP CRS, positive policy, 가상패치 룰을 CI/CD와 연계
3. SaaS 통제: CASB API mode와 proxy mode를 병행해 DLP, 외부 공유 격리, 퇴사자 토큰 회수를 자동 티켓으로 처리

**결론 (2줄):**
- 기술사 판단: 네트워크 세션은 NGFW, 웹 취약점은 WAF, SaaS 데이터 반출은 CASB로 분리하고 SIEM에서 단일 사건으로 결합함
- 향후 방향: SASE/SSE 전환 시 NGFW·WAF·CASB 로그를 사용자 ID와 자산 중요도 기준으로 통합 운영해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "NGFW, WAF, CASB를 설명하시오" | 통제점별 동작 원리와 배치 위치 | 보호 대상, 검사 계층, 대표 공격 비교 |
| 요구사항 명시형 | "비교하시오", "도입 방안을 제시하시오", "설계하시오" | 요구 자산별 통제점 선택 흐름 | 중복 차단, SaaS 사각지대, 로그 연계 기준 |

> 요약: 비교형은 보호 대상과 위치를 표로 고정하고, 설계형은 트래픽 흐름에 맞춘 계층 배치를 강조함.
