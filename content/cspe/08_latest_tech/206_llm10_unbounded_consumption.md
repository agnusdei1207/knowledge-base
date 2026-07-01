---
title: "LLM10 무제한 소비 (LLM10 Unbounded Consumption)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 206
---

# 📖 【암기용】 개념 완전 이해

> 목적: LLM10 Unbounded Consumption을 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **정의**: LLM 요청이 토큰, 컨텍스트, GPU, 도구 호출, 비용을 제한 없이 소비해 서비스 중단과 비용 폭증을 유발하는 위험
- **왜 필요한가**: LLM은 요청 1건의 자원 사용량 편차가 크고, 에이전트 도구 호출은 비용을 연쇄 증폭시킬 수 있음.
- **핵심 직관**: 사용량 수도꼭지를 잠그지 않으면 긴 질문 몇 개와 반복 작업만으로 GPU와 예산이 고갈되는 문제임.

## 깊이 이해
- **배경·문제의식**: 기존 API는 요청 수 중심으로 제한했지만 LLM은 입력·출력 토큰, 컨텍스트 길이, tool loop가 비용 단위임.
- **작동 원리**: 공격자나 오류가 긴 컨텍스트, 무한 반복, 고비용 추론, 병렬 요청, 대량 embedding 작업을 발생시켜 자원을 소모함.
- **비유**: 식당 예약 인원만 제한하고 실제 주문량과 이용 시간을 제한하지 않아 한 팀이 주방 전체를 점유하는 상황임.
- **구체 예시**: 128K 컨텍스트와 8K 출력 요청을 다계정으로 반복해 GPU 큐가 포화되고 월 예산 80%가 하루에 소진됨.
- **흔한 오해·주의점**: 단순 rate limit으로 부족하다. token per minute, max context, output cap, tool call budget이 필요함.

## 연결 개념
- Model DoS — 모델 자원 고갈 공격
- LLMOps — 추론 비용·지연·품질 운영
- AI Gateway — 토큰·쿼터·정책 제어 계층

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: LLM10은 LLM 자원과 비용 소비를 제한하지 않아 가용성과 예산이 고갈되는 위험임.
> 2. **가치**: 토큰·GPU·도구 호출 비용이 서비스 SLA와 FinOps에 직접 영향을 줌.
> 3. **판단 포인트**: RPM뿐 아니라 TPM, context cap, output cap, tool budget, circuit breaker를 적용해야 함.

## Ⅰ. 개요 및 필요성

LLM10은 무제한 자원 소비 위험이다. LLM 요청은 토큰과 GPU 사용량 편차가 크다. AI 서비스는 모델 계층 사용량 제한과 비용 통제가 필요하다.

## Ⅱ. 구조 및 구성요소

```text
LLM Request → Token/Context/Tool Usage
  → Cost & Latency Growth → Quota/Breaker Control
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Token Budget | 입력·출력 토큰 제한 | TPM, max output |
| Context Limit | 긴 문맥 제한 | 32K/128K 정책 |
| Tool Budget | 도구 호출 횟수·비용 제한 | agent loop 방지 |
| Circuit Breaker | 장애·비용 초과 차단 | degrade model |

> 요약: LLM10 대응은 토큰, 컨텍스트, 도구 호출, 비용 예산을 정책으로 제한하는 구조임.

## Ⅲ. 동작원리 및 흐름도

```text
요청 수신 → 비용 사전 추정 → 쿼터 검증
  → 추론 실행 → 비용·SLA 모니터링
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 입력 토큰·예상 출력·도구 호출 추정 | cost estimator |
| 2 | 사용자·테넌트별 쿼터 확인 | RPM/TPM/일예산 |
| 3 | timeout·output cap 적용 | p95 latency ≤3초 |
| 4 | 예산 초과 시 degrade·차단 | 예산 80% 경보 |

> 요약: LLM10 방어는 요청 실행 전 비용을 추정하고 실행 중 SLA와 예산을 기준으로 제한함.

## Ⅳ. 특징

| 구분 | 일반 Rate Limit | LLM10 Unbounded Consumption | 판단 포인트 |
|:---|:---|:---|:---|
| 제한 단위 | 요청 수·IP | 토큰·GPU time·tool call | 비용 기반 |
| 위험 | 트래픽 과다 | 소량 고비용 요청 | 요청 편차 |
| 통제 | RPM/QPS | TPM·context·output cap | AI Gateway |
| 운영 | 인프라 모니터링 | FinOps+SRE+LLMOps | 예산 SLA |

> 요약: LLM10은 요청 수보다 자원 사용량과 비용 편차를 중심으로 통제해야 하는 운영 위험임.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 쿼터 설계: 사용자·테넌트별 RPM, TPM, max context, max output, embedding batch size를 정책화
2. 비용 통제: 요청 전 예상 비용을 계산하고 일예산 80% 도달 시 소형 모델 전환 또는 차단 적용
3. 장애 보호: timeout, circuit breaker, prompt cache, priority queue를 적용해 핵심 업무 SLA 99.9% 유지

**결론 (2줄):**
- 기술사 판단: LLM10 대응은 보안과 FinOps를 결합해 토큰·도구·GPU 소비를 사전 제한하는 구조로 설계
- 향후 방향: Unbounded Consumption 관리는 AI Gateway, LLMOps, 비용 예측 모델과 통합됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "LLM10을 설명하시오" | 비용추정→쿼터→모니터링 흐름 | 일반 Rate Limit 대비 차이 |
| 요구사항 명시형 | "LLM 비용·가용성 관리 방안을 제시하시오" | TPM·context·tool budget 설계 | FinOps·SRE 연계 |

> 요약: 설명형은 무제한 소비 위험, 방안형은 토큰·비용·SLA 기반 통제를 중심으로 작성함.
