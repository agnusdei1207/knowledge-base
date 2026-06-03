+++
title = "788. 헥사고날 아키텍처 어댑터 포트 매핑 구조"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [헥사고날 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/) [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 매핑 구조은(는) [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

소프트웨어 개발 초창기의 3계층(N-Tier) 아키텍처는 보통 `Web(UI) ➔ Service(로직) ➔ Repository(DB)` 순서로 코드를 짰다. 이 구조는 치명적인 약점이 있었다. 가장 중요한 비즈니스 로직([Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))이 가장 안 중요한 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)(Repository)의 구조에 완벽하게 종속([Coupling](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/))된다는 점이다.

"DB 쿼리가 편하니까 로직도 이렇게 짜자"라며 DB 주도 설계가 만연해졌고, 나중에 프레임워크나 DB를 바꾸려 하면 시스템 전체를 새로 짜야 했다.

이 비극을 끊어내기 위해 알리스테어 코크번(Alistair Cockburn)이 2005년에 제안한 것이 <strong><a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">포트</a> 앤 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/">어댑터</a>(Ports and Adapters) 아키텍처</strong>다. 그는 외부와 내부를 완벽히 분리하는 모양을 '육각형(Hexagon)'으로 그렸고, 이 때문에 <strong><a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/">헥사고날 아키텍처</a></strong>라는 이름으로 더 유명해졌다.

- **📢 섹션 요약 비유**: 옛날엔 노트북(로직)에 마우스(입력기기) 선이 아예 납땜으로 붙어있어서 마우스가 고장 나면 노트북을 버려야 했다. [헥사고날 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/)는 노트북에 [USB](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/359_usb/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)([Port](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/))를 만들어 둔 것이다. 마우스든 키보드든 조이패드든 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)만 맞으면 노트북을 뜯지 않고 마음대로 갈아 끼울 수 있다.

---

다음은 [헥사고날 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/) [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 매핑 의 핵심 구조와 흐름을 보여주는 다이어그램이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">헥사고날 아키텍처 어댑터 포트 매핑</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">입력/요구사항</div><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">핵심 처리 과정</div><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">출력/결과물</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">요구 분석 설계·적용 품질 검증</div></div>
</div>
</div>



이 다이어그램은 [헥사고날 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/) [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 매핑 가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 검증된 결과물을 산출하는 흐름을 보여준다.

---

---

---

## Ⅱ. 아키텍처 및 핵심 원리

[헥사고날 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/)는 크게 <strong><a href="/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a>(내부)</strong>과 <strong><a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">포트</a>(경계)</strong>, <strong><a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/">어댑터</a>(외부)</strong> 세 가지로 이루어진다.

- **📢 섹션 요약 비유**: [헥사고날 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/) [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 매핑 구조은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

| 항목 | 설명 | 비고 |
| :--- | :--- | :--- |
| 핵심 특성 | [헥사고날 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/) [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 매핑 구조의 핵심 특성과 동작 방식 | 필수 이해 요소 |
| 적용 범위 | 어떤 프로젝트·상황에서 활용하는지 | 선택 기준 |
| 제약 조건 | 적용 시 주의해야 할 전제·한계 | 트레이드오프 |

---

---

---

## Ⅲ. 비교 및 연결

[도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)을 중심에 둔 아키텍처 3대장은 이름만 다를 뿐 뿌리는 하나다.

| 비교 항목 | 헥사고날 (Ports & Adapters) | 어니언 (Onion) 아키텍처 | 클린 (Clean) 아키텍처 |
|:---|:---|:---|:---|
| **제안자 (연도)** | 알리스테어 코크번 (2005) | 제프리 팔레르모 (2008) | 로버트 C. 마틴 (2012) |
| **주요 강조점** | <strong><a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/">포트</a>와 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/">어댑터</a></strong>를 통한 외부와의 통신 규격 분리 | 내부 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)을 서비스와 엔티티 계층으로 **더 잘게 쪼갬** | 앞선 사상을 모두 묶고, **유스케이스(UseCase)** 개념 대중화 |
| **의존성 방향** | 바깥 ➔ 안쪽 ([DIP](/knowledge-base/studynote/04_software_engineering/04_testing_quality/247_dip_dependency_inversion_principle/)) | 껍질 바깥 ➔ 중심 코어 | 바깥 ➔ 안쪽 ([DIP](/knowledge-base/studynote/04_software_engineering/04_testing_quality/247_dip_dependency_inversion_principle/)) |
| **핵심 철학** | **"DB와 UI는 세부 사항(Detail)일 뿐이다."** | **동일함** | **동일함** |

업계에서는 이 세 가지를 엄격하게 구분하기보다, "[포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)와 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) 개념을 가져다 쓴 [클린 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/217_clean_architecture_dependency_rule/)"라는 식으로 혼용해서 부르는 경우가 많다.

- **📢 섹션 요약 비유**: 헥사고날이 "멀티탭([포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/))에 플러그([어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/))를 꽂자!"라고 인터페이스 규격을 강조한 것이라면, 어니언 아키텍처는 "집 안의 거실과 안방([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 내부)도 겹겹이 분리하자"는 것이고, [클린 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/217_clean_architecture_dependency_rule/)는 이 두 가지를 합쳐 "가장 완벽한 인테리어 가이드북"을 써낸 것이다.

---

---

---

---

## Ⅳ. 실무 적용 및 기술사 판단

[헥사고날 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/)를 도입할 때 겪는 가장 큰 고통은 <strong>'<a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/">어댑터</a> 간의 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 맵핑(<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/010_schema_mapping/">Mapping</a>) 오버헤드'</strong>다.

- **📢 섹션 요약 비유**: [헥사고날 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/) [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 매핑 구조은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

---

---

---

## Ⅴ. 기대효과 및 결론

[헥사고날 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/)를 시스템의 코어 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)에 이식하면, 비즈니스 로직은 외부 기술의 유행([Oracle](/knowledge-base/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/) $\rightarrow$ [MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/), [REST](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/) $\rightarrow$ [gRPC](/knowledge-base/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/))으로부터 완벽하게 격리되어 <strong>소프트웨어의 수명(Longevity)</strong>이 비약적으로 늘어난다.

결론적으로 기술 리더는 "[데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/)부터 만들고 코딩을 시작하자"는 낡은 사고방식을 버려야 한다. [헥사고날 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/)는 <strong>"DB나 웹 화면이 아직 안 만들어졌어도, 우리는 가장 중요한 심장(<a href="/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 로직)부터 완벽하게 코딩하고 테스트할 수 있다"</strong>는 선언이다. 외부의 껍데기([어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/))는 가장 마지막에 결정해서 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)에 꽂아버리면 그만이기 때문이다.

- **📢 섹션 요약 비유**: 자동차의 진짜 심장은 엔진([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 로직)이다. 헥사고날 설계는 엔진을 먼저 완벽하게 만들어 테스트해 보고, 나중에 그 엔진에 스포츠카 껍데기(웹 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/))를 씌울지, 트럭 껍데기(모바일 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/))를 씌울지 나중에 결정해도 아무런 문제가 없는 완벽한 모듈화 기술이다.

---

---

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) ([Software Engineering](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)) | [헥사고날 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/) [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 매핑 구조의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [소프트웨어 생명주기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/003_sdlc/) ([SDLC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/), Software Development Life Cycle) | [헥사고날 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/) [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 매핑 구조은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | [헥사고날 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/) [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 매핑 구조 적용 결과는 QA 활동을 통해 검증되고 측정된다 |
| [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) ([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)) | [헥사고날 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/) [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 매핑 구조에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">소프트웨어 위기 (Software Crisis) 인식</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">헥사고날 아키텍처 어댑터 포트 매핑 구조 개념 정립</div>
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

1. [헥사고날 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/) [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 매핑 구조은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 961 / 973

← **이전**: [787. 애그리게이트 루트 외부 접근 단일 진입점 설계](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/787_aggregate_root_single_entry_point/)
**다음**: [789. 클린 아키텍처 엔티티 유스케이스 프레젠테이션 계층 분리](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/789_clean_architecture_entity_usecase/) →

---
