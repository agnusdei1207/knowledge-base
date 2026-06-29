---
title: "컴퓨터시스템응용기술사 핵심 트랙"
date: "2026-06-29"
tags:
  - "studynote-bigdata"
weight: 91
---

## 컴퓨터시스템응용기술사 핵심 트랙

- 기준: 컴퓨터시스템응용기술사 관점만 반영
- 과목 총 노트 수: 262개
- 과목 필요성:
  - 빅데이터는 대규모 분산 저장·처리·분석 시스템을 다루므로, 컴퓨터시스템응용기술사에서 분산 아키텍처와 데이터 활용 가치를 동시에 평가하기 좋은 과목이다.
  - 하둡(Hadoop), 스파크(Spark), 스트리밍, NoSQL(Not Only SQL), 거버넌스, 시각화까지 이어지는 전체 체계를 설명할 수 있어야 한다.
  - 최근에는 데이터 레이크하우스, 실시간 분석, 벡터 데이터베이스(Vector Database), 인공지능 연계 분석 플랫폼으로 출제 관점이 이동하고 있다.
  - 따라서 저장 구조, 처리 엔진, 데이터 품질, 서비스 활용까지 연결하는 서술 훈련이 필요하다.
- 우선 학습 챕터:
  - `02_hadoop`
  - `03_spark`
  - `04_streaming`
  - `06_nosql`
  - `07_data_lake`
  - `10_governance`
  - `12_trends`
- 추천 핵심 키워드 목표 수: 80개
- 단답형 포인트:
  - MapReduce, HDFS(Hadoop Distributed File System), RDD(Resilient Distributed Dataset), Spark SQL, Kafka, Flink, CEP(Complex Event Processing) 정의
  - CAP 정리(CAP Theorem), Parquet, Delta Lake, Apache Iceberg, Data Catalog, Lineage 같은 핵심 용어 정리
  - 배치, 마이크로배치, 스트리밍, 레이크하우스, 데이터 메시(Data Mesh) 차이 구분
- 서술형 포인트:
  - 배치와 스트리밍 통합 아키텍처, 대규모 데이터 플랫폼, 실시간 분석 체계, 데이터 거버넌스 전략을 비교형으로 전개
  - 성능, 확장성, 저장비용, 정합성, 운영복잡도 관점의 트레이드오프를 답안에 함께 넣어야 함
  - 빅데이터 플랫폼을 AI 학습·추론 데이터 공급체계로 확장해 설명하면 최근 출제 경향에 부합
- 최신 기술 동향 연결:
  - 레이크하우스: Delta Lake, Apache Iceberg, Hudi와 오픈 테이블 포맷 중심으로 정리
  - 데이터 파이프라인: 실시간 수집-처리-서빙 구조, Kappa Architecture, 실시간 OLAP(Online Analytical Processing)로 연결
  - 클라우드 네이티브: 서버리스 분석, 스토리지-컴퓨트 분리, 관리형 데이터 플랫폼으로 확장
  - 플랫폼 엔지니어링: 데이터 플랫폼 제품화, 분석 셀프서비스, 거버넌스 자동화와 접점 형성
  - AIOps: 데이터 품질 이상 탐지, 운영 메타데이터 기반 자율 튜닝, 관측성 분석과 연계
