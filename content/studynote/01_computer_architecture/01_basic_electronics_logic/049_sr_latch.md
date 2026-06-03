+++
title = "049. SR 래치 — SR Latch"
date = 2026-04-05

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

> **핵심 인사이트**
> 1. SR 래치(Set-Reset [Latch](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/048_latch/))는 디지털 회로의 가장 기본적인 기억 소자 — NOR 또는 NAND 게이트 2개의 교차 결합(Cross-Coupling)으로 이전 상태를 유지하는 피드백 루프를 형성하며, 모든 [플립플롭](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/051_flip_flop/)과 메모리의 근간이다.
> 2. 출력이 입력으로 피드백되는 순차 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)([Sequential Logic](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/044_sequential_logic/))의 핵심 원리 — 조합 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)([Combinational Logic](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/032_combinational_logic/))가 현재 입력만으로 출력을 결정하는 반면, SR 래치는 이전 상태를 기억하여 출력이 입력 변화 후에도 유지된다.
> 3. S=1, R=1(또는 NAND에서 S=0, R=0)은 금지 조건(Forbidden [State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/)) — 두 출력이 동시에 같은 값이 되어 정의되지 않은 상태가 발생하며, 이 한계를 극복하기 위해 D [플립플롭](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/051_flip_flop/)·JK [플립플롭](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/051_flip_flop/) 등이 개발되었다.

---

## Ⅰ. SR 래치 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">NOR 게이트 SR 래치:</div>
<div class="kb-diagram-note">S ── ── NOR1 ── ── Q</div>
<div class="kb-diagram-tree-item" style="--depth:2">NOR2 ── ── Q'</div>
<div class="kb-diagram-note">R ──</div>
<div class="kb-diagram-note">진리표 (NOR 기반):</div>
<div class="kb-diagram-note">S R Q(t+1) Q'(t+1) 동작</div>
<div class="kb-diagram-note">0 0 Q(t) Q'(t) 유지 (Hold/Memory)</div>
<div class="kb-diagram-note">0 1 0 1 리셋 (Reset: Q=0)</div>
<div class="kb-diagram-note">1 0 1 0 셋 (Set: Q=1)</div>
<div class="kb-diagram-note">1 1 ? ? 금지 (Forbidden!)</div>
<div class="kb-diagram-note">NAND 게이트 SR 래치:</div>
<div class="kb-diagram-note">S' ─ ── NAND1 ── ── Q</div>
<div class="kb-diagram-tree-item" style="--depth:2">NAND2 ── ── Q'</div>
<div class="kb-diagram-note">R' ─</div>
<div class="kb-diagram-note">진리표 (NAND 기반, 입력 반전):</div>
<div class="kb-diagram-note">S' R' Q(t+1) 동작</div>
<div class="kb-diagram-note">1 1 Q(t) 유지</div>
<div class="kb-diagram-note">1 0 0 리셋</div>
<div class="kb-diagram-note">0 1 1 셋</div>
<div class="kb-diagram-note">0 0 ? 금지 (S'=R'=0)</div>
<div class="kb-diagram-note">물리적 구현:</div>
<div class="kb-diagram-note">NOR SR: S=1이 셋, R=1이 리셋 (능동 하이)</div>
<div class="kb-diagram-note">NAND SR: S'=0이 셋, R'=0이 리셋 (능동 로우)</div>
<div class="kb-diagram-note">NAND 타입이 실제 회로에서 더 일반적</div>
</div>
</div>



> 📢 **섹션 요약 비유**: SR 래치 = 2명의 경비원 — 두 경비원이 서로를 감시. A가 "켜"(S=1)라 하면 B가 꺼지고 A는 계속 켜짐. B가 "꺼"(R=1)라 하면 A가 꺼짐. 둘 다 동시에 명령하면 혼란(금지)!

---

## Ⅱ. 금지 조건과 해결



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">금지 조건 (Forbidden State):</div>
<div class="kb-diagram-note">NOR SR에서 S=R=1:</div>
<div class="kb-diagram-note">NOR1 = NOR(S=1, Q') = 0 → Q = 0</div>
<div class="kb-diagram-note">NOR2 = NOR(R=1, Q) = 0 → Q' = 0</div>
<div class="kb-diagram-note">결과: Q=0, Q'=0 (정상적으로 Q' = NOT Q여야 하는데 위반!)</div>
<div class="kb-diagram-note">입력이 동시에 0으로 돌아가면: 레이싱 조건(Race Condition)</div>
<div class="kb-diagram-note">최종 상태 예측 불가능</div>
<div class="kb-diagram-note">해결 방법:</div>
<div class="kb-diagram-note">1. 입력 제약:</div>
<div class="kb-diagram-note">회로 설계에서 S=R=1 동시 인가 금지</div>
<div class="kb-diagram-note">(소프트웨어 제어로 보장)</div>
<div class="kb-diagram-note">2. JK 플립플롭:</div>
<div class="kb-diagram-note">J=K=1 → 출력 반전 (Toggle)으로 정의</div>
<div class="kb-diagram-note">금지 조건 제거</div>
<div class="kb-diagram-note">JK 진리표 추가:</div>
<div class="kb-diagram-note">J K Q(t+1)</div>
<div class="kb-diagram-note">0 0 Q(t) 유지</div>
<div class="kb-diagram-note">0 1 0 리셋</div>
<div class="kb-diagram-note">1 0 1 셋</div>
<div class="kb-diagram-note">1 1 NOT Q 반전 (토글)</div>
<div class="kb-diagram-note">3. D 플립플롭:</div>
<div class="kb-diagram-note">입력 D 하나만 (S=D, R=NOT D)</div>
<div class="kb-diagram-note">D=0: 리셋, D=1: 셋</div>
<div class="kb-diagram-note">S=R=1 절대 불가 → 금지 조건 원천 차단</div>
<div class="kb-diagram-note">가장 많이 쓰이는 플립플롭</div>
<div class="kb-diagram-note">CPU 레지스터, 캐시의 기본 단위</div>
<div class="kb-diagram-note">4. T 플립플롭:</div>
<div class="kb-diagram-note">T=1이면 토글, T=0이면 유지</div>
<div class="kb-diagram-note">카운터 회로에 유용</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 금지 조건 해결 = 혼선 방지 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) — SR(둘 다 말할 수 있어 혼선), D(한 명만 말함 → 혼선 없음), JK(둘 다 말하면 역할 바꾸기로 정의). 혼선 원천 차단이 핵심!

---

## Ⅲ. 클록 제어 래치



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">레벨 트리거 SR 래치 (Gated SR Latch):</div>
<div class="kb-diagram-note">CLK 신호로 입력 활성화 제어</div>
<div class="kb-diagram-note">구조:</div>
<div class="kb-diagram-note">CLK=1: S, R 입력 반영</div>
<div class="kb-diagram-note">CLK=0: S, R 무시 (이전 상태 유지)</div>
<div class="kb-diagram-note">AND 게이트 추가:</div>
<div class="kb-diagram-note">S_eff = S AND CLK</div>
<div class="kb-diagram-note">R_eff = R AND CLK</div>
<div class="kb-diagram-note">동작:</div>
<div class="kb-diagram-note">CLK S R Q(t+1)</div>
<div class="kb-diagram-note">0 x x Q(t) (입력 무시)</div>
<div class="kb-diagram-note">1 0 0 Q(t) 유지</div>
<div class="kb-diagram-note">1 0 1 0 리셋</div>
<div class="kb-diagram-note">1 1 0 1 셋</div>
<div class="kb-diagram-note">1 1 1 ? 금지</div>
<div class="kb-diagram-note">문제 - 투명성 (Transparency):</div>
<div class="kb-diagram-note">CLK=1인 동안 입력이 계속 출력에 반영</div>
<div class="kb-diagram-note">CLK 활성화 중 여러 번 상태 변경 가능</div>
<div class="kb-diagram-note">→ 예측 어려움</div>
<div class="kb-diagram-note">해결 - 엣지 트리거 플립플롭:</div>
<div class="kb-diagram-note">CLK의 상승 엣지(0→1)나 하강 엣지(1→0)에서만 샘플링</div>
<div class="kb-diagram-note">마스터-슬레이브 플립플롭:</div>
<div class="kb-diagram-note">마스터: 상승 엣지에서 입력 샘플</div>
<div class="kb-diagram-note">슬레이브: 하강 엣지에서 출력 반영</div>
<div class="kb-diagram-note">→ 클록 사이클당 1회만 상태 변경</div>
<div class="kb-diagram-note">현대 CPU: 엣지 트리거 D 플립플롭 수십억 개</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 클록 제어 래치 = 수업 시간만 발언 허용 — 수업(CLK=1) 중에만 학생(입력) 말할 수 있음. 쉬는 시간(CLK=0)엔 무시. 엣지 트리거는 딱 종이 울릴 때만!

---

## Ⅳ. [플립플롭](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/051_flip_flop/) 종류 비교



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">플립플롭 (Flip-Flop) 비교:</div>
<div class="kb-diagram-note">래치 vs 플립플롭:</div>
<div class="kb-diagram-note">래치: 레벨 트리거 (CLK 레벨에 반응)</div>
<div class="kb-diagram-note">플립플롭: 엣지 트리거 (CLK 전환에만 반응)</div>
<div class="kb-diagram-note">종류별 특성:</div>
<div class="kb-diagram-note">D 플립플롭 (가장 일반적):</div>
<div class="kb-diagram-note">입력: D, CLK</div>
<div class="kb-diagram-note">Q(t+1) = D (클록 엣지에서)</div>
<div class="kb-diagram-note">응용: 레지스터, 시프트 레지스터, 파이프라인</div>
<div class="kb-diagram-note">JK 플립플롭:</div>
<div class="kb-diagram-note">입력: J, K, CLK</div>
<div class="kb-diagram-note">J=K=0: 유지, J=0,K=1: 리셋</div>
<div class="kb-diagram-note">J=1,K=0: 셋, J=K=1: 토글</div>
<div class="kb-diagram-note">응용: 카운터, 주파수 분주</div>
<div class="kb-diagram-note">T 플립플롭:</div>
<div class="kb-diagram-note">입력: T, CLK</div>
<div class="kb-diagram-note">T=0: 유지, T=1: 토글</div>
<div class="kb-diagram-note">JK에서 J=K=T로 연결</div>
<div class="kb-diagram-note">응용: 2진 카운터</div>
<div class="kb-diagram-note">SR → D → JK → T 변환:</div>
<div class="kb-diagram-note">모든 플립플롭은 서로 변환 가능</div>
<div class="kb-diagram-note">D가 가장 단순, 구현 용이 → 범용</div>
<div class="kb-diagram-note">타이밍 파라미터:</div>
<div class="kb-diagram-note">셋업 타임 (t_su): CLK 엣지 이전 입력 안정화 시간</div>
<div class="kb-diagram-note">홀드 타임 (t_h): CLK 엣지 이후 입력 유지 시간</div>
<div class="kb-diagram-note">전파 지연 (t_pd): CLK → Q 출력까지 지연</div>
<div class="kb-diagram-note">CPU 클록 속도 결정 요인:</div>
<div class="kb-diagram-note">최대 클록 = 1 / (t_pd + t_su + 배선 지연)</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [플립플롭](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/051_flip_flop/) 종류 = 직원 역할 분담 — D(단순 보조: 시키는 대로), JK(다재다능: 세 가지 역할), T(전문가: 토글만). CPU는 수십억 D [플립플롭](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/051_flip_flop/)으로 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 구성!

---

## Ⅴ. 실무 시나리오 — CPU [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 설계



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">8비트 레지스터 설계 (D 플립플롭 8개):</div>
<div class="kb-diagram-note">구조:</div>
<div class="kb-diagram-note">D7..D0: 8비트 입력</div>
<div class="kb-diagram-note">Q7..Q0: 8비트 출력</div>
<div class="kb-diagram-note">CLK: 클록 신호</div>
<div class="kb-diagram-note">WE (Write Enable): 쓰기 허용</div>
<div class="kb-diagram-note">각 비트: D 플립플롭 + WE 제어</div>
<div class="kb-diagram-note">실제: D_eff = (WE=1) ? D_in : Q_out</div>
<div class="kb-diagram-note">동작:</div>
<div class="kb-diagram-note">WE=0: 현재 값 유지 (CLK 엣지에도 변경 없음)</div>
<div class="kb-diagram-note">WE=1 + CLK 상승 엣지: 새 데이터 래치</div>
<div class="kb-diagram-note">x86 CPU 레지스터:</div>
<div class="kb-diagram-note">RAX: 64비트 → D 플립플롭 64개</div>
<div class="kb-diagram-note">16개 범용 레지스터: 64 × 16 = 1024 플립플롭</div>
<div class="kb-diagram-note">(캐시, 파이프라인 레지스터 포함 시 수백만~수십억)</div>
<div class="kb-diagram-note">타이밍 (현대 CPU):</div>
<div class="kb-diagram-note">클록: 3~5GHz = 0.2~0.33ns 주기</div>
<div class="kb-diagram-note">D 플립플롭 전파 지연: ~50ps</div>
<div class="kb-diagram-note">셋업 타임: ~30ps</div>
<div class="kb-diagram-note">1nm 공정: 더 빠른 전환, 더 낮은 전압</div>
<div class="kb-diagram-note">5V → 0.7V (전력 절감, 속도 향상)</div>
<div class="kb-diagram-note">메모리 계층과 래치:</div>
<div class="kb-diagram-note">레지스터 (D 플립플롭): 0.3ns, 수십~수백 바이트</div>
<div class="kb-diagram-note">L1 캐시 (SRAM: 6T 래치): 1~2ns, 32~64KB</div>
<div class="kb-diagram-note">L2 캐시: 4~8ns</div>
<div class="kb-diagram-note">DRAM: 80~120ns</div>
<div class="kb-diagram-note">SRAM 셀 = 6개 트랜지스터로 1비트 SR 래치 구현</div>
</div>
</div>



> 📢 **섹션 요약 비유**: CPU [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) = 계산기 화면 — D [플립플롭](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/051_flip_flop/) 64개가 RAX [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/). CLK마다 새 값 저장. 3GHz = 0.33ns마다 갱신. 현대 CPU는 수십억 개 래치로 고속 연산!

---

## 📌 관련 개념 맵

```
SR 래치 (SR Latch)
+-- 게이트 기반: NOR / NAND
+-- 출력: Q, Q'
+-- 금지 조건: S=R=1
+-- 발전
|   +-- 클록 제어 래치 (Gated SR)
|   +-- D 플립플롭 (가장 일반)
|   +-- JK 플립플롭
|   +-- T 플립플롭
+-- 응용
    +-- CPU 레지스터
    +-- SRAM 셀
    +-- 파이프라인 레지스터
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[SR 래치 (1919년경)]
NOR/NAND 교차 결합
최초의 디지털 기억 소자
      |
      v
[JK 플립플롭 (1950s)]
금지 조건 해결
토글 기능 추가
      |
      v
[D 플립플롭 (1960s)]
단일 입력
레지스터의 표준
      |
      v
[엣지 트리거 (1970s~)]
마스터-슬레이브
클록 안전성
      |
      v
[현재: 수십억 플립플롭]
3nm 공정 CPU
레지스터, 캐시, 파이프라인
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. SR 래치 = 두 경비원 규칙 — A가 "켜"(S) 외치면 A 켜지고 유지. B가 "꺼"(R) 외치면 꺼짐. 둘 다 외치면 싸움(금지 조건)!
2. D [플립플롭](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/051_flip_flop/) = 클록마다 [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) — 카메라(D FF)가 종(CLK) 울릴 때마다 현재 모습(D) 찍어 저장(Q). 3GHz = 초당 30억 장 촬영!
3. [SRAM](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/250_sram/) 캐시 = 빠른 메모 판 — L1 캐시는 6개 [트랜지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/014_transistor/) SR 래치. DRAM보다 100배 빠르지만 비용도 100배. CPU 옆에 작게 두는 이유!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 49 / 803

← **이전**: [048. 래치 — Latch](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/048_latch/)
**다음**: [D 래치 (D Latch)](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/050_d_latch/) →

---
