---
title: "Data Lakehouse 데이터 레이크하우스 (Data Lakehouse)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 303
extra:
  question_no: "303"
  exam_status: "기출"
  exam_history: "137회"
  exam_note: "전망"
---

## 미리 알고가기

- Data Lake는 저비용 대용량 저장에 강하지만 정합성과 거버넌스 기능이 약한 편임
- Data Warehouse는 관리와 성능은 좋지만 스토리지와 엔진 종속성이 강하고 비용이 큼
- Lakehouse는 오브젝트 스토리지 위에 테이블 메타데이터 계층을 두어 두 성격을 결합함

## Ⅰ. 개요

- **정의/개념**: Data Lakehouse는 데이터 레이크의 유연한 저장 구조 위에 ACID 트랜잭션과 스키마 관리와 카탈로그와 고성능 분석 기능을 더해 데이터 웨어하우스급 신뢰성과 레이크의 확장성을 함께 제공하는 데이터 아키텍처임
- **배경/필요성**: 기업이 레이크와 웨어하우스를 이중 운영하면서 데이터 복제와 비용과 지연이 커져 하나의 저장 기반에서 분석과 머신러닝과 운영 데이터를 함께 다루는 구조가 필요해짐

## Ⅱ. 특징

- 스토리지와 컴퓨트 분리를 유지하면서도 테이블 단위 정합성과 버전 관리를 제공함
- 배치와 스트리밍과 BI와 ML 워크로드를 같은 데이터 기반에서 처리하기 좋음
- 오픈 테이블 포맷과 카탈로그가 핵심이어서 멀티엔진 상호운용성이 중요한 판단 기준이 됨
- 작은 파일 누적과 메타데이터 관리가 성능을 좌우하므로 운영 자동화가 필수임

## Ⅲ. 종류 및 비교

| 판단 기준 | Data Lake | Data Warehouse | Data Lakehouse |
|:---|:---|:---|:---|
| 저장 구조 | 파일 중심 | 테이블 중심 | 파일 기반 테이블 관리 |
| 정합성 | 상대적으로 약함 | 강함 | 강함 |
| 워크로드 유연성 | 높음 | 중간 | 높음 |
| 비용 구조 | 낮음 | 높음 | 중간 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Object Storage Layer | 대용량 정형과 비정형 데이터를 저비용으로 저장해 lakehouse의 물리적 기반을 제공하는 저장 계층임 |
| Open Table Format | 스냅샷과 트랜잭션과 스키마 진화를 관리해 파일 집합을 신뢰 가능한 테이블로 바꾸는 메타데이터 계층임 |
| Catalog and Metadata Service | 테이블 위치와 권한과 스키마를 관리해 여러 엔진이 같은 논리 구조를 공유하도록 만드는 공통 참조 계층임 |
| Multi Engine Compute | SQL 엔진과 Spark와 ML 엔진이 동일 데이터셋을 활용하게 해 분석과 처리 방식을 유연하게 만드는 실행 계층임 |
| Governance and Optimization | 품질 규칙과 접근 제어와 compaction과 lifecycle 관리를 수행해 운영 안정성과 비용 효율을 유지하는 관리 계층임 |

```text
+---------------+
| Compute Engine|
+---------------+
        |
        v
+---------------+
| Catalog / OTF |
+---------------+
        |
        v
+---------------+
| Object Storage|
+---------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 데이터 적재   | -> | 테이블화     | -> | 카탈로그 등록 | -> | 멀티엔진 조회 | -> | 최적화/거버넌스 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **데이터 적재**: 원천 데이터를 오브젝트 스토리지에 저장함
2. **테이블화**: 오픈 테이블 포맷으로 스냅샷과 스키마를 관리함
3. **카탈로그 등록**: 메타데이터와 권한을 중앙 카탈로그에 반영함
4. **멀티엔진 조회**: BI와 배치와 ML 엔진이 동일 데이터를 활용함
5. **최적화와 거버넌스**: compaction과 품질 검증과 비용 관리를 지속 수행함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 엔진과 포맷 호환성이 맞지 않으면 같은 데이터를 두고도 읽기 결과와 기능 수준이 달라져 멀티엔진 장점이 약화될 수 있음
   - 해결방안: certified engine matrix와 compatibility regression test를 적용하고 cross engine query parity rate와 unsupported feature incident count로 검증함
2. 문제: 작은 파일과 잦은 업데이트가 누적되면 메타데이터 탐색 비용이 커져 쿼리 성능과 운영 효율이 급격히 떨어질 수 있음
   - 해결방안: compaction automation과 write pattern governance를 적용하고 average file size와 metadata scan latency로 검증함
3. 문제: 레이크 중심 문화가 강하면 품질 규칙과 권한 통제가 느슨해져 데이터 웨어하우스 수준의 신뢰성을 확보하기 어려워질 수 있음
   - 해결방안: catalog centric governance와 data quality contract를 적용하고 governed table coverage와 failed quality check rate로 검증함

## Ⅶ. 적용 사례

- 엔터프라이즈 분석 플랫폼이 엔진 호환성 인증 체계를 운영하며 확인 지표는 cross engine query parity rate와 unsupported feature incident count임
- 대규모 로그 레이크가 compaction 자동화를 적용하며 확인 지표는 average file size와 metadata scan latency임
- 금융 데이터 조직이 카탈로그 중심 통제를 강화하며 확인 지표는 governed table coverage와 failed quality check rate임

## Ⅷ. 결론

Data Lakehouse는 저장 통합만으로 완성되지 않으므로 오픈 테이블 포맷과 카탈로그 거버넌스를 함께 운영할 때 비로소 레이크와 웨어하우스의 장점을 회수할 수 있음.
