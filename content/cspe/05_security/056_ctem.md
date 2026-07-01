---
title: "CTEM 지속적 위협 노출 관리 (CTEM Continuous Threat Exposure Management)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 56
---

# 📖 【암기용】 개념 완전 이해

> 목적: CTEM을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 공격자가 실제로 악용할 수 있는 노출을 계속 찾아 검증하고 줄이는 보안 운영 체계
- **왜 필요한가**: 취약점 스캐너는 수천 개 CVE를 보여주지만, 공격자는 외부 노출 자산, 인증 우회, 권한 상승 경로처럼 실제 침투 가능한 지점만 선택한다.
- **핵심 직관**: 창고 목록을 세는 것이 아니라 도둑이 들어올 수 있는 문을 찾아 잠그고 다시 열리는지 확인하는 방식임.

## 깊이 이해
- **배경·문제의식**: 패치 우선순위를 CVSS 점수만으로 정하면 인터넷 노출, exploit code, 중요 자산 연결성, 보상 통제 여부가 반영되지 않는다. CTEM은 노출을 자산, 공격 가능성, 검증, 조치, 재검증으로 연결함.
- **작동 원리**: scope로 보호 대상을 정하고, discover로 자산과 노출을 찾고, prioritize로 공격 가능성과 업무 영향을 점수화한다. validate에서 BAS, 침투 테스트, PoC로 실제 악용 가능성을 확인하고 mobilize로 보완 조치와 owner를 배정함.
- **비유**: 병원 검진에서 수치 이상을 모두 치료하지 않고, 암 의심 소견처럼 생명 위험과 진행 가능성이 높은 항목부터 조직검사와 치료를 진행하는 방식임.
- **구체 예시**: 외부 IP 2,000개 중 RCE CVE 40건이 발견되어도, 인터넷 노출, exploit 공개, 관리자 권한 획득 가능, 중요 DB 접근 경로가 확인된 5건을 7일 SLA로 처리함.
- **흔한 오해·주의점**: CTEM은 취약점 스캔 주기 단축이 아니다. 검증 없는 CVE 목록, owner 없는 티켓, 재검증 없는 패치 완료 처리는 CTEM으로 볼 수 없음.

## 연결 개념
- Vulnerability Scanner - 노출 후보를 수집하는 입력 도구
- BAS/Penetration Testing - 공격 가능성을 검증하는 수단
- Risk-Based Vulnerability Management - CTEM의 우선순위 산정 기반

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: CTEM 답안은 취약점 목록 나열이 아니라 scope, discover, prioritize, validate, mobilize와 KPI 폐루프를 제시해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CTEM은 자산과 공격면의 노출을 지속 식별하고 실제 악용 가능성 기준으로 검증·조치·재검증하는 운영 프로그램임.
> 2. **가치**: CVSS 단일 점수 대신 외부 노출, exploit 가능성, 자산 중요도, 보상 통제를 결합해 remediation SLA를 줄임.
> 3. **판단 포인트**: scope/discover/prioritize/validate/mobilize 5단계와 exposure reduction rate, retest pass rate, SLA 준수율을 연결해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 노출관리 개념 확인 | CTEM 5단계, 공격면, 검증, 조치 폐루프 | 취약점 스캔과 동일시 |
| 우선순위 판단 확인 | CVSS+EPSS+자산 중요도+인터넷 노출+exploit code | CVE 심각도만 기준으로 제시 |
| 운영 지표 확인 | exposure reduction, retest pass, SLA, owner | 재검증과 KPI 누락 |

> 요약: CTEM 문제는 "무엇이 취약한가"보다 "무엇이 실제 공격 가능한가와 누가 언제 줄였는가"를 묻는다.

---

## Ⅰ. 개요 및 필요성

CTEM은 공격 가능 노출 관리 체계임. 클라우드, SaaS, API, 원격접속이 증가하면서 자산 목록과 취약점 목록만으로는 실제 침투 경로를 줄이기 어렵다. 따라서 자산 식별, 공격 가능성 검증, 우선순위 조치, 재검증, KPI 관리를 연속 수행해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Business Scope -> Asset/Attack Surface Discover -> Exposure Prioritize
               -> Validate by BAS/Pentest -> Mobilize Remediation
               -> Retest/KPI -> Scope 재조정
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Scope | 핵심 업무, crown jewel, 외부 노출 범위 정의 | 서비스 owner와 RACI 지정 |
| Discover | 자산, 계정, API, CVE, misconfiguration 식별 | EASM, CSPM, scanner 연계 |
| Prioritize | 공격 가능성과 업무 영향을 점수화 | CVSS, EPSS, KEV, asset criticality |
| Validate | PoC, BAS, 침투 테스트로 악용 가능성 확인 | false positive 제거 |
| Mobilize | 패치, 설정 변경, 보상 통제, 재검증 수행 | SLA와 retest 기준 필요 |

> 요약: CTEM은 범위 정의부터 재검증까지 이어지는 노출 감소 운영 구조이며, discover만으로 완료되지 않음.

---

## Ⅲ. 동작원리 및 흐름도

```text
핵심 자산 선정 -> 외부/내부 노출 수집 -> 위험 점수 산정
-> 공격 가능성 검증 -> owner 배정/조치 -> 재검증 -> KPI 보고
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | crown jewel, 외부 서비스, privileged account 범위 지정 | scope coverage 95% 이상 |
| 2 | EASM, scanner, CSPM으로 노출 수집 | unknown asset 월 5% 이하 |
| 3 | CVSS, EPSS, KEV, 인터넷 노출, 자산 중요도 결합 | critical exposure 7일 SLA |
| 4 | BAS/Pentest/PoC로 실제 침투 가능성 확인 | false positive 20% 이하 |
| 5 | 패치, WAF rule, IAM 차단 후 재검증 | retest pass rate 95% 이상 |

> 요약: CTEM은 발견된 노출을 공격 가능성으로 걸러 조치하고 재검증 지표로 폐루프를 닫는 절차임.

---

## Ⅳ. 특징

| 구분 | 기존 취약점 관리 | CTEM | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 기준 | CVE, CVSS, 패치 목록 | 자산 중요도와 공격 가능성 | CVSS 9.8보다 exploit+외부 노출 우선 |
| 검증 | 스캔 결과 중심 | BAS, PoC, pentest 검증 | false positive 20% 이하 |
| 운영 | 월간 점검, 티켓 발행 | 지속 탐색, owner, 재검증 | critical 7일, high 30일 SLA |
| 성과 | 패치 건수 | 노출 감소율, retest pass | exposure reduction 30%/분기 |

> 요약: CTEM은 취약점 개수보다 검증된 공격 가능 노출을 SLA 안에 줄였는지를 측정함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Vulnerability Management | CTEM 프로그램 | 자산, 공격면, 검증, 조치 owner가 분리된 조직 |
| 비용/성과 | 전체 패치율 중심 | 고위험 노출 감소 중심 | critical backlog 100건 이상일 때 |
| 운영/위험 | 스캔 주기 의존 | 지속 discover와 retest | 클라우드 변경 일 10건 이상 환경 |

> 요약: CTEM은 동적 자산과 고위험 백로그가 많은 조직에서 우선순위 기반 보완 조치 체계로 적용함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 목록 과잉 | 스캐너 결과를 모두 backlog로 등록 | EPSS, KEV, 인터넷 노출로 필터링 | actionable finding 비율 60% 이상 |
| 조치 지연 | 서비스 owner와 예외 승인 부재 | RACI, SLA, risk acceptance | SLA 준수율 95% 이상 |
| 검증 누락 | 패치 완료만 보고 | retest 자동화, BAS 회귀 테스트 | retest pass rate 95% 이상 |
| 공격면 누락 | shadow IT, cloud asset 미등록 | EASM, CSPM, CMDB reconciliation | unknown asset 월 5% 이하 |

> 요약: CTEM 리스크는 결과 과잉, 조치 지연, 검증 누락, 공격면 누락이며 owner와 지표로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 노출 감소 | critical exposure 30%/분기 감소 | CTEM dashboard, retest 결과 |
| 조치 속도 | critical 7일, high 30일 SLA | ticket timestamp, change log |
| 검증 품질 | false positive 20% 이하, retest pass 95% | BAS/Pentest 결과, scanner 재스캔 |

> 요약: CTEM 성공 여부는 발견 건수가 아니라 고위험 노출 감소율, 조치 SLA, 재검증 통과율로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. Scope 정렬: 인터넷 노출 서비스, 관리자 계정, 고객 DB, API gateway를 crown jewel로 지정하고 CMDB/EASM coverage 95%를 기준으로 관리함.
2. 검증 기반 우선순위: CVSS, EPSS, CISA KEV, exploit 공개, lateral movement 가능성을 risk score에 반영하고 critical exposure는 7일 SLA로 처리함.
3. 폐루프 운영: 패치 후 Nessus/OpenVAS 재스캔, BAS 회귀 테스트, SOAR 티켓 종료 조건을 retest pass 95%로 설정함.

**결론 (2줄):**
- 기술사 판단: 자산 변동이 작으면 정기 취약점 관리로 충분하나, 클라우드·SaaS·외부 노출이 빈번하면 CTEM을 운영 지표 기반 프로그램으로 도입해야 함.
- 향후 방향: CTEM은 EASM, ASM, BAS, CSPM, SIEM을 통합해 공격면 변화와 조치 효과를 분기별 노출 감소율로 관리하는 방향으로 발전함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "CTEM을 설명하시오", "기술하시오" | 5단계와 재검증 폐루프 | 취약점 관리와 CTEM 차이 |
| 요구사항 명시형 | "도입 방안을 제시하시오", "운영 체계를 설계하시오" | scope, validate, mobilize, KPI 설계 | SLA, owner, exposure reduction 선택 기준 |

> 요약: 설명형은 CTEM 5단계, 설계형은 검증 기반 우선순위와 KPI 폐루프를 중심으로 작성함.
