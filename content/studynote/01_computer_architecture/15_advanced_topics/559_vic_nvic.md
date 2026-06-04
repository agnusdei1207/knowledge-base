---
title: "559. 벡터형 인터럽트 컨트롤러 (VIC: Vectored Interrupt Controller, NVIC: Nested Vectored Interrupt Controller)"
date: "2026-05-08"
tags:
  - "studynote-computer-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 벡터형 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 컨트롤러는 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)가 발생했을 때 CPU가 원인을 다시 소프트웨어로 탐색하지 않도록, 우선순위가 가장 높은 요청을 고르고 곧바로 해당 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 루틴 주소로 연결해 주는 하드웨어 디스패처다.
> 2. **가치**: VIC보다 NVIC가 강력한 이유는 단순 벡터화가 아니라, 우선순위 선점·자동 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) 저장·Tail Chaining까지 코어 내부에 통합해 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간과 지터를 함께 줄였다는 데 있다.
> 3. **판단 포인트**: [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 성능은 컨트롤러 종류보다도 우선순위 설계와 [ISR](/studynote/02_operating_system/01_overview_architecture/020_isr/) ([Interrupt Service Routine](/studynote/01_computer_architecture/08_io_storage_systems/317_isr/)) 길이에 크게 좌우되므로, 하드웨어 기능을 살리려면 "짧은 핸들러 + 정확한 선점 규칙"이 전제돼야 한다.

---

## Ⅰ. 개요 및 필요성

벡터형 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 컨트롤러는 여러 주변장치에서 동시에 들어오는 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 요청을 정리해 CPU에 전달하고, 동시에 "어느 주소로 들어가야 하는지"까지 알려 주는 하드웨어다. 즉 단순히 벨을 울리는 장치가 아니라, <strong>누가 먼저 처리돼야 하고 어디로 점프해야 하는지 결정하는 배차 시스템</strong>이다. 이 구조가 없으면 CPU는 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)가 들어올 때마다 상태 레지스터를 읽어 원인을 하나씩 확인해야 하므로 응답 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 커진다.

[초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [마이크로컨트롤러](/studynote/01_computer_architecture/03_architecture_basics_performance/130_microcontroller/)와 프로세서에서는 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 개수가 적어 소프트웨어 디스패치 비용이 크지 않았지만, 주변장치가 늘고 실시간 요구가 높아지면서 상황이 달라졌다. 모터 제어, 통신, 센서 샘플링처럼 마이크로초 단위 응답이 중요한 시스템에서는 "누가 불렀는지 찾는 시간" 자체가 손실이 된다. 그래서 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 아키텍처는 공유 IRQ ([Interrupt](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) Request)에서 vectored IRQ로, 다시 nested vectored 구조로 발전했다.

VIC와 NVIC의 차이도 바로 여기서 나온다. VIC는 벡터화 자체에 초점을 둔 반면, NVIC는 Cortex-M 코어 안으로 들어와 선점과 문맥 저장까지 하드웨어화했다. 따라서 NVIC는 더 적은 소프트웨어 개입으로 더 예측 가능한 응답시간을 만든다.

- **📢 섹션 요약 비유**: VIC가 민원 창구 직원이 번호표를 뽑아 주는 역할이라면, NVIC는 응급실 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 간호사와 수술실 문까지 한 번에 연결해 주는 체계다. 누가 급한지뿐 아니라 바로 어디로 들어가야 하는지도 같이 처리한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

벡터형 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 컨트롤러의 기본 동작은 `요청 수집 -> pending 기록 -> 우선순위 결정 -> 벡터 주소 제공 -> 핸들러 진입`이다. 여기서 NVIC는 한 걸음 더 나아가 예외 진입 시 주요 레지스터를 자동 저장하고, 우선순위가 더 높은 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)가 들어오면 현재 ISR을 선점하며, 연속 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 사이에서는 불필요한 복귀·재진입을 줄이는 Tail Chaining을 제공한다. 이 차이가 체감 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간을 크게 줄인다.

| 항목 | VIC | NVIC |
| :-- | :-- | :-- |
| 위치 | 주로 외부/주변 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 블록 | Cortex-M 코어 내부 |
| 벡터화 | 지원 | 지원 |
| 중첩 선점 | 제한적 또는 소프트웨어 의존 | 하드웨어 기반 선점 지원 |
| 문맥 저장 | 소프트웨어 부담 큼 | 자동 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) 저장 지원 |
| 실시간성 | 구현 의존 | 더 낮은 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 지터 |

이 그림은 NVIC가 왜 단순 컨트롤러가 아니라 "코어의 일부"처럼 동작하는지를 보여 준다.

```text
+------------------------------------------------------------------------------+
| NVIC 흐름: 인터럽트 선택과 문맥 저장을 하드웨어에 묶어 진입 지연을 줄인다   |
+------------------------------------------------------------------------------+
| Peripherals --> Pending Bits --> Priority Encoder --> Vector Fetch             |
|                                                         |                   |
|                                                         v                   |
|                                              Auto Stack Save                |
|                                                         |                   |
|                            higher priority arrival -----+-----> Preempt       |
|                                                         |                   |
|                                    next pending exists -+-----> Tail Chain   |
+------------------------------------------------------------------------------+
```

대표적으로 Cortex-M 계열에서는 예외 진입이 약 12 cycle 수준, Tail Chaining은 약 6 cycle 수준으로 알려져 있다. 물론 실제 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 플래시 wait [state](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/), [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 혼잡, [ISR](/studynote/02_operating_system/01_overview_architecture/020_isr/) 코드 길이에 따라 달라지지만, 핵심은 "문맥 저장과 다음 벡터 결정"을 하드웨어가 대신함으로써 소프트웨어 가변 비용을 크게 줄였다는 데 있다.

NVIC를 제대로 쓰려면 우선순위를 단순 숫자 크기가 아니라 선점 정책으로 이해해야 한다. 높은 우선순위 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)가 너무 많으면 오히려 낮은 우선순위 작업이 기아 상태에 빠질 수 있으므로, 제어 루프·통신·백그라운드 유지보수 작업을 계층적으로 나눠야 한다.

- **📢 섹션 요약 비유**: NVIC는 엘리베이터 제어기와 같다. 어느 층 호출이 더 급한지 정할 뿐 아니라, 문이 열리고 닫히는 절차까지 자동화해서 승객을 더 빠르고 일정하게 실어 나른다.

---

## Ⅲ. 비교 및 연결

벡터형 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 컨트롤러를 비교할 때는 "주소를 알려 주는가"보다 "얼마나 적은 소프트웨어 개입으로 예측 가능한 응답을 보장하는가"를 봐야 한다. 같은 벡터화라도 중첩과 자동 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) 저장이 없으면 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)은 [ISR](/studynote/02_operating_system/01_overview_architecture/020_isr/) 코드 품질에 크게 흔들린다. 그래서 VIC와 NVIC의 차이는 기능 수보다 시스템 경계에 더 가깝다.

| 방식 | 장점 | 약점 | 연결 개념 |
| :-- | :-- | :-- | :-- |
| [Polling](/studynote/02_operating_system/11_exam_summary/747_io_polling_overhead/) | 구조 단순 | CPU 낭비, [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 큼 | 저속 단순 장치 |
| 일반 VIC | 벡터화로 원인 탐색 비용 감소 | 중첩·문맥 관리가 소프트웨어 의존 | [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) ARM, 단순 [System on Chip](/studynote/01_computer_architecture/03_architecture_basics_performance/131_soc/) ([SoC](/studynote/01_computer_architecture/03_architecture_basics_performance/131_soc/)) |
| NVIC | 낮은 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 하드웨어 선점, Tail [Chaining](/studynote/12_it_management/03_ea_isp/887_chaining/) | 단일 코어 [마이크로컨트롤러](/studynote/01_computer_architecture/03_architecture_basics_performance/130_microcontroller/) ([Microcontroller](/studynote/01_computer_architecture/03_architecture_basics_performance/130_microcontroller/) Unit, MCU) 중심 | Cortex-M, 실시간 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) (Real-Time [Operating System](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/), RTOS) |
| GIC (Generic [Interrupt](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) Controller) / APIC (Advanced Programmable [Interrupt](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) Controller) | 멀티코어 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)·[가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 지원 | 구조 복잡, 비용 증가 | 서버/고성능 [System on Chip](/studynote/01_computer_architecture/03_architecture_basics_performance/131_soc/) ([SoC](/studynote/01_computer_architecture/03_architecture_basics_performance/131_soc/)) |

이 구조는 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)와도 직접 연결된다. RTOS (Real-Time [Operating System](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/))는 SysTick으로 주기 틱을 만들고, PendSV처럼 가장 낮은 우선순위 예외를 이용해 문맥 전환을 미룬다. 즉 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 컨트롤러 설계는 단순 주변장치 문제가 아니라, 스케줄러와 전력 관리 정책을 포함한 시스템 설계 문제다.

또한 NVIC의 장점은 [DMA](/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) ([Direct Memory Access](/studynote/01_computer_architecture/08_io_storage_systems/318_dma/))와 함께 쓸 때 극대화된다. 빠른 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 컨트롤러가 있어도 ISR에서 큰 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 복사하면 의미가 줄어든다. 따라서 실무에서는 "짧은 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) + [DMA](/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) 후속 처리 + [태스크](/studynote/02_operating_system/02_process_thread/150_task/)로 위임"이 정석이 된다.

- **📢 섹션 요약 비유**: Polling이 학생이 복도를 돌며 누가 부르는지 계속 확인하는 방식이라면, NVIC는 반장이 급한 순서대로 선생님 책상 위에 바로 호출장을 올려두는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 컨트롤러를 잘 쓰는 핵심은 우선순위 설계와 [ISR](/studynote/02_operating_system/01_overview_architecture/020_isr/) 예산 통제다. 예를 들어 20kHz 모터 제어 루프와 UART (Universal Asynchronous Receiver-Transmitter) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 출력이 같은 선점 등급에 있으면, 짧은 제어 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)가 긴 문자열 출력 때문에 흔들릴 수 있다. 따라서 주기 제어, 안전 감시, 통신, 백그라운드 처리를 다른 계층으로 분리해야 한다.

또한 NVIC의 자동 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) 저장은 편리하지만 무료가 아니다. [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)가 너무 자주 오면 push/pop과 플래시 fetch 자체가 부담이 되므로, 고빈도 샘플링은 DMA로 배치 처리하고 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 수를 줄이는 편이 낫다. 좋은 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 설계는 "많이 반응하는 것"이 아니라 "정말 필요한 순간에만 짧게 반응하는 것"이다.

### 적용 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 가장 긴급한 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)와 덜 긴급한 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)가 선점 그룹으로 분리되어 있는가?
2. [ISR](/studynote/02_operating_system/01_overview_architecture/020_isr/) 내부에서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 복사, 포맷팅, 대기 루프를 돌리지 않고 최소 처리만 하는가?
3. RTOS를 쓴다면 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호출 가능 우선순위와 금지 우선순위를 구분했는가?
4. 벡터 테이블 relocation이나 [bootloader](/studynote/02_operating_system/01_overview_architecture/029_bootloader/) 연동 시 메모리 장벽과 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)을 점검했는가?
5. [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 폭주 상황에서 [DMA](/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/), [batching](/studynote/05_database/06_dw_olap_trends/389_bulk_insert_batching_optimization/), debounce 같은 빈도 제어 수단이 있는가?

### 피해야 할 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 모든 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 우선순위를 최고 등급으로 두는 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)
- [ISR](/studynote/02_operating_system/01_overview_architecture/020_isr/) 안에서 printf, 동적 메모리 할당, 긴 [polling](/studynote/02_operating_system/11_exam_summary/747_io_polling_overhead/) 루프를 수행하는 코드
- 하드웨어는 NVIC인데 소프트웨어는 여전히 [polling](/studynote/02_operating_system/11_exam_summary/747_io_polling_overhead/) 구조처럼 작성해 장점을 버리는 설계
- 벡터 테이블을 바꾸고도 캐시/메모리 가시성을 고려하지 않는 부트 코드

기술사 답안에서는 VIC와 NVIC를 단순 세대 차이로 설명하기보다, **벡터화 -> 중첩 선점 -> 자동 문맥 저장 -> RTOS 연동** 흐름으로 써야 한다. 그래야 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 컨트롤러가 왜 실시간성의 핵심인지 살아난다.

- **📢 섹션 요약 비유**: 좋은 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 우선순위 설계는 도로 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 체계와 같다. 구급차, [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/), 일반차를 같은 차선에 아무렇게나 섞어 두면 도로가 막히듯, [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)도 급한 일과 덜 급한 일을 분리해야 흐름이 살아난다.

---

## Ⅴ. 기대효과 및 결론

벡터형 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 컨트롤러의 가장 큰 효과는 CPU가 사건을 더 빨리 아는 것이 아니라, **더 예측 가능하게** 아는 데 있다. 응답시간이 일정해지면 제어 루프 안정성이 올라가고, 저전력 모드에서 깨어나는 시점도 더 정밀하게 다룰 수 있다. 결과적으로 성능뿐 아니라 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 용이성과 신뢰성이 함께 좋아진다.

한계도 분명하다. [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 구조가 강력할수록 잘못된 우선순위 설계의 피해도 커지고, 지나친 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 중심 구조는 오히려 소프트웨어를 파편화한다. 따라서 이벤트 빈도가 매우 높은 경로는 [DMA](/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/), [폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/) 배치, [태스크](/studynote/02_operating_system/02_process_thread/150_task/) 큐와 조합하는 균형 감각이 필요하다.

미래 방향은 보안 분리와 [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)다. TrustZone 기반 보안 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 분리, 가상 머신용 가상 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 주입, 멀티코어 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 컨트롤러와의 결합이 더 중요해질 것이다. 결국 VIC/NVIC는 "[인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)가 있다"는 사실보다, <strong>누가 언제 어디로 들어갈지를 하드웨어가 얼마나 똑똑하게 정해 주는가</strong>로 기억해야 한다.

- **📢 섹션 요약 비유**: 벡터형 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 컨트롤러는 학교의 비상 방송 체계와 같다. 단순히 종을 울리는 것이 아니라, 어느 반이 먼저 대피하고 어디로 가야 하는지까지 정확히 안내해 혼란을 줄인다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| Vector Table | [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 번호를 실제 핸들러 주소와 연결하는 핵심 표다. |
| Priority / Preemption | 누가 현재 ISR을 끊고 들어올 수 있는지 결정한다. |
| Tail [Chaining](/studynote/12_it_management/03_ea_isp/887_chaining/) | 연속 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 사이의 불필요한 복귀 비용을 줄인다. |
| SysTick / PendSV | RTOS 스케줄링과 문맥 전환에 자주 쓰이는 예외 조합이다. |
| [DMA](/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) | [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 빈도와 [ISR](/studynote/02_operating_system/01_overview_architecture/020_isr/) 부담을 줄여 NVIC의 장점을 살린다. |
| WFI (Wait For [Interrupt](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)) | 예측 가능한 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 구조가 저전력 설계와 만나는 지점이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
Polling 기반 장치 감시
        |
        v
Vectored Interrupt Controller
        |
        v
Nested Vectored Interrupt Controller
        |
        v
RTOS 연동 예외 분리(SysTick / PendSV)
        |
        v
멀티코어 GIC · APIC · 가상 인터럽트 주입
```

이 흐름은 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 처리가 "누가 불렀는지 찾는 단계"에서 "선점·문맥 저장·시스템 정책을 함께 하드웨어화하는 단계"로 발전했음을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터 안에는 여러 장치가 "나부터 봐 줘!" 하고 동시에 손을 들어요.
2. VIC와 NVIC는 그중에서 가장 급한 친구를 먼저 고르고, 선생님이 바로 그 친구 자리로 가게 도와줘요.
3. 특히 NVIC는 가방 챙기기까지 빨리 해 줘서, 중요한 일을 더 빨리 시작할 수 있게 해 줘요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 559 / 803

<- **이전**: [558. NMI (Non-Maskable Interrupt)](/studynote/01_computer_architecture/15_advanced_topics/558_nmi/)
**다음**: [560. 멀티코어 인터럽트 라우팅 (GIC: Generic Interrupt Controller, APIC: Advanced Programmable](/studynote/01_computer_architecture/15_advanced_topics/560_multicore_interrupt_routing/) ->

---
