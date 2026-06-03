+++
title = "64. 존슨 카운터 (Johnson Counter)"
date = 2026-04-19

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 존슨 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)(Johnson [Counter](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/))는 마지막 출력의 보수를 처음 입력으로 되돌리는 변형된 시프트 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)다.
> 2. **가치**: n개의 플립플롭으로 2n개의 상태를 만들 수 있어 링 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)보다 상태 효율이 높다.
> 3. **판단**: 상태가 늘어도 해독이 쉽고, 순차 제어와 타이밍 생성에 자주 쓰인다.

---

## Ⅰ. 개요 및 필요성

존슨 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)는 링 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)의 단순함과 이진 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)의 상태 효율 사이를 절충한 회로다. 출력이 한 번 뒤집혀 돌아오기 때문에 상태 수가 두 배로 늘어난다.

이 방식은 순차 제어, [LED](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/013_led/) 패턴, 스캔 타이밍처럼 규칙적인 순환을 만들 때 유용하다.

- **📢 섹션 요약 비유**: 동그란 줄에서 뒤집힌 이름표를 넘기면 같은 인원으로 더 많은 순서를 만들 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">FF1 → FF2 → FF3 → FF4</div>
<div class="kb-diagram-tree-item" style="--depth:0">inverted ─</div>
</div>
</div>



| 구성 요소 | 역할 |
| :-- | :-- |
| [Flip-Flop](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/051_flip_flop/) | 상태 저장 |
| Inverted Feedback | 마지막 비트를 뒤집어 입력 |
| [Clock](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/045_clock/) | 상태 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) |
| Reset | [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 상태 지정 |

```text
0000 → 1000 → 1100 → 1110 → 1111 → 0111 → 0011 → 0001 → 0000
```

존슨 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)는 연속된 1과 0의 조합을 만들어 해독이 쉽다. 그래서 디코딩 로직이 단순하고, 제한된 하드웨어에서 많은 순서를 표현할 수 있다.

- **📢 섹션 요약 비유**: 한 번 뒤집어서 돌아오면 같은 색이 아니라 짝이 바뀐 카드들이 차례대로 나온다.

---

## Ⅲ. 비교 및 연결

| 구분 | [Ring Counter](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/063_ring_counter/) | Johnson [Counter](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/) | Binary [Counter](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/) |
| :-- | :-- | :-- | :-- |
| 상태 수 | n | 2n | 2^n |
| 상태 해석 | 매우 쉬움 | 쉬움 | 중간 |
| 하드웨어 효율 | 낮음 | 중간 | 높음 |

존슨 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)는 링 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)보다 상태 수가 많고, 이진 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)보다 해독이 쉽다. 그래서 실무에서는 "애매한 중간"이 아니라 "딱 필요한 절충"으로 쓰인다.

- **📢 섹션 요약 비유**: 줄은 하나인데 번호표를 앞뒤로 뒤집어 더 많은 차례를 만드는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 상태 수와 해독 난이도의 균형이 맞는가?
2. [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 상태와 reset 로직이 안정적인가?
3. 클록 경계에서 전이 오류가 없는가?
4. 출력 패턴이 요구 사항과 맞는가?
5. 링 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)보다 효율이 필요한 상황인가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 상태 수가 많아야 하는데 무조건 존슨 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)를 쓰는 설계
- [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화 상태를 대충 정하는 설계
- 해독 로직을 복잡하게 만들어 장점을 잃는 설계
- 타이밍 경합을 무시하고 순환만 보는 설계

기술사 관점에서는 존슨 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)를 "중간 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)" 회로가 아니라 "제어용 순환 상태기계"로 봐야 한다. 목적이 분명하면 충분히 강력하다.

- **📢 섹션 요약 비유**: 적당한 크기의 회전판이 있으면 너무 작지도, 너무 복잡하지도 않게 순서를 돌릴 수 있다.

---

## Ⅴ. 기대효과 및 결론

존슨 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)는 순환 상태를 적당한 비용으로 늘려 주는 실용적인 회로다. 그래서 단순 제어와 표시 패턴에서 자주 활용된다.

결국 핵심은 "적은 회로로 얼마나 규칙적인 순서를 만들 수 있는가"다.

- **📢 섹션 요약 비유**: 같은 바퀴를 조금 다르게 굴리면 더 다양한 패턴이 나온다.

---

## 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Shift Register</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Inverted Feedback</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Johnson Counter</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">2n State Sequence</div>
</div>
</div>



---

## 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Ring Counter</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Johnson Counter</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Sequence Generator</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Timing Control</div>
</div>
</div>



---

## 어린이를 위한 3줄 비유 설명

카드를 뒤집어서 다시 돌리면 다른 순서가 생겨요.  
존슨 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)는 그런 식으로 순서를 더 많이 만들어요.  
그래서 작은 회로로 여러 단계를 만들 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 64 / 803

← **이전**: [63. 링 카운터 (Ring Counter)](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/063_ring_counter/)
**다음**: [65. 상태도 (State Diagram)](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/065_state_diagram/) →

---
