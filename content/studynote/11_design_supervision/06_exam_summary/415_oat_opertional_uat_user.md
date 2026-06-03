+++
title = "415. 운영 인수 테스트·사용자 인수 테스트 감리 시점 (Operational and User Acceptance Test Audit Timing)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [운영 인수 테스트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/707_oat_operational_acceptance_testing/)([OAT](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/707_oat_operational_acceptance_testing/), [Operational Acceptance Testing](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/409_operational_acceptance_testing_oat/))와 사용자 [인수 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/406_acceptance_test_uat/)(UAT, User Acceptance Testing)는 각각 운영 가능성과 업무 적합성을 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 전환 게이트이며, 감리는 두 게이트의 시점과 증적이 맞는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 일이다.
> 2. **가치**: OAT에서 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)·배치·권한·모니터링을 걸러내고, UAT에서 사용자 시나리오와 승인 책임을 확정하면 운영 장애와 인수 분쟁을 크게 줄일 수 있다.
> 3. **판단 포인트**: [시스템 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/405_system_test/) 완료 후 [OAT](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/707_oat_operational_acceptance_testing/)/UAT가 어떤 순서와 기준으로 수행되며, 미해결 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)·서명·전환 승인 문서가 서로 연결되는지가 핵심이다.

## Ⅰ. 개요 및 필요성

[운영 인수 테스트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/707_oat_operational_acceptance_testing/)와 사용자 [인수 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/406_acceptance_test_uat/)는 모두 “마지막 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)”처럼 보이지만, 감리 관점에서는 질문이 다르다. OAT는 운영 조직이 실제 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 전환을 견딜 수 있는지 보는 시험이고, UAT는 현업 사용자가 요구사항이 업무 목적에 맞는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 승인 절차다. 따라서 감리는 둘을 같은 단계로 뭉개지 않고, **운영 안정성 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)**과 **업무 수용성 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)**을 분리해 시점을 본다.

특히 전환 직전에는 [시스템 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/405_system_test/)가 통과했더라도 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), 배치 [스케줄](/knowledge-base/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/), 권한 분리, 장애 대응, 헬프데스크 인수 같은 운영 요소가 빠질 수 있다. 반대로 OAT가 완료되어도 실제 사용자가 화면 흐름, 예외 처리, 출력물, 마감 업무를 승인하지 않으면 인수 완료로 보기 어렵다. 그래서 기술사 답안에서는 “무엇을 언제 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는가”를 시간축으로 제시하는 것이 중요하다.

```text
┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐
│ 시스템 테스트 │──▶│ OAT 수행     │──▶│ UAT 수행     │──▶│ 전환 승인     │──▶│ 운영 개시     │
└────────────┘   └────────────┘   └────────────┘   └────────────┘   └────────────┘
      │                  │                  │                  │
      └─기능 결함 정리   └─운영 준비 확인   └─업무 적합 확인   └─최종 Go/No-Go
```

- **📢 섹션 요약 비유**: 새 집에 들어가기 전, 전기·[가스](/knowledge-base/studynote/06_ict_convergence/01_blockchain/024_gas/)가 되는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 절차가 OAT이고 실제로 가족이 살아도 불편 없는지 보는 절차가 UAT다.

## Ⅱ. 아키텍처 및 핵심 원리

감리에서 보는 핵심 원리는 “시험 주체가 다르면 증적도 달라야 한다”는 점이다. OAT는 운영팀 중심으로 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 성공 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 배치 결과, 권한 점검표, 모니터링 설정값을 남겨야 하고, UAT는 현업 시나리오 결과, [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 수용 여부, 서명된 승인서, 교육 완료 기록을 남겨야 한다. 두 시험의 증적이 전환 승인서와 연결되어야 감리 추적성이 완성된다.

또 OAT와 UAT는 완전히 직렬일 수도, 일부 병행될 수도 있다. 다만 병행하더라도 감리인은 각 시험의 종료 조건을 분리해 본다. 예를 들어 UAT에서 업무 흐름이 맞아도 OAT에서 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 목표시간이나 운영 절차가 미흡하면 운영 개시를 보류해야 한다.

```text
┌──────────────────────┐
│ 운영 기준선 확정      │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ OAT: 복구·배치·권한   │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ UAT: 시나리오·승인    │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Go/No-Go 의사결정     │
└──────────────────────┘
```

| 단계 | 핵심 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 항목 | 대표 증적 |
|:---|:---|:---|
| [OAT](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/707_oat_operational_acceptance_testing/) | [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)·[복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), 배치, 권한, 모니터링, 운영절차 | [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 리허설 결과, 운영 매뉴얼, 작업일지 |
| UAT | 업무 시나리오 적합성, 출력물, 사용자 승인 | 시나리오 결과서, [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 처리표, 인수 서명서 |
| 전환 승인 | 미해결 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/), 책임자 승인, 일정 적정성 | Go/No-Go 회의록, 전환 계획서, 예외 승인서 |

- **📢 섹션 요약 비유**: 가게를 열기 전 주방 설비 점검표와 손님 시식 평가표가 모두 있어야 비로소 개업 결정을 내릴 수 있다.

## Ⅲ. 비교 및 연결

감리 답안에서는 OAT와 UAT를 비교해 쓰면 채점 포인트가 선명해진다. 같은 [인수 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/406_acceptance_test_uat/) 계열이라도 주체·목적·판정 기준이 다르기 때문이다. 여기에 [시스템 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/405_system_test/)와 전환 승인까지 함께 대비하면 시험 단계의 역할 구분이 훨씬 명확해진다.

| 비교 항목 | [시스템 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/405_system_test/) | [OAT](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/707_oat_operational_acceptance_testing/) | UAT |
|:---|:---|:---|:---|
| 주체 | 개발·QA 조직 | 운영 조직 | 현업 사용자·고객 |
| 초점 | 기능·[비기능 요구사항](/knowledge-base/studynote/04_software_engineering/03_design_architecture/133_non_functional_requirements/) 충족 | 운영 준비 상태와 전환 가능성 | 업무 목적과 사용 적합성 |
| 대표 시나리오 | 통합 기능, [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/), 장애 처리 | [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)/[복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), 배치, 권한, 모니터링 | 화면 흐름, 출력물, 마감 업무 |
| 종료 기준 | [테스트 케이스](/knowledge-base/studynote/04_software_engineering/11_testing_validation/441_test_case/) 통과 | 운영 절차 수행 가능 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 인수 서명과 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 수용 합의 |
| 감리 질문 | “만들어졌는가?” | “운영할 수 있는가?” | “사용자가 받아들일 것인가?” |

- **📢 섹션 요약 비유**: 자동차를 만들었다는 검사와 도로에 안전하게 굴릴 수 있다는 검사, 운전자가 만족한다는 검사는 서로 다른 통과문이다.

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 OAT와 UAT의 순서보다 **게이트 관리**가 더 중요하다. 감리는 각 시험이 실제 전환 일정에 밀려 형식적으로 끝나지 않았는지, 발견 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)이 누가 어떤 조건으로 수용했는지, 승인 권한자가 명확한지를 본다. 또한 운영 매뉴얼과 교육, 헬프데스크 이관, 장애 대응 연락체계가 시험 범위 밖으로 빠지지 않았는지도 자주 점검한다.

[결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)이 남아도 예외 승인을 통해 전환할 수는 있지만, 그 경우 감리 문서는 반드시 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)·완화책·책임자·추적 일정을 함께 남겨야 한다. 기술사 답안에서는 “[OAT](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/707_oat_operational_acceptance_testing/)/UAT 통과 여부”보다 “미통과 항목을 어떤 통제로 관리하는가”까지 적어야 실무성이 살아난다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

- OAT와 UAT의 목적, 주체, 종료 조건이 문서로 분리되어 있는가?
- [시스템 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/405_system_test/) 미해결 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)이 [OAT](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/707_oat_operational_acceptance_testing/)/UAT 판정에 어떤 영향을 주는지 정의되어 있는가?
- [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 리허설, 배치 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), 권한 점검 등 운영 증적이 실제 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)로 남는가?
- 사용자 승인 범위와 서명 권한자가 명확한가?
- Go/No-Go 회의에서 예외 승인 항목과 후속 조치가 추적되는가?

- **📢 섹션 요약 비유**: 이사 날이 정해졌다고 해서 [가스](/knowledge-base/studynote/06_ict_convergence/01_blockchain/024_gas/) 점검도 안 하고 열쇠도 안 받은 채 들어가면 안 되듯, 전환 일정보다 게이트 증적이 먼저다.

## Ⅴ. 기대효과 및 결론

OAT와 UAT의 감리 시점을 올바르게 설계하면 “개발 완료”와 “운영 가능”과 “업무 수용” 사이의 틈을 줄일 수 있다. 그 결과 전환 직후 장애, 사용자 반발, 책임 공방이 줄고, 운영 조직과 현업 조직의 승인 책임도 명확해진다. 특히 대규모 전환·차세대 시스템에서는 이 구분이 프로젝트 성공 여부를 좌우한다.

결론적으로 이 주제의 핵심은 시험 종류를 나열하는 것이 아니라, **누가 무엇을 근거로 운영 개시를 허락하는지**를 보여 주는 것이다. 답안에서는 [시스템 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/405_system_test/)→[OAT](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/707_oat_operational_acceptance_testing/)→UAT→전환 승인 흐름과 예외 승인 통제를 함께 제시하면 완성도가 높다.

- **📢 섹션 요약 비유**: 공연을 올리기 전 무대 장치 점검, 리허설, 관객 시사회가 모두 끝나야 정식 개막을 선언할 수 있다.

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [시스템 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/405_system_test/) | 기능·비기능 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)을 먼저 정리해야 [OAT](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/707_oat_operational_acceptance_testing/)/UAT의 판정이 흔들리지 않는다. |
| 컷오버(Cut-over) | [OAT](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/707_oat_operational_acceptance_testing/)/UAT 결과가 최종 전환 승인과 직접 연결된다. |
| [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)([Rollback](/knowledge-base/studynote/02_operating_system/05_deadlock/313_rollback/)) | OAT에서 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시나리오를 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)해야 전환 실패 시 피해를 줄인다. |
| [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준 협약([SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/), [Service Level Agreement](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/)) | OAT의 운영 기준선과 연결되어 목표 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)시간·가용성을 판단한다. |
| 사용자 교육 | UAT 승인 이후 실제 업무 정착률을 높이는 핵심 보완 활동이다. |

### 📈 관련 키워드 및 발전 흐름도

- 관련 키워드: [시스템 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/405_system_test/), [OAT](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/707_oat_operational_acceptance_testing/), UAT, 컷오버, Go/No-Go, [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/), 운영 매뉴얼, 인수 서명
- 발전 흐름: 기능 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 중심 테스트 → 운영 준비도 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)([OAT](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/707_oat_operational_acceptance_testing/)) → 사용자 수용성 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)(UAT) → 전환 승인 거버넌스 강화

```text
요구사항 검증
     │
     ▼
시스템 테스트
     │
     ▼
OAT(운영 가능성)
     │
     ▼
UAT(업무 수용성)
     │
     ▼
Go/No-Go 승인
     │
     ▼
운영 안정화
```

### 👶 어린이를 위한 3줄 비유 설명

1. OAT는 새 놀이터가 안전하게 돌아가는지 미리 점검하는 거예요.
2. UAT는 친구들이 정말 재미있고 불편하지 않은지 직접 써 보는 거예요.
3. 둘 다 괜찮다고 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)돼야 비로소 “이제 문 열자!”라고 말할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 493 / 530

← **이전**: [414. 리틀의 법칙 기반 스레드풀 성능감사 (Little's Law)](/knowledge-base/studynote/11_design_supervision/06_exam_summary/414_audit/)
**다음**: [416. 보안 테스트 퍼징 기반 이상 패킷 자동 주입 (Security Fuzzing for Abnormal Packet Injection)](/knowledge-base/studynote/11_design_supervision/06_exam_summary/416_process/) →

---
