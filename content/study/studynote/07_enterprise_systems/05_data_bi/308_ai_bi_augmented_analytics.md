+++
weight = 308
title = "308. AI BI 증강 분석 자동화 (Augmented Analytics)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Augmented Analytics (증강 분석)는 ML/AI가 [[001_dikw_pyramid|데이터]] 준비·인사이트 발견·결과 해석을 자동화하여 [[001_dikw_pyramid|데이터]] 전문가 없이도 분석이 가능하게 하는 패러다임이다.
> 2. **가치**: NLQ (Natural Language Query)를 통해 비기술 사용자도 자연어 텍스트로 즉시 [[003_bigdata_7v|시각화]]를 얻고, Auto-Insight로 [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]]·트렌드를 실시간 감지한다.
> 3. **판단 포인트**: [[190_ai_llm_requirements_specification|AI]] BI의 인사이트 자동화는 분석가를 대체하는 것이 아니라, 분석가가 고부가가치 해석과 의사결정에 집중할 수 있게 하는 도구다.

## Ⅰ. 개요 및 필요성

전통 BI (Business Intelligence)에서는 [[001_dikw_pyramid|데이터]] 분석가가 수동으로 [[298_qkv_attention|쿼리]]를 작성하고 [[003_bigdata_7v|시각화]]를 구성했다.
Gartner는 2017년 Augmented Analytics를 "AI와 ML이 [[001_dikw_pyramid|데이터]] 준비·인사이트 [[087_process_state_transition|생성]]·설명을 자동화하는 차세대 BI"로 정의했다.

증강 분석의 핵심 기능:
1. NLQ (Natural Language Query): 자연어로 [[001_dikw_pyramid|데이터]] 질의
2. Auto-Insight Generation: ML이 자동으로 [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]]·트렌드 발견
3. ML-Powered Forecasting: 시계열 예측 자동 [[087_process_state_transition|생성]]
4. [[111_anomaly_detection|Anomaly Detection]]: 대시보드에서 이상 지표 자동 하이라이트
5. [[001_dikw_pyramid|Data]] Storytelling: 분석 결과를 자동으로 내러티브 [[087_process_state_transition|생성]]

도구: [[164_tableau|Tableau]] Einstein Analytics, Microsoft [[165_power_bi|Power BI]] Copilot, Qlik Sense [[190_ai_llm_requirements_specification|AI]] Insights, ThoughtSpot (NLQ 특화)

📢 **섹션 요약 비유**: 증강 분석은 네비게이션 앱이다. 목적지만 말하면 최적 경로를 자동 계산해준다. 운전자는 핸들(의사결정)만 잡으면 된다.

## Ⅱ. 아키텍처 및 핵심 원리

### 증강 분석 기능 계층

| 계층 | 기능 | [[190_ai_llm_requirements_specification|AI]] 기술 |
|:---|:---|:---|
| [[001_dikw_pyramid|데이터]] 준비 자동화 | [[005_schema|스키마]] 추론, 결측값 처리 | [[176_automl_hyperparameter_optimization_bayesian|AutoML]], [[104_classification_analysis|분류]] 모델 |
| 자연어 [[298_qkv_attention|쿼리]] | 텍스트 → SQL 변환 | NLP, [[263_llm_large_language_model|LLM]] ([[302_gpt_autoregressive|GPT]]-4 기반) |
| 자동 인사이트 | [[076_outlier_detection_iqr_dbscan_isolation_forest|이상치]]·트렌드·상관관계 | 통계 검정, 클러스터링 |
| [[046_predictive_analytics|예측 분석]] | 시계열 예측 | Prophet, [[292_lstm|LSTM]] |
| [[001_dikw_pyramid|데이터]] 스토리텔링 | 수치 → 자동 내러티브 | NLG (자연어 [[087_process_state_transition|생성]]) |

### NLQ 처리 [[123_pipe|파이프]]라인

```
"지난 3개월 지역별 매출 상위 5개 상품" (자연어 입력)
  → 의도 파악 (Intent Classification)
  → 엔티티 추출 (기간: 3개월, 차원: 지역, 측도: 매출, Top5)
  → SQL 자동 생성
  → DW 쿼리 실행
  → 결과 시각화 자동 선택 (Bar Chart)
```

### [[103_ascii|ASCII]] 다이어그램: [[190_ai_llm_requirements_specification|AI]] BI 처리 흐름

```
  원시 데이터 (DW / Data Mart)
        │
        ▼
  ┌───────────────────────────────────────────────┐
  │              AI 분석 레이어                    │
  │  ┌────────────────┐  ┌──────────────────────┐ │
  │  │   NLQ 엔진     │  │  Auto-Insight Engine │ │
  │  │  (LLM + NLP)   │  │  (이상치/트렌드/예측) │ │
  │  └───────┬────────┘  └──────────┬───────────┘ │
  │          └──────────────┬───────┘             │
  │                         ▼                     │
  │  ┌──────────────────────────────────────────┐ │
  │  │  자동 시각화 선택 + 데이터 스토리텔링 NLG  │ │
  │  └──────────────────────────────────────────┘ │
  └─────────────────────────┬─────────────────────┘
                            ▼
        비즈니스 사용자 (코딩 불필요)
        ┌──────────────────────────────┐
        │  "Q3 판매 급감 원인은?"       │
        │  → 자동 분석 + 내러티브 생성 │
        └──────────────────────────────┘
```

### 주요 [[190_ai_llm_requirements_specification|AI]] BI 도구 비교

| 도구 | NLQ | Auto-Insight | 예측 | GenAI 통합 |
|:---|:---|:---|:---|:---|
| [[164_tableau|Tableau]] Einstein | ◎ | ◎ | ◎ | ◎ (Salesforce Einstein) |
| [[165_power_bi|Power BI]] Copilot | ◎ | ○ | ◎ | ◎ (Azure OpenAI) |
| Qlik Sense | ○ | ◎ | ○ | ○ |
| ThoughtSpot | ◎ | ○ | ○ | ◎ (SpotIQ) |

📢 **섹션 요약 비유**: NLQ는 구글 검색창이다. 복잡한 [[298_qkv_attention|쿼리]] 문법을 몰라도 말로 물으면 답을 찾아준다.

## Ⅲ. 비교 및 연결

### 전통 BI vs Augmented Analytics

| 항목 | 전통 BI | Augmented Analytics |
|:---|:---|:---|
| 사용자 | [[001_dikw_pyramid|데이터]] 분석가 | 모든 비즈니스 사용자 |
| 질의 방법 | SQL/MDX 수작업 | 자연어 텍스트 입력 |
| 인사이트 발견 | 수동 탐색 | [[190_ai_llm_requirements_specification|AI]] 자동 제안 |
| 예측 | 별도 ML 프로젝트 | 원클릭 예측 |

📢 **섹션 요약 비유**: 전통 BI는 도서관에서 직접 책을 찾는 것, 증강 분석은 [[190_ai_llm_requirements_specification|AI]] 사서가 "이런 책도 관심 있으실 것 같아요"라고 먼저 추천해주는 것이다.

## Ⅳ. 실무 적용 및 기술사 판단

### 도입 [[435_checklist_based_testing|체크리스트]]

- [ ] 비기술 사용자 비율 파악: 70% 이상이면 NLQ 중심 도구 선택
- [ ] [[001_dikw_pyramid|데이터]] 품질 선행 확보: NLQ는 [[005_schema|스키마]] 불일치 시 오답 [[087_process_state_transition|생성]]
- [ ] [[263_llm_large_language_model|LLM]] 연동 보안 검토: [[298_qkv_attention|쿼리]]에 PII 포함 가능성 [[396_validation|확인]]
- [ ] Auto-Insight 결과 [[395_verification_process_review|검증]] 프로세스: 오탐율 [[229_monitor|모니터]]링
- [ ] [[001_dikw_pyramid|데이터]] 접근 제어: 역할 기반 [[001_dikw_pyramid|데이터]] 접근 [[164_policy|정책]]

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

| [[128_water_scrum_fall_anti_pattern|안티패턴]] | 문제 | 해결 방법 |
|:---|:---|:---|
| [[001_dikw_pyramid|데이터]] 품질 무시하고 NLQ 도입 | 오답 [[087_process_state_transition|생성]] → 사용자 불신 | [[001_dikw_pyramid|데이터]] 품질 [[018_kpi|KPI]] 먼저 확보 |
| [[190_ai_llm_requirements_specification|AI]] 인사이트 무조건 신뢰 | 비즈니스 맥락 없는 인사이트 | [[064_relation_domain|도메인]] 전문가 [[395_verification_process_review|검증]] 필수 |

📢 **섹션 요약 비유**: [[190_ai_llm_requirements_specification|AI]] BI의 자동 인사이트는 자동차 경고등이다. [[130_signal|신호]]를 보내도 운전자가 원인을 이해하고 판단해야 한다. 경고등만 믿고 핸들을 놓으면 안 된다.

## Ⅴ. 기대효과 및 결론

| 항목 | 도입 전 | 도입 후 |
|:---|:---|:---|
| 보고서 [[087_process_state_transition|생성]] 시간 | 2~5일 | 수분 (자동 [[087_process_state_transition|생성]]) |
| [[001_dikw_pyramid|데이터]] 접근 가능 인력 | 전체 5~[[489_raid_10_hybrid|10]]% | 전체 60~80% |
| 인사이트 발견 [[015_지연_데이터_관점|지연]] | 분석 요청 후 1주일 | 실시간 자동 제안 |

📢 **섹션 요약 비유**: [[190_ai_llm_requirements_specification|AI]] BI는 탁월한 부조종사다. 조종사(분석가)는 중요한 결정에 집중하고, 부조종사는 반복 계기 [[396_validation|확인]]을 자동으로 처리한다.

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---|:---|:---|
| NLQ | 핵심 기능 | 자연어로 [[001_dikw_pyramid|데이터]] 질의 |
| Auto-Insight | 핵심 기능 | [[190_ai_llm_requirements_specification|AI]] 기반 자동 인사이트 발견 |
| [[001_dikw_pyramid|Data]] Storytelling | 출력 형태 | 분석 결과 자동 내러티브화 |
| Augmented Analytics | 패러다임 | [[190_ai_llm_requirements_specification|AI]] 강화 셀프서비스 BI |

### 📈 관련 키워드 및 발전 흐름도

```
전통 BI - 수작업 SQL 쿼리 + 정적 대시보드
    │
    ▼
셀프서비스 BI (Power BI, Tableau) - 드래그앤드롭
    │
    ▼
Augmented Analytics - AI/ML 자동 인사이트 발굴
    │
    ▼
NLQ (자연어 쿼리) + Auto-Narrative 리포트
    │
    ▼
GenAI BI - LLM 기반 대화형 데이터 분석
```

> **키워드**: Augmented Analytics, NLQ, [[176_automl_hyperparameter_optimization_bayesian|AutoML]] BI, Self-[[090_service_kubernetes_network_load_balancing|Service]] BI, [[165_power_bi|Power BI]], [[164_tableau|Tableau]], GenAI BI, Smart Insight

### 👶 어린이를 위한 3줄 비유 설명

1. 증강 분석은 "지난달 어느 과자가 제일 많이 팔렸어?"라고 말만 해도 [[070_graph_datastructure|그래프]]를 그려주는 컴퓨터예요.
2. Auto-Insight는 컴퓨터가 스스로 "이 상품 판매가 갑자기 줄었는데 왜 그럴까요?"라고 먼저 알려주는 기능이에요.
3. [[001_dikw_pyramid|Data]] Storytelling은 숫자들을 읽기 쉬운 이야기로 바꿔주는 거예요.
