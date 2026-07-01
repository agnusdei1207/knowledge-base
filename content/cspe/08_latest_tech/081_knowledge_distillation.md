---
title: "지식증류 (Knowledge Distillation)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 81
---

# 📖 【암기용】 개념 완전 이해

> 목적: 지식증류를 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 큰 teacher model의 출력·확률분포·추론 과정을 작은 student model이 학습하도록 하는 모델 압축 기법
- **왜 필요한가**: 대형 모델은 정확하지만 비용이 크고, 작은 모델은 배포가 쉽지만 지식과 추론력이 부족함.
- **핵심 직관**: 전문가가 정답뿐 아니라 풀이 감각까지 학생에게 전수해 작은 모델이 비슷한 판단을 하게 만드는 방식임.

## 깊이 이해
- **배경·문제의식**: 라벨만 학습하면 student는 정답 1개만 배움. teacher의 soft label은 오답 후보 간 상대 확률까지 포함해 더 풍부한 학습 신호를 제공함.
- **작동 원리**: teacher가 입력에 대해 logits, soft label, rationale, intermediate feature를 생성하고 student가 이를 모방함. LLM에서는 teacher 답변·CoT·선호 데이터를 생성해 SLM을 학습함.
- **비유**: 시험 정답지만 주는 것이 아니라, 선생님의 풀이 과정과 헷갈리는 선택지의 이유까지 배우는 것과 같음.
- **구체 예시**: 70B teacher 응답 10K~100K건으로 7B student를 instruction tuning하면 도메인 QA 비용을 크게 줄일 수 있음.
- **흔한 오해·주의점**: teacher 오류도 student에 전파됨. 생성 데이터 품질 필터링과 holdout 평가셋이 필요함.

## 연결 개념
- SLM — distillation의 주요 결과물
- Model Compression — distillation의 상위 개념
- RLAIF — AI feedback 기반 선호 데이터 생성

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Knowledge Distillation은 teacher의 지식·확률분포·추론 경로를 student에 이전하는 압축 학습 기법임.
> 2. **가치**: 대형 모델 수준의 도메인 능력을 더 작은 모델에 이전해 지연·비용·메모리를 줄임.
> 3. **판단 포인트**: teacher 품질, distillation data, loss 설계, 오류 전파, student 평가가 핵심임.

## Ⅰ. 개요 및 필요성

지식증류는 teacher-student 기반 모델 압축 기법임. 대형 LLM의 비용·지연 한계를 완화하기 위해 teacher의 출력 분포와 추론 패턴을 작은 student model에 이전함.

## Ⅱ. 구조 및 구성요소

```text
Input Data -> Teacher Model -> Soft Label/Rationale/Feature
       -> Student Training -> Compact Model -> Evaluation
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Teacher Model | 고품질 출력 생성 | LLM, ensemble |
| Distill Data | soft label·rationale | 품질 필터링 필요 |
| Student Model | 작은 배포 모델 | 1B~13B |
| Distillation Loss | teacher 모방 학습 | KL, CE, feature loss |

> 요약: teacher가 풍부한 학습 신호를 만들고 student가 이를 모방해 작은 모델의 성능을 끌어올림.

## Ⅲ. 동작원리 및 흐름도

```text
데이터 수집 -> teacher 추론 -> 응답 필터링
    -> student 학습 -> holdout 평가 -> 배포
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 도메인 입력 데이터 수집 | 중복·PII 제거 |
| 2 | teacher로 label/rationale 생성 | 자동·수동 품질 점수 |
| 3 | student SFT/KL 학습 | validation loss |
| 4 | 독립 평가셋 검증 | F1, MMLU, 환각률 |

> 요약: 증류는 teacher 출력 생성보다 데이터 필터링과 독립 평가가 품질을 좌우함.

## Ⅳ. 특징

| 구분 | 직접 SFT | Knowledge Distillation | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 학습 신호 | 정답 라벨 | soft label·rationale | 정보량 증가 |
| 비용 | 라벨링 비용 큼 | teacher 호출 비용 | 10K~100K 샘플 |
| 결과 모델 | 도메인 특화 | teacher 행동 모방 | 오류 전파 위험 |
| 적용 | 데이터 충분 시 | teacher 품질 높을 때 | holdout 필수 |

> 요약: 지식증류는 작은 모델의 도메인 능력 확보에 유리하지만 teacher 오류와 데이터 편향을 통제해야 함.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 고객지원 FAQ 50K건을 teacher LLM으로 증류해 7B SLM을 학습하고 F1 0.85 이상 기준으로 배포
2. teacher 응답은 PII 제거, 중복 제거, self-consistency 점수 0.8 이상만 학습 데이터로 채택
3. student 실패 케이스는 대형 LLM fallback과 active learning 루프로 재증류

**결론 (2줄):**
- 기술사 판단: 반복 도메인 업무와 비용 절감 목표는 distillation, 범용 고난도 추론은 teacher LLM 직접 호출을 선택함.
- 향후 방향: 지식증류는 reasoning model 능력을 SLM·온디바이스 모델로 이전하는 핵심 기법이 됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | teacher->student 학습 흐름 | SFT 대비 특징 |
| 요구사항 명시형 | 구축 방안을 제시하시오 | 데이터 생성·필터링·평가 절차 | 비용·오류 전파·fallback 기준 |

> 요약: 설명형은 teacher-student 원리, 구축형은 데이터 품질과 독립 평가 중심으로 목차를 전환함.
