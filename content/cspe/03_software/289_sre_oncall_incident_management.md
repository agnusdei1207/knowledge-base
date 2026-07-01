---
title: "SRE 온콜 관리·인시던트 대응 (SRE Oncall Incident Management)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 289
---

# 📖 【암기용】 개념 완전 이해

> 목적: SRE 온콜 관리·인시던트 대응을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 서비스 장애를 감지, 호출, 대응, 복구, 회고하는 운영 체계
- **왜 필요한가**: 24시간 서비스는 장애가 발생한다. 누가 호출되고, 어떤 기준으로 심각도를 정하며, 어떻게 복구하고 재발을 막을지 절차가 있어야 한다.
- **핵심 직관**: 온콜은 소방서 당직과 같다. 경보가 울리면 담당자가 출동하고, 지휘 체계와 복구 매뉴얼에 따라 피해 시간을 줄인다.

## 깊이 이해
- **배경·문제의식**: 장애 대응이 개인 경험에 의존하면 알림 누락, 중복 지휘, 늦은 escalation, 원인 미기록이 반복된다. SRE는 SLO와 error budget을 기준으로 장애 우선순위를 정한다.
- **작동 원리**: 모니터링 경보가 발생하면 oncall rotation과 escalation policy에 따라 담당자를 호출한다. Incident Commander가 역할을 나누고, runbook으로 복구하며, postmortem으로 재발 방지 항목을 관리한다.
- **비유**: 응급실에서 triage로 중증도를 분류하고, 담당 의사가 처치하며, 치료 후 회의로 재발 방지 조치를 정하는 흐름과 같다.
- **구체 예시**: 결제 성공률이 SLO 99.9%에서 99.5%로 하락하면 Sev2로 선언하고, 5분 내 담당자 호출, 30분 내 우회 라우팅, 24시간 내 postmortem을 수행한다.
- **흔한 오해·주의점**: 온콜은 사람을 밤새 대기시키는 제도가 아니다. 알림 품질, runbook, 자동 복구, 교대 정책이 없으면 피로와 대응 누락이 누적된다.

## 연결 개념
- SLO/Error Budget - 장애 심각도와 우선순위 기준
- Observability - 경보와 원인 분석 데이터
- Postmortem - 재발 방지 학습 절차

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 온콜 근무표가 아니라 SLO 기반 감지, escalation, 역할 분담, 복구, postmortem 체계를 제시한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SRE 온콜·인시던트 대응은 서비스 이상을 SLO 기준으로 감지하고 역할 기반으로 복구·회고하는 운영 프로세스이다.
> 2. **가치**: MTTD, MTTA, MTTR, 재발률을 줄이고 장애 대응을 개인 경험에서 조직 프로세스로 전환한다.
> 3. **판단 포인트**: 알림 품질, escalation policy, incident role, runbook, postmortem action item을 함께 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| SRE 운영 체계 이해 확인 | SLO, alert, oncall, escalation, postmortem | 장애 신고 절차만 나열 |
| 인시던트 대응 설계 판단 확인 | Sev 등급, Incident Commander, runbook | 원인 분석과 재발 방지 누락 |
| 운영 지표 적용 역량 확인 | MTTD, MTTA, MTTR, alert fatigue | 알림을 많이 만들면 된다고 작성 |

> 요약: 이 문제는 장애 대응 체계를 지표와 역할, 회고까지 연결하는 운영 설계 역량을 요구한다.

---

## Ⅰ. 개요 및 필요성

SRE 온콜은 장애 대응 운영 체계이다. 서비스 장애는 사용자 영향 시간과 매출 손실을 만들기 때문에 감지, 호출, 지휘, 복구, 회고 절차가 필요하다. SLO와 Sev 등급으로 우선순위를 정하고 MTTR 30분 이하 같은 목표로 운영한다.

---

## Ⅱ. 구조 및 구성요소

```text
Monitoring Alert -> Oncall Routing -> Escalation -> Incident Command -> Runbook Recovery -> Postmortem
                         +-> SLO/Sev Classification
                         +-> Status Communication
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Alert Rule | SLO 위반과 증상 기반 경보 생성 | burn rate alert, synthetic check |
| Oncall Rotation | 1차·2차 담당자 배정 | PagerDuty, Opsgenie |
| Escalation Policy | 미응답·고심각도 시 상위 호출 | MTTA 5분 이하 |
| Incident Role | 지휘, 커뮤니케이션, 작업 담당 분리 | Incident Commander |
| Postmortem | 원인과 재발 방지 항목 관리 | blameless, action owner |

> 요약: SRE 인시던트 체계는 경보부터 회고까지 역할과 지표로 연결된 운영 프로세스이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
SLO 위반 감지 -> 담당자 호출 -> 심각도 선언 -> 역할 배정 -> 복구 실행 -> 회고/재발방지
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | SLO와 증상 기반 alert 발생 | MTTD 5분 이하 |
| 2 | oncall 담당자 호출과 응답 확인 | MTTA 5분 이하 |
| 3 | Sev 등급과 Incident Commander 지정 | Sev1/Sev2 기준 문서화 |
| 4 | runbook 기반 완화·복구 수행 | MTTR 30분 이하 |
| 5 | postmortem과 action item 추적 | 재발 방지 완료율 95% 이상 |

> 요약: SRE 대응은 감지, 호출, 지휘, 복구, 회고를 시간 지표로 통제한다.

---

## Ⅳ. 특징

| 구분 | 전통 장애 대응 | SRE 온콜·인시던트 대응 | 수치·기술 포인트 |
|:---|:---|:---|:---|
| 기준 | 담당자 경험 | SLO, error budget | burn rate alert |
| 호출 | 수동 연락 | rotation, escalation | MTTA 5분 이하 |
| 지휘 | 중복 의사결정 | Incident Commander | role-based response |
| 회고 | 원인 문서 일부 | blameless postmortem | action item 완료율 95% |

> 요약: SRE 방식은 장애 대응을 개인 숙련에서 SLO와 역할 기반 운영 체계로 전환한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 업무시간 대응 중심 | 24x7 oncall과 escalation | SLA 99.9% 이상 서비스 |
| 비용/성능 | 알림 다수 생성 | SLO 기반 alert 압축 | alert fatigue 월 10건 이하 |
| 운영/위험 | 장애 후 수습 | runbook과 postmortem 학습 | MTTR 30분 이하 요구 |

> 요약: 사용자 영향이 큰 서비스는 SLO 기반 alert와 역할 분담형 인시던트 대응이 필요하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Alert Fatigue | 증상 아닌 원인별 경보 과다 | SLO burn rate alert, deduplication | actionable alert 80% 이상 |
| Escalation 지연 | 담당자 미응답·연락망 누락 | 1차/2차/관리자 escalation | MTTA 5분 이하 |
| 재발 반복 | postmortem action 미완료 | owner, due date, 월간 추적 | 재발률 월 1건 이하 |

> 요약: 온콜 운영의 리스크는 경보 피로, 호출 지연, 재발이며 지표와 소유자로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 감지 | MTTD 5분 이하 | monitoring event timestamp |
| 대응 | MTTA 5분 이하, MTTR 30분 이하 | incident timeline |
| 학습 | action item 완료율 95% 이상 | postmortem tracker |

> 요약: SRE 인시던트 체계는 감지, 대응, 학습 지표가 함께 관리될 때 재발을 줄인다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 서비스별 SLO와 burn rate alert를 정의하고 Sev1/Sev2/Sev3 기준을 사용자 영향과 error budget 소모율로 설정함
2. PagerDuty/Opsgenie로 1차·2차·관리자 escalation을 구성하고 MTTA 5분 이하를 목표로 온콜 훈련을 수행함
3. 주요 장애 유형별 runbook을 작성하고 postmortem action item에 owner와 due date를 부여해 완료율 95% 이상을 관리함

**결론 (2줄):**
- 기술사 판단: SLA 99.9% 이상 서비스는 SLO 기반 alert, 온콜 rotation, incident role, postmortem을 필수 운영 체계로 둠
- 향후 방향: SRE 대응은 AIOps 알림 상관분석, 자동 완화, error budget 기반 릴리스 제어와 결합됨

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "SRE 인시던트 대응을 설명하시오" | 감지·호출·복구·회고 흐름 | 전통 운영과 SRE 차이 |
| 요구사항 명시형 | "장애 대응 체계 구축 방안을 제시하시오" | Sev, escalation, runbook 절차 | MTTD, MTTA, MTTR, postmortem 지표 |

> 요약: 설명형은 운영 프로세스, 방안형은 지표와 역할 기반 구축 절차 중심으로 전개한다.
