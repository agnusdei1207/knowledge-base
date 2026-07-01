---
title: "레드팀·블루팀·퍼플팀 (Red Blue Purple Team)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 60
---

# 📖 【암기용】 개념 완전 이해

> 목적: 레드팀·블루팀·퍼플팀을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 레드팀은 공격을 재현하고, 블루팀은 탐지·대응하며, 퍼플팀은 두 결과를 연결해 탐지 룰과 대응 절차를 개선하는 체계
- **왜 필요한가**: 공격 훈련만 하고 끝나면 방어 역량이 남지 않고, 방어팀만 운영하면 실제 공격자의 우회 경로를 검증하기 어렵다.
- **핵심 직관**: 모의 침투 부대, 방어 관제팀, 합동 훈련 코치가 함께 훈련 기록을 보며 탐지와 대응을 고치는 구조임.

## 깊이 이해
- **배경·문제의식**: SOC는 로그와 룰을 보유해도 실제 공격 TTP를 탐지하는지 확인해야 한다. 레드팀은 ATT&CK 기반으로 공격 시나리오를 실행하고, 블루팀은 SIEM/EDR로 탐지와 대응을 수행하며, 퍼플팀은 탐지 공백과 대응 지연을 룰, playbook, 교육으로 환류함.
- **작동 원리**: 목표와 ROE를 정하고 레드팀이 phishing, credential access, lateral movement, exfiltration을 시뮬레이션한다. 블루팀은 alert, triage, containment를 수행하고 퍼플팀은 TTP별 탐지 성공 여부와 로그 공백을 분석함.
- **비유**: 축구 공격수와 수비수가 따로 연습하는 것이 아니라, 전술 코치가 경기 영상을 보며 어떤 패턴에서 실점했는지 수비 전술을 바꾸는 방식임.
- **구체 예시**: 레드팀이 ATT&CK T1059 PowerShell을 실행했는데 SIEM 탐지가 없으면, 퍼플팀은 PowerShell 4104 로그 수집, Sigma rule, SOAR playbook, analyst runbook을 추가함.
- **흔한 오해·주의점**: 퍼플팀은 별도 조직명만 의미하지 않는다. 공격 결과를 방어 탐지와 대응 절차로 전환하는 협업 방식이 핵심임.

## 연결 개념
- MITRE ATT&CK - 공격 시뮬레이션과 탐지 매핑 기준
- SIEM/EDR/SOAR - 블루팀 탐지와 대응 도구
- BAS/Threat Hunting - 퍼플팀 개선 과제의 검증 수단

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Red/Blue/Purple Team 답안은 공격 시뮬레이션, 방어 검증, 탐지 룰 개선 폐루프와 ATT&CK coverage를 제시해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Red Team은 공격자 TTP를 재현하고 Blue Team은 탐지·대응하며 Purple Team은 두 결과를 결합해 탐지·대응 품질을 개선함.
> 2. **가치**: 실제 공격 시나리오별 로그, alert, triage, containment 성공 여부를 측정해 SOC 공백을 수치화함.
> 3. **판단 포인트**: 단발 모의해킹이 아니라 ATT&CK mapping, detection rule, playbook, retest로 이어지는 폐루프가 핵심임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 역할 구분 확인 | Red=attack simulation, Blue=detect/respond, Purple=feedback | 팀 이름만 나열 |
| 운영 흐름 확인 | ROE, ATT&CK scenario, log, alert, containment, rule tuning | 공격 성공 여부만 강조 |
| 성과 측정 확인 | detection coverage, MTTD, MTTR, retest pass | 개선 지표와 재검증 누락 |

> 요약: 이 문제는 공격과 방어를 분리 설명하는 것이 아니라 탐지 룰 개선 폐루프로 연결하는 역량을 요구함.

---

## Ⅰ. 개요 및 필요성

레드·블루·퍼플팀은 공격방어 검증 체계임. 레드팀은 실제 공격을 재현하고 블루팀은 탐지와 대응을 수행하며 퍼플팀은 탐지 공백을 룰과 playbook으로 보완한다. APT와 계정 기반 공격 대응에는 공격 시뮬레이션과 방어 검증의 반복 운영이 필요함.

---

## Ⅱ. 구조 및 구성요소

```text
Threat Objective -> Red Team Scenario/ROE -> Attack Simulation
                 -> Blue Team Detect/Respond -> Purple Team Gap Analysis
                 -> Rule/Playbook 개선 -> Retest
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Red Team | ATT&CK 기반 공격 시나리오 실행 | phishing, credential access, lateral movement |
| Blue Team | SIEM, EDR, NDR로 탐지·대응 | alert triage, containment, IR |
| Purple Team | 공격 로그와 방어 결과를 매핑 | detection gap, rule tuning, runbook 개선 |
| ROE | 범위, 기간, 금지 행위, 연락망 정의 | 운영 장애와 법적 리스크 통제 |
| Metrics | 탐지율, MTTD, MTTR, retest pass 측정 | ATT&CK coverage 기준 |

> 요약: 세 팀의 차이는 역할이며, 퍼플팀은 공격 결과를 방어 개선 산출물로 전환하는 연결 기능임.

---

## Ⅲ. 동작원리 및 흐름도

```text
위협 시나리오 선정 -> ROE 승인 -> 레드팀 TTP 실행
-> 블루팀 탐지/대응 -> 로그와 alert 대조 -> 탐지 공백 분석
-> 룰/playbook 수정 -> 재실행 검증
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | crown jewel과 ATT&CK TTP 기반 시나리오 선정 | TTP coverage와 업무 영향 명시 |
| 2 | 레드팀이 phishing, C2, lateral movement 실행 | ROE 위반 0건 |
| 3 | 블루팀이 SIEM/EDR alert triage와 containment 수행 | MTTD 30분, MTTR 4시간 목표 |
| 4 | 퍼플팀이 탐지 성공/실패와 로그 공백을 매핑 | detection coverage 80% 이상 |
| 5 | Sigma/EDR rule, SOAR playbook, runbook 수정 후 retest | retest pass 95% |

> 요약: 운영 흐름은 공격 재현, 방어 대응, 공백 분석, 탐지 룰 개선, 재검증으로 닫혀야 함.

---

## Ⅳ. 특징

| 구분 | Red Team | Blue Team | Purple Team |
|:---|:---|:---|:---|
| 목적 | 공격 경로 검증 | 탐지·대응 수행 | 공격 결과를 방어 개선으로 전환 |
| 기준 | ATT&CK TTP, objective | alert, incident, containment | coverage, MTTD, MTTR |
| 산출물 | attack path, evidence | incident timeline, 대응 기록 | detection rule, playbook, gap report |
| 수치 포인트 | ROE 위반 0건 | MTTD 30분, MTTR 4시간 | retest pass 95% |

> 요약: Red는 공격 검증, Blue는 대응 실행, Purple은 탐지·대응 개선 지표를 만드는 역할임.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 평가 방식 | 연 1회 모의해킹 | Red/Blue/Purple 반복 훈련 | SOC와 중요 시스템이 있는 조직 |
| 결과 활용 | 취약점 보고서 | 탐지 룰, SOAR playbook, analyst training | 탐지 공백 개선이 목표일 때 |
| 성숙도 | 공격 검증 중심 | 공격방어 협업과 retest | ATT&CK coverage 측정 가능 시 |

> 요약: Red/Blue/Purple 체계는 모의해킹 결과를 SOC 탐지와 대응 개선으로 환류할 수 있을 때 효과가 검증됨.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 운영 장애 | 공격 시뮬레이션 강도 과다 | ROE, kill switch, maintenance window | 장애 티켓 0건 |
| 방어팀 학습 부재 | 결과 공유와 룰화 미흡 | purple workshop, ATT&CK mapping | rule conversion 70% 이상 |
| 탐지 착시 | 테스트용 IoC만 탐지 | behavior-based rule, negative test | TTP coverage 80% 이상 |
| 반복성 부족 | 단발 이벤트 종료 | quarterly exercise, BAS retest | retest pass 95% |

> 요약: 주요 리스크는 장애, 학습 부재, 탐지 착시, 반복성 부족이며 ROE와 retest 지표로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 탐지 커버리지 | ATT&CK 고위험 TTP 80% 이상 | scenario matrix, SIEM rule mapping |
| 대응 시간 | MTTD 30분, MTTR 4시간 | incident timeline, SOAR case |
| 개선 환류 | rule conversion 70%, retest pass 95% | detection backlog, 재실행 결과 |

> 요약: 성과는 공격 성공보다 탐지 커버리지, 대응 시간, 룰 전환, 재검증 통과율로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 시나리오 설계: crown jewel별 ATT&CK TTP를 선정하고 phishing, credential access, lateral movement, exfiltration을 ROE 안에서 실행함.
2. 방어 검증: SIEM, EDR, NDR, IAM 로그를 대조해 MTTD 30분, MTTR 4시간, ATT&CK coverage 80%를 기준으로 측정함.
3. 퍼플팀 환류: 미탐 TTP를 Sigma/EDR rule, SOAR playbook, analyst runbook으로 전환하고 분기별 retest pass 95%를 목표로 운영함.

**결론 (2줄):**
- 기술사 판단: 단순 모의해킹이 목표이면 Red Team 중심, SOC 탐지 품질 개선이 목표이면 Purple Team 폐루프까지 운영해야 함.
- 향후 방향: BAS, XDR, ATT&CK Navigator와 결합해 공격방어 훈련 결과를 detection engineering backlog로 지속 관리하는 체계가 필요함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "레드팀·블루팀·퍼플팀을 설명하시오" | 공격 시뮬레이션과 방어 검증 흐름 | 세 팀 역할과 산출물 차이 |
| 요구사항 명시형 | "운영 방안을 제시하시오", "SOC 개선 방안을 설계하시오" | ATT&CK mapping, 탐지 공백, 룰 개선 | MTTD/MTTR, retest, rule conversion |

> 요약: 설명형은 역할 구분, 운영형은 공격 시뮬레이션-방어 검증-탐지 룰 개선 폐루프를 중심으로 작성함.
