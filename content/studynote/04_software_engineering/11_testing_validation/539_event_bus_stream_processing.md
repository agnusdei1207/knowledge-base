+++
title = "539. 이벤트 버스 및 스트림 프로세싱"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 이벤트 버스(Event Bus)는 발행-구독(Pub/Sub) 방식으로 이벤트를 여러 소비자에게 전달하는 중앙 채널이고, 스트림 프로세싱(Stream Processing)은 이 연속적 이벤트 흐름을 실시간으로 변환·집계·분석하는 처리 엔진이다.
> 2. **가치**: 이벤트 버스는 서비스 간 느슨한 결합을 유지하면서 다수의 소비자에게 동일 이벤트를 전달하고, 스트림 프로세싱은 대용량 실시간 데이터에서 즉각적인 인사이트(이상 탐지, 실시간 추천, 집계 통계)를 추출한다.
> 3. **판단 포인트**: 이벤트 버스는 전달(routing)이 핵심이고 스트림 프로세싱은 계산(computation)이 핵심이며, 윈도우 처리(Window Processing), 상태 관리(Stateful Processing), 지연(Latency) 요구사항을 기준으로 도구를 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

이벤트 버스와 스트림 프로세싱은 이벤트 기반 아키텍처(EDA)를 구성하는 두 개의 핵심 인프라 계층이다. 이벤트 버스는 생산자가 발행한 이벤트를 적절한 소비자에게 전달하는 "고속도로" 역할을 하고, 스트림 프로세싱은 그 고속도로를 달리는 데이터를 실시간으로 가공하는 "공장" 역할을 한다.

이벤트 버스의 필요성은 서비스가 증가할수록 커진다. 초기에는 주문 서비스가 결제 서비스를 직접 호출할 수 있지만, 재고·배송·알림·포인트·통계 서비스가 추가되면 주문 서비스는 점점 더 많은 서비스를 직접 알아야 한다. 이벤트 버스는 이 문제를 해결한다. 주문 서비스는 이벤트만 발행하고, 관심 있는 서비스는 스스로 구독한다.

스트림 프로세싱이 필요한 이유는 실시간성(Real-time)이다. 하루가 지나서 배치 처리로 분석하면 이미 늦은 경우가 많다. 카드 사기 감지, 실시간 재고 업데이트, 사용자 행동 기반 즉시 추천, 실시간 대시보드는 이벤트가 발생하는 즉시 처리가 필요하다. Apache Flink, Kafka Streams, Apache Spark Structured Streaming이 대표적인 스트림 처리 엔진이다.

- **📢 섹션 요약 비유**: 이벤트 버스는 여러 TV 채널에 동시에 방송을 내보내는 방송국 송출 시스템이고, 스트림 프로세싱은 방송을 받아 실시간 자막을 달거나 여러 채널 시청률을 동시에 계산하는 방송 제작 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 이벤트 버스 vs 스트림 프로세서 구조 비교



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">이벤트 버스 (Event Bus) - 전달 중심</div></div>
<div class="kb-diagram-note">생산자 서비스들 이벤트 버스 소비자 서비스들</div>
<div class="kb-diagram-note">주문 서비스 ──→ (Kafka Topic ──→ 결제 서비스</div>
<div class="kb-diagram-note">결제 서비스 ──→ 또는 EventBridge) ──→ 재고 서비스</div>
<div class="kb-diagram-note">배송 서비스 ──→ ──→ 알림 서비스</div>
<div class="kb-diagram-tree-item" style="--depth:8">→ 분석 서비스</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">스트림 프로세서 (Stream Processor) - 계산 중심</div></div>
<div class="kb-diagram-note">이벤트 버스 (소스) → 스트림 프로세서 → 결과 (싱크)</div>
<div class="kb-diagram-note">Kafka Topic → (Flink/Kafka → DB / Kafka Topic</div>
<div class="kb-diagram-note">Streams) → / 대시보드 / 알림</div>
</div>
</div>



### 주요 이벤트 버스 플랫폼 비교

| 플랫폼 | 유형 | 처리량 | 보존 기간 | 주요 특징 |
|:---|:---|:---|:---|:---|
| Apache Kafka | 분산 이벤트 스트리밍 | 수백만 건/초 | 설정 가능 (무기한) | 고처리량, 재처리 용이 |
| AWS EventBridge | 관리형 서버리스 버스 | 중간 | 제한적 | AWS 서비스 통합, 규칙 기반 라우팅 |
| Google Pub/Sub | 관리형 메시지 서비스 | 높음 | 7일 기본 | GCP 생태계 통합 |
| Azure Service Bus | 엔터프라이즈 메시지 버스 | 중간 | 14일 | 트랜잭션 지원, 세션 기반 순서 |
| RabbitMQ | AMQP 메시지 브로커 | 수만 건/초 | 소비 시 삭제 | 복잡한 라우팅, 경량 |
| NATS | 고성능 메시지 시스템 | 수백만 건/초 | 제한적 | 초저지연, IoT 적합 |

### 스트림 프로세싱 핵심 개념

```
[스트림 처리 주요 개념]

1. 이벤트 타임 vs 처리 타임
   이벤트 타임: 이벤트가 실제 발생한 시각
   처리 타임: 시스템이 이벤트를 받은 시각
   (네트워크 지연으로 두 시간이 다를 수 있음)

2. 워터마크 (Watermark)
   "이 시점까지의 모든 이벤트가 도착했다"고 선언
   늦게 도착하는 이벤트(Late Data) 처리 기준

3. 윈도우 처리 (Window Processing)
   - 텀블링 윈도우: 5분 단위, 겹치지 않음
   - 슬라이딩 윈도우: 매 1분마다 5분 집계
   - 세션 윈도우: 사용자 비활성 기준

4. 상태 유지 처리 (Stateful Processing)
   - 이전 이벤트를 기억하며 현재 처리에 활용
   - 사용자별 누적 구매금액 계산 등
```

### 스트림 프로세싱 엔진 비교

| 엔진 | 처리 모델 | 상태 관리 | 지연(Latency) | 적합 사용처 |
|:---|:---|:---|:---|:---|
| Apache Flink | 순수 스트리밍 | 강력 (RocksDB) | 밀리초 수준 | 복잡한 CEP, 이상 탐지 |
| Kafka Streams | Kafka 기반 스트리밍 | 내장 (RocksDB) | 낮음 | Kafka 생태계 내 처리 |
| Apache Spark Streaming | 마이크로 배치 | 중간 | 수 초 | 대용량 배치+스트림 혼용 |
| Apache Storm | 순수 스트리밍 | 제한적 | 매우 낮음 | 레거시 시스템 |
| AWS Kinesis | 관리형 스트리밍 | 제한적 | 낮음 | AWS 생태계 통합 |

### 실시간 스트림 처리 파이프라인 예시



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">사기 탐지 스트림 파이프라인</div></div>
<div class="kb-diagram-note">카드 결제 이벤트 소스</div>
<div class="kb-diagram-note">↓ (Kafka Topic: payment-events)</div>
<div class="kb-diagram-note">Flink 스트림 처리</div>
<div class="kb-diagram-tree-item" style="--depth:2">사용자별 1분 내 결제 횟수 집계</div>
<div class="kb-diagram-tree-item" style="--depth:2">평소 대비 이상 패턴 감지</div>
<div class="kb-diagram-tree-item" style="--depth:2">지역 이상 감지 (해외 + 국내 동시 결제)</div>
<div class="kb-diagram-tree-item" style="--depth:2">금액 이상 감지 (평균 대비 10배 초과)</div>
<div class="kb-diagram-note">↓ (이상 감지 시)</div>
<div class="kb-diagram-note">알림 이벤트 발행 (alert-events)</div>
<div class="kb-diagram-tree-item" style="--depth:2">SMS 발송 서비스</div>
<div class="kb-diagram-tree-item" style="--depth:2">카드 일시 정지 서비스</div>
<div class="kb-diagram-tree-item" style="--depth:2">부정 거래 분석팀 알림</div>
</div>
</div>



- **📢 섹션 요약 비유**: 방송국(이벤트 버스)이 뉴스를 여러 채널에 동시 송출하고, 각 채널의 편집팀(스트림 프로세서)이 실시간으로 자막을 달고, 시청률을 집계하고, 음란물을 필터링한다. 방송 자체와 방송 처리는 별도의 역할이다.

---

## Ⅲ. 비교 및 연결

### 이벤트 버스 vs 스트림 프로세서 심층 비교

| 비교 항목 | 이벤트 버스 | 스트림 프로세서 |
|:---|:---|:---|
| 주요 목적 | 이벤트 라우팅 및 전달 | 이벤트 변환·집계·분석 |
| 처리 방식 | 단순 전달 (Store-and-Forward) | 변환 로직 적용 |
| 상태 관리 | 없음 (무상태) | 있음 (이전 이벤트 기억) |
| 출력 | 동일 이벤트 전달 | 새로운 집계 결과 또는 이벤트 |
| 대표 도구 | Kafka (Topic), EventBridge | Flink, Kafka Streams |
| 지연 | 매우 낮음 | 낮음~중간 (처리 복잡도에 의존) |

### 배치 처리 vs 스트림 처리

| 비교 항목 | 배치 처리 | 스트림 처리 |
|:---|:---|:---|
| 처리 시점 | 특정 시간(매일 자정) | 이벤트 발생 즉시 |
| 데이터 범위 | 한정된 데이터셋 | 무한한 데이터 스트림 |
| 레이턴시 | 시간~일 단위 | 밀리초~초 단위 |
| 복잡도 | 낮음 | 높음 (늦은 데이터, 상태 관리) |
| 적합 사용처 | 일별 리포트, 대용량 ETL | 사기 탐지, 실시간 추천 |

### Kafka의 이중 역할 (이벤트 버스 + 스트림 처리)

Apache Kafka는 이벤트 버스와 스트림 프로세서 역할을 모두 수행한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">Kafka 생태계</div></div>
<div class="kb-diagram-note">Kafka Producer → Kafka Topic (이벤트 버스) → Kafka Consumer</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Kafka Streams API (스트림 처리)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">결과를 다시 Kafka Topic으로 발행</div>
</div>
</div>



- **📢 섹션 요약 비유**: 물길(이벤트 버스)이 물을 흘려보내고, 수력발전소(스트림 프로세서)가 흐르는 물에서 전기(분석 결과)를 생산한다. 물길과 발전소는 다른 역할이지만 함께 작동한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 스트림 처리 설계 시 핵심 고려사항

```
[스트림 처리 설계 체크포인트]

1. 지연 허용 범위 결정
   - 100ms 이하: Flink (순수 스트리밍)
   - 수 초 허용: Spark Streaming (마이크로 배치)
   - 분 단위 허용: 배치 처리 고려

2. 상태(State) 크기 추정
   - 사용자별 집계 = 사용자 수 × 상태 크기
   - RocksDB 상태 저장소 용량 계획

3. 늦게 도착하는 이벤트 처리 전략
   - 워터마크 지연 설정 (e.g., 5분 허용)
   - 늦은 이벤트 무시 또는 별도 처리

4. 백프레셔 (Backpressure) 관리
   - 소비자가 처리하는 속도보다 빠르게 이벤트 발생 시
   - Kafka 파티션 증가로 병렬 처리 확장

5. 체크포인팅 (Checkpointing)
   - 스트림 처리 실패 시 마지막 체크포인트부터 재처리
   - 정확히 한 번(Exactly-once) 처리 보장
```

### 설계 판단 체크리스트

1. **이벤트 버스 선택 기준**: 처리량(Throughput), 메시지 보존 요구사항, 클라우드 생태계 통합 여부를 고려했는가?
2. **스트림 처리 엔진 선택**: 요구되는 레이턴시, 상태 관리 복잡도, 팀의 기술 역량을 평가했는가?
3. **윈도우 처리 설계**: 시간 기반 집계(tumbling/sliding/session window)가 비즈니스 요구사항을 올바르게 반영하는가?
4. **늦은 데이터 처리**: 네트워크 지연으로 늦게 도착한 이벤트를 어떻게 처리할지 정의되어 있는가?
5. **체크포인트/복구 전략**: 스트림 프로세서 장애 시 정확히 어느 지점부터 재처리할 것인지 설계되어 있는가?
6. **이벤트 스키마 관리**: Schema Registry를 통해 이벤트 스키마 버전이 중앙 관리되고 있는가?
7. **백프레셔 대응**: 이벤트 폭증 시 소비자가 과부하 없이 처리할 수 있는 메커니즘이 있는가?

### 안티패턴

- **이벤트 버스를 단순 API 대체재로 사용**: 이벤트 버스를 HTTP 호출 대신 요청-응답(Request-Reply) 패턴으로 사용하면 복잡성만 증가하고 이벤트 기반의 이점이 없다. 즉각적 응답이 필요한 경우 REST/gRPC를 사용해야 한다.
- **상태 없는 스트림 처리에 과도한 외부 저장소 조회**: 이벤트마다 데이터베이스를 조회하면 스트림 처리의 실시간성이 사라지고 DB가 병목이 된다. 상태를 스트림 프로세서 내 상태 저장소(RocksDB)에 캐싱해야 한다.
- **잘못된 이벤트 타임 기준**: 이벤트 발생 시각(event time)이 아닌 처리 시각(processing time)을 기준으로 윈도우를 계산하면, 네트워크 지연으로 늦게 도착한 이벤트가 잘못된 윈도우에 집계된다. 항상 이벤트 타임 기준 처리를 기본으로 해야 한다.

- **📢 섹션 요약 비유**: 물이 흐르는 동안 그 속도와 양을 잘못 측정하면 발전 효율이 떨어지듯, 이벤트 시간 기준 처리와 상태 관리 설계를 잘못하면 스트림 처리의 정확도가 크게 저하된다.

---

## Ⅴ. 기대효과 및 결론

이벤트 버스와 스트림 프로세싱의 조합은 현대 데이터 집약적 시스템의 표준 아키텍처로 자리잡았다. Netflix는 Kafka를 이벤트 버스로, Flink를 스트림 처리 엔진으로 사용하여 실시간 사용자 행동 분석과 개인화 추천을 구현한다. LinkedIn은 Kafka를 오픈소스로 공개한 원래 회사로, 내부적으로 하루 수조 건의 이벤트를 처리한다.

**정량적 효과**: Kafka + Flink 조합은 수십억 건의 이벤트를 수 ms 지연으로 처리하며, 배치 처리 대비 수십~수백 배 빠른 인사이트 도출이 가능하다. 사기 탐지의 경우 배치 처리(하루 뒤 탐지)에서 실시간 탐지(수 초 내)로의 전환이 피해 규모를 극적으로 줄인다.

결론적으로, 이벤트 버스는 마이크로서비스 간 느슨한 결합과 이벤트 전달을 담당하고, 스트림 프로세서는 흐르는 이벤트에서 실시간 가치를 추출한다. 이 둘은 서로를 보완하는 인프라 계층으로, 현대 데이터 아키텍처의 필수 구성 요소다.

- **📢 섹션 요약 비유**: 이벤트 버스(방송 네트워크)와 스트림 프로세서(방송 분석 센터)가 함께 있어야 실시간으로 소식을 전하면서 동시에 그 소식의 의미를 즉각 분석할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 이벤트 기반 아키텍처 (538) | 이벤트 버스와 스트림 처리는 EDA의 핵심 인프라 |
| 서비스 간 비동기 통신 (536) | 이벤트 버스는 비동기 통신의 핵심 인프라 |
| CQRS (554) | 스트림 처리로 읽기 모델(Read Model)을 실시간 갱신 |
| 이벤트 소싱 (555) | 이벤트 스트림을 재처리하여 다양한 뷰 생성 |
| 분산 추적 (569) | 스트림 처리 파이프라인의 이벤트 흐름 추적 |
| 관측성 아키텍처 (566) | 스트림 처리를 통한 실시간 메트릭 집계 |
| 로그 분산 수집 (568) | 로그도 이벤트 스트림으로 처리 가능 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Enterprise Service Bus (ESB) - 기업 통합 버스 (2000년대)</div>
<div class="kb-diagram-note">(중앙화된 통합 허브, 무거운 XML 처리)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Apache Kafka 오픈소스 공개 (LinkedIn, 2011)</div>
<div class="kb-diagram-note">(이벤트 스트리밍 플랫폼의 사실상 표준)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Apache Flink 등장 (2011, ASF 2014)</div>
<div class="kb-diagram-note">(순수 스트리밍 처리, 정확히 한 번 보장)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Kafka Streams API 추가 (2016)</div>
<div class="kb-diagram-note">(Kafka 생태계 내 경량 스트림 처리)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">클라우드 관리형 이벤트 버스 확산</div>
<div class="kb-diagram-note">(AWS EventBridge, GCP Pub/Sub, Azure Event Hubs)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">실시간 AI/ML 추론 파이프라인 통합</div>
<div class="kb-diagram-note">(스트림 처리 + 온라인 ML 모델)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">데이터 메시 (Data Mesh) 패러다임</div>
<div class="kb-diagram-note">(이벤트 버스를 통한 도메인별 데이터 제품 발행)</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 이벤트 버스는 방송국처럼 소식(이벤트)을 여러 채널(서비스)에 동시에 전달하고, 스트림 프로세서는 그 방송을 보면서 실시간으로 자막을 달고 통계를 내는 역할이에요.
2. 방송국이 없으면 각자 따로 전화해야 하고, 분석 팀이 없으면 방송이 나와도 그냥 지나쳐 버려요 - 둘 다 있어야 실시간 정보가 의미 있어져요.
3. 강물(이벤트 흐름)이 흐르는 동안 그 속에서 물고기(유용한 정보)를 잡으려면 올바른 그물(스트림 처리 로직)과 좋은 강(이벤트 버스)이 필요해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 669 / 973

← **이전**: [538. 이벤트 기반 아키텍처 (EDA) - 이벤트 생산자, 브로커, 소비자](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/538_event_driven_architecture_eda/)
**다음**: [539. 이벤트 버스 (Event Bus) 및 스트림 프로세싱](/knowledge-base/studynote/04_software_engineering/11_testing_validation/539_event_bus_stream_processing/) →

---
