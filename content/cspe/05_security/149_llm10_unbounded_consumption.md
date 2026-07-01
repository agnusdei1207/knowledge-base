---
title: "LLM10 무제한 소비 (LLM10 Unbounded Consumption)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 149
---

# 📖 【암기용】 개념 완전 이해

> 목적: LLM10 무제한 소비를 가용성·비용·모델 보호 관점에서 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: LLM 사용량을 제한하지 않아 과도한 추론 요청, 긴 컨텍스트, 반복 호출로 서비스 중단·비용 폭증·모델 추출이 발생하는 취약점
- **왜 필요한가**: LLM은 요청 1건도 토큰 수, 컨텍스트 길이, 도구 호출 횟수에 따라 비용과 GPU 시간이 크게 달라진다.
- **핵심 직관**: 전통 DoS가 서버 CPU를 고갈시키는 공격이라면, LLM10은 토큰과 추론 비용을 고갈시키는 DoS와 Denial of Wallet이다.

## 깊이 이해
- **배경·문제의식**: 클라우드 LLM API는 입력·출력 토큰, 이미지, tool call, 검색 호출마다 비용이 붙는다. 공격자는 긴 프롬프트, 반복 질의, 병렬 세션, 자동 재시도를 이용해 예산과 quota를 소모시킨다.
- **작동 원리**: variable-length input flood, context window overflow, resource-heavy prompt, model extraction, retry storm이 대표 경로이다. 방어는 rate limit, token budget, queue, circuit breaker, billing alert로 구성된다.
- **비유**: 수도요금 종량제 건물에서 수도꼭지를 무제한 개방하고 입주자별 계량기를 두지 않은 상황과 같다.
- **구체 예시**: 128K 컨텍스트 모델에 10만 토큰 입력을 초당 20건 보내면, 일반 1K 토큰 질의 대비 GPU 시간과 API 비용이 수십 배 증가해 정상 사용자의 p95 지연이 기준 SLO를 초과할 수 있다.
- **흔한 오해·주의점**: WAF rate limit만으로 충분하지 않다. 요청 수가 적어도 토큰 수와 tool call이 크면 비용이 폭증하므로 token-aware limit이 필요함.

## 연결 개념
- OWASP LLM Top 10 2025 — LLM10 Unbounded Consumption으로 분류
- FinOps — 사용자·테넌트·기능별 예산 통제와 연결
- API Gateway·Queue·Circuit Breaker — 추론 가용성 보호 수단

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 무제한 소비는 단순 트래픽 폭주가 아니라 토큰·GPU·API 비용·모델 지식재산을 동시에 보호하는 자원 통제 문제이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: LLM10 Unbounded Consumption은 추론 요청·토큰·컨텍스트·도구 호출에 제한이 없어 가용성 저하, 비용 폭증, 모델 추출이 발생하는 취약점이다.
> 2. **가치**: token budget, per-tenant quota, adaptive rate limit, circuit breaker를 적용하면 비용과 SLO를 계량 지표로 통제함.
> 3. **판단 포인트**: 요청 수 기반 제한이 아니라 입력 토큰, 출력 토큰, 동시성, tool call, 재시도 횟수를 함께 제한해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| LLM 가용성 공격 이해 확인 | DoS, Denial of Wallet, model extraction, retry storm | 일반 DDoS 설명만 쓰고 토큰 비용 누락 금지 |
| 자원 통제 설계 확인 | token-aware limit, quota, queue, circuit breaker, budget alert | WAF rate limit 한 줄로 끝내지 않음 |
| 운영 지표 판단 확인 | p95 지연, token/sec, cost/user, quota exhaustion | 비용·SLO 지표 없이 보안 통제만 나열 금지 |

> 요약: 이 문제는 LLM 추론 자원을 토큰·동시성·비용 단위로 제한하는 운영 보안 설계를 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: LLM10 추론 자원 무제한 사용
- 배경: LLM은 요청 수보다 토큰 길이, 컨텍스트 크기, 도구 호출, 재시도가 GPU 시간과 비용을 좌우함.
- 필요성: OWASP LLM10 기준으로 사용자·테넌트별 토큰 예산, rate limit, 재시도 한도, SLO 기반 차단 정책을 운영해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Client -> API Gateway -> Token Meter -> Quota Manager -> Inference Queue
                  +-> Risk Scorer -> Circuit Breaker
LLM / Tool Calls -> Cost Monitor -> Alert / Throttle / Block
```

| 구성요소 | 역할 | 통제 포인트 |
|:---|:---|:---|
| API Gateway | 인증·요청 수 제한 | IP/user/token rate limit |
| Token Meter | 입력·출력 토큰 추정 | max input 8K, max output 2K 같은 정책 |
| Quota Manager | 사용자·테넌트별 예산 관리 | daily token quota, monthly cost cap |
| Inference Queue | 동시성·우선순위 제어 | concurrency limit, priority class |
| Cost Monitor | 비용·SLO 감시 | cost/min, p95 latency, error budget |

> 요약: LLM10 방어 구조는 요청 수가 아니라 토큰·동시성·비용을 측정하고, quota 초과 시 throttle 또는 block을 수행한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요청 수신 -> 인증/사용자 식별 -> 토큰·도구 비용 예측
-> quota·동시성 확인 -> queue 배치 또는 차단 -> 추론 실행 -> 비용·SLO 로그 갱신
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | API key, user, tenant 식별 | 인증 성공, abuse history |
| 2 | 입력 토큰과 예상 출력 토큰 계산 | token count, context window limit |
| 3 | quota와 동시성 한도 확인 | daily quota, concurrent request limit |
| 4 | queue, throttle, circuit breaker 적용 | queue depth, p95 latency, error rate |
| 5 | 사용량·비용·차단 로그 저장 | cost/user, token/sec, quota hit |

> 요약: 무제한 소비 대응은 요청 전 비용 예측, 실행 전 quota 검증, 실행 후 비용 로그 갱신의 폐루프로 동작한다.

---

## Ⅳ. 특징

| 구분 | 일반 API DoS | LLM10 무제한 소비 | 수치·기술 포인트 |
|:---|:---|:---|:---|
| 자원 단위 | 요청 수, CPU, 메모리 | 입력·출력 토큰, GPU time, tool call, 비용 | tokens/sec, GPU queue |
| 공격 형태 | 대량 요청 | 긴 컨텍스트, 반복 질의, retry storm, model extraction | 128K context abuse |
| 피해 | 서비스 지연 | 비용 폭증, quota 고갈, 모델 복제 위험 | Denial of Wallet |
| 방어 | IP rate limit | token budget, quota, circuit breaker, anomaly detection | per-tenant cost cap |

> 요약: LLM10은 요청 수 제한만으로 식별하기 어렵고, 토큰·비용·동시성 지표를 합산해야 차단 가능하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 단순 rate limit | token-aware gateway+quota manager | 긴 컨텍스트 모델 또는 유료 API 사용 시 필수 |
| 비용/성능 | 무제한 재시도 | bounded retry+backoff+circuit breaker | p95 지연 SLO 2초 초과 시 차단 |
| 운영/위험 | 월말 비용 확인 | 실시간 cost alert+tenant budget | cost/user가 기준 대비 3배 초과 시 throttle |

> 요약: LLM10 통제는 클라우드 비용이 추론량에 비례하는 환경에서 FinOps와 보안 운영을 결합해 적용한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Denial of Wallet | 무제한 토큰·API 호출 | cost cap, prepaid quota, anomaly alert | cost/min, cost/user |
| 서비스 지연 | 긴 입력·동시 요청 | max context, queue, priority class | p95 latency, queue depth |
| 모델 추출 | 반복 질의로 경계 학습 | query similarity limit, watermark, output cap | similar query burst 건수 |

> 요약: 비용 고갈, 서비스 지연, 모델 추출은 각각 비용·지연·유사 질의 지표로 조기 탐지한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 토큰 한도 | 사용자별 daily token quota, 요청별 max input/output | gateway token counter |
| 가용성 | p95 latency 2초 이하, error rate 1% 이하 | APM, inference queue metric |
| 비용 통제 | tenant별 monthly cap, 이상 비용 10분 내 알림 | billing API, FinOps dashboard |

> 요약: LLM10 성공 기준은 토큰 한도 준수, p95 지연 SLO, 비용 알림 MTTA 10분 이하로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. Token-aware Gateway: 요청별 입력 8K·출력 2K 등 모델별 한도를 적용하고 초과 요청은 요약·분할·차단으로 처리
2. Quota·예산 통제: 사용자·테넌트별 daily token quota와 monthly cost cap을 설정하고 80%·100% 도달 시 알림·throttle 적용
3. 가용성 보호: inference queue, priority class, exponential backoff, circuit breaker를 적용해 p95 지연 2초 초과 시 저우선 요청 차단

**결론 (2줄):**
- 기술사 판단: 내부 업무 보조는 quota 중심, 대외 공개 서비스는 token-aware gateway와 circuit breaker를 필수 통제로 선택함
- 향후 방향: Agent가 다중 tool call을 수행하면서 비용 단위가 복합화되므로 요청 단위보다 workflow 단위 예산 통제가 필요함

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "무제한 소비를 설명하시오", "기술하시오" | 토큰·quota·queue 기반 동작 흐름 | 일반 DoS와 LLM10 차이 |
| 요구사항 명시형 | "대응 방안을 제시하시오", "운영 방안을 논하시오", "설계하시오" | gateway·quota·circuit breaker 설계 | 비용·SLO·모델 추출 대응 지표 |

> 요약: 설명형은 소비 자원 구조를, 운영형은 토큰 예산과 SLO 차단 정책을 중심으로 목차를 전환한다.
