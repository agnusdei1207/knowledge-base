---
title: "Human Evaluation 사람 평가 (Human Evaluation)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 230
extra:
  question_no: "230"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- Human Evaluation은 자동 지표로 포착하기 어려운 품질과 선호와 안전성을 사람이 직접 평가하는 방식임
- 생성형 AI와 검색 품질과 추천 설명력처럼 정성 요소가 큰 영역에서 특히 중요함
- 평가 기준표와 샘플링 설계와 평가자 일관성 관리가 핵심 품질 조건임

## Ⅰ. 개요

- **정의/개념**: Human Evaluation은 사람이 모델 출력이나 추천 결과를 직접 검토해 정확성, 유용성, 안전성, 선호도 같은 정성적 품질을 평가하고 모델 개선과 배포 판단에 반영하는 방법임
- **배경/필요성**: 생성형 AI와 랭킹 시스템은 자동 지표만으로는 문맥 적절성과 응답 품질과 정책 위반 가능성을 충분히 측정하기 어려워 인간 판단이 필수 보완 수단이 됨

## Ⅱ. 특징

- 자동 평가가 놓치는 뉘앙스와 유용성과 정책 적합성을 확인할 수 있음
- 비용과 시간이 많이 들고 평가자 간 편차가 존재함
- 대표 샘플링과 명확한 평가 기준이 없으면 결과 신뢰성이 떨어짐
- 자동 평가와 온라인 평가를 보완하는 정성 검증 단계로 활용됨

## Ⅲ. 종류 및 비교

| 판단 기준 | Human Evaluation | Offline Automatic Evaluation | Online Evaluation |
|:---|:---|:---|:---|
| 평가 주체 | 사람 평가자 | 지표 계산 엔진 | 실제 사용자 행동 |
| 강점 | 정성 품질과 선호 파악 | 빠르고 재현 가능 | 비즈니스 효과 직접 측정 |
| 한계 | 비용과 주관성 | 맥락 이해 한계 | 실험 위험 존재 |
| 적합 영역 | 생성형 AI, 검색, 요약 | 분류와 회귀 기초 비교 | 최종 운영 검증 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Evaluation Rubric | 정확성, 유용성, 안전성, 선호도 같은 평가 항목과 점수 기준을 명확히 정의하는 표준 규칙임 |
| Sampling Strategy | 어떤 입력과 세그먼트와 실패 케이스를 평가할지 정해 대표성과 효율을 맞추는 설계 계층임 |
| Reviewer Pool | 도메인 전문가와 일반 평가자를 조합해 필요한 판단 품질과 규모를 확보하는 인력 계층임 |
| Adjudication Workflow | 평가자 간 불일치 사례를 재검토해 최종 판정을 내리는 조정 절차임 |
| Feedback Integration | 평가 결과를 프롬프트 개선과 모델 재학습과 정책 보완으로 연결하는 개선 계층임 |

```text
+-------------+    +----------------+    +----------------+    +----------------+
| Sample Set  | -> | Rubric/Reviewer| -> | Adjudication   | -> | Feedback Loop  |
+-------------+    +----------------+    +----------------+    +----------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 샘플 선정    | -> | 기준표 적용  | -> | 사람 평가    | -> | 불일치 조정  | -> | 개선 반영    |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **샘플 선정**: 대표 입력과 고위험 케이스를 고름
2. **기준표 적용**: 평가 항목과 점수 기준을 교육하고 배포함
3. **사람 평가 수행**: 평가자가 결과를 검토하고 점수를 부여함
4. **불일치 조정**: 편차 큰 항목을 재검토해 합의를 만든다
5. **개선 반영**: 결과를 프롬프트와 모델과 정책 개선에 반영함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 평가 기준이 모호하면 평가자마다 점수 해석이 달라 결과 신뢰도가 크게 낮아질 수 있음
   - 해결방안: detailed rubric과 calibration session을 적용하고 inter rater agreement와 rubric ambiguity count로 검증함
2. 문제: 샘플링이 편향되면 실제 문제 케이스를 놓치고 잘못된 품질 결론에 도달할 수 있음
   - 해결방안: stratified sampling과 failure case oversampling을 적용하고 sample representativeness score와 critical case coverage로 검증함
3. 문제: 사람 평가 비용과 시간이 크면 릴리스 속도가 느려지고 평가 빈도가 급감할 수 있음
   - 해결방안: risk based sampling과 automatic prefiltering을 적용하고 evaluation cycle time과 cost per reviewed sample로 검증함

## Ⅶ. 적용 사례

- 요약 서비스가 평가 기준표와 교정 세션을 운영하며 확인 지표는 inter rater agreement와 rubric ambiguity count임
- 고객상담 LLM이 실패 사례 중심 샘플링을 수행하며 확인 지표는 sample representativeness score와 critical case coverage임
- 검색 품질 조직이 자동 사전 필터와 사람 평가를 결합하며 확인 지표는 evaluation cycle time과 cost per reviewed sample임

## Ⅷ. 결론

Human Evaluation은 정성 품질 판단의 최종 보루이므로 명확한 기준표와 대표 샘플과 일관성 관리 없이는 신뢰할 수 없는 평가가 됨.
