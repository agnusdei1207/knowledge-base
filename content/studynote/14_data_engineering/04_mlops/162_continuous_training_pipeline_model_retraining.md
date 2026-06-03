+++
title = "162. CT (Continuous Training) 파이프라인 - 모델 성능 저하 시 자동 재학습"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CT (Continuous [Training](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/))는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 세계의 변화를 ML 모델이 자동으로 따라잡도록, 재학습 파이프라인을 [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 기반으로 자동 실행하는 [MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/) 핵심 메커니즘이다.
> 2. **가치**: 수작업 재학습의 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)(수주)을 자동화(수시간)로 단축하여 [모델 드리프트](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/468_model_drift_retraining/)로 인한 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하를 사전에 차단하고, 비즈니스 손실을 최소화한다.
> 3. **판단 포인트**: 재학습 빈도가 높을수록 모델 신선도는 높아지나 컴퓨팅 비용과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 레이블링 비용이 증가하므로, [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 조건과 재학습 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)(전체 vs 증분)을 비즈니스 요구에 맞게 설계해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 CT (Continuous [Training](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/))란?

<strong>CT (Continuous <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/">Training</a>)</strong>는 ML 파이프라인을 자동으로 주기적 또는 이벤트 기반으로 실행하여, 최신 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 모델을 재학습하고 배포하는 자동화 체계다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">기존 방식 (수동 재학습) CT 방식 (자동 재학습)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">데이터 과학자가 수동으로</div><div class="kb-diagram-cell">트리거 감지</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">성능 저하 인지</div><div class="kb-diagram-cell">(일정/데이터/성능)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">재학습 스크립트 실행</div><div class="kb-diagram-cell">→</div><div class="kb-diagram-cell">파이프라인 자동 실행</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">↓</div><div class="kb-diagram-cell">데이터 검증 → 학습 → 평가</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">수동 모델 평가 및 배포</div><div class="kb-diagram-cell">↓</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">수주 소요</div><div class="kb-diagram-cell">자동 배포 또는 알람</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">수시간 소요</div></div>
</div>
</div>



### 1.2 CT가 필요한 이유

| 문제 상황 | 설명 | CT 해결 |
|:---|:---|:---|
| **계절성** | 쇼핑몰 구매 패턴이 명절마다 변화 | 주기적 재학습 |
| **사용자 행동 변화** | 스마트폰 보급으로 모바일 패턴 급증 | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 재학습 |
| **외부 충격** | COVID-19로 여행 수요 급감 | 즉시 재학습 |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 누적</strong> | 새 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 1만 건 이상 쌓이면 업데이트 필요 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 재학습 |
| **사기 패턴 변화** | 새로운 신용카드 사기 수법 등장 | 드리프트 감지 후 재학습 |

📢 **섹션 요약 비유**: CT는 날씨 예보 시스템과 같다. 기상 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 실시간으로 바뀌는 것처럼 비즈니스 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)도 계속 변하고, 예보 모델이 자동으로 최신 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 학습해 정확도를 유지하는 것처럼 CT는 ML 모델의 신선도를 자동으로 유지한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 CT [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 3가지 방식

| [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 종류 | 조건 | 장점 | 단점 |
|:---|:---|:---|:---|
| **일정 기반 (Schedule Trigger)** | 매일/매주/매월 정해진 시각 | 예측 가능, 리소스 계획 용이 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변화와 무관하게 실행 |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 기반 (<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a> Trigger)</strong> | 새 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) N건 이상 수집 시 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 충분히 쌓인 후 학습 | 변화 속도와 불일치 가능 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 기반 (<a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">Performance</a> Trigger)</strong> | 정확도/F1이 임계값 이하로 하락 | 진짜 필요할 때만 실행 | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하 후 대응 (사후적) |

### 2.2 CT 파이프라인 상세 구성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">CT 파이프라인 전체 흐름</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">트리거</div><div class="kb-diagram-cell">데이터</div><div class="kb-diagram-cell">피처</div><div class="kb-diagram-cell">모델</div><div class="kb-diagram-cell">모델</div><div class="kb-diagram-cell">자동</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">감지</div><div class="kb-diagram-cell">검증</div><div class="kb-diagram-cell">엔지니</div><div class="kb-diagram-cell">학습</div><div class="kb-diagram-cell">평가</div><div class="kb-diagram-cell">배포</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">어링</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Schedule</div><div class="kb-diagram-cell">스키마</div><div class="kb-diagram-cell">피처</div><div class="kb-diagram-cell">분산</div><div class="kb-diagram-cell">정확도</div><div class="kb-diagram-cell">통과 →</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Data</div><div class="kb-diagram-cell">검증</div><div class="kb-diagram-cell">계산</div><div class="kb-diagram-cell">학습</div><div class="kb-diagram-cell">F1-Score</div><div class="kb-diagram-cell">모델 레지</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Perf</div><div class="kb-diagram-cell">이상값</div><div class="kb-diagram-cell">정규화</div><div class="kb-diagram-cell">HPO</div><div class="kb-diagram-cell">드리프트</div><div class="kb-diagram-cell">스트리 등록</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Trigger</div><div class="kb-diagram-cell">체크</div><div class="kb-diagram-cell">인코딩</div><div class="kb-diagram-cell">교차검증</div><div class="kb-diagram-cell">비교</div><div class="kb-diagram-cell">→ 카나리</div></div>
<div class="kb-diagram-note">실패 →</div>
<div class="kb-diagram-note">알람 발송</div>
</div>
</div>



### 2.3 CT 파이프라인 상세 단계

#### 단계 1: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Validation](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/))

```python
# TensorFlow Data Validation (TFDV) 예시
import tensorflow_data_validation as tfdv

# 학습 데이터 통계 생성
train_stats = tfdv.generate_statistics_from_csv('train.csv')

# 스키마 추론
schema = tfdv.infer_schema(train_stats)

# 새 데이터 검증
new_stats = tfdv.generate_statistics_from_csv('new_data.csv')
anomalies = tfdv.validate_statistics(new_stats, schema)
```

#### 단계 2: [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 엔지니어링 ([Feature Engineering](/knowledge-base/studynote/12_it_management/02_itsm_itil/081_feature_engineering/))

| 작업 | 설명 | 도구 |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/">피처</a> 변환</strong> | 수치형 [정규화](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/), 범주형 인코딩 | Scikit-learn [Pipeline](/knowledge-base/studynote/12_it_management/02_itsm_itil/082_pipeline/), TF Transform |
| <strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/">피처</a> 선택</strong> | 중요도 기반 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 필터링 | [SHAP](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/327_shap/), Boruta |
| <strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/">피처</a> 저장</strong> | 온라인/오프라인 스토어 업데이트 | Feast, Hopsworks |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 분할</strong> | Train/[Validation](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)/Test 분리 | Stratified Split |

#### 단계 3: 모델 학습 (Model [Training](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/))



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">모델 학습 전략 비교</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">전체 재학습</div><div class="kb-diagram-cell">전체 데이터로 처음부터 학습</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(Full Retraining)</div><div class="kb-diagram-cell">고비용, 높은 정확도</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">증분 학습</div><div class="kb-diagram-cell">새 데이터만으로 기존 모델 업데이</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(Incremental)</div><div class="kb-diagram-cell">저비용, 점진적 성능 개선</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">앙상블 업데이트</div><div class="kb-diagram-cell">새 모델 추가, 가중치 재조정</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(Ensemble Update)</div><div class="kb-diagram-cell">안정성 높음, 복잡성 증가</div></div>
</div>
</div>



#### 단계 4: 모델 평가 및 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 게이트 (Evaluation Gate)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">신규 모델 학습 완료</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">자동 평가 게이트 (Gate)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">① 정확도 &gt; 기준 (예: 90%)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">② F1-Score 개선 여부</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">③ 현재 프로덕션 모델 대비</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">성능 향상 확인</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">④ 지연시간 SLA 충족</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">⑤ 공정성 메트릭 체크</div></div>
<div class="kb-diagram-note">통과 ▼ 실패 ▼</div>
<div class="kb-diagram-note">레지스트리 등록 알람 + 원인 분석</div>
<div class="kb-diagram-note">→ 카나리 배포 → 데이터팀 통보</div>
</div>
</div>



### 2.4 재학습 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 상세 비교

| [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 방법 | 장점 | 단점 | 적합 상황 |
|:---|:---|:---|:---|:---|
| **전체 재학습** | 전체 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 처음부터 | 최고 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 보장 | 높은 컴퓨팅 비용 | 중요 모델, 월 1회 이하 |
| **증분 학습** | 새 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 추가 학습 | 저비용, 빠른 실행 | Catastrophic Forgetting 위험 | 신경망, 온라인 학습 |
| **슬라이딩 윈도우** | 최근 N일 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 사용 | 오래된 패턴 제거 | [윈도우 크기](/knowledge-base/studynote/03_network/08_transport_layer/413_tcp_window_size_flow_control_16bit/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 필요 | 계절성 없는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| <strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/">가중치</a> 기반</strong> | 최신 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 높은 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) | 균형 잡힌 학습 | [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 튜닝 필요 | 대부분의 시계열 |

📢 **섹션 요약 비유**: CT 파이프라인은 레스토랑의 메뉴 자동 업데이트 시스템과 같다. 손님 취향([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))이 바뀌면 자동으로 감지([트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/))하고, 새 레시피를 시험(학습)하고, 맛 검사(평가 게이트)를 통과하면 실제 메뉴에 반영(배포)한다. 기준 미달이면 주방장에게 알람을 보낸다.

---

## Ⅲ. 비교 및 연결

### 3.1 CT [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 방식 심층 비교

| 항목 | 일정 기반 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기반 | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 기반 |
|:---|:---|:---|:---|
| **반응 시간** | 예정된 시각 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 임계값 도달 시 | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하 후 |
| **비용 예측** | 높음 (예측 가능) | 중간 ([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유입량 의존) | 낮음 (필요 시만) |
| <strong><a href="/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/">리스크</a></strong> | 불필요한 재학습 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 이슈 | 저하 구간 노출 |
| **권장 분야** | 금융 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/), 배치 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | [추천 시스템](/knowledge-base/studynote/10_ai/03_llm_nlp/211_recommendation_system/), 검색 | 고가용성 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) |
| **결합 사용** | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) + [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 조합 권장 | | |

### 3.2 Catastrophic Forgetting 문제와 해결



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">증분 학습의 문제 - Catastrophic Forgetting</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">이전 학습 데이터:</div><div class="kb-diagram-node">고양이, 개, 자동차</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">새 학습 데이터:</div><div class="kb-diagram-node">비행기, 배</div></div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">증분 학습 후: 비행기·배는 잘 분류,</div>
<div class="kb-diagram-note">고양이·개·자동차 성능 급락 (Forgetting!)</div>
<div class="kb-diagram-note">해결 방법:</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">① Replay Buffer: 이전 데이터 샘플 보존</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">② EWC (Elastic Weight Consolidation):</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">중요 가중치에 페널티 부여</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">③ Progressive Neural Networks:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">새 태스크에 별도 컬럼 추가</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">④ 전체 재학습 주기 병행</div></div>
</div>
</div>



### 3.3 CT vs 기존 배치 모델 업데이트 비교

| 항목 | 기존 배치 업데이트 | CT 자동화 |
|:---|:---|:---|
| **주기** | 수동 결정 (수주) | [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 기반 (수시간~수일) |
| **인력** | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 과학자 개입 | 자동화 (최소 인력) |
| **재현성** | 낮음 (수동 환경) | 높음 ([컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 기반) |
| <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/">감사</a> 추적</strong> | 어려움 | 파이프라인 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 자동 기록 |
| **실패 처리** | 수동 디버깅 | 자동 알람 + 이전 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 유지 |

📢 **섹션 요약 비유**: CT와 수동 재학습의 차이는 수동 환자 모니터링과 ICU 자동 모니터링의 차이와 같다. 수동 방식은 의사가 주기적으로 돌아보지만(늦은 반응), ICU 자동 시스템은 이상 수치 감지 즉시 알람을 울리고 응급 프로토콜을 자동 실행한다(빠른 반응).

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 CT 비용 vs [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 트레이드오프



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">모델 성능</div>
<div class="kb-diagram-connector">↑</div>
<div class="kb-diagram-note">····················· 이상적 성능 유지선</div>
<div class="kb-diagram-note">╲ ╱╲ ╱╲</div>
<div class="kb-diagram-note">╲ ╱ ╲ ╱ ╲</div>
<div class="kb-diagram-note">╲ ╱ ╲ ╱ ╲···(성능 저하 시작)</div>
<div class="kb-diagram-note">╳ ╳</div>
<div class="kb-diagram-note">재학습 재학습</div>
<div class="kb-diagram-tree-item" style="--depth:1">→ 시간</div>
<div class="kb-diagram-note">너무 자주 재학습 너무 늦은 재학습</div>
<div class="kb-diagram-note">(비용 낭비) (성능 저하 노출)</div>
</div>
</div>



| 재학습 빈도 | 컴퓨팅 비용 | 모델 신선도 | 권장 상황 |
|:---|:---:|:---:|:---|
| **매시간** | 매우 높음 | 최고 | 주식 예측, 사기 탐지 |
| **매일** | 높음 | 높음 | 실시간 추천, 광고 |
| **매주** | 중간 | 중간 | 검색 랭킹, 신용 평가 |
| **매월** | 낮음 | 낮음 | 정적 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 모델 |

### 4.2 기술사 시험 핵심 포인트

**Q. CT 파이프라인에서 평가 게이트(Evaluation Gate)의 역할과 중요성을 설명하시오.**

평가 게이트는 자동 재학습된 모델이 실제 프로덕션에 배포되기 전에 거치는 <strong>자동 품질 <a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a> 관문</strong>이다. 다음 세 가지 기준을 모두 통과해야 배포가 허용된다:
1. <strong>절대 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 기준</strong>: 정확도, [F1-Score](/knowledge-base/studynote/10_ai/03_llm_nlp/255_f1_score/) 등이 최소 기준치 이상
2. <strong>상대 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 기준</strong>: 현재 프로덕션 모델 대비 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상 또는 동등
3. **비기능 요건**: 추론 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/), 메모리 사용량 등

이를 통해 자동화 과정에서 발생할 수 있는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 문제나 코드 버그로 인한 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하 모델이 자동으로 배포되는 위험을 방지한다.

<strong>Q. 재학습 비용 vs 모델 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 저하 트레이드오프를 설명하시오.</strong>

- 재학습이 너무 잦으면: [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 컴퓨팅 비용 급증, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 레이블링 비용 증가
- 재학습이 너무 드물면: [모델 드리프트](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/468_model_drift_retraining/)로 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 품질 저하, 비즈니스 손실 발생
- **최적 해**: [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)를 조합하여 "필요할 때만 재학습" [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 채택

### 4.3 실무 CT 구현 예시 ([Kubeflow](/knowledge-base/studynote/14_data_engineering/04_mlops/167_kubeflow_kubernetes_ml_pipeline/) Pipelines)

```python
# Kubeflow Pipelines DSL로 CT 파이프라인 정의
from kfp import dsl
from kfp.components import func_to_container_op

@dsl.pipeline(name='CT Pipeline', description='Continuous Training')
def ct_pipeline(data_path: str, threshold: float = 0.90):
    # 단계 1: 데이터 검증
    validate_op = validate_data(data_path=data_path)

    # 단계 2: 피처 엔지니어링 (데이터 검증 통과 후)
    features_op = feature_engineering(
        data=validate_op.outputs['validated_data']
    )

    # 단계 3: 모델 학습
    train_op = train_model(
        features=features_op.outputs['features']
    )

    # 단계 4: 평가 게이트
    eval_op = evaluate_model(
        model=train_op.outputs['model'],
        threshold=threshold
    )

    # 단계 5: 조건부 배포
    with dsl.Condition(eval_op.outputs['passed'] == 'true'):
        deploy_op = deploy_model(
            model=train_op.outputs['model']
        )
```

📢 **섹션 요약 비유**: CT 파이프라인은 자동화된 스포츠 팀 훈련 시스템과 같다. 성적([성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/))이 떨어지거나, 새 선수([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))가 충분히 입단하면, 코치 없이도 자동으로 전술 훈련(재학습)이 시작되고, 경기력 테스트(평가 게이트)를 통과한 팀만 실전에 투입된다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 CT 도입 기대효과

| 항목 | 도입 전 | 도입 후 | 개선 |
|:---|:---|:---|:---|
| **재학습 주기** | 분기~반기 (수동) | 수시간~수일 (자동) | [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~100배 단축 |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/04_ai_llm/468_model_drift_retraining/">모델 드리프트</a> 노출</strong> | 수주간 저하 방치 | 즉시 감지 후 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 품질 유지 |
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 과학자 공수</strong> | 재학습에 50% 투입 | 연구개발에 집중 | 생산성 2배 향상 |
| **배포 실패율** | 수동 배포로 20% | 자동 게이트로 5% 미만 | 배포 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 향상 |

### 5.2 CT 설계 시 고려사항



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">CT 설계 체크리스트</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">□ 트리거 조건 명확화 (스케줄/데이터/성능 중 선택)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">□ 학습 데이터 윈도우 크기 결정 (전체 vs 슬라이딩)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">□ 평가 게이트 기준 설정 (절대값 + 상대값 조합)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">□ 실패 시 롤백 전략 (이전 버전 유지)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">□ 재학습 비용 예산 설정 (GPU 사용량 알람)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">□ 데이터 레이블링 파이프라인 연결 (지도학습의 경우)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">□ 피처 스토어 연동 (훈련/서빙 일관성 보장)</div></div>
</div>
</div>



### 5.3 결론

CT (Continuous [Training](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/))는 [MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/) 성숙도 Level 1 이상에서 반드시 구현해야 할 핵심 자동화 요소다. [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 방식의 올바른 선택, 평가 게이트를 통한 품질 보증, 재학습 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)(전체/증분)의 비용 최적화가 성공적인 CT 구현의 3대 축이다.

📢 **섹션 요약 비유**: CT는 스마트홈의 자동 온도 조절 시스템과 같다. [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 온도(기준 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/))에서 벗어나면 자동으로 감지하고, 에어컨이나 히터(재학습 파이프라인)를 켜서 다시 적정 온도(모델 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/))로 돌아오게 만든다. 사람이 일일이 조작할 필요가 없다.

---

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | [MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/) | CT는 [MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/) [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD의 세 번째 축 |
| [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) | [데이터 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/) ([Data Drift](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/)) | 입력 분포 변화가 CT 발동 조건 |
| [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) | [컨셉 드리프트](/knowledge-base/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/) ([Concept Drift](/knowledge-base/studynote/14_data_engineering/04_mlops/164_concept_drift_target_mapping_change/)) | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 변화로 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하 → CT 발동 |
| 구성요소 | [피처 스토어](/knowledge-base/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/) ([Feature Store](/knowledge-base/studynote/14_data_engineering/04_mlops/165_feature_store_training_serving_consistency/)) | 재학습 시 최신 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 제공 |
| 구성요소 | [모델 레지스트리](/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/) ([Model Registry](/knowledge-base/studynote/14_data_engineering/04_mlops/166_model_registry_versioning_mlflow/)) | CT 결과 모델 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 등록 |
| 도구 | [Kubeflow](/knowledge-base/studynote/14_data_engineering/04_mlops/167_kubeflow_kubernetes_ml_pipeline/) Pipelines | CT 파이프라인 [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) |
| 도구 | [Apache Airflow](/knowledge-base/studynote/14_data_engineering/04_mlops/168_airflow_dag_pipeline_scheduling/) | CT [스케줄](/knowledge-base/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/) 기반 [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) |
| 배포 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 롤아웃 | CT 완료 후 점진적 배포 |
| 문제 | Catastrophic Forgetting | 증분 학습의 핵심 위험 |

---

### 👶 어린이를 위한 3줄 비유 설명

1. CT는 식물을 자동으로 돌보는 로봇과 같아요. 흙이 마르면([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변화) 자동으로 물을 주고(재학습), 잎이 노래지면([성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하) 비료를 주는 것처럼 자동으로 관리해요.
2. 학교 성적이 떨어지면([성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)) 자동으로 과외 선생님이 배정되는(CT 파이프라인) 시스템처럼, CT는 모델이 약해지면 자동으로 다시 공부시켜요.
3. 게임 캐릭터가 새 구역에 가면 자동으로 레벨업 퀘스트가 생기는 것처럼, CT는 새 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 쌓이면 자동으로 모델 업그레이드 파이프라인을 실행해요.

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">수동 모델 재학습 (분기별 배치)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">CT 트리거 도입</div>
<div class="kb-diagram-tree-item" style="--depth:2">일정 기반 (cron) — 주기적 재학습</div>
<div class="kb-diagram-tree-item" style="--depth:2">데이터 기반 — 드리프트 감지 시 발동</div>
<div class="kb-diagram-tree-item" style="--depth:2">성능 기반 — 정확도 임계값 하락 시 발동</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">자동 재학습 파이프라인 (Kubeflow · Airflow)</div>
<div class="kb-diagram-tree-item" style="--depth:2">데이터 검증 → 피처 추출 → 학습</div>
<div class="kb-diagram-tree-item" style="--depth:2">평가 게이트 (성능 · SLA · 공정성)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">자동 배포 (카나리 → A/B → 전체)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">지속 모니터링 → 드리프트 재감지 → CT 재발동 (순환)</div>
</div>
</div>



---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 162 / 258

← **이전**: [161. MLOps (Machine Learning Operations) - AI 모델 개발~서빙 CI/CD 자동화](/knowledge-base/studynote/14_data_engineering/04_mlops/161_mlops_machine_learning_operations/)
**다음**: [163. 데이터 드리프트 (Data Drift) - 운영 데이터 통계 분포 이격](/knowledge-base/studynote/14_data_engineering/04_mlops/163_data_drift_statistical_distribution_shift/) →

---
