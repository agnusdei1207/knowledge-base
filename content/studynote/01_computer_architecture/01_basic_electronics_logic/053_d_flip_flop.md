+++
title = "53. D 플립플롭 (D Flip-Flop)"
date = 2026-05-01

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: D 플립플롭 (D Flip-Flop)은 클록 엣지에서 입력 D를 1비트 상태로 저장하는 동기식 순차회로다. S/R 플립플롭의 금지 상태를 완전히 제거하고, 단 하나의 입력(D)으로 명확한 동작을 보장한다.
> 2. **가치**: S/R 플립플롭의 금지 상태를 없애고, 레지스터와 파이프라인의 기본 저장 소자가 된다. 현대 CPU의 레지스터 파일, 파이프라인 버퍼, 캐시 제어 회로의 핵심 블록이다.
> 3. **판단 포인트**: setup time(설정 시간)과 hold time(유지 시간)을 지키지 않으면 metastability(준안정)가 발생할 수 있다. 타이밍 마진 설계가 D 플립플롭 활용의 핵심이다.

---

## Ⅰ. 개요 및 필요성

디지털 순차 논리 회로의 핵심은 "이전 상태를 기억하는 것"이다. 조합 논리 회로는 현재 입력만으로 출력을 결정하지만, 순차 논리 회로는 과거 상태까지 고려해야 한다. 이 "기억"을 담당하는 소자 중 가장 널리 사용되는 것이 D 플립플롭이다.

S/R(Set-Reset) 플립플롭은 논리 회로에서 가장 먼저 개발된 순차 소자지만, S=1, R=1 입력에서 출력이 정의되지 않는 "금지 상태(Forbidden State)"가 존재한다. 이 문제를 해결하기 위해 S/R 입력 앞에 NOT 게이트를 추가하여 D=1이면 S=1, R=0, D=0이면 S=0, R=1이 되도록 한 것이 D 래치(D Latch)다. 여기에 클록 엣지(Edge) 트리거 방식을 적용한 것이 D 플립플롭이다.

D 플립플롭이 중요한 이유는 "언제 값을 저장하는가"가 명확하기 때문이다. 클록의 특정 엣지(상승 또는 하강)에서만 입력 D를 샘플링하고, 나머지 시간에는 이전 상태를 유지한다. 이 특성 덕분에 동기식 디지털 시스템에서 모든 플립플롭이 동일한 기준 시점에 상태를 갱신할 수 있다.

현대 CPU의 레지스터 파일(Register File)은 수십~수백 개의 D 플립플롭으로 구성되며, 파이프라인 단계 사이의 데이터 래치도 모두 D 플립플롭이다. DRAM이 동적으로 전하를 저장한다면, 플립플롭은 정적으로(Static) 전력이 공급되는 한 영구히 상태를 유지한다.

- **📢 섹션 요약 비유**: D 플립플롭은 사진을 셔터가 열리는 순간에만 찍는 카메라와 같다. 셔터가 닫혀 있는 동안은 아무리 피사체가 움직여도 사진에 반영되지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 내부 구조: 마스터-슬레이브 래치



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Master-Slave D 플립플롭 내부:</div>
<div class="kb-diagram-note">CLK=0: Master 투명(D→Qm), Slave 불투명(Qs 유지)</div>
<div class="kb-diagram-note">CLK=1: Master 불투명(Qm 유지), Slave 투명(Qm→Q)</div>
<div class="kb-diagram-note">CLK' CLK</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">D 래치 Master</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">D 래치 Slave</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">Q</div></div>
<div class="kb-diagram-note">Qm Qs</div>
<div class="kb-diagram-note">상승 엣지(↑) 트리거:</div>
<div class="kb-diagram-note">CLK: 0→1 전환 순간에 Master의 Qm이 Slave로 전달</div>
<div class="kb-diagram-note">→ D의 값이 Q에 반영됨</div>
</div>
</div>



### D 플립플롭 동작 특성

| 클록 상태 | D | Q(next) | 설명 |
| :---: | :---: | :---: | :--- |
| ↑ 엣지 | 0 | 0 | 클록 상승 엣지에 D=0 샘플링 |
| ↑ 엣지 | 1 | 1 | 클록 상승 엣지에 D=1 샘플링 |
| 비엣지 | X | 유지 | 엣지 외 시간에는 이전 값 유지 |

부울식: Q(t+1) = D(t) | (샘플링 엣지 시점의 D)

### CMOS D 플립플롭 구현



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">트랜스미션 게이트 기반 구현 (12T 구조):</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">D ──</div><div class="kb-diagram-node">TG1</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">인버터</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">TG2</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">인버터</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">Q</div></div>
<div class="kb-diagram-note">CLK' CLK</div>
<div class="kb-diagram-note">CLK=0: TG1 투명, TG2 불투명 (Master 투명, Slave 불투명)</div>
<div class="kb-diagram-note">CLK=1: TG1 불투명, TG2 투명 (Master 불투명, Slave 투명)</div>
<div class="kb-diagram-note">총 트랜지스터: 12T (일반 구현)</div>
<div class="kb-diagram-note">최적화: 약 8~10T (특수 래치 구조 사용)</div>
</div>
</div>



### 타이밍 파라미터

```text
핵심 타이밍 파라미터:

setup time (tsu): 클록 엣지 이전에 D가 안정적이어야 하는 최소 시간
hold time (th):   클록 엣지 이후에 D가 유지되어야 하는 최소 시간
propagation delay (tpd): 클록 엣지 후 Q 출력이 안정화되는 시간
clock-to-Q delay (tCQ): 클록 엣지 후 Q 출력까지의 지연

타이밍 조건:
  T_clk > tpd_logic + tCQ + tsu + tskew
  (클록 주기 > 조합논리 지연 + FF 지연 + 셋업 시간 + 클록 스큐)

위반 시 결과:
  Setup violation: Q가 올바른 D 값을 래치하지 못함
  Hold violation: Q 값이 불안정하게 바뀜
  → 모두 Metastability(준안정 상태) 초래
```

- **📢 섹션 요약 비유**: D 플립플롭은 문이 열리는 정확한 순간에만 물건을 넣는 우편함이다. 문이 닫히기 직전이나 직후에 넣으려 하면 물건이 끼여 불안정해진다.

---

## Ⅲ. 비교 및 연결

### 플립플롭·래치 비교

| 항목 | D 래치 | D 플립플롭 | S/R 플립플롭 | J-K 플립플롭 |
| :--- | :--- | :--- | :--- | :--- |
| **동작 방식** | 레벨 민감 | 엣지 트리거 | 조합 입력 기반 | 엣지 + 토글 |
| **금지 상태** | 없음 | 없음 | S=R=1 금지 | 없음 |
| **토글** | 불가 | 불가 | 불가 | J=K=1 가능 |
| **입력 수** | 1(D) + CLK | 1(D) + CLK | 2(S,R) + CLK | 2(J,K) + CLK |
| **투명성** | CLK 레벨 동안 | 없음 | 없음 | 없음 |
| **안정성** | 중간 | 높음 | 낮음 | 중간 |
| **활용** | 단순 저장 | 레지스터/파이프라인 | 학습용 기본 회로 | 카운터/상태기계 |
| **현대 CPU 사용** | 드물 | 매우 많음 | 거의 없음 | 드물 |

### D 플립플롭으로 다른 플립플롭 구현



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">T 플립플롭 → D 플립플롭으로 구현:</div>
<div class="kb-diagram-note">D = T XOR Q (현재 상태와 T를 XOR하여 D에 입력)</div>
<div class="kb-diagram-note">Q(next) = D = T ⊕ Q (T=1이면 반전, T=0이면 유지)</div>
<div class="kb-diagram-note">J-K 플립플롭 → D 플립플롭으로 구현:</div>
<div class="kb-diagram-note">D = J·Q' + K'·Q (J-K 특성표를 D로 변환)</div>
<div class="kb-diagram-note">D = J·Q' + K'·Q</div>
</div>
</div>



- **📢 섹션 요약 비유**: D 래치는 열린 자물쇠, D 플립플롭은 한 번만 찍는 스탬프, S/R 플립플롭은 규칙이 헷갈리는 옛날 자물쇠다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### CPU 레지스터 파일 구현

```text
32비트 RISC-V 레지스터 파일:
  - 32개의 32비트 레지스터
  - 각 레지스터 = 32개의 D 플립플롭
  - 총 플립플롭 수: 32 × 32 = 1,024개

동작:
  - 쓰기: Write Enable=1, 클록 엣지에서 D → Q 래치
  - 읽기: 멀티플렉서로 선택한 레지스터의 Q 출력
  - 파이프라인 스테이지 사이: 32비트 버스 전체를 D 플립플롭 뱅크로 래치
```

### 파이프라인 레지스터



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">5단계 파이프라인 (IF/ID/EX/MEM/WB):</div>
<div class="kb-diagram-note">IF → ID → EX → MEM → WB</div>
<div class="kb-diagram-note">↑각 단계 사이에 D 플립플롭 뱅크 배치↑</div>
<div class="kb-diagram-note">IF/ID 레지스터:</div>
<div class="kb-diagram-tree-item" style="--depth:1">다음 PC(32비트) + 명령어(32비트) = 64비트</div>
<div class="kb-diagram-tree-item" style="--depth:1">64개의 D 플립플롭으로 구성</div>
<div class="kb-diagram-tree-item" style="--depth:1">매 클록 엣지에 새 값 래치</div>
<div class="kb-diagram-note">파이프라인 플러시:</div>
<div class="kb-diagram-tree-item" style="--depth:1">Reset 입력으로 모든 D 플립플롭을 0으로 초기화</div>
<div class="kb-diagram-tree-item" style="--depth:1">브랜치 미스 예측 시 활용</div>
</div>
</div>



### 메타스태빌리티(Metastability) 처리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">메타스태빌리티 발생 원인:</div>
<div class="kb-diagram-tree-item" style="--depth:1">비동기 입력 신호가 D 플립플롭의 setup/hold 윈도우에 걸릴 때</div>
<div class="kb-diagram-tree-item" style="--depth:1">서로 다른 클록 도메인 간 데이터 전달 시</div>
<div class="kb-diagram-note">해결 방법: 2단 동기화기 (Double-Flop Synchronizer)</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">FF1</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">FF2</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">동기화된 출력</div></div>
<div class="kb-diagram-note">clk clk</div>
<div class="kb-diagram-note">FF1이 메타스태빌리티에 빠져도, FF2의 setup 윈도우까지</div>
<div class="kb-diagram-note">안정화될 확률이 매우 높아짐</div>
<div class="kb-diagram-note">MTBF (Mean Time Between Failures) 계산으로 설계 검증</div>
</div>
</div>



### 설계 판단 체크리스트

1. 클록 엣지 기준으로 입력이 안정적인가? (Setup time 만족)
2. 클록 엣지 후 입력이 충분히 유지되는가? (Hold time 만족)
3. 비동기 리셋이 안전하게 설계되었는가? (Reset 동기화)
4. 파이프라인 단계마다 타이밍 여유(Slack)가 있는가?
5. 다른 클록 도메인과의 인터페이스에 2단 동기화기가 있는가?
6. 메타스태빌리티 MTBF가 시스템 요구 수명보다 충분히 긴가?

### 안티패턴

- **Setup 바이올레이션 무시**: 빠른 클록 주파수를 위해 타이밍 마진을 지나치게 줄이면, 온도·전압 변동 시 setup violation이 발생하여 시스템 오동작이 생긴다. Static Timing Analysis(STA)로 모든 경로의 타이밍을 검증해야 한다.
- **비동기 리셋 남용**: 비동기 리셋은 클록과 무관하게 즉시 동작하므로, 글리치에 취약하다. 글리치로 인한 의도치 않은 리셋이 발생할 수 있다. 동기식 리셋(클록 엣지에서만 리셋)이 더 안전하다.
- **래치와 플립플롭 혼용**: EDA 합성 도구에서 완전한 if-else 없는 조건문은 래치를 합성할 수 있다. 의도치 않은 래치 생성은 타이밍 분석을 복잡하게 하므로, HDL 코딩 시 명시적으로 래치/플립플롭을 구분해야 한다.

- **📢 섹션 요약 비유**: D 플립플롭은 신호등이 초록불로 바뀌는 순간에만 차를 보내는 교차로다. 초록불 직전이나 직후에 무리하게 진입하면 사고가 난다.

---

## Ⅴ. 기대효과 및 결론

D 플립플롭은 디지털 시스템의 기본 기억 단위다. 안정적이고 예측 가능하며, 동기식 회로 설계의 출발점이다. 현대 CPU, GPU, FPGA, ASIC 등 모든 디지털 시스템에서 수천만~수억 개의 D 플립플롭이 동기식 클록에 맞춰 동작한다.

| 기대효과 | 내용 |
|:---|:---|
| **동기식 설계 표준** | 모든 상태 변경이 클록 엣지에서만 발생 |
| **타이밍 예측성** | Setup/Hold 조건으로 동작 시점 완전 제어 |
| **메타스태빌리티 관리** | 2단 동기화기로 비동기 입력 안전 처리 |
| **고집적화** | 12T CMOS로 소면적 구현 가능 |
| **파이프라인 기반** | 현대 CPU 파이프라인의 기본 단계 구분 소자 |

미래 컴퓨팅에서도 D 플립플롭의 역할은 지속된다. 3D 적층 칩(3D-IC)에서 레이어 간 데이터 전달에도 플립플롭이 필요하고, 뉴로모픽 칩에서 스파이킹 뉴런의 발화 상태도 플립플롭으로 구현된다. 클록 속도가 GHz에서 수십 GHz로 올라갈수록 플립플롭의 타이밍 특성(Setup/Hold/tCQ)이 성능의 핵심 제약이 된다.

- **📢 섹션 요약 비유**: D 플립플롭은 매 순간 적는 메모장이 아니라, 종이 울릴 때만 적는 출석부다. 체계적인 기록이 가능하고, 나중에도 정확하게 조회할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **D 래치** | 레벨 민감 저장소 (D FF의 전신) |
| **S/R 플립플롭** | 금지 상태 존재 → D FF로 개선 |
| **setup/hold time** | 안전한 샘플링을 위한 타이밍 조건 |
| **metastability** | 타이밍 위반 시 불안정 상태 |
| **FSM (유한 상태 기계)** | D FF로 상태 저장 |
| **레지스터** | D FF 배열로 구성 |
| **파이프라인 버퍼** | 단계 사이 D FF 뱅크 |
| **2단 동기화기** | 비동기 입력 안전 처리 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">S/R 플립플롭 (금지 상태 존재)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">D 래치 (레벨 민감, S/R 금지 상태 해결)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">D 플립플롭 (엣지 트리거, 금지 상태 없음)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">레지스터 (D FF 배열, CPU 레지스터 파일)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">파이프라인 버퍼 (단계 간 데이터 래치)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">동기식 SRAM (D FF 기반 정적 메모리 셀)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">현대 CPU (수억 개의 D FF가 동기적으로 동작)</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. D 플립플롭은 종이 울릴 때만 선생님이 이름을 적는 출석부예요.
2. 종이 울리기 전에는 이름이 바뀌어도 적지 않아요.
3. 그래서 모두 같은 순간에 맞춰 규칙적으로 기록할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 53 / 803

← **이전**: [52. SR 플립플롭 (Set-Reset Flip-Flop)](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/052_sr_flip_flop/)
**다음**: [54. J-K 플립플롭 (J-K Flip-Flop)](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/054_jk_flip_flop/) →

---
