+++
title = "528. vLLM과 PagedAttention KV 캐시 최적화 (vLLM PagedAttention KV Cache Optimization)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: vLLM(Variable-length [Large Language Model](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) inference)의 PagedAttention은 OS [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/) 개념을 KV 캐시에 적용해 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 메모리 [단편화](/knowledge-base/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/)를 제거하고 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 최대 24배 향상시킨다.
> 2. **가치**: 연속 배치(Continuous [Batching](/knowledge-base/studynote/05_database/06_dw_olap_trends/389_bulk_insert_batching_optimization/))와 PagedAttention의 결합으로, 다양한 시퀀스 길이의 요청을 동적으로 스케줄링해 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 활용률을 획기적으로 높인다.
> 3. **판단 포인트**: vLLM의 Tensor Parallelism으로 모델을 여러 GPU에 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)하고, [Pipeline](/knowledge-base/studynote/12_it_management/02_itsm_itil/082_pipeline/) Parallelism으로 레이어를 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)할 때 통신 오버헤드와 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 간 트레이드오프를 설계 단계에서 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

[LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 서빙의 전통적 문제: 각 요청의 KV 캐시 크기는 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 완료 전까지 알 수 없어 과다 할당(Over-provisioning) 또는 미리 최대 시퀀스 길이만큼 연속 메모리를 예약해야 했다. 이로 인해 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 메모리의 <strong>20~40%가 <a href="/knowledge-base/studynote/02_operating_system/06_memory_management/341_internal_fragmentation/">내부 단편화</a>(<a href="/knowledge-base/studynote/02_operating_system/06_memory_management/341_internal_fragmentation/">Internal Fragmentation</a>)</strong>로 낭비됐다.

vLLM은 [UC](/knowledge-base/studynote/12_it_management/02_itsm_itil/087_underpinning_contract/) Berkeley 연구팀이 2023년 발표한 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 추론 엔진으로, PagedAttention으로 이 문제를 근본적으로 해결했다.

- **📢 섹션 요약 비유**: 호텔에서 투숙 기간을 모르는 손님에게 무조건 최대 일수분 방을 통째로 예약하던 방식에서, 필요한 만큼만 날마다 배정하는 방식으로 전환한 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">PagedAttention 구조</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">논리적 KV 캐시 물리적 GPU 메모리 블록</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">요청 A</div><div class="kb-diagram-cell">Block 0</div><div class="kb-diagram-cell">Block 3</div><div class="kb-diagram-cell">Block 7</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Token 1~16</div><div class="kb-diagram-note">►│(A:1-4)│(A:5-8)│(A:9-12)│</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">요청 B</div><div class="kb-diagram-cell">Block 1</div><div class="kb-diagram-cell">Block 4</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Token 1~8</div><div class="kb-diagram-note">►│(B:1-4)│(B:5-8)│</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">블록 테이블(Block Table) 매핑</div></div>
</div>
</div>



**PagedAttention 핵심 아이디어**
1. KV 캐시를 고정 크기 블록(예: 16토큰)으로 분할
2. 요청별 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) KV 블록 → 물리 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 메모리 블록을 블록 테이블로 간접 매핑
3. 비연속 물리 메모리 사용 가능 → [단편화](/knowledge-base/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/) 거의 제로
4. 프리픽스 캐시(Prefix Cache) 공유: 동일 시스템 프롬프트 → 블록 공유로 메모리 재사용

<strong>연속 배치(Continuous <a href="/knowledge-base/studynote/05_database/06_dw_olap_trends/389_bulk_insert_batching_optimization/">Batching</a>)</strong>

| 방식 | 동작 | 문제 |
|:---:|:---:|:---:|
| 정적 배치(Static [Batching](/knowledge-base/studynote/05_database/06_dw_olap_trends/389_bulk_insert_batching_optimization/)) | 배치 내 모든 요청 완료 후 새 요청 수용 | [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 유휴([Idle](/knowledge-base/studynote/02_operating_system/10_security/611_cpu_idle_wait_optimization/)) 시간 발생 |
| 연속 배치(Continuous [Batching](/knowledge-base/studynote/05_database/06_dw_olap_trends/389_bulk_insert_batching_optimization/)) | 완료된 요청 즉시 제거, 새 요청 즉시 삽입 | 높은 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 활용률 |

### vLLM [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 비교

| 프레임워크 | [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)([Throughput](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)) | 특이사항 |
|:---:|:---:|:---|
| Naive 서빙 | 1× (기준) | 정적 배치, KV 낭비 |
| vLLM | 최대 24× | PagedAttention + 연속 배치 |
| TGI(HuggingFace) | 5~[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)× | Flash Attention 활용 |
| TensorRT-[LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) | [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~20× | NVIDIA 최적화, 높은 복잡도 |

- **📢 섹션 요약 비유**: 연속 배치는 버스가 종점까지 기다리지 않고 내리는 승객 즉시 새 승객을 태우는 방식 — GPU가 한순간도 쉬지 않는다.

---

## Ⅲ. 비교 및 연결

### 모델 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

<strong>Tensor Parallelism(텐서 <a href="/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/">병렬</a>)</strong>: 단일 레이어의 행렬을 여러 GPU에 열(Column)/행(Row) 분할
- [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 간 All-Reduce 통신 필요 → 동일 서버(NVLink) 내 권장
- 메모리 절감: [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 수에 비례

<strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/082_pipeline/">Pipeline</a> Parallelism(파이프라인 <a href="/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/">병렬</a>)</strong>: 레이어 그룹을 GPU에 순차 배분
- 마이크로배치(Microbatch)로 버블(Bubble, 대기 시간) 최소화
- [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 간 다중 노드에 적합

| [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 방식 | 장점 | 단점 |
|:---:|:---:|:---:|
| Tensor Parallelism | 레이턴시 낮음 | 고속 NVLink 필수 |
| [Pipeline](/knowledge-base/studynote/12_it_management/02_itsm_itil/082_pipeline/) Parallelism | 다중 노드 확장 | 파이프라인 버블 |
| 혼합(Megatron-LM) | 대규모 모델 최적 | 설계 복잡도 높음 |

- **📢 섹션 요약 비유**: 텐서 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)은 주방 조리대를 여러 명이 나눠 쓰는 것, 파이프라인 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)은 냉채→메인→디저트 순서대로 다른 요리사가 담당하는 것이다.

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

1. **KV 캐시 용량 계획**: `--max-model-len × 배치 크기 × KV 바이트 수`로 [HBM](/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/495_hbm/) 요구량 사전 계산
2. <strong>프리픽스 <a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/">캐싱</a> 활용</strong>: [RAG](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/276_fine_tuning/)/챗봇에서 동일 시스템 프롬프트 → 자동 [캐시 히트](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/263_cache_hit_miss/) → TTFT(Time to First Token) 단축
3. **Speculative Decoding**: 소형 Draft 모델로 토큰 후보 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) → 대형 모델 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) → Decode [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 2~3배 향상
4. <strong><a href="/knowledge-base/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/">LoRA</a> 서빙</strong>: vLLM의 Punica 확장으로 다중 [LoRA](/knowledge-base/studynote/03_network/12_iot_wpan_edge/617_lora_lorawan_css_chirp_spread_spectrum/) [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) 동시 서빙 가능

- **📢 섹션 요약 비유**: vLLM은 GPU라는 주방을 낭비 없이 24시간 풀가동하는 최고 효율 주방 관리 시스템이다.

---

## Ⅴ. 기대효과 및 결론

vLLM의 PagedAttention과 연속 배치는 [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 서빙 인프라의 패러다임을 바꿨다. 동일한 GPU로 최대 24배 많은 요청을 처리할 수 있어 클라우드 서빙 비용이 획기적으로 절감됐다. OpenAI·Anthropic·Google 등 주요 서빙 인프라도 유사 최적화 기법을 채택했다. 향후 Speculative Decoding과 프리픽스 [캐싱](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/456_caching/)의 결합이 TTFT를 더욱 단축할 전망이다.

- **📢 섹션 요약 비유**: vLLM 이전 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 서빙은 방 하나에 손님 하나만 받던 호텔, 이후는 빈 방 없이 효율적으로 운영하는 비즈니스 호텔이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| PagedAttention | vLLM 핵심 · OS [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/) 기반 KV 캐시 |
| 연속 배치 | [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 최적화 · 동적 요청 스케줄링 |
| Tensor Parallelism | 모델 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화 · 행렬 분할 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) |
| [Pipeline](/knowledge-base/studynote/12_it_management/02_itsm_itil/082_pipeline/) Parallelism | 모델 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화 · 레이어 분할 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) |
| KV 캐시 | [LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 추론 · 어텐션 Key-Value 저장 |

### 📈 관련 키워드 및 발전 흐름도

```text
[vLLM 핵심 · OS 페이징 기반 KV 캐시] → [vLLM과 PagedAttention KV 캐시 최적화] → [LLM 추론 · 어텐션 Key-Value 저장]
```

### 👶 어린이를 위한 3줄 비유 설명

1. AI가 대화할 때 이전 내용을 기억하는 메모장(KV 캐시)을 낭비 없이 관리하는 것이 PagedAttention이에요.
2. 메모장을 미리 왕창 예약하지 않고, 필요한 만큼만 조각조각 빌려 쓰는 방식이에요.
3. 이 덕분에 같은 GPU로 훨씬 많은 사람과 동시에 대화할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 528 / 552

← **이전**: [527. HBM GPU 병렬 대역폭과 LLM 병목 완화 (HBM GPU Parallel Bandwidth LLM Bottleneck)](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/527_hbm_gpu_parallel_bandwidth_llm_bottleneck/)
**다음**: [529. DSPy 프롬프트 자동 최적화와 컴파일 (DSPy Prompt Auto-Optimization Compilation)](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/529_dspy_prompt_auto_optimization_compilation/) →

---
