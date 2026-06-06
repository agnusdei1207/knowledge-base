---
title: "Performance Audit Load Test Bottleneck"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 성능 감리는 SLA 기반 정량 지표(TPS/P95/Error%)와 USE/RED 방법론을 결합해 시스템의 처리율(λ), 응답시간(W), 동시사용자(L) 간의 Little's Law(L=λW) 관계를 정합성 있게 검증하는 엔지니어링 감사이며, 부하 테스트는 가상의 사용자 행위(Vuser+Think Time)를 합성하여 운영 부하의 N배(통상 1.5~3배) 수준으로 재현하는 능동적 스트레스 가시화 기법이다.
> 2. **가치**: 정밀한 병목 진단을 통해 CPU Steal-Time, GC Pause, DB Lock-wait, I/O Await, Connection Pool 고갈 같은 5대 자원 결핍 현상을 조기 식별하고, 일반적으로 인프라 증설 대비 3~10배 효율적인 코드/쿼리/아키텍처 개선안 도출로 MTTR 단축 및 TCO 절감(평균 25~40%)을 실현한다.
> 3. **판단 포인트**: "측정 없는 튜닝은 무의미"라는 원칙 하에, (a) 합성 부하(Synthetic) vs 실 트래픽(Replay) 선택, (b) Open-Loop(처리량 고정) vs Closed-Loop(동시성 고정) 모델링, (c) 캐리어/무선 구간 등 Last-Mile 한계 인지, (d) Warm-up 미반영으로 인한 Cold-Start 오판 회피가 핵심 의사결정 분기점이다.

---

## Ⅰ. 개요 및 필요성

성능 감리(Performance Audit)는 정보시스템의 발주자 관점에서 구축·운영 단계에서 SLA(Service Level Agreement)와 성능 요구사항(PRS, Performance Requirements Specification)의 이행 여부를 객관적으로 검증하는 제도적 절차다. 한국의 「정보시스템 감리 기준」(행정안전부 고시)과 「소프트웨어 진흥법」에 따라 5억 원 이상 공공정보시스템은 제3자 감리법인에 의한 성능 감리가 의무화되며, 이는 단순 인프라 사양 점검을 넘어 **트랜잭션 응답시간, 동시사용자 처리능력, 자원 사용률, 가용성**을 종합 평가하는 통합 엔지니어링 활동이다.

부하 테스트(Load Test)는 이러한 감리의 핵심 증거 수집 수단으로, JMeter·Gatling·nGrinder·k6·Locust 같은 합성 트래픽 생성기(Load Generator)를 이용해 운영 시나리오를 모사한다. 그러나 "부하 테스트를 했는데 왜 장애가 났는가?"라는 질문에 답하려면 **병목 진단(Bottleneck Diagnosis)** 능력이 필수다. 병목은 일반적으로 (1) Front-end(브라우저 렌더링·CDN), (2) Network(L4/L7·SSL·DNS), (3) Web/App Tier(Thread Pool·Lock Contention), (4) Middleware(JVM Heap·Connection Pool), (5) DB(Plan·Index·Lock), (6) Infra(CPU·I/O·NIC) 중 한 곳에 집중된다.

과거(2000년대)에는 인프라 스펙을 단순 나열하고 "서버 4대로 충분"이라는 결론만 내렸다면, 현재(2020년대)는 **Observability 3요소(Logs/Metrics/Traces)**와 **USE(Utilization-Saturation-Errors)·RED(Rate-Errors-Duration) 방법론**, **Distributed Tracing**을 통해 코드 라인 단위 병목을 추적한다. 클라우드·MSA 환경에서는 한 API 호출이 30개 이상의 마이크로서비스를 거치므로, 전통적 APM(APplication Performance Monitoring)만으로는 인과관계 파악이 불가능하며, OpenTelemetry 기반 통합 가시화가 표준으로 자리잡았다.

```text
+----------------------------------------------------------------------+
|            성능 감리(Performance Audit) 전체 흐름도                   |
+----------------------------------------------------------------------+
                            |
        +-------------------+-------------------+
        v                   v                   v
   [1. 계획]           [2. 측정]            [3. 진단]
   ----------         ----------          ----------
   • SLA 정의          • 부하 테스트        • USE Method
   • PRS 작성          • APM 데이터 수집    • RED Method
   • 시나리오 설계     • 프로파일링         • 병목 지점 식별
   • 데이터 셋업       • 로그/트레이스      • 인과 분석
        |                   |                   |
        v                   v                   v
   KPI: TPS, P95,       KPI: 실측치         KPI: 병목 Resource
   동시성, 가용성       (Bottleneck 추적)   개선안 도출
        |                   |                   |
        +-------------------+-------------------+
                            |
                            v
                    [4. 보고 및 판정]
                    -------------
                    • 적합 / 조건부 / 부적합
                    • 증설/튜닝 권고
                    • 수용 기준(SLO) 매핑
```

- **📢 섹션 요약 비유**: 성능 감리는 마치 **종합건강검진**과 같다. 혈액검사(부하 테스트)로 간수치·콜레스테롤(응답시간·처리율)을 측정하고, CT·MRI(APM/Tracing)로 정밀 부위(병목 지점)를 찾아, 결국 생활습관 개선(아키텍처 튜닝)을 처방하는 일련의 의료 절차다.

---

## Ⅱ. 아키텍처 및 핵심 원리

성능 감리 및 부하 테스트는 **발주처 -> 감리법인 -> 구축사**의 3자 관계에서 진행되며, 기술적으로는 다음과 같은 다층 아키텍처를 따른다.

### 1) 부하 테스트 핵심 아키텍처

```text
+---------------------------------------------------------------------+
|             부하 테스트 인프라 구성 (3-Tier Load Architecture)       |
+---------------------------------------------------------------------+

  [Load Generators]            [Target System Under Test (SUT)]
  +----------------+             +----------------------+
  |  JMeter Master |--Control--->|   L4/L7 LoadBalancer  |
  |  (or k6 cloud) |            |  (Nginx, ALB, F5)    |
  +----------------+             +----------+-----------+
         |                                  |
  +------+-------+                          v
  |  JMeter       |                  +--------------+
  |  Slave ×N     |                  |  WAS Tier    |
  | (Distributed) |                  |  (Tomcat,    |
  +---------------+                  |   Spring,    |
                                     |   Node.js)   |
         ^                           +------+-------+
         |                                  |
   [Monitoring Sidecar]                     v
   +----------------+               +--------------+
   | Prometheus     |               |   DB / Cache |
   | + Grafana      |               |  (Oracle,    |
   | + Scouter/     |               |   MySQL,     |
   |   Pinpoint     |               |   Redis)     |
   +----------------+               +--------------+
            ^                                ^
            +------------ Metrics -----------+
```

### 2) 핵심 수학적 원리: Little's Law와 큐잉 이론

성능 감리에서 절대적으로 활용되는 근본 법칙이다.

- **Little's Law**: `L = λ × W`
  - L: 시스템 내 동시 요청(Concurrent In-flight Requests)
  - λ: 처리율(Throughput, TPS)
  - W: 평균 응답시간(Residence Time)

  **예시**: 평균 응답시간 200ms, TPS 1,000이면 -> 동시 사용자는 200명이다. 이때 응답시간이 2초로 늘어나면 같은 TPS 유지 시 2,000명의 동시성을 견뎌야 하므로 Connection Pool/Thread Pool 사이즈 증설이 필수다.

- **응답시간 분해(Response Time Decomposition)**:
  ```
  Total Response Time = T_wait + T_service + T_queue
                      (큐 대기)  (실제 처리) (스케줄링 대기)
  ```
  T_wait 지배적 -> Connection Pool 증설 / T_service 지배적 -> 코드 최적화 / T_queue 지배적 -> 비동기/배치 처리 도입.

### 3) 병목 진단 5계층 모델 (USE Method 기반)

| 계층 | 진단 대상 | 핵심 메트릭 | 진단 도구 | 임계치/판단 기준 |
|:---|:---|:---|:---|:---|
| **L1 Infra** | CPU, Memory, Disk, NIC | Util%, Steal%, iowait, await | vmstat, mpstat, iostat, sar, dstat | CPU Util > 80% 지속, Steal > 10%, await > 10ms |
| **L2 OS/Network** | Socket, File Descr, Conntrack | TIME_WAIT, CLOSE_WAIT, fd limit | ss, netstat, lsof, /proc/sys/fs | FD 사용률 > 80%, TIME_WAIT 누적 |
| **L3 Middleware** | JVM Heap, GC, Thread Pool | Heap Usage, GC Pause, Active Thread | jstat, jmap, jstack, Scouter, Pinpoint | Full GC > 1회/시간, Heap > 80%, Dead Lock 감지 |
| **L4 Application** | Method Hotspot, SQL Plan, Cache | TPS, P95/P99, Error%, Cache Hit | APM(Dynatrace), OpenTelemetry, Glowroot | P99 > SLA × 2, Error > 0.5%, Cache < 80% |
| **L5 Database** | Lock, Buffer Hit, Slow Query | Lock Wait, Logical Reads, Full Scan | AWR, Statspack, pt-query-digest, V$SQL | Buffer Hit < 95%, Lock Wait > 100ms, Full Scan 탐지 |

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **Load Generator (JMeter/Gatling/k6)** | 가상 사용자(Vuser) 행위 합성 | HTTP/HTTPS/WebSocket/gRPC 프로토콜별 Sampler, Think Time(사용자 행동 간 대기, 통상 1~5초), Pacing(반복 간격), Ramp-up(점진 증가) 설정; 분산 모드에서 Master-Slave(RMI) 또는 Kubernetes 기반 CRD(k6-operator)로 수평 확장 |
| **APM Agent (Scouter/Pinpoint/Dynatrace)** | 코드·메서드 단위 가시화 | Bytecode Instrumentation(ASM/ByteBuddy)으로 트랜잭션 시작~종료 구간 Hook, Active Service Map 자동 구성, SQL 캡처, 외부 호출(Outbound) 별도 Span 분리; 트레이스 컨텍스트 전파는 W3C TraceContext 표준 사용 |
| **Metrics Backend (Prometheus + Grafana)** | 시계열 메트릭 수집·시각화 | Pull 방식 15초 간격 Scrape, TSDB에 1시간 단위 Block 저장, PromQL로 합·비·분위 함수(`quantile`, `histogram_quantile`) 지원, Alertmanager로 임계치 초과 시 Slack/PagerDuty 전파 |
| **Profiler (async-profiler, JFR, perf)** | CPU·메모리·Lock 정밀 분석 | Sampling(주기적 스택 캡처) + Flame Graph 시각화, Hot Method 식별; JFR(Java Flight Recorder)는 1% 미만 오버헤드로 운영 환경 프로파일링 가능; perf는 Linux 커널 이벤트 기반 HW 트레이스 |
| **Database Advisor (AWR, SQLd360, pg_stat_statements)** | SQL 플랜·인덱스 진단 | Oracle AWR은 1시간 단위 스냅샷 비교로 Top SQL·Wait Event 분석; MySQL slow_log + pt-query-digest로 정규화·그룹핑; EXPLAIN ANALYZE로 실제 vs 추정 Row 수 차이로 통계 정보 노후도 판별 |

### 4) 분산 트레이싱과 인과관계 추적

MSA 환경에서 한 HTTP 요청은 10~30개의 Span으로 구성되며, 각 Span은 `trace_id`(전체 흐름) -> `span_id`(개별 구간) -> `parent_span_id`(상위 호출)로 트리 구조를 이룬다. **Critical Path Analysis**로 응답시간의 병렬/직렬 흐름을 시각화하여, "어떤 서비스가 80% 시간을 잡아먹는가"를 즉시 판별한다. 한국형 APM인 **Scouter**는 자체 Agent + Collector + Web Console 구조로 Java/Node/Python을 지원하며, **Pinpoint**는 Naver가 개발해 HBase 기반 대용량 트레이스 저장에 강점을 가진다.

- **📢 섹션 요약 비유**: 부하 테스트는 **고속도로에 1만 대의 자율주행 RC카를 한꺼번에 몰아넣어 정체를 유발**하는 실험이고, 병목 진단은 그 정체가 톨게이트 부족(L4)인지, 톨게이트는 충분하나 결제 시스템(JVM Heap GC)이 느린 건지, 고속도로 노선(DB Full Scan) 자체가 잘못된 건지를 **블랙박스 GPS 로그**로 분간해내는 수사다.

---

## Ⅲ. 비교 및 연결

### 1) 부하 테스트 유형 비교

| 구분 | **Load Test (부하)** | **Stress Test (스트레스)** | **Spike Test (스파이크)** | **Soak Test (장시간/내구)** | **Capacity Test (용량)** |
|:---|:---|:---|:---|:---|:---|
| **목적** | SLA 응답시간·TPS 검증 | 한계점·회복탄력성(Resilience) 확인 | 급격한 트래픽 폭증 대응 | 메모리 누수·리소스 결핍 탐지 | 최대 동시사용자·처리량 측정 |
| **부하 곡선** | 정상 운영 × 1.5~2배 유지 | 정상 × 2~5배 점진 증가 | 0->최대->0 즉시 변동 | 정상 × 1.2~1.5배 8~24시간 지속 | 동시성 100->1000+ 점진 |
| **핵심 지표** | P95 응답시간, Error% | 임계 TPS, 시스템 붕괴 시점 | 큐 적체(Q Build-up) | Heap·FD·Conn 누수 여부 | Knee Point(처리량 정체 지점) |
| **실패 시 액션** | 코드/쿼리 튜닝 | Auto-scaling·Circuit Breaker 도입 | Rate Limit·Cache TTL 조정 | Heap Dump 분석·GC 튜닝 | 증설 vs 최적화 ROI 산정 |
| **도구 예** | JMeter, Gatling | JMeter + Chaos Monkey | k6 Stress, Locust | JMeter + Scouter 24h 관찰 | nGrinder, Cloud-based Loader |

### 2) 성능 진단 방법론
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 596 / 600

<- **이전**: [595. 보안 감리 제로 트러스트 적합성 평가](/studynote/11_design_supervision/06_exam_summary/595_security_audit_zero_trust_fitness/)
**다음**: [597. UX 감리 사용성 접근성 인터페이스 평가](/studynote/11_design_supervision/06_exam_summary/597_ux_audit_usability_accessibility_interface/) ->

---
