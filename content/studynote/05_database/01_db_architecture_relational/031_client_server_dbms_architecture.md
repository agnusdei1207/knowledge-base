---
title: "031. Client Server Dbms Architecture"
date: "2026-04-29"
tags:
  - "studynote-database"
weight: 31
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 클라이언트-서버 [DBMS](/studynote/05_database/04_transactions_concurrency/502_dbms/) 아키텍처는 DB 엔진을 서버에 중앙 집중화하고, 클라이언트는 SQL 요청만 전송하는 구조다. [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 공유 방식(모든 클라이언트가 DB [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 직접 접근)의 [동시성](/studynote/15_devops_sre/01_culture_methodology/014_concurrency/)·보안·[무결성](/studynote/09_security/01_intro_principles/003_integrity/) 문제를 해결했다.
> 2. **가치**: 2-Tier(클라이언트-DB 서버), 3-Tier(클라이언트-앱서버-DB 서버), N-Tier([마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)) 구조로 발전하며 확장성과 [보안성](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/)이 높아졌다. 3-Tier는 현대 웹 애플리케이션의 표준 구조다.
> 3. **판단 포인트**: [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 연결(Connection)은 비용이 크다. 커넥션 풀(Connection Pool)은 미리 N개 연결을 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)해두고 재사용하여 연결 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 오버헤드를 제거한다. 적절한 풀 크기가 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 핵심이다.

---

## Ⅰ. 개요 및 필요성

```text
아키텍처 발전:

1-Tier (파일 공유):
  [앱+DB+데이터 모두 한 기계]
  -> 다중 사용자 불가

2-Tier (C/S):
  [클라이언트 앱] --SQL--> [DB 서버]
  -> 클라이언트가 두꺼움 (Fat Client)

3-Tier:
  [브라우저/앱] --HTTP--> [앱 서버] --SQL--> [DB 서버]
  -> 표준 웹 아키텍처

N-Tier (MSA):
  [클라이언트] -> [API 게이트웨이] -> [서비스A,B,C] -> [DB A,B,C]
  -> 서비스별 독립 DB
```

- **📢 섹션 요약 비유**: 아키텍처 발전은 음식점 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 방식이다. 혼자 밥 해먹기(1-Tier), 식당 가서 주문(2-Tier), 배달앱으로 주문(3-Tier), 여러 배달 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 연동([MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/)) 순으로 복잡성과 확장성이 증가한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 커넥션 풀 작동 원리

```text
커넥션 풀 없이:
  요청마다 새 연결 생성 (100ms+) -> 응답 지연

커넥션 풀 사용:
  시작 시 10개 연결 미리 생성 (DB 서버와 TCP 유지)
  요청: 풀에서 유휴 연결 즉시 획득 (1ms 미만)
  완료: 연결 반납 (close 아닌 반환)

주요 파라미터:
  initialSize:    최초 연결 수 (5)
  minIdle:        최소 유휴 연결 (5)
  maxActive:      최대 연결 수 (20)
  maxWait:        연결 대기 최대 시간 (3000ms)
  validationQuery: 연결 유효성 확인 쿼리
```

### DB 미들웨어 계층

| 계층 | 역할 |
|:---|:---|
| **JDBC/ODBC** | 표준 DB 접근 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) |
| **ORM** | 객체-[관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 매핑 (Hibernate, JPA) |
| **커넥션 풀** | 연결 재사용 (HikariCP, DBCP) |
| <strong><a href="/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/">프록시</a></strong> | 연결 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)·[캐싱](/studynote/02_operating_system/08_storage_and_io_systems/456_caching/) (ProxySQL, PgBouncer) |
| <strong><a href="/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/">서비스 메시</a></strong> | [MSA DB](/studynote/13_cloud_architecture/05_data_engineering/284_msa_db/) 연결 관리 |

- **📢 섹션 요약 비유**: 커넥션 풀은 택시 대기소다. 항상 10대의 택시(DB 연결)가 대기하고 있어서 손님(요청)이 오면 즉시 배차(연결 제공)한다. 매번 새 택시를 불러오는 것(새 연결 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/))보다 훨씬 빠르다.

---

## Ⅲ. 비교 및 연결

| 비교 | 2-Tier | 3-Tier | [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) |
|:---|:---|:---|:---|
| 클라이언트 | [Fat](/studynote/02_operating_system/09_file_system/525_fat_file_allocation_table/) [Client](/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/) | Thin [Client](/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/) | [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) [Client](/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/) |
| 확장성 | 낮음 | 중간 | 높음 |
| 보안 | DB 직접 노출 | 앱 서버 방어 | [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이 |
| DB 수 | 1개 공유 | 1~2개 공유 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 독립 |

- **📢 섹션 요약 비유**: 2/3/[MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 계층은 회사 조직 구조다. 모두가 직접 사장에게 보고(2-Tier), 팀장을 통해 보고(3-Tier), 각 팀이 독립적으로 운영([MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/))으로 확장성이 달라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### HikariCP 최적 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) (Spring Boot)

```yaml
spring:
  datasource:
    hikari:
      pool-name: HikariPool-1
      maximum-pool-size: 10      # CPU 코어 수 × 2~3
      minimum-idle: 5
      connection-timeout: 3000   # 3초
      idle-timeout: 600000       # 10분 유휴 후 제거
      max-lifetime: 1800000      # 30분 후 연결 교체
      validation-timeout: 5000
      connection-test-query: "SELECT 1"
```

### 읽기-[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 분리 아키텍처

```text
쓰기 연결 풀 -> Primary DB (쓰기 전용)
읽기 연결 풀 -> Replica DB×N (읽기 분산)

장점:
  - 읽기 쿼리 부하 분산
  - Primary DB 쓰기 성능 보호
  - 읽기 쿼리 다중 복제본 병렬 처리
```

- **📢 섹션 요약 비유**: 읽기-[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 분리는 복사 센터 운영이다. 원본 작성(Primary/[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/))과 복사 출력(Replica/읽기)을 분리하여, 복사 수요가 많아도 원본 작업에 방해가 없다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong> | 커넥션 풀로 연결 오버헤드 제거 |
| **확장성** | 3-Tier/MSA로 수평 확장 용이 |
| **보안** | DB 서버를 클라이언트로부터 격리 |

[서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)·[엣지 컴퓨팅](/studynote/12_it_management/05_security_compliance/235_edge_computing_smart_factory/) 환경에서 DB 커넥션 풀이 새로운 도전을 받고 있다. [Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) 함수가 수천 개 동시 실행 시 커넥션 폭발(Connection Storm)이 발생하며, AWS RDS [Proxy](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)·PlanetScale [serverless](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) driver 같은 [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 전용 DB [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)가 해결책으로 등장했다.

- **📢 섹션 요약 비유**: [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) DB [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 대형 행사 주차 관리다. 수천 명 동시 방문([Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) 함수)에 주차 공간(DB 연결)이 부족하면 대기 줄이 생긴다. DB [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)(주차 대행)가 연결을 중간에서 효율적으로 관리한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **커넥션 풀** | DB 연결 재사용 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화 |
| **HikariCP** | Spring Boot 표준 커넥션 풀 |
| <strong>읽기-<a href="/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> 분리</strong> | Primary/Replica 부하 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) |
| <strong>RDS <a href="/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/">Proxy</a></strong> | [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/) 환경 DB 연결 관리 |
| **ORM** | 객체-DB 매핑 [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 계층 |

### 📈 관련 키워드 및 발전 흐름도

```text
[파일 공유 DB — 1-Tier, 동시성 문제]
    |
    v
[2-Tier C/S — DB 서버 중앙화, Fat Client]
    |
    v
[3-Tier — 앱 서버 추가, 커넥션 풀, 표준 웹 구조]
    |
    v
[MSA — 서비스별 독립 DB, API 게이트웨이]
    |
    v
[서버리스 DB 프록시 — Lambda 커넥션 폭발 해결]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 클라이언트-서버 DB는 식당 주문 시스템이에요 — 손님(클라이언트)이 주문하면 주방(DB 서버)에서 처리해요!
2. 커넥션 풀은 택시 대기소예요 — 미리 연결을 만들어둬서 요청이 오면 즉시 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)해요!
3. 현대 앱은 3-Tier로 브라우저->앱서버->DB 서버 구조로 동작해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 31 / 600

<- **이전**: [30. 데이터 무결성과 보안 — 데이터베이스 안전의 두 축](/studynote/05_database/01_db_architecture_relational/030_data_integrity_security/)
**다음**: [TP 모니터 (Transaction Processing Monitor)](/studynote/05_database/01_db_architecture_relational/032_tp_monitor/) ->

---
