---
title: "SIEM vs SOAR 비교 (SIEM vs SOAR)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 50
---

# 📖 【암기용】 개념 완전 이해

> 목적: SIEM vs SOAR 비교를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: SIEM은 로그 분석·탐지 플랫폼이고, SOAR는 경보 후속 조치와 대응 자동화 플랫폼임
- **왜 필요한가**: 두 도구를 같은 제품군으로만 보면 답안이 기능 나열로 흐른다. 시험에서는 "탐지"와 "대응"의 책임 분리를 명확히 해야 함.
- **핵심 직관**: SIEM은 화재 감지기와 관제 화면, SOAR는 출동 지시서와 자동 소화 설비에 가까움.

## 깊이 이해
- **배경·문제의식**: SOC는 먼저 로그에서 침해 징후를 찾아야 하고, 그다음 티켓, 조회, 차단, 복구를 반복해야 한다. SIEM은 전자를, SOAR는 후자를 맡아 MTTD와 MTTR을 각각 관리함.
- **작동 원리**: SIEM은 log source, parser, normalization, correlation rule로 alert를 만든다. SOAR는 alert를 case로 받아 connector, playbook, approval, rollback을 통해 조치를 실행함.
- **비유**: 병원에서 검사 장비가 이상 수치를 찾아내는 것이 SIEM이고, 간호·처방·격리·퇴원 절차를 체크리스트대로 수행하는 것이 SOAR임.
- **구체 예시**: SIEM이 "10분 내 실패 로그인 20회 후 관리자 권한 추가" 경보를 만들면, SOAR는 AD 계정 조회, CTI 확인, L2 승인, 계정 잠금, 티켓 기록, 원복 조건 등록을 수행함.
- **흔한 오해·주의점**: SOAR가 있으면 SIEM이 필요 없어지는 것이 아니다. SOAR의 입력 품질은 SIEM 경보 품질과 룰 튜닝에 의존함.

## 연결 개념
- SOC - SIEM과 SOAR를 운영 지표와 역할 분리로 통합
- UEBA/XDR - SIEM 탐지 품질과 SOAR 대응 범위를 보완
- IR Runbook - SOAR 플레이북 설계의 원천 절차

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: SIEM vs SOAR 답안은 분석 플랫폼 vs 대응 자동화 구분, 로그 수집-상관분석-티켓-플레이북-검증-MTTD/MTTR 흐름을 제시해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SIEM은 보안 데이터를 분석해 경보를 생성하고, SOAR는 경보를 표준 절차와 API 조치로 대응함.
> 2. **가치**: SIEM은 MTTD를 줄이고 SOAR는 MTTA/MTTR을 줄이며 SOC의 탐지-대응 폐루프를 완성함.
> 3. **판단 포인트**: SIEM 품질 없이 SOAR 자동화를 확대하면 오차단이 발생하므로 룰 튜닝 후 승인 기반 자동화를 적용함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 도구 역할 구분 확인 | SIEM=로그 수집·정규화·상관분석, SOAR=playbook·connector·response | 둘을 모두 관제 솔루션으로 뭉뚱그림 |
| SOC 흐름 이해 확인 | alert, ticket, enrichment, approval, action, verification | 탐지와 대응 단계 연결 누락 |
| 도입 판단 확인 | MTTD, MTTA, MTTR, 오탐률, 자동화 성공률 | SOAR가 SIEM을 대체한다고 서술 |

> 요약: SIEM vs SOAR 문제는 탐지와 대응의 책임 분리, 연동 흐름, 지표 차이를 명확히 쓰는 것이 핵심임.

---

## Ⅰ. 개요 및 필요성

- 개요: 탐지와 대응 자동화 도구 비교
- 배경: SIEM과 SOAR를 모두 관제 도구로 묶으면 로그 분석, 경보 생성, 티켓, 승인, 차단, 롤백의 책임 경계가 흐려짐.
- 필요성: SOC는 SIEM으로 MTTD·오탐률·로그 coverage를 관리하고, SOAR로 MTTA·MTTR·playbook success 95%를 관리해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Log Source -> SIEM Collector/Parser -> Correlation Rule -> Alert
           -> SOAR Case -> Enrichment -> Approval -> Action/Rollback
           -> Ticket/Metric -> Rule Tuning/Playbook 개선
```

| 구성요소 | SIEM 역할 | SOAR 역할 |
|:---|:---|:---|
| 입력 | FW, EDR, IAM, Cloud 로그 | SIEM alert, CTI, ticket |
| 처리 | parser, normalization, correlation | playbook, connector, approval |
| 산출 | alert, dashboard, compliance report | case, action, evidence, rollback |
| 지표 | MTTD, coverage, parser error, false positive | MTTA, MTTR, playbook success, false block |

> 요약: SIEM은 경보 생성까지, SOAR는 경보 이후 대응 실행과 증적 관리까지 담당함.

---

## Ⅲ. 동작원리 및 흐름도

```text
로그 발생 -> SIEM 수집/정규화 -> 상관분석 경보
-> SOAR case 생성 -> CTI/자산 정보 보강 -> 승인 판단
-> 계정 잠금/호스트 격리/차단 -> 검증 -> 룰·플레이북 개선
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | SIEM이 로그 소스 수집과 parser 적용 | coverage 95%, parser error 1% 이하 |
| 2 | correlation rule과 risk score로 alert 생성 | false positive 30% 이하 |
| 3 | SOAR가 case 생성과 enrichment 수행 | enrichment 성공률 95% 이상 |
| 4 | 승인 후 EDR/IAM/FW 조치 실행 | 승인 기록 100%, action success 95% |
| 5 | 검증과 튜닝으로 폐루프 완성 | MTTD 24시간, MTTR 72시간 이하 |

> 요약: SIEM은 탐지 경보를 만들고 SOAR는 그 경보를 승인된 대응 조치와 개선 데이터로 전환함.

---

## Ⅳ. 특징

| 구분 | SIEM | SOAR | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 목적 | 로그 분석과 경보 생성 | 대응 절차 자동화 | MTTD vs MTTA/MTTR |
| 핵심 기술 | log source, parser, normalization, correlation | playbook, connector, approval, rollback | parser error 1%, success 95% |
| 주요 사용자 | SOC L1/L2 분석가, 감사 담당 | SOC L1/L2, IR, ITSM 담당 | 티켓 SLA 15분 |
| 실패 리스크 | 로그 누락, 오탐 폭증 | 오차단, 커넥터 장애 | false positive 30%, false block 0건 |

> 요약: SIEM은 분석 품질, SOAR는 대응 통제 품질이 성패를 좌우함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 도입 순서 | SOAR 단독 도입 | SIEM 탐지 품질 확보 후 SOAR 연동 | SIEM 오탐 30% 이하 달성 후 자동화 확대 |
| 운영 목표 | 로그 저장·조회 | 탐지-대응 폐루프 | MTTD와 MTTR 동시 관리 필요 시 |
| 자동화 범위 | 경보 생성 자동화 | enrichment, ticket, containment 자동화 | 반복 경보 월 500건 이상 |

> 요약: SIEM은 SOAR의 입력 품질을 결정하므로 탐지 튜닝 후 대응 자동화를 단계적으로 확대해야 함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| SOAR 오차단 | SIEM 오탐이 자동 조치로 전파 | risk threshold, approval gate, allowlist | false block 0건 |
| 탐지 공백 | SIEM 로그 소스 누락 | source inventory, heartbeat, coverage report | coverage 95% 이상 |
| 대응 지연 | 연동 커넥터 장애 | connector health check, retry, manual fallback | connector success 95% |
| 책임 혼선 | SOC와 IT 운영 RACI 부재 | RACI, escalation matrix, change approval | SLA 준수율 95% |

> 요약: SIEM-SOAR 연동 리스크는 오탐 전파, 로그 누락, 커넥터 장애, 책임 혼선이며 단계별 통제가 필요함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| SIEM 탐지 | MTTD 24시간 이하, 오탐 30% 이하 | alert disposition, incident timeline |
| SOAR 대응 | MTTA 15분 이하, MTTR 72시간 이하 | case timeline, execution log |
| 연동 품질 | action success 95%, 승인 기록 100% | SOAR audit, ITSM ticket |

> 요약: 통합 성과는 SIEM 탐지 지표와 SOAR 대응 지표를 분리해 측정해야 함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. SIEM 선행 정비: AD, EDR, IAM, cloud audit 로그 coverage 95%, parser error 1%, false positive 30% 이하를 달성한 뒤 SOAR 입력으로 사용함.
2. SOAR 단계 자동화: enrichment와 ticket은 즉시 자동화하고, 계정 잠금·EDR 격리·FW 차단은 L2 승인과 rollback time 10분 이하 조건으로 적용함.
3. 통합 운영: MTTD, MTTA, MTTR, false block, connector success를 월간 SOC KPI로 관리하고 rule tuning과 playbook review를 함께 수행함.

**결론 (2줄):**
- 기술사 판단: SIEM은 "무엇이 이상한가"를 찾고 SOAR는 "어떻게 조치할 것인가"를 실행하므로 대체 관계가 아니라 연계 관계임.
- 향후 방향: XDR, UEBA, CTI, SOAR가 결합된 통합 SOC에서 탐지 품질과 대응 통제를 분리 지표로 관리해야 함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "SIEM과 SOAR를 비교하시오" | SIEM 경보 생성과 SOAR 대응 실행의 연계 흐름 | 목적, 기술, 사용자, 지표 차이 |
| 요구사항 명시형 | "도입 방안을 제시하시오", "운영 방안을 설계하시오" | 로그 품질 확보, 플레이북 승인, 롤백 흐름 | 오탐 전파 방지, MTTD/MTTR, 자동화 범위 |

> 요약: 비교형은 역할 차이를, 설계형은 SIEM 품질 기반 SOAR 자동화 순서를 중심으로 작성함.
