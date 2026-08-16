---
sidebar:
  order: 132
  label: "132. 데이터 패브릭 (Data Fabric)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "데이터 패브릭 (Data Fabric)"
date: "2026-08-14T00:02:00+09:00"
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

- **Data Fabric (데이터 패브릭)**: Gartner가 선정한 핵심 데이터 아키텍처로, 온프레미스, 클라우드, Multi-Cloud에 파편화된 이종 데이터 원천들을 물리적 이동 없이 Active Metadata(활성 메타데이터), AI/ML 지식 그래프(Knowledge Graph)를 기반으로 하나로 유연하게 직조(Fabric)하여 실시간 가상화 통합을 렌더링하는 기술.
- **Active Metadata (활성 메타데이터)**: 데이터 스크레이핑에 의한 수동 메타데이터(Passive Metadata)가 아닌, 쿼리 패턴, 사용자 접근 로그, 파이프라인 성능 실시간 데이터를 AI로 자동 지속 분석하여 파이프라인 최적화에 능동 반영하는 메타데이터.
- **Knowledge Graph (지식 그래프)**: 전사 데이터 자산 간의 연관 관계, 계보(Lineage), 스키마, 사용자 접근 이력을 노드와 엣지로 그래픽 시각화 및 자동 맵핑하는 메커니즘.

</details>

- 정의/개념: 활성 메타데이터로 분산 데이터를 연결하는 **Data Fabric**
- 배경/필요성: 하이브리드 환경은 **위치•정책•리니지 파편화** 유발

#### 한줄 요약

- 분산 데이터 저장소의 위치·관계·접근 정책을 활성 메타데이터와 지식 그래프로 관리한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Data Virtualization (데이터 가상화)**: 물리적 데이터 이동 0회로 분산 저장소 데이터를 가상 뷰(Virtual View)로 결합.
- **AI-Driven Data Management**: AI/ML 알고리즘이 추천 데이터셋, 자동으로 보안 PII 마스킹 처리 실행.

</details>

- **Active Metadata & Knowledge Graph-Driven Automation (활성 메타데이터 기반 자동화)**
- **Data Virtualization**: 필요에 따라 원격 조회•캐시•이동 결합
- **Unified Security & Automated Pipeline Generation (통합 보안 정책 및 자동 파이프라인 생성)**

#### 한줄 요약

- 자동 안내가 똑똑해도 지도 정보가 낡으면 잘못된 자료를 찾거나 잘못된 문을 열 수 있다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Data Virtualization Layer (가상화 레이어)**: Trino/Denodo 기반으로 서로 다른 DB(PostgreSQL, S3, Snowflake)를 단일 SQL 인터페이스로 묶어주는 가상 통합 엔진.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Data Fabric Architecture                        │
├────────────────────────────────────────────────────────────────────────┤
│ Consumers: [BI Analytics]  [Data Science / ML]  [Operational Apps]     │
├────────────────────────────────────────────────────────────────────────┤
│ Active Metadata & Knowledge Graph Layer (AI/ML Auto Catalog, Lineage) │
├────────────────────────────────────────────────────────────────────────┤
│ Data Virtualization & Orchestration Layer (Trino / Denodo / Airflow)   │
├────────────────────────────────────────────────────────────────────────┤
│ Hybrid Multi-Cloud Sources: [AWS S3]  [Snowflake]  [MySQL]  [Oracle]   │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 이종의 멀티 클라우드 소스 데이터를 Active Metadata 및 가상화 레이어를 거쳐 단일 패브릭으로 묶어 비즈니스 소비자에게 제공하는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| Data Sources | DB•DW•Lake의 데이터와 메타데이터 제공 |
| Active Metadata | 사용•품질•성능•변경 신호 지속 수집 |
| Knowledge Graph | 의미•소유•리니지•정책 관계 연결 |
| Virtualization | 통합 질의와 푸시다운•캐시 실행 |
| Policy Engine | 접근•마스킹•보존 규칙 일관 집행 |

#### 한줄 요약

- 분산 데이터 저장소를 활성 메타데이터와 통합 정책으로 연결한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Data Fabric vs Data Mesh**: Fabric은 기술/AI/메타데이터 중심의 통합 자동화 접근(Technology-centric), Mesh는 조직/도메인 팀 중심의 분산 책임 접근(People & Process-centric).

</details>

```text
[데이터 접근 요구]
      │
      ▼
1. 자산•의미 탐색
      │
      ▼
2. 정책•권한 판정
      │
      ▼
3. 실행 경로 계획
      │
      ▼
4. 원격 조회•캐시 실행
      │
      ▼
5. 사용 신호 메타데이터 반영
```

### 동작 원리

1. **자산•의미 탐색**: 카탈로그와 지식 그래프로 후보 식별
2. **정책•권한 판정**: 사용자•목적별 접근•마스킹 결정
3. **실행 경로 계획**: 푸시다운•캐시•이동 비용 비교
4. **원격 조회•캐시 실행**: 선택 경로로 통합 결과 생성
5. **사용 신호 메타데이터 반영**: 성능•품질•접근 이력 갱신

#### 한줄 요약

- 지도를 계속 갱신하고 목적과 권한에 맞는 길만 열며 통행 결과로 지도를 다시 고친다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Data Virtualization Efficiency**: 가상화 쿼리를 사용함으로써 ETL 개발 수개월 단축 및 스토리지 중복 비용 0원 달성.

</details>

| 비교 항목 | Traditional Data Warehouse / ETL | Data Fabric Architecture |
|:---|:---|:---|
| 데이터 접근 방식 | **물리적 ETL•ELT 복제** | 가상화•캐시•선택적 이동 조합 |
| 메타데이터 활용 | Passive Metadata (수동 단순 등록) | **Active Metadata (AI 기반 실시간 추적)** |
| 통합 구축 속도 | 느림 (ETL 파이프라인 구축 수개월) | **매우 빠름 (가상 뷰 생성으로 수일 내 연동)** |
| 아키텍처 중심 | 중앙집중식 모놀리식 스토리지 | **하이브리드 멀티클라우드 가상 통합** |

#### 한줄 요약

- 패브릭은 도로와 교통 규칙, 메시는 각 상점의 상품 책임에 가깝다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Virtualization Query Performance Latency**: 물리 데이터 이관이 없으므로, 서로 다른 멀티 클라우드 간 `JOIN` 실행 시 네트워크 렌더링 지연 발생 위험.

</details>

| 3대 구축 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| 1. Query Latency 병목 | 가상화 쿼리로 이종 DB 간 `JOIN` 시 네트워크 폭주 | **Trino Pushdown Predicate & 결과 Caching 적용** |
| 2. Active Metadata 지연 | 메타데이터 크롤링 지연으로 낡은 맵핑 전파 | **Debezium CDC 기반 실시간 메타 동기화 훅** |
| 3. Multi-Cloud Security | AWS와 Azure 간 IAM 보안 정책 불일치 | **Immuta / Privacera 통합 데이터 거버넌스 적용** |

> 사례: **삼성전자 / 현대자동차 글로벌 멀티 클라우드 하이브리드 Data Fabric 가상화 구축**

#### 한줄 요약

- 지도에 장소가 많다는 것보다 위치와 통행 제한이 실제와 맞는지 계속 확인해야 한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **Data Fabric 수립 기준(Data Fabric Architecture Standards)**: Active Metadata, Knowledge Graph, Data Virtualization (Trino) 및 Unified Security에 의거한 체계.

</details>

- 분산 자산 통합 자동화는 **Fabric**, 도메인 소유 분산은 Mesh 선택

#### 한줄 요약

- 연결망의 가치는 선의 개수가 아니라 지도가 정확하고 잘못 연 문을 바로 찾아 닫을 수 있는지에 달려 있다.
