---
title: "201. DORA 메트릭스 (DORA Metrics)"
date: "2026-04-21"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Google [DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) Research and Assessment팀이 6년간 3만 개 이상 조직을 연구하여 도출한 [DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 성과의 4가지 표준 측정 지표 — 배포 빈도(DF), 변경 [리드 타임](/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/)(LTC), [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간([MTTR](/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/)), 변경 실패율([CFR](/studynote/15_devops_sre/01_culture_methodology/025_change_failure_rate_cfr/))이다.
> 2. **가치**: DORA는 "얼마나 빠르게(Velocity)"와 "얼마나 안정적으로([Stability](/studynote/08_algorithm_stats/02_sorting/021_stability/))"를 동시에 측정하여, 속도와 품질이 트레이드오프가 아닌 함께 높일 수 있음을 데이터로 증명했다.
> 3. **판단 포인트**: Elite 팀은 하루 여러 번 배포하면서도 변경 실패율 5% 미만을 달성한다. 이는 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD 자동화·테스트 문화·심리적 안전감이 동시에 성숙했을 때만 가능하다.

---

## Ⅰ. 개요 및 필요성

[DORA](/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/)([DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) Research and Assessment)는 Nicole Forsgren, Jez Humble, Gene Kim이 주도한 연구 프로그램으로, 2014년부터 매년 "[State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) of [DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) Report"를 발행한다. 이 연구는 단순한 기술 채택 현황 조사를 넘어, <strong>특정 <a href="/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/">DevOps</a> 관행이 조직 성과에 어떤 영향을 미치는지</strong>를 인과관계 수준에서 밝혔다.

[DORA](/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 연구의 핵심 발견은 "소프트웨어 배포 성과가 조직 전체의 비즈니스 성과(수익성, 시장 점유율, 고객 만족도)와 강한 양의 상관관계를 갖는다"는 것이다. 즉, 개발 속도와 품질을 높이는 것이 비즈니스 경쟁력 자체를 높이는 것이다.

이를 측정하기 위해 4개의 핵심 지표를 정의했다: 배포 빈도([Deployment](/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/) Frequency), 변경 [리드 타임](/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/)([Lead Time](/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/) for Changes), [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간([MTTR](/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/): Mean Time to Restore), 변경 실패율([Change Failure Rate](/studynote/15_devops_sre/01_culture_methodology/025_change_failure_rate_cfr/)). 이 4개 지표로 팀을 Elite, High, Medium, Low 4개 등급으로 분류할 수 있다.

📢 **섹션 요약 비유**: [DORA](/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 메트릭은 자동차 계기판과 같다. 속도계(배포 빈도·리드타임)만 보면 빠르게 달리는지 알 수 있지만, 연료계·온도계(실패율·[복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간)도 함께 봐야 안전한지 알 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [DORA](/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 4대 지표 상세

| 지표 | 측정 대상 | Elite 기준 | Low 기준 |
|:---|:---|:---:|:---:|
| 배포 빈도 (DF) | 코드가 프로덕션에 배포되는 빈도 | 하루 여러 번 | 1~6개월에 1번 |
| 변경 리드타임 (LTC) | 코드 커밋부터 프로덕션 배포까지 시간 | 1시간 미만 | 1~6개월 |
| [MTTR](/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 장애 발생부터 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)까지 시간 | 1시간 미만 | 1~6개월 |
| 변경 실패율 ([CFR](/studynote/15_devops_sre/01_culture_methodology/025_change_failure_rate_cfr/)) | 배포가 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 장애를 유발한 비율 | 0~5% | 46~60% |

### 4개 지표의 두 축

```
  +-----------------------------------------------------+
  |                    DORA 지표 구조                     |
  +--------------------------+--------------------------+
  |    처리량 (Throughput)    |    안정성 (Stability)     |
  |                          |                          |
  |  ① 배포 빈도              |  ③ MTTR                  |
  |  (Deployment Frequency)  |  (Mean Time to Restore)  |
  |                          |                          |
  |  ② 변경 리드타임          |  ④ 변경 실패율            |
  |  (Lead Time for Changes) |  (Change Failure Rate)   |
  +--------------------------+--------------------------+
              |                           |
              v                           v
        빠른가? (속도)             안전한가? (품질)
```

### 팀 등급별 성과

| 등급 | 배포 빈도 | 리드타임 | [MTTR](/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) | 실패율 |
|:---:|:---:|:---:|:---:|:---:|
| **Elite** | 하루 여러 번 | < 1시간 | < 1시간 | 0~5% |
| **High** | 주 1회~하루 1회 | 1일~1주 | < 1일 | 5~[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)% |
| **Medium** | 주 1회~월 1회 | 1주~1개월 | 1일~1주 | [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~15% |
| **Low** | 월 1회 이하 | 1개월~6개월 | > 1주 | 16~30% |

📢 **섹션 요약 비유**: Elite 팀은 F1 레이서처럼 시속 300km로 달리면서도 사고율이 오히려 낮다. 빠른 속도와 높은 안전성이 반드시 트레이드오프가 아님을 [DORA](/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 데이터가 증명한다.

---

## Ⅲ. 비교 및 연결

### [DORA](/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) vs SPACE 프레임워크

| 항목 | [DORA](/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) | SPACE |
|:---|:---|:---|
| 초점 | 배포 파이프라인 성과 | 개발자 생산성 전반 |
| 측정 대상 | 시스템(팀 수준) | 개인·팀·시스템 |
| 지표 수 | 4개 | 5개 차원 |
| 한계 | 비엔지니어링 작업 미포함 | 주관적 지표 포함 |
| 보완 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | [DORA](/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) + SPACE 함께 사용 권장 |  |

### [DORA](/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 지표와 기술 관행 연결

| [DORA](/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 지표 향상 | 필요한 기술 관행 |
|:---|:---|
| 배포 빈도^ | [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD 자동화, [트렁크 기반 개발](/studynote/15_devops_sre/01_culture_methodology/040_trunk_based_development/), 작은 배포 단위 |
| 리드타임v | 자동화 테스트, [코드 리뷰](/studynote/04_software_engineering/06_software_architecture/330_code_review/) 속도, 배포 파이프라인 최적화 |
| [MTTR](/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/)v | 관찰성([Observability](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/)), 자동 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/), 인시던트 [관리 프로세스](/studynote/15_devops_sre/01_culture_methodology/018_admin_processes/) |
| 변경 실패율v | 테스트 커버리지, [카나리](/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)·[피처 플래그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/), 코드 품질 |

📢 **섹션 요약 비유**: DORA와 SPACE의 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)는 병원의 혈액 검사([DORA](/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/))와 건강 설문(SPACE)의 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)다. 혈액 검사는 객관적 수치를 주고, 설문은 환자가 느끼는 상태를 알려준다. 둘 다 필요하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong><a href="/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/">DORA</a> 지표 측정 방법 (<a href="/studynote/12_it_management/02_itsm_itil/874_configuration_item/">CI</a>/CD 도구 활용)</strong>:
```
배포 빈도 측정:
  CI/CD 시스템(Jenkins, ArgoCD)의 프로덕션 배포 이벤트 카운트
  -> 일/주/월 단위 집계

리드타임 측정:
  Git 커밋 타임스탬프 -> 프로덕션 배포 완료 타임스탬프
  -> 두 시간의 차이를 중앙값 또는 p75로 측정

MTTR 측정:
  인시던트 발생 시각 -> 서비스 완전 복구 시각
  -> PagerDuty, OpsGenie 등 인시던트 관리 도구에서 자동 측정

변경 실패율 측정:
  (장애 유발 배포 수 / 전체 배포 수) × 100
```

<strong><a href="/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/">DORA</a> 성숙도 향상 로드맵</strong>:
```
Low -> Medium:   CI 도입, 테스트 자동화 시작
Medium -> High:  CD 자동화, 카나리 배포 적용
High -> Elite:   완전 자동화 파이프라인, 카오스 엔지니어링
```

**기술사 판단 포인트**:
- [DORA](/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 지표는 "경쟁"이 아닌 "개선 추적" 도구다. 다른 팀과 비교보다 자신의 팀 트렌드 추적이 중요하다.
- 지표 개선을 위한 지름길(예: 작은 테스트만 배포해 빈도를 높임)은 실제 역량과 괴리를 만든다.
- 2023년 [DORA](/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 보고서에서 "[신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)([Reliability](/studynote/04_software_engineering/06_software_architecture/345_reliability_security/))"이 5번째 지표로 추가됐다.

📢 **섹션 요약 비유**: [DORA](/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 지표 개선은 다이어트와 같다. 체중계 숫자를 낮추기 위해 물을 빼는 지름길이 있지만, 실제 건강해지려면 식습관과 운동 문화를 바꿔야 한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 설명 |
|:---|:---|
| 성과 가시화 | [DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 투자의 효과를 경영진에게 데이터로 제시 |
| 개선 방향 명확화 | 4개 지표 중 어떤 것이 병목인지 진단 |
| [벤치마킹](/studynote/07_enterprise_systems/04_process_consulting/219_benchmarking_best_practice/) | 업계 Elite 기준과의 격차를 명확히 인식 |
| [기술 부채](/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/) | 낮은 [DORA](/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 점수 = [기술 부채](/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/)의 정량적 증거 |

[DORA](/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 메트릭은 DevOps의 "성적표"다. 6년간 수만 개 조직 데이터로 검증된 이 지표는, 소프트웨어 개발 성과를 비즈니스 언어로 번역하는 가장 강력한 도구다. 기술사 시험에서도 [DORA](/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 4개 지표의 정의와 Elite 기준, 그리고 각 지표 개선을 위한 기술 관행의 연결이 핵심 출제 포인트다.

📢 **섹션 요약 비유**: [DORA](/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 메트릭은 스포츠 선수의 기록표(타율, ERA, 기록)와 같다. 숫자 자체가 목표가 아니라, 어떤 훈련이 어떤 기록을 향상시키는지 이해하고 개선 계획을 세우는 데 사용한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD 파이프라인 | 배포 빈도와 리드타임 개선의 핵심 기술 인프라 |
| [카나리 배포](/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/) | 변경 실패율 감소에 직접 기여 |
| [Observability](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/) | [MTTR](/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) 단축을 위한 빠른 장애 감지 인프라 |
| [피처 플래그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/) | 변경 실패율 감소 + 배포 빈도 증가 동시 기여 |
| SPACE 프레임워크 | DORA와 보완하여 개발자 생산성 전반 측정 |
| 심리적 안전감 | [DORA](/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) Elite 팀의 공통된 비기술적 특성 |

### 👶 어린이를 위한 3줄 비유 설명

1. [DORA](/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 메트릭은 학교 성적표처럼, 우리 개발팀이 얼마나 자주 배포하는지(출석), 얼마나 빠른지(속도), 실수가 얼마나 적은지(정확도) 점수로 보여줘.

### 📈 관련 키워드 및 발전 흐름도

```text
DORA 4대 메트릭
    +-► 배포 빈도 (Deployment Frequency)
    +-► 변경 리드 타임 (Lead Time for Changes)
    +-► 변경 실패율 (Change Failure Rate)
    +-► MTTR (Mean Time to Recovery)
    |
    v
Elite · High · Medium · Low 성숙도 등급
```
2. 엘리트 팀은 하루에 여러 번 배포해도 실수가 5%도 안 돼. 빠르면서 정확한 거야.
3. 점수가 낮다고 절망하지 말고, 어떤 과목(지표)이 낮은지 찾아서 그것만 집중 개선하면 돼.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 200 / 371

<- **이전**: [200. IDP / Backstage (Internal Developer Platform)](/studynote/13_cloud_architecture/04_devops_observability/200_internal_developer_platform_backstage/)
**다음**: [202. SPACE 프레임워크 (SPACE Framework)](/studynote/13_cloud_architecture/04_devops_observability/202_space_framework_agile_performance/) ->

---
