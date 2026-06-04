+++
title = "24. Lead Time for Changes — 변경 리드 타임"
date = 2026-04-29

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: LTC ([Lead Time](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/) for Changes, 변경 [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/))는 [DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) ([DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) Research and Assessment) 4대 지표 중 하나로, 코드가 커밋된 시점부터 프로덕션(Production)에 성공적으로 배포되기까지 걸리는 총 시간을 측정하는 소프트웨어 딜리버리 속도 지표다.
> 2. **가치**: LTC는 개발 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인의 병목([Bottleneck](/knowledge-base/studynote/02_operating_system/10_security/617_io_bottleneck/))을 가시화하며, Elite 수준 팀은 LTC < 1시간을 달성하는 반면 Low 팀은 6개월 이상이다. LTC 단축은 고객 피드백 -> 코드 반영 -> 배포까지의 [피드백 루프](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/005_feedback_loop/)를 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)하여 시장 대응력을 높인다.
> 3. **판단 포인트**: LTC는 단순히 배포 자동화 속도가 아닌 [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 리뷰 대기·QA 병목·수동 승인 프로세스 등 모든 대기 시간을 포함한다. LTC 개선의 핵심은 자동화([CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD)보다 먼저 업무 흐름의 대기 시간([Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/) Time) 제거이다.

---

## Ⅰ. 개요 및 필요성

[Lead Time](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/) for Changes는 "아이디어가 실제 사용자에게 전달되기까지 얼마나 걸리는가?"의 소프트웨어 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이다.

```text
+--------------------------------------------------------------+
|           Lead Time for Changes 측정 구간                     |
+--------------------------------------------------------------+
|                                                              |
|  [코드 커밋] ---------------------------- [프로덕션 배포]       |
|      |                                         |            |
|      v                                         |            |
|  CI 빌드·테스트 (자동화, 수 분)                  |            |
|      |                                         |            |
|  PR 리뷰 대기 (수 시간~수 일) <- 주요 병목        |            |
|      |                                         |            |
|  통합 테스트·QA (수 시간~수 일) <- 병목           |            |
|      |                                         |            |
|  배포 승인 프로세스 (수 시간) <- 병목              |            |
|      |                                         |            |
|  CD 배포 (자동화, 수 분) ----------------------->            |
|                                                              |
|  LTC = 전체 구간의 합 (커밋 -> 프로덕션)                        |
+--------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: LTC는 피자 주문에서 수령까지의 총 시간이다. 오븐 굽기(빌드·배포 자동화)보다 주문 대기([PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 리뷰)·배달 대기(QA 병목)가 더 긴 경우가 많아, 오븐 속도보다 줄 서는 시간 단축이 핵심이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 성과 등급별 LTC 기준

| 등급 | LTC | 해당 조직 비율 |
|:---|:---:|:---:|
| **Elite** | < 1시간 | 상위 18% |
| **High** | 1일~1주 | 27% |
| **Medium** | 1주~1개월 | 34% |
| **Low** | > 6개월 | 21% |

### LTC 단축 5대 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

| [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 효과 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/040_trunk_based_development/">Trunk-based Development</a></strong> | [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 리뷰 대기 시간 감소 |
| **소규모 배치(Small Batch)** | [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 크기 축소 -> 리뷰 속도 향상 |
| **자동화 테스트 강화** | QA 병목 제거 |
| **배포 승인 자동화** | 수동 승인 게이트 제거 |
| **Feature Flags** | 배포와 릴리스 분리 -> 위험 감소 |

- **📢 섹션 요약 비유**: LTC 단축은 편의점 계산대 대기 시간 줄이기다. 계산대 속도(자동화)를 높이는 것도 중요하지만, 손님이 줄 서는 시간([PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 대기·QA 병목)이 더 긴 문제를 먼저 해결해야 한다.

---

## Ⅲ. 비교 및 연결

| [DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) 지표 | 측정 대상 | 목표 방향 |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/">Deployment</a> Frequency (DF)</strong> | 배포 빈도 | 높을수록 좋음 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/">Lead Time</a> for Changes (LTC)</strong> | 커밋->배포 시간 | 낮을수록 좋음 |
| <strong><a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/025_change_failure_rate_cfr/">Change Failure Rate</a> (<a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/025_change_failure_rate_cfr/">CFR</a>)</strong> | 배포 실패 비율 | 낮을수록 좋음 |
| <strong>Time to Restore <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">Service</a> (<a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/">MTTR</a>)</strong> | 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간 | 낮을수록 좋음 |

LTC와 DF는 "속도" 지표, CFR과 MTTR은 "안정성" 지표로 서로 보완 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 이룬다.

- **📢 섹션 요약 비유**: DF가 "얼마나 자주 배달하는가"이면, LTC는 "한 번 배달에 얼마나 걸리는가"다. 자주 배달하면서도 빠른 것이 Elite 팀의 특징이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: LTC 30일->4시간 개선
은행 핀테크 팀의 LTC를 30일(Low)에서 4시간(High->Elite 목표)으로 단축.

1. **측정**: JIRA + GitHub 연계로 커밋 시각과 배포 시각 자동 측정.
2. **병목 분석**: [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 리뷰 평균 대기 4일 -> 핵심 병목 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/).
3. **Trunk-based 전환**: 장수 브랜치 제거, 매일 main 머지.
4. <strong><a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/">PR</a> 규칙</strong>: PR당 200줄 이하 코드 변경 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 도입.
5. **자동화 QA**: Playwright [E2E](/knowledge-base/studynote/15_devops_sre/05_devsecops/265_e2e_end_to_ui_selenium/) 테스트 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 통합 -> 수동 QA 80% 제거.
6. **결과**: LTC 30일 -> 4시간 (99% 단축).

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- LTC 측정 없이 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 도구만 도입하는 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/). 자동화 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 구축 후 "빨라졌겠지" 하고 LTC를 측정하지 않으면 실제 병목([PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 대기, QA)이 해소되지 않았음을 모른다. "측정하지 않는 것은 개선할 수 없다(If you can't measure it, you can't improve it)."

- **📢 섹션 요약 비유**: LTC 측정 없이 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD만 도입하는 건, 식당 주방 속도만 올리고 홀 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 대기 시간을 무시하는 것이다. 손님이 느린 이유는 주방이 아니라 홀 대기에 있을 수 있다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **시장 반응 속도** | 고객 피드백->코드->배포 [피드백 루프](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/005_feedback_loop/) 단축 |
| **위험 감소** | 소규모 잦은 배포로 배포당 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 감소 |
| **개발자 생산성** | 대기 시간 감소 -> 몰입(Flow) 상태 향상 |

LTC는 DORA의 SPACE 프레임워크(Satisfaction·[Performance](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)·Activity·Communication·Efficiency)로 확장되어 [개발자 경험](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/058_dx_developer_experience/)(Developer Experience, [DX](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/726_platform_engineering_idp_dx/)) 관점의 생산성 측정으로 발전하고 있다.

- **📢 섹션 요약 비유**: LTC 단축은 가속 페달을 밟는 것이 아니라 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)등(병목)을 제거하는 것이다. 빠른 차([CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 자동화)가 있어도 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)등이 많으면 목적지에 늦게 도착한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/">DORA</a> 4대 지표</strong> | LTC가 속하는 소프트웨어 딜리버리 성과 측정 체계 |
| <strong><a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/040_trunk_based_development/">Trunk-based Development</a></strong> | LTC 단축을 위한 개발 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| **Feature Flags** | 배포와 릴리스 분리 -> LTC 단축 |
| <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/">CI</a>/CD</strong> | LTC 단축의 기술적 기반; 자동화 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 |
| <strong><a href="/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/">DORA</a> Elite</strong> | LTC < 1시간 달성 조직 수준 |

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 배포 — 릴리스 주기 수 개월, 높은 LTC]
    |
    v
[CI/CD 도입 — 자동화 빌드·테스트·배포, LTC 단축 시작]
    |
    v
[Trunk-based + 소규모 배치 — PR 병목 해소]
    |
    v
[DORA 측정 — LTC/DF/CFR/MTTR 데이터 기반 개선]
    |
    v
[Elite DevOps — LTC < 1시간, 지속 개선 문화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. LTC는 피자 가게에서 주문을 받은 후 피자가 완성되어 배달되기까지의 총 시간이에요!
2. 오븐(코드 빌드) 시간보다 주문 받기([PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 리뷰)와 품질 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)(QA) 기다리는 시간이 더 길어서 전체가 느려지는 경우가 많아요.
3. 세계 최고 IT 기업들은 코드를 짜고 1시간 안에 수억 명의 사용자에게 배포할 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 24 / 373

<- **이전**: [23. DORA 배포 빈도 (DORA Deployment Frequency)](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/023_dora_deployment_frequency/)
**다음**: [25. CFR (Change Failure Rate) — 변경 실패율](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/025_change_failure_rate_cfr/) ->

---
