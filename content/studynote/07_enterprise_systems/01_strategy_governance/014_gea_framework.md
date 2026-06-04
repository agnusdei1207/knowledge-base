+++
title = "14. 범정부 EA 프레임워크 (GEA) - 공공기관 정보화 아키텍처 의무 지침"
description = "공공부문의 정보화 투자 효율성 제고와 상호운용성 보장을 위한 범정부 전사적 아키텍처 프레임워크(GEA)의 구조와 컴플라이언스 분석"
date = 2024-05-24

[taxonomies]
tags = ["enterprise_systems"]

[extra]
tags = ["enterprise_systems"]
+++

# 14. 범정부 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 프레임워크 ([GEA](/knowledge-base/studynote/12_it_management/03_ea_isp/115_gea_government_ea_framework/), Government [Enterprise Architecture](/knowledge-base/studynote/12_it_management/01_governance_strategy/806_ea_enterprise_architecture/))

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 범정부 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 프레임워크([GEA](/knowledge-base/studynote/12_it_management/03_ea_isp/115_gea_government_ea_framework/))는 개별 부처별로 난립하던 공공 정보시스템을 국가 차원에서 하나의 거대한 가상 엔터프라이즈로 간주하고 표준화, 통합, [상호운용성](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/287_interoperability_tactics/)을 통제하기 위한 아키텍처 [참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/)이자 지침이다.
> 2. **가치**: 미국의 FEAF를 모델로 하여, 중복 투자를 획기적으로 방지하고 범정부적 정보 공동 활용을 통해 대국민 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 질을 향상시키며 정보화 예산 편성을 과학화한다.
> 3. **융합**: 비즈니스([BRM](/knowledge-base/studynote/12_it_management/03_ea_isp/117_brm_business_reference_model/)), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)([DRM](/knowledge-base/studynote/12_it_management/03_ea_isp/903_drm_data_reference_model_standard/)), [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)([SRM](/knowledge-base/studynote/12_it_management/03_ea_isp/118_srm_service_reference_model/)), 기술([TRM](/knowledge-base/studynote/12_it_management/03_ea_isp/120_trm_technical_reference_model/)), 성과([PRM](/knowledge-base/studynote/12_it_management/03_ea_isp/905_prm_performance_reference_model_it_roi/))의 5대 [참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/)을 기반으로 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)를 통합하여 예산 기획과 IT 구축을 융합하는 강력한 거버넌스 도구이다.

---

### Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

<strong>범정부 <a href="/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/">EA</a> 프레임워크(<a href="/knowledge-base/studynote/12_it_management/03_ea_isp/115_gea_government_ea_framework/">GEA</a>)</strong>는 국가 공공기관 전체의 정보화 아키텍처를 체계적으로 수립하고 관리하기 위해 행정안전부가 규정한 의무 지침이자 프레임워크이다. 과거 공공기관 정보화 사업은 각 부처가 독자적인 [사일로](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)([Silo](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)) 형태로 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/)하였다. 그 결과, 부처 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 연계가 불가능하여 국민이 동일한 서류를 여러 기관에 중복 제출해야 했고, 비슷한 성격의 시스템(예: 회계, 인사, 포털)이 기관마다 중복 구축되어 막대한 국가 예산이 낭비되는 치명적 한계에 봉착했다.

이를 타개하기 위해 미국 연방정부의 FEAF (Federal [Enterprise Architecture](/knowledge-base/studynote/12_it_management/01_governance_strategy/806_ea_enterprise_architecture/) Framework) 사상을 도입하여 한국형 프레임워크인 GEA가 탄생하였다. GEA의 가장 큰 철학은 '정부는 하나의 거대한 기업(Single Enterprise)'이라는 시각이다. 따라서 개별 부처는 독자적인 회사가 아니라 정부라는 큰 우산 아래의 하위 본부에 불과하며, 정보시스템 구축 시 반드시 국가가 정한 공통 표준과 [참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/)([Reference Model](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/))을 따라야 한다.

이 프레임워크는 단순한 기술적 가이드라인을 넘어선다. 현재 공공기관에서 새로운 IT 사업 예산을 타내려면, 먼저 범정부 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 메타시스템([EAMS](/knowledge-base/studynote/12_it_management/03_ea_isp/124_eams_ea_management_system/))에 접속하여 기존에 다른 기관이 만들어둔 유사 시스템이나 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 있는지 조회하고, 재사용이 불가능함을 증명해야만 예산 심의를 통과할 수 있는 강력한 컴플라이언스([Compliance](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/058_it_compliance_sox_basel_gdpr_isms/)) 도구로 작동한다.

```text
[공공기관 정보화 예산 낭비의 원인과 GEA 해결 구조]

(과거) 부처 파편화 및 중복 투자
[A부처] 민원처리 앱 신규 개발 (100억) --> 닫힌 데이터
[B부처] 유사한 민원 앱 또 개발 (100억) --> 예산 낭비, 상호운용 불가

       v GEA 도입 패러다임 전환 v

(현재) 범정부 참조모델 기반 통합 거버넌스
[정부 공통 참조 모델 (Reference Model)] <--- 재사용 및 표준 점검 의무화
       ^
       +- [A부처] 70% 공통 서비스 재사용 + 30% 커스텀 (30억)
       +- [B부처] 70% 공통 서비스 재사용 + 30% 커스텀 (30억)
       => 데이터 공동 활용, 총 예산 140억 절감 및 상호운용성(Interoperability) 달성
```
*해설: 이 개념도는 범정부 EA가 기술적 도구가 아니라 예산 최적화와 거버넌스 통제 수단임을 명확히 보여준다. 공공부문에서는 기술적 우수성보다 [상호운용성](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/287_interoperability_tactics/)과 재사용성을 통한 세금 낭비 방지가 최우선 가치이며, GEA는 이 통제를 시스템적으로 강제하는 게이트키퍼 역할을 한다.*

📢 **섹션 요약 비유**: GEA는 국가라는 거대한 도시의 '중앙 도시계획 위원회 규정'과 같습니다. 각 부처가 마음대로 배관 크기나 [전압](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/001_voltage/)을 다르게 집을 지으면 도시 전체가 마비되기 때문에, 중앙에서 정해준 규격([참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/)) 부품만 사용하도록 강제하여 어느 집이든 수도와 전기가 완벽히 호환되게 만드는 것입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

GEA의 핵심 구조는 방향성을 제시하는 <strong>프레임워크 가이드라인</strong>과, 실제 아키텍처를 구축할 때 템플릿과 기준이 되는 <strong>5대 범정부 <a href="/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/">참조 모델</a>(<a href="/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/">Reference Model</a>, <a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/197_rm_rate_monotonic_scheduling/">RM</a>)</strong>로 구성된다.

#### 범정부 5대 [참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/) ([Reference Model](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/))
[참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/)은 각 기관이 아키텍처를 정의할 때 사용할 수 있는 '공통 표준 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 체계'이다.
1. <strong><a href="/knowledge-base/studynote/12_it_management/03_ea_isp/117_brm_business_reference_model/">BRM</a> (Business <a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/197_rm_rate_monotonic_scheduling/">RM</a>, 업무 <a href="/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/">참조 모델</a>)</strong>: 정부의 모든 업무 기능을 기능별, 목적별로 계층화하여 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) (예: 복지, 국방, 행정지원).
2. <strong><a href="/knowledge-base/studynote/12_it_management/03_ea_isp/118_srm_service_reference_model/">SRM</a> (<a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">Service</a> <a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/197_rm_rate_monotonic_scheduling/">RM</a>, <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> <a href="/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/">참조 모델</a>)</strong>: IT 시스템이 제공하는 애플리케이션 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)를 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/). (예: 대국민 민원 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/), 공통 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)). 이를 통해 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) 단위의 재사용([Component](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) Reuse)을 극대화한다.
3. <strong><a href="/knowledge-base/studynote/12_it_management/03_ea_isp/903_drm_data_reference_model_standard/">DRM</a> (<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a> <a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/197_rm_rate_monotonic_scheduling/">RM</a>, <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> <a href="/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/">참조 모델</a>)</strong>: 범정부적으로 공동 활용해야 할 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/), [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 표준, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 교환 구조 정의.
4. <strong><a href="/knowledge-base/studynote/12_it_management/03_ea_isp/120_trm_technical_reference_model/">TRM</a> (Technical <a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/197_rm_rate_monotonic_scheduling/">RM</a>, 기술 <a href="/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/">참조 모델</a>)</strong>: 정보시스템 구축에 필요한 기술 요소(플랫폼, 네트워크, 보안 등)를 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하고, 각 영역별로 특정 벤더 기술이 아닌 개방형 표준(Open Standard) 프로파일을 지정.
5. <strong><a href="/knowledge-base/studynote/12_it_management/03_ea_isp/905_prm_performance_reference_model_it_roi/">PRM</a> (<a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">Performance</a> <a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/197_rm_rate_monotonic_scheduling/">RM</a>, 성과 <a href="/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/">참조 모델</a>)</strong>: 위 아키텍처들이 구축되었을 때 실제로 국가와 국민에게 어떤 성과(비용 절감, 만족도)를 냈는지 측정하는 평가 지표 프레임워크.

이 5가지 모델은 고립되어 작동하지 않으며, 투자(예산)부터 구축, 평가까지의 라이프사이클을 관통한다.

```text
+-------------------------------------------------------------+
|             [PRM] 성과 참조 모델 (투자 대비 효과 측정)      |
+-------------------------------------------------------------+
|                           ^ 측정                            |
| +------------------+    |       +------------------+    |
| | [BRM] 업무 참조 모델|<--- 지원 --->| [SRM] 서비스 참조모델|    |
| | (정부 기능 분류)  |            | (공통 컴포넌트/앱) |    |
| +------------------+            +------------------+    |
|           | 의존                            | 접근          |
|           v                                 v               |
| +------------------+            +------------------+    |
| | [DRM] 데이터 참조모델|            | [TRM] 기술 참조 모델|    |
| | (공동활용 DB 메타)  |            | (오픈스탠다드 인프라)|    |
| +------------------+            +------------------+    |
+-------------------------------------------------------------+
```
*해설: 이 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)도는 5대 [참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/)의 유기적 결합을 나타낸다. BRM이 목표를 제시하면 SRM이 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 구성하고 DRM이 혈액([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 공급하며 TRM이 뼈대(인프라)를 제공한다. 그리고 마지막으로 PRM이 전체 생태계의 건강 상태([ROI](/knowledge-base/studynote/12_it_management/01_governance_strategy/807_roi_return_on_investment/))를 진단한다. 실무적으로 정보화 사업 계획서([ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/885_isp_information_strategy_planning_4_steps/)) 작성 시, 이 5가지 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 코드를 사업 내역에 의무적으로 매핑해야 한다.*

📢 **섹션 요약 비유**: 5대 [참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/)([RM](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/197_rm_rate_monotonic_scheduling/))은 레고 블록의 '공식 [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/)'입니다. BRM은 설명서, SRM은 조립된 문/창문 파츠, DRM은 블록 색상표, TRM은 호환되는 바닥판 규격이며, 마지막 PRM은 완성된 성이 얼마나 멋진지 평가하는 채점표 역할을 하여 일관된 작품을 만들게 합니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

GEA는 민간 영역의 엔터프라이즈 아키텍처([TOGAF](/knowledge-base/studynote/12_it_management/03_ea_isp/113_togaf/) 등)와 근본적인 사상은 공유하지만, 그 목적과 통제 방식에서 확연한 차이를 보인다.

| 비교 기준 | 민간 기업 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) ([TOGAF](/knowledge-base/studynote/12_it_management/03_ea_isp/113_togaf/) 기반 등) | 범정부 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) ([GEA](/knowledge-base/studynote/12_it_management/03_ea_isp/115_gea_government_ea_framework/) / FEAF) |
|:---|:---|:---|
| **최우선 목적** | 시장 경쟁력 확보, 민첩성, 이윤 극대화 ([ROI](/knowledge-base/studynote/12_it_management/01_governance_strategy/807_roi_return_on_investment/)) | 예산 중복 방지, 대국민 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [상호운용성](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/287_interoperability_tactics/) 확보 |
| **통제 수준** | 유연함. 필요에 따라 프레임워크 테일러링(변형) | 매우 강력함. 법제화(ITA법)를 통한 의무화 및 강제 통제 |
| **핵심 산출물** | 비즈니스 모델 캔버스, 아키텍처 이행 계획서 | 5대 [참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/)([PRM](/knowledge-base/studynote/12_it_management/03_ea_isp/905_prm_performance_reference_model_it_roi/), [BRM](/knowledge-base/studynote/12_it_management/03_ea_isp/117_brm_business_reference_model/), [SRM](/knowledge-base/studynote/12_it_management/03_ea_isp/118_srm_service_reference_model/), [DRM](/knowledge-base/studynote/12_it_management/03_ea_isp/903_drm_data_reference_model_standard/), [TRM](/knowledge-base/studynote/12_it_management/03_ea_isp/120_trm_technical_reference_model/)) 매핑서 |
| **거버넌스 연계** | 사내 ARB (아키텍처 리뷰 보드) 심의 | 기획재정부/행정안전부 정보화 예산 편성 직접 연계 |

**핵심 융합 관점: 예산(Budget)과 아키텍처의 결합**
GEA의 가장 독특한 시너지는 IT 아키텍처가 재무/예산 통제와 완벽히 융합되어 있다는 점이다. 정부 부처가 정보화 사업 예산을 요구하면, 예산 부처(기재부)는 [GEA](/knowledge-base/studynote/12_it_management/03_ea_isp/115_gea_government_ea_framework/) 리포지토리를 조회하여 "요청한 시스템의 [BRM](/knowledge-base/studynote/12_it_management/03_ea_isp/117_brm_business_reference_model/)/SRM이 타 부처에 이미 존재하는지" 검사한다. 중복도가 50%를 넘어가면 예산은 삭감되고, 기존 공통 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(행망, 공용 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 등)를 의무적으로 연계 API로 호출하도록 지시받는다. 이는 아키텍처가 단순한 기술 도면이 아니라 강력한 행정 권력임을 시사한다.

```text
[범정부 EA 거버넌스와 예산 심의 프로세스의 융합]

[각 부처 정보화 기획] --- (사업 계획서 + GEA 참조모델 맵핑) --+
                                                            |
                                                            v
[EA 포털(EAMS) 자동 검증] <--- [데이터/서비스 중복 여부 스캐닝]
         | (중복 발생)
         +--> [반려 및 재사용 지시] "행안부 공통 인프라(TRM) 사용 조건부 승인"
         |
         v (중복 없음, 표준 부합)
[행안부 사전 협의 통과] ---> [기재부 예산 배정] ---> [시스템 구축 및 성과(PRM) 측정]
```
*해설: 이 흐름은 공공 프로젝트에서 아키텍처가 예산을 배정받기 위한 '의무 관문(Gate)'으로 작동함을 보여준다. 민간은 중복투자를 하더라도 런칭 속도가 중요하면 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/)하지만, 공공은 민첩성보다 혈세 낭비 방지와 [벤더 종속](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/)([Lock-in](/knowledge-base/studynote/12_it_management/05_security_compliance/362_lock_in_portability/)) 회피를 위해 개방형 표준([TRM](/knowledge-base/studynote/12_it_management/03_ea_isp/120_trm_technical_reference_model/)) 준수를 최우선으로 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한다.*

📢 **섹션 요약 비유**: 민간 EA가 기업이 이윤을 내기 위한 '스피드 보트 튜닝 설명서'라면, 범정부 EA는 수백 대의 배가 부딪치지 않고 항해하기 위한 '국가 해상 교통 관제 시스템 및 선박 표준 규격법'입니다. 여기서는 속도보다 규정 준수와 충돌 방지가 우선입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

공공 정보화 사업을 수주하거나 컨설팅하는 IT 전문가(감리, 아키텍트)에게 GEA의 이해는 프로젝트 성공의 당락을 가르는 절대적 요소이다.

1. <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/287_interoperability_tactics/">상호운용성</a>(<a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/084_blockchain_interoperability_polkadot_cosmos/">Interoperability</a>) 확보 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>: 공공 시스템은 타 기관과의 연계를 기본으로 설계해야 한다. 자체적인 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 시스템을 구축하는 것은 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)이며, 범정부 공동 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)([SRM](/knowledge-base/studynote/12_it_management/03_ea_isp/118_srm_service_reference_model/))과 행정망([TRM](/knowledge-base/studynote/12_it_management/03_ea_isp/120_trm_technical_reference_model/))을 활용하는 아키텍처를 제안해야 심의를 통과할 수 있다.
2. **형식적 매핑의 늪(Paperwork Overhead) 주의**: 실무에서 가장 큰 병목은 5대 [참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/) 매핑을 실제 시스템 구조에 맞게 설계하는 것이 아니라, 단순히 예산을 따내기 위해 끼워 맞추기식(Paperwork) 문서 작성을 하는 것이다. 이 경우 구축 후 시스템 구조와 [EAMS](/knowledge-base/studynote/12_it_management/03_ea_isp/124_eams_ea_management_system/) 시스템의 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)가 불일치하여, 다음 해 예산 평가([PRM](/knowledge-base/studynote/12_it_management/03_ea_isp/905_prm_performance_reference_model_it_roi/))에서 치명적인 페널티를 받게 된다.
3. <strong><a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/">클라우드 네이티브</a>와 GEA의 충돌 해결</strong>: 과거 GEA의 TRM은 물리적 서버와 [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) SW [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)을 중심으로 구성되었다. 하지만 최근 민간 클라우드(공공 클라우드 존) 도입이 강제되면서, 기술사는 구형 [TRM](/knowledge-base/studynote/12_it_management/03_ea_isp/120_trm_technical_reference_model/) 규격에 얽매이지 않고 DaaS(Desktop [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)), [SaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/951_saas/) 중심의 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) [참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/) 확장 지침을 선제적으로 해석하여 아키텍처에 반영해야 한다.

```text
[실무 의사결정 트리: 공공 정보화 사업 EA 검토 플로우]

[신규 공공 정보시스템 제안/설계]
         |
         v
[TRM 점검] 제안된 기술 스택이 특정 외산 벤더(Vendor Lock-in)에 종속되는가?
   +- (Yes) ---> 오픈소스 기반/범정부 표준 프레임워크(eGovFrame)로 스택 전면 교체
   |
   +- (No) ----> [SRM/DRM 점검] 민원인 데이터를 자체 수집하는가? (Data 사일로)
                  +- (Yes) --> 행정정보 공동이용센터 연계 API 호출망으로 설계 변경
                  |
                  +- (No) ---> [PRM 매핑] 최종 구축 시 예상되는 정량적 성과 지표 확립
                                +--> 범정부 EA 포털 등록 및 정보화 사업 승인
```
*해설: 이 [의사결정 트리](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/124_decision_tree/)는 공공 정보화 컨설턴트나 감리원이 설계도를 검열하는 핵심 기준이다. 특정 상용 DB를 고집하거나([TRM](/knowledge-base/studynote/12_it_management/03_ea_isp/120_trm_technical_reference_model/) 위반), 타 부처의 주민 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 중복으로 받아 저장하려 할 때([DRM](/knowledge-base/studynote/12_it_management/03_ea_isp/903_drm_data_reference_model_standard/) 위반) 즉시 아키텍처를 재설계하도록 통제해야 한다. 이것이 실무에서의 진정한 아키텍처 거버넌스이다.*

📢 **섹션 요약 비유**: 공공 프로젝트에서 GEA를 무시하고 시스템을 짜는 것은, 국가 고속도로를 설계하면서 일반 자동차 타이어와 호환되지 않는 특수 철로를 까는 것과 같습니다. 무조건 국가가 정한 바퀴 규격([TRM](/knowledge-base/studynote/12_it_management/03_ea_isp/120_trm_technical_reference_model/))과 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)등 체계([SRM](/knowledge-base/studynote/12_it_management/03_ea_isp/118_srm_service_reference_model/))를 따라야만 도로 공사 허가가 나옵니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

범정부 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 프레임워크는 한국의 전자정부(e-Government) 수준을 세계 최고 반열에 올린 숨은 공신이자 핵심 인프라이다.

| 지표 | 정량적 / 정성적 기대효과 | 비고 |
|:---|:---|:---|
| **비용 절감** | 부처 간 중복 시스템 통합 및 인프라 공동 활용으로 예산 대폭 절감 | 국가 클라우드 전환 가속화 |
| **행정 효율성** | 행정정보 공동 활용([DRM](/knowledge-base/studynote/12_it_management/03_ea_isp/903_drm_data_reference_model_standard/))을 통한 민원인의 무서류(Paperless) 원스톱 행정 구현 | 대국민 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 체감도 상승 |
| **IT 생태계** | 전자정부 표준 프레임워크(eGovFrame) 적용을 통한 중소 SW 기업의 진입 장벽 완화 | 특정 대기업 [벤더 종속](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/)성 타파 |

미래의 GEA는 정적이고 관료적인 [메타데이터 관리 시스템](/knowledge-base/studynote/05_database/02_modeling_normalization/125_metadata_management_system_mms/)에서 벗어나, '[데이터 패브릭](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/)([Data Fabric](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/))'과 [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 중심의 '디지털플랫폼정부(DPG) 아키텍처'로 진화하고 있다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 부처 간 물리적 장벽을 넘어 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적으로 하나로 연결되고, [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반의 성과 분석([PRM](/knowledge-base/studynote/12_it_management/03_ea_isp/905_prm_performance_reference_model_it_roi/))이 실시간으로 이루어지는 지능형 범정부 EA로의 발전이 핵심 방향이다.

📢 **섹션 요약 비유**: GEA는 흩어져 있던 정부 부처라는 섬들을 하나로 연결한 튼튼한 대교(大橋)입니다. 이 다리 덕분에 국민이라는 자동차는 병목없이 통합된 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 누릴 수 있고, 국가는 중복된 나룻배를 운영할 세금을 절약하여 더 나은 미래를 투자할 수 있게 되었습니다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
* <strong>FEAF (Federal <a href="/knowledge-base/studynote/12_it_management/01_governance_strategy/806_ea_enterprise_architecture/">Enterprise Architecture</a> Framework)</strong> | 미국 연방 정부가 개발한 공공 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 프레임워크로, 한국의 [GEA](/knowledge-base/studynote/12_it_management/03_ea_isp/115_gea_government_ea_framework/) 수립에 결정적 사상(5대 [참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/))을 제공한 모태
* **eGovFrame (전자정부 표준 프레임워크)** | GEA의 [TRM](/knowledge-base/studynote/12_it_management/03_ea_isp/120_trm_technical_reference_model/)/[SRM](/knowledge-base/studynote/12_it_management/03_ea_isp/118_srm_service_reference_model/) 원칙을 준수하여 공공사업에 스프링(Spring) 프레임워크 기반의 공통 개발 기반을 제공하는 기술 표준
* <strong><a href="/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/015_ita_information_technology_architecture/">ITA</a> 법 (정보기술아키텍처 도입 의무화법)</strong> | 공공기관이 의무적으로 EA를 도입하고 정보화 예산 평가 시 이를 증빙하도록 강제한 법적 근거
* <strong><a href="/knowledge-base/studynote/12_it_management/03_ea_isp/124_eams_ea_management_system/">EAMS</a> (범정부 <a href="/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/">EA</a> 포털)</strong> | 전 부처의 아키텍처 [참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/)과 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)가 등록, 통제, 공유되는 국가 통합 정보시스템
* <strong><a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/084_blockchain_interoperability_polkadot_cosmos/">Interoperability</a> (<a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/287_interoperability_tactics/">상호운용성</a>)</strong> | GEA가 추구하는 최상위 가치로, 서로 다른 기관의 시스템이나 이기종 기술 간에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 완벽히 교환하고 활용하는 능력


### 📈 관련 키워드 및 발전 흐름도

```text
[EA (Enterprise Architecture) — 비즈니스·IT 정렬 체계적 설계 방법론]
    |
    v
[GEA (Government EA Framework) — 범정부 공통 아키텍처·표준 참조 모델]
    |
    v
[TOGAF (The Open Group Architecture Framework) — 글로벌 EA 방법론 표준]
    |
    v
[디지털 정부 플랫폼 — GEA 기반 공공 서비스 표준화·재사용 실현]
    |
    v
[클라우드 퍼스트 (Cloud-First) 정책 — EA와 클라우드 전환 로드맵 통합]
```

이 흐름은 기업 아키텍처 방법론([EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/))이 공공 부문에 특화된 GEA로 발전하고, [TOGAF](/knowledge-base/studynote/12_it_management/03_ea_isp/113_togaf/) 표준과 융합하여 디지털 정부 플랫폼 구축과 클라우드 전환 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)의 기반으로 자리잡는 과정을 보여준다.


### 👶 어린이를 위한 3줄 비유 설명
1. 우리나라에는 경찰청, 소방청, 교육부 같은 여러 관공서가 있어요. 옛날에는 각자 자기들만의 방식대로 컴퓨터를 만들어서 서로 대화가 안 통했어요.
2. 그래서 나라에서 "이제부터 컴퓨터 시스템을 만들 때는 무조건 이 5가지 똑같은 규격과 레고 블록만 써라!" 하고 규칙을 정했는데, 이게 바로 범정부 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/)([GEA](/knowledge-base/studynote/12_it_management/03_ea_isp/115_gea_government_ea_framework/))예요.
3. 이 규칙 덕분에 관공서끼리 서로 정보를 쉽게 주고받을 수 있게 되어서, 우리가 서류를 한 번만 내도 모든 일이 척척 처리되는 마법 같은 전자정부가 만들어진 거랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 14 / 482

<- **이전**: [13. TOGAF (The Open Group Architecture Framework) - ADM(Architecture Development](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/013_togaf_framework/)
**다음**: [15. ITA (Information Technology Architecture) - 과거 EA와 동의어로 쓰이던 용어 (법제화 명칭)](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/015_ita_information_technology_architecture/) ->

---
