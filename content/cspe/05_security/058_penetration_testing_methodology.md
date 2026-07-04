---
title: "침투 테스트 방법론 (Penetration Testing Methodology)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 58
---

# 📖 【암기용】 개념 완전 이해

> 목적: 침투 테스트 방법론을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 허가된 범위 안에서 실제 공격 절차로 시스템 침투 가능성과 업무 영향을 검증하는 활동
- **왜 필요한가**: 취약점 스캔은 후보를 찾지만, 그 취약점이 인증 우회, 권한 상승, 데이터 접근으로 이어지는지는 별도 검증이 필요하다.
- **핵심 직관**: 도면 검토가 아니라 실제로 문을 열어 보고 어디까지 들어갈 수 있는지 확인하는 보안 점검임.

## 깊이 이해
- **배경·문제의식**: 조직은 패치 목록과 설정 점검만으로 공격자의 경로를 알기 어렵다. 침투 테스트는 scope와 ROE를 정하고 정찰, 취약점 분석, exploitation, post-exploitation, 보고, retest를 통해 위험을 증명함.
- **작동 원리**: 대상과 금지 행위를 합의한 뒤 OSINT와 스캔으로 공격면을 찾고, exploit으로 침투 가능성을 검증한다. 이후 권한 상승과 lateral movement 범위를 확인하되 데이터 파괴와 서비스 중단은 ROE로 제한함.
- **비유**: 소방 점검에서 소화기 위치만 보는 것이 아니라 실제 대피 훈련을 해 병목 지점과 연락 체계를 확인하는 활동임.
- **구체 예시**: VPN 포털에서 MFA bypass를 검증하고 일반 계정으로 내부 Git 서버 접근, secret 탈취, DB read 권한까지 이어지는 경로를 증거와 함께 보고함.
- **흔한 오해·주의점**: 침투 테스트는 무제한 해킹이 아니다. scope, ROE, 승인, 증거 보존, 영향 제한, 재검증이 없으면 감사와 법적 리스크가 발생함.

## 연결 개념
- Vulnerability Scanner - 침투 후보 취약점 식별
- Red Team - 장기 목표 기반 공격 시뮬레이션
- OWASP WSTG/PTES/NIST SP 800-115 - 방법론과 보고 기준

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 침투 테스트 답안은 scoping, ROE, exploitation, evidence, report, retest를 연결하고 운영 영향 통제를 포함해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 침투 테스트는 허가된 범위에서 공격자 TTP를 재현해 취약점의 실제 악용 가능성과 업무 영향을 검증하는 평가 방법임.
> 2. **가치**: 취약점 후보를 exploit chain, 권한 상승, 데이터 접근 증거로 전환해 조치 우선순위를 명확히 함.
> 3. **판단 포인트**: scope, ROE, 승인, exploitation, 보고서, retest, 안전 통제를 누락하면 방법론 답안으로 부족함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 절차 이해 확인 | scoping, recon, vuln analysis, exploitation, report, retest | 공격 기법만 나열 |
| 통제 역량 확인 | ROE, 허가, 영향 제한, 증거 보존 | 무단 해킹처럼 서술 |
| 조치 연계 확인 | risk rating, remediation, 재검증 | 보고서 제출 후 종료로 처리 |

> 요약: 침투 테스트 문제는 공격 재현 능력과 통제된 평가 절차를 함께 쓰는 것이 핵심임.

---

## Ⅰ. 개요 및 필요성

- 개요: 허가 기반 공격 검증
- 배경: 취약점 목록은 인증 우회, 권한 상승, 데이터 접근, lateral movement로 이어지는 실제 침투 가능성과 업무 영향을 증명하지 못함.
- 필요성: 침투 테스트는 scope와 ROE 승인 100%, critical 7일 SLA, retest pass 95% 기준으로 공격 경로 증거와 조치 완료를 검증해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Business Objective -> Scope/ROE -> Recon/Scanning -> Vulnerability Analysis
                  -> Exploitation -> Post-Exploitation -> Report -> Retest
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Scope/ROE | 대상, 기간, 금지 행위, 연락망 정의 | DoS, 데이터 삭제, phishing 허용 여부 명시 |
| Recon | OSINT, DNS, 포트, 기술 스택 파악 | passive/active 구분 |
| Exploitation | 취약점 악용과 권한 획득 검증 | 영향 제한과 승인 필요 |
| Post-Exploitation | 권한 상승, lateral movement, data access 확인 | 증거 최소 수집 원칙 |
| Report/Retest | 위험도, 재현 절차, 조치안, 재검증 | CVSS+업무 영향 반영 |

> 요약: 침투 테스트는 공격 기술보다 scope와 ROE로 통제된 검증 구조를 갖춰야 함.

---

## Ⅲ. 동작원리 및 흐름도

```text
목표 합의 -> ROE 승인 -> 정찰/스캔 -> 취약점 후보 선정
-> exploit 검증 -> 영향도 확인 -> 보고서 작성 -> 보완 조치 -> retest
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 대상 시스템, 계정, 테스트 시간, 금지 행위 합의 | 승인서와 emergency contact 100% 확보 |
| 2 | OSINT, Nmap, Burp Suite, Nessus로 공격면 식별 | 스캔 로그와 대상 목록 일치 |
| 3 | exploit으로 인증 우회, RCE, 권한 상승 검증 | 증거 screenshot, command log 보존 |
| 4 | 데이터 접근, lateral movement 가능 범위 평가 | 민감정보 원문 미수집, hash/metadata 사용 |
| 5 | 보고, 조치, 재검증 수행 | critical 7일 SLA, retest pass 95% |

> 요약: 침투 테스트는 허가된 공격 흐름을 증거로 남기고 조치 후 재검증까지 수행해야 완료됨.

---

## Ⅳ. 특징

| 구분 | 취약점 스캔 | 침투 테스트 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 목적 | 취약점 후보 자동 식별 | 실제 침투 가능성 검증 | exploit 성공 여부 |
| 범위 | 넓은 IP·서비스 | 합의된 중요 시스템 | scope와 ROE |
| 산출물 | CVE 목록, 점수 | 공격 경로, 증거, 업무 영향 | critical 7일 SLA |
| 한계 | 오탐 존재 | 기간과 tester 역량 의존 | retest pass 95% |

> 요약: 침투 테스트는 스캔 결과를 공격 경로와 업무 영향 증거로 바꾸지만, 범위와 시간이 제한됨.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 평가 방식 | 정기 취약점 스캔 | 수동 exploit 검증 | 중요 서비스 출시 전, 연 1회 이상 |
| 깊이 | CVE와 설정 오류 | exploit chain과 권한 상승 | crown jewel 접근 경로 확인 필요 시 |
| 통제 | 자동 스캔 정책 | ROE, 승인, 증거 관리 | 운영 영향 허용 범위가 낮은 환경 |

> 요약: 침투 테스트는 중요 서비스와 규제 대상 시스템에서 스캔으로 증명되지 않는 침투 가능성을 검증할 때 선택함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 서비스 장애 | exploit, brute force, scan rate 과다 | ROE, rate limit, maintenance window | 장애 티켓 0건 |
| 법적 분쟁 | 승인 범위 초과, 제3자 자산 포함 | 서면 승인, IP allowlist, legal review | scope 위반 0건 |
| 증거 부족 | 재현 절차와 로그 미보존 | screenshot, command log, timestamp | finding 재현율 95% |
| 조치 미완료 | 보고서 전달 후 owner 부재 | remediation plan, retest, SLA | retest pass 95% |

> 요약: 침투 테스트 리스크는 장애, 범위 위반, 증거 부족, 조치 미완료이며 ROE와 retest로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 범위 준수 | scope 위반 0건 | activity log, ROE 대조 |
| 발견 품질 | high 이상 finding 재현율 95% | PoC 재실행, 로그 확인 |
| 보완 완료 | critical 7일, high 30일, retest pass 95% | ITSM, retest report |

> 요약: 침투 테스트 성과는 finding 개수보다 재현 가능한 증거, 범위 준수, 재검증 통과율로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 사전 통제: scope, ROE, emergency contact, 금지 행위, 테스트 시간대를 문서화하고 승인된 IP와 계정만 사용함.
2. 실행 기준: NIST SP 800-115, PTES, OWASP WSTG 기준으로 recon, exploitation, post-exploitation을 수행하되 민감정보는 hash와 metadata로 증명함.
3. 사후 조치: finding별 owner, CVSS+업무 영향, 7/30일 SLA, retest pass 기준을 보고서에 포함하고 SOAR/ITSM으로 추적함.

**결론 (2줄):**
- 기술사 판단: 취약점 스캔은 폭을, 침투 테스트는 깊이를 제공하므로 중요 시스템은 스캔 후 고위험 항목을 침투 테스트로 검증해야 함.
- 향후 방향: 침투 테스트는 CTEM, BAS, bug bounty와 결합되어 단발 평가에서 지속 검증 체계로 전환됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "침투 테스트 방법론을 설명하시오" | scoping부터 retest까지 절차 | 스캔과 침투 테스트 차이 |
| 요구사항 명시형 | "수행 방안을 제시하시오", "통제 방안을 설계하시오" | ROE, exploit 제한, 증거 보존 | 장애·법적 리스크, SLA, 재검증 |

> 요약: 설명형은 방법론 절차, 방안형은 ROE와 재검증 중심으로 목차를 전환함.
