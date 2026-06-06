---
title: "085. Watermark"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
---

## 핵심 인사이트 (3줄 요약)

- **본질**: 워터마크(Watermark)는 스트리밍 시스템에서 "이벤트 시간 T의 워터마크 = T인 이벤트는 이제 모두 도착했다고 가정한다"는 의미의 [진행](/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 표시기([Progress](/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) Indicator)로, `Watermark = max_event_time - allowed_lateness`로 계산되며 이 값을 초과하면 윈도우가 닫힌다.
- **가치**: 워터마크 없이는 스트리밍 집계가 "언제 결과를 확정해야 하는지" 알 수 없어 윈도우가 영원히 닫히지 않거나 임의로 닫혀 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 이벤트가 누락된다. 워터마크는 <strong><a href="/studynote/16_bigdata/01_intro/002_bigdata_5v/">정확성</a>(Accuracy)과 <a href="/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a>(<a href="/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/">Latency</a>)</strong> 사이의 균형점을 명시적으로 정의한다.
- **판단 포인트**: 워터마크 허용 범위가 클수록 더 많은 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 이벤트를 수용하지만 윈도우 결과가 늦게 나오고, 작을수록 빠른 결과를 내지만 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 이벤트를 놓친다. 실무에서는 P99 이벤트 [지연 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) 측정 후 워터마크를 그보다 약간 크게 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)한다.

---

## Ⅰ. 개요 및 필요성

### 1. 이벤트 시간 집계의 근본 문제

이벤트 시간 기반 5분 윈도우를 계산할 때, 스트리밍 시스템은 "[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/):00~[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/):05 윈도우의 모든 이벤트가 도착했다"고 언제 확신할 수 있는가?

- 이 윈도우의 이벤트가 무한히 늦게 올 수 있다면 -> 윈도우를 영원히 닫을 수 없음
- 무조건 현재 시간 기준으로 닫으면 -> [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 이벤트 누락

워터마크는 이 딜레마를 "허용 [지연 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)"을 명시적으로 선언함으로써 해결한다.

### 2. 워터마크의 정의

```
Watermark(t) = "이벤트 시간 t 이전에 발생한 모든 이벤트는 도착했다"는 주장

계산식:
  Watermark = max(observed_event_time) - max_allowed_lateness

예시:
  현재까지 본 최대 이벤트 시간: 10:05:30
  허용 지연 시간: 30초
  워터마크 = 10:05:00
  -> "10:05:00 이전 이벤트는 모두 도착했다고 가정"
  -> 10:00~10:05 윈도우 닫을 수 있음!
```

**📢 섹션 요약 비유**
> 워터마크는 "[버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 출발 시간"이다. "5분 지각까지 기다린다(워터마크 = 5분)"고 정하면, 정시 + 5분이 지나면 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)는 출발(윈도우 닫힘)한다. 더 늦게 온 사람([지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 이벤트)은 다음 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)를 타야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 워터마크 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 및 전파

```
이벤트 스트림:
----------------------------------------------
  [이벤트 t=10:00] [이벤트 t=10:03] [이벤트 t=10:02] [이벤트 t=10:06]
                                      ^ 지연 이벤트
WM 생성 (allowed_lateness = 30s):
  After t=10:00: WM = 09:59:30
  After t=10:03: WM = 10:02:30
  After t=10:02: WM = 10:02:30 (최대값 유지, 감소 안 함!)
  After t=10:06: WM = 10:05:30

윈도우 10:00~10:05 닫히는 시점:
  WM >= 10:05:00 일 때 -> WM = 10:05:30 도달 시 닫힘
  10:02 이벤트는 WM 10:02:30 때 이미 도착 -> 윈도우에 포함됨 ✓
----------------------------------------------
```

### 2. Flink에서 워터마크 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 방법

```java
// 방법 1: 고정 지연 워터마크 (가장 일반적)
WatermarkStrategy<Event> strategy = WatermarkStrategy
    .<Event>forBoundedOutOfOrderness(Duration.ofSeconds(30))  // 최대 30초 지연 허용
    .withTimestampAssigner((event, ts) -> event.getTimestamp());

// 방법 2: 단조 증가 (지연 없는 정렬된 스트림)
WatermarkStrategy<Event> monotonic = WatermarkStrategy
    .<Event>forMonotonousTimestamps()
    .withTimestampAssigner((event, ts) -> event.getTimestamp());

// 방법 3: 커스텀 워터마크 생성기
WatermarkStrategy<Event> custom = WatermarkStrategy.forGenerator(
    ctx -> new CustomWatermarkGenerator()
);

// 적용
DataStream<Event> withWatermarks = stream
    .assignTimestampsAndWatermarks(strategy);
```

### 3. 다중 소스의 워터마크 처리

```
Source 1 파티션 A: WM = 10:05:00
Source 1 파티션 B: WM = 10:03:00   <- 이 파티션이 느림
Source 2:          WM = 10:06:00

연산자가 받는 효과적 워터마크 = min(10:05, 10:03, 10:06) = 10:03:00
-> 가장 느린 파티션이 전체 워터마크 진행을 막음 (Idle Source 문제)
```

<strong><a href="/studynote/02_operating_system/10_security/611_cpu_idle_wait_optimization/">Idle</a> Source 처리</strong>:
```java
WatermarkStrategy.<Event>forBoundedOutOfOrderness(Duration.ofSeconds(30))
    .withIdleness(Duration.ofMinutes(1));  // 1분 이상 이벤트 없으면 해당 파티션 무시
```

### 4. 워터마크 튜닝 트레이드오프

| 워터마크 크기 | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 이벤트 포용 | 결과 [지연 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) | 메모리 사용 |
|:---|:---|:---|:---|
| 너무 작음 (0초) | 극히 낮음 | 즉각 | 낮음 |
| 적정 (P99 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)) | 높음 | P99 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)만큼 | 보통 |
| 너무 큼 (1시간) | 매우 높음 | 1시간 이상 | 높음 (많은 상태 유지) |

**📢 섹션 요약 비유**
> 워터마크는 "학교 출석 마감 시간"과 같다. 마감(워터마크)이 짧으면 지각생([지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 이벤트)이 많이 누락되고, 마감이 길면 진짜 시작(결과 확정)이 늦어진다. P99 지각 시간을 파악해서 적정 마감을 정해야 한다.

---

## Ⅲ. 비교 및 연결

### 1. Flink vs Spark Structured Streaming의 워터마크

| 항목 | Flink Watermark | [Spark Structured Streaming](/studynote/16_bigdata/03_spark/061_structured_streaming/) Watermark |
|:---|:---|:---|
| [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 방식 | `forBoundedOutOfOrderness()` | `withWatermark("timestamp", "30 seconds")` |
| 윈도우 [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/) | 워터마크 기반 정밀 제어 | 워터마크 기반 (마이크로배치 내) |
| [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 이벤트 처리 | Side Output, allowedLateness | 워터마크 이후 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 무시 (기본) |
| [정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) | 이벤트 단위 | 마이크로배치 단위 |

### 2. 연결 개념

- <strong><a href="/studynote/16_bigdata/04_streaming/084_event_time_vs_processing_time/">Event Time vs Processing Time</a></strong>: 워터마크가 의미 있는 이유
- <strong><a href="/studynote/16_bigdata/04_streaming/086_window_operations/">Window Operations</a></strong>: 워터마크로 닫히는 대상
- **Side Output**: 워터마크 이후 도착한 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 이벤트의 대안 처리

**📢 섹션 요약 비유**
> Flink 워터마크는 "세밀한 항공기 충돌 방지 시스템"이고, Spark 워터마크는 "5분마다 상황을 점검하는 레이더"이다. 전자가 더 정밀하지만 복잡하고, 후자는 단순하지만 마이크로배치 주기의 오차가 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 1. 워터마크 적정값 결정 프로세스

```
Step 1: 이벤트 지연 분포 측정 (최소 1주일 데이터)
  - 지연 = 이벤트 수신 시간 - 이벤트 타임스탬프
  - P50 = 1초, P95 = 15초, P99 = 45초

Step 2: 비즈니스 허용 지연(Latency SLA) 확인
  - "1분 내에 집계 결과 필요" -> 최대 워터마크 한계

Step 3: 워터마크 = min(Latency SLA - 윈도우크기, P99_지연)
  - P99 = 45초, Latency SLA = 2분, 윈도우 = 5분
  - 워터마크 = 45초 (P99 기준)

Step 4: 모니터링
  - currentWatermark 메트릭 추적
  - 지연 이벤트 비율 모니터링 (Side Output 카운터)
```

### 2. [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

- [ ] 이벤트 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 분포 측정 (P95/P99 기준으로 워터마크 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/))
- [ ] [Idle](/studynote/02_operating_system/10_security/611_cpu_idle_wait_optimization/) Source 처리 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) (`withIdleness()`) — [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 불균형 대비
- [ ] 워터마크 [진행](/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링 (대시보드 or Flink UI)
- [ ] Side Output으로 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 이벤트 수 추적 -> [SLA](/studynote/12_it_management/02_itsm_itil/869_sla/) 이상 시 알림
- [ ] 다중 소스의 경우 가장 느린 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 및 처리

**📢 섹션 요약 비유**
> 워터마크 튜닝은 "교차로 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)등 타이밍 최적화"와 같다. 초록불 시간(워터마크 크기)이 너무 짧으면 대기 차량이 많이 누락되고, 너무 길면 교통 흐름이 느려진다. 실측 교통량([지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 분포) 기반으로 타이밍을 조정해야 한다.

---

## Ⅴ. 기대효과 및 결론

### 1. 기대효과

| 효과 | 설명 |
|:---|:---|
| 정확한 집계 | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 이벤트를 허용 범위 내에서 올바른 윈도우에 포함 |
| 윈도우 결정론적 닫힘 | "언제 윈도우가 닫히는가"를 명확히 정의 |
| 튜닝 가능한 정확도 | P99 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 기반 워터마크로 정확도-[지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 균형 |

### 2. 결론

워터마크는 이벤트 시간 스트리밍의 <strong>"시간 <a href="/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/">진행</a>을 정의하는 핵심 메커니즘"</strong>이다. 기술사 답안에서는 워터마크의 수식(`WM = max_event_time - allowed_lateness`), 워터마크가 어떻게 윈도우 닫힘을 결정하는지, 다중 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)에서의 min-watermark 동작, 그리고 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 이벤트 처리 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 함께 서술해야 완성도 높은 답안이 된다.

**📢 섹션 요약 비유**
> 워터마크 없는 이벤트 시간 처리는 "도착 시간을 알 수 없는 소포를 언제까지 기다려야 하는지 모르는 상황"이다. 워터마크는 "5일이 지나면 분실 처리하겠다"는 명확한 기준을 제공하여, 배송 시스템이 멈추지 않고 돌아갈 수 있게 한다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| Event Time | 전제 개념 | 워터마크는 이벤트 시간 처리에서만 의미 |
| [Window Operations](/studynote/16_bigdata/04_streaming/086_window_operations/) | 직접 연동 | 워터마크가 윈도우 닫힘을 결정 |
| Side Output | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 이벤트 대안 | 워터마크 이후 도착한 이벤트 처리 |
| [Idle](/studynote/02_operating_system/10_security/611_cpu_idle_wait_optimization/) Source | 문제 케이스 | [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)이 정지되면 워터마크가 [진행](/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 안 됨 |
| Exactly-Once | 목적 | 워터마크 기반 정확한 윈도우 집계 보장 |

### 📈 관련 키워드 및 발전 흐름도

```text
[이벤트 시간 (Event Time) — 데이터 실제 발생 시각]
    |
    v
[처리 시간 (Processing Time) — 시스템이 데이터를 수신한 시각]
    |
    v
[지연 데이터 (Late Data) — 네트워크 지연으로 늦게 도착한 이벤트]
    |
    v
[워터마크 (Watermark) — 지연 허용 임계값, 이후 데이터 무시]
    |
    v
[윈도우 집계 (Window Aggregation) — 시간 범위별 스트리밍 집계]
    |
    v
[상태 관리 (Stateful Processing) — 윈도우 상태 메모리 보관·정리]
```
워터마크는 이벤트 시간 기반 스트리밍에서 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리의 허용 한계를 정의하며, [정확성](/studynote/16_bigdata/01_intro/002_bigdata_5v/)과 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 간의 트레이드오프를 제어하는 핵심 메커니즘이다.

### 👶 어린이를 위한 3줄 비유 설명

선생님이 숙제 검사를 할 때 "30분까지 가져오면 봐줄게(워터마크 = 30분)"라고 하면, 조금 늦은 친구([지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 이벤트)도 30분 안에 내면 검사를 받을 수 있어요. 30분이 지나면(워터마크 초과) 선생님은 제출 마감(윈도우 닫힘)을 선언하고 채점을 시작해요. 너무 오래 기다리면 성적표가 늦게 나오니까 적당한 시간을 정하는 것이 중요해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 85 / 262

<- **이전**: [09. 이벤트 시간 vs 처리 시간 (Event Time vs Processing Time)](/studynote/16_bigdata/04_streaming/084_event_time_vs_processing_time/)
**다음**: [11. 윈도우 연산 (Window Operations) — 텀블링/슬라이딩/세션](/studynote/16_bigdata/04_streaming/086_window_operations/) ->

---
