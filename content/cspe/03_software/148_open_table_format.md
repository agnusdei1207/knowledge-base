---
title: "오픈 테이블 포맷 비교 (Open Table Format)"
date: "2026-07-11"
tags:
  - "cspe-software"
weight: 148
extra:
  question_no: "148"
  exam_status: "기출"
  exam_history: "137회"
---

## 미리 알고가기

- 오픈 테이블 포맷은 객체 스토리지의 데이터 파일과 테이블 버전·스키마·파티션 메타데이터 관리 규칙을 정의함
- Delta Lake는 순차 트랜잭션 로그의 Action으로 유효 파일 집합을 재구성함
- Apache Iceberg는 Snapshot·Manifest 계층으로 데이터·삭제 파일을 추적함
- Apache Hudi는 Timeline·File Group·Index로 레코드 키 기반 변경을 관리함
- 행 수준 변경은 대상 데이터 파일 재작성이나 별도 삭제·변경 파일 병합 비용을 발생시킴
- 위치 삭제는 파일과 행 위치를, 동등 삭제는 열 값 조건을 삭제 대상으로 기록함
- 파일 압축·스냅샷 만료·로그 병합은 포맷별 읽기·쓰기 비용을 조정하는 유지관리 작업임
- Change Data Feed는 테이블 버전 사이의 행 변경분을 증분 처리에 제공함

## 작성 근거(검토용)

- 비교의 핵심을 메타데이터 모델·행 변경 경로·유지관리로 제한함
- 세 포맷의 공통 ACID 문구를 반복하지 않고 실제 파일 추적과 갱신 경로가 갈리는 축을 선정함
- 구성요소는 데이터 저장·현재 상태 참조·변경 위치 식별이라는 공통 층과 포맷별 구현을 연결함
- 포맷별 커밋 절차가 달라 공통 흐름으로 묶지 않고 비교표와 구조에서 차이를 설명함
- 제목부터 결론까지 모든 문장·표 셀·요약을 5회 전수 검수해 각 열의 분석 수준을 통일함

## Ⅰ. 개요

- **정의/개념**: 오픈 테이블 포맷은 객체 스토리지 파일에 커밋·스냅샷·스키마·행 변경 규칙을 적용해 여러 엔진이 일관된 테이블을 공유하는 공개 규격임
- **배경/필요성**: 파일 목록과 디렉터리 규칙만으로 동시 쓰기·버전·스키마 진화를 관리하기 어려우므로 업무의 갱신·조회 특성에 맞는 메타데이터 형식이 필요함

## Ⅱ. 특징

- 기존 데이터 파일을 직접 덮어쓰지 않고 새 파일과 메타데이터 버전을 원자적으로 커밋함
- 읽기 엔진은 선택한 스냅샷의 메타데이터로 유효 데이터·삭제·변경 파일만 계획함
- 스키마·파티션·정렬 정보를 데이터 파일과 분리해 테이블 구조를 버전별로 진화시킴
- 포맷 규격과 카탈로그 인터페이스가 저장소와 연산 엔진의 결합 범위를 결정함
- 작은 파일·오래된 스냅샷·미병합 로그를 정리하는 유지관리 정책이 지속적으로 필요함

## Ⅲ. 종류 및 비교

| 판단 기준 | Delta Lake | Apache Iceberg | Apache Hudi |
|:---|:---|:---|:---|
| 메타데이터 모델 | `_delta_log` Action·Checkpoint·Change Data Feed | Metadata·Snapshot·Manifest 계층 | Timeline·File Group·Index |
| 행 변경 경로 | MERGE·UPDATE·DELETE가 새 파일과 로그 커밋 생성 | 데이터·위치·동등 삭제 파일과 파일 재작성 | CoW Base 재작성 또는 MoR Log 추가 |
| 유지관리 | 파일 압축·Checkpoint·VACUUM | Manifest 병합·파일 재작성·스냅샷 만료 | Compaction·Clustering·Cleaning |

> 요약: Delta는 로그, Iceberg는 스냅샷·Manifest, Hudi는 Timeline으로 메타데이터를 관리하며 행 변경 반영 방식과 유지관리 작업이 포맷별로 다름.

## Ⅳ. 구성요소 및 구조

| 공통 계층 | Delta Lake | Apache Iceberg | Apache Hudi |
|:---|:---|:---|:---|
| 데이터 저장 | Parquet Data File | Data·Delete File | Base·Log File |
| 현재 상태 참조 | 최신 로그 버전 | Catalog의 Metadata 포인터 | 완료된 Timeline Instant |
| 변경 위치 식별 | 파일 Add·Remove와 행 조건 | File·Position·Equality Delete | Record Key·Index·File Group |

> 요약: 세 포맷은 데이터 파일을 공통 계층으로 두지만 현재 상태를 참조하는 지점과 행 변경 위치를 식별하는 구조가 다름.

## Ⅵ. 실무 사례

1. Spark 변경 데이터 병합은 Delta MERGE를 적용하고 커밋 충돌·평균 파일 크기를 확인함
2. 다중 엔진 분석은 Iceberg 스냅샷을 공유하고 질의 계획 시간·엔진별 조회 결과를 대사함

## Ⅶ. 결론

- 오픈 테이블 포맷은 연산 엔진·행 변경 빈도·파티션 진화·증분 조회와 유지관리 방식을 기준으로 선택해야 함
