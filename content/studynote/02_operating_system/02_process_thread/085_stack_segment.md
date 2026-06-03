+++
title = "85. 스택 (Stack) 영역 - 지역 변수, 매개변수, 리턴 주소"
date = 2026-03-21

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> **본질**: [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)([Stack](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)) 영역은 [함수 호출](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/294_function_calling_tool_use/) 때 생기는 프레임(Frame)을 쌓아 두는 프로세스 메모리 영역이다.
> **가치**: 지역 변수, 매개변수, 복귀 주소, 저장 레지스터를 빠르게 관리할 수 있어 [함수 호출](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/294_function_calling_tool_use/)이 자연스러워진다.
> **판단 포인트**: 깊은 [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/), 큰 지역 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/), 무분별한 alloca는 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 오버플로([Overflow](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/095_overflow/)) 위험을 키운다.

---

## Ⅰ. 개요 및 필요성

[스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 영역은 [함수 호출](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/294_function_calling_tool_use/)과 복귀를 위해 사용하는 LIFO(Last In, First Out) 메모리 구조다. 호출이 중첩될 때마다 새로운 프레임이 올라가고, 함수가 끝나면 마지막에 들어온 프레임부터 내려간다.

이 구조가 필요한 이유는 [함수 호출](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/294_function_calling_tool_use/)의 상태를 빠르게 저장하고 복원해야 하기 때문이다. [ABI](/knowledge-base/studynote/02_operating_system/01_overview_architecture/015_abi/) ([Application Binary Interface](/knowledge-base/studynote/02_operating_system/01_overview_architecture/015_abi/))가 호출 규약을 정의하는 이유도, [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)을 어떻게 쓰는지 정하지 않으면 다른 함수와 모듈이 서로 맞물리지 않기 때문이다.

- 📢 섹션 요약 비유: 겹겹이 쌓는 작업대

---

## Ⅱ. 아키텍처 및 핵심 원리

[스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 프레임에는 보통 복귀 주소, 이전 프레임 포인터, 지역 변수, 임시 값, 인자가 들어간다. [SP](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/) ([Stack](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) Pointer)는 현재 꼭대기를 가리키고, [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/) (Frame Pointer)는 현재 프레임의 기준점을 잡아 디버깅과 접근을 쉽게 만든다. 많은 시스템에서 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)은 높은 주소에서 낮은 주소 방향으로 자란다.

```text
높은 주소
┌──────────────────┐
│ 이전 프레임      │
├──────────────────┤
│ 복귀 주소        │
├──────────────────┤
│ 지역 변수 / 임시값│
├──────────────────┤
│ 현재 SP          │
└──────────────────┘
낮은 주소
```

| 항목 | 역할 |
| --- | --- |
| Return Address | 함수가 끝난 뒤 돌아갈 위치 |
| Local Variables | 함수 내부 임시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| Saved Registers | 호출 전 상태 보존 |
| Args | 함수 입력값 보관 |

[스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)은 빠르지만 크기가 제한되므로, "빠르다"와 "많이 담을 수 있다"는 다른 얘기라는 점이 핵심이다.

- 📢 섹션 요약 비유: 서랍식 호출 기록

---

## Ⅲ. 비교 및 연결

[스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)은 힙([Heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/))과 자주 비교된다. [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)은 자동 관리되고 접근이 빠르지만 수명이 짧고 크기가 제한된다. 힙은 자유도가 높지만 할당/해제가 느리고 단편화가 생길 수 있다. 정적 영역이나 [BSS](/knowledge-base/studynote/02_operating_system/02_process_thread/083_bss_segment/) (Block Started by Symbol)는 프로그램 전체 수명 동안 유지되는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 가깝다.

| 영역 | 특징 | 대표 용도 |
| --- | --- | --- |
| [Stack](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) | 빠르고 자동 관리 | 지역 변수, 호출 프레임 |
| [Heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/) | 동적이고 유연 | 객체, 큰 버퍼 |
| Static/[BSS](/knowledge-base/studynote/02_operating_system/02_process_thread/083_bss_segment/) | 프로그램 전체 수명 | 전역/정적 변수 |

즉 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)은 "[함수 호출](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/294_function_calling_tool_use/)을 위한 임시 작업대"이고, 힙은 "장기 보관 창고"로 이해하면 경계가 선명해진다.

- 📢 섹션 요약 비유: 작업대와 창고

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 큰 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)이나 깊은 [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/)를 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)에 올리지 않는 것이 기본이다. 멀티스레드 환경에서는 스레드별 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 크기가 다르므로, [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/)나 지역 변수 크기를 조심해야 한다. 또한 주소가 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 영역인지 힙 영역인지 알고 디버깅해야 원인 분석이 빨라진다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 지역 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)이 지나치게 크지 않은가?
2. [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/) 깊이가 입력에 비례해 커지지 않는가?
3. 프레임 포인터를 기준으로 디버깅 가능한가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 지역 변수 주소를 밖으로 반환하는 것
- 대형 버퍼를 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)에 무심코 두는 것
- [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/) 종료 조건이 약한 알고리즘을 그대로 쓰는 것

- 📢 섹션 요약 비유: 빨리 쌓고 빨리 치우기

---

## Ⅴ. 기대효과 및 결론

[스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 구조를 이해하면 [함수 호출](/knowledge-base/studynote/06_ict_convergence/04_ai_llm/294_function_calling_tool_use/), 예외 처리, [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/), 디버깅을 하나의 메모리 모델로 설명할 수 있다. 반면 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)과 힙을 혼동하면 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 문제와 메모리 오류를 헷갈리기 쉽다. 그래서 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)은 "자동 정리되는 임시 작업대"로 기억하는 것이 좋다.

결론적으로 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 영역은 호출 규약과 메모리 안정성의 교차점이다. 기술사 답변에서는 [SP](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/), [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/), 호출 프레임, 오버플로 위험을 함께 설명하면 탄탄하다.

- 📢 섹션 요약 비유: 접시 [더미](/knowledge-base/studynote/04_software_engineering/11_testing_validation/459_dummy_test_double/)

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| --- | --- |
| [Stack](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) | LIFO 메모리 구조 |
| [SP](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/) ([Stack](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) Pointer) | 현재 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 꼭대기 |
| [FP](/knowledge-base/studynote/12_it_management/05_security_compliance/293_fp_function_point/) (Frame Pointer) | 현재 프레임 기준점 |
| [ABI](/knowledge-base/studynote/02_operating_system/01_overview_architecture/015_abi/) ([Application Binary Interface](/knowledge-base/studynote/02_operating_system/01_overview_architecture/015_abi/)) | 호출 규약 정의 |
| [Heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/) | 동적 할당 영역 |
| [Stack](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) [Overflow](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/095_overflow/) | [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 크기 초과 문제 |

### 📈 관련 키워드 및 발전 흐름도

```text
함수 호출
   ↓
새 스택 프레임 생성
   ↓
지역 변수 / 복귀 주소 저장
   ↓
함수 종료
   ↓
프레임 제거
```

### 👶 어린이를 위한 3줄 비유 설명

1. [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)은 접시를 위로 하나씩 쌓아 두는 선반 같아요.
2. 맨 위 접시부터 꺼내야 아래가 안 무너져요.
3. 그래서 마지막에 넣은 일이 먼저 끝나는 방식이 편해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 85 / 800

← **이전**: [84. 힙 (Heap) 영역 - 동적 할당 (malloc/free)](/knowledge-base/studynote/02_operating_system/02_process_thread/084_heap_segment/)
**다음**: [86. 프로세스 상태 (Process State)](/knowledge-base/studynote/02_operating_system/02_process_thread/086_process_state/) →

---
