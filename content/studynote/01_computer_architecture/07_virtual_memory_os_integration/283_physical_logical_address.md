---
title: 283. 물리 주소와 논리 주소 (Physical vs Logical Address)
date: '2026-04-20'
tags:
- studynote-computer-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[322_logical_virtual_address|논리 주소]] (Logical Address)는 프로세스가 바라보는 작업용 주소 공간이고, [[323_physical_address|물리 주소]] ([[323_physical_address|Physical Address]])는 실제 주기억장치인 RAM (Random Access Memory) 칩에 찍히는 하드웨어 주소다.
> 2. **가치**: 이 둘을 분리하면 모든 프로세스가 자기만의 0번지부터 시작하는 것처럼 실행되므로 [[307_memory_protection|메모리 보호]], 재배치, 멀티태스킹이 동시에 가능해진다.
> 3. **판단 포인트**: 핵심은 주소를 "많이 주는 것"이 아니라, [[328_mmu|MMU]] ([[284_mmu|Memory Management Unit]])가 [[322_logical_virtual_address|논리 주소]]를 얼마나 빠르고 안전하게 [[323_physical_address|물리 주소]]로 번역하느냐에 있다.

---

## Ⅰ. 개요 및 필요성

[[323_physical_address|물리 주소]]와 [[322_logical_virtual_address|논리 주소]]의 분리는 프로그램이 보는 메모리 세계와 하드웨어가 가진 실제 메모리 배치를 분리하는 구조다. 프로그램은 보통 자신의 코드, [[057_stack|스택]], 힙이 연속된 하나의 공간에 있다고 생각하지만, 실제 RAM은 운영체제가 여러 프로세스와 [[022_kernel_role|커널]], 입출력 버퍼를 섞어 배치한 조각난 공간일 수 있다. 이 간극을 그대로 노출하면 프로그램은 "내 [[001_dikw_pyramid|데이터]]가 실제 어디 있는지"를 매번 알아야 하고, 다른 프로그램의 영역을 침범할 위험도 커진다.

이 개념이 필요해진 이유는 멀티프로그래밍과 [[307_memory_protection|메모리 보호]] 때문이다. 하나의 물리 메모리를 여러 작업이 함께 쓰는 순간, 주소 체계를 분리하지 않으면 프로그램 충돌이 곧 시스템 장애로 이어진다. 반대로 [[322_logical_virtual_address|논리 주소]]를 도입하면 프로세스는 항상 같은 형태의 주소 공간을 사용하고, 운영체제는 뒤에서 실제 배치만 바꿔 끼우면 된다.

아래 그림은 "프로세스가 보는 주소"와 "하드웨어가 접근하는 주소"가 다른 계층에 속한다는 점을 보여준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│               주소 가상화의 핵심: 보는 주소와 찍히는 주소 분리      │
├──────────────────────────────────────────────────────────────────────┤
│ 프로세스 A                                                          │
│   load 0x0040  ─┐                                                   │
│                 ├─▶ MMU (Memory Management Unit) ─▶ 물리 0x9A40     │
│ store 0x1F20 ───┘                                                   │
│                                                                      │
│ 프로세스 B                                                          │
│   load 0x0040  ─┐                                                   │
│                 ├─▶ MMU (Memory Management Unit) ─▶ 물리 0x2C40     │
│ store 0x1F20 ───┘                                                   │
│                                                                      │
│ 같은 논리 주소라도 프로세스가 다르면 다른 물리 주소로 번역될 수 있다 │
└──────────────────────────────────────────────────────────────────────┘
```

중요한 점은 CPU (Central Processing Unit)가 직접 [[323_physical_address|물리 주소]]를 계산하지 않는다는 것이다. CPU는 [[158_instruction|명령어]]가 요구하는 [[322_logical_virtual_address|논리 주소]]만 내보내고, 실제 배치 정보는 운영체제가 만든 매핑 자료와 MMU가 처리한다. 덕분에 프로그램은 이식성과 단순성을 얻고, 시스템은 [[571_protection_vs_security|보호]]와 유연성을 얻는다.

**📢 섹션 요약 비유**: 아파트 입주자는 "우리 집은 101호"만 알면 되지만, 관리실은 그 101호가 어느 동 몇 층 배관과 연결되는지까지 안다. [[322_logical_virtual_address|논리 주소]]는 세입자 관점의 호수이고, [[323_physical_address|물리 주소]]는 관리실이 보는 실제 배관도다.

---

## Ⅱ. 아키텍처 및 핵심 원리

주소 변환은 [[158_instruction|명령어]] 실행 경로 한가운데에서 일어난다. CPU가 [[322_logical_virtual_address|논리 주소]]를 만들면 MMU는 이를 [[286_page_frame|페이지]] 번호와 오프셋으로 나누고, [[353_page_table|페이지 테이블]] ([[353_page_table|Page Table]])에서 대응되는 물리 프레임을 찾는다. 이때 오프셋은 그대로 유지되고, 앞부분의 [[286_page_frame|페이지]] 번호만 물리 프레임 번호로 바뀐다. 즉 변환의 핵심은 "상대 위치는 유지하되, 어느 실제 블록에 꽂을지만 바꾸는 것"이다.

속도를 위해 대부분의 시스템은 [[357_tlb|TLB]] ([[291_tlb|Translation Lookaside Buffer]])라는 변환 캐시를 함께 둔다. TLB에 있으면 주소 변환은 거의 즉시 끝나지만, 없으면 [[353_page_table|페이지 테이블]]을 추가로 읽어야 하므로 [[015_지연_데이터_관점|지연]]이 커진다. 그래서 물리/[[322_logical_virtual_address|논리 주소]] 구조는 단순 [[571_protection_vs_security|보호]] 기능이 아니라, 캐시 지역성·[[352_page_size|페이지 크기]]·[[211_context_switch|문맥 교환]] 비용까지 엮이는 [[282_performance_tactics|성능]] 설계 문제이기도 하다.

| 구성 요소 | 역할 | 핵심 포인트 |
| :-- | :-- | :-- |
| CPU | [[322_logical_virtual_address|논리 주소]] [[087_process_state_transition|생성]] | [[158_instruction|명령어]]가 [[316_reference_pattern_nosql|참조]]하는 주소는 기본적으로 [[322_logical_virtual_address|논리 주소]] |
| [[328_mmu|MMU]] | [[369_logic_bomb|논리]]→[[323_physical_address|물리 주소]] 변환 | [[571_protection_vs_security|보호]] [[073_bit|비트]], 접근 권한, [[286_page_frame|페이지]] 존재 여부 [[396_validation|확인]] |
| [[353_page_table|페이지 테이블]] | 매핑 정보 보관 | [[286_page_frame|페이지]] 번호와 물리 프레임 번호 대응 |
| [[357_tlb|TLB]] | 최근 변환 결과 캐시 | 변환 [[015_지연_데이터_관점|지연]] 감소, [[211_context_switch|문맥 교환]] 시 관리 필요 |
| RAM | 실제 [[001_dikw_pyramid|데이터]] 저장 | 최종 [[323_physical_address|물리 주소]]를 받아 읽기/[[289_cqrs_db|쓰기]] 수행 |

아래 흐름도는 주소 변환 과정에서 병목과 예외가 어디서 생기는지 보여준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│                 논리 주소가 물리 주소가 되기까지의 경로             │
├──────────────────────────────────────────────────────────────────────┤
│ CPU가 논리 주소 생성                                                │
│        │                                                            │
│        ▼                                                            │
│ 페이지 번호 + 오프셋 분리                                           │
│        │                                                            │
│        ▼                                                            │
│ TLB 조회 ────────────────┬───────────────▶ 적중(Hit)                │
│        │                 │                     │                     │
│        │                 └───────────────▶ 미적중(Miss)             │
│        │                                       │                     │
│        │                                       ▼                     │
│        │                              페이지 테이블 조회            │
│        │                                       │                     │
│        ▼                                       ▼                     │
│ 권한 확인 / 존재 확인                    프레임 번호 획득            │
│        │                                                            │
│        ├─ 실패 ▶ 페이지 폴트 (Page Fault) / 보호 예외               │
│        │                                                            │
│        ▼                                                            │
│ 물리 프레임 번호 + 오프셋 결합                                      │
│        │                                                            │
│        ▼                                                            │
│ RAM 접근                                                            │
└──────────────────────────────────────────────────────────────────────┘
```

예를 들어 4킬로바이트(KB) [[286_page_frame|페이지]]를 쓰는 시스템에서 [[322_logical_virtual_address|논리 주소]]의 하위 12비트는 오프셋으로 그대로 유지된다. 상위 [[073_bit|비트]]만 다른 물리 프레임으로 바뀌므로, 프로그램은 연속 공간처럼 보이는 메모리를 사용하면서도 운영체제는 실제 RAM을 떨어진 여러 프레임에 나누어 배치할 수 있다. 이것이 [[381_virtual_memory|가상 메모리]]의 유연성, 그리고 [[307_memory_protection|메모리 보호]]의 기술적 출발점이다.

**📢 섹션 요약 비유**: 택배 송장은 "아파트 101호"만 적지만, 물류센터는 내부 [[104_classification_analysis|분류]]표를 보고 실제 배송 차량과 구역을 정한다. 주소 변환은 호수를 택배 동선으로 바꾸는 [[104_classification_analysis|분류]] 작업과 같다.

---

## Ⅲ. 비교 및 연결

이 개념을 제대로 이해하려면 [[322_logical_virtual_address|논리 주소]]와 [[323_physical_address|물리 주소]]를 단순 정의로 외우지 말고, 각각이 어떤 계층의 책임인지 구분해야 한다. [[322_logical_virtual_address|논리 주소]]는 프로그램 실행 모델을 위한 추상화이고, [[323_physical_address|물리 주소]]는 메모리 하드웨어 제어를 위한 실체다. 따라서 두 주소는 숫자 체계가 다른 것이 아니라 "누구를 위해 존재하는가"가 다르다.

| 비교 항목 | [[322_logical_virtual_address|논리 주소]] (Logical Address) | [[323_physical_address|물리 주소]] ([[323_physical_address|Physical Address]]) |
| :-- | :-- | :-- |
| 관점 | 프로세스/[[158_instruction|명령어]] 관점 | 메모리 하드웨어 관점 |
| [[087_process_state_transition|생성]] 시점 | CPU가 메모리 [[316_reference_pattern_nosql|참조]] 시 [[087_process_state_transition|생성]] | [[328_mmu|MMU]] 변환 후 확정 |
| 연속성 | 연속된 공간처럼 보임 | 실제 프레임 단위로 흩어질 수 있음 |
| [[571_protection_vs_security|보호]] [[164_policy|정책]] | 접근 권한의 대상 | 실제 접근 위치의 대상 |
| 변경 가능성 | 프로세스는 보통 동일한 [[369_logic_bomb|논리]] 구조 유지 | 시스템 상태에 따라 재배치 가능 |

또한 이 주제는 운영체제의 여러 개념과 직접 연결된다. [[353_page_table|페이지 테이블]]은 주소 번역의 지도이고, [[720_page_fault_isr|페이지 폴트]] ([[387_page_fault|Page Fault]])는 필요한 [[286_page_frame|페이지]]가 아직 RAM에 없음을 뜻한다. [[211_context_switch|문맥 교환]] ([[211_context_switch|Context Switch]])은 단순히 CPU 레지스터만 바꾸는 작업이 아니라, 어떤 주소 공간을 기준으로 번역할지도 함께 전환하는 작업이다. 여기에 [[374_aslr|ASLR]] (Address Space Layout Randomization)을 더하면 같은 프로그램도 실행할 때마다 다른 [[322_logical_virtual_address|논리 주소]] 배치를 사용해 공격 난도를 높일 수 있다.

경계 비교를 하나 더 하자면, [[323_physical_address|물리 주소]]는 [[746_io_direct_memory_access_dma|DMA]] ([[318_dma|Direct Memory Access]]) 같은 장치 입장에서는 중요하지만 일반 애플리케이션 입장에서는 감춰져야 한다. 장치는 실제 메모리 위치와 [[001_dikw_pyramid|데이터]]를 주고받아야 하지만, 사용자 프로그램까지 [[323_physical_address|물리 주소]]를 직접 만지게 하면 [[571_protection_vs_security|보호]] 경계가 무너진다. 즉 "보여주지 않는 것" 자체가 보안 아키텍처의 일부다.

**📢 섹션 요약 비유**: 여행 앱의 지도 화면은 사용자가 보기 쉬운 관광 지도이고, 실제 도로 관리청의 좌표 [[001_dikw_pyramid|데이터]]는 공사와 통제를 위한 관리 지도다. 둘 다 같은 도시를 다루지만 목적과 책임이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 "[[322_logical_virtual_address|논리 주소]]를 쓰느냐"가 선택지가 아니라, 그 변환 비용과 [[571_protection_vs_security|보호]] [[164_policy|정책]]을 어떻게 다루느냐가 판단 포인트다. 예를 들어 서버가 [[211_context_switch|문맥 교환]]이 매우 잦은 워크로드를 처리하면 [[357_tlb|TLB]] 무효화 비용과 [[353_page_table|페이지 테이블]] 워킹 비용이 누적되어 [[015_지연_데이터_관점|지연]]시간이 증가할 수 있다. 이 경우 [[092_thread_lwp|스레드]] 모델, 큰 [[286_page_frame|페이지]]([[517_huge_page|Huge Page]]), 프로세스 격리 수준을 함께 검토해야 한다.

반대로 보안이 중요한 환경에서는 주소 공간 분리가 [[282_performance_tactics|성능]]보다 우선이다. 사용자 영역과 [[022_kernel_role|커널]] 영역을 강하게 분리하고, 실행 [[501_file_definition_logical_record|파일]] 배치를 무작위화하며, 접근 권한 [[073_bit|비트]]를 엄격히 적용해야 한다. 메모리 공유가 필요할 때도 "같은 물리 프레임을 서로 다른 [[322_logical_virtual_address|논리 주소]]에 연결한다"는 원리를 이해해야 안전한 [[118_shared_memory|공유 메모리]] 설계가 가능하다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. [[352_page_size|페이지 크기]] 선택이 [[357_tlb|TLB]] 적중률과 [[341_internal_fragmentation|내부 단편화]] 사이에서 균형을 이루는가?
2. [[211_context_switch|문맥 교환]]이 잦은 시스템에서 주소 공간 전환 비용을 측정했는가?
3. [[118_shared_memory|공유 메모리]] 구간의 읽기/[[289_cqrs_db|쓰기]] 권한을 최소 권한 원칙으로 제한했는가?
4. [[720_page_fault_isr|페이지 폴트]]가 정상적인 [[015_지연_데이터_관점|지연]]인지, 메모리 압박으로 인한 [[257_thrashing|스래싱]]([[257_thrashing|Thrashing]]) 징후인지 구분하고 있는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 애플리케이션이 [[323_physical_address|물리 주소]]를 직접 알아야 [[282_performance_tactics|성능]]이 난다고 오해하는 설계
- 주소 공간 격리를 무시한 채 디버깅 편의성만 보고 권한 검사를 느슨하게 하는 [[009_config|설정]]
- [[720_page_fault_isr|페이지 폴트]] 원인을 분석하지 않고 단순히 메모리를 증설하는 대응

기술사 관점에서는 "주소 번역은 추상화이면서 동시에 [[282_performance_tactics|성능]] 비용이 있는 계층"이라는 점을 짚어야 한다. 격리만 강조하면 시스템 [[282_performance_tactics|성능]] 설명이 약해지고, [[282_performance_tactics|성능]]만 강조하면 왜 이 구조가 보안과 안정성에 필수인지 놓치게 된다. 좋은 답안은 [[571_protection_vs_security|보호]]·재배치·캐시 효율·운영 오버헤드를 함께 묶어 설명한다.

**📢 섹션 요약 비유**: 놀이공원 입장권에는 구역 이름만 적혀 있지만, 운영팀은 사람 흐름과 안전 펜스를 보고 실제 동선을 조정한다. 표를 쉽게 만들면서도 사고를 막으려면 뒤쪽 통제 체계가 정교해야 한다.

---

## Ⅴ. 기대효과 및 결론

[[322_logical_virtual_address|논리 주소]]와 [[323_physical_address|물리 주소]]의 분리는 세 가지 효과를 만든다. 첫째, 프로세스마다 독립된 주소 공간을 제공해 충돌과 침범을 막는다. 둘째, 운영체제가 프로그램을 RAM 어디에 올릴지 유연하게 결정할 수 있어 메모리 활용률이 높아진다. 셋째, [[286_page_frame|페이지]] 교체와 [[381_virtual_memory|가상 메모리]] 확장을 통해 실제 RAM보다 큰 작업 집합도 다룰 수 있게 된다.

물론 전제조건도 있다. 주소 변환 계층은 반드시 빠르게 동작해야 하고, [[353_page_table|페이지 테이블]] 구조와 [[357_tlb|TLB]] 설계가 이를 뒷받침해야 한다. 또한 추상화가 강할수록 [[720_page_fault_isr|페이지 폴트]], [[357_tlb|TLB]] 미스, [[257_thrashing|스래싱]] 같은 간접 비용이 숨어들 수 있으므로, "추상화는 공짜가 아니다"라는 관점도 함께 기억해야 한다.

결국 이 개념은 주소를 두 벌로 나눈 것이 아니라, 시스템 설계의 책임을 분리한 것이다. 프로그램에는 단순한 작업 공간을 주고, 운영체제와 하드웨어에는 [[571_protection_vs_security|보호]]와 배치의 책임을 맡기는 구조라고 기억하면 된다. 그래서 [[323_physical_address|물리 주소]]와 [[322_logical_virtual_address|논리 주소]]의 관계는 단순 변환 공식이 아니라, 현대 운영체제가 성립하기 위한 계약 그 자체다.

**📢 섹션 요약 비유**: 무대 위 배우는 대본에 적힌 "왼쪽 문"만 보고 움직이지만, 무대 감독은 그 문 뒤 통로와 장치 위치까지 모두 안다. 공연이 매끄러운 이유는 배우와 감독이 서로 다른 지도를 [[289_cqrs_db|쓰기]] 때문이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [[328_mmu|MMU]] ([[284_mmu|Memory Management Unit]]) | [[322_logical_virtual_address|논리 주소]]를 [[323_physical_address|물리 주소]]로 바꾸는 핵심 번역기이며, [[571_protection_vs_security|보호]] [[073_bit|비트]] 검사도 함께 수행한다. |
| [[353_page_table|페이지 테이블]] ([[353_page_table|Page Table]]) | 어떤 [[369_logic_bomb|논리]] [[286_page_frame|페이지]]가 어떤 물리 프레임에 놓였는지 기록하는 매핑 구조다. |
| [[357_tlb|TLB]] ([[291_tlb|Translation Lookaside Buffer]]) | 최근 주소 변환 결과를 저장해 번역 [[015_지연_데이터_관점|지연]]을 줄이는 [[148_5g_embb_urllc_mmtc|초고속]] 캐시다. |
| [[720_page_fault_isr|페이지 폴트]] ([[387_page_fault|Page Fault]]) | [[322_logical_virtual_address|논리 주소]]는 유효하지만 현재 RAM에 해당 [[286_page_frame|페이지]]가 없을 때 운영체제를 호출하는 예외다. |
| [[381_virtual_memory|가상 메모리]] ([[381_virtual_memory|Virtual Memory]]) | [[322_logical_virtual_address|논리 주소]] 공간을 물리 메모리보다 크게 운영하게 해 주는 상위 개념이다. |
| [[374_aslr|ASLR]] (Address Space Layout Randomization) | [[322_logical_virtual_address|논리 주소]] 배치를 무작위화해 공격자가 주소를 예측하기 어렵게 만드는 보안 기법이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
고정 물리 배치 중심 메모리 사용
            │
            ▼
논리 주소 (Logical Address) / 물리 주소 (Physical Address) 분리
            │
            ▼
MMU (Memory Management Unit) + 페이지 테이블 (Page Table)
            │
            ▼
TLB (Translation Lookaside Buffer) 기반 고속 주소 변환
            │
            ▼
가상 메모리 (Virtual Memory) · 페이지 폴트 (Page Fault) 처리
            │
            ▼
ASLR (Address Space Layout Randomization) · 가상화 · 격리 강화
```

이 흐름은 단순 주소 변환에서 시작해 [[282_performance_tactics|성능]] 최적화, [[381_virtual_memory|가상 메모리]], 보안 강화로 확장되는 발전 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[322_logical_virtual_address|논리 주소]]는 내가 "내 장난감은 1번 서랍에 있어"라고 말하는 쉬운 이름표예요.
2. [[323_physical_address|물리 주소]]는 엄마가 아는 진짜 위치, 예를 들면 "거실 책장 두 번째 칸 뒤쪽" 같은 정확한 자리예요.
3. 그래서 나는 쉬운 이름만 기억하고, 엄마는 진짜 위치를 찾아 주니까 집이 어지러워도 장난감을 잘 찾을 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 283 / 803

← **이전**: [[282_virtual_memory|282. 가상 메모리 (Virtual Memory)]]
**다음**: [[284_mmu|284. MMU (Memory Management Unit)]] →

---
