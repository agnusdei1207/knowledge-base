+++
weight = 527
title = "527. HBM GPU 병렬 대역폭과 LLM 병목 완화 (HBM GPU Parallel Bandwidth LLM Bottleneck)"
date = "2026-05-09"
[extra]
categories = "studynote-ict-convergence"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[263_llm_large_language_model|LLM]] 추론은 연산(Compute Bound)이 아닌 메모리 [[140_bandwidth|대역폭]](Memory [[140_bandwidth|Bandwidth]] Bound) 병목이 지배적이며, [[495_hbm|HBM]]([[495_hbm|High Bandwidth Memory]])은 DRAM을 수직 적층해 1TB/s 이상의 [[140_bandwidth|대역폭]]으로 이 병목을 완화한다.
> 2. **가치**: [[418_gpu|GPU]] [[427_tensor_core|텐서 코어]]([[427_tensor_core|Tensor Core]])는 FP16/BF16 혼합 [[233_precision_recall_f1_roc_auc_threshold|정밀도]] 행렬 연산을 가속하지만, [[263_llm_large_language_model|LLM]] 추론의 KV 캐시는 O(레이어 × 헤드 × 시퀀스 길이)로 메모리를 소비해 결국 [[495_hbm|HBM]] 용량과 [[140_bandwidth|대역폭]]이 서빙 규모를 결정한다.
> 3. **판단 포인트**: H100(HBM3, 3.35TB/s, 80GB)은 A100(HBM2e, 2TB/s, 80GB) 대비 [[140_bandwidth|대역폭]] 1.67배 우위로, 배포 하드웨어 선택 시 [[410_mfu_algorithm|MFU]](Model [[137_flops|FLOPs]] Utilization)와 메모리 [[140_bandwidth|대역폭]]을 함께 분석해야 한다.

---

## Ⅰ. 개요 및 필요성

대형 언어 모델은 훈련 시 연산 집약적이지만, **추론 시에는 배치 크기가 작아 메모리 [[140_bandwidth|대역폭]] 병목**이 지배적이다. 70B 모델의 FP16 [[267_weight_bias_activation|가중치]]만 약 140GB — 단일 GPU로는 적재조차 불가능하다.

**[[263_llm_large_language_model|LLM]] 하드웨어 병목 이중 구조**
- **연산 병목(Compute Bound)**: 배치 크기 크고 행렬 연산 많을 때
- **메모리 병목(Memory [[140_bandwidth|Bandwidth]] Bound)**: 배치 크기 작고 [[267_weight_bias_activation|가중치]] 로드가 주를 이룰 때
- [[263_llm_large_language_model|LLM]] 자기회귀([[248_bert_encoder_mlm_gpt_decoder_autoregressive_comparison|Autoregressive]]) 추론: 한 번에 토큰 1개씩 [[087_process_state_transition|생성]] → 배치 크기 1 → **메모리 바운드 지배**

- **📢 섹션 요약 비유**: 요리사([[418_gpu|GPU]] 연산)는 빠른데 냉장고에서 재료 꺼내는 속도(메모리 [[140_bandwidth|대역폭]])가 느리면 결국 기다릴 수밖에 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
┌─────────────────────────────────────────────────┐
│                GPU 메모리 계층                   │
│                                                 │
│  ┌─────────────────────────────────────────┐    │
│  │           HBM(High Bandwidth Memory)    │    │
│  │  ┌──────┐ TSV  ┌──────┐ TSV  ┌──────┐ │    │
│  │  │DRAM_1│──────│DRAM_2│──────│DRAM_3│ │    │
│  │  │ Die  │      │ Die  │      │ Die  │ │    │
│  │  └──────┘      └──────┘      └──────┘ │    │
│  │        수직 적층(3D Stacking)           │    │
│  │        대역폭: 2~4 TB/s               │    │
│  └─────────────────────────────────────────┘    │
│                      │                          │
│  ┌───────────────────▼──────────────────────┐   │
│  │           SM(Streaming Multiprocessor)   │   │
│  │  ┌──────────────────────────────────┐   │   │
│  │  │     텐서 코어(Tensor Core)        │   │   │
│  │  │  FP16/BF16/INT8 행렬 곱 가속     │   │   │
│  │  └──────────────────────────────────┘   │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

**[[495_hbm|HBM]] 구조**
- [[496_tsv|TSV]](Through-Silicon Via, 실리콘 관통 비아)로 [[251_dram|DRAM]] 다이(Die)를 수직 적층
- HBM2e(A100): 2.0 TB/s, HBM3(H100): 3.35 TB/s, HBM3e(H200): 4.8 TB/s
- 용량: A100 40/80GB, H100 80GB, H200 141GB

### H100 vs A100 비교

| 항목 | A100 SXM4 | H100 SXM5 |
|:---:|:---:|:---:|
| [[495_hbm|HBM]] 세대 | HBM2e | HBM3 |
| 메모리 [[140_bandwidth|대역폭]] | 2.0 TB/s | 3.35 TB/s |
| 메모리 용량 | 80GB | 80GB |
| FP16 텐서 [[282_performance_tactics|성능]] | 312 TFLOPS | 989 TFLOPS |
| NVLink [[140_bandwidth|대역폭]] | 600 GB/s | 900 GB/s |
| TDP | 400W | 700W |

- **📢 섹션 요약 비유**: H100은 A100보다 냉장고([[495_hbm|HBM]]) 문이 훨씬 빠르게 열리고, 요리 화구([[427_tensor_core|텐서 코어]])도 3배 더 강력하다.

---

## Ⅲ. 비교 및 연결

### KV [[259_cache_memory|캐시 메모리]] 소비

트랜스포머의 KV(Key-Value) 캐시는 이전 토큰의 어텐션 계산 결과를 저장:

```
KV 캐시 크기 = 2 × 레이어 수 × 헤드 수 × 헤드 차원 × 시퀀스 길이 × 정밀도 바이트
```

- Llama 3 70B, FP16, 시퀀스 4096 토큰: ≈ **8GB** (모델 [[267_weight_bias_activation|가중치]] 140GB에 추가)
- 시퀀스 길이 증가 시 KV 캐시 선형 증가 → [[495_hbm|HBM]] 용량 한계 도달

**연산 강도(Arithmetic Intensity)와 루프라인 분석**

| 작업 | 연산 강도 | 병목 |
|:---:|:---:|:---:|
| 행렬 곱([[588_mlops_pipeline_automation|Training]]/Prefill) | 높음 | Compute Bound |
| 자기회귀 Decode | 낮음 | Memory Bound |
| 배치 Decode(대형 배치) | 중간 | 혼합 |

- **📢 섹션 요약 비유**: Prefill은 책 전체를 한 번에 읽는 것(연산 집약), Decode는 단어 하나씩 사전에서 찾는 것(메모리 집약)이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**[[263_llm_large_language_model|LLM]] 서빙 하드웨어 선택 기준**

1. **모델 파라미터 수 → 최소 [[495_hbm|HBM]] 용량 계산**
   - 7B FP16: ~14GB → 단일 A100 40GB 가능
   - 70B FP16: ~140GB → A100 2장 또는 H100 2장 필요

2. **[[139_throughput|처리량]] 목표 → [[140_bandwidth|대역폭]] 기준 TPS 계산**
   - Tokens/s ≈ [[140_bandwidth|대역폭]](GB/s) / 모델 크기(GB) × 1000

3. **전력 효율**: H100 TDP 700W → [[016_tco|TCO]](Total Cost of Ownership) 계산에 포함
4. **[[410_mfu_algorithm|MFU]](Model [[137_flops|FLOPs]] Utilization)**: 실제 사용 비율, 50% 이상이면 좋은 설계

**[[418_gpu|GPU]] 인프라 대안 비교**

| 플랫폼 | 장점 | 단점 |
|:---:|:---:|:---:|
| NVIDIA H100 | 최고 [[282_performance_tactics|성능]], 생태계 | 고비용, 공급 부족 |
| AMD MI300X | 192GB HMC, 가성비 | 소프트웨어 생태계 열세 |
| Google [[425_tpu|TPU]] v5 | 구글 클라우드 특화 | 유연성 제한 |

- **📢 섹션 요약 비유**: H100은 F1 레이싱카, A100은 스포츠카 — 둘 다 빠르지만 가격과 유지비가 다르다.

---

## Ⅴ. 기대효과 및 결론

HBM과 [[427_tensor_core|텐서 코어]]의 발전은 [[263_llm_large_language_model|LLM]] 서빙의 [[139_throughput|처리량]]을 수년 만에 수십 배 향상시켰다. 그러나 자기회귀 추론의 메모리 바운드 특성은 근본적 한계이므로, PagedAttention·FlashAttention·모델 병렬화 등 소프트웨어 최적화를 병행해야 한다. H200·Blackwell 아키텍처로 [[140_bandwidth|대역폭]]이 5TB/s를 넘어서면서 더욱 긴 [[033_context|컨텍스트]] 처리가 가능해질 전망이다.

- **📢 섹션 요약 비유**: [[495_hbm|HBM]] 발전은 [[190_ai_llm_requirements_specification|AI]] 두뇌의 혈관을 점점 굵게 만드는 과정 — 피([[001_dikw_pyramid|데이터]])가 빠르게 흐를수록 사고도 빨라진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[495_hbm|HBM]]([[495_hbm|High Bandwidth Memory]]) | [[418_gpu|GPU]] 메모리 · 수직 적층 고대역폭 메모리 |
| [[496_tsv|TSV]](Through-Silicon Via) | [[495_hbm|HBM]] 구조 · 다이 간 수직 연결 |
| [[427_tensor_core|텐서 코어]]([[427_tensor_core|Tensor Core]]) | [[418_gpu|GPU]] 연산 · 혼합 [[233_precision_recall_f1_roc_auc_threshold|정밀도]] 행렬 가속 |
| KV 캐시 | [[263_llm_large_language_model|LLM]] 추론 · 어텐션 키-값 캐시 |
| [[410_mfu_algorithm|MFU]] | [[282_performance_tactics|성능]] 지표 · 모델 [[137_flops|FLOPs]] 활용률 |

### 📈 관련 키워드 및 발전 흐름도

```text
[GPU 메모리 · 수직 적층 고대역폭 메모리] → [HBM GPU 병렬 대역폭과 LLM 병목 완화] → [성능 지표 · 모델 FLOPs 활용률]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[190_ai_llm_requirements_specification|AI]] 두뇌([[418_gpu|GPU]])가 아무리 빨라도 정보를 담은 기억창고([[495_hbm|HBM]])에서 꺼내는 속도가 느리면 기다려야 해요.
2. HBM은 기억창고를 여러 층으로 쌓아 문을 엄청 크게 만든 것이에요 — 한 번에 많은 정보를 꺼낼 수 있어요.
3. H100은 A100보다 이 문이 1.67배 더 크고, [[190_ai_llm_requirements_specification|AI]] 두뇌도 3배 더 강해요.
