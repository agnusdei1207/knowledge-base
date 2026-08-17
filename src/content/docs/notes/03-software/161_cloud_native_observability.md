---
sidebar:
  order: 161
  label: "161. 클라우드 네이티브 관측성 (Cloud Native Observability)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "클라우드 네이티브 관측성 (Cloud Native Observability)"
date: "2026-08-18T02:15:00+09:00"
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

<details><summary>용어 설명</summary>

- **클라우드 네이티브 관측성(Cloud-Native Observability)**: 분산 MSA 환경에서 시스템의 내부 상태를 외부 출력 신호인 메트릭(Metrics), 로그(Logs), 분산 추적(Traces)의 3대 기둥(3 Pillars)을 통해 종합적으로 추론하고 진단하는 체계.
- **분산 호출 병목 및 원인 규명 한계(Distributed Bottleneck & Root-Cause Failure)**: 단일 서버 모니터링 방식으로는 수십 개 마이크로서비스 간 비동기 호출 지연 구간과 미지의 장애(Unknown Unknowns) 원인을 식별하지 못하는 한계.

</details>

- 정의/개념: 분산 시스템의 내부 상태를 파악하기 위해 **메트릭(Metrics), 로그(Logs), 트레이스(Traces)를 연계 수집하고 분석**하는 클라우드 네이티브 관측성 체계
- 배경/필요성: 마이크로서비스 간 비동기 다단계 호출 구조로 인한 **단일 서버 모니터링 한계, 병목 구간 추적 불가 및 장애 원인 분석 지연 위험** 직면

#### 한줄 요약

- 메트릭(증상 감지), 트레이스(병목 구간 식별), 로그(상세 원인 규명)의 유기적 상관 분석을 통해 복잡한 분산 장애의 근본 원인을 즉시 규명

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Trace Context 상관 분석(Trace Correlation)**: 모든 메트릭과 로그에 고유 `trace_id`를 자동 주입하여 대시보드 클릭 한 번으로 관련 에러 로그와 지연 스팬(Span)을 즉시 조회하는 기법.
- **OpenTelemetry(OTel) 표준화**: 벤더 종속 없이 단일 SDK와 Collector로 메트릭, 로그, 트레이스를 일원화 수집하는 CNCF 표준 오픈소스 프레임워크.

</details>

- 메트릭(Prometheus), 로그(Loki), 트레이스(Tempo/Jaeger)의 **관측성 3대 기둥(3 Pillars) 통합**
- W3C Trace Context 표준 기반의 **엔드-투-엔드(E2E) 분산 컨텍스트 전파**
- 알려지지 않은 미지의 장애(Unknown Unknowns)를 다차원 라벨로 탐색하는 **능동적 디버깅 환경**

#### 한줄 요약

- 3대 텔레메트리 신호의 완벽한 상호 연계를 통해 분산 시스템의 MTTR(평균 복구 시간)을 획기적으로 단축

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **관측성 파이프라인 아키텍처**: Application Instrumentation, OTel Collector(수집/가공), 3대 저장소(Metrics/Logs/Traces DB), 시각화/분석 UI(Grafana).

</details>

```text
[ 클라우드 네이티브 통합 관측성(Observability) 파이프라인 구조도 ]

 1. [ 마이크로서비스 파드 계층 (App Instrumentation: OTel SDK) ]
    • Order Service ──► Payment Service ──► Delivery Service (Trace Context 전파)
                                    │ (OTLP / gRPC 전송)
                                    ▼
 2. [ 오픈텔레메트리 수집기 (OpenTelemetry Collector) ] ─────────┐
    • Receiver (수집) ➔ Processor (배치/PII 마스킹/샘플링) ➔ Exporter│
    └───────────────────────────────┬─────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
 3. [ Metrics: Prometheus ]   [ Traces: Tempo/Jaeger ]    [ Logs: Loki/ELK ]
    - QPS, Error Rate, CPU      - Trace ID, Span Latency    - Error Stack Trace
        └───────────────────────────┬───────────────────────────┘
                                    │
                                    ▼
 4. [ 통합 시각화 및 상관 분석 UI (Grafana Dashboard / Alertmanager) ]
```

선의 의미: OTel SDK가 생성한 3대 신호를 OTel Collector가 취합·가공하여 각 저장소로 보내고 Grafana에서 통합 상관 분석하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| OTel SDK (계측 계층) | 애플리케이션에 주입되어 **W3C `traceparent` 헤더를 전파하고 메트릭/로그/스팬 생성** |
| OTel Collector (수집 가공)| 텔레메트리 신호를 수신하여 **개인정보(PII) 마스킹, 필터링, 샘플링 후 저장소 라우팅** |
| 시계열 메트릭 저장소 | Prometheus 등을 통해 **초당 처리량(QPS), 응답 지연(P99), 에러율 시계열 보관** |
| 분산 트레이스 저장소 | Tempo/Jaeger를 통해 **트랜잭션별 마이크로서비스 호출 경로 및 스팬(Span) 지연 보관** |
| 구조화 로그 저장소 | Loki/Elasticsearch를 통해 **JSON 포맷의 상세 이벤트 및 스택 트레이스 보관** |
| 통합 분석 UI (Grafana) | `trace_id`를 매개로 **메트릭 이상 그래프에서 스팬과 로그로 원클릭 교차 분석 제공** |

#### 한줄 요약

- 계측 SDK, OTel 수집기, 3대 저장소, Grafana 분석 UI가 결합하여 엔드-투-엔드 관측성을 완성

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **관측성 기반 장애 진단 5단계 절차**: SLO 알람 감지 $\to$ 메트릭 이상 구간 확인 $\to$ 대표 Trace ID 추출 $\to$ 병목 Span 식별 $\to$ 연관 로그 분석.

</details>

```text
[ 관측성 3대 기둥 기반 장애 진단 및 근본 원인 분석 파이프라인 ]

 ┌────────────────────────────────────────┐
 │ 1. Alertmanager: SLO 응답 지연 경보 발생│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 2. Metrics: 결제 서비스 P99 지연 급증 확인│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 3. Traces: 지연된 요청의 대표 Trace ID 추출│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 4. Span 분석: 특정 DB 락 대기 병목(3s) 식별│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 5. Logs: 동일 Trace ID 에러 로그로 원인 확정
 └────────────────────────────────────────┘
```

### 동작 원리

1. 경보 발생: 결제 API의 P99 지연시간이 2초를 초과하여 Prometheus Alertmanager가 Slack 알림을 발송.
2. 메트릭 확인: Grafana 대시보드에서 장애 발생 시점의 에러율 및 지연 스파이크 그래프를 확인.
3. 트레이스 추출: 해당 시간대의 지연된 요청 중 하나를 선택하여 고유한 `trace_id`를 확보.
4. 스팬 분석: Jaeger 뷰에서 결제 서비스 $\to$ PostgreSQL 호출 스팬이 3초간 락 대기(Lock Wait) 중임을 시각적으로 확인.
5. 로그 연동: 동일 `trace_id`로 필터링된 Loki 로그를 열어 데드락 SQL 쿼리 문맥을 즉시 확인하고 장애 해결.

#### 한줄 요약

- 경보 발생 $\to$ 메트릭 확인 $\to$ 트레이스 추출 $\to$ 스팬 분석 $\to$ 로그 연동의 5단계

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **전통적 모니터링 vs 현대적 관측성**: 이미 알고 있는 고정 임계치 감시(Monitoring)와 원인 미상의 복잡 분산 장애 추론(Observability).

</details>

| 구분 | 전통적 모니터링 (Monitoring) | 클라우드 네이티브 관측성 (Observability) |
|:---|:---|:---|
| **적용 기준** | 단일 모놀리식 서버, 단순 3-Tier 인프라 | 대규모 분산 마이크로서비스(MSA), 멀티 클라우드 |
| **핵심 특징** | **사전 정의된 지표(CPU/RAM) 임계치 초과 감시 (Knowns)** | **메트릭·로그·트레이스 연계로 미지의 원인 추론 (Unknowns)** |
| **한계** | 복잡한 MSA 다단계 호출 지연의 병목 구간 추적 불가 | 수집 데이터량 폭증에 따른 저장소 비용 및 샘플링 관리 필요 |

#### 한줄 요약

- 기지(Known)의 단순 감시는 모니터링, 미지(Unknown)의 분산 원인 추론은 관측성을 적용

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **테일 기반 샘플링(Tail-based Sampling)**: 요청이 완료된 후 에러가 발생했거나 지연시간이 긴 비정상 트레이스만 100% 저장하고 정상 트레이스는 1%만 저장하는 비용 최적화 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 메트릭 라벨에 `user_id`를 넣어 High-Cardinality 비용 폭발 | **고유 식별자는 메트릭 라벨에서 제거하고 Trace/Log 속성으로 이관** | 시계열 메트릭 저장소 용량 90% 절감 |
| 하루 수억 건의 트레이스 저장으로 인한 스토리지 고갈 | **OTel Collector의 Tail-based Sampling (에러 100%, 정상 1% 저장)** | 트레이스 저장 비용 80% 절감 |
| 상용 APM(Datadog/Dynatrace) SDK 종속으로 인한 교체 불가 | **CNCF 표준 OpenTelemetry (OTel) SDK 및 프로토콜로 전면 통일** | 벤더 비종속 오픈소스 호환성 100% 확보 |

#### 한줄 요약

- 카디널리티 정제, 테일 기반 샘플링, OTel 표준화를 통해 관측성 비용과 효율을 최적화

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **AIOps 및 자가 치유 연계(AIOps & Self-Healing)**: 관측성 텔레메트리 데이터를 AI가 실시간 분석하여 이상을 사전 예측하고 자동으로 오토스케일링/복구를 수행하는 진화 방향.

</details>

- **클라우드 네이티브 관측성**은 복잡한 마이크로서비스 운영의 필수 전제조건이며, OpenTelemetry 표준을 기반으로 메트릭, 로그, 트레이스를 유기적으로 결합하여 시스템의 투명성과 복원력을 완성해야 함

#### 한줄 요약

- 3대 기둥의 유기적 상관 분석과 OTel 표준화를 통해 분산 클라우드의 신뢰성을 완성
