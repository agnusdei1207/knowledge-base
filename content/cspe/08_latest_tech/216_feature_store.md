---
title: "Feature Store 피처 스토어 (Feature Store)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 216
extra:
  question_no: "216"
  exam_status: "기출"
  exam_history: "135회"
---

## 미리 알고가기

- Feature Store는 학습과 추론에 쓰는 피처를 중앙에서 정의하고 재사용하는 데이터 인프라임
- 핵심 목적은 train serve skew를 줄이고 피처 중복 개발과 품질 불일치를 없애는 데 있음
- offline store와 online store를 함께 운영하는 구조가 일반적임

## Ⅰ. 개요

- **정의/개념**: Feature Store는 머신러닝 모델이 사용하는 피처를 표준 정의와 메타데이터와 저장소 형태로 관리하여 학습과 추론 단계에서 동일한 피처를 일관되게 제공하는 플랫폼임
- **배경/필요성**: 모델이 늘어날수록 팀마다 같은 피처를 중복 구현하고 학습용 계산식과 실시간 추론용 계산식이 달라지는 문제가 커져 중앙 관리 인프라가 필요해짐

## Ⅱ. 특징

- 피처 정의를 재사용 가능한 데이터 제품으로 관리함
- 배치 학습용 offline store와 실시간 추론용 online store를 함께 가짐
- 피처 메타데이터와 계보와 신선도를 함께 관리함
- 피처 제공 일관성이 모델 품질과 운영 안정성을 직접 좌우함

## Ⅲ. 종류 및 비교

| 판단 기준 | Feature Store | Data Warehouse | Vector DB |
|:---|:---|:---|:---|
| 핵심 데이터 | 모델 입력 피처 | 분석용 테이블 | 임베딩 벡터 |
| 운영 목적 | 학습과 추론 일관성 | BI와 리포팅 | 의미 검색 |
| 실시간성 | online serving 지원 | 주로 배치 중심 | 질의 검색 중심 |
| 대표 위험 | train serve skew, stale feature | 데이터 지연 | retrieval drift |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Feature Definition Registry | 피처 이름과 계산 로직과 소유자와 품질 기준을 등록해 재사용 기준점을 만드는 카탈로그임 |
| Offline Store | 대용량 학습 데이터셋 생성을 위해 과거 시점 기준 피처 값을 저장하는 배치 저장소임 |
| Online Store | 실시간 예측 요청에 낮은 지연으로 최신 피처를 제공하는 서빙 저장소임 |
| Feature Pipeline | 원천 데이터를 가공해 offline과 online 저장소에 동일 규칙으로 반영하는 처리 경로임 |
| Serving API and Monitor | 모델이 피처를 호출할 수 있게 제공하고 신선도와 오류를 관측하는 인터페이스 계층임 |

```text
+-------------+    +-------------------+    +---------------+    +--------------+
| Source Data | -> | Feature Pipeline  | -> | Offline Store | -> | Training     |
+-------------+    +-------------------+    +---------------+    +--------------+
                         |
                         v
                  +---------------+    +--------------+
                  | Online Store  | -> | Inference    |
                  +---------------+    +--------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 피처 정의    | -> | 피처 계산    | -> | 저장소 적재  | -> | 학습과 추론  | -> | 신선도 관측  |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **피처 정의**: 모델이 쓸 변수와 계산 규칙을 표준화함
2. **피처 계산**: 원천 데이터로부터 동일 로직으로 피처를 산출함
3. **저장소 적재**: offline과 online 저장소에 목적별로 반영함
4. **학습과 추론 사용**: 학습과 실시간 예측이 같은 피처 정의를 사용함
5. **신선도 관측**: 지연과 누락과 스큐를 지속 모니터링함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 학습용 피처 계산식과 운영 서빙 계산식이 분리되면 같은 모델도 운영에서 다른 입력을 받아 성능이 흔들릴 수 있음
   - 해결방안: single source feature definition과 shared feature pipeline을 적용하고 train serve skew rate와 offline online parity score로 검증함
2. 문제: 실시간 저장소 갱신이 지연되면 stale feature가 예측에 사용되어 정확도와 의사결정 품질이 저하될 수 있음
   - 해결방안: freshness SLA와 update lag monitoring을 적용하고 feature freshness lag와 stale feature usage rate로 검증함
3. 문제: 피처 소유자와 메타데이터가 없으면 중복 개발과 잘못된 재사용이 반복될 수 있음
   - 해결방안: feature catalog와 ownership policy를 적용하고 duplicate feature ratio와 undocumented feature count로 검증함

## Ⅶ. 적용 사례

- 추천 시스템이 offline과 online 피처 저장소를 분리 운영하며 확인 지표는 offline online parity score와 feature freshness lag임
- 사기 탐지 모델이 중앙 피처 카탈로그를 사용하며 확인 지표는 duplicate feature ratio와 stale feature usage rate임
- 대출 심사 플랫폼이 피처 소유자와 품질 기준을 등록하며 확인 지표는 undocumented feature count와 train serve skew rate임

## Ⅷ. 결론

Feature Store는 모델 입력을 데이터 제품으로 표준화하는 인프라이므로 피처 재사용성과 일관성과 신선도 통제를 동시에 만족시켜야 함.
