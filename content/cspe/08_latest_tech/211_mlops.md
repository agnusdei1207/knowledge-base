---
title: "MLOps (Machine Learning Operations)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 211
extra:
  question_no: "211"
  exam_status: "기출"
  exam_history: "135회, 137회"
---

## 미리 알고가기

- MLOps는 모델을 한 번 학습시키는 일보다 데이터와 코드와 모델을 지속적으로 운영하는 체계를 다룸
- DevOps에 지속적 학습과 데이터 계보와 모델 성능 모니터링을 추가한 형태로 이해하면 됨
- 재현성 확보와 배포 자동화와 드리프트 대응이 핵심 성숙도 지표임

## Ⅰ. 개요

- **정의/개념**: MLOps는 머신러닝 시스템의 데이터 수집과 학습과 검증과 배포와 모니터링과 재학습을 자동화하고 코드와 데이터와 모델의 생애주기를 통합 관리하는 운영 체계임
- **배경/필요성**: 노트북에서 만든 모델이 운영 환경에서 재현되지 않거나 데이터 변화로 빠르게 성능이 저하되는 문제가 반복되면서 ML 전용 파이프라인과 거버넌스가 필수 인프라가 됨

## Ⅱ. 특징

- 코드뿐 아니라 데이터와 모델 버전까지 함께 관리해야 함
- CI와 CD에 더해 CT와 모니터링 루프가 중요함
- 모델 배포 이후 성능 저하와 데이터 표류를 추적해야 운영 품질을 유지할 수 있음
- 팀 간 역할 분리보다 공통 파이프라인과 표준화가 더 중요해짐

## Ⅲ. 종류 및 비교

| 판단 기준 | MLOps | DevOps | LLMOps |
|:---|:---|:---|:---|
| 핵심 자산 | 코드, 데이터, 모델 | 코드와 인프라 | 프롬프트, RAG, 모델 API |
| 운영 루프 | 학습, 배포, 모니터링, 재학습 | 빌드, 테스트, 배포 | 평가, 가드레일, 비용 통제 |
| 주요 리스크 | drift, train serve skew | 배포 실패, 장애 | hallucination, token cost |
| 대표 지표 | reproducibility, retrain lead time | deployment frequency | answer quality, cost per request |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Data and Feature Pipeline | 원천 데이터를 정제하고 학습과 추론에 일관된 입력을 공급해 데이터 품질과 재현성을 확보하는 흐름임 |
| Training Pipeline | 코드와 하이퍼파라미터와 데이터 버전을 고정해 반복 가능한 학습과 평가를 수행하는 자동화 경로임 |
| Model Registry | 검증을 통과한 모델을 버전과 상태와 메타데이터와 함께 보관해 승격과 롤백을 관리하는 저장소임 |
| Deployment Orchestrator | 승인된 모델을 배치와 온라인 서빙 환경에 배포하며 카나리와 섀도 같은 전략을 적용하는 배포 계층임 |
| Monitoring and Retraining Loop | 운영 성능과 드리프트를 감시하고 임계치 초과 시 재학습을 트리거하는 폐루프 운영 계층임 |

```text
+----------+    +-----------+    +---------------+    +--------------+    +-------------+
| Data     | -> | Training  | -> | Model Registry| -> | Deployment   | -> | Monitoring  |
+----------+    +-----------+    +---------------+    +--------------+    +-------------+
                                                                                 |
                                                                                 v
                                                                           +-------------+
                                                                           | Retraining  |
                                                                           +-------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 데이터 준비  | -> | 모델 학습    | -> | 성능 검증    | -> | 배포 승격    | -> | 운영 관측    |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **데이터 준비**: 입력 데이터와 피처 정의와 스키마를 정리함
2. **모델 학습**: 버전 고정된 코드와 데이터로 모델을 학습함
3. **성능 검증**: 오프라인 평가와 기준 충족 여부를 판정함
4. **배포 승격**: 승인된 모델만 운영 환경으로 배포함
5. **운영 관측**: 지연과 성능과 드리프트를 보고 재학습 필요 여부를 판단함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 데이터와 코드와 모델 버전이 분리되면 동일 조건 재현이 어려워 운영 장애와 감사 대응 비용이 커질 수 있음
   - 해결방안: end to end lineage와 artifact version control을 적용하고 reproducibility rate와 lineage completeness score로 검증함
2. 문제: 운영 데이터 변화가 감지되지 않으면 정확도 저하가 장기간 누적되어 비즈니스 손실이 커질 수 있음
   - 해결방안: drift monitoring과 retraining trigger policy를 적용하고 drift detection lead time과 post drift recovery time으로 검증함
3. 문제: 수동 배포와 승인 절차는 모델 교체 시간을 늘리고 롤백 실패 가능성을 높일 수 있음
   - 해결방안: automated promotion gate와 canary deployment를 적용하고 deployment lead time과 rollback success rate로 검증함

## Ⅶ. 적용 사례

- 금융 예측 시스템이 모델 등록과 승격 기준을 자동화하며 확인 지표는 deployment lead time과 rollback success rate임
- 제조 불량 탐지 파이프라인이 데이터 표류 감지 후 재학습을 연계하며 확인 지표는 drift detection lead time과 post drift recovery time임
- 추천 시스템이 데이터와 모델 계보를 추적하며 확인 지표는 reproducibility rate와 lineage completeness score임

## Ⅷ. 결론

MLOps는 모델 개발보다 운영의 불확실성을 줄이는 체계이므로 재현성과 자동화와 관측성을 함께 갖춘 전주기 설계가 핵심임.
