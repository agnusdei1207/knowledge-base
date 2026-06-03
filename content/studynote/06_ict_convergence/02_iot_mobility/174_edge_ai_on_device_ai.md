+++
title = "174. 엣지 AI (Edge AI) 및 온디바이스 AI 아키텍처"
date = 2026-05-06

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 엣지 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) (Edge [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/))는 [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) ([AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/), [Artificial Intelligence](/knowledge-base/studynote/10_ai/01_ai_basics/001_artificial_intelligence/)) 추론을 원격 클라우드가 아니라 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 생성되는 가까운 위치에서 수행하는 구조이며, 온디바이스 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) ([On-Device AI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/635_on_device_ai/))는 그중에서도 <strong>단말 내부에서 직접 실행하는 가장 극단적인 형태</strong>다.
> 2. **가치**: 지연시간, 네트워크 비용, 프라이버시 노출, 오프라인 취약성을 동시에 줄일 수 있어 자율주행, 모바일 번역, 산업 비전, 헬스케어 단말에서 강한 설득력을 가진다.
> 3. **판단 포인트**: 엣지 채택의 핵심은 "모든 AI를 로컬에 넣을 수 있는가"가 아니라, <strong>응답시간·<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 민감도·배터리·발열·모델 크기</strong>를 함께 보고 클라우드와 역할을 어디서 나눌지 결정하는 데 있다.

---

## Ⅰ. 개요 및 필요성

엣지 AI는 센서가 만든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 멀리 있는 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)로 보내기 전에, 카메라·스마트폰·로봇·차량·공장 게이트웨이 같은 말단 또는 근접 노드에서 먼저 추론하는 아키텍처다. 온디바이스 AI는 이 중에서도 <strong>스마트폰, 웨어러블, 차량 제어기처럼 사용자가 들고 있거나 직접 탑승한 장치 내부에서 모델이 실행되는 경우</strong>를 가리킨다.

이 개념이 중요해진 이유는 클라우드 왕복이 너무 비싸기 때문이다. 시속 100km로 달리는 차량은 100ms 동안 약 2.8m를 이동한다. 충돌 회피, 음성 인터페이스, 공장 로봇 정지처럼 수십 밀리초 단위의 판단이 필요한 업무에서 클라우드 왕복 지연은 단순 불편이 아니라 사고 요인이 된다.

또 하나의 압력은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 비용이다. 예를 들어 고해상도 영상이나 생체 신호를 전부 업로드하면 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/), 저장 비용, 규제 부담이 함께 커진다. 그래서 엣지 AI의 본질은 "AI를 더 작게 만든다"보다, <strong>결정이 필요한 자리 근처에 지능을 배치해 불필요한 왕복을 없앤다</strong>는 데 있다.

- **📢 섹션 요약 비유**: 문제를 풀 때마다 본사에 전화를 거는 직원보다, 현장에 규칙을 익힌 담당자가 바로 판단하는 편이 훨씬 빠르다. 엣지 AI는 지능을 본사에서 현장으로 내려 보내는 권한 위임이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

엣지 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 아키텍처는 보통 <strong>센서 입력 → 전처리 → 로컬 추론 → 즉시 행동 → 선택적 <a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">동기화</a></strong>의 폐루프로 동작한다. 여기서 중요한 것은 클라우드를 완전히 버리는 것이 아니라, <strong>실시간 판단은 현장에 두고 무거운 학습과 전역 최적화는 클라우드가 맡는 역할 분리</strong>다.

| 계층 | 역할 | 대표 구성 요소 | 설계 포인트 |
| :--- | :--- | :--- | :--- |
| 입력 계층 | 현실 세계 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 수집 | 카메라, 마이크, 라이다, 산업 센서 | 샘플링 주기와 노이즈 처리 |
| 전처리 계층 | 모델 입력 형태로 변환 | 리사이즈, [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/), 특징 추출 | 지연시간과 전력 최소화 |
| 추론 계층 | 로컬에서 모델 실행 | [NPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/) ([Neural Processing Unit](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/)), [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) ([Graphics Processing Unit](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)), CPU (Central Processing Unit) | 모델 크기, 연산량, 메모리 적합성 |
| [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 계층 | 결과에 따라 행동 또는 상위 이관 | 로컬 경보, 제어 명령, 클라우드 [오프로딩](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/) | [신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) [임계치](/knowledge-base/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/), 실패 시 [폴백](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/171_fallback_resilience_pattern/) |
| [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 계층 | 모델 업데이트와 어려운 사례 수집 | OTA ([Over-the-Air](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/523_iot_firmware_ota_security/)) 업데이트, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 업로드 | 선택적 전송, [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리, [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) |

아래 구조는 엣지 AI가 왜 "클라우드 제거"가 아니라 "판단 루프의 재배치"인지 보여 준다. 짧은 루프는 로컬에서 닫고, 긴 루프만 상위 계층으로 올린다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Edge / On-Device AI execution loop</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Sensor -&gt; Preprocess -&gt; Model Runtime -&gt; NPU/GPU/CPU -&gt; Decision</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── local action</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(brake / alert)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── low confidence</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">or rare sample</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Edge/Cloud service</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">OTA compressed model update ◄──</div></div>
</div>
</div>



엣지에서 AI가 돌아가려면 모델을 작게 만드는 공학이 필수다. 대표 수단은 [양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) ([Quantization](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)), [가지치기](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/) ([Pruning](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/)), [지식 증류](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/) ([Knowledge Distillation](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)) 다. 예를 들어 32비트 [부동소수점](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/087_floating_point/) 가중치를 8비트 정수로 줄이면 메모리 사용량과 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)을 크게 낮출 수 있지만, 정확도 손실이 허용 범위 안에 있는지 반드시 검증해야 한다.

즉 엣지 AI의 핵심 원리는 단순 소형화가 아니다. <strong>모델 <a href="/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a>, 하드웨어 가속, <a href="/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/">신뢰도</a> 기반 <a href="/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/">라우팅</a>, 모델 업데이트 체계</strong>가 함께 맞물려야 실제 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 된다.

- **📢 섹션 요약 비유**: 무거운 백과사전을 들고 다닐 수 없으니, 자주 쓰는 내용만 뽑은 요약본을 주머니에 넣는 방식과 같다. 다만 모르는 문제가 나오면 다시 선생님에게 물어볼 길은 남겨 둬야 한다.

---

## Ⅲ. 비교 및 연결

엣지 AI를 이해할 때 가장 중요한 경계는 <strong>온디바이스 <a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a>, 근접 엣지 서버, 클라우드 <a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a></strong>의 차이다. 셋은 경쟁 관계라기보다, 연산 위치와 책임이 다르다.

| 비교 축 | 온디바이스 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) | 엣지 서버 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) | 클라우드 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) |
| :--- | :--- | :--- | :--- |
| 연산 위치 | 스마트폰, 카메라, 차량 전자 제어 장치 (ECU, Electronic [Control Unit](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/206_control_unit/)) 내부 | 공장/기지국/매장 근처 서버 | 원격 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) |
| 지연시간 | 가장 짧음 | 짧음 | 가장 김 |
| 프라이버시 | 원본 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 외부 반출 최소 | 로컬망 내 제한적 공유 | 외부 전송 전제 |
| 연산 규모 | 배터리, 주기억장치 (RAM, Random Access Memory), 발열 제약 큼 | 상대적으로 큰 모델 가능 | 가장 큰 모델과 장기 학습 가능 |
| 대표 사례 | 얼굴 인식, 오프라인 번역, 개인 비서 | [스마트 팩토리](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/166_smart_factory/) 비전, 매장 분석, [MEC](/knowledge-base/studynote/03_network/12_iot_wpan_edge/627_mec_multi_access_edge_computing_5g/) [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | 초대형 생성형 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/), 전역 추천, 모델 재학습 |

즉 온디바이스 AI는 엣지 AI의 부분집합이다. 민감 정보와 즉시 반응이 핵심이면 온디바이스가 적합하고, 여러 장치가 같은 현장 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 공유해야 하면 멀티액세스 [엣지 컴퓨팅](/knowledge-base/studynote/12_it_management/05_security_compliance/235_edge_computing_smart_factory/) ([MEC](/knowledge-base/studynote/03_network/12_iot_wpan_edge/627_mec_multi_access_edge_computing_5g/), Multi-access [Edge Computing](/knowledge-base/studynote/12_it_management/05_security_compliance/235_edge_computing_smart_factory/)) 이나 [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 엣지 서버가 더 자연스럽다. 반대로 긴 문맥 추론, 초거대 언어 모델 ([LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/), [Large Language Model](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)), 대규모 재학습은 여전히 클라우드가 유리하다.

또한 엣지 AI는 [연합 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/256_federated_learning_privacy_model_security/) ([Federated Learning](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/256_federated_learning_privacy_model_security/)) 과도 연결된다. 추론은 단말에서 하고, 학습 결과의 일부만 모아 전역 모델을 업데이트하면 원본 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 중앙으로 모으지 않고도 지능을 향상시킬 수 있기 때문이다. 즉 엣지는 "혼자서 다 한다"가 아니라, <strong>로컬 실행과 중앙 학습을 새로운 방식으로 결합하는 계층</strong>이다.

- **📢 섹션 요약 비유**: 큰 병원, 동네 의원, 집 안 상비약은 모두 치료를 하지만 역할이 다르다. 엣지 AI도 똑같이, 어디서 바로 처리하고 어디까지 상급 기관으로 보내야 하는지를 구분해야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 엣지 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 도입 여부는 기술 유행보다 <strong>제어 루프와 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 경계</strong>가 결정한다. 얼굴 잠금 해제처럼 원본 이미지가 외부로 나가면 안 되고 100ms도 느리면 사용자 경험이 급락하는 기능은 온디바이스가 맞다. 반면 공장 카메라 100대가 동시에 비전 모델을 돌리는 경우라면, 장치마다 큰 모델을 싣기보다 로컬 엣지 서버가 더 합리적일 수 있다.

반대로 "무조건 로컬"도 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)이다. 스마트폰에서 복잡한 생성형 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델을 계속 돌리면 발열과 배터리 소모가 심해지고, 업데이트 관리도 어려워진다. 이때는 짧은 명령, [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) 요약, 기본 번역은 단말에서 처리하고, 긴 문서 생성이나 무거운 추론만 클라우드로 보내는 <strong>하이브리드 <a href="/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/">라우팅</a></strong>이 현실적이다.

### 기술사 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 응답 지연이 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~50ms 수준으로 매우 민감한가?
2. 원본 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 생체, 의료, 음성, 영상 등 외부 반출 규제가 큰가?
3. 네트워크 단절 상황에서도 기능이 유지되어야 하는가?
4. 모델이 단말의 메모리, 배터리, 발열 한계 안에 들어오는가?
5. [신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/)가 낮을 때 클라우드로 위임할 [폴백](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/171_fallback_resilience_pattern/) 경로가 있는가?
6. 모델 배포, [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/), 모니터링, OTA 업데이트 체계가 준비되어 있는가?

### 자주 나오는 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- "엣지 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)"라고 말하면서 실제로는 모든 원본 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 계속 클라우드로 올리는 경우
- 저사양 단말에 과도하게 큰 모델을 억지로 넣어 발열과 응답 지연을 키우는 경우
- 로컬 추론은 넣었지만 모델 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리와 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 전략이 없어 운영 장애를 키우는 경우
- 현장 즉시 반응이 필요한 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)인데도 [신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) 판정 없이 매번 클라우드 응답을 기다리는 경우

기술사적 판단의 핵심은 하나다. <strong>엣지 AI의 목표는 "모든 계산을 로컬에서 하기"가 아니라, 사용자와 가장 가까운 곳에서 반드시 빨라야 하는 계산만 로컬로 당기는 것</strong>이다.

- **📢 섹션 요약 비유**: 가벼운 감기약은 집에 두고 바로 먹는 편이 낫지만, 큰 수술은 병원에 가야 한다. 엣지 AI도 모든 문제를 한 장소에서 해결하려 하지 말고, 문제 크기에 맞게 진료소를 나눠야 한다.

---

## Ⅴ. 기대효과 및 결론

엣지 AI를 제대로 설계하면 지연시간 단축, 네트워크 비용 절감, 프라이버시 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/), 오프라인 복원력이라는 네 가지 이점을 동시에 얻을 수 있다. 특히 현장 제어와 개인화 기능에서는 "조금 더 똑똑함"보다 "반드시 제때 반응함"이 더 큰 가치가 된다.

하지만 한계도 분명하다. 단말은 서버가 아니므로 연산량, 메모리, 전력, 발열에 강한 제약을 받는다. 또한 모델 업데이트, 품질 모니터링, 하드웨어 편차 대응이 어려워 운영 복잡도가 높아질 수 있다. 그래서 엣지 AI는 단순 배포 위치 변경이 아니라 <strong>소프트웨어·<a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/009_semiconductor/">반도체</a>·운영 체계가 함께 바뀌는 구조적 전환</strong>이다.

결론적으로 엣지 AI와 온디바이스 AI는 클라우드의 대체재가 아니라, <strong>지능의 배치 전략을 세분화한 현대 <a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> 아키텍처의 핵심 축</strong>으로 보는 것이 맞다. 기억해야 할 질문은 "AI를 어디에 둘 것인가?"가 아니라, "어떤 판단을 어느 거리 안에서 끝내야 하는가?"다.

- **📢 섹션 요약 비유**: 중요한 결정일수록 책임 있는 사람이 가까이에 있어야 한다. 엣지 AI는 [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/)의 머리를 더 똑똑하게만 만드는 것이 아니라, 필요한 자리 가까이 데려다 놓는 일이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 온디바이스 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) ([On-Device AI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/635_on_device_ai/)) | 엣지 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 중에서도 단말 내부에서 직접 추론하는 형태 |
| [NPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/) ([Neural Processing Unit](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/)) | 저전력 고속 추론을 가능하게 하는 대표 가속기 |
| [양자화](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) ([Quantization](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)) | 모델 크기와 연산량을 줄여 엣지 배포 가능성을 높이는 핵심 기법 |
| [MEC](/knowledge-base/studynote/03_network/12_iot_wpan_edge/627_mec_multi_access_edge_computing_5g/) (Multi-access [Edge Computing](/knowledge-base/studynote/12_it_management/05_security_compliance/235_edge_computing_smart_factory/)) | 단말보다 무거운 연산을 현장 근처 서버에서 처리하는 중간 계층 |
| [연합 학습](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/256_federated_learning_privacy_model_security/) ([Federated Learning](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/256_federated_learning_privacy_model_security/)) | 원본 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 없이 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 학습을 수행하는 확장 개념 |
| TinyML | 초저전력 [마이크로컨트롤러](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/130_microcontroller/) 수준으로 AI를 축소한 극단적 엣지 형태 |
| OTA 업데이트 ([Over-the-Air](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/523_iot_firmware_ota_security/) Update) | 현장에 배포된 모델을 원격으로 안전하게 갱신하는 운영 기법 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Cloud-only inference</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Latency / privacy / bandwidth pressure</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Model compression + edge accelerators</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">On-device inference and local action</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Selective feedback + OTA update</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Hybrid edge-cloud intelligence</div>
</div>
</div>



이 흐름은 "원격 추론 중심 구조 → 현장 제약 인식 → 경량화와 가속 → 로컬 추론 → 선택적 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) → 하이브리드 지능"으로 발전하는 방향을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 엣지 AI는 숙제를 풀 때마다 멀리 있는 선생님께 전화하지 않고, 내 옆에 있는 똑똑한 도우미가 바로 알려 주는 거예요.
2. 그래서 인터넷이 잠깐 끊겨도 바로바로 대답할 수 있고, 비밀 일기도 밖으로 안 보내도 돼요.
3. 아주 어려운 문제만 나중에 선생님께 물어보고, 쉬운 문제는 현장에서 바로 해결하는 거예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 174 / 552

← **이전**: [173. C-ITS (Cooperative Intelligent Transport Systems, 협력형 지능형 교통 체계)](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/173_c_its_cooperative_intelligent_transport_systems/)
**다음**: [175. 백스캐터 통신 (Ambient Backscatter Communication) - 주변 전파를 활용하는 무전원 IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/175_ambient_backscatter_communication/) →

---
