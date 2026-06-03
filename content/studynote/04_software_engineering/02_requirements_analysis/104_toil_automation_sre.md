+++
title = "104. 토일 (Toil) - SRE에서 줄여야 할 단순 반복적 운영 작업"

[taxonomies]
tags = ["software_engineering"]

[extra]
tags = ["software_engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [토일](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/) ([Toil](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/))은 구글의 [SRE](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/)(사이트 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 공학) 철학에서 정의한 개념으로, 시스템 운영자가 수동적이고 반복적으로 수행하는 '자동화 가능하지만 방치된 기술적 단순 노동'을 뜻한다.
> 2. **가치**: 운영 조직이 일시적인 불끄기(Tactical) 작업에 매몰되어 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 개선이라는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 엔지니어링 역량을 상실하는 것을 막는 핵심 진단 지표다.
> 3. **판단 포인트**: 사람의 지적 판단이 필요한 필수 행정 오버헤드(Overhead)와 [토일](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/)을 엄격히 분리하고, [SRE](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) 엔지니어의 [토일](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/) 허용 시간을 50% 이하로 통제하여 남은 시간을 스크립트 기반 영구 자동화 설계에 투자해야 한다.

---

## Ⅰ. 개요 및 필요성

[토일](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/) ([Toil](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/))은 거대한 IT 인프라 시스템을 운영할 때 사람이 직접 키보드와 마우스를 조작하여 간신히 현상 유지를 반복하는 소모적인 기술 노동이다. 서버가 10대에서 100대로 늘어나면 운영자의 수작업 시간도 정확히 10배 선형적으로 증가하는(O(n) 증대) 파괴적 특성을 지닌다.

전통적인 IT 인프라 조직에서는 장애 처리나 계정 발급 같은 수작업을 '당연한 일상 업무'로 여겼다. 하지만 이 노가다를 아무리 열심히 처리해봤자 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 새로운 기능이나 아키텍처가 발전하지 않고 어제와 똑같은 상태를 유지할 뿐이다. SRE는 이런 무의미한 노동에 뛰어난 엔지니어가 번아웃(Burnout)되는 것을 막기 위해 [토일](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/)을 '반드시 측정하고 척결해야 할 [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/)'로 공식 규정했다.

- **📢 섹션 요약 비유**: [토일](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/)은 마당에 물이 고일 때마다 '양동이로 직접 물을 퍼서 버리는 바보 같은 노동'이다. 비가 더 오면 퍼내는 시간도 끝없이 늘어나며, 마당이 근본적으로 좋아지지 않고 그저 물에 잠기는 것만 임시방편으로 막을 뿐이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

구글 SRE는 모든 업무가 [토일](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/)인지 아닌지를 6가지 엄격한 판단 기준으로 분류하여 상태를 측정한다.

| [토일](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/) 판단 기준 | 설명 및 판단 지표 |
|:---|:---|
| **수동적 (Manual)** | 기계가 스케줄러로 돌 수 있음에도 사람이 직접 명령어를 타이핑하여 실행하는가? |
| **반복적 (Repetitive)** | 일회성 작업이 아니라 매일, 매주 동일한 패턴으로 발생하는 작업인가? |
| **자동화 가능 (Automatable)** | 고도의 판단이나 창의력 없이 조건문 코드(if-else)로 완벽히 대체 가능한가? |
| **전술적 (Tactical)** | 아키텍처를 개선하는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/))이 아니라 당장의 알람 불을 끄는 행위인가? |
| **선형적 확장 (O(n))** | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 규모나 트래픽이 커질 때 사람의 노동 시간도 똑같은 비율로 늘어나는가? |
| **가치 창출 전무** | 작업을 완료했을 때 시스템의 기능이 진보하지 않고 그냥 원래 상태로 복귀할 뿐인가? |

```text
┌──────────────────────────────────────────────────────────────┐
│           SRE 엔지니어의 시간 포트폴리오 밸런스 조정           │
├──────────────────────────────────────────────────────────────┤
│  [ 나쁜 예: 운영에 함몰된 레거시 팀 ]                          │
│   ■■■■■■■■■■■■■■■■■■ (90%) : 토일 (알람 끄기, 재부팅)     │
│   ■■ (10%) : 엔지니어링 (새로운 스크립트 작성)                 │
│   => 결과: 시스템 커지면 퇴사자 속출, 신뢰성 붕괴                  │
│                                                              │
│  [ 올바른 예: 토일 50% 캡을 강제한 구글 SRE ]                   │
│   ■■■■■■■■■■ (50% 제한) : 최대치로 묶인 토일 처리 시간        │
│   ■■■■■■■■■■ (50% 보장) : 토일을 자동화하는 전략적 코딩 시간  │
│   => 결과: 내일은 자동화 덕분에 토일이 30%로 줄어드는 선순환 발생   │
└──────────────────────────────────────────────────────────────┘
```

이 다이어그램은 [토일](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/)을 줄이는 것이 단순한 구호가 아니라, 운영자의 강제적 시간 할당 룰을 통해 실현되는 시스템 공학(엔진ering)임을 보여준다.

- **📢 섹션 요약 비유**: 하루 종일 엑셀 복사/붙여넣기만 하도록 직원을 방치하는 것은 회사의 거대한 손실이다. 매일 오전 4시간만 그 작업을 하도록 제한하고, 오후 4시간은 엑셀 매크로 프로그램을 직접 짜도록 강제하여 다음 주부터는 버튼 한 번에 끝나게 만드는 것이 [토일](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/) 척결 원리다.

---

## Ⅲ. 비교 및 연결

조직 내에서 [토일](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/)을 척결하려면 이것이 사람이 꼭 해야 하는 '오버헤드(Overhead)'인지 명확히 구별해야 한다. 이를 혼동하면 시스템 자동화의 방향을 잘못 잡게 된다.

| 비교 항목 | [토일](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/) ([Toil](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/)) | 오버헤드 (Overhead) |
|:---|:---|:---|
| **정의** | 자동화 코드로 대체 가능한 기술적 운영 노가다 | 조직 유지와 성장을 위해 사람이 꼭 해야 하는 간접 관리 업무 |
| **작업 예시** | DB 계정 수동 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 꽉 찬 디스크 수동 삭제, 정기 배포 배포 스크립트 실행 | 팀 주간 회의, [코드 리뷰](/knowledge-base/studynote/04_software_engineering/06_software_architecture/330_code_review/)([PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/)), 연말 인사 평가, 기술 문서 작성 |
| **SRE의 목표** | 50% 이하로 강력히 통제하고 0%를 향해 코드로 소멸시킨다 | 건강한 조직을 위해 필수적이므로 일정 비율 유지 및 포용 |
| **자동화 여부** | 100% 자동화 대상 ([Ansible](/knowledge-base/studynote/15_devops_sre/05_devsecops/198_ansible_os_configuration_management_ssh/), [Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) 등) | 완전 자동화 불가 (인간의 인지적 판단 필요) |

- **📢 섹션 요약 비유**: 식당에서 설거지나 채소 다지기를 사람이 매일 반복하는 것은 기계(식기세척기, 믹서)로 대체해야 할 '[토일](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/)'이지만, 주방장들이 모여서 다음 달 새로운 신메뉴 레시피를 회의하는 시간은 기계가 할 수 없는 필수 '오버헤드'다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [SRE](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) 원칙을 도입할 때 [토일](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/) 관리는 가장 핵심적인 성과 지표([KPI](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/))로 직결된다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. <strong><a href="/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/">토일</a> 50% 캡(<a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/">Cap</a>) 룰의 캘린더 강제화</strong>: 운영 엔지니어의 캘린더를 분석하여 이번 주 티켓(Jira 등) 처리와 알림 대응이 전체 업무 시간의 50%를 초과했는가? 초과했다면 즉시 일반 개발팀으로 운영 티켓(On-call)을 강제 환원시키고, 해당 SRE는 자동화 파이프라인 개발에 투입시켜야 한다.
2. **O(n) 구조 절단**: [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 인스턴스가 10개에서 1,000개로 스케일아웃([Scale-out](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/))될 때, 엔지니어가 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 파일을 1,000번 배포해야 하는가? [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) 도구([Ansible](/knowledge-base/studynote/15_devops_sre/05_devsecops/198_ansible_os_configuration_management_ssh/), Chef)를 이용해 1대의 노력으로 1,000대를 자동 동기화하는 구조가 갖춰져 있는지 판단해야 한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- <strong><a href="/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/">토일</a> 전담 조직 신설</strong>: "SRE는 고급 개발을 해야 하니, 단순 반복 알람 끄기 작업만 전담하는 계약직 운영팀을 따로 뽑자." 이는 [SRE](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) 철학을 정면으로 위배하는 최악의 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)이다. 고통을 직접 느껴야 자동화의 필요성을 알고 코드를 짜게 된다. [토일](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/)을 다른 사람에게 외주화(Outsourcing)하는 순간, 시스템의 영구적 자동화 개선의 기회는 영원히 사라진다.

- **📢 섹션 요약 비유**: 양동이로 물 퍼내는 일이 힘들다고 싼 인건비의 알바생을 고용해서 대신 물을 퍼내게 하는 것은 바보 짓이다. 펌프 기계 자체를 설치하여 물을 빼는 근본적 자동화 아키텍처를 설계하는 것이 시스템 공학의 올바른 결단이다.

---

## Ⅴ. 기대효과 및 결론

[토일](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/) 관리는 무기력한 운영 조직을 능동적인 소프트웨어 개발 조직으로 탈바꿈시키는 구글 SRE의 가장 중요한 촉매제다. 

운영 업무의 50%를 고부가가치 엔지니어링 작업에 의무적으로 투자함으로써, 시스템은 지속적인 자가 치유(Self-healing)와 자동화 파이프라인을 구축하게 된다. 결국 [토일](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/)을 코드로 척결한 조직은 트래픽이 100배 폭증하더라도 엔지니어 인력을 비례해서 늘릴 필요가 없는 무한한 확장성과 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)을 달성하게 된다. [토일](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/)은 단순한 귀찮음의 영역이 아니라 기업 기술 경쟁력의 생사를 가르는 측정 대상이다.

- **📢 섹션 요약 비유**: [토일](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/) 척결은 수동 빨래를 세탁기로 바꾸는 위대한 일상 혁명이다. 기계가 1시간 동안 빨래(단순 노가다)를 알아서 돌려주는 동안, 사람은 책을 읽거나 내일의 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 짜는 고차원적 가치 생산에 집중할 수 있게 된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/">SRE</a> (<a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/">Site Reliability 엔진ering</a>)</strong> | 소프트웨어 엔지니어링 기법을 적용하여 인프라의 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)을 지키고 [토일](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/)을 코드로 소멸시키는 구글의 운영 철학 |
| **자동화 (Automation)** | 인간의 수작업([Toil](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/))을 인프라 애즈 코드([IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)), [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 파이프라인 등을 통해 기계의 영구적인 로직으로 치환하는 무기 |
| **오버헤드 (Overhead)** | [토일](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/)과는 반대로 조직의 커뮤니케이션이나 관리를 위해 반드시 소모되어야 하는 필수적 인간 간접 업무 시간 |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/">SLO</a> (<a href="/knowledge-base/studynote/15_devops_sre/03_sre_observability/123_slo_service_level_objective/">Service Level Objective</a>)</strong> | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 목표. 이 목표가 깨졌을 때만 긴급 불끄기에 들어가고, 달성 중이라면 여유 시간을 [토일](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/) 자동화 개발에 투자한다 |

### 📈 관련 키워드 및 발전 흐름도

```text
레거시 시스템의 수작업 운영 (O(n) 인력 소모)
    │
    ▼
토일(Toil) 6대 조건 기반의 엄격한 판별 및 측정
    │
    ▼
토일 시간 50% 상한(Cap) 통제 룰 적용
    │
    ▼
확보된 시간으로 자동화 스크립트/IaC (Terraform, Ansible) 개발
    │
    ▼
운영 부담(선형 증대) 소멸 및 무한 확장 가능한 신뢰성 아키텍처 완성
```

### 👶 어린이를 위한 3줄 비유 설명

1. [토일](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/)([Toil](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/))은 게임에서 매일 똑같은 몬스터를 천 번씩 클릭해서 잡아야 하는 엄청 지루한 '노가다 작업'이에요.
2. 구글 최고 기술자들은 이렇게 지루한 클릭만 하다가는 사람들이 너무 지쳐버릴 거라고 생각했어요.
3. 그래서 마우스 클릭하는 시간을 반으로 확 줄이고, 남은 시간 동안 '알아서 몬스터를 사냥해주는 자동 사냥 로봇(코드)'을 만들게 해서 모두를 행복하게 만들었답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 104 / 973

← **이전**: [103. SLA (Service Level Agreement)](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/103_sla_service_level_agreement_penalty/)
**다음**: [105. DevSecOps - 보안의 좌측 이동 (Shift-Left Security)](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/105_devsecops_shift_left_security/) →

---
