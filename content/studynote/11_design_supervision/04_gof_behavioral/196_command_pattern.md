---
title: "196. 커맨드 패턴 (Command Pattern)"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) 패턴 ([Command Pattern](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/))은 GoF 행위 패턴으로, 요청(Request)을 독립적인 [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) 객체([Command](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) Object)로 캡슐화하여, 요청을 큐에 저장하거나, 로깅하거나, 되돌리기([Undo](/studynote/11_design_supervision/06_exam_summary/393_undo/))·재실행([Redo](/studynote/05_database/04_transactions_concurrency/234_redo_roll_forward_durability_recovery/))할 수 있게 하는 패턴이다.
> 2. **가치**: 요청의 발신자(Invoker)와 수신자(Receiver)를 분리하여 결합도를 낮추고, 요청을 객체로 표현하여 '실행 취소', '재실행', '[트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 큐', '작업 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)' 등의 고급 기능을 쉽게 구현한다.
> 3. **판단 포인트**: [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) 패턴의 핵심 가치는 [Undo](/studynote/11_design_supervision/06_exam_summary/393_undo/)/[Redo](/studynote/05_database/04_transactions_concurrency/234_redo_roll_forward_durability_recovery/) 구현이다. 각 [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/)가 `execute()`와 `undo()` 메서드를 갖고, 실행 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)에 [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/)를 저장하면 실행 취소 기능을 체계적으로 구현할 수 있다. [CQRS](/studynote/12_it_management/05_security_compliance/306_cqrs/) 패턴에서 [Command](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) 객체가 [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) 패턴의 아키텍처 수준 확장이다.

---

## Ⅰ. 개요 및 필요성

GUI 애플리케이션에서 버튼 클릭, 메뉴 선택, 키보드 단축키 등 다양한 방법으로 동일한 동작(예: 저장)을 실행할 수 있다. 이를 직접 구현하면 동일한 저장 로직이 여러 곳에 중복된다. [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) 패턴은 '저장' 동작을 `SaveCommand` 객체로 캡슐화하여 어디서든 동일한 [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/)를 실행한다.

실세계 예시: ① 텍스트 에디터의 Ctrl+Z ([Undo](/studynote/11_design_supervision/06_exam_summary/393_undo/) [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)), ② 주식 거래 시스템의 주문 큐, ③ 게임의 플레이 녹화·재생, ④ [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)에서 [보상 트랜잭션](/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/)([Compensating Transaction](/studynote/04_software_engineering/09_cloud_native_ai_architecture/551_compensating_transaction_logical_rollback/)).

```text
+-------------------------------------------------------------+
|              커맨드 패턴 구조                                 |
+-------------------------------------------------------------+
|  Client -> Command (인터페이스)                              |
|           + execute(): void                                 |
|           + undo(): void                                    |
|                ^                                            |
|           ConcreteCommand                                   |
|           - receiver: Receiver                              |
|           + execute(): void { receiver.action(); }         |
|           + undo(): void { receiver.undoAction(); }        |
|                                                             |
|  Invoker (실행자)          Receiver (수신자)                 |
|  - command: Command        + action(): void                 |
|  + setCommand(cmd)         + undoAction(): void             |
|  + invoke(): command.execute()                              |
+-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 레스토랑에서 웨이터(Invoker)가 주문서([Command](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) 객체)를 받아 주방(Receiver)에 전달한다. 주문서에는 주문 내용(execute)과 취소 방법([undo](/studynote/11_design_supervision/06_exam_summary/393_undo/))이 기록되어 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[Undo](/studynote/11_design_supervision/06_exam_summary/393_undo/)/[Redo](/studynote/05_database/04_transactions_concurrency/234_redo_roll_forward_durability_recovery/) 구현: 실행된 [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/)를 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)(undoStack)에 쌓고, [Undo](/studynote/11_design_supervision/06_exam_summary/393_undo/) 시 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)에서 [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/)를 꺼내 `undo()`를 호출하며 redoStack에 이동한다. [Redo](/studynote/05_database/04_transactions_concurrency/234_redo_roll_forward_durability_recovery/) 시 redoStack에서 꺼내 `execute()`를 다시 호출한다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 기본 실행 | [command](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/).execute() 호출 | 버튼 클릭, 메뉴 선택 |
| [Undo](/studynote/11_design_supervision/06_exam_summary/393_undo/) [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) | 실행 [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/)를 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)에 저장 | Ctrl+Z |
| 매크로 [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) | 여러 [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/)를 하나로 묶음 | 복합 작업 |
| [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 실행 | [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/)를 큐에 저장 후 나중에 실행 | [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 큐 |

```text
+-------------------------------------------------------------+
|       Undo/Redo 스택 동작                                   |
+-------------------------------------------------------------+
|  execute(MoveCmd): undoStack=[MoveCmd], redoStack=[]        |
|  execute(ResizeCmd): undoStack=[MoveCmd, ResizeCmd]         |
|                                                             |
|  Undo: undoStack에서 ResizeCmd 꺼내 undo()                  |
|        redoStack=[ResizeCmd], undoStack=[MoveCmd]           |
|                                                             |
|  Redo: redoStack에서 ResizeCmd 꺼내 execute()               |
|        undoStack=[MoveCmd, ResizeCmd], redoStack=[]         |
+-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 요리 레시피([커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/))에서 잘못된 단계를 되돌리려면 역순으로 취소([undo](/studynote/11_design_supervision/06_exam_summary/393_undo/))하면 된다. 레시피에 각 단계의 취소 방법이 기록되어 있어야 한다.

---
## Ⅲ. 비교 및 연결

[CQRS](/studynote/12_it_management/05_security_compliance/306_cqrs/)([Command](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) Query Responsibility Segregation)와 [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) 패턴의 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/): CQRS의 '[Command](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/)'는 [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) 패턴의 아키텍처 수준 확장이다. CQRS에서 [Command](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) 객체는 시스템 상태를 변경하는 요청을 표현하고, [Command](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) Handler가 Receiver 역할을 한다.

| 비교 축 | A | B |
|:---|:---|:---|
| 수준 | 객체 수준 | 아키텍처 수준 |
| 핵심 | [Undo](/studynote/11_design_supervision/06_exam_summary/393_undo/)/[Redo](/studynote/05_database/04_transactions_concurrency/234_redo_roll_forward_durability_recovery/), 큐 | [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 모델 분리 |
| 통신 | 인프로세스 | 메시지 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) ([Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 등) |
| 적용 범위 | 단일 앱 내 | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템 |

- **📢 섹션 요약 비유**: [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) 패턴은 레스토랑 주문서(단일 앱), CQRS는 주문 관리 시스템([분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 아키텍처)이다. 둘 다 '요청을 객체로 캡슐화'하는 원칙을 공유한다.

---
## Ⅳ. 실무 적용 및 기술사 판단

스프링 MVC에서 `@RequestMapping` 핸들러가 Invoker, Controller 메서드가 ConcreteCommand 역할을 한다. 스프링 배치(Spring Batch)의 `Step` 인터페이스도 [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) 패턴을 구현하여 배치 단계의 실행·건너뛰기·재시작을 지원한다.

### 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) 객체가 execute()와 [undo](/studynote/11_design_supervision/06_exam_summary/393_undo/)() 메서드를 구현하여 [Undo](/studynote/11_design_supervision/06_exam_summary/393_undo/) 기능을 지원하는가?
2. 실행자(Invoker)와 수신자(Receiver)가 [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) 인터페이스로 분리되어 있는가?
3. 실행 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)(undoStack/redoStack)이 올바르게 관리되어 [Undo](/studynote/11_design_supervision/06_exam_summary/393_undo/)/Redo가 동작하는가?
4. 매크로 [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/)(CompositeCommand)로 복합 작업을 원자적으로 실행할 수 있는가?
5. [CQRS](/studynote/12_it_management/05_security_compliance/306_cqrs/) 패턴을 적용할 때 [Command](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) 객체가 [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) 패턴의 원칙을 따르는가?

- **📢 섹션 요약 비유**: 주문서([커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) 객체)는 주문 내용(execute)과 취소 방법([undo](/studynote/11_design_supervision/06_exam_summary/393_undo/))을 담아, 웨이터(Invoker)가 주방(Receiver)에 전달하거나 필요 시 취소할 수 있게 한다.

---

## Ⅴ. 기대효과 및 결론

[커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) 패턴을 적용하면 요청 발신자와 수신자의 결합도가 낮아지고, [Undo](/studynote/11_design_supervision/06_exam_summary/393_undo/)/[Redo](/studynote/05_database/04_transactions_concurrency/234_redo_roll_forward_durability_recovery/)·작업 큐·로깅·[트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 등의 고급 기능을 체계적으로 구현할 수 있다. [CQRS](/studynote/12_it_management/05_security_compliance/306_cqrs/)·[이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)과 결합하면 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템에서도 강력한 명령 처리 아키텍처를 달성한다.

한계는 [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) 클래스 수가 많아지면 관리 복잡성이 증가하고, [Undo](/studynote/11_design_supervision/06_exam_summary/393_undo/) 구현 시 상태 복원이 복잡한 경우 [메멘토](/studynote/04_software_engineering/05_devops_ci_cd/274_memento_pattern/)([Memento](/studynote/04_software_engineering/05_devops_ci_cd/274_memento_pattern/)) 패턴과 함께 사용해야 한다.

- **📢 섹션 요약 비유**: [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) 패턴은 체스 기보처럼, 모든 수([커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/))를 기록하면 어느 시점으로든 되돌리거나([Undo](/studynote/11_design_supervision/06_exam_summary/393_undo/)), 재현할 수 있다([Redo](/studynote/05_database/04_transactions_concurrency/234_redo_roll_forward_durability_recovery/)).

---

### 📌 관련 개념 맵

[요청 캡슐화] -> [커맨드 패턴] -> Undo/[Redo](/studynote/05_database/04_transactions_concurrency/234_redo_roll_forward_durability_recovery/) 스택] -> CQRS [Command](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/)] -> [이벤트 소싱 통합]

| 개념 | 연결 포인트 |
|:---|:---|
| [CQRS](/studynote/12_it_management/05_security_compliance/306_cqrs/) | [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) 패턴의 아키텍처 수준 확장 |
| [메멘토 패턴](/studynote/11_design_supervision/06_exam_summary/398_process/) | 복잡한 Undo를 위한 상태 [스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) 저장 |
| [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) | [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) 객체로 원자적 작업 표현 |
| [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/) | [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) 실행 결과를 이벤트로 저장 |

### 📈 관련 키워드 및 발전 흐름도

[GoF [Command](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/)(1994)] -> [GUI [Undo](/studynote/11_design_supervision/06_exam_summary/393_undo/)/[Redo](/studynote/05_database/04_transactions_concurrency/234_redo_roll_forward_durability_recovery/)] -> CQRS [Command](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) 객체] -> [이벤트 소싱 통합] -> [분산 보상 트랜잭션]

### 👶 어린이를 위한 3줄 비유 설명

1. [커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) 패턴은 주문서처럼, 요청을 객체로 만들어 나중에 실행하거나 취소([Undo](/studynote/11_design_supervision/06_exam_summary/393_undo/))할 수 있어요.
2. Ctrl+Z(되돌리기)가 바로 이 패턴을 사용해요.
3. CQRS에서 [Command](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) 객체도 이 패턴의 아키텍처 버전이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 257 / 530

<- **이전**: [195. 팩터리 메서드 vs 템플릿 메서드 (Factory Method vs Template Method)](/studynote/11_design_supervision/04_gof_behavioral/195_factory_vs_template_method/)
**다음**: [197. 상태 패턴 (State Pattern)](/studynote/11_design_supervision/04_gof_behavioral/197_state_pattern/) ->

---
