---
title: "소프트웨어 리팩터링 패턴 (Refactoring Patterns)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 278
---

# 📖 【암기용】 개념 완전 이해

> 목적: 리팩터링을 처음 보는 사람도, 코드 스멜부터 각 패턴의 적용 조건까지 완전히 이해하게 만든다. 시험 답안 양식이 아니라 이해를 위한 설명이다.

## 한눈에
- **개요**: 리팩터링은 **소프트웨어 유지보수** 활동 중 하나로, **외부에서 관찰되는 동작(behavior)을 그대로 유지**하면서 코드의 내부 구조·가독성·결합도를 개선하는 체계적 기법이다.
- **왜 필요한가**: 기능이 반복 추가되면 코드 스멜(긴 메서드, 중복, 순환 의존)이 쌓여 작은 변경도 여러 파일을 건드리게 되고, 결함 확률과 개발 리드타임이 늘어난다. 구조를 방치할수록 이후의 기술부채(279편)로 이어진다.
- **핵심 직관**: 영업 중인 건물에서 손님을 내보내지 않은 채(=기능은 그대로) 배관과 동선만 다시 까는 공사다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 리팩터링(Refactoring) | 외부 동작 보존 + 내부 구조 개선(Martin Fowler 정의) | 건물 영업 중 배관 재공사 |
| 코드 스멜(Code Smell) | 구조 개선이 필요하다는 신호가 되는 패턴 — 버그는 아니지만 방치하면 위험 | 몸에서 나는 이상 신호 |
| Extract Method | 긴 메서드의 일부를 의미 단위로 뽑아 별도 메서드로 분리 | 긴 문단을 소제목별로 나누기 |
| Move Method/Class | 책임이 맞지 않는 클래스의 메서드를 어울리는 클래스로 이동 | 엉뚱한 서랍의 물건을 제자리로 |
| Rename | 의도가 드러나지 않는 이름을 의미가 명확한 이름으로 교체 | 라벨을 다시 붙이기 |
| Introduce Parameter Object | 함께 몰려다니는 여러 인자를 하나의 값 객체로 묶음 | 낱개 부품을 세트로 포장 |
| Characterization Test(Golden Master) | 리팩터링 전 "현재 동작 그대로"를 기록해 고정하는 테스트 | 공사 전 현재 상태 사진 촬영 |
| Cyclomatic Complexity | 코드 안의 분기(if/for/while 등) 개수 기반 복잡도 지표 | 미로의 갈림길 개수 |
| Duplication(중복률) | 전체 코드 중 동일·유사한 코드가 차지하는 비율 | 복사-붙여넣기 흔적 |

## 깊이 이해

### 왜 코드 스멜이 쌓이는가 (배경)
- 요구사항이 늘 때마다 기존 메서드에 if문을 덧붙이는 방식으로 기능을 추가하면, 메서드 하나가 결제 검증·금액 계산·저장·이벤트 발행을 모두 떠안게 된다. 이런 상태에서 결제 정책 하나만 바꾸려 해도 200줄짜리 메서드 전체를 읽어야 하므로 결함 확률이 커진다.

### 코드 스멜을 구체 수치로 판별하기
- Long Method: 메서드 길이 50줄 이상 또는 분기(if/for) 10개 이상이면 후보로 본다. Cyclomatic Complexity가 10을 넘으면 테스트 케이스도 최소 10개 이상 필요해져 테스트 부담이 커진다.
- Duplicate Code: 정적분석 도구 기준 duplicated lines 3%를 넘으면 동일 로직 수정 시 누락 위험이 커진다(한 곳만 고치고 나머지를 놓치는 결함).
- God Class(불필요하게 많은 책임): 필드·메서드 수가 급증하고 여러 도메인 개념을 한 클래스가 담당하면 Move Class 대상이 된다.

### 워크드 예제 — 200줄 결제 메서드
- 리팩터링 전: `processPayment()` 한 메서드가 200줄, Cyclomatic Complexity 32, 분기 18개. 결제 검증 실패, 재고 부족, 카드 거절, 이벤트 발행 실패가 모두 한 메서드 안에서 분기 처리된다.
- 절차: ① characterization test로 기존 입력·출력 조합 30개(정상 결제, 카드 거절, 재고 부족, 타임아웃 등)를 먼저 테스트로 고정한다. ② Extract Method로 검증(`validate`)·계산(`calculateAmount`)·저장(`save`)·이벤트 발행(`publishEvent`) 4개 메서드로 분리한다. ③ 각 단계마다 테스트 30개를 재실행해 100% 통과를 확인한다.
- 리팩터링 후: 메서드당 평균 40~50줄, Cyclomatic Complexity는 메서드별 5~8 수준으로 낮아진다. 결제 정책만 바꿀 때는 `calculateAmount` 하나만 읽으면 된다.

### 어떤 스멜에 어떤 패턴을 쓰는가 (판별 원리)
- Long Method(50줄↑, 분기 10개↑) → Extract Method로 책임 단위 분리.
- Feature Envy(다른 클래스 필드를 더 많이 참조) → Move Method로 그 클래스로 이동.
- Long Parameter List(인자 5개 이상) → Introduce Parameter Object로 값 객체화.
- Duplicate Code(중복률 3%↑) → Extract Method 후 공통 모듈로 승격, 필요하면 Move Class.
- 판단 공통 기준: "이 변경이 외부 API·반환값·부작용을 하나라도 바꾸는가?"가 '예'이면 그건 리팩터링이 아니라 기능 변경이다.

### 흔한 오해
- 기능 개발과 리팩터링을 한 커밋에 섞으면 리뷰어가 "동작이 바뀐 건지 구조만 바뀐 건지" 구분할 수 없어 리뷰·검증 범위가 커진다. 그래서 실무에서는 refactoring-only PR로 분리해 feature diff 0건을 확인한다.
- characterization test 없이 구조만 바꾸면, 원래 있던 버그까지 "정상 동작"으로 착각해 없앨 위험(혹은 반대로 정상 동작을 깨는 회귀)이 있다.

## 연결 개념
- 코드 스멜 — 리팩터링 대상을 식별하는 신호 체계
- 단위 테스트·회귀 테스트(Characterization Test) — 동작 보존을 보장하는 안전망
- 기술부채(279편) — 리팩터링을 미룰 때 쌓이는 비용, 리팩터링은 부채 상환의 대표 실행 수단

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

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
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
