+++
title = "117. BRM (Business Reference Model, 업무 참조 모델)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: BRM (Business [Reference Model](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/), 업무 [참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/))의 본질은 기관의 업무 기능을 중복 없이 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)를 현재 구조와 목표 구조 사이의 전환 논리로 구체화하는 데 있다.
> 2. **가치**: 현행 구조, 목표 구조, 전환 과제의 추적성이 확보되어야 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 문서가 실제 투자와 아키텍처 변화로 이어진다.
> 3. **판단 포인트**: BRM (Business [Reference Model](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/), 업무 [참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/))은 도입 자체보다 범위, 책임, 측정 기준을 어떻게 연결하느냐에 따라 성과가 달라진다.

---

## Ⅰ. 개요 및 필요성

BRM (Business [Reference Model](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/), 업무 [참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/))은 조직이 당면한 요구를 반복 가능하고 설명 가능한 운영 체계로 바꾸기 위해 사용하는 핵심 관리 개념이다. 실무 초점은 기관의 업무 기능을 중복 없이 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)에 놓이며, 핵심은 업무 기능을 공통 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 체계로 정리해야 전사 아키텍처와 투자 의사결정이 같은 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) 위에서 움직일 수 있다는 점이다.

이 개념이 중요한 이유는 기관과 기업이 비슷한 업무를 서로 다른 이름으로 관리하면 중복 시스템과 중복 예산이 계속 생기기 때문이다. BRM은 업무 기능을 표준 계층으로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)해 어떤 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 어떤 업무를 지원하는지 연결하므로, 정보화 과제 발굴과 [참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/) 설계의 기준점이 된다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Business need ──▶ Function classify ──▶ EA linkage</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">duplicated work standard taxonomy investment</div></div>
</div>
</div>



이 그림은 BRM이 업무 요구를 기능 체계로 정리한 뒤 EA와 정보화 과제로 연결하는 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 구조임을 보여 준다.

- **📢 섹션 요약 비유**: 도서관 책을 주제별 서가에 정리해야 찾기 쉬워지듯, 업무도 같은 기준으로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)해야 정보화가 체계적으로 움직인다.

---

## Ⅱ. 아키텍처 및 핵심 원리

BRM (Business [Reference Model](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/), 업무 [참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/))이 제대로 작동하려면 업무 기능 계층, [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 기준, 연관 시스템, 관리 책임이 함께 정의되어야 한다. [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 체계만 있고 현행 시스템과 연결되지 않으면 [참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/)이 장식이 되고, 반대로 시스템 목록만 있으면 전사 관점의 중복 제거가 어렵다.

| 구성 축 | 설명 | 판단 포인트 |
|:---|:---|:---|
| 기능 계층 | 업무를 상위·중위·하위 기능으로 구조화해 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)을 세운다. | [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 단위가 너무 크거나 작으면 활용도가 떨어진다. |
| 기능 정의 | 기능 명칭과 범위를 표준화해 조직 간 비교 가능성을 높인다. | 같은 업무를 다른 이름으로 관리하지 않도록 해야 한다. |
| 조직 매핑 | 기능별 중복과 누락을 식별해 투자 우선순위를 재정렬한다. | [참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/)은 진단과 개선의 출발점이어야 한다. |
| 사업 매핑 | [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/), [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), 시스템 포트폴리오와 연결해 실행력을 높인다. | [참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/)과 실제 사업이 끊기지 않아야 한다. |



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Function map ──▶ Reference model ──▶ Portfolio linkage</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">classify standardize govern</div></div>
</div>
</div>



핵심 원리는 동일한 업무를 동일한 언어로 정의하는 데 있다. 그래야 기관 간 비교, 시스템 재사용, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 통합, 정보화 투자 심의가 같은 기준에서 이루어진다.

- **📢 섹션 요약 비유**: 청사진, 자재 목록, 공정 순서가 연결돼야 건물이 계획대로 올라가듯 업무 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)와 사업 연결이 함께 가야 한다.

---

## Ⅲ. 비교 및 연결

BRM (Business [Reference Model](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/), 업무 [참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/))은 인접한 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) [참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/)과 함께 볼 때 의미가 더 분명해진다. BRM이 업무 기능을 정의하면, DRM과 [SRM](/knowledge-base/studynote/12_it_management/03_ea_isp/118_srm_service_reference_model/), TRM은 각각 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)·기술 관점의 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)을 보완한다.

| 비교 대상 | 차이점 | 연결 포인트 |
|:---|:---|:---|
| [DRM](/knowledge-base/studynote/12_it_management/03_ea_isp/119_drm_data_reference_model_standard/) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)와 교환 기준에 초점 | BRM은 어떤 업무가 어떤 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 쓰는지 연결 |
| [SRM](/knowledge-base/studynote/12_it_management/03_ea_isp/118_srm_service_reference_model/) | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와 애플리케이션 기능 표준화 | BRM은 업무 기능 관점에서 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 필요성을 설명 |
| [TRM](/knowledge-base/studynote/12_it_management/03_ea_isp/120_trm_technical_reference_model/) | 기술 인프라와 표준 규격을 다룸 | BRM은 기술 선택의 업무 근거를 제공 |

실무에서는 BRM을 단독 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)표로 두기보다, [ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/101_isp_information_strategy_planning_4_steps/)·[EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/)·포트폴리오 관리의 상위 기준으로 사용해야 효과가 크다.

- **📢 섹션 요약 비유**: 지도와 나침반, 여행 일정표를 함께 보는 장거리 여행 준비와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 BRM (Business [Reference Model](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/), 업무 [참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/))을 적용할 때는 기능 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)의 일관성과 활용 목적을 먼저 정해야 한다. 공공기관에서는 기관별 업무를 [참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/)과 매핑해 중복 투자 방지와 범정부 표준화를 추진하고, 민간에서는 업무 포트폴리오 정리와 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 정합성 점검에 활용할 수 있다.

### 실무 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 업무 기능 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 기준이 조직 개편 이후에도 유지될 수 있을 만큼 안정적인가?
2. 기능 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)와 시스템·[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 매핑이 실제로 관리되는가?
3. 중복 투자나 누락 기능을 식별해 예산·로드맵에 반영하는가?
4. [참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/)이 [현행화](/knowledge-base/studynote/12_it_management/03_ea_isp/125_asis_update_ea_maintenance_synchronization/)되어 다음 [ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/101_isp_information_strategy_planning_4_steps/)·[EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 과제로 이어지는가?

### 자주 발생하는 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)표만 만들고 실제 시스템·예산 심의에 쓰지 않는 경우
- 조직도 기준으로만 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)해 기관 간 비교가 어려운 경우
- [현행화](/knowledge-base/studynote/12_it_management/03_ea_isp/125_asis_update_ea_maintenance_synchronization/) 없이 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 수립 문서로만 남겨 두는 경우

- **📢 섹션 요약 비유**: 지도 없이 길을 떠나지 않듯, 실무에서도 업무 기능 지도를 먼저 맞춰야 정보화 길이 보인다.

---

## Ⅴ. 기대효과 및 결론

BRM (Business [Reference Model](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/), 업무 [참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/))이 정착되면 조직은 업무 기능 기준으로 투자와 아키텍처를 설명할 수 있게 된다. 그 결과 중복 시스템이 줄고, 업무-[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)-기술의 추적성이 확보되며, 후속 ISP나 [ISMP](/knowledge-base/studynote/12_it_management/03_ea_isp/109_ismp_rfp_fp/) 수립도 더 정교해진다.

다만 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 체계가 현행 업무 변화를 따라가지 못하면 형식적 문서가 될 수 있다. 따라서 BRM은 한 번 만드는 표가 아니라, 지속적으로 [현행화](/knowledge-base/studynote/12_it_management/03_ea_isp/125_asis_update_ea_maintenance_synchronization/)되고 다른 [참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/)과 연동되는 살아 있는 기준으로 운영해야 한다.

- **📢 섹션 요약 비유**: 좋은 아키텍처 문서는 장식용 포스터가 아니라 실제 공사 순서를 정하는 설계도와 같다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| 업무 기능 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 전사 업무를 공통 기준으로 구조화 |
| [참조 모델](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model/) | 업무와 시스템을 연결하는 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) |
| 포트폴리오 관리 | 중복 투자와 우선순위를 재조정 |
| [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 연계 | 후속 아키텍처·정보화 과제와 연결 |

### 📈 관련 키워드 및 발전 흐름도


<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">업무 요구 정리</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">BRM (Business Reference Model)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">업무 기능 분류</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">EA 연계</div></div>
</div>
</div>



이 흐름은 업무 요구를 BRM으로 표준화하고, 이후 업무 기능 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)와 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) 연계 같은 확장 축으로 고도화하는 전개를 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명
1. BRM은 학교 물건을 교과목별 서랍에 나눠 넣는 정리표예요.
2. 같은 물건을 여러 서랍에 중복으로 넣지 않게 막아 줘요.
3. 그래서 필요한 걸 더 빨리 찾고, 새 물건도 뭘 사야 할지 쉽게 정할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 217 / 587

← **이전**: [116. 참조 모델 (Reference Model)](/knowledge-base/studynote/12_it_management/03_ea_isp/116_reference_model_brm_drm_srm_trm/)
**다음**: [117. BRM (Business Reference Model, 업무 참조 모델)](/knowledge-base/studynote/12_it_management/03_ea_isp/117_brm_business_reference_model_function/) →

---
