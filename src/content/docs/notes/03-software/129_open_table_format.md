---
sidebar:
  order: 129
  label: "129. 오픈 테이블 포맷 비교"
  badge:
    text: "기출 · 50%"
    variant: note
title: "오픈 테이블 포맷 비교 (Open Table Format)"
date: "2026-09-07T10:05:00+09:00"
tags:
  - "notes-software"
weight: 129
extra:
  question_no: "129"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "137회 기출, 세 오픈 포맷 선택 기준"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **오픈 테이블 포맷(Open Table Format)**: S3/GCS 등의 불변 Parquet 파일 상에서 ACID 트랜잭션, 타임 트래블, 스키마 진화를 지원하는 메타데이터 계층 표준.
- **3대 대표 기술**: Delta Lake(Databricks/Spark), Apache Iceberg(Apache/다중엔진), Apache Hudi(Uber/스트리밍).

</details>

- 정의/개념: 객체 스토리지 파일 상에서 ACID 트랜잭션, 타임트래블, 스키마 진화를 제공하는 Delta Lake, Apache **Iceberg**, Apache **Hudi** 3대 오픈 메타데이터 표준
- 배경/필요성: 디렉터리 기반 파티셔닝의 **O(N) 파일 리스팅 지연, 부분 쓰기 실패 시 롤백 불가 및 동시 쓰기 데이터 오염 한계**

#### 한줄 요약
- 오픈 테이블 포맷의 가치는 개별 기능이 아니라 표준을 공유해 엔진을 갈아 끼울 수 있게 하는 데 있으므로, 특정 엔진에 깊게 최적화될수록 그 중립성이라는 본래 이득이 줄어든다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **OCC(Optimistic Concurrency Control)**: 락 잠금 없이 각자 작업을 수행한 뒤 커밋 시점에 충돌을 검증하는 낙관적 동시성 제어.
- **Copy-on-Write vs Merge-on-Read**: 수정 시 파일 전체를 새로 쓰는 읽기 최적화 CoW와 변경 델타만 기록하고 읽을 때 합치는 쓰기 최적화 MoR.

</details>

- 객체 스토리지 기반의 100% ACID 트랜잭션 및 스냅샷 격리 보장
- 과거 특정 시점의 데이터 상태를 쿼리하고 원복하는 타임 트래블(Time Travel) 지원
- Spark, Trino, Presto, Flink 등 다양한 연산 엔진이 단일 테이블을 직접 공유(Engine-Agnostic)

#### 한줄 요약
- 오픈 메타데이터 표준을 통해 레이크의 경제성과 DW의 신뢰성을 동시에 확보한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **오픈 테이블 포맷 3계층**: Engine Layer(다중 분석 엔진), Metadata Layer(포맷별 메타데이터 트리), Storage Layer(객체 스토리지 불변 파일).

</details>

```text
[오픈 테이블 포맷 아키텍처]
├─ [카탈로그 계층 (Catalog)]
│  └─ REST / Glue (최신 메타 포인터)
├─ [메타데이터 계층 (Metadata)]
│  ├─ 스냅샷 및 스키마 진화 관리
│  └─ 파일별 통계 (Min/Max Skipping)
├─ [물리 데이터 계층 (Data Files)]
│  └─ 불변 Parquet / ORC 데이터 파일
└─ [삭제 처리 계층 (Delete Files)]
   ├─ CoW (Copy-on-Write 재기록)
   └─ MoR (Merge-on-Read 델타 병합)
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 | 주요 특징 |
|:---|:---|:---|
| 카탈로그 (Catalog) | 테이블 식별자와 현재 유효한 최신 메타데이터 파일 위치를 원자적 관리 | Glue, REST Catalog |
| 메타데이터 계층 | 스냅샷 버전, 스키마, 파티션 스펙, 파일별 Min/Max 통계 정보를 구조화 관리 | JSON / AVRO 트리 |
| 데이터 파일 (Data File) | 실제 비즈니스 레코드를 저장하는 불변(Immutable) Parquet/ORC 압축 파일 | 열 지향 포맷 |
| 삭제 파일 (Delete File) | MoR 모드에서 수정/삭제된 레코드의 위치 및 동등 조건을 별도 저장 | Positional/Equality Delete |

#### 한줄 요약
- 세 포맷 모두 불변 데이터 파일과 그것을 가리키는 메타데이터라는 같은 골격을 쓰므로, 차이는 저장 방식이 아니라 삭제와 갱신을 쓰기 시점에 반영할지 읽기 시점에 합칠지에서 갈린다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **오픈 테이블 트랜잭션 5단계**: 스냅샷 조회 $\to$ 불변 파일 쓰기 $\to$ 메타데이터 작성 $\to$ OCC 충돌 검증 $\to$ 카탈로그 포인터 갱신.

</details>

```text
다중 엔진에서 오픈 테이블 포맷으로 쓰기 트랜잭션 요청
        │
   [스냅샷 조회] 쓰기 엔진이 카탈로그를 참조하여 현재 유효한 최신 스냅샷 버전 확인
        │
   [불변 파일 기록] 변경된 레코드를 새로운 불변 Parquet 파일로 객체 스토리지에 기록
        │
   [메타데이터 생성] 신규 파일 경로 및 통계 정보를 담은 메타데이터(JSON/AVRO) 작성
        │
   [OCC 충돌 검증] 쓰기 도중 타 트랜잭션의 동일 파티션 변경 여부 검증 (충돌 시 자동 재시도)
        │
   [포인터 원자 갱신] 카탈로그의 최신 테이블 포인터를 신규 메타데이터로 원자적 교체 공개
```

#### 한줄 요약
- 낙관적 동시성 제어는 충돌이 드물다는 가정 위에서 잠금 비용을 없애므로, 같은 파티션에 쓰기가 몰리는 워크로드에서는 재시도가 반복되며 그 이득이 사라진다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Delta vs Iceberg vs Hudi**: Spark 최적화(Delta), 다중 엔진 중립 표준(Iceberg), 초저지연 스트리밍 CDC(Hudi).

</details>

| 비교 항목 | Delta Lake (Databricks) | Apache Iceberg (Apache 재단) | Apache Hudi (Uber) |
|:---|:---|:---|:---|
| 핵심 메타데이터 | JSON Log + Checkpoint Parquet | 3계층 AVRO Manifest 트리 | Timeline Commit Log (AVRO) |
| 파티셔닝 유연성 | 물리 디렉터리 경로 매핑 의존 | Hidden Partitioning (완전 가상화) | 디렉터리 경로 매핑 의존 |
| 최적 연동 생태계 | Apache Spark 및 Databricks 플랫폼| Trino, Snowflake, Flink, Spark 등 | Apache Flink / Spark CDC 스트리밍|
| 갱신 처리 모델 | Copy-on-Write (CoW) 중심 | CoW / Merge-on-Read (MoR) 지원 | **Merge-on-Read** (MoR) 초고속 쓰기 |

#### 한줄 요약
- Spark 중심은 Delta Lake, 다중 엔진 중립성은 Iceberg, 실시간 CDC 스트리밍은 Hudi를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Compaction & Vacuum**: 자잘한 파일을 512MB 표준 크기로 병합하고 보존 주기가 지난 과거 스냅샷 파일을 영구 삭제하는 공통 유지보수.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 스트리밍 인서트로 인한 Small Files 누적으로 쿼리 지연 | 정기적인 백그라운드 `Compaction` (Bin-packing) 배치 실행 | 파일 크기 512MB 표준화 및 스캔 속도 5배 향상 |
| 타임 트래블 구버전 파일 누적으로 인한 S3 비용 폭증 | 보존 기간(7일) 기준 `VACUUM` / `Expire Snapshots` 자동화 | 미사용 불변 파일 삭제 및 스토리지 비용 절감 |
| MoR 삭제 파일 누적으로 읽기 시점 조인 오버헤드 증가 | 주기적인 CoW 변환 및 데이터 파일 Rewrite 작업 수행 | 읽기 성능 저하 해소 |
| 이종 엔진 간 메타데이터 동기화 불일치 | REST Catalog 표준 채택 및 UniForm 메타데이터 자동 변환 | 멀티 엔진 간 무결점 상호 운용성 확보 |

#### 한줄 요약
- 정기 컴팩션, 스냅샷 만료 자동화, 파일 재작성, REST Catalog로 오픈 테이블 포맷을 최적화한다.

## Ⅶ. 결론

- 모던 데이터 스택 및 클라우드 레이크하우스 아키텍처의 **가장 핵심적인 기반 영속성 표준 계층**으로 확립되었으며, 실무 도입 시에는 **완전한 다중 엔진 중립성과 가상 파티셔닝이 필요한 엔터프라이즈 DW 환경에는 Apache Iceberg, Databricks/Spark 중심 배치 환경에는 Delta Lake(UniForm 연계), 초저지연 스트리밍 CDC/UPSERT 환경에는 Apache Hudi(MoR)를 선정하고, 정기 파일 컴팩션 및 REST Catalog 표준화**를 결합하여 데이터 아키텍처의 유연성과 처리 성능을 동시 보증

#### 한줄 요약
- 오픈 테이블 포맷은 객체 스토리지 상에서 ACID 트랜잭션과 엔진 독립성을 보장하여 데이터 레이크하우스의 성공을 견인하는 핵심 메타데이터 기술이다.
