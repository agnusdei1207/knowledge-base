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
- **개요**: **OpenTelemetry(OTel)**는 메트릭·로그·트레이스를 계측(instrument)·수집·가공·전송하기 위한 **CNCF 벤더 중립 관측성 표준**이다.
- **왜 필요한가**: 벤더 전용 APM agent만 쓰면 도구를 바꿀 때마다 애플리케이션 코드의 계측 부분을 다시 심어야 한다. OTel은 "계측은 표준으로 한 번, 전송 대상은 언제든 교체"를 가능하게 한다.
- **핵심 직관**: 항공사마다 다르던 수하물 태그를 국제표준 바코드로 통일해, 어느 공항 스캐너로도 같은 짐을 추적하게 만드는 것과 같다.

## 핵심 용어 정리

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| OpenTelemetry(OTel) | 관측 데이터 생성·수집·전송의 벤더 중립 표준 — 이 개념의 정체성 | 만국 공통 수하물 태그 규격 |
| API/SDK | 애플리케이션이 span·metric·log를 만드는 언어별 라이브러리 | 태그를 붙이는 프린터 |
| Instrumentation(계측) | 코드에 관측 지점을 심는 것(auto 자동/manual 수동) | 짐마다 태그를 붙이는 작업 |
| Collector | 신호를 수신·가공·전송하는 별도 프로세스(Receiver→Processor→Exporter) | 공항의 중앙 분류 컨베이어 |
| OTLP | OpenTelemetry Protocol — 표준 전송 프로토콜(gRPC/HTTP) | 태그를 읽는 공통 스캐너 규격 |
| Semantic Convention | 속성 이름을 표준화한 명명 규칙(예: http.status_code) | 모든 공항이 같은 필드명으로 짐 정보를 적는 규칙 |
| Context Propagation | 서비스 경계를 넘어 trace 문맥을 전달하는 것 | 환승할 때도 같은 수하물 번호가 따라가는 것 |
| Resource | 신호를 만든 주체를 식별하는 속성(service.name 등) | 짐에 붙은 소유자 이름표 |

## 깊이 이해

### 왜 만들어졌나 — OpenTracing + OpenCensus 통합
- 2019년 이전에는 트레이싱 표준(OpenTracing)과 메트릭·트레이싱 SDK(OpenCensus)가 따로 있어 라이브러리 개발자가 둘 중 하나만 지원하면 사용자가 갈라졌다. 두 프로젝트가 합쳐져 OpenTelemetry가 되었고 지금은 메트릭·로그·트레이스 3대 신호를 모두 표준화한다.

### 계측 → Collector → Backend, 수치로 흐름 이해
- 자바 결제 서비스에 OTel Java agent(자동 계측)를 붙이면 HTTP server span, DB client span, JVM GC metric이 코드 수정 없이 생성된다. 여기에 "결제 승인 금액" 같은 업무 속성은 manual instrumentation으로 한 줄 추가한다.
- 이 신호들은 OTLP(포트 gRPC 4317 / HTTP 4318)로 Collector에 전송된다. Collector가 초당 10,000 span을 받는다고 하면, tail sampling processor가 에러이거나 900ms를 넘는 span만 보존해 최종 backend 저장량을 원래의 5~10% 수준으로 줄인다.
- 이후 exporter가 Tempo(트레이스), Prometheus(메트릭) 등 서로 다른 backend로 동시에 내보낼 수 있다 — 코드는 한 번만 계측했는데 backend는 자유롭게 교체·복수 운용이 가능한 이유가 이 Collector 계층의 분리 구조다.

### Semantic Convention이 왜 필요한가
- 서비스 A가 지연 속성을 `latency_ms`로, 서비스 B가 `duration`으로 각자 이름 붙이면 backend에서 서비스 간 비교 쿼리가 불가능하다.
- OTel은 `http.request.method`, `http.response.status_code`, `db.system`처럼 이름을 표준화해, 어느 언어·프레임워크로 계측했든 같은 필드로 조회·집계할 수 있게 한다.

### Context Propagation — traceparent 형식
- 서비스 간 호출에서 문맥을 전달하지 않으면 trace가 서비스 경계에서 끊긴다. OTel은 W3C Trace Context 표준의 `traceparent` HTTP 헤더로 이를 해결한다.
- 형식은 `버전-traceid(32자리 16진수)-spanid(16자리 16진수)-flags(2자리)`다. 예: `00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01` — 맨 끝 `01`은 "이 trace를 샘플링해서 기록하라"는 플래그다. 이 한 줄만 다음 서비스로 전달되면 어디서든 같은 trace에 span을 이어붙일 수 있다.

### 비유와 흔한 오해
- **비유**: 여러 항공사가 각자 다른 수하물 태그를 쓰던 시절엔 환승할 때마다 짐을 새로 등록해야 했다. 국제표준 바코드로 통일하니 어느 공항 스캐너(backend)로도 같은 짐(요청)을 추적할 수 있게 된 것이 OTel이다.
- **오해**: OpenTelemetry는 대시보드나 저장소 제품이 아니다. 데이터를 표준 형식으로 만들고 나르는 계측·전송 계층일 뿐이고, 실제 저장·조회·알림은 Prometheus, Tempo, Jaeger 같은 별도 backend가 담당한다.

## 연결 개념
- Cloud Native Observability — OTel이 표준화해서 채워주는 3대 신호 체계(188에서 상세)
- Distributed Tracing — OTel의 trace API·context propagation이 구현하는 대상(190에서 상세)
- SRE — OTel로 수집한 신호가 SLI 측정의 데이터 소스가 됨(191에서 상세)

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
