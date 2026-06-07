---
title: "Write Through"
date: "2026-04-20"
tags:
  - "studynote-computer-architecture"
weight: 276
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Write-Through (동시 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/))는 CPU (Central Processing Unit)가 캐시에 값을 쓸 때, 같은 값을 하위 메모리까지 즉시 반영해 캐시와 메모리의 차이를 최소화하는 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이다.
> 2. **가치**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 최신 위치가 명확하므로 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 관리와 장애 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 판단이 단순해지며, 특히 장치 제어나 공유 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)처럼 "지금 반영되었는가"가 중요한 구간에 강하다.
> 3. **판단 포인트**: 매번 메모리 트래픽이 발생하므로 범용 고성능 캐시의 기본 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)으로는 불리하지만, [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 버퍼 (Write Buffer)와 결합하면 단순성과 신뢰성이 필요한 영역에서 여전히 유효하다.

---

## Ⅰ. 개요 및 필요성

Write-Through (동시 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/))는 캐시에 기록한 값을 즉시 하위 계층에도 함께 기록하는 캐시 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이다. CPU가 L1 (Level 1) 캐시에 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 갱신하면, 그 순간 메인 메모리 [DRAM](/studynote/01_computer_architecture/06_memory_hierarchy_cache/251_dram/) (Dynamic Random Access Memory)이나 다음 캐시 계층에도 같은 내용이 전달된다. 즉, 캐시는 빠른 작업 공간이지만 "최신본을 혼자 숨겨 두는 장소"가 아니라는 점이 핵심이다.

이 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 필요한 이유는 최신 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 위치를 단순하게 만들기 위해서다. [Write-Back](/studynote/01_computer_architecture/06_memory_hierarchy_cache/277_write_back/) ([나중 쓰기](/studynote/01_computer_architecture/06_memory_hierarchy_cache/277_write_back/))에서는 캐시 라인이 메모리보다 더 최신일 수 있으므로, 시스템은 [더티 비트](/studynote/01_computer_architecture/06_memory_hierarchy_cache/278_dirty_bit/) ([Dirty Bit](/studynote/02_operating_system/07_virtual_memory/396_dirty_bit/)), 퇴출 시점, 강제 플러시를 함께 관리해야 한다. 반면 Write-Through는 쓰는 순간 메모리도 함께 갱신되므로, 다른 코어·입출력 장치·운영체제가 "최신본이 어디 있는가"를 추적하는 부담이 크게 줄어든다.

특히 MMIO (Memory-Mapped I/O)처럼 하드웨어 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)에 즉시 명령을 전달해야 하는 공간에서는 이 철학이 중요하다. CPU가 장치 제어 값을 캐시에만 남겨 두면 실제 장치는 아무 일도 하지 않는다. 따라서 Write-Through는 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화용 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이라기보다, <strong>즉시성·가시성·<a href="/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a></strong>을 우선하는 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 이해해야 한다.

```text
+----------------------------------------------------------------------+
|        Write-Through가 필요한 이유: 최신본 위치를 숨기지 않음       |
+----------------------------------------------------------------------+
| CPU Store                                                            |
|    |                                                                 |
|    +--> L1 Cache 갱신                                                 |
|    |                                                                 |
|    +--> 하위 계층 즉시 반영 ---> L2 / Memory / Device                  |
|                                                                       |
| 결과: "최신 데이터가 캐시에만 있다"는 애매한 상태를 줄임             |
+----------------------------------------------------------------------+
```

이 그림의 핵심은 Write-Through가 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 높이기보다 <strong>최신 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>의 위치를 투명하게 만드는 <a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a></strong>이라는 점이다. 그래서 설계자는 속도보다 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 단순성, 장애 시 해석 용이성, 장치 제어의 즉시성을 얻는다.

- **📢 섹션 요약 비유**: Write-Through는 메모장에 약속을 적자마자 가족 공용 달력에도 바로 적는 방식과 같다. 조금 번거롭지만, 누가 보더라도 최신 일정이 어디에 있는지 헷갈리지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Write-Through의 동작은 단순하다. CPU가 [캐시 히트](/studynote/01_computer_architecture/06_memory_hierarchy_cache/263_cache_hit_miss/) 상태에서 값을 쓰면, 캐시 컨트롤러는 캐시 라인을 갱신하는 동시에 하위 계층으로 같은 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 요청을 내려보낸다. 이때 캐시는 최신 복사본을 갖고 있지만, 메모리도 거의 동시에 같은 값으로 갱신되므로 [더티 비트](/studynote/01_computer_architecture/06_memory_hierarchy_cache/278_dirty_bit/)가 사실상 필요 없다.

문제는 속도 차이다. L1 캐시 접근은 보통 수 ns 수준이지만, [DRAM](/studynote/01_computer_architecture/06_memory_hierarchy_cache/251_dram/) 반영은 수십~수백 ns가 걸릴 수 있다. 매 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)마다 CPU가 메모리 완료를 기다리면 파이프라인이 자주 멈추므로, 실제 구현에서는 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 버퍼를 두어 CPU는 먼저 버퍼에 쓰고 다음 명령으로 넘어가게 한다.

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| L1 (Level 1) 캐시 | 가장 먼저 갱신되는 빠른 저장소 | 히트 시 즉시 응답 |
| [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 버퍼 (Write Buffer) | 느린 하위 기록을 임시 흡수 | 버퍼 크기와 병합 능력 |
| 하위 캐시/L2 (Level 2) | 중간 계층 반영 지점 | 계층 간 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 유지 |
| [DRAM](/studynote/01_computer_architecture/06_memory_hierarchy_cache/251_dram/) | 최종 메모리 반영 지점 | 지연시간과 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) |

다음 그림은 순수 Write-Through와 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 버퍼를 둔 Write-Through의 차이를 보여준다.

```text
+----------------------------- 순수 Write-Through -----------------------------+
| CPU Store --> L1 갱신 --> DRAM 쓰기 완료 대기 --> 다음 명령                     |
|                       (긴 지연이 그대로 CPU 정지 시간으로 노출)              |
+-------------------------- Write Buffer 포함 구조 ----------------------------+
| CPU Store --> L1 갱신 --> Write Buffer 적재 --> 다음 명령                       |
|                               |                                               |
|                               +---------> DRAM에 순차 반영                     |
+-------------------------------------------------------------------------------+
```

핵심 공식은 단순하다. <strong><a href="/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> 빈도 × 메모리 반영 비용</strong>이 커질수록 Write-Through의 불리함이 커진다. 그래서 버퍼 병합, [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 폭 확대, 스트리밍 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 최적화가 함께 붙는다. 하지만 아무리 보완해도 "메모리에 자주 써야 한다"는 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)의 본질 자체는 바뀌지 않는다.

- **📢 섹션 요약 비유**: Write-Through는 주문을 받자마자 본사 시스템에도 바로 입력하는 매장과 같다. 손님 응대는 느려질 수 있어서 접수함([쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 버퍼)을 두지만, 결국 본사 기록을 즉시 맞춘다는 원칙은 그대로다.

---

## Ⅲ. 비교 및 연결

Write-Through를 제대로 이해하려면 Write-Back과 비교해야 한다. 두 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)의 차이는 "언제 메모리를 최신 상태로 만들 것인가"에 있다. Write-Through는 쓰는 순간 메모리를 갱신하고, Write-Back은 캐시에서 쫓겨날 때까지 갱신을 미룬다.

| 비교 항목 | Write-Through | [Write-Back](/studynote/01_computer_architecture/06_memory_hierarchy_cache/277_write_back/) |
| :--- | :--- | :--- |
| 메모리 갱신 시점 | 매 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)마다 즉시 | 퇴출(Eviction) 시점 |
| 메모리 트래픽 | 큼 | 상대적으로 작음 |
| 하드웨어 복잡도 | 낮음 | [더티 비트](/studynote/01_computer_architecture/06_memory_hierarchy_cache/278_dirty_bit/), 플러시 관리 필요 |
| [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 해석 | 직관적 | 최신본 위치 추적 필요 |
| 적합한 영역 | MMIO, 공유 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 단순 제어 | 범용 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 캐시, 고성능 연산 |

[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 미스 (Write Miss) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)과의 연결도 중요하다. Write-Through는 보통 No-Write-Allocate와 자주 짝을 이룬다. 캐시에 없는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 쓰려고 할 때 굳이 블록 전체를 캐시에 가져오지 않고, 하위 메모리에 바로 써 버리는 편이 캐시 오염을 줄이기 쉽기 때문이다.

또한 멀티코어 환경에서는 [캐시 일관성](/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) 프로토콜과의 관계도 달라진다. Write-Through는 메모리 기준 최신성이 상대적으로 분명해서 스누핑 (Snooping) 기반 무효화 논리가 단순해질 수 있다. 다만 이것이 코히런시 문제를 완전히 없애는 것은 아니며, 여전히 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 트래픽 증가와 공유 라인 경쟁은 발생한다.

- **📢 섹션 요약 비유**: Write-Through는 수정할 때마다 단체방 공지까지 바로 올리는 방식이고, Write-Back은 개인 메모장에서 다 고친 뒤 나중에 공지하는 방식이다. 전자는 모두가 빨리 알지만 시끄럽고, 후자는 조용하지만 중간 상태를 추적해야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 "모든 캐시에 Write-Through를 쓰자"가 아니라, <strong>어떤 주소 공간과 워크로드에만 이 <a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a>을 적용할 것인가</strong>를 판단해야 한다. 일반적인 CPU [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 캐시는 같은 변수에 반복 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)가 많아 Write-Back이 더 유리하다. 반면 장치 제어 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/), 공유 [플래그](/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/), 재읽기 가능성이 낮은 스트리밍 출력 버퍼는 Write-Through 또는 캐시 우회가 더 안전하다.

대표 사례는 MMIO다. 네트워크 카드, [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) ([Graphics Processing Unit](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)), 저장장치 컨트롤러의 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 공간은 CPU가 값을 쓴 즉시 장치가 이를 보아야 한다. 이 공간을 Write-Back으로 잘못 매핑하면 명령이 캐시에 남아 실제 하드웨어가 늦게 반응하거나 아예 반응하지 않는 장애가 발생할 수 있다.

또 다른 판단 포인트는 버퍼 포화다. [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 버퍼가 작은 시스템에서 연속 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 폭주가 발생하면, 결국 버퍼가 가득 차 CPU가 다시 정지한다. 따라서 설계자는 버퍼 깊이, 병합 가능성, [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/), 워크로드의 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 패턴을 함께 봐야 한다.

### 기술사 답안형 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 해당 영역은 <strong>즉시 반영</strong>이 중요한가, 아니면 <strong>반복 <a href="/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> <a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a></strong>이 중요한가?
2. [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 버퍼가 없거나 작다면, Write-Through로 인한 스톨을 감당할 수 있는가?
3. 장치 제어·공유 메타데이터처럼 최신 위치의 명확성이 중요한가?
4. Write Miss 시 No-Write-Allocate를 함께 써서 캐시 오염을 줄일 것인가?

### 회피해야 할 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 범용 연산 버퍼 전체를 무작정 Write-Through로 바꾸는 설계
- [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 버퍼 포화 가능성을 무시한 채 순차 대량 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 남발하는 코드
- MMIO 영역을 일반 DRAM처럼 취급해 캐시 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 혼동하는 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)

- **📢 섹션 요약 비유**: Write-Through는 소방서 출동 기록처럼 즉시 본부에 남겨야 할 업무에 맞다. 반대로 초안 문서를 쓰는 모든 순간까지 본부 승인 절차를 붙이면, 일은 안전해도 전체 조직이 느려진다.

---

## Ⅴ. 기대효과 및 결론

Write-Through의 가장 큰 효과는 <strong>단순한 <a href="/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a> 모델</strong>이다. 메모리가 빠르게 최신 상태에 가까워지므로, 장애 분석·장치 연동·다중 주체 간 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 가시성 판단이 쉬워진다. 캐시 퇴출 시 추가 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 책임이 적어 제어 로직도 비교적 단순하다.

반면 한계도 분명하다. 반복 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 워크로드에서는 메모리 트래픽이 급증하고, [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 병목과 전력 소모가 커질 수 있다. 그래서 현대 범용 프로세서의 주력 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 캐시는 Write-Back을 채택하고, Write-Through는 특정 계층이나 특정 주소 공간에서 선택적으로 사용된다.

미래 관점에서도 이 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)은 사라지지 않는다. 비휘발성 메모리, 장치 직결 인터페이스, 안전성 우선 시스템에서는 "최신 값을 숨기지 않는다"는 철학이 계속 중요하다. 따라서 Write-Through는 느린 옛 방식이 아니라, <strong>속도보다 즉시성과 해석 가능성을 택하는 설계 선택지</strong>로 기억하는 것이 맞다.

- **📢 섹션 요약 비유**: Write-Through는 매출이 발생할 때마다 장부를 바로 닫아 맞춰 두는 회계 방식과 같다. 속도는 덜 나와도, 지금 숫자가 맞는지 확인해야 하는 조직에서는 그 정직함이 가장 큰 힘이 된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [Write-Back](/studynote/01_computer_architecture/06_memory_hierarchy_cache/277_write_back/) ([나중 쓰기](/studynote/01_computer_architecture/06_memory_hierarchy_cache/277_write_back/)) | 메모리 반영을 지연해 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 얻는 대조 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) |
| [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 버퍼 (Write Buffer) | Write-Through의 메모리 지연을 흡수하는 핵심 보완 장치 |
| Write Miss / No-Write-Allocate | 캐시에 없는 주소에 쓸 때의 대표적 조합 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) |
| MMIO (Memory-Mapped I/O) | 즉시 반영이 중요한 대표 적용 영역 |
| [캐시 일관성](/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) ([Cache Coherence](/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/)) | 다중 코어에서 최신 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 가시성을 해석하는 상위 문제 |

### 📈 관련 키워드 및 발전 흐름도

```text
단순 캐시 쓰기 정책
    |
    v
Write-Through (동시 쓰기)
    |
    +--> 쓰기 버퍼 (Write Buffer)
    |        |
    |        +--> 버퍼 병합 · 버스 지연 은닉
    |
    +--> No-Write-Allocate
    |
    +--> MMIO · 장치 제어 · 일관성 단순화
             |
             v
      선택적 주소 공간 정책 설계
```

이 흐름도는 Write-Through가 단독 기법이 아니라, [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 버퍼·미스 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)·장치 메모리 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)과 결합되며 실무적으로 세분화된다는 점을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. Write-Through는 공책에 답을 쓰자마자 칠판에도 바로 똑같이 적는 거예요.
2. 그래서 느리긴 해도, 친구들이 칠판을 보면 항상 가장 최신 답을 볼 수 있어요.
3. 컴퓨터도 바로 알려야 하는 중요한 내용은 이렇게 "쓴 즉시 같이 적는 방식"을 써요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 276 / 803

<- **이전**: [275. 캐시 쓰기 정책 (Write Policy)](/studynote/01_computer_architecture/06_memory_hierarchy_cache/275_write_policy/)
**다음**: [277. Write-Back (나중 쓰기)](/studynote/01_computer_architecture/06_memory_hierarchy_cache/277_write_back/) ->

---
