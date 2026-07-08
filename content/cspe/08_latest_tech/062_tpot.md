---
title: "TPOT 토큰당 출력 지연 (Time Per Output Token)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 62
extra:
  question_no: "062"
  exam_status: "기출"
  exam_history: "138회"
  exam_note: "전망"
---

## 미리 알고가기

- TPOT는 첫 토큰 이후 각 출력 토큰을 생성하는 평균 시간임
- Decode 단계는 KV cache를 반복 참조하며 토큰을 하나씩 생성하는 구간임
- Memory-bound는 계산보다 메모리 읽기, 쓰기가 병목인 상태를 의미함

## Ⅰ. 개요

- **정의/개념**: TPOT(Time Per Output Token)은 첫 토큰 이후 각 출력 토큰이 생성되는 데 걸리는 평균 지연 시간으로, 스트리밍 응답의 부드러움과 실시간성을 나타내는 핵심 decode 성능 지표임
- **배경/필요성**: LLM은 자기회귀적으로 토큰을 하나씩 생성하므로, KV cache 접근과 메모리 대역폭 병목이 크면 사용자 화면에 텍스트가 끊겨 보이기 때문에 토큰당 출력 지연 관리가 필요함

## Ⅱ. 특징

- TTFT와 달리 prefill보다 디코딩 메모리 병목에 더 민감함
- KV cache 크기와 메모리 대역폭과 batch 크기의 영향을 크게 받음
- 사용자는 TPOT이 높아지면 타이핑이 느리게 보이는 것처럼 체감함
- speculative decoding, cache quantization, batch tuning의 효과를 확인하는 대표 지표임

## Ⅲ. 종류 및 비교

| 판단 기준 | TTFT | TPOT | Throughput |
|:---|:---|:---|:---|
| 측정 구간 | 첫 토큰 전 | 첫 토큰 후 매 토큰 | 일정 시간 총 처리량 |
| 주요 병목 | prefill, queue | decode, memory bandwidth | 전체 스케줄링 효율 |
| 사용자 체감 | 시작 반응 속도 | 출력 부드러움 | 전체 시스템 생산성 |
| 대표 개선책 | prefix caching | speculative decoding, cache 최적화 | continuous batching |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Decode Loop | 새 토큰을 하나씩 생성하는 반복 루프로 TPOT 측정의 기본 단위임 |
| KV Cache Reader | 과거 문맥을 메모리에서 읽어오는 단계로 디코딩 병목을 형성함 |
| Token Sampler | 확률 분포에서 다음 토큰을 선택해 실제 출력 토큰을 확정함 |
| Batch Coordinator | 동시에 실행 중인 요청 수를 조절해 메모리 혼잡과 토큰 지연을 제어함 |

```text
+------------------+     +------------------+     +------------------+     +------------------+
| Decode Loop      | --> | KV Cache Reader  | --> | Token Sampler    | --> | Batch Coord.     |
+------------------+     +------------------+     +------------------+     +------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 캐시 참조    | --> | logits 계산  | --> | 토큰 샘플링  | --> | 다음 스텝 반복 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **캐시 참조**: 현재까지의 KV cache를 읽어 새 토큰 생성에 필요한 문맥을 확보함
2. **logits 계산**: 현재 상태에서 다음 토큰 확률 분포를 계산함
3. **토큰 샘플링**: 샘플링 규칙에 따라 다음 출력 토큰을 확정함
4. **다음 스텝 반복**: 새 토큰을 캐시에 추가하고 같은 과정을 반복함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 긴 컨텍스트와 큰 batch가 겹치면 KV cache 접근량이 커져 메모리 대역폭 병목으로 TPOT이 급격히 악화될 수 있음
   - 해결방안: cache quantization과 batch 상한 조정을 적용하고 batch size별 TPOT과 GPU memory bandwidth로 효과를 검증함
2. 문제: throughput만 높이려 배치를 크게 잡으면 개별 사용자 화면에는 출력이 느리게 흘러 UX가 나빠질 수 있음
   - 해결방안: QoS 정책으로 interactive request의 batch 크기를 제한하고 p95 TPOT과 user satisfaction으로 균형점을 검증함
3. 문제: speculative decoding 같은 가속 기법도 acceptance rate가 낮으면 오히려 추가 오버헤드로 TPOT 개선이 작을 수 있음
   - 해결방안: workload별 speculative 정책을 분기하고 acceptance rate와 tokens/sec와 TPOT로 적합성을 검증함

## Ⅶ. 적용 사례

- 실시간 챗봇 스트리밍: 사용자에게 끊김 없는 텍스트 출력을 제공함, 확인 지표는 TPOT과 session completion rate임
- 음성 대화형 서비스: TTS와 결합된 응답 지연을 관리함, 확인 지표는 end-to-end speech latency임
- 코드 생성 플랫폼: 긴 출력에서도 빠른 타이핑 체감을 유지함, 확인 지표는 tokens/sec와 p95 TPOT임

## Ⅷ. 결론

TPOT은 단순한 속도 수치가 아니라 디코딩 메모리 병목과 사용자 체감 품질을 동시에 보여주는 지표이므로, batch와 cache 정책을 함께 설계해야 의미 있는 개선이 가능함.
