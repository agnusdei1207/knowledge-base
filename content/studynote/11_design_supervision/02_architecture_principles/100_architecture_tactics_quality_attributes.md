+++
title = "100. 아키텍처 전술 (Architecture Tactics) - 품질 속성 달성을 위한 설계 전략"
date = 2026-03-04

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)
- **본질**: 아키텍처 전술([Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/) Tactics)은 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/), [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/), [보안성](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/)과 같은 추상적인 품질 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)([Quality Attributes](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/279_quality_attributes_scenario/))을 실제 시스템에 구현하기 위해 아키텍트가 선택하는 구체적인 설계 결정들의 단위다.
- **가치**: 모호한 비기능적 요구사항을 개발자가 코드로 구현할 수 있는 명확한 기법(예: Ping/Echo, [Caching](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/), Encryption)으로 치환하여, 아키텍처 평가와 감리의 기준을 제공한다.
- **판단 포인트**: 특정 전술을 채택하면 하나의 품질 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)은 향상되지만 다른 품질은 저하될 수 있으므로(예: 보안을 위한 암호화 전술 도입 시 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하), 전술 간의 [상충점](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/095_tradeoff_point_architecture_evaluation_atam_conflict/)(Trade-off)을 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)하고 조율하는 것이 핵심이다.

### Ⅰ. 개요 및 필요성
[소프트웨어 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/201_software_architecture_definition/) 설계에서 기능적 요구사항(무엇을 하는가) 못지않게 중요한 것이 비기능적 요구사항(얼마나 잘하는가), 즉 품질 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)([Quality Attributes](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/279_quality_attributes_scenario/))이다.
하지만 "시스템이 빨라야 한다", "안전해야 한다"는 요구사항은 그 자체로 코드에 반영될 수 없다. 아키텍처 전술은 이러한 추상적 목표에 도달하기 위해 특정 자극(Stimulus)에 대한 시스템의 응답(Response)을 통제하는 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)된 설계 기법이다. 이 전술이 없으면 설계 의도가 개발자에게 전달되지 않아 아키텍처와 구현이 분리되는 현상이 발생한다.

- **📢 섹션 요약 비유**: "팀이 이겨야 한다(품질 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/))"는 구단주의 목표만으로는 선수가 움직일 수 없다. "수비수를 늘려라(보안 전술)", "빠른 윙어를 기용해라([성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 전술)"처럼 감독의 구체적인 작전 지시가 바로 아키텍처 전술이다.

### Ⅱ. 아키텍처 및 핵심 원리
아키텍처 전술은 각 품질 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)별로 세분화된 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 풀(Pool)을 형성하며, 이벤트나 장애라는 '자극'이 발생했을 때 시스템이 어떻게 대응할지를 메커니즘으로 정의한다.

| 품질 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) | 전술 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 구체적 전술 기법의 예시 |
|---|---|---|
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a> (<a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">Availability</a>)</strong> | [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 탐지, [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), 예방 | Ping/Echo(탐지), Active-Passive [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)([복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)), 예외 처리(예방) |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> (<a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">Performance</a>)</strong> | 자원 요구 통제, 자원 관리 | 이벤트 큐 속도 조절(통제), [다중 스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/095_multithreading_benefits/)([Concurrency](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/266_other_transparency/)), [캐싱](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/)(관리) |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/">보안성</a> (<a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/">Security</a>)</strong> | 공격 [저항](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/003_resistance/), 공격 탐지, [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)([Authentication](/knowledge-base/studynote/02_operating_system/10_security/604_authentication_factors/)), [인가](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)([Authorization](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)), 암호화, [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) |
| <strong>수정 용이성 (<a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/284_modifiability_tactics/">Modifiability</a>)</strong> | [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/) 감소, [응집도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/) 증가 | 인터페이스 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/), 런타임 [의존성 주입](/knowledge-base/studynote/04_software_engineering/06_software_architecture/337_dependency_injection/)([DI](/knowledge-base/studynote/11_design_supervision/10_patterns_antipatterns/661_enterprise_di_framework_lifecycle/)), [단일 책임 원칙](/knowledge-base/studynote/11_design_supervision/06_exam_summary/355_process/) 적용 |

```text
+-------------------------------------------------------------+
|       Architecture Tactics : Stimulus-Response Mechanism    |
+-------------------------------------------------------------+
|                                                             |
|   [ 자극 (Stimulus) ]                 [ 응답 (Response) ]   |
|   - 서버 A의 전원 장애                - 서버 B로 트래픽 전환|
|   - 해커의 비정상 패킷 유입           - 침입 차단 및 로그   |
|          |                                   ^              |
|          |                                   |              |
|          v                                   |              |
|   +-----------------------------------------------------+   |
|   |               [ 아키텍처 전술 제어부 ]              |   |
|   |                                                     |   |
|   |  - 가용성 전술 : Heartbeat 모니터링, Redundancy     |   |
|   |  - 보안성 전술 : IDS/IPS 침입 탐지 룰 적용          |   |
|   +-----------------------------------------------------+   |
+-------------------------------------------------------------+
```
위 다이어그램은 외부의 자극이 시스템에 [인가](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)될 때, 아키텍처 내부에 내장된 전술들이 이를 감지하고 적절한 응답을 만들어내어 품질 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)을 유지하는 메커니즘을 보여준다. 단일 전술들이 모여서 하나의 거대한 '아키텍처 패턴(예: 클러스터링 패턴)'을 이룬다.

- **📢 섹션 요약 비유**: 건물에 화재(자극)가 발생했을 때 연기를 감지하는 화재경보기([결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 탐지 전술)와 물을 뿌리는 스프링클러([결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 전술)가 동작하여 사람들의 대피 시간(응답)을 확보하는 소방 시스템과 같다.

### Ⅲ. 비교 및 연결
아키텍처 전술을 정확히 이해하려면 이보다 상위 개념인 '[디자인 패턴](/knowledge-base/studynote/04_software_engineering/04_testing_quality/251_design_patterns_gof_overview/)' 및 '아키텍처 패턴'과 비교해야 한다.

| 비교 항목 | 아키텍처 전술 ([Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/) Tactics) | [디자인 패턴](/knowledge-base/studynote/04_software_engineering/04_testing_quality/251_design_patterns_gof_overview/) / 아키텍처 패턴 |
|---|---|---|
| **개념의 위치** | 설계의 기초 단위 (원자적 기법) | 여러 전술이 결합된 완성된 구조 (분자적 템플릿) |
| **목적** | 단일 비기능적 요구사항(품질 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)) 달성 제어 | 클래스 간 상호작용 구조화 및 보편적 설계 문제 해결 |
| **크기/범위** | 국소적이고 구체적임 (예: DB 커넥션 [풀링](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/)) | 시스템 전반의 뼈대 (예: MVC, [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)) |

전술은 단독으로 쓰이기보다는 패턴을 구성하는 부품으로 결합된다. 예를 들어 '[마이크로서비스 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/)([MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/)) 패턴'은 [응집도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/) 증가 전술, [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/) 감소 전술, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [캐싱](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/)([성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 전술)이 복합적으로 융합된 결과물이다.

- **📢 섹션 요약 비유**: 전술이 밀가루, 계란, 설탕 같은 개별적인 '식재료'라면, 패턴은 이 재료들을 특정 비율로 섞어 만들어낸 '초코 케이크 레시피'다. 레시피(패턴) 안에는 항상 여러 식재료(전술)가 포함되어 있다.

### Ⅳ. 실무 적용 및 기술사 판단
실무 설계 및 감리에서 아키텍처 전술은 [상충점](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/095_tradeoff_point_architecture_evaluation_atam_conflict/)(Trade-off) 분석과 추적성 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)의 핵심 도구로 쓰인다.

1. <strong><a href="/knowledge-base/studynote/11_design_supervision/02_architecture_principles/095_tradeoff_point_architecture_evaluation_atam_conflict/">상충점</a> (Trade-off) <a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/">식별</a></strong>: [ATAM](/knowledge-base/studynote/04_software_engineering/04_testing_quality/229_atam_architecture_trade_off_analysis_method/) ([Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/) Trade-off Analysis Method) 같은 평가에서, "왜 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 저하되었는가?"를 찾을 때 아키텍트가 적용한 '보안 전술(강력한 암호화)'이 원인임을 역추적해 낸다. 모든 전술은 공짜가 아니다.
2. <strong>감리에서의 추적성 (<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/228_blockchain_smart_contract_traceability/">Traceability</a>) <a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a></strong>: 제안요청서(RFP)에 요구된 99.9% [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 목표가 물리 배포 뷰나 프로세스 뷰에 '[이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 전술(Active-Passive)'이나 '[서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/) 전술'로 실체화되어 있는지 추적하여 평가해야 한다.
3. **오버엔지니어링 경계**: 요구되는 품질 수준을 넘어서는 과도한 전술(예: 불필요한 실시간 캐시 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)) 적용은 복잡도만 높이므로 시스템 성격에 맞게 기각하는 결단이 필요하다.

- **📢 섹션 요약 비유**: 무거운 방탄복(보안 전술)을 입히면 병사의 달리기 속도([성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/))가 떨어진다. 작전 지역이 시가지인지 평야인지에 따라 방탄복 두께와 기동성 사이의 완벽한 밸런스([상충점](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/095_tradeoff_point_architecture_evaluation_atam_conflict/) 조율)를 찾는 것이 지휘관(아키텍트)의 판단이다.

### Ⅴ. 기대효과 및 결론
아키텍처 전술은 막연한 비즈니스 목표와 구체적인 엔지니어링 구현 사이를 이어주는 다리 역할을 한다. 품질 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)별 전술을 숙지하면, 설계 과정에서 "어떤 기법을 조합할 것인가"를 체계적으로 결정할 수 있다.
미래의 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 환경에서는 Auto-Scaling([성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 전술)이나 [Chaos 엔진ering](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/751_chaos_engineering/)([가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 전술)처럼 전술의 형태가 플랫폼 종속적으로 진화하고 있으나, 특정 자극에 대응하여 품질을 유지한다는 전술의 본질적 철학은 변함없이 시스템 설계의 근간으로 작용한다.

- **📢 섹션 요약 비유**: 뛰어난 의사는 "건강해지세요"라고 말하지 않고, "나트륨을 줄이고(전술 A), 매일 30분 걸으세요(전술 B)"라고 처방한다. 아키텍처 전술은 튼튼한 소프트웨어를 만들기 위한 정확하고 구체적인 처방전이다.

### 📌 관련 개념 맵
- **상위 개념**: [소프트웨어 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/201_software_architecture_definition/), 품질 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) ([Quality Attributes](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/279_quality_attributes_scenario/))
- **연관 개념**: 아키텍처 패턴, [ATAM](/knowledge-base/studynote/04_software_engineering/04_testing_quality/229_atam_architecture_trade_off_analysis_method/) ([Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/) Trade-off Analysis Method), [상충점](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/095_tradeoff_point_architecture_evaluation_atam_conflict/) (Trade-off)
- **파생 개념**: [서킷 브레이커](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/) ([Circuit Breaker](/knowledge-base/studynote/12_it_management/05_security_compliance/304_circuit_breaker/)), [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) (Redundancy)

### 📈 관련 키워드 및 발전 흐름도

```text
비기능 요구사항 정의 (품질 속성)
    |
    v
아키텍처 전술 (Tactics) 선택 · 자극과 응답 메커니즘 설계
    |
    v
아키텍처 패턴 (Patterns) 구성 · 여러 전술의 복합적 템플릿화
    |
    v
ATAM 평가 및 상충점 (Trade-off) 조율
```

이 흐름도는 목표 설정에서 시작해 구체적 전술 선택을 거쳐 완성된 패턴을 형성하고, 최종적으로 평가를 통해 조율하는 아키텍처 설계 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 축구팀이 "우승"이라는 목표를 이루려면 막연히 열심히 뛰는 것만으론 안 되고 아주 구체적인 작전이 필요해요.
2. 수비수를 한 명 더 늘리거나, 빠른 공격수로 교체하는 것처럼 특정 상황에 대응하는 작전 지시가 바로 아키텍처 전술이에요.
3. 컴퓨터 프로그램도 무너지지 않고 빠르게 돌아가기 위해 감독(아키텍트)이 서버를 늘리거나 캐시를 쓰라는 세밀한 전술을 지시한답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 143 / 530

<- **이전**: [99. ADR (Architecture Decision Record) - 아키텍처 설계 결정 기록](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/099_adr_architecture_decision_record/)
**다음**: [101. 객체 지향 설계 원칙 (SOLID, Object-Oriented Design Principles)](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/101_solid_object_oriented_design_principles/) ->

---
