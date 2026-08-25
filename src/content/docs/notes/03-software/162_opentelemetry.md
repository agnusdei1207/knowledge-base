---
sidebar:
  order: 162
  label: "162. OpenTelemetry"
  badge:
    text: "기출 · 70%"
    variant: note
title: "OpenTelemetry (OpenTelemetry)"
date: "2026-08-25T11:00:00+09:00"
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

- **OpenTelemetry(OTel)**: Metrics, Logs, Traces를 벤더 중립적으로 생성·수집·가공·전송하기 위한 CNCF 표준 오픈소스 프레임워크.
- **OTLP(OpenTelemetry Protocol)**: gRPC 및 HTTP 기반 Protobuf로 텔레메트리 데이터를 고속 압축 직렬화하여 전송하는 표준 프로토콜.

</details>

- 정의/개념: 메트릭, 로그, 분산 추적을 단일화하여 **OTLP 프로토콜로 수집·가공·전송하는 CNCF 벤더 중립적 표준 관측성 계측 프레임워크**
- 배경/필요성: 상용 모니터링 벤더별 전용 SDK 파편화로 인한 **백엔드 교체 시 소스코드 전면 재작성 부담 및 텔레메트리 데이터 분절 해결 불가**

#### 한줄 요약
- 단일 OTel 표준 SDK와 Collector로 코드 수정 없이 다중 분석 백엔드로 관측 데이터를 라우팅한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Auto-Instrumentation**: 소스코드 수정 없이 Java Agent 바이트코드 조작이나 eBPF를 통해 HTTP, DB 호출을 자동 계측.
- **Collector Pipeline**: 수신(Receiver) $\to$ 가공(Processor) $\to$ 전송(Exporter) 3단계로 구성된 모듈형 텔레메트리 가공 파이프라인.

</details>

- 백엔드 교체 시에도 애플리케이션 코드 수정을 배제하는 **완전한 벤더 중립성**
- Java Agent 등을 통한 소스코드 무수정 **자동 계측(Auto-Instrumentation)**
- PII 마스킹, 샘플링, 다중 백엔드 전송을 전담하는 **OTel Collector 파이프라인**

#### 한줄 요약
- 벤더 중립성, 무수정 자동 계측, 3단계 수집기 파이프라인을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **OTel 3대 핵심 아키텍처**: App Instrumentation(OTel API/SDK), Collector Layer(Receiver/Processor/Exporter), Backend Storage.

</details>

```text
[OpenTelemetry 핵심 아키텍처 및 수집 파이프라인]
|-- 1. Application Layer (OTel Instrumentation)
|   |-- OTel API (벤더 비종속 계측 추상화 인터페이스)
|   `-- OTel SDK (W3C traceparent 전파, 인메모리 버퍼링 및 OTLP 직렬화)
`-- 2. OpenTelemetry Collector Layer (OTLP gRPC: Port 4317)
    |-- Receivers: OTLP, Zipkin, Jaeger, Prometheus 신호 수신
    |-- Processors: PII 토큰 마스킹, Batching, Memory Limiter 상한 제어
    `-- Exporters: Prometheus, Tempo, Loki, Datadog 다중 백엔드 라우팅
`-- 3. Telemetry Backend Layer (Prometheus / Tempo / Loki / Grafana)
```

선의 의미: 계층 및 OTel SDK가 생성한 OTLP 신호가 OTel Collector의 3단계 파이프라인을 거쳐 다중 백엔드로 전송되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **OTel API (인터페이스)** | 애플리케이션 코드에서 **메트릭과 스팬을 생성하기 위한 벤더 독립적 인터페이스 제공**| 무의존성 명세 |
| **OTel SDK (구현체)** | Context 전파, 샘플링, 배치 버퍼링을 수행하고 **OTLP 패킷으로 직렬화 전송** | 런타임 바인딩 |
| **OTel Collector (수집기)**| Receiver, Processor, Exporter 파이프라인을 통해 **데이터 가공 및 다중 백엔드 라우팅**| 독립 프록시 데몬 |
| **OTLP (전송 프로토콜)** | Protobuf 기반으로 **메트릭, 로그, 트레이스를 효율적으로 압축 직렬화하여 전송** | gRPC Port 4317 |

#### 한줄 요약
- OTel API, OTel SDK, OTLP 프로토콜, OTel Collector가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Collector 처리 5단계**: OTLP 패킷 수신 $\to$ K8s 메타데이터 보강 $\to$ PII 마스킹 $\to$ 배치 및 메모리 제어 $\to$ 다중 백엔드 전송.

</details>

```text
애플리케이션에서 OTLP 텔레메트리 패킷 방출
        │
   1. [Receiver 수신] Collector의 Receiver 모듈이 포트 4317로 OTLP gRPC 패킷 접수
        │
   2. [Processor 메타 보강] 파드 이름, 네임스페이스, 버전(`service.version`) 라벨 주입
        │
   3. [Processor PII 마스킹] 정규식을 통해 HTTP Authorization 헤더 및 민감정보 자동 마스킹
        │
   4. [Processor 배치 제어] `memory_limiter`와 `batch` 모듈을 통해 OOM 방지 및 묶음 패킹
        │
   5. [Exporter 다중 전송] 메트릭은 Prometheus, 트레이스는 Tempo, 로그는 Loki로 병렬 전달
```

#### 한줄 요약
- OTLP 수신 → 메타 보강 → PII 마스킹 → 배치 제어 → 다중 전송 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Agent vs Gateway Mode**: 노드마다 데몬셋으로 띄우는 Agent 방식과 중앙 집중 클러스터로 띄우는 Gateway 방식.

</details>

| 비교 항목 | 에이전트 모드 (Agent: DaemonSet) | 게이트웨이 모드 (Gateway: Deployment) |
|:---|:---|:---|
| 배치 토폴로지 | **K8s Worker Node마다 1개씩 데몬셋 배포** | **중앙 전용 K8s 클러스터에 Deployment 배포** |
| 주요 핵심 역할 | **로컬 파드 텔레메트리 초저지연 1차 수집** | **전사 데이터 집계, 중앙 PII 마스킹, 외부 전송**|
| 네트워크 오버헤드 | 로컬 localhost/UDS 통신으로 최소화 | 중앙 수집기로의 네트워크 통신 트래픽 발생 |
| 실무 권장 패턴 | **노드 로컬 수집기(Agent) + 중앙 집중형 수집기(Gateway) 2-Tier 조합 구축** |

#### 한줄 요약
- 로컬 1차 수집은 Agent 모드, 중앙 2차 가공 및 전송은 Gateway 모드를 조합(2-Tier)하여 운영한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Memory Limiter**: 트래픽 폭증 시 OTel Collector가 메모리 부족(OOM)으로 다운되는 것을 막기 위해 임계치 초과 시 데이터를 안전하게 드롭하는 보호 장치.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 트레이스 스팬 내 Bearer Token 등 민감정보(PII) 유출 | **Collector Processor에서 `attributes/insert` 및 헤더 삭제 정제** | 보안 컴플라이언스 100% 준수 |
| 트래픽 폭증 시 OTel Collector 프로세스 OOM 비정상 종료 | **`memory_limiter` 및 `batch` 프로세서 파이프라인 필수 배치** | 수집기 무중단 안정성 확보 |
| Java Auto-Instrumentation 과다 수집으로 앱 CPU 저하 | **계측 스코프를 HTTP 엔드포인트 및 DB 쿼리 메서드로 한정** | 앱 CPU 오버헤드 3% 미만 유지 |
| 단일 백엔드 장애 시 전체 파이프라인 블로킹 | **Collector Exporter에 `sending_queue` 및 재시도 백오프 설정** | 데이터 유실 방지 및 비동기 격리 |

#### 한줄 요약
- PII 마스킹, 메모리 리미터, 계측 스코프 최적화, 전송 큐 비동기화로 운영한다.

## Ⅶ. 결론

- 분산 마이크로서비스 환경에서 모니터링 벤더 종속을 완전히 탈피하고 통합 관측성을 확립하기 위해 **CNCF 표준 OpenTelemetry API/SDK와 OTLP 프로토콜을 전사 표준으로 채택**하고, **2-Tier OTel Collector 파이프라인**을 구축하여 개방형 엔터프라이즈 관측성 완성

#### 한줄 요약
- OpenTelemetry는 단일 표준 API/SDK와 3단계 Collector 파이프라인을 통해 메트릭, 로그, 트레이스를 벤더 독립적으로 수집·가공하는 핵심 표준 기술이다.