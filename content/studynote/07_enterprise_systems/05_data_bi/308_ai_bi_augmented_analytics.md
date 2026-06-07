---
title: "Augmented Analytics"
date: "2026-04-21"
tags:
  - "studynote-enterprise-systems"
weight: 308
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Augmented Analytics (증강 분석)는 ML/AI가 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 준비·인사이트 발견·결과 해석을 자동화하여 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전문가 없이도 분석이 가능하게 하는 패러다임이다.
> 2. **가치**: NLQ (Natural Language Query)를 통해 비기술 사용자도 자연어 텍스트로 즉시 [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/)를 얻고, Auto-Insight로 [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)·트렌드를 실시간 감지한다.
> 3. **판단 포인트**: [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) BI의 인사이트 자동화는 분석가를 대체하는 것이 아니라, 분석가가 고부가가치 해석과 의사결정에 집중할 수 있게 하는 도구다.

## Ⅰ. 개요 및 필요성

전통 BI (Business Intelligence)에서는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분석가가 수동으로 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)를 작성하고 [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/)를 구성했다.
Gartner는 2017년 Augmented Analytics를 "AI와 ML이 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 준비·인사이트 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·설명을 자동화하는 차세대 BI"로 정의했다.

증강 분석의 핵심 기능:
1. NLQ (Natural Language Query): 자연어로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 질의
2. Auto-Insight Generation: ML이 자동으로 [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)·트렌드 발견
3. ML-Powered Forecasting: 시계열 예측 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)
4. [Anomaly Detection](/studynote/16_bigdata/05_analysis/111_anomaly_detection/): 대시보드에서 이상 지표 자동 하이라이트
5. [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Storytelling: 분석 결과를 자동으로 내러티브 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)

도구: [Tableau](/studynote/16_bigdata/08_visualization/164_tableau/) Einstein Analytics, Microsoft [Power BI](/studynote/16_bigdata/08_visualization/165_power_bi/) Copilot, Qlik Sense [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) Insights, ThoughtSpot (NLQ 특화)

📢 **섹션 요약 비유**: 증강 분석은 네비게이션 앱이다. 목적지만 말하면 최적 경로를 자동 계산해준다. 운전자는 핸들(의사결정)만 잡으면 된다.

## Ⅱ. 아키텍처 및 핵심 원리

### 증강 분석 기능 계층

| 계층 | 기능 | [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기술 |
|:---|:---|:---|
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 준비 자동화 | [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 추론, 결측값 처리 | [AutoML](/studynote/14_data_engineering/04_mlops/176_automl_hyperparameter_optimization_bayesian/), [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 모델 |
| 자연어 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) | 텍스트 -> SQL 변환 | NLP, [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) ([GPT](/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)-4 기반) |
| 자동 인사이트 | [이상치](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)·트렌드·상관관계 | 통계 검정, 클러스터링 |
| [예측 분석](/studynote/16_bigdata/02_hadoop/046_predictive_analytics/) | 시계열 예측 | Prophet, [LSTM](/studynote/10_ai/04_ai_ops_ethics/292_lstm/) |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 스토리텔링 | 수치 -> 자동 내러티브 | NLG (자연어 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)) |

### NLQ 처리 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인

```
"지난 3개월 지역별 매출 상위 5개 상품" (자연어 입력)
  -> 의도 파악 (Intent Classification)
  -> 엔티티 추출 (기간: 3개월, 차원: 지역, 측도: 매출, Top5)
  -> SQL 자동 생성
  -> DW 쿼리 실행
  -> 결과 시각화 자동 선택 (Bar Chart)
```

### [ASCII](/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램: [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) BI 처리 흐름

```
  원시 데이터 (DW / Data Mart)
        |
        v
  +-----------------------------------------------+
  |              AI 분석 레이어                    |
  |  +----------------+  +----------------------+ |
  |  |   NLQ 엔진     |  |  Auto-Insight Engine | |
  |  |  (LLM + NLP)   |  |  (이상치/트렌드/예측) | |
  |  +-------+--------+  +----------+-----------+ |
  |          +--------------+-------+             |
  |                         v                     |
  |  +------------------------------------------+ |
  |  |  자동 시각화 선택 + 데이터 스토리텔링 NLG  | |
  |  +------------------------------------------+ |
  +-------------------------+---------------------+
                            v
        비즈니스 사용자 (코딩 불필요)
        +------------------------------+
        |  "Q3 판매 급감 원인은?"       |
        |  -> 자동 분석 + 내러티브 생성 |
        +------------------------------+
```

### 주요 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) BI 도구 비교

| 도구 | NLQ | Auto-Insight | 예측 | GenAI 통합 |
|:---|:---|:---|:---|:---|
| [Tableau](/studynote/16_bigdata/08_visualization/164_tableau/) Einstein | ◎ | ◎ | ◎ | ◎ (Salesforce Einstein) |
| [Power BI](/studynote/16_bigdata/08_visualization/165_power_bi/) Copilot | ◎ | ○ | ◎ | ◎ (Azure OpenAI) |
| Qlik Sense | ○ | ◎ | ○ | ○ |
| ThoughtSpot | ◎ | ○ | ○ | ◎ (SpotIQ) |

📢 **섹션 요약 비유**: NLQ는 구글 검색창이다. 복잡한 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 문법을 몰라도 말로 물으면 답을 찾아준다.

## Ⅲ. 비교 및 연결

### 전통 BI vs Augmented Analytics

| 항목 | 전통 BI | Augmented Analytics |
|:---|:---|:---|
| 사용자 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분석가 | 모든 비즈니스 사용자 |
| 질의 방법 | SQL/MDX 수작업 | 자연어 텍스트 입력 |
| 인사이트 발견 | 수동 탐색 | [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 자동 제안 |
| 예측 | 별도 ML 프로젝트 | 원클릭 예측 |

📢 **섹션 요약 비유**: 전통 BI는 도서관에서 직접 책을 찾는 것, 증강 분석은 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 사서가 "이런 책도 관심 있으실 것 같아요"라고 먼저 추천해주는 것이다.

## Ⅳ. 실무 적용 및 기술사 판단

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

- [ ] 비기술 사용자 비율 파악: 70% 이상이면 NLQ 중심 도구 선택
- [ ] [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 선행 확보: NLQ는 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 불일치 시 오답 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)
- [ ] [LLM](/studynote/06_ict_convergence/04_ai_llm/263_llm_large_language_model/) 연동 보안 검토: [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/)에 PII 포함 가능성 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)
- [ ] Auto-Insight 결과 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 프로세스: 오탐율 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링
- [ ] [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근 제어: 역할 기반 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

| [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/) | 문제 | 해결 방법 |
|:---|:---|:---|
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 무시하고 NLQ 도입 | 오답 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) -> 사용자 불신 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 [KPI](/studynote/12_it_management/01_governance_strategy/018_kpi/) 먼저 확보 |
| [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 인사이트 무조건 신뢰 | 비즈니스 맥락 없는 인사이트 | [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 전문가 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 필수 |

📢 **섹션 요약 비유**: [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) BI의 자동 인사이트는 자동차 경고등이다. [신호](/studynote/02_operating_system/02_process_thread/130_signal/)를 보내도 운전자가 원인을 이해하고 판단해야 한다. 경고등만 믿고 핸들을 놓으면 안 된다.

## Ⅴ. 기대효과 및 결론

| 항목 | 도입 전 | 도입 후 |
|:---|:---|:---|
| 보고서 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 시간 | 2~5일 | 수분 (자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)) |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근 가능 인력 | 전체 5~[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)% | 전체 60~80% |
| 인사이트 발견 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 분석 요청 후 1주일 | 실시간 자동 제안 |

📢 **섹션 요약 비유**: [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) BI는 탁월한 부조종사다. 조종사(분석가)는 중요한 결정에 집중하고, 부조종사는 반복 계기 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)을 자동으로 처리한다.

### 📌 관련 개념 맵

| 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| NLQ | 핵심 기능 | 자연어로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 질의 |
| Auto-Insight | 핵심 기능 | [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 자동 인사이트 발견 |
| [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Storytelling | 출력 형태 | 분석 결과 자동 내러티브화 |
| Augmented Analytics | 패러다임 | [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 강화 셀프서비스 BI |

### 📈 관련 키워드 및 발전 흐름도

```
전통 BI - 수작업 SQL 쿼리 + 정적 대시보드
    |
    v
셀프서비스 BI (Power BI, Tableau) - 드래그앤드롭
    |
    v
Augmented Analytics - AI/ML 자동 인사이트 발굴
    |
    v
NLQ (자연어 쿼리) + Auto-Narrative 리포트
    |
    v
GenAI BI - LLM 기반 대화형 데이터 분석
```

> **키워드**: Augmented Analytics, NLQ, [AutoML](/studynote/14_data_engineering/04_mlops/176_automl_hyperparameter_optimization_bayesian/) BI, Self-[Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) BI, [Power BI](/studynote/16_bigdata/08_visualization/165_power_bi/), [Tableau](/studynote/16_bigdata/08_visualization/164_tableau/), GenAI BI, Smart Insight

### 👶 어린이를 위한 3줄 비유 설명

1. 증강 분석은 "지난달 어느 과자가 제일 많이 팔렸어?"라고 말만 해도 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)를 그려주는 컴퓨터예요.
2. Auto-Insight는 컴퓨터가 스스로 "이 상품 판매가 갑자기 줄었는데 왜 그럴까요?"라고 먼저 알려주는 기능이에요.
3. [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Storytelling은 숫자들을 읽기 쉬운 이야기로 바꿔주는 거예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 308 / 482

<- **이전**: [307. 다차원 큐브 MOLAP ROLAP HOLAP 성능 튜닝 (Multidimensional OLAP)](/studynote/07_enterprise_systems/05_data_bi/307_molap_rolap_holap/)
**다음**: [309. 시계열 데이터베이스 InfluxDB 다운샘플링 롤업 (Time-Series DB Downsampling)](/studynote/07_enterprise_systems/05_data_bi/309_influxdb_downsampling/) ->

---
