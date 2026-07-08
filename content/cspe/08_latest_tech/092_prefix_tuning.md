---
title: "Prefix Tuning (프리픽스 튜닝)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 92
extra:
  question_no: "092"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- prefix tuning은 실제 단어 대신 학습 가능한 가상 prefix 벡터를 각 레이어 attention에 주입하는 PEFT 방식임
- base model 가중치는 고정되고 prefix 파라미터만 학습됨
- task-specific steering에는 유용하지만 복잡한 도메인 적응에서는 한계가 있을 수 있음

## Ⅰ. 개요

- **정의/개념**: prefix tuning은 입력 앞에 가상의 연속 벡터 prefix를 붙여 attention 동작을 조절하고, 이 prefix 파라미터만 학습해 모델을 특정 업무에 적응시키는 PEFT 기법임
- **배경/필요성**: 전체 모델을 수정하지 않고 적은 파라미터로 생성 방향을 제어하려는 요구가 커지면서, 입력 조건을 학습 가능한 형태로 바꾸는 경량 튜닝 방식이 필요함

## Ⅱ. 특징

- 학습 대상이 매우 적어 비용과 저장 공간이 작음
- 입력 수준의 제어보다 더 강하게, full fine-tuning보다 훨씬 가볍게 생성 경향을 바꿀 수 있음
- prefix 길이와 삽입 위치가 부적절하면 표현력이 부족하거나 오히려 컨텍스트 자원을 낭비할 수 있음
- 긴 문맥 추론이나 복합 도메인 적응에서는 LoRA보다 성능이 약할 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Prompt Tuning | Prefix Tuning | LoRA |
|:---|:---|:---|:---|
| 조정 위치 | 입력 임베딩 | attention prefix | 선형 계층 |
| 학습 파라미터 | 매우 적음 | 매우 적음 | 적음 |
| 제어 강도 | 낮음 | 중간 | 높음 |
| 대표 활용 | 간단 태스크 | 생성 방향 제어 | 도메인 적응 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Virtual Prefix Tokens | 실제 텍스트 대신 학습 가능한 벡터로 attention의 조건을 형성함 |
| Prefix Projection | 작은 파라미터를 각 레이어가 사용하는 key, value 형태로 투영함 |
| Frozen Transformer | 기반 모델은 고정되어 prefix가 유도하는 방향만 반영함 |
| Task Data | 특정 출력 스타일이나 태스크 목적을 prefix에 학습시키는 입력 예시를 제공함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 가상 prefix 초기화 | --> | attention prefix 주입 | --> | prefix만 학습   | --> | 업무별 prefix 배포 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **가상 prefix 초기화**: 학습 가능한 연속 벡터를 준비함
2. **attention prefix 주입**: 각 레이어 attention에 prefix 정보를 추가함
3. **prefix만 학습**: base model은 고정하고 prefix 파라미터만 업데이트함
4. **업무별 prefix 배포**: 태스크별 prefix를 선택해 추론 시 적용함

## Ⅵ. 문제점 및 해결 방안

1. 문제: prefix 길이가 너무 짧으면 충분한 업무 정보를 담지 못해 적응 효과가 약해질 수 있음
   - 해결방안: prefix length를 실험적으로 조정하고 parameter count 대비 task score로 적절한 크기를 검증함
2. 문제: 지나치게 긴 prefix는 컨텍스트 자원을 소모하고 추론 비용을 늘려 실시간 서비스에 불리할 수 있음
   - 해결방안: latency budget 안에서 prefix 길이를 제한하고 context overhead와 p95 latency로 효율을 검증함
3. 문제: 복잡한 도메인 규칙까지 prefix만으로 반영하려 하면 성능 한계가 빠르게 드러날 수 있음
   - 해결방안: 단순 steering 용도로 한정하거나 LoRA와 비교 평가하고 validation score와 generalization rate로 적용 범위를 검증함

## Ⅶ. 적용 사례

- 응답 스타일 제어: 간결 답변, 표 형식 답변 같은 패턴을 학습함, 확인 지표는 format pass rate와 edit rate임
- 다국어 보조 태스크: 번역 방향과 톤을 조정함, 확인 지표는 BLEU류 점수와 latency임
- 경량 실험 환경: 다양한 태스크를 빠르게 비교함, 확인 지표는 training time과 storage size임

## Ⅷ. 결론

prefix tuning은 극소수 파라미터로 생성 방향을 바꾸는 데 적합한 PEFT 방식이므로, 복잡한 도메인 적응보다는 스타일 제어와 경량 실험에 더 어울림.
