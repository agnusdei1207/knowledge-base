---
sidebar:
  order: 161
  label: "161. 클라우드 네이티브 관측성 (Cloud Native Observability)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "클라우드 네이티브 관측성 (Cloud Native Observability)"
date: "2026-08-14T02:36:00+09:00"
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

- **관측성(Observability)**: Metrics, Logs, Traces(3대 기둥)를 통합 분석하여 복잡한 시스템의 비정상 원인을 추론하는 기술.
- **관측성 3대 기둥(3 Pillars)**: 수치 집계(Metrics), 이벤트 기록(Logs), 분산 엔드-투-엔드 이동 경로(Traces) 데이터.
- **오픈텔레메트리(OpenTelemetry, OTel)**: 텔레메트리 데이터 수집 및 표준화를 위한 CNCF 오픈소스 프로젝트.

</details>

- 정의/개념: 외부 신호로 내부 상태를 추론하는 **Observability**
- 배경/필요성: 분산 호출은 단일 Server 지표만으로 **장애 경로•원인** 식별 불가

#### 한줄 요약

- 결제 지연 그래프에서 느린 요청 하나를 골라 호출 경로와 같은 식별자의 오류 기록을 따라가면 어느 서비스에서 왜 늦어졌는지 좁힐 수 있다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Trace ID Correlation**: 모든 로그 및 메트릭에 동일한 `trace_id: 8f9a2b...` 코드를 자동 주입하여 로그와 트레이스를 단 1클릭으로 대조 추적.

</details>

- **지표**: Prometheus 기반 시스템 자원(CPU/RAM) 및 서비스 성능(QPS) 시각화.
- **로그**: Loki/Fluentbit 기반 구조화(JSON) 및 오류 상세 문맥 파악.
- **추적**: Jaeger/Tempo 기반 분산 서비스 간 호출 경로 및 병목 구간 추적.

#### 한줄 요약

- 모든 기록을 모으는 대신 사용자가 겪은 실패를 어떤 신호로 찾고 어떤 공통 키로 원인까지 이동할지 먼저 정하는 방식이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **OpenTelemetry Collector**: Receiver(수집) $\rightarrow$ Processor(배치/마스킹) $\rightarrow$ Exporter(전송) 3단계 구조로 텔레메트리 신호를 처리하는 중앙 수집 엔진.

</details>

```text
[Application Instrumentation] ─ [OTel Collector]
                                  │
         ┌────────────────────────┼──────────────────────┐
   [Metrics Store]           [Logs Store]          [Traces Store]
         └────────────────────────┼──────────────────────┘
                           [Analysis UI]
```

| 구성요소 | 책임 |
|---|---|
| Application Instrumentation | **Context 전파•Signal 생성** |
| OTel Collector | **수집•처리•Routing**과 민감 정보 제거 |
| Metrics Store | 시간별 **집계값**•**추세** 저장 |
| Logs Store | Event의 **상세 문맥** 저장 |
| Traces Store | 요청별 **Span 경로•지연** 저장 |
| Analysis UI | Signal **상관 분석•시각화** 제공 |

#### 한줄 요약

- 각 서비스가 단서를 만들고 문맥 전파가 같은 사건 번호를 붙이면 수집기와 저장소를 거쳐 분석 화면에서 하나의 장애 이야기로 재구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Context Propagation**: W3C Trace Context 표준(`traceparent` 헤더)을 HTTP 요청 헤더에 실어 다음 마이크로서비스로 전파(Propagate)하는 기법.

</details>

```text
[SLO Alert]
    │
    ▼
1. Metric 이상 구간 확인
    │
    ▼
2. 대표 Trace 선택
    │
    ▼
3. 병목 Span 식별
    │
    ▼
4. 동일 Context Log 조회
    │
    ▼
5. 원인 가설 검증
    │
    ▼
[대응 결정]
```

### 동작 원리

1. Metric 이상 구간 확인: 오류율•지연•Traffic 변화 식별
2. 대표 Trace 선택: 오류•지연 요청의 Trace ID 확보
3. 병목 Span 식별: Service 호출 경로와 지연 구간 확인
4. 동일 Context Log 조회: Trace ID로 상세 오류 검색
5. 원인 가설 검증: 배포•자원•의존 Signal과 대조

#### 한줄 요약

- 주문 요청이 결제와 재고를 거치는 동안 같은 추적 식별자를 전달하면 세 서비스의 지연과 오류가 한 호출 경로로 묶인다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Known Knowns vs Unknown Unknowns**: 모니터링은 이미 알고 있는 장애(CPU 90% 이상)를 체크, 관측성은 원인을 전혀 모르는 복잡한 장애(Unknown Unknowns)를 추론.

</details>

| 비교 항목 | Traditional Monitoring (모니터링) | Cloud-Native Observability (관측성) |
|:---|:---|:---|
| 핵심 질문 | **"시스템이 지금 정상인가?" (Known)**| **"왜 3번째 MSA 서비스에서 멈췄는가?" (Unknown)**|
| 수집 데이터 | 사전 정의 지표 중심 | **Metrics•Logs•Traces 연계** |
| 상관 관계  | Signal별 분석 중심 | **Trace Context 기반 교차 분석** |
| 적용 범위 | 알려진 상태 감시 | 복잡한 분산 원인 추론 |

#### 한줄 요약

- 메트릭으로 언제 나빠졌는지 찾고 추적로 느린 구간을 고른 뒤 로그에서 그 시점의 오류와 입력 문맥을 확인한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **High Cardinality Cost Explosion**: Log 및 Metric 라벨에 `user_id`, `email` 같은 수백만 개의 고유값을 함부로 넣었다가 저장소 디스크 및 비용이 폭발하는 안티패턴.

</details>

| 3대 관측성 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| 1. High Cardinality Costs | Metric 라벨에 user_id 넣어서 비용 폭발| **High-cardinality 지표는 Log로 이관 정제** |
| 2. Trace Data Overload | 하루 수억 건 트레이스 저장 시 디스크 고갈| **Tail-based Sampling 적용 (성공 1%, 에러 100% 저장)**|
| 3. Vendor Lock-in | 특정 APM (Dynatrace, Datadog) SDK 종속 | **OpenTelemetry (OTel) 표준 SDK로 전면 통일** |

> 사례: **토스 / 당근마켓 / 쿠팡 OpenTelemetry & Prometheus & Loki & Tempo 기반 통합 관측성 구축**

#### 한줄 요약

- 사용자 식별자를 메트릭 속성으로 모두 넣지 말고 오류 요청의 추적와 로그에서만 찾도록 나누면 경보 비용과 진단 단서를 함께 관리할 수 있다.

## Ⅶ. 결론

- SLO 감시는 **Metrics**, 경로는 Traces, 원인 문맥은 Logs 연결

#### 한줄 요약

- 사용자 증상에서 지표•추적•로그를 같은 문맥으로 이동할 수 있을 때만 신호를 수집한다.
