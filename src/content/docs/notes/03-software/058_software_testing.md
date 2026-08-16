---
sidebar:
  order: 58
  label: "058. 소프트웨어 테스트: 단위•통합•시스템•인수 (Software Testing)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "소프트웨어 테스트: 단위•통합•시스템•인수 (Software Testing)"
date: "2026-08-13T16:03:00+09:00"
tags:
  - "notes-software"
weight: 58
extra:
  question_no: "058"
  source_status: "기출"
  source_history: "120회"
  priority: 50
  priority_note: "120회 기출, 테스트 단계•목적 구분"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Software Testing (소프트웨어 테스트)**: 소프트웨어의 결함(Defect)을 도출하고 사용자 요구사항 준수 여부 및 제품 품질(Quality)을 동적/정적으로 검증/확인(V&V)하는 제반 활동.
- **Verification vs Validation (V&V)**: Verification(검증)은 "제품을 올바르게 만들고 있는가?(Right Building)"를 명세서 사양 관점에서 검사, Validation(확인)은 "올바른 제품을 만들었는가?(Right Product)"를 사용자 목적 관점에서 검사.
- **Test Pyramid**: 마이크 애들(Mike Cohn)이 제안한 테스트 전략 모델로, 하단의 빠른 단위 테스트(Unit) 비율을 극대화하고 상단의 느리고 비싼 E2E/인수 테스트 비율을 줄이는 피라미드 구조.

</details>

- 정의/개념: 소프트웨어 수명주기 전반에 걸쳐 요구사항 명세 적합성(Verification) 및 사용자 수용 목적(Validation)을 동적으로 실행 및 판정하는 **Software Testing 4대 단계**
- 배경/필요성: 결함을 늦게 발견하면 **수정 범위•회귀 비용** 증가

#### 한줄 요약

- 소프트웨어 테스트로 실제 결과와 기대 결과를 비교하는 것이 핵심이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Test Oracle**: 테스트 실행 결과가 참(True)인지 거짓(False)인지 판단하기 위해 미리 정의된 올바른 기대값(Expected Result) 또는 판단 기준.
- **Regression Testing (회귀 테스트)**: 소스코드 수정이나 기능 추가 후, 기존에 정상 작동하던 다른 모듈에 부작용(Side Effect) 결함이 발생하지 않았음을 재검증하는 테스트.

</details>

- **V-Model** 기반의 개발 단계별 1:1 대칭 테스트 레벨 매핑
- **Test Oracle & Test Case** 기반의 정량적 Pass/Fail 판정
- **Regression Testing** 자동화를 통한 지속적 일관 품질 보장

#### 한줄 요약

- 기대 결과에 따른 판정과 회귀 테스트가 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Unit Test (단위 테스트)**: 소스코드의 최소 단위(메서드, 클래스)를 독립적으로 격리하여 비즈니스 로직의 정합성을 검증하는 속도 빠른 테스트 (JUnit, PyTest).
- **Integration Test (통합 테스트)**: 단위 모듈 간의 인터페이스, 데이터 흐름, DB 연동, API 통신 결합 부작용을 검증하는 테스트 (Big Bang, Top-down, Bottom-up, Sandwich).
- **System Test (시스템 테스트)**: 실제 운영과 유사한 전체 통합 환경에서 기능적 요구사항 및 비기능적 요구사항(성능, 보안, 가용성)을 풀 스택으로 검증.
- **Acceptance Test (인수 테스트)**: 최종 사용자가 시스템이 요구사항 및 계약 기준을 만족하는지 검증하고 시스템 수용 여부를 결정하는 최종 단계 (Alpha/Beta Test).

</details>

```text
 [테스트 근거] ─── [테스트 케이스]
       │                    │
 [결함 저장소] ─── [테스트 실행기]
       │                    │
 [결과 저장소] ─── [테스트 픽스처]
```

선의 의미: 소프트웨어 개발 단계(V-Model의 왼쪽 Downstream)와 테스트 검증 레벨(V-Model의 오른쪽 Upstream)이 1:1 대칭 매핑되는 아키텍처 구조.

| 구성요소 | 책임 |
|:---|:---|
| 테스트 근거 | 요구사항•설계•위험 등 판정 기준 제공 |
| 테스트 케이스 | 입력•사전 조건•기대 결과 정의 |
| 테스트 픽스처 | 반복 가능한 실행 환경과 상태 구성 |
| 테스트 실행기 | 대상 실행과 실제 결과 수집 |
| 결과 저장소 | 통과•실패와 실행 증거 보관 |
| 결함 저장소 | 실패 원인•수정•재시험 상태 추적 |

#### 한줄 요약

- 테스트 근거, 테스트 케이스, 테스트 픽스처, 테스트 실행기, 결과 저장소, 결함 저장소의 연결 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Test Double (테스트 대역)**: 단위/통합 테스트 시 의존 객체(DB, 외부 API)를 가짜 객체로 대체하여 격리 테스트를 가능하게 하는 대역 객체 모음 (Dummy, Fake, Stub, Mock, Spy).

</details>

```text
┌──────────────────────────────┐
│ 테스트 계획 & 분석 (Basis)   │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 테스트 케이스 설계        │
│ 2. 픽스처•대역 구성          │
│ 3. 테스트 대상 실행          │
│ 4. 오라클 결과 판정          │
│ 5. 결함 기록•재시험          │
└──────────────┬───────────────┘
               ▼
   [테스트 리포트 산출 완결]
```

### 동작 원리

1. 테스트 케이스 설계: 근거에서 입력•기대 결과 도출.
2. 픽스처•대역 구성: 반복 환경과 Mock•Stub 의존성 준비.
3. 테스트 대상 실행: 실행기로 SUT 결과와 증거 수집.
4. 오라클 결과 판정: 실제 결과와 기대 결과 비교.
5. 결함 기록•재시험: 결함 수정 후 회귀 시험 수행.

#### 한줄 요약

- 오라클 판정에 따른 통과 증거 기록과 결함 증거 기록이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Mock vs Stub**: Stub은 호출 시 미리 준비된 가짜 데이터(Fixed Response)를 반환하고, Mock은 가짜 데이터 반환뿐만 아니라 해당 메서드가 '몇 번, 어떤 파라미터로 호출되었는지(Behavior Verification)'까지 검증하는 객체.

</details>

| Test Double 종류 | 핵심 정의 및 구현 방식 |
|:---|:---|
| Dummy | 인스턴스화된 매개변수로 넘겨지기만 할 뿐 내부 메서드는 실제로 전혀 호출되지 않는 객체 |
| Fake | 복잡한 런타임 동작을 단순화하여 구현한 객체 (e.g., RDBMS 대신 인메모리 H2/HashMap 사용) |
| Stub | 테스트 호출 시 미리 지정된 고정값(Hardcoded Result)만을 반환하는 응답 객체 |
| Spy | Stub의 역할을 하면서 호출된 횟수, 기록 등 상태 정보를 모니터링하여 기록하는 객체 |
| Mock | 행위 검증(Behavior Verification)을 목적으로 특정 메서드 호출 유무와 횟수를 검증하는 객체 |

#### 한줄 요약

- 단위 테스트, 통합 테스트, 시스템 테스트, 인수 테스트 순으로 검증 경계가 확대된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Defect Inflow Cost**: 결함 발견 시점이 개발 극초기(요구분석)에서 운영 배포 후로 뒤로 밀릴수록 조치 비용이 지수함수적으로 증가하는 법칙.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 상단 E2E•시스템 시험 편중으로 피드백 지연 | 위험 기반 **Test Pyramid** 구성 | 빠른 시험과 현실적 검증 균형 |
| DB•외부 API 의존성 때문에 단위 시험 격리 곤란 | **Mockito / WireMock 등 Test Double** 주입 | 반복 가능한 독립 시험 확보 |
| 코드 수정 후 무관한 모듈에서 연쇄 장애 발생 | **CI 파이프라인 상의 Automated Regression Test** 인가 | 부작용(Side Effect) 차단 |

> 사례: **JUnit 5 + Mockito + SpringBootTest + Jacoco (Coverage Check)** 연동 체계 구축

#### 한줄 요약

- 위험 기반 테스트, 경계값 분석, 독립 픽스처에 기반한 시험 조합이 핵심이다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **소프트웨어 테스트 수립 기준(Software Testing Strategy Standards)**: V-Model 검증 레벨, Test Pyramid 비율 및 자동화 검증율에 의거한 체계.

</details>

- 내부 로직은 **단위**, 경계는 **통합**, 요구 수용은 **시스템•인수 시험** 선택

#### 한줄 요약

- 검증 범위와 결함 유형에 맞는 테스트 단계 선택 기준이 핵심이다.
