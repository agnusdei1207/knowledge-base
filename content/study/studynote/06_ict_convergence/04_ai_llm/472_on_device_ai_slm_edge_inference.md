---
title: 472. 온디바이스 AI와 SLM 엣지 추론 (On-Device AI SLM Edge Inference)
date: '2026-05-09'
tags:
- studynote-ict-convergence
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 온디바이스 [[190_ai_llm_requirements_specification|AI]]([[635_on_device_ai|On-Device AI]])는 클라우드 없이 스마트폰·[[164_pc|PC]]·[[101_iot_concept|IoT]] 디바이스에서 직접 [[190_ai_llm_requirements_specification|AI]] 추론을 실행하며, [[313_slm|SLM]]([[313_slm|Small Language Model]], 소형 언어 모델)과 모델 경량화 기술이 이를 가능하게 한다.
> 2. **가치**: [[001_dikw_pyramid|데이터]]가 디바이스를 벗어나지 않아 프라이버시가 보장되고, 네트워크 없이도 동작하며, 클라우드 [[014_api_posix|API]] 비용과 [[015_지연_데이터_관점|지연]]([[141_latency|Latency]])이 제거된다.
> 3. **판단 포인트**: [[434_quantization|양자화]]([[434_quantization|Quantization]]) INT4는 모델 크기를 75% 줄이지만 정확도 손실이 발생하므로, 배터리·발열·정확도 요구사항을 함께 고려한 최적화 조합을 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

GPT-4 같은 대형 모델은 수백억 파라미터로 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] GPU가 필요하다. 그러나 스마트폰 앱, 차량 내 음성 인식, 산업 현장 [[101_iot_concept|IoT]] 기기에서는 클라우드 연결 없이 즉시 응답이 필요하다.

**온디바이스 [[190_ai_llm_requirements_specification|AI]] 필요 시나리오**
- 프라이버시 민감 [[001_dikw_pyramid|데이터]]: 의료 음성 기록, 금융 거래 분석
- 오프라인 환경: 비행기, 지하, 원격 현장
- [[015_지연_데이터_관점|지연]] 민감 [[090_service_kubernetes_network_load_balancing|서비스]]: 자율주행 보조, 실시간 번역
- 비용 절감: 클라우드 [[014_api_posix|API]] 호출 비용 제거 (GPT-4 [[014_api_posix|API]] ≈ $0.03/1K tokens)

**[[313_slm|SLM]] 대표 모델 (7B 이하)**

| 모델 | 파라미터 | 개발사 | 특징 |
|:---:|:---:|:---:|:---|
| Phi-3 Mini | 3.8B | Microsoft | 교과서 [[001_dikw_pyramid|데이터]] 고품질 학습 |
| Gemma 2B | 2B | Google | Android/Chrome 온디바이스 |
| Llama 3.2 3B | 3B | Meta | [[158_multimodal_clip_vision_audio_encoding|멀티모달]] 지원, 엣지 특화 |
| Qwen2.5 3B | 3B | Alibaba | 다국어(한국어) 우수 |

- **📢 섹션 요약 비유**: 대형 LLM이 대형 백화점이라면, SLM은 동네 편의점 — 품목은 적지만 집 앞에서 즉시 이용 가능하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
┌──────────────────────────────────────────────┐
│              온디바이스 AI 스택               │
│                                              │
│  ┌─────────┐  경량화  ┌──────────────────┐  │
│  │  원본    │ ───────► │  경량 모델        │  │
│  │  LLM    │          │ ┌──────────────┐ │  │
│  │  (70B)  │ 양자화   │ │ INT4 Weight  │ │  │
│  └─────────┘ 프루닝   │ │ 4GB VRAM     │ │  │
│              증류     │ └──────────────┘ │  │
│                       └──────────────────┘  │
│                              │               │
│                       ┌──────▼──────┐        │
│                       │  NPU 가속   │        │
│                       │(Hexagon/ANE)│        │
│                       └─────────────┘        │
└──────────────────────────────────────────────┘
```

**모델 경량화 3대 기법**

**1. [[434_quantization|양자화]]([[434_quantization|Quantization]])**: [[267_weight_bias_activation|가중치]] [[233_precision_recall_f1_roc_auc_threshold|정밀도]]를 FP32 → INT8 → INT4로 낮춤
- FP32(32bit) → INT4(4bit): 메모리 87.5% 절감, 추론 속도 2~4배 향상
- 도구: GGUF(llama.cpp), AWQ, GPTQ

**2. 프루닝([[435_pruning_hardware|Pruning]], [[435_pruning_hardware|가지치기]])**: 중요도 낮은 [[267_weight_bias_activation|가중치]](~0에 가까운 값) 제거
- 구조적 프루닝: 뉴런/레이어 단위 제거 → 하드웨어 최적화 용이
- 비구조적 프루닝: 개별 [[267_weight_bias_activation|가중치]] 제거 → 높은 압축률, 하드웨어 지원 필요

**3. [[252_knowledge_distillation_quantization_edge_slm_diffusion|지식 증류]]([[252_knowledge_distillation_quantization_edge_slm_diffusion|Knowledge Distillation]])**: 대형 교사(Teacher) 모델의 소프트 레이블(Soft Label)로 소형 학생(Student) 모델 학습
- DistilBERT: [[301_bert_mlm|BERT]] 40% 파라미터 감소, [[282_performance_tactics|성능]] 97% 유지

### 경량화 기법 비교

| 기법 | 메모리 절감 | 정확도 손실 | 재훈련 필요 |
|:---:|:---:|:---:|:---:|
| INT8 [[434_quantization|양자화]] | 50% | 낮음 | ✗ |
| INT4 [[434_quantization|양자화]] | 75% | 중간 | ✗ |
| 구조적 프루닝 | 30~50% | 중간 | ✓ |
| [[252_knowledge_distillation_quantization_edge_slm_diffusion|지식 증류]] | 40~80% | 낮음 | ✓ |

- **📢 섹션 요약 비유**: [[434_quantization|양자화]]는 백과사전을 요약본으로 만들고, 증류는 전문가의 지식을 신입에게 전수하는 것이다.

---

## Ⅲ. 비교 및 연결

### [[424_npu|NPU]]([[424_npu|Neural Processing Unit]]) 칩 가속

| 플랫폼 | [[424_npu|NPU]]/[[190_ai_llm_requirements_specification|AI]] 가속기 | [[282_performance_tactics|성능]](TOPS) |
|:---:|:---:|:---:|
| Apple M4 | Neural Engine(ANE) | 38 TOPS |
| Snapdragon 8 Gen 3 | Hexagon [[424_npu|NPU]] | 45 TOPS |
| MediaTek Dimensity 9300 | APU 790 | 35 TOPS |

**온디바이스 vs 클라우드 비교**

| 항목 | 온디바이스 | 클라우드 |
|:---:|:---:|:---:|
| [[015_지연_데이터_관점|지연]]([[141_latency|Latency]]) | 낮음([[489_raid_10_hybrid|10]]~50ms) | 높음(500ms~2s) |
| 프라이버시 | 높음 | 중간~낮음 |
| 비용 | [[459_quic_fec_forward_error_correction|초기]] 배포 비용 | 사용량 기반 |
| [[282_performance_tactics|성능]] | 제한적 | 무제한 |
| 오프라인 | 가능 | 불가 |

- **📢 섹션 요약 비유**: 온디바이스는 포켓 계산기, 클라우드는 슈퍼컴퓨터 — 빠르고 프라이빗하지만 계산 능력의 한계가 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**배포 프레임워크**
- **llama.cpp**: CPU/[[418_gpu|GPU]] 혼합, GGUF 포맷, 크로스 플랫폼
- **MediaPipe [[263_llm_large_language_model|LLM]]**: Google, 모바일 특화, Android/iOS
- **Core ML**: Apple ANE 최적화, iOS/macOS 전용
- **MLC [[263_llm_large_language_model|LLM]]**: 다양한 하드웨어 자동 최적화

**기술사 판단 포인트**

1. **배터리/발열 제약**: INT4 [[434_quantization|양자화]]로도 연속 추론 시 스마트폰 발열 → 쓰로틀링(Throttling) 대응 설계
2. **모델 업데이트**: 온디바이스 모델 패치 배포 [[268_strategy_pattern|전략]] — OTA([[523_iot_firmware_ota_security|Over-the-Air]]) 업데이트 메커니즘
3. **보안**: 기기 내 모델 [[267_weight_bias_activation|가중치]] 탈취 → 암호화 스토리지, [[790_secure_enclave|Secure Enclave]] 활용
4. **Hybrid 아키텍처**: 간단한 [[298_qkv_attention|쿼리]] → 온디바이스, 복잡한 요청 → 클라우드 [[171_fallback_resilience_pattern|폴백]]([[129_fallback|Fallback]]) 설계 권장

- **📢 섹션 요약 비유**: 스마트폰은 강력한 [[190_ai_llm_requirements_specification|AI]] 비서를 품고 싶지만 배터리가 하루 버텨야 한다 — 균형이 설계의 핵심이다.

---

## Ⅴ. 기대효과 및 결론

온디바이스 AI와 SLM은 AI의 민주화와 프라이버시 보호를 동시에 실현한다. [[434_quantization|양자화]]·프루닝·[[252_knowledge_distillation_quantization_edge_slm_diffusion|지식 증류]]의 조합으로 7B 이하 모델이 스마트폰에서 실질적인 [[282_performance_tactics|성능]]을 제공하게 됐으며, [[424_npu|NPU]] 하드웨어의 발전과 함께 엣지 AI의 활용 범위가 급격히 확대되고 있다.

- **📢 섹션 요약 비유**: AI가 클라우드라는 거대한 서버실을 탈출해 내 주머니 속 스마트폰에 들어오는 시대가 열리고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[313_slm|SLM]]([[313_slm|Small Language Model]]) | 온디바이스 [[190_ai_llm_requirements_specification|AI]] · 7B 이하 소형 언어 모델 |
| [[434_quantization|양자화]]([[434_quantization|Quantization]]) | 경량화 기법 · INT4/INT8 [[233_precision_recall_f1_roc_auc_threshold|정밀도]] 축소 |
| [[252_knowledge_distillation_quantization_edge_slm_diffusion|지식 증류]] | 경량화 기법 · 교사-학생 모델 학습 |
| [[424_npu|NPU]] | 하드웨어 · [[190_ai_llm_requirements_specification|AI]] 연산 전용 칩 |
| GGUF | 포맷 · llama.cpp 경량 모델 포맷 |

### 📈 관련 키워드 및 발전 흐름도

```text
[온디바이스 AI · 7B 이하 소형 언어 모델] → [온디바이스 AI · SLM 엣지 추론] → [포맷 · llama.cpp 경량 모델 포맷]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 큰 컴퓨터(클라우드)에만 있던 AI를 조그만 스마트폰 안에 넣는 것이 온디바이스 AI예요.
2. 책을 요약본으로 만들고([[434_quantization|양자화]]), 불필요한 부분을 지우고(프루닝), 선생님이 학생에게 가르치듯(증류) 크기를 줄여요.
3. 인터넷이 없어도 동작하고, 내 정보가 밖으로 나가지 않아서 안전해요.
