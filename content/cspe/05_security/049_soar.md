---
title: "SOAR 보안 자동화 대응 (SOAR)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 49
---

# 📖 【암기용】 개념 완전 이해

> 목적: SOAR를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 보안 경보를 표준 플레이북, 커넥터, 승인 절차로 자동 처리하는 보안 오케스트레이션·대응 플랫폼
- **왜 필요한가**: SOC는 반복 경보와 수동 조회에 시간이 소요된다. SOAR는 IP 평판 조회, 계정 잠금, 티켓 생성, EDR 격리 같은 절차를 일관된 순서로 실행함.
- **핵심 직관**: 숙련 분석가가 매번 하는 확인 절차를 체크리스트와 버튼으로 만들어, 승인된 범위 안에서 시스템들이 같은 순서로 움직이게 하는 것임.

## 깊이 이해
- **배경·문제의식**: SIEM 경보가 많아지면 L1 분석가는 여러 콘솔에서 같은 정보를 반복 조회한다. 수작업은 누락, 지연, 증적 불일치를 만들고 중대 사고 대응 속도를 낮춤.
- **작동 원리**: SIEM, EDR, CTI, IAM, firewall이 connector로 연결된다. Playbook은 enrichment, decision, approval, action, rollback, evidence logging 단계를 정의하고 case management가 결과를 보존함.
- **비유**: 항공 관제에서 비상 상황별 체크리스트가 있고, 조종사 승인 후 자동 항법과 지상 관제가 동시에 움직이는 구조와 유사함.
- **구체 예시**: 피싱 경보가 들어오면 SOAR가 URL reputation 조회, 샌드박스 분석, 사용자 메일함 검색, 유사 메일 격리, 관리자 승인 후 계정 비밀번호 reset을 수행하고 티켓에 증적을 저장함.
- **흔한 오해·주의점**: SOAR는 모든 대응을 무조건 자동화하지 않는다. 계정 잠금, 네트워크 차단, 서버 격리처럼 업무 영향이 큰 조치는 승인과 rollback 조건이 필요함.

## 연결 개념
- SIEM - SOAR 플레이북을 시작하는 경보와 위험 점수 제공
- SOC - SOAR를 통해 반복 triage와 대응 절차를 표준화
- IR Runbook - 사고 유형별 수동 절차를 자동화 가능한 플레이북으로 전환

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: SOAR 답안은 playbook, connector, approval, rollback, case, MTTD/MTTR 지표를 SIEM 경보-자동 대응 흐름으로 연결해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SOAR는 보안 도구를 오케스트레이션하고 표준 플레이북으로 반복 대응을 자동 실행하는 플랫폼임.
> 2. **가치**: enrichment, triage, ticket, containment를 자동화해 MTTA와 MTTR을 단축하고 증적 일관성을 확보함.
> 3. **판단 포인트**: 자동화 범위, 승인 단계, rollback, connector 장애, 업무 영향 통제를 함께 써야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| SOAR 구조 이해 확인 | playbook, connector, case, approval, rollback | SIEM과 동일한 분석 플랫폼으로 설명 |
| 자동화 설계 판단 확인 | enrichment, decision, containment, recovery | 무승인 자동 차단을 일반화 |
| 운영 지표 확인 | MTTA, MTTR, 자동화 성공률, rollback률 | 자동화 기능 목록만 나열 |

> 요약: SOAR 문제는 대응 절차를 자동화하되 승인과 롤백으로 업무 영향을 통제하는 역량을 요구함.

---

## Ⅰ. 개요 및 필요성

SOAR는 보안 자동화 대응 플랫폼임. SIEM 경보와 CTI 정보를 받아 표준 플레이북으로 분석, 티켓, 차단, 복구를 수행함. 반복 경보 처리와 다중 콘솔 수작업을 줄여 SOC의 MTTA 15분 이하, MTTR 72시간 이하 목표 달성에 기여함.

---

## Ⅱ. 구조 및 구성요소

```text
SIEM Alert -> SOAR Case -> Enrichment Connector -> Decision
           -> Approval -> Action Connector -> Verification/Rollback
           +-> Ticket/Evidence/Metric 저장
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Playbook | 사고 유형별 처리 단계 정의 | 피싱, 악성 IP, 계정 탈취 등 |
| Connector | SIEM, EDR, IAM, firewall, CTI API 연계 | 인증 토큰, rate limit 관리 |
| Approval Gate | 업무 영향 조치 승인 | 서버 격리, 계정 잠금, 차단 정책 |
| Case Management | 티켓, 증적, 타임라인 저장 | 감사 로그와 보고서 생성 |
| Rollback/Verification | 조치 검증과 원복 | 차단 해제, 계정 복구, 서비스 확인 |

> 요약: SOAR는 플레이북과 커넥터를 중심으로 경보를 승인된 대응 조치와 증적 기록으로 전환함.

---

## Ⅲ. 동작원리 및 흐름도

```text
SIEM 경보 수신 -> 중복 제거 -> CTI/자산 enrichment
-> 위험 점수 산정 -> 승인 필요 여부 판단
-> EDR 격리/IAM 잠금/FW 차단 -> 검증 -> 티켓 종료
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | SIEM alert 수신과 case 생성 | case 생성 1분 이하 |
| 2 | CTI, CMDB, IAM, EDR 정보 보강 | enrichment 성공률 95% 이상 |
| 3 | playbook 분기와 승인 요청 | high impact action 승인 기록 100% |
| 4 | containment, notification, ticket 업데이트 | action success rate 95% 이상 |
| 5 | 검증, rollback, postmortem | rollback 가능 조치 100% 정의 |

> 요약: SOAR는 경보 수신 후 정보 보강, 판단, 승인, 조치, 검증을 자동화된 절차로 실행함.

---

## Ⅳ. 특징

| 구분 | 수동 SOC 대응 | SOAR 기반 대응 | 수치·통제 포인트 |
|:---|:---|:---|:---|
| 처리 방식 | 콘솔별 수동 조회 | API connector 기반 orchestration | enrichment 5분 이내 |
| 절차 | 분석가 경험 의존 | playbook, approval, rollback 표준화 | runbook 준수율 95% |
| 대응 | 티켓 후 수동 조치 | EDR 격리, IAM 잠금, FW 차단 | MTTA 15분 이하 |
| 증적 | 화면 캡처·메일 | case timeline, audit log | 증적 누락 0건 |

> 요약: SOAR는 반복 대응을 표준 절차와 API 조치로 전환해 SOC 대응 시간을 지표로 관리하게 함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 자동화 대상 | L1 수동 triage | enrichment, dedup, ticket, containment | 반복 경보 월 500건 이상 |
| 대응 통제 | 담당자 판단 | approval gate, RBAC, rollback | 업무 영향 action 포함 시 |
| 시스템 연계 | 단일 도구 | SIEM, EDR, IAM, CTI, ITSM connector | 5개 이상 보안 도구 연계 |

> 요약: SOAR는 반복 대응량과 연동 도구 수가 많고, 승인 가능한 표준 조치가 정의된 환경에 적합함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 오차단 | 오탐 경보에 자동 차단 실행 | risk threshold, approval, allowlist | false block 0건 |
| 커넥터 장애 | API 변경, 토큰 만료, rate limit | health check, retry, secret rotation | connector success 95% 이상 |
| 업무 영향 | 서버 격리·계정 잠금 범위 과다 | impact matrix, maintenance window, rollback | rollback time 10분 이하 |
| 자동화 남용 | 플레이북 변경 통제 부재 | change approval, versioning, audit | unauthorized change 0건 |

> 요약: SOAR 리스크는 오차단, 커넥터 장애, 업무 영향, 변경 통제이며 승인·롤백·감사로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 자동화 성과 | playbook 성공률 95%, 자동 triage 50% | SOAR execution log |
| 대응 시간 | MTTA 15분 이하, MTTR 72시간 이하 | case timeline |
| 통제 품질 | 승인 기록 100%, rollback 정의 100% | audit log, playbook review |

> 요약: SOAR 성과는 자동화 성공률, MTTA/MTTR, 승인·롤백 통제율로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 플레이북 선정: 피싱, 악성 IP, 계정 탈취처럼 반복 경보 상위 20%를 우선 자동화하고 enrichment, decision, action, rollback 단계를 정의함.
2. 승인 통제: EDR 격리, IAM 잠금, firewall 차단은 risk score 80 이상과 L2 승인 조건을 두고 rollback time 10분 이하 절차를 명시함.
3. 운영 지표: playbook success 95%, connector success 95%, automated triage 50%, false block 0건을 월간 SOC 지표로 관리함.

**결론 (2줄):**
- 기술사 판단: SOAR는 분석 플랫폼이 아니라 대응 자동화 플랫폼이므로 SIEM 탐지 품질과 runbook 표준화 후 적용해야 함.
- 향후 방향: 생성형 AI 보조 분석은 SOAR playbook 초안과 증적 요약에 적용하되 승인·감사 로그는 사람이 책임지는 구조로 유지함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "SOAR를 설명하시오", "보안 자동화를 기술하시오" | 경보 수신, enrichment, 승인, 조치, 검증 흐름 | 수동 대응과 SOAR 플레이북 차이 |
| 요구사항 명시형 | "도입 방안을 제시하시오", "운영 리스크를 제시하시오" | connector, approval, rollback, case 흐름 | 오차단, 커넥터 장애, MTTA/MTTR 기준 |

> 요약: 설명형은 SOAR 구성과 흐름을, 방안형은 승인·롤백·지표 중심 자동화 설계를 작성함.
