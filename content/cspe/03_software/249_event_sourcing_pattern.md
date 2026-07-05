---
title: "Event Sourcing Pattern (이벤트 소싱)"
date: "2026-07-05"
tags:
  - "cspe-software"
weight: 249
---

## Ⅰ. 개요
- **정의**: 상태 변경을 직접 덮어쓰지 않고, 변경 이벤트를 순서대로 저장하여 현재 상태를 재구성하는 패턴임
- **배경/필요성**: CRUD 방식은 과거 상태를 추적할 수 없으므로, 변경 이력 보존과 상태 복원이 필요한 도메인에 적합한 저장 패턴이 필요함
- **비유**: 은행 통장에 잔액만 기록하는 것이 아니라, 모든 입출금 내역을 순서대로 기록하는 것과 같음

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Event Sourcing 구조와 CQRS 연계 | Event Store, Projection, Replay | CRUD와의 차이를 구조적으로 설명할 것 |

> 요약: 상태가 아닌 이벤트를 저장하여 변경 이력 추적과 상태 복원을 가능하게 하는 패턴임

## Ⅱ. 구성요소
```text
Command --> [Domain Logic] --> Event
                                |
                                v
                          [Event Store]
                                |
                                v
                          [Projection]
                                |
                                v
                          [Read Model]
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Event Store | 이벤트를 발생 순서대로 Append-Only로 저장하는 저장소임 | 회계 원장 |
| Event | 도메인 상태 변경을 표현하는 불변 객체(예: `OrderPlaced`)임 | 거래 전표 |
| Projection | 이벤트를 소비하여 조회용 Read Model을 생성하는 프로세스임 | 월별 결산표 작성 |
| Replay | 이벤트를 처음부터 재생하여 임의 시점의 상태를 복원하는 기능임 | 통장 처음부터 재계산 |

> 요약: Event Store에 이벤트를 저장하고 Projection으로 조회 모델을 생성함

## Ⅲ. 절차
```text
Command 수신 --> Event 생성 --> Event Store 저장 --> Projection 갱신
```
- 1단계: 외부 Command 수신 후 도메인 로직으로 유효성 검증
- 2단계: 상태 변경을 표현하는 Event 객체 생성(예: `ItemAdded`, `OrderPaid`)
- 3단계: Event Store에 Append-Only 방식으로 이벤트 영속화
- 4단계: 이벤트 핸들러가 Projection을 갱신하여 Read Model 최신화

> 요약: Command → Event 생성 → 저장 → Projection 순으로 처리함

## Ⅳ. 문제점
- 이벤트 스키마 진화: 이벤트 구조 변경 시 과거 이벤트와의 호환성 유지가 어려움
- Replay 성능: 이벤트 누적량이 증가하면 전체 Replay 소요 시간이 급증함
- 최종 일관성: Projection 갱신까지 지연이 발생하여 조회 시 최신 상태를 즉시 반영하지 못함

> 요약: 스키마 진화, Replay 성능, 최종 일관성이 주요 과제임

## Ⅴ. 개선방안
1. 단기: 이벤트 버전 관리 및 Upcaster 패턴으로 스키마 호환성 확보
2. 중기: Snapshot을 주기적으로 생성하여 Replay 시작점을 단축
3. 장기: CQRS 패턴 결합으로 읽기/쓰기 모델을 분리하여 일관성·성능을 동시 확보

> 요약: Upcaster, Snapshot, CQRS를 통해 Event Sourcing의 실용성을 높임

## Ⅵ. 전망
- 발전 방향: 감사 추적·규제 준수가 요구되는 금융·의료 도메인에서 채택이 확대될 전망임
- 기술사적 판단: Outbox 패턴(250 참조)과 결합하여 이벤트 발행의 신뢰성을 보장하는 것이 바람직함
- 기술사 제언: 멱등성(248 참조) 설계를 이벤트 소비자에 적용하여 중복 처리 문제를 해결하는 것이 필요함
