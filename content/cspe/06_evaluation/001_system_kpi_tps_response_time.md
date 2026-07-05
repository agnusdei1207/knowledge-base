---
title: "시스템 KPI: TPS와 응답시간 (System KPI: TPS & Response Time)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-evaluation"
weight: 1
---

## 📖 【암기용】 핵심 요약

*   **한눈에**: 시스템의 **처리 용량(Capacity)**을 나타내는 TPS(Throughput)와 **사용자 체감 속도(Latency)**를 나타내는 응답시간(Response Time)으로 구성된 성능 평가의 절대 기준.
*   **깊이 이해**:
    *   **배경**: 단일 서버 시절엔 CPU/Memory만 봤지만, 분산 환경에서는 시스템이 "얼마나 많은 일을(TPS), 얼마나 빨리(RT) 처리하는가"가 서비스 생존에 직결됨.
    *   **작동 원리**: TPS는 `단위 시간당 완료된 트랜잭션 수`, 응답시간은 `요청부터 응답까지의 총 체류 시간`. 자원이 여유로울 때는 TPS가 선형 증가하지만, 특정 **임계점(Saturation Point)**을 넘어서면 Queueing Theory에 의해 대기열이 발생, TPS는 정체(Flat)되고 응답시간은 기하급수적(Exponential)으로 폭증함.
    *   **비유**: **고속도로 톨게이트**. TPS는 `1초당 통과하는 차량 수(처리량)`, 응답시간은 `차량이 줄을 서서 요금을 내고 빠져나가는 데 걸린 총 시간(체감 속도)`. 차가 너무 몰리면(병목) 통과 차량 수(TPS)는 늘지 않고 대기 시간(RT)만 길어짐.
    *   **구체 예시**: 블랙프라이데이 이벤트 시, 평소 1,000 TPS / 200ms RT였던 시스템이 5,000 TPS의 부하를 받으면, DB Connection Pool 고갈로 인해 처리량은 2,000 TPS에서 멈추고 RT는 5,000ms 이상으로 치솟음(타임아웃 발생).
    *   **흔한 오해/주의점**: 응답시간을 '평균(Average)'으로만 관리하면 심각한 롱테일(Long-tail) 지연을 놓침. 반드시 **p95, p99 (Percentile)** 등 백분위수를 기준으로 보수적인 성능 기준(SLO)을 잡아야 함.
*   **연결 개념**: 리틀의 법칙(Little's Law), 대기행렬 이론(Queuing Theory), APM, SRE(SLO/SLI), 성능 테스트(Load Testing)

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **깊이 이해** | *   **배경**: 단일 서버 시절엔 CPU/Memory만 봤지만, 분산 환경에서는 시스템이 "얼마나 많은 일을(TPS), 얼마나 빨리(... | "작업 책상" |
| **작동 원리** | TPS는 `단위 시간당 완료된 트랜잭션 수`, 응답시간은 `요청부터 응답까지의 총 체류 시간` | "이 개념의 핵심" |
| **비유** | **고속도로 톨게이트** | "이 개념의 핵심" |
| **흔한 오해/주의점** | 응답시간을 '평균(Average)'으로만 관리하면 심각한 롱테일(Long-tail) 지연을 놓침 | "학습하는 기계" |
| **연결 개념** | 리틀의 법칙(Little's Law), 대기행렬 이론(Queuing Theory), APM, SRE(SLO/SLI), 성능 테스트(Load... | "교통 분산" |
| **본질** | TPS는 **Provider(시스템)** 관점의 처리 한계치, 응답시간(RT)은 **Consumer(사용자)** 관점의 서비스 품질 척도 | "이 개념의 핵심" |
| **가치** | 두 지표의 상관관계 곡선(Performance Curve)을 통해, 시스템의 병목 구간(Bottleneck)과 확장 임계점을 사전 식별 | "이 개념의 핵심" |

---



## 📝 【답안용】 서술 골격

> **💡 핵심 인사이트**
> *   **본질**: TPS는 **Provider(시스템)** 관점의 처리 한계치, 응답시간(RT)은 **Consumer(사용자)** 관점의 서비스 품질 척도.
> *   **가치**: 두 지표의 상관관계 곡선(Performance Curve)을 통해, 시스템의 병목 구간(Bottleneck)과 확장 임계점을 사전 식별.
> *   **판단 포인트**: 평균치가 아닌 극단값(p99) 중심의 분석, 그리고 구간별(Tier) 응답시간 분해(Response Time Breakdown)를 통한 핀포인트 튜닝이 핵심.

### Ⅰ. 시스템 성능의 척도, TPS와 응답시간(RT)의 개요
*   **TPS (Transactions Per Second)**: 1초 동안 시스템이 정상적으로 처리한 비즈니스 트랜잭션의 수 (시스템 처리 용량의 척도).
*   **Response Time (응답시간)**: 클라이언트가 요청을 보낸 시점부터 완전한 응답을 받을 때까지 소요된 총 시간.
*   **목적**: H/W 및 Cloud 리소스 용량 산정(Sizing), 성능 병목(Bottleneck) 탐지, 서비스 수준 협약(SLA) 준수 여부 검증.

### Ⅱ. TPS와 응답시간의 구성 및 수리적 상관관계
*   **응답시간 구성 (RT Breakdown)**: `사용자 체감 응답시간 = Network Latency + Queue Time(WAS 대기) + Service Time(CPU/DB 처리)`
*   **리틀의 법칙 (Little's Law)**: `L(동시 사용자) = λ(TPS) × W(응답시간)` 
*   **의미**: 일정한 응답시간(W)을 유지할 때, 동시 사용자(L)가 늘어나면 처리량(λ)도 비례해야 함. 자원 포화 시 λ가 정체되므로 W가 급증.

### Ⅲ. 부하 증가에 따른 성능 상관 곡선 (Performance Curve)
```text
[TPS 및 RT 상관관계 도식]
  지표 (Value)
   │                           ↗ (RT 기하급수적 급증: Queueing Effect)
   │                         /
   │      TPS (Linear) ──/───→ (TPS 정체: Saturation)
   │                   / │
   │                 /   │
   │               /     │
   │             /       │ (포화점 / 병목 지점)
   └───────────┴─────────┴─────────────→ 부하량 (Active Users / Load)
          Light Load     Heavy Load    
```
*   **Light Load 구간**: 자원이 충분하여 부하 증가에 따라 TPS 선형 증가, RT 일정.
*   **Heavy Load 구간**: 자원(CPU, DB Pool 등) 포화로 인해 Queue가 형성됨. TPS는 한계치에 수렴(Asymptote)하고 RT는 급증.

### Ⅳ. 꼬리 지연(Long-tail Latency) 해결을 위한 Percentile 분석
*   **평균(Average)의 한계**: 1개의 10초짜리 응답이 99개의 10ms 응답에 희석되어 병목을 은폐함.
*   **Percentile 지표 적용**: p95, p99 (상위 95%, 99% 사용자가 경험하는 최대 지연 시간) 지표를 측정.
*   **SRE 프랙티스**: "p99 RT 200ms 미만, 99.9% 가용성" 과 같이 구체적인 SLI/SLO를 설정하여 시스템 신뢰성(Reliability) 확보.

### Ⅴ. 병목 지점 식별 및 엔드투엔드(E2E) 튜닝 방안
*   **티어별(Tier) 분해**:
    *   **Web/WAS**: Thread/Connection Pool 고갈, Heap Memory GC Pause, 소켓 타임아웃 분석.
    *   **DB Layer**: Lock Contention, Slow Query, I/O Wait 분석.
*   **APM 툴 활용**: OpenTelemetry, Pinpoint, Scouter 등을 활용한 Call Stack/Transaction E2E Tracing 및 구간별 Latency 시각화.

### Ⅵ. Cloud-Native 환경에서의 지표 활용 (Auto-Scaling 연동)
*   **Metric-Driven Scaling**: CPU/Memory 단순 임계치를 넘어, Ingress Controller의 TPS 및 In-flight Requests, p95 RT를 HPA(Horizontal Pod Autoscaler) 메트릭으로 활용.
*   **KEDA 연동**: 이벤트 기반 아키텍처에서 Message Queue(Kafka, RabbitMQ)의 Lag 량과 TPS를 연계한 선제적/동적 스케일 아웃 수행.

---

### 🔄 문제 유형별 목차 전환 (실전 팁)
*   **"성능 분석 메커니즘"**을 묻는 문제: Ⅱ·Ⅲ을 통합하여 `[Ⅱ. Little's Law 기반 TPS-응답시간 수리적 상관관계]`, `[Ⅲ. 시스템 포화점(Saturation Point)의 성능 한계 곡선 분석]`으로 수리적/원리적 측면을 깊게 파고듦.
*   **"성능 최적화/모니터링 실무"**를 묻는 문제: Ⅴ·Ⅵ을 전진 배치하여 `[Ⅴ. APM 기반 응답시간 분해(RT Breakdown)와 병목 추적]`, `[Ⅵ. SRE 관점의 Percentile 기반 SLO 모니터링 및 KEDA 연동 방안]`으로 현장 실무 역량을 강력히 어필.
