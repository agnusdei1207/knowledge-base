+++
weight = 528
title = "528. vLLM과 PagedAttention KV 캐시 최적화 (vLLM PagedAttention KV Cache Optimization)"
date = "2026-05-09"
[extra]
categories = "studynote-ict-convergence"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: vLLM(Variable-length [[263_llm_large_language_model|Large Language Model]] inference)의 PagedAttention은 OS [[381_virtual_memory|가상 메모리]] [[259_paging|페이징]] 개념을 KV 캐시에 적용해 [[418_gpu|GPU]] 메모리 [[291_fragmentation_and_reassembly_process|단편화]]를 제거하고 [[139_throughput|처리량]]을 최대 24배 향상시킨다.
> 2. **가치**: 연속 배치(Continuous [[389_bulk_insert_batching_optimization|Batching]])와 PagedAttention의 결합으로, 다양한 시퀀스 길이의 요청을 동적으로 스케줄링해 [[418_gpu|GPU]] 활용률을 획기적으로 높인다.
> 3. **판단 포인트**: vLLM의 Tensor Parallelism으로 모델을 여러 GPU에 [[136_variance|분산]]하고, [[082_pipeline|Pipeline]] Parallelism으로 레이어를 [[136_variance|분산]]할 때 통신 오버헤드와 [[139_throughput|처리량]] 간 트레이드오프를 설계 단계에서 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

[[263_llm_large_language_model|LLM]] 서빙의 전통적 문제: 각 요청의 KV 캐시 크기는 [[087_process_state_transition|생성]] 완료 전까지 알 수 없어 과다 할당(Over-provisioning) 또는 미리 최대 시퀀스 길이만큼 연속 메모리를 예약해야 했다. 이로 인해 [[418_gpu|GPU]] 메모리의 **20~40%가 [[341_internal_fragmentation|내부 단편화]]([[341_internal_fragmentation|Internal Fragmentation]])**로 낭비됐다.

vLLM은 [[087_underpinning_contract|UC]] Berkeley 연구팀이 2023년 발표한 [[191_oss_license_compliance|오픈소스]] 추론 엔진으로, PagedAttention으로 이 문제를 근본적으로 해결했다.

- **📢 섹션 요약 비유**: 호텔에서 투숙 기간을 모르는 손님에게 무조건 최대 일수분 방을 통째로 예약하던 방식에서, 필요한 만큼만 날마다 배정하는 방식으로 전환한 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
┌──────────────────────────────────────────────────────┐
│                 PagedAttention 구조                   │
│                                                      │
│  논리적 KV 캐시           물리적 GPU 메모리 블록       │
│  ┌───────────────┐       ┌───────┬───────┬───────┐  │
│  │ 요청 A        │       │Block 0│Block 3│Block 7│  │
│  │ [Token 1~16]  │──────►│(A:1-4)│(A:5-8)│(A:9-12)│  │
│  └───────────────┘       └───────┴───────┴───────┘  │
│  ┌───────────────┐       ┌───────┬───────┐           │
│  │ 요청 B        │       │Block 1│Block 4│           │
│  │ [Token 1~8]   │──────►│(B:1-4)│(B:5-8)│           │
│  └───────────────┘       └───────┴───────┘           │
│                          블록 테이블(Block Table) 매핑 │
└──────────────────────────────────────────────────────┘
```

**PagedAttention 핵심 아이디어**
1. KV 캐시를 고정 크기 블록(예: 16토큰)으로 분할
2. 요청별 [[369_logic_bomb|논리]] KV 블록 → 물리 [[418_gpu|GPU]] 메모리 블록을 블록 테이블로 간접 매핑
3. 비연속 물리 메모리 사용 가능 → [[291_fragmentation_and_reassembly_process|단편화]] 거의 제로
4. 프리픽스 캐시(Prefix Cache) 공유: 동일 시스템 프롬프트 → 블록 공유로 메모리 재사용

**연속 배치(Continuous [[389_bulk_insert_batching_optimization|Batching]])**

| 방식 | 동작 | 문제 |
|:---:|:---:|:---:|
| 정적 배치(Static [[389_bulk_insert_batching_optimization|Batching]]) | 배치 내 모든 요청 완료 후 새 요청 수용 | [[418_gpu|GPU]] 유휴([[611_cpu_idle_wait_optimization|Idle]]) 시간 발생 |
| 연속 배치(Continuous [[389_bulk_insert_batching_optimization|Batching]]) | 완료된 요청 즉시 제거, 새 요청 즉시 삽입 | 높은 [[418_gpu|GPU]] 활용률 |

### vLLM [[282_performance_tactics|성능]] 비교

| 프레임워크 | [[139_throughput|처리량]]([[139_throughput|Throughput]]) | 특이사항 |
|:---:|:---:|:---|
| Naive 서빙 | 1× (기준) | 정적 배치, KV 낭비 |
| vLLM | 최대 24× | PagedAttention + 연속 배치 |
| TGI(HuggingFace) | 5~[[489_raid_10_hybrid|10]]× | Flash Attention 활용 |
| TensorRT-[[263_llm_large_language_model|LLM]] | [[489_raid_10_hybrid|10]]~20× | NVIDIA 최적화, 높은 복잡도 |

- **📢 섹션 요약 비유**: 연속 배치는 버스가 종점까지 기다리지 않고 내리는 승객 즉시 새 승객을 태우는 방식 — GPU가 한순간도 쉬지 않는다.

---

## Ⅲ. 비교 및 연결

### 모델 [[430_index_fast_full_scan|병렬]]화 [[268_strategy_pattern|전략]]

**Tensor Parallelism(텐서 [[430_index_fast_full_scan|병렬]])**: 단일 레이어의 행렬을 여러 GPU에 열(Column)/행(Row) 분할
- [[418_gpu|GPU]] 간 All-Reduce 통신 필요 → 동일 서버(NVLink) 내 권장
- 메모리 절감: [[418_gpu|GPU]] 수에 비례

**[[082_pipeline|Pipeline]] Parallelism(파이프라인 [[430_index_fast_full_scan|병렬]])**: 레이어 그룹을 GPU에 순차 배분
- 마이크로배치(Microbatch)로 버블(Bubble, 대기 시간) 최소화
- [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 간 다중 노드에 적합

| [[430_index_fast_full_scan|병렬]] 방식 | 장점 | 단점 |
|:---:|:---:|:---:|
| Tensor Parallelism | 레이턴시 낮음 | 고속 NVLink 필수 |
| [[082_pipeline|Pipeline]] Parallelism | 다중 노드 확장 | 파이프라인 버블 |
| 혼합(Megatron-LM) | 대규모 모델 최적 | 설계 복잡도 높음 |

- **📢 섹션 요약 비유**: 텐서 [[430_index_fast_full_scan|병렬]]은 주방 조리대를 여러 명이 나눠 쓰는 것, 파이프라인 [[430_index_fast_full_scan|병렬]]은 냉채→메인→디저트 순서대로 다른 요리사가 담당하는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**vLLM 배포 구성 예시**

```
vllm serve meta-llama/Llama-3-70B-Instruct \
  --tensor-parallel-size 4 \
  --max-model-len 8192 \
  --gpu-memory-utilization 0.90
```

**기술사 판단 포인트**

1. **KV 캐시 용량 계획**: `--max-model-len × 배치 크기 × KV 바이트 수`로 [[495_hbm|HBM]] 요구량 사전 계산
2. **프리픽스 [[456_caching|캐싱]] 활용**: [[276_fine_tuning|RAG]]/챗봇에서 동일 시스템 프롬프트 → 자동 [[263_cache_hit_miss|캐시 히트]] → TTFT(Time to First Token) 단축
3. **Speculative Decoding**: 소형 Draft 모델로 토큰 후보 [[087_process_state_transition|생성]] → 대형 모델 [[395_verification_process_review|검증]] → Decode [[139_throughput|처리량]] 2~3배 향상
4. **[[617_lora_lorawan_css_chirp_spread_spectrum|LoRA]] 서빙**: vLLM의 Punica 확장으로 다중 [[617_lora_lorawan_css_chirp_spread_spectrum|LoRA]] [[259_adapter_pattern_interface_wrapper|어댑터]] 동시 서빙 가능

- **📢 섹션 요약 비유**: vLLM은 GPU라는 주방을 낭비 없이 24시간 풀가동하는 최고 효율 주방 관리 시스템이다.

---

## Ⅴ. 기대효과 및 결론

vLLM의 PagedAttention과 연속 배치는 [[263_llm_large_language_model|LLM]] 서빙 인프라의 패러다임을 바꿨다. 동일한 GPU로 최대 24배 많은 요청을 처리할 수 있어 클라우드 서빙 비용이 획기적으로 절감됐다. OpenAI·Anthropic·Google 등 주요 서빙 인프라도 유사 최적화 기법을 채택했다. 향후 Speculative Decoding과 프리픽스 [[456_caching|캐싱]]의 결합이 TTFT를 더욱 단축할 전망이다.

- **📢 섹션 요약 비유**: vLLM 이전 [[418_gpu|GPU]] 서빙은 방 하나에 손님 하나만 받던 호텔, 이후는 빈 방 없이 효율적으로 운영하는 비즈니스 호텔이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| PagedAttention | vLLM 핵심 · OS [[259_paging|페이징]] 기반 KV 캐시 |
| 연속 배치 | [[139_throughput|처리량]] 최적화 · 동적 요청 스케줄링 |
| Tensor Parallelism | 모델 [[430_index_fast_full_scan|병렬]]화 · 행렬 분할 [[418_gpu|GPU]] [[136_variance|분산]] |
| [[082_pipeline|Pipeline]] Parallelism | 모델 [[430_index_fast_full_scan|병렬]]화 · 레이어 분할 [[418_gpu|GPU]] [[136_variance|분산]] |
| KV 캐시 | [[263_llm_large_language_model|LLM]] 추론 · 어텐션 Key-Value 저장 |

### 📈 관련 키워드 및 발전 흐름도

```text
[vLLM 핵심 · OS 페이징 기반 KV 캐시] → [vLLM과 PagedAttention KV 캐시 최적화] → [LLM 추론 · 어텐션 Key-Value 저장]
```

### 👶 어린이를 위한 3줄 비유 설명

1. AI가 대화할 때 이전 내용을 기억하는 메모장(KV 캐시)을 낭비 없이 관리하는 것이 PagedAttention이에요.
2. 메모장을 미리 왕창 예약하지 않고, 필요한 만큼만 조각조각 빌려 쓰는 방식이에요.
3. 이 덕분에 같은 GPU로 훨씬 많은 사람과 동시에 대화할 수 있어요.
