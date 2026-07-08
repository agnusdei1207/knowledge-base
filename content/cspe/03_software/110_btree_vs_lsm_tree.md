---
title: "B-Tree vs LSM-Tree 비교 (B-Tree vs LSM-Tree)"
date: "2026-07-08"
tags:
  - "cspe-software"
weight: 110
extra:
  question_no: "110"
  exam_status: "기출"
  exam_history: "137회"
---

## 미리 알고가기

- B-Tree는 제자리 갱신 중심의 균형 트리 저장 구조임
- LSM-Tree는 순차 쓰기와 병합을 중심으로 한 로그 구조 병합 저장 방식임
- 읽기·쓰기·공간 증폭 특성이 달라 워크로드 적합성이 다름

## Ⅰ. 개요

- **정의/개념**: B-Tree와 LSM-Tree는 키 기반 저장 엔진의 대표 구조로서 B-Tree는 균형 트리에서 제자리 탐색과 갱신을 수행하고, LSM-Tree는 메모리와 디스크 계층에 정렬된 세그먼트를 쌓은 뒤 병합해 쓰기 효율을 높이는 저장 방식임
- **배경/필요성**: 데이터베이스는 읽기와 쓰기 비율과 저장 매체 특성에 따라 병목이 달라지므로, 저장 구조 선택이 전체 성능과 운영 비용을 결정함

## Ⅱ. 특징

- B-Tree는 범위 조회와 point lookup이 안정적이며 읽기 지연 예측이 쉬움
- LSM-Tree는 순차 쓰기와 높은 ingest 처리량에 강함
- B-Tree는 랜덤 쓰기와 페이지 분할 비용이 부담이 될 수 있음
- LSM-Tree는 compaction과 read amplification 관리가 핵심 운영 과제임

## Ⅲ. 종류 및 비교

| 판단 기준 | B-Tree | LSM-Tree |
|:---|:---|:---|
| 쓰기 특성 | 제자리 갱신 | 순차 기록 후 병합 |
| 읽기 특성 | 안정적 lookup과 범위 조회 | point lookup은 보조 구조 의존 |
| 운영 부담 | 분할·조각화 관리 | compaction·증폭 관리 |
| 적합 워크로드 | 읽기 균형형 OLTP | 쓰기 집약형 로그·시계열 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Balanced Node or SSTable | B-Tree 노드와 LSM의 SSTable이 각각 저장 단위를 형성함 |
| Write Path | B-Tree는 페이지 갱신을, LSM은 memtable과 flush를 중심으로 처리함 |
| Read Path | B-Tree는 트리 탐색을, LSM은 여러 레벨과 Bloom Filter 확인을 수행함 |
| Maintenance Flow | B-Tree는 split과 rebalance를, LSM은 compaction을 통해 구조를 유지함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 워크로드 분석   | --> | 저장 구조 선택  | --> | 쓰기/읽기 운영  | --> | 증폭 비용 검증  |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **워크로드 분석**: 읽기·쓰기 비율과 범위 조회 빈도를 확인함
2. **저장 구조 선택**: B-Tree 또는 LSM-Tree를 고름
3. **쓰기와 읽기 운영**: 각 구조의 경로에 맞춰 튜닝함
4. **증폭 비용 검증**: read와 write와 space amplification을 측정함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 쓰기 집약 업무에 B-Tree를 그대로 적용하면 랜덤 I/O와 페이지 분할 비용이 누적되어 처리량이 제한될 수 있음
   - 해결방안: write-heavy workload는 LSM 계열을 검토하고 page split rate와 write throughput으로 검증함
2. 문제: 읽기 지연 민감 업무에 LSM-Tree를 도입하면서 compaction과 다중 레벨 조회를 관리하지 않으면 tail latency가 커질 수 있음
   - 해결방안: Bloom Filter와 compaction policy를 최적화하고 read amplification과 p99 latency로 검증함
3. 문제: 저장 구조별 증폭 비용을 측정하지 않으면 초기 성능 수치만 보고 장기 운영비를 과소평가할 수 있음
   - 해결방안: amplification budget을 관리하고 write amplification과 storage overhead ratio로 검증함

## Ⅶ. 적용 사례

- 로그 수집 플랫폼에서는 LSM 계열을 검토하고 확인 지표는 page split rate와 write throughput임
- 사용자 조회 중심 서비스에서는 LSM 읽기 경로를 튜닝하고 확인 지표는 read amplification와 p99 latency임
- 저장 엔진 평가 조직에서는 증폭 예산을 관리하고 확인 지표는 write amplification와 storage overhead ratio임

## Ⅷ. 결론

B-Tree와 LSM-Tree 선택의 기준은 유행이 아니라 읽기 지연 안정성과 쓰기 처리량 중 무엇을 더 우선하는지에 달려 있음.
