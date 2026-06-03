---
title: 767. 좀비로드 (ZombieLoad)
date: '2026-05-08'
tags:
- studynote-computer-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 좀비로드 (ZombieLoad)는 필 버퍼 (Fill Buffer)에 남아 있는 최근 로드 [[001_dikw_pyramid|데이터]]를, 예외나 보조 처리로 중단될 로드 명령이 투기적으로 받아 가게 만들어 샘플링하는 [[764_mds|MDS]] ([[380_mds_attack|Microarchitectural Data Sampling]]) 공격이다.
> 2. **가치**: 특정 주소를 정밀하게 읽는 방식은 아니지만, 같은 물리 코어에서 지나간 웹 요청, 키 입력, 가상 머신 메모리 트래픽 같은 연속적 [[001_dikw_pyramid|데이터]] 조각을 대량으로 모아 복원할 수 있다.
> 3. **판단 포인트**: 좀비로드 완화의 핵심은 마이크로코드 기반 버퍼 클리어와 동일 코어 공유 억제이며, 후속 변종까지 고려하면 Intel TSX (Transactional [[212_synchronization_mechanisms|Synchronization]] Extensions) 사용 여부도 함께 점검해야 한다.

---

## Ⅰ. 개요 및 필요성

좀비로드 (ZombieLoad)는 이름 그대로 "죽었어야 할 [[001_dikw_pyramid|데이터]]가 다시 살아나 보이는" 현상을 악용한다. 정상적으로는 실패하거나 취소되어야 할 로드 명령이, 파이프라인 정리 전에 필 버퍼에 남은 바이트를 잠깐 받아 버리고 그 흔적을 공격자가 캐시 부채널로 관측한다. 이 때문에 공격자는 자신이 권한 없는 주소를 읽지 못해도, 같은 코어를 스쳐 지나간 최근 [[001_dikw_pyramid|데이터]]의 조각을 계속 주워 모을 수 있다.

이 공격이 위험한 이유는 결과가 매우 실용적이기 때문이다. 웹 브라우저 탭, 사용자 프로세스, [[022_kernel_role|커널]], 가상 머신은 소프트웨어적으로 분리되어 있어도, 같은 물리 코어 위에서 실행되면 동일한 필 버퍼 구조를 공유한다. 따라서 공격자는 고정된 한 값을 뽑아내기보다, 피해자의 활동에서 흘러나온 "[[001_dikw_pyramid|데이터]] 흐름" 자체를 [[701_sniffing_eavesdropping_promiscuous|도청]]하는 쪽에 더 가깝게 행동한다.

좀비로드는 결국 [[282_performance_tactics|성능]]을 위해 촘촘히 연결된 로드 경로가, 보안 관점에서는 공용 환풍구가 될 수 있음을 보여줬다. 눈에 보이지 않는 하드웨어 내부 재사용이 얼마나 넓은 공격면을 만드는지 설명하는 대표 사례다.

- **📢 섹션 요약 비유**: 좀비로드는 잠깐 버려진 메모를 다시 살아난 것처럼 주워 읽는 공격이라서, 쓰레기통이 아니라 복도 위 공용 쪽지판을 훔쳐보는 것과 비슷하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

필 버퍼는 L1 캐시에 없는 캐시 라인을 하위 캐시나 메모리에서 가져올 때 잠깐 붙잡아 두는 구조다. 정상 동작에서는 [[001_dikw_pyramid|데이터]]가 곧바로 L1로 전달되고 버퍼는 다음 요청에 재사용된다. 그러나 잘못된 로드, 예외, [[720_page_fault_isr|페이지 폴트]], [[527_hardware_assisted_virtualization|하드웨어 보조]] 처리 같은 상황이 끼어들면, 파이프라인이 취소되기 전의 아주 짧은 순간에 이전 요청의 바이트가 새로운 로드 흐름에 섞여 들어갈 수 있다.

| 단계 | 정상 동작 | ZombieLoad 노출 지점 |
| :--- | :--- | :--- |
| 피해자 로드 | 캐시 라인이 Fill Buffer를 거쳐 올라옴 | 최근 [[001_dikw_pyramid|데이터]] 조각이 잠깐 잔류 |
| 공격자 로드 | 예외를 일으키면 폐기되어야 함 | 폐기 전 stale byte가 transient path에 반영 |
| 부채널 인코딩 | 정상적으로는 외부에 안 보임 | 캐시 흔적으로 값 추정 가능 |
| 반복 샘플링 | 의미 없는 잡음일 수 있음 | 여러 번 합치면 유의미한 문자열·포인터 복원 |

다음 그림은 좀비로드가 "실패한 로드"를 이용해 필 버퍼의 잔상을 빼내는 흐름을 보여준다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ ZombieLoad leak path                                              │
├────────────────────────────────────────────────────────────────────┤
│ Victim load traffic ──▶ Fill Buffer ──▶ L1 cache                  │
│                            │                                       │
│                            └─ stale bytes remain briefly           │
│                                       │                            │
│ Attacker invalid load ── transient consume ──▶ cache decode       │
└────────────────────────────────────────────────────────────────────┘
```

공격자는 보통 의미 있는 한 번의 읽기를 기대하지 않는다. 대신 수천~수백만 번의 로드를 반복하면서 어떤 바이트가 얼마나 자주 나타나는지 통계적으로 모은다. 이 성격 때문에 좀비로드는 비밀번호 한 글자, 포인터 일부, [[461_http_stateless_connection_oriented|HTTP]] 헤더 조각처럼 "흐름 속 [[001_dikw_pyramid|데이터]]"를 엿듣는 데 강하다.

중요한 점은 좀비로드가 캐시만의 문제가 아니라 로드 파이프라인 전체의 문제라는 사실이다. 로드가 실패했더라도 그 직전의 transient state가 관찰 가능하면 공격 표면은 남는다.

- **📢 섹션 요약 비유**: 사서가 잘못된 책을 찾으러 갔다가 돌아오기 전, 직전 손님의 책갈피가 잠깐 밖으로 보이는 순간을 [[148_5g_embb_urllc_mmtc|초고속]] 카메라로 계속 찍는 것이 좀비로드다.

---

## Ⅲ. 비교 및 연결

좀비로드는 [[765_ridl_attack|RIDL]], 폴아웃과 함께 [[764_mds|MDS]] 계열을 이루지만, 가장 상징적인 차별점은 필 버퍼를 통한 "연속 로드 트래픽 [[701_sniffing_eavesdropping_promiscuous|도청]]" 이미지가 강하다는 점이다. RIDL이 더 넓은 load path [[056_표본화_Sampling|sampling]] 개념에 가깝고, 폴아웃이 store path에 집중한다면, 좀비로드는 fill-buffer 관측을 통해 피해자의 활동 흐름을 잡아내는 데 특화돼 있다.

| 공격 | 핵심 표적 | 주로 새는 것 | 실무 판단 포인트 |
| :--- | :--- | :--- | :--- |
| ZombieLoad | Fill Buffer | 최근 로드 [[001_dikw_pyramid|데이터]] 흐름 | 동일 코어 공존 금지 여부 |
| [[765_ridl_attack|RIDL]] | LFB, Load [[446_port_and_bus|Port]] | in-flight [[074_byte|byte]] 전반 | 광범위 샘플링 대응 |
| [[766_fallout_attack|Fallout]] | Store Buffer | 저장 직전 값과 포인터 | KASLR 우회, [[022_kernel_role|커널]] 흔적 차단 |

또한 좀비로드는 후속 변종과도 연결된다. 특히 TAA (TSX Asynchronous Abort)는 Intel TSX를 사용하는 경로에서 유사한 transient [[056_표본화_Sampling|sampling]] 창을 다시 열어, "버퍼를 비우는 것"과 함께 "불필요한 TSX를 끌 것인가"라는 운영 결정을 추가로 요구했다. 즉 좀비로드는 단일 CVE로 끝난 문제가 아니라, 동일한 설계 철학에서 반복적으로 나타난 누수 패턴을 상징한다.

클라우드와 브라우저 샌드박스 관점에서 보면 이 공격은 더욱 현실적이다. 공격자가 피해자의 메모리 주소를 몰라도, 같은 코어에 공존하기만 하면 충분한 잡음을 모아 유의미한 정보로 바꿀 수 있기 때문이다.

- **📢 섹션 요약 비유**: RIDL이 공용 복도의 여러 서류를 넓게 스캔하는 느낌이라면, 좀비로드는 책 반납 카트에서 방금 읽은 책 제목들을 줄줄이 훔쳐보는 느낌에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

좀비로드 대응은 하드웨어·[[001_operating_system_purpose|운영체제]]·스케줄러가 같이 움직여야 한다. 우선 최신 BIOS/[[706_uefi|UEFI]] (Basic Input/Output System / Unified Extensible [[032_firmware|Firmware]] Interface) 마이크로코드와 [[001_operating_system_purpose|운영체제]] 패치를 적용해 사용자↔[[022_kernel_role|커널]], 프로세스↔프로세스, [[598_vm_migration_nic|VM]]↔[[598_vm_migration_nic|VM]] 전환 시 필 버퍼를 포함한 내부 버퍼를 청소하도록 해야 한다. [[310_multi_tenant_database_architecture|멀티테넌트]] 서버나 고보안 시스템에서는 여기에 [[400_smt|동시 멀티스레딩]]([[400_smt|SMT]], Simultaneous [[095_multithreading_benefits|Multithreading]]) 비활성화 또는 전용 코어 할당이 추가된다.

후속 변종까지 고려하면 TSX 정책도 중요하다. 애플리케이션이 TSX를 거의 쓰지 않는다면 비활성화가 가장 단순한 선택일 수 있다. 반대로 락 elision 같은 이유로 TSX 의존도가 높다면, 기능 이점과 보안 비용을 숫자로 비교해야 한다. 일반적으로 버퍼 클리어만 적용했을 때는 저한릿수 [[282_performance_tactics|성능]] 손실이 흔하지만, [[400_smt|SMT]] 비활성화까지 포함하면 [[430_index_fast_full_scan|병렬]] [[139_throughput|처리량]]이 [[489_raid_10_hybrid|10]]~30% 감소할 수 있다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. 마이크로코드와 [[022_kernel_role|커널]]이 [[764_mds|MDS]]/ZombieLoad 완화 기능을 모두 활성화하고 있는가?
2. [[310_multi_tenant_database_architecture|멀티테넌트]]·브라우저 렌더링·비밀 키 처리 같은 워크로드에서 동일 코어 공존을 허용하고 있지 않은가?
3. Intel TSX 사용 여부를 확인하고, 필요 없으면 비활성화할 계획이 있는가?
4. 패치 적용 전후의 지연시간, [[139_throughput|처리량]], [[033_context|컨텍스트]] 전환 비용을 실측했는가?

기술사 관점에서는 "[[282_performance_tactics|성능]] 최적화 기능을 얼마나 남길지"를 [[090_service_kubernetes_network_load_balancing|서비스]] 등급별로 나누는 것이 중요하다. 모든 시스템에서 동일한 정책을 강요하기보다, 고보안 구간은 보수적으로, 일반 구간은 측정 기반으로 선택하는 식의 계층적 대응이 현실적이다.

- **📢 섹션 요약 비유**: 좀비로드 대응은 호텔 방 문만 잠그는 것이 아니라, 공용 환풍구를 막고 손님 배치를 다시 짜는 운영 매뉴얼을 세우는 일과 비슷하다.

---

## Ⅴ. 기대효과 및 결론

좀비로드 완화가 제대로 적용되면 최소한 같은 물리 코어에 함께 있었다는 이유만으로 다른 프로세스나 VM의 최근 로드 [[001_dikw_pyramid|데이터]] 흐름이 새는 위험을 크게 줄일 수 있다. 이는 클라우드 격리, 브라우저 샌드박스, 키 관리 [[090_service_kubernetes_network_load_balancing|서비스]] 같은 현대 컴퓨팅의 기본 신뢰를 유지하는 데 중요하다.

하지만 장기적으로는 하드웨어가 실패한 로드의 transient [[272_state_pattern|state]] 자체를 더 엄격히 다뤄야 한다. 필 버퍼를 문맥별로 분리하고, 실패한 로드가 민감한 바이트를 마이크로상태에 남기지 않도록 설계해야 한다. 좀비로드는 "죽은 [[001_dikw_pyramid|데이터]]는 정말 죽었는가"를 하드웨어 설계자가 끝까지 확인해야 함을 가르친다.

- **📢 섹션 요약 비유**: 앞으로의 CPU는 반납된 책갈피가 다음 손님 앞에 다시 나타나지 않도록, 반납 카트를 즉시 봉인하는 도서관처럼 바뀌어야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 필 버퍼 (Fill Buffer) | 좀비로드의 직접 표적이 되는 로드 경유 버퍼 |
| [[764_mds|MDS]] ([[380_mds_attack|Microarchitectural Data Sampling]]) | [[765_ridl_attack|RIDL]], [[766_fallout_attack|Fallout]], ZombieLoad를 묶는 상위 취약점 계열 |
| [[400_smt|SMT]] (Simultaneous [[095_multithreading_benefits|Multithreading]]) | 같은 물리 코어의 버퍼 공유를 통해 공격면을 키움 |
| TAA (TSX Asynchronous Abort) | 좀비로드 이후 같은 설계 철학의 변종으로 확장된 사례 |
| MD_CLEAR / VERW | 문맥 전환 시 내부 버퍼를 청소하는 대표 완화 메커니즘 |

### 📈 관련 키워드 및 발전 흐름도

```text
Out-of-Order load path
    │
    ▼
Fill Buffer reuse
    │
    ▼
Fault / Assist / Abort window
    │
    ▼
ZombieLoad sampling
    │
    ▼
MD_CLEAR + SMT / TSX policy
```

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터는 책을 옮길 때 잠깐 놓아 두는 작은 책상이 있어요.
2. 좀비로드는 나쁜 친구가 그 책상에 남은 책갈피를 계속 훔쳐보며 누가 무슨 책을 읽었는지 맞추는 공격이에요.
3. 그래서 컴퓨터는 사람이나 일이 바뀔 때마다 그 책상을 바로 치우고, 중요한 손님은 같은 책상을 같이 안 쓰게 해야 해요.
