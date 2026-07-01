---
title: "PSIRT 제품 보안 대응 팀 (PSIRT)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 65
---

# 📖 【암기용】 개념 완전 이해

> 목적: PSIRT를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 제품 취약점 접수부터 공개 권고까지 책임지는 제품 보안 대응 조직
- **왜 필요한가**: 제품 취약점은 고객 시스템, 공급망, 규제 보고, 브랜드 신뢰에 영향을 준다. PSIRT는 제보 접수, triage, CVE 할당, 패치, advisory, coordinated disclosure를 표준 절차로 운영한다.
- **핵심 직관**: 제품에서 결함이 발견되면 고객센터가 아니라 전문 사고 지휘소가 원인 분석, 수리 일정, 고객 공지를 조율하는 구조임.

## 깊이 이해
- **배경·문제의식**: 보안 연구자, 고객, 내부 테스트, bug bounty에서 취약점이 제보되면 개발팀만으로는 재현, 심각도, 공개 일정, 법무 검토를 동시에 처리하기 어렵다. PSIRT는 제품 보안의 단일 창구 역할을 수행한다.
- **작동 원리**: 취약점 intake, triage, 재현, CVSS 산정, CVE assignment, remediation 개발, advisory 작성, coordinated disclosure, 사후 개선 순서로 운영한다.
- **비유**: 자동차 리콜 조직과 같다. 결함 제보를 검증하고 위험도를 정한 뒤 수리 부품, 고객 통지, 리콜 일정, 규제 보고를 관리한다.
- **구체 예시**: 인증 우회 취약점이 신고되면 PSIRT는 24시간 내 접수 확인, 7일 내 triage, CVSS 산정, CVE 예약, 90일 공개 일정 협의, 패치와 mitigation을 advisory로 공개함.
- **흔한 오해·주의점**: PSIRT는 SOC나 CSIRT와 다르다. SOC/CSIRT가 조직 침해 대응을 담당한다면 PSIRT는 제품 취약점과 고객 커뮤니케이션을 담당함.

## 연결 개념
- CVE/CVSS - 취약점 식별자와 severity 산정
- Coordinated Vulnerability Disclosure - 연구자·벤더·고객 공개 일정 조율
- Secure SDLC/SBOM - 재발 방지와 공급망 영향 분석

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: PSIRT 답안은 조직명 설명이 아니라 intake, triage, advisory, CVE assignment, coordinated disclosure, 고객 커뮤니케이션을 절차로 제시해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: PSIRT(Product Security Incident Response Team)는 제품 취약점 접수, 분석, 조치, 공개, 고객 지원을 총괄하는 제품 보안 대응 조직임.
> 2. **가치**: 연구자 제보와 고객 영향을 표준 SLA로 처리해 패치, mitigation, advisory, CVE 공개를 일관되게 제공함.
> 3. **판단 포인트**: intake/triage, CVSS, CVE assignment, coordinated disclosure, advisory 품질, 재발 방지 Secure SDLC 환류를 포함해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| PSIRT 역할 이해 확인 | 제품 취약점 대응, 연구자·고객·개발·법무 조율 | SOC/CSIRT와 혼동 |
| 대응 프로세스 판단 확인 | intake, triage, remediation, advisory, disclosure | 접수 후 패치만 작성 |
| 공개·커뮤니케이션 통제 확인 | CVE assignment, CVSS, 90일 조율, 고객 FAQ, mitigation | 고객 영향·공개 일정·재발 방지 누락 |

> 요약: PSIRT 문제는 제품 취약점 대응을 기술 조치와 공개 커뮤니케이션까지 연결하는 역량을 요구함.

---

## Ⅰ. 개요 및 필요성

PSIRT는 제품 보안 대응 조직이다. 제품 취약점은 고객 운영환경과 공급망에 영향을 주므로 단순 개발 결함으로 처리할 수 없다. PSIRT는 취약점 접수, 심각도 산정, 패치, CVE, advisory, 고객 지원을 총괄함.

---

## Ⅱ. 구조 및 구성요소

```text
제보/탐지 -> PSIRT Intake -> Triage/CVSS -> Remediation -> Advisory/Disclosure
  / 연구자, 고객, bug bounty, 내부 테스트
  / 개발, QA, 법무, 고객지원, CVE CNA
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Intake Channel | 이메일, 포털, bug bounty, 고객 제보 접수 | PGP, safe harbor, SLA 안내 |
| Triage Board | 재현성, 영향도, CVSS, exploit 가능성 판단 | 7일 내 초기 판정 |
| Remediation Team | 패치, workaround, regression test 수행 | 제품 버전별 영향 확인 |
| Disclosure Lead | CVE, advisory, 공개 일정, 연구자 조율 | coordinated disclosure 90일 기준 |
| Customer Response | mitigation, FAQ, 지원 케이스, 고객 공지 | critical 고객 24시간 알림 |

> 요약: PSIRT는 제보 접수부터 기술 조치와 공개·고객 대응까지 여러 조직을 묶는 제품 보안 거버넌스임.

---

## Ⅲ. 동작원리 및 흐름도

```text
취약점 제보 -> 접수 확인 -> 재현/영향 분석 -> CVSS/CVE 처리
  / exploit 가능성, 영향 제품, 고객 노출
패치/완화 개발 -> advisory 작성 -> coordinated disclosure -> 사후 개선
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 제보 접수와 tracking ID 발급 | 접수 확인 24시간 이내 |
| 2 | 재현, 영향 제품, 버전, exploit 가능성 triage | triage 7일 이내 |
| 3 | CVSS 산정, CVE 예약, 공개 전략 수립 | CVSS vector, CNA 기록 |
| 4 | 패치, workaround, regression test, 릴리스 승인 | critical patch 30일 목표 |
| 5 | advisory 공개, 고객 공지, 연구자 credit, 사후 분석 | 공개 후 문의 SLA 2영업일 |

> 요약: PSIRT는 제보를 추적 가능한 사건으로 만들고 CVSS/CVE, 패치, 공개, 사후 개선까지 관리함.

---

## Ⅳ. 특징

| 구분 | CSIRT/SOC | PSIRT | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 대상 | 조직 내부 침해 | 제품·서비스 취약점 | 고객 영향 제품 버전 |
| 입력 | SIEM, EDR, 침해 신고 | 연구자 제보, bug bounty, 내부 테스트 | 접수 24시간 |
| 산출물 | 침해 대응 보고서 | patch, mitigation, security advisory, CVE | triage 7일, 공개 90일 |
| 이해관계자 | 보안운영, IT, 법무 | 개발, QA, 고객, 연구자, CNA | 고객 공지 SLA |

> 요약: PSIRT는 침해 대응 조직이 아니라 제품 취약점의 조치와 공개를 책임지는 조직임.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 개발팀별 임의 대응 | 단일 PSIRT intake와 triage | 제품군 3개 이상, 외부 고객 존재 |
| 비용/성과 | 비공개 패치 중심 | advisory, CVE, mitigation 공개 | 고객 패치 판단 지원 |
| 운영/위험 | 공개 지연·중복 대응 | coordinated disclosure와 SLA | 연구자 제보·규제 보고 가능성 |

> 요약: 외부 고객에게 제품을 제공하는 조직은 PSIRT로 취약점 대응과 공개 품질을 표준화해야 함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 공개 지연 | owner 부재, 법무·개발 조율 지연 | RACI, disclosure calendar, executive escalation | advisory on-time 95% |
| 심각도 오류 | CVSS·고객 환경 미반영 | CVSS+환경 영향+exploit 가능성 검토 | severity reclass 5% 이하 |
| 고객 혼란 | mitigation 부족, 영향 버전 불명확 | 영향 제품표, workaround, FAQ, SBOM/VEX 제공 | 고객 문의 2영업일 응답 |

> 요약: PSIRT 리스크는 공개 지연, severity 오류, 고객 혼란이며 RACI와 advisory 품질 지표로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 접수·분석 | ack 24시간, triage 7일 | PSIRT case system |
| 조치 | critical patch 30일, workaround 7일 | 릴리스 노트, QA 결과 |
| 공개·고객 | advisory on-time 95%, 문의 2영업일 | advisory tracker, CRM |

> 요약: PSIRT 성과는 접수 속도, 패치·완화 제공 시간, advisory 공개 품질로 측정함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 체계 구축: `security@` 메일, PGP key, 취약점 제보 포털, safe harbor, tracking ID를 제공하고 접수 확인 24시간 SLA를 둠.
2. 처리 절차: triage board에서 CVSS 3.1/4.0, exploit 가능성, 고객 노출, CVE assignment를 7일 이내 결정하고 개발·QA·법무 RACI를 지정함.
3. 공개·환류: coordinated disclosure 90일 기준으로 advisory, patch, mitigation, FAQ, researcher credit을 공개하고 반복 취약점은 Secure SDLC checklist와 SAST rule로 전환함.

**결론 (2줄):**
- 기술사 판단: 고객 설치형 제품이나 SaaS를 운영하는 조직은 SOC와 별개로 PSIRT를 두고 제품 취약점 공개와 패치 책임을 분리해야 함.
- 향후 방향: PSIRT는 SBOM, VEX, bug bounty, Secure SDLC, 공급망 보안 공시를 통합하는 제품 보안 거버넌스로 확장되어야 함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "PSIRT를 설명하시오", "기술하시오" | intake, triage, remediation, advisory 흐름 | CSIRT/SOC와 PSIRT 차이 |
| 요구사항 명시형 | "구축 방안을 제시하시오", "운영 절차를 설계하시오" | CVE assignment, coordinated disclosure, 고객 공지 | SLA, RACI, advisory 품질, Secure SDLC 환류 |

> 요약: 설명형은 조직 역할과 프로세스, 설계형·운영형은 SLA와 공개 커뮤니케이션 통제를 중심으로 답안을 구성함.
