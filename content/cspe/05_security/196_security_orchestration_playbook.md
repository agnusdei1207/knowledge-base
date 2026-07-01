---
title: "보안 오케스트레이션 플레이북 (Security Orchestration Playbook)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 196
---

# 📖 【암기용】 개념 완전 이해

> 목적: 보안 오케스트레이션 플레이북을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 사고 유형별 보안 대응 절차를 조건, 승인, 자동 조치, 증적으로 정의한 실행 문서
- **왜 필요한가**: SOC가 피싱, 계정 탈취, 악성 IP 같은 반복 경보를 매번 수동 처리하면 누락과 지연이 발생함. 플레이북은 CISA 사고 대응 절차처럼 식별, 조정, 복구, 추적 단계를 같은 순서로 수행하게 함.
- **핵심 직관**: 숙련 분석가의 머릿속 절차를 조건문과 체크리스트로 옮겨, SOAR와 사람이 같은 기준으로 움직이게 만드는 대응 악보임.

## 깊이 이해
- **배경·문제의식**: SIEM과 EDR은 경보를 만들지만 누가 어떤 조건에서 계정을 잠그고, 방화벽을 차단하며, 언제 원복할지는 별도 설계가 필요함. 플레이북이 없으면 MTTA, MTTR, 감사 증적이 분석가마다 달라짐.
- **작동 원리**: trigger, enrichment, decision, approval, action, verification, rollback, evidence로 구성함. 각 단계는 API 커넥터, 권한, 실패 시 대체 절차, SLA를 함께 가진다.
- **비유**: 병원 응급실 triage 프로토콜과 유사함. 체온과 산소포화도 기준으로 우선순위를 정하고, 의사 승인 후 처치하며, 처치 결과와 투약 기록을 남김.
- **구체 예시**: 피싱 신고 1건이 들어오면 URL 평판 조회 1분, 샌드박스 분석 5분, 동일 메일 검색 10분, 유사 메일 격리, 사용자 비밀번호 reset 승인, 티켓 증적 저장 순서로 실행함.
- **흔한 오해·주의점**: 플레이북은 자동화 스크립트 목록이 아님. 업무 영향 조치에는 승인권자, 차단 범위, 원복 기준, 변경 이력, 실패 시 수동 절차가 필요함.

## 연결 개념
- SOAR - 플레이북을 실행하는 오케스트레이션 플랫폼
- NIST SP 800-61 Rev.3 - 사고 대응을 위험관리 활동과 연결하는 기준
- MITRE ATT&CK - 플레이북 trigger와 탐지 조건을 TTP 기준으로 매핑

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 플레이북 답안은 자동화 절차보다 승인, 원복, 증적, MTTA/MTTR, 변경통제까지 써야 채점 포인트가 살아남.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 보안 오케스트레이션 플레이북은 사고 유형별 대응을 trigger, enrichment, decision, action, rollback으로 표준화한 실행 절차임.
> 2. **가치**: 반복 triage와 조치 시간을 줄이고 MTTA 15분, high impact 승인 기록 100%, 증적 누락 0건을 목표로 관리함.
> 3. **판단 포인트**: 자동 실행 범위, 승인 gate, 커넥터 장애, 원복 시간, playbook versioning을 함께 제시해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| SOC 자동 대응 설계 확인 | trigger, enrichment, decision, approval, action, rollback | 단순 스크립트 자동 실행으로만 설명 |
| 업무 영향 통제 확인 | 승인권자, 차단 범위, allowlist, rollback time | 무승인 계정 잠금·네트워크 차단 일반화 |
| 운영 지표 확인 | MTTA, MTTR, playbook success, false block, audit log | 절차 설명 후 측정 지표 누락 |

> 요약: 이 문제는 보안 자동화를 실행 절차, 통제, 지표로 설계하는 역량을 요구함.

---

## Ⅰ. 개요 및 필요성

플레이북은 사고 대응 실행 절차서임. SIEM 경보와 SOAR 커넥터를 연결해 반복 사고를 같은 순서로 처리하고, 승인·원복·증적을 남긴다. CISA·NIST 사고 대응 권고처럼 식별, 분석, 대응, 복구가 지표로 추적되어야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Alert/Report -> Trigger -> Enrichment -> Decision
  / Human Approval -> Action -> Verification -> Rollback
  / Case Timeline -> Evidence -> Metric -> Review
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Trigger | SIEM, EDR, 신고, CTI hit로 실행 시작 | ATT&CK ID, severity, asset criticality 조건 |
| Enrichment | IP, URL, hash, 사용자, 자산 정보 보강 | STIX/TAXII, CMDB, IAM, EDR API |
| Decision | 위험 점수와 분기 조건 판단 | risk score 0~100, confidence 70 이상 |
| Approval/Action | 승인 후 격리, 잠금, 차단, 티켓 수행 | RBAC, maker-checker, change log |
| Verification/Rollback | 조치 결과 확인과 원복 | rollback time 10분 이하, evidence 보존 |

> 요약: 플레이북은 경보를 정보 보강, 판단, 승인, 조치, 검증, 원복으로 연결하는 통제형 실행 구조임.

---

## Ⅲ. 동작원리 및 흐름도

```text
피싱 신고 -> URL 평판/샌드박스 분석 -> 동일 메일 검색
-> 위험 점수 산정 -> 승인 필요 여부 판단
-> 메일 격리/계정 reset/EDR scan -> 검증 -> 사후 개선
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 경보 중복 제거와 case 생성 | case 생성 1분 이하 |
| 2 | CTI, 자산, 사용자, 로그 보강 | enrichment 성공률 95% 이상 |
| 3 | 위험 점수와 업무 영향도 산정 | high impact action 승인 100% |
| 4 | 차단, 격리, 통보, 티켓 업데이트 | action success 95% 이상 |
| 5 | 원복 가능성 확인과 post-incident review | false block 0건, rollback 10분 이하 |

> 요약: 플레이북은 경보 입력부터 사후 개선까지 동일 절차를 반복 실행하고 각 단계의 시간과 성공률을 남김.

---

## Ⅳ. 특징

| 구분 | 수동 Runbook | 오케스트레이션 Playbook | 수치·통제 포인트 |
|:---|:---|:---|:---|
| 실행 방식 | 문서 기반 수동 처리 | SOAR API와 승인 workflow 실행 | MTTA 15분 이하 |
| 품질 통제 | 담당자 경험 의존 | 조건, 임계값, allowlist, rollback 정의 | false block 0건 |
| 증적 | 캡처·메일 중심 | case timeline, audit log, evidence store | 증적 누락 0건 |
| 변경관리 | 문서 수정 이력 분산 | Git/version, 승인, 테스트 케이스 관리 | 변경 승인 100% |

> 요약: 플레이북은 대응 절차를 자동 실행 가능한 조건과 감사 가능한 증적으로 바꾸는 SOC 운영 자산임.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 대상 사고 | 임의 수동 대응 | 피싱, 계정 탈취, 악성 IP 등 반복 사고 | 월 100건 이상 반복 경보 |
| 통제 구조 | 담당자 재량 | approval, RBAC, rollback, allowlist | 업무 영향 조치 포함 시 |
| 운영 방식 | 문서 배포 | versioning, test, metric 기반 개선 | SOAR·ITSM 연동 3개 이상 |

> 요약: 플레이북은 반복성과 표준 조치가 높은 사고부터 적용하고, 업무 영향이 큰 조치는 승인과 원복을 선행해야 함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 오차단 | 저신뢰 경보에 자동 action 실행 | confidence 70 이상, allowlist, L2 승인 | false block 0건 |
| 커넥터 실패 | API 변경, 토큰 만료, rate limit | health check, retry, secret rotation | connector success 95% 이상 |
| 절차 노후화 | 공격 TTP 변화와 미반영 룰 | ATT&CK 분기 리뷰, 월 1회 tabletop | stale playbook 0건 |
| 권한 남용 | 자동 조치 계정 권한 과다 | JIT 권한, RBAC, 감사 로그 | privileged action 기록 100% |

> 요약: 플레이북 리스크는 오차단, 커넥터 장애, 노후화, 권한 남용이며 승인·검증·변경관리로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 대응 시간 | MTTA 15분 이하, MTTR 72시간 이하 | case timestamp, SOAR log |
| 실행 품질 | playbook success 95%, rollback 10분 이하 | execution report, drill 결과 |
| 감사성 | 승인·증적·변경 이력 100% 보존 | ITSM ticket, audit log |

> 요약: 플레이북 성과는 시간, 실행 성공률, 감사 이력으로 측정하고 분기별 훈련으로 보정함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 우선순위 선정: 반복 경보 상위 20%인 피싱, 악성 IP, 계정 탈취를 선정하고 trigger, action, owner, SLA를 정의함.
2. 안전장치 설계: EDR 격리, IAM 잠금, firewall 차단은 risk score 80 이상과 L2 승인, rollback 10분 이하 조건을 둠.
3. 지속 개선: 월 1회 tabletop과 분기별 purple team으로 playbook success 95%, false block 0건, stale playbook 0건을 검증함.

**결론 (2줄):**
- 기술사 판단: 플레이북은 자동화보다 통제 설계가 우선이며, SIEM 탐지 품질과 승인·원복 기준이 있을 때 SOAR 적용이 타당함.
- 향후 방향: CTI 자동화, ATT&CK coverage, 생성형 AI 요약을 결합하되 최종 차단 책임과 감사 로그는 조직 통제 체계에 남겨야 함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "플레이북을 설명하시오", "보안 오케스트레이션을 기술하시오" | trigger, enrichment, 승인, 조치, 원복 흐름 | 수동 runbook과 자동 playbook 차이 |
| 요구사항 명시형 | "도입 방안을 제시하시오", "운영 리스크를 설명하시오" | 사고 유형별 분기, 승인 gate, rollback 절차 | 오차단, 커넥터 장애, MTTA/MTTR 지표 |

> 요약: 설명형은 구조와 흐름, 방안형은 승인·원복·지표 기반 운영 설계를 중심으로 작성함.
