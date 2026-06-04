+++
title = "035. ECAB — 긴급 변경 자문 위원회 (Emergency Change Advisory Board)"
date = 2026-03-03

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

> **핵심 인사이트**
> 1. [ECAB](/knowledge-base/studynote/12_it_management/02_itsm_itil/865_feature_engineering/) (Emergency Change Advisory Board)는 [ITIL](/knowledge-base/studynote/12_it_management/02_itsm_itil/846_itil/) [변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/) 체계에서 긴급 변경(Emergency Change)을 신속하게 승인·검토하는 소규모·권한 위임 위원회로, 전체 [CAB](/knowledge-base/studynote/12_it_management/02_itsm_itil/080_cab/) (Change Advisory Board)를 소집할 시간이 없을 때 대안적 거버넌스를 제공한다.
> 2. 긴급 변경은 일반 변경 절차를 우회하지만 완전히 생략하는 것이 아니라, 사후 검토(Post-Implementation [Review](/knowledge-base/studynote/04_software_engineering/03_design_architecture/153_requirements_review_inspection_walkthrough/))를 통해 정식 변경 기록으로 등록해야 한다.
> 3. ECAB의 핵심 가치는 속도(Speed)와 통제(Control)의 균형 — 비즈니스 중단을 최소화하면서도 승인 없는 무단 변경(Unauthorized Change)을 방지한다.

---

## I. [ITIL](/knowledge-base/studynote/12_it_management/02_itsm_itil/846_itil/) [변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/) 체계에서의 [ECAB](/knowledge-base/studynote/12_it_management/02_itsm_itil/865_feature_engineering/) 위치

```
변경 관리 체계
+-- 표준 변경 (Standard Change)
|   사전 승인, 낮은 위험, 절차 자동화
|
+-- 일반 변경 (Normal Change)
|   CAB 심의 -> 변경 관리자 승인
|   (긴급 아님, 일정 계획 가능)
|
+-- 긴급 변경 (Emergency Change)
    ECAB 소집 -> 빠른 승인 -> 즉시 구현
    사후: PIR (Post-Implementation Review)
```

| 변경 유형    | 승인 주체    | 소요 시간  | 문서화   |
|------------|------------|----------|---------|
| 표준 변경   | 사전 승인    | 즉시      | 최소    |
| 일반 변경   | [CAB](/knowledge-base/studynote/12_it_management/02_itsm_itil/080_cab/)       | 수일~수주  | 완전    |
| **긴급 변경** | <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/865_feature_engineering/">ECAB</a></strong> | **수시간** | 사후 완전|

> 📢 **섹션 요약 비유**: 국회가 일반 법안은 상임위->본회의를 거치지만, 계엄 해제는 긴급회의로 빠르게 결정 — ECAB는 IT판 긴급회의.

---

## II. [ECAB](/knowledge-base/studynote/12_it_management/02_itsm_itil/865_feature_engineering/) 구성과 역할

```
ECAB 구성원 (소규모, 권한 위임):
+-- 변경 관리자 (Change Manager)     <- 의장
+-- 서비스 소유자 (Service Owner)
+-- 관련 기술 전문가 (Subject Matter Expert)
+-- 비즈니스 대표 (Business Representative)
    (영향받는 서비스 운영 부서)
```

| 역할           | 책임                              |
|--------------|-----------------------------------|
| [변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/)자    | [ECAB](/knowledge-base/studynote/12_it_management/02_itsm_itil/865_feature_engineering/) 소집, 승인/거부 결정          |
| 기술 전문가   | 기술적 타당성 검토, [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 계획 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)  |
| 비즈니스 대표 | 비즈니스 영향도 평가               |
| [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 소유자  | [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/869_sla/) 영향도, 커뮤니케이션 계획 승인  |

> 📢 **섹션 요약 비유**: 응급실의 의료진 팀처럼 — 환자([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 장애)가 위급할 때 소수 전문가가 빠른 결정을 내린다.

---

## III. 긴급 변경 프로세스

```
인시던트 발생 / 긴급 요건 식별
      |
      v
긴급 변경 요청(RFC: Request For Change) 작성
      |
      v
변경 관리자 -> ECAB 소집 (전화, 화상)
      |
      v
영향 분석, 롤백 계획, 위험 평가 (30분 이내)
      |
      v
ECAB 승인 / 거부
      |
      v
긴급 구현 (배포 팀 실행)
      |
      v
구현 결과 모니터링
      |
      v
PIR (Post-Implementation Review)
      |
      v
정식 변경 기록 등록 (CMDB 업데이트)
```

> 📢 **섹션 요약 비유**: 수술 전 동의서 없이 응급 수술부터 하고, 나중에 의무기록에 상세히 기록하는 것과 같다.

---

## [IV](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/). 긴급 변경 vs 무단 변경 구분

```
긴급 변경 (Legitimate):
  ECAB 승인 -> 구현 -> PIR -> CMDB 등록
  위험을 알고 제어된 상태에서 빠른 실행

무단 변경 (Unauthorized Change):
  승인 없이 구현 -> 감지 시 감사 추적
  인시던트의 주요 원인 (ITIL 통계: ~80%)
```

| 구분       | 긴급 변경               | 무단 변경          |
|-----------|-------------------------|--------------------|
| 승인       | [ECAB](/knowledge-base/studynote/12_it_management/02_itsm_itil/865_feature_engineering/) 승인 있음           | 승인 없음           |
| 기록       | RFC + PIR               | 없음 (사후 추적)   |
| 결과       | 통제된 위험              | 예상 못한 장애 유발 |
| 책임       | 명확한 책임자            | 책임자 불분명      |

> 📢 **섹션 요약 비유**: 응급 수술(긴급 변경)은 합법적 의료 행위, 무면허 수술(무단 변경)은 불법 — 속도는 같아도 책임과 결과가 다르다.

---

## V. 실무 시나리오 — 운영 DB 핫픽스

| 상황         | 내용                                         |
|-------------|----------------------------------------------|
| 발생         | 프로덕션 DB [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 손상으로 주문 처리 0%      |
| [ECAB](/knowledge-base/studynote/12_it_management/02_itsm_itil/865_feature_engineering/) 소집    | [변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/)자 + [DBA](/knowledge-base/studynote/05_database/01_db_architecture_relational/025_dba_database_administrator/) + [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 소유자 전화 회의  |
| 검토         | [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 재생성 SQL 스크립트 검토 (10분)       |
| [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 계획    | [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 복원 절차 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) (5분)                    |
| 승인         | [ECAB](/knowledge-base/studynote/12_it_management/02_itsm_itil/865_feature_engineering/) 구두 승인 + 이메일 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)                 |
| 구현         | [DBA](/knowledge-base/studynote/05_database/01_db_architecture_relational/025_dba_database_administrator/) [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 재생성 실행 (20분)               |
| PIR          | 24시간 내 인시던트 리포트 + RFC 공식 등록    |

> 📢 **섹션 요약 비유**: 화재 시 소방서 신고 후 소화기를 먼저 쓰는 것 — 승인(신고)과 실행(소화기)이 동시에, 기록(사고 보고서)은 사후에.

---

## 📌 관련 개념 맵

```
ECAB (Emergency Change Advisory Board)
+-- 상위 체계: ITIL 변경 관리
|   +-- CAB (정기 변경 심의)
|   +-- ECAB (긴급 변경 심의)
+-- 프로세스
|   +-- RFC -> ECAB 승인 -> 구현 -> PIR
+-- 관련 개념
|   +-- PIR (Post-Implementation Review)
|   +-- CMDB (구성 관리 DB)
|   +-- RFC (Request For Change)
|   +-- Rollback Plan
+-- 목적
    +-- 속도 vs 통제 균형
    +-- 무단 변경 방지
    +-- 감사 추적 보장
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[ITIL v1/v2]
CAB 중심 변경 관리, 긴급 변경 개념 미흡
      |
      v
[ITIL v3 (2007)]
ECAB 공식 정의, 긴급 변경 절차 표준화
      |
      v
[ITIL 4 (2019)]
변경 유형 재정의 (표준/일반/긴급)
속도 강조 (DevOps 연계)
      |
      v
[현재: DevOps + ITIL 변경 관리 통합]
CI/CD 파이프라인 내 자동 변경 승인
긴급 변경도 파이프라인 롤백으로 대응
Change Advisory Board -> Feature Toggle
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. ECAB는 IT 시스템에 문제가 생겼을 때 빨리 고치기 위한 긴급 회의 그룹이에요.
2. 일반 회의는 시간이 걸리니까, 소수 전문가가 빠르게 결정하고 바로 고쳐요.
3. 단, 나중에 반드시 보고서를 써서 기록으로 남겨야 해요 — 책임감 있는 응급처치!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 61 / 587

<- **이전**: [플랫폼 비즈니스 모델 (Platform Business Model)](/knowledge-base/studynote/12_it_management/01_governance_strategy/826_platform_business_model/)
**다음**: [35. 린 스타트업 (Lean Startup)](/knowledge-base/studynote/12_it_management/01_governance_strategy/827_lean_startup/) ->

---
