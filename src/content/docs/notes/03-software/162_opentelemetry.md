---
sidebar:
  order: 162
  label: "162. OpenTelemetry (OpenTelemetry)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "OpenTelemetry (OpenTelemetry)"
date: "2026-08-18T02:20:00+09:00"
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

- **오픈텔레메트리(OpenTelemetry, OTel)**: 메트릭, 로그, 분산 추적(Traces)을 단일화된 표준 API/SDK와 OTLP(OpenTelemetry Protocol)로 수집·가공·전송하는 CNCF 벤더 중립적 표준 프레임워크.
- **모니터링 벤더 종속 및 계측 파편화(Vendor Lock-in & Instrumentation Fragmentation)**: 상용 APM(Datadog, Dynatrace) 벤더별 전용 SDK 사용으로 인해 백엔드 교체 시 소스코드 재작성 부담과 텔레메트리 데이터 분절 위험.

</details>

- 정의/개념: 벤더 종속 없이 메트릭, 로그, 트레이스를 단일화하여 **OTLP 프로토콜로 수집·가공·전송하는 클라우드 네이티브 계측 표준** 프레임워크
- 배경/필요성: 상용 모니터링 벤더별 전용 SDK 파편화로 인한 **백엔드 교체 시 계측 코드 전면 재작성 부담 및 텔레메트리 데이터 분절 위험** 직면

#### 한줄 요약

- 단일 OTel 표준 SDK와 수집기(Collector)를 통해 애플리케이션 코드 수정 없이 다중 분석 백엔드로 관측 데이터를 라우팅

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **OTLP(OpenTelemetry Protocol)**: gRPC 및 HTTP Protobuf 기반의 초고속·경량 텔레메트리 데이터 직렬화 전송 표준 프로토콜.
- **파이프라인 아키텍처(Collector Pipeline)**: 수신(Receiver) $\to$ 가공(Processor) $\to$ 전송(Exporter)의 3단계 모듈형 구조.

</details>

- 백엔드 교체 시에도 애플리케이션 코드 변경 0회를 보장하는 **완전한 벤더 중립성**
- Java Agent, eBPF 등을 통한 무수정 **자동 계측(Auto-Instrumentation) 지원**
- PII 마스킹, 샘플링, 다중 백엔드 라우팅을 전담하는 **OTel Collector 파이프라인**

#### 한줄 요약

- 표준화된 API/SDK와 중앙 수집기를 분리하여 관측성 데이터의 생성과 전송 정책을 완벽히 격리

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **OTel 4대 핵심 구조**: API(명세 인터페이스), SDK(구현체/버퍼링), OTLP(전송 프로토콜), Collector(수집/가공/내보내기 엔진).

</details>

```text
[ OpenTelemetry 핵심 아키텍처 및 수집 파이프라인 ]

 1. [ 애플리케이션 계층 (Application Instrumentation) ]
    ┌─────────────────────────────────────────────────────────────┐
    │  • OTel API (추상화 계측 인터페이스)                         │
    │  • OTel SDK (Context 전파, Trace ID 생성, 인메모리 버퍼링)  │
    └────────────────────────────┬────────────────────────────────┘
                                 │ (OTLP / gRPC: Port 4317)
                                 ▼
 2. [ 오픈텔레메트리 수집기 (OTel Collector) ]
    ┌─────────────────────────────────────────────────────────────┐
    │ • Receivers:  OTLP, Zipkin, Jaeger, Prometheus 신호 수신    │
    │ • Processors: PII 토큰 마스킹, Batching, Memory Limiter     │
    │ • Exporters:  Tempo, Loki, Prometheus, Datadog 전송        │
    └────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
 3. [ 백엔드 저장소 (Prometheus / Tempo / Loki / Datadog) ]
```

선의 의미: OTel SDK가 생성한 OTLP 신호가 OTel Collector의 3단계 파이프라인을 거쳐 다중 백엔드로 전송되는 구조.

| 구성요소 | 책임 |
|:---|:---|
| OTel API (명세 인터페이스)| 애플리케이션 코드에서 **메트릭과 스팬을 생성하기 위한 벤더 독립적 인터페이스 제공** |
| OTel SDK (계측 구현체) | Context 전파, 샘플링, 배치 버퍼링을 수행하고 **OTLP 패킷으로 직렬화 전송** |
| OTel Collector | Receiver, Processor, Exporter 파이프라인을 통해 **데이터 가공 및 다중 백엔드 라우팅** |
| OTLP (전송 프로토콜) | Protobuf 기반으로 **메트릭, 로그, 트레이스를 효율적으로 압축 직렬화하여 전송** |

#### 한줄 요약

- OTel API, OTel SDK, OTLP 프로토콜, OTel Collector가 결합하여 벤더 중립적 관측성을 구현

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **OTel Collector 데이터 가공 5단계 파이프라인**: 수신(Receiver) $\to$ 컨텍스트 보강 $\to$ 필터/마스킹 $\to$ 배치 버퍼링 $\to$ 전송(Exporter).

</details>

```text
[ OpenTelemetry Collector 파이프라인 처리 흐름도 ]

 ┌────────────────────────────────────────┐
 │ 1. Receiver: OTLP gRPC 텔레메트리 수신  │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 2. Processor: 서비스명/환경 Attribute 보강│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 3. Processor: PII 개인정보/토큰 마스킹 │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 4. Processor: Batching 및 메모리 상한 제어│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 5. Exporter: 다중 백엔드 저장소 병렬 전송│
 └────────────────────────────────────────┘
```

### 동작 원리

1. 신호 수신: Receiver 모듈이 애플리케이션들로부터 포트 4317을 통해 OTLP gRPC 패킷을 접수.
2. 메타 보강: Processor가 K8s 파드 이름, 네임스페이스, 배포 버전(`service.version`) 라벨을 자동 주입.
3. 보안 가공: 정규표현식 필터를 통해 HTTP Authorization 헤더 및 주민번호 등 민감정보(PII)를 자동 마스킹.
4. 배치 제어: `batch` 및 `memory_limiter` 프로세서를 통해 메모리 고갈(OOM)을 방지하며 묶음 단위로 패킹.
5. 저장소 전송: Exporter가 가공된 메트릭은 Prometheus로, 트레이스는 Tempo로, 로그는 Loki로 병렬 전송.

#### 한줄 요약

- OTLP 수신 $\to$ 메타 보강 $\to$ PII 마스킹 $\to$ 배치 제어 $\to$ 다중 전송의 5단계

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Agent Mode vs Gateway Mode**: 워커 노드마다 데몬셋으로 띄우는 Agent 방식과 중앙 전용 클러스터로 띄우는 Gateway 방식.

</details>

| 구분 | 에이전트 모드 (Agent: DaemonSet) | 게이트웨이 모드 (Gateway: Deployment) |
|:---|:---|:---|
| **적용 기준** | 노드 내부 로컬 파드들의 트레이스를 초저지연 수집하는 환경 | 전사 트레이스 집계, 중앙 PII 마스킹, 외부 SaaS 전송 환경 |
| **핵심 특징** | **K8s Worker Node마다 1개씩 탑재, 로컬 통신 오버헤드 최소** | **중앙 집중형 스케일아웃, 단일 외부 방화벽 출구, 고도화 가공** |
| **한계** | 노드별 메모리 사용량 증가 및 중앙 집중 정책 제어 복잡 | 게이트웨이 장애 시 전사 텔레메트리 수집 일시 정체 위험 |

#### 한줄 요약

- 로컬 1차 수집은 Agent 모드, 중앙 2차 가공 및 전송은 Gateway 모드를 조합(2-Tier)하여 운영

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **메모리 리미터(Memory Limiter)**: 트래픽 급증 시 OTel Collector가 메모리 부족(OOM)으로 다운되는 것을 막기 위해 임계치 초과 시 데이터를 일시 드롭하는 안전장치.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 트레이스 스팬 내 Bearer Token 등 민감정보(PII) 유출 | **Collector Processor에서 `attributes/insert` 및 헤더 삭제 정제** | 보안 컴플라이언스 100% 준수 |
| 트래픽 폭증 시 OTel Collector 프로세스 OOM 비정상 종료 | **`memory_limiter` 및 `batch` 프로세서 파이프라인 필수 배치** | 수집기 무중단 안정성 확보 |
| Java Auto-Instrumentation 과다 수집으로 인한 앱 CPU 저하 | **계측 스코프를 HTTP 엔드포인트 및 DB 쿼리 메서드로 한정** | 앱 CPU 오버헤드 3% 미만 유지 |

#### 한줄 요약

- PII 마스킹, 메모리 리미터 적용, 계측 스코프 최적화를 통해 OTel 파이프라인의 안정성을 확보

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **텔레메트리 데이터 메시(Telemetry Data Mesh)**: OTel 표준을 통해 수집된 관측성 데이터를 전사 AI 분석 엔진 및 FinOps 플랫폼과 연계하는 차세대 거버넌스.

</details>

- **OpenTelemetry**는 클라우드 네이티브 관측성의 단일 표준 규격이며, 2-Tier 수집기 아키텍처와 메모리 제어 프로세서를 결합하여 벤더 비종속적이고 안정적인 엔터프라이즈 관측 인프라를 구축해야 함

#### 한줄 요약

- 단일 표준 SDK와 3단계 Collector 파이프라인을 통해 벤더 독립적 통합 관측성을 완성
