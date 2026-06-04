---
title: "329. 온디바이스 AI (On-Device AI)"
date: "2026-05-09"
tags:
  - "studynote-ai"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 온디바이스 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) ([On-Device AI](/studynote/01_computer_architecture/15_advanced_topics/635_on_device_ai/))는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 추론(Inference)을 원격 클라우드 서버가 아닌 스마트폰·웨어러블·[IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/)·자율주행 ECU 등 <strong>엣지 디바이스에 탑재된 <a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/">NPU</a> (<a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/">Neural Processing Unit</a>, 신경 처리 장치)</strong>에서 로컬로 수행하는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 배포 방식이다.
> 2. **가치**: 네트워크 없는 환경 동작·밀리초 이하 응답(실시간성)·개인 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 디바이스 내 처리(프라이버시)·클라우드 비용 0의 4대 이점이 있으며, Apple Intelligence·Google Gemini Nano·Samsung Galaxy AI가 온디바이스 AI의 대표 사례다.
> 3. **판단 포인트**: 온디바이스 AI의 핵심 기술은 **모델 경량화 3인방** — [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)([Quantization](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/))·[지식 증류](/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)([Knowledge Distillation](/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/))·모델 프루닝(Model [Pruning](/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/)) — 과 이를 하드웨어에서 가속하는 [NPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/)/DSP의 INT4/INT8 연산 최적화다.

---

## Ⅰ. 개요 및 필요성

응급 의료 드론이 산악 지형에서 환자를 구조할 때, [LTE](/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) [신호](/studynote/02_operating_system/02_process_thread/130_signal/)가 없는 환경에서도 의사 결정(골절 여부 판단 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/))이 필요하다. 클라우드 AI에 의존하면 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 없는 순간 AI가 멈춘다. 온디바이스 AI는 이 한계를 극복한다.

자율주행의 경우 더 명확하다. 브레이크 여부를 클라우드에 물어보고 100ms 후 답을 받으면 이미 사고다. <strong>엣지에서 1ms 내 결정</strong>이 생명을 구한다. 보안 카메라의 얼굴 인식도 영상을 클라우드로 보내면 [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/) 위반 — 디바이스에서 처리하면 [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) 문제가 없다.

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: 온디바이스 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) vs 클라우드 AI는 집 밖 vs 편의점의 차이다. 집에 있는 것(온디바이스)은 서버(편의점) 없이 즉시 사용 가능하지만 공간(메모리·연산)이 한정된다. 편의점(클라우드)은 모든 게 있지만 나갔다 와야 해서([네트워크 지연](/studynote/03_network/20_performance_evaluation_advanced/1002_network_delay_rtt_oneway_delay_components/)) 긴급 상황에는 집에 있는 것만 사용할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
+------------------------------------------------------------------+
|         온디바이스 AI 시스템 스택 (스마트폰 기준)                     |
+------------------------------------------------------------------+
|                                                                  |
|  애플리케이션 레이어 (Application Layer):                           |
|  카메라 AI, 번역, 음성인식, 코드 완성, 이미지 생성                    |
|              |                                                   |
|  AI 런타임 프레임워크 (AI Runtime):                                  |
|  TensorFlow Lite / CoreML / ONNX Runtime / MediaPipe            |
|              |                                                   |
|  경량화 모델 (Lightweight Model):                                  |
|  양자화 (INT4/INT8) + 지식 증류 + 프루닝 적용                       |
|  예: LLaMA 3.2 1B (INT4) -> 700MB -> 스마트폰 DRAM에 로드           |
|              |                                                   |
|  하드웨어 가속기 (NPU/DSP):                                         |
|  +---------------------------------------------------------+    |
|  |  Apple ANE (Apple Neural Engine): 38 TOPS (조 연산/초)  |    |
|  |  퀄컴 Hexagon NPU: 75 TOPS                              |    |
|  |  삼성 Exynos NPU: 34.4 TOPS                             |    |
|  |  Google Tensor NPU: 51 TOPS                             |    |
|  |  특징: INT8/INT4 행렬 곱셈 특화 병렬 처리                  |    |
|  +---------------------------------------------------------+    |
+------------------------------------------------------------------+
```

| 비교 항목 | 온디바이스 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) | 클라우드 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) |
|:---|:---|:---|
| [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간 | 1~50ms (실시간) | 100~2000ms (네트워크) |
| 프라이버시 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기기 내 처리 | 외부 서버 전송 |
| 네트워크 의존 | 없음 (오프라인 가능) | 필수 |
| 모델 크기 | 0.1~7B 파라미터 | 수천억 파라미터 |
| [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | 제한적 (경량 모델) | 최고 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) |
| 비용 | 0 ([초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 모델 탑재 후) | [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 과금 |

- **📢 섹션 요약 비유**: [NPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/) ([Neural Processing Unit](/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/))는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 전용 뇌다. CPU는 범용(모든 계산), GPU는 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 그래픽 처리, NPU는 딥러닝 행렬 곱셈만 수행하는 초특화 칩이다. [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 요리만 해야 하는 급식소([NPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/))에서는 갈비찜도 잡채도 할 줄 아는 만능 셰프(CPU) 대신 볶음밥 전문 셰프 100명([NPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/) [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 코어)이 훨씬 효율적이다.

---

## Ⅲ. 비교 및 연결

<strong>하이브리드 <a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> (Hybrid <a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a>) 아키텍처</strong>: 온디바이스와 클라우드를 상황에 따라 자동 전환하는 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/).
- 짧은 텍스트·오프라인 상태·프라이버시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) -> [SLM](/studynote/10_ai/04_ai_ops_ethics/313_slm/) 온디바이스 처리
- 복잡한 추론·인터넷 연결·대용량 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) -> [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 클라우드 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)

이 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 Apple Intelligence·Galaxy [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)·Google Pixel의 실제 구현 방식이다.

| 구분 | 핵심 초점 | 적용 상황 |
|:---|:---|:---|
| 기초 접근 | 원리 이해와 기준 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) | 작은 규모, 개념 학습 |
| 온디바이스 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) ([On-Device AI](/studynote/01_computer_architecture/15_advanced_topics/635_on_device_ai/)) | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 실용성의 균형 | 대표적인 실무 적용 |
| 확장 접근 | 자동화·대규모 최적화 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 고도화 단계 |

- **📢 섹션 요약 비유**: 하이브리드 AI는 주치의(온디바이스 [SLM](/studynote/10_ai/04_ai_ops_ethics/313_slm/))와 전문의(클라우드 [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/))의 협진 시스템이다. 감기 처방(단순 NLP)은 주치의에서 즉시 해결, 암 진단(복잡한 추론)은 대학병원 전문의에게 의뢰한다. 모든 진료를 대학병원에 가는 비용·시간·대기 낭비를 줄이면서 최고 전문성도 유지한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong>온디바이스 <a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> 배포 설계 <a href="/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/">체크리스트</a></strong>:
1. <strong>타겟 하드웨어 TOPS(Tera Operations Per Second) <a href="/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a></strong>: 모델 추론 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간 = 파라미터수 × 2 / TOPS
2. **메모리 제약**: 스마트폰 평균 [DRAM](/studynote/01_computer_architecture/06_memory_hierarchy_cache/251_dram/) 8~12GB -> INT4 7B 모델 ≈ 3.5GB 가능
3. **배터리 최적화**: [NPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/) 사용 시 CPU 대비 전력 90% 절감 가능 ([NPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/) [offloading](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/) 필수)
4. **프레임워크 선택**: iOS(CoreML+Metal), Android(TFLite+NNAPI), 크로스플랫폼(ONNX Runtime)
5. <strong>모델 업데이트 <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>: OTA([Over-The-Air](/studynote/04_software_engineering/08_security_compliance_devsecops/523_iot_firmware_ota_security/)) 업데이트 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 설계 ([연합 학습](/studynote/14_data_engineering/05_exam_keywords/256_federated_learning_privacy_model_security/)과 연계 가능)

- **📢 섹션 요약 비유**: 온디바이스 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 배터리 최적화는 전기차 회생제동과 같다. 일반 브레이크(CPU [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 추론)는 에너지를 열로 낭비하고, 회생제동([NPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/) [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/))은 같은 계산을 전용 회로에서 90% 적은 전력으로 처리해 배터리를 아낀다. NPU가 있는 기기에서 반드시 NPU를 활용해야 배터리 소모를 최소화할 수 있다.

---

## Ⅴ. 기대효과 및 결론

온디바이스 AI는 AI를 클라우드 서버실에서 꺼내 일상의 모든 기기에 심는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 편재화([AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) Everywhere) 혁명의 핵심이다. Apple M 시리즈·퀄컴 스냅드래곤·삼성 엑시노스·Google Tensor 등 모바일 [AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/)(Application Processor)의 [NPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/) [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 매년 2배씩 증가하며, 2~3년 내 스마트폰에서 70B 파라미터 LLM이 실시간 동작하는 시대가 예상된다. [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기능의 디바이스화는 클라우드 AI와 상호 보완하며 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 활용 생태계를 더욱 풍부하게 만들 것이다.

- **📢 섹션 요약 비유**: 온디바이스 AI는 PC에서 스마트폰으로의 컴퓨팅 전환과 동급의 혁명이다. 2010년대 "모든 앱이 클라우드로"가 패러다임이었다면, 2020년대 후반은 "AI가 다시 디바이스로"가 반대 방향 혁명이 일어나고 있다. 이 두 흐름이 하이브리드 AI로 수렴하며 사용자 경험의 새 지평이 열린다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [NPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/) (신경 처리 장치) | TOPS, INT8 가속 / 온디바이스 AI의 하드웨어 기반 |
| [SLM](/studynote/10_ai/04_ai_ops_ethics/313_slm/) | 소형 언어 모델, 경량화 / 온디바이스에 배포되는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델 |
| [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) ([Quantization](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)) | INT4, 메모리 절감 / 온디바이스 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 경량화 핵심 기법 |
| 하이브리드 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) | 온디바이스+클라우드 자동 전환 / 실용적 온디바이스 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 배포 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| [연합 학습](/studynote/14_data_engineering/05_exam_keywords/256_federated_learning_privacy_model_security/) | 프라이버시 보존, 로컬 학습 / 온디바이스 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 학습 개선 방법 |

### 📈 관련 키워드 및 발전 흐름도

```text
[입력 표현·특징 추출] -> [온디바이스 AI (On-Device AI)] -> [경량화·멀티모달·서비스 적용]
```

### 👶 어린이를 위한 3줄 비유 설명

1. <strong>온디바이스 <a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a></strong>는 AI가 인터넷 서버가 아닌 **스마트폰이나 자동차 안에서** 바로 동작하는 거예요!
2. 덕분에 <strong>인터넷 없어도 AI가 작동</strong>하고, 개인 정보가 서버로 나가지 않아 <strong>프라이버시도 <a href="/studynote/02_operating_system/10_security/571_protection_vs_security/">보호</a></strong>돼요.
3. <strong>Apple Intelligence, Galaxy <a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a></strong>처럼 요즘 폰에 탑재되는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기능이 모두 <strong><a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/">NPU</a> 칩 위에서 돌아가는</strong> 온디바이스 AI예요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 329 / 420

<- **이전**: [328. 연합 학습 (Federated Learning)](/studynote/10_ai/04_ai_ops_ethics/328_federated_learning/)
**다음**: [330. AI 윤리 (AI Ethics)](/studynote/10_ai/04_ai_ops_ethics/330_ai_ethics/) ->

---
