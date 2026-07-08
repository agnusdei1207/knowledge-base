---
title: "Data Lineage 데이터 계보 (Data Lineage)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 310
extra:
  question_no: "310"
  exam_status: "기출"
  exam_history: "136회"
---

## 미리 알고가기

- Data Lineage는 데이터가 어디서 왔고 어떤 변환을 거쳐 어디로 흘러가는지 추적하는 구조임
- 테이블 수준보다 컬럼 수준 계보가 더 정밀하지만 구현 난도와 비용이 높음
- 품질 사고 분석과 변경 영향 분석과 규제 대응에서 핵심 근거로 쓰임

## Ⅰ. 개요

- **정의/개념**: Data Lineage는 데이터의 생성과 수집과 변환과 적재와 소비 전 과정을 추적해 상류와 하류 관계와 변환 근거를 시각적으로 보여주는 메타데이터 기반 추적 체계임
- **배경/필요성**: 데이터 파이프라인이 복잡해질수록 오류 원인과 변경 영향 범위를 빠르게 찾기 어려워져 데이터 신뢰성과 규제 대응을 위해 흐름 가시성이 필수로 요구됨

## Ⅱ. 특징

- 상류와 하류 관계를 연결해 장애 원인 분석과 변경 영향 분석 속도를 높임
- SQL과 ETL과 API 흐름을 함께 해석할수록 실제 운영 가치가 커짐
- 컬럼 수준 추적은 정밀도가 높지만 파싱 복잡도와 운영 비용이 큼
- Catalog와 품질 지표와 결합되면 단순 지도보다 운영 통제 도구로 확장됨

## Ⅲ. 종류 및 비교

| 판단 기준 | Data Lineage | Data Catalog | Audit Log |
|:---|:---|:---|:---|
| 핵심 초점 | 데이터 흐름과 변환 관계 | 데이터 발견과 이해 | 이벤트 기록 |
| 대표 표현 | graph 기반 상하류 맵 | 검색 포털 | 시간순 로그 |
| 주요 활용 | 영향 분석과 RCA | 자산 탐색 | 행위 추적 |
| 정밀도 축 | 테이블 또는 컬럼 수준 | 자산 설명 수준 | 이벤트 수준 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Source and Target Nodes | 데이터베이스와 파일과 대시보드 같은 자산을 노드로 표현해 계보 추적의 기본 단위를 구성함 |
| Transformation Parser | SQL과 ETL 정의와 작업 로그를 해석해 어떤 입력이 어떤 출력으로 연결되는지 추출하는 해석 계층임 |
| Lineage Graph Store | 상류와 하류 관계를 그래프로 저장해 탐색과 시각화와 영향 분석을 빠르게 수행하게 하는 핵심 저장 계층임 |
| Metadata and Context Link | 소유자와 품질과 정책과 카탈로그 정보를 연결해 계보를 운영 의사결정 근거로 확장하는 보조 계층임 |
| Impact and RCA View | 변경 예정 자산이나 품질 사고 자산을 기준으로 영향 범위와 원인 경로를 보여주는 활용 계층임 |

```text
+-------------+    +-------------+    +-------------+    +-------------+
| Source Node | -> | Transform   | -> | Target Node | -> | Impact View |
+-------------+    +-------------+    +-------------+    +-------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 메타 수집     | -> | 로직 파싱     | -> | 관계 매핑     | -> | 그래프 저장   | -> | 영향/RCA 조회 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **메타 수집**: 데이터 소스와 작업 도구와 로그에서 계보 후보 정보를 수집함
2. **로직 파싱**: SQL과 스크립트와 작업 정의를 분석해 입력과 출력 관계를 해석함
3. **관계 매핑**: 상류와 하류와 변환 단계를 그래프 형태로 연결함
4. **그래프 저장**: 검색과 시각화와 질의를 위해 중앙 저장소에 반영함
5. **영향과 RCA 조회**: 변경 전 영향 범위와 사고 발생 후 원인 경로를 탐색함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 동적 SQL과 외부 SaaS 가공처럼 파싱이 어려운 구간이 많으면 실제 계보가 끊겨 영향 분석 신뢰도가 낮아질 수 있음
   - 해결방안: hybrid lineage capture와 connector expansion roadmap을 적용하고 lineage coverage ratio와 broken lineage segment count로 검증함
2. 문제: 컬럼 수준 계보를 무리하게 전 구간에 적용하면 파싱 비용과 저장 비용이 커져 운영 지속성이 떨어질 수 있음
   - 해결방안: critical data element prioritization과 tiered granularity policy를 적용하고 column level coverage on critical assets와 lineage processing cost ratio로 검증함
3. 문제: 계보가 주기적으로만 갱신되면 변경 직후 분석 결과가 실제와 달라져 사고 대응 속도가 오히려 늦어질 수 있음
   - 해결방안: event driven refresh와 freshness SLA monitoring을 적용하고 lineage freshness lag와 stale lineage incident count로 검증함

## Ⅶ. 적용 사례

- 데이터 플랫폼이 하이브리드 수집 방식을 운영하며 확인 지표는 lineage coverage ratio와 broken lineage segment count임
- 규제 보고 체계가 중요 자산 우선 컬럼 계보를 적용하며 확인 지표는 column level coverage on critical assets와 lineage processing cost ratio임
- 운영 분석 포털이 이벤트 기반 갱신을 도입하며 확인 지표는 lineage freshness lag와 stale lineage incident count임

## Ⅷ. 결론

Data Lineage는 데이터 흐름 그림이 아니라 운영 판단 근거이므로 coverage와 freshness를 관리 가능한 수준으로 설계해야 실무 가치가 유지됨.
