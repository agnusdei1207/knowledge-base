---
title: "On-Device AI SLM Edge Inference"
date: "2026-05-09"
tags:
  - "studynote-ict-convergence"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 온디바이스 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)([On-Device AI](/studynote/01_computer_architecture/15_advanced_topics/635_on_device_ai/))는 클라우드 없이 스마트폰·[PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)·[IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 디바이스에서 직접 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 추론을 실행하며, [SLM](/studynote/10_ai/04_ai_ops_ethics/313_slm/)([Small Language Model](/studynote/10_ai/04_ai_ops_ethics/313_slm/), 소형 언어 모델)과 모델 경량화 기술이 이를 가능하게 한다.
> 2. **가치**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 디바이스를 벗어나지 않아 프라이버시가 보장되고, 네트워크 없이도 동작하며, 클라우드 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 비용과 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)([Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))이 제거된다.
> 3. **판단 포인트**: [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)([Quantization](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)) INT4는 모델 크기를 75% 줄이지만 정확도 손실이 발생하므로, 배터리·발열·정확도 요구사항을 함께 고려한 최적화 조합을 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

GPT-4 같은 대형 모델은 수백억 파라미터로 [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) GPU가 필요하다. 그러나 스마트폰 앱, 차량 내 음성 인식, 산업 현장 [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 기기에서는 클라우드 연결 없이 즉시 응답이 필요하다.

<strong>온디바이스 <a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> 필요 시나리오</strong>
- 프라이버시 민감 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/): 의료 음성 기록, 금융 거래 분석
- 오프라인 환경: 비행기, 지하, 원격 현장
- [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 민감 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/): 자율주행 보조, 실시간 번역
- 비용 절감: 클라우드 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호출 비용 제거 (GPT-4 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) ≈ $0.03/1K tokens)

<strong><a href="/studynote/10_ai/04_ai_ops_ethics/313_slm/">SLM</a> 대표 모델 (7B 이하)</strong>

| 모델 | 파라미터 | 개발사 | 특징 |
|:---:|:---:|:---:|:---|
| Phi-3 Mini | 3.8B | Microsoft | 교과서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 고품질 학습 |
| Gemma 2B | 2B | Google | Android/Chrome 온디바이스 |
| Llama 3.2 3B | 3B | Meta | [멀티모달](/studynote/14_data_engineering/03_ml_dl_llm/158_multimodal_clip_vision_audio_encoding/) 지원, 엣지 특화 |
| Qwen2.5 3B | 3B | Alibaba | 다국어(한국어) 우수 |

- **📢 섹션 요약 비유**: 대형 LLM이 대형 백화점이라면, SLM은 동네 편의점 — 품목은 적지만 집 앞에서 즉시 이용 가능하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
+----------------------------------------------+
|              온디바이스 AI 스택               |
|                                              |
|  +---------+  경량화  +------------------+  |
|  |  원본    | -------► |  경량 모델        |  |
|  |  LLM    |          | +--------------+ |  |
|  |  (70B)  | 양자화   | | INT4 Weight  | |  |
|  +---------+ 프루닝   | | 4GB VRAM     | |  |
|              증류     | +--------------+ |  |
|                       +------------------+  |
|                              |               |
|                       +------v------+        |
|                       |  NPU 가속   |        |
|                       |(Hexagon/ANE)|        |
|                       +-------------+        |
+----------------------------------------------+
```

**모델 경량화 3대 기법**

<strong>1. <a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/">양자화</a>(<a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/">Quantization</a>)</strong>: [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)를 FP32 -> INT8 -> INT4로 낮춤
- FP32(32bit) -> INT4(4bit): 메모리 87.5% 절감, 추론 속도 2~4배 향상
- 도구: GGUF(llama.cpp), AWQ, GPTQ

<strong>2. 프루닝(<a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/">Pruning</a>, <a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/435_pruning_hardware/">가지치기</a>)</strong>: 중요도 낮은 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)(~0에 가까운 값) 제거
- 구조적 프루닝: 뉴런/레이어 단위 제거 -> 하드웨어 최적화 용이
- 비구조적 프루닝: 개별 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 제거 -> 높은 압축률, 하드웨어 지원 필요

<strong>3. <a href="/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/">지식 증류</a>(<a href="/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/">Knowledge Distillation</a>)</strong>: 대형 교사(Teacher) 모델의 소프트 레이블(Soft Label)로 소형 학생(Student) 모델 학습
- DistilBERT: [BERT](/studynote/10_ai/04_ai_ops_ethics/301_bert_mlm/) 40% 파라미터 감소, [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 97% 유지

### 경량화 기법 비교

| 기법 | 메모리 절감 | 정확도 손실 | 재훈련 필요 |
|:---:|:---:|:---:|:---:|
| INT8 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) | 50% | 낮음 | ✗ |
| INT4 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/) | 75% | 중간 | ✗ |
| 구조적 프루닝 | 30~50% | 중간 | ✓ |
| [지식 증류](/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/) | 40~80% | 낮음 | ✓ |

- **📢 섹션 요약 비유**: [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)는 백과사전을 요약본으로 만들고, 증류는 전문가의 지식을 신입에게 전수하는 것이다.

---

## Ⅲ. 비교 및 연결

### [NPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/)([Neural Processing Unit](/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/)) 칩 가속

| 플랫폼 | [NPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/)/[AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 가속기 | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)(TOPS) |
|:---:|:---:|:---:|
| Apple M4 | Neural 엔진(ANE) | 38 TOPS |
| Snapdragon 8 Gen 3 | Hexagon [NPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/) | 45 TOPS |
| MediaTek Dimensity 9300 | APU 790 | 35 TOPS |

**온디바이스 vs 클라우드 비교**

| 항목 | 온디바이스 | 클라우드 |
|:---:|:---:|:---:|
| [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)([Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)) | 낮음([10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~50ms) | 높음(500ms~2s) |
| 프라이버시 | 높음 | 중간~낮음 |
| 비용 | [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 배포 비용 | 사용량 기반 |
| [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | 제한적 | 무제한 |
| 오프라인 | 가능 | 불가 |

- **📢 섹션 요약 비유**: 온디바이스는 포켓 계산기, 클라우드는 슈퍼컴퓨터 — 빠르고 프라이빗하지만 계산 능력의 한계가 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**배포 프레임워크**
- **llama.cpp**: CPU/[GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 혼합, GGUF 포맷, 크로스 플랫폼
- <strong>MediaPipe <a href="/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/">LLM</a></strong>: Google, 모바일 특화, Android/iOS
- **Core ML**: Apple ANE 최적화, iOS/macOS 전용
- <strong>MLC <a href="/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/">LLM</a></strong>: 다양한 하드웨어 자동 최적화

**기술사 판단 포인트**

1. **배터리/발열 제약**: INT4 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)로도 연속 추론 시 스마트폰 발열 -> 쓰로틀링(Throttling) 대응 설계
2. **모델 업데이트**: 온디바이스 모델 패치 배포 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) — OTA([Over-the-Air](/studynote/04_software_engineering/08_security_compliance_devsecops/523_iot_firmware_ota_security/)) 업데이트 메커니즘
3. **보안**: 기기 내 모델 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 탈취 -> 암호화 스토리지, [Secure Enclave](/studynote/01_computer_architecture/15_advanced_topics/790_secure_enclave/) 활용
4. **Hybrid 아키텍처**: 간단한 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) -> 온디바이스, 복잡한 요청 -> 클라우드 [폴백](/studynote/07_enterprise_systems/03_eai_esb_msa/171_fallback_resilience_pattern/)([Fallback](/studynote/13_cloud_architecture/03_msa_serverless/129_fallback/)) 설계 권장

- **📢 섹션 요약 비유**: 스마트폰은 강력한 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 비서를 품고 싶지만 배터리가 하루 버텨야 한다 — 균형이 설계의 핵심이다.

---

## Ⅴ. 기대효과 및 결론

온디바이스 AI와 SLM은 AI의 민주화와 프라이버시 보호를 동시에 실현한다. [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)·프루닝·[지식 증류](/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/)의 조합으로 7B 이하 모델이 스마트폰에서 실질적인 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 제공하게 됐으며, [NPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/) 하드웨어의 발전과 함께 엣지 AI의 활용 범위가 급격히 확대되고 있다.

- **📢 섹션 요약 비유**: AI가 클라우드라는 거대한 서버실을 탈출해 내 주머니 속 스마트폰에 들어오는 시대가 열리고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [SLM](/studynote/10_ai/04_ai_ops_ethics/313_slm/)([Small Language Model](/studynote/10_ai/04_ai_ops_ethics/313_slm/)) | 온디바이스 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) · 7B 이하 소형 언어 모델 |
| [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)([Quantization](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)) | 경량화 기법 · INT4/INT8 [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) 축소 |
| [지식 증류](/studynote/14_data_engineering/05_exam_keywords/252_knowledge_distillation_quantization_edge_slm_diffusion/) | 경량화 기법 · 교사-학생 모델 학습 |
| [NPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/) | 하드웨어 · [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 연산 전용 칩 |
| GGUF | 포맷 · llama.cpp 경량 모델 포맷 |

### 📈 관련 키워드 및 발전 흐름도

```text
[온디바이스 AI · 7B 이하 소형 언어 모델] -> [온디바이스 AI · SLM 엣지 추론] -> [포맷 · llama.cpp 경량 모델 포맷]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 큰 컴퓨터(클라우드)에만 있던 AI를 조그만 스마트폰 안에 넣는 것이 온디바이스 AI예요.
2. 책을 요약본으로 만들고([양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)), 불필요한 부분을 지우고(프루닝), 선생님이 학생에게 가르치듯(증류) 크기를 줄여요.
3. 인터넷이 없어도 동작하고, 내 정보가 밖으로 나가지 않아서 안전해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 472 / 552

<- **이전**: [471. 연합 학습 프라이버시 보존 그래디언트 집계 (Federated Learning Privacy Gradient Aggregation)](/studynote/06_ict_convergence/04_ai_llm/471_federated_learning_privacy_gradient_aggregation/)
**다음**: [473. 블록체인 머클 트리와 해시 무결성 (Blockchain Merkle Tree and Hash Integrity)](/studynote/06_ict_convergence/01_blockchain/473_blockchain_merkle_tree_hash_integrity/) ->

---
