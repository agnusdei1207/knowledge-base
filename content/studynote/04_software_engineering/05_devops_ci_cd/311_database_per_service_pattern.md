+++
title = "311. 데이터베이스 퍼 서비스 (Database per Service) 패턴"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 퍼 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) ([Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) per [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 패턴은(는) [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

- **개념**: MSA로 서버를 10개로 쪼갰다면, DB도 10개로 쪼개야 한다는 원칙이다. '주문 DB'는 주문 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)만 접근할 수 있고, '결제 서버'가 주문 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 필요하면 DB 쿼리를 직접 때리는 게 아니라, 주문 서버의 API를 정중하게 호출해서 가져가야 한다.

- **필요성**: 개발자들이 서버 코드를 30개의 마이크로서비스로 쪼갰다([API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 분리). 그런데 DB는 여전히 거대한 오라클([Oracle](/knowledge-base/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/)) 1대만 쓰고 있다(공유 DB). 결제팀이 성능을 높이겠다고 `ORDERS` 테이블의 `status` 칼럼 이름을 `pay_status`로 바꿨다. 그 순간, 배송팀, 장바구니팀, 고객센터팀 서버가 이 테이블을 공유하고 있었기 때문에 일제히 `Column Not Found` 에러를 뿜으며 전사 쇼핑몰이 마비되었다. <strong>코드를 분리해 봐야 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 공유하면 100% 강결합(<a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/">Coupling</a>) 상태다.</strong> 이를 '[분산 모놀리스](/knowledge-base/studynote/04_software_engineering/11_testing_validation/537_distributed_monolith_antipattern/)([Distributed Monolith](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/537_anti_pattern_distributed_monolith/))'라는 최악의 안티패턴이라 부르며, 이를 박살 내기 위해 1서비스 1DB 철학이 필요했다.

- **💡 비유**: 한 지붕 아래 사는 대가족(공유 DB)에서, 누군가 말도 없이 화장실 구조를 바꾸면 온 가족이 화장실을 못 쓰게 됩니다. 그래서 가족들이 10채의 독립된 원룸([Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) per [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))으로 독립했습니다. 이제 각자 자기 집 화장실을 분홍색으로 칠하든 부수든 마음대로 할 수 있습니다. 다른 형제 집에 볼일이 있으면 마음대로 문을 열고 들어가는 게 아니라 초인종([API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/))을 누르고 부탁해야 합니다.

- **등장 배경 및 발전 과정**:
  1. <strong>모놀리식 공유 DB (Shared <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/">Database</a>)</strong>: 모든 부서가 하나의 RDBMS를 공유했다. [DBA](/knowledge-base/studynote/05_database/01_db_architecture_relational/025_dba_database_administrator/)([데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 관리자) 한 명이 모든 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 변경을 통제하며 비즈니스 속도를 늦추는 병목이 되었다.
  2. **MSA의 대두 (Conway's Law)**: 팀을 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 단위로 찢으면서 "남의 팀 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 남이 알아서 관리해라"라는 조직 분리 철학이 대두되었다.
  3. <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 중심에서 <a href="/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 중심(<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/310_architecture/">DDD</a>)으로의 전환</strong>: [Bounded Context](/knowledge-base/studynote/04_software_engineering/04_testing_quality/221_bounded_context_ddd_msa_boundary/)(제한된 문맥) 내에서 완벽한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 주도권(Ownership)을 갖기 위한 필연적 산물로 [Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) per [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 패턴이 정립되었다.

- **📢 섹션 요약 비유**: 이 패턴은 "내 돈은 내 지갑에, 네 돈은 네 지갑에"라는 철저한 재산 분할입니다. 지갑을 합쳐서 쓰면 편하긴 하지만([Join](/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/) 등), 나중에 네가 돈을 훔쳐갔네 내가 더 많이 썼네 하며 반드시 가족 간에 피 터지는 싸움([스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 충돌)이 벌어집니다.

---

다음은 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 퍼 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) (Databa의 핵심 구조와 흐름을 보여주는 다이어그램이다.

```text
+-------------------------------------------------------------+
|                  데이터베이스 퍼 서비스 (Databa                        |
+-------------------------------------------------------------+
|                                                             |
|  [입력/요구사항] ---> [핵심 처리 과정] ---> [출력/결과물]  |
|       |                    |                    |          |
|       v                    v                    v          |
|   요구 분석           설계·적용           품질 검증        |
|                                                             |
+-------------------------------------------------------------+
```

이 다이어그램은 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 퍼 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) (Databa가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 검증된 결과물을 산출하는 흐름을 보여준다.

---

---

---

## Ⅱ. 아키텍처 및 핵심 원리

[데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 퍼 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) ([Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) per [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 패턴의 핵심 원리와 구성 요소를 이해하기 위해 다음 구조를 살펴본다.

| 구성 요소 | 역할 | 적용 기준 |
| :--- | :--- | :--- |
| 개념 정의 | 핵심 용어와 범위를 명확히 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) | 용어 혼용·오해 방지 |
| 원칙 및 규칙 | 적용 시 따라야 할 기본 방향 | [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)·품질 기준 |
| 기법 및 도구 | 실질적 구현 방법과 지원 도구 | 생산성·자동화 |
| 측정 지표 | 결과물의 품질을 정량화하는 지표 | 의사결정 근거 |

[데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 퍼 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) ([Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) per [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 패턴의 핵심 원리는 **복잡성 분해**, **역할 분리**, <strong>품질 측정</strong>의 세 축으로 이해할 수 있다. 복잡한 문제를 관리 가능한 단위로 나누고, 각 역할의 책임을 명확히 하며, 결과를 정량적 지표로 평가하는 과정이 반복된다.

- **📢 섹션 요약 비유**: [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 퍼 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) ([Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) per [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 패턴의 아키텍처는 공장의 생산 라인과 같다. 각 공정(구성 요소)이 명확한 역할을 가지고 정해진 순서대로 움직여야 최종 제품의 품질이 보장된다. 어느 한 공정이 부실하면 전체 제품이 불량이 된다.

---

---

---

## Ⅲ. 비교 및 연결

[데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 퍼 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) ([Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) per [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 패턴을(를) 유사 개념과 비교하면 경계와 특성이 더 명확해진다.

| 비교 항목 | [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 퍼 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) ([Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) per [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 패턴 | 유사 대안 |
| :--- | :--- | :--- |
| 핵심 목적 | 체계적 품질·생산성 향상 | 임시 방편적 해결 |
| 적용 규모 | 중·대규모 프로젝트에서 효과적 | 소규모에서는 오버헤드 발생 가능 |
| 조직 요건 | 팀 전체의 공통 이해와 훈련 필요 | 개인 역량 의존 |
| 측정 가능성 | 정량적 지표로 성과 측정 가능 | 주관적 판단에 의존 |

다른 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) 개념과의 연결을 보면, [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 퍼 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) ([Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) per [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 패턴은(는) 요구공학·설계·테스트·형상관리 전반에 걸쳐 영향을 미친다. 특히 품질 보증(QA, Quality Assurance)과 [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/))와 긴밀하게 연계된다.

- **📢 섹션 요약 비유**: [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 퍼 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) ([Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) per [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 패턴과 유사 대안의 차이는 지도를 가지고 산에 오르는 것과 감으로만 오르는 차이와 같다. 지도(체계적 방법)가 있으면 정상까지 최단 경로를 찾을 수 있지만, 없으면 같은 곳을 맴돌거나 낭떠러지에 빠질 수 있다.

---

---

---

## Ⅳ. 실무 적용 및 기술사 판단

[데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 퍼 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) ([Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) per [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 패턴을(를) 실무에 적용할 때는 다음 판단 기준을 참고한다.

- **📢 섹션 요약 비유**: [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 퍼 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) ([Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) per [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 패턴은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

---

---

## Ⅴ. 기대효과 및 결론

[데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 퍼 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) ([Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) per [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 패턴을(를) 올바르게 적용하면 [소프트웨어 품질](/knowledge-base/studynote/04_software_engineering/06_software_architecture/339_software_quality_definition/)·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·팀 생산성이 동시에 향상된다. 그러나 도입에는 학습 비용과 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 투자가 필요하며, 조직 전체의 공감과 훈련이 선행되어야 한다.

**한계와 전제 조건**:
- 소규모 프로젝트에서는 오버헤드가 발생할 수 있다
- 팀 전체의 충분한 교육과 실습 기간이 필요하다
- 도구 지원 환경 구축에 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 비용이 발생한다

**미래 발전 방향**:
- [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)·[LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 기반 자동화 도구와의 통합으로 적용 효율 향상
- [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/)·[DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 환경에서의 진화적 적용
- 정량적 측정 체계의 고도화를 통한 의사결정 지원 강화

[데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 퍼 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) ([Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) per [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 패턴은 '어떻게 빠르게 짜는가'가 아니라 '어떻게 오래 유지할 수 있는 소프트웨어를 짜는가'에 대한 답이다. 단기 속도보다 장기 지속 가능성을 추구하는 관점으로 기억해야 한다.

- **📢 섹션 요약 비유**: [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 퍼 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) ([Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) per [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 패턴의 기대효과는 마라톤 훈련과 같다. 처음에는 느리고 고통스럽지만, 올바른 훈련 원칙을 지킨 선수만이 결승선에서 최고의 기록을 낼 수 있다. [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 원칙도 단기 편의보다 장기 완성도를 위한 투자다.

---

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) ([Software 엔진ering](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)) | [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 퍼 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) ([Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) per [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 패턴의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [소프트웨어 생명주기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/003_sdlc/) ([SDLC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/), Software Development Life Cycle) | [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 퍼 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) ([Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) per [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 패턴은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 퍼 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) ([Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) per [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 패턴 적용 결과는 QA 활동을 통해 검증되고 측정된다 |
| [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) ([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)) | [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 퍼 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) ([Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) per [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 패턴에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
소프트웨어 위기 (Software Crisis) 인식
    |
    v
데이터베이스 퍼 서비스 (Database per Service) 패턴 개념 정립
    |
    v
표준화 및 방법론 체계화 (ISO, CMMI, Agile)
    |
    v
클라우드 네이티브·AI 기반 확장 적용
    |
    v
지속적 개선 및 DevOps·MLOps 통합
```

이 흐름은 [소프트웨어 위기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/002_software_crisis/) 인식 -> 체계적 방법론 개발 -> 표준화 -> 현대적 플랫폼 적용으로 이어지는 발전 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 퍼 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) ([Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) per [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 패턴은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 311 / 973

<- **이전**: [310. 스트랭글러 피그 (Strangler Fig) 패턴 - 레거시를 점진적으로 MSA로 마이그레이션](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/310_strangler_fig_pattern/)
**다음**: [312. 사가 (Saga) 패턴의 코레오그래피 (Choreography) vs 오케스트레이션 (Orchestration)](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/312_saga_pattern_choreography_orchestration/) ->

---
