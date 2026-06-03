+++
title = "22. 형상 통제 (Configuration Control) - 변경 제어 위원회(CCB)"
description = "식별된 형상 항목(CI)에 대한 변경 요구를 체계적으로 검토, 승인, 추적하는 형상 관리의 핵심 제어 메커니즘"
date = 2026-03-04

[taxonomies]
tags = ["software_engineering"]

[extra]
tags = ["software_engineering"]
+++

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 형상 통제는 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)된 형상 항목([CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/))의 변경 사항을 무분별하게 적용하지 못하도록, [변경 통제 위원회](/knowledge-base/studynote/12_it_management/02_itsm_itil/080_cab/)([CCB](/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/))를 통해 검토, 승인, 반려하는 게이트키퍼 프로세스이다.
> 2. **가치**: 변경으로 인한 부작용(Side-effect)을 사전에 차단하고, 프로젝트의 [범위 크리프](/knowledge-base/studynote/04_software_engineering/03_design_architecture/161_scope_creep_requirements_inflation_prevention/)([Scope Creep](/knowledge-base/studynote/04_software_engineering/03_design_architecture/161_scope_creep_requirements_inflation_prevention/))를 방지하여 시스템의 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)과 품질을 유지한다.
> 3. **융합**: 최신 [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 환경에서는 전통적인 대면 회의 형태의 [CCB](/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/) 대신, 자동화된 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 파이프라인의 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 제어(Policy-as-Code) 및 [Pull Request](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 리뷰 과정으로 진화하고 있다.

---

### Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

형상 통제 (Configuration Control)는 [베이스라인](/knowledge-base/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/)([Baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/))이 설정된 형상 항목([CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/))에 대한 변경 요청(CR, Change Request)이 발생했을 때, 이를 공식적인 절차에 따라 평가하고 반영 여부를 결정하는 형상 관리의 중추적 활동이다. [형상 식별](/knowledge-base/studynote/04_software_engineering/01_overview_principles/021_configuration_identification/)이 "무엇을 관리할 것인가"를 정의한다면, 형상 통제는 "어떻게 변경을 허락할 것인가"를 규정한다.

소프트웨어 개발 과정에서 변경은 필연적이다. 요구사항의 변경, 버그 패치, [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 개선 등 수많은 변경 요청이 동시다발적으로 발생한다. 과거에는 개발자가 임의로 코드를 수정하여 시스템 일관성이 붕괴되는 일이 잦았다. 특히 여러 개발자가 동일한 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)을 수정할 때 발생하는 충돌과 예기치 못한 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)의 전파는 소프트웨어 위기의 주된 원인이었다.

이러한 문제를 해결하기 위해, 변경의 타당성과 파급 효과를 분석하는 [형상 통제 위원회](/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/)([CCB](/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/), Configuration Control Board)가 등장했다. CCB는 변경이 시스템 전반에 미치는 기술적, 비용적 영향을 평가하여 객관적이고 통제된 환경에서만 시스템이 진화할 수 있도록 제어하는 혁신적인 방파제 역할을 수행한다.

> **📢 섹션 요약 비유**: 건물의 기둥을 옮기고 싶을 때 인부 마음대로 옮기면 건물이 무너지지만, 건축 허가 위원회([CCB](/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/))의 도면 검토와 승인을 거치면 안전하게 구조를 변경할 수 있는 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

형상 통제의 핵심 메커니즘은 변경 요청(CR)의 라이프사이클 관리에 있다. 모든 변경은 엄격한 [상태 전이](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/)([State Transition](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/))를 거쳐 시스템에 반영된다.

이 [상태 전이](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/)도는 변경 요청(CR)이 발의되어 최종적으로 [베이스라인](/knowledge-base/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/)에 반영될 때까지의 엄격한 흐름을 보여준다. 각 전이 구간에는 승인 및 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 단계가 강제되어 있음을 이해해야 한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">1. CR 발의</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">2. 영향 분석│ ──(비용/일정 초과)──&gt;</div><div class="kb-diagram-node">반려 (Rejected)</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">3. CCB 심의│ ──(기술적 타당성 부족)──&gt;</div><div class="kb-diagram-node">보류/반려</div></div>
<div class="kb-diagram-note">↓ (승인: Approved)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">4. 체크아웃</div><div class="kb-diagram-cell">(Check-out) ─&gt; 개발자 로컬 환경</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(수정 진행)</div></div>
<div class="kb-diagram-note">↓ (체크인: Check-in)</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">5. 테스트/감사│ ──(결함 발견 시)──&gt;</div><div class="kb-diagram-node">재수정</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">6. 베이스라인 반영</div></div>
</div>
</div>



이 흐름의 핵심은 수정 단계(체크아웃)가 CCB의 심의 단계보다 뒤에 위치한다는 점이다. 따라서 무분별한 코딩 작업은 변경이 공식적으로 승인되기 전에 진행될 수 없으며, 불필요한 자원 낭비를 원천 차단한다. 실무에서는 이 승인 병목 구간의 처리 속도([Lead Time](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/))를 주기적으로 관찰해야 전체 개발 속도 저하를 막을 수 있다.

#### 구성 요소 및 내부 동작

| 요소명 | 역할 | 내부 동작 | 연관 도구 | 비유 |
|:---|:---|:---|:---|:---|
| **CR (Change Request)** | 변경을 요구하는 공식 문서 | 요구 사유, 대상 범위 명세 | Jira, Redmine | 민원 신청서 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/">CCB</a> (Control Board)</strong> | 변경을 심의하는 의사결정 기구 | 영향도(Impact) 평가, 승인 | 회의, 결재 시스템 | 심사 위원회 |
| **Check-out / Check-in** | 중앙 저장소와 로컬 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 | 잠금([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/)) 및 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 분기 | Git, SVN | 도서 대출/반납 |
| **Impact Analysis** | 변경 시 파급되는 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 및 리소스 분석 | 연관 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 트래킹 | 의존성 분석 도구 | 파장 예측기 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/">Baseline</a> Update</strong> | [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 완료된 후 새로운 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) 형성 | 태그 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 상태 기록 업데이트| [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/[CD Pipeline](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/081_cd_continuous_deployment_pipeline_architecture/) | 새로운 법령 공포 |

형상 통제 과정에서 <strong><a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/">CCB</a> (Configuration Control Board)</strong>의 구성은 프로젝트 규모에 따라 유동적이다. PM, 아키텍트, 품질 보증(QA) 담당자, 때로는 고객 대표까지 포함되어 기술적 영향뿐 아니라 비즈니스적 파급(비용, 일정)까지 다각도로 분석한다.

> **📢 섹션 요약 비유**: 공항의 보안 검색대와 같습니다. 수많은 수하물(변경 요청)이 밀려와도, 엑스레이(영향 분석)와 요원([CCB](/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/))의 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 없이는 절대 비행기(시스템)에 실릴 수 없는 통제 구역입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

전통적인 폭포수 환경의 형상 통제와 [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/)/[DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 환경의 형상 통제는 그 승인 주체와 접근 방식에서 큰 차이를 보인다.

다음 매트릭스는 무겁고 공식적인 [CCB](/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/) 기반 방식과, 자동화 및 [코드 리뷰](/knowledge-base/studynote/04_software_engineering/06_software_architecture/330_code_review/) 기반의 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 통제 방식의 아키텍처적 트레이드오프를 보여준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">비교 항목</div><div class="kb-diagram-cell">전통적 형상 통제 (폭포수)</div><div class="kb-diagram-cell">최신 형상 통제 (DevOps)</div><div class="kb-diagram-cell">판단 포인트</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">승인 주체</div><div class="kb-diagram-cell">공식적인 CCB 회의 기구</div><div class="kb-diagram-cell">동료 리뷰어(PR), 파이프라인</div><div class="kb-diagram-cell">조직의 문화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">승인 속도</div><div class="kb-diagram-cell">느림 (주/월 단위 회의)</div><div class="kb-diagram-cell">빠름 (실시간 / 일 단위)</div><div class="kb-diagram-cell">배포의 빈도</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">초점</div><div class="kb-diagram-cell">변경 억제 및 방어적 통제</div><div class="kb-diagram-cell">빠른 피드백과 안전한 적용</div><div class="kb-diagram-cell">리스크 수용도</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">자동화</div><div class="kb-diagram-cell">문서 기반의 수동 결재</div><div class="kb-diagram-cell">Policy-as-Code 자동 승인</div><div class="kb-diagram-cell">CI/CD 성숙도</div></div>
</div>
</div>



전통적 방식은 단일 승인 절차 레이턴시가 길지만, 컴플라이언스가 엄격한 국방, 금융 시스템에서는 치명적 장애를 격리하고 책임 소재를 명확히 하는 데 유리하다. 반면 [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 방식은 단건 지연은 짧고 수평 확장성이 좋아, 트래픽 변동이 크고 잦은 배포가 필요한 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 환경에서는 전체 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 기준으로 더 유리하다. 

**과목 융합 관점:**
- <strong>보안 (<a href="/knowledge-base/studynote/04_software_engineering/uncategorized/653_devsecops_shift_left/">DevSecOps</a>)</strong>: 통제 단계에 보안 스캐닝 도구([SAST](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/491_sast_static_analysis/)/[SCA](/knowledge-base/studynote/09_security/05_web_app_security/453_sca/))를 통합하여, 보안 취약점이 있는 변경은 [CCB](/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/) 심의 이전에 파이프라인에서 자동으로 반려(Block) 처리되도록 구성한다.
- <strong>운영 (<a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/">SRE</a>)</strong>: [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준 목표([SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/))를 기반으로 [에러 예산](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/101_error_budget_sre/)([Error Budget](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/101_error_budget_sre/))이 소진된 경우, CCB가 선제적으로 신규 기능에 대한 CR을 모두 반려하고 안정성 강화 작업만 승인하는 동적 통제 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 취한다.

> **📢 섹션 요약 비유**: 과거에는 왕([CCB](/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/))이 직접 문서를 보고 도장을 찍어야 법이 바뀌었다면, 지금은 헌법재판소 자동 판독기([CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 파이프라인)가 규칙에 맞는지 순식간에 검사하여 통과시키는 자율 주행 통제 방식과 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

실무에서 형상 통제는 모든 변경에 동일한 잣대를 들이대면 병목이 발생하여 프로젝트가 마비된다. 따라서 변경의 성격에 따라 차등화된 통제 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)([Tailoring](/knowledge-base/studynote/04_software_engineering/01_overview_principles/058_methodology_tailoring/))이 필수적이다.

이 의사결정 플로우는 실무에서 긴급도에 따라 어떻게 형상 통제를 우회 또는 가속할지를 판단하는 기준을 제시한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">CR 수신</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">서비스 중단 등 긴급한 장애인가?</div><div class="kb-diagram-note">──(Yes)──&gt;</div><div class="kb-diagram-node">Emergency CCB (사후 승인 가능)</div></div>
<div class="kb-diagram-note">↓ (Hotfix 배포)</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">(No)</div><div class="kb-diagram-node">정상화 후 공식 문서 보완</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">단순 UI 수정 등 경미한 변경인가?</div><div class="kb-diagram-note">──(Yes)──&gt;</div><div class="kb-diagram-node">Local CCB (PL 단독 승인)</div></div>
<div class="kb-diagram-note">(No)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">구조적 영향을 미치는 주요 변경인가?</div><div class="kb-diagram-note">──(Yes)──&gt;</div><div class="kb-diagram-node">정규 CCB 소집 및 전체 영향 분석</div></div>
</div>
</div>



이 흐름의 핵심은 긴급 변경(Hotfix)과 정규 변경을 분리하여 처리한다는 점이다. 따라서 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간([MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/))은 불필요한 절차 대기로 인해 악화되지 않으며, 사후 기록을 통해 통제 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 유지한다. 실무에서는 이 지점의 예외 허용 조건(Emergency 기준)을 명확히 문서화해야 권한 남용을 막을 수 있다.

#### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/) 및 치명적 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 사례
1. **유령 변경 (Ghost Changes)**: [CCB](/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/) 절차를 우회하여 개발자가 운영 서버에 직접 코드를 덮어쓰는 행위. 다음 배포 시 덮어써진 코드가 증발(Regression)하는 치명적 장애를 유발한다. **실무 판단**: 운영 환경에 대한 배포는 반드시 승인된 파이프라인(빌드 서버)만을 통해서 이루어지도록 접근 제어를 차단해야 한다.
2. <strong>형식적 <a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/">CCB</a> 운영</strong>: 기술적 검토 없이 결재 도장만 찍는 요식 행위. 병목만 유발하고 품질 향상에 기여하지 못한다. **실무 판단**: 변경 전/후 코드 차이(Diff)와 자동화된 테스트 결과를 기반으로만 승인이 이루어지는 시스템적 강제가 필요하다.

> **📢 섹션 요약 비유**: 고속도로 톨게이트에서 모든 차량(변경)을 정밀 검사하면 교통지옥이 되므로, 일반 차량은 하이패스로 통과시키고 의심되는 대형 화물차(중대한 변경)만 차단막을 내리고 꼼꼼히 검사하는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 필요합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

형상 통제를 철저히 수행했을 때의 도입 전후 효과는 다음과 같다.

| 구분 | 도입 전 | 도입 후 (기대효과) |
|:---|:---|:---|
| <strong>소프트웨어 <a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">무결성</a></strong> | 무분별한 덮어쓰기로 인한 버그 잦음 | [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)된 코드만 병합되어 높은 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 유지 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/156_requirements_traceability_vertical_horizontal/">요구사항 추적성</a></strong> | 왜 코드가 바뀌었는지 알 수 없음 | CR과 커밋(Commit) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 매핑으로 완벽 추적 |
| **범위 관리** | [범위 크리프](/knowledge-base/studynote/04_software_engineering/03_design_architecture/161_scope_creep_requirements_inflation_prevention/)([Scope Creep](/knowledge-base/studynote/04_software_engineering/03_design_architecture/161_scope_creep_requirements_inflation_prevention/)) 발생 | 예산/일정 외의 무리한 변경 차단 |

**미래 전망**: [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/)와 GitOps의 부상으로, 형상 통제의 중심이 사람의 회의(Meeting)에서 **선언적 시스템의 상태 수렴(Reconciliation)** 과정으로 이동하고 있다. 즉, Git 저장소에 반영된 선언적 코드([Desired State](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/080_kube_controller_manager_desired_state/))와 실제 운영 상태(Actual [State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/))가 다를 때, 자동화 도구(ArgoCD 등)가 이를 일치시키는 방식으로 형상 통제가 코드 레벨로 진화 중이다. IEEE 828 표준 또한 이러한 자동화된 통제 및 추적성 강화를 주요 권고 사항으로 포함하고 있다.

> **📢 섹션 요약 비유**: 견고한 형상 통제는 마구잡이로 자라나는 잡초를 정원사가 정교한 가위로 다듬는 것과 같아, 결과적으로 소프트웨어라는 나무가 기형적으로 자라지 않고 튼튼하게 성장할 수 있도록 지탱해 줍니다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))

- <strong><a href="/knowledge-base/studynote/04_software_engineering/01_overview_principles/021_configuration_identification/">형상 식별</a> (<a href="/knowledge-base/studynote/04_software_engineering/01_overview_principles/021_configuration_identification/">Configuration Identification</a>)</strong> | 통제해야 할 대상([CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/))을 찾아 이름을 붙여주는 선행 작업
- <strong><a href="/knowledge-base/studynote/04_software_engineering/01_overview_principles/023_configuration_audit/">형상 감사</a> (<a href="/knowledge-base/studynote/04_software_engineering/01_overview_principles/023_configuration_audit/">Configuration Audit</a>)</strong> | CCB의 승인을 받은 변경이 실제로 정확하게 반영되었는지 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 사후 단계
- <strong><a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/">베이스라인</a> (<a href="/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/">Baseline</a>)</strong> | 변경 통제의 기준점이 되는 공식적으로 승인된 특정 시점의 산출물 묶음
- <strong>풀 리퀘스트 (<a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/">Pull Request</a>)</strong> | 최신 Git 기반 협업에서 동료의 리뷰를 거쳐 코드를 병합하는, 현대화된 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)형 [CCB](/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/) 프로세스
- <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/">GitOps</a></strong> | Git을 단일 진실의 원천(SSOT)으로 삼아 인프라와 앱의 변경을 선언적으로 통제하는 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 운영론

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">변경 요청 (Change Request) — 개발자/이해관계자</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">CCB (Configuration Control Board) 심의 — 승인/반려</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">베이스라인 (Baseline) 업데이트 — 공식 산출물 묶음</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">형상 감사 (Configuration Audit) — 무결성 검증</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">GitOps — Git을 SSOT로 삼는 현대화된 통제 자동화</div></div>
</div>
</div>


변경 요청이 [CCB](/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/) 심의를 거쳐 [베이스라인](/knowledge-base/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/)에 반영되고 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)로 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)되며, GitOps가 이 전 과정을 자동화·선언적으로 통제하는 현대 [구성 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/089_configuration_management/) 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명
1. 게임의 규칙을 바꾸고 싶을 때, 친구들 몰래 혼자 맘대로 바꾸면 모두가 화를 내며 싸우게 돼요.
2. 그래서 규칙을 바꾸고 싶으면 "왜 바꿔야 하는지" 종이에 적어서 반장과 친구들(위원회)에게 허락을 받아야 해요.
3. 이렇게 허락받은 것만 진짜 규칙으로 바꾸는 과정을 '형상 통제'라고 한답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 22 / 973

← **이전**: [21. 형상 식별 (Configuration Identification) - 형상 항목(CI) 선정](/knowledge-base/studynote/04_software_engineering/01_overview_principles/021_configuration_identification/)
**다음**: [23. 형상 감사 (Configuration Audit)](/knowledge-base/studynote/04_software_engineering/01_overview_principles/023_configuration_audit/) →

---
