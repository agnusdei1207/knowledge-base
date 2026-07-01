---
title: "XP - 페어 프로그래밍·TDD (Extreme Programming)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 36
---

# 📖 【암기용】 개념 완전 이해

> 목적: XP를 처음 보는 사람도 기술 실천 중심 애자일이라는 관점으로 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: XP는 짧은 릴리스, TDD, 페어 프로그래밍, 리팩터링으로 변경 비용을 낮추는 애자일 개발 방식
- **왜 필요한가**: 요구사항이 자주 바뀌면 설계 문서만으로 품질을 지키기 어렵다. XP는 테스트와 코드 개선을 매일 수행해 변경을 받아들일 수 있는 코드 기반을 만든다.
- **핵심 직관**: 매번 큰 수리를 미루지 않고 매일 검사와 정비를 반복해 제품 상태를 유지하는 방식이다.

## 깊이 이해
- **배경·문제의식**: 변경이 잦은 프로젝트에서는 초기 설계가 빠르게 낡고, 결함이 누적되면 작은 기능 추가도 위험해진다. XP는 TDD, CI, refactoring, collective ownership으로 코드 품질을 지속 관리한다.
- **작동 원리**: 개발자는 테스트를 먼저 작성하고 실패를 확인한 뒤 최소 코드로 통과시킨다. 페어 프로그래밍으로 실시간 리뷰를 수행하고, CI가 전체 테스트를 반복 실행한다. 작은 릴리스로 고객 피드백을 자주 받는다.
- **비유**: 축구팀이 경기 후 한 번 회고하는 것이 아니라, 훈련 중 계속 코치 피드백과 전술 수정을 받는 구조이다.
- **구체 예시**: 주문 API 변경 시 실패하는 단위 테스트 3개를 먼저 작성하고, 구현 후 CI에서 2,000개 회귀 테스트를 10분 내 통과시킨 뒤 리팩터링을 수행함.
- **흔한 오해·주의점**: XP는 문서 없는 코딩 방식이 아니다. 사용자 스토리, acceptance test, coding standard, test suite가 있어야 변경 대응이 가능함.

## 연결 개념
- TDD: 실패 테스트 작성 후 구현과 리팩터링을 반복하는 개발 기법
- Pair Programming: 두 개발자가 driver와 navigator 역할로 실시간 리뷰 수행
- Continuous Integration: 코드 통합 시 자동 빌드·테스트 수행

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: XP 답안은 애자일 원칙보다 TDD, pair programming, refactoring, CI가 변경 비용과 결함 유출률을 어떻게 낮추는지 보여야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: XP는 변경 빈도가 높은 환경에서 테스트와 코드 품질 실천으로 제품을 지속 개선하는 애자일 방법론이다.
> 2. **가치**: TDD, pair programming, CI, refactoring으로 결함을 개발 초기에 발견하고 회귀 위험을 줄인다.
> 3. **판단 포인트**: 테스트 자동화율, code coverage, pairing 비용, refactoring debt를 함께 평가해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| XP 실천 항목 이해 확인 | pair programming, TDD, refactoring, CI, collective ownership | Scrum 이벤트와 혼동 |
| 품질 내재화 판단 확인 | test-first, 자동 회귀 테스트, small release | 테스트를 개발 후 검증으로만 설명 |
| 비용·조직 trade-off 확인 | pairing 투입비, 숙련도, 코드 소유권 | 페어 프로그래밍을 인력 낭비로 단정 |

> 요약: XP 문제는 기술 실천이 변경 비용과 결함 지표에 미치는 영향을 설명해야 점수를 확보한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 기술 실천 중심 애자일 방법론
- 배경: 요구사항 변경이 잦을수록 코드 중복, 낮은 테스트 커버리지, 회귀 결함이 누적되어 반복 개발 속도가 저하됨.
- 필요성: TDD, Pair Programming, Continuous Integration, Refactoring으로 테스트 커버리지, build 실패율, 회귀 결함 수를 관리해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
User Story -> Acceptance Test -> TDD -> Pair Programming
           -> CI Build/Test -> Refactoring -> Small Release
           +-> Collective Ownership / Coding Standard
```

| 구성요소 | 역할 | 산출물·지표 |
|:---|:---|:---|
| TDD | 테스트 선행 구현 | unit test, coverage, mutation score |
| Pair Programming | 실시간 리뷰와 지식 공유 | pairing log, review defect |
| Refactoring | 외부 기능 유지한 구조 개선 | code smell, complexity |
| CI/Small Release | 빠른 통합과 고객 피드백 | build time, release frequency |

> 요약: XP는 테스트, 리뷰, 구조 개선, 릴리스를 작은 주기로 묶어 코드 변경 리스크를 통제한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Story 선택 -> Acceptance Criteria 작성 -> 실패 테스트 작성
-> 최소 구현 -> 테스트 통과 -> Refactoring -> CI 검증 -> Small Release
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 사용자 스토리와 수용 기준 확정 | INVEST, acceptance test |
| 2 | 실패 단위 테스트 작성 | red 단계 확인 |
| 3 | 최소 코드 구현과 테스트 통과 | green 단계, coverage 80% 이상 |
| 4 | 리팩터링과 페어 리뷰 수행 | cyclomatic complexity 10 이하 |
| 5 | CI 통합과 소규모 릴리스 | build 10분 이내, rollback plan |

> 요약: XP는 red-green-refactor 루프를 CI와 small release에 연결해 변경을 작은 단위로 검증한다.

---

## Ⅳ. 특징

| 구분 | 일반 애자일 실행 | XP | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 개발 방식 | 구현 후 테스트 | test-first, TDD | coverage 80% 이상 |
| 리뷰 | PR 단계 리뷰 | pair programming 실시간 리뷰 | review defect density |
| 코드 품질 | 결함 발생 후 수정 | 지속 refactoring | complexity 10 이하 |
| 릴리스 | sprint 종료 중심 | small release, CI | 배포 빈도 주 1회 이상 |

> 요약: XP는 회의·관리보다 코드 수준 실천으로 품질과 변경 대응력을 만든다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | Scrum | XP | 선택 기준 |
|:---|:---|:---|:---|
| 초점 | 역할·이벤트·관리 | 개발 실천·코드 품질 | 결함·회귀 리스크가 크면 XP 보강 |
| 산출물 | backlog, sprint increment | test suite, refactored code | 자동 테스트 기반 필요 |
| 팀 역량 | PO·SM 운영 역량 | TDD·refactoring 숙련도 | pairing 수용 문화 필요 |

> 요약: Scrum은 관리 프레임, XP는 코드 품질 실천이므로 함께 적용하면 관리와 기술 통제가 결합된다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| TDD 형식화 | 테스트 가치 이해 부족 | test review, mutation testing | mutation score 60% 이상 |
| pairing 비용 증가 | 모든 작업 동일 적용 | 난도 높은 모듈 중심 선택 pairing | pairing time ratio |
| 리팩터링 지연 | 기능 일정 압박 | refactoring budget 10~20% 확보 | technical debt trend |

> 요약: XP 리스크는 실천의 형식화와 비용 증가이므로 적용 범위와 품질 지표를 분리해 운영해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 테스트 | unit coverage 80% 이상, flaky test 2% 이하 | CI report |
| 코드 품질 | complexity 10 이하, duplication 3% 이하 | SonarQube, static analysis |
| 릴리스 | 변경 실패율 15% 이하, MTTR 30분 이하 | DORA dashboard |

> 요약: XP 성과는 테스트 커버리지, 코드 복잡도, 변경 실패율로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 결제·정산·인증 등 결함 비용이 큰 모듈부터 TDD와 pair programming을 적용하고 coverage 80% 기준 설정
2. CI pipeline에 unit test, static analysis, mutation test를 넣어 build 10분 이내와 품질 gate 동시 관리
3. Sprint capacity의 10~20%를 refactoring budget으로 배정해 code smell과 technical debt를 누적 관리

**결론 (2줄):**
- 기술사 판단: 변경 빈도와 회귀 위험이 큰 제품은 XP 실천을 Scrum에 결합하고, 단순 유지보수는 선별 적용함
- 향후 방향: XP 실천은 DevOps, DevSecOps, AI code review와 결합되어 코드 품질 지표 중심의 지속 개선 체계로 확장됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "XP를 설명하시오" | red-green-refactor와 CI 흐름 | TDD, pairing, refactoring 특징 |
| 요구사항 명시형 | "품질 향상 방안을 제시하시오", "비교하시오" | 결함 예방 흐름과 지표 | Scrum 대비 기술 실천, 비용 대응 |

> 요약: 설명형은 XP 실천 항목, 방안형은 테스트 자동화와 코드 품질 지표 중심으로 목차를 전환한다.
