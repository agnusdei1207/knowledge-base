---
title: "394. vfork()"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
weight: 394
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: `vfork()`(Virtual Fork)는 부모 프로세스를 복제할 때 램은 물론이고 <strong><a href="/studynote/02_operating_system/06_memory_management/353_page_table/">페이지 테이블</a> 장부마저 복사하지 않고 부모의 메모리 우주를 통째로 완전히 똑같이 공유(Share)해 버리는, 세상에서 가장 가볍고 극단적인 <a href="/studynote/02_operating_system/02_process_thread/104_process_creation/">프로세스 생성</a> 시스템 콜</strong>이다.
> 2. **가치**: 아무리 [COW](/studynote/02_operating_system/09_file_system/542_cow_file_system/)([Copy-on-Write](/studynote/02_operating_system/09_file_system/542_cow_file_system/))가 가벼워도 수 MB의 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)을 복사하는 미세한 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)(Overhead)조차 용납할 수 없는 구형 시스템이나 극단적 실시간(RTOS) 환경에서, <strong>수 마이크로초(µs) 내에 새 프로세스를 쏴 올리는 최고속의 런타임을 제공</strong>한다.
> 3. **융합**: 자식이 부모의 메모리를 덮어쓰는 대참사를 막기 위해, 자식이 1초 안에 `exec()`(새 프로그램 덮어쓰기)를 부르거나 죽기(`exit()`) 전까지 <strong>부모 프로세스의 실행을 강제로 기절(Block)시켜버리는 치명적 트레이드오프</strong>를 동반하는 양날의 검이다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 일반적인 `fork()`는 COW를 써서 램 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 복사는 피하지만, 그래도 "가상 주소 매핑 장부([페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/))" 자체는 자식용으로 1벌 새로 쫙 복사해 줘야 한다. `vfork()`는 이 장부 복사마저 생략하고, 자식이 부모의 장부와 램 공간을 100% 동일하게 물고 태어나는 [돌연변이](/studynote/04_software_engineering/10_trends_pm_quality/638_mutation_testing_test_case_verification/) 함수다.
- **필요성**: 리눅스에서 프로세스를 띄우는 절대 공식은 `fork()`로 내 판박이를 낳은 뒤 즉시 `exec()`를 때려서 그 자식의 뇌를 완전히 새로운 앱(예: 카카오톡)으로 덮어씌우는 것이다. 공학자들은 분노했다. "아니, 어차피 0.001초 뒤에 `exec()` 때려서 지 기억(메모리 장부) 다 날려버리고 새 뇌로 갈아 끼울 건데, 뭐 하러 COW니 뭐니 하면서 힘들게 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/) 장부를 복사해 주고 자빠졌냐? 그냥 복사 자체를 1도 하지 마!" 이 극단적인 귀차니즘과 최적화의 결정체가 바로 `vfork()`다.

- **등장 배경 및 구시대의 생존술**:
  1. <strong><a href="/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/">초기</a> UNIX의 암흑기</strong>: [COW](/studynote/02_operating_system/09_file_system/542_cow_file_system/)([Copy-on-Write](/studynote/02_operating_system/09_file_system/542_cow_file_system/)) 기술이 발명되기 전, `fork()`는 수십 MB의 물리 램을 쌩으로 복사하는 최악의 함수였다.
  2. **vfork의 눈부신 등장 (BSD 3.0)**: "복사를 안 하면 램 복사 렉이 없어지잖아!"라며 등장한 `vfork()`는 당시 굼벵이 같던 서버 속도를 로켓으로 만들어준 구원자였다.
  3. **COW의 등장과 계륵**: 나중에 OS에 갓술인 COW가 탑재되며 `fork()`가 충분히 가벼워지자, 부모를 멈춰 세우는 기형적인 `vfork()`는 버그 유발자로 찍혀 POSIX 표준에서 삭제 권고를 받는 등 천덕꾸러기 신세로 전락했다.

```text
+-------------------------------------------------------------------------+
|        fork() + COW  vs  vfork() 의 동작 파이프라인 비교                |
+-------------------------------------------------------------------------+
|                                                                         |
| -> 1. fork() + exec() 구조 (현대 표준)                                   |
|  [부모] -(fork)--> 자식용 페이지 테이블 '복사 생성' (미세한 지연)        |
|  [부모] ---> 계속 지 할 일 함 (동시 실행 🟢)                             |
|  [자식] ---> 부모 장부 복사본 들고 놀다가 -(exec)--> 새 장부로 갈아탐     |
|                                                                         |
| -> 2. vfork() 구조 (극한의 변태 최적화)                                  |
|  [부모] -(vfork)--> 자식 생성! 장부 복사? 그런 거 없음. 원본 그대로 씀.  |
|  [부모] ---> 자식한테 뇌 뺏기고 '기절 (Blocked)' ☠️                      |
|  [자식] ---> 부모 뇌(원본 메모리) 들고 신나게 돎 -(exec)--> 새 뇌로 갈아탐|
|  [부모] ---> 자식이 새 뇌로 갈아타고 나서야 기절에서 깨어나 할 일 함 🟢  |
+-------------------------------------------------------------------------+
```
**[다이어그램 해설]** `vfork()`는 [동시성](/studynote/15_devops_sre/01_culture_methodology/014_concurrency/)([Concurrency](/studynote/05_database/05_distributed_nosql_newsql/266_other_transparency/))을 스스로 파괴하는 기형적인 구조다. 자식이 태어난 순간 부모는 무조건 멈춘다. 자식이 자기만의 새로운 메모리 공간(`exec`)을 얻어 부모의 공간에서 독립해 나가는 그 찰나의 순간(수 마이크로초)까지만 잠시 몸(메모리)을 하나로 합쳐 쓰는 심비오트(기생수) 같은 상태다. 장부 복사 비용(수 밀리초)조차 없애버린 극한의 속도를 얻었다.

- **📢 섹션 요약 비유**: `fork`는 엄마가 아이에게 새 자전거를 사주고 각자 갈 길 가는 것이지만, `vfork`는 아이가 자전거 사달라고 떼쓰니까 엄마가 타고 있던 자전거를 던져주고 아이가 저 멀리 새 자전거(`exec`)를 훔쳐 탈 때까지 길거리에 멍하니 서서 기다리는 눈물겨운 양보입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 주소 공간 완벽 공유와 파멸적 버그(Bug)의 위험

`vfork()`로 태어난 자식은 부모의 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)([Stack](/studynote/08_algorithm_stats/04_datastructure/057_stack/)), 힙([Heap](/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/)), [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 영역을 100% 쌩으로 공유한다. [COW](/studynote/02_operating_system/09_file_system/542_cow_file_system/) 락 같은 안전장치도 없다.
- 만약 자식이 태어나서 `exec()`를 부르기 전에 실수로 `int x = 10;` 이라며 변수 값을 바꿔버리면?
- 그건 <strong>부모 프로세스의 메모리를 직접 난도질한 것</strong>과 똑같다.
- 더 최악은 자식이 함수를 리턴(`return`)해 버리는 경우다. 자식이 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) 프레임을 파괴하며 리턴하면, 나중에 깨어난 부모는 찢어진 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)을 밟고 즉시 `Segmentation Fault`로 박살 난다.

**[vfork의 철칙]**: 자식은 태어나자마자 숨도 쉬지 말고 오직 `exec()`나 `_exit()` 둘 중 하나만 바로 호출해야 한다. 다른 코드를 단 한 줄이라도 쓰면 서버가 터지는 시한폭탄을 안고 코딩해야 한다.

---

### 하드웨어 [MMU](/studynote/02_operating_system/06_memory_management/328_mmu/) 관점에서의 극경량화

- `fork()`: 부모의 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)(수만 줄의 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/))을 순회하며 자식의 새 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)을 할당하고(RAM 소모), PTE에 락(R/O)을 거는 CPU 루프 연산이 필요하다.
- <strong><code>vfork()</code></strong>: 자식의 `PTBR(페이지 테이블 시작 레지스터)`에 그냥 부모의 `PTBR` 주소값을 띡! 하고 복사 붙여넣기 한 번 하고 끝난다. 메모리 낭비 0, 루프 연산 0, 완벽한 $O(1)$의 하드웨어 스위칭이다.

- **📢 섹션 요약 비유**: 회사 법인 카드를 하나 더 발급받아(fork) 나눠 쓰는 게 아니라, 사장님 지갑에서 유일한 법인 카드 1장을 확 뺏어서(vfork) 결제(`exec`)만 딱 하고 돌려주는 방식입니다. 뺏어간 동안 사장님이 결제 못 하고 식당에 묶여있는 건 감수해야 할 페널티입니다.

---

## Ⅲ. 비교 및 연결

### 비교 1: [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)([Thread](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) vs vfork()

"메모리를 100% 공유한다면 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)랑 다를 게 뭔가요?"
면접에서 가장 많이 나오는 날카로운 맹점이다.

| 비교 항목 | 멀티 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) (`pthread_create`) | `vfork()` 호출 |
|:---|:---|:---|
| **메모리 공유** | 코드/[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)/힙 공유, <strong><a href="/studynote/08_algorithm_stats/04_datastructure/057_stack/">스택</a>은 각자 따로 분리됨</strong> | 코드/[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)/힙, 심지어 <strong><a href="/studynote/08_algorithm_stats/04_datastructure/057_stack/">스택</a>(<a href="/studynote/08_algorithm_stats/04_datastructure/057_stack/">Stack</a>)까지 100% 동일 공유</strong> |
| **실행 주체** | 부모 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)와 자식 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 **동시에 병렬로 실행됨** | 자식이 `exec` 할 때까지 부모는 **강제 정지(Blocked)됨** |
| <strong><a href="/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a> 목적</strong> | 1개의 프로그램 안에서 여러 일을 쪼개서 같이 하려고 | 아예 다른 남의 프로그램(`exec`)을 1초라도 빨리 띄우려고 |
| **안전성** | 안전함 (각자 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)이 있어 지역 변수 안 섞임) | ☠️ 치명적 ([스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)이 같아서 자식이 변수 만지면 부모 죽음) |

### fork + [COW](/studynote/02_operating_system/09_file_system/542_cow_file_system/) 가 대세가 된 이유 (vfork의 몰락)
[초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 유닉스에서 `vfork()`는 영웅이었지만, 하드웨어 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 미친 듯이 발전하면서 영웅은 노망난 늙은이가 되었다.
- 현대의 `fork() + COW`는 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/) 복사 속도가 마이크로초(µs) 단위로 떨어졌다. 체감 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 거의 없다.
- 프로그래머 입장에서 "자식이 뭘 건드릴지 몰라 부모가 터질까 전전긍긍하는 `vfork`"를 쓸 바에야, 0.001초 미세하게 느리더라도 마음 편하게 맘대로 코딩할 수 있는 `fork`를 쓰는 것이 백배 천배 정신 건강에 좋았다.
- 결국 최신 POSIX 표준은 `vfork()`를 구시대의 유물로 선언했고, 요즘 리눅스 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에서 프로그래머가 `vfork()`를 호출하면 OS가 그냥 내부적으로 꼼수를 써서 가벼운 `fork()`처럼 비슷하게 돌려버리는 식으로 퉁치고 있다.

```text
+----------+------------+------------+-----------------------------+
| 프로세스 생성| 램 데이터 복사 | 페이지장부 복사 | 부모 동시 실행 |
+----------+------------+------------+-----------------------------+
| 구형 fork | ☠️ 100% 쌩복사| 100% 복사   | 🟢 동시 실행           |
| 현대 fork | 🟢 COW (안함)| 100% 복사   | 🟢 동시 실행            |
| vfork()  | 🟢 안 함    | 🟢 안 함    | ☠️ 부모 기절              |
+----------+------------+------------+-----------------------------+
```
**[매트릭스 해설]** `vfork`는 오직 '[페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 장부 복사'라는 쥐꼬리만 한 오버헤드 하나를 줄이기 위해 부모 프로세스의 심장([동시성](/studynote/15_devops_sre/01_culture_methodology/014_concurrency/))을 정지시켜버린 극약 처방이다. 최신 서버 환경에서는 이 쥐꼬리만 한 이득이 부모가 기절해서 버려지는 CPU 사이클(코어 놀림)보다 훨씬 작기 때문에 철저히 버림받았다.

- **📢 섹션 요약 비유**: F1 레이싱에서 차체 무게(장부 복사) 1kg을 줄이겠다고 드라이버에게 물([동시성](/studynote/15_devops_sre/01_culture_methodology/014_concurrency/))을 한 모금도 안 마시게 한 `vfork` 전략은, 훗날 엔진 출력(CPU [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/))이 수천 마력으로 늘어나자 1kg 가벼운 것보다 드라이버가 탈수증으로 기절(부모 Block)하는 손해가 훨씬 커져서 폐기된 전술과 같습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: 임베디드 리눅스 (uClinux)와 [MMU](/studynote/02_operating_system/06_memory_management/328_mmu/)-less 환경
서버 시장에선 버림받았지만, 세상 어딘가에는 여전히 `vfork()`가 신으로 추앙받는 곳이 있다. 바로 초소형 [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/), 라우터, 스마트워치 등에 들어가는 <strong>MMU가 없는(<a href="/studynote/02_operating_system/06_memory_management/328_mmu/">MMU</a>-less) 임베디드 칩셋(uClinux 등)</strong> 생태계다.
1. **문제 상황**: [MMU](/studynote/02_operating_system/06_memory_management/328_mmu/)([가상 메모리](/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) 하드웨어)가 없으면? 애초에 [페이징](/studynote/02_operating_system/04_synchronization/259_paging/) 테이블도 없고 [COW](/studynote/02_operating_system/09_file_system/542_cow_file_system/)(읽기 락킹)라는 흑마술 자체가 하드웨어적으로 성립하지 않는다.
2. **fork의 절대적 불가능**: MMU가 없으니 `fork()`를 치면 가짜 주소 매핑이 안 되므로 진짜 물리 램을 100% 통째로 복사(Memcpy)해야만 한다. 램 16MB짜리 임베디드 기기에서 이 짓을 하면 1초 만에 OOM으로 기계가 폭발한다.
3. **vfork의 영웅적 부활**:
   - 이 척박한 환경에서 새 프로세스를 띄울 유일한 생명줄이 바로 장부 복사도, 램 복사도 전혀 하지 않는 `vfork()`다.
   - uClinux 환경에서는 `fork()` 시스템 콜 자체가 아예 막혀있으며, 모든 개발자는 프로세스 분기 시 강제로 `vfork()`만을 사용하여 부모를 재우고 램을 쥐어짜며 코딩해야 한다. 가난한 하드웨어 환경이 낳은 실무의 눈물겨운 적응기다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/): 파이썬/Node.js에서의 `vfork` 호출 시도
고수준 스크립트 언어나 거대한 프레임워크가 뒤에서 돌고 있는 환경에서 C 모듈로 `vfork`를 때리면 지옥을 맛본다. 자바스크립트 V8 엔진이나 파이썬 런타임은 백그라운드에서 [가비지 컬렉터](/studynote/05_database/uncategorized/591_mvcc_garbage_collection_vacuum/)(GC) [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 미친 듯이 힙을 뒤적거리고 변수를 조작한다. 이 상태에서 `vfork`로 부모-자식 메모리가 100% 공유되면, 자식이 띄워지기도 전에 백그라운드 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 메모리를 박살 내어 알 수 없는 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 패닉으로 서버가 불탄다.

- **📢 섹션 요약 비유**: 부잣집(서버 CPU)에서는 설거지(장부 복사)하기 귀찮다고 밥 안 먹고 굶는 짓(vfork)을 하면 바보 취급받지만, 무인도([MMU](/studynote/02_operating_system/06_memory_management/328_mmu/) 없는 [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/))에 표류해서 물이 한 방울도 없을 때는 굶어서 설거짓거리를 안 만드는 것만이 유일하게 생존할 수 있는 위대한 생존 지침이 됩니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 내용 |
|:---|:---|
| **프로세스 런치 레이턴시 최저화**| 수십 MB에 달하는 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/) 매핑 연산을 생략하여, [프로세스 생성](/studynote/02_operating_system/02_process_thread/104_process_creation/) 시간을 밀리초(ms) 단위에서 마이크로초(µs) 단위로 수직 상승 |
| <strong>메모리 제약 환경 생존(<a href="/studynote/02_operating_system/06_memory_management/328_mmu/">MMU</a>-Less)</strong>| [가상 메모리](/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)가 칩셋 구조상 불가능한 초저가형 [마이크로컨트롤러](/studynote/01_computer_architecture/03_architecture_basics_performance/130_microcontroller/)(MCU)에서 [멀티태스킹](/studynote/02_operating_system/11_exam_summary/675_multitasking_terminology_preemptive/) 흉내를 낼 수 있게 해주는 유일한 치트키 |
| <strong><a href="/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/">운영체제</a> 철학의 스펙트럼 확장</strong>| 자원을 격리([Isolation](/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/))하는 일반적 OS의 원칙을 정면으로 깨부수고, [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 위해 100% 쌩 공유(Sharing)를 허용한 극단적 타협의 표본 |

### 결론 및 미래 전망

`vfork()`는 "가장 위험한 것이 가장 빠르다"는 시스템 프로그래밍의 뒷골목 철학을 여과 없이 보여주는 야생의 시스템 콜이다. [가상 메모리](/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)와 COW라는 우아한 갑옷이 발명되기 전, 척박한 물리 램 환경에서 프로세스를 낳기 위해 부모가 뇌를 멈추고 몸을 빌려줘야 했던 원시적인 투쟁의 흔적이다. 현대의 x86 리눅스 데스크톱 환경에서는 사실상 박물관에 박제된 화석이 되었고, `posix_spawn()` 같은 더 안전하고 최적화된 최신 융합 함수들에 밀려 사라지고 있다. 하지만 화성 탐사선이나 초소형 드론의 심장에 박힌 [MMU](/studynote/02_operating_system/06_memory_management/328_mmu/)-less 임베디드 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 안에서는, 단 1바이트의 램과 1클럭의 전력도 허투루 쓰지 않으려는 이 거칠고 위험한 함수의 톱니바퀴가 지금 이 순간에도 수천만 번씩 격렬하게 돌아가고 있다.

- **📢 섹션 요약 비유**: 최정보 에어백과 자율주행이 달린 최고급 세단(현대 fork) 시대에, 문짝 떼어내고 안전벨트도 없이 오직 제로백(가속) 하나에만 몰빵한 구형 레이싱카(vfork)입니다. 일반 도로에선 목숨 걸고 타야 하는 불법 개조 차량이지만, 아직도 오프로드(임베디드) 진흙탕 경주에서는 이만한 가성비 괴물이 존재하지 않습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [파일 지원 메모리](/studynote/02_operating_system/07_virtual_memory/392_file_backed_memory/) ([File-backed Memory](/studynote/02_operating_system/07_virtual_memory/392_file_backed_memory/)) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [쓰기 시 복사](/studynote/02_operating_system/07_virtual_memory/393_copy_on_write/) ([COW](/studynote/02_operating_system/09_file_system/542_cow_file_system/), [Copy-on-Write](/studynote/02_operating_system/09_file_system/542_cow_file_system/)) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [페이지 교체](/studynote/02_operating_system/04_synchronization/260_page_replacement/) ([Page Replacement](/studynote/02_operating_system/04_synchronization/260_page_replacement/))의 필요성 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [변경 비트](/studynote/02_operating_system/07_virtual_memory/396_dirty_bit/) (Modify [Bit](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) / [Dirty Bit](/studynote/02_operating_system/07_virtual_memory/396_dirty_bit/)) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[쓰기 시 복사 (COW, Copy-on-Write)]
    |
    v
[vfork()]
    |
    +---> [페이지 교체 (Page Replacement)의 필요성]
    +---> [변경 비트 (Modify Bit / Dirty Bit)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. vfork()은 컴퓨터가 메모리를 더 크게 보이게 하고 부족함을 숨기는 방법이에요.
2. 먼저 [쓰기 시 복사](/studynote/02_operating_system/07_virtual_memory/393_copy_on_write/) ([COW](/studynote/02_operating_system/09_file_system/542_cow_file_system/), [Copy-on-Write](/studynote/02_operating_system/09_file_system/542_cow_file_system/))을 이해하면 vfork()이 왜 필요한지 더 쉽게 보여요.
3. 그래서 vfork()을 잘 알면 나중에 [페이지 교체](/studynote/02_operating_system/04_synchronization/260_page_replacement/) ([Page Replacement](/studynote/02_operating_system/04_synchronization/260_page_replacement/))의 필요성도 훨씬 쉽게 배울 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 394 / 800

<- **이전**: [393. 쓰기 시 복사 (COW, Copy-on-Write) - fork() 시 자원 공유하다 쓸 때 페이지 복제](/studynote/02_operating_system/07_virtual_memory/393_copy_on_write/)
**다음**: [395. 페이지 교체 (Page Replacement)의 필요성 - 프레임 가용 공간 부족 시 (Over-allocation)](/studynote/02_operating_system/07_virtual_memory/395_page_replacement_algorithm/) ->

---
