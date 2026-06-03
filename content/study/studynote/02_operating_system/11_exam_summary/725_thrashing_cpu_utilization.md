---
title: 725. 스래싱 (Thrashing) CPU 이용률 저하
date: '2026-05-09'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[257_thrashing|스래싱]]([[257_thrashing|Thrashing]])은 [[673_multiprogramming_bottleneck_resource|다중 프로그래밍]]([[673_multiprogramming_bottleneck_resource|Multiprogramming]]) 환경에서 메모리(RAM)에 너무 많은 프로세스를 욱여넣었을 때, **CPU가 원래 해야 할 '프로그램 연산'은 멈춘 채, 디스크에서 [[286_page_frame|페이지]]를 넣고 빼는(Swap in/out) 무의미한 막노동에만 100%의 시간을 쏟는 치명적 시스템 붕괴 상태**다.
> 2. **악순환의 고리**: CPU 사용률이 떨어지는 것을 본 OS [[079_kube_scheduler_pod_placement|스케줄러]]는 "어라? CPU가 놀고 있네? 프로그램을 더 띄워야지!"라고 오판하여 메모리에 프로세스를 더 밀어 넣게 되고, 이로 인해 [[286_page_frame|Page]] Fault가 더 미친 듯이 폭발하며 시스템이 완전히 마비되는 데스 스파이럴(Death Spiral)에 빠진다.
> 3. **해결책**: [[257_thrashing|스래싱]]을 막는 유일한 방법은 [[258_degree_of_multiprogramming|다중 프로그래밍 정도]]([[258_degree_of_multiprogramming|Degree of Multiprogramming]])를 강제로 낮춰서 몇몇 프로세스를 완전히 쫓아내거나(Suspend), 각 프로세스가 필수적으로 필요로 하는 최소한의 메모리 덩어리인 **[[265_working_set|워킹 셋]]([[265_working_set|Working Set]])**을 보장해 주는 아키텍처를 도입하는 것이다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - **[[257_thrashing|스래싱]] ([[257_thrashing|Thrashing]])**: 프로세스가 실제 실행되는 시간보다, [[260_page_replacement|페이지 교체]]([[387_page_fault|Page Fault]] 처리)에 더 많은 시간을 소비하여 시스템 전체의 [[282_performance_tactics|성능]]이 곤두박질치는 현상.

- **필요성 ([[381_virtual_memory|가상 메모리]]의 독이 든 성배)**: 
  - [[255_demand_paging|요구 페이징]]([[255_demand_paging|Demand Paging]])이 등장하면서, 8GB 램으로 100GB짜리 프로그램 10개를 띄울 수 있게 되었다.
  - OS는 CPU를 100% 활용하기 위해 메모리에 최대한 많은 프로세스를 올렸다.
  - 하지만 각 프로세스에게 할당된 램(프레임)이 너무 적어지자, A 프로세스가 1초 실행될 때마다 자꾸 자기 [[286_page_frame|페이지]]가 없어서([[387_page_fault|Page Fault]]) 디스크를 긁어오고, 이 과정에서 B 프로세스의 [[286_page_frame|페이지]]를 쫓아냈다. B가 실행될 때는 또 A의 [[286_page_frame|페이지]]를 쫓아냈다.
  - **해결책**: "메모리(RAM) 용량의 한계를 인정하고, CPU [[079_kube_scheduler_pod_placement|스케줄러]]가 무지성으로 프로세스를 밀어 넣지 못하게 통제하는 **글로벌 메모리 관리 [[164_policy|정책]]**이 필요하다"는 뼈아픈 교훈을 얻었다.

  - 책상(RAM)은 아주 좁은데, 10과목의 숙제(프로세스 10개)를 동시에 하려고 한다.
  - 수학 문제를 풀려고 가방(디스크)에서 수학책을 꺼내 책상에 놓으려니 자리가 없다. 그래서 영어책을 가방에 넣었다(Swap-out).
  - 1분 뒤 영어 단어를 외우려고 가방에서 영어책을 꺼내려니 또 자리가 없다. 이번엔 방금 꺼낸 수학책을 가방에 넣는다.
  - **[[257_thrashing|스래싱]]**: 숙제를 하는 시간보다, **가방에서 책을 꺼냈다 넣었다 하는 시간([[387_page_fault|Page Fault]])**이 10배 더 걸려서 밤새 1문제도 못 푸는 상태.

- **발전 과정**:
  1. **[[459_quic_fec_forward_error_correction|초기]] [[381_virtual_memory|가상 메모리]]**: [[257_thrashing|스래싱]] 현상 발견. 원인 불명으로 잦은 시스템 다운.
  2. **원인 규명 (Denning, 1968)**: 과도한 [[673_multiprogramming_bottleneck_resource|다중 프로그래밍]]이 원인임을 밝혀내고 [[265_working_set|워킹 셋]]([[265_working_set|Working Set]]) 모델 제안.
  3. **현대 OS의 방어**: [[425_oom_killer_score|OOM Killer]], 지역성(Locality) 기반 [[260_page_replacement|페이지 교체]], [[306_pff|PFF]]([[266_page_fault_frequency|Page Fault Frequency]]) 조절 등으로 [[257_thrashing|스래싱]]을 원천 차단함.

- **📢 섹션 요약 비유**: CPU를 100% [[289_cqrs_db|쓰기]] 위해 일꾼을 100명 불렀는데, 삽(메모리)이 10개밖에 없습니다. 일꾼들이 흙을 파는 게 아니라 서로 삽을 뺏고 뺏기느라 하루 종일 멱살만 잡고 있는 공사장의 아수라장입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[257_thrashing|스래싱]]의 수학적 발생 구조 (CPU 이용률 [[070_graph_datastructure|그래프]])

[[001_operating_system_purpose|운영체제]] 교과서에서 [[257_thrashing|스래싱]]을 설명할 때 반드시 등장하는, [[258_degree_of_multiprogramming|다중 프로그래밍 정도]](N)와 CPU 이용률의 [[083_relationship_in_er_model|관계]] [[070_graph_datastructure|그래프]]다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 다중 프로그래밍 정도 (N) 와 CPU Utilization의 관계       │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │  CPU 이용률 (%)                                                      │
  │   100 │                 /■■■■■■■■■\                               │
  │       │               /         \ ◀── [Thrashing Point (임계점)] │
  │       │             /            \                                │
  │       │           /               \                               │
  │       │         /                  \                              │
  │       │       /                     \   (수직 낙하)                 │
  │       │     /                        \                            │
  │    0  └────┼──────────┼───────────────┼──────────▶                │
  │           적음         적정 수준          많음     다중 프로그래밍 정도 (N)│
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 
1. [[459_quic_fec_forward_error_correction|초기]]에는 N을 늘릴수록 (앱을 많이 켤수록) CPU가 I/O 대기 시간에 딴짓을 할 수 있어 CPU 이용률이 정비례로 쫙쫙 오른다.
2. 하지만 **임계점(Knee Point)**을 넘는 순간, 각 프로세스에게 돌아가는 램(프레임) 개수가 턱없이 부족해진다.
3. 모든 프로세스가 디스크를 긁어오기 시작한다([[387_page_fault|Page Fault]] 폭발). CPU는 디스크 I/O가 끝날 때까지 할 일이 없으니(Wait) **CPU 이용률이 0%로 수직 낙하**해 버린다.

---

### [[257_thrashing|스래싱]]을 악화시키는 OS의 "바보 같은 판단" (Death Spiral)

[[257_thrashing|스래싱]]이 발생하면 왜 컴퓨터는 스스로 회복하지 못하고 죽어버릴까? OS [[079_kube_scheduler_pod_placement|스케줄러]]의 치명적인 오판 때문이다.

1. 메모리가 모자라서 [[286_page_frame|Page]] Fault가 미친 듯이 터진다.
2. 모든 프로세스가 디스크 응답을 기다리며 **[[089_wait_queue|Wait Queue]](Sleep)**로 들어간다.
3. CPU를 쓸 프로세스가 없으니, **CPU 이용률(Utilization)이 [[489_raid_10_hybrid|10]]% 밑으로 뚝 떨어진다.**
4. OS의 [[161_short_term_scheduler|단기 스케줄러]]([[163_long_term_scheduler|장기 스케줄러]])가 이를 모니터링하다가 이렇게 생각한다. **"어라? CPU가 엄청 팽팽 놀고 있네? 컴퓨터 [[282_performance_tactics|성능]]이 낭비되고 있으니 빨리 메모리에 새 프로그램을 더 띄워야겠다!"**
5. OS가 램에 **새로운 프로세스를 추가로 밀어 넣는다 (N 값 증가).**
6. 가뜩이나 부족한 램이 더 조각나서 [[286_page_frame|Page]] Fault가 우주 끝까지 폭발한다. 시스템은 완벽한 벽돌(Freeze)이 된다.

- **📢 섹션 요약 비유**: 불이 나서([[387_page_fault|Page Fault]]) 사람들이 질식해 쓰러져 조용해지자(CPU 0%), 밖에서 통제하는 경찰(OS)이 "안에 조용한 걸 보니 아직 공간이 널널한가 보네!" 하고 사람을 더 밀어 넣어서 압사시켜 버리는 끔찍한 오판 구조입니다.

---

## Ⅲ. 비교 및 연결

### 로컬 교체 ([[400_local_replacement|Local Replacement]]) vs 글로벌 교체 ([[399_global_replacement|Global Replacement]])

[[257_thrashing|스래싱]]이 터졌을 때 그 피해가 어떻게 전파되는지를 결정하는 아키텍처다.

| [[164_policy|정책]] | 동작 방식 | [[257_thrashing|스래싱]] 파급 효과 |
|:---|:---|:---|
| **[[399_global_replacement|Global Replacement]]** | 램이 모자라면 **"남의 프로세스"가 쓰던 [[286_page_frame|페이지]]를 빼앗아** 내 걸로 씀. | 한 놈이 [[257_thrashing|스래싱]]에 빠지면, 남의 메모리도 다 뺏어서 **시스템 전체가 동반 [[257_thrashing|스래싱]]으로 멸망함**. (하지만 평소 효율이 좋아 현대 OS의 기본값임) |
| **[[400_local_replacement|Local Replacement]]** | 무조건 **"자신에게 처음 할당된 프레임 안에서만"** 쫓아내고 교체함. | 한 놈이 [[257_thrashing|스래싱]]에 빠져도 남의 메모리는 못 뺏으므로 **다른 앱은 멀쩡함**. (단, 메모리 활용 효율이 떨어져 안 씀) |

### 과목 융합 관점

- **저장 장치 (Storage)**: [[257_thrashing|스래싱]]을 겪을 때 시스템의 목숨은 **Swap Disk의 I/O 속도**에 달려있다. 과거 [[465_hdd_structure|HDD]] 시절에는 [[257_thrashing|스래싱]]이 나면 하드디스크 드르륵거리는 소리가 미친 듯이 나면서 마우스조차 1분 뒤에 움직였다(초당 100 IOPS). 현재는 [[482_nvme|NVMe]] [[327_ssd|SSD]](초당 100만 IOPS)를 스왑으로 [[289_cqrs_db|쓰기]] 때문에, 가벼운 [[257_thrashing|스래싱]]은 사용자가 눈치채지 못할 정도로 하드웨어가 멱살 잡고 캐리하고 있다.
- **클라우드 (Cloud)**: K8s에서 [[561_container_based_deployment|컨테이너]] 하나가 `malloc` 무한 루프를 돌며 글로벌 [[257_thrashing|스래싱]]을 유발하는 것을 막기 위해, 리눅스는 **[[062_cgroups|Cgroups]] ([[668_cgroups_hw_resource_allocation|Control Groups]])**를 쓴다. Cgroups는 프로세스 그룹별로 "너는 최대 램 1GB만 써!"라고 물리적 벽(Local Replacement와 유사한 효과)을 쳐서, Noisy Neighbor(시끄러운 이웃)가 노드 전체를 [[257_thrashing|스래싱]]으로 몰고 가는 것을 100% 방어한다.

- **📢 섹션 요약 비유**: 뷔페(글로벌 교체)에서는 한 명의 대식가([[257_thrashing|스래싱]] 프로세스)가 모든 초밥을 싹쓸이하면 식당 전체 손님이 굶습니다. 도시락(로컬 교체)은 자기 밥만 먹으니 남에게 피해는 안 주지만, 배고플 때 유도리가 없습니다. OS는 뷔페를 쓰되 진상 손님을 내쫓는 가드([[425_oom_killer_score|OOM Killer]])를 고용하는 쪽을 택했습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. **시나리오 — 클라우드 서버의 "System Hang"과 [[157_oom_killer|OOM]] Killer의 자비 없는 등판**: EC2 서버에 Spring Boot 앱 3개를 띄웠다. 피크 타임이 되자 갑자기 [[538_ssh_vs_telnet_secure_remote|SSH]] 접속조차 10분이 걸리는 완벽한 벽돌 상태(Hang)가 됨.
   - **원인 분석**: 램은 8GB인데 3개의 JVM이 힙을 늘리면서 각자 4GB씩 요구했다. 리눅스 커널이 스왑(Swap) 디스크를 열어 억지로 버티려 했으나, 3개의 앱이 GC([[591_mvcc_garbage_collection_vacuum|가비지 컬렉터]])를 돌리기 위해 메모리를 쫙 훑는 순간 극단적인 **[[257_thrashing|스래싱]]([[257_thrashing|Thrashing]])**이 터졌다.
   - **해결 (커널의 개입)**: 리눅스 커널은 CPU `iowait`이 치솟고 메모리 여유 공간이 [[431_ssthresh_slow_start_threshold|임계치]] 밑으로 떨어지면 "이대로 가면 OS가 죽는다"고 판단한다. 이때 **[[157_oom_killer|OOM]] ([[425_oom_killer_score|Out-Of-Memory]]) Killer** 데몬이 깨어나서 메모리를 제일 많이 먹으면서도 가장 만만한 놈(주로 JVM 프로세스)을 `SIGKILL(-9)`로 무자비하게 쏴 죽인다. 앱 1개가 죽자 프레임이 수십만 개 쏟아져 나오며 [[257_thrashing|스래싱]]이 멈추고 서버가 다시 살아난다.

2. **시나리오 — 모바일 OS (iOS/Android)의 스왑 금지 철학**: 스마트폰에서 카카오톡을 하다가 유튜브를 보고, 다시 인스타그램을 켰다.
   - **아키텍처 적용**: 데스크탑(Windows/Linux)은 램이 부족하면 하드디스크에 스왑(Swap)을 만들어 [[257_thrashing|스래싱]]을 견딘다. 하지만 **iOS와 안드로이드는 스왑 [[514_partition_slice_volume|파티션]] 자체가 없다!** 
   - 스마트폰의 [[256_flash_memory|플래시 메모리]](eMMC)에 스왑 아웃을 해대면 메모리 수명이 1년 만에 닳아버리고 배터리가 광탈하기 때문이다. 따라서 모바일 OS는 [[257_thrashing|스래싱]]이 발생할 틈도 주지 않고, 램이 모자란 순간 백그라운드에 있는 앱(예: 카카오톡)의 메모리를 가차 없이 날려버린다(App Kill). 사용자가 다시 카톡을 켜면 아예 처음부터 다시 부팅되게 만들어버리는 강압적이지만 효율적인 [[164_policy|정책]]을 쓴다.

### 의사결정 및 튜닝 플로우

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 메모리 부족 및 스래싱(Thrashing) 대응 아키텍처 플로우        │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [서버의 CPU `wa(I/O Wait)`가 50% 이상 치솟고 응답 지연이 폭발함]           │
  │                │                                                  │
  │                ▼                                                  │
  │      `free -m` 명령어로 확인 시 Swap 영역(Swap used)을 미친 듯이 쓰고 있는가?│
  │          ├─ 예 ─────▶ [스래싱(Thrashing) 확진!]                     │
  │          │            대책 1: 원인 앱의 메모리 누수(Leak) 픽스             │
  │          │            대책 2: Scale-up (RAM 하드웨어 즉각 증설)          │
  │          └─ 아니오 ──▶ 단순한 디스크 I/O 병목이거나 네트워크/DB 대기임.      │
  │                │                                                  │
  │                ▼                                                  │
  │      클라우드/K8s 환경에서 스래싱으로 인한 동반 장애를 막으려면?               │
  │          ├──▶ [Swap 끄기 (Swapoff) + Resource Limit 강제]          │
  │          │    결론: K8s는 스왑을 쓰는 것(느려지는 것)을 극도로 혐오한다.       │
  │          │          아예 스왑을 꺼서 스래싱 자체가 성립 못 하게 만들고,        │
  │          │          메모리를 넘기면 즉시 OOM Kill로 쳐내어 Fail-Fast를 유도함.│
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** "스왑(Swap)을 넉넉히 잡아두면 서버가 안 죽어서 좋겠지?"는 최악의 운영 마인드다. 스왑은 서버를 살려두는 게 아니라, 서버가 **산 채로 썩어가며([[257_thrashing|Thrashing]]) 아무 응답도 못 하는 좀비**로 만드는 악마의 공간이다. 현대 엔터프라이즈 환경에서는 스왑을 아예 0으로 끄거나 2GB 정도로 최소화하고, 차라리 깔끔하게 OOM으로 뻗고(Crash) 자동 재시작(Restart)하게 만드는 것이 최고의 아키텍처다.

### 도입 [[435_checklist_based_testing|체크리스트]]
- **[[306_pff|PFF]] ([[266_page_fault_frequency|Page Fault Frequency]]) 튜닝**: 시스템이 [[257_thrashing|스래싱]]에 빠지지 않게, 프로세스마다 '초당 발생하는 [[720_page_fault_isr|페이지 폴트]] 횟수'를 재고 있는가? 폴트가 너무 잦으면 "이 앱은 램이 더 필요하구나" 하고 프레임을 더 주고, 폴트가 거의 없으면 "램이 남아도네?" 하고 프레임을 뺏어서 다른 앱에 주는 **[[306_pff|PFF]] 동적 할당 [[001_algorithm_definition|알고리즘]]**의 철학을 [[282_performance_tactics|성능]] 모니터링에 적용해야 한다.

- **📢 섹션 요약 비유**: [[257_thrashing|스래싱]]은 빚(Swap)을 내서 돌려막기([[286_page_frame|Page]] 교체)를 하다 파산하는 것입니다. 가장 좋은 해결책은 빚을 더 내는 것이 아니라, 신용카드(Swap)를 가위로 잘라버리고 파산 선고([[157_oom_killer|OOM]] Kill)를 받은 뒤 깔끔하게 새 삶(재시작)을 시작하는 것입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | [[257_thrashing|스래싱]] 발생 및 방치 (Swap 남용) | [[257_thrashing|스래싱]] 회피 아키텍처 ([[157_oom_killer|OOM]]/K8s) | 개선 효과 |
|:---|:---|:---|:---|
| **정량 (CPU 활용률)**| I/O Wait 폭발로 연산 효율 0% 수렴 | 비정상 앱 제거로 **정상 워크로드 90% 방어**| 인프라의 [[139_throughput|처리량]]([[139_throughput|Throughput]]) 정상화 |
| **정량 (응답 속도)** | 디스크 스왑으로 수만 배(ms 단위) [[015_지연_데이터_관점|지연]] | 램(RAM) 내의 [[456_caching|캐싱]] 유지로 ns 단위 방어 | 사용자 이탈률 방어 및 [[090_service_kubernetes_network_load_balancing|서비스]] [[085_confidence_association_rule_conditional_probability|신뢰도]] 유지 |
| **정성 (운영 철학)** | 시스템 전체가 서서히 느려지다 죽음 | 문제의 [[561_container_based_deployment|컨테이너]]만 Fail-Fast 컷오프 | 장애 격리([[195_isolation_concurrency_control|Isolation]]) 및 폭발 반경(Blast [[541_radius_remote_authentication_aaa|Radius]]) 최소화 |

### 미래 전망
- **ZRAM ([[347_compaction|압축]] 스왑)의 대중화**: 안드로이드나 크롬OS 같은 기기는 스왑으로 디스크를 쓰지 않고, 램의 일부 공간을 떼어내어 [[347_compaction|압축]]기(ZRAM)로 쓴다. [[257_thrashing|스래싱]]이 나려고 할 때 디스크까지 가지 않고, 램 안에서 데이터를 1/3로 [[347_compaction|압축]]해 버리는 것이다. CPU 연산량은 조금 늘지만, 치명적인 디스크 I/O를 발생시키지 않아 [[257_thrashing|스래싱]]의 공포를 획기적으로 늦추는 최신 [[001_operating_system_purpose|운영체제]] 트렌드다.

### 결론
[[257_thrashing|스래싱]]([[257_thrashing|Thrashing]])은 컴퓨터 공학의 끝없는 탐욕([[673_multiprogramming_bottleneck_resource|다중 프로그래밍]])이 빚어낸 거대한 붕괴 현상이다. "더 많이, 더 동시에" 돌리려던 인간의 욕심이 메모리의 물리적 한계와 충돌했을 때, 시스템은 모든 일을 내려놓고 허둥대는 패닉에 빠지고 만다. 이 쓰라린 경험을 통해 [[001_operating_system_purpose|운영체제]]는 '무한한 [[381_virtual_memory|가상 메모리]]'라는 환상에서 깨어나, [[157_oom_killer|OOM]] Killer라는 냉혹한 자경단을 고용하고 [[265_working_set|워킹 셋]]([[265_working_set|Working Set]])이라는 [[571_protection_vs_security|보호]] 구역을 지정하는 성숙한 자원 통제자로 거듭났다. [[257_thrashing|스래싱]]은 아키텍트에게 **"한계 자원(RAM)을 넘어서는 스케일 아웃은 소프트웨어로 극복할 수 없다"**는 가장 차갑고 절대적인 물리 법칙을 일깨워준다.

- **📢 섹션 요약 비유**: 서커스 삐에로가 공을 3개, 4개 돌릴 때([[673_multiprogramming_bottleneck_resource|다중 프로그래밍]])는 환호가 쏟아집니다. 하지만 욕심을 내어 10개를 돌리는 순간([[257_thrashing|스래싱]] 임계점), 공은 몽땅 바닥에 떨어지고 삐에로는 공을 줍느라 공연(CPU 연산)을 완전히 망쳐버립니다. 내 시스템의 공이 몇 개인지를 아는 것이 진정한 엔지니어링입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[261_fifo_page_replacement|FIFO]] 벨라디의 모순 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [[724_optimal_page_replacement_unrealizable|최적 알고리즘]] ([[724_optimal_page_replacement_unrealizable|OPT]]) 구현 불가 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [[265_working_set|워킹 셋]] ([[265_working_set|Working Set]]) 메모리 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [[468_disk_scheduling_purpose|디스크 스케줄링]] SCAN 엘리베이터 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[최적 알고리즘 (OPT) 구현 불가]
    │
    ▼
[스래싱 (Thrashing) CPU 이용률 저하]
    │
    ├──▶ [워킹 셋 (Working Set) 메모리]
    └──▶ [디스크 스케줄링 SCAN 엘리베이터]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 [[347_compaction|압축]]해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 철수는 너무 욕심쟁이라서 책상(메모리) 위에 국어, 영어, 수학, 과학책 10권을 억지로 다 올려놓고 한 번에 공부하려고 했어요.
2. 책상이 너무 비좁아서, 수학을 풀려면 영어책을 바닥(디스크)에 내려놓고 수학책을 올려야 했어요. 1분 뒤 영어를 보려면 수학책을 내리고 영어책을 다시 올려야 했죠.
3. 결국 철수는 공부는 한 글자도 못 하고, 밤새도록 책을 올렸다 내렸다 하는([[387_page_fault|Page Fault]]) 막노동만 하다가 코피가 터져서 쓰러졌어요! 이걸 바로 '[[257_thrashing|스래싱]]([[257_thrashing|Thrashing]])'이라고 부른답니다.
