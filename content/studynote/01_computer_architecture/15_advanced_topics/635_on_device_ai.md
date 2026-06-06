---
title: "On-Device AI"
date: "2026-05-08"
tags:
  - "studynote-computer-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 온디바이스 [인공지능](/studynote/10_ai/03_llm_nlp/231_ai_turing_test/)(On-Device [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/))은 입력 수집, 추론, 일부 개인화까지를 개인 기기 내부에서 수행하는 실행 아키텍처다.
> 2. **가치**: 네트워크가 불안정해도 수십 ms 수준의 응답성을 유지하면서 사용자 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 사용 맥락을 기기 밖으로 덜 내보낼 수 있다.
> 3. **판단 포인트**: 모든 기능을 로컬로 넣는 것이 정답은 아니며, 모델 크기·배터리·발열·보안·업데이트 주기를 고려해 로컬과 클라우드의 경계를 설계해야 한다.

---

## Ⅰ. 개요 및 필요성

온디바이스 AI는 [인공지능](/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) 모델의 실행 위치를 클라우드 서버에서 스마트폰, 자동차, 노트북, 웨어러블 같은 개인 기기로 옮기는 접근이다. 여기서 중요한 것은 단순히 "기기에서 AI가 돈다"가 아니라, 입력 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 개인화 맥락이 같은 기기 안에서 순환한다는 점이다. 그래서 프라이버시, 응답성, 오프라인 동작이 함께 개선된다.

이 방식이 필요해진 이유는 사용자 경험이 점점 실시간성과 개인화를 요구하기 때문이다. 음성 호출어 감지는 [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~50ms 수준의 반응성이 중요하고, 실시간 번역이나 사진 보정은 네트워크 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 조금만 커져도 체감 품질이 급격히 나빠진다. 또 메시지, 음성, 건강 정보처럼 민감한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 중앙 서버에 오래 남길수록 보안·규제 부담이 커진다.

온디바이스 AI가 없으면 모든 요청이 서버 왕복에 묶이고, 사용자는 항상 연결 상태와 클라우드 비용의 영향을 받는다. 반대로 잘 설계된 온디바이스 AI는 "기기 자체가 사용자에게 맞춘 작은 추론 센터"가 된다. 엣지 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 칩이 하드웨어 기반이라면, 온디바이스 AI는 그 기반 위에 올라가는 사용자 경험 설계라고 볼 수 있다.

- **📢 섹션 요약 비유**: 온디바이스 AI는 동네에 있는 개인 비서와 같다. 멀리 있는 본사에 매번 묻지 않아도, 내 습관과 상황을 아는 비서가 옆에서 바로 도와주는 셈이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

온디바이스 AI의 내부는 보통 모델 배포, 안전한 저장, 하드웨어 스케줄링, 로컬 문맥 활용, 필요 시 클라우드 보조의 흐름으로 이루어진다. 대형 언어 모델([LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/), [Large Language Model](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/))이나 비전 모델은 먼저 클라우드에서 학습된 뒤, [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)·[지식 증류](/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)·압축을 거쳐 기기용 패키지로 변환된다. 이후 애플리케이션 프로세서([AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/), Application Processor) 안의 신경망 처리 장치([NPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/), [Neural Processing Unit](/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/)), 그래픽 처리 장치([GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/), [Graphics Processing Unit](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)), 중앙 처리 장치(CPU, Central Processing Unit)가 런타임의 스케줄링에 따라 역할을 나눈다.

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| 모델 런타임 | 연산 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 실행 | 플랫폼별 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 최적화, 메모리 재사용 |
| [NPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/)/[GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)/CPU [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) | 연산 자원 배분 | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 시간과 배터리 균형 |
| 로컬 저장소 | 모델·토큰·개인화 파라미터 저장 | 암호화, [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리, [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) |
| 시큐어 엔클레이브 | 민감 키와 모델 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) | 추론 결과·프롬프트 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) |
| 클라우드 보조 채널 | 대형 모델 호출, 업데이트 배포 | 하이브리드 전환 기준 |

다음 그림은 온디바이스 AI가 단순 추론 엔진이 아니라 "로컬 실행 파이프라인"임을 보여준다.

```text
+------------------------------------------------------------------------------+
| On-device AI: execute locally, fall back to cloud only when necessary        |
+------------------------------------------------------------------------------+
| User input -> App -> Model Runtime -> NPU/GPU/CPU -> Result                  |
|                         |                                                    |
|                         +-> Secure model store / local context               |
|                         |                                                    |
|                         +-> Optional cloud fallback / model update           |
+------------------------------------------------------------------------------+
```

핵심 원리는 "가벼운 것은 로컬에서, 무거운 것은 선택적으로 외부에서" 처리하는 분할 설계다. 예를 들어 호출어 감지, 사진 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/), 오타 교정, 소규모 번역은 로컬에서 처리하고, 긴 문서 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)이나 최신 지식 검색은 하이브리드 추론(Hybrid Inference)으로 넘길 수 있다. 따라서 온디바이스 AI의 본질은 모든 것을 로컬에 밀어 넣는 것이 아니라, 사용자의 체감 가치가 큰 부분을 로컬에 붙잡아 두는 데 있다.

- **📢 섹션 요약 비유**: 온디바이스 AI는 집 안에 작은 부엌을 두고, 간단한 요리는 바로 해 먹고, 큰 잔치는 필요할 때만 외부 케이터링을 부르는 방식과 같다. 매 끼니마다 배달을 기다릴 필요가 없다.

---

## Ⅲ. 비교 및 연결

온디바이스 AI를 이해할 때는 클라우드 AI와 하이브리드 AI를 같이 봐야 경계가 선명해진다. 클라우드 AI는 최신 모델과 방대한 메모리를 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 쉽지만, 응답성·프라이버시·오프라인성에서 불리하다. 반대로 온디바이스 AI는 빠르고 사적이지만 모델 크기와 최신성에서 제약이 있다. 그래서 실제 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 두 방식을 섞는 하이브리드 구조가 점점 일반적이다.

| 항목 | 클라우드 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) | 온디바이스 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) | 하이브리드 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) |
| :--- | :--- | :--- | :--- |
| 실행 위치 | 중앙 서버 | 사용자 기기 | 기기 + 서버 분할 |
| 장점 | 큰 모델, 최신 지식 | 저지연, 오프라인, 프라이버시 | 품질과 응답성 절충 |
| 약점 | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 통신비, [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) 부담 | 모델 크기·열 제약 | 경계 설계 복잡도 |
| 적합 기능 | 대규모 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 검색 | 호출어, 번역, 카메라, 보정 | 비서형 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/), 문서 요약 |

또한 온디바이스 AI는 엣지 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 칩과 [연합 학습](/studynote/14_data_engineering/05_exam_keywords/256_federated_learning_privacy_model_security/) 사이의 가교 역할을 한다. 엣지 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 칩은 로컬 실행을 가능하게 하는 하드웨어이고, [연합 학습](/studynote/14_data_engineering/05_exam_keywords/256_federated_learning_privacy_model_security/)은 이렇게 실행되는 기기들에서 모델 업데이트를 모으는 방식이다. 다시 말해 온디바이스 AI는 "어디서 돌리는가", [연합 학습](/studynote/14_data_engineering/05_exam_keywords/256_federated_learning_privacy_model_security/)은 "어떻게 더 똑똑해지는가"를 설명한다.

- **📢 섹션 요약 비유**: 클라우드 AI가 큰 도서관 사서라면, 온디바이스 AI는 늘 옆에 있는 손안의 메모장이고, 하이브리드 AI는 메모장으로 먼저 해결하다가 정말 큰 자료가 필요할 때만 도서관에 전화하는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 온디바이스 AI를 "사용자가 기다릴 수 없는 순간"에 먼저 배치하는 것이 효과적이다. 예를 들어 스마트폰 통화 번역, 카메라 장면 인식, 차량 음성 인터페이스, 웨어러블 이상 징후 감지는 수백 ms만 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)되어도 체감 품질이 크게 떨어진다. 이런 기능은 로컬 추론으로 배치하고, 대용량 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)은 서버로 넘기는 계층화가 흔하다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 첫 응답 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 지속 응답 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 사용자 체감 기준 안에 있는가?
2. 발열과 배터리 소모가 장시간 사용에서 허용 범위를 넘지 않는가?
3. 모델 파일과 사용자 프롬프트가 암호화된 저장소에 보관되는가?
4. 무선 업데이트(OTA, [Over-the-Air](/studynote/04_software_engineering/08_security_compliance_devsecops/523_iot_firmware_ota_security/)), [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/), 기기별 모델 분기 전략이 준비되었는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 모든 기기에 동일한 초대형 모델을 무리하게 넣는 것
- 로컬 추론이라고 하면서 로그와 입력 원문을 그대로 외부로 보내는 것
- 오프라인 모드와 실패 시 클라우드 [폴백](/studynote/07_enterprise_systems/03_eai_esb_msa/171_fallback_resilience_pattern/) 기준을 정의하지 않는 것

기술사 관점에서는 "로컬로 돌린다"는 구호보다 사용자 경험 경로를 분해해서 보는 것이 중요하다. 호출어, 전처리, 보안 저장, 모델 업데이트, 실패 복구까지 전체 수명주기를 설계해야 온디바이스 AI가 제품 경쟁력이 된다.

- **📢 섹션 요약 비유**: 온디바이스 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 설계는 여행 가방 싸기와 같다. 필요한 물건은 손닿는 곳에 넣고, 부피가 큰 물건은 부치거나 현지에서 조달해야 전체 여행이 편해진다.

---

## Ⅴ. 기대효과 및 결론

온디바이스 AI가 정착하면 사용자는 더 빠르고 더 개인화된 인터페이스를 경험한다. 네트워크가 불안정해도 핵심 기능이 살아 있고, 민감한 정보가 기기 안에 머무르므로 신뢰도도 올라간다. 제조사 입장에서도 서버 추론 비용 일부를 기기로 분산할 수 있어 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 단가를 안정화하기 쉽다.

반면 한계는 모델 최신성, 장치 이질성, 메모리 제약에서 온다. 스마트폰과 자동차, 웨어러블의 자원 여건이 모두 다르므로 동일한 모델을 일괄 배포하기 어렵고, 잘못 설계하면 발열과 저장 공간 압박이 곧 사용자 불만으로 이어진다. 앞으로는 개인화된 소형 모델, 로컬 지식 저장소, [멀티모달](/studynote/14_data_engineering/03_ml_dl_llm/158_multimodal_clip_vision_audio_encoding/) 센서 결합, 하이브리드 오케스트레이션이 온디바이스 AI의 다음 단계가 될 가능성이 크다.

- **📢 섹션 요약 비유**: 온디바이스 AI는 기계에 작은 자립심을 심는 기술이다. 모든 판단을 부모에게 전화하던 아이가, 기본적인 일은 스스로 해결하고 어려운 일만 도움을 요청하는 단계로 성장하는 것과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [NPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/) | 온디바이스 AI의 핵심 로컬 추론 하드웨어다. |
| [Quantization](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) | 큰 모델을 기기 안에 담기 위해 꼭 필요한 경량화 기법이다. |
| [Secure Enclave](/studynote/01_computer_architecture/15_advanced_topics/790_secure_enclave/) | 모델과 개인화 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)를 위한 보안 경계다. |
| Hybrid Inference | 로컬과 클라우드를 나누어 쓰는 실전 구조다. |
| [Federated Learning](/studynote/14_data_engineering/05_exam_keywords/256_federated_learning_privacy_model_security/) | 기기 내부 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 두면서 모델만 함께 개선하는 상위 학습 구조다. |

### 📈 관련 키워드 및 발전 흐름도

```text
Cloud assistant
    |
    v
Edge inference
    |
    v
On-device runtime + NPU
    |
    v
Local personalization · private context
    |
    v
Hybrid AI (device + cloud)
    |
    v
Federated learning · personal AI agent
```

이 흐름은 AI의 중심이 서버 한곳에서 사용자 기기 쪽으로 이동하면서, 실행 위치와 개인화 전략이 함께 바뀌는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 온디바이스 AI는 장난감 로봇이 집 밖 컴퓨터에게 물어보지 않고도 바로 생각하게 해주는 거예요.
2. 그래서 인터넷이 없어도 중요한 일은 혼자 척척 해낼 수 있어요.
3. 하지만 아주 어려운 숙제는 큰 컴퓨터 친구에게 잠깐 도움을 요청할 수도 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 636 / 803

<- **이전**: [634. 엣지 AI 칩 아키텍처](/studynote/01_computer_architecture/15_advanced_topics/634_edge_ai_chip/)
**다음**: [636. 연합 학습 (Federated Learning) 분산 아키텍처](/studynote/01_computer_architecture/15_advanced_topics/636_federated_learning/) ->

---
