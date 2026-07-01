---
title: "기술부채 측정·관리 (Technical Debt Measurement)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 279
---

# 📖 【암기용】 개념 완전 이해

> 목적: 기술부채를 빠른 납기나 누적 변경으로 생긴 구조적 비용이며 측정·상환해야 하는 관리 대상으로 이해하게 만든다.

## 한눈에
- **개요**: 기술부채는 지금은 동작하지만 향후 변경 비용과 결함 가능성을 증가시키는 설계·코드·테스트·운영 결함이다.
- **왜 필요한가**: 부채를 방치하면 신규 기능 개발 시간이 늘고 장애 복구와 보안 패치 속도가 떨어진다.
- **핵심 직관**: 급하게 만든 임시 도로를 계속 쓰면 유지비와 사고 비용이 누적되므로 보수 계획이 필요하다.

## 깊이 이해
- **배경·문제의식**: 일정 압박으로 중복 코드, 낮은 테스트, 오래된 라이브러리, 수동 배포가 생긴다. 처음에는 납기를 줄이지만 시간이 지나면 변경 리드타임을 늘린다.
- **작동 원리**: static analysis, defect trend, change failure rate, dependency risk를 측정해 부채 항목을 backlog로 등록하고 우선순위에 따라 상환한다.
- **비유**: 신용카드 결제처럼 단기 편의는 얻지만 이자가 붙어 다음 달 비용이 증가한다.
- **구체 예시**: SonarQube technical debt ratio 8%, duplicated lines 12%, coverage 45%, CVE high 3건이면 신규 기능보다 부채 상환 스프린트를 배정해야 한다.
- **흔한 오해·주의점**: 기술부채는 나쁜 코드만 의미하지 않는다. 의식적으로 선택한 단기 설계도 상환 계획이 없으면 부채가 된다.

## 연결 개념
- 리팩터링 — 부채 상환의 대표 실행 방법
- 품질 메트릭 — 복잡도, 중복, 커버리지, 결함 추세
- DevOps DORA 지표 — 리드타임과 변경 실패율 연결

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 기술부채를 측정 지표, 우선순위, 상환 전략, 거버넌스 체계로 답안화한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 기술부채는 단기 납기·설계 타협·운영 누적으로 향후 변경 비용을 증가시키는 구조적 부담이다.
> 2. **가치**: 부채를 측정 가능한 backlog로 전환해야 개발 리드타임, 결함률, 보안 위험을 통제할 수 있다.
> 3. **판단 포인트**: 코드 품질 지표만이 아니라 business impact, 변경 빈도, 장애 이력, CVE 등 우선순위 축을 함께 봐야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| SW 품질관리 역량 확인 | debt type, measurement, repayment | 기술부채를 단순 코드 냄새로 축소 |
| 정량 관리 확인 | complexity, duplication, coverage, lead time | "관리 필요" 같은 정성 문장만 제시 |
| 거버넌스 판단 확인 | debt backlog, quality gate, architecture review | 리팩터링만 제시하고 우선순위 누락 |

> 요약: 기술부채 답안은 측정, 우선순위, 상환, 재발 방지의 관리 루프를 보여야 한다.

---

## Ⅰ. 개요 및 필요성

기술부채는 단기 개발 선택이 향후 변경 비용을 증가시키는 상태다. 코드·설계·테스트·의존성·운영 자동화 부채가 누적되면 배포 리드타임과 장애 복구 시간이 증가하므로 측정 기반 관리가 필요하다.

---

## Ⅱ. 구조 및 구성요소

```text
Source/Architecture/Operation -> Debt Detection
  -> Metric Scoring -> Debt Backlog -> Prioritization
  -> Repayment Sprint -> Quality Gate
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Debt Inventory | 부채 항목 등록 | 코드, 테스트, 보안, 운영 |
| Metric Model | 정량 점수화 | complexity, duplication, CVE |
| Prioritization | 상환 순서 결정 | risk, change frequency, business impact |
| Governance | 재발 방지 | quality gate, ADR, review |

> 요약: 기술부채 관리는 탐지, 점수화, backlog화, 상환, 게이트 통제로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
정적 분석/운영 지표 수집 -> 부채 항목 생성
  -> 영향도·긴급도 점수화 -> 상환 계획 수립
  -> 리팩터링/자동화/업그레이드 -> 품질 게이트 검증
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 코드·테스트·운영 지표 수집 | scan coverage 100% |
| 2 | 부채 유형과 원인 분류 | code/design/test/security |
| 3 | 우선순위와 상환 일정 결정 | WSJF, risk score |
| 4 | 상환 후 품질 게이트 적용 | debt ratio, lead time 개선 |

> 요약: 부채는 발견 즉시 작업화하고, 상환 후 게이트를 통해 재유입을 차단한다.

---

## Ⅳ. 특징

| 구분 | 미관리 부채 | 측정·관리 부채 | 정량·기술 포인트 |
|:---|:---|:---|:---|
| 가시성 | 개인 인식 의존 | debt backlog | owner, due date |
| 우선순위 | 큰 목소리 기준 | risk·cost 점수 | WSJF, CVSS |
| 실행 | 임시 리팩터링 | sprint allocation | capacity 10~20% |
| 검증 | 완료 선언 | quality gate | coverage, duplication |

> 요약: 기술부채는 backlog와 품질 게이트로 전환할 때 관리 대상이 된다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 코드 부채 | 긴 메서드·중복 | 리팩터링 | complexity 15 초과, duplication 5% 초과 |
| 테스트 부채 | 회귀 테스트 부족 | test automation | change failure rate 15% 초과 |
| 보안·의존성 부채 | EOL·CVE | upgrade, patch | CVSS 7.0 이상 |

> 요약: 부채 유형별로 코드 지표, 장애 지표, CVE 점수를 달리 적용해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 상환 지연 | 기능 일정 우선 | capacity reserve 15%, debt SLA | overdue debt count |
| 재발 | 품질 게이트 부재 | CI gate, architecture review | new debt ratio |
| 과잉 개선 | 업무 영향 낮은 영역 개선 | change frequency 기반 선정 | value delivered per sprint |

> 요약: 부채 관리는 미상환, 재발, 과잉 개선을 모두 통제해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 코드 품질 | debt ratio 5% 이하, duplication 3% 이하 | SonarQube |
| 납기 영향 | lead time 20% 단축 | DORA metric |
| 운영 위험 | high CVE 0건, MTTR 30분 이하 | SCA, incident report |

> 요약: 성공 여부는 debt ratio, lead time, high CVE와 MTTR로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. SonarQube, SCA, CI 지표로 complexity, duplication, coverage, CVE를 매일 수집하고 debt backlog에 owner를 지정함.
2. 변경 빈도와 장애 이력이 높은 모듈을 우선으로 스프린트 capacity 15%를 부채 상환에 배정함.
3. 신규 부채 유입 방지를 위해 coverage 80%, high CVE 0건, duplication 3% 이하 quality gate를 merge 조건으로 설정함.

**결론 (2줄):**
- 기술사 판단: 기술부채는 제거 대상 전체가 아니라 위험·변경 빈도·업무 영향 기준으로 상환 순서를 정하는 관리 대상임.
- 향후 방향: platform engineering, automated quality gate, AI static analysis가 결합되어 부채 탐지와 상환 계획이 자동화됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "기술부채를 설명하시오" | 탐지·점수화·상환 흐름 | 부채 유형과 관리 특징 |
| 요구사항 명시형 | "측정 방안을 제시하시오", "관리 방안을 제시하시오" | 지표 수집과 우선순위 산정 | quality gate, capacity, 리스크 대응 |

> 요약: 설명형은 개념과 관리 루프, 방안형은 정량 지표와 실행 거버넌스 중심으로 전환한다.
