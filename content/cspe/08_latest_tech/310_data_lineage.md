---
title: "Data Lineage 데이터 계보 (Data Lineage)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 310
---

# 📖 【암기용】 개념 완전 이해

> 목적: Data Lineage를 데이터가 어디서 와서 어떤 변환을 거쳐 어디에 영향을 주는지 추적하는 metadata 체계로 이해하게 만든다.

## 한눈에
- **개요**: 데이터의 출처, 변환, 이동, 소비처를 추적하는 계보 정보
- **왜 필요한가**: 지표 오류나 schema 변경이 발생했을 때 어떤 원천과 리포트가 영향을 받는지 알아야 복구와 감사가 가능하다.
- **핵심 직관**: 택배 송장처럼 발송지, 경유지, 처리 시각, 수령지를 기록해 문제가 생긴 지점을 찾는 방식임.

## 깊이 이해
- **배경·문제의식**: 데이터 파이프라인이 많아지면 테이블 하나의 변경이 대시보드, ML feature, 정산 보고서에 어떤 영향을 주는지 수동 조사하기 어렵다.
- **작동 원리**: pipeline, SQL, job runtime, catalog metadata를 수집해 dataset, job, run 간 upstream/downstream 관계를 graph로 구성한다.
- **비유**: 식품 유통 이력처럼 생산 농가, 가공 공장, 물류센터, 판매점을 추적하면 오염 발생 시 회수 범위를 좁힐 수 있다.
- **구체 예시**: `customer.email` 컬럼을 마스킹하면 column-level lineage로 해당 컬럼을 쓰는 CRM 리포트와 ML feature pipeline을 찾아 배포 전 영향 분석을 수행한다.
- **흔한 오해·주의점**: Lineage는 ERD가 아니다. ERD는 데이터 구조 관계를, lineage는 데이터가 실제로 이동·변환된 실행 흐름을 보여준다.

## 연결 개념
- OpenLineage — dataset, job, run 기반 lineage 표준
- Data Catalog — lineage 탐색과 영향 분석 UI
- Data Quality — 오류 원인 추적과 품질 규칙 연결

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: Data Lineage는 upstream/downstream graph, column-level lineage, impact analysis, root cause analysis로 답해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Data Lineage는 데이터 자산과 처리 job의 상하류 관계를 기록해 데이터 흐름과 변환 이력을 추적하는 metadata graph임.
> 2. **가치**: schema 변경, 품질 오류, 규제 감사 시 영향 범위와 원인 경로를 lineage graph로 식별함.
> 3. **판단 포인트**: table/column-level lineage, runtime lineage, OpenLineage, impact analysis, freshness가 핵심임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 데이터 거버넌스 이해 확인 | upstream, downstream, transformation | ERD나 데이터 모델로 오해 |
| 장애·품질 대응 판단 확인 | impact analysis, root cause analysis | 시각화 기능만 설명 |
| 표준·자동화 확인 | OpenLineage, job/run/dataset metadata | 수동 문서 관리로 축소 |

> 요약: 이 문제는 lineage를 변경 영향 분석과 품질 오류 추적을 위한 실행 metadata로 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 데이터 흐름 추적 graph
- 배경: 파이프라인과 리포트가 많아지면 특정 테이블·컬럼 변경의 영향 범위를 수동 확인하기 어려움.
- 필요성: 품질 오류, 개인정보 처리, schema 변경, 감사 대응 시 upstream 원인과 downstream 영향을 추적해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Source Dataset -> Job / Transformation -> Target Dataset -> Report / ML
        +-> Run Metadata / SQL Parser
        +-> Catalog / OpenLineage Backend -> Impact Analysis
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Dataset Node | 테이블·파일·토픽 등 데이터 자산 표현 | table/column granularity |
| Job Node | SQL, Spark, Airflow, Flink 처리 작업 표현 | job/run 구분 |
| Edge | 입력·출력·변환 관계 저장 | upstream/downstream |
| Lineage Backend | graph 저장·검색·시각화 제공 | OpenLineage, DataHub |

> 요약: Data Lineage는 dataset, job, run, edge를 graph로 연결해 데이터 이동과 변환 경로를 표현한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
파이프라인 실행 -> SQL / job metadata 수집 -> lineage event 발행
-> graph 저장 -> 영향 분석 / 원인 추적 -> catalog 표시
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | job 실행 시 입력·출력 dataset과 query 수집 | event completeness |
| 2 | column mapping과 transformation 추출 | parse accuracy |
| 3 | lineage backend에 graph edge 저장 | graph consistency |
| 4 | 변경 영향과 오류 원인을 upstream/downstream으로 분석 | analysis coverage |

> 요약: Lineage는 실행 시점 metadata를 수집해 graph를 만들고 변경 영향과 장애 원인을 탐색한다.

---

## Ⅳ. 특징

| 구분 | Table-Level Lineage | Column-Level Lineage | 판단 기준 |
|:---|:---|:---|:---|
| 추적 단위 | 테이블·파일·토픽 | 컬럼·필드 | 개인정보·schema 영향 |
| 수집 난이도 | 상대적으로 낮음 | SQL parsing·UDF 해석 필요 | 변환 복잡도 |
| 활용 | 시스템 영향 범위 | 특정 지표·필드 영향 | 감사 상세도 |
| 한계 | 컬럼 영향 누락 | 동적 SQL·비정형 처리 한계 | 자동화 보정 필요 |

> 요약: 감사와 민감정보 영향 분석은 column-level lineage가 필요하지만 수집 정확도 검증이 필수다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 관리 방식 | 위키·수동 다이어그램 | runtime lineage event | 변경 빈도 |
| 분석 방향 | 담당자 문의 | upstream/downstream graph 탐색 | 장애 대응 시간 |
| 표준 | 도구별 metadata | OpenLineage 모델 | 도구 상호운용 |

> 요약: 파이프라인 변경과 장애 조사가 반복되면 수동 문서보다 runtime lineage 수집을 적용해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 누락 | connector 미지원·수동 job | OpenLineage instrumentation | lineage coverage |
| 오류 | SQL parser 한계·동적 코드 | 샘플 검증, manual override | edge accuracy |
| graph 과부하 | 노드·edge 급증 | retention, aggregation | graph query latency |

> 요약: Lineage 리스크는 coverage, accuracy, graph scale이며 자동 수집과 검증 루프로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 커버리지 | 핵심 파이프라인 lineage 수집 | job inventory 대조 |
| 정확도 | 샘플 영향 분석 결과 일치 | manual validation |
| 활용도 | incident·change ticket에서 lineage 참조 | ticket audit |

> 요약: Data Lineage 성과는 graph 존재보다 실제 변경·장애 대응에서 영향 분석에 쓰이는지로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. Airflow, Spark, dbt, Flink 등 핵심 파이프라인에 OpenLineage 또는 catalog connector를 적용함.
2. table-level lineage부터 시작하고 개인정보·재무 지표는 column-level lineage와 data quality rule을 연결함.
3. schema 변경 프로세스에 downstream impact analysis와 owner 승인 단계를 포함함.

**결론 (2줄):**
- 기술사 판단: Lineage는 감사 문서가 아니라 변경 관리와 품질 장애 대응에 연결될 때 운영 가치가 발생함.
- 향후 방향: Lineage는 catalog, data contract, observability, AI context graph와 결합해 데이터 신뢰성 판단 근거로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Data Lineage를 설명하시오" | lineage event 수집과 graph 구성 | table vs column lineage |
| 요구사항 명시형 | "데이터 품질 장애 대응 방안을 제시하시오" | upstream 원인 추적과 downstream 영향 분석 | 누락·정확도 리스크 대응 |

> 요약: 설명형은 graph 모델을, 방안형은 변경 영향과 장애 원인 분석을 중심으로 작성한다.
