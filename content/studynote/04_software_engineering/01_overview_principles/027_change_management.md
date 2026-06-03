+++
title = "27. 변경 관리 (Change Management) — 소프트웨어 변경의 체계적 통제"
date = 2026-04-29

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/)(Change [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/))는 소프트웨어 개발 및 운영 중 발생하는 모든 변경(요구사항 변경, [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 수정, 기능 추가)을 공식 프로세스로 통제하여 변경의 영향 범위를 분석하고 품질·일정·비용 영향을 관리하는 [SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/)([Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/))의 핵심 활동이다.
> 2. **가치**: 체계적 [변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/) 없이 임의로 변경이 이루어지면 코드베이스가 일관성을 잃고, [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)되지 않은 변경이 운영 환경에 배포되어 장애를 유발한다. [ITIL](/knowledge-base/studynote/12_it_management/02_itsm_itil/062_itil/) v4에서 [변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/)는 "변경 사후 장애 비율([Change Failure Rate](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/025_change_failure_rate_cfr/))"을 핵심 KPI로 정의한다.
> 3. **판단 포인트**: [변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/)의 핵심 결정 포인트는 "긴급 변경(Emergency Change)과 일반 변경(Standard/Normal Change)의 승인 경로 분리"다. 긴급 변경은 사후 승인·검토를 허용하되, 사후 반드시 PIR(Post-Implementation [Review](/knowledge-base/studynote/04_software_engineering/03_design_architecture/153_requirements_review_inspection_walkthrough/))을 수행해야 한다.

---

## Ⅰ. 개요 및 필요성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">변경 관리 프로세스 흐름</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1. 변경 요청(RFC)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2. 영향 분석 (Impact Assessment)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3. 변경 승인 (CAB: Change Advisory Board)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">4. 변경 구현 (Implementation)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">5. 검토 및 종료 (PIR: Post-Implementation Review)</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: [변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/)는 건물 리모델링 허가 프로세스다. 임의로 벽을 허물면 건물이 무너질 수 있으니(장애), 설계 검토→허가→시공→검수 단계를 반드시 거친다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 변경 유형 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)

| 유형 | 정의 | 승인 경로 |
|:---|:---|:---|
| **표준 변경** | 사전 승인된 반복 변경 | 사전 등록 후 자동 승인 |
| **일반 변경** | 계획된 신규 변경 | [CAB](/knowledge-base/studynote/12_it_management/02_itsm_itil/080_cab/) 사전 검토·승인 |
| **긴급 변경** | 즉각 대응 필요 | [ECAB](/knowledge-base/studynote/12_it_management/02_itsm_itil/081_feature_engineering/) 긴급 승인 + 사후 PIR |

### 영향 분석 (Impact Assessment) 항목

```text
□ 영향 범위: 어떤 서비스·컴포넌트에 영향?
□ 위험도: 변경 실패 시 영향 심각도?
□ 롤백 계획: 실패 시 원복 절차?
□ 테스트 계획: 어떻게 검증할 것인가?
□ 리소스: 인력·시간·비용 추정
```

- **📢 섹션 요약 비유**: 영향 분석은 도미노 넘어뜨리기 전 시뮬레이션이다. 이 도미노(변경)가 넘어지면 어느 도미노([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))까지 영향이 가는지 미리 확인하고, 막을 방법을 준비한다.

---

## Ⅲ. 비교 및 연결

| 비교 | [ITSM](/knowledge-base/studynote/12_it_management/02_itsm_itil/096_iso_iec_20000_itsm_certification/) [변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/) | [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) [변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/) |
|:---|:---|:---|
| 승인 방식 | 위원회([CAB](/knowledge-base/studynote/12_it_management/02_itsm_itil/080_cab/)) | 자동화 파이프라인 |
| 속도 | 주 단위 | 시간·분 단위 |
| 위험 관리 | 수동 검토 | 자동 테스트·[검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| 변경 기록 | [변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/) 시스템 | Git 히스토리 |

- **📢 섹션 요약 비유**: [ITSM](/knowledge-base/studynote/12_it_management/02_itsm_itil/096_iso_iec_20000_itsm_certification/) [변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/)는 정부 기관 허가 프로세스(느리지만 철저)이고, [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) [변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/)는 스타트업의 빠른 시험 출시(빠르지만 자동 안전장치 필수)이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### DevOps에서 [변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/) 자동화
- [GitOps](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/): Git 커밋이 변경 요청 → [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 리뷰가 [CAB](/knowledge-base/studynote/12_it_management/02_itsm_itil/080_cab/) 역할 → [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 파이프라인이 자동 배포.
- [Feature Flag](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/): 코드 배포와 기능 활성화 분리 → 긴급 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 지원.

### [DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) [Change Failure Rate](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/025_change_failure_rate_cfr/) 관리
- Elite 조직: 배포 후 장애 비율 < 5%.
- 변경 실패 시 [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) 단축 + PIR → 재발 방지 루프.

- **📢 섹션 요약 비유**: GitOps는 디지털 법원 기록 시스템이다. 모든 변경이 Git에 기록되고(증거 보존), PR은 판사 검토([CAB](/knowledge-base/studynote/12_it_management/02_itsm_itil/080_cab/)), [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 통과는 법원 허가(승인)다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **품질 보증** | [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)된 변경만 운영 환경 배포 |
| **추적 가능성** | 모든 변경의 이력·승인 기록 유지 |
| **위험 감소** | 사전 영향 분석으로 장애 예방 |

[AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 변경 위험 예측(Change [Risk](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) Prediction)은 과거 변경 이력과 코드 변경 패턴을 학습하여 특정 변경의 장애 발생 확률을 자동으로 추정하는 방향으로 발전하고 있다.

- **📢 섹션 요약 비유**: [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 변경 위험 예측은 자동 기상 예보다. 과거 날씨 패턴(변경 이력)을 학습해 "이 코드 변경은 70% 확률로 장애가 날 수 있습니다"고 자동으로 경보를 울린다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/">SCM</a></strong> | [변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/)를 포함하는 [소프트웨어 형상 관리](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/648_ccb_configuration_control_board/) |
| <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/080_cab/">CAB</a></strong> | 변경 승인을 결정하는 위원회 |
| **RFC** | 공식 변경 요청 문서 |
| **PIR** | 변경 후 효과 검토 활동 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/">GitOps</a></strong> | DevOps의 코드 기반 [변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/) 자동화 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">수동 변경 — 비공식 변경, 추적 불가</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">ITSM 변경 관리 — CAB 중심 공식 프로세스</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Agile 변경 관리 — 스프린트 내 변경 통합</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">DevOps/GitOps — CI/CD 기반 자동화 변경 관리</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">AI 위험 예측 — 변경 실패율 자동 예측·경보</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. [변경 관리](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_change_enablement/)는 건물 공사 허가 과정이에요! 마음대로 벽을 허물면 건물이 무너지니까(장애 발생), 반드시 설계→검토→허가→시공→검수 단계를 거쳐요.
2. DevOps에서는 Git에 모든 변경이 기록되고, 자동 테스트가 허가 역할을 해줘요!
3. AI는 과거 변경 기록을 학습해서 "이 변경은 장애가 날 것 같아요"라고 미리 경고해주기도 한답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 27 / 973

← **이전**: [26. VCS (Version Control System) — 형상 이력 관리 시스템](/knowledge-base/studynote/04_software_engineering/01_overview_principles/026_version_control_system/)
**다음**: [28. 소프트웨어 리엔지니어링 (Software Reengineering)](/knowledge-base/studynote/04_software_engineering/01_overview_principles/028_software_reengineering/) →

---
