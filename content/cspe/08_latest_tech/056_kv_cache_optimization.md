---
title: "KV Cache 최적화 (KV Cache Optimization)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 56
extra:
  question_no: "056"
  exam_status: "기출"
  exam_history: "138회"
  exam_note: "전망"
---

## 미리 알고가기

- KV Cache는 디코딩 단계에서 과거 토큰의 Key, Value를 재사용하기 위해 저장하는 메모리 영역임
- Prefill은 입력 프롬프트 전체를 한 번에 처리해 초기 KV cache를 만드는 단계임
- Decode는 새 토큰을 하나씩 생성하며 기존 KV cache를 계속 참조하는 단계임

## Ⅰ. 개요

- **정의/개념**: KV Cache Optimization은 디코딩 단계에서 누적되는 Key, Value 캐시의 메모리 사용량과 접근 비용을 줄여 LLM 추론 지연과 동시 처리량을 개선하는 메모리 최적화 기술군임
- **배경/필요성**: 긴 컨텍스트와 다중 동시 요청 환경에서는 모델 연산보다 KV cache 저장과 읽기가 더 큰 병목이 되므로, 캐시 크기 압축과 배치 방식 개선과 메모리 관리 최적화가 필요함

## Ⅱ. 특징

- 디코딩 속도와 동시 접속 수를 결정하는 핵심 메모리 병목을 직접 다룸
- 모델 구조 변경 없이도 서빙 레이어에서 상당한 속도 개선 효과를 얻을 수 있음
- GQA, quantization, paging, offloading처럼 구조적, 시스템적 기법이 함께 사용됨
- 캐시 최적화가 과도하면 품질 저하나 fallback 오버헤드가 생길 수 있어 균형 조정이 필요함

## Ⅲ. 종류 및 비교

| 판단 기준 | 기본 KV Cache | 구조 최적화형 GQA, MQA | 시스템 최적화형 Paging, Offloading |
|:---|:---|:---|:---|
| 적용 위치 | 기본 attention 구조 | 모델 아키텍처 | 서빙 메모리 관리 |
| 메모리 절감 효과 | 없음 | 큼 | 큼 |
| 품질 영향 | 기준선 | 약간 있을 수 있음 | 거의 없음 |
| 대표 활용 | 기본 LLM | Llama 계열 | vLLM, 장문맥 서빙 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Prefill Cache Builder | 입력 프롬프트를 처리해 초기 KV cache를 생성하고 요청별 상태를 시작함 |
| Decode Cache Reader | 새 토큰 생성 시 필요한 과거 Key, Value를 반복 참조해 디코딩 속도를 좌우함 |
| Compression Strategy | GQA, FP8, INT8 같은 방식으로 캐시 크기를 줄여 메모리 사용량을 억제함 |
| Cache Manager | paging, sharing, offloading을 통해 실제 GPU, CPU 메모리 배치를 제어함 |

```text
+------------------+     +------------------+     +------------------+     +------------------+
| Prefill Builder  | --> | Decode Reader    | --> | Compression      | --> | Cache Manager    |
+------------------+     +------------------+     +------------------+     +------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| Prefill 생성 | --> | 캐시 저장    | --> | Decode 참조  | --> | 압축/관리    |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **Prefill 생성**: 입력 프롬프트 전체를 처리해 각 레이어의 Key, Value를 계산함
2. **캐시 저장**: 계산된 Key, Value를 요청 상태에 맞는 메모리 공간에 적재함
3. **Decode 참조**: 새 토큰 생성 때 기존 캐시를 읽어 이전 문맥과 attention을 수행함
4. **압축 및 관리**: 캐시 크기와 배치 상태에 따라 quantization, paging, sharing을 적용함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 컨텍스트 길이와 동시 요청 수가 함께 늘어나면 KV cache가 GPU 메모리를 빠르게 소진해 OOM과 처리량 저하를 유발함
   - 해결방안: GQA와 cache quantization과 paging을 조합하고 KV cache size와 동시 요청 수로 메모리 효율을 검증함
2. 문제: 캐시 압축이 과도하면 attention 품질이 흔들려 장문맥 응답 정확도와 안정성이 떨어질 수 있음
   - 해결방안: FP8, INT8 등 단계별 압축 수준을 비교하고 long-context accuracy와 answer faithfulness로 품질을 검증함
3. 문제: 캐시를 GPU 밖으로 오프로딩하면 메모리 여유는 생기지만 전송 지연 때문에 TPOT이 악화될 수 있음
   - 해결방안: hot cache는 GPU에 유지하고 cold cache만 CPU로 이동하며 TPOT과 throughput으로 오프로딩 정책을 검증함

## Ⅶ. 적용 사례

- 장문맥 챗봇 서빙: 긴 대화 이력을 유지하면서도 동접자를 확보함, 확인 지표는 KV cache size와 TPOT임
- 온프레미스 오픈모델 배포: 제한된 VRAM에서 더 큰 컨텍스트를 처리함, 확인 지표는 GPU memory usage와 OOM rate임
- 에이전트 시스템: 여러 도구 호출 중 누적 문맥을 유지함, 확인 지표는 context retention rate와 latency임

## Ⅷ. 결론

KV Cache Optimization의 핵심은 단순 저장 공간 절약이 아니라 디코딩 병목을 메모리 차원에서 줄여 긴 문맥과 동시 요청을 모두 감당할 수 있는 서빙 구조를 만드는 데 있음.
