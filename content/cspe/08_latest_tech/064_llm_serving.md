---
title: "LLM 서빙 (LLM Serving)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 64
---

# 📖 【암기용】 개념 완전 이해

> 목적: LLM Serving을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 학습된 LLM을 API·애플리케이션에서 SLA 기준으로 호출하도록 배포·추론·스케일링하는 운영 체계
- **왜 필요한가**: 모델 파일만 있으면 서비스가 되는 것이 아니라, GPU 메모리·배치·지연·보안·비용을 함께 관리해야 함.
- **핵심 직관**: 모델을 연구실 데모에서 24시간 운영되는 생산 라인으로 올리는 과정임.

## 깊이 이해
- **배경·문제의식**: LLM은 수십GB~수백GB 가중치와 긴 KV Cache를 사용해 일반 웹 API보다 자원 제약이 큼. 트래픽 급증 시 OOM, tail latency, 비용 폭증이 발생함.
- **작동 원리**: 모델 로딩->토크나이징->prefill->decode->streaming 응답을 처리하고, scheduler가 batching·cache·GPU parallelism을 조정함. 관측성은 TTFT·TPOT·tokens/s·error rate로 수행함.
- **비유**: 대형 주방에서 주문 접수, 재료 준비, 조리, 배식, 재고·비용 관리를 동시에 하는 것과 같음.
- **구체 예시**: 70B FP16 모델은 가중치만 약 140GB가 필요하므로 tensor parallel 2~4 GPU 또는 양자화가 필요함.
- **흔한 오해·주의점**: 모델 정확도만 높으면 되는 것이 아님. p95 지연, GPU 원가, 권한 통제, 프롬프트 보안까지 운영 품질에 포함됨.

## 연결 개념
- vLLM/TensorRT-LLM — 대표 LLM 서빙 엔진
- TTFT/TPOT — 서빙 지연 SLA
- KV Cache/PagedAttention — 서빙 메모리 최적화

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: LLM Serving은 모델 추론을 API로 안정 제공하기 위한 런타임·스케줄러·관측성·보안 운영 체계임.
> 2. **가치**: GPU idle time과 KV cache 낭비를 줄여 p95 지연, tokens/s, $/1K tokens를 서비스 목표에 맞춤.
> 3. **판단 포인트**: 모델 크기, 병렬화, 배칭, KV Cache, 가드레일, FinOps를 통합 설계해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| LLM 운영 아키텍처 설계 역량 확인 | Gateway-엔진-GPU워커-관측성 4계층, TTFT/TPOT SLA | 모델 정확도만 서술하고 운영 계층 누락 |
| 일반 ML Serving과 차별점 확인 | KV Cache 메모리, 토큰 단위 스케줄링, streaming | 웹 API 스케일링 일반론으로 대체 |
| 비용·보안 통합 판단 확인 | $/1K tokens, quota, prompt injection·PII 통제 | 성능 얘기만 하고 보안·FinOps 누락 |

> 요약: 이 문제는 추론 API 구축이 아니라 지연·비용·보안을 동시에 만족하는 운영 체계 설계를 묻는다.

## Ⅰ. 개요 및 필요성

- 개요: LLM 운영 배포·추론 체계
- 배경: 생성형 AI 서비스는 GPU 메모리, KV cache, 토큰 단가가 운영 비용과 지연의 주 제약이 됨.
- 필요성: vLLM·TensorRT-LLM, 스케줄링, 관측성, RBAC·감사로그를 함께 설계해 p95 지연과 $/1K tokens를 관리해야 함.

## Ⅱ. 구조 및 구성요소

```text
Client -> API Gateway -> Serving Engine -> GPU Workers

       Auth/Rate     Scheduler       Model+KV Cache
           -------- Observability/Guardrail --------
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| API Gateway | 인증·Rate Limit·라우팅 | tenant별 quota |
| Serving Engine | prefill/decode·batching 처리 | vLLM, TensorRT-LLM |
| GPU Worker | 모델 가중치·KV Cache 보유 | TP/PP/quantization |
| Observability | TTFT·TPOT·tokens/s 수집 | SLO·FinOps 기준 |

> 요약: LLM Serving은 API 계층, 추론 엔진, GPU 워커, 관측성·보안 계층으로 구성됨.

## Ⅲ. 동작원리 및 흐름도

```text
요청 인증 -> 토큰화 -> 스케줄링 -> prefill -> decode
    -> streaming 응답 -> 로그/비용/안전성 기록
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 인증·quota·prompt 정책 확인 | RBAC, rate limit |
| 2 | 토큰화·batch scheduling | queue time, batch token |
| 3 | prefill/decode 실행 | TTFT, TPOT, GPU util |
| 4 | 응답 streaming·로그 기록 | error rate, $/1K tokens |

> 요약: 요청 진입부터 응답 streaming까지 지연·비용·안전성을 계측하며 GPU 추론을 운영함.

## Ⅳ. 특징

| 구분 | 일반 ML Serving | LLM Serving | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 자원 | CPU/GPU 단발 추론 | 대용량 GPU+KV Cache | 70B FP16 약 140GB |
| 지연 | 단일 inference latency | TTFT+TPOT 분리 | streaming SLA |
| 스케줄링 | 요청 단위 batch | token step batch | continuous batching |
| 보안 | 입력 검증 중심 | prompt injection·PII·output guard | 감사로그 필요 |

> 요약: LLM Serving은 토큰 단위 지연과 GPU 메모리 관리가 핵심이며 일반 ML Serving보다 운영 변수가 많음.

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 상용 API (GPT·Claude) | 자체 서빙 (vLLM 등) | 선택 기준 |
|:---|:---|:---|:---|
| 초기 비용·운영 | 무설비, 토큰 과금 | GPU 확보·운영 인력 필요 | 월 토큰량이 GPU 상각비를 넘으면 자체 서빙 |
| 데이터 통제 | 외부 전송 (계약 의존) | 내부망 유지 가능 | 민감 데이터·규제 산업은 자체 서빙 |
| 모델 품질·최신성 | 최상위 모델 즉시 사용 | 오픈모델 한계 | 품질 요구가 높으면 상용 API 우선 |

> 요약: 토큰 물량·데이터 규제·품질 요구 3축으로 상용 API와 자체 서빙을 판단함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| GPU OOM·장애 | KV Cache 폭증, 긴 컨텍스트 | max model len 제한, TP 분산 | OOM 0건, 가용성 99.9% |
| 비용 폭주 | 무제한 호출·긴 프롬프트 | tenant quota, prompt 길이 상한 | $/1K tokens, 월 예산 준수 |
| 프롬프트 보안 사고 | injection·PII 유입 | 입력 필터+출력 Guard, 감사로그 | 차단율, 유출 0건 |

> 요약: LLM Serving 리스크는 메모리·비용·보안 3축이며, 상한 설정과 이중 방어로 통제함.

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. vLLM/TensorRT-LLM 중 모델·GPU 지원성을 비교하고 TTFT·TPOT·tokens/s 기준으로 엔진 선택
2. API Gateway에서 tenant별 quota, prompt length limit, RBAC를 적용해 비용 폭주와 데이터 오염 차단
3. Grafana/Prometheus로 TTFT p95, TPOT p95, GPU util, cache hit, $/1K tokens를 관측

**결론 (2줄):**
- 기술사 판단: 대화형 API는 latency-aware serving, 배치 분석은 throughput-optimized serving으로 분리함.
- 향후 방향: LLM Serving은 라우터·가드레일·FinOps·Agent runtime을 포함한 AI 플랫폼 계층으로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 | Ⅴ·Ⅵ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | 인증->prefill->decode->관측 흐름 | 일반 ML Serving 대비 차이 |
| 요구사항 명시형 | 설계하시오, 운영 방안을 제시하시오 | 엔진 선택·SLA·보안 절차 | GPU 비용·지연·가드레일 기준 |

> 요약: 설명형은 운영 구조, 설계형은 SLA·비용·보안 통합 기준으로 목차를 전환함.
