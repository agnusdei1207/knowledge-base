---
title: 데이터 독립성 — 물리적·논리적 (Data Independence)
date: 2026-07-05
tags: ["cspe-software"]
weight: 183
---

## Ⅰ. 개요
- 정의: 하위 단계의 데이터 구조가 변경되어도 상위 단계의 스키마나 응용 프로그램에 영향을 주지 않는 성질
- 배경: 데이터 관리 효율성 향상 및 응용 프로그램의 유지보수성 확보
| 구분 | 내용 |
|------|------|
| 출제 의도 | 논리적 독립성과 물리적 독립성의 차이와 3단계 스키마 구조와의 관계 이해 |

## Ⅱ. 구성요소
  [ Application ]
        | (Logical Independence)
  [ Conceptual Schema ]
        | (Physical Independence)
  [ Internal Schema ]
| 구성요소 | 설명 | 비유 |
|----------|------|------|
| Logical Indep | 개념 스키마 변경 시 외부 스키마 영향 없음 | 인터페이스 |
| Physical Indep | 저장 구조 변경 시 개념 스키마 영향 없음 | 케이스 교체 |
| Mapping | 각 단계 간의 대응 관계 정의 정보 | 통역사 |
> 요약: 계층 간 결합도를 낮추어 유연한 데이터 관리를 지원하는 구조

## Ⅲ. 절차
  Storage Change -> Update Mapping -> No App Change
1. Modification: 인덱스 추가 또는 파일 시스템 변경(물리 단계)
2. Mapping Update: 내부-개념 간 매핑 정보를 DBMS가 자동 갱신
3. Transparency: 응용 프로그램은 동일한 논리 질의 사용
4. Maintenance: 프로그램 수정 없이 시스템 성능/구조 개선
> 요약: 매핑 레이어를 통한 하위 단계 변경의 상위 단계 격리

## Ⅳ. 문제점
- 계층 간 매핑(Transformation) 오버헤드로 인한 미세한 성능 손실
- 데이터 구조가 급격히 변할 경우 완전한 독립성 유지의 한계

## Ⅴ. 개선방안
- DBMS의 최적화된 매핑 엔진 및 데이터 사전을 통한 관리
- 데이터 모델링 단계에서 유연한 개념 스키마 설계

## Ⅵ. 전망
- NoSQL 및 Schema-less 구조에서의 동적 데이터 독립성 관리 기술 중요성 증대
