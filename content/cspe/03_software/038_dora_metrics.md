---
title: "애자일 DORA 메트릭 (DORA Metrics)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 38
---

# 📖 【암기용】 개념 완전 이해

> 목적: DORA Metrics를 처음 보는 사람도 DevOps 성과 측정 지표로 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: DORA Metrics는 소프트웨어 전달 성과를 배포·변경·복구 지표로 측정하는 4대 지표
- **왜 필요한가**: 개발 조직은 기능을 많이 만들었다고 성과가 입증되지 않는다. 배포 빈도, 변경 리드타임, 변경 실패율, MTTR을 함께 봐야 납기와 운영 품질의 균형을 판단할 수 있다.
- **핵심 직관**: 병원이 수술 건수만 보지 않고 회복 시간과 재수술률을 함께 보는 것처럼, 개발도 배포 속도와 실패·복구를 같이 봐야 한다.

## 깊이 이해
- **배경·문제의식**: 전통적 프로젝트 지표는 일정 준수와 투입 인력 중심이라 실제 고객 가치 전달 속도와 운영 리스크를 설명하지 못한다. DORA는 DevOps Research and Assessment에서 제시한 지표로 software delivery performance를 정량화한다.
- **작동 원리**: Deployment Frequency는 얼마나 자주 배포하는지, Lead Time for Changes는 커밋부터 운영 반영까지 걸리는 시간, Change Failure Rate는 배포 후 장애·롤백 비율, MTTR은 장애 복구 시간을 측정한다.
- **비유**: 택배 회사가 발송 횟수, 주문 접수부터 배송까지 시간, 오배송률, 문제 해결 시간을 함께 보는 방식이다.
- **구체 예시**: 한 팀이 주 5회 배포, 변경 리드타임 6시간, 변경 실패율 8%, MTTR 25분을 유지하면 배포 속도와 운영 복구가 균형을 이룬 상태로 판단 가능함.
- **흔한 오해·주의점**: Elite/High 등급 수치 범위 암기보다 팀의 추세와 병목 원인 분석이 우선이다. 배포 빈도만 높이고 실패율이 오르면 개선이 아니다.

## 연결 개념
- DevOps: 개발과 운영을 연결해 소프트웨어 전달 흐름을 개선하는 문화·프로세스
- CI/CD: 변경 리드타임과 배포 빈도를 좌우하는 자동화 체계
- SRE: MTTR, SLO, error budget으로 운영 신뢰성을 관리하는 방식

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: DORA 답안은 4대 지표 이름보다 납기 속도와 운영 리스크를 동시에 측정하고 추세로 개선 여부를 판단하는 구조가 필요하다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DORA Metrics는 deployment frequency, lead time for changes, change failure rate, MTTR로 소프트웨어 전달 성과를 측정하는 지표 체계이다.
> 2. **가치**: 개발 속도와 운영 복구를 함께 측정해 DevOps 개선이 고객 가치 전달로 이어지는지 검증한다.
> 3. **판단 포인트**: 절대 등급보다 팀별 기준선, 4주 이동 평균, 변경 실패율·MTTR 동시 추세가 핵심 판단 기준이다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| DevOps 성과 지표 이해 확인 | 4대 지표 명칭과 측정 기점 | 배포 빈도만 강조 |
| 속도와 신뢰성 균형 판단 | lead time, failure rate, MTTR trade-off | Elite 등급 암기 중심 답안 |
| 개선 방안 제시 역량 확인 | CI/CD, test automation, canary, rollback | 지표 수집 도구만 나열 |

> 요약: DORA 문제는 4대 지표를 납기·품질·복구 의사결정에 연결하는 답안이어야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: DevOps 전달 성과 측정 지표
- 배경: 기능 개발량만으로는 고객 가치 전달 속도와 운영 장애 위험을 판단할 수 없어, 개발·배포·복구 과정을 같은 기준으로 측정해야 함.
- 필요성: 배포 빈도, 변경 리드타임, 변경 실패율, MTTR 4개 지표로 delivery speed와 service recovery를 함께 관리해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Code Commit -> CI Build/Test -> Deploy -> Production Change
            -> Incident/Rollback -> Recovery
            +-> DF / LTC / CFR / MTTR Metrics
```

| 구성요소 | 역할 | 측정 기준 |
|:---|:---|:---|
| Deployment Frequency | 운영 배포 빈도 측정 | 일/주/월 배포 횟수 |
| Lead Time for Changes | 커밋부터 운영 반영까지 시간 | commit timestamp -> deploy timestamp |
| Change Failure Rate | 장애·롤백 유발 변경 비율 | failed deployment / total deployment |
| MTTR | 장애 탐지 후 복구까지 시간 | incident start -> service restore |

> 요약: DORA는 배포 흐름의 시작, 운영 반영, 실패, 복구 지점을 4개 지표로 연결한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Git Event 수집 -> CI/CD 로그 수집 -> 배포 성공/실패 분류
-> Incident 로그 연결 -> 4대 지표 계산 -> 추세 분석 -> 개선 backlog 반영
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 커밋·빌드·배포 이벤트 수집 | timestamp 누락 0건 |
| 2 | 운영 배포와 변경 단위 매핑 | release ID, commit SHA 연결 |
| 3 | 장애·롤백·hotfix를 실패 변경으로 분류 | CFR 산식 표준화 |
| 4 | incident 복구 시간 계산 | MTTR 30분 이하 목표 |
| 5 | 4주 이동 평균으로 개선 추세 판단 | 지표 급등락 원인 기록 |

> 요약: DORA는 도구 로그를 연결해 배포와 장애 사건을 같은 변경 단위로 계산해야 한다.

---

## Ⅳ. 특징

| 구분 | 전통적 개발 KPI | DORA Metrics | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 속도 | 투입 인력, 완료 기능 수 | deployment frequency, lead time | 주 1회 이상 배포 추세 |
| 품질 | 테스트 결함 수 | change failure rate | 15% 이하 목표 |
| 복구 | 장애 건수 | MTTR | 30분 이하 목표 |
| 개선 방식 | 프로젝트 종료 회고 | 지속 측정과 병목 제거 | 4주 이동 평균 비교 |

> 요약: DORA는 활동량이 아니라 변경이 운영에 도달하고 복구되는 실제 흐름을 측정한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 단일 지표 관리 | DORA 통합 관리 | 선택 기준 |
|:---|:---|:---|:---|
| 배포 속도 | 배포 횟수만 측정 | DF와 CFR 동시 측정 | 배포 증가 시 실패율 유지 필요 |
| 납기 | 프로젝트 일정 중심 | 커밋-운영 lead time | 제품팀 flow 측정 필요 |
| 운영 | 장애 건수 중심 | MTTR과 rollback 연결 | SRE·DevOps 조직에 적합 |

> 요약: DORA는 속도 지표와 실패·복구 지표를 함께 해석할 때 의미가 있다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 지표 왜곡 | 배포 단위 쪼개기 | 변경 단위 기준과 release ID 표준화 | metric audit count |
| 실패 은폐 | 장애 분류 기준 불명확 | rollback, hotfix, incident를 CFR에 포함 | postmortem 누락률 |
| 속도 편향 | DF만 목표화 | CFR·MTTR guardrail 설정 | CFR 15% 이하, MTTR 30분 이하 |

> 요약: DORA 운영 리스크는 산식 표준화와 guardrail 없이는 지표 게임으로 전환될 수 있다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 전달 속도 | lead time 1일 이하 추세 | Git, CI/CD, deployment log |
| 변경 품질 | change failure rate 15% 이하 | incident, rollback, hotfix log |
| 복구 | MTTR 30분 이하 | APM, alert, incident timeline |

> 요약: DORA 성과는 팀별 기준선 대비 lead time 감소와 CFR·MTTR 유지 여부로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. Git commit SHA, CI build ID, deployment ID, incident ID를 연결해 변경 단위별 추적성을 구성
2. CI/CD에 자동 테스트, canary, feature flag, rollback 자동화를 적용해 CFR 15% 이하와 MTTR 30분 이하 유지
3. 4주 이동 평균 dashboard로 DF, LTC, CFR, MTTR을 함께 보고 병목을 backlog 개선 항목으로 전환

**결론 (2줄):**
- 기술사 판단: DevOps 성숙도는 배포 빈도 단독이 아니라 lead time, change failure rate, MTTR 균형으로 판단함
- 향후 방향: DORA는 SRE SLO, value stream, platform engineering 지표와 결합되어 조직 전달 성과의 공통 언어로 확장됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "DORA Metrics를 설명하시오" | 4대 지표 산식과 수집 흐름 | 전통 KPI 대비 차이 |
| 요구사항 명시형 | "DevOps 개선 방안을 제시하시오", "운영 지표를 설계하시오" | 로그 연결과 추세 분석 | guardrail, CFR·MTTR 통제 |

> 요약: 설명형은 지표 체계, 방안형은 수집 구조와 개선 backlog 연결 중심으로 목차를 구성한다.
