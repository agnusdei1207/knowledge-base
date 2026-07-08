---
title: "Model Registry 모델 레지스트리 (Model Registry)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 217
extra:
  question_no: "217"
  exam_status: "기출"
  exam_history: "135회"
---

## 미리 알고가기

- Model Registry는 학습된 모델 아티팩트를 버전과 상태와 메타데이터와 함께 관리하는 저장소임
- 단순 파일 보관소가 아니라 승인과 승격과 롤백의 기준점을 제공한다는 점이 핵심임
- 실험 추적과 서빙 배포와 연결될 때 운영 가치가 커짐

## Ⅰ. 개요

- **정의/개념**: Model Registry는 학습된 모델 파일과 메타데이터와 평가 결과와 배포 상태를 통합 관리하여 어떤 모델이 어떤 기준으로 운영에 승격되었는지 추적하게 하는 모델 생애주기 저장소임
- **배경/필요성**: 모델 버전이 많아질수록 파일명과 폴더 수준 관리로는 승인 이력과 성능 차이와 롤백 대상을 명확히 구분하기 어려워 중앙 등록 체계가 필요해짐

## Ⅱ. 특징

- 모델 버전과 상태를 Staging과 Production 같은 단계로 구분해 관리함
- 학습 데이터와 코드와 평가 지표를 모델 아티팩트와 연결해 계보를 확보함
- 배포 자동화와 결합하면 승격 기준과 롤백 절차를 단순화할 수 있음
- 운영 승인 절차와 보안 검증을 내장할수록 통제 수준이 높아짐

## Ⅲ. 종류 및 비교

| 판단 기준 | Model Registry | Artifact Repository | Experiment Tracking |
|:---|:---|:---|:---|
| 핵심 대상 | 승인 대상 모델 버전 | 일반 바이너리와 패키지 | 실험 실행 기록 |
| 주요 기능 | stage 관리, 승격, 롤백 | 파일 저장 | params, metrics 비교 |
| 계보 수준 | 데이터와 코드와 배포 연결 | 제한적 | 실험 중심 |
| 운영 역할 | deployment gate | 보관소 | 연구 기록 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Model Artifact | 가중치와 직렬화 파일과 추론 서명을 포함한 실제 배포 대상 모델 패키지임 |
| Metadata and Metrics | 버전과 학습 데이터와 평가 결과와 소유자 정보를 저장해 비교와 승인 판단 근거를 제공함 |
| Stage Management | 개발과 검증과 운영 상태를 나눠 모델 승격과 롤백을 관리하는 생애주기 계층임 |
| Approval and Policy Gate | 성능과 보안과 규정 기준을 통과한 모델만 상위 단계로 이동시키는 통제 장치임 |
| Deployment Link | 레지스트리 상태 변화가 실제 서빙 배포와 연결되도록 오케스트레이터와 연동하는 접점임 |

```text
+-------------+    +-------------------+    +----------------+    +----------------+
| Train Output| -> | Registry Metadata | -> | Stage/Approval | -> | Deployment Link|
+-------------+    +-------------------+    +----------------+    +----------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 모델 저장    | -> | 메타 등록    | -> | 승인 심사    | -> | 단계 승격    | -> | 배포 및 롤백 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **모델 저장**: 학습 완료 모델 아티팩트를 레지스트리에 업로드함
2. **메타 등록**: 성능 지표와 데이터 버전과 코드 커밋을 함께 기록함
3. **승인 심사**: 배포 기준과 보안과 규정 검사를 수행함
4. **단계 승격**: 합격한 모델을 운영 후보나 운영 상태로 전환함
5. **배포 및 롤백**: 운영 연결 시스템이 상태 변화에 맞춰 배포하거나 이전 버전으로 복귀함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 평가 지표와 데이터 버전이 연결되지 않으면 어떤 모델이 왜 운영에 올라갔는지 추적하기 어려워질 수 있음
   - 해결방안: mandatory lineage metadata와 evaluation snapshot을 적용하고 lineage completeness score와 approval traceability rate로 검증함
2. 문제: 단계 승격 절차가 수동이면 잘못된 모델이 운영에 반영되거나 롤백 시간이 길어질 수 있음
   - 해결방안: automated promotion gate와 deployment integration을 적용하고 promotion lead time과 rollback time으로 검증함
3. 문제: 레지스트리 없이 모델 파일만 관리하면 중복 버전과 고아 모델이 누적되어 운영 복잡도가 커질 수 있음
   - 해결방안: central registry policy와 retention policy를 적용하고 duplicate artifact ratio와 orphan model count로 검증함

## Ⅶ. 적용 사례

- 추천 모델 파이프라인이 레지스트리 단계 승격 후 자동 배포를 연계하며 확인 지표는 promotion lead time과 rollback time임
- 금융 예측 모델이 평가 스냅샷과 데이터 버전을 필수 등록하며 확인 지표는 approval traceability rate와 lineage completeness score임
- 제조 AI 플랫폼이 중앙 레지스트리로 모델 자산을 정리하며 확인 지표는 duplicate artifact ratio와 orphan model count임

## Ⅷ. 결론

Model Registry는 모델 파일 보관소가 아니라 운영 승격의 기준점이므로 메타데이터와 승인 절차와 배포 연계를 함께 갖춰야 함.
