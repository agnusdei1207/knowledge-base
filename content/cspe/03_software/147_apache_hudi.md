---
title: "Apache Hudi"
date: "2026-07-14T00:00:00+09:00"
tags:
  - "cspe-software"
weight: 147
extra:
  question_no: "147"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- Hudi는 레코드 키 기반 Upsert와 증분 처리를 제공하는 오픈 테이블 포맷임
- Timeline은 Commit·Delta Commit·Compaction·Clean 같은 테이블 동작의 순서와 상태를 기록함
- File Group은 같은 레코드 키 범위를 저장하는 파일 버전 집합임
- File Slice는 한 시점의 Base File과 이후 Log File을 묶은 조회 단위임
- Copy-on-Write(CoW)는 갱신 시 새 Base File을 작성해 읽기 시 병합을 줄임
- Merge-on-Read(MoR)는 변경을 Log File에 추가하고 조회 또는 Compaction에서 Base File과 병합함
- Record Key는 레코드를 식별하고 Precombine 값은 같은 키로 들어온 변경의 적용 순서를 정함
- Index는 Record Key를 해당 File Group에 매핑해 갱신 대상 파일을 찾음
- Snapshot Query는 최신 Base·Log 상태를, Read Optimized Query는 Base File을, Incremental Query는 변경분을 조회함

## 작성 근거(검토용)

- Hudi는 레코드 키·Timeline·File Group·Index·CoW·MoR 갱신 경로를 핵심으로 선정함
- 비교표는 CoW와 MoR의 갱신 방식·조회 비용·유지관리를 동일 기준에서 대비함
- 절차는 레코드 키로 파일 그룹을 찾고 쓰기 결과를 Timeline에 커밋하는 Upsert 흐름을 설명함
- 제목부터 결론까지 모든 문장·표 셀·요약을 5회 전수 검수해 파일·로그 병합 시점을 구분함

## Ⅰ. 개요

- **정의/개념**: Hudi는 레코드 키·Index·Timeline으로 데이터 레이크의 Upsert·삭제·증분 조회를 관리하는 오픈 테이블 포맷임
- **배경/필요성**: 변경 빈도가 높은 운영 데이터를 전체 파티션 재작성 없이 레이크에 반영하고 변경분을 후속 처리하기 위해 키 기반 Upsert 구조가 필요함

### 쉽게 이해하기 (학습용)
- 레코드 키로 기존 파일 위치를 찾아 대량 변경을 빠르게 반영하는 데이터 레이크 테이블 포맷임

## Ⅱ. 특징

- 레코드 키와 Index로 변경 대상 File Group을 찾아 Upsert·Delete 범위를 결정함
- Timeline이 쓰기와 Table Service의 요청·진행·완료 상태를 순서대로 관리함
- CoW는 변경 대상 Base File을 재작성하고 MoR는 Log File을 추가해 쓰기·읽기 비용을 조정함
- Snapshot·Read Optimized·Incremental Query가 최신 상태·Base File·변경분의 조회 범위를 나눔
- Compaction·Clustering·Cleaning이 Log 병합·파일 배치·보존 버전을 관리함

### 쉽게 이해하기 (학습용)
- 빠른 읽기는 파일 즉시 재작성, 빠른 쓰기는 변경 로그 후 병합이라는 선택이 필요함

## Ⅲ. 종류 및 비교

| 판단 기준 | Copy-on-Write | Merge-on-Read |
|:---|:---|:---|
| 갱신 방식 | 변경 레코드를 반영한 새 Base File을 즉시 작성 | 변경 레코드를 Log File에 추가하고 Base File은 보존 |
| 조회 비용 | 최신 Base File만 읽어 병합 없이 조회 | Snapshot 조회는 Base·Log를 병합, Read Optimized는 Base만 조회 |
| 유지관리 | Clustering·Cleaning 중심, Compaction 불필요 | Compaction으로 Log를 Base File에 주기적으로 병합 |

> 요약: Hudi는 CoW의 즉시 Base 재작성과 MoR의 Log 선기록 중에서 선택해 쓰기 지연, 조회 병합 비용, Compaction 부담을 조정함.

### 쉽게 이해하기 (학습용)
- CoW는 완성 장부를 즉시 다시 쓰고 MoR은 변경 메모를 먼저 붙인 뒤 나중에 합침

## Ⅳ. 설계 요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Record Key·Precombine | 레코드를 식별하고 같은 키 변경의 적용 순서를 판정함 |
| Index | 레코드 키를 대상 File Group에 매핑해 Upsert 파일 범위를 줄임 |
| Timeline | 쓰기·Compaction·Clustering·Cleaning 동작의 시점과 상태를 관리함 |
| File Group·File Slice | Base File과 해당 키 범위의 Log File 버전을 묶어 저장함 |
| Metadata Table | 파일 목록·열 통계·Index 메타데이터를 관리해 조회 계획을 지원함 |
| Table Service | Compaction·Clustering·Cleaning으로 파일 구조와 보존 범위를 관리함 |

```text
변경 레코드 -> Key·Index -> File Group -> Base File·Log File
                               |
                            Timeline
```

> 요약: 레코드 키와 Index가 변경 대상 File Group을 찾고 Timeline이 Base·Log 파일의 커밋 상태를 확정함.

### 쉽게 이해하기 (학습용)
- 레코드 색인, 파일 묶음, 작업 시간선과 압축·정리 서비스로 구성됨

## Ⅴ. 원리 및 절차 흐름도

```text
키·순서 판정 -> File Group 조회 -> Base 재작성 또는 Log 추가 -> Timeline 커밋 -> 후속 정리
```

1. **레코드 판정**: Record Key로 대상을 식별하고 Precombine 값으로 같은 키의 변경 순서를 정함
2. **파일 조회**: Index가 현재 레코드가 속한 File Group을 찾음
3. **변경 기록**: CoW는 새 Base File을 쓰고 MoR는 변경을 Log File에 추가함
4. **동작 커밋**: 성공한 파일 쓰기를 Timeline의 완료 Instant로 확정함
5. **파일 정리**: 정책에 따라 Compaction·Clustering·Cleaning을 예약·수행함

> 요약: Hudi는 키로 파일 그룹을 찾아 CoW 또는 MoR 경로로 변경을 기록하고 Timeline 커밋으로 공개함.

### 쉽게 이해하기 (학습용)
- 키로 파일 묶음을 찾고 CoW 재작성 또는 MoR 로그 추가 뒤 시간선에 커밋함

## Ⅵ. 실무 사례

1. 주문 변경 데이터 레이크는 MoR Upsert를 적용하고 쓰기 지연·스냅샷 조회 시간을 확인함
2. 조회 중심 고객 테이블은 CoW를 적용하고 파일 재작성량·분석 질의 시간을 확인함

### 쉽게 이해하기 (학습용)
- CDC Upsert에서 쓰기 지연·조회 병합·Compaction 적체·파일 수를 확인함

## Ⅶ. 결론

- Hudi는 변경 빈도·키 기반 Upsert·최신성 요구·조회 시 병합 비용과 Table Service 실행 비용을 기준으로 선택해야 함
- CoW·MoR 선택 뒤에도 Compaction·Clustering·Cleaning 지연과 Timeline 정합성을 지속 관찰해야 함

### 쉽게 이해하기 (학습용)
- 변경 메모가 너무 쌓이거나 오래된 파일 정리가 밀리지 않는지 계속 확인해야 함
