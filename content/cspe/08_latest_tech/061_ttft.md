---
title: "TTFT 최초 토큰 지연 (Time To First Token)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 61
---

# 📖 【암기용】 개념 완전 이해

> 목적: TTFT를 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: 요청 수신부터 첫 출력 토큰 생성까지의 지연 시간
- **왜 필요한가**: 사용자가 "응답이 시작됐다"고 느끼는 체감 속도를 결정하며, 대화형 서비스의 UX 핵심 지표임.
- **핵심 직관**: 식당에서 주문 후 첫 반찬이 나오기까지의 대기 시간과 같음.

## 깊이 이해
- **배경·문제의식**: LLM은 출력 전에 전체 프롬프트를 한 번 처리(prefill)해야 하므로, 프롬프트가 길수록 첫 토큰이 늦어짐. 70B 모델에 4K 토큰 프롬프트 시 TTFT 200~800ms.
- **작동 원리**: 요청 수신 -> 토크나이징 -> KV cache 계산(prefill) -> 첫 토큰 샘플링. prefill은 프롬프트 길이에 비례하는 compute-bound 연산임.
- **비유**: 시험 문제를 끝까지 다 읽어야 첫 답을 쓸 수 있는 것과 동일.
- **구체 예시**: 70B 모델, A100 1장, 프롬프트 2K 토큰 -> TTFT 약 400ms. Prefix Caching 적용 시 80ms로 단축.
- **흔한 오해·주의점**: TTFT가 짧다고 전체 응답이 빠른 것은 아님. decode 단계(TPOT)가 별도 병목.

## 연결 개념
- TPOT — decode 단계 지연 지표
- Prefix Caching — 공통 프롬프트 재사용으로 TTFT 단축
- Tensor Parallelism — prefill 연산 분산으로 TTFT 감소

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: TTFT는 prefill 단계의 연산 지연으로 결정되는 LLM 서빙 핵심 지연 지표임.
> 2. **가치**: 사용자 체감 응답성을 좌우하며, 대화형 서비스 SLA의 기준 메트릭으로 사용됨.
> 3. **판단 포인트**: 프롬프트 길이·모델 크기·GPU 수·prefix 재사용 여부가 TTFT를 결정함.

---

## Ⅰ. 개요 및 필요성

TTFT는 LLM 첫 토큰 생성 지연 시간임. LLM 서빙에서 사용자 체감 응답성을 결정하는 핵심 SLA 지표로, 프롬프트가 길어지고 모델이 커지면서 prefill 최적화가 서빙 설계의 핵심 과제가 됨.

---

## Ⅱ. 구조 및 구성요소

```text
요청 수신 -> Tokenizer -> Prefill(KV 생성) -> Sampler -> 첫 토큰
                Prefix Cache    TP 분산
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Tokenizer | 프롬프트를 토큰 시퀀스로 변환 | 지연 1~5ms, 병목 아님 |
| Prefill Engine | 전체 프롬프트의 KV cache 일괄 계산 | compute-bound, TTFT의 90% |
| Sampler | 첫 토큰 확률 분포에서 샘플링 | top-p/temperature 적용 |

> 요약: TTFT는 Prefill Engine의 연산 시간이 지배하며, TP 분산과 prefix 재사용이 주요 최적화 축임.

---

## Ⅲ. 동작원리 및 흐름도

```text
요청 -> 프롬프트 토크나이징 -> prefix 캐시 조회
  -> 미스: 전체 prefill -> KV cache 저장 -> 샘플링 -> 첫 토큰 출력
  -> 히트: 잔여 토큰만 prefill -> 샘플링 -> 첫 토큰 출력
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 프롬프트 토크나이징 | 토큰 수, 최대 시퀀스 길이 |
| 2 | Prefix Cache 조회 | 히트율, 캐시 크기(GB) |
| 3 | Prefill 연산(KV 생성) | GPU 활용률, TP degree |
| 4 | 첫 토큰 샘플링·출력 | TTFT SLA(p99 500ms 이내) |

> 요약: prefix 캐시 히트 시 prefill 연산을 건너뛰어 TTFT를 800ms->80ms로 단축함.

---

## Ⅳ. 특징

| 구분 | TTFT | TPOT |
|:---|:---|:---|
| 병목 단계 | prefill(compute-bound) | decode(memory-bound) |
| 영향 인자 | 프롬프트 길이, 모델 크기 | 배치 크기, KV cache 크기 |
| 최적화 기법 | Prefix Caching, TP 분산 | Speculative Decoding, 양자화 |
| 수치 예시 | 70B/A100: 200~800ms | 70B/A100: 20~50ms/token |

> 요약: TTFT는 compute-bound prefill, TPOT는 memory-bound decode가 지배하여 최적화 방향이 다름.

---

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. Prefix Caching으로 시스템 프롬프트 KV를 재사용하여 TTFT 800ms->80ms 달성
2. Tensor Parallelism 4-way 적용으로 prefill FLOPs를 GPU 4장에 분산, TTFT 1/3 단축
3. 프롬프트 길이 제한(4K 토큰) + chunked prefill로 p99 TTFT 500ms SLA 준수

**결론 (2줄):**
- 기술사 판단: 대화형 서비스는 TTFT p99 500ms, 배치 분석은 throughput 우선으로 SLA를 분리 설계함.
- 향후 방향: Prefix Caching + chunked prefill + TP 자동 스케일링으로 프롬프트 길이 무관한 일정 TTFT 달성이 목표임.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | 설명하시오, 기술하시오 | prefill->샘플링 전체 흐름 | TTFT vs TPOT 비교 |
| 요구사항 명시형 | 최적화 방안을 제시하시오 | prefix caching·TP 적용 단계 | 최적화 전후 수치 비교 |

> 요약: 설명형은 prefill 원리, 방안형은 TTFT 단축 기법과 수치를 중심으로 목차를 전환함.
