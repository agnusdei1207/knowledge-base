+++
title = "044. 카파 아키텍처 — 단일 스트리밍 레이어"
date = 2026-04-05

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

> **핵심 인사이트**
> 1. [카파 아키텍처](/knowledge-base/studynote/16_bigdata/04_streaming/096_kappa_architecture/)([Kappa Architecture](/knowledge-base/studynote/16_bigdata/04_streaming/096_kappa_architecture/))는 Jay Kreps(LinkedIn)가 2014년 제안한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 아키텍처로 — [람다](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) 아키텍처의 "배치 + 스피드 레이어 이중 코드" 문제를 스트리밍 레이어 하나로 통합하여 해결한다.
> 2. 카파의 핵심은 Kafka를 이벤트 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)(Event Log)로 활용하는 것으로 — 모든 히스토리 이벤트를 Kafka에 보관하고, 재처리(Reprocessing)가 필요할 때 스트리밍 처리를 처음부터 재실행하여 배치 처리를 대체한다.
> 3. 카파는 코드 단순성과 운영 효율에서 [람다](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)를 능가하지만 — 대규모 재처리 시 자원 집약적이고 Kafka의 무한 보관 비용이 실용적 제약이 되어, 실제로는 도메인과 워크로드 특성에 따라 [람다](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)·카파·통합 플랫폼을 선택적으로 적용하는 것이 현실이다.

---

## Ⅰ. [카파 아키텍처](/knowledge-base/studynote/16_bigdata/04_streaming/096_kappa_architecture/) 개념



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">카파 아키텍처 (Kappa Architecture):</div>
<div class="kb-diagram-note">Jay Kreps (LinkedIn/Confluent) 제안, 2014년</div>
<div class="kb-diagram-note">람다의 문제:</div>
<div class="kb-diagram-note">배치 레이어 + 스피드 레이어 = 동일 로직 2회 구현</div>
<div class="kb-diagram-note">→ 코드 불일치 위험, 유지보수 비용 2배</div>
<div class="kb-diagram-note">카파의 해결:</div>
<div class="kb-diagram-note">스트리밍 레이어만 사용 (배치 레이어 제거)</div>
<div class="kb-diagram-note">재처리 = 스트리밍을 처음부터 재실행</div>
<div class="kb-diagram-note">아키텍처:</div>
<div class="kb-diagram-note">모든 데이터 소스</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Kafka (이벤트 로그, 영구 보관)</div>
<div class="kb-diagram-tree-item" style="--depth:3">스트리밍 처리 v1 (현재 버전)</div>
<div class="kb-diagram-note">↓ 서빙 레이어 (실시간 결과)</div>
<div class="kb-diagram-tree-item" style="--depth:3">재처리 필요 시: 스트리밍 v2 (새 버전)</div>
<div class="kb-diagram-note">(Kafka 처음부터 재실행)</div>
<div class="kb-diagram-note">↓ 새 서빙 레이어</div>
<div class="kb-diagram-note">v2 안정화 후 v1 폐기 → v2가 메인</div>
<div class="kb-diagram-note">핵심 원칙:</div>
<div class="kb-diagram-note">1. 모든 데이터는 이벤트 로그 (Kafka)</div>
<div class="kb-diagram-note">2. 스트리밍이 유일한 처리 레이어</div>
<div class="kb-diagram-note">3. 재처리 = Kafka Consumer group 초기화</div>
<div class="kb-diagram-note">4. 서빙 레이어: 처리 결과 저장 (Redis, Cassandra)</div>
<div class="kb-diagram-note">람다 vs 카파:</div>
<div class="kb-diagram-note">람다: 두 파이프라인 (정확성 + 속도)</div>
<div class="kb-diagram-note">카파: 하나의 파이프라인 (속도 + 정확성)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [카파 아키텍처](/knowledge-base/studynote/16_bigdata/04_streaming/096_kappa_architecture/)는 단 하나의 스마트 컨베이어 — [람다](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)가 낮 컨베이어(배치) + 야간 컨베이어(스피드) 두 개라면, 카파는 하나의 스마트 컨베이어로 모든 것 처리.

---

## Ⅱ. [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 이벤트 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)

```
Kafka 이벤트 로그 (Event Log):

카파의 Kafka 활용:
  일반적 Kafka: 수일~수주 보관 (소비 후 삭제)
  카파의 Kafka: 장기 보관 (수개월~무한)
  
  이유: 재처리 시 과거 이벤트 모두 필요

Kafka 보관 설정:
  retention.bytes = -1  (무제한 크기)
  retention.ms = -1     (무제한 기간)
  cleanup.policy = compact (키 기반 중복 제거)
  
  또는:
  S3 티어링 (Kafka + S3):
  실시간: Kafka 보관 (7일)
  장기: S3에 offload (무제한)
  Apache Kafka + Confluent Tiered Storage

소비자 그룹 초기화 (재처리):
  # v1 (현재)
  kafka-consumer-groups.sh --bootstrap-server ... 
    --group v1-processor --describe
    
  # v2 재처리 시작 (오프셋을 처음으로)
  kafka-consumer-groups.sh --bootstrap-server ...
    --group v2-processor --reset-offsets 
    --to-earliest --execute

이벤트 설계:
  이벤트 소싱 (Event Sourcing):
  현재 상태 대신 이벤트 로그로 상태 재현
  
  orders 이벤트:
  {"event": "OrderCreated", "order_id": "A1", "amount": 100}
  {"event": "OrderPaid", "order_id": "A1"}
  {"event": "OrderShipped", "order_id": "A1", "tracking": "T1"}
  
  재처리: 처음부터 재생하면 현재 상태 재현 가능
```

> 📢 **섹션 요약 비유**: [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 이벤트 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 일기장 — 오늘의 상태(모놀리식 DB) 대신, 매일 일어난 사건(이벤트)을 일기로 기록. 처음부터 일기 읽으면 현재 상태를 재현할 수 있어요.

---

## Ⅲ. 스트리밍 처리 엔진



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">카파 아키텍처 스트리밍 처리 엔진:</div>
<div class="kb-diagram-note">Apache Flink:</div>
<div class="kb-diagram-note">진정한 스트리밍 처리 (마이크로 배치 아님)</div>
<div class="kb-diagram-note">이벤트 타임 처리 (Event Time Processing)</div>
<div class="kb-diagram-note">정확히 한 번 (Exactly-Once) 시맨틱</div>
<div class="kb-diagram-note">강점:</div>
<div class="kb-diagram-tree-item" style="--depth:1">지연 없는 실시간 처리</div>
<div class="kb-diagram-tree-item" style="--depth:1">윈도우 연산 정확성</div>
<div class="kb-diagram-tree-item" style="--depth:1">상태 관리 (State Backend: RocksDB)</div>
<div class="kb-diagram-note">카파 재처리:</div>
<div class="kb-diagram-note">Flink Job v2 시작 → Kafka 처음부터 소비</div>
<div class="kb-diagram-note">→ 병렬 처리로 히스토리 빠르게 재처리</div>
<div class="kb-diagram-note">Apache Kafka Streams:</div>
<div class="kb-diagram-note">Kafka 내장 스트리밍 라이브러리</div>
<div class="kb-diagram-note">별도 클러스터 불필요 (경량)</div>
<div class="kb-diagram-note">장점: 운영 단순, 마이크로서비스 내장 가능</div>
<div class="kb-diagram-note">단점: Kafka 생태계 종속, 복잡 집계 제약</div>
<div class="kb-diagram-note">Apache Spark Structured Streaming:</div>
<div class="kb-diagram-note">마이크로 배치 기반 (수초 단위)</div>
<div class="kb-diagram-note">Spark 기존 코드 재활용 가능</div>
<div class="kb-diagram-note">장점: 데이터 엔지니어 학습 곡선 낮음</div>
<div class="kb-diagram-note">단점: 진정한 실시간 아님 (마이크로 배치)</div>
<div class="kb-diagram-note">도구 선택:</div>
<div class="kb-diagram-note">ms 단위 실시간: Flink</div>
<div class="kb-diagram-note">초 단위 거의 실시간: Spark Structured Streaming</div>
<div class="kb-diagram-note">경량 서비스 내장: Kafka Streams</div>
<div class="kb-diagram-note">기존 Spark 환경: Structured Streaming</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 스트리밍 엔진 선택은 배달 방식 선택 — Flink는 즉시 배달(수ms), Spark Streaming은 배달 묶음(수초), [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Streams는 자전거 배달(경량). 주문 규모에 맞게 선택.

---

## Ⅳ. 카파의 장단점과 선택 기준



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">카파 vs 람다 상세 비교:</div>
<div class="kb-diagram-note">코드 복잡도:</div>
<div class="kb-diagram-note">람다: 동일 로직을 Spark(배치) + Flink(스피드) 두 번 구현</div>
<div class="kb-diagram-note">카파: Flink 하나로 통합</div>
<div class="kb-diagram-note">→ 카파: 코드 50% 절감</div>
<div class="kb-diagram-note">재처리 성능:</div>
<div class="kb-diagram-note">람다: Spark 배치 → 빠른 재처리 (수천 TB/시간)</div>
<div class="kb-diagram-note">카파: Flink 스트리밍 → 느린 재처리 (수백 GB/시간)</div>
<div class="kb-diagram-note">→ 람다: 대규모 재처리 유리</div>
<div class="kb-diagram-note">보관 비용:</div>
<div class="kb-diagram-note">람다: S3 파일 시스템 (저렴)</div>
<div class="kb-diagram-note">카파: Kafka 무한 보관 → 비용 증가</div>
<div class="kb-diagram-note">→ 람다: 장기 보관 유리</div>
<div class="kb-diagram-note">데이터 일관성:</div>
<div class="kb-diagram-note">람다: 배치 뷰 + 스피드 뷰 병합 (복잡한 쿼리)</div>
<div class="kb-diagram-note">카파: 단일 스트리밍 출력 (단순한 쿼리)</div>
<div class="kb-diagram-note">→ 카파: 일관성 단순</div>
<div class="kb-diagram-note">운영 복잡도:</div>
<div class="kb-diagram-note">람다: 두 파이프라인 운영</div>
<div class="kb-diagram-note">카파: 하나의 파이프라인</div>
<div class="kb-diagram-note">→ 카파: 운영 단순</div>
<div class="kb-diagram-note">선택 기준:</div>
<div class="kb-diagram-note">카파 적합:</div>
<div class="kb-diagram-note">이벤트 스트림 중심 시스템</div>
<div class="kb-diagram-note">실시간 처리 우선</div>
<div class="kb-diagram-note">재처리 빈도 낮음</div>
<div class="kb-diagram-note">팀 규모 작음 (운영 인력 제약)</div>
<div class="kb-diagram-note">람다 적합:</div>
<div class="kb-diagram-note">대규모 히스토리 데이터 (TB 단위)</div>
<div class="kb-diagram-note">복잡한 배치 집계 (ML 피처 등)</div>
<div class="kb-diagram-note">재처리 자주 필요</div>
<div class="kb-diagram-note">정확성 최우선 (금융)</div>
<div class="kb-diagram-note">현대적 대안:</div>
<div class="kb-diagram-note">Delta Lake + Apache Spark:</div>
<div class="kb-diagram-note">배치+스트리밍 동일 코드 처리</div>
<div class="kb-diagram-note">람다의 이점 + 카파의 단순성 = 통합 아키텍처</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 카파 vs [람다](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)는 하나의 다용도 냄비 vs 전용 요리기구 세트 — 카파는 하나로 다 해결(단순하지만 한계), [람다](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)는 각 음식별 전용 도구(복잡하지만 최적화).

---

## Ⅴ. 실무 시나리오 — 실시간 사기 탐지



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">결제 사기 탐지 카파 아키텍처:</div>
<div class="kb-diagram-note">요구사항:</div>
<div class="kb-diagram-note">모든 결제 트랜잭션 실시간 분석</div>
<div class="kb-diagram-note">사기 패턴 탐지: ms 단위 응답</div>
<div class="kb-diagram-note">모델 업데이트 시 전체 재처리 가능</div>
<div class="kb-diagram-note">카파 아키텍처:</div>
<div class="kb-diagram-note">결제 이벤트 → Kafka (무한 보관)</div>
<div class="kb-diagram-note">→ Flink Job v1 (사기 탐지 모델 v1)</div>
<div class="kb-diagram-note">→ 결과: Redis (블랙리스트) + Cassandra (로그)</div>
<div class="kb-diagram-note">→ 결제 API: Redis 조회 후 허용/거부</div>
<div class="kb-diagram-note">모델 업데이트 시나리오:</div>
<div class="kb-diagram-note">사기 패턴 변경 → 모델 v2 학습</div>
<div class="kb-diagram-note">재처리 과정:</div>
<div class="kb-diagram-note">1. Flink Job v2 시작 (새 모델 적용)</div>
<div class="kb-diagram-note">2. Kafka Consumer Group 오프셋: 처음부터</div>
<div class="kb-diagram-note">3. 병렬 처리: v2가 Kafka 히스토리 소비</div>
<div class="kb-diagram-note">4. 새 Redis/Cassandra에 결과 저장</div>
<div class="kb-diagram-note">v2 재처리 완료 후:</div>
<div class="kb-diagram-note">5. 결제 API: v1 Redis → v2 Redis로 전환</div>
<div class="kb-diagram-note">6. v1 Flink Job 종료</div>
<div class="kb-diagram-note">성능:</div>
<div class="kb-diagram-note">실시간 처리: &lt;50ms 지연 (사기 탐지)</div>
<div class="kb-diagram-note">재처리 속도: 3개월 히스토리 재처리 ~4시간</div>
<div class="kb-diagram-note">(병렬화로 단축 가능)</div>
<div class="kb-diagram-note">카파 vs 람다 결정:</div>
<div class="kb-diagram-note">이 시나리오: 카파 적합</div>
<div class="kb-diagram-note">이유: ms 단위 응답 필요 + 스트리밍 중심</div>
<div class="kb-diagram-note">재처리 4시간은 허용 범위 내</div>
<div class="kb-diagram-note">람다 필요 사례:</div>
<div class="kb-diagram-note">월간 집계 정산 (TB 단위 배치 처리 필요)</div>
<div class="kb-diagram-note">→ 카파의 재처리로는 비효율적</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 결제 사기 탐지 카파는 보안 카메라 + 즉시 알림 — 모든 거래(이벤트)를 실시간으로 분석하고, 의심 패턴 발견 시 즉시 차단. 녹화([Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 보관)를 처음부터 재생하면 과거 분석도 가능.

---

## 📌 관련 개념 맵

```
카파 아키텍처
+-- 핵심 요소
|   +-- Kafka (이벤트 로그, 무한 보관)
|   +-- 스트리밍 처리 (Flink, Kafka Streams)
|   +-- 서빙 레이어 (Redis, Cassandra)
+-- 재처리 메커니즘
|   +-- Consumer Group 오프셋 초기화
|   +-- 병렬 처리로 빠른 재처리
+-- 비교
|   +-- 람다 (배치+스피드, 코드 중복)
|   +-- 카파 (스트리밍 통합, 단순)
+-- 대안
|   +-- Delta Lake + Spark (통합 플랫폼)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[람다 아키텍처 (2012)]
Nathan Marz: 배치+스피드 레이어
정확성+실시간성 동시 달성
      |
      v
[카파 아키텍처 (2014)]
Jay Kreps: 스트리밍으로 통합
Kafka 이벤트 로그 중심
      |
      v
[Flink 고도화 (2015~)]
이벤트 타임, Exactly-Once
카파의 기술적 기반 강화
      |
      v
[통합 플랫폼 (2019~)]
Delta Lake, Apache Iceberg
배치+스트리밍 동일 코드
      |
      v
[현재: 스트림 중심]
Kafka + Flink 사실상 표준
람다 단순화 추세
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. [카파 아키텍처](/knowledge-base/studynote/16_bigdata/04_streaming/096_kappa_architecture/)는 하나의 스마트 컨베이어 — [람다](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)가 낮 컨베이어 + 야간 컨베이어 두 개라면, 카파는 하나로 24시간 처리해요!
2. Kafka는 일기장 — 모든 사건을 일기로 기록해두면, 나중에 처음부터 읽어서 현재 상태를 재현할 수 있어요.
3. 재처리가 핵심 장점 — 분석 방법을 바꿔야 할 때, [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 일기장의 처음부터 다시 읽으면 되어요. 배치 시스템 없이도 가능!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 44 / 258

← **이전**: [043. 람다 아키텍처 — 배치 & 스피드 레이어](/knowledge-base/studynote/14_data_engineering/01_infrastructure/043_lambda_architecture_batch_speed_layer/)
**다음**: [045. 컬럼형 저장 형식 — Parquet & ORC](/knowledge-base/studynote/14_data_engineering/01_infrastructure/045_columnar_storage_format_parquet_orc/) →

---
