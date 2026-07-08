---
title: "조인 알고리즘 — NLJ·Hash Join·Merge Join (Join Algorithms)"
date: "2026-07-08"
tags:
  - "cspe-software"
weight: 109
extra:
  question_no: "109"
  exam_status: "기출"
  exam_history: "137회"
---

## 미리 알고가기

- 조인 알고리즘은 두 집합을 어떤 순서와 구조로 결합할지 정하는 실행 방식임
- NLJ와 Hash Join과 Merge Join은 I/O와 메모리와 정렬 요구가 다름
- 데이터 크기와 인덱스 존재 여부가 선택의 핵심 기준임

## Ⅰ. 개요

- **정의/개념**: 조인 알고리즘은 두 개 이상의 테이블을 조인 조건으로 결합할 때 어떤 자료 접근 방식과 메모리 구조와 정렬 전략을 사용할지 결정하는 실행 기법으로, 대표적으로 NLJ와 Hash Join과 Merge Join이 활용됨
- **배경/필요성**: 조인은 대부분의 복합 질의에서 비용 비중이 가장 크므로, 데이터 분포와 인덱스와 메모리 여건에 맞는 알고리즘 선택이 성능을 좌우함

## Ⅱ. 특징

- NLJ는 작은 집합이나 인덱스가 있는 경우 유리함
- Hash Join은 대용량 등치 조인에 강함
- Merge Join은 정렬된 입력이나 정렬 결과가 필요한 경우 효율적임
- 잘못된 조인 알고리즘 선택은 CPU와 메모리와 디스크 spill 비용을 동시에 키움

## Ⅲ. 종류 및 비교

| 판단 기준 | NLJ | Hash Join | Merge Join |
|:---|:---|:---|:---|
| 적합 조건 | 작은 outer와 인덱스 존재 | 대용량 등치 조인 | 정렬된 입력 또는 정렬 필요 |
| 강점 | 단순하고 선택적 접근 유리 | 높은 처리량 | 순차 처리와 정렬 결합 유리 |
| 한계 | 대용량에서 느림 | 메모리 부족 시 spill | 선행 정렬 비용 |
| 주요 자원 | 랜덤 I/O | 메모리 | 정렬 I/O |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Outer and Inner Input | 어느 집합을 기준으로 읽을지에 따라 비용이 달라짐 |
| Join Predicate | 등치 조건인지 범위 조건인지가 알고리즘 선택을 좌우함 |
| Memory Buffer | 해시 테이블 구성과 정렬 병합 처리 가능 범위를 결정함 |
| Spill or Lookup Path | 메모리 부족 시 spill이나 인덱스 lookup 비용이 성능 차이를 만듦 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 입력 특성 분석  | --> | 알고리즘 선택   | --> | 조인 수행      | --> | 자원 사용 검증  |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **입력 특성 분석**: 데이터 크기와 정렬 상태와 인덱스를 확인함
2. **알고리즘 선택**: 비용이 낮은 조인 방식을 고름
3. **조인 수행**: 선택된 경로로 레코드를 결합함
4. **자원 사용 검증**: spill과 CPU와 I/O 사용량을 확인함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 입력 크기 추정이 틀리면 옵티마이저가 NLJ를 택해 대용량 조인에서 심각한 지연을 일으킬 수 있음
   - 해결방안: cardinality correction과 plan review를 수행하고 join plan regression count와 worst-query latency로 검증함
2. 문제: Hash Join에 필요한 메모리를 확보하지 못하면 디스크 spill이 발생해 처리량이 급격히 떨어질 수 있음
   - 해결방안: memory grant tuning을 적용하고 spill ratio와 hash join throughput으로 검증함
3. 문제: Merge Join에 필요한 정렬 비용을 무시하면 전체 계획에서 불필요한 sort가 누적될 수 있음
   - 해결방안: sort avoidance index를 설계하고 extra sort count와 merge join efficiency로 검증함

## Ⅶ. 적용 사례

- 복합 주문 조회 SQL에서는 계획 리뷰를 수행하고 확인 지표는 join plan regression count와 worst-query latency임
- 대용량 배치 조인에서는 메모리 할당을 조정하고 확인 지표는 spill ratio와 hash join throughput임
- 정렬 결과가 필요한 리포트 쿼리에서는 sort 회피 인덱스를 설계하고 확인 지표는 extra sort count와 merge join efficiency임

## Ⅷ. 결론

조인 알고리즘 선택은 문법 문제가 아니라 입력 데이터 특성과 메모리 조건을 바탕으로 가장 싼 결합 경로를 고르는 실행 전략임.
