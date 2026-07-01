---
title: "지시 튜닝 (Instruction Tuning)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 87
---

# 📖 【암기용】 개념 완전 이해

> 목적: Instruction Tuning을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 모델이 자연어 지시를 이해하고 원하는 형식으로 응답하도록 지시-응답 데이터로 추가 학습하는 기법
- **왜 필요한가**: 사전학습 모델은 다음 토큰 예측에는 강하지만, “요약하라”, “표로 정리하라” 같은 명령 수행 능력은 별도 학습이 필요함.
- **핵심 직관**: 책을 많이 읽은 사람에게 업무 지시를 받았을 때 어떤 산출물을 내야 하는지 훈련하는 과정임.

## 깊이 이해
- **배경·문제의식**: Pretrained LM은 지식은 많지만 사용자의 의도와 출력 포맷을 안정적으로 따르지 못함. Instruction Tuning은 다양한 task instruction과 답변 예시를 학습해 범용 지시 수행 능력을 만든다.
- **작동 원리**: 지시문, 입력 맥락, 기대 출력으로 구성된 데이터셋을 SFT로 학습함. 여러 태스크를 섞어 학습하면 unseen task에도 zero-shot 수행력이 향상됨.
- **비유**: 박식한 인턴에게 “회의록 요약”, “위험 표 작성”, “고객 답변 작성” 훈련을 반복시키는 것과 같음.
- **구체 예시**: Alpaca류 데이터는 teacher LLM으로 생성한 instruction-response 쌍을 사용해 작은 모델의 지시 수행 능력을 높임.
- **흔한 오해·주의점**: Instruction Tuning은 선호 정렬과 다름. 유해성·선호도 조정은 RLHF/DPO 같은 alignment 단계가 추가로 필요함.

## 연결 개념
- Fine-Tuning — Instruction Tuning의 상위 학습 절차
- RLHF/DPO — 선호 정렬 단계
- Synthetic Data — 지시 데이터 생성 방법

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Instruction Tuning은 지시-응답 데이터로 모델의 명령 이해와 출력 형식 준수 능력을 학습시키는 SFT 기법임.
> 2. **가치**: 다양한 업무 지시를 zero-shot/few-shot으로 수행하게 하여 범용 AI assistant 기반을 형성함.
> 3. **판단 포인트**: instruction 다양성, 출력 품질, 포맷 일관성, safety alignment 분리 여부가 핵심임.

## Ⅰ. 개요 및 필요성

Instruction Tuning은 지시 수행 능력 학습 기법임. 사전학습 모델이 사용자 명령과 출력 형식을 안정적으로 따르도록, 다양한 지시-응답 예시로 supervised fine-tuning을 수행함.

## Ⅱ. 구조 및 구성요소

```text
Instruction Dataset -> SFT Training -> Instruction-tuned Model
      -> Task Evaluation -> Alignment/RLHF 단계
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Instruction | 사용자의 명령 문장 | task 다양성 필요 |
| Input Context | 문제·문서·대화 맥락 | 선택 입력 |
| Response | 기대 출력 | 형식·품질 검증 |
| Evaluation | 지시 수행 평가 | 형식 준수율, 정확도 |

> 요약: Instruction Tuning은 명령·맥락·응답 쌍을 학습해 모델이 다양한 사용자 지시를 따르게 함.

## Ⅲ. 동작원리 및 흐름도

```text
지시 데이터 수집 -> 품질 필터링 -> SFT 학습
    -> 지시 수행 평가 -> 안전 정렬 단계 연결
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | task별 instruction-response 수집 | task coverage |
| 2 | 중복·저품질·PII 제거 | 품질 점수 |
| 3 | SFT로 응답 패턴 학습 | validation loss |
| 4 | unseen task 평가 | exact match, format pass |

> 요약: Instruction Tuning은 데이터 다양성과 출력 품질 관리가 zero-shot 지시 수행력의 핵심임.

## Ⅳ. 특징

| 구분 | Pretraining | Instruction Tuning | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 목표 | 다음 토큰 예측 | 사용자 지시 수행 | assistant화 |
| 데이터 | 대규모 비지도 텍스트 | 지시-응답 쌍 | 10K~1M 샘플 |
| 효과 | 언어·지식 형성 | 형식·업무 수행 | format pass rate |
| 한계 | 지시 불안정 | 선호·안전 별도 필요 | RLHF/DPO 연계 |

> 요약: Instruction Tuning은 모델을 사용자 명령 수행형으로 바꾸지만, 안전성과 선호 정렬은 별도 단계가 필요함.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 사내 assistant는 요약·분류·검색 질의·보고서 작성 instruction 10K건 이상으로 SFT 수행
2. JSON·표·서술형 출력은 schema validator로 형식 준수율 95% 이상을 배포 기준으로 설정
3. 지시 튜닝 후 유해 응답·개인정보·정책 위반은 RLHF/DPO 또는 guardrail 단계로 보정

**결론 (2줄):**
- 기술사 판단: 모델이 지시를 못 따르면 Instruction Tuning, 답변 선호·안전성 문제는 Alignment 기법을 선택함.
- 향후 방향: 지시 데이터는 synthetic data와 human review를 결합해 도메인별 assistant 품질을 좌우함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | 지시 데이터->SFT->평가 흐름 | Pretraining 대비 차이 |
| 요구사항 명시형 | 구축 방안을 제시하시오 | 데이터 품질·형식 검증 절차 | alignment와 역할 분리 |

> 요약: 설명형은 지시 수행 학습 원리, 구축형은 instruction data 품질과 형식 평가 중심으로 목차를 전환함.
