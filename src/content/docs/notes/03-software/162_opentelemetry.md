---
sidebar:
  order: 162
  label: "162. OpenTelemetry (OpenTelemetry)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "OpenTelemetry (OpenTelemetry)"
date: "2026-08-10T10:00:00+09:00"
tags:
  - "notes-software"
weight: 162
extra:
  question_no: "162"
  source_status: "기출"
  source_history: "135회"
  priority: 70
  priority_note: "관측 신호 수집 표준의 구조와 적용 출제"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **OpenTelemetry (OTel / 오픈텔레메트리)**: CNCF의 2위 인기 오픈소스 프로젝트로, 이종의 관측성 툴(Datadog, New Relic, Jaeger, Prometheus)에 묶이지 않고 Metrics, Logs, Traces 텔레메트리 데이터를 표준화된 OTLP 프로토콜로 수집 전송하는 글로벌 표준 계측 프레임워크.
- **OTLP (OpenTelemetry Protocol)**: gRPC / HTTP Protobuf 기반의 초경량 텔레메트리 전송 표준 프로토콜.
- **OTel Collector**: Receiver(수집), Processor(가공/마스킹), Exporter(전송) 파이프라인으로 구성되어 이종의 APM 벤더(Datadog, Jaeger)로 텔레메트리를 다중 전송하는 프록시 서비스.

</details>

- 정의/개념: 특정 APM 상용 벤더(Datadog, Dynatrace) 종속성(Vendor Lock-in)을 0% 탈피하고, 벤더 중립적(Vendor-Neutral)인 OTLP 표준 프로토콜로 메트릭, 로그, 트레이스를 수집 및 전송하는 글로벌 텔레메트리 프레임워크인 **OpenTelemetry (OTel)**
- 배경/필요성: APM 상용 툴을 교체할 때마다 소스코드 내 SDK를 전면 재작성해야 하는 파행 예방, 이중 모니터링 툴 사용 시 데이터 수집 파편화 차단 요구성

#### 한줄 요약

- 여러 언어가 서로 다른 상자에 담던 관측 데이터를 같은 규격으로 포장하면 분석 도구를 바꿔도 애플리케이션 계측을 다시 만들 필요가 줄어든다.

## Ⅱ. 특징 (OpenTelemetry 3대 핵심 혜택)

<details><summary>핵심 용어</summary>

- **Vendor-Neutral Standard**: 애플리케이션에는 OTel SDK만 탑재하고, 백엔드 저장소(Jaeger $\rightarrow$ Datadog)를 바꿔도 코드 수정 0회 달성.

</details>

- **Vendor Agnostic (단일 OTel SDK로 Datadog, Jaeger, Prometheus 백엔드 100% 지원)**
- **Unified Telemetry API & SDK (Metrics, Logs, Traces 3대 기둥 통합 수집 표준)**
- **Auto-Instrumentation (코드 수정 없이 Java Agent / Node.js 훅으로 자동 계측)**

#### 한줄 요약

- 애플리케이션은 표준 신호만 만들고 필터, 배치, 재시도, 다중 백엔드 전송은 컬렉터에 맡겨 업무 코드와 전송 정책을 분리한다.

## Ⅲ. 구조 및 구성요소 (OTel 3대 계층 파이프라인 아키텍처)

<details><summary>핵심 용어</summary>

- **OTel API vs SDK vs Collector**: API는 코드상 계측 인터페이스, SDK는 실제 수집 구현체, Collector는 중앙 수집/전송 엔진.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   OpenTelemetry Standard Architecture                  │
├────────────────────────────────────────────────────────────────────────┤
│ [App (Java/Go/Node)] ──► OTel API & SDK (Auto-Instrumentation)        │
│                               │ (OTLP Protocol over gRPC / HTTP)       │
│                               ▼                                        │
│ [OTel Collector Engine] ──► Receiver ──► Processor ──► Exporter        │
│                                                          │             │
│         ┌────────────────────────────────────────────────┤             │
│         ▼                                                ▼             │
│ [Jaeger / Tempo (Traces)]                       [Prometheus (Metrics)] │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: App 코드가 OTel SDK 및 OTLP 프로토콜로 OTel Collector에 전송 후 Receiver, Processor, Exporter를 타고 다중 백엔드로 분기 전송되는 구조.

| 구성요소 (Element) | 역할 및 기술 메커니즘 | 실무 적용 포인트 |
|:---|:---|:---|
| **OTel API** | **앱 코드상에서 Trace/Metric 수집을 위한 언어별 표준 규약**| `tracer.startSpan()` |
| **OTel SDK** | **API 구체 구현체, 메모리 버퍼링 및 Batch Processor 처리** | `BatchSpanProcessor` |
| **OTLP Protocol** | **Protobuf gRPC/HTTP 기반 초경량 텔레메트리 직렬화 전송** | `otlp/grpc:4317` 포트 |
| **OTel Collector** | **중앙 수집 프록시 (Receiver $\rightarrow$ Processor $\rightarrow$ Exporter)**| PII 개인정보 마스킹 파이프라인 |

#### 한줄 요약

- 계측기가 화물을 만들고 SDK가 포장하면 OTLP라는 운송 규격으로 컬렉터 물류센터를 거쳐 분석 저장소에 도착한다.

## Ⅳ. 흐름도 (OTel Collector 3단계 Pipeline 가공 흐름)

<details><summary>핵심 용어</summary>

- **OTel Collector Pipeline**: Receiver(OTLP 수집) $\rightarrow$ Processor(PII 마스킹/메모리 제한) $\rightarrow$ Exporter(Jaeger/Datadog 전송).

</details>

```text
[App OTLP Output] ──► [Receiver: otlp] ──► [Processor: memory_limiter & attributes (PII Masking)]
                                                                     │
                                                                     ▼
 [Datadog & Jaeger Systems] ◄── [Exporter: datadog & otlphttp] ──────┘
```

### 동작 원리

1. **Receiver**: `otlp` 리시버가 Port 4317로 gRPC 텔레메트리 데이터 수신.
2. **Processor**: `memory_limiter`가 메모리 오버헤드를 막고, `attributes` 가 주민번호/카드번호 PII 정규식 마스킹.
3. **Exporter**: 가공된 깔끔한 트레이스를 Jaeger와 Datadog 2곳으로 동시에 다중 전송 (**OTel Pipeline 완결**).

#### 한줄 요약

- 결제 서비스의 추적과 로그는 SDK에서 묶여 컬렉터로 가고 그곳에서 개인정보가 제거된 뒤 추적·로그 저장소에 각각 전달된다.

## Ⅴ. 종류 및 비교 (Agent Mode 대 Deployment Gateway Mode)

<details><summary>핵심 용어</summary>

- **OTel Collector DaemonSet vs Deployment**: Node 마다 설치하는 Agent 방식과 중앙 전용 서버로 띄우는 Gateway 방식.

</details>

| 비교 항목 | OTel Collector Agent Mode (DaemonSet) | OTel Collector Gateway Mode (Deployment) |
|:---|:---|:---|
| **배치 위치** | **K8s 모든 Worker Node마다 1개씩 탑재** | **중앙 전용 K8s Pod 또는 EC2 배치** |
| **핵심 목적** | **Node 내부 Pod 들의 트레이스를 초저지연 수집**| **전사 텔레메트리 중앙 집중 PII 마스킹 및 전송**|
| **추천 구성** | **Agent (1차 수집) $\rightarrow$ Gateway (2차 마스킹/전송) 2단 혼용 아키텍처** |

#### 한줄 요약

- 단일 분석 도구의 작은 환경은 직접 전송이 단순하지만 여러 팀의 정책과 목적지를 통일하려면 컬렉터 경유가 변경 범위를 줄인다.

## Ⅵ. 실무 고려사항 및 대책 (OpenTelemetry 3대 실무 지침)

<details><summary>핵심 용어</summary>

- **Auto-Instrumentation Performance Impact**: Java Agent 등의 자동 계측 도구가 앱 부팅 시 CPU/Memory 사용량을 소폭 증가시키는 현상.

</details>

| 3대 OpenTelemetry 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Agent CPU Overhead** | Java Auto-Instrumentation 과다 수집| **수집 범위를 HTTP/DB 쿼리로 한정 튜닝** |
| **2. PII Leak in Traces** | HTTP Header의 Bearer Token이 Trace 유출 | **OTel Collector Processor에서 헤더 삭제**|
| **3. OTel Collector OOM** | 트래픽 폭증 시 Collector 메모리 파산 | **`memory_limiter` 및 `batch` 프로세서 필수 설정**|

> 사례: **토스 / 당근마켓 / 쿠팡 OpenTelemetry 표준 채택 및 Datadog/Jaeger 이중 전송 시스템**

#### 한줄 요약

- 백엔드가 멈췄을 때 컬렉터의 대기열이 무한히 메모리를 쓰지 않도록 상한과 디스크 보존을 두고 자체 상태도 별도 경보로 감시해야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **OpenTelemetry 수립 기준(OTel Standards)**: OTLP 표준 프로토콜, OTel Collector DaemonSet/Gateway, PII Processor 마스킹 및 Auto-Instrumentation에 의거한 체계.

</details>

- **OpenTelemetry 수립 기준**에 따라 전사 관측성 인프라 수립 시 **OpenTelemetry & OTLP & OTel Collector** 필수 적용

#### 한줄 요약

- 작은 단일 환경은 SDK 직접 전송으로 시작하되 공통 처리와 다중 목적지가 필요해지면 컬렉터를 이중화해 계측 코드와 전송 정책을 분리해야 한다.
