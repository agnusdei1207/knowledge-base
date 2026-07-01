---
title: "Cloud Migration 6R (Cloud Migration 6R)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 287
---

# 📖 【암기용】 개념 완전 이해

> 목적: Cloud Migration 6R을 모든 시스템을 한 방식으로 옮기는 것이 아니라 업무 가치·기술 부채·위험에 따라 이전 전략을 나누는 분류 체계로 이해하게 만든다.

## 한눈에
- **개요**: 클라우드 이전 대상을 Retain, Retire, Rehost, Replatform, Repurchase, Refactor로 분류하는 마이그레이션 전략
- **왜 필요한가**: 레거시 시스템은 중요도, 구조, 비용, 규제, 수명주기가 달라 같은 이전 방식으로 처리하면 비용과 위험이 커진다.
- **핵심 직관**: 이사를 할 때 모든 물건을 그대로 옮기지 않고 버릴 것, 보관할 것, 새로 살 것, 고쳐 쓸 것을 나누는 방식이다.

## 깊이 이해
- **배경·문제의식**: 클라우드 이전은 데이터센터 종료 일정만 보고 밀어붙이면 기술 부채와 운영 리스크를 클라우드로 그대로 옮긴다.
- **작동 원리**: 애플리케이션 포트폴리오를 평가해 유지, 폐기, 재호스팅, 일부 플랫폼 변경, SaaS 전환, 재설계를 선택한다.
- **비유**: 오래된 사무실 이전에서 중요 문서는 새 금고로, 불필요한 장비는 폐기, 표준 소프트웨어는 구독형으로 바꾸는 것과 같다.
- **구체 예시**: 단순 VM 업무는 Rehost, DB 버전만 managed service로 바꾸면 Replatform, 패키지 회계 시스템은 SaaS Repurchase, 핵심 고객 앱은 Refactor를 검토한다.
- **흔한 오해·주의점**: 6R은 성숙도 순위가 아니다. 일정이 급하면 Rehost 후 현대화가 맞을 수 있고, 규제 시스템은 Retain이 합리적일 수 있다.

## 연결 개념
- Cloud Adoption Framework — 마이그레이션 거버넌스와 운영 전환
- FinOps — 이전 후 비용과 사용량 관리
- Multi Cloud — 이전 대상 cloud 선택과 의존성 판단

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: Cloud Migration 6R은 전략 이름 암기가 아니라 애플리케이션별 비용·위험·현대화 수준을 결정하는 포트폴리오 판단 도구다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Cloud Migration 6R은 애플리케이션별 이전 여부와 이전 방식을 6가지 전략으로 분류하는 의사결정 프레임워크임.
> 2. **가치**: 데이터센터 이전, 비용 절감, 기술 부채 개선, SaaS 전환, 규제 대응을 동일 기준으로 비교하게 함.
> 3. **판단 포인트**: 업무 가치, 기술 적합성, 의존성, 데이터, 규제, 일정, 비용을 함께 평가해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 마이그레이션 전략 이해 확인 | 6R 의미와 선택 기준 | 모든 시스템 Rehost로 단순화 |
| 포트폴리오 판단 확인 | 업무 중요도, 기술 부채, 규제 | 기술 관점만 설명 |
| 실행 리스크 확인 | 의존성, 데이터, cutover, rollback | 이전 후 운영·비용 누락 |

> 요약: 이 문제는 시스템별로 다른 이전 전략을 선택하고 실행 리스크를 통제하는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 클라우드 이전 전략 6종
- 배경: 레거시 애플리케이션은 업무 가치와 기술 구조가 달라 단일 이전 방식으로는 비용·일정·장애 리스크가 커짐.
- 필요성: 6R로 포트폴리오를 분류해 이전 우선순위, 현대화 수준, cutover 방식을 결정해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Application Portfolio -> Assessment -> 6R Classification
6R -> Retain / Retire / Rehost / Replatform / Repurchase / Refactor
Strategy -> Migration Wave -> Test / Cutover / Operate
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Assessment | 업무·기술·비용·위험 평가 | dependency mapping |
| 6R Strategy | 애플리케이션별 이전 방식 선정 | 복수 전략 조합 가능 |
| Migration Wave | 이전 묶음과 순서 결정 | 업무 의존성 반영 |
| Operating Model | 이전 후 운영 기준 | monitoring, cost, security |

> 요약: 6R은 포트폴리오 평가 결과를 이전 전략과 wave 계획으로 연결한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
자산 식별 -> 업무 중요도 평가 -> 기술 적합성 평가
-> 의존성 / 데이터 / 규제 확인 -> 6R 전략 선택
-> wave 계획 -> migration 실행 -> 검증 / 운영 전환
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 애플리케이션, DB, 인터페이스 자산 목록화 | CMDB completeness |
| 2 | 업무 가치와 수명주기 평가 | business owner 승인 |
| 3 | 기술 적합성과 의존성 분석 | dependency map |
| 4 | 6R 선택 후 wave, test, rollback 계획 수립 | migration readiness |

> 요약: 6R은 자산 식별, 평가, 전략 선택, wave 실행의 순서로 동작한다.

---

## Ⅳ. 특징

| 전략 | 의미 | 선택 기준 |
|:---|:---|:---|
| Retain | 현 위치 유지 | 규제, 수명 종료 전, 이전 비용 과다 |
| Retire | 폐기 | 사용량 없음, 중복 기능 |
| Rehost | VM 단위 이전 | 일정 우선, 변경 최소 |
| Replatform | 일부 플랫폼 변경 | managed DB, runtime 변경 |
| Repurchase | SaaS 등으로 교체 | 표준 업무, 패키지 대체 가능 |
| Refactor | 아키텍처 재설계 | 핵심 업무, 확장·변경 요구 |

> 요약: 6R 전략은 우열이 아니라 업무 가치와 변경 허용 범위에 따른 선택지다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | Rehost | Replatform | Refactor |
|:---|:---|:---|:---|
| 변경 범위 | 인프라 중심 | 일부 runtime·관리형 서비스 | 애플리케이션 구조 변경 |
| 일정 | 짧은 이전 wave에 적합 | 중간 | 장기 현대화 |
| 위험 | 기술 부채 유지 | 호환성 검증 필요 | 일정·비용 변동 큼 |

> 요약: 이전 일정이 우선이면 Rehost, 운영 개선이 필요하면 Replatform, 핵심 서비스 현대화가 필요하면 Refactor를 검토한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 의존성 누락 | 인터페이스·배치 미식별 | dependency discovery | failed interface count |
| 비용 역전 | lift-and-shift 후 과다 리소스 | rightsizing, FinOps | cloud spend variance |
| 전환 장애 | data sync·DNS 전환 오류 | rehearsal, rollback plan | cutover defect count |

> 요약: 마이그레이션 리스크는 의존성, 비용, cutover에서 발생하므로 사전 discovery와 리허설이 필요하다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 준비도 | wave별 readiness 승인 | checklist |
| 이전 품질 | migration defect 목표 이내 | test report |
| 운영 전환 | monitoring, backup, access 구성 완료 | runbook review |

> 요약: 6R 실행 성과는 준비도, 결함, 운영 전환 완료 여부로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 애플리케이션 포트폴리오를 업무 중요도, 기술 부채, 의존성, 데이터 민감도, 비용 기준으로 평가함.
2. 각 애플리케이션에 6R 전략과 target landing zone, migration wave, rollback 기준을 매핑함.
3. 이전 후 rightsizing, backup, DR, observability, 보안 접근통제를 완료하고 FinOps review로 비용을 검증함.

**결론 (2줄):**
- 기술사 판단: 6R은 전면 현대화가 아니라 시스템별 위험과 가치에 맞는 이전 전략을 선택하는 포트폴리오 도구임.
- 향후 방향: Cloud Migration은 AI assessment, automated discovery, hybrid/multi cloud landing zone과 결합되어 지속 현대화 방식으로 전환됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Cloud Migration 6R을 설명하시오" | 평가에서 전략 선택까지 흐름 | 6R 전략별 선택 기준 |
| 요구사항 명시형 | "클라우드 전환 방안을 제시하시오" | 포트폴리오 평가와 wave 실행 절차 | 의존성, 비용, cutover 리스크 |

> 요약: 설명형은 6R 분류, 방안형은 평가·wave·운영 전환 계획을 중심으로 작성한다.
