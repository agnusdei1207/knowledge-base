+++
title = "86. 프로세스 상태 (Process State)"
date = 2026-03-21

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 프로세스 상태([Process](/knowledge-base/studynote/12_it_management/05_security_compliance/943_process/) [State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/))는 프로세스가 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)부터 종료까지 어떤 단계에 있는지 보여 준다.
> 2. **가치**: Ready, Running, Waiting, Terminated를 이해하면 Scheduler, [Dispatcher](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/), [Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) Switch가 연결된다.
> 3. **판단 포인트**: PCB ([Process](/knowledge-base/studynote/12_it_management/05_security_compliance/943_process/) Control Block)와 대기 큐를 같이 봐야 [상태 전이](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/)가 정확해진다.

---

## Ⅰ. 개요 및 필요성
프로세스 상태는 “지금 CPU (Central Processing Unit)를 쓰는가, 기다리는가, 끝났는가”를 보여 준다. 상태를 구분해야 스케줄러가 누구에게 CPU를 줄지 결정할 수 있다.

결국 이 개념은 자원 사용의 흐름을 읽는 일이다.
- **📢 섹션 요약 비유**: 준비 중과 기다림을 구분해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리
| 상태 | 의미 | 전이 [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) |
|:---|:---|:---|
| [New](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 직후 | admit |
| Ready | CPU를 받을 준비 | dispatch 대기 |
| Running | CPU를 점유 중 | preempt, wait, exit |
| Waiting | 입출력 대기 | I/O 완료 |
| Terminated | 종료 완료 | 자원 회수 |

+------+ admit  +-------+ dispatch +--------+
| [New](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)  |------->| Ready |------->| Running|
+------+       +--+----+       +--+-----+
                 |               | exit
                 | wait I/O      | preempt
                 v               v
            +--------+     +------------+
            |Waiting |<-----| Terminated |
            +--+-----+ I/O  +------------+
               +-------- complete
- **📢 섹션 요약 비유**: [상태 전이](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/)는 스케줄링 사건으로 바뀐다.

---

## Ⅲ. 비교 및 연결
| 비교 항목 | Ready | Running | Waiting | Terminated |
|:---|:---|:---|:---|:---|
| CPU 점유 | 없음 | 있음 | 없음 | 없음 |
| 큐 위치 | [ready queue](/knowledge-base/studynote/02_operating_system/02_process_thread/088_ready_queue/) | 실행 중 | [wait queue](/knowledge-base/studynote/02_operating_system/02_process_thread/089_wait_queue/) | 없음 |
| 핵심 판단 | 언제 CPU를 받을까 | 지금 무엇을 실행하나 | 언제 깨어날까 | 자원 회수 여부 |

상태 이름보다 상태를 바꾸는 사건을 함께 봐야 정확하다.
- **📢 섹션 요약 비유**: Ready와 Waiting은 완전히 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단
- [ ] Ready와 Waiting을 혼동하지 않는다.
- [ ] [Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) Switch가 비용이 드는 전환임을 이해한다.
- [ ] PCB에 레지스터와 프로그램 카운터가 저장된다는 점을 설명한다.
- [ ] 선점형과 비선점형 스케줄링을 구분한다.

- ❌ Waiting을 단순히 쉬는 상태로만 설명하는 것
- ❌ Scheduler와 Dispatcher를 같은 것으로 보는 것
- ❌ [상태 전이](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/) 없이 프로세스 실행을 설명하는 것
- **📢 섹션 요약 비유**: 문맥 교환과 PCB를 함께 봐야 한다.

---

## Ⅴ. 기대효과 및 결론
프로세스 상태는 한 사람의 일과표처럼 보면 쉽다. 준비 중인지, 일하는 중인지, 기다리는지, 끝났는지를 알아야 다음 행동을 정할 수 있다.
- **📢 섹션 요약 비유**: 상태를 알면 운영체제의 흐름이 보인다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Ready | CPU를 기다리는 줄이다. |
| Running | 실제로 CPU를 쓰는 순간이다. |
| Waiting | 입출력 결과를 기다리는 줄이다. |
| PCB ([Process](/knowledge-base/studynote/12_it_management/05_security_compliance/943_process/) Control Block) | 상태를 기억하는 노트다. |
| [Dispatcher](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/) | 준비된 일을 CPU 위에 올린다. |

### 📈 관련 키워드 및 발전 흐름도

```text
생성 -> Ready -> Running -> Waiting ↔ Ready -> Terminated
```

### 👶 어린이를 위한 3줄 비유 설명

1. 놀이터에서 줄을 서는 아이는 아직 차례를 기다리는 중이다.
2. 그네를 타는 아이는 지금 실제로 움직이고 있는 중이다.
3. 끝나고 집에 간 아이는 이제 더 이상 줄에 서 있지 않다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 86 / 800

<- **이전**: [85. 스택 (Stack) 영역 - 지역 변수, 매개변수, 리턴 주소](/knowledge-base/studynote/02_operating_system/02_process_thread/085_stack_segment/)
**다음**: [87. 생성 (New) -> 준비 (Ready) -> 실행 (Running) -> 대기 (Waiting/Blocked) -> 종료 (Terminated)](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) ->

---
