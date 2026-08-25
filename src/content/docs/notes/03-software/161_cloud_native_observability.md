---
sidebar:
  order: 161
  label: "161. 클라우드 네이티브 관측성"
  badge:
    text: "기출 · 70%"
    variant: note
title: "클라우드 네이티브 관측성 (Cloud Native Observability)"
date: "2026-08-25T11:00:00+09:00"
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

- **클라우드 네이티브 관측성(Observability)**: 분산 시스템의 외부 출력 신호인 Metrics, Logs, Traces 3대 기둥을 유기적으로 연계하여 시스템 내부 상태를 추론하는 체계.
- **3 Pillars of Observability**: 정량적 통계 수치(Metrics), 상세 실행 기록(Logs), 분산 호출 경로 및 지연(Traces).

</details>

- 정의/개념: 분산 시스템의 내부 상태를 파악하기 위해 **메트릭, 로그, 분산 추적 3대 텔레메트리 신호를 연계 수집하고 상관 분석하는 클라우드 네이티브 관측 체계**
- 배경/필요성: 마이크로서비스 간 비동기 다단계 호출 구조로 인한 **기존 단일 서버 모니터링 한계, 분산 호출 병목 구간 추적 불가 및 장애 원인 분석 지연 해결 불가**

#### 한줄 요약
- 메트릭(증상 감지), 트레이스(병목 식별), 로그(원인 확정)의 상관 분석으로 분산 장애를 즉시 해결한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Trace Correlation**: 메트릭 그래프 이상 발생 시 동일한 `trace_id`를 매개로 관련 분산 트레이스와 에러 로그를 즉시 핀포인트 조회하는 기법.
- **OpenTelemetry(OTel)**: 벤더 종속 없이 단일 SDK와 Collector로 3대 관측성 신호를 통합 수집하는 CNCF 표준 프레임워크.

</details>

- 메트릭(Prometheus), 로그(Loki), 트레이스(Tempo/Jaeger)의 **관측성 3대 기둥(3 Pillars) 통합**
- W3C Trace Context 표준 기반의 **엔드-투-엔드(E2E) 분산 컨텍스트 전파**
- 알려지지 않은 미지의 장애(Unknown Unknowns)를 다차원 분석하는 **상관 분석(Correlation)**

#### 한줄 요약
- 3대 기둥의 유기적 상관 분석과 표준 프로토콜을 통해 미지의 분산 장애 원인을 신속히 규명한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **관측성 4대 아키텍처 계층**: Instrumentation Layer(OTel SDK), Collection Layer(OTel Collector), Storage Layer(3대 저장소), Visualization(Grafana).

</details>

```text
[클라우드 네이티브 3대 관측성 아키텍처 구조]
|-- 1. App Workload & OTel SDK Layer (W3C traceparent 헤더 전파 및 텔레메트리 생성)
|-- 2. OpenTelemetry Collector Layer
|   `-- Receiver (수신) -> Processor (PII 마스킹/샘플링) -> Exporter (라우팅)
`-- 3. Telemetry Storage Layer
    |-- Metrics: Prometheus (초당 요청수 QPS, P99 응답지연, 에러율)
    |-- Traces: Tempo / Jaeger (Trace ID 기반 분산 호출 경로 및 Span 지연)
    `-- Logs: Loki / Elasticsearch (Trace ID가 주입된 구조화 JSON 로그)
`-- 4. Unified Visualization Layer (Grafana Dashboard: 메트릭 -> 트레이스 -> 로그 원클릭 전환)
```

선의 의미: 계층 및 OTel SDK가 생성한 3대 신호를 OTel Collector가 취합·가공하여 저장소로 라우팅하고 Grafana에서 통합 분석하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **OTel SDK (계측 계층)** | 애플리케이션에 주입되어 **W3C `traceparent` 헤더를 전파하고 메트릭/로그/스팬 생성** | 표준 계측 API |
| **OTel 수집기 (Collector)**| 텔레메트리 신호를 수신하여 **개인정보(PII) 마스킹, 필터링, 샘플링 후 저장소 라우팅** | 파이프라인 가공 |
| **시계열 메트릭 저장소** | Prometheus 등을 통해 **초당 처리량(QPS), 응답 지연(P99), 에러율 시계열 보관** | 집계 및 알림 |
| **분산 트레이스 저장소** | Tempo/Jaeger를 통해 **트랜잭션별 마이크로서비스 호출 경로 및 스팬(Span) 지연 보관**| 호출 경로 추적 |
| **구조화 로그 저장소** | Loki/Elasticsearch를 통해 **JSON 포맷의 상세 이벤트 및 스택 트레이스 보관** | 상세 원인 기록 |
| **통합 분석 UI (Grafana)** | `trace_id`를 매개로 **메트릭 이상 그래프에서 스팬과 로그로 원클릭 교차 분석 제공** | 상관 분석 대시보드 |

#### 한줄 요약
- 계측 SDK, OTel 수집기, 3대 저장소, Grafana 분석 UI가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **장애 진단 5단계**: SLO 경보 수신 $\to$ 메트릭 지연 확인 $\to$ 대표 Trace ID 추출 $\to$ 병목 Span 식별 $\to$ 동일 Trace 로그로 원인 확정.

</details>

```text
서비스 장애 발생 및 관측성 진단 개시
        │
   1. [경보 발생] Prometheus Alertmanager가 결제 서비스 P99 응답 지연 2초 초과 슬랙 알림 발송
        │
   2. [메트릭 확인] Grafana 대시보드에서 장애 발생 시점의 에러율 및 지연 스파이크 그래프 확인
        │
   3. [대표 트레이스 추출] 지연이 발생한 특정 요청의 고유 식별자인 `trace_id` 즉시 추출
        │
   4. [스팬 병목 식별] Jaeger 트레이스 뷰에서 결제 -> DB 호출 스팬이 3초간 Lock 대기 중임을 확인
        │
   5. 동일 `trace_id`로 필터링된 Loki 로그를 열어 데드락을 유발한 SQL 쿼리 확인 및 즉시 조치
```

#### 한줄 요약
- 경보 발생 → 메트릭 확인 → 트레이스 추출 → 스팬 분석 → 로그 연동 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **전통적 모니터링 vs 현대적 관측성**: 고정 임계치 감시(Monitoring)와 복잡 분산 장애 원인 추론(Observability).

</details>

| 비교 항목 | 전통적 모니터링 (Monitoring) | 클라우드 네이티브 관측성 (Observability) |
|:---|:---|:---|
| 진단 대상 영역 | **이미 알고 있는 기지의 장애 (Known Knowns)** | **원인 불명의 복잡한 미지 장애 (Unknown Unknowns)**|
| 데이터 통합 수준 | CPU/RAM/서버로그의 사일로화된 분리 수집 | **Metrics, Logs, Traces의 `trace_id` 기반 유기적 결합**|
| 장애 원인 추적 | 관리자의 경험과 감에 의존한 수동 디버깅 | **E2E 트레이스 기반 핀포인트 병목 구간 즉시 식별** |
| 최적 적용 환경 | 단일 모놀리식 서버, 단순 3-Tier 아키텍처 | **대규모 분산 마이크로서비스, 멀티 클라우드** |

#### 한줄 요약
- 단순 임계치 감시는 모니터링, 복잡한 분산 원인 추론은 관측성을 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Tail-based Sampling**: 요청이 끝난 후 에러가 발생했거나 지연시간이 긴 비정상 트레이스만 100% 저장하고 정상 트레이스는 1%만 저장하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 메트릭 라벨에 `user_id`를 넣어 High-Cardinality 비용 폭발 | **고유 식별자는 메트릭 라벨에서 제거하고 Trace/Log 속성으로 이관** | 시계열 메트릭 저장소 용량 90% 절감 |
| 하루 수억 건의 트레이스 저장으로 인한 스토리지 고갈 | **OTel Collector의 Tail-based Sampling (에러 100%, 정상 1% 저장)** | 트레이스 저장 비용 80% 절감 |
| 상용 APM(Datadog/Dynatrace) SDK 종속으로 인한 교체 불가 | **CNCF 표준 OpenTelemetry (OTel) SDK 및 프로토콜로 전면 통일** | 벤더 비종속 오픈소스 호환성 100% 확보 |
| 마이크로서비스 간 비동기 메시징 시 계보 단절 | **Kafka 메시지 헤더에 W3C `traceparent` 명시적 주입 및 복원** | 비동기 분산 트랜잭션 추적성 완비 |

#### 한줄 요약
- 카디널리티 정제, 테일 기반 샘플링, OTel 표준화, Kafka 헤더 전파로 최적화한다.

## Ⅶ. 결론

- 마이크로서비스 환경에서 시스템의 복원력과 신뢰성을 확보하기 위해 **OpenTelemetry 표준을 기반으로 메트릭(Prometheus), 로그(Loki), 트레이스(Tempo)를 유기적으로 결합하고 Trace Correlation 기반의 통합 대시보드를 구축**하여 완전한 클라우드 네이티브 관측성 완성

#### 한줄 요약
- 클라우드 네이티브 관측성은 메트릭, 로그, 분산 추적의 상관 분석을 통해 복잡한 분산 시스템의 미지 장애를 신속히 규명하는 현대 소프트웨어 엔지니어링의 핵심 운영 체계다.