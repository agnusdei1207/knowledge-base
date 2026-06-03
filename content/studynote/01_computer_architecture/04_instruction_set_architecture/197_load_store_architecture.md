+++
title = "197. 로드/스토어 아키텍처 (Load-Store Architecture)"
date = 2026-04-19

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 로드/스토어 아키텍처 (Load-Store [Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/))는 메모리 접근을 `LOAD`와 `STORE`에만 맡기고, 산술·[논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 연산은 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) ([Register](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/)) 사이에서만 수행하게 만드는 역할 분리형 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 구조다.
> 2. **가치**: 메모리 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 연산 파이프라인에서 분리하므로 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 실행의 예측 가능성이 높아지고, 파이프라이닝·슈퍼스칼라·[비순차 실행](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/238_out_of_order_execution/) 같은 고성능 기법을 설계하기 쉬워진다.
> 3. **판단 포인트**: 코드 길이는 늘고 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 의존성 관리가 중요해지지만, 컴파일러 최적화와 충분한 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 받쳐 주면 전체 처리량은 오히려 크게 좋아진다.

---

## Ⅰ. 개요 및 필요성

로드/스토어 아키텍처는 메모리에서 값을 가져오는 일과 계산하는 일을 분리한 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 집합 구조다. 즉 `A = B + C`를 계산할 때도 먼저 `LOAD`로 값을 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)에 올리고, 그다음 `ADD` 같은 연산 명령이 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)끼리만 계산하며, 마지막에 `STORE`로 결과를 메모리에 기록한다. 이 구조의 핵심은 <strong>느린 메모리 통신을 계산기 내부에서 직접 처리하지 않게 만드는 것</strong>이다.

이런 방식이 필요해진 이유는 메모리 접근 시간과 코어 내부 연산 속도의 차이가 매우 크기 때문이다. 중앙처리장치인 CPU (Central Processing Unit) 내부의 산술논리장치 [ALU](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/) ([Arithmetic Logic Unit](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/))는 한두 클럭 안에 덧셈을 끝낼 수 있지만, 캐시 미스가 난 메모리 접근은 수십~수백 클럭이 걸릴 수 있다. 만약 하나의 산술 명령이 메모리를 직접 읽고 쓰게 허용하면, 파이프라인은 가장 느린 메모리 응답에 맞춰 흔들리게 된다.

로드/스토어 철학은 특히 [RISC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/195_risc/) (Reduced [Instruction](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Set Computer) 계열에서 강하게 채택되었다. 이는 [CISC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/196_cisc/) (Complex [Instruction](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Set Computer)의 "[명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 하나로 많은 일을 하자"는 접근보다, "[명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)는 단순하게 하고 여러 개를 빠르고 규칙적으로 흘리자"는 판단에 가깝다. 결국 이 구조는 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 수를 줄이는 것이 아니라, <strong>하드웨어가 예측하기 쉬운 형태로 일을 쪼개는 것</strong>에 목적이 있다.

- **📢 섹션 요약 비유**: 로드/스토어 구조는 요리사가 직접 창고에 뛰어가지 않게 하고, 보조가 재료를 미리 도마 위에 올려두는 주방 운영과 같다. 요리사는 요리만, 보조는 운반만 맡을 때 주방 전체 흐름이 끊기지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

로드/스토어 아키텍처의 핵심은 <strong>연산 경로와 메모리 경로를 <a href="/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/">논리</a>적으로 분리</strong>하는 데 있다. 연산 명령은 [범용 레지스터](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/162_gpr/) [GPR](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/162_gpr/) (General Purpose [Register](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/))만 읽고 쓰며, 메모리 접근은 로드/스토어 유닛인 LSU (Load-Store Unit)가 전담한다. 이 덕분에 파이프라인은 "연산은 빠르다, 메모리는 느릴 수 있다"는 사실을 구조적으로 다룰 수 있다.

아래 그림은 동일한 계산을 로드/스토어 방식으로 처리할 때, 어느 단계에서 메모리를 만나고 어느 단계에서 순수 연산이 일어나는지 보여준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">로드/스토어 아키텍처의 실행 분리: 메모리 접근과 연산 분업</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">목표: C = A + B</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">1) LOAD R1,</div><div class="kb-diagram-node">A</div><div class="kb-diagram-connector">▶</div><div class="kb-diagram-note">메모리에서 A를 읽어 R1에 적재</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">2) LOAD R2,</div><div class="kb-diagram-node">B</div><div class="kb-diagram-connector">▶</div><div class="kb-diagram-note">메모리에서 B를 읽어 R2에 적재</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3) ADD R3, R1, R2 ─▶ ALU가 레지스터 R1, R2만 사용해 계산</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">4) STORE</div><div class="kb-diagram-node">C</div><div class="kb-diagram-connector">▶</div><div class="kb-diagram-note">계산 결과 R3를 메모리 C에 저장</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">분리 효과</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">메모리 경로</div><div class="kb-diagram-cell">연산 경로</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">LOAD/STORE</div><div class="kb-diagram-cell">ADD/SUB/AND</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">주소 계산</div><div class="kb-diagram-cell">레지스터 연산</div></div>
</div>
</div>



이 구조가 중요한 이유는 파이프라인 단계별 책임이 선명해지기 때문이다. [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 인출과 해독 뒤에 메모리 접근이 필요한 명령만 LSU를 거치고, 일반 연산은 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)과 [ALU](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/) 안에서 빠르게 끝난다. 덕분에 하드웨어는 포워딩 (Forwarding), [비순차 실행](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/238_out_of_order_execution/) (Out-of-Order Execution, OoO), 로드/스토어 큐 같은 기법을 체계적으로 붙일 수 있다.

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) ([Register](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/) [File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)) | 연산 대상 임시 보관 | [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 수가 부족하면 메모리 스필 (Spill) 증가 |
| 로드/스토어 유닛 (LSU) | 주소 계산, 캐시/메모리 접근 | 캐시 미스 시 전체 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 관리가 핵심 |
| 산술논리장치 ([ALU](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/)) | [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 기반 산술·[논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 연산 | 고정 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 설계가 쉬움 |
| 파이프라인 제어부 | 해저드 감지, 포워딩, 스톨 제어 | load-use hazard 완화가 중요 |

다만 분리가 곧 만능은 아니다. `LOAD` 직후 바로 그 값을 쓰는 명령이 오면 load-use hazard가 생겨 한두 클럭의 대기가 필요할 수 있다. 그래서 좋은 로드/스토어 구조는 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 형식이 단순한 것에서 끝나지 않고, 컴파일러의 재배치와 마이크로아키텍처의 포워딩 설계가 함께 맞물려야 한다.

- **📢 섹션 요약 비유**: 이 구조는 공장에서 자재 운반 레일과 조립 로봇 라인을 분리한 것과 같다. 자재차가 늦더라도 조립 규칙 자체는 단순해지고, 어디서 병목이 생기는지 훨씬 쉽게 보인다.

---

## Ⅲ. 비교 및 연결

로드/스토어 아키텍처를 이해하려면 메모리-직접 연산을 허용하는 구조와 비교해야 한다. 대표적으로 전통적 CISC의 [register](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/)-memory 형태는 `ADD R1, [M]`처럼 연산 명령 안에 메모리 참조를 섞을 수 있다. 반면 로드/스토어 구조는 이 동작을 `LOAD` + `ADD`로 나눈다. 표면적으로는 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 수가 늘지만, 하드웨어 입장에서는 훨씬 다루기 쉬운 입력을 받게 된다.

| 비교 항목 | [Register](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/)-Memory/[CISC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/196_cisc/) 성향 | Load-Store/[RISC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/195_risc/) 성향 |
| :--- | :--- | :--- |
| 연산 [피연산자](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/160_operand/) | [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) + 메모리 혼합 가능 | [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)만 허용 |
| [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 길이/형식 | 다양하고 복합적 | 상대적으로 단순하고 규칙적 |
| 코드 밀도 | 높을 수 있음 | 다소 낮아질 수 있음 |
| 파이프라인 예측 가능성 | 낮아지기 쉬움 | 높아지기 쉬움 |
| 컴파일러 역할 | 상대적으로 작음 | [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 할당·스케줄링이 중요 |

이 차이는 단순히 [ISA](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/157_isa/) ([Instruction Set Architecture](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/157_isa/)) 취향 차이가 아니라, <strong>복잡성을 어디에 둘 것인가</strong>의 문제다. 로드/스토어 구조는 하드웨어 제어를 단순하게 하는 대신, 컴파일러가 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 할당과 명령 재배치를 더 잘해야 한다. 그래서 이 구조는 컴파일러, 캐시, [파이프라인 해저드](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/221_pipeline_hazards/), 분기 예측과 자연스럽게 연결된다.

특히 현대 x86도 내부적으로는 복잡한 [CISC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/196_cisc/) 명령을 잘게 쪼개 마이크로 연산으로 바꿔 실행한다. 이는 외부 ISA는 달라도, <strong>고성능 실행 엔진 내부는 결국 로드/스토어에 가까운 분해된 형태를 선호한다</strong>는 뜻이다. 따라서 로드/스토어는 특정 진영의 문법이 아니라, 현대 고성능 프로세서가 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 얻는 방향을 보여주는 기준선으로 볼 수 있다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">복합 명령 축소</div>
<div class="kb-diagram-tree-item" style="--depth:2">CISC 외부 명령 ─▶ 내부 마이크로 연산 분해</div>
<div class="kb-diagram-tree-item" style="--depth:2">RISC 명령 ─▶ 처음부터 Load/Store 분리</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">파이프라인 예측 가능성 향상</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">슈퍼스칼라·OoO 확장 용이</div>
</div>
</div>



- **📢 섹션 요약 비유**: 한 사람이 운전도 하고 짐도 싣고 계산도 하는 가게보다, 배송·정산·조립을 역할별로 나눈 가게가 커질수록 유리하다. 처음엔 번거로워 보여도 규모가 커질수록 분업의 이익이 커진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 로드/스토어 아키텍처는 단순 이론이 아니라, [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 튜닝과 시스템 설계 판단에 직접 연결된다. 대표적 사례가 메모리 정렬, 캐시 친화적 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 배치, 그리고 메모리 매핑 입출력 MMIO (Memory-Mapped I/O) 처리다. 로드/스토어 구조에서는 장치 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 접근도 결국 특정 주소에 대한 `LOAD`/`STORE`로 표현되므로, 메모리 모델과 배리어의 이해가 중요해진다.

### 판단 기준

1. **고처리량 코어 설계**: 파이프라인 폭을 넓히고 [비순차 실행](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/238_out_of_order_execution/)을 강화하려면 로드/스토어 구조가 유리하다. 메모리 접근 명령과 순수 연산 명령을 구분할 수 있어 스케줄러와 해저드 제어가 단순해진다.
2. **컴파일러 성숙도**: [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 할당, 명령 재배치, 루프 최적화가 약한 환경이라면 로드/스토어의 장점이 충분히 살아나지 못한다. [ISA](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/157_isa/) 선택은 컴파일러 생태계와 함께 봐야 한다.
3. **코드 크기 제약**: 임베디드처럼 플래시 메모리가 매우 작은 환경에서는 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 증가가 부담일 수 있다. 이때는 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)(예: Thumb, RVC ([RISC-V](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/200_riscv/) Compressed)) 같은 보완 기법까지 함께 고려해야 한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- **로드 직후 즉시 사용을 반복하는 코드 배치**: `LOAD` 다음 줄마다 바로 의존 연산을 두면 파이프라인이 자주 멈춘다.
- <strong><a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/">레지스터</a> 부족을 무시한 과도한 임시값 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a></strong>: 소스 수준 표현은 간단해 보여도 실제로는 스필이 늘어 메모리 접근이 폭증할 수 있다.
- <strong><a href="/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/416_memory_barrier/">메모리 배리어</a> 없이 장치 <a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/">레지스터</a>를 제어하는 코드</strong>: 순서 보장이 필요한 구간에서 배리어가 빠지면 MMIO 동작과 멀티코어 가시성 문제가 생길 수 있다.

기술사 관점에서의 핵심 문장은 명확하다. <strong>로드/스토어 아키텍처는 메모리 병목을 없애는 구조가 아니라, 메모리 병목의 위치를 분리하고 제어 가능하게 만드는 구조</strong>다. 따라서 채택 여부는 "[명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 수가 적은가"가 아니라, "예측 가능성과 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화 가능성을 얼마나 높일 수 있는가"로 판단해야 한다.

- **📢 섹션 요약 비유**: 이 구조를 잘 쓰는 것은 택배 상자를 많이 옮기지 않는 것이 아니라, 어느 차선이 배송용이고 어느 차선이 작업용인지 분명히 나누는 일과 같다. 차선을 나누면 정체를 없애지는 못해도 관리와 우회가 쉬워진다.

---

## Ⅴ. 기대효과 및 결론

로드/스토어 아키텍처의 가장 큰 효과는 프로세서가 고속으로 확장될수록 구조적 이점이 커진다는 점이다. [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 형식이 단순하고 연산 대상이 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)로 제한되면, 디코딩·스케줄링·포워딩·예외 처리의 규칙성이 높아진다. 이는 클럭 상승 자체보다도, 높은 처리량과 안정적인 구현을 가능하게 한다.

물론 대가도 있다. 같은 작업을 더 많은 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)로 표현해야 하므로 코드 크기가 커질 수 있고, [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)가 부족하면 오히려 메모리 접근이 늘어 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 떨어질 수 있다. 그래서 현대 로드/스토어 계열은 더 많은 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/), 강한 컴파일러, [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/), 정교한 캐시 계층을 함께 발전시켜 왔다.

결론적으로 로드/스토어 아키텍처는 "메모리를 덜 쓰는 구조"가 아니라 <strong>"메모리 접근을 드러내는 구조"</strong>로 기억하는 것이 정확하다. 이 노출 덕분에 하드웨어와 컴파일러는 병목을 숨기지 않고 정면으로 최적화할 수 있었고, 그 결과가 오늘날 ARM (Advanced [RISC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/195_risc/) Machine), [RISC-V](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/200_riscv/) (Reduced [Instruction](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Set Computer Five), [MIPS](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/201_mips/) ([Microprocessor](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/129_microprocessor/) without Interlocked [Pipeline Stages](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/219_pipeline_stages/)) 계열의 기본 설계 철학으로 이어졌다.

- **📢 섹션 요약 비유**: 좋은 로드/스토어 구조는 문제를 감추는 마술이 아니라, 배관을 벽 밖으로 빼서 어디가 막히는지 바로 보이게 하는 설계와 같다. 배관이 보이면 고치기 쉽고, 확장도 쉬워진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [RISC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/195_risc/) (Reduced [Instruction](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Set Computer) | 로드/스토어 철학을 가장 강하게 채택한 [ISA](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/157_isa/) 계열 |
| [CISC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/196_cisc/) (Complex [Instruction](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Set Computer) | 메모리-직접 연산과 대비되며, 내부적으로는 로드/스토어식 분해를 활용 |
| [GPR](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/162_gpr/) (General Purpose [Register](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/)) | 메모리 대신 연산의 주 작업 공간이 되는 핵심 자원 |
| [파이프라인 해저드](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/221_pipeline_hazards/) ([Pipeline](/knowledge-base/studynote/12_it_management/02_itsm_itil/082_pipeline/) Hazard) | `LOAD` 이후 의존 명령에서 대표적으로 드러나는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 이슈 |
| MMIO (Memory-Mapped I/O) | 장치 접근도 결국 로드/스토어 규칙 안에서 처리된다는 점을 보여줌 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">누산기·메모리 직접 연산 중심 구조</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">레지스터 활용 확대</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">로드/스토어 아키텍처 정착</div>
<div class="kb-diagram-tree-item" style="--depth:2">파이프라인 최적화</div>
<div class="kb-diagram-tree-item" style="--depth:2">슈퍼스칼라 확장</div>
<div class="kb-diagram-tree-item" style="--depth:2">비순차 실행 (OoO)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">ARM (Advanced RISC Machine) · MIPS (Microprocessor without Interlocked Pipeline Stages) · RISC-V (Reduced Instruction Set Computer Five)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">압축 명령어 · 정교한 컴파일러 · 메모리 모델 고도화</div>
</div>
</div>



이 흐름은 "메모리를 직접 만지는 편의성"에서 "[병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 실행을 위한 구조적 분리"로 중심축이 이동한 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터가 계산할 때는, 멀리 있는 창고에서 물건을 가져오는 일과 책상 위에서 계산하는 일을 따로 나누는 게 더 빨라요.
2. 그래서 먼저 심부름꾼이 물건을 책상 위에 올려두고, 계산하는 친구는 책상 위 물건만 가지고 바로 계산해요.
3. 이렇게 하면 창고가 조금 늦어도 계산 규칙은 단순해져서, 컴퓨터가 더 빠르고 똑똑하게 일할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 197 / 803

← **이전**: [196. CISC (Complex Instruction Set Computer)](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/196_cisc/)
**다음**: [198. x86 아키텍처](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/198_x86_architecture/) →

---
