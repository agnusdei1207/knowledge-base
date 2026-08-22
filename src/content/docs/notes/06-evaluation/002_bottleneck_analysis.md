---
sidebar:
  order: 2
  label: "002. 병목 분석 (Bottleneck Analysis)"
  badge:
    text: "미출 · 50%"
    variant: note
title: "시스템 성능 제약 요인 식별 및 최적화 : 병목 분석 (USE 및 RED 방법론)"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-evaluation"
weight: 2
extra:
  question_no: "002"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "성능 튜닝 및 진단의 핵심 방법론, 병목(Bottleneck) 및 임계 경로(Critical Path) 식별, Brendan Gregg의 USE 방법론(Utilization, Saturation, Errors), Tom Wilkie의 RED 방법론(Rate, Errors, Duration), 대기열 이론(M/M/1 Queue) 기반 포화점 분석, 병목 이동(Bottleneck Shift) 검증"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **병목 분석(Bottleneck Analysis / Performance Diagnostics)**: 소프트웨어 시스템 및 IT 인프라 전 구간에서 트래픽 증가 시 처리량(Throughput)을 제약하고 응답 지연(Latency)을 급증시키는 가장 취약한 단일 제약 자원(Resource) 또는 소프트웨어 임계 경로(Critical Path)를 정량적으로 식별하고 근본 원인을 규명하는 성능 엔지니어링 기법.
- **자원 포화에 따른 대기열 폭증 및 병목 이동 결함(Queue Saturation & Bottleneck Shift Defect)**: 특정 자원(예: DB Connection Pool)의 용량이 한계에 도달했을 때 요청이 대기열(Queue)에 적체되어 응답시간이 비선형적으로 폭증하는 현상과, 해당 병목을 튜닝한 직후 차순위 자원(예: CPU 또는 Disk I/O)으로 병목 지점이 연쇄 전이되는 현상을 사전에 예측하지 못하는 구조적 결함.

</details>

- 정의/개념: 시스템 전 구간의 성능 제약 요인을 체계적으로 해소하기 위해 **기준 부하 주입 $\rightarrow$ 인프라 계층 USE(가동률/포화도/에러) 진단 $\rightarrow$ 서비스 계층 RED(요청률/에러율/지연) 분석 $\rightarrow$ APM 분산 추적(Distributed Tracing) 및 플레임 그래프(Flame Graph) 핫스폿 격리 $\rightarrow$ 단일 요인 튜닝 및 병목 이동(Bottleneck Shift) 재검증** 을 집행하는 **계층적 성능 진단 프레임워크**
- 배경/필요성: 마이크로서비스 및 멀티 클라우드 환경의 복잡성 증가로 인해 단순 하드웨어 증설(Scale-up)만으로는 소프트웨어 락(Lock) 경합이나 비효율적 쿼리로 인한 성능 저하를 해결할 수 없으므로, 자원과 애플리케이션 코드를 아우르는 구조적 진단 체계 필요

#### 한줄 요약
- 병목 분석은 USE와 RED 방법론 및 분산 추적을 융합하여 자원과 코드 경로의 제약 요인을 식별·제거한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **병목 진단 2대 핵심 방법론**:
  - **USE 방법론 (Utilization, Saturation, Errors / Brendan Gregg)**: 모든 하드웨어 자원(CPU, 메모리, 디스크, 네트워크)의 사용률, 큐 적체 포화도, 에러 발생 여부를 점검하는 인프라 중심 분석.
  - **RED 방법론 (Rate, Errors, Duration / Tom Wilkie)**: 모든 마이크로서비스 엔드포인트의 초당 요청률(Rate), 실패 요청 비율(Errors), 처리 소요 시간(Duration)을 측정하는 서비스 중심 분석.

</details>

- **자원과 서비스의 교차 진단 (USE + RED 융합)**: 인프라 하드웨어의 자원 고갈(USE)과 애플리케이션 API의 호출 지연(RED)을 시계열 상에서 상호 대조(Correlation)
- **임계 경로(Critical Path) 핫스폿 격리**: 트랜잭션의 총 소요 시간 중 가장 많은 비중을 차지하는 함수, 락(Lock) 대기, 슬로우 SQL 구간을 1ms 단위로 정밀 프로파일링
- **반복적 단일 가설 검증 (Hypothesis Testing)**: 여러 설정을 동시에 바꾸지 않고 유력 병목 후보 1개만을 수정한 뒤 동일 부하 환경에서 성능 개선율과 병목 이동 여부를 재검증

#### 한줄 요약
- USE/RED 융합 분석, 임계 경로 핫스폿 격리, 가설 기반 단일 요인 튜닝 및 병목 이동 검증을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **병목 분석 4대 아키텍처 계층**:
  1. **Workload & Baseline Layer**: 재현 가능한 부하 프로파일 및 성능 기준선(Baseline) 정의.
  2. **Infrastructure Telemetry (USE Engine)**: OS 커널 메트릭, CPU 런큐(Run Queue), 디스크 I/O 큐 수집.
  3. **Application Telemetry (RED Engine)**: API 게이트웨이 및 서비스 메시의 트래픽, 에러, 지연시간 수집.
  4. **Code & Profiling Layer**: APM 분산 추적(Trace), 스레드 덤프, JVM 플레임 그래프(Flame Graph).

</details>

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 1. 통제된 부하 주입 및 베이스라인 (Load Injection & Baseline) ]       │
│  └─ [ 부하 도구 (JMeter / k6) ] ➔ 단계적 부하 주입(Ramp-up)으로 한계점 유도 │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (다계층 텔레메트리 동시 수집)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 2. 계층별 병목 관측 엔진 (Multilayer Observation Engine) ]             │
├───────────────────────────────────┬─────────────────────────────────────┤
│ [ 인프라 계층: USE 관측 (OS/HW) ] │ [ 서비스 계층: RED 관측 (App/API) ] │
│ ├─ Utilization: CPU 95%, Disk 80% │ ├─ Rate: 초당 4,000 RPS 인입        │
│ ├─ Saturation: CPU 런큐 12, Disk큐│ ├─ Errors: HTTP 504 Gateway Timeout │
│ └─ Errors: 네트워크 패킷 Drop 발생│ └─ Duration: p99 지연 3.2초 급증    │
└───────────────────────────────────┴─────────────────────────────────────┘
                                     │ (상관관계 분석 및 임계 경로 추적)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 3. 코드 레벨 정밀 프로파일링 계층 (Deep Code & Query Profiling) ]     │
│  ├─ [ APM 분산 추적 ] ➔ Service A(20ms) ➔ Service B(3,100ms: Bottleneck)│
│  └─ [ 플레임 그래프 ] ➔ DB Lock 경합(synchronized) 및 비효율적 Full Scan│
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (튜닝 및 병목 이동 검증)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 4. 가설 검증 및 최적화 루프 (Hypothesis Testing & Bottleneck Shift) ] │
│  ├─ DB 인덱스 생성 및 Connection Pool 2배 확장 적용                     │
│  └─ [ 동일 부하 재실행 ➔ 지연 120ms로 단축 확인 및 차순위 네트워크 검증]│
└─────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 부하 주입 상태에서 USE와 RED 지표를 동시 수집하고 코드 프로파일링을 통해 병목을 규명한 후 튜닝 효과를 검증하는 구조

| 분석 영역 | 핵심 진단 지표 | 주요 점검 도구 및 메커니즘 | 대표적 병목 원인 |
|:---|:---|:---|:---|
| **CPU 인프라** | **Utilization, Run Queue Length** | `vmstat`, `top`, `perf`, `mpstat` | 연산 집약 루프, 잦은 Context Switching |
| **메모리 인프라** | **Paging, Major Page Fault, OOM** | `free`, `sar -B`, JVM Heap Dump | 메모리 누수, 과도한 객체 생성, GC Pause |
| **디스크 I/O** | **IOPS, Disk Queue, %util, await** | `iostat -xz 1`, `iotop`, `blktrace` | 동기 디스크 쓰기, DB Full Table Scan |
| **네트워크 I/O** | **Drop/Error Counter, TCP Backlog** | `netstat -s`, `ss -s`, `ethtool` | 대역폭 포화, 소켓 버퍼 고갈, 패킷 재전송 |
| **애플리케이션** | **RED (Rate, Errors, Duration)** | Prometheus, OpenTelemetry, Envoy | 비효율적 동기 외부 API 호출, Thread 고갈 |
| **데이터베이스** | **Slow Query, Lock Wait, Pool Active**| Slow Query Log, Thread Pool Dump | 미인덱싱 쿼리, Row Lock 경합, Pool 고갈 |

#### 한줄 요약
- CPU(런큐), 메모리(GC), 디스크(await), 네트워크(Drop), 앱(RED), DB(Lock) 계층별 관측으로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **병목 분석 및 제거 5단계 반복 사이클**:
  1. 부하 시험 환경 및 성능 기준선(Baseline) 확립
  2. USE 방법론을 통한 인프라 자원 포화도(Saturation) 스캔
  3. RED 방법론 및 APM 분산 추적을 통한 서비스 지연 구간 국소화
  4. 단일 병목 원인 가설 수립 및 코드/인프라 튜닝 단행
  5. 동일 부하 환경에서 재시험 수행 및 병목 이동(Bottleneck Shift) 검증

</details>

```text
1. [기준선 수립 및 부하 주입]
    ├─ 테스트 환경 고정: 가상 사용자 5,000명 주입
    └─ [베이스라인 측정: 1,200 TPS에서 처리량 정체 및 p99 응답시간 4.5초 기록]
            │
            ▼
2. [1차 인프라 USE 진단]
    ├─ Web/WAS 서버: CPU 40%, Memory 50% (정상 여유 확인)
    ├─ DB 서버: CPU 98% (포화), 런큐(Run Queue) 16 도달 (CPU 자원 병목 의심)
    └─ [가설: DB 서버의 CPU 포화가 전체 시스템의 처리량을 제한함]
            │
            ▼
3. [2차 서비스 RED 및 코드 프로파일링]
    ├─ APM 분산 추적으로 결제 API 트레이스 분석 ➔ 총 4.5초 중 DB 쿼리 소요시간 4.2초
    ├─ DB Slow Query Log 분석 ➔ `SELECT * FROM orders WHERE user_id = ?` (1회 실행 시 3초)
    └─ [실행 계획(Explain Plan) 확인 ➔ 1,000만 건 테이블의 Full Table Scan 확인]
            │
            ▼
4. [단일 요인 튜닝 (Single-factor Optimization)]
    ├─ `orders` 테이블의 `user_id` 컬럼에 B-Tree 인덱스 생성
    └─ (동시에 다른 설정값을 변경하지 않고 인덱스만 단일 적용하여 인과관계 고립)
            │
            ▼
5. [재시험 및 병목 이동(Bottleneck Shift) 확인]
    ├─ 동일 5,000명 부하 주입 ➔ DB CPU 사용률 98% ➔ 15%로 급감, 처리량 3,500 TPS로 상승
    ├─ [차순위 병목 관측] 3,500 TPS 도달 시 WAS의 Network Socket 백로그 큐가 포화됨을 신규 식별
    └─ [다음 튜닝 사이클(Network Buffer 튜닝)로 회귀하여 반복 최적화]
```

**동작 원리**

1. **대기열 이론(Queueing Theory) 적용**: 대기열 이용률($\rho$)이 1.0에 근접할수록 대기시간($W_q = \frac{\rho}{\mu(1-\rho)}$)이 무한대로 발산하므로, 포화 자원을 우선 제거
2. **인과관계 고립**: 여러 파라미터를 동시 수정할 경우 개선의 주원인을 파악할 수 없으므로 철저한 1변수 변경(One-variable-at-a-time) 원칙 준수
3. **가장 굵은 파이프 원칙**: 시스템의 최대 처리량은 가장 좁은 병목 구간의 용량에 의해 결정되므로, 비병목 구간 최적화는 전체 성능에 기여하지 못함(아달의 법칙)
4. **시계열 상관 분석**: 지연시간 스파이크 발생 시점과 정확히 일치하는 자원 사용률 피크를 찾아내어 우발적 노이즈와 진짜 병목 분리
5. **지속적 병목 이동 대응**: 1차 병목 해소 시 처리량이 증가하면서 숨어 있던 2차, 3차 병목이 수면 위로 드러나는 병목 이동을 필수 점검

#### 한줄 요약
- 베이스라인 측정, USE 인프라 스캔, RED/APM 핫스폿 분석, 단일 요인 튜닝, 재시험 및 병목 이동 검증 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **성능 분석 3대 진단 프레임워크 비교**:
  - USE 방법론: 자원 중심 (Utilization, Saturation, Errors).
  - RED 방법론: 서비스 중심 (Rate, Errors, Duration).
  - Google SRE 4대 황금 신호: 사용자 및 시스템 통합 (Latency, Traffic, Errors, Saturation).

</details>

| 비교 항목 | USE 방법론 (Brendan Gregg) | RED 방법론 (Tom Wilkie) | 4대 황금 신호 (Google SRE) |
|:---|:---|:---|:---|
| **진단 대상** | **하드웨어 및 OS 물리 자원 (CPU, Disk, Net)**| **마이크로서비스 API 및 애플리케이션**| **엔드투엔드 분산 서비스 아키텍처** |
| **핵심 지표** | **가동률(U), 포화도(S), 에러(E)** | **요청률(R), 에러율(E), 지연시간(D)** | **지연, 트래픽, 에러, 포화도** |
| **분석 관점** | **자원 공급자 관점 (Hardware-Centric)** | **서비스 소비자 관점 (Service-Centric)**| **시스템-사용자 통합 관점 (Unified)** |
| **주요 활용** | 서버 용량 산정, 인프라 병목 색출 | MSA 호출 지연 분석, 마이크로서비스 장애 | SLA/SLO 모니터링, 알람(Alerting) 기준 |
| **한계점** | 소프트웨어 로직/쿼리 병목 추적 불가 | 하드웨어 물리 고갈의 근본 원인 미제공 | 심층 커널 레벨 프로파일링 데이터 부족 |

#### 한줄 요약
- USE는 인프라 자원, RED는 서비스 API 경로, 4대 황금 신호는 전사 서비스 수준 모니터링에 최적화된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **병목 분석 시 발생하는 3대 현업 문제점과 엔지니어링 대책**:

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 1분 평균 CPU 사용률이 50%로 정상이어서 안심했으나 **수 밀리초(ms) 단위의 마이크로 버스트(Micro-burst)로 인해 순간 런큐 적체 및 패킷 드롭 발생** | **초 단위 이하 고해상도 메트릭 수집 도구(eBPF 기반 BCC/bpftrace)를 적용하여 10ms 단위 런큐 지연 모니터링** | 순간 포화(Micro-saturation) 완벽 탐지 및 병목 규명 |
| DB 인덱스를 추가하여 쿼리 병목을 해소했으나 **증가한 트래픽으로 인해 WAS 스레드 풀 및 네트워크 인터페이스가 새로운 병목으로 부상** | **1차 튜닝 완료 후 동일 부하 조건에서 즉시 재시험을 수행하여 단계별 병목 이동(Bottleneck Shift) 추적 및 시스템 균형 최적화** | 연쇄 병목 조기 식별 및 시스템 처리 한계치 300% 확장 |
| 여러 개발자가 성능 개선을 위해 WAS JVM 옵션, DB 파라미터, 소스코드를 동시에 변경하여 **어떤 변경 사항이 성능 향상에 기여했는지 인과관계 규명 불가** | **'가설 수립 $\rightarrow$ 1개 단일 요인 변경(Single-variable Change) $\rightarrow$ 부하 재검증'의 엄격한 과학적 엔지니어링 프로세스 강제** | 성능 개선 인과관계 100% 입증 및 튜닝 부작용 차단 |

#### 한줄 요약
- eBPF로 순간 포화를 잡고, 재시험으로 병목 이동을 추적하며, 1변수 변경으로 인과관계를 입증한다.

## Ⅶ. 결론

- 시스템의 잠재된 처리 역량을 극대화하고 자원 낭비를 방지하는 핵심 엔지니어링 절차인 **병목 분석 체계**는 단순한 감(Intuition)에 의한 튜닝을 배제하고 데이터에 기반한 체계적 최적화를 실현하는 필수 방법론이며, 실무 구현 시 **인프라 자원 중심의 USE 방법론과 서비스 중심의 RED 방법론의 융합**, **APM 분산 추적을 통한 임계 경로 코드 핫스폿 격리**, **단일 요인 변경 기반의 엄격한 가설 검증**, **튜닝 후 병목 이동(Bottleneck Shift)에 대한 반복적 재시험**을 완성하여 최고 수준의 시스템 확장성과 고효율 처리 성능을 완성

#### 한줄 요약
- USE와 RED의 융합 진단 및 가설 기반 튜닝을 통해 무결점 병목 분석 최적화를 완성한다.
