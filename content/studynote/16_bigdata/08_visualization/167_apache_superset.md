---
title: 167. Apache Superset — 오픈소스 엔터프라이즈 BI SQL Lab
date: '2026-04-21'
tags:
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)

- **본질**: Apache Superset은 Airbnb에서 시작하여 2021년 Apache Top-Level Project로 승격된 [[191_oss_license_compliance|오픈소스]] BI 플랫폼으로, SQL Lab(고급 SQL 에디터)과 40개 이상의 차트 유형을 무료로 제공하며 엔터프라이즈 도구와 기능적으로 경쟁 가능하다.
- **가치**: Druid·ClickHouse·Trino/Presto·[[263_storage_compute_separation_bigquery|BigQuery]] 등 현대 분석 [[002_database_definition|데이터베이스]]와의 네이티브 통합으로 서브세컨드 대화형 분석을 지원하며, 완전 커스터마이징 가능한 [[191_oss_license_compliance|오픈소스]] 특성이 자체 BI 플랫폼 구축의 핵심 기반이 된다.
- **판단 포인트**: Looker의 LookML 시맨틱 레이어와 달리 SQL이 시맨틱 레이어 역할을 하는 Superset은 기술 팀 친화적이지만 비기술 비즈니스 사용자에게는 Metabase가 더 적합하므로, 팀 기술 수준에 따른 선택이 필요하다.

---

## Ⅰ. 개요 및 필요성

### Apache Superset의 역사

2015년 Airbnb의 [[001_dikw_pyramid|데이터]] 인프라 팀이 내부 BI 도구로 개발을 시작했다. 2016년 [[191_oss_license_compliance|오픈소스]]로 공개, 2021년 Apache Software Foundation의 Top-Level [[042_relational_algebra_project|Project]]([[385_tlp|TLP]])로 승격되었다. 현재 Airbnb, Lyft, Dropbox, Twitter 등 수백 개 기업이 프로덕션 환경에서 사용한다.

**Apache Preset**: Superset의 매니지드 클라우드 [[288_version_ihl_tos_total_length|버전]] — 설치·운영 없이 SaaS로 Superset 사용.

**📢 섹션 요약 비유**: Apache Superset은 **[[191_oss_license_compliance|오픈소스]] 레스토랑 레시피**와 같다. 레시피가 공개되어 있어 누구나 음식(BI 플랫폼)을 만들 수 있고, 자신의 취향(비즈니스 요구사항)에 맞게 수정할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Superset [[106_ta_as_is_analysis|기술 아키텍처]]

```
┌─────────────────────────────────────────────────────────────┐
│                  Apache Superset 아키텍처                    │
├──────────────────────────────────────────────────────────────┤
│  프론트엔드 (React + TypeScript)                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  SQL Lab: 고급 SQL 에디터                               │ │
│  │  Chart Builder: 데이터셋 기반 차트 제작                 │ │
│  │  Dashboard: 차트 조합·공유                              │ │
│  └────────────────────────────────────────────────────────┘ │
│                          │                                   │
│  백엔드 (Python Flask)                                       │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Superset Core: 쿼리 실행, 보안, API                   │ │
│  │  Celery: 비동기 쿼리 실행, 캐시 갱신                   │ │
│  │  SQLAlchemy: 다양한 DB 연결                             │ │
│  └────────────────────────────────────────────────────────┘ │
│                          │                                   │
│  인프라                                                      │
│  ┌────────────────┬───────────────┬──────────────────────┐  │
│  │ Redis          │ PostgreSQL/   │ 데이터 소스           │  │
│  │ (캐시+메시지큐)│ MySQL         │ (Druid, ClickHouse,   │  │
│  │                │ (메타데이터)  │  BigQuery, Snowflake, │  │
│  │                │               │  Trino, PostgreSQL)   │  │
│  └────────────────┴───────────────┴──────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### SQL Lab: 핵심 기능

```
SQL Lab 주요 기능:
  ▪ 멀티탭 SQL 에디터 (여러 쿼리 동시 작업)
  ▪ 자동완성 (테이블명, 컬럼명, SQL 키워드)
  ▪ 쿼리 이력 (Query History) 저장·재사용
  ▪ 저장된 쿼리 (Saved Queries) 팀 공유
  ▪ 쿼리 결과 시각화 바로가기 (Explore 버튼)
  ▪ CSV/JSON 다운로드
  ▪ 비동기 실행 (장시간 쿼리 백그라운드 처리)
  ▪ Jinja2 템플릿 (동적 쿼리 파라미터)
```

### [[001_dikw_pyramid|데이터]]셋 중심 모델

Superset의 차트 제작 흐름:

```
[데이터 소스 연결]
      │
      ▼
[데이터셋 생성]
  테이블 직접 연결 또는 SQL로 가상 데이터셋 생성
  (비즈니스 로직을 SQL로 표현)
      │
      ▼
[차트 제작 (Chart Builder)]
  데이터셋 선택 → 차트 유형 선택 → 필드 드래그앤드롭
      │
      ▼
[대시보드 구성]
  차트들을 드래그앤드롭으로 배치
```

**📢 섹션 요약 비유**: Superset의 SQL Lab은 **[[001_dikw_pyramid|데이터]] 과학자의 실험실**과 같다. 원하는 실험([[298_qkv_attention|쿼리]])을 자유롭게 수행하고, 결과를 즉시 [[003_bigdata_7v|시각화]]하며, 성공한 실험은 팀과 공유할 수 있다.

---

## Ⅲ. 비교 및 연결

### Superset vs Metabase 비교

| 차원 | Apache Superset | Metabase |
|:---|:---|:---|
| **대상 사용자** | [[001_dikw_pyramid|데이터]] 팀, SQL 능숙자 | 비기술 비즈니스 사용자 |
| **[[009_config|설정]] 복잡도** | 높음 (서버, [[542_redis|Redis]], Celery) | 낮음 (단일 JAR [[501_file_definition_logical_record|파일]]) |
| **SQL 능력** | SQL Lab으로 강력 | SQL 옵션 있음 |
| **시맨틱 레이어** | SQL 기반 | 자체 질문 기반 |
| **커스터마이징** | 완전 [[191_oss_license_compliance|오픈소스]] | 부분 ([[191_oss_license_compliance|오픈소스]] [[288_version_ihl_tos_total_length|버전]]) |
| **차트 유형** | 40+ (고급 포함) | 30+ (기본 위주) |
| **가격** | 무료 (상업용 가능) | 무료 기본 + Pro |

### 지원 [[002_database_definition|데이터베이스]] 생태계

Superset이 특히 강점을 보이는 현대 분석 [[002_database_definition|데이터베이스]]:

| [[002_database_definition|데이터베이스]] | 특징 | Superset 통합 |
|:---|:---|:---|
| **Apache Druid** | 서브초 [[316_olap|OLAP]], 시계열 특화 | 네이티브 커넥터 |
| **ClickHouse** | 컬럼형, 초고성능 집계 | 공식 지원 |
| **Trino/Presto** | [[136_variance|분산]] SQL, 멀티 소스 | 공식 지원 |
| **Apache Pinot** | 실시간 [[316_olap|OLAP]] | 네이티브 커넥터 |
| **[[263_storage_compute_separation_bigquery|BigQuery]]** | GCP 관리형 [[209_data_warehouse_schema_on_write|DW]] | 공식 지원 |

**📢 섹션 요약 비유**: Superset vs Metabase는 **전문 주방 vs 가정 주방**이다. 전문 주방(Superset)은 다양하고 복잡한 요리(분석)가 가능하지만 요리사([[001_dikw_pyramid|데이터]]팀)가 필요하다. 가정 주방(Metabase)은 누구나 쉽게 요리(분석)할 수 있지만 기능이 한정된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 보안 모델

```
Superset 보안 계층:
  1. 역할 기반 접근 제어 (RBAC):
     - Admin: 전체 권한
     - Alpha: 대시보드·차트 생성, 데이터셋 접근
     - Gamma: 공유 받은 대시보드만 조회
     - SQL Lab: SQL Lab 전용 접근
     
  2. 행 수준 보안 (RLS):
     - 데이터셋에 행 필터 정책 추가
     - 역할별 자동 WHERE 절 삽입
     예: 영업팀 역할에 region = '서울' 자동 적용
     
  3. 데이터셋 수준 접근 제어:
     - 데이터셋별 접근 가능 역할 지정
```

### 배포 아키텍처

| 환경 | 추천 구성 |
|:---|:---|
| **개발/소규모** | [[063_docker_architecture|Docker]] Compose (단일 서버) |
| **프로덕션** | [[205_kubernetes_container_orchestration|Kubernetes]] ([[056_helm_chart|Helm Chart]]), 별도 [[542_redis|Redis]]·DB |
| **관리형** | Apache Preset (클라우드 [[309_saas|SaaS]]) |

**📢 섹션 요약 비유**: Superset의 [[205_kubernetes_container_orchestration|Kubernetes]] 배포는 **프랜차이즈 레스토랑 확장**과 같다. 맛이 [[395_verification_process_review|검증]]된 레시피(Superset)를 여러 도시(서버)에 표준화된 방식([[056_helm_chart|Helm Chart]])으로 확장한다.

---

## Ⅴ. 기대효과 및 결론

### Superset 도입 효과

| 영역 | 효과 |
|:---|:---|
| **비용** | 상용 BI 도구 대비 라이선스 비용 0 |
| **유연성** | 완전 [[191_oss_license_compliance|오픈소스]] → 내부 필요에 맞게 수정 |
| **분석 속도** | SQL Lab으로 즉각적인 탐색적 분석 |
| **생태계** | 현대 [[316_olap|OLAP]] [[002_database_definition|데이터베이스]]와 깊은 통합 |

### 결론

Apache Superset은 **기술 팀 주도 [[001_dikw_pyramid|데이터]] 플랫폼 구축에 최적화된 [[191_oss_license_compliance|오픈소스]] BI**다. 라이선스 비용 없이 엔터프라이즈 수준의 기능을 제공하며, 현대 분석 [[002_database_definition|데이터베이스]](Druid, ClickHouse)와의 깊은 통합이 대규모 빅데이터 분석 환경에서 강점이다. 단, 설치·운영·보안 [[009_config|설정]]에 인프라 전문 지식이 필요하므로, [[001_dikw_pyramid|데이터]] 엔지니어링 역량이 있는 팀에게 권장된다.

**📢 섹션 요약 비유**: Apache Superset은 **[[191_oss_license_compliance|오픈소스]] 스위스 아미 나이프**와 같다. 하나의 도구로 SQL 분석, [[003_bigdata_7v|시각화]], 대시보드, 공유, 보안을 모두 처리할 수 있는 만능 도구이며, 무료로 제공된다.

---

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---|:---|:---|
| SQL Lab | 핵심 기능 | 고급 SQL 에디터 + 결과 [[003_bigdata_7v|시각화]] |
| Apache Druid | 통합 DB | 서브초 실시간 [[316_olap|OLAP]] 분석 |
| ClickHouse | 통합 DB | 초고성능 컬럼형 [[316_olap|OLAP]] |
| Celery | 백그라운드 처리 | 비동기 [[298_qkv_attention|쿼리]] 실행·캐시 갱신 |
| Apache Preset | 관리형 [[090_service_kubernetes_network_load_balancing|서비스]] | Superset의 [[309_saas|SaaS]] 클라우드 [[288_version_ihl_tos_total_length|버전]] |
| Metabase | 비교 제품 | 비기술 사용자 친화적 [[191_oss_license_compliance|오픈소스]] BI |
| [[569_rbac|RBAC]] | 보안 모델 | 역할 기반 접근 제어 + RLS |

### 📈 관련 키워드 및 발전 흐름도

```text
[BI 도구]
    │
    ▼
[시각화]
    │
    ▼
[Apache Superset]
    │
    ▼
[SQL Lab]
    │
    ▼
[대시보드]
    │
    ▼
[셀프서비스 분석]
```

전통 BI가 웹 기반 [[003_bigdata_7v|시각화]] 도구를 거쳐 SQL Lab과 셀프서비스 분석 플랫폼으로 진화하는 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명

- Apache Superset은 **무료로 쓸 수 있는 강력한 [[001_dikw_pyramid|데이터]] 현미경**이에요: 돈 한 푼 안 내고도 전문 과학자([[001_dikw_pyramid|데이터]]팀)가 [[001_dikw_pyramid|데이터]]를 깊이 들여다볼 수 있어요.
- SQL Lab은 **[[001_dikw_pyramid|데이터]] 과학자의 실험실 노트**예요: 원하는 [[298_qkv_attention|쿼리]]를 자유롭게 써보고, 결과를 바로 차트로 만들고, 좋은 [[298_qkv_attention|쿼리]]는 팀원과 공유할 수 있어요.
- Superset은 전문가용, Metabase는 비전문가용이에요 — 요리사([[001_dikw_pyramid|데이터]]팀)에겐 Superset, 일반 손님(비즈니스 사용자)에겐 Metabase가 더 편해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 167 / 262

← **이전**: [[166_looker|166. Looker / Looker Studio — LookML 시맨틱 레이어 BI]]
**다음**: [[168_grafana|168. Grafana — 메트릭/로그/추적 통합 관측성 시각화]] →

---
