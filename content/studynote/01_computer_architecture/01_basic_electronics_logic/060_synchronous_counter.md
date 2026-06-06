---
title: "Synchronous Counter"
date: "2026-03-19"
tags:
  - "studynote-computer-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 동기식 카운터는 모든 [플립플롭](/studynote/01_computer_architecture/01_basic_electronics_logic/051_flip_flop/)이 하나의 공통 클럭을 공유하며 동시에 상태를 바꾸는 순차 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)회로다.
> 2. **가치**: 비동기식 리플 카운터의 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 누적과 글리치를 줄여 고속 CPU와 타이머에 적합하다.
> 3. **판단 포인트**: 다음 상태를 미리 계산하는 look-ahead [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)와 클럭 스큐 관리가 성능을 좌우한다.

---

## Ⅰ. 개요 및 필요성

카운터는 숫자를 세는 회로지만, 고속 시스템에서는 "언제" 바뀌는지가 더 중요하다. 비동기식 카운터는 앞 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)가 바뀌어야 다음 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)가 바뀌어서 느리고 흔들린다.

동기식 카운터는 모든 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)가 같은 순간에 갱신되도록 해, [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)(Program [Counter](/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/))나 버스트 주소 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)처럼 정확한 박자가 필요한 곳에서 쓰인다.

- **📢 섹션 요약 비유**: 도미노처럼 순서대로 넘기지 않고, 지휘자의 손짓에 맞춰 동시에 박수치는 합창단이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

핵심은 공통 클럭과 조합 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)의 결합이다. 각 [플립플롭](/studynote/01_computer_architecture/01_basic_electronics_logic/051_flip_flop/)은 다음 박자에 뒤집힐지 미리 계산하고, 클럭 에지에서 한꺼번에 반응한다.

```text
CLK ------------------> [FF0]
  +-------------------> [FF1]
  +-------------------> [FF2]
  +-------------------> [FF3]

AND / look-ahead logic가 다음 상태를 미리 계산
```

| 구성 요소 | 역할 |
| :-- | :-- |
| T/JK [플립플롭](/studynote/01_computer_architecture/01_basic_electronics_logic/051_flip_flop/) | 상태 저장과 반전 |
| 공통 클럭 | 동시에 상태 갱신 |
| Look-ahead [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) | 다음 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)의 반전 조건 계산 |
| Enable | 카운트 시작/정지 제어 |

예를 들어 `011`에서 `100`으로 넘어갈 때, 하위 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)가 모두 1이라는 조건을 AND 게이트가 미리 감시한다. 그래서 클럭이 오면 모든 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)가 한 번에 바뀐다.

- **📢 섹션 요약 비유**: 출발 총이 울리기 전, 누가 뛰어야 할지 이미 전원이 다 알고 있는 경기장이다.

---

## Ⅲ. 비교 및 연결

| 항목 | 비동기식(Ripple) | 동기식([Synchronous](/studynote/03_network/01_data_communication/010_동기식_비동기식_전송/)) |
| :-- | :-- | :-- |
| 속도 | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 누적 | 일정하고 빠름 |
| 안정성 | 글리치 가능 | 안정적 |
| 회로 | 단순 | 더 복잡 |
| 고속 적합성 | 낮음 | 높음 |

동기식 카운터는 조합 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)를 더 쓰는 대신 전파 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 줄여 고속화에 유리하다. 그래서 현대 반도체에서는 단순한 연결보다 예측 가능한 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 구조를 선호한다.

- **📢 섹션 요약 비유**: 줄서서 하나씩 움직이는 것과, 미리 연습해 두고 동시에 움직이는 군무의 차이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

동기식 카운터는 단순한 숫자 세기보다 주소 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 주파수 분주, 상태기계 제어에서 중요하다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 출력 글리치가 허용되지 않는가?
2. 높은 클럭 속도에서 안정성이 필요한가?
3. Mod-N 카운터나 Gray Code가 필요한가?
4. 클럭 스큐와 셋업/홀드 조건을 만족하는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 비동기식 구조를 고속 주소 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)에 그대로 쓰는 설계
- look-ahead 없이 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수만 늘리는 설계
- 클럭 분배를 무시하고 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)만 추가하는 설계

- **📢 섹션 요약 비유**: 빨리 가야 하는 자동차에 브레이크만 붙이는 게 아니라, 엔진과 변속기까지 같이 맞춰야 하는 문제다.

---

## Ⅴ. 기대효과 및 결론

동기식 카운터는 박자와 정확도를 동시에 잡는다. 이 특성 덕분에 CPU, 메모리, 통신 장비의 시간 제어에 널리 쓰인다.

결국 카운터를 설계할 때는 "얼마나 세는가"보다 "얼마나 정확하게 동시에 세는가"를 봐야 한다.

- **📢 섹션 요약 비유**: 오케스트라가 박자를 하나로 맞춰야 아름다운 곡이 되는 것과 같다.

---

## 관련 개념 맵

```text
클럭(Clock)
   v
플립플롭(Flip-Flop)
   v
동기식 카운터
   v
PC / 타이머 / 주소 생성
```

---

## 관련 키워드 및 발전 흐름도

```text
비동기식 카운터
   v
동기식 카운터
   v
Look-ahead 논리
   v
고속 주소/상태 제어
```

---

## 어린이를 위한 3줄 비유 설명

동기식 카운터는 모두가 같은 박자에 맞춰 숫자를 세는 로봇이에요.
누가 먼저 움직일지 기다리지 않아서 빨라요.
그래서 컴퓨터가 시간을 정확하게 맞출 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 60 / 803

<- **이전**: [59. 카운터 (Counter)](/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)
**다음**: [61. 비동기식 카운터 (리플 카운터)](/studynote/01_computer_architecture/01_basic_electronics_logic/061_asynchronous_counter/) ->

---
