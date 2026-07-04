---
title: "기술부채 측정·관리 (Technical Debt Measurement)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 279
---

# 📖 【암기용】 개념 완전 이해

> 목적: 기술부채를 처음 보는 사람도, 부채의 은유가 왜 성립하는지부터 측정 지표 계산까지 완전히 이해하게 만든다.

## 한눈에
- **개요**: 기술부채(Technical Debt)는 **소프트웨어 품질 관리** 관점에서, 지금 당장은 동작하지만 설계·코드·테스트를 타협해 얻은 대가로 **향후 변경 비용이 계속 늘어나는 구조적 부담**을 금융 부채에 비유한 개념이다.
- **왜 필요한가**: 부채를 측정하지 않으면 "느낌상 코드가 지저분하다"는 감(感)에만 의존하게 되어 상환 우선순위를 정할 수 없고, 신규 기능 개발 속도와 장애 복구·보안 패치 속도가 함께 떨어진다.
- **핵심 직관**: 신용카드로 급하게 결제(=빠른 납기)하면 당장은 편하지만, 갚지 않으면 매달 이자(=유지보수 비용 증가)가 붙는다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 기술부채(Technical Debt) | 단기 타협이 향후 변경 비용을 늘리는 구조적 부담(Ward Cunningham, 1992) | 신용카드로 당겨쓴 돈 |
| 원금(Principal) | 지금 아낀 설계·테스트 작업량 그 자체 | 빌린 원금 |
| 이자(Interest) | 부채를 갚지 않고 방치할 때 매 변경마다 추가로 드는 비용 | 매달 붙는 카드 이자 |
| 부채 4분면(Technical Debt Quadrant) | 의도적/무의식적 × 신중함/무모함으로 나눈 부채 발생 유형 분류(Martin Fowler) | 빚을 진 이유를 4가지로 나눈 표 |
| Technical Debt Ratio | 부채 상환 예상 시간 ÷ 전체 개발 예상 시간 × 100(SonarQube SQALE 모델) | 소득 대비 빚 비율(DTI) |
| CVSS | 보안 취약점 심각도를 0~10으로 점수화한 지표 | 연체 이자율 |
| WSJF | (Cost of Delay) ÷ (Job Size) — 지연 비용 대비 작업 크기로 상환 우선순위 산정 | 빚 중 무엇부터 갚을지 정하는 공식 |

## 깊이 이해

### 왜 '부채'라는 은유를 쓰는가 (배경)
- 1992년 Ward Cunningham이 처음 사용한 은유다. "지금 완벽하지 않은 코드를 내보내는 것 자체는 문제가 아니다. 문제는 그 부채를 갚지 않고 계속 쌓아두는 것이다"라는 취지로, 단기 타협(원금)에는 반드시 이자가 붙는다는 점을 강조하기 위한 표현이다.

### 부채 4분면으로 유형 구분하기
- 신중+의도적(Prudent & Deliberate): "지금은 이 방식으로 가고, 출시 후에 정리하자" — 계획된 타협.
- 무모+의도적(Reckless & Deliberate): "설계 원칙 몰라도 돼, 그냥 빨리 짜" — 알면서 무시.
- 신중+무의식적(Prudent & Inadvertent): 출시 후에야 "지금 보니 이 설계가 최선이 아니었다"를 깨달음 — 정상적인 학습 곡선.
- 무모+무의식적(Reckless & Inadvertent): "계층이 뭔지도 몰랐다" — 역량 부족이 원인. 이 유형은 리팩터링보다 교육이 먼저다.

### Technical Debt Ratio를 수치로 계산하기
- SonarQube SQALE 모델 공식: `부채비율 = 부채 상환 시간(remediation cost) ÷ 개발 비용(development cost) × 100`.
- 예: 정적분석에서 발견된 issue들을 모두 고치는 데 예상 400시간이 걸리고, 전체 코드베이스를 처음부터 다시 개발한다면 5,000시간이 걸린다고 추정되면 → 부채비율 = 400/5,000×100 = 8%.
- 등급 기준(SQALE): A(≤5%), B(5~10%), C(10~20%), D(20~50%), E(50%↑). 8%는 B등급으로, "신규 기능보다 부채 상환 스프린트를 배정해야 하는" 경계선에 해당한다.

### 상환 우선순위를 정하는 WSJF
- `WSJF = Cost of Delay ÷ Job Size`. 예: 결제 모듈 부채는 방치 시 매달 장애 대응 비용이 200만 원씩 늘어난다고 추정(Cost of Delay 크다)하고, 상환에 필요한 작업량이 5인일(Job Size 작다)이면 WSJF 값이 커져 최우선 상환 대상이 된다. 반대로 관리자 화면 하나만 쓰는 legacy 모듈은 Cost of Delay가 작아 뒤로 밀린다.
- 실무 판정 예: duplicated lines 12%, coverage 45%, CVE high 3건이 함께 나오면 코드 품질(중복·커버리지)뿐 아니라 보안 위험(CVE)까지 겹친 상태이므로, 다음 스프린트 capacity의 15~20%를 부채 상환에 강제 배정한다.

### 흔한 오해
- 기술부채는 "나쁜 코드"만을 뜻하지 않는다. 의도적으로 선택한 단기 설계(신중+의도적 사분면)도 상환 계획이 없으면 결국 부채로 남는다.
- "리팩터링만 하면 부채가 사라진다"는 것도 오해다. 코드 부채는 리팩터링으로, 테스트 부채는 자동화로, 보안·의존성 부채는 업그레이드/패치로 — 유형마다 상환 수단이 다르다.

## 연결 개념
- 리팩터링(278편) — 코드 부채를 상환하는 대표 실행 방법
- 품질 메트릭 — Cyclomatic Complexity·Duplication·Coverage로 부채를 정량화하는 도구
- DevOps DORA 지표 — 변경 리드타임·변경 실패율로 부채가 실제 배포 속도에 미치는 영향을 확인

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

- 개요: 기술부채는 단기 선택이 향후 변경 비용을 키우는 상태다.
- 배경: 코드·설계·테스트·의존성·운영 자동화 부채가 누적되면 배포 리드타임과 장애 복구 시간이 증가한다.
- 필요성: 복잡도, 중복률, 테스트 커버리지, 변경 실패율 같은 지표로 부채 상환 우선순위를 정해야 한다.

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

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
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
