---
title: "모델 DoS (Model Denial of Service)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 144
---

# 📖 【암기용】 개념 완전 이해

> 목적: 모델 DoS를 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: AI 모델에 과도한 계산·메모리·토큰 비용을 유발하는 입력을 보내 서비스 가용성과 비용을 소진시키는 공격
- **왜 필요한가**: LLM과 AI API는 입력 길이, 추론 토큰, 도구 호출, 검색 요청에 따라 GPU 시간과 비용이 증가한다. 공격자는 복잡한 프롬프트·긴 컨텍스트·반복 도구 호출로 지연과 과금 폭증을 만든다.
- **핵심 직관**: 콜센터에 통화 시간이 긴 질문만 반복해 상담원 좌석을 점유하게 만드는 것과 같다.

## 깊이 이해
- **배경·문제의식**: 기존 DoS는 네트워크 대역폭과 연결 수를 소진시킨다. 모델 DoS는 정상 API 요청처럼 보이지만 GPU VRAM, KV cache, context window, agent tool call을 소모한다.
- **작동 원리**: 공격자는 긴 입력, 압축 해제형 텍스트, 난해한 추론 요청, 무한 루프 유도, 검색 폭증 프롬프트를 사용한다. 시스템은 요청을 정상 처리하면서 p95 지연, GPU 사용률, 토큰 비용이 임계치를 넘는다.
- **비유**: 식당에서 값싼 메뉴를 주문하면서 조리 시간이 긴 특수 요청을 계속 추가해 주방 전체 회전율을 떨어뜨리는 상황이다.
- **구체 예시**: 128K context LLM에 최대 길이 입력과 tool call 20회를 반복시키면 요청당 GPU 시간이 단문 질의 대비 수십 배 증가하고, 동시 요청 100개에서 p95 지연이 SLO 2초를 초과할 수 있다.
- **흔한 오해·주의점**: "WAF와 IP 차단으로 충분함"은 부족하다. 모델 DoS는 토큰 예산, 요청 복잡도, 도구 호출 횟수, GPU 큐 길이를 함께 제한해야 한다.

## 연결 개념
- API Rate Limiting: 사용자·키·조직 단위 호출량과 토큰량 제한
- LLM Gateway: 프롬프트 길이, 출력 토큰, 도구 호출, 비용 정책을 중앙 통제
- SLO/SLA: p95 지연, 오류율, 가용성, 비용 한도를 기준으로 대응

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 모델 DoS는 네트워크 트래픽보다 추론 자원과 토큰 비용을 소진시키는 AI 서비스 가용성 공격이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 모델 DoS는 긴 컨텍스트, 고비용 추론, 반복 도구 호출로 GPU·KV cache·토큰 예산을 소진시키는 서비스 거부 공격이다.
> 2. **가치**: 방어는 rate limit을 호출 수가 아니라 토큰, 추론 시간, tool call, GPU queue, 비용 한도 기준으로 설계해야 한다.
> 3. **판단 포인트**: LLM API, RAG, Agent 서비스는 요청 복잡도별 quota와 circuit breaker 없이는 p95 지연과 월 과금이 동시에 임계치를 넘을 수 있다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| AI 가용성 위협 이해 | 토큰 폭증, 긴 컨텍스트, GPU 큐, 도구 호출 루프 | 일반 DDoS 대역폭 문제로만 설명 |
| 방어 아키텍처 설계 | LLM Gateway, token budget, timeout, queue isolation | IP 차단과 CAPTCHA만 제시 |
| 운영 지표 판단 | p95 latency, tokens/request, GPU util, cost/hour | TPS만 보고 모델 비용 누락 |
> 요약: 이 문제는 AI 추론 자원의 비용·지연·격리 지표를 중심으로 가용성 통제를 설계하는 역량을 본다.

---

## Ⅰ. 개요 및 필요성

모델 DoS는 AI 추론 자원을 소진시켜 서비스 지연·오류·비용 폭증을 유발하는 공격이다.
LLM 서비스는 입력 토큰, 출력 토큰, context window, tool call 수에 비례해 GPU 시간과 비용이 증가한다.
기업 AI 서비스는 네트워크 방어와 별도로 모델 게이트웨이, 비용 한도, 큐 격리, SLO 기반 차단을 설계해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Client / Attacker -> API Gateway -> LLM Gateway -> Model Runtime
                                  +-> Token Budget / Policy / Queue
Model Runtime -> Tool / RAG / Agent Loop -> Response / Cost Log
```

| 구성요소 | 역할 | 통제 포인트 |
|:---|:---|:---|
| API Gateway | 인증, 조직·키 단위 접근 제어 | key quota, mTLS, WAF 연계 |
| LLM Gateway | 입력·출력·도구 호출 정책 적용 | max tokens, timeout, cost cap |
| 모델 런타임 | GPU/CPU에서 추론 수행 | GPU util, KV cache, batch queue |
| 도구/RAG 계층 | 검색·함수호출·에이전트 실행 | tool call limit, recursion depth |
| 관측 계층 | 지연·토큰·비용·오류 수집 | OpenTelemetry, billing log |
> 요약: 모델 DoS 방어는 API 앞단보다 LLM Gateway와 런타임 큐에서 토큰·시간·비용을 제한하는 구조가 핵심이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
고비용 요청 생성 -> 인증 통과 -> 긴 입력/도구 호출 실행
-> GPU 큐 적체 / 토큰 비용 증가 -> SLO 초과 -> 제한/격리/차단
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 긴 컨텍스트·난해한 추론·반복 tool call 요청 | input tokens, requested max output |
| 2 | 게이트웨이 정책 검증 | org quota, risk score, allowlist |
| 3 | 모델 추론과 도구 호출 수행 | GPU queue length, tool call count |
| 4 | SLO·비용 임계치 초과 여부 판단 | p95 2초, cost/hour, error rate |
| 5 | timeout, degrade, circuit breaker 적용 | 차단률, 정상 사용자 영향 |
> 요약: 모델 DoS는 정상 요청 경로를 사용하므로 요청 복잡도와 자원 사용량 기준으로 단계별 제한해야 한다.

---

## Ⅳ. 특징

| 구분 | 기존 DDoS | 모델 DoS | 수치·판단 기준 |
|:---|:---|:---|:---|
| 소진 자원 | 네트워크 대역폭, 연결 수 | GPU, VRAM, KV cache, 토큰 비용 | tokens/request, GPU util |
| 요청 형태 | 대량 패킷·봇 트래픽 | 정상 API처럼 보이는 고비용 요청 | p95 latency, cost/hour |
| 방어 위치 | CDN, WAF, L4/L7 LB | LLM Gateway, scheduler, quota | max input/output tokens |
| 피해 양상 | 접속 불가, 5xx 증가 | 지연, 과금 폭증, agent loop | tool call 5회 이하 제한 |
> 요약: 모델 DoS는 트래픽 수보다 요청당 계산 비용이 핵심이므로 토큰·도구·GPU 큐 지표로 판단한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 제한 단위 | IP·요청 수 | 사용자·토큰·GPU초·비용 | LLM API와 RAG 서비스 |
| 격리 방식 | 공통 서버 풀 | tenant별 queue, priority, circuit breaker | 유료/무료 사용자 혼재 |
| 운영 목표 | 오류율 감소 | SLO 준수와 비용 상한 동시 충족 | 월 과금·p95 지연 관리 필요 |
> 요약: AI 서비스는 호출 수 제한보다 자원 기반 quota와 tenant 격리를 적용해야 모델 DoS를 통제할 수 있다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 토큰 폭탄 | 긴 입력·출력 최대값 요청 | max context, output cap, summarization | tokens/request p95 |
| Agent 루프 | 도구 재귀·반복 계획 | recursion depth, tool timeout | tool calls/session |
| 정상 사용자 피해 | 공격 요청과 같은 큐 사용 | priority queue, bulkhead, degrade mode | paid user p95, error rate |
> 요약: 토큰 폭탄, 도구 루프, 큐 공유를 분리해 제한해야 공격 요청이 정상 사용자를 밀어내지 않는다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 지연 | p95 2초, p99 5초 이하 | APM, OpenTelemetry trace |
| 자원 | GPU util 80% 이하, queue wait 500ms 이하 | runtime metrics, scheduler log |
| 비용 | 조직별 일 비용 한도 100% 이하 | billing log, FinOps dashboard |
> 요약: 모델 DoS 대응 성과는 지연, GPU 큐, 조직별 비용 한도를 동시에 만족하는지로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. LLM Gateway: max input 8K/32K tier, max output 2K, tool call 5회, request timeout 30초 정책을 조직별로 적용
2. 자원 격리: 무료·유료·관리자 tenant queue를 분리하고 paid user p95 2초 초과 시 무료 tier degrade mode 전환
3. 관측·차단: tokens/request p95, GPU queue wait, cost/hour를 SIEM과 FinOps 대시보드에 연결해 임계치 초과 시 circuit breaker 실행

**결론 (2줄):**
- 기술사 판단: LLM 서비스의 가용성은 네트워크 TPS가 아니라 토큰·GPU초·도구 호출 수 기준 quota로 관리해야 함
- 향후 방향: AI Gateway와 FinOps, SRE SLO가 결합되어 모델 추론 비용과 가용성을 같은 통제면에서 운영하게 됨

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "모델 DoS를 설명하시오" | 고비용 요청이 GPU·토큰·도구 자원을 소진하는 흐름 | 기존 DDoS와 모델 DoS 비교 |
| 요구사항 명시형 | "대응 방안을 제시하시오", "운영 방안을 설계하시오" | LLM Gateway, quota, queue isolation 절차 | SLO·비용·GPU 지표 기반 선택 |
> 요약: 설명형은 자원 소진 원리, 운영형은 토큰 예산과 큐 격리 중심으로 목차를 구성한다.
