---
title: 205. 데이터패스 (Datapath)
date: '2026-04-19'
tags:
- studynote-computer-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[001_dikw_pyramid|데이터]]패스 (Datapath)는 CPU (Central Processing Unit) 내부에서 [[001_dikw_pyramid|데이터]]를 읽고, 선택하고, 연산하고, 다시 저장하는 실제 하드웨어 경로의 집합이다.
> 2. **가치**: 같은 [[158_instruction|명령어]] 집합 구조 ([[157_isa|Instruction Set Architecture]], [[157_isa|ISA]])를 쓰더라도 [[001_dikw_pyramid|데이터]]패스를 어떻게 구성하느냐에 따라 [[015_지연_데이터_관점|지연]]시간, [[139_throughput|처리량]], 전력 효율이 크게 달라진다.
> 3. **판단 포인트**: 좋은 [[001_dikw_pyramid|데이터]]패스는 단순히 빠른 길이 아니라, [[206_control_unit|제어 유닛]] ([[206_control_unit|Control Unit]], CU)과 정확히 맞물리면서도 파이프라인 해저드와 임계 경로를 감당할 수 있는 균형 잡힌 길이다.

---

## Ⅰ. 개요 및 필요성

[[001_dikw_pyramid|데이터]]패스 (Datapath)는 [[158_instruction|명령어]]가 요구한 작업을 실제 전기 [[130_signal|신호]]의 이동과 연산으로 바꾸는 하드웨어 실행 경로다. [[206_control_unit|제어 유닛]]이 “무엇을 할지”를 결정한다면, [[001_dikw_pyramid|데이터]]패스는 “어디에서 값을 꺼내 어떤 연산기를 지나 어디에 기록할지”를 수행한다. 즉 컴퓨터 구조에서 제어는 의사결정이고, [[001_dikw_pyramid|데이터]]패스는 실행 동선이다.

이 개념이 중요한 이유는 [[158_instruction|명령어]] 하나가 생각보다 많은 하드웨어 단계를 거치기 때문이다. 예를 들어 덧셈 [[158_instruction|명령어]]도 [[164_pc|프로그램 카운터]] (Program [[059_counter|Counter]], [[164_pc|PC]])에서 [[158_instruction|명령어]]를 가져오고, [[057_register|레지스터]] [[501_file_definition_logical_record|파일]] ([[175_register_addressing|Register]] [[501_file_definition_logical_record|File]])에서 [[160_operand|피연산자]]를 읽고, 산술논리연산장치 ([[117_alu|Arithmetic Logic Unit]], [[117_alu|ALU]])에서 계산한 뒤, 결과를 다시 [[057_register|레지스터]]에 써야 한다. 이 경로가 비효율적이면 제어 [[130_signal|신호]]가 정확해도 전체 CPU는 느려진다.

특히 파이프라이닝 이전의 단일 사이클 구조에서는 모든 [[158_instruction|명령어]]가 가장 긴 경로에 맞춰 한 번에 끝나야 했다. 그 결과 메모리 접근이 긴 [[158_instruction|명령어]] 하나 때문에 단순한 [[057_register|레지스터]] 간 덧셈도 느린 클럭을 강요받았다. [[001_dikw_pyramid|데이터]]패스 설계는 바로 이 비효율을 줄이기 위해, 공용 자원을 어떻게 배치하고 경로를 어떻게 나눌지 결정하는 핵심 작업이 되었다.

- **📢 섹션 요약 비유**: [[001_dikw_pyramid|데이터]]패스는 대형 병원의 환자 이동 동선과 같다. 의사가 처방을 내려도 접수, 검사, 수술실, 회복실로 가는 길이 꼬여 있으면 치료가 늦어지듯, CPU도 [[001_dikw_pyramid|데이터]]가 지나가는 길이 엉키면 [[282_performance_tactics|성능]]이 떨어진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[001_dikw_pyramid|데이터]]패스의 핵심은 저장 장치, 연산 장치, 선택 장치, 전달 경로가 하나의 흐름으로 연결된다는 점이다. 대표 구성 요소는 [[164_pc|PC]], [[158_instruction|명령어]] 메모리 ([[158_instruction|Instruction]] Memory), [[057_register|레지스터]] [[501_file_definition_logical_record|파일]], [[117_alu|ALU]], [[001_dikw_pyramid|데이터]] 메모리 ([[001_dikw_pyramid|Data]] Memory), [[041_multiplexer|멀티플렉서]] ([[041_multiplexer|Multiplexer]], [[944_mux_demux_multiplexer_demultiplexer_circuit_sharing|MUX]]), 그리고 단계 사이 값을 붙잡아 두는 파이프라인 [[057_register|레지스터]] ([[082_pipeline|Pipeline]] [[175_register_addressing|Register]])다. [[206_control_unit|제어 유닛]]은 이 부품들에 선택 [[130_signal|신호]]와 [[289_cqrs_db|쓰기]] 허용 [[130_signal|신호]]를 보내고, [[001_dikw_pyramid|데이터]]패스는 그 [[130_signal|신호]]에 맞춰 값을 흘려보낸다.

아래 그림은 파이프라인 [[001_dikw_pyramid|데이터]]패스가 무엇을 연결하는지 한눈에 보여준다. 중요한 점은 [[206_control_unit|제어 유닛]]이 계산 자체를 하지 않고, [[001_dikw_pyramid|데이터]]패스 안의 어느 길을 열지 지정한다는 것이다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Datapath flow: fetch → read → execute → memory → writeback         │
├──────────────────────────────────────────────────────────────────────┤
│ PC ─▶ Instruction Memory ─▶ Stage Register ─▶ Register File         │
│                                                │                     │
│                                                ├──▶ Immediate Select │
│                                                ▼                     │
│                                         ALU / Address Calc           │
│                                                │                     │
│                         Data Memory or ALU Result ─▶ Write Back      │
└──────────────────────────────────────────────────────────────────────┘
```

이 흐름에서 [[282_performance_tactics|성능]]을 좌우하는 것은 두 가지다. 첫째, 어떤 자원이 한 사이클 안에 너무 많은 일을 맡아 임계 경로 (Critical Path)를 길게 만들지 않는가이다. 둘째, 여러 [[158_instruction|명령어]]가 동시에 흐를 때 같은 자원을 두고 충돌하지 않도록 단계와 버퍼를 적절히 나눴는가이다. 그래서 현대 CPU는 단일 거대 경로보다, 여러 짧은 단계로 분리된 파이프라인 [[001_dikw_pyramid|데이터]]패스를 선호한다.

| 구성 요소 | 역할 | 설계 포인트 |
| :-- | :-- | :-- |
| [[164_pc|PC]] | 다음 [[158_instruction|명령어]] 주소 유지 | 분기 시 빠른 갱신 필요 |
| RegFile | [[160_operand|피연산자]] 읽기/결과 저장 | 읽기 [[446_port_and_bus|포트]]·[[289_cqrs_db|쓰기]] [[446_port_and_bus|포트]] 수가 병목이 됨 |
| [[117_alu|ALU]] | 산술·[[369_logic_bomb|논리]]·주소 계산 | 가장 잦은 연산 경로의 [[015_지연_데이터_관점|지연]] 최소화 |
| [[944_mux_demux_multiplexer_demultiplexer_circuit_sharing|MUX]] | 경로 선택 | 제어 [[130_signal|신호]] 증가와 회로 복잡도 증가 |
| [[082_pipeline|Pipeline]] [[175_register_addressing|Register]] | 단계 경계 유지 | 너무 많으면 오버헤드, 너무 적으면 긴 경로 |

즉 [[001_dikw_pyramid|데이터]]패스 설계는 단순 배선 문제가 아니라, “어떤 값을 언제 어디로 보낼 것인가”를 시간축까지 포함해 조직하는 문제다. 파이프라인 [[057_register|레지스터]]를 늘리면 [[133_clock_cycle_time|클럭 주기]]를 줄이기 쉬워지지만, 분기 실패나 [[001_dikw_pyramid|데이터]] 의존 시 [[658_ir_recovery|복구]] 비용이 커진다. 반대로 경로를 단순하게 만들면 제어는 쉬워지지만 [[139_throughput|처리량]]이 낮아진다.

- **📢 섹션 요약 비유**: [[001_dikw_pyramid|데이터]]패스는 물류 창고의 컨베이어벨트와 분류기 같다. 상자를 빠르게 보내려면 벨트만 빠를 것이 아니라, 어느 갈래로 보낼지 고르는 분류기와 중간 적치 구간이 함께 잘 설계되어야 한다.

---

## Ⅲ. 비교 및 연결

[[001_dikw_pyramid|데이터]]패스를 이해하려면 단일 사이클, 다중 사이클, 파이프라인 구조를 함께 봐야 경계가 선명해진다. 세 방식은 같은 [[158_instruction|명령어]]를 실행하지만, “하드웨어를 한 번에 몰아서 쓸지, 단계별로 나눠 돌릴지, 여러 [[158_instruction|명령어]]를 겹쳐 흘릴지”에서 차이가 난다.

| 구분 | 단일 사이클 [[001_dikw_pyramid|데이터]]패스 | 다중 사이클 [[001_dikw_pyramid|데이터]]패스 | 파이프라인 [[001_dikw_pyramid|데이터]]패스 |
| :-- | :-- | :-- | :-- |
| 시간 배치 | [[158_instruction|명령어]] 1개를 1사이클에 완료 | [[158_instruction|명령어]] 1개를 여러 단계로 분리 | 여러 [[158_instruction|명령어]]를 단계별로 겹침 |
| 장점 | 구조가 직관적 | 자원 재사용이 쉬움 | [[139_throughput|처리량]]이 높음 |
| 약점 | 긴 임계 경로 | 단계별 유한 상태 기계 (Finite [[272_state_pattern|State]] Machine, FSM) 제어 | 해저드 처리 필요 |
| 대표 이슈 | 느린 클럭 | 제어 상태 증가 | 포워딩·스톨·플러시 |

이 차이는 [[206_control_unit|제어 유닛]]과도 직접 연결된다. 단일 사이클에서는 한 번의 제어 [[130_signal|신호]] 묶음으로 전체 [[158_instruction|명령어]]를 끝내야 하지만, 다중 사이클과 파이프라인에서는 단계별로 다른 제어가 필요하다. 따라서 [[001_dikw_pyramid|데이터]]패스가 세분화될수록 제어 [[130_signal|신호]]도 더 정교해지고, 반대로 제어 전략이 복잡해질수록 [[001_dikw_pyramid|데이터]]패스는 그 [[130_signal|신호]]를 안전하게 수용할 구조를 갖춰야 한다.

또한 [[001_dikw_pyramid|데이터]]패스는 파이프라인 해저드와 분리해서 볼 수 없다. 구조 해저드 ([[222_structural_hazard|Structural Hazard]])는 같은 자원을 동시에 요구할 때 생기고, [[223_data_hazard|데이터 해저드]] ([[223_data_hazard|Data Hazard]])는 앞 [[158_instruction|명령어]] 결과가 아직 기록되기 전에 뒤 [[158_instruction|명령어]]가 읽으려 할 때 발생한다. 이를 줄이기 위해 포워딩 (Forwarding), 스톨 (Stall), [[279_split_cache|분리 캐시]], 다중 [[446_port_and_bus|포트]] [[057_register|레지스터]] [[501_file_definition_logical_record|파일]] 같은 설계가 [[001_dikw_pyramid|데이터]]패스 안으로 들어온다.

- **📢 섹션 요약 비유**: 단일 사이클은 한 사람이 요리를 처음부터 끝까지 다 하는 주방이고, 다중 사이클은 한 사람이 단계별로 나눠서 하는 주방이며, 파이프라인은 여러 사람이 조리·플레이팅·서빙을 동시에 이어받는 주방이다. 속도가 빨라질수록 서로 부딪치지 않게 동선을 더 치밀하게 짜야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무나 기술사 관점에서 [[001_dikw_pyramid|데이터]]패스의 핵심 판단은 “[[282_performance_tactics|성능]]을 높이기 위해 무엇을 추가하고, 그 대가로 무엇을 감수할 것인가”이다. 예를 들어 임베디드 프로세서는 전력과 면적이 중요하므로 단순한 인오더 (In-Order) 파이프라인 [[001_dikw_pyramid|데이터]]패스를 선택하는 경우가 많다. 반면 고성능 서버용 CPU는 더 넓은 발행폭과 더 많은 포워딩 경로, 복수 실행 유닛을 두어 복잡하지만 높은 [[139_throughput|처리량]]을 확보한다.

### 설계 체크포인트

1. 가장 긴 [[117_alu|ALU]]/메모리 경로가 목표 [[133_clock_cycle_time|클럭 주기]] 안에 들어오는가?
2. [[509_register_file_ports|레지스터 파일 포트]] 수가 실제 [[158_instruction|명령어]] 병렬성 요구를 감당하는가?
3. 포워딩 경로를 추가했을 때 [[015_지연_데이터_관점|지연]] 감소 효과가 [[944_mux_demux_multiplexer_demultiplexer_circuit_sharing|MUX]] 증가 비용보다 큰가?
4. 분기 실패 시 플러시 비용이 파이프라인 깊이에 비해 과도하지 않은가?

### 피해야 할 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 모든 [[158_instruction|명령어]]를 빠르게 하겠다며 경로를 무한정 추가해 MUX와 배선을 비대하게 만드는 설계
- 메모리 [[015_지연_데이터_관점|지연]]을 무시한 채 [[117_alu|ALU]] 중심으로만 최적화해 실제 워크로드에서 병목이 남는 설계
- 해저드 처리 없이 “이론상 [[139_throughput|처리량]]”만 보고 파이프라인을 깊게 만드는 설계

결국 좋은 [[001_dikw_pyramid|데이터]]패스는 가장 화려한 구조가 아니라, 목표 제품의 전력·면적·[[282_performance_tactics|성능]] 조건에 맞는 구조다. 교육용 [[195_risc|RISC]] 예제 [[001_dikw_pyramid|데이터]]패스와 애플리케이션 프로세서 (Application Processor, [[572_ap_access_point_ds_distribution_system|AP]]) [[001_dikw_pyramid|데이터]]패스가 다른 이유도 여기에 있다. 전자는 원리를 명확히 보여주는 것이 목적이고, 후자는 실제 워크로드에서 높은 효율을 내야 하기 때문이다.

- **📢 섹션 요약 비유**: [[001_dikw_pyramid|데이터]]패스 설계는 도시 도로망 계획과 같다. 차가 막힌다고 무조건 고가도로를 계속 올리면 공사비와 관리비가 폭증하듯, CPU도 우회 경로를 많이 넣는다고 항상 좋은 것이 아니라 필요한 곳에만 넣어야 한다.

---

## Ⅴ. 기대효과 및 결론

잘 설계된 [[001_dikw_pyramid|데이터]]패스는 [[158_instruction|명령어]] 실행 시간을 줄이고, 파이프라인의 [[139_throughput|처리량]]을 높이며, [[206_control_unit|제어 유닛]]이 만든 [[130_signal|신호]]를 예측 가능하게 실현한다. 그 결과 같은 ISA를 유지하면서도 더 높은 [[282_performance_tactics|성능]]과 더 나은 전력 효율을 얻을 수 있다. [[204_microarchitecture|마이크로아키텍처]] 경쟁에서 [[001_dikw_pyramid|데이터]]패스가 핵심인 이유가 바로 여기에 있다.

다만 [[001_dikw_pyramid|데이터]]패스는 넓히기만 하면 끝나는 구조가 아니다. 경로가 많아질수록 배선 길이, 제어 복잡도, [[395_verification_process_review|검증]] 난이도, 소비전력이 함께 증가한다. 특히 최신 고성능 코어에서는 [[001_dikw_pyramid|데이터]]패스 자체가 너무 복잡해져, 오히려 클럭 향상보다 [[395_verification_process_review|검증]] 가능성과 전력 관리가 더 큰 제약이 되기도 한다.

따라서 [[001_dikw_pyramid|데이터]]패스는 “[[001_dikw_pyramid|데이터]]가 흐르는 길”로만 외우기보다, “[[282_performance_tactics|성능]]과 복잡도의 타협이 새겨진 하드웨어 실행 구조”로 기억하는 것이 정확하다. [[206_control_unit|제어 유닛]]이 두뇌라면 [[001_dikw_pyramid|데이터]]패스는 단순 근육이 아니라, 근육·혈관·관절이 함께 묶인 실행 인프라다.

- **📢 섹션 요약 비유**: [[001_dikw_pyramid|데이터]]패스는 운동선수의 몸과 같다. 근육만 크다고 좋은 선수가 되지 않듯, CPU도 연산기만 강해서는 안 되고 혈관처럼 이어진 전달 경로와 관절처럼 움직이는 선택 구조가 함께 조화로워야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [[206_control_unit|제어 유닛]] ([[206_control_unit|Control Unit]], CU) | [[001_dikw_pyramid|데이터]]패스의 경로 선택과 [[289_cqrs_db|쓰기]] 시점을 제어하는 [[130_signal|신호]] 발생 주체 |
| 산술논리연산장치 ([[117_alu|Arithmetic Logic Unit]], [[117_alu|ALU]]) | [[001_dikw_pyramid|데이터]]패스 중심에서 산술·[[369_logic_bomb|논리]]·주소 계산을 수행하는 연산 블록 |
| 파이프라인 [[057_register|레지스터]] ([[082_pipeline|Pipeline]] [[175_register_addressing|Register]]) | 단계 사이 값을 고정해 [[139_throughput|처리량]]을 높이는 [[001_dikw_pyramid|데이터]]패스 경계 장치 |
| [[228_data_forwarding|데이터 포워딩]] ([[228_data_forwarding|Data Forwarding]]) | 결과를 [[057_register|레지스터]] 기록 전에 우회 전달해 [[223_data_hazard|데이터 해저드]]를 줄이는 기법 |
| [[158_instruction|명령어]] 집합 구조 ([[157_isa|Instruction Set Architecture]], [[157_isa|ISA]]) | [[001_dikw_pyramid|데이터]]패스가 구현해야 하는 외부 기능 계약 |

### 📈 관련 키워드 및 발전 흐름도

```text
단일 사이클 Datapath
        │
        ▼
다중 사이클 Datapath
        │
        ▼
파이프라인 Datapath
        │
        ├──▶ 구조 해저드 대응: 자원 분리, 다중 포트
        ├──▶ 데이터 해저드 대응: Forwarding, Stall
        └──▶ 고성능 확장: Superscalar, Out-of-Order
```

이 흐름은 [[001_dikw_pyramid|데이터]]패스가 단순 실행 경로에서 출발해, 파이프라인 충돌을 다루고, 다시 다중 실행 구조로 확장되는 진화를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[001_dikw_pyramid|데이터]]패스는 컴퓨터 안에서 숫자들이 지나가는 길과 작업대예요.
2. 숫자는 창고에서 나와 계산 기계에서 계산하고 다시 제자리에 돌아가요.
3. 길이 잘 정리되어 있으면 컴퓨터는 빨리 일하고, 길이 엉키면 중간에서 자꾸 막혀요.
