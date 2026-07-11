---
title: "메시지 큐 — RabbitMQ·ActiveMQ (Message Queue)"
date: "2026-07-11"
tags:
  - "cspe-software"
weight: 206
extra:
  question_no: "206"
  exam_status: "미출제"
---

## 미리 알고가기

- 메시지 큐는 생산자와 소비자의 실행 시점·처리 속도를 분리하고 Broker가 메시지를 라우팅·보관·전달하는 구조임
- Publisher Confirm은 생산자에서 Broker까지, Consumer Acknowledgement는 Broker에서 소비자 처리까지를 각각 확인함
- At-Least-Once 전달에서는 장애 후 메시지가 다시 전달될 수 있으므로 소비자는 업무 키로 중복 효과를 제거해야 함
- RabbitMQ는 Exchange·Binding·Queue, ActiveMQ Artemis는 Address·Routing Type·Queue를 중심으로 라우팅함
- Retry 횟수·지연·Dead Letter Queue와 메시지 만료를 정하지 않으면 실패 메시지가 정상 처리량을 잠식할 수 있음

## 작성 근거(검토용)

- 메시지 큐는 비동기 분리, 라우팅, 영속성, 확인, 재전달·중복, 흐름 제어, 실패 격리를 핵심 축으로 설명함
- 비교표는 RabbitMQ와 ActiveMQ Artemis의 라우팅·프로토콜·확인·복제·연동·적합 조건을 대비함
- 주문 후처리와 Java 업무 연계는 미라우팅 건수·재전달률·큐 적체·Failover 시간으로 검증함

## Ⅰ. 개요

- **정의/개념**: 메시지 큐는 생산자가 Broker에 메시지를 발행하고 Broker가 라우팅·저장한 뒤 소비자가 비동기로 처리·확인하는 응용 간 완충·전달 구조임
- **배경/필요성**: 호출 대상의 일시 장애와 처리 속도 차이가 요청 서비스의 응답·가용성에 직접 전파되지 않도록 전달 상태·재시도·적체를 별도 계층에서 관리해야 함

## Ⅱ. 특징

- Exchange·Address 규칙이 Routing Key·Anycast·Multicast에 따라 하나 이상의 Queue로 메시지를 배치함
- Durable 토폴로지와 Persistent 메시지·복제 Queue가 Broker 재시작과 노드 장애 후 전달 데이터를 복구함
- 생산자 확인과 소비자 수동 확인을 분리해 저장 성공과 업무 처리 성공의 경계를 각각 기록함
- Consumer Prefetch·Credit·Queue 한도로 미확인 메시지와 생산 속도를 제한해 소비자 메모리·적체를 통제함
- Negative Acknowledgement·재전달·지연 Retry·Dead Letter Queue로 실패 메시지를 정상 Queue에서 분리함
- 중복 전달·순서 변경·Poison Message를 고려해 소비자 멱등 키와 최대 재시도 횟수를 설계함

## Ⅲ. 종류 및 비교

| 판단 기준 | RabbitMQ | ActiveMQ Artemis |
|:---|:---|:---|
| 라우팅 구조 | Exchange Type·Binding·Routing Key -> Queue | Address·Anycast/Multicast Routing Type -> Queue |
| 주요 프로토콜 | AMQP 0-9-1과 플러그인 프로토콜 | Core·AMQP·OpenWire·MQTT·STOMP |
| 소비 API | Channel·Consumer·Ack·Prefetch | Core API·JMS/Jakarta Messaging·Consumer Credit |
| 전달 확인 | Publisher Confirm과 Consumer Ack | Send 보장·Transaction과 Consumer Ack |
| 고가용성 | Quorum Queue의 복제 로그·리더 | 공유 저장소·복제·Mirroring 기반 Failover |
| 연동 중심 | Exchange 기반 세밀한 Routing과 작업 Queue | Java/JMS 계약과 다중 프로토콜 Broker 연동 |
| 적합 조건 | Topic·Direct·Fanout 라우팅과 비동기 작업 분배 | JMS·XA·기존 ActiveMQ Client와 시스템 통합 |

> 요약: RabbitMQ는 Exchange·Binding 라우팅을, ActiveMQ Artemis는 Address·Routing Type과 JMS·다중 프로토콜 연동을 중심으로 구성함.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Producer·Publisher | 메시지·Routing Key·Header·영속성 속성을 Broker에 전달함 |
| Exchange·Address | Binding 또는 Routing Type에 따라 메시지 목적지를 선택함 |
| Queue·Persistence | 소비 전 메시지와 전달 상태를 메모리·저장소·복제본에 유지함 |
| Consumer·Acknowledgement | 메시지를 처리하고 성공·실패·재전달 여부를 Broker에 알림 |
| Retry·DLQ·Expiry | 실패 횟수·재시도 지연·격리 Queue·만료 기준을 적용함 |
| Cluster·Federation·Bridge | Broker 장애 복구와 Broker·데이터센터 사이 메시지 이동을 담당함 |

```text
Producer -> Exchange|Address -> Queue -> Consumer -> Ack
                unroutable       └-> Retry -> DLQ
```

> 요약: Broker는 라우팅 결과를 Queue에 저장하고 Consumer 확인 전까지 전달 상태를 유지하며 반복 실패를 DLQ로 격리함.

## Ⅴ. 원리 및 절차 흐름도

```text
메시지 발행 -> 라우팅·저장 -> 생산자 확인 -> 소비자 전달 -> 처리 확인 -> 삭제·재전달·DLQ
```

1. **메시지 발행**: 생산자가 목적지·Routing Key·업무 식별자와 Payload를 전송함
2. **라우팅·저장**: Broker가 Binding·Routing Type을 평가해 Queue에 메시지를 기록함
3. **생산자 확인**: 저장·복제 정책을 충족하면 Confirm 또는 Send 결과를 생산자에게 반환함
4. **소비자 전달**: Credit·Prefetch 범위에서 대기 메시지를 소비자에게 배분함
5. **처리 확인**: 성공은 Ack 후 삭제하고 실패는 정책에 따라 재전달·지연 Retry·DLQ로 이동함

> 요약: 메시지는 Broker 저장과 소비자 업무 처리에서 각각 확인되며 실패 횟수에 따라 재전달 또는 DLQ로 전이됨.

## Ⅵ. 실무 사례

1. 주문 후처리는 RabbitMQ Topic·Quorum Queue·Confirm을 적용하고 미라우팅 건수·재전달률을 확인함
2. Java 업무 연계는 Artemis JMS·DLQ·Failover를 적용하고 Queue 적체량·복구 시간을 확인함

## Ⅶ. 결론

- 메시지 큐는 라우팅 계약·저장 확인·소비 확인·멱등 처리·적체 한도·실패 격리를 하나의 전달 정책으로 설계해야 함
