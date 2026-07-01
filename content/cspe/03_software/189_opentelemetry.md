---
title: "OpenTelemetry (OpenTelemetry)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 189
---

# 📖 【암기용】 개념 완전 이해

> 목적: OpenTelemetry를 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 메트릭, 로그, 트레이스를 수집·전송하기 위한 벤더 중립 관측성 표준
- **왜 필요한가**: APM 도구마다 SDK와 데이터 형식이 다르면 서비스 변경과 도구 교체 때 계측을 반복해야 한다.
- **핵심 직관**: 여러 택배사가 쓰던 송장 양식을 표준 송장으로 통일해 배송 추적을 어느 시스템에서도 읽게 하는 방식이다.

## 깊이 이해
- **배경·문제의식**: 분산 시스템은 요청이 여러 언어와 플랫폼을 지나간다. 각 벤더 전용 에이전트만 쓰면 계측 방식이 흩어지고 데이터 이동성이 떨어진다.
- **작동 원리**: 애플리케이션은 OTel SDK와 auto-instrumentation으로 span, metric, log를 생성하고, Collector가 수신, 처리, 샘플링, 변환 후 OTLP나 vendor exporter로 backend에 전송한다.
- **비유**: 공항 수하물 태그를 표준화해 항공사와 공항이 바뀌어도 이동 경로를 추적하는 구조이다.
- **구체 예시**: Java 서비스에 OTel agent를 적용해 HTTP server span, DB client span, JVM metric을 생성하고 Collector에서 tail sampling 후 Tempo와 Prometheus로 전송한다.
- **흔한 오해·주의점**: OpenTelemetry는 저장소나 대시보드 제품이 아니다. 수집 표준과 파이프라인이며, backend 선택, cardinality, sampling, PII 제거는 별도 설계가 필요하다.

## 연결 개념
- Cloud Native Observability - OTel이 구현하는 수집 표준
- Distributed Tracing - OTel trace API와 context propagation
- OTLP - OpenTelemetry Protocol

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: OpenTelemetry 답안은 SDK, Collector, OTLP, exporter, sampling, semantic convention을 함께 제시해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: OpenTelemetry는 metric, log, trace를 생성·수집·처리·전송하는 CNCF 벤더 중립 관측성 표준임.
> 2. **가치**: SDK와 Collector를 통해 애플리케이션 계측과 backend 전송을 분리해 APM 교체와 멀티 백엔드 전송을 가능하게 함.
> 3. **판단 포인트**: auto/manual instrumentation, Collector pipeline, OTLP, semantic convention, sampling, PII filtering을 기준으로 설계해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 관측성 표준 이해 확인 | SDK, API, Collector, OTLP, exporter | APM 제품으로 오해 |
| 분산 추적 적용 확인 | context propagation, span, trace_id | 로그 수집 도구로 축소 |
| 운영 설계 확인 | sampling, attribute, processor, backend | 비용·개인정보 처리 누락 |

> 요약: 이 문제는 OTel을 수집 표준과 처리 파이프라인으로 설명해야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: 관측성 데이터 수집 표준
- 배경: 클라우드 네이티브 환경은 언어와 벤더가 혼재해 도구별 계측이 운영 부담이 된다.
- 필요성: OTel SDK, Collector, OTLP로 데이터 생성과 저장소를 분리해 관측 데이터 이식성을 확보한다.

---

## Ⅱ. 구조 및 구성요소

```text
Application -> OTel SDK/Agent -> OTel Collector -> Processor -> Exporter -> Backend
  / Signals: trace, metric, log
  / Protocol: OTLP
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| API/SDK | span, metric, log 생성 | 언어별 구현 |
| Auto Instrumentation | 코드 변경 최소화 계측 | Java agent, Python instrumentation |
| Collector | 수신, 처리, 라우팅 | receiver, processor, exporter |
| OTLP | 표준 전송 프로토콜 | gRPC, HTTP |

> 요약: OpenTelemetry는 애플리케이션 계측과 Collector 파이프라인을 분리해 backend 선택 자유도를 확보함.

---

## Ⅲ. 동작원리 및 흐름도

```text
요청 수신 -> context 추출 -> span/metric/log 생성 -> OTLP 전송 -> collector 처리 -> backend export
  / sampling 적용 -> 비용 통제
  / attribute filter -> PII 제거
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | SDK가 trace context를 추출 또는 생성 | traceparent 전파율 |
| 2 | span, metric, log record 생성 | semantic attribute 준수 |
| 3 | OTLP로 Collector에 전송 | export failure 1% 이하 |
| 4 | processor가 sampling, batch, filter 수행 | dropped span 비율 |
| 5 | exporter가 backend로 전달 | backend ingest success |

> 요약: OTel은 context 전파부터 Collector 처리와 backend 전송까지 표준 파이프라인으로 동작함.

---

## Ⅳ. 특징

| 구분 | 벤더 전용 APM | OpenTelemetry | 수치/판단 포인트 |
|:---|:---|:---|:---|
| 계측 | 제품별 SDK | 표준 API/SDK | 언어 3종 이상 적용 |
| 전송 | 벤더 프로토콜 | OTLP | multi-exporter 구성 |
| 처리 | backend 의존 | Collector processor | sampling, filter, batch |
| 이동성 | 교체 비용 큼 | backend 분리 | exporter 교체 시간 |

> 요약: OpenTelemetry는 계측과 저장소를 분리해 관측 데이터의 표준화와 이식성을 제공함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | APM agent 직접 전송 | SDK -> Collector -> backend | 멀티 backend, 벤더 교체 |
| 비용/처리 | 전체 trace 저장 | sampling/filter 처리 | trace volume 예산 |
| 운영/위험 | vendor lock-in | OTLP 표준 | 조직 표준 계측 필요 |

> 요약: 여러 언어와 관측 backend가 공존하면 OTel Collector 중심 구조가 적합함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 데이터 폭증 | span attribute 과다 | sampling, attribute allowlist | ingest volume |
| PII 노출 | log/attribute 필터 누락 | processor filter, masking | PII 검출 0건 |
| 계측 누락 | 일부 서비스 미적용 | auto instrumentation, coverage 점검 | trace coverage |

> 요약: OTel 리스크는 수집량, 개인정보, 계측 누락을 Collector 정책으로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 적용 | trace coverage 95% 이상 | backend service map |
| 품질 | export failure 1% 이하 | Collector metric |
| 비용 | ingest volume 예산 준수 | backend billing, Collector metric |

> 요약: OpenTelemetry 운영은 coverage, export 실패율, ingest volume으로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 계측 표준화: Java, Node.js, Python 서비스에 OTel auto instrumentation을 적용하고 핵심 업무 span은 manual instrumentation으로 보강
2. Collector 파이프라인 구성: receiver, batch, tail sampling, attribute filter, OTLP exporter를 표준 Helm chart로 배포
3. 거버넌스 적용: semantic convention, PII attribute denylist, trace coverage 95% 이상, export failure 1% 이하를 운영 기준으로 설정

**결론 (2줄):**
- 기술사 판단: 관측성 도구가 여러 개이거나 벤더 종속을 줄여야 하면 OpenTelemetry를 수집 표준으로 채택함
- 향후 방향: OTel Logs 안정화, eBPF auto-instrumentation, profiling 신호가 통합 관측성 파이프라인으로 확장됨

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "OpenTelemetry를 설명하시오", "기술하시오" | context 전파, Collector, OTLP 전송 흐름 | 벤더 APM 대비 표준화 |
| 요구사항 명시형 | "관측성 플랫폼을 설계하시오", "도입 방안을 제시하시오" | sampling, filter, exporter pipeline | coverage, 비용, PII 통제 |

> 요약: 설명형은 표준 구성, 설계형은 Collector 정책과 운영 지표 중심으로 전환함.
