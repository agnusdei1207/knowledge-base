---
title: "vLLM (vLLM)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 65
extra:
  question_no: "065"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- vLLM은 PagedAttention을 핵심으로 하는 오픈소스 LLM 서빙 프레임워크임
- OpenAI-compatible API는 기존 애플리케이션이 적은 수정으로 대체 엔진을 사용할 수 있게 해주는 인터페이스임
- Tensor Parallelism은 큰 모델을 여러 GPU에 분산해 실행하는 대표 기법임

## Ⅰ. 개요

- **정의/개념**: vLLM은 PagedAttention과 continuous batching을 기반으로 LLM 추론 처리량과 메모리 효율을 높인 오픈소스 서빙 프레임워크로, OpenAI 호환 API와 다양한 추론 최적화 기능을 제공하는 실행 엔진임
- **배경/필요성**: 기본 HuggingFace generate 방식은 동접 요청과 긴 컨텍스트에서 메모리 파편화와 낮은 처리량 문제를 드러내므로, 실제 프로덕션 환경에 맞는 전용 고성능 서빙 엔진이 필요함

## Ⅱ. 특징

- PagedAttention으로 메모리 효율을 높이고 continuous batching으로 처리량을 향상시킴
- OpenAI API 호환 인터페이스를 제공해 서비스 전환 비용을 낮춤
- prefix caching, multi-LoRA, tensor parallelism 같은 실무 기능을 빠르게 수용함
- GPU 메모리 정책과 스케줄링 파라미터 튜닝에 따라 성능 차이가 크게 날 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | 기본 Transformers 서빙 | vLLM | TensorRT-LLM, TGI |
|:---|:---|:---|:---|
| 메모리 관리 | 단순 | PagedAttention 중심 | 엔진별 상이 |
| 배치 스케줄링 | 제한적임 | continuous batching | 엔진별 최적화 |
| 호환성 | 높음 | 매우 높음 | 엔진별 차이 |
| 대표 강점 | 연구 편의성 | 범용 고성능 서빙 | 특정 하드웨어 최적화 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| API Server | OpenAI 호환 엔드포인트를 제공해 애플리케이션 연동 비용을 낮춤 |
| Scheduler, Block Manager | continuous batching과 PagedAttention 블록 관리를 수행해 처리량과 메모리 효율을 높임 |
| Execution Backend | attention kernel과 tensor parallelism을 사용해 실제 GPU 추론을 수행함 |
| Extension Layer | prefix caching, multi-LoRA, speculative decoding 같은 기능을 서비스 정책에 맞게 확장함 |

```text
+------------------+     +------------------+     +------------------+     +------------------+
| API Server       | --> | Scheduler/Block  | --> | Exec Backend     | --> | Extension Layer  |
+------------------+     +------------------+     +------------------+     +------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| API 요청 수신 | --> | 배치/블록 관리 | --> | GPU 추론 실행 | --> | 스트리밍 응답 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **API 요청 수신**: OpenAI 호환 요청을 받아 인증과 파라미터 검증을 수행함
2. **배치 및 블록 관리**: continuous batching과 block manager가 요청 상태와 메모리를 조정함
3. **GPU 추론 실행**: attention 커널과 병렬 실행으로 토큰 생성과 캐시 관리를 수행함
4. **스트리밍 응답 반환**: 생성 토큰을 실시간으로 반환하고 요청 종료 시 메모리를 회수함

## Ⅵ. 문제점 및 해결 방안

1. 문제: `gpu_memory_utilization` 같은 파라미터를 높게 잡으면 캐시 공간은 늘어나지만 activation 공간 부족으로 OOM이 발생할 수 있음
   - 해결방안: 모델 크기와 컨텍스트 길이에 맞춰 메모리 상한을 조정하고 OOM rate와 effective throughput으로 최적 값을 검증함
2. 문제: 다양한 모델과 커널과 GPU 조합을 지원하는 만큼 특정 조합에서는 기대한 최적화가 제대로 작동하지 않을 수 있음
   - 해결방안: 모델별 서빙 프로파일을 유지하고 benchmark 대비 production tokens/sec로 호환성을 검증함
3. 문제: OpenAI 호환성이 높아도 프레임워크 기능이 계속 확장되면서 설정 복잡도가 올라가 운영 실수가 생길 수 있음
   - 해결방안: 표준 서빙 템플릿과 canary rollout을 운영하고 config drift와 deployment failure rate로 운영 안정성을 검증함

## Ⅶ. 적용 사례

- 스타트업 자체 API 대체: 외부 API 비용을 줄이기 위해 오픈모델을 서빙함, 확인 지표는 cost per token과 throughput임
- 사내 온프레미스 챗봇: 민감 데이터가 외부로 나가지 않도록 폐쇄망 배포를 수행함, 확인 지표는 security compliance와 p95 latency임
- 다중 LoRA 서비스: 하나의 기반 모델에 여러 도메인 어댑터를 얹어 운영함, 확인 지표는 adapter switch latency와 memory usage임

## Ⅷ. 결론

vLLM의 가치는 단순 오픈소스 엔진이라는 점보다 PagedAttention과 continuous batching을 실서비스에서 바로 쓸 수 있는 형태로 묶어 LLM 서빙의 사실상 표준 운영 기반을 제공한다는 데 있음.
