+++
title = "56. 마스터-슬레이브 플립플롭 (Master-Slave Flip-Flop)"
date = 2026-05-01

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 마스터-슬레이브 플립플롭은 두 개의 래치를 직렬로 연결하되, 서로 반대 위상의 클록으로 제어함으로써 엣지 트리거처럼 동작하게 한 구조다. 한 래치가 열릴 때 다른 래치는 닫혀 있어 데이터 경로가 한 방향으로만 흐른다.
> 2. **가치**: 레벨 민감 래치의 투명 구간 문제와 J-K 플립플롭의 race-around 문제를 구조적으로 해결한다. 현대 edge-triggered 플립플롭의 이론적 기반이 되며, 클록 반주기씩 역할을 분리하는 핵심 아이디어다.
> 3. **판단 포인트**: 클록의 전/후반 구간 역할 분리가 핵심이다. Master는 CLK=0 구간에 입력을 받고, Slave는 CLK=1 구간에 출력을 반영한다(또는 반대로 설계 가능). 두 래치가 절대로 동시에 열리면 안 된다.

---

## Ⅰ. 개요 및 필요성

래치(Latch)는 클록이 활성화된 레벨 동안 입력이 출력에 그대로 전달되는 "투명(Transparent)" 특성을 가진다. 이는 클록이 활성화된 동안 입력 신호의 변화가 즉시 출력에 반영되어, 타이밍 제어가 어려워지는 문제를 야기한다.

특히 J-K 플립플롭에서 J=K=1 상태에서 클록이 1로 유지되면, 출력 Q가 반전 → 피드백 → 다시 반전 → ... 의 무한 루프(race-around)가 발생한다. 이 문제를 해결하기 위해 1950년대에 마스터-슬레이브(Master-Slave) 구조가 고안되었다.

마스터-슬레이브 구조의 핵심 아이디어는 단순하다: 입력을 받는 마스터(Master)와 출력을 반영하는 슬레이브(Slave)를 시간적으로 분리하는 것이다. 마스터가 열려 있을 때 슬레이브는 잠겨 있고, 슬레이브가 열릴 때 마스터는 잠긴다. 이렇게 하면 입력에서 출력까지 경로가 동시에 열리는 경우가 없어지고, 전체적으로 클록 엣지에서만 상태가 변경되는 것처럼 동작한다.

이 구조는 이후 트랜스미션 게이트 기반 엣지 트리거 플립플롭의 개념적 기반이 되었으며, 오늘날 모든 D 플립플롭 구현의 기초다.

- **📢 섹션 요약 비유**: 마스터-슬레이브는 에어락(Airlock, 우주선의 이중 문)이다. 외부 문(마스터)이 열릴 때 내부 문(슬레이브)은 반드시 닫혀 있고, 내부 문이 열릴 때 외부 문은 반드시 닫혀 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 마스터-슬레이브 구조 다이어그램



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">구조:</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">Master Latch</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">Slave Latch</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">출력 Q</div></div>
<div class="kb-diagram-note">CLK'(반전) CLK</div>
<div class="kb-diagram-note">CLK=0 (마스터 활성화):</div>
<div class="kb-diagram-note">Master: 투명 (D → Qm 통과)</div>
<div class="kb-diagram-note">Slave: 불투명 (Q 유지)</div>
<div class="kb-diagram-note">CLK=1 (슬레이브 활성화):</div>
<div class="kb-diagram-note">Master: 불투명 (Qm 유지)</div>
<div class="kb-diagram-note">Slave: 투명 (Qm → Q 통과)</div>
<div class="kb-diagram-note">결과:</div>
<div class="kb-diagram-note">CLK의 하강 엣지(1→0) 직전까지의 D 값이 Qm에 저장</div>
<div class="kb-diagram-note">CLK의 상승 엣지(0→1)에서 Qm이 Q로 전달</div>
<div class="kb-diagram-note">→ 전체적으로 하강 엣지에서 래치, 상승 엣지에서 출력하는 동작</div>
<div class="kb-diagram-note">(구현에 따라 반대로도 가능)</div>
</div>
</div>



### Race-Around 억제 원리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Race-Around 억제 메커니즘:</div>
<div class="kb-diagram-note">1. J-K 마스터-슬레이브 FF에서:</div>
<div class="kb-diagram-note">CLK=0: Master 열림 (J,K 입력 반영 → Qm 변경)</div>
<div class="kb-diagram-note">CLK=1: Slave 열림 (Qm → Q 반영)</div>
<div class="kb-diagram-note">Master 닫힘 (Q 변경이 J-K 게이트에 피드백되어도 마스터 차단)</div>
<div class="kb-diagram-note">2. Race-Around 억제:</div>
<div class="kb-diagram-note">CLK=1 구간: Master 닫힘 → Q 변경이 Master에 들어오더라도 Qm 불변</div>
<div class="kb-diagram-note">→ Q의 변화가 J-K 게이트를 통해 다시 Qm을 바꾸는 경로 차단</div>
<div class="kb-diagram-note">→ 무한 토글 불가</div>
</div>
</div>



### 마스터-슬레이브 D 플립플롭 진리표

| CLK | D | 동작 | Q(next) |
| :---: | :---: | :--- | :---: |
| 0→1 (↑) | 0 | 슬레이브 열림, 마스터 닫힘 직전의 Qm=D 전달 | 0 |
| 0→1 (↑) | 1 | 슬레이브 열림, 마스터 닫힘 직전의 Qm=D 전달 | 1 |
| 1→0 (↓) | X | 마스터 열림, 슬레이브 닫힘 | 유지 |
| 안정 0 | X | 마스터 투명, Qm 변함 | Qm 변경 중 |
| 안정 1 | X | 슬레이브 투명, Q 안정 | 이전 Qm 유지 |

### CMOS 트랜스미션 게이트 구현



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">마스터-슬레이브 D FF (트랜스미션 게이트 기반):</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">D ──</div><div class="kb-diagram-node">TG1</div><div class="kb-diagram-note">──</div><div class="kb-diagram-node">INV1</div><div class="kb-diagram-note">──</div><div class="kb-diagram-node">TG2</div><div class="kb-diagram-note">──</div><div class="kb-diagram-node">INV2</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">Q</div></div>
<div class="kb-diagram-note">CLK' │ CLK</div>
<div class="kb-diagram-tree-item" style="--depth:7">(피드백, 래치 형성)</div>
<div class="kb-diagram-note">TG1(마스터): CLK=0 시 ON (입력 샘플링)</div>
<div class="kb-diagram-note">TG2(슬레이브): CLK=1 시 ON (출력 전달)</div>
<div class="kb-diagram-note">트랜지스터 수: TG1(2T) + INV1(2T) + TG2(2T) + INV2(2T) = 8T (최소)</div>
<div class="kb-diagram-note">실제 구현: 12~16T (리셋/셋 포함)</div>
</div>
</div>



- **📢 섹션 요약 비유**: 마스터는 메모하고(CLK=0에 D 저장), 슬레이브는 발표하는(CLK=1에 Q 출력) 역할이다. 두 역할이 동시에 일어나지 않아 값이 중간에 흔들리지 않는다.

---

## Ⅲ. 비교 및 연결

### 래치 vs 마스터-슬레이브 vs 에지 트리거 비교

| 항목 | D 래치 | 마스터-슬레이브 FF | 엣지 트리거 D FF |
| :--- | :--- | :--- | :--- |
| **동작 방식** | 레벨 민감 | 유사 엣지 | 완전 엣지 |
| **투명 구간** | CLK=1 전체 | 없음 (사실상) | 없음 |
| **Race-around** | 가능 | 억제 | 없음 |
| **클록 구간** | 1개 | 2개 (반주기씩) | 엣지 순간 |
| **복잡도** | 낮음 | 중간 | 중간~높음 |
| **Setup/Hold** | 간단 | 복잡 | 표준화됨 |
| **현대 활용도** | 낮음 | 학습용 | 매우 높음 |

### 마스터-슬레이브 구조의 한계



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">마스터-슬레이브의 1-to-0 Catching 문제:</div>
<div class="kb-diagram-note">CLK=0 (마스터 활성):</div>
<div class="kb-diagram-note">입력 D가 1이었다가 0으로 바뀌면 Qm = 0</div>
<div class="kb-diagram-note">이후 CLK=1에서 Q = 0 (원래 의도와 다를 수 있음)</div>
<div class="kb-diagram-note">문제: CLK=0 구간 동안 D의 마지막 값이 아닌 중간값이 래치될 수 있음</div>
<div class="kb-diagram-note">→ 글리치(Glitch)에 취약</div>
<div class="kb-diagram-note">해결: 완전한 엣지 트리거 구조가 필요</div>
<div class="kb-diagram-note">→ 마스터-슬레이브는 이론적 중간 단계로 이해</div>
</div>
</div>



- **📢 섹션 요약 비유**: 래치는 열린 창문, 마스터-슬레이브는 번갈아 여는 이중문, 엣지 트리거는 딱 한 순간만 열리는 고속 셔터다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 마스터-슬레이브 J-K 플립플롭 구현



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">마스터-슬레이브 J-K 플립플롭:</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">J ──</div><div class="kb-diagram-node">AND</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">Q → 피드백</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">SR-Master</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">SR-Slave</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">Q</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">K ──</div><div class="kb-diagram-node">AND</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">Q' → 피드백</div></div>
<div class="kb-diagram-note">CLK=0: Master SR 래치 활성 (J,K 입력 처리)</div>
<div class="kb-diagram-note">CLK=1: Slave SR 래치 활성 (Master 출력 반영)</div>
<div class="kb-diagram-note">Race-around 억제:</div>
<div class="kb-diagram-note">CLK=1에서 Slave 활성 → Q 변경</div>
<div class="kb-diagram-note">→ Q 변경이 J,K AND 게이트로 피드백되어도 Master 닫혀 있음</div>
<div class="kb-diagram-note">→ 무한 토글 방지</div>
</div>
</div>



### 현대 CMOS D 플립플롭과의 관계

```text
마스터-슬레이브 → 현대 엣지 트리거 발전 과정:

1. 마스터-슬레이브: CLK 반주기 분리 (1950~1960s)
2. CMOS 트랜스미션 게이트 FF: 8~12T 최적화 (1970s~)
3. C2MOS (Clocked CMOS): 전력 최적화 (1980s~)
4. 완전 정적 CMOS D FF: 현재 표준 (~12T)

공통점: 모두 마스터-슬레이브 개념에서 출발
차이점: 물리 구현의 최적화 방식
```

### 설계 판단 체크리스트

1. 두 래치가 동시에 열리지 않는가? (클록 위상 분리 확인)
2. race-around가 억제되는가? (J-K 마스터-슬레이브에서 특히 중요)
3. 1-to-0 catching 문제가 설계에 영향을 주는가? (필요 시 엣지 트리거로 교체)
4. 클록 위상 반전(INV) 게이트의 지연이 타이밍에 영향을 주는가?
5. 현대 설계에서는 엣지 트리거 FF 사용이 더 적합한지 검토했는가?

### 안티패턴

- **클록 위상 분리 무시**: 마스터와 슬레이브에 같은 위상의 클록을 연결하면 두 래치가 동시에 열려 단순한 레벨 래치와 동일해진다. 반드시 NOT 게이트로 반전된 클록을 사용해야 한다.
- **동시 투명 구간 발생**: 클록 신호의 글리치(Glitch)로 인해 CLK와 CLK'가 동시에 활성화되는 순간이 생기면 마스터와 슬레이브가 동시에 열려 데이터가 직통으로 통과한다. 클록 회로의 노이즈 억제가 필요하다.
- **래치와 플립플롭 혼동**: 마스터-슬레이브 구조가 엣지 트리거처럼 동작하지만, 완전한 엣지 트리거 플립플롭과는 다르다. 1-to-0 catching 문제가 있으므로 시스템 요구사항을 정확히 파악해야 한다.

- **📢 섹션 요약 비유**: 마스터-슬레이브는 교대 근무로 문을 지키는 경비원이다. 아침 경비원(마스터)이 오전에 방문자를 받아두고, 오후 경비원(슬레이브)이 그 목록을 공식 기록에 올린다.

---

## Ⅴ. 기대효과 및 결론

마스터-슬레이브 플립플롭은 레벨 민감 래치의 투명 문제와 J-K 플립플롭의 race-around 문제를 해결한 중요한 설계 기법이다. 현대 엣지 트리거 플립플롭의 이론적 기반이며, 클록 위상 분리라는 핵심 아이디어는 여전히 유효하다.

| 기대효과 | 내용 |
|:---|:---|
| **Race-Around 억제** | J-K FF의 무한 토글 문제 구조적 해결 |
| **엣지 트리거 기반** | 현대 D FF의 개념적 원형 |
| **타이밍 분리** | 클록 반주기씩 역할 분리 |
| **안정성 향상** | 레벨 래치보다 예측 가능한 동작 |
| **교육적 가치** | 엣지 트리거의 원리를 설명하는 핵심 구조 |

현대 ASIC과 FPGA 설계에서는 완전한 엣지 트리거 플립플롭이 표준이지만, 마스터-슬레이브 개념은 다양한 형태로 살아있다. 예를 들어, 멀티-사이클 경로(Multi-Cycle Path)와 이중 클록 도메인 교차(Clock Domain Crossing) 처리에서 마스터-슬레이브 원리가 적용된다. 기술사 시험에서는 래치→마스터-슬레이브→엣지 트리거의 발전 과정을 설명하는 문제가 자주 출제된다.

- **📢 섹션 요약 비유**: 마스터-슬레이브는 한 사람이 쓰고 나면 다른 사람이 마무리하는 접이식 작업대다. 한 쪽이 열리면 다른 쪽은 닫혀 있어야 작업이 꼬이지 않는다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **D 래치** | 마스터-슬레이브의 기본 블록 |
| **엣지 트리거** | 마스터-슬레이브의 발전형 |
| **Race-Around** | J-K FF에서 마스터-슬레이브로 해결 |
| **Setup/Hold Time** | 마스터-슬레이브 타이밍 조건 |
| **D 플립플롭** | 마스터-슬레이브의 현대 구현 |
| **클록 위상** | CLK와 CLK' 분리 설계 |
| **1-to-0 Catching** | 마스터-슬레이브의 한계 |
| **트랜스미션 게이트** | CMOS 마스터-슬레이브 구현 소자 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">D 래치 (레벨 민감, 투명 구간)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">마스터-슬레이브 D FF (클록 반주기 분리, Race-Around 억제)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">트랜스미션 게이트 D FF (CMOS 최적화, 8~12T)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">엣지 트리거 D FF (완전 엣지 동작, 현재 표준)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">현대 CMOS D FF (Static, 12T 표준)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">현대 CPU의 레지스터, 파이프라인 버퍼</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 마스터는 먼저 적고(CLK=0에 입력 저장), 슬레이브는 나중에 보여줘요(CLK=1에 출력).
2. 둘이 동시에 열리지 않아서 값이 헷갈리지 않아요.
3. 이 구조가 컴퓨터의 모든 플립플롭이 안정적으로 동작하는 비결이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 56 / 803

← **이전**: [55. T 플립플롭 (T Flip-Flop)](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/055_t_flip_flop/)
**다음**: [57. 레지스터 (Register)](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) →

---
