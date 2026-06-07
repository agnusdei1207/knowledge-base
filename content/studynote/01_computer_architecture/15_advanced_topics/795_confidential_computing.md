---
title: "Confidential Computing"
date: "2026-05-08"
tags:
  - "studynote-computer-architecture"
weight: 795
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 기밀 컴퓨팅은 저장 중 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 전송 중 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)뿐 아니라, 실행 중 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [in Use](/studynote/04_software_engineering/10_trends_pm_quality/694_confidential_computing_data_in_use/))까지 하드웨어 격리 영역에서 보호하는 보안 패러다임이다.
> 2. **가치**: 클라우드 사업자와 하이퍼바이저를 완전 신뢰하지 않아도 민감 워크로드를 올릴 수 있게 해, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 주권과 규제 대응의 현실적 기반을 만든다.
> 3. **판단 포인트**: 핵심 판단은 [TEE](/studynote/01_computer_architecture/14_hardware_security_trends/478_tee/) ([Trusted Execution Environment](/studynote/09_security/19_ai_advanced_security/972_tee_based_ml/))만으로 충분한지, 원격 증명과 사이드채널 대응, 워크로드 수정 비용까지 감수할 가치가 있는지의 균형이다.

---

## Ⅰ. 개요 및 필요성

기존 보안은 디스크의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 네트워크를 보호하는 데는 익숙했지만, 실제 계산 순간의 평문은 CPU와 메모리 안에 노출될 수밖에 없었다. 기밀 컴퓨팅은 이 마지막 빈틈을 메우려는 시도다. 즉 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 "쉬고 있을 때"뿐 아니라 "일하고 있을 때"도 외부에서 보이지 않게 하려는 것이다. 그래서 이 기술은 단일 제품명이 아니라, 현대 클라우드가 신뢰를 재설계하는 큰 흐름으로 보는 편이 정확하다.

```text
+--------------------------------------------------------------+
|            Security across the full data lifecycle          |
+--------------------------------------------------------------+
| Data at rest   -> disk encryption                           |
| Data in transit-> TLS                                       |
| Data in use    -> confidential computing / TEE              |
+--------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 귀중품을 창고에 둘 때와 옮길 때만 잠그는 것이 아니라, 꺼내서 손보는 순간에도 불투명한 작업실 안에서 다루자는 생각과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

기밀 컴퓨팅은 대개 하드웨어 [TEE](/studynote/01_computer_architecture/14_hardware_security_trends/478_tee/), [메모리 암호화 엔진](/studynote/09_security/04_endpoint_security/393_memory_encryption_engine/), 측정 부팅, 원격 증명으로 구성된다. 워크로드는 [enclave](/studynote/09_security/04_endpoint_security/390_enclave/) 또는 confidential [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 형태로 올라가고, 외부 사용자는 측정값과 서명된 증명서를 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한 뒤에만 키를 제공한다. 따라서 단순 격리만으로는 부족하고, "내가 기대한 코드가 실제 격리 공간에서 돌고 있다"는 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 루프가 필수다. [Intel SGX](/studynote/01_computer_architecture/14_hardware_security_trends/480_intel_sgx/), AMD SEV-SNP, Intel TDX, ARM CCA는 이 패러다임의 서로 다른 구현이라고 볼 수 있다.

| 구성 축 | 역할 | 핵심 질문 |
| :--- | :--- | :--- |
| [TEE](/studynote/01_computer_architecture/14_hardware_security_trends/478_tee/) / [Enclave](/studynote/09_security/04_endpoint_security/390_enclave/) | 실행 중 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 격리 | 무엇을 어디까지 격리할 것인가 |
| [Memory Encryption](/studynote/01_computer_architecture/15_advanced_topics/796_memory_encryption/) | 외부 메모리 평문 노출 방지 | 기밀성만인지 무결성까지인지 |
| [Measured Boot](/studynote/09_security/18_iot_ot_physical/919_measured_boot/) | 로드 코드 측정 | 어디서부터 신뢰를 시작할 것인가 |
| [Remote Attestation](/studynote/09_security/04_endpoint_security/396_remote_attestation/) | 원격 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)과 키 릴리스 | 누가 측정값을 믿을 것인가 |

```text
+--------------------------------------------------------------+
|         Generic confidential-computing trust sequence       |
+--------------------------------------------------------------+
| Create trusted domain -> measure code -> attest             |
|                                            |                 |
|                                            v                 |
|                                 release secrets / process    |
+--------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 비밀 회의실을 만들고, 참석자 명단을 확인한 뒤에야 회의 자료를 나눠 주는 절차와 같다. 방만 있다고 회의 자료를 바로 줄 수는 없다.

---

## Ⅲ. 비교 및 연결

TEE는 빠르지만 하드웨어 제조사와 구현 신뢰에 의존하고, [FHE](/studynote/01_computer_architecture/15_advanced_topics/617_fhe_modular_multiplier/) (Fully [Homomorphic Encryption](/studynote/09_security/20_extra_exam_prep/1098_homomorphic_encryption/))와 MPC (Multi-Party Computation)는 더 강한 수학적 모델을 제공하지만 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 비용이 크다. 또한 CPU 내부 enclave형과 [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 단위 confidential computing은 개발 수정 범위와 운영 방식이 다르다. 그래서 기밀 컴퓨팅 도입은 "무조건 [TEE](/studynote/01_computer_architecture/14_hardware_security_trends/478_tee/)"가 아니라, 요구 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)·규제 수준·공격 모델을 맞춰 고르는 문제다.

| 비교 대상 | 장점 | 대표 한계 |
| :--- | :--- | :--- |
| [TEE](/studynote/01_computer_architecture/14_hardware_security_trends/478_tee/) 기반 기밀 컴퓨팅 | 실용적 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 즉시 적용성 | 제조사·사이드채널 신뢰 필요 |
| [FHE](/studynote/01_computer_architecture/15_advanced_topics/617_fhe_modular_multiplier/) | 암호문 상태 연산 가능 | 실무 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 부담 큼 |
| MPC | 여러 주체가 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 신뢰 형성 | [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 복잡도와 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 증가 |

- **📢 섹션 요약 비유**: 장갑 낀 작업실, 수학 마법, 여러 사람이 나눠 드는 비밀 상자는 모두 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 지키는 방식이지만, 속도와 운영 방식이 제각각이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 금융 분석, 의료 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 협업, [멀티 클라우드](/studynote/12_it_management/05_security_compliance/202_multi_cloud_hybrid_cloud_governance/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리, 모델 보호형 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 추론이 대표 적용 분야다. 기술사 판단에서는 첫째 원격 증명을 실제로 업무 흐름에 넣었는지, 둘째 [메모리 암호화](/studynote/01_computer_architecture/15_advanced_topics/796_memory_encryption/)가 무결성까지 보장하는지, 셋째 사이드채널과 디버그 예외를 어떻게 줄였는지 확인해야 한다. 또한 SGX처럼 애플리케이션 수정이 큰 방식인지, confidential VM처럼 기존 워크로드 이식성이 높은 방식인지도 의사결정 포인트다.

- **📢 섹션 요약 비유**: 비밀 회의실을 만든 뒤에도 출입 명부를 검사하고 [도청](/studynote/03_network/14_network_security_threats/701_sniffing_eavesdropping_promiscuous/) 장비를 점검해야 진짜 안전한 회의가 된다. 기밀 컴퓨팅도 마찬가지다.

---

## Ⅴ. 기대효과 및 결론

기밀 컴퓨팅은 민감 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 클라우드 이전을 가속하고, [데이터 공유](/studynote/05_database/06_dw_olap_trends/386_data_clean_room_sharing/) 협업의 신뢰 비용을 낮추는 효과가 크다. 반면 하드웨어 [종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/), 측정·증명 운영 복잡도, 사이드채널 대응은 여전히 부담이다. 앞으로는 엔클레이브 간 상호 증명, [GPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)·CXL까지 확장된 기밀 영역, 표준화된 증명 API가 더 중요해질 가능성이 크다. 따라서 기밀 컴퓨팅은 제품 기능이 아니라 "클라우드에서도 실행 중 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 보이지 않아야 한다"는 보안 원칙으로 기억하는 것이 적절하다.

- **📢 섹션 요약 비유**: 귀중품을 맡길 때 창고만 믿는 시대에서, 작업대까지 불투명 상자로 덮는 시대로 넘어간 것이라고 보면 된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [Remote Attestation](/studynote/09_security/04_endpoint_security/396_remote_attestation/) | 기밀 컴퓨팅의 실제 신뢰 성립 조건 |
| Confidential [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) | [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 단위로 적용되는 대표 실무 형태 |
| [Memory Encryption](/studynote/01_computer_architecture/15_advanced_topics/796_memory_encryption/) | 실행 중 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 보호의 물리적 기반 |
| CCC | Confidential Computing Consortium, 표준화 생태계 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Measured Trusted Domain]
    |
    v
[Remote Attestation]
    |
    v
[Secret Release for Processing]
    |
    +---> [Confidential VM / Enclave]
    +---> [Protected Result Sharing]
```

이 흐름은 기밀 컴퓨팅이 단순 격리에서 끝나지 않고, 측정과 증명 뒤에야 비밀을 주입하는 구조임을 보여준다. 즉 "격리"보다 "[검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)된 격리"가 핵심이다.

### 👶 어린이를 위한 3줄 비유 설명

1. 중요한 숙제를 할 때, 아무도 안 들여다볼 수 있는 투명하지 않은 비밀 책상 안에서 공부하는 것과 비슷해요.
2. 선생님은 그 비밀 책상이 진짜인지 먼저 확인한 뒤에만 숙제 종이를 넣어 줘요.
3. 그래서 밖에서 보는 사람은 숙제 답안을 훔쳐보기 훨씬 어려워져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 796 / 803

<- **이전**: [794. AWS Nitro Enclaves (AWS Nitro Enclaves)](/studynote/01_computer_architecture/15_advanced_topics/794_aws_nitro_enclaves/)
**다음**: [796. 메모리 암호화 (Memory Encryption)](/studynote/01_computer_architecture/15_advanced_topics/796_memory_encryption/) ->

---
