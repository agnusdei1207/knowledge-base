---
sidebar:
  order: 111
  label: "111. 데이터 독립성 - 논리•물리 (Data Independence)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "데이터 독립성 - 논리•물리 (Data Independence)"
date: "2026-08-13T21:35:00+09:00"
tags:
  - "notes-software"
weight: 111
extra:
  question_no: "111"
  source_status: "기출"
  source_history: "128회"
  priority: 50
  priority_note: "128회 기출, 논리•물리 독립성 구조 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Data Independence (데이터 독립성)**: 데이터베이스 계층 구조(3-Schema Architecture)에서 특정 계층의 스키마 구조가 변경되더라도 상위 계층의 스키마나 응용 프로그램(Application)에 전혀 영향을 주지 않는 데이터 아키텍처 특성.
- **Logical Data Independence (논리적 데이터 독립성)**: 데이터베이스의 개념 스키마(Conceptual Schema) 구조(테이블 컬럼 추가/삭제/변경)가 바뀌어도 외부 스키마(External Schema/View)나 응용 프로그램이 영향을 받지 않는 속성.
- **Physical Data Independence (물리적 데이터 독립성)**: 디스크 물리적 저장 방식(인덱스 재구성, B-Tree 파티셔닝, 파일 레아이웃)이 변경되어도 개념 스키마 및 응용 프로그램이 영향을 받지 않는 속성.

</details>

- 정의/개념: 하위 스키마 변경을 상위 계층에서 숨기는 **데이터 독립성**
- 배경/필요성: 파일 구조와 앱이 결합되면 **저장 변경마다 재개발** 발생

#### 한줄 요약

- 창고 선반을 바꿔도 화면을 고치지 않게 층 사이 번역표를 두는 원리이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **3-Schema Architecture**: ANSI/SPARC에서 제안한 External, Conceptual, Internal 3단계 계층화 분리 모델.
- **Mapping (사상 / 맵핑)**: 계층과 계층 사이의 데이터 변환 룰 (External-Conceptual Mapping, Conceptual-Internal Mapping).

</details>

- **External / Conceptual / Internal 3단계 계층 구조의 명확한 분리**
- **Logical Data Independence** (개념 스키마 변경 $\leftrightarrow$ 외부 스키마 격리)
- **Physical Data Independence** (내부 스키마 변경 $\leftrightarrow$ 개념 스키마 격리)

#### 한줄 요약

- 저장 방식 변경은 물리적 독립성으로, 업무 구조 변경은 논리적 독립성으로 사용자를 보호한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **External-Conceptual Mapping**: 외부 스키마와 개념 스키마 간의 변환 매핑 (논리적 독립성 보장 영역).
- **Conceptual-Internal Mapping**: 개념 스키마와 내부 스키마 간의 변환 매핑 (물리적 독립성 보장 영역).

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   ANSI/SPARC 3-Schema & Data Independence              │
├────────────────────────────────────────────────────────────────────────┤
│ [External Schema A]   [External Schema B]   (사용자 View 계층)         │
│          ▲                    ▲                                        │
│          └───────────┬────────┘ (Logical Data Independence: 외부-개념 Mapping)
│                      ▼                                                 │
│            [Conceptual Schema]             (전체 논리적 데이터 구조)    │
│                      ▲                                                 │
│                      │ (Physical Data Independence: 개념-내부 Mapping)  │
│                      ▼                                                 │
│             [Internal Schema]              (물리적 디스크 저장 구조)    │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 외부/개념/내부 3단계 스키마 사이를 외부-개념 매핑과 개념-내부 매핑으로 상호 격리하여 독립성을 완성하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| **외부 스키마** | 사용자•응용별 데이터 뷰 정의 |
| **외부-개념 매핑** | 외부 뷰와 통합 논리 구조 변환 |
| **개념 스키마** | 전체 엔티티•관계•제약조건 정의 |
| **개념-내부 매핑** | 논리 구조와 물리 저장 구조 변환 |
| **내부 스키마** | 파일•페이지•인덱스 배치 정의 |

#### 한줄 요약

- 외부 스키마, 개념 스키마, 내부 스키마 사이에 두 단계의 매핑을 둔다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Schema Evolution (스키마 진화)**: 비즈니스 요구사항 변경으로 DB 테이블 컬럼이 추가되거나 인덱스가 재구성되어도 매핑 정보만 수정하여 응용 프로그램의 수정 없이 정상 작동하게 하는 메커니즘.

</details>

```text
[스키마 변경]
      │
      ▼
1. 변경 계층 식별
      │
      ▼
2. 영향 매핑 수정
      │
      ▼
3. 상위 인터페이스 보존
      │
      ▼
4. 질의•갱신 호환 검증
      │
      ▼
5. 변경 스키마 전환
```

### 동작 원리

1. **변경 계층 식별**: 개념•내부 스키마 변경 범위 판정
2. **영향 매핑 수정**: 대응 외부-개념•개념-내부 사상 갱신
3. **상위 인터페이스 보존**: 기존 뷰•논리 구조 계약 유지
4. **질의•갱신 호환 검증**: 읽기•쓰기•성능 회귀 시험
5. **변경 스키마 전환**: 호환 기간 후 새 매핑 활성화

#### 한줄 요약

- 외부 스키마와 내부 스키마 사이의 매핑이 변경된 저장 구조를 은닉하여 동일한 결과를 반환한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Logical vs Physical Independence**: 논리적은 비즈니스 테이블 구조 변경 시 응용 보호, 물리적은 파일/인덱스/하드웨어 변경 시 응용/개념 스키마 보호.

</details>

| 비교 항목 | Logical Data Independence (논리적) | Physical Data Independence (물리적) |
|:---|:---|:---|
| **격리 대상 변경** | **테이블 추가/삭제, 컬럼 추가/삭제, 관계 변경** | **인덱스 추가/삭제, 파티셔닝, 파일 레이아웃** |
| **영향 받는 매핑** | **External - Conceptual Mapping** | **Conceptual - Internal Mapping** |
| **달성 난이도** | **높음 (뷰/매핑 구조 설계 복잡성 증가)** | **상대적 낮음 (DBMS가 자동 관리)** |
| **실무 적용 사례** | **DB View 생성 및 ORM 엔티티 맵핑 패턴** | **B+Tree 인덱스 생성 및 파티셔닝 적용** |

#### 한줄 요약

- 물리적 독립성은 저장 구조 변경을, 논리적 독립성은 개념 스키마 변경을 은닉한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **View & Interface Abstraction**: 응용 프로그램이 테이블을 직접 참조하지 않고 DB View 또는 API Interface를 경유하게 하여 독립성 극대화.

</details>

| 3대 독립성 장애 요소 | 발생 원인 및 위협 요소 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Direct Table Access** | 앱이 DB 물리 테이블을 직접 SQL로 조회 | **DB View 또는 ORM 레퍼 인터페이스 레이어 신설** |
| **2. Physical Coupling** | 쿼리 내에 물리적 힌트(`INDEX(idx_user)`) 남발 | **옵티마이저 CBO에 맡기고 힌트 하드코딩 최소화** |
| **3. Breaking Schema Change**| 컬럼 삭제 시 기존 View 및 앱 에러 발생 | **Deprecated 컬럼 유예 기간 설정 및 확장 후 축소**|

> 사례: **MSA 환경에서 DB View 및 JPA Entity Abstraction Layer 기반 데이터 독립성 구현**

#### 한줄 요약

- 번역표가 결과뿐 아니라 쓰기와 속도까지 유지하는지 확인해야 한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **데이터 독립성 수립 기준(Data Independence Standards)**: ANSI/SPARC 3대 스키마, 계층별 Mapping 레이어 및 DB View/ORM 아키텍처에 의거한 체계.

</details>

- 논리 변경은 **외부-개념**, 저장 변경은 개념-내부 매핑으로 격리

#### 한줄 요약

- 데이터 독립성 적용 기준은 어느 계층의 변화를 어떤 매핑이 맡을지 정한다.
