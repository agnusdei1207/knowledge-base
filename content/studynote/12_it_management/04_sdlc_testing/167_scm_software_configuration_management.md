+++
title = "167. SCM (Software Configuration Management, 소프트웨어 형상 관리)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SCM ([Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/), [소프트웨어 형상 관리](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/648_ccb_configuration_control_board/))은 소프트웨어 산출물을 형상 항목 ([Configuration Item](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)) 단위로 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)하고, 변경을 승인·기록·[감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)하는 통제 체계다.
> 2. **가치**: 소스코드뿐 아니라 요구사항, 설계서, [테스트 케이스](/knowledge-base/studynote/04_software_engineering/11_testing_validation/833_test_case/), 배포 패키지까지 같은 기준으로 관리해야 변경 추적성, 재현 가능한 릴리스, 빠른 복구가 가능해진다.
> 3. **판단 포인트**: [형상 식별](/knowledge-base/studynote/04_software_engineering/01_overview_principles/021_configuration_identification/) -> [형상 통제](/knowledge-base/studynote/04_software_engineering/01_overview_principles/022_configuration_control/) -> [형상 상태 기록](/knowledge-base/studynote/04_software_engineering/01_overview_principles/024_configuration_status_accounting/) -> [형상 감사](/knowledge-base/studynote/04_software_engineering/01_overview_principles/023_configuration_audit/)의 흐름과 [베이스라인](/knowledge-base/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/) ([Baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)) 관리가 핵심이며, 단순 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 도구 사용만으로 SCM이 완성되지는 않는다.

---

## Ⅰ. 개요 및 필요성

SCM ([Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/))은 소프트웨어를 구성하는 각 산출물의 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)과 변경 이력을 체계적으로 관리하는 활동이다. 여기서 대상은 코드만이 아니라 요구사항 명세서, 설계 문서, 테스트 산출물, 실행 패키지, 운영 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)값까지 포함된다. 즉, "무엇이 현재 공식 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)인가"를 조직 차원에서 합의하고 통제하는 관리 체계다.

이 개념이 필요한 이유는 소프트웨어가 수정은 쉽지만, 그 영향은 매우 넓기 때문이다. 운영 장애가 발생했을 때 어떤 코드와 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)이 배포됐는지, 어떤 승인 절차를 거쳐 바뀌었는지 모르면 원인 분석과 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)이 모두 느려진다. 특히 대규모 프로젝트나 규제 산업에서는 변경 사실 자체보다 <strong>통제되지 않은 변경</strong>이 더 큰 위험이 된다.

아래 그림은 SCM이 없는 경우와 있는 경우의 차이를 단순화해 보여준다.

```text
+--------------------------------------------------------------+
|             SCM의 필요성: 변경을 기록하지 않으면 혼란이 된다    |
+-------------------------------+------------------------------+
| SCM 없음                      | SCM 있음                     |
+-------------------------------+------------------------------+
| 누가 바꿨는지 모름            | 변경 요청과 승인 이력 존재    |
| 어떤 버전이 운영 중인지 불명확 | 배포 버전과 기준선 추적 가능  |
| 장애 시 원복 경로 불명확      | 이전 기준선으로 신속 복구     |
+-------------------------------+------------------------------+
```

따라서 SCM은 개발 속도를 늦추는 문서 작업이 아니라, 변경이 빨라질수록 더 중요해지는 안전장치다. [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) ([Agile](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/))과 [데브옵스](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) ([DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)) 환경에서도 [형상 통제](/knowledge-base/studynote/04_software_engineering/01_overview_principles/022_configuration_control/) 원칙은 사라지지 않고, 더 자동화된 방식으로 재구성될 뿐이다.

- **📢 섹션 요약 비유**: SCM은 병원 진료 기록부와 같다. 약을 바꿀 때마다 기록이 남아야 나중에 부작용이 생겨도 원인을 찾고 이전 처방으로 돌아갈 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

SCM의 핵심 원리는 "무엇을 관리할지 정의하고, 어떻게 바뀌는지 통제하며, 현재 상태를 기록하고, 최종적으로 맞게 관리됐는지 검증한다"는 네 단계다. 이를 보통 [형상 식별](/knowledge-base/studynote/04_software_engineering/01_overview_principles/021_configuration_identification/), [형상 통제](/knowledge-base/studynote/04_software_engineering/01_overview_principles/022_configuration_control/), [형상 상태 기록](/knowledge-base/studynote/04_software_engineering/01_overview_principles/024_configuration_status_accounting/), [형상 감사](/knowledge-base/studynote/04_software_engineering/01_overview_principles/023_configuration_audit/)의 4대 기능으로 정리한다. 이 네 기능은 순서가 바뀌면 안 되고, 서로 증빙 자료를 이어 주는 체인으로 봐야 한다.

아래 흐름은 [소프트웨어 형상 관리](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/648_ccb_configuration_control_board/)의 전체 제어 루프를 보여준다.

```text
+--------------------------------------------------------------+
|                SCM 제어 루프 (Control Loop)                  |
+--------------------------------------------------------------+
| 형상 식별                                                     |
|   +- 형상 항목 (Configuration Item, CI) 정의                  |
|        |                                                     |
|        v                                                     |
| 기준선 설정 (Baseline)                                        |
|        |                                                     |
|        v                                                     |
| 변경 요청 (CR) --> 영향 분석 --> 형상 통제 위원회               |
|                              (Configuration Control Board,    |
|                               CCB) 승인/반려                  |
|        |                                                     |
|        v                                                     |
| 구현 · 테스트 · 배포                                          |
|        |                                                     |
|        v                                                     |
| 상태 기록 · 감사 · 차기 기준선 갱신                           |
+--------------------------------------------------------------+
```

| 기능 | 핵심 질문 | 실무 산출물 |
| :--- | :--- | :--- |
| [형상 식별](/knowledge-base/studynote/04_software_engineering/01_overview_principles/021_configuration_identification/) ([Configuration Identification](/knowledge-base/studynote/04_software_engineering/01_overview_principles/021_configuration_identification/)) | 무엇을 관리할 것인가? | [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/) 목록, 명명 규칙, [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 체계 |
| [형상 통제](/knowledge-base/studynote/04_software_engineering/01_overview_principles/022_configuration_control/) ([Configuration Control](/knowledge-base/studynote/04_software_engineering/01_overview_principles/022_configuration_control/)) | 어떤 변경을 승인할 것인가? | 변경 요청서, 영향 분석서, [CCB](/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/) 회의록 |
| [형상 상태 기록](/knowledge-base/studynote/04_software_engineering/01_overview_principles/024_configuration_status_accounting/) ([Configuration Status Accounting](/knowledge-base/studynote/04_software_engineering/01_overview_principles/024_configuration_status_accounting/)) | 지금 상태가 무엇인가? | [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 현황표, 배포 이력, 릴리스 노트 |
| [형상 감사](/knowledge-base/studynote/04_software_engineering/01_overview_principles/023_configuration_audit/) ([Configuration Audit](/knowledge-base/studynote/04_software_engineering/01_overview_principles/023_configuration_audit/)) | 관리 절차와 결과가 맞는가? | 기능/물리 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 결과, 증빙 문서 |

[베이스라인](/knowledge-base/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/)은 공식 검토와 승인을 거쳐 잠긴 기준 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이다. 기능 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) (Functional [Baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/))은 요구사항 확정 시점, 할당 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) (Allocated [Baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/))은 설계 확정 시점, 제품 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) (Product [Baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/))은 시험과 릴리스 확정 시점에서 주로 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)한다. [베이스라인](/knowledge-base/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/)이 있어야 "무엇이 바뀌었는지"를 비교할 출발점이 생긴다.

즉, SCM의 핵심은 단순 저장이 아니라 <strong>공식 상태를 지정하고 변경을 제어하는 것</strong>이다. Git 같은 도구는 이를 돕는 수단이지만, [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) 정의와 승인 체계까지 포함해야 비로소 SCM이라고 부를 수 있다.

- **📢 섹션 요약 비유**: SCM은 건물 설계 도면 관리와 같다. 현재 승인된 도면이 무엇인지 정해 두고, 수정하려면 검토와 승인 절차를 거쳐야 공사가 뒤엉키지 않는다.

---

## Ⅲ. 비교 및 연결

SCM은 자주 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 (Version Control)와 동일시되지만 범위가 더 넓다. [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 이력과 병합을 다루는 핵심 도구이지만, 어떤 변경을 승인할지, 어떤 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)을 공식 릴리스로 볼지, [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 때 어떤 증빙을 제출할지는 별도의 관리 체계가 필요하다. 그래서 Git을 쓴다고 자동으로 SCM이 완성되는 것은 아니다.

| 항목 | [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 | SCM |
| :--- | :--- | :--- |
| 관리 대상 | 주로 소스코드와 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 이력 | 코드, 문서, 테스트, 패키지, [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 전체 |
| 핵심 기능 | 커밋, 브랜치, 병합 | [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/), 통제, 상태 기록, [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) |
| 초점 | 개발 효율과 협업 | 공식 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)과 변경 통제 |
| 대표 도구/수단 | Git, SVN (Apache Subversion) | Git + CR/[CCB](/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/) + 릴리스/[감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 체계 |

또한 현대 운영에서는 GitOps와도 연결된다. GitOps는 Git을 단일 진실의 원천 (Single Source of Truth)으로 삼아 인프라와 애플리케이션 배포를 선언적으로 관리한다. 이는 전통적 SCM 원칙을 자동화된 파이프라인으로 옮긴 형태로 볼 수 있으며, 변화의 속도는 빨라졌지만 추적성과 승인, [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)이라는 핵심 목적은 동일하다.

즉, SCM은 전통적 문서 중심 프로세스와 현대 DevOps를 가르는 개념이 아니라, 둘을 이어 주는 상위 원칙이다. 시험에서는 "[버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 ⊂ SCM" 관계와 GitOps가 SCM 철학을 자동화한다는 연결점을 함께 제시하면 좋다.

- **📢 섹션 요약 비유**: Git이 책장의 책 번호표라면, SCM은 어떤 책을 공식 교재로 채택했고 누가 언제 개정판을 승인했는지까지 적는 도서관 운영 규칙이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 SCM의 가치는 배포 직전보다 장애 순간에 더 크게 드러난다. 예를 들어 금융 [서비스 운영](/knowledge-base/studynote/12_it_management/02_itsm_itil/067_service_operation/) 중 결제 오류가 발생했을 때, 최근 핫픽스가 어떤 요구사항 변경과 연결됐는지, 어떤 브랜치와 빌드 [아티팩트](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/) ([Artifact](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/))가 운영에 올라갔는지, 누구 승인으로 릴리스됐는지를 즉시 따라갈 수 있어야 한다. 이 추적성이 있으면 원인 분석과 원복이 빨라지고, 없으면 대응이 사람 기억에 의존하게 된다.

또한 조직 규모와 규제 수준에 따라 통제 강도는 달라져야 한다. 국방·항공·금융처럼 규제와 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 요구가 높은 환경에서는 [CCB](/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/) ([Configuration Control](/knowledge-base/studynote/04_software_engineering/01_overview_principles/022_configuration_control/) Board, [형상 통제 위원회](/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/))와 정식 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) 관리가 필수이고, 스타트업 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에서는 경량화된 승인 흐름을 쓰더라도 태그, 변경 이력, 릴리스 증빙은 남겨야 한다. 빠른 배포와 [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)는 상충 관계가 아니라 자동화 수준의 차이로 이해하는 편이 정확하다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 형상 항목 ([Configuration Item](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/))이 코드 외 문서·[설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)·배포 패키지까지 정의되어 있는가?
2. 운영 반영 전 변경 요청, 영향 분석, 승인 기록이 남는가?
3. 릴리스 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)과 배포 대상 환경이 1:1로 추적되는가?
4. [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)나 장애 대응 시 이전 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)으로 복원 가능한가?

### 대표 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 브랜치 전략만 있고 공식 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) 정의가 없는 경우
- 운영 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 변경을 수동으로 적용해 코드 이력과 분리되는 경우
- 변경 승인 기록 없이 긴급 수정이 누적되는 경우

기술사 답안에서는 SCM 4대 기능, [베이스라인](/knowledge-base/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/) 3종, [CCB](/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/) 역할, IEEE 828 같은 표준 연결까지 정리하면 답변의 구조가 선명해진다. 핵심은 "[형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) 도구"가 아니라 "[형상 통제](/knowledge-base/studynote/04_software_engineering/01_overview_principles/022_configuration_control/) 체계"를 설명하는 것이다.

- **📢 섹션 요약 비유**: SCM은 회사 결재선이 붙은 공사 일지와 같다. 자재를 바꾸거나 설계를 수정할 때마다 기록과 승인 흔적이 남아야 사고가 나도 책임과 원인을 바로 찾을 수 있다.

---

## Ⅴ. 기대효과 및 결론

SCM을 제대로 운영하면 변경 추적성, 릴리스 재현성, [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 대응력, [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 속도가 함께 좋아진다. 개발팀은 어떤 산출물이 현재 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)인지 명확히 알고, 운영팀은 어느 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이 어떤 환경에 배포됐는지 추적할 수 있으며, 품질팀은 요구사항과 실제 결과의 일치 여부를 근거 자료로 확인할 수 있다. 결국 SCM은 협업 조직이 같은 소프트웨어를 같은 기준으로 바라보게 만드는 공통 언어다.

다만 모든 조직이 동일한 무게의 절차를 가져야 하는 것은 아니다. 문서 양을 늘리는 것이 목적이 아니라, 변경 통제를 유지하면서 속도를 해치지 않는 수준을 찾는 것이 중요하다. 그래서 앞으로의 SCM은 더 많은 자동화, [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 코드화, [GitOps](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) 연계로 발전하되, [베이스라인](/knowledge-base/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/)과 승인·[감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 원칙 자체는 계속 유지될 가능성이 크다.

결론적으로 SCM은 "소프트웨어 변경을 기억하고 통제하는 시스템"으로 이해하면 된다. 변경은 피할 수 없지만, 통제되지 않은 변경은 장애와 책임 공백을 만들기 때문이다.

- **📢 섹션 요약 비유**: SCM은 큰 오케스트라의 악보 관리와 같다. 누구나 자기 악보를 조금씩 바꿔 버리면 합주가 무너지지만, 공식 악보와 수정 이력이 정리되어 있으면 전체 연주가 안정된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/) ([Configuration Item](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)) | 소스코드, 문서, [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 등 SCM이 직접 관리하는 단위 |
| [베이스라인](/knowledge-base/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/) ([Baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)) | 공식 승인된 기준 상태로, 변경 비교와 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)의 기준점 |
| [CCB](/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/) ([Configuration Control](/knowledge-base/studynote/04_software_engineering/01_overview_principles/022_configuration_control/) Board) | 주요 변경의 승인·반려를 결정하는 통제 조직 |
| SCMP ([Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) Plan) | SCM 범위, 절차, 책임을 정의하는 계획 문서 |
| [GitOps](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) | SCM 원칙을 인프라·배포 자동화까지 확장한 현대 운영 방식 |

### 📈 관련 키워드 및 발전 흐름도

```text
형상 항목 (Configuration Item) 식별
    |
    v
베이스라인 (Baseline) 설정
    |
    v
변경 요청 · CCB (Configuration Control Board) 통제
    |
    v
상태 기록 (Status Accounting) · 형상 감사 (Audit)
    |
    v
GitOps · IaC (Infrastructure as Code) 기반 자동화 SCM
```

이 흐름도는 SCM이 단순 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 이력 관리에서 출발해, 승인·[감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)·자동화까지 포함하는 운영 체계로 확장되는 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. SCM은 레고 작품을 만들 때 "어떤 조각을 언제 바꿨는지"를 공책에 적어 두는 방법이에요.
2. 중요한 순간마다 사진을 찍어 두면, 나중에 망가져도 예전 모습으로 다시 만들 수 있어요.
3. 그리고 마음대로 바꾸지 말고 선생님의 확인을 받으면, 친구들이 함께 만들어도 작품이 엉망이 되지 않아요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 281 / 587

<- **이전**: [166. CI/CD (Continuous Integration/Continuous Deployment, 지속적 통합/배포)](/knowledge-base/studynote/12_it_management/04_sdlc_testing/166_cicd_continuous_integration_deployment/)
**다음**: [168. 프로젝트 리스크 대응 전략 (Risk Response Strategies)](/knowledge-base/studynote/12_it_management/04_sdlc_testing/168_risk_response_strategies/) ->

---
