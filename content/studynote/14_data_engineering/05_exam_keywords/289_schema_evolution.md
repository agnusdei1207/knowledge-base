---
title: "Schema Evolution Compatibility Registry"
date: "2026-05-09"
tags:
  - "studynote-data-engineering"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 분산 이벤트 스트리밍 환경(Kafka, Pulsar, Kinesis)에서 Avro·Protocol Buffers·JSON Schema 등의 직렬화 포맷 변경 시, 중앙 **Schema Registry**(주제: `_schemas` 토픽 기반)가 `BACKWARD`·`FORWARD`·`FULL`·`TRANSITIVE` 호환성 매트릭스를 통해 프로듀서-컨슈머 간의 데이터 계약을 자동 검증·버전 관리하는 **데이터 컨트랙트 거버넌스(Schema-as-Contract)**의 핵심 컴포넌트이다.
> 2. **가치**: 스키마 드리프트(Schema Drift) 조기 차단(빌드 시점 100% 검증), 무중단 Blue-Green 배포(확장-수축 패턴 지원), 메시지 손실 0건 유지, 데이터 리니지 자동 추적, 컴플라이언스(GDPR/PCI-DSS) 감사 대응력 강화 — Netflix·LinkedIn·Uber 사례에서 컨슈머 장애 MTTR 평균 70% 단축.
> 3. **판단 포인트**: 호환성 모드(`BACKWARD_TRANSITIVE` vs `FULL_TRANSITIVE`) 선택, Subject 네이밍 전략(`TopicNameStrategy` vs `RecordNameStrategy`), Schema ID 임베딩 방식(Confluent Wire Format의 Magic Byte 0x00 + 4-byte Schema ID), 레지스트리 HA(Leader/Follower Raft consensus), 클라이언트 사이드 캐시 TTL, GitOps/CI 게이트 통합, 그리고 mTLS·RBAC·감사 로그를 통한 4대 보안 요구사항 충족 여부.

---

## Ⅰ. 개요 및 필요성

Kafka·Pulsar·NATS JetStream 등 이벤트 스트리밍 플랫폼이 엔터프라이즈 데이터 아키텍처의 신경망으로 자리 잡으면서, **데이터의 형태(Schema)**는 더 이상 한 애플리케이션이 닫힌 환경에서 관리하는 정적 산출물이 아니라 **수십·수백 개의 프로듀서와 컨슈머가 끊임없이 진화시키는 라이브 계약(Living Contract)**이 되었다. 2014년 LinkedIn이 Confluent Schema Registry를 오픈소스화한 이래, Apache Kafka 생태계의 사실 표준으로 정착했으며 현재는 CNCF Apicurio Registry, AWS Glue Schema Registry, Azure Schema Registry(for Event Hubs), Google Cloud Pub/Sub Schemas, Buf Schema Registry(Protobuf 전용), Karapace(Aiven 포크)로까지 구현체가 분화되었다.

본질적 문제는 **"누가, 어떤 순서로, 어떤 필드를 추가하거나 삭제할 것인가"**라는 단순해 보이는 변경이 **분산 트랜잭션의 정합성을 깨뜨리고 다운스트림 데이터 레이크/데이터 웨어하우스(Snowflake, BigQuery, Iceberg, Delta Lake) 전체의 파이프라인을 망가뜨린다**는 점이다. 실제로 2018년 한 글로벌 e-커머스사는 Black Friday 전야에 `order_event` 토픽의 `total_price` 필드 타입을 `double` -> `long`(센트 단위 정수화)으로 변경하여, 컨슈머가 `ClassCastException`을 던지며 약 4시간 동안 결제 사후 분석 파이프라인이 중단된 사례가 있다. 이는 *implicit* 스키마(코드에 암묵적으로 존재하는 스키마)와 *explicit* 스키마(외부 정의된 스키마) 사이의 **불일치 상태(Inconsistency)**가 운영 리스크로 현실화된 대표적 사례다.

**스키마 진화 호환성 레지스트리 관리**는 이러한 문제를 다음 세 가지 핵심 메커니즘으로 해결한다:
1. **중앙 집중식 버전 카
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 289 / 300

<- **이전**: [288. dbt 데이터 변환 모델링 테스트 문서화 (dbt Data Transformation Modeling Testing)](/studynote/14_data_engineering/05_exam_keywords/288_dbt_transformation/)
**다음**: [290. 파케이 ORC 열 지향 저장 포맷 최적화 (Parquet ORC Columnar Storage Format)](/studynote/14_data_engineering/05_exam_keywords/290_parquet_orc_columnar/) ->

---
