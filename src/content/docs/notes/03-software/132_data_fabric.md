---
sidebar:
  order: 132
  label: "132. 데이터 패브릭"
  badge:
    text: "기출 · 50%"
    variant: note
title: "데이터 패브릭 (Data Fabric)"
date: "2026-08-25T11:00:00+09:00"
tags:
  - "notes-software"
weight: 132
extra:
  question_no: "132"
  source_status: "기출"
  source_history: "135회"
  priority: 50
  priority_note: "135회 기출, 메타데이터 기반 통합 설계"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **데이터 패브릭(Data Fabric)**: 분산된 이종 데이터 원천을 물리적 복제 없이 Active Metadata, 지식 그래프, AI 자동화를 통해 직조(Fabric)하여 실시간 가상 통합을 제공하는 아키텍처.
- **Active Metadata**: 수동 관리에 의존하지 않고 시스템 로그, 접근 패턴, 쿼리 메트릭을 AI로 실시간 분석하여 파이프라인과 거버넌스를 자동 최적화하는 동적 메타데이터.

</details>

- 정의/개념: 분산된 이종 데이터 환경에서 **Active Metadata와 지식 그래프 및 데이터 가상화를 통해 물리적 이동 없이 데이터를 실시간 통합·제공**하는 지능형 데이터 아키텍처
- 배경/필요성: 하이브리드·멀티 클라우드 확산으로 인한 **데이터 사일로(Silo) 고립, 메타데이터 수동 관리 한계 및 전사 데이터 계보 추적 불가 해결 불가**

#### 한줄 요약
- Active Metadata와 데이터 가상화로 물리적 이동 없이 이종 데이터를 단일 패브릭으로 통합한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Data Virtualization(데이터 가상화)**: 물리적 ETL 복제 없이 원천 DB로 조건절 쿼리를 직접 푸시다운하여 실시간 가상 뷰로 통합 제공하는 기술.
- **Semantic Knowledge Graph**: 데이터 자산 간의 의미론적 관계, 스키마 계보(Lineage), 소유권을 노드-엣지 그래프로 표현하여 AI 추천에 활용.

</details>

- AI/ML 기반으로 쿼리 패턴과 성능을 지속 학습하는 **Active Metadata 기반 자동화**
- 물리적 복제 없이 분산 원천을 단일 SQL로 조회하는 **데이터 가상화(Data Virtualization)**
- 분산 저장소 전반에 일관된 PII 마스킹과 접근 제어를 적용하는 **통합 거버넌스 집행**

#### 한줄 요약
- 활성 메타데이터와 지식 그래프를 활용하여 분산 데이터의 가상화 통합과 자동화를 실현한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **데이터 패브릭 4대 레이어**: Consumer Layer(소비 계층), Active Metadata Layer(지능형 지식그래프), Virtualization Layer(가상화 쿼리 엔진), Source Layer(멀티클라우드 원천).

</details>

```text
[데이터 패브릭 지능형 가상화 아키텍처]
|-- 1. Business Consumer Layer (BI 대시보드, SQL 분석가, AI/ML 데이터 사이언티스트)
|-- 2. Active Metadata & Knowledge Graph Layer (실시간 로그 분석, 계보 추적, AI 추천 카탈로그)
|-- 3. Virtualization & Orchestration Layer (Trino / Denodo / Apache Airflow)
|   |-- Data Virtualization (물리적 이동 없는 분산 쿼리 푸시다운)
|   `-- Unified Policy Engine (RBAC / ABAC 및 PII 동적 마스킹)
`-- 4. Hybrid Multi-Cloud Sources (AWS S3, Snowflake, Oracle, MySQL, Kafka)
```

선의 의미: 계층 및 이종의 멀티 클라우드 소스 데이터를 Active Metadata와 가상화 레이어를 거쳐 단일 패브릭으로 제공하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **데이터 원천 (Data Sources)** | 하이브리드 멀티 클라우드 상의 **RDBMS, DW, Data Lake 데이터 제공** | 이종 데이터 분산 |
| **Active Metadata 엔진** | 실시간 쿼리 및 접근 패턴을 감지하여 **데이터 추천 및 파이프라인 자동 최적화** | AI 기반 동적 분석 |
| **지식 그래프 (Knowledge Graph)**| 전사 데이터 간의 **의미론적 연관 관계, 스키마 계보(Lineage), 소유권 매핑** | 메타데이터 네트워크화 |
| **가상화 엔진 (Virtualization)**| 분산 원천 데이터에 대한 **단일 SQL 인터페이스 및 조건절 푸시다운 수행** | Trino, Denodo |
| **정책 엔진 (Policy Engine)** | 역할 기반(RBAC) 및 속성 기반(ABAC) **통합 보안/PII 마스킹 정책 자동 강제** | 일관된 보안 거버넌스 |

#### 한줄 요약
- 원천 데이터, Active Metadata, 지식 그래프, 가상화 엔진, 정책 엔진이 유기적으로 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **지능형 가상화 쿼리 5단계**: 자산 탐색 $\to$ 정책/권한 검증 $\to$ 최적 분산 계획 $\to$ 조건절 푸시다운 $\to$ 메타데이터 피드백.

</details>

```text
비즈니스 분석가의 통합 데이터 쿼리 요청 (SQL / 자연어)
        │
   1. [자산 탐색] 지식 그래프와 카탈로그를 참조하여 타깃 데이터 자산 위치 및 스키마 매핑
        │
   2. [정책 검증] 정책 엔진이 사용자의 ABAC 권한을 검증하고 PII 민감정보 실시간 동적 마스킹
        │
   3. [실행 계획 수립] 가상화 옵티마이저가 네트워크 I/O와 DB 부하를 고려한 최적 분산 플랜 수립
        │
   4. [가상 쿼리 푸시다운] 원천 DB들로 조건절(Predicate Pushdown) 전송 및 결과만 메모리 취합
        │
   5. [메타 피드백] 쿼리 응답 시간 및 캐시 적중률 통계를 Active Metadata 엔진에 피드백
```

#### 한줄 요약
- 자산 탐색 → 권한 검증 → 분산 계획 수립 → 푸시다운 실행 → 메타 피드백 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **전통적 ETL vs 데이터 패브릭**: 물리적 대용량 복제 방식의 ETL과 Active Metadata 기반 실시간 가상화 통합 방식의 데이터 패브릭.

</details>

| 비교 항목 | 전통적 ETL / Data Warehouse | 데이터 패브릭 (Data Fabric) |
|:---|:---|:---|
| 데이터 통합 방식 | **물리적 데이터 일괄 복제 및 이동 (Batch ETL)**| **데이터 가상화 기반 실시간 원격 조회 (Zero Copy)** |
| 메타데이터 활용 | 정적 메타데이터 (단순 문서화 카탈로그) | **Active Metadata 기반 AI 자동화 및 계보 추적** |
| 파이프라인 구축 소요| 수주 ~ 수개월 소요 (파이프라인 개발) | **수 시간 ~ 수일 이내 가상 뷰 즉시 생성** |
| 인프라 스토리지 비용| 데이터 중복 저장으로 고비용 발생 | **물리 복제 최소화로 클라우드 스토리지 비용 절감**|

#### 한줄 요약
- 물리적 일괄 복제는 전통적 ETL, 분산 원천의 실시간 지능형 통합은 데이터 패브릭을 채택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Cross-Cloud Latency**: 서로 다른 클라우드(AWS vs Azure) 간 대용량 가상화 조인 시 네트워크 대역폭 한계로 쿼리가 지연되는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 이종 클라우드 DB 간 가상화 `JOIN` 시 네트워크 지연 급증 | **Trino 조건절 푸시다운(Pushdown) 및 빈번 쿼리 가상 캐싱 적용** | 네트워크 전송 데이터량 90% 절감 |
| 메타데이터 갱신 지연으로 인한 낡은(Stale) 매핑 정보 조회 | **Debezium CDC 기반 실시간 스키마/메타데이터 동기화 훅 설정** | 메타데이터 최신성 100% 보장 |
| 멀티 클라우드 환경에서 이종 IAM 보안 정책 불일치 | **Immuta / Privacera 등 중앙 데이터 거버넌스 플랫폼 도입** | 단일 보안 정책으로 전사 일관 통제 |
| 대규모 Ad-hoc 분석 시 원천 운영 DB CPU 과부하 | **운영계 Read Replica 지정 연결 및 쿼리 리소스 쿼터제 적용** | 운영 서비스 영향도 0화 |

#### 한줄 요약
- 조건절 푸시다운, CDC 메타 동기화, 중앙 거버넌스, Read Replica 격리로 운영한다.

## Ⅶ. 결론

- 하이브리드·멀티 클라우드 환경에서 물리적 복제 비용을 절감하고 실시간 분석을 가속하기 위해 **Active Metadata와 데이터 가상화 기반의 데이터 패브릭을 표준 아키텍처로 도입**하고, **Data Mesh의 도메인 제품 개념을 상호 보완적으로 결합**하여 차세대 데이터 생태계 완성

#### 한줄 요약
- 데이터 패브릭은 Active Metadata와 지식 그래프, 데이터 가상화를 통해 물리적 이동 없이 분산 데이터를 지능형으로 통합하는 차세대 데이터 아키텍처다.