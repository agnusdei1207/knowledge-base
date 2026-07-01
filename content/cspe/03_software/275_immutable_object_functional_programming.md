---
title: "불변 객체·함수형 프로그래밍 (Immutable Object Functional Programming)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 275
---

# 📖 【암기용】 개념 완전 이해

> 목적: 불변 객체와 함수형 프로그래밍을 상태 변경을 줄여 동시성 결함과 부작용을 낮추는 설계 방식으로 이해하게 만든다.

## 한눈에
- **개요**: 불변 객체는 생성 후 상태가 바뀌지 않는 객체이고, 함수형 프로그래밍은 순수 함수와 값 변환을 중심으로 구성한다.
- **왜 필요한가**: 멀티스레드와 분산 환경에서 공유 상태 변경이 race condition, 재현 어려운 결함, 테스트 부담을 만든다.
- **핵심 직관**: 원본 문서를 고치지 않고 새 사본을 만들어 전달하면 누가 언제 바꿨는지 추적하기 쉽다.

## 깊이 이해
- **배경·문제의식**: 객체지향 시스템은 내부 상태 변경이 많을수록 호출 순서에 따라 결과가 바뀐다. 함수형 접근은 입력이 같으면 출력이 같은 순수 함수를 중심으로 예측 가능성을 높인다.
- **작동 원리**: 객체 필드를 `final`로 고정하고, 변경 시 새 객체를 만들며, 컬렉션은 persistent data structure로 구조 공유를 사용한다.
- **비유**: 회의록 원본을 수정하지 않고 버전별 사본을 남기면 변경 이력이 명확해지는 것과 같다.
- **구체 예시**: Java `String`은 불변이라 여러 스레드가 공유해도 내부 문자 배열 변경 경쟁이 없다. Kotlin data class `copy()`는 값 변경을 새 객체로 표현한다.
- **흔한 오해·주의점**: 불변 객체는 메모리를 무조건 많이 쓰는 구조가 아니다. 구조 공유와 escape analysis를 사용하면 할당 비용을 줄일 수 있다.

## 연결 개념
- 스레드 안전 — 공유 변경 상태 제거
- 순수 함수 — 입력과 출력의 결정성
- 이벤트 소싱 — 상태 변경을 이벤트 로그로 보존

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 불변성과 함수형 기법을 동시성, 테스트, 상태 관리 관점에서 답안화한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 불변 객체는 생성 후 상태 변경을 금지하고, 함수형 프로그래밍은 순수 함수·값 변환·부작용 격리를 지향한다.
> 2. **가치**: 공유 상태 변경을 줄여 race condition, rollback 복잡도, 테스트 조합 수를 감소시킨다.
> 3. **판단 포인트**: 적용 범위는 도메인 값 객체, 병렬 처리, 이벤트 흐름에 우선 두고 대용량 객체 복사는 구조 공유로 통제한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 상태 관리 패러다임 이해 확인 | immutable, pure function, side effect isolation | 함수형 언어 문법 나열 |
| 동시성 설계 판단 확인 | 공유 변경 상태 제거, thread-safe by design | lock 대체 가능 조건 누락 |
| 실무 적용 한계 확인 | 객체 생성 비용, GC 압력, 구조 공유 | 모든 객체를 불변으로 만들라는 단정 |

> 요약: 이 문제는 함수형 개념보다 상태 변경 통제와 적용 범위 판단을 묻는다.

---

## Ⅰ. 개요 및 필요성

불변 객체·함수형 프로그래밍은 상태 변경을 제한하는 소프트웨어 설계 방식이다. 동시성, 테스트, 롤백, 이벤트 처리에서 변경 가능한 공유 상태가 결함 원인이 되므로 값 중심 모델과 부작용 격리가 필요하다.

---

## Ⅱ. 구조 및 구성요소

```text
Input Value -> Pure Function -> New Value
  / Immutable Object -> Structural Sharing -> Safe Sharing
  / Side Effect Boundary -> DB/IO/Network
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Immutable Object | 생성 후 상태 고정 | final, readonly, record |
| Pure Function | 같은 입력에 같은 출력 | 테스트·병렬화 용이 |
| Structural Sharing | 변경 부분만 새 노드 생성 | persistent collection |
| Effect Boundary | IO·DB 변경 격리 | transaction, adapter layer |

> 요약: 함수형 구조는 값 변환 경로와 부작용 경계를 분리해 상태 변경 지점을 줄인다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요청 입력 -> 값 객체 생성 -> 순수 함수 조합
  -> 새 상태 산출 -> 부작용 경계에서 저장/전송
  -> 로그/이벤트로 변경 추적
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 입력을 값 객체로 변환 | validation pass |
| 2 | 순수 함수로 도메인 계산 | deterministic test |
| 3 | 새 객체 또는 이벤트 생성 | original object unchanged |
| 4 | DB·메시지 등 부작용 수행 | transaction boundary |

> 요약: 계산은 순수 함수로 격리하고 외부 변경은 경계 계층에 모아 재현성과 추적성을 확보한다.

---

## Ⅳ. 특징

| 구분 | 가변 객체 중심 | 불변·함수형 중심 | 정량·기술 포인트 |
|:---|:---|:---|:---|
| 동시성 | lock 필요 | 공유 읽기 가능 | race condition 경로 감소 |
| 테스트 | 호출 순서 의존 | 입력·출력 검증 | property-based test 가능 |
| 상태 추적 | 내부 변경 누락 가능 | 버전·이벤트 추적 | audit log와 연결 |
| 비용 | 객체 재사용 | 객체 생성 증가 가능 | allocation rate MB/s 측정 |

> 요약: 불변성은 정확성과 추적성을 얻는 대신 할당량과 GC 압력을 지표로 관리해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 도메인 모델 | setter 기반 엔티티 | value object, record | 값 동일성·검증 규칙 명확한 영역 |
| 병렬 처리 | 공유 컬렉션 변경 | map/filter/reduce | 데이터 독립 작업 |
| 상태 변경 | in-place update | event/new state | 감사·롤백 요구 |

> 요약: 불변성은 값 객체, 병렬 계산, 감사 추적이 필요한 상태 변경에 우선 적용한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| GC 압력 | 객체 생성량 증가 | structural sharing, escape analysis | allocation rate, GC pause |
| 모델 왜곡 | 모든 엔티티 불변화 | aggregate 단위 변경 허용 | domain rule violation |
| 학습 비용 | 함수형 추상화 과다 | team guideline, code review | review defect count |

> 요약: 적용 리스크는 할당량, 도메인 모델 적합성, 팀 규칙으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 동시성 | shared mutable state 신규 0건 | static analysis, review |
| 테스트 | pure function coverage 90% 이상 | unit/property test |
| 자원 | allocation rate 기준 대비 20% 이내 증가 | profiler, GC log |

> 요약: 성공 여부는 공유 변경 상태 감소, 순수 함수 테스트, 할당량 증가폭으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 금액, 기간, 식별자 같은 도메인 값은 Java record, Kotlin data class, C# record로 불변 값 객체화함.
2. 병렬 계산은 mutable shared list 대신 stream map/filter/reduce와 immutable collection으로 구성함.
3. 외부 변경은 repository, message producer, transaction boundary에 모아 순수 계산과 IO를 분리함.

**결론 (2줄):**
- 기술사 판단: 도메인 값과 병렬 계산은 불변성을 기본으로 두고, 대용량 엔티티 변경은 aggregate 경계에서 제한적으로 허용.
- 향후 방향: 함수형 패턴은 reactive stream, event sourcing, CQRS와 결합해 상태 변경을 추적 가능한 값 흐름으로 전환함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "설명하시오", "기술하시오" | 값 변환과 부작용 경계 흐름 | 동시성·테스트·추적성 |
| 요구사항 명시형 | "설계하시오", "적용 방안을 제시하시오" | 도메인 값 객체와 IO 경계 설계 | GC 압력, 적용 범위, 선택 기준 |

> 요약: 설명형은 패러다임 구조, 설계형은 상태 변경 지점과 경계 통제 중심으로 전환한다.
