---
title: "컴퓨터시스템응용기술사 핵심 트랙"
date: "2026-06-29"
tags:
  - "studynote-data-engineering"
weight: 91
---

## 컴퓨터시스템응용기술사 핵심 트랙

- 기준: 컴퓨터시스템응용기술사 관점만 반영
- 과목 총 노트 수: 210개
- 과목 필요성:
  - 데이터 엔지니어링은 시스템이 생성한 데이터를 어떻게 수집·정제·적재·서빙하는지 설명하는 기반 과목으로, 실시간 처리와 분석 플랫폼 설계 문제의 핵심 축이다.
  - 컴퓨터시스템응용기술사는 데이터 파이프라인을 단순 배치 작업이 아니라 분산 시스템, 저장 구조, 운영 자동화가 결합된 시스템 아키텍처로 본다.
  - 특히 ETL(Extract, Transform, Load)과 ELT(Extract, Load, Transform), 스트리밍, 메타데이터, 데이터 품질, 인공지능(AI) 학습 파이프라인을 연결해 묻는 문제가 많다.
  - 따라서 데이터 흐름, 장애 복구, 정합성, 지연시간, 거버넌스를 한 답안 안에서 구조적으로 묶는 훈련이 필요하다.
- 우선 학습 챕터:
  - `01_infrastructure`
  - `04_mlops`
  - `03_ml_dl_llm`
  - `02_math_mining`
  - CDC(Change Data Capture), 워크플로 오케스트레이션(Workflow Orchestration), 데이터 품질, 피처 스토어(Feature Store) 관련 세부 노트
- 추천 핵심 키워드 목표 수: 70개
- 단답형 포인트:
  - ETL, ELT, CDC, 데이터 레이크(Data Lake), 데이터 웨어하우스(Data Warehouse), 데이터 레이크하우스(Data Lakehouse) 정의와 차이
  - Airflow, Spark, Flink, Kafka, dbt(Data Build Tool), MLflow 등 도구의 역할 구분
  - 데이터 드리프트(Data Drift), 개념 드리프트(Concept Drift), 스키마 에볼루션(Schema Evolution), 멱등성(Idempotency) 개념 정리
- 서술형 포인트:
  - 배치와 스트리밍 파이프라인 통합, 실시간 데이터 플랫폼, MLOps(Machine Learning Operations) 운영모델을 비교형으로 전개
  - 품질, 계보(Lineage), 보안, 비용, 지연시간을 함께 다루는 데이터 플랫폼 아키텍처 문제가 중요
  - 데이터 제품화, 도메인 중심 소유, 모델 재학습 자동화까지 포함해야 컴퓨터시스템응용기술사 답안답다
- 최신 기술 동향 연결:
  - 데이터 파이프라인: CDC, 스트리밍, 오케스트레이션, 데이터 계약(Data Contract) 중심으로 정리
  - 레이크하우스: Delta Lake, Apache Iceberg, Hudi 기반 오픈 테이블 포맷(Open Table Format)과 연계
  - 플랫폼 엔지니어링: 데이터 플랫폼 셀프서비스, DataOps 관점의 표준화와 연결
  - 클라우드 네이티브: 관리형 스트리밍·분산처리 서비스와 컨테이너 기반 데이터 워크로드 운영으로 확장
  - AIOps: 데이터 품질 이상 탐지, 파이프라인 장애 예측, 자동 복구 시나리오로 연결
