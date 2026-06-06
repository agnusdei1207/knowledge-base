---
title: "011. Backward Chaining"
date: "2024-05-24"
description: "가설이나 목표에서 출발하여 조건 데이터를 역으로 검증해 나가는 전문가 시스템의 목표 주도 추론 방식"
tags:
  - "ai"
---
# [11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/). 후향 추론 (Backward [Chaining](/studynote/12_it_management/03_ea_isp/887_chaining/))
#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 목표(Goal)나 가설을 먼저 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)하고, 이를 증명하기 위해 필요한 조건(Premise)을 규칙 베이스에서 역으로 탐색하는 목표 주도(Goal-Driven) 추론 메커니즘.
> 2. **가치**: 증명하고자 하는 가설과 관련 없는 규칙의 탐색을 배제하여 연산 효율을 극대화하며, 왜 그런 결론이 도출되었는지 설명(Explanation)하기 용이.
> 3. **융합**: [전문가 시스템](/studynote/10_ai/03_llm_nlp/233_expert_system/)(MYCIN 등)의 진단 엔진, 선언적 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) 프로그래밍(Prolog), 사이버 보안의 위협 트리 분석 등 방대한 인과관계 역추적 분야에서 핵심 역할을 수행.

---

### Ⅰ. 개요 및 필요성 ([Context](/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)
[전문가 시스템](/studynote/10_ai/03_llm_nlp/233_expert_system/)([Expert System](/studynote/10_ai/03_llm_nlp/233_expert_system/))은 인간 전문가의 지식을 규칙(Rule) 형태로 저장하고 이를 통해 결론을 도출한다. 이때 방대한 [지식 베이스](/studynote/10_ai/01_ai_basics/008_knowledge_base_inference_engine/)([Knowledge Base](/studynote/10_ai/01_ai_basics/008_knowledge_base_inference_engine/))에서 결론을 찾는 방법론 중 하나가 바로 후향 추론(Backward [Chaining](/studynote/12_it_management/03_ea_isp/887_chaining/))이다.
[초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시스템은 주어진 모든 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 바탕으로 결론을 도출하는 [전향 추론](/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/)([Forward Chaining](/studynote/10_ai/01_ai_basics/010_forward_chaining/))을 사용했다. 그러나 [전향 추론](/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/)은 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 많을 경우, 목표와 무관한 수많은 중간 결론까지 도출하며 컴퓨팅 자원을 낭비하는 문제(Rule Explosion)가 있었다.
이를 해결하기 위해 등장한 후향 추론은, "A라는 가설이 참인가?"라는 명확한 목표를 먼저 세운 뒤, A가 참이 되기 위한 조건 B와 C를 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하고, 다시 B와 C의 조건을 역으로 추적하는 방식을 취한다. 이는 특정 질병을 의심하고 그 증상이 있는지 역으로 문진하는 의사의 진단 과정과 동일하다.

이 도식은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 너무 많을 때 목표 지향적 탐색이 왜 자원을 덜 소모하는지를 보여주는 개념적 대조도이다.
```text
+--------------------------------------------------------+
| [전향 추론: 데이터 주도]                                |
| Data(A, B, C...) -> Rule 평가 폭발 -> 무관한 결론들 생성  |
|                                                        |
| [후향 추론: 목표 주도]                                  |
| Goal(X) 설정 -> X를 위한 조건 Rule 추적 -> 필요 Data만 요청|
+--------------------------------------------------------+
```
이 흐름의 핵심은 출발점의 차이다. [전향 추론](/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/)은 입력된 모든 사실에서 파생될 수 있는 모든 가지를 탐색하지만, 후향 추론은 오직 '목표'와 연결된 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 경로만 활성화한다. 따라서 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집 비용이 비싸거나, 가능한 결론의 수가 입력 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)보다 적을 때 압도적인 효율을 발휘한다.

📢 **섹션 요약 비유**: 마치 수백 명의 용의자([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 전부 조사하는 대신, 유력한 용의자 한 명(목표 가설)을 찍어두고 그의 알리바이를 역으로 캐묻는 표적 수사 방식과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
후향 추론 엔진은 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)([Stack](/studynote/08_algorithm_stats/04_datastructure/057_stack/)) 기반의 [깊이 우선 탐색](/studynote/08_algorithm_stats/03_graph_search/034_dfs/)([DFS](/studynote/08_algorithm_stats/03_graph_search/034_dfs/)) 구조를 활용하여 목표를 하위 목표(Sub-goal)로 쪼개며 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한다.

**후향 추론 시스템의 주요 구성 요소**
| 구성 요소 | 역할 | 내부 동작 |
|:---|:---|:---|
| <strong>Goal <a href="/studynote/08_algorithm_stats/04_datastructure/057_stack/">Stack</a></strong> | [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)해야 할 목표/가설 보관 | 현재 목표를 Pop하고, 필요 조건(하위 목표)을 Push하는 LIFO 구조 |
| **Rule Base** | [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 지식이 저장된 규칙 셋 | `IF 조건 THEN 결과` 형태의 규칙을 저장 (THEN 절을 먼저 매칭) |
| **Working Memory** | 이미 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)된 사실(Fact) 보관 | 평가 중인 조건이 이미 참/거짓으로 판명되었는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 캐시 |
| **Inference 엔진** | 역추적 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) 제어 | 규칙 매칭(Pattern Matching), 변수 바인딩(Unification), [백트래킹](/studynote/08_algorithm_stats/01_basics/010_backtracking/)([Backtracking](/studynote/08_algorithm_stats/01_basics/010_backtracking/)) 수행 |
| **User Interface** | 부족한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 요청 | 작업 메모리에 없는 사실이 필요할 때 사용자에게 질문(예/아니오)을 던짐 |

다음은 후향 추론 엔진이 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)과 작업 메모리를 이용해 가설을 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)해 나가는 순차 흐름도이다.
```text
[초기 상태: Goal(Z) 검증 요청]
   v
[Rule Base 검색] : THEN 절에 Z가 있는 규칙 R1 (IF X AND Y THEN Z) 발견
   v
[Sub-Goal 분할] : X와 Y를 새로운 목표로 Goal Stack에 Push
   v
[작업 메모리 확인] : X가 작업 메모리에 있는가?
   +- (Yes) -> X 증명 완료. 다음 목표 Y 검사.
   +- (No)  -> X를 결과로 갖는 다른 Rule 검색
                 또는 사용자에게 질의 (Ask User)
   v
[Backtracking] : 만약 X를 증명할 수 없으면 이전 분기점으로 회귀하여 다른 규칙 탐색
```
이 흐름의 핵심은 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 단계가 철저히 하향식([Top-Down](/studynote/04_software_engineering/12_testing_maintenance/402_top_down_integration/))으로 이루어지며, 작업 메모리(Working Memory)가 단기 캐시 역할을 하여 중복 질문을 방지한다는 점이다. 특히, 특정 하위 목표를 증명할 수 없게 되면 즉시 해당 경로를 폐기하고 다른 대안 규칙으로 되돌아가는 [백트래킹](/studynote/08_algorithm_stats/01_basics/010_backtracking/)([Backtracking](/studynote/08_algorithm_stats/01_basics/010_backtracking/)) 메커니즘이 필수적으로 동작한다. 이로 인해 메모리 오버헤드가 적고 불필요한 추론 가지가 조기에 차단된다.

📢 **섹션 요약 비유**: 마치 거대한 미로의 출구(목표)에 서서, 입구([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) 쪽으로 역방향 발자국을 따라가며 막힌 길을 하나씩 지워나가는 과정과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
[AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 시스템의 추론 방식을 설계할 때 가장 큰 고민은 [전향 추론](/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/)과 후향 추론 중 무엇을 선택할 것인가이다. 이는 문제의 공간적 형태에 따라 결정된다.

<strong><a href="/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/">전향 추론</a> vs 후향 추론 비교 매트릭스</strong>
| 비교 항목 | [전향 추론](/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/) ([Forward Chaining](/studynote/10_ai/01_ai_basics/010_forward_chaining/)) | 후향 추론 (Backward [Chaining](/studynote/12_it_management/03_ea_isp/887_chaining/)) | 판단 포인트 |
|:---|:---|:---|:---|
| **시작점** | 알려진 사실 (Facts) | [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)할 가설 (Goal) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 많은가 vs 목표가 명확한가 |
| **탐색 방식** | 상향식 ([Bottom-Up](/studynote/04_software_engineering/12_testing_maintenance/403_bottom_up_integration/)), 너비 우선 | 하향식 ([Top-Down](/studynote/04_software_engineering/12_testing_maintenance/402_top_down_integration/)), 깊이 우선 | 모든 결과 예측 vs 단일 가설 증명 |
| <strong>적합한 <a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a></strong> | 시스템 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링, 프로세스 제어 | 질병 진단, 고장 수리, 디버깅 | 반응형 처리인가 vs 분석형 처리인가 |
| **사용자 개입** | 사전에 모든 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 입력해야 함 | 필요한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 그때그때 질문함 | 대화형 인터페이스 요구 여부 |

다음은 두 추론 방식의 [상태 공간 탐색](/studynote/10_ai/03_llm_nlp/236_state_space_search_dfs_bfs/) 구조의 차이를 보여주는 비교도이다.
```text
[전향 추론: 팬-아웃(Fan-out) 구조]         [후향 추론: 팬-인(Fan-in) 구조]
  Fact 1 -+                              Goal -+- SubGoal 1 - Fact A
          +-> Rule 1 -+                        +- SubGoal 2 - Fact B
  Fact 2 -+           +-> 결론(다수)                (필요한 사실만 선택적 탐색)
                      |
  Fact 3 ---> Rule 2 -+
```
이 방식의 핵심 차이는 분기 방향이다. [전향 추론](/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/)은 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 사실들이 조합되어 수많은 파생 결과를 낳는 구조(팬아웃)이므로 설계 플래닝 등에 유리하다. 반면 후향 추론은 단일 결론에서 시작해 소수의 필수 원인으로 좁혀 들어가는 [팬인](/studynote/04_software_engineering/04_testing_quality/197_fan_in_fan_out/)([Fan-in](/studynote/04_software_engineering/04_testing_quality/197_fan_in_fan_out/)) 구조이므로 진단과 디버깅에 압도적으로 유리하다. 실무에서는 두 방식을 혼합한 하이브리드 추론 엔진을 구축하여, 중요 이벤트는 전향적으로 감지하고 원인 분석은 후향적으로 수행하기도 한다.

📢 **섹션 요약 비유**: [전향 추론](/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/)이 냉장고에 있는 모든 재료([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 꺼내놓고 "무엇을 만들 수 있을까?" 고민하는 요리사라면, 후향 추론은 "김치찌개를 만들자!"(목표)라고 정한 뒤 김치와 돼지고기가 있는지 냉장고를 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 요리사입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
실무에서 추론 엔진을 도입할 때, 문제의 성격에 따라 후향 추론의 적용 여부를 신중히 판단해야 한다.

<strong>실무 <a href="/studynote/14_data_engineering/03_ml_dl_llm/124_decision_tree/">의사결정 트리</a> (<a href="/studynote/14_data_engineering/03_ml_dl_llm/124_decision_tree/">Decision Tree</a>)</strong>
```text
[문제 정의]
   v
[Q1. 가능한 결과(결론)의 수가 초기 데이터의 수보다 적은가?]
 +-- (No) -> 전향 추론 도입 고려 (예: 모든 조건에 따른 시스템 제어)
 +-- (Yes) -> [Q2. 사용자에게 질의응답을 통해 데이터를 점진적으로 얻을 수 있는가?]
       +-- (No) -> 초기 일괄 배치 처리, 하이브리드 엔진 검토
       +-- (Yes) -> 후향 추론 최적 적용 대상 (도입 확정)
```
이 [의사결정 트리](/studynote/14_data_engineering/03_ml_dl_llm/124_decision_tree/)의 핵심은 '[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집 비용'과 '결론의 수렴성'이다. 만약 모든 센서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 실시간으로 수집되는 [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링 환경이라면 [전향 추론](/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/)이 맞다. 하지만 사용자가 직접 증상을 입력해야 하는 헬스케어 챗봇이나 헬프데스크 시스템에서는, 쓸데없는 질문을 피하기 위해 반드시 후향 추론을 채택해야 한다.

<strong>실무 <a href="/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a> (주의사항)</strong>
- **무한 루프의 늪**: 규칙이 상호 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)(A가 B를 요구하고, B가 다시 A를 요구)하게 작성된 경우, 후향 추론 엔진은 [깊이 우선 탐색](/studynote/08_algorithm_stats/03_graph_search/034_dfs/)의 특성상 무한 루프에 빠질 위험이 크다. 따라서 규칙 베이스 설계 시 순환 [종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/)(Circular Dependency) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)기를 반드시 도입해야 한다.
- **불필요한 목표 분할**: 성공 가능성이 거의 없는 목표를 너무 깊게 탐색하면 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 저하된다. 이를 막기 위해 [휴리스틱](/studynote/02_operating_system/03_cpu_scheduling/210_heuristics_scheduling/)이나 우선순위 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)를 두어 유력한 하위 목표부터 탐색하도록 엔진을 최적화해야 한다.

📢 **섹션 요약 비유**: 진료실 의사가 환자의 모든 신체 수치를 한 번에 검사(전향)하면 비용이 감당 안 되듯, 실무 시스템도 필요한 질문만 던져 네트워크 통신 비용과 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호출을 최소화하는 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 필수적입니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)
후향 추론은 전통적인 규칙 기반 AI를 넘어, 오늘날 설명 가능한 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)([XAI](/studynote/12_it_management/05_security_compliance/227_xai_explainable_ai_lime_shap/))와 결합하여 새로운 전기를 맞이하고 있다.

| 기대 효과 | 도입 전 (단순 탐색) | 도입 후 (후향 추론 적용) |
|:---|:---|:---|
| **연산 효율성** | 모든 규칙 평가로 인한 CPU/메모리 병목 | 목표와 연관된 규칙만 평가하여 리소스 70% 이상 절감 |
| **사용자 경험** | 불필요한 대량의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 입력 요구 | 필요한 정보만 대화형으로 문답하여 피로도 감소 |
| **설명 가능성** | 왜 이 결론이 나왔는지 역추적 불가 | Goal [Stack](/studynote/08_algorithm_stats/04_datastructure/057_stack/) 궤적을 통해 명확한 인과관계 추적 및 로깅 가능 |

**미래 전망**
최근 초거대 언어 모델([LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/))이 [환각](/studynote/06_ict_convergence/04_ai_llm/275_react_framework/)([Hallucination](/studynote/12_it_management/05_security_compliance/345_llm_foundation_model_hallucination/)) 현상을 극복하기 위해, 프롬프트상에서 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 요구받을 때 이러한 후향 추론 메커니즘(예: Tree-of-Thoughts에서 가설 역검증)을 암묵적으로 모방하는 추세가 늘고 있다. 향후 신경망의 직관적 결론을 후향 추론 심볼릭 엔진이 사후 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 뉴로-심볼릭 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)(Neuro-Symbolic [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)) 아키텍처의 핵심 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/)로 자리 잡을 것이다.

📢 **섹션 요약 비유**: 블랙박스처럼 결과를 뱉어내는 현대 딥러닝이 '천재적인 직관'이라면, 후향 추론은 그 직관이 수학적으로 맞는지 꼼꼼히 역산해보는 '냉철한 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)관'의 역할로 부활하고 있습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/">전향 추론</a> (<a href="/studynote/10_ai/01_ai_basics/010_forward_chaining/">Forward Chaining</a>)</strong> | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 출발해 결론을 도출하는 반대 방향 추론 방식 |
| **규칙 베이스 (Rule Base)** | IF-THEN 형식으로 지식을 표현하는 후향 추론의 지식 저장소 |
| <strong>Goal <a href="/studynote/08_algorithm_stats/04_datastructure/057_stack/">Stack</a></strong> | 현재 증명해야 할 하위 목표들을 쌓아두는 후향 추론의 핵심 자료구조 |
| <strong>설명 가능한 <a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> (<a href="/studynote/12_it_management/05_security_compliance/227_xai_explainable_ai_lime_shap/">XAI</a>)</strong> | 후향 추론의 추적 가능한 인과 경로를 현대 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 해석 가능성에 활용 |
| <strong>뉴로-심볼릭 <a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> (Neuro-Symbolic <a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a>)</strong> | LLM의 직관적 결론을 심볼릭 역추론으로 사후 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 하이브리드 아키텍처 |
### 📈 관련 키워드 및 발전 흐름도

```text
[목표 설정 (Goal Setting) — 도달하고자 하는 결론 명시]
    |
    v
[후향 추론 엔진 (Backward Chaining Engine) — 목표를 하위 목표로 재귀 분해]
    |
    v
[규칙 베이스 (Knowledge Base / Rule Base) — 조건-결론 규칙 저장소 조회]
    |
    v
[전향 추론 (Forward Chaining) — 데이터 주도 보완 또는 하이브리드 적용]
    |
    v
[뉴로-심볼릭 AI (Neuro-Symbolic AI) — LLM 직관을 심볼릭 역추론으로 검증]
```

이 흐름은 목표 지향적 역추론이 규칙 기반 AI를 거쳐 현대 설명 가능한 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)([XAI](/studynote/12_it_management/05_security_compliance/227_xai_explainable_ai_lime_shap/))로 진화하는 맥락을 나타낸다.

### 👶 어린이를 위한 3줄 비유 설명

1. 후향 추론은 "범인을 먼저 정해두고" 단서를 역으로 맞춰가는 탐정 수사 방법이에요.
2. 냉장고에 있는 재료를 모두 꺼내 보는 대신, "카레를 만들자!"고 결정한 뒤 감자·당근만 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 현명한 요리사랍니다.
3. 불필요한 조사를 하지 않아서 컴퓨터가 빠르게 정답을 찾을 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 11 / 420

<- **이전**: [10. 전향 추론 (Forward Chaining) - 데이터에서 시작하여 결론 도출 (데이터 주도)](/studynote/10_ai/01_ai_basics/010_forward_chaining/)
**다음**: [12. 퍼지 논리 (Fuzzy Logic) - 0과 1 사이의 확률적 연속값(소속도)을 이용해 애매한 개념 처리 (Zadeh 제안)](/studynote/10_ai/01_ai_basics/012_fuzzy_logic/) ->

---
