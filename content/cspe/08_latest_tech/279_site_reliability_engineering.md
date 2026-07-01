---
title: "사이트 신뢰성 공학 (Site Reliability Engineering)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 279
---

# 📖 【암기용】 개념 완전 이해

> 목적: SRE를 운영팀 이름이 아니라 소프트웨어 공학으로 서비스 신뢰성을 목표·지표·자동화·오류 예산으로 관리하는 방식으로 이해하게 만든다.

## 한눈에
- **개요**: SLO와 error budget을 기준으로 서비스 신뢰성, 배포 속도, 운영 자동화를 균형 있게 관리하는 공학적 운영 체계
- **왜 필요한가**: 기능 배포만 앞세우면 장애가 늘고, 가용성 100% 목표로 운영하면 배포가 멈춘다.
- **핵심 직관**: 도로 제한속도처럼 SLO는 허용 가능한 위험 수준을 정하고, error budget은 그 범위 안에서 배포와 개선을 조정한다.

## 깊이 이해
- **배경·문제의식**: 전통 운영은 장애 대응과 수작업 처리에 치우쳐 개발 속도와 운영 품질이 분리되기 쉬웠다.
- **작동 원리**: 사용자 관점 SLI를 정하고 SLO를 설정한 뒤 error budget 소진율에 따라 배포, 개선 작업, 장애 대응 우선순위를 조정한다.
- **비유**: 항공사는 모든 지연을 0으로 만들 수 없지만 정시 운항 목표와 지연 허용치를 정해 운항·정비·스케줄을 조정한다.
- **구체 예시**: API availability SLO 99.9%는 4주 1,000,000건 요청 기준 1,000건 오류 예산을 의미하며, 예산 소진 시 신규 배포보다 안정화 작업을 우선한다.
- **흔한 오해·주의점**: SRE는 24시간 장애 대응 인력 투입이 아니다. 반복 운영을 자동화하고 서비스 수준 목표를 제품 의사결정에 연결하는 역할이다.

## 연결 개념
- SLO — 사용자 영향 기준의 목표
- Error Budget — 신뢰성 목표와 배포 속도 균형 장치
- Observability — SLI 측정과 원인 분석 데이터 기반

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: SRE는 운영 자동화 기법이 아니라 SLO와 error budget을 통해 제품 위험을 계량화하는 운영 모델이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SRE는 소프트웨어 공학 원칙으로 서비스 신뢰성을 SLI, SLO, error budget, 자동화로 관리하는 체계임.
> 2. **가치**: 장애 대응, 배포 정책, 용량 관리, toil 제거를 사용자 영향 지표에 연결함.
> 3. **판단 포인트**: SLO 수준, error budget 정책, toil 비율, incident review, 관측성 품질이 성패를 좌우함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| SRE 개념 이해 확인 | SLI, SLO, error budget, toil | 운영팀 명칭으로 축소 |
| 운영 의사결정 확인 | budget burn 기반 배포 통제 | 가용성 100% 목표로 서술 |
| 실무 적용 판단 확인 | observability, incident, automation | 장애 대응 절차만 나열 |

> 요약: 이 문제는 신뢰성을 감정적 목표가 아니라 사용자 영향 기반 수치와 정책으로 운영하는 능력을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 신뢰성 공학 운영 체계
- 배경: 클라우드와 MSA는 배포 빈도와 장애 전파 경로가 늘어 수작업 운영만으로 신뢰성 목표를 유지하기 어려움.
- 필요성: SLI/SLO와 error budget을 기준으로 배포, 장애 대응, 자동화 투자 우선순위를 결정해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
User Journey -> SLI -> SLO -> Error Budget
Error Budget -> Release Policy / Reliability Work / Incident Review
Observability -> Alert -> Response -> Postmortem -> Automation
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| SLI | 사용자 관점 측정 지표 | latency, availability, correctness |
| SLO | 목표 서비스 수준 | 100% 목표 지양 |
| Error Budget | 허용 실패량 | 배포 정책과 연결 |
| Toil 관리 | 반복 수작업 제거 | 자동화 투자 기준 |

> 요약: SRE는 사용자 여정에서 SLI를 뽑고 SLO와 error budget으로 운영 의사결정을 통제한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
서비스 범위 정의 -> SLI 선정 -> SLO 설정 -> error budget 산정
-> burn rate 감시 -> 배포 허용 / 중단 판단
-> incident 대응 -> postmortem -> 자동화 backlog 반영
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 사용자 여정과 critical path 식별 | service catalog |
| 2 | SLI와 SLO 설정 | 사용자 영향 반영 여부 |
| 3 | error budget burn rate 측정 | budget remaining |
| 4 | 장애 후 postmortem과 toil 제거 수행 | action item completion |

> 요약: SRE는 목표 설정, 예산 소진 감시, 대응, 재발 방지 자동화로 반복되는 폐루프 운영을 수행한다.

---

## Ⅳ. 특징

| 구분 | 전통 운영 | SRE | 판단 기준 |
|:---|:---|:---|:---|
| 목표 | 시스템 정상 여부 | 사용자 경험 기반 SLO | user journey |
| 장애 판단 | 임계치 alert | error budget burn | 사용자 영향 |
| 업무 방식 | 수작업 처리 | 자동화와 toil 제거 | 반복 작업 비율 |
| 배포 정책 | 승인 중심 | budget 기반 허용·중단 | 위험 수용 범위 |

> 요약: SRE는 운영의 초점을 인프라 정상 상태에서 사용자 영향과 오류 예산 기반 의사결정으로 이동시킨다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | DevOps | SRE | 선택 기준 |
|:---|:---|:---|:---|
| 중심 개념 | 개발·운영 협업 | SLO 기반 신뢰성 공학 | 대규모 서비스 운영 |
| 지표 | 배포 빈도, lead time | SLI, error budget, toil | 사용자 영향 측정 필요 |
| 정책 | 팀 문화와 자동화 | 예산 소진에 따른 release gate | 장애와 배포 균형 |

> 요약: DevOps가 협업 원칙이면 SRE는 SLO와 error budget으로 운영 의사결정을 계량화한 실행 모델이다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| SLO 오설정 | 내부 metric 중심 | 사용자 여정 기반 SLI 선정 | customer-impact incidents |
| 알림 피로 | 증상 없는 alert 과다 | burn rate alert 적용 | actionable alert ratio |
| Toil 누적 | 반복 수작업 방치 | 자동화 backlog와 sprint 반영 | toil percentage |

> 요약: SRE 리스크는 목표 설정 오류, 알림 품질, toil 누적에서 발생하며 SLO와 자동화 지표로 관리한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 신뢰성 | SLO 준수와 budget 잔여율 | SLO dashboard |
| 대응 | MTTA·MTTR 목표 이내 | incident record |
| 운영 부담 | toil 비율 50% 이하 목표 | 업무 분류 기록 |

> 요약: SRE 도입 효과는 SLO 준수, 대응 시간, toil 비율로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 핵심 사용자 여정별 SLI를 latency, availability, error rate로 정의하고 SLO 문서에 측정식과 제외 조건을 명시함.
2. error budget policy를 제품·개발·운영 조직이 합의하고 burn rate에 따라 배포 허용, freeze, 안정화 작업 전환 기준을 둠.
3. postmortem을 blame-free 형식으로 수행하고 반복 장애 action item을 자동화 backlog와 운영 runbook에 반영함.

**결론 (2줄):**
- 기술사 판단: 서비스 규모와 배포 빈도가 증가하면 SRE를 도입해 신뢰성 목표와 변경 속도를 같은 지표 체계로 관리해야 함.
- 향후 방향: SRE는 AIOps, platform engineering, progressive delivery와 결합되어 정책 기반 자동 복구 체계로 발전함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "SRE를 설명하시오" | SLI, SLO, error budget 운영 흐름 | 전통 운영 대비 차이 |
| 요구사항 명시형 | "서비스 신뢰성 확보 방안을 제시하시오" | budget burn 기반 배포·대응 절차 | toil, alert fatigue, postmortem |

> 요약: 설명형은 SRE 구성 체계를, 방안형은 SLO 정책과 자동화 실행을 중심으로 작성한다.
