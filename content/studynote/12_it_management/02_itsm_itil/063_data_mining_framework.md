---
title: 63. 데이터 마이닝 프레임워크 (Data Mining Framework)
date: '2026-04-05'
tags:
- studynote-it-management
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[284_data_mining_association_classification_clustering_crisp_dm|데이터 마이닝]] 프레임워크([[284_data_mining_association_classification_clustering_crisp_dm|Data Mining]] Framework)는 [[001_dikw_pyramid|데이터]]를 모으고, 탐색하고, 모델링하고, 평가하고, 배포하는 전체 과정을 묶는 절차적 틀이다.
> 2. **가치**: [[001_algorithm_definition|알고리즘]] 하나보다 프레임워크가 중요한 이유는, 비즈니스 목표와 품질 [[395_verification_process_review|검증]]이 빠지면 좋은 모델도 실패하기 때문이다.
> 3. **판단**: [[225_kdd_t_test_anova_statistical_analysis|KDD]], CRISP-DM, SEMMA 같은 프레임워크를 이해하면 [[001_dikw_pyramid|데이터]] 프로젝트를 분석가가 아니라 조직 프로세스로 볼 수 있다.

---

## Ⅰ. 개요 및 필요성

[[284_data_mining_association_classification_clustering_crisp_dm|데이터 마이닝]]은 "좋은 모델을 찾는 일"로만 보이기 쉽지만, 실제로는 문제 정의부터 결과 활용까지 이어지는 긴 흐름이다. 그래서 프레임워크가 없으면 모델은 있어도 프로젝트는 실패한다.

프레임워크는 분석의 순서를 잡아 주고, 누가 무엇을 언제 확인해야 하는지 알려준다. 즉 기술보다 운영과 협업을 정리하는 도구다.

- **📢 섹션 요약 비유**: 퍼즐을 맞출 때 그림 설명서가 없으면 부품은 많아도 완성하기 어렵다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Business Understanding
  ↓
Data Understanding
  ↓
Data Preparation
  ↓
Modeling
  ↓
Evaluation
  ↓
Deployment
```

| 프레임워크 | 핵심 단계 | 특징 |
| :-- | :-- | :-- |
| [[225_kdd_t_test_anova_statistical_analysis|KDD]] | [[022_mcts_four_stages|Selection]] → Preprocessing → Transformation → [[284_data_mining_association_classification_clustering_crisp_dm|Data Mining]] → Interpretation | 학술적 전통이 강함 |
| CRISP-DM | Business → [[001_dikw_pyramid|Data]] → [[654_ir_preparation|Preparation]] → Modeling → Evaluation → [[087_deployment_kubernetes_workload_rolling_update|Deployment]] | 산업 표준에 가까움 |
| SEMMA | Sample → Explore → Modify → Model → Assess | SAS 중심 흐름 |

[[284_data_mining_association_classification_clustering_crisp_dm|데이터 마이닝]] 프레임워크는 [[001_algorithm_definition|알고리즘]]이 아니라 "일하는 순서"다. 좋은 순서가 있어야 [[001_dikw_pyramid|데이터]] 품질, [[395_verification_process_review|검증]], 배포가 빠지지 않는다.

- **📢 섹션 요약 비유**: 집을 지을 때 설계, 자재, 시공, 검사가 순서대로 있어야 무너지지 않는다.

---

## Ⅲ. 비교 및 연결

| 구분 | [[284_data_mining_association_classification_clustering_crisp_dm|데이터 마이닝]] | [[241_machine_learning_basics|머신러닝]] | [[001_dikw_pyramid|데이터]] 분석 |
| :-- | :-- | :-- | :-- |
| 초점 | 패턴 발견 | 예측 [[282_performance_tactics|성능]] | 인사이트 |
| 결과물 | 규칙, [[104_classification_analysis|분류]], 군집 | 모델 | 보고서 |
| 중요 포인트 | 절차와 [[395_verification_process_review|검증]] | 일반화 | 해석 |

| 프레임워크 | 장점 | 주의점 |
| :-- | :-- | :-- |
| [[225_kdd_t_test_anova_statistical_analysis|KDD]] | 연구에 강함 | 단계가 추상적일 수 있음 |
| CRISP-DM | 실무 친화적 | 조직 적용이 필요 |
| SEMMA | 도구 친화적 | 범용성은 낮음 |

프레임워크의 차이는 이름보다도 적용 맥락에 있다. 학술 연구는 [[225_kdd_t_test_anova_statistical_analysis|KDD]], 기업 프로젝트는 CRISP-DM, SAS 환경은 SEMMA가 잘 맞는다.

- **📢 섹션 요약 비유**: 같은 여행이라도 지도, 네비게이션, 관광 안내서가 서로 다른 도움을 준다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. 비즈니스 문제를 먼저 정의했는가?
2. [[001_dikw_pyramid|데이터]] 품질과 결측치를 검토했는가?
3. 모델 [[282_performance_tactics|성능]]뿐 아니라 해석 가능성을 봤는가?
4. [[395_verification_process_review|검증]] 결과를 실제 운영에 연결했는가?
5. 재학습과 모니터링 계획이 있는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- [[001_algorithm_definition|알고리즘]]만 고르고 문제 정의를 뒤로 미루는 설계
- 평가 없이 모델만 반복 훈련하는 설계
- 배포 후 모니터링이 없는 설계
- 팀마다 다른 기준으로 분석하는 설계

기술사 관점에서는 [[284_data_mining_association_classification_clustering_crisp_dm|데이터 마이닝]] 프레임워크를 "분석 절차"가 아니라 "조직의 학습 루프"로 봐야 한다. 그래야 결과물이 한 번의 보고서로 끝나지 않는다.

- **📢 섹션 요약 비유**: 학교 숙제도 문제를 읽고, 풀고, 확인하고, 다시 보는 순서가 있어야 실수가 줄어든다.

---

## Ⅴ. 기대효과 및 결론

프레임워크를 쓰면 모델 하나의 [[282_performance_tactics|성능]]보다 프로젝트 전체의 성공 확률이 높아진다. 무엇보다 [[001_dikw_pyramid|데이터]] 프로젝트가 "운"이 아니라 "절차"로 움직이게 된다.

결국 [[284_data_mining_association_classification_clustering_crisp_dm|데이터 마이닝]]은 모델링이 아니라 관리된 탐색이다.

- **📢 섹션 요약 비유**: 길을 잘 찾는 사람은 지도만 보는 게 아니라 출발점과 도착점을 함께 본다.

---

## 관련 개념 맵

```text
Business Problem
  ↓
Data Mining Framework
  ↓
Modeling / Evaluation
  ↓
Deployment / Monitoring
```

---

## 관련 키워드 및 발전 흐름도

```text
KDD
  ↓
CRISP-DM
  ↓
SEMMA
  ↓
DataOps / MLOps
```

---

## 어린이를 위한 3줄 비유 설명

퍼즐을 맞추려면 설명서가 필요해요.  
[[284_data_mining_association_classification_clustering_crisp_dm|데이터 마이닝]]도 순서를 정해 놓아야 잘 돼요.  
프레임워크는 그 순서를 알려 주는 설명서예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 109 / 587

← **이전**: [[062_itil|62. ITIL (IT Infrastructure Library)]]
**다음**: [[063_itil_v3_service_lifecycle|63. ITIL V3 의 서비스 수명주기 (Service Lifecycle) 5단계]] →

---
