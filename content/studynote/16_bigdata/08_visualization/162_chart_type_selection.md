+++
title = "162. 차트 유형 선택 (Chart Type Selection) — 비교/추세/비율/분포별 적합 차트"
date = 2026-04-21

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)

- **본질**: 차트 유형 선택은 "어떤 차트가 예쁜가"가 아니라 "독자에게 어떤 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이야기(비교/추세/비율/분포/상관/흐름/지리)를 전달할 것인가"에서 시작하는 커뮤니케이션 설계다.
- **가치**: 잘못된 차트 선택은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 오해를 유발한다 — 5개 이상의 범주에 파이 차트를 쓰거나, 연속 시계열에 막대 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)를 쓰면 패턴이 보이지 않는다.
- **판단 포인트**: 상키 다이어그램(Sankey Diagram)은 흐름과 볼륨을 동시에 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)하는 고급 차트로, 사용자 여정·에너지 흐름·물류 분석에서 꺾은선·막대로는 불가능한 인사이트를 제공한다.

---

## Ⅰ. 개요 및 필요성

### 잘못된 차트 선택의 대가

같은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)라도 어떤 차트를 선택하느냐에 따라 전혀 다른 해석을 유발한다:

- **파이 차트로 7개 범주**: 5% 차이의 [슬라이스](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/)를 시각적으로 구분 불가
- **막대 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)로 시계열 추세**: 증감 방향성은 보이지만 [모멘텀](/knowledge-base/studynote/10_ai/03_llm_nlp/276_momentum_optimizer/)(가속도) 파악 어려움
- **히스토그램 vs 막대 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 혼동**: 히스토그램은 연속형(구간), 막대는 범주형
- **3D 파이 차트**: 원근법으로 앞쪽 [슬라이스](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/)가 더 크게 보이는 시각적 왜곡

**📢 섹션 요약 비유**: 차트 선택은 **운동 종목 선택**과 같다. 헤엄치려면 수영복, 달리려면 운동화 — 상황에 맞지 않는 장비(차트)를 쓰면 목적을 달성할 수 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이야기 유형별 차트 선택 체계

```
┌────────────────────────────────────────────────────────────┐
│              차트 선택 결정 트리                            │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  무엇을 이야기할 것인가?                                    │
│       │                                                    │
│  ┌────┴────┬────────┬──────────┬──────────┬──────────┐    │
│  │비교     │추세    │비율      │분포      │상관      │    │
│  │Compare  │Trend   │Part-Whole│Distribut.│Correlat. │    │
│  └────┬────┴─┬──────┴──┬───────┴──┬───────┴──┬───────┘    │
│       │      │         │          │          │            │
│      막대   꺾은선    파이(≤5)   히스토그램  산점도        │
│      그래프  그래프   도넛      박스플롯   버블차트        │
│      (Bar)  (Line)   트리맵    바이올린   히트맵          │
│      그룹형 Area     워터폴    능선 그림               │
│      누적형 Sparkline                                      │
└────────────────────────────────────────────────────────────┘
```

### 유형별 상세 차트 가이드

#### 1. 비교(Comparison)

| 차트 | 적합 상황 | 주의사항 |
|:---|:---|:---|
| **가로 막대** | 범주 수 많음 (5개+), 긴 레이블 | Y축 반드시 0 시작 |
| **세로 막대 (컬럼)** | 시간 비교, 범주 수 적음 | 3D 금지 |
| **그룹 막대** | 범주 내 하위 그룹 비교 | 그룹 수 3개 이하 권장 |
| **누적 막대** | 전체 대비 부분 비교 | 중간 층의 절대값 비교 어려움 |

#### 2. 추세(Trend)

| 차트 | 적합 상황 | 주의사항 |
|:---|:---|:---|
| **꺾은선 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)** | 연속 시계열, 다중 계열 비교 | 계열 수 5개 이하 권장 |
| **Area Chart** | 볼륨 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/), 누적 추세 | 전체가 가려지는 문제 |
| **Sparkline** | 표 안의 미니 추세선 | 상세값보다 방향성 전달 |

#### 3. 비율(Part-to-Whole)

| 차트 | 적합 상황 | 주의사항 |
|:---|:---|:---|
| **파이 차트** | 범주 2-5개, 합이 100% | 범주 5개 이상 금지 |
| **도넛 차트** | 중앙에 [KPI](/knowledge-base/studynote/12_it_management/01_governance_strategy/018_kpi/) 수치 표시 | 파이와 동일 주의사항 |
| **트리맵** | 계층적 비율 (시장점유율 지역별) | 같은 면적 구분 어려움 |
| **워터폴** | 누적 증감 표시 (재무 분석) | 기준값 명확히 표시 |

#### 4. 분포(Distribution)

| 차트 | 적합 상황 | 장점 |
|:---|:---|:---|
| **히스토그램** | 단일 연속형 변수 분포 | 빈도 분포 직관적 |
| **박스 플롯** | 그룹 간 분포 비교 | 사분위수·[이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/) 표시 |
| **바이올린 플롯** | 분포 형태 + 박스 플롯 통합 | 분포 밀도 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) |
| **능선 플롯 (Ridgeline)** | 다중 그룹 분포 시계열 | 시간 흐름 분포 변화 |

#### 5. 상관관계(Correlation/[Relationship](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/))

| 차트 | 적합 상황 | 특징 |
|:---|:---|:---|
| **산점도** | 2개 연속형 변수 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 기본 [상관 분석](/knowledge-base/studynote/06_ict_convergence/05_data_science/325_correlation_analysis_pearson_spearman/) |
| **버블 차트** | 3번째 변수 크기 인코딩 | 다변수 표현 |
| **히트맵** | 상관 행렬, 시간×범주 패턴 | 많은 변수 간 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
| **쌍 플롯(Pair Plot)** | 다변수 상관 매트릭스 | 탐색적 분석 |

**📢 섹션 요약 비유**: 차트 유형 선택은 **레스토랑 메뉴 선택**과 같다. 비교(샐러드 바), 추세(코스 요리), 비율(뷔페 접시 구성), 분포(셰프 추천 다양성) — 각 목적에 맞는 메뉴(차트)가 있다.

---

## Ⅲ. 비교 및 연결

### 고급 차트: 상키 다이어그램(Sankey Diagram)

상키 다이어그램은 **노드(Node) 간 흐름의 양([Volume](/knowledge-base/studynote/14_data_engineering/01_infrastructure/001_bigdata_3v_5v/))**을 표시하는 특수 차트다:

```
[방문] ─── 1000 ─→ [홈페이지]
                        │
               600 ─→ [상품 목록]
                        │
               300 ─→ [장바구니]
                        │
               150 ─→ [결제 완료]
               150 ────→ [이탈]
```

- **선 두께**: 흐름의 양에 비례
- 적용: 사용자 여정 분석, 에너지 흐름 (Sankey가 처음 개발한 증기 효율 분석), 물류 경로

### 코드 다이어그램(Chord Diagram)

원형 배치의 노드 간 **양방향 흐름**을 표시:
- 지역 간 인구 이동
- 국가 간 무역 흐름
- 소셜 네트워크 상호 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)

**📢 섹션 요약 비유**: 상키 다이어그램은 **강줄기 지도**와 같다. 강(흐름)의 굵기가 수량을 나타내며, 강이 어디서 어디로 흘러가는지(방향성)와 얼마나 흐르는지(볼륨)를 동시에 보여준다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 차트 선택 실수 방지 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

```
파이 차트 사용 전:
  □ 범주 수가 5개 이하인가?
  □ 합이 100%인가?
  □ 범주 간 비율 차이가 충분한가 (5% 이상)?
  □ 트리맵이 더 적합하지 않은가?

꺾은선 그래프 사용 전:
  □ X축이 연속적인 시간인가?
  □ 데이터 포인트 간 연속성이 논리적인가?

히스토그램 사용 전:
  □ 데이터가 연속형인가? (범주형이면 막대 그래프)
  □ 적절한 빈(Bin) 크기를 선택했는가?
```

### 분야별 차트 선택 가이드

| 분야 | 주요 차트 | 이유 |
|:---|:---|:---|
| 금융 분석 | 캔들스틱, 워터폴, 면적 차트 | 가격 변동, 재무 누적 표현 |
| 마케팅 | 퍼널 차트, 상키, 세그먼트 막대 | 전환율, 고객 여정 분석 |
| 의료·바이오 | 생존 분석([Kaplan-Meier](/knowledge-base/studynote/06_ict_convergence/05_data_science/393_survival_analysis_kaplan_meier/)), 박스 플롯 | 임상 결과 분포 비교 |
| 지리 정보 | 코로플레스, 버블 맵, 히트맵 | 공간 패턴 표현 |

**📢 섹션 요약 비유**: 분야별 표준 차트는 **직업별 유니폼**과 같다. 의사는 가운, 소방관은 방화복 — 해당 분야의 목적에 최적화된 표준 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) 언어가 있다.

---

## Ⅴ. 기대효과 및 결론

### 적절한 차트 선택의 효과

| 영역 | 효과 |
|:---|:---|
| **이해 속도** | 5초 안에 핵심 인사이트 파악 가능 |
| **분석 품질** | 적합한 차트로 숨겨진 패턴 발견 |
| **커뮤니케이션** | 비기술 [이해관계자](/knowledge-base/studynote/04_software_engineering/03_design_architecture/173_stakeholder_identification_impact_matrix/)도 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이해 가능 |
| **[신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)** | 올바른 차트로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 왜곡 방지 |

### 결론

차트 유형 선택은 **[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 스토리텔링의 첫 번째 결정**이다. "어떤 이야기를 전달할 것인가?"에서 시작하여 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 특성(범주형/연속형/시계열)과 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 유형(비교/추세/비율/분포/상관)에 따라 최적의 차트를 선택해야 한다. 잘못된 차트는 올바른 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 오해하게 만드는 치명적인 커뮤니케이션 오류다.

**📢 섹션 요약 비유**: 차트 선택은 **이야기 형식 선택**과 같다. 소설(꺾은선 — 시간 흐름), 사진(산점도 — [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)), 지도(코로플레스 — 지리), 파이 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)(파이 — 비율) — 각 이야기에 맞는 형식이 있다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| 비교 차트 | 유형 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 막대, 그룹 막대, 누적 막대 |
| 추세 차트 | 유형 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 꺾은선, Area Chart, Sparkline |
| 비율 차트 | 유형 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 파이, 도넛, 트리맵, 워터폴 |
| 분포 차트 | 유형 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 히스토그램, 박스 플롯, 바이올린 |
| 상관 차트 | 유형 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 산점도, 버블, 히트맵 |
| 상키 다이어그램 | 고급 차트 | 흐름 볼륨 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) |
| Chartjunk | 제거 대상 | 시각적 노이즈 — 3D, 그림자 등 |

### 📈 관련 키워드 및 발전 흐름도

```text
[비교 차트]
    │
    ▼
[추세 차트]
    │
    ▼
[비율 차트]
    │
    ▼
[분포 차트]
    │
    ▼
[상관 차트]
```

이 흐름도는 비교 차트에서 출발해 Chartjunk까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

- 차트 유형 선택은 **숙제 발표 형식 선택**과 같아요: 시간의 변화를 설명하려면 꺾은선 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/), 비율을 보여주려면 파이 차트 — 이야기에 맞는 형식을 써야 친구들이 이해할 수 있어요.
- 파이 차트에 10개 조각을 넣으면 어느 것이 더 큰지 알 수 없어요 — 케이크를 10조각으로 자르면 다 비슷하게 보이잖아요!
- 상키 다이어그램은 **강물 지도**예요: 강물이 어디서 갈라지고 어디로 흘러가는지, 그리고 얼마나 많이 흐르는지(선 두께)를 한눈에 보여줘요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 162 / 262

← **이전**: [161. 데이터 시각화 원칙 (Data Visualization Principles) — Tufte 데이터 잉크 비율](/knowledge-base/studynote/16_bigdata/08_visualization/161_visualization_principles/)
**다음**: [163. 대시보드 설계 (Dashboard Design) — KPI 중심 5초 규칙 인터랙티브](/knowledge-base/studynote/16_bigdata/08_visualization/163_dashboard_design/) →

---
