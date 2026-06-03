---
title: 212. 오토인코더 (Autoencoder) 구조
date: '2026-05-09'
tags:
- studynote-ai
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[335_autoencoder|오토인코더]] ([[335_autoencoder|Autoencoder]])는 입력 [[001_dikw_pyramid|데이터]](사진, 소리)를 모래시계처럼 좁아지는 '[[040_encoder|인코더]]([[040_encoder|Encoder]])'를 통해 핵심 진액(잠재 공간 벡터 $Z$)으로 꾹꾹 짓눌러 [[347_compaction|압축]]한 뒤, 다시 '[[039_decoder|디코더]]([[039_decoder|Decoder]])'를 통해 원래의 사진과 똑같은 모습으로 부풀려 복원해 내는 **[[122_unsupervised_learning|비지도 학습]](Unsupervised) 기반의 [[347_compaction|압축]] 및 복원 딥러닝 뼈대 구조**다.
> 2. **가치**: "정답(Label)이 없는 수백만 장의 쓰레기 [[001_dikw_pyramid|데이터]]"를 줘도, AI가 자기 스스로 "어떻게 [[347_compaction|압축]]했다가 복원해야 원본이랑 똑같아질까?"를 고민하며 [[001_dikw_pyramid|데이터]]의 숨겨진 우주의 규칙(핵심 특징 [[247_feature_label_variables|피처]])을 스스로 깨우쳐내는 특징 추출(Feature Extraction)의 절대적 황제다.
> 3. **판단 포인트**: [[001_dikw_pyramid|데이터]]를 통과시킬 때 미세한 노이즈(먼지)를 섞어 넣고 "먼지를 무시하고 원본으로 복원해 봐!"라고 가혹하게 훈련시키는 **Denoising [[335_autoencoder|Autoencoder]](DAE)** 기법을 붙이면, 이 모델은 흐릿한 옛날 사진을 4K 초고화질로 깎아주거나 기계의 미세한 진동을 감지하는 [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]]([[111_anomaly_detection|Anomaly Detection]]) 괴물로 각성한다.

---

## Ⅰ. 개요 및 필요성

고양이 사진을 주고 "이건 고양이야"라고 사람이 하나하나 정답표(Label)를 달아주는 [[121_supervised_learning|지도 학습]](Supervised)은 완벽하지만, 사람의 인건비가 너무 비싸서 파산하기 딱 좋은 방법이다. 세상에 굴러다니는 99%의 [[933_cctv|CCTV]] 영상과 텍스트는 정답표가 없는 그냥 '날것의 [[001_dikw_pyramid|데이터]](Unlabeled)'다. 

학자들은 고민했다. **"정답을 안 가르쳐주고도, 딥러닝이 [[001_dikw_pyramid|데이터]] 스스로의 생김새(특징)를 독학하게 만들 수는 없을까?"** 
이 천재적인 역발상에서 튀어나온 것이 **[[335_autoencoder|오토인코더]] ([[335_autoencoder|Autoencoder]])**다. 모델에게 고양이 사진을 10만 장 던져주고 이렇게 명령한다. "내가 정답은 안 알려줄 건데, 네가 이 100만 픽셀짜리 고양이 사진을 겨우 100개의 숫자([[347_compaction|압축]] 벡터)로 엄청나게 찌그러뜨렸다가, 다시 100만 픽셀짜리 똑같은 고양이 사진으로 완벽하게 그려서(복원해서) 나한테 제출해 봐!" 

이 미친 [[347_compaction|압축]]과 복원의 고문을 견디기 위해, 인공신경망 뇌는 고양이의 배경(하늘, 풀밭) 같은 쓸데없는 정보는 눈물을 머금고 다 쳐내버리고, 오직 고양이의 뾰족한 귀, 둥근 눈동자 같은 **'절대 까먹으면 안 되는 가장 중요한 핵심 알맹이(Feature)'**만 병목 구간에 필사적으로 살아남게 보존하는 생존 본능을 발휘한다. 이것이 정답 없이 세상을 스스로 깨우치는 [[081_dimensionality_reduction_pca_principal_component_analysis|차원 축소]]([[347_compaction|압축]])의 기적이다.

```text
┌──────────────────────────────────────────────┐
│ Background Problem → Need → Adoption Value   │
├──────────────────────────────────────────────┤
│ Existing limitation │ Operational pressure   │
│ New requirement     │ Design decision point  │
└──────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[335_autoencoder|오토인코더]]는 천재 화가에게 치는 가장 가혹한 장난이다. 거대한 풍경화를 보여준 다음, 화가의 손에 아주 얇은 포스트잇 종이 1장(병목 [[347_compaction|압축]] 공간 $Z$)만 주고 그 풍경을 메모하라고 시킨다. 1시간 뒤 풍경화를 싹 치워버리고, "아까 네가 포스트잇에 적은 메모만 보고 원본 풍경화를 100% 똑같이 다시 그려내(복원)!"라고 명령한다. 화가는 포스트잇에 쓸데없는 구름이나 나뭇잎 개수 따윈 적지 않고, 오직 "큰 산 1개, 강물 1개"라는 진짜 핵심 뼈대 정보만 꾹꾹 [[347_compaction|압축]]해서 적어둘 것이다. 이 강제된 [[347_compaction|압축]] 능력이 바로 [[335_autoencoder|오토인코더]]가 세상의 본질을 파악하는 핵심 원리다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[335_autoencoder|오토인코더]]의 뼈대는 가운데 허리가 극단적으로 잘록하게 들어간 **모래시계(Hourglass)** 모양의 대칭적 신경망 네트워크 아키텍처다.

```text
┌──────────────────────────────────────────────────────────────┐
│           오토인코더 (Autoencoder)의 모래시계 압축-복원 아키텍처 도해       │
├──────────────────────────────────────────────────────────────┤
│  [1. 인코더 (Encoder) - 무자비한 압축기]                          │
│   * 입력(X): 1024 픽셀의 원본 고양이 사진.                       │
│   * 과정: 신경망 층을 지날 때마다 데이터 크기를 512 ─▶ 256 ─▶ 128로 깎아버림. │
│                                                              │
│  [2. 잠재 공간 (Latent Space / Bottleneck Z) - 마법의 엑기스]    │
│   * 1024개의 픽셀이 겨우 숫자 32개(Z 벡터)로 짓눌려 압축된 심해의 병목 구간. │
│   * 놀라운 점: 이 32개의 숫자 안에는 고양이의 '귀 모양, 눈 색깔, 털 질감'이라는 │
│               우주 최고로 엑기스만 남은 고밀도 의미(Feature)가 응축되어 있음.│
│                                                              │
│  [3. 디코더 (Decoder) - 기적의 부풀리기 복원기]                   │
│   * 과정: 32개의 숫자(Z)만 달랑 들고, 다시 128 ─▶ 256 ─▶ 512 ─▶ 1024 픽셀로│
│          상상력을 동원해 거꾸로 부풀려 그림을 새로 그려냄 (출력 X').          │
│                                                              │
│  [4. 훈련 로스(Loss) 계산]                                       │
│   * 내가 처음에 넣은 사진(X)과, 모델이 압축했다가 복원해 낸 가짜 사진(X') 사이의│
│     틀린 그림 찾기(MSE 오차)를 해서, 둘이 100% 똑같아지도록 뇌를 뜯어고침!  │
└──────────────────────────────────────────────────────────────┘
```

**핵심 원리 (잠재 벡터 $Z$의 [[081_dimensionality_reduction_pca_principal_component_analysis|차원 축소]])**:
고전적인 통계학의 '[[163_pca|PCA]]([[338_pca_principal_component_analysis|주성분 분석]])'도 [[001_dikw_pyramid|데이터]]를 [[347_compaction|압축]]하지만, 선형적인 깎아내기밖에 못 해서 복잡한 얼굴 사진을 넣으면 바보가 된다. 반면 [[335_autoencoder|오토인코더]]는 딥러닝의 비선형(Non-linear) [[129_activation_function|활성화 함수]] 릴레이를 타고 깎아 들어가기 때문에, 사진 속의 구불구불한 털과 곡선 패턴마저 억지로 펴서 좁은 잠재 공간($Z$) 안에 완벽하게 욱여넣는 압도적인 [[081_dimensionality_reduction_pca_principal_component_analysis|차원 축소]]([[079_dimensionality_reduction|Dimensionality Reduction]]) 파워를 발휘한다.

| 요소 | 역할 |
|:---|:---|
| 특성 공학 | 문제 구조를 모델이 학습 가능한 형태로 바꾸는 출발점이다. |
| 평가 지표 | 같은 정확도여도 비즈니스 위험은 지표 선택에 따라 달라진다. |
| 모델 선택 | 문제의 선형성, [[001_dikw_pyramid|데이터]] 크기, 해석성 요구를 반영한다. |
| 최적화 | 탐색·튜닝을 통해 [[282_performance_tactics|성능]]과 비용의 균형점을 찾는다. |

- **📢 섹션 요약 비유**: [[335_autoencoder|오토인코더]]의 [[347_compaction|압축]]은 거대한 소 한 마리를 가마솥에 넣고 3박 4일 동안 푹 고아서 딱 종이컵 한 컵 분량의 '초강력 사골 엑기스(잠재 벡터 $Z$)'를 만들어내는 작업이다. 이 엑기스 안에는 소의 뼈와 살은 보이지 않지만, 물([[039_decoder|디코더]])을 붓고 다시 끓이면 원본 쇠고기국 1,000그릇의 완벽한 맛(원본 이미지)이 100% 부활하는 신비로운 맛의 본질이 [[347_compaction|압축]]되어 있다.

---

## Ⅲ. 비교 및 연결

세상에는 [[335_autoencoder|오토인코더]]를 단순히 [[347_compaction|압축]]기로 쓰지 않고, 꼼수를 섞어 기상천외한 마법을 부리는 수많은 변종 [[638_mutation_testing_test_case_verification|돌연변이]]들이 존재한다.

| [[638_mutation_testing_test_case_verification|돌연변이]] [[335_autoencoder|오토인코더]] | 핵심 훈련 꼼수 ([[319_architecture|Architecture]] Hack) | [[348_mlops|MLOps]] 현업에서의 미친 활약상 (Use Case) |
|:---|:---|:---|
| **기본 [[335_autoencoder|오토인코더]] (AE)** | 쌩사진을 [[347_compaction|압축]]([[040_encoder|인코더]])했다가 그냥 그대로 다시 복원([[039_decoder|디코더]])함 | 거의 안 씀. 단순히 차원 깎기 용도로만 쓰고 모델 [[267_weight_bias_activation|가중치]]는 버림. |
| **디노이징 [[335_autoencoder|오토인코더]] (DAE)** | 원본 사진에 검은색 모자이크 먼지(Noise)를 잔뜩 뿌려 넣은 뒤, 모델에게 "먼지 없는 원본으로 깨끗하게 복원해!"라고 가혹하게 채찍질함 | 흐릿하고 모자이크 쳐진 옛날 [[933_cctv|CCTV]] 사진을 넣으면, **AI가 스스로 노이즈를 쓱싹 지우고 초고화질 4K [[933_cctv|CCTV]] 원본으로 깨끗하게 닦아내어 뱉어내는 흑마술(Denoising)** |
| **희소 [[335_autoencoder|오토인코더]] (Sparse AE)** | 병목(Z) 구간의 용량은 엄청 크게 냅두는 대신, "한 번에 뇌 신경 세포의 5%만 써서 [[347_compaction|압축]]해!"라고 족쇄(L1 [[134_regularization_dropout_batch_norm|Regularization]])를 채워 전기를 아끼게 묶어버림 | 쓸데없는 정보는 다 무시하고 오직 특정 시각 패턴(예: 가로줄, 세로줄)에만 극도로 예민하게 반응하는 특징 추출의 절대 신 |
| **[[213_variational_autoencoder|변이형 오토인코더]] ([[315_autoencoder_vae|VAE]])** | 숫자(Z) 한 개로 [[347_compaction|압축]]하는 게 아니라, "[[138_normal_distribution|정규 분포]](평균, [[136_variance|분산]])라는 뭉게구름 [[130_probability|확률]]" 형태로 [[347_compaction|압축]]해서 뱉게 만듦 | 사진을 그냥 복사(복원)하는 게 아니라, [[130_probability|확률]] 주사위를 굴려 **이 세상에 존재하지 않는 전혀 새로운 사람 얼굴을 창조([[087_process_state_transition|생성]]형 [[190_ai_llm_requirements_specification|AI]])**해 내는 위대한 창조주 |

특히 현업 공장([[166_smart_factory|Smart Factory]])의 [[348_mlops|MLOps]] 백엔드에서 **[[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]]([[111_anomaly_detection|Anomaly Detection]])**를 할 때 [[335_autoencoder|오토인코더]]는 황제로 군림한다. 정상적인 모터 회전 소리 [[001_dikw_pyramid|데이터]]만 10만 개 넣고 [[335_autoencoder|오토인코더]]를 훈련시킨다. 나중에 실전(Serving)에서 갑자기 쇠 갈리는 소리(고장 [[001_dikw_pyramid|데이터]])가 들어오면, 평생 정상 [[001_dikw_pyramid|데이터]]만 [[347_compaction|압축]]/복원해 본 모델은 이 고장 난 소리를 제대로 복원하지 못하고 완전히 찌그러진 그림을 뱉어낸다. 이때 "원본과 복원본의 오차(Reconstruction Error)가 펑 터졌네! 이거 100% 고장이다!"라고 설비 고장 알람을 0.01초 만에 쏘아 올리는 기가 막힌 방어망이 성립된다.

- **📢 섹션 요약 비유**: [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]]에 쓰이는 [[335_autoencoder|오토인코더]]는 평생 '모차르트 교향곡(정상 [[001_dikw_pyramid|데이터]])'만 듣고 따라 치는 연습만 죽어라 한 피아노 천재다. 이 천재에게 갑자기 록밴드의 헤비메탈 음악(고장 [[001_dikw_pyramid|데이터]])을 들려주고 똑같이 쳐보라고 하면, 당황해서 건반을 마구 엇나가며 엄청난 불협화음(복원 오차 에러)을 낸다. 우리는 이 불협화음의 크기만 딱 듣고도 "아, 지금 들어온 [[001_dikw_pyramid|데이터]]가 정상적인 모차르트가 아니라 미친 불량품이구나!"라고 1초 만에 눈치를 까고 기계 전원을 차단할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

의료 MRI에서 암세포를 찾는 [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]]망이나, 넷플릭스 [[211_recommendation_system|추천 시스템]]의 유저 취향 [[347_compaction|압축]]기(Latent Factor)로 [[335_autoencoder|오토인코더]]를 배포(CD)할 때 아키텍트는 병목 구간의 용량을 철저히 조율해야 한다.

### 실무 아키텍처 판단 ([[435_checklist_based_testing|체크리스트]])
1. **잠재 공간([[617_io_bottleneck|Bottleneck]] Z)의 해상도(차원 수) 튜닝의 칼춤**: [[040_encoder|인코더]]와 [[039_decoder|디코더]] 사이의 허리(Z)를 몇 개의 숫자로 [[347_compaction|압축]]할 것인가? 1,000픽셀을 10개(Z=[[489_raid_10_hybrid|10]])로 너무 빡세게 조이면, 고양이의 눈과 귀 정보가 다 박살 나서 복원본(디코딩)이 찰흙 덩어리처럼 나온다. 반대로 Z=800처럼 널널하게 열어두면 모델이 뇌를 쓰지 않고(특징 추출 안 함) 그냥 원본을 복사 붙여넣기(Identity [[010_schema_mapping|Mapping]])하는 멍청한 패스스루 통로로 전락한다. 입력 [[001_dikw_pyramid|데이터]] 복잡도에 비례하여 [[347_compaction|압축]]과 정보 손실의 타협점(Trade-off Curve)을 찾아내는 튜닝이 프로젝트의 생사를 가른다.
2. **비대칭 (Asymmetric) [[039_decoder|디코더]] 배포 최적화**: 훈련([[588_mlops_pipeline_automation|Training]]) 단계에서는 [[040_encoder|인코더]]와 [[039_decoder|디코더]] 양쪽의 거대한 파라미터가 다 필요하다. 하지만 실전 런타임(Serving)에서 "유저의 행동 [[568_logs_distributed_logging_elk_fluentd|로그]]를 100차원 벡터(Z)로 [[347_compaction|압축]]해서 [[002_database_definition|데이터베이스]]에 넣는 기능"만 필요하다면, 무겁게 훈련이 끝난 [[039_decoder|디코더]] 신경망 덩어리는 통째로 썰어서 쓰레기통에 버려버리고, 오직 **[[040_encoder|인코더]]([[040_encoder|Encoder]]) 뇌의 절반만 쏙 빼서 가볍게 [[532_microservices_decomposition_patterns|마이크로서비스]]([[063_docker_architecture|Docker]])로 말아 배포**해야 추론 랙([[141_latency|Latency]])과 [[418_gpu|GPU]] 대여비를 절반으로 후려칠 수 있다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- **[[121_supervised_learning|지도 학습]](Supervised)이 넘치는 꿀 [[064_relation_domain|도메인]]에 억지 [[335_autoencoder|오토인코더]] 이식**: 우리 회사에 이미 "불량품", "정상품"이라고 예쁘게 정답표(Labeling)가 달려있는 완벽한 엑셀 [[001_dikw_pyramid|데이터]]가 100만 장이 쌓여있는데, 주니어 [[001_dikw_pyramid|데이터]] 과학자가 "논문에서 폼 나게 봤다"며 정답 레이블을 싹 다 무시하고 [[122_unsupervised_learning|비지도 학습]]인 [[335_autoencoder|오토인코더]]로 억지 [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]] [[123_pipe|파이프]]라인을 구축하는 오버엔지니어링 코미디. 정답지가 충분하다면 무조건 정답을 주고 뇌를 때리는 [[121_supervised_learning|지도 학습]]([[287_resnet_skip_connection|ResNet]], XGBoost) 모델을 짜는 것이 압도적으로 10배 정확하고 싸게 먹힌다. [[335_autoencoder|오토인코더]]는 "정답 [[001_dikw_pyramid|데이터]]가 없거나, 불량품 [[001_dikw_pyramid|데이터]]가 0.01%밖에 없는" 극한의 결핍 환경에서만 꺼내 드는 비상용 생존 나이프다.

- **📢 섹션 요약 비유**: 병목 튜닝은 모래시계의 허리 구멍 크기를 조절하는 것이다. 허리 구멍(Z 공간)이 너무 크면 모래([[001_dikw_pyramid|데이터]])가 1초 만에 쏟아져 내려가서 컴퓨터가 아무런 생각(특징 추출)을 할 틈도 없이 바보 복사기가 된다. 허리 구멍이 바늘구멍처럼 너무 좁으면 모래가 꽉 막혀서 모델이 터져버린다(정보 유실). [[001_dikw_pyramid|데이터]]의 굵기에 딱 맞춰서 모래가 천천히 엑기스만 쏙쏙 빠져나가게 유리병 허리를 정밀하게 굽는 유리가마 장인이 되어야 한다.

---

## Ⅴ. 기대효과 및 결론

[[335_autoencoder|오토인코더]]([[335_autoencoder|Autoencoder]])의 철학적 가치는, 인간의 개입(정답표 달아주기 노가다) 없이 기계가 **스스로 [[001_dikw_pyramid|데이터]]의 [[347_compaction|압축]]된 본질을 득도([[266_self_supervised_learning|Self-Supervised Learning]])**하게 만들었다는 데 있다. 세상 모든 지식의 겉껍데기를 다 태워버리고 남은 단단한 사리, '잠재 공간(Latent Space)'이라는 위대한 다차원 우주의 좌표계를 발견한 것이다.

이 잠재 공간의 획득은 [[231_ai_turing_test|인공지능]]이 무언가를 '[[087_process_state_transition|생성]](Generation)'하는 신의 영역으로 넘어가는 티핑 포인트가 되었다. 단순히 [[016_replication_factor|복제]]만 하던 [[335_autoencoder|오토인코더]]는 [[130_probability|확률]]과 [[136_variance|분산]]을 집어넣어 [[213_variational_autoencoder|변이형 오토인코더]]([[315_autoencoder_vae|VAE]])로 진화했고, 이제는 그 [[347_compaction|압축]]된 잠재 공간(Z) 안에서 노이즈를 닦아내는 흑마술인 **잠재 [[153_diffusion_model_stable_diffusion_denoising|디퓨전 모델]] ([[288_latent_diffusion_model|Latent Diffusion Model]], Stable Diffusion)**로 최종 진화하여, 몇 초 만에 우주에 없는 완벽한 고해상도 초실사 그림을 뚝딱 찍어내는 마법을 부리고 있다.

결국 [[335_autoencoder|오토인코더]]는 딥러닝에게 "복잡한 것을 단순하게 쥐어짤 줄 아는 [[347_compaction|압축]]의 미학"을 가르친 근본 뼈대다. 가장 중요한 특징(Feature)만 걸러내는 이 거대한 모래시계 필터가 존재하지 않았다면, 오늘날 수조 개의 파라미터를 돌리며 세상을 [[347_compaction|압축]]해서 외워버린 챗GPT([[263_llm_large_language_model|LLM]])나 [[960_deepfake|딥페이크]] 동영상(Sora) 같은 초거대 모델들은 차원의 저주를 맞고 영원히 부화하지 못했을 것이다.

- **📢 섹션 요약 비유**: [[335_autoencoder|오토인코더]]는 [[231_ai_turing_test|인공지능]]에게 '모방'을 통해 '창조'를 가르친 위대한 미술 선생님이다. 처음엔 제자([[190_ai_llm_requirements_specification|AI]])에게 피카소 그림을 억지로 [[347_compaction|압축]]해서 똑같이 베껴 그리라고만 훈련시켰다(단순 복원). 하지만 제자가 수만 장을 베껴 그리며 물감의 본질(잠재 벡터)을 완벽히 득도하고 나자, 어느 날부터는 선생님이 가르쳐주지 않은 전혀 새로운 피카소 풍의 그림([[087_process_state_transition|생성]]형 [[190_ai_llm_requirements_specification|AI]])을 스스로 스케치북에 쓱쓱 그려내기 시작하며 스승을 뛰어넘은 진짜 창조주로 각성하게 된 것이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[122_unsupervised_learning|비지도 학습]] ([[122_unsupervised_learning|Unsupervised Learning]])** | [[335_autoencoder|오토인코더]]가 숨 쉬는 토대. "이 사진이 개야, 고양이야?"라고 사람이 정답(Label)을 주지 않아도, 그냥 1억 장의 사진만 던져주면 지가 알아서 눈치껏 훈련하는 가성비 끝판왕 생태계 |
| **[[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]] ([[111_anomaly_detection|Anomaly Detection]])** | [[335_autoencoder|오토인코더]]가 [[348_mlops|MLOps]] 산업 현장에서 돈을 버는 최고의 1군 킬러 앱. 정상 [[001_dikw_pyramid|데이터]]만 죽어라 [[347_compaction|압축]]/복원시킨 다음, 고장 난 부품 사진이 들어오면 복원을 못 하고 에러를 뿜게 만들어 범인을 색출하는 [[123_pipe|파이프]]라인 |
| **디노이징 [[335_autoencoder|오토인코더]] (DAE)** | 원본 사진에 노이즈(모자이크)를 잔뜩 뿌린 뒤 "원래 깨끗한 사진으로 다시 복원해!"라고 가혹한 훈련을 시켜서, 딥러닝 뇌의 강건함(Robustness) 맷집을 수십 배 튀겨버리는 진화형 마개조 수술 |
| **잠재 공간 (Latent Space / Z)** | 100만 픽셀짜리 고양이 사진이 모래시계 병목에 낑겨서 딱 100개의 숫자로 짓눌려 [[347_compaction|압축]]된, 우주의 모든 지식이 진액으로 응축되어 둥둥 떠다니는 [[231_ai_turing_test|인공지능]] 머릿속의 기하학적 초공간 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 전처리] → [오토인코더 (Autoencoder) 구조] → [최적화·운영 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[335_autoencoder|오토인코더]]는 거대한 고양이 사진을 억지로 구겨서 아주 작은 **'비밀 쪽지([[347_compaction|압축]])'**에 꾹꾹 눌러 적은 다음, 나중에 그 쪽지 한 장만 보고도 다시 똑같은 고양이 사진으로 완벽하게 **'그려내는(복원)'** 천재 화가 로봇이에요.
2. 로봇에게 비밀 쪽지 칸을 아주아주 좁게 만들어주면, 로봇은 쓸데없는 뒷배경 같은 건 다 포기하고 "뾰족한 귀, 둥근 눈" 같은 진짜 고양이의 제일 중요한 엑기스 비밀만 쏙쏙 뽑아 적는 눈치를 갖게 돼요.
3. 이 로봇에게 평생 예쁜 사과 사진만 그렸다 복원하게 훈련시키면, 나중에 썩은 사과 사진이 들어왔을 때 로봇이 "어? 내 쪽지 공식엔 이런 더러운 점이 없는데?"라며 그림을 못 그리고 삐용삐용 에러를 울려주는 훌륭한 썩은 사과 경찰관이 된답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 212 / 420

← **이전**: [[211_recommendation_system|211. 추천 시스템 (Recommendation System)]]
**다음**: [[213_variational_autoencoder|213. 변이형 오토인코더 (VAE)]] →

---
