---
title: "LLM04 Data and Model Poisoning (LLM04 Data and Model Poisoning)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 200
extra:
  question_no: "200"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- LLM04는 학습 데이터와 임베딩 데이터와 모델 가중치의 무결성 훼손을 다루는 OWASP 위험 항목임
- 데이터 오염과 모델 오염과 백도어 삽입이 모두 포함되는 상위 개념으로 이해해야 함
- RAG 인제스천과 RLHF와 외부 체크포인트 반입이 주요 진입 경로임

## Ⅰ. 개요

- **정의/개념**: LLM04 Data and Model Poisoning은 사전학습과 파인튜닝과 RLHF와 RAG 임베딩 과정에서 데이터나 모델 가중치가 악의적으로 변조되어 편향과 허위 지식과 백도어를 주입하는 OWASP 위험 항목임
- **배경/필요성**: 생성형 AI는 대규모 외부 데이터와 체크포인트와 사용자 피드백에 의존하므로, 훈련과 지식 주입 경로의 무결성을 관리하지 않으면 모델 자체가 잘못된 행동을 학습할 수 있음

## Ⅱ. 특징

- 전체 성능 저하뿐 아니라 특정 상황에서만 발동하는 stealth형 오염을 포함함
- 데이터셋과 임베딩 문서와 모델 가중치가 모두 공격 대상임
- 문제가 학습된 뒤에는 영향 범위 분리가 어려워 복구 비용이 큼
- 공급망 관리와 데이터 검증과 레드팀형 검증이 함께 필요함

## Ⅲ. 종류 및 비교

| 판단 기준 | Data Poisoning | Model Poisoning | RAG Poisoning |
|:---|:---|:---|:---|
| 주입 대상 | 학습 샘플과 라벨 | 체크포인트와 가중치 | 검색 문서와 임베딩 데이터 |
| 대표 결과 | 편향, 성능 저하 | 백도어, 안전 정책 약화 | 허위 근거와 답변 오염 |
| 탐지 시점 | 학습 전후 | 반입 시와 런타임 | ingestion과 retrieval 시 |
| 주요 방어 | provenance, outlier check | signed registry, scan | ingestion approval, retrieval filter |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Data, Model Source | 외부 데이터셋과 체크포인트와 피드백 채널이 오염 유입의 원천이 됨 |
| Ingestion, Validation Gate | 출처와 이상 패턴과 라이선스와 트리거 징후를 검사해 오염 자산을 격리함 |
| Training, Fine-tuning Loop | 오염 데이터와 모델이 실제 가중치 업데이트와 정렬 과정에 영향을 주는 계층임 |
| Retrieval, Embedding Store | RAG 문서 오염이 추론 시점마다 반복 재주입되는 지식 경로임 |
| Monitoring, Unlearning, Rollback | 오염 발견 후 영향 범위를 추적하고 재학습과 언러닝과 롤백을 수행함 |

```text
+-------------------+      +-------------------+      +-------------------+
| Data / Model Src  | ---> | Validate / Ingest | ---> | Train / Fine-tune |
+-------------------+      +-------------------+      +-------------------+
                                                           |
                                                           v
                                                   +-------------------+
                                                   | Retrieve / Monitor|
                                                   +-------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 오염 자산 유입    | --> | 검증 우회/통과    | --> | 지식/가중치 왜곡 | --> | 배포 후 이상 응답  |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **오염 자산 유입**: 공격자가 데이터와 모델과 문서 경로에 개입함
2. **검증 우회 또는 통과**: 부실한 검사로 오염 자산이 파이프라인에 들어감
3. **지식과 가중치 왜곡**: 학습 또는 임베딩 과정에서 악성 규칙이 내재화됨
4. **배포 후 이상 응답**: 편향과 환각과 백도어 동작이 운영에서 나타남

## Ⅵ. 문제점 및 해결 방안

1. 문제: 대규모 외부 데이터와 사용자 피드백을 신뢰하고 바로 학습이나 임베딩에 반영하면 오염 데이터가 모델 지식으로 빠르게 굳어질 수 있음
   - 해결방안: staged ingestion과 provenance scoring을 적용하고 trusted data ratio와 poisoned sample detection rate로 검증함
2. 문제: 오픈소스 체크포인트를 검증 없이 사용하면 weight-level backdoor나 안전 정책 약화가 그대로 서비스에 반영될 수 있음
   - 해결방안: checkpoint scan과 signed registry를 적용하고 backdoor detection rate와 approved checkpoint coverage로 검증함
3. 문제: RAG 문서 오염은 모델 재학습 없이도 즉시 응답 품질을 왜곡할 수 있어 운영 단계에서 반복 피해를 만들 수 있음
   - 해결방안: ingestion approval과 retrieval filtering을 적용하고 poisoned retrieval rate와 answer integrity score로 검증함

## Ⅶ. 적용 사례

- 기업 내부 RAG가 승인된 문서만 임베딩하도록 운영되며 확인 지표는 poisoned retrieval rate와 grounded answer score임
- 파인튜닝 파이프라인이 외부 체크포인트 스캔과 데이터 provenance를 결합해 운영되며 확인 지표는 approved checkpoint coverage와 backdoor detection rate임
- RLHF 기반 챗봇이 피드백 오염을 막기 위해 배치 검수형 학습을 적용하며 확인 지표는 suspicious feedback rate와 post-train regression score임

## Ⅷ. 결론

LLM04는 생성형 AI의 판단 근거 자체를 훼손하는 무결성 위험이므로 데이터와 모델과 임베딩 자산 전부에 대한 검증 게이트가 필요함.
