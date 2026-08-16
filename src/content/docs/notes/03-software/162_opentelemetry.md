---
sidebar:
  order: 162
  label: "162. OpenTelemetry (OpenTelemetry)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "OpenTelemetry (OpenTelemetry)"
date: "2026-08-14T02:40:00+09:00"
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

<details><summary>용어 설명</summary>

- **오픈텔레메트리(OpenTelemetry, OTel)**: 메트릭, 로그, 트레이스를 표준화된 OTLP 프로토콜로 수집·전송하는 벤더 중립적 계측 프레임워크.
- **OTLP (OpenTelemetry Protocol)**: gRPC 및 HTTP Protobuf 기반의 텔레메트리 데이터 전송 표준 프로토콜.
- **OTel 컬렉터(Collector)**: 데이터를 수집(Receiver), 가공(Processor), 전송(Exporter)하는 파이프라인 구조의 텔레메트리 중계 엔진.

</details>

- 정의/개념: Telemetry 생성•수집•전송 표준인 **OpenTelemetry**
- 배경/필요성: 공급자별 SDK는 Backend 변경 때 **계측 재작성•Signal 분절** 유발

#### 한줄 요약

- 여러 언어가 서로 다른 상자에 담던 관측 데이터를 같은 규격으로 포장하면 분석 도구를 바꿔도 애플리케이션 계측을 다시 만들 필요가 줄어든다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Vendor-Neutral Standard**: 애플리케이션에는 OTel SDK만 탑재하고, 백엔드 저장소(Jaeger $\rightarrow$ Datadog)를 바꿔도 코드 수정 0회 달성.

</details>

- **벤더 중립**: 단일 OTel SDK로 Datadog, Jaeger, Prometheus 등 백엔드 유연성 확보.
- **통합 API(Unified Telemetry API)**: Metrics, Logs, Traces 3대 데이터의 통합 수집 표준화.
- **자동 계측**: 코드 수정 없는 Java Agent 및 라이브러리 훅 기반 자동 데이터 수집.

#### 한줄 요약

- 애플리케이션은 표준 신호만 만들고 필터, 배치, 재시도, 다중 백엔드 전송은 컬렉터에 맡겨 업무 코드와 전송 정책을 분리한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **OTel API vs SDK vs Collector**: API는 코드상 계측 인터페이스, SDK는 실제 수집 구현체, Collector는 중앙 수집/전송 엔진.

</details>

```text
[OpenTelemetry]
 ├── [API]
 ├── [SDK]
 ├── [OTLP]
 └── [Collector]
```

| 구성요소 | 책임 |
|---|---|
| API | Application 계측의 **언어별 Interface** 제공 |
| SDK | Signal 생성•Sampling•Batch와 **Context 전파** 구현 |
| OTLP | Telemetry의 **직렬화•전송 규격** 제공 |
| Collector | **Receiver•Processor•Exporter** Pipeline 실행 |

#### 한줄 요약

- 계측기가 화물을 만들고 SDK가 포장하면 OTLP라는 운송 규격으로 컬렉터 물류센터를 거쳐 분석 저장소에 도착한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **OTel Collector Pipeline**: Receiver(OTLP 수집) $\rightarrow$ Processor(PII 마스킹/메모리 제한) $\rightarrow$ Exporter(Jaeger/Datadog 전송).

</details>

```text
[Telemetry 입력]
      │
      ▼
1. Receiver 수신
      │
      ▼
2. Resource•Context 보강
      │
      ▼
3. Filter•Masking•Sampling
      │
      ▼
4. Batch•Memory 제한
      │
      ▼
5. Exporter 전송
      │
      ▼
[Backend 저장]
```

### 동작 원리

1. **Receiver 수신**: OTLP 등 입력 Protocol 처리
2. **Resource•Context 보강**: Service•환경 Attribute 부착
3. **Filter•Masking•Sampling**: 민감 정보와 수집량 통제
4. **Batch•Memory 제한**: 전송 효율과 Buffer 상한 관리
5. **Exporter 전송**: Signal별 Backend로 전달

#### 한줄 요약

- 결제 서비스의 추적과 로그는 SDK에서 묶여 컬렉터로 가고 그곳에서 개인정보가 제거된 뒤 추적·로그 저장소에 각각 전달된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **OTel Collector DaemonSet vs Deployment**: Node 마다 설치하는 Agent 방식과 중앙 전용 서버로 띄우는 Gateway 방식.

</details>

| 비교 항목 | OTel Collector Agent Mode (DaemonSet) | OTel Collector Gateway Mode (Deployment) |
|:---|:---|:---|
| 배치 위치 | **K8s 모든 Worker Node마다 1개씩 탑재** | **중앙 전용 K8s Pod 또는 EC2 배치** |
| 핵심 목적 | **Node 내부 Pod 들의 트레이스를 초저지연 수집**| **전사 텔레메트리 중앙 집중 PII 마스킹 및 전송**|
| 추천 구성 | **Agent (1차 수집) $\rightarrow$ Gateway (2차 마스킹/전송) 2단 혼용 아키텍처** |

#### 한줄 요약

- 단일 분석 도구의 작은 환경은 직접 전송이 단순하지만 여러 팀의 정책과 목적지를 통일하려면 컬렉터 경유가 변경 범위를 줄인다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Auto-Instrumentation Performance Impact**: Java Agent 등의 자동 계측 도구가 앱 부팅 시 CPU/Memory 사용량을 소폭 증가시키는 현상.

</details>

| 3대 OpenTelemetry 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| 1. Agent CPU Overhead | Java Auto-Instrumentation 과다 수집| **수집 범위를 HTTP/DB 쿼리로 한정 튜닝** |
| 2. PII Leak in Traces | HTTP Header의 Bearer Token이 Trace 유출 | **OTel Collector Processor에서 헤더 삭제**|
| 3. OTel Collector OOM | 트래픽 폭증 시 Collector 메모리 파산 | **`memory_limiter` 및 `batch` 프로세서 필수 설정**|

> 사례: **토스 / 당근마켓 / 쿠팡 OpenTelemetry 표준 채택 및 Datadog/Jaeger 이중 전송 시스템**

#### 한줄 요약

- 백엔드가 멈췄을 때 컬렉터의 대기열이 무한히 메모리를 쓰지 않도록 상한과 디스크 보존을 두고 자체 상태도 별도 경보로 감시해야 한다.

## Ⅶ. 결론

- Node 수집은 **Agent**, 중앙 정책•다중 전송은 Gateway 배치

#### 한줄 요약

- 애플리케이션에는 표준 계측만 두고 수집량•민감 정보•목적지 정책은 Collector에서 관리한다.
