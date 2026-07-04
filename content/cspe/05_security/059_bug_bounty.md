---
title: "버그 바운티 (Bug Bounty)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 59
---

# 📖 【암기용】 개념 완전 이해

> 목적: 버그 바운티를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 외부 보안 연구자가 허가된 범위에서 취약점을 제보하면 보상과 조치를 연결하는 프로그램
- **왜 필요한가**: 내부 보안팀과 정기 점검만으로는 다양한 공격 관점, 새 기능 오류, 비정상 조합 취약점을 모두 찾기 어렵다.
- **핵심 직관**: 회사가 정한 운동장과 규칙 안에서 여러 전문가가 취약점을 찾고, 유효한 발견에 보상을 지급하는 제도임.

## 깊이 이해
- **배경·문제의식**: 서비스는 배포 주기가 짧고 API, 모바일, 클라우드가 복합되어 내부 테스트 케이스만으로 공격면을 모두 덮기 어렵다. 버그 바운티는 scope, safe harbor, triage, reward, remediation SLA로 외부 연구자 활동을 통제함.
- **작동 원리**: 조직은 대상과 금지 행위를 공개하고, 연구자는 취약점을 제보한다. triage 팀은 재현성과 영향도를 검증하고, severity에 따라 보상액을 결정하며, 개발팀은 SLA 안에 수정 후 연구자에게 결과를 알림.
- **비유**: 제품 출시 후 고객 불만을 기다리는 것이 아니라, 정해진 규칙으로 전문가 품질 검사를 공개 모집하는 방식임.
- **구체 예시**: OAuth redirect 취약점으로 account takeover가 가능한 보고는 critical로 분류되어 7일 SLA와 5,000달러 보상을 적용하고, rate limit 미흡 단독 이슈는 low로 분류함.
- **흔한 오해·주의점**: 버그 바운티는 무제한 공개 해킹 허가가 아니다. safe harbor, scope, 개인정보 처리, 중복 보고 기준, 보상 정책이 없으면 법적 분쟁과 운영 부담이 발생함.

## 연결 개념
- Vulnerability Disclosure Policy - 제보 접수와 법적 보호 기준
- Penetration Testing - 제한된 기간의 계획 평가와 비교
- Secure SDLC - 제보 취약점의 개발 프로세스 환류

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 버그 바운티 답안은 scope, safe harbor, triage, reward, SLA, remediation, disclosure를 운영 체계로 제시해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Bug Bounty는 외부 연구자의 취약점 제보를 허가 범위, 검증 절차, 보상 정책, 조치 SLA로 관리하는 보안 프로그램임.
> 2. **가치**: 내부 점검이 놓친 비즈니스 로직, 인증 우회, API 남용 취약점을 다양한 공격 관점으로 발견함.
> 3. **판단 포인트**: scope와 safe harbor 없이 공개하면 법적·운영 리스크가 커지므로 triage SLA와 reward 기준을 먼저 설계해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 제도 개념 확인 | 외부 연구자, 제보, 검증, 보상, 조치 | 단순 신고 게시판으로 서술 |
| 운영 통제 확인 | scope, safe harbor, 금지 행위, 개인정보 보호 | 무제한 공격 허용으로 표현 |
| 성과 관리 확인 | triage SLA, reward, remediation SLA, duplicate rate | 보상만 강조하고 조치 지표 누락 |

> 요약: 버그 바운티 문제는 외부 연구자 활용보다 안전한 운영 규칙과 조치 SLA를 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: 보상형 취약점 제보 제도
- 배경: 빠른 배포와 API·모바일·클라우드 조합에서는 내부 보안 테스트만으로 비즈니스 로직과 조합 취약점을 모두 검증하기 어려움.
- 필요성: 버그 바운티는 scope, safe harbor, triage 72시간, critical 7일 SLA, reward dispute 5% 이하 기준으로 운영해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Program Policy -> Scope/Safe Harbor -> Researcher Report -> Triage
               -> Severity/Reward -> Remediation SLA -> Retest/Disclosure
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Scope | 대상 도메인, 앱, API, 제외 시스템 정의 | third-party와 production 영향 제한 |
| Safe Harbor | 허가된 연구 범위와 법적 보호 조건 명시 | 데이터 삭제, DoS, social engineering 금지 |
| Triage | 재현성, 영향도, 중복 여부 검증 | 72시간 1차 응답 SLA |
| Reward | severity와 품질 기준으로 보상 결정 | CVSS+business impact 반영 |
| Remediation | owner 배정, 수정, 재검증, 공개 조율 | critical 7일 SLA |

> 요약: 버그 바운티는 정책, 범위, 법적 보호, 검증, 보상, 조치가 결합된 운영 프로그램임.

---

## Ⅲ. 동작원리 및 흐름도

```text
프로그램 공개 -> 연구자 테스트 -> 취약점 보고
-> triage/중복 확인 -> severity/reward 결정 -> 개발 조치
-> retest -> 보상 지급/공개
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | scope, 금지 행위, safe harbor, 보상표 공개 | 정책 변경 이력 관리 |
| 2 | 연구자가 PoC, 영향도, 재현 절차 제출 | 재현 가능한 보고서 비율 80% 이상 |
| 3 | triage 팀이 중복, 심각도, 악용 가능성 검증 | 1차 응답 72시간 이내 |
| 4 | 개발팀이 수정하고 연구자가 retest 수행 | critical 7일, high 30일 SLA |
| 5 | 보상 지급과 disclosure 조율 | 지급 30일 이내, duplicate dispute 5% 이하 |

> 요약: 버그 바운티는 제보 접수 후 검증, 보상, 조치, 재검증, 공개까지 SLA로 관리해야 함.

---

## Ⅳ. 특징

| 구분 | 침투 테스트 | 버그 바운티 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 참여자 | 계약 tester 소수 | 외부 연구자 다수 | private/public program |
| 기간 | 1~4주 프로젝트 | 상시 운영 | triage 72시간 |
| 보상 | 고정 계약비 | 유효 취약점별 reward | critical 1,000~10,000달러 |
| 통제 | NDA와 ROE | scope, safe harbor, platform policy | duplicate rate 20% 이하 |

> 요약: 버그 바운티는 지속성과 다양한 관점이 장점이나, scope와 triage 체계 없이는 운영 비용이 증가함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 평가 방식 | 정기 침투 테스트 | 상시 crowd testing | 대외 서비스와 API 변경이 월 1회 이상 |
| 비용 구조 | 고정 계약 | 유효 finding별 reward | 품질 기반 보상 선호 시 |
| 공개 범위 | 비공개 내부 평가 | private 또는 public program | triage 인력과 법무 검토 준비 후 public 전환 |

> 요약: 버그 바운티는 외부 노출 서비스가 많고 triage와 보상 운영 체계가 준비된 조직에서 단계적으로 확대해야 함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 범위 초과 | scope와 금지 행위 불명확 | wildcard 제외, test account, rate limit | out-of-scope report 10% 이하 |
| 개인정보 노출 | 연구자가 실제 데이터 접근 | 최소 증거 원칙, PII 수집 금지 | PII incident 0건 |
| triage 적체 | 보고 급증, 중복 제보 | severity queue, duplicate rule, platform triage | first response 72시간 |
| 보상 분쟁 | reward 기준 모호 | severity matrix, appeal 절차 | reward dispute 5% 이하 |

> 요약: 버그 바운티 리스크는 범위 초과, 개인정보, triage 적체, 보상 분쟁이며 정책과 SLA로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| triage 품질 | 1차 응답 72시간, 재현율 80% 이상 | platform ticket, triage log |
| 조치 성과 | critical 7일, high 30일 SLA | ITSM, retest 결과 |
| 프로그램 건전성 | duplicate 20% 이하, dispute 5% 이하 | report analytics, reward history |

> 요약: 버그 바운티 성과는 보고 건수보다 유효 취약점 비율, 응답 SLA, 조치 SLA, 분쟁률로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 정책 설계: 도메인, API, 모바일 앱 scope와 safe harbor를 공개하고 DoS, social engineering, PII 수집, third-party 공격을 금지함.
2. 운영 절차: 72시간 triage SLA, severity matrix, duplicate rule, reward table, appeal 절차를 정의하고 platform ticket으로 증적을 보관함.
3. 조치 환류: critical 7일, high 30일 remediation SLA를 개발 backlog에 연결하고 반복 취약점은 Secure SDLC checklist와 SAST/DAST rule로 전환함.

**결론 (2줄):**
- 기술사 판단: 외부 서비스 공격면이 작고 triage 인력이 없으면 VDP부터 시작하고, 대외 서비스가 많으면 private bug bounty 후 public 전환이 적절함.
- 향후 방향: AI 코드 생성과 API 확대로 비즈니스 로직 취약점이 늘어나므로 bug bounty는 CTEM과 Secure SDLC 지표로 통합 운영되어야 함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "버그 바운티를 설명하시오" | 제보, triage, 보상, 조치 흐름 | 침투 테스트와 차이 |
| 요구사항 명시형 | "도입 방안을 제시하시오", "운영 리스크를 설명하시오" | scope, safe harbor, SLA, disclosure | 개인정보, 분쟁, triage 적체 통제 |

> 요약: 설명형은 제도와 절차, 방안형은 safe harbor와 SLA 기반 운영 통제를 중심으로 작성함.
