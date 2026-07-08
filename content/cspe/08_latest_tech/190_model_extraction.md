---
title: "Model Extraction 모델 추출 (Model Extraction)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 190
extra:
  question_no: "190"
  exam_status: "기출"
  exam_history: "137회"
  exam_note: "전망"
---

## 미리 알고가기

- 모델 추출은 공개 API의 입출력을 대량 수집해 원본 모델 기능을 모방하는 대체 모델을 만드는 공격임
- 가중치를 직접 훔치지 않아도 예측 결과와 신뢰도 점수만으로 상당한 복제가 가능함
- 방어는 완전 차단보다 응답 정보량 축소와 이상 질의 탐지와 워터마킹 조합에 가까움

## Ⅰ. 개요

- **정의/개념**: 모델 추출은 상용 ML API나 LLM 서비스에 대량의 질의를 보내 입력과 출력 관계를 수집한 뒤, 이 데이터를 이용해 원본과 유사한 성능의 대체 모델을 학습하는 공격임
- **배경/필요성**: 공개 API는 비즈니스를 위해 열려 있지만 응답 패턴이 곧 모델 지식을 드러내는 채널이 되므로, 기업 입장에서는 핵심 지식재산과 수익 모델을 보호할 대응이 필요해짐

## Ⅱ. 특징

- 정상 API 호출처럼 보이기 때문에 전통적 침입 탐지보다 구분이 어려움
- 예측 라벨뿐 아니라 confidence score가 주어지면 모델 경계 복제가 훨씬 쉬워짐
- 복제된 대체 모델은 직접 상용화되거나 후속 적대 공격의 실험장으로 쓰일 수 있음
- 완벽한 차단보다 비용 증가와 탐지와 법적 증거 확보를 함께 설계해야 현실적임

## Ⅲ. 종류 및 비교

| 판단 기준 | Label-only Extraction | Score-based Extraction | Functionality Stealing |
|:---|:---|:---|:---|
| 수집 정보 | 최종 라벨만 | 라벨과 confidence | 전체 응답 기능과 패턴 |
| 공격 효율 | 낮음 | 높음 | 매우 높음 |
| 대표 피해 | 경계 근사 | 정밀 복제 | 서비스 대체와 경쟁모델 구축 |
| 방어 포인트 | rate limit, anomaly detect | score truncation | watermark, legal trace |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Target API | 공격 대상인 상용 모델 서비스로 입력에 대한 예측 결과를 반환함 |
| Query Generator | 경계 근처나 대표 샘플을 선택해 추출 효율을 높이는 입력 생성기임 |
| Response Collector | 라벨과 점수와 설명 정보를 수집해 대체 학습 데이터셋을 만듦 |
| Substitute Training | 수집한 입출력 쌍으로 대체 모델을 학습해 원본 기능을 근사함 |
| Detection, Watermark Layer | 이상 질의 탐지와 응답 축소와 소유권 워터마킹으로 추출을 어렵게 함 |

```text
+-------------------+      +-------------------+      +-------------------+
| Query Generator   | ---> | Target API        | ---> | Response Collector|
+-------------------+      +-------------------+      +-------------------+
                                                           |
                                                           v
                                                   +-------------------+
                                                   | Substitute Model  |
                                                   +-------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 질의 샘플 생성   | --> | API 반복 호출    | --> | 응답 데이터 축적 | --> | 대체 모델 학습  |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **질의 샘플 생성**: 공격자가 정보량이 큰 입력을 선택하거나 생성함
2. **API 반복 호출**: 원본 모델에 다수의 질의를 수행함
3. **응답 데이터 축적**: 라벨과 점수와 패턴을 학습용으로 저장함
4. **대체 모델 학습**: 원본 동작을 모방하는 모델을 구축함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 세밀한 confidence score와 풍부한 디버그 정보를 그대로 주면 공격자가 결정 경계를 빠르게 근사할 수 있음
   - 해결방안: response truncation과 score rounding을 적용하고 extraction fidelity와 user utility score로 검증함
2. 문제: 분산 계정과 저속 질의를 이용하면 단순 rate limit만으로는 추출 시도를 충분히 탐지하지 못할 수 있음
   - 해결방안: behavioral anomaly detection과 identity correlation을 적용하고 suspicious query detection rate와 false alarm rate로 검증함
3. 문제: 추출을 완전히 막기 어렵기 때문에 사후에 도용 여부를 증명할 장치가 없으면 대응 비용이 커질 수 있음
   - 해결방안: model watermarking과 ownership evidence를 적용하고 watermark verification rate와 legal traceability score로 검증함

## Ⅶ. 적용 사례

- 이미지 판독 API가 confidence score를 축약하고 운영되며 확인 지표는 extraction fidelity와 customer usefulness score임
- 금융 사기 탐지 서비스가 비정상 탐색형 질의를 탐지해 차단하며 확인 지표는 suspicious query detection rate와 attack containment time임
- 기업 생성형 AI API가 워터마크와 응답 패턴 분석으로 도용 가능성을 추적하며 확인 지표는 watermark verification rate와 model cloning incident rate임

## Ⅷ. 결론

모델 추출은 공개 API 자체를 학습 채널로 뒤집는 경제적 공격이므로 응답 최소화와 질의 행위 분석과 소유권 증거화를 함께 설계해야 방어력이 생김.
