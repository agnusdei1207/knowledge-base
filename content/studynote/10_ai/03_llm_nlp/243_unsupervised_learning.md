+++
title = "243. 비지도 학습 (군집화, 연관성, 차원 축소)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ai"]

[extra]
tags = ["studynote-ai"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)([Unsupervised Learning](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/))은 인간이 일일이 "이 사진은 고양이(정답)"라고 가르쳐주는 피곤한 라벨링(Labeling) 노가다를 완전히 던져버리고, **정답지가 전혀 없는 쓰레기장 같은 날것의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 무더기를 기계에 쏟아부어 "네가 알아서 끼리끼리 묶어보고([군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/)), 숨겨진 법칙을 찾아봐!"라고 방목하는 야생의 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 통계 탐색법**이다.
> 2. **가치**: 고객 천만 명의 구매 영수증([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 보고 인간은 아무 규칙도 찾지 못한다. 하지만 [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)(연관 분석)을 돌리면 "기저귀를 산 아빠들은 맥주도 같이 산다"는 상상도 못 한 숨겨진 황금 룰을 1초 만에 끄집어낸다. 넷플릭스 [추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/), 백화점 VIP 고객 타겟팅 등 '우리가 뭘 찾아야 할지조차 모를 때' 기계가 먼저 통찰력(Insight)의 보물 지도를 그려주는 궁극의 B2C 무기다.
> 3. **판단 포인트**: 정답(Label)이 없으므로 모델이 일을 잘했는지 채점([Metric](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/))하기가 미치도록 애매하다. 끼리끼리 묶는 **[군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/)([Clustering](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/))**, 장바구니 패턴을 캐내는 **연관 분석(Association)**, 너무 많은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 칼럼을 핵심만 쥐어짜 내는 **[차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/)([Dimensionality Reduction](/knowledge-base/studynote/12_it_management/02_itsm_itil/079_dimensionality_reduction/))**의 3대 아키텍처가 비지도 대륙을 떠받치는 기둥이다.

---

## Ⅰ. 개요 및 필요성

[초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/)은 [지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/)(Supervised)의 달콤함에 취해 있었다. 정답지가 달린 엑스레이 10만 장만 들이부으면 암을 100% 진단해 내는 천재가 탄생했기 때문이다.
그러나 현실 비즈니스는 달랐다. 아마존(Amazon)이 고객 1억 명의 클릭 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 모았는데, 이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에는 "이 고객은 A등급, 저 고객은 B등급"이라는 정답표(Label)가 달려있을 리 만무했다. 알바생 1만 명을 고용해 1억 명의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 수동으로 정답표를 다는 것은 돈과 시간이 우주 단위로 깨지는 미친 짓(라벨링 병목)이었다.

"야! 정답지(Label) 만드는 거 포기해! 그냥 1억 명 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 날것 그대로 컴퓨터한테 통째로 부어버리자. **컴퓨터가 알아서 자기들끼리 비슷한 패턴을 가진 놈들끼리 그룹으로 쪼개거나([군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/)), 숨겨진 규칙을 찾아내게 방치해 볼까?**"

이 발상의 전환에서 태어난 것이 바로 **[비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/) ([Unsupervised Learning](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/))**이다. 지도(Supervision, 인간 선생님의 가이드)를 완전히 끊어버리고, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 속에 흐르는 수학적 거리(Distance)와 밀도(Density)만으로 1억 명의 고객을 "돈 많이 쓰는 30대 그룹", "가전제품만 보는 50대 그룹"으로 0.1초 만에 묶어버린 것이다. 이 야생의 훈련법 덕분에 기업들은 정답지가 없는 빅데이터의 바다에서도 완벽한 통찰력을 건져 올리며 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 마케팅의 신세계를 열어젖혔다.

```text
┌──────────────────────────────────────────────┐
│ Background Problem → Need → Adoption Value   │
├──────────────────────────────────────────────┤
│ Existing limitation │ Operational pressure   │
│ New requirement     │ Design decision point  │
└──────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/)은 '정답이 있는 퍼즐 맞추기'다. 완성된 그림(정답)을 힐끔힐끔 보면서 퍼즐([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 맞추니 100점 맞기가 쉽다. [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)은 '모래사장에서 외계인 유물 조립하기'다. 완성된 그림(정답지) 따윈 아예 없다. 그냥 조각들 수백만 개를 모아놓고, "이 조각은 저 조각이랑 홈이 대충 비슷하게 생겼네?" 하고 기계 스스로 끼리끼리 뭉쳐보는 거다. 다 뭉치고 났더니 인간도 상상 못한 멋진 성벽(숨겨진 패턴)이 완성되는 신비로운 야생 조립법이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)의 아키텍처는 정답(Target $Y$) 없이 오직 입력 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)($X$)만으로 지지고 볶아 새로운 3가지 출력물(Insight)을 뽑아내는 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인을 가진다.

```text
┌──────────────────────────────────────────────────────────────┐
│           비지도 학습 (Unsupervised Learning) 3대 알고리즘 뼈대 도해      │
├──────────────────────────────────────────────────────────────┤
│  [입력]: 정답지(Label)가 아예 없는 100만 명의 백화점 영수증 데이터($X$만 존재)│
│                                                              │
│  [1. 군집화 (Clustering) - "유유상종 끼리끼리 묶어라!"]                │
│   * 방식: K-Means 알고리즘 발동! 고객 데이터를 수학적 3차원 공간에 점으로 쫙 뿌림.│
│   * 계산: 점들 사이의 거리(유클리드 거리)를 재서 제일 가까운 놈들끼리 올가미로 묶음.│
│   ─▶ 출력 결과: "사장님! 고객을 [A: 명품 사는 VIP], [B: 지하 푸드코트만 가는│
│                 구두쇠], [C: 화장품 사는 20대] 3개의 그룹으로 찢었습니다!" │
│                                                              │
│  [2. 연관 규칙 탐색 (Association Rules) - "장바구니 훔쳐보기"]         │
│   * 방식: Apriori 알고리즘. 영수증 100만 장에 어떤 물건들이 같이 찍혔나 통계 냄.│
│   ─▶ 출력 결과: "신박한 팩트 발견! [기저귀]를 산 남자는 80% 확률로 [맥주]도   │
│                 같이 삽니다! 기저귀 옆에 맥주 매대를 당장 배치하시죠!"        │
│                                                              │
│  [3. 차원 축소 (Dimensionality Reduction) - "핵심만 남기고 찌그러뜨려!"]│
│   * 방식: PCA 알고리즘. 데이터 칼럼(나이, 키, 몸무게, 시력...)이 1,000개나 돼서│
│          컴퓨터가 터지려 함.                                      │
│   ─▶ 출력 결과: 1,000개의 쓸모없는 변수들을 수학적으로 쥐어짜서, 정보 손실을 최소로│
│                 유지한 채 가장 엑기스인 딱 '10개의 슈퍼 칼럼'으로 압축 완료!  │
└──────────────────────────────────────────────────────────────┘
```

**핵심 원리 (K-Means 거리 기반 분할)**:
[군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/)의 대명사 **K-Means(K-평균)** [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 극강의 단순함을 자랑한다. 1) 아무 데나 K개의 캡틴(중심점, Centroid)을 뚝 찍는다. 2) 모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 자기랑 제일 가까운 캡틴한테 달라붙어 팀을 만든다. 3) 팀이 다 짜지면, 팀원들의 정가운데(평균 위치)로 캡틴이 이동한다. 4) 캡틴이 움직였으니 다시 2번으로 돌아가 자기랑 가까운 캡틴한테 다시 줄을 선다. 이 짓을 캡틴이 더 이상 안 움직일 때까지 수백 번 빙글빙글 돌면, 소름 돋게도 100만 개의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 예쁘게 K개의 그룹(군집)으로 딱 갈라지며 상황이 종료된다.

| 요소 | 역할 |
|:---|:---|
| 특성 공학 | 문제 구조를 모델이 학습 가능한 형태로 바꾸는 출발점이다. |
| 평가 지표 | 같은 정확도여도 비즈니스 위험은 지표 선택에 따라 달라진다. |
| 모델 선택 | 문제의 선형성, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 크기, 해석성 요구를 반영한다. |
| 최적화 | 탐색·튜닝을 통해 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 비용의 균형점을 찾는다. |

- **📢 섹션 요약 비유**: K-Means [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 '운동장 모래알 편 가르기'다. 선생님이 운동장에 3명의 반장(캡틴)을 아무 데나 세워놓고 "다들 젤 가까운 반장 뒤로 줄 서!"라고 외친다. 애들이 줄을 서면, 반장들은 애들 무리의 딱 정중앙(평균)으로 자리를 옮긴다. 앗, 반장이 움직였으니 애들은 다시 자기랑 젤 가까워진 새로운 반장 뒤로 우왕좌왕 다시 줄을 선다(반복). 이 난장판을 계속하다 보면 어느 순간 반장도 안 움직이고 애들도 자리가 고정되는 완벽한 '3개의 파벌(군집)'이 운동장에 기가 막히게 완성된다.

---

## Ⅲ. 비교 및 연결

[비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)의 왕좌를 놓고 [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/)([Clustering](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/)) 세계에서 피 터지게 싸우는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)들의 아키텍처 장단점을 비교해 보자.

| [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 작동 방식 (철학) | 킬러 장점 (Pros) | 치명적 붕괴 단점 (Cons) |
|:---|:---|:---|:---|
| **K-Means (K-평균)** | 점들 사이의 **수학적 거리(직선)**를 재서 가까운 놈들끼리 둥글게 원(구형)을 그리며 묶음 | 로직이 우주에서 제일 단순해서 **계산 속도가 빛처럼 빠름.** 빅데이터 1차 쪼개기 국룰. | **개발자가 K(몇 개의 그룹으로 쪼갤지)를 처음에 하드코딩으로 무조건 정해줘야 함.** 초승달 모양 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 절대 못 묶음. |
| **[DBSCAN](/knowledge-base/studynote/06_ict_convergence/05_data_science/351_dbscan_density_based_clustering/) (밀도 기반)** | 캡틴이고 나발이고 없음. 그냥 **점들이 빽빽하게 뭉쳐있는 곳(밀도)을 쭉 따라가며** 아메바처럼 영역을 묶음 | **K 개수를 안 정해줘도 지가 알아서 덩어리 개수를 찾아냄.** 초승달, 도넛 모양 등 아무리 찌그러진 그룹도 완벽히 묶고, 뚝 떨어진 쓰레기(Noise/[이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/))는 버려버림. | K-Means보다 계산량이 무식하게 커서 **[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 100만 개 넘어가면 서버 메모리(RAM) 터짐.** |
| **[계층적 군집화](/knowledge-base/studynote/10_ai/05_data_science_ml/358_hierarchical_clustering/) (Hierarchical)** | 제일 가까운 두 놈을 묶고, 그다음 가까운 놈 묶고... 위로 올라가며 **거대한 족보(덴드로그램 트리)를 그림** | K를 안 정해도 됨. 족보 그림을 눈으로 보고 "음, 이쯤에서 가위로 자르면 4그룹이네" 하고 **인간이 사후 결정(해석력 최고) 가능.** | 계산 복잡도가 $O(N^3)$ 수준이라 **[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 1만 개만 넘어도 평생 계산만 하다가 컴퓨터 늙어 죽음.** |

실무 B2B 현장에서는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 1억 개라면 묻지도 따지지도 않고 **K-Means**를 돌린다. K값을 몇으로 할지 모를 때는 K를 1부터 10까지 다 돌려보고, 그룹 간 거리가 가장 예쁘게 찢어지는 구간을 찾는 **'엘보우 기법(Elbow Method, 꺾이는 팔꿈치 점 찾기)'**이나 실루엣 계수([Silhouette Score](/knowledge-base/studynote/06_ict_convergence/05_data_science/350_kmeans_elbow_silhouette/))로 최적의 덩어리 개수를 꼼수로 역추산해 낸다.

- **📢 섹션 요약 비유**: K-Means는 '피자 커터기'다. 피자를 무조건 둥글고 예쁜 4조각(K=4)으로 딱딱 예쁘게 자른다. 빠르고 깔끔하지만, 피자 토핑이 별 모양으로 뿌려져 있어도 무시하고 그냥 원형으로 쪼개버리는 무식함이 있다. DBSCAN은 '물감 번지기'다. 도화지에 물감을 한 방울 톡 떨어뜨리면, 물감이 빽빽하게 이어진 길(밀도)을 따라 꼬불꼬불 퍼져나간다. K개수를 안 정해줘도 물감이 멈춘 덩어리 모양(초승달, 별 모양) 그대로 그룹이 묶이는 엄청난 유연성을 가졌지만, 시간이 좀 걸린다.

---

## Ⅳ. 실무 적용 및 기술사 판단

대형 마트의 고객 타겟팅 문자를 보내기 위해 [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/) [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인(K-Means + [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/))을 태울 때, 아키텍트가 전처리 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)를 켜지 않으면 마케팅 부서가 폭파된다.

### 실무 아키텍처 판단 ([체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/))
1. **차원의 저주 돌파를 위한 [PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) ([주성분 분석](/knowledge-base/studynote/06_ict_convergence/05_data_science/338_pca_principal_component_analysis/)) 융합 필수**: 백화점 VIP의 특징 변수(차원)가 1,000개나 된다고 치자(나이, 방문 횟수, 구매액 등). 이 1,000차원짜리 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 그대로 K-Means 거리를 재면 "모든 고객의 거리가 다 똑같이 멀게 나오는" 수학적 붕괴(차원의 저주)가 터진다. 클러스터링을 태우기 전에 반드시 전처리 미들웨어로 **[PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/)([차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/))**를 띄워, 쓸데없는 990개의 겹치는 변수를 찌그러뜨리고 핵심 주성분 변수 딱 10차원으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)해 가볍게 만든 뒤 K-Means에 쑤셔 넣는 **차원축소 $\rightarrow$ [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/) [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인**이 100% 필수 방어막이다.
2. **단위 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) (Scaling / Standardization) 하드코딩**: K-Means는 '거리'를 재서 그룹을 묶는 바보다. 어떤 고객의 나이는 '30(세)'이고, 연봉은 '50,000,000(원)'이다. 이걸 그냥 거리 공식에 넣으면, 컴퓨터는 "와! 연봉 숫자가 5천만이라서 나이 30보다 100만 배 더 중요하구나!"라고 착각하고 오직 연봉으로만 그룹을 찢어버린다. 모델에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 밀어 넣기 전에 반드시 모든 칼럼의 숫자 크기를 0에서 1 사이([Min-Max](/knowledge-base/studynote/14_data_engineering/02_math_mining/078_data_scaling_normalization_min_max_standardization_z_score/))나, 평균 0 표준편차 1(Standard Scaler)로 꽉꽉 찌그러뜨려 놓는 **[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [스케일링](/knowledge-base/studynote/10_ai/03_llm_nlp/249_scaling_normalization_standardization/)(Scaling)**을 하지 않으면 그 군집 모델은 쓰레기다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **[비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/) 결과의 무지성 맹신 (해석력의 부재 버그)**: [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)(K-Means) 돌렸더니 고객이 3개 그룹으로 찢어졌다. 개발자가 사장님한테 "사장님! 컴퓨터가 고객을 3개로 나눴습니다!"라고 자랑한다. 사장님이 "그래서 그 3개 그룹의 특징이 뭔데?"라고 물으면 개발자는 대답을 못 하고 땀만 흘린다. [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)은 정답(Label) 없이 자기들끼리 뭉쳐놓기만 할 뿐, **"이 그룹이 어떤 놈들인지(예: VIP, 진상, 체리피커)" 이름표(해석)를 달아주지 않는다**. [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/)가 끝나면 반드시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분석가([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 전문가)가 3개 그룹의 평균값과 통계를 눈으로 뜯어보고 사람이 직접 "아! 1번 그룹은 명품 VIP구나!"라고 네이밍(해석)하는 **Human-in-the-Loop 꼬리표 공정**이 빠지면 비즈니스적으로 아무 쓸모 없는 숫자 놀음으로 전락한다.

- **📢 섹션 요약 비유**: [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)(Scaling) 없이 K-Means 돌리는 건, 코끼리 무게(kg)와 개미 털 길이(mm)를 똑같은 자로 재는 멍청한 짓이다. 코끼리는 5,000kg이고 개미 털은 5mm다. 자로 재면 코끼리가 숫자가 무식하게 크니까, AI는 코끼리가 세상에서 제일 중요한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)라고 맹신해 버린다. [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)는 코끼리와 개미를 '요술 축소 빔'으로 똑같이 10cm 사이즈 미니어처로 줄여놓고, 그들의 진짜 무늬(패턴)만 공정하게 비교하게 만드는 [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) 세계의 절대 규칙(저울 세팅)이다.

---

## Ⅴ. 기대효과 및 결론

[비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)([Unsupervised Learning](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/))은 [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/)이 인간이 떠먹여 주는 '정답지(Label)'의 달콤한 모유 수유를 끊고, 거칠고 험난한 날것의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 우주에서 **스스로 질서와 우주적 법칙을 창조해 낸 독립선언문**이다.

[지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/)이 과거의 정답을 외워 미래를 맞추는 모범생이라면, [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)은 아무도 밟지 않은 눈밭에서 새로운 길을 개척하는 [탐험](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/315_exploration_exploitation/)가다. 이 야생의 [탐험](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/315_exploration_exploitation/)가 덕분에 인류는 기저귀와 맥주의 기괴한 상관관계를 밝혀냈고(Apriori), 은행 카드 결제 내역 1억 건 중에서 유독 혼자 저 멀리 동떨어져 있는 점 1개를 찾아내어 "이건 100% 해커가 훔쳐서 결제한 사기 거래다!([이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/), [Anomaly Detection](/knowledge-base/studynote/16_bigdata/05_analysis/111_anomaly_detection/))"라고 0.1초 만에 알람을 울리는 철통 보안 금융망을 완성해 냈다.

최근 거대 언어 모델([LLM](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/)) 챗GPT의 미친듯한 똑똑함의 기저에도 이 [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)의 변종인 '[자기 지도 학습](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/266_self_supervised_learning/)(Self-Supervised)'이 똬리를 틀고 있다. 수천억 원을 들여 인터넷 문서를 라벨링하지 않고, 그냥 위키피디아 텍스트 수십억 줄을 통째로 쏟아부어 "문장의 다음 단어를 네가 스스로 묶고 유추해 봐!"라고 방임했기에 AGI([강인공지능](/knowledge-base/studynote/10_ai/01_ai_basics/003_strong_ai_agi/))를 향한 지능 폭발이 일어날 수 있었던 것이다. 결국 인간이 상상할 수 있는 지식의 한계를 부수고, 보이지 않는 무한의 다차원 세계에서 진정한 통찰력의 밧줄을 건져 올리는 구원자는 영원히 [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)의 몫이다.

- **📢 섹션 요약 비유**: [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)은 인류에게 주어진 '외계인의 암호 해독기'다. 하늘에서 뚝 떨어진 100만 권의 외계어 책([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))이 있다. 인간은 뜻(정답 라벨)을 모르니 쳐다만 보고 있다. [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)(해독기)에 이 책을 넣으면, 번역은 못 해줘도 "음, 이 동그라미 글자랑 세모 글자는 항상 같이 붙어 다니네?(연관성) 이 별 모양 글자는 이쪽 책에만 잔뜩 모여있네?([군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/))"라고 규칙들을 기가 막히게 분리해서 던져준다. 그러면 인간 학자가 그걸 보고 "아! 동그라미는 '안녕'이라는 뜻이구나!" 하고 깨달음(해석)을 얻어 비즈니스 우주를 정복하게 되는 위대한 협업이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/) ([Supervised Learning](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/))** | [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)의 정반대 거울. 얘는 인간이 사진 10만 장마다 "이건 고양이!"라고 정답표(Label)를 다 달아줘서 훈련시키는 과외 수업이라 돈과 인건비가 터지게 많이 드는 차이점이 있다 |
| **[K-Means Clustering](/knowledge-base/studynote/10_ai/01_ai_basics/057_k_means_clustering_unsupervised_learning/) (K-평균 [군집화](/knowledge-base/studynote/16_bigdata/05_analysis/105_clustering_analysis/))** | 비지도 대륙을 지배하는 1등 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/). 아무런 정답이 없어도, 점들 사이의 수학적 거리만 쓱쓱 재서 K개의 파벌(덩어리)로 1초 만에 예쁘게 찢어놓는 빅데이터 쪼개기의 황제 |
| **[PCA](/knowledge-base/studynote/08_algorithm_stats/10_linear_algebra/163_pca/) ([주성분 분석](/knowledge-base/studynote/06_ict_convergence/05_data_science/338_pca_principal_component_analysis/), [차원 축소](/knowledge-base/studynote/14_data_engineering/02_math_mining/081_dimensionality_reduction_pca_principal_component_analysis/))** | [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)의 든든한 청소부. 엑셀 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 칼럼(차원)이 1,000개면 너무 무거워서 컴퓨터가 뻗으니까, 가장 중요한 정보 10개로 확 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)해서 찌그러뜨려 주는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 다이어트 비법 |
| **Apriori (선험적 연관 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/))** | 대형 마트와 쇼핑몰의 지갑을 털어가는 마법사. 100만 명의 장바구니 영수증을 [비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)으로 뒤져서 "A를 산 놈은 B도 사더라!"라는 교집합 규칙을 뽑아내는 [추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/)의 조상님 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 전처리] → [비지도 학습 (군집화, 연관성, 차원 축소)] → [최적화·운영 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명

1. **[지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/121_supervised_learning/)**은 엄마가 "이 블록은 네모, 저건 세모야" 하고 **정답을 다 알려주면서** 모양 맞추기를 가르치는 거예요.
2. 반면에 **[비지도 학습](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/)([Unsupervised Learning](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/122_unsupervised_learning/))**은 엄마가 정답을 하나도 안 알려주고 그냥 **수만 개의 섞인 레고 블록을 방에 확 쏟아부어 버린 채 나가는 거**예요!
3. 그럼 똑똑한 로봇이 혼자 방에 앉아서 **"어? 이 블록들은 색깔이 비슷하네? 얘네는 크기가 비슷하네?"** 라면서 스스로 끼리끼리 예쁘게 묶어놓고 숨겨진 규칙을 찾아내는 멋진 자습 방법이랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 243 / 420

← **이전**: [242. 지도 학습 (Supervised Learning) : 분류와 회귀](/knowledge-base/studynote/10_ai/03_llm_nlp/242_supervised_learning/)
**다음**: [244. 강화 학습 (Reinforcement Learning)](/knowledge-base/studynote/10_ai/03_llm_nlp/244_reinforcement_learning_mdp/) →

---
