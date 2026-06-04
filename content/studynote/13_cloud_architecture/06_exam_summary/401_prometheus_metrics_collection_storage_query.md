---
title: "401. 프로메테우스 메트릭 수집 저장 쿼리 (Prometheus Metrics Collection Storage Query)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Prometheus는 **Pull 기반 HTTP 스크래핑(/metrics 엔드포인트)**으로 **레이블(Label)이 부착된 시계열(Time-series) 메트릭**을 수집하고, **LSM-Tree 기반의 사내 TSDB(Time-Series Database)**에 **1차 Head Block(메모리) -> WAL(쓰기 로그) -> 2차 Persistent Block(2시간 단위 디스크 청크)**의 3단계 구조로 저장하며, **시계열·벡터·순간·범위 연산자**를 결합한 함수형 PromQL(Prometheus Query Language)로 다차원 집계를 수행한다.
> 2. **가치**: **단일 인스턴스 기준 초당 100만 샘플(100만 series) 수집·압축·쿼리**가 가능하며, **Cortex·Thanos·Mimir·VictoriaMetrics**와 결합 시 **수 페타바이트급 롱텀 스토리지(Retention 1년+)**와 **무제한 수평 확장(샤딩·복제)**을 실현해, 쿠버네티스·MSA 환경에서 사실상 **De-facto 표준 옵저버빌리티 패브릭**으로 자리매김했다.
> 3. **판단 포인트**: 핵심 트레이드오프는 **(a) Pull vs Push**, **(b) 로컬 vs 원격 스토리지(Thanos/Mimir)**, **(c) 고카디널리티(High-Cardinality) 허용 범위**, **(d) Pushgateway 사용 범위(배치/단기 작업 전용)**, **(e) Recording Rule/Alert Rule 오버헤드**이며, 기술사는 **샘플링·릴레이션 정책(Retention: ST 24h, LT 1y)·샤딩 전략·Alertmanager 라우팅·OpenTelemetry 마이그레이션**을 통합 설계할 수 있어야 한다.

---

## Ⅰ. 개요 및 필요성

MSA(Microservices Architecture)와 쿠버네티스(Kubernetes)가 보편화되면서, **수십~수만 개 컨테이너/POD**에서 발생하는 **"4가지 골든 시그널(Latency, Traffic, Errors, Saturation)"**과 USE 메서드(Utilization, Saturation, Errors) 기반의 지표를 단일 시스템에서 일관되게 수집·저장·조회할 수 있어야 한다. 기존 **Nagios/Zabbix 같은 Push·에이전트 기반 모니터링**은 메트릭이 1차원(호스트 단위)이고 **저장·쿼리·시각화가 분리되지 못해** MSA 환경에서 한계가 드러났다. 또한 **StatsD/Graphite** 같은 시스템은 카디널리티·라벨 기반 쿼리·알람 라우팅이 빈약했고, **InfluxDB**는 TICK 스택으로 통합되었지만 HTTP Pull 생태계·PromQL 수준의 표현력은 부족했다.

Prometheus는 **2012년 SoundCloud에서 시작**(2016년 CNCF 인큐베이팅, **2018년 Graduated**)되어, CNCF 2번째 Graduated 프로젝트가 되었고, 현재는 **쿠버네티스·Istio·Envoy·etcd·CoreDNS·Kubelet** 등 클라우드 네이티브 생태계의 사실상 **메트릭 표준**으로 자리 잡았다. **"Prometheus + Alertmanager + Grafana"**(PAG) 스택은 컨테이너 옵저버빌리티의 삼각편대를 형성한다.

```text
  +------------------------------------------------------------------+
  |        기존(Push/Agent 기반)        vs       Prometheus(Pull)    |
  +------------------------------------------------------------------+
  |                                                                  |
  |  Zabbix/Nagios         Prometheus                               |
  |  +----------+          +--------------+                          |
  |  |  Agent   |  push ->  |              |  <--- /metrics (Pull)    |
  |  | (각 호스트)|         |  Prometheus  |  <--- Service Discovery  |
  |  |  agent->  |          |   Server     |                          |
  |  | server   |          |              |                          |
  |  +----------+          +------+-------+                          |
  |       1차원 메트릭              |                                  |
  |  (호스트 단위 메트릭)            v                                  |
  |                          TSDB (2h block + WAL)                    |
  |  쿼리:Zabbix Expression        PromQL (다차원·시계열·벡터)        |
  |                                                                  |
  |  ❌ MSA 환경 한계           ✅ 컨테이너·MSA·쿠버네티스 최적화     |
  |  ❌ 시계열 압축 약함         ✅ 1.3 byte/sample 압축              |
  |  ❌ 알람 라우팅 빈약         ✅ Alertmanager(계단식·억제·그룹화)  |
  +------------------------------------------------------------------+
```

**왜 Pull 모델인가?** ① **서비스 디스커버리(SD)와 결합**해 *스케줄링 측면에서 마스터(서버)가 SLA 보장**, ② **단일 인스턴스에서 자기 메트릭(self-scraping)** 수집 가능, ③ **네트워크 방화벽 정책에 친화적**(아웃바운드만 허용), ④ **중복·중복 수집 방지**(단일 scrape_interval 보장). 다만 배치·단기 작업(Job)처럼 노출 엔드포인트가 일시적인 경우 **Pushgateway**(임시 버퍼) 보완이 필요하다.

- **📢 섹션 요약 비유**: 🏥 **응급실의 중환자 모니터링**과 같다. 환자(POD)가 ICU에 누워 있으면, 간호사(Prometheus Server)가 **주기적으로 병문안(스크레이핑)** 와서 심장박수·혈압(메트릭)을 메모장에 적고, 차트(시계열 DB)에 누적한다. 응급 환자(긴 수명 메트릭)는 차트에 영구 보존, 외래 환자(단기 메트릭)는 Pushgateway라는 **임시 대기실**에서 잠깐 머문 뒤 병원에 들어온다. 의사가 차트를 보면 즉시 상태를 판단(PromQL)한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Prometheus 아키텍처는 **수집(Scraping) -> 저장(TSDB) -> 쿼리(PromQL) -> 알람(Alerting)** 의 4단계로 구성된다.

```text
                       +----------------------------------------+
                       |         Prometheus Server (단일 binary)  |
                       |  +-------------+   +----------------+  |
                       |  | Retrieval   |--->|  TSDB          |  |
                       |  | (Scrape)    |   | +------------+ |  |
                       |  |  - SD       |   | | Head Block | |  |
                       |  |  - scrape   |   | |  (mem+mmap)| |  |
                       |  |  - relabel  |   | +------------+ |  |
                       |  +------+------+   | | WAL(32MB)  | |  |
                       |         |          | +------------+ |  |
                       |         |          | |Persistent  | |  |
                       |  +------v------+   | | Block 2h   | |  |
                       |  | PromQL      |--->| | (leveldb)  | |  |
                       |  | Engine      |   | +------------+ |  |
                       |  +------+------+   +----------------+  |
                       |         |                               |
                       |  +------v------+                        |
                       |  | Rule Manager|---> Alertmanager        |
                       |  | (record/    |   (라우팅·억제·그룹화)  |
                       |  |  alert)     |                        |
                       |  +-------------+                        |
                       +----------------------------------------+
                                    ^          |           ^
                                    | /metrics | /reload   |
                                    | (Pull)   |           |
        +---------------------------+---+      |   +-------+--------------+
        |                               |      |   |                      |
   +----v-----+  +--------+  +---------v+ +----v---v+  +--------------+  |
   | node_expor|  |kubelet |  |App(JVM/  | |Pushgatew|  |Remote Write  |  |
   | ter :9100 |  | :10250 |  |Python/Go | |ay :9091 |  | -> Thanos/    |  |
   | (Host)    |  |(cAdv)  |  | /metrics)| |(배치잡) |  |   Cortex/    |  |
   +-----------+  +--------+  +----------+ +---------+  |   Mimir      |  |
        ^              ^             ^                  +--------------+  |
        |              |             |                                    |
   +----+--------------+-------------+-------------+                       |
   |  Service Discovery (SD):                      |                       |
   |   - kubernetes_sd_config (pod/svc/endpoints)  |                       |
   |   - file_sd_config (Consul/Nomad)             |                       |
   |   - dns_sd_config, ec2_sd_config, gce_sd_...  |                       |
   +-----------------------------------------------+                       |
                                                                          |
   <---------------- Grafana (시각화) ---------------> <----- Alertmanager ---+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Retrieval (Scraper)** | 메트릭 수집 엔진 | scrape_interval(기본 15s), scrape_timeout(10s) 주기로 **SD(Service Discovery)** 를 통해 타깃을 동적 해소, **`/metrics` HTTP GET**(Accept: text/plain, application/openmetrics-text) 요청, **Exposition Format** 파싱(0.0.4 또는 OpenMetrics 1.0.0) |
| **Relabeling / Metric Relabel** | 라벨 재작성 | `keep`/`drop`/`labelmap`/`labeldrop`/`regex`/`replacement` 액션으로 카디널리티·노이즈 제어. `action: labelmap`, `regex: __meta_kubernetes_pod_label_(.+)`로 K8s 라벨을 주입 |
| **TSDB (Storage Engine)** | 시계열 전용 DB | Go로 작성된 자체 엔진. 데이터는 **시계열 ID(해시)** + **Chunk(Value, Timestamp)** 구조. **1) Appender로 Head Block(in-memory + mmap)** 에 append -> **2) WAL(Write-Ahead Log)에 32MB 단위 segment로 fsync** -> **3) 2시간 경과 시 Persistent Block 디스크 청크로 flush + compaction** |
| **PromQL Engine** | 쿼리·집계 엔진 | 표현식 -> AST(Abstract Syntax Tree) -> **Selector(Vector Selector, Range Vector) -> 함수/연산자 -> Output(Vector/Instant Vector/Scalar)**. 시그너처: `<metric>{<label>}` `[<duration>]` `(offset <duration>)` |
| **Rule Manager** | 사전 계산·알람 평가 | **Recording Rule**(자주 쓰는 복잡 쿼리를 사전 계산해 새 시계열 생성) + **Alerting Rule**(임계치 기반 평가 -> `for` 지속시간 확인 -> Alertmanager 전송). `evaluation_interval`(기본 1m) |
| **Alertmanager** | 알람 라우팅·억제 | Prometheus와 분리(서로 다른 도메인) 운영. **Grouping**(라벨 기반), **Inhibition**(상위 알람 시 하위 억제), **Silences**(일시적 음소거), **Routing Tree**(match/re/matchers) -> Receiver(PagerDuty/Slack/Webhook) |
| **Service Discovery** | 동적 타깃 해소 | Kubernetes(7가지 역할: node/pod/service/endpoints/endpointslice/ingress/pod), Consul, EC2, GCE, file, dns 등 30+가지 SD 어댑터. **Relabel 단계에서 `__address__`·`__meta_*` 메타라벨 활용** |
| **Pushgateway** | Push 보조 게이트웨이 | **단기·배치 작업(Job)** 등 자기 노출 엔드포인트가 없는 경우 push. **장기 배치에 사용 시 메트릭 영구화·중복 위험**(anti-pattern). 기본 보존: 1시간 |

### 핵심 메커니즘: TSDB 저장 구조 (LSM-Tree 변형)

Prometheus 2.x의 TSDB는 **로그 구조 병합 트리(LSM-Tree)** 의 시계열 특화 구현이다.

1. **메모리 내 Head Block**: `[]Chunk`로 구성, 각 Chunk는 **Goroutine-safe Appender API**로 **시간순 정렬된 (timestamp, value) 쌍**을 누적. Chunk 크기는 **120 sample**(기본). Head Block의 in-memory 부분은 **mmap**으로 디스크에 매핑되어 재시작 시 복원.
2. **WAL (Write-Ahead Log)**: 모든 append는 **WAL segment**에 기록(32MB 초과 시 rotation). 체크포인트(Head Block 디스크 직렬화) 발생 시 WAL은 truncate. **내구성·재해복구** 보장(최대 2시간 데이터 손실).
3. **Persistent Block (2시간 청크)**: 디렉터리 구조: `chunks/`(데이터), `index/`(메타), `meta.json`, `tombstones/`. 압축 알고리즘은 **Double-Delta + Gorilla XOR**(Facebook 시계열 압축 기법), **샘플당 평균 1.3 byte** 압축률.
4. **Compaction**: 2시간 블록들이 **머지(merge)**되어 더 큰 블록(기본 31개 -> ~3일)으로 통합. 머지 시 `tombstones`로 삭제된 시리즈 처리.

**시계열 ID 해시**: `metric_name + labels(sorted)` -> **FNV64 해시(64-bit)** -> 시계열 식별자. 동일 메트릭 + 동일 라벨 조합이 유일한 시계열이 되므로, **라벨 카디널리티 폭증은 곧 메모리·디스크 폭발**로 이어진다(예: `user_id` 라벨은 절대 금지).

### PromQL 핵심 함수 (시험 빈출)

| 카테고리 | 함수 | 시그너처 / 예시 | 설명 |
| :--- | :--- | :--- | :--- |
| **즉시 벡터(Instant Vector)** | `rate()`, `irate()` | `rate(http_requests_total[5m])` | `rate`는 [range] 구간 평균 **초당 증가율**, `irate`는 마지막 2개 데이터 포인트 기반 **순간 증가율** (노이즈 큼) |
| **누적** | `increase()` | `increase(http_requests_total[1h])` | range 구간의 **총 증가량** (rate × range) |
| **히스토그램** | `histogram_quantile()` | `histogram_quantile(0.95, sum by(le)(rate(http_request_duration_seconds_bucket[5m])))` | **버킷 누적합**에서 분위수 근사 계산 (선형 보간) |
| **예측** | `predict_linear()`, `deriv()` | `predict_linear(node_filesystem_free_bytes{mountpoint="/"}[6h], 4*3600) < 0` | **선형 회귀**로 t초 후 값 예측 (디스크 풀 알람) |
| **집계** | `sum by()`, `topk()`, `quantile()` | `topk(3, sum by(pod)(rate(http_requests_total[5m])))` | 시계열·라벨 단위 집계, **벡터 매칭**(on/ignoring) 필수 |
| **결합** | `*`, `/`, `and`, `or`, `unless` | `up == 0 and on(instance) changes(node_uname_info[5m]) == 0` | **벡터 간 라벨 매칭** 후 산술·집합 연산 |

- **📢 섹션 요약 비유**: 📚 **도서
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 401 / 800

<- **이전**: [400. 클라우드 스트리밍 Kinesis EventHub](/studynote/13_cloud_architecture/06_exam_summary/400_cloud_streaming_kinesis_eventhub/)
**다음**: [402. 그라파나 대시보드 시각화 알림](/studynote/13_cloud_architecture/06_exam_summary/402_grafana_dashboard_visualization_alerting/) ->

---
