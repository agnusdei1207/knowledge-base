---
title: "관측 가능성 (Observability Monitoring)"
date: "2026-07-05"
tags:
  - "cspe-software"
weight: 77
---

## Ⅰ. 개요
- **정의**: 외부 출력(Metrics·Logs·Traces)만으로 시스템 내부 상태를 추론할 수 있는 능력임
- **배경/필요성**: 분산 시스템에서 사전 정의 알림만으로는 예측하지 못한 장애 원인을 파악할 수 없으므로 탐색적 분석이 필요함
- **비유**: 대시보드 계기판(모니터링)을 넘어 엔진 내부 센서 데이터로 고장 원인을 진단하는 것과 유사함

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 모니터링과 관측 가능성 차이 | 3대 신호(Metrics/Logs/Traces), 상관 분석 | 모니터링 = 관측 가능성이 아님(모니터링은 하위 집합) |

> 요약: 관측 가능성은 3대 텔레메트리 신호로 시스템 내부 상태를 추론하는 능력임

## Ⅱ. 구성요소
```text
Application
  |--- Metrics  --> Prometheus --> Grafana
  |--- Logs     --> Fluentd   --> Elasticsearch (078 참조)
  |--- Traces   --> OTel SDK  --> Jaeger (079 참조)
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Metrics | 시계열 수치 데이터(CPU, 요청 수, 지연 P99 등) | 체온계 수치 |
| Logs | 이벤트별 구조화/비구조화 텍스트 기록 | 진료 기록부 |
| Traces | 분산 요청의 서비스 간 호출 경로·지연 추적 | 택배 송장 추적 |
| OpenTelemetry | Metrics/Logs/Traces 수집을 통합한 벤더 중립 계측 프레임워크 | 만능 센서 키트 |

> 요약: Metrics·Logs·Traces 3대 신호와 OpenTelemetry 통합 수집으로 구성됨

## Ⅲ. 절차
```text
Instrument --> Collect --> Store --> Correlate --> Alert/Analyze
     |            |          |          |              |
   OTel SDK   Collector   TSDB/ES   Trace-Log 연계  Dashboard
```
- 1단계: 애플리케이션에 OTel SDK로 Metrics·Logs·Traces 계측 코드 삽입함
- 2단계: OTel Collector가 텔레메트리를 수집·변환·라우팅함
- 3단계: 신호별 저장소(Prometheus/ES/Jaeger)에 적재 후 Trace ID로 상관 연계함
- 4단계: 대시보드 시각화·알림 설정 후 이상 탐지 시 근본 원인 탐색적 분석 수행함

> 요약: 계측-수집-저장-상관분석 4단계로 관측 가능성을 확보함

## Ⅳ. 문제점
- 텔레메트리 폭증: 마이크로서비스 증가 시 데이터 볼륨이 기하급수적으로 증가함
- 신호 간 단절: Metrics·Logs·Traces가 별도 도구에 저장되면 상관 분석이 수동 작업화됨
- 계측 부담: 애플리케이션 코드에 계측 삽입 시 개발자 작업량 증가함

> 요약: 데이터 폭증, 신호 단절, 계측 부담이 주요 문제임

## Ⅴ. 개선방안
1. 단기: 샘플링 전략(Tail-based Sampling)으로 텔레메트리 볼륨 제어함
2. 중기: OpenTelemetry 통합 파이프라인으로 Trace ID 기반 3대 신호 자동 상관함
3. 장기: eBPF·Auto-instrumentation으로 코드 수정 없이 자동 계측함

> 요약: 샘플링, OTel 통합, 자동 계측으로 개선 가능함

## Ⅵ. 전망
- 발전 방향: OpenTelemetry가 CNCF 사실 표준으로 자리잡아 벤더 종속 해소 가속 중임
- 기술사적 판단: SRE(076 참조)의 SLI 수집 기반이므로 연계 서술 필요함
- 기술사 제언: Metrics·Logs·Traces 통합 저장·분석 아키텍처(예: Grafana Stack) 설계를 권고함
