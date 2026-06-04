+++
title = "85. ERP 구축 생명주기 - 패키지 선정 -> 커스터마이징 / CBO (Custom Built Object) -> 데이터 이관 -> 빅뱅/점진적 오픈"

[taxonomies]
tags = ["enterprise_systems"]

[extra]
tags = ["enterprise_systems"]
+++

## 핵심 인사이트 (3줄 요약)

> **본질**: [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) ([Enterprise Resource Planning](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)) 구축 생명주기는 패키지 도입이 아니라 업무 표준화와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이관을 함께 설계하는 변화 관리 과정이다.
> **가치**: 준비, 적합성 검토(Fit-Gap), 커스터마이징, 이관, UAT (User [Acceptance Test](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/406_acceptance_test_uat/)), 컷오버(Cutover)를 순서대로 밟아야 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)를 줄일 수 있다.
> **판단 포인트**: 기능 추가보다 프로세스 합의와 [마스터 데이터](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) 정리가 먼저다. 그렇지 않으면 골격보다 예외가 먼저 무너진다.

---

## Ⅰ. 개요 및 필요성

ERP는 재무, 구매, 생산, 인사 같은 핵심 업무를 하나의 흐름으로 묶는 통합 시스템이다. 하지만 성공 여부는 소프트웨어 설치보다 업무 방식의 통일과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질에 더 크게 좌우된다.

생명주기가 필요한 이유는 ERP가 한 번에 끝나는 프로젝트가 아니기 때문이다. 요구 분석부터 안정화(Hypercare)까지 이어지는 과정에서, 기능보다 조직 합의·교육·이관 준비가 느슨하면 시스템은 도입돼도 현장은 옛 방식으로 돌아간다.

- 📢 섹션 요약 비유: 프로젝트가 아니라 전환

---

## Ⅱ. 아키텍처 및 핵심 원리

[ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) 구축은 보통 준비, Fit-Gap 분석, 설계/구현, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이관, 시험, 컷오버, 안정화의 순서로 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/)된다. Fit-Gap은 패키지 표준 기능과 실제 업무 사이의 차이를 찾는 단계이고, 이 차이를 줄일지, 커스터마이징할지, 프로세스를 바꿀지를 결정한다.

```text
준비 -> Fit-Gap -> 설계/구현 -> 데이터 이관 -> UAT -> Cutover -> Hypercare
```

| 단계 | 핵심 산출물 | 판단 포인트 |
| --- | --- | --- |
| 준비 | 범위, 조직, 일정 | 스폰서와 책임자가 있는가 |
| Fit-Gap | 표준 vs 예외 목록 | 바꿀 프로세스와 남길 예외가 구분됐는가 |
| 이관 | 정제된 [마스터 데이터](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) | 중복/오염 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 제거됐는가 |
| UAT | 사용자 승인 | 실제 업무 시나리오가 통과하는가 |
| Cutover | 전환 계획 | 다운타임과 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)이 정의됐는가 |

핵심은 "기능을 많이 넣는가"가 아니라 "업무를 일관되게 운영할 수 있는가"다.

- 📢 섹션 요약 비유: 단계별 교정기

---

## Ⅲ. 비교 및 연결

[ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) 도입은 빅뱅(Big Bang)과 단계적(Phased) 전환으로 나뉜다. 빅뱅은 짧고 강하지만 실패 충격이 크고, 단계적 전환은 오래 걸리지만 위험을 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)한다. 또한 표준 패키지 중심 구현은 유지보수가 쉽지만, 과도한 커스터마이징은 업그레이드 비용을 키운다.

| 비교 대상 | 차이점 |
| --- | --- |
| Big Bang | 한 번에 전환, [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 집중 |
| Phased Rollout | [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)별/조직별 순차 전환 |
| Standardization | 패키지 기능에 맞춰 업무를 맞춤 |
| Customization | 예외 업무를 시스템에 반영 |

따라서 ERP는 "시스템 구축"보다 "업무 재설계"에 가깝고, 변경관리와 교육이 기술 작업 못지않게 중요하다.

- 📢 섹션 요약 비유: 한 번에 옮길까, 나눠 옮길까

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 커스터마이징을 최소화하고, 꼭 필요한 차이만 남기는 것이 원칙이다. [마스터 데이터](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) 정제, 사용자 교육, 역할별 승인 흐름, 전환 리허설을 충분히 하지 않으면 go-live 직후 장애와 수작업이 폭증한다. 또한 스폰서와 프로세스 오너가 명확해야 일정이 흔들리지 않는다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. Fit-Gap 결과에 따라 표준 적용/커스터마이징/업무 변경이 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)됐는가?
2. [마스터 데이터](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/)가 이관 전에 정제됐는가?
3. Cutover와 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/), Hypercare 담당이 정의됐는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 화면만 바꾸고 프로세스는 그대로 두는 것
- [데이터 정제](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/266_data_cleansing/) 없이 이관부터 밀어붙이는 것
- 승인 구조 없이 현업에 교육만 던지는 것

- 📢 섹션 요약 비유: 업무 전환 리허설

---

## Ⅴ. 기대효과 및 결론

성공적인 [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) 구축은 정보가 한곳에서 이어지고, 재무·물류·인사 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 같은 규칙으로 처리하게 만든다. 그 결과 결산 속도, 재고 가시성, 통제 추적성이 좋아진다. 반대로 생명주기 관리가 약하면 통합 시스템이 오히려 부서별 [사일로](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)를 숨기는 껍데기가 된다.

결론적으로 ERP는 도구보다 운영 방식의 표준화가 먼저다. 기술사 답변에서는 "패키지 선택"보다 "업무 합의->이관->안정화"의 순서를 강조하면 설득력이 높다.

- 📢 섹션 요약 비유: 회사 이사 준비

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| --- | --- |
| [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) ([Enterprise Resource Planning](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)) | 전사 통합 업무 플랫폼 |
| Fit-Gap | 표준 기능과 예외의 [차이 분석](/knowledge-base/studynote/12_it_management/03_ea_isp/107_gap_analysis_task_identification/) |
| UAT (User [Acceptance Test](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/406_acceptance_test_uat/)) | 현업 승인 단계 |
| Cutover | 전환 [실행 계획](/knowledge-base/studynote/05_database/03_relational_model/166_execution_plan_optimizer_navigation_tree/) |
| Hypercare | go-live 직후 집중 안정화 |
| Master [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 전사 공통 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질의 핵심 |

### 📈 관련 키워드 및 발전 흐름도

```text
준비 / 범위 합의
   v
Fit-Gap 분석
   v
설계·커스터마이징
   v
마스터 데이터 정제 / 이관
   v
UAT 및 전환 리허설
   v
Cutover
   v
Hypercare / 안정화
```

### 👶 어린이를 위한 3줄 비유 설명

1. ERP는 회사의 여러 서랍을 한 번에 정리해서 같은 위치에 넣는 큰 정리 상자예요.
2. 정리법을 먼저 정하지 않으면 물건은 들어가도 다시 찾기 어려워요.
3. 그래서 순서와 이름표를 먼저 맞춰야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 85 / 482

<- **이전**: [84. 확장형 ERP (Extended ERP) - 외부 공급망(SCM) 및 고객(CRM)까지 통합 연계 (ERP II)](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/084_extended_erp_erp_ii_scm_crm/)
**다음**: [86. BPR과 ERP의 관계 - 시스템에 맞춰 업무를 변경할 것인가(BPR 선행), 업무에 맞춰 시스템을 고칠 것인가(커스터마이징)](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/086_bpr_vs_erp_customization/) ->

---
