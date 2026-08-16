---
sidebar:
  order: 112
  label: "112. 3단계 스키마 - 외부•개념•내부 (Three-Level Schema)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "3단계 스키마 - 외부•개념•내부 (Three-Level Schema)"
date: "2026-08-13T21:42:00+09:00"
tags:
  - "notes-software"
weight: 112
extra:
  question_no: "112"
  source_status: "기출"
  source_history: "128회"
  priority: 50
  priority_note: "128회 기출, 외부•개념•내부 스키마 구조"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Three-Level Schema Architecture (ANSI/SPARC 3단계 스키마 구조)**: 데이터베이스 시스템의 복잡성을 숨기고 데이터 독립성을 보장하기 위해, 데이터베이스를 외부 스키마(External), 개념 스키마(Conceptual), 내부 스키마(Internal) 3개 계층으로 구분하여 정의한 표준 아키텍처.
- **External Schema (외부 스키마 / 서브키마)**: 개별 사용자나 응용 프로그램의 관점에서 본 데이터베이스의 논리적 뷰(View) 및 접근 범위 정의.
- **Conceptual Schema (개념 스키마 / 전체 스키마)**: 데이터베이스 전체의 통합된 논리적 구조로, 모든 엔티티, 관계, 제약조건, 무결성 규칙을 정의하는 중심 스키마.
- **Internal Schema (내부 스키마 / 물리 스키마)**: 물리적 저장 장치(디스크) 관점의 레코드 포맷, 인덱스 구조, 파티셔닝 및 저장 블록 배치를 정의하는 스키마.

</details>

- 정의/개념: 외부•개념•내부로 DB 표현을 나눈 **3단계 스키마**
- 배경/필요성: 사용자 뷰와 저장 배치 결합은 **변경 전파•권한 노출** 유발

#### 한줄 요약

- 화면과 장부 및 창고 배치를 세 층으로 나누고 번역표로 연결하는 구조이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Multi-External to Single-Conceptual**: 하나의 개념 스키마 위에 다수의 외부 스키마(View)가 존재할 수 있는 N:1 계층적 관계.
- **2-Level Mappings**: 계층 간 사상(External-Conceptual, Conceptual-Internal Mapping)을 통해 상하위 변경 영향 상쇄.

</details>

- **3-Layer Separation (External, Conceptual, Internal)**
- **N:1 External View Multiplicity (다중 외부 뷰 대 단일 개념 스키마)**
- **2-Level Independent Mapping (외부-개념 맵핑 & 개념-내부 맵핑)**

#### 한줄 요약

- 각 층이 관심사를 분리해 변경이 다른 층으로 바로 번지는 것을 줄인다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **External-Conceptual Mapping**: 외부 스키마 뷰 쿼리를 개념 스키마 테이블 연산으로 변환하여 논리적 독립성을 보장하는 사상.
- **Conceptual-Internal Mapping**: 개념 스키마 테이블 연산을 내부 스키마 디스크 블록/인덱스 연산으로 변환하여 물리적 독립성을 보장하는 사상.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                    ANSI/SPARC Three-Level Schema Model                 │
├────────────────────────────────────────────────────────────────────────┤
│ [User A View]       [User B View]       [User C View] (External Schema)│
│       │                   │                   │                        │
│       └───────────────────┼───────────────────┘                        │
│                           ▼ (External-Conceptual Mapping)              │
│                [Unified Conceptual Schema]                             │
│                           │ (Entity, Relationship, Constraint)         │
│                           ▼ (Conceptual-Internal Mapping)              │
│                [Internal Disk Layout Schema]                           │
│                 (B+Tree Index, Page Allocation, Block)                 │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 3개 스키마 계층을 2개 변환 매핑(Mapping)이 중계하여 계층 간 독립성과 투명성을 제공하는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| 외부 스키마 | 사용자별 뷰•접근 범위 표현 |
| 외부-개념 매핑 | 외부 뷰를 통합 논리 구조로 변환 |
| 개념 스키마 | 엔티티•관계•제약조건 통합 정의 |
| 개념-내부 매핑 | 논리 연산을 물리 접근으로 변환 |
| 내부 스키마 | 파일•페이지•인덱스 저장 방식 표현 |

#### 한줄 요약

- 외부 스키마, 개념 스키마, 내부 스키마를 두 단계의 매핑으로 연결한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Query Translation Process**: 외부 스키마 쿼리가 DBMS를 통해 개념 연산 및 내부 디스크 읽기로 2단계 사상되어 결과를 재조합하는 과정.

</details>

```text
[외부 스키마 질의]
       │
       ▼
1. 외부 뷰 해석
       │
       ▼
2. 개념 연산 변환
       │
       ▼
3. 물리 접근 변환
       │
       ▼
4. 저장 데이터 접근
       │
       ▼
5. 외부 형식 반환
```

### 동작 원리

1. 외부 뷰 해석: 사용자 열•행 범위와 권한 확인
2. 개념 연산 변환: 외부-개념 매핑으로 논리 연산 생성
3. 물리 접근 변환: 개념-내부 매핑으로 접근 경로 생성
4. 저장 데이터 접근: 파일•페이지•인덱스에서 레코드 조회
5. 외부 형식 반환: 결과를 사용자 뷰 구조로 투영

#### 한줄 요약

- 외부 스키마의 열을 개념 스키마 개체와 내부 스키마 저장 위치로 매핑하여 조회한 뒤 다시 외부 스키마 형식으로 반환한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Logical vs Physical Abstraction**: 외부-개념 간 추상화 대 개념-내부 간 추상화의 성격 차이.

</details>

| 비교 항목 | External Schema (외부) | Conceptual Schema (개념) | Internal Schema (내부) |
|:---|:---|:---|:---|
| 주요 대상자 | **일반 사용자, Web 개발자** | **데이터 아키텍트 (DA), DB 설계자** | **DBA, 스토리지 관리자** |
| 수량 특성 | **다수 존재 (N개 View 가능)** | **단 1개만 존재 (Single)** | **단 1개만 존재 (Single)** |
| 관심 영역 | **특정 서비스 화면용 서브셋** | **전체 데이터 구조 및 무결성** | **물리 디스크 I/O 최적화** |
| 변환 맵핑 | External-Conceptual Mapping | 양쪽 맵핑의 중심축 | Conceptual-Internal Mapping |

#### 한줄 요약

- 외부는 사용자별 뷰, 개념은 공통 업무 논리 구조, 내부는 물리 저장 배치이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Schema Governance (스키마 거버넌스)**: 개념 스키마 무분별 수정을 통제하고, 변경 발생 시 외부 뷰 매핑을 동기화하는 DB 관리 프로세스.

</details>

| 고려사항 및 문제 | 위협 요소 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| 개념 스키마 변경 시 기존 외부 뷰 파행 | 앱 응용 쿼리 타임아웃 및 Syntax Error | **외부-개념 맵핑(DB View) 사전 업데이트 및 검증** |
| 내부 디스크 파티셔닝 변경 시 개념 스키마 혼선| 물리 튜닝이 논리 모델링에 영향 전파 | **스토리지 엔진 내부 맵핑 투명화 **|
| 외부 뷰 과다 생성으로 인한 DB 성능 저하 | View 매핑 파싱 오버헤드 발생 | **미사용 외부 뷰 주기적 정제 및 인라인 뷰 최적화** |

> 사례: **RDBMS (Oracle / MySQL) View, Synonym 및 Tablespace 기반 3단계 스키마 운용**

#### 한줄 요약

- 개념 스키마는 하나로 유지하되 사용자마다 필요한 속성과 권한만 다른 외부 스키마로 제공한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **3단계 스키마 수립 기준(Three-Level Schema Standards)**: ANSI/SPARC 계층화, 외부 뷰 보안성, 2단계 맵핑 및 데이터 독립성 보장성에 의거한 체계.

</details>

- 사용자별 표현은 **외부**, 공통 논리는 개념, 저장 배치는 내부로 분리

#### 한줄 요약

- 3단계 스키마 적용 기준은 외부 스키마•개념 스키마•내부 스키마를 분리하고 매핑으로 연결한다.
