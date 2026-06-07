---
title: "Quality Attribute Scenario"
date: "2026-04-10"
tags:
  - "studynote-design-supervision"
weight: 91
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [품질 속성 시나리오](/studynote/12_it_management/05_security_compliance/993_process/)([Quality Attribute Scenario](/studynote/12_it_management/05_security_compliance/993_process/))는 "빠르다, 안전하다" 같은 모호한 비기능적 요구사항을 6가지 육하원칙 뼈대(자극원, 자극, 환경, 대상, 응답, 응답 척도)에 맞춰 구체적이고 측정 가능한 문장으로 해체하고 재조립하는 명세 기법이다.
> 2. **가치**: 아키텍처 설계의 목표치를 명확한 수치로 합의함으로써, 개발자와 [이해관계자](/studynote/04_software_engineering/03_design_architecture/173_stakeholder_identification_impact_matrix/)(고객/경영진) 간의 주관적 해석 차이로 인한 설계 실패와 분쟁을 사전에 차단하는 법적 방어막 역할을 한다.
> 3. **판단 포인트**: 단순히 요구사항을 한 줄로 적는 것을 넘어, 아키텍처가 특정 상황(과부하, 장애, 공격 등)에서 어떤 방식으로 대처하고 어느 정도의 응답 척도(시간, 비율 등)를 달성해야 하는지를 구체적인 수치로 증명할 수 있어야 한다.

---

## Ⅰ. 개요 및 필요성

[품질 속성 시나리오](/studynote/12_it_management/05_security_compliance/993_process/)는 시스템이 달성해야 하는 비기능적 요구사항([가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/), [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/), [보안성](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) 등)을 정량적이고 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 가능한 형태로 정의하는 아키텍처 명세 도구다.

시스템 구축 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/), 고객은 대개 "서버가 절대 죽지 않고 미친 듯이 빨라야 한다"는 식의 형용사 위주의 주관적이고 모호한 요구사항을 던진다. 이러한 문과식 표현은 아키텍트에게 독이 된다. '빠르다'의 기준이 1초인지 0.1초인지, '죽지 않는다'의 기준이 다운타임 5분 허용인지 단 1초도 안 되는지에 따라 필요한 서버의 대수와 아키텍처의 복잡도가 천양지차로 달라지기 때문이다. 이를 방치하면 프로젝트 후반부에 반드시 책임 소재를 둔 분쟁이 발생한다. 따라서 모든 품질 [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)은 객관적인 테스트가 가능하도록 철저하게 정량적인 시나리오로 치환되어야 메모리를 소모한다.

- **📢 섹션 요약 비유**: 인테리어 업자에게 "방음이 잘 되게 해주세요"라고 요구하면 얇은 스펀지 하나로 끝낼 수 있다. 이를 "윗집에서 10kg 아령을 바닥에 떨어뜨렸을 때(자극), 우리 집 거실에서 측정되는 소음이 30dB 이하여야 한다(응답 척도)"는 식으로 수학적 방어율 계약서로 뜯어고쳐서 나중에 딴소리 못하게 못을 박는 과정이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[품질 속성 시나리오](/studynote/12_it_management/05_security_compliance/993_process/)는 카네기멜론 대학의 [소프트웨어 공학](/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) 연구소(SEI)에서 제안한 6가지 핵심 구성 요소를 갖춘 템플릿으로 작성된다. 어떤 요구사항이든 이 6칸의 빈칸을 채워 넣어야만 완전한 시나리오로 인정받는다.

| 구성 요소 | 의미 | 작성 예시 ([성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 시나리오) |
| :--- | :--- | :--- |
| **자극원 (Source)** | 시스템에 자극을 가하는 주체 | 일반 온라인 쇼핑몰 고객들 |
| **자극 (Stimulus)** | 시스템에 도달한 조건이나 이벤트 | 이벤트 상품 결제 버튼을 동시에 클릭함 |
| <strong>환경 (<a href="/studynote/15_devops_sre/02_cicd_gitops/066_gitlab_flow_environment_branch_strategy/">Environment</a>)</strong> | 자극이 발생했을 때 시스템의 상태 | 블랙프라이데이 트래픽 10배 폭주 상태 |
| <strong>대상 (<a href="/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/">Artifact</a>)</strong> | 자극의 영향을 받는 시스템 범위 | 결제 처리 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 서버 및 대기열([Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/)) |
| **응답 (Response)** | 자극에 대한 시스템의 대처 행동 | 요청을 버리지 않고 순차적으로 처리 승인함 |
| **응답 척도 (Measure)** | 응답이 달성해야 할 정량적 기준 | 99%의 결제 처리가 <strong>1.5초 이내</strong>에 완료될 것 |

```text
+--------------------------------------------------------------+
|                  품질 속성 시나리오 6요소 흐름               |
+--------------------------------------------------------------+
| [자극원] ---------> [자극] ---------> [대상 시스템]          |
| (누가)            (무엇을)          (어디에)                 |
|                                      |                       |
|  ^                                   v                       |
|  |                                [응답]                     |
| [환경]                            (어떻게 대처하는가)        |
| (어떤 상황에서)                      |                       |
|                                      v                       |
|                                   [응답 척도]                |
|                                   (정확히 몇 초/몇 %인가)    |
+--------------------------------------------------------------+
```

이 뼈대에서 가장 중요한 것은 <strong>응답 척도(Response Measure)</strong>다. 시스템이 살아남았다는 것만으로는 부족하며, 그 생존의 성적표가 숫자로 증명되어야 한다.

- **📢 섹션 요약 비유**: 복싱 선수의 맷집 테스트와 같다. "헤비급 챔피언(자극원)이 1라운드(환경)에 턱(대상)을 풀 파워로 때릴 때(자극), 쓰러지지 않고 버티며(응답) 카운트 5초 이내에 자세를 고쳐 잡는다(응답 척도)"라는 6단계 해부학적 내구성 측정표다.

---

## Ⅲ. 비교 및 연결

[품질 속성 시나리오](/studynote/12_it_management/05_security_compliance/993_process/)는 크게 3대 아키텍처 [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)([가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/), [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/), [보안성](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/))에서 빈번하게 사용되며, 각각 중점을 두는 자극과 척도의 방향이 다르다.

| 품질 [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) | 주요 자극 (Stimulus) | 핵심 응답 척도 (Response Measure) | 트레이드오프 연결 |
| :--- | :--- | :--- | :--- |
| <strong><a href="/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a> (<a href="/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">Availability</a>)</strong> | 하드웨어 고장, 네트워크 단절 | [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간([MTTR](/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/)), 가동률(99.99%) | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하 유발 ([이중화](/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 비용) |
| <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> (<a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">Performance</a>)</strong> | 대규모 동시 접속, 과부하 트래픽 | [지연 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)([Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)), [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)([Throughput](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)) | [보안성](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) 약화 유발 (복잡한 암호화 생략) |
| <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/">보안성</a> (<a href="/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/">Security</a>)</strong> | 비인가 접근, SQL [인젝션](/studynote/04_software_engineering/11_testing_validation/872_injection/) 공격 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유출 0 [Byte](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/), 100% 공격 차단 | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하 유발 (패킷 검사 오버헤드) |

이처럼 각 품질 [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)은 독립적으로 존재하지 않는다. [보안성](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) 시나리오를 엄격하게 잡으면(예: 모든 패킷의 3중 암호화), 필연적으로 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 시나리오의 응답 척도([지연 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))에 악영향을 미친다. 아키텍트는 시나리오 간의 충돌을 발견하고 우선순위를 조정하는 설계의 저울질(Trade-off Analysis)을 수행해야 한다.

- **📢 섹션 요약 비유**: 건물 설계 시 "지진에 5초 버틴다([가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/))", "10만 명이 에스컬레이터를 타도 대기 1분이다([성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/))", "도둑이 다이너마이트를 터뜨려도 금고가 안 뚫린다([보안성](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/))"라는 세 장의 서류가 서로 충돌(금고를 두껍게 하면 무게 때문에 지진에 취약해짐)할 때 타협점을 찾는 과정이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [품질 속성 시나리오](/studynote/12_it_management/05_security_compliance/993_process/)는 [ATAM](/studynote/04_software_engineering/04_testing_quality/229_atam_architecture_trade_off_analysis_method/)([Architecture](/studynote/12_it_management/05_security_compliance/319_architecture/) Tradeoff Analysis Method) 같은 아키텍처 평가 방법론의 가장 핵심적인 입력 자료로 사용된다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. **응답 척도가 정량적으로 측정 가능한가?** "빨리 처리된다", "안전하게 보호된다" 같은 모호한 표현이 단 하나라도 남아있으면 안 된다. 무조건 시간, 퍼센트, [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 등의 숫자로 변환해야 한다.
2. **비현실적인 환경 가정이 없는가?** "초당 10억 건의 공격이 들어올 때 0.001초 만에 방어한다"는 식의 예산을 무시한 과도한 시나리오는 폐기하거나 예산 제약을 환경 조건에 명시해야 한다.
3. <strong><a href="/studynote/04_software_engineering/03_design_architecture/173_stakeholder_identification_impact_matrix/">이해관계자</a> 전원이 동의했는가?</strong> 시나리오는 개발팀만 보는 것이 아니라 비즈니스 담당자, 인프라 운영자가 모두 동의하고 서명해야 하는 계약서다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 6가지 뼈대 중 '환경'과 '자극원'을 빼고 대충 "트래픽이 오면 1초 내에 처리한다"고 뭉뚱그려 작성하는 행위. (평소 트래픽인지 명절 폭주 트래픽인지 기준이 없어 평가 불능에 빠진다.)
- 모든 시나리오의 요구 수준을 최고 등급(예: [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 99.9999%)으로 설정해 구현 비용을 천문학적으로 팽창시키는 설계.

- **📢 섹션 요약 비유**: [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) [테스트 시나리오](/studynote/04_software_engineering/11_testing_validation/834_test_scenario/) 없이 차를 팔면, 고객이 비포장도로에서 시속 200km를 밟고 사고가 난 뒤 제조사 탓을 한다. 시나리오는 "포장도로(환경)에서 고급 휘발유(자극원)를 넣었을 때만 이 연비가 나온다"는 법적 면책 조항이자 방어선이다.

---

## Ⅴ. 기대효과 및 결론

[품질 속성 시나리오](/studynote/12_it_management/05_security_compliance/993_process/)를 도입하면 요구사항의 모호성이 완벽히 제거되어, 아키텍처 설계의 방향성이 뚜렷해지고 테스트 자동화의 기준점이 마련된다. 또한, 시스템의 한계점을 명확히 인지하게 되어 향후 확장이나 장애 발생 시 책임 소재를 명확히 가릴 수 있다.

미래의 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 환경에서는 이러한 시나리오들이 단순한 문서로 남는 것이 아니라, [카오스 엔지니어링](/studynote/01_computer_architecture/15_advanced_topics/751_chaos_engineering/)([Chaos 엔진ering](/studynote/01_computer_architecture/15_advanced_topics/751_chaos_engineering/))이나 자동화된 [부하 테스트](/studynote/04_software_engineering/11_testing_validation/838_load_test/) 스크립트([Code](/studynote/02_operating_system/02_process_thread/082_process_memory_structure/))로 직접 변환되어 실시간으로 시스템을 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 도구로 진화하고 있다. 결론적으로 [품질 속성 시나리오](/studynote/12_it_management/05_security_compliance/993_process/)는 "개발자와 사장님이 동일한 숫자를 보며 합의하게 만드는 유일한 통역기"로 기억해야 한다.

- **📢 섹션 요약 비유**: 눈대중으로 대충 지은 집은 태풍이 오면 무너지지만, "풍속 50m/s에서 진동 3cm 이하"라는 정확한 시나리오 수치에 맞춰 지은 집은 절대 무너지지 않는 것과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| <strong>비기능적 요구사항 (<a href="/studynote/04_software_engineering/03_design_architecture/133_non_functional_requirements/">NFR</a>)</strong> | [품질 속성 시나리오](/studynote/12_it_management/05_security_compliance/993_process/)가 구체화하고자 하는 대상의 원형 ([성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/), [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/), [보안성](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) 등) |
| <strong><a href="/studynote/04_software_engineering/04_testing_quality/229_atam_architecture_trade_off_analysis_method/">ATAM</a> (아키텍처 평가)</strong> | 작성된 시나리오들을 기반으로 아키텍처의 트레이드오프와 위험 요소를 평가하는 감리 기법 |
| <strong><a href="/studynote/12_it_management/02_itsm_itil/869_sla/">SLA</a> (<a href="/studynote/12_it_management/02_itsm_itil/869_sla/">Service Level Agreement</a>)</strong> | 시나리오의 응답 척도가 실제 비즈니스 계약으로 발전한 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준 협약 |
| <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/751_chaos_engineering/">카오스 엔지니어링</a> (<a href="/studynote/01_computer_architecture/15_advanced_topics/751_chaos_engineering/">Chaos 엔진ering</a>)</strong> | [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 시나리오(장애 유발)를 실제 운영 환경에 주입하여 응답 척도를 실증하는 테스트 기법 |

### 📈 관련 키워드 및 발전 흐름도

```text
비기능적 요구사항 (모호한 형용사)
    |
    v
품질 속성 시나리오 (6요소 구체화 및 정량화)
    |
    +---------+---------+
    v         v         v
 가용성 시나리오 성능 시나리오 보안성 시나리오
(MTTR/장애복구) (TPS/응답시간) (침입차단율)
    |         |         |
    v         v         v
ATAM 아키텍처 평가 (트레이드오프 분석)
    |
    v
카오스 엔지니어링 및 자동화된 인프라 테스트 (Code화)
```

### 👶 어린이를 위한 3줄 비유 설명

1. 엄마가 "방 좀 깨끗하게 치워!"라고 하면 얼마나 치워야 깨끗한지 몰라서 맨날 혼나요.
2. 그래서 "저녁 6시까지(환경), 내가(자극원), 청소기를 돌려서(자극), 거실 바닥에(대상), 장난감이 하나도 없게(응답) 치우고, 엄마한테 100점을 받겠다(응답 척도)!"라고 약속을 적었어요.
3. 이렇게 6가지 규칙으로 정확하게 약속을 정해서 싸우지 않게 만드는 종이가 '[품질 속성 시나리오](/studynote/12_it_management/05_security_compliance/993_process/)'랍니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 134 / 530

<- **이전**: [90. 아키텍처 드라이버 (Architecture Drivers) - 시스템 설계 핵심 요구사항](/studynote/11_design_supervision/02_architecture_principles/090_architecture_drivers_quality_attributes_constraints/)
**다음**: [92. 아키텍처 평가 방법론 - ATAM (Architecture Trade-off Analysis Method)](/studynote/11_design_supervision/02_architecture_principles/092_atam_architecture_tradeoff_analysis_method/) ->

---
