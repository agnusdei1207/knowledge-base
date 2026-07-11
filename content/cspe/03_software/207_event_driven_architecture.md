---
title: "이벤트 기반 아키텍처 (Event-Driven Architecture)"
date: "2026-07-11"
tags:
  - "cspe-software"
weight: 207
extra:
  question_no: "207"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- 이벤트는 소프트웨어에서 이미 발생한 상태 변화·사실과 그 문맥을 기록한 데이터임
- 생산자는 소비자를 지정하지 않고 Event Type·Source·ID·Schema에 따라 Broker·Router에 이벤트를 발행함
- 소비자는 독립적으로 구독·처리하므로 시간 결합은 줄지만 결과는 비동기로 반영되고 중복·순서 역전이 발생할 수 있음
- DB 변경과 이벤트 발행의 원자성은 Transactional Outbox·CDC로 연결하고 소비자는 Event ID·업무 키로 멱등 처리함
- 이벤트 계약은 의미·Schema·순서·호환성·개인정보 범위를 포함하며 Payload 형식만 맞는다고 호환되는 것은 아님

## 작성 근거(검토용)

- 이벤트 기반 아키텍처는 생산·라우팅·구독, 계약, 비동기 일관성, 멱등성, 재시도·재생, 추적성을 핵심 축으로 설명함
- 비교표는 알림·상태 전달·이벤트 소싱의 Payload·소비자 조회·원본·재생·결합·적합 조건을 대비함
- 주문 이벤트와 검색 색인은 발행 지연·중복 효과율·소비 지연·재생 복구 시간으로 검증함

## Ⅰ. 개요

- **정의/개념**: 이벤트 기반 아키텍처는 생산자가 발생 사실을 이벤트로 발행하고 Router·Broker가 관심 소비자에게 전달해 각 소비자가 상태와 후속 동작을 비동기로 갱신하는 구조임
- **배경/필요성**: 서비스 간 직접 호출의 가용성·배포·처리 속도 결합을 줄이고 하나의 상태 변화에 여러 후속 기능을 독립 추가하기 위해 이벤트 계약과 전달 계층이 필요함

## Ⅱ. 특징

- 생산자·소비자는 Event Type·Schema·Topic 계약으로 연결되고 서로의 주소·실행 시점은 알지 않아도 됨
- Broker가 Filter·Partition·Subscription에 따라 이벤트를 복제·분배하고 Offset·Ack로 소비 위치를 관리함
- 결과가 여러 소비자에 시간차로 반영되므로 사용자 응답·재조회·보상 흐름에 수렴 시간을 명시함
- At-Least-Once 재전달과 소비자 재시작에 대비해 Event ID·업무 키·처리 이력으로 부수 효과를 멱등화함
- Schema Registry·호환성 검사·폐기 정책으로 Event Type과 필드 의미를 생산자·소비자 배포 사이에 유지함
- Correlation ID·Causation ID·Trace Context와 DLQ·재생 기록으로 비동기 처리 경로와 실패 원인을 추적함

## Ⅲ. 종류 및 비교

| 판단 기준 | Event Notification | Event-Carried State Transfer | Event Sourcing |
|:---|:---|:---|:---|
| Payload 범위 | 발생 사실과 자원 식별자 | 소비에 필요한 변경 상태·Snapshot | 상태를 만든 업무 사건 전체 |
| 소비자 추가 조회 | 최신 상세 상태를 생산자 API에서 조회 | 자체 저장소를 Payload로 갱신 | 이벤트를 순서대로 적용해 상태 구성 |
| 원본 데이터 | 생산자 DB가 현재 상태의 원본 | 생산자 상태와 소비자 복제본 병행 | Event Store가 상태 이력의 원본 |
| 재생 목적 | 후속 동작 재시도 | 소비자 Projection 재구성 | Aggregate 상태·Projection 재구성 |
| 결합 지점 | 생산자 조회 API·가용성 | Event Schema·상태 중복 | 사건 순서·버전·재생 규칙 |
| 적합 조건 | 이벤트 후 최신 원본 조회 필요 | 소비자 독립 조회·로컬 Projection 필요 | 감사 이력·시점 복원·재계산 필요 |

> 요약: 알림은 발생 사실, 상태 전달은 소비용 데이터, 이벤트 소싱은 상태를 만든 사건 이력을 이벤트로 제공함.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Event Producer·Outbox | 업무 트랜잭션과 발행 대상을 같은 저장 경계에 기록함 |
| Relay·CDC | Outbox·변경 로그를 읽어 Broker에 발행하고 전송 위치를 관리함 |
| Broker·Router | Topic·Filter·Partition으로 이벤트를 Subscription에 전달함 |
| Schema Registry·Contract | Event Type·필드·호환성·보존·개인정보 규칙을 관리함 |
| Consumer·Projection | 이벤트를 멱등 처리하고 자체 상태·후속 동작을 갱신함 |
| Retry·DLQ·Replay·Trace | 실패 격리·재처리·상태 재구성과 인과 경로 추적을 지원함 |

```text
Domain Transaction -> Outbox -> Relay/CDC -> Broker -> Consumer -> Projection
                                             └-> Retry·DLQ·Replay
```

> 요약: Outbox·CDC가 업무 상태와 이벤트 발행을 연결하고 Broker가 계약별 소비자에 전달해 Projection을 갱신함.

## Ⅴ. 원리 및 절차 흐름도

```text
업무·Outbox 기록 -> 이벤트 발행 -> 계약·라우팅 -> 멱등 소비 -> Ack·Projection -> Retry·DLQ
```

1. **업무·Outbox 기록**: 생산자가 상태 변경과 Event ID·Type·Payload를 한 트랜잭션에 저장함
2. **이벤트 발행**: Relay·CDC가 미발행 레코드를 읽어 Broker에 보내고 발행 위치를 기록함
3. **계약·라우팅**: Broker와 Registry가 Schema·Topic·Partition 규칙에 따라 Subscription에 전달함
4. **멱등 소비**: 소비자가 Event ID·업무 키를 확인하고 중복 부수 효과 없이 업무를 수행함
5. **상태·실패 처리**: 성공은 Offset·Ack와 Projection을 갱신하고 반복 실패는 Retry·DLQ로 격리함

> 요약: 업무 변경과 Outbox를 함께 기록하고 소비자가 계약 검증·멱등 처리 후 Offset과 Projection을 갱신함.

## Ⅵ. 실무 사례

1. 주문 상태 변경은 Outbox·Schema Registry를 적용하고 발행 지연·중복 업무 반영 건수를 확인함
2. 상품 검색 색인은 상태 전달 이벤트로 갱신하고 소비 지연·전체 재생 복구 시간을 확인함

## Ⅶ. 결론

- 이벤트 기반 아키텍처는 이벤트 의미·발행 원자성·멱등성·수렴 시간·재생·추적 기준을 소비자 수명주기와 함께 설계해야 함
