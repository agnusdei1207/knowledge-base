+++
title = "801. RISC-V ePMP (Enhanced PMP)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ePMP는 기존 PMP를 확장해 M-mode 자체의 권한까지 더 엄격히 통제하고, W^X (Write XOR Execute) 같은 보안 원칙을 [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) 수준에서 강제하려는 [RISC-V](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/200_riscv/) 보안 확장이다.
> 2. **가치**: 부트 로더와 보안 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)가 동작하는 최상위 특권 모드의 실수나 취약점을 줄여, 오픈 하드웨어 [secure boot](/knowledge-base/studynote/02_operating_system/10_security/608_secure_boot/) 체인의 신뢰성을 높인다.
> 3. **판단 포인트**: 핵심 판단은 mseccfg.MML·RL 같은 강화 기능을 언제 활성화할지, 그리고 활성화 직후 현재 실행 코드와 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)이 올바른 권한 영역에 있는지 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 절차다.

---

## Ⅰ. 개요 및 필요성

표준 PMP는 하위 모드를 제한하는 데는 유용하지만, M-mode가 너무 강하면 [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) 버그 하나로 전체 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 경계가 무너질 수 있다. ePMP는 바로 이 문제를 줄이기 위해 나온다. 즉 "최고 권한도 무제한이면 위험하다"는 생각을 하드웨어에 반영한 것이다. 그래서 ePMP는 RISC-V에서 secure boot와 고신뢰 [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) 설계를 더 현실적으로 만드는 중요한 연결 고리다.

```text
+--------------------------------------------------------------+
|           ePMP constrains even the top privilege            |
+--------------------------------------------------------------+
| Standard PMP : mainly lower-mode restriction                |
| ePMP         : stronger M-mode control + W^X intent         |
+--------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 왕에게도 안전벨트를 매는 셈이다. 왕이 가장 힘이 세더라도, 실수로 성문을 부수면 모두 위험해지기 때문이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

ePMP의 핵심은 `mseccfg` 레지스터와 MML (Machine Mode [Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/)), RL (Rule [Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/)) 같은 추가 제어 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)다. 이를 통해 M-mode가 모든 메모리를 마음대로 실행하거나 수정하는 것을 더 엄격하게 제한할 수 있고, [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)을 영구 봉인에 가깝게 고정할 수 있다. 결과적으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 영역과 코드 영역 분리, M-mode [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/), 실행 전용 부트 코드 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)가 훨씬 명확해진다. 즉 ePMP는 표준 PMP의 주소 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)에 "특권 모드 자기 절제"를 추가한 구조다.

| 강화 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| mseccfg | ePMP 동작 모드 전환 | 활성화 전 현재 권한 맵 점검 |
| MML | M-mode에 대한 엄격한 규칙 적용 | 활성화 후 예외 동작 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| RL | 규칙 영구 고정 | 락 전 최종 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 검토 |
| W^X 강화 | [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 가능한 영역의 실행 차단 | 부트 코드/[스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 분리 |

```text
+--------------------------------------------------------------+
|                 ePMP hardening transition                   |
+--------------------------------------------------------------+
| Configure PMP -> verify code/stack regions -> set MML/RL    |
|                                         |                    |
|                                         +- lock hardened mode |
+--------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 문단속 규칙을 정한 뒤 실제 열쇠 위치를 확인하고 마지막으로 봉인 스티커를 붙이는 절차와 같다. 순서를 틀리면 안 된다.

---

## Ⅲ. 비교 및 연결

표준 PMP가 하위 권한에 대한 울타리라면, ePMP는 최고 권한의 행동 규칙까지 추가한 강화형 울타리다. x86의 SMEP/SMAP, ARM의 PXN/WXN 같은 "실행과 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 분리" 철학과도 연결된다. 따라서 ePMP는 단순 [RISC-V](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/200_riscv/) 확장이라기보다, 현대 CPU 보안 원칙을 경량 코어에 이식한 시도라고 볼 수 있다.

| 비교 대상 | 강점 | 대표 차이 |
| :--- | :--- | :--- |
| 표준 PMP | 간단한 물리 경계 제어 | M-mode 자기 제한은 약함 |
| ePMP | M-mode [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)·W^X 강화 | [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 순서와 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 부담 증가 |
| 대형 CPU NX/SMEP류 | 성숙한 실행 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 철학 | RISC-V에는 ePMP 식 구현 |

- **📢 섹션 요약 비유**: 일반 출입 금지선, 왕실 전용 규칙, 대형 궁전의 자동 보안문은 모두 비슷한 원칙을 다른 규모로 구현한 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [secure boot](/knowledge-base/studynote/02_operating_system/10_security/608_secure_boot/) [ROM](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/255_rom/) 이후의 2단계 부트 로더, 보안 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/), [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) 업데이트 코드 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)에 ePMP가 유용하다. 기술사 답안에서는 MML을 켜기 전에 현재 실행 PC와 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 포인터가 어떤 영역에 있는지 확인해야 한다는 운영 포인트를 쓰면 좋다. 또한 RL을 너무 빨리 걸면 현장 복구가 어려워지고, 너무 늦게 걸면 공격 창이 넓어지므로 락 시점 설계가 중요하다.

- **📢 섹션 요약 비유**: 강한 자물쇠를 달아도 집 안에 사람을 가둬 버리면 곤란하다. ePMP는 강하게 잠그되, 잠그기 직전 점검이 더 중요하다.

---

## Ⅴ. 기대효과 및 결론

ePMP는 [RISC-V](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/200_riscv/) [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/)를 "최고 권한이라서 안전하다"는 사고에서 "최고 권한이라서 더 엄격히 통제해야 한다"는 사고로 바꾸는 데 의미가 있다. 이 방향이 자리 잡아야 오픈 실리콘 기반 보안 부트 체인이 상용 수준 신뢰성을 얻을 수 있다. 앞으로는 ePMP와 측정 부트, DICE 계열 키 파생이 더 자연스럽게 결합될 가능성이 크다. 핵심은 ePMP를 PMP의 옵션이 아니라, 특권 코드 하드닝 도구로 이해하는 것이다.

- **📢 섹션 요약 비유**: 가장 힘센 기사에게도 안전 규칙을 지키게 해야 성이 오래 안전한 것처럼, ePMP는 최상위 코드에도 규칙을 씌운다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| mseccfg | ePMP 강화 동작을 여는 핵심 [CSR](/knowledge-base/studynote/09_security/04_endpoint_security/169_pkcs10_csr/) |
| MML | Machine Mode [Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/), M-mode 규칙 강화의 중심 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) |
| RL | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 변경을 어렵게 해 [secure boot](/knowledge-base/studynote/02_operating_system/10_security/608_secure_boot/) 신뢰를 높임 |
| W^X | [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)와 실행을 분리해 코드 주입을 줄이는 원칙 |

### 📈 관련 키워드 및 발전 흐름도

```text
[PMP Region Design]
    |
    v
[ePMP Hardening Bits]
    |
    v
[Locked M-mode Policy]
    |
    +---> [Protected Boot Code]
    +---> [Fault on Bad Execute / Write]
```

이 흐름은 일반 PMP 설계 위에 ePMP 강화 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 적용하고, 최종적으로 봉인된 M-mode [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 부트 코드와 실행 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)를 만든다는 구조를 보여준다. 즉 ePMP의 핵심은 락 이후의 안정 상태다.

### 👶 어린이를 위한 3줄 비유 설명

1. 제일 큰 형도 장난감 방에서 뛰지 말라는 규칙을 지켜야 모두 안전해요.
2. ePMP는 컴퓨터에서 제일 힘센 프로그램에게도 그런 규칙을 더 엄격히 붙여 줘요.
3. 그래서 실수로 위험한 코드를 밟거나 쓰면 바로 막을 수 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 802 / 803

<- **이전**: [800. RISC-V PMP (Physical Memory Protection)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/800_riscv_pmp/)
**다음**: [802. 오픈소스 하드웨어 RoT (OpenTitan)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/802_opentitan/) ->

---
