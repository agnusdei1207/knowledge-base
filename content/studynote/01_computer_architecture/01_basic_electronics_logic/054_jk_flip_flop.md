+++
title = "54. J-K 플립플롭 (J-K Flip-Flop)"
date = 2026-05-01

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: J-K 플립플롭 (J-K Flip-Flop)은 S/R 플립플롭의 금지 상태(S=R=1)를 해결한 순차회로다. J=K=1일 때 현재 상태를 반전(Toggle)하는 추가 동작이 가능하여, 모든 4가지 입력 조합에 대해 명확한 출력이 정의된다.
> 2. **가치**: J=1, K=1일 때 toggle(토글) 동작이 가능해 카운터와 제어회로에 유용하다. T 플립플롭은 J-K 플립플롭의 J=K 입력을 묶은 특수한 경우이며, D 플립플롭도 J=D, K=D'로 변환하여 구현 가능하다.
> 3. **판단 포인트**: 레벨 트리거 구조에서는 race-around(레이스 어라운드) 문제가 생길 수 있어 edge-triggered 설계가 중요하다. J=K=1 상태를 장시간 허용하면 안 된다.

---

## Ⅰ. 개요 및 필요성

S/R 플립플롭은 1940년대 디지털 회로 설계 초기부터 사용된 기본 순차 소자다. 그러나 S=1, R=1 입력에서 출력 Q와 Q'가 모두 1이 되는 "금지 상태(Forbidden State)"가 존재한다는 치명적 약점이 있다. 이 상태에서 S, R이 동시에 0으로 바뀌면 출력이 예측 불가능해진다.

J-K 플립플롭은 이 문제를 해결하기 위해 1954년 Jack Kilby가 개발에 참여하면서 체계화된 구조다(일부 문헌에서는 발명자 불명, "J"와 "K"가 특정 의미 없는 레이블이라는 설도 있다). 핵심 변경점은 J=K=1 입력에서 출력이 현재 상태의 반전(Toggle)이 되도록 피드백 연결을 추가한 것이다.

이 토글 특성 덕분에 J-K 플립플롭은 단순한 저장 소자를 넘어, 카운터 설계의 핵심 블록으로 자리잡았다. 특히 비동기 카운터(Ripple Counter)에서 각 자리의 플립플롭을 J-K로 구성하면, J=K=1 고정으로 매 클록마다 토글하는 1비트 카운터를 쉽게 구성할 수 있다.

- **📢 섹션 요약 비유**: J-K 플립플롭은 두 개의 스위치로 켜기, 끄기, 유지, 반전까지 할 수 있는 만능 스위치다. S/R의 "두 스위치 동시 켬" 오동작 문제를 "토글"이라는 의미 있는 동작으로 해결했다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### J-K 플립플롭 동작표

| J | K | Q(next) | 설명 |
| :---: | :---: | :---: | :--- |
| 0 | 0 | Q (유지) | 현재 상태 유지 |
| 0 | 1 | 0 (reset) | 강제로 0 |
| 1 | 0 | 1 (set) | 강제로 1 |
| 1 | 1 | Q' (toggle) | 현재 상태 반전 |

### 내부 구조와 피드백



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">J-K 플립플롭 내부 (NAND 게이트 기반 SR FF + 피드백):</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">J ──</div><div class="kb-diagram-node">AND</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">SR FF</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">Q</div></div>
<div class="kb-diagram-note">↑ → 피드백 (Q를 K측 AND에 연결)</div>
<div class="kb-diagram-note">Q' (현재 상태)</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">K ──</div><div class="kb-diagram-node">AND</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">R</div></div>
<div class="kb-diagram-connector">↑</div>
<div class="kb-diagram-note">Q (현재 상태)</div>
<div class="kb-diagram-note">J=1, K=1 시:</div>
<div class="kb-diagram-note">S게이트 입력 = J AND Q' = 1 AND Q'</div>
<div class="kb-diagram-note">R게이트 입력 = K AND Q = 1 AND Q</div>
<div class="kb-diagram-note">Q=0이면: S=1, R=0 → Q(next)=1 (토글!)</div>
<div class="kb-diagram-note">Q=1이면: S=0, R=1 → Q(next)=0 (토글!)</div>
</div>
</div>



### Race-Around 문제



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Race-Around 발생 조건:</div>
<div class="kb-diagram-note">레벨 트리거 J-K FF + J=K=1 + 클록=1 유지 시</div>
<div class="kb-diagram-note">문제 과정:</div>
<div class="kb-diagram-note">CLK=1: Q 토글 → Q 변경 → 피드백 → 다시 토글 → 무한 토글</div>
<div class="kb-diagram-note">→ 클록이 1인 동안 Q가 여러 번 반전 → 예측 불가능</div>
<div class="kb-diagram-note">해결:</div>
<div class="kb-diagram-note">1. Edge-triggered (엣지 트리거): 클록 엣지에서만 샘플링</div>
<div class="kb-diagram-note">2. Master-Slave J-K FF: 클록 반주기로 시간 분리</div>
<div class="kb-diagram-note">3. 펄스 폭 제한: CLK 펄스를 FF의 전파 지연보다 짧게 설정</div>
</div>
</div>



- **📢 섹션 요약 비유**: J-K 플립플롭은 엘리베이터의 올라가기/내려가기/정지/반전 버튼을 한 몸에 넣은 장치다. 단, 올라가기+내려가기를 동시에 너무 오래 누르면 오동작한다(race-around).

---

## Ⅲ. 비교 및 연결

### 4종 플립플롭 특성 비교

| 항목 | S/R | D | J-K | T |
| :--- | :--- | :--- | :--- | :--- |
| **금지 상태** | S=R=1 금지 | 없음 | 없음 | 없음 |
| **토글** | 불가 | 불가 | J=K=1 가능 | T=1 항상 |
| **입력 수** | 2 (S, R) | 1 (D) | 2 (J, K) | 1 (T) |
| **복잡도** | 낮음 | 낮음 | 중간 | 낮음 |
| **활용** | 기본 | 레지스터 | 카운터/FSM | 카운터 |
| **관계** | 기본형 | 개선형 | 범용형 | JK 특수형 |

### J-K로 다른 플립플롭 구현



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">T 플립플롭 구현 (J=K=T):</div>
<div class="kb-diagram-note">J=T, K=T 연결 → T=1이면 J=K=1 → 토글</div>
<div class="kb-diagram-note">T=0이면 J=K=0 → 유지</div>
<div class="kb-diagram-note">D 플립플롭 구현 (J=D, K=D'):</div>
<div class="kb-diagram-note">J=D, K=NOT(D) 연결</div>
<div class="kb-diagram-note">D=1: J=1, K=0 → Set → Q=1</div>
<div class="kb-diagram-note">D=0: J=0, K=1 → Reset → Q=0</div>
<div class="kb-diagram-note">→ D 플립플롭과 동일 동작</div>
<div class="kb-diagram-note">카운터 구성 (J=K=1 고정):</div>
<div class="kb-diagram-note">매 클록마다 토글 → 2분주기(주파수 절반) 동작</div>
<div class="kb-diagram-note">n개 직렬 → n비트 비동기 바이너리 카운터</div>
</div>
</div>



- **📢 섹션 요약 비유**: J-K는 D보다 다재다능하지만, 운전이 조금 더 까다로운 자동차다. T 플립플롭은 J-K의 "항상 반전 모드"만 쓰는 단순화 버전이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 비동기 카운터 설계 (J-K 활용)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">4비트 비동기 카운터:</div>
<div class="kb-diagram-note">CLK(외부)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">JK-FF0</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">JK-FF1</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">JK-FF2</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">JK-FF3</div></div>
<div class="kb-diagram-note">Q0(LSB) Q1 Q2 Q3(MSB)</div>
<div class="kb-diagram-note">CLK0=CLK CLK1=Q0 CLK2=Q1 CLK3=Q2</div>
<div class="kb-diagram-note">동작: Q0이 토글할 때마다 Q1 토글, Q1이 토글할 때마다 Q2 토글...</div>
<div class="kb-diagram-note">결과: 0000 → 0001 → 0010 → 0011 → ... → 1111 → 0000</div>
<div class="kb-diagram-note">단점: 각 FF의 지연이 누적 → 비동기 ripple 지연</div>
</div>
</div>



### 동기 카운터에서 J-K 역할



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">동기 2비트 카운터 (J-K 입력 논리 설계):</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Q1 Q0</div><div class="kb-diagram-cell">Q1(next) Q0(next)</div><div class="kb-diagram-cell">J1 K1</div><div class="kb-diagram-cell">J0 K0</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">0 0</div><div class="kb-diagram-cell">0 1</div><div class="kb-diagram-cell">0 X</div><div class="kb-diagram-cell">1 X</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">0 1</div><div class="kb-diagram-cell">1 0</div><div class="kb-diagram-cell">1 X</div><div class="kb-diagram-cell">X 1</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1 0</div><div class="kb-diagram-cell">1 1</div><div class="kb-diagram-cell">X 0</div><div class="kb-diagram-cell">1 X</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1 1</div><div class="kb-diagram-cell">0 0</div><div class="kb-diagram-cell">X 1</div><div class="kb-diagram-cell">X 1</div></div>
<div class="kb-diagram-note">해석:</div>
<div class="kb-diagram-note">J0 = 1 (항상), K0 = 1 (항상) → Q0는 항상 토글</div>
<div class="kb-diagram-note">J1 = Q0, K1 = Q0 → Q0=1일 때만 Q1 토글</div>
</div>
</div>



### 설계 판단 체크리스트

1. toggle 동작이 필요한 카운터 설계인가? J-K 또는 T 플립플롭 선택
2. level-triggered race-around를 피했는가? edge-triggered 구현 확인
3. setup/hold 조건을 만족하는가?
4. 비동기 preset/clear가 안전한가? (글리치 방지)
5. 카운터 연결 시 동기/비동기 방식을 선택했는가?
6. D 플립플롭으로 충분한데 굳이 J-K를 쓰는 건 아닌가?

### 안티패턴

- **J=K=1을 장시간 허용**: 레벨 트리거 구조에서 J=K=1 상태가 CLK 활성 구간 동안 유지되면 race-around가 발생한다. 반드시 엣지 트리거 또는 마스터-슬레이브 구조를 사용해야 한다.
- **D 플립플롭으로 충분한데 J-K 사용**: 단순한 데이터 저장에 J-K 플립플롭을 사용하면 불필요한 복잡성이 추가된다. J=D, K=D'로 연결해야 하는 번거로움이 생기며, 게이트 수도 증가한다.
- **클록 폭 고려 미흡**: 레벨 트리거 J-K에서 CLK 펄스 폭이 전파 지연보다 길면 race-around가 발생한다. 플립플롭의 최대 클록 펄스 폭(tWH) 명세를 반드시 확인해야 한다.

- **📢 섹션 요약 비유**: J-K 플립플롭은 반전까지 되는 만능 리모컨이지만, 버튼이 많아 헷갈릴 수 있다. race-around는 두 버튼을 동시에 오래 누르는 실수와 같다.

---

## Ⅴ. 기대효과 및 결론

J-K 플립플롭은 카운터와 제어회로에서 중요한 역할을 한다. S/R 플립플롭보다 안전하고, 토글 기능으로 동작 범위가 넓다. T 플립플롭과 D 플립플롭 모두 J-K 플립플롭의 특수화로 볼 수 있으므로, J-K를 이해하면 모든 플립플롭 유형을 체계적으로 파악할 수 있다.

| 기대효과 | 내용 |
|:---|:---|
| **금지 상태 해결** | S/R의 S=R=1 문제를 토글로 의미화 |
| **카운터 설계** | J=K=1 고정으로 자연스러운 2분주기 |
| **범용성** | T, D 플립플롭으로 변환 가능 |
| **FSM 구현** | set/reset/toggle 모두 지원 |
| **교육적 가치** | 모든 플립플롭 유형 이해의 중심 |

FPGA 설계에서는 D 플립플롭이 기본 셀로 사용되지만, 논리 합성 도구가 자동으로 카운터 설계를 J-K 의미론으로 최적화하여 D 플립플롭에 매핑한다. 결국 J-K의 개념은 추상적 수준에서 카운터 설계를 이해하는 데 필수적이다.

- **📢 섹션 요약 비유**: J-K 플립플롭은 하나의 스위치로 불을 켰다 껐다 하는 현관 전등이다. 단순히 켜고 끄는 것을 넘어, 한 번만 눌러도 상태가 자동으로 반전된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **S/R 플립플롭** | 금지 상태 해결 → J-K 탄생 |
| **D 플립플롭** | J=D, K=D'로 J-K 구현 |
| **T 플립플롭** | J=K=T인 J-K 특수형 |
| **Race-Around** | J=K=1 레벨 트리거 위험 |
| **카운터** | J=K=1 고정 → 비동기 카운터 |
| **FSM** | set/reset/toggle로 상태 전이 |
| **마스터-슬레이브** | Race-Around 해결 구조 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">S/R 플립플롭 (금지 상태 S=R=1 존재)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">J-K 플립플롭 (피드백으로 토글 동작 추가, 금지 상태 해결)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">마스터-슬레이브 J-K (Race-Around 억제)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Edge-Triggered J-K (엣지에서만 동작, 완전한 안정화)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">T 플립플롭 (J-K의 특수형, 카운터 특화)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">비동기 카운터 (J-K 직렬 연결 + J=K=1)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">동기 카운터 (J-K 조합 논리로 입력 제어)</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. J-K 플립플롭은 두 버튼으로 켜고 끄고 뒤집을 수 있는 장난감이에요.
2. 버튼을 오래 누르면 헷갈릴 수 있어서, 딱 한 번만 눌러야 해요(race-around 주의).
3. 그래서 규칙에 맞게 쓰면 숫자를 세는 카운터에 아주 좋아요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 54 / 803

← **이전**: [53. D 플립플롭 (D Flip-Flop)](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/053_d_flip_flop/)
**다음**: [55. T 플립플롭 (T Flip-Flop)](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/055_t_flip_flop/) →

---
