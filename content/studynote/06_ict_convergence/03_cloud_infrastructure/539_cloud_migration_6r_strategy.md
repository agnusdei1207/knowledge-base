+++
title = "539. 클라우드 마이그레이션 6R 전략 (Cloud Migration 6R Strategy)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 마이그레이션 6R [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 각 애플리케이션의 비즈니스 가치, [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/), 클라우드 친화성을 기준으로 최적의 이전 경로를 선택하는 의사결정 프레임워크다.
> 2. **가치**: Rehost(빠른 이전)에서 [Refactor](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)(최고 최적화)까지 비용-효과 스펙트럼이 명확하여, 전체 포트폴리오를 경제적으로 분류할 수 있다.
> 3. **판단 포인트**: 모든 시스템을 [Refactor](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)(재설계)하는 것이 이상적이지만, 비용과 시간 제약에서 Rehost와 Replatform으로 빠른 클라우드 이전 효과를 먼저 확보하는 것이 현실적이다.

---

## Ⅰ. 개요 및 필요성

기업이 [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)(On-Premises) 시스템을 클라우드로 이전할 때, 수백~수천 개의 애플리케이션을 동일한 방식으로 이전하는 것은 비효율적이다. AWS의 Gartner(가트너)가 정의한 <strong>6R 프레임워크</strong>는 각 애플리케이션의 특성에 맞는 최적 이전 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 제시한다.

**마이그레이션 필요성**:
- [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 임대 계약 만료, 하드웨어 노후화
- 클라우드 [탄력성](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/571_resiliency_fault_tolerance_patterns/)(Elasticity), 종량제 비용 모델 확보
- [레거시 시스템 현대화](/knowledge-base/studynote/04_software_engineering/01_overview_principles/034_legacy_system_modernization/), [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) 해소
- [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)/[클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 역량 확보

- **📢 섹션 요약 비유**: 6R은 이사 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다 — 짐을 통째로 옮기거나(Rehost), 가구를 재배치하거나(Replatform), 새 집에 맞게 리모델링하거나([Refactor](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)), 아예 새 가구를 사거나(Repurchase), 필요 없는 짐을 버리거나(Retire), 그냥 안 가거나(Retain).

---

## Ⅱ. 아키텍처 및 핵심 원리

<strong>6R <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a> 전체 구조</strong>:



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">빠른 이전 최고 최적화</div>
<div class="kb-diagram-note">비용 비용</div>
<div class="kb-diagram-note">Rehost Replatform Repurchase Refactor Retire Retain</div>
<div class="kb-diagram-note">(Lift (Lift &amp; (Replace) (Re- (폐기) (현행</div>
<div class="kb-diagram-note">&amp; Shift) Reshape) architect) 유지)</div>
</div>
</div>



| [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 내용 | 이점 | 적합 사례 |
|:---|:---|:---|:---|
| Rehost ([Lift](/knowledge-base/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/) & Shift) | 코드/DB 변경 없이 [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 그대로 이전 | 빠름, 위험 낮음 | 레거시 대용량 이전 |
| Replatform ([Lift](/knowledge-base/studynote/14_data_engineering/02_math_mining/086_lift_association_rule_marketing/) & Reshape) | 최소 변경으로 관리형 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 활용 | 관리 부담 감소 | DB → RDS 전환 |
| Repurchase | 기존 앱 폐기 후 SaaS로 전환 | 유지보수 제거 | [CRM](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/) → Salesforce |
| [Refactor](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) / Re-architect | [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/)로 완전 재설계 | 최고 효과 | 핵심 경쟁력 앱 |
| Retire | 사용 안 되는 앱 폐기 | 비용 절감 | 중복/유휴 시스템 |
| Retain | [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 현행 유지 | 안정성 유지 | 규제, 레이턴시 요구 |

<strong><a href="/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/124_decision_tree/">의사결정 트리</a></strong>:
1. 앱이 더 이상 필요한가? → NO: Retire
2. 클라우드 이전이 적합한가? → NO: Retain
3. 완제품 SaaS가 있는가? → YES: Repurchase
4. 핵심 경쟁력 앱이고 클라우드 최적화 가치가 있는가? → YES: [Refactor](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)
5. 관리형 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 최소 변경 가능한가? → YES: Replatform
6. 나머지: Rehost

- **📢 섹션 요약 비유**: Refactor는 집을 최신 스마트홈으로 전면 리모델링하는 것, Rehost는 가구 배치도 안 바꾸고 그냥 이사하는 것, Retain은 이사 자체를 안 하는 것이다.

---

## Ⅲ. 비교 및 연결

<strong>Rehost vs <a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/">Refactor</a> 비교</strong>:

| 구분 | Rehost | [Refactor](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) |
|:---|:---|:---|
| 소요 시간 | 짧음 (주~월) | 김 (월~년) |
| 비용 | 낮음 | 높음 |
| 클라우드 혜택 | 제한적 (자원 [탄력성](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/571_resiliency_fault_tolerance_patterns/)만) | 완전 ([서버리스](/knowledge-base/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/), 오토스케일, 관리형 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) |
| [기술 부채](/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) | 유지 | 해소 |
| [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) | 낮음 | 중간~높음 |

<strong>7R(최신 <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/">버전</a>)</strong>: Relocate([Hypervisor](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) 수준 이전)를 추가한 확장 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/). AWS VMware Cloud로 VMware 워크로드를 그대로 이전하는 경우.

<strong>마이그레이션 파동(<a href="/knowledge-base/studynote/03_network/11_wireless_mobile_communication/590_wave_ieee_802_11p_dsrc_v2x/">Wave</a>) 접근법</strong>: 전체 앱 포트폴리오를 3~5개 파동으로 나누어 이전. 1파동: 비핵심 앱(Rehost), 2파동: 중요 앱(Replatform), 3파동: 핵심 앱([Refactor](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)) 순서.

- **📢 섹션 요약 비유**: 마이그레이션 파동은 군대 이동과 같다 — 선발대(비핵심 앱)가 먼저 이동하여 기지를 설치하고, 본대(핵심 앱)는 안전이 확보된 후 이동한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**기술사 시험 판단 포인트**:
1. 6R을 비용-효과 스펙트럼으로 설명하고, 각 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)의 적합 기준(비즈니스 가치, 기술 복잡도, 마이그레이션 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/))을 제시한다.
2. 모든 앱을 Refactor하지 않고 포트폴리오를 분류하는 현실적 이유(비용, 시간)를 설명한다.
3. "Quick Win" — Rehost로 빠른 클라우드 이전 효과를 먼저 보여주고 신뢰를 확보하는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 언급한다.

**실무 시나리오**: 제조업 기업의 50개 앱 클라우드 이전 —
- [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)(SAP): Retain (벤더 계약, 레이턴시 요구)
- 구 사내 게시판: Retire (대체 [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) 사용)
- HR 시스템: Repurchase (WorkDay [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) 전환)
- 생산 모니터링: Rehost (빠른 이전 우선)
- 물류 최적화 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/): [Refactor](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) (클라우드 ML [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 활용, 경쟁력 핵심)
- 배치 리포팅 서버: Replatform (EC2 → [Lambda](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) 전환, 최소 변경)

- **📢 섹션 요약 비유**: 6R 분류는 이사할 때 짐을 정리하는 것이다 — 자주 쓰는 것(Rehost), 버릴 것(Retire), 새 것으로 살 것(Repurchase)을 먼저 분류해야 이사가 효율적이다.

---

## Ⅴ. 기대효과 및 결론

6R 기반 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 마이그레이션의 기대 효과:
- **비용 최적화**: Retire/Retain으로 불필요한 클라우드 지출 사전 차단
- <strong><a href="/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/">리스크</a> <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a></strong>: 파동별 이전으로 전체 중단 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 최소화
- <strong><a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/">클라우드 네이티브</a> 전환</strong>: Refactor로 핵심 앱의 [탄력성](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/571_resiliency_fault_tolerance_patterns/), 확장성 확보
- **운영 단순화**: Repurchase([SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/))로 유지보수 부담 이전

클라우드 마이그레이션은 기술 프로젝트인 동시에 <strong>비즈니스 변환 프로젝트</strong>이며, 6R 프레임워크는 이 두 관점을 연결하는 공통 언어다.

- **📢 섹션 요약 비유**: 6R 없는 클라우드 이전은 설계도 없는 이사다 — 짐을 다 옮긴 후에야 새 집에 맞지 않는 가구를 발견하고, 다시 비용을 들여 바꾸는 상황이 생긴다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [IaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) / [PaaS](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) / [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) | [클라우드 서비스 모델](/knowledge-base/studynote/12_it_management/05_security_compliance/201_cloud_service_models_iaas_paas_saas/), 관리 부담 · 499 |
| [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) ([Infrastructure as Code](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/062_infrastructure_as_code/)) | [Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/), 마이그레이션 자동화 · 504 |
| [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) ([Cloud Native](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/199_cloud_native_architecture_msa_cicd_devops/)) | [Refactor](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/), [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/), [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) · 501 |
| [FinOps](/knowledge-base/studynote/12_it_management/05_security_compliance/344_finops/) | 마이그레이션 비용 관리, [TCO](/knowledge-base/studynote/12_it_management/01_governance_strategy/016_tco/) 분석 · 500 |
| [SDDC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/631_sddc/) (Software Defined [Data Center](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)) | [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 현대화, Retain 대안 · 540 |

### 📈 관련 키워드 및 발전 흐름도

```text
[클라우드 서비스 모델 · 관리 부담] → [클라우드 마이그레이션 6R 전략] → [온프레미스 현대화 · Retain 대안]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 클라우드 이사에는 6가지 방법이 있어요 — 가구를 그대로 들고 가거나, 새로 사거나, 아예 안 가거나.
2. Refactor는 새 방에 맞게 집 전체를 새로 꾸미는 것 — 가장 좋지만 시간과 돈이 많이 들어요.
3. Rehost는 짐을 그냥 옮기는 것 — 빠르지만 새 집의 좋은 기능(클라우드 혜택)을 아직 못 쓰는 거예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 539 / 552

← **이전**: [538. 적대적 예제와 차분 프라이버시 방어 (Adversarial Examples and Differential Privacy Defense)](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/538_adversarial_examples_differential_privacy/)
**다음**: [540. SDDC와 HCI 소프트웨어 정의 데이터센터 (SDDC HCI Software-Defined Datacenter)](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/540_sddc_hci_software_defined_appliance/) →

---
