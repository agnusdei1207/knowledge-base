+++
title = "90. 배정밀도 (Double Precision, FP64)"
date = 2026-04-19

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 배정밀도 (Double [Precision](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/), FP64)는 [IEEE 754](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/088_ieee_754/) 표준에 정의된 64비트(8바이트) [부동소수점](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/087_floating_point/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 포맷으로, 지수부와 가수부를 확장하여 연산 오차를 극도로 통제한다.
> 2. **가치**: [단정밀도](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/089_single_precision/) (FP32)의 7자리 유효숫자 한계를 15~17자리로 확장하여, 수치해석, 궤도 계산, 금융 시스템 등 오차 누적이 치명적인 도메인에서 정확성을 보장한다.
> 3. **판단 포인트**: FP32 대비 2배의 메모리 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)과 4배의 연산 파이프라인 지연이 발생하므로, 높은 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)가 반드시 필요한 [HPC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/548_automotive_hpc/) ([High Performance Computing](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/226_hpc_supercomputing_infrastructure/)) 환경에서 선별적으로 채택해야 한다.

---

## Ⅰ. 개요 및 필요성

배정밀도 (Double [Precision](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/), FP64)는 실수를 컴퓨터 메모리에 저장하기 위해 [단정밀도](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/089_single_precision/)(32비트)의 두 배인 64비트를 사용하는 아키텍처 규격이다. 부호(1비트), 지수(11비트), 가수(52비트)로 구성되며, 극도로 크거나 작은 수를 다룰 때 발생하는 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) 손실을 방지하기 위해 설계되었다.

컴퓨터가 실수를 2진수로 변환하여 계산할 때, 무한 소수는 필연적으로 유한한 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수에 맞게 잘려나가며 잘림 오차 (Truncation Error)가 발생한다. [단정밀도](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/089_single_precision/) 환경에서 우주선의 궤적이나 양자 역학 시뮬레이션을 수행하면, 미세한 오차가 곱셈과 나눗셈을 거치며 수만 배로 증폭되어 시스템 붕괴를 초래한다. 배정밀도는 이러한 치명적인 오차 누적을 막기 위해 유효숫자의 해상도를 비약적으로 늘린 '안전망' 역할을 한다.

- **📢 섹션 요약 비유**: [단정밀도](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/089_single_precision/)가 일반적인 현미경이라면, 배정밀도는 원자의 구조를 보면서 동시에 은하계 전체를 관측할 수 있는 초대형 전자현미경과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

배정밀도 포맷은 64비트라는 거대한 공간을 분할하여 수의 스케일과 디테일을 동시에 극대화한다. 핵심은 11비트로 늘어난 지수부와 52비트로 확장된 가수부의 조합이다.

| 구성 요소 | [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수 | 역할 | 물리적 한계치 |
| :--- | :--- | :--- | :--- |
| **부호 (Sign)** | 1비트 | 양수/음수 결정 | 0 (양수), 1 (음수) |
| **지수 (Exponent)** | 11비트 | 수의 스케일(배율) 결정 | $[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)^{-308}$ ~ $[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)^{308}$ 범위 커버 |
| **가수 (Mantissa)** | 52비트 | 실제 유효 숫자(디테일) 저장 | 10진수 기준 15~17자리 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) 보존 |

```text
┌──────────────────────────────────────────────────────────────┐
│           배정밀도 (FP64) 비트 레이아웃 및 구성              │
├──────────────────────────────────────────────────────────────┤
│ [63]    [62 <--- 11 bits ---> 52]    [51 <---- 52 bits ----> 0]
│ ┌──┐    ┌───────────────────────┐    ┌────────────────────────┐
│ │ S│    │   지수부 (Exponent)   │    │    가수부 (Mantissa)   │
│ └──┘    └───────────────────────┘    └────────────────────────┘
│ 부호           배율 결정 (크기)             유효 숫자 (정밀도)  │
│                                                              │
│ * 지수 편향 (Bias): 1023                                     │
│ * 실제 값: (-1)^S * 1.Mantissa * 2^(Exponent - 1023)         │
└──────────────────────────────────────────────────────────────┘
```

FP64의 가수부는 숨겨진 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)(Hidden [Bit](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/))를 포함해 총 53비트의 연산을 수행한다. 이는 소수점 아래 15번째 자리까지의 미세한 변화도 놓치지 않고 덧셈기에 적립함을 의미한다. 반면 11비트의 지수부는 편향([Bias](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/094_bias/)) 값 1023을 사용하여 매우 작은 소수부터 우주적 크기의 정수까지 [오버플로우](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/095_overflow/) 없이 표현할 수 있게 해준다.

- **📢 섹션 요약 비유**: 이 구조는 가장 큰 우주의 크기(지수부)를 가리키면서도, 그 안에 있는 먼지 알갱이의 무게(가수부)까지 정확하게 소수점 15자리로 적어두는 완벽한 회계 장부와 같다.

---

## Ⅲ. 비교 및 연결

배정밀도는 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)를 얻은 대신, 하드웨어 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)과 연산기 면적이라는 거대한 비용을 지불해야 한다. [단정밀도](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/089_single_precision/)와 배정밀도를 비교하면 시스템 설계의 트레이드오프가 명확해진다.

| 비교 항목 | [단정밀도](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/089_single_precision/) (FP32) | 배정밀도 (FP64) | 아키텍처 판단 포인트 |
| :--- | :--- | :--- | :--- |
| **메모리 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)** | 4 Bytes | 8 Bytes | 메모리 병목 (Memory Bound) 심화 |
| **캐시 (Cache) 효율**| 라인당 16개 적재 | 라인당 8개 적재 | 캐시 미스 (Cache Miss) 증가 |
| **[ALU](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/) 복잡도** | 24x24 곱셈기 | 53x53 곱셈기 | 다이(Die) 면적 약 4배 차지 |
| **적용 분야** | 3D 그래픽스, [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 학습 | 과학 시뮬레이션, 금융 | [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) vs [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) ([Throughput](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)) |

동일한 캐시 메모리에 적재할 수 있는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 양이 절반으로 줄어들며, FPU ([Floating Point](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/087_floating_point/) Unit) 내부의 곱셈기 크기는 기하급수적으로 커진다. 이로 인해 파이프라인의 임계 경로 (Critical Path)가 길어지고 전체 클럭 주파수를 저하시킬 위험이 있다.

- **📢 섹션 요약 비유**: [단정밀도](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/089_single_precision/)가 2단 샌드위치를 빠르고 가볍게 만드는 공정이라면, 배정밀도는 5단 수제 버거를 쓰러지지 않게 정교하게 조립해야 해서 재료비와 시간이 4배 이상 드는 고급 공정과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 배정밀도의 도입은 "오차 누적이 전체 시스템을 파괴하는가?"에 대한 판단에서 출발해야 한다. 무분별한 채택은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하를 부른다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) 및 판단 기준
1. **상쇄 오차 (Catastrophic Cancellation) 방어**: 두 개의 매우 비슷한 큰 수끼리 뺄셈을 할 때 유효숫자가 증발하는 현상. 유체역학이나 기상 예측 시스템에서 이런 연산이 빈번하다면 반드시 FP64를 채택해야 한다.
2. **[GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 및 딥러닝 연산**: [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델 학습이나 3D 게임 좌표계 연산에 `double`을 무분별하게 사용하면 VRAM이 2배로 소모되고, [텐서 코어](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/) ([Tensor Core](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/427_tensor_core/)) 활용이 제한되어 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 폭락한다. 이 경우 FP32나 심지어 FP16, BF16 채택을 우선 고려해야 한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 요구사항 분석 없이 "정밀하면 무조건 좋다"는 마인드로 모든 [부동소수점](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/087_floating_point/) 변수를 `double`로 선언하는 설계.
- 글로벌 타임스탬프(나노초 단위)의 누적 값을 [단정밀도](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/089_single_precision/) 변수로 처리하여 시간이 지남에 따라 증가분이 흡수되어 버리는 아키텍처 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/).

- **📢 섹션 요약 비유**: 나무 조각을 다듬을 때 전기톱([단정밀도](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/089_single_precision/)) 대신 미세한 치과용 드릴(배정밀도)을 고집하면, 디테일은 살릴지언정 밤을 새워도 조각상을 완성하지 못하는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

배정밀도 (FP64)는 유한한 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)로 무한한 실수를 표현해야 하는 컴퓨팅 환경에서 계산 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) ([Integrity](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/))을 보장하는 궁극의 해법이다. 

연산 지연과 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)의 낭비라는 명확한 한계가 존재하지만, 우주 항공, 고에너지 물리학, 양자 화학 분야에서는 대체 불가능한 표준이다. 하드웨어 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 발전과 함께 슈퍼컴퓨터의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 지표인 [FLOPS](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/137_flops/)([Floating Point](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/087_floating_point/) Operations Per Second) 측정의 절대적인 척도로 작용하고 있다. 소프트웨어 엔지니어는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 허용 오차 범위와 시스템의 메모리 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)을 저울질하여 배정밀도의 무게를 견딜 수 있는지 판단해야 한다.

- **📢 섹션 요약 비유**: 배정밀도는 항공모함의 거대한 닻과 같다. 평소에는 무겁고 거추장스럽지만, 태풍이 몰아치는 수치 해석의 바다에서 배가 떠내려가지 않게 버텨주는 유일한 구명줄이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **FP32 ([단정밀도](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/089_single_precision/))** | 배정밀도의 절반 크기로 딥러닝과 그래픽스 등 범용적 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 책임지는 기본 포맷 |
| **[IEEE 754](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/088_ieee_754/)** | 컴퓨터가 [부동소수점](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/087_floating_point/)을 표현하는 방식을 규정한 국제 표준 |
| **상쇄 오차 (Catastrophic Cancellation)** | 비슷한 값의 뺄셈에서 유효숫자가 크게 손실되는 현상으로, FP64가 필요한 주요 원인 |
| **[ALU](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/) ([Arithmetic Logic Unit](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/))** | [부동소수점](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/087_floating_point/) 연산을 실제 수행하는 하드웨어 장치로, FP64 지원 시 면적이 크게 증가 |

### 📈 관련 키워드 및 발전 흐름도

```text
정수 연산 한계 돌파
    │
    ▼
FP32 (단정밀도) · IEEE 754 표준화
    │
    ▼
잘림 오차 (Truncation Error) · 상쇄 오차 (Cancellation)
    │
    ▼
FP64 (배정밀도) · 고성능 컴퓨팅 (HPC) 무결성 확보
    │
    ▼
최신 AI 가속기에서의 혼합 정밀도 (Mixed Precision) 연산
```

이 흐름도는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 표현 방식이 단순성에서 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)로, 그리고 최근에는 목적에 따라 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)를 혼합하여 효율을 극대화하는 방향으로 진화하고 있음을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 배정밀도 상자는 일반 상자보다 두 배나 커서 엄청 무거운 대형 보물 상자예요.
2. 이 상자 안에는 아주 미세한 모래알 하나의 무게까지 절대 잊어버리지 않고 다 적어둘 수 있는 마법의 장부가 있어요.
3. 숫자를 우주 끝까지 꼼꼼하게 계산해야 하는 똑똑한 과학자들만 이 무겁고 거대한 상자를 들고 다닌답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 90 / 803

← **이전**: [89. 단정밀도 (Single Precision, FP32)](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/089_single_precision/)
**다음**: [91. 반정밀도 (Half Precision, FP16)](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/091_half_precision/) →

---
