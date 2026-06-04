+++
title = "CALMS 프레임워크 (CALMS Framework)"
date = 2025-05-14

[taxonomies]
tags = ["studynote-cloud"]

[extra]
tags = ["studynote-cloud"]
+++

## 핵심 인사이트 (3줄 요약)
1. <strong><a href="/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/">데브옵스</a>의 5대 기둥</strong>: Culture(문화), Automation(자동화), [Lean](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/087_lean_software_development_7_principles/)(린 사상), Measurement(측정), Sharing(공유)의 약자로, [데브옵스](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 성숙도를 평가하는 핵심 지표임.
2. **기술 이상의 철학**: 단순히 자동화 도구만 도입하는 것이 아니라, 조직의 일하는 방식 전반을 혁신하는 다각적 프레임워크임.
3. **지속적 개선 도구**: 조직 내 부족한 영역을 식별하고, 각 영역의 균형 잡힌 성장을 통해 비즈니스 가치를 극대화함.

---

### Ⅰ. 개요 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
- **정의**: [데브옵스](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)([DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/))의 성숙도를 측정하고 성공적인 도입을 위해 필수적으로 고려해야 할 5가지 핵심 가치를 정의한 모델.
- **배경**: [데브옵스](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)가 단순 자동화 도구의 집합으로 오해받는 것을 방지하고, 조직 문화와 가치 중심의 접근을 강조하기 위해 제시됨.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **핵심 원리**: 5가지 영역이 상호 유기적으로 연결되어 선순환 구조를 형성함.

```text
[ CALMS Framework Structure ]

      +-----------------------------------------+
      |               SHARING (S)               | <---+
      | (Knowledge, Success, Failure Sharing)   |     |
      +-----------------------------------------+     |
            ^                                         |
      +-----+-----+      +-----------+      +---------+
      | CULTURE (C)|      |LEAN (L)   |      | MEASUREMENT (M) |
      | (Trust,    |      | (Waste    |      | (KPI, Metrics,  |
      |  Blameless)| <--->|  Removal) |<--->|  Data-driven)   |
      +-----+-----+      +-----------+      +---------+
            |                                         ^
            v                                         |
      +-----------------------------------------+     |
      |             AUTOMATION (A)              |-----+
      | (CI/CD, IaC, Test Automation)           |
      +-----------------------------------------+
```

- **5대 핵심 요소**:
    1. **Culture (문화)**: 사람과 프로세스 중심. 팀 간의 신뢰와 공동 책임을 중시.
    2. **Automation (자동화)**: 휴먼 에러 제거 및 효율성 향상. 빌드, 테스트, 배포, 인프라의 자동화.
    3. <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/087_lean_software_development_7_principles/">Lean</a> (린)</strong>: 낭비 제거. 가치 흐름(Value [Stream](/knowledge-base/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/)) 최적화와 작은 단위의 반복 배포.
    4. **Measurement (측정)**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기반 의사결정. [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/), 장애율 등 객관적 지표 관리.
    5. **Sharing (공유)**: 성공과 실패의 경험을 조직 전체가 나누어 동반 성장 유도.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 요소 | 핵심 질문 | 실무 예시 |
| :--- | :--- | :--- |
| **Culture** | 팀 간의 심리적 안전감이 있는가? | [Blameless Post-mortem](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/206_postmortem_blameless_devops_culture/) (비난 없는 회고) |
| **Automation** | 반복적 작업을 기계가 수행하는가? | [Jenkins](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/), [Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/), [Ansible](/knowledge-base/studynote/15_devops_sre/05_devsecops/198_ansible_os_configuration_management_ssh/) 활용 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/087_lean_software_development_7_principles/">Lean</a></strong> | 불필요한 절차나 대기 시간이 없는가? | 승인 절차 간소화, 배치 크기([Batch Size](/knowledge-base/studynote/10_ai/05_data_science_ml/346_batch_size_generalization/)) 축소 |
| **Measurement** | 무엇을 기준으로 개선을 판단하는가? | [DORA Metrics](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/201_dora_metrics_devops_performance/) (배포 빈도, [MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) 등) |
| **Sharing** | 지식이 특정 개인에게만 머물러 있지 않은가? | 기술 세미나, 사내 위키(Wiki) 활성화 |

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
- **실무 적용**: 자동화(A)가 가장 눈에 띄지만, 문화(C)가 뒷받침되지 않으면 도구는 팀 간의 감시 수단으로 전락할 수 있음. 5가지 요소의 균형이 가장 중요함.
- **기술사적 판단**: CALMS는 [데브옵스](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 성숙도 모델의 글로벌 표준이며, 최근에는 'S ([Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/))'를 포함한 CALMSS로 확장되기도 함. 인프라가 복잡해질수록 측정(M)과 공유(S)의 중요성이 더욱 부각됨.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과**: 팀 간 장벽 해소, 제품 출시 기간(Time-to-Market) 단축, 안정적 [서비스 운영](/knowledge-base/studynote/12_it_management/02_itsm_itil/067_service_operation/).
- **결론**: CALMS는 '어떻게 [데브옵스](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)를 할 것인가'에 대한 나침반이며, 기술을 넘어 비즈니스 가치로 연결되는 핵심 가이드임.

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- **상위 개념**: [데브옵스](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/), [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/), 린 경영.
- **관련 모델**: [DORA Metrics](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/201_dora_metrics_devops_performance/), Three Ways of [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/).
- **연관 기술**: [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 도구, 모니터링/로깅 시스템.

### 👶 어린이를 위한 3줄 비유 설명
1. 축구팀이 이기려면 좋은 공(자동화)도 필요하지만, 친구들과 친하게 지내고(문화) 전술을 나누는 것(공유)도 중요해요.

### 📈 관련 키워드 및 발전 흐름도

```text
DevOps 도입 (도구만 도입, 문화 부재)
    |
    v
CALMS: Culture · Automation · Lean · Measurement · Sharing
    |
    v
성숙도 평가: DORA Metrics · SPACE Framework
```

2. 경기가 끝나고 우리가 몇 골을 넣었는지 기록(측정)해서 부족한 점을 찾아요.
3. 불필요한 행동을 줄이고(린) 다 같이 힘을 합쳐야 최고의 팀이 될 수 있다는 약속이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 161 / 371

<- **이전**: [데브옵스 (DevOps: Culture, Automation, Collaboration)](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/161_devops_culture_automation_collaboration/)
**다음**: [지속적 통합 (CI, Continuous Integration)](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/163_continuous_integration_ci_automated_build_test/) ->

---
