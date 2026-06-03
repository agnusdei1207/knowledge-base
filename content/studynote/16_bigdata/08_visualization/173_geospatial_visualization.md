+++
title = "173. 지리공간 시각화 (Geospatial Visualization) — Kepler.gl, Folium, Deck.gl"
date = 2026-04-21

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 지리공간 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) (Geospatial Visualization)는 위치 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 지도 위에 찍는 작업이 아니라, 공간 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)·밀도·이동 흐름을 사람의 눈이 읽을 수 있는 레이어로 번역하는 분석 기법이다.
> 2. **가치**: Kepler.gl은 대규모 공간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 빠르게 탐색하는 데 강하고, Folium은 Python 중심 보고서에 가볍게 붙이기 좋으며, Deck.gl은 제품 수준의 고성능 맞춤형 지도를 만드는 데 유리하다.
> 3. **판단 포인트**: 좋은 지도는 점을 많이 그리는 지도가 아니라, 줌 수준·공간 집계·투영법·[개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)를 함께 고려해 "무엇을 읽게 할 것인가"를 먼저 정한 지도다.

---

## Ⅰ. 개요 및 필요성

지리공간 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)는 위도·경도, 선형 경로, 행정 구역, 래스터 (Raster) 같은 위치 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 지도 위에서 의미 있는 패턴으로 드러내는 방법이다. 같은 판매 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)라도 표로 보면 지점별 숫자만 보이지만, 지도에 올리면 상권 공백, 군집, 이동 축, 생활권 경계처럼 공간적 구조가 바로 보인다. 그래서 물류, 교통, 재난 대응, 부동산, 마케팅, 스마트시티 같은 분야에서는 "얼마나 많은가"만큼 "어디에서 일어나는가"가 중요하다.

하지만 지도는 일반 차트보다 어려운 점이 많다. 점이 수백만 개로 늘어나면 과밀 표시 (Overplotting)가 생기고, 시야를 넓히면 개별 점은 의미를 잃는다. 또한 구면 좌표를 평면 지도에 옮기는 투영법이 면적과 거리 해석을 바꾸고, 이동 경로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 시간축까지 포함하므로 단순 산점도로는 핵심을 잃기 쉽다.

즉 지리공간 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)의 필요성은 "지도 배경이 예뻐서"가 아니라, 공간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만의 질문이 따로 있기 때문이다. 어느 지역이 밀집되는가, 어느 경로로 이동하는가, 행정 구역별 불균형이 어디에 있는가, 어느 시점에 어디서 [이상치](/knowledge-base/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)가 생기는가 같은 질문은 공간적 표현이 있어야 제대로 드러난다.

특히 Global Positioning System (GPS) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 배달 경로, 차량 텔레매틱스, 휴대폰 이동 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)처럼 시공간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 커질수록 지도는 단순 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)가 아니라 탐색 인터페이스가 된다. 그래서 도구 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) "그릴 수 있느냐"가 아니라, "얼마나 큰 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 어떤 방식으로 읽게 하느냐"의 문제로 바뀐다.

- **📢 섹션 요약 비유**: 지리공간 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)는 주소가 적힌 긴 명단을 보는 대신, 도시 지도 위에 핀과 선을 꽂아 어디가 붐비고 어디가 비는지 한눈에 보는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

좋은 지리공간 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)는 원본 좌표를 곧바로 뿌리는 대신, 좌표계 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)와 공간 집계, 렌더링 계층을 거쳐 만들어진다. 일반적인 흐름은 Coordinate [Reference](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) System ([CRS](/knowledge-base/studynote/09_security/05_web_app_security/243_owasp_core_rule_set_crs_waf_anomaly_scoring/)) 정리 → 공간 인덱싱 → 레이어 선택 → 타일 또는 집계 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) → 클라이언트 렌더링 순서다. 이 중 어느 단계를 생략하느냐에 따라 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 해석력이 동시에 흔들린다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Geospatial visualization pipeline</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">raw points / lines / polygons / raster</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">CRS normalization + cleaning</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">spatial index / aggregation</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ H3 hex cells</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ grid / tile bucket</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ region join</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">render layer</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ point / heatmap</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ hex / choropleth</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ arc / trip / 3D</div></div>
</div>
</div>



레이어 선택은 질문 선택과 같다. 개별 위치를 봐야 하면 포인트 레이어가 맞고, 밀도를 봐야 하면 히트맵이나 헥사곤 집계가 맞다. 행정 구역 간 비교는 코로플레스 (Choropleth)가 적합하고, 출발지-도착지 흐름은 Arc Layer나 Flow Map이 더 낫다. 같은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다른 레이어로 그리면 완전히 다른 질문에 답하게 된다.

| 레이어 | 잘 드러나는 것 | 주의점 |
| :--- | :--- | :--- |
| Point | 개별 이벤트, 이상 좌표 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 많으면 과밀 표시 |
| Heatmap / Hex | 밀집 지역, 핫스팟 | 개별 이벤트 해석은 약해짐 |
| Choropleth | 행정 구역별 비교 | 절대값 사용 시 면적 왜곡과 오해 가능 |
| Arc / Trip | 이동 방향, 출발-도착 흐름 | 선이 많아지면 시각 혼잡 증가 |

공간 집계에서 자주 쓰이는 것이 H3 육각형 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) (Hexagonal Hierarchical Spatial [Index](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/))다. 육각형은 사각형보다 인접 방향 편향이 적고, 같은 줌 수준에서 비교적 균일한 셀을 제공해 밀도 분석에 유리하다. 따라서 수백만 개 GPS 포인트를 그대로 그리기보다 H3 셀 단위로 묶으면 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)도 좋아지고 패턴도 더 선명해진다.

또한 대용량 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)에서 핵심은 Web Graphics [Library](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) (WebGL) 기반 렌더링이다. Kepler.gl과 Deck.gl이 강한 이유는 Central Processing Unit (CPU) 중심의 [Document](/knowledge-base/studynote/14_data_engineering/01_infrastructure/037_document/) Object Model (DOM) 조작 대신 [Graphics Processing Unit](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) ([GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/))에 점·선·폴리곤 렌더링을 맡기기 때문이다. 반대로 Folium은 Leaflet 기반이라 빠르게 시작하기 좋지만, 수백만 건을 실시간으로 다루는 데는 한계가 있다.

- **📢 섹션 요약 비유**: 지도 그리기는 재료를 한꺼번에 식탁 위에 쏟아 놓는 일이 아니라, 비슷한 재료를 묶고 접시에 맞게 나눠 담아 손님이 한눈에 이해하게 만드는 플레이팅과 같다.

---

## Ⅲ. 비교 및 연결

Kepler.gl, Folium, Deck.gl은 모두 지도 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)를 하지만 역할이 다르다. Kepler.gl은 업로드 후 바로 여러 레이어를 시험할 수 있어 탐색형 분석에 강하고, Deck.gl은 애플리케이션 안에 고성능 지도 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)를 직접 설계할 수 있어 제품화에 적합하다. Folium은 Python Notebook, 리포트, 교육용 데모처럼 "빠르게 지도 하나를 만들어 공유"하는 데 강점이 있다.

| 도구 | 강점 | 약점 | 잘 맞는 상황 |
| :--- | :--- | :--- | :--- |
| Kepler.gl | Graphical User Interface (GUI) 기반 빠른 탐색, WebGL, 다양한 레이어 | 세밀한 제품 통합은 제한적 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 탐색, 분석가용 대시보드 |
| Folium | Python 친화성, 간단한 HyperText Markup Language (HTML) 산출 | 대규모 실시간 렌더링 한계 | Notebook, 보고서, 교육 |
| Deck.gl | 고성능, 세밀한 커스터마이징, 앱 통합 | [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 개발 난이도 높음 | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)형 지도, 대규모 인터랙션 |

표현 방식도 비교가 필요하다. 포인트 맵은 이벤트 위치를 살리지만 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 많을수록 털실 뭉치가 되고, 코로플레스는 행정 구역 비교에 좋지만 면적 큰 지역이 시각적으로 과대평가될 수 있다. 헥사곤 집계는 밀도 패턴을 잘 보여 주지만, 실제 행정 경계와 직접 일치하지 않을 수 있다. 즉 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) 유형 선택은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조와 의사결정 질문을 함께 봐야 한다.

또 하나의 중요한 연결점은 투영법이다. 웹 지도 표준인 Web Mercator는 탐색과 내비게이션에 편리하지만 고위도에서 면적 왜곡이 커진다. 따라서 인구 밀도나 토지 면적처럼 "넓이 비교"가 핵심이면 Equal-Area Projection을 검토해야 한다. 지도는 배경이 아니라 해석의 일부이므로, 투영법이 바뀌면 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지도 바뀐다.

이 영역은 Geographic Information System (GIS), PostGIS, GeoParquet, 벡터 타일과도 연결된다. 즉 프런트엔드 지도를 잘 그리는 것만으로는 충분하지 않고, 서버 쪽 공간 조인과 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/), 저장 포맷, 타일링 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 함께 맞아야 실무적인 대규모 지도가 완성된다.

- **📢 섹션 요약 비유**: 같은 도시라도 관광 지도를 만들 때와 재난 대피 지도를 만들 때 강조해야 할 정보가 다르듯이, 도구와 레이어와 투영법도 질문에 맞게 달라져야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 먼저 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 규모와 목적을 구분해야 한다. 분석가가 하루 동안 업로드한 택시 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 빠르게 탐색하려면 Kepler.gl이 적합하고, Python [데이터 파이프라인](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/) 결과를 보고서에 붙이려면 Folium이면 충분하다. 반면 수백만 건 이상을 사용자 인터랙션과 함께 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)해야 하면, 서버 측 집계와 벡터 타일을 준비한 뒤 Deck.gl이나 PyDeck으로 전달하는 구성이 현실적이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Practical decision workflow</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">exploration by analyst?</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ yes -&gt; Kepler.gl</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ no</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">notebook / static report?</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ yes -&gt; Folium</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ no</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">product-scale interactive map?</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ yes -&gt; Deck.gl + server-side aggregation / tiles</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ no -&gt; lightweight map stack</div></div>
</div>
</div>



### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 줌 레벨별로 다른 집계 단위를 준비한다. 전역은 H3 집계, 근접 확대는 포인트 표시가 일반적이다.
2. 코로플레스는 절대 건수보다 면적·인구·수요 기반 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 여부를 먼저 검토한다.
3. GeoJSON을 그대로 크게 보내기보다 GeoParquet, PostGIS, vector tile로 전처리한다.
4. 이동 경로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 익명화, 일반화, 시간 해상도 조정으로 [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) 노출을 줄인다.
5. 3D [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)와 애니메이션은 정보 가치가 있을 때만 쓰고, 단순 장식이라면 오히려 해석을 방해한다.

### 선택 판단

| 상황 | 권장 판단 | 이유 |
| :--- | :--- | :--- |
| 수십만 건 이하 탐색형 분석 | Kepler.gl | GUI로 빠르게 레이어 실험 가능 |
| Python 분석 결과 공유 | Folium | 코드 양이 적고 산출물이 단순함 |
| 수백만 건 이상 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)형 지도 | Deck.gl + 집계 타일 | [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 렌더링과 커스터마이징 필요 |
| 핫스팟 분석 | H3 / hexbin / heatmap | 점보다 밀도 패턴이 중요 |
| 행정 구역 비교 | Choropleth + [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) | 구역 단위 의미를 살리기 좋음 |

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 수백만 포인트를 전부 포인트 레이어로만 그려 패턴도 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)도 모두 잃는 것
- 면적이 큰 지역의 절대값만 코로플레스로 칠해 밀도 해석을 왜곡하는 것
- Web Mercator 왜곡을 무시한 채 면적 비교 결론을 내리는 것
- 개인 이동 궤적을 그대로 공개해 프라이버시 위험을 키우는 것

기술사 답안에서는 <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 규모 → 공간 집계 → 도구 선택 → 투영법 → <a href="/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/">개인정보</a> <a href="/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/">보호</a></strong> 순서로 정리하면 실무성이 높다. 지리공간 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)는 예쁜 지도 제작이 아니라, 질문에 맞는 공간 요약과 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 설계의 문제다.

- **📢 섹션 요약 비유**: 도시 전체 상황판을 만들 때 집집마다 불빛 하나씩 그대로 보여 주는 것보다, 동네별 열기와 길 흐름을 적절히 묶어 보여 주는 편이 훨씬 이해하기 쉽다.

---

## Ⅴ. 기대효과 및 결론

지리공간 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)를 잘 설계하면 숫자 표에서는 보이지 않던 핫스팟, 이동 축, 공백 지역, 공급 불균형이 한눈에 드러난다. 이는 물류 동선 최적화, 상권 분석, 재난 대응, 도시 운영, 환경 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링처럼 공간적 의사결정이 핵심인 분야에서 큰 힘을 발휘한다. 특히 시계열을 결합하면 "어디서"뿐 아니라 "언제" 문제가 생기는지까지 함께 읽을 수 있다.

하지만 지도는 해석을 쉽게 해 주는 동시에 오해도 쉽게 만든다. 투영 왜곡, 부적절한 집계, 지나친 3D 효과, 과도한 점 표시는 잘못된 인상을 줄 수 있다. 또한 위치 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 개인 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 위험이 높아, [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/) 품질만큼 익명화와 [접근 통제](/knowledge-base/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/)가 중요하다.

따라서 이 주제는 "지도를 예쁘게 그리는 기술"이 아니라, <strong>공간 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 질문에 맞게 요약하고 안전하게 전달하는 기술</strong>로 기억해야 한다. Kepler.gl, Folium, Deck.gl의 차이도 결국 도구 취향이 아니라 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 규모와 운영 목적의 차이다.

- **📢 섹션 요약 비유**: 좋은 지도는 동네 전체를 축소해 붙여 놓은 사진이 아니라, 길·건물·[신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 중 지금 가장 필요한 것만 골라 보여 주는 안내판과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| H3 Hexagonal [Index](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) | 대규모 포인트를 균일한 육각형 셀로 집계하는 방식 |
| Choropleth | 구역 단위 비교에 적합한 대표 지도 표현 |
| Vector Tile | 큰 공간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 줌 단위로 나눠 빠르게 전달하는 방식 |
| [CRS](/knowledge-base/studynote/09_security/05_web_app_security/243_owasp_core_rule_set_crs_waf_anomaly_scoring/) / Projection | 공간 좌표를 어떤 기준으로 해석할지 결정하는 기초 |
| GeoParquet | 대용량 공간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 컬럼형으로 저장하는 포맷 |
| PostGIS | 서버 측 공간 조인과 인덱싱을 담당하는 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 확장 |
| Deck.gl Layer | WebGL 기반 대규모 지도 렌더링의 핵심 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Raw GPS / polygon / raster data</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">CRS normalization + spatial indexing</div>
<div class="kb-diagram-tree-item" style="--depth:2">H3 / grid aggregation</div>
<div class="kb-diagram-tree-item" style="--depth:2">region join</div>
<div class="kb-diagram-tree-item" style="--depth:2">vector tile generation</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Interactive map rendering</div>
<div class="kb-diagram-tree-item" style="--depth:2">Folium for lightweight reporting</div>
<div class="kb-diagram-tree-item" style="--depth:2">Kepler.gl for rapid exploration</div>
<div class="kb-diagram-tree-item" style="--depth:2">Deck.gl for product-scale WebGL apps</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Real-time geo analytics / digital twin / spatial decision support</div>
</div>
</div>



이 흐름은 공간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 단순 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에서 출발해, 인덱싱과 집계를 거쳐, 대화형 지도와 실시간 의사결정 플랫폼으로 확장되는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 지리공간 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)는 주소가 적힌 긴 종이를 보는 대신, 지도 위에 색점과 선으로 어디가 붐비는지 보여 주는 거예요.
2. 점이 너무 많으면 벌집 모양 칸으로 묶어서 어느 동네가 더 뜨거운지 쉽게 볼 수 있어요.
3. 그래서 배달길이나 교통길을 한눈에 보고 어디가 막히는지 빨리 알 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 173 / 262

← **이전**: [172. 네트워크 시각화 (Network Visualization)](/knowledge-base/studynote/16_bigdata/08_visualization/172_network_visualization/)
**다음**: [174. 빅데이터 시각화 도전 (Big Data Visualization Challenges) — 집계/샘플링/렌더링 최적화](/knowledge-base/studynote/16_bigdata/08_visualization/174_bigdata_visualization_challenges/) →

---
