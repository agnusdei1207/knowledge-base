---
sidebar:
  order: 89
  label: "089. 데이터베이스 정규화 1NF~BCNF (Database Normalization)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "데이터베이스 정규화 1NF~BCNF (Database Normalization)"
date: "2026-08-13T19:08:00+09:00"
tags:
  - "notes-software"
weight: 89
extra:
  question_no: "089"
  source_status: "기출"
  source_history: "120회, 135회"
  priority: 70
  priority_note: "120•135회 반복, 정규화•함수종속 핵심"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Database Normalization (데이터베이스 정규화)**: 릴레이션 간의 바람직하지 않은 데이터 중복(Redundancy)과 갱신 이상(Anomaly)을 제거하기 위해, 함수적 종속성(FD)을 기반으로 스키마를 단계별(1NF~BCNF/5NF)로 무손실 분해(Lossless Decomposition)하는 논리적 설계 기법.
- **Data Anomaly (데이터 이상 현상)**: 테이블 정규화 미비로 인해 데이터 CUD 연산 시 발생하는 3대 현상 (삽입 이상, 수정 이상, 삭제 이상).
- **Functional Dependency (FD, 함수적 종속성)**: 어떤 속성 $X$의 값이 다른 속성 $Y$의 값을 유일하게 결정할 때, "$Y$는 $X$에 함수적으로 종속된다 ($X \rightarrow Y$)"라고 정의하는 속성 간의 관계.

</details>

- 정의/개념: 데이터베이스 논리 설계 시 데이터의 중복성을 극소화하고 이상 현상(Anomaly)을 제거하기 위해 함수적 종속성을 기반으로 릴레이션을 분해해 나가는 프로세스인 **Database Normalization (정규화)**
- 배경/필요성: 한 릴레이션의 여러 사실 혼재는 **삽입•수정•삭제 이상** 유발

#### 한줄 요약

- 고객 정보가 주문마다 반복되면 주소가 일부만 바뀔 수 있어 고객과 주문을 분리한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Lossless Join Decomposition (무손실 조인 분해)**: 분해된 릴레이션들을 다시 자연 조인(Natural Join)했을 때, 원래의 릴레이션과 정확히 일치하며 유령 튜플(Spurious Tuple)이 생성되지 않는 성질.
- **Dependency Preservation (종속성 보존)**: 릴레이션 분해 후에도 원본 릴레이션의 모든 함수적 종속성(FD)이 분해된 릴레이션들 상에서 그대로 검증 및 유지되는 성질.

</details>

- **3대 이상 현상 (Insertion, Update, Deletion Anomaly) 제거**
- **Functional Dependency (함수적 종속성)** 기반의 릴레이션 무손실 분해
- **Lossless Join Decomposition (무손실 조인)** 및 **Dependency Preservation (종속성 보존)** 보장

#### 한줄 요약

- 정규화는 같은 사실을 한곳에 저장해 수정 오류를 줄이지만 조회 때 표를 다시 연결할 수 있다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Insertion Anomaly (삽입 이상)**: 데이터를 삽입할 때 불필요한 원치 않는 정보까지 억지로 함께 입력해야 하거나, 필수 키 값이 없어 입력을 못 하는 현상.
- **Update Anomaly (수정 이상)**: 중복 데이터 중 일부 튜플만 수정하여 데이터 불일치(Inconsistency)가 발생하는 현상.
- **Deletion Anomaly (삭제 이상)**: 튜플을 삭제할 때 삭제하고 싶지 않은 연관된 다른 유용한 정보까지 함께 유실되는 현상.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Normalization Process                           │
├───────────────┬────────────────────────────────────────────────────────┤
│ 1NF (원자값)  │ 다중값 속성(Repeating Group) 제거                      │
│ 2NF (부분 종속)│ 복합키의 일부에만 종속되는 부분 함수 종속성 제거 (Full FD)│
│ 3NF (이행 종속)│ $A \rightarrow B$ 이고 $B \rightarrow C$ 인 이행적 함수 종속성 제거    │
│ BCNF (결정자) │ 모든 결정자(Determinant)가 후보키(Candidate Key)가 되도록 분해│
└───────────────┴────────────────────────────────────────────────────────┘
```

선의 의미: 1NF부터 BCNF까지 차례대로 데이터 이상 현상의 원인이 되는 함수적 종속 관계를 제거해 나가는 구조.

| 정규형 (Normal Form) | 제거 대상 (Eliminated Target) | 정규화 만족 조건 및 상태 |
|:---|:---|:---|
| **1NF (제1정규형)** | **Repeating Group (다속성/다중값)** | 모든 속성의 도메인이 **원자값(Atomic Value)** 으로만 구성 |
| **2NF (제2정규형)** | **Partial Functional Dependency** | 기본키가 복합키일 때, **완전 함수 종속(Full FD)** 만족 |
| **3NF (제3정규형)** | **Transitive Functional Dependency**| 기본키가 아닌 속성 간의 **이행적 함수 종속성 제거** |
| **BCNF (보이스-코드)**| **Non-Key Determinant** | 모든 함수적 종속성 $X \rightarrow Y$ 에서 **결정자 $X$가 후보키** |

#### 한줄 요약

- 업무 종속과 키를 찾아 표를 나누고 복원과 제약 유지를 확인한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Determinant Key Rule**: BCNF에서는 "모든 결정자는 후보키여야 한다"는 강력한 규칙 적용.

</details>

```text
[비정규 릴레이션]
       │ (속성 원자값화)
       ▼
 [1NF (First Normal Form)]
       │ (부분 함수 종속성 제거: Full FD화)
       ▼
 [2NF (Second Normal Form)]
       │ (이행적 함수 종속성 제거: X -> Y -> Z)
       ▼
 [3NF (Third Normal Form)]
       │ (모든 결정자를 후보키화)
       ▼
 [BCNF (Boyce-Codd Normal Form)]
```

### 동작 원리

1. **1NF**: 취미 등 배열/복수 형태 데이터를 쪼개어 단일 원자값 렌더링.
2. **2NF**: `{학번, 과목코드} -> 성적`, `{학번} -> 학과명` 일 때, 학과명은 학번에만 종속되므로 릴레이션 분리.
3. **3NF**: `학번 -> 학과코드`, `학과코드 -> 학과위치` 일 때, `학번 -> 학과위치` 이행 종속 분리.
4. **BCNF**: 후보키가 아닌 속성이 타 속성을 결정할 경우 릴레이션 분리.

#### 한줄 요약

- 사실을 정하는 규칙대로 표를 나누고 다시 합쳤을 때 원본만 나오는지 확인한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **3NF vs BCNF**: 3NF 합성은 종속성 보존을 목표로 하며, BCNF 분해는 일부 종속성을 개별 릴레이션에서 검사하지 못할 수 있음.

</details>

| 비교 항목 | 3NF (제3정규형) | BCNF (보이스-코드 정규형) |
|:---|:---|:---|
| 만족 조건 | 이행적 함수 종속 제거 ($X \rightarrow Y, Y \rightarrow Z$) | **모든 결정자 $X$가 반드시 후보키(Super Key)** |
| 종속성 보존 여부 | **종속성 보존 합성 가능** | **일부 종속성을 조인 후 검사할 수 있음** |
| 분해 수준 | 실무 상용 DB 설계의 표준 목표 | 고도의 무결성이 필요한 엄격한 설계 |
| 조인 오버헤드 | BCNF 대비 조인 횟수 적음 | 과도한 릴레이션 분리로 조인 비용 증가 |

#### 한줄 요약

- 단일 값에서 시작해 키 일부 종속과 키가 아닌 결정자의 이상을 차례로 줄인다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Over-Normalization (과도한 정규화)**: BCNF/4NF/5NF 등 지나친 정규화로 테이블 수가 급증하여 `JOIN` 연산 오버헤드로 인한 성능 추락 현상 (반정규화 필요성 대두).

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 과도한 정규화로 다중 JOIN 발생 및 조회 TPS 추락 | **OLTP 핵심 조회 테이블에 대한 전략적 반정규화(Denormalization)**| 조회 성능 회복 |
| BCNF 분해 시 종속성 보존(Dependency Preservation) 파괴 | **3NF 정규화 수준 유지 및 Application Trigger/Constraint 검증** | 종속성 보존 |
| 정규화 시 PK/FK 인덱스 미생성으로 인한 성능 저하 | **분해된 FK 필드에 B-Tree 인덱스 필수 생성** | 조인 성능 보장 |

> 사례: **쇼핑몰 주문/고객/배송 릴레이션의 3NF 정규화 및 FK 인덱싱**

#### 한줄 요약

- 거래 모델은 사실의 종속대로 표를 나누고 다시 합쳤을 때 원본과 같은지 확인한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **정규화 수립 기준(Database Normalization Standards)**: 데이터 무결성 요건, 함수적 종속성(FD) 및 OLTP 3NF 표준성에 의거한 체계.

</details>

- 종속성 보존이 중요하면 **3NF**, 결정자 이상 제거는 **BCNF** 선택

#### 한줄 요약

- 목표 정규형은 중복 사실 제거와 제약 검사 비용을 함께 고려한다.
