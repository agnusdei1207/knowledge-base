---
title: "OpenTelemetry (OpenTelemetry)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 276
---

# 📖 【암기용】 개념 완전 이해

> 목적: OpenTelemetry를 관측 데이터를 생성·수집·전송하는 벤더 중립 표준으로 이해하게 만든다.

## 한눈에
- **개요**: 애플리케이션 telemetry를 표준 API, SDK, Collector, OTLP로 수집·전송하는 CNCF 관측성 프레임워크
- **왜 필요한가**: MSA와 Kubernetes는 서비스·Pod·노드가 계속 바뀌므로 벤더별 에이전트만 붙이면 trace, metric, log 상관분석이 끊어진다.
- **핵심 직관**: 병원 검사 장비가 제조사마다 달라도 표준 검사 항목과 전송 형식으로 의무기록에 모으는 방식이다.

## 깊이 이해
- **배경·문제의식**: OpenTracing과 OpenCensus는 분산 추적과 telemetry 표준화를 각각 추진했으나, 운영 현장에서는 코드 계측과 backend 전송 방식이 분리되어 이식 비용이 컸다.
- **작동 원리**: 애플리케이션은 OTel API/SDK로 trace, metric, log를 만들고 Collector는 수신, 처리, 내보내기 파이프라인으로 여러 backend에 전달한다.
- **비유**: 택배 송장 양식을 표준화하면 택배사가 바뀌어도 발송자, 수신자, 운송 경로 정보를 같은 방식으로 추적할 수 있다.
- **구체 예시**: checkout 요청에 trace id를 부여하고 payment span, DB query metric, 오류 log를 같은 trace context로 연결해 장애 범위를 확인한다.
- **흔한 오해·주의점**: OpenTelemetry는 저장소나 대시보드 제품이 아니다. Prometheus, Tempo, Jaeger, 상용 APM으로 보내기 전 계측·수집 표준을 제공한다.

## 연결 개념
- Distributed Tracing — trace id와 span으로 요청 경로를 추적
- Cloud Native Observability — OTel이 telemetry 표준 수집 계층 담당
- SRE/SLO — OTel telemetry를 사용자 영향 지표로 해석

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: OpenTelemetry는 관측 backend가 아니라 계측 표준과 Collector pipeline으로 벤더 종속을 낮추는 운영 기반이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: OpenTelemetry는 traces, metrics, logs를 생성·수집·전송하는 CNCF 벤더 중립 관측성 표준임.
> 2. **가치**: SDK와 Collector를 표준화해 APM 교체, 멀티 backend 전송, MSA trace context 전파를 코드 재작성 없이 처리함.
> 3. **판단 포인트**: 계측 범위, Collector 배치, OTLP 전송, sampling, attribute cardinality를 함께 설계해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 관측성 표준 이해 확인 | API, SDK, Collector, OTLP, signal | APM 제품명 나열로 축소 |
| MSA 운영 설계 확인 | trace context, span, metric, log 상관관계 | 로그 수집기와 동일시 |
| 벤더 중립 판단 확인 | backend 독립, exporter, sampling | 저장소 기능을 OTel 기능으로 오기 |

> 요약: 이 문제는 OpenTelemetry를 계측 표준, 수집 파이프라인, backend 독립성 관점으로 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 벤더 중립 telemetry 표준
- 배경: MSA와 Kubernetes에서는 서비스 호출 경로와 workload 위치가 계속 바뀌어 backend별 에이전트 계측이 운영 부담을 만든다.
- 필요성: trace, metric, log를 OTLP와 Collector로 표준화해 도구 교체와 멀티 backend 전송을 가능하게 해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Application -> OTel API / SDK -> Exporter -> Collector
Collector -> Receiver -> Processor -> Exporter -> Observability Backend
Context Propagation -> Trace / Metric / Log Correlation
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| API/SDK | 코드 계측과 signal 생성 | manual, auto instrumentation |
| OTLP | telemetry 전송 프로토콜 | gRPC, HTTP 지원 |
| Collector | 수집·가공·전송 중계 | receiver, processor, exporter |
| Backend | 저장·조회·시각화 | Prometheus, Jaeger, Tempo 등 |

> 요약: OpenTelemetry는 애플리케이션 계측부터 Collector 전송까지를 표준화하고 저장·분석 backend는 선택 가능하게 둔다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요청 수신 -> trace context 생성 -> span / metric / log 기록
-> SDK export -> Collector receive -> batch / filter / sample
-> backend export -> dashboard / alert / trace 분석
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | API/SDK가 span, metric, log record 생성 | instrumentation coverage |
| 2 | trace context를 HTTP header, message metadata로 전파 | propagation success rate |
| 3 | Collector가 batch, filter, sampling 수행 | dropped telemetry count |
| 4 | exporter가 backend별 형식으로 전송 | export error rate |

> 요약: OTel은 서비스 요청에 context를 붙이고 각 signal을 Collector pipeline으로 보내 backend 분석으로 연결한다.

---

## Ⅳ. 특징

| 구분 | 내용 | 판단 포인트 |
|:---|:---|:---|
| 표준성 | API, SDK, OTLP, Collector를 공개 규격으로 제공 | backend 교체 가능성 |
| 확장성 | receiver, processor, exporter 조합으로 pipeline 구성 | 멀티 backend 전송 |
| 운영 리스크 | attribute cardinality와 sampling 정책 미흡 시 저장 비용 증가 | label allowlist |
| 적용 한계 | 계측 누락 서비스는 trace 경로가 끊김 | instrumentation coverage |

> 요약: OpenTelemetry의 가치는 벤더 중립 계측과 Collector pipeline이며, cardinality와 계측 누락을 설계 단계에서 통제해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | OpenTelemetry | 선택 기준 |
|:---|:---|:---|:---|
| 계측 | 벤더별 agent | 표준 API/SDK | APM 교체 가능성 |
| 전송 | backend 직접 전송 | Collector 중계 | 멀티 backend, 필터링 |
| 운영 | 도구별 설정 분산 | pipeline 정책 통합 | sampling, attribute 정책 |

> 요약: 조직이 여러 관측 backend를 쓰거나 APM 교체 가능성을 요구하면 OTel Collector 중심 구성이 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Trace 단절 | context header 미전파 | gateway, service, broker 전파 규칙 적용 | orphan span ratio |
| 비용 증가 | 고유값 attribute 사용 | attribute allowlist, aggregation | time series count |
| 데이터 손실 | Collector 과부하 | batch size, queue, retry 설정 | dropped spans, export failures |

> 요약: OTel 운영 리스크는 context, cardinality, Collector 처리량이며 pipeline 지표로 지속 점검한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 계측 범위 | 핵심 API 90% 이상 trace 생성 | endpoint inventory 대조 |
| 전송 품질 | export error rate 1% 이하 | Collector self metric |
| 비용 통제 | series 수 예산 이내 | backend cardinality report |

> 요약: 도입 성과는 계측 범위, Collector 전송 오류, telemetry cardinality로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 핵심 서비스부터 OTel SDK 또는 auto instrumentation을 적용하고 HTTP, gRPC, message broker에 trace context 전파를 표준화함.
2. Collector를 sidecar, daemonset, gateway 중 workload 특성에 맞게 배치하고 processor에서 batch, filter, tail sampling을 적용함.
3. service.name, environment, version 등 공통 attribute를 표준화하고 user_id 같은 고유값 attribute는 수집 제외함.

**결론 (2줄):**
- 기술사 판단: MSA·Kubernetes 환경에서는 OpenTelemetry를 계측 표준으로 두고 backend는 SLO·비용·보존기간 기준으로 선택함.
- 향후 방향: OTel은 eBPF telemetry, profiling, AIOps 분석과 결합되어 표준 관측 데이터 계층으로 확대됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "OpenTelemetry를 설명하시오" | API/SDK, Collector, OTLP 동작 흐름 | 벤더 중립성과 적용 한계 |
| 요구사항 명시형 | "MSA 관측성 표준화 방안을 제시하시오" | trace context 전파와 Collector pipeline | sampling, cardinality, backend 선택 기준 |

> 요약: 설명형은 구성 표준을, 방안형은 계측 범위와 Collector 운영 정책을 중심으로 작성한다.
