---
title: 202. 온디바이스 AI (On-Device AI)
date: '2026-05-09'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 온디바이스 [[190_ai_llm_requirements_specification|AI]] ([[635_on_device_ai|On-Device AI]])는 사용자의 스마트폰, 노트북, 자율주행차 안에서 **외부 클라우드 인터넷(Wi-Fi, [[418_5g_embb_urllc_mmtc_slicing|5G]]) 연결 없이 오직 기기 자체에 내장된 칩셋([[424_npu|NPU]]/[[418_gpu|GPU]])만으로 [[231_ai_turing_test|인공지능]] 추론(Inference)을 100% 로컬에서 돌려버리는 독립 생태계 기술**이다.
> 2. **가치**: "시리야" 하고 물었을 때 [[001_dikw_pyramid|데이터]]가 미국 구글/애플 서버로 넘어갔다 오는 1초의 [[015_지연_데이터_관점|지연]]([[141_latency|Latency]])과 심각한 개인 사생활(Privacy) 유출 공포를 한 방에 삭제했다. 비행기 모드나 산속에서도 0.01초 만에 외국어 동시통역이 터져 나오는 미친 반응 속도의 기적을 창조했다.
> 3. **판단 포인트**: 100GB가 넘는 거대 [[190_ai_llm_requirements_specification|AI]] 뇌(파라미터)를 손바닥만 한 스마트폰 램(RAM 8GB)에 쑤셔 넣는 것은 물리적으로 불가능하므로, 파라미터 소수점을 싹둑 자르는 **[[434_quantization|양자화]]([[434_quantization|Quantization]])**와 작은 모델에 똑똑함을 이식하는 **[[252_knowledge_distillation_quantization_edge_slm_diffusion|지식 증류]]([[252_knowledge_distillation_quantization_edge_slm_diffusion|Knowledge Distillation]])** 등 영혼의 다이어트 경량화 아키텍처가 제품 상용화의 유일한 [[172_maas_mobility_as_a_service|마스]]터키다.

---

## Ⅰ. 개요 및 필요성

2020년 이전의 [[231_ai_turing_test|인공지능]]은 100% '클라우드 인공호흡기'에 의존하는 환자였다. 
사용자가 핸드폰에 대고 "이 꽃 이름이 뭐야?"라고 사진을 찍으면, 그 무거운 사진 [[001_dikw_pyramid|데이터]]는 [[418_5g_embb_urllc_mmtc_slicing|5G]] 망을 타고 바다 건너 미국의 거대한 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]](클라우드 서버)로 날아간다. 수만 대의 H100 GPU가 돌아가며 "이건 장미야!"라고 정답을 계산한 뒤, 다시 바다를 건너 내 스마트폰 화면에 글씨를 뿌려주었다.

이 방식은 세 가지 치명적인 재앙을 불렀다. 첫째, [[141_latency|지연 시간]]([[141_latency|Latency]])이다. 시속 100km로 달리는 자율주행차가 보행자를 보고 클라우드에 "브레이크 밟을까요?"라고 물어보고 답변을 기다리면 이미 보행자를 친 후다. 둘째, 보안(Privacy)이다. 내 침실의 홈 [[933_cctv|CCTV]] 영상이나 회사의 기밀 회의 녹음 [[501_file_definition_logical_record|파일]]이 구글 서버로 넘어가는 것을 사람들은 견디지 못했다. 셋째, 서버비(Cost) 파산이다. 전 세계 10억 명이 매일 챗GPT에 물어볼 때마다 오픈AI는 천문학적인 [[418_gpu|GPU]] 전기세를 내야 했다.

이 세 가지 지옥을 단번에 부수기 위해 애플(Apple)과 삼성, 퀄컴이 하드웨어 반란을 일으켰다. **"통신 선을 다 뽑아버려! 딥러닝 뇌를 아예 스마트폰 칩셋([[572_ap_access_point_ds_distribution_system|AP]]) 안에 구겨 넣어버려서 폰 자체가 하나의 작은 [[231_ai_turing_test|인공지능]]이 되게 만들자!"** 이것이 삼성이 갤럭시 S24에 '가우스(Gauss)'를 때려 박고, 애플이 아이폰에 '애플 인텔리전스'를 박아 넣은 **온디바이스 [[190_ai_llm_requirements_specification|AI]] ([[635_on_device_ai|On-Device AI]])** 시대의 거대한 서막이다.

```text
┌──────────────────────────────────────────────┐
│ Background Problem → Need → Adoption Value   │
├──────────────────────────────────────────────┤
│ Existing limitation │ Operational pressure   │
│ New requirement     │ Design decision point  │
└──────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 옛날 AI는 학교에서 모르는 문제가 나오면, 시험 도중에 비행기를 타고 미국에 있는 아인슈타인(클라우드)에게 물어보고 와서 답을 적는 멍청한 방식이었다. 온디바이스 AI는 아인슈타인의 뇌를 복사해서 내 주머니 속 커닝 페이퍼([[424_npu|NPU]])에 [[347_compaction|압축]]해 넣어둔 것이다. 비행기를 탈 필요도 없고([[015_지연_데이터_관점|지연]] 0초), 내가 무슨 문제를 틀렸는지 미국이 알 길도 없으며(프라이버시), 지하실에 갇혀 인터넷이 끊겨도 완벽한 정답을 0.1초 만에 척척 풀어내는 절대 반지다.

---

## Ⅱ. 아키텍처 및 핵심 원리

온디바이스 AI의 본질은 무거운 딥러닝 모델의 수학 공식을 스마트폰 배터리로 굴릴 수 있도록 밑바닥 하드웨어와 소프트웨어를 양쪽에서 갈아엎는 처절한 수술이다.

```text
┌──────────────────────────────────────────────────────────────┐
│           온디바이스 AI (On-Device AI) 경량화 및 엣지 구동 아키텍처 도해 │
├──────────────────────────────────────────────────────────────┤
│  [1. 클라우드의 거인 (Training & Compression)]                     │
│   * 수천억 개 파라미터 GPT-4 뇌 (크기: 300GB) ─▶ 폰에 절대 안 들어감!  │
│   * 영혼의 다이어트 발동 (소프트웨어):                                │
│     ▶ 가지치기(Pruning): 바보 같은 뉴런 시냅스 선을 가위로 싹둑 잘라냄.     │
│     ▶ 지식 증류(KD): GPT-4의 지식을 80억 개짜리 꼬마 Llama 3 뇌로 복사함. │
│     ▶ 양자화(INT4): 3.141592(32비트)를 '대충 3(4비트)'으로 찌그러뜨림.   │
│   * ─▶ 짠! 모델 크기가 300GB에서 스마트폰에 쏙 들어가는 4GB로 폭풍 압축 완료! │
│                                                              │
│  [2. 스마트폰 런타임 (On-Device NPU 추론)]                        │
│   * 4GB로 찌그러진 모델 뇌가 스마트폰의 메인보드 램(RAM)에 상주함.         │
│   * 사용자가 "비행기 모드(통신 차단)" 상태에서 "영어를 한국어로 통역해 줘" 요청!│
│   * CPU나 GPU 대신, 전기를 1W만 먹는 'NPU(신경망 전용칩)'가 깨어나서      │
│     0.01초 만에 100% 로컬 오프라인 통역 연산을 끝내고 답변을 뱉어냄!        │
└──────────────────────────────────────────────────────────────┘
```

**핵심 원리 ([[424_npu|NPU]] 하드웨어 가속과 [[424_npu|NPU]] 런타임)**:
아무리 모델을 4GB로 줄여도 폰에 있는 CPU로 계산하면 핸드폰이 불덩이처럼 뜨거워지며 1시간 만에 배터리가 0%가 된다. 그래서 스마트폰 두뇌([[572_ap_access_point_ds_distribution_system|AP]]) 안에 **[[424_npu|NPU]] ([[424_npu|Neural Processing Unit]], 신경망 전용 칩)**라는 독방을 하나 만들어 두었다. 퀄컴의 헥사곤(Hexagon)이나 애플의 뉴럴 엔진(Neural Engine)이 그것이다. NPU는 복잡한 인터넷이나 게임 기능은 전혀 못 하지만, 오직 딥러닝 행렬 곱셈 하나만은 전기를 거의 안 먹고 빛의 속도로 씹어 먹는다. 텐서플로우 라이트(TFLite)나 코어ML(CoreML) 같은 모바일 전용 변환기(Runtime)가 딥러닝 코드를 이 [[424_npu|NPU]] 기계어로 완벽히 번역해 꽂아 넣어주는 것이 기술의 심장이다.

| 요소 | 역할 |
|:---|:---|
| 입력 표현 | [[001_dikw_pyramid|데이터]]를 토큰·벡터·[[099_feature_map_activation_map_cnn_output|특성 맵]]으로 바꾸는 전처리 계층이다. |
| 모델 구조 | 정보를 축적·선택·[[087_process_state_transition|생성]]하는 핵심 계산 흐름을 담당한다. |
| 경량화 | 배포 환경에 맞춰 메모리와 연산량을 조정한다. |
| 응용 [[090_service_kubernetes_network_load_balancing|서비스]] | 검색, [[087_process_state_transition|생성]], 추천, 제어 등 실제 문제 해결 단계로 이어진다. |

- **📢 섹션 요약 비유**: 온디바이스 AI는 1,000페이지짜리 엄청나게 무겁고 두꺼운 요리 백과사전(클라우드 [[190_ai_llm_requirements_specification|AI]])을, 핵심만 뽑아 손바닥만 한 10페이지짜리 요약 수첩(경량화 모델)으로 찢어 만드는 과정이다. 그리고 이 수첩을 스마트폰이라는 아주 작지만 요리 속도는 미친 듯이 빠른 전용 전자레인지([[424_npu|NPU]])에 넣고 돌리면, 1초 만에 인터넷 검색 없이 뚝딱 완벽한 요리가 나오는 환상의 콤비다.

---

## Ⅲ. 비교 및 연결

[[001_dikw_pyramid|데이터]]의 처리 위치에 따라 클라우드(Cloud), 엣지(Edge), 온디바이스(On-Device) 3대 컴퓨팅 아키텍처가 전쟁 중이다.

| 컴퓨팅 패러다임 | 클라우드 [[190_ai_llm_requirements_specification|AI]] (Cloud) | [[235_edge_computing_smart_factory|엣지 컴퓨팅]] [[190_ai_llm_requirements_specification|AI]] (Edge) | 온디바이스 [[190_ai_llm_requirements_specification|AI]] (On-Device) |
|:---|:---|:---|:---|
| **두뇌의 물리적 위치**| 태평양 건너 구글/AWS [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] | 집 앞 통신사 기지국이나 공장 서버실 | **내 주머니 속 스마트폰, 내 손목 스마트워치 칩 안** |
| **응답 [[015_지연_데이터_관점|지연]] ([[141_latency|Latency]])**| 1초 ~ 3초 (가장 느림) | 0.05초 (매우 빠름) | **0.001초 (미친 반사 신경, [[585_zero_skipping|Zero]] [[141_latency|Latency]])** |
| **[[781_personal_information|개인정보]] 유출 (Privacy)**| 모든 정보가 바다를 건너 서버에 기록됨 (위험) | 암호화되어 근처 기지국까지만 감 | **절대 폰 밖을 나가지 않음 (100% 철통 보안)** |
| **구동 가능한 모델 한계**| 수천억 파라미터 1조 개 [[302_gpt_autoregressive|GPT]]-4 (우주 최고 똑똑함) | 수백억 파라미터 수준 (준수함) | **10억 ~ 80억 (1B~8B) 파라미터 소형 모델([[313_slm|SLM]]) 한계 (특정 임무만 잘함)** |
| **치명적 약점** | 인터넷(Wi-Fi) 끊기면 아예 죽은 벽돌이 됨 | [[459_quic_fec_forward_error_correction|초기]] 서버 인프라 구축 비용 비쌈 | **스마트폰 배터리 용량과 램(RAM) 크기의 절대적 제약** |

오늘날 거대 IT 기업들은 이 흑백 [[369_logic_bomb|논리]]에서 벗어나 **하이브리드(Hybrid) [[190_ai_llm_requirements_specification|AI]] 아키텍처**로 진화했다. 사용자가 폰으로 "오늘 알람 맞춰줘" 같은 간단하고 개인적인(Privacy) 명령을 내리면 온디바이스 AI가 0.1초 만에 통신 없이 처리하고, "양자역학의 기원을 논문으로 요약해 줘" 같은 엄청난 지식이 필요한 미션이 들어오면 폰의 뇌가 포기하고 몰래 클라우드 [[302_gpt_autoregressive|GPT]]-4로 바통 터치를 해서 대답을 가져오는([[339_routing_overview_best_path_selection|Routing]]) 지능적 스위칭 시스템이 대세다.

- **📢 섹션 요약 비유**: 클라우드 AI가 서울 대학병원의 수석 박사님이라면(엄청 똑똑하지만 예약 대기 길고 돈 많이 듦), 온디바이스 AI는 우리 집 거실에 상주하는 주치의 선생님이다. 내가 감기 기운(간단한 추론)이 있으면 거실에서 1초 만에 약을 처방해 주지만, 내 병이 심각한 암(고차원 추론)이라고 판단되면 주치의가 알아서 서울 대학병원(클라우드)으로 환자를 이송해 주는 완벽한 협진 시스템(하이브리드 [[190_ai_llm_requirements_specification|AI]])이 구축되고 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

안드로이드나 iOS 모바일 앱에 실시간 객체 인식이나 번역 AI를 얹을 때, 주니어 앱 개발자가 가장 많이 일으키는 대참사는 RAM 폭파와 배터리 광탈이다.

### 실무 아키텍처 판단 ([[435_checklist_based_testing|체크리스트]])
1. **Int8 [[434_quantization|양자화]] 추론([[434_quantization|Quantization]]-Aware [[588_mlops_pipeline_automation|Training]]) [[123_pipe|파이프]]라인**: 훈련된 PyTorch 모델을 그대로 폰에 올리는 건 앱을 터뜨리는 짓이다. 안드로이드 NNAPI나 iOS CoreML 포맷으로 변환할 때, 모델의 모든 [[267_weight_bias_activation|가중치]] 32비트 소수점을 8비트 정수(Int8)로 깎아버리는 [[434_quantization|양자화]](PTQ)를 반드시 먹여야 모델 크기가 1/4로 [[347_compaction|압축]]되고 NPU가 비로소 굉음을 내며 가속한다. 단, 소수점을 쳐냈을 때 모델 정확도가 폭락한다면, 훈련할 때부터 미리 8비트로 깎일 것을 대비해 맷집을 키워 훈련하는 **QAT ([[434_quantization|양자화]] 인지 학습)** [[123_pipe|파이프]]라인으로 [[348_mlops|MLOps]] 백엔드를 재설계해야 한다.
2. **동적 메모리([[291_kv_cache|KV Cache]]) 폭발 [[656_ir_containment|억제]] 룰**: 작은 언어 모델([[313_slm|SLM]])을 폰에 쑤셔 넣었다 하더라도, 유저가 채팅을 1시간 동안 계속 이어나가면 모델이 과거의 대화를 기억하기 위해 램에 쌓아두는 'KV 캐시' 텐서가 기하급수적으로 폭발해 폰이 다운된다. 모바일 환경에선 토큰 길이가 2,048을 넘어가면 강제로 낡은 대화 기억([[033_context|Context]])을 앞부분부터 [[261_fifo_page_replacement|FIFO]](선입선출)로 버려버리거나, 캐시를 4비트로 또 [[347_compaction|압축]]해 버리는 극단적인 메모리 리미트 하드코딩 락([[510_lock|Lock]])을 걸어야 배포 심사를 통과할 수 있다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- **[[001_operating_system_purpose|운영체제]](OS) 백그라운드 킬러의 무지성 무시**: 스마트폰 OS(iOS, Android)는 앱이 백그라운드로 내려가거나 메모리를 너무 많이 쳐먹으면 배터리를 살리기 위해 가차 없이 앱 프로세스([[190_ai_llm_requirements_specification|AI]] 모델)의 목을 쳐버린다([[425_oom_killer_score|OOM Killer]]). 앱 개발자가 [[190_ai_llm_requirements_specification|AI]] 모델 추론 로직을 메인 [[092_thread_lwp|스레드]](UI [[092_thread_lwp|Thread]])에 올려버리면 화면이 버벅대다 앱이 강제 종료되는 코미디가 발생한다. 무조건 [[190_ai_llm_requirements_specification|AI]] 텐서 연산은 비동기 백그라운드 워커 [[092_thread_lwp|스레드]](Background [[092_thread_lwp|Thread]])로 완전히 찢어서(Decoupling) 돌리고, OS가 모델을 죽여버려도 재시작 시 아주 빠르게 모델의 [[267_weight_bias_activation|가중치]]를 램에 다시 로딩할 수 있도록 메모리 맵([[749_memory_mapped_file_mmap|mmap]]) I/O 최적화를 걸어둬야 생존한다.

- **📢 섹션 요약 비유**: 스마트폰의 램(RAM) 공간은 아주 좁고 까탈스러운 1인용 텐트다. 뚱뚱한 곰(32비트 모델)을 그대로 텐트에 쑤셔 넣으면 텐트가 찢어진다([[157_oom_killer|OOM]] 강제 종료). 무조건 곰을 8비트 다이어트([[434_quantization|양자화]])시켜 날씬하게 만든 다음 넣어야 한다. 게다가 곰이 텐트 안에서 밥을 계속 먹으며 똥([[291_kv_cache|KV Cache]] 기억)을 싸면 다시 텐트가 터지니까, 일정량 이상 쌓이면 무조건 밖으로 버려버리는 청소 규칙을 짜놓지 않으면 스마트폰 배터리가 30분 만에 녹아내린다.

---

## Ⅴ. 기대효과 및 결론

온디바이스 [[190_ai_llm_requirements_specification|AI]]([[635_on_device_ai|On-Device AI]])의 완성은 구글과 오픈AI 같은 클라우드 거대 독점 기업이 쥐고 있던 '지능의 권력'을 전 세계 수십억 명의 개인 주머니 속으로 완벽하게 [[136_variance|분산]]([[010_decentralization|Decentralization]])시킨 민주주의 혁명이다.

이제 우리는 나만의 비밀 일기장이나 회사 극비 문서를 읽고 회의록을 요약해 주는 AI를 쓰면서도, 구글 서버에 내 [[001_dikw_pyramid|데이터]]가 해킹될까 봐 덜덜 떨지 않아도 된다. 내 스마트폰의 칩([[424_npu|NPU]])이 인터넷 선을 끊은 방구석 오프라인 상태에서도 완벽하게 문서를 읽고 스스로 파쇄해 버리는 100% 에어갭([[102_air_gapped_cicd_tarball_delivery|Air-gapped]]) 보안을 실현했기 때문이다. 또한, 지구상 인터넷이 터지지 않는 사하라 사막 한가운데서도 의료 진단 AI와 동시통역기를 꺼내 쓸 수 있게 된 이 경이로운 이동성(Mobility)은 인류의 지식 격차를 산산조각 내버렸다.

미래의 온디바이스 AI는 단순히 나 혼자 똑똑한 것을 넘어, 근처에 있는 친구의 아이폰과 내 갤럭시가 [[605_bluetooth_ieee_802_15_1_piconet_scatternet|블루투스]]로 몰래 대화를 나누며 각자 배운 지식을 암호화해 교환하는 **[[256_federated_learning_privacy_model_security|연합 학습]]([[256_federated_learning_privacy_model_security|Federated Learning]])**의 거대한 글로벌 거미줄 뇌망([[544_hive|Hive]] Mind)으로 진화하고 있다. [[001_dikw_pyramid|데이터]]의 주권은 영원히 내 주머니에 둔 채, 지능의 속도는 빛처럼 폭발하는 시대. 온디바이스 AI는 인류 역사상 가장 사적이고 완벽한 나만의 절대 비서의 탄생이다.

- **📢 섹션 요약 비유**: 클라우드 [[190_ai_llm_requirements_specification|AI]] 시대에는 [[231_ai_turing_test|인공지능]]이 저 멀리 성벽([[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]]) 안에 갇힌 신탁의 마법사였다. 우리는 비밀을 말하고 마법사가 대답해 주기를 두려움에 떨며 며칠을 기다렸다. 온디바이스 AI는 그 거대한 마법사의 능력을 엄지손가락만 한 요정으로 [[347_compaction|압축]]해, 우리 모두의 주머니 속에 1마리씩 공짜로 분양해 준 기적이다. 이 요정은 절대 내 비밀을 남에게 발설하지 않고, 내가 부르면 비행기 안이든 우주든 0.1초 만에 튀어나와 정답을 바치는 나만의 영원한 충신이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[424_npu|NPU]] (신경망 전용 칩)** | 스마트폰 칩셋([[572_ap_access_point_ds_distribution_system|AP]]) 안에 숨겨져 있는 [[231_ai_turing_test|인공지능]] 연산 전용 괴물 모터. 전기는 거의 안 먹으면서 행렬 곱셈을 광속으로 처리해 온디바이스 AI가 배터리 방전 없이 살아 숨 쉬게 하는 물리적 심장 |
| **[[434_quantization|양자화]] ([[434_quantization|Quantization]])** | 모델 [[267_weight_bias_activation|가중치]]의 무거운 32비트 소수점을 날려버리고 8비트나 4비트 정수로 뭉툭하게 깎아내려, 모델의 크기를 1/4로 박살 내 스마트폰의 좁은 램(RAM)에 억지로 쑤셔 넣는 영혼의 다이어트 마법 |
| **[[313_slm|SLM]] (소형 언어 모델)** | 수천억 개의 파라미터가 폰에 안 들어가니까, 아예 80억 개(8B) 수준으로 덩치를 극단적으로 줄이되 [[001_dikw_pyramid|데이터]] 질을 높여 폰 안에서 거대 모델처럼 유창하게 떠들게 만든 꼬마 천재 [[246_transformer_self_attention_parallel_positional_encoding|트랜스포머]] |
| **[[256_federated_learning_privacy_model_security|연합 학습]] ([[256_federated_learning_privacy_model_security|Federated Learning]])** | 내 폰 안에서 온디바이스 AI가 공부한 똑똑해진 지혜([[267_weight_bias_activation|가중치]] 업데이트 값)만을 뽑아내서 중앙 구글 서버로 쏘아 올려, 내 카톡 원본은 절대 털리지 않으면서도 글로벌 AI를 훈련시키는 보안 [[123_pipe|파이프]]라인 |

### 📈 관련 키워드 및 발전 흐름도

```text
[입력 표현·특징 추출] → [온디바이스 AI (On-Device AI)] → [경량화·멀티모달·서비스 적용]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 옛날엔 폰에서 [[231_ai_turing_test|인공지능]] 번역기를 쓰려면, 폰이 와이파이를 타고 미국 구글 본사까지 헤엄쳐서 답을 물어보고 와야 해서 인터넷이 안 터지면 완전 바보 벽돌이 됐어요.
2. 온디바이스 AI는 구글 본사의 거대한 [[231_ai_turing_test|인공지능]] 뇌를 마법으로 엄청 작게 [[347_compaction|압축]]해서 **내 핸드폰 안에 통째로 이식시켜버린 기적**이에요!
3. 이제 비행기 모드를 켜고 인터넷 선을 확! 뽑아버려도, 폰 안에 갇힌 요정([[424_npu|NPU]] 칩)이 스스로 생각하고 1초 만에 영어 통역을 줄줄 읊어대는 나만의 영원한 첩보 요원이 되었답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 202 / 420

← **이전**: [[201_neuromorphic_computing|201. 뉴로모픽 컴퓨팅 (Neuromorphic Computing)]]
**다음**: [[203_slm_small_language_model|203. 슬림 언어 모델 (SLM, Small Language Model)]] →

---
