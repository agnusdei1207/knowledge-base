+++
title = "649. 기준선 (Baseline) 수립 변경 통제"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) ([Baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)) 수립 변경 통제은(는) [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

소프트웨어 개발 프로젝트는 끊임없는 '변경'과의 싸움이다. 기획자는 어제 확정한 요구사항을 오늘 아침에 바꾸고, 개발자는 남이 짠 코드를 말없이 고쳐버린다.

결국 한 달 뒤, "어? 로그인 버튼 누가 지웠어?", "내가 어제 수정한 코드가 왜 옛날 코드로 다시 덮어씌워졌지?"라는 절망적인 외침이 개발실에 울려 퍼진다. 여러 명이 협업하는 환경에서 **'누가, 언제, 왜 이 코드를 고쳤는지'** 알 수 없게 되는 순간 시스템은 붕괴된다.

이 무법지대를 통제하기 위해, 건축 공학의 도면 관리 기법을 본떠 만든 것이 <strong><a href="/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/">형상 관리</a>(<a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/089_configuration_management/">Configuration Management</a>)</strong>다. 코드가 수정될 때마다 꼬리표([버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/))를 달고, 중요한 시점에는 굵은 선([베이스라인](/knowledge-base/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/))을 그어 절대 함부로 고치지 못하게 자물쇠를 채우는([형상 통제](/knowledge-base/studynote/04_software_engineering/01_overview_principles/022_configuration_control/)) 위대한 규칙이다.

- **📢 섹션 요약 비유**: 여러 명이 하나의 커다란 모래성을 쌓을 때, 아무나 맘대로 모래를 파내면 성이 무너진다. [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)는 1시간마다 모래성의 사진을 찍어두고([버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리), "이제부터 이 기둥은 완성본이니까 누구도 건드리지 마!"라고 금줄을 치는 것([베이스라인](/knowledge-base/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/))이다.

---

다음은 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) ([Baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)) 수립 변경의 핵심 구조와 흐름을 보여주는 다이어그램이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">기준선 (Baseline) 수립 변경</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">입력/요구사항</div><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">핵심 처리 과정</div><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">출력/결과물</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">요구 분석 설계·적용 품질 검증</div></div>
</div>
</div>



이 다이어그램은 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) ([Baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)) 수립 변경가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 검증된 결과물을 산출하는 흐름을 보여준다.

---

---

---

## Ⅱ. 아키텍처 및 핵심 원리

[형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)는 크게 4가지 절차로 톱니바퀴처럼 맞물려 돌아간다.

- **📢 섹션 요약 비유**: [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) ([Baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)) 수립 변경 통제은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

| 항목 | 설명 | 비고 |
| :--- | :--- | :--- |
| 핵심 특성 | [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) ([Baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)) 수립 변경 통제의 핵심 특성과 동작 방식 | 필수 이해 요소 |
| 적용 범위 | 어떤 프로젝트·상황에서 활용하는지 | 선택 기준 |
| 제약 조건 | 적용 시 주의해야 할 전제·한계 | 트레이드오프 |

---

---

---

## Ⅲ. 비교 및 연결

실무에서 [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)(Configuration Mgt)와 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리(Version Control)를 똑같은 것으로 착각하지만, 포함 관계가 다르다.

| 비교 항목 | [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 (Version Control) | [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) ([Configuration Management](/knowledge-base/studynote/12_it_management/02_itsm_itil/089_configuration_management/)) |
|:---|:---|:---|
| **의미** | 파일의 변경 이력(History)만 관리 | [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리를 포함한 **전사적 변경 통제 프로세스** |
| **관리 대상** | 주로 소스코드 (Source [Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/)) | 소스코드, 기획서, 설계도, DB [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/), 환경설정 |
| **사용 도구** | **Git**, SVN | Git + **Jira** + <strong><a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/">CCB</a> 회의체</strong> |
| **포커스** | "이 코드를 언제 누가 어떻게 합쳤지?" | "이 변경이 비즈니스 일정과 품질에 영향이 없나?" |

Git은 훌륭한 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 도구지만, Git 하나만 쓴다고 [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)가 되는 것은 아니다. 변경 요청 티켓(Jira)과 의사 결정 과정([CCB](/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/))이 묶여야 비로소 [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)가 완성된다.

- **📢 섹션 요약 비유**: [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리(Git)는 '블랙박스 녹화기'다. 사고(변경)가 났을 때 돌려볼 수 있다. [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)는 블랙박스뿐만 아니라, 음주 운전 단속([CCB](/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/))과 차량 정비 일지([감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/))까지 모두 합친 '종합 교통안전 시스템'이다.

---

---

---

---

## Ⅳ. 실무 적용 및 기술사 판단

최근 [데브옵스](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)([DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/))와 [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/)([Agile](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/)) 시대에는 무거운 [CCB](/knowledge-base/studynote/04_software_engineering/03_design_architecture/160_change_control_board_ccb_requirements_review/) 회의를 매번 열 수 없어 [형상 통제](/knowledge-base/studynote/04_software_engineering/01_overview_principles/022_configuration_control/)의 패러다임이 바뀌었다.

- **📢 섹션 요약 비유**: [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) ([Baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)) 수립 변경 통제은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

---

---

---

## Ⅴ. 기대효과 및 결론

[베이스라인](/knowledge-base/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/)과 깐깐한 CCB를 거치는 [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) 체계가 완성되면, 배포 날 끔찍한 버그가 터져도 당황할 필요가 없다. 1초 만에 어제 찍어둔 [베이스라인](/knowledge-base/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/)(Tag v1.0)으로 완벽하게 <strong><a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/">롤백</a>(<a href="/knowledge-base/studynote/02_operating_system/05_deadlock/313_rollback/">Rollback</a>)</strong>할 수 있기 때문이다. 이 심리적 안전감이 개발자들의 코딩 속도를 오히려 3배 이상 빠르게 만들어 준다.

결론적으로 [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)는 단순한 코드 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 도구가 아니다. <strong>"우리의 소프트웨어는 어제 어떤 상태였고, 오늘은 어떤 상태이며, 내일은 어떻게 변할 것인가?"</strong>를 완벽하게 통제하고 기록하는 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 심장이다. [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)가 무너진 프로젝트는 아무리 천재 개발자 100명을 모아놔도 모래성처럼 흩어질 뿐이다.

- **📢 섹션 요약 비유**: [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)는 '타임머신'이다. 실수를 해서 세상이 멸망하더라도, 언제든 가장 평화로웠던 어제([베이스라인](/knowledge-base/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/))로 시간을 돌릴 수 있다. 타임머신이 있는 영웅(개발팀)은 어떤 괴물(버그) 앞에서도 두려움 없이 과감하게 싸울 수 있다.

---

---

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) ([Software Engineering](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)) | [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) ([Baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)) 수립 변경 통제의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [소프트웨어 생명주기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/003_sdlc/) ([SDLC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/), Software Development Life Cycle) | [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) ([Baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)) 수립 변경 통제은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) ([Baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)) 수립 변경 통제 적용 결과는 QA 활동을 통해 검증되고 측정된다 |
| [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) ([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)) | [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) ([Baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)) 수립 변경 통제에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">소프트웨어 위기 (Software Crisis) 인식</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">기준선 (Baseline) 수립 변경 통제 개념 정립</div>
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

1. [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) ([Baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)) 수립 변경 통제은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 816 / 973

← **이전**: [649. 기준선 (Baseline) 수립 변경 통제](/knowledge-base/studynote/04_software_engineering/uncategorized/649_baseline_change_control/)
**다음**: [650. CI/CD 지속적 통합, 배포 파이프라인](/knowledge-base/studynote/04_software_engineering/uncategorized/650_ci_cd_pipeline/) →

---
