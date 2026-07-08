---
title: "Data Poisoning 데이터 오염 (Data Poisoning)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 192
extra:
  question_no: "192"
  exam_status: "기출"
  exam_history: "137회"
  exam_note: "전망"
---

## 미리 알고가기

- 데이터 오염은 학습 단계에서 잘못된 샘플과 라벨을 주입해 모델 판단 자체를 왜곡하는 공격임
- 적대적 예제가 추론 시점 공격이라면 데이터 오염은 학습 시점 공격이라는 점이 핵심 차이임
- 오픈 데이터와 RLHF와 RAG 수집 경로가 넓어질수록 공격 표면이 커짐

## Ⅰ. 개요

- **정의/개념**: 데이터 오염은 공격자가 훈련 데이터나 피드백 데이터에 조작된 샘플과 잘못된 라벨과 편향된 정보를 주입해 모델의 결정 경계와 안전 특성을 훼손하는 공격임
- **배경/필요성**: 대규모 AI는 외부 데이터셋과 크라우드 라벨링과 사용자 피드백에 의존하는 경우가 많아, 데이터 무결성을 검증하지 않으면 모델 품질과 윤리 기준이 근본적으로 오염될 수 있음

## Ⅱ. 특징

- 모델이 학습하는 지식 기반 자체를 바꾸므로 배포 후 복구 비용이 큼
- 전체 정확도를 낮추는 untargeted 공격과 특정 행위만 유도하는 targeted 공격이 모두 가능함
- 온라인 학습과 RLHF와 RAG 문서 수집은 오염 주입 경로가 되기 쉬움
- 사후에 문제를 발견해도 오염 데이터 영향만 선택적으로 제거하기가 매우 어렵다

## Ⅲ. 종류 및 비교

| 판단 기준 | Availability Poisoning | Integrity Poisoning | Backdoor Poisoning |
|:---|:---|:---|:---|
| 목표 | 전체 성능 저하 | 특정 오분류 유도 | 트리거 기반 숨은 동작 |
| 징후 | 정확도 전반 하락 | 일부 목표만 실패 | 평소 정상, 특정 조건만 발동 |
| 탐지 난도 | 상대적으로 낮음 | 중간 | 높음 |
| 대표 방어 | outlier 제거 | data provenance | backdoor scan, provenance |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Data Source, Collector | 외부 크롤링과 사용자 피드백과 라벨링 경로처럼 오염이 유입되는 원천 계층임 |
| Poisoned Sample, Label | 잘못된 내용이나 라벨과 편향된 텍스트가 모델 학습 방향을 비정상적으로 끌어당김 |
| Training Pipeline | 오염 데이터를 검증 없이 통과시키면 가중치에 잘못된 규칙이 각인됨 |
| Validation, Provenance Gate | 이상치와 출처와 라벨 일관성을 확인해 오염 샘플을 걸러내는 통제 지점임 |
| Monitoring, Unlearning Plan | 학습 후 성능 변화와 이상 행동을 감시하고 필요 시 재학습과 언러닝 전략을 준비함 |

```text
+-------------------+      +-------------------+      +-------------------+
| Data Source       | ---> | Poisoned Samples  | ---> | Training Pipeline |
+-------------------+      +-------------------+      +-------------------+
                                                           |
                                                           v
                                                   +-------------------+
                                                   | Validation Gate   |
                                                   +-------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 오염 샘플 주입   | --> | 학습 데이터 혼합  | --> | 왜곡된 규칙 학습 | --> | 배포 후 오동작  |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **오염 샘플 주입**: 공격자가 데이터나 피드백 채널에 조작된 샘플을 넣음
2. **학습 데이터 혼합**: 파이프라인이 이를 정상 데이터와 함께 사용함
3. **왜곡된 규칙 학습**: 모델이 잘못된 상관관계와 라벨을 내재화함
4. **배포 후 오동작**: 정확도 저하나 특정 편향과 숨은 오류가 나타남

## Ⅵ. 문제점 및 해결 방안

1. 문제: 출처와 라벨 검증 없이 외부 데이터와 사용자 피드백을 바로 학습에 반영하면 조작된 샘플이 자연스럽게 모델 지식에 스며들 수 있음
   - 해결방안: provenance tracking과 quarantine review를 적용하고 trusted data ratio와 suspicious sample detection rate로 검증함
2. 문제: targeted poisoning은 전체 정확도는 유지한 채 특정 조건만 오염시켜 일반 검증셋으로는 발견하기 어려울 수 있음
   - 해결방안: targeted scenario evaluation과 slice-based testing을 적용하고 trigger condition error rate와 hidden bias score로 검증함
3. 문제: 오염을 뒤늦게 발견하면 이미 학습된 모델에서 영향 범위를 분리하기 어려워 재학습 비용이 커질 수 있음
   - 해결방안: dataset versioning과 unlearning plan을 준비하고 rollback lead time과 retraining cost ratio로 검증함

## Ⅶ. 적용 사례

- 전자상거래 추천 모델이 리뷰 조작과 피드백 오염을 차단하도록 배치 학습으로 전환되며 확인 지표는 suspicious feedback rate와 recommendation stability임
- 기업 RAG 시스템이 문서 인제스천 전 승인 게이트를 두고 운영되며 확인 지표는 poisoned document detection rate와 answer integrity score임
- RLHF 기반 챗봇이 보상 데이터 검수를 강화해 운영되며 확인 지표는 harmful preference sample rate와 post-train regression score임

## Ⅷ. 결론

데이터 오염은 모델의 행동을 사후에 고치는 문제가 아니라 학습 입력의 무결성을 지키는 문제이므로 데이터 계보와 검증 게이트가 방어의 중심이 되어야 함.
