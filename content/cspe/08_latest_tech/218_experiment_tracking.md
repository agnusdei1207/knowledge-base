---
title: "Experiment Tracking 실험 추적 (Experiment Tracking)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 218
---

# 📖 【암기용】 개념 완전 이해

> 목적: Experiment Tracking을 ML/AI 실험의 조건과 결과를 기록해 재현성과 비교 가능성을 확보하는 체계로 이해하게 만든다.

## 한눈에
- **개요**: 실험별 코드, 데이터, 파라미터, 모델, 지표, 산출물을 기록·비교하는 관리 체계
- **왜 필요한가**: 모델 성능은 데이터 split, hyperparameter, feature, code version에 따라 달라지므로 기록이 없으면 같은 결과를 다시 만들 수 없다.
- **핵심 직관**: Experiment Tracking은 실험실 연구노트이며 어떤 조건에서 어떤 점수가 나왔는지 남기는 증거임.

## 깊이 이해
- **배경·문제의식**: 노트북 파일명과 수동 메모만으로는 best model의 학습 조건, 데이터 버전, 평가 지표를 추적하기 어렵다.
- **작동 원리**: run ID마다 parameter, metric, artifact, dataset version, code SHA, tag를 저장하고 dashboard에서 비교함.
- **비유**: 요리 대회에서 재료 양, 조리 시간, 온도, 심사 점수, 완성 사진을 모두 기록해 우승 레시피를 재현하는 방식임.
- **구체 예시**: 추천 모델 실험에서 learning_rate 0.001, embedding_dim 128, train data v12, NDCG@10 0.421을 run ID로 저장함.
- **흔한 오해·주의점**: Experiment Tracking은 단순 로그 저장이 아니라 모델 선택 근거와 registry 승격 근거를 제공하는 품질 기록임.

## 연결 개념
- Model Registry — 실험에서 선택된 모델을 운영 후보로 등록
- Hyperparameter Optimization — 실험 조건 탐색과 결과 비교
- MLOps — 실험부터 배포까지 재현 가능한 파이프라인 구성

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Experiment Tracking은 ML/AI 실험의 입력 조건과 결과 지표를 run 단위로 기록·비교하는 체계임.
> 2. **가치**: 재현성, 모델 선택 근거, 성능 회귀 분석, 감사 추적성을 확보함.
> 3. **판단 포인트**: parameter와 metric만이 아니라 dataset version, code SHA, artifact, environment를 함께 기록해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| ML 실험 관리 이해 확인 | run, parameter, metric, artifact, dataset version | 단순 로그 저장으로 설명 |
| 재현성 확보 판단 확인 | code SHA, environment, seed, data split | best score만 기록 |
| MLOps 연결 구조 확인 | tracking -> registry -> deployment 흐름 | 운영 배포와의 연결 누락 |

> 요약: Experiment Tracking 문제는 실험 결과 비교와 운영 모델 선택 근거를 재현 가능하게 남기는 구조를 묻는 문제임.

---

## Ⅰ. 개요 및 필요성

- 개요: ML 실험 기록 체계
- 배경: 수동 실험 기록은 best model의 데이터, 코드, 파라미터, 환경 정보를 누락해 재현성을 훼손함.
- 필요성: 실험 메타데이터 100%, 재현 성공률 95% 이상, 모델 선택 근거 100% 기록 기준이 필요함.

---

## Ⅱ. 구조 및 구성요소

```text
Training Code -> Experiment Run -> Tracking Server
Tracking Server -> Metric Dashboard -> Model Selection
Model Selection -> Model Registry
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Run ID | 실험 단위 식별자 | parameter·metric 연결 키 |
| Parameter Log | hyperparameter와 실행 설정 기록 | learning rate, batch size |
| Metric Log | 학습·검증·테스트 지표 저장 | AUC, F1, RMSE |
| Artifact Store | 모델 파일, 그래프, 결과 파일 보관 | confusion matrix |
| Metadata | dataset version, code SHA, 환경 기록 | reproducibility |

> 요약: Experiment Tracking은 run ID를 중심으로 실험 조건, 지표, 산출물, 환경 정보를 한 번에 추적함.

---

## Ⅲ. 동작원리 및 흐름도

```text
실험 설계 -> run 생성 -> parameter/metric 기록
-> artifact 저장 -> 실험 비교 -> registry 등록 후보 선정
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 실험 목적과 평가 지표를 지정 | primary metric 1개 이상 |
| 2 | run ID를 생성하고 parameter와 seed를 기록 | 필수 parameter 100% |
| 3 | 학습 중 metric과 artifact를 저장 | metric 누락 0건 |
| 4 | dashboard에서 baseline 대비 개선 여부 비교 | 개선폭 1%p 이상 |
| 5 | 선택 모델을 registry에 등록하고 근거를 연결 | registry link 100% |

> 요약: Experiment Tracking은 실험 조건과 결과를 run 단위로 저장하고 모델 선택 근거를 registry로 전달함.

---

## Ⅳ. 특징

| 구분 | 수동 실험 기록 | Experiment Tracking | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 기록 단위 | 파일명·메모 | run ID | run metadata 100% |
| 비교 방식 | 표 수동 작성 | dashboard와 query | baseline 대비 개선폭 |
| 재현성 | 기억과 노트 의존 | code·data·env 연결 | 재현 성공률 95% 이상 |
| 운영 연결 | 모델 파일 별도 전달 | registry 연계 | 선택 근거 100% |

> 요약: Experiment Tracking은 실험을 일회성 작업에서 비교 가능한 증거 데이터로 전환함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 노트북 파일과 스프레드시트 | tracking server와 artifact store | 실험 run 월 100개 이상 |
| 비용/성능 | 수동 비교 | 자동 dashboard와 query | 모델 선택 시간 1일 이하 |
| 운영/위험 | best model 근거 불명 | registry link와 metadata | 감사·재현성 요구 시 |

> 요약: Experiment Tracking은 실험 수가 많고 모델 선택 근거를 조직적으로 남겨야 할 때 필요함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 재현 실패 | dataset version과 code SHA 누락 | 필수 metadata gate 적용 | 재현 성공률 95% 이상 |
| 지표 오해 | train metric만 기록 | validation/test metric 분리 | test metric 기록률 100% |
| 저장소 비용 증가 | artifact 무제한 보관 | retention policy와 압축 | 월 저장 증가율 20% 이하 |

> 요약: 실험 추적 리스크는 메타데이터 누락, 지표 해석 오류, artifact 비용이며 필수 필드와 보관 정책으로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 기록 완전성 | parameter·metric·artifact 100% | tracking audit |
| 재현성 | 동일 run 재현 성공률 95% 이상 | 재실행 검증 |
| 모델 선택 | registry 등록 모델의 run link 100% | registry metadata 확인 |

> 요약: Experiment Tracking 성과는 기록 완전성, 재현 성공률, registry 연결률로 검증함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. MLflow 또는 Weights & Biases 기반 tracking server를 구성하고 run ID, parameter, metric, artifact, dataset version을 필수 기록으로 지정함.
2. baseline 모델 대비 primary metric 1%p 이상 개선, fairness gap 5%p 이하, latency 200ms 이하 기준을 모델 선택 조건으로 둠.
3. registry 등록 시 experiment run link를 필수화해 운영 모델의 선택 근거와 재현 경로를 100% 연결함.

**결론 (2줄):**
- 기술사 판단: 개인 탐색은 파일 기록으로 시작할 수 있으나 팀 단위 모델 개발과 운영 배포가 있으면 Experiment Tracking을 필수화함.
- 향후 방향: Experiment Tracking은 LLM prompt evaluation, automated HPO, Model Registry와 결합해 AI 개발 증거 체계로 발전함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Experiment Tracking을 설명하시오" | run 생성->지표 기록->비교 흐름 | 수동 실험 기록 대비 차이 |
| 요구사항 명시형 | "ML 재현성 확보 방안을 제시하시오" | metadata gate와 registry 연계 | code·data·env 기록 기준 |

> 요약: 설명형은 실험 기록 구조, 방안형은 재현성 확보와 운영 모델 선택 근거를 중심으로 작성함.
