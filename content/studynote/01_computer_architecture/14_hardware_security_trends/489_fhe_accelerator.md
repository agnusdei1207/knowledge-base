---
title: 489. 동형 암호 가속기 (FHE Accelerator)
date: '2026-03-20'
tags:
- studynote-computer-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[1019_homomorphic_encryption|동형 암호]] 가속기 ([[617_fhe_modular_multiplier|FHE]] Accelerator)는 [[617_fhe_modular_multiplier|완전 동형 암호]] ([[617_fhe_modular_multiplier|FHE]], Fully [[1019_homomorphic_encryption|Homomorphic Encryption]])의 거대한 [[195_polynomial_generator_crc|다항식]] 연산과 [[120_concept|부트스트래핑]]을 전용 하드웨어로 줄여, 복호화 없는 계산을 실용 구간으로 끌어오는 장치다.
> 2. **가치**: 저장 중 [[001_dikw_pyramid|데이터]]와 전송 중 [[001_dikw_pyramid|데이터]]뿐 아니라 **사용 중 [[001_dikw_pyramid|데이터]] ([[001_dikw_pyramid|Data]] [[694_confidential_computing_data_in_use|in Use]])** 까지 [[571_protection_vs_security|보호]]할 수 있어, 클라우드가 평문을 보지 못하는 프라이버시 분석과 [[231_ai_turing_test|인공지능]] 추론을 가능하게 한다.
> 3. **판단 포인트**: FHE는 보안은 매우 강하지만 지연시간과 메모리 비용이 크므로, 연산 깊이·[[120_concept|부트스트래핑]] 빈도·메모리 [[140_bandwidth|대역폭]]을 감당할 수 있는 워크로드에만 가속기를 붙여야 효과가 난다.

---

## Ⅰ. 개요 및 필요성

[[1019_homomorphic_encryption|동형 암호]] 가속기 ([[617_fhe_modular_multiplier|FHE]] Accelerator)는 [[617_fhe_modular_multiplier|완전 동형 암호]] ([[617_fhe_modular_multiplier|FHE]], Fully [[1019_homomorphic_encryption|Homomorphic Encryption]]) 연산에서 가장 무거운 [[195_polynomial_generator_crc|다항식]] 곱셈, 키 스위칭, [[120_concept|부트스트래핑]]을 전용 회로로 처리하는 하드웨어다. 일반 암호화는 저장할 때와 보낼 때만 [[571_protection_vs_security|보호]]하고, 계산할 때는 결국 평문으로 풀어야 했다. 반면 FHE는 암호문 상태 그대로 덧셈·곱셈을 수행하므로, 클라우드 운영자조차 [[001_dikw_pyramid|데이터]] 의미를 모른 채 결과만 계산할 수 있다.

문제는 계산 비용이다. FHE는 격자 기반 [[195_polynomial_generator_crc|다항식]] 연산과 노이즈 관리를 동반하므로, 같은 연산이라도 평문 대비 여러 자릿수 큰 오버헤드가 생긴다. 특히 클라우드 [[231_ai_turing_test|인공지능]] 추론, 금융 통계, 의료 분석처럼 [[001_dikw_pyramid|데이터]] 민감도는 높지만 [[139_throughput|처리량]]도 요구되는 환경에서는 중앙처리장치 (CPU, Central Processing Unit)만으로 [[090_service_kubernetes_network_load_balancing|서비스]] 수준 목표를 맞추기 어렵다. 그래서 FHE의 실용화는 [[001_algorithm_definition|알고리즘]] 개선과 함께, 그 수학 구조에 맞춘 가속 하드웨어의 등장을 필요로 했다.

아래 그림은 FHE가 왜 "계산은 맡기되 비밀은 맡기지 않는" 구조로 불리는지 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ FHE trust boundary: server computes, client keeps the secret key        │
├──────────────────────────────────────────────────────────────────────────┤
│ Client                                                                   │
│   plaintext ──encrypt──▶ ciphertext                                       │
│                              │                                             │
│                              ▼                                             │
│                     Cloud FHE Accelerator                                  │
│                     ├─ add / multiply / rotate                             │
│                     └─ bootstrap when noise grows                          │
│                              │                                             │
│                              ▼                                             │
│                 ciphertext result ──decrypt──▶ plaintext result            │
│                                                                            │
│ Server never receives the secret key or plaintext                          │
└──────────────────────────────────────────────────────────────────────────┘
```

이 그림의 핵심은 서버가 계산은 수행하지만 비밀키와 평문은 끝까지 클라이언트 쪽에 남는다는 점이다. 즉 [[617_fhe_modular_multiplier|FHE]] 가속기는 단순한 암호 연산 카드가 아니라, **평문 노출 없는 클라우드 계산**을 가능하게 만드는 [[001_dikw_pyramid|데이터]] 경계 장치다.

- **📢 섹션 요약 비유**: [[617_fhe_modular_multiplier|FHE]] 가속기는 속이 보이지 않는 금고 안에서 로봇 팔이 계산을 대신해 주는 것과 같다. 금고를 맡긴 사람만 열쇠를 갖고 있고, 계산을 맡은 사람은 금고 안 내용을 끝내 모른다.

---

## Ⅱ. 아키텍처 및 핵심 원리

대부분의 [[617_fhe_modular_multiplier|FHE]] 스킴은 잔여수 체계 (RNS, Residue Number System) 위에서 거대한 [[195_polynomial_generator_crc|다항식]] 환 연산을 반복한다. 이때 핵심 병목은 수론적 변환 (NTT, Number Theoretic Transform), 역수론적 변환 (INTT, Inverse Number Theoretic Transform), 키 스위칭, 그리고 노이즈를 다시 낮추는 [[120_concept|부트스트래핑]]이다. 따라서 좋은 [[617_fhe_modular_multiplier|FHE]] 가속기는 단순히 곱셈기를 많이 넣는 것이 아니라, **메모리 이동을 줄이며 이 네 단계가 끊기지 않게 파이프라인을 짜는 것**이 핵심이다.

| 구성 요소 | 역할 | 설계 포인트 |
| :-- | :-- | :-- |
| 호스트 런타임 | 연산 [[070_graph_datastructure|그래프]] 스케줄링, 파라미터·키 관리 | [[356_pcie|PCI Express]] ([[356_pcie|PCIe]]) 왕복을 줄이고 배치 단위를 키워야 한다. |
| NTT/INTT 어레이 | [[195_polynomial_generator_crc|다항식]] 곱셈을 점별 곱셈 형태로 변환 | [[192_module_independence|모듈]]러 곱셈 병렬도와 [[001_dikw_pyramid|데이터]] 재사용이 [[282_performance_tactics|성능]]을 좌우한다. |
| 키 스위칭·리스케일 유닛 | 기저 변환, 스케일 정리, 노이즈 제어 | 중간 버퍼 재활용과 [[233_precision_recall_f1_roc_auc_threshold|정밀도]] 손실 관리가 중요하다. |
| [[120_concept|부트스트래핑]] 엔진 | 누적된 노이즈를 초기화에 가깝게 복원 | 가장 긴 지연구간이므로 전용 파이프라인이 필요하다. |
| 온칩 [[250_sram|SRAM]] + [[495_hbm|HBM]] | 중간 암호문 타일과 키 [[001_dikw_pyramid|데이터]] 저장 | 연산 자체보다 메모리 [[140_bandwidth|대역폭]]이 병목이 되기 쉽다. |

아래 그림은 [[617_fhe_modular_multiplier|FHE]] 가속기에서 암호문이 어떤 하드웨어 경로를 통과하는지 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ FHE accelerator datapath                                                 │
├──────────────────────────────────────────────────────────────────────────┤
│ HBM / DDR                                                                │
│   │ ciphertext tiles                                                     │
│   ▼                                                                      │
│ DMA + on-chip SRAM                                                       │
│   │                                                                      │
│   ├─▶ NTT / INTT array ─▶ point-wise MUL/ADD ─▶ rescale / mod-switch     │
│   │                                                                      │
│   └──────────────────────────────────────────────▶ key-switch engine      │
│                                                   │                      │
│                                                   └──▶ bootstrap engine   │
│                                                            │             │
│                                                            ▼             │
│                                                      ciphertext writeback │
└──────────────────────────────────────────────────────────────────────────┘
```

이 경로에서 중요한 사실은 연산 순서가 수학적 필요성에 의해 거의 정해져 있다는 점이다. NTT는 [[195_polynomial_generator_crc|다항식]] 합성곱을 빠른 점별 곱셈으로 바꾸고, 키 스위칭과 리스케일은 스킴이 계속 성립하도록 표현을 바꾸며, [[120_concept|부트스트래핑]]은 깊은 회로를 계속 계산할 수 있도록 노이즈를 새로 정돈한다. 결국 [[617_fhe_modular_multiplier|FHE]] 가속기 설계는 "연산기 수"보다 "중간 암호문을 얼마나 덜 옮기느냐"가 더 큰 승부처가 된다.

- **📢 섹션 요약 비유**: [[617_fhe_modular_multiplier|FHE]] 가속기는 밀가루 공장과 비슷하다. 밀을 빻는 기계만 빠르다고 끝이 아니라, 저장창고·운반 벨트·정제 공정이 끊기지 않아야 전체 생산량이 올라간다.

---

## Ⅲ. 비교 및 연결

[[617_fhe_modular_multiplier|FHE]] 가속기는 [[795_confidential_computing|기밀 컴퓨팅]]의 다른 방법과 함께 봐야 경계가 또렷해진다. [[478_tee|신뢰 실행 환경]] ([[478_tee|TEE]], [[972_tee_based_ml|Trusted Execution Environment]])은 안전한 실행 구역 안에서 **평문**을 처리하므로 지연시간은 상대적으로 작지만 CPU 공급자와 부채널 완화를 어느 정도 신뢰해야 한다. 반면 FHE는 서버가 끝까지 평문을 보지 못하므로 신뢰 가정을 더 줄일 수 있지만, 연산 비용이 훨씬 크다. 다자간 계산 (MPC, Multi-Party Computation)은 여러 참여자가 비밀을 나눠 계산하는 방식이라 네트워크 상호작용 비용이 커지는 대신, 단일 하드웨어 신뢰점에 덜 의존한다.

| 구분 | [[617_fhe_modular_multiplier|FHE]] 가속기 | [[478_tee|TEE]] | MPC |
| :-- | :-- | :-- | :-- |
| 서버가 보는 [[001_dikw_pyramid|데이터]] | 끝까지 암호문 | 실행 중 평문 가능 | 분할된 비밀 조각 |
| 신뢰 가정 | 비밀키 보유자만 신뢰 | CPU/[[032_firmware|펌웨어]]/부채널 완화 일부 신뢰 | 다수 참여자 중 임계 수 이상 정직 가정 |
| [[282_performance_tactics|성능]] 특성 | 가장 무겁지만 가장 강한 비노출 | 상대적으로 빠름 | 네트워크 왕복 비용 큼 |
| 잘 맞는 용도 | 프라이버시 분석, 비밀 추론 | 저지연 기밀 처리 | 공동 통계, 연합 계산 |

실무에서는 이 셋이 경쟁만 하는 것이 아니라 보완적으로 쓰인다. 예를 들어 키 보관과 인증은 [[475_hsm|하드웨어 보안 모듈]] ([[475_hsm|HSM]], [[157_hsm_hardware_security_module|Hardware Security Module]])이 맡고, [[160_session_controlling_terminal|세션]] 설정과 제어 평면은 [[480_intel_sgx|Intel SGX]] 같은 TEE가 처리하며, 대량 암호문 연산만 [[617_fhe_modular_multiplier|FHE]] 가속기에 보내는 식의 혼합 구조가 가능하다. 즉 [[617_fhe_modular_multiplier|FHE]] 가속기는 "모든 보안을 대체하는 칩"이 아니라, **평문 노출을 가장 강하게 줄여야 하는 [[001_dikw_pyramid|데이터]] 평면**에 투입되는 특수 엔진이다.

- **📢 섹션 요약 비유**: TEE가 잠긴 상담실이라면, FHE는 내용이 안 보이는 봉인 문서끼리 계산하는 방식이고, MPC는 여러 사람이 문서 조각을 나눠 들고 함께 퍼즐을 맞추는 방식이다. 같은 보안이라도 믿는 대상과 비용 구조가 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

[[617_fhe_modular_multiplier|FHE]] 가속기는 개인정보가 매우 민감하지만 계산은 외부 인프라에 맡겨야 하는 구간에서 빛난다. 대표적으로 암호화된 의료 영상 [[104_classification_analysis|분류]], 금융기관 간 위험도 공동 분석, 고객 [[001_dikw_pyramid|데이터]]가 노출되면 안 되는 클라우드 [[231_ai_turing_test|인공지능]] 추론이 있다. 다만 현재도 지연시간과 메모리 요구량이 크기 때문에, 초저지연 제어 루프나 대화형 범용 [[090_service_kubernetes_network_load_balancing|서비스]] 전체를 통째로 FHE에 넣는 것은 현실성이 낮다.

### 적용 판단 [[435_checklist_based_testing|체크리스트]]

1. **연산 깊이 [[396_validation|확인]]**: 회로 깊이가 깊어 [[120_concept|부트스트래핑]]이 자주 필요한가, 아니면 얕은 추론이라 키 스위칭 중심으로 끝나는가?
2. **스킴 선택 [[396_validation|확인]]**: 근사 실수 계산은 CKKS (Cheon-Kim-Kim-Song), 정확한 정수 계산은 BFV/BGV (Brakerski-Fan-Vercauteren / Brakerski-Gentry-Vaikuntanathan), [[073_bit|비트]] 단위 빠른 논리는 TFHE (Fast Fully [[1019_homomorphic_encryption|Homomorphic Encryption]] over the [[390_torus|Torus]])가 적합한가?
3. **[[140_bandwidth|대역폭]] 예산 [[396_validation|확인]]**: 암호문 팽창과 키 [[001_dikw_pyramid|데이터]] 적재를 감당할 [[495_hbm|HBM]] ([[495_hbm|High Bandwidth Memory]]) 또는 고대역 메모리 구성이 있는가?
4. **[[139_throughput|처리량]] 방식 [[396_validation|확인]]**: 단건 지연시간보다 배치 [[139_throughput|처리량]]으로 사업 모델을 맞출 수 있는가?
5. **키 보관 경계 [[396_validation|확인]]**: 비밀키는 사용자 측 또는 HSM에 남기고, 가속기에는 평가키만 보내는 구조가 설계되었는가?

### 피해야 할 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 평문용 [[231_ai_turing_test|인공지능]] 모델을 그대로 옮겨 암호문 팽창과 [[120_concept|부트스트래핑]] 비용을 무시하는 설계
- "암호문이니까 안전하다"며 키 관리와 테넌트 분리를 소홀히 하는 운영
- 몇 밀리초 제어가 필요한 자율 제어 루프에 FHE를 직접 넣는 설계

기술사 답안에서는 FHE의 장밋빛 가능성만 쓰면 부족하다. **왜 느린지**, **어디가 병목인지**, **그래서 어떤 워크로드만 가속기 대상인지**를 함께 적어야 설득력이 생긴다. 특히 연산 깊이와 [[120_concept|부트스트래핑]] 여부를 판단 포인트로 적어 주면 답안의 수준이 올라간다.

- **📢 섹션 요약 비유**: [[617_fhe_modular_multiplier|FHE]] 가속기 도입은 냉동창고 물류를 짜는 일과 같다. 상하기 쉬운 물건은 반드시 냉장 상태를 지켜야 하지만, 모든 물건을 그런 방식으로 옮기면 비용이 폭증하므로 정말 차갑게 지켜야 할 물건에만 투입해야 한다.

---

## Ⅴ. 기대효과 및 결론

[[617_fhe_modular_multiplier|FHE]] 가속기의 가장 큰 효과는 "[[571_protection_vs_security|보호]]하면서 계산한다"는 오랜 난제를 현실 [[090_service_kubernetes_network_load_balancing|서비스]]로 당겨 온다는 점이다. [[001_dikw_pyramid|데이터]] 소유자가 인프라 소유자를 완전히 믿지 않아도, 비밀키를 내놓지 않은 채 분석과 추론을 외부에 맡길 수 있다면 클라우드 보안 모델은 한 단계 더 강해진다. 이는 [[001_dikw_pyramid|데이터]] 활용과 [[001_dikw_pyramid|데이터]] 주권을 동시에 만족시키는 방향이라는 점에서 의미가 크다.

물론 한계도 분명하다. 큰 면적과 [[466_power_consumption|전력 소모]], 높은 메모리 비용, 아직 성숙하지 않은 컴파일러·런타임 생태계는 대중화를 늦추는 요소다. 앞으로는 HBM과 [[497_chiplet|칩렛]] 결합, 자동 파라미터 튜닝, [[478_tee|TEE]]·HSM과 결합한 하이브리드 [[795_confidential_computing|기밀 컴퓨팅]]이 실용화를 앞당길 가능성이 크다. 따라서 [[1019_homomorphic_encryption|동형 암호]] 가속기는 "모든 계산의 기본 칩"이 아니라, **가장 민감한 계산을 위해 선택적으로 붙이는 프라이버시 전용 엔진**으로 기억하는 것이 정확하다.

- **📢 섹션 요약 비유**: [[617_fhe_modular_multiplier|FHE]] 가속기는 비밀 서류 전용 복사 공장과 같다. 일반 서류를 복사하는 데까지 모두 들고 갈 필요는 없지만, 절대 노출되면 안 되는 문서는 느리더라도 전용 공장에서 처리할 가치가 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [[617_fhe_modular_multiplier|완전 동형 암호]] ([[617_fhe_modular_multiplier|FHE]], Fully [[1019_homomorphic_encryption|Homomorphic Encryption]]) | 암호문 상태에서 덧셈과 곱셈을 수행하게 하는 수학적 기반이다. |
| 수론적 변환 (NTT, Number Theoretic Transform) | [[617_fhe_modular_multiplier|FHE]] [[195_polynomial_generator_crc|다항식]] 곱셈의 핵심 병목으로, 가속기 병렬화의 중심이 된다. |
| [[120_concept|부트스트래핑]] ([[120_concept|Bootstrapping]]) | 누적 노이즈를 다시 낮춰 깊은 회로 계산을 계속 가능하게 만든다. |
| 키 스위칭 ([[067_db_key_uniqueness_minimality|Key]] Switching) | 암호문 표현과 키 기준을 바꾸어 후속 연산을 이어 가게 한다. |
| CKKS / BFV / TFHE | 근사 실수, 정확 정수, [[073_bit|비트]] 연산 등 워크로드별 [[617_fhe_modular_multiplier|FHE]] 스킴 선택지를 제공한다. |
| [[795_confidential_computing|기밀 컴퓨팅]] ([[795_confidential_computing|Confidential Computing]]) | [[617_fhe_modular_multiplier|FHE]] 가속기는 처리 중 [[001_dikw_pyramid|데이터]] [[571_protection_vs_security|보호]]를 강화하는 가장 강한 축 중 하나다. |

### 📈 관련 키워드 및 발전 흐름도

```text
저장 데이터 암호화 · 전송 데이터 암호화
                │
                ▼
부분 동형 암호 (PHE, Partially Homomorphic Encryption)
                │
                ▼
완전 동형 암호 (FHE, Fully Homomorphic Encryption)
                │
                ▼
RNS · NTT · Bootstrapping 최적화
                │
                ▼
FHE Accelerator + HBM
                │
                ▼
프라이버시 보호 인공지능 · 제로트러스트 분석
```

이 흐름은 "보관 [[571_protection_vs_security|보호]]"에서 "연산 [[571_protection_vs_security|보호]]"로, 다시 "수학적 가능성"에서 "전용 하드웨어 실용화"로 진화하는 방향을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[617_fhe_modular_multiplier|FHE]] 가속기는 비밀이 든 상자를 열지 않고도 안에서 계산해 주는 특별한 로봇이에요.
2. 보통 컴퓨터는 계산하려면 상자를 열어 봐야 하지만, 이 로봇은 상자를 닫은 채로도 일을 할 수 있어요.
3. 대신 일이 아주 어려워서, 보통 컴퓨터보다 훨씬 힘센 전용 기계가 필요하답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 489 / 803

← **이전**: [[488_smm|488. 시스템 관리 모드 (SMM)]]
**다음**: [[490_edge_computing_hw|490. 엣지 컴퓨팅 하드웨어 (Edge Computing HW)]] →

---
