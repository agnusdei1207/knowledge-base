---
title: "Memento Pattern"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [Memento](/studynote/04_software_engineering/05_devops_ci_cd/274_memento_pattern/) ([메멘토](/studynote/04_software_engineering/05_devops_ci_cd/274_memento_pattern/)) 패턴은 객체의 캡슐화(Encapsulation)를 훼손하지 않으면서, 특정 시점의 내부 상태([스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/))를 외부에 저장하고 필요 시 복원([Undo](/studynote/11_design_supervision/06_exam_summary/393_undo/)/[Redo](/studynote/05_database/04_transactions_concurrency/234_redo_roll_forward_durability_recovery/))할 수 있게 한다.
> 2. **가치**: Originator (원본 객체)만이 Memento의 내용을 읽고 쓸 수 있으므로, 상태 노출 없이 [Undo](/studynote/11_design_supervision/06_exam_summary/393_undo/) 스택을 구현할 수 있다.
> 3. **판단 포인트**: 텍스트 에디터 [Undo](/studynote/11_design_supervision/06_exam_summary/393_undo/), 게임 세이브·로드, [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)처럼 "시간을 되돌리는" 기능이 필요할 때 적용한다.

---

## Ⅰ. 개요 및 필요성
[Undo](/studynote/11_design_supervision/06_exam_summary/393_undo/) (실행 취소) 기능을 구현하려면 이전 상태를 저장해야 한다. 하지만 저장 객체(Caretaker)가 Originator의 내부 필드에 직접 접근하면 **캡슐화가 깨진다**.

```
  ❌ 나쁜 방법: 캡슐화 파괴
  Caretaker caretaker = ...;
  caretaker.savedState = editor.text;  // private 필드 직접 접근
  caretaker.savedCursor = editor.cursor; // 내부 구현 노출

  ✅ Memento 패턴: 캡슐화 보존
  Memento m = editor.save();         // Originator가 직접 스냅샷 생성
  caretaker.push(m);                 // Caretaker는 불투명한 Memento만 보관
  editor.restore(m);                 // 복원도 Originator가 직접
```

| 역할 | 책임 | 비유 |
|:---|:---|:---|
| **Originator** | 상태를 가진 원본 객체, [Memento](/studynote/04_software_engineering/05_devops_ci_cd/274_memento_pattern/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·복원 | 사진 찍히는 대상 |
| <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/274_memento_pattern/">Memento</a></strong> | 특정 시점의 상태 [스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) (불투명 객체) | 인화된 사진 |
| **Caretaker** | Memento를 보관하지만 내용을 읽지 않음 | 사진 앨범 |

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: 게임 세이브 기능 — 캐릭터(Originator)가 자기 상태를 세이브 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)([Memento](/studynote/04_software_engineering/05_devops_ci_cd/274_memento_pattern/))로 저장하고, 세이브 슬롯(Caretaker)이 보관하고, 로드(restore)하면 그 시점으로 복원된다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
  Originator                     Caretaker
  --------------                 ------------------
  - state                        - history: Stack<Memento>
  + save(): Memento              + push(m: Memento)
  + restore(m: Memento)          + pop(): Memento
        |                               |
        +----- creates --------►  Memento
                                  ------------------
                                  - state (private)
                                  + getState() [Originator only]
```

```
  [ 작업 흐름 ]

  (1) 초기 상태: "Hello"
       | save() -> Memento("Hello")
       | history: [M1("Hello")]

  (2) 입력: "Hello World"
       | save() -> Memento("Hello World")
       | history: [M1("Hello"), M2("Hello World")]

  (3) 입력: "Hello World!!!"
       | save() -> Memento("Hello World!!!")
       | history: [M1, M2, M3("Hello World!!!")]

  (4) Ctrl+Z (Undo)
       | history.pop() -> M3
       | restore(M2) -> 텍스트 = "Hello World"

  (5) Ctrl+Z (Undo)
       | restore(M1) -> 텍스트 = "Hello"
```

```
  Command + Memento = 완전한 Undo/Redo 시스템

  +-----------------------------------------------------+
  |  UndoManager (Caretaker)                            |
  |                                                     |
  |  undoStack: Stack<Command>                          |
  |  redoStack: Stack<Command>                          |
  |                                                     |
  |  execute(cmd):                                      |
  |    memento = originator.save()                      |
  |    cmd.setMemento(memento)                          |
  |    cmd.execute()                                    |
  |    undoStack.push(cmd)                              |
  |                                                     |
  |  undo():                                            |
  |    cmd = undoStack.pop()                            |
  |    originator.restore(cmd.getMemento())             |
  |    redoStack.push(cmd)                              |
  |                                                     |
  |  redo():                                            |
  |    cmd = redoStack.pop()                            |
  |    cmd.execute()                                    |
  |    undoStack.push(cmd)                              |
  +-----------------------------------------------------+
```

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 역할 | 입력·상태·출력을 분리하는 책임 경계 | 구현보다 경계를 먼저 본다. |
| 제어 지점 | 조건, 이벤트, 정책이 만나는 곳 | 병목과 결합이 생기는 곳이다. |
| [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 포인트 | 테스트·[로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·모니터링으로 확인할 지점 | 운영 가능성이 설계 품질을 결정한다. |

- **📢 섹션 요약 비유**: 체스 경기 기록지(Caretaker) — 각 수([Memento](/studynote/04_software_engineering/05_devops_ci_cd/274_memento_pattern/))를 기록해두면, 언제든 되감아서(restore) 특정 시점으로 돌아갈 수 있다. 기록지는 수의 의미를 이해할 필요가 없다.

---

## Ⅲ. 비교 및 연결
| 방식 | 설명 | 장점 | 단점 |
|:---|:---|:---|:---|
| <strong>내부 클래스 <a href="/studynote/04_software_engineering/05_devops_ci_cd/274_memento_pattern/">Memento</a></strong> | Originator 내부에 private 클래스 | 캡슐화 완벽 | 언어 지원 필요 |
| **Interface 기반** | Memento를 빈 인터페이스로 | 유연성 | 캡슐화 약화 가능 |
| **직렬화(Serialization)** | 객체를 [byte](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/)[]로 저장 | 딥카피 자동 | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 비용 |
| **Shallow Copy** | [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 복사 | 빠름 | [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 타입 공유 주의 |
| **Deep Copy** | 완전 복사 | 안전 | 메모리·시간 비용 |

| 패턴 | Memento와의 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
|:---|:---|
| [Command](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) ([커맨드](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/)) | Command에 Memento를 포함하면 [Undo](/studynote/11_design_supervision/06_exam_summary/393_undo/) 가능 |
| [Prototype](/studynote/04_software_engineering/04_testing_quality/257_prototype_pattern_object_cloning/) ([프로토타입](/studynote/04_software_engineering/04_testing_quality/257_prototype_pattern_object_cloning/)) | 딥카피로 [Memento](/studynote/04_software_engineering/05_devops_ci_cd/274_memento_pattern/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 가능 |
| [Iterator](/studynote/04_software_engineering/04_testing_quality/270_iterator_pattern/) ([이터레이터](/studynote/04_software_engineering/04_testing_quality/270_iterator_pattern/)) | [Iterator](/studynote/04_software_engineering/04_testing_quality/270_iterator_pattern/) 상태를 Memento로 저장·복원 |
| [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) (상태) | State와 [Memento](/studynote/04_software_engineering/05_devops_ci_cd/274_memento_pattern/) 조합으로 FSM 히스토리 관리 |

- **📢 섹션 요약 비유**: Memento는 "타임캡슐" — 묻는 사람(Originator)만 내용을 알고, 묻어두는 사람(Caretaker)은 언제 묻었는지만 알면 된다.

---

## Ⅳ. 실무 적용 및 기술사 판단
대용량 객체의 경우 매번 전체 상태를 저장하면 메모리 폭발:

```
  일반 Memento:
  State1(100MB) -> State2(100MB) -> State3(100MB)
  -> Undo 3단계 = 300MB 필요

  Incremental Memento (증분 저장):
  State1(100MB) -> Delta1(변경분만, ~1KB) -> Delta2(~1KB)
  -> Undo 3단계 = 100MB + 2KB 필요

  구현: 변경된 필드만 저장, 역순으로 적용
```

```
  DB Transaction    ↔    Memento Pattern
  ----------------------------------------
  BEGIN                  originator.save()
  UPDATE/INSERT          실행
  ROLLBACK               originator.restore(memento)
  COMMIT                 history.clear() (더 이상 롤백 불필요)
```

- <strong>캡슐화 보존</strong>이 [Memento](/studynote/04_software_engineering/05_devops_ci_cd/274_memento_pattern/) 패턴의 핵심 가치임을 반드시 언급
- [Command](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) + [Memento](/studynote/04_software_engineering/05_devops_ci_cd/274_memento_pattern/) = [Undo](/studynote/11_design_supervision/06_exam_summary/393_undo/)/[Redo](/studynote/05_database/04_transactions_concurrency/234_redo_roll_forward_durability_recovery/) 시스템 조합 설계 제시
- 메모리 비용과 <strong>증분(Incremental) <a href="/studynote/04_software_engineering/05_devops_ci_cd/274_memento_pattern/">Memento</a></strong> 최적화 방법 언급

### 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 해결하려는 변화 축이 분명한가?
2. [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 비용보다 변경 절감 효과가 큰가?
3. 테스트·[로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: Memento는 "방 사진 촬영" — 청소하기 전에 사진을 찍어두면(save), 나중에 원래 배치로 복원(restore)할 수 있다. 청소부(Caretaker)는 사진만 보관하고 방 배치는 몰라도 된다.

---

## Ⅴ. 기대효과 및 결론
| 효과 | 설명 |
|:---|:---|
| 캡슐화 보존 | Caretaker가 내부 구현 없이 상태 보관 |
| [Undo](/studynote/11_design_supervision/06_exam_summary/393_undo/)/[Redo](/studynote/05_database/04_transactions_concurrency/234_redo_roll_forward_durability_recovery/) 구현 | 히스토리 스택으로 시간 역행 가능 |
| 오류 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | 잘못된 연산 후 이전 상태로 복원 |
| [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 지원 | DB [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)과 동일한 원리의 메모리 내 구현 |

- **메모리 사용**: 상태가 크거나 [Undo](/studynote/11_design_supervision/06_exam_summary/393_undo/) 깊이가 깊을수록 메모리 급증 -> 최대 히스토리 수 제한 필요
- <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong>: Deep Copy 비용 -> 증분 저장 또는 [Copy-on-Write](/studynote/02_operating_system/09_file_system/542_cow_file_system/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 고려
- **캡슐화**: Java에서는 내부 클래스, C++에서는 `friend` 키워드로 구현

[Memento](/studynote/04_software_engineering/05_devops_ci_cd/274_memento_pattern/) ([메멘토](/studynote/04_software_engineering/05_devops_ci_cd/274_memento_pattern/)) 패턴은 <strong>캡슐화를 지키면서 역사를 기록</strong>하는 우아한 해법이다. 텍스트 에디터의 Ctrl+Z, 게임 세이브·로드, [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 등 "시간을 되돌리는" 모든 기능의 설계 근간이다. [Command](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) 패턴과 결합하면 완전한 [Undo](/studynote/11_design_supervision/06_exam_summary/393_undo/)/[Redo](/studynote/05_database/04_transactions_concurrency/234_redo_roll_forward_durability_recovery/) 시스템이 완성된다.

확장 방향은 ① 선언형 API와의 결합, ② [관측 가능성](/studynote/04_software_engineering/02_requirements_analysis/111_observability_metrics_logs_traces/)([Observability](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/)) 내장, ③ [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: Memento는 "회사 연간 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)" — 매년 말 서버 상태를 통째로 저장해두고, 문제 생기면 언제든 그 시점으로 되돌아갈 수 있다.

---

### 📌 관련 개념 맵
| [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | GoF Behavioral Pattern | 행동 패턴 그룹 |
| 하위 개념 | Originator / [Memento](/studynote/04_software_engineering/05_devops_ci_cd/274_memento_pattern/) / Caretaker | 패턴 3요소 |
| 연관 개념 | [Command Pattern](/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) | [Undo](/studynote/11_design_supervision/06_exam_summary/393_undo/) 스택을 위한 조합 |
| 연관 개념 | [Prototype Pattern](/studynote/11_design_supervision/03_gof_creational_structural/149_prototype_pattern/) | Deep Copy로 [Memento](/studynote/04_software_engineering/05_devops_ci_cd/274_memento_pattern/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| 연관 개념 | DB [Transaction](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) [Rollback](/studynote/02_operating_system/05_deadlock/313_rollback/) | 동일 원리의 [영속성](/studynote/05_database/04_transactions_concurrency/196_durability_permanent_storage/) 층 구현 |
| 연관 개념 | Encapsulation (캡슐화) | Memento가 보존하는 핵심 원칙 |

### 📈 관련 키워드 및 발전 흐름도
상태 캡슐화 -> [메멘토 패턴](/studynote/11_design_supervision/06_exam_summary/398_process/) -> [Undo](/studynote/11_design_supervision/06_exam_summary/393_undo/)/[Redo](/studynote/05_database/04_transactions_concurrency/234_redo_roll_forward_durability_recovery/)·[Snapshot](/studynote/02_operating_system/10_security/637_zfs_snapshot_cow_architecture/)

### 👶 어린이를 위한 3줄 비유 설명
1. 그림 그리다가 망했을 때 "되돌리기" 버튼을 누르면 이전 그림으로 돌아가죠?
2. [메멘토 패턴](/studynote/11_design_supervision/06_exam_summary/398_process/)은 그 되돌리기 기능을 만드는 방법이에요.
3. 그림판(Originator)이 자기 그림의 사진([Memento](/studynote/04_software_engineering/05_devops_ci_cd/274_memento_pattern/))을 찍어두고, 앨범(Caretaker)에 저장해두는 거예요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 266 / 530

<- **이전**: [204. 이터레이터 패턴 (Iterator Pattern)](/studynote/11_design_supervision/04_gof_behavioral/204_iterator_pattern/)
**다음**: [206. 해석자 패턴 (Interpreter Pattern)](/studynote/11_design_supervision/04_gof_behavioral/206_interpreter_pattern/) ->

---
