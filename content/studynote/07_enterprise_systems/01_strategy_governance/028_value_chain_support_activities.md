+++
title = "28. 가치 사슬 지원 활동 (Value Chain Support Activities)"
date = 2026-04-29

[taxonomies]
tags = ["studynote-enterprise-systems"]

[extra]
tags = ["studynote-enterprise-systems"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 마이클 포터의 [가치 사슬](/knowledge-base/studynote/12_it_management/05_security_compliance/249_value_chain_competitive_analysis/)([Value Chain](/knowledge-base/studynote/12_it_management/05_security_compliance/249_value_chain_competitive_analysis/))에서 지원 활동([Support](/knowledge-base/studynote/14_data_engineering/02_math_mining/084_support_association_rule_transaction/) Activities)은 본원적 활동(Primary Activities)을 가능하게 하는 인프라다. 기업 인프라, 인적 자원 관리(HRM), 기술 개발(R&D), 조달 관리(Procurement) 4가지로 구성된다.
> 2. **가치**: 지원 활동은 직접 가치를 창출하지는 않지만 본원적 활동의 효율성·경쟁력을 결정한다. 탁월한 IT 인프라가 물류 관리를 최적화하고, 우수한 HRM이 R&D 혁신을 가능케 하는 식이다.
> 3. **판단 포인트**: [디지털 전환](/knowledge-base/studynote/12_it_management/01_governance_strategy/055_digital_transformation/)([DX](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/726_platform_engineering_idp_dx/)) 시대에는 지원 활동의 디지털화가 경쟁 우위의 핵심이 됐다. [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 조달 최적화, HR 어낼리틱스, 클라우드 기반 기업 인프라가 본원적 활동의 비용·속도·품질을 결정한다.

---

## Ⅰ. 개요 및 필요성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">포터 가치 사슬 (Porter Value Chain)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">지원 활동:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">기업 인프라 (Finance, Legal, Planning)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">인적 자원 관리 (HRM: Recruitment, Training)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">기술 개발 (R&amp;D, IT, 공정 혁신)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">조달 관리 (Procurement: 원자재·설비 구매)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">↓ 지원 활동이 아래 본원 활동을 지원 ↓</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">입고물류 → 운영 → 출고물류 → 마케팅 → 서비스</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: [가치 사슬](/knowledge-base/studynote/12_it_management/05_security_compliance/249_value_chain_competitive_analysis/) 지원 활동은 무대 뒤의 스태프다. 배우(본원 활동)가 무대에서 빛나려면 조명팀(인프라), 의상팀(조달), 연출팀(기술 개발), 배우 코디(HRM)가 완벽히 지원해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 4대 지원 활동 상세

| 지원 활동 | 핵심 기능 | [DX](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/726_platform_engineering_idp_dx/) 시대 변화 |
|:---|:---|:---|
| **기업 인프라** | 재무·법무·계획·IT | 클라우드 [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/), 디지털 거버넌스 |
| **인적 자원 관리** | 채용·교육·평가·보상 | HR 어낼리틱스, [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 채용 |
| **기술 개발** | R&D, IT, 공정 혁신 | [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/), [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)/ML 플랫폼 |
| **조달 관리** | 원자재·[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 구매 | [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) [공급망](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 최적화, e-Procurement |

### 디지털 지원 활동 혁신



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">전통 지원 활동 DX 혁신</div>
<div class="kb-diagram-note">기업 인프라 → 클라우드 ERP (SAP S/4HANA)</div>
<div class="kb-diagram-note">HRM → AI 채용 (HireVue) + 피플 어낼리틱스</div>
<div class="kb-diagram-note">기술 개발 → DevOps + AI/ML 플랫폼</div>
<div class="kb-diagram-note">조달 → e-Procurement + 공급망 AI (Coupa, Ariba)</div>
</div>
</div>



- **📢 섹션 요약 비유**: [DX](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/726_platform_engineering_idp_dx/) 지원 활동 혁신은 공장 내부를 자동화하는 것이다. 공장 바닥(본원 활동)에서 제품을 만들지만, 자동화된 부품 조달(조달), [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 설비 관리(인프라), 스마트 교육 시스템(HRM)이 효율을 결정한다.

---

## Ⅲ. 비교 및 연결

| 비교 | 본원적 활동 | 지원 활동 |
|:---|:---|:---|
| 직접 가치 창출 | ✅ | ❌ |
| 경쟁 우위 기여 | 직접적 | 간접적·기반적 |
| 예시 | 생산·배송·마케팅 | HR·IT·재무·조달 |

- **📢 섹션 요약 비유**: 본원 활동이 무대 공연이라면, 지원 활동은 공연을 가능케 하는 모든 인프라다. 관객은 배우(본원 활동)를 보지만, 무대 뒤(지원 활동)가 없으면 공연이 불가능하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### IT 기업의 [가치 사슬](/knowledge-base/studynote/12_it_management/05_security_compliance/249_value_chain_competitive_analysis/) 지원 활동 분석
- **기업 인프라**: [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 인프라(AWS/GCP/Azure), [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) 기반 [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/).
- **HRM**: [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 개발자 채용, 지속적 학습 플랫폼(O'Reilly, Coursera).
- **기술 개발**: 내부 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)/ML 플랫폼, [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인, 특허 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)폴리오.
- **조달**: [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 소프트웨어 조달, 클라우드 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 최적화([FinOps](/knowledge-base/studynote/12_it_management/05_security_compliance/344_finops/)).

- **📢 섹션 요약 비유**: IT 기업의 기술 개발 지원 활동은 군대의 병참(Logistics)이다. 전방(제품 개발)이 싸우려면 후방([AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 플랫폼·[DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)·특허)의 지원이 완벽해야 한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **본원 활동 효율 향상** | 지원 활동 강화로 생산·물류·마케팅 최적화 |
| **경쟁 우위 확보** | 경쟁사 대비 우수한 지원 체계로 차별화 |
| **혁신 가속** | 탁월한 R&D·IT 지원으로 제품 혁신 속도 제고 |

[AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시대에는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)/[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 인프라 자체가 핵심 지원 활동이 됐다. [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 학습 클러스터, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼, [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인이 현대 기업의 경쟁력을 결정하는 21세기 [가치 사슬](/knowledge-base/studynote/12_it_management/05_security_compliance/249_value_chain_competitive_analysis/) 지원 활동이다.

- **📢 섹션 요약 비유**: [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 인프라는 현대 기업의 발전소다. 과거에는 전기 인프라가 없으면 공장이 돌아가지 않았듯, 지금은 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 인프라가 없으면 기업 경쟁력을 잃는 시대다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/249_value_chain_competitive_analysis/">가치 사슬</a></strong> | 포터의 경쟁 우위 분석 프레임워크 |
| **본원적 활동** | 지원 활동이 뒷받침하는 주요 가치 창출 활동 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/726_platform_engineering_idp_dx/">DX</a></strong> | 지원 활동의 디지털화 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| <strong><a href="/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/">ERP</a></strong> | 기업 인프라 통합 지원 시스템 |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/344_finops/">FinOps</a></strong> | 클라우드 조달 최적화 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">포터 가치 사슬 — 지원 활동 4가지 정의</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">ERP 도입 — 기업 인프라 통합 자동화</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">HR 어낼리틱스 — 데이터 기반 인적 자원 관리</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">e-Procurement + AI — 조달 자동화·최적화</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">AI/데이터 인프라 — 21세기 핵심 지원 활동</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 지원 활동은 무대 뒤의 스태프예요! 배우(본원 활동)가 공연하려면 조명·의상·음향팀이 완벽히 준비해야 해요.
2. [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시대에는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 인프라와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플랫폼이 가장 중요한 지원 활동이 됐어요!
3. 지원 활동이 강한 기업이 더 빠르고 저렴하게 제품을 만들어 경쟁에서 이길 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 28 / 482

← **이전**: [27. 가치 사슬 본원적 활동 (Value Chain Primary Activities)](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/027_value_chain_primary_activities/)
**다음**: [29. 포터의 5 Forces 모델 (Porter Five Forces)](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/029_five_forces_model/) →

---
