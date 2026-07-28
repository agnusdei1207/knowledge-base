---
sidebar:
  order: 48
  label: "048. LLM Serving (LLM 서빙)"
  badge:
    text: "미출제 · 70%"
    variant: note
title: "LLM Serving (LLM 서빙)"
date: "2026-07-25T01:25:00+09:00"
tags:
  - "notes-latest_tech"
weight: 48
extra:
  question_no: "048"
  source_status: "미출제"
  source_history: ""
  priority: 70
  priority_note: "지연·처리량·비용을 통합 설계하는 주제"
---

## 미리 알고가기

- **LLM 서빙 (Large Language Model Serving)**: 동시 요청의 추론과 자원을 조정하는 운영 계층
- **텐서 병렬화 (Tensor Parallelism)**: 레이어 가중치를 여러 GPU에 분할하여 병렬 연산하는 기법
- **추론 엔진 (Inference Engine)**: 가속 알고리즘이 탑재된 서빙 핵심 구동 코어
- **SLA (Service Level Agreement)**: 응답 속도 및 가동률 품질 보증 합의


## Ⅰ. 개요

- 정의/개념: 모델 추론을 동시 요청에 제공하는 체계
- **배경/필요성**: 메모리·지연·비용·품질 통합 관리

### 쉽게 이해하기 (학습용)
- 모델을 다수 사용자가 안정적으로 쓰도록 접수·배정·계산·감시함

## Ⅱ. 특징

- 스트리밍·배치·가변 길이 요청을 지원한다
- 프리필·디코드 자원 차이에 맞춰 스케줄링한다
- 텐서·파이프라인 병렬화가 부하를 분산한다
- 격리·관측·회귀 검증이 서비스 품질을 지킨다

### 쉽게 이해하기 (학습용)

- 여러 요청을 묶고 나누는 방식이 지연과 처리량을 함께 바꾼다

## Ⅲ. 구성요소 및 구조

| 구성 요소 | 설명 |
|:---|:---|
| API Gateway | 인증, 할당량, 스트리밍 처리 |
| Model Router | 모델 및 인스턴스 선택 |
| Scheduler | 배치 및 캐시 메모리 관리 |
| Engine | 양자화 및 병렬 추론 실행 |
| Control Plane | 배포, 스케일링, 모니터링 수행 |

```text
[ Control Plane ]
  Model Registry·Release Policy·Router Config·Autoscaler·Evaluation·Telemetry
                                |
[ Serving Data Plane ]
  Client -> API Gateway -> Model Router -> Replica Group -> Stream
                                             |
                              [ Worker Replica ]
  Queue·Scheduler <-> KV Manager <-> Distributed Model Executor -> Sampler
                                |
[ Trust·Operations Boundary ]
  IAM·Quota·Tenant Isolation·Safety Gate·Secret·Audit·Fallback
```

### 쉽게 이해하기 (학습용)

- 요청을 검증해 적절한 모델 작업자에게 배정하고 생성 결과를 실시간으로 돌려줌

## Ⅳ. 원리 및 절차 흐름도

```text
요구정의
↓
구성설계
↓
품질검증
↓
배포운영
```

| 절차 | 설명 |
|:---|:---|
| 요구정의 | 모델·SLO·보안·비용 목표 수립함 |
| 구성설계 | 양자화·병렬화·배치 전략 설계함 |
| 품질검증 | 부하 테스트 및 장애 회귀 검증함 |
| 배포운영 | 카나리 배포 및 관측 체계 구축함 |

### 쉽게 이해하기 (학습용)

- 평균 검증만 통과하지 말고 피크 부하와 GPU 장애에서도 서비스 약속을 지키는지 확인함

## Ⅴ. 종류 및 비교

| 판단 기준 | 오프라인 추론 | 온라인 서빙 |
|:---|:---|:---|
| 입력 처리 | 고정 데이터·대량 배치 | 실시간·가변 길이 스트리밍 |
| 최적화 목표 | 총 시간 및 비용 효율 | 반응성 및 처리량 관리 |
| 운영 통제 | 작업 단위 재실행 | 스케일링·격리·무중단 |

> 요약: 일괄 처리와 실시간 서빙의 목표를 구분함

### 쉽게 이해하기 (학습용)

- 서빙 방식은 빠른 응답과 높은 서버 효율 사이를 조절한다

## Ⅵ. 실무 사례

- 모델 라우팅 시 비용과 품질, 권한 등을 통합 검증함

### 쉽게 이해하기 (학습용)

- 모델 품질이 같아도 배치·캐시 운영에 따라 서비스 속도는 달라진다

## Ⅶ. 결론

- LLM을 안정적인 온라인 서비스로 제공하기 위해 **모델 적재·요청 스케줄링·동적 배치·분산 추론·관측 및 장애 복구**를 검토하고, 목표 TTFT·TPOT·처리량에 맞는 서빙 구조를 설계해야 한다.
- 실제 품질·Goodput·비용으로 지속적인 검증이 필요함

### 쉽게 이해하기 (학습용)

- 좋은 서빙은 답의 품질과 속도·비용을 함께 유지한다
