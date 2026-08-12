---
sidebar:
  order: 161
  label: "161. 클라우드 네이티브 관측성 (Cloud Native Observability)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "클라우드 네이티브 관측성 (Cloud Native Observability)"
date: "2026-08-10T10:00:00+09:00"
tags:
  - "notes-software"
weight: 161
extra:
  question_no: "161"
  source_status: "기출"
  source_history: "135회"
  priority: 70
  priority_note: "로그•지표•추적의 연결 구조 출제"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Cloud-Native Observability (관측성)**: 분산 클라우드 네이티브 아키텍처에서 외부 텔레메트리(Telemetry) 신호인 3대 기둥(Metrics, Logs, Traces)을 통합 렌더링하여 시스템 내부의 복잡한 비정상 상태(Unknown Unknowns) 원인을 추론하고 시각화하는 기술.
- **Metrics, Logs, Traces (Observability 3 Pillars)**: 수치 집계(Metrics), 이벤트 기록(Logs), 분산 엔드-투-엔드 이동 경로(Traces)의 3대 핵심 텔레메트리 데이터.
- **OpenTelemetry (OTel)**: 메트릭, 로그, 트레이스 데이터를 수집/표준화하기 위한 CNCF 산하의 글로벌 텔레메트리 표준 오픈소스 프로젝트.

</details>

- 정의/개념: 분산 마이크로서비스 환경에서 발생되는 Metrics(지표), Logs(로그), Traces(추적) 3대 텔레메트리 신호를 단일 Trace ID로 바인딩 상호 연동하여 장애 근본 원인을 초고속 추적하는 시스템 능력인 **Cloud-Native Observability**
- 배경/필요성: 수백 개 MSA 서비스와 K8s pod 간 얽히고설킨 장애 발생 시 단순 서버 모니터링(Monitoring) 수준으로는 "왜 서비스가 멈췄는지" 원인 추론 불가능 극복 요구성

#### 한줄 요약

- 결제 지연 그래프에서 느린 요청 하나를 골라 호출 경로와 같은 식별자의 오류 기록을 따라가면 어느 서비스에서 왜 늦어졌는지 좁힐 수 있다.

## Ⅱ. 특징 (Observability 3대 기둥 및 통합 파이프라인)

<details><summary>핵심 용어</summary>

- **Trace ID Correlation**: 모든 로그 및 메트릭에 동일한 `trace_id: 8f9a2b...` 코드를 자동 주입하여 로그와 트레이스를 단 1클릭으로 대조 추적.

</details>

- **Metrics (Prometheus 기반 CPU/RAM/QPS 시각화 및 이상 징후 알림)**
- **Logs (Loki / Fluentbit 기반 구조화 JSON 로그 및 상세 오류 문맥 파악)**
- **Traces (Jaeger / Tempo 기반 분산 서비스 간 HTTP 호출 병목 핑퐁 추적)**

#### 한줄 요약

- 모든 기록을 모으는 대신 사용자가 겪은 실패를 어떤 신호로 찾고 어떤 공통 키로 원인까지 이동할지 먼저 정하는 방식이다.

## Ⅲ. 구조 및 구성요소 (Observability 3대 기둥 및 OTel Collector 아키텍처)

<details><summary>핵심 용어</summary>

- **OpenTelemetry Collector**: Receiver(수집) $\rightarrow$ Processor(배치/마스킹) $\rightarrow$ Exporter(전송) 3단계 구조로 텔레메트리 신호를 처리하는 중앙 수집 엔진.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│               Cloud-Native Observability Architecture                  │
├────────────────────────────────────────────────────────────────────────┤
│ [App / K8s Pods] ──► [OpenTelemetry Agent (Auto-Instrumentation)]     │
│                             │ (Metrics / Logs / Traces)                │
│                             ▼                                          │
│ [OpenTelemetry Collector] ──► Receiver ──► Processor ──► Exporter      │
│                             │                                          │
│         ┌───────────────────┼───────────────────┐                      │
│         ▼                   ▼                   ▼                      │
│ [Prometheus (Metrics)] [Loki / ES (Logs)] [Jaeger / Tempo (Traces)]    │
│         └───────────────────┬───────────────────┘                      │
│                             ▼                                          │
│                  [Grafana Unified Dashboard]                           │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: OTel Collector를 통해 수집된 3대 텔레메트리가 각각의 전용 저장소로 저장된 후 Grafana 단일 뷰 대시보드로 통합 연동되는 아키텍처.

| 관측성 3대 기둥 (Pillar) | 핵심 역할 및 기술 메커니즘 | 대표 기술 스택 도구 |
|:---|:---|:---|
| **1. Metrics (지표)** | **시간 흐름에 따른 수치 집계 (CPU %, QPS, 500 Error Count)**| **Prometheus, Datadog** |
| **2. Logs (로그)** | **이벤트 발생 시점의 상세 텍스트/JSON 문맥 기록** | **Grafana Loki, Fluentbit, ELK** |
| **3. Traces (추적)** | **유저 1개 요청이 수십 개 MSA를 거쳐가는 구간별 Latency**| **Jaeger, Grafana Tempo, Zipkin** |

#### 한줄 요약

- 각 서비스가 단서를 만들고 문맥 전파가 같은 사건 번호를 붙이면 수집기와 저장소를 거쳐 분석 화면에서 하나의 장애 이야기로 재구성된다.

## Ⅳ. 흐름도 (Trace ID 바인딩 3-Pillar 장애 추적 흐름)

<details><summary>핵심 용어</summary>

- **Context Propagation**: W3C Trace Context 표준(`traceparent` 헤더)을 HTTP 요청 헤더에 실어 다음 마이크로서비스로 전파(Propagate)하는 기법.

</details>

```text
[Grafana Alert: 500 Error Spike] ──► [Click Metric Spike (Prometheus)]
                                                 │
                                                 ▼ (Trace ID Jump)
 [Check Specific Error Log (Loki)] ◄── [Click Slow Trace Span (Tempo)]
```

### 동작 원리

1. **Alert & Metric**: Grafana에서 결제 500 에러 스파이크 메트릭 알림 감지.
2. **Trace Jump**: 해당 메트릭 클릭 시 유입된 특정 Trace ID의 Jaeger 트레이스 맵으로 이동하여 `Payment-Service`가 3초간 멈춘 병목 지점 발견.
3. **Log Drilldown**: 동일 Trace ID로 Loki 로그를 1초 만에 드라이브다운 검색하여 `Database Connection Timeout` 원인 확정 (**Observability 완결**).

#### 한줄 요약

- 주문 요청이 결제와 재고를 거치는 동안 같은 추적 식별자를 전달하면 세 서비스의 지연과 오류가 한 호출 경로로 묶인다.

## Ⅴ. 종류 및 비교 (전통적 Monitoring 대 Cloud-Native Observability)

<details><summary>핵심 용어</summary>

- **Known Knowns vs Unknown Unknowns**: 모니터링은 이미 알고 있는 장애(CPU 90% 이상)를 체크, 관측성은 원인을 전혀 모르는 복잡한 장애(Unknown Unknowns)를 추론.

</details>

| 비교 항목 | Traditional Monitoring (모니터링) | Cloud-Native Observability (관측성) |
|:---|:---|:---|
| **핵심 질문** | **"시스템이 지금 정상인가?" (Known)**| **"왜 3번째 MSA 서비스에서 멈췄는가?" (Unknown)**|
| **수집 데이터** | 단일 인프라 CPU/RAM 메트릭 위주 | **Metrics + Logs + Traces 3대 기둥 100% 통합** |
| **상관 관계 (Correlation)**| 파편화 (메트릭 툴과 로그 툴이 분리됨)| **Trace ID 기반 3대 데이터 1클릭 교차 점프** |
| **시스템 복잡도**| 단일 모놀리식 서버에 적합 | **수백 개 MSA & Kubernetes 환경 필수** |

#### 한줄 요약

- 메트릭으로 언제 나빠졌는지 찾고 추적로 느린 구간을 고른 뒤 로그에서 그 시점의 오류와 입력 문맥을 확인한다.

## Ⅵ. 실무 고려사항 및 대책 (Observability 실무 3대 파행 대책)

<details><summary>핵심 용어</summary>

- **High Cardinality Cost Explosion**: Log 및 Metric 라벨에 `user_id`, `email` 같은 수백만 개의 고유값을 함부로 넣었다가 저장소 디스크 및 비용이 폭발하는 안티패턴.

</details>

| 3대 관측성 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. High Cardinality Costs**| Metric 라벨에 user_id 넣어서 비용 폭발| **High-cardinality 지표는 Log로 이관 정제** |
| **2. Trace Data Overload** | 하루 수억 건 트레이스 저장 시 디스크 고갈| **Tail-based Sampling 적용 (성공 1%, 에러 100% 저장)**|
| **3. Vendor Lock-in** | 특정 APM (Dynatrace, Datadog) SDK 종속 | **OpenTelemetry (OTel) 표준 SDK로 전면 통일** |

> 사례: **토스 / 당근마켓 / 쿠팡 OpenTelemetry & Prometheus & Loki & Tempo 기반 통합 관측성 구축**

#### 한줄 요약

- 사용자 식별자를 메트릭 속성으로 모두 넣지 말고 오류 요청의 추적와 로그에서만 찾도록 나누면 경보 비용과 진단 단서를 함께 관리할 수 있다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Observability 수립 기준(Observability Standards)**: OpenTelemetry 표준, 3-Pillar(Prometheus+Loki+Tempo), Trace ID Correlation 및 Tail-based Sampling에 의거한 체계.

</details>

- **Observability 수립 기준**에 따라 차세대 MSA 구축 시 **Cloud-Native Observability & OpenTelemetry** 필수 적용

#### 한줄 요약

- SLO 이상에서 대표 추적와 같은 식별자의 로그까지 이동할 수 있는 신호만 남기고 원인 분석에 쓰이지 않는 수집량은 줄여야 한다.
