---
title: 뷰 View 및 인덱스 Index (DB View and Index)
date: 2026-07-05
tags: ["cspe-software"]
weight: 176
---

## Ⅰ. 개요
- 정의: 물리적 테이블을 기반으로 한 가상 테이블(View)과 검색 속도 향상을 위한 데이터 구조(Index)
- 배경: 데이터 보안/편의성 제공 및 대용량 데이터 탐색 성능 한계 극복
| 구분 | 내용 |
|------|------|
| 출제 의도 | View의 보안 효과와 Index의 구조(B-Tree, Bitmap) 및 생성 전략 파악 |

## Ⅱ. 구성요소
  [ Index Tree ] -> [ Pointer ] -> [ Table Data ]
  [ View Definition ] -> [ Base Table Query ]
| 구성요소 | 설명 | 비유 |
|----------|------|------|
| View | 하나 이상의 테이블에서 유도된 가상 테이블 | 돋보기 |
| B-Tree Index | 균형 트리 구조의 일반적인 인덱스 | 색인 사전 |
| Bitmap Index | 비트맵 열로 구성된 인덱스(낮은 카디널리티) | 체크 박스 |
> 요약: 추상화를 통한 보안성과 구조화를 통한 성능의 조화

## Ⅲ. 절차
  Request -> Check Index -> Access Row -> (Apply View Rule)
1. Scanning: 인덱스 존재 여부 및 선택도(Selectivity) 판단
2. Traversal: 인덱스 트리를 탐색하여 대상 주소(RID) 획득
3. Retrieval: 획득한 주소로 실제 테이블 데이터 블록 접근
4. Mapping: 뷰 정의에 따라 필요한 컬럼만 필터링하여 노출
> 요약: 효율적 경로 탐색과 논리적 노출 제어를 통한 데이터 서비스

## Ⅳ. 문제점
- 과도한 인덱스 생성 시 CUD(수정) 성능 저하 및 저장공간 낭비
- View 중첩 사용 시 쿼리 복잡도 증가 및 성능 최적화의 난해함

## Ⅴ. 개선방안
- 사용 빈도가 높은 조건 위주로 인덱스 선별 및 정기적 재구성
- Materialized View(구체화 뷰) 도입으로 복잡한 연산 결과 캐싱

## Ⅵ. 전망
- AI 기반 자동 인덱스 추천 및 실시간 변경 부하를 최소화하는 컬럼형 인덱스 기술 고도화
