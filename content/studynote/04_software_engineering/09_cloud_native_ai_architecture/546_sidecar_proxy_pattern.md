+++
title = "546. 사이드카 (Sidecar) 프록시 패턴 - Istio, Envoy, Linkerd"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) (Sidecar) [프록시 패턴](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/158_proxy_pattern/) - [Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/), Envoy, Linkerd은(는) [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 오토바이 옆에 사람 1명이 더 탈 수 있게 조그맣게 달아놓은 보조석을 '[사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)'라고 부른다. 쿠버네티스의 방([Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/)) 안에는 원래 내 앱(Tomcat 등) 1개만 띄우는 게 국룰이다. 하지만 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) 패턴은 이 방 안에 `Envoy`나 `Linkerd-proxy` 같은 초소형 C++ [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 깡통을 1개 더 몰래 끼워 넣는다(Sidecar [Injection](/knowledge-base/studynote/04_software_engineering/11_testing_validation/480_injection/)). 앱이 밖으로 통신을 쏘려고 하면, 이 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)가 옆에서 잽싸게 낚아채서 암호화([mTLS](/knowledge-base/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/))를 씌우고 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)을 대신해 준다.

- **필요성**: MSA로 서버를 50개 찢었다. 보안팀에서 "모든 서버끼리 통신할 때 인증서 달고 암호화([mTLS](/knowledge-base/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/))해라!" 지시가 떨어졌다. 자바팀은 스프링 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 추가해서 3일 만에 짰다. Node.js 팀은 인증서 파싱 버그가 터져서 2주일 내내 야근했다. C++ 팀은 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)가 없어서 개발을 포기했다. **"통신이나 보안 같은 공통 기능(Cross-Cutting)을 각자 언어(App)의 뱃속에 로직으로 짜게 냅두면 언어 파편화 지옥에 빠져 죽는다. 앱 밖으로 끄집어내서 언어 상관없이 똑같이 적용되는 투명한 조끼([Proxy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/))를 입혀버리자!"**라는 생존의 딜레마가 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)를 발명하게 했다.

- **💡 비유**: [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)는 대통령(앱)을 모시는 **'수석 비서관 겸 경호원'**과 똑같습니다. 대통령은 오직 국정(비즈니스 로직)만 고민하면 됩니다. 대통령이 "저기 국방부 장관한테 이 서류 좀 줘!"라고 허공에 말하면, 항상 옆에 붙어있는 수석 비서관([사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/))이 그걸 낚아채서, 특급 기밀 암호([mTLS](/knowledge-base/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/))로 포장하고 방탄조끼를 입은 뒤 오토바이를 타고 가장 안 막히는 길([라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/))로 달려가 상대방 비서관에게 전달합니다. 대통령은 비서관이 오토바이를 타는지 헬기를 타는지 알 필요도 없이 완벽하게 국정에만 100% 에너지를 쏟을 수 있습니다.

- **등장 배경 및 발전 과정**:
  1. **팻 클라이언트([Fat](/knowledge-base/studynote/02_operating_system/09_file_system/525_fat_file_allocation_table/) [Client](/knowledge-base/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/))의 비극**: 2010년 초반 넷플릭스는 통신 툴(`Eureka, Hystrix`)을 자바 앱 소스 안에 다 때려 박았다. 자바 앱은 비대해졌고, 다른 언어 개발자들은 이 훌륭한 툴을 구경만 해야 했다.
  2. **[Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) [Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 구조의 재발견 (2015)**: K8s가 "우리는 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 1개가 기본 단위가 아니라, [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 여러 개를 묶을 수 있는 `Pod`라는 방(Room)이 기본 단위야!"라고 선포했다. 천재들이 무릎을 쳤다. "아, 저 방 안에 꼬붕 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 하나 더 넣어서 통신 짬처리시키면 대박이겠네!"
  3. **Envoy와 Istio의 천하통일 (현재)**: 2016년 차량 공유 기업 Lyft가 초광속 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) `Envoy`를 오픈소스로 풀었다. 이를 구글이 주워다가 `Istio` [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 메시의 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)로 박아버리면서 클라우드 통신망의 절대 표준 패턴으로 폭발했다.

- **📢 섹션 요약 비유**: 옛날 개발은 정수기 물을 마시기 위해 **'내 뱃속(위장)에 더러운 물을 걸러내는 필터를 수술해서 박아넣는 짓([Fat](/knowledge-base/studynote/02_operating_system/09_file_system/525_fat_file_allocation_table/) [Client](/knowledge-base/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/))'**이었습니다. 소화 불량([성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하)이 오죠. [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) 패턴은 내 뱃속을 건드리지 않고, 그냥 내가 차고 다니는 수통 주둥이에 **'뗐다 붙였다 할 수 있는 10원짜리 휴대용 필터([사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/))'**를 꽉 끼우는 겁니다. 내 몸(코드)은 100% 순결하게 남겨둔 채 물만 완벽하게 정수해 먹는 천재적인 외과 수술 면제술입니다.

---

다음은 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) (Sidecar) [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 패의 핵심 구조와 흐름을 보여주는 다이어그램이다.

```text
┌─────────────────────────────────────────────────────────────┐
│                  사이드카 (Sidecar) 프록시 패                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [입력/요구사항] ──▶ [핵심 처리 과정] ──▶ [출력/결과물]  │
│       │                    │                    │          │
│       ▼                    ▼                    ▼          │
│   요구 분석           설계·적용           품질 검증        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

이 다이어그램은 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) (Sidecar) [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) 패가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 검증된 결과물을 산출하는 흐름을 보여준다.

---

---

---

## Ⅱ. 아키텍처 및 핵심 원리

[사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) (Sidecar) [프록시 패턴](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/158_proxy_pattern/) - [Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/), Envoy, Linkerd의 핵심 원리와 구성 요소를 이해하기 위해 다음 구조를 살펴본다.

| 구성 요소 | 역할 | 적용 기준 |
| :--- | :--- | :--- |
| 개념 정의 | 핵심 용어와 범위를 명확히 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) | 용어 혼용·오해 방지 |
| 원칙 및 규칙 | 적용 시 따라야 할 기본 방향 | [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)·품질 기준 |
| 기법 및 도구 | 실질적 구현 방법과 지원 도구 | 생산성·자동화 |
| 측정 지표 | 결과물의 품질을 정량화하는 지표 | 의사결정 근거 |

[사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) (Sidecar) [프록시 패턴](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/158_proxy_pattern/)의 핵심 원리는 **복잡성 분해**, **역할 분리**, **품질 측정**의 세 축으로 이해할 수 있다. 복잡한 문제를 관리 가능한 단위로 나누고, 각 역할의 책임을 명확히 하며, 결과를 정량적 지표로 평가하는 과정이 반복된다.

- **📢 섹션 요약 비유**: [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) (Sidecar) [프록시 패턴](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/158_proxy_pattern/)의 아키텍처는 공장의 생산 라인과 같다. 각 공정(구성 요소)이 명확한 역할을 가지고 정해진 순서대로 움직여야 최종 제품의 품질이 보장된다. 어느 한 공정이 부실하면 전체 제품이 불량이 된다.

---

---

---

## Ⅲ. 비교 및 연결

[사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) (Sidecar) [프록시 패턴](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/158_proxy_pattern/)을(를) 유사 개념과 비교하면 경계와 특성이 더 명확해진다.

| 비교 항목 | [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) (Sidecar) [프록시 패턴](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/158_proxy_pattern/) | 유사 대안 |
| :--- | :--- | :--- |
| 핵심 목적 | 체계적 품질·생산성 향상 | 임시 방편적 해결 |
| 적용 규모 | 중·대규모 프로젝트에서 효과적 | 소규모에서는 오버헤드 발생 가능 |
| 조직 요건 | 팀 전체의 공통 이해와 훈련 필요 | 개인 역량 의존 |
| 측정 가능성 | 정량적 지표로 성과 측정 가능 | 주관적 판단에 의존 |

다른 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) 개념과의 연결을 보면, [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) (Sidecar) [프록시 패턴](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/158_proxy_pattern/)은(는) 요구공학·설계·테스트·형상관리 전반에 걸쳐 영향을 미친다. 특히 품질 보증(QA, Quality Assurance)과 [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/))와 긴밀하게 연계된다.

- **📢 섹션 요약 비유**: [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) (Sidecar) [프록시 패턴](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/158_proxy_pattern/)과 유사 대안의 차이는 지도를 가지고 산에 오르는 것과 감으로만 오르는 차이와 같다. 지도(체계적 방법)가 있으면 정상까지 최단 경로를 찾을 수 있지만, 없으면 같은 곳을 맴돌거나 낭떠러지에 빠질 수 있다.

---

---

---

## Ⅳ. 실무 적용 및 기술사 판단

[사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) (Sidecar) [프록시 패턴](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/158_proxy_pattern/)을(를) 실무에 적용할 때는 다음 판단 기준을 참고한다.

- **📢 섹션 요약 비유**: [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) (Sidecar) [프록시 패턴](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/158_proxy_pattern/)은(는) 복잡한 공사 현장에서 설계도와 공정표를 기반으로 팀을 이끄는 현장 감독과 같다. 원칙 없이 무작정 짓기 시작하면 결국 재공사가 필요하듯, 소프트웨어도 올바른 원칙 위에서만 품질과 효율이 보장된다.

---

---

## Ⅴ. 기대효과 및 결론

[사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) (Sidecar) [프록시 패턴](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/158_proxy_pattern/)을(를) 올바르게 적용하면 [소프트웨어 품질](/knowledge-base/studynote/04_software_engineering/06_software_architecture/339_software_quality_definition/)·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·팀 생산성이 동시에 향상된다. 그러나 도입에는 학습 비용과 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 투자가 필요하며, 조직 전체의 공감과 훈련이 선행되어야 한다.

**한계와 전제 조건**:
- 소규모 프로젝트에서는 오버헤드가 발생할 수 있다
- 팀 전체의 충분한 교육과 실습 기간이 필요하다
- 도구 지원 환경 구축에 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 비용이 발생한다

**미래 발전 방향**:
- [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)·[LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 기반 자동화 도구와의 통합으로 적용 효율 향상
- [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/)·[DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 환경에서의 진화적 적용
- 정량적 측정 체계의 고도화를 통한 의사결정 지원 강화

[사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) (Sidecar) [프록시 패턴](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/158_proxy_pattern/)은 '어떻게 빠르게 짜는가'가 아니라 '어떻게 오래 유지할 수 있는 소프트웨어를 짜는가'에 대한 답이다. 단기 속도보다 장기 지속 가능성을 추구하는 관점으로 기억해야 한다.

- **📢 섹션 요약 비유**: [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) (Sidecar) [프록시 패턴](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/158_proxy_pattern/)의 기대효과는 마라톤 훈련과 같다. 처음에는 느리고 고통스럽지만, 올바른 훈련 원칙을 지킨 선수만이 결승선에서 최고의 기록을 낼 수 있다. [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 원칙도 단기 편의보다 장기 완성도를 위한 투자다.

---

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) ([Software Engineering](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)) | [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) (Sidecar) [프록시 패턴](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/158_proxy_pattern/)의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [소프트웨어 생명주기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/003_sdlc/) ([SDLC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/), Software Development Life Cycle) | [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) (Sidecar) [프록시 패턴](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/158_proxy_pattern/)은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) (Sidecar) [프록시 패턴](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/158_proxy_pattern/) 적용 결과는 QA 활동을 통해 검증되고 측정된다 |
| [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) ([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)) | [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) (Sidecar) [프록시 패턴](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/158_proxy_pattern/)에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
소프트웨어 위기 (Software Crisis) 인식
    │
    ▼
사이드카 (Sidecar) 프록시 패턴 개념 정립
    │
    ▼
표준화 및 방법론 체계화 (ISO, CMMI, Agile)
    │
    ▼
클라우드 네이티브·AI 기반 확장 적용
    │
    ▼
지속적 개선 및 DevOps·MLOps 통합
```

이 흐름은 [소프트웨어 위기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/002_software_crisis/) 인식 → 체계적 방법론 개발 → 표준화 → 현대적 플랫폼 적용으로 이어지는 발전 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) (Sidecar) [프록시 패턴](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/158_proxy_pattern/)은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 684 / 973

← **이전**: [546. 사이드카 (Sidecar) 프록시 패턴 - Istio, Envoy, Linkerd](/knowledge-base/studynote/04_software_engineering/11_testing_validation/546_sidecar_proxy_pattern/)
**다음**: [547. 트래픽 라우팅, 카나리 배포 제어 (Service Mesh의 역할)](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/547_service_mesh_traffic_routing_canary/) →

---
