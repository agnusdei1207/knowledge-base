+++
title = "88. 클라우드 ERP (SaaS ERP) - 2 Tier ERP 구조 (본사는 On-Premise 구축형 무거운 ERP, 지사는 SaaS 형태 가벼운 ERP 혼용)"

[taxonomies]
tags = ["enterprise_systems"]

[extra]
tags = ["enterprise_systems"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: `2-Tier ERP` 구조는 통제와 표준화가 필요한 본사에는 무거운 구축형([On-Premise](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)) ERP를, 민첩성과 현지화가 필요한 해외 지사나 계열사에는 가벼운 `SaaS (Software as a Service)` ERP를 배치하는 혼합형 아키텍처다.
> 2. **가치**: 전 세계 모든 지사에 본사용 ERP를 구축할 때 발생하는 막대한 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 비용과 배포 시간을 극적으로 줄이면서도, 재무/인사 등 핵심 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 중앙 통제력을 유지할 수 있다.
> 3. **판단 포인트**: 지사에서 발생하는 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)의 실시간 통합 수준을 어디까지 요구할 것인지, 그리고 [마스터 데이터](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/)(Master [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))의 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 권한을 본사가 얼마나 꽉 쥐고 있을지가 아키텍처 성패를 가른다.

---

## Ⅰ. 개요 및 필요성

전통적인 글로벌 기업들은 전 세계 모든 지사에 본사와 동일한 단일 글로벌 [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)(Single Instance [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/))를 롤아웃(Roll-out)하려 했다. 그러나 지사마다 세금 제도가 다르고, 비즈니스 규모가 작아 수백억 원의 구축형 `ERP (Enterprise Resource Planning)`를 감당할 IT 인력도, 예산도 부족했다. 결국 프로젝트는 수년씩 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)되고 지사들은 엑셀로 비밀 장부를 만드는 섀도우 IT([Shadow IT](/knowledge-base/studynote/12_it_management/01_governance_strategy/049_shadow_it/))가 만연해졌다.

이 딜레마를 해결하기 위해 등장한 것이 <strong>2-Tier <a href="/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/">ERP</a></strong> 모델이다. 본사는 글로벌 재무 연결과 생산 계획을 통제하는 코어(Tier 1)를 유지하고, 지사나 인수합병(M&A)된 자회사는 브라우저만 있으면 당장 쓸 수 있는 클라우드 기반의 [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)(Tier 2)를 도입하여 두 시스템을 `EAI (Enterprise Application Integration)`나 API로 느슨하게 연결하는 방식이다.

- **📢 섹션 요약 비유**: 대형 항공모함(본사)이 좁은 해협의 모든 섬에 직접 정박하려다 좌초되는 대신, 민첩한 쾌속정([SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)) 여러 대를 띄워 섬의 물건을 싣고 모함으로 가져오게 만드는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

2-Tier [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) 구조의 핵심은 "어디서 무엇을 처리하고, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 어떻게 합치는가"에 대한 명확한 역할 분담이다. [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) ERP는 `Multi-tenant(다중 임대)` 아키텍처를 기반으로 하여 인프라 관리 부담이 없고 벤더가 자동으로 규제를 업데이트해 준다.

| 구성 요소 | Tier 1 (본사 / Core) | Tier 2 (지사 / Edge) |
| :--- | :--- | :--- |
| **배포 형태** | [On-Premise](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 또는 [Private Cloud](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/008_private_cloud/) | [퍼블릭 클라우드](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/007_public_cloud/) 기반 [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) |
| **주요 역할** | 글로벌 연결 결산, [SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [마스터 데이터](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) 통제 | 현지 영업, 구매, 현지 세무/HR 처리 |
| **커스터마이징** | 비즈니스 특화 로직 반영 (High) | 표준 프로세스 수용 강제 (Low) |
| <strong>유지보수(<a href="/knowledge-base/studynote/12_it_management/01_governance_strategy/016_tco/">TCO</a>)</strong> | 내부 IT 조직이 전담 (고비용) | 구독료 지불, 벤더가 업데이트 (저비용) |



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2-Tier ERP 데이터 동기화 아키텍처</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Tier 1: 본사 글로벌 ERP</div><div class="kb-diagram-note">(SAP S/4HANA, Oracle 등)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">실적</div><div class="kb-diagram-cell">마스터 데이터 (품목, 고객, 환율 등) 하향 전파</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">결산</div><div class="kb-diagram-cell">(MDM 통제)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">상향</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ API / EAI / Batch 연동 계층</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Tier 2</div><div class="kb-diagram-cell">Tier 2</div><div class="kb-diagram-cell">Tier 2</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(A국 지사)</div><div class="kb-diagram-cell">(B국 지사)</div><div class="kb-diagram-cell">(C국 자회사</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">SaaS ERP</div><div class="kb-diagram-cell">SaaS ERP</div><div class="kb-diagram-cell">SaaS ERP</div></div>
</div>
</div>


이 아키텍처가 굴러가기 위한 필수 원리는 <strong><a href="/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/">MDM</a> (Master <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a> <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/">Management</a>)</strong> 이다. 본사가 품목 코드나 고객 코드를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하여 지사로 뿌려주어야만, 나중에 지사들이 올려보낸 재무 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 본사에서 깨짐 없이 합산(Consolidation)할 수 있다.

- **📢 섹션 요약 비유**: 프랜차이즈 본사(Tier 1)가 메뉴와 가격표([마스터 데이터](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/))를 정해서 내려보내면, 각국 가맹점(Tier 2)은 현지 POS기로 물건을 팔고 그날 저녁 매출액만 본사로 전송하는 시스템이다.

---

## Ⅲ. 비교 및 연결

2-Tier ERP는 단일 [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)(Single Tier) 체제와 비교할 때 극명한 트레이드오프를 가진다.

| 비교 축 | Single Tier (단일 글로벌 [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)) | 2-Tier (본사 [On-Premise](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) + 지사 [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/)) |
| :--- | :--- | :--- |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 정합성</strong> | 100% 실시간 일치 (동일 DB 사용) | 연동 주기에 따른 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 발생 (Batch 등) |
| **구축 속도(Agility)** | 수년 소요, 현지 법인 [저항](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/003_resistance/) 극심 | 수개월 내 도입, [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) 표준 기능 즉시 사용 |
| **인수합병(M&A) 대응** | 새로 구축하여 통합하기 매우 어려움 | 피인수 기업에 SaaS만 깔아주면 즉시 통합 가능 |
| **IT 거버넌스** | 중앙 집중 완벽 통제 | 본사-지사 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 맵핑 및 인터페이스 관리 필요 |

클라우드 시대로 넘어오면서 [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) 자체가 `AI (Artificial Intelligence)` 기반의 예측 기능이나 자동화된 세무 패치를 제공하기 시작했다. 따라서 지사는 무거운 본사 시스템을 강요받는 시나리오보다 SaaS를 쓸 때 현지 규제 대응력이 훨씬 높아진다.

- **📢 섹션 요약 비유**: 단일 ERP는 모든 직원이 하나의 거대한 엑셀 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 동시에 수정하는 것이고, 2-Tier는 각자 자기 장부에 적고 퇴근 전에 본사 장부에 합계만 붙여넣는 방식이다. 속도는 빠르지만 합칠 때 규칙([마스터 데이터](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/))이 틀리면 엉망이 된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 2-Tier [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) 전환 프로젝트가 실패하는 가장 큰 이유는 "SaaS에 [On-Premise](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 시절의 버릇(과도한 커스터마이징)을 버리지 못할 때" 발생한다.

### 설계 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. <strong>지사의 요구사항을 <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/">SaaS</a> 시스템에 코딩으로 개발하려 하는가?</strong>
   - **판단**: 절대 회피. SaaS의 본질은 [멀티 테넌트](/knowledge-base/studynote/03_network/17_sdn_nfv/888_multi_tenant_cloud_resource_isolation_noisy_neighbor/)이므로 코어 소스를 수정할 수 없다. `PaaS (Platform as a Service)` 환경을 연동하여 확장 앱을 외부에서 개발(`Side-by-Side Extensibility`)하거나, 지사의 프로세스를 [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) 표준에 맞춰야(Fit-to-Standard) 한다.
2. <strong><a href="/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/">마스터 데이터</a>의 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a> 권한을 지사에 위임했는가?</strong>
   - **판단**: 회피. 지사가 마음대로 '노트북'을 '컴퓨터'로 코드를 따서 등록하면 본사 결산 시 매출이 찢어진다. `MDM` [허브](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/)를 통해 본사가 [마스터 데이터](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/)를 중앙 통제해야 한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 본사가 지사의 모든 일일 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)(전표 단위)을 실시간으로 가져오려고 [EAI](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/143_eai_enterprise_application_integration_hub/) 연동 주기를 초 단위로 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)하는 것. 이는 클라우드 네트워크 비용을 폭증시키고 시스템 장애를 유발한다. 지사의 일일 마감 후 요약([Summary](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/300_summary/)) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 가져오는 것이 2-Tier의 기본이다.

- **📢 섹션 요약 비유**: 렌탈 아파트([SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/))에 입주하면서 집주인에게 벽을 허물고 방을 늘려달라(커스터마이징)고 요구하면 쫓겨난다. 내 짐(프로세스)을 아파트 구조에 맞춰야 한다.

---

## Ⅴ. 기대효과 및 결론

2-Tier [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) 모델은 글로벌 비즈니스의 <strong>"통제력(Control)과 민첩성(Agility)"</strong>이라는 상충하는 두 마리 토끼를 잡을 수 있는 가장 현실적인 아키텍처다. [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 구축 비용(CAPEX)을 낮추고, 운영 비용(OPEX)을 예측 가능하게 만들며, 새로운 시장 진출이나 M&A 시 IT 통합의 병목을 없애준다.

다만, 두 개의 다른 시스템이 돌아가므로 `API` 연동의 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 맵핑 룰, [보안 정책](/knowledge-base/studynote/09_security/01_intro_principles/007_security_policy/)의 파편화라는 새로운 관리 숙제가 남는다. 결론적으로 기업의 [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 더 이상 '거대한 하나의 괴물'을 만드는 것이 아니라, 각 비즈니스 노드의 민첩성에 맞는 적절한 무게의 `SaaS`를 조합(Composable)하는 방향으로 나아가고 있다.

- **📢 섹션 요약 비유**: 머리는 하나(통제)여도, 손과 발은 각자의 환경에 맞게 가장 가볍고 빠른 도구([SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/))를 쥐여주어야 거인(기업)이 쓰러지지 않고 빠르게 달릴 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/">SaaS</a> (<a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/185_saas_software_as_a_service/">Software as a Service</a>)</strong> | 인프라, 플랫폼, 애플리케이션을 모두 벤더가 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 형태로 제공하는 클라우드 모델 |
| <strong><a href="/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/">MDM</a> (Master <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a> <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/">Management</a>)</strong> | 2-Tier [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) 환경에서 양쪽 시스템이 같은 언어(코드)로 소통하게 해주는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [기준 정보 관리](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/268_mdm_master_data_management/) 체계 |
| **Fit-to-Standard** | 시스템을 회사에 맞추지 않고, 회사의 업무를 글로벌 표준 [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) 시스템 기능에 맞추는 구축 방법론 |
| <strong><a href="/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/143_eai_enterprise_application_integration_hub/">EAI</a> / <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a></strong> | 본사의 [On-Premise](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) ERP와 지사의 [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) 간에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 주고받게 해주는 통합 미들웨어/인터페이스 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Single Instance ERP (단일 글로벌 롤아웃) · 막대한 TCO 및 지연</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">SaaS ERP의 성숙 (보안, 현지 규제 자동화)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">2-Tier ERP Architecture (본사 코어 통제 + 지사 민첩성 확보)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Side-by-Side Extensibility (SaaS 코어는 건드리지 않고 외부 PaaS에서 확장 기능 개발)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Composable ERP / Postmodern ERP (비즈니스 모듈별로 다양한 SaaS를 조립하여 사용)</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 아주 큰 장난감 회사(본사)는 로봇을 만드는 복잡한 큰 기계(구축형 [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/))가 필요해요.
2. 하지만 동네 장난감 가게(지사)들은 그 큰 기계 대신, 태블릿으로 주문만 받는 가벼운 앱([SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/309_saas/) [ERP](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/))이 훨씬 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 편하죠.
3. 이렇게 대장과 꼬마들이 각자 자기 몸집에 딱 맞는 장부를 따로 쓰면서도, 저녁에는 계산을 딱 맞추는 똑똑한 방법을 '2-Tier 구조'라고 불러요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 88 / 482

← **이전**: [87. ERP 패키지의 장점 - 베스트 프랙티스(Best Practice) 내재화, 통합 데이터베이스 구축, 유지보수 용이](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/087_erp_package_advantages_best_practice/)
**다음**: [89. 포스트 모던 ERP (Postmodern ERP) - 거대하고 무거운 단일 모놀리식 벤더 중심에서 벗어나, 코어 ERP와 각 부문별](/knowledge-base/studynote/07_enterprise_systems/02_erp_systems/089_postmodern_erp_best_of_breed/) →

---
