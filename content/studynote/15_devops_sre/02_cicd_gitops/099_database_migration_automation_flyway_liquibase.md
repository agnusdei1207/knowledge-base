---
title: "099. Database Migration Automation Flyway Liquibase"
date: "2026-03-04"
tags:
  - "cicd-gitops"
  - "studynote-devops-sre"
weight: 99
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [데이터베이스 마이그레이션](/studynote/15_devops_sre/05_devsecops/271_ddl_liquibase/) 자동화는 소스코드처럼 DB [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)([DDL](/studynote/05_database/01_db_architecture_relational/020_ddl/)/[DML](/studynote/12_it_management/02_itsm_itil/867_dml/))의 변경 이력을 [형상 관리](/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)(Version Control)하여 상태를 일치시키는 시스템이다.
> 2. **가치**: 애플리케이션 코드가 배포될 때 DB [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 변경도 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 안에서 함께 자동 실행되므로, 개발 환경과 운영 환경 간의 불일치 및 휴먼 에러를 원천 차단한다.
> 3. **판단 포인트**: 직관적인 SQL 작성이 유리한 소규모 팀은 Flyway를, [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)된 구조와 강력한 자동 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 기능이 필요한 복잡한 엔터프라이즈 환경은 Liquibase를 선택하는 것이 합리적이다.

## Ⅰ. 개요 및 필요성
과거에는 애플리케이션 코드는 Git으로 관리하면서도, [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)는 DBA나 개발자가 수동으로 SQL 스크립트를 서버에 접속해 실행했다. 이런 방식은 특정 환경(Dev, Staging, Prod)에서 테이블 추가를 깜빡하거나 컬럼 이름이 달라 장애를 유발하는 핵심 원인이었다. 배포 주기가 하루에도 수십 번씩 일어나는 현대의 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD([지속적 통합](/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/)/배포) 환경에서는 코드와 DB가 정확히 한 몸처럼 움직여야 한다. 이를 위해 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 변경 이력을 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)으로 통제하는 "코드로서의 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)([Database](/studynote/05_database/04_transactions_concurrency/501_database/) [as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) [Code](/studynote/02_operating_system/02_process_thread/082_process_memory_structure/))" 도구들이 필수적으로 등장했다.

- **📢 섹션 요약 비유**: 요리(앱) 레시피만 완벽하게 적어놓고 주방 도구(DB)는 그때그때 손으로 대충 맞추다가 실수가 잦아지니, 아예 주방 세팅 순서까지 번호를 매겨 레시피에 포함한 것이다.

## Ⅱ. 아키텍처 및 핵심 원리
DB 마이그레이션 도구의 핵심은 타겟 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 안에 <strong><a href="/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/">버전</a> <a href="/studynote/05_database/01_db_architecture_relational/012_metadata/">메타데이터</a> 테이블(<a href="/studynote/05_database/04_transactions_concurrency/505_schema/">Schema</a> History Table)</strong>을 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하여 [현재 상태](/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)를 추적하는 것이다. 애플리케이션이 기동되거나 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인이 실행될 때, 도구는 프로젝트에 있는 스크립트 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)들의 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)과 DB 내의 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)을 비교한다.

```text
+-------------------------------------------------------------+
|          DB 마이그레이션 자동화 흐름 (Flyway 예시)          |
+-------------------------------------------------------------+
|  [Git Repository]                                           |
|  +-- V1__create_users.sql                                   |
|  +-- V2__add_email_col.sql  <-- (신규 스크립트 커밋)         |
|                                                             |
|       |                                                     |
|       v CI/CD Pipeline (App + Migration Tool 실행)          |
|                                                             |
|  [Target Database]                                          |
|  +----------------------+  (비교) +----------------------+  |
|  | 스키마 히스토리 테이블 | <------> | 아직 적용 안 된 V2 |  |
|  | (Current: V1)        |  (실행) | 발견 후 DDL 실행   |  |
|  +----------------------+         +----------------------+  |
|       |                                                     |
|       v 마이그레이션 완료 후 V2로 상태 업데이트             |
+-------------------------------------------------------------+
```

이 다이어그램은 마이그레이션 엔진이 타겟 DB의 상태를 검사하고, 부족한 변경분(V2)만을 순차적으로 실행한 뒤 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)를 갱신하는 [멱등성](/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/)([Idempotency](/studynote/15_devops_sre/04_iac_cloud_native/194_idempotency/)) 보장 메커니즘을 보여준다. 스크립트가 한 번 성공적으로 적용되면 다시 실행되지 않는다.

- **📢 섹션 요약 비유**: 책갈피([메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 테이블)를 꽂아두고, 다음번에 읽을 때는 무조건 책갈피 꽂힌 다음 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)(새로운 스크립트)부터 차례대로 읽어 나가는 안전한 독서법이다.

## Ⅲ. 비교 및 연결
시장 표준으로 자리 잡은 Flyway와 Liquibase는 철학이 다르다. Flyway는 SQL 본연의 강력함을, Liquibase는 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 종류에 구애받지 않는 [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)와 복원력([Rollback](/studynote/02_operating_system/05_deadlock/313_rollback/))을 강조한다.

| 비교 항목 | Flyway | Liquibase |
| :--- | :--- | :--- |
| **스크립트 언어** | Plain SQL 중심 (`.sql`) | XML, YAML, [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) 중심 (SQL도 지원) |
| <strong><a href="/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/">추상화</a> 수준</strong> | 특정 DB(MySQL, [Oracle](/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/)) 종속적 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) | DB 독립적인 [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 태그 사용 |
| <strong><a href="/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/">롤백</a> 지원</strong> | 무료 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)은 제한적, 수동 스크립트 필요 | 구조화된 포맷 덕분에 <strong>자동 <a href="/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/">롤백</a>(<a href="/studynote/11_design_supervision/06_exam_summary/393_undo/">Undo</a>)</strong> 지원 |
| **진입 장벽** | 매우 낮음 (SQL만 알면 즉시 도입) | 약간 높음 (전용 태그 학습 필요) |

인프라를 코드로 관리하는 [IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)([Terraform](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) 등)가 하드웨어를 통제한다면, 마이그레이션 도구는 애플리케이션 내부의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조를 코드로 통제하여 [데브옵스](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 생태계의 마지막 퍼즐을 완성한다.

- **📢 섹션 요약 비유**: Flyway가 현지어(SQL)로 유창하게 직접 말하는 직관적인 가이드라면, Liquibase는 조금 복잡하지만 어떤 나라에 가든 알아서 번역([추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/))해주고 실수하면 되돌려주는 만능 통역기다.

## Ⅳ. 실무 적용 및 기술사 판단
실무 환경에서는 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 마이그레이션 시 기존 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 중단되는 현상을 가장 경계해야 한다. 컬럼의 이름을 바꾸거나 삭제할 때 한 번에 실행하면 애플리케이션의 구버전과 충돌하여 에러가 발생한다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) 및 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
1. <strong><a href="/studynote/15_devops_sre/02_cicd_gitops/082_zero_downtime_deployment_rolling_blue_green_canary/">무중단 배포</a> 패턴 (Expand-and-Contract)</strong>: 기존 컬럼을 놔둔 채 새 컬럼을 추가(Expand)하여 구/신버전 앱이 동시에 동작하게 한 뒤, 안전해지면 기존 컬럼을 삭제(Contract)하도록 스크립트를 분리했는가?
2. **보안 및 권한**: 마이그레이션을 수행하는 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 계정(Role)이 전체 DB 삭제 권한을 갖지 않도록 [최소 권한 원칙](/studynote/09_security/01_intro_principles/010_least_privilege/)([IAM](/studynote/09_security/11_iam_access_control/526_iam/))을 적용했는가?
3. <strong><a href="/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a></strong>: 한 번 적용되어 DB에 기록된 과거의 마이그레이션 스크립트(V1.sql)의 내용을 뒤늦게 수정하는 행위. ([체크섬](/studynote/01_computer_architecture/02_data_representation_arithmetic/112_checksum/) 오류를 발생시켜 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인이 붕괴됨)

- **📢 섹션 요약 비유**: 무중단 DB 배포는 다리를 부수고 새로 짓는 것이 아니다. 옆에 새 다리를 지어 차들을 안전하게 옮긴 뒤(Expand), 밤에 몰래 옛날 다리를 허무는(Contract) 치밀한 공사다.

## Ⅴ. 기대효과 및 결론
DB 마이그레이션 자동화는 개발과 운영 사이의 단절을 해결하는 [데이터옵스](/studynote/14_data_engineering/04_mlops/196_dataops_dbt_ci_cd_data_testing/)([DataOps](/studynote/12_it_management/05_security_compliance/965_dataops/))의 핵심 기반이다. 이를 통해 개발자는 [코드 리뷰](/studynote/04_software_engineering/06_software_architecture/330_code_review/) 과정에서 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 변경 사항을 함께 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)할 수 있고, 인프라 배포의 재현성이 100% 보장된다. [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 관리는 더 이상 DBA만의 수동 작업이 아니라, [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인에 내재화된 자동화 프로세스로 다루어야 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 확보할 수 있다.

- **📢 섹션 요약 비유**: [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 변경 작업이 눈 가리고 하는 폭탄 돌리기에서, 튼튼한 안전벨트([버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리)를 매고 정해진 궤도를 달리는 롤러코스터로 바뀌게 된다.

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
| :--- | :--- |
| [Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) History Table | Flyway나 Liquibase가 실행 이력을 기록해두는 타겟 DB 내의 메타 테이블 |
| Expand-and-Contract | 무중단 DB [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 변경을 위해 추가 단계와 삭제 단계를 분리하는 [디자인 패턴](/studynote/04_software_engineering/04_testing_quality/251_design_patterns_gof_overview/) |
| [IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) ([Infrastructure as Code](/studynote/15_devops_sre/02_cicd_gitops/062_infrastructure_as_code/)) | 인프라 구조를 코드로 관리하듯, DB 구조를 코드로 관리하는 사상적 기반 |
| [멱등성](/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/) ([Idempotency](/studynote/15_devops_sre/04_iac_cloud_native/194_idempotency/)) | 마이그레이션 스크립트를 여러 번 실행해도 한 번만 적용되도록 보장하는 특성 |

### 📈 관련 키워드 및 발전 흐름도
```text
DBA의 수동 DDL 실행 및 형상 관리 부재
    |
    v
Database as Code (코드로서의 DB 사상 대두)
    |
    v
Flyway, Liquibase 도입 (파이프라인 통합 및 자동화)
    |
    v
Expand-and-Contract 적용 (무중단 데이터베이스 배포)
    |
    v
DataOps 및 AI 기반 스키마 최적화·보안 스캐닝 결합
```
이 흐름도는 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 변경이 수동 작업에서 코드 기반 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인으로 편입되고, 궁극적으로 무중단 및 지능형 DataOps로 진화하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 게임 캐릭터의 능력치를 바꾸려면 게임사에서 서버의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 고쳐야 해요.
2. 예전에는 사람이 일일이 고치다가 실수도 했지만, 이제는 '자동 명령서'를 보내서 기계가 순서대로 고쳐줘요.
3. 이 명령서에는 번호가 붙어 있어서, 순서가 섞이지 않고 딱 한 번씩만 똑똑하게 업데이트된답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 99 / 373

<- **이전**: [98. 롤백 (Rollback) 전략 - 파이프라인 에러율 기반 자동 복구](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)
**다음**: [100. 멀티 리전 (Multi-Region) 배포 파이프라인 - 글로벌 고가용성(DR) 및 레이턴시 최적화](/studynote/15_devops_sre/02_cicd_gitops/100_multi_region_deployment_pipeline_disaster_recovery/) ->

---
