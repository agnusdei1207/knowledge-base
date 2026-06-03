+++
title = "108. 단순성 유지 원칙 (KISS, Keep It Simple, Stupid)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [KISS](/knowledge-base/studynote/04_software_engineering/04_testing_quality/249_kiss_keep_it_simple_stupid/) (Keep It Simple, Stupid, 단순성 유지 원칙)는 소프트웨어 설계와 구현에서 불필요한 복잡성을 제거하고 가능한 가장 단순한 해법을 선택해야 한다는 원칙이며, 복잡성 자체가 결함의 온상이 된다는 관찰에서 출발한다.
> 2. **가치**: 단순한 코드는 읽기 쉽고, 테스트하기 쉽고, 수정하기 쉬우며, 새로운 팀원이 온보딩하는 시간을 단축시킨다. 복잡한 해법 대신 단순한 해법을 택하는 훈련이 전체 팀의 생산성을 높인다.
> 3. **판단 포인트**: 단순성은 기능의 제거가 아니라 불필요한 복잡성의 제거이므로, "이 복잡함이 실제 문제를 해결하기 위해 필수적인가, 아니면 설계자가 자의적으로 추가한 우발적 복잡성(accidental complexity)[인가](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/)"를 구분해야 한다.

---

## Ⅰ. 개요 및 필요성

[KISS](/knowledge-base/studynote/04_software_engineering/04_testing_quality/249_kiss_keep_it_simple_stupid/) 원칙은 1960년대 미 해군 수석 엔지니어 켈리 존슨(Kelly Johnson)이 항공기 설계 원칙으로 제시한 것에서 유래했다. 항공기는 전장에서 평범한 기술자가 간단한 공구만으로 수리할 수 있어야 한다는 실용적 요구에서 비롯됐다. 소프트웨어 공학에서도 이 철학은 그대로 적용된다.

소프트웨어의 복잡성에는 두 종류가 있다. 첫째, 본질적 복잡성(essential complexity)은 문제 자체가 복잡한 경우로 제거할 수 없다. 둘째, 우발적 복잡성(accidental complexity)은 설계자가 불필요하게 추가한 복잡성으로 KISS가 제거해야 할 대상이다. 과도한 [디자인 패턴](/knowledge-base/studynote/04_software_engineering/04_testing_quality/251_design_patterns_gof_overview/) 적용, 불필요한 계층 추가, 추측성 기능 구현이 대표적이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">복잡성의 두 유형과 KISS 적용 대상</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">복잡성 전체</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">본질적 복잡성 우발적 복잡성</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(Essential Complexity) (Accidental Complexity)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">문제 자체의 속성 설계자가 추가한 복잡성</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 수용·관리 필요 → KISS로 제거 대상</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">과도한 패턴 불필요 계층 추측성 기능</div></div>
</div>
</div>



[KISS](/knowledge-base/studynote/04_software_engineering/04_testing_quality/249_kiss_keep_it_simple_stupid/) 없이 설계가 진행되면 코드는 점점 "영리한 트릭"으로 가득 찬 블랙박스가 된다. 팀원이 코드를 이해하는 데 드는 시간이 늘어나고, 버그가 발생했을 때 원인 추적이 어려워진다.

- **📢 섹션 요약 비유**: 조종사가 긴급 상황에서 항공기를 수리할 때 복잡한 특수 공구가 필요하면 생존율이 낮아진다. 핵심 기능을 단순한 구조로 만들어야 위기에서도 대처가 빠르다.

---

## Ⅱ. 아키텍처 및 핵심 원리

KISS를 실현하는 구체적 기법으로는 ① 명확한 함수명으로 의도를 전달하여 주석을 줄이기, ② 한 함수가 한 가지 일만 하게 분리하기([SRP](/knowledge-base/studynote/04_software_engineering/04_testing_quality/243_srp_single_responsibility_principle/), [Single Responsibility Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/243_srp_single_responsibility_principle/)), ③ 조건문 중첩을 줄이기 위한 Early Return 패턴, ④ [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 계층을 필요 이상으로 쌓지 않기 등이 있다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 함수 설계 | 50줄 이상 함수, 다중 책임 | 함수 분리, Early Return |
| 클래스 설계 | 과도한 [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) 깊이 | 컴포지션 우선, 계층 축소 |
| 아키텍처 | 필요 없는 계층 추가 | 계층 통합, [직접 통신](/knowledge-base/studynote/02_operating_system/02_process_thread/120_direct_communication/) |
| [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 영리하지만 해독 불가한 코드 | [가독성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/333_readability_vs_efficiency/) 우선 명료한 구현 |



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Early Return 패턴: 복잡한 중첩 조건 제거</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Before (복잡한 중첩): After (KISS 적용):</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">if (user != null) { if (user == null) return null;</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">if (user.isActive()) { if (!user.isActive()) return;</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">if (user.hasRole()) { if (!user.hasRole()) return;</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">doProcess(); doProcess();</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">}</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">}</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">}</div></div>
</div>
</div>



측정 기준으로 순환 복잡도(Cyclomatic Complexity)가 있다. 일반적으로 메서드당 복잡도가 10을 초과하면 단순화 검토가 필요하고, 15를 초과하면 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)이 강하게 권장된다. [SonarQube](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/079_sonarqube/) 등의 [정적 분석](/knowledge-base/studynote/04_software_engineering/06_software_architecture/331_static_analysis/) 도구로 자동 측정이 가능하다.

- **📢 섹션 요약 비유**: 요리 레시피가 복잡할수록 실수가 생긴다. 파스타 삶기는 "물 끓이고, 면 넣고, 8분 기다리고, 건지기"면 충분하다. 이 단계에 전처리·온도 제어 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 끼워 넣으면 오히려 망친다.

---
## Ⅲ. 비교 및 연결

KISS는 [YAGNI](/knowledge-base/studynote/11_design_supervision/06_exam_summary/362_yagni/) (You Aren't Gonna Need It, 불필요한 기능 구현 금지)와 자주 함께 언급되지만, 적용 시점과 관점이 다르다.

| 비교 축 | A | B |
|:---|:---|:---|
| **초점** | 현재 존재하는 복잡성 제거 | 미래 추가를 위한 과도한 설계 방지 |
| **적용 대상** | 구현 코드, 아키텍처 구조 | 기능 범위, 설계 확장성 |
| **발동 시점** | 코드 작성 및 리뷰 시 | 기능 기획 및 설계 시 |
| **방지하는 문제** | 우발적 복잡성(이해·유지보수 비용) | 과도한 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)([YAGNI](/knowledge-base/studynote/11_design_supervision/06_exam_summary/362_yagni/) 위반) |

KISS는 또한 소프트웨어 감리(Software [Audit](/knowledge-base/studynote/12_it_management/05_security_compliance/363_audit/)) 관점에서 중요한 품질 지표다. 감리인은 아키텍처 복잡도가 요구사항 대비 과도하게 설계되었는지를 평가하며, [KISS](/knowledge-base/studynote/04_software_engineering/04_testing_quality/249_kiss_keep_it_simple_stupid/) 위반(과도한 패턴 적용, 불필요한 계층)을 아키텍처 결함으로 지적할 수 있다.

- **📢 섹션 요약 비유**: KISS는 현재 테이블이 너무 복잡하게 만들어졌다는 것을 알아채는 눈이고, YAGNI는 아직 사용하지 않을 서랍을 미리 만들지 않겠다는 결심이다. 둘 다 "필요한 것만"을 지향하지만 다른 순간에 작동한다.

---
## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [KISS](/knowledge-base/studynote/04_software_engineering/04_testing_quality/249_kiss_keep_it_simple_stupid/) 위반의 가장 흔한 사례는 "[디자인 패턴](/knowledge-base/studynote/04_software_engineering/04_testing_quality/251_design_patterns_gof_overview/) 강박"이다. 현재 구조에서 단순 if-else로 충분한 상황에서 [Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 패턴·Factory 패턴을 억지로 끼워 넣는 것이 대표적이다. [코드 리뷰](/knowledge-base/studynote/04_software_engineering/06_software_architecture/330_code_review/)에서 "이 패턴이 지금 당장 어떤 문제를 해결하고 있는가?"라는 질문이 KISS의 리트머스 시험지다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 이 코드를 처음 보는 동료가 10분 이내에 이해할 수 있는가?
2. 순환 복잡도가 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) 이하인가?
3. 각 함수·클래스가 하나의 명확한 역할만 수행하는가?
4. 적용된 [디자인 패턴](/knowledge-base/studynote/04_software_engineering/04_testing_quality/251_design_patterns_gof_overview/)이 현재 요구사항에서 실제로 필요한가?
5. 계층이나 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)를 하나 제거해도 기능상 문제가 없는 경우가 있는가?

- **📢 섹션 요약 비유**: 좋은 의사는 가장 간단한 치료법부터 시도한다. 두통 환자에게 바로 뇌수술을 권하지 않는다. 코드도 가장 단순한 해법이 작동하면, 복잡한 패턴을 굳이 적용할 이유가 없다.

---

## Ⅴ. 기대효과 및 결론

KISS를 지속적으로 적용하면 코드베이스의 [인지 부하](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/686_cognitive_load_team_topologies/)([cognitive load](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/686_cognitive_load_team_topologies/))가 줄어들고 신규 팀원의 온보딩 속도가 빨라진다. 버그 발생 시 원인 추적 시간이 단축되고, [테스트 케이스](/knowledge-base/studynote/04_software_engineering/11_testing_validation/441_test_case/) 작성이 쉬워진다. 유지보수 비용의 70% 이상이 코드 이해에서 발생한다는 연구 결과를 고려하면, KISS의 직접적 경제 효과는 상당하다.

한계는 단순성과 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 간의 트레이드오프다. [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화를 위한 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 조작, 캐시 계층 추가, 비동기 처리는 코드를 복잡하게 만들지만 필수적인 경우가 많다. 이때는 "[성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 목표를 위한 필수 복잡성"으로 문서화하여 본질적 복잡성으로 분류해야 한다.

미래 방향으로는 ① [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 코드 보조 도구가 복잡한 코드를 자동으로 단순화하는 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 제안, ② 저코드·노코드(Low-code/No-code) 플랫폼의 [KISS](/knowledge-base/studynote/04_software_engineering/04_testing_quality/249_kiss_keep_it_simple_stupid/) 철학 구현, ③ 클라우드 함수([FaaS](/knowledge-base/studynote/12_it_management/05_security_compliance/342_faas/)) 단위의 극단적 단순화가 트렌드를 이루고 있다.

KISS는 "영리함의 [억제](/knowledge-base/studynote/09_security/13_secops_ir_forensics/656_ir_containment/)"가 아니라 "진짜 실력자의 선택"이다. 복잡한 코드는 누구나 쓸 수 있지만, 단순하고 명료한 코드는 깊은 이해에서 나온다.

- **📢 섹션 요약 비유**: 세계 최고의 요리사는 재료 본연의 맛을 살리는 단순한 요리를 만든다. 복잡한 소스와 장식은 실력 부족을 가리기 위한 허세일 때가 많다.

---

### 📌 관련 개념 맵

[복잡성 관리] → KISS] → SRP] → [순환 복잡도 측정] → [리팩토링] → [코드 리뷰]

| 개념 | 연결 포인트 |
|:---|:---|
| [YAGNI](/knowledge-base/studynote/11_design_supervision/06_exam_summary/362_yagni/) | KISS와 함께 오버엔지니어링을 방지하는 상호 보완 원칙 |
| [SRP](/knowledge-base/studynote/04_software_engineering/04_testing_quality/243_srp_single_responsibility_principle/) ([Single Responsibility Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/243_srp_single_responsibility_principle/)) | 단일 책임이 KISS의 구체적 함수·클래스 수준 적용 형태 |
| 순환 복잡도 | [KISS](/knowledge-base/studynote/04_software_engineering/04_testing_quality/249_kiss_keep_it_simple_stupid/) 준수 여부를 정량적으로 측정하는 코드 [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) |
| [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) | [KISS](/knowledge-base/studynote/04_software_engineering/04_testing_quality/249_kiss_keep_it_simple_stupid/) 위반을 교정하는 구체적 기법 집합 |

### 📈 관련 키워드 및 발전 흐름도

[우발적 복잡성 인식] → KISS 원칙 정립] → SRP·[리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 기법] → [순환 복잡도 자동 측정] → AI 기반 코드 단순화 제안] → [Low-code 플랫폼]

### 👶 어린이를 위한 3줄 비유 설명

1. 레고로 자동차를 만들 때 필요 없는 블록을 잔뜩 쌓으면 무거워서 잘 굴러가지 않아요.
2. KISS는 꼭 필요한 바퀴, 차체, 엔진 블록만 사용하는 원칙이에요.
3. 단순하게 만들어야 빠르고, 고장도 잘 안 나고, 친구에게 설명하기도 쉬워요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 158 / 530

← **이전**: [107. DRY 원칙 (Don't Repeat Yourself) - 코드 중복 방지 (데이터 일관성 보장)](/knowledge-base/studynote/11_design_supervision/09_design_principles/107_dry_principle/)
**다음**: [108. KISS 원칙 (Keep It Simple, Stupid)](/knowledge-base/studynote/11_design_supervision/09_design_principles/108_kiss_principle/) →

---
