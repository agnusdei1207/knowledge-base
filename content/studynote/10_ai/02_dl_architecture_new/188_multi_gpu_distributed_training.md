---
title: 188. 멀티 GPU 분산 학습 전술 (데이터 vs 모델 병렬화)
date: '2026-05-09'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 멀티 [[418_gpu|GPU]] [[136_variance|분산]] 학습 전술은 거대한 딥러닝 모델이나 수백 기가의 훈련 [[001_dikw_pyramid|데이터]]가 [[418_gpu|GPU]] 1대의 좁은 VRAM(메모리)에 들어가지 않아 터지는 폭발([[157_oom_killer|OOM]])을 막기 위해, 수십~수백 대의 GPU를 엮어 무거운 짐을 **[[001_dikw_pyramid|데이터]] 단위로 쪼갤 것인가([[001_dikw_pyramid|데이터]] [[430_index_fast_full_scan|병렬]]화), 뇌 구조 단위로 쪼갤 것인가(모델 [[430_index_fast_full_scan|병렬]]화)**를 결정하는 [[348_mlops|MLOps]] 인프라 [[136_variance|분산]] 아키텍처다.
> 2. **가치**: 이 [[430_index_fast_full_scan|병렬]]화 전술 없이는 1,750억 개의 파라미터를 가진 [[302_gpt_autoregressive|GPT]]-3나 Llama 같은 초거대 언어 모델([[263_llm_large_language_model|LLM]])을 지구상의 그 어떤 슈퍼컴퓨터로도 훈련시킬 수 없다. 파라미터가 기하급수적으로 팽창하는 시대에 AI의 한계 돌파를 가능하게 한 1등 공신이다.
> 3. **판단 포인트**: 모델 크기가 [[418_gpu|GPU]] 1대에 들어간다면 무조건 훈련 속도를 수직으로 올리는 **'[[001_dikw_pyramid|데이터]] [[430_index_fast_full_scan|병렬]]화(DDP)'**를 써야 하지만, 모델 자체가 너무 비대해 1대에 담기지 않는다면 신경망을 레이어별로 토막 내어 [[418_gpu|GPU]] 1번, 2번, 3번에 나눠 담고 바통 터치를 하는 **'[[123_pipe|파이프]]라인 모델 [[430_index_fast_full_scan|병렬]]화([[015_payback_period|PP]]/TP)'** 혹은 **[[585_zero_skipping|Zero]](DeepSpeed)** 같은 초고도 쪼개기 마법을 설계해야만 한다.

---

## Ⅰ. 개요 및 필요성

딥러닝의 모델 정확도는 뇌(파라미터 [[267_weight_bias_activation|가중치]])의 크기와 쏟아붓는 [[001_dikw_pyramid|데이터]]의 양에 완벽히 비례하여 올라간다. 하지만 물리적인 하드웨어의 한계가 발목을 잡는다. 최상급 NVIDIA H100 [[418_gpu|GPU]] 1대의 램(VRAM)은 기껏해야 80GB다. 

만약 내가 훈련시킬 고양이 사진 [[001_dikw_pyramid|데이터]]가 1TB(1,000GB)라면 어떻게 해야 할까? 혹은 [[001_dikw_pyramid|데이터]]는 적은데 모델 파라미터 자체가 300GB라서 [[418_gpu|GPU]] 1대에 아예 올라타지도 못한다면? 
과거에는 [[267_weight_bias_activation|가중치]]를 강제로 [[434_quantization|양자화]]로 깎아버리거나 모델 크기를 포기했다. 하지만 인프라 엔지니어들은 이 물리적 족쇄를 끊어내기 위해 **"[[418_gpu|GPU]] 1대가 못 버티면, 8대를 묶어서 (80GB x 8 = 640GB) 하나의 거대한 뇌처럼 쓰자!"**라는 [[136_variance|분산]] 처리(Distributed [[588_mlops_pipeline_automation|Training]]) 클러스터링을 고안해 냈다.

문제는 수백 대의 GPU를 어떻게 효율적으로 갈구며 일을 시킬 것인가다. 일의 성격에 따라 [[001_dikw_pyramid|데이터]]의 산더미를 쪼개서 나눠줄지(**[[001_dikw_pyramid|Data]] Parallelism**), 아니면 거대한 프랑켄슈타인의 뇌 자체를 4등분 해서 수술대 4곳에 따로 눕혀놓고 훈련시킬지(**Model Parallelism**) 치열한 아키텍처 분기점이 발생한다.

```text
┌──────────────────────────────────────────────┐
│ Background Problem → Need → Adoption Value   │
├──────────────────────────────────────────────┤
│ Existing limitation │ Operational pressure   │
│ New requirement     │ Design decision point  │
└──────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 1명의 제빵사([[418_gpu|GPU]] 1대)가 감당 못 할 100만 개의 빵 주문이 들어왔다. **[[001_dikw_pyramid|데이터]] [[430_index_fast_full_scan|병렬]]화**는 똑같은 오븐(모델)을 가진 100명의 제빵사를 고용해, 반죽([[001_dikw_pyramid|데이터]]) 1만 개씩을 나눠주고 다 구운 빵(기울기)을 마지막에 한 곳에 모으는 다구리 전술이다. 반면 빵 1개의 크기가 너무 거대해서 오븐 1개에 안 들어간다면? **모델 [[430_index_fast_full_scan|병렬]]화**를 써서 1번 요리사는 반죽만(모델 앞부분), 2번 요리사는 굽기만(중간 부분), 3번 요리사는 포장만(뒷부분) 하도록 거대한 빵의 제작 공정 자체를 여러 오븐에 찢어버리는 컨베이어 벨트 전술이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

멀티 GPU를 다루는 두 가지 절대적 축인 [[001_dikw_pyramid|데이터]] [[430_index_fast_full_scan|병렬]]화(DP)와 모델 [[430_index_fast_full_scan|병렬]]화(MP/[[015_payback_period|PP]])의 동작 메커니즘을 뜯어보자.

```text
┌──────────────────────────────────────────────────────────────┐
│           멀티 GPU 훈련을 지배하는 양대 분산 아키텍처 (DDP vs PP)     │
├──────────────────────────────────────────────────────────────┤
│  [1. 데이터 병렬화 (Data Parallelism / DDP)]                 │
│   * 상황: 모델 뇌는 작은데, 데이터가 미친 듯이 많을 때.                   │
│   * 원리: 4대의 GPU에 똑같은 '쌍둥이 뇌(Model)' 4개를 복사해 둠!          │
│          거대한 데이터 더미를 1/4씩 쪼개서 각 GPU에 던져줌.              │
│   * 동기화(All-Reduce): 각 GPU가 따로 공부한 깨달음(Gradient 오차)을   │
│          가운데서 하나로 합쳐서(평균 내서), 다시 4대의 뇌에 똑같이 덮어씀.     │
│   * 무기: PyTorch의 Distributed Data Parallel (DDP) 표준!       │
│                                                              │
│  [2. 파이프라인 모델 병렬화 (Pipeline Model Parallelism / PP)] │
│   * 상황: 모델 뇌 자체가 100층짜리 트랜스포머라 GPU 1대에 안 들어갈 때.      │
│   * 원리: 신경망 뇌를 찢어발김!                                   │
│      ─▶ GPU 0번: 1~30층 담당 (사진 보고 귀 찾기)                │
│      ─▶ GPU 1번: 31~60층 담당 (눈, 코 찾기)                     │
│      ─▶ GPU 2번: 61~100층 담당 (최종 고양이 판별!)                 │
│   * 동기화: GPU 0번이 계산 끝나면 ─▶ 1번으로 바통 터치(통신 넘김) ─▶ 2번으로 넘김│
│            컨베이어 벨트처럼 뇌의 기억 조각이 통신선을 타고 릴레이 뜀!        │
└──────────────────────────────────────────────────────────────┘
```

**핵심 원리 (통신 병목과 링-올리듀스)**:
[[001_dikw_pyramid|데이터]] [[430_index_fast_full_scan|병렬]]화(DDP)의 약점은 4대의 GPU가 각자 훈련한 깨달음(Gradient)을 하나로 뭉칠 때 중앙 컨트롤 타워가 터져버린다는 것이다. 이를 막기 위해 최신 아키텍처는 중앙 서버를 폭파해 버리고, 4대의 GPU가 서로 동그란 원(Ring) 모양으로 손을 잡고 릴레이로 옆 사람에게만 자신의 깨달음을 전달해 순식간에 4명 모두 똑같은 뇌 지식을 공유하게 만드는 **링 올리듀스 (Ring All-Reduce / NCCL)** [[136_variance|분산]] 수학 [[001_algorithm_definition|알고리즘]]을 태워 통신 병목을 0으로 박살 냈다.

| 요소 | 역할 |
|:---|:---|
| [[075_loss_function_cost_function|손실 함수]] | 모델이 줄여야 할 오차를 정의하며 학습 방향을 만든다. |
| [[080_gradient_descent_learning_rate|학습률]] | 업데이트 폭을 결정해 수렴 속도와 발산 위험을 좌우한다. |
| 일반화 | 훈련 [[282_performance_tactics|성능]]이 아니라 실제 [[001_dikw_pyramid|데이터]] [[282_performance_tactics|성능]]으로 품질을 판단하게 만든다. |
| [[136_variance|분산]] 학습 | 대규모 모델에서 학습 속도와 자원 배치를 현실화한다. |

- **📢 섹션 요약 비유**: [[001_dikw_pyramid|데이터]] [[430_index_fast_full_scan|병렬]]화(DDP)의 [[212_synchronization_mechanisms|동기화]] 과정은 4명의 학생이 100쪽짜리 책을 25쪽씩 나눠서 공부한 다음, 둥글게 모여 앉아 서로 공부한 핵심 요약본 노트를 옆으로 옆으로 돌려 읽으며 10분 만에 4명 다 100쪽 분량의 완벽한 동일한 뇌([[267_weight_bias_activation|가중치]])를 장착하는 텔레파시 그룹 스터디다.

---

## Ⅲ. 비교 및 연결

실무에서 [[001_dikw_pyramid|데이터]]와 모델 크기에 따라 두 기술을 선택하거나, 끔찍한 단점을 메꾸기 위해 둘을 섞어버려야 한다.

| 아키텍처 비교 | [[001_dikw_pyramid|Data]] Parallel ([[001_dikw_pyramid|데이터]] [[430_index_fast_full_scan|병렬]]화 / DDP) | Model Parallel (모델 [[430_index_fast_full_scan|병렬]]화 / [[015_payback_period|PP]] & TP) |
|:---|:---|:---|
| **쪼개는 대상** | 거대한 훈련 **[[001_dikw_pyramid|데이터]]셋 (배치)** 덩어리 | 거대한 딥러닝 **모델(레이어 층)** 자체 |
| **[[418_gpu|GPU]] 내부 상태**| 4대 [[418_gpu|GPU]] 모두 **100% 완벽히 똑같은 뇌([[016_replication_factor|복제]]본)**를 가짐 | GPU마다 **각기 다른 뇌 조각(토막)**만 가지고 있음 |
| **병목 위험 요소**| 4대 GPU가 매 턴마다 엄청난 덩치의 오차(Gradient) 숫자를 서로 교환하느라 네트워크 랜선([[140_bandwidth|대역폭]])이 터짐 | [[418_gpu|GPU]] 0번이 앞단 계산을 끝낼 때까지 [[418_gpu|GPU]] 1번은 아무 일도 못 하고 손가락만 빠는 **버블(Bubble) 유휴 시간 지옥**이 터짐 |
| **최신 돌파구** | Ring All-Reduce [[001_algorithm_definition|알고리즘]]으로 네트워크 통신량 1/N 최적화 | [[123_pipe|파이프]]라인([[015_payback_period|PP]]) 기법으로 [[001_dikw_pyramid|데이터]]를 잘게 쪼개 연속으로 밀어 넣어 버블(쉬는 시간)을 0으로 채워버림 |

최근에는 [[418_gpu|GPU]] 1대에 안 들어가는 수천억 파라미터의 [[302_gpt_autoregressive|GPT]]-4를 훈련하기 위해, 세로로 층을 찢는 [[405_gpipe_pipeline_parallelism|파이프라인 병렬화]]([[015_payback_period|PP]])와, [[001_dikw_pyramid|데이터]] 배치도 찢는 [[001_dikw_pyramid|데이터]] [[430_index_fast_full_scan|병렬]]화(DDP), 심지어 행렬 계산 자체를 가로로 찢어버리는 텐서 [[430_index_fast_full_scan|병렬]]화(TP) 3가지를 한 방에 섞어버린 **3D [[430_index_fast_full_scan|병렬]]화 (3D Parallelism, Megatron-LM)** 구조가 거대 언어 모델([[263_llm_large_language_model|LLM]]) 인프라의 최종 보스(De Facto) 궤도로 천하를 통일했다.

- **📢 섹션 요약 비유**: 모델 [[405_gpipe_pipeline_parallelism|파이프라인 병렬화]]([[015_payback_period|PP]])의 가장 큰 버그인 버블(쉬는 시간) 현상은, 컨베이어 벨트에서 1번 작업자([[418_gpu|GPU]] 0)가 엔진 조립을 10분 동안 낑낑댈 때, 2번 작업자([[418_gpu|GPU]] 1)는 바퀴를 끼우려고 아무 일도 안 하고 10분 내내 서서 기다리는 지옥이다. 이 노는 시간을 없애려고, 1번이 엔진 조립을 아주 잘게(Micro-batch) 썰어서 1분마다 하나씩 2번에게 휙휙 던져주어 2번도 쉬지 않고 바퀴를 미친 듯이 끼우게 만드는 공정 [[208_schedule_history_transaction_execution_order|스케줄]]링 최적화가 MLOps의 밥줄이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

Pytorch 클러스터 환경에서 멀티 [[418_gpu|GPU]] 코드를 짤 때 주니어 엔지니어들이 가장 많이 치는 `DataParallel(DP)` 버그를 막아내고 인프라 요금을 지켜야 한다.

### 실무 아키텍처 판단 ([[435_checklist_based_testing|체크리스트]])
1. **구시대적 DP 폐기 및 DDP(Distributed [[001_dikw_pyramid|Data]] Parallel) 강제화**: 파이토치 초보자는 코드 한 줄로 멀티 GPU가 된다며 `nn.DataParallel(DP)` [[192_module_independence|모듈]]을 쓴다. 이건 0번 [[418_gpu|GPU]] 혼자 [[172_maas_mobility_as_a_service|마스]]터 역할을 하며 오차 계산을 다 짊어지고 1,2,3번 GPU에 뿌려대는 구식 싱글 프로세스/멀티 [[092_thread_lwp|스레드]] 병목 쓰레기 구조다. 0번 칩의 CPU가 터져 뻗어버린다. 기술사는 무조건 멀티 프로세스 기반으로 4대의 GPU가 동등한 권력으로 통신하는 **`nn.parallel.DistributedDataParallel (DDP)`** 클래스를 강제로 씌우도록 아키텍처 룰을 결계 쳐야 한다.
2. **DeepSpeed [[585_zero_skipping|Zero]] 최적화 도입 (최신 마법)**: DDP조차도 각 GPU가 거대한 쌍둥이 뇌 전체와 [[163_optimizer_sql_execution_plan_generator|옵티마이저]]([[277_adam_optimizer|Adam]])를 복사해 가져야 해서 VRAM 메모리 낭비가 4배로 극심하다. 마이크로소프트(Microsoft)가 개발한 **DeepSpeed ([[585_zero_skipping|ZeRO]], [[334_vram_zero_optimizer|Zero Redundancy Optimizer]])** [[336_library_vs_framework|라이브러리]]는, 4대의 GPU가 뇌 구조를 복사해서 갖지 않고 아주 영리하게 파편화([[179_table_partitioning_concept|Partitioning]])해서 나눠 가지게 하여, [[418_gpu|GPU]] 메모리를 수학적으로 획기적으로 비워버려 ([[585_zero_skipping|Zero]] 중복) 1,000억 개 파라미터 모델을 푼돈 클라우드에서도 돌아가게 만드는 현존 최고의 가성비 치트키다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- **NVLink/[[361_infiniband|InfiniBand]] 하드웨어 [[344_bus|버스]] 망각 [[352_defect_definition|결함]]**: 아무리 DDP와 DeepSpeed 코드를 완벽하게 짜놔도, 클라우드 인스턴스를 빌릴 때 싸구려 가상 네트워크로 묶인 GPU들을 대여하면 폭망한다. 8대의 GPU가 매 프레임마다 수십 GB의 오차 텐서(Gradient) 덩어리를 핑퐁 쳐야 하는데, 랜선이 느리면 [[418_gpu|GPU]] 코어는 연산을 1초 만에 끝내놓고 옆 GPU로 [[001_dikw_pyramid|데이터]] 보내는 데 10초를 낭비하며 멍을 때린다. 멀티 [[418_gpu|GPU]] 클러스터 훈련 시엔 무조건 GPU끼리 광속의 전용 차선으로 [[001_dikw_pyramid|데이터]]를 직접 꽂는 **엔비디아 NVLink 브릿지 커넥터**와 **[[361_infiniband|InfiniBand]] 네트워크 [[259_adapter_pattern_interface_wrapper|어댑터]]**가 장착된 노드를 [[528_provisioning|프로비저닝]] 해야만 선혈이 튀지 않는다.

- **📢 섹션 요약 비유**: 소프트웨어 [[136_variance|분산]] 처리 코드를 아무리 잘 짜놔도, 하드웨어 네트워크(NVLink)가 안 받쳐주면 소용이 없다. 100명의 천재 학자([[418_gpu|GPU]] 코어)를 모셔다 놓고 집단 토론(DDP 훈련)을 시키려는데, 학자들에게 최첨단 동시 무전기(NVLink)를 안 주고 비둘기 발목에 쪽지 묶어서 날리라고(싸구려 랜선) 시키면 토론이 100배 느려지는 끔찍한 병목이 터진다. 통신 속도가 [[136_variance|분산]] 학습의 병목 1순위다.

---

## Ⅴ. 기대효과 및 결론

멀티 [[418_gpu|GPU]] [[136_variance|분산]] 학습 전술의 안착은 [[231_ai_turing_test|인공지능]]의 스케일(Scale)을 무한대 차원으로 확장한 빅뱅의 방아쇠다. 만약 한 대의 GPU로만 훈련해야 하는 물리적 감옥에 갇혀있었다면, 오늘날 수백만 권의 위키백과를 통째로 읽고 추론하는 [[302_gpt_autoregressive|GPT]], Claude 같은 초거대 언어 모델([[263_llm_large_language_model|LLM]])이나, 전 세계의 도로 주행 영상을 집어삼키는 테슬라의 FSD 오토파일럿 신경망은 아예 시도조차 불가능했을 것이다.

[[001_dikw_pyramid|데이터]] [[430_index_fast_full_scan|병렬]]화(DDP)가 방대한 우주의 경험치([[001_dikw_pyramid|데이터]])를 무한의 속도로 소화할 수 있는 강력한 컨베이어 벨트를 깔아주었다면, 모델 [[430_index_fast_full_scan|병렬]]화([[015_payback_period|PP]], TP)와 [[585_zero_skipping|ZeRO]] 메모리 최적화는 한 대의 기계로는 결코 담을 수 없는 초월적인 거대 [[231_ai_turing_test|인공지능]] 뇌(파라미터)를 찢어서 [[136_variance|분산]] 배양하는 기적의 딥러닝 외과 수술이다. 결국 현대의 [[348_mlops|MLOps]] 백엔드 엔지니어링은 "단 1%의 [[418_gpu|GPU]] 코어도 통신 병목으로 놀게 내버려 두지 않겠다"는 철학 아래, 이 [[430_index_fast_full_scan|병렬]]화 기술들을 [[095_multithreading_benefits|다중 스레드]]로 교묘하게 엮어내는 [[073_container_orchestration_tools|오케스트레이션]] 예술의 정점으로 진화하고 있다.

- **📢 섹션 요약 비유**: [[136_variance|분산]] 학습 전술은 [[231_ai_turing_test|인공지능]]이라는 거인(프랑켄슈타인)을 배양하는 수술실이다. 100GB짜리 좁은 수조([[418_gpu|GPU]] 1대)에서는 절대 키울 수 없는 초거대 3,000GB짜리 거인의 뇌를 만들기 위해, 수백 개의 좁은 수조를 투명한 [[123_pipe|파이프]](NVLink 통신)로 연결해 [[001_dikw_pyramid|데이터]] 영양분(DDP)을 폭포처럼 쏟아붓고 뇌 부위를 나눠서 기르는([[015_payback_period|PP]]/TP) 것이다. 이 [[123_pipe|파이프]]라인의 밸브 조절 예술 덕분에 인류는 신의 뇌 용량을 닮은 초거대 [[225_foundation_model_peft_lora|파운데이션 모델]]([[225_foundation_model_peft_lora|Foundation Model]])을 기어이 깨우고야 말았다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **DDP ([[001_dikw_pyramid|데이터]] [[430_index_fast_full_scan|병렬]]화)** | 모델(뇌) 크기는 작지만 훈련 [[001_dikw_pyramid|데이터]]가 수백만 장일 때, 여러 대의 GPU에 뇌를 복사해 두고 훈련 [[001_dikw_pyramid|데이터]]를 N등분 해서 폭풍 [[136_variance|분산]] 학습시키는 가성비 국룰 기법 |
| **[[405_gpipe_pipeline_parallelism|파이프라인 병렬화]] ([[015_payback_period|PP]])** | 모델(뇌) 자체가 수백 층이라 한 GPU에 안 들어갈 때, 뇌 층을 썰어서 1번 GPU는 앞단 층만 계산, 2번 GPU는 뒷단 층만 계산하게 컨베이어 벨트 넘겨주기 하는 거대 훈련 기법 |
| **텐서 [[430_index_fast_full_scan|병렬]]화 (TP / Tensor Parallel)** | 아예 행렬 연산 곱셈 자체를 반으로 쪼개서, 왼쪽 곱셈은 1번 [[418_gpu|GPU]], 오른쪽 곱셈은 2번 GPU가 돌리고 0.1초 만에 더해버리는 가장 무식하고 엄청난 네트워크 [[140_bandwidth|대역폭]](통신속도)이 필요한 극한의 [[430_index_fast_full_scan|병렬]] [[136_variance|분산]]법 |
| **DeepSpeed ([[585_zero_skipping|ZeRO]] 최적화)** | 4대 GPU가 [[016_replication_factor|복제]]된 [[163_optimizer_sql_execution_plan_generator|옵티마이저]], 기울기를 들고 있어서 메모리가 낭비되는 바보짓을 고치기 위해, [[016_replication_factor|복제]]본을 지우고 1/4씩 찢어서 나눠 갖게 해 VRAM을 텅텅 비워버리는 마이크로소프트의 구세주 [[191_oss_license_compliance|오픈소스]] [[336_library_vs_framework|라이브러리]] |

### 📈 관련 키워드 및 발전 흐름도

```text
[손실 함수·기울기 계산] → [멀티 GPU 분산 학습 전술 (데이터 vs 모델 병렬화)] → [대규모 분산 학습·서빙 최적화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 1명의 로봇 요리사([[418_gpu|GPU]] 1대)가 100만 명분의 샌드위치를 혼자 만들면 허리가 부러져 쓰러져요.
2. **[[001_dikw_pyramid|데이터]] [[430_index_fast_full_scan|병렬]]화(DDP)** 전술은 로봇을 10명 [[016_replication_factor|복제]]해서 각자 10만 명분씩 똑같은 샌드위치를 미친 듯이 빠르게 만들게 시키는 마법이에요!
3. **모델 [[430_index_fast_full_scan|병렬]]화([[015_payback_period|PP]])** 전술은 샌드위치가 코끼리만 하게 너무 거대할 때, 1번 로봇은 빵만 자르고 2번 로봇은 치즈만 올리고 3번 로봇은 햄만 올려서, 로봇들끼리 컨베이어 벨트로 넘겨가며 거대 샌드위치를 완성하는 멋진 분업 작전이랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 188 / 420

← **이전**: [[187_mixed_precision_training|187. 혼합 정밀도 훈련 (Mixed Precision Training)]]
**다음**: [[189_zero_deepspeed|189. ZeRO (Zero Redundancy Optimizer)]] →

---
