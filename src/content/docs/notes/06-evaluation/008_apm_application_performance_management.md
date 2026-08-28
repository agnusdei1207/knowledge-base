---
sidebar:
  order: 8
  label: "008. APM 애플리케이션 성능 관리 (Application Performance Management)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "분산 환경 관측성 및 트랜잭션 추적 : APM (W3C Trace Context & OpenTelemetry)"
date: "2026-08-26T15:51:05+09:00"
tags:
  - "notes-evaluation"
weight: 8
extra:
  question_no: "008"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "137회 기출, 애플리케이션 성능 관리(APM), 관측성 3대 기둥(Metrics, Logs, Traces), 분산 추적(Distributed Tracing: Trace ID, Span ID, W3C Trace Context traceparent 헤더), 바이트코드 인스트루멘테이션(Instrumentation), OpenTelemetry(OTel) 표준 수집기 및 적응형 샘플링(Tail-based Sampling)"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **애플리케이션 성능 관리(APM: Application Performance Management / Observability)**: 복잡한 분산 환경(마이크로서비스, 클라우드 네이티브)에서 최종 사용자 요청이 진입하여 여러 서비스 및 데이터베이스를 거쳐 반환될 때까지의 전 구간 호출 궤적(Trace)과 시스템 자원 상태(Metrics), 이벤트 로그(Logs)를 실시간 계측·연계하여 성능 병목 지점과 오류의 근본 원인(Root Cause)을 1초 내에 규명하는 성능 관리 프레임워크.
- **사일로화된 인프라 모니터링의 원인 분석 한계 결함(Siloed Metric Blindness Defect)**: 서버 CPU/메모리 가동률만 감시하는 전통적 모니터링 방식으로는, 인프라 자원이 정상(CPU 30%)임에도 불구하고 특정 마이크로서비스의 DB 락(Lock) 경합이나 서드파티 외부 API 타임아웃으로 인해 사용자 화면이 5초 이상 멈추는 분산 트랜잭션 지연의 원인을 추적하지 못하는 구조적 결함.

</details>

- 정의/개념: 메트릭·로그·추적을 연계하는 **애플리케이션 성능 관리** 체계
- 배경/필요성: 서버 자원 지표만 보는 감시는 인프라가 정상인데도 분산 호출의 **병목 원인**을 수작업 재현으로만 좁힐 수 있어 장애 시간이 그대로 비용이 되므로, 요청 단위 추적에 메트릭·로그를 상관시키는 관측 계층을 애플리케이션 실행 경로에 삽입해 구간별 지연을 즉시 지목할 필요

#### 한줄 요약
- APM은 W3C 표준 분산 추적과 메트릭/로그 연계를 통해 마이크로서비스 전 구간의 성능 병목을 실시간 식별한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **관측성(Observability) 3대 기둥 및 APM 핵심 요소**:
  - **분산 추적 (Traces)**: 요청의 엔드투엔드 여정을 트리 구조(Trace ID 및 Span ID)로 표현한 호출 경로.
  - **집계 메트릭 (Metrics)**: 초당 처리량(TPS), 에러율, CPU/메모리 사용량을 일정 주기로 집계한 수치 데이터.
  - **구조화 로그 (Logs)**: 런타임 이벤트 및 예외 스택트레이스를 Trace ID와 결합하여 기록한 텍스트 데이터.

</details>

- `traceparent`로 호출 문맥을 잇는 **W3C Trace Context**
- 코드 수정 없이 실행시간을 수집하는 **자동 계측**
- 완료 후 오류·지연 요청을 선별하는 **꼬리 기반 샘플링**

#### 한줄 요약
- W3C 분산 추적, 비침습적 자동 계측, 3대 기둥(Traces/Metrics/Logs) 연계, 꼬리 기반 샘플링을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **APM & OpenTelemetry 4대 핵심 아키텍처 계층**:
  1. **Instrumentation Layer**: OTel SDK, Java Agent, eBPF 프로브.
  2. **Collector & Processing Layer**: OTel Collector (Receiver ➔ Processor ➔ Exporter).
  3. **Storage Layer**: 분산 추적 저장소(Jaeger/Tempo), 시계열 DB(Prometheus), 로그 저장소(Loki/Elasticsearch).
  4. **Visualization & Analytics Layer**: 서비스 맵(Service Map), 플레임 그래프(Flame Graph), 이상 탐지 알람.

</details>

```text
[APM 플랫폼]
|
+-- [계측 계층]
|   `-- Agent·SDK·eBPF
+-- [수집·처리 계층]
|   `-- OTel Collector
+-- [저장 계층]
|   +-- Trace 저장소
|   +-- Metric 저장소
|   `-- Log 저장소
`-- [분석 계층]
    `-- 서비스 맵·플레임 그래프
```

선의 의미: APM 플랫폼의 계층별 포함 관계

| 구성요소 | 책임 |
|:---|:---|
| 계측 계층 | Agent·SDK로 **Span·메트릭** 생성 |
| 수집·처리 계층 | **OTel Collector** 기반 가공·라우팅 |
| 저장 계층 | 추적·메트릭·로그의 **관측 데이터** 보관 |
| 분석 계층 | 서비스 맵으로 **병목 원인** 시각화 |

#### 한줄 요약
- Collector가 계측 계층과 저장 계층 사이에 끼어들어 가공과 라우팅을 흡수하므로, 저장소나 백엔드를 바꿔도 이미 배포된 애플리케이션을 다시 계측하는 비용이 발생하지 않는다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **APM 분산 트랜잭션 추적 및 병목 진단 5단계 프로세스**:
  1. 클라이언트 요청이 API Gateway로 유입 시 전역 고유 Trace ID 발급
  2. HTTP 헤더(`traceparent`)를 통해 Order Service $\rightarrow$ Payment Service로 문맥 전파
  3. Payment Service 내에서 DB 쿼리 실행 시 DB Span 생성 및 실행 시간 측정
  4. OTel Collector가 지연시간 1초 초과를 감지하고 해당 트레이스를 100% 샘플링
  5. 운영자가 서비스 맵 대시보드에서 붉은색 결제 노드를 클릭하여 슬로우 쿼리 확인

</details>

```text
요청자          서비스 계층        OTel Collector       분석 저장소
  |                  |                    |                    |
  |----------------->| 요청               |                    |
  |                  | 1. 문맥 전파       |                    |
  |                  | 2. Span 계측       |                    |
  |                  |------------------->|                    |
  |                  |                    | 3. 수집·샘플링     |
  |                  |                    |------------------->|
  |                  |                    |                    | 4. 상관 분석
  |<-----------------| 응답               |                    |
```

**동작 원리**

1. **문맥 전파**: Trace ID로 서비스 간 호출 연결
2. **Span 계측**: 서비스·DB 구간별 실행시간 기록
3. **수집·샘플링**: 오류·지연 Trace 선별 보존
4. **상관 분석**: 메트릭·로그·Trace로 병목 원인 식별

#### 한줄 요약
- 모든 Trace를 보존하면 수집·저장 비용이 트래픽에 비례해 늘고 무작위로 버리면 정작 느린 요청이 사라지므로, 갈래는 지연·오류를 만난 Trace만 100% 남기는 선별 지점에서 갈린다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **APM 계측 방식 3대 기술 비교**:
  - Java Agent 바이트코드 계측: JVM 클래스 로딩 시점 훅 (가장 상세, 언어 종속).
  - eBPF 기반 커널 계측: 리눅스 커널 소켓/시스템 콜 후킹 (무설치, 블랙박스).
  - 수동 SDK 코드 계측: 개발자가 직접 OpenTelemetry API 호출 (정밀, 코드 수정 필요).

</details>

| 비교 항목 | Java Agent | eBPF | 수동 SDK |
|:---|:---|:---|:---|
| 적용 기준 | **런타임 상세 분석** | **언어 무관 관측** | **업무 구간 계측** |
| 계측 위치 | **JVM·CLR 런타임** | **Linux 커널** | **애플리케이션 코드** |
| 가시성 | 메서드·SQL의 **상세 추적** | 시스템 호출·패킷의 **흐름 추적** | 업무 로직의 **사용자 정의 Span** |
| 한계 | 언어별 **Agent 종속** | 업무 문맥 **식별 한계** | 코드 수정과 **유지보수 비용** |

#### 한줄 요약
- Java Agent는 상세 함수/SQL 계측, eBPF는 무침습 커널 네트워크 계측, SDK는 커스텀 비즈니스 계측에 특화된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **APM 구축 시 3대 위험 요소와 엔지니어링 대책**:

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 전수 수집으로 **저장 비용·OOM** 증가 | 오류·지연 중심 **꼬리 기반 샘플링** | **수집 비용** 절감 |
| 메시지 큐에서 **Trace Context 단절** | 레코드 헤더에 **traceparent** 전파 | **추적 연속성** 확보 |
| 쿼리 인자에 **PII 노출** | Collector의 **마스킹 필터** 적용 | **개인정보 유출** 방지 |

#### 한줄 요약
- Tail 샘플링으로 비용을 통제하고, Kafka 헤더 전파로 연속성을 유지하며, Collector 마스킹으로 개인정보를 보호한다.

## Ⅶ. 결론

- 이기종 분산 환경은 **OpenTelemetry**, 오류·지연 분석은 **꼬리 기반 샘플링** 적용

#### 한줄 요약
- 전 구간 추적은 원인 규명 시간을 줄이는 대신 계측 오버헤드와 저장 비용을 상시 물리므로, 샘플링 정책이 관측 가능성과 운영비를 조절하는 손잡이가 된다.
