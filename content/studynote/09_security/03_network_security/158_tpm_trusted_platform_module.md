---
title: 158. TPM (Trusted Platform Module) — 플랫폼 키 저장, 원격 증명
date: '2026-05-05'
tags:
- studynote-security
---

## 핵심 인사이트

> 1. **본질**: [[476_tpm|TPM]] ([[476_tpm|Trusted Platform Module]])은 단말 내부에 신뢰 루트 ([[487_root_of_trust|Root of Trust]])를 제공하는 보안 칩으로, 중요한 키를 안전하게 저장하고 부팅 상태를 측정한다.
> 2. **가치**: 디스크 암호화 키 [[571_protection_vs_security|보호]], 측정 부팅 ([[919_measured_boot|Measured Boot]]), 플랫폼 [[003_integrity|무결성]] [[395_verification_process_review|검증]]을 통해 [[001_operating_system_purpose|운영체제]]가 올라오기 전 단계부터 장치 신뢰를 확보할 수 있다.
> 3. **판단 포인트**: TPM은 고가치 중앙 키를 처리하는 [[475_hsm|HSM]] ([[157_hsm_hardware_security_module|Hardware Security Module]])의 대체재가 아니라, 개별 단말의 키 [[571_protection_vs_security|보호]]와 원격 증명을 담당하는 [[321_endpoint_security|엔드포인트 보안]] 구성 요소다.

---

## Ⅰ. 개요 및 필요성

TPM은 개인용 컴퓨터, 노트북, 서버 메인보드 등에 탑재되어 플랫폼의 암호키와 [[003_integrity|무결성]] 측정을 담당하는 전용 보안 모듈이다. 일반 소프트웨어만으로 키를 보관하면 [[001_operating_system_purpose|운영체제]] 침해, 메모리 노출, 오프라인 디스크 탈취 상황에서 [[571_protection_vs_security|보호]] 한계가 분명하다. TPM은 이런 취약점을 줄이기 위해, [[001_operating_system_purpose|운영체제]] 바깥의 하드웨어 경계 안에 키와 신뢰 기준을 두도록 설계되었다.

이 모듈이 특히 중요해진 이유는 부팅 [[459_quic_fec_forward_error_correction|초기]]가 가장 취약한 구간이기 때문이다. 사용자가 로그인하기 전, 심지어 [[001_operating_system_purpose|운영체제]]가 완전히 올라오기 전에는 보안 에이전트나 백신도 아직 제 역할을 못 한다. 공격자가 이 시점에 [[029_bootloader|부트로더]]나 [[032_firmware|펌웨어]]를 변조하면, 이후 보안 체계 전체를 우회할 수 있다.

TPM은 바로 이 지점에서 "정상적으로 부팅되었을 때만 키를 풀어 준다"는 조건부 신뢰를 제공한다. 그래서 [[397_bitlocker_windows_fde|BitLocker]] 같은 디스크 암호화, Windows Hello 같은 장치 [[303_authentication_authorization_patterns|인증]], 기업 단말 [[003_integrity|무결성]] [[395_verification_process_review|검증]]에서 핵심 역할을 한다.

- **📢 섹션 요약 비유**: TPM은 집 안 금고 열쇠를 아무 서랍에 두지 않고, 집 상태를 먼저 검사한 뒤에만 열쇠를 내주는 현관 경비원과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

TPM의 핵심 기능은 안전한 키 저장, 플랫폼 측정, 조건부 키 해제, 원격 증명이다. 부팅 과정에서 [[032_firmware|펌웨어]], [[029_bootloader|부트로더]], [[022_kernel_role|커널]] 같은 구성 요소의 해시가 순서대로 기록되고, [[476_tpm|TPM]] 내부 PCR (Platform Configuration [[175_register_addressing|Register]])에 누적된다. 이후 특정 키는 이 측정값이 예상 상태와 일치할 때만 복호화되도록 봉인 (Sealing)할 수 있다.

아래 그림은 [[476_tpm|TPM]] 기반 측정 부팅과 키 해제 흐름을 보여준다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ TPM measured boot and key release                                 │
├────────────────────────────────────────────────────────────────────┤
│ Power on                                                          │
│   -> Firmware hash   -> PCR extend                               │
│   -> Bootloader hash -> PCR extend                               │
│   -> Kernel hash     -> PCR extend                               │
│                                                                    │
│ Sealed key release rule: PCR value must match trusted state       │
│   Match    -> release disk key / device secret                    │
│   Mismatch -> deny release, recovery or alert                     │
└────────────────────────────────────────────────────────────────────┘
```

이 그림의 핵심은 TPM이 단순 저장소가 아니라 **상태를 조건으로 키 사용을 통제하는 장치**라는 점이다. 키 자체를 빼내 쓰게 하는 것이 아니라, "이 장치가 정상 상태일 때만 이 키를 사용하라"는 [[164_policy|정책]]을 강제한다. 따라서 공격자가 디스크만 떼어 가거나 부팅 경로를 바꿔도, 필요한 키를 쉽게 얻지 못한다.

| 구성 요소 | 역할 | 보안 의미 |
| :--- | :--- | :--- |
| PCR (Platform Configuration [[175_register_addressing|Register]]) | 부팅 구성 요소 측정값 누적 | 정상/비정상 부팅 상태 판단 기준 |
| Sealing | 특정 상태에서만 키 복호화 | 디스크 키, [[303_authentication_authorization_patterns|인증]] 비밀 [[571_protection_vs_security|보호]] |
| EK (Endorsement [[067_db_key_uniqueness_minimality|Key]]) | [[476_tpm|TPM]] 고유 [[655_ir_detection_analysis|식별]] 기반 키 | 장치 신뢰의 뿌리 제공 |
| Attestation [[067_db_key_uniqueness_minimality|Key]] | 측정값 서명 | 원격 증명에서 장치 상태 전달 |

[[476_tpm|TPM]] 2.0에서는 [[001_algorithm_definition|알고리즘]] 유연성과 활용 시나리오가 더 넓어졌다. 하지만 원리는 단순하다. 중요한 키를 [[001_operating_system_purpose|운영체제]] 밖에 두고, 그 키를 아무 때나 풀지 말고, 부팅 상태와 장치 [[003_integrity|무결성]]을 먼저 [[396_validation|확인]]하자는 것이다.

- **📢 섹션 요약 비유**: TPM은 금고만 지키는 경비가 아니라, 출입기록표를 [[396_validation|확인]]한 뒤 조건이 맞을 때만 금고 문을 여는 자동 심사대와 같다.

---

## Ⅲ. 비교 및 연결

TPM은 HSM이나 보안 구역인 [[478_tee|TEE]] ([[972_tee_based_ml|Trusted Execution Environment]])와 자주 함께 언급되지만 역할이 다르다. HSM은 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]]나 클라우드에서 고가치 중앙 키를 [[571_protection_vs_security|보호]]하고 대외 서명·복호 연산을 처리하는 장비다. TPM은 개별 단말 내부에 들어가, 장치 수준의 키 보관과 부팅 신뢰를 맡는다.

| 항목 | [[476_tpm|TPM]] | [[475_hsm|HSM]] | [[790_secure_enclave|Secure Enclave]] / [[478_tee|TEE]] |
| :--- | :--- | :--- | :--- |
| 주된 위치 | 개인용 컴퓨터·서버·노트북 메인보드 | [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]]·클라우드 | 모바일·[[131_soc|SoC]] ([[131_soc|System on Chip]]) 내부 |
| 주된 목적 | [[916_secure_boot|부팅 무결성]], 로컬 키 [[571_protection_vs_security|보호]] | 중앙 키 [[571_protection_vs_security|보호]]와 암호 연산 | 앱 격리와 민감 연산 [[571_protection_vs_security|보호]] |
| 대표 사례 | [[397_bitlocker_windows_fde|BitLocker]], 원격 증명 | [[303_authentication_authorization_patterns|인증]]기관 루트키, 결제 키, [[188_code_signing_software_authentication|코드 서명]] | [[702_biometric_authentication|생체 인증]], 앱 키 저장 |
| [[139_throughput|처리량]] 목표 | 낮음~중간 | 중간~높음 | 중간 |

TPM은 [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]] ([[667_zero_trust_runtime_integrity_measurement|Zero Trust]])와도 강하게 연결된다. 사용자의 비밀번호나 [[303_authentication_authorization_patterns|인증]]서만 보는 것이 아니라, "이 요청을 보내는 단말이 정상 상태인가"를 [[396_validation|확인]]하는 근거를 제공하기 때문이다. 원격 증명 ([[396_remote_attestation|Remote Attestation]])을 통해 장치는 자신의 측정 상태를 서명해 보내고, 서버는 이를 기반으로 접속 허용 여부를 판단할 수 있다.

즉 TPM은 키 보관 장치이면서 동시에 **장치 상태를 증명하는 하드웨어 신분증** 역할을 한다. 이 점이 단순 저장소와 가장 큰 차이다.

- **📢 섹션 요약 비유**: HSM이 은행 중앙 금고라면, TPM은 각 직원 노트북에 붙은 신분 [[396_validation|확인]] 봉인과 같다. 둘 다 보안 장치지만 지키는 범위와 목적이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 TPM은 디스크 암호화 자동 해제, [[608_secure_boot|보안 부팅]], 단말 [[303_authentication_authorization_patterns|인증]]서 [[571_protection_vs_security|보호]], 원격 근무 단말 신뢰 [[395_verification_process_review|검증]]에 널리 쓰인다. 예를 들어 기업은 [[476_tpm|TPM]] 기반 키와 측정 부팅을 활용해, 정상 [[032_firmware|펌웨어]]와 [[164_policy|정책]]을 유지한 장치만 [[983_vpn_virtual_private_network|VPN]] (Virtual Private Network)이나 [[309_saas|SaaS]] (Software [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]])에 접속하게 만들 수 있다. Windows 11의 [[476_tpm|TPM]] 2.0 요구사항도 이런 보안 기준 강화를 반영한다.

다만 TPM이 있다고 끝나는 것은 아니다. [[658_ir_recovery|복구]] 키 관리, [[032_firmware|펌웨어]] 업데이트 [[164_policy|정책]], [[608_secure_boot|Secure Boot]] [[009_config|설정]], PCR 바인딩 [[164_policy|정책]]을 함께 설계해야 한다. 또한 TPM은 고속 서명 처리 장치가 아니므로, 대량 [[191_transaction_concept_states|트랜잭션]] 서명이나 중앙 루트키 [[571_protection_vs_security|보호]] 용도로는 HSM과 같은 다른 계층 장비가 더 적합하다.

### 판단 [[435_checklist_based_testing|체크리스트]]

1. [[571_protection_vs_security|보호]]하려는 자산이 장치 로컬 키와 부팅 신뢰인가?
2. [[608_secure_boot|Secure Boot]], 디스크 암호화, [[658_ir_recovery|복구]] 키 [[164_policy|정책]]이 함께 설계되었는가?
3. 원격 증명 결과를 실제 접근 통제에 연결할 수 있는가?
4. TPM을 중앙 키 관리 장비처럼 과대해석하고 있지 않은가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- TPM만 있으면 모든 악성코드를 막는다고 생각하는 것
- [[658_ir_recovery|복구]] 키 관리 없이 [[476_tpm|TPM]] 기반 암호화만 켜 두는 것
- 중앙 공개키 기반구조 루트키 같은 고가치 서버 키까지 [[476_tpm|TPM]] 하나로 해결하려는 것

- **📢 섹션 요약 비유**: [[476_tpm|TPM]] 도입은 자물쇠 하나를 다는 일이 아니라, 열쇠를 누가 언제 받을지까지 규칙을 정하는 일이다. 경비원이 있어도 운영 규칙이 없으면 사고는 난다.

---

## Ⅴ. 기대효과 및 결론

TPM의 기대효과는 명확하다. 키 [[571_protection_vs_security|보호]]를 소프트웨어 권한 관리에서 하드웨어 신뢰 경계로 끌어올리고, 부팅 [[459_quic_fec_forward_error_correction|초기]] [[003_integrity|무결성]]을 [[395_verification_process_review|검증]]하며, 단말 상태를 원격에서 판단할 근거를 제공한다. 이 덕분에 디스크 탈취, 부팅 변조, 비정상 단말 접속 같은 위험에 대한 방어력이 높아진다.

하지만 TPM은 만능 해결책이 아니다. [[032_firmware|펌웨어]] 취약점, 운영 [[164_policy|정책]] 부실, [[658_ir_recovery|복구]] 체계 미흡, 사용자 권한 남용은 여전히 문제를 만든다. 따라서 TPM은 "모든 보안을 대신하는 칩"이 아니라, **엔드포인트 신뢰를 하드웨어에서 시작하게 만드는 기초 구성 요소**로 이해해야 한다.

결론적으로 TPM은 현대 단말 보안에서 중요한 전환점을 만든다. 보안을 [[001_operating_system_purpose|운영체제]] 안쪽에서만 보지 않고, 부팅과 키 [[571_protection_vs_security|보호]]의 출발점을 하드웨어까지 내리는 사고방식을 정착시켰기 때문이다. 그래서 TPM은 작은 칩이지만, 실제로는 장치 신뢰 사슬의 첫 고리다.

- **📢 섹션 요약 비유**: TPM은 보안 성벽 전체가 아니라, 성문이 열리기 전에 신분과 봉인을 먼저 [[396_validation|확인]]하는 첫 관문이다. 이 첫 관문이 단단해야 뒤의 보안도 의미가 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[608_secure_boot|Secure Boot]] | 신뢰된 부팅 경로를 강제하는 상위 메커니즘 |
| [[919_measured_boot|Measured Boot]] | TPM의 PCR 측정과 직접 연결되는 부팅 [[395_verification_process_review|검증]] 방식 |
| [[397_bitlocker_windows_fde|BitLocker]] | [[476_tpm|TPM]] 기반 키 봉인을 대표적으로 활용하는 사례 |
| [[396_remote_attestation|Remote Attestation]] | 단말 상태를 외부 서비스에 증명하는 기능 |
| [[475_hsm|HSM]] | TPM과 비교되는 중앙 키 [[571_protection_vs_security|보호]] 장비 |

### 📈 관련 키워드 및 발전 흐름도

```text
Local key storage problem
    │
    ▼
Secure Boot / Measured Boot
    │
    ▼
TPM 2.0
  (key sealing + platform measurement)
    │
    ▼
Remote Attestation
    │
    ▼
Zero Trust endpoint verification
```

이 흐름도는 TPM이 단순 키 저장소를 넘어, 장치 [[003_integrity|무결성]] [[395_verification_process_review|검증]]과 [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]] 접속 판단으로 확장되는 경로를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. TPM은 컴퓨터 안에 있는 아주 작은 경비 로봇이에요.
2. 이 로봇은 집 안이 멀쩡한지 먼저 [[396_validation|확인]]하고, 괜찮을 때만 보물상자 열쇠를 꺼내 줘요.
3. 그래서 나쁜 사람이 컴퓨터를 몰래 바꿔 놓으면, 로봇이 열쇠를 안 줘서 쉽게 못 열어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 211 / 1108

← **이전**: [[157_hsm_hardware_security_module|157. HSM (Hardware Security Module) — 물리적 키 보호]]
**다음**: [[159_pki_public_key_infrastructure|159. PKI (Public Key Infrastructure) — 공개키 인증서 체계]] →

---
