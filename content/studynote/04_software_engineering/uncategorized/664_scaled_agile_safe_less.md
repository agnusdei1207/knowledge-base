+++
title = "664. 대규모 애자일 SAFe, LeSS"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [대규모 애자일](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/092_scaled_agile_frameworks_overview/) [SAFe](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/), LeSS은(는) [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

- **개념**: [대규모 애자일](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/092_scaled_agile_frameworks_overview/) 프레임워크([Scaled Agile](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/092_scaled_agile_frameworks_overview/) Frameworks)는 단일 [스크럼](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/062_scrum_framework_overview/) 팀의 범위를 넘어 다수의 팀, 부서, 나아가 전사적 차원에서 [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) 가치와 실천법을 적용하기 위한 조직 설계 및 운영 방법론이다. 대표적으로 딘 레핑웰(Dean Leffingwell)이 창시한 무겁고 체계적인 <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/">SAFe</a></strong>와 크레이그 라만(Craig Larman) 등이 창시한 가볍고 [스크럼](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/062_scrum_framework_overview/) 친화적인 <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/094_less_large_scale_scrum/">LeSS</a></strong>가 있다.
- **필요성**: 소규모 팀 단위의 [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/)은 성공적이나, 기업 전체로 보면 수십 개의 [스크럼](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/062_scrum_framework_overview/) 팀이 서로 다른 방향으로 달리거나 의존성(Dependency) 문제로 인해 통합 시점에 거대한 충돌이 발생하는 '[애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) [사일로](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)([Agile](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) [Silo](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/))' 현상이 발생한다. 대규모 시스템을 개발하기 위해서는 이 팀들을 하나의 제품 비전으로 묶어줄(Alignment) 정교한 [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) 메커니즘이 필수적으로 요구되었다.
- **💡 비유**: 단일 [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) 팀이 빠르고 민첩한 '스피드보트'라면, [대규모 애자일](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/092_scaled_agile_frameworks_overview/)은 이 수십 대의 스피드보트들이 서로 부딪히지 않고 하나의 거대한 목적지를 향해 대형을 유지하며 항해하도록 지휘하는 '함대 사령부' 시스템과 같다.

- **등장 배경 및 발전 과정**:
  1. <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/062_scrum_framework_overview/">스크럼</a>의 한계</strong>: [스크럼](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/062_scrum_framework_overview/)은 3~9명의 단일 팀을 위한 완벽한 프레임워크지만, 100명이 넘는 개발자가 하나의 거대한 [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) 시스템을 만들 때는 어떻게 협업해야 하는지 가이드하지 않았다.
  2. <strong>SoS (<a href="/knowledge-base/studynote/04_software_engineering/uncategorized/658_agile_scrum_roles/">Scrum</a> of Scrums)의 부족</strong>: 각 팀의 [스크럼](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/062_scrum_framework_overview/) 마스터들이 모이는 SoS 기법이 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)에 도입되었으나, 단순한 소통 창구 역할에 그쳐 전사적 예산 기획과 아키텍처 정렬을 해결하지 못했다.
  3. **엔터프라이즈 프레임워크의 탄생**: 이에 따라 기업의 기존 거버넌스와 [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/)을 타협시킨 [SAFe](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/)(2011년)가 대기업을 중심으로 폭발적으로 성장했고, 이에 반발하여 [스크럼](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/062_scrum_framework_overview/) 본연의 단순함을 유지하려는 [LeSS](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/094_less_large_scale_scrum/), Spotify 모델 등이 대안으로 등장하며 시장을 양분하게 되었다.

규모가 커짐에 따라 단일 [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) 팀에서 발생하는 의존성 지옥(Dependency Hell)과 이를 대규모 프레임워크가 어떻게 구조화하는지를 시각적으로 대비해 볼 수 있다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">단일 애자일의 한계(Silo) vs 대규모 애자일(정렬) 비교</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">확장 전: 애자일 사일로 및 의존성 지옥</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(Team A) ──서로 일정 안맞음──▶ (Team B)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">스프린트 스프린트</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">▼ 통합 실패 (Integration Hell) ▼</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">결과물 A</div><div class="kb-diagram-connector">◀</div><div class="kb-diagram-node">결과물 B</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">* 문제: 각자 빠르지만, 통합하면 시스템이 동작하지 않음.</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">확장 후: 대규모 애자일(Scaled Agile) 정렬 메커니즘</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">전사 비전 / 포트폴리오 백로그</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">▼ 동기화된 릴리스 기차 (예: SAFe ART) ▼</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(Team A) (Team B)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">동일한 주기의 동일한 주기의</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">스프린트 진행 스프린트 진행</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">▶ 지속적 통합 ◀</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">하나의 완성된 시스템</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">* 해결: 동일한 박자(Cadence)와 통합 이벤트로 전체 정렬 확보.</div></div>
</div>
</div>



**[다이어그램 해설]** 확장 전의 모습은 각 팀이 자신만의 백로그와 [스프린트](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/067_sprint_timebox/) 주기를 가지고 독립적으로 달리는 상황이다. 소프트웨어의 크기가 작을 때는 문제가 없으나, 마이크로서비스나 대형 플랫폼처럼 시스템 간 결합도가 높은 환경에서는 A팀이 B팀의 API를 기다리며 노는(Block) 현상이나, 나중에 합쳤을 때 구조가 어긋나는 통합 지옥이 필연적으로 발생한다. [대규모 애자일](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/092_scaled_agile_frameworks_overview/)은 상위에 '포트폴리오 백로그'를 두어 목표를 통일하고, 아래의 모든 팀이 [스프린트](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/067_sprint_timebox/) 시작일과 종료일(Cadence)을 완벽히 맞추어 정기적으로 결과물을 강제 통합([Synchronization](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/))하게 만듦으로써 부분 최적화가 아닌 전체 최적화를 달성한다.

- **📢 섹션 요약 비유**: 각자 뛰어난 악기 연주자들([애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) 팀)이 모였다고 교향곡이 되는 것이 아니라, 모두가 동일한 악보(비전)를 보고 지휘자의 일치된 박자(Cadence)에 맞춰야 훌륭한 오케스트라([대규모 애자일](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/092_scaled_agile_frameworks_overview/))가 완성되는 것과 같습니다.

---

---

---

---

## Ⅱ. 아키텍처 및 핵심 원리

[대규모 애자일](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/092_scaled_agile_frameworks_overview/) [SAFe](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/), LeSS의 핵심 원리와 구성 요소를 이해하기 위해 다음 구조를 살펴본다.

| 구성 요소 | 역할 | 적용 기준 |
| :--- | :--- | :--- |
| 개념 정의 | 핵심 용어와 범위를 명확히 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) | 용어 혼용·오해 방지 |
| 원칙 및 규칙 | 적용 시 따라야 할 기본 방향 | [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)·품질 기준 |
| 기법 및 도구 | 실질적 구현 방법과 지원 도구 | 생산성·자동화 |
| 측정 지표 | 결과물의 품질을 정량화하는 지표 | 의사결정 근거 |

[대규모 애자일](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/092_scaled_agile_frameworks_overview/) [SAFe](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/), LeSS의 핵심 원리는 **복잡성 분해**, **역할 분리**, <strong>품질 측정</strong>의 세 축으로 이해할 수 있다. 복잡한 문제를 관리 가능한 단위로 나누고, 각 역할의 책임을 명확히 하며, 결과를 정량적 지표로 평가하는 과정이 반복된다.

- **📢 섹션 요약 비유**: [대규모 애자일](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/092_scaled_agile_frameworks_overview/) [SAFe](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/), LeSS의 아키텍처는 공장의 생산 라인과 같다. 각 공정(구성 요소)이 명확한 역할을 가지고 정해진 순서대로 움직여야 최종 제품의 품질이 보장된다. 어느 한 공정이 부실하면 전체 제품이 불량이 된다.

---

---

---

## Ⅲ. 비교 및 연결

[대규모 애자일](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/092_scaled_agile_frameworks_overview/) [SAFe](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/), LeSS을(를) 유사 개념과 비교하면 경계와 특성이 더 명확해진다.

| 비교 항목 | [대규모 애자일](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/092_scaled_agile_frameworks_overview/) [SAFe](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/), [LeSS](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/094_less_large_scale_scrum/) | 유사 대안 |
| :--- | :--- | :--- |
| 핵심 목적 | 체계적 품질·생산성 향상 | 임시 방편적 해결 |
| 적용 규모 | 중·대규모 프로젝트에서 효과적 | 소규모에서는 오버헤드 발생 가능 |
| 조직 요건 | 팀 전체의 공통 이해와 훈련 필요 | 개인 역량 의존 |
| 측정 가능성 | 정량적 지표로 성과 측정 가능 | 주관적 판단에 의존 |

다른 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) 개념과의 연결을 보면, [대규모 애자일](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/092_scaled_agile_frameworks_overview/) [SAFe](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/), LeSS은(는) 요구공학·설계·테스트·형상관리 전반에 걸쳐 영향을 미친다. 특히 품질 보증(QA, Quality Assurance)과 [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/))와 긴밀하게 연계된다.

- **📢 섹션 요약 비유**: [대규모 애자일](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/092_scaled_agile_frameworks_overview/) [SAFe](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/), LeSS과 유사 대안의 차이는 지도를 가지고 산에 오르는 것과 감으로만 오르는 차이와 같다. 지도(체계적 방법)가 있으면 정상까지 최단 경로를 찾을 수 있지만, 없으면 같은 곳을 맴돌거나 낭떠러지에 빠질 수 있다.

---

---

---

## Ⅳ. 실무 적용 및 기술사 판단

[대규모 애자일](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/092_scaled_agile_frameworks_overview/) [SAFe](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/), LeSS을(를) 실무에 적용할 때는 다음 판단 기준을 참고한다.

- **📢 섹션 요약 비유**: [대규모 애자일](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/092_scaled_agile_frameworks_overview/) [SAFe](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/), LeSS은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

---

---

## Ⅴ. 기대효과 및 결론

[대규모 애자일](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/092_scaled_agile_frameworks_overview/) [SAFe](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/), LeSS을(를) 올바르게 적용하면 [소프트웨어 품질](/knowledge-base/studynote/04_software_engineering/06_software_architecture/339_software_quality_definition/)·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·팀 생산성이 동시에 향상된다. 그러나 도입에는 학습 비용과 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 투자가 필요하며, 조직 전체의 공감과 훈련이 선행되어야 한다.

**한계와 전제 조건**:
- 소규모 프로젝트에서는 오버헤드가 발생할 수 있다
- 팀 전체의 충분한 교육과 실습 기간이 필요하다
- 도구 지원 환경 구축에 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 비용이 발생한다

**미래 발전 방향**:
- [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)·[LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 기반 자동화 도구와의 통합으로 적용 효율 향상
- [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/)·[DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 환경에서의 진화적 적용
- 정량적 측정 체계의 고도화를 통한 의사결정 지원 강화

[대규모 애자일](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/092_scaled_agile_frameworks_overview/) [SAFe](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/), LeSS은 '어떻게 빠르게 짜는가'가 아니라 '어떻게 오래 유지할 수 있는 소프트웨어를 짜는가'에 대한 답이다. 단기 속도보다 장기 지속 가능성을 추구하는 관점으로 기억해야 한다.

- **📢 섹션 요약 비유**: [대규모 애자일](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/092_scaled_agile_frameworks_overview/) [SAFe](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/), LeSS의 기대효과는 마라톤 훈련과 같다. 처음에는 느리고 고통스럽지만, 올바른 훈련 원칙을 지킨 선수만이 결승선에서 최고의 기록을 낼 수 있다. [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 원칙도 단기 편의보다 장기 완성도를 위한 투자다.

---

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) ([Software Engineering](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)) | [대규모 애자일](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/092_scaled_agile_frameworks_overview/) [SAFe](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/), LeSS의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [소프트웨어 생명주기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/003_sdlc/) ([SDLC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/), Software Development Life Cycle) | [대규모 애자일](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/092_scaled_agile_frameworks_overview/) [SAFe](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/), LeSS은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | [대규모 애자일](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/092_scaled_agile_frameworks_overview/) [SAFe](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/), [LeSS](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/094_less_large_scale_scrum/) 적용 결과는 QA 활동을 통해 검증되고 측정된다 |
| [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) ([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)) | [대규모 애자일](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/092_scaled_agile_frameworks_overview/) [SAFe](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/), LeSS에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">소프트웨어 위기 (Software Crisis) 인식</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">대규모 애자일 SAFe, LeSS 개념 정립</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">표준화 및 방법론 체계화 (ISO, CMMI, Agile)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">클라우드 네이티브·AI 기반 확장 적용</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">지속적 개선 및 DevOps·MLOps 통합</div>
</div>
</div>



이 흐름은 [소프트웨어 위기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/002_software_crisis/) 인식 → 체계적 방법론 개발 → 표준화 → 현대적 플랫폼 적용으로 이어지는 발전 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [대규모 애자일](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/092_scaled_agile_frameworks_overview/) [SAFe](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/093_safe_scaled_agile_framework_art_pi/), LeSS은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 834 / 973

← **이전**: [663. 스토리 포인트 플래닝 포커 합의](/knowledge-base/studynote/04_software_engineering/uncategorized/663_story_point_planning_poker/)
**다음**: [665. 린 스타트업 MVP 피벗 사이클](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/665_lean_development_7_principles/) →

---
