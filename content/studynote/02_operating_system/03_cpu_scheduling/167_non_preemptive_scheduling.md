+++
title = "167. 비선점형 스케줄링 (Non-preemptive Scheduling)"
date = 2026-03-22

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)형 스케줄링 (Non-preemptive Scheduling)은 실행 중인 프로세스가 입출력 (Input/Output, I/O) 대기나 종료로 스스로 CPU를 내놓을 때까지 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 강제로 빼앗지 않는 스케줄링 방식이다.
> 2. **가치**: 강제 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) ([Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/))이 줄어들어 구현과 실행 흐름이 단순해지고, 캐시 교란과 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) 오버헤드가 작아 [배치 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/)와 협력적 런타임에 유리하다.
> 3. **판단 포인트**: 오버헤드 절감만 보고 채택하면 응답성 저하, [호위 효과](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/174_convoy_effect/) ([Convoy Effect](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/174_convoy_effect/)), 기아 현상 ([Starvation](/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/)), 악성 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) 독점 문제가 즉시 드러나므로 적용 범위를 엄격히 제한해야 한다.

---

## Ⅰ. 개요 및 필요성

[비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)형 스케줄링은 한 번 CPU를 얻은 작업이 스스로 양보할 때까지 계속 실행되는 방식이다. 여기서 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)가 개입하는 시점은 주로 작업 종료, 블로킹 I/O 요청, 명시적 양보 호출처럼 "현재 실행 중인 작업이 멈추는 순간"이다. 즉 실행 흐름의 주도권이 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 강제 타이머보다 작업의 자발적 상태 변화에 더 많이 놓여 있다.

이 방식이 등장한 배경은 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 시스템에서 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 자체가 비싼 작업이었기 때문이다. [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 저장·복원, 메모리 맵 전환, 캐시 손실을 자주 일으키면 계산 자원이 적은 시스템에서는 오히려 본업보다 교체 비용이 더 커졌다. 특히 [일괄 처리 시스템](/knowledge-base/studynote/02_operating_system/11_exam_summary/672_batch_processing_system_metrics/) (Batch System)은 응답시간보다 전체 작업 완료가 중요했기 때문에, 한 작업을 길게 몰아주는 것이 합리적인 경우가 많았다.

이 그림은 [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)형 스케줄링에서 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)가 언제 움직이는지 보여준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">비선점형 스케줄러의 개입 시점: Running에서만 끝난다</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Ready Queue ──▶ Running ──▶ Waiting (I/O 요청) ──▶ Ready</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">▶ Terminated (작업 종료)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">스케줄러 호출: Waiting 진입 / Terminated 진입 / 명시적 yield</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">스케줄러 미호출: 타이머 만료에 의한 강제 Running→Ready 전환</div></div>
</div>
</div>



핵심은 "[운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 못 빼앗는다"는 사실이 장점이자 위험이라는 점이다. 정상적인 짧은 작업에게는 매끄러운 실행을 주지만, 길고 나쁜 작업에게는 과도한 독점 권한을 준다.

- **📢 섹션 요약 비유**: [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)형 스케줄링은 발표자가 스스로 마이크를 내려놓을 때까지 사회자가 끼어들지 않는 회의 방식과 같다. 깔끔하게 끝내는 사람에게는 효율적이지만, 말을 길게 끄는 사람이 나오면 모두가 기다려야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)형 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)는 "언제 뺏을 것인가"보다 "언제 다시 고를 것인가"에 집중한다. 따라서 핵심 설계 포인트는 강제 타이머보다 [상태 전이](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/632_state_transition_diagram_testing/) 지점, 큐 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/), 평균 대기시간과 기아 사이의 균형이다. 대표 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 [FCFS](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/) (First-Come, First-Served), [SJF](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/175_sjf_scheduling/) ([Shortest Job First](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/175_sjf_scheduling/)), [HRN](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/187_hrn_scheduling/) (Highest Response Ratio Next)처럼 모두 다음에 누구를 선택할지에 초점을 둔다.

| [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 선택 기준 | 강점 | 약점 |
| :------- | :-------- | :--- | :--- |
| [FCFS](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/) | 먼저 도착한 순서 | 구현이 가장 단순 | 긴 작업이 뒤 작업을 오래 묶음 |
| [SJF](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/175_sjf_scheduling/) | 예상 CPU 버스트가 가장 짧은 작업 | 평균 대기시간 최소화 경향 | 실행 시간 예측이 어렵고 긴 작업 기아 가능 |
| [HRN](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/187_hrn_scheduling/) | `(대기시간 + 서비스시간) / 서비스시간` 최대 | 오래 기다린 작업 보정 가능 | 계산 비용과 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 복잡도 증가 |

[비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)형에서는 Running 상태의 작업이 CPU 버스트를 길게 가져갈수록 [Ready Queue](/knowledge-base/studynote/02_operating_system/02_process_thread/088_ready_queue/) 체류 시간이 급격히 늘어난다. 특히 FCFS는 긴 CPU 바운드 (CPU-bound) 작업 앞에 짧은 I/O 바운드 (I/O-bound) 작업이 줄줄이 묶이는 [호위 효과](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/174_convoy_effect/)를 일으키기 쉽다. 반대로 강제 선점이 없으므로 캐시 지역성, 락 설계 단순성, 디버깅 예측 가능성은 좋아진다.

이 그림은 긴 작업 하나가 전체 응답성을 어떻게 망가뜨리는지 보여준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">호위 효과: 앞의 긴 작업 하나가 뒤를 모두 묶는다</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">도착 순서: P1(100ms) → P2(5ms) → P3(3ms)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">CPU 실행:</div><div class="kb-diagram-node">P1 100ms</div><div class="kb-diagram-node">P2 5ms</div><div class="kb-diagram-node">P3 3ms</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">대기시간: P1=0 P2=100ms P3=105ms</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">짧은 작업은 빨리 끝낼 수 있어도, 비선점에서는 끼어들 수 없음</div></div>
</div>
</div>



즉 [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)형 스케줄링의 핵심 원리는 단순하다. "실행 중인 작업을 존중하는 대신, 큐 앞단 선택 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 전체 성능을 최대한 보정한다." 하지만 이 보정은 어디까지나 사후적이며, 실행 중 독점을 중단시키지는 못한다.

- **📢 섹션 요약 비유**: [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)형은 한 차선 도로에서 추월 금지를 건 운영과 같다. 앞차가 규칙적으로 달리면 부드럽지만, 느린 트럭이 한 번 들어오면 뒤 차량 흐름 전체가 함께 느려진다.

---

## Ⅲ. 비교 및 연결

[비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)형 스케줄링은 [선점형 스케줄링](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/166_preemptive_scheduling/)과 비교해야 경계가 분명해진다. 전자는 오버헤드와 단순성에서 이점을 얻고, 후자는 응답성과 공정성에서 이점을 얻는다. 현대 시스템은 대개 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 수준에서는 선점형을 쓰고, 사용자 수준 런타임에서는 협력적 [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/) 방식을 일부 조합하는 하이브리드 구조를 택한다.

| 비교 축 | [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)형 스케줄링 | [선점형 스케줄링](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/166_preemptive_scheduling/) |
| :------ | :---------------- | :-------------- |
| CPU 회수 방식 | 작업이 스스로 반환 | 타이머/우선순위로 강제 회수 |
| 응답성 | 낮을 수 있음 | 대화형 환경에 유리 |
| [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 오버헤드 | 상대적으로 작음 | 상대적으로 큼 |
| 공정성 제어 | 약함 | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 세밀하게 조정 가능 |
| 실패 모드 | 긴 작업 독점, 무한 루프 정지 | [경쟁 조건](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/213_race_condition/), [우선순위 역전](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/205_priority_inversion/), 오버헤드 증가 |

이 비교는 현대 애플리케이션 구조에도 그대로 이어진다. 예를 들어 Node.js [이벤트 루프](/knowledge-base/studynote/02_operating_system/02_process_thread/142_event_loop/), Python `asyncio`, 사용자 수준 [코루틴](/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/) ([Coroutine](/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/))은 내부적으로 협력적 스케줄링을 사용한다. [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 선점형이지만, 런타임 내부 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/)들은 `await`, `yield`, 콜백 반환 시점까지 CPU를 양보하지 않는다는 점에서 [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)형 철학을 계승한다.

따라서 [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)형은 과거 메인프레임의 유물이 아니라, "신뢰할 수 있는 짧은 작업들이 스스로 양보한다"는 전제가 성립할 때 여전히 강력한 모델이다. 다만 이 전제를 어기는 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/)가 섞이면 전체 시스템의 체감 성능은 급격히 나빠진다.

- **📢 섹션 요약 비유**: 선점형이 교통경찰이 직접 신호를 바꿔 흐름을 조절하는 교차로라면, [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)형은 운전자들이 자발적으로 끼어들지 않겠다고 약속한 회전교차로와 같다. 모두가 예의 바르면 부드럽지만, 한 대만 규칙을 무시해도 혼잡이 커진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)형 스케줄링은 "[운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 전체 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)"보다 "특정 실행 환경의 내부 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)"으로 더 자주 등장한다. 대표 사례가 초소형 [마이크로컨트롤러](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/130_microcontroller/) ([Microcontroller](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/130_microcontroller/) Unit, MCU)의 슈퍼 루프 (Super Loop), GUI [이벤트 루프](/knowledge-base/studynote/02_operating_system/02_process_thread/142_event_loop/), 서버 애플리케이션의 협력적 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)다. 공통점은 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) 수가 제한적이고, 실행 시간이 짧으며, 개발자가 양보 지점을 통제할 수 있다는 점이다.

### 실무 시나리오

1. <strong>임베디드 <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/">펌웨어</a></strong>: 센서 읽기, 제어 출력, 통신 송신을 순차 호출하는 슈퍼 루프는 구현이 단순하고 메모리 사용량이 작다. 대신 각 루틴이 오래 걸리지 않도록 잘게 쪼개야 한다.
2. <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/142_event_loop/">이벤트 루프</a> 서버</strong>: 요청 처리 중 긴 CPU 계산을 넣으면 전체 연결이 막히므로, 계산량 큰 작업은 워커 스레드나 별도 프로세스로 넘겨야 한다.
3. <strong><a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/">배치 처리</a></strong>: 인터랙션보다 총 처리량이 중요하고 작업 특성을 예측할 수 있다면, [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)형 계열 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 오버헤드 측면에서 유리할 수 있다.

### 채택 기준

- [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/)가 신뢰 가능하고 실행 시간이 짧은가?
- 응답시간보다 처리량과 단순성이 더 중요한가?
- 명시적 `yield` 지점을 코드 수준에서 관리할 수 있는가?
- 긴 작업을 분할하거나 외부로 오프로드할 수 있는가?

### 회피 기준

- 사용자 상호작용 응답성이 중요한 시스템
- 우선순위가 다른 작업이 섞이는 실시간 환경
- 악성 코드나 무한 루프 가능성이 있는 비신뢰 환경

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [이벤트 루프](/knowledge-base/studynote/02_operating_system/02_process_thread/142_event_loop/) 안에 긴 동기 계산을 넣는 것
- 모든 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/)를 "금방 끝나겠지"라고 가정하는 것
- 기아 현상 보정 없이 SJF만 맹목적으로 적용하는 것

- **📢 섹션 요약 비유**: [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)형 운영은 작은 식당의 셰프 한 명이 주문을 직접 순서대로 처리하는 것과 같다. 메뉴가 단순하면 효율적이지만, 손 많이 가는 주문 하나가 들어오면 나머지 손님 음식이 모두 밀린다.

---

## Ⅴ. 기대효과 및 결론

[비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)형 스케줄링의 가장 큰 장점은 예측 가능한 단순성이다. [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) 개입 지점이 적고 강제 중단이 없으므로 구현이 작고, 실행 중 상태 추적이 쉬우며, 잘 설계된 짧은 [태스크](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) 환경에서는 높은 처리 효율을 낼 수 있다. 특히 제한된 자원 환경이나 협력적 런타임에서는 여전히 경쟁력 있는 선택이다.

하지만 현대 범용 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)에서 이것만으로 전체 시스템을 운영하기는 어렵다. 사용자는 즉각적 반응을 기대하고, 작업은 불균일하며, 신뢰할 수 없는 코드도 함께 돌기 때문이다. 그래서 오늘날의 현실적 해법은 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 수준의 선점형 기반 위에, 필요한 부분에서만 협력적 [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/) 모델을 얹는 하이브리드 설계다.

결론적으로 [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)형 스케줄링은 "옛날 방식"이라기보다 "양보가 통제 가능한 곳에서 빛나는 방식"으로 기억하는 편이 정확하다. 뺏지 않는 자유는 강력하지만, 그 자유를 감당할 규율이 있을 때만 장점이 된다.

- **📢 섹션 요약 비유**: [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)형은 도서관 열람실 좌석 운영과 같다. 조용하고 규칙적인 이용자들만 있으면 가장 효율적이지만, 한 사람이 자리를 독점하면 좋은 규칙도 바로 불편한 규칙으로 바뀐다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :---------- |
| [호위 효과](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/174_convoy_effect/) ([Convoy Effect](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/174_convoy_effect/)) | FCFS형 [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)에서 짧은 작업이 긴 작업 뒤에 묶이는 대표 병목 |
| [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) ([Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)) | [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)형은 이 비용을 줄이는 대신 응답성을 희생함 |
| 협력적 [멀티태스킹](/knowledge-base/studynote/02_operating_system/11_exam_summary/675_multitasking_terminology_preemptive/) (Cooperative [Multitasking](/knowledge-base/studynote/02_operating_system/11_exam_summary/675_multitasking_terminology_preemptive/)) | [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)형 철학이 사용자 수준 런타임으로 확장된 형태 |
| 슈퍼 루프 (Super Loop) | 임베디드 환경에서 흔한 단순 [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/) 실행 구조 |
| [코루틴](/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/) ([Coroutine](/knowledge-base/studynote/02_operating_system/02_process_thread/141_coroutine/)) | 명시적 양보를 통해 [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)형 장점을 현대적으로 활용하는 구조 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">일괄 처리 시스템</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">비선점형 스케줄링</div>
<div class="kb-diagram-tree-item" style="--depth:2">▶ FCFS · SJF · HRN</div>
<div class="kb-diagram-tree-item" style="--depth:2">▶ 호위 효과 · 기아 현상</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">협력적 멀티태스킹</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">이벤트 루프 · 코루틴 · 사용자 수준 스케줄러</div>
</div>
</div>



이 흐름도는 [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)형이 과거 배치 시스템에서 출발해, 오늘날 협력적 런타임 설계로 재해석되는 흐름을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)형은 놀이터 미끄럼틀을 탄 친구가 스스로 내려올 때까지 기다려 주는 규칙이에요.
2. 그래서 타는 친구는 방해받지 않아 좋지만, 오래 타면 뒤 친구들이 계속 기다려야 해요.
3. 모두가 짧게 타고 양보하면 좋지만, 한 친구가 욕심내면 줄이 금방 길어져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 167 / 800

← **이전**: [166. 선점형 스케줄링 (Preemptive Scheduling)](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/166_preemptive_scheduling/)
**다음**: [168. 디스패처 (Dispatcher) - 문맥 교환 수행 모듈](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/) →

---
