+++
title = "110. 무중단 DB 스키마 롤아웃 (Zero-Downtime) - Expand and Contract 패턴"
date = 2026-04-19

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Expand and Contract 패턴은 DB [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 변경([DDL](/knowledge-base/studynote/05_database/01_db_architecture_relational/020_ddl/))을 <strong>확장(Expand) -> 병행(Migrate) -> 수축(Contract)</strong>의 3단계로 분리하여, 신·구버전 앱이 동시에 운영 DB를 사용해도 <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 중단 없이(<a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/">Zero</a>-Downtime)</strong> [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)를 진화시키는 기법이다.
> 2. **가치**: 컬럼 삭제·이름 변경을 가장 마지막 단계로 미룸으로써, 배포 중 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)하더라도 <strong>DB <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>가 그대로 남아 장애를 방지</strong>하며, 이는 블루/그린 배포의 DB 판 완성형이다.
> 3. **판단 포인트**: Flyway·Liquibase로 각 단계를 <strong><a href="/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/">버전</a> 관리(V1__expand, V2__migrate, V3__contract)</strong>하고 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD에 통합하며, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 마이그레이션은 [Lazy](/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) Migration 또는 DB [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)로 실시간 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)한다.

---

## Ⅰ. 개요 및 필요성

앱은 블루/그린·[카나리 배포](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/)로 무중단이 가능하지만, <strong>DB <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/">스키마</a>(<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/020_ddl/">DDL</a>)는 갑자기 바꾸면 구버전 앱이 에러</strong>를 뿜는다. "컬럼 이름을 `name` -> `full_name`으로 바꿔야 하는데, 구버전 앱은 아직 `name`을 읽고 있다." 이때 점검 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 띄우는 것은 현대 DevOps의 목표가 아니다.

```text
+-------------------------------------------------------+
|       Expand and Contract 3단계 흐름도                 |
+-------------------------------------------------------+
|  Phase 1: Expand (확장)                               |
|   DB: full_name 컬럼 추가 (name 그대로 유지)          |
|   App v1: name 읽기/쓰기 (변경 없음)                  |
|                                                       |
|  Phase 2: Migrate (병행)                              |
|   DB: name -> full_name 데이터 복사 (트리거/배치)      |
|   App v2: full_name 쓰기 + name에도 동시 기록         |
|   (구버전 앱 호환 유지)                               |
|                                                       |
|  Phase 3: Contract (수축)                             |
|   App v2 전면 배포 확인 후                            |
|   DB: name 컬럼 삭제 (청소)                           |
|   App v2: full_name만 사용                            |
|                                                       |
|  롤백 안전: Phase 1~2에서 문제 시 name 그대로 활용    |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 레고 성의 빨간 기둥을 파란색으로 바꾸고 싶을 때, 성을 무너뜨리지 않고 **파란 기둥을 옆에 세우고(Expand)**, 사람들을 파란 기둥으로 옮긴 뒤(Migrate), 빨간 기둥을 조용히 빼내는(Contract) 공사법이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 3단계 상세

| 단계 | DB 변경 | 앱 변경 | [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) |
|:---|:---|:---|:---|
| **Expand** | 새 컬럼 추가 (구 컬럼 유지) | 변경 없음 | 구버전 100% 호환 |
| **Migrate** | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) ([트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)/배치) | 신버전 배포 (양쪽 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)) | 신·구 동시 호환 |
| **Contract** | 구 컬럼 삭제 | 구버전 완전 제거 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 후 | 신버전 전용 |

### [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 마이그레이션 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

| [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 방식 | 장점 | 단점 |
|:---|:---|:---|:---|
| **배치 마이그레이션** | 일괄 UPDATE SQL | 간단 | 대량 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 시 DB 부하 |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/">Lazy</a> Migration</strong> | 앱이 읽을 때 없으면 복사 | 부하 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) | 완료 시점 불확실 |
| <strong>DB <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/">트리거</a></strong> | INSERT/UPDATE 시 자동 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) | 실시간 | [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 관리 복잡 |

- **📢 섹션 요약 비유**: 배치는 이사할 때 트럭 한 번에 짐을 다 옮기는 것이고, Lazy는 필요할 때만 하나씩 가져오는 것이며, [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)는 매일 자동으로 짐을 옮기는 로봇이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 빅뱅 배포 | Expand & Contract |
|:---|:---|:---|
| **방식** | 점검 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) -> 한 번에 변경 | <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 유지하며 단계적</strong> |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/">호환성</a></strong> | 고려 안 함 | **구·신버전 동시 호환** |
| **복잡도** | 낮음 | 높음 (3단계) |
| <strong><a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/">롤백</a></strong> | DB 복원 매우 어려움 | <strong>매우 쉬움 (<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 유실 0)</strong> |
| **적합 환경** | 소규모·저위험 | **금융·이커머스·고가용** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD 통합 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. <strong>Flyway/Liquibase</strong>로 SQL 스크립트를 `V1__expand.sql`, `V2__migrate.sql`, `V3__contract.sql`로 [버저닝](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/317_versioning_data_model_design/).
2. <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/">파이프</a>라인</strong>: 앱 배포 **전에** Expand, 앱 배포 **후** Migrate, 구버전 제거 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 후 Contract.
3. **테스트**: "구버전 앱 + 신버전 DB" 조합으로 [통합 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/400_integration_testing/) 필수 실행.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **Contract 서두르기**: 구버전 앱이 아직 남아있는데 구 컬럼 삭제 -> 구버전 앱 에러 폭발.
- <strong>마이그레이션 미완료 <a href="/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a> 누락</strong>: 10만 건 중 1천 건만 복사된 상태에서 Contract -> [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소실.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 빅뱅 배포 | E&C 패턴 | 개선 |
|:---|:---|:---|:---|
| [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중단 | 30분~수시간 | **0분** | 100% |
| [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 안전성 | 낮음 | **매우 높음** | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유실 0 |
| 배포 빈도 | 월 1회 | **일 수회** | [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 가속 |

무중단 DB [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 롤아웃은 "진정한 [지속적 배포](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/099_continuous_deployment_cd/)(CD)"를 완성하는 마지막 퍼즐이다. 앱은 자유롭게 배포하면서 DB 때문에 점검을 잡는다면, 그것은 반쪽짜리 DevOps다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong>Blue/Green <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/">Deployment</a></strong> | 앱 [무중단 배포](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/082_zero_downtime_deployment_rolling_blue_green_canary/)의 짝꿍 |
| **Flyway / Liquibase** | DB 마이그레이션 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 도구 |
| <strong>하위 <a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/">호환성</a> (Backward <a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/">Compatibility</a>)</strong> | Expand 단계에서 반드시 보장해야 할 성질 |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/195_canary_release_deployment/">Canary Release</a></strong> | DB 변경 영향도를 조금씩 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 배포 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| **Feature Toggle** | 신·구 로직 전환을 코드 레벨에서 제어 |

### 📈 관련 키워드 및 발전 흐름도

```text
[점검 페이지 시대 — DB 변경 시 서비스 전면 중단]
    |
    v
[Expand and Contract 패턴 (2010s) — 단계적 스키마 진화]
    |
    v
[Flyway/Liquibase CI/CD 통합 (2015~) — 마이그레이션 자동화]
    |
    v
[현재: Online DDL + Ghost/pt-osc — 대용량 테이블 무중단 변경]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 레고 성의 빨간 기둥을 파란색으로 바꾸고 싶은데, 성을 무너뜨리기 싫어요.
2. 먼저 파란 기둥을 **옆에 하나 더 세우고**, 사람들이 파란 기둥을 쓰게 한 다음에,
3. 마지막에 쓸모없어진 빨간 기둥을 **조용히 빼내는** 아주 조심스러운 공사 방법이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 110 / 373

<- **이전**: [109. SBOM 추출 파이프라인 (Software Bill of Materials) - 공급망 보안 의무화](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/109_sbom_extraction_pipeline/)
**다음**: [111. 마이크로 프론트엔드 배포 (Micro Frontends Deployment) - 독립 배포·Module Federation](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/111_micro_frontends_deployment/) ->

---
