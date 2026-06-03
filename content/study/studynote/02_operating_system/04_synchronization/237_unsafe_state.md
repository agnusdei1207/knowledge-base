+++
weight = 237
title = "237. 불안전 상태 (Unsafe State)"
date = "2026-05-09"
[extra]
categories = "studynote-operating-system"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[299_unsafe_state|불안전 상태]] ([[299_unsafe_state|Unsafe State]])는 운영체제의 [[041_resource_allocation|자원 할당]] 상태 중, 현재 남은 자원으로는 **시스템 내의 어떤 프로세스도 요구하는 최대 자원량(Max Need)을 충족시켜 줄 수 없어 '안전 순서열([[093_safe_scaled_agile_framework_art_pi|Safe]] Sequence)'을 단 하나도 찾을 수 없는 논리적 파산 상태**를 의미한다.
> 2. **가치**: "[[299_unsafe_state|불안전 상태]]가 곧 [[281_deadlock_definition|교착 상태]]([[281_deadlock_definition|Deadlock]])다"라는 명제는 틀렸다. [[299_unsafe_state|불안전 상태]]는 **데드락이 발생할 '가능성([[096_risk_non_risk_architecture_evaluation_flaws|Risk]])'이 0보다 큰 지뢰밭 영역**일 뿐, 프로세스들이 자원을 얌전하게 쓰고 빨리 반납하면 무사히 지나갈 수도 있는 확률적 공간이다.
> 3. **융합**: [[297_deadlock_avoidance|교착 상태 회피]] [[001_algorithm_definition|알고리즘]](은행원 [[001_algorithm_definition|알고리즘]])의 유일한 목적은 시스템이 단 한순간이라도 이 [[299_unsafe_state|불안전 상태]]로 넘어가지 못하도록, 요구된 [[041_resource_allocation|자원 할당]]을 거부(Deny)하고 스레드를 대기(Block)시키는 완벽한 예방선을 긋는 것이다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 시스템이 프로세스들에게 자원을 빌려주다가, 은행(OS)의 금고 잔고(Available)가 너무 바닥을 쳐서 남은 돈으로는 그 누구의 추가 대출 요구(Need)도 해결해 줄 수 없는 상태. 즉, 빚의 연쇄 상환 고리가 끊어진 상태다.
- **필요성**: 시스템이 어느 순간 데드락에 빠지는 것은 번개를 맞는 것처럼 우연한 일이 아니다. 반드시 "자원을 아슬아슬하게 돌려막기 하다가 벼랑 끝에 몰린" 수학적 임계점을 지나야만 발생한다. 이 임계점의 명확한 정의가 있어야만 운영체제가 "여기서부터는 브레이크를 밟아야 한다"고 코딩할 수 있다.

- **등장 배경**: 데이크스트라의 은행원 [[001_algorithm_definition|알고리즘]] 시뮬레이션에서, '[[298_safe_state|안전 상태]]([[298_safe_state|Safe State]])'의 대척점으로서 수학적으로 정의되었다. 데드락 회피 철학은 "[[299_unsafe_state|불안전 상태]]를 정의하고, 거기로 가는 모든 경로를 차단한다"는 네거티브(Negative) 방어 논리에 기반하고 있다.

```text
  [안전 상태, 불안전 상태, 교착 상태의 포함 관계도]

  ┌─────────────────────────────────────────────────────┐
  │  전체 자원 할당 상태 (All States)                   │
  │                                                     │
  │  ┌─────────────────┐ ┌────────────────────────┐     │
  │  │ 안전 상태        │ │ 불안전 상태 (Unsafe)      │ │
  │  │ (Safe State)    │ │                        │     │
  │  │                 │ │   ┌────────────────┐   │     │
  │  │                 │ │   │ 교착 상태       │   │    │
  │  │ (데드락 확률 0%)  │ │   │ (Deadlock)     │   │   │
  │  │                 │ │   │ (파산 확정 ☠️)   │   │   │
  │  │                 │ │   └────────────────┘   │     │
  │  └─────────────────┘ └────────────────────────┘     │
  └─────────────────────────────────────────────────────┘
```
**[다이어그램 해설]** [[281_deadlock_definition|교착 상태]]([[281_deadlock_definition|Deadlock]])는 반드시 [[299_unsafe_state|불안전 상태]]([[299_unsafe_state|Unsafe State]]) 안에서만 발생한다. 하지만 [[299_unsafe_state|불안전 상태]]의 모든 공간이 [[281_deadlock_definition|교착 상태]]인 것은 아니다. [[299_unsafe_state|불안전 상태]]는 "프로세스들이 최악의 경우(Maximum)로 자원을 요구할 경우 데드락이 터지는 상태"다. 만약 프로세스들이 양심껏 최대치를 요구하지 않고 일찍 작업을 끝내 반환해 준다면, [[299_unsafe_state|불안전 상태]]에서도 데드락 없이 무사히 빠져나올 수 있다. (그래서 은행원 [[001_algorithm_definition|알고리즘]]이 "너무 쫄보같이 보수적이다"라고 비판받는 것이다).

- **📢 섹션 요약 비유**: [[298_safe_state|안전 상태]]는 "태풍이 안 오는 날씨"고, [[299_unsafe_state|불안전 상태]]는 "태풍 경보가 내린 바다"입니다. [[281_deadlock_definition|교착 상태]]는 "배가 뒤집힌 것"입니다. 태풍 경보가 내린 바다에 나간다고 100% 배가 뒤집히는 건 아니지만(운 좋게 살 수도 있음), 배가 뒤집힌 사고는 무조건 태풍이 온 바다에서 일어납니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[299_unsafe_state|불안전 상태]] ([[299_unsafe_state|Unsafe State]])의 수학적 성립 과정

어떻게 안전했던 시스템이 [[299_unsafe_state|불안전 상태]]로 곤두박질치는가?

**[초기 안전 상태]**
시스템 자원 총 10개, 현재 남은 자원(Available) = **2개**
| 프로세스 | 현재 [[551_quota_disk_limit|할당량]] (Alloc) | 최대 필요량 (Max) | 추가 필요량 (Need) |
|:---:|:---:|:---:|:---:|
| P1 | 5 | [[489_raid_10_hybrid|10]] | 5 |
| **P2** | **2** | **4** | **2** |
| P3 | 1 | 4 | 3 |

*분석*: 남은 자원이 2개다. P2의 Need(2)를 딱 만족시킨다. P2를 밀어주면 P2가 끝나면서 기존 [[551_quota_disk_limit|할당량]] 2개까지 뱉어내어 남은 자원이 4개가 된다. 이 4개로 P3(Need 3)를 살리고, 그다음 P1을 살릴 수 있다. ($P_2 \to P_3 \to P_1$ 안전 순서열 존재 ─▶ **[[298_safe_state|Safe State]]**)

**[잘못된 대출 승인으로 인한 [[299_unsafe_state|불안전 상태]] 진입]**
위 상황에서 P3가 "자원 1개만 먼저 빌려주세요!"라고 요청했다. 스케줄러가 아무 생각 없이 1개를 내어줬다 치자.
▶ 현재 남은 자원(Available) = **1개**로 줄어듦. (P3의 Alloc은 2, Need는 2로 변경됨)

| 프로세스 | 현재 [[551_quota_disk_limit|할당량]] (Alloc) | 최대 필요량 (Max) | 추가 필요량 (Need) |
|:---:|:---:|:---:|:---:|
| P1 | 5 | [[489_raid_10_hybrid|10]] | 5 |
| **P2** | **2** | **4** | **2** |
| **P3** | **2** | **4** | **2** |

*재분석*: 이제 남은 자원이 **1개**뿐이다. 그런데 P1(5), P2(2), P3(2) 그 누구의 Need도 1개로는 채워줄 수 없다! 
🚨 **결과**: 그 어떤 안전 순서열도 그릴 수 없다. 이것이 바로 **[[299_unsafe_state|불안전 상태]]([[299_unsafe_state|Unsafe State]])**로의 추락이다. 이 상태에서 P2나 P3가 자원을 더 달라고 하면 영원히 무한 대기([[281_deadlock_definition|Deadlock]])에 빠지게 된다. 은행원 [[001_algorithm_definition|알고리즘]]은 P3가 1개를 달라고 했을 때 이 결과를 미리 계산해 보고, 1개를 주는 것을 거절(Block)하여 시스템을 [[093_safe_scaled_agile_framework_art_pi|Safe]] State에 머물게 하는 기술이다.

### 회피(Avoidance)의 극단적 보수성 (왜 욕을 먹는가?)
위의 [[299_unsafe_state|불안전 상태]] 시나리오를 다시 보자. 
P2와 P3는 최대(Max) 4개가 필요하다고 OS에 신고(계약)해 놨지만, 실제로 코드를 돌려보니 3개만 쓰고 끝날 수도 있는 일이다. 만약 P2가 운 좋게 3개만 쓰고 자원을 반납했다면, 남은 1개 자원으로도 충분히 시스템은 돌아갔을 것이다. 
하지만 은행원 [[001_algorithm_definition|알고리즘]]은 **"니들이 최악으로 나쁜 마음(Max)을 먹었을 때"를 가정**하고 철퇴를 내리기 때문에, 실제로는 데드락이 터지지 않을 상황인데도 멀쩡한 스레드를 재워버리는(Sleep) 극심한 시스템 낭비를 유발한다.

- **📢 섹션 요약 비유**: 대출 심사역(회피 [[001_algorithm_definition|알고리즘]])은 너무 보수적입니다. 고객이 마이너스 통장 한도(Max Need)를 1억 뚫어놓으면, 실제로 고객이 100만 원만 꺼내 쓸 확률이 높음에도 불구하고 "이놈이 내일 1억을 한 번에 다 빼가면 어쩌지?"라고 최악을 상정하여 다른 고객들의 대출을 다 막아버리는 꽉 막힌 금융 시스템입니다.

---

## Ⅲ. 비교 및 연결

### 상태 변화와 시스템의 반응 ([[632_state_transition_diagram_testing|State Transition]])

| [[632_state_transition_diagram_testing|상태 전이]] | 원인 및 조건 | OS 스케줄러의 행동 |
|:---|:---|:---|
| **[[093_safe_scaled_agile_framework_art_pi|Safe]] ─▶ [[093_safe_scaled_agile_framework_art_pi|Safe]]** | 락(자원) 요청을 시뮬레이션해 보니 여전히 [[093_safe_scaled_agile_framework_art_pi|Safe]] Sequence가 존재함 | 락 획득 승인! (CPU 할당) |
| **[[093_safe_scaled_agile_framework_art_pi|Safe]] ─▶ Unsafe** | 락 요청을 승인하면 [[093_safe_scaled_agile_framework_art_pi|Safe]] Sequence가 붕괴됨 | 🚨 락 승인 거부! (스레드를 대기 큐로 던지고 Sleep) |
| **Unsafe ─▶ [[281_deadlock_definition|Deadlock]]**| Unsafe 상태에서 프로세스들이 실제로 Max Need까지 자원을 요구해 버림 | 시스템 먹통. 제3의 개입(강제 킬/재부팅) 전까지 [[658_ir_recovery|복구]] 불가 |
| **Unsafe ─▶ [[093_safe_scaled_agile_framework_art_pi|Safe]]** | Unsafe 상태였는데, 프로세스가 양심껏 자원을 조기 반납함 (운이 좋음) | 가용 자원이 늘어나며 기적적으로 다시 [[093_safe_scaled_agile_framework_art_pi|Safe]] State로 회귀 |

### [[299_unsafe_state|불안전 상태]]의 역설 (Unsafe $\neq$ [[281_deadlock_definition|Deadlock]])
컴퓨터 공학 시험에 나오는 가장 큰 함정이다. "[[299_unsafe_state|불안전 상태]]에 진입하면 반드시 [[281_deadlock_definition|교착 상태]]가 발생한다"는 **거짓(False)**이다.
[[299_unsafe_state|불안전 상태]]는 **"[[281_deadlock_definition|교착 상태]]가 발생할 가능성이 0보다 커진 상태"**일 뿐이다. 만약 모든 프로세스가 자원을 최대로 요구하기 전에 스스로 I/O 대기를 타거나 자원을 풀어버린다면, 데드락은 터지지 않고 늪을 무사히 빠져나온다. 단지 OS [[022_kernel_role|커널]] 설계자들은 그 '운'에 시스템의 명운을 맡기는 것을 병적으로 싫어할 뿐이다.

- **📢 섹션 요약 비유**: [[299_unsafe_state|불안전 상태]]는 '안전벨트를 안 매고 시속 200km로 달리는 상태'입니다. 무조건 사고가 나서 죽는 건 아니지만(운 좋으면 도착함), 만약 사고(최대 자원 요구)가 나면 무조건 죽는(데드락) 미친 짓입니다. OS는 안전벨트를 매지 않으면 아예 시동이 안 걸리게(할당 거부) 막아두는 겁니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오
1. **Linux [[157_oom_killer|OOM]] ([[157_oom_killer|Out of Memory]]) Killer의 작동 원리 ([[299_unsafe_state|불안전 상태]]의 실무적 방치)**: 
   - 리눅스는 데드락 회피(Banker's [[001_algorithm_definition|Algorithm]])를 포기했다. 즉, **리눅스 시스템은 밥 먹듯이 [[299_unsafe_state|불안전 상태]]([[299_unsafe_state|Unsafe State]])를 들락날락한다**. 
   - 사용자가 메모리(자원)를 요청(malloc)하면 리눅스는 "일단 다 써!"라고 가상 메모리를 펑펑 남발한다(**Memory Overcommit**). 
   - 그러다 진짜로 물리 메모리가 부족해져서 데드락 직전의 임계점(진짜 100% 꽉 참)에 도달하면, 그제야 **[[425_oom_killer_score|OOM Killer]]**라는 자객을 보내서 메모리를 많이 먹는 놈을 뒤통수 쳐서 죽여버린다.
   - **아키텍처의 승리**: 이론적으로는 위험해 보이지만, 대부분의 프로세스가 `malloc` 해놓고 실제론 메모리를 다 안 쓴다는 현실적 통계(운)를 믿고 오버헤드 0의 극강의 스루풋을 달성한 실무 아키텍처의 승리다.
2. **[[205_kubernetes_container_orchestration|Kubernetes]](K8s) Resource Overcommit 제어**: 클라우드 인프라에서도 리눅스처럼 오버커밋을 즐긴다. K8s [[085_pod_kubernetes_container_unit|파드]]([[198_pod_kubernetes_minimum_deployment_unit|Pod]])에 `Requests`와 `Limits`를 다르게 설정하는 것 자체가 "[[299_unsafe_state|불안전 상태]]를 합법적으로 허용하겠다"는 선언이다.
   - 노드의 전체 메모리가 10G인데, 10개 [[085_pod_kubernetes_container_unit|파드]]의 Limits 합이 20G면 시스템은 항상 [[299_unsafe_state|불안전 상태]]다.
   - 만약 운이 나빠 10개 [[085_pod_kubernetes_container_unit|파드]]가 동시에 2G씩 달라고 하면 데드락([[157_oom_killer|OOM]])이 터져 [[085_pod_kubernetes_container_unit|파드]]들이 우수수 Eviction(퇴거) 당한다. 이것이 회피를 포기한 대가지만, 클라우드 회사는 빈 공간을 팔아 돈을 더 버는 비즈니스 모델을 택했다.

```text
  ┌────────────────────────────────────────────────────────────────────┐
  │     클라우드 환경의 자원 오버커밋(Overcommit)과 Unsafe State 관리  │
  ├────────────────────────────────────────────────────────────────────┤
  │                                                                    │
  │   [ K8s 클러스터 자원 배분 전략 결정 ]                             │
  │                                                                    │
  │   [ 1. Guaranteed QoS (안전 상태 100% 강제 유지) ]                 │
  │     ▶ 방법: 모든 파드의 Requests == Limits 로 똑같이 설정.         │
  │     ▶ 효과: 노드 자원보다 큰 파드는 배치가 거부됨(Banker's 회피).  │
  │     ▶ 단점: 비싼 서버 CPU가 맨날 50%씩 텅텅 놀아서 돈 낭비 극심.   │
  │                                                                    │
  │   [ 2. Burstable QoS (불안전 상태 적극 활용) ]                     │
  │     ▶ 방법: Requests < Limits 로 뻥튀기 배포 허용.                 │
  │     ▶ 효과: 100만 원짜리 서버에 200만 원어치 파드를 구겨 넣음.     │
  │     ▶ 리스크: 모두가 Limit을 당겨 쓰면(Unsafe -> Deadlock 터짐)    │
  │              OOM Killer가 파드를 랜덤하게 죽여버림.                │
  │                                                                    │
  │   ✅ 아키텍트의 타협: 무거운 DB는 1번(Safe)으로 띄우고,            │
  │                     죽어도 바로 살아나는 웹서버는 2번(Unsafe)으로! │
  └────────────────────────────────────────────────────────────────────┘
```
**[다이어그램 해설]** "서버 자원을 100% 안전([[093_safe_scaled_agile_framework_art_pi|Safe]])하게 관리한다"는 것은 비즈니스 관점에서 보면 "자원을 낭비하여 회사에 손해를 끼치고 있다"는 말과 동의어다. 위대한 인프라 아키텍트는 시스템이 [[299_unsafe_state|불안전 상태]]([[299_unsafe_state|Unsafe State]])에서 아슬아슬하게 줄타기하도록 만들면서도, 진짜 파국(데드락)이 터졌을 때 즉시 죽이고 살리는 자동 [[658_ir_recovery|복구]] 아키텍처(Self-healing)를 붙여 시스템의 ROI를 극대화한다.

- **📢 섹션 요약 비유**: 비행기 오버부킹(초과 예약)과 같습니다. 좌석이 100개(자원)인데 표를 110장(Limits 뻥튀기) 팝니다. 모든 승객이 나타나면(최대 자원 요구) 자리가 모자라 데드락이 터지지만, 항공사는 "항상 [[489_raid_10_hybrid|10]]%는 안 오더라([[210_heuristics_scheduling|휴리스틱]])"는 통계를 믿고 [[299_unsafe_state|불안전 상태]](오버부킹)를 유지하며 돈을 법니다. 자리가 모자라면 바우처를 주고 다음 비행기로 쫓아내면([[425_oom_killer_score|OOM Killer]]) 그만입니다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과
[[298_safe_state|안전 상태]]와 [[299_unsafe_state|불안전 상태]]의 경계선을 이해하면, 개발자는 시스템에 부하가 걸렸을 때 왜 특정 스레드가 락을 얻지 못하고 영원히 무한 대기에 빠지는지 그 근본적인 '자원 고갈 스레숄드(Threshold)'를 수리적으로 파악하고 아키텍처를 재설계할 수 있다.

### 결론 및 미래 전망
[[299_unsafe_state|불안전 상태]]([[299_unsafe_state|Unsafe State]])를 절대악으로 규정하고 이를 피하기 위해 수만 줄의 행렬 연산을 돌리던(은행원 [[001_algorithm_definition|알고리즘]]) 고전 운영체제의 결벽증은 현대에 이르러 완전히 타파되었다.
현대의 대규모 [[136_variance|분산]] 컴퓨팅(클라우드, [[619_msa_traffic_hardware|MSA]])은 [[299_unsafe_state|불안전 상태]]를 두려워하지 않는다. 오히려 [[299_unsafe_state|불안전 상태]]를 적극적으로 활용(Overcommit)하여 인프라 효율을 극대화하고, 만약 그것이 곪아 터져 데드락이 되면 재빨리 [[532_microservices_decomposition_patterns|마이크로서비스]] 하나를 [[561_container_based_deployment|컨테이너]] 단위로 킬(Kill)하고 재생성(Restart) 시키는 **장애 내성(Fault-tolerance)** 기술로 패러다임이 진화했다. 즉, "절대 안 넘어지게 조심해서 걷기([[298_safe_state|Safe State]] 방어)"보다 "넘어지면 0.1초 만에 아무 일 없던 것처럼 털고 일어나기(Resilience)"가 현대 IT 인프라의 새로운 진리다.

- **📢 섹션 요약 비유**: 과거에는 자전거가 안 넘어지게 하려고 양옆에 무거운 보조 바퀴(회피 [[001_algorithm_definition|알고리즘]])를 달고 다녔습니다. 지금은 보조 바퀴를 떼어버리고 쌩쌩 달리며 넘어질 위험([[299_unsafe_state|불안전 상태]])을 감수합니다. 대신, 넘어져도 다치지 않는 완벽한 전신 에어백(클라우드 자동 [[658_ir_recovery|복구]])을 입고 달리는 시대가 온 것입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[225_binary_semaphore|이진 세마포어]] ([[225_binary_semaphore|Binary Semaphore]]) = 뮤텍스와 유사 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [[226_counting_semaphore|카운팅 세마포어]] ([[226_counting_semaphore|Counting Semaphore]]) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [[229_monitor|모니터]] ([[229_monitor|Monitor]]) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [[228_condition_variable|조건 변수]] ([[228_condition_variable|Condition Variable]]) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[카운팅 세마포어 (Counting Semaphore)]
    │
    ▼
[불안전 상태 (Unsafe State)]
    │
    ├──▶ [모니터 (Monitor)]
    └──▶ [조건 변수 (Condition Variable)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 용돈이 500원 남았는데, 친구 두 명이 와서 각자 "나중에 1,000원씩 빌려줄 수 있어?"라고 약속을 걸어놨어요.
2. 당장 500원을 한 명한테 줘버리면, 나중에 1,000원 달라고 할 때 줄 돈이 모자라서 싸움(데드락)이 날 확률이 엄청 높겠죠?
3. 이렇게 "아직 싸움이 난 건 아니지만, 한 발짝만 더 헛디디면 무조건 크게 싸움이 날 것 같은 조마조마한 상태"를 **[[299_unsafe_state|불안전 상태]]([[299_unsafe_state|Unsafe State]])**라고 한답니다!
