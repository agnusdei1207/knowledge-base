---
title: "Model Serving 모델 서빙 (Model Serving)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 225
extra:
  question_no: "225"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- Model Serving은 학습된 모델을 실제 서비스 요청에 응답하도록 배포하고 운영하는 추론 제공 계층임
- 성능만이 아니라 버전 일관성과 지연 시간과 리소스 효율이 핵심 판단 기준임
- Feature Store와 Model Registry와 Observability가 함께 붙어야 운영 품질이 안정됨

## Ⅰ. 개요

- **정의/개념**: Model Serving은 학습된 모델을 API나 배치나 스트리밍 형태로 운영 환경에 배포하여 예측 요청을 처리하고 결과를 안정적으로 제공하는 추론 서비스 체계임
- **배경/필요성**: 모델 정확도가 높아도 운영 환경에서 응답 지연과 버전 불일치와 확장성 문제가 생기면 실제 비즈니스 가치로 이어지지 않아 서빙 아키텍처가 필수 인프라가 됨

## Ⅱ. 특징

- 온라인 서빙과 배치 추론과 스트리밍 추론 등 사용 패턴에 따라 구조가 달라짐
- 모델 버전과 피처 버전 일관성이 운영 품질을 좌우함
- 지연 시간과 처리량과 비용 효율 간 균형이 중요함
- 관측성과 자동 확장과 롤백 체계가 함께 필요함

## Ⅲ. 종류 및 비교

| 판단 기준 | Online Serving | Batch Inference | Stream Inference |
|:---|:---|:---|:---|
| 응답 방식 | 요청 즉시 예측 | 대량 일괄 처리 | 이벤트 흐름 기반 |
| 핵심 지표 | latency, availability | throughput, completion time | lag, consistency |
| 대표 용도 | 추천, 사기 탐지 | 리포트, 캠페인 스코어링 | 이상 탐지, IoT |
| 설계 포인트 | autoscaling, cache | scheduler, artifact sync | exactly once, windowing |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Model Runtime | 모델 로딩과 추론 수행을 담당하며 프레임워크 호환성과 성능 최적화의 핵심이 되는 실행 엔진임 |
| Request Gateway | 인증과 라우팅과 버전 선택과 속도 제한을 처리해 요청을 적절한 서빙 인스턴스로 보내는 관문임 |
| Feature Fetcher | 온라인 추론 시 필요한 최신 피처를 가져와 모델 입력과 서빙 환경의 일관성을 유지하는 계층임 |
| Autoscaling and Resource Manager | CPU와 GPU 사용량과 요청 부하에 따라 인스턴스를 조절해 비용과 성능을 균형화하는 운영 계층임 |
| Observability and Rollback | 지연과 오류와 품질 지표를 수집하고 장애 시 이전 버전으로 복귀하게 하는 관측 및 복구 계층임 |

```text
+-------------+    +----------------+    +----------------+    +------------------+
| User Request| -> | Gateway        | -> | Feature Fetcher| -> | Model Runtime    |
+-------------+    +----------------+    +----------------+    +------------------+
                                                                          |
                                                                          v
                                                                   +--------------+
                                                                   | Monitor/RB   |
                                                                   +--------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 요청 수신    | -> | 버전 선택    | -> | 피처 조회    | -> | 추론 수행    | -> | 결과 반환 및 관측 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **요청 수신**: API나 이벤트로 예측 요청을 받음
2. **버전 선택**: 운영 정책에 따라 서빙 모델 버전을 결정함
3. **피처 조회**: 최신 입력 피처를 조회하고 검증함
4. **추론 수행**: 런타임이 모델을 실행해 예측값을 생성함
5. **결과 반환 및 관측**: 응답을 반환하고 지연과 오류와 품질을 기록함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 서빙 모델 버전과 피처 버전이 맞지 않으면 정확도 저하와 예측 오류가 즉시 발생할 수 있음
   - 해결방안: version locked serving contract를 적용하고 model feature compatibility rate와 prediction error due to schema mismatch로 검증함
2. 문제: 부하 증가 시 자동 확장이 늦거나 비효율적이면 지연 시간과 운영 비용이 동시에 악화될 수 있음
   - 해결방안: autoscaling policy tuning과 runtime optimization을 적용하고 p99 latency와 cost per inference로 검증함
3. 문제: 장애 시 롤백 체계가 없으면 잘못 배포된 모델이 장시간 운영에 남을 수 있음
   - 해결방안: health check based rollback과 staged deployment를 적용하고 rollback execution time과 failed deployment containment rate로 검증함

## Ⅶ. 적용 사례

- 추천 API가 피처 버전 잠금과 온라인 서빙 계약을 운영하며 확인 지표는 model feature compatibility rate와 prediction error due to schema mismatch임
- 실시간 사기 탐지 서비스가 자동 확장 정책을 최적화하며 확인 지표는 p99 latency와 cost per inference임
- 금융 스코어링 엔진이 상태 기반 롤백을 적용하며 확인 지표는 rollback execution time과 failed deployment containment rate임

## Ⅷ. 결론

Model Serving은 모델을 서비스 가치로 전환하는 마지막 관문이므로 버전 일관성과 지연 통제와 롤백 가능성을 핵심 설계 원칙으로 삼아야 함.
