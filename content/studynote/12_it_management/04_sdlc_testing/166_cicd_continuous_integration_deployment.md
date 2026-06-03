---
title: 166. CI/CD (Continuous Integration/Continuous Deployment, 지속적 통합/배포)
date: '2026-04-21'
tags:
- studynote-it-management
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[090_configuration_item|CI]]/CD는 코드 변경을 빌드·테스트·[[395_verification_process_review|검증]]·배포 가능한 산출물까지 자동 흐름으로 연결해, 통합과 배포를 이벤트가 아니라 일상 작업으로 바꾸는 개발 운영 체계다.
> 2. **가치**: 작은 변경을 자주 [[395_verification_process_review|검증]]하고 자주 배포하면 통합 충돌, 배포 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]], 장애 원인 범위가 함께 줄어들어 속도와 안정성을 동시에 높일 수 있다.
> 3. **판단 포인트**: [[090_configuration_item|CI]] ([[019_continuous_integration|Continuous Integration]], [[076_ci_continuous_integration|지속적 통합]]), [[164_continuous_delivery|Continuous Delivery]] ([[164_continuous_delivery|지속적 제공]]), [[165_continuous_deployment|Continuous Deployment]] ([[099_continuous_deployment_cd|지속적 배포]])의 경계를 명확히 구분하고, 조직 성숙도에 맞는 자동화 수준을 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

[[090_configuration_item|CI]]/CD는 소프트웨어 변경을 "개발 완료 후 한 번에 통합"하던 방식에서 벗어나, 커밋 단위로 자주 통합하고 [[395_verification_process_review|검증]]하며 배포 가능한 상태를 유지하는 접근이다. 과거의 대규모 통합 방식에서는 개발자별 작업 기간이 길어질수록 코드 충돌, 환경 차이, 수작업 배포 오류가 한 번에 폭발했다. 이른바 통합 지옥 (Integration Hell)은 기능 개발보다 병합과 안정화에 더 많은 시간을 쓰게 만들었다.

CI는 이 문제를 "작은 변경의 빠른 [[395_verification_process_review|검증]]"으로 줄인다. CD는 여기서 한 걸음 더 나아가, [[395_verification_process_review|검증]]된 산출물을 스테이징이나 운영 환경으로 안전하게 보내는 자동 경로를 만든다. 결국 [[090_configuration_item|CI]]/CD의 필요성은 단순 자동화가 아니라, 변경의 크기를 줄여 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]]를 관리 가능한 단위로 쪼개는 데 있다.

```text
┌────────────────────────────────────────────────────────────────────┐
│        대형 배치 통합 vs 지속 통합: 위험의 크기를 줄이는 전략      │
├────────────────────────────────────────────────────────────────────┤
│ Old way:                                                          │
│   weeks of changes ─▶ big merge ─▶ late test ─▶ big failure       │
│                                                                    │
│ CI/CD way:                                                        │
│   small commit ─▶ auto build ─▶ auto test ─▶ deploy-ready state   │
│   repeated many times with smaller blast radius                    │
└────────────────────────────────────────────────────────────────────┘
```

이 그림에서 핵심은 [[090_configuration_item|CI]]/CD가 단지 속도를 올리는 장치가 아니라, 실패 반경 (Blast [[541_radius_remote_authentication_aaa|Radius]])을 줄이는 구조라는 점이다. 변경 단위가 작을수록 원인 추적, [[098_rollback_strategy_pipeline_error_threshold|롤백]], 재배포가 모두 쉬워진다.

- **📢 섹션 요약 비유**: 한 달 치 숙제를 마지막 날 몰아서 검사하면 어디서 틀렸는지 찾기 어렵다. [[090_configuration_item|CI]]/CD는 숙제를 매일 내고 바로 채점받아, 틀린 부분을 작고 빨리 고치게 하는 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[090_configuration_item|CI]]/CD 파이프라인은 보통 소스 변경 감지, 빌드, 자동 테스트, 보안·품질 검사, [[075_artifact_management_nexus_docker_registry|아티팩트]] ([[075_artifact_management_nexus_docker_registry|Artifact]]) [[087_process_state_transition|생성]], 환경 배포의 순서로 구성된다. 중요한 점은 각 단계가 단순 절차가 아니라 "다음 단계로 넘겨도 되는가"를 판단하는 품질 게이트 (Quality Gate) 역할을 한다는 것이다. 즉 파이프라인은 자동화된 컨베이어벨트이면서 동시에 자동 심사관이다.

| 단계 | 주요 작업 | 실패 시 의미 |
| :--- | :--- | :--- |
| Source | 커밋, [[067_pull_request_pr_merge_request_code_review|Pull Request]], [[330_code_review|코드 리뷰]] | 변경 추적 불가, [[025_baseline|기준선]] 불명확 |
| Build | 컴파일, 패키징, 이미지 [[087_process_state_transition|생성]] | 실행 가능한 산출물 미확보 |
| Test | 단위·통합·[[265_e2e_end_to_ui_selenium|E2E]] ([[401_transport_layer_role_end_to_end_multiplexing|End-to-End]]) 테스트 | 기능 안정성 미검증 |
| Scan | [[331_static_analysis|정적 분석]], 취약점 검사, 라이선스 [[396_validation|확인]] | 품질·보안 위험 잠재 |
| Deploy | 스테이징/운영 반영 | 운영 전환 실패 또는 배포 위험 |

다음 [[103_ascii|ASCII]] 다이어그램은 전형적인 [[090_configuration_item|CI]]/CD 흐름과 "한 번 만든 산출물을 같은 형태로 승격"하는 원칙을 보여준다.

```text
┌────────────────────────────────────────────────────────────────────┐
│                     CI/CD pipeline with quality gates              │
├────────────────────────────────────────────────────────────────────┤
│ Commit/Pull Request                                               │
│   │                                                                │
│   ▼                                                                │
│ Build ──▶ Unit Test ──▶ Integration Test ──▶ Security Scan         │
│   │           │                  │                    │             │
│   └──── fail fast and stop pipeline if any gate fails ───────────┐ │
│                                                                  │ │
│ Artifact Registry  ◀─────────────────────────────────────────────┘ │
│   │                                                                │
│   ▼                                                                │
│ Staging Deploy ──▶ Manual Approval(optional) ──▶ Production Deploy │
└────────────────────────────────────────────────────────────────────┘
```

여기서 좋은 파이프라인은 환경마다 다시 빌드하지 않는다. 같은 [[075_artifact_management_nexus_docker_registry|아티팩트]]를 테스트, 스테이징, 운영으로 승격해야 환경 차이로 인한 "테스트에서는 성공했는데 운영에서 실패" 문제를 줄일 수 있다. 또한 Fail Fast 원칙에 따라 앞단에서 실패를 빨리 드러내야 전체 [[085_lead_time_cycle_time|리드 타임]]이 짧아진다.

- **📢 섹션 요약 비유**: 공장에서 제품을 만들 때 중간 검사에서 불량이 나오면 바로 라인을 멈춰야 손실이 적다. [[090_configuration_item|CI]]/CD도 앞 단계에서 빨리 걸러낼수록 뒤의 큰 사고를 막는다.

---

## Ⅲ. 비교 및 연결

시험과 실무에서 가장 자주 묻는 포인트는 [[090_configuration_item|CI]], [[164_continuous_delivery|Continuous Delivery]], Continuous Deployment의 차이다. CI는 코드가 항상 통합 가능한 상태인지 보장하는 데 초점이 있다. Continuous Delivery는 운영 직전까지 자동화하되 최종 운영 반영에 사람 승인을 두고, Continuous Deployment는 그 승인마저 자동화해 [[395_verification_process_review|검증]] 통과 후 바로 운영에 반영한다.

| 구분 | 핵심 질문 | 운영 배포 승인 | 적합한 환경 |
| :--- | :--- | :--- | :--- |
| [[090_configuration_item|CI]] | 통합 결과가 항상 건강한가? | 해당 없음 | 모든 개발 조직 |
| [[164_continuous_delivery|Continuous Delivery]] | 언제든 배포할 준비가 되었는가? | 있음 | 규제 산업, 승인 절차가 중요한 조직 |
| [[165_continuous_deployment|Continuous Deployment]] | [[395_verification_process_review|검증]] 통과 시 즉시 배포할 것인가? | 없음 | 테스트 자동화와 관측성이 높은 조직 |

브랜치 [[268_strategy_pattern|전략]]도 [[090_configuration_item|CI]]/CD 성숙도와 연결된다. Git Flow는 릴리스 브랜치 중심이라 Delivery에 잘 맞고, [[040_trunk_based_development|Trunk-Based Development]] ([[040_trunk_based_development|트렁크 기반 개발]])는 짧은 브랜치 수명과 기능 [[186_character_stuffing_dle_stx_etx|플래그]] ([[576_feature_flag_ab_testing_rollout|Feature Flag]])를 전제로 Deployment에 더 유리하다. 즉 [[090_configuration_item|CI]]/CD는 도구 설정만의 문제가 아니라 소스 관리 [[268_strategy_pattern|전략]], 테스트 [[085_confidence_association_rule_conditional_probability|신뢰도]], 배포 [[268_strategy_pattern|전략]]이 맞물린 운영 체계다.

- **📢 섹션 요약 비유**: CI는 매일 건강검진을 하는 것이고, Continuous Delivery는 여행 가방을 늘 싸 둔 상태, Continuous Deployment는 비행기 표만 나오면 바로 공항으로 출발하는 상태다. 자동화 수준이 올라갈수록 준비와 신뢰가 더 필요하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 "파이프라인이 돌아간다"보다 "배포를 믿고 맡길 수 있는가"가 더 중요하다. 예를 들어 웹 [[090_service_kubernetes_network_load_balancing|서비스]] 팀이 GitHub Actions나 Jenkins로 CI를 구축했더라도, 테스트가 느리거나 자주 깨지는 플래키 테스트 (Flaky Test) 상태라면 운영 자동 배포는 오히려 위험하다. 따라서 자동화 수준은 조직의 테스트 품질, [[098_rollback_strategy_pipeline_error_threshold|롤백]] 체계, 관측성, 승인 요구사항에 맞춰 단계적으로 올려야 한다.

### 실무 판단 [[435_checklist_based_testing|체크리스트]]

1. 빌드 결과가 환경마다 동일하게 재현되는가?
2. [[397_unit_test|단위 테스트]], [[400_integration_testing|통합 테스트]], 보안 스캔이 자동 게이트로 연결돼 있는가?
3. 운영 배포 후 이상 징후를 감지할 [[342_routing_metric_hop_bandwidth_delay|메트릭]]·[[568_logs_distributed_logging_elk_fluentd|로그]]·트레이스가 준비돼 있는가?
4. [[194_blue_green_deployment_strategy|블루-그린 배포]] ([[304_process|Blue-Green Deployment]])나 [[115_canary_deployment_gradual_rollout|카나리 배포]] ([[115_canary_deployment_gradual_rollout|Canary Deployment]]) 같은 안전한 전환 [[268_strategy_pattern|전략]]이 있는가?
5. 실패 시 자동 또는 반자동 [[098_rollback_strategy_pipeline_error_threshold|롤백]] 절차가 정의돼 있는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 테스트 없이 빌드 성공만으로 운영 자동 배포를 여는 경우
- 스테이징과 운영이 다른 이미지나 다른 설정으로 배포되는 경우
- 파이프라인 시간이 너무 길어 개발자가 우회 배포를 선택하게 되는 경우
- 비밀정보를 파이프라인 스크립트에 직접 넣어 보안 사고를 유발하는 경우

대표 시나리오로 전자상거래 [[090_service_kubernetes_network_load_balancing|서비스]]는 [[067_pull_request_pr_merge_request_code_review|PR]] 단계에서 [[331_static_analysis|정적 분석]]과 테스트를 수행하고, `main` 병합 시 [[561_container_based_deployment|컨테이너]] 이미지를 [[087_process_state_transition|생성]]해 스테이징에 자동 배포한 뒤, 핵심 지표가 안정적이면 운영으로 승격한다. 규제가 강한 금융권은 Continuous Delivery가 현실적일 수 있고, [[309_saas|SaaS]] (Software [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]]) 플랫폼은 높은 테스트 성숙도를 바탕으로 Continuous Deployment를 선택할 수 있다.

- **📢 섹션 요약 비유**: 자동문이 있다고 해서 모든 건물 출입을 무조건 무인으로 맡기지는 않는다. 사람 흐름과 위험도에 따라 경비원을 두기도 하고 완전 자동 출입을 쓰기도 하듯, [[090_configuration_item|CI]]/CD도 조직 상황에 맞는 자동화 강도를 골라야 한다.

---

## Ⅴ. 기대효과 및 결론

[[090_configuration_item|CI]]/CD가 잘 정착되면 배포 빈도는 높아지고, 변경 [[085_lead_time_cycle_time|리드 타임]] ([[085_lead_time_cycle_time|Lead Time]] for Changes)은 짧아지며, 장애가 나도 원인 범위를 좁게 잡아 빠르게 복구할 수 있다. 이는 [[523_dhcp_dora_process|DORA]] ([[652_devops_calms_culture|DevOps]] Research and Assessment) 지표에서 말하는 배포 빈도, 변경 실패율, [[451_mttr|MTTR]] (Mean Time To [[658_ir_recovery|Recovery]]), [[085_lead_time_cycle_time|리드 타임]] 개선과 직결된다. 즉 [[090_configuration_item|CI]]/CD는 개발 편의 도구가 아니라, 조직의 전달 성능을 측정 가능한 수준으로 끌어올리는 관리 체계다.

반대로 자동화만 있고 테스트 신뢰, 운영 가시성, 팀 문화가 부족하면 "빠르게 자주 망가뜨리는 파이프라인"이 될 수 있다. 따라서 [[090_configuration_item|CI]]/CD의 핵심 기억 포인트는 "빠른 배포"가 아니라 "작은 변경을 반복 가능하게 [[395_verification_process_review|검증]]하고 안전하게 흘려보내는 시스템"이다. 도착점은 도구 도입이 아니라, 배포가 특별 이벤트가 아닌 평상 업무가 되는 상태다.

- **📢 섹션 요약 비유**: 좋은 택배 시스템은 빨리 보내는 것만이 아니라, 어디에 있는지 보이고 문제 나면 바로 회수할 수 있어야 한다. [[090_configuration_item|CI]]/CD도 속도와 통제를 함께 갖춘 배송망으로 기억해야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[652_devops_calms_culture|DevOps]] | [[090_configuration_item|CI]]/CD가 실천되는 조직 문화와 운영 방식 |
| [[075_artifact_management_nexus_docker_registry|Artifact]] | 동일 산출물을 여러 환경으로 승격시키는 핵심 단위 |
| Quality Gate | 테스트·보안·품질 기준을 자동으로 통과시키는 문턱 |
| [[576_feature_flag_ab_testing_rollout|Feature Flag]] | Trunk-Based Development와 자동 배포를 연결하는 위험 분리 장치 |
| Blue-Green/[[595_canary_stack_smashing_protector|Canary]] | 운영 전환 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]]를 줄이는 대표 배포 [[268_strategy_pattern|전략]] |

### 📈 관련 키워드 및 발전 흐름도

```text
수동 통합 · 수동 배포
        │
        ▼
CI (Continuous Integration)
        │
        ▼
Continuous Delivery
        │
        ▼
Continuous Deployment
        │
        ▼
GitOps · Progressive Delivery · DevSecOps
```

이 흐름은 "통합 자동화"에서 출발해 "배포 자동화"로 확장되고, 이후 선언적 운영과 보안 내재화까지 발전하는 경로를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 친구들이 만든 레고를 매일 조금씩 합쳐 보고 바로 흔들어 보면 어디가 잘못됐는지 빨리 알 수 있어요.
2. [[090_configuration_item|CI]]/CD는 레고를 다 만든 뒤 창고에만 두지 않고, 검사까지 끝내서 바로 전시장에 가져갈 수 있게 준비해 두는 거예요.
3. 그래서 큰 실수는 줄고, 고쳐야 할 부분도 작은 조각 단위로 금방 찾을 수 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 280 / 587

← **이전**: [[165_bdd_behavior_driven_development|165. BDD (Behavior Driven Development, 행위 주도 개발)]]
**다음**: [[167_scm_software_configuration_management|167. SCM (Software Configuration Management, 소프트웨어 형상 관리)]] →

---
