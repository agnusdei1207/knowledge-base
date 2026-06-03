---
title: 297. 데이터 가상화 (Data Virtualization)
date: '2026-03-04'
tags:
- studynote-enterprise
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 여러 이기종 [[001_dikw_pyramid|데이터]] 소스를 물리적으로 통합하거나 이동시키지 않고, [[198_abstraction_control_data_process|추상화]] 계층을 통해 마치 하나의 [[002_database_definition|데이터베이스]]인 것처럼 실시간으로 조회하고 활용하는 기술이다.
> 2. **가치**: 복잡한 [[215_etl_vs_elt_pipeline|ETL]](추출, 변환, 적재) 과정 없이 [[001_dikw_pyramid|데이터]]에 즉시 접근할 수 있어 [[001_dikw_pyramid|데이터]] 신선도를 확보하고, [[001_dikw_pyramid|데이터]] 중복 저장에 따른 인프라 비용을 절감한다.
> 3. **판단 포인트**: [[001_dikw_pyramid|데이터]] 원천 시스템의 실시간 정보가 중요하거나, 보안/규제상 [[001_dikw_pyramid|데이터]] 이동이 제한된 환경에서 통합 분석 환경을 구축할 때 가장 효과적이다.

---

## Ⅰ. 개요 및 필요성

빅데이터 환경에서 모든 [[001_dikw_pyramid|데이터]]를 한곳([[209_data_warehouse_schema_on_write|DW]]/[[208_data_lake_schema_on_read|Data Lake]])으로 모으는 것은 엄청난 리소스를 요구한다. 특히 실시간으로 변하는 운영 [[001_dikw_pyramid|데이터]]([[327_hint_handoff|OLTP]])를 분석계로 [[212_synchronization_mechanisms|동기화]]하는 데는 시차가 발생할 수밖에 없다.

[[360_data_virtualization|데이터 가상화]]는 **"[[001_dikw_pyramid|데이터]]를 가져오지 말고, 있는 곳에서 [[298_qkv_attention|쿼리]]하자"**는 접근 방식을 통해, [[001_dikw_pyramid|데이터]] 원천의 물리적 위치와 상관없이 [[369_logic_bomb|논리]]적인 통합 뷰(Unified [[151_sql_view_virtual_table|View]])를 제공한다.

- **📢 섹션 요약 비유**: 수많은 영화 [[501_file_definition_logical_record|파일]]을 내 컴퓨터로 다 다운로드([[215_etl_vs_elt_pipeline|ETL]])하는 대신, 스트리밍 [[090_service_kubernetes_network_load_balancing|서비스]]([[247_data_virtualization_federated_query|Data Virtualization]])에 접속해 보고 싶은 영화를 즉시 감상하는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[360_data_virtualization|데이터 가상화]] 시스템은 사용자로부터 [[298_qkv_attention|쿼리]]를 받아 이를 각 원천 시스템이 이해할 수 있는 언어로 번역하고, 결과를 취합하여 전달하는 미들웨어 역할을 수행한다.

```text
[사용자/BI 도구] (Standard SQL 쿼리 실행)
           │
           ▼
┌──────────────────────────────────────────────────────────────┐
│                  데이터 가상화 계층 (DV Layer)                │
│ [추상화] [연방 쿼리 최적화] [캐싱] [데이터 보안 및 거버넌스]  │
└──────────────────────────────────────────────────────────────┘
      │               │               │               │
      ▼               ▼               ▼               ▼
 [SQL DB]        [NoSQL DB]       [SaaS API]      [Flat Files]
```

| 주요 메커니즘 | 설명 | 핵심 기술 |
|:---|:---|:---|
| [[198_abstraction_control_data_process|추상화]] ([[198_abstraction_control_data_process|Abstraction]]) | 기술적 복잡성을 숨기고 [[369_logic_bomb|논리]]적 테이블 제공 | 원천 시스템의 [[005_schema|스키마]] 맵핑 |
| [[195_federated_query_data_fabric_distributed_join|연방 쿼리]] ([[195_federated_query_data_fabric_distributed_join|Federated Query]]) | 여러 소스에 [[136_variance|분산]]된 [[001_dikw_pyramid|데이터]]를 조인하여 처리 | [[136_variance|분산]] [[298_qkv_attention|쿼리]] 엔진 (Presto, Trino 등) |
| [[298_qkv_attention|쿼리]] 최적화 (Optimization) | [[001_dikw_pyramid|데이터]] 이동을 최소화하는 최적 경로 계산 | 푸시다운(Push-down) 최적화 |
| 보안 제어 ([[283_security_tactics|Security]]) | 가상 계층에서 통합 권한 관리 | 로우/컬럼 레벨 접근 제어 |

- **📢 섹션 요약 비유**: 외국인 가이드들이 여러 명 있어도 통역사([[247_data_virtualization_federated_query|Data Virtualization]]) 한 명만 있으면 내가 한국말로 질문해도 모든 답을 한 번에 들을 수 있는 원리다.

---

## Ⅲ. 비교 및 연결

전통적인 [[001_dikw_pyramid|데이터]] 통합 방식인 ETL과 [[015_virtualization|가상화]] 방식은 보완적인 [[083_relationship_in_er_model|관계]]에 가깝다.

| 항목 | [[215_etl_vs_elt_pipeline|ETL]] 기반 통합 (Physical) | [[360_data_virtualization|데이터 가상화]] (Logical) |
|:---|:---|:---|
| [[001_dikw_pyramid|데이터]] 위치 | 분석계 저장소로 [[016_replication_factor|복제]]됨 | 원천 시스템에 그대로 유지 |
| [[001_dikw_pyramid|데이터]] 신선도 | 배치 주기에 따라 [[015_지연_데이터_관점|지연]] 발생 | 실시간(Real-time) 조회 가능 |
| 구현 속도 | [[123_pipe|파이프]]라인 설계 등으로 느림 | 가상 뷰 [[087_process_state_transition|생성]]만으로 즉시 가능 |
| [[282_performance_tactics|성능]] 특성 | [[016_replication_factor|복제]]된 [[001_dikw_pyramid|데이터]]로 고속 처리 가능 | 네트워크 및 원천 시스템 [[282_performance_tactics|성능]]에 의존 |

최근에는 대용량 이력 [[001_dikw_pyramid|데이터]]는 ETL로 처리하고, 최신 운영 [[001_dikw_pyramid|데이터]]는 [[015_virtualization|가상화]]로 연결하는 **하이브리드 아키텍처**가 주를 이룬다.

- **📢 섹션 요약 비유**: 자주 쓰는 생필품은 미리 장을 봐서 냉장고([[215_etl_vs_elt_pipeline|ETL]])에 넣어두고, 신선 식품이나 배달 음식은 필요할 때 즉시 주문([[247_data_virtualization_federated_query|Data Virtualization]])하는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 **원천 시스템 부하**와 **응답 속도**를 가장 신중하게 판단해야 한다. [[015_virtualization|가상화]] 계층에서 복잡한 조인([[521_join|Join]])을 수행할 경우 원천 DB에 과도한 [[298_qkv_attention|쿼리]] 부하를 줄 수 있기 때문이다.

### [[435_checklist_based_testing|체크리스트]]
1. 원천 시스템의 실시간 상태를 분석 대시보드에 즉시 반영해야 하는가?
2. [[001_dikw_pyramid|데이터]] 소스가 너무 다양하여 일일이 ETL을 구축하기에 비용이 과다한가?
3. 원천 시스템의 CPU/Memory 여유가 [[015_virtualization|가상화]] [[298_qkv_attention|쿼리]]를 받아낼 만큼 충분한가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- 수십 억 건의 대규모 [[001_dikw_pyramid|데이터]]를 조인하면서 [[015_virtualization|가상화]]만 고집하는 경우. 이럴 때는 [[001_dikw_pyramid|데이터]]를 물리적으로 한곳에 모아 인덱싱하는 것이 [[282_performance_tactics|성능]] 면에서 훨씬 유리하다.

- **📢 섹션 요약 비유**: 아무리 스트리밍이 좋아도 초고화질 대용량 영화를 끊김 없이 보려면 미리 다운로드받아 두는 것이 속 편한 것과 같다.

---

## Ⅴ. 기대효과 및 결론

[[360_data_virtualization|데이터 가상화]]는 [[104_da_as_is_analysis|데이터 아키텍처]]에 **유연성(Agility)**과 **속도**를 부여한다. 비즈니스 요구사항이 바뀔 때마다 물리적 인프라를 새로 구축할 필요 없이 [[369_logic_bomb|논리]]적인 모델링만으로 대응할 수 있기 때문이다.

결론적으로, [[360_data_virtualization|데이터 가상화]]는 [[212_data_fabric_virtualization|데이터 패브릭]]을 실현하는 가장 핵심적인 기술이며, [[001_dikw_pyramid|데이터]] [[002_silo_hyeonhyung|사일로]]를 허물고 전사적 '단일 진실 공급원(SSOT)'을 구축하는 지름길이다.

- **📢 섹션 요약 비유**: 수만 권의 책을 직접 소유하지 않아도 검색 한 번으로 원하는 문장을 찾아내는 구글 검색 포털처럼, 기업 [[001_dikw_pyramid|데이터]]도 검색과 연결의 시대로 진입한 것이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[195_federated_query_data_fabric_distributed_join|연방 쿼리]] ([[195_federated_query_data_fabric_distributed_join|Federated Query]]) | [[360_data_virtualization|데이터 가상화]]의 핵심 [[298_qkv_attention|쿼리]] 처리 방식 |
| 푸시다운 (Push-down) | 연산을 최대한 원천 DB에서 수행하게 하여 [[001_dikw_pyramid|데이터]] 이동을 줄이는 기술 |
| [[001_dikw_pyramid|데이터]] [[198_abstraction_control_data_process|추상화]] | 복잡한 물리 구조를 사용자에게 쉬운 [[369_logic_bomb|논리]] 구조로 변환하는 과정 |

### 📈 관련 키워드 및 발전 흐름도

```
물리적 ETL 복사 - 지연·중복 스토리지 문제
    │
    ▼
연합 쿼리 (Federated Query) 초기 방식
    │
    ▼
데이터 가상화 레이어 - 논리적 단일 뷰 제공
    │
    ▼
Denodo/Dremio - 실시간 쿼리 푸시다운 최적화
    │
    ▼
Data Fabric 구성 요소로 편입·진화
```

> **키워드**: [[247_data_virtualization_federated_query|Data Virtualization]], Logical [[208_data_warehouse_schema_on_write_inmon|Data Warehouse]], [[195_federated_query_data_fabric_distributed_join|Federated Query]], Denodo, Dremio, Query Pushdown

### 👶 어린이를 위한 3줄 비유 설명
1. 전 세계 친구들의 일기장을 내가 다 가지고 있으려면 가방이 너무 무거워요.
2. 대신 마법 거울을 통해서 친구들의 일기장을 바로 비춰보기로 했어요.
3. 거울만 보면 친구들이 지금 일기에 뭐라고 쓰는지 바로 알 수 있답니다!
