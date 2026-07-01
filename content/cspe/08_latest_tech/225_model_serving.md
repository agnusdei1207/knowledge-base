---
title: "모델 서빙 (Model Serving)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 225
---

# 📖 【암기용】 개념 완전 이해

> 목적: 모델 서빙을 학습된 모델을 실제 서비스 요청에 연결하는 실행 계층으로 이해하게 만든다.

## 한눈에
- **개요**: 학습된 ML 모델을 API, batch, stream 형태로 배포해 예측 결과를 제공하는 운영 기술
- **왜 필요한가**: 모델 파일만으로는 사용자 요청을 처리할 수 없고, 전처리, 추론, 확장, 버전 관리, 모니터링이 함께 필요하다.
- **핵심 직관**: 모델 서빙은 완성된 요리를 손님 주문에 맞춰 정해진 시간 안에 내보내는 주방 운영과 같다.

## 깊이 이해
- **배경·문제의식**: 학습 환경의 notebook·GPU 파일은 운영 서비스의 SLA, 동시성, 보안, 버전 관리를 만족하지 못한다.
- **작동 원리**: request를 수신해 feature 전처리, 모델 로드, inference 실행, 후처리, 응답 반환, 로그 기록, scale-out을 수행한다.
- **비유**: 도서관 검색 시스템이 책 목록을 갖고 있어도 대출 창구, 검색 단말, 대기열 관리가 없으면 사용자에게 책을 제공할 수 없는 상황이다.
- **구체 예시**: 추천 모델 API는 p95 latency 100ms 이하, error rate 0.1% 이하, canary 5% 배포 기준으로 version v2를 운영에 투입한다.
- **흔한 오해·주의점**: 모델 서빙은 API 서버 배포만이 아니며, feature consistency, batching, model version, rollback, 모니터링까지 포함한다.

## 연결 개념
- Model Registry — 배포 가능한 모델 버전 관리
- Online Inference — 실시간 요청 기반 추론
- Batch Inference — 대량 데이터를 주기적으로 예측

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: 모델 서빙은 latency, throughput, version, feature consistency, rollback을 함께 설계해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Model Serving은 학습된 모델을 운영 요청에 연결해 예측 결과를 제공하는 추론 실행 계층임.
> 2. **가치**: p95 latency, throughput, error rate, model version, feature skew를 통제해 예측 서비스를 운영 SLA에 맞춤.
> 3. **판단 포인트**: online, batch, streaming serving 중 업무 지연 허용치와 비용 조건에 맞는 방식을 선택해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| ML 운영 아키텍처 이해 확인 | request, preprocessing, inference, response, monitoring | 모델 파일 배포로만 설명 |
| 서비스 품질 판단 확인 | latency, throughput, autoscaling, rollback | 정확도만 쓰고 SLA 누락 |
| 배포 전략 이해 확인 | canary, A/B, shadow, blue-green | version과 feature skew 관리 누락 |

> 요약: 이 문제는 모델을 운영 SLA 안에서 안전하게 제공하는 추론 아키텍처를 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 운영 추론 제공 계층
- 배경: 학습된 모델은 API, 전처리, scale-out, 버전 관리가 없으면 서비스 요청을 처리하지 못함.
- 필요성: p95 latency 100ms, error rate 0.1%, rollback 5분 이내 같은 SLA 기준으로 서빙 구조를 설계해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Client -> API Gateway -> Preprocess -> Model Runtime -> Postprocess -> Response
Model Registry -> Deployment Controller -> Monitoring -> Rollback
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| API Gateway | 인증, 라우팅, rate limit 처리 | REST, gRPC |
| Pre/Post Processor | feature 변환과 결과 후처리 | training-serving consistency 필요 |
| Model Runtime | 모델 로드와 inference 실행 | TensorFlow Serving, TorchServe, Triton |
| Deployment Controller | 버전 배포와 rollback 제어 | canary, shadow, blue-green |

> 요약: 모델 서빙은 요청 처리 경로와 모델 버전 배포 경로를 분리해 SLA와 rollback을 관리한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요청 수신 -> feature 생성 -> model inference -> 결과 후처리 -> 응답 반환 -> 로그·지표 기록
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | API 요청 인증과 rate limit 적용 | 429 rate 정책 |
| 2 | feature 전처리와 schema 검증 | schema mismatch 0건 |
| 3 | 모델 runtime에서 추론 실행 | p95 latency 100ms 이하 |
| 4 | 응답 반환 후 로그·metric 저장 | error rate 0.1% 이하 |

> 요약: 모델 서빙은 요청 처리와 관측 로그 기록이 함께 수행되어야 품질과 원인 추적이 가능하다.

---

## Ⅳ. 특징

| 구분 | Batch Serving | Online Serving | 수치 기준 |
|:---|:---|:---|:---|
| 처리 방식 | 대량 데이터 주기 예측 | 요청마다 실시간 예측 | p95 latency 100ms |
| 비용 구조 | 스케줄 기반 자원 사용 | 상시 자원 유지 | GPU utilization 60% 이상 |
| 적용 업무 | 일일 추천 목록, 리스크 산출 | 검색 랭킹, 실시간 사기 탐지 | freshness 1분 이하 |

> 요약: 지연 허용치가 짧으면 online serving, 대량 산출과 비용 절감이 우선이면 batch serving을 선택한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 서빙 방식 | batch inference | online / streaming inference | 업무 latency 요구 |
| 확장 전략 | 고정 인스턴스 | HPA, KEDA, GPU autoscaling | QPS 변동성과 cold start |
| 배포 전략 | 전체 교체 | canary, shadow, blue-green | 오류 허용도와 검증 데이터 |

> 요약: 모델 서빙 방식은 지연 허용치, QPS 변동, 배포 검증 수준을 기준으로 선택한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 지연 초과 | 모델 크기, cold start, 전처리 병목 | model quantization, warm pool, batching | p95 latency 100ms 이하 |
| serving skew | 학습·서빙 feature 변환 불일치 | 공통 feature transform과 schema 검증 | skew diff 1% 이하 |
| 배포 장애 | 신규 모델 오류 | canary 5%, shadow traffic, rollback 자동화 | rollback 5분 이내 |

> 요약: 서빙 리스크는 지연, feature skew, 배포 장애를 중심으로 통제해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 지연시간 | p95 100ms 이하 | APM, inference log |
| 처리량 | 목표 QPS 대비 120% capacity | load test, autoscaling metric |
| 품질 추적 | model_id별 AUC·CTR 분리 | prediction log, delayed label |

> 요약: 서빙 품질은 latency와 throughput뿐 아니라 model_id별 예측 품질까지 추적해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 아키텍처 선택: latency 100ms 이하 업무는 online serving, 1시간 이상 허용 업무는 batch serving, 이벤트 연속 처리는 streaming serving을 선택함.
2. 배포 통제: model registry 승인 모델만 canary 5%로 배포하고 error rate 0.1% 초과 또는 CTR 10% 하락 시 rollback함.
3. 성능 튜닝: CPU 모델은 thread pool과 batching을 조정하고 GPU 모델은 Triton dynamic batching과 quantization을 적용함.

**결론 (2줄):**
- 기술사 판단: Model Serving은 모델 정확도보다 SLA, feature consistency, version rollback, 모니터링을 함께 만족해야 운영 가능함.
- 향후 방향: 모델 서빙은 LLM serving, vector retrieval, edge inference, GPU autoscaling과 결합된 추론 플랫폼으로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "모델 서빙을 설명하시오" | 요청 처리와 추론 흐름 | batch와 online 차이 |
| 요구사항 명시형 | "모델 서빙 아키텍처를 설계하시오" | SLA 기준 처리 흐름 | 배포 전략과 리스크 대응 |

> 요약: 설명형은 추론 제공 구조를, 설계형은 SLA와 배포 통제 기준을 중심으로 작성한다.
