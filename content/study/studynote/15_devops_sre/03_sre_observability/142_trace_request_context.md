+++
weight = 142
title = "142. Trace·Span·Context Propagation - 분산 추적의 핵심 구성"
date = "2026-04-19"
[extra]
categories = "studynote-devops-sre"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Trace는 **하나의 요청 전체 경로**, Span은 **각 서비스 구간의 작업 단위**이며, Context Propagation은 **Trace ID·Span ID를 HTTP 헤더(traceparent)로 서비스 간 전파**하여 전체 호출 체인을 연결하는 메커니즘이다.
> 2. **가치**: Context가 전파되지 않으면 각 서비스의 로그가 **독립적으로 흩어져** 연결이 불가능하지만, traceparent 헤더로 **전체 호출 체인을 하나의 Trace로 묶어** 시각화한다.
> 3. **판단 포인트**: W3C Trace Context(traceparent: 00-traceId-spanId-flags)가 표준이며, B3(Zipkin)에서 W3C로 수렴 중이다. 서비스 메시(Istio)가 자동 전파를 지원한다.

---

## Ⅰ. 개요 및 필요성

```text
traceparent: 00-{traceId}-{spanId}-{flags}
  예: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
  → HTTP 요청 헤더로 서비스 간 전파
  → 수신 서비스: 새 Span 생성 + 부모 Span 연결
```

- **📢 섹션 요약 비유**: Context Propagation은 **릴레이 바톤**이다. 각 주자(서비스)가 바톤(Trace ID)을 이어받아 전체 레이스(요청)를 추적한다.

---

## Ⅱ~Ⅴ. 결론

Trace·Span·Context Propagation은 **분산 추적의 3대 핵심**이며, W3C Trace Context가 표준이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Trace** | 전체 요청 경로 |
| **Span** | 개별 작업 구간 |
| **Context** | Trace/Span ID 전파 |
| **traceparent** | W3C 표준 헤더 |
| **Baggage** | 사용자 정의 컨텍스트 |

### 📈 관련 키워드 및 발전 흐름도

```text
[B3 헤더 (Zipkin, 2012)] → [Jaeger 헤더 (Uber)]
    → [W3C Trace Context (2020, 표준)]
    → [OTel Context Propagation (2021)]
    → [현재: W3C 수렴 — B3·Jaeger 호환]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Context는 **릴레이 바톤**이에요. 각 주자(서비스)가 **바톤(ID)**을 이어받아요.
2. 바톤에 **추적 번호(Trace ID)**가 적혀 있어서 전체 레이스를 추적해요.
3. 바톤을 안 넘기면 **누가 달렸는지** 모르니까 꼭 넘겨야 해요!
