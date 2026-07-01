---
title: "소프트웨어 리팩터링 패턴 (Refactoring Patterns)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 278
---

# 📖 【암기용】 개념 완전 이해

> 목적: 리팩터링을 외부 동작을 보존하면서 내부 구조를 개선하는 체계적 변경으로 이해하게 만든다.

## 한눈에
- **개요**: 리팩터링은 기능 변경 없이 코드 구조, 중복, 의존성을 개선하는 활동이다.
- **왜 필요한가**: 기능 추가가 반복되면 중복, 긴 메서드, 순환 의존, 테스트 어려움이 누적되어 변경 비용이 증가한다.
- **핵심 직관**: 건물을 영업 중인 상태로 유지하면서 배관과 동선을 고치는 작업이다.

## 깊이 이해
- **배경·문제의식**: 요구사항 변화가 누적되면 코드가 최초 설계와 달라진다. 구조를 방치하면 작은 기능도 여러 파일을 건드려 결함 확률이 증가한다.
- **작동 원리**: 테스트로 기존 동작을 고정하고, 작은 단계로 extract method, move method, rename, introduce parameter object 같은 패턴을 적용한다.
- **비유**: 책 내용을 바꾸지 않고 목차, 문단, 색인을 정리해 다음 독자가 찾기 쉽게 만드는 것과 같다.
- **구체 예시**: 200줄 결제 메서드를 검증, 계산, 저장, 이벤트 발행 4개 메서드로 분리하고 단위 테스트 30개를 통과시킨다.
- **흔한 오해·주의점**: 리팩터링은 기능 개발과 섞으면 검증 범위가 커진다. 동작 보존 테스트 없이 구조 변경만 수행하면 회귀 결함을 만들 수 있다.

## 연결 개념
- 코드 스멜 — 리팩터링 대상 식별 신호
- 단위 테스트·회귀 테스트 — 동작 보존 안전망
- 기술부채 — 리팩터링 우선순위 판단 기준

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 리팩터링 패턴을 코드 스멜, 테스트 안전망, 단계적 개선, 지표 기반 관리로 답안화한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 리팩터링은 외부 관찰 동작을 유지하면서 내부 코드 구조를 개선하는 통제된 변경 활동이다.
> 2. **가치**: 중복, 결합도, 복잡도를 낮춰 변경 영향 범위와 회귀 결함을 줄인다.
> 3. **판단 포인트**: 패턴 이름보다 테스트 확보, 작은 커밋, complexity·duplication 지표, rollback 가능성이 핵심이다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| SW 유지보수 역량 확인 | behavior preservation, code smell, refactoring pattern | 기능 추가와 리팩터링 혼동 |
| 패턴 적용 판단 확인 | extract, move, inline, rename, parameter object | 패턴 목록만 나열하고 적용 조건 누락 |
| 품질 지표 연결 확인 | coverage, cyclomatic complexity, duplication | 정성 표현만 쓰고 수치 지표 누락 |

> 요약: 리팩터링 답안은 동작 보존과 구조 지표 개선을 동시에 제시해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 리팩터링은 기능 변경 없이 내부 설계를 개선하는 활동이다.
- 배경: 요구사항 누적은 코드 스멜과 기술부채를 만들며 이를 방치하면 결함 수정 시간과 배포 리스크가 증가한다.
- 필요성: 테스트 기반의 작은 구조 개선으로 중복, 긴 함수, 순환 의존 같은 코드 스멜을 제거해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Code Smell -> Test Safety Net -> Refactoring Pattern
  -> Small Commit -> Review/CI -> Metric Check
  -> Release/Rollback
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Code Smell | 개선 대상 신호 | long method, duplicate code |
| Safety Net | 기존 동작 보존 | unit/regression test |
| Refactoring Pattern | 구조 개선 절차 | extract method, move class |
| Quality Metric | 개선 여부 확인 | complexity, coverage, duplication |

> 요약: 리팩터링은 스멜 탐지, 테스트 고정, 패턴 적용, 지표 확인 순서로 수행한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
대상 코드 선정 -> 테스트 작성/보강 -> 작은 구조 변경
  -> 테스트 실행 -> 코드 리뷰 -> 지표 비교
  -> 통합 또는 rollback
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 스멜과 변경 빈도 기반 대상 선정 | churn, defect count |
| 2 | 동작 보존 테스트 확보 | coverage 80% 이상 |
| 3 | 패턴을 작은 단위로 적용 | commit당 변경 파일 제한 |
| 4 | CI·리뷰·지표 비교 | test pass 100%, complexity 감소 |

> 요약: 리팩터링은 테스트를 먼저 고정하고 작은 변경을 반복해 회귀 가능성을 낮춘다.

---

## Ⅳ. 특징

| 구분 | 임의 구조 변경 | 리팩터링 패턴 | 정량·기술 포인트 |
|:---|:---|:---|:---|
| 목적 | 기능·구조 혼합 | 외부 동작 보존 | behavior test 통과 |
| 절차 | 대규모 변경 | small step | commit size 300 LOC 이하 |
| 판단 | 개인 경험 | code smell 기반 | cyclomatic complexity |
| 검증 | 수동 확인 | CI·coverage·diff | mutation score 가능 |

> 요약: 리팩터링은 패턴화된 작은 변경과 자동 테스트로 구조 개선을 통제한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| Extract Method | 긴 메서드 유지 | 책임 단위 분리 | 50줄 이상·분기 10개 이상 |
| Move Class | 순환 의존 유지 | 응집도 높은 모듈 이동 | package cycle 검출 |
| Introduce Parameter Object | 인자 5개 이상 | 값 객체로 묶음 | API 변경 영향 관리 가능 |

> 요약: 패턴 선택은 코드 스멜의 형태와 변경 영향 범위에 맞춰야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 회귀 결함 | 테스트 부족 | characterization test, golden master | regression failure 0건 |
| 범위 확대 | 기능 변경 동시 수행 | refactoring-only PR | feature diff 0건 |
| 일정 지연 | 빅뱅 구조 변경 | strangler, branch by abstraction | PR lead time |

> 요약: 리팩터링 리스크는 테스트, PR 범위, 단계적 전환으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 복잡도 | cyclomatic complexity 15 이하 | SonarQube, lizard |
| 중복 | duplicated lines 3% 이하 | static analysis |
| 검증 | unit test pass 100%, coverage 80% 이상 | CI report |

> 요약: 리팩터링 효과는 복잡도, 중복률, 테스트 통과율로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 변경 빈도 상위 20% 파일과 결함 이력 파일을 우선 선정하고 characterization test로 현재 동작을 고정함.
2. extract method, move class, rename, parameter object를 PR당 1~2개 패턴으로 제한해 리뷰 가능 크기로 유지함.
3. SonarQube quality gate에 complexity, duplication, coverage 기준을 두고 기준 미달 시 merge를 차단함.

**결론 (2줄):**
- 기술사 판단: 리팩터링은 기능 개발 전후에 수행하되, 동작 보존 테스트 없는 구조 변경은 배포 대상에서 제외.
- 향후 방향: IDE 자동 리팩터링, static analysis, AI code review가 결합되어 지표 기반 지속 개선으로 정착함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "리팩터링 패턴을 설명하시오" | 스멜 탐지와 패턴 적용 흐름 | 주요 패턴과 효과 지표 |
| 요구사항 명시형 | "개선 방안을 제시하시오", "관리 방안을 제시하시오" | 테스트 안전망과 단계적 적용 | 회귀 리스크, 품질 게이트 |

> 요약: 설명형은 패턴 체계, 방안형은 테스트·지표·PR 통제 중심으로 전환한다.
