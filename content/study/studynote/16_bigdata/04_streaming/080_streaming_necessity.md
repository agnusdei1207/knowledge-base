+++
weight = 80
title = "05. 스트리밍 처리 필요성 — 실시간 의사결정의 한계 극복"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)

- **본질**: 스트리밍 처리(Streaming Processing)는 [[001_dikw_pyramid|데이터]]가 [[087_process_state_transition|생성]]되는 즉시 처리하여 밀리초~초 단위의 의사결정을 가능하게 하는 패러다임으로, [[228_batch_processing_hadoop_spark|배치 처리]]([[228_batch_processing_hadoop_spark|Batch Processing]])의 수 시간 [[015_지연_데이터_관점|지연]]이 비즈니스 가치를 소멸시키는 영역(사기 탐지, [[101_iot_concept|IoT]] 이상 감지, 주식 거래)에서 필수적이다.
- **가치**: 같은 [[001_dikw_pyramid|데이터]]라도 "1분 뒤"가 아닌 "지금 이 순간" 처리하는 것이 결과의 비즈니스 가치를 결정하는 영역이 있다. 신용카드 사기는 거래 후 수 초 안에 탐지해야 하고, [[101_iot_concept|IoT]] 센서 이상은 발생 즉시 경보해야 하며, 재고 최적화는 실시간 수요 변동에 즉각 반응해야 한다.
- **판단 포인트**: 스트리밍과 [[228_batch_processing_hadoop_spark|배치 처리]] 선택의 핵심은 **허용 [[141_latency|지연 시간]]([[141_latency|Latency]] [[085_sla|SLA]])**이다. 수 초 이내가 필요하면 스트리밍, 수십 분~수 시간이 허용되면 마이크로배치, 하루 이상이면 배치가 적합하며 스트리밍은 배치보다 인프라 복잡도와 비용이 높다.

---

## Ⅰ. 개요 및 필요성

### 1. [[228_batch_processing_hadoop_spark|배치 처리]]의 한계

전통적인 빅데이터 처리는 하루치 [[001_dikw_pyramid|데이터]]를 밤에 모아서 새벽에 일괄 처리(Batch)하는 T+1 패턴이었다. 이 방식은 대부분의 BI/리포팅 요구사항을 만족했지만, 비즈니스 환경이 빨라지면서 다음 한계가 부각됐다.

| [[228_batch_processing_hadoop_spark|배치 처리]]의 한계 | 실제 영향 |
|:---|:---|
| [[001_dikw_pyramid|데이터]] [[015_지연_데이터_관점|지연]] (수 시간~1일) | 사기 탐지 시 이미 거래 완료 |
| 야간 배치 창 이용 | 피크 시간 실시간 인사이트 불가 |
| 대량 재처리 부담 | 오류 [[001_dikw_pyramid|데이터]] 수정 시 전체 배치 재실행 |
| 이벤트 기반 대응 불가 | 공장 설비 이상 발견 시 이미 폭발 |

### 2. 스트리밍이 필수인 사용 사례

```
[스트리밍 처리가 필수인 영역]

1. 금융 사기 탐지
   이벤트: 카드 결제 발생
   요구 지연: < 500ms
   이유: 결제 승인 전에 사기 판단 필요

2. IoT 이상 감지
   이벤트: 온도 센서 급등
   요구 지연: < 1초
   이유: 설비 폭발/화재 방지

3. 주식/암호화폐 자동 거래
   이벤트: 가격 변동
   요구 지연: < 10ms (초고빈도 거래)
   이유: 가격 차익거래 기회는 수 ms에 소멸

4. 실시간 개인화 추천
   이벤트: 사용자 클릭/탐색
   요구 지연: < 100ms
   이유: 현재 세션 컨텍스트로 즉각 추천

5. 네트워크 침해 탐지 (SIEM)
   이벤트: 로그인 시도/트래픽 급증
   요구 지연: < 5초
   이유: 침해 확산 전 격리 조치
```

**📢 섹션 요약 비유**
> [[228_batch_processing_hadoop_spark|배치 처리]]는 "하루치 우편물을 저녁에 한꺼번에 배달하는 우체부"이고, 스트리밍은 "편지가 도착하는 즉시 수신자에게 전달하는 퀵서비스"다. 대부분은 저녁 배달로 충분하지만, 긴급 서류는 퀵서비스가 필수다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. [[019_처리_지연|처리 지연]] 스펙트럼

```
지연 시간 스펙트럼
│
│ < 1ms   ┤ 초고빈도 거래 (Custom FPGA/ASIC, CEP)
│ < 100ms ┤ 결제 사기 탐지, 실시간 추천
│ < 1s    ┤ IoT 이상 감지, 알림
│ < 10s   ┤ 대시보드 실시간 지표, SIEM
│ < 1min  ┤ Spark Structured Streaming (마이크로배치)
│ < 1hr   ┤ Spark 배치 (소규모)
│ < 1day  ┤ Hadoop MapReduce 야간 배치
│
└─────────────────────────────────────────────
  스트리밍 필수 영역 ←─────────→ 배치 가능 영역
```

### 2. [[216_lambda_kappa_architecture_batch_realtime|Lambda]] vs [[235_kappa|Kappa]] 아키텍처

| 아키텍처 | 구조 | 장점 | 단점 |
|:---|:---|:---|:---|
| [[095_lambda_architecture|Lambda Architecture]] | 배치 레이어 + 스피드 레이어 + 서빙 레이어 | [[002_bigdata_5v|정확성]](배치) + 속도(스트리밍) 양립 | 코드 [[456_dual_redundancy|이중화]], 운영 복잡도 |
| [[096_kappa_architecture|Kappa Architecture]] | 스트리밍 단일 레이어 | 단순, 일관된 [[007_codebase|코드베이스]] | 재처리 시 [[179_kafka_flink_watermark_time_window|Kafka]] 리플레이 필요 |

### 3. 스트리밍 처리 핵심 개념 비교

| 구분 | [[228_batch_processing_hadoop_spark|배치 처리]] | 마이크로배치 | 진정한 스트리밍 |
|:---|:---|:---|:---|
| 대표 기술 | [[395_hadoop_mapreduce_disk_bottleneck|Hadoop MapReduce]] | [[061_structured_streaming|Spark Structured Streaming]] | [[215_flink_native_stream_watermark_window_time|Apache Flink]], [[044_apache_storm|Apache Storm]] |
| 처리 단위 | 고정 [[001_dikw_pyramid|데이터]]셋 | 시간 슬롯 (수 초~수 분) | 이벤트 단위 |
| [[141_latency|지연 시간]] | 분~시간 | 초~분 | 밀리초~초 |
| 상태 관리 | 없음 | 제한적 | 완전한 상태 기반 |
| 정확한 한 번 처리 | 기본 제공 | 가능 | 복잡([[549_2pc_two_phase_commit_limitations_msa|2PC]] 필요) |

**📢 섹션 요약 비유**
> 스트리밍 아키텍처 선택은 "음식 배달 시스템 설계"와 같다. Lambda는 레스토랑(배치) + 패스트푸드(스트리밍)를 병행 운영하는 것이고, Kappa는 패스트푸드만으로 모든 수요를 충족하는 방식이다. 메뉴([[001_dikw_pyramid|데이터]] 복잡도)에 따라 선택이 달라진다.

---

## Ⅲ. 비교 및 연결

### 1. 스트리밍 기술 [[057_stack|스택]] 선택 기준

| 요구사항 | 권장 기술 |
|:---|:---|
| 밀리초 [[015_지연_데이터_관점|지연]] + 상태 기반 + Exactly-Once | [[215_flink_native_stream_watermark_window_time|Apache Flink]] |
| Spark 기반 기존 인프라 확장 | [[061_structured_streaming|Spark Structured Streaming]] |
| [[179_kafka_flink_watermark_time_window|Kafka]] 네이티브 SQL 스트리밍 | ksqlDB |
| AWS 관리형 [[090_service_kubernetes_network_load_balancing|서비스]] | [[091_amazon_kinesis|Amazon Kinesis]] + [[216_lambda_kappa_architecture_batch_realtime|Lambda]]/Flink |
| 대용량 내구성 [[389_mesh_topology|메시]]지 큐 | [[214_kafka_pubsub_topic_partition_offset_broker|Apache Kafka]] |

### 2. 연결 개념

- **[[084_event_time_vs_processing_time|Event Time vs Processing Time]]**: 스트리밍의 핵심 시간 개념
- **[[085_watermark|Watermark]]**: [[015_지연_데이터_관점|지연]] 이벤트 허용 임계값 — 스트리밍 [[002_bigdata_5v|정확성]]의 핵심
- **[[083_cross_validation|Exactly-Once Semantics]]**: 스트리밍 [[001_dikw_pyramid|데이터]] [[442_consistency_integrity|무결성 보장]] 메커니즘

**📢 섹션 요약 비유**
> 스트리밍 처리 필요성을 판단할 때는 "의사결정의 유통기한"을 따져야 한다. 30일이 지나도 유효한 통계는 배치로 충분하고, 10초 안에 썩는 의사결정 정보는 스트리밍이 필수다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 1. 스트리밍 도입 의사결정 프레임워크

```
Step 1: 비즈니스 요구 지연 시간(Latency SLA) 명확화
  - "1분 이내에 사기를 탐지해야 한다" → 스트리밍 필요
  - "매일 아침 전날 매출 리포트" → 배치로 충분

Step 2: 데이터 볼륨과 속도 추정
  - 초당 수천~수백만 이벤트 → 스트리밍 인프라 필요
  - 하루 수 GB → 야간 배치로 가능

Step 3: 상태 관리 요구사항 확인
  - 이전 이벤트와 비교/연관 분석 필요? → 상태 기반 스트리밍 엔진
  - 단순 필터/변환만 필요? → 간단한 마이크로배치로 가능

Step 4: 운영 역량 및 비용 검토
  - 스트리밍은 배치보다 운영 복잡도 2~5배 높음
  - Exactly-Once 보장, 장애 복구 전략 수립 필요
```

### 2. 스트리밍 도입 [[435_checklist_based_testing|체크리스트]]

- [ ] [[141_latency|Latency]] [[085_sla|SLA]] 문서화 (비즈니스 요구사항 기반)
- [ ] 초당 이벤트 수(EPS) 피크 추정
- [ ] 상태 저장 연산(집계, 조인) 필요 여부 판단
- [ ] Exactly-Once vs At-Least-Once 선택 (비용-[[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 트레이드오프)
- [ ] 장애 [[658_ir_recovery|복구]] 및 재처리 [[268_strategy_pattern|전략]] 수립
- [ ] 클라우드 vs [[061_on_premise_legacy_infrastructure|온프레미스]] 스트리밍 플랫폼 선택

**📢 섹션 요약 비유**
> 스트리밍 도입은 "응급실 vs 일반 외래 진료 선택"이다. 모든 환자를 응급실(스트리밍)로 보내면 과부하가 걸린다. 진짜 응급 상황(실시간 의사결정 필수)만 응급실로, 나머지는 예약 진료(배치)로 효율적으로 [[104_classification_analysis|분류]]해야 한다.

---

## Ⅴ. 기대효과 및 결론

### 1. 기대효과

| 영역 | 효과 | 수치 예시 |
|:---|:---|:---|
| 사기 탐지 | 피해 예방 | 탐지 [[015_지연_데이터_관점|지연]] 1일 → 수 초 시 손실 90% 감소 |
| [[101_iot_concept|IoT]] [[229_monitor|모니터]]링 | 장비 [[452_availability|가용성]] 향상 | 장애 예방율 30~50% 향상 |
| 실시간 추천 | 전환율 증가 | [[160_session_controlling_terminal|세션]] [[033_context|컨텍스트]] 추천 시 [[090_ctr_mode|CTR]] 15~25% 향상 |
| 운영 비용 | 배치 대비 인프라 비용 증가 | 2~5배 운영 비용 증가 (트레이드오프) |

### 2. 결론

스트리밍 처리는 "필요한 곳에 선택적으로" 적용해야 하는 고비용 아키텍처다. 기술사 답안에서는 배치-마이크로배치-스트리밍의 **[[015_지연_데이터_관점|지연]]-비용-복잡도 트레이드오프**를 명확히 설명하고, [[216_lambda_kappa_architecture_batch_realtime|Lambda]]/[[235_kappa|Kappa]] 아키텍처의 장단점과 함께 비즈니스 요구에 따른 기술 선택 근거를 제시하는 것이 핵심이다.

**📢 섹션 요약 비유**
> 스트리밍 처리 필요성은 "속도 위반 단속 카메라 vs 블랙박스 사후 분석"의 차이다. 사고를 막으려면 실시간 단속(스트리밍)이 필요하고, 사고 원인 분석은 블랙박스(배치)로 충분하다. 목적에 맞는 도구를 선택해야 한다.

---

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---|:---|:---|
| [[215_flink_native_stream_watermark_window_time|Apache Flink]] | 핵심 스트리밍 엔진 | 상태 기반 이벤트 시간 처리의 표준 |
| [[214_kafka_pubsub_topic_partition_offset_broker|Apache Kafka]] | [[389_mesh_topology|메시]]지 소스 | 스트리밍 [[001_dikw_pyramid|데이터]] [[454_buffering|버퍼링]] 및 내구성 보장 |
| [[095_lambda_architecture|Lambda Architecture]] | 아키텍처 패턴 | 배치+스트리밍 이중 처리 구조 |
| [[096_kappa_architecture|Kappa Architecture]] | 대안 패턴 | 스트리밍 단일화로 운영 단순화 |
| [[085_watermark|Watermark]] | 핵심 메커니즘 | [[015_지연_데이터_관점|지연]] 이벤트 처리 정확도 조절 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Apache Flink]
    │
    ▼
[Apache Kafka]
    │
    ▼
[Lambda Architecture]
    │
    ▼
[Kappa Architecture]
    │
    ▼
[Watermark]
```

이 흐름도는 Apache Flink에서 출발해 Watermark까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

[[228_batch_processing_hadoop_spark|배치 처리]]는 하루치 편지를 저녁에 한꺼번에 가져다주는 우체부이고, 스트리밍은 편지가 오자마자 즉시 배달해주는 퀵서비스예요. 평소 편지는 저녁 배달로 충분하지만, 엄마한테 "지금 당장 집에 와야 해!"라는 긴급 [[389_mesh_topology|메시]]지는 퀵서비스(스트리밍)로 보내야 해요. 모든 편지를 퀵서비스로 보내면 비용이 너무 많이 들기 때문에 진짜 급한 것만 스트리밍을 써야 해요!
