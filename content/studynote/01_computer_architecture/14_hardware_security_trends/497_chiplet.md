---
title: "497. 칩렛 (Chiplet) 아키텍처"
date: "2026-03-20"
tags:
  - "studynote-computer-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 칩렛 (Chiplet) 아키텍처는 거대한 단일 다이 대신 기능별로 나눈 여러 다이를 하나의 패키지 안에서 시스템처럼 묶는 설계 방식이다.
> 2. **가치**: 연산, 입출력, 캐시를 서로 다른 공정과 면적으로 분리해 수율과 원가를 개선하고, 같은 부품 조합으로 다양한 제품군을 빠르게 확장할 수 있다.
> 3. **판단 포인트**: 성공 여부는 "쪼갰는가"가 아니라 D2D (Die-to-Die) 인터커넥트, 패키징, [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), 열 설계를 얼마나 정교하게 통합했는가에 달려 있다.

---

## Ⅰ. 개요 및 필요성

칩렛 아키텍처는 중앙처리장치 (CPU, Central Processing Unit), 그래픽 처리장치 ([GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/), [Graphics Processing Unit](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)), 입출력 (I/O, Input/Output), 캐시 같은 블록을 하나의 거대한 실리콘 다이로 만들지 않고, 여러 개의 작은 다이로 분리해 한 패키지 안에서 결합하는 구조다. [반도체](/studynote/01_computer_architecture/01_basic_electronics_logic/009_semiconductor/) 공정이 5nm, 3nm로 갈수록 웨이퍼 비용과 [결함](/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 민감도가 커지면서, "모든 기능을 최신 공정 한 장에 담는 방식"은 수율과 개발비 측면에서 빠르게 불리해졌다. 특히 고속 연산 블록은 최신 공정이 필요하지만, 아날로그 I/O나 메모리 PHY (Physical Layer)는 굳이 같은 고가 공정을 쓸 이유가 적다.

즉 칩렛은 단순 분할이 아니라 <strong>공정 미스매치와 대형 다이 수율 문제를 동시에 푸는 <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>이다. 같은 면적이라도 거대한 단일 다이는 [결함](/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 하나로 전체가 폐기되지만, 여러 작은 다이는 불량 난 다이만 걸러 조립할 수 있다. 여기에 제품 파생도 쉬워져 같은 I/O 다이에 연산 칩렛 수만 바꿔 데스크톱, 서버, 가속기 계열을 빠르게 만들 수 있다.

```text
+----------------------------------------------------------------------------+
| 왜 단일 대형 다이에서 칩렛으로 이동하는가                                   |
+-------------------------------+--------------------------------------------+
| Monolithic Die                | Chiplet Package                            |
| [Core + Cache + I/O + PHY]    | [Compute][Compute][I/O][Cache]            |
|                               |                                            |
| 결함 1개 => 전체 폐기         | 결함 1개 => 해당 다이만 교체               |
| 전부 동일 공정 사용           | 연산/입출력/아날로그를 공정별 분리          |
| 제품 파생 시 재설계 범위 큼   | 조합 변경으로 제품군 확장 용이             |
+-------------------------------+--------------------------------------------+
```

이 그림의 핵심은 칩렛이 "더 작은 칩"이 아니라 <strong>패키지 수준에서 재조립 가능한 <a href="/studynote/01_computer_architecture/01_basic_electronics_logic/009_semiconductor/">반도체</a> 구조</strong>라는 점이다. 설계 단위가 다이에서 패키지로 올라가면서, [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)뿐 아니라 제조와 [공급망](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)까지 함께 바뀐다.

- **📢 섹션 요약 비유**: 칩렛은 통짜 가구를 한 번에 만드는 대신, 상판·서랍·다리를 따로 만들어 조립하는 방식과 같다. 한 부품이 불량이어도 전체를 버리지 않아도 되고, 방 크기에 맞춰 조합을 바꾸기 쉽다.

---

## Ⅱ. 아키텍처 및 핵심 원리

칩렛 구조의 핵심은 기능 분할과 패키지 내부 연결이다. 보통 연산 칩렛은 최신 미세 공정으로 만들고, I/O 다이와 아날로그 블록은 상대적으로 성숙한 공정에 배치한다. 이렇게 만든 다이들은 패키지 기판, 실리콘 인터포저 (Silicon Interposer), [브리지](/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/) 구조 위에서 D2D 인터커넥트로 묶인다. 이때 중요한 것은 단순 연결 여부가 아니라 <strong>패키지 내부에서도 <a href="/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/">캐시 일관성</a>, 메모리 접근, 전력 전달이 시스템처럼 유지되는가</strong>다.

| 구성 요소 | 역할 | 설계 포인트 |
| :-- | :-- | :-- |
| 연산 칩렛 | CPU·[GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)·[인공지능](/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) 코어 수행 | 최신 공정, [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)/W 최적화 |
| I/O 다이 | 메모리 컨트롤러, [PCIe](/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) ([Peripheral Component Interconnect](/studynote/01_computer_architecture/09_system_bus_interconnects/355_pci/) Express), [CXL](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) ([Compute Express Link](/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/)), PHY 집적 | 성숙 공정 활용, 면적 대비 효율 |
| 캐시/가속 타일 | 대용량 캐시 또는 전용 기능 추가 | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간과 열 밀도 균형 |
| D2D 인터커넥트 | 칩렛 간 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·제어 전송 | [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/), hop [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 전력/[bit](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) |
| 패키지 구조 | 기판, 인터포저, [브리지](/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/), 적층 통합 | 배선 밀도, 수율, 조립 비용 |

칩렛 설계는 보통 세 단계로 판단한다. 첫째, 어떤 블록을 다이 경계 밖으로 뺄지 정한다. 둘째, 칩렛 간 트래픽이 얼마나 많은지 계산해 패키지 배선과 프로토콜을 고른다. 셋째, 조립 전 각 다이를 KGD (Known Good Die) 수준으로 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)해 패키지 수율 손실을 줄인다.

```text
+----------------------------------------------------------------------------+
| 칩렛 패키지의 전형적 데이터 경로                                            |
+----------------------------------------------------------------------------+
| [Compute Chiplet A] --+                                                     |
| [Compute Chiplet B] --+-- Coherent D2D Fabric -- [I/O Die] -- DDR / CXL    |
| [Cache / Accel Tile] -+                               |                     |
|                                                       +---- PCIe / Network  |
+----------------------------------------------------------------------------+
| 핵심 과제: 대역폭 확보 · 지연 최소화 · KGD 확보 · 전력 전달 · 열 분산       |
+----------------------------------------------------------------------------+
```

최근에는 [UCIe](/studynote/01_computer_architecture/12_accelerators_ai_hardware/443_ucie/) (Universal Chiplet Interconnect Express) 같은 표준이 등장해, 서로 다른 회사의 칩렛을 공통 규격으로 묶으려는 흐름도 강해지고 있다. 다만 표준이 있다고 해서 바로 호환되는 것은 아니다. 물리층, 패키지, 전력, 보안, 관리 모델이 같이 맞아야 진짜 생태계가 된다.

- **📢 섹션 요약 비유**: 칩렛은 레고 블록이 아니라 배관과 전기선까지 연결되는 모듈식 건물이다. 블록을 쌓는 것보다, 내부 통로와 배선을 얼마나 잘 설계했는지가 완성도를 좌우한다.

---

## Ⅲ. 비교 및 연결

칩렛은 오래전 MCM (Multi-Chip [Module](/studynote/04_software_engineering/04_testing_quality/192_module_independence/))과 닮아 보이지만 성격이 다르다. MCM은 여러 칩을 한 패키지에 모으는 데 초점이 있었다면, 현대 칩렛은 미세한 D2D 인터커넥트와 재사용 가능한 타일 설계, 표준화된 조합을 지향한다. 또 단일 다이와 비교할 때 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 무조건 좋아지는 것도 아니다. 패키지 내부 hop이 늘어나면 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 전력 소모가 증가할 수 있기 때문이다.

| 항목 | 단일 다이 (Monolithic) | 칩렛 | 전통적 MCM |
| :-- | :-- | :-- | :-- |
| 통합 방식 | 하나의 거대한 다이 | 기능별 다이 분리 후 패키지 통합 | 서로 다른 칩을 같은 패키지에 배치 |
| 장점 | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 최소화, 구조 단순 | 수율·원가·확장성 우수 | 이기종 칩 결합 쉬움 |
| 약점 | 대형 다이 수율과 비용 부담 | 패키지 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)·[검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 복잡도 | [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)·[일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 한계 |
| 잘 맞는 영역 | 소형 고집적 시스템 온 칩 ([SoC](/studynote/01_computer_architecture/03_architecture_basics_performance/131_soc/), [System on Chip](/studynote/01_computer_architecture/03_architecture_basics_performance/131_soc/)) | 서버 CPU, [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 가속기, 고성능 컴퓨팅 ([HPC](/studynote/01_computer_architecture/15_advanced_topics/548_automotive_hpc/), [High Performance Computing](/studynote/06_ict_convergence/03_cloud_infrastructure/226_hpc_supercomputing_infrastructure/)) | 보드 집적 대체, 특수 시스템 |

칩렛은 [HBM](/studynote/01_computer_architecture/14_hardware_security_trends/495_hbm/) ([High Bandwidth Memory](/studynote/01_computer_architecture/14_hardware_security_trends/495_hbm/)), [TSV](/studynote/01_computer_architecture/14_hardware_security_trends/496_tsv/) (Through-Silicon Via), 2.5D 패키징과도 강하게 연결된다. 예를 들어 [인공지능](/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) ([AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/), [Artificial Intelligence](/studynote/10_ai/01_ai_basics/001_artificial_intelligence/)) 가속기는 연산 타일을 여러 칩렛으로 나누고, HBM을 인터포저 위에 함께 올려 패키지 단위에서 하나의 가속기처럼 동작시킨다. 즉 칩렛은 단독 기술이 아니라 <strong>고대역폭 메모리, 패키징, 인터커넥트 표준이 함께 묶이는 상위 설계 개념</strong>이다.

또한 칩렛은 조직 운영 측면에서도 의미가 크다. 공정 노드 변화가 빨라질수록 모든 블록을 한꺼번에 재검증하기보다, [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)된 I/O 다이를 유지하고 연산 칩렛만 갱신하는 방식이 훨씬 빠르다. 그래서 칩렛은 아키텍처 혁신이면서 동시에 제품 개발 프로세스 혁신이기도 하다.

- **📢 섹션 요약 비유**: 단일 다이는 원룸형 집, 칩렛은 모듈형 주택에 가깝다. 원룸은 동선이 짧지만 확장이 어렵고, 모듈형 주택은 방을 늘리기 쉽지만 연결 통로 설계가 중요하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 칩렛은 서버 CPU, [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 가속기, 네트워크 [ASIC](/studynote/01_computer_architecture/01_basic_electronics_logic/070_asic/) (Application-Specific Integrated Circuit)처럼 규모가 크고 제품 파생이 잦은 영역에서 특히 유리하다. 예를 들어 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)센터용 프로세서는 같은 I/O 다이를 유지한 채 연산 칩렛 수만 2개, 4개, 8개로 바꿔 제품군을 늘릴 수 있다. 반대로 모바일 SoC처럼 초저전력, 초소형, 초저지연이 절대적인 제품은 패키지 복잡도보다 단일 다이의 이점이 더 클 수 있다.

### 적용 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. **분할 타당성**: 어떤 블록을 다이 경계 밖으로 빼도 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 손실이 허용되는가?
2. **트래픽 특성**: 칩렛 간 통신량이 많아 패키지 인터커넥트가 병목이 되지 않는가?
3. <strong>열 <a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a></strong>: 고발열 연산 칩렛이 한곳에 몰리지 않도록 배치 가능한가?
4. <strong>수율 <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>: KGD 확보, 조립 후 테스트, 불량 분석 체계가 준비되어 있는가?
5. **생태계 선택**: 사내 독자 링크를 쓸지, [UCIe](/studynote/01_computer_architecture/12_accelerators_ai_hardware/443_ucie/) 같은 표준 기반으로 갈지 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 있는가?

### 피해야 할 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 다이를 너무 잘게 쪼개 패키지 내부 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 조립 비용만 키우는 설계
- 패키지 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 계산 없이 "칩렛이면 확장 가능"하다고 가정하는 접근
- 칩렛 재사용만 강조하고 전력 전달·클럭 동기·보안 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 뒤로 미루는 운영

기술사 답안에서는 칩렛의 장점만 적기보다, **수율 향상과 공정 분리의 이득** 그리고 <strong>인터커넥트·패키징·<a href="/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a> 복잡도의 비용</strong>을 함께 써야 한다. 그래야 칩렛을 유행어가 아니라 실제 설계 선택지로 이해하고 있다는 점이 드러난다.

- **📢 섹션 요약 비유**: 칩렛 도입은 방을 더 만드는 일이 아니라, 복도·전기 배선·배관까지 새로 설계하는 증축 공사와 같다. 방 수만 늘리면 끝나는 문제가 아니다.

---

## Ⅴ. 기대효과 및 결론

칩렛 아키텍처가 성숙하면 [반도체](/studynote/01_computer_architecture/01_basic_electronics_logic/009_semiconductor/) 산업은 더 빠른 제품 파생, 공정 혼합 최적화, 대형 다이 수율 개선이라는 세 가지 이점을 크게 얻는다. 특히 AI와 HPC처럼 한 세대 안에서도 연산, 메모리, I/O 요구가 빠르게 바뀌는 분야에서는 칩렛 기반 설계가 민첩성을 높인다. 이는 "더 큰 칩을 만든다"는 경쟁에서 "더 잘 조합된 패키지를 만든다"는 경쟁으로 무게중심이 이동하고 있음을 뜻한다.

물론 한계도 분명하다. 패키지 비용 증가, 인터커넥트 전력, 열 집중, 다이 간 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 유지, [공급망](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/) 복잡도는 계속 부담이다. 앞으로는 [UCIe](/studynote/01_computer_architecture/12_accelerators_ai_hardware/443_ucie/) 기반 생태계 확대, 3D 칩렛 적층, 광 인터커넥트, 백사이드 전력 전달 같은 기술이 이런 약점을 줄여 나갈 가능성이 크다.

결론적으로 칩렛은 "칩을 여러 개 붙인다"는 수준이 아니라, [반도체](/studynote/01_computer_architecture/01_basic_electronics_logic/009_semiconductor/) 설계의 기본 단위를 다이에서 패키지로 끌어올린 변화다. 따라서 칩렛을 이해할 때는 수율 개선만 외우지 말고, <strong>패키지 내부가 하나의 시스템 버스처럼 동작하도록 만드는 기술</strong>로 기억하는 것이 정확하다.

- **📢 섹션 요약 비유**: 칩렛은 여러 부품을 상자에 담는 방식이 아니라, 작은 엔진과 변속기와 배터리를 조합해 한 대의 자동차를 만드는 플랫폼 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)과 같다. 조합이 유연해지는 대신, 연결부 설계가 곧 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| 단일 다이 (Monolithic Die) | 칩렛이 대체하려는 기존 통합 방식으로, 대형화될수록 수율 부담이 커진다. |
| D2D (Die-to-Die) 인터커넥트 | 칩렛 간 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)과 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 결정하는 핵심 연결 계층이다. |
| KGD (Known Good Die) | 패키지 조립 전에 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)된 다이를 확보해 수율 손실을 줄이는 개념이다. |
| [UCIe](/studynote/01_computer_architecture/12_accelerators_ai_hardware/443_ucie/) (Universal Chiplet Interconnect Express) | 칩렛 생태계 표준화를 노리는 대표 인터커넥트 규격이다. |
| 2.5D / 3D 패키징 | 칩렛을 고밀도로 통합하는 패키지 기술 기반이다. |
| [HBM](/studynote/01_computer_architecture/14_hardware_security_trends/495_hbm/) ([High Bandwidth Memory](/studynote/01_computer_architecture/14_hardware_security_trends/495_hbm/)) | 칩렛 기반 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 가속기와 자주 결합되는 초대역폭 메모리다. |

### 📈 관련 키워드 및 발전 흐름도

```text
단일 대형 다이 중심 설계
        |
        v
수율 악화 · 공정 비용 상승 · 레티클 한계 압박
        |
        v
MCM (Multi-Chip Module) 재조명
        |
        v
칩렛 아키텍처 + 고속 D2D 인터커넥트
        |
        +---------> UCIe 표준화
        +---------> 2.5D / 3D 패키징
        +---------> HBM 결합형 AI / HPC 패키지
```

이 흐름은 대형 단일 다이의 한계를 해결하려는 시도가 패키지 수준 통합, 표준화, 이기종 집적으로 확장되는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 칩렛은 큰 장난감을 한 번에 만드는 대신, 머리·몸통·팔을 따로 만들어 조립하는 방법이에요.
2. 그래서 팔 하나가 잘못 만들어져도 전체를 버리지 않고, 필요한 만큼만 더 붙일 수 있어요.
3. 대신 부품끼리 빨리 이야기하게 만드는 연결 통로를 아주 잘 만들어야 진짜 좋은 장난감이 돼요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 497 / 803

<- **이전**: [496. TSV (Through-Silicon Via, 실리콘 관통 전극)](/studynote/01_computer_architecture/14_hardware_security_trends/496_tsv/)
**다음**: [498. 2.5D 및 3D 패키징 기술](/studynote/01_computer_architecture/14_hardware_security_trends/498_2d_3d_packaging/) ->

---
