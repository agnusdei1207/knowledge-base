---
title: 99. 데이터베이스 마이그레이션 자동화 (Flyway, Liquibase) - CI/CD 기반 스키마 형상 관리
date: '2026-03-04'
tags:
- cicd-gitops
- studynote-devops-sre
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[271_ddl_liquibase|데이터베이스 마이그레이션]] 자동화는 소스코드처럼 DB [[005_schema|스키마]]([[020_ddl|DDL]]/[[083_dml|DML]])의 변경 이력을 [[020_software_configuration_management|형상 관리]](Version Control)하여 상태를 일치시키는 시스템이다.
> 2. **가치**: 애플리케이션 코드가 배포될 때 DB [[005_schema|스키마]] 변경도 [[123_pipe|파이프]]라인 안에서 함께 자동 실행되므로, 개발 환경과 운영 환경 간의 불일치 및 휴먼 에러를 원천 차단한다.
> 3. **판단 포인트**: 직관적인 SQL 작성이 유리한 소규모 팀은 Flyway를, [[198_abstraction_control_data_process|추상화]]된 구조와 강력한 자동 [[098_rollback_strategy_pipeline_error_threshold|롤백]] 기능이 필요한 복잡한 엔터프라이즈 환경은 Liquibase를 선택하는 것이 합리적이다.

## Ⅰ. 개요 및 필요성
과거에는 애플리케이션 코드는 Git으로 관리하면서도, [[002_database_definition|데이터베이스]] [[005_schema|스키마]]는 DBA나 개발자가 수동으로 SQL 스크립트를 서버에 접속해 실행했다. 이런 방식은 특정 환경(Dev, Staging, Prod)에서 테이블 추가를 깜빡하거나 컬럼 이름이 달라 장애를 유발하는 핵심 원인이었다. 배포 주기가 하루에도 수십 번씩 일어나는 현대의 [[090_configuration_item|CI]]/CD([[076_ci_continuous_integration|지속적 통합]]/배포) 환경에서는 코드와 DB가 정확히 한 몸처럼 움직여야 한다. 이를 위해 [[005_schema|스키마]] 변경 이력을 [[288_version_ihl_tos_total_length|버전]]으로 통제하는 "코드로서의 [[002_database_definition|데이터베이스]]([[501_database|Database]] [[344_as_autonomous_system_asn|as]] [[082_process_memory_structure|Code]])" 도구들이 필수적으로 등장했다.

- **📢 섹션 요약 비유**: 요리(앱) 레시피만 완벽하게 적어놓고 주방 도구(DB)는 그때그때 손으로 대충 맞추다가 실수가 잦아지니, 아예 주방 세팅 순서까지 번호를 매겨 레시피에 포함한 것이다.

## Ⅱ. 아키텍처 및 핵심 원리
DB 마이그레이션 도구의 핵심은 타겟 [[002_database_definition|데이터베이스]] 안에 **[[288_version_ihl_tos_total_length|버전]] [[012_metadata|메타데이터]] 테이블([[505_schema|Schema]] History Table)**을 [[087_process_state_transition|생성]]하여 [[178_as_is_to_be_analysis|현재 상태]]를 추적하는 것이다. 애플리케이션이 기동되거나 [[090_configuration_item|CI]]/CD [[123_pipe|파이프]]라인이 실행될 때, 도구는 프로젝트에 있는 스크립트 [[501_file_definition_logical_record|파일]]들의 [[288_version_ihl_tos_total_length|버전]]과 DB 내의 [[288_version_ihl_tos_total_length|버전]]을 비교한다.

```text
┌─────────────────────────────────────────────────────────────┐
│          DB 마이그레이션 자동화 흐름 (Flyway 예시)          │
├─────────────────────────────────────────────────────────────┤
│  [Git Repository]                                           │
│  ├── V1__create_users.sql                                   │
│  ├── V2__add_email_col.sql  ◀─ (신규 스크립트 커밋)         │
│                                                             │
│       │                                                     │
│       ▼ CI/CD Pipeline (App + Migration Tool 실행)          │
│                                                             │
│  [Target Database]                                          │
│  ┌──────────────────────┐  (비교) ┌──────────────────────┐  │
│  │ 스키마 히스토리 테이블 │ ◀────▶ │ 아직 적용 안 된 V2 │  │
│  │ (Current: V1)        │  (실행) │ 발견 후 DDL 실행   │  │
│  └──────────────────────┘         └──────────────────────┘  │
│       │                                                     │
│       ▼ 마이그레이션 완료 후 V2로 상태 업데이트             │
└─────────────────────────────────────────────────────────────┘
```

이 다이어그램은 마이그레이션 엔진이 타겟 DB의 상태를 검사하고, 부족한 변경분(V2)만을 순차적으로 실행한 뒤 [[012_metadata|메타데이터]]를 갱신하는 [[171_idempotency_iac_terraform|멱등성]]([[194_idempotency|Idempotency]]) 보장 메커니즘을 보여준다. 스크립트가 한 번 성공적으로 적용되면 다시 실행되지 않는다.

- **📢 섹션 요약 비유**: 책갈피([[012_metadata|메타데이터]] 테이블)를 꽂아두고, 다음번에 읽을 때는 무조건 책갈피 꽂힌 다음 [[286_page_frame|페이지]](새로운 스크립트)부터 차례대로 읽어 나가는 안전한 독서법이다.

## Ⅲ. 비교 및 연결
시장 표준으로 자리 잡은 Flyway와 Liquibase는 철학이 다르다. Flyway는 SQL 본연의 강력함을, Liquibase는 [[002_database_definition|데이터베이스]] 종류에 구애받지 않는 [[198_abstraction_control_data_process|추상화]]와 복원력([[313_rollback|Rollback]])을 강조한다.

| 비교 항목 | Flyway | Liquibase |
| :--- | :--- | :--- |
| **스크립트 언어** | Plain SQL 중심 (`.sql`) | XML, YAML, [[343_json|JSON]] 중심 (SQL도 지원) |
| **[[198_abstraction_control_data_process|추상화]] 수준** | 특정 DB(MySQL, [[188_pl_sql_t_sql_procedural|Oracle]]) 종속적 [[298_qkv_attention|쿼리]] | DB 독립적인 [[198_abstraction_control_data_process|추상화]] 태그 사용 |
| **[[098_rollback_strategy_pipeline_error_threshold|롤백]] 지원** | 무료 [[288_version_ihl_tos_total_length|버전]]은 제한적, 수동 스크립트 필요 | 구조화된 포맷 덕분에 **자동 [[098_rollback_strategy_pipeline_error_threshold|롤백]]([[393_undo|Undo]])** 지원 |
| **진입 장벽** | 매우 낮음 (SQL만 알면 즉시 도입) | 약간 높음 (전용 태그 학습 필요) |

인프라를 코드로 관리하는 [[793_iac_idempotency_template|IaC]]([[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]] 등)가 하드웨어를 통제한다면, 마이그레이션 도구는 애플리케이션 내부의 [[001_dikw_pyramid|데이터]] 구조를 코드로 통제하여 [[652_devops_calms_culture|데브옵스]] 생태계의 마지막 퍼즐을 완성한다.

- **📢 섹션 요약 비유**: Flyway가 현지어(SQL)로 유창하게 직접 말하는 직관적인 가이드라면, Liquibase는 조금 복잡하지만 어떤 나라에 가든 알아서 번역([[198_abstraction_control_data_process|추상화]])해주고 실수하면 되돌려주는 만능 통역기다.

## Ⅳ. 실무 적용 및 기술사 판단
실무 환경에서는 [[005_schema|스키마]] 마이그레이션 시 기존 [[090_service_kubernetes_network_load_balancing|서비스]]가 중단되는 현상을 가장 경계해야 한다. 컬럼의 이름을 바꾸거나 삭제할 때 한 번에 실행하면 애플리케이션의 구버전과 충돌하여 에러가 발생한다.

### [[435_checklist_based_testing|체크리스트]] 및 [[128_water_scrum_fall_anti_pattern|안티패턴]]
1. **[[082_zero_downtime_deployment_rolling_blue_green_canary|무중단 배포]] 패턴 (Expand-and-Contract)**: 기존 컬럼을 놔둔 채 새 컬럼을 추가(Expand)하여 구/신버전 앱이 동시에 동작하게 한 뒤, 안전해지면 기존 컬럼을 삭제(Contract)하도록 스크립트를 분리했는가?
2. **보안 및 권한**: 마이그레이션을 수행하는 [[123_pipe|파이프]]라인 계정(Role)이 전체 DB 삭제 권한을 갖지 않도록 [[010_least_privilege|최소 권한 원칙]]([[526_iam|IAM]])을 적용했는가?
3. **[[128_water_scrum_fall_anti_pattern|안티패턴]]**: 한 번 적용되어 DB에 기록된 과거의 마이그레이션 스크립트(V1.sql)의 내용을 뒤늦게 수정하는 행위. ([[112_checksum|체크섬]] 오류를 발생시켜 [[123_pipe|파이프]]라인이 붕괴됨)

- **📢 섹션 요약 비유**: 무중단 DB 배포는 다리를 부수고 새로 짓는 것이 아니다. 옆에 새 다리를 지어 차들을 안전하게 옮긴 뒤(Expand), 밤에 몰래 옛날 다리를 허무는(Contract) 치밀한 공사다.

## Ⅴ. 기대효과 및 결론
DB 마이그레이션 자동화는 개발과 운영 사이의 단절을 해결하는 [[196_dataops_dbt_ci_cd_data_testing|데이터옵스]]([[324_dataops|DataOps]])의 핵심 기반이다. 이를 통해 개발자는 [[330_code_review|코드 리뷰]] 과정에서 [[005_schema|스키마]] 변경 사항을 함께 [[395_verification_process_review|검증]]할 수 있고, 인프라 배포의 재현성이 100% 보장된다. [[005_schema|스키마]] 관리는 더 이상 DBA만의 수동 작업이 아니라, [[123_pipe|파이프]]라인에 내재화된 자동화 프로세스로 다루어야 [[194_consistency_database_integrity|일관성]]을 확보할 수 있다.

- **📢 섹션 요약 비유**: [[002_database_definition|데이터베이스]] 변경 작업이 눈 가리고 하는 폭탄 돌리기에서, 튼튼한 안전벨트([[288_version_ihl_tos_total_length|버전]] 관리)를 매고 정해진 궤도를 달리는 롤러코스터로 바뀌게 된다.

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
| :--- | :--- |
| [[505_schema|Schema]] History Table | Flyway나 Liquibase가 실행 이력을 기록해두는 타겟 DB 내의 메타 테이블 |
| Expand-and-Contract | 무중단 DB [[005_schema|스키마]] 변경을 위해 추가 단계와 삭제 단계를 분리하는 [[251_design_patterns_gof_overview|디자인 패턴]] |
| [[793_iac_idempotency_template|IaC]] ([[062_infrastructure_as_code|Infrastructure as Code]]) | 인프라 구조를 코드로 관리하듯, DB 구조를 코드로 관리하는 사상적 기반 |
| [[171_idempotency_iac_terraform|멱등성]] ([[194_idempotency|Idempotency]]) | 마이그레이션 스크립트를 여러 번 실행해도 한 번만 적용되도록 보장하는 특성 |

### 📈 관련 키워드 및 발전 흐름도
```text
DBA의 수동 DDL 실행 및 형상 관리 부재
    │
    ▼
Database as Code (코드로서의 DB 사상 대두)
    │
    ▼
Flyway, Liquibase 도입 (파이프라인 통합 및 자동화)
    │
    ▼
Expand-and-Contract 적용 (무중단 데이터베이스 배포)
    │
    ▼
DataOps 및 AI 기반 스키마 최적화·보안 스캐닝 결합
```
이 흐름도는 [[005_schema|스키마]] 변경이 수동 작업에서 코드 기반 [[123_pipe|파이프]]라인으로 편입되고, 궁극적으로 무중단 및 지능형 DataOps로 진화하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 게임 캐릭터의 능력치를 바꾸려면 게임사에서 서버의 [[001_dikw_pyramid|데이터]]를 고쳐야 해요.
2. 예전에는 사람이 일일이 고치다가 실수도 했지만, 이제는 '자동 명령서'를 보내서 기계가 순서대로 고쳐줘요.
3. 이 명령서에는 번호가 붙어 있어서, 순서가 섞이지 않고 딱 한 번씩만 똑똑하게 업데이트된답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 99 / 373

← **이전**: [[098_rollback_strategy_pipeline_error_threshold|98. 롤백 (Rollback) 전략 - 파이프라인 에러율 기반 자동 복구]]
**다음**: [[100_multi_region_deployment_pipeline_disaster_recovery|100. 멀티 리전 (Multi-Region) 배포 파이프라인 - 글로벌 고가용성(DR) 및 레이턴시 최적화]] →

---
