+++
weight = 380
title = "380. NUMA (Non-Uniform Memory Access)"
date = "2026-03-27"
[extra]
categories = "studynote-computer-architecture"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[377_numa_allocation|NUMA]] ([[377_numa_allocation|Non-Uniform Memory Access]])는 모든 프로세서가 같은 메모리를 보되, 실제 접근 [[015_지연_데이터_관점|지연]]시간은 메모리의 물리적 위치에 따라 달라지는 다중 [[125_socket|소켓]] 서버용 메모리 아키텍처다.
> 2. **가치**: 중앙 메모리 병목을 피하고 [[125_socket|소켓]]별 메모리 [[140_bandwidth|대역폭]]을 늘려, [[379_uma|UMA]] ([[379_uma|Uniform Memory Access]])보다 훨씬 큰 코어 수와 메모리 용량으로 확장할 수 있다.
> 3. **판단 포인트**: NUMA는 하드웨어만으로 끝나지 않으며, [[092_thread_lwp|스레드]] 배치·메모리 할당·[[015_virtualization|가상화]] 토폴로지까지 함께 맞춰야 비로소 [[282_performance_tactics|성능]] 이점을 얻는다.

---

## Ⅰ. 개요 및 필요성

[[377_numa_allocation|NUMA]] ([[377_numa_allocation|Non-Uniform Memory Access]])는 [[375_multiprocessor|다중 프로세서]] 시스템에서 메모리를 [[125_socket|소켓]] 가까이에 [[136_variance|분산]] 배치해 확장성을 확보하는 구조다. 핵심 배경은 UMA처럼 모든 CPU (Central Processing Unit)가 하나의 중앙 메모리 경로를 공유하면, 코어 수가 늘어날수록 메모리 컨트롤러와 인터커넥트에 병목이 집중된다는 점이다. 즉, 메모리를 하나로 묶으면 프로그래밍은 쉬워지지만, 하드웨어는 점점 더 비싼 정체 구간을 떠안게 된다.

특히 2소켓, 4소켓 서버에서는 각 [[125_socket|소켓]]이 동시에 대용량 메모리 요청을 발생시키므로, 단일 [[344_bus|버스]] 기반 구조는 [[140_bandwidth|대역폭]]과 [[015_지연_데이터_관점|지연]]시간을 함께 감당하기 어렵다. NUMA는 이 문제를 해결하기 위해 "메모리는 [[136_variance|분산]]하되 주소 공간은 공유"하는 절충안을 택했다. 덕분에 응용프로그램은 여전히 하나의 큰 메모리를 쓰는 것처럼 보지만, 실제로는 로컬 메모리와 원격 메모리를 구분하는 물리적 차이가 생긴다.

아래 그림은 UMA의 중앙 집중 병목이 왜 NUMA로 바뀌는지를 보여준다.

```text
┌─────────────────────────── UMA vs NUMA 전환 이유 ───────────────────────────┐
│                                                                           │
│ UMA: 모든 CPU가 하나의 메모리 길목으로 몰림                               │
│                                                                           │
│  [CPU0]   [CPU1]   [CPU2]   [CPU3]                                        │
│     │        │        │        │                                          │
│     └────────┴────────┴────────┴────────┐                                 │
│                                          ▼                                 │
│                              [공유 메모리 / 단일 병목]                    │
│                                                                           │
│ NUMA: 소켓마다 가까운 메모리를 두고, 필요할 때만 서로 건너감              │
│                                                                           │
│  [Socket0]──Local──[Mem0]      [Socket1]──Local──[Mem1]                   │
│      └─────────────── Interconnect ───────────────┘                       │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

NUMA를 기억할 때 가장 중요한 문장은 "확장성을 얻기 위해 균일성을 포기한 구조"다. 메모리 접근 시간이 더 이상 모두 같지 않기 때문에, [[001_operating_system_purpose|운영체제]]와 응용프로그램은 [[001_dikw_pyramid|데이터]]가 어느 노드에 놓이는지 신경 써야 한다.

📢 섹션 요약 비유: UMA가 큰 사무실 한가운데 복사기 1대를 두는 방식이라면, NUMA는 부서마다 복사기를 두고 급할 때만 다른 부서 복사기를 빌려 쓰는 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[377_numa_allocation|NUMA]] 시스템은 보통 "[[125_socket|소켓]] + 로컬 메모리 + 노드 간 연결"의 형태로 구성된다. 하나의 [[377_numa_allocation|NUMA]] 노드에는 CPU [[125_socket|소켓]], 메모리 컨트롤러, 그 [[125_socket|소켓]]에 직접 연결된 [[251_dram|DRAM]] (Dynamic Random Access Memory)이 묶여 있다. 이때 같은 노드의 메모리를 읽는 것은 로컬 접근이고, 다른 노드의 메모리를 읽는 것은 원격 접근이다.

핵심은 소프트웨어가 보는 주소 공간은 하나지만, 하드웨어는 각 물리 주소를 특정 홈 노드에 귀속시킨다는 점이다. 그래서 같은 load/store 명령이라도 어디에 있는 [[001_dikw_pyramid|데이터]]를 읽느냐에 따라 [[015_지연_데이터_관점|지연]]시간이 달라진다. 또한 현대 NUMA는 대개 ccNUMA (cache-coherent [[377_numa_allocation|NUMA]]) 형태이므로, 여러 노드에 걸쳐 [[402_cache_coherence|캐시 일관성]]까지 유지해야 한다.

| 구성 요소 | 역할 | [[282_performance_tactics|성능]] 영향 | 설계상 의미 |
| :-- | :-- | :-- | :-- |
| [[377_numa_allocation|NUMA]] 노드 | CPU [[125_socket|소켓]]과 로컬 메모리의 묶음 | 로컬 접근 시 가장 낮은 [[015_지연_데이터_관점|지연]]시간 | 확장 단위 |
| 로컬 메모리 | 해당 [[125_socket|소켓]]에 직접 연결된 메모리 | 높은 [[140_bandwidth|대역폭]], 낮은 [[015_지연_데이터_관점|지연]]시간 | 최우선 배치 대상 |
| 원격 메모리 | 다른 노드에 속한 메모리 | 인터커넥트 횡단으로 [[015_지연_데이터_관점|지연]] 증가 | 과도하면 [[282_performance_tactics|성능]] 급락 |
| 인터커넥트 | 노드 간 메모리 요청 전달 경로 | 홉 수와 [[140_bandwidth|대역폭]]이 병목 결정 | 멀티소켓 핵심 인프라 |
| [[402_cache_coherence|캐시 일관성]] | 노드 간 최신 [[001_dikw_pyramid|데이터]] 보장 | [[289_cqrs_db|쓰기]] 공유 시 트래픽 증가 | ccNUMA 필수 조건 |

아래 그림은 로컬 접근과 원격 접근의 차이를 보여준다.

```text
┌──────────────────────── NUMA 메모리 접근 경로 ────────────────────────┐
│                                                                       │
│                Local Access                      Remote Access         │
│                                                                       │
│  Core on Node0 ───────▶ Mem0               Core on Node0              │
│        │                   │                     │                     │
│        │                   └─ 같은 노드          └──────▶ Interconnect │
│        │                         (짧은 경로)                  │         │
│        │                                                      ▼         │
│        └────────────────────────────────────────────────────▶ Mem1       │
│                                                           (다른 노드)   │
│                                                                       │
│  결과: Local < Remote                                                 │
│        지연시간 감소, 대역폭 유리      지연시간 증가, 혼잡 시 편차 확대 │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

실무에서는 이 차이가 작게는 1.3배, 크게는 2배 이상으로 벌어질 수 있다. 특히 [[001_dikw_pyramid|데이터]] 구조를 여러 [[092_thread_lwp|스레드]]가 공유하며 [[289_cqrs_db|쓰기]]까지 섞이면, 원격 접근 비용에 [[402_cache_coherence|캐시 일관성]] 비용이 덧붙어 체감 [[282_performance_tactics|성능]]이 더 나빠진다. 그래서 [[377_numa_allocation|NUMA]] [[282_performance_tactics|성능]] 최적화의 핵심은 "연산하는 코어 가까이에 [[001_dikw_pyramid|데이터]]를 두는 것"이다.

📢 섹션 요약 비유: 내 책상 서랍에서 문서를 꺼내면 바로 읽을 수 있지만, 다른 층 캐비닛에서 가져오려면 이동 시간과 대기 시간이 같이 붙는 것과 같다.

---

## Ⅲ. 비교 및 연결

NUMA를 제대로 이해하려면 [[379_uma|UMA]], [[195_real_time_scheduling|SMP]] (Symmetric Multiprocessing), 그리고 [[136_variance|분산]] 메모리 구조와의 경계를 함께 봐야 한다. NUMA는 프로그래밍 모델 면에서는 [[118_shared_memory|공유 메모리]] 계열이지만, [[282_performance_tactics|성능]] 특성 면에서는 위치 인식이 필요한 준분산 구조에 가깝다.

| 비교 항목 | [[379_uma|UMA]] | [[377_numa_allocation|NUMA]] | [[378_distributed_memory|분산 메모리 시스템]] |
| :-- | :-- | :-- | :-- |
| 주소 공간 | 단일 | 단일 | 노드별 분리 |
| 메모리 접근 시간 | 거의 균일 | 위치에 따라 비균일 | 원격은 [[119_message_passing|메시지 전달]] |
| 확장성 | 제한적 | 중간~높음 | 매우 높음 |
| 프로그래밍 난이도 | 가장 낮음 | 튜닝 필요 | 가장 높음 |
| 대표 환경 | 소형 [[195_real_time_scheduling|SMP]] | 멀티소켓 서버 | 클러스터, MPP |

[[001_operating_system_purpose|운영체제]] 관점에서는 NUMA가 [[195_real_time_scheduling|SMP]] 스케줄링의 "평등성 가정"을 깨뜨린다. 전통적인 SMP는 어느 코어에 태워도 비슷한 메모리 [[282_performance_tactics|성능]]을 기대하지만, NUMA에서는 [[092_thread_lwp|스레드]] 이동이 곧 메모리 원격화로 이어질 수 있다. 그래서 Linux는 [[377_numa_allocation|NUMA]]-aware scheduler, first-touch [[164_policy|정책]], AutoNUMA 같은 기능을 통해 [[092_thread_lwp|스레드]]와 메모리의 지역성을 유지하려고 한다.

[[015_virtualization|가상화]] 관점에서는 vNUMA (virtual [[377_numa_allocation|NUMA]]) 노출이 중요하다. 하이퍼바이저가 큰 가상 머신을 여러 물리 노드에 걸쳐 배치하면서 게스트 [[001_operating_system_purpose|운영체제]]에 [[377_numa_allocation|NUMA]] 토폴로지를 숨기면, 게스트는 UMA처럼 오판하고 메모리를 비효율적으로 사용한다. 반대로 vNUMA를 적절히 노출하면 [[002_database_definition|데이터베이스]], Java [[598_vm_migration_nic|Virtual Machine]], 인메모리 분석 엔진이 노드 단위로 더 현명하게 메모리를 배치할 수 있다.

또한 NUMA는 [[497_chiplet|칩렛]] 기반 프로세서와도 연결된다. 최근에는 단일 [[125_socket|소켓]] 내부에서도 CCD (Core Complex Die), IOD (I/O Die) 같은 구조 차이로 메모리 접근 특성이 완전히 균일하지 않다. 즉, NUMA는 멀티소켓 서버만의 개념이 아니라 "물리적 거리 차이가 [[282_performance_tactics|성능]] 차이로 드러나는 모든 대형 시스템"을 읽는 관점이 되었다.

📢 섹션 요약 비유: NUMA는 한 건물 안에 있지만 부서별 창고 위치가 다른 회사와 같아서, 같은 회사 규칙을 따르더라도 물건이 어디 있느냐에 따라 일의 속도가 달라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

[[377_numa_allocation|NUMA]] 환경에서는 "CPU 사용률이 높다"보다 "원격 메모리 비율이 높다"가 더 직접적인 병목 신호일 수 있다. 따라서 고성능 서버에서는 단순 코어 수보다 노드 수, 노드별 메모리 용량, 워크로드의 메모리 지역성을 함께 봐야 한다. 특히 [[002_database_definition|데이터베이스]], JVM (Java [[598_vm_migration_nic|Virtual Machine]]), in-memory cache, 대용량 분석 엔진은 [[377_numa_allocation|NUMA]] 민감도가 높다.

### 실무 판단 포인트

1. **대형 [[002_database_definition|데이터베이스]]**
   - 채택: [[125_socket|소켓]]별 메모리 [[140_bandwidth|대역폭]]이 필요하고, 버퍼 풀을 노드별로 잘 활용할 수 있을 때
   - 주의: 특정 노드에만 메모리가 몰리면 전체 메모리가 남아도 로컬 부족으로 [[282_performance_tactics|성능]]이 무너질 수 있음

2. **저지연 트레이딩·게임 서버**
   - 채택: [[092_thread_lwp|스레드]] 고정과 메모리 고정이 가능할 때
   - 회피: [[092_thread_lwp|스레드]] 이동이 잦고 객체 공유가 많은 구조라면 [[377_numa_allocation|NUMA]] 이점이 줄어듦

3. **[[015_virtualization|가상화]]·클라우드 환경**
   - 채택: vNUMA 토폴로지를 손님 [[001_operating_system_purpose|운영체제]]에 맞게 노출할 수 있을 때
   - 회피: 물리 배치를 숨긴 채 큰 VM만 제공하면 예측 불가능한 [[015_지연_데이터_관점|지연]]이 발생함

아래 진단 흐름은 [[377_numa_allocation|NUMA]] 튜닝의 기본 사고방식을 요약한다.

```text
┌──────────────────── NUMA 병목 진단 흐름 ────────────────────┐
│                                                             │
│  성능 저하 발생                                              │
│        │                                                     │
│        ▼                                                     │
│  원격 메모리 접근 비율이 높은가?                            │
│        │                                                     │
│   ┌────┴────┐                                                │
│   │         │                                                │
│  예        아니오                                            │
│   │         │                                                │
│   ▼         ▼                                                │
│ 스레드-메모리  락 경합, I/O, 알고리즘 병목 등                │
│ 지역성 점검    다른 원인 우선 확인                          │
│   │                                                          │
│   ▼                                                          │
│ CPU pinning / 메모리 바인딩 / interleave 정책 검토          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

기술사 관점에서 기억할 체크리스트는 분명하다. 첫째, 멀티소켓 서버를 단일 대형 자원으로만 보지 말고 노드 단위로 본다. 둘째, first-touch [[164_policy|정책]]이 워크로드에 유리한지, 아니면 interleave가 더 안정적인지 판단한다. 셋째, 모니터링 시 CPU 사용률뿐 아니라 [[377_numa_allocation|NUMA]] [[263_cache_hit_miss|hit]]/miss, remote access, [[286_page_frame|page]] migration 지표를 함께 본다.

📢 섹션 요약 비유: [[377_numa_allocation|NUMA]] 서버 운영은 큰 창고 하나를 보는 일이 아니라 여러 창고의 재고와 동선을 함께 맞추는 물류 운영과 같다.

---

## Ⅴ. 기대효과 및 결론

NUMA의 가장 큰 효과는 대형 서버의 확장 한계를 뒤로 미룬다는 점이다. [[125_socket|소켓]]마다 메모리 채널과 [[140_bandwidth|대역폭]]을 붙여 주기 때문에, 코어 수와 메모리 용량이 커져도 UMA보다 훨씬 현실적인 [[282_performance_tactics|성능]]을 낼 수 있다. 이는 대규모 [[002_database_definition|데이터베이스]], [[015_virtualization|가상화]] 호스트, [[548_automotive_hpc|HPC]] ([[226_hpc_supercomputing_infrastructure|High Performance Computing]]) 노드, [[190_ai_llm_requirements_specification|AI]] 전처리 서버 같은 메모리 집약적 환경에서 특히 중요하다.

반면 NUMA는 "추상적으로는 [[118_shared_memory|공유 메모리]], 실제로는 위치 민감형 구조"라는 이중성을 가진다. 이 때문에 잘 설계하면 큰 이득을 얻지만, 무심코 쓰면 오히려 원격 접근과 [[402_cache_coherence|캐시 일관성]] 오버헤드만 떠안는다. 즉 NUMA는 자동으로 빠른 기술이 아니라, locality-aware 설계가 뒷받침될 때 빠른 기술이다.

앞으로는 [[441_cxl|CXL]] ([[441_cxl|Compute Express Link]]) 기반 메모리 확장, [[497_chiplet|칩렛]] 기반 프로세서, 서브 [[377_numa_allocation|NUMA]] 클러스터링처럼 "메모리 위치를 더 세밀하게 다루는 구조"가 늘어날 가능성이 높다. 따라서 NUMA는 단순 암기 항목이 아니라, 현대 시스템이 왜 점점 더 "거리"를 의식하게 되는지를 설명하는 핵심 관점으로 기억해야 한다.

📢 섹션 요약 비유: NUMA는 도시를 키우기 위해 동네별 물류창고를 만든 방식이라서, 길만 잘 설계하면 도시가 훨씬 커질 수 있지만 동선이 꼬이면 오히려 더 느려진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [[379_uma|UMA]] ([[379_uma|Uniform Memory Access]]) | 모든 메모리 접근 시간이 거의 같은 구조로, NUMA의 비교 기준이 된다. |
| ccNUMA (cache-coherent [[377_numa_allocation|NUMA]]) | [[377_numa_allocation|NUMA]] 위에서 [[402_cache_coherence|캐시 일관성]]을 유지하는 현대 서버의 일반적 형태다. |
| [[195_real_time_scheduling|SMP]] (Symmetric Multiprocessing) | [[001_operating_system_purpose|운영체제]]가 여러 프로세서를 대등하게 다루는 모델이며, NUMA에서는 이 스케줄링이 지역성을 고려해야 한다. |
| First-Touch [[164_policy|Policy]] | 처음 접근한 CPU가 속한 노드에 메모리를 우선 할당해 지역성을 높이는 [[164_policy|정책]]이다. |
| vNUMA (virtual [[377_numa_allocation|NUMA]]) | 가상 머신에 [[377_numa_allocation|NUMA]] 토폴로지를 노출해 게스트 [[001_operating_system_purpose|운영체제]]가 올바른 메모리 배치를 하도록 돕는다. |
| CPU Pinning | [[092_thread_lwp|스레드]]를 특정 코어 또는 노드에 묶어 원격 메모리 접근을 줄이는 실무 기법이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
공유 메모리 확장 요구
    │
    ▼
UMA (Uniform Memory Access)
    │
    ├─ 코어 증가에 따른 중앙 메모리 병목
    ▼
NUMA (Non-Uniform Memory Access)
    │
    ├─ 캐시 일관성 강화
    ▼
ccNUMA (cache-coherent NUMA)
    │
    ├─ 운영체제/가상화 최적화
    ▼
First-Touch · AutoNUMA · vNUMA
    │
    ├─ 더 큰 메모리 풀 요구
    ▼
Chiplet NUMA · CXL 기반 메모리 확장
```

이 흐름은 "[[118_shared_memory|공유 메모리]]의 단순성 유지 → 확장성 한계 노출 → 위치 인식형 최적화 → [[369_memory_pool|메모리 풀]] 확장"으로 발전하는 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. NUMA는 큰 학교에서 교실마다 자기 사물함을 두고, 필요하면 다른 반 사물함도 빌려 쓰는 방식이에요.
2. 내 반 사물함은 가깝고 빠르지만, 다른 반 사물함은 멀어서 가져오는 데 시간이 더 걸려요.
3. 그래서 공부를 빨리하려면 내가 자주 쓰는 책을 내 반 사물함 가까이에 두는 게 중요해요.
