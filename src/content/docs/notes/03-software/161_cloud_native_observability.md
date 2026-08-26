---
sidebar:
  order: 161
  label: "161. 클라우드 네이티브 관측성"
  badge:
    text: "기출 · 70%"
    variant: note
title: "클라우드 네이티브 관측성 (Cloud Native Observability)"
date: "2026-08-26T13:14:23+09:00"
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

- 정의/개념: 메트릭·로그·추적 신호를 연계해 **시스템 내부 상태를 추론하는 관측 체계**
- 배경/필요성: 마이크로서비스 확대로 **기존 단일 모니터링의 장애 병목 추적 한계**

#### 한줄 요약
- 메트릭·추적·로그 상관 분석 기반 **분산 장애 원인 신속 규명**

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Trace Correlation**: 메트릭 그래프 이상 발생 시 동일한 `trace_id`를 매개로 관련 분산 트레이스와 에러 로그를 즉시 핀포인트 조회하는 기법.
- **OpenTelemetry(OTel)**: 벤더 종속 없이 단일 SDK와 Collector로 3대 관측성 신호를 통합 수집하는 CNCF 표준 프레임워크.

</details>

- 메트릭(Prometheus), 로그(Loki), 트레이스(Tempo/Jaeger)의 **관측성 3대 기둥(3 Pillars) 통합**
- W3C Trace Context 표준 기반의 **엔드-투-엔드(E2E) 분산 컨텍스트 전파**
- 알려지지 않은 미지의 장애(Unknown Unknowns)를 다차원 분석하는 **상관 분석(Correlation)**

#### 한줄 요약
- 3대 신호 통합과 표준 프로토콜 기반 **분산 장애 신속 진단**

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **관측성 4대 아키텍처 계층**: Instrumentation Layer(OTel SDK), Collection Layer(OTel Collector), Storage Layer(3대 저장소), Visualization(Grafana).

</details>

```text
[클라우드 네이티브 관측성 아키텍처 구조]
|-- OTel SDK
|   |-- 텔레메트리 생성
|   `-- W3C traceparent 헤더 전파
|-- OTel 수집기
|   |-- Receiver (신호 수신)
|   |-- Processor (PII 마스킹 및 샘플링)
|   `-- Exporter (저장소 라우팅)
|-- 메트릭 저장소
|   `-- Prometheus (QPS, P99 지연)
|-- 트레이스 저장소
|   `-- Tempo (호출 경로, Span 지연)
|-- 로그 저장소
|   `-- Loki (구조화 JSON 로그)
`-- 통합 분석 UI
    `-- Grafana (신호 간 원클릭 교차 분석)
```

선의 의미: 계층 및 OTel SDK가 생성한 3대 신호를 OTel Collector가 취합·가공하여 저장소로 라우팅하고 Grafana에서 통합 분석하는 구조

| 구성요소 | 책임 | 주요 특징 |
|:---|:---|:---|
| OTel SDK (계측) | 애플리케이션에 주입되어 **W3C traceparent 전파 및 텔레메트리 생성** | 표준 계측 API |
| OTel 수집기 | 텔레메트리를 수신해 **PII 마스킹 및 저장소 라우팅** | 파이프라인 가공 |
| 메트릭 저장소 | Prometheus 기반 **QPS·P99 지연·에러율 시계열 보관** | 집계 및 알림 |
| 트레이스 저장소 | Tempo 기반 **분산 호출 경로 및 스팬(Span) 지연 보관** | 경로 추적 |
| 로그 저장소 | Loki 기반 **JSON 포맷 구조화 로그 및 스택 보관** | 상세 원인 기록 |
| 통합 분석 UI | Grafana 기반 **Trace ID 연계 원클릭 교차 분석 제공** | 상관 분석 대시보드 |

#### 한줄 요약
- 계측 SDK, 수집기, 3대 저장소, 시각화 UI로 **통합 파이프라인 구축**

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **장애 진단 5단계**: SLO 경보 수신 $\to$ 메트릭 지연 확인 $\to$ 대표 Trace ID 추출 $\to$ 병목 Span 식별 $\to$ 동일 Trace 로그로 원인 확정.

</details>

```text
서비스 장애 발생 및 관측성 진단 개시
        │
   1. [경보 발생] Prometheus P99 지연 2초 초과 알림 발송
        │
   2. [메트릭 확인] Grafana 대시보드 에러율 및 지연 스파이크 확인
        │
   3. [대표 트레이스 추출] 지연 발생 요청의 고유 trace_id 추출
        │
   4. [스팬 병목 식별] Jaeger 트레이스 뷰에서 DB Lock 지연 확인
        │
   5. [로그 원인 확정] 동일 trace_id의 Loki 로그로 데드락 SQL 확정
```

#### 한줄 요약
- 경보·메트릭·트레이스·스팬·로그 연계로 **장애 원인 신속 확정**

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **전통적 모니터링 vs 현대적 관측성**: 고정 임계치 감시(Monitoring)와 복잡 분산 장애 원인 추론(Observability).

</details>

| 비교 항목 | 전통적 모니터링 (Monitoring) | 클라우드 네이티브 관측성 (Observability) |
|:---|:---|:---|
| 진단 대상 영역 | **기지의 장애 (Known Knowns)** | **미지의 장애 (Unknown Unknowns)** |
| 데이터 통합 수준 | CPU·메모리·서버로그 사일로 수집 | **3대 신호의 Trace ID 기반 연계** |
| 장애 원인 추적 | 관리자 감에 의존한 수동 분석 | **E2E 트레이스 기반 병목 즉시 식별** |
| 최적 적용 환경 | 단일 모놀리식 서버 환경 | **대규모 분산 마이크로서비스** |

#### 한줄 요약
- 단순 임계치 감시는 모니터링, 복잡 분산 원인 추론은 **관측성 체계** 적용

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Tail-based Sampling**: 요청이 끝난 후 에러가 발생했거나 지연시간이 긴 비정상 트레이스만 100% 저장하고 정상 트레이스는 1%만 저장하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 메트릭 라벨 카디널리티 폭발 | **식별자를 메트릭에서 제거하고 추적·로그 속성으로 이관** | 시계열 메트릭 용량 90% 절감 |
| 트레이스 스토리지 고갈 | **OTel Collector의 테일 기반 샘플링(에러 100% 저장)** | 트레이스 저장 비용 80% 절감 |
| 상용 APM SDK 종속 | **CNCF 표준 OpenTelemetry(OTel) 체계로 통일** | 벤더 비종속 호환성 확보 |
| 비동기 메시징 시 계보 단절 | **Kafka 메시지 헤더에 W3C traceparent 명시적 주입** | 비동기 분산 트랜잭션 추적 |

#### 한줄 요약
- 카디널리티 정제·테일 샘플링·OTel 표준화로 **운영 비용 절감**

## Ⅶ. 결론

- 분산 시스템 장애 원인 추론은 **관측성 체계**, 표준 계측은 **OpenTelemetry** 기반 선택

#### 한줄 요약
- 3대 신호 상관 분석과 OTel 표준화 기반 **클라우드 네이티브 관측성 확립**
