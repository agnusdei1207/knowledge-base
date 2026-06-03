---
title: 99. 지속적 배포 (CD, Continuous Deployment / Delivery)
tags:
- software_engineering
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CD ([[165_continuous_deployment|Continuous Deployment]] / Delivery)는 [[090_configuration_item|CI]]([[076_ci_continuous_integration|지속적 통합]])를 통과해 검증이 완료된 소프트웨어 빌드 결과물을 실제 운영 서버(Production)까지 안전하고 빠르게 릴리즈하는 자동화 파이프라인이다.
> 2. **가치**: 배포에 수반되는 인간의 반복적인 수동 작업과 장애 발생의 공포를 제거하여, 하루에도 수십 번의 '스몰 배포(Small [[087_deployment_kubernetes_workload_rolling_update|Deployment]])'를 가능하게 함으로써 비즈니스 민첩성을 극대화한다.
> 3. **판단 포인트**: 최종 운영 서버 반영 전 담당자의 수동 승인을 거치는지(Delivery) 아니면 무인 자동화로 100% 직행하는지([[087_deployment_kubernetes_workload_rolling_update|Deployment]])에 따라 조직의 릴리즈 통제 수준이 결정된다.

---

## Ⅰ. 개요 및 필요성

지속적 배포/제공 (CD, [[165_continuous_deployment|Continuous Deployment]] / Delivery)은 [[004_agile_relation|애자일]]([[004_agile_relation|Agile]])과 [[652_devops_calms_culture|데브옵스]]([[652_devops_calms_culture|DevOps]]) 환경에서 코드의 변경 사항을 사용자에게 전달하는 속도의 병목을 해결하기 위해 고안된 프랙티스다. 개발자들이 합친 코드를 에러 없이 조립하는 과정이 [[090_configuration_item|CI]]([[019_continuous_integration|Continuous Integration]])라면, CD는 그 완성된 결과물을 포장하여 라이브 환경까지 안전하게 탁송하는 시스템이다.

과거 [[062_itil|ITIL]] 기반의 전통적 환경에서는 새 [[288_version_ihl_tos_total_length|버전]]을 배포하기 위해 "빅뱅 릴리즈" 방식을 취했다. 수십 명의 엔지니어가 주말 새벽에 모여 스크립트를 수동으로 실행하고 코드를 복사했으며, 한 번의 실수로 인한 다운타임과 대국민 사과문은 일상이었다. 시장은 점점 더 빠른 기능 업데이트를 요구하는데, 배포 과정 자체가 거대한 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]]로 작용했다. 이를 타파하기 위해 배포 과정을 코드화([[072_declarative_pipeline_jenkinsfile_as_code|Pipeline as Code]])하고, 에러 감지 시 즉각 [[098_rollback_strategy_pipeline_error_threshold|롤백]]([[313_rollback|Rollback]])하는 자동화 봇(Bot)을 도입하여 '배포의 공포'를 0으로 수렴시킨 것이 CD 파이프라인의 탄생 배경이다.

- **📢 섹션 요약 비유**: CI가 공장 안에서 불량 부품을 골라내며 완벽한 자동차를 '조립'하는 과정이라면, CD는 완성된 자동차를 탁송 트럭에 태워 고객의 집 문 앞까지 단 1초의 [[015_지연_데이터_관점|지연]] 없이 완벽하게 '배송'하는 100% 자율주행 물류 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

CD 파이프라인은 코드가 커밋되는 순간부터 운영 서버에 안착하기까지의 워크플로우를 자동화 툴체인(예: [[071_jenkins_ci_cd_pipeline_automation|Jenkins]], ArgoCD, GitHub Actions)으로 연결한다.

```text
┌──────────────────────────────────────────────────────────────┐
│             CD 파이프라인의 2가지 뉘앙스와 워크플로우        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ [ CI 완료 ] ──▶ [ Staging 환경 자동 배포 ] ──▶ (통합 테스트/QA)│
│                                                              │
│ 1. Continuous Delivery (지속적 제공) - 인간의 마지막 허락    │
│    (QA 완료) ──▶ [출하 대기장 보관] ──▶ 👤 PO/보안팀 수동 승인 ──▶ [운영 환경 배포]│
│                                         (Approve Click)      │
│                                                              │
│ 2. Continuous Deployment (지속적 배포) - 로봇의 무인 독주    │
│    (QA 완료) ──▶ 🤖 조건 만족 시 즉시 100% 자동 직행 ────────▶ [운영 환경 배포]│
└──────────────────────────────────────────────────────────────┘
```

CD의 핵심 아키텍처는 **[[082_zero_downtime_deployment_rolling_blue_green_canary|무중단 배포]]([[082_zero_downtime_deployment_rolling_blue_green_canary|Zero Downtime Deployment]])** 메커니즘을 내장한다는 것이다. 고객이 [[090_service_kubernetes_network_load_balancing|서비스]]를 사용 중인 10초의 순간에도 릴리즈가 이루어져야 하므로, 구버전 서버와 신버전 서버를 스위치처럼 교체하는 블루/그린(Blue/Green) 배포나, 서버를 1~2대씩 순차적으로 갈아 끼우는 롤링(Rolling) 배포, 트래픽을 5%만 먼저 흘려보내 모니터링하는 [[595_canary_stack_smashing_protector|카나리]]([[595_canary_stack_smashing_protector|Canary]]) 배포 기법이 파이프라인 내부 로직으로 작동한다. 

- **📢 섹션 요약 비유**: Delivery가 고객 집 앞에 택배를 두고 가서 주인이 직접 상자를 열어야 하는 방식이라면, Deployment는 자율주행 로봇이 내 방 책상 위에 물건을 세팅하고 껍질까지 뜯어 놓는 완벽한 풀오토 배송이다.

---

## Ⅲ. 비교 및 연결

조직의 성숙도에 따라 Delivery와 [[087_deployment_kubernetes_workload_rolling_update|Deployment]] 중 무엇을 채택할지 뚜렷한 경계가 나뉜다.

| 비교 항목 | [[164_continuous_delivery|Continuous Delivery]] (제공) | [[165_continuous_deployment|Continuous Deployment]] (배포) |
| :--- | :--- | :--- |
| **운영 서버 배포 주체** | 인간 (버튼 클릭 등 수동 승인) | 시스템 (조건 충족 시 자동화) |
| **비즈니스 통제력** | 높음 (마케팅 타이밍에 맞춰 출시 가능) | 낮음 (개발 완료 즉시 시장에 나감) |
| **테스트 [[085_confidence_association_rule_conditional_probability|신뢰도]] 요구사항** | 높지만 마지막 방어선(인간)이 있음 | **절대적 ([[164_tdd_test_driven_development|TDD]], [[265_e2e_end_to_ui_selenium|E2E]] 완벽해야 함)** |
| **적합한 기업 조직** | 금융, 의료, B2B 엔터프라이즈 솔루션 | 넷플릭스, 아마존 등 B2C 플랫폼 |

특히 현대의 [[531_cloud_native_architecture|클라우드 네이티브]] 환경에서는 Git 저장소의 상태를 유일한 진실의 원천(SSOT)으로 삼고, [[196_kubernetes_k8s_container_orchestration|쿠버네티스]]([[205_kubernetes_container_orchestration|Kubernetes]]) 클러스터가 저장소의 상태와 현재 서버 상태를 지속적으로 일치시키는 [[167_gitops|깃옵스]]([[119_gitops_single_source_of_truth|GitOps]]) 아키텍처와 연결되어 CD의 신뢰성을 극도로 끌어올렸다. 

- **📢 섹션 요약 비유**: Delivery는 결재 서류가 사장님 책상 위까지 완벽하게 작성되어 대기하는 상태(결재 대기)이고, Deployment는 [[190_ai_llm_requirements_specification|AI]] 비서가 서류를 검토하자마자 곧바로 회사 도장을 찍어 밖으로 발송해버리는 전권 위임 시스템이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

CD는 기술적인 도구 설치만으로 완성되지 않으며, 배포 실패 시의 [[098_rollback_strategy_pipeline_error_threshold|롤백]]([[313_rollback|Rollback]]) 전략이 철저하게 준비되어야 한다.

### [[435_checklist_based_testing|체크리스트]] 및 의사결정 기준
1. **스몰 배지(Small Batch) 단위 배포 여부**: 한 달 치 코드를 모아서 한 번에 CD 파이프라인에 태우면 에러 추적이 불가능하다. 변경 사항을 아주 작은 단위로 쪼개어 하루에도 여러 번 파이프라인을 통과시키는 개발 문화가 정착되었는가?
2. **자동 [[098_rollback_strategy_pipeline_error_threshold|롤백]] [[431_ssthresh_slow_start_threshold|임계치]] [[009_config|설정]]**: 배포 직후 5분 내에 [[461_http_stateless_connection_oriented|HTTP]] 500 에러율이 1%를 초과하거나 CPU 사용량이 폭증하면 인간의 개입 없이 CD 도구가 알아서 이전 [[288_version_ihl_tos_total_length|버전]] 컨테이너로 [[098_rollback_strategy_pipeline_error_threshold|롤백]]하도록 헬스체크 트리거가 연동되어 있는가 판단해야 한다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- **수동 스크립트의 난입**: 파이프라인 중간에 "DB [[005_schema|스키마]] 변경은 DBA가 직접 콘솔에서 실행해야 한다"며 수동 병목을 남겨두는 설계. 이는 CD의 생명인 재현 가능성을 파괴하며, 새벽 배포 시 담당자 부재로 인한 파이프라인 프리징을 유발하는 [[128_water_scrum_fall_anti_pattern|안티패턴]]이다. (DB 마이그레이션 도구인 Flyway, Liquibase 등을 연동해 코드화해야 함).

- **📢 섹션 요약 비유**: [[098_rollback_strategy_pipeline_error_threshold|롤백]] 없는 CD는 브레이크 없이 시속 100km로 달리는 스포츠카와 같다. 진정한 CD 파이프라인은 빠르게 달리는 엔진뿐만 아니라, 위험을 감지하면 1초 만에 제자리에 멈춰 서는 완벽한 자율 긴급 제동(자동 [[098_rollback_strategy_pipeline_error_threshold|롤백]]) 시스템을 갖춰야만 실무에 도입할 수 있다.

---

## Ⅴ. 기대효과 및 결론

완벽한 CD ([[165_continuous_deployment|Continuous Deployment]]/Delivery) 파이프라인이 뚫리면 조직의 개발 문화 자체가 바뀐다. 배포에 대한 두려움이 사라져 개발자는 코드 작성 자체에만 집중할 수 있고, '아이디어가 떠오르고 코드를 짜서 고객이 실제로 쓰기까지의 시간([[085_lead_time_cycle_time|Lead Time]])'이 수 주에서 단 몇 시간으로 단축된다.

비록 [[090_configuration_item|CI]] 환경 구축보다 테스트 커버리지에 대한 강박적인 요구 수준이 높아 도입 난이도는 높지만, 한 번 구축된 CD 파이프라인은 [[652_devops_calms_culture|데브옵스]]의 최종 목표인 '무중단 [[090_service_kubernetes_network_load_balancing|서비스]] 혁신'을 물리적으로 보장한다. CD는 단순한 배포 자동화 스크립트가 아니라, 비즈니스의 민첩성을 담보하는 가장 강력한 IT 심장으로 기억되어야 한다.

- **📢 섹션 요약 비유**: 과거의 배포는 이삿짐 센터를 불러 날짜를 정하고 온 집안이 난리가 나는 큰 행사였다면, CD가 도입된 배포는 수도꼭지를 틀면 물이 자연스럽게 흘러나오듯 언제든 고객에게 새로운 기능을 공급할 수 있는 안정적인 상수도 인프라다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **블루/그린 배포 (Blue/Green [[087_deployment_kubernetes_workload_rolling_update|Deployment]])** | CD 파이프라인 내에서 다운타임을 없애기 위해 구버전과 신버전 트래픽을 스위칭하는 핵심 [[082_zero_downtime_deployment_rolling_blue_green_canary|무중단 배포]] 기법 |
| **[[595_canary_stack_smashing_protector|카나리]] 릴리즈 ([[195_canary_release_deployment|Canary Release]])** | CD 배포 시 전체 트래픽 대신 일부 사용자(예: 5%)에게만 먼저 신버전을 노출해 에러를 탐지하는 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] 최소화 기법 |
| **[[167_gitops|깃옵스]] ([[119_gitops_single_source_of_truth|GitOps]])** | CD의 진화형으로, 인프라와 배포 선언문을 Git에 올려두면 봇(ArgoCD 등)이 이를 읽어 운영 서버의 상태를 강제로 일치시키는 [[212_synchronization_mechanisms|동기화]] 패턴 |

### 📈 관련 키워드 및 발전 흐름도

```text
빅뱅 배포 (Big Bang) · 월 단위 수동 배포, 잦은 장애 발생
    │
    ▼
지속적 통합 (CI) 정착 · 코드 병합 및 테스트 자동화 보편화
    │
    ▼
지속적 제공 (Continuous Delivery) · 검증된 코드를 출하 대기까지 자동화 (수동 승인)
    │
    ▼
무중단 배포 기법 융합 · 블루/그린, 카나리, 롤링 등 다운타임 제로 아키텍처
    │
    ▼
지속적 배포 (Continuous Deployment) · Git 커밋부터 라이브 환경까지 100% 무인 자동화 직행
```

### 👶 어린이를 위한 3줄 비유 설명

1. CD는 장난감 공장에서 다 만들어진 예쁜 장난감을 우리 집 앞까지 가장 빠르고 안전하게 가져다주는 자동화된 배달 로봇이에요.
2. 로봇은 배달 중에 장난감이 고장 나지 않게 튼튼하게 포장하고, 집 주인이 쓰고 있는 도중에도 뺏어가지 않고 몰래 새것으로 바꿔주는 마술([[082_zero_downtime_deployment_rolling_blue_green_canary|무중단 배포]])을 부린답니다.
3. 이 로봇 덕분에 어른들은 밤새워서 힘들게 일하지 않아도 매일매일 새로운 장난감 기능을 우리에게 선물해 줄 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 99 / 973

← **이전**: [[098_iac_infrastructure_as_code_terraform|98. 인프라로서의 코드 (IaC, Infrastructure as Code)]]
**다음**: [[100_sre_site_reliability_engineering_error_budget|100. SRE (Site Reliability Engineering) - 구글의 운영 방식, 에러 예산]] →

---
