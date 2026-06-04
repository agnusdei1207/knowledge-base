+++
title = "124. SLA (Service Level Agreement) - 서비스 수준 계약·위반 시 책임"
date = 2026-04-19

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SLA는 <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 제공자와 고객 간의 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 품질에 대한 공식 계약</strong>이며, [SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) 미달 시 <strong>크레딧 환불·위약금 등 법적 책임</strong>이 발생하는 비즈니스 문서이다.
> 2. **가치**: SLA가 없으면 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 장애 시 "얼마나 보상받을 수 있는가?"에 대한 기준이 없지만, SLA는 <strong>99.9% <a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a> 미달 시 월 요금의 <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/">10</a>% 크레딧</strong> 등 명확한 보상 규칙을 정의한다.
> 3. **판단 포인트**: [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/869_sla/) ≥ [SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/)(내부 목표가 더 엄격해야 여유 확보)이며, 클라우드 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(AWS·GCP·Azure)는 모두 공개 SLA를 제공한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    SLI -> SLO -> SLA 계층                              |
+-------------------------------------------------------+
|  SLI = 99.95% (측정 결과)                             |
|  SLO = 99.9% (내부 목표) -> SLI > SLO ✅ OK          |
|  SLA = 99.5% (고객 계약) -> SLI > SLA ✅ 계약 준수    |
|                                                       |
|  SLI가 SLA 미달(99.4%):                              |
|   -> 계약 위반 -> 월 요금 10% 크레딧 반환             |
|                                                       |
|  핵심: SLO(엄격) > SLA(느슨) -> 내부 여유 확보        |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: SLA는 보험 계약이다. "화재(장애) 시 보험금(크레딧) 지급"처럼, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 품질 미달 시 보상을 약속한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 클라우드 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/869_sla/) 예시

| [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/869_sla/) | 위반 시 |
|:---|:---|:---|
| **AWS EC2** | 99.99% | [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~30% 크레딧 |
| **GCP Compute** | 99.99% | [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~50% 크레딧 |
| <strong>Azure <a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/">VM</a></strong> | 99.95% | [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~100% 크레딧 |

### [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/869_sla/) 포함 항목
1. <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 범위</strong>: 어떤 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 적용되는가.
2. <strong><a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a> 목표</strong>: 99.9%, 99.99% 등.
3. **측정 방법**: [SLI](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/) 정의·측정 주기.
4. **위반 보상**: 크레딧 비율·청구 절차.
5. **면책 조항**: 불가항력·유지보수 시간.

- **📢 섹션 요약 비유**: SLA는 식당 메뉴판의 "음식이 30분 안에 안 나오면 무료!" 같은 품질 보증이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [SLI](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/) | [SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/) | [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/869_sla/) |
|:---|:---|:---|:---|
| **성격** | 측정 | 내부 목표 | **외부 계약** |
| **위반 시** | 알림 | Budget 소진 | **법적 보상** |
| **엄격도** | - | 높음 | **낮음** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/869_sla/) 설계 [Best Practice](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/087_erp_package_advantages_best_practice/)
1. SLO를 SLA보다 엄격하게 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) (여유 확보).
2. [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/869_sla/) 위반 알림을 Error Budget이 50% 시점에 발동.
3. 유지보수 윈도우는 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/869_sla/) 계산에서 제외.

---

## Ⅴ. 기대효과 및 결론

SLA는 <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> <a href="/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/">신뢰성</a>의 비즈니스 표현</strong>이며, [SLI](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/)->[SLO](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/)->[Error Budget](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/101_error_budget_sre/)->SLA의 체계적 관리가 SRE의 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/102_sli_slo_service_level_indicator_objective/">SLI</a></strong> | SLA의 측정 기반 |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/">SLO</a></strong> | SLA보다 엄격한 내부 목표 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/101_error_budget_sre/">Error Budget</a></strong> | SLO에서 파생, [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/869_sla/) 준수 여유 |
| **크레딧** | [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/869_sla/) 위반 시 보상 수단 |
| **면책 조항** | 불가항력·유지보수 제외 규정 |

### 📈 관련 키워드 및 발전 흐름도

```text
[전통 SLA (통신·호스팅, 2000s)]
    |
    v
[클라우드 SLA (AWS·GCP·Azure, 2010~)]
    |
    v
[SRE — SLI/SLO/Error Budget 체계 (2016)]
    |
    v
[OpenSLO — SLA/SLO를 코드로 정의 (2022~)]
    |
    v
[현재: AI SLA — AI 서비스 성능 보장 계약]
```

### 👶 어린이를 위한 3줄 비유 설명
1. SLA는 식당의 **"30분 안에 안 나오면 무료!"** 같은 약속이에요.
2. 약속([SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/869_sla/))을 못 지키면 **돈을 돌려줘야(크레딧)** 해요.
3. 그래서 식당([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))은 <strong>약속보다 더 빨리(<a href="/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/181_slo_service_level_objective/">SLO</a>)</strong> 음식을 내놓으려고 노력해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 124 / 373

<- **이전**: [123. SLO (Service Level Objective) - 서비스 수준 목표 설정과 Error Budget](/knowledge-base/studynote/15_devops_sre/03_sre_observability/123_slo_service_level_objective/)
**다음**: [125. Error Budget (에러 예산) - 신뢰성과 혁신 속도의 균형 도구](/knowledge-base/studynote/15_devops_sre/03_sre_observability/125_error_budget/) ->

---
