---
title: "610. 보안 해시 함수 회로 (SHA-3 / Keccak)"
date: "2026-05-08"
tags:
  - "studynote-computer-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [SHA-3](/studynote/09_security/02_crypto/101_sha_3/) (Secure Hash [Algorithm](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 3) 하드웨어는 케칵 ([Keccak](/studynote/09_security/02_crypto/101_sha_3/))의 스펀지 구조를 1600비트 상태 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)와 24라운드 순열 회로로 구현해, 메시지를 흡수하고 짜내는 과정을 고정 지연으로 수행하는 전용 해시 엔진이다.
> 2. **가치**: SHA-2 (Secure Hash [Algorithm](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 2) 계열과 달리 긴 캐리 전파 가산기보다 배타적 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)합 (Exclusive OR, XOR), [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)곱 (AND), [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 회전이 중심이어서, 필드 프로그래머블 게이트 어레이 ([Field-Programmable Gate Array](/studynote/01_computer_architecture/15_advanced_topics/606_dynamic_partial_reconfiguration/), [FPGA](/studynote/01_computer_architecture/15_advanced_topics/606_dynamic_partial_reconfiguration/))와 애플리케이션 특화 집적회로 (Application-Specific Integrated Circuit, [ASIC](/studynote/01_computer_architecture/01_basic_electronics_logic/070_asic/))에서 면적 대비 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)이 높다.
> 3. **판단 포인트**: 반복형, 언롤드, 파이프라인 구조 중 무엇을 고를지는 순열 코어 자체보다도 입출력 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/), [패딩](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/) 처리, 사이드채널 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/), 목표 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)(Gbps)을 함께 맞출 수 있는지에 달려 있다.

---

## Ⅰ. 개요 및 필요성

[SHA-3](/studynote/09_security/02_crypto/101_sha_3/) 하드웨어는 메시지 [무결성](/studynote/09_security/01_intro_principles/003_integrity/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)과 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)용 해시를 전용 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)로 처리하는 보안 가속기다. 미국 국립표준기술연구소 (National Institute of Standards and Technology, NIST)는 SHA-2 이후의 구조적 다양성을 확보하기 위해 공개 경쟁을 진행했고, 그 결과 Keccak이 [SHA-3](/studynote/09_security/02_crypto/101_sha_3/) 표준으로 채택되었다. 핵심은 머클-담고르드 (Merkle-Damgård)형 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 함수가 아니라, 하나의 큰 상태를 계속 섞는 스펀지 구조라는 점이다.

왜 전용 회로가 필요할까. 보안 [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/), 저장장치, 네트워크 장비, [블록체인](/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 노드, 포스트 양자 암호 ([Post-Quantum Cryptography](/studynote/14_data_engineering/04_mlops/183_post_quantum_cryptography_key_transition/), [PQC](/studynote/12_it_management/05_security_compliance/992_quantum_computing_pqc_transition/)) 프로토콜은 짧은 메시지부터 긴 스트림까지 반복적으로 해시해야 한다. 범용 중앙처리장치 (Central Processing Unit, CPU)도 해시를 계산할 수는 있지만, 고속 링크에서 패킷마다 해시를 붙이거나 SHAKE 기반 키 파생을 대량 수행할 때는 지연과 전력 예측성이 떨어진다.

특히 SHA-3는 같은 순열 코어를 공유한 채 SHA3-224/256/384/512와 SHAKE 같은 확장 출력 함수 (eXtendable-Output Function, XOF) 계열을 함께 지원할 수 있어, 하드웨어 재사용성이 높다. 즉 한 번 잘 만든 코어가 여러 보안 기능의 공통 엔진이 된다.

- **📢 섹션 요약 비유**: [SHA-3](/studynote/09_security/02_crypto/101_sha_3/) 하드웨어는 손으로 반죽을 치대는 제빵사가 아니라, 같은 반죽통을 정확한 힘과 횟수로 반복 회전시키는 자동 반죽기와 같다. 많이 만들수록 전용 기계의 가치가 커진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

SHA-3의 내부 상태는 1600비트이며, `rate + capacity = 1600` 관계를 따른다. 예를 들어 SHA3-256은 rate가 1088비트, capacity가 512비트다. 메시지는 rate 부분에 XOR로 흡수되고, 그 뒤 24라운드의 [Keccak](/studynote/09_security/02_crypto/101_sha_3/)-f[1600] 순열이 상태 전체를 섞는다. 필요한 길이만큼 상태의 앞부분을 다시 읽어 해시를 짜내는데, 출력이 더 필요하면 순열을 한 번 더 돌리면 된다.

아래 그림은 스펀지 구조와 순열 코어가 어떻게 연결되는지 보여 준다.

```text
+----------------------------------------------------------------------------+
| msg block -> pad10*1 -> XOR into rate bits -> state[1600]                 |
|                                              |                             |
|                                              v                             |
|                    theta -> rho -> pi -> chi -> iota   (24 rounds)        |
|                                              |                             |
|                                              +--> squeeze r bits -> digest |
+----------------------------------------------------------------------------+
```

| 단계 | 역할 | 하드웨어 관점의 포인트 |
| :--- | :--- | :--- |
| Theta | 열 패리티를 이용한 확산 | XOR 트리 중심이라 배선과 팬아웃 관리가 중요하다 |
| Rho | 각 레인의 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 회전 | 회전 상수가 고정되어 배선 최적화에 유리하다 |
| [Pi](/studynote/12_it_management/01_governance_strategy/805_process_innovation/) | 레인 위치 재배치 | 실질적으로 permutation wiring이라 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) 깊이가 거의 없다 |
| Chi | 비선형 혼합 | `A XOR ((NOT B) AND C)`로 임계 경로가 되기 쉽다 |
| Iota | 라운드 상수 주입 | 작은 상수 XOR로 대칭성을 깨뜨린다 |

하드웨어 친화성이 높은 이유는 명확하다. Rho와 Pi는 거의 배선 재배열이고, Theta와 Chi도 긴 캐리 체인을 요구하지 않는다. 그래서 동일한 주파수 조건에서 SHA-2처럼 가산기 기반인 구조보다 타이밍 수렴이 쉬운 편이다. 다만 Chi 단계의 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) 깊이와 1600비트 상태 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)의 배치가 성능을 좌우하므로, 결국 좋은 [SHA-3](/studynote/09_security/02_crypto/101_sha_3/) 코어는 "수학"보다 "배선과 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)링"이 성패를 가른다.

- **📢 섹션 요약 비유**: [SHA-3](/studynote/09_security/02_crypto/101_sha_3/) 코어는 세탁기 안 빨래를 숫자로 바꿔 섞는 장치와 같다. 빨래를 집어넣는 입구(rate)와 세탁통([state](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/)), 그리고 세탁 모드 24단계가 정확히 맞물려야 깨끗한 결과가 나온다.

---

## Ⅲ. 비교 및 연결

[SHA-3](/studynote/09_security/02_crypto/101_sha_3/) 하드웨어를 볼 때 가장 자주 비교되는 대상은 SHA-2다. 두 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 모두 해시를 만들지만, 하드웨어가 느끼는 부담은 꽤 다르다.

| 항목 | SHA-2 계열 | [SHA-3](/studynote/09_security/02_crypto/101_sha_3/) / [Keccak](/studynote/09_security/02_crypto/101_sha_3/) |
| :--- | :--- | :--- |
| 기본 구조 | [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 함수 반복 | 스펀지 구조 + 순열 |
| 주된 연산 | 덧셈, XOR, 시프트 | XOR, AND, NOT, rotate, permutation |
| 임계 경로 성격 | 캐리 전파 지연이 길다 | Chi 단계와 광폭 배선이 핵심이다 |
| 출력 확장성 | 고정 길이 중심 | SHAKE, cSHAKE, KMAC으로 확장 쉬움 |
| 하드웨어 재사용성 | [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)별 변형 차이 큼 | 동일한 1600비트 코어 재사용성이 높음 |

SHA-3는 해시 하나로 끝나지 않는다. 같은 [Keccak](/studynote/09_security/02_crypto/101_sha_3/) 순열을 기반으로 SHAKE, cSHAKE (customizable SHAKE), KMAC ([Keccak](/studynote/09_security/02_crypto/101_sha_3/) [Message Authentication Code](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)) 같은 확장 가능 출력 함수와 메시지 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 코드로 이어진다. 따라서 시스템 온 칩 (System-on-Chip, [SoC](/studynote/01_computer_architecture/03_architecture_basics_performance/131_soc/)) 입장에서는 "하나의 큰 순열 엔진 + 모드 제어" 구조로 여러 보안 기능을 묶을 수 있다.

구현 구조도 비교 대상이다. 반복형(iterative)은 1개의 라운드 블록을 24번 재사용해 면적이 작고, 언롤드(unrolled)는 여러 라운드를 한 번에 펼쳐 지연을 줄이며, 완전 파이프라인은 각 라운드 사이에 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)를 넣어 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 극대화한다. 결국 보안 가속기는 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 비교와 아키텍처 비교가 함께 이뤄져야 전체 그림이 보인다.

- **📢 섹션 요약 비유**: SHA-2가 복잡한 덧셈이 많은 계산기 공장이라면, SHA-3는 넓은 반죽통을 계속 뒤섞는 믹서 공장에 가깝다. 공장이 다르면 병목도 다르게 생긴다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 가장 먼저 정할 것은 목표 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)과 전력 예산이다. 반복형 구조라면 `Throughput ≈ rate × fclk / cycles_per_block`으로 대략 계산할 수 있다. 예를 들어 SHA3-256에서 rate가 1088비트이고, 24사이클 반복형 코어가 500MHz로 동작하면 이론 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)은 약 22.7Gbps 수준이다. 하지만 실제 시스템에서는 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/), [패딩](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/), 출력 포맷, backpressure 때문에 이 수치가 그대로 나오지 않는다.

### 적용 판단 포인트

1. **초소형 기기**: 면적과 전력이 우선이면 반복형 또는 부분 언롤드 구조가 유리하다.
2. **고속 패킷 처리**: 10GbE 이상 네트워크라면 다중 버퍼, [직접 메모리 접근](/studynote/02_operating_system/08_storage_and_io_systems/450_dma_direct_memory_access/) ([Direct Memory Access](/studynote/01_computer_architecture/08_io_storage_systems/318_dma/), [DMA](/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/)), 파이프라인 구조를 함께 설계해야 한다.
3. <strong>보안 <a href="/studynote/04_software_engineering/04_testing_quality/192_module_independence/">모듈</a></strong>: 사이드채널 저항성이 중요하면 마스킹, 듀얼 레일, 클록 균형화처럼 회로 수준 방어가 필요하다.
4. <strong><a href="/studynote/12_it_management/05_security_compliance/992_quantum_computing_pqc_transition/">PQC</a> 연동</strong>: SHAKE 기반 키 확장이 많다면 고정 길이 해시보다 확장 출력 최적화가 더 중요하다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

- [패딩](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/) 규칙 `pad10*1`과 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 구분 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 표준대로 처리하는가?
- 5×5×64 레인 순서와 엔디언 차이를 소프트웨어 모델과 일치시켰는가?
- 테스트 벡터(KAT)뿐 아니라 긴 메시지 스트림과 SHAKE 출력 길이 변화도 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)했는가?
- 코어 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)보다 입출력 경로가 느려 전체 가속기가 병목이 되지 않는가?

### 피해야 할 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- CPU [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 쓰기만으로 코어를 먹여 살리려는 구조
- [Pi](/studynote/12_it_management/01_governance_strategy/805_process_innovation/) 단계를 실제 조합 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)로 구현해 배선 장점을 잃는 구조
- 암호 [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/)인데도 전력 파형 노출을 고려하지 않는 구조

- **📢 섹션 요약 비유**: [SHA-3](/studynote/09_security/02_crypto/101_sha_3/) 가속기 설계는 고속도로를 까는 일과 같다. 톨게이트(순열)만 넓히면 끝이 아니라, 진입로와 출구와 교통량까지 같이 맞춰야 진짜 속도가 난다.

---

## Ⅴ. 기대효과 및 결론

잘 설계된 [SHA-3](/studynote/09_security/02_crypto/101_sha_3/) 하드웨어는 보안 기능을 "느린 소프트웨어 루틴"에서 "항상 켜져 있는 인프라"로 바꿔 준다. 저장장치 [무결성](/studynote/09_security/01_intro_principles/003_integrity/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), 네트워크 패킷 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), [펌웨어](/studynote/02_operating_system/01_overview_architecture/032_firmware/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), 키 파생이 모두 더 짧은 지연과 더 낮은 에너지로 수행된다. 또한 동일 코어를 SHAKE·KMAC까지 확장할 수 있어, 보안 블록의 재사용성이 커진다.

한계도 분명하다. 1600비트 상태 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)는 소형 칩에 부담이 될 수 있고, 파이프라인을 깊게 넣을수록 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 지연과 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 전력이 늘어난다. 사이드채널 대응을 추가하면 면적과 주파수 이득의 일부를 포기해야 한다.

결국 [SHA-3](/studynote/09_security/02_crypto/101_sha_3/) 하드웨어의 핵심은 "복잡한 해시 함수를 빠르게 계산한다"가 아니라, <strong>동일한 순열 코어를 다양한 보안 모드로 안전하고 예측 가능하게 서비스한다</strong>는 데 있다. 이 관점을 잡으면 왜 Keccak이 현대 보안 SoC의 공용 엔진으로 주목받는지 자연스럽게 이해된다.

- **📢 섹션 요약 비유**: 좋은 [SHA-3](/studynote/09_security/02_crypto/101_sha_3/) 코어는 만능 믹서기와 같다. 반죽, 소스, 크림을 각각 손으로 만들던 주방을 하나의 강력한 공용 장비가 안정적으로 떠받친다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 스펀지 구조 (Sponge Construction) | 메시지를 흡수하고 출력 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 짜내는 SHA-3의 기본 동작 모델이다. |
| [Keccak](/studynote/09_security/02_crypto/101_sha_3/)-f[1600] | [SHA-3](/studynote/09_security/02_crypto/101_sha_3/) 계열이 공통으로 재사용하는 1600비트 순열 코어다. |
| SHAKE | 같은 코어를 확장 출력 함수로 재활용하는 대표 사례다. |
| [DMA](/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) ([Direct Memory Access](/studynote/01_computer_architecture/08_io_storage_systems/318_dma/)) | 코어가 고속이어도 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공급이 막히면 성능이 나오지 않음을 보여 주는 주변 구조다. |
| 사이드채널 방어 (Side-Channel Countermeasure) | 전력·전자기 누설을 줄여 보안 가속기를 실제 제품 수준으로 끌어올린다. |
| KMAC | [Keccak](/studynote/09_security/02_crypto/101_sha_3/) 순열을 기반으로 한 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 기능으로, 해시 코어 재사용성을 잘 보여 준다. |

### 📈 관련 키워드 및 발전 흐름도

```text
Merkle-Damgård 해시 시대
        |
        v
Keccak 스펀지 구조 제안
        |
        v
SHA-3 표준화
        |
        v
SHA3-256/512 · SHAKE · KMAC 공용 코어
        |
        v
언롤드 · 파이프라인 보안 가속기
        |
        v
PQC 대응형 보안 SoC
```

이 흐름은 해시 회로가 단순 [무결성](/studynote/09_security/01_intro_principles/003_integrity/) 블록에서, 다양한 보안 모드를 품는 공용 순열 엔진으로 발전해 온 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [SHA-3](/studynote/09_security/02_crypto/101_sha_3/) 하드웨어는 편지를 아주 복잡하게 섞어 아무도 못 알아보게 만드는 마법 믹서기예요.
2. 한 번 잘 만든 믹서기는 짧은 편지도, 긴 편지도, 여러 보안 일도 똑같이 빠르게 처리해요.
3. 그래서 컴퓨터는 중요한 비밀을 더 빨리, 더 안전하게 지킬 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 610 / 803

<- **이전**: [609. 단일 이벤트 래치업 (SEL, Single Event Latchup)](/studynote/01_computer_architecture/15_advanced_topics/609_single_event_latchup/)
**다음**: [611. 분산 산술 (Distributed Arithmetic) 매크로](/studynote/01_computer_architecture/15_advanced_topics/611_distributed_arithmetic/) ->

---
