+++
title = "768. SGAxe 및 CrossTalk 공격"
date = 2026-05-08

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SGAxe와 CrossTalk는 "신뢰 실행 환경은 안전하다" 또는 "다른 코어는 충분히 멀다"는 가정을 무너뜨린 후속 [마이크로아키텍처](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/204_microarchitecture/) 부채널 공격으로, 각각 [Intel SGX](/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/480_intel_sgx/) ([Software Guard Extensions](/knowledge-base/studynote/09_security/04_endpoint_security/389_sgx/)) 내부 비밀과 코어 간 특수 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 경로를 노렸다.
> 2. **가치**: SGAxe는 [Intel SGX](/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/480_intel_sgx/) ([Software Guard Extensions](/knowledge-base/studynote/09_security/04_endpoint_security/389_sgx/)) 원격 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 체인에 필요한 비밀을 탈취해 가짜 신뢰를 만들 수 있음을 보였고, CrossTalk는 SRBDS (Special [Register](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/) Buffer [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Sampling](/knowledge-base/studynote/03_network/01_data_communication/056_표본화_Sampling/))를 통해 물리적으로 다른 코어의 특수 명령 결과까지 엿볼 수 있음을 증명했다.
> 3. **판단 포인트**: 이 계열의 대응은 단순 패치 적용을 넘어 마이크로코드 업데이트, [SGX](/knowledge-base/studynote/09_security/04_endpoint_security/389_sgx/) TCB (Trusted Computing Base) [Recovery](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), 특수 명령 직렬화, 그리고 [기밀 컴퓨팅](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/795_confidential_computing/) 배치 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)까지 포함해야 완결된다.

---

## Ⅰ. 개요 및 필요성

[멜트다운](/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/482_meltdown/), [스펙터](/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/483_spectre/), [MDS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/764_mds/) 이후 많은 운영자는 "그래도 [SGX](/knowledge-base/studynote/09_security/04_endpoint_security/389_sgx/) 같은 신뢰 실행 환경은 마지막 보루일 것" 그리고 "누수는 대체로 같은 코어 안에서만 일어날 것"이라고 기대했다. SGAxe와 CrossTalk는 바로 이 두 가정을 정면으로 깨뜨린 사례다. 하나는 SGX의 신뢰 체인 자체를 흔들었고, 다른 하나는 물리적으로 다른 코어 사이에도 누수 통로가 있을 수 있음을 보여줬다.

SGAxe는 CacheOut 계열의 L1D (Level 1 [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Cache) 축출 샘플링을 바탕으로 [SGX](/knowledge-base/studynote/09_security/04_endpoint_security/389_sgx/) 관련 비밀을 회수해, 원격 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)([Remote Attestation](/knowledge-base/studynote/09_security/04_endpoint_security/396_remote_attestation/)) 신뢰를 위조할 수 있음을 보였다. CrossTalk는 SRBDS라는 이름으로 공개되었으며, `RDRAND`, `RDSEED`, 일부 [SGX](/knowledge-base/studynote/09_security/04_endpoint_security/389_sgx/) 특수 경로처럼 특수 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 값을 전달할 때 쓰는 공유 staging buffer를 다른 코어에서 엿들을 수 있음을 드러냈다.

즉 두 공격은 단순히 "새로운 CVE가 또 나왔다"는 의미가 아니라, 하드웨어가 제공하던 최고 수준의 격리 약속이 실제 배선·버퍼·전달 경로 수준에서는 생각보다 쉽게 깨질 수 있음을 보여준다. 신뢰 기반을 설계하는 사람에게는 [보안 기능](/knowledge-base/studynote/04_software_engineering/11_testing_validation/503_security_features_design/)의 이름보다 내부 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 경로가 더 중요하다는 교훈을 남겼다.

- **📢 섹션 요약 비유**: 성벽은 두꺼웠지만, 성 안의 비밀문서가 지나가는 배수로와 우편관이 새고 있었던 셈이라서 SGAxe와 CrossTalk는 "벽"보다 "배관"을 공격한 사례다.

---

## Ⅱ. 아키텍처 및 핵심 원리

SGAxe와 CrossTalk는 같은 문맥에서 자주 묶이지만, 메커니즘은 다르다. SGAxe는 [SGX](/knowledge-base/studynote/09_security/04_endpoint_security/389_sgx/) 내부 비밀이 캐시·축출 경로에서 새는 문제를 파고들고, CrossTalk는 특수 명령 결과가 잠깐 머무는 전역 staging buffer를 코어 간에 공유한다는 점을 찌른다. 하나는 "엔클레이브의 비밀도 밖으로 나온다"를, 다른 하나는 "다른 코어도 안전지대가 아니다"를 보여준 셈이다.

| 구분 | SGAxe | [CrossTalk](/knowledge-base/studynote/03_network/01_data_communication/030_누화_크로스토크/) / SRBDS |
| :--- | :--- | :--- |
| 주된 표적 | [SGX](/knowledge-base/studynote/09_security/04_endpoint_security/389_sgx/) 관련 비밀, 특히 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 체인 자료 | 특수 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 명령 결과의 staging buffer |
| 핵심 경로 | CacheOut류 L1D eviction [sampling](/knowledge-base/studynote/03_network/01_data_communication/056_표본화_Sampling/) | 공유 special-[register](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/) staging buffer |
| 깨지는 경계 | 엔클레이브 내부 비밀, 원격 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 신뢰 | 물리 코어 분리 가정 |
| 대표 영향 | 가짜 [SGX](/knowledge-base/studynote/09_security/04_endpoint_security/389_sgx/) 원격 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 가능성 | [RDRAND](/knowledge-base/studynote/09_security/20_extra_exam_prep/1002_rdrand_intel_hardware_rng/)/RDSEED/[SGX](/knowledge-base/studynote/09_security/04_endpoint_security/389_sgx/) 특수 경로 값 노출 |
| 주요 완화 | [SGX](/knowledge-base/studynote/09_security/04_endpoint_security/389_sgx/) TCB [Recovery](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), 마이크로코드, 재검증 | 마이크로코드 직렬화, staging buffer [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) |

다음 그림은 두 공격이 겨냥한 신뢰 경로를 한눈에 보여준다.

```text
+--------------------------------------------------------------------+
| Trusted path failures                                             |
+-------------------------------+------------------------------------+
| SGAxe                         | CrossTalk / SRBDS                  |
| SGX enclave / attest secret   | Core 0: RDRAND / SGX op            |
|            |                  |            |                       |
|    L1D eviction path          |   shared staging buffer            |
|            |                  |            |                       |
|   CacheOut-style sample       |   Core 1: transient sample         |
+-------------------------------+------------------------------------+
```

SGAxe를 이해할 때는 Quoting [Enclave](/knowledge-base/studynote/09_security/04_endpoint_security/390_enclave/) (QE)와 원격 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 체인이 중요하다. 공격자가 attestation-related secret을 회수하면, 외부 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)자 입장에서는 가짜 엔클레이브를 진짜처럼 믿을 위험이 생긴다. CrossTalk를 이해할 때는 "특수 명령은 코어 안에서만 끝난다"는 믿음이 깨진다는 점이 중요하다. 공유 staging buffer에 값이 잠깐 놓이는 순간, 다른 코어도 그 잔상을 관찰할 수 있기 때문이다.

결국 두 공격 모두 기능 격리와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 격리가 같지 않다는 사실을 보여준다. [보안 기능](/knowledge-base/studynote/04_software_engineering/11_testing_validation/503_security_features_design/)이 아무리 화려해도, 그 기능을 떠받치는 버퍼와 전달 경로가 공유되면 신뢰의 마지막 고리가 끊어진다.

- **📢 섹션 요약 비유**: SGAxe는 왕의 금고에서 나오는 열쇠 도장을 위조한 사건이고, CrossTalk는 다른 건물 우편실에서 내 비밀 서류가 지나는 우편관을 몰래 엿본 사건이라고 생각하면 된다.

---

## Ⅲ. 비교 및 연결

이 둘을 [RIDL](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/765_ridl_attack/), [좀비로드](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/767_zombieload_attack/) 같은 [MDS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/764_mds/) 계열과 연결해서 보면 신뢰 경계가 단계적으로 무너지는 흐름이 보인다. [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 공격이 같은 코어의 버퍼 공유를 보여줬다면, CrossTalk는 코어 경계 너머의 공유 경로까지 드러냈고, SGAxe는 그 위에 세워진 [SGX](/knowledge-base/studynote/09_security/04_endpoint_security/389_sgx/) 신뢰 체인 자체를 흔들었다. 즉 "같은 코어의 누수"에서 끝난 이야기가 아니라, "최고 [보안 기능](/knowledge-base/studynote/04_software_engineering/11_testing_validation/503_security_features_design/)도 하드웨어 공유 경로에 종속된다"는 결론으로 확장된 것이다.

| 신뢰 경계 | [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [MDS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/764_mds/) 계열 | [CrossTalk](/knowledge-base/studynote/03_network/01_data_communication/030_누화_크로스토크/) | SGAxe |
| :--- | :--- | :--- | :--- |
| 같은 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) / 같은 코어 | 버퍼 잔상 누수 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 포함 | 포함 |
| 다른 물리 코어 | 대체로 제한적 | 명시적으로 붕괴 | 간접적으로 영향 |
| [SGX](/knowledge-base/studynote/09_security/04_endpoint_security/389_sgx/) 엔클레이브 내부 비밀 | 상대적으로 더 강한 가정 | 일부 특수 경로와 연결 | 직접적으로 붕괴 |
| 원격 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 신뢰 | 대체로 유지 | 우회 가능성 확대 | 실질적 위조 위험 제시 |

이 흐름은 [기밀 컴퓨팅](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/795_confidential_computing/)([Confidential Computing](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/795_confidential_computing/))에도 큰 시사점을 준다. 엔클레이브, 하드웨어 난수, 원격 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 모두 안전하다고 가정해 설계를 짜더라도, 실제 칩 내부의 공유 버퍼와 전달 경로를 모르면 그 가정은 쉽게 깨진다. 따라서 설계자는 기능 명세보다 실제 [마이크로아키텍처](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/204_microarchitecture/) 자원 공유 지도를 더 꼼꼼히 봐야 한다.

- **📢 섹션 요약 비유**: 예전에는 같은 방 사람끼리만 몰래 엿듣는 문제였다면, 이제는 다른 층 사람도 배관을 타고 듣고, 심지어 건물 출입증 발급소의 도장까지 훔치는 수준으로 커진 셈이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무 대응은 두 층으로 나뉜다. 첫째는 즉시 적용 가능한 기술적 완화다. 최신 BIOS/UEFI와 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 마이크로코드를 적용해 SRBDS 완화를 켜고, 특수 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 명령 경로를 직렬화하여 staging buffer 공유 창을 줄여야 한다. 둘째는 [SGX](/knowledge-base/studynote/09_security/04_endpoint_security/389_sgx/) 운영 복구다. SGAxe 영향 범위에 들어가는 플랫폼은 [SGX](/knowledge-base/studynote/09_security/04_endpoint_security/389_sgx/) TCB Recovery를 수행해 신뢰 기준을 갱신하고, 기존 attestation 자격과 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 체인을 재검증해야 한다.

보안 설계자는 "패치를 했으니 다시 안전하다"고 끝내면 안 된다. SGX를 실제로 쓰는 서비스라면 quote [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/), 플랫폼 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 갱신, Quoting [Enclave](/knowledge-base/studynote/09_security/04_endpoint_security/390_enclave/) 관련 운영 절차까지 다시 점검해야 한다. 또한 CrossTalk는 일반 워크로드 전체에 큰 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 손실을 주지는 않을 수 있지만, `RDRAND`·`RDSEED` 호출이 매우 많은 암호 모듈이나 빈번한 attestation 경로에서는 직렬화 비용이 체감될 수 있다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. SRBDS/[CrossTalk](/knowledge-base/studynote/03_network/01_data_communication/030_누화_크로스토크/) 대응용 최신 마이크로코드와 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 패치가 적용되어 있는가?
2. SGX를 사용하는 경우 TCB [Recovery](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서/quote 갱신, 원격 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 재설정을 완료했는가?
3. 패치 불가능한 구형 플랫폼에서는 [SGX](/knowledge-base/studynote/09_security/04_endpoint_security/389_sgx/) 사용 중단 또는 전용 호스트 격리를 검토했는가?
4. 난수 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·원격 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)·[기밀 컴퓨팅](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/795_confidential_computing/) 워크로드에서 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 보안 영향을 별도로 계측했는가?

기술사 관점의 핵심은 "신뢰 기능을 켠다"가 아니라 "신뢰 기능의 운영 수명주기를 관리한다"는 데 있다. 특히 SGAxe는 비밀이 한 번 유출되면 플랫폼 신뢰 자체를 재발급해야 함을 보여줬기 때문에, 패치와 운영 복구가 함께 움직여야 한다.

- **📢 섹션 요약 비유**: SGAxe와 [CrossTalk](/knowledge-base/studynote/03_network/01_data_communication/030_누화_크로스토크/) 대응은 금고 문만 고치는 수준이 아니라, 위조됐을지 모르는 도장과 출입증을 전부 다시 발급하고 우편관 운행 방식까지 바꾸는 일이다.

---

## Ⅴ. 기대효과 및 결론

이들 공격에 대한 완화와 운영 복구가 제대로 이뤄지면, 최소한 [SGX](/knowledge-base/studynote/09_security/04_endpoint_security/389_sgx/)·특수 명령·코어 격리 같은 고신뢰 기능에 대한 과도한 낙관을 줄이고 현실적인 신뢰 모델을 세울 수 있다. 원격 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 체인을 새로 정비하면 가짜 플랫폼을 진짜로 믿는 위험을 줄일 수 있고, [CrossTalk](/knowledge-base/studynote/03_network/01_data_communication/030_누화_크로스토크/) 대응은 코어 간 특수 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전달이 더 이상 무방비 상태로 남지 않게 만든다.

장기적으로는 하드웨어가 "[보안 기능](/knowledge-base/studynote/04_software_engineering/11_testing_validation/503_security_features_design/)"만 추가할 것이 아니라, 그 기능을 지탱하는 전달 경로 전체를 보안 설계 대상으로 삼아야 한다. 엔클레이브, [난수 생성기](/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/486_trng/), 특수 명령 버퍼, [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 체인이 모두 문맥별로 격리되고 자동으로 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화되는 방향이 필요하다. SGAxe와 CrossTalk는 결국 "가장 깊은 [신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) 공유 버퍼 위에 세워지면 무너질 수 있다"는 사실을 기억하게 만든다.

- **📢 섹션 요약 비유**: 미래의 CPU는 성벽만 높은 왕성이 아니라, 배수로·우편관·출입증 발급소까지 한 세트로 잠그는 도시처럼 설계되어야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [Intel SGX](/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/480_intel_sgx/) ([Software Guard Extensions](/knowledge-base/studynote/09_security/04_endpoint_security/389_sgx/)) | SGAxe가 신뢰 체인과 엔클레이브 비밀을 흔든 대상 |
| CacheOut / L1D eviction [sampling](/knowledge-base/studynote/03_network/01_data_communication/056_표본화_Sampling/) | SGAxe의 기반이 된 캐시 축출 샘플링 계열 |
| SRBDS (Special [Register](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/) Buffer [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Sampling](/knowledge-base/studynote/03_network/01_data_communication/056_표본화_Sampling/)) | CrossTalk의 공식 취약점 명칭으로, 특수 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) staging buffer 누수를 뜻함 |
| [RDRAND](/knowledge-base/studynote/09_security/20_extra_exam_prep/1002_rdrand_intel_hardware_rng/) / RDSEED | CrossTalk가 노린 대표 특수 명령 경로 |
| TCB [Recovery](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) (Trusted Computing Base [Recovery](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)) | 유출 가능성이 생긴 [SGX](/knowledge-base/studynote/09_security/04_endpoint_security/389_sgx/) 플랫폼의 신뢰 기준을 다시 세우는 운영 절차 |

### 📈 관련 키워드 및 발전 흐름도

```text
Transient-execution research
    |
    v
MDS / CacheOut / SRBDS
    |
    +- SGAxe: SGX trust collapse
    |
    +- CrossTalk: cross-core leakage
    |
    v
Microcode + TCB Recovery + secure deployment policy
```

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터 안에는 아무도 못 열 거라고 믿었던 비밀 금고와 비밀 우편관이 있었어요.
2. SGAxe는 금고 도장을 훔쳐서 가짜 출입증을 만들었고, CrossTalk는 멀리 있는 다른 방의 우편관을 몰래 들여다봤어요.
3. 그래서 이제는 금고 비밀번호만 바꾸는 게 아니라, 도장도 새로 만들고 우편관도 한 사람씩만 쓰게 바꿔야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 769 / 803

<- **이전**: [767. 좀비로드 (ZombieLoad)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/767_zombieload_attack/)
**다음**: [769. 플런더버그 (Plundervolt)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/769_plundervolt/) ->

---
