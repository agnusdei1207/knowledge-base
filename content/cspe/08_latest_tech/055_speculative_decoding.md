---
title: "Speculative Decoding (추측 디코딩)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 55
extra:
  question_no: "055"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- Draft Model은 빠르게 초안 토큰을 생성하는 소형 모델 또는 보조 헤드임
- Target Model은 최종 품질 기준이 되는 본 모델로 초안을 검증하고 승인함
- Acceptance Rate는 초안 토큰 중 실제로 타겟 모델이 그대로 채택한 비율임

## Ⅰ. 개요

- **정의/개념**: Speculative Decoding은 빠른 draft 모델이 다음 토큰들을 미리 생성하고 느린 target 모델이 이를 병렬 검증해 여러 토큰을 한 번에 승인함으로써 생성 품질을 유지한 채 추론 속도를 높이는 디코딩 최적화 기법임
- **배경/필요성**: 자기회귀 LLM은 토큰을 하나씩 순차 생성해야 하므로 GPU 병렬성이 충분히 활용되지 못해 응답 지연이 커지므로, 품질 저하 없이 생성 경로를 앞당기는 서빙 최적화가 필요함

## Ⅱ. 특징

- 모델 자체를 바꾸지 않고 디코딩 전략만 조정해 tokens/sec를 높일 수 있음
- draft가 잘 맞을수록 여러 토큰을 한 번에 승인해 latency 개선 효과가 큼
- acceptance rate가 낮으면 오히려 추가 검증 비용 때문에 이점이 줄 수 있음
- Medusa, self-speculative decoding 같은 파생 구조로 확장되고 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | 표준 자기회귀 생성 | Speculative Decoding | Self-Speculative / Medusa |
|:---|:---|:---|:---|
| 생성 단위 | 1토큰씩 | 다수 토큰 초안 후 승인 | 보조 헤드 기반 다수 토큰 예측 |
| 추가 모델 필요 | 없음 | 보통 필요 | 별도 모델 없이 가능 |
| 품질 | 기준선 | 이론상 유지 가능 | 구현에 따라 차이 |
| 적합 환경 | 단순 서빙 | memory-bound 서빙 가속 | 고도화 추론 엔진 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Draft Generator | 작은 모델이나 보조 헤드가 앞으로 나올 여러 토큰 초안을 빠르게 생성함 |
| Target Verifier | 큰 모델이 초안 토큰을 병렬로 검증해 승인 가능한 구간을 결정함 |
| Acceptance Controller | 승인된 토큰 길이와 반려 시 fallback 지점을 계산해 생성 흐름을 이어감 |
| Serving Router | 현재 부하와 batch 상태에 따라 speculative mode를 켜거나 끄는 운영 제어 계층임 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 초안 생성    | --> | 병렬 검증    | --> | 승인/반려    | --> | 다음 구간 반복 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **초안 생성**: draft 모델이 다음에 나올 여러 토큰을 빠르게 예측함
2. **병렬 검증**: target 모델이 초안 구간 전체를 한 번에 평가해 적합성을 판단함
3. **승인 및 반려**: 일치하는 토큰은 여러 개를 한 번에 채택하고 어긋난 지점부터는 fallback함
4. **반복 수행**: 남은 구간에 대해 같은 절차를 반복해 전체 문장을 생성함

## Ⅵ. 문제점 및 해결 방안

1. 문제: draft 모델의 품질이 낮아 acceptance rate가 떨어지면 검증과 fallback 오버헤드만 늘고 속도 이점이 사라질 수 있음
   - 해결방안: target과 근접한 draft 모델을 짝지어 선택하고 acceptance rate와 tokens/sec로 적합성을 검증함
2. 문제: 별도 draft 모델을 올리면 GPU 메모리 사용량이 증가해 특정 환경에서는 오히려 서빙 효율이 나빠질 수 있음
   - 해결방안: Medusa나 self-speculative 구조를 검토하고 VRAM 사용량과 latency 개선폭으로 운영 효율을 검증함
3. 문제: 대형 배치나 compute-bound 환경에서는 병렬 검증 이득이 작아 speculative decoding이 실제 처리량 향상으로 이어지지 않을 수 있음
   - 해결방안: 부하 기반 동적 활성화 정책을 적용하고 batch size별 throughput과 p95 latency로 적용 구간을 검증함

## Ⅶ. 적용 사례

- 엔터프라이즈 LLM 서빙: interactive chat의 응답 속도를 높임, 확인 지표는 TTFT와 tokens/sec임
- 코드 생성 보조: 문법적으로 예측 가능한 토큰 구간을 빠르게 승인함, 확인 지표는 acceptance rate와 latency임
- 오픈소스 추론 엔진: vLLM류 백엔드 가속 옵션으로 사용함, 확인 지표는 GPU utilization과 throughput임

## Ⅷ. 결론

Speculative Decoding의 가치는 초안 모델을 붙이는 데 있지 않고 acceptance rate가 높은 구간을 병렬 승인해 품질 손상 없이 지연 시간을 줄이는 서빙 최적화 전략을 만드는 데 있음.
