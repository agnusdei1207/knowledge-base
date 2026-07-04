---
title: "위협 헌팅 (Threat Hunting)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 43
---

# 📖 【암기용】 개념 완전 이해

> 목적: 위협 헌팅을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 알림을 기다리지 않고 가설을 세워 숨어 있는 침해 흔적을 능동적으로 찾는 보안 활동
- **왜 필요한가**: APT와 fileless 공격은 정상 계정, PowerShell, cloud API처럼 합법 도구를 사용해 규칙 기반 알림을 피한다.
- **핵심 직관**: 화재 경보가 울리기만 기다리지 않고, 연기 냄새와 전기 사용 패턴을 보고 숨은 발화 지점을 찾는 방식임.

## 깊이 이해
- **배경·문제의식**: SIEM과 EDR 알림은 이미 알려진 패턴에 강하지만, 낮은 빈도 행위와 내부 계정 오남용은 조용히 지나간다. 위협 헌팅은 "우리 환경에 이런 TTP가 이미 존재할 수 있다"는 가정에서 시작한다.
- **작동 원리**: 가설 수립, 데이터 수집, 쿼리 실행, 결과 triage, 오탐 제거, 탐지 룰 전환, 대응 조치 순서로 진행한다.
- **비유**: 병원 건강검진처럼 증상이 없어도 혈액검사, 영상검사, 문진으로 초기 이상 징후를 찾는 활동임.
- **구체 예시**: "업무 시간 외 관리자 계정으로 PowerShell 4104 로그와 rare domain HTTPS 연결이 함께 발생했는가"라는 가설을 세우고 EDR, AD, DNS, proxy 로그를 30일 범위로 조회한다.
- **흔한 오해·주의점**: 위협 헌팅은 알림 대응의 다른 이름이 아니다. 사전 가설, 탐색 쿼리, 오탐 제거, 룰 전환 산출물이 있어야 함.

## 연결 개념
- MITRE ATT&CK - 헌팅 가설의 TTP 기준 제공
- SIEM/EDR/XDR - 헌팅 데이터와 쿼리 실행 기반
- CTI - 공격 그룹 TTP와 IoC를 헌팅 우선순위로 제공

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 위협 헌팅 답안은 hypothesis-driven hunting, 로그 소스, TTP, false positive 제거, 탐지 룰 전환까지 써야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Threat Hunting은 알려진 알림이 없는 상태에서 가설 기반으로 침해 흔적을 능동 탐색하는 SOC 활동임.
> 2. **가치**: 탐지 룰 공백, 장기 은닉, 정상 계정 오남용을 찾아 MTTD를 24시간 단위로 낮추는 운영 수단임.
> 3. **판단 포인트**: 가설, 데이터, 쿼리, triage, false positive, 룰 전환, 대응 조치가 한 흐름으로 제시되어야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 능동 탐지 개념 확인 | hypothesis-driven hunting, assume breach | SIEM 알림 대응과 동일시 |
| 운영 절차 이해 확인 | 데이터 수집, 쿼리, triage, 룰화 | 헌팅 도구명만 나열 |
| 탐지 품질 판단 확인 | false positive 제거, coverage 개선, MTTD | 오탐 처리와 지표 누락 |

> 요약: 위협 헌팅 문제는 숨어 있는 TTP를 가설로 찾아 탐지 룰로 환류하는 운영 절차를 요구함.

---

## Ⅰ. 개요 및 필요성

- 개요: 가설 기반 능동 탐지 활동
- 배경: 기존 알림은 알려진 IoC와 룰에 의존하므로 장기 은닉, 계정 오남용, fileless 행위가 경보 없이 지나갈 수 있음.
- 필요성: SOC는 ATT&CK, CTI, 90일 보존 로그를 결합해 헌팅 쿼리를 실행하고 rule conversion rate 30% 이상으로 룰 전환을 관리해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
CTI/ATT&CK -> Hunting Hypothesis -> Data Source -> Query
-> Triage -> False Positive 제거 -> Detection Rule -> IR/SOAR
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| 가설 | 특정 TTP가 내부에 존재한다는 탐색 문장 | ATT&CK technique, PIR 기반 |
| 데이터 소스 | EDR, AD, DNS, proxy, cloud audit | 30일 이상 조회 가능한 로그 필요 |
| 헌팅 쿼리 | 조건·빈도·상관 기준으로 이상 행위 검색 | KQL, SPL, Sigma |
| 환류 | 탐지 룰, playbook, 차단 정책으로 전환 | 오탐률과 owner 기록 |

> 요약: 위협 헌팅은 가설과 로그를 쿼리로 연결하고, 검증 결과를 탐지 룰과 대응 절차로 환류하는 구조임.

---

## Ⅲ. 동작원리 및 흐름도

```text
위협 시나리오 선정 -> 가설 작성 -> 로그 범위 확정
-> 쿼리 실행 -> 결과 triage -> 오탐 제거 -> 탐지 룰 등록
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | CTI와 ATT&CK으로 헌팅 주제 선정 | T1059, T1003, T1078 등 |
| 2 | EDR, AD, DNS, proxy 로그 질의 | 로그 보존 90일, 필드 누락률 |
| 3 | 결과를 자산·계정·시간대 기준 triage | incident 후보, benign 후보 분리 |
| 4 | 룰·대응 절차로 전환 | false positive rate, rule hit count |

> 요약: 헌팅은 가설 검증 후 오탐을 제거하고 반복 탐지가 가능한 룰로 바꾸는 폐루프 활동임.

---

## Ⅳ. 특징

| 구분 | 알림 기반 대응 | 위협 헌팅 | 수치·로그 포인트 |
|:---|:---|:---|:---|
| 시작점 | 발생한 alert | 가설과 CTI | PIR, ATT&CK ID |
| 분석 방식 | case 단위 triage | 30~90일 로그 탐색 | KQL/SPL query |
| 성과물 | incident ticket | detection rule, IOC, playbook | rule conversion rate |
| 한계 | 알려진 룰 의존 | 숙련도와 로그 품질 의존 | false positive rate 10% 이하 |

> 요약: 위협 헌팅은 알림 이전의 가설 검증이며, 산출물은 탐지 룰과 대응 playbook으로 남아야 함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 탐지 방식 | signature, alert | hypothesis-driven query | APT, insider threat, cloud misuse |
| 데이터 요구 | 단일 장비 로그 | EDR, identity, DNS, proxy, cloud | 다중 로그 90일 보존 시 |
| 운영 역할 | Tier 1 alert triage | Tier 2/3 analyst hunting | 고위험 TTP 주간 점검 |

> 요약: 위협 헌팅은 룰 기반 탐지 공백이 의심되고 장기 로그와 분석 인력이 있을 때 적용함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 오탐 과다 | 가설 범위가 넓음 | 자산 중요도, 시간대, 빈도 조건 추가 | false positive rate 10% 이하 |
| 데이터 공백 | EDR·DNS·cloud 로그 누락 | 로그 소스 inventory와 field completeness 점검 | field completeness 95% |
| 산출물 미전환 | 일회성 분석 종료 | 룰 등록, SOAR playbook, owner 지정 | rule conversion rate 30% 이상 |

> 요약: 헌팅 리스크는 오탐, 로그 공백, 일회성 분석이며 조건 튜닝과 룰 전환으로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 헌팅 주기 | 고위험 TTP 주 1회 | hunting calendar |
| 탐지 전환 | 헌팅 10건 중 룰 3건 이상 | detection engineering backlog |
| 탐지 시간 | MTTD 24시간 이하 목표 | incident timeline, alert timestamp |

> 요약: 위협 헌팅 성과는 수행 횟수보다 룰 전환률, MTTD, 고위험 TTP 커버리지로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 가설 수립: CTI의 공격 그룹 TTP와 내부 crown jewel 자산을 연결해 "업무 외 시간 관리자 PowerShell 실행" 같은 PIR 기반 가설을 작성함.
2. 데이터 분석: EDR, AD event 4624/4672, PowerShell 4104, DNS, proxy, cloud audit 로그를 90일 범위로 KQL/SPL 질의함.
3. 운영 환류: 확인된 패턴을 Sigma/EDR 룰과 SOAR playbook으로 등록하고 false positive rate, hit count, owner를 월 1회 검토함.

**결론 (2줄):**
- 기술사 판단: 위협 헌팅은 알림 대응 조직이 아니라 가설, 데이터, 룰 전환 역량을 갖춘 SOC에서 효과가 검증됨.
- 향후 방향: ATT&CK 기반 hunting library와 XDR telemetry를 결합해 고위험 TTP 탐지를 주기 운영 지표로 관리해야 함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "위협 헌팅을 설명하시오" | 가설 수립부터 룰 전환까지 흐름 | 알림 대응과 능동 탐지 차이 |
| 요구사항 명시형 | "운영 방안을 제시하시오", "SOC 적용을 설계하시오" | 로그 소스, 쿼리, false positive 제거 | MTTD, 룰 전환률, 주기 운영 지표 |

> 요약: 설명형은 개념과 절차, 운영형은 가설 품질과 탐지 전환 지표를 중심으로 작성함.
