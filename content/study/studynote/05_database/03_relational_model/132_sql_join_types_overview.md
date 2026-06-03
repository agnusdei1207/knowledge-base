+++
weight = 132
title = "132. SQL JOIN 유형 총정리 - INNER·LEFT·RIGHT·FULL·CROSS·SELF"
date = "2026-04-19"
[extra]
categories = "studynote-database"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SQL JOIN은 **두 테이블의 공통 컬럼(키)을 기준으로 행을 결합**하는 연산이며, INNER(교집합)·LEFT(좌측 전체+매칭)·RIGHT(우측 전체+매칭)·FULL(합집합)·CROSS(카테시안 곱)·SELF(자기 참조)로 구분된다.
> 2. **가치**: JOIN은 **정규화된 DB에서 분리된 데이터를 하나로 합치는 유일한 수단**이며, JOIN 유형 선택이 결과 행 수와 NULL 처리를 결정한다.
> 3. **판단 포인트**: INNER는 양쪽 모두 매칭, LEFT는 왼쪽 전체 보존(매칭 없으면 NULL), FULL OUTER는 양쪽 모두 보존이며, **인덱스·실행 계획 최적화**가 성능의 핵심이다.

---

## Ⅰ. 개요 및 필요성

```text
INNER JOIN:  A ∩ B (교집합)
LEFT JOIN:   A 전체 + B 매칭 (없으면 NULL)
RIGHT JOIN:  B 전체 + A 매칭 (없으면 NULL)
FULL JOIN:   A ∪ B (합집합, 없으면 NULL)
CROSS JOIN:  A × B (카테시안 곱)
SELF JOIN:   A ⋈ A (자기 참조)
```

- **📢 섹션 요약 비유**: INNER는 "둘 다 참석한 사람만", LEFT는 "A반 전체 + B반에서 겹치는 사람", FULL은 "양쪽 모두 포함".

---

## Ⅱ. 아키텍처 및 핵심 원리

| JOIN | NULL 가능 | 행 수 |
|:---|:---|:---|
| **INNER** | 없음 | 매칭만 |
| **LEFT** | 우측 NULL | **좌측 ≤ 결과** |
| **FULL** | 양쪽 NULL | 최대 |
| **CROSS** | 없음 | A×B |

---

## Ⅲ~Ⅴ. 결론

JOIN은 **관계형 DB의 핵심 연산**이며, 적절한 인덱스·JOIN 순서·실행 계획 분석이 성능을 결정한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **INNER JOIN** | 교집합 |
| **LEFT JOIN** | 좌측 전체 보존 |
| **FULL OUTER** | 합집합 |
| **Hash/Nested Loop/Merge** | JOIN 알고리즘 |
| **인덱스** | JOIN 성능 핵심 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Cartesian Product (이론)] → [INNER/OUTER JOIN (SQL-92)]
    → [Lateral Join (SQL:2003)] → [Hash Join 최적화 (2010s)]
    → [현재: Adaptive Join — DB가 런타임에 최적 알고리즘 선택]
```

### 👶 어린이를 위한 3줄 비유 설명
1. INNER JOIN은 **양쪽 모두 참석한 사람만** 명단에 남겨요.
2. LEFT JOIN은 **A반 전체 + B반에서 겹치는 사람**을 포함해요.
3. 겹치지 않는 사람은 **빈칸(NULL)**으로 채워진답니다!