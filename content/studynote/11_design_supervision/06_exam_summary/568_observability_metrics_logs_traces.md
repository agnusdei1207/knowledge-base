---
title: "568. 관측 가능성 메트릭 로그 트레이스 (Observability Metrics Logs Traces)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 관측 가능성(Observability)은 시스템 외부에서 출력된 **Metrics(시계열 수치)**, **Logs(이벤트 레코드)**, **Traces(분산 인과 관계)**의 3축 데이터를 상관 분석하여 내부 상태를 추론하는 엔지니어링 체계이며, OpenTelemetry SDK/Collector/OTLP를 통해 계측(Instrumentation)을 표준화한다.
> 2. **가치**: 컨테이너/MSA 환경에서 평균 탐지 시간(MTTD)을 4시간->15분, 평균 복구 시간(MTTR)을 65% 단축하며, 알 수 없는 장애(Unknown Unknowns)에 대한 근본 원인 분석(RCA) 성공률을 전통적 임계치 기반 모니터링 대비 3배 이상 향상시킨다.
> 3. **판단 포인트**: Pull(Prometheus) vs Push(OTLP) 수집 모델, 카디널리티(High Cardinality) 폭증에 따른 TSDB 비용 최적화, 샘플링 전략(Head-based vs Tail-based 100% Sampling) 선택, 그리고 SRE·AIOps로의 진화 로드맵이 핵심 의사결정 축이다.

---

## Ⅰ. 개요 및 필요성

클라우드 네이티브·MSA·Kubernetes 환경으로 전환되면서, 단일 시스템의 응답 지연이 20개 마이크로서비스의 비동기 호출 체인을 거쳐 발생하는 **다층 의존성(Multi-tier Dependency)** 문제가常态化되었다. 전통적인 SNMP/Nagios 기반의 능동 모니터링(Active Monitoring)은 **"이미 정의된 알려진 장애(Known Unknowns)"**만 탐지할 수 있으며, **알 수 없는 장애(Unknown Unknowns)** 에는 무력하다. 또한 12-Factor App과 같은 Stateless 아키텍처에서는 컨테이너가 5~10초 수명으로 재생성·소멸되므로 IP 기반의 정적 임계치 모니터링은 의미가 없어졌다.

이러한 배경에서 2017년 Twitter의 **Catherine Peters**가 논문 *"Applying Observability to Large-Scale Complex Systems"*를 통해 **관측 가능성(Observability)**을 정량화한 후, CNCF(Cloud Native Computing Foundation)는 2019년 OpenTracing과 OpenCensus를 합병하여 **OpenTelemetry** 프로젝트를 출범시켰다. 현재(v1.40 기준) 자동 계측(Auto-Instrumentation)이 60개 이상 라이브러리를 지원하며, eBPF 기반의 **Pixie**, **Cilium Tetragon** 같은 무침습(Zero-Instrumentation) 기법이 차세대 표준으로 부상하고 있다.

```text
+---------------- 전통적 모니터링(known-unknowns) ----------------+
|  [App]-[Nagios]--정적 임계치---> [Alert]                          |
|            단일 호스트, 동기 호출, IP 기반                       |
|            ✗ 컨테이너 IP 변동, MSA 호출 추적 불가                |
+----------------------------------------------------------------+
                              v 진화
+---------------- 현대 관측 가능성(unknown-unknowns) -------------+
| [Svc-A]-[Svc-B]-[Svc-C]-[Kafka]-[DB]                            |
|    |        |        |       |      |                           |
|    v        v        v       v      v                           |
| [OTel SDK] ---- OTLP(4317/gRPC, 4318/HTTP) -----> [OTel Col]   |
|                                                  +-Metrics->Prom |
|                                                  +-Logs ->Loki  |
|                                                  +-Traces->Tempo|
+----------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 전통적 모니터링이 **자동차 계기판(속도·RPM·연료)**이라면, 관측 가능성은 **항공기의 블랙박스·비행 데이터 기록기·엔진 센서 300종**이 통합되어, 기체가 흔들리는 *원인*(난기류? 엔진? 조종?)을 사후에 역추적하는 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

관측 가능성은 **데이터 수집 계층(Instrumentation) -> 전송 계층(Transport) -> 저장·분석 계층(Storage/Analytics) -> 시각화·자동화 계층(Visualization/Automation)**의 4계층으로 구성된다. OpenTelemetry의 **Context Propagation**(W3C Trace Context 표준, `traceparent`, `tracestate` 헤더)이 모든 계층을 관통하는 **식별자(ID) 그래프** 역할을 수행한다.

```text
                       [Application / Sidecar / eBPF Probe]
                                    | auto/manual instr.
                                    v
        +--------------- OpenTelemetry SDK ---------------+
        |  +-Tracer API--+  +-Meter API--+  +-Logger API-+ |
        |  | Span 생성    |  | Counter    |  | 구조화 로그 | |
        |  | Baggage 전파 |  | Histogram  |  | Trace 연동 | |
        |  +------+-------+  +------+-----+  +-----+------+ |
        +---------+-----------------+---------------+--------+
                  | OTLP/gRPC (port 4317)            |
                  | OTLP/HTTP (port 4318)            |
                  v                                  v
        +---------------- OpenTelemetry Collector -----------------+
        |  Receivers  ->  Processors  ->  Exporters                  |
        |  (otlp/zipkin) (batch, tail-  (prometheus/loki/         |
        |   jaeger)      sampling,     jaeger/datadog/s3)         |
        |                 attributes)                               |
        +--------+-------------+----------------+------------------+
                 v             v                v
        +-------------+ +--------------+ +-----------------+
        | Prometheus  | | Elasticsearch| |   Jaeger/Tempo  |
        | Mimir/Cortex| | Loki/Splunk  | |  Zipkin/Honeycomb|
        +------+------+ +------+-------+ +--------+--------+
               |              |                   |
               +--------------+-------------------+
                              v
                      +---------------+
                      |   Grafana /   | <- PromQL, LogQL, TraceQL
                      |   Kibana/     |
                      |   Datadog APM |
                      +---------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Metrics(메트릭)** | 시스템 상태의 **집계된 정량 수치**. CPU 80%, RPS 1200, p99 latency 450ms 등 | **Counter**(단조 증가), **Gauge**(증감), **Histogram**(분포), **Summary**(분위수). 카디널리티 ≤ 10을 권고하며, PromQL `rate()`, `histogram_quantile()`로 SLO 산출. RED 메서드(Rate·Errors·Duration), USE 메서드(Utilization·Saturation·Errors) 적용 |
| **Logs(로그)** | 이산 이벤트(Discrete Event)의 구조화 레코드. 단일 발생 사실의 맥락(context) | **구조화 로깅**(JSON/Logfmt) 필수. ECS(Elastic Common Schema), OTel Semantic Conventions 표준. 레벨(TRACE/DEBUG/INFO/WARN/ERROR/FATAL), MDC(Mapped Diagnostic Context), TraceID/spanID 필드 포함 시 Logs↔Traces 양방향 점프 가능 |
| **Traces(트레이스)** | 분산 요청의 **인과 관계 DAG**(Directed Acyclic Graph). 한 사용자 요청이 거치는 모든 서비스·스팬의 호출 그래프 | **Trace(64-bit ID)** > **Span(작업 단위)** > **Parent-Child 관계**. W3C `traceparent` 헤더(`00-{trace_id}-{span_id}-{flags}`)로 전파. Baggage는 사용자 정의 K-V 컨텍스트 전파. **Context Propagation**이 MSA 통합의 핵심 |
| **OpenTelemetry Collector** | 수집·처리·라우팅 파이프라인. Vendor 중립적 게이트웨이 역할 | **Receiver(43종)** -> **Processor(batch, memory_limiter, tail_sampling, attributes, k8sattributes)** -> **Exporter(40종)**. Stateful(예: `statefulset`) 또는 Agent/Sidecar/Gateway 3가지 배포 토폴로지 선택 |

핵심 알고리즘 및 파라미터:
- **Cumulative Flow Diagram vs Histogram**: Counter는 `rate()`로 1초당 증가율 환산. Histogram Bucket은 `le`(less-or-equal) 경계값으로 정의하며, Prometheus 기본 Bucket은 `0.005, 0.01, 0.025, ..., 10` (11개).
- **Tail-based Sampling**: 100% 수집 후 Collector에서 N개/초 샘플링, 또는 `status_code=ERROR` 같은 조건부 보존. 비용은 10배 절감되나 Trace Completion Latency가 5~10초 증가.
- **Cardinality 제어**: `http_status_code`(10) × `method`(5) × `path`(1000) = 50,000 시계열. `user_id`, `email` 같은 High-Cardinality 라벨은 **Span Attribute나 Log Field**로 옮기고 Metric Label에서는 제외.

- **📢 섹션 요약 비유**: Metrics는 **건강검진 수치**(혈압·콜레스테롤), Logs는 **진료 기록**(언제 아픈지·증상), Traces는 **MRI 영상**(몸속 혈관·신경의 흐름을 따라가며 원인 질환 위치 파악)이다. 셋이 동시에 갖춰야만 의사가 정확한 진단을 내릴 수 있다.

---

## Ⅲ. 비교 및 연결

| 구분 | 전통적 모니터링(Monitoring) | 관측 가능성(Observability) |
| :--- | :--- | :--- |
| **데이터 신호** | 주로 단일 Metric(임계치) | Metrics + Logs + Traces 3축 융합 |
| **장애 유형** | Known-unknowns(예상 가능한 임계치 초과) | Known + **Unknown-unknowns**(처음 보는 패턴) |
| **아키텍처 가정** | 정적 호스트, 동기 호출, 영속 IP | 동적 컨테이너, 비동기, 무상태, IP 변동 |
| **상관 분석** | 수동 대시보드, 룰 기반 | 자동 상관(Correlation), Trace↔Log 점프, AIOps 추론 |
| **비용·노력** | 낮음(임계치 룰 수십 개) | 높음(계측 표준화, 카디널리티 관리, SRE 역량) |
| **대표 도구** | Nagios, Zabbix, Cacti | **OpenTelemetry + Grafana 스택, Datadog, Honeycomb, Dynatrace** |
| **표준화** | SNMP, syslog, WMI 등 도구별 파편화 | **OpenTelemetry(CNCF Graduated 2025)**, W3C Trace Context, OTel Semantic Conventions |
| **Alerting** | 정적 임계치(예: CPU>90% 5분) | 동적 베이스라인 + SLO 기반 오류 예산(Burn Rate) Alert |
| **근본 원인** | 1계층(단일 서비스) | N계층(전체 호출 체인), Baggage로 비즈니스 컨텍스트 추적 |
| **필수 역량** | Sysadmin, NOC | **SRE**, Platform Engineer, Observability Engineer |

다른 시스템 영역과의 연결:
- **SRE/SLI·SLO·Error Budget**: Observability 데이터가 SLI 산출의 원천. `availability = 1 - (sum(rate(errors[28d])) / sum(rate(total[28d])))`.
- **AIOps·DevOps**: Datadog Watchdog, Grafana ML, Elastic ML이 이상치 탐지(Anomaly Detection)에 활용.
- **Chaos Engineering**: LitmusChaos, Gremlin로 주입한 장애가 Traces에 어떻게 표현되는지 관찰.
- **보안(Observability-Driven Security)**: Falco, Tetragon으로 런타임 보안 이벤트를 Trace/Log 신호로 통합.

- **📢 섹션 요약 비유**: 모니터링이 **CCTV의 정적 화면**(움직임 감지만), 관측 가능성은 **CCTV + 출입 기록 + 발자국 + CCTV 녹화본 + 얼굴 인식 AI**가 결합된 **통합 수사관 시스템**이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **계측 표준화 여부**: OpenTelemetry SDK를 단일 표준으로 채택했는가? Datadog APM, New Relic 같은 **Vendor-Specific Agent**에 종속되어 Lock-in이 발생하고 있지 않은가? 기술사 답안에서는 **OTel -> Vendor Agnostic -> 비용 협상력** 인과를 명시해야 한다.
2. **3축 데이터 상관(Correlation) 전략**: `trace_id`, `span_id`를 Log/Metric 레코드에 자동으로 주입하여 Grafana의 **Correlations** 기능, Elastic의 **Service Map**, Datadog의 **Trace↔Log 양방향 점프**가 가능한가? 상관되지 않은 3축은 데이터 사일로(Silo)다.
3. **카디널리티 거버넌스**: `user_id`, `order_id` 등 High-Cardinality 필드를 Metric Label로 사용하고 있지 않은가? 라벨 카디널리티 합산이 **TSDB Shard 수 × 샘플 수** 비용을 지수적으로 증가시킨다. 예: 라벨 3개×1000×1000 = 10억 시계열 -> 일 1TB 인덱스 폭증.
4. **샘플링 정책의 경제성**: 100% 샘플링 시 트래픽 1K RPS × 평균 20 Span/요청 = 20K Span/s -> 일 17억 Span. **Tail-based Sampling + Error/High-Latency 우선 보존**(예: p99 임계치 초과 Span 무조건 저장) 전략을 적용했는가?
5. **비용·성능 트레이드오프**: eBPF 기반 **Pixie/Parca**로 코드 변경 없이 계측하여 SDK 오버헤드(평균 2~5% CPU)를 제거할 수 있는가? 단, eBPF 커널 버전 요구(4.19+)와 **커널 크래시 리스크**를 동시에 검토.

### 피해야 할 안티패턴

- **로그 폭격(Log Bombing)**: 디버깅 편의를 위해 INFO 레벨로 전 요청의 Request Body·Response Body를 저장 -> 일 10TB 로그 폭증, GDPR·PII 위반. ⇒ 구조화 로깅 + 샘플링 + 필드 마스킹 적용.
- **메트릭 황무지(Metric Desert)**: 모든 호출에 대한 메트릭을 생성하여 동일 정보 중복. **4 Golden Signals**(Latency, Traffic, Errors, Saturation) + **RED/USE**로 최소 집합 유지.
- **스팬 폭주(Span Explosion)**: 내부 라이브러리 함수마다 Span 생성 -> 1 요청당 500+ Span. ⇒ 자동 계측(Auto-Instrumentation) 기본 사용, 수동 Span은 **비즈니스 경계(Boundary)** 단위로만.
- **단일 신호 의존(Metric-only or Log-only 사고)**: 한 축만으로 SLA를 증명하려 함. SRE 원칙상 **3축 모두**가 있어야 가설-검증 사이클이 작동.
- **수동 임계치의 만성화**: `CPU>80%` 룰 100개로 1년 운영 -> 알림 피로(Alert Fatigue) -> 실제 장애 무시. ⇒ **Multi-Window Multi-Burn-Rate Alert**(Google SRE Workbook 5장) 채택.

- **📢 섹션 요약 비유**: 안티패턴은 **온도계 1000개를 환자에게 부착하는 의사**와 같다. 데이터가 많다고 진단이 좋아지는 게 아니라, **맥락이 있는 신호 3종**이 정밀 진단
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 568 / 600

<- **이전**: [567. 멱등성 설계 중복 요청 처리](/studynote/11_design_supervision/06_exam_summary/568_idempotency_design_duplicate_request_han/)
**다음**: [569. SRE 에러 버짓 토일 자동화](/studynote/11_design_supervision/06_exam_summary/569_sre_error_budget_toil_automation/) ->

---
