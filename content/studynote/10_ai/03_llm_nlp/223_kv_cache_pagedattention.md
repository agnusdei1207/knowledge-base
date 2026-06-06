---
title: "KV Cache Pagedattention"
date: "2026-05-09"
tags:
  - "studynote-ai"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: LLM이 대답을 만들어낼 때마다 과거에 자기가 내뱉은 단어들의 수학적 기억([Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/)-Value)을 매번 처음부터 다시 계산하지 않고 저장해 두는 <strong>KV 캐시(Cache)</strong>는 끔찍한 메모리 파편화를 일으킨다. 이를 해결하기 위해 기존 컴퓨터 OS의 <strong><a href="/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/">가상 메모리</a> <a href="/studynote/02_operating_system/04_synchronization/259_paging/">페이징</a>(<a href="/studynote/02_operating_system/04_synchronization/259_paging/">Paging</a>) 기법을 딥러닝 <a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/">GPU</a> 메모리 관리로 그대로 훔쳐 와서 쪼개 넣은 혁명이 바로 PagedAttention (vLLM 프레임워크의 심장)</strong>이다.
> 2. **가치**: 기존 [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 서빙은 한 사람당 할당된 메모리 블록이 중간중간 텅텅 비어 버리는 멍청한 관리([내부 단편화](/studynote/02_operating_system/06_memory_management/341_internal_fragmentation/) 60%) 때문에 비싼 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)(H100) 1대로 고작 10명밖에 동시 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 못 했다. PagedAttention은 이 빈 공간을 테트리스처럼 꽉꽉 채워 넣어 메모리 낭비를 4%로 압살 시키고, <strong>동시 <a href="/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/">처리량</a>(<a href="/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/">Throughput</a>)을 무려 20배 폭발시켜 기업의 <a href="/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a> 서버 운영비를 1/20로 깎아버렸다.</strong>
> 3. **판단 포인트**: 기존 어텐션(Attention)이 물리적으로 한 덩어리의 커다란 연속된 메모리 공간을 강제 요구했다면, PagedAttention은 이 덩어리를 잘게 잘라(Block) [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 메모리 여기저기에 흩뿌려 놓고 가상 포인터 테이블(Block Table)로 묶어버린다. 프롬프트 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)이나 [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)([Quantization](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)) 없이 오직 <strong>'순수 메모리 인프라 배관 공사'</strong>만으로 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 가속을 이뤄낸 아키텍처의 승리다.

---

## Ⅰ. 개요 및 필요성

우리가 챗GPT에게 긴 질문을 던지면, 챗GPT는 단어를 하나씩 뱉어낸다([Auto-regressive](/studynote/10_ai/05_data_science_ml/383_llm_autoregressive_math/)). "안녕 -> 하 -> 세 -> 요".
이때 '요'라는 글자를 뱉으려면 그전에 자기가 뱉었던 '안녕', '하', '세'라는 단어들이 어떤 문맥을 갖는지 수학적 행렬(Key와 Value)로 전부 연산해야 한다. 다음 글자를 뱉을 때마다 앞글자들을 처음부터 싹 다 다시 계산하면 서버가 터지니까, 앞글자들의 행렬을 버리지 않고 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 메모리에 킵해두는 꼼수가 바로 <strong>KV 캐시 (<a href="/studynote/06_ict_convergence/04_ai_llm/291_kv_cache/">Key-Value Cache</a>)</strong>다.

그런데 대형 참사가 터졌다. 유저 A가 질문을 던지면 서버는 "얘가 몇 글자나 뱉을지 모르니까 일단 메모리 2,000칸을 통째로 예약해 둬야지!"라고 커다란 방(연속 메모리)을 잡아버린다. 유저 A가 100글자만 뱉고 대화를 끝내버리면 나머지 1,900칸은 아무도 못 쓰는 쓰레기 공간이 되어버린다([내부 단편화](/studynote/02_operating_system/06_memory_management/341_internal_fragmentation/)). 유저 B가 오면 또 새로운 2,000칸을 잡는다. 결국 <strong>최고급 80GB짜리 <a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/">GPU</a> 메모리 중 60% 이상이 그냥 '예약만 해두고 텅텅 빈 공기'로 낭비</strong>되어 버렸다. [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 연산력은 펑펑 노는데 "메모리 꽉 찼어!"라며 유저들을 다 튕겨내는 어처구니없는 상황이 [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 기업들의 목을 조였다.

이때 [UC](/studynote/12_it_management/02_itsm_itil/871_underpinning_contract/) 버클리 연구진이 이마를 쳤다. "야! 이거 1960년대 컴퓨터 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)(OS)가 램(RAM) 모자랄 때 해결했던 '[페이징](/studynote/02_operating_system/04_synchronization/259_paging/)([Paging](/studynote/02_operating_system/04_synchronization/259_paging/)) 기법'이랑 완전 똑같은 문제잖아? OS의 [페이징](/studynote/02_operating_system/04_synchronization/259_paging/)을 딥러닝 [트랜스포머](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) 어텐션 공식에 그대로 갖다 박아버리자!"
그렇게 탄생한 것이 <strong>vLLM (<a href="/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/">오픈소스</a> <a href="/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/">LLM</a> 서빙 프레임워크)</strong>과 그 심장인 <strong>PagedAttention(<a href="/studynote/10_ai/04_ai_ops_ethics/338_vllm_paged_attention/">페이지드 어텐션</a>)</strong> [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다. 무식하게 큰 방을 예약하는 짓을 끝내고, 블록(Block) 단위로 쪼개어 낭비율을 4%로 깎아낸 미친 최적화의 서막이다.

```text
+----------------------------------------------+
| Background Problem -> Need -> Adoption Value   |
+----------------------------------------------+
| Existing limitation | Operational pressure   |
| New requirement     | Design decision point  |
+----------------------------------------------+
```

- **📢 섹션 요약 비유**: 기존 KV 캐시는 식당([GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/))의 '무식한 테이블 예약'이다. 손님이 2명 올지 20명 올지 모르니까 무조건 20인용 대형 테이블을 통째로 줘버린다. 손님 2명이 앉고 나면 나머지 18자리는 텅텅 비는데, 다른 손님을 못 받는다. PagedAttention(vLLM)은 '레고 블록 테이블'이다. 손님이 올 때 처음엔 딱 2인용 블록 테이블만 주고, 친구가 한 명 더 올 때마다 창고에서 1인용 테이블([Page](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)/Block)을 딱 하나씩만 꺼내서 동적으로 붙여준다. 남는 자리가 없으니 식당에 손님(동시 유저)을 20배나 더 우겨넣을 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

PagedAttention은 연속된 물리적 메모리를 요구하던 [트랜스포머](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/)의 어텐션 뇌 수술을 감행하여, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 파편화되어 흩어져 있어도 가상 주소로 한방에 묶어서 연산해 버리는 기적을 쓴다.

```text
+--------------------------------------------------------------+
|           vLLM의 PagedAttention 메모리 관리 아키텍처 도해               |
+--------------------------------------------------------------+
|  [기존: 멍청한 연속 메모리 할당 (Fragmentation 지옥)]                  |
|   * GPU 메모리: [ 유저A (1,000칸 예약, 100칸 씀) ] [ 텅텅 빔 900칸 ]       |
|   * --> 낭비가 90%라 유저 B, C를 더 받을 수가 없음. (서버 다운)             |
|                                                              |
|  [PagedAttention: 블록(Block) 테이블과 동적 가상 할당 혁명]            |
|   * 논리적 가상 메모리 (유저가 보는 환상): 유저 A의 KV 데이터는 이어진 것처럼 보임.|
|   * 물리적 GPU 메모리 (실제 쪼개진 파편):                             |
|      [블록1: 유저A]  [블록2: 유저B]  [블록3: 유저A]  [블록4: 텅빔]      |
|                                                              |
|  [★ Block Table (포인터 맵핑 심장부)]                              |
|   * OS의 페이지 테이블처럼, 조각난 물리적 블록 주소를 논리적으로 묶어줌.        |
|     - 유저 A의 문맥 --> 물리적 GPU 블록 1번 + 블록 3번 순서로 이어라!        |
|   * 글자가 길어져서 공간이 모자라면? 미리 예약하지 않고 그때그때 텅 빈         |
|     블록 4번을 툭 떼어서 테이블 포인터에 쓱 엮어주기만 하면 끝 (동적 할당)!     |
|   --> GPU 물리 메모리 구석구석 빈 공간(구멍) 없이 테트리스처럼 완벽히 꽉꽉 채워짐!|
+--------------------------------------------------------------+
```

<strong>핵심 원리 (<a href="/studynote/02_operating_system/02_process_thread/118_shared_memory/">공유 메모리</a> <a href="/studynote/02_operating_system/09_file_system/542_cow_file_system/">Copy-On-Write</a>)</strong>:
이 '블록 쪼개기([페이징](/studynote/02_operating_system/04_synchronization/259_paging/))'의 진짜 미친 마법은 <strong>메모리 공유(Memory Sharing)</strong>에서 터진다. 만약 10명의 유저가 "해리포터 1권 내용 요약해 줘!"라고 똑같은 프롬프트를 날렸다고 치자.
기존 방식은 10명에게 똑같이 해리포터 1권 분량의 KV [캐시 메모리](/studynote/01_computer_architecture/06_memory_hierarchy_cache/259_cache_memory/)(엄청난 용량)를 10번 복사해서 줬다. PagedAttention은 "어? 너희 10명 프롬프트 앞부분이 똑같네?"라며 물리적 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 메모리의 <strong>단 1개 블록(해리포터 문맥)</strong>을 10명의 Block Table이 가상 포인터로 같이 쳐다보게 만들어 버린다(공유). 그러다 유저 1명이 다른 문장을 뱉기 시작하면, 그때서야 자기만의 새 블록을 복사해서 떨어져 나가는 <strong><a href="/studynote/02_operating_system/09_file_system/542_cow_file_system/">Copy-On-Write</a> (<a href="/studynote/02_operating_system/09_file_system/542_cow_file_system/">COW</a>)</strong> OS 기법을 발동시킨다. 메모리 소모가 극단적으로 박살 난다.

| 요소 | 역할 |
|:---|:---|
| 입력 표현 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 토큰·벡터·[특성 맵](/studynote/10_ai/01_ai_basics/099_feature_map_activation_map_cnn_output/)으로 바꾸는 전처리 계층이다. |
| 모델 구조 | 정보를 축적·선택·[생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하는 핵심 계산 흐름을 담당한다. |
| 경량화 | 배포 환경에 맞춰 메모리와 연산량을 조정한다. |
| 응용 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | 검색, [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 추천, 제어 등 실제 문제 해결 단계로 이어진다. |

- **📢 섹션 요약 비유**: 기존 방식은 학교에서 선생님이 100명의 학생에게 각자 1권씩 똑같은 100페이지짜리 교과서(메모리)를 몽땅 복사해서 던져주느라 제본실([GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/))이 파산하는 구조다. PagedAttention([COW](/studynote/02_operating_system/09_file_system/542_cow_file_system/))은 100명의 학생 책상에 가상 포인터([모니터](/studynote/02_operating_system/04_synchronization/229_monitor/))만 놔두고, 교탁 위에 있는 단 1권의 교과서를 100명이 화면으로 똑같이 쳐다보게(공유) 만든다. 그러다 학생 1명이 "저는 교과서에 필기 좀 할게요" 할 때만, 그 학생을 위해 종이 1장을 새로 복사해 주는 궁극의 메모리 짠돌이 구두쇠 기법이다.

---

## Ⅲ. 비교 및 연결

[LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 서빙(추론)을 가속해서 서버비를 아끼고 속도를 올리려는 인프라 진영의 3대장 꼼수를 비교해 보면 PagedAttention의 위치가 명확해진다.

| [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 서빙 가속 기술 | 작동 철학 | 가장 큰 장점 (효과) | 한계점 (Trade-off) |
|:---|:---|:---|:---|
| <strong><a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/">양자화</a> (<a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/">Quantization</a> / AWQ 등)</strong> | 모델의 뇌세포 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 숫자를 정수(INT4)로 확 깎아내려 **뇌 크기 자체를 다이어트** 시킴 | 모델 크기가 1/4로 줄어들어 싸구려 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 1장에도 쏙 들어감 | 모델이 너무 심하게 멍청해져서 수학 문제나 복잡한 추론을 틀림 ([환각](/studynote/06_ict_convergence/04_ai_llm/275_react_framework/) 증가) |
| **FlashAttention (플래시 어텐션)** | [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 메모리(VRAM)와 아주 빠른 연산 캐시([SRAM](/studynote/01_computer_architecture/06_memory_hierarchy_cache/250_sram/)) 사이를 왔다 갔다 하는 <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 이동 횟수(I/O)를 타일링으로 쳐냄</strong> | 긴 [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/)(문서 10만 자)를 읽을 때 속도가 10배 폭발함 | 메모리 공간 낭비 자체(파편화)를 해결해주지는 못해서 동시 접속자 수 증가에는 한계가 있음 |
| **PagedAttention (vLLM / 본 기술)** | <strong>OS <a href="/studynote/02_operating_system/04_synchronization/259_paging/">페이징</a> 개념으로 KV 캐시 파편화를 없애</strong> 남는 메모리 구석구석을 테트리스로 채움 | <strong>서버 1대가 동시에 처리할 수 있는 유저 수(<a href="/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/">Throughput</a>)가 <a href="/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/">10</a>~20배 폭발함 (B2C <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>의 구세주)</strong> | 어텐션 공식([Kernel](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))을 마개조해야 해서 PagedAttention이 지원하지 않는 이상한 커스텀 모델에는 꽂아 넣을 수 없음 |

현대의 최첨단 [MLOps](/studynote/12_it_management/05_security_compliance/348_mlops/) 서빙 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인(예: TGI, TensorRT-[LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/), vLLM)은 이 3가지를 다 짬뽕한다. "AWQ로 모델을 깎아 넣고 + 안에서는 FlashAttention으로 계산하고 + 밖에서는 PagedAttention으로 수백 명의 동시 접속자를 테트리스로 욱여넣는" 완벽한 삼위일체 아키텍처가 글로벌 빅테크 서빙의 표준(De-facto Standard)으로 굳어졌다.

- **📢 섹션 요약 비유**: [양자화](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/)([Quantization](/studynote/01_computer_architecture/12_accelerators_ai_hardware/434_quantization/))는 배달 기사(모델)가 무거운 짐을 가볍게 포장지 다 뜯어내고 배달하는 거다(몸이 가벼워 빠르지만 물건이 좀 망가짐). FlashAttention은 기사가 트럭(VRAM)에서 짐을 내릴 때 왔다 갔다 10번 할 걸, 짐수레([SRAM](/studynote/01_computer_architecture/06_memory_hierarchy_cache/250_sram/))를 써서 1번 만에 다 나르는 꼼수다(동선 최적화). PagedAttention은 트럭 짐칸([GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 메모리)에 물건을 던져넣어 빈 공간이 숭숭 뚫려있던 걸, 테트리스 장인이 나타나 구석구석 빈틈없이 꽉꽉 채워 넣어 한 번에 20배 많은 물건(동시 유저)을 싣고 출발하게 만드는 '적재 공간 혁명'이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

스타트업이 B2C [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 챗봇 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 런칭하며 HuggingFace 디폴트 코드 그대로 LLM을 띄우면 10명만 들어와도 서버가 죽는다. 이때 vLLM을 도입하며 아키텍트가 조율해야 할 트레이드오프가 있다.

### 실무 아키텍처 판단 ([체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/))
1. **블록 사이즈 (Block Size) 최적화의 딜레마**: PagedAttention은 KV 캐시를 잘게 쪼갠다고 했다. 이 '블록 1개의 크기'를 16개 토큰 단위로 자를지, 32개 토큰 단위로 자를지가 시스템의 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 가른다. 블록을 너무 크게 잡으면(128토큰) 유저가 10토큰만 쓰고 끝날 경우 여전히 블록 안에 118칸의 빈 공간([내부 단편화](/studynote/02_operating_system/06_memory_management/341_internal_fragmentation/)) 낭비가 터진다. 반대로 너무 잘게 쪼개면(1토큰) 낭비는 0%지만, 이걸 가상으로 이어 붙이는 Block Table 맵핑 연산 오버헤드 때문에 GPU가 포인터 계산만 하다가 지쳐 쓰러진다. <strong>통상적으로 <code>block_size=16</code>이 가장 완벽한 메모리 낭비 4% 미만의 황금 비율(Golden Ratio)</strong>로 증명되었다.
2. <strong>동적 배칭(Continuous <a href="/studynote/05_database/06_dw_olap_trends/389_bulk_insert_batching_optimization/">Batching</a> / In-flight <a href="/studynote/05_database/06_dw_olap_trends/389_bulk_insert_batching_optimization/">Batching</a>) 융합 필수</strong>: PagedAttention이 메모리를 아껴줘서 공간이 남아도, 연산 엔진이 멍청하면 안 된다. 예전엔 A유저가 100글자 뽑고 B유저가 5글자 뽑을 때, 시스템이 100글자 끝날 때까지 다 같이 기다렸다가 한 번에 묶어서(Static Batch) 다음 턴으로 넘겼다. vLLM은 메모리를 쪼갠 김에, B유저가 5글자 뱉고 끝나서 빠져나가면 <strong>그 남는 자리에 0.1초 만에 새로 접속한 C유저를 중간에 휙 끼워 넣어 연산을 돌려버리는 '동적 연속 배칭(Continuous <a href="/studynote/05_database/06_dw_olap_trends/389_bulk_insert_batching_optimization/">Batching</a>)'</strong>을 결합해야 진정한 20배 [Throughput](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 폭발이 달성된다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong>단일 배치 추론(<a href="/studynote/10_ai/05_data_science_ml/346_batch_size_generalization/">Batch Size</a> 1) 환경에서의 오남용</strong>: vLLM과 PagedAttention은 '수백 명의 유저가 미친 듯이 몰려와서 동시 다발적으로 질문을 던질 때(High [Throughput](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리)' 메모리가 터지는 걸 막는 기술이다. 만약 로컬 PC에서 혼자 프라이빗하게 모델을 돌리거나([Batch Size](/studynote/10_ai/05_data_science_ml/346_batch_size_generalization/)=1), 실시간 대화가 아니라 오프라인에서 문서 1개를 깊게 요약하는 백그라운드 작업이라면? 이 복잡한 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 맵핑 연산(Overhead) 때문에 오히려 순수 파이토치 기본 코드보다 속도가 더 느려지는 끔찍한 역효과가 난다. 서빙 솔루션은 유저 트래픽 밀도에 맞춰 무기를 꺼내야 한다.

- **📢 섹션 요약 비유**: 연속 배칭(Continuous [Batching](/studynote/05_database/06_dw_olap_trends/389_bulk_insert_batching_optimization/))의 결합은 '지하철 회전율'이다. 옛날엔 10명이 지하철을 타면 이 10명이 전부 다 종점(문장 끝)에서 내릴 때까지 중간에 아무도 안 태우고 달렸다(Static Batch). 너무 비효율적이다. vLLM의 연속 배칭은 강남역에서 3명이 내리자마자 0.1초 만에 문을 열고 새로운 대기 손님 3명을 그 빈자리에 바로 밀어 넣고 달린다. PagedAttention이 '빈자리'를 찰떡같이 관리해주기 때문에 이런 중간 껴넣기가 가능해진 것이다.

---

## Ⅴ. 기대효과 및 결론

vLLM의 PagedAttention은 거대 언어 모델([LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)) 상용화 역사에서 가장 똑똑하고 찌질한(?) 인프라 공학의 승리다. 모델의 뇌(파라미터 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/))를 단 1%도 건드리지 않고, 오직 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 내부의 쓰레기처럼 버려지던 '메모리 구멍([Fragmentation](/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/))'들을 싹싹 긁어모아 꿰매는 하수도 배관 공사만으로 시스템 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 20배나 뻥튀기시킨 기적이기 때문이다.

이 기술이 세상에 공개된 2023년 이후, [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 서빙 생태계는 완전히 찢어졌다. 스타트업들은 한 달에 수천만 원씩 내던 H100 클라우드 [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 임대료를 단 1장으로 막아내며 B2C 챗봇 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 흑자로 전환할 수 있는 산소호흡기를 얻었다. 1960년대 컴퓨터 OS 할아버지들이 램(RAM) 1MB가 모자라서 벌벌 떨며 만들었던 낡은 '[가상 메모리](/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) [페이징](/studynote/02_operating_system/04_synchronization/259_paging/)' 철학이, 반세기가 지나 가장 최첨단의 [트랜스포머](/studynote/14_data_engineering/05_exam_keywords/246_transformer_self_attention_parallel_positional_encoding/) [인공지능](/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 가속기 위에서 화려하게 부활한 것이다.

결국 [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 시대의 진정한 승리자는 단순히 "모델 크기를 1조 개로 키운 자"가 아니다. 그 미치도록 무겁고 비싼 1조 개짜리 모델을 유저 수백만 명에게 버벅거림 없이, 낭비되는 메모리 1바이트 없이 완벽하게 서빙(Serving)할 수 있는 <strong>메모리 아키텍처 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/">오케스트레이션</a> 능력</strong>을 가진 자가 시장의 과금 패권을 쥐게 될 것이다. PagedAttention은 그 거대한 [LLMOps](/studynote/12_it_management/05_security_compliance/221_llmops_large_language_model_ops/) 비용 전쟁의 가장 완벽한 엑스칼리버 검이다.

- **📢 섹션 요약 비유**: PagedAttention은 [인공지능](/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) 인프라계의 '짐 싸기 달인(테트리스 고수)'이다. 똑같은 30인치 캐리어([GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 메모리)를 주더라도, 초보자는 신발과 옷을 대충 던져넣어서 5벌만 넣어도 꽉 찼다고 징징댄다(기존 KV 캐시). 하지만 테트리스 고수(vLLM)는 옷을 진공 팩(Block)으로 쪼개고 구석구석 빈 공간에 양말(포인터)을 끼워 넣어 무려 100벌을 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)해 싣고 유럽 여행(수백 명 동시 서빙)을 떠난다. 똑같은 가방(돈)으로 20배의 짐을 나르는 이 효율성이 기업을 살리는 마법이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/06_ict_convergence/04_ai_llm/291_kv_cache/">KV Cache</a> (키-밸류 캐시)</strong> | PagedAttention이 수술대에 올린 환자. 다음 글자를 뱉을 때 앞글자들의 계산(어텐션)을 재탕하려고 임시로 저장해 두는 거대한 메모리 쓰레기통이자 서빙 병목의 주범 |
| <strong><a href="/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/">운영체제</a> <a href="/studynote/02_operating_system/04_synchronization/259_paging/">페이징</a> (OS <a href="/studynote/02_operating_system/04_synchronization/259_paging/">Paging</a> / <a href="/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/">Virtual Memory</a>)</strong> | vLLM 논문이 훔쳐 온 위대한 조상님. 하드디스크와 램을 조각([Page](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)) 내어 가상 주소로 맵핑해서 메모리가 꽉 찬 것처럼 속이던 컴퓨터 구조 1원칙이 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 메모리로 재림함 |
| <strong><a href="/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/">Throughput</a> (동시 <a href="/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/">처리량</a>)</strong> | vLLM 도입의 유일한 목적. "1초에 글자를 얼마나 빨리 뱉나([Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))"가 아니라, "서버 1대가 동시에 유저 1,000명을 안 터지고 받아낼 수 있나?"를 측정하는 비용 효율 지표 |
| **FlashAttention (플래시 어텐션)** | 메모리 낭비를 줄이는 vLLM과 찰떡궁합을 이루는 친구. 얜 메모리 낭비를 막는 게 아니라 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 속도 렉을 막아줘서 둘이 같이 쓰면 용량과 속도가 동시에 폭발한다 |

### 📈 관련 키워드 및 발전 흐름도

```text
[입력 표현·특징 추출] -> [vLLM KV 캐시와 PagedAttention (KV Cache Pagedattention)] -> [경량화·멀티모달·서비스 적용]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 챗봇 로봇은 사람과 대화할 때 전에 했던 말을 까먹지 않으려고 수첩(KV 캐시)에 적어놔요. 근데 예전엔 <strong>수첩 100장짜리를 통째로 한 명한테 줘버려서 빈 종이가 엄청 낭비</strong>됐어요!
2. <strong><a href="/studynote/10_ai/04_ai_ops_ethics/338_vllm_paged_attention/">페이지드 어텐션</a>(PagedAttention)</strong> 기술은 수첩을 아예 가위로 한 장 한 장(블록) 오려뒀어요. 그리고 손님이 대화할 때마다 <strong>필요한 딱 한 장씩만 풀로 붙여서 연결</strong>해 주는 거예요!
3. 빈 종이가 하나도 안 버려지니까, 로봇은 남은 종이로 무려 <strong>20배나 더 많은 친구들</strong>과 동시에 대화를 나눌 수 있는 엄청난 인싸가 되었답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 223 / 420

<- **이전**: [222. 스케일 업(Scale-up) 스케일 아웃 파라미터 분산 로드](/studynote/10_ai/03_llm_nlp/222_scale_up_out_distributed_training/)
**다음**: [224. 하드웨어 가속 컴파일러 (TensorRT / ONNX)](/studynote/10_ai/03_llm_nlp/224_hardware_accelerator_tensorrt_onnx/) ->

---
