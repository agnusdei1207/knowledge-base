---
title: "vLLM"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 65
---

# 📖 【암기용】 개념 완전 이해

> 목적: vLLM을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **정의**: PagedAttention과 continuous batching을 중심으로 LLM 추론 처리량을 높이는 오픈소스 서빙 엔진
- **왜 필요한가**: 기본 Transformers 추론은 KV Cache 단편화와 정적 배치 한계로 고동시성 서비스 처리량이 낮음.
- **핵심 직관**: GPU 메모리를 페이지처럼 잘게 나누고, 빈 자리에 새 요청을 계속 넣어 LLM API 처리량을 높이는 런타임임.

## 깊이 이해
- **배경·문제의식**: 대화형 LLM은 요청 길이와 출력 길이가 모두 달라 GPU 메모리 낭비가 크다. vLLM은 KV Cache를 OS 페이지처럼 관리해 단편화를 줄이고, 동적 배칭으로 GPU 유휴 시간을 줄임.
- **작동 원리**: 요청 큐를 scheduler가 관리하고, PagedAttention이 KV block table을 통해 가변 길이 sequence를 처리함. OpenAI-compatible API 서버로 애플리케이션 연동이 가능함.
- **비유**: 호텔 객실을 통째로 장기 배정하지 않고, 필요한 객실만 배정·회수해 객실 회전율을 높이는 방식임.
- **구체 예시**: 동일 GPU에서 PagedAttention과 continuous batching 적용 시 naive serving 대비 동시 요청 수와 tokens/s가 증가함.
- **흔한 오해·주의점**: vLLM은 모든 모델·GPU에서 항상 최적은 아님. 모델 아키텍처, quantization, LoRA, tensor parallel 지원성을 확인해야 함.

## 연결 개념
- PagedAttention — vLLM의 핵심 KV Cache 관리 기법
- Continuous Batching — vLLM 처리량 개선 축
- LLM Serving — vLLM 적용 영역

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: vLLM은 PagedAttention 기반 KV Cache 가상화와 동적 배칭을 제공하는 LLM 서빙 엔진임.
> 2. **가치**: 가변 길이 요청의 메모리 낭비를 줄여 동일 GPU에서 tokens/s와 동시성을 높임.
> 3. **판단 포인트**: 모델 지원성, tensor parallel, quantization, LoRA, OpenAI-compatible API 연동을 검토해야 함.

## Ⅰ. 개요 및 필요성

vLLM은 오픈소스 LLM 서빙 엔진임. 고동시성 LLM API는 KV Cache 단편화와 정적 배치 병목이 발생하므로, PagedAttention과 continuous batching 기반 런타임이 필요함.

## Ⅱ. 구조 및 구성요소

```text
Client/OpenAI API → vLLM Server → Scheduler
       → PagedAttention KV Blocks → GPU Executor → Streaming
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| OpenAI API Server | REST 호환 엔드포인트 제공 | 기존 앱 연동 용이 |
| Scheduler | 요청 큐·continuous batching | prefill/decode 조정 |
| PagedAttention | KV Cache block 관리 | 단편화 감소 |
| GPU Executor | 모델 실행·병렬화 | TP, quantization 지원 |

> 요약: vLLM은 API 서버, 스케줄러, PagedAttention, GPU 실행기로 구성된 LLM 추론 런타임임.

## Ⅲ. 동작원리 및 흐름도

```text
요청 수신 → 토큰화 → scheduler 배치 편성
    → PagedAttention KV 할당 → GPU decode → streaming 반환
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | OpenAI-compatible 요청 수신 | endpoint, auth proxy |
| 2 | continuous batching으로 배치 구성 | queue time, active seq |
| 3 | PagedAttention으로 KV block 관리 | block utilization, OOM |
| 4 | GPU 실행·streaming 응답 | TTFT, TPOT, tokens/s |

> 요약: vLLM은 동적 배치와 KV block 관리를 결합해 고동시성 요청을 GPU에 효율적으로 공급함.

## Ⅳ. 특징

| 구분 | Transformers 기본 서빙 | vLLM | 수치·판단 포인트 |
|:---|:---|:---|:---|
| KV 관리 | 연속 메모리 | PagedAttention | OOM·단편화 감소 |
| 배칭 | 정적/제한적 | continuous batching | 혼합 길이 트래픽 적합 |
| API | 직접 구현 필요 | OpenAI-compatible | 전환 비용 감소 |
| 한계 | 단순 | 커널·모델 지원성 확인 | 신규 모델 검증 필요 |

> 요약: vLLM은 범용 LLM API 처리량 개선에 강점이 있으나, 모델별 지원성과 품질 회귀 검증이 필요함.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 사내 LLM API를 vLLM OpenAI-compatible endpoint로 구성하고 기존 SDK 연동 비용을 축소
2. 배포 전 모델별 TTFT, TPOT, tokens/s, OOM, 정확도 회귀를 Transformers baseline과 비교
3. tenant별 max model len, max num seqs, max batch tokens를 설정해 비용 폭주와 tail latency 제한

**결론 (2줄):**
- 기술사 판단: 오픈모델 기반 대화형 API는 vLLM을 우선 검토하고, NVIDIA 전용 극한 최적화는 TensorRT-LLM과 비교함.
- 향후 방향: vLLM은 serving engine을 넘어 LoRA serving, speculative decoding, distributed inference 기능을 확장함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | scheduler·PagedAttention 흐름 | 기본 서빙 대비 차이 |
| 요구사항 명시형 | 도입 방안을 제시하시오, 비교하시오 | 벤치마크·설정·검증 절차 | vLLM vs TensorRT-LLM 선택 기준 |

> 요약: 설명형은 vLLM 구조, 도입형은 엔진 선택과 운영 파라미터 중심으로 목차를 전환함.
