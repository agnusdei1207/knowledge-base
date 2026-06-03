---
title: 196. 커맨드 패턴 (Command Pattern)
date: '2026-05-10'
tags:
- studynote-design-supervision
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[271_command_pattern|커맨드]] 패턴 ([[271_command_pattern|Command Pattern]])은 GoF 행위 패턴으로, 요청(Request)을 독립적인 [[271_command_pattern|커맨드]] 객체([[271_command_pattern|Command]] Object)로 캡슐화하여, 요청을 큐에 저장하거나, 로깅하거나, 되돌리기([[393_undo|Undo]])·재실행([[234_redo_roll_forward_durability_recovery|Redo]])할 수 있게 하는 패턴이다.
> 2. **가치**: 요청의 발신자(Invoker)와 수신자(Receiver)를 분리하여 결합도를 낮추고, 요청을 객체로 표현하여 '실행 취소', '재실행', '[[191_transaction_concept_states|트랜잭션]] 큐', '작업 [[568_logs_distributed_logging_elk_fluentd|로그]]' 등의 고급 기능을 쉽게 구현한다.
> 3. **판단 포인트**: [[271_command_pattern|커맨드]] 패턴의 핵심 가치는 [[393_undo|Undo]]/[[234_redo_roll_forward_durability_recovery|Redo]] 구현이다. 각 [[271_command_pattern|커맨드]]가 `execute()`와 `undo()` 메서드를 갖고, 실행 [[057_stack|스택]]에 [[271_command_pattern|커맨드]]를 저장하면 실행 취소 기능을 체계적으로 구현할 수 있다. [[306_cqrs|CQRS]] 패턴에서 [[271_command_pattern|Command]] 객체가 [[271_command_pattern|커맨드]] 패턴의 아키텍처 수준 확장이다.

---

## Ⅰ. 개요 및 필요성

GUI 애플리케이션에서 버튼 클릭, 메뉴 선택, 키보드 단축키 등 다양한 방법으로 동일한 동작(예: 저장)을 실행할 수 있다. 이를 직접 구현하면 동일한 저장 로직이 여러 곳에 중복된다. [[271_command_pattern|커맨드]] 패턴은 '저장' 동작을 `SaveCommand` 객체로 캡슐화하여 어디서든 동일한 [[271_command_pattern|커맨드]]를 실행한다.

실세계 예시: ① 텍스트 에디터의 Ctrl+Z ([[393_undo|Undo]] [[057_stack|스택]]), ② 주식 거래 시스템의 주문 큐, ③ 게임의 플레이 녹화·재생, ④ [[136_variance|분산]] [[191_transaction_concept_states|트랜잭션]]에서 [[551_compensating_transaction_logical_rollback|보상 트랜잭션]]([[551_compensating_transaction_logical_rollback|Compensating Transaction]]).

```text
┌─────────────────────────────────────────────────────────────┐
│              커맨드 패턴 구조                                 │
├─────────────────────────────────────────────────────────────┤
│  Client → Command (인터페이스)                              │
│           + execute(): void                                 │
│           + undo(): void                                    │
│                ▲                                            │
│           ConcreteCommand                                   │
│           - receiver: Receiver                              │
│           + execute(): void { receiver.action(); }         │
│           + undo(): void { receiver.undoAction(); }        │
│                                                             │
│  Invoker (실행자)          Receiver (수신자)                 │
│  - command: Command        + action(): void                 │
│  + setCommand(cmd)         + undoAction(): void             │
│  + invoke(): command.execute()                              │
└─────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 레스토랑에서 웨이터(Invoker)가 주문서([[271_command_pattern|Command]] 객체)를 받아 주방(Receiver)에 전달한다. 주문서에는 주문 내용(execute)과 취소 방법([[393_undo|undo]])이 기록되어 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[393_undo|Undo]]/[[234_redo_roll_forward_durability_recovery|Redo]] 구현: 실행된 [[271_command_pattern|커맨드]]를 [[057_stack|스택]](undoStack)에 쌓고, [[393_undo|Undo]] 시 [[057_stack|스택]]에서 [[271_command_pattern|커맨드]]를 꺼내 `undo()`를 호출하며 redoStack에 이동한다. [[234_redo_roll_forward_durability_recovery|Redo]] 시 redoStack에서 꺼내 `execute()`를 다시 호출한다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 기본 실행 | [[271_command_pattern|command]].execute() 호출 | 버튼 클릭, 메뉴 선택 |
| [[393_undo|Undo]] [[057_stack|스택]] | 실행 [[271_command_pattern|커맨드]]를 [[057_stack|스택]]에 저장 | Ctrl+Z |
| 매크로 [[271_command_pattern|커맨드]] | 여러 [[271_command_pattern|커맨드]]를 하나로 묶음 | 복합 작업 |
| [[015_지연_데이터_관점|지연]] 실행 | [[271_command_pattern|커맨드]]를 큐에 저장 후 나중에 실행 | [[191_transaction_concept_states|트랜잭션]] 큐 |

```text
┌─────────────────────────────────────────────────────────────┐
│       Undo/Redo 스택 동작                                   │
├─────────────────────────────────────────────────────────────┤
│  execute(MoveCmd): undoStack=[MoveCmd], redoStack=[]        │
│  execute(ResizeCmd): undoStack=[MoveCmd, ResizeCmd]         │
│                                                             │
│  Undo: undoStack에서 ResizeCmd 꺼내 undo()                  │
│        redoStack=[ResizeCmd], undoStack=[MoveCmd]           │
│                                                             │
│  Redo: redoStack에서 ResizeCmd 꺼내 execute()               │
│        undoStack=[MoveCmd, ResizeCmd], redoStack=[]         │
└─────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 요리 레시피([[271_command_pattern|커맨드]] [[057_stack|스택]])에서 잘못된 단계를 되돌리려면 역순으로 취소([[393_undo|undo]])하면 된다. 레시피에 각 단계의 취소 방법이 기록되어 있어야 한다.

---
## Ⅲ. 비교 및 연결

[[306_cqrs|CQRS]]([[271_command_pattern|Command]] Query Responsibility Segregation)와 [[271_command_pattern|커맨드]] 패턴의 [[083_relationship_in_er_model|관계]]: CQRS의 '[[271_command_pattern|Command]]'는 [[271_command_pattern|커맨드]] 패턴의 아키텍처 수준 확장이다. CQRS에서 [[271_command_pattern|Command]] 객체는 시스템 상태를 변경하는 요청을 표현하고, [[271_command_pattern|Command]] Handler가 Receiver 역할을 한다.

| 비교 축 | A | B |
|:---|:---|:---|
| 수준 | 객체 수준 | 아키텍처 수준 |
| 핵심 | [[393_undo|Undo]]/[[234_redo_roll_forward_durability_recovery|Redo]], 큐 | [[289_cqrs_db|쓰기]] 모델 분리 |
| 통신 | 인프로세스 | 메시지 [[344_bus|버스]] ([[179_kafka_flink_watermark_time_window|Kafka]] 등) |
| 적용 범위 | 단일 앱 내 | [[136_variance|분산]] 시스템 |

- **📢 섹션 요약 비유**: [[271_command_pattern|커맨드]] 패턴은 레스토랑 주문서(단일 앱), CQRS는 주문 관리 시스템([[136_variance|분산]] 아키텍처)이다. 둘 다 '요청을 객체로 캡슐화'하는 원칙을 공유한다.

---
## Ⅳ. 실무 적용 및 기술사 판단

스프링 MVC에서 `@RequestMapping` 핸들러가 Invoker, Controller 메서드가 ConcreteCommand 역할을 한다. 스프링 배치(Spring Batch)의 `Step` 인터페이스도 [[271_command_pattern|커맨드]] 패턴을 구현하여 배치 단계의 실행·건너뛰기·재시작을 지원한다.

### 판단 [[435_checklist_based_testing|체크리스트]]
1. [[271_command_pattern|커맨드]] 객체가 execute()와 [[393_undo|undo]]() 메서드를 구현하여 [[393_undo|Undo]] 기능을 지원하는가?
2. 실행자(Invoker)와 수신자(Receiver)가 [[271_command_pattern|커맨드]] 인터페이스로 분리되어 있는가?
3. 실행 [[057_stack|스택]](undoStack/redoStack)이 올바르게 관리되어 [[393_undo|Undo]]/Redo가 동작하는가?
4. 매크로 [[271_command_pattern|커맨드]](CompositeCommand)로 복합 작업을 원자적으로 실행할 수 있는가?
5. [[306_cqrs|CQRS]] 패턴을 적용할 때 [[271_command_pattern|Command]] 객체가 [[271_command_pattern|커맨드]] 패턴의 원칙을 따르는가?

- **📢 섹션 요약 비유**: 주문서([[271_command_pattern|커맨드]] 객체)는 주문 내용(execute)과 취소 방법([[393_undo|undo]])을 담아, 웨이터(Invoker)가 주방(Receiver)에 전달하거나 필요 시 취소할 수 있게 한다.

---

## Ⅴ. 기대효과 및 결론

[[271_command_pattern|커맨드]] 패턴을 적용하면 요청 발신자와 수신자의 결합도가 낮아지고, [[393_undo|Undo]]/[[234_redo_roll_forward_durability_recovery|Redo]]·작업 큐·로깅·[[191_transaction_concept_states|트랜잭션]] 등의 고급 기능을 체계적으로 구현할 수 있다. [[306_cqrs|CQRS]]·[[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]]과 결합하면 [[136_variance|분산]] 시스템에서도 강력한 명령 처리 아키텍처를 달성한다.

한계는 [[271_command_pattern|커맨드]] 클래스 수가 많아지면 관리 복잡성이 증가하고, [[393_undo|Undo]] 구현 시 상태 복원이 복잡한 경우 [[274_memento_pattern|메멘토]]([[274_memento_pattern|Memento]]) 패턴과 함께 사용해야 한다.

- **📢 섹션 요약 비유**: [[271_command_pattern|커맨드]] 패턴은 체스 기보처럼, 모든 수([[271_command_pattern|커맨드]])를 기록하면 어느 시점으로든 되돌리거나([[393_undo|Undo]]), 재현할 수 있다([[234_redo_roll_forward_durability_recovery|Redo]]).

---

### 📌 관련 개념 맵

[요청 캡슐화] → [커맨드 패턴] → [[[393_undo|Undo]]/[[234_redo_roll_forward_durability_recovery|Redo]] 스택] → [[[306_cqrs|CQRS]] [[271_command_pattern|Command]]] → [이벤트 소싱 통합]

| 개념 | 연결 포인트 |
|:---|:---|
| [[306_cqrs|CQRS]] | [[271_command_pattern|커맨드]] 패턴의 아키텍처 수준 확장 |
| [[398_process|메멘토 패턴]] | 복잡한 Undo를 위한 상태 [[022_snapshot_backup_architecture|스냅샷]] 저장 |
| [[191_transaction_concept_states|트랜잭션]] | [[271_command_pattern|커맨드]] 객체로 원자적 작업 표현 |
| [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] | [[271_command_pattern|커맨드]] 실행 결과를 이벤트로 저장 |

### 📈 관련 키워드 및 발전 흐름도

[GoF [[271_command_pattern|Command]](1994)] → [GUI [[393_undo|Undo]]/[[234_redo_roll_forward_durability_recovery|Redo]]] → [[[306_cqrs|CQRS]] [[271_command_pattern|Command]] 객체] → [이벤트 소싱 통합] → [분산 보상 트랜잭션]

### 👶 어린이를 위한 3줄 비유 설명

1. [[271_command_pattern|커맨드]] 패턴은 주문서처럼, 요청을 객체로 만들어 나중에 실행하거나 취소([[393_undo|Undo]])할 수 있어요.
2. Ctrl+Z(되돌리기)가 바로 이 패턴을 사용해요.
3. CQRS에서 [[271_command_pattern|Command]] 객체도 이 패턴의 아키텍처 버전이에요!
