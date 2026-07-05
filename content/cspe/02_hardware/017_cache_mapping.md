---
title: 캐시 매핑 — Direct·Full·Set Associative (Cache Mapping)
date: 2026-07-05
tags: ["cspe-hardware"]
weight: 17
---

## Ⅰ. 개요
- 정의: 주메모리의 데이터를 캐시 메모리의 어느 위치에 저장할지 결정하는 규칙
- 배경: 고가인 캐시의 한정된 공간을 효율적으로 활용하여 적중률(Hit Rate) 극대화 필요
- 출제 의도: 매핑 방식에 따른 캐시 적중률, 구현 복잡도, 탐색 시간의 트레이드오프 이해

## Ⅱ. 구성요소
- ASCII 구조도
  [Direct]        [Full]            [Set-Associative]
  Mem A -> Line X  Mem A -> Any Line  Mem A -> Set Y (Any Line in Set)
  (1:1 Fixed)      (Anywhere)        (Grouped Anywhere)

- 구성요소 표
| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| Direct Mapping | 주소의 인덱스 필드가 가리키는 고정 위치에 저장 | 지정석 |
| Fully Assoc. | 캐시의 빈 공간 어디든 저장 가능 | 자유석 |
| Set Assoc. | 여러 개의 라인을 하나의 세트로 묶어 그 중 선택 | 구역 지정석 |
> 요약: Direct는 단순하지만 충돌이 잦고, Full은 유연하지만 탐색이 무거움

## Ⅲ. 절차
- ASCII 흐름도
  (Memory Address) -> (Extract Tag/Index) -> (Check Valid Bit) -> (Compare Tag)
                                                                    |
                       +--------- (Hit: Data Out) <--- (Miss: Fetch from Mem)

- 4단계 설명
1. 주소 분해: CPU가 요청한 주소를 태그, 인덱스(Set 필드), 오프셋으로 분리
2. 세트 선택: 인덱스 정보를 활용하여 캐시 내 대상 세트(혹은 라인) 접근
3. 태그 비교: 선택된 영역 내의 모든 라인 태그와 요청 주소 태그를 동시 비교
4. 데이터 인출: 일치하는 태그가 있고 Valid bit가 1이면 데이터를 CPU로 전달
> 요약: 인덱스로 범위를 좁히고 태그로 최종 데이터를 확인하는 절차임

## Ⅳ. 문제점
- Thrashing (Direct): 동일 인덱스로 매핑되는 서로 다른 데이터가 반복 교체되며 적중률 급감
- 하드웨어 비용 (Full): 모든 라인을 동시에 비교하기 위한 고가의 비교기(Comparator) 필요

## Ⅴ. 개선방안
- (단기) N-way Set Associative: Direct와 Full의 장점을 절충 (현대 CPU 표준)
- (중기) Victim Cache: 캐시에서 방출된 데이터를 임시 보관하여 충돌 미스 완화
- (장기) Way Prediction: 접근 가능성이 높은 Way를 미리 예측하여 전력 및 지연 단축

## Ⅵ. 전망
- 로드맵: L1/L2는 저지연 위주의 낮은 Associativity, L3는 고적중 위주의 높은 방식 적용
- CSF: 데이터 접근 패턴(Spatial/Temporal Locality)에 최적화된 동적 매핑 기술 확보
