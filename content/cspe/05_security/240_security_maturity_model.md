---
title: "보안 성숙도 모델 (Security Maturity Model)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 240
---

# 📖 【암기용】 개념 완전 이해

> 목적: 보안 성숙도 모델을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 조직 보안 역량의 현재 수준과 목표 수준을 단계로 평가하고 개선 로드맵을 만드는 체계
- **왜 필요한가**: 보안 투자는 장비 구매만으로 끝나지 않는다. 정책, 프로세스, 인력, 자동화, 측정 지표가 어느 단계인지 알아야 예산과 개선 순서를 정할 수 있다.
- **핵심 직관**: 건강검진처럼 보안 조직의 현재 체력 수치를 측정하고, 목표 체력까지 필요한 훈련 계획을 세우는 방법이다.

## 깊이 이해
- **배경·문제의식**: 기업은 NIST CSF, ISO 27001, CMMI, OWASP SAMM, BSIMM 같은 기준을 동시에 요구받는다. 그러나 점검 항목을 나열하면 실행 우선순위가 흐려지므로 maturity level과 current-target gap이 필요하다.
- **작동 원리**: 영역(Identify, Protect, Detect, Respond, Recover 또는 Governance, Design, Implementation, Verification, Operations)을 정하고 현재 수준을 1~5단계로 평가한다. 목표 수준과 차이를 계산해 로드맵, 예산, 책임자, 측정 지표를 만든다.
- **비유**: 학생에게 모든 과목을 한 번에 만점으로 만들라고 하지 않고, 현재 점수와 목표 점수 차이가 큰 과목부터 학습 계획을 세우는 것과 같다.
- **구체 예시**: 애플리케이션 보안에서 SAMM 기준 Governance 2, Design 1, Implementation 2, Verification 1이면 위협 모델링과 SAST 자동화를 6개월 우선 과제로 둔다.
- **흔한 오해·주의점**: 성숙도 점수는 인증서가 아니다. 점수가 높아도 실제 사고 탐지·복구 지표가 낮으면 운영 통제가 실패한 상태이다.

## 연결 개념
- NIST CSF — Identify, Protect, Detect, Respond, Recover 기반 보안 기능 프레임워크
- OWASP SAMM·BSIMM — 애플리케이션 보안 프로그램 성숙도 평가 모델
- Metric Governance — 성숙도 개선을 지표와 책임 체계로 관리하는 방식

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 성숙도 모델은 점수 산정이 아니라 현재-목표 차이를 로드맵, 예산, 지표 거버넌스로 전환하는 관리 체계이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 보안 성숙도 모델은 조직의 보안 역량을 단계별 수준으로 평가하고 current-target gap을 개선 로드맵으로 전환하는 체계이다.
> 2. **가치**: NIST CSF, CMMI, OWASP SAMM, BSIMM 기준으로 정책·프로세스·기술·지표 우선순위를 정한다.
> 3. **판단 포인트**: 점수 자체보다 목표 수준, 위험 허용도, 투자 우선순위, metric governance가 실행 성과를 결정한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 보안 거버넌스 평가 역량 확인 | maturity levels, current-target gap, roadmap | 모델명만 나열하고 개선 계획 누락 |
| 프레임워크 선택 판단 확인 | NIST CSF, CMMI, SAMM, BSIMM 차이 | 하나의 모델을 모든 조직에 적용 |
| 지표 기반 운영 확인 | KPI/KRI, owner, budget, audit evidence | 점수 상승을 보안 효과로 단정 |

> 요약: 이 문제는 보안 수준 평가를 실행 가능한 로드맵과 지표 거버넌스로 연결하는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

보안 성숙도 모델은 보안 역량을 단계별 수준으로 평가하는 체계이다. 조직은 규제, 사고 대응, 클라우드 전환, 개발 보안 요구를 동시에 처리해야 한다. 성숙도 평가는 현재 수준과 목표 수준의 차이를 보여주고 투자 순서와 책임 구조를 정한다.

---

## Ⅱ. 구조 및 구성요소

```text
평가 범위 -> 기준 모델 선택 -> 현재 수준 평가
        -> 목표 수준 설정 -> gap 분석 -> roadmap
        -> KPI/KRI 측정 -> 개선 반복
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| 기준 모델 | 평가 영역과 수준 기준 제공 | NIST CSF, CMMI, SAMM, BSIMM |
| Maturity Level | 역량 단계를 1~5 수준으로 표현 | ad hoc, managed, defined, measured |
| Gap Analysis | 현재와 목표 차이 산정 | 위험 허용도·규제 요구 반영 |
| Roadmap | 개선 과제·예산·책임자 배치 | 3/6/12개월 단위 |
| Metric Governance | 지표, 증적, 감사 추적 | KPI, KRI, dashboard |

> 요약: 성숙도 모델은 기준 모델, 수준 평가, gap 분석, 로드맵, 지표 거버넌스로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
범위 확정 -> 모델 선정 -> 증적 수집 -> level 평가
        -> target level 결정 -> gap 우선순위화
        -> roadmap 실행 -> metric review
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 평가 범위와 조직 단위 확정 | 전사, 클라우드, AppSec, SOC |
| 2 | 프레임워크 선정과 항목 매핑 | NIST CSF, SAMM, BSIMM control |
| 3 | 인터뷰·증적·지표 기반 현재 수준 평가 | 정책, 로그, 티켓, 감사자료 |
| 4 | 목표 수준과 gap 우선순위 산정 | 규제, 사고 이력, 자산가치 |
| 5 | 로드맵 실행과 지표 검토 | KPI/KRI, budget, owner |

> 요약: 평가 흐름은 증거 기반 현재 수준을 산정하고 목표 수준과 차이를 과제·예산·지표로 전환한다.

---

## Ⅳ. 특징

| 구분 | 체크리스트 점검 | 보안 성숙도 모델 | 수치·기준 |
|:---|:---|:---|:---|
| 결과 | 항목별 준수 여부 | 단계 수준과 gap | Level 1~5 |
| 관점 | 단기 감사 대응 | 지속 개선·투자 계획 | 3/6/12개월 roadmap |
| 모델 | 단일 통제 목록 | NIST CSF, CMMI, SAMM, BSIMM | 기능·도메인별 선택 |
| 검증 | 문서 존재 확인 | 지표·증적·운영 결과 확인 | MTTD, MTTR, patch SLA |

> 요약: 성숙도 모델은 점검표보다 현재 수준, 목표 수준, 실행 로드맵을 함께 제시한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 모델 선택 | NIST CSF는 전사 보안 기능 | SAMM/BSIMM은 AppSec 프로그램 | 평가 범위가 전사인지 개발 보안인지 |
| 비용/성과 | 감사 대응은 단기 증적 중심 | 성숙도는 다년 로드맵 중심 | 예산·조직 변화까지 포함 |
| 운영/위험 | 점수 산정 후 종료 | metric governance로 반복 측정 | quarterly review 필요 |

> 요약: 전사 보안은 NIST CSF, 애플리케이션 보안은 SAMM·BSIMM을 우선 적용하고 지표로 반복 관리한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 점수 형식화 | 인터뷰 중심 평가 | 로그·티켓·감사증적 기반 검증 | evidence coverage 90% 이상 |
| 목표 과다 | 모든 영역 Level 5 지향 | 위험 기반 target level 설정 | budget 대비 완료율 |
| 지표 단절 | 과제와 KPI/KRI 미연결 | metric owner, dashboard, review cadence | quarterly review 100% |

> 요약: 성숙도 평가는 증거 기반, 목표 현실화, 지표 거버넌스가 없으면 점수 보고서로 끝난다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 평가 신뢰도 | 주요 항목 증적 90% 이상 | 정책, 로그, 티켓, 감사자료 샘플링 |
| 로드맵 이행 | 6개월 과제 완료율 80% 이상 | PMO, security program dashboard |
| 운영 성과 | MTTD 30분, MTTR 4시간, patch SLA 15일 | SIEM, SOAR, vulnerability platform |

> 요약: 도입 성과는 성숙도 점수보다 증적 커버리지, 로드맵 완료율, 탐지·복구·패치 지표로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 전사 보안은 NIST CSF 2.0 기준으로 Identify·Protect·Detect·Respond·Recover·Govern 영역을 평가함
2. 애플리케이션 보안은 OWASP SAMM 또는 BSIMM으로 Governance, Design, Implementation, Verification, Operations 수준을 산정함
3. current-target gap을 3/6/12개월 roadmap으로 만들고 KPI/KRI, owner, budget, audit evidence를 quarterly review에 연결함

**결론 (2줄):**
- 기술사 판단: 규제·감사 대응 조직은 NIST CSF, 제품 개발 조직은 SAMM·BSIMM을 선택하고 목표 수준은 위험 기반으로 정한다
- 향후 방향: 성숙도 평가는 GRC, SIEM, DevSecOps 지표를 연결한 continuous control monitoring으로 전환된다

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "보안 성숙도 모델을 설명하시오", "기술하시오" | 평가 범위, 모델 선정, gap 분석 흐름 | 체크리스트 점검과 차이 |
| 요구사항 명시형 | "도입 방안을 제시하시오", "비교하시오" | NIST CSF/SAMM/BSIMM 선택 기준 | roadmap, KPI/KRI, metric governance |

> 요약: 설명형은 평가 절차를, 요구사항형은 모델 선택·gap 로드맵·지표 거버넌스를 중심으로 답안을 전환한다.
