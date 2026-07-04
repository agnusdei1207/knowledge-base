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
- **개요**: PagedAttention과 continuous batching을 중심으로 LLM 추론 처리량을 높이는 오픈소스 서빙 엔진
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

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 서빙 엔진 핵심 기법 이해 확인 | PagedAttention(KV block 가상화), continuous batching | 제품 소개만 하고 기법 원리 누락 |
| 엔진 선택 판단 확인 | vLLM vs TensorRT-LLM 비교 축(범용성 vs NVIDIA 극한 최적화) | 특정 엔진을 무조건 우위로 단정 |
| 도입 검증 역량 확인 | baseline 대비 TTFT·TPOT·정확도 회귀 검증 절차 | 벤치마크 없이 도입 결론 서술 |

> 요약: 이 문제는 도구 사용법이 아니라 KV 메모리 관리 원리와 엔진 선택·검증 기준을 묻는다.

## Ⅰ. 개요 및 필요성

- 개요: 오픈소스 LLM 서빙 엔진
- 배경: 고동시성 LLM API는 KV cache 단편화와 정적 배치로 GPU 메모리 낭비와 큐 대기가 발생함.
- 필요성: PagedAttention과 continuous batching으로 KV block을 관리하고 throughput·p95 latency를 동시에 측정해야 함.

## Ⅱ. 구조 및 구성요소

```text
Client/OpenAI API -> vLLM Server -> Scheduler
       -> PagedAttention KV Blocks -> GPU Executor -> Streaming
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
요청 수신 -> 토큰화 -> scheduler 배치 편성
    -> PagedAttention KV 할당 -> GPU decode -> streaming 반환
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | OpenAI-compatible 요청 수신 | endpoint, auth proxy |
| 2 | continuous batching으로 배치 구성 | queue time, active seq |
| 3 | PagedAttention으로 KV block 관리 | block utilization, OOM |
| 4 | GPU 실행·streaming 응답 | TTFT, TPOT, tokens/s |

> 요약: vLLM은 동적 배치와 KV block 관리를 결합해 고동시성 요청의 GPU idle time을 줄임.

## Ⅳ. 특징

| 구분 | Transformers 기본 서빙 | vLLM | 수치·판단 포인트 |
|:---|:---|:---|:---|
| KV 관리 | 연속 메모리 | PagedAttention | OOM·단편화 감소 |
| 배칭 | 정적/제한적 | continuous batching | 혼합 길이 트래픽 적합 |
| API | 직접 구현 필요 | OpenAI-compatible | 전환 비용 감소 |
| 한계 | 단순 | 커널·모델 지원성 확인 | 신규 모델 검증 필요 |

> 요약: vLLM은 범용 LLM API 처리량 개선에 강점이 있으나, 모델별 지원성과 품질 회귀 검증이 필요함.

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | vLLM | TensorRT-LLM | 선택 기준 |
|:---|:---|:---|:---|
| 하드웨어 | NVIDIA·AMD 등 폭넓음 | NVIDIA 전용 | 이기종 GPU 혼용이면 vLLM |
| 최적화 방식 | 런타임 스케줄링 중심 | 커널 컴파일 극한 최적화 | 고정 모델·최대 성능이면 TensorRT-LLM |
| 도입 난이도 | pip 설치, OpenAI 호환 | 엔진 빌드 필요 | 빠른 도입·모델 교체 잦으면 vLLM |

> 요약: 모델 교체가 잦고 범용성이 필요하면 vLLM, NVIDIA 고정 스택의 극한 성능이면 TensorRT-LLM을 선택함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 신규 모델 미지원 | 아키텍처별 커널 의존 | 지원 매트릭스 사전 확인, fallback 경로 | 배포 전 호환성 체크 통과 |
| 품질 회귀 | quantization·커널 차이 | baseline 대비 정확도 회귀 테스트 | 벤치마크 점수 편차 1% 이내 |
| 버전 업그레이드 파손 | 빠른 릴리스 주기 | 카나리 배포, 성능·정확도 게이트 | 롤백 시간, 게이트 통과율 |

> 요약: vLLM 리스크는 지원성과 회귀이며, 사전 호환 확인과 카나리 게이트로 통제함.

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 사내 LLM API를 vLLM OpenAI-compatible endpoint로 구성하고 기존 SDK 연동 비용을 축소
2. 배포 전 모델별 TTFT, TPOT, tokens/s, OOM, 정확도 회귀를 Transformers baseline과 비교
3. tenant별 max model len, max num seqs, max batch tokens를 설정해 비용 폭주와 tail latency 제한

**결론 (2줄):**
- 기술사 판단: 오픈모델 기반 대화형 API는 vLLM을 우선 검토하고, NVIDIA 전용 극한 최적화는 TensorRT-LLM과 비교함.
- 향후 방향: vLLM은 serving engine을 넘어 LoRA serving, speculative decoding, distributed inference 기능을 확장함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 | Ⅴ·Ⅵ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | scheduler·PagedAttention 흐름 | 기본 서빙 대비 차이 |
| 요구사항 명시형 | 도입 방안을 제시하시오, 비교하시오 | 벤치마크·설정·검증 절차 | vLLM vs TensorRT-LLM 선택 기준 |

> 요약: 설명형은 vLLM 구조, 도입형은 엔진 선택과 운영 파라미터 중심으로 목차를 전환함.
